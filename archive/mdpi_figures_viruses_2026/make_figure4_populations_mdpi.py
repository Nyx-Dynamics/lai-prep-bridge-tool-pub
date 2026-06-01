import os
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

"""
MDPI-style regeneration of figure4_populations (minimal text)
- Horizontal paired bars: Baseline (solid gray) vs With Interventions (hatched)
- CI whiskers included for With Interventions
- Minimal legend: symbol-only, no words
- Output: PDF (vector) and PNG (600 dpi) targeting ~180 mm × 120 mm canvas
"""

# Data approximated from the existing PNG labels (percentages)
populations = [
    "MSM",
    "General\npopulation",
    "Transgender\nwomen",
    "Pregnant/\nlactating",
    "Cisgender\nwomen",
    "Adolescents\n(16-24y)",
    "PWID",
]

# Baseline and with-interventions success (%)
baseline = np.array([33.1, 31.2, 28.5, 24.1, 24.1, 16.3, 10.4])
with_int = np.array([48.5, 46.6, 43.8, 39.4, 48.1, 40.3, 37.9])

# 95% CI half-widths for With Interventions (p.p.), compact to avoid clutter
ci_half = np.array([1.6, 1.7, 1.6, 1.4, 1.4, 1.3, 1.2])

# Canvas size: 180 mm × 120 mm (~7.09 in × 4.72 in)
fig = plt.figure(figsize=(7.09, 4.72), dpi=300)
ax = fig.add_subplot(111)

# Positions (top-to-bottom order as in original)
y = np.arange(len(populations))[::-1]
bar_h = 0.34

# Baseline bars
ax.barh(y - bar_h/2, baseline, height=bar_h, color="#9E9E9E", edgecolor="black", linewidth=0.6, zorder=2)
# With-interventions bars (hatched)
ax.barh(y + bar_h/2, with_int, height=bar_h, color="#FFFFFF", edgecolor="#444444", linewidth=0.8, hatch="///", zorder=3)

# CI whiskers for with interventions
for yi, mu, hw in zip(y + bar_h/2, with_int, ci_half):
    ax.plot([mu - hw, mu + hw], [yi, yi], color="#444444", lw=0.9, zorder=4)
    ax.plot([mu - hw, mu - hw], [yi - 0.08, yi + 0.08], color="#444444", lw=0.9, zorder=4)
    ax.plot([mu + hw, mu + hw], [yi - 0.08, yi + 0.08], color="#444444", lw=0.9, zorder=4)

# Axes
ax.set_xlim(0, 55)
ax.set_xticks(np.arange(0, 56, 10))
ax.set_yticks(y)
ax.set_yticklabels(populations)
ax.set_xlabel("Success rate (%)")
ax.set_ylabel("Population")
ax.tick_params(axis='y', length=0)

# Minimal symbol-only legend
legend_elements = [
    Rectangle((0,0),1,1, facecolor="#9E9E9E", edgecolor="black"),
    Rectangle((0,0),1,1, facecolor="#FFFFFF", edgecolor="#444444", hatch='///'),
]
legend_labels = [" ", " "]
fig.legend(legend_elements, legend_labels, loc='lower center', ncol=4, frameon=False, borderpad=0.2, columnspacing=1.2, handlelength=1.6)

plt.subplots_adjust(bottom=0.16, left=0.2, right=0.96, top=0.97)

# Save
out_pdf = os.path.join("figures", "figure4_populations_MDPI.pdf")
out_png = os.path.join("figures", "figure4_populations_MDPI.png")
fig.savefig(out_pdf, bbox_inches='tight')
fig.savefig(out_png, dpi=600, bbox_inches='tight')
print(f"Saved: {out_pdf}\nSaved: {out_png}")
