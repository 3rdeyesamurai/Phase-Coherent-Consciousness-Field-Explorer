import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from ion_hall_parametric import PropulsionCalculator
import os

def save_to_csv(results, filename):
    """Save results to CSV file"""
    df = pd.DataFrame(results)
    df.to_csv(filename, index=False)
    print(f"Saved {len(results)} data points to {filename}")

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
        grouped = gas_data.groupby(x_var)['Isp_ax'].mean()
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

    print(f"Created plots for {thruster_type} thruster")

def run_full_sweep():
    """Run complete parametric sweep for both thruster types"""
    print("Initializing propulsion calculator...")
    calc = PropulsionCalculator()

    print("Running ion engine parametric sweep...")
    ion_results = calc.parametric_sweep_ion()
    save_to_csv(ion_results, 'output/ion_sweep.csv')
    create_plots(ion_results, 'ion')

    print("Running Hall thruster parametric sweep...")
    hall_results = calc.parametric_sweep_hall()
    save_to_csv(hall_results, 'output/hall_sweep.csv')
    create_plots(hall_results, 'hall')

    print("\nSweep complete!")
    print(f"Ion engine: {len(ion_results)} data points")
    print(f"Hall thruster: {len(hall_results)} data points")

    # Print some summary statistics
    ion_df = pd.DataFrame(ion_results)
    hall_df = pd.DataFrame(hall_results)

    print("\nIon Engine Summary (Xenon, typical conditions):")
    xenon_ion = ion_df[(ion_df['gas'] == 'Xenon') &
                      (ion_df['Va'] >= 1500) & (ion_df['Va'] <= 2500) &
                      (ion_df['Ib'] >= 1.0) & (ion_df['Ib'] <= 3.0)]
    if not xenon_ion.empty:
        print(f"  Thrust: {xenon_ion['T_axial'].mean() * 1000:.1f} mN")
        print(f"  Isp: {xenon_ion['Isp_ax'].mean():.1f} s")
        print(f"  Power: {xenon_ion['P_elec'].mean():.1f} W")

    print("\nHall Thruster Summary (Xenon, typical conditions):")
    xenon_hall = hall_df[(hall_df['gas'] == 'Xenon') &
                        (hall_df['Vd'] >= 300) & (hall_df['Vd'] <= 500) &
                        (hall_df['mdot'] >= 3e-6) & (hall_df['mdot'] <= 7e-6)]
    if not xenon_hall.empty:
        print(f"  Thrust: {xenon_hall['T_axial'].mean() * 1000:.1f} mN")
        print(f"  Isp: {xenon_hall['Isp_ax'].mean():.1f} s")
        print(f"  Power: {xenon_hall['P_elec'].mean():.1f} W")
if __name__ == "__main__":
    run_full_sweep()
