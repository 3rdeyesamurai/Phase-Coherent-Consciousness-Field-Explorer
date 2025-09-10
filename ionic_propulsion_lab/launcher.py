#!/usr/bin/env python3
"""
Ionic Propulsion Lab Launcher
A user-friendly launcher for the Enhanced Ionic Propulsion Analysis Tool

This script provides an easy way to run the ionic propulsion lab with
simplified options and user-friendly interface.
"""

import os
import sys
import subprocess
import webbrowser
import time
from pathlib import Path

def print_banner():
    """Display the application banner"""
    print("""
╔══════════════════════════════════════════════════════════════╗
║                    🚀 IONIC PROPULSION LAB                    ║
║              Enhanced Electric Propulsion Analysis            ║
║                                                              ║
║  Features:                                                   ║
║  • Ion Engines & Hall Thrusters                              ║
║  • Space-charge effects (Child-Langmuir)                    ║
║  • Real-time interactive visualization                       ║
║  • Multi-gas performance analysis                           ║
║  • Professional plots & data export                         ║
╚══════════════════════════════════════════════════════════════╝
    """)

def check_dependencies():
    """Check if required Python packages are installed"""
    required_packages = ['numpy', 'pandas', 'matplotlib']
    missing_packages = []

    for package in required_packages:
        try:
            __import__(package)
        except ImportError:
            missing_packages.append(package)

    if missing_packages:
        print("❌ Missing required packages:")
        for package in missing_packages:
            print(f"   - {package}")
        print("\n📦 Installing missing packages...")
        try:
            subprocess.check_call([sys.executable, '-m', 'pip', 'install'] + missing_packages)
            print("✅ Packages installed successfully!")
        except subprocess.CalledProcessError:
            print("❌ Failed to install packages. Please install manually:")
            print(f"   pip install {' '.join(missing_packages)}")
            return False

    return True

def run_analysis():
    """Run the parametric sweep analysis"""
    print("\n🔬 Running Parametric Analysis...")
    print("   This will generate performance data for ion engines and Hall thrusters")
    print("   Analysis includes space-charge effects and multi-gas comparisons")

    try:
        result = subprocess.run([sys.executable, 'run_sweep.py'],
                              capture_output=True, text=True, cwd=os.getcwd())

        if result.returncode == 0:
            print("✅ Analysis completed successfully!")
            print("   Generated files:")
            print("   • ion_sweep.csv (1,500 data points)")
            print("   • hall_sweep.csv (1,500 data points)")
            print("   • 9 professional plots in output/ folder")
            return True
        else:
            print("❌ Analysis failed:")
            print(result.stderr)
            return False

    except Exception as e:
        print(f"❌ Error running analysis: {e}")
        return False

def start_web_server():
    """Start the local web server for interactive visualization"""
    print("\n🌐 Starting Interactive Web Visualization...")
    print("   This will open your browser with real-time parameter controls")

    try:
        # Check if port 8000 is available
        import socket
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        result = sock.connect_ex(('127.0.0.1', 8000))
        sock.close()

        if result == 0:
            print("⚠️  Port 8000 is already in use. Please close other servers first.")
            return False

        # Start web server
        print("   Starting server on http://localhost:8000")
        server_process = subprocess.Popen([sys.executable, '-m', 'http.server', '8000'],
                                        cwd=os.path.join(os.getcwd(), 'viz'),
                                        stdout=subprocess.DEVNULL,
                                        stderr=subprocess.DEVNULL)

        # Wait a moment for server to start
        time.sleep(2)

        # Open browser
        webbrowser.open('http://localhost:8000')

        print("✅ Web server started!")
        print("   • Interactive dashboard: http://localhost:8000")
        print("   • Adjust parameters in real-time")
        print("   • Compare gas performance")
        print("   • View detailed analytics")
        print("\n💡 Tip: Keep this window open while using the web interface")

        return server_process

    except Exception as e:
        print(f"❌ Error starting web server: {e}")
        return False

def show_menu():
    """Display the main menu"""
    while True:
        print("\n" + "="*60)
        print("📋 MAIN MENU")
        print("="*60)
        print("1. 🔬 Run Parametric Analysis")
        print("2. 🌐 Launch Interactive Visualization")
        print("3. 📊 View Results (Open Output Folder)")
        print("4. 📖 View Documentation")
        print("5. ⚙️  Configure Parameters")
        print("6. 🚪 Exit")
        print("="*60)

        try:
            choice = input("Select option (1-6): ").strip()

            if choice == '1':
                if run_analysis():
                    input("\n✅ Analysis complete! Press Enter to continue...")

            elif choice == '2':
                server_process = start_web_server()
                if server_process:
                    input("\n💡 Press Enter to stop the web server...")
                    server_process.terminate()
                    print("✅ Web server stopped.")

            elif choice == '3':
                output_dir = Path('output')
                if output_dir.exists():
                    if sys.platform == 'win32':
                        os.startfile(output_dir)
                    elif sys.platform == 'darwin':
                        subprocess.run(['open', output_dir])
                    else:
                        subprocess.run(['xdg-open', output_dir])
                    print("✅ Opened output folder")
                else:
                    print("❌ Output folder not found. Run analysis first.")

            elif choice == '4':
                readme_path = Path('README.md')
                if readme_path.exists():
                    if sys.platform == 'win32':
                        os.startfile(readme_path)
                    elif sys.platform == 'darwin':
                        subprocess.run(['open', readme_path])
                    else:
                        subprocess.run(['xdg-open', readme_path])
                    print("✅ Opened documentation")
                else:
                    print("❌ Documentation not found")

            elif choice == '5':
                config_path = Path('config.json')
                if config_path.exists():
                    if sys.platform == 'win32':
                        os.startfile(config_path)
                    elif sys.platform == 'darwin':
                        subprocess.run(['open', config_path])
                    else:
                        subprocess.run(['xdg-open', config_path])
                    print("✅ Opened configuration file")
                    print("💡 Edit parameters and re-run analysis to see changes")
                else:
                    print("❌ Configuration file not found")

            elif choice == '6':
                print("\n👋 Thank you for using Ionic Propulsion Lab!")
                print("   Your analysis results are saved in the output/ folder")
                break

            else:
                print("❌ Invalid choice. Please select 1-6.")

        except KeyboardInterrupt:
            print("\n\n👋 Goodbye!")
            break
        except Exception as e:
            print(f"❌ Error: {e}")

def main():
    """Main launcher function"""
    print_banner()

    # Check if we're in the right directory
    if not Path('config.json').exists():
        print("❌ Error: Please run this script from the ionic_propulsion_lab directory")
        print("   Current directory:", os.getcwd())
        input("Press Enter to exit...")
        return

    # Check dependencies
    if not check_dependencies():
        input("\nPress Enter to exit...")
        return

    # Show menu
    show_menu()

if __name__ == "__main__":
    main()
