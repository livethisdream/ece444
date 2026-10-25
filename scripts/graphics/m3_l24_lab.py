#!/usr/bin/env python3
"""Generate the L24 Lab (null steering) lesson-page figures as inline SVG.

  - L24-element-settings : the eight gain percentages and phase offsets that
                           the course example asks students to type into the
                           GUI's Element Gains and Phase Control panels
  - L24-monopulse        : sum and delta together, and the signed error function
                           their ratio produces across boresight

Array is the PHASER's: N = 8, d = 14 mm, worked at 10.443 GHz, the Find HB100
frequency of phaser-00 in the 2026-10-23 dry run (d/lambda = 0.487), with the
two ADAR1000 subarrays (elements 1-4 and 5-8) forming the digital pair. The
expected-sweep figures (L24-sweep-notch, L24-delta-beam) were retired with the
L24 Lab pass: they drew a -21 dB floor the hardware does not have, and the lab
explains the nulls rather than redrawing the bench traces.
The figures carry no equations (house rule); numbers and short words only.

    python3 scripts/graphics/m3_l24_lab.py
    -> book/extras/viz/img/L24-*.svg
"""

from __future__ import annotations

import io
import re
from pathlib import Path

import numpy as np
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from svg_font_stack import apply_font_stack

NAVY, BLUE, RED, GREEN, ORANGE, GRAY = "#004a85", "#0067b9", "#b01e24", "#1d7a4d", "#e67e22", "#5a5a5a"
INK, RULE = "#1a1a1a", "#c7d2e0"
ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "book/extras/viz/img"

N = 8
DL = 0.014 * 10.443e9 / 3.00e8   # d / lambda at phaser-00's 10.443 GHz
KD = 2 * np.pi * DL
NIDX = np.arange(N)
NULL_ANG = 22.5                  # the course example's null direction

plt.rcParams.update({
    "svg.fonttype": "none",
    "font.size": 13,
    "axes.edgecolor": "#8a929c",
    "axes.labelcolor": INK,
    "xtick.color": GRAY, "ytick.color": GRAY,
    "text.color": INK,
    "axes.linewidth": 1.0,
    "legend.frameon": False,
})


def finalize(fig, name: str) -> None:
    buf = io.StringIO()
    fig.savefig(buf, format="svg", transparent=True, bbox_inches="tight", pad_inches=0.06)
    plt.close(fig)
    s = buf.getvalue()
    s = s[s.index("<svg"):]
    s = apply_font_stack(s)
    (OUT / f"{name}.svg").write_text(s, encoding="utf-8")
    print(f"wrote {OUT / (name + '.svg')}")


# ---------------------------------------------------------------- array maths
def steer(theta_deg: float) -> np.ndarray:
    return np.exp(-1j * NIDX * KD * np.sin(np.deg2rad(theta_deg)))


def null_weights(theta1_deg: float, theta0_deg: float = 0.0):
    wd, wn = steer(theta0_deg), steer(theta1_deg)
    r = np.vdot(wn, wd) / np.vdot(wn, wn)
    return wd - r * wn, r


def response(w: np.ndarray, theta_deg) -> np.ndarray:
    A = np.exp(1j * np.outer(np.sin(np.deg2rad(np.atleast_1d(theta_deg))), NIDX) * KD)
    return np.abs(A @ w)


# ------------------------------------------------------------------ figure 1
def element_settings() -> None:
    """What the student types into Element Gains and Phase Control."""
    w, _ = null_weights(NULL_ANG)
    g = 100 * np.abs(w) / np.abs(w).max()
    p = np.rad2deg(np.angle(w))
    el = np.arange(1, N + 1)

    fig, (a1, a2) = plt.subplots(2, 1, figsize=(4.8, 5.4))
    a1.bar(el, g, width=0.62, color=NAVY)
    for x, y in zip(el, g):
        a1.text(x, y + 3, f"{y:.0f}", ha="center", va="bottom", fontsize=11, color=INK)
    a1.set_ylim(0, 118)
    a1.set_xticks(el)
    a1.set_xlabel("element")
    a1.set_ylabel("element gain (%)")
    a1.grid(axis="y", color=RULE, linewidth=0.8)
    a1.set_axisbelow(True)

    a2.axhline(0, color="#8a929c", linewidth=1.0)
    a2.vlines(el, 0, p, color=ORANGE, linewidth=2.4)
    a2.plot(el, p, "o", color=ORANGE, markersize=6)
    for x, y in zip(el, p):
        off = 2.2 if y >= 0 else -2.2
        a2.text(x, y + off, f"{y:+.1f}", ha="center",
                va="bottom" if y >= 0 else "top", fontsize=10.5, color=INK)
    a2.set_ylim(-21, 21)
    a2.set_xticks(el)
    a2.set_xlabel("element")
    a2.set_ylabel("phase offset (deg)")
    a2.grid(axis="y", color=RULE, linewidth=0.8)
    a2.set_axisbelow(True)

    fig.tight_layout()
    finalize(fig, "L24-element-settings")


