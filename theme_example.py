#!/usr/bin/env python3
"""
Simple Example: Using ttkthemes for Dark Theme in Tkinter Applications
========================================================================

This example demonstrates how to:
1. Install and use the ttkthemes package
2. Apply dark themes to tkinter/ttk applications
3. Create a simple GUI with theme switching capability

Requirements:
- pip install ttkthemes

Usage:
- Run this script to see theme switching in action
- Click the "Switch Theme" button to toggle between light and dark themes
"""

import tkinter as tk
from tkinter import ttk, messagebox
from ttkthemes import ThemedStyle
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np


class ThemeExampleApp:
    """Simple application demonstrating ttkthemes usage"""

    def __init__(self, root):
        self.root = root
        self.root.title("🚀 ttkthemes Dark Theme Example")
        self.root.geometry("800x600")

        # Initialize theme system
        self.style = ThemedStyle(self.root)
        self.current_theme = "arc"  # Default light theme

        # Create main layout
        self.create_main_layout()

        # Apply initial theme
        self.apply_theme()

        # Create sample plot
        self.create_sample_plot()

    def create_main_layout(self):
        """Create the main application layout"""
        # Main container
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        # Title
        title_label = ttk.Label(
            main_frame,
            text="ttkthemes Dark Theme Demonstration",
            font=("Arial", 16, "bold")
        )
        title_label.pack(pady=(0, 20))

        # Theme control section
        theme_frame = ttk.LabelFrame(main_frame, text="Theme Controls", padding=10)
        theme_frame.pack(fill=tk.X, pady=(0, 20))

        # Theme selection
        ttk.Label(theme_frame, text="Available Themes:").grid(row=0, column=0, sticky='w', pady=5)

        self.theme_var = tk.StringVar(value=self.current_theme)
        theme_combo = ttk.Combobox(
            theme_frame,
            textvariable=self.theme_var,
            values=self.get_available_themes(),
            state="readonly",
            width=20
        )
        theme_combo.grid(row=0, column=1, padx=(10, 0), pady=5)
        theme_combo.bind("<<ComboboxSelected>>", self.on_theme_selected)

        # Quick theme switch button
        ttk.Button(
            theme_frame,
            text="🔄 Switch to Dark Theme",
            command=self.switch_to_dark_theme
        ).grid(row=0, column=2, padx=(20, 0), pady=5)

        # Sample controls section
        controls_frame = ttk.LabelFrame(main_frame, text="Sample Controls", padding=10)
        controls_frame.pack(fill=tk.X, pady=(0, 20))

        # Sample input controls
        ttk.Label(controls_frame, text="Sample Input:").grid(row=0, column=0, sticky='w', pady=5)

        self.input_var = tk.StringVar(value="Hello World!")
        ttk.Entry(
            controls_frame,
            textvariable=self.input_var,
            width=30
        ).grid(row=0, column=1, padx=(10, 0), pady=5)

        # Sample buttons
        button_frame = ttk.Frame(controls_frame)
        button_frame.grid(row=1, column=0, columnspan=3, pady=(10, 0))

        ttk.Button(
            button_frame,
            text="📊 Update Plot",
            command=self.update_plot
        ).pack(side=tk.LEFT, padx=(0, 10))

        ttk.Button(
            button_frame,
            text="ℹ️ Show Info",
            command=self.show_info
        ).pack(side=tk.LEFT, padx=(0, 10))

        ttk.Button(
            button_frame,
            text="❌ Exit",
            command=self.root.quit
        ).pack(side=tk.LEFT)

        # Plot area
        plot_frame = ttk.LabelFrame(main_frame, text="Sample Plot", padding=10)
        plot_frame.pack(fill=tk.BOTH, expand=True)

        # Create matplotlib figure
        self.figure = plt.Figure(figsize=(8, 4), dpi=100)
        self.canvas = FigureCanvasTkAgg(self.figure, plot_frame)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    def get_available_themes(self):
        """Get list of available themes from ttkthemes"""
        return [
            "arc",          # Clean, modern theme (default)
            "equilux",      # Dark theme
            "black",        # Pure black theme
            "blue",         # Blue accent theme
            "clearlooks",   # Traditional GTK theme
            "radiance",     # Ubuntu's Radiance theme
            "ubuntu",       # Ubuntu theme
            "adapta",       # Modern flat theme
            "plastik",      # Plastic-like theme
            "keramik",      # KDE Keramik theme
        ]

    def apply_theme(self):
        """Apply the current theme to the application"""
        try:
            self.style.set_theme(self.current_theme)

            # Configure matplotlib for dark themes
            if self.current_theme in ["equilux", "black"]:
                self.configure_dark_matplotlib()
            else:
                self.configure_light_matplotlib()

            # Update plot if it exists
            if hasattr(self, 'ax'):
                self.update_plot()

        except Exception as e:
            messagebox.showerror("Theme Error", f"Could not apply theme '{self.current_theme}': {e}")

    def configure_dark_matplotlib(self):
        """Configure matplotlib for dark themes"""
        plt.style.use('dark_background')
        plt.rcParams['figure.facecolor'] = '#2a2a2a'
        plt.rcParams['axes.facecolor'] = '#3a3a3a'
        plt.rcParams['axes.edgecolor'] = '#555555'
        plt.rcParams['axes.labelcolor'] = 'white'
        plt.rcParams['text.color'] = 'white'
        plt.rcParams['xtick.color'] = 'white'
        plt.rcParams['ytick.color'] = 'white'
        plt.rcParams['grid.color'] = '#555555'

    def configure_light_matplotlib(self):
        """Configure matplotlib for light themes"""
        plt.style.use('default')
        plt.rcParams['figure.facecolor'] = 'white'
        plt.rcParams['axes.facecolor'] = 'white'
        plt.rcParams['axes.edgecolor'] = 'black'
        plt.rcParams['axes.labelcolor'] = 'black'
        plt.rcParams['text.color'] = 'black'
        plt.rcParams['xtick.color'] = 'black'
        plt.rcParams['ytick.color'] = 'black'
        plt.rcParams['grid.color'] = '#cccccc'

    def on_theme_selected(self, event=None):
        """Handle theme selection from combobox"""
        new_theme = self.theme_var.get()
        if new_theme != self.current_theme:
            self.current_theme = new_theme
            self.apply_theme()

    def switch_to_dark_theme(self):
        """Quick switch to a dark theme"""
        self.current_theme = "equilux"  # Dark theme
        self.theme_var.set(self.current_theme)
        self.apply_theme()

    def create_sample_plot(self):
        """Create a sample plot"""
        self.ax = self.figure.add_subplot(111)

        # Generate sample data
        x = np.linspace(0, 10, 100)
        y = np.sin(x) * np.exp(-x/10)

        self.line, = self.ax.plot(x, y, 'b-', linewidth=2, label='Sample Data')
        self.ax.set_xlabel('X Values')
        self.ax.set_ylabel('Y Values')
        self.ax.set_title('Sample Plot with Theme Support')
        self.ax.grid(True, alpha=0.3)
        self.ax.legend()

        self.canvas.draw()

    def update_plot(self):
        """Update the sample plot with new data"""
        if not hasattr(self, 'ax'):
            return

        # Generate new sample data based on input
        input_text = self.input_var.get()
        try:
            # Try to parse input as a number for frequency
            frequency = float(input_text) if input_text.replace('.', '').isdigit() else 1.0
        except:
            frequency = 1.0

        x = np.linspace(0, 10, 100)
        y = np.sin(frequency * x) * np.exp(-x/10)

        self.line.set_ydata(y)
        self.ax.set_title(f'Sample Plot: sin({frequency}x) * exp(-x/10)')

        self.canvas.draw()

    def show_info(self):
        """Show information about the current theme"""
        info_text = f"""
Current Theme Information:
═══════════════════════════

Theme Name: {self.current_theme}
Theme Type: {'Dark' if self.current_theme in ['equilux', 'black'] else 'Light'}

Available Themes:
{chr(10).join('• ' + theme for theme in self.get_available_themes())}

Usage Tips:
• Use 'equilux' for a modern dark theme
• Use 'arc' for a clean light theme
• Use 'black' for a pure black theme
• All themes support matplotlib integration

The ttkthemes package provides many more themes!
Check the documentation for the complete list.
        """

        messagebox.showinfo("Theme Information", info_text)


def main():
    """Main application entry point"""
    root = tk.Tk()
    app = ThemeExampleApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
