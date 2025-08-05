#!/bin/bash

# Oracle EBS R12 i-Supplier Assistant Startup Script

echo "🚀 Oracle EBS R12 i-Supplier Assistant - Tanger Med"
echo "=================================================="

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is required but not installed."
    exit 1
fi

# Check if pip is installed
if ! command -v pip3 &> /dev/null; then
    echo "❌ pip3 is required but not installed."
    exit 1
fi

# Install dependencies if requirements.txt exists
if [ -f "requirements.txt" ]; then
    echo "📦 Installing Python dependencies..."
    pip3 install -r requirements.txt
    if [ $? -ne 0 ]; then
        echo "❌ Failed to install dependencies"
        exit 1
    fi
fi

# Create log directory
mkdir -p logs

echo "🔧 Starting services..."

# Function to cleanup background processes
cleanup() {
    echo "🛑 Shutting down services..."
    kill $BACKEND_PID 2>/dev/null
    kill $FRONTEND_PID 2>/dev/null
    exit 0
}

# Set trap to cleanup on script exit
trap cleanup SIGINT SIGTERM

# Start backend server
echo "🖥️  Starting backend server on port 8000..."
python3 run.py > logs/backend.log 2>&1 &
BACKEND_PID=$!

# Wait a moment for backend to start
sleep 3

# Check if backend started successfully
if ! kill -0 $BACKEND_PID 2>/dev/null; then
    echo "❌ Backend server failed to start. Check logs/backend.log"
    exit 1
fi

# Start frontend server
echo "🌐 Starting frontend server on port 3000..."
cd frontend

# Try to use Node.js serve if available, otherwise use Python
if command -v npx &> /dev/null; then
    echo "   Using Node.js serve..."
    npx serve -s . -p 3000 > ../logs/frontend.log 2>&1 &
    FRONTEND_PID=$!
else
    echo "   Using Python HTTP server..."
    python3 -m http.server 3000 > ../logs/frontend.log 2>&1 &
    FRONTEND_PID=$!
fi

cd ..

# Wait a moment for frontend to start
sleep 2

# Check if frontend started successfully
if ! kill -0 $FRONTEND_PID 2>/dev/null; then
    echo "❌ Frontend server failed to start. Check logs/frontend.log"
    kill $BACKEND_PID 2>/dev/null
    exit 1
fi

echo "✅ Services started successfully!"
echo ""
echo "🔗 Access the application:"
echo "   Frontend: http://localhost:3000"
echo "   Backend API: http://localhost:8000"
echo "   API Docs: http://localhost:8000/docs"
echo ""
echo "📝 Logs are available in the logs/ directory"
echo "Press Ctrl+C to stop all services"
echo ""

# Wait for user to stop the services
wait