# 🚀 Hướng Dẫn Deploy Smart Traffic System

## ⚠️ VẤN ĐỀ QUAN TRỌNG

Dự án này **KHÔNG THỂ DEPLOY** hoàn toàn lên Vercel vì:

1. ❌ **Backend Python/FastAPI** - Vercel chỉ hỗ trợ Serverless Functions nhẹ
2. ❌ **YOLO Models** - Quá nặng (35MB+), cần GPU
3. ❌ **Video Processing** - Cần CPU/GPU mạnh, không phù hợp serverless
4. ❌ **Real-time RTSP** - Cần persistent connection, không phù hợp Vercel

---

## ✅ GIẢI PHÁP DEPLOY

### **PHƯƠNG ÁN 1: DEPLOY RIÊNG FRONTEND & BACKEND**

#### 🎨 Frontend → Vercel (Miễn phí)
#### ⚙️ Backend → VPS hoặc Local (Cần GPU)

---

## 📦 BƯỚC 1: DEPLOY FRONTEND LÊN VERCEL

### 1. Chuẩn bị Frontend

**Tạo file `vercel.json` trong thư mục Frontend:**

```json
{
  "version": 2,
  "builds": [
    {
      "src": "package.json",
      "use": "@vercel/static-build",
      "config": {
        "distDir": "dist"
      }
    }
  ],
  "routes": [
    {
      "src": "/assets/(.*)",
      "dest": "/assets/$1"
    },
    {
      "src": "/(.*)",
      "dest": "/index.html"
    }
  ]
}
```

**Thêm build script vào `package.json`:**

```json
{
  "scripts": {
    "dev": "vite",
    "build": "vite build",
    "preview": "vite preview",
    "vercel-build": "vite build"
  }
}
```

### 2. Deploy lên Vercel

**Cách 1: Qua Website (Dễ nhất)**

1. Truy cập: https://vercel.com
2. Login bằng GitHub
3. Click "New Project"
4. Import repository của bạn
5. **Root Directory**: Chọn `Frontend`
6. **Framework Preset**: Vite
7. **Build Command**: `npm run build`
8. **Output Directory**: `dist`
9. Click "Deploy"

**Cách 2: Qua CLI**

```bash
cd Frontend
npm install -g vercel
vercel login
vercel --prod
```

### 3. Cấu hình Environment Variables

Trong Vercel Dashboard → Settings → Environment Variables:

```
VITE_API_URL=http://your-backend-url:8000
```

**LƯU Ý:** Backend phải deploy riêng!

---

## ⚙️ BƯỚC 2: DEPLOY BACKEND

### ❌ Vercel KHÔNG ĐƯỢC (do YOLO, video processing)

### ✅ Lựa chọn deploy Backend:

#### **Option 1: VPS (Khuyến nghị - Cần GPU)**

**Nhà cung cấp:**
- **DigitalOcean** ($5-10/tháng)
- **Linode** ($5/tháng)
- **AWS EC2** (Free tier 1 năm)
- **Google Cloud** ($300 credit)

**Setup:**

```bash
# SSH vào VPS
ssh user@your-vps-ip

# Clone repo
git clone <your-repo>
cd Smart-Trafic-Monitoring-System-main/Backend

# Setup Python
sudo apt update
sudo apt install python3.11 python3-pip -y

# Install dependencies
pip install -r requirements.txt

# Install YOLO dependencies
pip install ultralytics opencv-python

# Run with PM2 (auto-restart)
sudo npm install -g pm2
pm2 start "uvicorn app.main:app --host 0.0.0.0 --port 8000" --name traffic-backend
pm2 save
pm2 startup
```

#### **Option 2: Railway.app (Dễ, nhưng không có GPU)**

```bash
# Install Railway CLI
npm install -g @railway/cli

# Login
railway login

# Deploy
cd Backend
railway init
railway up
```

**LƯU Ý:** Railway miễn phí nhưng **KHÔNG CÓ GPU**, YOLO sẽ chạy chậm!

#### **Option 3: Render.com (Miễn phí, không GPU)**

1. Truy cập: https://render.com
2. Tạo "New Web Service"
3. Connect GitHub repo
4. **Root Directory**: `Backend`
5. **Build Command**: `pip install -r requirements.txt`
6. **Start Command**: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
7. Deploy

**LƯU Ý:** Render miễn phí **sleep sau 15 phút**, không phù hợp production!

#### **Option 4: Chạy Local + Ngrok (Testing)**

```bash
# Chạy Backend local
cd Backend
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000

# Terminal khác: Expose ra internet
ngrok http 8000
```

Copy URL ngrok (vd: `https://abc123.ngrok.io`) và dùng làm `VITE_API_URL`

---

## 🔧 BƯỚC 3: KẾT NỐI FRONTEND - BACKEND

### 1. Sửa Frontend để gọi Backend URL

**File: `Frontend/src/config.ts` (tạo mới)**

```typescript
export const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';
```

