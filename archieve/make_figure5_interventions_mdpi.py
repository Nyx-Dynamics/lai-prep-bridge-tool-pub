import os
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

"""
MDPI-style clarity redesign of figure5_interventions (minimal text)
- Single horizontal bar chart showing intervention lift (Δ percentage points)
- Rank-ordered by absolute improvement to maximize readability
- Optional CI whiskers included (tight, to avoid clutter)
- Minimal legend (symbol-only, or none); rely on axis label and numeric ticks
- Output: PDF (vector) + PNG (600 dpi) targeting ~180 mm × 120 mm canvas

NOTE: Values are approximations inferred from the original PNG (forest plot).
Replace arrays below with precise numbers if available from source tables.
"""

# Populations (same ordering used elsewhere in the manuscript)
populations = [
    "MSM",
    "General\npopulation",
    "Transgender\nwomen",
    "Pregnant/\nlactating",
    "Cisgender\nwomen",
    "Adolescents\n(16–24y)",
    "PWID",
]

# Absolute improvement (percentage points) — approximate, from original figure
# These represent the incremental lift attributable to the intervention bundle
# (vs baseline), not the final success rate.
delta_pp = np.array([15.35, 15.35, 15.36, 15.33, 23.96, 23.96, 27.46])

# Compact CI half-widths (p.p.) for the lift values (visual approximations)
ci_half = np.array([1.1, 1.1, 1.1, 1.1, 1.5, 1.6, 1.8])

# Rank order by effect size (descending)
order = np.argsort(-delta_pp)
populations_ord = [populations[i] for i in order]
delta_ord = delta_pp[order]
ci_ord = ci_half[order]

# Canvas (≈180 mm × 120 mm)
fig = plt.figure(figsize=(7.09, 4.72), dpi=300)
ax = fig.add_subplot(111)

# Positions (top-to-bottom)
y = np.arange(len(populations_ord))[::-1]
bar_h = 0.5

# Bars (hatched white on grey spine for grayscale robustness)
ax.barh(y, delta_ord, height=bar_h, color="#FFFFFF", edgecolor="#444444", linewidth=0.9, hatch="///", zorder=2)

# CI whiskers
for yi, mu, hw in zip(y, delta_ord, ci_ord):
    ax.plot([mu - hw, mu + hw], [yi, yi], color="#444444", lw=1.0, zorder=3)
    ax.plot([mu - hw, mu - hw], [yi - 0.09, yi + 0.09], color="#444444", lw=1.0, zorder=3)
    ax.plot([mu + hw, mu + hw], [yi - 0.09, yi + 0.09], color="#444444", lw=1.0, zorder=3)

# Axes
ax.set_xlim(0, max(delta_ord) + 5)
ax.set_xticks(np.arange(0, 36, 5))
ax.set_yticks(y)
ax.set_yticklabels(populations_ord)
ax.set_xlabel("Δ success (percentage points)")
ax.set_ylabel("Population")
ax.tick_params(axis='y', length=0)

# Subtle reference line at 15 p.p. (common threshold seen in original)
ax.axvline(15, color="#B0B0B0", linestyle=(0, (2, 2)), lw=0.8, zorder=1)

# Minimal symbol-only legend (optional): show hatched token only
legend_elements = [Rectangle((0,0), 1, 1, facecolor="#FFFFFF", edgecolor="#444444", hatch='///')]
legend_labels = [" "]
fig.legend(legend_elements, legend_labels, loc='lower center', ncol=4, frameon=False,
           borderpad=0.2, columnspacing=1.2, handlelength=1.6)

plt.subplots_adjust(bottom=0.16, left=0.2, right=0.96, top=0.97)

# Save
out_pdf = os.path.join('figures', 'figure5_interventions_MDPI.pdf')
out_png = os.path.join('figures', 'figure5_interventions_MDPI.png')
fig.savefig(out_pdf, bbox_inches='tight')
fig.savefig(out_png, dpi=600, bbox_inches='tight')
print(f"Saved: {out_pdf}\nSaved: {out_png}")
