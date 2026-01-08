"""
Script vẽ ROI cho RTSP Camera
Hướng dẫn sử dụng:
1. Chạy: python select_roi_rtsp.py
2. Chế độ 1 - Vẽ Traffic Light ROI:
   - Click chuột trái vào 4 góc của đèn giao thông (theo thứ tự: trên-trái, trên-phải, dưới-phải, dưới-trái)
   - Nhấn 's' để save và chuyển sang chế độ 2
3. Chế độ 2 - Vẽ Stop Line:
   - Click chuột trái vào 2 điểm đầu-cuối của vạch dừng
   - Nhấn 's' để save
4. Nhấn 'r' để reset
5. Nhấn 'q' để thoát
"""

import cv2
import numpy as np
import sys
import os
import json
from datetime import datetime

# Add parent directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'app'))

class RTSPROISelector:
    def __init__(self, rtsp_url, camera_name="camera_live"):
        self.rtsp_url = rtsp_url
        self.camera_name = camera_name
        self.mode = 1  # 1: Traffic light ROI, 2: Stop line
        self.points = []
        self.frame = None
        self.original_frame = None

        # Kết quả
        self.traffic_light_roi = None
        self.stop_line_y = None

        print(f"\n{'='*70}")
        print(f"[*] RTSP ROI SELECTOR - {camera_name}")
        print(f"{'='*70}")
        print(f"[*] Camera URL: {rtsp_url}")
        print(f"{'='*70}\n")

    def mouse_callback(self, event, x, y, flags, param):
        """Callback function cho sự kiện chuột"""
        if event == cv2.EVENT_LBUTTONDOWN:
            if self.mode == 1:  # Traffic Light ROI
                if len(self.points) < 4:
                    self.points.append([x, y])
                    print(f"[OK] Diem {len(self.points)}/4: ({x}, {y})")
                    if len(self.points) == 4:
                        print("\n[OK] Da chon du 4 diem! Nhan 's' de save hoac 'r' de reset")
                else:
                    print("[!] Da chon du 4 diem! Nhan 's' de save hoac 'r' de reset")

            elif self.mode == 2:  # Stop Line
                if len(self.points) < 2:
                    self.points.append([x, y])
                    print(f"[OK] Diem {len(self.points)}/2: ({x}, {y})")
                    if len(self.points) == 2:
                        print("\n[OK] Da chon du 2 diem! Nhan 's' de save hoac 'r' de reset")
                else:
                    print("[!] Da chon du 2 diem! Nhan 's' de save hoac 'r' de reset")

            self.draw_roi()

    def draw_roi(self):
        """Vẽ ROI lên frame"""
        if self.original_frame is None:
            return

        self.frame = self.original_frame.copy()

        # Vẽ chế độ hiện tại
        if self.mode == 1:
            mode_text = "CHE DO 1: VE TRAFFIC LIGHT ROI (4 diem)"
            color = (0, 255, 255)  # Yellow
            required_points = 4
        else:
            mode_text = "CHE DO 2: VE STOP LINE (2 diem)"
            color = (0, 0, 255)  # Red
            required_points = 2

        cv2.putText(self.frame, mode_text, (10, 30),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, color, 2)

        # Vẽ các điểm đã chọn
        for i, point in enumerate(self.points):
            cv2.circle(self.frame, tuple(point), 8, (0, 255, 0), -1)
            cv2.putText(self.frame, str(i+1), (point[0]+15, point[1]),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

        # Vẽ hình dạng tùy theo chế độ
        if self.mode == 1 and len(self.points) > 0:
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
            if len(self.points) == 4:
                pts = np.array(self.points, dtype=np.int32)
                overlay = self.original_frame.copy()
                cv2.fillPoly(overlay, [pts], (0, 255, 255))
                self.frame = cv2.addWeighted(self.original_frame, 0.6, overlay, 0.4, 0)

                # Vẽ lại các điểm lên trên
                for i, point in enumerate(self.points):
                    cv2.circle(self.frame, tuple(point), 8, (0, 255, 0), -1)
                    cv2.putText(self.frame, str(i+1), (point[0]+15, point[1]),
                               cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

        elif self.mode == 2 and len(self.points) > 0:
            # Vẽ đường stop line
            if len(self.points) == 2:
                pt1 = tuple(self.points[0])
                pt2 = tuple(self.points[1])
                cv2.line(self.frame, pt1, pt2, (0, 0, 255), 3)

                # Tính Y trung bình
                avg_y = (self.points[0][1] + self.points[1][1]) // 2
                cv2.putText(self.frame, f"Stop Line Y={avg_y}",
                           (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)

        # Hiển thị hướng dẫn
        instructions = [
            "Click chuot trai: Chon diem",
            "'s': Save va tiep tuc",
            "'r': Reset lai cac diem",
            "'q': Thoat"
        ]
        y_offset = 100
        for instruction in instructions:
            cv2.putText(self.frame, instruction, (10, y_offset),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
            y_offset += 25

        cv2.imshow('RTSP ROI Selector', self.frame)

    def save_config(self):
        """Lưu cấu hình ROI theo format của API"""
        if self.traffic_light_roi is None or self.stop_line_y is None:
            print("[ERROR] Chua co du thong tin de luu (can ca ROI va Stop Line)")
            return None

        # Tính x, y, w, h từ 4 điểm
        roi_points = np.array(self.traffic_light_roi)
        x = int(roi_points[:, 0].min())
        y = int(roi_points[:, 1].min())
        w = int(roi_points[:, 0].max() - x)
        h = int(roi_points[:, 1].max() - y)

        # Format giống API endpoint (app/api/v1/api_red_light_config.py)
        config = {
            "camera_name": self.camera_name,
            "traffic_light_roi": {
                "x": x,
                "y": y,
                "w": w,
                "h": h
            },
            "stop_line_y": self.stop_line_y,
            "created_at": datetime.now().isoformat(),
            "camera_source": self.rtsp_url
        }

        # Lưu vào thư mục config (giống API)
        config_dir = os.path.join(os.path.dirname(__file__), "app/config")
        os.makedirs(config_dir, exist_ok=True)

        config_file = os.path.join(config_dir, f"red_light_config_{self.camera_name}.json")

        with open(config_file, 'w', encoding='utf-8') as f:
            json.dump(config, indent=2, fp=f)

        print(f"\n[OK] Da luu cau hinh vao: {config_file}")
        print("\n[*] Cau hinh:")
        print(json.dumps(config, indent=2, ensure_ascii=False))

        return config

    def run(self):
        """Chạy script chọn ROI"""
        # Kết nối RTSP stream với chất lượng tốt hơn
        print("[*] Dang ket noi voi RTSP camera...")
        cap = cv2.VideoCapture(self.rtsp_url, cv2.CAP_FFMPEG)

        # Set buffer và chất lượng
        cap.set(cv2.CAP_PROP_BUFFERSIZE, 3)
        cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*'H264'))

        if not cap.isOpened():
            print(f"[ERROR] Khong the ket noi RTSP: {self.rtsp_url}")
            return False

        print("[OK] Ket noi thanh cong!")

        # Đọc và bỏ qua 5 frame đầu (thường bị mờ)
        print("[*] Dang lay frame chat luong cao...")
        for i in range(5):
            ret, _ = cap.read()

        # Đọc frame chính
        ret, frame = cap.read()

        if not ret:
            print("[ERROR] Khong the doc frame tu RTSP stream")
            cap.release()
            return False

        print(f"[OK] Da lay frame: {frame.shape}")

        self.original_frame = frame.copy()
        self.frame = frame.copy()

        # Tạo window full screen và set mouse callback
        window_name = 'RTSP ROI Selector'
        cv2.namedWindow(window_name, cv2.WINDOW_KEEPRATIO)
        cv2.resizeWindow(window_name, frame.shape[1], frame.shape[0])
        cv2.setMouseCallback(window_name, self.mouse_callback)

        print("\n" + "="*70)
        print("CHE DO 1: VE TRAFFIC LIGHT ROI")
        print("="*70)
        print("[*] Click chuot vao 4 goc cua den giao thong theo thu tu:")
        print("   1. Goc tren-trai")
        print("   2. Goc tren-phai")
        print("   3. Goc duoi-phai")
        print("   4. Goc duoi-trai")
        print("[*] Nhan 's' de save va chuyen sang che do 2")
        print("[*] Nhan 'r' de reset")
        print("[*] Nhan 'q' de thoat")
        print("="*70 + "\n")

        self.draw_roi()

        while True:
            key = cv2.waitKey(1) & 0xFF

            if key == ord('q'):
                print("\n[*] Da thoat!")
                break

            elif key == ord('r'):
                self.points = []
                print(f"\n[*] Da reset che do {self.mode}!")
                self.draw_roi()

            elif key == ord('s'):
                if self.mode == 1:
                    # Save Traffic Light ROI
                    if len(self.points) != 4:
                        print(f"\n[!] Can chon dung 4 diem! (Hien tai: {len(self.points)})")
                        continue

                    self.traffic_light_roi = [pt[:] for pt in self.points]
                    print("\n[OK] Da luu Traffic Light ROI!")

                    # Chuyển sang chế độ 2
                    self.mode = 2
                    self.points = []

                    print("\n" + "="*70)
                    print("CHE DO 2: VE STOP LINE")
                    print("="*70)
                    print("[*] Click chuot vao 2 diem dau-cuoi cua vach dung")
                    print("[*] Nhan 's' de save va hoan thanh")
                    print("[*] Nhan 'r' de reset")
                    print("[*] Nhan 'q' de thoat")
                    print("="*70 + "\n")

                    self.draw_roi()

                elif self.mode == 2:
                    # Save Stop Line
                    if len(self.points) != 2:
                        print(f"\n[!] Can chon dung 2 diem! (Hien tai: {len(self.points)})")
                        continue

                    # Tính Y trung bình
                    self.stop_line_y = (self.points[0][1] + self.points[1][1]) // 2
                    print(f"\n[OK] Da luu Stop Line! Y = {self.stop_line_y}")

                    # Lưu cấu hình
                    config = self.save_config()

                    print("\n" + "="*70)
                    print("HOAN THANH!")
                    print("="*70)
                    print(f"[*] Traffic Light ROI: {self.traffic_light_roi}")
                    print(f"[*] Stop Line Y: {self.stop_line_y}")
                    print("\n[*] Ban co the su dung cau hinh nay trong API hoac database")
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
        sys.exit(1)

    print(f"[*] RTSP URL: {rtsp_url}")

    selector = RTSPROISelector(rtsp_url, camera_name="camera_live")
    selector.run()
