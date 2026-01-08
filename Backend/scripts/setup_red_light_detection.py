"""
============================================================================
SETUP TOOL - PHÁT HIỆN VƯỢT ĐÈN ĐỎ
============================================================================
Tool tương tác để thiết lập:
1. ROI (Region of Interest) cho đèn tín hiệu giao thông
2. Stop Line (Vạch dừng) - đường Y mà xe không được vượt qua khi đèn đỏ

CÁCH SỬ DỤNG:
-----------
1. Chạy script:
   python setup_red_light_detection.py

2. Hoặc chỉ định camera source:
   python setup_red_light_detection.py 0                    # USB camera
   python setup_red_light_detection.py rtsp://...           # RTSP camera
   python setup_red_light_detection.py path/to/video.mp4    # Video file

3. Làm theo hướng dẫn trên màn hình:
   - BƯỚC 1: Vẽ ROI cho đèn tín hiệu (click 4 góc)
   - BƯỚC 2: Vẽ Stop Line (click 2 điểm tạo đường ngang)

4. Config sẽ được lưu vào:
   app/config/red_light_config.json

PHÍM TẮT:
---------
- Click chuột trái: Chọn điểm
- 's': Save và tiếp tục
- 'r': Reset lại (vẽ lại từ đầu)
- 'q': Thoát

Tác giả: Smart Traffic Monitoring Team
Version: 2.0
Date: 2025-12-24
============================================================================
"""

import cv2
import numpy as np
import json
import os
import sys
import io
from datetime import datetime
from typing import Optional, Tuple, List

# Fix encoding for Windows console
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')


