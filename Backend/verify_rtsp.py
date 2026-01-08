import cv2
import os
import re
from urllib.parse import quote
from dotenv import load_dotenv
import time


def encode_rtsp_url(rtsp_url: str) -> str:
    """
    Tự động URL encode password trong RTSP URL để xử lý ký tự đặc biệt như $ # @ v.v.
    """
    if not rtsp_url or not rtsp_url.startswith('rtsp://'):
        return rtsp_url
    
    try:
        match = re.match(r'rtsp://([^:]+):([^@]+)@(.+)', rtsp_url)
        if match:
            username = match.group(1)
            password = match.group(2)
            rest = match.group(3)
            
            # Xóa escaped backslash (ví dụ: \$ -> $)
            password = password.replace('\\$', '$').replace('\\#', '#').replace('\\@', '@')
            
            if '%' not in password:  # Chưa encode
                encoded_password = quote(password, safe='')
                print(f"[*] Password đã được URL-encode (chứa ký tự đặc biệt)")
            else:
                encoded_password = password
            
            return f"rtsp://{username}:{encoded_password}@{rest}"
        return rtsp_url
    except:
        return rtsp_url

def verify_rtsp_connection():
    # Load .env file
    load_dotenv(os.path.join(os.path.dirname(__file__), ".env"))
    
    rtsp_url = os.getenv("RTSP_URL")
    if rtsp_url:
        rtsp_url = "".join(rtsp_url.split()) # Remove all whitespace/newlines
        rtsp_url = encode_rtsp_url(rtsp_url) # URL encode password
    
    enable_rtsp = os.getenv("ENABLE_RTSP", "False").lower() == "true"

    
    print(f"[*] Checking source configuration...")
    print(f"[*] ENABLE_RTSP: {enable_rtsp}")
    
    if rtsp_url:
        masked_url = rtsp_url[:15] + "..." + rtsp_url[-15:] if len(rtsp_url) > 30 else "TOO SHORT"
        print(f"[*] SOURCE URL (Masked): {masked_url}")
        print(f"[*] URL Length: {len(rtsp_url)} characters")
    else:
        print("[!] RTSP_URL is None")

    
    if not enable_rtsp:
        print("[!] RTSP/Stream is not enabled in .env")
        return
        
    if not rtsp_url:
        print("[!] RTSP_URL is not set in .env")
        return
        
    is_file = os.path.isfile(rtsp_url) or rtsp_url.startswith("./") or rtsp_url.startswith("../")
    
    if is_file:
        print(f"[*] Detected local file source. Checking if file exists...")
        if os.path.exists(rtsp_url):
            print(f"[OK] File exists: {rtsp_url}")
        else:
            print(f"[ERROR] File not found: {rtsp_url}")
            # Try relative to app dir
            alt_path = os.path.join(os.path.dirname(__file__), "app", rtsp_url.lstrip("./"))
            if os.path.exists(alt_path):
                print(f"[*] Found alternate path: {alt_path}")
                rtsp_url = alt_path
            else:
                return

    print(f"[*] Attempting to open source: {rtsp_url[:60]}...")
    
    # Set environment variable to force TCP for RTSP (Common fix when VLC works but OpenCV doesn't)
    os.environ["OPENCV_FFMPEG_CAPTURE_OPTIONS"] = "rtsp_transport;tcp"
    
    # Try to open the stream with FFMPEG backend
    cap = cv2.VideoCapture(rtsp_url, cv2.CAP_FFMPEG)
    
    # Wait for connection (timeout)
    start_time = time.time()
    connected = False
    
    timeout = 2 if is_file else 15 # Longer timeout for real camera
    
    while time.time() - start_time < timeout:
        if cap.isOpened():
            connected = True
            break
        time.sleep(0.5)

        
    if connected:
        print("[OK] Successfully opened source!")
        
        # Try to read a frame
        ret, frame = cap.read()
        if ret:
            print(f"[OK] Frame captured successfully! Size: {frame.shape}")
        else:
            print("[!] Opened, but failed to capture a frame.")
            
        cap.release()
    else:
        print("[ERROR] Failed to open source (timeout or unreachable).")
        if not is_file:
            print("[*] Please check:")
            print("    1. If the camera is online")
            print("    2. If the RTSP URL is correct")
            print("    3. If there are network/firewall issues")


if __name__ == "__main__":
    verify_rtsp_connection()
