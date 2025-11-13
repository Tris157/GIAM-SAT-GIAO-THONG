import cv2
import asyncio
from typing import Optional
import numpy as np


class RTSPStreamService:
    """Service to handle RTSP camera streaming"""

    def __init__(self, rtsp_url: str):
        self.rtsp_url = rtsp_url
        self.cap: Optional[cv2.VideoCapture] = None
        self.is_running = False
        self.current_frame: Optional[np.ndarray] = None
        self.lock = asyncio.Lock()

    def connect(self) -> bool:
        """Connect to RTSP stream"""
        try:
            self.cap = cv2.VideoCapture(self.rtsp_url)

            # Set buffer size to reduce latency
            self.cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)

            if self.cap.isOpened():
                self.is_running = True
                return True
            return False
        except Exception as e:
            print(f"Error connecting to RTSP stream: {e}")
            return False

    def disconnect(self):
        """Disconnect from RTSP stream"""
        self.is_running = False
        if self.cap:
            self.cap.release()
            self.cap = None

    async def read_frame(self) -> Optional[np.ndarray]:
        """Read a frame from the RTSP stream"""
        if not self.cap or not self.is_running:
            return None

        try:
            ret, frame = self.cap.read()
            if ret:
                async with self.lock:
                    self.current_frame = frame
                return frame
            return None
        except Exception as e:
            print(f"Error reading frame: {e}")
            return None

    async def get_current_frame(self) -> Optional[np.ndarray]:
        """Get the current frame"""
        async with self.lock:
            return self.current_frame.copy() if self.current_frame is not None else None

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
            print(f"Error encoding frame: {e}")
            return None


class RTSPStreamManager:
    """Manager for multiple RTSP streams"""

    def __init__(self):
        self.streams: dict[str, RTSPStreamService] = {}

    def add_stream(self, name: str, rtsp_url: str) -> bool:
        """Add a new RTSP stream"""
        if name in self.streams:
            return False

        stream = RTSPStreamService(rtsp_url)
        if stream.connect():
            self.streams[name] = stream
            return True
        return False

    def remove_stream(self, name: str):
        """Remove an RTSP stream"""
        if name in self.streams:
            self.streams[name].disconnect()
            del self.streams[name]

    def get_stream(self, name: str) -> Optional[RTSPStreamService]:
        """Get a stream by name"""
        return self.streams.get(name)

    def get_all_streams(self) -> list[str]:
        """Get all stream names"""
        return list(self.streams.keys())

    def disconnect_all(self):
        """Disconnect all streams"""
        for stream in self.streams.values():
            stream.disconnect()
        self.streams.clear()
