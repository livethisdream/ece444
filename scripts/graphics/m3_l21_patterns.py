#!/usr/bin/env python3
"""Generate the L21 (Antenna Pattern) lesson-page figures as inline SVG.

  - L21-patch-element          : ideal and steeper element power patterns over
                                 a ground plane, one hemisphere, HPBW marked
  - L21-measured-vs-predicted  : predicted product pattern against the trace
                                 the L21 Lab sweep is expected to produce

Exported with live <text> (svg.fonttype='none') carrying the shared font
stack. Transparent background, USAFA palette, no equations baked into the
artwork.

    python3 scripts/graphics/m3_l21_patterns.py
    -> writes book/extras/viz/img/L21-{patch-element,measured-vs-predicted}.svg

Illustrative patterns computed from the course array's parameters; the
"measured" trace is a synthesized expectation, not recorded data.
"""

from __future__ import annotations

import io
import re
from pathlib import Path
from svg_font_stack import apply_font_stack

import matplotlib
import numpy as np

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

NAVY, BLUE, RED, GREEN = "#004a85", "#0067b9", "#b01e24", "#1d7a4d"
ORANGE, GRAY, INK, RULE = "#e67e22", "#5a5a5a", "#1a1a1a", "#c7d2e0"
REPO = Path(__file__).resolve().parents[2]
OUT = REPO / "book/extras/viz/img"

# Course array (ADALM-PHASER at the workshop frequency)
N, D_MM, LAM_MM = 8, 14.0, 29.1
DL = D_MM / LAM_MM  # 0.481
FLOOR = -40.0

plt.rcParams.update(
    {
        "svg.fonttype": "none",
        "font.size": 13,
        "axes.edgecolor": "#8a929c",
        "axes.labelcolor": INK,
        "xtick.color": GRAY,
        "ytick.color": GRAY,
        "text.color": INK,
        "axes.linewidth": 1.0,
        "legend.frameon": False,
    }
)


def finalize(fig, name: str) -> None:
    buf = io.StringIO()
    fig.savefig(buf, format="svg", transparent=True, bbox_inches="tight", pad_inches=0.06)
    plt.close(fig)
    s = buf.getvalue()
    s = s[s.index("<svg"):]
    s = apply_font_stack(s)
    (OUT / f"{name}.svg").write_text(s, encoding="utf-8")
    print(f"wrote {OUT / (name + '.svg')}")


def af(theta_deg: np.ndarray, t0_deg: float) -> np.ndarray:
    """Normalized uniform array factor, field, peak = 1."""
    psi = 2 * np.pi * DL * (np.sin(np.radians(theta_deg)) - np.sin(np.radians(t0_deg)))
    s = np.sin(psi / 2)
    small = np.abs(s) < 1e-12
    return np.where(small, 1.0, np.sin(N * psi / 2) / (N * np.where(small, 1.0, s)))


# Ideal element: it captures its share of the aperture, so its POWER pattern is
# cos(theta) (the projected-aperture rule) and its field pattern is sqrt(cos).
# A real patch is steeper; the course caveat is power cos^1.3 to cos^1.5.
P_IDEAL, P_PATCH = 1.0, 1.4


def ef(theta_deg: np.ndarray, p: float = P_IDEAL) -> np.ndarray:
    """Element factor as a FIELD pattern for a power pattern cos^p(theta)."""
    c = np.clip(np.cos(np.radians(theta_deg)), 0.0, None)
    return c ** (p / 2.0)


def db(x: np.ndarray) -> np.ndarray:
    return 20 * np.log10(np.clip(np.abs(x), 1e-6, None))


