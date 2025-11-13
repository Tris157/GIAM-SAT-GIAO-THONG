# ============================================================================
# FILE: traffic_violation.py - DATABASE MODEL CHO VI PHẠM GIAO THÔNG
# ============================================================================
# File này định nghĩa SQLAlchemy model cho bảng traffic_violations trong database
# Model này map Python class → Database table
#
# CHỨC NĂNG:
# - Định nghĩa schema của bảng traffic_violations
# - Tạo indexes để tối ưu query performance
# - Sử dụng trong tất cả API endpoints để CRUD violations

# ============================================================================
# PHẦN 1: IMPORT THƯ VIỆN
# ============================================================================

# Dòng 1: Import SQLAlchemy column types và Index
from sqlalchemy import Column, Integer, String, DateTime, Float, Boolean, Index
# - Column: Định nghĩa cột trong bảng
# - Integer: Kiểu số nguyên (id, hour_of_day)
# - String: Kiểu chuỗi (camera_name, violation_type, etc.)
# - DateTime: Kiểu datetime với timezone
# - Float: Kiểu số thực (position_x, position_y, confidence)
# - Boolean: Kiểu True/False (is_processed)
# - Index: Tạo database index để query nhanh hơn

# Dòng 2: Import func cho SQL functions
from sqlalchemy.sql import func
# func: Chứa các SQL functions như NOW(), COUNT(), SUM()
# Dùng func.now() để set default timestamp khi insert

# Dòng 3: Import Base class
from app.db.base import Base
# Base: Declarative base của SQLAlchemy
# Tất cả models phải inherit từ Base


# ============================================================================
# PHẦN 2: TRAFFIC VIOLATION MODEL
# ============================================================================

