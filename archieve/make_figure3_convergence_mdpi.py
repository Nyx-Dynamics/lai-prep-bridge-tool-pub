import os
import numpy as np
import matplotlib.pyplot as plt

"""
MDPI-style regeneration of figure3_convergence (minimal text)
- Dual-axis plot: left y = Margin of Error (±pp, log scale), right y = Processing Speed
- X = Validation tiers: 1K, 1M, 10M, 21.2M
- Minimal text: numeric axes only, no annotations or sentences
- Output: PDF + 600 dpi PNG at ~180 mm width
"""

# Sample sizes (ordered)
x_labels = ["1K", "1M", "10M", "21.2M"]
x = np.arange(len(x_labels))

# Values approximated from the existing PNG
margin_error_pp = np.array([2.4, 0.09, 0.03, 0.015])  # ± percentage points
processing_speed = np.array([1200, 18000, 98000, 82000])  # patients/second

fig, ax1 = plt.subplots(figsize=(7.09, 4.72), dpi=300)

# Left axis: Margin of Error (log scale)
ax1.set_yscale('log')
ax1.plot(x, margin_error_pp, color="#D55E00", marker='o', lw=1.5)
ax1.set_xlim(-0.2, len(x_labels)-0.8)
ax1.set_xticks(x)
ax1.set_xticklabels(x_labels)
ax1.set_xlabel("Validation size")
ax1.set_ylabel("Margin of error (± pp, log)")

# Shade a low-error zone (0 to 0.05 pp) for visual reference (no label text)
ax1.axhspan(0.015, 0.05, color="#A5D6A7", alpha=0.35, zorder=0)

# Right axis: Processing speed
ax2 = ax1.twinx()
ax2.plot(x, processing_speed, color="#0072B2", marker='s', lw=1.5)
ax2.set_ylabel("Throughput (patients/s)")

# Grid and margins
ax1.grid(True, which='both', axis='y', linestyle=':', linewidth=0.6, alpha=0.5)
plt.subplots_adjust(bottom=0.12, left=0.12, right=0.88, top=0.96)

out_pdf = os.path.join("figures", "figure3_convergence_MDPI.pdf")
out_png = os.path.join("figures", "figure3_convergence_MDPI.png")
fig.savefig(out_pdf, bbox_inches='tight')
fig.savefig(out_png, dpi=600, bbox_inches='tight')
print(f"Saved: {out_pdf}\nSaved: {out_png}")
