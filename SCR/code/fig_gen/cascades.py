"""Figure 1: Oral PrEP vs. LAI-PrEP circular cascade comparison (code-generated).

This script recreates the figure using matplotlib primitives so the layout is editable
via code.

Requested layout corrections implemented:
  1) Prevent overlaps by tuning bubble angles and using an adequate ring radius.
  2) Ensure all bubbles/callouts are drawn above the dotted rings (explicit z-order).
  3) Move dotted rings behind everything.
  4) Move all overlay callouts an additional 0.075 inches away from the outer ring.

Outputs:
  • figure1_cascades_fixed.png
  • figure1_cascades_fixed.pdf
  • figure1_cascades_fixed.svg

Run:
  python figure1_cascades_fixed.py
"""

from __future__ import annotations

import math
import os
from dataclasses import dataclass
from typing import Iterable, List, Optional, Tuple

import matplotlib.pyplot as plt
import matplotlib.patheffects as pe
from matplotlib.patches import Circle, FancyBboxPatch


# -----------------------------
# Global sizing (inches)
# -----------------------------
FIG_W_IN = 16
FIG_H_IN = 8
DPI = 300

# Required edge-to-edge separation between overlay callouts and the outer ring bubbles.
# (Per request: move overlay bubbles 0.075" away from the outer ring.)
CALLOUT_EXTRA_OFFSET_IN = 0.075

# Outer-node radius (used to ensure callouts clear the circular bubbles)
OUTER_NODE_R_IN = 0.55

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
        # Soft glow via concentric translucent circles (cheap, deterministic).
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
        fontsize=12,
        fontweight="bold",
        zorder=Z_TEXT,
    )

    # Outer bubbles
    bubble_centers = {}
    for b in outer_bubbles:
        xy = polar_to_xy(center, ring_radius, b.angle_deg)
        bubble_centers[b.text] = xy
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

    # Callouts (overlay bubbles)
    for c in callouts:
        anchor_xy = polar_to_xy(center, ring_radius, c.anchor_angle_deg)

        # Direction from center to anchor (unit vector)
        th = math.radians(c.anchor_angle_deg)
        ux, uy = math.cos(th), math.sin(th)

        # Place callout center outside the outer bubble edge with a guaranteed
        # clearance so the callout rectangle does not overlap the circle.
        #
        # For an axis-aligned rectangle centered at (x,y) with half-width hw and
        # half-height hh, the distance from center to the rectangle boundary in
        # direction (ux,uy) is: d_rect = hw*|ux| + hh*|uy|.
        hw, hh = c.width / 2, c.height / 2
        d_rect = hw * abs(ux) + hh * abs(uy)

        # Increase clearance between callout boxes and bubble circles.
        # User requested 0.075" away from the outer ring.
        gap = CALLOUT_EXTRA_OFFSET_IN + 0.125  # Adding extra base gap to ensure no overlap with circles
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


