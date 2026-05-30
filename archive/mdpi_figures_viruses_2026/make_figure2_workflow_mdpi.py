import os
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Circle

"""
MDPI-style minimal-text workflow schematic for figure2_workflow
- Five stages shown as rounded rectangles with numbers 1–5
- Vertical flow with arrows; minimal legend mapping numbers to short labels
- Output: PDF + 600 dpi PNG at ~180 mm width
"""

# Canvas
fig, ax = plt.subplots(figsize=(7.09, 4.72), dpi=300)
ax.set_xlim(0, 10)
ax.set_ylim(0, 10)
ax.axis('off')

# Positions for boxes (from top to bottom)
y_positions = [8.5, 6.9, 5.3, 3.7, 2.1]
labels = [
    "Patient\nPresentation",
    "Risk\nStratification",
    "Barrier\nAssessment",
    "Intervention\nRecommendation",
    "Outcome\nPrediction",
]
colors = ["#56B4E9", "#E69F00", "#D55E00", "#CC79A7", "#009E73"]

# Draw numbered boxes
for i, (y, lab, col) in enumerate(zip(y_positions, labels, colors), start=1):
    box = FancyBboxPatch((2, y-0.7), 6, 1.2, boxstyle="round,pad=0.02,rounding_size=0.2",
                          linewidth=1.2, edgecolor="#333333", facecolor=col, alpha=0.95)
    ax.add_patch(box)
    # Number token on the left as a small circle
    circ = Circle((1.1, y-0.1), radius=0.28, facecolor=col, edgecolor="#333333", linewidth=1.0)
    ax.add_patch(circ)
    ax.text(1.1, y-0.1, str(i), va='center', ha='center', fontsize=9, fontweight='bold', color='white')
    # Minimal label inside box (two lines max)
    ax.text(5, y-0.1, lab, va='center', ha='center', fontsize=8, color='white', fontweight='bold')
    # Arrow down except last
    if i < 5:
        ax.annotate('', xy=(5, y-0.7), xytext=(5, y-1.0),
                    arrowprops=dict(arrowstyle='->', lw=1.2, color='#444444'))

# Minimal legend (numbers → labels), placed at bottom
legend_items = [f"{i}" for i in range(1,6)]
legend_labels = [
    "Patient",
    "Risk",
    "Barriers",
    "Interv.",
    "Outcome",
]
# Render legend as a simple row of tokens and short words
x0, y0 = 1.0, 0.5
for k, (tok, cap, col) in enumerate(zip(legend_items, legend_labels, colors)):
    x = x0 + k*1.6
    circ = Circle((x, y0), radius=0.16, facecolor=col, edgecolor='#333333', lw=0.8)
    ax.add_patch(circ)
    ax.text(x, y0, tok, va='center', ha='center', fontsize=7, color='white', fontweight='bold')
    ax.text(x+0.35, y0, cap, va='center', ha='left', fontsize=7, color='#333333')

# Subtle recycling loop: curved arrow from step 5 back to step 1 along right margin
# Make the curve convex relative to the boxes (bowing outward to the right) and positioned close to box edges
# Derive geometry from box layout to keep placement robust to future tweaks
box_x, box_w, box_h = 2.0, 6.0, 1.2
x_right = box_x + box_w
proximity_dx = 0.4   # distance from box right edge to loop (closer to boxes)
x_loop = x_right + proximity_dx
# Compute near-edge y coordinates with a small padding to avoid touching corners
pad = 0.1
y_top = y_positions[0] + (box_h/2) - pad
y_bot = y_positions[-1] - (box_h/2) + pad
ax.annotate('', xy=(x_loop, y_top), xytext=(x_loop, y_bot),
            arrowprops=dict(arrowstyle='-|>', lw=1.0, color='#666666',
                            connectionstyle='arc3,rad=0.6', alpha=0.85),
            clip_on=False)

plt.subplots_adjust(left=0.02, right=0.98, top=0.98, bottom=0.14)

out_pdf = os.path.join('figures', 'figure2_workflow_MDPI.pdf')
out_png = os.path.join('figures', 'figure2_workflow_MDPI.png')
fig.savefig(out_pdf, bbox_inches='tight')
fig.savefig(out_png, dpi=600, bbox_inches='tight')
print(f"Saved: {out_pdf}\nSaved: {out_png}")
