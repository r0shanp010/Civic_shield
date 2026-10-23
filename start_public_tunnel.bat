@echo off
title CivicShield Public Internet Tunnel Generator
color 0E

echo ====================================================================
echo      CIVICSHIELD - INSTANT PUBLIC INTERNET TUNNEL GENERATOR
echo ====================================================================
echo.
echo This script exposes your local CivicShield app to the public internet
echo with a live HTTPS link for your faculty review / presentation.
echo.

echo [1/3] Ensuring backend is running on port 8000...
start "CivicShield Backend" cmd /k "cd backend && python -m uvicorn app.main:app --host 127.0.0.1 --port 8000"

timeout /t 3 /nobreak >nul

echo [2/3] Ensuring frontend is running on port 5173...
start "CivicShield Frontend" cmd /k "cd frontend && npm run dev"

timeout /t 3 /nobreak >nul

echo [3/3] Generating live public HTTPS tunnel...
echo.
echo Starting Localtunnel on port 5173...
npx localtunnel --port 5173
