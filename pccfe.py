#!/usr/bin/env python3
"""
Phase-Coherent Consciousness Field Explorer (PCCFE)
Interactive application visualizing the brain-as-harmonic-emitter model from UHFF and IHRT.
Integrates concepts like universal field, standing waves, interference, golden ratio, torus knots, etc.
"""

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import pygame
import scipy.signal
from scipy.integrate import quad
import tkinter as tk
from tkinter import filedialog
import random
import threading
import time
import io

# Constants
PHI = (1 + np.sqrt(5)) / 2  # Golden ratio
CM = 3 / PHI  # Corrective mirror constant
PI = np.pi

class PCCFE:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((1200, 800))
        pygame.display.set_caption("Phase-Coherent Consciousness Field Explorer")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont(None, 24)

        # Parameters
        self.emotion_params = {'calm': 0.5, 'focused': 0.5, 'anxious': 0.5}
        self.phase_shift = 0.0
        self.amplitude = 1.0
        self.frequency = 1.0
        self.coherence = 0.5
        self.mode = 'brain'  # brain, quantum, multi, biofield

        # Data for simulations
        self.eeg_data = None
        self.rng_entropy = []

        # UI elements
        self.buttons = {}
        self.sliders = {}
        self.setup_ui()

        # Matplotlib figures
        self.fig_brain = plt.figure(figsize=(6, 4))
        self.ax_brain = self.fig_brain.add_subplot(111, projection='3d')

        self.fig_quantum = plt.figure(figsize=(6, 4))
        self.ax_quantum = self.fig_quantum.add_subplot(111)

        self.fig_multi = plt.figure(figsize=(6, 4))
        self.ax_multi = self.fig_multi.add_subplot(111, projection='3d')

        self.fig_bio = plt.figure(figsize=(6, 4))
        self.ax_bio = self.fig_bio.add_subplot(111)

    def setup_ui(self):
        # Buttons: dict of {'rect': pygame.Rect, 'text': str, 'action': func}
        self.buttons = {
            'brain': {'rect': pygame.Rect(10, 10, 100, 50), 'text': 'Brain Model', 'action': lambda: setattr(self, 'mode', 'brain')},
            'quantum': {'rect': pygame.Rect(120, 10, 100, 50), 'text': 'Quantum', 'action': lambda: setattr(self, 'mode', 'quantum')},
            'multi': {'rect': pygame.Rect(230, 10, 100, 50), 'text': 'Multi-Domain', 'action': lambda: setattr(self, 'mode', 'multi')},
            'biofield': {'rect': pygame.Rect(340, 10, 100, 50), 'text': 'Biofield', 'action': lambda: setattr(self, 'mode', 'biofield')},
            'load_eeg': {'rect': pygame.Rect(10, 250, 100, 50), 'text': 'Load EEG', 'action': self.load_eeg_data},
            'export': {'rect': pygame.Rect(120, 250, 100, 50), 'text': 'Export', 'action': self.export_data}
        }

        # Sliders: dict of {'rect': pygame.Rect, 'min': float, 'max': float, 'value': float, 'label': str}
        self.sliders = {
            'calm': {'rect': pygame.Rect(10, 70, 200, 20), 'min': 0, 'max': 1, 'value': 0.5, 'label': 'Calm'},
            'focused': {'rect': pygame.Rect(10, 100, 200, 20), 'min': 0, 'max': 1, 'value': 0.5, 'label': 'Focused'},
            'anxious': {'rect': pygame.Rect(10, 130, 200, 20), 'min': 0, 'max': 1, 'value': 0.5, 'label': 'Anxious'},
            'phase': {'rect': pygame.Rect(10, 160, 200, 20), 'min': -PI, 'max': PI, 'value': 0, 'label': 'Phase'},
            'amp': {'rect': pygame.Rect(10, 190, 200, 20), 'min': 0, 'max': 2, 'value': 1, 'label': 'Amp'},
            'freq': {'rect': pygame.Rect(10, 220, 200, 20), 'min': 0.1, 'max': 5, 'value': 1, 'label': 'Freq'}
        }

        self.dragging_slider = None

    def draw_button(self, button):
        """Draw a button."""
        pygame.draw.rect(self.screen, (100, 100, 100), button['rect'])
        pygame.draw.rect(self.screen, (255, 255, 255), button['rect'], 2)
        text_surf = self.font.render(button['text'], True, (255, 255, 255))
        text_rect = text_surf.get_rect(center=button['rect'].center)
        self.screen.blit(text_surf, text_rect)

    def draw_slider(self, slider):
        """Draw a slider."""
        rect = slider['rect']
        pygame.draw.line(self.screen, (255, 255, 255), (rect.left, rect.centery), (rect.right, rect.centery), 2)
        value_ratio = (slider['value'] - slider['min']) / (slider['max'] - slider['min'])
        knob_x = rect.left + int(value_ratio * rect.width)
        pygame.draw.circle(self.screen, (255, 0, 0), (knob_x, rect.centery), 8)
        label_surf = self.font.render(f"{slider['label']}: {slider['value']:.2f}", True, (255, 255, 255))
        self.screen.blit(label_surf, (rect.right + 10, rect.top))

    def handle_mouse_event(self, event):
        """Handle mouse events for UI."""
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            # Check buttons
            for name, button in self.buttons.items():
                if button['rect'].collidepoint(mouse_pos):
                    button['action']()
                    return
            # Check sliders
            for name, slider in self.sliders.items():
                rect = slider['rect']
                if rect.collidepoint(mouse_pos):
                    self.dragging_slider = name
                    self.update_slider_value(name, mouse_pos[0])
                    return
        elif event.type == pygame.MOUSEBUTTONUP:
            self.dragging_slider = None
        elif event.type == pygame.MOUSEMOTION and self.dragging_slider:
            self.update_slider_value(self.dragging_slider, event.pos[0])

    def update_slider_value(self, slider_name, mouse_x):
        """Update slider value based on mouse position."""
        slider = self.sliders[slider_name]
        rect = slider['rect']
        value_ratio = max(0, min(1, (mouse_x - rect.left) / rect.width))
        slider['value'] = slider['min'] + value_ratio * (slider['max'] - slider['min'])

    def universal_field(self, x, t, n_terms=5):
        """Compute universal field U(x,t) with phase shifts modulated by emotions."""
        U = 0
        for n in range(1, n_terms + 1):
            k_n = n * PI / 10  # Wave number
            omega_n = n * 2 * PI * self.frequency
            phi_n = self.phase_shift + self.emotion_params['calm'] * 0.1 * n - self.emotion_params['anxious'] * 0.1 * n
            U += self.amplitude * np.sin(k_n * x - omega_n * t + phi_n)
        return U

    def standing_wave(self, x, t):
        """Compute standing wave Ψ(x,t)."""
        k = PI / 5
        omega = 2 * PI * self.frequency
        return 2 * self.amplitude * np.cos(k * x) * np.sin(omega * t)

    def interference_field(self, x, t, n_terms=3):
        """Compute interference field I(x,t)."""
        I = 0
        for n in range(1, n_terms + 1):
            k_n = n * PI / 10
            omega_n = n * 2 * PI * self.frequency
            phi_n = self.phase_shift
            I += self.amplitude * np.cos(k_n * x - omega_n * t + phi_n)
        return I

    def torus_knot(self, t, p=2, q=3, R=1, r=0.5):
        """Compute torus knot coordinates."""
        x = (R + r * np.cos(q * t)) * np.cos(p * t)
        y = (R + r * np.cos(q * t)) * np.sin(p * t)
        z = r * np.sin(q * t)
        return x, y, z

    def coordinated_rotation(self, theta, t, m1=1, m2=2, sigma=1):
        """Compute coordinated-rotation field."""
        A1, A2 = 1, 1
        omega, nu = 2*PI, 2*PI
        phi0 = 0
        E = A1 * np.exp(1j * (m1 * theta - omega * t)) + A2 * np.exp(1j * (sigma * m2 * theta - nu * t + phi0))
        delta_phi = (m1 - sigma * m2) * theta - (omega - nu) * t + phi0
        return E, delta_phi

    def tonal_torus(self, theta, t, n1=1, n2=2, sigma=1):
        """Compute tonal torus field."""
        B1, B2 = 1, 1
        Omega, Lambda = 2*PI, 2*PI
        phi0 = 0
        S = B1 * np.exp(1j * (n1 * theta - Omega * t)) + B2 * np.exp(1j * (sigma * n2 * theta - Lambda * t + phi0))
        R = 2 * abs(B1 * B2) / (abs(B1)**2 + abs(B2)**2)
        return S, R

    def mass_lattice(self, x_range):
        """Compute mass as standing lattice integral."""
        def integrand(x):
            return abs(self.universal_field(x, 0))**2
        Mh, _ = quad(integrand, x_range[0], x_range[1])
        return Mh

    def entropy_phase_loss(self, phases):
        """Compute entropy as phase-loss."""
        # Simplified entropy calculation
        return np.var(phases)

    def fig_to_surface(self, fig):
        """Convert matplotlib figure to pygame surface."""
        buf = io.BytesIO()
        fig.savefig(buf, format='png', dpi=100, bbox_inches='tight')
        buf.seek(0)
        surf = pygame.image.load(buf)
        buf.close()
        return surf

    def update_brain_model(self):
        """Update brain model visualization."""
        self.ax_brain.clear()
        x = np.linspace(-10, 10, 100)
        t = time.time()
        U = [self.universal_field(xi, t) for xi in x]
        self.ax_brain.plot(x, U, np.zeros_like(x), 'b-')
        self.ax_brain.set_title('Brain Harmonic Field')

    def update_quantum_simulation(self):
        """Update quantum collapse simulation."""
        self.ax_quantum.clear()
        x = np.linspace(0, 10, 100)
        t = time.time()
        psi = [self.standing_wave(xi, t) for xi in x]
        I = [self.interference_field(xi, t) for xi in x]
        self.ax_quantum.plot(x, psi, label='Wavefunction')
        self.ax_quantum.plot(x, I, label='Interference')
        self.ax_quantum.legend()
        self.ax_quantum.set_title('Quantum Collapse Simulation')

    def update_multi_domain(self):
        """Update multi-domain bridging."""
        self.ax_multi.clear()
        t_vals = np.linspace(0, 2*PI, 100)
        x, y, z = self.torus_knot(t_vals)
        self.ax_multi.plot(x, y, z, 'g-')
        self.ax_multi.set_title('Torus Knot Overlay')

    def update_biofield_scanner(self):
        """Update biofield scanner mode."""
        self.ax_bio.clear()
        if self.eeg_data is not None:
            self.ax_bio.plot(self.eeg_data[:, 0], self.eeg_data[:, 1])
        self.ax_bio.set_title('EEG Coherence Heatmap')

    def simulate_rng(self):
        """Simulate RNG modulated by coherence."""
        while True:
            entropy = random.random() * (1 - self.coherence)
            self.rng_entropy.append(entropy)
            if len(self.rng_entropy) > 100:
                self.rng_entropy.pop(0)
            time.sleep(0.1)

    def load_eeg_data(self):
        """Load EEG data from file."""
        root = tk.Tk()
        root.withdraw()
        file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
        if file_path:
            self.eeg_data = np.loadtxt(file_path, delimiter=',')
        root.destroy()

    def export_data(self):
        """Export current visualization."""
        if self.mode == 'brain':
            self.fig_brain.savefig('brain_model.png')
        elif self.mode == 'quantum':
            self.fig_quantum.savefig('quantum_simulation.png')
        elif self.mode == 'multi':
            self.fig_multi.savefig('multi_domain.png')
        elif self.mode == 'biofield':
            self.fig_bio.savefig('biofield_scanner.png')

    def run(self):
        # Start RNG simulation thread
        rng_thread = threading.Thread(target=self.simulate_rng)
        rng_thread.daemon = True
        rng_thread.start()

        running = True
        while running:
            self.clock.tick(60)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                self.handle_mouse_event(event)

            # Update parameters from sliders
            self.emotion_params['calm'] = self.sliders['calm']['value']
            self.emotion_params['focused'] = self.sliders['focused']['value']
            self.emotion_params['anxious'] = self.sliders['anxious']['value']
            self.phase_shift = self.sliders['phase']['value']
            self.amplitude = self.sliders['amp']['value']
            self.frequency = self.sliders['freq']['value']
            self.coherence = (self.emotion_params['calm'] + self.emotion_params['focused']) / 2

            # Clear screen
            self.screen.fill((0, 0, 0))

            # Draw UI
            for button in self.buttons.values():
                self.draw_button(button)
            for slider in self.sliders.values():
                self.draw_slider(slider)

            # Update visualizations
            if self.mode == 'brain':
                self.update_brain_model()
                surf = self.fig_to_surface(self.fig_brain)
                self.screen.blit(surf, (300, 100))
            elif self.mode == 'quantum':
                self.update_quantum_simulation()
                surf = self.fig_to_surface(self.fig_quantum)
                self.screen.blit(surf, (300, 100))
            elif self.mode == 'multi':
                self.update_multi_domain()
                surf = self.fig_to_surface(self.fig_multi)
                self.screen.blit(surf, (300, 100))
            elif self.mode == 'biofield':
                self.update_biofield_scanner()
                surf = self.fig_to_surface(self.fig_bio)
                self.screen.blit(surf, (300, 100))

            # Display metrics
            entropy_text = self.font.render(f'Entropy: {self.entropy_phase_loss([self.phase_shift]):.3f}', True, (255, 255, 255))
            self.screen.blit(entropy_text, (10, 300))
            coherence_text = self.font.render(f'Coherence: {self.coherence:.3f}', True, (255, 255, 255))
            self.screen.blit(coherence_text, (10, 330))
            mass_text = self.font.render(f'Mass Lattice: {self.mass_lattice([-10, 10]):.3f}', True, (255, 255, 255))
            self.screen.blit(mass_text, (10, 360))

            pygame.display.flip()

        pygame.quit()

if __name__ == "__main__":
    app = PCCFE()
    app.run()
