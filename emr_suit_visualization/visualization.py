import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.patches import Circle
from matplotlib.colors import LinearSegmentedColormap
import matplotlib.gridspec as gridspec
from scipy import interpolate
import sympy as sp
import pandas as pd
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

from body_model import EMRBodyModel

class EMRVisualization:
    """
    Core visualization class for EMR Suit monitoring system
    """

    def __init__(self):
        self.body_model = EMRBodyModel()
        self.data_log = []
        self.current_view = 'front'

        # Physics constants
        self.mu0 = 4 * np.pi * 1e-7  # Permeability of free space
        self.k = 1.380649e-23  # Boltzmann constant

        # Custom colormap for heatmaps
        self.heatmap_cmap = LinearSegmentedColormap.from_list(
            "emr_heatmap", ["blue", "cyan", "green", "yellow", "red"]
        )

    def generate_emr_data(self):
        """
        Generate simulated EMR suit data using physics formulas
        """
        # Current through coils (A)
        I = np.random.uniform(50, 150, 6)  # 6 body regions

        # Distance from coils (m)
        d = np.random.uniform(0.01, 0.05, 6)

        # EMR force calculation: FEMR = μ0*I²/(2π*d)
        femr = self.mu0 * I**2 / (2 * np.pi * d)

        # Thermal data
        Tc = np.random.uniform(250, 290, 6)  # Cold temperature (K)
        Th = np.random.uniform(300, 320, 6)  # Hot temperature (K)
        eta = 1 - Tc/Th  # Efficiency

        # Propellant flow (kg/s)
        flow_rate = np.random.uniform(1.0, 1.5, 5)  # 5 thrust pods

        # Safety metrics
        sf = np.random.uniform(2, 4, 6)  # Safety factor
        risk_prob = np.random.uniform(1e-8, 1e-6, 6)  # Risk probability

        # Thrust and power
        thrust = np.random.uniform(250, 450, 5)  # N per pod
        power = np.random.uniform(2.0, 3.0, 5)  # kW per pod
        efficiency = np.random.uniform(0.7, 0.85, 5)  # Efficiency

        return {
            'femr': femr,
            'thermal': {'Tc': Tc, 'Th': Th, 'eta': eta},
            'flow_rate': flow_rate,
            'safety': {'sf': sf, 'risk': risk_prob},
            'performance': {'thrust': thrust, 'power': power, 'efficiency': efficiency},
            'timestamp': datetime.now()
        }

    def create_heatmap_overlay(self, ax, data, regions):
        """
        Create 2D human body heatmap overlay
        """
        # Create grid for interpolation
        x = np.linspace(0, 1, 100)
        y = np.linspace(0, 1, 100)
        X, Y = np.meshgrid(x, y)

        # Initialize data grid
        Z = np.zeros((100, 100))

        # Map data to body regions
        region_names = list(regions.keys())
        for i, region in enumerate(region_names):
            x_range = regions[region]['x']
            y_range = regions[region]['y']

            # Create mask for region
            mask_x = (X >= x_range[0]) & (X <= x_range[1])
            mask_y = (Y >= y_range[0]) & (Y <= y_range[1])
            mask = mask_x & mask_y

            # Apply data to region
            if i < len(data):
                Z[mask] = data[i]

        # Smooth the data
        Z_smooth = interpolate.interp2d(x, y, Z, kind='cubic')(x, y)

        # Create heatmap
        heatmap = ax.contourf(X, Y, Z_smooth, levels=20, cmap=self.heatmap_cmap, alpha=0.7)
        plt.colorbar(heatmap, ax=ax, label='EM Field Strength (N)')

        return heatmap

    def create_vector_field(self, ax, data):
        """
        Create real-time field vector mapping
        """
        # Create vector field grid
        x = np.linspace(0.2, 0.8, 15)
        y = np.linspace(0.1, 0.9, 15)
        X, Y = np.meshgrid(x, y)

        # Generate vector components based on EMR physics
        U = np.sin(2 * np.pi * X) * np.cos(2 * np.pi * Y) * data['femr'].mean() / 1000
        V = np.cos(2 * np.pi * X) * np.sin(2 * np.pi * Y) * data['femr'].mean() / 1000

        # Plot vector field
        ax.quiver(X, Y, U, V, scale=50, color='purple', alpha=0.6, width=0.005)
        ax.set_title('EMR Force Vector Field', fontsize=12)

    def create_status_gauges(self, fig, data):
        """
        Create component status indicators
        """
        gs = gridspec.GridSpec(2, 3, figure=fig, left=0.1, right=0.9, top=0.9, bottom=0.1, hspace=0.3)

        # Thrust pods status
        ax1 = fig.add_subplot(gs[0, 0])
        pods = ['Arm L', 'Arm R', 'Leg L', 'Leg R', 'Back']
        thrust_values = data['performance']['thrust']
        colors = ['green' if t > 300 else 'yellow' if t > 200 else 'red' for t in thrust_values]

        bars = ax1.bar(pods, thrust_values, color=colors)
        ax1.set_ylabel('Thrust (N)')
        ax1.set_title('Thrust Pods Status')
        ax1.set_ylim(0, 500)

        # Add value labels
        for bar, value in zip(bars, thrust_values):
            ax1.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 10,
                    f'{value:.0f}', ha='center', va='bottom')

        # Efficiency gauge
        ax2 = fig.add_subplot(gs[0, 1])
        efficiency = data['performance']['efficiency'].mean() * 100
        ax2.pie([efficiency, 100-efficiency], colors=['green', 'lightgray'],
               labels=[f'{efficiency:.1f}%', ''], startangle=90)
        ax2.set_title('System Efficiency')

        # Power consumption
        ax3 = fig.add_subplot(gs[0, 2])
        power_values = data['performance']['power']
        ax3.plot(pods, power_values, 'ro-', linewidth=2, markersize=8)
        ax3.set_ylabel('Power (kW)')
        ax3.set_title('Power Draw per Pod')
        ax3.grid(True, alpha=0.3)

        # Safety metrics
        ax4 = fig.add_subplot(gs[1, 0])
        sf_mean = data['safety']['sf'].mean()
        ax4.bar(['Safety Factor'], [sf_mean], color='blue')
        ax4.set_ylim(0, 5)
        ax4.axhline(y=2, color='red', linestyle='--', alpha=0.7, label='Minimum')
        ax4.legend()
        ax4.set_title('Safety Factor')

        # Risk probability
        ax5 = fig.add_subplot(gs[1, 1])
        risk_mean = data['safety']['risk'].mean()
        ax5.semilogy(['Risk Probability'], [risk_mean], 'rx', markersize=12)
        ax5.set_title('Risk Assessment')
        ax5.set_ylabel('Probability')
        ax5.grid(True, alpha=0.3)

        # Thermal efficiency
        ax6 = fig.add_subplot(gs[1, 2])
        thermal_eff = data['thermal']['eta'].mean() * 100
        ax6.pie([thermal_eff, 100-thermal_eff], colors=['cyan', 'lightgray'],
               labels=[f'{thermal_eff:.1f}%', ''], startangle=90)
        ax6.set_title('Thermal Efficiency')

    def create_thermal_contours(self, ax, data):
        """
        Create thermal contour plots
        """
        # Create temperature grid
        x = np.linspace(0, 1, 50)
        y = np.linspace(0, 1, 50)
        X, Y = np.meshgrid(x, y)

        # Generate temperature distribution
        T = 280 + 20 * np.sin(2 * np.pi * X) * np.cos(2 * np.pi * Y)
        T += np.random.normal(0, 5, T.shape)  # Add noise

        # Create contours
        contours = ax.contour(X, Y, T, levels=15, cmap='coolwarm')
        ax.clabel(contours, inline=True, fontsize=8)
        ax.set_title('Thermal Distribution (°K)', fontsize=12)
        plt.colorbar(contours, ax=ax, label='Temperature (K)')

    def create_flow_visualization(self, ax, data):
        """
        Create propellant flow visualization
        """
        # Create flow field
        x = np.linspace(0.3, 0.7, 20)
        y = np.linspace(0.2, 0.8, 20)
        X, Y = np.meshgrid(x, y)

        # Flow vectors (simulating ionized seawater flow)
        U = np.ones_like(X) * 0.5  # Horizontal flow
        V = np.zeros_like(Y)  # No vertical component

        # Add some turbulence
        U += 0.2 * np.sin(4 * np.pi * X) * np.cos(4 * np.pi * Y)
        V += 0.1 * np.sin(4 * np.pi * X) * np.sin(4 * np.pi * Y)

        # Scale by flow rate
        flow_scale = data['flow_rate'].mean()
        U *= flow_scale
        V *= flow_scale

        # Plot streamlines
        ax.streamplot(X, Y, U, V, density=1.5, color='blue', linewidth=1, arrowsize=1)
        ax.set_title('Propellant Flow (kg/s)', fontsize=12)
        ax.set_xlim(0.2, 0.8)
        ax.set_ylim(0.1, 0.9)

    def create_control_feedback(self, ax, data):
        """
        Create control system feedback graphs
        """
        time = np.linspace(0, 10, 100)
        t = np.linspace(0, 2*np.pi, 100)

        # DDSQA field composition
        phi_total = np.sum([0.3 * np.cos(2*np.pi*f*t + np.random.uniform(0, 2*np.pi))
                           for f in [1, 2, 3]], axis=0)

        ax.plot(time, phi_total, 'b-', linewidth=2, label='Φ_total(t)')
        ax.set_xlabel('Time (s)')
        ax.set_ylabel('Field Strength')
        ax.set_title('DDSQA Field Composition', fontsize=12)
        ax.grid(True, alpha=0.3)
        ax.legend()

    def create_alert_system(self, data):
        """
        Generate alerts based on safety thresholds
        """
        alerts = []

        # Check thermal limits
        if np.any(data['thermal']['Tc'] > 295):
            alerts.append("WARNING: Thermal exceedance detected!")

        # Check safety factor
        if np.any(data['safety']['sf'] < 2.5):
            alerts.append("CAUTION: Safety factor below threshold!")

        # Check risk probability
        if np.any(data['safety']['risk'] > 1e-6):
            alerts.append("ALERT: Risk probability elevated!")

        # Check thrust levels
        if np.any(data['performance']['thrust'] < 280):
            alerts.append("WARNING: Thrust below nominal levels!")

        return alerts

    def log_data(self, data):
        """
        Log metrics data for analysis
        """
        log_entry = {
            'timestamp': data['timestamp'],
            'mean_femr': data['femr'].mean(),
            'mean_thrust': data['performance']['thrust'].mean(),
            'mean_efficiency': data['performance']['efficiency'].mean(),
            'mean_power': data['performance']['power'].mean(),
            'mean_safety_factor': data['safety']['sf'].mean(),
            'max_risk': data['safety']['risk'].max(),
            'mean_thermal_eff': data['thermal']['eta'].mean(),
            'total_flow': data['flow_rate'].sum()
        }

        self.data_log.append(log_entry)

    def save_log_to_csv(self, filename='emr_suit_log.csv'):
        """
        Save logged data to CSV file
        """
        if self.data_log:
            df = pd.DataFrame(self.data_log)
            df.to_csv(filename, index=False)
            print(f"Data log saved to {filename}")

    def create_main_visualization(self, fig, data):
        """
        Create the main EMR suit visualization layout
        """
        fig.clear()

        # Create main grid layout
        gs = gridspec.GridSpec(3, 4, figure=fig, hspace=0.3, wspace=0.3)

        # Body model with heatmap
        ax_body = fig.add_subplot(gs[0:2, 0:2])
        self.body_model.create_body_silhouette(ax_body, self.current_view)
        regions = self.body_model.get_body_regions()
        self.create_heatmap_overlay(ax_body, data['femr'], regions)
        self.body_model.add_thrust_pods(ax_body)
        self.body_model.setup_plot(ax_body, "EMR Suit - Body Heatmap")

        # Vector field
        ax_vector = fig.add_subplot(gs[0, 2])
        self.create_vector_field(ax_vector, data)

        # Thermal contours
        ax_thermal = fig.add_subplot(gs[0, 3])
        self.create_thermal_contours(ax_thermal, data)

        # Flow visualization
        ax_flow = fig.add_subplot(gs[1, 2])
        self.create_flow_visualization(ax_flow, data)

        # Control feedback
        ax_control = fig.add_subplot(gs[1, 3])
        self.create_control_feedback(ax_control, data)

        # Status gauges (bottom row)
        self.create_status_gauges(fig, data)

        # Add alerts
        alerts = self.create_alert_system(data)
        if alerts:
            alert_text = "\n".join(alerts)
            fig.text(0.02, 0.02, f"ALERTS:\n{alert_text}",
                    fontsize=10, color='red', fontweight='bold',
                    bbox=dict(boxstyle="round,pad=0.3", facecolor="yellow", alpha=0.8))

        plt.tight_layout()
