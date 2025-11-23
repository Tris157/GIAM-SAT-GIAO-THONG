"""
Telegram Notifier Service
Gửi cảnh báo vi phạm giao thông real-time qua Telegram Bot
"""

import os
import asyncio
import logging
from typing import Optional
from datetime import datetime
import requests
import cv2
import numpy as np
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

logger = logging.getLogger(__name__)


class TelegramNotifier:
    """
    Service gửi thông báo vi phạm giao thông qua Telegram Bot

    Features:
    - Gửi ảnh bằng chứng vi phạm
    - Gửi thông tin chi tiết (thời gian, loại xe, biển số)
    - Async để không block luồng chính
    - Retry mechanism khi gửi thất bại
    """

    def __init__(self):
        """Khởi tạo Telegram Bot"""
        self.bot_token = os.getenv("TELEGRAM_BOT_TOKEN")
        self.chat_id = os.getenv("TELEGRAM_CHAT_ID")
        self.api_base_url = f"https://api.telegram.org/bot{self.bot_token}"

        # Kiểm tra config
        if not self.bot_token or self.bot_token == "YOUR_BOT_TOKEN_HERE":
            logger.warning("⚠️ TELEGRAM_BOT_TOKEN chưa được cấu hình trong .env")
            self.enabled = False
            return

        if not self.chat_id or self.chat_id == "YOUR_CHAT_ID_HERE":
            logger.warning("⚠️ TELEGRAM_CHAT_ID chưa được cấu hình trong .env")
            self.enabled = False
            return

        # Kiểm tra kết nối bot
        try:
            response = requests.get(f"{self.api_base_url}/getMe", timeout=10)
            if response.status_code == 200:
                self.enabled = True
                logger.info("✅ Telegram Bot đã được khởi tạo thành công")
            else:
                self.enabled = False
                logger.error("❌ Bot token không hợp lệ")
        except Exception as e:
            logger.error(f"❌ Lỗi khởi tạo Telegram Bot: {e}")
            self.enabled = False


    async def send_violation_alert(
        self,
        image: np.ndarray,
        violation_data: dict,
        max_retries: int = 3
    ) -> bool:
        """
        Gửi cảnh báo vi phạm vượt đèn đỏ qua Telegram

        Args:
            image: Frame ảnh vi phạm (numpy array BGR)
            violation_data: Dict chứa thông tin vi phạm
                - timestamp: Thời gian vi phạm
                - vehicle_type: Loại xe (car/motor)
                - license_plate: Biển số xe (nếu có)
                - camera_name: Tên camera
                - location: Vị trí camera
            max_retries: Số lần retry nếu gửi thất bại

        Returns:
            bool: True nếu gửi thành công, False nếu thất bại
        """

        if not self.enabled:
            logger.warning("⚠️ Telegram Bot chưa được kích hoạt (thiếu config)")
            return False

        try:
            # Chuyển đổi image từ numpy array sang bytes
            _, img_encoded = cv2.imencode('.jpg', image)
            img_bytes = img_encoded.tobytes()

            # Format thông tin vi phạm
            timestamp = violation_data.get('timestamp', datetime.now())
            vehicle_type = violation_data.get('vehicle_type', 'Unknown')
            license_plate = violation_data.get('license_plate', 'Không nhận diện được')
            camera_name = violation_data.get('camera_name', 'Camera Live')
            location = violation_data.get('location', 'Hà Nội')

            # Định dạng loại xe
            vehicle_type_vn = "Ô tô" if vehicle_type == "car" else "Xe máy" if vehicle_type == "motor" else "Phương tiện"

            # Tạo message cảnh báo (no markdown for compatibility)
            message = f"""CANH BAO VI PHAM GIAO THONG

Loai vi pham: Vuot den do
Loai xe: {vehicle_type_vn}
Bien so: {license_plate}
Vi tri: {location}
Camera: {camera_name}
Thoi gian: {timestamp.strftime('%d/%m/%Y %H:%M:%S')}

He thong da tu dong ghi nhan vi pham.
Anh bang chung dinh kem ben duoi.
"""

            # Gửi ảnh kèm caption (với retry)
            for attempt in range(max_retries):
                try:
                    # Sử dụng requests để gửi ảnh
                    files = {'photo': ('violation.jpg', img_bytes, 'image/jpeg')}
                    data = {
                        'chat_id': self.chat_id,
                        'caption': message
                    }

                    response = requests.post(
                        f"{self.api_base_url}/sendPhoto",
                        files=files,
                        data=data,
                        timeout=30
                    )

                    if response.status_code == 200:
                        logger.info(f"✅ Đã gửi cảnh báo vi phạm qua Telegram: {vehicle_type_vn} - {license_plate}")
                        return True
                    else:
                        logger.error(f"❌ Telegram API error: {response.text}")
                        if attempt < max_retries - 1:
                            await asyncio.sleep(1)
                        else:
                            return False

                except Exception as e:
                    if attempt < max_retries - 1:
                        logger.warning(f"⚠️ Gửi Telegram thất bại (lần {attempt + 1}), retry sau 1s: {e}")
                        await asyncio.sleep(1)
                    else:
                        logger.error(f"❌ Gửi Telegram thất bại sau {max_retries} lần thử: {e}")
                        return False

        except Exception as e:
            logger.error(f"❌ Lỗi khi gửi cảnh báo Telegram: {e}")
            return False


    async def send_test_message(self) -> bool:
        """
        Gửi tin nhắn test để kiểm tra kết nối Telegram Bot

        Returns:
            bool: True nếu gửi thành công
        """

        if not self.enabled:
            logger.error("❌ Telegram Bot chưa được kích hoạt")
            return False

        try:
            message = """TEST TELEGRAM BOT

Ket noi thanh cong!
Bot canh bao vi pham giao thong da san sang.

He thong se tu dong gui canh bao khi phat hien:
  - Vuot den do
  - Anh bang chung vi pham
  - Thong tin thoi gian & vi tri

Powered by Smart Traffic Monitoring System
"""

            response = requests.post(
                f"{self.api_base_url}/sendMessage",
                json={
                    'chat_id': self.chat_id,
                    'text': message
                },
                timeout=10
            )

            if response.status_code == 200:
                logger.info("✅ Gửi test message thành công!")
                return True
            else:
                logger.error(f"❌ Gửi test message thất bại: {response.text}")
                return False

        except Exception as e:
            logger.error(f"❌ Gửi test message thất bại: {e}")
            return False


    async def send_system_report(
        self,
        report_data: dict,
        max_retries: int = 3
    ) -> bool:
        """
        Gửi báo cáo tổng kết tình hình hệ thống qua Telegram

        Args:
            report_data: Dict chứa thông tin báo cáo
                - period: Khoảng thời gian báo cáo (hôm nay/tuần này/tháng này)
                - total_violations: Tổng số vi phạm
                - violations_by_type: Dict {vehicle_type: count}
                - processed_count: Số vi phạm đã xử lý
                - unprocessed_count: Số vi phạm chưa xử lý
                - top_violation_hours: List giờ cao điểm vi phạm
                - camera_status: Dict trạng thái camera
                - traffic_stats: Thống kê lưu lượng giao thông
                - system_uptime: Thời gian hệ thống chạy
            max_retries: Số lần retry nếu gửi thất bại

        Returns:
            bool: True nếu gửi thành công
        """

        if not self.enabled:
            logger.warning("⚠️ Telegram Bot chưa được kích hoạt")
            return False

        try:
            # Lấy dữ liệu từ report_data
            period = report_data.get('period', 'Hôm nay')
            total_violations = report_data.get('total_violations', 0)
            violations_by_type = report_data.get('violations_by_type', {})
            processed_count = report_data.get('processed_count', 0)
            unprocessed_count = report_data.get('unprocessed_count', 0)
            top_hours = report_data.get('top_violation_hours', [])
            camera_status = report_data.get('camera_status', {})
            traffic_stats = report_data.get('traffic_stats', {})
            system_uptime = report_data.get('system_uptime', 'N/A')

            # Tính toán các chỉ số
            processing_rate = (processed_count / total_violations * 100) if total_violations > 0 else 0

            # Format thông tin vi phạm theo loại xe
            violations_breakdown = ""
            for vehicle_type, count in violations_by_type.items():
                vehicle_icon = "🚗" if vehicle_type == "car" else "🏍️" if vehicle_type == "motor" else "🚙"
                vehicle_name = "Ô tô" if vehicle_type == "car" else "Xe máy" if vehicle_type == "motor" else vehicle_type
                violations_breakdown += f"  {vehicle_icon} {vehicle_name}: {count} lượt\n"

            # Format giờ cao điểm
            peak_hours = ""
            for i, hour_data in enumerate(top_hours[:3], 1):
                peak_hours += f"  {i}. {hour_data.get('hour', 'N/A')}h - {hour_data.get('count', 0)} vi phạm\n"

            # Format trạng thái camera
            camera_info = ""
            for camera_name, status in camera_status.items():
                status_icon = "🟢" if status == "online" else "🔴"
                camera_info += f"  {status_icon} {camera_name}: {status.upper()}\n"

            # Format thống kê giao thông
            traffic_info = f"""
📊 **Lưu lượng giao thông:**
  🚗 Ô tô: {traffic_stats.get('cars', 0)} xe
  🏍️ Xe máy: {traffic_stats.get('motors', 0)} xe
  🚚 Xe tải: {traffic_stats.get('trucks', 0)} xe
  🚌 Xe buýt: {traffic_stats.get('buses', 0)} xe
"""

            # Tạo message báo cáo
            message = f"""
📈 **BÁO CÁO TỔNG KẾT HỆ THỐNG** 📈
━━━━━━━━━━━━━━━━━━━━━━━━━━━

⏰ **Thời gian:** {period}
🕐 **Thời điểm:** {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}

━━━━━━━━━━━━━━━━━━━━━━━━━━━
🚨 **VI PHẠM GIAO THÔNG**
━━━━━━━━━━━━━━━━━━━━━━━━━━━

📊 **Tổng số vi phạm:** {total_violations} lượt

📋 **Chi tiết theo loại xe:**
{violations_breakdown if violations_breakdown else '  Không có dữ liệu'}

✅ **Đã xử lý:** {processed_count} ({processing_rate:.1f}%)
⏳ **Chưa xử lý:** {unprocessed_count}

⏰ **Giờ cao điểm vi phạm:**
{peak_hours if peak_hours else '  Không có dữ liệu'}

━━━━━━━━━━━━━━━━━━━━━━━━━━━
📹 **TRẠNG THÁI CAMERA**
━━━━━━━━━━━━━━━━━━━━━━━━━━━

{camera_info if camera_info else '  Không có camera nào đang hoạt động'}

━━━━━━━━━━━━━━━━━━━━━━━━━━━
🚦 **THỐNG KÊ GIAO THÔNG**
━━━━━━━━━━━━━━━━━━━━━━━━━━━
{traffic_info}

━━━━━━━━━━━━━━━━━━━━━━━━━━━
⚙️ **HỆ THỐNG**
━━━━━━━━━━━━━━━━━━━━━━━━━━━

🖥️ **Uptime:** {system_uptime}
🟢 **Trạng thái:** Đang hoạt động bình thường

━━━━━━━━━━━━━━━━━━━━━━━━━━━

💡 **Khuyến nghị:**
{'⚠️ Cần xử lý ' + str(unprocessed_count) + ' vi phạm chưa được xử lý' if unprocessed_count > 0 else '✅ Tất cả vi phạm đã được xử lý'}

⚡ Powered by Smart Traffic Monitoring System
"""

            # Gửi báo cáo (với retry)
            for attempt in range(max_retries):
                try:
                    response = requests.post(
                        f"{self.api_base_url}/sendMessage",
                        json={
                            'chat_id': self.chat_id,
                            'text': message
                        },
                        timeout=30
                    )

                    if response.status_code == 200:
                        logger.info(f"✅ Đã gửi báo cáo tổng kết qua Telegram: {period}")
                        return True
                    else:
                        logger.error(f"❌ Telegram API error: {response.text}")
                        if attempt < max_retries - 1:
                            await asyncio.sleep(1)
                        else:
                            return False

                except Exception as e:
                    if attempt < max_retries - 1:
                        logger.warning(f"⚠️ Gửi báo cáo thất bại (lần {attempt + 1}), retry sau 1s: {e}")
                        await asyncio.sleep(1)
                    else:
                        logger.error(f"❌ Gửi báo cáo thất bại sau {max_retries} lần thử: {e}")
                        return False

        except Exception as e:
            logger.error(f"❌ Lỗi khi gửi báo cáo Telegram: {e}")
            return False


# Singleton instance
_telegram_notifier = None

def get_telegram_notifier() -> TelegramNotifier:
    """
    Get singleton instance của TelegramNotifier

    Returns:
        TelegramNotifier instance
    """
    global _telegram_notifier
    if _telegram_notifier is None:
        _telegram_notifier = TelegramNotifier()
    return _telegram_notifier
