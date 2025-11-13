# ============================================================================
# FILE: api_violations.py - API ENDPOINTS CHO QUẢN LÝ VI PHẠM GIAO THÔNG
# ============================================================================
# File này chứa tất cả các REST API endpoints để:
# - Cấu hình phát hiện vượt đèn đỏ
# - Lấy danh sách vi phạm
# - Xử lý vi phạm (đánh dấu đã xử lý, xóa)
# - Xem thống kê vi phạm
#
# Tất cả endpoints đều ASYNC và sử dụng AsyncSession cho database

# ============================================================================
# PHẦN 1: IMPORT CÁC THƯ VIỆN
# ============================================================================

# Dòng 5: Import các module từ FastAPI
from fastapi import APIRouter, HTTPException, Depends
# - APIRouter: Tạo nhóm routes (như Express.Router trong Node.js)
# - HTTPException: Throw lỗi HTTP (404, 500, v.v.)
# - Depends: Dependency injection (tự động inject database session)

# Dòng 6: Import các type hints
from typing import List, Optional
# - List[ViolationResponse]: API trả về danh sách violations
# - Optional[str]: Tham số có thể None (camera_name=None)

# Dòng 7: Import Pydantic BaseModel
from pydantic import BaseModel
# Pydantic: Validate input/output data tự động
# Tự động convert JSON → Python object và validate kiểu dữ liệu

# Dòng 8: Import datetime
from datetime import datetime
# Để làm việc với thời gian vi phạm (violated_at)

# Dòng 9-10: Import SQLAlchemy async
from sqlalchemy.ext.asyncio import AsyncSession  # Session bất đồng bộ
from sqlalchemy import select  # Query builder (select(), filter(), v.v.)

# Dòng 12: Import database session getter
from app.db.base import get_db
# get_db(): Generator trả về AsyncSession, tự động close sau khi xong

# Dòng 13: Import model TrafficViolation
from app.models.traffic_violation import TrafficViolation
# Model SQLAlchemy định nghĩa bảng traffic_violations trong database

# Dòng 14: Import RTSP detection manager
from app.api.v1.api_rtsp import rtsp_detection_manager
# Manager quản lý tất cả camera RTSP đang chạy
# Dùng để cấu hình red light detection cho từng camera

# Dòng 16: Tạo router
router = APIRouter()
# Tất cả các @router.get/post/put/delete sẽ được đăng ký vào router này
# Sau đó router này được include vào main app trong main.py


# ============================================================================
# PHẦN 2: PYDANTIC MODELS (REQUEST/RESPONSE SCHEMAS)
# ============================================================================

# Dòng 19-25: Model cho request cấu hình red light detection
class RedLightConfig(BaseModel):
    """
    Schema cho cấu hình phát hiện vượt đèn đỏ

    Frontend gửi JSON theo format này:
    {
      "camera_name": "camera_live",
      "traffic_light_roi": {"x": 10, "y": 10, "w": 80, "h": 150},
      "stop_line_y": 400,
      "enable": true
    }
    """
    camera_name: str  # Tên camera (ví dụ: "camera_live")

    # ROI = Region of Interest (vùng chứa đèn tín hiệu)
    traffic_light_roi: dict  # {"x": 10, "y": 10, "w": 80, "h": 150}
    # x, y: Tọa độ góc trên trái của vùng đèn
    # w, h: Chiều rộng và chiều cao của vùng đèn

    stop_line_y: int  # Tọa độ Y của vạch dừng (ví dụ: 400)
    # Nếu xe vượt qua Y=400 khi đèn đỏ → vi phạm

    enable: bool = True  # Bật/tắt detection (mặc định: bật)


