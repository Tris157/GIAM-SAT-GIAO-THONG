from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi.responses import StreamingResponse, FileResponse, Response
from sqlalchemy.orm import Session
from sqlalchemy import func, and_, or_, desc
from datetime import datetime, timedelta
from typing import List, Optional
import io
import csv
import json

from app.db.database import get_db
from app.db.base import get_db_sync
from app.models.traffic_record import TrafficRecord
from app.schemas.traffic_record import (
    TrafficRecordCreate,
    TrafficRecordResponse,
    ReportFilter,
    TrafficStatistics,
    HourlyStatistics,
    DailyTrend,
    RoadComparison,
    ReportResponse
)
from app.services.report_export_service import report_export_service

router = APIRouter()


# Helper function to save traffic data periodically
async def save_traffic_record(db: Session, road_name: str, data: dict):
    """Save traffic data to database for reporting"""
    now = datetime.now()

    total_vehicles = data.get("count_car", 0) + data.get("count_motor", 0)
    avg_speed = 0.0
    if data.get("speed_car", 0) > 0 and data.get("speed_motor", 0) > 0:
        avg_speed = (data.get("speed_car", 0) + data.get("speed_motor", 0)) / 2
    elif data.get("speed_car", 0) > 0:
        avg_speed = data.get("speed_car", 0)
    elif data.get("speed_motor", 0) > 0:
        avg_speed = data.get("speed_motor", 0)

    # Determine traffic status
    traffic_status = "clear"
    if total_vehicles > 15:
        traffic_status = "congested"
    elif total_vehicles > 8:
        traffic_status = "busy"

    record = TrafficRecord(
        road_name=road_name,
        count_car=data.get("count_car", 0),
        count_motor=data.get("count_motor", 0),
        total_vehicles=total_vehicles,
        speed_car=data.get("speed_car", 0.0),
        speed_motor=data.get("speed_motor", 0.0),
        avg_speed=avg_speed,
        traffic_status=traffic_status,
        hour_of_day=now.hour,
        day_of_week=now.weekday(),
        date=now.strftime("%Y-%m-%d")
    )

    db.add(record)
    db.commit()
    db.refresh(record)
    return record


@router.post("/traffic-records/", response_model=TrafficRecordResponse)
async def create_traffic_record(
    road_name: str,
    data: dict,
    db: Session = Depends(get_db)
):
    """Manually save a traffic record"""
    return await save_traffic_record(db, road_name, data)


@router.get("/traffic-records/", response_model=List[TrafficRecordResponse])
async def get_traffic_records(
    road_name: Optional[str] = None,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    limit: int = Query(100, le=1000),
    db: Session = Depends(get_db)
):
    """Get historical traffic records with filters"""
    query = db.query(TrafficRecord)

    if road_name:
        query = query.filter(TrafficRecord.road_name == road_name)

    if start_date:
        query = query.filter(TrafficRecord.date >= start_date)

    if end_date:
        query = query.filter(TrafficRecord.date <= end_date)

    records = query.order_by(desc(TrafficRecord.recorded_at)).limit(limit).all()
    return records


