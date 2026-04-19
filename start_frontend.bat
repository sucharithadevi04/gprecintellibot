@echo off
title GPREC IntelliBot - Frontend (Streamlit)
echo.
echo ==========================================
echo   GPREC IntelliBot - Starting Frontend...
echo ==========================================
echo.

cd /d "%~dp0"

REM Check Python
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.10+ from https://python.org
    pause
    exit /b 1
)

echo Starting Streamlit Frontend on http://localhost:8501
echo.
echo IMPORTANT: Make sure the backend is running first!
echo Run start_backend.bat in another terminal.
echo.
cd frontend
streamlit run app.py --server.port 8501 --server.address localhost

pause
