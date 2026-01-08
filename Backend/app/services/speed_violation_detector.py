from datetime import datetime
import cv2
import os
from app.models.traffic_violation import TrafficViolation
from app.services.telegram_notifier import get_telegram_notifier
from app.db.base import get_db, sync_engine  # Sử dụng sync engine cho thread riêng biệt nếu cần
from sqlalchemy.orm import Session
import asyncio
import threading

class SpeedViolationDetector:
    """
    Detector phát hiện xe chạy quá tốc độ
    """
    def __init__(self, speed_limit_car=60, speed_limit_motor=50):
        self.speed_limit_car = speed_limit_car      # km/h
        self.speed_limit_motor = speed_limit_motor  # km/h
        self.violation_cooldown = {} # {track_id: timestamp}
        self.cooldown_duration = 20.0 # giây (tránh bắt 1 xe nhiều lần)
        
        self.violation_images_dir = "./app/static/violation_images"
        os.makedirs(self.violation_images_dir, exist_ok=True)
        
        self.telegram_notifier = get_telegram_notifier()

    def _is_in_cooldown(self, track_id):
        if track_id in self.violation_cooldown:
            last_time = self.violation_cooldown[track_id]
            if (datetime.now() - last_time).total_seconds() < self.cooldown_duration:
                return True
        return False

    async def check_speed_violation(self, frame, track_id, vehicle_type, speed, bbox, camera_name="Unknown"):
        """
        Kiểm tra và xử lý vi phạm tốc độ
        Hàm này nên được gọi trong loop xử lý xe
        """
        # 1. Kiểm tra cooldown
        if self._is_in_cooldown(track_id):
            return None

        # 2. Kiểm tra giới hạn tốc độ
        limit = self.speed_limit_motor if vehicle_type in ['motor', 'motorbike', 'xe máy'] else self.speed_limit_car
        
        # Chỉ bắt vi phạm nếu vượt quá giới hạn + 5km/h (sai số cho phép)
        if speed > (limit + 5):
            print(f"🚨 PHÁT HIỆN QUÁ TỐC ĐỘ: Xe {vehicle_type} ID={track_id}, Tốc độ={speed}km/h (Giới hạn {limit}km/h)")

            # CHỈ xử lý vi phạm cho camera RTSP, BỎ QUA video test
            if camera_name != "camera_live":
                print(f"⏭️ Bỏ qua vi phạm tốc độ từ video test: {camera_name}")
                return None

            # 3. Tạo record vi phạm (CHỈ cho camera RTSP)
            current_time = datetime.now()

            # Lưu ảnh
            image_filename = f"speeding_{camera_name}_{current_time.strftime('%Y%m%d_%H%M%S_%f')}.jpg"
            image_path = os.path.join(self.violation_images_dir, image_filename)

            # Vẽ thông tin lên ảnh (Annotate)
            annotated_frame = frame.copy()
            x1, y1, x2, y2 = bbox
            cv2.rectangle(annotated_frame, (x1, y1), (x2, y2), (0, 0, 255), 2)
            cv2.putText(annotated_frame, f"SPEEDING: {speed}km/h (Limit: {limit})",
                       (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

            cv2.imwrite(image_path, annotated_frame)

            # 4. Lưu DB (Cần chạy trong async context hoặc thread khác nếu hàm cha là sync)
            # Ở đây giả sử context async
            violation_data = {
                'camera_name': camera_name,
                'violation_type': 'speeding',
                'vehicle_type': vehicle_type,
                'position_x': float((x1+x2)/2),
                'position_y': float(y2),
                'traffic_light_status': 'green', # Tốc độ thì thường đèn xanh
                'violated_at': current_time,
                'image_path': image_path,
                'note': f"Tốc độ đo được: {speed}km/h. Giới hạn: {limit}km/h",
                'confidence': 1.0
            }

            # KHÔNG GỬI TELEGRAM CHO VI PHẠM TỐC ĐỘ
            # Chỉ log và lưu DB, không spam Telegram
            print(f"✅ Đã lưu vi phạm tốc độ vào DB (không gửi Telegram)")
            # try:
            #     await self.telegram_notifier.send_violation_alert(annotated_frame, violation_data)
            #     print(f"📱 Đã gửi thông báo Telegram cho camera RTSP")
            # except Exception as e:
            #     print(f"Lỗi gửi Telegram speeding: {e}")

            # Lưu vào cooldown
            self.violation_cooldown[track_id] = current_time

            return violation_data

        return None
    
    def process_speed_violation_sync(self, frame, track_id, vehicle_type, speed, bbox, camera_name="Unknown"):
        """
        Phiên bản Sync của check_speed_violation để gọi từ luồng xử lý video
        """
        # 1. Kiểm tra cooldown
        if self._is_in_cooldown(track_id):
            return

        # 2. Kiểm tra giới hạn tốc độ
        limit = self.speed_limit_motor if vehicle_type in ['motor', 'motorbike', 'xe máy'] else self.speed_limit_car
        
        # Chỉ bắt vi phạm nếu vượt quá giới hạn + 5km/h
        if speed > (limit + 5):
            print(f"🚨 PHÁT HIỆN QUÁ TỐC ĐỘ: Xe {vehicle_type} ID={track_id}, Tốc độ={speed}km/h (Giới hạn {limit}km/h)")

            # CHỈ xử lý cho camera RTSP, BỎ QUA video test
            if camera_name != "camera_live":
                print(f"⏭️ Bỏ qua vi phạm tốc độ từ video test: {camera_name}")
                return

            # 3. Tạo record vi phạm (CHỈ cho camera RTSP)
            current_time = datetime.now()

            # Resize image if too big for storage/telegram
            # frame_resized = cv2.resize(frame, (1280, 720)) if frame.shape[1] > 1280 else frame

            image_filename = f"speeding_{camera_name}_{track_id}_{current_time.strftime('%Y%m%d_%H%M%S')}.jpg"
            image_path = os.path.join(self.violation_images_dir, image_filename)

            # Vẽ thông tin
            annotated_frame = frame.copy()
            x1, y1, x2, y2 = bbox
            # Đảm bảo bbox nằm trong frame
            h, w = frame.shape[:2]
            x1, y1 = max(0, x1), max(0, y1)
            x2, y2 = min(w, x2), min(h, y2)

            cv2.rectangle(annotated_frame, (x1, y1), (x2, y2), (0, 0, 255), 2)
            cv2.putText(annotated_frame, f"SPEED: {speed}km/h (Limit: {limit})",
                       (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

            try:
                cv2.imwrite(image_path, annotated_frame)
            except Exception as e:
                print(f"Lỗi save ảnh speeding: {e}")
                return

            # Data
            violation_data = {
                'camera_name': camera_name,
                'violation_type': 'speeding',
                'vehicle_type': vehicle_type,
                'position_x': float((x1+x2)/2),
                'position_y': float(y2),
                'traffic_light_status': 'green',
                'violated_at': current_time,
                'image_path': image_path,
                'note': f"Tốc độ: {speed}km/h (Giới hạn: {limit}km/h)",
                'confidence': 1.0,
                'is_processed': False
            }

            # 4. Lưu DB (KHÔNG gửi Telegram)
            # Lưu DB
            self.save_violation_to_db_sync(violation_data)

            # KHÔNG GỬI TELEGRAM CHO VI PHẠM TỐC ĐỘ
            # Chỉ gửi Telegram cho vi phạm vượt đèn đỏ
            # def send_telegram():
            #     try:
            #         asyncio.run(self.telegram_notifier.send_violation_alert(annotated_frame, violation_data))
            #         print(f"📱 Đã gửi thông báo Telegram cho camera RTSP")
            #     except Exception as e:
            #         print(f"Telegram error: {e}")
            # threading.Thread(target=send_telegram, daemon=True).start()

            print(f"✅ Đã lưu vi phạm tốc độ từ camera RTSP vào DB (không gửi Telegram)")

            # Update cooldown
            self.violation_cooldown[track_id] = current_time

    # Helper để lưu DB đồng bộ (nếu cần gọi từ luồng sync)
    def save_violation_to_db_sync(self, violation_data):
        try:
            # Tạo session mới
            with Session(sync_engine) as session:
                violation = TrafficViolation(**violation_data)
                session.add(violation)
                session.commit()
                print("✅ Đã lưu vi phạm tốc độ vào DB")
        except Exception as e:
            print(f"❌ Lỗi lưu DB speeding: {e}")

