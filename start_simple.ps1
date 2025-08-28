#!/usr/bin/env pwsh

Write-Host "Starting Oracle EBS Assistant (Simple Mode)..." -ForegroundColor Green
Write-Host ""

# Change to script directory
Set-Location $PSScriptRoot

# Check if Python is available
try {
    $pythonVersion = python --version 2>&1
    Write-Host "Python version: $pythonVersion" -ForegroundColor Cyan
} catch {
    Write-Host "Error: Python not found. Please install Python 3.8+ and add it to PATH." -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}

# Check if virtual environment is activated
if ($env:VIRTUAL_ENV) {
    Write-Host "Virtual environment: $env:VIRTUAL_ENV" -ForegroundColor Cyan
} else {
    Write-Host "Warning: No virtual environment detected. Consider using a virtual environment." -ForegroundColor Yellow
}

# Start the server
Write-Host "Starting FastAPI server on http://localhost:8000" -ForegroundColor Green
Write-Host "Press Ctrl+C to stop the server" -ForegroundColor Yellow
Write-Host ""

try {
    python -m uvicorn backend.simple_main:app --reload --host 0.0.0.0 --port 8000
} catch {
    Write-Host "Error starting server: $_" -ForegroundColor Red
    Write-Host ""
    Write-Host "Troubleshooting steps:" -ForegroundColor Yellow
    Write-Host "1. Make sure you're in the correct directory" -ForegroundColor White
    Write-Host "2. Install dependencies: pip install -r requirements.txt" -ForegroundColor White
    Write-Host "3. Check if port 8000 is available" -ForegroundColor White
    Read-Host "Press Enter to exit"
}