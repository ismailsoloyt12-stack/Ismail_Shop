@echo off
title Enhanced App Manager with Image Support
color 0D

echo ================================================================================
echo        ENHANCED APP STORE MANAGEMENT - WITH IMAGE SUPPORT
echo ================================================================================
echo.
echo This version includes full image management:
echo - Upload app icons
echo - Add banner images
echo - Manage screenshots and preview photos
echo - Organize all images in proper directories
echo.
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

REM Check if enhanced script exists
if not exist "manage_apps_enhanced.py" (
    echo [ERROR] manage_apps_enhanced.py not found!
    echo Please make sure the enhanced script is in this directory.
    echo.
    pause
    exit /b 1
)

echo [OK] Python detected
python --version
echo.

REM Create necessary directories
echo Creating image directories...
if not exist "static\images\app_icons" mkdir "static\images\app_icons"
if not exist "static\images\app_banners" mkdir "static\images\app_banners"
if not exist "static\images\screenshots" mkdir "static\images\screenshots"
if not exist "Apps_Link" mkdir "Apps_Link"

echo.
echo ================================================================================
echo Starting Enhanced App Management System...
echo ================================================================================
echo.

REM Run the enhanced management system
python manage_apps_enhanced.py

echo.
echo ================================================================================
echo App Management System closed.
echo.
pause
