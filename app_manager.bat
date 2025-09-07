@echo off
setlocal enabledelayedexpansion
title App Store Manager - Advanced Menu
color 0B

:MENU
cls
echo ================================================================================
echo                         APP STORE MANAGEMENT SYSTEM
echo ================================================================================
echo.
echo   [1] Run App Manager (Add/Edit/Remove Apps)
echo   [2] Start Web Server (Run the App Store)
echo   [3] Backup App Data
echo   [4] View Apps_Link Folder
echo   [5] Open Apps Data in Notepad
echo   [6] Check Python Installation
echo   [7] Install Requirements (if needed)
echo   [8] Exit
echo.
echo ================================================================================
set /p choice="Enter your choice (1-8): "

if "%choice%"=="1" goto RUN_MANAGER
if "%choice%"=="2" goto RUN_SERVER
if "%choice%"=="3" goto BACKUP_DATA
if "%choice%"=="4" goto VIEW_APPS_FOLDER
if "%choice%"=="5" goto OPEN_DATA
if "%choice%"=="6" goto CHECK_PYTHON
if "%choice%"=="7" goto INSTALL_REQUIREMENTS
if "%choice%"=="8" goto EXIT

echo Invalid choice! Please select 1-8.
pause
goto MENU

:RUN_MANAGER
cls
echo ================================================================================
echo                         STARTING APP MANAGEMENT SYSTEM
echo ================================================================================
echo.
if not exist "manage_apps.py" (
    echo [ERROR] manage_apps.py not found!
    pause
    goto MENU
)
python manage_apps.py
echo.
echo Press any key to return to menu...
pause >nul
goto MENU

:RUN_SERVER
cls
echo ================================================================================
echo                         STARTING WEB SERVER
echo ================================================================================
echo.
if exist "app.py" (
    echo Starting Flask server...
    echo Press Ctrl+C to stop the server
    echo.
    python app.py
) else (
    echo [ERROR] app.py not found!
)
echo.
pause
goto MENU

:BACKUP_DATA
cls
echo ================================================================================
echo                         BACKING UP APP DATA
echo ================================================================================
echo.

REM Create backup folder with timestamp
for /f "tokens=2 delims==" %%a in ('wmic OS Get localdatetime /value') do set "dt=%%a"
set "YY=%dt:~2,2%"
set "YYYY=%dt:~0,4%"
set "MM=%dt:~4,2%"
set "DD=%dt:~6,2%"
set "HH=%dt:~8,2%"
set "Min=%dt:~10,2%"
set "Sec=%dt:~12,2%"
set "backup_name=backup_%YYYY%%MM%%DD%_%HH%%Min%%Sec%"

if not exist "backups" mkdir backups

echo Creating backup: %backup_name%
echo.

if exist "apps_data.json" (
    copy "apps_data.json" "backups\%backup_name%_apps_data.json" >nul
    echo [OK] Backed up apps_data.json
) else (
    echo [WARNING] apps_data.json not found
)

if exist "users.json" (
    copy "users.json" "backups\%backup_name%_users.json" >nul
    echo [OK] Backed up users.json
) else (
    echo [WARNING] users.json not found
)

echo.
echo Backup completed successfully!
echo Location: backups\%backup_name%_*.json
echo.
pause
goto MENU

:VIEW_APPS_FOLDER
cls
echo ================================================================================
echo                         APPS_LINK FOLDER CONTENTS
echo ================================================================================
echo.

if not exist "Apps_Link" (
    echo Creating Apps_Link folder...
    mkdir Apps_Link
)

echo Opening Apps_Link folder in Explorer...
start "" "Apps_Link"

echo.
echo Contents of Apps_Link folder:
echo ------------------------------
dir /b "Apps_Link" 2>nul || echo (Folder is empty)
echo.
pause
goto MENU

:OPEN_DATA
cls
echo ================================================================================
echo                         OPENING APP DATA FILE
echo ================================================================================
echo.

if exist "apps_data.json" (
    echo Opening apps_data.json in Notepad...
    start notepad "apps_data.json"
) else (
    echo [ERROR] apps_data.json not found!
    echo Run the App Manager first to create the data file.
)
echo.
pause
goto MENU

:CHECK_PYTHON
cls
echo ================================================================================
echo                         PYTHON INSTALLATION CHECK
echo ================================================================================
echo.

python --version >nul 2>&1
if %errorlevel% equ 0 (
    echo [OK] Python is installed:
    python --version
    echo.
    echo Python location:
    where python
    echo.
    echo Checking installed packages:
    echo ----------------------------
    python -m pip list 2>nul || echo pip not found
) else (
    echo [ERROR] Python is not installed or not in PATH!
    echo.
    echo Please install Python from: https://www.python.org/
    echo Make sure to check "Add Python to PATH" during installation.
)
echo.
pause
goto MENU

:INSTALL_REQUIREMENTS
cls
echo ================================================================================
echo                         INSTALLING REQUIREMENTS
echo ================================================================================
echo.

if exist "requirements.txt" (
    echo Installing packages from requirements.txt...
    python -m pip install -r requirements.txt
) else (
    echo No requirements.txt found. Installing common packages...
    echo.
    echo Installing Flask...
    python -m pip install flask
    echo.
    echo Installing Flask-Login...
    python -m pip install flask-login
    echo.
    echo Creating requirements.txt...
    echo flask>requirements.txt
    echo flask-login>>requirements.txt
)

echo.
echo Installation complete!
echo.
pause
goto MENU

:EXIT
cls
echo ================================================================================
echo.
echo    Thank you for using App Store Management System!
echo.
echo ================================================================================
timeout /t 2 >nul
exit
