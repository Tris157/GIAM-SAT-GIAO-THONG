"""
Script vẽ ROI cho Vehicle Tracking trên RTSP Camera
Hướng dẫn sử dụng:
1. Chạy: python select_vehicle_roi_rtsp.py
2. Click chuột trái vào các điểm để tạo vùng ROI (polygon, tối thiểu 4 điểm)
3. Nhấn 's' để save
4. Nhấn 'r' để reset
5. Nhấn 'q' để thoát

Kết quả sẽ được lưu vào app/config/vehicle_roi_camera_live.json
"""

import cv2
import numpy as np
import sys
import os
import json
from datetime import datetime

# Add parent directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'app'))

class VehicleROISelector:
    def __init__(self, rtsp_url, camera_name="camera_live"):
        self.rtsp_url = rtsp_url
        self.camera_name = camera_name
        self.points = []
        self.frame = None
        self.original_frame = None

        print(f"\n{'='*70}")
        print(f"[*] VEHICLE ROI SELECTOR - {camera_name}")
        print(f"{'='*70}")
        print(f"[*] Camera URL: {rtsp_url}")
        print(f"{'='*70}\n")

    def mouse_callback(self, event, x, y, flags, param):
        """Callback function cho sự kiện chuột"""
        if event == cv2.EVENT_LBUTTONDOWN:
            self.points.append([x, y])
            print(f"[OK] Điểm {len(self.points)}: ({x}, {y})")
            self.draw_roi()

    def draw_roi(self):
        """Vẽ ROI lên frame"""
        if self.original_frame is None:
            return

        self.frame = self.original_frame.copy()

        # Vẽ title
        cv2.putText(self.frame, "VE ROI CHO VEHICLE TRACKING", (10, 30),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)

        # Vẽ các điểm đã chọn
        for i, point in enumerate(self.points):
            cv2.circle(self.frame, tuple(point), 8, (0, 255, 0), -1)
            cv2.putText(self.frame, str(i+1), (point[0]+15, point[1]),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

        # Vẽ đường nối giữa các điểm
        if len(self.points) > 1:
            for i in range(len(self.points)):
                pt1 = tuple(self.points[i])
                if i < len(self.points) - 1:
                    pt2 = tuple(self.points[i+1])
                else:
                    pt2 = tuple(self.points[0])  # Nối điểm cuối với điểm đầu
                cv2.line(self.frame, pt1, pt2, (255, 0, 0), 2)

        # Nếu có đủ 4 điểm, tô vùng ROI
        if len(self.points) >= 4:
            pts = np.array(self.points, dtype=np.int32)
            overlay = self.original_frame.copy()
            cv2.fillPoly(overlay, [pts], (0, 255, 255))
            self.frame = cv2.addWeighted(self.original_frame, 0.6, overlay, 0.4, 0)

            # Vẽ lại các điểm lên trên
            for i, point in enumerate(self.points):
                cv2.circle(self.frame, tuple(point), 8, (0, 255, 0), -1)
                cv2.putText(self.frame, str(i+1), (point[0]+15, point[1]),
                           cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

            # Hiển thị số điểm
            cv2.putText(self.frame, f"So diem: {len(self.points)}", (10, 70),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

        # Hiển thị hướng dẫn
        instructions = [
            "Click chuot trai: Chon diem (toi thieu 4 diem)",
            "'s': Save va thoat",
            "'r': Reset lai cac diem",
            "'q': Thoat khong save"
        ]
        y_offset = 100
        for instruction in instructions:
            cv2.putText(self.frame, instruction, (10, y_offset),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
            y_offset += 25

        cv2.imshow('Vehicle ROI Selector', self.frame)

    def save_config(self):
        """Lưu cấu hình ROI"""
        if len(self.points) < 4:
            print(f"[ERROR] Can chon it nhat 4 diem! (Hien tai: {len(self.points)})")
            return None

        # Format: numpy array để dùng trong code
        config = {
            "camera_name": self.camera_name,
            "region": self.points,  # List of [x, y] points
            "created_at": datetime.now().isoformat(),
            "camera_source": self.rtsp_url,
            "note": "ROI for vehicle tracking and speed detection"
        }

        # Lưu vào thư mục config
        config_dir = os.path.join(os.path.dirname(__file__), "app/config")
        os.makedirs(config_dir, exist_ok=True)

        config_file = os.path.join(config_dir, f"vehicle_roi_{self.camera_name}.json")

        with open(config_file, 'w', encoding='utf-8') as f:
            json.dump(config, indent=2, fp=f)

        print(f"\n[OK] Da luu cau hinh vao: {config_file}")
        print("\n[*] Cau hinh:")
        print(json.dumps(config, indent=2, ensure_ascii=False))

        # In ra numpy array để copy vào code
        print("\n[*] Copy vao code (app/core/config.py):")
        print(f"RTSP_REGION = np.array({self.points})")

        return config

    def run(self):
        """Chạy script chọn ROI"""
        # Kết nối RTSP stream
        print("[*] Dang ket noi voi RTSP camera...")
        cap = cv2.VideoCapture(self.rtsp_url)
        cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)

        if not cap.isOpened():
            print(f"[ERROR] Khong the ket noi RTSP: {self.rtsp_url}")
            return False

        print("[OK] Ket noi thanh cong!")

        # Đọc frame
        print("[*] Dang lay frame...")
        ret, frame = cap.read()

        if not ret:
            print("[ERROR] Khong the doc frame tu RTSP stream")
            cap.release()
            return False

        print(f"[OK] Da lay frame: {frame.shape}")

        self.original_frame = frame.copy()
        self.frame = frame.copy()

        # Tạo window và set mouse callback
        window_name = 'Vehicle ROI Selector'
        cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)
        cv2.setMouseCallback(window_name, self.mouse_callback)

        print("\n" + "="*70)
        print("VE ROI CHO VEHICLE TRACKING")
        print("="*70)
        print("[*] Click chuot vao cac diem de tao vung ROI (toi thieu 4 diem)")
        print("[*] Nen ve theo thu tu: trai-duoi -> trai-tren -> phai-tren -> phai-duoi")
        print("[*] Nhan 's' de save")
        print("[*] Nhan 'r' de reset")
        print("[*] Nhan 'q' de thoat")
        print("="*70 + "\n")

        self.draw_roi()

        while True:
            key = cv2.waitKey(1) & 0xFF

            if key == ord('q'):
                print("\n[*] Da thoat khong save!")
                break

            elif key == ord('r'):
                self.points = []
                print("\n[*] Da reset!")
                self.draw_roi()

            elif key == ord('s'):
                # Save ROI
                if len(self.points) < 4:
                    print(f"\n[!] Can chon it nhat 4 diem! (Hien tai: {len(self.points)})")
                    continue

                config = self.save_config()

                if config:
                    print("\n" + "="*70)
                    print("HOAN THANH!")
                    print("="*70)
                    print(f"[*] ROI Points: {self.points}")
                    print("\n[*] Ban co the:")
                    print("   1. Su dung config file da luu")
                    print("   2. Copy numpy array vao app/core/config.py")
                    print("   3. Restart server de ap dung ROI moi")
                    print("="*70 + "\n")

                break

        cap.release()
        cv2.destroyAllWindows()
        return True

if __name__ == "__main__":
    # Đọc RTSP URL từ .env
    from dotenv import load_dotenv
    load_dotenv()

    rtsp_url = os.getenv("RTSP_URL")

    if not rtsp_url:
        print("[ERROR] Khong tim thay RTSP_URL trong file .env")
        print("[*] Vui long them RTSP_URL vao file Backend/.env")
        print("[*] Vi du: RTSP_URL=rtsp://admin:password@192.168.1.100:554/stream")
        sys.exit(1)

    print(f"[*] RTSP URL: {rtsp_url}")

    selector = VehicleROISelector(rtsp_url, camera_name="camera_live")
    selector.run()
