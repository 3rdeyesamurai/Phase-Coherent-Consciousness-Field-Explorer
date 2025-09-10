#!/usr/bin/env python3
"""
Ionic Propulsion Lab Executable Builder
Creates standalone executables for Windows, macOS, and Linux

This script uses PyInstaller to create distributable executables
that include all dependencies and can run without Python installation.
"""

import os
import sys
import subprocess
import platform
import shutil
from pathlib import Path


def print_header():
    """Display build header"""
    print("""
            IONIC PROPULSION LAB EXECUTABLE BUILDER
              Standalone Application Creator
    """)


def check_pyinstaller():
    """Check if PyInstaller is installed"""
    print("[TOOL] Checking PyInstaller installation...")

    try:
        import PyInstaller  # noqa: F401
        print("[OK] PyInstaller found")
        return True
    except ImportError:
        print("[ERROR] PyInstaller not found")
        print("\n[INSTALL] Installing PyInstaller...")

        try:
            subprocess.check_call(
                [sys.executable, '-m', 'pip', 'install', 'pyinstaller'])
            print("[OK] PyInstaller installed successfully")
            return True
        except subprocess.CalledProcessError:
            print("[ERROR] Failed to install PyInstaller")
            print("   Please install manually: pip install pyinstaller")
            return False


def check_dependencies():
    """Check if all required packages are available"""
    print("\n[DEP] Checking application dependencies...")

    required_packages = [
        'numpy', 'pandas', 'matplotlib', 'tkinter', 'json', 'os', 'sys'
    ]

    missing_packages = []
    for package in required_packages:
        try:
            if package == 'tkinter':
                import tkinter  # noqa: F401
            else:
                __import__(package)
            print(f"[OK] {package} available")
        except ImportError:
            missing_packages.append(package)
            print(f"[ERROR] {package} missing")

    if missing_packages:
        print(
            f"\n[INSTALL] Installing missing packages: {
                ', '.join(missing_packages)}")
        try:
            subprocess.check_call(
                [sys.executable, '-m', 'pip', 'install'] + missing_packages)
            print("[OK] All packages installed")
            return True
        except subprocess.CalledProcessError:
            print("[ERROR] Failed to install packages")
            return False

    print("[OK] All dependencies available")
    return True


def create_spec_file():
    """Create PyInstaller spec file for better control"""
    # Get the current directory (should be ionic_propulsion_lab)
    current_dir = os.getcwd()

    spec_content = f'''
# -*- mode: python ; coding: utf-8 -*-

import os
import sys

block_cipher = None

# Add current directory to path
current_dir = r"{current_dir}"

a = Analysis(
    [os.path.join(current_dir, 'gui_app.py')],
    pathex=[current_dir],
    binaries=[],
    datas=[
        (os.path.join(current_dir, 'config.json'), '.'),
        (os.path.join(current_dir, 'README.md'), '.'),
        (os.path.join(current_dir, 'USER_GUIDE.md'), '.'),
        (os.path.join(current_dir, 'INSTALL_GUIDE.md'), '.'),
        (os.path.join(current_dir, 'ion_hall_parametric.py'), '.'),
    ],
    hiddenimports=[
        'numpy',
        'pandas',
        'matplotlib',
        'matplotlib.backends.backend_tkagg',
        'tkinter',
        'json',
        'os',
        'sys',
        'pathlib',
        'subprocess',
        'threading',
        'webbrowser',
        'socket',
        'urllib.request',
        'ion_hall_parametric',
        'numpy.core._methods',
        'numpy.lib.format',
    ],
    hookspath=[],
    hooksconfig={{}},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='Ionic_Propulsion_Lab',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=None,
)
'''

    with open('ionic_propulsion_lab.spec', 'w') as f:
        f.write(spec_content)

    print("[OK] Created PyInstaller spec file")
    return True


