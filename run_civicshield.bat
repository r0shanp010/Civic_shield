@echo off
title CivicShield - AI Anti-Corruption Platform Launcher
color 0B
echo ===============================================================================
echo            CIVICSHIELD - AI COMPLAINT MANAGEMENT PLATFORM
echo ===============================================================================
echo.
echo [1/2] Starting FastAPI Backend on http://127.0.0.1:8000 ...
start "CivicShield Backend (FastAPI)" cmd /k "cd /d %~dp0backend && python -m uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload"

timeout /t 2 /nobreak >nul

echo [2/2] Starting React Vite Frontend on http://localhost:5173 ...
start "CivicShield Frontend (Vite)" cmd /k "cd /d %~dp0frontend && npm run dev"

echo.
echo ===============================================================================
echo    Both servers have been started in separate background windows!
echo    - Frontend Portal:  http://localhost:5173/
echo    - Backend API Docs: http://127.0.0.1:8000/docs
echo ===============================================================================
pause
