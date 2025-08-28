@echo off
echo ========================================
echo Oracle EBS Assistant - Original Version
echo ========================================

echo Starting backend...
cd backend
start "Backend" cmd /k "python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000"

timeout /t 3 /nobreak > nul

echo Starting frontend...
cd ..\frontend
start "Frontend" cmd /k "python -m http.server 3000"

echo.
echo ========================================
echo Original version restored!
echo Frontend: http://localhost:3000
echo Backend: http://localhost:8000
echo ========================================
pause