@echo off
title 🎮 Ultra-Enhanced App Store Manager 🎮
color 0A

echo ================================================================================
echo                    🚀 ULTRA-ENHANCED APP STORE MANAGER 🚀
echo                           Welcome to Your Store System!
echo ================================================================================
echo.
echo Starting the enhanced app store management system...
echo.
echo 📱 Initializing databases...
echo ☁️ Starting cloud sync...
echo 🤖 Loading AI systems...
echo.

:: Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ ERROR: Python is not installed or not in PATH!
    echo Please install Python from https://www.python.org/
    echo.
    pause
    exit /b 1
)

echo ✅ Python detected!
echo.
echo ================================================================================
echo                         🎯 LAUNCHING APP STORE MANAGER
echo ================================================================================
echo.

:: Run the enhanced app management system
python manage_apps_enhanced.py

:: If there's an error, keep the window open
if errorlevel 1 (
    echo.
    echo ❌ An error occurred while running the app store manager.
    echo Please check the error message above.
    echo.
    pause
)

:: Keep window open after normal exit
echo.
echo ================================================================================
echo                    👋 Thank you for using the App Store Manager!
echo                          Press any key to close this window
echo ================================================================================
pause >nul
