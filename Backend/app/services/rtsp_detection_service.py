import cv2
import asyncio
import threading
import time
import os
import re
from urllib.parse import quote, urlparse, urlunparse
from typing import Optional, Dict, List
import numpy as np
from ultralytics import YOLO, solutions
import torch
import cvzone
from app.services.red_light_detector import RedLightDetector
from app.core.config import SettingMetricTransport
conf_settings = SettingMetricTransport()


def encode_rtsp_url(rtsp_url: str) -> str:
    """
    Tự động URL encode password trong RTSP URL để xử lý ký tự đặc biệt như $ # @ v.v.
    Ví dụ: rtsp://user:Pass$123@ip:554/path -> rtsp://user:Pass%24123@ip:554/path
    """
    if not rtsp_url or not rtsp_url.startswith('rtsp://'):
        return rtsp_url
    
    try:
        # Parse URL để lấy các phần
        # Format: rtsp://username:password@host:port/path
        match = re.match(r'rtsp://([^:]+):([^@]+)@(.+)', rtsp_url)
        if match:
            username = match.group(1)
            password = match.group(2)
            rest = match.group(3)  # host:port/path
            
            # Xóa escaped backslash từ .env (ví dụ: \$ -> $)
            password = password.replace('\\$', '$').replace('\\#', '#').replace('\\@', '@')
            
            # URL encode password (giữ nguyên nếu đã encode)
            if '%' not in password:  # Chưa encode
                encoded_password = quote(password, safe='')
            else:
                encoded_password = password
            
            # Reconstruct URL
            encoded_url = f"rtsp://{username}:{encoded_password}@{rest}"
            if encoded_url != rtsp_url:
                print(f"🔐 Password đã được URL-encode")
            return encoded_url
        else:
            # Không có credentials hoặc format khác
            return rtsp_url
    except Exception as e:
        print(f"⚠️ Không thể encode URL: {e}")
        return rtsp_url


