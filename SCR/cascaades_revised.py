"""Figure 1 (minimal): Oral PrEP vs. LAI-PrEP circular cascade comparison.

Conceptual focus:
- Oral PrEP: Awareness → Willingness → Eligibility/Initiation are tightly clustered
  (same-day, no meaningful temporal delay). Major loss occurs at 6-month adherence.
- LAI-PrEP: Awareness → Willingness → Eligibility → Bridge/First Injection form an
  elongated arc (multi-week bridge, major structural attrition). Persistence after
  successful initiation is high but only for those who clear the bridge.

Outputs:
• figure1_cascades_minimal.png
• figure1_cascades_minimal.pdf
• figure1_cascades_minimal.svg
"""

from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Iterable, List, Optional, Tuple

import matplotlib.pyplot as plt
import matplotlib.patheffects as pe
from matplotlib.patches import Circle, FancyBboxPatch

# -----------------------------
# Global sizing (inches)
# -----------------------------

# Layout constants (in inches)
OUTER_NODE_R_IN = 0.45  # Radius of outer bubble nodes
CALLOUT_EXTRA_OFFSET_IN = 0.075  # Extra offset for callout boxes from outer ring

FIG_W_IN = 16
FIG_H_IN = 8
DPI = 300

# Z-orders (higher renders on top)
Z_DOTTED = 1
Z_RING_FILL = 2
Z_SHADOW = 3
Z_BUBBLE = 6
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
    zorder: int = Z_BUBBLE,
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
):
    # Dotted rings (back)
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
        fontsize=12,
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


