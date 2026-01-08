# 🚀 QUICK REFERENCE: Debug Light Detection

## ⚡ NHANH NHẤT (2 phút)

### 1. Check hiện tại đang detect cái gì?
```bash
http://localhost:8000/api/v1/debug/light-detection/camera_live?show_masks=true
```
→ Mở trong browser, xem 4 panels

### 2. Tìm ROI đúng tự động
```bash
curl -X POST http://localhost:8000/api/v1/debug/calibrate-roi/camera_live
```
→ Copy ROI từ response

### 3. Apply ROI mới
```bash
curl -X POST http://localhost:8000/api/v1/violations/config \
  -H "Content-Type: application/json" \
  -d '{
    "camera_name": "camera_live",
    "traffic_light_roi": {"x": TỪ_BƯỚC_2, "y": ..., "w": ..., "h": ...},
    "stop_line_y": 544,
    "enable": true
  }'
```

### 4. Verify
```bash
http://localhost:8000/api/v1/debug/light-detection/camera_live?show_masks=true
```
→ Xem lại, đã detect đỏ chưa?

---

## 📊 HIỂU KẾT QUẢ

### JSON Response
```json
{
  "detected_color": "red",          // ✅ OK - đã detect đúng
  "color_pixels": {
    "red": 850,                     // ✅ > 20 là OK
    "yellow": 0,
    "green": 0
  },
  "analysis": {
    "confidence": 85.2              // ✅ > 50% là OK
  }
}
```

### Image Response (4 panels)
```
┌───────────┬───────────┬───────────┬───────────┐
│ Original  │ Red Mask  │Yellow Mask│Green Mask │
│           │ (850 px)  │  (0 px)   │  (0 px)   │
└───────────┴───────────┴───────────┴───────────┘
```

- **Original đen:** ROI sai vị trí
- **Red mask có màu đỏ:** Đang detect đúng ✅
- **All masks đen:** ROI không chứa đèn ❌

---

## 🔧 FIX NHANH

### ROI sai → Auto-calibrate
```bash
POST /api/v1/debug/calibrate-roi/camera_live
```

### Threshold quá cao → Giảm xuống
Edit `red_light_detector.py:376`:
```python
min_threshold = 10  # Từ 20 → 10
```

### Vẫn không detect → HSV ranges quá strict
Edit `red_light_detector.py:316`:
```python
lower_red1 = np.array([0, 50, 30])  # Giảm Sat + Val
```

---

## 🎯 4 API ENDPOINTS

| API | URL | Mục đích |
|-----|-----|----------|
| **Stats** | `GET /debug/light-detection/{cam}` | JSON stats |
| **Visual** | `GET /debug/light-detection/{cam}?show_masks=true` | Ảnh 4 panels |
| **Calibrate** | `POST /debug/calibrate-roi/{cam}` | Tìm ROI |
| **HSV Info** | `GET /debug/test-hsv-ranges` | Xem ranges |

---

## ✅ CHECKLIST 30 GIÂY

- [ ] Backend đang chạy?
- [ ] Đèn đỏ đang BẬT?
- [ ] Call API debug → xem visualization
- [ ] Red mask có màu không?
  - **Có:** ROI OK, HSV OK ✅
  - **Không:** Chạy calibrate-roi

---

**💡 Tip:** Bookmark URL này để debug nhanh:
```
http://localhost:8000/api/v1/debug/light-detection/camera_live?show_masks=true
```
