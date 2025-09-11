import tkinter as tk
from tkinter import ttk, messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.animation import FuncAnimation
import threading
import time
import os
import sys

from visualization import EMRVisualization

class EMRGUIApp:
    """
    Main GUI application for EMR Suit Visualization Software
    """

    def __init__(self, root):
        self.root = root
        self.root.title("EMR Suit Visualization Software v1.0")
        self.root.geometry("1400x900")
        self.root.configure(bg='#f0f0f0')

        # Initialize visualization system
        self.viz = EMRVisualization()
        self.is_running = True
        self.animation = None

        # Create GUI components
        self.create_widgets()

        # Start real-time updates
        self.start_real_time_updates()

        # Handle window close
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

    def create_widgets(self):
        """
        Create all GUI widgets and layout
        """
        # Main frame
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Title
        title_label = ttk.Label(main_frame, text="EMR Suit Monitoring System",
                               font=('Arial', 16, 'bold'))
        title_label.pack(pady=(0, 10))

        # Control panel
        control_frame = ttk.LabelFrame(main_frame, text="Controls", padding=10)
        control_frame.pack(fill=tk.X, pady=(0, 10))

        # Buttons
        button_frame = ttk.Frame(control_frame)
        button_frame.pack(fill=tk.X)

        self.view_button = ttk.Button(button_frame, text="Switch View (Front/Back)",
                                    command=self.switch_view)
        self.view_button.pack(side=tk.LEFT, padx=(0, 10))

        self.update_button = ttk.Button(button_frame, text="Manual Update",
                                       command=self.manual_update)
        self.update_button.pack(side=tk.LEFT, padx=(0, 10))

        self.save_button = ttk.Button(button_frame, text="Save Data Log",
                                    command=self.save_data_log)
        self.save_button.pack(side=tk.LEFT, padx=(0, 10))

        # Status indicators
        status_frame = ttk.Frame(control_frame)
        status_frame.pack(fill=tk.X, pady=(10, 0))

        ttk.Label(status_frame, text="System Status:").pack(side=tk.LEFT)
        self.status_label = ttk.Label(status_frame, text="Initializing...",
                                     foreground="orange", font=('Arial', 10, 'bold'))
        self.status_label.pack(side=tk.LEFT, padx=(5, 0))

        # Alert panel
        alert_frame = ttk.LabelFrame(main_frame, text="System Alerts", padding=10)
        alert_frame.pack(fill=tk.X, pady=(0, 10))

        self.alert_text = tk.Text(alert_frame, height=3, wrap=tk.WORD,
                                 bg='#fffacd', fg='red', font=('Arial', 9))
        self.alert_text.pack(fill=tk.X)
        self.alert_text.insert(tk.END, "System initializing... No alerts at this time.")
        self.alert_text.config(state=tk.DISABLED)

        # Metrics display
        metrics_frame = ttk.LabelFrame(main_frame, text="Real-time Metrics", padding=10)
        metrics_frame.pack(fill=tk.X, pady=(0, 10))

        # Create metrics labels
        self.metrics_vars = {}
        metrics = [
            ('EMR Force (N)', 'emr_force'),
            ('Thrust (N)', 'thrust'),
            ('Efficiency (%)', 'efficiency'),
            ('Power (kW)', 'power'),
            ('Safety Factor', 'safety'),
            ('Risk Prob.', 'risk'),
            ('Thermal Eff. (%)', 'thermal'),
            ('Flow Rate (kg/s)', 'flow')
        ]

        metrics_grid = ttk.Frame(metrics_frame)
        metrics_grid.pack(fill=tk.X)

        for i, (label, key) in enumerate(metrics):
            ttk.Label(metrics_grid, text=f"{label}:").grid(row=i//4, column=(i%4)*2, sticky='w', padx=(0,5))
            self.metrics_vars[key] = ttk.Label(metrics_grid, text="--", font=('Arial', 9, 'bold'))
            self.metrics_vars[key].grid(row=i//4, column=(i%4)*2+1, sticky='w')

        # Matplotlib figure
        self.figure = plt.Figure(figsize=(14, 8), dpi=100)
        self.canvas = FigureCanvasTkAgg(self.figure, master=main_frame)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

        # Initial data generation and plot
        self.current_data = self.viz.generate_emr_data()
        self.viz.create_main_visualization(self.figure, self.current_data)
        self.canvas.draw()

    def switch_view(self):
        """
        Switch between front and back body views
        """
        if self.viz.current_view == 'front':
            self.viz.current_view = 'back'
            self.view_button.config(text="Switch View (Back/Front)")
        else:
            self.viz.current_view = 'front'
            self.view_button.config(text="Switch View (Front/Back)")

        # Update visualization
        self.viz.create_main_visualization(self.figure, self.current_data)
        self.canvas.draw()

    def manual_update(self):
        """
        Perform manual data update
        """
        self.current_data = self.viz.generate_emr_data()
        self.update_display()
        self.status_label.config(text="Manual update completed", foreground="green")

    def update_display(self):
        """
        Update the visualization display with new data
        """
        self.viz.create_main_visualization(self.figure, self.current_data)
        self.canvas.draw()

        # Update metrics display
        self.update_metrics_display()

        # Update alerts
        self.update_alerts()

        # Log data
        self.viz.log_data(self.current_data)

    def update_metrics_display(self):
        """
        Update the metrics display labels
        """
        data = self.current_data

        metrics_updates = {
            'emr_force': f"{data['femr'].mean():.2f}",
            'thrust': f"{data['performance']['thrust'].mean():.0f}",
            'efficiency': f"{data['performance']['efficiency'].mean()*100:.1f}",
            'power': f"{data['performance']['power'].mean():.2f}",
            'safety': f"{data['safety']['sf'].mean():.2f}",
            'risk': f"{data['safety']['risk'].max():.2e}",
            'thermal': f"{data['thermal']['eta'].mean()*100:.1f}",
            'flow': f"{data['flow_rate'].sum():.2f}"
        }

        for key, value in metrics_updates.items():
            self.metrics_vars[key].config(text=value)

    def update_alerts(self):
        """
        Update the alerts display
        """
        alerts = self.viz.create_alert_system(self.current_data)

        self.alert_text.config(state=tk.NORMAL)
        self.alert_text.delete(1.0, tk.END)

        if alerts:
            alert_text = "\n".join(alerts)
            self.alert_text.insert(tk.END, alert_text)
            self.alert_text.config(fg='red')
            self.status_label.config(text="ALERTS ACTIVE", foreground="red")
        else:
            self.alert_text.insert(tk.END, "System operating normally. No alerts.")
            self.alert_text.config(fg='green')
            self.status_label.config(text="SYSTEM NORMAL", foreground="green")

        self.alert_text.config(state=tk.DISABLED)

    def start_real_time_updates(self):
        """
        Start real-time data updates
        """
        def update_loop():
            while self.is_running:
                try:
                    self.current_data = self.viz.generate_emr_data()
                    # Update on main thread
                    self.root.after(0, self.update_display)
                    time.sleep(5)  # Update every 5 seconds
                except Exception as e:
                    print(f"Update error: {e}")
                    time.sleep(1)

        # Start update thread
        self.update_thread = threading.Thread(target=update_loop, daemon=True)
        self.update_thread.start()

        # Set status
        self.root.after(1000, lambda: self.status_label.config(text="SYSTEM NORMAL", foreground="green"))

    def save_data_log(self):
        """
        Save the data log to CSV file
        """
        try:
            self.viz.save_log_to_csv()
            messagebox.showinfo("Success", "Data log saved successfully to emr_suit_log.csv")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save data log: {e}")

    def on_closing(self):
        """
        Handle window close event
        """
        self.is_running = False

        # Save data log before closing
        try:
            self.viz.save_log_to_csv()
        except:
            pass

        self.root.destroy()

def main():
    """
    Main application entry point
    """
    # Set matplotlib backend for Tkinter
    plt.switch_backend('TkAgg')

    # Create root window
    root = tk.Tk()

    # Create application
    app = EMRGUIApp(root)

    # Start main loop
    root.mainloop()

if __name__ == "__main__":
    main()
