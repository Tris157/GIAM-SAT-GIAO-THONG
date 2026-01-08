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
from app.api.v1 import api_red_light_config  # Router quản lý config ROI và Stop Line (NEW)
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
# PHẦN 3: KHỞI TẠO FASTAPI APPLICATION VỚI CẤU HÌNH NÂNG CAO
# ============================================================================

# Import thêm các modules cho middleware
from fastapi import Request, Response
from fastapi.responses import JSONResponse
import time
import uuid
from datetime import datetime

# Tạo instance FastAPI với cấu hình chi tiết
app = FastAPI(
    title="🚦 Smart Traffic Monitoring System API",
    description="""
    ## Hệ thống giám sát giao thông thông minh - Vietnam Transport

    ### 🎯 Tính năng chính:
    * 📹 **Phát hiện vi phạm giao thông** real-time với AI
    * 🚗 **Theo dõi phương tiện** và thống kê
    * 📊 **Báo cáo và phân tích** chi tiết
    * 🤖 **Chatbot hỗ trợ** thông minh
    * 📱 **Telegram Bot** thông báo vi phạm
    * 🌦️ **Tích hợp thông tin thời tiết**

    ### 🔐 Xác thực:
    Sử dụng JWT Bearer Token cho các API yêu cầu authentication.

    ### 📝 API Response Format:
    ```json
    {
        "success": true,
        "data": {...},
        "message": "Success",
        "request_id": "uuid-here",
        "timestamp": "2025-12-08T10:30:00"
    }
    ```
    """,
    version="3.0.0",  # Nâng version lên 3.0.0
    docs_url="/api/docs",  # Custom docs URL
    redoc_url="/api/redoc",  # Custom ReDoc URL
    openapi_url="/api/openapi.json",  # Custom OpenAPI JSON URL
    contact={
        "name": "Smart Traffic Team",
        "email": "support@smarttraffic.vn",
    },
    license_info={
        "name": "MIT License",
        "url": "https://opensource.org/licenses/MIT",
    },
)

# ============================================================================
# MIDDLEWARE 1: REQUEST ID TRACKING (Theo dõi mọi request)
# ============================================================================

@app.middleware("http")
async def add_request_id_middleware(request: Request, call_next):
    """
    Middleware thêm Request ID vào mọi request để tracking
    Request ID sẽ xuất hiện trong response headers và logs
    """
    # Tạo unique request ID
    request_id = str(uuid.uuid4())
    request.state.request_id = request_id

    # Thêm vào response headers
    response = await call_next(request)
    response.headers["X-Request-ID"] = request_id

    return response

# ============================================================================
# MIDDLEWARE 2: RESPONSE TIME TRACKING & LOGGING
# ============================================================================

@app.middleware("http")
async def add_process_time_middleware(request: Request, call_next):
    """
    Middleware đo thời gian xử lý request và log thông tin
    Hiển thị màu sắc theo response time (xanh/vàng/đỏ)
    """
    start_time = time.time()

    # Xử lý request
    response = await call_next(request)

    # Tính thời gian xử lý
    process_time = time.time() - start_time
    process_time_ms = round(process_time * 1000, 2)

    # Thêm vào response headers
    response.headers["X-Process-Time"] = f"{process_time_ms}ms"

    # Log với màu sắc theo response time
    request_id = getattr(request.state, 'request_id', 'N/A')
    method = request.method
    url = str(request.url.path)
    status_code = response.status_code

    # Chọn màu dựa trên response time và status code
    if process_time_ms < 100:
        time_color = "\033[92m"  # Xanh - nhanh
    elif process_time_ms < 500:
        time_color = "\033[93m"  # Vàng - trung bình
    else:
        time_color = "\033[91m"  # Đỏ - chậm

    if 200 <= status_code < 300:
        status_color = "\033[92m"  # Xanh - success
    elif 400 <= status_code < 500:
        status_color = "\033[93m"  # Vàng - client error
    else:
        status_color = "\033[91m"  # Đỏ - server error

    reset_color = "\033[0m"

    # Log request với màu sắc
    print(f"📊 [{datetime.now().strftime('%H:%M:%S')}] "
          f"{method:6} {url:50} "
          f"{status_color}{status_code}{reset_color} "
          f"{time_color}{process_time_ms}ms{reset_color} "
          f"[{request_id[:8]}]")

    return response

