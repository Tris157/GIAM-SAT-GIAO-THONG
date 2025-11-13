# 🌦️ Hướng Dẫn Tính Năng Dự Báo Thời Tiết

## 📋 Tổng Quan

Tính năng dự báo thời tiết đã được tích hợp vào hệ thống Smart Traffic Monitoring System, giúp phân tích ảnh hưởng của thời tiết đến giao thông.

## ✨ Tính Năng

### 1. **Thời Tiết Hiện Tại**
- 🌡️ Nhiệt độ thực tế và cảm giác
- 💨 Tốc độ gió
- 💧 Độ ẩm không khí
- 👁️ Tầm nhìn
- 🔲 Áp suất khí quyển
- ☔ Lượng mưa (nếu có)

### 2. **Dự Báo 5 Ngày**
- 📅 Nhiệt độ min/max cho mỗi ngày
- ☁️ Mô tả thời tiết
- 💧 Xác suất mưa
- 🌡️ Nhiệt độ trung bình

### 3. **Cảnh Báo Ảnh Hưởng Giao Thông**
Hệ thống tự động phân tích và cảnh báo:

#### 🟢 Mức Thấp (Low)
- Thời tiết tốt
- Giao thông bình thường
- Không có khuyến nghị đặc biệt

#### 🟡 Mức Trung Bình (Medium)
- Thời tiết ổn định nhưng có yếu tố cần lưu ý
- Khuyến nghị giảm tốc độ nhẹ

#### 🟠 Mức Cao (High)
**Điều kiện kích hoạt:**
- ☔ Mưa/Mưa phùn
- 🌫️ Sương mù (tầm nhìn < 5km)
- 💨 Gió mạnh (> 40 km/h)

**Khuyến nghị:**
- Giảm tốc độ 20-30%
- Tăng khoảng cách an toàn
- Bật đèn xe
- Cẩn thận khi lái xe
- Bật đèn sương mù (nếu có sương)

#### 🔴 Mức Cực Đoan (Extreme)
**Điều kiện kích hoạt:**
- ❄️ Tuyết
- 🌫️ Sương mù dày đặc (tầm nhìn < 1km)

**Khuyến nghị:**
- Hạn chế di chuyển
- Sử dụng phương tiện công cộng
- Kiểm tra lốp xe
- Không chuyển làn đột ngột

## 🚀 Cách Sử Dụng

### Bước 1: Khởi động hệ thống

#### Backend:
```bash
cd Backend/app
../venv/Scripts/python.exe -m uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

#### Frontend:
```bash
cd Frontend
npm run dev
```

### Bước 2: Truy cập Dashboard

Mở trình duyệt và truy cập: `http://localhost:5173`

### Bước 3: Xem Thời Tiết

Widget thời tiết hiển thị ở **thanh bên phải** trong tab **"Giám Sát"**.

## 🔑 Cấu Hình API Key (Tùy Chọn)

Hiện tại hệ thống đang chạy ở **Demo Mode** với dữ liệu mẫu.

Để sử dụng dữ liệu thời tiết thực, làm theo các bước sau:

### 1. Đăng ký OpenWeatherMap (MIỄN PHÍ)

1. Truy cập: https://openweathermap.org/api
2. Click "Sign Up" (Đăng ký)
3. Xác nhận email
4. Vào trang "API Keys" và copy API key của bạn

### 2. Cấu hình Backend

Mở file `Backend/.env` và thay đổi:

```env
# Thay "demo" bằng API key thực của bạn
OPENWEATHER_API_KEY=your_actual_api_key_here

# Tọa độ vị trí (mặc định: Hà Nội)
WEATHER_LAT=21.0285
WEATHER_LON=105.8542
```

### 3. Thay đổi vị trí (Tùy chọn)

Nếu muốn đổi vị trí khác Hà Nội:

1. Tìm tọa độ GPS của vị trí: https://www.latlong.net/
2. Cập nhật `WEATHER_LAT` và `WEATHER_LON` trong file `.env`

Ví dụ cho TP. Hồ Chí Minh:
```env
WEATHER_LAT=10.8231
WEATHER_LON=106.6297
```

### 4. Khởi động lại Backend

```bash
cd Backend/app
../venv/Scripts/python.exe -m uvicorn main:app --reload
```

## 🧪 Test API Endpoints

### Test thời tiết hiện tại:
```bash
curl http://localhost:8000/api/v1/weather/current
```

### Test dự báo 5 ngày:
```bash
curl http://localhost:8000/api/v1/weather/forecast?days=5
```

### Test với tọa độ khác:
```bash
# TP. Hồ Chí Minh
curl "http://localhost:8000/api/v1/weather/current?lat=10.8231&lon=106.6297"
```

## 📊 API Response Format