# Dòng 6-8: Định nghĩa class model
class TrafficViolation(Base):
    """
    Model SQLAlchemy cho bảng traffic_violations

    Model này lưu trữ thông tin về các vi phạm giao thông:
    - Vi phạm vượt đèn đỏ (red_light)
    - Vi phạm vượt tốc độ (speeding)
    - Vi phạm đi sai làn (wrong_lane)

    ===== CẤU TRÚC BẢNG =====

    traffic_violations
    ├── id (PK)                    - ID duy nhất
    ├── camera_name                - Tên camera phát hiện
    ├── violation_type             - Loại vi phạm
    ├── vehicle_type               - Loại xe
    ├── image_path                 - Đường dẫn ảnh bằng chứng
    ├── position_x, position_y     - Vị trí vi phạm
    ├── traffic_light_status       - Màu đèn lúc vi phạm
    ├── violated_at                - Timestamp vi phạm
    ├── date                       - Ngày vi phạm (YYYY-MM-DD)
    ├── hour_of_day                - Giờ vi phạm (0-23)
    ├── is_processed               - Đã xử lý chưa?
    ├── note                       - Ghi chú
    └── confidence                 - Độ tin cậy YOLO

    ===== INDEXES =====

    Single column indexes:
    - id (primary key, auto index)
    - camera_name (index=True)
    - violation_type (index=True)
    - violated_at (index=True)
    - date (index=True)
    - hour_of_day (index=True)
    - is_processed (index=True)

    Composite indexes (query nhanh hơn khi filter nhiều cột):
    - (camera_name, date)
    - (violation_type, date)
    - (is_processed, date)

    ===== VÍ DỤ RECORD =====

    {
        "id": 1,
        "camera_name": "camera_live",
        "violation_type": "red_light",
        "vehicle_type": "car",
        "image_path": "./app/static/violation_images/violation_camera_live_20251110.jpg",
        "position_x": 150.5,
        "position_y": 420.0,
        "traffic_light_status": "red",
        "violated_at": "2025-11-10T14:30:25.123456+07:00",
        "date": "2025-11-10",
        "hour_of_day": 14,
        "is_processed": False,
        "note": None,
        "confidence": 0.95
    }
    """

    # Dòng 8: Tên bảng trong database
    __tablename__ = "traffic_violations"
    # __tablename__: Tên bảng SQL
    # SQLAlchemy sẽ tạo bảng với tên này trong database

    # ========================================================================
    # PHẦN 2.1: PRIMARY KEY
    # ========================================================================

    # Dòng 10: ID - Primary Key
    id = Column(Integer, primary_key=True, index=True)
    # - Integer: Kiểu số nguyên
    # - primary_key=True: Đây là primary key (unique, not null)
    # - index=True: Tạo index (tự động với primary key)
    # - Auto-increment: SQLite tự động tăng id khi insert
    #
    # VÍ DỤ: 1, 2, 3, 4, ...

    # ========================================================================
    # PHẦN 2.2: THÔNG TIN CAMERA
    # ========================================================================

    # Dòng 12-13: Tên camera
    camera_name = Column(String, index=True, nullable=False)
    # - String: Kiểu chuỗi (VARCHAR trong SQL)
    # - index=True: Tạo index để query theo camera nhanh
    # - nullable=False: Bắt buộc phải có (NOT NULL)
    #
    # VÍ DỤ: "camera_live", "camera_1", "camera_highway_1"
    #
    # INDEX: Tạo index để query này nhanh:
    #   SELECT * FROM traffic_violations WHERE camera_name = 'camera_live'

    # ========================================================================
    # PHẦN 2.3: LOẠI VI PHẠM
    # ========================================================================

    # Dòng 15-16: Loại vi phạm
    violation_type = Column(String, default="red_light", index=True)
    # - default="red_light": Giá trị mặc định nếu không chỉ định
    # - index=True: Index để filter theo loại vi phạm
    #
    # CÁC GIÁ TRỊ HỢP LỆ:
    # - "red_light": Vượt đèn đỏ (phổ biến nhất)
    # - "speeding": Vượt tốc độ
    # - "wrong_lane": Đi sai làn
    #
    # INDEX: Query nhanh:
    #   SELECT * FROM traffic_violations WHERE violation_type = 'red_light'

    # ========================================================================
    # PHẦN 2.4: THÔNG TIN PHƯƠNG TIỆN
    # ========================================================================

    # Dòng 18-19: Loại xe
    vehicle_type = Column(String, nullable=False)
    # - nullable=False: Bắt buộc phải có
    # - Không index vì ít khi query riêng theo vehicle_type
    #
    # CÁC GIÁ TRỊ HỢP LỆ:
    # - "car": Ô tô
    # - "motor" / "motorcycle": Xe máy
    # - "truck": Xe tải
    # - "bus": Xe buýt
    #
    # Giá trị này đến từ YOLO detection (class name)

    # ========================================================================
    # PHẦN 2.5: ẢNH BẰNG CHỨNG
    # ========================================================================

    # Dòng 21-22: Đường dẫn ảnh
    image_path = Column(String, nullable=False)
    # - nullable=False: Bắt buộc phải có ảnh
    # - Lưu relative path, không phải full path
    #
    # FORMAT: "./app/static/violation_images/violation_camera_live_20251110_143025_123456.jpg"
    #
    # CÁCH SỬ DỤNG:
    # 1. Backend lưu ảnh vào ./app/static/violation_images/
    # 2. Lưu path này vào database
    # 3. Frontend fetch: http://localhost:8000/static/violation_images/violation_....jpg
    #
    # LƯU Ý:
    # - File name có timestamp → unique, không bị trùng
    # - Static files được serve qua FastAPI StaticFiles

    # ========================================================================
    # PHẦN 2.6: VỊ TRÍ VI PHẠM
    # ========================================================================

    # Dòng 24-26: Tọa độ vị trí
    position_x = Column(Float)
    position_y = Column(Float)
    # - Float: Số thực (có thể có số lẻ)
    # - nullable=True (default): Có thể null
    #
    # GIÁ TRỊ:
    # - position_x: Tọa độ X của bottom center bbox (pixel)
    # - position_y: Tọa độ Y của bottom bbox (pixel)
    #
    # VÍ DỤ:
    # - position_x: 150.5 (xe ở giữa màn hình ngang)
    # - position_y: 420.0 (xe vượt qua vạch dừng Y=400)
    #
    # CÁCH DÙNG:
    # - Vẽ lại vị trí xe trên ảnh
    # - Phân tích heatmap vi phạm
    # - Xác định làn xe vi phạm nhiều nhất

    # ========================================================================
    # PHẦN 2.7: TRẠNG THÁI ĐÈN
    # ========================================================================

    # Dòng 28-29: Màu đèn lúc vi phạm
    traffic_light_status = Column(String, nullable=False)
    # - nullable=False: Bắt buộc phải có
    #
    # CÁC GIÁ TRỊ HỢP LỆ:
    # - "red": Đèn đỏ (vi phạm chắc chắn)
    # - "yellow": Đèn vàng (vi phạm nếu strict mode)
    # - "green": Đèn xanh (không vi phạm, bug?)
    #
    # LƯU Ý:
    # - Giá trị này đến từ RedLightDetector.detect_light_color()
    # - Nếu detection lỗi → cần review lại ảnh

    # ========================================================================
    # PHẦN 2.8: THỜI GIAN
    # ========================================================================

    # Dòng 31-34: Timestamp và derived fields

    # Dòng 32: Timestamp chính xác
    violated_at = Column(DateTime(timezone=True), server_default=func.now(), index=True)
    # - DateTime(timezone=True): Lưu timezone (UTC+7 cho VN)
    # - server_default=func.now(): Auto set timestamp khi insert
    # - index=True: Index để sort và filter theo thời gian
    #
    # FORMAT: "2025-11-10T14:30:25.123456+07:00" (ISO 8601)
    #
    # SQL EQUIVALENT:
    #   violated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
    #
    # CÁCH DÙNG:
    #   SELECT * FROM traffic_violations
    #   WHERE violated_at >= '2025-11-10 00:00:00'
    #   ORDER BY violated_at DESC

    # Dòng 33: Ngày (YYYY-MM-DD)
    date = Column(String, index=True)
    # - String: Lưu dạng text "2025-11-10"
    # - index=True: Index để query theo ngày nhanh
    # - Derived từ violated_at (extract date part)
    #
    # TẠI SAO DÙNG STRING THAY VÌ DATE?
    # - Dễ dàng query: WHERE date = '2025-11-10'
    # - Không cần convert timezone
    # - SQLite không có DATE type riêng
    #
    # CÁCH DÙNG:
    #   SELECT * FROM traffic_violations
    #   WHERE date = '2025-11-10'
    #   GROUP BY date

    # Dòng 34: Giờ trong ngày
    hour_of_day = Column(Integer, index=True)
    # - Integer: 0-23 (24-hour format)
    # - index=True: Index để phân tích theo giờ
    # - Derived từ violated_at (extract hour)
    #
    # VÍ DỤ:
    # - 14:30:25 → hour_of_day = 14
    # - 09:15:00 → hour_of_day = 9
    # - 23:59:59 → hour_of_day = 23
    #
    # CÁCH DÙNG:
    #   SELECT hour_of_day, COUNT(*)
    #   FROM traffic_violations
    #   GROUP BY hour_of_day
    #   ORDER BY COUNT(*) DESC
    # → Tìm giờ nào có nhiều vi phạm nhất

    # ========================================================================
    # PHẦN 2.9: TRẠNG THÁI XỬ LÝ
    # ========================================================================

    # Dòng 36-37: Đã xử lý chưa
    is_processed = Column(Boolean, default=False, index=True)
    # - Boolean: True/False (1/0 trong SQLite)
    # - default=False: Mặc định chưa xử lý
    # - index=True: Index để filter vi phạm chưa xử lý
    #
    # WORKFLOW:
    # 1. Vi phạm mới: is_processed = False
    # 2. Admin xem và xử lý → call API PUT /violations/{id}/process
    # 3. Update: is_processed = True
    #
    # QUERY PHỔ BIẾN:
    #   SELECT * FROM traffic_violations
    #   WHERE is_processed = False
    #   ORDER BY violated_at DESC
    # → Lấy vi phạm chưa xử lý, mới nhất trước

    # ========================================================================
    # PHẦN 2.10: GHI CHÚ
    # ========================================================================

    # Dòng 39-40: Ghi chú
    note = Column(String, nullable=True)
    # - nullable=True: Có thể null (optional)
    # - Không index vì ít khi query theo note
    #
    # VÍ DỤ:
    # - "Đã xử phạt 1.000.000 VNĐ"
    # - "Xe không có biển số"
    # - "False positive - xe dừng đúng luật"
    #
    # CÁCH DÙNG:
    # Admin có thể thêm note khi mark as processed:
    #   PUT /violations/123/process?note=Đã xử phạt

    # ========================================================================
    # PHẦN 2.11: CONFIDENCE SCORE
    # ========================================================================

    # Dòng 42-43: Độ tin cậy YOLO
    confidence = Column(Float, default=1.0)
    # - Float: 0.0 - 1.0 (0% - 100%)
    # - default=1.0: Mặc định 100% (nếu không có YOLO conf)
    #
    # GIÁ TRỊ:
    # - 0.95: YOLO 95% chắc chắn đây là xe
    # - 0.50: YOLO 50% chắc chắn (low confidence)
    # - 1.0: Default (không có confidence từ detector)
    #
    # CÁCH DÙNG:
    # - Filter vi phạm có confidence thấp để review:
    #   SELECT * FROM traffic_violations WHERE confidence < 0.7
    # - Chỉ hiển thị vi phạm confidence cao:
    #   SELECT * FROM traffic_violations WHERE confidence >= 0.9

    # ========================================================================
    # PHẦN 2.12: COMPOSITE INDEXES
    # ========================================================================

    # Dòng 45-50: Tạo composite indexes
    __table_args__ = (
        Index('idx_camera_date', 'camera_name', 'date'),
        Index('idx_violation_type_date', 'violation_type', 'date'),
        Index('idx_processed_date', 'is_processed', 'date'),
    )
    # __table_args__: Tuple chứa table-level arguments
    #
    # COMPOSITE INDEX = INDEX NHIỀU CỘT
    # Tối ưu cho queries filter nhiều cột cùng lúc

    # Index 1: (camera_name, date)
    # TỐI ƯU CHO:
    #   SELECT * FROM traffic_violations
    #   WHERE camera_name = 'camera_live' AND date = '2025-11-10'
    #
    # KHÔNG TỐI ƯU CHO:
    #   SELECT * FROM traffic_violations WHERE date = '2025-11-10'
    # (Vì date không phải cột đầu tiên trong index)

    # Index 2: (violation_type, date)
    # TỐI ƯU CHO:
    #   SELECT * FROM traffic_violations
    #   WHERE violation_type = 'red_light' AND date = '2025-11-10'

    # Index 3: (is_processed, date)
    # TỐI ƯU CHO:
    #   SELECT * FROM traffic_violations
    #   WHERE is_processed = False AND date = '2025-11-10'
    # Rất phổ biến: Lấy vi phạm chưa xử lý hôm nay