# Dòng 28-42: Model cho response violation
class ViolationResponse(BaseModel):
    """
    Schema cho response trả về thông tin vi phạm

    API trả về JSON theo format này:
    {
      "id": 1,
      "camera_name": "camera_live",
      "violation_type": "red_light",
      "vehicle_type": "car",
      "image_path": "static/violations/abc.jpg",
      "position_x": 150.5,
      "position_y": 400.0,
      "traffic_light_status": "red",
      "violated_at": "2025-11-10T14:30:00",
      "is_processed": false
    }
    """
    id: int  # ID vi phạm trong database
    camera_name: str  # Camera phát hiện vi phạm
    violation_type: str  # Loại vi phạm: "red_light", "speeding", "wrong_lane"
    vehicle_type: str  # Loại xe: "car", "motorbike", "truck", "bus"
    image_path: str  # Đường dẫn ảnh vi phạm
    position_x: float  # Tọa độ X của xe (pixel)
    position_y: float  # Tọa độ Y của xe (pixel)
    traffic_light_status: str  # Trạng thái đèn: "red", "yellow", "green"
    violated_at: datetime  # Thời gian vi phạm
    is_processed: bool  # Đã xử lý chưa?

    # Dòng 41-42: Config cho Pydantic v2
    class Config:
        from_attributes = True  # Cho phép convert từ SQLAlchemy model → Pydantic model


# ============================================================================
# PHẦN 3: API ENDPOINTS - CẤU HÌNH RED LIGHT DETECTION
# ============================================================================

# Dòng 45-75: POST /violations/config - Cấu hình red light detection
@router.post("/violations/config")
async def configure_red_light_detection(config: RedLightConfig):
    """
    Cấu hình phát hiện vượt đèn đỏ cho một camera

    ===== CÁCH SỬ DỤNG =====

    Frontend gửi POST request với JSON body:
    {
      "camera_name": "camera_live",
      "traffic_light_roi": {"x": 10, "y": 10, "w": 80, "h": 150},
      "stop_line_y": 400,
      "enable": true
    }

    ===== GIẢI THÍCH THAM SỐ =====

    traffic_light_roi: Vùng chứa đèn tín hiệu
    - x: Khoảng cách từ mép trái màn hình (pixel)
    - y: Khoảng cách từ mép trên màn hình (pixel)
    - w: Chiều rộng vùng đèn (pixel)
    - h: Chiều cao vùng đèn (pixel)

    Ví dụ: Đèn tín hiệu ở góc trên trái
    → {"x": 10, "y": 10, "w": 80, "h": 150}

    stop_line_y: Vạch dừng (tọa độ Y)
    - Nếu xe có position_y > stop_line_y khi đèn đỏ → vi phạm

    ===== LƯU Ý =====
    Dựa vào ảnh camera, recommend config:
    - traffic_light_roi: {"x": 10, "y": 10, "w": 80, "h": 150} (góc trên trái)
    - stop_line_y: 400 (vạch dừng ở giữa màn hình)
    """

    # --- BƯỚC 1: LẤY STREAM TỪ MANAGER ---
    # Dòng 54: Tìm camera stream theo tên
    stream = rtsp_detection_manager.get_stream(config.camera_name)
    # rtsp_detection_manager: Dict lưu tất cả camera đang chạy
    # get_stream(): Trả về RTSPDetectionStream object hoặc None

    # Dòng 56-57: Kiểm tra camera có tồn tại không
    if not stream:
        # Throw 404 nếu không tìm thấy camera
        raise HTTPException(status_code=404, detail=f"Camera {config.camera_name} not found")

    # --- BƯỚC 2: CẤU HÌNH RED LIGHT DETECTION ---
    try:
        # Dòng 60-64: Gọi method configure_red_light_detection
        stream.configure_red_light_detection(
            roi=config.traffic_light_roi,  # Vùng đèn
            stop_line_y=config.stop_line_y,  # Vạch dừng
            enable=config.enable  # Bật/tắt
        )
        # Method này sẽ:
        # 1. Lưu config vào stream.red_light_config
        # 2. Khởi tạo RedLightDetector nếu enable=True
        # 3. Bắt đầu phát hiện vi phạm trong video stream

        # --- BƯỚC 3: TRẢ VỀ RESPONSE THÀNH CÔNG ---
        # Dòng 66-73: Return JSON confirm config
        return {
            "message": f"Red light detection configured for {config.camera_name}",
            "config": {
                "traffic_light_roi": config.traffic_light_roi,
                "stop_line_y": config.stop_line_y,
                "enabled": config.enable
            }
        }
    except Exception as e:
        # Dòng 74-75: Catch lỗi và throw 500
        raise HTTPException(status_code=500, detail=str(e))


