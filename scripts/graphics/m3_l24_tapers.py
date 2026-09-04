#!/usr/bin/env python3
"""Generate the L24 (Sidelobes and Tapering Theory) deck figures as inline SVG.

  - L24-edge-fourier   : aperture illumination (sharp vs smooth edge) and the
                         pattern each one produces -- why sidelobes exist
  - L24-taper-shapes   : the 8 element amplitudes for four tapers, as stems
  - L24-taper-patterns : uniform / Chebyshev -30 dB / Hann patterns on one axis
  - L24-sll-vs-cost    : the Dolph trade curve -- HPBW and taper efficiency
                         against design sidelobe level, named tapers marked

Every number here is computed from the same formulas the lesson page and the
taper-explorer widget use: N = 8, d/lambda = 0.481 (10.3 GHz, d = 14 mm).
Deck figures carry no equations -- words, numbers and axis labels only.

    python3 scripts/graphics/m3_l24_tapers.py
    -> book/extras/slides/fig/L24-*.svg
"""

from __future__ import annotations
import io, re
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

NAVY, BLUE, RED, GREEN, ORANGE, GRAY = "#004a85", "#0067b9", "#b01e24", "#1d7a4d", "#e67e22", "#5a5a5a"
INK, RULE = "#1a1a1a", "#c7d2e0"
OUT = Path(__file__).resolve().parents[2] / "book/extras/slides/fig"

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
    s = re.sub(r"font-family:[^;}]*", "font-family:inherit", s)
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
    finalize(fig, "L24-edge-fourier")


def taper_shapes() -> None:
    """Four tapers as element-amplitude stems, at the numbers a student types
    into the Element Gains column."""
    sets = [("Uniform", np.ones(N), NAVY),
            ("Chebyshev −30 dB", dolph(30), GREEN),
            ("Hann", hann(), ORANGE),
            ("Blackman", BLACKMAN, RED)]
    fig, axes = plt.subplots(2, 2, figsize=(9.4, 5.4), sharey=True, sharex=True)
    axes = axes.ravel()
    x = np.arange(1, N + 1)
    for ax, (name, a, col) in zip(axes, sets):
        pct = np.round(a * 100).astype(int)
        ax.vlines(x, 0, pct, color=col, lw=3.4)
        ax.plot(x, pct, "o", color=col, ms=7)
        for xi, v in zip(x, pct):
            ax.text(xi, v + 5, str(v), color=col, fontsize=11, ha="center",
                    va="bottom", fontweight="bold")
        ax.set_title(name, color=col, fontsize=13.5, fontweight="bold", pad=6)
        ax.set_xlim(0.4, N + 0.6); ax.set_ylim(0, 126)
        ax.set_xticks(x); ax.set_xticklabels([str(i) for i in x], fontsize=10)
        ax.grid(color=RULE, linewidth=0.8, axis="y")
        for sp in ("top", "right"):
            ax.spines[sp].set_visible(False)
    for ax in axes[2:]:
        ax.set_xlabel("Element")
    for ax in (axes[0], axes[2]):
        ax.set_ylabel("Element gain  (%)")
        ax.set_yticks([0, 25, 50, 75, 100])
    fig.subplots_adjust(hspace=0.34, wspace=0.14)
    finalize(fig, "L24-taper-shapes")


def taper_patterns() -> None:
    """The same three tapers as patterns, with the equal-ripple floor of the
    Chebyshev design visible against the decaying uniform sidelobes."""
    fig, ax = plt.subplots(figsize=(8.6, 4.2))
    for name, a, col, lw in [("Uniform", np.ones(N), NAVY, 2.4),
                             ("Chebyshev −30 dB", dolph(30), GREEN, 2.2),
                             ("Hann", hann(), ORANGE, 2.2)]:
        ax.plot(TH, pattern_db(a), color=col, lw=lw,
                label=f"{name}   {hpbw(a):.1f}° wide")
    ax.set_xlim(-90, 90); ax.set_ylim(-60, 4)
    ax.set_xticks(range(-90, 91, 15))
    ax.set_xlabel("Angle from broadside  (deg)")
    ax.set_ylabel("Relative power  (dB)")
    ax.grid(color=RULE, linewidth=0.8)
    for sp in ("top", "right"):
        ax.spines[sp].set_visible(False)
    ax.axhline(-30, color=GREEN, lw=1.1, ls=(0, (4, 3)))
    ax.axhline(-12.8, color=NAVY, lw=1.1, ls=(0, (4, 3)))
    ax.text(-88, -11.4, "−12.8 dB", color=NAVY, fontsize=11.5, fontweight="bold",
            ha="left", va="bottom")
    ax.text(-88, -28.6, "−30 dB", color=GREEN, fontsize=11.5, fontweight="bold",
            ha="left", va="bottom")
    ax.legend(loc="lower center", bbox_to_anchor=(0.5, -0.30), ncol=3,
              fontsize=11.5, handlelength=1.6, columnspacing=1.5)
    finalize(fig, "L24-taper-patterns")


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
    finalize(fig, "L24-sll-vs-cost")


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
    edge_fourier(); taper_shapes(); taper_patterns(); sll_vs_cost()
    report()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