**Sửa các file API call:**

```typescript
// Trước
const response = await fetch('http://localhost:8000/api/v1/...');

// Sau
import { API_URL } from '@/config';
const response = await fetch(`${API_URL}/api/v1/...`);
```

### 2. Enable CORS trên Backend

**File: `Backend/app/main.py`**

Đảm bảo có:

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Trong production: chỉ cho phép domain cụ thể
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

---

## 📊 SO SÁNH PHƯƠNG ÁN DEPLOY BACKEND

| Nền tảng | Giá | GPU | Khả dụng | Phù hợp |
|----------|-----|-----|----------|---------|
| **VPS (DigitalOcean)** | $5-10/tháng | ❌ (GPU từ $50/tháng) | 24/7 | ⭐⭐⭐⭐⭐ Production |
| **Railway.app** | Free | ❌ | 24/7 | ⭐⭐⭐ Testing |
| **Render.com** | Free | ❌ | Sleep sau 15 phút | ⭐⭐ Demo |
| **AWS EC2** | Free 1 năm | ❌ | 24/7 | ⭐⭐⭐⭐ Production |
| **Local + Ngrok** | Free | ✅ | Khi máy bật | ⭐⭐⭐⭐ Development |
| **Google Colab** | Free | ✅ Tesla T4 | 12h/session | ⭐⭐⭐ Testing |

---

## 🎯 KHUYẾN NGHỊ THEO MỤC ĐÍCH

### 🏆 Dự thi KHKT (Demo):
```
✅ Frontend: Vercel (miễn phí, nhanh)
✅ Backend: Local + Ngrok (có GPU)
✅ Models: Chạy local với GPU
```

### 💼 Production thực tế:
```
✅ Frontend: Vercel hoặc Netlify
✅ Backend: VPS với GPU (DigitalOcean GPU Droplet)
✅ Database: PostgreSQL (managed)
✅ Models: GPU server
```

### 🧪 Testing/Development:
```
✅ Frontend: Vercel
✅ Backend: Railway hoặc Render
⚠️ Lưu ý: YOLO sẽ chạy chậm vì không có GPU
```

---

## 🚨 LỖI THƯỜNG GẶP

### 1. Vercel 404 Error

**Nguyên nhân:** Deploy cả project thay vì chỉ Frontend

**Giải pháp:**
- Trong Vercel: Settings → Root Directory → Chọn `Frontend`
- Hoặc: Deploy chỉ thư mục Frontend

### 2. CORS Error

**Nguyên nhân:** Backend không cho phép origin từ Vercel

**Giải pháp:**
```python
# Backend/app/main.py
allow_origins=["https://your-vercel-domain.vercel.app"]
```

### 3. Model Not Found

**Nguyên nhân:** Models không được push lên Git (bị gitignore)

**Giải pháp:**
- Upload models lên Google Drive
- Download khi deploy: `wget <drive-link> -O best.pt`

### 4. Out of Memory

**Nguyên nhân:** YOLO models quá nặng cho serverless

**Giải pháp:**
- Dùng VPS thay vì Vercel/Render
- Hoặc: Tắt YOLO detection khi deploy

---

## 📝 CHECKLIST DEPLOY

### Frontend (Vercel):
- [ ] Tạo file `vercel.json`
- [ ] Set `VITE_API_URL` environment variable
- [ ] Build thành công (`npm run build`)
- [ ] Deploy lên Vercel
- [ ] Test truy cập URL

### Backend:
- [ ] Chọn nền tảng deploy (VPS/Railway/Render)
- [ ] Upload models (nếu cần)
- [ ] Cấu hình CORS
- [ ] Test API endpoints
- [ ] Enable HTTPS (nếu production)

### Kết nối:
- [ ] Frontend gọi được Backend API
- [ ] CORS không bị lỗi
- [ ] Authentication hoạt động
- [ ] Database kết nối OK

---

## 🆘 HỖ TRỢ

**Nếu gặp lỗi:**

1. Check logs: `vercel logs` (Frontend) hoặc logs trên platform backend
2. Test API: `curl https://your-backend-url/api/v1/health`
3. Check CORS: Mở DevTools → Network → xem lỗi

**Contact:**
- GitHub Issues: <your-repo-issues>
- Email: <your-email>

---

## ✅ KẾT LUẬN

**Cho dự án KHKT của bạn:**

1. ✅ **Deploy Frontend lên Vercel** - Dễ, nhanh, miễn phí
2. ✅ **Chạy Backend local + Ngrok** - Có GPU, mượt
3. ✅ **Khi demo**: Bật Backend trước, Frontend tự động kết nối

**KHÔNG NÊN:**
- ❌ Deploy Backend lên Vercel (không hỗ trợ)
- ❌ Deploy toàn bộ project lên 1 nơi (sẽ lỗi)
- ❌ Dùng serverless cho YOLO (quá nặng)

**Bạn cần deploy ngay bây giờ để demo hay để production sau này?**
