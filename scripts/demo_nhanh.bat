@echo off
REM ========================================================================
REM   SMART TRAFFIC MONITORING SYSTEM - DEMO SCRIPT
REM   Phiên bản: 3.0.0
REM   Dành cho: Demo nhanh cho đối tác camera
REM ========================================================================

echo.
echo ========================================================================
echo.
echo              SMART TRAFFIC MONITORING SYSTEM
echo                      DEMO SCRIPT v3.0
echo.
echo ========================================================================
echo.

REM Kiểm tra Python
echo [CHECK 1/4] Kiem tra Python...
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python khong duoc cai dat!
    echo Vui long cai Python 3.9-3.12 tu: https://www.python.org
    pause
    exit /b 1
)
echo [OK] Python da cai dat

REM Kiểm tra Node.js
echo [CHECK 2/4] Kiem tra Node.js...
node --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Node.js khong duoc cai dat!
    echo Vui long cai Node.js 18+ tu: https://nodejs.org
    pause
    exit /b 1
)
echo [OK] Node.js da cai dat

REM Kiểm tra Backend venv
echo [CHECK 3/4] Kiem tra Backend virtual environment...
if not exist "..\Backend\venv\Scripts\python.exe" (
    echo [WARNING] Virtual environment chua duoc tao!
    echo Dang tao virtual environment...
    cd ..\Backend
    python -m venv venv
    echo [OK] Virtual environment da duoc tao
    cd ..
)
echo [OK] Backend venv da san sang

REM Kiểm tra Frontend node_modules
echo [CHECK 4/4] Kiem tra Frontend dependencies...
if not exist "..\Frontend\node_modules" (
    echo [WARNING] Node modules chua duoc cai!
    echo Vui long chay: cd ..\Frontend && npm install
    pause
)
echo [OK] Frontend dependencies da san sang

echo.
echo ========================================================================
echo   TAT CA KIEM TRA HOAN TAT!
echo   Dang khoi dong he thong...
echo ========================================================================
echo.

REM ========================================================================
REM   KHOI DONG BACKEND
REM ========================================================================

echo [STEP 1/3] Khoi dong Backend Server...
start "Backend Server - Smart Traffic" cmd /k "cd ..\Backend\app && ..\..\venv\Scripts\python.exe -m uvicorn main:app --reload --host 0.0.0.0 --port 8000"

echo Dang cho Backend khoi dong...
timeout /t 12 /nobreak >nul

echo [OK] Backend dang chay tai: http://localhost:8000
echo      API Docs:              http://localhost:8000/api/docs
echo.

REM ========================================================================
REM   KHOI DONG FRONTEND
REM ========================================================================

echo [STEP 2/3] Khoi dong Frontend...
start "Frontend - Smart Traffic" cmd /k "cd ..\Frontend && pnpm run dev"

echo Dang cho Frontend khoi dong...
timeout /t 8 /nobreak >nul

echo [OK] Frontend dang chay tai: http://localhost:5173
echo.

REM ========================================================================
REM   MO TRINH DUYET
REM ========================================================================

echo [STEP 3/3] Mo trinh duyet...
timeout /t 3 /nobreak >nul
start http://localhost:5173

echo.
echo ========================================================================
echo.
echo              HE THONG DA SAN SANG DE DEMO!
echo.
echo   Frontend (Dashboard):  http://localhost:5173
echo   Backend (API):         http://localhost:8000
echo   API Documentation:     http://localhost:8000/api/docs
echo   Health Check:          http://localhost:8000/api/health
echo.
echo ========================================================================
echo.
echo HUONG DAN SU DUNG:
echo   1. Trinh duyet se tu dong mo Dashboard
echo   2. Dang nhap hoac dung chuc nang moi luon
echo   3. Tab 'Dashboard'  - Xem tong quan giao thong
echo   4. Tab 'Analytics'  - Xem bieu do phan tich
echo   5. Tab 'Chat'       - Thu chatbot AI
echo   6. Tab 'Live'       - Xem camera truc tiep (neu da cau hinh)
echo.
echo DE TAT HE THONG:
echo   - Nhan Ctrl+C trong cac cua so Backend/Frontend
echo   - Hoac dong tat ca cua so terminal
echo.
echo ========================================================================
echo.
pause
