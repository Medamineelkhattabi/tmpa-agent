@echo off
echo 🚀 Starting Oracle EBS Assistant with Visual Guides...

echo 📦 Installing dependencies...
python install_pillow.py

echo 🎯 Generating visual guides...
python generate_visual_guides.py

echo 🔧 Starting backend server...
start "Backend Server" cmd /k "python -m uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000"

timeout /t 3 /nobreak > nul

echo 🌐 Starting frontend server...
start "Frontend Server" cmd /k "cd frontend && python -m http.server 3000"

echo ✅ Oracle EBS Assistant started successfully!
echo 🔗 Frontend: http://localhost:3000
echo 🔗 Backend API: http://localhost:8000
echo 📸 Visual guides available for all procedures

pause