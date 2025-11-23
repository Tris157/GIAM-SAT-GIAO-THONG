# ============================================================================
# FILE: red_light_detector.py - PHÁT HIỆN VI PHẠM VƯỢT ĐÈN ĐỎ
# ============================================================================
# File này chứa class RedLightDetector để:
# - Nhận diện màu đèn tín hiệu (đỏ/vàng/xanh) bằng HSV color space
# - Kiểm tra xe vượt vạch dừng khi đèn đỏ
# - Lưu ảnh bằng chứng vi phạm
# - Vẽ overlay giám sát lên frame video
#
# CÔNG NGHỆ SỬ DỤNG:
# - OpenCV (cv2): Xử lý ảnh và video
# - HSV Color Space: Nhận diện màu chính xác hơn RGB
# - NumPy: Xử lý ma trận và mảng

# ============================================================================
# PHẦN 1: IMPORT THƯ VIỆN
# ============================================================================

# Dòng 5: Import OpenCV
import cv2
# OpenCV (cv2): Thư viện Computer Vision mạnh nhất
# Dùng để:
# - Đọc/ghi ảnh (imread, imwrite)
# - Convert color space (cvtColor)
# - Vẽ hình (rectangle, line, putText)
# - Tạo mask (inRange)

# Dòng 6: Import NumPy
import numpy as np
# NumPy: Thư viện xử lý mảng và ma trận
# Frame ảnh là np.ndarray (mảng 3 chiều: height x width x channels)

# Dòng 7: Import type hints
from typing import Optional, Tuple, List, Dict
# - Optional[int]: Giá trị có thể None
# - Tuple[int, int, int, int]: Tuple 4 số nguyên (bbox)
# - List[Dict]: Danh sách các dict
# - Dict: Dictionary

# Dòng 8: Import datetime
from datetime import datetime
# Để tạo timestamp cho vi phạm và cooldown

# Dòng 9: Import os
import os
# Để tạo thư mục lưu ảnh vi phạm

# Dòng 10: Import asyncio
import asyncio
# Để chạy async function gửi Telegram

# Dòng 11: Import TelegramNotifier
from app.services.telegram_notifier import get_telegram_notifier
# Service gửi cảnh báo qua Telegram Bot


# ============================================================================
# PHẦN 2: CLASS REDLIGHTDETECTOR - DETECTOR CHÍNH
# ============================================================================