def main():
    fig = plt.figure(figsize=(FIG_W_IN, FIG_H_IN))
    ax = fig.add_axes([0, 0, 1, 1])
    # Add a small margin so outward-offset callouts are never clipped.
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
        "Identifying Critical Barriers Across the Prevention Continuum",
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
        zorder=Z_CALLOUT,
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
        "Same-Day Start Available \u2022 Daily Pill",
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
        zorder=Z_CALLOUT,
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
        "Mandatory 2\u20138 Week Bridge \u2022 Bimonthly Injection",
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
    ring_radius = 2.55
    dotted_r1 = 1.75
    dotted_r2 = 2.35

    left_center = (4.35, 3.10)
    right_center = (11.65, 3.10)

    # -----------------------------
    # Oral PrEP cascade (left)
    # -----------------------------
    # Text kwargs shared for outer bubbles
    outer_text_kw = dict(ha="center", va="center", fontsize=8, color="white", fontweight="bold")
    outer_text_kw_small = dict(ha="center", va="center", fontsize=7.5, color="white", fontweight="bold")

    oral_bubbles = [
        Bubble(
            angle_deg=100,  # 12 o'clock area, slightly more space
            radius=0.55,
            face="#2e7d62",
            edge="#1b5e46",
            lw=2,
            text="1. Awareness\n\n100%\n\nMSM: 85\u201390%\nTrans: 50\u201370%",
            text_kwargs=dict(**outer_text_kw_small),
        ),
        Bubble(
            angle_deg=78,
            radius=0.55,
            face="#3fa37b",
            edge="#2b7a5d",
            lw=2,
            text="2. Willingness\n\n90\u201395%\n\nInterested",
            text_kwargs=dict(**outer_text_kw_small),
        ),
        Bubble(
            angle_deg=56,
            radius=0.55,
            face="#53b98a",
            edge="#2b7a5d",
            lw=2,
            text="3. Eligibility\n\n85\u201390%\n\nMeets criteria",
            text_kwargs=dict(**outer_text_kw_small),
        ),
        Bubble(
            angle_deg=34,
            radius=0.55,
            face="#72d2a2",
            edge="#3aa978",
            lw=2,
            text="4. Access\n\n75\u201385%\n\nInsurance/appt",
            text_kwargs=dict(**outer_text_kw_small),
        ),
        Bubble(
            angle_deg=12,
            radius=0.55,
            face="#6bd9ac",
            edge="#3aa978",
            lw=2,
            text="5. Linkage\n\n75\u201380%\n\nAttend appt",
            text_kwargs=dict(**outer_text_kw_small),
        ),
        Bubble(
            angle_deg=-10,  # Slightly past 3 o'clock
            radius=0.55,
            face="#77e1b8",
            edge="#3aa978",
            lw=2,
            text="6.\nPrescription\n\n75\u201380%\n\nSame-day start",
            text_kwargs=dict(**outer_text_kw_small),
        ),
        Bubble(
            angle_deg=-90,  # 6 o'clock - huge distance from 3 to 6
            radius=0.55,
            face="#9ef1cd",
            edge="#6acaa3",
            lw=2,
            text="7. Initiation\n\n70\u201378%\n\nFill Rx, start",
            text_kwargs=dict(ha="center", va="center", fontsize=7.3, color="#0f172a", fontweight="bold"),
        ),
        Bubble(
            angle_deg=-150,
            radius=0.55,
            face="#baf6dd",
            edge="#86d8b8",
            lw=2,
            text="8. Adherence\n\n52\u201362%\n\n6 mo retention",
            text_kwargs=dict(ha="center", va="center", fontsize=7.3, color="#0f172a", fontweight="bold"),
        ),
        Bubble(
            angle_deg=170, # More space for "Persistence"
            radius=0.55,
            face="#49b07f",
            edge="#2b7a5d",
            lw=2,
            text="Persistence\n\n52%\n\nContinued use",
            text_kwargs=dict(**outer_text_kw_small),
        ),
    ]

    oral_callouts = [
        Callout(
            anchor_angle_deg=170,
            text="Provider\nAccess",
            width=1.25,
            height=0.55,
            face="#f8fafc",
            edge="#94a3b8",
            lw=1.5,
            text_color="#0f172a",
            dx=-0.35,
            dy=0.35,
        ),
        Callout(
            anchor_angle_deg=78,
            text="Insurance\nCoverage",
            width=1.35,
            height=0.55,
            face="#f8fafc",
            edge="#94a3b8",
            lw=1.5,
            text_color="#0f172a",
            dx=0.15,
            dy=0.55,
        ),
        Callout(
            anchor_angle_deg=-120, # In the middle of the "long distance"
            text="Daily Pill\nBurden",
            width=1.35,
            height=0.55,
            face="#fff5f5",
            edge="#dc2626",
            lw=1.8,
            text_color="#991b1b",
            dx=-0.25,
            dy=-0.35,
        ),
        Callout(
            anchor_angle_deg=-175,
            text="PrEP Stigma",
            width=1.35,
            height=0.50,
            face="#f8fafc",
            edge="#94a3b8",
            lw=1.5,
            text_color="#0f172a",
            dx=-0.35,
            dy=-0.25,
        ),
    ]

    draw_cascade(
        ax,
        center=left_center,
        ring_radius=ring_radius,
        ring_radii_dotted=(dotted_r1, dotted_r2),
        central_radius=1.10,
        central_face="#b8322a",
        central_edge="#7f1d1d",
        central_text="ADHERENCE &\nPERSISTENCE\n\nCritical Barrier\n\n40\u201348% Lost",
        outer_bubbles=oral_bubbles,
        callouts=oral_callouts,
    )

    # -----------------------------
    # LAI-PrEP cascade (right)
    # -----------------------------
    lai_text_kw = dict(ha="center", va="center", fontsize=7.8, color="white", fontweight="bold")

    lai_bubbles = [
        Bubble(
            angle_deg=130,  # Far away from willingness
            radius=0.55,
            face="#6d28d9",
            edge="#4c1d95",
            lw=2,
            text="1. Awareness\n\n100%\n\nLAI-PrEP exists",
            text_kwargs=dict(**lai_text_kw),
        ),
        Bubble(
            angle_deg=75,   # Willingness
            radius=0.55,
            face="#8b5cf6",
            edge="#6d28d9",
            lw=2,
            text="2. Willingness\n\n95%\n\n67% prefer",
            text_kwargs=dict(**lai_text_kw),
        ),
        Bubble(
            angle_deg=25,   # Eligibility (Distance from willingness)
            radius=0.55,
            face="#5b5bd6",
            edge="#3730a3",
            lw=2,
            text="3. Eligibility\n\n90%\n\nMeets criteria",
            text_kwargs=dict(**lai_text_kw),
        ),
        Bubble(
            angle_deg=-25,  # Prescription (Distance from eligibility)
            radius=0.55,
            face="#3b82f6",
            edge="#1d4ed8",
            lw=2,
            text="4.\nPrescription\n\n85%\n\nProvider Rx",
            text_kwargs=dict(**lai_text_kw),
        ),
        Bubble(
            angle_deg=-75,  # Injection (Distance from prescription)
            radius=0.55,
            face="#34a0a4",
            edge="#0f766e",
            lw=2,
            text="6. Injection\n\n45%\n\nFirst dose",
            text_kwargs=dict(**lai_text_kw),
        ),
        Bubble(
            angle_deg=-115, # Persistence (Standard distance)
            radius=0.55,
            face="#2f9e8f",
            edge="#0f766e",
            lw=2,
            text="7.\nPersistence\n\n37%\n\n81\u201383% of those\nwho initiate",
            text_kwargs=dict(ha="center", va="center", fontsize=7.0, color="white", fontweight="bold"),
        ),
        Bubble(
            angle_deg=-155, # Retention
            radius=0.55,
            face="#2c7fb8",
            edge="#1d4ed8",
            lw=2,
            text="8. Retention\n\n37%\n\nContinued care",
            text_kwargs=dict(**lai_text_kw),
        ),
        Bubble(
            angle_deg=210,  # BRIDGE (Separate, significant metric)
            radius=0.55,
            face="#3b82f6",
            edge="#1d4ed8",
            lw=2,
            text="5. BRIDGE\n\n52.9%\n\nNavigate 2\u20138 wks",
            text_kwargs=dict(ha="center", va="center", fontsize=7.0, color="white", fontweight="bold"),
        ),
    ]

    lai_callouts = [
        Callout(
            anchor_angle_deg=210,
            text="Lead-in Period",
            width=1.45,
            height=0.50,
            face="#f8fafc",
            edge="#94a3b8",
            lw=1.5,
            text_color="#0f172a",
            dx=-0.35,
            dy=0.35,
        ),
        Callout(
            anchor_angle_deg=25,
            text="HIV Testing\nRequirements",
            width=1.70,
            height=0.58,
            face="#fff5f5",
            edge="#dc2626",
            lw=1.8,
            text_color="#991b1b",
            dx=0.35,
            dy=0.35,
        ),
        Callout(
            anchor_angle_deg=-25,
            text="Appointment\nScheduling",
            width=1.65,
            height=0.58,
            face="#fff5f5",
            edge="#dc2626",
            lw=1.8,
            text_color="#991b1b",
            dx=0.35,
            dy=0.05,
        ),
        Callout(
            anchor_angle_deg=-75,
            text="Insurance\nAuthorization",
            width=1.70,
            height=0.58,
            face="#fff5f5",
            edge="#dc2626",
            lw=1.8,
            text_color="#991b1b",
            dx=0.35,
            dy=-0.15,
        ),
    ]

    draw_cascade(
        ax,
        center=right_center,
        ring_radius=ring_radius,
        ring_radii_dotted=(dotted_r1, dotted_r2),
        central_radius=1.10,
        central_face="#b8322a",
        central_edge="#7f1d1d",
        central_text="BRIDGE\nNAVIGATION\n\n2\u20138 Weeks\n\n47.1% Lost",
        outer_bubbles=lai_bubbles,
        callouts=lai_callouts,
    )

    # Bottom subtle divider (optional, matches screenshot feel)
    ax.plot([0.5, FIG_W_IN - 0.5], [0.35, 0.35], color="#e2e8f0", lw=1)

    out_dir = "/Users/acdmbpmax/PycharmProjects/lai-prep-bridge-tool/SCR/figures"
    os.makedirs(out_dir, exist_ok=True)
    out_base = os.path.join(out_dir, "figure1_cascades_fixed")
    fig.savefig(out_base + ".png", dpi=DPI, bbox_inches="tight")
    fig.savefig(out_base + ".pdf", bbox_inches="tight")
    fig.savefig(out_base + ".svg", bbox_inches="tight")
    plt.close(fig)


if __name__ == "__main__":
    main()