# Dòng 78-92: POST /violations/enable/{camera_name} - Bật/tắt detection
@router.post("/violations/enable/{camera_name}")
async def enable_red_light_detection(camera_name: str, enable: bool = True):
    """
    Bật hoặc tắt red light detection cho camera

    ===== CÁCH SỬ DỤNG =====

    Bật detection:
    POST /violations/enable/camera_live?enable=true

    Tắt detection:
    POST /violations/enable/camera_live?enable=false

    ===== LƯU Ý =====
    Chỉ bật/tắt detection, KHÔNG thay đổi config (ROI, stop_line_y)
    """

    # Dòng 81: Lấy camera stream
    stream = rtsp_detection_manager.get_stream(camera_name)

    # Dòng 83-84: Kiểm tra camera tồn tại
    if not stream:
        raise HTTPException(status_code=404, detail=f"Camera {camera_name} not found")

    # Dòng 86: Bật/tắt monitoring
    stream.enable_red_light_monitoring(enable)
    # Method này set flag enable=True/False
    # Nếu enable=False → không phát hiện vi phạm nữa

    # Dòng 88-92: Return response
    return {
        "message": f"Red light detection {'enabled' if enable else 'disabled'} for {camera_name}",
        "camera_name": camera_name,
        "enabled": enable
    }


# Dòng 95-104: GET /violations/statistics/{camera_name} - Lấy thống kê
@router.get("/violations/statistics/{camera_name}")
async def get_violation_statistics(camera_name: str):
    """
    Lấy thống kê vi phạm theo camera

    ===== RESPONSE EXAMPLE =====
    {
      "total_violations": 50,
      "today_violations": 5,
      "red_light_violations": 30,
      "last_violation_time": "2025-11-10T14:30:00"
    }
    """

    # Dòng 98: Lấy camera stream
    stream = rtsp_detection_manager.get_stream(camera_name)

    # Dòng 100-101: Kiểm tra tồn tại
    if not stream:
        raise HTTPException(status_code=404, detail=f"Camera {camera_name} not found")

    # Dòng 103-104: Lấy và return statistics
    stats = stream.get_violation_statistics()
    # Method này return dict với các thống kê từ stream
    return stats


# ============================================================================
# PHẦN 4: API ENDPOINTS - QUẢN LÝ VI PHẠM (DATABASE)
# ============================================================================

