# 🔧 HƯỚNG DẪN DEBUG & FIX LIGHT DETECTION

**Vấn đề:** Hệ thống nhận diện màu đèn tín hiệu SAI - đang đèn đỏ mà không báo vi phạm

**Nguyên nhân có thể:**
1. ❌ ROI (Region of Interest) không đúng vị trí
2. ❌ HSV color ranges không phù hợp với camera
3. ❌ Lighting conditions khác với mong đợi

**Giải pháp:** Dùng các DEBUG endpoints để tìm và fix vấn đề

---

## 🎯 CÁC BƯỚC DEBUG (QUAN TRỌNG!)

### **Bước 1: Restart Backend**
```bash
cd Backend
python -m uvicorn app.main:app --reload
```

Đảm bảo backend đang chạy OK.

---

### **Bước 2: Kiểm tra Detection hiện tại**

#### **API 1: Check detection stats (JSON)**
```bash
GET http://localhost:8000/api/v1/debug/light-detection/camera_live
```

**Response:**
```json
{
  "camera_name": "camera_live",
  "detected_color": "unknown",
  "roi": {
    "x": 1570,
    "y": 154,
    "width": 43,
    "height": 73
  },
  "color_pixels": {
    "red": 0,
    "yellow": 0,
    "green": 0
  },
  "hsv_averages": {
    "hue": 120.5,
    "saturation": 80.3,
    "value": 150.2
  },
  "analysis": {
    "is_red_detected": false,
    "is_yellow_detected": false,
    "is_green_detected": false,
    "confidence": 0
  },
  "suggestions": [
    "❌ ROI có thể SAI - không detect đủ pixels",
    "💡 Hãy kiểm tra lại vị trí ROI (x, y, w, h)"
  ]
}
```

**PHÂN TÍCH:**
- `color_pixels.red = 0` → Không detect được đỏ → ROI SAI!
- `detected_color = "unknown"` → Không nhận diện được
- Suggestions cho biết vấn đề và cách fix

---

#### **API 2: Xem visualization (IMAGE)**
```bash
GET http://localhost:8000/api/v1/debug/light-detection/camera_live?show_masks=true
```

**Response:** Ảnh JPG với 4 panels:
```
┌──────────┬──────────┬──────────┬──────────┐
│ Original │   Red    │  Yellow  │  Green   │
│   ROI    │   Mask   │   Mask   │   Mask   │
│          │  (0 px)  │  (0 px)  │  (0 px)  │
└──────────┴──────────┴──────────┴──────────┘
        DETECTED: UNKNOWN
```

**NHÌN VÀO ẢNH NÀY BẠN SẼ THẤY:**
- Panel 1: Vùng ROI gốc (có chứa đèn không?)
- Panel 2: Mask đỏ (vùng đỏ được detect)
- Panel 3: Mask vàng
- Panel 4: Mask xanh

**NẾU ROI SAI:**
- Panel 1 sẽ không chứa đèn tín hiệu
- Tất cả masks sẽ đen (0 pixels)

---

### **Bước 3: Tự động tìm ROI đúng**

#### **API 3: Auto-calibrate ROI**
```bash
POST http://localhost:8000/api/v1/debug/calibrate-roi/camera_live
```

**LƯU Ý:** Đảm bảo **đèn đỏ ĐANG BẬT** khi chạy API này!

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
  "all_candidates": [
    {
      "rank": 1,
      "roi": {"x": 1580, "y": 160, "w": 30, "h": 35},
      "area": 850,
      "center": {"x": 1595, "y": 177}
    },
    {
      "rank": 2,
      "roi": {"x": 150, "y": 200, "w": 25, "h": 28},
      "area": 600,
      "center": {"x": 162, "y": 214}
    }
  ]
}
```

**PHÂN TÍCH:**
- `recommended_roi` là ROI tốt nhất hệ thống tìm được
- Có thể có nhiều candidates (đèn khác, vật đỏ khác)
- Chọn ROI gần vị trí đèn tín hiệu thật nhất

---

### **Bước 4: Apply ROI mới**

Copy ROI từ response trên và gọi API config:

```bash
POST http://localhost:8000/api/v1/violations/config
Content-Type: application/json

{
  "camera_name": "camera_live",
  "traffic_light_roi": {
    "x": 1580,
    "y": 160,
    "w": 30,
    "h": 35
  },
  "stop_line_y": 544,
  "enable": true
}
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

### **Bước 5: Verify lại**

Gọi lại API debug để xem đã OK chưa:

```bash
GET http://localhost:8000/api/v1/debug/light-detection/camera_live
```

