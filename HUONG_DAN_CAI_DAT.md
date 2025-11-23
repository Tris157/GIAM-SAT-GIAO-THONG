# 🚀 HƯỚNG DẪN CÀI ĐẶT VÀ CHẠY DỰ ÁN

## 📋 MỤC LỤC
1. [Yêu cầu hệ thống](#yêu-cầu-hệ-thống)
2. [Cài đặt công cụ cần thiết](#cài-đặt-công-cụ-cần-thiết)
3. [Clone dự án](#clone-dự-án)
4. [Cài đặt Backend](#cài-đặt-backend)
5. [Cài đặt Frontend](#cài-đặt-frontend)
6. [Chạy dự án](#chạy-dự-án)
7. [Xử lý lỗi thường gặp](#xử-lý-lỗi-thường-gặp)

---

## 🖥️ YÊU CẦU HỆ THỐNG

### Tối thiểu:
- **CPU**: Intel Core i5 hoặc tương đương
- **RAM**: 8GB
- **Ổ cứng**: 5GB trống
- **GPU**: Không bắt buộc (nhưng khuyên dùng cho AI)
- **OS**: Windows 10/11, macOS 10.15+, Linux Ubuntu 18.04+

### Khuyên dùng:
- **CPU**: Intel Core i7 hoặc AMD Ryzen 7
- **RAM**: 16GB
- **GPU**: NVIDIA GTX 1660 trở lên (có CUDA)
- **Ổ cứng**: SSD với 10GB trống

---

## 🔧 CÀI ĐẶT CÔNG CỤ CẦN THIẾT

### 1. Python 3.11+

**Windows:**
```bash
# Tải từ python.org
https://www.python.org/downloads/

# Hoặc dùng Chocolatey
choco install python --version=3.11
```

**macOS:**
```bash
brew install python@3.11
```

**Linux:**
```bash
sudo apt update
sudo apt install python3.11 python3.11-venv python3-pip
```

**Kiểm tra:**
```bash
python --version
# Kết quả: Python 3.11.x
```

### 2. Node.js 18+ và npm

**Windows/macOS:**
```bash
# Tải từ nodejs.org
https://nodejs.org/

# Hoặc dùng nvm (khuyên dùng)
nvm install 18
nvm use 18
```

**Linux:**
```bash
curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
sudo apt-get install -y nodejs
```

**Kiểm tra:**
```bash
node --version  # v18.x.x
npm --version   # 9.x.x
```

### 3. Git

**Windows:**
```bash
# Tải từ git-scm.com
https://git-scm.com/download/win

# Hoặc dùng Chocolatey
choco install git
```

**macOS:**
```bash
brew install git
```

**Linux:**
```bash
sudo apt install git
```

**Kiểm tra:**
```bash
git --version
```

---

## 📥 CLONE DỰ ÁN

### Từ GitHub:
```bash
# Clone repository
git clone https://github.com/your-username/Smart-Trafic-Monitoring-System.git

# Hoặc nếu đã có file ZIP, giải nén vào thư mục bạn muốn
```

### Vào thư mục dự án:
```bash
cd Smart-Trafic-Monitoring-System-main
```

### Cấu trúc thư mục:
```
Smart-Trafic-Monitoring-System-main/
├── Backend/              # Code Python FastAPI
├── Frontend/             # Code React TypeScript
├── HUONG_DAN_CAI_DAT.md # File này
└── README.md
```

---

## 🐍 CÀI ĐẶT BACKEND

### Bước 1: Tạo Virtual Environment

**Windows:**
```bash
cd Backend
python -m venv venv
venv\Scripts\activate
```

**macOS/Linux:**
```bash
cd Backend
python3 -m venv venv
source venv/bin/activate
```

**Khi kích hoạt thành công**, bạn sẽ thấy `(venv)` ở đầu dòng lệnh:
```
(venv) D:\KHKT_TRI\...\Backend>
```

### Bước 2: Cài đặt Dependencies

```bash
# Cập nhật pip
python -m pip install --upgrade pip

# Cài đặt các thư viện
pip install -r requirements.txt
```

**Thời gian**: ~5-10 phút (tùy tốc độ mạng)

### Bước 3: Tải Model AI (quan trọng!)

Model AI không có trong GitHub (quá lớn ~35MB). Bạn cần:

**Option 1: Tải model có sẵn**
```bash
# Tạo thư mục models
mkdir -p "app/ai_models/model N/original model"

# Tải file best.pt (5.3MB) về và copy vào:
# Backend/app/ai_models/model N/original model/best.pt
```

**Option 2: Dùng model YOLOv8 mặc định**
```bash
# Model sẽ tự động tải lần đầu chạy
# File: yolov8n.pt (~6MB)
```

### Bước 4: Khởi tạo Database

```bash
# Tạo database SQLite
python -m app.db.init_db

# Kết quả:
# ✓ Database created: app/data/traffic_monitor.db
# ✓ Tables created successfully
```

### Bước 5: Kiểm tra cài đặt

```bash
# Test import
python -c "import fastapi, sqlalchemy, cv2, ultralytics; print('✓ All imports OK')"

# Kết quả mong đợi:
# ✓ All imports OK
```

---

## ⚛️ CÀI ĐẶT FRONTEND

### Bước 1: Vào thư mục Frontend

**Từ thư mục Backend:**
```bash
cd ..
cd Frontend
```

**Hoặc từ thư mục gốc:**
```bash
cd Frontend
```

### Bước 2: Cài đặt Dependencies

```bash
npm install
```

**Thời gian**: ~3-5 phút (tùy tốc độ mạng)

**Nếu gặp lỗi**, thử:
```bash
# Xóa cache và cài lại
rm -rf node_modules package-lock.json
npm install

# Hoặc dùng npm ci (nhanh hơn)
npm ci
```

### Bước 3: Cấu hình API URL

Tạo file `.env` trong thư mục `Frontend/`:

**Windows:**
```bash
echo VITE_API_URL=http://localhost:8000 > .env
```

**macOS/Linux:**
```bash
echo "VITE_API_URL=http://localhost:8000" > .env
```

**Hoặc tạo thủ công** file `Frontend/.env`:
```env
VITE_API_URL=http://localhost:8000
VITE_WS_URL=ws://localhost:8000
```

### Bước 4: Kiểm tra cài đặt

```bash
# Check dependencies
npm list --depth=0

# Test build (không bắt buộc)
npm run build
```

---

## 🚀 CHẠY DỰ ÁN

### Option 1: Chạy thủ công (2 terminal)

**Terminal 1 - Backend:**
```bash
# Windows
cd Backend
venv\Scripts\activate
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# macOS/Linux
cd Backend
source venv/bin/activate
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

**Kết quả:**
```
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
INFO:     Started reloader process
INFO:     Started server process
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```

**Terminal 2 - Frontend:**
```bash
cd Frontend
npm run dev
```

**Kết quả:**
```
  VITE v7.1.9  ready in 1234 ms

  ➜  Local:   http://localhost:5173/
  ➜  Network: http://192.168.1.100:5173/
  ➜  press h + enter to show help
```

### Option 2: Chạy tự động (Windows)

Tạo file `start.bat` ở thư mục gốc:

```batch
@echo off
echo ========================================
echo   SMART TRAFFIC MONITORING SYSTEM
echo ========================================
echo.

echo [1/2] Starting Backend...
start "Backend Server" cmd /k "cd Backend && venv\Scripts\activate && python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000"

timeout /t 5 /nobreak >nul

echo [2/2] Starting Frontend...
start "Frontend Server" cmd /k "cd Frontend && npm run dev"

echo.
echo ========================================
echo   Servers are starting...
echo   Backend:  http://localhost:8000
echo   Frontend: http://localhost:5173
echo ========================================
pause
```

**Chạy:**
```bash
start.bat
```

### Option 3: Chạy tự động (macOS/Linux)

Tạo file `start.sh` ở thư mục gốc:

```bash
#!/bin/bash

echo "========================================"
echo "  SMART TRAFFIC MONITORING SYSTEM"
echo "========================================"
echo ""

echo "[1/2] Starting Backend..."
cd Backend
source venv/bin/activate
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000 &
BACKEND_PID=$!

sleep 5

echo "[2/2] Starting Frontend..."
cd ../Frontend
npm run dev &
FRONTEND_PID=$!

echo ""
echo "========================================"
echo "  Servers are running!"
echo "  Backend:  http://localhost:8000"
echo "  Frontend: http://localhost:5173"
echo "  Press Ctrl+C to stop"
echo "========================================"

# Cleanup on exit
trap "kill $BACKEND_PID $FRONTEND_PID" EXIT
wait
```

**Cấp quyền và chạy:**
```bash
chmod +x start.sh
./start.sh
```

---

## 🌐 TRUY CẬP ỨNG DỤNG

### 1. Mở trình duyệt

Truy cập: **http://localhost:5173**

### 2. Đăng nhập

**Tài khoản mặc định:**
- **Username**: `admin`
- **Password**: `admin123`

**Hoặc tạo tài khoản mới:**
- Click "Đăng ký" trên trang login
- Điền thông tin và tạo tài khoản

### 3. Kiểm tra các tính năng

✅ **Dashboard**: Xem tổng quan thống kê
✅ **Live Detection**: Camera trực tiếp (nếu có)
✅ **History**: Lịch sử phát hiện
✅ **Reports**: Báo cáo thống kê
✅ **Settings**: Cấu hình hệ thống

---

## ❌ XỬ LÝ LỖI THƯỜNG GẶP

### Lỗi 1: Port đã được sử dụng

**Triệu chứng:**
```
ERROR: [Errno 10048] error while attempting to bind on address ('0.0.0.0', 8000)
```

**Giải pháp:**

**Windows:**
```bash
# Tìm process đang dùng port 8000
netstat -ano | findstr :8000

# Kill process (thay PID bằng số tìm được)
taskkill /PID [PID] /F

# Hoặc đổi port
python -m uvicorn app.main:app --port 8001
```

**macOS/Linux:**
```bash
# Tìm và kill process
lsof -ti:8000 | xargs kill -9

# Hoặc đổi port
python -m uvicorn app.main:app --port 8001
```

### Lỗi 2: Module not found

**Triệu chứng:**
```
ModuleNotFoundError: No module named 'fastapi'
```

**Giải pháp:**
```bash
# Kiểm tra virtual environment đã kích hoạt chưa
# Phải thấy (venv) ở đầu dòng

# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate

# Cài lại dependencies
pip install -r requirements.txt
```

### Lỗi 3: CUDA/GPU không khả dụng

**Triệu chứng:**
```
WARNING: CUDA not available, using CPU
```

**Giải pháp:**

**Option 1: Cài CUDA Toolkit (nếu có GPU NVIDIA)**
```bash
# Tải CUDA Toolkit 11.8 hoặc 12.1
https://developer.nvidia.com/cuda-downloads

# Cài PyTorch với CUDA
pip install torch torchvision --index-url https://download.pytorch.org/whl/cu118
```

**Option 2: Dùng CPU (máy yếu)**
```python
# File: Backend/app/core/config.py
# Thêm dòng này
FORCE_CPU = True
```

### Lỗi 4: Model file không tìm thấy

**Triệu chứng:**
```
FileNotFoundError: Model file not found: ./app/ai_models/model N/original model/best.pt
```

**Giải pháp:**
```bash
# Tạo thư mục
mkdir -p "Backend/app/ai_models/model N/original model"

# Copy file best.pt vào đó

# Hoặc sửa config để dùng model mặc định
# File: Backend/app/core/config.py
MODELS_PATH = r'yolov8n.pt'  # Sẽ tự động tải
```

### Lỗi 5: npm install failed

**Triệu chứng:**
```
npm ERR! code ERESOLVE
npm ERR! ERESOLVE unable to resolve dependency tree
```

**Giải pháp:**
```bash
# Option 1: Force install
npm install --legacy-peer-deps

# Option 2: Clear cache
npm cache clean --force
rm -rf node_modules package-lock.json
npm install

# Option 3: Dùng yarn
npm install -g yarn
yarn install
```

### Lỗi 6: Database locked

**Triệu chứng:**
```
sqlite3.OperationalError: database is locked
```

**Giải pháp:**
```bash
# Stop tất cả server
# Xóa file lock
rm Backend/app/data/traffic_monitor.db-journal

# Khởi động lại
```

### Lỗi 7: CORS error trên Browser

**Triệu chứng:**
```
Access to fetch at 'http://localhost:8000' has been blocked by CORS policy
```

**Giải pháp:**

Kiểm tra file `Backend/app/main.py`:
```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### Lỗi 8: WebSocket connection failed

**Triệu chứng:**
```
WebSocket connection to 'ws://localhost:8000/ws' failed
```

**Giải pháp:**
```bash
# Kiểm tra Backend đang chạy
curl http://localhost:8000/health

# Kiểm tra file Frontend/.env
VITE_WS_URL=ws://localhost:8000

# Restart cả 2 servers
```

---

## 📊 KIỂM TRA HỆ THỐNG

### Health Check

**Backend API:**
```bash
curl http://localhost:8000/health
# Response: {"status":"healthy"}
```

**Backend Docs:**
Mở trình duyệt: **http://localhost:8000/docs**

**Frontend:**
Mở trình duyệt: **http://localhost:5173**

### Performance Test

```bash
# Test API response time
curl -w "@-" -o /dev/null -s http://localhost:8000/api/v1/cameras <<'EOF'
    time_namelookup:  %{time_namelookup}\n
       time_connect:  %{time_connect}\n
    time_appconnect:  %{time_appconnect}\n
      time_redirect:  %{time_redirect}\n
 time_starttransfer:  %{time_starttransfer}\n
                    ----------\n
         time_total:  %{time_total}\n
EOF
```

---

## 🎯 NEXT STEPS

Sau khi cài đặt thành công:

1. **Đọc tài liệu API**: http://localhost:8000/docs
2. **Xem hướng dẫn deploy**: [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md)
3. **Tối ưu hệ thống**: [OPTIMIZATION_GUIDE.md](OPTIMIZATION_GUIDE.md)
4. **Đọc thuyết minh dự án**: [THUYET_MINH_DU_AN.md](THUYET_MINH_DU_AN.md)

---

## 📞 HỖ TRỢ

Nếu gặp vấn đề khác:

1. Check logs trong terminal
2. Kiểm tra file `Backend/logs/app.log`
3. Tìm trong [Issues](https://github.com/your-repo/issues)
4. Tạo issue mới với đầy đủ thông tin lỗi

---

## 📝 CHECKLIST CÀI ĐẶT

- [ ] Python 3.11+ đã cài
- [ ] Node.js 18+ đã cài
- [ ] Git đã cài
- [ ] Clone/tải dự án về
- [ ] Backend: Virtual environment đã tạo
- [ ] Backend: Dependencies đã cài (requirements.txt)
- [ ] Backend: Model AI đã tải (best.pt)
- [ ] Backend: Database đã khởi tạo
- [ ] Frontend: Dependencies đã cài (npm install)
- [ ] Frontend: File .env đã tạo
- [ ] Backend chạy thành công (http://localhost:8000)
- [ ] Frontend chạy thành công (http://localhost:5173)
- [ ] Đăng nhập thành công
- [ ] Các tính năng hoạt động

---

**Chúc bạn cài đặt thành công! 🎉**

*Lưu ý: Nếu dùng cho production, hãy đọc thêm [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md)*
