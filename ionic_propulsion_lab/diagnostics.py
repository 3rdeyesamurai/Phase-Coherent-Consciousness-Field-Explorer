#!/usr/bin/env python3
"""
Ionic Propulsion Lab Diagnostics
Comprehensive system health check and troubleshooting tool
"""

import os
import sys
import platform
import subprocess
import json
from pathlib import Path
import socket
import urllib.request

def print_header():
    """Display diagnostics header"""
    print("""
╔══════════════════════════════════════════════════════════════╗
║                 🔍 IONIC PROPULSION LAB DIAGNOSTICS           ║
║              System Health Check & Troubleshooting             ║
╚══════════════════════════════════════════════════════════════╝
    """)

def check_python_version():
    """Check Python version compatibility"""
    print("🐍 Checking Python version...")

    version = sys.version_info
    print(f"   Current version: {version.major}.{version.minor}.{version.micro}")

    if version.major < 3:
        print("❌ Python 2 is not supported. Please upgrade to Python 3.7+")
        return False, "Python 2 detected"

    if version.major == 3 and version.minor < 7:
        print("❌ Python 3.7 or higher is required")
        print("   Current version is too old")
        return False, "Python version too old"

    print("✅ Python version is compatible")
    return True, None

def check_required_files():
    """Check if all required files exist"""
    print("\n📁 Checking required files...")

    required_files = [
        'config.json',
        'launcher.py',
        'run_sweep.py',
        'ion_hall_parametric.py',
        'viz/index.html',
        'setup.py',
        'USER_GUIDE.md',
        'README.md'
    ]

    missing_files = []
    for file_path in required_files:
        if not Path(file_path).exists():
            missing_files.append(file_path)

    if missing_files:
        print("❌ Missing required files:")
        for file in missing_files:
            print(f"   - {file}")
        return False, f"Missing files: {missing_files}"

    print("✅ All required files found")
    return True, None

def check_config_file():
    """Validate config.json file"""
    print("\n⚙️  Checking configuration file...")

    try:
        with open('config.json', 'r') as f:
            config = json.load(f)

        # Check required sections
        required_sections = ['gases', 'gas_masses', 'ion_engine', 'hall_thruster', 'constants']
        for section in required_sections:
            if section not in config:
                print(f"❌ Missing configuration section: {section}")
                return False, f"Missing config section: {section}"

        # Validate gas masses
        if 'gas_masses' in config:
            for gas, mass in config['gas_masses'].items():
                if not isinstance(mass, (int, float)) or mass <= 0:
                    print(f"❌ Invalid mass for gas {gas}: {mass}")
                    return False, f"Invalid mass for {gas}"

        # Validate ion engine config
        if 'ion_engine' in config:
            ion_config = config['ion_engine']
            required_ion_keys = ['Va_range', 'Ib_range', 'Va_steps', 'Ib_steps']
            for key in required_ion_keys:
                if key not in ion_config:
                    print(f"❌ Missing ion engine parameter: {key}")
                    return False, f"Missing ion parameter: {key}"

        print("✅ Configuration file is valid")
        return True, None

    except json.JSONDecodeError as e:
        print(f"❌ Invalid JSON in config.json: {e}")
        return False, f"JSON error: {e}"
    except FileNotFoundError:
        print("❌ config.json not found")
        return False, "Config file missing"
    except Exception as e:
        print(f"❌ Error reading config.json: {e}")
        return False, f"Config error: {e}"

def check_dependencies():
    """Check Python package dependencies"""
    print("\n📦 Checking Python packages...")

    required_packages = [
        ('numpy', 'numpy'),
        ('pandas', 'pandas'),
        ('matplotlib', 'matplotlib'),
        ('json', 'built-in'),
        ('os', 'built-in'),
        ('sys', 'built-in'),
        ('pathlib', 'built-in')
    ]

    missing_packages = []
    for package_name, import_name in required_packages:
        try:
            if import_name == 'built-in':
                __import__(package_name)
            else:
                __import__(import_name)
            print(f"✅ {package_name} available")
        except ImportError:
            if import_name != 'built-in':
                missing_packages.append(package_name)
                print(f"❌ {package_name} missing")
            else:
                print(f"⚠️  {package_name} (built-in module) not found")

    if missing_packages:
        print(f"\n🔧 To install missing packages, run:")
        print(f"   pip install {' '.join(missing_packages)}")
        return False, f"Missing packages: {missing_packages}"

    print("✅ All required packages available")
    return True, None

def check_file_permissions():
    """Check file and directory permissions"""
    print("\n🔐 Checking file permissions...")

    test_files = [
        'config.json',
        'run_sweep.py',
        'viz/index.html'
    ]

    permission_issues = []

    for file_path in test_files:
        try:
            # Try to read the file
            with open(file_path, 'r') as f:
                f.read(1)
            print(f"✅ Can read {file_path}")
        except PermissionError:
            permission_issues.append(f"Cannot read {file_path}")
            print(f"❌ Cannot read {file_path}")
        except FileNotFoundError:
            print(f"⚠️  {file_path} not found")
        except Exception as e:
            permission_issues.append(f"Error accessing {file_path}: {e}")
            print(f"❌ Error accessing {file_path}: {e}")

    # Check if we can create output directory
    try:
        output_dir = Path('output')
        output_dir.mkdir(exist_ok=True)
        test_file = output_dir / 'test_write.tmp'
        test_file.write_text('test')
        test_file.unlink()
        print("✅ Can create files in output directory")
    except Exception as e:
        permission_issues.append(f"Cannot write to output directory: {e}")
        print(f"❌ Cannot write to output directory: {e}")

    if permission_issues:
        return False, f"Permission issues: {permission_issues}"

    print("✅ File permissions are OK")
    return True, None

