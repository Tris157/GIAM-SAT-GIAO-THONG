# ============================================================================
# FILE: main.py - ĐIỂM BẮT ĐẦU CỦA BACKEND SERVER
# ============================================================================
# File này là nơi khởi tạo và cấu hình toàn bộ FastAPI application
# Khi chạy: uvicorn app.main:app --reload
# Uvicorn sẽ tìm biến 'app' trong file này và khởi chạy server

# ============================================================================
# PHẦN 1: IMPORT CÁC THƯ VIỆN CẦN THIẾT
# ============================================================================

import os  # Module để làm việc với hệ điều hành (đọc biến môi trường, path, v.v.)
import sys  # Module để tương tác với Python interpreter (exit, argv, v.v.)
import signal  # Module để xử lý tín hiệu hệ thống (Ctrl+C, kill, v.v.)
import asyncio  # Module để lập trình bất đồng bộ (async/await)

# Fix UTF-8 encoding cho Windows console
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

# Import các router API từ thư mục api/v1
from app.api.v1 import api_vehicles_frames  # Router xử lý xe cộ và frames video
from app.api.v1 import api_chatbot  # Router xử lý chatbot AI
from app.api.v1 import api_reports  # Router xử lý báo cáo và export
from app.api.v1 import api_rtsp  # Router xử lý camera RTSP real-time
from app.api.v1 import api_auth  # Router xử lý đăng nhập/đăng ký
from app.api.v1 import api_weather  # Router xử lý thông tin thời tiết
from app.api.v1 import api_violations  # Router xử lý vi phạm giao thông
from app.api.v1 import api_debug_light  # Router DEBUG light detection (NEW)
from app.api.v1 import state  # Module lưu trạng thái global (analyzer, v.v.)

from fastapi import FastAPI  # Framework web FastAPI chính
from fastapi.middleware.cors import CORSMiddleware  # Middleware xử lý CORS (cho phép frontend gọi API)
from fastapi.staticfiles import StaticFiles  # Serve static files (images, CSS, v.v.)
from starlette.responses import RedirectResponse  # Response để redirect URL

from app.db.database import create_tables  # Hàm tạo bảng database (cũ, đã comment)
from app.services.traffic_data_scheduler import init_scheduler, get_scheduler  # Scheduler tự động lưu data
from app.models.traffic_violation import TrafficViolation  # Model vi phạm - import để SQLAlchemy biết
from app.db.base import Base, engine as async_engine  # Base class và engine cho async database
from sqlalchemy import create_engine  # Import sync engine để tạo tables

# ============================================================================
# PHẦN 2: CẤU HÌNH BIẾN MÔI TRƯỜNG
# ============================================================================
# Các biến môi trường này ảnh hưởng đến cách OpenCV xử lý video

# Dòng 23: Tắt MSMF (Media Foundation) của Windows
# Lý do: MSMF đôi khi gây kẹt khi nhấn Ctrl+C, khó tắt server
os.environ["OPENCV_VIDEOIO_PRIORITY_MSMF"] = "0"  # 0 = tắt MSMF

# Dòng 24: Ưu tiên sử dụng DirectShow thay vì MSMF
# DirectShow: API video cũ của Windows, ổn định hơn cho real-time streaming
os.environ["OPENCV_VIDEOIO_PRIORITY_DSHOW"] = "1"  # 1 = bật DirectShow

# Dòng 27: Cho phép duplicate OpenMP libraries
# Lý do: NumPy, PyTorch, OpenCV đều có OpenMP riêng → xung đột
# "TRUE" = bỏ qua warning về duplicate libraries
os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"

# ============================================================================
# PHẦN 3: KHỞI TẠO FASTAPI APPLICATION
# ============================================================================

# Dòng 30: Tạo instance FastAPI chính
# Đây là "app" mà uvicorn sẽ chạy
app = FastAPI(
    title="Smart Traffic Monitoring System API",  # Tên hiển thị trong docs
    version="2.0.0"  # Phiên bản API
)

