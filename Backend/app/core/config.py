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


class SettingMetricTransport:
    REGIONS = [
        np.array([[50, 400], [50, 265], [370, 130], [540, 130], [490, 400]]),
        np.array([[230, 400], [90, 260], [350, 200], [600, 320], [600, 400]]),
        np.array([[50, 400], [50, 340], [400, 125], [530, 185], [470, 400]]),
        np.array([[140, 400], [400, 200], [550, 200], [530, 400]]),
        np.array([[50, 400], [50, 320], [390, 130], [550, 220], [480, 400]]),
    ]

    PATH_VIDEOS = [
        "./app/video_test/Văn Quán.mp4",
        "./app/video_test/Văn Phú.mp4",
        "./app/video_test/Nguyễn Trãi.mp4",
        "./app/video_test/Ngã Tư Sở.mp4",
        "./app/video_test/Đường Láng.mp4",
    ]

    METER_PER_PIXELS = [0.03,
                        0.09,
                        0.5,
                        0.11,
                        0.06
                        ]
    MODELS_PATH = r'./app/ai_models/model N/original model/best.pt'

    DEVICE = 'cuda:0'  # Auto GPU detection in services


settings = SettingServer()