#!/usr/bin/env python3
"""Generate the L18 (Beam Steering Theory) deck figures as inline SVG.

  - L18-path-difference   : plane wave off broadside, the d sin(theta0) leg
  - L18-phase-ramp        : commanded ramp, unwrapped line vs wrapped bars
  - L18-sin-space         : the same steered pattern vs theta and vs sin(theta)
  - L18-broadening        : projected aperture Nd cos(theta0)
  - L18-steered-patterns  : N=8 array steered to 0/30/45/60 deg (widget fallback)

Deck figures carry no equations: symbols and short words only. Two of them are
copied to book/extras/viz/img/ for the lesson page.

    python3 scripts/graphics/m3_l18_steering.py
"""

from __future__ import annotations

import io
import re
import shutil
from pathlib import Path

import numpy as np
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

NAVY, BLUE, RED, GREEN, AMBER, GREY = "#004a85", "#0067b9", "#b01e24", "#1d7a4d", "#8a5a00", "#5a5a5a"
INK, RULE = "#1a1a1a", "#c7d2e0"

FIG = Path(__file__).resolve().parents[2] / "book/extras/slides/fig"
IMG = Path(__file__).resolve().parents[2] / "book/extras/viz/img"

# Course array at the workshop frequency: d = 14 mm, lambda = 29.1 mm (10.3 GHz).
N, DL = 8, 14.0 / 29.1

plt.rcParams.update(
    {
        "svg.fonttype": "none",
        "font.size": 13,
        "axes.edgecolor": "#8a929c",
        "axes.labelcolor": INK,
        "xtick.color": GREY,
        "ytick.color": GREY,
        "text.color": INK,
        "axes.linewidth": 1.0,
        "legend.frameon": False,
    }
)


def finalize(fig, name: str, also_page: bool = False) -> None:
    buf = io.StringIO()
    fig.savefig(buf, format="svg", transparent=True, bbox_inches="tight", pad_inches=0.06)
    plt.close(fig)
    s = buf.getvalue()
    s = s[s.index("<svg"):]
    s = re.sub(r"font-family:[^;}]*", "font-family:inherit", s)
    (FIG / f"{name}.svg").write_text(s, encoding="utf-8")
    print(f"wrote {FIG / (name + '.svg')}")
    if also_page:
        shutil.copyfile(FIG / f"{name}.svg", IMG / f"{name}.svg")
        print(f"wrote {IMG / (name + '.svg')}")


def af_db(theta_deg: np.ndarray, t0_deg: float, floor: float = -40.0) -> np.ndarray:
    """Uniform N-element array factor, dB, normalized to unity peak."""
    psi = 2 * np.pi * DL * (np.sin(np.radians(theta_deg)) - np.sin(np.radians(t0_deg)))
    num = np.sin(N * psi / 2.0)
    den = N * np.sin(psi / 2.0)
    with np.errstate(divide="ignore", invalid="ignore"):
        f = np.where(np.abs(den) < 1e-12, 1.0, num / den)
    db = 20 * np.log10(np.clip(np.abs(f), 1e-9, None))
    return np.clip(db, floor, 0.0)


