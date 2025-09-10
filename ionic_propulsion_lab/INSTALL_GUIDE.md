# 🚀 Ionic Propulsion Lab - Complete Installation & Troubleshooting Guide

This guide provides step-by-step instructions for installing and troubleshooting the Enhanced Ionic Propulsion Analysis Tool on various operating systems.

---

## 🎯 Quick Installation (3 Methods)

### Method 1: Automated Setup (Recommended)
```bash
# Download and extract the ionic_propulsion_lab folder
# Open terminal/command prompt in the ionic_propulsion_lab directory
python setup.py
```
**What it does:** Automatically installs dependencies, creates shortcuts, and verifies installation.

### Method 2: Manual Installation
```bash
# 1. Install Python packages
pip install numpy pandas matplotlib

# 2. Run diagnostic check
python diagnostics.py

# 3. Launch the application
python launcher.py
```

### Method 3: Windows One-Click
```bash
# Simply double-click: run_lab.bat
# The batch file handles everything automatically
```

---

## 📋 System Requirements

### Minimum Requirements
- **Python:** 3.7 or higher
- **RAM:** 2 GB available
- **Disk Space:** 100 MB free
- **Operating System:** Windows 7+, macOS 10.12+, Ubuntu 16.04+

### Recommended Requirements
- **Python:** 3.9 or higher
- **RAM:** 4 GB available
- **Disk Space:** 500 MB free
- **Operating System:** Windows 10+, macOS 11+, Ubuntu 20.04+

---

## 🖥️ Operating System Specific Instructions

### Windows Installation

#### Step 1: Install Python
1. Visit: https://python.org/downloads/
2. Download Python 3.9+ installer
3. **IMPORTANT:** Check "Add Python to PATH" during installation
4. Verify installation: `python --version`

#### Step 2: Download Ionic Propulsion Lab
1. Extract the `ionic_propulsion_lab` folder to your desired location
2. Open Command Prompt or PowerShell
3. Navigate to the folder: `cd path\to\ionic_propulsion_lab`

#### Step 3: Run Setup
```cmd
# Option A: Automated setup
python setup.py

# Option B: Manual setup
pip install numpy pandas matplotlib
python diagnostics.py

# Option C: Direct launch
run_lab.bat
```

#### Windows Troubleshooting
- **"Python not recognized":** Reinstall Python with "Add to PATH" checked
- **Permission errors:** Run Command Prompt as Administrator
- **Antivirus blocking:** Add exception for the ionic_propulsion_lab folder

### macOS Installation

#### Step 1: Install Python
```bash
# Using Homebrew (recommended)
brew install python

# Or download from python.org
# Make sure to check "Add Python to PATH"
```

#### Step 2: Download and Setup
```bash
# Extract the ionic_propulsion_lab folder
cd ionic_propulsion_lab

# Run setup
python3 setup.py
```

#### macOS Troubleshooting
- **Permission errors:** Use `sudo` or adjust folder permissions
- **Python path issues:** Use `python3` instead of `python`
- **Gatekeeper blocking:** Right-click app and select "Open"

### Linux Installation

#### Ubuntu/Debian
```bash
# Install Python and pip
sudo apt update
sudo apt install python3 python3-pip

# Install required packages
pip3 install numpy pandas matplotlib

# Run the lab
cd ionic_propulsion_lab
python3 launcher.py
```

#### CentOS/RHEL/Fedora
```bash
# Install Python
sudo yum install python3 python3-pip  # CentOS/RHEL
sudo dnf install python3 python3-pip  # Fedora

# Install packages
pip3 install numpy pandas matplotlib

# Run the lab
cd ionic_propulsion_lab
python3 launcher.py
```

#### Linux Troubleshooting
- **Permission errors:** Use `sudo` for system-wide installation
- **Python path:** Use `python3` and `pip3` instead of `python`/`pip`
- **Missing libraries:** Install development packages if needed

---

## 🔧 Troubleshooting Common Issues

