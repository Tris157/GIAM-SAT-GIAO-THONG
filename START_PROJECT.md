# 🚀 Hướng dẫn chạy dự án

## ✅ ĐANG CHẠY - Servers đã khởi động thành công!

### 📊 Trạng thái hiện tại:

- ✅ **Backend API**: http://localhost:8000
  - FastAPI server đang chạy
  - Database đã kết nối
  - API Docs: http://localhost:8000/docs

- ✅ **Frontend**: http://localhost:3000
  - HTML/CSS/JS thuần
  - Python HTTP Server
  - Login Page: http://localhost:3000/login.html

---

## 🌐 Truy cập ứng dụng:

### **Mở trình duyệt và truy cập:**

```
http://localhost:3000
```

**Hoặc trực tiếp:**
```
http://localhost:3000/login.html
```

---

## 📋 Các bước đã thực hiện:

### **1. Backend (FastAPI)**
```bash
✅ Đã khởi động: python -m uvicorn app.main:app --reload
✅ Port: 8000
✅ Database: SQLite đã sẵn sàng
✅ API Endpoints: /auth/login, /auth/register, /api/*
```

### **2. Frontend (Vanilla HTML/CSS/JS)**
```bash
✅ Đã khởi động: python -m http.server 3000
✅ Port: 3000
✅ Pages: index.html, login.html, register.html, dashboard.html
```

---

## 🎯 Test ứng dụng:

### **Bước 1: Truy cập Login Page**
```
http://localhost:3000/login.html
```

### **Bước 2: Tạo tài khoản mới**
- Click "Sign up" ở cuối trang login
- Hoặc truy cập: http://localhost:3000/register.html
- Điền thông tin:
  - Username: test
  - Email: test@example.com
  - Password: test123
  - Confirm Password: test123

### **Bước 3: Đăng nhập**
- Quay lại login page
- Nhập username và password vừa tạo
- Click "Sign In"

### **Bước 4: Xem Dashboard**
- Sau khi login thành công sẽ redirect tới: http://localhost:3000/dashboard.html
- Xem thông tin user
- Xem statistics
- Test logout

---

## 🔍 Kiểm tra API Backend:

### **API Documentation (Swagger UI):**
```
http://localhost:8000/docs
```

### **Test API trực tiếp:**

**1. Health Check:**
```bash
curl http://localhost:8000/
```

**2. Register User:**
```bash
curl -X POST http://localhost:8000/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "email": "test@example.com",
    "password": "test123"
  }'
```

**3. Login:**
```bash
curl -X POST http://localhost:8000/auth/login \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=testuser&password=test123"
```

---

## 🛠️ Lệnh chạy dự án (Để chạy lại sau này):

### **Terminal 1 - Backend:**
```bash
cd Backend
venv\Scripts\activate  # Windows
# hoặc: source venv/bin/activate  # Linux/Mac

python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

### **Terminal 2 - Frontend:**
```bash
cd Frontend
python -m http.server 3000
```

---

## 🎨 Giao diện Features:

### **Login/Register Pages:**
- ✅ Animated gradient background
- ✅ 3D floating circles
- ✅ Glass-morphism effects
- ✅ Smooth animations
- ✅ Real-time validation
- ✅ Password strength indicator (Register)
- ✅ Loading states
- ✅ Error handling

### **Dashboard:**
- ✅ Sidebar navigation
- ✅ User info display
- ✅ Statistics cards
- ✅ Animated numbers
- ✅ Logout functionality
- ✅ Responsive design

---

## 🐛 Troubleshooting:

### **Nếu Backend không chạy:**
```bash
# Kiểm tra port 8000 có bị chiếm không
netstat -ano | findstr :8000

# Thử port khác
python -m uvicorn app.main:app --port 8001
```

### **Nếu Frontend không chạy:**
```bash
# Kiểm tra port 3000
netstat -ano | findstr :3000

# Thử port khác
python -m http.server 3001
```

### **Nếu có lỗi CORS:**
Backend đã có CORS middleware, nhưng nếu vẫn lỗi:
- Kiểm tra file `Backend/app/main.py`
- Tìm dòng `allow_origins=["*"]`
- Đảm bảo middleware được add

### **Nếu Login không hoạt động:**
1. Mở Console trong browser (F12)
2. Xem tab Network để check API calls
3. Xem tab Console để check JavaScript errors
4. Kiểm tra API_BASE_URL trong `Frontend/js/login.js`

---

## 📱 Các trang web:

| Trang | URL | Mô tả |
|-------|-----|-------|
| **Home** | http://localhost:3000 | Redirect to Login |
| **Login** | http://localhost:3000/login.html | Đăng nhập |
| **Register** | http://localhost:3000/register.html | Đăng ký tài khoản |
| **Dashboard** | http://localhost:3000/dashboard.html | Dashboard chính |
| **API Docs** | http://localhost:8000/docs | Swagger UI |
| **ReDoc** | http://localhost:8000/redoc | Alternative API docs |

---

## 💡 Tips:

### **Development:**
- Mở browser DevTools (F12) để debug
- Console sẽ hiện API responses
- Network tab để xem requests/responses

### **Testing:**
- Tạo nhiều user để test
- Test validation errors
- Test password strength indicator
- Test logout và re-login

### **Customization:**
- Đổi màu: Edit `Frontend/css/login.css`
- Đổi animation speed: Tìm `animation:` trong CSS
- Thêm features: Edit các file `.js`

---

## 🎉 Kết luận:

**Dự án đã chạy thành công!** 🚀

Bạn có thể:
- ✅ Truy cập http://localhost:3000
- ✅ Tạo tài khoản mới
- ✅ Đăng nhập
- ✅ Xem dashboard
- ✅ Test tất cả features

**Enjoy coding!** 💻
