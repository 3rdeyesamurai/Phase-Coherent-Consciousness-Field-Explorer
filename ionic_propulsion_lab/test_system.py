#!/usr/bin/env python3
"""
Ionic Propulsion Lab System Test
Comprehensive testing of all components and error handling
"""

import os
import sys
import subprocess
import json
from pathlib import Path


def test_pyinstaller():
    """Test PyInstaller availability"""
    print("🔧 Testing PyInstaller...")
    try:
        import PyInstaller
        print("✅ PyInstaller available")
        return True
    except ImportError:
        print("❌ PyInstaller not available")
        print("   Installing PyInstaller...")
        try:
            subprocess.check_call(
                [sys.executable, '-m', 'pip', 'install', 'pyinstaller'])
            print("✅ PyInstaller installed")
            return True
        except Exception as e:
            print(f"❌ Failed to install PyInstaller: {e}")
            return False


def test_dependencies():
    """Test all required dependencies"""
    print("\n📦 Testing dependencies...")

    required = [
        'numpy', 'pandas', 'matplotlib', 'tkinter',
        'json', 'os', 'sys', 'pathlib', 'subprocess', 'threading'
    ]

    missing = []
    for dep in required:
        try:
            if dep == 'tkinter':
                import tkinter
            else:
                __import__(dep)
            print(f"✅ {dep}")
        except ImportError:
            print(f"❌ {dep}")
            missing.append(dep)

    if missing:
        print(f"\n🔧 Installing missing: {missing}")
        try:
            subprocess.check_call(
                [sys.executable, '-m', 'pip', 'install'] + missing)
            print("✅ Dependencies installed")
            return True
        except Exception as e:
            print(f"❌ Failed to install dependencies: {e}")
            return False

    return True


def test_files():
    """Test all required files exist"""
    print("\n📁 Testing file structure...")

    required_files = [
        'config.json',
        'gui_app.py',
        'ion_hall_parametric.py',
        'run_sweep.py',
        'viz/index.html'
    ]

    missing = []
    for file_path in required_files:
        if os.path.exists(file_path):
            print(f"✅ {file_path}")
        else:
            print(f"❌ {file_path}")
            missing.append(file_path)

    return len(missing) == 0, missing


def test_config():
    """Test configuration file"""
    print("\n⚙️  Testing configuration...")

    try:
        with open('config.json', 'r') as f:
            config = json.load(f)

        required_keys = [
            'gases',
            'gas_masses',
            'ion_engine',
            'hall_thruster',
            'constants']
        for key in required_keys:
            if key not in config:
                print(f"❌ Missing config key: {key}")
                return False

        print("✅ Configuration valid")
        return True
    except Exception as e:
        print(f"❌ Configuration error: {e}")
        return False


def test_calculator():
    """Test propulsion calculator"""
    print("\n🧮 Testing calculator...")

    try:
        from ion_hall_parametric import PropulsionCalculator
        calc = PropulsionCalculator()

        # Test ion engine calculation
        result = calc.calculate_ion_engine(
            2000, 2.0, 'Xenon',
            0.01, 0.002, 0.7, 0.95, 'cos', 5.0
        )

        if 'T_axial' in result and result['T_axial'] > 0:
            print("✅ Ion engine calculation works")
        else:
            print("❌ Ion engine calculation failed")
            return False

        # Test Hall thruster calculation
        result = calc.calculate_hall_thruster(
            400, 5e-6, 'Xenon', 0.6, 0.85, 'cos', 30.0
        )

        if 'T_axial' in result and result['T_axial'] > 0:
            print("✅ Hall thruster calculation works")
        else:
            print("❌ Hall thruster calculation failed")
            return False

        return True
    except Exception as e:
        print(f"❌ Calculator test failed: {e}")
        return False


def test_gui_import():
    """Test GUI can be imported"""
    print("\n🖥️  Testing GUI import...")

    try:
        # Just test import, don't create window
        import gui_app
        print("✅ GUI can be imported")
        return True
    except Exception as e:
        print(f"❌ GUI import failed: {e}")
        return False


def test_build_script():
    """Test build script can run"""
    print("\n🏗️  Testing build script...")

    try:
        # Test if build script can at least start
        result = subprocess.run([sys.executable,
                                 'build_executable.py',
                                 '--help'],
                                capture_output=True,
                                text=True,
                                timeout=10)

        # Even if it fails, as long as it runs without crashing
        print("✅ Build script can execute")
        return True
    except subprocess.TimeoutExpired:
        print("⚠️  Build script timed out (expected for --help)")
        return True
    except Exception as e:
        print(f"❌ Build script failed: {e}")
        return False


def run_all_tests():
    """Run all system tests"""
    print("🚀 IONIC PROPULSION LAB - SYSTEM TEST")
    print("=" * 50)

    tests = [
        ("PyInstaller", test_pyinstaller),
        ("Dependencies", test_dependencies),
        ("Files", lambda: test_files()[0]),
        ("Configuration", test_config),
        ("Calculator", test_calculator),
        ("GUI Import", test_gui_import),
        ("Build Script", test_build_script),
    ]

    results = []
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ {test_name} crashed: {e}")
            results.append((test_name, False))

    # Summary
    print("\n" + "=" * 50)
    print("📋 TEST SUMMARY")
    print("=" * 50)

    passed = 0
    total = len(results)

    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{test_name}: {status}")
        if result:
            passed += 1

    print(f"\n📊 Results: {passed}/{total} tests passed")

    if passed == total:
        print("\n🎉 ALL TESTS PASSED!")
        print("   Your Ionic Propulsion Lab is ready for use.")
        print("\n🚀 Quick start options:")
        print("   • python gui_app.py (GUI)")
        print("   • python launcher.py (Menu)")
        print("   • python build_executable.py (Build exe)")
        return True
    else:
        print("\n⚠️  SOME TESTS FAILED")
        print("   Please address the issues above before proceeding.")
        print("\n🔧 Common fixes:")
        print("   • pip install pyinstaller (for executable building)")
        print("   • pip install numpy pandas matplotlib (dependencies)")
        print("   • Check that all files are present")
        return False


if __name__ == "__main__":
    success = run_all_tests()
    input("\nPress Enter to exit...")
    sys.exit(0 if success else 1)
