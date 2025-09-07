@echo off
title 🔗 Create Desktop Shortcut
color 09

echo ================================================================================
echo                      🔗 CREATE DESKTOP SHORTCUT 🔗
echo ================================================================================
echo.
echo This will create a shortcut on your desktop for easy access.
echo.

:: Create VBS script to create shortcut
echo Creating shortcut...

(
echo Set oWS = WScript.CreateObject("WScript.Shell"^)
echo sLinkFile = oWS.SpecialFolders("Desktop"^) ^& "\App Store Manager.lnk"
echo Set oLink = oWS.CreateShortcut(sLinkFile^)
echo oLink.TargetPath = "F:\ismail_SHOP3\Launch_Store_Manager.bat"
echo oLink.WorkingDirectory = "F:\ismail_SHOP3"
echo oLink.IconLocation = "%SystemRoot%\System32\shell32.dll, 13"
echo oLink.Description = "Ultra-Enhanced App Store Management System"
echo oLink.WindowStyle = 1
echo oLink.Save
) > "%temp%\CreateShortcut.vbs"

:: Run the VBS script
cscript //nologo "%temp%\CreateShortcut.vbs"

:: Clean up
del "%temp%\CreateShortcut.vbs"

echo.
echo ✅ Desktop shortcut created successfully!
echo.
echo You can now launch the App Store Manager from your desktop!
echo.
pause
