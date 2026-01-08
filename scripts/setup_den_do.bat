@echo off
chcp 65001 >nul
echo ============================================================
echo    SETUP PHÁT HIỆN VƯỢT ĐÈN ĐỎ
echo ============================================================
echo.
echo Tool này giúp bạn thiết lập:
echo   1. ROI (vùng chứa đèn tín hiệu)
echo   2. Stop Line (vạch dừng)
echo.
echo Hướng dẫn:
echo   - BƯỚC 1: Click 4 góc quanh đèn tín hiệu
echo   - BƯỚC 2: Click 2 điểm để vẽ vạch dừng
echo   - Nhấn 's' để lưu, 'r' để vẽ lại, 'q' để thoát
echo.
echo ============================================================
echo.

cd ..\Backend
python scripts\setup_red_light_detection.py 0

pause
