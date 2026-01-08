import os
from dotenv import load_dotenv
import numpy as np

load_dotenv()

class SettingServer:
    PROJECT_NAME = "FastAPI CRUD with JWT"
    DATABASE_URL = os.getenv("DATABASE_URL")
    JWT_SECRET = os.getenv("JWT_SECRET_KEY")
    JWT_ALGORITHM = os.getenv("JWT_ALGORITHM")
    ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))
    
    # RTSP Configuration
    ENABLE_RTSP = os.getenv("ENABLE_RTSP", "False").lower() == "true"
    RTSP_URL = os.getenv("RTSP_URL", "")
    RTSP_URL_INTERNAL = os.getenv("RTSP_URL_INTERNAL", "rtsp://admin:abcd1234@192.168.1.205:554/cam/realmonitor?channel=1&subtype=0")
    RTSP_METER_PER_PIXEL = float(os.getenv("RTSP_METER_PER_PIXEL", "0.04"))
    # ROI for RTSP camera - None = nhận diện toàn bộ frame
    RTSP_REGION = None  # Đã tắt ROI filtering


class SettingMetricTransport:
    REGIONS = [
        np.array([[0, 351], [590, 388], [337, 185], [260, 189]]),
        np.array([[345, 391], [332, 177], [268, 164], [2, 304], [6, 384]]),
        np.array([[40, 233], [212, 105], [224, 61], [338, 68], [286, 265], [239, 333]]),
        np.array([[6, 248], [330, 130], [552, 123], [461, 395], [5, 384]]),
    ]

    PATH_VIDEOS = [
        "./app/video_test/CAO TOC-LT-DG.avi",
        "./app/video_test/CAO-TOC-TL.avi",
        "./app/video_test/CAU RONG.mp4",
        "./app/video_test/QUANG TRUNG.mp4",
    ]

    METER_PER_PIXELS = [0.03,
                        0.09,
                        0.5,
                        0.11
                        ]
    MODELS_PATH = r'./app/ai_models/model N/original model/best.pt'

    DEVICE = 'cuda:0'  # Auto GPU detection in services


settings = SettingServer()