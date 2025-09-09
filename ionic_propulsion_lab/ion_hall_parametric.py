import numpy as np
import json
import math

class PropulsionCalculator:
    def __init__(self, config_path='config.json'):
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
            # Uniform cone: average cos over half-angle
            if param_rad == 0:
                return 1.0
            return (1 - np.cos(param_rad)) / param_rad
        else:
            raise ValueError(f"Unknown divergence model: {model}")

    def calculate_ion_engine(self, Va, Ib, gas, tau_open, tau_trans, divergence_model, divergence_param):
        """Calculate ion engine performance metrics"""
        m_i = self.gas_masses[gas] * self.constants['amu']  # kg
        q = self.constants['q']  # C

        # Effective beam current accounting for grid losses
        Ib_eff = Ib * tau_open * tau_trans

        # Exhaust velocity (ideal)
        v_e0 = np.sqrt(2 * q * Va / m_i)

        # Divergence efficiency
        eta_div = self.calculate_divergence_efficiency(divergence_model, divergence_param, 'ion')

        # Axial thrust - correct formula: T = Ib * sqrt(2 * m_i * Va / q)
        T_axial = Ib_eff * np.sqrt(2 * m_i * Va / q) * eta_div

        # Axial specific impulse
        Isp_ax = (v_e0 * eta_div) / self.constants['g0']

        # Electrical power
        P_elec = Va * Ib

        # Mass flow rate
        mdot = Ib_eff * m_i / q

        return {
            'Va': Va,
            'Ib': Ib,
            'Ib_eff': Ib_eff,
            'v_e0': v_e0,
            'eta_div': eta_div,
            'T_axial': T_axial,
            'Isp_ax': Isp_ax,
            'P_elec': P_elec,
            'mdot': mdot,
            'gas': gas,
            'thruster_type': 'ion'
        }

    def calculate_hall_thruster(self, Vd, mdot, gas, eta_acc, tau_prop, divergence_model, divergence_param):
        """Calculate Hall thruster performance metrics"""
        m_i = self.gas_masses[gas] * self.constants['amu']  # kg
        q = self.constants['q']  # C

        # Exhaust velocity (ideal)
        v_e0 = np.sqrt(eta_acc * 2 * q * Vd / m_i)

        # Divergence efficiency
        eta_div = self.calculate_divergence_efficiency(divergence_model, divergence_param, 'hall')

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
        """Perform parametric sweep for ion engine"""
        ion_config = self.config['ion_engine']
        Va_range = np.linspace(ion_config['Va_range'][0], ion_config['Va_range'][1], ion_config['Va_steps'])
        Ib_range = np.logspace(np.log10(ion_config['Ib_range'][0]), np.log10(ion_config['Ib_range'][1]), ion_config['Ib_steps'])

        results = []
        for gas in self.gases:
            for Va in Va_range:
                for Ib in Ib_range:
                    result = self.calculate_ion_engine(
                        Va, Ib, gas,
                        ion_config['tau_open'],
                        ion_config['tau_trans'],
                        ion_config['divergence']['model'],
                        ion_config['divergence']['param_deg']
                    )
                    results.append(result)

        return results

    def parametric_sweep_hall(self):
        """Perform parametric sweep for Hall thruster"""
        hall_config = self.config['hall_thruster']
        Vd_range = np.linspace(hall_config['Vd_range'][0], hall_config['Vd_range'][1], hall_config['Vd_steps'])
        mdot_range = np.logspace(np.log10(hall_config['mdot_range'][0]), np.log10(hall_config['mdot_range'][1]), hall_config['mdot_steps'])

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

if __name__ == "__main__":
    calc = PropulsionCalculator()
    print("Ion engine example:")
    ion_result = calc.calculate_ion_engine(2000, 2.0, 'Xenon', 0.7, 0.95, 'gaussian', 5.0)
    print(f"Thrust: {ion_result['T_axial']:.3f} N, Isp: {ion_result['Isp_ax']:.1f} s")

    print("\nHall thruster example:")
    hall_result = calc.calculate_hall_thruster(400, 5e-6, 'Xenon', 0.6, 0.85, 'cos', 30.0)
    print(f"Thrust: {hall_result['T_axial']:.3f} N, Isp: {hall_result['Isp_ax']:.1f} s")
