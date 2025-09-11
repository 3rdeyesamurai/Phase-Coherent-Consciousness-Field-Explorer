import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Ellipse, Rectangle, Circle

class EMRBodyModel:
    """
    2D Human Body Model for EMR Suit Visualization
    Provides detailed silhouette with anatomical features and thrust pod positions
    """

    def __init__(self, figsize=(10, 12)):
        self.figsize = figsize
        self.thrust_pods = {
            'left_arm': {'pos': (0.3, 0.7), 'radius': 0.03},
            'right_arm': {'pos': (0.7, 0.7), 'radius': 0.03},
            'left_leg': {'pos': (0.35, 0.3), 'radius': 0.03},
            'right_leg': {'pos': (0.65, 0.3), 'radius': 0.03},
            'back': {'pos': (0.5, 0.6), 'radius': 0.04}
        }

    def create_body_silhouette(self, ax, view='front'):
        """
        Create detailed 2D human body silhouette
        """
        # Head (ellipse)
        head = Ellipse((0.5, 0.85), 0.15, 0.18, facecolor='lightblue', edgecolor='black', linewidth=2)
        ax.add_patch(head)

        # Neck (rectangle)
        neck = Rectangle((0.475, 0.75), 0.05, 0.08, facecolor='lightblue', edgecolor='black', linewidth=2)
        ax.add_patch(neck)

        # Torso (trapezoid with rounded shoulders)
        if view == 'front':
            # Front view torso
            torso_x = [0.4, 0.6, 0.65, 0.35]
            torso_y = [0.75, 0.75, 0.35, 0.35]
        else:
            # Back view torso
            torso_x = [0.35, 0.65, 0.7, 0.3]
            torso_y = [0.75, 0.75, 0.35, 0.35]

        ax.fill(torso_x, torso_y, 'lightblue', edgecolor='black', linewidth=2)

        # Arms
        if view == 'front':
            # Left arm
            arm_left_x = [0.35, 0.25, 0.25, 0.35]
            arm_left_y = [0.7, 0.7, 0.4, 0.4]
            ax.fill(arm_left_x, arm_left_y, 'lightblue', edgecolor='black', linewidth=2)

            # Right arm
            arm_right_x = [0.65, 0.75, 0.75, 0.65]
            arm_right_y = [0.7, 0.7, 0.4, 0.4]
            ax.fill(arm_right_x, arm_right_y, 'lightblue', edgecolor='black', linewidth=2)
        else:
            # Back view - arms partially visible
            arm_left_x = [0.3, 0.2, 0.2, 0.3]
            arm_left_y = [0.65, 0.65, 0.45, 0.45]
            ax.fill(arm_left_x, arm_left_y, 'lightgray', edgecolor='black', linewidth=2)

            arm_right_x = [0.7, 0.8, 0.8, 0.7]
            arm_right_y = [0.65, 0.65, 0.45, 0.45]
            ax.fill(arm_right_x, arm_right_y, 'lightgray', edgecolor='black', linewidth=2)

        # Legs
        # Left leg
        leg_left_x = [0.42, 0.48, 0.48, 0.42]
        leg_left_y = [0.35, 0.35, 0.05, 0.05]
        ax.fill(leg_left_x, leg_left_y, 'lightblue', edgecolor='black', linewidth=2)

        # Right leg
        leg_right_x = [0.52, 0.58, 0.58, 0.52]
        leg_right_y = [0.35, 0.35, 0.05, 0.05]
        ax.fill(leg_right_x, leg_right_y, 'lightblue', edgecolor='black', linewidth=2)

        # Joints (circles)
        joints = [
            (0.5, 0.75),   # Shoulders
            (0.45, 0.35),  # Hips
            (0.55, 0.35),
            (0.45, 0.05),  # Knees
            (0.55, 0.05),
            (0.3, 0.55),   # Elbows (front view)
            (0.7, 0.55)
        ]

        for joint in joints:
            ax.add_patch(Circle(joint, 0.015, facecolor='white', edgecolor='black', linewidth=1))

    def add_thrust_pods(self, ax, pod_status=None):
        """
        Add thrust pods to the body model
        """
        if pod_status is None:
            pod_status = {pod: True for pod in self.thrust_pods.keys()}

        for pod_name, pod_info in self.thrust_pods.items():
            color = 'red' if pod_status.get(pod_name, True) else 'gray'
            ax.add_patch(Circle(pod_info['pos'], pod_info['radius'],
                              facecolor=color, edgecolor='darkred', linewidth=2))

    def get_body_regions(self):
        """
        Define body regions for heatmap overlay
        """
        regions = {
            'head': {'x': [0.425, 0.575], 'y': [0.8, 0.95]},
            'torso': {'x': [0.35, 0.65], 'y': [0.35, 0.75]},
            'left_arm': {'x': [0.2, 0.4], 'y': [0.4, 0.7]},
            'right_arm': {'x': [0.6, 0.8], 'y': [0.4, 0.7]},
            'left_leg': {'x': [0.4, 0.5], 'y': [0.05, 0.35]},
            'right_leg': {'x': [0.5, 0.6], 'y': [0.05, 0.35]}
        }
        return regions

    def setup_plot(self, ax, title="EMR Suit Body Model"):
        """
        Setup plot parameters
        """
        ax.set_xlim(0, 1)
        ax.set_ylim(0, 1)
        ax.set_aspect('equal')
        ax.axis('off')
        ax.set_title(title, fontsize=14, fontweight='bold')
