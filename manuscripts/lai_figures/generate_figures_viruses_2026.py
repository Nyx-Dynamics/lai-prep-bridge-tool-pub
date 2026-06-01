#!/usr/bin/env python3
"""
LAI-PrEP Bridge Period Decision Tool - Complete Figure Generation Suite
========================================================================
MDPI Viruses Manuscript Figures

Generates all 9 figures for publication:
  Figure 1: Critical Insights (2×2 tile grid)
  Figure 2: Tool Workflow Diagram
  Figure 3: Progressive Validation Convergence
  Figure 4: Population-Specific Success Rates
  Figure 5: Intervention Impact (Forest Plot)
  Figure 6: Regional Health Equity Analysis
  Figure 7: Barrier Dose-Response Relationship
  Figure 8: Global Impact Projections
  Figure 9: Oral vs LAI-PrEP Comparison

Author: Adrian C. Demidont, DO
Affiliation: Nyx Dynamics LLC
Date: January 2026
Output: PDF (vector) + PNG (600 dpi) for each figure
"""

import os
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Rectangle, Circle, FancyArrowPatch
from matplotlib.lines import Line2D
from matplotlib import rcParams
import warnings

warnings.filterwarnings('ignore')

# =============================================================================
# SETUP: Create output directory and set MDPI typography
# =============================================================================
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


# =============================================================================
# FIGURE 1: Critical Insights (2×2 Tile Grid)
# =============================================================================
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

    fig.savefig('figures/Figure1_Critical_Insights.pdf', bbox_inches='tight')
    fig.savefig('figures/Figure1_Critical_Insights.png', dpi=600, bbox_inches='tight')
    plt.close()
    print("✓ Figure 1 complete")


# =============================================================================
# FIGURE 2: Tool Workflow Diagram
# =============================================================================
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
        box = FancyBboxPatch((2, y - 0.7), 6, 1.2, boxstyle="round,pad=0.02,rounding_size=0.2",
                             linewidth=1.2, edgecolor="#333333", facecolor=col, alpha=0.95)
        ax.add_patch(box)
        circ = Circle((1.1, y - 0.1), radius=0.28, facecolor=col, edgecolor="#333333", linewidth=1.0)
        ax.add_patch(circ)
        ax.text(1.1, y - 0.1, str(i), va='center', ha='center', fontsize=9, fontweight='bold', color='white')
        ax.text(5, y - 0.1, lab, va='center', ha='center', fontsize=8, color='white', fontweight='bold')
        if i < 5:
            ax.annotate('', xy=(5, y - 0.7), xytext=(5, y - 1.0),
                        arrowprops=dict(arrowstyle='->', lw=1.2, color='#444444'))

    # Legend row
    legend_labels = ["Patient", "Risk", "Barriers", "Interv.", "Outcome"]
    x0, y0 = 1.0, 0.5
    for k, (cap, col) in enumerate(zip(legend_labels, colors)):
        x = x0 + k * 1.6
        circ = Circle((x, y0), radius=0.16, facecolor=col, edgecolor='#333333', lw=0.8)
        ax.add_patch(circ)
        ax.text(x, y0, str(k + 1), va='center', ha='center', fontsize=7, color='white', fontweight='bold')
        ax.text(x + 0.35, y0, cap, va='center', ha='left', fontsize=7, color='#333333')

    # Feedback loop arrow
    box_x, box_w, box_h = 2.0, 6.0, 1.2
    x_loop = box_x + box_w + 0.4
    y_top = y_positions[0] + (box_h / 2) - 0.1
    y_bot = y_positions[-1] - (box_h / 2) + 0.1
    ax.annotate('', xy=(x_loop, y_top), xytext=(x_loop, y_bot),
                arrowprops=dict(arrowstyle='-|>', lw=1.0, color='#666666',
                                connectionstyle='arc3,rad=0.6', alpha=0.85), clip_on=False)

    plt.subplots_adjust(left=0.02, right=0.98, top=0.98, bottom=0.14)
    fig.savefig('figures/Figure2_Workflow.pdf', bbox_inches='tight')
    fig.savefig('figures/Figure2_Workflow.png', dpi=600, bbox_inches='tight')
    plt.close()
    print("✓ Figure 2 complete")


