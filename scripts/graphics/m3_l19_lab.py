#!/usr/bin/env python3
"""Generate the L19 (Beam Steering Lab) deck figures as inline SVG.

  - L19-bench-setup     : the bench geometry, array + protractor arc + HB100
  - L19-sweep-compare   : two beam-sweep traces, source at 0 deg and at +30 deg
  - L19-phase-ramp      : commanded ramp, wrapped values, quantized values
  - L19-error-budget    : the four error sources sized in degrees

Exported with live <text> (svg.fonttype='none'), font-family rewritten to
'inherit' so the injected figure picks up the deck font. Transparent
background, USAFA palette, no baked formulas -- the math lives in the slide
text, per COURSE_SPEC.md section 3.

    python3 scripts/graphics/m3_l19_lab.py
    -> writes book/extras/slides/fig/L19-*.svg

Array parameters are the PHASER's: N = 8, d = 14 mm, HB100 at 10.525 GHz.
"""

from __future__ import annotations

import io
import re
from pathlib import Path

import numpy as np
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

NAVY, BLUE, RED, GREEN, ORANGE, GRAY = (
    "#004a85",
    "#0067b9",
    "#b01e24",
    "#1d7a4d",
    "#e67e22",
    "#5a5a5a",
)
INK, RULE = "#1a1a1a", "#c7d2e0"
OUT = Path(__file__).resolve().parents[2] / "book/extras/slides/fig"
VIZ = Path(__file__).resolve().parents[2] / "book/extras/viz/img"
# figures the lesson page embeds as well as the deck
PAGE_FIGS = {"L19-sweep-compare", "L19-error-budget"}

C = 3e8
N = 8
D = 0.014
FREQ = 10.525e9
LAM = C / FREQ
LSB = 2.8125  # ADAR1000 phase LSB, degrees (= sweep grid step)

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
    s = re.sub(r"font-family:[^;}]*", "font-family:inherit", s)
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / f"{name}.svg").write_text(s, encoding="utf-8")
    print(f"wrote {OUT / (name + '.svg')}")
    if name in PAGE_FIGS:
        VIZ.mkdir(parents=True, exist_ok=True)
        (VIZ / f"{name}.svg").write_text(s, encoding="utf-8")
        print(f"wrote {VIZ / (name + '.svg')}")


def af_db(steer_deg: np.ndarray, source_deg: float) -> np.ndarray:
    """Beam-sweep trace: received power vs commanded steer angle, with the
    source fixed at source_deg. By reciprocity this is the array factor
    evaluated at (sin(source) - sin(steer)), plus the cos(theta) projected-
    aperture scan loss on the steered peak."""
    k = 2 * np.pi / LAM
    psi = k * D * (np.sin(np.radians(source_deg)) - np.sin(np.radians(steer_deg)))
    num = np.sin(N * psi / 2)
    den = N * np.sin(psi / 2)
    af = np.where(np.abs(den) < 1e-9, 1.0, num / np.where(np.abs(den) < 1e-9, 1.0, den))
    pw = np.abs(af) ** 2 * np.cos(np.radians(steer_deg))
    return 10 * np.log10(pw + 10 ** (-23.0 / 10))  # sweep noise floor fills the nulls


def bench_setup() -> None:
    """Bench geometry: array at the origin, protractor arc, HB100 at 0 and 30
    degrees. A drawing, not a data plot -- the numbers are on the slide."""
    fig, ax = plt.subplots(figsize=(7.6, 4.0))
    ax.set_aspect("equal")
    ax.axis("off")

    # 8-element array along x, boresight up the +y axis
    for i in range(N):
        x = (i - (N - 1) / 2) * 0.062
        ax.add_patch(plt.Rectangle((x - 0.021, -0.045), 0.042, 0.09,
                                   facecolor=NAVY, edgecolor="none", alpha=0.85))
    ax.plot([-0.30, 0.30], [-0.075, -0.075], color=NAVY, lw=2.2)
    ax.text(0, -0.135, "8-element array (d = 14 mm)", ha="center", va="top",
            fontsize=12.5, color=INK)

    # protractor arc
    R = 1.0
    a = np.radians(np.linspace(-62, 62, 400))
    ax.plot(R * np.sin(a), R * np.cos(a), color=GRAY, lw=1.4, ls=(0, (6, 4)))
    for t in range(-60, 61, 15):
        ar = np.radians(t)
        ax.plot([0.965 * R * np.sin(ar), R * np.sin(ar)],
                [0.965 * R * np.cos(ar), R * np.cos(ar)], color=GRAY, lw=1.2)
        ax.text(1.10 * R * np.sin(ar), 1.10 * R * np.cos(ar), f"{t}",
                ha="center", va="center", fontsize=10.5, color=GRAY)

    # boresight ray + source position 1
    ax.plot([0, 0], [0, R], color=GRAY, lw=1.2, ls=(0, (2, 3)))
    ax.plot(0, R, marker="v", ms=13, color=GREEN)
    ax.text(0, R + 0.15, "HB100 at boresight", ha="center", va="bottom",
            fontsize=12, color=GREEN)

    # steered ray + source position 2
    a30 = np.radians(30)
    ax.plot([0, R * np.sin(a30)], [0, R * np.cos(a30)], color=ORANGE, lw=1.8)
    ax.plot(R * np.sin(a30), R * np.cos(a30), marker="v", ms=13, color=ORANGE)
    ax.plot([R * np.sin(a30) + 0.05, 1.24], [R * np.cos(a30), R * np.cos(a30)],
            color=ORANGE, lw=1.0)
    ax.text(1.28, R * np.cos(a30), "HB100 moved to +30", ha="left", va="center",
            fontsize=12, color=ORANGE)

    # range label
    ax.text(0.11, 0.46, "1 m", ha="right", va="center", fontsize=12, color=INK)
    ax.set_xlim(-1.20, 2.05)
    ax.set_ylim(-0.30, 1.34)
    finalize(fig, "L19-bench-setup")


