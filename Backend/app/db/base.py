# ============================================================================
# FILE: base.py - DATABASE CONNECTION VÀ SESSION SETUP
# ============================================================================
# File này khởi tạo database engine và session cho toàn bộ ứng dụng
#
# CHỨC NĂNG:
# - Tạo async engine cho SQLite
# - Tạo sessionmaker để tạo AsyncSession
# - Tạo Base class cho tất cả models
# - Cung cấp get_db() dependency để inject vào FastAPI endpoints

# ============================================================================
# PHẦN 1: IMPORT THƯ VIỆN
# ============================================================================

# Dòng 1: Import SQLAlchemy async components
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
# - create_async_engine: Tạo async database engine
# - AsyncSession: Session bất đồng bộ để query database
#
# TẠI SAO ASYNC?
# - FastAPI là async framework
# - Async database không block event loop
# - Có thể handle nhiều requests đồng thời
# - Performance tốt hơn sync database

# Dòng 2: Import sessionmaker và declarative_base
from sqlalchemy.orm import sessionmaker, declarative_base
# - sessionmaker: Factory tạo session instances
# - declarative_base: Tạo base class cho models

# Dòng 3: Import settings
from app.core.config import settings
# settings: Object chứa config (DATABASE_URL, etc.)


# ============================================================================
# PHẦN 2: TẠO DATABASE ENGINE
# ============================================================================

# Dòng 5: Tạo async engine
engine = create_async_engine(settings.DATABASE_URL, future=True, echo=True)
# create_async_engine(): Tạo async database engine
#
# THAM SỐ:
# - settings.DATABASE_URL: Connection string
#   Format: "sqlite+aiosqlite:///./app/traffic_monitor.db"
#   Giải thích:
#     - sqlite: Database type
#     - aiosqlite: Async driver cho SQLite
#     - ./app/traffic_monitor.db: Path to database file
#
# - future=True: Dùng SQLAlchemy 2.0 style
#   Enabled select() thay vì .query()
#   Required cho async operations
#
# - echo=True: Log tất cả SQL queries ra console
#   Useful cho debugging:
#     SELECT * FROM traffic_violations WHERE id = ?
#     INSERT INTO traffic_violations ...
#   Set echo=False trong production để giảm logs

# ENGINE LÀ GÌ?
# - Engine = Connection pool manager
# - Quản lý connections đến database
# - Tự động mở/đóng connections
# - Reuse connections để performance tốt
#
# ENGINE ĐƯỢC DÙNG KHI:
# - Tạo sessions (AsyncSession)
# - Tạo tables (Base.metadata.create_all)
# - Execute raw SQL (await engine.execute())


# ============================================================================
# PHẦN 3: TẠO SESSION FACTORY
# ============================================================================

# Dòng 6: Tạo sessionmaker
AsyncSessionLocal = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

# Factory function để tạo session (dùng cho background tasks)
def get_db_session_factory():
    """
    Trả về sessionmaker để tạo db session trong background tasks

    Returns:
        Async context manager để tạo AsyncSession
    """
    return AsyncSessionLocal
# sessionmaker(): Factory để tạo session instances
#
# THAM SỐ:
# - engine: Async engine đã tạo ở trên
#   Mọi session sẽ dùng engine này để connect database
#
# - class_=AsyncSession: Tạo AsyncSession thay vì Session
#   AsyncSession support async/await
#   Bắt buộc cho async database operations
#
# - expire_on_commit=False: Không expire objects sau commit
#   Giải thích:
#     - Mặc định: Sau commit, objects expire (need reload)
#     - False: Objects vẫn accessible sau commit
#     - Useful khi cần access objects sau commit mà không reload
#
#   VÍ DỤ:
#   violation = TrafficViolation(...)
#   session.add(violation)
#   await session.commit()
#   print(violation.id)  # ✅ OK với expire_on_commit=False
#                        # ❌ Error với expire_on_commit=True (need refresh)

# SESSIONMAKER LÀ GÌ?
# - Factory pattern để tạo sessions
# - Mỗi request tạo 1 session mới
# - Session auto-closed sau khi xong
#
# CÁCH DÙNG:
# async with AsyncSessionLocal() as session:
#     # Use session here
#     result = await session.execute(query)
# # Session auto-closed


