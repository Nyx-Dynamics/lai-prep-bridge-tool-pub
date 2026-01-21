#!/usr/bin/env python3
"""
LAI-PrEP Figure 6: Regional Health Equity Analysis
===================================================
Generates Figure 6 with:
- Panel A: Bubble chart (size = HIV burden, color = baseline success)
- Panel B: Patient distribution by region
- Panel C: Figure 4 style horizontal paired bars

Author: Adrian C. Demidont, DO
Affiliation: Nyx Dynamics LLC
Date: January 2026
"""

import os
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import rcParams
from matplotlib.patches import Patch
from matplotlib.lines import Line2D

# Create output directory if it doesn't exist
output_dir = os.path.join('../figures')
os.makedirs(output_dir, exist_ok=True)

# Configure matplotlib
rcParams.update({
    'font.family': 'sans-serif',
    'font.sans-serif': ['Arial', 'Helvetica', 'DejaVu Sans'],
    'font.size': 10.0,
    'axes.labelweight': 'bold',
    'axes.titleweight': 'bold',
    'axes.linewidth': 1.2,
    'figure.dpi': 300,
})

COLORS = {'green': '#009E73', 'cyan': '#56B4E9', 'grey': '#9E9E9E'}

# Data
regions = ['Sub-Saharan\nAfrica', 'Asia-Pacific', 'Latin America\n& Caribbean',
           'Eastern Europe\n& Central Asia', 'Western &\nCentral Europe', 'North America']
regions_short = ['SSA', 'Asia-Pacific', 'LAC', 'EECA', 'WCE', 'North America']
baseline = np.array([21.69, 24.82, 26.45, 27.11, 29.33, 28.87])
with_int = np.array([41.49, 43.21, 44.89, 45.02, 47.18, 46.93])
improvements = with_int - baseline
sample_pct = np.array([62, 18, 8, 5, 4, 3])

# Color gradient: darkest red for lowest baseline, lighter for higher baseline
baseline_norm = (baseline - baseline.min()) / (baseline.max() - baseline.min())
regional_colors = []
for val in baseline_norm:
    r = 0.8 + 0.2 * val  # 0.8 to 1.0
    g = 0.2 * val  # 0.0 to 0.2
    b = 0.2 * val  # 0.0 to 0.2
    regional_colors.append((r, g, b))

fig = plt.figure(figsize=(14, 12), dpi=300)

# =============================================================================
# Panel A: Bubble chart (top left)
# =============================================================================
ax1 = fig.add_subplot(2, 2, 1)
x = np.arange(len(regions))

# Bubble sizes proportional to HIV burden (sample_pct)
bubble_sizes = sample_pct * 25  # Scale for visibility

# Plot bubbles for baseline and with interventions
for i, (xi, b, w, size, color) in enumerate(zip(x, baseline, with_int, bubble_sizes, regional_colors)):
    # Baseline bubble
    ax1.scatter(xi - 0.15, b, s=size, c=[color], edgecolors='black', linewidth=1.5,
                zorder=5, alpha=0.9)
    # With interventions bubble (green)
    ax1.scatter(xi + 0.15, w, s=size, c=[COLORS['green']], edgecolors='black', linewidth=1.5,
                zorder=5, alpha=0.9)
    # Connect with line
    ax1.plot([xi - 0.15, xi + 0.15], [b, w], color='gray', lw=1.5, zorder=1)

ax1.set_xticks(x)
ax1.set_xticklabels(regions_short, fontsize=11, fontweight='bold')
ax1.set_ylabel("Success Rate (%)", fontsize=12, fontweight='bold')
ax1.set_ylim(15, 55)
ax1.set_title("A. Regional Success Rates\n(Bubble size = HIV burden)", fontweight='bold', fontsize=13)
ax1.grid(axis='y', alpha=0.3, linestyle='--')

# Legend for Panel A
legend_elements = [
    Line2D([0], [0], marker='o', color='w', markerfacecolor='darkred', markersize=10,
           label='Baseline (red gradient)', markeredgecolor='black'),
    Line2D([0], [0], marker='o', color='w', markerfacecolor=COLORS['green'], markersize=10,
           label='With Interventions', markeredgecolor='black'),
]
ax1.legend(handles=legend_elements, loc='upper left', fontsize=10)

# Equity gap annotation - positioned above LAC (x=2) at y=20
# Bidirectional arrows connecting to SSA (x=0) and WCE (x=4) baselines
gap = max(baseline) - min(baseline)

# Position bubble above LAC
bubble_x = 2  # LAC position
bubble_y = 20

# Draw the bubble/label
ax1.text(bubble_x, bubble_y, f'Equity Gap:\n{gap:.1f} pp',
         ha='center', va='center', fontsize=8, fontweight='bold',
         bbox=dict(boxstyle='round,pad=0.3', facecolor='lightyellow', edgecolor='black', lw=1.2),
         zorder=10)

