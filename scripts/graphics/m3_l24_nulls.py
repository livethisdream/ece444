#!/usr/bin/env python3
"""Generate the L24 (null steering) lesson-page figures as inline SVG.

  - L24-jammer-sidelobe   : uniform N=8 pattern, target at broadside, jammer
                            arriving through the first sidelobe at +22.5 deg
  - L24-pattern-null      : uniform (thin) vs null-steered (bold), notch marked
  - L24-cost-vs-angle     : main-lobe loss vs null angle, split into the
                            subtraction and rescaling terms
  - L24-quant-depth       : exact vs ADAR1000-rounded weights, the RMS fill
                            estimate, and the depth phaser-00 measured
  - L24-cancel-phasors    : why the null is exact: the desired beam's phasors
                            at theta_1 end at N r_n, and r_n w_n reaches the
                            same point in a straight line
  - L24-projection        : why the rule is the smallest change, and why a
                            null near the beam removes most of it (schematic)
  - L24-weight-circle     : the eight weights on a circle about 1, mirror
                            pairs conjugate
  - L24-error-phasors     : why rounding moves the null but independent
                            channel errors fill it to sqrt(N) eps

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
def loss_terms(a: float):
    """Subtraction loss, rescaling loss, and total at the look direction (dB)."""
    w, r = null_weights(a)
    sub = -20 * np.log10(1 - abs(r) ** 2)
    resc = 20 * np.log10(np.abs(w).max())
    return sub, resc, sub + resc


def cost_vs_angle() -> None:
    """Loss in the look direction (broadside) as the null is walked in, by term."""
    halves = (np.linspace(-60, -5, 400), np.linspace(5, 60, 400))
    fig, ax = plt.subplots(figsize=(5.2, 3.2))
    ax.axvspan(-6.6, 6.6, color=RED, alpha=0.10, lw=0)
    ax.axhline(0, color="#8a929c", lw=0.9)
    for k, (col, lw, lab) in enumerate(((ORANGE, 1.8, "subtraction"),
                                         (GRAY, 1.8, "rescaling"),
                                         (NAVY, 2.6, "total"))):
        for h, half in enumerate(halves):
            ax.plot(half, [loss_terms(a)[k] for a in half], color=col, lw=lw,
                    ls=(0, (5, 3)) if k == 1 else "-", label=lab if h else None)
    ax.set_xlim(-60, 60)
    ax.set_ylim(-3, 11)
    ax.set_xticks(range(-60, 61, 30))
    ax.set_xlabel("null angle (deg from broadside)")
    ax.set_ylabel("look-direction loss (dB)")
    ax.grid(color=RULE, linewidth=0.8)
    ax.text(0, -2.7, "half-power beam", ha="center", va="bottom", rotation=90,
            color=RED, fontsize=11.5)
    tot = loss_terms(22.5)[2]
    ax.annotate(f"{tot:.1f} dB at\n+22.5 deg", xy=(22.5, tot), xytext=(30, tot + 3.0),
                arrowprops=dict(arrowstyle="->", color=NAVY, lw=1.3), color=NAVY, fontsize=12)
    resc5 = loss_terms(5.0)[1]
    ax.annotate("rescaling\nraises the beam", xy=(5.2, resc5), xytext=(16, -2.7),
                arrowprops=dict(arrowstyle="->", color=GRAY, lw=1.3), color=GRAY, fontsize=11.5,
                va="bottom")
    ax.legend(loc="upper left", fontsize=11.5, bbox_to_anchor=(0.0, 1.0))
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


# ------------------------------------------------------------------ figure 5
def _plane(ax, lim):
    ax.set_aspect("equal")
    ax.axhline(0, color="#8a929c", lw=0.8)
    ax.axvline(0, color="#8a929c", lw=0.8)
    ax.set_xticks([]); ax.set_yticks([])
    for sp in ax.spines.values():
        sp.set_visible(False)
    ax.set_xlim(*lim[0]); ax.set_ylim(*lim[1])


def _chain(ax, steps, color, lw=2.0, start=0j):
    z = start
    for st in steps:
        ax.annotate("", xy=(z.real + st.real, z.imag + st.imag), xytext=(z.real, z.imag),
                    arrowprops=dict(arrowstyle="-|>", color=color, lw=lw, mutation_scale=11,
                                    shrinkA=0, shrinkB=0))
        z += st
    return z


def cancel_phasors() -> None:
    """At theta_1: w_d's unit phasors fan out and end at N r_n; r_n w_n's are aligned."""
    psi = KD * np.sin(np.deg2rad(22.5))
    _, r = null_weights(22.5)
    unit = np.exp(1j * NIDX * psi)                  # w_d,n v_n(theta_1), w_d = 1
    aligned = np.full(N, r)                          # r_n w_n,n v_n(theta_1) = r_n
    end = unit.sum()
    assert abs(end - N * r) < 1e-9 and abs(aligned.sum() - N * r) < 1e-9
    pts = np.concatenate([[0], np.cumsum(unit)])
    x0, x1 = pts.real.min() - 0.2, pts.real.max() + 0.2
    y0, y1 = pts.imag.min() - 0.2, pts.imag.max() + 0.2
    fig, ax = plt.subplots(figsize=(6.0, 3.6))
    _plane(ax, ((x0, x1 + 2.5), (y0, y1)))           # label column to the right of the chains
    _chain(ax, unit, NAVY, 2.0)
    _chain(ax, aligned, ORANGE, 2.6)
    ax.plot([end.real], [end.imag], "o", color=RED, ms=8, zorder=5)
    tx = x1 + 0.15
    ax.text(tx, y1 - 0.05, "beam: eight unit phasors,\n" f"each turned {np.degrees(psi):.1f} deg",
            color=NAVY, fontsize=12, va="top")
    ax.text(tx, (y0 + y1) / 2 + 0.1, "subtracted: eight phasors\n" f"of {abs(r):.3f}, all in line",
            color=ORANGE, fontsize=12, va="center")
    ax.text(tx, y0 + 0.1, "both end at " f"{abs(end):.2f}\n"
            f"at {np.degrees(np.angle(end)):.1f} deg", color=RED, fontsize=12, va="bottom")
    finalize(fig, "L24-cancel-phasors")


# ------------------------------------------------------------------ figure 6
def projection() -> None:
    """Schematic: w_d, the w_n direction, the removed part r_n w_n, and w."""
    fig, axes = plt.subplots(1, 2, figsize=(5.3, 2.75))
    for ax, ang, title in ((axes[0], 22.5, "on a sidelobe"),
                           (axes[1], 5.0, "near the main lobe")):
        _, r = null_weights(ang)
        c = abs(r)                                    # cos of the angle between w_d and w_n
        phi = np.arccos(c)
        wd = np.exp(1j * phi)                         # unit w_d, w_n along the real axis
        proj = c + 0j                                 # r_n w_n, normalized
        w = wd - proj                                 # perpendicular to w_n
        _plane(ax, ((-0.25, 1.35), (-0.25, 1.2)))
        ax.axhline(0, color="white", lw=2)            # hide the axis under w_n
        ax.annotate("", xy=(1.25, 0), xytext=(0, 0),
                    arrowprops=dict(arrowstyle="-|>", color=GRAY, lw=1.4, ls="--"))
        for vec, col, lw in ((wd, NAVY, 2.6), (proj, ORANGE, 2.8)):
            ax.annotate("", xy=(vec.real, vec.imag), xytext=(0, 0),
                        arrowprops=dict(arrowstyle="-|>", color=col, lw=lw, mutation_scale=14))
        ax.annotate("", xy=(wd.real, wd.imag), xytext=(proj.real, proj.imag),
                    arrowprops=dict(arrowstyle="-|>", color=GREEN, lw=2.6, mutation_scale=14))
        s = 0.06                                      # right-angle mark at proj
        ax.plot([c - s, c - s, c], [0, s, s], color=GREEN, lw=1.0)
        ax.text(1.27, -0.09, r"$\mathbf{w}_\mathrm{n}$", color=GRAY, fontsize=20, ha="right", va="top")
        ax.text(wd.real * 0.5 - 0.06, wd.imag * 0.5 + 0.03, r"$\mathbf{w}_\mathrm{d}$",
                color=NAVY, fontsize=20, ha="right")
        ax.text(proj.real * 0.5, -0.06, r"$r_\mathrm{n}\mathbf{w}_\mathrm{n}$", color=ORANGE,
                fontsize=20, ha="center", va="top")
        ax.text(c + 0.05, wd.imag * 0.5, r"$\mathbf{w}$", color=GREEN, fontsize=20, va="center")
        ax.set_title(f"{title}\nprojection {c:.2f}, keeps {1 - c**2:.2f}",
                     fontsize=11.5, color=INK)
    finalize(fig, "L24-projection")


# ------------------------------------------------------------------ figure 7
def weight_circle() -> None:
    """The eight weights w_n = 1 - r_n e^{-jn psi_1} on a circle about 1."""
    w, r = null_weights(22.5)
    fig, ax = plt.subplots(figsize=(5.0, 3.7))
    th = np.linspace(0, 2 * np.pi, 400)
    R = abs(r)
    ax.plot(1 + R * np.cos(th), R * np.sin(th), color=RULE, lw=1.6)
    ax.plot([1], [0], "+", color=GRAY, ms=10)
    ax.text(1.0, -0.035, "center 1", color=GRAY, fontsize=11.5, ha="center", va="top")
    for n in range(N // 2):                          # mirror pairs n, N-1-n
        a, b = w[n], w[N - 1 - n]
        assert abs(a - np.conj(b)) < 1e-12
        ax.plot([a.real, b.real], [a.imag, b.imag], color=ORANGE, lw=1.0, ls=(0, (3, 3)))
    k = 2                                             # element 3, the largest phase
    ax.plot([0, w[k].real * 1.08], [0, w[k].imag * 1.08], color=GRAY, lw=0.9)
    ax.plot(w.real, w.imag, "o", color=NAVY, ms=9, zorder=5)
    for n in range(N):
        d = w[n] - 1
        off = d / abs(d) * 0.055
        ax.text(w[n].real + off.real, w[n].imag + off.imag, str(n + 1), color=NAVY,
                fontsize=12.5, ha="center", va="center", fontweight="bold")
    ax.text(0.03, -0.03, "phase of element 3:\n" f"{np.degrees(np.angle(w[k])):+.1f} deg",
            color=GRAY, fontsize=11.5, va="top")
    ax.set_aspect("equal")
    ax.set_xlim(0, 1.32)
    ax.set_ylim(-0.32, 0.32)
    ax.axhline(0, color="#8a929c", lw=0.8)
    ax.set_xlabel("real part")
    ax.set_ylabel("imaginary part")
    ax.grid(color=RULE, linewidth=0.6)
    ax.text(1.31, -0.30, "mirror pairs:\nconjugates", color=ORANGE, fontsize=11.5,
            ha="right", va="bottom")
    finalize(fig, "L24-weight-circle")


# ------------------------------------------------------------------ figure 8
def error_phasors() -> None:
    """Left: rounding errors come in conjugate pairs. Right: independent errors random-walk."""
    w, _ = null_weights(22.5)
    ws = w / np.abs(w).max()
    wq = quantize(w)
    psi = KD * np.sin(np.deg2rad(22.5))
    centre = np.exp(1j * (NIDX - (N - 1) / 2) * psi)  # phase referred to the array center
    err_round = (wq - ws) * centre
    lsb = np.deg2rad(2.8125)
    eps = np.hypot(lsb / np.sqrt(12), 0.01 / np.sqrt(12))
    rr = np.sqrt(N) * eps
    for seed in range(200):                          # a walk that ends near its RMS distance
        rng = np.random.default_rng(seed)
        ph = rng.uniform(-lsb / 2, lsb / 2, N)
        am = rng.uniform(-0.005, 0.005, N)
        wr = (np.abs(ws) + am) * np.exp(1j * (np.angle(ws) + ph))
        err_rand = (wr - ws) * centre
        if abs(abs(err_rand.sum()) - rr) < 0.1 * rr:
            break
    fig, axes = plt.subplots(1, 2, figsize=(5.4, 2.55))
    for ax, err, title, lim in ((axes[0], err_round, "rounding this table (2x zoom):\npairs sum onto the real axis", 0.035),
                                (axes[1], err_rand, "independent channel errors:\na random walk", 0.07)):
        reach = max(np.abs(np.cumsum(err).imag).max(), rr if ax is axes[1] else 0) + 0.15 * lim
        ylim = max(0.68 * lim, reach)                 # fit the walk and the circle, not a guess
        _plane(ax, ((-lim, lim), (-ylim, ylim)))
        z = 0j
        for n, e in enumerate(err):
            col = (NAVY, BLUE, GREEN, ORANGE)[min(n, N - 1 - n)]
            ax.annotate("", xy=(z.real + e.real, z.imag + e.imag), xytext=(z.real, z.imag),
                        arrowprops=dict(arrowstyle="-|>", color=col, lw=1.8, mutation_scale=10,
                                        shrinkA=0, shrinkB=0))
            z += e
        ax.plot([z.real], [z.imag], "o", color=RED, ms=7, zorder=5)
        ax.set_title(title, fontsize=11.5, color=INK)
        if ax is axes[1]:
            t = np.linspace(0, 2 * np.pi, 300)
            ax.plot(rr * np.cos(t), rr * np.sin(t), color=RED, lw=1.0, ls=(0, (4, 3)))
            ax.text(lim - 0.002, ylim - 0.002, "circle: √N × ε", color=RED,
                    fontsize=11, ha="right", va="top")      # top-right corner, outside the circle
        else:
            assert abs(z.imag) < 1e-12
    finalize(fig, "L24-error-phasors")


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    jammer_sidelobe()
    pattern_null()
    cost_vs_angle()
    quant_depth()
    cancel_phasors()
    projection()
    weight_circle()
    error_phasors()


if __name__ == "__main__":
    main()