# Dòng 31-37: Thêm CORS Middleware
# CORS = Cross-Origin Resource Sharing
# Cho phép Frontend (localhost:5173) gọi API Backend (localhost:8000)
app.add_middleware(
    CORSMiddleware,  # Class xử lý CORS
    allow_origins=["*"],  # ["*"] = cho phép TẤT CẢ domain gọi API (dev only, production nên giới hạn)
    allow_credentials=True,  # Cho phép gửi cookies và auth headers
    allow_methods=["*"],  # Cho phép tất cả HTTP methods (GET, POST, PUT, DELETE, v.v.)
    allow_headers=["*"],  # Cho phép tất cả headers
)

# ============================================================================
# PHẦN 4: SỰ KIỆN KHỞI ĐỘNG SERVER (STARTUP)
# ============================================================================

# Decorator để đăng ký hàm chạy KHI SERVER BẮT ĐẦU
@app.on_event("startup")
async def startup_event():
    """
    Hàm này chạy MỘT LẦN duy nhất khi server khởi động
    Nhiệm vụ: Setup database, analyzer, scheduler, Telegram bot
    """
    import traceback

    print("🚀 Bắt đầu startup event...")

    # --- BƯỚC 1: TẠO BẢNG DATABASE ---
    try:
        print("⏳ Đang tạo database tables...")
        # Dùng sync engine để tạo tables (tránh async deadlock)
        # Đổi sqlite+aiosqlite thành sqlite
        from app.core.config import settings
        sync_db_url = settings.DATABASE_URL.replace("sqlite+aiosqlite", "sqlite")
        sync_engine = create_engine(sync_db_url, echo=False)
        Base.metadata.create_all(sync_engine)
        sync_engine.dispose()  # Đóng connection ngay lập tức
        print("✅ Database tables created successfully")
    except Exception as e:
        print(f"❌ Database creation failed: {e}")
        traceback.print_exc()
        raise

    # --- BƯỚC 2: KHỞI TẠO ANALYZER (BACKGROUND THREAD - KHÔNG BLOCK) ---
    try:
        print("⏳ Analyzer sẽ được khởi tạo trong background thread...")

        # Sử dụng Thread thay vì asyncio để KHÔNG BLOCK startup event
        import threading

        def init_analyzer_thread():
            try:
                import time
                time.sleep(2)  # Đợi server sẵn sàng
                print("🔄 Background Thread: Bắt đầu init analyzer...")
                state.init_analyzer()
                print("✅ Background Thread: Analyzer đã khởi tạo xong!")
            except Exception as e:
                print(f"❌ Background Thread: Analyzer init failed: {e}")
                traceback.print_exc()

        # Tạo daemon thread - chạy độc lập, KHÔNG block main thread
        analyzer_thread = threading.Thread(target=init_analyzer_thread, daemon=True)
        analyzer_thread.start()
        print("✅ Analyzer background thread started (không đợi init xong)")
    except Exception as e:
        print(f"❌ Failed to create analyzer thread: {e}")
        traceback.print_exc()

    # --- BƯỚC 3: SCHEDULER (AUTO-SAVE DATA) ---
    try:
        async def start_scheduler_when_ready():
            try:
                print("🔄 Background: Đang chờ analyzer khởi tạo...")
                # Đợi analyzer khởi tạo xong
                while state.analyzer is None:
                    await asyncio.sleep(1)

                print("🔄 Background: Bắt đầu khởi động scheduler...")
                # Khởi động scheduler
                scheduler = init_scheduler(state.analyzer, interval_seconds=10)
                await scheduler.start()
                print("✅ Traffic data auto-save scheduler started (interval: 10s)")
            except Exception as e:
                print(f"❌ Background: Scheduler failed: {e}")
                traceback.print_exc()

        asyncio.create_task(start_scheduler_when_ready())
        print("✅ Scheduler background task created")
    except Exception as e:
        print(f"❌ Failed to create scheduler task: {e}")
        traceback.print_exc()

    # --- BƯỚC 4: KẾT NỐI RTSP CAMERA ---
    from app.core.config import settings
    if settings.ENABLE_RTSP and settings.RTSP_URL:
        try:
            from app.api.v1.api_rtsp import rtsp_detection_manager, read_rtsp_detection_frames
            print(f"🔄 Connecting to RTSP Camera: {settings.RTSP_URL}...")
            success = rtsp_detection_manager.add_stream("camera_live", settings.RTSP_URL)
            if success:
                print("✅ RTSP camera connected")
                asyncio.create_task(read_rtsp_detection_frames("camera_live"))
            else:
                print("❌ Failed to connect to RTSP camera")
        except Exception as e:
            print(f"❌ Error connecting to RTSP: {e}")
    else:
        print("ℹ️ RTSP camera: Disabled (Enable in .env)")

    # --- BƯỚC 5: KHỞI ĐỘNG TELEGRAM BOT (BACKGROUND THREAD) ---
    try:
        print("🔄 Telegram Bot sẽ được khởi tạo trong background...")

        # Sử dụng Thread để không block startup event
        def init_telegram_bot_thread():
            try:
                import time
                time.sleep(5)  # Đợi server sẵn sàng
                print("🔄 Background Thread: Bắt đầu init Telegram Bot...")

                # Import và khởi động bot
                from app.services.telegram_polling import get_polling_service
                from app.db.base import get_db_session_factory
                import asyncio

                polling_service = get_polling_service()
                db_factory = get_db_session_factory()

                # Tạo event loop mới cho thread này
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                loop.run_until_complete(polling_service.start_polling(db_factory))

                print("✅ Background Thread: Telegram Bot đã khởi tạo xong!")
            except Exception as e:
                print(f"❌ Background Thread: Telegram Bot init failed: {e}")
                traceback.print_exc()

        # Tạo daemon thread
        telegram_thread = threading.Thread(target=init_telegram_bot_thread, daemon=True)
        telegram_thread.start()
        print("✅ Telegram Bot background thread started (không đợi init xong)")
    except Exception as e:
        print(f"⚠️ Failed to create Telegram Bot thread: {e}")
        print("   (Bot sẽ không hoạt động, nhưng hệ thống vẫn chạy)")
        traceback.print_exc()

    print("\n" + "="*60)
    print("🎉 STARTUP EVENT HOÀN THÀNH!")
    print("="*60 + "\n")

