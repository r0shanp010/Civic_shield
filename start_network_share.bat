@echo off
title CivicShield Local Network Host
color 0B

echo ====================================================================
echo        CIVICSHIELD - LOCAL WI-FI / NETWORK HOSTING
echo ====================================================================
echo.
echo Detecting your Local IP Address...
for /f "tokens=2 delims=:" %%a in ('ipconfig ^| findstr /c:"IPv4 Address"') do (
    set LOCAL_IP=%%a
    goto :found_ip
)

:found_ip
set LOCAL_IP=%LOCAL_IP: =%
echo Your Computer's Network IP is: %LOCAL_IP%
echo.
echo [1/3] Starting Backend bound to 0.0.0.0:8000 ...
start "CivicShield Backend Network" cmd /k "cd backend && python -m uvicorn app.main:app --host 0.0.0.0 --port 8000"

timeout /t 3 /nobreak >nul

echo [2/3] Starting Frontend bound to 0.0.0.0:5173 ...
start "CivicShield Frontend Network" cmd /k "cd frontend && npx vite --host 0.0.0.0 --port 5173"

timeout /t 3 /nobreak >nul

echo [3/3] Opening Web App in Browser ...
start http://localhost:5173

echo.
echo ====================================================================
echo   CivicShield is now accessible to other devices on your Wi-Fi!
echo   
echo   Open this URL on your Mobile Phone or Faculty Laptop:
echo   --> http://%LOCAL_IP%:5173
echo ====================================================================
echo.
pause
