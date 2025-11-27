# FIX LỖI EXPORT PDF - "Vui lòng thử lại"

## LỖI ĐANG GẶP

Frontend báo lỗi: **"Lỗi khi export PDF. Vui lòng thử lại."**

## NGUYÊN NHÂN

Có 3 nguyên nhân chính:

### 1. Database không có dữ liệu
Khi database trống, API không thể tạo báo cáo

### 2. API endpoint trả về lỗi
Server backend có thể gặp lỗi khi xử lý request

### 3. Frontend gửi request sai format
Parameters không đúng định dạng mà API yêu cầu

---

## CÁCH FIX

### BƯỚC 1: Kiểm tra Backend đang chạy

Mở terminal và chạy:

```bash
cd Backend
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000
```

Đợi đến khi thấy:
```
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
```

### BƯỚC 2: Test API qua Swagger UI

1. Mở trình duyệt: **http://localhost:8000/docs**

2. Tìm endpoint: **POST /api/v1/reports/export/pdf**

3. Click "Try it out"

4. Nhập request body mẫu:

```json
{
  "road_names": [],
  "start_date": "2025-11-20",
  "end_date": "2025-11-27",
  "period": "day"
}
```

5. Click "Execute"

6. Kiểm tra Response:
   - **200 OK** → API hoạt động tốt
   - **422 Validation Error** → Request body sai format
   - **500 Internal Server Error** → Backend có lỗi

### BƯỚC 3: Thêm dữ liệu test vào database

Nếu database trống, chạy script này để thêm data test:

```bash
cd Backend
python test_full_system.py
```

Hoặc tạo file `add_test_data.py`:

```python
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from datetime import datetime, timedelta
from app.db.database import get_db_sync
from app.models.traffic_record import TrafficRecord

def add_test_data():
    db = next(get_db_sync())

    # Thêm 50 bản ghi test
    for i in range(50):
        date = datetime.now() - timedelta(days=i % 7)
        record = TrafficRecord(
            road_name="Đường Lê Lợi",
            count_car=10 + i % 20,
            count_motor=15 + i % 25,
            total_vehicles=25 + i % 45,
            speed_car=30.0 + i % 20,
            speed_motor=25.0 + i % 15,
            avg_speed=27.5 + i % 18,
            traffic_status="clear" if i % 3 == 0 else "busy",
            hour_of_day=date.hour,
            day_of_week=date.weekday(),
            date=date.strftime("%Y-%m-%d")
        )
        db.add(record)

    db.commit()
    print(f"[OK] Đã thêm 50 bản ghi test vào database")

if __name__ == "__main__":
    add_test_data()
```

Chạy:
```bash
python add_test_data.py
```

### BƯỚC 4: Kiểm tra lại Frontend

1. Refresh trang Frontend (F5)
2. Thử export PDF lại
3. Nếu vẫn lỗi, mở **Console** (F12) để xem lỗi chi tiết

---

## DEBUG CHI TIẾT

### Xem log Backend

Khi click "Export PDF" ở Frontend, xem console Backend xem có lỗi gì:

```
[Errno ...] → Lỗi file system
ValidationError → Dữ liệu sai format
KeyError → Thiếu field trong data
```

### Xem log Frontend (Browser Console)

Nhấn F12 → Tab Console:

```javascript
// Lỗi network
Failed to fetch → Backend không chạy hoặc sai URL

// Lỗi từ API
422 Unprocessable Entity → Request body sai
500 Internal Server Error → Backend có lỗi

// Lỗi trong Frontend code
TypeError → Code Frontend có bug
```

### Test trực tiếp qua curl

```bash
curl -X POST http://localhost:8000/api/v1/reports/export/pdf ^
  -H "Content-Type: application/json" ^
  -d "{\"start_date\":\"2025-11-20\",\"end_date\":\"2025-11-27\",\"period\":\"day\"}" ^
  --output test_report.pdf
```

Nếu thành công, file `test_report.pdf` sẽ được tạo.

---

## LỖI THƯỜNG GẶP VÀ CÁCH FIX

### Lỗi 1: "Failed to fetch"

**Nguyên nhân:** Backend không chạy hoặc Frontend gọi sai URL

**Fix:**
- Kiểm tra Backend đang chạy ở port 8000
- Kiểm tra CORS đã bật trong backend

### Lỗi 2: "422 Validation Error"

**Nguyên nhân:** Request body thiếu field hoặc sai kiểu dữ liệu

**Fix:** Đảm bảo request có đúng format:

```typescript
// Frontend code
const requestBody = {
  road_names: [],  // Array of strings
  start_date: "2025-11-20",  // YYYY-MM-DD
  end_date: "2025-11-27",    // YYYY-MM-DD
  period: "day"  // "day" | "week" | "month"
}
```

### Lỗi 3: "500 Internal Server Error"

**Nguyên nhân:** Backend gặp lỗi khi xử lý (thường do data trống)

**Fix:**
1. Thêm dữ liệu test vào database
2. Kiểm tra log backend để xem lỗi cụ thể

### Lỗi 4: Database locked

**Nguyên nhân:** SQLite đang bị lock bởi process khác

**Fix:**
```bash
# Dừng tất cả Python processes
wmic process where "name='python.exe'" delete

# Xóa file database và tạo lại
del Backend\traffic_data.db
cd Backend
python -m uvicorn app.main:app --reload
```

---

## CODE FIX NHANH

### Fix scheduler error (Error in scheduler loop)

File: `Backend/app/services/traffic_data_scheduler.py`

Tìm dòng:
```python
async with get_db() as session:
```

Sửa thành:
```python
async for session in get_db():
```

---

## KIỂM TRA CUỐI CÙNG

Chạy script test để đảm bảo tất cả OK:

```bash
cd Backend
python test_export_quick.py
```

Kết quả mong đợi:
```
Test PDF...
[OK] PDF - 116,580 bytes - File: test_20251127_222707.pdf
Test Excel...
[OK] Excel - 12,697 bytes - File: test_20251127_222707.xlsx
```

Nếu cả 2 đều [OK] → Chức năng export hoạt động tốt!

---

## TÓM TẮT CHECKLIST

- [ ] Backend đang chạy (port 8000)
- [ ] Database có dữ liệu (ít nhất 10 records)
- [ ] API test qua Swagger UI → 200 OK
- [ ] Script test_export_quick.py chạy OK
- [ ] Frontend refresh (F5) rồi thử lại

---

**Nếu làm theo tất cả các bước trên mà vẫn lỗi, gửi cho tôi:**
1. Screenshot lỗi từ Frontend
2. Log từ Backend console
3. Response từ Browser Console (F12 → Network tab)

Tôi sẽ giúp debug chi tiết hơn!

---

© 2025 - Hướng dẫn fix lỗi Export PDF
