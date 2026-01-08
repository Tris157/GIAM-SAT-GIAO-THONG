"""
API endpoints for Red Light Detection Configuration
Quản lý cấu hình ROI và Stop Line cho phát hiện vượt đèn đỏ
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional
import json
import os
from datetime import datetime

router = APIRouter()
from app.utils.dependencies import get_current_admin_user
from app.models.user import User
from fastapi import Depends

# Đường dẫn lưu config
CONFIG_DIR = "app/config"
CONFIG_FILE = f"{CONFIG_DIR}/red_light_config_camera_live.json"


class TrafficLightROI(BaseModel):
    """Model cho ROI đèn tín hiệu"""
    x: int
    y: int
    w: int
    h: int


class RedLightConfig(BaseModel):
    """Model cho config Red Light Detection"""
    camera_name: str
    traffic_light_roi: TrafficLightROI
    stop_line_y: int
    camera_source: Optional[str] = None


class RedLightConfigResponse(BaseModel):
    """Response model"""
    success: bool
    message: str
    config: Optional[RedLightConfig] = None


@router.post("/save", response_model=RedLightConfigResponse)
async def save_red_light_config(
    config: RedLightConfig,
    current_admin: User = Depends(get_current_admin_user)
):
    """
    Lưu cấu hình ROI và Stop Line

    Args:
        config: Cấu hình bao gồm ROI và Stop Line Y

    Returns:
        Response với trạng thái và message
    """
    try:
        # Tạo thư mục nếu chưa tồn tại
        os.makedirs(CONFIG_DIR, exist_ok=True)

        # Tạo config dict
        config_data = {
            "camera_name": config.camera_name,
            "traffic_light_roi": {
                "x": config.traffic_light_roi.x,
                "y": config.traffic_light_roi.y,
                "w": config.traffic_light_roi.w,
                "h": config.traffic_light_roi.h
            },
            "stop_line_y": config.stop_line_y,
            "created_at": datetime.now().isoformat(),
            "camera_source": config.camera_source or "camera_live"
        }

        # Lưu vào file JSON
        with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
            json.dump(config_data, f, indent=2, ensure_ascii=False)

        return RedLightConfigResponse(
            success=True,
            message="Đã lưu cấu hình thành công!",
            config=config
        )

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Lỗi khi lưu cấu hình: {str(e)}"
        )


@router.get("/load", response_model=RedLightConfigResponse)
async def load_red_light_config():
    """
    Load cấu hình ROI và Stop Line đã lưu

    Returns:
        Config đã lưu hoặc null nếu chưa có
    """
    try:
        if not os.path.exists(CONFIG_FILE):
            return RedLightConfigResponse(
                success=False,
                message="Chưa có cấu hình nào được lưu",
                config=None
            )

        # Đọc config từ file
        with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
            config_data = json.load(f)

        # Convert sang model
        config = RedLightConfig(
            camera_name=config_data["camera_name"],
            traffic_light_roi=TrafficLightROI(**config_data["traffic_light_roi"]),
            stop_line_y=config_data["stop_line_y"],
            camera_source=config_data.get("camera_source")
        )

        return RedLightConfigResponse(
            success=True,
            message="Đã load cấu hình thành công!",
            config=config
        )

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Lỗi khi load cấu hình: {str(e)}"
        )


@router.delete("/delete", response_model=RedLightConfigResponse)
async def delete_red_light_config(
    current_admin: User = Depends(get_current_admin_user)
):
    """
    Xóa cấu hình đã lưu

    Returns:
        Response với trạng thái
    """
    try:
        if os.path.exists(CONFIG_FILE):
            os.remove(CONFIG_FILE)
            return RedLightConfigResponse(
                success=True,
                message="Đã xóa cấu hình thành công!",
                config=None
            )
        else:
            return RedLightConfigResponse(
                success=False,
                message="Không tìm thấy cấu hình để xóa",
                config=None
            )

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Lỗi khi xóa cấu hình: {str(e)}"
        )
