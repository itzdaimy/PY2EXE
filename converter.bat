@echo off
title Py2Exe v2
color 0A

:: Check if PyInstaller is installed
where pyinstaller > nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo ====================================================
    echo  PyInstaller is not installed or found in your PATH.
    echo  Please install PyInstaller by running:
    echo      pip install pyinstaller
    echo ====================================================
    pause
    exit /b
)

:mainMenu
cls
echo ================================================
echo                  Py2Exe v2

echo ================================================
echo   Package your Python scripts into executables
echo   Current working directory: %cd%
echo ================================================
echo 1. Package with console (Default)
echo 2. Package without console (No Console)
echo 3. Help
echo 4. Exit
echo ================================================
set /p choice="Choose an option (1-4): "

if "%choice%"=="1" goto packageWithConsole
if "%choice%"=="2" goto packageNoConsole
if "%choice%"=="3" goto help
if "%choice%"=="4" goto exit
echo Invalid choice! Please enter a valid option.
pause
goto mainMenu

:packageWithConsole
cls
echo ================================================
echo       Packaging with console (Default)
echo ================================================
set /p script="Enter the path to your Python script (default: launcher.py): "
if "%script%"=="" (
    set script=launcher.py
)
if not exist "%script%" (
    echo Error: The script "%script%" does not exist.
    pause
    goto mainMenu
)
echo Packaging "%script%" with console...
pyinstaller --onefile "%script%"
echo Process completed. Check the 'dist' folder for your executable.
pause
goto mainMenu

:packageNoConsole
cls
echo ================================================
echo  Packaging without console (Windowed Mode)
echo ================================================
set /p script="Enter the path to your Python script (default: launcher.py): "
if "%script%"=="" (
    set script=launcher.py
)
if not exist "%script%" (
    echo Error: The script "%script%" does not exist.
    pause
    goto mainMenu
)
echo Packaging "%script%" without console...
pyinstaller --onefile --noconsole "%script%"
echo Process completed. Check the 'dist' folder for your executable.
pause
goto mainMenu

:help
cls
echo ================================================
echo                    Help
echo ================================================
echo  This script packages Python scripts into executables
echo  using PyInstaller. You can choose between:
echo     - Console Mode: Includes a terminal for output.
echo     - No Console: Creates a windowed application.
echo ================================================
echo  Notes:
echo  - Ensure PyInstaller is installed via 'pip install pyinstaller'.
echo  - Your packaged executable will appear in the 'dist' folder.
echo ================================================
pause
goto mainMenu

:exit
cls
echo ================================================
echo          Thanks for using Py2Exe v2!
echo ================================================
timeout /t 3 > nul
exit
