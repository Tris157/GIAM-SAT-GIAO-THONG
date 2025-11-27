# LỖI VÀ CÁCH FIX - EXPORT PDF

## LỖI PHÁT HIỆN

```
sqlalchemy.exc.MissingGreenlet: greenlet_spawn has not been called
```

**Vị trí:** `Backend/app/api/v1/api_reports.py:131`

## NGUYÊN NHÂN

API endpoint `/reports/export/pdf` đang dùng:
- **Async endpoint** (`async def export_pdf_report`)
- **Async database** (`aiosqlite`)
- Nhưng gọi **SYNC query** (`db.query().all()`)

→ XUNG ĐỘT!

SQLAlchemy async engine không cho phép dùng `.query()` trong async context.

## FIX NHANH

Có 2 cách fix. Tôi khuyên dùng **CÁCH 2** vì đơn giản hơn.

---

### CÁCH 1: Chuyển sang Async Queries (phức tạp)

Sửa file `api_reports.py` - thay tất cả:

```python
# TRÙ́ỚC (SAI):
road_names = db.query(TrafficRecord.road_name).distinct().all()

# SAU (ĐÚNG):
from sqlalchemy import select
result = await db.execute(select(TrafficRecord.road_name).distinct())
road_names = result.scalars().all()
```

**Nhược điểm:** Phải sửa rất nhiều chỗ!

---

### CÁCH 2: Dùng Sync Session cho Reports (khuyên dùng)

Tạo helper function dùng sync engine cho reports.

#### Bước 1: Tạo sync session factory

File: `Backend/app/db/database.py`

Thêm vào cuối file:

```python
# Sync engine for reports (không dùng async)
def get_db_sync():
    """
    Sync database session cho reports
    Dùng khi cần .query() thay vì await
    """
    from sqlalchemy import create_engine
    from sqlalchemy.orm import sessionmaker
    from app.core.config import settings

    # Chuyển async URL sang sync URL
    sync_url = settings.DATABASE_URL.replace("sqlite+aiosqlite://", "sqlite:///")

    sync_engine = create_engine(sync_url, echo=False)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=sync_engine)

    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
```

#### Bước 2: Sửa endpoint export PDF

File: `Backend/app/api/v1/api_reports.py`

Tìm dòng:

```python
@router.post("/reports/export/pdf")
async def export_pdf_report(
    filter_params: ReportFilter,
    db: Session = Depends(get_db)  # ← DÒNG NÀY
):
```

Sửa thành:

```python
@router.post("/reports/export/pdf")
async def export_pdf_report(
    filter_params: ReportFilter,
    db: Session = Depends(get_db_sync)  # ← DÙNG get_db_sync
):
```

Và sửa luôn function `generate_report`:

Tìm:
```python
async def generate_report(
    filter_params: ReportFilter,
    db: Session = Depends(get_db)  # ← DÒNG NÀY
) -> ReportResponse:
```

Sửa thành:
```python
def generate_report(  # ← BỎ async
    filter_params: ReportFilter,
    db: Session  # ← BỎ Depends
) -> ReportResponse:
```

Và sửa chỗ gọi nó:

Tìm:
```python
report = await generate_report(filter_params, db)
```

Sửa thành:
```python
report = generate_report(filter_params, db)  # ← BỎ await
```

#### Bước 3: Làm tương tự cho export Excel

File: `Backend/app/api/v1/api_reports.py`

Tìm:
```python
@router.post("/reports/export/excel")
async def export_excel_report(
    filter_params: ReportFilter,
    db: Session = Depends(get_db)  # ← DÒNG NÀY
):
```

Sửa thành:
```python
@router.post("/reports/export/excel")
async def export_excel_report(
    filter_params: ReportFilter,
    db: Session = Depends(get_db_sync)  # ← DÙNG get_db_sync
):
```

Và sửa chỗ gọi generate_report:
```python
report = generate_report(filter_params, db)  # ← BỎ await
```

---

## KIỂM TRA SAU KHI FIX

### Test 1: Chạy lại server

```bash
cd Backend
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000
```

### Test 2: Test API qua curl

```bash
curl -X POST http://localhost:8000/api/v1/reports/export/pdf ^
  -H "Content-Type: application/json" ^
  -d "{\"start_date\":\"2025-11-20\",\"end_date\":\"2025-11-27\",\"period\":\"day\"}" ^
  --output test_report.pdf
```

Kiểm tra file `test_report.pdf` - phải > 10 KB!

### Test 3: Test qua Frontend

1. Mở Frontend
2. Click "Export PDF"
3. Phải download được file PDF

---

## NẾU VẪN LỖI

Nếu vẫn gặp lỗi khác, có thể do:

### Lỗi: Database không có data

**Fix:** Thêm dữ liệu test:

```bash
cd Backend
python test_full_system.py
```

### Lỗi: Module import error

**Fix:**
```python
# Trong api_reports.py, thêm import
from app.db.database import get_db_sync
```

---

© 2025 - Fix lỗi Export PDF/Excel
