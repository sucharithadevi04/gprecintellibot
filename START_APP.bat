@echo off
title GPREC IntelliBot - Full App Launcher
echo.
echo ==========================================
echo    GPREC IntelliBot - Starting App...
echo ==========================================
echo.

cd /d "%~dp0"

echo Step 1: Installing dependencies...
pip install -r requirements.txt --quiet
echo Dependencies ready!
echo.

echo Step 2: Starting Backend (FastAPI)...
start "GPREC Backend" cmd /k "cd backend && python -m uvicorn main:app --host 0.0.0.0 --port 8000 --reload"

echo Waiting for backend to initialize...
timeout /t 4 /nobreak >nul

echo.
echo Step 3: Starting Frontend (Streamlit)...
start "GPREC Frontend" cmd /k "cd frontend && streamlit run app.py --server.port 8501 --server.address localhost"

echo.
echo ==========================================
echo   GPREC IntelliBot is running!
echo.
echo   Frontend: http://localhost:8501
echo   Backend:  http://localhost:8000
echo   API Docs: http://localhost:8000/docs
echo ==========================================
echo.
echo Press any key to open the app in browser...
pause >nul

start http://localhost:8501
