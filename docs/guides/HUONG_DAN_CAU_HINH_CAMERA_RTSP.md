# 📹 HƯỚNG DẪN CÀI ĐẶT CAMERA RTSP REAL-TIME

**Ngày:** 2025-12-03
**Camera:** IP Camera tại Quảng Nam
**URL:** `rtsp://iocqnm:Quangnam$ioc2020@113.174.246.181:554/h264/ch1/main/av_stream`

---

## ✅ CÁC THAY ĐỔI ĐÃ THỰC HIỆN

### 1. Cấu hình file .env

**File:** `Backend/.env`

```env
# RTSP Camera Configuration
ENABLE_RTSP=True
RTSP_URL=rtsp://iocqnm:Quangnam$ioc2020@113.174.246.181:554/h264/ch1/main/av_stream
```

**Thay đổi:**
- ✅ `ENABLE_RTSP=True` (từ False → True)
- ✅ `RTSP_URL` đã update với URL camera thật

---

### 2. Cập nhật api_rtsp.py để dùng config từ .env

**File:** [Backend/app/api/v1/api_rtsp.py](Backend/app/api/v1/api_rtsp.py:17-30)

**Trước:**
```python
# Hardcoded URL
rtsp_url = "rtsp://iocqnm:Quangnam$ioc2020@113.174.246.181:554/h264/ch1/main/av_stream"
```

**Sau:**
```python
# Get RTSP URL from config
from app.core.config import settings

if not settings.ENABLE_RTSP or not settings.RTSP_URL:
    print("⚠️ RTSP not enabled or URL not configured")
    return

rtsp_url = settings.RTSP_URL
```

**Lợi ích:**
- ✅ Dễ thay đổi URL mà không cần sửa code
- ✅ Có thể bật/tắt RTSP bằng 1 flag
- ✅ Tập trung config ở 1 nơi (.env)

---

## 🚀 CÁCH KHỞI ĐỘNG HỆ THỐNG

### Bước 1: Kiểm tra kết nối camera

Test camera có hoạt động không bằng VLC hoặc ffplay:

```bash
# Dùng VLC
vlc rtsp://iocqnm:Quangnam$ioc2020@113.174.246.181:554/h264/ch1/main/av_stream

# Hoặc dùng ffplay (nếu có FFmpeg)
ffplay rtsp://iocqnm:Quangnam$ioc2020@113.174.246.181:554/h264/ch1/main/av_stream
```

**Nếu thấy video:** ✅ Camera OK, tiếp tục bước 2
**Nếu không thấy gì:** ❌ Kiểm tra:
- IP camera có online không?
- Username/password đúng chưa?
- Port 554 có bị firewall block không?

---

### Bước 2: Restart Backend

```bash
cd Backend

# Kill process cũ (nếu có)
# Windows: Tìm và tắt tiến trình python trong Task Manager
# Linux/Mac: pkill -f uvicorn

# Chạy lại backend
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

**Xem logs để kiểm tra:**

```
🔄 Connecting to RTSP Camera: rtsp://iocqnm:Quangnam$ioc2020@113.174.246.181:554/h264/ch1/main/av_stream...
🚀 GPU detected: NVIDIA GeForce RTX ...
Loading YOLO model from ./app/ai_models/model N/original model/best.pt...
✅ YOLO model loaded successfully on CUDA:0
✅ RTSP camera connected successfully
✅ RTSP camera connected
🎬 Starting detection loop for camera_live
📊 camera_live: Cars=3, Motors=12, Total=15
```

**Nếu thấy:**
- ✅ `RTSP camera connected` → Thành công!
- ✅ `Starting detection loop` → Detection đang chạy
- ✅ `Cars=..., Motors=...` → Đang detect xe real-time

**Nếu thấy lỗi:**
- ❌ `Failed to open RTSP stream` → Kiểm tra URL
- ❌ `Camera disconnected, attempting reconnect` → Camera mất kết nối
- ❌ `Error connecting to RTSP` → Xem chi tiết lỗi

---

### Bước 3: Kiểm tra API

#### 3.1. Xem danh sách streams

```bash
curl http://localhost:8000/api/v1/rtsp/streams
```

**Response:**
```json
{
  "detection_streams": ["camera_live"],
  "raw_streams": [],
  "total_count": 1
}
```

---

#### 3.2. Lấy frame hiện tại (ảnh JPEG)

```bash
# Mở trong browser
http://localhost:8000/api/v1/rtsp/frame/camera_live
```

**Kết quả:** Ảnh JPEG real-time với bounding boxes của YOLO

---

#### 3.3. Xem detection stats

```bash
curl http://localhost:8000/api/v1/rtsp/detections/camera_live
```

**Response:**
```json
{
  "count_car": 5,
  "count_motor": 18,
  "speed_car": 0.0,
  "speed_motor": 0.0,
  "total_vehicles": 23,
  "violations": []
}
```

---

### Bước 4: Kiểm tra WebSocket stream (Frontend)

Nếu Frontend đang chạy, mở:

```
http://localhost:3000
```

Và xem camera "camera_live" có stream video không.

---

## 🔧 CẤU HÌNH PHÁT HIỆN VI PHẠM ĐÈN ĐỎ

Sau khi camera đã chạy, cần cấu hình ROI và stop line cho detection vi phạm đèn đỏ.

### Bước 1: Tìm ROI tự động (Auto-calibrate)

**LƯU Ý:** Đảm bảo đèn đỏ ĐANG BẬT khi chạy lệnh này!

```bash
curl -X POST http://localhost:8000/api/v1/debug/calibrate-roi/camera_live
```

**Response:**
```json
{
  "success": true,
  "message": "Tìm thấy 3 vùng đỏ phù hợp",
  "recommended_roi": {
    "x": 1580,
    "y": 160,
    "w": 30,
    "h": 35
  },
  "all_candidates": [...]
}
```

Copy ROI từ `recommended_roi`.

---

### Bước 2: Xác định vị trí vạch dừng (stop_line_y)

Mở ảnh từ camera:
```
http://localhost:8000/api/v1/rtsp/frame/camera_live
```

Dùng Paint/Photoshop để đo tọa độ Y của vạch dừng.

**Ví dụ:** Nếu vạch dừng nằm ở pixel Y=544 thì:
```
stop_line_y = 544
```

---

### Bước 3: Apply cấu hình vi phạm đèn đỏ

```bash
curl -X POST http://localhost:8000/api/v1/violations/config \
  -H "Content-Type: application/json" \
  -d '{
    "camera_name": "camera_live",
    "traffic_light_roi": {
      "x": 1580,
      "y": 160,
      "w": 30,
      "h": 35
    },
    "stop_line_y": 544,
    "enable": true
  }'
