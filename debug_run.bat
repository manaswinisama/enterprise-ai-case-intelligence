@echo off
title ProcessIQ Debug Launcher
echo Testing Backend startup...
cd /d "%~dp0backend"
call "..\venv\Scripts\activate.bat"
python -m uvicorn main:app --reload --port 8000
pause