# Dòng 107-136: GET /violations/list - Lấy danh sách vi phạm
@router.get("/violations/list", response_model=List[ViolationResponse])
async def get_violations(
    camera_name: Optional[str] = None,  # Filter theo camera (optional)
    is_processed: Optional[bool] = None,  # Filter theo trạng thái (optional)
    limit: int = 100,  # Giới hạn số kết quả (mặc định: 100)
    offset: int = 0,  # Offset cho pagination (mặc định: 0)
    db: AsyncSession = Depends(get_db)  # Inject database session
):
    """
    Lấy danh sách vi phạm với filtering và pagination

    ===== CÁCH SỬ DỤNG =====

    Lấy tất cả vi phạm (100 kết quả đầu):
    GET /violations/list

    Lấy vi phạm chưa xử lý:
    GET /violations/list?is_processed=false

    Lấy vi phạm của camera_live:
    GET /violations/list?camera_name=camera_live

    Pagination (lấy 50 kết quả tiếp theo):
    GET /violations/list?limit=50&offset=50

    ===== THAM SỐ =====
    - camera_name: Tên camera (None = tất cả camera)
    - is_processed: True/False/None (None = tất cả)
    - limit: Số kết quả tối đa
    - offset: Bỏ qua N kết quả đầu tiên
    - db: AsyncSession (tự động inject bởi FastAPI)

    ===== GIẢI THÍCH DEPENDS(get_db) =====
    - FastAPI tự động gọi get_db() để tạo AsyncSession
    - Session được inject vào tham số db
    - Sau khi endpoint chạy xong, session tự động close
    """

    # --- BƯỚC 1: TẠO BASE QUERY ---
    # Dòng 124: Tạo SELECT query
    query = select(TrafficViolation)
    # select(): Tạo query builder
    # Tương đương SQL: SELECT * FROM traffic_violations

    # --- BƯỚC 2: THÊM FILTERS NẾU CÓ ---
    # Dòng 126-127: Filter theo camera_name
    if camera_name:
        query = query.filter(TrafficViolation.camera_name == camera_name)
        # Thêm WHERE camera_name = ?

    # Dòng 129-130: Filter theo is_processed
    if is_processed is not None:  # Chú ý: phải check "is not None" vì False cũng là giá trị hợp lệ
        query = query.filter(TrafficViolation.is_processed == is_processed)
        # Thêm WHERE is_processed = ?

    # --- BƯỚC 3: THÊM ORDERING VÀ PAGINATION ---
    # Dòng 132: Sắp xếp theo thời gian mới nhất trước
    query = query.order_by(TrafficViolation.violated_at.desc())
    # .desc(): Giảm dần (newest first)

    # Dòng 132 (tiếp): Thêm offset và limit
    query = query.offset(offset).limit(limit)
    # offset(50): Bỏ qua 50 kết quả đầu
    # limit(100): Chỉ lấy tối đa 100 kết quả

    # --- BƯỚC 4: THỰC THI QUERY ---
    # Dòng 133: Execute query (ASYNC)
    result = await db.execute(query)
    # await: Đợi database trả về kết quả
    # result: Result object chứa rows

    # Dòng 134: Lấy tất cả violations từ result
    violations = result.scalars().all()
    # .scalars(): Chỉ lấy object (không lấy tuple)
    # .all(): Lấy tất cả rows thành list

    # --- BƯỚC 5: RETURN RESPONSE ---
    # Dòng 136: Return list violations
    return violations
    # FastAPI tự động convert List[TrafficViolation] → List[ViolationResponse]
    # Nhờ có response_model=List[ViolationResponse]


# Dòng 139-149: GET /violations/{violation_id} - Lấy 1 vi phạm theo ID
@router.get("/violations/{violation_id}", response_model=ViolationResponse)
async def get_violation(violation_id: int, db: AsyncSession = Depends(get_db)):
    """
    Lấy thông tin chi tiết của 1 vi phạm theo ID

    ===== CÁCH SỬ DỤNG =====
    GET /violations/123

    ===== RESPONSE =====
    - 200 OK: Trả về ViolationResponse
    - 404 Not Found: Không tìm thấy vi phạm
    """

    # Dòng 142: Tạo query với filter ID
    query = select(TrafficViolation).filter(TrafficViolation.id == violation_id)
    # WHERE id = ?

    # Dòng 143: Execute query
    result = await db.execute(query)

    # Dòng 144: Lấy 1 kết quả (hoặc None)
    violation = result.scalar_one_or_none()
    # .scalar_one_or_none(): Lấy 1 object duy nhất
    # - Nếu có: return object
    # - Nếu không có: return None
    # - Nếu có nhiều hơn 1: raise exception

    # Dòng 146-147: Kiểm tra tồn tại
    if not violation:
        raise HTTPException(status_code=404, detail="Violation not found")

    # Dòng 149: Return violation
    return violation