```

**Response:**
```json
{
  "message": "Red light detection configured for camera_live",
  "config": {
    "traffic_light_roi": {"x": 1580, "y": 160, "w": 30, "h": 35},
    "stop_line_y": 544,
    "enabled": true
  }
}
```

---

### Bước 4: Verify detection

Kiểm tra debug endpoint:

```bash
curl http://localhost:8000/api/v1/debug/light-detection/camera_live
```

**Response (nếu OK):**
```json
{
  "detected_color": "red",
  "color_pixels": {
    "red": 850,
    "yellow": 0,
    "green": 0
  },
  "analysis": {
    "is_red_detected": true,
    "confidence": 85.2
  }
}
```

**Hoặc xem visualization:**
```
http://localhost:8000/api/v1/debug/light-detection/camera_live?show_masks=true
```

---

## 📊 DATA FLOW (Real-time Camera vs Test Videos)

### ❌ Trước (Test Videos)

```
AnalyzeOnRoadForMultiProcessing
  ↓
  Đọc video từ ./app/video_test/
  ↓
  YOLO detection
  ↓
  Lưu vào database (TrafficRecord)
  ↓
  Telegram report → Lấy từ database
```

**Vấn đề:** Data là test videos có sẵn, không phải real-time.

---

### ✅ Sau (RTSP Camera)

```
RTSPDetectionService (camera_live)
  ↓
  Đọc stream từ RTSP URL (REAL-TIME)
  ↓
  YOLO detection + Red Light Detection
  ↓
  Lưu vào rtsp_detection_manager.shared_data
  ↓
  Telegram report → Lấy từ Analyzer.shared_data (REAL-TIME)
