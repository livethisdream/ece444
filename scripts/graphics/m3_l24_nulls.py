#!/usr/bin/env python3
"""Generate the L24 (null steering) lesson-page figures as inline SVG.

  - L24-jammer-sidelobe   : uniform N=8 pattern, target at broadside, jammer
                            arriving through the first sidelobe at +22.5 deg
  - L24-pattern-null      : uniform (thin) vs null-steered (bold), notch marked
  - L24-cost-vs-angle     : |r| and main-lobe loss vs null angle
  - L24-quant-depth       : exact vs ADAR1000-rounded weights, the RMS fill
                            estimate, and the depth phaser-00 measured

Array is the PHASER's: N = 8, d = 14 mm, 10.525 GHz -> d/lambda = 0.491.
The figures carry no equations (house rule); numbers and short words only.

    python3 scripts/graphics/m3_l24_nulls.py
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
DL = 0.491                      # d / lambda at 10.525 GHz
KD = 2 * np.pi * DL
FLOOR = -50.0                   # plot floor, dB
MEASURED = (-50.0, -46.0)       # phaser-00 notch bottom, dB below uniform peak (2026-10-23)
NIDX = np.arange(N)

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
    """Weight vector that points the beam at theta (conjugate steering vector)."""
    return np.exp(-1j * NIDX * KD * np.sin(np.deg2rad(theta_deg)))


def null_weights(theta1_deg: float, theta0_deg: float = 0.0):
    wd = steer(theta0_deg)
    wn = steer(theta1_deg)
    r = np.vdot(wn, wd) / np.vdot(wn, wn)
    w = wd - r * wn
    return w, r


def response(w: np.ndarray, theta_deg: np.ndarray) -> np.ndarray:
    A = np.exp(1j * np.outer(np.sin(np.deg2rad(theta_deg)), NIDX) * KD)
    return np.abs(A @ w)


def resp_at(w: np.ndarray, theta_deg: float) -> float:
    return float(np.abs(np.exp(1j * np.sin(np.deg2rad(theta_deg)) * NIDX * KD) @ w))


def db_pattern(w: np.ndarray, theta_deg: np.ndarray, ref: float) -> np.ndarray:
    return 20 * np.log10(np.clip(response(w, theta_deg) / ref, 1e-9, None))


def quantize(w: np.ndarray, phase_lsb: float = 2.8125, gain_step: float = 0.01) -> np.ndarray:
    a = np.abs(w) / np.abs(w).max()
    aq = np.round(a / gain_step) * gain_step
    pq = np.deg2rad(np.round(np.rad2deg(np.angle(w)) / phase_lsb) * phase_lsb)
    return aq * np.exp(1j * pq)


TH = np.linspace(-90, 90, 4001)
UNIF = steer(0.0)
PK = response(UNIF, TH).max()          # = N


def _axes(ax, ymin=FLOOR):
    ax.set_xlim(-90, 90)
    ax.set_ylim(ymin, 4)
    ax.set_xticks(range(-90, 91, 30))
    ax.set_xlabel("angle from broadside (deg)")
    ax.set_ylabel("relative response (dB)")
    ax.grid(color=RULE, linewidth=0.8)


# ------------------------------------------------------------------ figure 1
def jammer_sidelobe() -> None:
    """Uniform pattern: the target owns the main lobe, the jammer owns a sidelobe."""
    fig, ax = plt.subplots(figsize=(8.4, 3.9))
    ax.plot(TH, db_pattern(UNIF, TH, PK), color=NAVY, lw=2.2)
    _axes(ax, -40)
    ax.annotate("target  0 dB", xy=(0, 0), xytext=(-52, -6),
                arrowprops=dict(arrowstyle="->", color=GREEN, lw=1.6), color=GREEN, fontsize=13)
    ax.annotate("jammer  -13 dB", xy=(22.5, -13.0), xytext=(38, -6),
                arrowprops=dict(arrowstyle="->", color=RED, lw=1.6), color=RED, fontsize=13)
    ax.axhline(-13.0, color=RED, lw=0.9, ls=(0, (4, 4)))
    finalize(fig, "L24-jammer-sidelobe")


# ------------------------------------------------------------------ figure 2
def pattern_null() -> None:
    w, r = null_weights(22.5)
    ws = w / np.abs(w).max()
    p_null = db_pattern(ws, TH, PK)
    fig, ax = plt.subplots(figsize=(8.4, 4.2))
    ax.plot(TH, db_pattern(UNIF, TH, PK), color=GRAY, lw=1.2, label="uniform, broadside")
    ax.plot(TH, p_null, color=NAVY, lw=2.4, label="null steered to +22.5 deg")
    _axes(ax)
    loss = p_null.max()
    ax.annotate("", xy=(22.5, FLOOR + 2), xytext=(22.5, -13),
                arrowprops=dict(arrowstyle="->", color=RED, lw=1.6))
    ax.text(26, -26, "notch at\n+22.5 deg", color=RED, fontsize=12.5)
    ax.annotate(f"main lobe {loss:.1f} dB", xy=(0, loss), xytext=(-86, -9),
                arrowprops=dict(arrowstyle="->", color=ORANGE, lw=1.5), color=ORANGE, fontsize=12.5)
    ax.legend(loc="lower center", fontsize=12, bbox_to_anchor=(0.5, -0.42), ncol=2)
    finalize(fig, "L24-pattern-null")


# ------------------------------------------------------------------ figure 3
def cost_vs_angle() -> None:
    """Loss in the look direction (broadside) as the null is walked in."""
    def look_loss(a: float) -> float:
        w, _ = null_weights(a)
        ws = w / np.abs(w).max()
        return -20 * np.log10(resp_at(ws, 0.0) / PK)

    ang = np.concatenate([np.linspace(-60, -5, 400), np.linspace(5, 60, 400)])
    loss = [look_loss(a) for a in ang]
    fig, ax = plt.subplots(figsize=(8.4, 4.0))
    ax.plot(ang[:400], loss[:400], color=NAVY, lw=2.3)
    ax.plot(ang[400:], loss[400:], color=NAVY, lw=2.3)
    ax.set_xlim(-60, 60)
    ax.set_ylim(0, 9)
    ax.set_xticks(range(-60, 61, 15))
    ax.set_xlabel("null angle (deg from broadside)")
    ax.set_ylabel("loss at the look direction (dB)")
    ax.grid(color=RULE, linewidth=0.8)
    ax.axvspan(-6.6, 6.6, color=RED, alpha=0.10)
    ax.text(0, 8.1, "half-power beam", ha="center", color=RED, fontsize=12)
    for a, dx, txt in ((22.5, 2, "+22.5 deg\n2.0 dB"), (14.7, -14, "first null\nfree"),
                       (45, 2, "45 deg\n0.8 dB")):
        y = look_loss(a)
        ax.plot([a], [y], "o", color=ORANGE, ms=7)
        ax.annotate(txt, xy=(a, y), xytext=(a + dx, y + 0.8), color=ORANGE, fontsize=11.5)
    finalize(fig, "L24-cost-vs-angle")


# ------------------------------------------------------------------ figure 4
def quant_depth() -> None:
    """Depth against the uniform peak: exact, rounded, RMS estimate, measured."""
    w, r = null_weights(22.5)
    ws = w / np.abs(w).max()
    wq = quantize(w)
    th = np.linspace(0, 45, 4001)
    pk = response(ws, TH).max()
    exact = db_pattern(ws, th, PK)
    rounded = db_pattern(wq, th, PK)
    lsb = np.deg2rad(2.8125)
    eps = np.hypot(lsb / np.sqrt(12), 0.01 / np.sqrt(12))
    rms = 20 * np.log10(eps / np.sqrt(N) * pk / PK)
    fig, ax = plt.subplots(figsize=(8.4, 4.0))
    ax.axhspan(*MEASURED, color=ORANGE, alpha=0.22, lw=0)
    ax.text(0.8, MEASURED[1] + 1.3, "measured on phaser-00", color=ORANGE, fontsize=12)
    ax.axhline(rms, color=RED, lw=1.2, ls=(0, (5, 4)))
    ax.text(44.2, rms + 1.3, f"RMS estimate {rms:.0f} dB", color=RED, fontsize=12, ha="right")
    ax.plot(th, rounded, color=NAVY, lw=3.2, label="rounded to the ADAR1000 steps")
    ax.plot(th, exact, color="#9aa3ad", lw=1.3, ls=(0, (4, 2)), label="exact weights")
    ax.set_xlim(0, 45)
    ax.set_ylim(-70, 4)
    ax.set_xlabel("angle from broadside (deg)")
    ax.set_ylabel("dB below the uniform peak")
    ax.grid(color=RULE, linewidth=0.8)
    ax.legend(loc="upper right", fontsize=12)
    finalize(fig, "L24-quant-depth")


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    jammer_sidelobe()
    pattern_null()
    cost_vs_angle()
    quant_depth()


if __name__ == "__main__":
    main()
