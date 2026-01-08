# 📹 HƯỚNG DẪN TRIỂN KHAI HỆ THỐNG GIÁM SÁT GIAO THÔNG

**Dành cho:** Đơn vị quản lý camera giao thông  
**Phiên bản:** 3.0.0  
**Ngày:** 11/12/2024  
**Tác giả:** Smart Traffic Monitoring Team

---

## 📋 TỔNG QUAN

Hệ thống **Smart Traffic Monitoring System** là giải pháp AI giám sát giao thông thông minh, có khả năng:

- ✅ Phát hiện và đếm phương tiện real-time
- ✅ Nhận diện vi phạm giao thông (vượt đèn đỏ, quá tốc độ)
- ✅ Phân tích lưu lượng và xuất báo cáo
- ✅ Tích hợp camera RTSP có sẵn
- ✅ Cảnh báo qua Telegram Bot
- ✅ Dashboard web hiện đại

---

## 🎯 QUY TRÌNH CÀI ĐẶT (5 BƯỚC)

### BƯỚC 1: CHUẨN BỊ MÁY CHỦ

#### Yêu cầu phần cứng tối thiểu:
| Thành phần | Tối thiểu | Khuyến nghị |
|------------|-----------|-------------|
| **CPU** | Intel Core i5 Gen 8+ | Intel Core i7 Gen 10+ hoặc AMD Ryzen 7 |
| **RAM** | 8 GB | 16 GB |
| **GPU** | Không bắt buộc | NVIDIA GTX 1650+ (4GB VRAM) |
| **Ổ cứng** | 50 GB trống | 100 GB+ SSD |
| **Network** | 100 Mbps | 1 Gbps |

#### Yêu cầu phần mềm:
- **Hệ điều hành:** Windows 10/11 (64-bit) hoặc Ubuntu 20.04+
- **Python:** 3.9, 3.10, 3.11 hoặc 3.12
- **Node.js:** 18.x hoặc cao hơn
- **Git:** Phiên bản mới nhất

---

### BƯỚC 2: TẢI VÀ CÀI ĐẶT

#### 2.1. Clone mã nguồn

```bash
# Tải source code
git clone https://github.com/your-repo/Smart-Traffic-Monitoring-System.git
cd Smart-Traffic-Monitoring-System
```

#### 2.2. Cài đặt Backend (Python)

```bash
# Di chuyển vào thư mục Backend
cd Backend

# Tạo môi trường ảo Python
python -m venv venv

# Kích hoạt môi trường ảo
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Cài đặt thư viện
pip install -r requirements_cpu.txt

# Nếu có GPU NVIDIA:
pip install -r requirements_gpu.txt
```

#### 2.3. Cài đặt Frontend (React)

```bash
# Mở terminal mới, di chuyển vào thư mục Frontend
cd Frontend

# Cài đặt Node packages
npm install -g pnpm
pnpm install
```

---

### BƯỚC 3: CẤU HÌNH CAMERA RTSP

#### 3.1. Lấy thông tin camera

Bạn cần cung cấp:
- **RTSP URL** của camera (ví dụ: `rtsp://username:password@192.168.1.100:554/stream1`)
- **Username/Password** nếu camera yêu cầu xác thực
- **Resolution** (khuyến nghị: 1280x720 hoặc 1920x1080)
- **FPS** (khuyến nghị: 15-30 FPS)

#### 3.2. Cấu hình file `.env`

Tạo file `Backend/.env` với nội dung:

```env
# Database
DATABASE_URL=sqlite+aiosqlite:///./traffic_data.db

# JWT Authentication
JWT_SECRET_KEY=your-secret-key-here-change-in-production
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=1440

# RTSP Camera Configuration
ENABLE_RTSP=True
RTSP_URL=rtsp://username:password@camera-ip:554/stream1

# Google Gemini API (cho Chatbot)
GOOGLE_API_KEY=your-google-api-key-here

# Telegram Bot (tùy chọn)
TELEGRAM_BOT_TOKEN=your-telegram-bot-token-here
TELEGRAM_CHAT_ID=your-chat-id-here
```

#### 3.3. Test kết nối camera

```bash
# Chạy script test camera
cd Backend/app
python test_rtsp_connection.py
```

---

### BƯỚC 4: KHỞI ĐỘNG HỆ THỐNG

