@echo off
title CivicShield Web Application Launcher
color 0A

echo ====================================================================
echo        CIVICSHIELD AI-BASED GRIEVANCE MANAGEMENT SYSTEM
echo ====================================================================
echo.
echo [1/3] Starting FastAPI Backend on http://127.0.0.1:8000 ...
start "CivicShield Backend (FastAPI)" cmd /k "cd backend && python -m uvicorn app.main:app --host 127.0.0.1 --port 8000"

timeout /t 3 /nobreak >nul

echo [2/3] Starting React Vite Frontend on http://localhost:5173 ...
start "CivicShield Frontend (React)" cmd /k "cd frontend && npm run dev"

timeout /t 3 /nobreak >nul

echo [3/3] Launching Web Browser ...
start http://localhost:5173

echo.
echo ====================================================================
echo   CivicShield Web Application is now running!
echo   - Frontend: http://localhost:5173
echo   - Backend:  http://localhost:8000
echo   - API Docs: http://localhost:8000/docs
echo ====================================================================
echo.
pause
