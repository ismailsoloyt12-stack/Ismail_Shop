@echo off
title 🔐 App Store Manager (Administrator Mode)
color 0E

echo ================================================================================
echo                  🔐 LAUNCHING WITH ADMINISTRATOR PRIVILEGES 🔐
echo ================================================================================
echo.

:: Check for admin rights
net session >nul 2>&1
if %errorLevel% == 0 (
    echo ✅ Running with Administrator privileges
    echo.
    cd /d "F:\ismail_SHOP3"
    python manage_apps_enhanced.py
) else (
    echo ⚠️ Requesting Administrator privileges...
    echo.
    echo You may see a UAC prompt. Please click "Yes" to continue.
    echo.
    
    :: Create a temporary VBS script to elevate privileges
    echo Set UAC = CreateObject^("Shell.Application"^) > "%temp%\getadmin.vbs"
    echo UAC.ShellExecute "cmd.exe", "/c cd /d ""F:\ismail_SHOP3"" && python manage_apps_enhanced.py && pause", "", "runas", 1 >> "%temp%\getadmin.vbs"
    
    "%temp%\getadmin.vbs"
    del "%temp%\getadmin.vbs"
    exit /b
)

pause
