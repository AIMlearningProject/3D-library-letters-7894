@echo off
echo ========================================
echo  NamePlate Studio Pro - Launcher
echo ========================================
echo.

REM Check if Python is available
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python from python.org
    pause
    exit /b 1
)

echo Starting NamePlate Studio Pro...
echo.

python launch_gui.py

if errorlevel 1 (
    echo.
    echo ========================================
    echo  Application exited with errors
    echo ========================================
    pause
)