def sweep_compare() -> None:
    """The measurement: the same beam, traced twice, with the source moved."""
    fine = np.linspace(-60, 60, 4001)
    grid = np.arange(-60, 60 + LSB / 2, LSB)

    fig, ax = plt.subplots(figsize=(8.0, 4.2))
    for src, col, lab in ((0.0, NAVY, "source at 0"), (30.0, ORANGE, "source at +30")):
        ax.plot(fine, af_db(fine, src), color=col, lw=2.0, label=lab)
        ax.plot(grid, af_db(grid, src), ls="none", marker="o", ms=3.4,
                color=col, alpha=0.85)

    ax.axhline(-23, color=GRAY, lw=1.1, ls=(0, (5, 4)))
    ax.text(-58, -24.2, "sweep noise floor", fontsize=11, color=GRAY, va="top")
    ax.axhline(-3, color=GREEN, lw=1.1, ls=(0, (3, 3)))
    ax.text(58, -2.6, "-3 dB", fontsize=11, color=GREEN, va="bottom", ha="right")

    ax.set_xlim(-60, 60)
    ax.set_ylim(-30, 3)
    ax.set_xticks(range(-60, 61, 15))
    ax.set_xlabel("commanded steer angle (deg)")
    ax.set_ylabel("array gain (dB, rel. broadside peak)")
    ax.grid(color=RULE, lw=0.8)
    ax.set_axisbelow(True)
    ax.legend(loc="lower center", bbox_to_anchor=(0.5, -0.42), ncol=2, fontsize=12)
    finalize(fig, "L19-sweep-compare")


def phase_ramp() -> None:
    """What the GUI applies: the ramp, wrapped into 0-360, then onto the LSB."""
    dphi = 360 * D / LAM * np.sin(np.radians(30))
    n = np.arange(N)
    raw = n * dphi
    wrapped = raw % 360
    quant = np.round(wrapped / LSB) * LSB

    fig, ax = plt.subplots(figsize=(7.8, 4.0))
    ax.plot(n + 1, raw, color=GRAY, lw=1.6, ls=(0, (5, 4)), marker="o", ms=5,
            label="commanded ramp")
    ax.plot(n + 1, wrapped, color=NAVY, lw=0, marker="o", ms=9,
            label="wrapped into 0-360")
    ax.plot(n + 1, quant, color=RED, lw=0, marker="x", ms=9, mew=2.0,
            label="on the 2.8125 deg grid")
    for i in range(N):
        if raw[i] > 360:
            ax.annotate("", xy=(i + 1, wrapped[i] + 12), xytext=(i + 1, raw[i] - 12),
                        arrowprops=dict(arrowstyle="->", color=BLUE, lw=1.3))
    ax.axhline(360, color=ORANGE, lw=1.3, ls=(0, (5, 4)))
    ax.text(0.75, 372, "wrap here", fontsize=11.5, color=ORANGE, va="bottom", ha="left")
    ax.set_xlim(0.5, 8.6)
    ax.set_ylim(-40, 680)
    ax.set_xticks(range(1, 9))
    ax.set_yticks(range(0, 721, 120))
    ax.set_xlabel("element number")
    ax.set_ylabel("phase (deg)")
    ax.grid(color=RULE, lw=0.8, axis="y")
    ax.set_axisbelow(True)
    ax.legend(loc="upper left", fontsize=11.5)
    finalize(fig, "L19-phase-ramp")


def error_budget() -> None:
    """The four error sources, sized as a peak-angle error in degrees."""
    labels = [
        "multipath in the room",
        "HB100 drift (200 MHz, at 45)",
        "protractor / aim",
        "sweep grid (half a step)",
    ]
    lo = [0.0, 0.0, 0.0, 0.0]
    hi = [1.0, 1.15, 1.5, 1.41]
    cols = [GRAY, ORANGE, BLUE, NAVY]
    fig, ax = plt.subplots(figsize=(7.6, 3.4))
    y = np.arange(len(labels))
    ax.barh(y, hi, left=lo, height=0.52, color=cols, alpha=0.9)
    for i, h in enumerate(hi):
        ax.text(h + 0.06, y[i], f"{h:.2f}", va="center", fontsize=12, color=INK)
    ax.set_yticks(y)
    ax.set_yticklabels(labels, fontsize=12.5)
    ax.set_xlim(0, 2.0)
    ax.set_xlabel("peak-angle error contributed (deg)")
    ax.grid(color=RULE, lw=0.8, axis="x")
    ax.set_axisbelow(True)
    finalize(fig, "L19-error-budget")


def main() -> int:
    bench_setup()
    sweep_compare()
    phase_ramp()
    error_budget()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