# Dòng 152-177: PUT /violations/{violation_id}/process - Đánh dấu đã xử lý
@router.put("/violations/{violation_id}/process")
async def mark_violation_processed(
    violation_id: int,  # ID vi phạm
    note: Optional[str] = None,  # Ghi chú (optional)
    db: AsyncSession = Depends(get_db)
):
    """
    Đánh dấu vi phạm đã được xử lý

    ===== CÁCH SỬ DỤNG =====

    Đánh dấu đã xử lý (không ghi chú):
    PUT /violations/123/process

    Đánh dấu đã xử lý (có ghi chú):
    PUT /violations/123/process?note=Đã xử phạt

    ===== RESPONSE =====
    {
      "message": "Violation marked as processed",
      "violation_id": 123,
      "is_processed": true
    }
    """

    # --- BƯỚC 1: TÌM VI PHẠM ---
    # Dòng 159: Query tìm violation
    query = select(TrafficViolation).filter(TrafficViolation.id == violation_id)

    # Dòng 160: Execute
    result = await db.execute(query)

    # Dòng 161: Lấy 1 kết quả
    violation = result.scalar_one_or_none()

    # Dòng 163-164: Kiểm tra tồn tại
    if not violation:
        raise HTTPException(status_code=404, detail="Violation not found")

    # --- BƯỚC 2: CẬP NHẬT TRẠNG THÁI ---
    # Dòng 166: Set is_processed = True
    violation.is_processed = True

    # Dòng 167-168: Cập nhật note nếu có
    if note:
        violation.note = note

    # --- BƯỚC 3: LƯU VÀO DATABASE ---
    # Dòng 170: Commit transaction
    await db.commit()
    # commit(): Lưu thay đổi vào database
    # Nếu không commit → thay đổi sẽ mất khi session close

    # Dòng 171: Refresh object
    await db.refresh(violation)
    # refresh(): Load lại object từ database
    # Để có dữ liệu mới nhất (sau khi commit)

    # --- BƯỚC 4: RETURN RESPONSE ---
    # Dòng 173-177: Return success message
    return {
        "message": "Violation marked as processed",
        "violation_id": violation_id,
        "is_processed": True
    }


# Dòng 180-196: DELETE /violations/{violation_id} - Xóa vi phạm
@router.delete("/violations/{violation_id}")
async def delete_violation(violation_id: int, db: AsyncSession = Depends(get_db)):
    """
    Xóa vi phạm khỏi database

    ===== CÁCH SỬ DỤNG =====
    DELETE /violations/123

    ===== CẢNH BÁO =====
    Hành động này KHÔNG THỂ HOÀN TÁC!
    Vi phạm sẽ bị xóa vĩnh viễn khỏi database.
    """

    # --- BƯỚC 1: TÌM VI PHẠM ---
    # Dòng 183: Query tìm violation
    query = select(TrafficViolation).filter(TrafficViolation.id == violation_id)

    # Dòng 184: Execute
    result = await db.execute(query)

    # Dòng 185: Lấy kết quả
    violation = result.scalar_one_or_none()

    # Dòng 187-188: Kiểm tra tồn tại
    if not violation:
        raise HTTPException(status_code=404, detail="Violation not found")

    # --- BƯỚC 2: XÓA KHỎI DATABASE ---
    # Dòng 190: Đánh dấu xóa
    await db.delete(violation)
    # delete(): Đánh dấu object để xóa
    # Chưa xóa thật trong database

    # Dòng 191: Commit để xóa thật
    await db.commit()
    # Sau commit, violation đã bị xóa vĩnh viễn

    # --- BƯỚC 3: RETURN RESPONSE ---
    # Dòng 193-196: Return success
    return {
        "message": "Violation deleted successfully",
        "violation_id": violation_id
    }


