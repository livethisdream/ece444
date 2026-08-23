#!/usr/bin/env python3
"""Generate the L27 (null steering) deck/page figures as inline SVG.

  - L27-jammer-sidelobe   : uniform N=8 pattern, target at broadside, jammer
                            arriving through the first sidelobe at +22.5 deg
  - L27-weight-phasors    : per-element phasor construction w = 1 - r*wn
  - L27-pattern-null      : uniform (thin) vs null-steered (bold), notch marked
  - L27-cost-vs-angle     : |r| and main-lobe loss vs null angle
  - L27-quant-depth       : ideal vs quantized weights against the sweep floor

Array is the PHASER's: N = 8, d = 14 mm, 10.525 GHz -> d/lambda = 0.491.
Deck figures carry no equations (house rule); numbers and short words only.

    python3 scripts/graphics/m3_l27_nulls.py
    -> book/extras/slides/fig/L27-*.svg  (+ two copies in book/extras/viz/img/)
"""

from __future__ import annotations
import io
import re
from pathlib import Path

import numpy as np
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

NAVY, BLUE, RED, GREEN, ORANGE, GREY = "#004a85", "#0067b9", "#b01e24", "#1d7a4d", "#e67e22", "#5a5a5a"
INK, RULE = "#1a1a1a", "#c7d2e0"
ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "book/extras/slides/fig"
OUT_PAGE = ROOT / "book/extras/viz/img"

N = 8
DL = 0.491                      # d / lambda at 10.525 GHz
KD = 2 * np.pi * DL
FLOOR = -50.0                   # plot floor, dB
SWEEP_FLOOR = -23.0             # measured sweep noise floor, dB below uniform peak
NIDX = np.arange(N)

plt.rcParams.update({
    "svg.fonttype": "none",
    "font.size": 13,
    "axes.edgecolor": "#8a929c",
    "axes.labelcolor": INK,
    "xtick.color": GREY, "ytick.color": GREY,
    "text.color": INK,
    "axes.linewidth": 1.0,
    "legend.frameon": False,
})


def finalize(fig, name: str, also_page: bool = False) -> None:
    buf = io.StringIO()
    fig.savefig(buf, format="svg", transparent=True, bbox_inches="tight", pad_inches=0.06)
    plt.close(fig)
    s = buf.getvalue()
    s = s[s.index("<svg"):]
    s = re.sub(r"font-family:[^;}]*", "font-family:inherit", s)
    (OUT / f"{name}.svg").write_text(s, encoding="utf-8")
    print(f"wrote {OUT / (name + '.svg')}")
    if also_page:
        OUT_PAGE.mkdir(parents=True, exist_ok=True)
        (OUT_PAGE / f"{name}.svg").write_text(s, encoding="utf-8")
        print(f"wrote {OUT_PAGE / (name + '.svg')}")


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
    finalize(fig, "L27-jammer-sidelobe", also_page=True)


# ------------------------------------------------------------------ figure 2
def weight_phasors() -> None:
    """The weights are 1 minus a rotating vector: their tips ride a circle."""
    fig, axes = plt.subplots(1, 2, figsize=(9.6, 4.6))
    for ax, t1 in zip(axes, (22.5, 7.0)):
        w, r = null_weights(t1)
        ax.set_aspect("equal")
        ax.axis("off")
        ax.set_xlim(-0.35, 1.95)
        ax.set_ylim(-1.05, 1.45)
        ax.plot([-0.3, 1.9], [0, 0], color=RULE, lw=0.9)
        ax.plot([0, 0], [-0.95, 0.95], color=RULE, lw=0.9)
        th = np.linspace(0, 2 * np.pi, 400)
        ax.plot(1 + abs(r) * np.cos(th), abs(r) * np.sin(th), color=RED, lw=1.4, ls=(0, (5, 4)))
        ax.annotate("", xy=(1, 0), xytext=(0, 0),
                    arrowprops=dict(arrowstyle="->", color=GREY, lw=2.0))
        for n in range(N):
            ax.annotate("", xy=(w[n].real, w[n].imag), xytext=(0, 0),
                        arrowprops=dict(arrowstyle="->", color=NAVY, lw=1.7))
            ax.plot([w[n].real], [w[n].imag], "o", color=NAVY, ms=4.5)
        ax.text(1 + abs(r) + 0.07, 0.0, f"radius {abs(r):.2f}", color=RED,
                ha="left", va="center", fontsize=12.5)
        ax.text(0.8, -1.02, f"null at {t1:g} deg", color=INK, ha="center", fontsize=13.5)
    axes[0].annotate("steering weight", xy=(0.88, 0.015), xytext=(0.15, 1.30),
                     arrowprops=dict(arrowstyle="->", color=GREY, lw=1.3),
                     color=GREY, fontsize=12.5)
    axes[1].annotate("eight element weights", xy=(0.72, 0.62), xytext=(0.05, 1.30),
                     arrowprops=dict(arrowstyle="->", color=NAVY, lw=1.3),
                     color=NAVY, fontsize=12.5)
    finalize(fig, "L27-weight-phasors")


