# HƯỚNG DẪN TEST HỆ THỐNG - 27/11/2025

## ✅ TRẠNG THÁI: BACKEND ĐANG CHẠY!

Backend server đang hoạt động tại: **http://0.0.0.0:8000**

```
✅ Server: HOẠT ĐỘNG
✅ Analyzer (5 processes): HOẠT ĐỘNG
✅ API Endpoints: HOẠT ĐỘNG
✅ Database: HOẠT ĐỘNG
```

---

## 🧪 CÁC CÁCH TEST HỆ THỐNG

### 1. TEST QUA TRÌNH DUYỆT WEB

#### a) Swagger UI - Giao diện test API tương tác

Mở trình duyệt và truy cập:

```
http://localhost:8000/docs
```

Bạn sẽ thấy giao diện Swagger UI với TẤT CẢ các API endpoints. Có thể:
- Click vào từng endpoint để xem chi tiết
- Click "Try it out" để test trực tiếp
- Xem Request/Response format

#### b) Test các trang cụ thể

**Trang chủ:**
```
http://localhost:8000/
```
→ Sẽ redirect về frontend (nếu frontend đang chạy)

**API Documentation (OpenAPI JSON):**
```
http://localhost:8000/openapi.json
```
→ Xem cấu trúc API dạng JSON

---

### 2. TEST API QUA CURL (Command Line)

Mở terminal và chạy các lệnh sau:

#### a) Kiểm tra Weather API

```bash
curl http://localhost:8000/api/v1/weather/current
```

**Kết quả mong đợi:**
```json
{
  "weather": {
    "location": "Hà Nội",
    "temperature": 28.5,
    "description": "trời quang, có mây"
  }
}
```

#### b) Kiểm tra Authentication - Đăng ký user mới

```bash
curl -X POST http://localhost:8000/api/v1/auth/signup ^
  -H "Content-Type: application/json" ^
  -d "{\"username\":\"testuser\",\"email\":\"test@example.com\",\"password\":\"password123\"}"
```

#### c) Kiểm tra Violations API - Lấy danh sách vi phạm

```bash
curl http://localhost:8000/api/v1/violations/list?page=1^&page_size=10
```

#### d) Kiểm tra ChatBot

```bash
curl -X POST http://localhost:8000/chat ^
  -H "Content-Type: application/json" ^
  -d "{\"query\":\"Hôm nay có bao nhiêu xe vi phạm?\"}"
```

---

### 3. TEST FRONTEND (Nếu có)

#### Khởi động Frontend

Mở terminal MỚI (không đóng terminal Backend!) và chạy:

```bash
cd Frontend
npm run dev
```

Frontend sẽ chạy tại: **http://localhost:5173**

#### Các tính năng Frontend có thể test:

1. **Dashboard:** Xem tổng quan giao thông
2. **Live Camera:** Xem camera real-time với detection
3. **Violations:** Xem danh sách vi phạm
4. **Reports:** Xuất báo cáo Excel/PDF
5. **ChatBot:** Chat với AI về giao thông
6. **Authentication:** Đăng nhập/Đăng ký

---

### 4. TEST ANALYZER (YOLO AI Detection)

Analyzer đang chạy với **5 child processes** phân tích video!

#### Kiểm tra Analyzer đang hoạt động:

Mở Python và test:

```python
import requests

# Kiểm tra stream đang chạy
response = requests.get("http://localhost:8000/api/v1/rtsp/streams")
print(response.json())
```

#### Upload video để phân tích:

Sử dụng Swagger UI:
1. Truy cập: http://localhost:8000/docs
2. Tìm endpoint: `POST /api/v1/vehicles/analyze`
3. Click "Try it out"
4. Upload file video (.mp4, .avi)
5. Click "Execute"

Hệ thống sẽ:
- Phát hiện xe cộ trong video
- Đếm số lượng xe
- Phát hiện vi phạm
- Lưu kết quả vào database

---

### 5. TEST DATABASE

#### Kiểm tra database đã được tạo:

```bash
cd Backend
dir traffic_data.db
```

Nếu file tồn tại → Database OK ✅

#### Xem dữ liệu trong database:

```bash
sqlite3 traffic_data.db
.tables
SELECT * FROM traffic_violations LIMIT 5;
.quit
```

---

### 6. TEST TELEGRAM BOT

#### Bước 1: Tìm Bot trên Telegram

Mở Telegram và tìm bot của bạn (tên bot trong file `.env`)

#### Bước 2: Gửi lệnh test

Gửi tin nhắn cho bot:
```
/start
```

Bot sẽ trả lời với menu các lệnh.

Thử các lệnh khác:
```
/status - Xem trạng thái hệ thống
/report - Xem báo cáo hôm nay
/help - Danh sách lệnh
```

---

### 7. TEST SCHEDULER (Auto-save)

Scheduler tự động lưu traffic data **mỗi 10 giây**.

#### Kiểm tra:

1. Để server chạy 30 giây
2. Xem console output sẽ thấy log:
```
✅ Traffic data auto-save scheduler started (interval: 10s)
```

3. Kiểm tra database sẽ thấy data được cập nhật định kỳ

---

## 📊 CHECKLIST TEST TRƯỚC KHI THI

### Backend Tests

- [ ] Server khởi động thành công (< 15 giây)
- [ ] Swagger UI hiển thị đầy đủ endpoints
- [ ] Weather API trả về dữ liệu đúng
- [ ] Authentication (đăng ký/đăng nhập) hoạt động
- [ ] Violations API trả về danh sách
- [ ] ChatBot API trả lời được câu hỏi
- [ ] Database file tồn tại và có data
- [ ] Analyzer khởi tạo (5 processes)
- [ ] Scheduler chạy mỗi 10 giây
- [ ] Telegram Bot phản hồi lệnh