def patch_element() -> None:
    th = np.linspace(-90, 90, 2001)
    ang = np.radians(90 - th)  # 0 deg broadside -> straight up

    def radius(p):
        d = np.clip(db(ef(th, p)), FLOOR, None)
        return (d - FLOOR) / (-FLOOR)

    r_ideal, r_patch = radius(P_IDEAL), radius(P_PATCH)

    fig = plt.figure(figsize=(5.8, 4.0))
    ax = fig.add_subplot(111)
    for ring, lab in [(0.75, "-10"), (0.5, "-20"), (0.25, "-30")]:
        c = np.linspace(0, np.pi, 200)
        ax.plot(ring * np.cos(c), ring * np.sin(c), color=RULE, lw=0.8, zorder=0)
        ax.text(0.02, ring + 0.03, lab, fontsize=10, color=GRAY)
    ax.text(0.02, 1.03, "0 dB", fontsize=10, color=GRAY)
    for a_deg in (-60, -30, 0, 30, 60):
        aa = np.radians(90 - a_deg)
        ax.plot([0, 1.06 * np.cos(aa)], [0, 1.06 * np.sin(aa)], color=RULE, lw=0.8, zorder=0)
        ax.text(1.14 * np.cos(aa), 1.14 * np.sin(aa), f"{a_deg}°", fontsize=11,
                color=GRAY, ha="center", va="center")
    ax.fill(r_ideal * np.cos(ang), r_ideal * np.sin(ang), color=BLUE, alpha=0.10)
    ax.plot(r_ideal * np.cos(ang), r_ideal * np.sin(ang), color=NAVY, lw=2.6,
            label="Ideal element")
    ax.plot(r_patch * np.cos(ang), r_patch * np.sin(ang), color=ORANGE, lw=2.0,
            ls=(0, (6, 4)), label="Real patch, steeper")
    ax.plot([-1.25, 1.25], [0, 0], color=INK, lw=2.4)
    ax.add_patch(plt.Rectangle((-0.16, 0.0), 0.32, 0.045, color=RED, zorder=5))
    ax.text(0, -0.10, "ground plane", fontsize=11.5, color=INK, ha="center", va="top")
    ax.text(0.21, 0.07, "patch", fontsize=11.5, color=RED, ha="left", va="bottom")
    for sgn in (1, -1):
        aa = np.radians(90 - sgn * 60.0)
        ax.plot([0, 0.62 * np.cos(aa)], [0, 0.62 * np.sin(aa)],
                color=GREEN, lw=1.4, ls=(0, (4, 3)))
    ax.plot([0.55, 0.78], [0.32, 0.78], color=GREEN, lw=1.0)
    ax.text(0.81, 0.80, "120° half-power\nbeamwidth, ideal",
            fontsize=11.5, color=GREEN, ha="left", va="center")
    ax.text(0, -0.30, "no radiation into the back hemisphere",
            fontsize=11.5, color=GRAY, ha="center", va="top")
    ax.legend(loc="lower center", fontsize=11.5, ncol=2, bbox_to_anchor=(0.5, -0.06))
    ax.set_xlim(-1.55, 1.80)
    ax.set_ylim(-0.62, 1.30)
    ax.set_aspect("equal")
    ax.axis("off")
    finalize(fig, "L21-patch-element")


def measured_vs_predicted() -> None:
    th = np.linspace(-90, 90, 6001)
    pred = db(ef(th, P_IDEAL) * af(th, 30.0))
    grid = np.arange(-90, 90.001, 2.8125)
    skew = 1.8  # hand-set rotation offset, deg
    p = (ef(grid - skew, P_PATCH) * af(grid - skew, 30.0)) ** 2
    rng = np.random.default_rng(7)
    noise = 10 ** (-23 / 10) * (0.55 + 0.9 * rng.random(grid.size))
    meas = 10 * np.log10(p + noise)

    fig, ax = plt.subplots(figsize=(8.2, 4.3))
    ax.axhline(-23, color=RED, lw=1.2, ls=(0, (3, 3)))
    ax.plot(th, pred, color=NAVY, lw=2.2, label="Predicted, element × array")
    ax.plot(grid, meas, color=ORANGE, lw=1.8, marker="o", ms=3.2,
            label="Expected measured sweep")
    ax.set_xlim(-90, 90)
    ax.set_ylim(-34, 3)
    ax.set_xticks(range(-90, 91, 30))
    ax.set_yticks([0, -10, -20, -30])
    ax.grid(color=RULE, lw=0.7)
    ax.set_xlabel("Angle from broadside (deg)")
    ax.set_ylabel("Relative power (dB)")
    ax.legend(loc="lower center", bbox_to_anchor=(0.5, -0.42), ncol=2, fontsize=12)
    ax.annotate("main lobe and first sidelobes agree", xy=(30, -6), xytext=(-50, 1.2),
                fontsize=11.5, color=NAVY,
                arrowprops=dict(arrowstyle="->", color=NAVY, lw=1.1))
    ax.annotate("sweep noise floor", xy=(76, -23.4), xytext=(46, -30.5),
                fontsize=11.5, color=RED,
                arrowprops=dict(arrowstyle="->", color=RED, lw=1.1))
    finalize(fig, "L21-measured-vs-predicted")


if __name__ == "__main__":
    OUT.mkdir(parents=True, exist_ok=True)
    patch_element()
    measured_vs_predicted()
