# Oracle EBS R12 i-Supplier Assistant - Startup Script (Windows PowerShell)

Write-Host "🚀 Oracle EBS R12 i-Supplier Assistant - Tanger Med"
Write-Host "=================================================="

# Check if Python is installed
if (-not (Get-Command python -ErrorAction SilentlyContinue)) {
    Write-Error "❌ Python is required but not installed."
    exit 1
}

# Check if pip is installed
if (-not (Get-Command pip -ErrorAction SilentlyContinue)) {
    Write-Error "❌ pip is required but not installed."
    exit 1
}

# Install dependencies if requirements.txt exists
if (Test-Path "requirements.txt") {
    Write-Host "📦 Installing Python dependencies..."
    pip install -r requirements.txt
    if ($LASTEXITCODE -ne 0) {
        Write-Error "❌ Failed to install dependencies"
        exit 1
    }
}

# Create logs directory if it doesn't exist
if (-not (Test-Path "logs")) {
    New-Item -ItemType Directory -Path "logs" | Out-Null
}

Write-Host "🔧 Starting services..."

# Start backend server
Write-Host "🖥️  Starting backend server on port 8000..."
$backend = Start-Process -FilePath "python" -ArgumentList "run.py" -RedirectStandardOutput "logs\backend.log" -RedirectStandardError "logs\backend.log" -NoNewWindow -PassThru

Start-Sleep -Seconds 3

if ($backend.HasExited) {
    Write-Error "❌ Backend server failed to start. Check logs/backend.log"
    exit 1
}

# Start frontend server
Write-Host "🌐 Starting frontend server on port 3000..."
Push-Location "frontend"

if (Get-Command npx -ErrorAction SilentlyContinue) {
    Write-Host "   Using Node.js serve..."
    $frontend = Start-Process -FilePath "npx" -ArgumentList "serve", "-s", ".", "-p", "3000" -RedirectStandardOutput "..\logs\frontend.log" -RedirectStandardError "..\logs\frontend.log" -NoNewWindow -PassThru
} else {
    Write-Host "   Using Python HTTP server..."
    $frontend = Start-Process -FilePath "python" -ArgumentList "-m", "http.server", "3000" -RedirectStandardOutput "..\logs\frontend.log" -RedirectStandardError "..\logs\frontend.log" -NoNewWindow -PassThru
}

Pop-Location
Start-Sleep -Seconds 2

if ($frontend.HasExited) {
    Write-Error "❌ Frontend server failed to start. Check logs/frontend.log"
    $backend.Kill()
    exit 1
}

Write-Host "✅ Services started successfully!"
Write-Host ""
Write-Host "🔗 Access the application:"
Write-Host "   Frontend: http://localhost:3000"
Write-Host "   Backend API: http://localhost:8000"
Write-Host "   API Docs: http://localhost:8000/docs"
Write-Host ""
Write-Host "📝 Logs are available in the logs/ directory"
Write-Host "Press Ctrl+C to stop all services"
Write-Host ""

# Wait for both processes to run
Wait-Process -Id $backend.Id, $frontend.Id