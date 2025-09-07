@echo off
title 💾 Store Data Backup Utility
color 0B

echo ================================================================================
echo                        💾 STORE DATA BACKUP UTILITY 💾
echo ================================================================================
echo.
echo This utility will backup all your store data including:
echo   • App database (apps_data.json)
echo   • Customer databases
echo   • Analytics data
echo   • Images and media files
echo.

:: Create backup folder with timestamp
set datetime=%date:~-4%%date:~3,2%%date:~0,2%_%time:~0,2%%time:~3,2%%time:~6,2%
set datetime=%datetime: =0%
set backup_folder=Backup_%datetime%

echo Creating backup folder: %backup_folder%
mkdir "backups\%backup_folder%" 2>nul

echo.
echo 📂 Backing up data files...

:: Backup JSON data
if exist apps_data.json (
    copy apps_data.json "backups\%backup_folder%\apps_data.json" >nul
    echo ✅ Apps database backed up
) else (
    echo ⚠️ Apps database not found
)

:: Backup data directory
if exist data (
    echo 📊 Backing up databases...
    xcopy /E /I /Q data "backups\%backup_folder%\data" >nul
    echo ✅ Databases backed up
)

:: Backup images
if exist static\images (
    echo 🖼️ Backing up images...
    xcopy /E /I /Q static\images "backups\%backup_folder%\images" >nul
    echo ✅ Images backed up
)

:: Backup app files
if exist Apps_Link (
    echo 📦 Backing up app files...
    xcopy /E /I /Q Apps_Link "backups\%backup_folder%\Apps_Link" >nul
    echo ✅ App files backed up
)

echo.
echo ================================================================================
echo                     ✅ BACKUP COMPLETED SUCCESSFULLY!
echo                   Location: backups\%backup_folder%
echo ================================================================================
echo.
echo Press any key to exit...
pause >nul
