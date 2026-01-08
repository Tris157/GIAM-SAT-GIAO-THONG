"""
DEMO: Traffic Light Color Detection
Phát hiện màu đèn tín hiệu giao thông (ĐỎ-VÀNG-XANH)

Chức năng:
- Kết nối camera phụ (RTSP hoặc USB)
- Phát hiện màu đèn tín hiệu real-time
- Hiển thị kết quả trên màn hình
- Vẽ ROI (Region of Interest) cho đèn tín hiệu

Tác giả: Smart Traffic Monitoring Team
Phiên bản: 1.0
Ngày: 2025-12-20
"""

import cv2
import numpy as np
from typing import Tuple, Optional
import json
import os
from datetime import datetime


class TrafficLightDetector:
    """Lớp phát hiện màu đèn tín hiệu giao thông"""

    def __init__(self, roi_config_path: str = "app/config/traffic_light_roi.json"):
        """
        Khởi tạo detector

        Args:
            roi_config_path: Đường dẫn đến file config ROI
        """
        self.roi_config_path = roi_config_path
        self.roi = None
        self.load_roi()

        # Định nghĩa ngưỡng màu trong không gian HSV
        # ĐỎ (có 2 dải vì đỏ nằm ở 2 đầu của vòng tròn màu)
        self.RED_LOWER_1 = np.array([0, 100, 100])
        self.RED_UPPER_1 = np.array([10, 255, 255])
        self.RED_LOWER_2 = np.array([160, 100, 100])
        self.RED_UPPER_2 = np.array([180, 255, 255])

        # VÀNG
        self.YELLOW_LOWER = np.array([15, 100, 100])
        self.YELLOW_UPPER = np.array([35, 255, 255])

        # XANH
        self.GREEN_LOWER = np.array([40, 50, 50])
        self.GREEN_UPPER = np.array([90, 255, 255])

        # Ngưỡng confidence
        self.MIN_PIXELS = 50  # Số pixel tối thiểu để xác định màu

    def load_roi(self):
        """Tải ROI từ file config"""
        if os.path.exists(self.roi_config_path):
            try:
                with open(self.roi_config_path, 'r') as f:
                    data = json.load(f)
                    self.roi = data.get('roi')
                    print(f"✅ Đã tải ROI từ {self.roi_config_path}")
            except Exception as e:
                print(f"⚠️ Không thể tải ROI: {e}")
        else:
            print(f"⚠️ File ROI không tồn tại: {self.roi_config_path}")
            print("💡 Bạn sẽ cần vẽ ROI bằng cách nhấn phím 'r'")

    def save_roi(self, roi: list):
        """
        Lưu ROI vào file config

        Args:
            roi: Danh sách 4 điểm [x, y]
        """
        os.makedirs(os.path.dirname(self.roi_config_path), exist_ok=True)
        with open(self.roi_config_path, 'w') as f:
            json.dump({'roi': roi}, f, indent=2)
        print(f"✅ Đã lưu ROI vào {self.roi_config_path}")

    def detect_color(self, frame: np.ndarray) -> Tuple[str, float, np.ndarray]:
        """
        Phát hiện màu đèn tín hiệu

        Args:
            frame: Khung hình từ camera

        Returns:
            (color, confidence, debug_image)
            - color: 'RED', 'YELLOW', 'GREEN', hoặc 'UNKNOWN'
            - confidence: Độ tin cậy (0-1)
            - debug_image: Ảnh debug để hiển thị
        """
        # Nếu có ROI, crop frame
        if self.roi:
            pts = np.array(self.roi, dtype=np.int32)
            mask = np.zeros(frame.shape[:2], dtype=np.uint8)
            cv2.fillPoly(mask, [pts], 255)
            roi_frame = cv2.bitwise_and(frame, frame, mask=mask)
        else:
            roi_frame = frame.copy()

        # Chuyển sang không gian màu HSV
        hsv = cv2.cvtColor(roi_frame, cv2.COLOR_BGR2HSV)

        # Tạo mask cho từng màu
        red_mask1 = cv2.inRange(hsv, self.RED_LOWER_1, self.RED_UPPER_1)
        red_mask2 = cv2.inRange(hsv, self.RED_LOWER_2, self.RED_UPPER_2)
        red_mask = cv2.bitwise_or(red_mask1, red_mask2)

        yellow_mask = cv2.inRange(hsv, self.YELLOW_LOWER, self.YELLOW_UPPER)
        green_mask = cv2.inRange(hsv, self.GREEN_LOWER, self.GREEN_UPPER)

        # Đếm số pixel của mỗi màu
        red_pixels = cv2.countNonZero(red_mask)
        yellow_pixels = cv2.countNonZero(yellow_mask)
        green_pixels = cv2.countNonZero(green_mask)

        # Tổng số pixel trong ROI
        total_pixels = roi_frame.shape[0] * roi_frame.shape[1]

        # Tính confidence
        red_conf = red_pixels / total_pixels if total_pixels > 0 else 0
        yellow_conf = yellow_pixels / total_pixels if total_pixels > 0 else 0
        green_conf = green_pixels / total_pixels if total_pixels > 0 else 0

        # Tạo debug image
        debug_image = frame.copy()
        debug_h = 150
        debug_w = frame.shape[1]
        debug_bar = np.zeros((debug_h, debug_w, 3), dtype=np.uint8)

        # Vẽ bar chart
        cv2.rectangle(debug_bar, (10, 30), (10 + int(red_conf * 200), 60), (0, 0, 255), -1)
        cv2.rectangle(debug_bar, (10, 70), (10 + int(yellow_conf * 200), 100), (0, 255, 255), -1)
        cv2.rectangle(debug_bar, (10, 110), (10 + int(green_conf * 200), 140), (0, 255, 0), -1)

        cv2.putText(debug_bar, f"RED: {red_conf:.2%}", (220, 50),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
        cv2.putText(debug_bar, f"YELLOW: {yellow_conf:.2%}", (220, 90),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
        cv2.putText(debug_bar, f"GREEN: {green_conf:.2%}", (220, 130),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)

        # Ghép debug bar vào frame
        debug_image = np.vstack([debug_image, debug_bar])

        # Xác định màu
        max_conf = max(red_conf, yellow_conf, green_conf)

        if max_conf < self.MIN_PIXELS / total_pixels:
            return 'UNKNOWN', 0.0, debug_image

        if red_conf == max_conf and red_pixels > self.MIN_PIXELS:
            return 'RED', red_conf, debug_image
        elif yellow_conf == max_conf and yellow_pixels > self.MIN_PIXELS:
            return 'YELLOW', yellow_conf, debug_image
        elif green_conf == max_conf and green_pixels > self.MIN_PIXELS:
            return 'GREEN', green_conf, debug_image
        else:
            return 'UNKNOWN', 0.0, debug_image


class ROIDrawer:
    """Công cụ vẽ ROI"""

    def __init__(self):
        self.points = []
        self.drawing = False

    def mouse_callback(self, event, x, y, flags, param):
        """Callback cho sự kiện chuột"""
        if event == cv2.EVENT_LBUTTONDOWN:
            if len(self.points) < 4:
                self.points.append([x, y])
                print(f"✅ Đã chọn điểm {len(self.points)}: ({x}, {y})")

                if len(self.points) == 4:
                    print("✅ Đã chọn đủ 4 điểm! Nhấn 's' để lưu, 'r' để vẽ lại")

    def draw_roi(self, frame: np.ndarray, detector: TrafficLightDetector):
        """
        Vẽ ROI trên frame

        Args:
            frame: Khung hình
            detector: Detector instance
        """
        window_name = "Vẽ ROI - Chọn 4 góc của đèn tín hiệu"
        cv2.namedWindow(window_name)
        cv2.setMouseCallback(window_name, self.mouse_callback)

        print("\n" + "="*60)
        print("🎨 HƯỚNG DẪN VẼ ROI")
        print("="*60)
        print("1. Click chuột để chọn 4 góc bao quanh đèn tín hiệu")
        print("2. Thứ tự: Trên trái → Trên phải → Dưới phải → Dưới trái")
        print("3. Nhấn 's' để lưu ROI")
        print("4. Nhấn 'r' để vẽ lại")
        print("5. Nhấn 'q' để thoát")
        print("="*60 + "\n")

        cap = cv2.VideoCapture(camera_source)

        while True:
            ret, frame = cap.read()
            if not ret:
                print("❌ Không thể đọc frame từ camera")
                break

            display_frame = frame.copy()

            # Vẽ các điểm đã chọn
            for i, point in enumerate(self.points):
                cv2.circle(display_frame, tuple(point), 5, (0, 255, 0), -1)
                cv2.putText(display_frame, str(i+1),
                           (point[0]+10, point[1]+10),
                           cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

            # Vẽ đường nối
            if len(self.points) > 1:
                pts = np.array(self.points, dtype=np.int32)
                cv2.polylines(display_frame, [pts], len(self.points) == 4,
                            (0, 255, 0), 2)

            # Hiển thị hướng dẫn
            cv2.putText(display_frame, f"Diem da chon: {len(self.points)}/4",
                       (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)

            cv2.imshow(window_name, display_frame)

            key = cv2.waitKey(1) & 0xFF

            if key == ord('s') and len(self.points) == 4:
                detector.save_roi(self.points)
                detector.roi = self.points
                print("✅ Đã lưu ROI thành công!")
                break
            elif key == ord('r'):
                self.points = []
                print("🔄 Đã xóa các điểm, vẽ lại ROI")
            elif key == ord('q'):
                print("🚪 Thoát chế độ vẽ ROI")
                break

        cap.release()
        cv2.destroyAllWindows()


def main(camera_source):
    """
    Hàm chính chạy demo

    Args:
        camera_source: Nguồn camera (RTSP URL hoặc index USB)
    """
    print("\n" + "="*60)
    print("🚦 DEMO PHÁT HIỆN ĐÈN TÍN HIỆU GIAO THÔNG")
    print("="*60)
    print(f"📹 Camera: {camera_source}")
    print("="*60 + "\n")

    # Khởi tạo detector
    detector = TrafficLightDetector()

    # Kết nối camera
    cap = cv2.VideoCapture(camera_source)

    if not cap.isOpened():
        print(f"❌ Không thể kết nối đến camera: {camera_source}")
        print("💡 Hướng dẫn:")
        print("   - RTSP: rtsp://username:password@ip:port/path")
        print("   - USB: 0, 1, 2, ...")
        return

    print("✅ Đã kết nối camera thành công!")

    # Lấy thông tin camera
    fps = cap.get(cv2.CAP_PROP_FPS)
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    print(f"📊 Thông số: {width}x{height} @ {fps:.1f} FPS\n")

    print("⌨️  PHÍM TẮT:")
    print("   'r' - Vẽ lại ROI")
    print("   'q' - Thoát")
    print("   'Space' - Chụp ảnh màn hình")
    print("="*60 + "\n")

    # Nếu chưa có ROI, vẽ ROI
    if detector.roi is None:
        drawer = ROIDrawer()
        drawer.draw_roi(cap, detector)
        # Kết nối lại camera sau khi vẽ ROI
        cap = cv2.VideoCapture(camera_source)

    window_name = "Traffic Light Detection - Phát hiện đèn tín hiệu"
    cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)

    frame_count = 0

    while True:
        ret, frame = cap.read()

        if not ret:
            print("❌ Không thể đọc frame từ camera")
            break

        frame_count += 1

        # Phát hiện màu đèn
        color, confidence, debug_image = detector.detect_color(frame)

        # Vẽ ROI lên frame
        if detector.roi:
            pts = np.array(detector.roi, dtype=np.int32)
            cv2.polylines(debug_image, [pts], True, (0, 255, 0), 2)

        # Hiển thị kết quả
        color_map = {
            'RED': ((0, 0, 255), "ĐÈN ĐỎ"),
            'YELLOW': ((0, 255, 255), "ĐÈN VÀNG"),
            'GREEN': ((0, 255, 0), "ĐÈN XANH"),
            'UNKNOWN': ((128, 128, 128), "KHÔNG XÁC ĐỊNH")
        }

        color_bgr, color_text = color_map.get(color, ((128, 128, 128), "KHÔNG XÁC ĐỊNH"))

        # Vẽ kết quả lên góc trên bên trái
        result_text = f"{color_text} ({confidence:.1%})"

        # Tạo background cho text
        (text_w, text_h), _ = cv2.getTextSize(result_text, cv2.FONT_HERSHEY_SIMPLEX, 1.2, 3)
        cv2.rectangle(debug_image, (5, 5), (15 + text_w, 15 + text_h), (0, 0, 0), -1)

        cv2.putText(debug_image, result_text, (10, 40),
                   cv2.FONT_HERSHEY_SIMPLEX, 1.2, color_bgr, 3)

        # Hiển thị FPS
        cv2.putText(debug_image, f"Frame: {frame_count}", (10, height - 20),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)

        # Hiển thị thời gian
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        cv2.putText(debug_image, timestamp, (width - 250, height - 20),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)

        cv2.imshow(window_name, debug_image)

        # In log mỗi 30 frames
        if frame_count % 30 == 0:
            print(f"[{timestamp}] Phát hiện: {color_text} (Confidence: {confidence:.1%})")

        # Xử lý phím
        key = cv2.waitKey(1) & 0xFF

        if key == ord('q'):
            print("\n🚪 Dừng chương trình...")
            break
        elif key == ord('r'):
            print("\n🎨 Chuyển sang chế độ vẽ ROI...")
            cap.release()
            cv2.destroyAllWindows()
            drawer = ROIDrawer()
            drawer.draw_roi(frame, detector)
            cap = cv2.VideoCapture(camera_source)
            cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)
        elif key == ord(' '):  # Space
            screenshot_path = f"screenshot_{datetime.now().strftime('%Y%m%d_%H%M%S')}.jpg"
            cv2.imwrite(screenshot_path, debug_image)
            print(f"📸 Đã lưu ảnh: {screenshot_path}")

    cap.release()
    cv2.destroyAllWindows()

    print("\n" + "="*60)
    print("✅ DEMO KẾT THÚC")
    print("="*60)


if __name__ == "__main__":
    import sys

    # Lấy camera source từ command line hoặc dùng mặc định
    if len(sys.argv) > 1:
        camera_source = sys.argv[1]
        # Nếu là số thì convert sang int (USB camera)
        try:
            camera_source = int(camera_source)
        except ValueError:
            pass  # Giữ nguyên string (RTSP URL)
    else:
        # Mặc định: thử USB camera đầu tiên
        camera_source = 0
        print("⚠️ Không có tham số camera, sử dụng mặc định: USB camera 0")
        print("💡 Cách dùng: python demo_traffic_light_detection.py [camera_source]")
        print("   Ví dụ: python demo_traffic_light_detection.py 0")
        print("   Ví dụ: python demo_traffic_light_detection.py rtsp://admin:123@192.168.1.100:554/stream")
        print()

    main(camera_source)
