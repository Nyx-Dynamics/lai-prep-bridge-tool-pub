import os
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from matplotlib.patches import Rectangle

"""
Two‑panel MDPI‑style figure contrasting Oral vs LAI PrEP over time (weekly)
- Minimal text (panel letters, numeric axes, symbol‑only legend)
- X: Weeks since decision to start PrEP (0–12)
- Y: % on PrEP (0–100)
- Panel A (Oral): same‑day start at week 0, rapid persistence decline
- Panel B (LAI): pre‑initiation bridge (10–14 days), step to first injection (~47%)
  then high persistence (near‑flat)
Outputs:
  figures/figure_oral_vs_lai_MDPI.pdf
  figures/figure_oral_vs_lai_MDPI.png (600 dpi)
"""

# ---------------- Parameters (easy to tweak) ----------------
WEEKS = 12
DT = 1.0  # weekly step

# Oral PrEP: start at 100% at t=0, exponential decay toward ~30% by week 12
oral_start = 100.0
oral_target_w12 = 30.0
# derive exponential decay rate k so that oral(t=12) ≈ oral_target_w12
k = -np.log(oral_target_w12 / oral_start) / WEEKS  # simple mono‑exponential

# LAI PrEP: 0% until first injection, shaded bridge 10–14d (≈1.4–2.0w), step to 47% at week 2
first_injection_week = 2.0
first_injection_pct = 47.0
lai_post_injection_drop_pp_per_4w = 1.0  # slight monthly decline

# ---------------- Data generation ----------------
weeks = np.arange(0, WEEKS + DT, DT)

# Oral trajectory
o_oral = oral_start * np.exp(-k * weeks)

# LAI trajectory: step at week 2, then slight decline over time (high persistence)
o_lai = np.zeros_like(weeks)
for i, t in enumerate(weeks):
    if t < first_injection_week:
        o_lai[i] = 0.0
    else:
        months = (t - first_injection_week) / 4.0
        o_lai[i] = max(0.0, first_injection_pct - lai_post_injection_drop_pp_per_4w * months)

# Clip to [0, 100]
o_oral = np.clip(o_oral, 0, 100)
o_lai = np.clip(o_lai, 0, 100)

# ---------------- Plot styling ----------------
plt.rcParams.update({
    "font.size": 8.0,
    "axes.labelsize": 8.0,
    "axes.titlesize": 9.0,
    "legend.fontsize": 8.0,
    "xtick.labelsize": 8.0,
    "ytick.labelsize": 8.0,
})

# Colors (Okabe–Ito safe)
BLUE = "#0072B2"  # Oral
GREEN = "#009E73"  # LAI
GREY = "#9E9E9E"
BAND = "#B0B0B0"

# ---------------- Figure canvas ----------------
fig, (axA, axB) = plt.subplots(1, 2, figsize=(7.09, 4.72), dpi=300, sharey=True)

# Common axes setup
for ax in (axA, axB):
    ax.set_xlim(0, WEEKS)
    ax.set_ylim(0, 100)
    ax.set_xticks(np.arange(0, WEEKS + 1, 2))
    ax.set_yticks(np.arange(0, 101, 10))

# ---------------- Panel A: Oral ----------------
axA.plot(weeks, o_oral, color=BLUE, lw=1.6)
# Optional small weekly markers (very faint to keep minimal)
axA.plot(weeks, o_oral, color=BLUE, marker='o', ms=2.2, lw=0, alpha=0.6)
# Panel letter
axA.text(0.02, 0.98, "A", transform=axA.transAxes, va='top', ha='left', fontsize=9, fontweight='bold')

# ---------------- Panel B: LAI ----------------
# Shaded bridge window: 10–14 days ~ 1.4–2.0 weeks
bridge_lo, bridge_hi = 10/7.0, 14/7.0
axB.axvspan(bridge_lo, bridge_hi, color=BAND, alpha=0.3, lw=0)

# LAI line and markers
axB.plot(weeks, o_lai, color=GREEN, lw=1.6)
axB.plot(weeks, o_lai, color=GREEN, marker='o', ms=2.2, lw=0, alpha=0.6)

# Visual step marker at first injection (week ~2)
axB.axvline(first_injection_week, color="#666666", lw=0.8, linestyle=(0, (3, 2)))
# Numeric token “47” close to the step (no words)
axB.text(first_injection_week + 0.15, first_injection_pct + 2.0, "47", color="#444444", fontsize=8, va='bottom', ha='left')

# Panel letter
axB.text(0.02, 0.98, "B", transform=axB.transAxes, va='top', ha='left', fontsize=9, fontweight='bold')

# ---------------- Symbol‑only legend ----------------
legend_elements = [
    Line2D([0], [0], color=BLUE, lw=1.6),
    Line2D([0], [0], color=GREEN, lw=1.6),
    Rectangle((0, 0), 1, 1, facecolor=BAND, edgecolor=BAND, alpha=0.3),
]
legend_labels = [" ", " ", "10–14"]  # numeric token only for bridge window
leg = fig.legend(legend_elements, legend_labels, loc='lower center', ncol=6, frameon=False,
                 borderpad=0.2, columnspacing=1.2, handlelength=1.8)

# Common axis labels (minimal text)
fig.supxlabel("Weeks since decision", x=0.52)
fig.supylabel("% on PrEP", x=0.02)

# Layout
plt.subplots_adjust(left=0.08, right=0.98, top=0.96, bottom=0.16, wspace=0.14)

# ---------------- Save outputs ----------------
out_pdf = os.path.join("figures", "figure_oral_vs_lai_MDPI.pdf")
out_png = os.path.join("figures", "figure_oral_vs_lai_MDPI.png")
fig.savefig(out_pdf, bbox_inches='tight')
fig.savefig(out_png, dpi=600, bbox_inches='tight')
print(f"Saved: {out_pdf}\nSaved: {out_png}")