# Helper function (SYNC) for PDF/Excel exports
def _generate_report_sync(
    filter_params: ReportFilter,
    db: Session
) -> ReportResponse:
    """Generate comprehensive traffic report (SYNC version for report exports)"""

    # Build base query
    query = db.query(TrafficRecord)

    if filter_params.road_names:
        query = query.filter(TrafficRecord.road_name.in_(filter_params.road_names))

    if filter_params.start_date:
        query = query.filter(TrafficRecord.date >= filter_params.start_date)

    if filter_params.end_date:
        query = query.filter(TrafficRecord.date <= filter_params.end_date)

    # Get date range
    start_date = filter_params.start_date or (datetime.now() - timedelta(days=7)).strftime("%Y-%m-%d")
    end_date = filter_params.end_date or datetime.now().strftime("%Y-%m-%d")

    # Calculate statistics per road
    statistics = []
    road_comparisons = []

    roads = filter_params.road_names if filter_params.road_names else \
        db.query(TrafficRecord.road_name).distinct().all()

    if not filter_params.road_names:
        roads = [r[0] for r in roads]

    for road in roads:
        road_query = query.filter(TrafficRecord.road_name == road)
        records = road_query.all()

        if not records:
            continue

        total_records = len(records)
        vehicles = [r.total_vehicles for r in records]
        speeds = [r.avg_speed for r in records if r.avg_speed > 0]

        # Calculate peak hours
        hourly_avg = db.query(
            TrafficRecord.hour_of_day,
            func.avg(TrafficRecord.total_vehicles).label('avg_vehicles')
        ).filter(
            TrafficRecord.road_name == road,
            TrafficRecord.date >= start_date,
            TrafficRecord.date <= end_date
        ).group_by(TrafficRecord.hour_of_day).all()

        peak_hour = None
        off_peak_hour = None
        if hourly_avg:
            sorted_hours = sorted(hourly_avg, key=lambda x: x.avg_vehicles, reverse=True)
            peak_hour = sorted_hours[0].hour_of_day if sorted_hours else None
            off_peak_hour = sorted_hours[-1].hour_of_day if sorted_hours else None

        # Calculate congestion rate
        congested_count = sum(1 for r in records if r.traffic_status == "congested")
        congestion_rate = (congested_count / total_records * 100) if total_records > 0 else 0

        stat = TrafficStatistics(
            road_name=road,
            total_records=total_records,
            avg_vehicles=sum(vehicles) / len(vehicles) if vehicles else 0,
            max_vehicles=max(vehicles) if vehicles else 0,
            min_vehicles=min(vehicles) if vehicles else 0,
            avg_speed=sum(speeds) / len(speeds) if speeds else 0,
            peak_hour=peak_hour,
            off_peak_hour=off_peak_hour,
            congestion_rate=congestion_rate
        )
        statistics.append(stat)

        # For comparison
        road_comparisons.append(RoadComparison(
            road_name=road,
            avg_vehicles=stat.avg_vehicles,
            avg_speed=stat.avg_speed,
            congestion_rate=congestion_rate,
            total_records=total_records
        ))

    # Calculate hourly trends (overall)
    hourly_trends = []
    for hour in range(24):
        hour_records = query.filter(TrafficRecord.hour_of_day == hour).all()
        if hour_records:
            avg_vehicles = sum(r.total_vehicles for r in hour_records) / len(hour_records)
            avg_speed = sum(r.avg_speed for r in hour_records if r.avg_speed > 0)
            avg_speed = avg_speed / len([r for r in hour_records if r.avg_speed > 0]) if any(r.avg_speed > 0 for r in hour_records) else 0

            status = "clear"
            if avg_vehicles > 15:
                status = "congested"
            elif avg_vehicles > 8:
                status = "busy"

            hourly_trends.append(HourlyStatistics(
                hour=hour,
                avg_vehicles=avg_vehicles,
                avg_speed=avg_speed,
                traffic_status=status
            ))

    # Calculate daily trends
    daily_trends = []
    daily_data = db.query(
        TrafficRecord.date,
        func.avg(TrafficRecord.total_vehicles).label('avg_vehicles'),
        func.max(TrafficRecord.total_vehicles).label('max_vehicles'),
        func.avg(TrafficRecord.avg_speed).label('avg_speed')
    ).filter(
        and_(
            TrafficRecord.date >= start_date,
            TrafficRecord.date <= end_date
        )
    ).group_by(TrafficRecord.date).order_by(TrafficRecord.date).all()

    for day_data in daily_data:
        # Find peak hour for this day
        peak_hour_data = db.query(
            TrafficRecord.hour_of_day,
            func.avg(TrafficRecord.total_vehicles).label('avg_vehicles')
        ).filter(
            TrafficRecord.date == day_data.date
        ).group_by(TrafficRecord.hour_of_day).order_by(desc('avg_vehicles')).first()

        daily_trends.append(DailyTrend(
            date=day_data.date,
            avg_vehicles=day_data.avg_vehicles,
            max_vehicles=day_data.max_vehicles,
            avg_speed=day_data.avg_speed or 0,
            peak_hour=peak_hour_data.hour_of_day if peak_hour_data else 0
        ))

    return ReportResponse(
        period=filter_params.period,
        start_date=start_date,
        end_date=end_date,
        statistics=statistics,
        hourly_trends=hourly_trends,
        daily_trends=daily_trends,
        road_comparisons=road_comparisons
    )


# API endpoint (uses sync session for .query() support)
@router.post("/reports/generate", response_model=ReportResponse)
def generate_report(
    filter_params: ReportFilter,
    db: Session = Depends(get_db_sync)
):
    """Generate comprehensive traffic report via API"""
    return _generate_report_sync(filter_params, db)


