# 📦 DANH SÁCH THƯ VIỆN CÀI ĐẶT

**Dành cho:** Hệ thống Smart Traffic Monitoring System  
**Phiên bản:** 3.0.0  
**Ngày cập nhật:** 11/12/2024

---

## 🐍 BACKEND - PYTHON PACKAGES

### requirements_cpu.txt (Cho máy không có GPU)

```txt
# Web Framework
fastapi==0.104.1
uvicorn[standard]==0.24.0
python-multipart==0.0.6

# Database
sqlalchemy[asyncio]==2.0.23
aiosqlite==0.19.0
alembic==1.12.1

# Authentication & Security
python-jose[cryptography]==3.3.0
passlib[bcrypt]==1.7.4
bcrypt==4.1.1

# AI & Computer Vision
ultralytics==8.0.228
opencv-python==4.8.1.78
openvino==2024.0.0
openvino-dev==2024.0.0
torch==2.1.1
torchvision==0.16.1
numpy==1.24.3
pillow==10.1.0

# Object Tracking
filterpy==1.4.5
scikit-image==0.22.0
lap==0.4.0

# Report Generation
reportlab==4.0.7
matplotlib==3.8.2
openpyxl==3.1.2
pandas==2.1.4

# Telegram Integration
python-telegram-bot==20.7
telegram==0.0.1

# AI Chatbot
google-generativeai==0.3.1
langchain==0.1.0
langgraph==0.0.20

# Utilities
python-dotenv==1.0.0
pydantic==2.5.2
pydantic-settings==2.1.0
requests==2.31.0
httpx==0.25.2
aiofiles==23.2.1
python-dateutil==2.8.2
pytz==2023.3

# Monitoring
psutil==5.9.6
```

### requirements_gpu.txt (Cho máy có GPU NVIDIA)

```txt
# Kế thừa tất cả từ CPU version
-r requirements_cpu.txt

# GPU-optimized packages
torch==2.1.1+cu118
torchvision==0.16.1+cu118
--extra-index-url https://download.pytorch.org/whl/cu118

# CUDA utilities
nvidia-ml-py3==7.352.0
```

---

## 🎨 FRONTEND - NODE.JS PACKAGES

### package.json

```json
{
  "name": "smart-traffic-frontend",
  "version": "3.0.0",
  "type": "module",
  "scripts": {
    "dev": "vite",
    "build": "tsc && vite build",
    "preview": "vite preview",
    "lint": "eslint . --ext ts,tsx"
  },
  "dependencies": {
    "react": "^18.3.1",
    "react-dom": "^18.3.1",
    "react-router-dom": "^6.20.1",
    
    "axios": "^1.6.2",
    "date-fns": "^4.1.0",
    
    "@radix-ui/react-accordion": "^1.2.2",
    "@radix-ui/react-alert-dialog": "^1.1.4",
    "@radix-ui/react-avatar": "^1.1.2",
    "@radix-ui/react-checkbox": "^1.1.3",
    "@radix-ui/react-dialog": "^1.1.4",
    "@radix-ui/react-dropdown-menu": "^2.1.4",
    "@radix-ui/react-label": "^2.1.1",
    "@radix-ui/react-popover": "^1.1.4",
    "@radix-ui/react-progress": "^1.1.1",
    "@radix-ui/react-scroll-area": "^1.2.2",
    "@radix-ui/react-select": "^2.1.4",
    "@radix-ui/react-separator": "^1.1.1",
    "@radix-ui/react-slider": "^1.2.1",
    "@radix-ui/react-slot": "^1.1.1",
    "@radix-ui/react-switch": "^1.1.2",
    "@radix-ui/react-tabs": "^1.1.2",
    "@radix-ui/react-toast": "^1.2.4",
    "@radix-ui/react-tooltip": "^1.1.6",
    
    "class-variance-authority": "^0.7.1",
    "clsx": "^2.1.1",
    "cmdk": "^1.0.4",
    "framer-motion": "^11.15.0",
    "lucide-react": "^0.468.0",
    "recharts": "^2.15.0",
    "tailwind-merge": "^2.6.0",
    "tailwindcss-animate": "^1.0.7",
    "vaul": "^1.1.3",
    "zod": "^3.24.1",
    "zustand": "^5.0.2"
  },
  "devDependencies": {
    "@types/node": "^22.10.2",
    "@types/react": "^18.3.18",
    "@types/react-dom": "^18.3.5",
    "@typescript-eslint/eslint-plugin": "^8.18.0",
    "@typescript-eslint/parser": "^8.18.0",
    "@vitejs/plugin-react": "^4.3.4",
    "autoprefixer": "^10.4.20",
    "eslint": "^9.17.0",
    "eslint-plugin-react-hooks": "^5.0.0",
    "eslint-plugin-react-refresh": "^0.4.16",
    "postcss": "^8.4.49",
    "tailwindcss": "^3.4.17",
    "typescript": "~5.6.2",
    "vite": "^6.0.3"
  }
}
```

---

## 💻 HỆ ĐIỀU HÀNH

### Windows 10/11

**Phần mềm cần cài:**
1. Python 3.9-3.12: https://www.python.org/downloads/
2. Node.js 18+: https://nodejs.org/
3. Git: https://git-scm.com/download/win
4. Visual C++ Redistributable: https://aka.ms/vs/17/release/vc_redist.x64.exe

**Lệnh kiểm tra:**
```bash
python --version
node --version
npm --version
git --version
```

### Ubuntu 20.04+

