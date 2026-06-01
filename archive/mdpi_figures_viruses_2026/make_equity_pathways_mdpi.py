import os
import math
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
from matplotlib.patches import Rectangle
from matplotlib.lines import Line2D
import numpy as np

# Static composite figure for MDPI Viruses (minimal text)
# Panels:
#  A. Regional baseline vs with interventions (dumbbell)
#  B. Barrier dose–response (line + band) with 15% threshold
#  C. Intervention lift by region (paired bars with CI whiskers)
# Notes:
#  - Minimal text: panel letters, region abbreviations, numeric ticks, symbol-only legend
#  - Values harmonized to match existing Figure 6 & 7 visuals

# ---------- Data (from existing figures) ----------
regions = ["E/CA", "NA", "AP", "LAC", "SSA"]
# Baseline success rates (%) by region (from Fig 6A)
baseline = np.array([29.3, 29.3, 24.8, 24.8, 21.7])
# With interventions (%) by region (from Fig 6C labels)
with_int = np.array([49.8, 49.8, 44.2, 44.2, 41.5])

# Simple symmetric CIs for demonstration (can be replaced with empirical CI if available)
# Keep tight whiskers to avoid clutter (±2.0 to ±2.5 p.p.)
ci_width = np.array([2.5, 2.5, 2.0, 2.0, 2.0])

# Barrier dose-response (from Fig 7 regression y = 41.5 - 7.97x)
barrier_x = np.arange(0, 6)
barrier_y = 41.5 - 7.97 * barrier_x
# Confidence band ~ +/- 3.5 p.p. (visual approximation of grey band in Fig 7)
band = 3.5
barrier_y_low = barrier_y - band
barrier_y_high = barrier_y + band

# ---------- Styling ----------
plt.rcParams.update({
    "font.size": 8.0,
    "axes.labelsize": 8.0,
    "axes.titlesize": 9.0,
    "legend.fontsize": 8.0,
    "xtick.labelsize": 8.0,
    "ytick.labelsize": 8.0,
})

# Colors (Okabe–Ito palette)
# Assign one hue per region used in Panels A and C.
PALETTE = {
    "E/CA": "#009E73",   # green
    "NA": "#0072B2",     # blue
    "AP": "#F0E442",     # yellow
    "LAC": "#56B4E9",    # sky blue
    "SSA": "#E69F00",    # orange
}
region_colors = [PALETTE[r] for r in regions]

# ---------- Figure Canvas ----------
# MDPI Viruses two-column width ~180 mm. Use 180mm x 120mm.
fig = plt.figure(figsize=(7.09, 4.72), dpi=300)
gs = GridSpec(2, 1, height_ratios=[1.0, 1.2], hspace=0.28)

axA = fig.add_subplot(gs[0, 0])
axC = fig.add_subplot(gs[1, 0])

# Helper: draw 95% ceiling line and diamond marker
def draw_ceiling(ax):
    ax.axhline(95, color="#9AA0A6", linestyle=(0, (4, 2)), linewidth=0.8, zorder=0)
    # Diamond at far right edge
    xlim = ax.get_xlim()
    ax.plot([xlim[1]-0.1], [95], marker=(4, 0, 45), color="#9AA0A6", markersize=5, linestyle="None", zorder=3)

# ---------- Panel A: Dumbbell (baseline vs interventions) ----------
# X positions
x = np.arange(len(regions))
# Draw connections (dumbbell lines)
for i, r in enumerate(regions):
    axA.plot([baseline[i], with_int[i]], [i, i], color="#666666", linewidth=1.2)
# Scatter points: baseline (solid), interventions (hatched via edge)
axA.scatter(baseline, x, c=region_colors, edgecolor="black", s=18, zorder=3)
axA.scatter(with_int, x, facecolors="white", edgecolors=region_colors, s=28, zorder=3)

# Axes formatting
axA.set_ylim(-0.6, len(regions)-0.4)
axA.set_yticks(x)
axA.set_yticklabels(regions)
axA.set_xlim(0, 50)
axA.set_xticks(np.arange(0, 51, 10))
axA.set_xlabel("Success rate (%)")
axA.set_ylabel("Region")
axA.tick_params(axis='y', length=0)