# Dòng 12-13: Định nghĩa class
class RedLightDetector:
    """
    Class phát hiện vi phạm vượt đèn đỏ

    NGUYÊN LÝ HOẠT ĐỘNG:

    1. NHẬN DIỆN MÀU ĐÈN:
       - Crop ROI (Region of Interest) chứa đèn tín hiệu
       - Convert BGR → HSV color space
       - Tạo mask cho từng màu (đỏ, vàng, xanh)
       - Đếm pixels của từng màu
       - Màu nào nhiều pixels nhất → đó là màu đèn

    2. KIỂM TRA VI PHẠM:
       - Lấy vị trí bottom (đáy) của bounding box xe
       - Nếu bottom_y > stop_line_y KHI đèn đỏ → VI PHẠM!
       - Lưu ảnh bằng chứng với annotations

    3. TRÁNH DUPLICATE:
       - Dùng cooldown: Sau khi detect vi phạm, đợi 5s mới detect lại
       - Dùng position key để track: xe ở cùng 1 vị trí không detect lại

    TẠI SAO DÙNG HSV THAY VÌ RGB?
    - HSV tách rời màu sắc (Hue) khỏi độ sáng (Value)
    - RGB bị ảnh hưởng nhiều bởi ánh sáng
    - Đèn đỏ trong bóng tối: RGB=(80,0,0) vs ánh sáng RGB=(255,0,0)
    - Nhưng HSV: Hue đều ~0° (đỏ) bất kể độ sáng
    """

    # ========================================================================
    # PHẦN 2.1: CONSTRUCTOR - KHỞI TẠO DETECTOR
    # ========================================================================

    # Dòng 15-39: Hàm __init__
    def __init__(self, camera_name: str):
        """
        Khởi tạo RedLightDetector

        Args:
            camera_name: Tên camera (ví dụ: "camera_live")

        GIẢI THÍCH CÁC THUỘC TÍNH:
        """

        # --- THÔNG TIN CAMERA ---
        # Dòng 16: Lưu tên camera
        self.camera_name = camera_name
        # Dùng để tạo filename cho ảnh vi phạm

        # --- CẤU HÌNH ROI VÀ STOP LINE ---
        # Dòng 18-20: ROI (Region of Interest) cho đèn tín hiệu
        self.traffic_light_roi = None
        # Format: (x, y, w, h)
        # - x, y: Tọa độ góc trên trái của vùng đèn
        # - w: Chiều rộng vùng
        # - h: Chiều cao vùng
        # None = chưa config, cần set qua set_traffic_light_roi()

        # Dòng 22-24: Vạch dừng (stop line)
        self.stop_line_y = None
        # Tọa độ Y của vạch dừng (pixel)
        # Xe vượt qua Y này khi đèn đỏ → vi phạm
        # None = chưa config, cần set qua set_stop_line()

        # --- TRACKING VÀ COOLDOWN ---
        # Dòng 26-27: Set tracking violations
        self.tracked_violations = set()
        # Set chứa các vehicle ID đã vi phạm
        # Tránh detect duplicate cho cùng 1 xe

        # Dòng 37-39: Cooldown dictionary
        self.violation_cooldown = {}
        # Format: {position_key: timestamp}
        # position_key: f"{x_grid}_{y_grid}" (grid 50x50 pixels)
        # timestamp: Thời điểm phát hiện vi phạm
        # Dùng để tránh detect liên tục xe ở cùng vị trí

        self.cooldown_duration = 5.0  # seconds
        # Thời gian cooldown: 5 giây
        # Sau 5 giây mới được detect lại ở vị trí đó

        # --- STATISTICS ---
        # Dòng 29-31: Thống kê
        self.violation_count = 0  # Tổng số vi phạm đã phát hiện
        self.last_light_status = 'unknown'  # Trạng thái đèn cuối cùng

        # --- LƯU ẢNH VI PHẠM ---
        # Dòng 33-35: Thư mục lưu ảnh
        self.violation_images_dir = "./app/static/violation_images"
        # Đường dẫn tương đối từ root project
        # Static files được serve qua /static/violation_images/...

        os.makedirs(self.violation_images_dir, exist_ok=True)
        # Tạo thư mục nếu chưa tồn tại
        # exist_ok=True: Không báo lỗi nếu folder đã tồn tại

        # --- TELEGRAM BOT NOTIFIER ---
        # Khởi tạo Telegram notifier để gửi cảnh báo real-time
        self.telegram_notifier = get_telegram_notifier()
        # Singleton instance, tự động load config từ .env

    # ========================================================================
    # PHẦN 2.2: CONFIG METHODS - CẤU HÌNH ROI VÀ STOP LINE
    # ========================================================================

    # Dòng 41-50: Method set ROI
    def set_traffic_light_roi(self, x: int, y: int, w: int, h: int):
        """
        Thiết lập vùng chứa đèn giao thông (ROI)

        Args:
            x: Tọa độ X của góc trên trái (pixels)
            y: Tọa độ Y của góc trên trái (pixels)
            w: Chiều rộng ROI (pixels)
            h: Chiều cao ROI (pixels)

        VÍ DỤ:
        Đèn tín hiệu ở góc trên trái màn hình
        → set_traffic_light_roi(10, 10, 80, 150)
        → ROI từ (10, 10) đến (90, 160)

        LƯU Ý:
        - ROI phải đủ lớn để chứa toàn bộ đèn
        - Nhưng không quá lớn để tránh nhiễu
        - Đèn tín hiệu thường có 3 đèn xếp dọc
        - → h thường gấp ~2-3 lần w
        """
        # Dòng 49: Lưu ROI
        self.traffic_light_roi = (x, y, w, h)
        # Tuple 4 số: (x, y, width, height)

        # Dòng 50: In thông báo
        print(f"✅ Traffic light ROI set: x={x}, y={y}, w={w}, h={h}")

    # Dòng 52-60: Method set stop line
    def set_stop_line(self, y: int):
        """
        Thiết lập vạch dừng (stop line)

        Args:
            y: Tọa độ Y của vạch dừng (pixels)

        GIẢI THÍCH:
        - Vạch dừng là tọa độ Y mà xe KHÔNG ĐƯỢC vượt qua khi đèn đỏ
        - Thường là vạch kẻ đường trắng trước ngã tư
        - Hoặc vạch zebra crossing

        VÍ DỤ:
        Vạch dừng ở giữa màn hình (frame 720p)
        → set_stop_line(400)
        → Xe có bottom_y > 400 khi đèn đỏ = vi phạm

        CÁCH XÁC ĐỊNH Y:
        1. Mở frame ảnh từ camera
        2. Đo tọa độ Y của vạch dừng (dùng paint/photoshop)
        3. Set giá trị đó
        """
        # Dòng 59: Lưu stop line Y
        self.stop_line_y = y

        # Dòng 60: In thông báo
        print(f"✅ Stop line set at Y={y}")

    # ========================================================================
    # PHẦN 2.3: COLOR DETECTION - NHẬN DIỆN MÀU ĐÈN
    # ========================================================================

    # Dòng 62-135: Method detect màu đèn
    def detect_light_color(self, frame: np.ndarray) -> str:
        """
        Nhận diện màu đèn giao thông sử dụng HSV color space

        Args:
            frame: Frame ảnh từ camera (np.ndarray shape: HxWx3, BGR format)

        Returns:
            'red': Đèn đỏ
            'yellow': Đèn vàng
            'green': Đèn xanh
            'unknown': Không nhận diện được

        ALGORITHM:

        1. Crop ROI từ frame
        2. Convert BGR → HSV
        3. Tạo mask cho từng màu:
           - Đỏ: Hue 0-10° và 160-180° (đỏ nằm 2 đầu spectrum)
           - Vàng: Hue 15-35°
           - Xanh: Hue 40-90°
        4. Đếm số pixels của từng màu
        5. Màu nào có nhiều pixels nhất → return màu đó

        TẠI SAO HSV?
        - Hue (H): Màu sắc thuần túy (0-180°)
        - Saturation (S): Độ bão hòa màu
        - Value (V): Độ sáng
        → Tách rời màu sắc khỏi ánh sáng!

        RGB vs HSV:
        - Ban ngày: Đèn đỏ RGB=(255,0,0) HSV=(0°, 100%, 100%)
        - Ban đêm: Đèn đỏ RGB=(100,0,0) HSV=(0°, 100%, 40%)
        → Hue luôn là 0° (đỏ) bất kể độ sáng!
        """

        # --- BƯỚC 1: KIỂM TRA ROI ĐÃ CONFIG CHƯA ---
        # Dòng 72-73: Check ROI
        if self.traffic_light_roi is None:
            return 'unknown'
        # Nếu chưa config ROI → không thể detect → return unknown

        # --- BƯỚC 2: CROP ROI VÀ CONVERT HSV ---
        try:
            # Dòng 76: Unpack ROI
            x, y, w, h = self.traffic_light_roi
            # x, y: Góc trên trái
            # w, h: Chiều rộng và cao

            # Dòng 78-80: Validate ROI nằm trong frame
            if x < 0 or y < 0 or x + w > frame.shape[1] or y + h > frame.shape[0]:
                return 'unknown'
            # frame.shape: (height, width, channels)
            # frame.shape[1]: width
            # frame.shape[0]: height
            # Nếu ROI vượt ra ngoài frame → invalid → return unknown

            # Dòng 82: Crop ROI
            roi = frame[y:y+h, x:x+w]
            # Slicing NumPy array: [y_start:y_end, x_start:x_end]
            # Lấy vùng hình chữ nhật chứa đèn tín hiệu

            # Dòng 84-85: Convert BGR → HSV
            hsv = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)
            # cvtColor(): Convert color space
            # BGR: Blue-Green-Red (OpenCV default)
            # HSV: Hue-Saturation-Value
            # hsv shape: (h, w, 3) với 3 channels: H, S, V

            # --- BƯỚC 3: ĐỊNH NGHĨA HSV RANGES ---

            # Dòng 87-92: Đỏ (Red) - 2 ranges
            # Lý do 2 ranges: Hue là vòng tròn 0-180°
            # Đỏ nằm ở 2 đầu: 0-10° và 160-180°

            # Range 1: Đỏ sáng (0-10°)
            lower_red1 = np.array([0, 100, 100])
            # [Hue=0°, Saturation≥100, Value≥100]
            upper_red1 = np.array([10, 255, 255])
            # [Hue≤10°, Saturation≤255, Value≤255]

            # Range 2: Đỏ thẫm (160-180°)
            lower_red2 = np.array([160, 100, 100])
            upper_red2 = np.array([180, 255, 255])

            # Dòng 94-96: Vàng (Yellow)
            lower_yellow = np.array([15, 100, 100])
            # Vàng: Hue 15-35° (giữa đỏ và xanh lá)
            upper_yellow = np.array([35, 255, 255])

            # Dòng 98-100: Xanh lá (Green)
            lower_green = np.array([40, 50, 50])
            # Xanh lá: Hue 40-90°
            # Saturation và Value thấp hơn vì đèn xanh thường nhạt hơn
            upper_green = np.array([90, 255, 255])

            # --- BƯỚC 4: TẠO MASKS ---

            # Dòng 102-105: Mask đỏ (combine 2 ranges)
            mask_red1 = cv2.inRange(hsv, lower_red1, upper_red1)
            # inRange(): Tạo binary mask
            # Pixel trong range → 255 (trắng)
            # Pixel ngoài range → 0 (đen)
            mask_red2 = cv2.inRange(hsv, lower_red2, upper_red2)

            mask_red = cv2.bitwise_or(mask_red1, mask_red2)
            # bitwise_or(): Kết hợp 2 masks
            # Pixel trắng ở mask1 HOẶC mask2 → trắng ở mask_red

            # Dòng 107-108: Masks vàng và xanh
            mask_yellow = cv2.inRange(hsv, lower_yellow, upper_yellow)
            mask_green = cv2.inRange(hsv, lower_green, upper_green)

            # --- BƯỚC 5: ĐẾM PIXELS ---

            # Dòng 110-113: Đếm số pixels mỗi màu
            red_pixels = cv2.countNonZero(mask_red)
            # countNonZero(): Đếm số pixels ≠ 0 (pixels trắng)
            yellow_pixels = cv2.countNonZero(mask_yellow)
            green_pixels = cv2.countNonZero(mask_green)

            # --- BƯỚC 6: XÁC ĐỊNH MÀU ---

            # Dòng 115-116: Tìm màu có nhiều pixels nhất
            max_pixels = max(red_pixels, yellow_pixels, green_pixels)

            # Dòng 118-122: Threshold tối thiểu
            min_threshold = 30
            # Cần ít nhất 30 pixels để coi là có đèn
            # Tránh false positive từ nhiễu

            if max_pixels < min_threshold:
                return 'unknown'
            # Không đủ pixels → không có đèn

            # Dòng 124-129: Return màu
            if red_pixels == max_pixels:
                return 'red'
            elif yellow_pixels == max_pixels:
                return 'yellow'
            elif green_pixels == max_pixels:
                return 'green'

            # Dòng 131: Fallback
            return 'unknown'

        # Dòng 133-135: Exception handling
        except Exception as e:
            print(f"❌ Error detecting light color: {e}")
            return 'unknown'

    # ========================================================================
    # PHẦN 2.4: COOLDOWN MECHANISM - TRÁNH DETECT DUPLICATE
    # ========================================================================

    # Dòng 137-142: Check cooldown
    def _is_in_cooldown(self, position_key: str) -> bool:
        """
        Kiểm tra vị trí còn trong cooldown không

        Args:
            position_key: Key định danh vị trí (ví dụ: "3_8")

        Returns:
            True: Còn trong cooldown, không detect
            False: Hết cooldown, có thể detect

        GIẢI THÍCH COOLDOWN:
        - Sau khi detect vi phạm tại vị trí X
        - Lưu timestamp vào violation_cooldown[position_key]
        - Trong 5 giây tiếp theo, không detect lại vị trí đó
        - Tránh detect liên tục cùng 1 xe (30 FPS = 30 detections/giây!)

        VÍ DỤ:
        - T=0s: Detect xe vị trí (150, 420) → lưu cooldown["3_8"] = T0
        - T=1s: Xe vẫn ở (160, 425) → check cooldown → skip
        - T=6s: Xe mới vị trí (170, 430) → hết cooldown → detect lại
        """
        # Dòng 139-141: Check elapsed time
        if position_key in self.violation_cooldown:
            # Tính thời gian đã trôi qua
            elapsed = (datetime.now() - self.violation_cooldown[position_key]).total_seconds()
            # total_seconds(): Convert timedelta → seconds (float)

            return elapsed < self.cooldown_duration
            # Nếu < 5 giây → còn cooldown → return True

        # Dòng 142: Không có trong cooldown
        return False
        # Chưa từng detect vị trí này → không cooldown

    # ========================================================================
    # PHẦN 2.5: VIOLATION CHECKING - KIỂM TRA VI PHẠM
    # ========================================================================

    # Dòng 144-235: Method check violation (CORE LOGIC)
    def check_violation(
        self,
        frame: np.ndarray,  # Frame hiện tại
        detections: List[Dict],  # List xe detected
        light_status: str  # Trạng thái đèn
    ) -> List[Dict]:
        """
        Kiểm tra vi phạm vượt đèn đỏ

        Args:
            frame: Frame ảnh hiện tại (BGR, np.ndarray)
            detections: List các xe đã detect bởi YOLO
                Format: [
                    {
                        'class': 'car',  # Loại xe
                        'bbox': (x1, y1, x2, y2),  # Bounding box
                        'conf': 0.95  # Confidence score
                    },
                    ...
                ]
            light_status: Trạng thái đèn ('red', 'yellow', 'green', 'unknown')

        Returns:
            List các vi phạm detected
            Format: [
                {
                    'camera_name': 'camera_live',
                    'violation_type': 'red_light',
                    'vehicle_type': 'car',
                    'position_x': 150.5,
                    'position_y': 420.0,
                    'traffic_light_status': 'red',
                    'bbox': (x1, y1, x2, y2),
                    'confidence': 0.95,
                    'timestamp': datetime(...),
                    'image_path': 'app/static/violation_images/...'
                },
                ...
            ]

        ALGORITHM:

        1. Loop qua tất cả detections
        2. Với mỗi xe:
           a. Lấy điểm bottom (đáy) của bounding box
           b. Tạo position_key từ (x, y)
           c. Check cooldown → skip nếu còn cooldown
           d. Check: bottom_y > stop_line_y?
           e. Nếu YES + đèn đỏ → VI PHẠM!
           f. Lưu ảnh bằng chứng
           g. Add vào cooldown
           h. Return violation dict

        TẠI SAO DÙNG BOTTOM (ĐÁY) BBOX?
        - Bottom là điểm QUAN TRỌNG nhất
        - Bottom = vị trí bánh xe chạm đất
        - Nếu bottom vượt vạch → xe đã vượt thật
        - Top bbox chỉ là nóc xe, không quan trọng
        """

        # --- BƯỚC 1: KHỞI TẠO ---
        # Dòng 162: List lưu violations
        violations = []

        # Dòng 164-165: Cập nhật trạng thái đèn
        self.last_light_status = light_status

        # --- BƯỚC 2: VALIDATE CONFIG ---
        # Dòng 167-169: Check đã config chưa
        if self.stop_line_y is None or light_status == 'unknown':
            return violations
        # Nếu chưa config stop line HOẶC không biết màu đèn
        # → không thể check vi phạm → return empty list

        # --- BƯỚC 3: CHỈ CHECK KHI ĐÈN ĐỎ ---
        # Dòng 171-175: Check light status
        if light_status not in ['red']:
            # Đèn không đỏ (xanh hoặc vàng)
            # → clear cooldown (vì xe có thể đi qua hợp lệ)
            self.violation_cooldown.clear()
            return violations
        # NOTE: Có thể thêm 'yellow' vào list nếu muốn strict hơn
        # → Vượt đèn vàng cũng coi là vi phạm

        # Dòng 177: Lấy timestamp hiện tại
        current_time = datetime.now()

        # --- BƯỚC 4: LOOP QUA TẤT CẢ DETECTIONS ---
        # Dòng 179: Loop
        for det in detections:
            # Dòng 180-182: Unpack detection
            bbox = det['bbox']  # (x1, y1, x2, y2)
            vehicle_type = det['class']  # 'car', 'motorbike', 'truck', ...
            confidence = det.get('conf', 1.0)  # Confidence (default: 1.0)

            # --- BƯỚC 5: TÍNH BOTTOM CENTER ---
            # Dòng 184-187: Tính điểm bottom center
            # bbox: (x1, y1, x2, y2)
            # - (x1, y1): Góc trên trái
            # - (x2, y2): Góc dưới phải

            bottom_center_x = (bbox[0] + bbox[2]) / 2
            # Center X: Trung điểm của x1 và x2
            # Dùng để xác định xe ở làn nào

            bottom_y = bbox[3]
            # Bottom Y: y2 (tọa độ dưới cùng)
            # Đây là điểm quan trọng nhất!

            # --- BƯỚC 6: TẠO POSITION KEY ---
            # Dòng 189-190: Tạo key cho tracking
            position_key = f"{int(bottom_center_x/50)}_{int(bottom_y/50)}"
            # Chia thành grid 50x50 pixels
            # Ví dụ: (175, 425) → "3_8"
            # Xe trong cùng grid → cùng position_key
            # Tránh detect nhiều lần xe ở gần nhau

            # --- BƯỚC 7: CHECK COOLDOWN ---
            # Dòng 192-194: Skip nếu còn cooldown
            if self._is_in_cooldown(position_key):
                continue
            # continue: Bỏ qua xe này, chuyển sang xe tiếp theo

            # --- BƯỚC 8: CHECK VI PHẠM ---
            # Dòng 196-197: Kiểm tra vượt vạch dừng
            if bottom_y > self.stop_line_y:
                # Bottom của xe > Y của vạch dừng
                # → Xe đã vượt qua vạch!
                # + Đèn đang đỏ (đã check ở trên)
                # → VI PHẠM!

                # --- BƯỚC 9: TẠO VIOLATION DICT ---
                # Dòng 198-209: Build violation object
                violation = {
                    'camera_name': self.camera_name,  # Camera nào detect
                    'violation_type': 'red_light',  # Loại vi phạm
                    'vehicle_type': vehicle_type,  # Loại xe
                    'position_x': float(bottom_center_x),  # Vị trí X
                    'position_y': float(bottom_y),  # Vị trí Y
                    'traffic_light_status': light_status,  # Màu đèn (red)
                    'bbox': bbox,  # Bounding box gốc
                    'confidence': float(confidence),  # Độ tin cậy
                    'timestamp': current_time  # Thời gian vi phạm
                }

                # --- BƯỚC 10: LƯU ẢNH BẰNG CHỨNG ---
                # Dòng 211-213: Tạo filename
                image_filename = f"violation_{self.camera_name}_{current_time.strftime('%Y%m%d_%H%M%S_%f')}.jpg"
                # Format: violation_camera_live_20251110_143025_123456.jpg
                # %f: Microseconds → unique filename

                image_path = os.path.join(self.violation_images_dir, image_filename)
                # Full path: ./app/static/violation_images/violation_...jpg

                # Dòng 215-221: Vẽ annotations và save
                annotated_frame = self._annotate_violation(
                    frame.copy(),  # Copy frame để không modify gốc
                    bbox,  # Bounding box của xe
                    vehicle_type,  # Loại xe
                    light_status  # Màu đèn
                )
                # Method này vẽ:
                # - Bounding box đỏ quanh xe
                # - Text "VIOLATION: CAR"
                # - Vạch dừng màu đỏ
                # - ROI đèn tín hiệu
                # - Timestamp

                # Dòng 224: Lưu ảnh
                cv2.imwrite(image_path, annotated_frame)
                # imwrite(): Lưu np.ndarray → file JPG

                # Dòng 225: Thêm image_path vào violation
                violation['image_path'] = image_path

                # --- BƯỚC 11: GỬI TELEGRAM NOTIFICATION ---
                # Gửi cảnh báo qua Telegram Bot (async, không block)
                try:
                    # Tạo violation data cho Telegram
                    telegram_data = {
                        'timestamp': current_time,
                        'vehicle_type': vehicle_type,
                        'license_plate': 'Không nhận diện được',  # TODO: Tích hợp OCR
                        'camera_name': self.camera_name,
                        'location': 'Hà Nội'  # TODO: Lấy từ config
                    }

                    # Gửi async (trong < 1 giây)
                    asyncio.create_task(
                        self.telegram_notifier.send_violation_alert(
                            annotated_frame,  # Ảnh đã vẽ annotations
                            telegram_data
                        )
                    )
                    print(f"📱 Telegram notification queued for {vehicle_type}")
                except Exception as e:
                    print(f"⚠️ Telegram notification failed: {e}")
                    # Không throw error, tiếp tục xử lý vi phạm bình thường

                # --- BƯỚC 12: UPDATE STATISTICS ---
                # Dòng 227-228: Thêm vào list và tăng counter
                violations.append(violation)
                self.violation_count += 1

                # --- BƯỚC 13: ADD COOLDOWN ---
                # Dòng 230-231: Lưu cooldown
                self.violation_cooldown[position_key] = current_time
                # Vị trí này không detect lại trong 5 giây

                # --- BƯỚC 14: LOG ---
                # Dòng 233: In ra console
                print(f"🚨 VIOLATION DETECTED: {vehicle_type} ran red light at Y={bottom_y:.0f}")
                # 🚨: Emoji cảnh báo để dễ nhận biết trong logs

        # --- BƯỚC 14: RETURN ---
        # Dòng 235: Return list violations
        return violations
        # List có thể empty (không vi phạm) hoặc có 1-N violations

    # ========================================================================
    # PHẦN 2.6: ANNOTATION - VẼ BẰNG CHỨNG VI PHẠM
    # ========================================================================

    # Dòng 237-308: Method annotate violation
    def _annotate_violation(
        self,
        frame: np.ndarray,  # Frame để vẽ
        bbox: Tuple[float, float, float, float],  # Bounding box xe
        vehicle_type: str,  # Loại xe
        light_status: str  # Màu đèn
    ) -> np.ndarray:
        """
        Vẽ annotations lên frame vi phạm

        Vẽ các thành phần:
        1. Bounding box đỏ quanh xe vi phạm
        2. Text "VIOLATION: CAR" phía trên xe
        3. Vạch dừng (stop line) màu đỏ
        4. Text "STOP LINE - DO NOT CROSS"
        5. ROI đèn tín hiệu với màu đỏ
        6. Text "LIGHT: RED"
        7. Timestamp ở góc dưới

        Args:
            frame: Frame gốc (đã copy)
            bbox: (x1, y1, x2, y2)
            vehicle_type: 'car', 'motorbike', ...
            light_status: 'red', 'yellow', 'green'

        Returns:
            Frame đã vẽ annotations
        """

        # Dòng 245: Convert bbox sang int
        x1, y1, x2, y2 = map(int, bbox)
        # map(int, ...): Convert tất cả floats → ints
        # OpenCV cần tọa độ integer

        # --- VẼ BOUNDING BOX XE ---
        # Dòng 247-248: Vẽ hình chữ nhật đỏ
        cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 255), 3)
        # rectangle(img, pt1, pt2, color, thickness)
        # - pt1: (x1, y1) góc trên trái
        # - pt2: (x2, y2) góc dưới phải
        # - color: (0, 0, 255) = Red (BGR format!)
        # - thickness: 3 pixels

        # --- VẼ TEXT VIOLATION ---
        # Dòng 250-260: Text "VIOLATION"
        violation_text = f"VIOLATION: {vehicle_type.upper()}"
        # upper(): Chữ hoa cho nổi bật

        cv2.putText(
            frame,  # Image
            violation_text,  # Text
            (x1, max(y1 - 10, 30)),  # Position (x, y)
            # x: Căn trái với bbox
            # y: Trên bbox 10px, nhưng tối thiểu y=30 (không bị cắt)
            cv2.FONT_HERSHEY_SIMPLEX,  # Font
            0.8,  # Font scale
            (0, 0, 255),  # Color: Red
            2  # Thickness
        )

        # --- VẼ VẠCH DỪNG ---
        # Dòng 262-269: Vẽ line ngang
        cv2.line(
            frame,
            (0, int(self.stop_line_y)),  # Start point (x=0)
            (frame.shape[1], int(self.stop_line_y)),  # End point (x=width)
            (0, 0, 255),  # Red
            3  # Thickness 3px
        )
        # line(): Vẽ đường thẳng từ trái sang phải

        # Dòng 271-280: Text "STOP LINE"
        cv2.putText(
            frame,
            "STOP LINE - DO NOT CROSS",
            (10, int(self.stop_line_y) - 10),  # Trên vạch 10px
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            (0, 0, 255),
            2
        )

        # --- VẼ ROI ĐÈN TÍN HIỆU ---
        # Dòng 282-294: Vẽ rectangle ROI
        if self.traffic_light_roi:
            x, y, w, h = self.traffic_light_roi

            # Rectangle quanh ROI
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 0, 255), 2)

            # Text trạng thái đèn
            cv2.putText(
                frame,
                f"LIGHT: {light_status.upper()}",  # "LIGHT: RED"
                (x, max(y - 10, 20)),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7,
                (0, 0, 255),
                2
            )

        # --- VẼ TIMESTAMP ---
        # Dòng 296-306: Timestamp góc dưới trái
        timestamp_text = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        # Format: 2025-11-10 14:30:25

        cv2.putText(
            frame,
            timestamp_text,
            (10, frame.shape[0] - 10),  # Góc dưới trái (x=10, y=height-10)
            cv2.FONT_HERSHEY_SIMPLEX,
            0.6,
            (0, 0, 255),
            2
        )

        # Dòng 308: Return frame đã vẽ
        return frame

    # ========================================================================
    # PHẦN 2.7: MONITORING OVERLAY - VẼ OVERLAY GIÁM SÁT
    # ========================================================================

    # Dòng 310-401: Method draw monitoring overlay
    def draw_monitoring_overlay(
        self,
        frame: np.ndarray,
        light_status: str,
        show_roi: bool = True
    ) -> np.ndarray:
        """
        Vẽ overlay giám sát lên frame (cho live stream)

        Khác với _annotate_violation():
        - Này dùng cho LIVE MONITORING (mọi frame)
        - _annotate_violation dùng cho ẢNH BẰNG CHỨNG (chỉ khi vi phạm)

        Vẽ:
        1. ROI đèn tín hiệu với màu theo trạng thái
        2. Text "Light: RED/YELLOW/GREEN"
        3. Vạch dừng (màu thay đổi theo đèn)
        4. Text "STOP LINE"
        5. Statistics "Violations: 5"
        6. Status "Monitoring: ACTIVE"

        Args:
            frame: Frame gốc
            light_status: Trạng thái đèn
            show_roi: Có hiển thị ROI không (default: True)

        Returns:
            Frame đã vẽ overlay
        """

        # Dòng 327: Copy frame
        annotated = frame.copy()
        # Không modify frame gốc

        # --- VẼ ROI ĐÈN TÍN HIỆU ---
        # Dòng 329-351: ROI với màu dynamic
        if show_roi and self.traffic_light_roi:
            x, y, w, h = self.traffic_light_roi

            # Dòng 333-340: Chọn màu theo trạng thái
            color = (128, 128, 128)  # Gray mặc định (unknown)
            if light_status == 'red':
                color = (0, 0, 255)  # Red
            elif light_status == 'yellow':
                color = (0, 255, 255)  # Yellow (BGR!)
            elif light_status == 'green':
                color = (0, 255, 0)  # Green

            # Dòng 342: Vẽ rectangle
            cv2.rectangle(annotated, (x, y), (x+w, y+h), color, 2)

            # Dòng 343-351: Text trạng thái
            cv2.putText(
                annotated,
                f"Light: {light_status.upper()}",
                (x, max(y - 10, 20)),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.6,
                color,  # Màu theo trạng thái
                2
            )

        # --- VẼ VẠCH DỪNG ---
        # Dòng 353-374: Stop line với màu dynamic
        if self.stop_line_y:
            # Dòng 355-357: Chọn màu
            line_color = (255, 255, 0)  # Cyan/Yellow mặc định
            if light_status == 'red':
                line_color = (0, 0, 255)  # Red khi đèn đỏ (cảnh báo!)

            # Dòng 359-365: Vẽ line
            cv2.line(
                annotated,
                (0, int(self.stop_line_y)),
                (frame.shape[1], int(self.stop_line_y)),
                line_color,
                2  # Thickness 2px (mỏng hơn violation)
            )

            # Dòng 366-374: Text "STOP LINE"
            cv2.putText(
                annotated,
                "STOP LINE",
                (10, int(self.stop_line_y) - 10),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.6,
                line_color,
                2
            )

        # --- VẼ STATISTICS ---
        # Dòng 376-386: Số vi phạm
        stats_text = f"Violations: {self.violation_count}"
        cv2.putText(
            annotated,
            stats_text,
            (10, 30),  # Góc trên trái
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            (0, 0, 255),  # Red
            2
        )

        # --- VẼ STATUS ---
        # Dòng 388-399: Monitoring status
        status_text = "Monitoring: ACTIVE" if light_status != 'unknown' else "Monitoring: INACTIVE"
        status_color = (0, 255, 0) if light_status != 'unknown' else (128, 128, 128)
        # Green: Active, Gray: Inactive

        cv2.putText(
            annotated,
            status_text,
            (10, 60),  # Dưới statistics
            cv2.FONT_HERSHEY_SIMPLEX,
            0.6,
            status_color,
            2
        )

        # Dòng 401: Return
        return annotated

    # ========================================================================
    # PHẦN 2.8: UTILITIES - THỐNG KÊ VÀ RESET
    # ========================================================================

    # Dòng 403-410: Method get statistics
    def get_statistics(self) -> Dict:
        """
        Lấy thống kê vi phạm

        Returns:
            Dict chứa:
            - camera_name: Tên camera
            - total_violations: Tổng số vi phạm
            - current_light_status: Trạng thái đèn hiện tại
            - is_monitoring: Đang giám sát không
        """
        return {
            'camera_name': self.camera_name,
            'total_violations': self.violation_count,
            'current_light_status': self.last_light_status,
            'is_monitoring': self.stop_line_y is not None and self.traffic_light_roi is not None
            # is_monitoring=True nếu đã config cả ROI và stop line
        }

    # Dòng 412-417: Method reset statistics
    def reset_statistics(self):
        """
        Reset tất cả statistics về 0

        Dùng khi:
        - Bắt đầu phiên giám sát mới
        - Clear data cũ
        - Testing
        """
        # Dòng 414-416: Reset counters và sets
        self.violation_count = 0
        self.tracked_violations.clear()
        self.violation_cooldown.clear()

        # Dòng 417: Log
        print(f"✅ Statistics reset for camera {self.camera_name}")