# ------------------------------------------------------------------ figure 3
def pattern_null() -> None:
    w, r = null_weights(22.5)
    ws = w / np.abs(w).max()
    p_null = db_pattern(ws, TH, PK)
    fig, ax = plt.subplots(figsize=(8.4, 4.2))
    ax.plot(TH, db_pattern(UNIF, TH, PK), color=GREY, lw=1.2, label="uniform, broadside")
    ax.plot(TH, p_null, color=NAVY, lw=2.4, label="null steered to +22.5 deg")
    _axes(ax)
    loss = p_null.max()
    ax.annotate("", xy=(22.5, FLOOR + 2), xytext=(22.5, -13),
                arrowprops=dict(arrowstyle="->", color=RED, lw=1.6))
    ax.text(26, -26, "notch at\n+22.5 deg", color=RED, fontsize=12.5)
    ax.annotate(f"main lobe {loss:.1f} dB", xy=(0, loss), xytext=(-86, -9),
                arrowprops=dict(arrowstyle="->", color=ORANGE, lw=1.5), color=ORANGE, fontsize=12.5)
    ax.legend(loc="lower center", fontsize=12, bbox_to_anchor=(0.5, -0.42), ncol=2)
    finalize(fig, "L27-pattern-null", also_page=True)


# ------------------------------------------------------------------ figure 4
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
    finalize(fig, "L27-cost-vs-angle", also_page=True)


# ------------------------------------------------------------------ figure 5
def quant_depth() -> None:
    w, r = null_weights(22.5)
    ws = w / np.abs(w).max()
    wq = quantize(w)
    th = np.linspace(0, 45, 4001)
    pk = response(ws, TH).max()
    ideal = 20 * np.log10(np.clip(response(ws, th) / pk, 1e-9, None))
    noise = 10 ** (SWEEP_FLOOR / 10) * PK ** 2 / pk ** 2
    meas = 10 * np.log10(np.clip(response(wq, th) ** 2 / pk ** 2 + noise, 1e-12, None))
    fig, ax = plt.subplots(figsize=(8.4, 4.0))
    ax.plot(th, ideal, color=GREY, lw=1.4, label="exact weights")
    ax.plot(th, meas, color=NAVY, lw=2.4, label="quantized weights, measured sweep")
    ax.axhline(10 * np.log10(noise), color=RED, lw=1.2, ls=(0, (5, 4)))
    ax.text(1.5, 10 * np.log10(noise) + 1.2, "sweep noise floor", color=RED, fontsize=12)
    ax.set_xlim(0, 45)
    ax.set_ylim(-50, 4)
    ax.set_xlabel("angle from broadside (deg)")
    ax.set_ylabel("relative response (dB)")
    ax.grid(color=RULE, linewidth=0.8)
    depth = meas[np.argmin(np.abs(th - 22.5))]
    ax.annotate(f"{-depth:.0f} dB notch", xy=(22.5, depth), xytext=(27, -12),
                arrowprops=dict(arrowstyle="->", color=ORANGE, lw=1.5), color=ORANGE, fontsize=12.5)
    ax.legend(loc="lower left", fontsize=12)
    finalize(fig, "L27-quant-depth", also_page=True)


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    jammer_sidelobe()
    weight_phasors()
    pattern_null()
    cost_vs_angle()
    quant_depth()


if __name__ == "__main__":
    main()
