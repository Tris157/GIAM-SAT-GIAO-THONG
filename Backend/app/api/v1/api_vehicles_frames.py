from fastapi import APIRouter
from fastapi.responses import JSONResponse
from app.api.v1 import state
import asyncio
from fastapi.responses import Response
from fastapi import WebSocket, WebSocketDisconnect
from app.api.v1.api_rtsp import rtsp_detection_manager
from app.core.config import settings

router = APIRouter()

# COMMENT OUT: Startup event đã được di chuyển vào main.py
# @router.on_event("startup")
# def start_up():
#     if state.analyzer is None:
#         state.analyzer = AnalyzeOnRoadForMultiprocessing()
#         state.analyzer.run_multiprocessing()

@router.get(path= '/roads_name')
async def get_road_names():
    """
    API endpoint trả về danh sách tên các tuyến đường (road_name) mà analyzer đang xử lý.
    """
    # Kiểm tra nếu analyzer chưa được khởi tạo
    if state.analyzer is None:
        return JSONResponse(content={
            "road_names": [],
            "message": "Analyzer đang được khởi tạo, vui lòng đợi..."
        })

    # Kiểm tra nếu analyzer.names là None hoặc empty
    names = getattr(state.analyzer, 'names', None)
    if names is None:
        return JSONResponse(content={
            "road_names": [],
            "message": "Không có camera RTSP nào được cấu hình"
        })

    return JSONResponse(content={"road_names": names})

@router.websocket("/ws/frames/{road_name}")
async def websocket_frames(websocket: WebSocket, road_name: str):
    """
    WebSocket endpoint truyền liên tục frame (byte code) của tuyến đường road_name.
    """
    await websocket.accept()
    try:
        while True:
            frame_bytes = await asyncio.to_thread(state.analyzer.get_frame_road, road_name)
            await websocket.send_bytes(frame_bytes)
            await asyncio.sleep(1/30)
    except WebSocketDisconnect:
        pass
    except Exception as e:
        await websocket.close()
        
@router.websocket("/ws/info/{road_name}")
async def websocket_info(websocket: WebSocket, road_name: str):
    """
    WebSocket endpoint truyền liên tục info (thông tin phương tiện) của tuyến đường road_name.
    """
    await websocket.accept()
    try:
        while True:
            data = await asyncio.to_thread(state.analyzer.get_info_road, road_name)
            await websocket.send_json(data)
            await asyncio.sleep(5)
    except WebSocketDisconnect:
        pass
    except Exception as e:
        print(data)
        await websocket.close()

@router.get(path= '/info/{road_name}')
async def get_info_road(road_name: str):
    # Nếu road_name là "camera_live", lấy từ RTSP stream
    if road_name == "camera_live":
        try:
            if settings.ENABLE_RTSP:
                camera_stream = rtsp_detection_manager.get_stream("camera_live")
                if camera_stream:
                    detections = await camera_stream.get_detections()
                    return JSONResponse(content={
                        "road_name": "camera_live",
                        "count_car": detections.get("count_car", 0),
                        "count_motor": detections.get("count_motor", 0),
                        "speed_car": detections.get("speed_car", 0.0),
                        "speed_motor": detections.get("speed_motor", 0.0),
                        "total_vehicles": detections.get("total_vehicles", 0),
                        "violations": detections.get("violations", [])
                    })
        except Exception as e:
            print(f"⚠️ Error getting camera_live data: {e}")

    # Fallback: Lấy từ Analyzer (test videos)
    data = await asyncio.to_thread(state.analyzer.get_info_road, road_name)
    if data is None:
        return JSONResponse(content={
            "Lỗi: Dữ liệu bị lỗi, kiểm tra road_services"
            }, status_code=500)
    return JSONResponse(content= data)


@router.get(path='/frames/{road_name}')
async def get_frame_road(road_name: str):
    # Nếu road_name là "camera_live", lấy từ RTSP stream
    if road_name == "camera_live":
        try:
            if settings.ENABLE_RTSP:
                camera_stream = rtsp_detection_manager.get_stream("camera_live")
                if camera_stream:
                    frame = await camera_stream.get_current_frame()
                    if frame is not None:
                        frame_bytes = camera_stream.encode_frame(frame)
                        if frame_bytes:
                            return Response(content=frame_bytes, media_type="image/jpeg")
        except Exception as e:
            print(f"⚠️ Error getting camera_live frame: {e}")

    # Fallback: Lấy từ Analyzer (test videos)
    frame_bytes = await asyncio.to_thread(state.analyzer.get_frame_road, road_name)

    if frame_bytes is None:
        return JSONResponse(
            content={"error": "Lỗi: Dữ liệu bị lỗi, kiểm tra core"},
            status_code=500
        )
    return Response(content=frame_bytes, media_type="image/jpeg")
