import cv2
import asyncio
from typing import Optional, Dict, List
import numpy as np
from ultralytics import YOLO
import openvino as ov
import torch
from app.services.red_light_detector import RedLightDetector


class RTSPDetectionService:
    """Service to handle RTSP camera streaming with YOLO detection"""

    def __init__(self, rtsp_url: str, camera_name: str = "camera_live", model_path: str = "./app/ai_models/model N/original model/obstacle.pt"):
        self.rtsp_url = rtsp_url
        self.camera_name = camera_name
        self.model_path = model_path
        self.cap: Optional[cv2.VideoCapture] = None
        self.model: Optional[YOLO] = None
        self.is_running = False
        self.current_frame: Optional[np.ndarray] = None
        self.current_detections: Dict = {
            "count_car": 0,
            "count_motor": 0,
            "speed_car": 0.0,
            "speed_motor": 0.0,
            "total_vehicles": 0,
            "violations": []  # Red light violations
        }
        self.lock = asyncio.Lock()

        # Red light violation detector
        self.red_light_detector = RedLightDetector(camera_name)
        self.enable_violation_detection = False  # Bật/tắt detection vi phạm

    def load_model(self) -> bool:
        """Load YOLO model with GPU support (auto-detect)"""
        try:
            # Detect available device
            if torch.cuda.is_available():
                device = 'cuda:0'
                gpu_name = torch.cuda.get_device_name(0)
                print(f"🚀 GPU detected: {gpu_name}")
            else:
                device = 'cpu'
                print("⚠️ No GPU detected, using CPU")

            print(f"Loading YOLO model from {self.model_path}...")
            self.model = YOLO(self.model_path, task='detect')

            # Move model to device
            self.model.to(device)

            print(f"✅ YOLO model loaded successfully on {device.upper()}")
            return True
        except Exception as e:
            print(f"❌ Error loading model: {e}")
            return False

    def connect(self) -> bool:
        """Connect to RTSP stream"""
        try:
            self.cap = cv2.VideoCapture(self.rtsp_url)

            # Set buffer size to reduce latency
            self.cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)

            # Set resolution (optional)
            self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
            self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

            if self.cap.isOpened():
                self.is_running = True
                print("✅ RTSP camera connected successfully")
                return True
            else:
                print("❌ Failed to open RTSP stream")
                return False
        except Exception as e:
            print(f"❌ Error connecting to RTSP stream: {e}")
            return False

    def disconnect(self):
        """Disconnect from RTSP stream"""
        self.is_running = False
        if self.cap:
            self.cap.release()
            self.cap = None
        print("🔌 RTSP camera disconnected")

    async def process_frame(self) -> Optional[np.ndarray]:
        """Read and process frame with YOLO detection"""
        if not self.cap or not self.is_running or not self.model:
            return None

        try:
            ret, frame = self.cap.read()
            if not ret or frame is None:
                # Camera disconnected, try to reconnect
                if not hasattr(self, '_reconnect_attempts'):
                    self._reconnect_attempts = 0

                self._reconnect_attempts += 1

                # Only log every 10 attempts to avoid spam
                if self._reconnect_attempts % 10 == 1:
                    print(f"⚠️ Camera disconnected, attempting reconnect (attempt {self._reconnect_attempts})...")

                self.cap.release()
                await asyncio.sleep(3)  # Wait 3s before reconnecting

                try:
                    self.cap = cv2.VideoCapture(self.rtsp_url)
                    self.cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)
                    self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
                    self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

                    # Test if reconnection successful
                    test_ret, test_frame = self.cap.read()
                    if test_ret and test_frame is not None:
                        print(f"✅ Camera reconnected successfully!")
                        self._reconnect_attempts = 0  # Reset counter
                        return test_frame
                except Exception as e:
                    print(f"❌ Reconnect failed: {e}")

                return None

            # Run YOLO detection
            results = self.model(frame, verbose=False, conf=0.3, iou=0.4)

            # Process detections
            count_car = 0
            count_motor = 0
            detections_list = []  # For red light detection

            if results and len(results) > 0:
                result = results[0]

                # Draw bounding boxes
                annotated_frame = result.plot()

                # Count vehicles by class and prepare for red light detection
                if result.boxes is not None and len(result.boxes) > 0:
                    classes = result.boxes.cls.cpu().numpy()
                    boxes = result.boxes.xyxy.cpu().numpy()  # Get bounding boxes
                    confs = result.boxes.conf.cpu().numpy()  # Get confidences

                    for i, cls in enumerate(classes):
                        bbox = boxes[i]  # (x1, y1, x2, y2)
                        conf = confs[i]

                        if int(cls) == 0:  # Car class
                            count_car += 1
                            vehicle_type = 'car'
                        elif int(cls) == 1:  # Motorcycle class
                            count_motor += 1
                            vehicle_type = 'motor'
                        else:
                            continue

                        # Add to detections list for red light detection
                        detections_list.append({
                            'class': vehicle_type,
                            'bbox': tuple(bbox),
                            'conf': float(conf)
                        })

                # Red light violation detection
                violations = []
                if self.enable_violation_detection:
                    # Detect traffic light color
                    light_status = self.red_light_detector.detect_light_color(frame)

                    # Check for violations
                    violations = self.red_light_detector.check_violation(
                        frame,
                        detections_list,
                        light_status
                    )

                    # Draw monitoring overlay
                    annotated_frame = self.red_light_detector.draw_monitoring_overlay(
                        annotated_frame,
                        light_status,
                        show_roi=True
                    )

                # Update detections
                async with self.lock:
                    self.current_detections = {
                        "count_car": count_car,
                        "count_motor": count_motor,
                        "speed_car": 0.0,  # Speed estimation can be added later
                        "speed_motor": 0.0,
                        "total_vehicles": count_car + count_motor,
                        "violations": violations
                    }
                    self.current_frame = annotated_frame

                return annotated_frame
            else:
                # No detections, but still check traffic light if enabled
                if self.enable_violation_detection:
                    light_status = self.red_light_detector.detect_light_color(frame)
                    frame = self.red_light_detector.draw_monitoring_overlay(
                        frame,
                        light_status,
                        show_roi=True
                    )

                # No detections, return original frame
                async with self.lock:
                    self.current_detections = {
                        "count_car": 0,
                        "count_motor": 0,
                        "speed_car": 0.0,
                        "speed_motor": 0.0,
                        "total_vehicles": 0,
                        "violations": []
                    }
                    self.current_frame = frame
                return frame

        except Exception as e:
            print(f"❌ Error processing frame: {e}")
            return None

    async def get_current_frame(self) -> Optional[np.ndarray]:
        """Get the current processed frame"""
        async with self.lock:
            return self.current_frame.copy() if self.current_frame is not None else None

    async def get_detections(self) -> Dict:
        """Get current detection results"""
        async with self.lock:
            return self.current_detections.copy()

    def encode_frame(self, frame: np.ndarray, quality: int = 85) -> Optional[bytes]:
        """Encode frame to JPEG bytes"""
        try:
            # Resize frame for better streaming performance
            height, width = frame.shape[:2]
            if width > 1280:
                scale = 1280 / width
                new_width = 1280
                new_height = int(height * scale)
                frame = cv2.resize(frame, (new_width, new_height))

            # Encode to JPEG
            encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), quality]
            _, buffer = cv2.imencode('.jpg', frame, encode_param)
            return buffer.tobytes()
        except Exception as e:
            print(f"❌ Error encoding frame: {e}")
            return None

    # Red Light Violation Detection Methods
    def configure_red_light_detection(self, roi: Dict, stop_line_y: int, enable: bool = True):
        """
        Configure red light violation detection

        Args:
            roi: Dictionary with keys 'x', 'y', 'w', 'h' for traffic light ROI
            stop_line_y: Y coordinate of the stop line
            enable: Enable or disable detection
        """
        self.red_light_detector.set_traffic_light_roi(
            roi['x'], roi['y'], roi['w'], roi['h']
        )
        self.red_light_detector.set_stop_line(stop_line_y)
        self.enable_violation_detection = enable
        print(f"✅ Red light detection configured for {self.camera_name}")

    def enable_red_light_monitoring(self, enable: bool = True):
        """Enable or disable red light violation monitoring"""
        self.enable_violation_detection = enable
        status = "enabled" if enable else "disabled"
        print(f"Red light monitoring {status} for {self.camera_name}")

    def get_violation_statistics(self) -> Dict:
        """Get red light violation statistics"""
        return self.red_light_detector.get_statistics()