def build_executable():
    """Build the executable using PyInstaller"""
    print("\n[BUILD] Building executable...")

    system = platform.system().lower()
    spec_file = 'ionic_propulsion_lab.spec'

    # Build command - try multiple approaches
    cmd_options = [
        [sys.executable, '-m', 'pyinstaller', '--clean', '--noconfirm', spec_file],
        ['pyinstaller', '--clean', '--noconfirm', spec_file],
        ['python', '-m', 'pyinstaller', '--clean', '--noconfirm', spec_file],
    ]

    cmd = None
    for option in cmd_options:
        try:
            # Test if this command works
            result = subprocess.run(
                option + ['--help'],
                capture_output=True,
                text=True,
                timeout=5)
            if result.returncode == 0 or 'usage' in result.stdout.lower():
                cmd = option
                break
        except (subprocess.TimeoutExpired, FileNotFoundError, subprocess.CalledProcessError):
            continue

    if cmd is None:
        print("[ERROR] Could not find a working PyInstaller command")
        return False

    # Note: --onefile and --windowed options are specified in the .spec file
    # Don't add them here when using a spec file

    print(f"[CMD] Build command: {' '.join(cmd)}")

    try:
        result = subprocess.run(cmd, capture_output=True, text=True)

        if result.returncode == 0:
            print("[OK] Executable built successfully!")

            # Find the executable
            dist_dir = Path('dist')
            if dist_dir.exists():
                exe_files = list(dist_dir.glob('*'))
                if exe_files:
                    exe_path = exe_files[0]
                    print(f"[DIR] Executable location: {exe_path.absolute()}")

                    # Copy to root directory for easy access
                    final_name = f"Ionic_Propulsion_Lab_{system}.exe" if system == 'windows' else f"Ionic_Propulsion_Lab_{system}"
                    shutil.copy2(exe_path, final_name)
                    print(f"[COPY] Copied to: {Path(final_name).absolute()}")

            return True
        else:
            print("[ERROR] Build failed")
            print("STDOUT:", result.stdout)
            print("STDERR:", result.stderr)
            return False

    except Exception as e:
        print(f"[ERROR] Build error: {e}")
        return False


def create_installer_script():
    """Create a simple installer script"""
    system = platform.system().lower()

    if system == 'windows':
        installer_content = '''@echo off
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
set "DESKTOP=%USERPROFILE%\\Desktop"
set "SHORTCUT=%DESKTOP%\\Ionic Propulsion Lab.lnk"

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
'''
    else:
        installer_content = '''#!/bin/bash
# Ionic Propulsion Lab Installer for Linux/macOS

echo "================================================"
echo "    🚀 IONIC PROPULSION LAB INSTALLER"
echo "================================================"
echo

# Check executable
if [[ "$OSTYPE" == "darwin"* ]]; then
    EXE_NAME="Ionic_Propulsion_Lab_darwin"
else
    EXE_NAME="Ionic_Propulsion_Lab_linux"
fi

if [ ! -f "$EXE_NAME" ]; then
    echo "❌ Executable not found. Please run build_executable.py first."
    exit 1
fi

echo "✅ Found executable"
echo

# Create desktop shortcut (Linux)
if [[ "$OSTYPE" != "darwin"* ]]; then
    echo "📌 Creating desktop shortcut..."
    DESKTOP_DIR="$HOME/Desktop"
    SHORTCUT="$DESKTOP_DIR/Ionic Propulsion Lab.desktop"

    cat > "$SHORTCUT" << EOF
[Desktop Entry]
Version=1.0
Type=Application
Name=Ionic Propulsion Lab
Comment=Enhanced Electric Propulsion Analysis Tool
Exec=$(pwd)/$EXE_NAME
Icon=$(pwd)/icon.png
Path=$(pwd)
Terminal=false
StartupNotify=false
EOF

    chmod +x "$SHORTCUT"

    if [ -f "$SHORTCUT" ]; then
        echo "✅ Desktop shortcut created"
    else
        echo "⚠️  Desktop shortcut creation failed"
    fi
fi

echo
echo "🎉 Installation complete!"

echo
echo "You can now run:"
echo "  ./$EXE_NAME"
echo
echo "For help, see the documentation files."
'''

    installer_name = 'install_lab.bat' if system == 'windows' else 'install_lab.sh'

    # Handle encoding for Windows
    try:
        with open(installer_name, 'w', encoding='utf-8') as f:
            f.write(installer_content)
    except UnicodeEncodeError:
        # Fallback: remove emoji characters for Windows compatibility
        clean_content = installer_content.replace('🚀', 'IONIC PROPULSION LAB')
        clean_content = clean_content.replace('✅', '[OK]')
        clean_content = clean_content.replace('❌', '[ERROR]')
        clean_content = clean_content.replace('📁', '[DIR]')
        clean_content = clean_content.replace('⚙️', '[CONFIG]')
        clean_content = clean_content.replace('🎉', '[SUCCESS]')

        with open(installer_name, 'w') as f:
            f.write(clean_content)

    if system != 'windows':
        os.chmod(installer_name, 0o755)

    print(f"✅ Created installer script: {installer_name}")
    return True