# --------------------------------------------------------------------------- 1
def path_difference() -> None:
    """Two adjacent elements, a wave arriving theta0 off broadside, and the
    extra leg the wavefront still has to travel to reach the nearer element."""
    t0 = np.radians(35.0)
    u = np.array([np.sin(t0), np.cos(t0)])          # toward the source
    v = np.array([np.cos(t0), -np.sin(t0)])         # along a wavefront

    fig, ax = plt.subplots(figsize=(7.9, 4.0))
    ax.set_aspect("equal")
    ax.axis("off")

    xs = np.arange(N) * 1.0
    ax.plot([-0.6, N - 0.4], [0, 0], color=GREY, lw=1.2, zorder=1)
    for i, x in enumerate(xs):
        ax.add_patch(plt.Rectangle((x - 0.16, -0.12), 0.32, 0.24,
                                   facecolor="white", edgecolor=NAVY, lw=1.6, zorder=3))
    # wavefronts through the adjacent pair under discussion, drawn above the
    # array only (the half below it is geometry the reader does not need)
    a, b = xs[4], xs[5]
    for x0, style, reach in ((b, "-", 2.9), (a, "--", 1.5)):
        p = np.array([x0, 0.0])
        seg = np.array([p - reach * v, p + 0.12 * v])
        ax.plot(seg[:, 0], seg[:, 1], color=BLUE, lw=1.5, ls=style, zorder=2)

    # incoming propagation arrows, off to the right of the geometry
    for s in (0.6, 1.75, 2.9):
        start = np.array([b, 0.0]) + s * v + 3.1 * u
        ax.annotate("", xy=start - 1.15 * u, xytext=start,
                    arrowprops=dict(arrowstyle="-|>", color=BLUE, lw=1.4, alpha=0.8))
    tip = np.array([b, 0.0]) + 3.0 * v + 3.2 * u
    ax.text(tip[0] + 0.2, tip[1], "incoming wave", color=BLUE,
            fontsize=12, ha="left", va="center")

    # the extra leg: from element a, perpendicular foot on the wavefront through b
    p_a = np.array([a, 0.0])
    foot = p_a + ((np.array([b, 0.0]) - p_a) @ u) * u
    ax.plot([p_a[0], foot[0]], [p_a[1], foot[1]], color=RED, lw=2.6, zorder=5)
    ax.plot([p_a[0], b], [0, 0], color=NAVY, lw=2.6, zorder=4)
    m = 0.13
    ax.plot([foot[0] - m * (u[0] + v[0]), foot[0] - m * u[0], foot[0] - m * (u[0] - v[0])],
            [foot[1] - m * (u[1] + v[1]), foot[1] - m * u[1], foot[1] - m * (u[1] - v[1])],
            color=INK, lw=0.9, zorder=5)
    mid = (p_a + foot) / 2
    ax.annotate("extra path", xy=(mid[0] - 0.06, mid[1] + 0.04),
                xytext=(mid[0] - 1.85, mid[1] + 1.35),
                color=RED, fontsize=12.5, ha="center",
                arrowprops=dict(arrowstyle="-", color=RED, lw=1.0))
    ax.text((a + b) / 2, -0.34, "d", color=NAVY, fontsize=14, ha="center", va="top", style="italic")

    # broadside reference and the scan angle
    ax.plot([b, b], [0, 2.6], color=GREY, lw=1.1, ls=":", zorder=2)
    ax.text(b, 2.68, "broadside", color=GREY, fontsize=11.5, ha="center", va="bottom")
    arc = np.linspace(0, t0, 60)
    r = 1.5
    ax.plot(b + r * np.sin(arc), r * np.cos(arc), color=INK, lw=1.1)
    ax.text(b + (r + 0.3) * np.sin(t0 / 2), (r + 0.3) * np.cos(t0 / 2),
            r"$\theta_0$", color=INK, fontsize=15, ha="center", va="center")
    ax.plot([b, b + 2.6 * u[0]], [0, 2.6 * u[1]], color=INK, lw=1.2)

    for i, x in enumerate(xs):
        ax.text(x, -0.5, f"{i}", color=GREY, fontsize=11, ha="center", va="top")
    ax.text(-0.6, -0.95, "element number", color=GREY, fontsize=11.5, ha="left", va="top")

    ax.set_xlim(-1.2, N + 2.6)
    ax.set_ylim(-1.3, 3.5)
    finalize(fig, "L18-path-difference", also_page=True)


