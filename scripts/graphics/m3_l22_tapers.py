#!/usr/bin/env python3
"""Generate the L22 (Sidelobes and Tapering) figures as inline SVG.

  - L22-edge-fourier   : aperture illumination (sharp vs smooth edge) and the
                         pattern each one produces -- why sidelobes exist
  - L22-sll-vs-cost    : the Dolph trade curve -- HPBW and taper efficiency
                         against design sidelobe level, named tapers marked
  - L22-cheb-map       : the -30 dB Chebyshev polynomial T_7(x) in dB, with
                         the equal-ripple sidelobe region, the main lobe up to
                         x0, and the stretch of x that visible space covers
  - L22-pedestal-trade : highest sidelobe and HPBW against the pedestal P,
                         with the minimum near P = 0.06 and Hamming marked
  - L22-taylor-vs-cheb : -30 dB Chebyshev and Taylor on 64 elements, amplitudes
                         (the Chebyshev edge spike) and patterns
  - L22-rounding       : exact against 1%-rounded patterns, the -50 dB design
                         and the GUI Chebyshev preset
  - L22-cheb-vs-hann   : the -30 dB Chebyshev and Hann patterns overlaid
  - L22-phasor-sidelobe: the eight-phasor chain at the first null and at the
                         first sidelobe (one and a half turns)
  - L22-preset-traces  : the four GUI presets' theory patterns on the uniform
                         peak's scale, floored at the -23 dB sweep floor

Every number here is computed from the same formulas the lesson page and the
taper-explorer widget use: N = 8, d/lambda = 0.481 (10.3 GHz, d = 14 mm).
The figures carry no equations -- words, numbers and axis labels only.

    python3 scripts/graphics/m3_l22_tapers.py
    -> book/extras/viz/img/L22-*.svg (the nine figures above)
"""

from __future__ import annotations
import io, re
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from svg_font_stack import apply_font_stack

NAVY, BLUE, RED, GREEN, ORANGE, GRAY = "#004a85", "#0067b9", "#b01e24", "#1d7a4d", "#e67e22", "#5a5a5a"
INK, RULE = "#1a1a1a", "#c7d2e0"
OUT = Path(__file__).resolve().parents[2] / "book/extras/viz/img"

N, DL = 8, 0.481

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


# --------------------------------------------------------------------------
# tapers and pattern machinery
# --------------------------------------------------------------------------
def cheb_T(n, x):
    x = np.asarray(x, float)
    o = np.empty_like(x)
    m = np.abs(x) <= 1
    o[m] = np.cos(n * np.arccos(x[m]))
    xm = x[~m]
    o[~m] = np.cosh(n * np.arccosh(np.abs(xm))) * np.where(xm < 0, (-1.0) ** n, 1.0)
    return o


def dolph(sll_db: float, n: int = N, K: int = 4096) -> np.ndarray:
    """Dolph-Chebyshev amplitudes for an even-N broadside array, peak = 1.

    AF(psi) = T_{N-1}(x0 cos(psi/2)) = 2 sum_m a_m cos((2m-1)psi/2), so the
    a_m fall out of a Fourier quadrature over one period of psi."""
    M = n // 2
    R = 10 ** (abs(sll_db) / 20.0)
    x0 = np.cosh(np.arccosh(R) / (n - 1))
    psi = 2 * np.pi * np.arange(K) / K
    f = cheb_T(n - 1, x0 * np.cos(psi / 2))
    half = np.array([(f * np.cos((2 * m - 1) * psi / 2)).sum() / K for m in range(1, M + 1)])
    a = np.concatenate([half[::-1], half])
    return a / a.max()


def hann(n: int = N) -> np.ndarray:
    p = (np.arange(n) + 1) / (n + 1) - 0.5      # sample cos^2 on an N+1 grid
    a = np.cos(np.pi * p) ** 2
    return a / a.max()


