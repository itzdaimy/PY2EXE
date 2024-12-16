@echo off
title PyInstaller Installer
color 0A

:: Check if pip is installed
where pip > nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo Pip is not installed or not found in your PATH.
    echo Please install Python and ensure pip is added to your PATH.
    pause
    exit /b
)

:: Install PyInstaller
echo Installing PyInstaller...
pip install pyinstaller

:: Check if PyInstaller was successfully installed
if %ERRORLEVEL% EQU 0 (
    echo PyInstaller installed successfully!
) else (
    echo An error occurred while installing PyInstaller.
)

pause
exit