# ============================================================================
# PHẦN 4: TẠO BASE CLASS CHO MODELS
# ============================================================================

# Dòng 7: Tạo declarative base
Base = declarative_base()
# declarative_base(): Tạo base class cho tất cả models
#
# TẤT CẢ MODELS PHẢI INHERIT TỪ BASE:
# class TrafficViolation(Base):
#     __tablename__ = "traffic_violations"
#     id = Column(Integer, primary_key=True)
#     ...
#
# BASE CÓ GÌ?
# - __tablename__: Tên bảng trong database
# - metadata: Thông tin về tất cả tables
# - __table__: Table object của model
#
# METADATA LÀ GÌ?
# - Base.metadata: Container chứa tất cả table definitions
# - Dùng để tạo/xóa tables:
#   Base.metadata.create_all(engine)  # Tạo tất cả tables
#   Base.metadata.drop_all(engine)    # Xóa tất cả tables


# ============================================================================
# PHẦN 5: DATABASE SESSION DEPENDENCY
# ============================================================================

# Dòng 8-10: Dependency cho FastAPI endpoints
async def get_db():
    """
    Async generator cung cấp database session cho endpoints

    Đây là DEPENDENCY INJECTION pattern trong FastAPI
    Tự động inject AsyncSession vào endpoint parameters

    CÁCH DÙNG TRONG ENDPOINT:

    @router.get("/violations/list")
    async def get_violations(db: AsyncSession = Depends(get_db)):
        query = select(TrafficViolation)
        result = await db.execute(query)
        return result.scalars().all()

    FLOW:

    1. Request đến endpoint
    2. FastAPI gọi get_db()
    3. get_db() tạo session từ AsyncSessionLocal
    4. yield session → inject vào endpoint
    5. Endpoint sử dụng session
    6. Endpoint return response
    7. Session tự động close (cleanup)

    YIELD VS RETURN:

    yield: Generator pattern
    - Pause function tại yield
    - Resume function sau khi endpoint done
    - Cho phép cleanup code sau yield

    Code sau yield chạy khi:
    - Endpoint return response
    - Exception xảy ra
    - Request canceled

    VÍ DỤ FLOW ĐẦY ĐỦ:

    async def get_db():
        print("1. Creating session...")
        async with AsyncSessionLocal() as session:
            print("2. Session created")
            yield session
            print("4. Cleaning up session...")
        print("5. Session closed")

    @router.get("/test")
    async def test(db: AsyncSession = Depends(get_db)):
        print("3. Using session in endpoint")
        return {"status": "ok"}

    Output:
    1. Creating session...
    2. Session created
    3. Using session in endpoint
    4. Cleaning up session...
    5. Session closed

    ASYNC WITH:

    async with AsyncSessionLocal() as session:
        yield session

    - async with: Async context manager
    - Tự động gọi __aenter__ khi vào block
    - Tự động gọi __aexit__ khi ra khỏi block
    - __aexit__ close session và release connection

    TƯƠNG ĐƯƠNG VỚI:

    session = AsyncSessionLocal()
    try:
        await session.__aenter__()
        yield session
    finally:
        await session.__aexit__(None, None, None)

    LỢI ÍCH:

    1. AUTO CLEANUP:
       - Session luôn được close
       - Không bị memory leak
       - Connection pool không bị exhaust

    2. ISOLATION:
       - Mỗi request có session riêng
       - Không conflict giữa requests
       - Thread-safe

    3. TRANSACTION:
       - Mỗi session có transaction riêng
       - Rollback tự động nếu error
       - Commit manual với await session.commit()

    ERROR HANDLING:

    Nếu endpoint raise exception:
    - Session tự động rollback
    - Session tự động close
    - Exception propagate lên FastAPI
    - FastAPI return error response

    VÍ DỤ:

    @router.post("/violations")
    async def create_violation(db: AsyncSession = Depends(get_db)):
        violation = TrafficViolation(...)
        db.add(violation)
        # Nếu error ở đây → session rollback + close
        await db.commit()  # ❌ Không chạy đến đây nếu có error
        return {"id": violation.id}
    """
    # Dòng 9-10: Create và yield session
    async with AsyncSessionLocal() as session:
        # async with: Context manager
        # - Tự động __aenter__: Initialize session
        # - Tự động __aexit__: Close session khi done

        yield session
        # yield: Pause function và return session
        # FastAPI inject session vào endpoint
        # Sau khi endpoint done, resume function
        # Session auto-closed bởi async with