# ============================================================================
# PHẦN 5: XỬ LÝ TÍN HIỆU (CTRL+C)
# ============================================================================

# Dòng 74-79: Hàm xử lý khi người dùng nhấn Ctrl+C
def signal_handler(signum, frame):
    """
    Xử lý tín hiệu SIGINT (Ctrl+C) và SIGTERM (kill)
    Cleanup trước khi thoát để tránh leak resources
    """
    print("\nĐang shutdown server...")  # Thông báo đang tắt
    if state.analyzer:  # Nếu analyzer đang chạy
        state.analyzer.cleanup_processes()  # Dọn dẹp processes, threads, cameras
    sys.exit(0)  # Thoát chương trình với code 0 (thành công)

# Dòng 82-83: Đăng ký signal handler
# Khi nhấn Ctrl+C hoặc kill process → gọi signal_handler()
signal.signal(signal.SIGINT, signal_handler)  # SIGINT = Ctrl+C
signal.signal(signal.SIGTERM, signal_handler)  # SIGTERM = kill command

# ============================================================================
# PHẦN 6: ĐỊNH NGHĨA ROUTES (API ENDPOINTS)
# ============================================================================

# Dòng 85-87: Route root "/" redirect về frontend
@app.get(path='/')  # GET request đến "/"
def direct_home():
    # Redirect người dùng về frontend (React app)
    return RedirectResponse(url='http://localhost:5173/')

# Dòng 89-95: Đăng ký các router (nhóm các endpoints liên quan)
# include_router(): Thêm tất cả endpoints từ router vào app

# Router 1: Authentication (đăng nhập, đăng ký)
app.include_router(
    api_auth.router,  # Router object từ api_auth.py
    prefix="/api/v1/auth",  # Tất cả endpoints sẽ bắt đầu với /api/v1/auth
    tags=["authentication"]  # Tag để nhóm trong API docs
)

# Router 2: Chatbot
app.include_router(
    api_chatbot.router,
    prefix="",  # Không có prefix, direct paths
    tags=["chat"]
)

# Router 3: Vehicles và Frames
app.include_router(
    api_vehicles_frames.router,
    prefix="",
    tags=["vehicles and frames"]
)

# Router 4: Reports và Analytics
app.include_router(
    api_reports.router,
    prefix="/api/v1",
    tags=["reports and analytics"]
)