# =============================================================================
# FIGURE 3: Progressive Validation Convergence
# =============================================================================
def make_figure3_convergence():
    """
    Dual-axis plot showing margin of error convergence and processing speed
    across validation tiers: 1K, 1M, 10M, 21.2M patients
    """
    print("Creating Figure 3: Convergence...")

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

    # Policy-grade precision zone
    ax1.axhspan(0.01, 0.05, color="#A5D6A7", alpha=0.35, zorder=0)
    ax1.text(3.2, 0.03, "Policy-Grade\nPrecision", fontsize=7, ha='right', va='center', style='italic')

    # Right axis: Processing speed
    ax2 = ax1.twinx()
    ax2.plot(x, processing_speed, color=COLORS['blue'], marker='s', markersize=8, lw=2.0, linestyle='--',
             label='Processing Speed')
    ax2.set_ylabel("Throughput (patients/s)", fontweight='bold', color=COLORS['blue'])
    ax2.tick_params(axis='y', labelcolor=COLORS['blue'])

    # Value annotations
    for i, (xe, ye) in enumerate(zip(x, margin_error_pp)):
        ax1.annotate(f'±{ye:.3f}', xy=(xe, ye), xytext=(0, 12), textcoords='offset points',
                     ha='center', fontsize=7, fontweight='bold',
                     bbox=dict(boxstyle='round,pad=0.3', facecolor='white', edgecolor='gray', alpha=0.9))

    # 144× improvement annotation
    ax1.annotate('144× precision\nimprovement', xy=(2.5, 0.15), xytext=(1, 0.8),
                 arrowprops=dict(arrowstyle='->', lw=1.2, color='black'),
                 fontsize=8, fontweight='bold', ha='center',
                 bbox=dict(boxstyle='round', facecolor='lightyellow', alpha=0.9))

    ax1.grid(True, which='both', axis='y', linestyle=':', linewidth=0.6, alpha=0.5)

    # Combined legend
    lines1, labels1 = ax1.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax1.legend(lines1 + lines2, labels1 + labels2, loc='upper right', fontsize=8)

    plt.subplots_adjust(bottom=0.12, left=0.12, right=0.88, top=0.96)
    fig.savefig('figures/Figure3_Convergence.pdf', bbox_inches='tight')
    fig.savefig('figures/Figure3_Convergence.png', dpi=600, bbox_inches='tight')
    plt.close()
    print("✓ Figure 3 complete")


# =============================================================================
# FIGURE 4: Population-Specific Success Rates
# =============================================================================
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
    fig.savefig('figures/Figure4_Populations.pdf', bbox_inches='tight')
    fig.savefig('figures/Figure4_Populations.png', dpi=600, bbox_inches='tight')
    plt.close()
    print("✓ Figure 4 complete")


# =============================================================================
# FIGURE 5: Intervention Impact (Forest Plot)
# =============================================================================
def make_figure5_interventions():
    """
    Horizontal bar chart showing intervention lift (Δ percentage points)
    ranked by absolute improvement
    """
    print("Creating Figure 5: Interventions...")

    populations = ["MSM", "General\npopulation", "Transgender\nwomen",
                   "Pregnant/\nlactating", "Cisgender\nwomen", "Adolescents\n(16–24y)", "PWID"]
    delta_pp = np.array([15.35, 15.35, 15.36, 15.33, 23.96, 23.96, 27.46])
    ci_half = np.array([1.1, 1.1, 1.1, 1.1, 1.5, 1.6, 1.8])

    # Rank order by effect size
    order = np.argsort(-delta_pp)
    populations_ord = [populations[i] for i in order]
    delta_ord = delta_pp[order]
    ci_ord = ci_half[order]

    fig = plt.figure(figsize=(7.09, 4.72), dpi=300)
    ax = fig.add_subplot(111)

    y = np.arange(len(populations_ord))[::-1]
    bar_h = 0.5

    ax.barh(y, delta_ord, height=bar_h, color="#FFFFFF", edgecolor="#444444",
            linewidth=0.9, hatch="///", zorder=2)

    # CI whiskers
    for yi, mu, hw in zip(y, delta_ord, ci_ord):
        ax.plot([mu - hw, mu + hw], [yi, yi], color="#444444", lw=1.0, zorder=3)
        ax.plot([mu - hw, mu - hw], [yi - 0.09, yi + 0.09], color="#444444", lw=1.0, zorder=3)
        ax.plot([mu + hw, mu + hw], [yi - 0.09, yi + 0.09], color="#444444", lw=1.0, zorder=3)

    ax.set_xlim(0, max(delta_ord) + 5)
    ax.set_xticks(np.arange(0, 36, 5))
    ax.set_yticks(y)
    ax.set_yticklabels(populations_ord)
    ax.set_xlabel("Δ Success (percentage points)", fontweight='bold')
    ax.set_ylabel("Population", fontweight='bold')
    ax.tick_params(axis='y', length=0)
    ax.axvline(15, color=COLORS['band'], linestyle=(0, (2, 2)), lw=0.8, zorder=1)

    plt.subplots_adjust(bottom=0.12, left=0.2, right=0.96, top=0.97)
    fig.savefig('figures/Figure5_Interventions.pdf', bbox_inches='tight')
    fig.savefig('figures/Figure5_Interventions.png', dpi=600, bbox_inches='tight')
    plt.close()
    print("✓ Figure 5 complete")