```

**Lợi ích:**
- ✅ Data real-time từ camera thật
- ✅ Báo cáo chính xác theo thời gian thực
- ✅ Vi phạm đèn đỏ được detect ngay lập tức

---

## 🔍 DEBUGGING

### Vấn đề 1: Camera không kết nối được

**Triệu chứng:**
```
❌ Failed to open RTSP stream
```

**Giải pháp:**
1. Kiểm tra camera có online không (ping IP)
   ```bash
   ping 113.174.246.181
   ```

2. Test stream bằng VLC
   ```bash
   vlc rtsp://iocqnm:Quangnam$ioc2020@113.174.246.181:554/h264/ch1/main/av_stream
   ```

3. Kiểm tra firewall có block port 554 không

4. Kiểm tra username/password có đúng không

---

### Vấn đề 2: Camera connect nhưng không có frame

**Triệu chứng:**
```
⚠️ Camera disconnected, attempting reconnect (attempt 1)...
```

**Giải pháp:**
1. Kiểm tra bandwidth - RTSP stream cần băng thông ổn định

2. Giảm resolution trong code (nếu cần):
   ```python
   # Backend/app/services/rtsp_detection_service.py:69
   self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)  # Giảm từ 1280
   self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 360)  # Giảm từ 720
   ```

3. Tăng buffer size:
   ```python
   # Backend/app/services/rtsp_detection_service.py:66
   self.cap.set(cv2.CAP_PROP_BUFFERSIZE, 3)  # Tăng từ 1
   ```

---

### Vấn đề 3: Detection chậm / lag

**Triệu chứng:**
- Frame rate thấp
- Lag nhiều giây

**Giải pháp:**
1. Kiểm tra GPU có đang dùng không:
   ```
   # Trong logs phải thấy:
   🚀 GPU detected: NVIDIA ...
   ✅ YOLO model loaded successfully on CUDA:0
   ```

2. Giảm FPS nếu cần:
   ```python
   # Backend/app/api/v1/api_rtsp.py:82
   await asyncio.sleep(0.05)  # Tăng từ 0.01 → ~20 FPS
   ```

3. Giảm JPEG quality khi encode:
   ```python
   # Backend/app/services/rtsp_detection_service.py:251
   encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 70]  # Giảm từ 85
   ```

---

### Vấn đề 4: Không detect được đèn đỏ

**Xem chi tiết tại:** [HUONG_DAN_DEBUG_LIGHT_DETECTION.md](./HUONG_DAN_DEBUG_LIGHT_DETECTION.md)

**Quick fix:**
1. Chạy auto-calibrate ROI:
   ```bash
   POST /api/v1/debug/calibrate-roi/camera_live
   ```

2. Apply ROI mới với `/api/v1/violations/config`

3. Verify với:
   ```bash
   GET /api/v1/debug/light-detection/camera_live?show_masks=true
   ```

---

## 📝 CHECKLIST HOÀN TẤT

- [x] Cập nhật .env với ENABLE_RTSP=True
- [x] Cập nhật .env với RTSP_URL camera thật
- [x] Cập nhật api_rtsp.py để dùng config từ .env
- [ ] Test camera stream bằng VLC/ffplay
- [ ] Restart Backend
- [ ] Xem logs → check "RTSP camera connected"
- [ ] Test API: GET /api/v1/rtsp/streams
- [ ] Test API: GET /api/v1/rtsp/frame/camera_live
- [ ] Test API: GET /api/v1/rtsp/detections/camera_live
- [ ] Cấu hình red light detection:
  - [ ] POST /api/v1/debug/calibrate-roi/camera_live
  - [ ] POST /api/v1/violations/config (với ROI + stop_line_y)
  - [ ] GET /api/v1/debug/light-detection/camera_live
- [ ] Test violation detection: xe vượt đèn đỏ → có báo vi phạm không?
- [ ] Test Telegram report: POST /api/v1/violations/send-report?period=today

---

## 🎯 SO SÁNH DATA SOURCES

| Aspect | Test Videos (Cũ) | RTSP Camera (Mới) |
|--------|------------------|-------------------|
| **Data source** | 5 videos có sẵn | Camera real-time |
| **Update frequency** | Không real-time | Real-time (30 FPS) |
| **Locations** | Văn Quán, Văn Phú, Nguyễn Trãi, Ngã Tư Sở, Đường Láng | 1 camera IP tại Quảng Nam |
| **Violations** | Dựa vào video test | Dựa vào camera thật |
| **Telegram report** | Tổng hợp từ 5 videos | Data từ 1 camera real-time |
| **Use case** | Demo, testing | Production (thực chiến) |

---

## 💡 LƯU Ý QUAN TRỌNG

1. **Camera phải online 24/7** - Nếu camera offline, hệ thống sẽ tự động reconnect sau 3s

2. **ROI phải được cấu hình lại** - Mỗi camera khác nhau cần ROI khác nhau cho đèn tín hiệu

3. **Stop line cũng cần điều chỉnh** - Phụ thuộc vào góc nhìn camera

4. **Bandwidth quan trọng** - RTSP stream H.264 1280x720 cần ~2-5 Mbps

5. **GPU tăng tốc độ rất nhiều** - Nếu không có GPU, detection sẽ chậm hơn 5-10 lần

6. **Telegram report giờ là real-time** - Dữ liệu lấy từ `state.analyzer.shared_data` của camera_live

---

## 📞 HỖ TRỢ

Nếu gặp vấn đề:

1. **Check logs Backend** - Xem chi tiết lỗi trong console
2. **Test camera riêng** - Dùng VLC/ffplay để loại trừ vấn đề camera
3. **Xem debug endpoints** - Dùng các API debug để trace vấn đề
4. **Check documentation:**
   - [FIX_TELEGRAM_REPORT.md](./FIX_TELEGRAM_REPORT.md)
   - [FIX_LIGHT_DETECTION_SUMMARY.md](./FIX_LIGHT_DETECTION_SUMMARY.md)
   - [HUONG_DAN_DEBUG_LIGHT_DETECTION.md](./HUONG_DAN_DEBUG_LIGHT_DETECTION.md)

---

**🎉 Hoàn tất! Hệ thống giờ sử dụng camera RTSP real-time!**

**Next steps:**
1. Restart Backend
2. Test camera connection
3. Cấu hình red light detection (ROI + stop line)
4. Test violations
5. Gửi Telegram report thử nghiệm
