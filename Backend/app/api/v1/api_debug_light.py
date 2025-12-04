# ============================================================================
# FILE: api_debug_light.py - DEBUG ENDPOINT CHO TRAFFIC LIGHT DETECTION
# ============================================================================
# API endpoints để debug và calibrate red light detection

from fastapi import APIRouter, HTTPException
from fastapi.responses import Response
import cv2
import numpy as np
from typing import Dict, Optional
from app.api.v1.api_rtsp import rtsp_detection_manager

router = APIRouter()


@router.get("/debug/light-detection/{camera_name}")
async def debug_light_detection(camera_name: str, show_masks: bool = False):
    """
    Debug traffic light detection cho camera

    Args:
        camera_name: Tên camera (e.g., "camera_live")
        show_masks: True = return masks visualization, False = return stats only

    Returns:
        JSON với thông tin chi tiết về detection
        hoặc image với masks nếu show_masks=True
    """
    # Lấy stream từ manager
    stream = rtsp_detection_manager.get_stream(camera_name)
    if not stream:
        raise HTTPException(status_code=404, detail=f"Camera {camera_name} not found")

    # Lấy frame hiện tại
    frame = await stream.get_current_frame()
    if frame is None:
        raise HTTPException(status_code=500, detail="No frame available")

    # Lấy detector
    detector = stream.red_light_detector
    if not detector.traffic_light_roi:
        raise HTTPException(
            status_code=400,
            detail="Traffic light ROI not configured. Please call /violations/config first"
        )

    # Detect với debug mode ON
    detected_color = detector.detect_light_color(frame, debug=True)

    # Lấy ROI và phân tích chi tiết
    x, y, w, h = detector.traffic_light_roi
    roi = frame[y:y+h, x:x+w]
    hsv = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)

    # Tạo masks cho từng màu
    # Red masks (3 ranges)
    lower_red1 = np.array([0, 70, 50])
    upper_red1 = np.array([10, 255, 255])
    mask_red1 = cv2.inRange(hsv, lower_red1, upper_red1)

    lower_red2 = np.array([160, 70, 50])
    upper_red2 = np.array([180, 255, 255])
    mask_red2 = cv2.inRange(hsv, lower_red2, upper_red2)

    lower_red3 = np.array([0, 50, 100])
    upper_red3 = np.array([15, 255, 255])
    mask_red3 = cv2.inRange(hsv, lower_red3, upper_red3)

    mask_red = cv2.bitwise_or(mask_red1, mask_red2)
    mask_red = cv2.bitwise_or(mask_red, mask_red3)

    # Yellow mask
    lower_yellow = np.array([15, 70, 50])
    upper_yellow = np.array([35, 255, 255])
    mask_yellow = cv2.inRange(hsv, lower_yellow, upper_yellow)

    # Green mask
    lower_green = np.array([40, 50, 50])
    upper_green = np.array([90, 255, 255])
    mask_green = cv2.inRange(hsv, lower_green, upper_green)

    # Đếm pixels
    red_pixels = cv2.countNonZero(mask_red)
    yellow_pixels = cv2.countNonZero(mask_yellow)
    green_pixels = cv2.countNonZero(mask_green)

    # Tính average HSV values trong ROI
    avg_h = np.mean(hsv[:, :, 0])
    avg_s = np.mean(hsv[:, :, 1])
    avg_v = np.mean(hsv[:, :, 2])

    if show_masks:
        # Tạo visualization với masks
        vis_width = w * 4 + 15  # ROI + 3 masks với spacing
        vis_height = h
        visualization = np.zeros((vis_height, vis_width, 3), dtype=np.uint8)

        # 1. Original ROI
        visualization[0:h, 0:w] = roi

        # 2. Red mask (màu đỏ)
        mask_red_colored = cv2.cvtColor(mask_red, cv2.COLOR_GRAY2BGR)
        mask_red_colored[mask_red > 0] = [0, 0, 255]  # Red
        visualization[0:h, w+5:w*2+5] = mask_red_colored

        # 3. Yellow mask (màu vàng)
        mask_yellow_colored = cv2.cvtColor(mask_yellow, cv2.COLOR_GRAY2BGR)
        mask_yellow_colored[mask_yellow > 0] = [0, 255, 255]  # Yellow
        visualization[0:h, w*2+10:w*3+10] = mask_yellow_colored

        # 4. Green mask (màu xanh)
        mask_green_colored = cv2.cvtColor(mask_green, cv2.COLOR_GRAY2BGR)
        mask_green_colored[mask_green > 0] = [0, 255, 0]  # Green
        visualization[0:h, w*3+15:w*4+15] = mask_green_colored

        # Thêm text labels
        cv2.putText(visualization, "Original", (5, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
        cv2.putText(visualization, f"Red: {red_pixels}", (w+10, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
        cv2.putText(visualization, f"Yellow: {yellow_pixels}", (w*2+15, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
        cv2.putText(visualization, f"Green: {green_pixels}", (w*3+20, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)

        # Text kết quả phía dưới
        result_text = f"DETECTED: {detected_color.upper()}"
        cv2.putText(visualization, result_text, (5, h-10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

        # Encode và return image
        _, buffer = cv2.imencode('.jpg', visualization)
        return Response(content=buffer.tobytes(), media_type="image/jpeg")

    # Return JSON stats
    return {
        "camera_name": camera_name,
        "detected_color": detected_color,
        "roi": {
            "x": x,
            "y": y,
            "width": w,
            "height": h,
            "total_pixels": w * h
        },
        "color_pixels": {
            "red": red_pixels,
            "yellow": yellow_pixels,
            "green": green_pixels
        },
        "hsv_averages": {
            "hue": round(avg_h, 2),
            "saturation": round(avg_s, 2),
            "value": round(avg_v, 2)
        },
        "analysis": {
            "is_red_detected": red_pixels > 20,
            "is_yellow_detected": yellow_pixels > 20,
            "is_green_detected": green_pixels > 20,
            "confidence": round(max(red_pixels, yellow_pixels, green_pixels) / (w * h) * 100, 2)
        },
        "suggestions": get_detection_suggestions(red_pixels, yellow_pixels, green_pixels, detected_color)
    }


def get_detection_suggestions(red_px, yellow_px, green_px, detected) -> list:
    """Generate suggestions based on detection results"""
    suggestions = []

    total_px = red_px + yellow_px + green_px

    if total_px < 20:
        suggestions.append("❌ ROI có thể SAI - không detect đủ pixels")
        suggestions.append("💡 Hãy kiểm tra lại vị trí ROI (x, y, w, h)")
        suggestions.append("💡 ROI phải chứa ĐÚNG vùng đèn tín hiệu")

    if detected == 'unknown':
        suggestions.append("⚠️ Không nhận diện được màu đèn")
        if total_px < 20:
            suggestions.append("💡 ROI không chứa đèn hoặc đèn tắt")
        else:
            suggestions.append("💡 HSV ranges có thể cần điều chỉnh")

    if red_px > 100 and detected != 'red':
        suggestions.append("🔴 Có nhiều pixels đỏ nhưng không detect là RED")
        suggestions.append("💡 Vàng/xanh đang chiếm ưu thế hơn")

    if not suggestions:
        suggestions.append("✅ Detection hoạt động tốt!")

    return suggestions


@router.post("/debug/calibrate-roi/{camera_name}")
async def calibrate_roi_auto(camera_name: str):
    """
    Tự động tìm ROI tốt nhất cho traffic light

    Algorithm:
    1. Lấy frame hiện tại
    2. Scan toàn bộ frame tìm vùng có nhiều đỏ nhất
    3. Return ROI gợi ý

    NOTE: Chỉ là GỢI Ý, vẫn cần human verify
    """
    stream = rtsp_detection_manager.get_stream(camera_name)
    if not stream:
        raise HTTPException(status_code=404, detail=f"Camera {camera_name} not found")

    frame = await stream.get_current_frame()
    if frame is None:
        raise HTTPException(status_code=500, detail="No frame available")

    # Convert to HSV
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Tạo red mask cho toàn bộ frame
    lower_red1 = np.array([0, 70, 50])
    upper_red1 = np.array([10, 255, 255])
    mask_red1 = cv2.inRange(hsv, lower_red1, upper_red1)

    lower_red2 = np.array([160, 70, 50])
    upper_red2 = np.array([180, 255, 255])
    mask_red2 = cv2.inRange(hsv, lower_red2, upper_red2)

    mask_red = cv2.bitwise_or(mask_red1, mask_red2)

    # Tìm contours (vùng đỏ)
    contours, _ = cv2.findContours(mask_red, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    if not contours:
        return {
            "success": False,
            "message": "Không tìm thấy vùng đỏ nào trong frame",
            "suggestion": "Đảm bảo đèn đỏ đang BẬT khi chạy calibration"
        }

    # Lọc contours theo diện tích (đèn tín hiệu thường 20-200 pixels)
    valid_contours = []
    for cnt in contours:
        area = cv2.contourArea(cnt)
        if 20 < area < 500:  # Đèn tín hiệu thường nhỏ
            x, y, w, h = cv2.boundingRect(cnt)
            # Đèn tròn: aspect ratio gần 1
            aspect_ratio = w / h if h > 0 else 0
            if 0.5 < aspect_ratio < 2.0:
                valid_contours.append((x, y, w, h, area))

    if not valid_contours:
        return {
            "success": False,
            "message": "Không tìm thấy vùng đỏ phù hợp (có thể quá lớn hoặc quá nhỏ)",
            "total_red_regions": len(contours)
        }

    # Sắp xếp theo diện tích giảm dần
    valid_contours.sort(key=lambda x: x[4], reverse=True)

    # Top 3 candidates
    candidates = []
    for i, (x, y, w, h, area) in enumerate(valid_contours[:3]):
        candidates.append({
            "rank": i + 1,
            "roi": {"x": x, "y": y, "w": w, "h": h},
            "area": area,
            "center": {"x": x + w//2, "y": y + h//2}
        })

    return {
        "success": True,
        "message": f"Tìm thấy {len(candidates)} vùng đỏ phù hợp",
        "recommended_roi": candidates[0]["roi"] if candidates else None,
        "all_candidates": candidates,
        "instructions": [
            "1. Kiểm tra ROI được gợi ý trên frame",
            "2. Gọi POST /violations/config với ROI này",
            "3. Test lại với GET /debug/light-detection"
        ]
    }


@router.get("/debug/test-hsv-ranges")
async def test_hsv_ranges():
    """
    Return current HSV ranges đang sử dụng

    Để user có thể điều chỉnh nếu cần
    """
    return {
        "red_ranges": [
            {
                "name": "Red Range 1 (Bright)",
                "lower": [0, 70, 50],
                "upper": [10, 255, 255],
                "description": "Đỏ sáng, đèn LED mạnh"
            },
            {
                "name": "Red Range 2 (Dark)",
                "lower": [160, 70, 50],
                "upper": [180, 255, 255],
                "description": "Đỏ thẫm, đèn xa/tối"
            },
            {
                "name": "Red Range 3 (Very Bright)",
                "lower": [0, 50, 100],
                "upper": [15, 255, 255],
                "description": "Đỏ rất sáng, LED cao cấp"
            }
        ],
        "yellow_range": {
            "lower": [15, 70, 50],
            "upper": [35, 255, 255]
        },
        "green_range": {
            "lower": [40, 50, 50],
            "upper": [90, 255, 255]
        },
        "min_pixels_threshold": 20,
        "notes": [
            "HSV ranges đã được tối ưu cho đa dạng lighting conditions",
            "Nếu vẫn detect sai, có thể do ROI không đúng",
            "Hue: 0-180°, Saturation: 0-255, Value: 0-255"
        ]
    }
