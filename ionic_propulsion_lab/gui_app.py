
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


class IonicPropulsionGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("🚀 Enhanced Ionic Propulsion Lab")
        self.root.geometry("1400x900")
        self.root.minsize(1200, 800)

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

        # Initialize the GUI components
        self.create_menu()
        self.create_main_layout()
        self.create_parameter_controls()
        self.create_results_display()
        self.initialize_calculator()

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

        # Left panel - Controls
        left_panel = ttk.Frame(main_frame, width=400)
        left_panel.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 10))

        # Right panel - Results
        right_panel = ttk.Frame(main_frame)
        right_panel.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        self.left_panel = left_panel
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
                  foreground="blue").pack(anchor=tk.W, padx=(0, 5))

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
                  foreground="blue").pack(anchor=tk.W, padx=(0, 5))

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
                  foreground="blue").pack(anchor=tk.W, padx=(0, 5))

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
                  foreground="blue").pack(anchor=tk.W, padx=(0, 5))

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
                  foreground="blue").pack(anchor=tk.W, padx=(0, 5))

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
                  foreground="blue").pack(anchor=tk.W, padx=(0, 5))

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
• Web-based visualization interface
• Complete documentation and guides

PHYSICS MODELS:
• Ion Engine: Grid transparency, beam divergence, space-charge
• Hall Thruster: Acceleration efficiency, propellant utilization
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
