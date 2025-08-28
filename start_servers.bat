@echo off
echo Starting Oracle EBS R12 i-Supplier Assistant for Tanger Med
echo ============================================================

echo.
echo Starting Backend Server (Port 8000)...
start "Backend Server" cmd /k "cd /d %~dp0backend && python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000"

timeout /t 3 /nobreak >nul

echo.
echo Starting Frontend Server (Port 3000)...
start "Frontend Server" cmd /k "cd /d %~dp0frontend && python -m http.server 3000"

timeout /t 2 /nobreak >nul

echo.
echo ============================================================
echo Servers are starting up...
echo.
echo Backend API: http://localhost:8000
echo Frontend UI: http://localhost:3000
echo.
echo Features:
echo - Realistic Oracle EBS R12 interface mockups
echo - Bilingual support (French/English)
echo - Interactive visual guides with annotations
echo - Step-by-step procedure guidance
echo - Authentic Oracle styling and branding
echo.
echo Press any key to open the application in your browser...
pause >nul

start http://localhost:3000

echo.
echo Application opened in browser!
echo Both servers are running in separate windows.
echo Close those windows to stop the servers.
pause