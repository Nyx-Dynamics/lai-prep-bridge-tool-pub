import os
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, ArrowStyle

"""
MDPI-style redesign of figure1_critical_insights (minimal text)
- 2×2 tile grid with numeric tokens and simple glyphs (no sentences)
- Tiles:
  A) Oral PrEP post-init adherence ~30%
  B) LAI PrEP post-init persistence 81–92%
  C) Pre-init bridge loss 47.1%
  D) Barrier shift: post → pre (bridge)
- Output: PDF (vector) + PNG (600 dpi) targeting ~180 mm × 120 mm
"""

# Canvas
fig, axes = plt.subplots(2, 2, figsize=(7.09, 4.72), dpi=300)
plt.subplots_adjust(wspace=0.16, hspace=0.2, left=0.04, right=0.98, top=0.96, bottom=0.10)

# Colors (Okabe–Ito inspired, print safe)
BLUE = "#56B4E9"
ORANGE = "#E69F00"
GREEN = "#009E73"
PURPLE = "#CC79A7"
GREY = "#4D4D4D"
LIGHT = "#F7F7F7"

# Helper to draw a rounded tile background
def tile(ax, face):
    ax.set_axis_off()
    box = FancyBboxPatch((0.02, 0.02), 0.96, 0.96, transform=ax.transAxes,
                         boxstyle="round,pad=0.02,rounding_size=0.04",
                         linewidth=0.8, edgecolor=GREY, facecolor=face, alpha=0.96)
    ax.add_patch(box)

# Tile A: Oral PrEP adherence ~30%
axA = axes[0, 0]
tile(axA, LIGHT)
axA.text(0.08, 0.78, "Oral PrEP", fontsize=9, fontweight='bold', color=GREY, transform=axA.transAxes)
axA.text(0.08, 0.46, "≈30%", fontsize=22, fontweight='bold', color=ORANGE, transform=axA.transAxes)
axA.text(0.08, 0.20, "post-init adherence", fontsize=8, color=GREY, transform=axA.transAxes)

# Simple pill glyph (two rounded rectangles)
axA.add_patch(FancyBboxPatch((0.62, 0.58), 0.26, 0.18, transform=axA.transAxes,
                             boxstyle="round,pad=0.02,rounding_size=0.08",
                             linewidth=0.8, edgecolor=GREY, facecolor="#FFFFFF"))
axA.add_patch(FancyBboxPatch((0.62, 0.40), 0.26, 0.18, transform=axA.transAxes,
                             boxstyle="round,pad=0.02,rounding_size=0.08",
                             linewidth=0.8, edgecolor=GREY, facecolor="#FFFFFF", hatch='///'))

# Tile B: LAI persistence 81–92%
axB = axes[0, 1]
tile(axB, LIGHT)
axB.text(0.08, 0.78, "LAI PrEP", fontsize=9, fontweight='bold', color=GREY, transform=axB.transAxes)
axB.text(0.08, 0.46, "81–92%", fontsize=22, fontweight='bold', color=GREEN, transform=axB.transAxes)
axB.text(0.08, 0.20, "post-init persistence", fontsize=8, color=GREY, transform=axB.transAxes)

# Simple syringe-like glyph (minimal)
axB.plot([0.70, 0.92], [0.62, 0.62], color=GREY, lw=1.2, transform=axB.transAxes)
axB.plot([0.82, 0.82], [0.54, 0.70], color=GREY, lw=1.2, transform=axB.transAxes)
axB.plot([0.88, 0.92], [0.54, 0.58], color=GREY, lw=1.2, transform=axB.transAxes)

# Tile C: Pre-init bridge loss 47.1%
axC = axes[1, 0]
tile(axC, LIGHT)
axC.text(0.08, 0.78, "Pre-init bridge", fontsize=9, fontweight='bold', color=GREY, transform=axC.transAxes)
axC.text(0.08, 0.46, "47.1%", fontsize=22, fontweight='bold', color=PURPLE, transform=axC.transAxes)
axC.text(0.08, 0.20, "lost before first dose", fontsize=8, color=GREY, transform=axC.transAxes)

# Bridge glyph: two boxes and a gap
axC.add_patch(FancyBboxPatch((0.62, 0.55), 0.12, 0.16, transform=axC.transAxes,
                             boxstyle="round,pad=0.02,rounding_size=0.06",
                             linewidth=0.8, edgecolor=GREY, facecolor="#FFFFFF"))
axC.add_patch(FancyBboxPatch((0.78, 0.55), 0.12, 0.16, transform=axC.transAxes,
                             boxstyle="round,pad=0.02,rounding_size=0.06",
                             linewidth=0.8, edgecolor=GREY, facecolor="#FFFFFF", hatch='///'))

# Tile D: Barrier shift (post → pre)
axD = axes[1, 1]
tile(axD, LIGHT)
axD.text(0.08, 0.78, "Barrier shift", fontsize=9, fontweight='bold', color=GREY, transform=axD.transAxes)
axD.text(0.08, 0.46, "post → pre", fontsize=18, fontweight='bold', color=BLUE, transform=axD.transAxes)
axD.text(0.08, 0.20, "implementation paradox", fontsize=8, color=GREY, transform=axD.transAxes)

# Arrow cue (curved), minimal
axD.annotate('', xy=(0.86, 0.62), xytext=(0.50, 0.62), xycoords=axD.transAxes,
             arrowprops=dict(arrowstyle=ArrowStyle('simple', head_length=6, head_width=6),
                             lw=0.8, color=GREY, alpha=0.9, shrinkA=0, shrinkB=0,
                             connectionstyle='arc3,rad=0.0'))

# Footer tokens row (symbol-only style)
fig.text(0.5, 0.04, "Oral ≈30   LAI 81–92   Bridge 47.1   Shift post→pre", ha='center', va='center', fontsize=8, color=GREY)

out_pdf = os.path.join('figures', 'figure1_critical_insights_MDPI.pdf')
out_png = os.path.join('figures', 'figure1_critical_insights_MDPI.png')
fig.savefig(out_pdf, bbox_inches='tight')
fig.savefig(out_png, dpi=600, bbox_inches='tight')
print(f"Saved: {out_pdf}\nSaved: {out_png}")
