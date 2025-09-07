@echo off
title App Store Web Server
color 02

echo ================================================================================
echo                      STARTING APP STORE WEB SERVER
echo ================================================================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Python is not installed or not in PATH!
    echo Please install Python from https://www.python.org/
    echo.
    pause
    exit /b 1
)

REM Check if app.py exists
if not exist "app.py" (
    echo [ERROR] app.py not found in current directory!
    echo Please make sure you're in the correct folder.
    echo.
    pause
    exit /b 1
)

echo [INFO] Python detected successfully
echo.
echo Starting Flask server...
echo ================================================================================
echo.
echo Server will run at: http://localhost:5000
echo.
echo Press Ctrl+C to stop the server
echo.
echo ================================================================================
echo.

REM Run the Flask app
python app.py

echo.
echo ================================================================================
echo Server stopped.
pause