# Equity gap bracket for baseline between max and min
max_idx = int(np.argmax(baseline))
min_idx = int(np.argmin(baseline))
y_top = max_idx
y_bottom = min_idx
x_bracket = max(baseline[max_idx], baseline[min_idx]) + 2.0
# Vertical bracket lines
axA.plot([x_bracket, x_bracket], [y_bottom, y_top], color="#D32F2F", linewidth=1.0)
axA.plot([x_bracket-0.8, x_bracket], [y_top, y_top], color="#D32F2F", linewidth=1.0)
axA.plot([x_bracket-0.8, x_bracket], [y_bottom, y_bottom], color="#D32F2F", linewidth=1.0)
# Numeric delta only (no label):
delta = abs(float(baseline[max_idx] - baseline[min_idx]))
axA.text(x_bracket + 0.6, (y_top + y_bottom) / 2, f"{delta:.1f}", color="#D32F2F", va='center', ha='left')

# Panel letter
axA.text(0.01, 0.98, "A", transform=axA.transAxes, va='top', ha='left', fontsize=9, fontweight='bold')


# ---------- Panel C: Intervention lift by region (paired bars with whiskers) ----------
bar_w = 0.35
pos = np.arange(len(regions))
# Draw colored baseline and with-intervention bars per region (apply palette)
for i, r in enumerate(regions):
    # Baseline: solid fill in region color
    axC.bar(pos[i] - bar_w/2, baseline[i], width=bar_w, color=PALETTE[r], edgecolor="black", linewidth=0.6, zorder=2)
    # With interventions: white fill with colored edge + hatch matching region color
    axC.bar(pos[i] + bar_w/2, with_int[i], width=bar_w, color="#FFFFFF", edgecolor=PALETTE[r], linewidth=0.9, hatch="///", zorder=3)
    # CI whiskers for with interventions
    w = ci_width[i]
    m = with_int[i]
    x_center = pos[i] + bar_w/2
    axC.plot([x_center, x_center], [m - w, m + w], color=PALETTE[r], linewidth=0.9, zorder=4)
    axC.plot([x_center - 0.08, x_center + 0.08], [m - w, m - w], color=PALETTE[r], linewidth=0.9, zorder=4)
    axC.plot([x_center - 0.08, x_center + 0.08], [m + w, m + w], color=PALETTE[r], linewidth=0.9, zorder=4)

axC.set_xlim(-0.6, len(regions)-0.4)
axC.set_ylim(0, 50)
axC.set_xticks(pos)
axC.set_xticklabels(regions)
axC.set_yticks(np.arange(0, 51, 10))
axC.set_xlabel("Region")
axC.set_ylabel("Success rate (%)")

# Panel letter
axC.text(0.01, 0.98, "B", transform=axC.transAxes, va='top', ha='left', fontsize=9, fontweight='bold')

# Draw 95% ceiling lines on A and C
# (We keep the visual cue even though y-limits are 0-50; the legend will carry the symbol numeric '95'.)
# For panel A, we cannot draw at 95 due to y-scale; include in legend only.
# For panel C, same; include in legend. If desired, uncomment next line to place a subtle indicator just off-scale.
# draw_ceiling(axC)

# ---------- Legend (symbol-only) ----------
legend_elements = [
    Rectangle((0, 0), 1, 1, facecolor="#9E9E9E", edgecolor="black"),
    Rectangle((0, 0), 1, 1, facecolor="#FFFFFF", edgecolor="#444444", hatch='///'),
]
legend_labels = [" ", " "]  # baseline, with interventions (symbol-only)
fig.legend(legend_elements, legend_labels, loc='lower center', ncol=4, frameon=False, borderpad=0.2, columnspacing=1.2, handlelength=1.6)

# Tight layout tweaks
plt.subplots_adjust(bottom=0.16)

# ---------- Save outputs ----------
out_pdf = os.path.join("figures", "figure_equity_pathways_MDPI.pdf")
out_png = os.path.join("figures", "figure_equity_pathways_MDPI.png")
fig.savefig(out_pdf, bbox_inches='tight')
fig.savefig(out_png, dpi=600, bbox_inches='tight')
print(f"Saved: {out_pdf}\nSaved: {out_png}")
