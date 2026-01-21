#!/usr/bin/env python3
"""
LAI-PrEP Bridge Period Decision Tool - Figure 8: Global Impact Projections
===========================================================================
MDPI Viruses Manuscript

Generates Figure 8: Global Impact Projections
Multi-panel figure showing projected impact at UNAIDS scale:
  A) Success Rate Improvement
  B) Projected HIV Infections Prevented
  C) 5-Year Cost Analysis
  D) UNAIDS 2025 Target Progress

Author: Adrian C. Demidont, DO
Affiliation: Nyx Dynamics LLC
Date: January 2026
Output: PDF (vector) + PNG (600 dpi)
"""

import os
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
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


def make_figure8_impact():
    """
    Multi-panel figure showing projected impact at UNAIDS scale
    """
    print("Creating Figure 8: Impact...")

    fig = plt.figure(figsize=(12, 8), dpi=300)

    # Panel A: Cascade improvement
    ax1 = fig.add_subplot(2, 2, 1)
    categories = ['Current\nBaseline', 'With Tool\nImplementation']
    values = [24, 44]
    colors_bar = [COLORS['grey'], COLORS['green']]
    bars = ax1.bar(categories, values, color=colors_bar, edgecolor='black', lw=1.5)
    ax1.set_ylabel('Bridge Period Success (%)', fontweight='bold')
    ax1.set_ylim(0, 55)
    ax1.set_title('A. Success Rate Improvement', fontweight='bold')
    ax1.annotate('+83%\nimprovement', xy=(1, 44), xytext=(1, 50),
                 ha='center', fontsize=10, fontweight='bold', color=COLORS['red'])

    # Panel B: Infections prevented
    ax2 = fig.add_subplot(2, 2, 2)
    years = ['Year 1', 'Year 2', 'Year 3', 'Year 4', 'Year 5']
    infections_prevented = [80, 160, 240, 320, 400]  # thousands, cumulative
    ax2.fill_between(range(5), infections_prevented, color=COLORS['green'], alpha=0.3)
    ax2.plot(range(5), infections_prevented, 'o-', color=COLORS['green'], lw=2, markersize=8)
    ax2.set_xticks(range(5))
    ax2.set_xticklabels(years)
    ax2.set_ylabel('Cumulative Infections Prevented (K)', fontweight='bold')
    ax2.set_title('B. Projected HIV Infections Prevented', fontweight='bold')
    ax2.set_ylim(0, 500)
    ax2.grid(True, alpha=0.3)

    # Panel C: Cost savings
    ax3 = fig.add_subplot(2, 2, 3)
    cost_categories = ['Implementation\nCost', 'Healthcare\nSavings']
    cost_values = [4, 44]  # billions
    colors_cost = [COLORS['red'], COLORS['green']]
    ax3.bar(cost_categories, cost_values, color=colors_cost, edgecolor='black', lw=1.5)
    ax3.set_ylabel('Billions USD', fontweight='bold')
    ax3.set_title('C. 5-Year Cost Analysis', fontweight='bold')
    ax3.annotate('11:1 ROI', xy=(0.5, 30), fontsize=14, fontweight='bold',
                 ha='center', color=COLORS['blue'])

    # Panel D: UNAIDS gap closure
    ax4 = fig.add_subplot(2, 2, 4)
    ax4.axis('off')

    # Progress bar
    bar_y = 0.5
    bar_height = 0.15
    # Background
    ax4.add_patch(Rectangle((0.1, bar_y), 0.8, bar_height, facecolor='lightgray',
                            edgecolor='black', lw=2, transform=ax4.transAxes))
    # Filled portion (23.4%)
    ax4.add_patch(Rectangle((0.1, bar_y), 0.8 * 0.234, bar_height, facecolor=COLORS['green'],
                            edgecolor='black', lw=2, transform=ax4.transAxes))

    ax4.text(0.5, 0.75, '23.4% of UNAIDS Gap Closed', ha='center', va='center',
             fontsize=14, fontweight='bold', transform=ax4.transAxes)
    ax4.text(0.5, 0.25, 'Current: 3.5-3.8M | Target: 21.2M | Gap: 17.7M\nThis intervention: +4.1M transitions',
             ha='center', va='center', fontsize=10, style='italic', transform=ax4.transAxes)
    ax4.set_title('D. UNAIDS 2025 Target Progress', fontweight='bold', y=0.95)

    plt.tight_layout()

    # Save outputs
    pdf_path = os.path.join(OUTPUT_DIR, 'Figure8_Impact.pdf')
    png_path = os.path.join(OUTPUT_DIR, 'Figure8_Impact.png')

    fig.savefig(pdf_path, bbox_inches='tight')
    fig.savefig(png_path, dpi=600, bbox_inches='tight')
    plt.close()

    print(f"✓ Figure 8 complete")
    print(f"  → {pdf_path}")
    print(f"  → {png_path}")


if __name__ == "__main__":
    print("=" * 60)
    print("LAI-PrEP Bridge Tool - Figure 8 Generation")
    print("=" * 60)
    make_figure8_impact()
    print("\nDone!")
