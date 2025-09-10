import numpy as np
import json
import math
import sys


class PropulsionCalculator:
    def __init__(self, config_path=None):
        if config_path is None:
            # Default to config.json with proper path resolution for
            # executables
            import os
            script_dir = os.path.dirname(os.path.abspath(__file__))
            config_paths = [
                'config.json',  # Current directory
                os.path.join(script_dir, 'config.json'),  # Script directory
            ]

            # Add PyInstaller path if available
            if hasattr(sys, '_MEIPASS'):
                config_paths.insert(
                    0, os.path.join(
                        sys._MEIPASS, 'config.json'))

            config_path = None
            for path in config_paths:
                if os.path.exists(path):
                    config_path = path
                    break

            if config_path is None:
                raise FileNotFoundError(
                    "Could not find config.json file. Please ensure it exists in the application directory.")

        with open(config_path, 'r') as f:
            self.config = json.load(f)

        self.constants = self.config['constants']
        self.gases = self.config['gases']
        self.gas_masses = self.config['gas_masses']

    def calculate_divergence_efficiency(self, model, param_deg, thruster_type):
        """Calculate axial efficiency due to plume divergence"""
        param_rad = np.radians(param_deg)

        if model == 'gaussian':
            # Gaussian distribution: η_div ≈ exp(-σ²/2)
            return np.exp(-param_rad**2 / 2)
        elif model == 'cos':
            # RMS half-angle approximation: η_div ≈ cos(σ)
            return np.cos(param_rad)
        else:
            raise ValueError(f"Unknown divergence model: {model}")

    def calculate_child_langmuir_limit(self, Va, m_i, q, A_open, d):
        """Calculate Child-Langmuir space-charge limited current density"""
        epsilon_0 = 8.854e-12  # F/m

        # Child-Langmuir current density: J_CL = (4/9)ε₀ √(2q/m_i) * (V_a^(3/2)
        # / d²)
        prefactor = (4.0 / 9.0) * epsilon_0 * np.sqrt(2 * q / m_i)
        J_CL = prefactor * (Va**(3 / 2)) / (d**2)

        # Space-charge limited current
        I_CL = J_CL * A_open

        return I_CL, J_CL

    def calculate_space_charge_impingement(self, Ib, I_CL):
        """Calculate space-charge impingement factor"""
        if Ib <= I_CL:
            return 1.0  # No impingement
        else:
            return I_CL / Ib  # Current limited by space charge

    def calculate_ion_engine(
            self,
            Va,
            Ib,
            gas,
            A_grid,
            d,
            tau_geom,
            tau_trans,
            divergence_model,
            sigma_deg):
        """Calculate ion engine performance metrics with enhanced physics"""
        m_i = self.gas_masses[gas] * self.constants['amu']  # kg
        q = self.constants['q']  # C

        # Geometric open area
        A_open = A_grid * tau_geom

        # Ideal beam thrust (no losses)
        T_ideal = Ib * np.sqrt(2 * m_i * Va / q)

        # Exhaust velocity (ideal)
        v_e0 = np.sqrt(2 * q * Va / m_i)

        # Child-Langmuir space-charge limit
        I_CL, J_CL = self.calculate_child_langmuir_limit(Va, m_i, q, A_open, d)

        # Space-charge impingement factor
        tau_imp = self.calculate_space_charge_impingement(Ib, I_CL)

        # Effective beam current accounting for all losses
        Ib_eff = Ib * tau_geom * tau_trans * tau_imp

        # Divergence efficiency
        eta_div = self.calculate_divergence_efficiency(
            divergence_model, sigma_deg, 'ion')

        # Effective thrust with all losses
        T_axial = T_ideal * tau_geom * tau_trans * tau_imp * eta_div

        # Effective specific impulse
        Isp_eff = (v_e0 / self.constants['g0']) * \
            tau_geom * tau_trans * tau_imp * eta_div

        # Electrical power
        P_elec = Va * Ib

        # Mass flow rate
        mdot = Ib_eff * m_i / q

        # Perveance margin (how far from space-charge limit)
        perveance_margin = I_CL / Ib if Ib > 0 else float('inf')

        return {
            'Va': Va,
            'Ib': Ib,
            'Ib_eff': Ib_eff,
            'I_CL': I_CL,
            'J_CL': J_CL,
            'tau_geom': tau_geom,
            'tau_trans': tau_trans,
            'tau_imp': tau_imp,
            'sigma_deg': sigma_deg,
            'eta_div': eta_div,
            'T_ideal': T_ideal,
            'T_axial': T_axial,
            'v_e0': v_e0,
            'Isp_eff': Isp_eff,
            'P_elec': P_elec,
            'mdot': mdot,
            'perveance_margin': perveance_margin,
            'gas': gas,
            'thruster_type': 'ion'
        }

    def calculate_hall_thruster(
            self,
            Vd,
            mdot,
            gas,
            eta_acc,
            tau_prop,
            divergence_model,
            divergence_param):
        """Calculate Hall thruster performance metrics"""
        m_i = self.gas_masses[gas] * self.constants['amu']  # kg
        q = self.constants['q']  # C

        # Exhaust velocity (ideal)
        v_e0 = np.sqrt(eta_acc * 2 * q * Vd / m_i)

        # Divergence efficiency
        eta_div = self.calculate_divergence_efficiency(
            divergence_model, divergence_param, 'hall')

        # Axial thrust
        T_axial = mdot * tau_prop * v_e0 * eta_div

        # Axial specific impulse
        Isp_ax = (v_e0 * eta_div) / self.constants['g0']

        # Electrical power (approximate)
        P_elec = Vd * (mdot * q / (m_i * eta_acc))  # Rough estimate

        # Beam current (for comparison)
        Ib = mdot * q / m_i

        return {
            'Vd': Vd,
            'mdot': mdot,
            'Ib': Ib,
            'v_e0': v_e0,
            'eta_div': eta_div,
            'T_axial': T_axial,
            'Isp_ax': Isp_ax,
            'P_elec': P_elec,
            'gas': gas,
            'thruster_type': 'hall'
        }

    def parametric_sweep_ion(self):
        """Perform parametric sweep for ion engine with enhanced physics"""
        ion_config = self.config['ion_engine']
        Va_range = np.linspace(
            ion_config['Va_range'][0],
            ion_config['Va_range'][1],
            ion_config['Va_steps'])
        Ib_range = np.logspace(
            np.log10(
                ion_config['Ib_range'][0]), np.log10(
                ion_config['Ib_range'][1]), ion_config['Ib_steps'])

        # Extract geometry and loss parameters
        A_grid = ion_config['geometry']['A_grid']
        d = ion_config['geometry']['d']
        tau_geom = ion_config['geometry']['tau_geom']
        tau_trans = ion_config['losses']['tau_trans']
        div_model = ion_config['divergence']['model']
        sigma_deg = ion_config['divergence']['sigma_deg']

        results = []
        for gas in self.gases:
            for Va in Va_range:
                for Ib in Ib_range:
                    result = self.calculate_ion_engine(
                        Va, Ib, gas, A_grid, d, tau_geom, tau_trans, div_model, sigma_deg)
                    results.append(result)

        return results

    def parametric_sweep_hall(self):
        """Perform parametric sweep for Hall thruster"""
        hall_config = self.config['hall_thruster']
        Vd_range = np.linspace(
            hall_config['Vd_range'][0],
            hall_config['Vd_range'][1],
            hall_config['Vd_steps'])
        mdot_range = np.logspace(
            np.log10(
                hall_config['mdot_range'][0]), np.log10(
                hall_config['mdot_range'][1]), hall_config['mdot_steps'])

        results = []
        for gas in self.gases:
            for Vd in Vd_range:
                for mdot in mdot_range:
                    result = self.calculate_hall_thruster(
                        Vd, mdot, gas,
                        hall_config['eta_acc'],
                        hall_config['tau_prop'],
                        hall_config['divergence']['model'],
                        hall_config['divergence']['param_deg']
                    )
                    results.append(result)

        return results

    def update_config(self, new_config):
        """Update calculator configuration dynamically (for GUI integration)"""
        self.config = new_config
        self.constants = self.config['constants']
        self.gases = self.config['gases']
        self.gas_masses = self.config['gas_masses']
        print("✅ Calculator configuration updated")