# --------------------------------------------------------------------------- 2
def phase_ramp() -> None:
    """Commanded phases for theta0 = 30 deg: the straight unwrapped ramp and
    the sawtooth the hardware is actually given."""
    dphi = 360.0 * DL * np.sin(np.radians(30.0))
    n = np.arange(N)
    unwrapped = -n * dphi
    wrapped = unwrapped % 360.0

    fig, axes = plt.subplots(1, 2, figsize=(8.6, 3.7))
    ax = axes[0]
    ax.plot(n, unwrapped, color=NAVY, lw=2.0, marker="o", ms=6, zorder=3)
    ax.axhline(0, color=RULE, lw=1.0)
    for k in range(-1, -3, -1):
        ax.axhline(360 * k, color=RULE, lw=1.0, ls="--")
    ax.set_title("commanded ramp", color=INK, fontsize=13.5, pad=8)
    ax.set_xlabel("element number")
    ax.set_ylabel("phase (deg)")
    ax.set_ylim(-680, 80)
    ax.set_xticks(n)

    ax = axes[1]
    ax.bar(n, wrapped, width=0.62, color=BLUE, edgecolor=NAVY, lw=1.0, zorder=3)
    ax.axhline(360, color=RULE, lw=1.0, ls="--")
    ax.set_title("what the hardware is given", color=INK, fontsize=13.5, pad=8)
    ax.set_xlabel("element number")
    ax.set_ylabel("phase (deg)")
    ax.set_ylim(0, 400)
    ax.set_yticks([0, 90, 180, 270, 360])
    ax.set_xticks(n)
    for a in axes:
        a.spines["top"].set_visible(False)
        a.spines["right"].set_visible(False)
    fig.tight_layout()
    finalize(fig, "L18-phase-ramp")


# --------------------------------------------------------------------------- 3
def sin_space() -> None:
    """The steered pattern is a rigid shift in sin(theta), not in theta."""
    th = np.linspace(-90, 90, 4001)
    fig, axes = plt.subplots(1, 2, figsize=(8.8, 3.8))

    ax = axes[0]
    ax.plot(th, af_db(th, 0.0), color=GREY, lw=1.6)
    ax.plot(th, af_db(th, 45.0), color=NAVY, lw=2.0)
    ax.text(-2, 1.2, "broadside", color=GREY, fontsize=11.5, ha="right", va="bottom")
    ax.text(47, 1.2, "steered", color=NAVY, fontsize=11.5, ha="left", va="bottom")
    ax.set_xlim(-90, 90)
    ax.set_xticks([-90, -45, 0, 45, 90])
    ax.set_xlabel("scan angle (deg)")
    ax.set_ylabel("relative power (dB)")
    ax.set_title("versus angle", color=INK, fontsize=13.5, pad=8)

    ax = axes[1]
    s = np.sin(np.radians(th))
    ax.plot(s, af_db(th, 0.0), color=GREY, lw=1.6)
    ax.plot(s, af_db(th, 45.0), color=NAVY, lw=2.0)
    ax.annotate("", xy=(0.707, -6), xytext=(0.0, -6),
                arrowprops=dict(arrowstyle="-|>", color=RED, lw=1.6))
    ax.text(0.35, -4.4, "same shape, shifted", color=RED, fontsize=11.5, ha="center")
    ax.set_xlim(-1, 1)
    ax.set_xticks([-1, -0.5, 0, 0.5, 1])
    ax.set_xlabel("sine of scan angle")
    ax.set_title("versus sine of angle", color=INK, fontsize=13.5, pad=8)

    for a in axes:
        a.set_ylim(-40, 5)
        a.grid(True, color=RULE, lw=0.7, alpha=0.7)
        a.spines["top"].set_visible(False)
        a.spines["right"].set_visible(False)
    fig.tight_layout()
    finalize(fig, "L18-sin-space")


