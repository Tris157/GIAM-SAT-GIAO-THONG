from abc import abstractmethod
import cvzone
import cv2
import os
import numpy as np
from datetime import datetime
from ultralytics import solutions
from app.utils.transport_utils import *
from app.core.config import SettingMetricTransport
conf = SettingMetricTransport()

# Thêm cái này để tránh xung đột
os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"

from app.services.speed_violation_detector import SpeedViolationDetector

class AnalyzeOnRoadBase:
    """Class gói gọn script xử lý tuần tự nhưng đảm bảo tính đóng gói OOP
        Attributes:
            count_car_display (int): số lượng xe oto trung bình
            speed_car_display (int): trung bình tốc độ tức thời của oto
            count_moto_display (int): số lượng xe xe máy trung bình
            speed_moto_display (int): trung bình tốc độ tức thời của xe máy
            speed_tool (solutions.SpeedEstimator()): đối tượng SpeedEstimator của YOLO
            frame_output (np.array): ảnh đã qua xử lý được vẽ hoặc không vẽ (tuỳ vào biến is_draw)\
            các thông tin được chuẩn đoán
        Examples:
            Hướng dẫn chạy xử lý 1 video đơn
            >>> analyzer = AnalyzeOnRoadBase(
            >>>     path_video=path_video,
            >>>     meter_per_pixel=meter_per_pixel,
            >>>     info_dict=info_dict,
            >>>     frame_dict=frame_dict,
            >>>     lock_info=lock_info,
            >>>     lock_frame=lock_frame,
            >>> )
            >>> analyzer.process_on_single_video()
    """
    
    
    
    
    
    def __init__(self, path_video = "./video_test/CAU RONG.mp4", meter_per_pixel = 0.06,
                 model_path= conf.MODELS_PATH, time_step=30,
                 is_draw=True, device= conf.DEVICE, iou=0.3, conf=0.2, show=False,
                 region = np.array([[50, 400], [50, 265], [370, 130], [600, 130], [600, 400]])):
        
        






















        try:
            self.speed_tool = solutions.SpeedEstimator(
                model=model_path,
                tracker='bytetrack.yaml',
                verbose=False,
                show=False,
                device=device,
                iou=iou,
                conf=conf,
                meter_per_pixel=meter_per_pixel,
                max_hist=3,  # Giảm từ 20 xuống 3 để tốc độ hiển thị nhanh hơn
                fps=25  # FPS của video để tính tốc độ chính xác
            )
            print(f"✅ SpeedEstimator initialized successfully for {path_video}")
        except Exception as e:
            print(f"❌ Failed to initialize SpeedEstimator for {path_video}: {e}")
            raise

        self.region = region
        self.region_pts = region.reshape((-1, 1, 2))

        self.show = show
        self.path_video = path_video
        self.name = path_video.split('/')[-1][:-4]

        self.count_car_display = 0
        self.list_count_car = []
        self.speed_car_display = 0
        self.list_speed_car = []

        self.count_motor_display = 0
        self.list_count_motor = []
        self.speed_motor_display = 0
        self.list_speed_motor = []

        self.time_pre = datetime.now()
        self.frame_output = None
        self.time_step = time_step
        self.frame_predict = None
        self.is_draw = is_draw
        self.delta_time = 0
        self.time_pre_for_fps = datetime.now()

        # ROI
        self.roi_y_start = 130
        self.roi_x_start = 50

        # Draw
        self.font = cv2.FONT_HERSHEY_SIMPLEX
        self.font_scale = 0.5
        self.font_thickness = 1
        self.color_motor = (0, 0, 255)  # Red for motorcycles
        self.color_car = (255, 0, 0)    # Blue for cars
        self.color_region = (0, 255, 255)  # Yellow for region

        # Tracking
        self.ids = None
        self.speeds = {}
        self.speeds = {}
        self.boxes = None
        self.classes = None

        # Speed Violation Detector
        try:
            self.speed_detector = SpeedViolationDetector(speed_limit_car=60, speed_limit_motor=50)
            print("✅ Speed Violation Detector initialized")
        except Exception as e:
            print(f"⚠️ Failed to init Speed Violation Detector: {e}")

    @abstractmethod
    def update_for_frame(self):
        pass

    @abstractmethod
    def update_for_vehicle(self):
        pass

    def update_data(self):
        """Hàm này sẽ được gọi để cập nhật dữ liệu cho frame và thông tin phương tiện sau một khoảng thời gian
            đã thiết lập là time_step"""

        # Gọi hàm này để cập nhật dữ liệu cho frame (luôn được cập nhật đảm bảo tính realtime)
        self.update_for_frame()

        # Tính toán thời gian đã trôi qua kể từ lần cập nhật trước
        time_now = datetime.now()
        self.delta_time = (time_now - self.time_pre).total_seconds()

        # Khi đủ thời gian đã thiết lập, cập nhật thông tin phương tiện
        if self.delta_time >= self.time_step:
            self.time_pre = time_now

            # Tính toán trung bình các giá trị - deque tự động giới hạn size
            self.count_car_display = avg_none_zero(self.list_count_car)
            self.speed_car_display = avg_none_zero(self.list_speed_car)
            self.count_motor_display = avg_none_zero(self.list_count_motor)
            self.speed_motor_display = avg_none_zero(self.list_speed_motor)

            # Cập nhật thông tin phương tiện vào info_dict
            self.update_for_vehicle()

            # Reset danh sách để chuẩn bị cho lần cập nhật tiếp theo
            self.list_count_car.clear()
            self.list_count_motor.clear()
            self.list_speed_car.clear()
            self.list_speed_motor.clear()

    def process_single_frame(self, frame_input):
        """Hàm này xử lý từng frame một
        Args:
            frame_input (np.array): Ảnh được đọc từ opencv
        """
        try:
            # Tránh copy toàn bộ frame, chỉ tạo view
            self.frame_output = frame_input

            # Sử dụng view thay vì copy - ascontiguousarray để đảm bảo memory layout
            self.frame_predict = np.ascontiguousarray(
                self.frame_output[self.roi_y_start:, self.roi_x_start:]
            )

            # Cần dùng bản copy để tránh công cụ ghi đè label lên ảnh đầu vào
            # Run SpeedEstimator với tracking - sử dụng process() method
            if self.speed_tool:
                try:
                    results = self.speed_tool.process(self.frame_predict.copy())
                except Exception as e:
                    print(f"❌ Error running SpeedEstimator: {e}")
                    pass

            self.post_processing()

            # Vẽ đè lên hình các thông tin
            if self.is_draw:
                self.draw_info_to_frame_output()
            # p = Thread(target= lambda : self.post_processing())
            # p.start()


            # Cập nhật data
            self.update_data()

        except Exception as e:
            print(f"Lỗi khi xử lý với file {self.name}: {e}")

    def post_processing(self):
        if self.speed_tool.track_data is not None:
            # Batch convert to numpy một lần thay vì nhiều lần
            track_data = self.speed_tool.track_data
            self.speeds = self.speed_tool.spd

            # Check if track_data attributes exist before accessing
            if track_data.id is not None and track_data.cls is not None and track_data.xyxy is not None:
                self.ids = track_data.id.cpu().numpy().astype(np.int32)
                self.classes = track_data.cls.cpu().numpy().astype(np.int32)
                self.boxes = track_data.xyxy.cpu().numpy().astype(np.int32)
            else:
                # No tracks found, set empty arrays
                return

            car_mask = (self.classes == 0)
            motor_mask = (self.classes == 1)

            count_car = np.sum(car_mask)
            count_motor = np.sum(motor_mask)

            self.list_count_car.append(int(count_car))
            self.list_count_motor.append(int(count_motor))

            car_ids = self.ids[car_mask]
            motor_ids = self.ids[motor_mask]

            car_speeds = [self.speeds[tid] for tid in car_ids if tid in self.speeds]
            motor_speeds = [self.speeds[tid] for tid in motor_ids if tid in self.speeds]

            if car_speeds:
                self.list_speed_car.extend(car_speeds)
            if motor_speeds:
                self.list_speed_motor.extend(motor_speeds)
            
            # --- TÍNH NĂNG MỚI: PHÁT HIỆN VI PHẠM TỐC ĐỘ ---
            # Chỉ check nếu có detector (được init ở __init__)
            if hasattr(self, 'speed_detector'):
                 # Duyệt qua tất cả xe được track
                for i, track_id in enumerate(self.ids):
                    if track_id in self.speeds:
                        speed = self.speeds[track_id]
                        vehicle_type = 'car' if self.classes[i] == 0 else 'motorbike'
                        bbox = self.boxes[i]
                        
                        # Gọi detector check (chạy sync db save, telegram chạy async ngầm trong detector nếu có loop)
                        # Ở đây chúng ta gọi hàm save_violation_to_db_sync gián tiếp qua logic check
                        # Tuy nhiên Detector check_speed_violation đang là async. 
                        # Chúng ta nên sử dụng thread riêng hoặc run_coroutine_threadsafe nếu đang trong loop
                        
                        # Check speed violation (sync version for video test)
                        try:
                            self.speed_detector.process_speed_violation_sync(
                                frame=self.frame_output,
                                track_id=track_id,
                                vehicle_type=vehicle_type,
                                speed=speed,
                                bbox=bbox,
                                camera_name=self.name
                            )
                        except Exception as e:
                            print(f"⚠️ Error checking speed violation: {e}")
                            pass


    def draw_info_to_frame_output(self):
        """Hàm này để vẽ các thông tin lên ảnh - optimized version"""
        try:
            if self.ids is not None and len(self.ids) > 0:
                # Vectorized center calculation
                x1 = self.boxes[:, 0]
                y1 = self.boxes[:, 1]
                x2 = self.boxes[:, 2]
                y2 = self.boxes[:, 3]

                cx = ((x1 + x2) // 2).astype(np.int32)
                cy = ((y1 + y2) // 2).astype(np.int32)

                # Batch ROI
                cx_adj = cx + self.roi_x_start
                cy_adj = cy + self.roi_y_start

                # Tìm các điểm nằm trong vùng ROI
                valid_indices = []
                for idx in range(len(cx_adj)):
                    result = cv2.pointPolygonTest(
                        self.region_pts,
                        (int(cx_adj[idx]), int(cy_adj[idx])),
                        False
                    )
                    if result >= 0:
                        valid_indices.append(idx)

                valid_indices = np.array(valid_indices)

                for idx in valid_indices:
                    track_id = self.ids[idx]
                    class_id = self.classes[idx]
                    speed_id = self.speeds.get(track_id, 0)

                    color = self.color_motor if class_id == 1 else self.color_car
                    label = f"{speed_id} km/h"

                    cx_local = cx[idx]
                    cy_local = cy[idx]

                    cv2.putText(self.frame_predict, label,
                               (cx_local - 50, cy_local - 15),
                               self.font, self.font_scale, color, self.font_thickness)
                    cv2.circle(self.frame_predict, (cx_local, cy_local), 5, color, -1)

            # Gắn lại vùng được cắt để predict lại vào frame ban đầu
            self.frame_output[130:, 50:] = self.frame_predict
            cv2.polylines(self.frame_output, [self.region_pts],
                         isClosed=True, color=self.color_region, thickness=4)

            info = [
                f"Xe may: {self.count_motor_display} xe, Vtb = {self.speed_motor_display} km/h",
                f"Oto: {self.count_car_display} xe, Vtb = {self.speed_car_display} km/h"
            ]

            colors = [(0, 0, 200), (200, 0, 0)]

            for i, t in enumerate(info):
                cvzone.putTextRect(
                    self.frame_output, t,
                    (10, 25 + i * 35),
                    scale=1.5, thickness=2,
                    colorT=colors[i],
                    colorR=(50, 50, 50),
                    border=2,
                    colorB=(255, 255, 255)
                )

        except Exception as e:
            print(f"Lỗi khi vẽ: {e}")

    def process_on_single_video(self):
        """Hàm này sẽ được gọi để xử lý video bằng việc đọc từng frame và xử lý từng frame một"""
        cam = cv2.VideoCapture(self.path_video)

        if not cam.isOpened():
            print(f'Không thể mở video: {self.path_video}')
            return

        target_size = (600, 400)

        try:
            while True:
                check, cap = cam.read()

                if not check:
                    print(f'Kết thúc video: {self.path_video}')
                    # Restart video để loop
                    cam.set(cv2.CAP_PROP_POS_FRAMES, 0)
                    continue

                cap = cv2.resize(cap, target_size)

                # FPS calculation - optimized
                time_now = datetime.now()
                delta_time = (time_now - self.time_pre_for_fps).total_seconds()
                fps = round(1 / delta_time) if delta_time > 0 else 0
                self.time_pre_for_fps = time_now

                cvzone.putTextRect(cap, f"FPS: {fps}",
                                 (516, 20),
                                 scale=1.1, thickness=2,
                                 colorT=(0, 255, 100),
                                 colorR=(50, 50, 50),
                                 border=2,
                                 colorB=(255, 255, 255))

                # Xử lý từng frame
                self.process_single_frame(cap)

                # Hiển thị frame nếu show là True
                if self.show:
                    cv2.imshow(f'{self.name}', self.frame_output)
                    if cv2.waitKey(1) & 0xFF == ord('q'):
                        break

        except KeyboardInterrupt:
            print(f"Đã dừng xử lý {self.name}")
        except Exception as e:
            print(f"Lỗi khi xử lý {self.name}: {e}")
        finally:
            # Giải phóng tài nguyên
            cam.release()
            if self.show:
                cv2.destroyAllWindows()

#************************************************************************ Script for testing *******************************************************
if __name__ == "__main__":
    # Example usage
    path_video = conf.path_videos[1]
    meter_per_pixel = conf.meter_per_pixels[1]

    analyzer = AnalyzeOnRoadBase(
        path_video=path_video,
        meter_per_pixel=meter_per_pixel,
        region=conf.regions[1],
        show=True
    )

    analyzer.process_on_single_video()