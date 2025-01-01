@echo off
title PyInstaller Packager
color 0A

where pyinstaller > nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo PyInstaller is not installed or not found in your PATH.
    echo Please install PyInstaller by running 'pip install pyinstaller'.
    pause
    exit /b
)

echo Current working directory: %cd%

:main
cls
echo ===========================================
echo          PyInstaller Packager
echo ===========================================
echo.
echo 1. Package with console (Default)
echo 2. Package without console (No Console)
echo 3. Exit
echo.
echo ===========================================
set /p choice="Choose an option (1-3): "

if "%choice%"=="1" goto withConsole
if "%choice%"=="2" goto noConsole
if "%choice%"=="3" goto exit
echo Invalid choice! Please try again.
pause
goto main

:withConsole
cls
echo ===========================================
echo Packaging with console...
set /p script="Enter the path to your Python script (e.g., launcher.py): "
if "%script%"=="" (
    set script=launcher.py
)
echo Using script: %script%

:: Check if the Python script exists
if not exist "%script%" (
    echo Error: The script "%script%" does not exist.
    pause
    goto main
)

start cmd.exe /k pyinstaller --onefile "%script%"
echo PyInstaller has been launched in a separate Command Prompt.
pause
goto main

:noConsole
cls
echo ===========================================
echo Packaging without console (windowed mode)...
set /p script="Enter the path to your Python script (e.g., launcher.py): "
if "%script%"=="" (
    set script=launcher.py
)
echo Using script: %script%

:: Check if the Python script exists
if not exist "%script%" (
    echo Error: The script "%script%" does not exist.
    pause
    goto main
)

start cmd.exe /k pyinstaller --onefile --noconsole "%script%"
echo PyInstaller has been launched in a separate Command Prompt.
pause
goto main

:exit
cls
echo Thanks for using PyInstaller Packager!
timeout /t 3 > nul
exit