def taylor(sll_db: float, nbar: int, n: int = N) -> np.ndarray:
    """Taylor n-bar line-source distribution sampled at the element centers."""
    A = np.arccosh(10 ** (abs(sll_db) / 20.0)) / np.pi
    sig = nbar / np.sqrt(A ** 2 + (nbar - 0.5) ** 2)
    zsq = lambda k: sig ** 2 * (A ** 2 + (k - 0.5) ** 2)
    g = np.ones(n)
    p = (np.arange(n) - (n - 1) / 2) / n
    for m in range(1, nbar):
        num = np.prod([1 - m ** 2 / zsq(k) for k in range(1, nbar)])
        den = np.prod([1 - m ** 2 / k ** 2 for k in range(1, nbar) if k != m])
        g += 2 * ((-1) ** (m + 1)) * num / (2 * den) * np.cos(2 * np.pi * m * p)
    return g / g.max()


BLACKMAN = np.array([0.06, 0.27, 0.66, 1.0, 1.0, 0.66, 0.27, 0.06])

TH = np.linspace(-90, 90, 240001)


def pattern_db(a: np.ndarray) -> np.ndarray:
    a = np.asarray(a, float)
    n = np.arange(len(a)) - (len(a) - 1) / 2
    psi = 2 * np.pi * DL * np.sin(np.radians(TH))
    F = np.abs(np.sum(a[:, None] * np.exp(1j * n[:, None] * psi[None, :]), axis=0)) / a.sum()
    return 20 * np.log10(np.maximum(F, 1e-14))


def hpbw(a: np.ndarray) -> float:
    db = pattern_db(a)
    i0 = int(np.argmax(db))
    lo = TH[:i0][db[:i0] <= -3][-1]
    hi = TH[i0:][db[i0:] <= -3][0]
    return hi - lo


def eta_t(a: np.ndarray) -> float:
    a = np.asarray(a, float)
    return a.sum() ** 2 / (len(a) * np.sum(a ** 2))


def first_sll(a: np.ndarray) -> float:
    db = pattern_db(a)
    d = np.diff(np.sign(np.diff(db)))
    pk = [i + 1 for i in np.where(d < 0)[0] if abs(TH[i + 1]) > 1e-3]
    return max(db[p] for p in pk) if pk else float("nan")


# --------------------------------------------------------------------------
def edge_fourier() -> None:
    """The Fourier reading of a taper: a sharp aperture edge carries the
    high space-frequency content that lands in the sidelobes."""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(9.6, 3.6),
                                   gridspec_kw={"width_ratios": [1, 1.35]})

    p = np.linspace(-0.62, 0.62, 1400)
    rect = np.where(np.abs(p) <= 0.5, 1.0, 0.0)
    smooth = np.where(np.abs(p) <= 0.5, np.cos(np.pi * np.clip(p, -0.5, 0.5)) ** 2, 0.0)
    ax1.plot(p, rect, color=NAVY, lw=2.6, label="sharp edge")
    ax1.plot(p, smooth, color=ORANGE, lw=2.6, label="smooth edge")
    ax1.set_xlim(-0.62, 0.62); ax1.set_ylim(-0.06, 1.18)
    ax1.set_xlabel("Position across the aperture")
    ax1.set_ylabel("Illumination")
    ax1.set_xticks([-0.5, 0, 0.5]); ax1.set_xticklabels(["edge", "center", "edge"])
    ax1.set_yticks([0, 0.5, 1.0])
    ax1.grid(color=RULE, linewidth=0.8)
    for sp in ("top", "right"):
        ax1.spines[sp].set_visible(False)
    ax1.legend(loc="upper center", ncol=2, fontsize=11, handlelength=1.5, columnspacing=1.1,
               bbox_to_anchor=(0.5, 1.16))

    du = pattern_db(np.ones(N))
    dh = pattern_db(hann())
    ax2.plot(TH, du, color=NAVY, lw=2.2, label="sharp edge")
    ax2.plot(TH, dh, color=ORANGE, lw=2.2, label="smooth edge")
    ax2.set_xlim(-90, 90); ax2.set_ylim(-60, 4)
    ax2.set_xticks(range(-90, 91, 30))
    ax2.set_xlabel("Angle from broadside  (deg)")
    ax2.set_ylabel("Relative power  (dB)")
    ax2.grid(color=RULE, linewidth=0.8)
    for sp in ("top", "right"):
        ax2.spines[sp].set_visible(False)
    ax2.axhline(-12.8, color=NAVY, lw=1.1, ls=(0, (4, 3)))
    ax2.axhline(-31.8, color=ORANGE, lw=1.1, ls=(0, (4, 3)))
    ax2.text(-87, -11.2, "−12.8 dB", color=NAVY, fontsize=11.5, fontweight="bold",
             ha="left", va="bottom")
    ax2.text(-87, -30.2, "−31.8 dB", color=ORANGE, fontsize=11.5, fontweight="bold",
             ha="left", va="bottom")
    finalize(fig, "L22-edge-fourier")