# Dòng 199-227: GET /violations/summary/daily - Tổng hợp theo ngày
@router.get("/violations/summary/daily")
async def get_daily_summary(
    camera_name: Optional[str] = None,  # Filter theo camera (optional)
    db: AsyncSession = Depends(get_db)
):
    """
    Lấy tổng hợp vi phạm theo ngày (30 ngày gần nhất)

    ===== CÁCH SỬ DỤNG =====

    Tổng hợp tất cả camera:
    GET /violations/summary/daily

    Tổng hợp camera cụ thể:
    GET /violations/summary/daily?camera_name=camera_live

    ===== RESPONSE EXAMPLE =====
    [
      {
        "date": "2025-11-10",
        "total_violations": 15,
        "unique_vehicle_types": 3
      },
      {
        "date": "2025-11-09",
        "total_violations": 20,
        "unique_vehicle_types": 4
      },
      ...
    ]
    """

    # Dòng 205: Import func cho aggregate functions
    from sqlalchemy import func
    # func: Chứa các hàm SQL như COUNT(), SUM(), AVG(), v.v.

    # --- BƯỚC 1: TẠO AGGREGATE QUERY ---
    # Dòng 207-211: SELECT với GROUP BY
    query = select(
        TrafficViolation.date,  # Cột date để group
        func.count(TrafficViolation.id).label('total_violations'),  # COUNT(id) AS total_violations
        func.count(func.distinct(TrafficViolation.vehicle_type)).label('unique_vehicle_types')  # COUNT(DISTINCT vehicle_type)
    ).group_by(TrafficViolation.date)  # GROUP BY date

    # Tương đương SQL:
    # SELECT
    #   date,
    #   COUNT(id) AS total_violations,
    #   COUNT(DISTINCT vehicle_type) AS unique_vehicle_types
    # FROM traffic_violations
    # GROUP BY date

    # --- BƯỚC 2: THÊM FILTER NẾU CÓ ---
    # Dòng 213-214: Filter theo camera
    if camera_name:
        query = query.filter(TrafficViolation.camera_name == camera_name)
        # WHERE camera_name = ?

    # --- BƯỚC 3: ORDERING VÀ LIMIT ---
    # Dòng 216: Sắp xếp và giới hạn 30 ngày
    query = query.order_by(TrafficViolation.date.desc()).limit(30)
    # ORDER BY date DESC LIMIT 30
    # Lấy 30 ngày gần nhất

    # --- BƯỚC 4: EXECUTE QUERY ---
    # Dòng 217: Execute
    result = await db.execute(query)

    # Dòng 218: Lấy tất cả rows
    results = result.all()
    # .all(): Lấy tất cả rows (không dùng scalars vì có nhiều cột)

    # --- BƯỚC 5: FORMAT VÀ RETURN ---
    # Dòng 220-227: Convert từ Row → Dict
    return [
        {
            "date": r.date,  # Truy cập column bằng attribute
            "total_violations": r.total_violations,
            "unique_vehicle_types": r.unique_vehicle_types
        }
        for r in results  # List comprehension
    ]
    # FastAPI tự động convert list[dict] → JSON array


# ============================================================================
# PHẦN 5: QUICK SETUP ENDPOINT
# ============================================================================

# Dòng 230-249: POST /violations/quick-setup/camera_live - Setup nhanh
@router.post("/violations/quick-setup/camera_live")
async def quick_setup_camera_live():
    """
    Quick setup cho camera_live dựa trên ảnh camera của bạn

    ===== MỤC ĐÍCH =====
    Endpoint này giúp setup nhanh red light detection cho camera_live
    mà không cần phải tự tính toán ROI và stop_line_y

    ===== CONFIG ĐÃ TỐI ƯU =====
    Dựa vào phân tích ảnh camera:
    - Cột đèn tín hiệu: Ở góc trên trái
    - Vạch zebra crossing: Ở giữa màn hình
    - Vạch dừng: Trước vạch zebra

    ===== CÁCH SỬ DỤNG =====
    POST /violations/quick-setup/camera_live

    Không cần body, tự động setup với config đã tối ưu
    """

    # --- TẠO CONFIG ĐÃ TỐI ƯU ---
    # Dòng 237-247: Config object
    config = RedLightConfig(
        camera_name="camera_live",  # Tên camera

        # ROI cho đèn tín hiệu (góc trên trái)
        traffic_light_roi={
            "x": 5,      # 5 pixels từ mép trái
            "y": 5,      # 5 pixels từ mép trên
            "w": 100,    # Chiều rộng 100px
            "h": 180     # Chiều cao 180px (3 đèn xếp dọc)
        },

        # Vạch dừng (trước vạch zebra)
        stop_line_y=420,  # Y=420 pixels
        # Xe có position_y > 420 khi đèn đỏ → vi phạm

        enable=True  # Bật detection luôn
    )

    # --- GỌI CONFIGURE ENDPOINT ---
    # Dòng 249: Reuse configure endpoint
    return await configure_red_light_detection(config)
    # Gọi lại hàm configure ở trên với config đã tối ưu