### Frontend Tests (nếu có)

- [ ] Frontend khởi động thành công
- [ ] Kết nối được với Backend API
- [ ] Dashboard hiển thị dữ liệu
- [ ] Live camera stream hoạt động
- [ ] Upload video và phân tích OK
- [ ] Export report (Excel/PDF) OK
- [ ] ChatBot UI hoạt động

### Performance Tests

- [ ] Server phản hồi < 1 giây
- [ ] Video analysis không lag
- [ ] Multiple requests đồng thời OK
- [ ] Memory usage ổn định (< 2GB)
- [ ] CPU usage hợp lý (< 80%)

---

## 🐛 XỬ LÝ LỖI THƯỜNG GẶP

### Lỗi 1: Port 8000 đã được sử dụng

**Triệu chứng:**
```
ERROR: [Errno 10048] error while attempting to bind on address ('0.0.0.0', 8000)
```

**Giải pháp:**
```bash
# Kill tất cả Python processes
wmic process where "name='python.exe'" delete

# Hoặc đổi port khác
python -m uvicorn app.main:app --host 0.0.0.0 --port 8001
```

### Lỗi 2: Module not found

**Triệu chứng:**
```
ModuleNotFoundError: No module named 'xxx'
```

**Giải pháp:**
```bash
cd Backend
pip install -r requirements.txt
```

### Lỗi 3: Database locked

**Triệu chứng:**
```
sqlite3.OperationalError: database is locked
```

**Giải pháp:**
```bash
# Xóa file database cũ
del Backend\traffic_data.db
# Restart server để tạo mới
```

### Lỗi 4: CUDA out of memory

**Triệu chứng:**
```
RuntimeError: CUDA out of memory
```

**Giải pháp:**
- Đóng các ứng dụng khác đang dùng GPU
- Hoặc chạy trên CPU: Sửa `device='cpu'` trong config

---

## 📝 MẸO TEST NHANH TRƯỚC KHI DEMO

### Test 30 giây:

```bash
# 1. Khởi động Backend (5 giây)
cd Backend
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000

# 2. Đợi server sẵn sàng (10 giây)
# Thấy "Application startup complete" → OK

# 3. Test API nhanh (5 giây)
curl http://localhost:8000/docs

# 4. Mở Swagger UI trên trình duyệt (5 giây)
# http://localhost:8000/docs

# 5. Test 1-2 endpoints bất kỳ (5 giây)
# Click "Try it out" → Execute
```

**Nếu tất cả OK → Hệ thống sẵn sàng demo! 🎉**

---

## 🎬 FLOW DEMO CHO KỲ THI

### Phần 1: Giới thiệu (2 phút)

1. Mở slide/powerpoint
2. Giới thiệu vấn đề và giải pháp
3. Mô tả kiến trúc hệ thống

### Phần 2: Demo Backend (5 phút)

1. **Khởi động server:**
   ```bash
   python -m uvicorn app.main:app --host 0.0.0.0 --port 8000
   ```
   → Giải thích: "Server khởi động với Analyzer AI, Scheduler, Telegram Bot"

2. **Mở Swagger UI:**
   ```
   http://localhost:8000/docs
   ```
   → Show tất cả endpoints

3. **Demo Weather API:**
   - Click endpoint `/api/v1/weather/current`
   - Execute → Show kết quả JSON
   → Giải thích: "Hệ thống tích hợp thời tiết để đánh giá ảnh hưởng đến giao thông"

4. **Demo ChatBot:**
   - Endpoint `/chat`
   - Gửi query: "Hôm nay có bao nhiêu xe?"
   → Giải thích: "ChatBot AI sử dụng Google Gemini"

### Phần 3: Demo Frontend (5 phút)

1. **Khởi động Frontend:**
   ```bash
   npm run dev
   ```
   → Truy cập: http://localhost:5173

2. **Show Dashboard:**
   - Biểu đồ thống kê
   - Số lượng xe real-time

3. **Show Live Camera:**
   - Stream video với detection boxes
   - Đếm xe tự động

4. **Show Violations:**
   - Danh sách vi phạm
   - Hình ảnh vi phạm

### Phần 4: Demo Video Analysis (3 phút)

1. **Upload video test:**
   - Chọn video có xe cộ
   - Hệ thống phân tích tự động

2. **Show kết quả:**
   - Số xe phát hiện
   - Loại xe (car, motorbike, truck)
   - Vi phạm (nếu có)

### Phần 5: Q&A (5 phút)

Chuẩn bị trả lời các câu hỏi:
- Thuật toán AI sử dụng? → YOLOv11
- Database? → SQLite (có thể scale lên PostgreSQL)
- Độ chính xác? → 85-90% (tùy điều kiện)
- Xử lý bao nhiêu camera? → 5 camera đồng thời

---

## 🔗 LINKS QUAN TRỌNG

- **Backend API:** http://localhost:8000/docs
- **Frontend:** http://localhost:5173
- **OpenAPI JSON:** http://localhost:8000/openapi.json

---

## 📞 HOTLINE HỖ TRỢ

Nếu gặp vấn đề gấp:
1. Đọc phần "Xử lý lỗi thường gặp" ở trên
2. Check console log để xem lỗi cụ thể
3. Restart lại server (thường fix được 90% lỗi)

---

**Chúc bạn test thành công và thi tốt! 🎓🚀**

---

© 2025 Smart Traffic Monitoring System - Testing Guide