def sll_vs_cost() -> None:
    """What a deeper sidelobe specification costs, along the Dolph family."""
    sll = np.linspace(15.0, 55.0, 240)
    hp = np.array([hpbw(dolph(s)) for s in sll])
    et = np.array([eta_t(dolph(s)) for s in sll])

    fig, ax = plt.subplots(figsize=(8.4, 4.4))
    ax.plot(-sll, hp, color=NAVY, lw=2.8)
    ax.set_xlim(-56, -10); ax.set_ylim(12, 23)
    ax.set_xticks(range(-55, -9, 5))
    ax.set_xlabel("Design sidelobe level  (dB)")
    ax.set_ylabel("HPBW  (deg)  —  solid", color=NAVY)
    ax.tick_params(axis="y", colors=NAVY)
    ax.grid(color=RULE, linewidth=0.8)
    ax.spines["top"].set_visible(False)

    ax2 = ax.twinx()
    ax2.plot(-sll, et, color=ORANGE, lw=2.4, ls=(0, (5, 3)))
    ax2.set_ylim(0.58, 1.06)
    ax2.set_ylabel("Taper efficiency  —  dashed", color=ORANGE)
    ax2.tick_params(axis="y", colors=ORANGE)
    ax2.spines["top"].set_visible(False)

    for s, lab, dx, dy, ha in [(12.8, "uniform", -0.8, 0.30, "right"),
                               (20.0, "−20 dB", 0.8, 0.30, "left"),
                               (30.0, "−30 dB", 0.8, 0.30, "left"),
                               (40.0, "−40 dB", 0.8, 0.30, "left")]:
        a = np.ones(N) if s < 13 else dolph(s)
        y = hpbw(a)
        ax.plot(-s, y, "o", color=NAVY, ms=7.5, zorder=5)
        ax.text(-s + dx, y + dy, lab, color=NAVY, fontsize=11.5, fontweight="bold",
                ha=ha, va="bottom")

    for a, lab, col, dy in [(hann(), "Hann", RED, -0.35),
                            (BLACKMAN, "Blackman", GREEN, -0.35),
                            (taylor(30.0, 4), "Taylor −30 dB", GRAY, -0.45)]:
        x = first_sll(a)
        side = "left" if lab.startswith("Taylor") else "right"
        ax.plot(x, hpbw(a), "D", color=col, ms=7, zorder=6)
        ax.text(x + (0.9 if side == "left" else -0.9), hpbw(a) + dy, lab,
                color=col, fontsize=11.5, fontweight="bold", ha=side,
                va="bottom" if dy > 0 else "top")
    finalize(fig, "L22-sll-vs-cost")