#### 4.1. Khởi động Backend

```bash
# Terminal 1 - Backend
cd Backend/app
..\venv\Scripts\python.exe -m uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

**Kiểm tra:** Mở trình duyệt, truy cập http://localhost:8000/api/docs

#### 4.2. Khởi động Frontend

```bash
# Terminal 2 - Frontend
cd Frontend
pnpm run dev
```

**Kiểm tra:** Mở trình duyệt, truy cập http://localhost:5173

---

### BƯỚC 5: KIỂM TRA VÀ DEMO

#### 5.1. Checklist kiểm tra

- [ ] Backend server chạy thành công (http://localhost:8000/api/health)
- [ ] Frontend hiển thị giao diện đầy đủ
- [ ] Camera RTSP kết nối và hiển thị video
- [ ] AI phát hiện xe trong video
- [ ] Dashboard cập nhật số liệu real-time
- [ ] Có thể xuất báo cáo PDF/Excel

#### 5.2. Demo tính năng

1. **Giám sát video live:**
   - Truy cập tab "Live Camera"
   - Xem video từ camera RTSP
   - Quan sát AI phát hiện xe (bounding boxes)

2. **Phân tích traffic:**
   - Truy cập tab "Dashboard"
   - Xem biểu đồ lưu lượng real-time
   - Check số xe ô tô, xe máy

3. **Xuất báo cáo:**
   - Truy cập tab "Reports"
   - Chọn khoảng thời gian
   - Click "Export PDF" hoặc "Export Excel"

---

## 🚦 BỔ SUNG CAMERA PHỤ PHÁT HIỆN VƯỢT ĐÈN ĐỎ

### Tổng quan

Để phát hiện vi phạm vượt đèn đỏ với độ chính xác cao (95%+), hệ thống cần:
- **Camera chính:** Giám sát làn đường, phát hiện xe cộ
- **Camera phụ:** Nhìn trực tiếp đèn tín hiệu giao thông (ĐỎ-VÀNG-XANH)

### Yêu cầu Camera Phụ

#### Khuyến nghị loại camera:

**1. Camera IP RTSP (Ưu tiên cao nhất)**
- Hikvision DS-2CD2xxx series
- Dahua IPC-HFWxxxx series
- AXIS M-series
- **Thông số tối thiểu:**
  - Resolution: 1920x1080 (Full HD)
  - FPS: 15-30
  - Hỗ trợ PoE (Power over Ethernet)
  - Chống ngược sáng (WDR/HDR)
  - Hoạt động tốt ban đêm (Low Light)
  - Chịu nước IP66+ (nếu lắp ngoài trời)

**2. Camera USB (Dự phòng)**
- Logitech C920/C922/C930e
- Resolution tối thiểu: 1280x720
- FPS: 20-30

### Vị Trí Lắp Đặt Camera Phụ

**Nguyên tắc vàng:**
```
      Đèn tín hiệu
           🚦
           ↑
           | 10-30m
           |
         📹 Camera phụ
```

**Yêu cầu:**
- ✅ Nhìn thẳng vào mặt đèn tín hiệu (3 đèn: đỏ-vàng-xanh phải rõ nét)
- ✅ Góc lệch < 30 độ so với trục đèn
- ✅ Khoảng cách 10-30m (tùy độ phân giải)
- ✅ Đèn chiếm 5-10% diện tích khung hình
- ❌ Tránh cây cối che khuất
- ❌ Tránh ngược sáng mặt trời trực tiếp
- ❌ Tránh vị trí rung lắc

### Cấu hình Camera Phụ

#### Bước 1: Kết nối phần cứng

**Phương án A - Camera IP (Khuyến nghị):**
```
Camera IP → Dây mạng Cat5e/Cat6 (max 100m) → Switch PoE → Máy tính
```

**Phương án B - Camera USB:**
```
Camera USB → Dây USB (max 5m) → Máy tính
```

#### Bước 2: Cấu hình trong file `.env`

Thêm vào file `Backend/.env`:

```env
# Camera phụ nhìn đèn tín hiệu
TRAFFIC_LIGHT_CAMERA_ENABLED=True

# Nếu dùng camera IP RTSP:
TRAFFIC_LIGHT_CAMERA_URL=rtsp://admin:password@192.168.1.101:554/h264/ch1/main/av_stream

