"""
Script de chon ROI (Region of Interest) cho video
Cach su dung:
1. Chay script: python select_roi.py
2. Click chuot trai de chon cac diem ROI (toi thieu 4 diem)
3. Nhan 's' de save ROI hien tai va chuyen sang video tiep theo
4. Nhan 'r' de reset lai cac diem da chon
5. Nhan 'q' de thoat
"""

import cv2
import numpy as np
import sys
import io

# Fix encoding for Windows
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

from core.config import SettingMetricTransport

class ROISelector:
    def __init__(self, video_paths):
        self.video_paths = video_paths
        self.current_video_idx = 0
        self.points = []
        self.all_regions = []
        self.frame = None
        self.original_frame = None

    def mouse_callback(self, event, x, y, flags, param):
        """Callback function cho sự kiện chuột"""
        if event == cv2.EVENT_LBUTTONDOWN:
            # Thêm điểm mới
            self.points.append([x, y])
            print(f"Diem {len(self.points)}: ({x}, {y})")

            # Vẽ lại frame
            self.draw_roi()

    def draw_roi(self):
        """Vẽ ROI lên frame"""
        self.frame = self.original_frame.copy()

        # Vẽ các điểm
        for i, point in enumerate(self.points):
            cv2.circle(self.frame, tuple(point), 5, (0, 255, 0), -1)
            cv2.putText(self.frame, str(i+1), (point[0]+10, point[1]),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

        # Vẽ đường nối giữa các điểm
        if len(self.points) > 1:
            for i in range(len(self.points)):
                pt1 = tuple(self.points[i])
                pt2 = tuple(self.points[(i+1) % len(self.points)])
                cv2.line(self.frame, pt1, pt2, (255, 0, 0), 2)

        # Nếu có đủ điểm, vẽ vùng ROI
        if len(self.points) >= 3:
            pts = np.array(self.points, dtype=np.int32)
            cv2.fillPoly(self.frame, [pts], (0, 255, 255), cv2.LINE_AA)
            # Blend với frame gốc để thấy vùng ROI trong suốt
            self.frame = cv2.addWeighted(self.original_frame, 0.7, self.frame, 0.3, 0)

            # Vẽ lại các điểm và số thứ tự lên trên
            for i, point in enumerate(self.points):
                cv2.circle(self.frame, tuple(point), 5, (0, 255, 0), -1)
                cv2.putText(self.frame, str(i+1), (point[0]+10, point[1]),
                           cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

        # Hiển thị hướng dẫn
        instructions = [
            "Click chuot trai: Chon diem ROI",
            "Phim 's': Save va chuyen video tiep",
            "Phim 'r': Reset lai cac diem",
            "Phim 'q': Thoat"
        ]
        y_offset = 30
        for instruction in instructions:
            cv2.putText(self.frame, instruction, (10, y_offset),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
            y_offset += 30

        cv2.imshow('Select ROI', self.frame)

    def process_video(self, video_path):
        """Xử lý một video để chọn ROI"""
        # Convert relative path to absolute path
        import os
        if not os.path.isabs(video_path):
            video_path = os.path.abspath(video_path)

        print(f"Trying to open: {video_path}")
        cap = cv2.VideoCapture(video_path)

        if not cap.isOpened():
            print(f"Khong the mo video: {video_path}")
            return False

        # Đọc frame đầu tiên
        ret, frame = cap.read()
        if not ret:
            print(f"Không thể đọc frame từ video: {video_path}")
            cap.release()
            return False

        # RESIZE FRAME VỀ (600, 400) - GIỐNG VỚI ANALYZER
        frame = cv2.resize(frame, (600, 400))

        self.original_frame = frame.copy()
        self.frame = frame.copy()
        self.points = []

        # Tạo window và set mouse callback
        window_name = 'Select ROI'
        cv2.namedWindow(window_name)
        cv2.setMouseCallback(window_name, self.mouse_callback)

        print(f"\n{'='*60}")
        print(f"Video {self.current_video_idx + 1}/{len(self.video_paths)}: {video_path}")
        print(f"{'='*60}")
        print("Click chuot trai de chon cac diem ROI (toi thieu 4 diem)")
        print("Nhan 's' de save va chuyen video tiep theo")
        print("Nhan 'r' de reset lai cac diem")
        print("Nhan 'q' de thoat")

        self.draw_roi()

        while True:
            key = cv2.waitKey(1) & 0xFF

            if key == ord('q'):
                # Thoát
                cap.release()
                cv2.destroyAllWindows()
                return False

            elif key == ord('r'):
                # Reset lai cac diem
                self.points = []
                print("\nDa reset lai cac diem!")
                self.draw_roi()

            elif key == ord('s'):
                # Save ROI
                if len(self.points) < 4:
                    print(f"\nCan chon it nhat 4 diem! (Hien tai: {len(self.points)} diem)")
                    continue

                region = np.array(self.points)
                self.all_regions.append(region)
                print(f"\nDa save ROI cho video {self.current_video_idx + 1}:")
                print(f"np.array({self.points})")

                cap.release()
                return True

        cap.release()
        return False

    def run(self):
        """Chạy script chọn ROI cho tất cả video"""
        print("\n" + "="*60)
        print("SCRIPT CHỌN ROI CHO VIDEO")
        print("="*60)

        for idx, video_path in enumerate(self.video_paths):
            self.current_video_idx = idx

            if not self.process_video(video_path):
                break

        cv2.destroyAllWindows()

        # In ket qua cuoi cung
        if len(self.all_regions) > 0:
            print("\n" + "="*60)
            print("KET QUA - COPY VAO config.py:")
            print("="*60)
            print("REGIONS = [")
            for i, region in enumerate(self.all_regions):
                points_str = str(region.tolist())
                print(f"    np.array({points_str}),")
            print("]")
            print("="*60)
        else:
            print("\nKhong co ROI nao duoc chon!")

if __name__ == "__main__":
    # Lấy danh sách video từ config
    video_paths = SettingMetricTransport.PATH_VIDEOS

    print(f"\nSe chon ROI cho {len(video_paths)} video:")
    for i, path in enumerate(video_paths):
        print(f"  {i+1}. {path}")

    selector = ROISelector(video_paths)
    selector.run()