def cleanup_build_files():
    """Clean up temporary build files"""
    print("\n🧹 Cleaning up build files...")

    cleanup_items = [
        'build',
        'ionic_propulsion_lab.spec',
        '__pycache__',
        '*.spec'
    ]

    for item in cleanup_items:
        if os.path.exists(item):
            if os.path.isdir(item):
                shutil.rmtree(item)
            else:
                os.remove(item)
            print(f"🗑️  Removed: {item}")

    print("✅ Cleanup complete")


def show_usage():
    """Show usage instructions"""
    system = platform.system().lower()

    print(f"""
╔══════════════════════════════════════════════════════════════╗
║                    🎯 BUILD COMPLETE!                          ║
╚══════════════════════════════════════════════════════════════╝

EXECUTABLE CREATED:
   • File: Ionic_Propulsion_Lab_{system}.exe (Windows) or executable (Linux/macOS)
   • Location: Current directory
   • Size: Check file properties

HOW TO USE:
   1. Double-click the executable file
   2. Or run from command line: ./Ionic_Propulsion_Lab_{system}

WHAT IT INCLUDES:
   ✅ Complete GUI application
   ✅ All physics calculations
   ✅ Interactive plots
   ✅ Documentation files
   ✅ Configuration files
   ✅ Web interface components

SYSTEM REQUIREMENTS:
   • No Python installation needed
   • Works on clean Windows/Linux/macOS systems
   • All dependencies included

FOR DISTRIBUTION:
   • Zip the executable with all files
   • Users can run immediately
   • No installation required

TROUBLESHOOTING:
   • If executable doesn't start: Check antivirus software
   • If GUI doesn't appear: Try running from command line
   • For errors: Check the console output

For detailed help, see the documentation files included with the executable.
    """)


def main():
    """Main build function"""
    print_header()

    print("This will create a standalone executable for the Ionic Propulsion Lab.")
    print("The executable will include all dependencies and can run on any compatible system.\n")

    # Check PyInstaller
    if not check_pyinstaller():
        print("\n❌ Cannot proceed without PyInstaller")
        input("Press Enter to exit...")
        return

    # Check dependencies
    if not check_dependencies():
        print("\n❌ Cannot proceed without required packages")
        input("Press Enter to exit...")
        return

    # Create spec file
    if not create_spec_file():
        print("\n❌ Failed to create spec file")
        input("Press Enter to exit...")
        return

    # Build executable
    if not build_executable():
        print("\n❌ Build failed")
        input("Press Enter to exit...")
        return

    # Create installer
    create_installer_script()

    # Cleanup
    cleanup_build_files()

    # Show results
    show_usage()

    input("\nPress Enter to exit...")


if __name__ == "__main__":
    main()