# Bidirectional arrow from bubble to SSA baseline
ax1.annotate('', xy=(0 - 0.15, baseline[0]), xytext=(bubble_x - 0.3, bubble_y - 1.5),
             arrowprops=dict(arrowstyle='<->', color='black', lw=1.5, connectionstyle='arc3,rad=0.2'))

# Bidirectional arrow from bubble to WCE baseline
ax1.annotate('', xy=(4 - 0.15, baseline[4]), xytext=(bubble_x + 0.3, bubble_y - 1.5),
             arrowprops=dict(arrowstyle='<->', color='black', lw=1.5, connectionstyle='arc3,rad=-0.2'))

# =============================================================================
# Panel B: Patient Distribution (top right)
# =============================================================================
ax2 = fig.add_subplot(2, 2, 2)
bars = ax2.barh(regions_short, sample_pct, color=[regional_colors[i] for i in range(len(regions))],
                edgecolor='black', lw=1.2)
ax2.set_xlabel("% of Global Patients", fontsize=12, fontweight='bold')
ax2.set_xlim(0, 70)
ax2.set_title("B. Patient Distribution by Region", fontweight='bold', fontsize=13)

for i, v in enumerate(sample_pct):
    ax2.text(v + 1, i, f'{v}%', va='center', fontsize=10, fontweight='bold')

# =============================================================================
# Panel C: Figure 4 style horizontal paired bars (bottom, spanning full width)
# =============================================================================
ax3 = fig.add_subplot(2, 1, 2)

# Order by baseline success (lowest at top for visual impact)
order = np.argsort(baseline)
regions_ord = [regions[i] for i in order]
baseline_ord = baseline[order]
with_int_ord = with_int[order]
improvements_ord = improvements[order]
colors_ord = [regional_colors[i] for i in order]

y = np.arange(len(regions))
height = 0.35

# Baseline bars (regional colors)
bars_base = ax3.barh(y - height / 2, baseline_ord, height, label='Baseline (red = lower success)',
                     color=colors_ord, edgecolor='black', lw=1.2)

# With interventions bars (green)
bars_int = ax3.barh(y + height / 2, with_int_ord, height, label='With Interventions',
                    color=COLORS['green'], edgecolor='black', lw=1.2)

# Add white bidirectional arrows and improvement text inside green bars (Figure 4 style)
for i, (b, w, imp) in enumerate(zip(baseline_ord, with_int_ord, improvements_ord)):
    # Bidirectional arrow (white)
    mid_y = i + height / 2
    ax3.annotate('', xy=(w - 1, mid_y), xytext=(b + 1, mid_y),
                 arrowprops=dict(arrowstyle='<->', color='white', lw=2))

    # Improvement value - Figure 4 style: WHITE text in GREEN bubble inside the bar
    text_x = (b + w) / 2
    ax3.text(text_x, mid_y, f'+{imp:.1f} pp', ha='center', va='center',
             fontsize=8, fontweight='bold', color='white',
             bbox=dict(boxstyle='round,pad=0.3', facecolor=COLORS['green'],
                       edgecolor='white', linewidth=1.5, alpha=0.95),
             zorder=6)

# Baseline percentage labels
for i, (b, color) in enumerate(zip(baseline_ord, colors_ord)):
    ax3.text(b - 1, i - height / 2, f'{b:.1f}%', ha='right', va='center',
             fontsize=10, fontweight='bold', color='white')

# With interventions percentage labels (at end of green bar)
for i, w in enumerate(with_int_ord):
    ax3.text(w + 1, i + height / 2, f'{w:.1f}%', ha='left', va='center',
             fontsize=10, fontweight='bold', color='black')

ax3.set_yticks(y)
ax3.set_yticklabels(regions_ord, fontsize=11, fontweight='bold')
ax3.set_xlabel("Success Rate (%)", fontsize=12, fontweight='bold')
ax3.set_xlim(0, 55)
ax3.set_title("C. Impact of Evidence-Based Interventions by Region", fontweight='bold', fontsize=13)
ax3.tick_params(axis='y', length=0)
ax3.grid(axis='x', alpha=0.3, linestyle='--')
ax3.legend(loc='lower right', fontsize=10)

plt.suptitle('Regional Health Equity Analysis at UNAIDS Global Scale', fontsize=16, fontweight='bold', y=0.99)

plt.tight_layout(rect=[0, 0, 1, 0.97])
fig.savefig(os.path.join(output_dir, 'Figure6_Regional.png'), dpi=600, bbox_inches='tight')
fig.savefig(os.path.join(output_dir, 'Figure6_Regional.pdf'), bbox_inches='tight')
plt.close()
print('Figure 6 regenerated successfully')
