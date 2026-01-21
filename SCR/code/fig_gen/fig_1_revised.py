"""Figure 1: Oral PrEP vs. LAI-PrEP circular cascade comparison (FIXED - No overlaps).

Key fixes:
  1) Increased ring radius and figure width to prevent overlap
  2) Repositioned callouts further from circles with larger gaps
  3) Adjusted bubble angles to create more separation
  4) Manual dx/dy adjustments for each callout to ensure no overlap

Outputs:
  • figure1_cascades_fixed.png
  • figure1_cascades_fixed.pdf
  • figure1_cascades_fixed.svg
"""

from __future__ import annotations

import math
import os
from dataclasses import dataclass
from typing import Iterable, List, Optional, Tuple

import matplotlib.pyplot as plt
import matplotlib.patheffects as pe
from matplotlib.patches import Circle, FancyBboxPatch

# Layout constants (in inches)
OUTER_NODE_R_IN = 0.45  # Original size
ORAL_BUBBLE_R_IN = OUTER_NODE_R_IN * 1.2  # 20% larger = 0.54
CALLOUT_EXTRA_OFFSET_IN = 0.075  # Extra offset for callout boxes from outer ring

# -----------------------------
# Global sizing (inches) - INCREASED for more spacing
# -----------------------------
FIG_W_IN = 18  # Wider figure
FIG_H_IN = 9   # Taller figure
DPI = 300

# Outer-node radius - REDUCED by 0.125"
OUTER_NODE_R_IN = 0.375  # Reduced from 0.50

# Z-orders (higher renders on top)
Z_DOTTED = 1
Z_RING_FILL = 2
Z_SHADOW = 3
Z_BUBBLE = 6
Z_CALLOUT = 7
Z_TEXT = 10


@dataclass(frozen=True)
class Bubble:
    angle_deg: float
    radius: float
    face: str
    edge: str
    lw: float
    text: str
    text_kwargs: dict


@dataclass(frozen=True)
class Callout:
    anchor_angle_deg: float
    text: str
    width: float
    height: float
    face: str
    edge: str
    lw: float
    text_color: str
    # Optional manual nudges (inches)
    dx: float = 0.0
    dy: float = 0.0


def polar_to_xy(center: Tuple[float, float], r: float, angle_deg: float) -> Tuple[float, float]:
    th = math.radians(angle_deg)
    return (center[0] + r * math.cos(th), center[1] + r * math.sin(th))


def add_rounded_box(
    ax,
    xy: Tuple[float, float],
    w: float,
    h: float,
    face: str,
    edge: str,
    lw: float = 1.5,
    rounding: float = 0.15,
    zorder: int = Z_CALLOUT,
    alpha: float = 1.0,
    shadow: bool = True,
):
    """Add a rounded rectangle where xy is the bottom-left corner."""
    patch = FancyBboxPatch(
        xy,
        w,
        h,
        boxstyle=f"round,pad=0.02,rounding_size={rounding}",
        facecolor=face,
        edgecolor=edge,
        linewidth=lw,
        alpha=alpha,
        zorder=zorder,
    )

    if shadow:
        patch.set_path_effects(
            [
                pe.SimplePatchShadow(offset=(1.5, -1.5), alpha=0.25, rho=0.98),
                pe.Normal(),
            ]
        )

    ax.add_patch(patch)
    return patch


def add_circle(
    ax,
    center: Tuple[float, float],
    r: float,
    face: str,
    edge: str,
    lw: float = 2,
    zorder: int = Z_BUBBLE,
    shadow: bool = True,
    glow: bool = False,
    glow_color: Optional[str] = None,
):
    """Add a circle with optional drop shadow and subtle glow."""
    if glow:
        gc = glow_color or face
        for k, alpha in [(1.15, 0.10), (1.30, 0.06), (1.50, 0.04)]:
            ax.add_patch(
                Circle(
                    center,
                    r * k,
                    facecolor=gc,
                    edgecolor="none",
                    alpha=alpha,
                    zorder=zorder - 1,
                )
            )

    circ = Circle(center, r, facecolor=face, edgecolor=edge, linewidth=lw, zorder=zorder)

    if shadow:
        circ.set_path_effects(
            [
                pe.SimplePatchShadow(offset=(1.8, -1.8), alpha=0.25, rho=0.98),
                pe.Normal(),
            ]
        )

    ax.add_patch(circ)
    return circ