# Router 5: RTSP Live Camera
app.include_router(
    api_rtsp.router,
    prefix="",
    tags=["rtsp live camera"]
)

# Router 6: Weather
app.include_router(
    api_weather.router,
    prefix="/api/v1",
    tags=["weather"]
)

# Router 7: Traffic Violations
app.include_router(
    api_violations.router,
    prefix="/api/v1",
    tags=["traffic violations"]
)

# Router 8: Debug Light Detection (NEW - for debugging traffic light detection)
app.include_router(
    api_debug_light.router,
    prefix="/api/v1",
    tags=["debug"]
)

# ============================================================================
# PHẦN 7: MOUNT STATIC FILES
# ============================================================================

# Dòng 98: Serve static files (ảnh vi phạm, v.v.)
# StaticFiles: Tự động serve tất cả files trong thư mục
app.mount(
    "/static",  # URL path: /static/...
    StaticFiles(directory="app/static"),  # Thư mục chứa files
    name="static"  # Tên để reference sau này
)
# Ví dụ: /static/violation_images/abc.jpg → app/static/violation_images/abc.jpg

# ============================================================================
# PHẦN 8: SỰ KIỆN TẮT SERVER (SHUTDOWN)
# ============================================================================

# Dòng 100-113: Hàm chạy KHI SERVER TẮT
@app.on_event("shutdown")
async def shutdown():
    """
    Hàm cleanup khi server shutdown
    Dọn dẹp scheduler, analyzer, đóng connections
    """
    print("Shutdown event triggered...")

    # --- BƯỚC 1: DỪNG SCHEDULER ---
    scheduler = get_scheduler()  # Lấy scheduler instance
    if scheduler:
        await scheduler.stop()  # Dừng scheduler
        print("✅ Traffic data scheduler stopped")

    # --- BƯỚC 2: CLEANUP ANALYZER ---
    if state.analyzer:
        state.analyzer.cleanup_processes()  # Dọn dẹp processes, threads
        print("✅ Analyzer cleaned up")

# ============================================================================
# PHẦN 9: GHI CHÚ VỀ LUỒNG HOẠT ĐỘNG
# ============================================================================
"""
LƯU Ý QUAN TRỌNG VỀ LUỒNG HOẠT ĐỘNG:

1. KHI CHẠY SERVER (uvicorn app.main:app):
   - Uvicorn import file này và tìm biến 'app'
   - FastAPI khởi tạo event loop
   - Gọi startup_event() một lần
   - Server bắt đầu lắng nghe requests

2. SERVER CHẠY LIÊN TỤC:
   - Main thread: FastAPI event loop (xử lý HTTP requests)
   - Background threads: Video analysis, YOLO detection
   - Background tasks: Scheduler (save data mỗi 10s), RTSP reader

3. CÁC THREAD PHÂN TÍCH VIDEO:
   - Tạo trong analyze_multi.process() với daemon=False
   - Chạy song song với main thread
   - KHÔNG cần join() vì FastAPI event loop giữ process sống

4. KHI NHẤN CTRL+C:
   - Signal handler được gọi
   - Cleanup: Stop scheduler, close cameras, kill processes
   - Server shutdown gracefully

5. TẠI SAO KHÔNG CẦN JOIN():
   - FastAPI server (uvicorn) giữ main thread chạy mãi
   - Nếu chạy như Python script thường → cần join()
   - Nhưng với web server → main thread KHÔNG BAO GIỜ kết thúc
   - Các thread con tiếp tục chạy song song với event loop

VÍ DỤ FLOW MỘT REQUEST:
1. Frontend gửi: GET /api/v1/violations/list
2. FastAPI routing → tìm endpoint trong api_violations.router
3. Gọi hàm handler tương ứng (get_violations_list)
4. Handler query database → trả về JSON
5. Response về frontend → Frontend render UI

KIẾN TRÚC:
┌─────────────────┐
│  Frontend       │
│  (React)        │
└────────┬────────┘
         │ HTTP/WebSocket
         ↓
┌─────────────────┐
│  FastAPI App    │ ← File này (main.py)
│  (Event Loop)   │
└────────┬────────┘
         │
    ┌────┴────┬────────┬──────────┐
    ↓         ↓        ↓          ↓
[Routers] [Database] [YOLO]  [Scheduler]
"""
