
#!/usr/bin/env python3
"""
Ionic Propulsion Lab GUI Application
A comprehensive desktop GUI for electric propulsion analysis

Features:
- Real-time parameter adjustment with physics explanations
- Interactive plots and calculations
- Comprehensive error handling
- Standalone executable capability
- Professional user interface
"""

import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext, filedialog
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
import json
import os
import sys
import subprocess
import threading
from datetime import datetime

# Import EMR Suit Visualization components
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'emr_suit_visualization'))
try:
    from visualization import EMRVisualization
    from body_model import EMRBodyModel
    EMR_AVAILABLE = True
except ImportError:
    EMR_AVAILABLE = False
    print("EMR Suit Visualization not available - some features will be disabled")


class IonicPropulsionGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("🚀 Enhanced Ionic Propulsion Lab")
        self.root.geometry("1400x900")
        self.root.minsize(1200, 800)

        # Apply dark theme styling
        self.apply_dark_theme()

    def apply_dark_theme(self):
        """Apply modern dark grey theme to the entire application"""
        # Define dark theme colors (white text, deep dark grey backgrounds, dark orange accents)
        self.dark_colors = {
            'bg_primary': '#1a1a1a',      # Deep dark grey background
            'bg_secondary': '#2a2a2a',    # Slightly lighter deep grey
            'bg_tertiary': '#333333',     # Even lighter deep grey
            'fg_primary': '#ffffff',      # White text
            'fg_secondary': '#cccccc',    # Light grey text
            'fg_accent': '#ff6b35',       # Dark orange accent
            'border': '#404040',          # Dark border color
            'button_bg': '#3a3a3a',       # Dark button background
            'button_hover': '#4a4a4a',    # Dark button hover
            'entry_bg': '#2a2a2a',        # Dark entry background
            'scrollbar': '#404040',       # Dark scrollbar color
            'notebook_tab': '#2a2a2a',    # Dark notebook tab background
            'notebook_active': '#3a3a3a', # Dark active tab background
        }

        # Configure root window
        self.root.configure(bg=self.dark_colors['bg_primary'])

        # Configure ttk styles
        style = ttk.Style()

        # Configure main frames
        style.configure('TFrame', background=self.dark_colors['bg_primary'])
        style.configure('TLabelFrame', background=self.dark_colors['bg_primary'],
                       foreground=self.dark_colors['fg_primary'],
                       bordercolor=self.dark_colors['border'])
        style.configure('TLabelFrame.Label', background=self.dark_colors['bg_primary'],
                       foreground='#666666',  # Dark grey for section titles
                       font=('Segoe UI', 10, 'bold'))

        # Configure labels
        style.configure('TLabel', background=self.dark_colors['bg_primary'],
                       foreground=self.dark_colors['fg_primary'],
                       font=('Segoe UI', 10, 'normal'))

        # Configure buttons with modern styling
        style.configure('TButton',
                       background=self.dark_colors['button_bg'],
                       foreground=self.dark_colors['fg_primary'],
                       bordercolor=self.dark_colors['border'],
                       font=('Segoe UI', 9, 'bold'),
                       padding=8)
        style.map('TButton',
                 background=[('active', self.dark_colors['button_hover']),
                           ('pressed', self.dark_colors['bg_tertiary'])],
                 foreground=[('active', self.dark_colors['fg_accent'])],
                 bordercolor=[('active', self.dark_colors['border'])],
                 relief=[('pressed', 'sunken')])

        # Configure entry fields
        style.configure('TEntry',
                       fieldbackground=self.dark_colors['entry_bg'],
                       bordercolor=self.dark_colors['border'],
                       insertcolor=self.dark_colors['fg_primary'],
                       font=('Segoe UI', 9))

        # Configure combobox
        style.configure('TCombobox',
                       fieldbackground=self.dark_colors['entry_bg'],
                       background=self.dark_colors['button_bg'],
                       bordercolor=self.dark_colors['border'],
                       arrowcolor=self.dark_colors['fg_primary'],
                       font=('Segoe UI', 9))
        style.map('TCombobox',
                 fieldbackground=[('readonly', self.dark_colors['entry_bg'])],
                 selectbackground=[('readonly', self.dark_colors['bg_tertiary'])],
                 selectforeground=[('readonly', self.dark_colors['fg_primary'])],
                 background=[('active', self.dark_colors['button_hover'])],
                 arrowcolor=[('active', self.dark_colors['fg_accent'])])

        # Configure radiobuttons
        style.configure('TRadiobutton',
                       background=self.dark_colors['bg_primary'],
                       foreground=self.dark_colors['fg_primary'],
                       font=('Segoe UI', 9))
        style.map('TRadiobutton',
                 background=[('active', self.dark_colors['bg_primary'])],
                 foreground=[('active', self.dark_colors['fg_accent'])],
                 indicatorcolor=[('selected', self.dark_colors['fg_accent'])],
                 indicatorbackground=[('selected', self.dark_colors['bg_primary'])],
                 indicatorrelief=[('selected', 'flat')])

        # Configure scales (sliders)
        style.configure('TScale',
                       background=self.dark_colors['bg_primary'],
                       troughcolor=self.dark_colors['bg_tertiary'],
                       bordercolor=self.dark_colors['border'],
                       lightcolor=self.dark_colors['button_hover'],
                       darkcolor=self.dark_colors['button_bg'])
        style.map('TScale',
                 background=[('active', self.dark_colors['bg_primary'])],
                 troughcolor=[('active', self.dark_colors['bg_secondary'])],
                 lightcolor=[('active', self.dark_colors['fg_accent'])],
                 darkcolor=[('active', self.dark_colors['button_hover'])])

        # Configure notebook (tabs)
        style.configure('TNotebook',
                       background=self.dark_colors['bg_primary'],
                       bordercolor=self.dark_colors['border'],
                       tabmargins=[2, 5, 2, 0])
        style.configure('TNotebook.Tab',
                       background=self.dark_colors['notebook_tab'],
                       foreground=self.dark_colors['fg_secondary'],
                       bordercolor=self.dark_colors['border'],
                       font=('Segoe UI', 9, 'bold'),
                       padding=[10, 5])
        style.map('TNotebook.Tab',
                 background=[('selected', self.dark_colors['notebook_active']),
                           ('active', self.dark_colors['button_hover'])],
                 foreground=[('selected', self.dark_colors['fg_accent']),
                           ('active', self.dark_colors['fg_primary'])],
                 bordercolor=[('selected', self.dark_colors['border'])],
                 expand=[('selected', [1, 1, 1, 0])])

        # Configure scrollbar
        style.configure('TScrollbar',
                       background=self.dark_colors['scrollbar'],
                       troughcolor=self.dark_colors['bg_secondary'],
                       bordercolor=self.dark_colors['border'],
                       arrowcolor=self.dark_colors['fg_primary'],
                       width=16)
        style.map('TScrollbar',
                 background=[('active', self.dark_colors['button_hover'])],
                 arrowcolor=[('active', self.dark_colors['fg_accent'])],
                 troughcolor=[('active', self.dark_colors['bg_tertiary'])],
                 bordercolor=[('active', self.dark_colors['border'])],
                 relief=[('pressed', 'sunken')])

        # Configure progressbar (if used)
        style.configure('TProgressbar',
                       background=self.dark_colors['fg_accent'],
                       troughcolor=self.dark_colors['bg_tertiary'],
                       bordercolor=self.dark_colors['border'],
                       lightcolor=self.dark_colors['fg_accent'],
                       darkcolor=self.dark_colors['fg_accent'])

        # Apply theme to existing widgets
        self.root.option_add('*TCombobox*Listbox.background', self.dark_colors['bg_secondary'])
        self.root.option_add('*TCombobox*Listbox.foreground', self.dark_colors['fg_primary'])
        self.root.option_add('*TCombobox*Listbox.selectBackground', self.dark_colors['fg_accent'])
        self.root.option_add('*TCombobox*Listbox.selectForeground', self.dark_colors['bg_primary'])

        # Configure menu
        self.root.option_add('*Menu.background', self.dark_colors['bg_secondary'])
        self.root.option_add('*Menu.foreground', self.dark_colors['fg_primary'])
        self.root.option_add('*Menu.selectColor', self.dark_colors['fg_accent'])
        self.root.option_add('*Menu.activeBackground', self.dark_colors['button_hover'])
        self.root.option_add('*Menu.activeForeground', self.dark_colors['fg_primary'])

        # Configure text widgets
        self.root.option_add('*Text.background', self.dark_colors['entry_bg'])
        self.root.option_add('*Text.foreground', self.dark_colors['fg_primary'])
        self.root.option_add('*Text.insertBackground', self.dark_colors['fg_accent'])
        self.root.option_add('*Text.selectBackground', self.dark_colors['fg_accent'])
        self.root.option_add('*Text.selectForeground', self.dark_colors['bg_primary'])

        # Configure scrolled text
        self.root.option_add('*ScrolledText.background', self.dark_colors['entry_bg'])
        self.root.option_add('*ScrolledText.foreground', self.dark_colors['fg_primary'])
        self.root.option_add('*ScrolledText.insertBackground', self.dark_colors['fg_accent'])
        self.root.option_add('*ScrolledText.selectBackground', self.dark_colors['fg_accent'])
        self.root.option_add('*ScrolledText.selectForeground', self.dark_colors['bg_primary'])

        # Configure canvas (for scrollable areas)
        self.root.option_add('*Canvas.background', self.dark_colors['bg_primary'])

        # Configure status bar
        self.root.option_add('*Label.background', self.dark_colors['bg_primary'])
        self.root.option_add('*Label.foreground', self.dark_colors['fg_primary'])

        # Set matplotlib style to dark background
        plt.style.use('dark_background')
        plt.rcParams['figure.facecolor'] = self.dark_colors['bg_primary']
        plt.rcParams['axes.facecolor'] = self.dark_colors['bg_secondary']
        plt.rcParams['axes.edgecolor'] = self.dark_colors['border']
        plt.rcParams['axes.labelcolor'] = self.dark_colors['fg_primary']
        plt.rcParams['text.color'] = self.dark_colors['fg_primary']
        plt.rcParams['xtick.color'] = self.dark_colors['fg_secondary']
        plt.rcParams['ytick.color'] = self.dark_colors['fg_secondary']
        plt.rcParams['grid.color'] = self.dark_colors['border']
        plt.rcParams['savefig.facecolor'] = self.dark_colors['bg_primary']
        plt.rcParams['savefig.edgecolor'] = self.dark_colors['bg_primary']

        # Initialize variables
        self.calc = None
        self.current_results = {}
        self.config = self.load_config()

        # Folder paths
        self.input_folder = tk.StringVar(value=os.getcwd())
        self.output_folder = tk.StringVar(
            value=os.path.join(os.getcwd(), 'output'))

        # Status bar (create early for error handling)
        self.status_var = tk.StringVar()
        self.status_var.set(
            "Initializing - Enhanced Ionic Propulsion Analysis Tool")
        status_bar = ttk.Label(
            self.root,
            textvariable=self.status_var,
            relief=tk.SUNKEN)
        status_bar.pack(side=tk.BOTTOM, fill=tk.X)

        # Mission feasibility indicator
        self.mission_status_var = tk.StringVar()
        self.mission_status_var.set("🟡 Mission Status: Not Analyzed")
        mission_status_bar = ttk.Label(
            self.root,
            textvariable=self.mission_status_var,
            relief=tk.SUNKEN,
            background="light yellow")
        mission_status_bar.pack(side=tk.BOTTOM, fill=tk.X)

        # Parametric sweep configuration variables
        self.sweep_config = {
            'ion_engine': {
                'Va_steps': tk.IntVar(value=20),
                'Ib_steps': tk.IntVar(value=15),
                'Va_min': tk.DoubleVar(value=500),
                'Va_max': tk.DoubleVar(value=4000),
                'Ib_min': tk.DoubleVar(value=0.1),
                'Ib_max': tk.DoubleVar(value=5.0)
            },
            'hall_thruster': {
                'Vd_steps': tk.IntVar(value=20),
                'mdot_steps': tk.IntVar(value=15),
                'Vd_min': tk.DoubleVar(value=200),
                'Vd_max': tk.DoubleVar(value=800),
                'mdot_min': tk.DoubleVar(value=1.0),
                'mdot_max': tk.DoubleVar(value=10.0)
            }
        }

        # Mission planning variables (load from config if available)
        mission_defaults = self.config.get('mission_planning', {}).get('default_values', {})
        self.mission_config = {
            'bus_power': tk.DoubleVar(value=mission_defaults.get('bus_power', 5000)),  # W
            'target_dv': tk.DoubleVar(value=mission_defaults.get('target_dv', 2000)),  # m/s
            'mission_time': tk.DoubleVar(value=mission_defaults.get('mission_time', 365)),  # days
            'engine_count': tk.IntVar(value=mission_defaults.get('engine_count', 4)),
            'engine_rating': tk.DoubleVar(value=mission_defaults.get('engine_rating', 1.0)),  # kW per engine
            'xenon_budget': tk.DoubleVar(value=mission_defaults.get('xenon_budget', 1000)),  # kg
            'power_efficiency': tk.DoubleVar(value=self.config.get('mission_planning', {}).get('power_efficiency', 0.7)),  # Power processing efficiency
            'thrust_margin': tk.DoubleVar(value=self.config.get('mission_planning', {}).get('thrust_margin', 1.2))  # Safety margin
        }

        # Initialize tooltips
        self.create_tooltips()

        # Initialize the GUI components
        self.create_menu()
        self.create_main_layout()
        self.create_parameter_controls()
        self.create_results_display()
        self.initialize_calculator()

        # Create keyboard shortcuts
        self.create_keyboard_shortcuts()

    def create_tooltips(self):
        """Create tooltip functionality for better user experience"""
        # This is a simple tooltip implementation
        # In a full implementation, you'd use a proper tooltip library
        self.tooltip = None

    def create_keyboard_shortcuts(self):
        """Create keyboard shortcuts for common actions"""
        # Bind keyboard shortcuts
        self.root.bind('<Control-r>', lambda e: self.update_calculations())
        self.root.bind('<Control-s>', lambda e: self.run_parametric_sweep())
        self.root.bind('<Control-e>', lambda e: self.export_results())
        self.root.bind('<Control-d>', lambda e: self.run_diagnostics())
        self.root.bind('<F1>', lambda e: self.show_parameter_help())
        self.root.bind('<Control-q>', lambda e: self.root.quit())
        self.root.bind('<Control-m>', lambda e: self.analyze_mission())

    def load_config(self):
        """Load configuration file with proper path resolution for executables"""
        config_paths = [
            'config.json',  # Current directory
            os.path.join(
                os.path.dirname(__file__),
                'config.json'),
            # Script directory
        ]

        # Add PyInstaller path if available
        if hasattr(sys, '_MEIPASS'):
            config_paths.insert(0, os.path.join(sys._MEIPASS, 'config.json'))

        for config_path in config_paths:
            try:
                if os.path.exists(config_path):
                    with open(config_path, 'r') as f:
                        return json.load(f)
            except Exception:
                continue

        # If no config file found, show warning and use defaults
        messagebox.showwarning(
            "Configuration Warning",
            "Could not find config.json file.\nUsing default configuration.")
        return self.get_default_config()

    def get_default_config(self):
        """Return default configuration"""
        return {
            "ion_engine": {
                "Va_range": [500, 4000],
                "Ib_range": [0.1, 5.0],
                "geometry": {"A_grid": 0.01, "d": 0.002, "tau_geom": 0.7},
                "losses": {"tau_trans": 0.95},
                "divergence": {"model": "cos", "sigma_deg": 5.0}
            },
            "hall_thruster": {
                "Vd_range": [200, 800],
                "mdot_range": [1e-6, 10e-6],
                "eta_acc": 0.6,
                "tau_prop": 0.85,
                "divergence": {"model": "cos", "param_deg": 30.0}
            }
        }

    def create_menu(self):
        """Create application menu"""
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)

        # File menu
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(
            label="Run Parametric Sweep",
            command=self.run_parametric_sweep)
        file_menu.add_command(
            label="Export Results",
            command=self.export_results)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.root.quit)

        # Tools menu
        tools_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Tools", menu=tools_menu)
        tools_menu.add_command(
            label="Run Diagnostics",
            command=self.run_diagnostics)
        tools_menu.add_command(
            label="View Documentation",
            command=self.view_documentation)

        # Help menu
        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Help", menu=help_menu)
        help_menu.add_command(
            label="Physics Guide",
            command=self.show_physics_guide)
        help_menu.add_command(
            label="Parameter Help",
            command=self.show_parameter_help)
        help_menu.add_command(label="About", command=self.show_about)

    def create_main_layout(self):
        """Create main application layout"""
        # Main container
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Left panel - Controls with scroll bar
        left_container = ttk.Frame(main_frame, width=450)
        left_container.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 10))

        # Create canvas and scrollbar for left panel
        left_canvas = tk.Canvas(left_container, width=430)
        left_scrollbar = ttk.Scrollbar(left_container, orient="vertical", command=left_canvas.yview)
        left_scrollable_frame = ttk.Frame(left_canvas)

        left_scrollable_frame.bind(
            "<Configure>",
            lambda e: left_canvas.configure(scrollregion=left_canvas.bbox("all"))
        )

        left_canvas.create_window((0, 0), window=left_scrollable_frame, anchor="nw")
        left_canvas.configure(yscrollcommand=left_scrollbar.set)

        # Pack the canvas and scrollbar
        left_canvas.pack(side="left", fill="both", expand=True)
        left_scrollbar.pack(side="right", fill="y")

        # Bind mousewheel to canvas
        def _on_mousewheel(event):
            left_canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        left_canvas.bind_all("<MouseWheel>", _on_mousewheel)

        # Right panel - Results
        right_panel = ttk.Frame(main_frame)
        right_panel.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        self.left_panel = left_scrollable_frame
        self.right_panel = right_panel

    def create_parameter_controls(self):
        """Create parameter control panel"""
        # Thruster type selection
        type_frame = ttk.LabelFrame(
            self.left_panel,
            text="🚀 Thruster Type",
            padding=10)
        type_frame.pack(fill=tk.X, pady=(0, 10))

        self.thruster_type = tk.StringVar(value="ion")
        ttk.Radiobutton(
            type_frame,
            text="Ion Engine",
            variable=self.thruster_type,
            value="ion",
            command=self.update_parameter_controls).pack(
            anchor=tk.W)
        ttk.Radiobutton(
            type_frame,
            text="Hall Thruster",
            variable=self.thruster_type,
            value="hall",
            command=self.update_parameter_controls).pack(
            anchor=tk.W)

        # Gas selection
        gas_frame = ttk.LabelFrame(
            self.left_panel,
            text="🌍 Propellant Gas",
            padding=10)
        gas_frame.pack(fill=tk.X, pady=(0, 10))

        self.gas_var = tk.StringVar(value="Xenon")
        gas_combo = ttk.Combobox(
            gas_frame,
            textvariable=self.gas_var,
            values=[
                "Xenon",
                "Iodine",
                "Krypton",
                "Argon",
                "WaterOH"],
            state="readonly")
        gas_combo.pack(fill=tk.X)
        gas_combo.bind("<<ComboboxSelected>>", self.update_calculations)

        # Mission planning parameters
        self.create_mission_planning_controls()

        # Folder selection
        folder_frame = ttk.LabelFrame(
            self.left_panel,
            text="📁 Input/Output Folders",
            padding=10)
        folder_frame.pack(fill=tk.X, pady=(0, 10))

        # Input folder
        input_frame = ttk.Frame(folder_frame)
        input_frame.pack(fill=tk.X, pady=(0, 5))
        ttk.Label(input_frame, text="Input Folder:").pack(side=tk.LEFT)
        ttk.Entry(
            input_frame,
            textvariable=self.input_folder,
            width=30).pack(
            side=tk.LEFT,
            fill=tk.X,
            expand=True,
            padx=(
                5,
                0))
        ttk.Button(
            input_frame,
            text="Browse",
            command=self.select_input_folder).pack(
            side=tk.RIGHT)

        # Output folder
        output_frame = ttk.Frame(folder_frame)
        output_frame.pack(fill=tk.X, pady=(0, 5))
        ttk.Label(output_frame, text="Output Folder:").pack(side=tk.LEFT)
        ttk.Entry(
            output_frame,
            textvariable=self.output_folder,
            width=30).pack(
            side=tk.LEFT,
            fill=tk.X,
            expand=True,
            padx=(
                5,
                0))
        ttk.Button(
            output_frame,
            text="Browse",
            command=self.select_output_folder).pack(
            side=tk.RIGHT)

        # Ion Engine parameters
        self.ion_frame = ttk.LabelFrame(
            self.left_panel,
            text="⚡ Ion Engine Parameters",
            padding=10)

        # Hall Thruster parameters
        self.hall_frame = ttk.LabelFrame(
            self.left_panel,
            text="🔄 Hall Thruster Parameters",
            padding=10)

        # Sweep parameter controls
        self.create_sweep_controls()

        # EMR Suit Parameter Controls (only if available)
        if EMR_AVAILABLE:
            self.create_emr_parameter_controls()

        # Control buttons
        button_frame = ttk.Frame(self.left_panel)
        button_frame.pack(fill=tk.X, pady=(10, 0))

        ttk.Button(
            button_frame,
            text="🔄 Update Calculations",
            command=self.update_calculations).pack(
            fill=tk.X,
            pady=(
                0,
                5))
        ttk.Button(button_frame, text="📊 Run Parametric Sweep",
                   command=self.run_parametric_sweep).pack(fill=tk.X)

        self.update_parameter_controls()

    def create_mission_planning_controls(self):
        """Create mission planning parameter controls"""
        # Mission planning frame
        self.mission_frame = ttk.LabelFrame(
            self.left_panel,
            text="🛰️ Mission Planning",
            padding=10)
        self.mission_frame.pack(fill=tk.X, pady=(0, 10))

        # Bus power input
        ttk.Label(self.mission_frame, text="Bus Power (W)",
                  font=("Arial", 10, "bold")).pack(anchor=tk.W)
        bus_power_frame = ttk.Frame(self.mission_frame)
        bus_power_frame.pack(fill=tk.X, pady=(0, 10))

        bus_power_scale = ttk.Scale(
            bus_power_frame,
            from_=1000,
            to=20000,
            variable=self.mission_config['bus_power'],
            orient=tk.HORIZONTAL,
            command=self.update_mission_calculations)
        bus_power_scale.pack(side=tk.LEFT, fill=tk.X, expand=True)

        ttk.Label(
            bus_power_frame,
            textvariable=self.mission_config['bus_power'],
            width=8).pack(side=tk.RIGHT)

        ttk.Label(self.mission_frame, text="W (watts)",
                  foreground="yellow").pack(anchor=tk.W, padx=(0, 5))

        # Target Δv input
        ttk.Label(self.mission_frame, text="Target Δv (m/s)",
                  font=("Arial", 10, "bold")).pack(anchor=tk.W)
        dv_frame = ttk.Frame(self.mission_frame)
        dv_frame.pack(fill=tk.X, pady=(0, 10))

        dv_scale = ttk.Scale(
            dv_frame,
            from_=100,
            to=10000,
            variable=self.mission_config['target_dv'],
            orient=tk.HORIZONTAL,
            command=self.update_mission_calculations)
        dv_scale.pack(side=tk.LEFT, fill=tk.X, expand=True)

        ttk.Label(
            dv_frame,
            textvariable=self.mission_config['target_dv'],
            width=8).pack(side=tk.RIGHT)

        ttk.Label(self.mission_frame, text="m/s (meters per second)",
                  foreground="yellow").pack(anchor=tk.W, padx=(0, 5))

        # Mission time input
        ttk.Label(self.mission_frame, text="Mission Time (days)",
                  font=("Arial", 10, "bold")).pack(anchor=tk.W)
        time_frame = ttk.Frame(self.mission_frame)
        time_frame.pack(fill=tk.X, pady=(0, 10))

        time_scale = ttk.Scale(
            time_frame,
            from_=30,
            to=2000,
            variable=self.mission_config['mission_time'],
            orient=tk.HORIZONTAL,
            command=self.update_mission_calculations)
        time_scale.pack(side=tk.LEFT, fill=tk.X, expand=True)

        ttk.Label(
            time_frame,
            textvariable=self.mission_config['mission_time'],
            width=8).pack(side=tk.RIGHT)

        ttk.Label(self.mission_frame, text="days",
                  foreground="yellow").pack(anchor=tk.W, padx=(0, 5))

        # Array design inputs
        ttk.Label(self.mission_frame, text="Array Design",
                  font=("Arial", 10, "bold")).pack(anchor=tk.W, pady=(10, 5))

        # Engine count
        ttk.Label(self.mission_frame, text="Engine Count").pack(anchor=tk.W)
        engine_count_frame = ttk.Frame(self.mission_frame)
        engine_count_frame.pack(fill=tk.X, pady=(0, 5))

        engine_count_scale = ttk.Scale(
            engine_count_frame,
            from_=1,
            to=20,
            variable=self.mission_config['engine_count'],
            orient=tk.HORIZONTAL,
            command=self.update_mission_calculations)
        engine_count_scale.pack(side=tk.LEFT, fill=tk.X, expand=True)

        ttk.Label(
            engine_count_frame,
            textvariable=self.mission_config['engine_count'],
            width=8).pack(side=tk.RIGHT)

        # Engine rating
        ttk.Label(self.mission_frame, text="Engine Rating (kW)").pack(anchor=tk.W)
        engine_rating_frame = ttk.Frame(self.mission_frame)
        engine_rating_frame.pack(fill=tk.X, pady=(0, 10))

        engine_rating_scale = ttk.Scale(
            engine_rating_frame,
            from_=0.1,
            to=5.0,
            variable=self.mission_config['engine_rating'],
            orient=tk.HORIZONTAL,
            command=self.update_mission_calculations)
        engine_rating_scale.pack(side=tk.LEFT, fill=tk.X, expand=True)

        ttk.Label(
            engine_rating_frame,
            textvariable=self.mission_config['engine_rating'],
            width=8).pack(side=tk.RIGHT)

        ttk.Label(self.mission_frame, text="kW per engine",
                  foreground="yellow").pack(anchor=tk.W, padx=(0, 5))

        # Xenon budget input
        ttk.Label(self.mission_frame, text="Xenon Budget (kg)",
                  font=("Arial", 10, "bold")).pack(anchor=tk.W)
        xenon_frame = ttk.Frame(self.mission_frame)
        xenon_frame.pack(fill=tk.X, pady=(0, 10))

        xenon_scale = ttk.Scale(
            xenon_frame,
            from_=10,
            to=5000,
            variable=self.mission_config['xenon_budget'],
            orient=tk.HORIZONTAL,
            command=self.update_mission_calculations)
        xenon_scale.pack(side=tk.LEFT, fill=tk.X, expand=True)

        ttk.Label(
            xenon_frame,
            textvariable=self.mission_config['xenon_budget'],
            width=8).pack(side=tk.RIGHT)

        ttk.Label(self.mission_frame, text="kg (kilograms)",
                  foreground="yellow").pack(anchor=tk.W, padx=(0, 5))

        # Mission analysis button
        ttk.Button(
            self.mission_frame,
            text="📊 Analyze Mission Feasibility",
            command=self.analyze_mission).pack(fill=tk.X, pady=(10, 0))

    def create_sweep_controls(self):
        """Create parametric sweep parameter controls"""
        # Sweep parameters frame
        self.sweep_frame = ttk.LabelFrame(
            self.left_panel,
            text="📊 Parametric Sweep Parameters",
            padding=10)
        self.sweep_frame.pack(fill=tk.X, pady=(0, 10))

        # Ion Engine sweep controls
        ion_sweep_frame = ttk.LabelFrame(
            self.sweep_frame,
            text="Ion Engine Sweep Ranges",
            padding=5)
        ion_sweep_frame.pack(fill=tk.X, pady=(0, 10))

        # Va range controls
        ttk.Label(
            ion_sweep_frame,
            text="Va Range (V):").grid(
            row=0,
            column=0,
            sticky=tk.W,
            pady=2)
        ttk.Label(
            ion_sweep_frame,
            text="Min:").grid(
            row=1,
            column=0,
            sticky=tk.W)
        ttk.Label(
            ion_sweep_frame,
            text="Max:").grid(
            row=2,
            column=0,
            sticky=tk.W)
        ttk.Label(
            ion_sweep_frame,
            text="Steps:").grid(
            row=3,
            column=0,
            sticky=tk.W)

        va_min_entry = ttk.Entry(
            ion_sweep_frame,
            textvariable=self.sweep_config['ion_engine']['Va_min'],
            width=8)
        va_min_entry.grid(row=1, column=1, padx=5)
        va_max_entry = ttk.Entry(
            ion_sweep_frame,
            textvariable=self.sweep_config['ion_engine']['Va_max'],
            width=8)
        va_max_entry.grid(row=2, column=1, padx=5)
        va_steps_entry = ttk.Entry(
            ion_sweep_frame,
            textvariable=self.sweep_config['ion_engine']['Va_steps'],
            width=8)
        va_steps_entry.grid(row=3, column=1, padx=5)

        # Ib range controls
        ttk.Label(
            ion_sweep_frame,
            text="Ib Range (A):").grid(
            row=0,
            column=2,
            sticky=tk.W,
            pady=2)
        ttk.Label(
            ion_sweep_frame,
            text="Min:").grid(
            row=1,
            column=2,
            sticky=tk.W)
        ttk.Label(
            ion_sweep_frame,
            text="Max:").grid(
            row=2,
            column=2,
            sticky=tk.W)
        ttk.Label(
            ion_sweep_frame,
            text="Steps:").grid(
            row=3,
            column=2,
            sticky=tk.W)

        ib_min_entry = ttk.Entry(
            ion_sweep_frame,
            textvariable=self.sweep_config['ion_engine']['Ib_min'],
            width=8)
        ib_min_entry.grid(row=1, column=3, padx=5)
        ib_max_entry = ttk.Entry(
            ion_sweep_frame,
            textvariable=self.sweep_config['ion_engine']['Ib_max'],
            width=8)
        ib_max_entry.grid(row=2, column=3, padx=5)
        ib_steps_entry = ttk.Entry(
            ion_sweep_frame,
            textvariable=self.sweep_config['ion_engine']['Ib_steps'],
            width=8)
        ib_steps_entry.grid(row=3, column=3, padx=5)

        # Hall Thruster sweep controls
        hall_sweep_frame = ttk.LabelFrame(
            self.sweep_frame,
            text="Hall Thruster Sweep Ranges",
            padding=5)
        hall_sweep_frame.pack(fill=tk.X, pady=(0, 10))

        # Vd range controls
        ttk.Label(
            hall_sweep_frame,
            text="Vd Range (V):").grid(
            row=0,
            column=0,
            sticky=tk.W,
            pady=2)
        ttk.Label(
            hall_sweep_frame,
            text="Min:").grid(
            row=1,
            column=0,
            sticky=tk.W)
        ttk.Label(
            hall_sweep_frame,
            text="Max:").grid(
            row=2,
            column=0,
            sticky=tk.W)
        ttk.Label(
            hall_sweep_frame,
            text="Steps:").grid(
            row=3,
            column=0,
            sticky=tk.W)

        vd_min_entry = ttk.Entry(
            hall_sweep_frame,
            textvariable=self.sweep_config['hall_thruster']['Vd_min'],
            width=8)
        vd_min_entry.grid(row=1, column=1, padx=5)
        vd_max_entry = ttk.Entry(
            hall_sweep_frame,
            textvariable=self.sweep_config['hall_thruster']['Vd_max'],
            width=8)
        vd_max_entry.grid(row=2, column=1, padx=5)
        vd_steps_entry = ttk.Entry(
            hall_sweep_frame,
            textvariable=self.sweep_config['hall_thruster']['Vd_steps'],
            width=8)
        vd_steps_entry.grid(row=3, column=1, padx=5)

        # mdot range controls
        ttk.Label(hall_sweep_frame,
                  text="ṁ Range (mg/s):").grid(row=0,
                                               column=2,
                                               sticky=tk.W,
                                               pady=2)
        ttk.Label(
            hall_sweep_frame,
            text="Min:").grid(
            row=1,
            column=2,
            sticky=tk.W)
        ttk.Label(
            hall_sweep_frame,
            text="Max:").grid(
            row=2,
            column=2,
            sticky=tk.W)
        ttk.Label(
            hall_sweep_frame,
            text="Steps:").grid(
            row=3,
            column=2,
            sticky=tk.W)

        mdot_min_entry = ttk.Entry(
            hall_sweep_frame,
            textvariable=self.sweep_config['hall_thruster']['mdot_min'],
            width=8)
        mdot_min_entry.grid(row=1, column=3, padx=5)
        mdot_max_entry = ttk.Entry(
            hall_sweep_frame,
            textvariable=self.sweep_config['hall_thruster']['mdot_max'],
            width=8)
        mdot_max_entry.grid(row=2, column=3, padx=5)
        mdot_steps_entry = ttk.Entry(
            hall_sweep_frame,
            textvariable=self.sweep_config['hall_thruster']['mdot_steps'],
            width=8)
        mdot_steps_entry.grid(row=3, column=3, padx=5)

        # Add validation for numeric inputs
        for entry in [
                va_min_entry,
                va_max_entry,
                va_steps_entry,
                ib_min_entry,
                ib_max_entry,
                ib_steps_entry,
                vd_min_entry,
                vd_max_entry,
                vd_steps_entry,
                mdot_min_entry,
                mdot_max_entry,
                mdot_steps_entry]:
            entry.configure(
                validate="key", validatecommand=(
                    self.root.register(
                        self.validate_numeric), "%P"))

    def update_parameter_controls(self):
        """Update parameter controls based on thruster type"""
        # Remove existing frames
        for frame in [self.ion_frame, self.hall_frame]:
            try:
                frame.pack_forget()
            except BaseException:
                pass

        if self.thruster_type.get() == "ion":
            self.create_ion_controls()
        else:
            self.create_hall_controls()

    def create_ion_controls(self):
        """Create ion engine parameter controls"""
        self.ion_frame.pack(fill=tk.X, pady=(0, 10))

        # Clear existing widgets
        for widget in self.ion_frame.winfo_children():
            widget.destroy()

        # Acceleration Voltage
        ttk.Label(self.ion_frame, text="Acceleration Voltage (Va)",
                  font=("Arial", 10, "bold")).pack(anchor=tk.W)
        va_frame = ttk.Frame(self.ion_frame)
        va_frame.pack(fill=tk.X, pady=(0, 10))

        self.va_var = tk.DoubleVar(value=2000)
        va_scale = ttk.Scale(
            va_frame,
            from_=500,
            to=4000,
            variable=self.va_var,
            orient=tk.HORIZONTAL,
            command=self.update_calculations)
        va_scale.pack(side=tk.LEFT, fill=tk.X, expand=True)

        va_label = ttk.Label(va_frame, textvariable=self.va_var, width=8)
        va_label.pack(side=tk.RIGHT)

        ttk.Label(self.ion_frame, text="V (volts)",
                  foreground="yellow").pack(anchor=tk.W, padx=(0, 5))

        # Beam Current
        ttk.Label(self.ion_frame, text="Beam Current (Ib)",
                  font=("Arial", 10, "bold")).pack(anchor=tk.W)
        ib_frame = ttk.Frame(self.ion_frame)
        ib_frame.pack(fill=tk.X, pady=(0, 10))

        self.ib_var = tk.DoubleVar(value=2.0)
        ib_scale = ttk.Scale(
            ib_frame,
            from_=0.1,
            to=5.0,
            variable=self.ib_var,
            orient=tk.HORIZONTAL,
            command=self.update_calculations)
        ib_scale.pack(side=tk.LEFT, fill=tk.X, expand=True)

        ib_label = ttk.Label(ib_frame, textvariable=self.ib_var, width=8)
        ib_label.pack(side=tk.RIGHT)

        ttk.Label(self.ion_frame, text="A (amperes)",
                  foreground="yellow").pack(anchor=tk.W, padx=(0, 5))

        # Grid Geometry
        ttk.Label(self.ion_frame, text="Grid Parameters",
                  font=("Arial", 10, "bold")).pack(anchor=tk.W, pady=(10, 5))

        # Geometric Transparency
        ttk.Label(
            self.ion_frame,
            text="Geometric Transparency (τ_geom)").pack(
            anchor=tk.W)
        tau_geom_frame = ttk.Frame(self.ion_frame)
        tau_geom_frame.pack(fill=tk.X, pady=(0, 5))

        self.tau_geom_var = tk.DoubleVar(value=0.7)
        tau_geom_scale = ttk.Scale(
            tau_geom_frame,
            from_=0.5,
            to=0.9,
            variable=self.tau_geom_var,
            orient=tk.HORIZONTAL,
            command=self.update_calculations)
        tau_geom_scale.pack(side=tk.LEFT, fill=tk.X, expand=True)

        ttk.Label(
            tau_geom_frame,
            textvariable=self.tau_geom_var,
            width=8).pack(
            side=tk.RIGHT)

        # Transmission Efficiency
        ttk.Label(
            self.ion_frame,
            text="Transmission Efficiency (τ_trans)").pack(
            anchor=tk.W)
        tau_trans_frame = ttk.Frame(self.ion_frame)
        tau_trans_frame.pack(fill=tk.X, pady=(0, 5))

        self.tau_trans_var = tk.DoubleVar(value=0.95)
        tau_trans_scale = ttk.Scale(
            tau_trans_frame,
            from_=0.8,
            to=1.0,
            variable=self.tau_trans_var,
            orient=tk.HORIZONTAL,
            command=self.update_calculations)
        tau_trans_scale.pack(side=tk.LEFT, fill=tk.X, expand=True)

        ttk.Label(
            tau_trans_frame,
            textvariable=self.tau_trans_var,
            width=8).pack(
            side=tk.RIGHT)

        # Divergence Angle
        ttk.Label(self.ion_frame, text="Beam Divergence Angle (σ)",
                  font=("Arial", 10, "bold")).pack(anchor=tk.W, pady=(10, 5))
        sigma_frame = ttk.Frame(self.ion_frame)
        sigma_frame.pack(fill=tk.X, pady=(0, 5))

        self.sigma_var = tk.DoubleVar(value=5.0)
        sigma_scale = ttk.Scale(
            sigma_frame,
            from_=1,
            to=45,
            variable=self.sigma_var,
            orient=tk.HORIZONTAL,
            command=self.update_calculations)
        sigma_scale.pack(side=tk.LEFT, fill=tk.X, expand=True)

        ttk.Label(
            sigma_frame,
            textvariable=self.sigma_var,
            width=8).pack(
            side=tk.RIGHT)

        ttk.Label(self.ion_frame, text="degrees (°) - RMS half-angle",
                  foreground="yellow").pack(anchor=tk.W, padx=(0, 5))

    def create_hall_controls(self):
        """Create Hall thruster parameter controls"""
        self.hall_frame.pack(fill=tk.X, pady=(0, 10))

        # Clear existing widgets
        for widget in self.hall_frame.winfo_children():
            widget.destroy()

        # Discharge Voltage
        ttk.Label(self.hall_frame, text="Discharge Voltage (Vd)",
                  font=("Arial", 10, "bold")).pack(anchor=tk.W)
        vd_frame = ttk.Frame(self.hall_frame)
        vd_frame.pack(fill=tk.X, pady=(0, 10))

        self.vd_var = tk.DoubleVar(value=400)
        vd_scale = ttk.Scale(
            vd_frame,
            from_=200,
            to=800,
            variable=self.vd_var,
            orient=tk.HORIZONTAL,
            command=self.update_calculations)
        vd_scale.pack(side=tk.LEFT, fill=tk.X, expand=True)

        vd_label = ttk.Label(vd_frame, textvariable=self.vd_var, width=8)
        vd_label.pack(side=tk.RIGHT)

        ttk.Label(self.hall_frame, text="V (volts)",
                  foreground="yellow").pack(anchor=tk.W, padx=(0, 5))

        # Mass Flow Rate
        ttk.Label(self.hall_frame, text="Mass Flow Rate (ṁ)",
                  font=("Arial", 10, "bold")).pack(anchor=tk.W)
        mdot_frame = ttk.Frame(self.hall_frame)
        mdot_frame.pack(fill=tk.X, pady=(0, 10))

        self.mdot_var = tk.DoubleVar(value=5.0)
        mdot_scale = ttk.Scale(
            mdot_frame,
            from_=1,
            to=10,
            variable=self.mdot_var,
            orient=tk.HORIZONTAL,
            command=self.update_calculations)
        mdot_scale.pack(side=tk.LEFT, fill=tk.X, expand=True)

        mdot_label = ttk.Label(mdot_frame, textvariable=self.mdot_var, width=8)
        mdot_label.pack(side=tk.RIGHT)

        ttk.Label(self.hall_frame, text="mg/s (milligrams per second)",
                  foreground="yellow").pack(anchor=tk.W, padx=(0, 5))

        # Acceleration Efficiency
        ttk.Label(
            self.hall_frame,
            text="Acceleration Efficiency (η_acc)").pack(
            anchor=tk.W)
        eta_acc_frame = ttk.Frame(self.hall_frame)
        eta_acc_frame.pack(fill=tk.X, pady=(0, 5))

        self.eta_acc_var = tk.DoubleVar(value=0.6)
        eta_acc_scale = ttk.Scale(
            eta_acc_frame,
            from_=0.4,
            to=0.8,
            variable=self.eta_acc_var,
            orient=tk.HORIZONTAL,
            command=self.update_calculations)
        eta_acc_scale.pack(side=tk.LEFT, fill=tk.X, expand=True)

        ttk.Label(
            eta_acc_frame,
            textvariable=self.eta_acc_var,
            width=8).pack(
            side=tk.RIGHT)

        # Propellant Utilization
        ttk.Label(
            self.hall_frame,
            text="Propellant Utilization (τ_prop)").pack(
            anchor=tk.W)
        tau_prop_frame = ttk.Frame(self.hall_frame)
        tau_prop_frame.pack(fill=tk.X, pady=(0, 5))

        self.tau_prop_var = tk.DoubleVar(value=0.85)
        tau_prop_scale = ttk.Scale(
            tau_prop_frame,
            from_=0.7,
            to=0.95,
            variable=self.tau_prop_var,
            orient=tk.HORIZONTAL,
            command=self.update_calculations)
        tau_prop_scale.pack(side=tk.LEFT, fill=tk.X, expand=True)

        ttk.Label(
            tau_prop_frame,
            textvariable=self.tau_prop_var,
            width=8).pack(
            side=tk.RIGHT)

        # Divergence Angle
        ttk.Label(self.hall_frame, text="Beam Divergence Angle",
                  font=("Arial", 10, "bold")).pack(anchor=tk.W, pady=(10, 5))
        hall_sigma_frame = ttk.Frame(self.hall_frame)
        hall_sigma_frame.pack(fill=tk.X, pady=(0, 5))

        self.hall_sigma_var = tk.DoubleVar(value=30.0)
        hall_sigma_scale = ttk.Scale(
            hall_sigma_frame,
            from_=10,
            to=60,
            variable=self.hall_sigma_var,
            orient=tk.HORIZONTAL,
            command=self.update_calculations)
        hall_sigma_scale.pack(side=tk.LEFT, fill=tk.X, expand=True)

        ttk.Label(
            hall_sigma_frame,
            textvariable=self.hall_sigma_var,
            width=8).pack(
            side=tk.RIGHT)

        ttk.Label(self.hall_frame, text="degrees (°) - Full cone angle",
                  foreground="yellow").pack(anchor=tk.W, padx=(0, 5))

    def create_results_display(self):
        """Create results display panel"""
        # Results notebook
        self.results_notebook = ttk.Notebook(self.right_panel)
        self.results_notebook.pack(fill=tk.BOTH, expand=True)

        # Real-time results tab
        realtime_frame = ttk.Frame(self.results_notebook)
        self.results_notebook.add(realtime_frame, text="📊 Real-Time Results")

        self.create_realtime_results(realtime_frame)

        # Physics explanations tab
        physics_frame = ttk.Frame(self.results_notebook)
        self.results_notebook.add(physics_frame, text="🔬 Physics Guide")

        self.create_physics_guide(physics_frame)

        # Plot tab
        plot_frame = ttk.Frame(self.results_notebook)
        self.results_notebook.add(plot_frame, text="📈 Interactive Plot")

        self.create_plot_area(plot_frame)

        # EMR Suit Visualization tab (only if available)
        if EMR_AVAILABLE:
            emr_frame = ttk.Frame(self.results_notebook)
            self.results_notebook.add(emr_frame, text="🦸 EMR Suit Monitor")

            self.create_emr_visualization(emr_frame)

    def create_realtime_results(self, parent):
        """Create real-time results display"""
        # Results display
        results_frame = ttk.LabelFrame(
            parent, text="📈 Current Performance Metrics", padding=10)
        results_frame.pack(fill=tk.BOTH, expand=True)

        # Create scrollable text area for results
        self.results_text = scrolledtext.ScrolledText(
            results_frame, height=20, font=("Consolas", 10))
        self.results_text.pack(fill=tk.BOTH, expand=True)

        # Initial results
        self.update_calculations()

    def create_physics_guide(self, parent):
        """Create physics explanations panel"""
        physics_text = scrolledtext.ScrolledText(
            parent, font=("Arial", 10), wrap=tk.WORD)
        physics_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        physics_content = """
🔬 IONIC PROPULSION PHYSICS GUIDE
═══════════════════════════════════════════════════════════════════════════════

ION ENGINE PHYSICS:
───────────────────

1. THRUST CALCULATION:
   T = I_b × √(2 × m_i × V_a / q) × η_div

   Where:
   • I_b = Beam current (amperes)
   • m_i = Ion mass (kg)
   • V_a = Acceleration voltage (volts)
   • q = Elementary charge (1.602×10⁻¹⁹ C)
   • η_div = Divergence efficiency

2. SPECIFIC IMPULSE:
   I_sp = (v_e / g₀) × η_div

   Where:
   • v_e = Exhaust velocity (m/s)
   • g₀ = Standard gravity (9.81 m/s²)
   • η_div = Divergence efficiency

3. EXHAUST VELOCITY:
   v_e = √(2 × q × V_a / m_i)

4. SPACE-CHARGE LIMIT (Child-Langmuir):
   J_CL = (4/9) × ε₀ × √(2 × q / m_i) × (V_a^(3/2) / d²)

   Where:
   • ε₀ = Permittivity of free space (8.854×10⁻¹² F/m)
   • d = Grid gap distance (m)

5. PERVEANCE MARGIN:
   Margin = I_CL / I_b

   • > 1.0: Operating below space-charge limit
   • < 1.0: Space-charge limited operation

HALL THRUSTER PHYSICS:
──────────────────────

1. THRUST CALCULATION:
   T = ṁ × τ_prop × v_e × η_div

   Where:
   • ṁ = Mass flow rate (kg/s)
   • τ_prop = Propellant utilization efficiency
   • v_e = Exhaust velocity (m/s)
   • η_div = Divergence efficiency

2. EXHAUST VELOCITY:
   v_e = √(η_acc × 2 × q × V_d / m_i)

   Where:
   • η_acc = Acceleration efficiency
   • V_d = Discharge voltage (volts)

3. SPECIFIC IMPULSE:
   I_sp = (v_e / g₀) × η_div

DIVERGENCE MODELS:
──────────────────

1. COSINE MODEL (Recommended):
   η_div = cos(σ)

   Where σ is the RMS half-angle in radians

2. GAUSSIAN MODEL:
   η_div = exp(-σ²/2)

   Where σ is the standard deviation in radians

PARAMETER EFFECTS:
──────────────────

ION ENGINE:
• Higher V_a → Higher I_sp, lower thrust efficiency
• Higher I_b → Higher thrust, same I_sp
• Lower τ_geom → Lower thrust, higher I_sp
• Lower τ_trans → Lower thrust, higher I_sp
• Higher σ → Lower thrust and I_sp

HALL THRUSTER:
• Higher V_d → Higher I_sp
• Higher ṁ → Higher thrust, lower I_sp
• Higher η_acc → Higher I_sp
• Higher τ_prop → Higher thrust
• Lower divergence → Higher efficiency

UNITS AND CONVERSIONS:
──────────────────────

• Thrust: N (newtons) or mN (millinewtons)
• Specific Impulse: s (seconds)
• Power: W (watts)
• Current: A (amperes)
• Voltage: V (volts)
• Mass flow: kg/s or mg/s
• Angles: degrees (°) or radians (rad)

TROUBLESHOOTING:
────────────────

• Low thrust: Check beam current and grid transparency
• Low I_sp: Check acceleration voltage and divergence
• Space-charge limit: Reduce current or increase grid gap
• High power: Check voltage and current settings
• No results: Ensure calculator is initialized

For detailed documentation, see README.md and USER_GUIDE.md
        """

        physics_text.insert(tk.END, physics_content)
        physics_text.config(state=tk.DISABLED)

    def create_plot_area(self, parent):
        """Create interactive plot area"""
        plot_frame = ttk.LabelFrame(
            parent, text="📈 Performance Visualization", padding=10)
        plot_frame.pack(fill=tk.BOTH, expand=True)

        # Plot controls
        control_frame = ttk.Frame(plot_frame)
        control_frame.pack(fill=tk.X, pady=(0, 10))

        ttk.Label(control_frame, text="X-axis:").pack(side=tk.LEFT, padx=(0, 5))
        self.x_var = tk.StringVar(value="Va")
        x_combo = ttk.Combobox(
            control_frame,
            textvariable=self.x_var,
            values=[
                "Va",
                "Ib",
                "T_axial",
                "Isp_eff"],
            width=10)
        x_combo.pack(side=tk.LEFT, padx=(0, 10))

        ttk.Label(control_frame, text="Y-axis:").pack(side=tk.LEFT, padx=(0, 5))
        self.y_var = tk.StringVar(value="T_axial")
        y_combo = ttk.Combobox(
            control_frame,
            textvariable=self.y_var,
            values=[
                "T_axial",
                "Isp_eff",
                "P_elec",
                "perveance_margin"],
            width=10)
        y_combo.pack(side=tk.LEFT, padx=(0, 10))

        ttk.Button(control_frame, text="🔄 Update Plot",
                   command=self.update_plot).pack(side=tk.LEFT)

        # Plot canvas
        self.figure, self.ax = plt.subplots(figsize=(8, 6))
        self.canvas = FigureCanvasTkAgg(self.figure, plot_frame)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

        # Initial plot
        self.update_plot()

    def initialize_calculator(self):
        """Initialize the propulsion calculator"""
        try:
            from ion_hall_parametric import PropulsionCalculator
            self.calc = PropulsionCalculator()
            self.status_var.set("✅ Calculator initialized successfully")
        except Exception as e:
            messagebox.showerror("Initialization Error",
                                 f"Could not initialize calculator: {e}")
            self.status_var.set("❌ Calculator initialization failed")

    def update_calculations(self, *args):
        """Update real-time calculations"""
        if not self.calc:
            return

        try:
            if self.thruster_type.get() == "ion":
                # Ion engine calculation
                result = self.calc.calculate_ion_engine(
                    self.va_var.get(),
                    self.ib_var.get(),
                    self.gas_var.get(),
                    self.config['ion_engine']['geometry']['A_grid'],
                    self.config['ion_engine']['geometry']['d'],
                    self.tau_geom_var.get(),
                    self.tau_trans_var.get(),
                    self.config['ion_engine']['divergence']['model'],
                    self.sigma_var.get()
                )

                self.display_ion_results(result)

            else:
                # Hall thruster calculation
                result = self.calc.calculate_hall_thruster(
                    self.vd_var.get(),
                    self.mdot_var.get() * 1e-6,  # Convert mg/s to kg/s
                    self.gas_var.get(),
                    self.eta_acc_var.get(),
                    self.tau_prop_var.get(),
                    self.config['hall_thruster']['divergence']['model'],
                    self.hall_sigma_var.get()
                )

                self.display_hall_results(result)

            self.current_results = result
            self.update_plot()

        except Exception as e:
            self.results_text.delete(1.0, tk.END)
            self.results_text.insert(tk.END, f"❌ Calculation Error: {e}")
            self.status_var.set(f"❌ Calculation error: {str(e)[:50]}...")

    def update_mission_calculations(self, *args):
        """Update mission-related calculations when parameters change"""
        # This method is called when mission planning sliders change
        # Could be used for real-time mission feasibility updates
        pass

    def analyze_mission(self):
        """Analyze mission feasibility based on current parameters"""
        if not self.current_results:
            messagebox.showwarning("No Results", "Please run calculations first.")
            return

        try:
            # Get current thruster results
            result = self.current_results

            # Mission parameters
            bus_power = self.mission_config['bus_power'].get()
            target_dv = self.mission_config['target_dv'].get()
            mission_time = self.mission_config['mission_time'].get()
            engine_count = self.mission_config['engine_count'].get()
            engine_rating = self.mission_config['engine_rating'].get()
            xenon_budget = self.mission_config['xenon_budget'].get()
            power_efficiency = self.mission_config['power_efficiency'].get()
            thrust_margin = self.mission_config['thrust_margin'].get()

            # Calculate array performance
            single_engine_power = result['P_elec']
            single_engine_thrust = result['T_axial']

            # Array calculations
            array_power = single_engine_power * engine_count
            array_thrust = single_engine_thrust * engine_count

            # Power analysis
            available_power = bus_power * power_efficiency
            power_utilization = (array_power / available_power) * 100

            # Thrust analysis (with margin)
            required_thrust = single_engine_thrust * thrust_margin
            array_thrust_margin = array_thrust / required_thrust

            # Mass flow and propellant analysis
            single_engine_mdot = result['mdot']
            array_mdot = single_engine_mdot * engine_count

            # Mission duration analysis
            mission_seconds = mission_time * 24 * 3600  # Convert days to seconds
            total_propellant_needed = array_mdot * mission_seconds

            # Xenon budget analysis
            propellant_utilization = (total_propellant_needed / xenon_budget) * 100

            # Δv calculation (simplified)
            isp_eff = result.get('Isp_eff', result.get('Isp_ax', 0))
            if isp_eff > 0:
                actual_dv = isp_eff * 9.81 * np.log(1 + (xenon_budget / (engine_count * 10)))  # Rough estimate
                dv_achievement = (actual_dv / target_dv) * 100
            else:
                actual_dv = 0
                dv_achievement = 0

            # Mission feasibility assessment
            feasibility_score = 0
            issues = []

            if power_utilization <= 100:
                feasibility_score += 25
            else:
                issues.append("Power consumption exceeds available bus power")

            if propellant_utilization <= 100:
                feasibility_score += 25
            else:
                issues.append("Propellant consumption exceeds budget")

            if dv_achievement >= 100:
                feasibility_score += 25
            else:
                issues.append(f"Δv achievement: {dv_achievement:.1f}% of target")

            if array_thrust_margin >= 1.0:
                feasibility_score += 25
            else:
                issues.append("Insufficient thrust margin")

            # Display mission analysis results
            self.display_mission_analysis(
                result, array_power, array_thrust, power_utilization,
                propellant_utilization, dv_achievement, feasibility_score, issues
            )

        except Exception as e:
            messagebox.showerror("Mission Analysis Error", f"Could not analyze mission: {e}")

    def display_mission_analysis(self, result, array_power, array_thrust,
                                power_utilization, propellant_utilization,
                                dv_achievement, feasibility_score, issues):
        """Display mission analysis results"""
        self.results_text.delete(1.0, tk.END)

        # Mission parameters summary
        mission_params = f"""
╔══════════════════════════════════════════════════════════════╗
║                    🛰️ MISSION ANALYSIS                          ║
║                Feasibility Assessment                          ║
╚══════════════════════════════════════════════════════════════╝

📊 MISSION PARAMETERS:
   • Bus Power: {self.mission_config['bus_power'].get():.0f} W
   • Target Δv: {self.mission_config['target_dv'].get():.0f} m/s
   • Mission Time: {self.mission_config['mission_time'].get():.0f} days
   • Engine Count: {self.mission_config['engine_count'].get()}
   • Engine Rating: {self.mission_config['engine_rating'].get():.1f} kW
   • Xenon Budget: {self.mission_config['xenon_budget'].get():.0f} kg

🔧 ARRAY PERFORMANCE:
   • Single Engine Power: {result['P_elec']:.0f} W
   • Single Engine Thrust: {result['T_axial'] * 1000:.1f} mN
   • Array Power: {array_power:.0f} W
   • Array Thrust: {array_thrust * 1000:.1f} mN

⚡ POWER ANALYSIS:
   • Available Power: {self.mission_config['bus_power'].get() * self.mission_config['power_efficiency'].get():.0f} W
   • Power Utilization: {power_utilization:.1f}%
   • Status: {'✅ Within limits' if power_utilization <= 100 else '❌ Exceeds limits'}

🧪 PROPELLANT ANALYSIS:
   • Propellant Utilization: {propellant_utilization:.1f}%
   • Status: {'✅ Within budget' if propellant_utilization <= 100 else '❌ Exceeds budget'}

🚀 MISSION PERFORMANCE:
   • Δv Achievement: {dv_achievement:.1f}%
   • Status: {'✅ Target met' if dv_achievement >= 100 else '❌ Target not met'}

📈 THRUST MARGIN:
   • Thrust Margin: {self.mission_config['thrust_margin'].get():.1f}x
   • Status: {'✅ Adequate margin' if array_thrust / (result['T_axial'] * self.mission_config['thrust_margin'].get()) >= 1 else '❌ Insufficient margin'}

🎯 FEASIBILITY SCORE: {feasibility_score}/100
   • {'🟢 HIGH FEASIBILITY' if feasibility_score >= 75 else '🟡 MODERATE FEASIBILITY' if feasibility_score >= 50 else '🔴 LOW FEASIBILITY'}
        """

        if issues:
            mission_params += f"\n⚠️ ISSUES IDENTIFIED:\n"
            for i, issue in enumerate(issues, 1):
                mission_params += f"   {i}. {issue}\n"

        mission_params += f"""
💡 RECOMMENDATIONS:
   • {'Increase engine count or reduce power per engine' if power_utilization > 100 else 'Power allocation looks good'}
   • {'Increase xenon budget or reduce mission time' if propellant_utilization > 100 else 'Propellant budget is adequate'}
   • {'Optimize thruster performance or extend mission time' if dv_achievement < 100 else 'Δv target is achievable'}
   • {'Review thrust requirements and safety margins' if array_thrust / (result['T_axial'] * self.mission_config['thrust_margin'].get()) < 1 else 'Thrust margin is appropriate'}
        """

        self.results_text.insert(tk.END, mission_params)

        # Update mission status indicator
        if feasibility_score >= 75:
            self.mission_status_var.set(f"🟢 Mission Status: HIGH FEASIBILITY ({feasibility_score}/100)")
        elif feasibility_score >= 50:
            self.mission_status_var.set(f"🟡 Mission Status: MODERATE FEASIBILITY ({feasibility_score}/100)")
        else:
            self.mission_status_var.set(f"🔴 Mission Status: LOW FEASIBILITY ({feasibility_score}/100)")

        self.status_var.set(f"✅ Mission analysis complete - Feasibility: {feasibility_score}/100")

    def display_ion_results(self, result):
        """Display ion engine calculation results"""
        self.results_text.delete(1.0, tk.END)

        output = f"""
╔══════════════════════════════════════════════════════════════╗
║                    🚀 ION ENGINE RESULTS                        ║
║                Enhanced Physics Calculations                   ║
╚══════════════════════════════════════════════════════════════╝

📊 INPUT PARAMETERS:
   • Gas: {result['gas']}
   • Acceleration Voltage: {result['Va']:.0f} V
   • Beam Current: {result['Ib']:.2f} A
   • Geometric Transparency: {result['tau_geom']:.3f}
   • Transmission Efficiency: {result['tau_trans']:.3f}
   • Divergence Angle: {result['sigma_deg']:.1f}°

🔬 PHYSICS CALCULATIONS:

IDEAL PERFORMANCE (No Losses):
   • Ideal Thrust: {result['T_ideal'] * 1000:.1f} mN
   • Exhaust Velocity: {result['v_e0']:.0f} m/s

SPACE-CHARGE ANALYSIS:
   • Child-Langmuir Current: {result['I_CL']:.2f} A
   • Current Density: {result['J_CL']:.1e} A/m²
   • Perveance Margin: {result['perveance_margin']:.2f}
   • Space-charge Factor: {result['tau_imp']:.3f}

ACTUAL PERFORMANCE (With Losses):
   • Effective Thrust: {result['T_axial'] * 1000:.1f} mN
   • Effective Isp: {result['Isp_eff']:.1f} s
   • Electrical Power: {result['P_elec']:.0f} W
   • Mass Flow Rate: {result['mdot'] * 1000:.1f} mg/s

EFFICIENCY ANALYSIS:
   • Thrust Efficiency: {(result['T_axial'] / result['T_ideal']) * 100:.1f}%
   • Divergence Efficiency: {result['eta_div']:.3f}
   • Overall Efficiency: {result['eta_div'] * result['tau_geom'] * result['tau_trans'] * result['tau_imp']:.3f}

⚠️  INTERPRETATION:
   • Perveance > 1.0: Operating below space-charge limit
   • Perveance < 1.0: Space-charge limited (reduce current)
   • Higher divergence angle reduces efficiency
   • Grid transparency affects thrust directly

💡 TIPS:
   • For maximum thrust: Increase beam current
   • For maximum Isp: Increase acceleration voltage
   • For optimal efficiency: Minimize divergence angle
   • Monitor perveance margin to avoid space-charge issues
        """

        self.results_text.insert(tk.END, output)
        self.status_var.set(
            f"✅ Ion engine calculation complete - Thrust: {result['T_axial'] * 1000:.1f} mN")

    def display_hall_results(self, result):
        """Display Hall thruster calculation results"""
        self.results_text.delete(1.0, tk.END)

        output = f"""
╔══════════════════════════════════════════════════════════════╗
║                  🔄 HALL THRUSTER RESULTS                      ║
║                Enhanced Physics Calculations                   ║
╚══════════════════════════════════════════════════════════════╝

📊 INPUT PARAMETERS:
   • Gas: {result['gas']}
   • Discharge Voltage: {result['Vd']:.0f} V
   • Mass Flow Rate: {result['mdot'] * 1000:.1f} mg/s
   • Acceleration Efficiency: {result['eta_div']:.3f}
   • Propellant Utilization: {result['tau_prop']:.3f}
   • Divergence Angle: {result['eta_div']:.1f}°

🔬 PHYSICS CALCULATIONS:

PERFORMANCE METRICS:
   • Thrust: {result['T_axial'] * 1000:.1f} mN
   • Specific Impulse: {result['Isp_ax']:.1f} s
   • Exhaust Velocity: {result['v_e0']:.0f} m/s
   • Electrical Power: {result['P_elec']:.0f} W
   • Beam Current: {result['Ib']:.2f} A

EFFICIENCY ANALYSIS:
   • Divergence Efficiency: {result['eta_div']:.3f}
   • Overall Efficiency: {result['eta_div'] * result['tau_prop']:.3f}

⚠️  INTERPRETATION:
   • Higher discharge voltage increases Isp
   • Higher mass flow increases thrust but reduces Isp
   • Efficiency depends on magnetic field design
   • Divergence losses reduce overall performance

💡 TIPS:
   • For maximum thrust: Increase mass flow rate
   • For maximum Isp: Increase discharge voltage
   • Monitor efficiency for optimal operation
   • Consider thermal management at high power
        """

        self.results_text.insert(tk.END, output)
        self.status_var.set(
            f"✅ Hall thruster calculation complete - Thrust: {result['T_axial'] * 1000:.1f} mN")

    def update_plot(self):
        """Update the interactive plot"""
        if not hasattr(self, 'current_results') or not self.current_results:
            return

        try:
            self.ax.clear()

            # Simple parameter sweep for visualization
            if self.thruster_type.get() == "ion":
                # Vary voltage for ion engine
                voltages = np.linspace(500, 4000, 50)
                thrusts = []
                isp_values = []

                for va in voltages:
                    result = self.calc.calculate_ion_engine(
                        va, self.ib_var.get(), self.gas_var.get(),
                        self.config['ion_engine']['geometry']['A_grid'],
                        self.config['ion_engine']['geometry']['d'],
                        self.tau_geom_var.get(), self.tau_trans_var.get(),
                        self.config['ion_engine']['divergence']['model'],
                        self.sigma_var.get()
                    )
                    thrusts.append(result['T_axial'] * 1000)  # Convert to mN
                    isp_values.append(result['Isp_eff'])

                x_data = voltages
                x_label = "Acceleration Voltage (V)"

            else:
                # Vary voltage for Hall thruster
                voltages = np.linspace(200, 800, 50)
                thrusts = []
                isp_values = []

                for vd in voltages:
                    result = self.calc.calculate_hall_thruster(
                        vd, self.mdot_var.get() * 1e-6, self.gas_var.get(),
                        self.eta_acc_var.get(), self.tau_prop_var.get(),
                        self.config['hall_thruster']['divergence']['model'],
                        self.hall_sigma_var.get()
                    )
                    thrusts.append(result['T_axial'] * 1000)  # Convert to mN
                    isp_values.append(result['Isp_ax'])

                x_data = voltages
                x_label = "Discharge Voltage (V)"

            # Plot based on selected variables
            x_var = self.x_var.get()
            y_var = self.y_var.get()

            if x_var == "Va" or x_var == "Vd":
                x_plot = x_data
            elif x_var == "Ib":
                x_plot = [self.ib_var.get()] * len(thrusts)
            elif x_var == "T_axial":
                x_plot = thrusts
            else:  # Isp_eff or Isp_ax
                x_plot = isp_values

            if y_var == "T_axial":
                y_plot = thrusts
                y_label = "Thrust (mN)"
            elif y_var == "Isp_eff" or y_var == "Isp_ax":
                y_plot = isp_values
                y_label = "Specific Impulse (s)"
            elif y_var == "P_elec":
                # Approximate power calculation
                if self.thruster_type.get() == "ion":
                    y_plot = [va * self.ib_var.get() for va in x_data]
                else:
                    y_plot = [vd * 10 for vd in x_data]  # Rough approximation
                y_label = "Electrical Power (W)"
            else:  # perveance_margin (ion only)
                if self.thruster_type.get() == "ion":
                    y_plot = [0.8] * len(thrusts)  # Placeholder
                else:
                    y_plot = [1.0] * len(thrusts)
                y_label = "Perveance Margin"

            self.ax.plot(
                x_plot,
                y_plot,
                'b-',
                linewidth=2,
                marker='o',
                markersize=3)
            self.ax.set_xlabel(x_label)
            self.ax.set_ylabel(y_label)
            self.ax.set_title(
                f"{self.thruster_type.get().title()} Performance: {y_var} vs {x_var}")
            self.ax.grid(True, alpha=0.3)

            self.figure.tight_layout()
            self.canvas.draw()

        except Exception as e:
            self.ax.clear()
            self.ax.text(0.5, 0.5, f"Plot Error:\n{str(e)}",
                         ha='center', va='center', transform=self.ax.transAxes)
            self.canvas.draw()

    def run_parametric_sweep(self):
        """Run parametric sweep in background thread with GUI-configured parameters"""
        def sweep_worker():
            try:
                self.status_var.set("🔬 Preparing parametric sweep...")

                # Create dynamic configuration based on GUI settings
                sweep_config = self.create_sweep_config()

                # Save temporary config file
                temp_config_path = os.path.join(
                    os.getcwd(), 'temp_sweep_config.json')
                with open(temp_config_path, 'w') as f:
                    json.dump(sweep_config, f, indent=2)

                self.status_var.set("🔬 Running parametric sweep...")

                # Run sweep with temporary config and output folder
                env = os.environ.copy()
                env['IONIC_SWEEP_CONFIG'] = temp_config_path
                env['IONIC_OUTPUT_FOLDER'] = self.output_folder.get()

                result = subprocess.run([sys.executable,
                                         'run_sweep.py'],
                                        capture_output=True,
                                        text=True,
                                        cwd=os.path.dirname(__file__) or os.getcwd(),
                                        env=env)

                # Clean up temporary config
                if os.path.exists(temp_config_path):
                    os.remove(temp_config_path)

                if result.returncode == 0:
                    self.status_var.set(
                        "✅ Parametric sweep completed successfully!")
                    output_folder_name = self.output_folder.get()
                    messagebox.showinfo("Success",
                                        f"Parametric sweep completed!\n\n"
                                        f"Results saved to {output_folder_name} folder:\n"
                                        "• ion_sweep.csv\n"
                                        "• hall_sweep.csv\n"
                                        "• 9 professional plots")
                else:
                    self.status_var.set("❌ Parametric sweep failed")
                    messagebox.showerror(
                        "Sweep Failed",
                        f"Parametric sweep failed:\n{
                            result.stderr}")

            except Exception as e:
                self.status_var.set("❌ Parametric sweep error")
                messagebox.showerror("Error", f"Parametric sweep failed: {e}")

        # Run in background thread to avoid freezing GUI
        sweep_thread = threading.Thread(target=sweep_worker, daemon=True)
        sweep_thread.start()

    def create_sweep_config(self):
        """Create sweep configuration based on current GUI settings"""
        thruster_type = self.thruster_type.get()

        if thruster_type == "ion":
            config = {
                "gases": [self.gas_var.get()],
                "gas_masses": {self.gas_var.get(): self.config['gas_masses'][self.gas_var.get()]},
                "ion_engine": {
                    "Va_range": [self.sweep_config['ion_engine']['Va_min'].get(),
                                 self.sweep_config['ion_engine']['Va_max'].get()],
                    "Ib_range": [self.sweep_config['ion_engine']['Ib_min'].get(),
                                 self.sweep_config['ion_engine']['Ib_max'].get()],
                    "Va_steps": self.sweep_config['ion_engine']['Va_steps'].get(),
                    "Ib_steps": self.sweep_config['ion_engine']['Ib_steps'].get(),
                    "geometry": self.config['ion_engine']['geometry'],
                    "losses": {
                        "tau_trans": self.tau_trans_var.get()
                    },
                    "divergence": {
                        "model": self.config['ion_engine']['divergence']['model'],
                        "sigma_deg": self.sigma_var.get()
                    }
                },
                "hall_thruster": self.config['hall_thruster'],
                "constants": self.config['constants']
            }
        else:
            config = {
                "gases": [self.gas_var.get()],
                "gas_masses": {self.gas_var.get(): self.config['gas_masses'][self.gas_var.get()]},
                "ion_engine": self.config['ion_engine'],
                "hall_thruster": {
                    "Vd_range": [self.sweep_config['hall_thruster']['Vd_min'].get(),
                                 self.sweep_config['hall_thruster']['Vd_max'].get()],
                    "mdot_range": [self.sweep_config['hall_thruster']['mdot_min'].get(),
                                   self.sweep_config['hall_thruster']['mdot_max'].get()],
                    "Vd_steps": self.sweep_config['hall_thruster']['Vd_steps'].get(),
                    "mdot_steps": self.sweep_config['hall_thruster']['mdot_steps'].get(),
                    "eta_acc": self.eta_acc_var.get(),
                    "tau_prop": self.tau_prop_var.get(),
                    "divergence": {
                        "model": self.config['hall_thruster']['divergence']['model'],
                        "param_deg": self.hall_sigma_var.get()
                    }
                },
                "constants": self.config['constants']
            }

        return config

    def validate_numeric(self, value):
        """Validate numeric input for sweep parameters"""
        if value == "":
            return True
        try:
            float(value)
            return True
        except ValueError:
            return False

    def select_input_folder(self):
        """Select input folder for configuration files"""
        folder = filedialog.askdirectory(title="Select Input Folder")
        if folder:
            self.input_folder.set(folder)

    def select_output_folder(self):
        """Select output folder for results and plots"""
        folder = filedialog.askdirectory(title="Select Output Folder")
        if folder:
            self.output_folder.set(folder)

    def export_results(self):
        """Export current results to file"""
        if not self.current_results:
            messagebox.showwarning(
                "No Results",
                "No results to export. Run calculations first.")
            return

        try:
            filename = filedialog.asksaveasfilename(
                defaultextension=".json",
                filetypes=[("JSON files", "*.json"), ("All files", "*.*")],
                title="Export Results"
            )

            if filename:
                with open(filename, 'w') as f:
                    json.dump(self.current_results, f, indent=2)

                messagebox.showinfo("Export Complete",
                                    f"Results exported to:\n{filename}")

        except Exception as e:
            messagebox.showerror(
                "Export Error",
                f"Could not export results: {e}")

    def run_diagnostics(self):
        """Run system diagnostics"""
        try:
            result = subprocess.run([sys.executable,
                                     'diagnostics.py'],
                                    capture_output=True,
                                    text=True,
                                    cwd=os.getcwd())

            if result.returncode == 0:
                messagebox.showinfo(
                    "Diagnostics Complete",
                    "System diagnostics completed successfully!\n\n"
                    "All components are working properly.")
            else:
                messagebox.showwarning(
                    "Diagnostics Issues",
                    f"Some issues detected:\n{
                        result.stderr}")

        except Exception as e:
            messagebox.showerror(
                "Diagnostics Error",
                f"Could not run diagnostics: {e}")

    def view_documentation(self):
        """Open documentation files"""
        docs = ["README.md", "USER_GUIDE.md", "INSTALL_GUIDE.md"]

        for doc in docs:
            if os.path.exists(doc):
                try:
                    if sys.platform == 'win32':
                        os.startfile(doc)
                    elif sys.platform == 'darwin':
                        subprocess.run(['open', doc])
                    else:
                        subprocess.run(['xdg-open', doc])
                except Exception as e:
                    messagebox.showerror("Documentation Error",
                                         f"Could not open {doc}: {e}")
                break
        else:
            messagebox.showwarning(
                "Documentation Not Found",
                "Documentation files not found in current directory.")

    def show_physics_guide(self):
        """Show physics guide dialog"""
        self.results_notebook.select(1)  # Switch to physics tab

    def show_parameter_help(self):
        """Show parameter help dialog"""
        help_text = """
IONIC PROPULSION PARAMETER GUIDE
═══════════════════════════════════════════════════════════════════════════════

ACCELERATION VOLTAGE (Va) - Ion Engine:
• Units: Volts (V)
• Range: 500 - 4000 V
• Effect: Higher voltage → Higher Isp, Lower thrust efficiency
• Physics: v_e = √(2 × q × Va / m_i)

BEAM CURRENT (Ib) - Ion Engine:
• Units: Amperes (A)
• Range: 0.1 - 5.0 A
• Effect: Higher current → Higher thrust, Same Isp
• Physics: T ∝ Ib (proportional relationship)

DISCHARGE VOLTAGE (Vd) - Hall Thruster:
• Units: Volts (V)
• Range: 200 - 800 V
• Effect: Higher voltage → Higher Isp
• Physics: v_e = √(η_acc × 2 × q × Vd / m_i)

MASS FLOW RATE (ṁ) - Hall Thruster:
• Units: mg/s (milligrams per second)
• Range: 1 - 10 mg/s
• Effect: Higher flow → Higher thrust, Lower Isp
• Physics: T = ṁ × v_e × η_div

GEOMETRIC TRANSPARENCY (τ_geom):
• Units: Dimensionless (0.5 - 0.9)
• Effect: Higher transparency → Higher thrust
• Physics: A_open = A_grid × τ_geom

TRANSMISSION EFFICIENCY (τ_trans):
• Units: Dimensionless (0.8 - 1.0)
• Effect: Higher efficiency → Higher thrust
• Physics: Accounts for beam impingement losses

DIVERGENCE ANGLE (σ):
• Units: Degrees (°)
• Range: 1° - 45° (ion), 10° - 60° (Hall)
• Effect: Lower angle → Higher efficiency
• Physics: η_div = cos(σ) for RMS half-angle

ACCELERATION EFFICIENCY (η_acc) - Hall:
• Units: Dimensionless (0.4 - 0.8)
• Effect: Higher efficiency → Higher Isp
• Physics: v_e = √(η_acc × 2 × q × Vd / m_i)

PROPELLANT UTILIZATION (τ_prop) - Hall:
• Units: Dimensionless (0.7 - 0.95)
• Effect: Higher utilization → Higher thrust
• Physics: T = ṁ × τ_prop × v_e × η_div

PERVEANCE MARGIN (Ion Engine):
• Units: Dimensionless
• Safe Range: > 1.0
• Critical: < 1.0 (space-charge limited)
• Physics: I_CL / I_b (Child-Langmuir limit)

TROUBLESHOOTING TIPS:
─────────────────────

Low Thrust:
• Ion: Increase beam current or grid transparency
• Hall: Increase mass flow rate or propellant utilization

Low Isp:
• Ion: Increase acceleration voltage
• Hall: Increase discharge voltage or acceleration efficiency

Space-Charge Issues:
• Reduce beam current
• Increase grid gap distance
• Improve grid transparency

High Power Consumption:
• Reduce beam current (ion)
• Reduce discharge voltage (Hall)
• Optimize operating point

For detailed physics equations, see the Physics Guide tab.
        """

        help_window = tk.Toplevel(self.root)
        help_window.title("Parameter Help - Ionic Propulsion Lab")
        help_window.geometry("800x600")

        help_text_widget = scrolledtext.ScrolledText(
            help_window, font=("Arial", 10), wrap=tk.WORD)
        help_text_widget.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        help_text_widget.insert(tk.END, help_text)
        help_text_widget.config(state=tk.DISABLED)

        ttk.Button(
            help_window,
            text="Close",
            command=help_window.destroy).pack(
            pady=10)

    def create_emr_parameter_controls(self):
        """Create EMR Suit parameter controls"""
        if not EMR_AVAILABLE:
            return

        # EMR Suit Parameter Controls
        self.emr_frame = ttk.LabelFrame(
            self.left_panel,
            text="🦸 EMR Suit Parameters",
            padding=10)
        self.emr_frame.pack(fill=tk.X, pady=(0, 10))

        # Initialize EMR variables
        self.emr_current = tk.DoubleVar(value=100.0)  # Current (A)
        self.emr_distance = tk.DoubleVar(value=0.02)  # Distance (m)
        self.emr_temp_cold = tk.DoubleVar(value=270.0)  # Cold temperature (K)
        self.emr_temp_hot = tk.DoubleVar(value=310.0)  # Hot temperature (K)
        self.emr_flow_rate = tk.DoubleVar(value=1.2)  # Flow rate (kg/s)
        self.emr_safety_factor = tk.DoubleVar(value=3.0)  # Safety factor
        self.emr_risk_prob = tk.DoubleVar(value=1e-7)  # Risk probability
        self.emr_thrust = tk.DoubleVar(value=350.0)  # Thrust per pod (N)
        self.emr_power = tk.DoubleVar(value=2.5)  # Power per pod (kW)
        self.emr_efficiency = tk.DoubleVar(value=0.8)  # Efficiency

        # Current control
        ttk.Label(self.emr_frame, text="Coil Current (A)",
                  font=("Arial", 10, "bold")).pack(anchor=tk.W)
        current_frame = ttk.Frame(self.emr_frame)
        current_frame.pack(fill=tk.X, pady=(0, 10))

        current_scale = ttk.Scale(
            current_frame,
            from_=10,
            to=200,
            variable=self.emr_current,
            orient=tk.HORIZONTAL,
            command=self.update_emr_calculations)
        current_scale.pack(side=tk.LEFT, fill=tk.X, expand=True)

        ttk.Label(
            current_frame,
            textvariable=self.emr_current,
            width=8).pack(side=tk.RIGHT)

        ttk.Label(self.emr_frame, text="A (amperes)",
                  foreground="yellow").pack(anchor=tk.W, padx=(0, 5))

        # Distance control
        ttk.Label(self.emr_frame, text="Coil Distance (m)",
                  font=("Arial", 10, "bold")).pack(anchor=tk.W)
        distance_frame = ttk.Frame(self.emr_frame)
        distance_frame.pack(fill=tk.X, pady=(0, 10))

        distance_scale = ttk.Scale(
            distance_frame,
            from_=0.005,
            to=0.1,
            variable=self.emr_distance,
            orient=tk.HORIZONTAL,
            command=self.update_emr_calculations)
        distance_scale.pack(side=tk.LEFT, fill=tk.X, expand=True)

        ttk.Label(
            distance_frame,
            textvariable=self.emr_distance,
            width=8).pack(side=tk.RIGHT)

        ttk.Label(self.emr_frame, text="m (meters)",
                  foreground="yellow").pack(anchor=tk.W, padx=(0, 5))

        # Temperature controls
        ttk.Label(self.emr_frame, text="Thermal Parameters",
                  font=("Arial", 10, "bold")).pack(anchor=tk.W, pady=(10, 5))

        # Cold temperature
        ttk.Label(self.emr_frame, text="Cold Temperature (K)").pack(anchor=tk.W)
        cold_temp_frame = ttk.Frame(self.emr_frame)
        cold_temp_frame.pack(fill=tk.X, pady=(0, 5))

        cold_temp_scale = ttk.Scale(
            cold_temp_frame,
            from_=250,
            to=290,
            variable=self.emr_temp_cold,
            orient=tk.HORIZONTAL,
            command=self.update_emr_calculations)
        cold_temp_scale.pack(side=tk.LEFT, fill=tk.X, expand=True)

        ttk.Label(
            cold_temp_frame,
            textvariable=self.emr_temp_cold,
            width=8).pack(side=tk.RIGHT)

        # Hot temperature
        ttk.Label(self.emr_frame, text="Hot Temperature (K)").pack(anchor=tk.W)
        hot_temp_frame = ttk.Frame(self.emr_frame)
        hot_temp_frame.pack(fill=tk.X, pady=(0, 10))

        hot_temp_scale = ttk.Scale(
            hot_temp_frame,
            from_=300,
            to=320,
            variable=self.emr_temp_hot,
            orient=tk.HORIZONTAL,
            command=self.update_emr_calculations)
        hot_temp_scale.pack(side=tk.LEFT, fill=tk.X, expand=True)

        ttk.Label(
            hot_temp_frame,
            textvariable=self.emr_temp_hot,
            width=8).pack(side=tk.RIGHT)

        # Flow rate control
        ttk.Label(self.emr_frame, text="Propellant Flow Rate (kg/s)",
                  font=("Arial", 10, "bold")).pack(anchor=tk.W)
        flow_frame = ttk.Frame(self.emr_frame)
        flow_frame.pack(fill=tk.X, pady=(0, 10))

        flow_scale = ttk.Scale(
            flow_frame,
            from_=0.5,
            to=2.0,
            variable=self.emr_flow_rate,
            orient=tk.HORIZONTAL,
            command=self.update_emr_calculations)
        flow_scale.pack(side=tk.LEFT, fill=tk.X, expand=True)

        ttk.Label(
            flow_frame,
            textvariable=self.emr_flow_rate,
            width=8).pack(side=tk.RIGHT)

        ttk.Label(self.emr_frame, text="kg/s (kilograms per second)",
                  foreground="yellow").pack(anchor=tk.W, padx=(0, 5))

        # Safety parameters
        ttk.Label(self.emr_frame, text="Safety Parameters",
                  font=("Arial", 10, "bold")).pack(anchor=tk.W, pady=(10, 5))

        # Safety factor
        ttk.Label(self.emr_frame, text="Safety Factor").pack(anchor=tk.W)
        safety_frame = ttk.Frame(self.emr_frame)
        safety_frame.pack(fill=tk.X, pady=(0, 5))

        safety_scale = ttk.Scale(
            safety_frame,
            from_=2.0,
            to=5.0,
            variable=self.emr_safety_factor,
            orient=tk.HORIZONTAL,
            command=self.update_emr_calculations)
        safety_scale.pack(side=tk.LEFT, fill=tk.X, expand=True)

        ttk.Label(
            safety_frame,
            textvariable=self.emr_safety_factor,
            width=8).pack(side=tk.RIGHT)

        # Risk probability
        ttk.Label(self.emr_frame, text="Risk Probability").pack(anchor=tk.W)
        risk_frame = ttk.Frame(self.emr_frame)
        risk_frame.pack(fill=tk.X, pady=(0, 10))

        risk_scale = ttk.Scale(
            risk_frame,
            from_=1e-8,
            to_=1e-5,
            variable=self.emr_risk_prob,
            orient=tk.HORIZONTAL,
            command=self.update_emr_calculations)
        risk_scale.pack(side=tk.LEFT, fill=tk.X, expand=True)

        ttk.Label(
            risk_frame,
            textvariable=self.emr_risk_prob,
            width=12).pack(side=tk.RIGHT)

        # Performance parameters
        ttk.Label(self.emr_frame, text="Performance Parameters",
                  font=("Arial", 10, "bold")).pack(anchor=tk.W, pady=(10, 5))

        # Thrust per pod
        ttk.Label(self.emr_frame, text="Thrust per Pod (N)").pack(anchor=tk.W)
        thrust_frame = ttk.Frame(self.emr_frame)
        thrust_frame.pack(fill=tk.X, pady=(0, 5))

        thrust_scale = ttk.Scale(
            thrust_frame,
            from_=200,
            to=500,
            variable=self.emr_thrust,
            orient=tk.HORIZONTAL,
            command=self.update_emr_calculations)
        thrust_scale.pack(side=tk.LEFT, fill=tk.X, expand=True)

        ttk.Label(
            thrust_frame,
            textvariable=self.emr_thrust,
            width=8).pack(side=tk.RIGHT)

        # Power per pod
        ttk.Label(self.emr_frame, text="Power per Pod (kW)").pack(anchor=tk.W)
        power_frame = ttk.Frame(self.emr_frame)
        power_frame.pack(fill=tk.X, pady=(0, 5))

        power_scale = ttk.Scale(
            power_frame,
            from_=1.5,
            to_=4.0,
            variable=self.emr_power,
            orient=tk.HORIZONTAL,
            command=self.update_emr_calculations)
        power_scale.pack(side=tk.LEFT, fill=tk.X, expand=True)

        ttk.Label(
            power_frame,
            textvariable=self.emr_power,
            width=8).pack(side=tk.RIGHT)

        # Efficiency
        ttk.Label(self.emr_frame, text="System Efficiency").pack(anchor=tk.W)
        efficiency_frame = ttk.Frame(self.emr_frame)
        efficiency_frame.pack(fill=tk.X, pady=(0, 10))

        efficiency_scale = ttk.Scale(
            efficiency_frame,
            from_=0.6,
            to_=0.9,
            variable=self.emr_efficiency,
            orient=tk.HORIZONTAL,
            command=self.update_emr_calculations)
        efficiency_scale.pack(side=tk.LEFT, fill=tk.X, expand=True)

        ttk.Label(
            efficiency_frame,
            textvariable=self.emr_efficiency,
            width=8).pack(side=tk.RIGHT)

        # EMR control buttons
        emr_button_frame = ttk.Frame(self.emr_frame)
        emr_button_frame.pack(fill=tk.X, pady=(10, 0))

        ttk.Button(
            emr_button_frame,
            text="🔄 Update EMR",
            command=self.update_emr_calculations).pack(
            fill=tk.X,
            pady=(0, 5))

        ttk.Button(
            emr_button_frame,
            text="📊 Start Flight Logging",
            command=self.start_emr_flight_logging).pack(
            fill=tk.X,
            pady=(0, 5))

        ttk.Button(
            emr_button_frame,
            text="🛑 Stop Flight Logging",
            command=self.stop_emr_flight_logging).pack(
            fill=tk.X)

    def update_emr_calculations(self, *args):
        """Update EMR calculations when parameters change"""
        if not EMR_AVAILABLE or not hasattr(self, 'emr_viz'):
            return

        try:
            # Generate new EMR data based on current parameters
            emr_data = self.generate_emr_data_from_params()

            # Update EMR visualization
            self.emr_viz.create_main_visualization(self.emr_figure, emr_data)
            self.emr_canvas.draw()

            # Update EMR metrics display
            self.update_emr_metrics_display(emr_data)

            # Update alerts
            self.update_emr_alerts(emr_data)

            # Log data if flight logging is active
            if hasattr(self, 'emr_flight_logging') and self.emr_flight_logging:
                self.emr_viz.log_data(emr_data)

        except Exception as e:
            print(f"EMR calculation error: {e}")

    def generate_emr_data_from_params(self):
        """Generate EMR data based on current parameter settings"""
        # Use physics formulas to generate realistic data
        I = self.emr_current.get()
        d = self.emr_distance.get()
        Tc = self.emr_temp_cold.get()
        Th = self.emr_temp_hot.get()
        flow_rate = self.emr_flow_rate.get()
        sf = self.emr_safety_factor.get()
        risk = self.emr_risk_prob.get()
        thrust = self.emr_thrust.get()
        power = self.emr_power.get()
        efficiency = self.emr_efficiency.get()

        # Calculate EMR force using physics formula: FEMR = μ0*I²/(2π*d)
        mu0 = 4 * np.pi * 1e-7
        femr = mu0 * I**2 / (2 * np.pi * d)

        # Calculate thermal efficiency: η = 1 - Tc/Th
        thermal_eff = 1 - Tc/Th

        # Generate data for 6 body regions
        femr_data = np.random.normal(femr, femr * 0.1, 6)
        thermal_data = {
            'Tc': np.random.normal(Tc, 5, 6),
            'Th': np.random.normal(Th, 5, 6),
            'eta': np.random.normal(thermal_eff, 0.05, 6)
        }

        # Generate flow rate data for 5 thrust pods
        flow_data = np.random.normal(flow_rate, flow_rate * 0.1, 5)

        # Safety data
        safety_data = {
            'sf': np.random.normal(sf, sf * 0.1, 6),
            'risk': np.random.normal(risk, risk * 0.5, 6)
        }

        # Performance data
        performance_data = {
            'thrust': np.random.normal(thrust, thrust * 0.05, 5),
            'power': np.random.normal(power, power * 0.05, 5),
            'efficiency': np.random.normal(efficiency, efficiency * 0.05, 5)
        }

        return {
            'femr': femr_data,
            'thermal': thermal_data,
            'flow_rate': flow_data,
            'safety': safety_data,
            'performance': performance_data,
            'timestamp': datetime.now()
        }

    def create_emr_visualization(self, parent):
        """Create EMR Suit visualization tab with scrollable layout"""
        if not EMR_AVAILABLE:
            ttk.Label(parent, text="EMR Suit Visualization not available",
                     font=("Arial", 12)).pack(expand=True)
            return

        # Initialize EMR visualization
        self.emr_viz = EMRVisualization()
        self.emr_flight_logging = False

        # Create scrollable frame for EMR content
        emr_canvas = tk.Canvas(parent, bg='#f0f0f0')
        emr_scrollbar = ttk.Scrollbar(parent, orient="vertical", command=emr_canvas.yview)
        emr_scrollable_frame = ttk.Frame(emr_canvas)

        emr_scrollable_frame.bind(
            "<Configure>",
            lambda e: emr_canvas.configure(scrollregion=emr_canvas.bbox("all"))
        )

        emr_canvas.create_window((0, 0), window=emr_scrollable_frame, anchor="nw")
        emr_canvas.configure(yscrollcommand=emr_scrollbar.set)

        # Pack the scrollable components
        emr_canvas.pack(side="left", fill="both", expand=True)
        emr_scrollbar.pack(side="right", fill="y")

        # Bind mousewheel to canvas
        def _on_emr_mousewheel(event):
            emr_canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        emr_canvas.bind_all("<MouseWheel>", _on_emr_mousewheel)

        # EMR visualization canvas (larger for better visibility)
        self.emr_figure = plt.Figure(figsize=(14, 10), dpi=100)
        self.emr_canvas = FigureCanvasTkAgg(self.emr_figure, emr_scrollable_frame)
        self.emr_canvas.get_tk_widget().pack(fill=tk.X, pady=(10, 0))

        # EMR controls and metrics
        emr_control_frame = ttk.Frame(emr_scrollable_frame)
        emr_control_frame.pack(fill=tk.X, pady=(10, 0))

        # View switch button
        ttk.Button(
            emr_control_frame,
            text="🔄 Switch View (Front/Back)",
            command=self.switch_emr_view).pack(side=tk.LEFT, padx=(0, 10))

        # Manual update button
        ttk.Button(
            emr_control_frame,
            text="🔄 Manual Update",
            command=self.manual_emr_update).pack(side=tk.LEFT, padx=(0, 10))

        # Save data button
        ttk.Button(
            emr_control_frame,
            text="💾 Save EMR Data",
            command=self.save_emr_data).pack(side=tk.LEFT, padx=(0, 10))

        # EMR metrics display
        emr_metrics_frame = ttk.LabelFrame(emr_scrollable_frame, text="EMR Real-Time Metrics", padding=10)
        emr_metrics_frame.pack(fill=tk.X, pady=(10, 0))

        # Create metrics display
        self.emr_metrics_vars = {}
        emr_metrics = [
            ('EMR Force (N)', 'emr_force'),
            ('Thermal Eff. (%)', 'thermal_eff'),
            ('Flow Rate (kg/s)', 'flow_rate'),
            ('Safety Factor', 'safety_factor'),
            ('Risk Prob.', 'risk_prob'),
            ('Thrust (N)', 'thrust'),
            ('Power (kW)', 'power'),
            ('Efficiency (%)', 'efficiency')
        ]

        emr_metrics_grid = ttk.Frame(emr_metrics_frame)
        emr_metrics_grid.pack(fill=tk.X)

        for i, (label, key) in enumerate(emr_metrics):
            ttk.Label(emr_metrics_grid, text=f"{label}:").grid(row=i//4, column=(i%4)*2, sticky='w', padx=(0,5))
            self.emr_metrics_vars[key] = ttk.Label(emr_metrics_grid, text="--", font=('Arial', 9, 'bold'))
            self.emr_metrics_vars[key].grid(row=i//4, column=(i%4)*2+1, sticky='w')

        # EMR alerts display
        emr_alerts_frame = ttk.LabelFrame(emr_scrollable_frame, text="EMR System Alerts", padding=10)
        emr_alerts_frame.pack(fill=tk.X, pady=(10, 0))

        self.emr_alert_text = tk.Text(emr_alerts_frame, height=3, wrap=tk.WORD,
                                    bg=self.dark_colors['bg_secondary'], fg='red', font=('Arial', 9))
        self.emr_alert_text.pack(fill=tk.X)
        self.emr_alert_text.insert(tk.END, "EMR system initializing... No alerts at this time.")
        self.emr_alert_text.config(state=tk.DISABLED)

        # Initial EMR visualization
        emr_data = self.generate_emr_data_from_params()
        self.emr_viz.create_main_visualization(self.emr_figure, emr_data)
        self.emr_canvas.draw()

        # Update EMR metrics
        self.update_emr_metrics_display(emr_data)
        self.update_emr_alerts(emr_data)

    def switch_emr_view(self):
        """Switch between front and back EMR suit views"""
        if EMR_AVAILABLE and hasattr(self, 'emr_viz'):
            if self.emr_viz.current_view == 'front':
                self.emr_viz.current_view = 'back'
            else:
                self.emr_viz.current_view = 'front'

            # Update visualization
            emr_data = self.generate_emr_data_from_params()
            self.emr_viz.create_main_visualization(self.emr_figure, emr_data)
            self.emr_canvas.draw()

    def manual_emr_update(self):
        """Perform manual EMR data update"""
        if EMR_AVAILABLE:
            emr_data = self.generate_emr_data_from_params()
            self.emr_viz.create_main_visualization(self.emr_figure, emr_data)
            self.emr_canvas.draw()
            self.update_emr_metrics_display(emr_data)
            self.update_emr_alerts(emr_data)

    def save_emr_data(self):
        """Save EMR logged data to CSV"""
        if EMR_AVAILABLE and hasattr(self, 'emr_viz'):
            try:
                self.emr_viz.save_log_to_csv()
                messagebox.showinfo("Success", "EMR data saved successfully to emr_suit_log.csv")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save EMR data: {e}")

    def update_emr_metrics_display(self, data):
        """Update EMR metrics display"""
        if not hasattr(self, 'emr_metrics_vars'):
            return

        metrics_updates = {
            'emr_force': f"{data['femr'].mean():.2f}",
            'thermal_eff': f"{data['thermal']['eta'].mean()*100:.1f}",
            'flow_rate': f"{data['flow_rate'].mean():.2f}",
            'safety_factor': f"{data['safety']['sf'].mean():.2f}",
            'risk_prob': f"{data['safety']['risk'].max():.2e}",
            'thrust': f"{data['performance']['thrust'].mean():.0f}",
            'power': f"{data['performance']['power'].mean():.2f}",
            'efficiency': f"{data['performance']['efficiency'].mean()*100:.1f}"
        }

        for key, value in metrics_updates.items():
            if key in self.emr_metrics_vars:
                self.emr_metrics_vars[key].config(text=value)

    def update_emr_alerts(self, data):
        """Update EMR alerts display"""
        if not hasattr(self, 'emr_alert_text'):
            return

        alerts = self.emr_viz.create_alert_system(data)

        self.emr_alert_text.config(state=tk.NORMAL)
        self.emr_alert_text.delete(1.0, tk.END)

        if alerts:
            alert_text = "\n".join(alerts)
            self.emr_alert_text.insert(tk.END, alert_text)
            self.emr_alert_text.config(fg='red')
        else:
            self.emr_alert_text.insert(tk.END, "EMR system operating normally. No alerts.")
            self.emr_alert_text.config(fg='green')

        self.emr_alert_text.config(state=tk.DISABLED)

    def start_emr_flight_logging(self):
        """Start EMR flight logging"""
        if EMR_AVAILABLE:
            self.emr_flight_logging = True
            self.status_var.set("✅ EMR flight logging started")
            messagebox.showinfo("Flight Logging", "EMR flight logging has been started.\nData will be logged every update cycle.")

    def stop_emr_flight_logging(self):
        """Stop EMR flight logging"""
        if EMR_AVAILABLE:
            self.emr_flight_logging = False
            self.status_var.set("🛑 EMR flight logging stopped")
            messagebox.showinfo("Flight Logging", "EMR flight logging has been stopped.\nData has been saved to emr_suit_log.csv")

    def show_about(self):
        """Show about dialog"""
        about_text = """
🚀 Enhanced Ionic Propulsion Lab
═══════════════════════════════════════════════════════════════════════════════

Version: 2.0 - Advanced Physics Edition
Platform: Cross-platform (Windows, macOS, Linux)

FEATURES:
• Real-time ion engine and Hall thruster calculations
• Space-charge effects (Child-Langmuir limit)
• Comprehensive loss modeling
• Interactive parameter adjustment
• Professional plotting capabilities
• EMR Suit Visualization and monitoring
• Complete documentation and guides

PHYSICS MODELS:
• Ion Engine: Grid transparency, beam divergence, space-charge
• Hall Thruster: Acceleration efficiency, propellant utilization
• EMR Suit: Electromagnetic resonance, thermal management
• Divergence: Cosine and Gaussian models
• Multi-gas support: Xenon, Iodine, Krypton, Argon, Water

DEVELOPMENT:
• Built with Python and Tkinter
• Advanced physics calculations
• Error handling and validation
• User-friendly interface design

CONTACT & SUPPORT:
• Documentation: README.md, USER_GUIDE.md
• Diagnostics: Run diagnostics.py
• Web Interface: viz/index.html

For questions or issues, check the documentation first.
        """

        messagebox.showinfo("About Ionic Propulsion Lab", about_text)


def main():
    """Main application entry point"""
    root = tk.Tk()
    app = IonicPropulsionGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
