@echo off
echo Starting Oracle EBS Assistant (Simple Mode)...
echo.

cd /d "%~dp0"
python -m uvicorn backend.simple_main:app --reload --host 0.0.0.0 --port 8000

pause