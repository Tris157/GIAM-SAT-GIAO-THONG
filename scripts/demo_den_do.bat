@echo off
chcp 65001 >nul
echo ========================================
echo   🚦 DEMO PHÁT HIỆN ĐÈN TÍN HIỆU
echo   Smart Traffic Monitoring System
echo ========================================
echo.
echo Đây là demo phát hiện màu đèn tín hiệu giao thông
echo (ĐỎ - VÀNG - XANH)
echo.

:MENU
echo ========================================
echo CHỌN LOẠI CAMERA:
echo ========================================
echo [1] Camera USB (Logitech, Microsoft...)
echo [2] Camera IP RTSP
echo [3] Video file (test)
echo [0] Thoát
echo ========================================
echo.
set /p choice="Nhập lựa chọn (0-3): "

if "%choice%"=="1" goto USB_CAMERA
if "%choice%"=="2" goto RTSP_CAMERA
if "%choice%"=="3" goto VIDEO_FILE
if "%choice%"=="0" goto END
goto MENU

:USB_CAMERA
echo.
echo ========================================
echo 📹 CAMERA USB
echo ========================================
echo.
set /p usb_index="Nhập index camera USB (0, 1, 2...): "
echo.
echo Đang khởi động camera USB %usb_index%...
echo.
cd ..\Backend
python scripts\demo_traffic_light_detection.py %usb_index%
cd ..
goto END

:RTSP_CAMERA
echo.
echo ========================================
echo 📹 CAMERA IP RTSP
echo ========================================
echo.
echo Định dạng: rtsp://username:password@ip:port/path
echo Ví dụ: rtsp://admin:Admin123@192.168.1.100:554/stream
echo.
set /p rtsp_url="Nhập RTSP URL: "
echo.
echo Đang kết nối đến %rtsp_url%...
echo.
cd ..\Backend
python scripts\demo_traffic_light_detection.py "%rtsp_url%"
cd ..
goto END

:VIDEO_FILE
echo.
echo ========================================
echo 🎥 VIDEO FILE
echo ========================================
echo.
set /p video_path="Nhập đường dẫn video file: "
echo.
echo Đang mở video %video_path%...
echo.
cd ..\Backend
python scripts\demo_traffic_light_detection.py "%video_path%"
cd ..
goto END

:END
echo.
echo ========================================
echo   Cảm ơn đã sử dụng!
echo ========================================
pause
