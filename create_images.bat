@echo off
title Create Default Images for App Store
color 06

echo ================================================================================
echo           CREATE DEFAULT PLACEHOLDER IMAGES
echo ================================================================================
echo.
echo This will create placeholder images for testing:
echo - Default app icon (512x512)
echo - Default banner (1024x500)
echo - Sample screenshots (720x1280)
echo - Sample preview photos (1080x1920)
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

echo [OK] Python detected
echo.

REM Run the image creation script
python create_default_images.py

echo.
pause