# ============================================================================
# TỔNG KẾT: LUỒNG HOẠT ĐỘNG CỦA CÁC API
# ============================================================================
"""
===== 1. CẤU HÌNH RED LIGHT DETECTION =====

Flow: Frontend → POST /violations/config → RTSPDetectionStream → RedLightDetector

1. Frontend gửi POST /violations/config với ROI và stop_line_y
2. API tìm camera stream trong rtsp_detection_manager
3. Gọi stream.configure_red_light_detection()
4. Stream khởi tạo RedLightDetector
5. Detector bắt đầu phân tích frames:
   - Crop ROI từ frame
   - Detect màu đèn (HSV color space)
   - Kiểm tra xe vượt vạch dừng
   - Nếu vi phạm → lưu vào database

===== 2. QUẢN LÝ VI PHẠM =====

Flow: Frontend → GET/PUT/DELETE /violations/* → Database (SQLite)

GET /violations/list:
1. Frontend request với filters
2. API build SQLAlchemy query
3. Execute query với AsyncSession
4. Return list[ViolationResponse]

PUT /violations/{id}/process:
1. Frontend gửi PUT request
2. API tìm violation trong database
3. Set is_processed = True
4. Commit vào database

DELETE /violations/{id}:
1. Frontend gửi DELETE request
2. API tìm và xóa violation
3. Commit để xóa vĩnh viễn

===== 3. THỐNG KÊ =====

Flow: Frontend → GET /violations/summary/daily → Database (SQLite)

1. Frontend request daily summary
2. API build aggregate query (GROUP BY date)
3. Execute với COUNT(), DISTINCT()
4. Return 30 ngày gần nhất

===== 4. DATABASE PATTERN =====

Tất cả endpoints đều dùng pattern:
1. Inject AsyncSession qua Depends(get_db)
2. Build query với select()
3. Execute với await db.execute()
4. Process results
5. Return response
6. Session tự động close (managed by FastAPI)

===== 5. ERROR HANDLING =====

Tất cả endpoints đều có error handling:
- 404: Không tìm thấy (camera, violation)
- 500: Lỗi server (exception)
- 200: Thành công

===== 6. KIẾN TRÚC =====

┌──────────────┐
│   Frontend   │
│   (React)    │
└──────┬───────┘
       │ HTTP Request
       ↓
┌──────────────────────────────┐
│   api_violations.py          │
│   (FastAPI Router)           │
├──────────────────────────────┤
│ • /violations/config         │ → RTSPDetectionStream
│ • /violations/list           │ → Database
│ • /violations/{id}/process   │ → Database
│ • /violations/{id}           │ → Database
│ • /violations/summary/daily  │ → Database
└──────┬───────────────────────┘
       │
   ┌───┴────┬─────────────┐
   ↓        ↓             ↓
┌──────┐ ┌──────┐  ┌─────────────┐
│ RTSP │ │ DB   │  │ RedLight    │
│ Mgr  │ │(SQL) │  │ Detector    │
└──────┘ └──────┘  └─────────────┘

===== 7. ASYNC PATTERN =====

Tất cả functions đều async:
- async def endpoint(): ...
- await db.execute()
- await db.commit()
- await db.refresh()

Lý do: Không block event loop khi query database

===== 8. PYDANTIC VALIDATION =====

Tất cả input/output đều validate:
- RedLightConfig: Validate config request
- ViolationResponse: Validate API response
- Tự động convert JSON ↔ Python object
- Type checking tự động

===== VÍ DỤ FLOW ĐẦY ĐỦ - PHÁT HIỆN VI PHẠM =====

1. User config detection qua Frontend
2. Frontend → POST /violations/config
3. API → stream.configure_red_light_detection()
4. Stream → RedLightDetector.detect_light_color()
5. Detector phát hiện đèn đỏ
6. Xe vượt stop_line_y
7. Detector lưu violation vào database
8. Frontend → GET /violations/list
9. API query database
10. Return violations
11. Frontend hiển thị trong table

===== LƯU Ý QUAN TRỌNG =====

1. Tất cả operations đều ASYNC (không block)
2. Database session tự động cleanup
3. Errors được handle với HTTPException
4. Response tự động validate bởi Pydantic
5. CORS đã enable trong main.py (Frontend có thể gọi API)
"""
