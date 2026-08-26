@echo off
title ProcessIQ - Enterprise AI Case Intelligence Platform Launcher
echo ======================================================
echo Starting ProcessIQ Enterprise Platform...
echo ======================================================

:: 1. Launch FastAPI Backend
echo [1/2] Launching Backend API Server (Port 8000)...
start "ProcessIQ Backend" cmd /k "call .\venv\Scripts\activate.bat && cd backend && python main.py"

:: 2. Wait 2 seconds for server initialization
timeout /t 2 /nobreak >nul

:: 3. Launch Vite Frontend
echo [2/2] Launching Frontend Dashboard (Port 5173)...
start "ProcessIQ Frontend" cmd /k "cd frontend && npm run dev"

:: 4. Open dashboard in default browser
timeout /t 3 /nobreak >nul
start http://localhost:5173

echo ======================================================
echo Application is running! Keep terminal windows open.
echo ======================================================