# =============================================================================
# FIGURE 6: Regional Health Equity Analysis
# =============================================================================
def make_figure6_regional():
    """
    Regional comparison showing baseline vs intervention success rates
    with equity gap visualization
    """
    print("Creating Figure 6: Regional...")

    regions = ["Sub-Saharan\nAfrica", "Asia-Pacific", "Latin America\n& Caribbean",
               "Eastern Europe\n& Central Asia", "Western &\nCentral Europe", "North America"]
    baseline = np.array([21.69, 24.82, 26.45, 27.11, 29.33, 28.87])
    with_int = np.array([41.49, 43.21, 44.89, 45.02, 47.18, 46.93])
    sample_pct = np.array([62, 18, 8, 5, 4, 3])  # % of global patients

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 5), dpi=300)

    # Panel A: Success rates
    x = np.arange(len(regions))
    width = 0.35
    ax1.bar(x - width / 2, baseline, width, label='Baseline', color=COLORS['grey'], edgecolor='black', lw=0.8)
    ax1.bar(x + width / 2, with_int, width, label='With Interventions', color=COLORS['green'], edgecolor='black',
            lw=0.8)
    ax1.set_xticks(x)
    ax1.set_xticklabels(regions, fontsize=7, rotation=45, ha='right')
    ax1.set_ylabel("Success Rate (%)", fontweight='bold')
    ax1.set_ylim(0, 55)
    ax1.legend(loc='upper left', fontsize=7)
    ax1.set_title("A. Regional Success Rates", fontweight='bold', fontsize=10)

    # Equity gap annotation
    gap = max(baseline) - min(baseline)
    ax1.annotate(f'Equity Gap:\n{gap:.1f} pp', xy=(0, baseline[0]), xytext=(2, 15),
                 arrowprops=dict(arrowstyle='->', lw=1), fontsize=8, ha='center',
                 bbox=dict(boxstyle='round', facecolor='lightyellow', alpha=0.9))

    # Panel B: Sample distribution
    ax2.barh(regions, sample_pct, color=COLORS['cyan'], edgecolor='black', lw=0.8)
    ax2.set_xlabel("% of Global Patients", fontweight='bold')
    ax2.set_xlim(0, 70)
    ax2.set_title("B. Patient Distribution", fontweight='bold', fontsize=10)

    for i, v in enumerate(sample_pct):
        ax2.text(v + 1, i, f'{v}%', va='center', fontsize=8, fontweight='bold')

    plt.tight_layout()
    fig.savefig('figures/Figure6_Regional.pdf', bbox_inches='tight')
    fig.savefig('figures/Figure6_Regional.png', dpi=600, bbox_inches='tight')
    plt.close()
    print("✓ Figure 6 complete")


# =============================================================================
# FIGURE 7: Barrier Dose-Response Relationship
# =============================================================================
def make_figure7_barriers():
    """
    Shows inverse relationship between number of barriers and success rate
    with regression line and patient distribution inset
    """
    print("Creating Figure 7: Barriers...")

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
    fig.savefig('figures/Figure7_Barriers.pdf', bbox_inches='tight')
    fig.savefig('figures/Figure7_Barriers.png', dpi=600, bbox_inches='tight')
    plt.close()
    print("✓ Figure 7 complete")


# =============================================================================
# FIGURE 8: Global Impact Projections
# =============================================================================
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
    fig.savefig('figures/Figure8_Impact.pdf', bbox_inches='tight')
    fig.savefig('figures/Figure8_Impact.png', dpi=600, bbox_inches='tight')
    plt.close()
    print("✓ Figure 8 complete")


