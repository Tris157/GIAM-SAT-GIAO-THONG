from fastapi import APIRouter, WebSocket, WebSocketDisconnect, HTTPException
from fastapi.responses import StreamingResponse
import asyncio
from typing import Optional
import io

from app.services.rtsp_service import RTSPStreamManager, RTSPStreamService
from app.services.rtsp_detection_service import RTSPDetectionManager, RTSPDetectionService

router = APIRouter()

# Global RTSP stream managers
rtsp_manager = RTSPStreamManager()  # For raw stream (no detection)
rtsp_detection_manager = RTSPDetectionManager()  # For stream with YOLO detection


@router.on_event("startup")
async def startup_event():
    """Initialize RTSP streams on startup"""
    # Get RTSP URL from config
    from app.core.config import settings

    if not settings.ENABLE_RTSP or not settings.RTSP_URL:
        print("⚠️ RTSP not enabled or URL not configured")
        return

    rtsp_url = settings.RTSP_URL

    # Add stream WITH detection (camera_live)
    success = rtsp_detection_manager.add_stream("camera_live", rtsp_url)
    if success:
        print("✅ RTSP camera with detection connected successfully")
        # Start background task to continuously read and process frames
        asyncio.create_task(read_rtsp_detection_frames("camera_live"))
    else:
        print("❌ Failed to connect to RTSP camera with detection")

    # Optionally add raw stream (no detection) - camera_raw
    # success_raw = rtsp_manager.add_stream("camera_raw", rtsp_url)
    # if success_raw:
    #     print("✅ RTSP raw camera connected successfully")
    #     asyncio.create_task(read_rtsp_frames("camera_raw")))


@router.on_event("shutdown")
async def shutdown_event():
    """Cleanup RTSP streams on shutdown"""
    rtsp_manager.disconnect_all()
    rtsp_detection_manager.disconnect_all()
    print("🔌 RTSP streams disconnected")


async def read_rtsp_frames(stream_name: str):
    """Background task to continuously read frames from RTSP stream (no detection)"""
    stream = rtsp_manager.get_stream(stream_name)
    if not stream:
        return

    while stream.is_running:
        try:
            await stream.read_frame()
            await asyncio.sleep(0.033)  # ~30 FPS
        except Exception as e:
            print(f"Error in read_rtsp_frames: {e}")
            await asyncio.sleep(1)


async def read_rtsp_detection_frames(stream_name: str):
    """Background task to continuously read and process frames with YOLO detection"""
    stream = rtsp_detection_manager.get_stream(stream_name)
    if not stream:
        print(f"❌ Stream {stream_name} not found")
        return

    print(f"🎬 Starting detection loop for {stream_name}")
    frame_count = 0

    while stream.is_running:
        try:
            frame = await stream.process_frame()
            if frame is not None:
                frame_count += 1
                if frame_count % 30 == 0:  # Log every 30 frames
                    detections = await stream.get_detections()
                    print(f"📊 {stream_name}: Cars={detections['count_car']}, Motors={detections['count_motor']}, Total={detections['total_vehicles']}")

            # Small sleep to avoid CPU spike and allow other tasks to run
            await asyncio.sleep(0.01)
        except Exception as e:
            print(f"❌ Error in read_rtsp_detection_frames: {e}")
            await asyncio.sleep(1)


@router.get("/rtsp/streams")
async def get_rtsp_streams():
    """Get list of available RTSP streams"""
    detection_streams = rtsp_detection_manager.get_all_streams()
    raw_streams = rtsp_manager.get_all_streams()
    return {
        "detection_streams": detection_streams,
        "raw_streams": raw_streams,
        "total_count": len(detection_streams) + len(raw_streams)
    }


@router.get("/rtsp/frame/{stream_name}")
async def get_rtsp_frame(stream_name: str):
    """Get latest frame from RTSP stream as JPEG (with detection)"""
    # Try detection stream first
    stream = rtsp_detection_manager.get_stream(stream_name)
    if not stream:
        # Fallback to raw stream
        stream = rtsp_manager.get_stream(stream_name)

    if not stream:
        raise HTTPException(status_code=404, detail="Stream not found")

    frame = await stream.get_current_frame()
    if frame is None:
        raise HTTPException(status_code=503, detail="No frame available")

    frame_bytes = stream.encode_frame(frame)
    if frame_bytes is None:
        raise HTTPException(status_code=500, detail="Failed to encode frame")

    return StreamingResponse(
        io.BytesIO(frame_bytes),
        media_type="image/jpeg",
        headers={
            "Cache-Control": "no-cache, no-store, must-revalidate",
            "Pragma": "no-cache",
            "Expires": "0"
        }
    )


@router.get("/rtsp/detections/{stream_name}")
async def get_rtsp_detections(stream_name: str):
    """Get current detection results from RTSP stream"""
    stream = rtsp_detection_manager.get_stream(stream_name)
    if not stream:
        raise HTTPException(status_code=404, detail="Detection stream not found")

    detections = await stream.get_detections()
    return detections


@router.websocket("/ws/rtsp/{stream_name}")
async def websocket_rtsp_stream(websocket: WebSocket, stream_name: str):
    """WebSocket endpoint to stream RTSP frames (with detection if available)"""
    await websocket.accept()

    # Try detection stream first
    stream = rtsp_detection_manager.get_stream(stream_name)
    if not stream:
        # Fallback to raw stream
        stream = rtsp_manager.get_stream(stream_name)

    if not stream:
        await websocket.close(code=1008, reason="Stream not found")
        return

    try:
        last_frame_id = None
        while True:
            # Get current frame
            frame = await stream.get_current_frame()
            if frame is not None:
                # Create a simple frame ID based on frame content hash
                # to avoid sending duplicate frames
                frame_id = hash(frame.tobytes())

                if frame_id != last_frame_id:
                    # Encode frame
                    frame_bytes = stream.encode_frame(frame, quality=75)
                    if frame_bytes:
                        # Send frame via WebSocket
                        await websocket.send_bytes(frame_bytes)
                        last_frame_id = frame_id

            # Reduce sleep to increase responsiveness
            await asyncio.sleep(0.03)  # ~33 FPS max

    except WebSocketDisconnect:
        print(f"WebSocket disconnected for stream: {stream_name}")
    except Exception as e:
        print(f"Error in websocket_rtsp_stream: {e}")
    finally:
        try:
            await websocket.close()
        except:
            pass


@router.post("/rtsp/add")
async def add_rtsp_stream(stream_name: str, rtsp_url: str):
    """Add a new RTSP stream"""
    if rtsp_manager.get_stream(stream_name):
        raise HTTPException(status_code=400, detail="Stream already exists")

    success = rtsp_manager.add_stream(stream_name, rtsp_url)
    if not success:
        raise HTTPException(status_code=500, detail="Failed to connect to RTSP stream")

    # Start background task for new stream
    asyncio.create_task(read_rtsp_frames(stream_name))

    return {
        "message": "Stream added successfully",
        "stream_name": stream_name
    }


@router.delete("/rtsp/remove/{stream_name}")
async def remove_rtsp_stream(stream_name: str):
    """Remove an RTSP stream"""
    stream = rtsp_manager.get_stream(stream_name)
    if not stream:
        raise HTTPException(status_code=404, detail="Stream not found")

    rtsp_manager.remove_stream(stream_name)
    return {
        "message": "Stream removed successfully",
        "stream_name": stream_name
    }