def cheb_map(sll_db: float = 30.0) -> None:
    """Why equal ripple: T_7 stays within +-1 for |x| <= 1 (every sidelobe at
    the design level) and grows fastest beyond it (the main lobe, up to x0)."""
    R = 10 ** (sll_db / 20.0)
    x0 = np.cosh(np.arccosh(R) / (N - 1))
    xv = x0 * np.cos(np.pi * DL)               # x at endfire: psi = kd
    x = np.linspace(-1.0, x0, 6001)
    db = 20 * np.log10(np.maximum(np.abs(cheb_T(N - 1, x)), 1e-4)) - 20 * np.log10(R)

    fig, ax = plt.subplots(figsize=(8.4, 4.0))
    ymin, ymax = -62, 6
    ax.axvspan(-1.0, 1.0, color=RULE, alpha=0.35, lw=0)
    ax.axvspan(xv, x0, ymin=0, ymax=0.045, color=BLUE, alpha=0.9, lw=0)
    ax.axhline(-sll_db, color=RED, lw=1.4, ls=(0, (5, 3)))
    ax.plot(x, db, color=NAVY, lw=2.4)
    ax.plot([x0], [0], "o", color=NAVY, ms=7, zorder=5)
    ax.set_xlim(-1.0, x0 + 0.02); ax.set_ylim(ymin, ymax)
    ax.set_xlabel("x"); ax.set_ylabel("Pattern  (dB)")
    ax.grid(color=RULE, linewidth=0.8)
    for sp in ("top", "right"):
        ax.spines[sp].set_visible(False)

    # labels placed from the data: each sits in a gap the curve leaves
    nulls = np.cos((2 * np.arange(N - 1) + 1) * np.pi / (2 * (N - 1))) * 1.0
    gap = sorted(z for z in nulls if xv < z < 1)[:1]
    vis_x = (xv + gap[0]) / 2 if gap else (xv + x0) / 2
    box = dict(facecolor="white", edgecolor="none", pad=1.5)
    ax.text(-0.5, -sll_db + 2.0, f"every sidelobe at −{sll_db:.0f} dB", color=RED,
            ha="center", va="bottom", fontsize=11.5, fontweight="bold")
    ax.text(-0.5, -sll_db + 9.0, "|x| ≤ 1: sidelobe region", color=GRAY,
            ha="center", va="bottom", fontsize=11)
    ax.text(x0 - 0.07, -3.0, f"main lobe, peak at x₀ = {x0:.3f}", color=NAVY,
            ha="right", va="center", fontsize=11.5, fontweight="bold")
    ax.text(vis_x, ymin + 0.06 * (ymax - ymin), "visible space", color=BLUE,
            ha="center", va="bottom", fontsize=11, fontweight="bold", bbox=box)
    finalize(fig, "L22-cheb-map")


P_GRID = (np.arange(N) - (N - 1) / 2) / (N + 1)    # the lesson's pedestal sampling


def pedestal(P: float) -> np.ndarray:
    a = P + (1 - P) * np.cos(np.pi * P_GRID) ** 2
    return a / a.max()


def mn(t: str) -> str:
    """Typographic minus in every number a label prints."""
    return t.replace("-", "\u2212")


def style(ax) -> None:
    ax.grid(color=RULE, linewidth=0.8)
    for sp in ("top", "right"):
        ax.spines[sp].set_visible(False)


def pedestal_trade() -> None:
    """Sidelobe level and beamwidth against pedestal: a trade with an optimum."""
    P = np.linspace(0.0, 1.0, 201)
    sl = np.array([first_sll(pedestal(x)) for x in P])
    hp = np.array([hpbw(pedestal(x)) for x in P])
    i = int(np.argmin(sl))

    fig, ax = plt.subplots(figsize=(7.2, 4.2))
    ax.plot(P, sl, color=NAVY, lw=2.6)
    ax.set_xlim(0, 1); ax.set_ylim(-36, -10)
    ax.set_xlabel("Pedestal P")
    ax.set_ylabel("Highest sidelobe  (dB)  —  solid", color=NAVY)
    ax.tick_params(axis="y", colors=NAVY)
    style(ax)
    ax2 = ax.twinx()
    ax2.plot(P, hp, color=ORANGE, lw=2.2, ls=(0, (5, 3)))
    ax2.set_ylim(12, 21)
    ax2.set_ylabel("HPBW  (deg)  —  dashed", color=ORANGE)
    ax2.tick_params(axis="y", colors=ORANGE)
    ax2.spines["top"].set_visible(False)

    # the three low points crowd together, so their labels stack in the empty
    # band under the rising curve (x from 0.22, below -28 dB) with leader lines
    low = [(0.0, "Hann"), (0.08, "Hamming"), (P[i], f"minimum, P = {P[i]:.2f}")]
    for k, (x, lab) in enumerate(low):
        y = first_sll(pedestal(x))
        ax.plot(x, y, "o", color=NAVY, ms=7, zorder=5, clip_on=False)
        ty = -28.6 - 2.3 * k
        ax.annotate(mn(f"{lab}: {y:.1f} dB"), xy=(x, y), xytext=(0.24, ty),
                    color=NAVY, fontsize=11, fontweight="bold", va="center",
                    arrowprops=dict(arrowstyle="-", color=NAVY, lw=0.8))
    yu = first_sll(pedestal(1.0))
    ax.plot(1.0, yu, "o", color=NAVY, ms=7, zorder=5, clip_on=False)
    ax.text(0.97, yu + 1.2, mn(f"uniform: {yu:.1f} dB"), color=NAVY, fontsize=11,
            fontweight="bold", ha="right", va="center")
    finalize(fig, "L22-pedestal-trade")


