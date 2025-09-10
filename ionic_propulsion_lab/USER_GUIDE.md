# 🚀 Ionic Propulsion Lab - User Guide

Welcome to the **Enhanced Ionic Propulsion Lab**! This guide will help you get started with analyzing ion engines and Hall thrusters using advanced physics models.

## 🎯 Quick Start (3 Steps)

### Step 1: Launch the Lab
**For Windows users:** Double-click `run_lab.bat`
**For other systems:** Run `python launcher.py`

This will open the main menu with all available options.

### Step 2: Run Your First Analysis
1. Select option **1** from the main menu
2. Wait for the parametric sweep to complete (takes ~30 seconds)
3. The system will generate performance data and plots

### Step 3: Explore Interactive Results
1. Select option **2** from the main menu
2. Your browser will open with the interactive dashboard
3. Adjust sliders to see real-time performance changes

---

## 📋 Detailed Usage Guide

### Main Menu Options

#### 1. 🔬 Run Parametric Analysis
- **What it does:** Generates comprehensive performance data
- **Output:** CSV files + 9 professional plots
- **Time:** ~30 seconds for full analysis
- **Data points:** 1,500 per thruster type

#### 2. 🌐 Launch Interactive Visualization
- **What it does:** Opens web-based dashboard
- **Features:** Real-time parameter adjustment
- **URL:** http://localhost:8000
- **Tip:** Keep the launcher window open

#### 3. 📊 View Results
- **What it does:** Opens the output folder
- **Contents:** All generated plots and data files
- **Format:** PNG plots + CSV spreadsheets

#### 4. 📖 View Documentation
- **What it does:** Opens detailed technical documentation
- **Includes:** Physics models, configuration options, troubleshooting

#### 5. ⚙️ Configure Parameters
- **What it does:** Opens the configuration file
- **File:** `config.json`
- **Tip:** Edit values and re-run analysis to see changes

---

## 🎛️ Interactive Dashboard Guide

### Thruster Types
- **Ion Engine:** Gridded electrostatic thruster
- **Hall Thruster:** Magnetic confinement thruster

### Gas Selection
- **Xenon:** Most common propellant (highest performance)
- **Iodine:** Alternative with similar performance
- **Krypton:** Lower cost but reduced efficiency
- **Argon:** Research/development use

### Parameter Controls

#### Ion Engine Parameters
- **Beam Current (A):** 0.1 - 5.0 A (affects thrust)
- **Acceleration Voltage (V):** 500 - 4000 V (affects Isp)
- **Grid Transparency:** 0.5 - 0.9 (affects efficiency)
- **Transmission:** 0.8 - 1.0 (affects efficiency)
- **Divergence Angle:** 1° - 45° (affects efficiency)

#### Hall Thruster Parameters
- **Mass Flow (mg/s):** 1 - 10 mg/s (affects thrust)
- **Discharge Voltage (V):** 200 - 800 V (affects Isp)

### Charts Explained

#### 1. Thrust vs Voltage
- **X-axis:** Acceleration/Discharge voltage
- **Y-axis:** Thrust in milliNewtons
- **Use:** Compare performance across voltage ranges

#### 2. Isp vs Voltage
- **X-axis:** Acceleration/Discharge voltage
- **Y-axis:** Specific impulse in seconds
- **Use:** Efficiency comparison across operating points

#### 3. Power vs Thrust
- **X-axis:** Thrust in milliNewtons
- **Y-axis:** Electrical power in Watts
- **Use:** Operating point optimization

#### 4. Efficiency Analysis (Ion only)
- **X-axis:** Thrust in milliNewtons
- **Y-axis:** Specific impulse in seconds
- **Use:** Overall thruster efficiency assessment

---

## 🔧 Configuration Guide

### Basic Configuration (`config.json`)

```json
{
  "ion_engine": {
    "Va_range": [500, 4000],    // Voltage sweep range
    "Ib_range": [0.1, 5.0],     // Current sweep range
    "geometry": {
      "A_grid": 0.01,           // Grid area (m²)
      "d": 0.002,               // Grid gap (m)
      "tau_geom": 0.7           // Geometric transparency
    }
  }
}
```