# ------------------------------------------------------------------ figure 4
def monopulse() -> None:
    """Sum and delta together, and the error function their ratio produces."""
    th = np.linspace(-20, 20, 4001)
    A = np.exp(1j * np.outer(np.sin(np.deg2rad(th)), NIDX) * KD)
    sig = A @ np.ones(N)
    dlt = A @ np.r_[np.ones(4), -np.ones(4)]
    ps = 20 * np.log10(np.maximum(np.abs(sig), 1e-9) / N)
    pd = 20 * np.log10(np.maximum(np.abs(dlt), 1e-9) / N)

    # the two subarrays are displaced, so delta sits in quadrature with sum:
    # the error signal is Im(delta * conj(sum)) / |sum|^2
    err = -np.imag(dlt * np.conj(sig)) / np.abs(sig) ** 2

    fig, (a1, a2) = plt.subplots(2, 1, figsize=(4.8, 5.6))

    a1.set_xlim(-20, 20)
    a1.set_ylim(-40, 3)
    a1.set_xticks(range(-20, 21, 10))
    a1.set_xlabel("angle from broadside (deg)")
    a1.set_ylabel("channel level (dB)")
    a1.grid(color=RULE, linewidth=0.8)
    a1.plot(th, ps, color=GRAY, linewidth=1.6, label="sum")
    a1.plot(th, pd, color=NAVY, linewidth=2.6, label="delta")
    a1.annotate("delta: exact zero\non boresight", xy=(0.3, -38), xytext=(4.0, -36),
                fontsize=11.5, color=RED, va="bottom",
                arrowprops=dict(arrowstyle="->", color=RED, linewidth=1.2))
    a1.annotate("sum is flat here", xy=(0.5, -0.2), xytext=(2.0, -23.0),
                fontsize=11.5, color=GRAY,
                arrowprops=dict(arrowstyle="->", color=GRAY, linewidth=1.2))
    a1.legend(loc="lower left", fontsize=11.5, bbox_to_anchor=(0.2, 0.0))   # between the sum null and the delta zero

    win = np.abs(th) <= 12
    a2.set_xlim(-12, 12)
    a2.set_ylim(-2.2, 2.2)
    a2.set_xticks(range(-12, 13, 4))
    a2.set_xlabel("angle from broadside (deg)")
    a2.set_ylabel("error function")
    a2.grid(color=RULE, linewidth=0.8)
    a2.axhline(0, color="#8a929c", linewidth=1.0)
    a2.axvline(0, color="#8a929c", linewidth=1.0)
    lin = np.abs(th) <= 5
    a2.plot(th[win], err[win], color=NAVY, linewidth=2.6)
    a2.plot(th[lin], err[lin], color=GREEN, linewidth=3.4)
    a2.text(-11.4, 1.82, "slope 0.11 per degree", fontsize=11.5, color=INK)
    a2.annotate("straight within +/-5 deg",
                xy=(-3.6, err[np.argmin(np.abs(th + 3.6))]), xytext=(-11.4, 1.18),
                fontsize=11.5, color=GREEN,
                arrowprops=dict(arrowstyle="->", color=GREEN, linewidth=1.2))
    a2.annotate("zero on boresight", xy=(0.15, 0.02), xytext=(2.2, -1.85),
                fontsize=11.5, color=RED,
                arrowprops=dict(arrowstyle="->", color=RED, linewidth=1.2))

    fig.tight_layout()
    finalize(fig, "L24-monopulse")



def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    element_settings()
    monopulse()


if __name__ == "__main__":
    main()
