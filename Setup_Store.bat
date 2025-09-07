@echo off
title 🔧 Store Setup & Installation
color 0D

echo ================================================================================
echo                    🔧 APP STORE SETUP & INSTALLATION 🔧
echo ================================================================================
echo.
echo This will set up your app store for first-time use.
echo.

:: Check Python installation
echo 🔍 Checking Python installation...
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python is not installed!
    echo.
    echo Please install Python from: https://www.python.org/downloads/
    echo Make sure to check "Add Python to PATH" during installation.
    echo.
    pause
    exit /b 1
) else (
    python --version
    echo ✅ Python is installed!
)

echo.
echo 📁 Creating required directories...

:: Create all required directories
mkdir static\images\app_icons 2>nul
mkdir static\images\app_banners 2>nul
mkdir static\images\screenshots 2>nul
mkdir Apps_Link 2>nul
mkdir backups 2>nul
mkdir analytics 2>nul
mkdir exports 2>nul
mkdir cache 2>nul
mkdir logs 2>nul
mkdir data 2>nul
mkdir templates 2>nul

echo ✅ Directories created!

echo.
echo 📄 Creating initial data files...

:: Create empty apps_data.json if it doesn't exist
if not exist apps_data.json (
    echo [] > apps_data.json
    echo ✅ Created apps_data.json
) else (
    echo ✅ apps_data.json already exists
)

echo.
echo 🎨 Creating default placeholder images...

:: Create placeholder text files for default images
echo This is a placeholder for default_icon.png > static\images\app_icons\default_icon.txt
echo This is a placeholder for default_banner.jpg > static\images\app_banners\default_banner.txt
echo ✅ Placeholder files created!

echo.
echo 🚀 Adding sample data...

:: Create a sample app entry
echo Do you want to add 5 sample apps to get started? (Y/N)
set /p add_samples=

if /i "%add_samples%"=="Y" (
    echo.
    echo Adding sample apps...
    python -c "import manage_apps_enhanced; manage_apps_enhanced.ensure_directories(); [manage_apps_enhanced.quick_add_sample() for _ in range(5)]" 2>nul
    if errorlevel 1 (
        echo ⚠️ Could not add sample apps automatically
    ) else (
        echo ✅ Sample apps added!
    )
)

echo.
echo ================================================================================
echo                      ✅ SETUP COMPLETED SUCCESSFULLY!
echo ================================================================================
echo.
echo Your app store is now ready to use!
echo.
echo 📋 Quick Start Guide:
echo    1. Double-click "Launch_Store_Manager.bat" to start the system
echo    2. Use option 1 to add new apps
echo    3. Use option 5 to view analytics
echo    4. Use option 19 for quick actions
echo.
echo 💡 Tips:
echo    • Run "Backup_Store_Data.bat" regularly to backup your data
echo    • Use "Launch_As_Admin.bat" if you need elevated privileges
echo    • Check the "backups" folder for automatic backups
echo.
echo Press any key to launch the store manager...
pause >nul

:: Launch the store manager
call Launch_Store_Manager.bat
