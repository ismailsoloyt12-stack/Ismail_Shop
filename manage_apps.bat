@echo off
title App Store Management System
color 0A

echo ========================================
echo    GAME ^& APP STORE MANAGEMENT
echo ========================================
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

REM Display Python version
echo Detected Python version:
python --version
echo.

REM Check if manage_apps_enhanced.py exists
if not exist "manage_apps.py" (
    echo [ERROR] manage_apps_enhanced.py not found in current directory!
    echo Please make sure you're running this from the correct folder.
    echo.
    pause
    exit /b 1
)

REM Run the management system
echo Starting App Management System...
echo ========================================
python manage_apps_enhanced.py

REM Keep window open after script finishes
echo.
echo ========================================
echo App Management System closed.
echo.
pause