# ============================================================================
# MIDDLEWARE 3: ERROR HANDLER (Xử lý lỗi toàn cục)
# ============================================================================

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """
    Middleware xử lý tất cả exceptions chưa được catch
    Trả về JSON response chuẩn và log chi tiết
    """
    import traceback

    request_id = getattr(request.state, 'request_id', 'N/A')

    # Log chi tiết lỗi
    print(f"\n❌ [ERROR] Request ID: {request_id}")
    print(f"   URL: {request.method} {request.url}")
    print(f"   Error: {str(exc)}")
    print(f"   Traceback:\n{traceback.format_exc()}")

    # Trả về JSON response
    return JSONResponse(
        status_code=500,
        content={
            "success": False,
            "error": "Internal Server Error",
            "message": str(exc),
            "request_id": request_id,
            "timestamp": datetime.now().isoformat(),
        }
    )

# ============================================================================
# MIDDLEWARE 4: CORS với Security Headers
# ============================================================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Production: thay bằng domain cụ thể
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["X-Request-ID", "X-Process-Time"],  # Cho phép frontend đọc headers
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

    # Lưu thời gian bắt đầu
    app.state.start_time = time.time()
    app.state.total_requests = 0

    # ANSI colors
    CYAN = "\033[96m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    RED = "\033[91m"
    BLUE = "\033[94m"
    MAGENTA = "\033[95m"
    RESET = "\033[0m"
    BOLD = "\033[1m"

    # Banner đẹp
    print(f"\n{CYAN}{BOLD}")
    print("╔══════════════════════════════════════════════════════════════╗")
    print("║                                                              ║")
    print("║    🚦  SMART TRAFFIC MONITORING SYSTEM  🚦                   ║")
    print("║                                                              ║")
    print("║    Vietnam Transport Edition - v3.0.0                       ║")
    print("║                                                              ║")
    print("╚══════════════════════════════════════════════════════════════╝")
    print(f"{RESET}\n")

    print(f"{BOLD}{BLUE}🚀 Khởi động hệ thống...{RESET}\n")

    # --- BƯỚC 1: TẠO BẢNG DATABASE ---
    try:
        print(f"{YELLOW}⏳ [1/5] Database: Đang tạo tables...{RESET}")
        # Dùng sync engine để tạo tables (tránh async deadlock)
        # Đổi sqlite+aiosqlite thành sqlite
        from app.core.config import settings
        sync_db_url = settings.DATABASE_URL.replace("sqlite+aiosqlite", "sqlite")
        sync_engine = create_engine(sync_db_url, echo=False)
        Base.metadata.create_all(sync_engine)
        sync_engine.dispose()  # Đóng connection ngay lập tức
        print(f"{GREEN}✅ [1/5] Database: Khởi tạo thành công{RESET}")
    except Exception as e:
        print(f"{RED}❌ [1/5] Database: Thất bại - {e}{RESET}")
        traceback.print_exc()
        raise

    # --- BƯỚC 2: KHỞI TẠO ANALYZER (BACKGROUND THREAD - KHÔNG BLOCK) ---
    try:
        print(f"{YELLOW}⏳ [2/5] AI Analyzer: Đang khởi tạo YOLO models...{RESET}")

        # Sử dụng Thread thay vì asyncio để KHÔNG BLOCK startup event
        import threading

        def init_analyzer_thread():
            try:
                import time
                time.sleep(2)  # Đợi server sẵn sàng
                print(f"{BLUE}🔄 AI Analyzer: Loading models...{RESET}")
                state.init_analyzer()
                print(f"{GREEN}✅ [2/5] AI Analyzer: Khởi tạo thành công{RESET}")
            except Exception as e:
                print(f"{RED}❌ AI Analyzer: Thất bại - {e}{RESET}")
                traceback.print_exc()

        # Tạo daemon thread - chạy độc lập, KHÔNG block main thread
        analyzer_thread = threading.Thread(target=init_analyzer_thread, daemon=True)
        analyzer_thread.start()
        print(f"{GREEN}✅ [2/5] AI Analyzer: Background thread started{RESET}")
    except Exception as e:
        print(f"{RED}❌ [2/5] AI Analyzer: Thất bại - {e}{RESET}")
        traceback.print_exc()

    # --- BƯỚC 3: SCHEDULER (AUTO-SAVE DATA) ---
    try:
        print(f"{YELLOW}⏳ [3/5] Scheduler: Đang cấu hình...{RESET}")

        async def start_scheduler_when_ready():
            try:
                # Đợi analyzer khởi tạo xong
                while state.analyzer is None:
                    await asyncio.sleep(1)

                print(f"{BLUE}🔄 Scheduler: Đang khởi động...{RESET}")
                # Khởi động scheduler
                scheduler = init_scheduler(state.analyzer, interval_seconds=10)
                await scheduler.start()
                print(f"{GREEN}✅ [3/5] Scheduler: Khởi động thành công (interval: 10s){RESET}")
            except Exception as e:
                print(f"{RED}❌ Scheduler: Thất bại - {e}{RESET}")
                traceback.print_exc()

        asyncio.create_task(start_scheduler_when_ready())
        print(f"{GREEN}✅ [3/5] Scheduler: Background task created{RESET}")
    except Exception as e:
        print(f"{RED}❌ [3/5] Scheduler: Thất bại - {e}{RESET}")
        traceback.print_exc()

    # --- BƯỚC 4: KẾT NỐI RTSP CAMERA (NON-BLOCKING ASYNC) ---
    print(f"{YELLOW}⏳ [4/5] RTSP Camera: Khởi tạo background task...{RESET}")

    async def init_rtsp_background():
        """
        Hàm khởi tạo RTSP chạy ngầm, không block server startup
        Sử dụng run_in_executor cho các tác vụ nặng (load model, connect camera)
        """
        import asyncio
        # Đợi 2s để server in hết log startup
        await asyncio.sleep(2)

        from app.core.config import settings
        
        if not (settings.ENABLE_RTSP and settings.RTSP_URL):
             print(f"{MAGENTA}ℹ️  [4/5] RTSP Camera: Đã tắt (Bật trong .env){RESET}")
             return

        try:
            print(f"{BLUE}🔄 RTSP: Đang khởi tạo connection...{RESET}")
            from app.api.v1.api_rtsp import rtsp_detection_manager, read_rtsp_detection_frames
            from app.services.rtsp_detection_service import RTSPDetectionService
            
            # 1. Tạo service object (trong main loop để tạo Lock đúng chỗ)
            stream = RTSPDetectionService(
                rtsp_url=settings.RTSP_URL, 
                camera_name="camera_live",
                model_path="./app/ai_models/model N/original model/best.pt"
            )

            # 2. Run blocking tasks in Executor (Thread Pool)
            loop = asyncio.get_running_loop()
            
            # Load Model (Heavy!)
            print(f"{BLUE}   ...Loading YOLO model (this implies CPU/GPU usage)...{RESET}")
            model_loaded = await loop.run_in_executor(None, stream.load_model)
            if not model_loaded:
                print(f"{RED}❌ RTSP: Không thể load model{RESET}")
                return

            # Connect Camera (Blocking IO!)
            print(f"{BLUE}   ...Connecting to RTSP stream...{RESET}")
            connected = await loop.run_in_executor(None, stream.connect)

            if connected:
                # 3. Register to manager
                rtsp_detection_manager.streams["camera_live"] = stream
                print(f"{GREEN}✅ [4/5] RTSP Camera: Kết nối thành công{RESET}")

                # 4. Configure Red Light
                try:
                    # Load config from file if exists
                    import json
                    import os
                    config_file = "./app/config/red_light_config_camera_live.json"

                    if os.path.exists(config_file):
                        with open(config_file, 'r', encoding='utf-8') as f:
                            config = json.load(f)
                            stream.configure_red_light_detection(
                                roi=config.get("traffic_light_roi", {"x": 1570, "y": 154, "w": 43, "h": 73}),
                                stop_line_y=config.get("stop_line_y", 544),
                                enable=True
                            )
                            print(f"{GREEN}🚦 Red Light Detection: Đã enable (config file){RESET}")
                    else:
                        stream.configure_red_light_detection(
                                roi={"x": 1570, "y": 154, "w": 43, "h": 73},
                                stop_line_y=544,
                                enable=True
                        )
                        print(f"{GREEN}🚦 Red Light Detection: Đã enable (default){RESET}")
                except Exception as e:
                    print(f"{YELLOW}⚠️  Red Light Config: {e}{RESET}")

                # 5. Start Reading Loop (Async task in main loop)
                asyncio.create_task(read_rtsp_detection_frames("camera_live"))

                # 6. Connect Internal Camera (Optional)
                if settings.RTSP_URL_INTERNAL:
                    print(f"{YELLOW}⏳ Connecting Internal Camera...{RESET}")
                    stream_internal = RTSPDetectionService(settings.RTSP_URL_INTERNAL, "camera_internal")
                    if await loop.run_in_executor(None, stream_internal.load_model):
                        if await loop.run_in_executor(None, stream_internal.connect):
                            rtsp_detection_manager.streams["camera_internal"] = stream_internal
                            print(f"{GREEN}✅ Internal Camera Connected{RESET}")
                            asyncio.create_task(read_rtsp_detection_frames("camera_internal"))
                        else:
                            print(f"{RED}❌ Internal Camera Connect Failed{RESET}")
            else:
                print(f"{RED}❌ [4/5] RTSP Camera: Connect Failed (Timeout/Unreachable){RESET}")

        except Exception as e:
            print(f"{RED}❌ [4/5] RTSP Init Error: {e}{RESET}")
            import traceback
            traceback.print_exc()

    # Schedule the async initialization
    asyncio.create_task(init_rtsp_background())

    # --- BƯỚC 5: KHỞI ĐỘNG TELEGRAM BOT (BACKGROUND THREAD) ---
    try:
        print(f"{YELLOW}⏳ [5/5] Telegram Bot: Đang khởi động...{RESET}")

        # Sử dụng Thread để không block startup event
        def init_telegram_bot_thread():
            try:
                import time
                time.sleep(5)  # Đợi server sẵn sàng
                print(f"{BLUE}🔄 Telegram Bot: Connecting...{RESET}")

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

                print(f"{GREEN}✅ [5/5] Telegram Bot: Khởi động thành công{RESET}")
            except Exception as e:
                print(f"{RED}❌ Telegram Bot: Thất bại - {e}{RESET}")
                traceback.print_exc()

        # Tạo daemon thread
        telegram_thread = threading.Thread(target=init_telegram_bot_thread, daemon=True)
        telegram_thread.start()
        print(f"{GREEN}✅ [5/5] Telegram Bot: Background thread started{RESET}")
    except Exception as e:
        print(f"{YELLOW}⚠️  [5/5] Telegram Bot: Không khởi động - {e}{RESET}")
        print(f"{YELLOW}   (Bot sẽ không hoạt động, nhưng hệ thống vẫn chạy){RESET}")
        traceback.print_exc()

    # Banner kết thúc
    print(f"\n{GREEN}{BOLD}")
    print("╔══════════════════════════════════════════════════════════════╗")
    print("║                                                              ║")
    print("║    ✨  HỆ THỐNG ĐÃ KHỞI ĐỘNG THÀNH CÔNG!  ✨                ║")
    print("║                                                              ║")
    print("║    🌐 API Docs:    http://localhost:8000/api/docs           ║")
    print("║    📊 Health:      http://localhost:8000/api/health         ║")
    print("║    📈 Metrics:     http://localhost:8000/api/system/status  ║")
    print("║                                                              ║")
    print("╚══════════════════════════════════════════════════════════════╝")
    print(f"{RESET}\n")

    print(f"{CYAN}💡 Tip: Nhấn Ctrl+C để tắt server gracefully{RESET}\n")

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

# ============================================================================
# PHẦN 6A: HEALTH CHECK & SYSTEM ENDPOINTS
# ============================================================================

@app.get(
    path='/api/health',
    tags=["system"],
    summary="Health Check",
    description="Kiểm tra trạng thái sống của API server"
)
async def health_check():
    """
    Health check endpoint - kiểm tra API có đang hoạt động không
    Trả về thông tin cơ bản về hệ thống
    """
    return {
        "success": True,
        "status": "healthy",
        "service": "Smart Traffic Monitoring System",
        "version": "3.0.0",
        "timestamp": datetime.now().isoformat(),
        "uptime_seconds": round(time.time() - app.state.start_time, 2) if hasattr(app.state, 'start_time') else 0,
    }

@app.get(
    path='/api/system/status',
    tags=["system"],
    summary="System Status",
    description="Trạng thái chi tiết của hệ thống"
)
async def system_status():
    """
    System status endpoint - trạng thái chi tiết của các components
    """
    import psutil
    from app.api.v1 import state

    # CPU và Memory
    cpu_percent = psutil.cpu_percent(interval=0.5)
    memory = psutil.virtual_memory()

    # Disk usage
    disk = psutil.disk_usage('/')

    return {
        "success": True,
        "data": {
            "api": {
                "status": "running",
                "version": "3.0.0",
                "uptime_seconds": round(time.time() - app.state.start_time, 2) if hasattr(app.state, 'start_time') else 0,
            },
            "analyzer": {
                "status": "running" if state.analyzer else "not_initialized",
                "initialized": state.analyzer is not None,
            },
            "system": {
                "cpu_percent": cpu_percent,
                "memory": {
                    "total_gb": round(memory.total / (1024**3), 2),
                    "used_gb": round(memory.used / (1024**3), 2),
                    "percent": memory.percent,
                },
                "disk": {
                    "total_gb": round(disk.total / (1024**3), 2),
                    "used_gb": round(disk.used / (1024**3), 2),
                    "percent": disk.percent,
                }
            }
        },
        "timestamp": datetime.now().isoformat(),
    }

@app.get(
    path='/api/system/metrics',
    tags=["system"],
    summary="System Metrics",
    description="Metrics và thống kê performance"
)
async def system_metrics():
    """
    System metrics endpoint - metrics về performance và usage
    """
    import psutil
    from app.api.v1 import state

    # Process hiện tại
    process = psutil.Process()

    return {
        "success": True,
        "data": {
            "process": {
                "cpu_percent": process.cpu_percent(interval=0.5),
                "memory_mb": round(process.memory_info().rss / (1024**2), 2),
                "num_threads": process.num_threads(),
                "num_handles": process.num_handles() if sys.platform == 'win32' else 0,
            },
            "api": {
                "total_requests": getattr(app.state, 'total_requests', 0),
                "uptime_seconds": round(time.time() - app.state.start_time, 2) if hasattr(app.state, 'start_time') else 0,
            },
        },
        "timestamp": datetime.now().isoformat(),
    }

# Dòng 85-87: Route root "/" redirect về frontend
@app.get(path='/', include_in_schema=False)  # Ẩn khỏi docs
def direct_home():
    """Redirect về frontend React app"""
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

# Router 9: Red Light Detection Config (NEW - quản lý ROI và Stop Line)
app.include_router(
    api_red_light_config.router,
    prefix="/api/v1/red-light-config",
    tags=["red light config"]
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