# ============================================================================
# TỔNG KẾT: LUỒNG HOẠT ĐỘNG REDLIGHTDETECTOR
# ============================================================================
"""
===== 1. SETUP (Chạy 1 lần) =====

1. Khởi tạo detector:
   detector = RedLightDetector("camera_live")

2. Config ROI và stop line:
   detector.set_traffic_light_roi(10, 10, 80, 150)
   detector.set_stop_line(400)

===== 2. DETECTION LOOP (Mỗi frame) =====

Loop liên tục trong RTSPDetectionStream:

for frame in video_stream:
    # 1. Detect màu đèn
    light_status = detector.detect_light_color(frame)

    # 2. Detect vehicles (YOLO)
    detections = yolo_model.detect(frame)
    # detections: [{'class': 'car', 'bbox': (x1,y1,x2,y2), 'conf': 0.95}, ...]

    # 3. Check violations
    violations = detector.check_violation(frame, detections, light_status)

    # 4. Nếu có vi phạm → lưu vào database
    if violations:
        for violation in violations:
            save_to_database(violation)

    # 5. Vẽ overlay cho live stream
    overlay_frame = detector.draw_monitoring_overlay(frame, light_status)

    # 6. Stream overlay_frame về frontend
    send_to_frontend(overlay_frame)

===== 3. COLOR DETECTION ALGORITHM =====

Frame → Crop ROI → BGR→HSV → Create Masks → Count Pixels → Determine Color

Ví dụ:
- ROI: 80x150 pixels
- Đèn đỏ sáng chiếm 500 pixels
- HSV range [0-10, 100-255, 100-255]
- mask_red có 500 white pixels
- mask_yellow có 50 pixels
- mask_green có 30 pixels
→ max_pixels = 500 (red) → return 'red'

===== 4. VIOLATION CHECKING ALGORITHM =====

For each vehicle:
    bottom_y = bbox[3]  # Đáy bbox

    if bottom_y > stop_line_y AND light_status == 'red':
        # VI PHẠM!
        1. Tạo position_key
        2. Check cooldown → skip nếu còn
        3. Annotate frame
        4. Save image
        5. Return violation dict
        6. Add cooldown

===== 5. COORDINATE SYSTEM =====

OpenCV coordinate system:
- Origin (0, 0) ở GÓC TRÊN TRÁI
- X tăng sang PHẢI
- Y tăng XUỐNG DƯỚI

Ví dụ frame 1280x720:
- Góc trên trái: (0, 0)
- Góc trên phải: (1280, 0)
- Góc dưới trái: (0, 720)
- Góc dưới phải: (1280, 720)

Stop line Y=400:
- Vạch ngang ở giữa màn hình
- Xe có bottom_y > 400 → vượt vạch

===== 6. HSV COLOR SPACE =====

Tại sao HSV tốt hơn RGB?

RGB Problem:
- Đèn đỏ ban ngày: (255, 0, 0)
- Đèn đỏ ban đêm: (100, 0, 0)
→ Khác nhau nhiều! Khó set threshold

HSV Solution:
- Đèn đỏ ban ngày: Hue=0°, Saturation=100%, Value=100%
- Đèn đỏ ban đêm: Hue=0°, Saturation=100%, Value=40%
→ Hue luôn là 0° (đỏ)! Dễ detect

HSV Range cho đèn:
- Đỏ: Hue 0-10° và 160-180° (2 đầu vòng tròn)
- Vàng: Hue 15-35°
- Xanh lá: Hue 40-90°

===== 7. COOLDOWN MECHANISM =====

Tại sao cần cooldown?

Không có cooldown:
- Video 30 FPS
- Xe đứng yên vi phạm 1 giây
- → 30 detections cho cùng 1 xe!
- Database bị spam

Có cooldown:
- Detect xe lần 1 → lưu cooldown
- 5 giây sau mới detect lại
- → 1 xe chỉ tạo 1 violation record

Position Key:
- Chia màn hình thành grid 50x50 pixels
- Xe ở (175, 425) → key "3_8"
- Xe ở (185, 435) → key "3_8" (cùng grid)
→ Cooldown áp dụng cho cả vùng, không chỉ 1 pixel

===== 8. BOUNDING BOX =====

YOLO detect xe → trả về bbox (x1, y1, x2, y2):
- (x1, y1): Góc trên trái
- (x2, y2): Góc dưới phải

Bottom center:
- X: (x1 + x2) / 2  → trung điểm ngang
- Y: y2  → đáy bbox (quan trọng nhất!)

Tại sao dùng bottom?
- Bottom = vị trí bánh xe
- Bánh xe vượt vạch = xe vượt vạch
- Top bbox chỉ là nóc xe, không liên quan

===== 9. IMAGE ANNOTATION =====

Khi có vi phạm:

1. Copy frame (không modify gốc)
2. Vẽ bbox đỏ quanh xe
3. Vẽ text "VIOLATION: CAR"
4. Vẽ vạch dừng màu đỏ
5. Vẽ ROI đèn tín hiệu
6. Vẽ timestamp
7. Save → ./app/static/violation_images/violation_...jpg
8. Frontend fetch: http://localhost:8000/static/violation_images/...jpg

===== 10. INTEGRATION VỚI HỆ THỐNG =====

RedLightDetector được dùng trong:

1. RTSPDetectionStream (api_rtsp.py):
   - Stream nhận frames từ RTSP camera
   - Gọi detector.detect_light_color()
   - Gọi detector.check_violation()
   - Nếu có violation → lưu database

2. Database (TrafficViolation model):
   - Violation dict → TrafficViolation object
   - Lưu vào SQLite
   - Frontend query để hiển thị

3. Frontend:
   - GET /api/v1/violations/list → danh sách vi phạm
   - Hiển thị ảnh từ violation.image_path
   - Charts, statistics, filters

===== 11. PERFORMANCE OPTIMIZATION =====

Tối ưu:
1. Cooldown → giảm số lần detect từ 30/s → ~1/5s
2. Position grid → nhóm các xe gần nhau
3. ROI crop → chỉ analyze vùng nhỏ thay vì full frame
4. HSV inRange → rất nhanh (OpenCV C++ backend)
5. countNonZero → O(n) linear time, rất nhanh

Bottleneck:
- cv2.imwrite(): I/O disk (chậm)
- Solution: Có thể save async hoặc queue

===== 12. TESTING TIPS =====

Test từng bước:

1. Test ROI:
   frame = cv2.imread('test.jpg')
   roi = frame[y:y+h, x:x+w]
   cv2.imshow('ROI', roi)
   → Đảm bảo ROI chứa đúng đèn

2. Test màu:
   status = detector.detect_light_color(frame)
   print(status)  # Should be 'red'/'yellow'/'green'

3. Test stop line:
   # Vẽ line lên frame
   cv2.line(frame, (0, stop_y), (w, stop_y), (0,255,0), 2)
   → Đảm bảo line ở đúng vị trí vạch dừng

4. Test full pipeline:
   violations = detector.check_violation(frame, detections, 'red')
   → Check violations có đúng không

===== 13. COMMON ISSUES =====

Issue 1: Không detect được màu
- Check: ROI có đúng không? (dùng cv2.imshow)
- Check: HSV ranges có phù hợp với camera không?
- Solution: Tune HSV ranges bằng trackbar

Issue 2: False positives (detect nhầm)
- Nguyên nhân: Stop line Y sai, hoặc bottom_y calculation sai
- Solution: Vẽ line lên frame để kiểm tra

Issue 3: Detect nhiều lần cùng 1 xe
- Nguyên nhân: Cooldown quá ngắn hoặc grid quá nhỏ
- Solution: Tăng cooldown_duration hoặc grid size

Issue 4: Không lưu được ảnh
- Nguyên nhân: Folder không tồn tại hoặc permission denied
- Solution: Check os.makedirs và file permissions

===== 14. FUTURE IMPROVEMENTS =====

Có thể cải thiện:

1. ML-based color detection:
   - Train CNN để detect màu đèn
   - Chính xác hơn HSV threshold

2. Multi-lane tracking:
   - Track từng làn xe riêng
   - Detect vượt làn

3. Speed detection:
   - Tính vận tốc từ consecutive frames
   - Phát hiện vượt tốc độ

4. License plate recognition:
   - OCR biển số xe
   - Tự động tạo biên bản vi phạm

5. Real-time alerts:
   - WebSocket push notification
   - Email/SMS khi có vi phạm

===== 15. SECURITY & PRIVACY =====

Lưu ý:
- Ảnh vi phạm chứa hình ảnh người
- Cần tuân thủ luật bảo vệ dữ liệu cá nhân
- Có policy xóa ảnh sau X ngày
- Encrypt ảnh khi lưu (optional)
- Access control cho endpoints

END OF DOCUMENTATION
"""
