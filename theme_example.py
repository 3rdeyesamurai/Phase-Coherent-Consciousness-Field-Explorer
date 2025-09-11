#!/usr/bin/env python3
"""
Simple Example: Using ttkthemes for Dark Theme in Tkinter Applications
========================================================================

This example demonstrates how to:
1. Install and import ttkthemes
2. Apply dark themes to tkinter/ttk applications
3. Switch between different themes dynamically
4. Customize theme colors and styling

Requirements:
- pip install ttkthemes
- Python 3.6+
"""

import tkinter as tk
from tkinter import ttk, messagebox
from ttkthemes import ThemedStyle
import sys

class ThemeExampleApp:
    """Simple application demonstrating ttkthemes dark theme usage"""

    def __init__(self, root):
        self.root = root
        self.root.title("🎨 ttkthemes Dark Theme Example")
        self.root.geometry("600x500")

        # Initialize ttkthemes style
        self.style = ThemedStyle(self.root)

        # Define available themes (focus on dark themes)
        self.themes = {
            "equilux": "Dark theme with blue accents",
            "black": "Pure black theme",
            "darkly": "Dark theme with green accents",
            "solar": "Dark theme with orange accents",
            "superhero": "Dark theme with blue-grey accents",
            "cyborg": "Dark cyberpunk theme",
            "slate": "Dark slate theme",
            "cosmo": "Modern dark theme",
            "flatly": "Flat dark theme",
            "journal": "Minimal dark theme"
        }

        # Create the GUI
        self.create_widgets()

        # Apply initial dark theme
        self.apply_theme("equilux")

    def create_widgets(self):
        """Create the main application widgets"""
        # Main frame
        main_frame = ttk.Frame(self.root, padding=20)
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Title
        title_label = ttk.Label(
            main_frame,
            text="🦸 ttkthemes Dark Theme Demo",
            font=("Arial", 16, "bold")
        )
        title_label.pack(pady=(0, 20))

        # Theme selection
        theme_frame = ttk.LabelFrame(main_frame, text="🎨 Theme Selection", padding=10)
        theme_frame.pack(fill=tk.X, pady=(0, 20))

        ttk.Label(theme_frame, text="Choose Dark Theme:").pack(anchor=tk.W)

        # Theme combobox
        self.theme_var = tk.StringVar(value="equilux")
        theme_combo = ttk.Combobox(
            theme_frame,
            textvariable=self.theme_var,
            values=list(self.themes.keys()),
            state="readonly"
        )
        theme_combo.pack(fill=tk.X, pady=(5, 10))
        theme_combo.bind("<<ComboboxSelected>>", self.on_theme_change)

        # Theme description
        self.desc_label = ttk.Label(theme_frame, text=self.themes["equilux"])
        self.desc_label.pack(anchor=tk.W)

        # Demo widgets section
        demo_frame = ttk.LabelFrame(main_frame, text="🎯 Demo Widgets", padding=10)
        demo_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 20))

        # Buttons
        button_frame = ttk.Frame(demo_frame)
        button_frame.pack(fill=tk.X, pady=(0, 10))

        ttk.Button(button_frame, text="🚀 Launch", command=self.launch_demo).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(button_frame, text="⚙️ Settings", command=self.settings_demo).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(button_frame, text="❌ Cancel", command=self.cancel_demo).pack(side=tk.LEFT)

        # Progress bar
        ttk.Label(demo_frame, text="Progress:").pack(anchor=tk.W)
        self.progress = ttk.Progressbar(demo_frame, mode='determinate', maximum=100, value=75)
        self.progress.pack(fill=tk.X, pady=(0, 10))

        # Entry field
        ttk.Label(demo_frame, text="Enter your name:").pack(anchor=tk.W)
        self.name_entry = ttk.Entry(demo_frame)
        self.name_entry.pack(fill=tk.X, pady=(0, 10))
        self.name_entry.insert(0, "John Doe")

        # Checkboxes
        check_frame = ttk.Frame(demo_frame)
        check_frame.pack(fill=tk.X, pady=(0, 10))

        self.dark_mode = tk.BooleanVar(value=True)
        ttk.Checkbutton(check_frame, text="Dark Mode", variable=self.dark_mode).pack(side=tk.LEFT, padx=(0, 20))

        self.notifications = tk.BooleanVar(value=True)
        ttk.Checkbutton(check_frame, text="Notifications", variable=self.notifications).pack(side=tk.LEFT)

        # Radio buttons
        ttk.Label(demo_frame, text="Difficulty Level:").pack(anchor=tk.W)
        radio_frame = ttk.Frame(demo_frame)
        radio_frame.pack(fill=tk.X, pady=(0, 10))

        self.difficulty = tk.StringVar(value="medium")
        ttk.Radiobutton(radio_frame, text="Easy", variable=self.difficulty, value="easy").pack(side=tk.LEFT, padx=(0, 10))
        ttk.Radiobutton(radio_frame, text="Medium", variable=self.difficulty, value="medium").pack(side=tk.LEFT, padx=(0, 10))
        ttk.Radiobutton(radio_frame, text="Hard", variable=self.difficulty, value="hard").pack(side=tk.LEFT)

        # Information section
        info_frame = ttk.LabelFrame(main_frame, text="ℹ️ Theme Information", padding=10)
        info_frame.pack(fill=tk.X)

        info_text = """
🎨 ttkthemes provides beautiful pre-built themes for tkinter applications.

Key Features:
• Easy theme switching with single line of code
• Professional dark themes included
• Consistent styling across all widgets
• Customizable colors and fonts
• Cross-platform compatibility

Popular Dark Themes:
• equilux: Blue-accented dark theme
• black: Pure black background
• darkly: Green-accented dark theme
• solar: Orange-accented dark theme
• cyborg: Cyberpunk-inspired theme

Usage:
from ttkthemes import ThemedStyle
style = ThemedStyle(root)
style.set_theme("equilux")  # Apply dark theme
        """

        info_label = ttk.Label(info_frame, text=info_text, justify=tk.LEFT)
        info_label.pack(anchor=tk.W)

    def apply_theme(self, theme_name):
        """Apply the selected theme"""
        try:
            self.style.set_theme(theme_name)
            self.desc_label.config(text=self.themes.get(theme_name, "Unknown theme"))
            print(f"✅ Applied theme: {theme_name}")
        except Exception as e:
            print(f"❌ Error applying theme {theme_name}: {e}")
            messagebox.showerror("Theme Error", f"Could not apply theme {theme_name}: {e}")

    def on_theme_change(self, event=None):
        """Handle theme selection change"""
        selected_theme = self.theme_var.get()
        self.apply_theme(selected_theme)

    def launch_demo(self):
        """Demo launch button action"""
        name = self.name_entry.get()
        difficulty = self.difficulty.get()
        dark_mode = "enabled" if self.dark_mode.get() else "disabled"
        notifications = "enabled" if self.notifications.get() else "disabled"

        message = f"""
🚀 Launch Configuration:

Name: {name}
Difficulty: {difficulty.title()}
Dark Mode: {dark_mode}
Notifications: {notifications}
Theme: {self.theme_var.get()}

Ready for launch! 🌟
        """

        messagebox.showinfo("Launch Demo", message)

    def settings_demo(self):
        """Demo settings button action"""
        messagebox.showinfo("Settings", "⚙️ Settings panel would open here")

    def cancel_demo(self):
        """Demo cancel button action"""
        if messagebox.askyesno("Cancel", "Are you sure you want to cancel?"):
            self.name_entry.delete(0, tk.END)
            self.progress.config(value=0)
            print("❌ Operation cancelled")


def main():
    """Main application entry point"""
    print("🎨 Starting ttkthemes Dark Theme Example...")
    print("Available themes:", list(ThemedStyle().themes))

    root = tk.Tk()
    app = ThemeExampleApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