def draw_dotted_rings(
    ax,
    center: Tuple[float, float],
    radii: Iterable[float],
    color: str = "#c7d3e2",
    lw: float = 1.6,
):
    for rr in radii:
        ring = Circle(
            center,
            rr,
            facecolor="none",
            edgecolor=color,
            linewidth=lw,
            linestyle=(0, (2, 2)),
            zorder=Z_DOTTED,
        )
        ax.add_patch(ring)


def draw_cascade(
    ax,
    center: Tuple[float, float],
    ring_radius: float,
    ring_radii_dotted: Tuple[float, float],
    central_radius: float,
    central_face: str,
    central_edge: str,
    central_text: str,
    outer_bubbles: List[Bubble],
    callouts: List[Callout],
):
    # Dotted rings first (back)
    draw_dotted_rings(ax, center, ring_radii_dotted)

    # Central bubble
    add_circle(
        ax,
        center,
        central_radius,
        face=central_face,
        edge=central_edge,
        lw=3,
        zorder=Z_BUBBLE,
        shadow=True,
        glow=True,
        glow_color="#d24b43",
    )
    ax.text(
        center[0],
        center[1] + 0.10,
        central_text,
        ha="center",
        va="center",
        color="white",
        fontsize=11,
        fontweight="bold",
        zorder=Z_TEXT,
    )

    # Outer bubbles
    for b in outer_bubbles:
        xy = polar_to_xy(center, ring_radius, b.angle_deg)
        add_circle(
            ax,
            xy,
            b.radius,
            face=b.face,
            edge=b.edge,
            lw=b.lw,
            zorder=Z_BUBBLE,
            shadow=True,
        )
        ax.text(
            xy[0],
            xy[1],
            b.text,
            zorder=Z_TEXT,
            **b.text_kwargs,
        )

    # Callouts (overlay boxes) - positioned OUTSIDE the ring with guaranteed clearance
    for c in callouts:
        anchor_xy = polar_to_xy(center, ring_radius, c.anchor_angle_deg)

        # Direction from center to anchor (unit vector)
        th = math.radians(c.anchor_angle_deg)
        ux, uy = math.cos(th), math.sin(th)

        # Calculate safe distance: bubble radius + gap + half of box diagonal projection
        hw, hh = c.width / 2, c.height / 2
        d_rect = hw * abs(ux) + hh * abs(uy)

        # Large gap to ensure no overlap
        gap = CALLOUT_EXTRA_OFFSET_IN + 0.20
        radial_shift = OUTER_NODE_R_IN + gap + d_rect

        callout_center = (
            anchor_xy[0] + ux * radial_shift + c.dx,
            anchor_xy[1] + uy * radial_shift + c.dy,
        )

        # Convert from callout center to bottom-left
        bl = (callout_center[0] - c.width / 2, callout_center[1] - c.height / 2)
        add_rounded_box(
            ax,
            bl,
            c.width,
            c.height,
            face=c.face,
            edge=c.edge,
            lw=c.lw,
            rounding=0.10,
            zorder=Z_CALLOUT,
            shadow=True,
        )

        ax.text(
            callout_center[0],
            callout_center[1],
            c.text,
            ha="center",
            va="center",
            color=c.text_color,
            fontsize=8.5,
            fontweight="bold",
            zorder=Z_TEXT,
        )


# Define Z-order for title boxes
Z_TITLE = 5

# Oral PrEP cascade data
oral_bubbles = [
    Bubble(
        angle_deg=90,
        radius=OUTER_NODE_R_IN,
        face="#81c784",
        edge="#2e7d32",
        lw=2,
        text="Need\nPrEP",
        text_kwargs={"ha": "center", "va": "center", "color": "white", "fontsize": 9, "fontweight": "bold"},
    ),
    Bubble(
        angle_deg=30,
        radius=OUTER_NODE_R_IN,
        face="#66bb6a",
        edge="#2e7d32",
        lw=2,
        text="Screen\n& Offer",
        text_kwargs={"ha": "center", "va": "center", "color": "white", "fontsize": 8, "fontweight": "bold"},
    ),
    Bubble(
        angle_deg=330,
        radius=OUTER_NODE_R_IN,
        face="#4caf50",
        edge="#2e7d32",
        lw=2,
        text="Same\nDay\nStart",
        text_kwargs={"ha": "center", "va": "center", "color": "white", "fontsize": 8, "fontweight": "bold"},
    ),
    Bubble(
        angle_deg=270,
        radius=OUTER_NODE_R_IN,
        face="#43a047",
        edge="#2e7d32",
        lw=2,
        text="Daily\nPill",
        text_kwargs={"ha": "center", "va": "center", "color": "white", "fontsize": 8, "fontweight": "bold"},
    ),
    Bubble(
        angle_deg=210,
        radius=OUTER_NODE_R_IN,
        face="#388e3c",
        edge="#2e7d32",
        lw=2,
        text="On\nPrEP",
        text_kwargs={"ha": "center", "va": "center", "color": "white", "fontsize": 9, "fontweight": "bold"},
    ),
    Bubble(
        angle_deg=150,
        radius=OUTER_NODE_R_IN,
        face="#2e7d32",
        edge="#1b5e20",
        lw=2,
        text="Persist\n12mo",
        text_kwargs={"ha": "center", "va": "center", "color": "white", "fontsize": 8, "fontweight": "bold"},
    ),
]