# ============================================================================
# TỔNG KẾT: CÁCH SỬ DỤNG MODEL
# ============================================================================
"""
===== 1. TẠO BẢNG =====

Trong app/db/base.py có code:

async with engine.begin() as conn:
    await conn.run_sync(Base.metadata.create_all)

Code này sẽ tạo bảng với SQL:

CREATE TABLE traffic_violations (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    camera_name VARCHAR NOT NULL,
    violation_type VARCHAR DEFAULT 'red_light',
    vehicle_type VARCHAR NOT NULL,
    image_path VARCHAR NOT NULL,
    position_x REAL,
    position_y REAL,
    traffic_light_status VARCHAR NOT NULL,
    violated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    date VARCHAR,
    hour_of_day INTEGER,
    is_processed BOOLEAN DEFAULT 0,
    note VARCHAR,
    confidence REAL DEFAULT 1.0
);

CREATE INDEX ix_traffic_violations_camera_name ON traffic_violations (camera_name);
CREATE INDEX ix_traffic_violations_violation_type ON traffic_violations (violation_type);
CREATE INDEX idx_camera_date ON traffic_violations (camera_name, date);
... (các indexes khác)

===== 2. INSERT VIOLATION =====

Trong RedLightDetector.check_violation():

from app.models.traffic_violation import TrafficViolation
from datetime import datetime

# Tạo object
violation = TrafficViolation(
    camera_name="camera_live",
    violation_type="red_light",
    vehicle_type="car",
    image_path="./app/static/violation_images/violation_camera_live_20251110.jpg",
    position_x=150.5,
    position_y=420.0,
    traffic_light_status="red",
    violated_at=datetime.now(),
    date="2025-11-10",
    hour_of_day=14,
    is_processed=False,
    confidence=0.95
)

# Insert vào database
async with AsyncSession(engine) as session:
    session.add(violation)
    await session.commit()

===== 3. QUERY VIOLATIONS =====

# Lấy tất cả vi phạm
from sqlalchemy import select

query = select(TrafficViolation)
result = await db.execute(query)
violations = result.scalars().all()

# Filter theo camera
query = select(TrafficViolation).filter(
    TrafficViolation.camera_name == "camera_live"
)

# Filter vi phạm chưa xử lý
query = select(TrafficViolation).filter(
    TrafficViolation.is_processed == False
)

# Filter theo ngày
query = select(TrafficViolation).filter(
    TrafficViolation.date == "2025-11-10"
)

# Kết hợp nhiều filters
query = select(TrafficViolation).filter(
    TrafficViolation.camera_name == "camera_live",
    TrafficViolation.date == "2025-11-10",
    TrafficViolation.is_processed == False
)

# Sort theo thời gian
query = query.order_by(TrafficViolation.violated_at.desc())

# Pagination
query = query.offset(0).limit(100)

===== 4. UPDATE VIOLATION =====

# Lấy violation
query = select(TrafficViolation).filter(TrafficViolation.id == 123)
result = await db.execute(query)
violation = result.scalar_one_or_none()

# Update
violation.is_processed = True
violation.note = "Đã xử phạt"

# Commit
await db.commit()
await db.refresh(violation)

===== 5. DELETE VIOLATION =====

# Lấy violation
query = select(TrafficViolation).filter(TrafficViolation.id == 123)
result = await db.execute(query)
violation = result.scalar_one_or_none()

# Delete
await db.delete(violation)
await db.commit()

===== 6. AGGREGATE QUERIES =====

from sqlalchemy import func

# Đếm vi phạm theo ngày
query = select(
    TrafficViolation.date,
    func.count(TrafficViolation.id).label('total')
).group_by(TrafficViolation.date)

result = await db.execute(query)
stats = result.all()

# Đếm vi phạm theo giờ
query = select(
    TrafficViolation.hour_of_day,
    func.count(TrafficViolation.id).label('total')
).group_by(TrafficViolation.hour_of_day)

# Đếm vi phạm theo loại
query = select(
    TrafficViolation.violation_type,
    func.count(TrafficViolation.id).label('total')
).group_by(TrafficViolation.violation_type)

===== 7. INDEX PERFORMANCE =====

WITHOUT INDEXES:
SELECT * FROM traffic_violations WHERE camera_name = 'camera_live'
→ Full table scan (O(n)) - SLOW

WITH INDEX:
SELECT * FROM traffic_violations WHERE camera_name = 'camera_live'
→ Index scan (O(log n)) - FAST

COMPOSITE INDEX EXAMPLE:
SELECT * FROM traffic_violations
WHERE camera_name = 'camera_live' AND date = '2025-11-10'

Without composite index:
1. Scan index camera_name → 1000 rows
2. Filter date from 1000 rows → SLOW

With composite index (camera_name, date):
1. Direct lookup → 10 rows → FAST!

===== 8. DATABASE FILE =====

SQLite database file location:
./Backend/app/traffic_monitor.db

Có thể mở bằng:
- sqlite3 CLI: sqlite3 traffic_monitor.db
- DB Browser for SQLite (GUI)
- Python: sqlite3.connect('traffic_monitor.db')

===== 9. MIGRATION =====

Khi thay đổi model (thêm/xóa column):

Option 1: Delete database và tạo lại (DEV only)
rm traffic_monitor.db
# Restart server → auto create new database

Option 2: Dùng Alembic (PRODUCTION)
alembic revision --autogenerate -m "Add new column"
alembic upgrade head

===== 10. BEST PRACTICES =====

1. INDEXES:
   - Index các cột thường query (WHERE, ORDER BY)
   - Composite index cho multi-column queries
   - Tránh index quá nhiều → slow INSERT

2. NULLABLE:
   - Chỉ nullable=True nếu thực sự optional
   - Foreign keys: nullable=False
   - Required fields: nullable=False

3. DEFAULT VALUES:
   - Set default cho boolean: default=False
   - Set default cho enums: default="red_light"
   - Dùng server_default cho timestamp

4. DATA TYPES:
   - Integer cho ID, counts, hours
   - Float cho coordinates, confidence
   - String cho text, enums
   - DateTime cho timestamps
   - Boolean cho flags

5. PERFORMANCE:
   - Dùng select() thay vì .query() (SQLAlchemy 2.0)
   - Pagination với offset/limit
   - Eager loading cho relationships
   - Bulk insert khi có nhiều records

END OF DOCUMENTATION
"""