class RTSPDetectionService:
    """Service to handle RTSP camera streaming with YOLO detection using DEDICATED THREAD"""

    def __init__(self, rtsp_url: str, camera_name: str = "camera_live", model_path: str = "./app/ai_models/model N/original model/best.pt", meter_per_pixel: float = 0.04, region: Optional[np.ndarray] = None):
        # Tự động URL encode password trong RTSP URL
        self.rtsp_url = encode_rtsp_url(rtsp_url)
        self.camera_name = camera_name
        self.model_path = model_path
        self.meter_per_pixel = meter_per_pixel
        self.cap: Optional[cv2.VideoCapture] = None
        self.speed_tool: Optional[solutions.SpeedEstimator] = None
        self.is_running = False

        # ROI Region (default for RTSP cameras)
        if region is None:
            # Default region (full frame minus some margin)
            self.region = np.array([[50, 400], [50, 265], [370, 130], [600, 130], [600, 400]])
        else:
            self.region = region
        self.region_pts = self.region.reshape((-1, 1, 2))

        # Data containers
        self.current_frame: Optional[np.ndarray] = None
        self.current_detections: Dict = {
            "count_car": 0,
            "count_motor": 0,
            "speed_car": 0.0,
            "speed_motor": 0.0,
            "total_vehicles": 0,
            "violations": []
        }
        self.lock = threading.Lock() # Use threading Lock for thread safety

        # Thread control
        self.thread: Optional[threading.Thread] = None
        self.stop_event = threading.Event()

        # Red light detector
        self.red_light_detector = RedLightDetector(camera_name)
        self.enable_violation_detection = False

        # FPS Stats
        self.fps = 0
        self.frame_count = 0
        self.start_time = time.time()

        # Speed tracking data
        self.speeds = {}
        self.track_ids = None
        self.track_classes = None

        # Drawing styles
        self.font = cv2.FONT_HERSHEY_SIMPLEX
        self.font_scale = 0.5
        self.font_thickness = 1
        self.color_motor = (0, 0, 255)  # Red for motorcycles
        self.color_car = (255, 0, 0)    # Blue for cars
        self.color_region = (0, 255, 255)  # Yellow for region

    def load_model(self) -> bool:
        """Load SpeedEstimator model with tracking"""
        try:
            if torch.cuda.is_available():
                device = 'cuda:0'
                print(f"🚀 GPU detected: {torch.cuda.get_device_name(0)}")
            else:
                device = 'cpu'
                print("⚠️ No GPU detected, using CPU")

            print(f"Loading SpeedEstimator model from {self.model_path}...")
            self.speed_tool = solutions.SpeedEstimator(
                model=self.model_path,
                tracker='bytetrack.yaml',
                verbose=False,
                show=False,
                device=device,
                iou=0.3,
                conf=0.2,
                meter_per_pixel=self.meter_per_pixel,
                max_hist=3,  # Giảm từ 20 xuống 3 để tốc độ hiển thị nhanh hơn
                fps=25  # FPS của camera để tính tốc độ chính xác
            )
            print(f"✅ SpeedEstimator model loaded successfully on {device}")
            return True
        except Exception as e:
            print(f"❌ Error loading SpeedEstimator model: {e}")
            return False

    def connect(self) -> bool:
        """Connect to RTSP stream and START BACKGROUND THREAD"""
        try:
            print(f"🔗 Attempting to connect to RTSP: {self.rtsp_url[:50]}...")

            # Force TCP transport for RTSP (Critical for some external cameras)
            os.environ["OPENCV_FFMPEG_CAPTURE_OPTIONS"] = "rtsp_transport;tcp|timeout;60000000"

            # Create VideoCapture with RTSP options for better stability
            self.cap = cv2.VideoCapture(self.rtsp_url, cv2.CAP_FFMPEG)

            # Set RTSP transport to TCP and increase timeout for external cameras
            self.cap.set(cv2.CAP_PROP_OPEN_TIMEOUT_MSEC, 30000)  # 30 second timeout for external
            self.cap.set(cv2.CAP_PROP_READ_TIMEOUT_MSEC, 30000)  # 30 second read timeout

            # Buffer and frame settings
            self.cap.set(cv2.CAP_PROP_BUFFERSIZE, 3)
            self.cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*'H264'))

            # Try to read a test frame to verify connection
            print(f"📡 Testing RTSP connection (waiting up to 30s)...")

            # Skip first few frames (often corrupted)
            for i in range(3):
                ret, _ = self.cap.read()
                if not ret:
                    break

            # Read the actual test frame
            ret, test_frame = self.cap.read()

            if ret and test_frame is not None:
                print(f"✅ RTSP connection successful! Frame size: {test_frame.shape}")

                self.is_running = True
                self.stop_event.clear()

                # Start the dedicated capture/inference thread
                self.thread = threading.Thread(target=self._capture_loop, daemon=True)
                self.thread.start()

                print(f"✅ RTSP Stream & Inference Thread started for {self.camera_name}")
                return True
            else:
                print(f"❌ Failed to read test frame from RTSP stream")
                print(f"   Check if camera URL is correct: {self.rtsp_url}")
                print(f"   Check if camera is online and accessible")
                return False

        except Exception as e:
            print(f"❌ Error connecting to RTSP stream: {e}")
            print(f"   URL: {self.rtsp_url}")
            print(f"   Possible issues:")
            print(f"   - Camera is offline or not accessible")
            print(f"   - Incorrect credentials in RTSP URL")
            print(f"   - Network firewall blocking connection")
            print(f"   - RTSP port 554 not accessible")
            return False

    def disconnect(self):
        """Stop thread and release resources"""
        self.is_running = False
        self.stop_event.set()
        
        if self.thread and self.thread.is_alive():
            self.thread.join(timeout=2.0)
            
        if self.cap:
            self.cap.release()
            self.cap = None
        print("🔌 RTSP camera disconnected")

    def _capture_loop(self):
        """
        Main loop running in a separate thread.
        Handles: Frame Read -> YOLO Inference -> Data Update
        """
        print(f"🧵 Thread started for {self.camera_name}")
        
        while not self.stop_event.is_set():
            if not self.cap or not self.cap.isOpened():
                time.sleep(1)
                continue

            # 1. READ FRAME (Blocking, but okay because we are in a thread!)
            ret, frame = self.cap.read()
            
            if not ret:
                print(f"⚠️ {self.camera_name}: Frame read failed, reconnecting...")
                self.cap.release()
                time.sleep(2)
                self.cap = cv2.VideoCapture(self.rtsp_url)
                self.cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)
                continue

            # 2. INFERENCE WITH TRACKING (Heavy CPU/GPU task)
            processed_frame = frame
            detections = self.current_detections.copy() # Default to old values

            if self.speed_tool:
                try:
                    # Run SpeedEstimator with tracking - returns results object
                    processed_frame = self.speed_tool.estimate_speed(frame.copy())

                    # Extract tracking data from internal attributes
                    if hasattr(self.speed_tool, 'track_data') and self.speed_tool.track_data is not None:
                        track_data = self.speed_tool.track_data
                        self.speeds = self.speed_tool.spd

                        # Process counts and speeds
                        count_car = 0
                        count_motor = 0
                        detections_list = []
                        car_speeds = []
                        motor_speeds = []

                        if track_data.id is not None and track_data.cls is not None and track_data.xyxy is not None:
                            self.track_ids = track_data.id.cpu().numpy().astype(np.int32)
                            self.track_classes = track_data.cls.cpu().numpy().astype(np.int32)
                            track_boxes = track_data.xyxy.cpu().numpy().astype(np.int32)

                            # Draw annotations on frame FIRST
                            processed_frame = frame.copy()

                            # Filter vehicles by ROI and count
                            for i, cls in enumerate(self.track_classes):
                                track_id = self.track_ids[i]
                                bbox = track_boxes[i]
                                x1, y1, x2, y2 = bbox

                                # Calculate center point
                                cx = (x1 + x2) // 2
                                cy = (y1 + y2) // 2

                                # Check if center is inside ROI (if ROI is defined)
                                inside_roi = True
                                if self.region_pts is not None:
                                    result = cv2.pointPolygonTest(self.region_pts, (int(cx), int(cy)), False)
                                    inside_roi = (result >= 0)

                                if inside_roi:  # Inside ROI or no ROI defined
                                    # Count vehicles
                                    if int(cls) == 0:
                                        count_car += 1
                                        if track_id in self.speeds:
                                            car_speeds.append(self.speeds[track_id])
                                    elif int(cls) == 1:
                                        count_motor += 1
                                        if track_id in self.speeds:
                                            motor_speeds.append(self.speeds[track_id])

                                    # Draw for vehicles
                                    speed = self.speeds.get(track_id, 0)
                                    color = self.color_motor if cls == 1 else self.color_car

                                    # Draw bounding box
                                    cv2.rectangle(processed_frame, (x1, y1), (x2, y2), color, 2)

                                    # Draw speed label
                                    label = f"{speed} km/h"
                                    cv2.putText(processed_frame, label, (x1, y1 - 10),
                                              self.font, self.font_scale, color, self.font_thickness)

                                    # Draw center point
                                    cv2.circle(processed_frame, (cx, cy), 5, color, -1)

                                # Add to detections list (all vehicles, not just in ROI)
                                detections_list.append({
                                    'class': 'car' if int(cls) == 0 else 'motor',
                                    'bbox': tuple(bbox),
                                    'conf': 1.0,
                                    'track_id': int(track_id),
                                    'speed': self.speeds.get(track_id, 0)
                                })

                            # Calculate average speeds
                            speed_car = round(np.mean(car_speeds)) if car_speeds else 0
                            speed_motor = round(np.mean(motor_speeds)) if motor_speeds else 0

                            # Draw ROI polygon (only if ROI is defined)
                            if self.region_pts is not None:
                                cv2.polylines(processed_frame, [self.region_pts],
                                            isClosed=True, color=self.color_region, thickness=4)

                            # Draw info text with cvzone (like video test)
                            info = [
                                f"Xe may: {count_motor} xe, Vtb = {speed_motor} km/h",
                                f"Oto: {count_car} xe, Vtb = {speed_car} km/h"
                            ]
                            colors = [(0, 0, 200), (200, 0, 0)]

                            for i, t in enumerate(info):
                                cvzone.putTextRect(
                                    processed_frame, t,
                                    (10, 25 + i * 35),
                                    scale=1.5, thickness=2,
                                    colorT=colors[i],
                                    colorR=(50, 50, 50),
                                    border=2,
                                    colorB=(255, 255, 255)
                                )
                        else:
                            # No tracks found
                            speed_car = 0
                            speed_motor = 0
                            processed_frame = frame

                        # Red light check
                        violations = []
                        if self.enable_violation_detection:
                            light_status = self.red_light_detector.detect_light_color(frame)
                            violations = self.red_light_detector.check_violation(frame, detections_list, light_status)
                            processed_frame = self.red_light_detector.draw_monitoring_overlay(processed_frame, light_status, show_roi=True)

                        detections = {
                            "count_car": count_car,
                            "count_motor": count_motor,
                            "speed_car": float(speed_car),
                            "speed_motor": float(speed_motor),
                            "total_vehicles": count_car + count_motor,
                            "violations": violations
                        }
                    else:
                        # No track data
                        processed_frame = frame

                except Exception as e:
                    print(f"❌ Inference Error: {e}")

            # 3. UPDATE STATE (Thread-safe)
            with self.lock:
                self.current_frame = processed_frame
                self.current_detections = detections
                
            # FPS Calculation logic (optional)
            self.frame_count += 1
            if self.frame_count % 30 == 0:
                 elapsed = time.time() - self.start_time
                 self.fps = 30 / elapsed if elapsed > 0 else 0
                 self.start_time = time.time()
                 # print(f"FPS: {self.fps:.2f}")

    # --- API ACCESSORS (Called from Main Thread) ---

    async def get_current_frame(self) -> Optional[np.ndarray]:
        """Non-blocking getter for the latest frame"""
        with self.lock:
            if self.current_frame is None:
                return None
            return self.current_frame.copy()

    async def get_detections(self) -> Dict:
        """Non-blocking getter for statistics"""
        with self.lock:
            return self.current_detections.copy()

    # Backwards compatibility for API calls
    async def process_frame(self) -> Optional[np.ndarray]:
        """Legacy method used by api_rtsp.py - now just returns latest frame"""
        # Sleep briefly to mimic 'waiting for new frame' and avoid tight loops in API
        await asyncio.sleep(0.01) 
        return await self.get_current_frame()

    def encode_frame(self, frame: np.ndarray, quality: int = 70) -> Optional[bytes]:
        """Encode frame to JPEG"""
        try:
            # Resize if needed
            height, width = frame.shape[:2]
            if width > 1280:
                frame = cv2.resize(frame, (1280, int(height * (1280/width))))
                
            encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), quality]
            _, buffer = cv2.imencode('.jpg', frame, encode_param)
            return buffer.tobytes()
        except Exception as e:
            return None

    # Config methods...
    def configure_red_light_detection(self, roi: Dict, stop_line_y: int, enable: bool = True):
        self.red_light_detector.set_traffic_light_roi(roi['x'], roi['y'], roi['w'], roi['h'])
        self.red_light_detector.set_stop_line(stop_line_y)
        self.enable_violation_detection = enable

    def enable_red_light_monitoring(self, enable: bool = True):
        self.enable_violation_detection = enable

    def get_violation_statistics(self) -> Dict:
        return self.red_light_detector.get_statistics()


class RTSPDetectionManager:
    """Manager for RTSP streams"""
    def __init__(self):
        self.streams: Dict[str, RTSPDetectionService] = {}

    def add_stream(self, name: str, rtsp_url: str, model_path: str = "./app/ai_models/model N/original model/best.pt", meter_per_pixel: float = 0.04, region: Optional[np.ndarray] = None) -> bool:
        if name in self.streams: return False

        stream = RTSPDetectionService(rtsp_url, camera_name=name, model_path=model_path, meter_per_pixel=meter_per_pixel, region=region)
        if stream.load_model() and stream.connect():
            self.streams[name] = stream
            return True
        return False

    def remove_stream(self, name: str):
        if name in self.streams:
            self.streams[name].disconnect()
            del self.streams[name]

    def get_stream(self, name: str) -> Optional[RTSPDetectionService]:
        return self.streams.get(name)

    def get_all_streams(self) -> list:
        return list(self.streams.keys())

    def disconnect_all(self):
        for stream in self.streams.values():
            stream.disconnect()
        self.streams.clear()

