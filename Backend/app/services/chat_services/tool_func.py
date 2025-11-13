import requests
import json
from langchain_core.tools import tool
from typing import Annotated

BASE_URL = "http://localhost:8000"

@tool
def get_roads() -> str:
    """Lấy danh sách các tuyến đường hiện có từ API.
    Trả về chuỗi JSON chứa danh sách tên các tuyến đường.
    """
    try:
        response = requests.get(f"{BASE_URL}/roads_name")
        if response.status_code == 200:
            data = response.json()
            if data and data != []:
                return json.dumps(data, ensure_ascii=False)
            else:
                return "Không có tuyến đường nào."
        elif response.status_code == 500:
            return "Lỗi: Dữ liệu bị lỗi, kiểm tra core"
        else:
            return f"Lỗi API: {response.status_code} - {response.text}"
    except requests.exceptions.ConnectionError:
        return "Không thể kết nối đến API server. Kiểm tra xem server có đang chạy không."
    except requests.exceptions.RequestException as e:
        return f"Lỗi khi gọi API: {str(e)}"
    except Exception as e:
        return f"Lỗi không xác định: {str(e)}"
    
@tool
def get_frame_road(road_name: Annotated[str, "Tên tuyến đường"]) -> str:
    """Lấy url bytecode cho frame (ảnh) hiện tại của tuyến đường theo tên (road_name).
    Trả về url của ảnh JPEG.
    """
    try:
        response = requests.get(f"{BASE_URL}/frames/{road_name}")
        if response.status_code == 200:
            return f"{BASE_URL}/frames/{road_name}"
        elif response.status_code == 500:
            return "Lỗi: Dữ liệu bị lỗi, kiểm tra core"
        else:
            return f"Lỗi API: {response.status_code} - {response.text}"
    except requests.exceptions.ConnectionError:
        return "Không thể kết nối đến API server. Kiểm tra xem server có đang chạy không."
    except requests.exceptions.RequestException as e:
        return f"Lỗi khi gọi API: {str(e)}"
    except Exception as e:
        return f"Lỗi không xác định: {str(e)}"

@tool
def get_info_road(road_name: Annotated[str, "Tên tuyến đường"]) -> str:
    """Lấy thông tin (info) hiện tại của tuyến đường theo tên (road_name).
    Trả về chuỗi JSON chứa số lượng xe, tốc độ, v.v.
    """
    try:
        response = requests.get(f"{BASE_URL}/info/{road_name}")
        if response.status_code == 200:
            data = response.json()
            if data and data != {}:
                return json.dumps(data, ensure_ascii=False)
            else:
                return "Không lấy được info cho tuyến đường này."
        elif response.status_code == 500:
            return "Lỗi: Dữ liệu bị lỗi, kiểm tra core"
        else:
            return f"Lỗi API: {response.status_code} - {response.text}"
    except requests.exceptions.ConnectionError:
        return "Không thể kết nối đến API server. Kiểm tra xem server có đang chạy không."
    except requests.exceptions.RequestException as e:
        return f"Lỗi khi gọi API: {str(e)}"
    except Exception as e:
        return f"Lỗi không xác định: {str(e)}"

@tool
def get_camera_live_frame() -> str:
    """Lấy url frame (ảnh) hiện tại từ camera RTSP trực tiếp với detection (bounding boxes).
    Camera này có tên là 'camera_live' và hiển thị phát hiện YOLO real-time.
    Trả về URL của ảnh JPEG với các bounding boxes xung quanh xe được phát hiện.
    """
    try:
        response = requests.get(f"{BASE_URL}/rtsp/frame/camera_live")
        if response.status_code == 200:
            return f"{BASE_URL}/rtsp/frame/camera_live"
        elif response.status_code == 503:
            return "Camera live chưa có frame nào. Vui lòng thử lại sau."
        elif response.status_code == 404:
            return "Camera live không tồn tại hoặc chưa được khởi động."
        else:
            return f"Lỗi API: {response.status_code} - {response.text}"
    except requests.exceptions.ConnectionError:
        return "Không thể kết nối đến API server. Kiểm tra xem server có đang chạy không."
    except requests.exceptions.RequestException as e:
        return f"Lỗi khi gọi API: {str(e)}"
    except Exception as e:
        return f"Lỗi không xác định: {str(e)}"

@tool
def get_camera_live_detections() -> str:
    """Lấy thông tin phát hiện (detection) hiện tại từ camera RTSP trực tiếp.
    Trả về chuỗi JSON chứa số lượng xe ô tô (count_car), xe máy (count_motor),
    tốc độ (speed_car, speed_motor), và tổng số phương tiện (total_vehicles).
    """
    try:
        response = requests.get(f"{BASE_URL}/rtsp/detections/camera_live")
        if response.status_code == 200:
            data = response.json()
            if data and data != {}:
                return json.dumps(data, ensure_ascii=False)
            else:
                return "Không lấy được thông tin detection từ camera live."
        elif response.status_code == 404:
            return "Camera live không tồn tại hoặc chưa được khởi động."
        else:
            return f"Lỗi API: {response.status_code} - {response.text}"
    except requests.exceptions.ConnectionError:
        return "Không thể kết nối đến API server. Kiểm tra xem server có đang chạy không."
    except requests.exceptions.RequestException as e:
        return f"Lỗi khi gọi API: {str(e)}"
    except Exception as e:
        return f"Lỗi không xác định: {str(e)}"
