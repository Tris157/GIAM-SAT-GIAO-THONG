@echo off
echo ========================================
echo    CLEAN UP SMART TRAFFIC PROJECT
echo ========================================
echo.

echo [1/4] Cleaning Python cache files...
for /d /r Backend %%d in (__pycache__) do @if exist "%%d" rd /s /q "%%d" 2>nul
del /s /q Backend\*.pyc 2>nul
del /s /q Backend\*.pyo 2>nul
echo     ✓ Python cache cleaned

echo [2/4] Cleaning log files...
del /s /q Backend\*.log 2>nul
del /s /q Frontend\*.log 2>nul
echo     ✓ Log files cleaned

echo [3/4] Cleaning OS temp files...
del /q nul 2>nul
del /s /q Thumbs.db 2>nul
del /s /q desktop.ini 2>nul
echo     ✓ OS temp files cleaned

echo [4/4] Checking git status...
git status --short
echo.

echo ========================================
echo    CLEANUP COMPLETED!
echo ========================================
echo.
echo Repository is now optimized for git push.
echo Models and venv are gitignored - download separately.
echo.
pause