### Issue 1: "Python is not recognized as an internal or external command"
**Symptoms:** Command prompt can't find Python
**Solutions:**
1. Reinstall Python and check "Add Python to PATH"
2. Use full path: `C:\Python39\python.exe setup.py`
3. Add Python to PATH manually:
   - Windows: System Properties → Environment Variables
   - Add: `C:\Python39\` and `C:\Python39\Scripts\` to PATH

### Issue 2: "ModuleNotFoundError: No module named 'numpy'"
**Symptoms:** Import errors for required packages
**Solutions:**
```bash
# Install missing packages
pip install numpy pandas matplotlib

# Or for user-only installation
pip install --user numpy pandas matplotlib

# Verify installation
python -c "import numpy, pandas, matplotlib; print('All packages OK')"
```

### Issue 3: "Cannot save file into a non-existent directory: 'output'"
**Symptoms:** CSV/Plot generation fails
**Solutions:**
1. Check write permissions in the ionic_propulsion_lab folder
2. Run as Administrator (Windows) or with sudo (Linux/macOS)
3. Create output directory manually: `mkdir output`
4. Check available disk space

### Issue 4: "Port 8000 is already in use"
**Symptoms:** Web server fails to start
**Solutions:**
1. Close other applications using port 8000
2. Find process using port: `netstat -ano | findstr :8000` (Windows)
3. Kill process: `taskkill /PID <process_id> /F` (Windows)
4. Or use different port in launcher.py

### Issue 5: "Permission denied" or "Access denied"
**Symptoms:** Can't read/write files
**Solutions:**
1. **Windows:** Run Command Prompt as Administrator
2. **macOS/Linux:** Use `sudo` or fix permissions:
   ```bash
   chmod -R 755 ionic_propulsion_lab
   chown -R $USER ionic_propulsion_lab
   ```
3. Move folder to a location with proper permissions (avoid Program Files)

### Issue 6: "ImportError: DLL load failed" (Windows)
**Symptoms:** Package installation succeeds but import fails
**Solutions:**
1. Install Microsoft Visual C++ Redistributable
2. Reinstall Python in a clean directory
3. Use conda instead of pip: `conda install numpy pandas matplotlib`

### Issue 7: Web browser doesn't open automatically
**Symptoms:** Web server starts but browser doesn't launch
**Solutions:**
1. Manually open: http://localhost:8000
2. Check default browser settings
3. Disable popup blockers for local development

### Issue 8: "config.json not found"
**Symptoms:** Application can't find configuration file
**Solutions:**
1. Ensure you're running from the ionic_propulsion_lab directory
2. Check if config.json exists: `dir config.json` (Windows) or `ls config.json`
3. Restore config.json from backup if corrupted

---

## 🧪 Diagnostic Tools

### Run System Diagnostics
```bash
# Check system health
python diagnostics.py
```

This will test:
- ✅ Python version compatibility
- ✅ Required files presence
- ✅ Configuration file validity
- ✅ Package dependencies
- ✅ File permissions
- ✅ Network connectivity
- ✅ Core functionality

### Manual Health Checks

#### Check Python Installation
```bash
python --version
python -c "import sys; print(sys.version)"
```

#### Check Package Installation
```bash
python -c "import numpy; print('NumPy OK')"
python -c "import pandas; print('Pandas OK')"
python -c "import matplotlib; print('Matplotlib OK')"
```

#### Check File Permissions
```bash
# Windows
dir ionic_propulsion_lab

# Linux/macOS
ls -la ionic_propulsion_lab
```

#### Test Core Functionality
```bash
python -c "from ion_hall_parametric import PropulsionCalculator; print('Core OK')"
```

---

## 📦 Manual Package Installation

### Using pip (Recommended)
```bash
# Install all required packages
pip install numpy pandas matplotlib

# Install in user directory (no admin rights needed)
pip install --user numpy pandas matplotlib

# Upgrade existing packages
pip install --upgrade numpy pandas matplotlib
```

### Using conda (Alternative)
```bash
# Create environment
conda create -n ionic_lab python=3.9
conda activate ionic_lab

