#!/usr/bin/env python3
"""
LAI-PrEP Bridge Period Decision Tool - Figure 2: Tool Workflow Diagram
=======================================================================
MDPI Viruses Manuscript

Generates Figure 2: Tool Workflow Diagram
Five stages as numbered rounded rectangles with vertical flow:
  1) Patient Presentation
  2) Risk Stratification
  3) Barrier Assessment
  4) Intervention Recommendation
  5) Outcome Prediction

Author: Adrian C. Demidont, DO
Affiliation: Nyx Dynamics LLC
Date: January 2026
Output: PDF (vector) + PNG (600 dpi)
"""

import os
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Circle
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


def make_figure2_workflow():
    """
    MDPI-style minimal-text workflow schematic:
    Five stages as numbered rounded rectangles with vertical flow
    """
    print("Creating Figure 2: Workflow...")

    fig, ax = plt.subplots(figsize=(7.09, 4.72), dpi=300)
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)
    ax.axis('off')

    y_positions = [8.5, 6.9, 5.3, 3.7, 2.1]
    labels = ["Patient\nPresentation", "Risk\nStratification", "Barrier\nAssessment",
              "Intervention\nRecommendation", "Outcome\nPrediction"]
    colors = [COLORS['cyan'], COLORS['orange'], COLORS['red'], COLORS['purple'], COLORS['green']]

    for i, (y, lab, col) in enumerate(zip(y_positions, labels, colors), start=1):
        # Main box
        box = FancyBboxPatch((2, y - 0.7), 6, 1.2, boxstyle="round,pad=0.02,rounding_size=0.2",
                             linewidth=1.2, edgecolor="#333333", facecolor=col, alpha=0.95)
        ax.add_patch(box)

        # Number circle
        circ = Circle((1.1, y - 0.1), radius=0.28, facecolor=col, edgecolor="#333333", linewidth=1.0)
        ax.add_patch(circ)
        ax.text(1.1, y - 0.1, str(i), va='center', ha='center', fontsize=9, fontweight='bold', color='white')

        # Label text
        ax.text(5, y - 0.1, lab, va='center', ha='center', fontsize=9, fontweight='bold', color='white')

        # Arrow to next stage (except for the last one)
        if i < 5:
            ax.annotate('', xy=(5, y - 0.9), xytext=(5, y - 0.7),
                        arrowprops=dict(arrowstyle='->', color='#333333', lw=1.5))

    # Title
    ax.text(5, 9.5, "LAI-PrEP Bridge Period Decision Tool Workflow",
            va='center', ha='center', fontsize=11, fontweight='bold', color=COLORS['dark'])

    # Save outputs
    pdf_path = os.path.join(OUTPUT_DIR, 'Figure2_Workflow.pdf')
    png_path = os.path.join(OUTPUT_DIR, 'Figure2_Workflow.png')

    fig.savefig(pdf_path, bbox_inches='tight')
    fig.savefig(png_path, dpi=600, bbox_inches='tight')
    plt.close()

    print(f"✓ Figure 2 complete")
    print(f"  → {pdf_path}")
    print(f"  → {png_path}")


if __name__ == "__main__":
    print("=" * 60)
    print("LAI-PrEP Bridge Tool - Figure 2 Generation")
    print("=" * 60)
    make_figure2_workflow()
    print("\nDone!")