# --------------------------------------------------------------------------- 4
def broadening() -> None:
    """Projected aperture: the array looks shorter from off broadside."""
    t0 = np.radians(40.0)
    u = np.array([np.sin(t0), np.cos(t0)])
    v = np.array([np.cos(t0), -np.sin(t0)])
    L = float(N - 1)

    fig, ax = plt.subplots(figsize=(7.6, 4.4))
    ax.set_aspect("equal")
    ax.axis("off")

    xs = np.arange(N) * 1.0
    ax.plot([-0.5, L + 0.5], [0, 0], color=GREY, lw=1.2)
    for x in xs:
        ax.add_patch(plt.Rectangle((x - 0.16, -0.12), 0.32, 0.24,
                                   facecolor="white", edgecolor=NAVY, lw=1.6, zorder=3))
    ax.annotate("", xy=(L, -0.62), xytext=(0, -0.62),
                arrowprops=dict(arrowstyle="<|-|>", color=NAVY, lw=1.4))
    ax.text(L / 2, -0.95, "array length", color=NAVY, fontsize=12.5, ha="center", va="top")

    # rays toward the source from the two ends
    base = 5.5 * u                                  # foot of the bracket on the left ray
    endp = base + (L * np.cos(t0)) * v              # lands on the right ray
    for p0, tmax in ((np.array([0.0, 0.0]), 6.6), (np.array([L, 0.0]), 3.6)):
        ax.plot([p0[0], p0[0] + tmax * u[0]], [p0[1], p0[1] + tmax * u[1]],
                color=BLUE, lw=1.3, alpha=0.85)
    ax.annotate("", xy=endp, xytext=base,
                arrowprops=dict(arrowstyle="<|-|>", color=RED, lw=2.0))
    mid = (base + endp) / 2
    ax.text(mid[0] + 0.95 * u[0], mid[1] + 0.95 * u[1], "projected length",
            color=RED, fontsize=12.5, ha="center", va="bottom")

    ax.plot([L, L], [0, 3.4], color=GREY, lw=1.1, ls=":")
    ax.text(L, 3.5, "broadside", color=GREY, fontsize=11.5, ha="center", va="bottom")
    arc = np.linspace(0, t0, 60)
    r = 2.0
    ax.plot(L + r * np.sin(arc), r * np.cos(arc), color=INK, lw=1.1)
    ax.text(L + (r + 0.36) * np.sin(t0 / 2), (r + 0.36) * np.cos(t0 / 2),
            r"$\theta_0$", color=INK, fontsize=15, ha="center", va="center")

    ax.set_xlim(-1.0, L + 3.4)
    ax.set_ylim(-1.6, 5.0)
    finalize(fig, "L18-broadening", also_page=True)


# --------------------------------------------------------------------------- 5
def steered_patterns() -> None:
    """Static fallback for the widget: four commanded angles on one axis."""
    th = np.linspace(-90, 90, 6001)
    fig, ax = plt.subplots(figsize=(8.6, 4.1))
    for t0, c, lw in ((0, GREY, 1.6), (30, BLUE, 1.7), (45, NAVY, 1.9), (60, AMBER, 1.9)):
        ax.plot(th, af_db(th, t0), color=c, lw=lw, label=f"{t0}°")
    ax.axhline(-3, color=GREEN, lw=1.0, ls="--")
    ax.text(88, -2.6, "half power", color=GREEN, fontsize=11, ha="right", va="bottom")
    ax.set_xlim(-90, 90)
    ax.set_ylim(-40, 2)
    ax.set_xticks([-90, -60, -30, 0, 30, 60, 90])
    ax.set_xlabel("scan angle (deg)")
    ax.set_ylabel("relative power (dB)")
    ax.grid(True, color=RULE, lw=0.7, alpha=0.7)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.legend(loc="upper left", fontsize=11, title="commanded", title_fontsize=11)
    fig.tight_layout()
    finalize(fig, "L18-steered-patterns")


if __name__ == "__main__":
    FIG.mkdir(parents=True, exist_ok=True)
    IMG.mkdir(parents=True, exist_ok=True)
    path_difference()
    phase_ramp()
    sin_space()
    broadening()
    steered_patterns()
