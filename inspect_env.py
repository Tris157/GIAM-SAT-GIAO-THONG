import os
from dotenv import load_dotenv

# Load .env from Backend directory
load_dotenv("Backend/.env", override=True)

rtsp_url = os.getenv("RTSP_URL")
print(f"RTSP_URL (RAW from env): {rtsp_url}")

if rtsp_url and "$" in rtsp_url:
    print("Found $ in URL. Checking if it's correctly loaded.")
elif not rtsp_url:
    print("RTSP_URL is None or Empty!")
