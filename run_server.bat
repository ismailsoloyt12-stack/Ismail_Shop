@echo off
echo ===================================
echo  Game ^& App Store - Starting Server
echo ===================================
echo.
echo Checking Python installation...
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.7+ from python.org
    pause
    exit /b 1
)

echo Installing required packages...
pip install -r requirements.txt

echo.
echo ===================================
echo Starting the App Store server...
echo ===================================
echo.
echo Server will run at: http://localhost:5000
echo Press Ctrl+C to stop the server
echo.
echo To add apps to your store:
echo 1. Run manage_apps.py in another terminal
echo 2. Or edit apps_data.json directly
echo.
python app.py
pause
