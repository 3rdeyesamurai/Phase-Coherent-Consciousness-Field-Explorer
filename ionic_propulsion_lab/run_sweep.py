import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from ion_hall_parametric import PropulsionCalculator
import os

def save_to_csv(results, filename):
    """Save results to CSV file"""
    # Ensure output directory exists
    output_dir = os.path.dirname(filename)
    if output_dir:
        try:
            os.makedirs(output_dir, exist_ok=True)
            print(f"✅ Created/verified directory: {output_dir}")
        except Exception as e:
            print(f"❌ Error creating directory {output_dir}: {e}")
            return False

    try:
        df = pd.DataFrame(results)
        df.to_csv(filename, index=False)
        print(f"✅ Saved {len(results)} data points to {filename}")
        return True
    except Exception as e:
        print(f"❌ Error saving CSV to {filename}: {e}")
        return False

def create_plots(results, thruster_type, output_dir='output'):
    """Create static plots for the results"""
    df = pd.DataFrame(results)

    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)

    # Unique gases
    gases = df['gas'].unique()

    if thruster_type == 'ion':
        x_var = 'Va'
        x_label = 'Acceleration Voltage (V)'
        title_prefix = 'Ion Engine'
    else:
        x_var = 'Vd'
        x_label = 'Discharge Voltage (V)'
        title_prefix = 'Hall Thruster'

    # Plot 1: Thrust vs Voltage for each gas
    plt.figure(figsize=(12, 8))
    for gas in gases:
        gas_data = df[df['gas'] == gas]
        # Group by voltage and take mean thrust (averaging over other parameters)
        grouped = gas_data.groupby(x_var)['T_axial'].mean()
        plt.plot(grouped.index, grouped.values * 1000, label=gas, marker='o', markersize=3)

    plt.xlabel(x_label)
    plt.ylabel('Axial Thrust (mN)')
    plt.title(f'{title_prefix}: Thrust vs {x_label}')
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(f'{output_dir}/{thruster_type}_thrust_vs_V.png', dpi=300, bbox_inches='tight')
    plt.close()

    # Plot 2: Isp vs Voltage for each gas
    plt.figure(figsize=(12, 8))
    for gas in gases:
        gas_data = df[df['gas'] == gas]
        # Use appropriate Isp column based on thruster type
        isp_col = 'Isp_eff' if thruster_type == 'ion' else 'Isp_ax'
        grouped = gas_data.groupby(x_var)[isp_col].mean()
        plt.plot(grouped.index, grouped.values, label=gas, marker='s', markersize=3)

    plt.xlabel(x_label)
    plt.ylabel('Axial Specific Impulse (s)')
    plt.title(f'{title_prefix}: Isp vs {x_label}')
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(f'{output_dir}/{thruster_type}_isp_vs_V.png', dpi=300, bbox_inches='tight')
    plt.close()

    # Plot 3: Power vs Thrust (efficiency-like plot)
    plt.figure(figsize=(10, 8))
    for gas in gases:
        gas_data = df[df['gas'] == gas]
        plt.scatter(gas_data['T_axial'] * 1000, gas_data['P_elec'], label=gas, alpha=0.6, s=20)

    plt.xlabel('Axial Thrust (mN)')
    plt.ylabel('Electrical Power (W)')
    plt.title(f'{title_prefix}: Power vs Thrust')
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(f'{output_dir}/{thruster_type}_power_vs_thrust.png', dpi=300, bbox_inches='tight')
    plt.close()

    # For ion engines, add space-charge analysis plots
    if thruster_type == 'ion':
        # Plot 4: Perveance margin vs Thrust
        plt.figure(figsize=(10, 8))
        for gas in gases:
            gas_data = df[df['gas'] == gas]
            plt.scatter(gas_data['T_axial'] * 1000, gas_data['perveance_margin'],
                       label=gas, alpha=0.6, s=20)

        plt.axhline(y=1.0, color='red', linestyle='--', alpha=0.7, label='Space-charge limit')
        plt.xlabel('Axial Thrust (mN)')
        plt.ylabel('Perveance Margin (I_CL/I_b)')
        plt.title(f'{title_prefix}: Space-Charge Analysis')
        plt.legend()
        plt.grid(True, alpha=0.3)
        plt.yscale('log')
        plt.tight_layout()
        plt.savefig(f'{output_dir}/{thruster_type}_perveance_analysis.png', dpi=300, bbox_inches='tight')
        plt.close()

        # Plot 5: Thrust efficiency breakdown
        plt.figure(figsize=(12, 8))
        for gas in gases:
            gas_data = df[df['gas'] == gas]
            # Calculate efficiency as T_axial / T_ideal
            efficiency = gas_data['T_axial'] / gas_data['T_ideal']
            plt.scatter(gas_data['Va'], efficiency, label=gas, alpha=0.6, s=20)

        plt.xlabel('Acceleration Voltage (V)')
        plt.ylabel('Thrust Efficiency (T_eff/T_ideal)')
        plt.title(f'{title_prefix}: Thrust Efficiency vs Voltage')
        plt.legend()
        plt.grid(True, alpha=0.3)
        plt.tight_layout()
        plt.savefig(f'{output_dir}/{thruster_type}_efficiency_analysis.png', dpi=300, bbox_inches='tight')
        plt.close()

    print(f"Created plots for {thruster_type} thruster")

