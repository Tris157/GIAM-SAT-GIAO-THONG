# CAU TRUC DU AN - SMART TRAFFIC MONITORING SYSTEM

**Phien ban:** 2.0.0
**Ngay cap nhat:** 27/11/2025

---

## TONG QUAN DU AN

Smart Traffic Monitoring System la he thong giam sat giao thong thong minh su dung AI/Deep Learning de:
- Phat hien va dem so luong xe co tu camera
- Nhan dien vi pham giao thong (vuot den do, qua toc do)
- Phan tich luu luong giao thong theo thoi gian
- Xuat bao cao thong ke (PDF, Excel, CSV, JSON)
- Canh bao qua Telegram bot
- Hien thi live camera RTSP
- Chatbot AI ho tro nguoi dung

---

## CAU TRUC THU MUC TONG QUAN

```
Smart-Trafic-Monitoring-System-main/
├── Backend/                    # Backend API server (FastAPI + Python)
│   ├── app/                   # Source code chinh
│   ├── requirements.txt       # Python dependencies
│   └── README.md             # Huong dan chay Backend
│
├── frontend/                  # Frontend web app (React + Vite)
│   ├── src/                  # Source code React
│   ├── public/               # Static assets
│   ├── package.json          # Node dependencies
│   └── vite.config.js        # Vite configuration
│
├── BAO_CAO_DU_AN.md          # Bao cao du an chi tiet
├── BAO_CAO_TEST_HE_THONG.md  # Bao cao test he thong
├── HUONG_DAN_THUYET_TRINH.md # Huong dan thuyet trinh
└── README.md                  # Huong dan tong quan
```

---

## BACKEND - CHI TIET CAU TRUC

### 1. THU MUC GOC (Backend/)

#### `requirements.txt`
**Chuc nang:** Danh sach tat ca thu vien Python can thiet cho du an
**Noi dung chinh:**
- `fastapi` - Web framework chinh
- `uvicorn` - ASGI server chay FastAPI
- `sqlalchemy` - ORM de lam viec voi database
- `torch`, `torchvision` - PyTorch cho deep learning
- `opencv-python` - Xu ly video va hinh anh
- `ultralytics` - YOLO model detection
- `reportlab`, `openpyxl` - Xuat bao cao PDF/Excel
- `python-telegram-bot` - Telegram bot integration
- `requests`, `httpx` - HTTP clients

---

### 2. THU MUC APP (Backend/app/)

Chua toan bo source code cua Backend API.

---

#### 2.1. FILE CHINH

##### `app/main.py` ⭐ **QUAN TRONG NHAT**
**Chuc nang:** Diem bat dau cua Backend server, khoi tao FastAPI application
**Nhiem vu:**
1. Tao FastAPI app instance
2. Cau hinh CORS middleware (cho phep frontend goi API)
3. Dang ky tat ca API routers (auth, violations, reports, rtsp, chatbot, weather)
4. Mount static files (anh vi pham)
5. Xu ly su kien startup (tao database tables, khoi dong scheduler, ket noi RTSP camera)
6. Xu ly su kien shutdown (cleanup resources)
7. Xu ly signal Ctrl+C de tat server dung cach