def check_network_connectivity():
    """Check network connectivity for web interface"""
    print("\n🌐 Checking network connectivity...")

    try:
        # Check if we can reach a common website
        urllib.request.urlopen('http://www.google.com', timeout=5)
        print("✅ Internet connection available")
        return True, None
    except Exception as e:
        print("⚠️  No internet connection detected")
        print("   Web interface will work locally without internet")
        return True, "No internet (local mode only)"

def check_system_resources():
    """Check system resources"""
    print("\n💻 Checking system resources...")

    # Check available memory (rough estimate)
    try:
        import psutil
        memory = psutil.virtual_memory()
        memory_gb = memory.available / (1024**3)
        print(".1f")
        if memory_gb < 1:
            print("⚠️  Low memory detected. Performance may be slow.")
            return True, "Low memory warning"
    except ImportError:
        print("ℹ️  Memory check skipped (psutil not available)")

    # Check disk space
    try:
        stat = os.statvfs('.')
        free_space_gb = (stat.f_bavail * stat.f_frsize) / (1024**3)
        print(".1f")
        if free_space_gb < 1:
            print("⚠️  Low disk space detected.")
            return False, "Low disk space"
    except AttributeError:
        # Windows doesn't have statvfs
        print("ℹ️  Disk space check skipped (not supported on this OS)")
    except Exception as e:
        print(f"ℹ️  Disk space check failed: {e}")
        print("   This is normal on some systems")

    print("✅ System resources OK")
    return True, None

def test_core_functionality():
    """Test core functionality of the system"""
    print("\n🧪 Testing core functionality...")

    try:
        # Test importing the main module
        from ion_hall_parametric import PropulsionCalculator
        print("✅ Can import PropulsionCalculator")

        # Test creating calculator instance
        calc = PropulsionCalculator()
        print("✅ Can create calculator instance")

        # Test basic calculation
        result = calc.calculate_ion_engine(
            2000, 2.0, 'Xenon',
            0.01, 0.002, 0.7, 0.95, 'cos', 5.0
        )

        if 'T_axial' in result and result['T_axial'] > 0:
            print("✅ Basic calculation works")
        else:
            print("❌ Basic calculation failed")
            return False, "Calculation test failed"

        print("✅ Core functionality test passed")
        return True, None

    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False, f"Import error: {e}"
    except Exception as e:
        print(f"❌ Core functionality test failed: {e}")
        return False, f"Functionality test failed: {e}"

def generate_report(results):
    """Generate a comprehensive diagnostic report"""
    print("\n📋 DIAGNOSTIC REPORT")
    print("="*50)

    all_passed = True
    issues = []

    for test_name, (passed, error_msg) in results.items():
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"{test_name}: {status}")
        if not passed:
            all_passed = False
            issues.append(f"{test_name}: {error_msg}")

    print("="*50)

    if all_passed:
        print("🎉 ALL DIAGNOSTICS PASSED!")
        print("   Your Ionic Propulsion Lab is ready to use.")
        print("\n🚀 Quick start:")
        print("   python launcher.py")
    else:
        print("⚠️  SOME ISSUES DETECTED")
        print("   Please address the following issues:")
        for issue in issues:
            print(f"   • {issue}")

        print("\n🔧 Common solutions:")
        print("   • Run: python setup.py (for first-time setup)")
        print("   • Install missing packages: pip install <package_name>")
        print("   • Check file permissions")
        print("   • Ensure you're in the ionic_propulsion_lab directory")

    return all_passed

def main():
    """Main diagnostic function"""
    print_header()

    print("This diagnostic tool will check your system and identify any issues")
    print("that might prevent the Ionic Propulsion Lab from working properly.\n")

    # Run all diagnostic checks
    results = {}

    results['Python Version'] = check_python_version()
    results['Required Files'] = check_required_files()
    results['Configuration'] = check_config_file()
    results['Dependencies'] = check_dependencies()
    results['File Permissions'] = check_file_permissions()
    results['Network'] = check_network_connectivity()
    results['System Resources'] = check_system_resources()
    results['Core Functionality'] = test_core_functionality()

    # Generate report
    all_passed = generate_report(results)

    print("\n" + "="*50)
    if all_passed:
        print("🎯 NEXT STEPS:")
        print("   1. Run: python launcher.py")
        print("   2. Select option 1 to run analysis")
        print("   3. Select option 2 for interactive visualization")
    else:
        print("🛠️  TROUBLESHOOTING:")
        print("   1. Review the error messages above")
        print("   2. Run: python setup.py (if first time)")
        print("   3. Check USER_GUIDE.md for detailed help")
        print("   4. Re-run this diagnostic: python diagnostics.py")

    input("\nPress Enter to exit...")

if __name__ == "__main__":
    main()
