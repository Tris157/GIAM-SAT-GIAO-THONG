# 🚦 Smart Traffic Monitoring System

Hệ thống giám sát và phân tích giao thông thông minh sử dụng AI (YOLO + OpenVINO) để phát hiện và đếm phương tiện theo thời gian thực.

![Python](https://img.shields.io/badge/Python-3.9--3.12-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-0.104-green)
![React](https://img.shields.io/badge/React-18.3-61DAFB)
![TypeScript](https://img.shields.io/badge/TypeScript-5.5-blue)
![OpenVINO](https://img.shields.io/badge/OpenVINO-2024-purple)

## ✨ Tính Năng Chính

### 🎥 Giám Sát Video Real-time
- ✅ Phát hiện và đếm xe ô tô, xe máy theo thời gian thực với YOLO
- ✅ Tính toán tốc độ trung bình của từng loại xe
- ✅ WebSocket streaming cho hiển thị video mượt mà (15 FPS)
- ✅ Hỗ trợ đa tuyến đường (5 tuyến mặc định, có thể mở rộng)
- ✅ ByteTrack tracking để theo dõi xe qua nhiều frame

### 📊 Phân Tích & Báo Cáo (NEW)
- ✅ **Giờ Cao Điểm / Thấp Điểm**: Tự động phát hiện giờ có lưu lượng cao/thấp nhất
- ✅ **Xu Hướng Theo Giờ**: Area Chart hiển thị traffic theo 24 giờ
- ✅ **So Sánh Tuyến Đường**: Bar Chart so sánh lưu lượng giữa các đường
- ✅ **Biểu Đồ Xu Hướng**: Line Chart theo dõi traffic theo thời gian thực
- ✅ **Export Dữ Liệu**: CSV và JSON format
- ✅ **Lọc Thời Gian**: Hôm nay / 7 ngày / 30 ngày
- ✅ **Real-time Update**: Tự động cập nhật mỗi khi có dữ liệu mới

### 🤖 Trợ Lý AI
- ✅ Chatbot tích hợp Google Gemini API
- ✅ ReActAgent based on LangGraph
- ✅ Trả lời câu hỏi về tình hình giao thông
- ✅ Gợi ý tuyến đường dựa trên dữ liệu thực tế
- ✅ Hiểu ngữ cảnh và phân tích xu hướng

### 🎨 Giao Diện Hiện Đại
- ✅ Dark theme với OKLCH color space
- ✅ Glass morphism effects
- ✅ Framer Motion animations
- ✅ Responsive design (Mobile/Tablet/Desktop)
- ✅ Custom scrollbar với gradient
- ✅ Animated background với gradient orbs
- ✅ Real-time updates không cần refresh

## 🛠️ Công Nghệ Sử Dụng

### Backend
| Công nghệ | Phiên bản | Mô tả |
|-----------|-----------|-------|
| **FastAPI** | 0.104+ | REST API và WebSocket server |
| **OpenVINO** | 2024 | INT8 quantized YOLO inference |
| **SQLAlchemy** | 2.0+ | ORM cho database |
| **SQLite** | 3.x | Database lưu trữ lịch sử |
| **OpenCV** | 4.x | Xử lý video và computer vision |
| **Google Gemini API** | - | AI chatbot |
| **ByteTrack** | - | Object tracking |
| **LangGraph** | - | ReActAgent framework |

### Frontend
| Công nghệ | Phiên bản | Mô tả |
|-----------|-----------|-------|
| **React** | 18.3+ | UI framework |
| **TypeScript** | 5.5+ | Type-safe JavaScript |
| **Vite** | 7.x | Build tool |
| **TailwindCSS** | 3.x | Utility-first CSS |
| **Recharts** | 2.x | Data visualization |
| **Framer Motion** | 11.x | Animation library |
| **Shadcn/ui** | - | UI components |
| **date-fns** | 4.x | Date utilities |

## 📋 Yêu Cầu Hệ Thống

### Phần Cứng
- **CPU**: Intel Core i5 hoặc tương đương (khuyến nghị i7+)
- **RAM**: Tối thiểu 8GB (khuyến nghị 16GB+)
- **GPU**: Optional - NVIDIA GPU cho tăng tốc (CUDA support)
- **Storage**: ~5GB cho models và dependencies
- **Network**: Kết nối internet để tải models và API calls

### Phần Mềm
- **OS**: Windows 10/11, Ubuntu 20.04+, macOS 12+
- **Python**: 3.9 - 3.12 (không hỗ trợ 3.13+)
- **Node.js**: 18.x hoặc cao hơn
- **pnpm**: 8.x hoặc cao hơn
- **Git**: Để clone repository

## 🚀 Hướng Dẫn Cài Đặt

### Bước 1: Clone Repository

```bash
git clone <repository-url>
cd Smart-Trafic-Monitoring-System-main
```

### Bước 2: Cài Đặt Backend

#### 2.1. Tạo Môi Trường Ảo Python

```bash
cd Backend
python -m venv venv
```

#### 2.2. Kích Hoạt Môi Trường Ảo

**Windows:**
```bash
.\venv\Scripts\activate
```

**Linux/Mac:**
```bash
source venv/bin/activate
```

#### 2.3. Cài Đặt Dependencies

**Cho CPU (khuyến nghị cho hầu hết người dùng):**
```bash
pip install -r requirements_cpu.txt
```

**Cho GPU (nếu có NVIDIA GPU + CUDA):**
```bash
pip install -r requirements_gpu.txt
```

**Linux: Cài thêm OpenCV dependencies:**
```bash
sudo apt update
sudo apt install -y libgl1 libglib2.0-0
```

#### 2.4. Cấu Hình File .env

Tạo hoặc chỉnh sửa file `Backend/.env`:

```env
# Google Gemini API Key (Bắt buộc cho chatbot)
GOOGLE_API_KEY=your_google_api_key_here

# Database Configuration
DATABASE_URL=sqlite:///./traffic_data.db

# JWT Configuration (Optional - cho authentication)
JWT_SECRET_KEY=your_secret_key_here
ACCESS_TOKEN_EXPIRE_MINUTES=30
JWT_ALGORITHM=HS256
```

**Lấy Google API Key:**
1. Truy cập: https://aistudio.google.com/app/apikey
2. Đăng nhập với Google account
3. Click "Create API Key"
4. Copy key và paste vào file `.env`

#### 2.5. Tải Video Test

**Cách 1: Tải từ Google Drive (khuyến nghị)**
```bash
cd app
pip install gdown
gdown --folder https://drive.google.com/drive/folders/1gkac5U5jEs174p7V7VC3rCmgvO_cVwxH
cd ..
```

**Cách 2: Sử dụng video có sẵn**
- Video đã có trong `Backend/app/video_test/`
- Bỏ qua bước này nếu folder đã tồn tại

### Bước 3: Cài Đặt Frontend

#### 3.1. Cài Đặt pnpm (nếu chưa có)

```bash
npm install -g pnpm
```

#### 3.2. Cài Đặt Dependencies

```bash
cd Frontend
pnpm install
```

**Nếu gặp lỗi, thử:**
```bash
pnpm install --force
# hoặc
npm install
```

## 🎮 Chạy Ứng Dụng

### Cách 1: Chạy Thủ Công (Khuyến Nghị)

#### Terminal 1 - Backend:
```bash
cd Backend/app
# Windows
..\venv\Scripts\python.exe -m uvicorn main:app --reload --host 0.0.0.0 --port 8000

# Linux/Mac
../venv/bin/python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

#### Terminal 2 - Frontend:
```bash
cd Frontend
pnpm run dev
```

**Kết quả:**
- Backend: http://localhost:8000
- Frontend: http://localhost:5173
- API Docs: http://localhost:8000/docs

### Cách 2: Script Tự Động

**Windows - Tạo file `start.bat`:**
```batch
@echo off
echo Starting Smart Traffic Monitoring System...
start "Backend Server" cmd /k "cd Backend\app && ..\venv\Scripts\python.exe -m uvicorn main:app --reload --host 0.0.0.0 --port 8000"
timeout /t 5
start "Frontend Server" cmd /k "cd Frontend && pnpm run dev"
echo Both servers started!
pause
```

**Linux/Mac - Tạo file `start.sh`:**
```bash
#!/bin/bash
echo "Starting Smart Traffic Monitoring System..."
cd Backend/app && ../venv/bin/python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000 &
BACKEND_PID=$!
sleep 5
cd Frontend && pnpm run dev &
FRONTEND_PID=$!
echo "Backend PID: $BACKEND_PID"
echo "Frontend PID: $FRONTEND_PID"
echo "Both servers started!"
wait
```

**Chạy:**
```bash
# Windows
start.bat

# Linux/Mac
chmod +x start.sh
./start.sh
```

### Cách 3: Docker (Khuyến Nghị Cho Production)

**Bước 1: Chuẩn bị video**
```bash
cd Backend/app
pip install gdown
gdown --folder https://drive.google.com/drive/folders/1gkac5U5jEs174p7V7VC3rCmgvO_cVwxH
cd ../..
```

**Bước 2: Build và chạy**
```bash
# CPU version
docker compose up --build

# GPU version
docker compose up --build --build-arg DEVICE=gpu

# Run in background
docker compose up --build -d
```

**Dừng containers:**
```bash
docker compose down
```

## 📖 Hướng Dẫn Sử Dụng Chi Tiết

### 1️⃣ Tab Giám Sát (Monitor)

**Giao diện chính:**
- Video streaming ở giữa màn hình
- 5 tuyến đường ở sidebar bên phải
- Thông tin traffic real-time

**Cách sử dụng:**
1. Mở http://localhost:5173
2. Mặc định hiển thị tab "Giám Sát"
3. Click vào tên tuyến đường để xem video
4. Xem thông tin:
   - 🚗 Số xe ô tô
   - 🏍️ Số xe máy
   - ⚡ Tốc độ trung bình
   - 🚦 Trạng thái (Thông thoáng / Đông đúc / Tắc nghẽn)

**Trạng thái giao thông:**
| Tổng Xe | Trạng Thái | Màu | Icon |
|---------|-----------|-----|------|
| > 15 | Tắc nghẽn | 🔴 Đỏ | AlertTriangle |
| 8-15 | Đông đúc | 🟡 Vàng | Clock |
| < 8 | Thông thoáng | 🟢 Xanh | CheckCircle |

### 2️⃣ Tab Phân Tích (Analytics)

**4 loại biểu đồ chính:**

#### 📈 Giờ Cao Điểm / Thấp Điểm
- **Vị trí**: 2 cards đầu tiên
- **Thông tin**:
  - Giờ nào đông/vắng nhất
  - Số xe trung bình
  - Trạng thái traffic
- **Cách tính**: AVG(tổng xe) theo từng giờ

#### 📊 Xu Hướng Theo Giờ
- **Loại**: Area Chart
- **Màu sắc**: Indigo (#6366f1)
- **Trục X**: 0-23 giờ
- **Trục Y**: Số xe trung bình
- **Tương tác**: Hover để xem chi tiết

#### 📊 So Sánh Tuyến Đường
- **Loại**: Bar Chart (xếp chồng)
- **Màu sắc**:
  - 🔵 Xanh dương: Ô tô
  - 🟢 Xanh lá: Xe máy
- **Tương tác**: Click tên đường để focus

#### 📈 Biểu Đồ Xu Hướng
- **Loại**: Line Chart
- **Màu sắc**: 5 màu khác nhau (mỗi tuyến)
- **Data**: 50 điểm gần nhất
- **Update**: Real-time mỗi khi có data mới

**Export dữ liệu:**

**CSV Format:**
```csv
Time,Văn Phú Vehicles,Văn Phú Speed,Nguyễn Trãi Vehicles,...
14:30:25,12,32.5,8,28.3,...
14:30:30,13,31.8,9,29.1,...
```

**JSON Format:**
```json
{
  "exportedAt": "2025-01-06T14:30:00.000Z",
  "period": "day",
  "roads": ["Văn Phú", "Nguyễn Trãi", ...],
  "data": [...],
  "summary": {
    "hourlyStats": [...],
    "roadComparison": [...],
    "peakAnalysis": {...}
  }
}
```

### 3️⃣ Tab Trợ Lý AI (Chatbot)

**Tính năng:**
- Chat với AI về traffic
- Phân tích xu hướng
- Gợi ý tuyến đường

**Ví dụ câu hỏi:**
```
Người dùng: "Tuyến đường nào đang tắc nhất?"
AI: "Hiện tại đường Nguyễn Trãi đang có lưu lượng cao nhất với 23 xe..."

Người dùng: "Giờ nào nên đi qua Văn Phú?"
AI: "Dựa trên dữ liệu, thời gian tối ưu là 6h-7h sáng và 20h-21h tối..."

Người dùng: "So sánh traffic giữa Văn Phú và Đường Láng"
AI: "Đường Láng có lưu lượng cao hơn 35% so với Văn Phú..."
```

## 🗂️ Cấu Trúc Dự Án

```
Smart-Trafic-Monitoring-System-main/
├── Backend/
│   ├── app/
│   │   ├── api/
│   │   │   └── v1/
│   │   │       ├── api_chat.py              # Chat endpoints
│   │   │       ├── api_reports.py           # Reports & Analytics
│   │   │       ├── api_traffic.py           # Traffic monitoring
│   │   │       └── state.py                 # Shared state
│   │   ├── core/
│   │   │   ├── config.py                    # Configuration
│   │   │   └── security.py                  # JWT & Auth
│   │   ├── db/
│   │   │   └── database.py                  # Database setup
│   │   ├── models/
│   │   │   ├── traffic_record.py            # Traffic record model
│   │   │   └── user.py                      # User model
│   │   ├── schemas/
│   │   │   ├── traffic_record.py            # Pydantic schemas
│   │   │   └── ChatResponse.py              # Chat schemas
│   │   ├── services/
│   │   │   ├── road_services/               # Traffic detection
│   │   │   │   ├── AnalyzeOnRoad.py
│   │   │   │   └── AnalyzeOnRoadForMultiProcessing.py
│   │   │   └── chat_services/               # Chat logic
│   │   │       └── tool_func.py
│   │   ├── ai_models/                       # YOLO models
│   │   │   ├── model_S/                     # Small model
│   │   │   └── model_N/                     # Nano model
│   │   ├── video_test/                      # Video files
│   │   ├── utils/                           # Utilities
│   │   ├── main.py                          # FastAPI app
│   │   └── traffic_data.db                  # SQLite database
│   ├── venv/                                # Virtual environment
│   ├── requirements_cpu.txt                 # CPU dependencies
│   ├── requirements_gpu.txt                 # GPU dependencies
│   ├── Dockerfile                           # Docker config
│   └── .env                                 # Environment variables
│
├── Frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── ui/                          # Shadcn components
│   │   │   ├── TrafficDashboard.tsx         # Main dashboard
│   │   │   ├── TrafficReports.tsx           # Reports (NEW)
│   │   │   ├── TrafficAnalytics.tsx         # Analytics
│   │   │   ├── VideoMonitor.tsx             # Video display
│   │   │   ├── ChatInterface.tsx            # AI chat
│   │   │   └── LoadingSpinner.tsx           # Loading UI
│   │   ├── hooks/
│   │   │   ├── useWebSocket.ts              # WebSocket hooks
│   │   │   └── use-mobile.ts                # Mobile detection
│   │   ├── lib/
│   │   │   └── utils.ts                     # Utilities
│   │   ├── assets/                          # Images, icons
│   │   ├── config.ts                        # API config
│   │   ├── App.tsx                          # Root component
│   │   ├── App.css                          # Animations
│   │   ├── index.css                        # TailwindCSS
│   │   └── main.tsx                         # Entry point
│   ├── public/                              # Static files
│   ├── package.json                         # Dependencies
│   ├── vite.config.ts                       # Vite config
│   ├── tailwind.config.js                   # Tailwind config
│   ├── components.json                      # Shadcn config
│   └── Dockerfile                           # Docker config
│
├── docker-compose.yml                       # Docker Compose
├── TRAFFIC_REPORTS_GUIDE.md                 # Reports guide
└── README.md                                # This file
```

## 🔧 API Documentation

### REST Endpoints

#### Traffic Endpoints

**GET `/roads_name`**
- Lấy danh sách tuyến đường
```json
Response: {
  "road_names": ["Văn Phú", "Nguyễn Trãi", ...]
}
```

**GET `/info/{road_name}`**
- Lấy thông tin traffic của 1 tuyến
```json
Response: {
  "count_car": 12,
  "count_motor": 31,
  "speed_car": 32.4,
  "speed_motor": 26.1
}
```

**GET `/frames/{road_name}`**
- Lấy frame mới nhất (JPEG bytes)
- Response type: `image/jpeg`

#### Reports Endpoints (NEW)

**POST `/api/v1/reports/generate`**
- Tạo báo cáo thống kê
```json
Request: {
  "period": "day|week|month",
  "road_names": ["Văn Phú"],
  "start_date": "2025-01-01",
  "end_date": "2025-01-07"
}
Response: {
  "statistics": [...],
  "hourly_trends": [...],
  "daily_trends": [...],
  "road_comparisons": [...]
}
```

**GET `/api/v1/reports/export/csv`**
- Export dữ liệu CSV
- Query params: `road_name`, `start_date`, `end_date`

**GET `/api/v1/reports/export/json`**
- Export dữ liệu JSON
- Query params: `road_name`, `start_date`, `end_date`

#### Chat Endpoints

**POST `/chat`**
- Gửi tin nhắn cho AI
```json
Request: {
  "message": "Tuyến nào đang tắc?"
}
Response: {
  "message": "Đường Nguyễn Trãi đang tắc...",
  "image": []
}
```

### WebSocket Endpoints

**WS `/ws/frames/{road_name}`**
- Stream video frames (15 FPS)
- Binary: JPEG bytes

**WS `/ws/info/{road_name}`**
- Stream traffic info (5s interval)
```json
{
  "count_car": 12,
  "count_motor": 31,
  "speed_car": 32.4,
  "speed_motor": 26.1
}
```

**WS `/chat`**
- Chat WebSocket
```json
Request: { "message": "string" }
Response: { "message": "string", "image": [] }
```

### Example Usage

```bash
# Get roads
curl http://localhost:8000/roads_name

# Get traffic info
curl http://localhost:8000/info/"Văn Phú"

# Get frame
curl http://localhost:8000/frames/"Văn Phú" --output frame.jpg

# Send chat
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"message":"Traffic on Văn Phú?"}'

# Export CSV
curl "http://localhost:8000/api/v1/reports/export/csv?road_name=Văn Phú" --output report.csv
```

## 🐛 Xử Lý Lỗi Thường Gặp

### ❌ Lỗi 1: ModuleNotFoundError

**Triệu chứng:**
```
ModuleNotFoundError: No module named 'sqlalchemy'
```

**Nguyên nhân:** Chưa cài dependencies

**Giải pháp:**
```bash
cd Backend
pip install sqlalchemy python-dotenv
# Hoặc cài lại toàn bộ
pip install -r requirements_cpu.txt
```

### ❌ Lỗi 2: Port Already in Use

**Triệu chứng:**
```
ERROR: [Errno 10048] error while attempting to bind on address ('0.0.0.0', 8000)
```

**Giải pháp Windows:**
```bash
# Tìm process đang dùng port
netstat -ano | findstr :8000

# Kill process (thay <PID>)
taskkill /PID <PID> /F
```

**Giải pháp Linux/Mac:**
```bash
# Kill process trên port 8000
lsof -ti:8000 | xargs kill -9

# Hoặc đổi port
uvicorn main:app --port 8001
```

### ❌ Lỗi 3: CORS Error

**Triệu chứng:**
```
Access to fetch at 'http://localhost:8000' has been blocked by CORS policy
```

**Giải pháp:**
```python
# Backend/app/main.py
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Thêm origin Frontend
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### ❌ Lỗi 4: Video Not Found

**Triệu chứng:**
```
FileNotFoundError: [Errno 2] No such file or directory: 'video_test/Văn Phú.mp4'
```

**Giải pháp:**
```bash
# Tải video từ Google Drive
cd Backend/app
pip install gdown
gdown --folder https://drive.google.com/drive/folders/1gkac5U5jEs174p7V7VC3rCmgvO_cVwxH

# Kiểm tra files
ls video_test/
```

### ❌ Lỗi 5: Google API Key Invalid

**Triệu chứng:**
```
Error: Invalid API key
```

**Giải pháp:**
1. Truy cập https://aistudio.google.com/app/apikey
2. Tạo key mới
3. Cập nhật `Backend/.env`:
```env
GOOGLE_API_KEY=AIzaSyA_...
```
4. Restart Backend

### ❌ Lỗi 6: pnpm Not Found

**Triệu chứng:**
```
'pnpm' is not recognized as an internal or external command
```

**Giải pháp:**
```bash
# Cài pnpm global
npm install -g pnpm

# Hoặc dùng npm
cd Frontend
npm install
npm run dev
```

### ❌ Lỗi 7: Frontend Cannot Connect Backend

**Triệu chứng:**
- Frontend load nhưng không có data
- Console error: `WebSocket connection failed`

**Giải pháp:**
```typescript
// Frontend/src/config.ts
export const endpoints = {
  base: "http://localhost:8000",  // Check port
  ws: "ws://localhost:8000",      // Check protocol
}
```

### ❌ Lỗi 8: OpenVINO Import Error

**Triệu chứng:**
```
ImportError: cannot import name 'Core' from 'openvino'
```

**Giải pháp:**
```bash
pip uninstall openvino openvino-dev
pip install openvino==2024.0
```

## 🔧 Cấu Hình Nâng Cao

### Thêm Tuyến Đường Mới

**Bước 1:** Thêm video
```bash
# Copy video vào folder
cp your_video.mp4 Backend/app/video_test/"Tên Đường Mới.mp4"
```

**Bước 2:** Restart Backend
- Backend tự động phát hiện video mới
- Frontend tự động hiển thị

### Thay Đổi Model YOLO

```python
# Backend/app/services/road_services/AnalyzeOnRoad.py
model_path = "ai_models/model_N"  # Đổi sang model_N (nhẹ hơn)
# hoặc
model_path = "ai_models/model_S"  # model_S (chính xác hơn)
```

### Tối Ưu Hiệu Năng

**Tăng FPS xử lý:**
```python
# Backend/app/services/road_services/AnalyzeOnRoad.py
frame_skip = 3  # Giảm để xử lý nhiều frame hơn (default: 5)
```

**Giảm độ trễ WebSocket:**
```python
# Backend/app/api/v1/api_traffic.py
await asyncio.sleep(0.033)  # ~30 FPS (default: 1/15 = ~15 FPS)
```

**Tăng số điểm lưu trữ:**
```typescript
// Frontend/src/components/TrafficReports.tsx
setHistoricalData((prev) => [...prev, newPoint].slice(-100));  // default: 50
```

### Đổi Database Sang PostgreSQL

```bash
# Cài driver
pip install psycopg2-binary
```

```env
# Backend/.env
DATABASE_URL=postgresql://user:password@localhost:5432/traffic_db
```

```python
# Backend/app/db/database.py
# Code tự động hỗ trợ PostgreSQL
```

## 📊 Giám Sát Hệ Thống

### Health Check

```bash
# Check Backend health
curl http://localhost:8000/health

# Check Frontend
curl http://localhost:5173
```

### Monitor Logs

**Backend:**
```bash
# Real-time logs
cd Backend/app
python -m uvicorn main:app --log-level debug

# Save to file
python -m uvicorn main:app > backend.log 2>&1
```

**Frontend:**
```bash
# Real-time logs trong terminal
pnpm run dev

# Build size analysis
pnpm run build
```

### Performance Monitoring

**Backend:**
- API docs: http://localhost:8000/docs
- Measure response time
- Monitor CPU/RAM usage

**Frontend:**
- React DevTools
- Network tab (F12)
- Lighthouse audit

## 🤝 Đóng Góp

### Quy Trình

1. Fork repository
2. Tạo branch: `git checkout -b feature/amazing`
3. Commit: `git commit -m 'Add feature'`
4. Push: `git push origin feature/amazing`
5. Tạo Pull Request

### Code Style

**Python (PEP 8):**
```python
# Use type hints
def process_frame(frame: np.ndarray) -> Dict[str, int]:
    """Process frame and return vehicle counts"""
    pass

# Docstrings
def calculate_speed(distance: float, time: float) -> float:
    """
    Calculate speed from distance and time.

    Args:
        distance: Distance in meters
        time: Time in seconds

    Returns:
        Speed in km/h
    """
    return (distance / time) * 3.6
```

**TypeScript:**
```typescript
// Use strict mode
interface TrafficData {
  count_car: number;
  count_motor: number;
  speed_car: number;
  speed_motor: number;
}

// Props typing
interface Props {
  trafficData: TrafficData;
  allowedRoads: string[];
}
```

## 📝 Changelog

### Version 2.1 (2025-01-06) - LATEST
- ✨ Thêm hệ thống báo cáo thống kê hoàn chỉnh
- ✨ Export CSV/JSON functionality
- ✨ Giờ cao điểm / thấp điểm analysis
- ✨ 4 loại biểu đồ: Area, Bar, Line, Pie
- 🎨 Dark theme với OKLCH color space
- 🎨 Glass morphism UI effects
- 🎨 Framer Motion animations
- 🗄️ SQLite database integration
- 📊 Real-time data collection (50 points)

### Version 2.0 (2025-01-05)
- ✨ Thêm TrafficAnalytics component
- 🤖 Tích hợp Google Gemini chatbot
- 🎨 Cải thiện UI/UX
- 🐛 Fix WebSocket stability issues

### Version 1.0 (2024-12)
- 🎉 Initial release
- 🎥 Traffic monitoring real-time
- 🤖 YOLO detection + ByteTrack
- 📡 WebSocket streaming
- 📊 Basic analytics

## 📄 License

MIT License - Xem file LICENSE

## 👥 Credits

**Developers:**
- **Doan Ba  Trí** - Main Developer

**Acknowledgments:**
- OpenVINO team - Optimization tools
- Ultralytics - YOLO models
- FastAPI community
- React ecosystem
- Shadcn/ui - UI components

## 📞 Liên Hệ & Hỗ Trợ

- **GitHub Issues**: [Create an issue](https://github.com/yourusername/repo/issues)
- **Documentation**:
  - `TRAFFIC_REPORTS_GUIDE.md` - Hướng dẫn tính năng báo cáo
  - `README.md` - File này
- **API Docs**: http://localhost:8000/docs (khi chạy Backend)

## 🎓 Use Cases

### Cho Ban Quản Lý Giao Thông
- Xác định giờ cao điểm để bố trí CSGT
- Lập lịch bảo trì đường vào giờ thấp điểm
- Điều chỉnh đèn tín hiệu thông minh
- Phân tích xu hướng để lập kế hoạch dài hạn

### Cho Công Ty Vận Tải
- Tránh tuyến đường tắc nghẽn
- Lên lịch xe trong giờ thấp điểm
- Tối ưu route delivery
- Dự đoán thời gian di chuyển

### Cho Nghiên Cứu
- Thu thập data cho AI models
- Phân tích pattern giao thông
- Publish papers về smart city
- Training deep learning models

---

**Made with ❤️ for Smart Traffic Monitoring System**

*Last updated: 2025-01-06*