**Cài đặt dependencies:**
```bash
# Update package list
sudo apt update

# Python và pip
sudo apt install python3.9 python3.9-venv python3-pip

# Node.js
curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
sudo apt install -y nodejs

# Git
sudo apt install git

# OpenCV dependencies
sudo apt install -y libgl1 libglib2.0-0 libsm6 libxext6 libxrender-dev

# Build tools
sudo apt install -y build-essential cmake
```

---

## 🚦 THƯ VIỆN BỔ SUNG CHO PHÁT HIỆN VƯỢT ĐÈN ĐỎ

### Additional Python Packages (Thêm vào requirements.txt)

```txt
# Traffic Light Color Detection
scikit-learn==1.3.2
scipy==1.11.4

# Image Processing (enhanced)
opencv-contrib-python==4.8.1.78  # Thay thế opencv-python nếu cần thêm tính năng

# Color Space Conversion
colormath==3.0.0
```

### Giải thích:
- **scikit-learn:** Machine learning để cải thiện độ chính xác phát hiện màu đèn
- **scipy:** Tính toán toán học nâng cao cho xử lý ảnh
- **opencv-contrib-python:** Thêm algorithms xử lý ảnh nâng cao (optional)
- **colormath:** Chuyển đổi không gian màu chính xác (HSV, LAB, RGB)

### Cài đặt:
```bash
pip install scikit-learn==1.3.2 scipy==1.11.4 colormath==3.0.0
```

---

## 🎥 YÊU CẦU CAMERA

### Định dạng hỗ trợ:
- **RTSP:** ✅ (Khuyến nghị)
- **RTMP:** ✅
- **HTTP Stream:** ✅
- **USB Camera:** ✅ (Dùng index: 0, 1, 2...)
- **File video:** ✅ (.mp4, .avi, .mov, .mkv)

### Codec video hỗ trợ:
- **H.264/AVC:** ✅ (Khuyến nghị)
- **H.265/HEVC:** ✅
- **MJPEG:** ✅

### Thông số camera khuyến nghị:

**Camera Chính (Giám sát giao thông):**

| Thông số | Tối thiểu | Khuyến nghị | Tối đa |
|----------|-----------|-------------|--------|
| **Resolution** | 640x480 | 1280x720 | 1920x1080 |
| **FPS** | 10 | 15-20 | 30 |
| **Bitrate** | 512 Kbps | 2 Mbps | 8 Mbps |
| **Latency** | < 500ms | < 200ms | < 100ms |

**Camera Phụ (Nhìn đèn tín hiệu) - BẮT BUỘC:**

| Thông số | Tối thiểu | Khuyến nghị | Tối đa |
|----------|-----------|-------------|--------|
| **Resolution** | 1280x720 | **1920x1080** | 4K |
| **FPS** | 15 | **20-30** | 60 |
| **Bitrate** | 1 Mbps | **2-4 Mbps** | 8 Mbps |
| **WDR/HDR** | ❌ | **✅ Bắt buộc** | ✅ |
| **Low Light** | ❌ | **✅ Bắt buộc** | ✅ |
| **Latency** | < 500ms | **< 100ms** | < 50ms |

---

## 🔧 CÔNG CỤ HỖ TRỢ

### Test RTSP Connection:
1. **VLC Media Player:** https://www.videolan.org/
2. **FFmpeg:** https://ffmpeg.org/download.html
3. **OBS Studio:** https://obsproject.com/

### Quản lý Python:
1. **pip:** Built-in with Python
2. **virtualenv:** `pip install virtualenv`

### Quản lý Node.js:
1. **pnpm:** `npm install -g pnpm` (Khuyến nghị)
2. **npm:** Built-in with Node.js

---

## 📊 KÍCH THƯỚC CÀI ĐẶT

| Thành phần | Kích thước |
|------------|-----------|
| **Python packages** | ~3.5 GB |
| **Node packages** | ~500 MB |
| **YOLO models** | ~50 MB |
| **Source code** | ~100 MB |
| **Tổng cộng** | **~4.2 GB** |

**Thời gian cài đặt ước tính:**
- Mạng nhanh (100 Mbps): ~15-20 phút
- Mạng trung bình (50 Mbps): ~30-40 phút

---

## ✅ CHECKLIST CÀI ĐẶT

### Trước khi cài:
- [ ] Kiểm tra Python version (3.9-3.12)
- [ ] Kiểm tra Node.js version (18+)
- [ ] Đảm bảo đủ dung lượng ổ cứng (5GB)
- [ ] Kết nối internet ổn định

### Sau khi cài:
- [ ] Backend có thể khởi động: `uvicorn main:app`
- [ ] Frontend có thể build: `pnpm run build`
- [ ] Tất cả dependencies không có conflict
- [ ] YOLO model load thành công

---

## 🆘 XỬ LÝ LỖI THƯỜNG GẶP

### Lỗi: "Microsoft Visual C++ 14.0 is required"
**Giải pháp:** Cài Visual C++ Build Tools
```bash
# Download và cài
https://visualstudio.microsoft.com/visual-cpp-build-tools/
```

### Lỗi: "No module named 'cv2'"
**Giải pháp:** 
```bash
pip uninstall opencv-python opencv-python-headless
pip install opencv-python==4.8.1.78
```

### Lỗi: "pnpm: command not found"
**Giải pháp:**
```bash
npm install -g pnpm
# Hoặc dùng npm thay thế
npm install
```

---

**© 2024 Smart Traffic Monitoring System - Tài liệu thư viện v3.0**
