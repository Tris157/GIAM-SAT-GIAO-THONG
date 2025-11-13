"""
Report Export Service - Generate PDF and Excel reports with charts
"""
import io
import os
from datetime import datetime
from typing import List, Optional
import matplotlib
matplotlib.use('Agg')  # Non-GUI backend
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak, Image
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from openpyxl import Workbook
from openpyxl.chart import BarChart, LineChart, PieChart, Reference
from openpyxl.styles import Font, Alignment, PatternFill
from openpyxl.utils import get_column_letter

from app.schemas.traffic_record import TrafficStatistics, HourlyStatistics, DailyTrend, RoadComparison


class ReportExportService:
    """Service for exporting traffic reports to PDF and Excel with visualizations"""

    @staticmethod
    def generate_pdf_report(
        statistics: List[TrafficStatistics],
        hourly_trends: List[HourlyStatistics],
        daily_trends: List[DailyTrend],
        road_comparisons: List[RoadComparison],
        start_date: str,
        end_date: str
    ) -> bytes:
        """
        Generate comprehensive PDF report with charts

        Returns:
            PDF file as bytes
        """
        buffer = io.BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=A4)
        story = []

        # Styles
        styles = getSampleStyleSheet()
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=24,
            textColor=colors.HexColor('#1E40AF'),
            spaceAfter=30,
            alignment=TA_CENTER
        )
        heading_style = ParagraphStyle(
            'CustomHeading',
            parent=styles['Heading2'],
            fontSize=16,
            textColor=colors.HexColor('#3B82F6'),
            spaceAfter=12,
            spaceBefore=12
        )

        # Title
        title = Paragraph("Báo Cáo Giao Thông Thông Minh", title_style)
        story.append(title)

        # Report info
        info_text = f"""
        <b>Thời gian:</b> {start_date} đến {end_date}<br/>
        <b>Ngày tạo báo cáo:</b> {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}<br/>
        <b>Số lượng đường giám sát:</b> {len(statistics)}<br/>
        """
        story.append(Paragraph(info_text, styles['Normal']))
        story.append(Spacer(1, 0.3 * inch))

        # Statistics Summary Table
        story.append(Paragraph("1. Tổng Quan Thống Kê", heading_style))

        if statistics:
            # Prepare table data
            table_data = [[
                'Tên Đường',
                'Số Bản Ghi',
                'TB Số Xe',
                'Max Xe',
                'TB Tốc Độ',
                'Giờ Cao Điểm',
                'Tỷ Lệ Tắc (%)'
            ]]

            for stat in statistics:
                table_data.append([
                    stat.road_name,
                    str(stat.total_records),
                    f"{stat.avg_vehicles:.1f}",
                    str(stat.max_vehicles),
                    f"{stat.avg_speed:.1f} km/h",
                    f"{stat.peak_hour}:00" if stat.peak_hour is not None else "N/A",
                    f"{stat.congestion_rate:.1f}%"
                ])

            # Create table
            table = Table(table_data, colWidths=[1.5*inch, 0.8*inch, 0.8*inch, 0.7*inch, 1*inch, 1*inch, 1*inch])
            table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#3B82F6')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 10),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                ('GRID', (0, 0), (-1, -1), 1, colors.black),
                ('FONTSIZE', (0, 1), (-1, -1), 9),
            ]))
            story.append(table)
            story.append(Spacer(1, 0.3 * inch))

        # Generate and add hourly chart
        if hourly_trends:
            story.append(Paragraph("2. Xu Hướng Theo Giờ", heading_style))
            hourly_chart_path = ReportExportService._create_hourly_chart(hourly_trends)
            if hourly_chart_path:
                img = Image(hourly_chart_path, width=5*inch, height=3*inch)
                story.append(img)
                story.append(Spacer(1, 0.2 * inch))
                os.remove(hourly_chart_path)  # Clean up

        # Generate and add daily trend chart
        if daily_trends:
            story.append(Paragraph("3. Xu Hướng Theo Ngày", heading_style))
            daily_chart_path = ReportExportService._create_daily_chart(daily_trends)
            if daily_chart_path:
                img = Image(daily_chart_path, width=5*inch, height=3*inch)
                story.append(img)
                story.append(Spacer(1, 0.2 * inch))
                os.remove(daily_chart_path)

        # Road comparison chart
        if road_comparisons and len(road_comparisons) > 1:
            story.append(PageBreak())
            story.append(Paragraph("4. So Sánh Các Tuyến Đường", heading_style))
            comparison_chart_path = ReportExportService._create_comparison_chart(road_comparisons)
            if comparison_chart_path:
                img = Image(comparison_chart_path, width=5*inch, height=3*inch)
                story.append(img)
                os.remove(comparison_chart_path)

        # Build PDF
        doc.build(story)
        buffer.seek(0)
        return buffer.getvalue()

    @staticmethod
    def _create_hourly_chart(hourly_trends: List[HourlyStatistics]) -> Optional[str]:
        """Create hourly trend chart"""
        try:
            fig, ax1 = plt.subplots(figsize=(10, 6))

            hours = [h.hour for h in hourly_trends]
            vehicles = [h.avg_vehicles for h in hourly_trends]
            speeds = [h.avg_speed for h in hourly_trends]

            # Plot vehicles
            color = 'tab:blue'
            ax1.set_xlabel('Giờ trong ngày', fontsize=12)
            ax1.set_ylabel('Số xe trung bình', color=color, fontsize=12)
            ax1.bar(hours, vehicles, color=color, alpha=0.6, label='Số xe')
            ax1.tick_params(axis='y', labelcolor=color)
            ax1.set_xticks(range(0, 24, 2))

            # Plot speeds on second y-axis
            ax2 = ax1.twinx()
            color = 'tab:red'
            ax2.set_ylabel('Tốc độ TB (km/h)', color=color, fontsize=12)
            ax2.plot(hours, speeds, color=color, marker='o', linewidth=2, label='Tốc độ')
            ax2.tick_params(axis='y', labelcolor=color)

            plt.title('Lưu Lượng và Tốc Độ Theo Giờ', fontsize=14, fontweight='bold')
            fig.tight_layout()

            # Save to temp file
            temp_file = f'temp_hourly_{datetime.now().timestamp()}.png'
            plt.savefig(temp_file, dpi=150, bbox_inches='tight')
            plt.close()

            return temp_file

        except Exception as e:
            print(f"Error creating hourly chart: {e}")
            return None

    @staticmethod
    def _create_daily_chart(daily_trends: List[DailyTrend]) -> Optional[str]:
        """Create daily trend chart"""
        try:
            fig, ax = plt.subplots(figsize=(10, 6))

            dates = [datetime.strptime(d.date, '%Y-%m-%d') for d in daily_trends]
            vehicles = [d.avg_vehicles for d in daily_trends]
            max_vehicles = [d.max_vehicles for d in daily_trends]

            ax.plot(dates, vehicles, marker='o', linewidth=2, label='TB số xe', color='tab:blue')
            ax.plot(dates, max_vehicles, marker='s', linewidth=2, label='Max số xe', color='tab:orange')

            ax.set_xlabel('Ngày', fontsize=12)
            ax.set_ylabel('Số xe', fontsize=12)
            ax.set_title('Xu Hướng Lưu Lượng Theo Ngày', fontsize=14, fontweight='bold')
            ax.legend()
            ax.grid(True, alpha=0.3)

            # Format x-axis
            ax.xaxis.set_major_formatter(mdates.DateFormatter('%d/%m'))
            plt.xticks(rotation=45)

            fig.tight_layout()

            # Save to temp file
            temp_file = f'temp_daily_{datetime.now().timestamp()}.png'
            plt.savefig(temp_file, dpi=150, bbox_inches='tight')
            plt.close()

            return temp_file

        except Exception as e:
            print(f"Error creating daily chart: {e}")
            return None

    @staticmethod
    def _create_comparison_chart(comparisons: List[RoadComparison]) -> Optional[str]:
        """Create road comparison chart"""
        try:
            fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))

            roads = [c.road_name for c in comparisons]
            vehicles = [c.avg_vehicles for c in comparisons]
            congestion = [c.congestion_rate for c in comparisons]

            # Bar chart for vehicles
            ax1.bar(roads, vehicles, color='tab:blue', alpha=0.7)
            ax1.set_xlabel('Tuyến đường', fontsize=11)
            ax1.set_ylabel('Số xe trung bình', fontsize=11)
            ax1.set_title('So Sánh Lưu Lượng', fontsize=12, fontweight='bold')
            plt.setp(ax1.xaxis.get_majorticklabels(), rotation=45, ha='right')

            # Bar chart for congestion
            colors_list = ['green' if c < 30 else 'orange' if c < 60 else 'red' for c in congestion]
            ax2.bar(roads, congestion, color=colors_list, alpha=0.7)
            ax2.set_xlabel('Tuyến đường', fontsize=11)
            ax2.set_ylabel('Tỷ lệ tắc nghẽn (%)', fontsize=11)
            ax2.set_title('So Sánh Tắc Nghẽn', fontsize=12, fontweight='bold')
            plt.setp(ax2.xaxis.get_majorticklabels(), rotation=45, ha='right')

            fig.tight_layout()

            # Save to temp file
            temp_file = f'temp_comparison_{datetime.now().timestamp()}.png'
            plt.savefig(temp_file, dpi=150, bbox_inches='tight')
            plt.close()

            return temp_file

        except Exception as e:
            print(f"Error creating comparison chart: {e}")
            return None

    @staticmethod
    def generate_excel_report(
        statistics: List[TrafficStatistics],
        hourly_trends: List[HourlyStatistics],
        daily_trends: List[DailyTrend],
        road_comparisons: List[RoadComparison],
        start_date: str,
        end_date: str
    ) -> bytes:
        """
        Generate comprehensive Excel report with multiple sheets and charts

        Returns:
            Excel file as bytes
        """
        buffer = io.BytesIO()
        wb = Workbook()

        # Remove default sheet
        if 'Sheet' in wb.sheetnames:
            wb.remove(wb['Sheet'])

        # Sheet 1: Summary
        ws_summary = wb.create_sheet("Tổng Quan")
        ReportExportService._create_summary_sheet(ws_summary, statistics, start_date, end_date)

        # Sheet 2: Hourly Trends
        if hourly_trends:
            ws_hourly = wb.create_sheet("Xu Hướng Theo Giờ")
            ReportExportService._create_hourly_sheet(ws_hourly, hourly_trends)

        # Sheet 3: Daily Trends
        if daily_trends:
            ws_daily = wb.create_sheet("Xu Hướng Theo Ngày")
            ReportExportService._create_daily_sheet(ws_daily, daily_trends)

        # Sheet 4: Road Comparison
        if road_comparisons:
            ws_comparison = wb.create_sheet("So Sánh Tuyến Đường")
            ReportExportService._create_comparison_sheet(ws_comparison, road_comparisons)

        # Save to buffer
        wb.save(buffer)
        buffer.seek(0)
        return buffer.getvalue()

    @staticmethod
    def _create_summary_sheet(ws, statistics: List[TrafficStatistics], start_date: str, end_date: str):
        """Create summary sheet in Excel"""
        # Title
        ws['A1'] = 'BÁO CÁO GIAO THÔNG THÔNG MINH'
        ws['A1'].font = Font(size=18, bold=True, color='1E40AF')
        ws.merge_cells('A1:G1')
        ws['A1'].alignment = Alignment(horizontal='center')

        # Info
        ws['A3'] = f'Thời gian: {start_date} đến {end_date}'
        ws['A4'] = f'Ngày tạo: {datetime.now().strftime("%d/%m/%Y %H:%M:%S")}'

        # Headers
        headers = ['Tên Đường', 'Số Bản Ghi', 'TB Số Xe', 'Max Xe', 'TB Tốc Độ', 'Giờ Cao Điểm', 'Tỷ Lệ Tắc (%)']
        for col, header in enumerate(headers, 1):
            cell = ws.cell(row=6, column=col, value=header)
            cell.font = Font(bold=True, color='FFFFFF')
            cell.fill = PatternFill(start_color='3B82F6', end_color='3B82F6', fill_type='solid')
            cell.alignment = Alignment(horizontal='center')

        # Data
        for row, stat in enumerate(statistics, 7):
            ws.cell(row=row, column=1, value=stat.road_name)
            ws.cell(row=row, column=2, value=stat.total_records)
            ws.cell(row=row, column=3, value=round(stat.avg_vehicles, 1))
            ws.cell(row=row, column=4, value=stat.max_vehicles)
            ws.cell(row=row, column=5, value=f"{stat.avg_speed:.1f}")
            ws.cell(row=row, column=6, value=f"{stat.peak_hour}:00" if stat.peak_hour is not None else "N/A")
            ws.cell(row=row, column=7, value=f"{stat.congestion_rate:.1f}%")

        # Auto-adjust column widths
        for col in range(1, 8):
            ws.column_dimensions[get_column_letter(col)].width = 15

    @staticmethod
    def _create_hourly_sheet(ws, hourly_trends: List[HourlyStatistics]):
        """Create hourly trends sheet with chart"""
        # Headers
        ws['A1'] = 'Giờ'
        ws['B1'] = 'TB Số Xe'
        ws['C1'] = 'TB Tốc Độ (km/h)'
        ws['D1'] = 'Trạng Thái'

        for cell in ['A1', 'B1', 'C1', 'D1']:
            ws[cell].font = Font(bold=True)
            ws[cell].fill = PatternFill(start_color='3B82F6', end_color='3B82F6', fill_type='solid')
            ws[cell].font = Font(bold=True, color='FFFFFF')

        # Data
        for row, trend in enumerate(hourly_trends, 2):
            ws.cell(row=row, column=1, value=f"{trend.hour}:00")
            ws.cell(row=row, column=2, value=round(trend.avg_vehicles, 1))
            ws.cell(row=row, column=3, value=round(trend.avg_speed, 1))
            ws.cell(row=row, column=4, value=trend.traffic_status)

        # Create line chart
        chart = LineChart()
        chart.title = "Lưu Lượng Theo Giờ"
        chart.y_axis.title = "Số xe"
        chart.x_axis.title = "Giờ"

        data = Reference(ws, min_col=2, min_row=1, max_row=len(hourly_trends) + 1)
        cats = Reference(ws, min_col=1, min_row=2, max_row=len(hourly_trends) + 1)
        chart.add_data(data, titles_from_data=True)
        chart.set_categories(cats)

        ws.add_chart(chart, "F2")

    @staticmethod
    def _create_daily_sheet(ws, daily_trends: List[DailyTrend]):
        """Create daily trends sheet with chart"""
        # Headers
        headers = ['Ngày', 'TB Số Xe', 'Max Số Xe', 'TB Tốc Độ', 'Giờ Cao Điểm']
        for col, header in enumerate(headers, 1):
            cell = ws.cell(row=1, column=col, value=header)
            cell.font = Font(bold=True, color='FFFFFF')
            cell.fill = PatternFill(start_color='3B82F6', end_color='3B82F6', fill_type='solid')

        # Data
        for row, trend in enumerate(daily_trends, 2):
            ws.cell(row=row, column=1, value=trend.date)
            ws.cell(row=row, column=2, value=round(trend.avg_vehicles, 1))
            ws.cell(row=row, column=3, value=trend.max_vehicles)
            ws.cell(row=row, column=4, value=round(trend.avg_speed, 1))
            ws.cell(row=row, column=5, value=f"{trend.peak_hour}:00")

        # Create line chart
        chart = LineChart()
        chart.title = "Xu Hướng Theo Ngày"
        chart.y_axis.title = "Số xe"
        chart.x_axis.title = "Ngày"

        data = Reference(ws, min_col=2, min_row=1, max_col=3, max_row=len(daily_trends) + 1)
        cats = Reference(ws, min_col=1, min_row=2, max_row=len(daily_trends) + 1)
        chart.add_data(data, titles_from_data=True)
        chart.set_categories(cats)

        ws.add_chart(chart, "G2")

    @staticmethod
    def _create_comparison_sheet(ws, comparisons: List[RoadComparison]):
        """Create road comparison sheet with charts"""
        # Headers
        headers = ['Tên Đường', 'TB Số Xe', 'TB Tốc Độ', 'Tỷ Lệ Tắc (%)', 'Số Bản Ghi']
        for col, header in enumerate(headers, 1):
            cell = ws.cell(row=1, column=col, value=header)
            cell.font = Font(bold=True, color='FFFFFF')
            cell.fill = PatternFill(start_color='3B82F6', end_color='3B82F6', fill_type='solid')

        # Data
        for row, comp in enumerate(comparisons, 2):
            ws.cell(row=row, column=1, value=comp.road_name)
            ws.cell(row=row, column=2, value=round(comp.avg_vehicles, 1))
            ws.cell(row=row, column=3, value=round(comp.avg_speed, 1))
            ws.cell(row=row, column=4, value=round(comp.congestion_rate, 1))
            ws.cell(row=row, column=5, value=comp.total_records)

        # Create bar chart
        chart = BarChart()
        chart.title = "So Sánh Lưu Lượng"
        chart.y_axis.title = "Số xe"

        data = Reference(ws, min_col=2, min_row=1, max_row=len(comparisons) + 1)
        cats = Reference(ws, min_col=1, min_row=2, max_row=len(comparisons) + 1)
        chart.add_data(data, titles_from_data=True)
        chart.set_categories(cats)

        ws.add_chart(chart, "G2")


# Global service instance
report_export_service = ReportExportService()