def taylor_vs_cheb(n: int = 64, sll_db: float = 30.0, nbar: int = 5) -> None:
    """A Chebyshev design on a large array spikes its edge elements; Taylor
    lets the far sidelobes decay and keeps the edge smooth."""
    c = dolph(sll_db, n, K=16384); t = taylor(sll_db, nbar, n)
    fig, (a1, a2) = plt.subplots(2, 1, figsize=(6.6, 5.4))
    k = np.arange(1, n // 2 + 1)
    half_c = c[: n // 2]; half_t = t[: n // 2]
    a1.plot(k, half_c, "o-", color=NAVY, ms=3.5, lw=1.6, label="Chebyshev")
    a1.plot(k, half_t, "s-", color=ORANGE, ms=3.2, lw=1.6, label="Taylor")
    a1.set_xlim(0.5, n // 2 + 0.5); a1.set_ylim(0, 1.05)
    a1.set_xlabel("Element, edge to center"); a1.set_ylabel("Amplitude")
    style(a1)
    a1.annotate("edge spike", xy=(1, half_c[0]), xytext=(5, half_c[0] + 0.22),
                color=NAVY, fontsize=11, fontweight="bold",
                arrowprops=dict(arrowstyle="->", color=NAVY, lw=1.2))
    a1.legend(loc="lower right", fontsize=11)

    db_c = pattern_db(c); db_t = pattern_db(t)
    m = TH >= 0
    a2.plot(TH[m], db_t[m], color=ORANGE, lw=1.4)
    a2.plot(TH[m], db_c[m], color=NAVY, lw=1.4)
    a2.axhline(-sll_db, color=RED, lw=1.2, ls=(0, (5, 3)))
    a2.set_xlim(0, 90); a2.set_ylim(-60, 2)
    a2.set_xlabel("Angle from broadside  (deg)"); a2.set_ylabel("Pattern  (dB)")
    style(a2)
    a2.text(89, -sll_db + 1.5, "Chebyshev: every sidelobe on the line", color=NAVY,
            ha="right", va="bottom", fontsize=11, fontweight="bold")
    a2.text(89, -57, "Taylor: far sidelobes decay", color=ORANGE,
            ha="right", va="bottom", fontsize=11, fontweight="bold",
            bbox=dict(facecolor="white", edgecolor="none", pad=1.5))
    fig.tight_layout(h_pad=1.2)
    finalize(fig, "L22-taylor-vs-cheb")


def rounding() -> None:
    """Rounding to the PHASER's 1% gain step: harmless at -30 dB, fatal at -50
    dB, and it erases the nulls of the GUI's -100 dB-class Chebyshev preset."""
    ex50 = dolph(50.0); r50 = np.round(ex50 * 100) / 100
    ex100 = dolph(100.0); r100 = np.round(ex100 * 100) / 100
    fig, (a1, a2) = plt.subplots(2, 1, figsize=(6.6, 4.8), sharex=True)
    m = TH >= 0
    for ax, ex, rd, title in [(a1, ex50, r50, "\u221250 dB design"),
                              (a2, ex100, r100, "GUI Chebyshev preset")]:
        ax.plot(TH[m], pattern_db(ex)[m], color=GRAY, lw=1.3, label="exact")
        ax.plot(TH[m], pattern_db(rd)[m], color=NAVY, lw=2.0, label="rounded to 1%")
        ax.set_xlim(0, 90); ax.set_ylim(-110, 2)
        ax.set_ylabel("Pattern  (dB)")
        ax.text(1, -104, title, fontsize=12.5, color=INK, fontweight="bold",
                ha="left", va="bottom")
        style(ax)
    a2.set_xlabel("Angle from broadside  (deg)")
    s_ex, s_rd = first_sll(ex50), first_sll(r50)
    a1.axhline(s_rd, color=RED, lw=1.1, ls=(0, (5, 3)))
    # under the main lobe, left of the first null, the band from -42 to -60 dB
    # is empty at every angle below about 25 degrees
    a1.axhline(s_ex, color=GRAY, lw=0.9, ls=(0, (2, 2)))
    a1.text(89, s_rd + 1.5, mn(f"rounded: {s_rd:.1f} dB"), color=RED, ha="right",
            va="bottom", fontsize=11, fontweight="bold")
    a1.text(1, s_ex - 1.5, mn(f"exact: {s_ex:.1f} dB"), color=GRAY, ha="left",
            va="top", fontsize=11)
    end = pattern_db(r100)[-1]
    a2.text(88, (end + pattern_db(ex100)[-1]) / 2, "rounded: no null,\nno sidelobe",
            color=NAVY, ha="right", va="center", fontsize=11, fontweight="bold")
    a2.legend(loc="center left", fontsize=11)
    fig.tight_layout(h_pad=0.8)
    finalize(fig, "L22-rounding")


def cheb_vs_hann() -> None:
    """Same suppression, different shape: equal ripple against decaying lobes."""
    c = dolph(30.0); h = hann()
    m = TH >= 0
    fig, ax = plt.subplots(figsize=(7.6, 3.8))
    ax.plot(TH[m], pattern_db(h)[m], color=RED, lw=1.8, label=f"Hann, HPBW {hpbw(h):.1f}°")
    ax.plot(TH[m], pattern_db(c)[m], color=NAVY, lw=2.2, label=f"Chebyshev −30 dB, HPBW {hpbw(c):.1f}°")
    ax.axhline(-30, color=NAVY, lw=1.0, ls=(0, (5, 3)))
    ax.axhline(-3.01, color=GRAY, lw=0.9, ls=(0, (2, 2)))
    ax.set_xlim(0, 90); ax.set_ylim(-70, 2)
    ax.set_xlabel("Angle from broadside  (deg)"); ax.set_ylabel("Pattern  (dB)")
    style(ax)
    ax.legend(loc="upper right", fontsize=11)
    finalize(fig, "L22-cheb-vs-hann")


def phasor_sidelobe() -> None:
    """Lesson 16's chain of eight unit phasors at the first null (one turn,
    a closed octagon) and at the first sidelobe (one and a half turns)."""
    fig, axes = plt.subplots(1, 2, figsize=(8.4, 4.0))
    for ax, turns, title, col in [(axes[0], 1.0, "first null: one turn, closes", RED),
                                  (axes[1], 1.5, "first sidelobe: 1.5 turns, leftover", NAVY)]:
        psi = 2 * np.pi * turns / N
        z = np.concatenate([[0], np.cumsum(np.exp(1j * psi * np.arange(N)))])
        for k in range(N):
            # phasors that complete the first full turn cancel; draw them pale
            done = turns > 1 and (k + 1) * psi <= 2 * np.pi + 1e-9
            ax.annotate("", xy=(z[k + 1].real, z[k + 1].imag), xytext=(z[k].real, z[k].imag),
                        arrowprops=dict(arrowstyle="-|>", color=RULE if done else col,
                                        lw=1.8, mutation_scale=12))
        if abs(z[-1]) > 1e-6:
            ax.annotate("", xy=(z[-1].real, z[-1].imag), xytext=(0, 0),
                        arrowprops=dict(arrowstyle="-|>", color=ORANGE, lw=2.4, mutation_scale=14))
            db = 20 * np.log10(abs(z[-1]) / N)
            ax.text(z.real.mean(), z.imag.min() - 0.35,
                    mn(f"sum = {abs(z[-1]):.2f} of 8 ({db:.1f} dB)"),
                    color=ORANGE, ha="center", va="top", fontsize=11, fontweight="bold")
        ax.set_aspect("equal"); ax.axis("off")
        pad = 0.6
        ax.set_xlim(z.real.min() - pad, z.real.max() + pad)
        ax.set_ylim(z.imag.min() - pad - 0.6, z.imag.max() + pad)
        ax.set_title(title, fontsize=12, color=INK)
    finalize(fig, "L22-phasor-sidelobe")


GUI_PRESETS = [("Uniform", np.ones(N), NAVY),
               ("Hann", np.array([.12, .43, .77, 1, 1, .77, .43, .12]), RED),
               ("Blackman", BLACKMAN, GREEN),
               ("Chebyshev", np.array([.04, .23, .62, 1, 1, .62, .23, .04]), ORANGE)]
FLOOR_DB = -23.0


def preset_traces() -> None:
    """The four presets as a sweep would draw them, from theory: the pattern on
    the uniform peak's scale (so the taper's peak drop shows), floored at the
    sweep's noise floor."""
    fig, ax = plt.subplots(figsize=(7.6, 4.0))
    m = np.abs(TH) <= 60
    for name, a, col in GUI_PRESETS:
        y = pattern_db(a) + 20 * np.log10(a.sum() / len(a))
        ax.plot(TH[m], np.maximum(y[m], FLOOR_DB), color=col, lw=2.0,
                label=mn(f"{name}, peak {20 * np.log10(a.sum() / len(a)):+.1f} dB").replace("+0.0", "0.0"))
    ax.axhline(FLOOR_DB, color=GRAY, lw=1.1, ls=(0, (5, 3)))
    ax.text(-59, FLOOR_DB - 0.8, "noise floor, −23 dB", color=GRAY, ha="left", va="top", fontsize=11)
    ax.set_xlim(-60, 60); ax.set_ylim(-28, 2)
    ax.set_xticks(range(-60, 61, 15))
    ax.set_xlabel("Commanded steer angle  (deg)")
    ax.set_ylabel("dB relative to uniform peak")
    style(ax)
    ax.legend(loc="upper right", fontsize=10.5)
    finalize(fig, "L22-preset-traces")


def report() -> None:
    rows = [("Uniform", np.ones(N)), ("Chebyshev −20 dB", dolph(20)),
            ("Chebyshev −30 dB", dolph(30)), ("Chebyshev −40 dB", dolph(40)),
            ("Hann", hann()), ("Taylor -30 n4", taylor(30.0, 4)), ("Blackman", BLACKMAN),
            ("GUI Chebyshev", np.array([.04, .23, .62, 1, 1, .62, .23, .04]))]
    print(f"\n{'taper':<18}{'a_n (%)':<30}{'SLL':>8}{'HPBW':>8}{'eta_t':>8}{'drop':>8}")
    for name, a in rows:
        pct = " ".join(f"{v:.0f}" for v in np.round(a * 100))
        print(f"{name:<18}{pct:<30}{first_sll(a):8.1f}{hpbw(a):8.2f}"
              f"{eta_t(a):8.3f}{20*np.log10(a.sum()/len(a)):8.2f}")


def main() -> int:
    OUT.mkdir(parents=True, exist_ok=True)
    edge_fourier(); sll_vs_cost(); cheb_map()
    pedestal_trade(); taylor_vs_cheb(); rounding(); cheb_vs_hann()
    phasor_sidelobe(); preset_traces()
    report()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
