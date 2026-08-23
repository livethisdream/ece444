#!/usr/bin/env python3
"""Generate the L28 (null steering lab) deck/page figures as inline SVG.

  - L28-element-settings : the eight gain percentages and phase offsets that
                           the course example asks students to type into the
                           GUI's Element Gains and Phase Control panels
  - L28-sweep-notch      : frozen uniform reference vs the null-steered sweep,
                           on the GUI's 2.8125 deg steering grid, with the
                           measurement noise floor that sets the notch reading
  - L28-delta-beam       : two-channel sum vs difference (Beam 1 Phase = 180),
                           boresight null and the twin peaks near +/-11 deg
  - L28-mvdr-vs-manual   : two-channel manual vs MVDR response against an
                           interferer -- the static fallback for the widget
  - L28-monopulse        : sum and delta together, and the signed error function
                           their ratio produces across boresight

Array is the PHASER's: N = 8, d = 14 mm, 10.525 GHz -> d/lambda = 0.491, with
the two ADAR1000 subarrays (elements 1-4 and 5-8) forming the digital pair.
Deck figures carry no equations (house rule); numbers and short words only.

    python3 scripts/graphics/m3_l28_lab.py
    -> book/extras/slides/fig/L28-*.svg  (+ two copies in book/extras/viz/img/)
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
DL = 0.491                       # d / lambda at 10.525 GHz
KD = 2 * np.pi * DL
NIDX = np.arange(N)
STEP = 2.8125                    # GUI sweep step = phase LSB as a steer step
FLOOR_DBC = -21.6                # measured sweep floor that caps the notch read
NULL_ANG = 22.5                  # the course example's null direction

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
    return np.exp(-1j * NIDX * KD * np.sin(np.deg2rad(theta_deg)))


def null_weights(theta1_deg: float, theta0_deg: float = 0.0):
    wd, wn = steer(theta0_deg), steer(theta1_deg)
    r = np.vdot(wn, wd) / np.vdot(wn, wn)
    return wd - r * wn, r


def response(w: np.ndarray, theta_deg) -> np.ndarray:
    A = np.exp(1j * np.outer(np.sin(np.deg2rad(np.atleast_1d(theta_deg))), NIDX) * KD)
    return np.abs(A @ w)


def quantize(w: np.ndarray, phase_lsb: float = 2.8125, gain_step: float = 0.01) -> np.ndarray:
    a = np.abs(w) / np.abs(w).max()
    aq = np.round(a / gain_step) * gain_step
    pq = np.deg2rad(np.round(np.rad2deg(np.angle(w)) / phase_lsb) * phase_lsb)
    return aq * np.exp(1j * pq)


def with_floor(db: np.ndarray, floor_dbc: float = FLOOR_DBC) -> np.ndarray:
    """Add the receiver noise floor in power, the way the sweep measures it."""
    return 10 * np.log10(10 ** (db / 10) + 10 ** (floor_dbc / 10))


GRID = np.arange(-90, 90.001, STEP)          # the GUI's steering grid
UNIF = steer(0.0)
PK = response(UNIF, GRID).max()


def _axes(ax, ymin=-30, ymax=4):
    ax.set_xlim(-60, 60)
    ax.set_ylim(ymin, ymax)
    ax.set_xticks(range(-60, 61, 15))
    ax.set_xlabel("steering angle (deg)")
    ax.set_ylabel("relative response (dB)")
    ax.grid(color=RULE, linewidth=0.8)


# ------------------------------------------------------------------ figure 1
def element_settings() -> None:
    """What the student types into Element Gains and Phase Control."""
    w, _ = null_weights(NULL_ANG)
    g = 100 * np.abs(w) / np.abs(w).max()
    p = np.rad2deg(np.angle(w))
    el = np.arange(1, N + 1)

    fig, (a1, a2) = plt.subplots(1, 2, figsize=(9.4, 3.5))
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
    finalize(fig, "L28-element-settings", also_page=True)


# ------------------------------------------------------------------ figure 2
def sweep_notch() -> None:
    """Frozen uniform reference vs the null-steered sweep on the GUI grid."""
    w, _ = null_weights(NULL_ANG)
    wq = quantize(w)
    u = with_floor(20 * np.log10(response(UNIF, GRID) / PK))
    q = with_floor(20 * np.log10(response(wq, GRID) / PK))

    fig, ax = plt.subplots(figsize=(8.6, 4.2))
    _axes(ax, ymin=-31)
    ax.plot(GRID, u, color=GREY, linewidth=1.3, label="uniform (frozen reference)")
    ax.plot(GRID, q, color=NAVY, linewidth=2.6, label="null steered")
    ax.axhline(FLOOR_DBC, color=RULE, linewidth=1.4, linestyle=(0, (5, 4)),
               label="sweep noise floor")

    i = int(np.argmin(np.abs(GRID - NULL_ANG)))
    ax.plot([GRID[i]], [q[i]], "o", color=RED, markersize=7)
    ax.annotate("notch  -21.6 dBc", xy=(GRID[i], q[i] - 0.3), xytext=(29, -26.2),
                fontsize=12, color=RED,
                arrowprops=dict(arrowstyle="->", color=RED, linewidth=1.3))
    ax.annotate("main lobe  -1.8 dB", xy=(0, q.max()), xytext=(-57, -5.0),
                fontsize=12, color=NAVY,
                arrowprops=dict(arrowstyle="->", color=NAVY, linewidth=1.3))
    ax.plot([NULL_ANG], [u[i]], "o", color=GREY, markersize=6)
    ax.annotate("reference sidelobe  -12.8 dBc", xy=(NULL_ANG + 0.6, u[i]),
                xytext=(30, -9.5), fontsize=12, color=GREY,
                arrowprops=dict(arrowstyle="->", color=GREY, linewidth=1.2))
    ax.legend(loc="lower left", fontsize=11.5, ncol=1)
    fig.tight_layout()
    finalize(fig, "L28-sweep-notch", also_page=True)


# ------------------------------------------------------------------ figure 3
def delta_beam() -> None:
    """Sum vs difference of the two digital channels."""
    s = np.ones(N)
    d = np.r_[np.ones(4), -np.ones(4)]
    th = np.linspace(-60, 60, 4001)
    ps = with_floor(20 * np.log10(np.maximum(response(s, th), 1e-9) / N), -22.0)
    pd = with_floor(20 * np.log10(np.maximum(response(d, th), 1e-9) / N), -22.0)

    fig, ax = plt.subplots(figsize=(8.6, 4.2))
    _axes(ax, ymin=-31)
    ax.set_xlabel("angle from broadside (deg)")
    ax.plot(th, ps, color=GREY, linewidth=1.4, label="sum  (Beam 1 Phase 0)")
    ax.plot(th, pd, color=NAVY, linewidth=2.6,
            label="difference  (Beam 1 Phase 180)")
    for sgn in (-1, 1):
        pk = sgn * 11.0
        ax.plot([pk], [pd[np.argmin(np.abs(th - pk))]], "o", color=GREEN, markersize=6)
    ax.annotate("peaks near +/-11 deg", xy=(11, pd[np.argmin(np.abs(th - 11))]),
                xytext=(19, -7.5), fontsize=12, color=GREEN,
                arrowprops=dict(arrowstyle="->", color=GREEN, linewidth=1.3))
    ax.annotate("boresight null  -22 dBc", xy=(0.4, -21.6),
                xytext=(3.5, -28.6), fontsize=12, color=RED,
                arrowprops=dict(arrowstyle="->", color=RED, linewidth=1.3))
    ax.legend(loc="lower left", fontsize=11.5)
    fig.tight_layout()
    finalize(fig, "L28-delta-beam", also_page=True)


# ------------------------------------------------------------------ figure 4
def mvdr_vs_manual() -> None:
    """Two-channel manual vs MVDR against a 10 dB interferer (widget fallback)."""
    ti, pi_db = 20.0, 10.0
    m = np.arange(4)

    def gsub(u):
        return np.exp(1j * np.outer(np.atleast_1d(u), m)).sum(axis=1)

    def chan(theta):
        u = KD * np.sin(np.deg2rad(np.atleast_1d(theta)))
        return np.stack([gsub(u), gsub(u) * np.exp(1j * 4 * u)], axis=-1)

    sv, vi = chan(0.0)[0], chan(ti)[0]
    P = 10 ** (pi_db / 10)
    R = 1e-3 * np.eye(2) + np.outer(sv, sv.conj()) + P * np.outer(vi, vi.conj())
    R = R + 1e-3 * np.trace(R).real / 2 * np.eye(2)
    Ri = np.linalg.inv(R)
    wv = Ri @ sv / (np.conj(sv) @ Ri @ sv)
    wm = np.array([1.0, 1.0]) / np.sqrt(2)
    wv = wv / np.linalg.norm(wv)

    th = np.linspace(-60, 60, 4001)
    A = chan(th)
    ref = np.abs(chan(0.0)[0] @ np.conj(wm))
    pm = with_floor(20 * np.log10(np.abs(A @ np.conj(wm)) / ref), -30)
    pv = with_floor(20 * np.log10(np.abs(A @ np.conj(wv)) / ref), -30)

    fig, ax = plt.subplots(figsize=(8.6, 4.0))
    _axes(ax, ymin=-39)
    ax.set_xlabel("angle from broadside (deg)")
    ax.plot(th, pm, color=GREY, linewidth=1.4, label="manual  (both channels added)")
    ax.plot(th, pv, color=NAVY, linewidth=2.6, label="MVDR")
    ax.axvline(ti, color=ORANGE, linewidth=1.4, linestyle=(0, (5, 4)))
    ax.text(ti + 1.5, 1.2, "interferer", fontsize=11.5, color=ORANGE)
    ax.annotate("17 dB lower here", xy=(ti + 0.3, -29.4),
                xytext=(27, -23.0), fontsize=12, color=RED,
                arrowprops=dict(arrowstyle="->", color=RED, linewidth=1.3))
    ax.annotate("look direction held", xy=(0, pv[np.argmin(np.abs(th))]),
                xytext=(-58, -13.0), fontsize=12, color=GREEN,
                arrowprops=dict(arrowstyle="->", color=GREEN, linewidth=1.3))
    ax.legend(loc="lower left", fontsize=11.5)
    fig.tight_layout()
    finalize(fig, "L28-mvdr-vs-manual")

    d_supp = pm[np.argmin(np.abs(th - ti))] - pv[np.argmin(np.abs(th - ti))]
    d_look = pv[np.argmin(np.abs(th))] - pm[np.argmin(np.abs(th))]
    print(f"  [check] suppression {d_supp:.1f} dB, look-direction change {d_look:.2f} dB")


# ------------------------------------------------------------------ figure 5
def monopulse() -> None:
    """Sum and delta together, and the error function their ratio produces."""
    th = np.linspace(-20, 20, 4001)
    A = np.exp(1j * np.outer(np.sin(np.deg2rad(th)), NIDX) * KD)
    sig = A @ np.ones(N)
    dlt = A @ np.r_[np.ones(4), -np.ones(4)]
    ps = with_floor(20 * np.log10(np.maximum(np.abs(sig), 1e-9) / N), -21.8)
    pd = with_floor(20 * np.log10(np.maximum(np.abs(dlt), 1e-9) / N), -21.8)

    # the two subarrays are displaced, so delta sits in quadrature with sum:
    # the error signal is Im(delta * conj(sum)) / |sum|^2
    err = -np.imag(dlt * np.conj(sig)) / np.abs(sig) ** 2

    fig, (a1, a2) = plt.subplots(1, 2, figsize=(10.2, 3.9))

    a1.set_xlim(-20, 20)
    a1.set_ylim(-26, 3)
    a1.set_xticks(range(-20, 21, 10))
    a1.set_xlabel("angle from broadside (deg)")
    a1.set_ylabel("channel level (dB)")
    a1.grid(color=RULE, linewidth=0.8)
    a1.plot(th, ps, color=GREY, linewidth=1.6, label="sum")
    a1.plot(th, pd, color=NAVY, linewidth=2.6, label="delta")
    a1.plot([0], [-21.8], "o", color=RED, markersize=6)
    a1.annotate("delta null  -21.8 dBc", xy=(0.4, -21.6), xytext=(2.6, -24.8),
                fontsize=11.5, color=RED,
                arrowprops=dict(arrowstyle="->", color=RED, linewidth=1.2))
    a1.annotate("sum is flat here", xy=(0.5, 0.15), xytext=(5.0, 1.6),
                fontsize=11.5, color=GREY,
                arrowprops=dict(arrowstyle="->", color=GREY, linewidth=1.2))
    a1.legend(loc="upper left", fontsize=11.5)

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
    finalize(fig, "L28-monopulse", also_page=True)



def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    element_settings()
    sweep_notch()
    delta_beam()
    mvdr_vs_manual()
    monopulse()


if __name__ == "__main__":
    main()