### Advanced Parameters

#### Space-Charge Effects
- **Grid Gap (d):** Smaller gaps increase space-charge limits
- **Grid Area:** Larger grids handle higher currents
- **Geometric Transparency:** Higher values improve efficiency

#### Divergence Modeling
- **Gaussian Model:** For detailed beam profiles
- **Cosine Model:** Simplified approximation
- **Angle Range:** 1°-45° typical for ion thrusters

---

## 📊 Understanding Results

### Performance Metrics

#### Thrust (mN)
- **Ion Engine:** Typically 10-100 mN
- **Hall Thruster:** Typically 20-200 mN
- **Factors:** Beam current, mass flow, voltage

#### Specific Impulse (s)
- **Ion Engine:** 1,000-4,000 s
- **Hall Thruster:** 800-2,000 s
- **Factors:** Exhaust velocity, divergence losses

#### Power (W)
- **Ion Engine:** 500-5,000 W
- **Hall Thruster:** 500-3,000 W
- **Factors:** Voltage, current, efficiency

### Efficiency Analysis

#### Thrust Efficiency
- **Definition:** Actual thrust / Ideal thrust
- **Typical Values:** 20-40% for ion engines
- **Loss Sources:** Geometric, transmission, divergence

#### Perveance Margin
- **Definition:** Space-charge limit / Operating current
- **Safe Range:** > 1.0 (above limit)
- **Critical:** < 1.0 (space-charge limited)

---

## 🛠️ Troubleshooting

### Common Issues

#### "Python not found"
**Solution:** Install Python from python.org
- Check "Add to PATH" during installation
- Restart command prompt after installation

#### "Missing packages"
**Solution:** The launcher will install automatically
- Or manually: `pip install numpy pandas matplotlib`

#### "Port 8000 in use"
**Solution:** Close other web servers
- Or change port in launcher.py

#### "No output files"
**Solution:** Run analysis first (option 1)
- Check that config.json exists
- Verify write permissions

### Performance Tips

- **Faster Analysis:** Reduce steps in config.json
- **Memory Usage:** Large parameter ranges use more RAM
- **Web Interface:** Close browser tab when done to free port

---

## 📚 Learning Resources

### Physics Concepts
- **Child-Langmuir Law:** Space-charge limited current
- **Specific Impulse:** Efficiency measure for rockets
- **Beam Divergence:** Angular spread of exhaust

### Applications
- **Spacecraft Propulsion:** Station-keeping, orbit raising
- **Deep Space Missions:** High-efficiency requirements
- **Satellite Technology:** Precise attitude control

---

## 🎓 Examples & Tutorials

### Example 1: Basic Ion Engine Analysis
1. Run parametric analysis
2. Open interactive dashboard
3. Select "Ion Engine" tab
4. Adjust voltage slider: 1000V → 3000V
5. Observe thrust and Isp changes

### Example 2: Gas Comparison
1. Run analysis with all gases selected
2. In dashboard, compare Xenon vs Iodine
3. Note performance differences
4. Adjust parameters to optimize for each gas

### Example 3: Space-Charge Effects
1. Run analysis
2. View perveance analysis plot
3. Adjust grid gap in config.json
4. Re-run to see space-charge limit changes

---

## 📞 Support & Resources

### Getting Help
- Check the **README.md** for detailed technical documentation
- Review **config.json** for all available parameters
- Examine **output/** folder for generated results

### File Locations
- **Configuration:** `config.json`
- **Results:** `output/` folder
- **Web Interface:** `viz/index.html`
- **Documentation:** `README.md`

---

## 🚀 Next Steps

1. **Experiment:** Try different parameter combinations
2. **Customize:** Modify config.json for your specific needs
3. **Analyze:** Compare results with published thruster data
4. **Extend:** Add new gases or physics models

**Happy analyzing! Your ionic propulsion expertise starts here!** 🎉