# ============================================================================
# TỔNG KẾT: KIẾN TRÚC DATABASE
# ============================================================================
"""
===== 1. FLOW TẠO DATABASE =====

app/db/base.py (file này):
┌──────────────────────────────────┐
│ 1. Create Engine                 │
│    - Connection pool manager     │
│    - SQLite + aiosqlite driver   │
└──────────┬───────────────────────┘
           ↓
┌──────────────────────────────────┐
│ 2. Create SessionMaker           │
│    - Factory cho sessions        │
│    - AsyncSession class          │
└──────────┬───────────────────────┘
           ↓
┌──────────────────────────────────┐
│ 3. Create Base                   │
│    - Base class cho models       │
│    - Metadata container          │
└──────────┬───────────────────────┘
           ↓
┌──────────────────────────────────┐
│ 4. Define get_db()               │
│    - Dependency cho endpoints    │
│    - Auto session management     │
└──────────────────────────────────┘

app/models/traffic_violation.py:
┌──────────────────────────────────┐
│ 5. Define Model                  │
│    class TrafficViolation(Base) │
│    - Columns                     │
│    - Indexes                     │
└──────────────────────────────────┘

app/main.py (startup event):
┌──────────────────────────────────┐
│ 6. Create Tables                 │
│    Base.metadata.create_all()    │
│    - Execute CREATE TABLE        │
│    - Execute CREATE INDEX        │
└──────────────────────────────────┘

===== 2. FLOW XỬ LÝ REQUEST =====

Client Request:
GET /api/v1/violations/list

FastAPI Router:
@router.get("/violations/list")
async def get_violations(db: AsyncSession = Depends(get_db)):
    ...

Flow:
1. FastAPI nhận request
2. Call Depends(get_db)
   ↓
3. get_db() tạo session:
   async with AsyncSessionLocal() as session:
       yield session
   ↓
4. Session inject vào endpoint
   ↓
5. Endpoint execute query:
   query = select(TrafficViolation)
   result = await db.execute(query)
   ↓
6. Return response
   ↓
7. Exit async with → session.close()
   ↓
8. Response gửi về client

===== 3. CONNECTION POOLING =====

Engine quản lý connection pool:

Pool (mặc định 5 connections):
┌────────────┐
│ Conn 1     │ ← Request 1 using
├────────────┤
│ Conn 2     │ ← Request 2 using
├────────────┤
│ Conn 3     │ ← Available
├────────────┤
│ Conn 4     │ ← Available
├────────────┤
│ Conn 5     │ ← Available
└────────────┘

Request 6 arrives → Wait for connection
Request 1 done → Release conn 1
Request 6 → Use conn 1

LỢI ÍCH:
- Reuse connections (không tạo mới mỗi request)
- Giới hạn max connections (tránh overload)
- Auto cleanup (close unused connections)

===== 4. ASYNC VS SYNC =====

SYNC (blocking):
def get_data():
    session = SessionLocal()  # Blocking
    result = session.query(Model).all()  # Blocking
    session.close()
    return result

# Event loop blocked! Other requests wait!

ASYNC (non-blocking):
async def get_data():
    async with AsyncSessionLocal() as session:  # Non-blocking
        result = await session.execute(select(Model))  # Non-blocking
    return result.scalars().all()

# Event loop free! Other requests processed!

PERFORMANCE:
- Sync: 1 request/time → 10 req/sec
- Async: 100 requests/time → 1000 req/sec (với I/O)

===== 5. SESSION LIFECYCLE =====

Session States:
┌──────────────┐
│  Transient   │ ← Object created, not in session
└──────┬───────┘
       │ session.add(obj)
       ↓
┌──────────────┐
│   Pending    │ ← Object in session, not in database
└──────┬───────┘
       │ await session.commit()
       ↓
┌──────────────┐
│  Persistent  │ ← Object in database, in session
└──────┬───────┘
       │ session.close()
       ↓
┌──────────────┐
│   Detached   │ ← Object out of session

VÍ DỤ:
# Transient
violation = TrafficViolation(...)

# Pending
session.add(violation)

# Persistent
await session.commit()
print(violation.id)  # Has ID now

# Detached
session.close()
# violation.id still accessible
# But violation.camera_name might not (depends on expire_on_commit)

===== 6. TRANSACTION MANAGEMENT =====

Mỗi session có 1 transaction:

BEGIN TRANSACTION
├─ INSERT violation 1
├─ INSERT violation 2
├─ UPDATE violation 3
└─ COMMIT

Nếu error:
BEGIN TRANSACTION
├─ INSERT violation 1  ✓
├─ INSERT violation 2  ✓
├─ UPDATE violation 3  ✗ ERROR!
└─ ROLLBACK (discard all changes)

AUTO ROLLBACK VỚI ASYNC WITH:
async with AsyncSessionLocal() as session:
    session.add(obj1)  # ✓
    session.add(obj2)  # ✓
    raise Exception()  # ✗ ERROR
# auto rollback + close

MANUAL TRANSACTION:
async with AsyncSessionLocal() as session:
    try:
        session.add(obj1)
        await session.commit()
        session.add(obj2)
        await session.commit()
    except Exception:
        await session.rollback()
        raise

===== 7. BEST PRACTICES =====

1. ALWAYS USE ASYNC:
   ✓ async with AsyncSessionLocal() as session:
   ✗ session = AsyncSessionLocal()  # Need manual close

2. ONE SESSION PER REQUEST:
   ✓ db: AsyncSession = Depends(get_db)
   ✗ global_session = AsyncSessionLocal()  # Shared!

3. DON'T SHARE SESSIONS:
   ✗ Pass session between functions
   ✓ Inject session via Depends

4. COMMIT EXPLICITLY:
   ✗ Auto-commit (SQLAlchemy 2.0 không có)
   ✓ await session.commit()

5. HANDLE ERRORS:
   try:
       await session.commit()
   except IntegrityError:
       await session.rollback()
       raise HTTPException(400, "Duplicate entry")

===== 8. DATABASE FILE LOCATION =====

SQLite file: ./Backend/app/traffic_monitor.db

Relative to: Backend/ directory (where main.py runs)

Full path example:
d:/KHKT_TRI/KHKT-NEWUPDATE/Smart-Trafic-Monitoring-System-main/Backend/app/traffic_monitor.db

Check nếu file exists:
import os
os.path.exists("./app/traffic_monitor.db")

===== 9. DEBUGGING =====

Enable SQL logging (echo=True):
engine = create_async_engine(..., echo=True)

Console output:
2025-11-10 14:30:25,123 INFO sqlalchemy.engine.Engine
SELECT traffic_violations.id, traffic_violations.camera_name
FROM traffic_violations
WHERE traffic_violations.is_processed = ?
2025-11-10 14:30:25,124 INFO sqlalchemy.engine.Engine [cached since 0.001s ago] (0,)

Disable trong production (echo=False):
- Giảm logs
- Improve performance
- Avoid sensitive data in logs

===== 10. COMMON PATTERNS =====

PATTERN 1: Simple Query
@router.get("/violations")
async def get_all(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(TrafficViolation))
    return result.scalars().all()

PATTERN 2: Filter Query
async def get_by_camera(camera: str, db: AsyncSession = Depends(get_db)):
    query = select(TrafficViolation).filter(TrafficViolation.camera_name == camera)
    result = await db.execute(query)
    return result.scalars().all()

PATTERN 3: Insert
async def create(data: dict, db: AsyncSession = Depends(get_db)):
    violation = TrafficViolation(**data)
    db.add(violation)
    await db.commit()
    await db.refresh(violation)
    return violation

PATTERN 4: Update
async def update(id: int, data: dict, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(TrafficViolation).filter(TrafficViolation.id == id))
    violation = result.scalar_one_or_none()
    if not violation:
        raise HTTPException(404)

    for key, value in data.items():
        setattr(violation, key, value)

    await db.commit()
    return violation

PATTERN 5: Delete
async def delete(id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(TrafficViolation).filter(TrafficViolation.id == id))
    violation = result.scalar_one_or_none()
    if not violation:
        raise HTTPException(404)

    await db.delete(violation)
    await db.commit()
    return {"message": "Deleted"}

END OF DOCUMENTATION
"""