class RedLightSetupTool:
    """Tool thiết lập ROI và Stop Line cho Red Light Detector"""

    def __init__(self, camera_source, camera_name: str = "camera_live"):
        """
        Khởi tạo setup tool

        Args:
            camera_source: Nguồn camera (int, RTSP URL, hoặc video path)
            camera_name: Tên camera (dùng để lưu config)
        """
        self.camera_source = camera_source
        self.camera_name = camera_name
        self.config_dir = "app/config"
        self.config_file = f"{self.config_dir}/red_light_config_{camera_name}.json"

        # State
        self.current_step = 1  # 1=ROI, 2=Stop Line
        self.roi_points = []  # 4 điểm cho ROI
        self.stop_line_points = []  # 2 điểm cho stop line

        # Frame
        self.frame = None
        self.original_frame = None

        # Results
        self.roi = None  # (x, y, w, h)
        self.stop_line_y = None  # int

    def mouse_callback(self, event, x, y, flags, param):
        """Callback xử lý sự kiện chuột"""
        if event == cv2.EVENT_LBUTTONDOWN:
            if self.current_step == 1:
                # BƯỚC 1: Vẽ ROI (4 điểm)
                if len(self.roi_points) < 4:
                    self.roi_points.append([x, y])
                    print(f"[OK] ROI diem {len(self.roi_points)}: ({x}, {y})")

                    if len(self.roi_points) == 4:
                        print("\n" + "="*60)
                        print("[OK] DA CHON DU 4 DIEM ROI!")
                        print("Nhan 's' de luu va chuyen sang buoc 2 (ve Stop Line)")
                        print("Nhan 'r' de ve lai ROI")
                        print("="*60)

            elif self.current_step == 2:
                # BƯỚC 2: Vẽ Stop Line (2 điểm tạo đường ngang)
                if len(self.stop_line_points) < 2:
                    self.stop_line_points.append([x, y])
                    print(f"[OK] Stop Line diem {len(self.stop_line_points)}: ({x}, {y})")

                    if len(self.stop_line_points) == 2:
                        # Tính Y trung bình từ 2 điểm
                        avg_y = int((self.stop_line_points[0][1] + self.stop_line_points[1][1]) / 2)
                        self.stop_line_y = avg_y
                        print("\n" + "="*60)
                        print(f"[OK] DA VE STOP LINE TAI Y = {avg_y}")
                        print("Nhan 's' de luu config")
                        print("Nhan 'r' de ve lai Stop Line")
                        print("="*60)

            self.draw_overlay()

    def draw_overlay(self):
        """Vẽ overlay lên frame"""
        self.frame = self.original_frame.copy()

        # === VẼ ROI ===
        if len(self.roi_points) > 0:
            # Vẽ các điểm ROI
            for i, point in enumerate(self.roi_points):
                cv2.circle(self.frame, tuple(point), 6, (0, 255, 0), -1)
                cv2.putText(self.frame, str(i+1),
                           (point[0]+10, point[1]+10),
                           cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

            # Vẽ đường nối
            if len(self.roi_points) > 1:
                pts = np.array(self.roi_points, dtype=np.int32)
                cv2.polylines(self.frame, [pts], len(self.roi_points) == 4,
                             (0, 255, 0), 2)

            # Nếu đủ 4 điểm, tô màu vùng ROI
            if len(self.roi_points) == 4:
                pts = np.array(self.roi_points, dtype=np.int32)
                overlay = self.frame.copy()
                cv2.fillPoly(overlay, [pts], (0, 255, 0))
                self.frame = cv2.addWeighted(self.frame, 0.7, overlay, 0.3, 0)

                # Vẽ lại các điểm lên trên overlay
                for i, point in enumerate(self.roi_points):
                    cv2.circle(self.frame, tuple(point), 6, (0, 255, 0), -1)
                    cv2.putText(self.frame, str(i+1),
                               (point[0]+10, point[1]+10),
                               cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

        # === VẼ STOP LINE ===
        if len(self.stop_line_points) > 0:
            # Vẽ các điểm stop line
            for i, point in enumerate(self.stop_line_points):
                cv2.circle(self.frame, tuple(point), 8, (0, 0, 255), -1)

            # Nếu đủ 2 điểm, vẽ đường ngang
            if len(self.stop_line_points) == 2:
                avg_y = int((self.stop_line_points[0][1] + self.stop_line_points[1][1]) / 2)

                # Vẽ stop line ở giữa khung hình (nửa chiều rộng)
                frame_width = self.frame.shape[1]
                start_x = frame_width // 4
                end_x = 3 * frame_width // 4

                cv2.line(self.frame,
                        (start_x, avg_y),
                        (end_x, avg_y),
                        (0, 0, 255), 3)

                cv2.putText(self.frame, f"STOP LINE (Y={avg_y})",
                           (start_x + 10, avg_y - 10),
                           cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)

        # === VẼ INSTRUCTIONS ===
        instructions = []
        if self.current_step == 1:
            instructions = [
                f"BUOC 1: VE ROI DEN TIN HIEU ({len(self.roi_points)}/4 diem)",
                "Click 4 goc bao quanh den tin hieu",
                "Thu tu: Tren trai → Tren phai → Duoi phai → Duoi trai",
                "",
                "Phim 's': Luu va chuyen sang buoc 2",
                "Phim 'r': Ve lai ROI",
                "Phim 'q': Thoat"
            ]
        elif self.current_step == 2:
            instructions = [
                f"BUOC 2: VE STOP LINE ({len(self.stop_line_points)}/2 diem)",
                "Click 2 diem bat ky tao duong ngang",
                "(Duong se tu dong ve o giua khung hinh)",
                "",
                "Phim 's': Luu config",
                "Phim 'r': Ve lai Stop Line",
                "Phim 'q': Thoat"
            ]

        y_offset = 30
        for instruction in instructions:
            # Background cho text
            if instruction:  # Skip empty lines
                (text_w, text_h), _ = cv2.getTextSize(instruction,
                                                      cv2.FONT_HERSHEY_SIMPLEX,
                                                      0.6, 2)
                cv2.rectangle(self.frame, (5, y_offset - 20),
                             (15 + text_w, y_offset + 5),
                             (0, 0, 0), -1)

            cv2.putText(self.frame, instruction, (10, y_offset),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
            y_offset += 30

        cv2.imshow("Red Light Detection Setup", self.frame)

    def calculate_roi_bbox(self) -> Tuple[int, int, int, int]:
        """
        Tính bounding box (x, y, w, h) từ 4 điểm ROI

        Returns:
            (x, y, w, h): Tọa độ góc trên trái và kích thước
        """
        if len(self.roi_points) != 4:
            return None

        pts = np.array(self.roi_points)
        x = int(pts[:, 0].min())
        y = int(pts[:, 1].min())
        w = int(pts[:, 0].max() - x)
        h = int(pts[:, 1].max() - y)
        return (x, y, w, h)

    def save_config(self):
        """Lưu config vào file JSON"""
        if self.roi is None or self.stop_line_y is None:
            print("[ERROR] Chua du thong tin de luu config!")
            return False

        # Tạo thư mục nếu chưa tồn tại
        os.makedirs(self.config_dir, exist_ok=True)

        config = {
            "camera_name": self.camera_name,
            "traffic_light_roi": {
                "x": self.roi[0],
                "y": self.roi[1],
                "w": self.roi[2],
                "h": self.roi[3]
            },
            "stop_line_y": self.stop_line_y,
            "created_at": datetime.now().isoformat(),
            "camera_source": str(self.camera_source)
        }

        with open(self.config_file, 'w', encoding='utf-8') as f:
            json.dump(config, f, indent=2, ensure_ascii=False)

        print("\n" + "="*60)
        print("[OK] DA LUU CONFIG THANH CONG!")
        print("="*60)
        print(f"[FILE] {self.config_file}")
        print(f"\n[INFO] Thong tin da luu:")
        print(f"  - ROI den tin hieu: x={self.roi[0]}, y={self.roi[1]}, "
              f"w={self.roi[2]}, h={self.roi[3]}")
        print(f"  - Stop Line Y: {self.stop_line_y}")
        print("\n[TIP] De su dung config nay trong code:")
        print(f"""
import json

# Load config
with open('{self.config_file}', 'r') as f:
    config = json.load(f)

# Setup detector
detector = RedLightDetector('{self.camera_name}')
detector.set_traffic_light_roi(
    config['traffic_light_roi']['x'],
    config['traffic_light_roi']['y'],
    config['traffic_light_roi']['w'],
    config['traffic_light_roi']['h']
)
detector.set_stop_line(config['stop_line_y'])
""")
        print("="*60)
        return True

    def run(self):
        """Chạy tool setup"""
        print("\n" + "="*60)
        print("RED LIGHT DETECTION SETUP TOOL")
        print("="*60)
        print(f"Camera: {self.camera_source}")
        print(f"Camera Name: {self.camera_name}")
        print("="*60 + "\n")

        # Kết nối camera
        cap = cv2.VideoCapture(self.camera_source)

        if not cap.isOpened():
            print(f"[ERROR] Khong the ket noi den camera: {self.camera_source}")
            print("\n[TIP] Huong dan:")
            print("   - USB camera: python setup_red_light_detection.py 0")
            print("   - RTSP: python setup_red_light_detection.py rtsp://user:pass@ip:port/path")
            print("   - Video: python setup_red_light_detection.py path/to/video.mp4")
            return

        print("[OK] Da ket noi camera thanh cong!")

        # Lấy thông tin camera
        fps = cap.get(cv2.CAP_PROP_FPS)
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        print(f"[INFO] Thong so: {width}x{height} @ {fps:.1f} FPS\n")

        # Đọc frame đầu tiên
        ret, frame = cap.read()
        if not ret:
            print("[ERROR] Khong the doc frame tu camera")
            cap.release()
            return

        self.original_frame = frame.copy()
        self.frame = frame.copy()

        # Tạo window
        window_name = "Red Light Detection Setup"
        cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)
        cv2.setMouseCallback(window_name, self.mouse_callback)

        print("BAT DAU THIET LAP!")
        print("="*60)
        print("BUOC 1: VE ROI CHO DEN TIN HIEU")
        print("  -> Click 4 goc bao quanh den tin hieu")
        print("="*60 + "\n")

        self.draw_overlay()

        # Main loop
        while True:
            # Cập nhật frame mới (nếu là video/camera live)
            if not isinstance(self.camera_source, str) or \
               self.camera_source.startswith('rtsp://'):
                ret, new_frame = cap.read()
                if ret:
                    self.original_frame = new_frame.copy()
                    self.draw_overlay()

            key = cv2.waitKey(1) & 0xFF

            if key == ord('q'):
                print("\n[EXIT] Thoat chuong trinh...")
                break

            elif key == ord('r'):
                # Reset
                if self.current_step == 1:
                    self.roi_points = []
                    print("\n[RESET] Da xoa ROI, ve lai!")
                elif self.current_step == 2:
                    self.stop_line_points = []
                    self.stop_line_y = None
                    print("\n[RESET] Da xoa Stop Line, ve lai!")
                self.draw_overlay()

            elif key == ord('s'):
                # Save và chuyển bước
                if self.current_step == 1:
                    # Hoàn thành bước 1
                    if len(self.roi_points) == 4:
                        self.roi = self.calculate_roi_bbox()
                        print(f"\n[OK] Da luu ROI: {self.roi}")
                        print("\n" + "="*60)
                        print("BUOC 2: VE STOP LINE")
                        print("  -> Click 2 diem bat ky de tao duong ngang")
                        print("  -> Duong se tu dong ve o giua khung hinh")
                        print("="*60 + "\n")
                        self.current_step = 2
                        self.draw_overlay()
                    else:
                        print(f"\n[WARNING] Can chon du 4 diem! (Hien tai: {len(self.roi_points)})")

                elif self.current_step == 2:
                    # Hoàn thành bước 2
                    if len(self.stop_line_points) == 2:
                        # Lưu config
                        if self.save_config():
                            print("\n[OK] HOAN THANH! Nhan 'q' de thoat.")
                    else:
                        print(f"\n[WARNING] Can chon 2 diem! (Hien tai: {len(self.stop_line_points)})")

        cap.release()
        cv2.destroyAllWindows()

        print("\n" + "="*60)
        print("[OK] SETUP HOAN TAT!")
        print("="*60)


def main():
    """Hàm main"""
    # Parse arguments
    if len(sys.argv) > 1:
        camera_source = sys.argv[1]
        # Convert to int nếu là số (USB camera)
        try:
            camera_source = int(camera_source)
        except ValueError:
            pass  # Giữ nguyên string (RTSP hoặc file path)
    else:
        # Mặc định: USB camera 0
        camera_source = 0
        print("[WARNING] Khong co tham so, su dung mac dinh: USB camera 0")
        print("[TIP] Cach dung: python setup_red_light_detection.py [camera_source]")
        print()

    # Camera name (có thể custom)
    camera_name = "camera_live"
    if len(sys.argv) > 2:
        camera_name = sys.argv[2]

    # Run tool
    tool = RedLightSetupTool(camera_source, camera_name)
    tool.run()


if __name__ == "__main__":
    main()
