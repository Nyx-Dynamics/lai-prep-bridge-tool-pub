#!/usr/bin/env python3
"""
LAI-PrEP Bridge Period Decision Tool - Figure 7: Barrier Dose-Response
=======================================================================
MDPI Viruses Manuscript

Generates Figure 7: Barrier Dose-Response Relationship
Shows inverse relationship between number of barriers and success rate
with regression line and patient distribution inset

Author: Adrian C. Demidont, DO
Affiliation: Nyx Dynamics LLC
Date: January 2026
Output: PDF (vector) + PNG (600 dpi)
"""

import os
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import rcParams
import warnings

warnings.filterwarnings('ignore')

# Output directory
OUTPUT_DIR = '/SCR/figures'
os.makedirs(OUTPUT_DIR, exist_ok=True)

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


def make_figure7_barriers():
    """
    Shows inverse relationship between number of barriers and success rate
    with regression line and patient distribution inset
    """
    print("Creating Figure 7: Barriers...")

    # Data from validation tiers
    barriers = np.array([0, 1, 2, 3, 4, 5])

    # Success rates from validation
    tier2_success = np.array([44.0, 33.6, 23.5, 14.8, 8.1, 5.3])
    tier3_success = np.array([44.0, 33.6, 23.5, 14.8, 8.1, 5.3])
    tier4_success = np.array([43.996, 33.614, 23.497, 14.794, 8.098, 5.281])

    # Patient distribution by barrier count
    barrier_dist = np.array([15, 25, 30, 18, 8, 4])

    fig, ax = plt.subplots(figsize=(8, 6), dpi=300)

    # Plot data points from validation tiers
    ax.scatter(barriers, tier2_success, s=100, c=COLORS['cyan'], marker='o',
               label='Tier 2 (1M)', alpha=0.8, edgecolors='black', linewidth=1)
    ax.scatter(barriers, tier3_success, s=100, c=COLORS['green'], marker='^',
               label='Tier 3 (10M)', alpha=0.8, edgecolors='black', linewidth=1)
    ax.scatter(barriers, tier4_success, s=120, c=COLORS['red'], marker='s',
               label='Tier 4 (21.2M)', alpha=0.8, edgecolors='darkred', linewidth=1.5)

    # Regression line
    z = np.polyfit(barriers, tier4_success, 1)
    p = np.poly1d(z)
    x_line = np.linspace(0, 5, 100)
    ax.plot(x_line, p(x_line), '--', color='black', lw=2,
            label=f'Regression: y = {z[1]:.1f} - {abs(z[0]):.2f}x')

    # Critical threshold annotation
    ax.axhline(y=24, color='gray', linestyle=':', lw=1.5, alpha=0.7)
    ax.text(5.1, 24.5, 'Current baseline\n(24%)', fontsize=8, va='bottom', style='italic')

    ax.set_xlabel('Number of Structural Barriers', fontsize=11, fontweight='bold')
    ax.set_ylabel('Success Rate (%)', fontsize=11, fontweight='bold')
    ax.set_title('Structural Barrier Dose-Response Relationship', fontsize=12, fontweight='bold')
    ax.grid(True, alpha=0.3, linestyle='--')
    ax.set_xlim(-0.2, 5.2)
    ax.set_ylim(0, 50)
    ax.legend(loc='upper right', fontsize=9)

    # Inset: Patient distribution
    inset_ax = fig.add_axes([0.18, 0.18, 0.25, 0.22])
    bars = inset_ax.bar(range(6), barrier_dist, color='lightblue', edgecolor='black', linewidth=1)
    inset_ax.set_xlabel('Barriers', fontsize=8)
    inset_ax.set_ylabel('% Patients', fontsize=8)
    inset_ax.set_title('Distribution', fontsize=9, fontweight='bold')
    inset_ax.set_ylim(0, 35)
    inset_ax.grid(True, alpha=0.3, axis='y')

    # Average decline annotation
    ax.annotate(f'Average decline:\n{abs(z[0]):.2f} pp/barrier',
                xy=(2, 25), xytext=(1.5, 38),
                bbox=dict(boxstyle='round', facecolor='yellow', alpha=0.8),
                fontsize=10, fontweight='bold',
                arrowprops=dict(arrowstyle='->', lw=1.5))

    plt.tight_layout()

    # Save outputs
    pdf_path = os.path.join(OUTPUT_DIR, 'Figure7_Barriers.pdf')
    png_path = os.path.join(OUTPUT_DIR, 'Figure7_Barriers.png')

    fig.savefig(pdf_path, bbox_inches='tight')
    fig.savefig(png_path, dpi=600, bbox_inches='tight')
    plt.close()

    print(f"✓ Figure 7 complete")
    print(f"  → {pdf_path}")
    print(f"  → {png_path}")


if __name__ == "__main__":
    print("=" * 60)
    print("LAI-PrEP Bridge Tool - Figure 7 Generation")
    print("=" * 60)
    make_figure7_barriers()
    print("\nDone!")
