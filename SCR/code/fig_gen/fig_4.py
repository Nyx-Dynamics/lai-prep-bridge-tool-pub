#!/usr/bin/env python3
"""
LAI-PrEP Figure 4: Population-Specific Success Rates
=====================================================
Horizontal paired bars: Baseline vs With Interventions for each population
With improvement gap indicators and *** significance markers

Author: Adrian C. Demidont, DO
Affiliation: Nyx Dynamics LLC
Date: January 2026
"""

import os
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import rcParams

# Create output directory
output_dir = '../figures'
os.makedirs(output_dir, exist_ok=True)

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


def make_figure4_populations():
    """
    Horizontal paired bars: Baseline vs With Interventions for each population
    """
    print("Creating Figure 4: Populations...")

    populations = ["MSM", "General\npopulation", "Transgender\nwomen",
                   "Pregnant/\nlactating", "Cisgender\nwomen", "Adolescents\n(16-24y)", "PWID"]
    baseline = np.array([33.11, 31.22, 28.46, 24.11, 24.10, 16.34, 10.36])
    with_int = np.array([48.46, 46.57, 43.82, 39.44, 48.06, 40.30, 37.82])
    ci_half = np.array([1.6, 1.7, 1.6, 1.4, 1.4, 1.3, 1.2])

    fig = plt.figure(figsize=(7.09, 4.72), dpi=300)
    ax = fig.add_subplot(111)

    y = np.arange(len(populations))[::-1]
    bar_h = 0.34

    # Baseline bars
    ax.barh(y - bar_h / 2, baseline, height=bar_h, color=COLORS['grey'],
            edgecolor="black", linewidth=0.6, zorder=2, label='Baseline')
    # With-interventions bars
    ax.barh(y + bar_h / 2, with_int, height=bar_h, color="#FFFFFF",
            edgecolor="#444444", linewidth=0.8, hatch="///", zorder=3, label='With Interventions')

    # CI whiskers
    for yi, mu, hw in zip(y + bar_h / 2, with_int, ci_half):
        ax.plot([mu - hw, mu + hw], [yi, yi], color="#444444", lw=0.9, zorder=4)
        ax.plot([mu - hw, mu - hw], [yi - 0.08, yi + 0.08], color="#444444", lw=0.9, zorder=4)
        ax.plot([mu + hw, mu + hw], [yi - 0.08, yi + 0.08], color="#444444", lw=0.9, zorder=4)

    ax.set_xlim(0, 55)
    ax.set_xticks(np.arange(0, 56, 10))
    ax.set_yticks(y)
    ax.set_yticklabels(populations)
    ax.set_xlabel("Success Rate (%)", fontweight='bold')
    ax.set_ylabel("Population", fontweight='bold')
    ax.tick_params(axis='y', length=0)
    ax.legend(loc='lower right', fontsize=8)

    plt.subplots_adjust(bottom=0.12, left=0.2, right=0.96, top=0.97)
    fig.savefig(os.path.join(output_dir, 'Figure4_Populations.pdf'), bbox_inches='tight')
    fig.savefig(os.path.join(output_dir, 'Figure4_Populations.png'), dpi=600, bbox_inches='tight')
    plt.close()
    print("✓ Figure 4 complete")


if __name__ == "__main__":
    make_figure4_populations()
