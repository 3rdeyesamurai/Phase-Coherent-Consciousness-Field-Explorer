@echo off
REM Ionic Propulsion Lab Installer for Windows
echo.
echo ================================================
echo     🚀 IONIC PROPULSION LAB INSTALLER
echo ================================================
echo.

echo This will install the Ionic Propulsion Lab on your system.
echo.

REM Check if executable exists
if not exist "Ionic_Propulsion_Lab_windows.exe" (
    echo ❌ Executable not found. Please run build_executable.py first.
    pause
    exit /b 1
)

echo ✅ Found executable
echo.

REM Create desktop shortcut
echo 📌 Creating desktop shortcut...
set "DESKTOP=%USERPROFILE%\Desktop"
set "SHORTCUT=%DESKTOP%\Ionic Propulsion Lab.lnk"

powershell "$s=(New-Object -COM WScript.Shell).CreateShortcut('%SHORTCUT%');$s.TargetPath='%~dp0Ionic_Propulsion_Lab_windows.exe';$s.WorkingDirectory='%~dp0';$s.Save()"

if exist "%SHORTCUT%" (
    echo ✅ Desktop shortcut created
) else (
    echo ⚠️  Desktop shortcut creation failed
)

echo.
echo 🎉 Installation complete!
echo.
echo You can now:
echo • Double-click the desktop shortcut
echo • Run: Ionic_Propulsion_Lab_windows.exe
echo.
echo For help, see the documentation files.
echo.
pause
