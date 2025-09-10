#!/usr/bin/env python3
"""
Simple test script to debug GUI issues
"""

import tkinter as tk
from tkinter import ttk, messagebox
import traceback


def test_basic_gui():
    """Test basic GUI functionality"""
    try:
        print("Testing basic Tkinter...")
        root = tk.Tk()
        root.title("Test GUI")
        root.geometry("400x300")

        # Add a simple label
        label = ttk.Label(
            root, text="GUI Test - If you see this, Tkinter works!")
        label.pack(pady=20)

        # Add a button to close
        def close_app():
            root.quit()
            root.destroy()

        button = ttk.Button(root, text="Close Test", command=close_app)
        button.pack(pady=10)

        print("✅ Basic GUI created successfully")
        print("Starting main loop...")

        # Start the GUI (this will block until window is closed)
        root.mainloop()

        print("✅ GUI test completed successfully")

    except Exception as e:
        print(f"❌ GUI test failed: {e}")
        traceback.print_exc()


if __name__ == "__main__":
    test_basic_gui()
