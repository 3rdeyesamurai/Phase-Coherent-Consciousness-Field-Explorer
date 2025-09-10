# 🚀 Enhanced Ionic Propulsion Lab

An advanced parametric analysis tool for ion engines and Hall thrusters with sophisticated physics modeling and real-time interactive visualization.

## 🎯 Quick Start (Choose Your Path)

### Option A: Standalone Executable (Easiest)
1. **Download:** Get the pre-built executable for your system
2. **Run:** Double-click `Ionic_Propulsion_Lab.exe` (Windows) or executable (Linux/macOS)
3. **Use:** Full GUI application with all features included

### Option B: Build Your Own Executable
1. Run: `python build_executable.py`
2. Follow the build process
3. Use the generated executable

### Option C: Development Setup
1. **Automated:** `python setup.py` (installs dependencies automatically)
2. **Manual:** `pip install numpy pandas matplotlib`
3. **Launch:** `python launcher.py` or `python gui_app.py`

### Option D: Command Line Tools
1. **Analysis:** `python run_sweep.py`
2. **Web Interface:** `python -m http.server 8000` → `http://localhost:8000/viz/index.html`
3. **Diagnostics:** `python diagnostics.py`

## ✨ Key Features

- **🔬 Advanced Physics Models**: Child-Langmuir space-charge limits, geometric transparency, plume divergence
- **📊 Parametric Sweeps**: Comprehensive analysis across voltage, current, mass flow, geometry, and gas types
- **🎛️ Interactive Web Interface**: Real-time sliders and filters with D3.js charts
- **📈 Enhanced Analytics**: Perveance analysis, efficiency breakdowns, space-charge diagnostics
- **🌍 Multi-Gas Support**: Xenon, Iodine, Krypton, Argon, and Water fragments
- **📋 Professional Plots**: High-quality PNG plots for reports and publications

## Physics Models

### Ion Engine
- **Axial Thrust**: `T_axial = I_b,eff * √(2 m_i q V_a) * η_div`
- **Effective Beam Current**: `I_b,eff = I_b * τ_open * τ_trans`
- **Axial Isp**: `Isp_ax = (v_e,0 * η_div)/g₀`

### Hall Thruster
- **Axial Thrust**: `T_axial = ṁ * τ_prop * v_e,0 * η_div`
- **Exhaust Velocity**: `v_e,0 = √(η_acc 2 q V_d / m_i)`

### Divergence Models
- **Gaussian**: `η_div ≈ exp(-σ²/2)` (σ in radians)
- **Cosine**: `η_div = (1 - cosθ)/θ` (uniform cone)

## Quick Start

1. **Run the parametric sweep**:
   ```bash
   python run_sweep.py
   ```

2. **View static plots** in the `output/` directory:
   - `ion_thrust_vs_Va.png`
   - `ion_isp_vs_Va.png`
   - `hall_thrust_vs_Vd.png`
   - `hall_isp_vs_Vd.png`

3. **Interactive visualization**:
   - Start a local web server:
     ```bash
     python -m http.server 8000
     ```
   - Open `viz/index.html` in your browser
   - Click "Load Data" to visualize the results

## Configuration

Edit `config.json` to customize:

```json
{
  "gases": ["Xenon", "Iodine", "Krypton", "Argon", "WaterOH"],
  "ion_engine": {
    "Va_range": [500, 4000],      // Acceleration voltage range (V)
    "Ib_range": [0.1, 5.0],       // Beam current range (A)
    "tau_open": 0.7,              // Grid optical transparency
    "tau_trans": 0.95,            // Transmission efficiency
    "divergence": {
      "model": "gaussian",        // "gaussian" or "cos"
      "param_deg": 5.0            // σ or half-angle (degrees)
    }
  },
  "hall_thruster": {
    "Vd_range": [200, 800],       // Discharge voltage range (V)
    "mdot_range": [1e-6, 10e-6],  // Mass flow range (kg/s)
    "eta_acc": 0.6,               // Acceleration efficiency
    "tau_prop": 0.85,             // Propellant utilization
    "divergence": {
      "model": "cos",
      "param_deg": 30.0
    }
  }
}
```

## File Structure

```
ionic_propulsion_lab/
├── config.json              # Configuration parameters
├── ion_hall_parametric.py   # Physics calculation engine
├── run_sweep.py            # Main sweep execution script
├── README.md               # This documentation
├── output/                 # Generated CSV files and plots
│   ├── ion_sweep.csv
│   ├── hall_sweep.csv
│   ├── ion_thrust_vs_Va.png
│   └── ...
└── viz/                    # Web visualization
    └── index.html
```

## Interactive Features

### Web Interface Controls

- **Thruster Type**: Switch between Ion Engine and Hall Thruster
- **Gas Selection**: Multi-select filter for propellant gases
- **Parameter Sliders**:
  - Beam Current (Ion only)
  - Mass Flow (Hall only)
  - Grid Transparency (τ_open)
  - Transmission (τ_trans)
  - Divergence Angle
- **Real-time Updates**: Charts update instantly as you adjust parameters

### Charts

1. **Thrust vs Voltage**: Performance curves for each gas
2. **Isp vs Voltage**: Efficiency comparison
3. **Power vs Thrust**: Operating point analysis
4. **Efficiency Analysis**: Isp vs Thrust trade-offs

## Dependencies

- Python 3.7+
- NumPy
- Pandas
- Matplotlib
- Modern web browser with JavaScript enabled

## Example Results

### Ion Engine (Xenon, 2000V, 2A beam)
- Thrust: ~85 mN
- Isp: ~3800 s
- Power: ~4000 W
- Efficiency: ~65%

### Hall Thruster (Xenon, 400V, 5 mg/s)
- Thrust: ~45 mN
- Isp: ~1600 s
- Power: ~2000 W
- Efficiency: ~55%

## Advanced Usage

### Custom Physics Models

Modify `ion_hall_parametric.py` to add:
- Additional divergence models
- Ionization efficiency variations
- Magnetic field effects
- Temperature-dependent properties

### Sensitivity Analysis

The parametric sweeps enable:
- Partial derivatives: `∂T/∂τ_open`, `∂T/∂σ`
- Pareto front analysis for thrust vs power vs Isp
- Optimization studies across operating envelopes

### Data Export

CSV files contain all calculated parameters for:
- External analysis tools
- Report generation
- Comparison with experimental data

## Troubleshooting

### Web Visualization Issues
- Ensure you're running a local web server (not opening HTML directly)
- Check browser console for JavaScript errors
- Verify CSV file paths are correct

### Python Errors
- Install missing dependencies: `pip install numpy pandas matplotlib`
- Check file permissions for output directory
- Verify config.json syntax

### Performance
- Large parameter ranges may take time to compute
- Reduce steps in config.json for faster execution
- Web interface handles up to ~10,000 data points smoothly

## Contributing

To extend the lab:
1. Add new gas properties to `config.json`
2. Implement additional physics models in `ion_hall_parametric.py`
3. Enhance web visualization with new chart types
4. Add export functionality for different formats

## License

This project is provided as-is for educational and research purposes.