def main():
    fig = plt.figure(figsize=(FIG_W_IN, FIG_H_IN))
    ax = fig.add_axes([0, 0, 1, 1])

    ax.set_xlim(-0.8, FIG_W_IN + 0.8)
    ax.set_ylim(-0.6, FIG_H_IN)
    ax.set_aspect("equal")
    ax.axis("off")

    # -----------------------------
    # Titles
    # -----------------------------
    ax.text(
        FIG_W_IN / 2,
        FIG_H_IN - 0.35,
        "Oral PrEP vs. LAI-PrEP: Circular Cascade Comparison",
        ha="center",
        va="top",
        fontsize=20,
        fontweight="bold",
        color="#0f172a",
        zorder=Z_TEXT,
    )

    ax.text(
        FIG_W_IN / 2,
        FIG_H_IN - 0.78,
        "Temporal paradox: same-day oral initiation vs. delayed LAI bridge",
        ha="center",
        va="top",
        fontsize=11,
        color="#334155",
        zorder=Z_TEXT,
    )

    # -----------------------------
    # Header panels
    # -----------------------------
    header_y = FIG_H_IN - 1.80
    header_h = 0.95
    header_w = 6.6

    # Left header
    add_rounded_box(
        ax,
        (0.8, header_y),
        header_w,
        header_h,
        face="#c8f7d8",
        edge="#1f7a4a",
        lw=2,
        rounding=0.12,
        zorder=Z_BUBBLE,
        shadow=False,
    )

    ax.text(
        0.8 + header_w / 2,
        header_y + header_h * 0.62,
        "ORAL PrEP CASCADE",
        ha="center",
        va="center",
        fontsize=14,
        fontweight="bold",
        color="#1f7a4a",
        zorder=Z_TEXT,
    )

    ax.text(
        0.8 + header_w / 2,
        header_y + header_h * 0.28,
        "Same-day HIV test • Rx • Pill in mouth",
        ha="center",
        va="center",
        fontsize=9,
        fontweight="bold",
        color="#0f172a",
        zorder=Z_TEXT,
    )

    # Right header
    add_rounded_box(
        ax,
        (FIG_W_IN - 0.8 - header_w, header_y),
        header_w,
        header_h,
        face="#ffeab0",
        edge="#d48806",
        lw=2,
        rounding=0.12,
        zorder=Z_BUBBLE,
        shadow=False,
    )

    ax.text(
        FIG_W_IN - 0.8 - header_w / 2,
        header_y + header_h * 0.62,
        "LAI-PrEP CASCADE",
        ha="center",
        va="center",
        fontsize=14,
        fontweight="bold",
        color="#b45309",
        zorder=Z_TEXT,
    )

    ax.text(
        FIG_W_IN - 0.8 - header_w / 2,
        header_y + header_h * 0.28,
        "2–8 week bridge to first injection",
        ha="center",
        va="center",
        fontsize=9,
        fontweight="bold",
        color="#0f172a",
        zorder=Z_TEXT,
    )

    # -----------------------------
    # Cascade layout constants
    # -----------------------------
    ring_radius_oral = 2.35   # slightly tighter ring to reinforce “no temporal gap”
    ring_radius_lai = 2.75    # slightly larger to visually elongate the bridge
    dotted_r1 = 1.75
    dotted_r2 = 2.35

    left_center = (4.35, 3.10)
    right_center = (11.65, 3.10)

    # -----------------------------
    # Oral PrEP cascade (left)
    # -----------------------------
    text_kw_white = dict(ha="center", va="center", fontsize=8, color="white", fontweight="bold")
    text_kw_dark = dict(ha="center", va="center", fontsize=7.5, color="#0f172a", fontweight="bold")

    oral_bubbles = [
        Bubble(
            angle_deg=100,
            radius=0.55,
            face="#2e7d62",
            edge="#1b5e46",
            lw=2,
            text="1. Awareness\n\nCommunity & provider\nknowledge",
            text_kwargs=text_kw_white,
        ),
        Bubble(
            angle_deg=70,
            radius=0.55,
            face="#3fa37b",
            edge="#2b7a5d",
            lw=2,
            text="2. Willingness\n\nReady to start",
            text_kwargs=text_kw_white,
        ),
        Bubble(
            angle_deg=40,
            radius=0.55,
            face="#53b98a",
            edge="#2b7a5d",
            lw=2,
            text="3. Eligibility\n& Initiation\n\nHIV−, Rx written,\nPill started\nsame day",
            text_kwargs=text_kw_white,
        ),
        Bubble(
            angle_deg=-110,
            radius=0.65,
            face="#baf6dd",
            edge="#86d8b8",
            lw=2,
            text="6‑month\nAdherence\n\n≈50% retained",
            text_kwargs=text_kw_dark,
        ),
    ]

    draw_cascade(
        ax,
        center=left_center,
        ring_radius=ring_radius_oral,
        ring_radii_dotted=(dotted_r1, dotted_r2),
        central_radius=1.10,
        central_face="#b8322a",
        central_edge="#7f1d1d",
        central_text="ADHERENCE &\nPERSISTENCE\n\nCritical Barrier\n\n40–50% lost\nby 6 months",
        outer_bubbles=oral_bubbles,
    )

    # -----------------------------
    # LAI-PrEP cascade (right)
    # -----------------------------
    lai_text_kw = dict(ha="center", va="center", fontsize=7.8, color="white", fontweight="bold")

    lai_bubbles = [
        Bubble(
            angle_deg=110,
            radius=0.55,
            face="#6d28d9",
            edge="#4c1d95",
            lw=2,
            text="1. Awareness\n\nLAI-PrEP exists",
            text_kwargs=lai_text_kw,
        ),
        Bubble(
            angle_deg=70,
            radius=0.55,
            face="#8b5cf6",
            edge="#6d28d9",
            lw=2,
            text="2. Willingness\n\nPrefers injections",
            text_kwargs=lai_text_kw,
        ),
        Bubble(
            angle_deg=30,
            radius=0.55,
            face="#5b5bd6",
            edge="#3730a3",
            lw=2,
            text="3. Eligibility\n\nEnhanced HIV testing,\nacute HIV ruled out",
            text_kwargs=lai_text_kw,
        ),
        Bubble(
            angle_deg=-10,
            radius=0.65,
            face="#3b82f6",
            edge="#1d4ed8",
            lw=2,
            text="4. Bridge /\nFirst Injection\n\n2–8 weeks,\n~47% lost",
            text_kwargs=lai_text_kw,
        ),
        Bubble(
            angle_deg=-110,
            radius=0.60,
            face="#2f9e8f",
            edge="#0f766e",
            lw=2,
            text="12‑month\nPersistence\n\n≈81–85%\nof initiators",
            text_kwargs=dict(ha="center", va="center", fontsize=7.0, color="white", fontweight="bold"),
        ),
    ]

    draw_cascade(
        ax,
        center=right_center,
        ring_radius=ring_radius_lai,
        ring_radii_dotted=(dotted_r1, dotted_r2),
        central_radius=1.10,
        central_face="#b8322a",
        central_edge="#7f1d1d",
        central_text="BRIDGE\nNAVIGATION\n\n2–8 Weeks\n\n47.1% lost\nbefore first dose",
        outer_bubbles=lai_bubbles,
    )

    # Bottom subtle divider
    ax.plot([0.5, FIG_W_IN - 0.5], [0.35, 0.35], color="#e2e8f0", lw=1, zorder=Z_DOTTED)

    # Create output directory if it doesn't exist
    import os
    output_dir = os.path.join(os.path.dirname(__file__), 'figures')
    os.makedirs(output_dir, exist_ok=True)
    
    # Save with relative path
    out_base = os.path.join(output_dir, "figure1_cascades_minimal")
    fig.savefig(out_base + ".png", dpi=DPI, bbox_inches="tight")
    fig.savefig(out_base + ".pdf", bbox_inches="tight")
    fig.savefig(out_base + ".svg", bbox_inches="tight")
    plt.close(fig)
    
    print(f"✓ Figures saved to: {output_dir}")


if __name__ == "__main__":
    main()
