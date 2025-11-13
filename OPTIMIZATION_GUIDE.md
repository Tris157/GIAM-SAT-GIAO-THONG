# 🚀 Hướng Dẫn Tối Ưu Hóa Dự Án

## 📦 Giảm Dung Lượng Repository

### 1. **Models (AI Weights) - KHÔNG ĐẨY LÊN GITHUB**

Models đã được thêm vào `.gitignore`:
```
weight/
Backend/app/ai_models/
*.pt
*.onnx
```

**Lưu trữ models:**
- Upload lên Google Drive, OneDrive, hoặc Hugging Face
- Chia sẻ link download trong README
- Dung lượng models: ~35MB (obstacle.pt + traffic_sign.pt + best.pt)

### 2. **Python Virtual Environment - KHÔNG ĐẨY LÊN GITHUB**

Đã được gitignore:
```
Backend/venv/
venv/
env/
```

**Setup lại venv:**
```bash
cd Backend
python -m venv venv
venv\Scripts\activate  # Windows
pip install -r requirements.txt
```

### 3. **Node Modules - KHÔNG ĐẨY LÊN GITHUB**

Đã được gitignore:
```
node_modules
```

**Setup lại:**
```bash
cd Frontend
npm install
```

### 4. **Cache Files - Tự Động Xóa**

Các file cache Python được tự động xóa:
```bash
# Xóa __pycache__
find Backend -type d -name "__pycache__" -exec rm -rf {} +

# Xóa .pyc, .pyo
find Backend -type f \( -name "*.pyc" -o -name "*.pyo" \) -delete

# Xóa logs
find Backend -type f -name "*.log" -delete
```

### 5. **Database - Chỉ Giữ Schema**

File database test (~60-72KB) có thể xóa:
```bash
rm Backend/app/traffic_data.db
rm Backend/traffic_data.db
```

Database sẽ tự động được tạo lại khi chạy app.

---

## 📊 Dung Lượng Sau Tối Ưu

| Mục | Trước | Sau | Giảm |
|-----|-------|-----|------|
| **Total Repository** | ~2GB | ~50-100MB | -95% |
| Models (*.pt) | 35MB | 0MB (gitignored) | -100% |
| Backend venv | ~1.5GB | 0MB (gitignored) | -100% |
| Frontend node_modules | ~400MB | 0MB (gitignored) | -100% |
| Python cache | ~50MB | 0MB (cleaned) | -100% |

---

## 🎯 Checklist Trước Khi Push

- [ ] Xóa tất cả `__pycache__`
- [ ] Xóa file `.pyc`, `.pyo`, `.log`
- [ ] Đảm bảo `venv/` không bị track
- [ ] Đảm bảo `node_modules/` không bị track
- [ ] Đảm bảo models (*.pt) không bị track
- [ ] Commit `.gitignore` mới
- [ ] Kiểm tra `git status` - không có file lớn

---

## 🔧 Setup Dự Án Sau Khi Clone

### Bước 1: Clone Repository
```bash
git clone <your-repo-url>
cd Smart-Trafic-Monitoring-System-main
```

### Bước 2: Setup Backend
```bash
cd Backend
python -m venv venv
venv\Scripts\activate  # Windows
# hoặc: source venv/bin/activate  # Linux/Mac

pip install -r requirements.txt
```

### Bước 3: Download Models
```bash
# Tạo thư mục
mkdir -p "Backend/app/ai_models/model N/original model"

# Download từ link được cung cấp và đặt vào:
# Backend/app/ai_models/model N/original model/obstacle.pt
# Backend/app/ai_models/model N/original model/traffic_sign.pt
# Backend/app/ai_models/model N/original model/best.pt
```

### Bước 4: Setup Frontend
```bash
cd Frontend
npm install
```

### Bước 5: Chạy Ứng Dụng

**Backend:**
```bash
cd Backend
venv\Scripts\activate
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

**Frontend:**
```bash
cd Frontend
npm run dev
```

---

## 📝 File `.gitignore` Quan Trọng

Đảm bảo file `.gitignore` có các dòng sau:

```gitignore
# Python
Backend/venv/
venv/
env/
__pycache__/
*.py[cod]
*.pyc
*.pyo
*.log

# Node
node_modules/
dist/

# Models (Large files)
weight/
Backend/app/ai_models/
*.pt
*.onnx
*.tflite
*.h5

# Database
*.db
*.sqlite
*.sqlite3

# Environment
.env
.env.local

# OS
nul
Thumbs.db
.DS_Store
```

---

## 🚨 Lỗi Thường Gặp

### 1. "Model not found"
```bash
# Download models và đặt đúng thư mục
Backend/app/ai_models/model N/original model/obstacle.pt
```

### 2. "ModuleNotFoundError"
```bash
# Cài lại dependencies
pip install -r requirements.txt
```

### 3. "npm ERR!"
```bash
# Xóa và cài lại
rm -rf node_modules package-lock.json
npm install
```

---

## 💡 Tips Tối Ưu Thêm

### 1. Sử dụng Git LFS cho files lớn (Optional)
```bash
git lfs install
git lfs track "*.pt"
git lfs track "*.mp4"
```

### 2. Nén models trước khi chia sẻ
```bash
# Windows
tar -czf models.tar.gz Backend/app/ai_models/

# Linux/Mac
tar -czf models.tar.gz Backend/app/ai_models/
```

### 3. Tạo script tự động cleanup
```bash
# cleanup.sh
#!/bin/bash
find Backend -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null
find Backend -type f \( -name "*.pyc" -o -name "*.pyo" -o -name "*.log" \) -delete 2>/dev/null
echo "✅ Cleanup completed!"
```

---

## 📦 Requirements Files

### Backend: `requirements.txt`
```
fastapi
uvicorn
sqlalchemy
aiosqlite
python-jose[cryptography]
passlib[bcrypt]
python-multipart
ultralytics
opencv-python
numpy
```

### Frontend: `package.json` dependencies
```json
{
  "dependencies": {
    "react": "^19.2.0",
    "react-dom": "^19.2.0",
    "react-router-dom": "^7.x",
    "tailwindcss": "^4.x",
    "@radix-ui/react-*": "latest",
    "lucide-react": "latest",
    "recharts": "^2.x"
  }
}
```

---

## ✅ Kết Luận

Sau khi tối ưu:
- ✅ Repository giảm từ **2GB → ~50-100MB** (-95%)
- ✅ Đẩy lên GitHub nhanh hơn 20x
- ✅ Clone nhanh hơn 20x
- ✅ Tiết kiệm bandwidth và storage
- ✅ Dễ dàng chia sẻ với team

**Lưu ý:** Models cần được download riêng sau khi clone!