@router.get("/reports/export/csv")
async def export_csv(
    road_name: Optional[str] = None,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """Export traffic records to CSV"""
    query = db.query(TrafficRecord)

    if road_name:
        query = query.filter(TrafficRecord.road_name == road_name)
    if start_date:
        query = query.filter(TrafficRecord.date >= start_date)
    if end_date:
        query = query.filter(TrafficRecord.date <= end_date)

    records = query.order_by(TrafficRecord.recorded_at).all()

    # Create CSV in memory
    output = io.StringIO()
    writer = csv.writer(output)

    # Write header
    writer.writerow([
        'ID', 'Road Name', 'Date', 'Time', 'Hour', 'Day of Week',
        'Cars', 'Motors', 'Total Vehicles', 'Car Speed', 'Motor Speed',
        'Avg Speed', 'Traffic Status'
    ])

    # Write data
    for record in records:
        writer.writerow([
            record.id,
            record.road_name,
            record.date,
            record.recorded_at.strftime('%H:%M:%S'),
            record.hour_of_day,
            record.day_of_week,
            record.count_car,
            record.count_motor,
            record.total_vehicles,
            record.speed_car,
            record.speed_motor,
            record.avg_speed,
            record.traffic_status
        ])

    output.seek(0)

    return StreamingResponse(
        iter([output.getvalue()]),
        media_type="text/csv",
        headers={
            "Content-Disposition": f"attachment; filename=traffic_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        }
    )


@router.get("/reports/export/json")
async def export_json(
    road_name: Optional[str] = None,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """Export traffic records to JSON"""
    query = db.query(TrafficRecord)

    if road_name:
        query = query.filter(TrafficRecord.road_name == road_name)
    if start_date:
        query = query.filter(TrafficRecord.date >= start_date)
    if end_date:
        query = query.filter(TrafficRecord.date <= end_date)

    records = query.order_by(TrafficRecord.recorded_at).all()

    data = []
    for record in records:
        data.append({
            "id": record.id,
            "road_name": record.road_name,
            "date": record.date,
            "recorded_at": record.recorded_at.isoformat(),
            "hour_of_day": record.hour_of_day,
            "day_of_week": record.day_of_week,
            "count_car": record.count_car,
            "count_motor": record.count_motor,
            "total_vehicles": record.total_vehicles,
            "speed_car": record.speed_car,
            "speed_motor": record.speed_motor,
            "avg_speed": record.avg_speed,
            "traffic_status": record.traffic_status
        })

    json_str = json.dumps(data, indent=2)

    return StreamingResponse(
        iter([json_str]),
        media_type="application/json",
        headers={
            "Content-Disposition": f"attachment; filename=traffic_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        }
    )


@router.post("/reports/export/pdf")
async def export_pdf_report(
    filter_params: ReportFilter,
    db: Session = Depends(get_db_sync)
):
    """
    Export comprehensive traffic report to PDF with charts

    This generates a professional PDF report including:
    - Summary statistics table
    - Hourly traffic trends chart
    - Daily traffic trends chart
    - Road comparison charts
    """
    # Generate report data first (sync call, no await)
    report = _generate_report_sync(filter_params, db)

    # Generate PDF
    pdf_bytes = report_export_service.generate_pdf_report(
        statistics=report.statistics,
        hourly_trends=report.hourly_trends or [],
        daily_trends=report.daily_trends or [],
        road_comparisons=report.road_comparisons or [],
        start_date=report.start_date,
        end_date=report.end_date
    )

    return Response(
        content=pdf_bytes,
        media_type="application/pdf",
        headers={
            "Content-Disposition": f"attachment; filename=traffic_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
        }
    )


@router.post("/reports/export/excel")
async def export_excel_report(
    filter_params: ReportFilter,
    db: Session = Depends(get_db_sync)
):
    """
    Export comprehensive traffic report to Excel with multiple sheets and charts

    The Excel file includes:
    - Summary sheet with formatted table
    - Hourly trends sheet with line chart
    - Daily trends sheet with line chart
    - Road comparison sheet with bar chart
    """
    # Generate report data first (sync call, no await)
    report = _generate_report_sync(filter_params, db)

    # Generate Excel
    excel_bytes = report_export_service.generate_excel_report(
        statistics=report.statistics,
        hourly_trends=report.hourly_trends or [],
        daily_trends=report.daily_trends or [],
        road_comparisons=report.road_comparisons or [],
        start_date=report.start_date,
        end_date=report.end_date
    )

    return Response(
        content=excel_bytes,
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={
            "Content-Disposition": f"attachment; filename=traffic_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
        }
    )