def run_full_sweep():
    """Run complete parametric sweep for both thruster types"""
    print("🔬 Initializing propulsion calculator...")
    try:
        calc = PropulsionCalculator()
        print("✅ Calculator initialized successfully")
    except Exception as e:
        print(f"❌ Failed to initialize calculator: {e}")
        return False

    success_count = 0

    print("\n⚡ Running ion engine parametric sweep...")
    try:
        ion_results = calc.parametric_sweep_ion()
        print(f"📊 Generated {len(ion_results)} ion engine data points")

        if save_to_csv(ion_results, 'output/ion_sweep.csv'):
            create_plots(ion_results, 'ion')
            success_count += 1
    except Exception as e:
        print(f"❌ Ion engine sweep failed: {e}")

    print("\n⚡ Running Hall thruster parametric sweep...")
    try:
        hall_results = calc.parametric_sweep_hall()
        print(f"📊 Generated {len(hall_results)} Hall thruster data points")

        if save_to_csv(hall_results, 'output/hall_sweep.csv'):
            create_plots(hall_results, 'hall')
            success_count += 1
    except Exception as e:
        print(f"❌ Hall thruster sweep failed: {e}")

    if success_count == 0:
        print("\n❌ All sweeps failed. Please check the error messages above.")
        return False

    print(f"\n🎉 Sweep complete! ({success_count}/2 successful)")
    print("📁 Results saved to output/ folder")
    print("📊 Generated plots and CSV files ready for analysis")

    # Print some summary statistics
    try:
        if 'ion_results' in locals() and ion_results:
            ion_df = pd.DataFrame(ion_results)
            print(f"\n📈 Ion Engine Summary (Xenon, typical conditions):")
            xenon_ion = ion_df[(ion_df['gas'] == 'Xenon') &
                              (ion_df['Va'] >= 1500) & (ion_df['Va'] <= 2500) &
                              (ion_df['Ib'] >= 1.0) & (ion_df['Ib'] <= 3.0)]
            if not xenon_ion.empty:
                print(f"   Thrust: {xenon_ion['T_axial'].mean() * 1000:.1f} mN")
                print(f"   Isp: {xenon_ion['Isp_eff'].mean():.1f} s")
                print(f"   Power: {xenon_ion['P_elec'].mean():.1f} W")
                print(f"   Perveance margin: {xenon_ion['perveance_margin'].mean():.2f}")
                print(f"   Thrust efficiency: {(xenon_ion['T_axial']/xenon_ion['T_ideal']).mean():.3f}")

        if 'hall_results' in locals() and hall_results:
            hall_df = pd.DataFrame(hall_results)
            print(f"\n📈 Hall Thruster Summary (Xenon, typical conditions):")
            xenon_hall = hall_df[(hall_df['gas'] == 'Xenon') &
                                (hall_df['Vd'] >= 300) & (hall_df['Vd'] <= 500) &
                                (hall_df['mdot'] >= 3e-6) & (hall_df['mdot'] <= 7e-6)]
            if not xenon_hall.empty:
                print(f"   Thrust: {xenon_hall['T_axial'].mean() * 1000:.1f} mN")
                print(f"   Isp: {xenon_hall['Isp_ax'].mean():.1f} s")
                print(f"   Power: {xenon_hall['P_elec'].mean():.1f} W")

    except Exception as e:
        print(f"⚠️  Could not generate summary statistics: {e}")

    print("\n💡 Next steps:")
    print("   1. View plots in output/ folder")
    print("   2. Run: python launcher.py → Option 2 for interactive viz")
    print("   3. Open: http://localhost:8000 in your browser")

    return True
if __name__ == "__main__":
    run_full_sweep()