# =============================================================================
# FIGURE 9: Oral vs LAI-PrEP Comparison Over Time
# =============================================================================
def make_figure9_oral_vs_lai():
    """
    Two-panel figure contrasting Oral vs LAI PrEP over time (weekly)
    """
    print("Creating Figure 9: Oral vs LAI...")

    WEEKS = 12
    weeks = np.arange(0, WEEKS + 1, 1)

    # Oral PrEP: exponential decay from 100% to ~30%
    oral_start = 100.0
    oral_target_w12 = 30.0
    k = -np.log(oral_target_w12 / oral_start) / WEEKS
    o_oral = oral_start * np.exp(-k * weeks)

    # LAI PrEP: 0% until first injection at week 2, then high persistence
    first_injection_week = 2.0
    first_injection_pct = 47.0
    o_lai = np.zeros_like(weeks, dtype=float)
    for i, t in enumerate(weeks):
        if t < first_injection_week:
            o_lai[i] = 0.0
        else:
            months = (t - first_injection_week) / 4.0
            o_lai[i] = max(0.0, first_injection_pct - 1.0 * months)

    fig, (axA, axB) = plt.subplots(1, 2, figsize=(10, 5), dpi=300, sharey=True)

    for ax in (axA, axB):
        ax.set_xlim(0, WEEKS)
        ax.set_ylim(0, 100)
        ax.set_xticks(np.arange(0, WEEKS + 1, 2))
        ax.set_yticks(np.arange(0, 101, 20))
        ax.grid(True, alpha=0.3, linestyle='--')

    # Panel A: Oral
    axA.plot(weeks, o_oral, color=COLORS['blue'], lw=2.5, marker='o', markersize=4)
    axA.fill_between(weeks, o_oral, alpha=0.2, color=COLORS['blue'])
    axA.text(0.02, 0.98, "A", transform=axA.transAxes, va='top', ha='left',
             fontsize=12, fontweight='bold')
    axA.set_title("Oral PrEP", fontweight='bold')
    axA.set_xlabel("Weeks since decision", fontweight='bold')
    axA.set_ylabel("% on PrEP", fontweight='bold')

    # Panel B: LAI
    bridge_lo, bridge_hi = 10 / 7.0, 14 / 7.0
    axB.axvspan(bridge_lo, bridge_hi, color=COLORS['band'], alpha=0.4, label='Bridge period')
    axB.plot(weeks, o_lai, color=COLORS['green'], lw=2.5, marker='s', markersize=4)
    axB.fill_between(weeks, o_lai, alpha=0.2, color=COLORS['green'])
    axB.axvline(first_injection_week, color="#666666", lw=1.2, linestyle='--')
    axB.text(first_injection_week + 0.3, first_injection_pct + 3, "47%",
             color=COLORS['dark'], fontsize=10, fontweight='bold')
    axB.text(0.02, 0.98, "B", transform=axB.transAxes, va='top', ha='left',
             fontsize=12, fontweight='bold')
    axB.set_title("LAI-PrEP", fontweight='bold')
    axB.set_xlabel("Weeks since decision", fontweight='bold')
    axB.legend(loc='upper right', fontsize=8)

    # Legend
    legend_elements = [
        Line2D([0], [0], color=COLORS['blue'], lw=2.5, label='Oral PrEP'),
        Line2D([0], [0], color=COLORS['green'], lw=2.5, label='LAI-PrEP'),
        Rectangle((0, 0), 1, 1, facecolor=COLORS['band'], alpha=0.4, label='Bridge (10-14d)'),
    ]
    fig.legend(handles=legend_elements, loc='lower center', ncol=3, fontsize=9,
               bbox_to_anchor=(0.5, 0.02))

    plt.tight_layout(rect=[0, 0.08, 1, 1])
    fig.savefig('figures/Figure9_Oral_vs_LAI.pdf', bbox_inches='tight')
    fig.savefig('figures/Figure9_Oral_vs_LAI.png', dpi=600, bbox_inches='tight')
    plt.close()
    print("✓ Figure 9 complete")


# =============================================================================
# MAIN: Generate all figures
# =============================================================================
def main():
    print("=" * 70)
    print("LAI-PrEP Bridge Period Decision Tool - Figure Generation")
    print("MDPI Viruses Manuscript")
    print("=" * 70)
    print()

    make_figure1_critical_insights()
    make_figure2_workflow()
    make_figure3_convergence()
    make_figure4_populations()
    make_figure5_interventions()
    make_figure6_regional()
    make_figure7_barriers()
    make_figure8_impact()
    make_figure9_oral_vs_lai()

    print()
    print("=" * 70)
    print("ALL FIGURES GENERATED SUCCESSFULLY!")
    print("=" * 70)
    print("\nOutput files in ./figures/:")
    print("  Figure1_Critical_Insights.pdf/png")
    print("  Figure2_Workflow.pdf/png")
    print("  Figure3_Convergence.pdf/png")
    print("  Figure4_Populations.pdf/png")
    print("  Figure5_Interventions.pdf/png")
    print("  Figure6_Regional.pdf/png")
    print("  Figure7_Barriers.pdf/png")
    print("  Figure8_Impact.pdf/png")
    print("  Figure9_Oral_vs_LAI.pdf/png")
    print("\nAll figures saved in PDF (vector) and PNG (600 dpi) formats")
    print("Ready for MDPI Viruses submission!")


if __name__ == "__main__":
    main()