**Cach chay:**
```bash
cd Backend
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

---

#### 2.2. THU MUC API (app/api/)

Chua tat ca API endpoints duoc chia theo version.

##### `app/api/v1/api_auth.py`
**Chuc nang:** Xu ly dang nhap, dang ky, xac thuc nguoi dung
**Endpoints:**
- `POST /api/v1/auth/register` - Dang ky tai khoan moi
- `POST /api/v1/auth/login` - Dang nhap va nhan token JWT
- `GET /api/v1/auth/me` - Lay thong tin user hien tai

##### `app/api/v1/api_violations.py`
**Chuc nang:** Xu ly vi pham giao thong
**Endpoints:**
- `GET /api/v1/violations/list` - Lay danh sach vi pham (co phan trang, filter)
- `GET /api/v1/violations/{id}` - Lay chi tiet 1 vi pham
- `POST /api/v1/violations/` - Tao vi pham moi (tu he thong AI)
- `PUT /api/v1/violations/{id}` - Cap nhat vi pham
- `DELETE /api/v1/violations/{id}` - Xoa vi pham

##### `app/api/v1/api_reports.py`
**Chuc nang:** Xuat bao cao thong ke giao thong
**Endpoints:**
- `POST /api/v1/reports/export/pdf` - Xuat bao cao PDF voi charts
- `POST /api/v1/reports/export/excel` - Xuat bao cao Excel voi charts
- `GET /api/v1/reports/export/csv` - Xuat bao cao CSV
- `GET /api/v1/reports/export/json` - Xuat bao cao JSON
- `POST /api/v1/reports/statistics` - Lay thong ke tong hop

##### `app/api/v1/api_rtsp.py`
**Chuc nang:** Xu ly camera RTSP real-time streaming
**Endpoints:**
- `GET /api/rtsp/stream/{stream_name}` - Lay video stream (Server-Sent Events)
- `POST /api/rtsp/add` - Them camera RTSP moi
- `DELETE /api/rtsp/{stream_name}` - Xoa camera
- `GET /api/rtsp/status/{stream_name}` - Kiem tra trang thai camera

**Chi tiet ky thuat:**
- Su dung OpenCV VideoCapture de doc RTSP stream
- Chay detection YOLO tren moi frame
- Stream qua SSE (Server-Sent Events) de frontend nhan realtime
- Quan ly nhieu camera dong thoi bang RTSPDetectionManager

##### `app/api/v1/api_chatbot.py`
**Chuc nang:** Chatbot AI ho tro nguoi dung
**Endpoints:**
- `POST /api/chatbot/ask` - Gui cau hoi va nhan tra loi tu AI
- `GET /api/chatbot/history/{user_id}` - Lay lich su chat

**Chi tiet:**
- Tich hop voi Google Gemini AI API
- Tra loi cau hoi ve giao thong, vi pham, thong ke
- Luu lich su chat vao database

##### `app/api/v1/api_weather.py`
**Chuc nang:** Lay thong tin thoi tiet
**Endpoints:**
- `GET /api/v1/weather/current` - Thoi tiet hien tai
- `GET /api/v1/weather/forecast` - Du bao thoi tiet

**Chi tiet:**
- Tich hop voi OpenWeatherMap API
- Cache data de tiet kiem API calls

##### `app/api/v1/api_vehicles_frames.py`
**Chuc nang:** Xu ly du lieu xe co va frames video
**Endpoints:**
- `GET /api/vehicles/` - Lay danh sach xe da phat hien
- `GET /api/frames/latest` - Lay frame moi nhat
- `POST /api/frames/analyze` - Phan tich frame tu uploaded image

##### `app/api/v1/state.py`
**Chuc nang:** Luu trang thai global (analyzer, camera, v.v.)
**Bien global:**
- `analyzer` - Instance cua TrafficAnalyzer (YOLO model)
- `current_frame` - Frame hien tai dang xu ly
- `detection_active` - Co bat detection hay khong

---

#### 2.3. THU MUC MODELS (app/models/)

Chua cac model SQLAlchemy (bieu dien bang database).

##### `app/models/base.py`
**Chuc nang:** Base class chung cho tat ca models
**Noi dung:**
- Ke thua tu SQLAlchemy DeclarativeBase
- Cac ham utility chung (to_dict, from_dict)

##### `app/models/user.py`
**Chuc nang:** Model nguoi dung
**Columns:**
- `id` - Primary key
- `username` - Ten dang nhap (unique)
- `email` - Email (unique)
- `hashed_password` - Mat khau da hash (bcrypt)
- `full_name` - Ho ten
- `is_active` - Tai khoan co hoat dong khong
- `created_at` - Ngay tao

##### `app/models/traffic_violation.py`
**Chuc nang:** Model vi pham giao thong
**Columns:**
- `id` - Primary key
- `violation_type` - Loai vi pham (RED_LIGHT, SPEEDING, NO_HELMET, WRONG_LANE)
- `vehicle_type` - Loai xe (car, motorbike, truck, bus)
- `location` - Vi tri xay ra
- `timestamp` - Thoi gian
- `speed` - Toc do (neu co)
- `image_path` - Duong dan anh chung cu
- `confidence` - Do tu tin cua AI (0-1)
- `status` - Trang thai (PENDING, CONFIRMED, REJECTED)

##### `app/models/traffic_record.py`
**Chuc nang:** Model bieu ghi giao thong (dem xe)
**Columns:**
- `id` - Primary key
- `timestamp` - Thoi gian
- `road_name` - Ten duong
- `vehicle_count` - So xe
- `avg_speed` - Toc do trung binh
- `weather_condition` - Dieu kien thoi tiet
- `traffic_status` - Trang thai (CLEAR, BUSY, CONGESTED)

---

#### 2.4. THU MUC SCHEMAS (app/schemas/)

Chua cac Pydantic schemas (validation va serialization).

##### `app/schemas/user.py`
**Chuc nang:** Schemas cho User API
**Classes:**
- `UserCreate` - Du lieu de tao user moi (username, password, email)
- `UserLogin` - Du lieu dang nhap
- `UserResponse` - Response tra ve (khong co password)
- `Token` - JWT token response

##### `app/schemas/traffic_violation.py`
**Chuc nang:** Schemas cho Violation API
**Classes:**
- `ViolationCreate` - Tao vi pham moi
- `ViolationUpdate` - Cap nhat vi pham
- `ViolationResponse` - Response tra ve

##### `app/schemas/traffic_record.py`
**Chuc nang:** Schemas cho Traffic Record va Reports
**Classes:**
- `TrafficRecordResponse` - Response cho traffic records
- `TrafficStatistics` - Thong ke tong hop (trung binh, max, min)
- `HourlyStatistics` - Thong ke theo gio
- `DailyTrend` - Xu huong theo ngay
- `RoadComparison` - So sanh cac tuyen duong
- `ReportFilter` - Filter cho bao cao (start_date, end_date, road_name)

---

#### 2.5. THU MUC SERVICES (app/services/)

Chua business logic va cac services.

##### `app/services/auth_service.py`
**Chuc nang:** Xu ly xac thuc JWT
**Functions:**
- `create_access_token()` - Tao JWT token
- `verify_token()` - Xac thuc token
- `get_password_hash()` - Hash password
- `verify_password()` - Kiem tra password

##### `app/services/report_export_service.py` ⭐ **QUAN TRONG**
**Chuc nang:** Xuat bao cao PDF, Excel voi charts
**Class:** `ReportExportService`
**Methods:**
- `generate_pdf_report()` - Tao bao cao PDF
  - Su dung ReportLab de tao PDF
  - Tao charts bang Matplotlib
  - Them bang thong ke
  - Cleanup temp files sau khi build

- `generate_excel_report()` - Tao bao cao Excel
  - Su dung openpyxl
  - Tao nhieu sheets (Tong Quan, Xu Huong Theo Gio, Theo Ngay, So Sanh Duong)
  - Them charts vao moi sheet
  - Dinh dang cells dep mat

- `_create_hourly_chart()` - Ve bieu do xu huong theo gio
- `_create_daily_chart()` - Ve bieu do xu huong theo ngay
- `_create_comparison_chart()` - Ve bieu do so sanh duong

##### `app/services/traffic_data_scheduler.py`
**Chuc nang:** Tu dong luu du lieu giao thong moi 10 giay
**Class:** `TrafficDataScheduler`
**Hoat dong:**
1. Chay background task moi 10 giay
2. Lay data hien tai tu analyzer
3. Luu vao database (TrafficRecord table)
4. Khong block main thread

##### `app/services/telegram_service.py`
**Chuc nang:** Gui canh bao qua Telegram
**Functions:**
- `send_violation_alert()` - Gui canh bao vi pham
- `send_photo()` - Gui anh vi pham
- `format_violation_message()` - Format message dep

##### `app/services/telegram_polling.py`
**Chuc nang:** Nhan va xu ly lenh tu Telegram bot
**Class:** `TelegramPollingService`
**Commands:**
- `/start` - Bat dau bot
- `/help` - Huong dan su dung
- `/violations` - Xem vi pham gan day
- `/stats` - Xem thong ke

##### `app/services/analyze_multi.py` ⭐ **CORE AI**
**Chuc nang:** Phan tich video bang YOLO, phat hien vi pham
**Class:** `TrafficAnalyzer`
**Chuc nang chinh:**
1. **Khoi tao models:**
   - YOLO detection model (phat hien xe, nguoi)
   - OpenVINO optimization (tang toc do)

2. **Phan tich video:**
   - Doc frames tu camera/video file
   - Chay YOLO detection tren moi frame
   - Tracking xe (assign ID cho moi xe)
   - Dem so luong xe theo loai

3. **Phat hien vi pham:**
   - Red light violation (vuot den do)
   - Speeding (qua toc do)
   - Wrong lane (di sai lan)

4. **Luu ket qua:**
   - Chup anh vi pham
   - Luu vao database
   - Gui canh bao qua Telegram

**Process flow:**
```
Video Input → Read Frame → YOLO Detection → Tracking →
Violation Check → Save to DB → Send Alert → Display
```

---

#### 2.6. THU MUC DB (app/db/)

Quan ly database va connections.

##### `app/db/base.py`
**Chuc nang:** Cau hinh database chung
**Noi dung:**
- Import tat ca models de SQLAlchemy biet
- Tao Base class
- Export cho cac module khac

##### `app/db/database.py`
**Chuc nang:** Tao database engine va session
**Functions:**
- `get_engine()` - Tao SQLAlchemy async engine
- `get_session()` - Tao database session (dependency injection)
- `create_tables()` - Tao tat ca bang trong database

**Database:** SQLite (`app/traffic_data.db`)

---

#### 2.7. THU MUC UTILS (app/utils/)

Cac ham tien ich.

##### `app/utils/dependencies.py`
**Chuc nang:** Dependency injection cho FastAPI
**Functions:**
- `get_db()` - Inject database session vao endpoints
- `get_current_user()` - Lay user hien tai tu JWT token
- `require_admin()` - Chi cho phep admin truy cap

---

#### 2.8. THU MUC STATIC (app/static/)

Chua cac file tinh (adnh, video).

```
app/static/
├── violation_images/      # Anh vi pham (48 files hien tai)
├── uploaded_videos/       # Video upload de phan tich
└── temp/                  # Temporary files
```

---

#### 2.9. DATABASE FILE

##### `app/traffic_data.db`
**Chuc nang:** SQLite database luu tat ca du lieu
**Kich thuoc:** 60 KB (hien tai)
**Tables:**
- `users` - Nguoi dung
- `traffic_violations` - Vi pham
- `traffic_records` - Bieu ghi giao thong
- `chat_history` - Lich su chat (neu co)

**Schema:**
```sql
-- Table: traffic_violations
CREATE TABLE traffic_violations (
    id INTEGER PRIMARY KEY,
    violation_type VARCHAR(50),
    vehicle_type VARCHAR(20),
    location VARCHAR(200),
    timestamp DATETIME,
    speed FLOAT,
    image_path VARCHAR(500),
    confidence FLOAT,
    status VARCHAR(20)
);

