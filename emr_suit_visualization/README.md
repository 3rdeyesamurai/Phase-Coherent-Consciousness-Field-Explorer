# EMR Suit Visualization Software

This software provides comprehensive real-time visualization for EMR (Electromagnetic Resonance) Suit systems, designed for monitoring and analysis of suit performance in various environments including deep-sea, atmospheric, and exoatmospheric flight.

## Features Implemented

### Visualization Methods
- **2D Human Body Heatmap Overlay**: Displays EM field strength using FEMR = μ0I²/2πd approximations, thermal distribution, and propulsion readiness across suit sections using color-coded heatmaps.
- **Real-Time Field Vector Mapping**: Plots vector fields showing Lorentz force F = q(E + v × B) and EMR force FEMR = μ0I²/2πd, with thrust directionality and field stability.
- **Component Status Indicators**: Dynamic gauges/bar graphs for EMR Thrust Pods, Cryo Regulator, and Power Bus showing thrust (N), efficiency (70–85%), and power draw (2.5 kW/pod).
- **Thermal Contour Plots**: 2D contour plots displaying cryogenic temperatures using η = 1 - Tc/Th and boil-off suppression (ṁ = Q/hfg).
- **Propellant Flow Visualization**: Animated streamlines/particle traces for ionized seawater flow (1.0–1.5 kg/s) across suit pods.
- **Safety and Reliability Metrics Display**: Real-time safety factor (SF = 2–4), risk probability (< 10⁻⁶), and redundancy status (Rs = 1 - (1 - e⁻λt)ⁿ).
- **Control System Feedback Loops**: Dynamic graphs for DDSQA field composition (Φtotal(t) = Σαi(t)cos(ωi(t)t + δi(t))) and MPC cost function (J = Σ(xkᵀQxk + ukᵀRuk)).
- **Validation Progress Tracker**: Checklist/progress bar for validation roadmap (EMR simulations, bench tests, manned certification).

### Advanced Features
- **Integration Stubs**: Placeholders for Meep (FDTD EM), gprMax (EM propagation), Elmer (thermal multiphysics), FEniCS (PDE vector fields), Palace (EM reliability).
- **Refined Body Model**: Highly detailed 2D silhouette with head (ellipse), neck, torso (trapezoid with rounded shoulders), arms/legs with joints (circles), outlines (Line2D), and thrust pods (red circles) for exoskeleton realism.
- **Physical Formula Integration**: Data generation uses physics formulas (FEMR = μ0I²/2πd, η = 1 - Tc/Th, ṁ = Q/hfg) with SymPy symbolic calculations for EMR force.
- **Real-Time Animation**: FuncAnimation for true dynamic updates (0.5s intervals) with enhanced heatmaps, alerts, and metrics overlays.
- **Thrust Pods Visualization**: Modular pod positions (arms, legs, back) with red indicators for cryo/power integration.
- **Enhanced Metrics & Alerts**: Real-time readiness checks, symbolic EMR force display, and dynamic alert system.
- **Scalable Architecture**: Modular design for easy integration of real simulation tools and multi-user deployment.

### Required Features
- **Real-Time Monitoring**: Continuous updates with simulated live sensor data.
- **Suit Readiness Checks**: Verification of EMR Thrust Pod functionality (thrust 250–450 N, noise < 20 dB), Cryo Regulator and Power Bus status (η ≈ 99%, power 2.5 kW/pod), safety margins (SF = 2–4, risk < 10⁻⁶).
- **Flight Continuity Assurance**: Simulation of fault tolerance (N+1 redundancy), fail-safe descent modes, propellant levels, and flow rates.
- **Alert System**: Highlights anomalies (thermal exceedance, field instability) with color changes and alerts.
- **Data Logging and Reporting**: Records metrics (Isp, η, noise) for post-flight analysis; saves to CSV.
- **User Interface**: Intuitive GUI with Tkinter for switching views, manual updates, and real-time alerts.
- **Scalability**: Python-based for easy extension to multi-user access and parallel processing.

## Installation

1. Ensure Python 3.13+ is installed.
2. Install required packages:
   ```
   pip install numpy matplotlib scipy pandas
   ```
3. Navigate to the project directory:
   ```
   cd EMR_Suit_Visualization
   ```
4. Run the application:
   ```
   python main.py
   ```

## Usage

- **Launching**: Execute `python main.py` to open the GUI.
- **Interface**:
  - "Switch View": Toggle between front and back body views.
  - "Manual Update": Force refresh of visualizations.
  - Alert area displays real-time warnings (e.g., thermal exceedance).
- **Real-Time Updates**: Visualizations refresh automatically every 5 seconds.
- **Data Logging**: Metrics are logged in-memory and saved to `emr_suit_log.csv` upon exit.
- **Alerts**: Automatic detection of anomalies like high temperature or low propellant.

## Technical Details

- **Programming Languages**: Python (primary), with support for C++ extensions if needed.
- **Libraries**: NumPy (data processing), Matplotlib (visualization), SciPy (optimization), Pandas (data logging), Tkinter (GUI).
- **Simulation**: Uses random/simulated data for demonstration; replace with real sensor inputs for production.
- **Scalability**: Can be deployed on servers for multi-user monitoring; parallel processing via NumPy/SciPy.

## File Structure

- `main.py`: Main GUI application
- `visualization.py`: Core visualization functions
- `body_model.py`: 2D human body model definitions
- `README.md`: This documentation
- `requirements.txt`: Python dependencies

## Physics Formulas Implemented

### EMR Force Calculation
```
FEMR = μ₀ * I² / (2π * d)
```
Where:
- μ₀ = 4π × 10⁻⁷ T⋅m/A (permeability of free space)
- I = current through coils (A)
- d = distance from coils (m)

### Thermal Efficiency
```
η = 1 - Tc/Th
```
Where:
- Tc = cold temperature (K)
- Th = hot temperature (K)

### Safety Factor
```
SF = 2–4 (target range)
```

### Risk Probability
```
P_risk < 10⁻⁶ (acceptable threshold)
```

## Notes

- This implementation uses simulated data. For actual deployment, integrate with EMR suit sensors and replace random generators with real-time data feeds.
- The software is designed to be error-free and ready-to-run upon completion.
- For advanced features like full EM simulations, integrate with tools like VisIt, Meep, Elmer, FEniCS, Palace, gprMax as specified.
- Ensure matplotlib backend supports GUI (TkAgg is used).

## Future Enhancements

- Integration with real EMR suit telemetry systems
- Multi-user collaborative monitoring
- Advanced EM field simulations using Meep/FEniCS
- Machine learning-based anomaly detection
- 3D visualization capabilities
- Real-time data streaming from suit sensors
