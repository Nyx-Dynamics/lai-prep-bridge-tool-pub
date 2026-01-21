#!/usr/bin/env python3
"""
LAI-PrEP Bridge Period Decision Tool - Figure 1: Critical Insights
===================================================================
MDPI Viruses Manuscript

Generates Figure 1: Critical Insights (2×2 tile grid)
  A) Oral PrEP post-init adherence ~30%
  B) LAI PrEP post-init persistence 81–92%
  C) Pre-init bridge loss 47.1%
  D) Barrier shift: post → pre (bridge)

Author: Adrian C. Demidont, DO
Affiliation: Nyx Dynamics LLC
Date: January 2026
Output: PDF (vector) + PNG (600 dpi)
"""

import os
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
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


def make_figure1_critical_insights():
    """
    MDPI-style 2×2 tile grid with numeric tokens and simple glyphs:
    A) Oral PrEP post-init adherence ~30%
    B) LAI PrEP post-init persistence 81–92%
    C) Pre-init bridge loss 47.1%
    D) Barrier shift: post → pre (bridge)
    """
    print("Creating Figure 1: Critical Insights...")

    fig, axes = plt.subplots(2, 2, figsize=(7.09, 4.72), dpi=300)
    plt.subplots_adjust(wspace=0.16, hspace=0.2, left=0.04, right=0.98, top=0.96, bottom=0.10)

    def tile(ax, face):
        ax.set_axis_off()
        box = FancyBboxPatch((0.02, 0.02), 0.96, 0.96, transform=ax.transAxes,
                             boxstyle="round,pad=0.02,rounding_size=0.04",
                             linewidth=0.8, edgecolor=COLORS['dark'], facecolor=face, alpha=0.96)
        ax.add_patch(box)

    # Tile A: Oral PrEP adherence ~30%
    axA = axes[0, 0]
    tile(axA, COLORS['light'])
    axA.text(0.08, 0.78, "Oral PrEP", fontsize=9, fontweight='bold', color=COLORS['dark'], transform=axA.transAxes)
    axA.text(0.08, 0.46, "≈30%", fontsize=22, fontweight='bold', color=COLORS['orange'], transform=axA.transAxes)
    axA.text(0.08, 0.20, "post-init adherence", fontsize=8, color=COLORS['dark'], transform=axA.transAxes)
    # Pill glyph
    axA.add_patch(FancyBboxPatch((0.62, 0.58), 0.26, 0.18, transform=axA.transAxes,
                                 boxstyle="round,pad=0.02,rounding_size=0.08",
                                 linewidth=0.8, edgecolor=COLORS['dark'], facecolor="#FFFFFF"))
    axA.add_patch(FancyBboxPatch((0.62, 0.40), 0.26, 0.18, transform=axA.transAxes,
                                 boxstyle="round,pad=0.02,rounding_size=0.08",
                                 linewidth=0.8, edgecolor=COLORS['dark'], facecolor="#FFFFFF", hatch='///'))

    # Tile B: LAI persistence 81–92%
    axB = axes[0, 1]
    tile(axB, COLORS['light'])
    axB.text(0.08, 0.78, "LAI PrEP", fontsize=9, fontweight='bold', color=COLORS['dark'], transform=axB.transAxes)
    axB.text(0.08, 0.46, "81–92%", fontsize=22, fontweight='bold', color=COLORS['green'], transform=axB.transAxes)
    axB.text(0.08, 0.20, "post-init persistence", fontsize=8, color=COLORS['dark'], transform=axB.transAxes)
    # Syringe glyph
    axB.plot([0.70, 0.92], [0.62, 0.62], color=COLORS['dark'], lw=1.2, transform=axB.transAxes)
    axB.plot([0.82, 0.82], [0.54, 0.70], color=COLORS['dark'], lw=1.2, transform=axB.transAxes)
    axB.plot([0.88, 0.92], [0.54, 0.58], color=COLORS['dark'], lw=1.2, transform=axB.transAxes)

    # Tile C: Pre-init bridge loss 47.1%
    axC = axes[1, 0]
    tile(axC, COLORS['light'])
    axC.text(0.08, 0.78, "Pre-init bridge", fontsize=9, fontweight='bold', color=COLORS['dark'],
             transform=axC.transAxes)
    axC.text(0.08, 0.46, "47.1%", fontsize=22, fontweight='bold', color=COLORS['purple'], transform=axC.transAxes)
    axC.text(0.08, 0.20, "lost before first dose", fontsize=8, color=COLORS['dark'], transform=axC.transAxes)
    # Bridge glyph
    axC.add_patch(FancyBboxPatch((0.62, 0.55), 0.12, 0.16, transform=axC.transAxes,
                                 boxstyle="round,pad=0.02,rounding_size=0.06",
                                 linewidth=0.8, edgecolor=COLORS['dark'], facecolor="#FFFFFF"))
    axC.add_patch(FancyBboxPatch((0.78, 0.55), 0.12, 0.16, transform=axC.transAxes,
                                 boxstyle="round,pad=0.02,rounding_size=0.06",
                                 linewidth=0.8, edgecolor=COLORS['dark'], facecolor="#FFFFFF", hatch='///'))

    # Tile D: Barrier shift (post → pre)
    axD = axes[1, 1]
    tile(axD, COLORS['light'])
    axD.text(0.08, 0.78, "Barrier shift", fontsize=9, fontweight='bold', color=COLORS['dark'], transform=axD.transAxes)
    axD.text(0.08, 0.46, "post → pre", fontsize=18, fontweight='bold', color=COLORS['cyan'], transform=axD.transAxes)
    axD.text(0.08, 0.20, "implementation paradox", fontsize=8, color=COLORS['dark'], transform=axD.transAxes)
    # Arrow
    axD.annotate('', xy=(0.86, 0.62), xytext=(0.50, 0.62), xycoords=axD.transAxes,
                 arrowprops=dict(arrowstyle='simple', lw=0.8, color=COLORS['dark'], alpha=0.9))

    # Footer
    fig.text(0.5, 0.04, "Oral ≈30   LAI 81–92   Bridge 47.1   Shift post→pre",
             ha='center', va='center', fontsize=8, color=COLORS['dark'])

    # Save outputs
    pdf_path = os.path.join(OUTPUT_DIR, 'Figure1_Critical_Insights.pdf')
    png_path = os.path.join(OUTPUT_DIR, 'Figure1_Critical_Insights.png')

    fig.savefig(pdf_path, bbox_inches='tight')
    fig.savefig(png_path, dpi=600, bbox_inches='tight')
    plt.close()

    print(f"✓ Figure 1 complete")
    print(f"  → {pdf_path}")
    print(f"  → {png_path}")


if __name__ == "__main__":
    print("=" * 60)
    print("LAI-PrEP Bridge Tool - Figure 1 Generation")
    print("=" * 60)
    make_figure1_critical_insights()
    print("\nDone!")