class RTSPDetectionManager:
    """Manager for RTSP streams with detection"""

    def __init__(self):
        self.streams: Dict[str, RTSPDetectionService] = {}

    def add_stream(self, name: str, rtsp_url: str, model_path: str = "./app/ai_models/model N/original model/obstacle.pt") -> bool:
        """Add a new RTSP stream with detection"""
        if name in self.streams:
            print(f"⚠️ Stream {name} already exists")
            return False

        stream = RTSPDetectionService(rtsp_url, camera_name=name, model_path=model_path)

        # Load model first
        if not stream.load_model():
            return False

        # Then connect to camera
        if stream.connect():
            self.streams[name] = stream
            print(f"✅ Stream {name} added successfully")
            return True

        print(f"❌ Failed to add stream {name}")
        return False

    def remove_stream(self, name: str):
        """Remove an RTSP stream"""
        if name in self.streams:
            self.streams[name].disconnect()
            del self.streams[name]
            print(f"🗑️ Stream {name} removed")

    def get_stream(self, name: str) -> Optional[RTSPDetectionService]:
        """Get a stream by name"""
        return self.streams.get(name)

    def get_all_streams(self) -> list:
        """Get all stream names"""
        return list(self.streams.keys())

    def disconnect_all(self):
        """Disconnect all streams"""
        for stream in self.streams.values():
            stream.disconnect()
        self.streams.clear()
        print("🔌 All streams disconnected")
