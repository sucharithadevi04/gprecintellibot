@echo off
title GPREC IntelliBot - Backend Server
echo.
echo ==========================================
echo   GPREC IntelliBot - Starting Backend...
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

REM Install dependencies if not installed
echo Checking dependencies...
pip install -r requirements.txt --quiet

echo.
echo Starting FastAPI Backend on http://localhost:8000
echo API Docs available at: http://localhost:8000/docs
echo.
cd backend
python -m uvicorn main:app --host 0.0.0.0 --port 8000 --reload

pause