### Current Weather Response:
```json
{
  "weather": {
    "location": "Hà Nội",
    "temperature": 28.5,
    "feels_like": 30.2,
    "humidity": 65,
    "pressure": 1013,
    "description": "trời quang, có mây",
    "icon": "02d",
    "wind_speed": 12.5,
    "clouds": 25,
    "visibility": 10.0,
    "weather_code": 801,
    "demo": true
  },
  "traffic_impact": {
    "level": "low",
    "color": "green",
    "message": "Thời tiết tốt, giao thông bình thường",
    "recommendations": []
  }
}
```

### Forecast Response:
```json
{
  "location": "Hà Nội",
  "days": [
    {
      "date": "2025-11-08",
      "day_name": "Saturday",
      "temp_min": 24.0,
      "temp_max": 32.0,
      "temp_avg": 28.0,
      "description": "có mây rải rác",
      "icon": "02d",
      "humidity": 60,
      "rain_probability": 10
    }
    // ... 4 ngày tiếp theo
  ],
  "demo": true
}
```

## 🎨 Giao Diện

Widget thời tiết bao gồm:

1. **Card Thời Tiết Hiện Tại**
   - Icon thời tiết động
   - Nhiệt độ lớn, dễ đọc
   - Chi tiết 4 chỉ số: Gió, Độ ẩm, Tầm nhìn, Áp suất
   - Nút refresh thủ công

2. **Alert Cảnh Báo** (chỉ hiện khi thời tiết xấu)
   - Màu sắc theo mức độ nguy hiểm
   - Icon cảnh báo
   - Danh sách khuyến nghị cụ thể

3. **Dự Báo 5 Ngày**
   - Layout dạng lưới
   - Icon thời tiết
   - Nhiệt độ min/max
   - Xác suất mưa

## 🔧 Tùy Chỉnh

### Thay đổi thời gian cache:

Mở `Backend/app/services/weather_service.py`:

```python
self._cache_timeout = timedelta(minutes=10)  # Đổi thành 5, 15, 30 minutes...
```

### Thay đổi tần suất auto-refresh Frontend:

Mở `Frontend/src/components/WeatherWidget.tsx`:

```typescript
const interval = setInterval(fetchWeather, 10 * 60 * 1000); // 10 phút
// Đổi thành: 5 * 60 * 1000 (5 phút) hoặc 15 * 60 * 1000 (15 phút)
```

## 📈 Giá Trị Thực Tiễn

### Cho Đồ Án Tốt Nghiệp:
1. ✅ Tích hợp thực tế với hệ thống giao thông
2. ✅ Dữ liệu thời tiết ảnh hưởng đến mật độ xe
3. ✅ Cảnh báo an toàn cho người tham gia giao thông
4. ✅ Phân tích tương quan thời tiết - tắc đường

### Cho Ứng Dụng Thực Tế:
1. 🚗 Hỗ trợ ra quyết định cho tài xế
2. 📊 Dự đoán mật độ giao thông dựa trên thời tiết
3. 🚨 Cảnh báo sớm điều kiện nguy hiểm
4. 📈 Phân tích dữ liệu lịch sử

## ❓ Troubleshooting

### Lỗi: "demo": true luôn hiển thị

**Nguyên nhân:** API key chưa được cấu hình hoặc không hợp lệ

**Giải pháp:**
1. Kiểm tra file `.env` có `OPENWEATHER_API_KEY` chính xác
2. Verify API key tại: https://home.openweathermap.org/api_keys
3. Khởi động lại backend

### Lỗi: Weather widget không hiển thị

**Nguyên nhân:** Backend không chạy hoặc CORS error

**Giải pháp:**
1. Kiểm tra backend đang chạy: `curl http://localhost:8000/api/v1/weather/current`
2. Xem console log trên browser (F12)
3. Kiểm tra CORS middleware trong `main.py`

### Lỗi: API rate limit exceeded

**Nguyên nhân:** Free tier OpenWeatherMap giới hạn 60 calls/minute

**Giải pháp:**
1. Tăng thời gian cache lên 15-30 phút
2. Giảm tần suất auto-refresh
3. Upgrade plan (nếu cần)

## 📝 Dependencies

### Backend:
- `aiohttp` - Async HTTP client cho API calls
- `python-dotenv` - Đọc environment variables

### Frontend:
- `lucide-react` - Icons
- `framer-motion` - Animations
- Các UI components đã có sẵn

## 🎓 Tài Liệu Tham Khảo

- OpenWeatherMap API Docs: https://openweathermap.org/api
- Weather Codes: https://openweathermap.org/weather-conditions
- Tọa độ GPS Việt Nam: https://www.latlong.net/

## 💡 Ý Tưởng Mở Rộng

1. **Lưu lịch sử thời tiết** vào database
2. **Phân tích tương quan** thời tiết vs tắc đường
3. **Biểu đồ xu hướng** nhiệt độ theo giờ
4. **Thông báo push** khi có thời tiết xấu
5. **Tích hợp AI** dự đoán traffic dựa trên forecast

---

**Phát triển bởi:** Smart Traffic Monitoring System Team
**Ngày cập nhật:** 08/11/2025
**Version:** 1.0.0