# Nếu dùng camera USB:
# TRAFFIC_LIGHT_CAMERA_URL=0  # 0 = USB camera đầu tiên, 1 = thứ hai

# Tùy chỉnh độ sáng (1.0 = bình thường, >1 = sáng hơn)
TRAFFIC_LIGHT_BRIGHTNESS=1.2
TRAFFIC_LIGHT_CONTRAST=1.3
```

#### Bước 3: Vẽ ROI (Region of Interest)

Chạy công cụ vẽ ROI để chọn vùng chứa đèn tín hiệu:

```bash
cd Backend
python app/select_roi.py --camera traffic_light
```

**Hướng dẫn:**
1. Cửa sổ video từ camera phụ sẽ hiển thị
2. Click chuột để chọn 4 góc bao quanh đèn tín hiệu:
   ```
   Click 1 (trên trái)
   ┌─────────────┐
   │  🔴 ĐỎ      │
   │  🟡 VÀNG    │
   │  🟢 XANH    │
   └─────────────┘
              Click 4 (dưới phải)
   ```
3. Nhấn `s` để lưu
4. Nhấn `r` để vẽ lại nếu sai
5. Nhấn `q` để thoát

ROI sẽ được lưu tại: `Backend/app/config/traffic_light_roi.json`

#### Bước 4: Test phát hiện đèn

```bash
cd Backend
python demo_traffic_light_detection.py
```

Kết quả mong đợi:
```
Detected: RED (Confidence: 0.92)
Detected: GREEN (Confidence: 0.88)
Detected: YELLOW (Confidence: 0.85)
```

### Xử Lý Sự Cố Camera Phụ

**Sự cố 1: Không kết nối được camera RTSP**
```
Lỗi: "Failed to open RTSP stream"
```
Giải pháp:
1. Test URL bằng VLC: Media → Open Network Stream → Nhập RTSP URL
2. Kiểm tra: `ping [IP_camera]`
3. Đảm bảo firewall mở port 554
4. Thử format URL: `rtsp://username:password@IP:port/path`

**Sự cố 2: Camera USB không nhận**
```
Lỗi: "Camera index 0 not found"
```
Giải pháp:
1. Kiểm tra Device Manager (Windows): Win+X → Device Manager → Cameras
2. Thử index khác: 0, 1, 2, 3
3. Cài lại driver camera

**Sự cố 3: Phát hiện sai màu đèn**
```
Triệu chứng: Đèn đỏ bị nhận thành xanh
```
Giải pháp:
1. Vẽ lại ROI chính xác hơn (chỉ bao đèn, không bao vật khác)
2. Điều chỉnh độ sáng/tương phản trong `.env`
3. Kiểm tra camera có bị mờ/bẩn không
4. Điều chỉnh threshold HSV trong code (nếu cần)

**Sự cố 4: FPS quá thấp**
```
Triệu chứng: Video giật lag, FPS < 10
```
Giải pháp:
1. Giảm resolution camera xuống 720p
2. Giảm FPS xuống 15
3. Đảm bảo dùng GPU (nếu có): `nvidia-smi`

### Checklist Triển Khai Camera Phụ

```
□ Phần cứng
  □ Đã chọn mua camera phù hợp
  □ Đã chuẩn bị dây cáp (mạng/USB)
  □ Đã chuẩn bị giá đỡ/khung treo

□ Lắp đặt
  □ Đã xác định vị trí lắp tối ưu
  □ Đã lắp camera và kéo dây
  □ Đã kết nối nguồn điện/PoE
  □ Đã kết nối mạng về máy tính

□ Cấu hình
  □ Đã thêm RTSP URL vào .env
  □ Đã vẽ ROI cho đèn tín hiệu
  □ Đã test phát hiện đỏ/vàng/xanh

□ Kiểm tra
  □ Đèn tín hiệu hiển thị rõ nét
  □ Phát hiện đúng 3 màu (đỏ-vàng-xanh)
  □ Độ chính xác > 95% (test 100 mẫu)
  □ FPS ổn định > 15
```

---

## 🔧 YÊU CẦU NETWORK CHO CAMERA

### Băng thông cần thiết:

| Số camera | Resolution | FPS | Băng thông |
|-----------|-----------|-----|------------|
| 1 camera | 720p | 15 | ~2 Mbps |
| 1 camera | 1080p | 30 | ~5-8 Mbps |
| 2 camera (chính + phụ) | 1080p + 720p | 30 + 15 | ~7-10 Mbps |
| 5 camera | 720p | 15 | ~10 Mbps |
| 10 camera | 1080p | 30 | ~50-80 Mbps |

### Cấu hình mạng:

- **Latency:** < 100ms (từ camera đến server)
- **Packet loss:** < 1%
- **Port cần mở:**
  - 8000 (Backend API)
  - 5173 (Frontend - chỉ dev mode)
  - 554 (RTSP - output từ camera)

---

## 🎬 SCRIPT DEMO TỰ ĐỘNG

Để demo nhanh cho chú xem, bạn có thể chạy script này:

```bash
# File: demo_quick.bat (Windows)
@echo off
echo ========================================
echo   SMART TRAFFIC MONITORING SYSTEM
echo              DEMO SCRIPT
echo ========================================
echo.

echo [1/3] Khởi động Backend...
start "Backend Server" cmd /k "cd Backend\app && ..\..\venv\Scripts\python.exe -m uvicorn main:app --host 0.0.0.0 --port 8000"

timeout /t 10

echo [2/3] Khởi động Frontend...
start "Frontend Server" cmd /k "cd Frontend && pnpm run dev"

timeout /t 5

echo [3/3] Mở trình duyệt...
start http://localhost:5173

echo.
echo ========================================
echo   HỆ THỐNG ĐÃ SẴN SÀNG!
echo   Frontend: http://localhost:5173
echo   API Docs: http://localhost:8000/api/docs
echo ========================================
pause
```

---

## 📊 GIÁM SÁT VÀ BẢO TRÌ

### Kiểm tra log hệ thống:

```bash
# Backend logs
tail -f Backend/logs/traffic_system.log

# Check system health
curl http://localhost:8000/api/system/status
```

### Backup dữ liệu:

```bash
# Backup database
cp Backend/app/traffic_data.db backup/traffic_data_$(date +%Y%m%d).db

# Backup ảnh vi phạm
cp -r Backend/app/static/violation_images backup/images_$(date +%Y%m%d)
```

---

## 🆘 XỬ LÝ SỰ CỐ THƯỜNG GẶP

### Sự cố 1: Camera không kết nối

**Triệu chứng:** Lỗi "RTSP connection failed"

**Giải pháp:**
1. Kiểm tra RTSP URL đúng format: `rtsp://user:pass@ip:port/path`
2. Test bằng VLC Media Player: File → Open Network Stream
3. Kiểm tra firewall cho phép port 554
4. Thử giảm resolution/FPS của camera

### Sự cố 2: AI không phát hiện xe

**Triệu chứng:** Video hiển thị nhưng không có bounding boxes

**Giải pháp:**
1. Kiểm tra Analyzer đã khởi động: http://localhost:8000/api/system/status
2. Check console log Backend có lỗi không
3. Restart Backend server

### Sự cố 3: Backend chậm/lag

**Triệu chứng:** Response time > 1 giây

**Giải pháp:**
1. Giảm số camera xử lý đồng thời
2. Giảm FPS xuống 10-15
3. Nâng cấp RAM/CPU
4. Cân nhắc thêm GPU

---

## 📞 HỖ TRỢ KỸ THUẬT

**Team:** Smart Traffic Monitoring System  
**Email:** support@smarttraffic.vn  
**Hotline:** 0900 XXX XXX  
**Remote Support:** TeamViewer/AnyDesk

**Thời gian hỗ trợ:**
- Trong giờ: 8:00 - 17:30 (T2-T6)
- Ngoài giờ: Qua email/Telegram

---

## 📝 CHECKLIST GIAO NHẬN

Khi triển khai xong, cần xác nhận:

- [ ] Hệ thống chạy ổn định > 24h
- [ ] Camera kết nối thành công
- [ ] AI phát hiện xe chính xác > 85%
- [ ] Dashboard cập nhật real-time
- [ ] Xuất báo cáo thành công
- [ ] Đã backup dữ liệu
- [ ] Đã đào tạo người vận hành

**Ký xác nhận:**

- Người triển khai: ________________
- Đơn vị nhận: ________________
- Ngày: ________________

---

**© 2024 Smart Traffic Monitoring System - Tài liệu triển khai v3.0**
