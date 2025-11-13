"""
Traffic Recording Service - Auto-save traffic data to database for analytics
"""
from datetime import datetime, timedelta
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, and_, or_
from typing import List, Dict, Optional
from app.models.traffic_record import TrafficRecord
from app.schemas.traffic_record import (
    TrafficRecordCreate,
    TrafficStatistics,
    HourlyStatistics,
    DailyTrend,
    RoadComparison
)
import logging

logger = logging.getLogger(__name__)


class TrafficRecordingService:
    """Service to record and query traffic data"""

    @staticmethod
    async def save_traffic_data(db: AsyncSession, road_name: str, traffic_data: Dict) -> TrafficRecord:
        """
        Save traffic data snapshot to database

        Args:
            db: Database session
            road_name: Name of the road
            traffic_data: Dict with count_car, count_motor, speed_car, speed_motor

        Returns:
            TrafficRecord object
        """
        try:
            now = datetime.now()

            count_car = traffic_data.get('count_car', 0)
            count_motor = traffic_data.get('count_motor', 0)
            total_vehicles = count_car + count_motor

            speed_car = traffic_data.get('speed_car', 0.0)
            speed_motor = traffic_data.get('speed_motor', 0.0)

            # Calculate average speed weighted by vehicle count
            if total_vehicles > 0:
                avg_speed = (speed_car * count_car + speed_motor * count_motor) / total_vehicles
            else:
                avg_speed = 0.0

            # Determine traffic status
            if total_vehicles > 15:
                traffic_status = "congested"
            elif total_vehicles > 8:
                traffic_status = "busy"
            else:
                traffic_status = "clear"

            record = TrafficRecord(
                road_name=road_name,
                count_car=count_car,
                count_motor=count_motor,
                total_vehicles=total_vehicles,
                speed_car=round(speed_car, 2),
                speed_motor=round(speed_motor, 2),
                avg_speed=round(avg_speed, 2),
                traffic_status=traffic_status,
                hour_of_day=now.hour,
                day_of_week=now.weekday(),
                date=now.strftime('%Y-%m-%d')
            )

            db.add(record)
            await db.commit()
            await db.refresh(record)

            return record

        except Exception as e:
            logger.error(f"Error saving traffic data: {e}")
            await db.rollback()
            raise

    @staticmethod
    async def get_records(
        db: AsyncSession,
        road_name: Optional[str] = None,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        limit: int = 1000
    ) -> List[TrafficRecord]:
        """Get traffic records with filters"""
        try:
            query = select(TrafficRecord)

            filters = []
            if road_name:
                filters.append(TrafficRecord.road_name == road_name)
            if start_date:
                filters.append(TrafficRecord.date >= start_date)
            if end_date:
                filters.append(TrafficRecord.date <= end_date)

            if filters:
                query = query.where(and_(*filters))

            query = query.order_by(TrafficRecord.recorded_at.desc()).limit(limit)

            result = await db.execute(query)
            return result.scalars().all()

        except Exception as e:
            logger.error(f"Error fetching records: {e}")
            return []

    @staticmethod
    async def get_statistics(
        db: AsyncSession,
        road_names: Optional[List[str]] = None,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None
    ) -> List[TrafficStatistics]:
        """Get aggregated statistics per road"""
        try:
            # Build base query
            query = select(
                TrafficRecord.road_name,
                func.count(TrafficRecord.id).label('total_records'),
                func.avg(TrafficRecord.total_vehicles).label('avg_vehicles'),
                func.max(TrafficRecord.total_vehicles).label('max_vehicles'),
                func.min(TrafficRecord.total_vehicles).label('min_vehicles'),
                func.avg(TrafficRecord.avg_speed).label('avg_speed'),
                func.sum(
                    func.case(
                        (TrafficRecord.traffic_status == 'congested', 1),
                        else_=0
                    )
                ).label('congested_count')
            )

            # Apply filters
            filters = []
            if road_names:
                filters.append(TrafficRecord.road_name.in_(road_names))
            if start_date:
                filters.append(TrafficRecord.date >= start_date)
            if end_date:
                filters.append(TrafficRecord.date <= end_date)

            if filters:
                query = query.where(and_(*filters))

            query = query.group_by(TrafficRecord.road_name)

            result = await db.execute(query)
            rows = result.all()

            statistics = []
            for row in rows:
                # Get peak hours for this road
                peak_hour = await TrafficRecordingService._get_peak_hour(
                    db, row.road_name, start_date, end_date, is_peak=True
                )
                off_peak_hour = await TrafficRecordingService._get_peak_hour(
                    db, row.road_name, start_date, end_date, is_peak=False
                )

                congestion_rate = (row.congested_count / row.total_records * 100) if row.total_records > 0 else 0.0

                statistics.append(TrafficStatistics(
                    road_name=row.road_name,
                    total_records=row.total_records,
                    avg_vehicles=round(row.avg_vehicles, 2),
                    max_vehicles=row.max_vehicles,
                    min_vehicles=row.min_vehicles,
                    avg_speed=round(row.avg_speed, 2),
                    peak_hour=peak_hour,
                    off_peak_hour=off_peak_hour,
                    congestion_rate=round(congestion_rate, 2)
                ))

            return statistics

        except Exception as e:
            logger.error(f"Error calculating statistics: {e}")
            return []

    @staticmethod
    async def _get_peak_hour(
        db: AsyncSession,
        road_name: str,
        start_date: Optional[str],
        end_date: Optional[str],
        is_peak: bool = True
    ) -> Optional[int]:
        """Get peak or off-peak hour for a road"""
        try:
            query = select(
                TrafficRecord.hour_of_day,
                func.avg(TrafficRecord.total_vehicles).label('avg_vehicles')
            ).where(TrafficRecord.road_name == road_name)

            if start_date:
                query = query.where(TrafficRecord.date >= start_date)
            if end_date:
                query = query.where(TrafficRecord.date <= end_date)

            query = query.group_by(TrafficRecord.hour_of_day)

            if is_peak:
                query = query.order_by(func.avg(TrafficRecord.total_vehicles).desc())
            else:
                query = query.order_by(func.avg(TrafficRecord.total_vehicles).asc())

            result = await db.execute(query.limit(1))
            row = result.first()

            return row.hour_of_day if row else None

        except Exception as e:
            logger.error(f"Error getting peak hour: {e}")
            return None

    @staticmethod
    async def get_hourly_trends(
        db: AsyncSession,
        road_name: str,
        date: Optional[str] = None
    ) -> List[HourlyStatistics]:
        """Get hourly traffic trends for a specific road and date"""
        try:
            query = select(
                TrafficRecord.hour_of_day,
                func.avg(TrafficRecord.total_vehicles).label('avg_vehicles'),
                func.avg(TrafficRecord.avg_speed).label('avg_speed'),
                func.mode().within_group(TrafficRecord.traffic_status).label('traffic_status')
            ).where(TrafficRecord.road_name == road_name)

            if date:
                query = query.where(TrafficRecord.date == date)

            query = query.group_by(TrafficRecord.hour_of_day).order_by(TrafficRecord.hour_of_day)

            result = await db.execute(query)
            rows = result.all()

            hourly_stats = []
            for row in rows:
                hourly_stats.append(HourlyStatistics(
                    hour=row.hour_of_day,
                    avg_vehicles=round(row.avg_vehicles, 2),
                    avg_speed=round(row.avg_speed, 2),
                    traffic_status=row.traffic_status or "clear"
                ))

            return hourly_stats

        except Exception as e:
            logger.error(f"Error getting hourly trends: {e}")
            return []

    @staticmethod
    async def get_daily_trends(
        db: AsyncSession,
        road_name: str,
        start_date: str,
        end_date: str
    ) -> List[DailyTrend]:
        """Get daily traffic trends for a date range"""
        try:
            # Get daily aggregates
            query = select(
                TrafficRecord.date,
                func.avg(TrafficRecord.total_vehicles).label('avg_vehicles'),
                func.max(TrafficRecord.total_vehicles).label('max_vehicles'),
                func.avg(TrafficRecord.avg_speed).label('avg_speed')
            ).where(
                and_(
                    TrafficRecord.road_name == road_name,
                    TrafficRecord.date >= start_date,
                    TrafficRecord.date <= end_date
                )
            ).group_by(TrafficRecord.date).order_by(TrafficRecord.date)

            result = await db.execute(query)
            rows = result.all()

            daily_trends = []
            for row in rows:
                # Get peak hour for this specific day
                peak_query = select(
                    TrafficRecord.hour_of_day,
                    func.avg(TrafficRecord.total_vehicles).label('avg_vehicles')
                ).where(
                    and_(
                        TrafficRecord.road_name == road_name,
                        TrafficRecord.date == row.date
                    )
                ).group_by(TrafficRecord.hour_of_day).order_by(
                    func.avg(TrafficRecord.total_vehicles).desc()
                ).limit(1)

                peak_result = await db.execute(peak_query)
                peak_row = peak_result.first()
                peak_hour = peak_row.hour_of_day if peak_row else 0

                daily_trends.append(DailyTrend(
                    date=row.date,
                    avg_vehicles=round(row.avg_vehicles, 2),
                    max_vehicles=row.max_vehicles,
                    avg_speed=round(row.avg_speed, 2),
                    peak_hour=peak_hour
                ))

            return daily_trends

        except Exception as e:
            logger.error(f"Error getting daily trends: {e}")
            return []

    @staticmethod
    async def compare_roads(
        db: AsyncSession,
        road_names: List[str],
        start_date: Optional[str] = None,
        end_date: Optional[str] = None
    ) -> List[RoadComparison]:
        """Compare traffic across multiple roads"""
        try:
            query = select(
                TrafficRecord.road_name,
                func.avg(TrafficRecord.total_vehicles).label('avg_vehicles'),
                func.avg(TrafficRecord.avg_speed).label('avg_speed'),
                func.count(TrafficRecord.id).label('total_records'),
                func.sum(
                    func.case(
                        (TrafficRecord.traffic_status == 'congested', 1),
                        else_=0
                    )
                ).label('congested_count')
            ).where(TrafficRecord.road_name.in_(road_names))

            if start_date:
                query = query.where(TrafficRecord.date >= start_date)
            if end_date:
                query = query.where(TrafficRecord.date <= end_date)

            query = query.group_by(TrafficRecord.road_name)

            result = await db.execute(query)
            rows = result.all()

            comparisons = []
            for row in rows:
                congestion_rate = (row.congested_count / row.total_records * 100) if row.total_records > 0 else 0.0

                comparisons.append(RoadComparison(
                    road_name=row.road_name,
                    avg_vehicles=round(row.avg_vehicles, 2),
                    avg_speed=round(row.avg_speed, 2),
                    congestion_rate=round(congestion_rate, 2),
                    total_records=row.total_records
                ))

            return comparisons

        except Exception as e:
            logger.error(f"Error comparing roads: {e}")
            return []

    @staticmethod
    async def delete_old_records(db: AsyncSession, days_to_keep: int = 90) -> int:
        """Delete records older than specified days (for data cleanup)"""
        try:
            cutoff_date = (datetime.now() - timedelta(days=days_to_keep)).strftime('%Y-%m-%d')

            query = select(TrafficRecord).where(TrafficRecord.date < cutoff_date)
            result = await db.execute(query)
            records = result.scalars().all()

            count = len(records)
            for record in records:
                await db.delete(record)

            await db.commit()
            logger.info(f"Deleted {count} old traffic records")

            return count

        except Exception as e:
            logger.error(f"Error deleting old records: {e}")
            await db.rollback()
            return 0


# Global service instance
traffic_recording_service = TrafficRecordingService()
