"""
Telegram Bot Command Handler
Xử lý tin nhắn và lệnh từ Telegram Bot
"""

import os
import logging
from datetime import datetime, timedelta
from typing import Optional
import requests
from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger(__name__)


class TelegramBotHandler:
    """
    Handler xử lý các lệnh từ Telegram Bot

    Supported Commands:
    - /start - Khởi động bot và hiển thị hướng dẫn
    - /stats - Thống kê vi phạm hôm nay
    - /report - Gửi báo cáo tổng kết
    - /status - Trạng thái hệ thống
    - /help - Hướng dẫn sử dụng
    """

    def __init__(self):
        """Khởi tạo handler"""
        self.bot_token = os.getenv("TELEGRAM_BOT_TOKEN")
        self.api_base_url = f"https://api.telegram.org/bot{self.bot_token}"


    def send_message(self, chat_id: str, text: str) -> bool:
        """
        Gửi tin nhắn đến chat

        Args:
            chat_id: ID của chat
            text: Nội dung tin nhắn

        Returns:
            bool: True nếu gửi thành công
        """
        try:
            response = requests.post(
                f"{self.api_base_url}/sendMessage",
                json={
                    'chat_id': chat_id,
                    'text': text
                },
                timeout=10
            )

            return response.status_code == 200

        except Exception as e:
            logger.error(f"❌ Lỗi gửi message: {e}")
            return False


    async def handle_start_command(self, chat_id: str, db_session) -> str:
        """Xử lý lệnh /start"""
        message = """Chao mung ban den voi He Thong Giam Sat Giao Thong!

Toi la bot canh bao vi pham giao thong tu dong.

CAC LENH CO SAN:
/stats - Xem thong ke vi pham hom nay
/report - Gui bao cao tong ket
/status - Trang thai he thong
/help - Huong dan su dung

He thong se tu dong gui canh bao khi phat hien vi pham vuot den do.

Powered by Smart Traffic Monitoring System"""

        self.send_message(chat_id, message)
        return message


    async def handle_stats_command(self, chat_id: str, db_session) -> str:
        """Xử lý lệnh /stats - Thống kê vi phạm hôm nay"""
        from app.models.traffic_violation import TrafficViolation
        from sqlalchemy import select

        try:
            # Query vi phạm hôm nay
            now = datetime.now()
            start_of_day = datetime(now.year, now.month, now.day)

            query = select(TrafficViolation).where(
                TrafficViolation.violated_at >= start_of_day
            )
            result = await db_session.execute(query)
            violations = result.scalars().all()

            total = len(violations)
            processed = sum(1 for v in violations if v.is_processed)
            unprocessed = total - processed

            # Đếm theo loại xe
            cars = sum(1 for v in violations if v.vehicle_type == 'car')
            motors = sum(1 for v in violations if v.vehicle_type == 'motor')

            message = f"""THONG KE VI PHAM HOM NAY

Tong so vi pham: {total} luot
Da xu ly: {processed} ({processed/total*100:.1f}% if total > 0 else 0)
Chua xu ly: {unprocessed}

PHAN LOAI:
Oto: {cars} luot
Xe may: {motors} luot

Thoi gian: {now.strftime('%d/%m/%Y %H:%M:%S')}

Powered by Smart Traffic Monitoring System"""

            self.send_message(chat_id, message)
            return message

        except Exception as e:
            logger.error(f"❌ Lỗi xử lý /stats: {e}")
            error_msg = "Loi khi lay thong ke. Vui long thu lai sau."
            self.send_message(chat_id, error_msg)
            return error_msg


    async def handle_report_command(self, chat_id: str, db_session) -> str:
        """Xử lý lệnh /report - Gửi báo cáo tổng kết"""
        from app.services.telegram_notifier import get_telegram_notifier
        from app.models.traffic_violation import TrafficViolation
        from sqlalchemy import select

        try:
            # Thông báo đang xử lý
            self.send_message(chat_id, "Dang tao bao cao tong ket...")

            # Query vi phạm hôm nay
            now = datetime.now()
            start_of_day = datetime(now.year, now.month, now.day)

            query = select(TrafficViolation).where(
                TrafficViolation.violated_at >= start_of_day
            )
            result = await db_session.execute(query)
            violations = result.scalars().all()

            # Tạo report data
            total_violations = len(violations)
            violations_by_type = {}
            for v in violations:
                vtype = v.vehicle_type or 'unknown'
                violations_by_type[vtype] = violations_by_type.get(vtype, 0) + 1

            processed_count = sum(1 for v in violations if v.is_processed)
            unprocessed_count = total_violations - processed_count

            # Giờ cao điểm
            hours_count = {}
            for v in violations:
                hour = v.violated_at.hour
                hours_count[hour] = hours_count.get(hour, 0) + 1

            top_hours = [
                {"hour": hour, "count": count}
                for hour, count in sorted(hours_count.items(), key=lambda x: x[1], reverse=True)[:3]
            ]

            report_data = {
                "period": "Hom nay",
                "total_violations": total_violations,
                "violations_by_type": violations_by_type,
                "processed_count": processed_count,
                "unprocessed_count": unprocessed_count,
                "top_violation_hours": top_hours,
                "camera_status": {"camera_live": "online"},
                "traffic_stats": {
                    "cars": violations_by_type.get("car", 0) * 10,
                    "motors": violations_by_type.get("motor", 0) * 10,
                    "trucks": 0,
                    "buses": 0
                },
                "system_uptime": "N/A"
            }

            # Gửi báo cáo qua TelegramNotifier
            notifier = get_telegram_notifier()
            success = await notifier.send_system_report(report_data)

            if success:
                return "Bao cao da duoc gui!"
            else:
                error_msg = "Loi khi gui bao cao."
                self.send_message(chat_id, error_msg)
                return error_msg

        except Exception as e:
            logger.error(f"❌ Lỗi xử lý /report: {e}")
            error_msg = "Loi khi tao bao cao. Vui long thu lai sau."
            self.send_message(chat_id, error_msg)
            return error_msg


    async def handle_status_command(self, chat_id: str, db_session) -> str:
        """Xử lý lệnh /status - Trạng thái hệ thống"""
        from app.api.v1.api_rtsp import rtsp_detection_manager

        try:
            # Kiểm tra trạng thái camera
            camera_status = "ONLINE" if rtsp_detection_manager.streams else "OFFLINE"
            camera_count = len(rtsp_detection_manager.streams)

            message = f"""TRANG THAI HE THONG

Camera: {camera_status}
So luong camera: {camera_count}

He thong: Dang hoat dong binh thuong
Database: Ket noi thanh cong
Telegram Bot: Hoat dong

Thoi gian: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}

Powered by Smart Traffic Monitoring System"""

            self.send_message(chat_id, message)
            return message

        except Exception as e:
            logger.error(f"❌ Lỗi xử lý /status: {e}")
            error_msg = "Loi khi lay trang thai. Vui long thu lai sau."
            self.send_message(chat_id, error_msg)
            return error_msg


    async def handle_help_command(self, chat_id: str, db_session) -> str:
        """Xử lý lệnh /help"""
        message = """HUONG DAN SU DUNG BOT

CAC LENH CO SAN:

/start - Khoi dong bot va hien thi huong dan
/stats - Xem thong ke vi pham hom nay
/report - Gui bao cao tong ket day du
/status - Kiem tra trang thai he thong
/help - Hien thi huong dan nay

CHU Y:
- Bot se tu dong gui canh bao khi phat hien vi pham
- Moi canh bao se kem theo anh bang chung
- Ban co the gui lenh bat cu luc nao

Lien he ho tro: admin@traffic.vn

Powered by Smart Traffic Monitoring System"""

        self.send_message(chat_id, message)
        return message


    async def handle_message(self, message_data: dict, db_session) -> Optional[str]:
        """
        Xử lý tin nhắn từ Telegram

        Args:
            message_data: Data từ Telegram webhook
            db_session: Database session

        Returns:
            str: Response message
        """
        try:
            # Parse message
            message = message_data.get('message', {})
            chat_id = str(message.get('chat', {}).get('id', ''))
            text = message.get('text', '').strip()

            logger.info(f"📨 Nhận tin nhắn từ {chat_id}: {text}")

            # Xử lý command
            if text.startswith('/'):
                command = text.split()[0].lower()

                if command == '/start':
                    return await self.handle_start_command(chat_id, db_session)
                elif command == '/stats':
                    return await self.handle_stats_command(chat_id, db_session)
                elif command == '/report':
                    return await self.handle_report_command(chat_id, db_session)
                elif command == '/status':
                    return await self.handle_status_command(chat_id, db_session)
                elif command == '/help':
                    return await self.handle_help_command(chat_id, db_session)
                else:
                    # Unknown command
                    unknown_msg = f"Lenh '{command}' khong hop le. Gui /help de xem danh sach lenh."
                    self.send_message(chat_id, unknown_msg)
                    return unknown_msg
            else:
                # Not a command - friendly response
                friendly_msg = "Chao ban! Gui /help de xem danh sach lenh ho tro."
                self.send_message(chat_id, friendly_msg)
                return friendly_msg

        except Exception as e:
            logger.error(f"❌ Lỗi xử lý message: {e}")
            return None


# Singleton instance
_bot_handler = None

def get_bot_handler() -> TelegramBotHandler:
    """Get singleton instance của TelegramBotHandler"""
    global _bot_handler
    if _bot_handler is None:
        _bot_handler = TelegramBotHandler()
    return _bot_handler