# Install packages
conda install numpy pandas matplotlib
```

### Platform-Specific Installation

#### Windows with Chocolatey
```cmd
choco install python
refreshenv
pip install numpy pandas matplotlib
```

#### macOS with Homebrew
```bash
brew install python
pip3 install numpy pandas matplotlib
```

#### Ubuntu/Debian
```bash
sudo apt install python3-numpy python3-pandas python3-matplotlib
```

---

## 🌐 Network and Firewall Issues

### Web Interface Not Loading
1. **Check firewall:** Allow Python through firewall
2. **Verify port:** Ensure port 8000 is not blocked
3. **Local access:** Use http://127.0.0.1:8000 or http://localhost:8000

### Corporate Network Issues
1. **Proxy settings:** Configure pip proxy if needed
2. **SSL certificates:** Use `--trusted-host` with pip if SSL issues
3. **Offline installation:** Download packages manually and install with `pip install package.whl`

---

## 🔄 Updating the Ionic Propulsion Lab

### Update Process
```bash
# Backup your results
cp -r output output_backup

# Download new version
# Replace files with updated versions

# Run diagnostics
python diagnostics.py

# Test functionality
python launcher.py
```

### Version Compatibility
- Always backup `config.json` before updating
- Check `USER_GUIDE.md` for new features
- Run diagnostics after major updates

---

## 📞 Getting Help

### Self-Help Resources
1. **USER_GUIDE.md** - Step-by-step usage instructions
2. **README.md** - Technical documentation
3. **Diagnostics tool:** `python diagnostics.py`
4. **Error messages:** Usually contain specific solutions

### Common Support Scenarios

#### "Everything was working, now it's broken"
1. Check if files were accidentally moved/deleted
2. Run diagnostics: `python diagnostics.py`
3. Restore from backup if needed

#### "Performance is slow"
1. Close other applications
2. Check available RAM (>2GB recommended)
3. Reduce parameter sweep ranges in config.json

#### "Plots don't look right"
1. Update matplotlib: `pip install --upgrade matplotlib`
2. Check config.json for valid parameter ranges
3. Verify data files in output/ folder

---

## 🚀 Advanced Configuration

### Custom Python Installation
```bash
# Install in custom location
python -m pip install --target=C:\MyPythonLibs numpy pandas matplotlib

# Add to Python path
export PYTHONPATH=$PYTHONPATH:/path/to/custom/libs
```

### Virtual Environment Setup
```bash
# Create virtual environment
python -m venv ionic_lab_env

# Activate environment
# Windows: ionic_lab_env\Scripts\activate
# Linux/macOS: source ionic_lab_env/bin/activate

# Install packages
pip install numpy pandas matplotlib

# Run the lab
python launcher.py
```

### Docker Container (Advanced)
```dockerfile
FROM python:3.9-slim

WORKDIR /app
COPY . /app

RUN pip install numpy pandas matplotlib

CMD ["python", "launcher.py"]
```

---

## 📋 Quick Reference

### Essential Commands
```bash
# Install dependencies
pip install numpy pandas matplotlib

# Run diagnostics
python diagnostics.py

# Launch application
python launcher.py

# Start web interface
python -m http.server 8000

# Direct analysis
python run_sweep.py
```

### File Locations
- **Main scripts:** `launcher.py`, `run_sweep.py`
- **Configuration:** `config.json`
- **Documentation:** `README.md`, `USER_GUIDE.md`
- **Web interface:** `viz/index.html`
- **Results:** `output/` folder

### Key URLs
- **Web Interface:** http://localhost:8000
- **Documentation:** Open `USER_GUIDE.md`
- **Configuration:** Edit `config.json`

---

## 🎯 Success Checklist

After installation, verify these work:
- ✅ `python --version` shows 3.7+
- ✅ `python -c "import numpy, pandas, matplotlib"` succeeds
- ✅ `python diagnostics.py` shows all tests passing
- ✅ `python launcher.py` opens the main menu
- ✅ Web interface loads at http://localhost:8000
- ✅ Analysis generates CSV files and plots

**If all checks pass, your Ionic Propulsion Lab is ready for advanced electric propulsion analysis!** 🚀
