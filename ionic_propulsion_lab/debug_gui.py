#!/usr/bin/env python3
"""
Debug script to isolate GUI issues
"""

import sys
import traceback

def test_gui_import():
    """Test importing the GUI module"""
    try:
        print("Testing GUI module import...")
        from gui_app import IonicPropulsionGUI
        print("✅ GUI module imported successfully")
        return True
    except Exception as e:
        print(f"❌ GUI module import failed: {e}")
        traceback.print_exc()
        return False

def test_gui_initialization():
    """Test GUI initialization without main loop"""
    try:
        print("\nTesting GUI initialization...")
        import tkinter as tk

        root = tk.Tk()
        root.title("Debug Test")
        root.geometry("400x300")

        # Try to create the GUI instance
        from gui_app import IonicPropulsionGUI
        app = IonicPropulsionGUI(root)

        print("✅ GUI initialized successfully")

        # Don't start main loop, just test initialization
        root.destroy()
        return True

    except Exception as e:
        print(f"❌ GUI initialization failed: {e}")
        traceback.print_exc()
        return False

def test_config_loading():
    """Test configuration loading"""
    try:
        print("\nTesting configuration loading...")
        from gui_app import IonicPropulsionGUI

        # Create a dummy root just for testing
        import tkinter as tk
        root = tk.Tk()

        # Test the load_config method
        gui = IonicPropulsionGUI.__new__(IonicPropulsionGUI)  # Create without __init__
        gui.root = root
        config = gui.load_config()

        print(f"✅ Configuration loaded: {type(config)}")
        print(f"   Keys: {list(config.keys()) if isinstance(config, dict) else 'Not a dict'}")

        root.destroy()
        return True

    except Exception as e:
        print(f"❌ Configuration loading failed: {e}")
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("🔧 GUI Debug Test")
    print("=" * 50)

    success = True

    success &= test_gui_import()
    success &= test_config_loading()
    success &= test_gui_initialization()

    print("\n" + "=" * 50)
    if success:
        print("✅ All tests passed! GUI should work.")
    else:
        print("❌ Some tests failed. Check the error messages above.")