oral_callouts = [
    Callout(
        anchor_angle_deg=90,
        text="100% Eligible",
        width=1.2,
        height=0.35,
        face="#e8f5e9",
        edge="#2e7d32",
        lw=1.8,
        text_color="#1b5e20",
        dy=0.1,
    ),
    Callout(
        anchor_angle_deg=30,
        text="95% Screened",
        width=1.2,
        height=0.35,
        face="#e8f5e9",
        edge="#2e7d32",
        lw=1.8,
        text_color="#1b5e20",
        dx=0.15,
    ),
    Callout(
        anchor_angle_deg=330,
        text="90% Start",
        width=1.1,
        height=0.35,
        face="#e8f5e9",
        edge="#2e7d32",
        lw=1.8,
        text_color="#1b5e20",
        dx=0.15,
    ),
    Callout(
        anchor_angle_deg=270,
        text="85% Initiate",
        width=1.2,
        height=0.35,
        face="#e8f5e9",
        edge="#2e7d32",
        lw=1.8,
        text_color="#1b5e20",
        dy=-0.1,
    ),
    Callout(
        anchor_angle_deg=210,
        text="70% at 6mo",
        width=1.2,
        height=0.35,
        face="#fff9c4",
        edge="#f57c00",
        lw=1.8,
        text_color="#e65100",
        dx=-0.15,
    ),
    Callout(
        anchor_angle_deg=150,
        text="52% at 12mo",
        width=1.3,
        height=0.35,
        face="#ffccbc",
        edge="#d32f2f",
        lw=1.8,
        text_color="#b71c1c",
        dx=-0.15,
    ),
]

# LAI-PrEP cascade data
lai_bubbles = [
    Bubble(
        angle_deg=90,
        radius=OUTER_NODE_R_IN,
        face="#ffb74d",
        edge="#e65100",
        lw=2,
        text="Need\nPrEP",
        text_kwargs={"ha": "center", "va": "center", "color": "white", "fontsize": 9, "fontweight": "bold"},
    ),
    Bubble(
        angle_deg=30,
        radius=OUTER_NODE_R_IN,
        face="#ffa726",
        edge="#e65100",
        lw=2,
        text="Screen\n& Offer",
        text_kwargs={"ha": "center", "va": "center", "color": "white", "fontsize": 8, "fontweight": "bold"},
    ),
    Bubble(
        angle_deg=330,
        radius=OUTER_NODE_R_IN,
        face="#ff9800",
        edge="#e65100",
        lw=2,
        text="Bridge\nStart",
        text_kwargs={"ha": "center", "va": "center", "color": "white", "fontsize": 8, "fontweight": "bold"},
    ),
    Bubble(
        angle_deg=270,
        radius=OUTER_NODE_R_IN,
        face="#fb8c00",
        edge="#e65100",
        lw=2,
        text="1st\nInjection",
        text_kwargs={"ha": "center", "va": "center", "color": "white", "fontsize": 8, "fontweight": "bold"},
    ),
    Bubble(
        angle_deg=210,
        radius=OUTER_NODE_R_IN,
        face="#f57c00",
        edge="#e65100",
        lw=2,
        text="On\nLAI",
        text_kwargs={"ha": "center", "va": "center", "color": "white", "fontsize": 9, "fontweight": "bold"},
    ),
    Bubble(
        angle_deg=150,
        radius=OUTER_NODE_R_IN,
        face="#e65100",
        edge="#bf360c",
        lw=2,
        text="",
        text_kwargs={"ha": "center", "va": "center", "color": "white", "fontsize": 8, "fontweight": "bold"},
    ),
]