if __name__ == "__main__":
    calc = PropulsionCalculator()
    print("Enhanced Ion Engine Example (Xenon, 2000V, 2A):")

    # Use the config values for the example
    ion_config = calc.config['ion_engine']
    ion_result = calc.calculate_ion_engine(
        2000, 2.0, 'Xenon',
        ion_config['geometry']['A_grid'],
        ion_config['geometry']['d'],
        ion_config['geometry']['tau_geom'],
        ion_config['losses']['tau_trans'],
        ion_config['divergence']['model'],
        ion_config['divergence']['sigma_deg']
    )

    print(f"Ideal Thrust: {ion_result['T_ideal'] * 1000:.1f} mN")
    print(f"Effective Thrust: {ion_result['T_axial'] * 1000:.1f} mN")
    print(f"Effective Isp: {ion_result['Isp_eff']:.1f} s")
    print(f"Space-charge limit: {ion_result['I_CL']:.2f} A")
    print(f"Perveance margin: {ion_result['perveance_margin']:.2f}")
    print(f"Divergence efficiency: {ion_result['eta_div']:.3f}")

    print("\nHall Thruster Example (Xenon, 400V, 5 mg/s):")
    hall_result = calc.calculate_hall_thruster(
        400, 5e-6, 'Xenon', 0.6, 0.85, 'cos', 30.0)
    print(
        f"Thrust: {
            hall_result['T_axial'] *
            1000:.1f} mN, Isp: {
            hall_result['Isp_ax']:.1f} s")
