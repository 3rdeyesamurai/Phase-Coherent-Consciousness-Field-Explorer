@echo off
REM Ionic Propulsion Lab Launcher for Windows
REM This batch file provides an easy way to run the ionic propulsion lab

echo.
echo ================================================
echo         🚀 IONIC PROPULSION LAB
echo     Enhanced Electric Propulsion Analysis
echo ================================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python is not installed or not in PATH
    echo.
    echo 📥 Please install Python from: https://python.org
    echo    Make sure to check "Add Python to PATH" during installation
    echo.
    pause
    exit /b 1
)

REM Check if we're in the right directory
if not exist "config.json" (
    echo ❌ Error: Please run this script from the ionic_propulsion_lab directory
    echo.
    echo Current directory: %CD%
    echo.
    echo Expected: C:\path\to\ionic_propulsion_lab
    echo.
    pause
    exit /b 1
)

echo ✅ Python found
echo ✅ Correct directory detected
echo.

REM Run the launcher
python launcher.py

echo.
echo ================================================
echo         Session Complete
echo ================================================
echo.
echo Your results are saved in the output\ folder
echo.
pause