lai_callouts = [
    Callout(
        anchor_angle_deg=90,
        text="100% Eligible",
        width=1.2,
        height=0.35,
        face="#fff9c4",
        edge="#f57c00",
        lw=1.8,
        text_color="#e65100",
        dy=0.1,
    ),
    Callout(
        anchor_angle_deg=30,
        text="95% Screened",
        width=1.2,
        height=0.35,
        face="#fff9c4",
        edge="#f57c00",
        lw=1.8,
        text_color="#e65100",
        dx=0.15,
    ),
    Callout(
        anchor_angle_deg=330,
        text="90% Bridge",
        width=1.2,
        height=0.35,
        face="#fff9c4",
        edge="#f57c00",
        lw=1.8,
        text_color="#e65100",
        dx=0.15,
    ),
    Callout(
        anchor_angle_deg=270,
        text="47.6% to LAI",
        width=1.3,
        height=0.35,
        face="#ffccbc",
        edge="#d32f2f",
        lw=1.8,
        text_color="#b71c1c",
        dy=-0.1,
    ),
    Callout(
        anchor_angle_deg=210,
        text="45% at 6mo",
        width=1.2,
        height=0.35,
        face="#ffccbc",
        edge="#d32f2f",
        lw=1.8,
        text_color="#b71c1c",
        dx=-0.15,
    ),
    Callout(
        anchor_angle_deg=150,
        text="42% at 12mo",
        width=1.3,
        height=0.35,
        face="#ffccbc",
        edge="#d32f2f",
        lw=1.8,
        text_color="#b71c1c",
        dx=-0.15,
    ),
]


def main():
    """Generate the dual cascade comparison figure"""
    
    # Create figure
    fig, ax = plt.subplots(figsize=(16, 10), dpi=300)
    ax.set_xlim(-8, 8)
    ax.set_ylim(-6, 6)
    ax.set_aspect("equal")
    ax.axis("off")
    
    # Define centers and radii
    left_center = (-4.5, 0)
    right_center = (4.5, 0)
    ring_radius = 2.5
    dotted_r1 = 3.2
    dotted_r2 = 3.8
    
    # Draw left cascade (Oral PrEP)
    draw_cascade(
        ax,
        center=left_center,
        ring_radius=ring_radius,
        ring_radii_dotted=(dotted_r1, dotted_r2),
        central_radius=1.05,
        central_face="#b8322a",
        central_edge="#7f1d1d",
        central_text="ADHERENCE &\nPERSISTENCE\n\n40–48% Lost",
        outer_bubbles=oral_bubbles,
        callouts=oral_callouts,
    )
    
    # Draw right cascade (LAI-PrEP)
    draw_cascade(
        ax,
        center=right_center,
        ring_radius=ring_radius,
        ring_radii_dotted=(dotted_r1, dotted_r2),
        central_radius=1.05,
        central_face="#9c27b0",
        central_edge="#6a1b9a",
        central_text="BRIDGE\nNAVIGATION\n\n2–8 Weeks\n\n47.1% Lost",
        outer_bubbles=lai_bubbles,
        callouts=lai_callouts,
    )
    
    # Add title boxes (lowered by 0.125")
    top_y = 4.5 - 0.125  # Lowered by 0.125"
    
    # Oral PrEP title box
    add_rounded_box(
        ax,
        (left_center[0] - 3.0, top_y),
        6.0,
        0.9,
        face="#c8e6c9",
        edge="#2e7d32",
        lw=2.5,
        rounding=0.15,
        zorder=Z_TITLE,
        shadow=True,
    )
    ax.text(
        left_center[0],
        top_y + 0.45,
        "ORAL PrEP CASCADE\nSame-Day Start Available • Daily Pill",
        ha="center",
        va="center",
        fontsize=12,
        fontweight="bold",
        color="#1b5e20",
        zorder=Z_TEXT,
    )
    
    # LAI-PrEP title box
    add_rounded_box(
        ax,
        (right_center[0] - 3.0, top_y),
        6.0,
        0.9,
        face="#fff9c4",
        edge="#f57c00",
        lw=2.5,
        rounding=0.15,
        zorder=Z_TITLE,
        shadow=True,
    )
    ax.text(
        right_center[0],
        top_y + 0.45,
        "LAI-PrEP CASCADE\nMandatory 2–8 Week Bridge • Bimonthly Injection",
        ha="center",
        va="center",
        fontsize=12,
        fontweight="bold",
        color="#e65100",
        zorder=Z_TEXT,
    )
    
    # Save outputs
    out_base = "figure1_cascades_fixed"
    fig.savefig(f"{out_base}.png", dpi=600, bbox_inches="tight")
    fig.savefig(f"{out_base}.pdf", bbox_inches="tight")
    fig.savefig(f"{out_base}.svg", bbox_inches="tight")
    plt.close()
    
    print(f"Saved to {out_base}.png, .pdf, .svg")


if __name__ == "__main__":
    main()