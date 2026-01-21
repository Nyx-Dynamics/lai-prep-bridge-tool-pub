#!/usr/bin/env python3
"""
LAI-PrEP Figure 5: Intervention Impact (Forest Plot)
=====================================================
Two-panel forest plot showing absolute and relative improvement by population

Author: Adrian C. Demidont, DO
Affiliation: Nyx Dynamics LLC
Date: January 2026
"""

import os
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import rcParams

# Create output directory
os.makedirs('figures', exist_ok=True)

# MDPI Typography Standards
rcParams.update({
    "font.family": "sans-serif",
    "font.sans-serif": ["Arial", "Helvetica", "DejaVu Sans"],
    "font.size": 8.0,
    "axes.labelsize": 8.0,
    "axes.titlesize": 9.0,
    "axes.labelweight": "bold",
    "axes.titleweight": "bold",
    "axes.linewidth": 1.2,
    "xtick.labelsize": 8.0,
    "ytick.labelsize": 8.0,
    "xtick.major.width": 1.0,
    "ytick.major.width": 1.0,
    "legend.fontsize": 8.0,
    "figure.dpi": 300,
    "savefig.dpi": 600,
    "savefig.bbox": "tight",
    "savefig.facecolor": "white"
})

# Okabe-Ito colorblind-safe palette
COLORS = {
    'blue': "#0072B2",
    'orange': "#E69F00",
    'green': "#009E73",
    'purple': "#CC79A7",
    'red': "#D55E00",
    'cyan': "#56B4E9",
    'grey': "#9E9E9E",
    'dark': "#4D4D4D",
    'light': "#F7F7F7",
    'band': "#B0B0B0"
}


def make_figure5_interventions():
    """
    Two-panel forest plot showing absolute and relative improvement by population
    Matches existing figure5_interventions.png - removes faint gray annotation text
    """
    print("Creating Figure 5: Interventions...")

    populations = ["PWID", "Adolescents", "Cisgender women", "Pregnant/lactating",
                   "Transgender women", "General population", "MSM"]
    absolute_imp = [27.46, 23.96, 23.96, 15.33, 15.36, 15.35, 15.35]
    relative_imp = [265, 147, 99, 64, 54, 49, 46]

    # Marker sizes proportional to population (visual approximation)
    marker_sizes = [80, 100, 180, 120, 120, 150, 200]

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 7), sharey=True)

    y_pos = np.arange(len(populations))

    # Panel A: Absolute Improvement
    # Color gradient based on improvement (orange for high, blue for others)
    colors_abs = ['#4D4D4D' if imp > 25 else ('#E69F00' if imp > 20 else COLORS['cyan'])
                  for imp in absolute_imp]

    for i, (imp, size, color) in enumerate(zip(absolute_imp, marker_sizes, colors_abs)):
        ax1.scatter(imp, i, s=size, c=color, edgecolors='black', linewidth=1, zorder=5)
        # Horizontal line to y-axis
        ax1.plot([0, imp], [i, i], color='black', lw=1, zorder=1)
        # Value label
        ax1.text(imp + 0.8, i, f'{imp:.2f}', va='center', fontsize=9, fontweight='bold')

    # Reference line at 15 points (clinical significance) - NO TEXT LABEL
    ax1.axvline(x=15, color='gray', linestyle='--', linewidth=1.5, alpha=0.7, zorder=2)

    ax1.set_xlim(0, 30)
    ax1.set_xlabel('Absolute Improvement (percentage points)', fontsize=11, fontweight='bold')
    ax1.set_title('Absolute Improvement', fontsize=12, fontweight='bold')
    ax1.set_yticks(y_pos)
    ax1.set_yticklabels(populations, fontsize=10)

    # Panel B: Relative Improvement
    colors_rel = ['darkred' if imp > 200 else ('#E69F00' if imp > 100 else COLORS['cyan'])
                  for imp in relative_imp]

    for i, (imp, size, color) in enumerate(zip(relative_imp, marker_sizes, colors_rel)):
        # Use squares for relative improvement
        ax2.scatter(imp, i, s=size, c=color, marker='s', edgecolors='black', linewidth=1, zorder=5)
        # Horizontal line to y-axis
        ax2.plot([0, imp], [i, i], color='black', lw=1, zorder=1)
        # Value label
        ax2.text(imp + 5, i, f'{imp}%', va='center', fontsize=9, fontweight='bold')

    # Reference line at 100% (doubling) - NO TEXT LABEL
    ax2.axvline(x=100, color='gray', linestyle='--', linewidth=1.5, alpha=0.7, zorder=2)

    ax2.set_xlim(0, 300)
    ax2.set_xlabel('Relative Improvement (%)', fontsize=11, fontweight='bold')
    ax2.set_title('Relative Improvement', fontsize=12, fontweight='bold')

    # Main title
    fig.suptitle('Intervention Effectiveness by Population Group\n(Forest Plot)',
                 fontsize=14, fontweight='bold', y=0.98)

    # Footnote with dotted line explanations
    fig.text(0.5, 0.02,
             'Marker size proportional to population size at 21.2M scale. Dashed lines indicate clinical significance threshold (15 pts) and doubling of success rate (100%).',
             ha='center', fontsize=9, style='italic', color='#4D4D4D')

    plt.tight_layout(rect=[0, 0.05, 1, 0.93])
    fig.savefig('figures/Figure5_Interventions.pdf', bbox_inches='tight')
    fig.savefig('figures/Figure5_Interventions.png', dpi=600, bbox_inches='tight')
    plt.close()
    print("✓ Figure 5 complete")


if __name__ == "__main__":
    make_figure5_interventions()
