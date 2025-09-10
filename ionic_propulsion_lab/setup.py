#!/usr/bin/env python3
"""
Ionic Propulsion Lab Setup Script
Automated installation and setup for the Enhanced Ionic Propulsion Analysis Tool
"""

import os
import sys
import subprocess
import platform
from pathlib import Path


def print_header():
    """Display setup header"""
    print("""
╔══════════════════════════════════════════════════════════════╗
║                 🚀 IONIC PROPULSION LAB SETUP                 ║
║              Enhanced Electric Propulsion Analysis            ║
╚══════════════════════════════════════════════════════════════╝
    """)


def check_python_version():
    """Check if Python version is compatible"""
    print("🐍 Checking Python version...")
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 7):
        print("❌ Python 3.7 or higher is required")
        print(
            f"   Current version: {
                version.major}.{
                version.minor}.{
                version.micro}")
        return False

    print(f"✅ Python {version.major}.{version.minor}.{version.micro} found")
    return True


def install_packages():
    """Install required Python packages"""
    print("\n📦 Installing required packages...")

    required_packages = [
        'numpy',
        'pandas',
        'matplotlib'
    ]

    # Check which packages are missing
    missing_packages = []
    for package in required_packages:
        try:
            __import__(package)
            print(f"✅ {package} already installed")
        except ImportError:
            missing_packages.append(package)

    if not missing_packages:
        print("✅ All packages already installed!")
        return True

    print(f"📥 Installing: {', '.join(missing_packages)}")

    try:
        # Try to install packages
        subprocess.check_call([
            sys.executable, '-m', 'pip', 'install', '--user'
        ] + missing_packages)

        print("✅ Packages installed successfully!")
        return True

    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install packages: {e}")
        print("\n🔧 Manual installation:")
        print(f"   pip install {' '.join(missing_packages)}")
        return False


def create_desktop_shortcut():
    """Create desktop shortcut for Windows"""
    if platform.system() != 'Windows':
        return

    print("\n🖥️  Creating desktop shortcut...")

    try:
        import winshell
        from win32com.client import Dispatch

        desktop = winshell.desktop()
        shortcut_path = os.path.join(desktop, "Ionic Propulsion Lab.lnk")

        shell = Dispatch('WScript.Shell')
        shortcut = shell.CreateShortCut(shortcut_path)
        shortcut.Targetpath = os.path.join(os.getcwd(), "run_lab.bat")
        shortcut.WorkingDirectory = os.getcwd()
        shortcut.IconLocation = sys.executable
        shortcut.save()

        print(f"✅ Desktop shortcut created: {shortcut_path}")

    except ImportError:
        print("ℹ️  Desktop shortcut creation skipped (winshell not available)")
        print("   You can manually create a shortcut to run_lab.bat")

    except Exception as e:
        print(f"ℹ️  Desktop shortcut creation failed: {e}")
        print("   You can still run the lab using run_lab.bat")


def verify_installation():
    """Verify that everything is working"""
    print("\n🔍 Verifying installation...")

    # Check if all files exist
    required_files = [
        'config.json',
        'launcher.py',
        'run_sweep.py',
        'ion_hall_parametric.py',
        'viz/index.html'
    ]

    missing_files = []
    for file_path in required_files:
        if not Path(file_path).exists():
            missing_files.append(file_path)

    if missing_files:
        print("❌ Missing files:")
        for file in missing_files:
            print(f"   - {file}")
        return False

    print("✅ All required files found")

    # Test import of key modules
    try:
# These imports are used in the setup process

        # Quick test calculation
        from ion_hall_parametric import PropulsionCalculator
        calc = PropulsionCalculator()

        print("✅ Core modules working correctly")
        return True

    except Exception as e:
        print(f"❌ Module test failed: {e}")
        return False


def show_usage_instructions():
    """Display usage instructions"""
    print("""
╔══════════════════════════════════════════════════════════════╗
║                    🎯 GETTING STARTED                        ║
╚══════════════════════════════════════════════════════════════╝

🚀 QUICK START:
   1. Double-click: run_lab.bat (Windows)
   2. Or run: python launcher.py (any system)
   3. Select option 1 to run analysis
   4. Select option 2 for interactive visualization

📁 WHAT YOU'LL GET:
   • ion_sweep.csv (1,500 data points)
   • hall_sweep.csv (1,500 data points)
   • 9 professional plots in output/ folder
   • Interactive web dashboard at http://localhost:8000

🎛️  INTERACTIVE FEATURES:
   • Real-time parameter adjustment
   • Multi-gas performance comparison
   • Space-charge effect visualization
   • Efficiency analysis and diagnostics

📚 DOCUMENTATION:
   • USER_GUIDE.md - Step-by-step instructions
   • README.md - Technical documentation
   • config.json - Configuration options

🆘 NEED HELP?
   • Check USER_GUIDE.md for detailed instructions
   • Review README.md for technical details
   • All results saved in output/ folder

╔══════════════════════════════════════════════════════════════╗
║              🎉 ENJOY YOUR PROPULSION ANALYSIS!              ║
╚══════════════════════════════════════════════════════════════╝
    """)


def main():
    """Main setup function"""
    print_header()

    print("Welcome to the Ionic Propulsion Lab Setup!")
    print("This will install and configure the enhanced electric propulsion analysis tool.\n")

    # Check Python version
    if not check_python_version():
        input("Press Enter to exit...")
        return

    # Install packages
    if not install_packages():
        print("\n❌ Setup failed. Please install packages manually and try again.")
        input("Press Enter to exit...")
        return

    # Create desktop shortcut (Windows only)
    create_desktop_shortcut()

    # Verify installation
    if not verify_installation():
        print("\n❌ Setup verification failed.")
        print("   Please check the error messages above.")
        input("Press Enter to exit...")
        return

    # Show success message and usage instructions
    print("\n" + "=" * 70)
    print("🎉 SETUP COMPLETE! Ionic Propulsion Lab is ready to use!")
    print("=" * 70)

    show_usage_instructions()

    input("\nPress Enter to exit...")


if __name__ == "__main__":
    main()