**Response (THÀNH CÔNG):**
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
  },
  "suggestions": [
    "✅ Detection hoạt động tốt!"
  ]
}
```

**Nếu thấy:**
- `detected_color = "red"` ✅
- `red_pixels > 20` ✅
- `confidence > 50%` ✅

→ **ĐÃ FIX XONG!**

---

## 📊 CÁC API ENDPOINTS

### 1. Debug Detection (Stats)
```
GET /api/v1/debug/light-detection/{camera_name}
```
**Response:** JSON stats về detection hiện tại

### 2. Debug Detection (Visual)
```
GET /api/v1/debug/light-detection/{camera_name}?show_masks=true
```
**Response:** JPEG image với 4 masks

### 3. Auto Calibrate ROI
```
POST /api/v1/debug/calibrate-roi/{camera_name}
```
**Response:** Recommended ROI + candidates

### 4. Get HSV Ranges
```
GET /api/v1/debug/test-hsv-ranges
```
**Response:** HSV ranges hiện tại đang dùng

### 5. Apply Config
```
POST /api/v1/violations/config
Body: {camera_name, traffic_light_roi, stop_line_y, enable}
```
**Response:** Config confirmation

---

## 🎨 HIỂU VỀ HSV RANGES

### HSV là gì?
- **H**ue (Màu sắc): 0-180° (đỏ=0, xanh lá=60, xanh dương=120)
- **S**aturation (Độ bão hòa): 0-255 (0=trắng xám, 255=màu thuần)
- **V**alue (Độ sáng): 0-255 (0=đen, 255=trắng sáng)

### Đèn đỏ HSV Ranges (đã tối ưu):

#### Range 1: Đỏ sáng (đèn LED mạnh)
```python
Lower: [0, 70, 50]    # Hue 0-10°, Sat ≥70, Val ≥50
Upper: [10, 255, 255]
```

#### Range 2: Đỏ thẫm (đèn xa/tối)
```python
Lower: [160, 70, 50]  # Hue 160-180°, Sat ≥70, Val ≥50
Upper: [180, 255, 255]
```

#### Range 3: Đỏ rất sáng (LED cao cấp)
```python
Lower: [0, 50, 100]   # Hue 0-15°, Sat ≥50, Val ≥100
Upper: [15, 255, 255]
```

**Ranges này đã cover:**
- ✅ Đèn đỏ sáng/tối
- ✅ Đèn LED/halogen
- ✅ Ban ngày/ban đêm
- ✅ Đèn xa/gần

---

## 🔧 NẾU VẪN KHÔNG DETECT ĐƯỢC ĐỎ

### Tình huống 1: ROI đã đúng nhưng vẫn không detect
**Nguyên nhân:** Đèn quá nhạt hoặc bị che
**Giải pháp:** Giảm threshold trong code

Sửa file `red_light_detector.py`:
```python
# Dòng 376: Giảm min_threshold từ 20 → 10
min_threshold = 10  # Giảm từ 20
```

### Tình huống 2: Detect được nhưng không stable (nhảy qua nhảy lại)
**Nguyên nhân:** ROI quá nhỏ hoặc đèn chớp nháy
**Giải pháp:** Tăng ROI size hoặc giảm min_detections

Sửa file `red_light_detector.py`:
```python
# Dòng 156: Giảm min_detections từ 3 → 2
self.min_detections = 2  # Giảm từ 3
```

### Tình huống 3: Detect nhầm màu khác thành đỏ
**Nguyên nhân:** HSV ranges quá rộng
**Giải pháp:** Tăng Saturation threshold

Sửa file `red_light_detector.py`:
```python
# Dòng 316: Tăng Saturation từ 70 → 100
lower_red1 = np.array([0, 100, 50])  # Tăng từ 70 → 100
```

---

## 🧪 TEST MANUAL (Không dùng API)

Nếu muốn test trực tiếp bằng Python:

```python
import cv2
import numpy as np

# Đọc frame từ video/camera
frame = cv2.imread('frame.jpg')

# Crop ROI
x, y, w, h = 1580, 160, 30, 35
roi = frame[y:y+h, x:x+w]

# Convert to HSV
hsv = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)

# Tạo red mask
lower_red = np.array([0, 70, 50])
upper_red = np.array([10, 255, 255])
mask_red = cv2.inRange(hsv, lower_red, upper_red)

# Đếm pixels
red_pixels = cv2.countNonZero(mask_red)
print(f"Red pixels: {red_pixels}")

# Hiển thị
cv2.imshow('ROI', roi)
cv2.imshow('Red Mask', mask_red)
cv2.waitKey(0)
```

---

## 📝 CHECKLIST DEBUG

- [ ] Backend đã restart
- [ ] Gọi GET `/debug/light-detection` → check stats
- [ ] Gọi GET `/debug/light-detection?show_masks=true` → xem visualization
- [ ] Nếu ROI sai → Gọi POST `/debug/calibrate-roi`
- [ ] Apply ROI mới với POST `/violations/config`
- [ ] Verify lại với GET `/debug/light-detection`
- [ ] Test thực tế với đèn đỏ → xe vượt vạch → có báo vi phạm không?

---

## 🎯 CẢI TIẾN ĐÃ THỰC HIỆN

### 1. Giảm Saturation & Value thresholds
- **Trước:** `[0, 100, 100]` → detect chỉ đèn sáng
- **Sau:** `[0, 70, 50]` → detect cả đèn nhạt/xa

### 2. Thêm range thứ 3 cho đèn LED sáng
- **Mới:** `[0, 50, 100]` → cover đèn LED cao cấp

### 3. Giảm min_threshold
- **Trước:** 30 pixels
- **Sau:** 20 pixels → sensitive hơn với đèn nhỏ

### 4. Debug mode
- Thêm parameter `debug=True` để in ra stats
- Giúp trace vấn đề nhanh hơn

---

**🎉 Chúc bạn debug thành công! Nếu vẫn còn vấn đề, check lại ROI là quan trọng nhất!**
