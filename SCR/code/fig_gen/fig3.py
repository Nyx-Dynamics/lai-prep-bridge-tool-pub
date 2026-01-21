
#!/usr/bin/env python3
"""
LAI-PrEP Figure 3: Progressive Validation Convergence
=====================================================
Dual-axis plot showing margin of error convergence and processing speed
across validation tiers: 1K, 1M, 10M, 21.2M patients

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


def make_figure3_convergence():
    """
    Dual-axis plot showing margin of error convergence and processing speed
    across validation tiers: 1K, 1M, 10M, 21.2M patients
    """
    print("Creating Figure 3: Progressive Validation Convergence...")

    x_labels = ["1K", "1M", "10M", "21.2M"]
    x = np.arange(len(x_labels))
    margin_error_pp = np.array([2.6, 0.09, 0.028, 0.018])
    processing_speed = np.array([1000, 10870, 98040, 83800])

    fig, ax1 = plt.subplots(figsize=(7.09, 4.72), dpi=300)

    # Left axis: Margin of Error (log scale)
    ax1.set_yscale('log')
    ax1.plot(x, margin_error_pp, color=COLORS['red'], marker='o', markersize=8, lw=2.0, label='Margin of Error')
    ax1.set_xlim(-0.3, len(x_labels) - 0.7)
    ax1.set_xticks(x)
    ax1.set_xticklabels(x_labels)
    ax1.set_xlabel("Validation Scale (patients)", fontweight='bold')
    ax1.set_ylabel("Margin of Error (± pp, log)", fontweight='bold', color=COLORS['red'])
    ax1.tick_params(axis='y', labelcolor=COLORS['red'])

    # Policy-grade precision zone (green shading from 0.01 to 0.05 pp)
    ax1.axhspan(0.01, 0.05, color="#A5D6A7", alpha=0.35, zorder=0)

    # Policy-grade label - positioned at (10^-2, 10M) which is x=2 (10M), y=0.01
    ax1.text(2, 0.01, "Policy-Grade Precision Zone", fontsize=8, fontweight='bold',
             ha='center', va='bottom',
             bbox=dict(boxstyle='round,pad=0.4', facecolor='white', edgecolor='#2E7D32',
                       linewidth=1.2, alpha=0.95))

    # Right axis: Processing speed
    ax2 = ax1.twinx()
    ax2.plot(x, processing_speed, color=COLORS['blue'], marker='s', markersize=8, lw=2.0, linestyle='--',
             label='Processing Speed')
    ax2.set_ylabel("Throughput (patients/s)", fontweight='bold', color=COLORS['blue'])
    ax2.tick_params(axis='y', labelcolor=COLORS['blue'])

    # Value annotations - custom positioning for each
    for i, (xe, ye) in enumerate(zip(x, margin_error_pp)):
        if i == 0:  # 1K - offset right of node
            ax1.annotate(f'±{ye:.3f}', xy=(xe, ye), xytext=(9, 0), textcoords='offset points',
                         ha='left', fontsize=7, fontweight='bold',
                         bbox=dict(boxstyle='round,pad=0.3', facecolor='white', edgecolor='gray', alpha=0.9))
        elif i == 3:  # 21.2M - place below node
            ax1.annotate(f'±{ye:.3f}', xy=(xe, ye), xytext=(0, -18), textcoords='offset points',
                         ha='center', fontsize=7, fontweight='bold',
                         bbox=dict(boxstyle='round,pad=0.3', facecolor='white', edgecolor='gray', alpha=0.9))
        else:  # Others - place above node
            ax1.annotate(f'±{ye:.3f}', xy=(xe, ye), xytext=(0, 12), textcoords='offset points',
                         ha='center', fontsize=7, fontweight='bold',
                         bbox=dict(boxstyle='round,pad=0.3', facecolor='white', edgecolor='gray', alpha=0.9))

    # 144× improvement annotation
    ax1.annotate('144× precision\nimprovement', xy=(3, 0.018), xytext=(2.2, 0.25),
                 arrowprops=dict(arrowstyle='->', lw=1.5, color='black'),
                 fontsize=9, fontweight='bold', ha='center',
                 bbox=dict(boxstyle='round,pad=0.4', facecolor='lightyellow', edgecolor='black',
                           linewidth=1, alpha=0.95))

    ax1.grid(True, which='both', axis='y', linestyle=':', linewidth=0.6, alpha=0.5)

    # Combined legend
    lines1, labels1 = ax1.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax1.legend(lines1 + lines2, labels1 + labels2, loc='upper right', fontsize=8)

    plt.subplots_adjust(bottom=0.12, left=0.12, right=0.88, top=0.96)
    fig.savefig(os.path.join(output_dir, 'Figure3_Progressive_Validation_Convergence.pdf'), bbox_inches='tight')
    fig.savefig(os.path.join(output_dir, 'Figure3_Progressive_Validation_Convergence.png'), dpi=600, bbox_inches='tight')
    plt.close()
    print("✓ Figure 3 complete")


if __name__ == "__main__":
    make_figure3_convergence()