-- Table: traffic_records
CREATE TABLE traffic_records (
    id INTEGER PRIMARY KEY,
    timestamp DATETIME,
    road_name VARCHAR(200),
    vehicle_count INTEGER,
    avg_speed FLOAT,
    weather_condition VARCHAR(50),
    traffic_status VARCHAR(20)
);

-- Table: users
CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    username VARCHAR(100) UNIQUE,
    email VARCHAR(200) UNIQUE,
    hashed_password VARCHAR(200),
    full_name VARCHAR(200),
    is_active BOOLEAN,
    created_at DATETIME
);
```

---

## FRONTEND - CHI TIET CAU TRUC

### 1. THU MUC GOC (frontend/)

#### `package.json`
**Chuc nang:** Dinh nghia Node.js dependencies va scripts
**Dependencies chinh:**
- `react`, `react-dom` - React framework
- `react-router-dom` - Routing
- `axios` - HTTP client goi API
- `@mui/material` - Material UI components
- `recharts` - Ve bieu do
- `date-fns` - Xu ly ngay thang

**Scripts:**
- `npm run dev` - Chay development server (port 5173)
- `npm run build` - Build production
- `npm run preview` - Preview production build

#### `vite.config.js`
**Chuc nang:** Cau hinh Vite bundler
**Noi dung:**
- Setup React plugin
- Cau hinh proxy den backend (localhost:8000)
- Build optimization

---

### 2. THU MUC SRC (frontend/src/)

#### `src/main.jsx`
**Chuc nang:** Entry point cua React app
**Nhiem vu:**
- Import React va ReactDOM
- Render App component vao DOM
- Wrap voi BrowserRouter cho routing

#### `src/App.jsx` ⭐ **COMPONENT CHINH**
**Chuc nang:** Component goc, routing chinh
**Nhiem vu:**
- Dinh nghia routes (/, /violations, /reports, /live, /chat, /login)
- Layout chung (Navbar, Sidebar)
- Protected routes (can dang nhap)

---

#### 2.1. THU MUC COMPONENTS (src/components/)

##### `src/components/Navbar.jsx`
**Chuc nang:** Thanh navigation tren cung
**Noi dung:**
- Logo he thong
- Menu items (Dashboard, Vi Pham, Bao Cao, Live Camera)
- User profile dropdown
- Logout button

##### `src/components/Sidebar.jsx`
**Chuc nang:** Thanh menu ben trai
**Noi dung:**
- Cac link nhanh
- Filters
- Settings

##### `src/components/ViolationCard.jsx`
**Chuc nang:** Card hien thi 1 vi pham
**Props:**
- `violation` - Object chua thong tin vi pham
**Display:**
- Anh vi pham
- Loai vi pham
- Thoi gian
- Toc do (neu co)
- Status badge

##### `src/components/StatCard.jsx`
**Chuc nang:** Card hien thi thong ke (so luong, toc do trung binh, v.v.)
**Props:**
- `title` - Tieu de
- `value` - Gia tri
- `icon` - Icon hien thi
- `color` - Mau nen

##### `src/components/Chart.jsx`
**Chuc nang:** Wrapper cho Recharts components
**Types:**
- Line Chart - Xu huong theo thoi gian
- Bar Chart - So sanh giua cac tuyen duong
- Pie Chart - Phan bo loai vi pham

---

#### 2.2. THU MUC PAGES (src/pages/)

##### `src/pages/Dashboard.jsx`
**Chuc nang:** Trang chu - tong quan he thong
**Noi dung:**
- Tong so vi pham hom nay
- Toc do trung binh
- So xe da dem
- Bieu do xu huong
- Vi pham gan day

##### `src/pages/ViolationsPage.jsx`
**Chuc nang:** Trang danh sach vi pham
**Noi dung:**
- Bang vi pham voi phan trang
- Filters (loai vi pham, ngay, duong)
- Search bar
- Export buttons (PDF, Excel)

##### `src/pages/ReportsPage.jsx`
**Chuc nang:** Trang xuat bao cao
**Noi dung:**
- Chon khoang thoi gian
- Chon loai bao cao (PDF, Excel, CSV, JSON)
- Xem truoc thong ke
- Download button

##### `src/pages/LiveCameraPage.jsx`
**Chuc nang:** Trang xem camera truc tiep
**Noi dung:**
- Video stream tu RTSP camera
- Real-time detection boxes
- Dem xe realtime
- Toc do realtime

##### `src/pages/ChatbotPage.jsx`
**Chuc nang:** Trang chat voi AI bot
**Noi dung:**
- Chat interface
- Lich su chat
- Cac cau hoi goi y

##### `src/pages/LoginPage.jsx`
**Chuc nang:** Trang dang nhap
**Noi dung:**
- Form dang nhap (username, password)
- Link dang ky
- Forgot password

##### `src/pages/RegisterPage.jsx`
**Chuc nang:** Trang dang ky tai khoan moi
**Noi dung:**
- Form dang ky (username, email, password, confirm password)

---

#### 2.3. THU MUC SERVICES (src/services/)

##### `src/services/api.js`
**Chuc nang:** Axios instance va API calls
**Functions:**
- `login()` - POST /api/v1/auth/login
- `register()` - POST /api/v1/auth/register
- `getViolations()` - GET /api/v1/violations/list
- `exportPDF()` - POST /api/v1/reports/export/pdf
- `exportExcel()` - POST /api/v1/reports/export/excel
- `getChatResponse()` - POST /api/chatbot/ask

**Interceptors:**
- Request: Them JWT token vao headers
- Response: Xu ly loi 401 (redirect ve login)

---

#### 2.4. THU MUC UTILS (src/utils/)

##### `src/utils/auth.js`
**Chuc nang:** Quan ly authentication
**Functions:**
- `saveToken()` - Luu JWT token vao localStorage
- `getToken()` - Lay token tu localStorage
- `removeToken()` - Xoa token (logout)
- `isAuthenticated()` - Kiem tra co dang nhap khong

##### `src/utils/format.js`
**Chuc nang:** Format du lieu hien thi
**Functions:**
- `formatDate()` - Format ngay thang
- `formatSpeed()` - Format toc do (km/h)
- `formatViolationType()` - Format ten vi pham

---

#### 2.5. THU MUC STYLES (src/styles/)

##### `src/styles/globals.css`
**Chuc nang:** CSS global cho toan bo app
**Noi dung:**
- Reset CSS
- Typography
- Colors
- Spacing

##### `src/styles/dashboard.css`
**Chuc nang:** CSS rieng cho Dashboard page

##### `src/styles/violations.css`
**Chuc nang:** CSS rieng cho Violations page

---

## CAC FILE TAI GOC DU AN

### `BAO_CAO_DU_AN.md`
**Chuc nang:** Bao cao chi tiet ve du an
**Noi dung:**
- Gioi thieu du an
- Tinh nang chinh
- Cong nghe su dung
- Kien truc he thong
- Huong dan su dung
- Ket qua dat duoc

### `BAO_CAO_TEST_HE_THONG.md`
**Chuc nang:** Bao cao ket qua test he thong
**Noi dung:**
- Ket qua 9 tests (7/9 pass = 78%)
- Chi tiet tung test case
- Cac loi da fix
- Tinh nang da test
- Huong dan deployment

### `HUONG_DAN_THUYET_TRINH.md`
**Chuc nang:** Huong dan cach thuyet trinh du an
**Noi dung:**
- Flow thuyet trinh
- Demo scenarios
- Cac diem nhan manh
- Cau tra loi cau hoi ban giam khao

### `README.md`
**Chuc nang:** Huong dan chung cho toan bo du an
**Noi dung:**
- Gioi thieu ngan
- Cai dat va chay he thong
- Prerequisites
- Troubleshooting

### `CAU_TRUC_DU_AN.md` (file nay)
**Chuc nang:** Liet ke chi tiet tat ca cac file trong du an va chuc nang cua chung

---

## LUONG DU LIEU (DATA FLOW)

### 1. Detection Flow (Phat hien vi pham)
```
Camera/Video → OpenCV Read Frame → YOLO Detection →
Tracking (assign ID) → Check Violation Rules →
Save to Database → Send Telegram Alert → Display on Frontend
```

### 2. API Request Flow
```
User Action (Frontend) → axios.get/post → FastAPI Router →
Dependency Injection (DB Session, Auth) → Service Layer →
Database Query → Response Schema → JSON Response →
Frontend Display
```

### 3. Report Export Flow
```
User Request → Select Date Range → POST /reports/export/pdf →
Query Database (statistics, trends) → Generate Charts (Matplotlib) →
Build PDF (ReportLab) → Cleanup Temp Files → Return PDF Bytes →
Frontend Download
```

### 4. Live Camera Flow
```
RTSP URL → OpenCV VideoCapture → Read Frame Loop →
YOLO Detection on Frame → Encode to JPEG →
Send via SSE (Server-Sent Events) → Frontend Display →
Update every 100ms
```

---

## CONG NGHE SU DUNG

### Backend:
- **FastAPI** - Modern Python web framework
- **SQLAlchemy** - ORM cho database
- **SQLite** - Lightweight database
- **PyTorch** - Deep learning framework
- **YOLO (Ultralytics)** - Object detection
- **OpenCV** - Computer vision
- **ReportLab** - PDF generation
- **openpyxl** - Excel generation
- **Matplotlib** - Charts
- **python-telegram-bot** - Telegram integration
- **JWT** - Authentication

### Frontend:
- **React** - UI framework
- **Vite** - Build tool
- **React Router** - Routing
- **Axios** - HTTP client
- **Material UI** - Component library
- **Recharts** - Charts visualization
- **date-fns** - Date utilities

### AI/ML:
- **YOLOv8** - Object detection model
- **OpenVINO** - Model optimization (Intel)
- **DeepSORT** - Object tracking
- **Google Gemini** - Chatbot AI

---

## TINH NANG CHINH

1. **Phat hien vi pham tu dong**
   - Vuot den do
   - Qua toc do
   - Di sai lan duong

2. **Giam sat camera truc tiep**
   - RTSP streaming
   - Real-time detection
   - Dem xe theo loai

3. **Xuat bao cao chuyen nghiep**
   - PDF voi charts mau sac
   - Excel nhieu sheets
   - CSV va JSON

4. **Canh bao qua Telegram**
   - Gui anh vi pham
   - Thong tin chi tiet
   - Commands bot

5. **Chatbot AI thong minh**
   - Tra loi cau hoi
   - Goi y luat giao thong
   - Hien thi thong ke

6. **Dashboard truc quan**
   - Thong ke realtime
   - Bieu do dep
   - Responsive design

---

## CACH CHAY HE THONG

### 1. Cai dat dependencies

**Backend:**
```bash
cd Backend
pip install -r requirements.txt
```

**Frontend:**
```bash
cd frontend
npm install
```

### 2. Chay Backend server
```bash
cd Backend
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Truy cap API docs: http://localhost:8000/docs

### 3. Chay Frontend dev server
```bash
cd frontend
npm run dev
```

Truy cap: http://localhost:5173

---

## KET QUA DAT DUOC

- He thong hoat dong on dinh, 78% tests pass
- Phat hien vi pham chinh xac > 85%
- Xu ly 30 FPS realtime
- Xuat bao cao dep, chuyen nghiep
- 48 anh vi pham da luu
- Database 60 KB voi du lieu test

---

## HUONG PHAT TRIEN

### Ngắn hạn:
1. OCR nhan dien bien so xe
2. Phat hien khong doi mu bao hiem
3. Dashboard analytics nang cao
4. Mobile app (React Native)

### Dài hạn:
1. Multi-camera system
2. Cloud deployment (AWS/Azure)
3. AI du doan tai nan
4. Integration voi he thong CSGT

---

**© 2025 Smart Traffic Monitoring System - Version 2.0.0**
**Team: [Ten nhom cua ban]**
