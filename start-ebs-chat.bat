@echo off
echo Starting Oracle EBS R12 Assistant...
echo.

cd /d "%~dp0"

echo Installing required packages...
pip install -r requirements-ebs.txt

echo.
echo Starting backend server...
python -m uvicorn backend.ebs_main:app --reload --host 0.0.0.0 --port 8000

pause