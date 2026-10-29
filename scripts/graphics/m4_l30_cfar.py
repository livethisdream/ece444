#!/usr/bin/env python3
"""Generate the L30 (CFAR processing) lesson-page figures as inline SVG.

  - L30-window      : one row of range cells: the cell under test, its guard
                      cells, its reference cells, and the threshold they set
  - L30-cfar-loss   : the extra SNR a cell-averaging CFAR needs against a
                      known noise power, against the number of reference cells
  - L30-failures    : two profiles where cell averaging goes wrong (a second
                      target in the window, a clutter edge), with the CA, GO
                      and SO thresholds
  - L30-window-2d   : the same window on a range-Doppler grid
  - L30-rd-detections : a synthetic range-Doppler map after MTI, and the cells
                      cfar_2d declares, run with the lesson's own code excerpt

The detector is square law on complex samples, so noise power in a cell is
exponential with mean Pn. The CA bias is alpha = N (Pfa^(-1/N) - 1); the GO
and SO biases solve the Gandhi-Kassam closed forms for Pfa. The figures carry
no equations (house rule).

    python3 scripts/graphics/m4_l30_cfar.py
    -> book/extras/viz/img/L30-*.svg
"""

from __future__ import annotations
import io
from pathlib import Path

import numpy as np
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, FancyArrowPatch
from scipy import signal
from scipy.optimize import brentq
from scipy.special import comb
from scipy.stats import gamma, ncx2
from svg_font_stack import apply_font_stack

NAVY, BLUE, RED, GREEN, ORANGE, GRAY = "#004a85", "#0067b9", "#b01e24", "#1d7a4d", "#e67e22", "#5a5a5a"
INK, RULE = "#1a1a1a", "#c7d2e0"
ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "book/extras/viz/img"

PFA = 1e-6

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


def tidy(ax) -> None:
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.grid(True, color="#e6eef6", lw=0.8)
    ax.set_axisbelow(True)


# ------------------------------------------------------------------ CFAR maths
def db(x):
    return 10 * np.log10(x)


def alpha_ca(n: int, pfa: float = PFA) -> float:
    """CA bias on the mean of n reference cells: Pfa = (1 + alpha/n)^-n."""
    return n * (pfa ** (-1 / n) - 1)


def pfa_so(a: float, n: int) -> float:
    """Smallest-of, n cells a side, threshold a times the smaller half mean."""
    return 2 * sum(comb(n - 1 + k, k) * (2 + a / n) ** (-(n + k)) for k in range(n))


def pfa_go(a: float, n: int) -> float:
    return 2 * (1 + a / n) ** (-n) - pfa_so(a, n)


def alpha_go(n: int, pfa: float = PFA) -> float:
    return brentq(lambda a: np.log(pfa_go(a, n)) - np.log(pfa), 0.1, 2e3)


def alpha_so(n: int, pfa: float = PFA) -> float:
    return brentq(lambda a: np.log(pfa_so(a, n)) - np.log(pfa), 0.1, 2e3)


def pd_ca(snr: float, n: int, pfa: float = PFA) -> float:
    """Pd of a steady target, averaged over the CA noise estimate (Gamma(n))."""
    a = alpha_ca(n, pfa)
    y = np.linspace(gamma.ppf(1e-9, n), gamma.ppf(1 - 1e-9, n), 3001)
    v = ncx2.sf(2 * a * y / n, 2, 2 * snr) * gamma.pdf(y, n)
    return float(np.sum(v) * (y[1] - y[0]))


def required_snr_db(n: int | None, pd: float = 0.9) -> float:
    if n is None:                                   # noise power known
        return brentq(lambda s: ncx2.sf(2 * np.log(1 / PFA), 2, 2 * 10 ** (s / 10)) - pd, 0, 30)
    return brentq(lambda s: pd_ca(10 ** (s / 10), n) - pd, 0, 40)


def noise_cells(rng, n: int, level=1.0) -> np.ndarray:
    x = (rng.standard_normal(n) + 1j * rng.standard_normal(n)) / np.sqrt(2)
    return np.abs(x) ** 2 * level


def cfar_1d(p: np.ndarray, guard: int, ref: int, kind: str = "ca", pfa: float = PFA) -> np.ndarray:
    """Threshold for each interior cell of a power profile; NaN near the ends."""
    n = len(p)
    out = np.full(n, np.nan)
    a = {"ca": alpha_ca(2 * ref, pfa), "go": alpha_go(ref, pfa), "so": alpha_so(ref, pfa)}[kind]
    for i in range(guard + ref, n - guard - ref):
        lo = p[i - guard - ref:i - guard].mean()
        hi = p[i + guard + 1:i + guard + 1 + ref].mean()
        est = {"ca": (lo + hi) / 2, "go": max(lo, hi), "so": min(lo, hi)}[kind]
        out[i] = a * est
    return out


# The lesson's excerpt, verbatim: CA-CFAR on a range-Doppler map in dB.
def cfar_2d(rd_map, guard, ref, bias_db, axes=None):
    P = 10 ** (rd_map / 10)                                  # dB back to power
    (gr, gv), (rr, rv) = guard, ref                          # (range, Doppler) half-widths
    win = np.ones((2 * (gr + rr) + 1, 2 * (gv + rv) + 1))
    win[rr:rr + 2 * gr + 1, rv:rv + 2 * gv + 1] = 0          # guard cells and the cell under test
    def pad(A): return np.pad(np.pad(A, ((0, 0), (gv + rv,) * 2), "wrap"), ((gr + rr,) * 2, (0, 0)))
    total = signal.fftconvolve(pad(P), win, mode="valid")
    count = signal.fftconvolve(pad(np.ones_like(P)), win, mode="valid")
    snr_db = 10 * np.log10(P / (total / count))              # each cell over its local noise
    det = snr_db > bias_db
    r_ax, v_ax = axes or (np.arange(P.shape[0]), np.arange(P.shape[1]))
    hits = [(r_ax[i], v_ax[j], snr_db[i, j]) for i, j in zip(*np.nonzero(det))]
    return det, hits


# -------------------------------------------------------------------- figures
def window() -> None:
    g, r = 2, 4                                   # drawn small enough to read
    cells = np.arange(-(g + r) - 2, g + r + 3)
    fig, ax = plt.subplots(figsize=(6.8, 2.3))
    for c in cells:
        d = abs(c)
        if d == 0:
            fc, ec = RED, RED
        elif d <= g:
            fc, ec = "#e3e7ec", "#8a929c"
        elif d <= g + r:
            fc, ec = "#cfe0f1", NAVY
        else:
            fc, ec = "white", "#c7d2e0"
        ax.add_patch(Rectangle((c - 0.45, 0), 0.9, 1, fc=fc, ec=ec, lw=1.2))
    ax.text(0, 1.3, "cell under test", color=RED, ha="center", fontsize=12.5, weight="bold")
    top = 2.0
    for sgn in (-1, 1):
        ax.text(sgn * (g + 1) / 2, -0.45, "guard", color=GRAY, ha="center", fontsize=12)
        mid = sgn * (g + (r + 1) / 2)
        ax.text(mid, -0.45, "reference", color=NAVY, ha="center", fontsize=12)
        ax.plot([mid, mid], [1.05, top], color=NAVY, lw=1.1)
    ax.plot([-(g + (r + 1) / 2), g + (r + 1) / 2], [top, top], color=NAVY, lw=1.1)
    ax.text(0, top + 0.3, "average × bias = the threshold the cell under test must cross",
            color=NAVY, ha="center", fontsize=12.5)
    ax.text(cells[-1] + 0.9, 0.5, "range", color=GRAY, va="center", fontsize=12)
    ax.annotate("", xy=(cells[-1] + 0.85, 0.12), xytext=(cells[-1] + 0.2, 0.12),
                arrowprops=dict(arrowstyle="->", color=GRAY, lw=1))
    ax.set_xlim(cells[0] - 0.7, cells[-1] + 2.2)
    ax.set_ylim(-0.8, 2.75)
    ax.set_aspect("equal")
    ax.axis("off")
    finalize(fig, "L30-window")


def cfar_loss() -> None:
    ideal = required_snr_db(None)
    ns = np.array([4, 6, 8, 12, 16, 24, 32, 48, 64, 96, 128, 192, 256])
    loss = np.array([required_snr_db(int(n)) - ideal for n in ns])
    fig, ax = plt.subplots(figsize=(6.4, 3.0))
    ax.plot(ns, loss, color=NAVY, lw=2.2)
    for n in (16, 32, 144):
        L = required_snr_db(n) - ideal
        ax.plot(n, L, "o", color=RED, ms=6)
        ax.annotate(f"{n} cells, {L:.1f} dB", (n, L), xytext=(8, 6),
                    textcoords="offset points", color=RED, fontsize=12)
    ax.set_xscale("log")
    ax.set_xticks([4, 8, 16, 32, 64, 128, 256])
    ax.set_xticklabels(["4", "8", "16", "32", "64", "128", "256"])
    ax.set_xlim(4, 300)
    ax.set_ylim(0, 8)
    ax.set_xlabel("reference cells")
    ax.set_ylabel("extra SNR needed (dB)")
    tidy(ax)
    finalize(fig, "L30-cfar-loss")
    print(f"  known-noise SNR for Pd 0.9: {ideal:.2f} dB; loss at 16/32/144: "
          + ", ".join(f"{required_snr_db(n) - ideal:.2f}" for n in (16, 32, 144)))


def target(p: np.ndarray, rng, k: int, snr_db: float) -> None:
    """Add a steady target at cell k with a Hann window's -6 dB neighbors."""
    s = np.sqrt(10 ** (snr_db / 10))
    for d, h in ((-1, 0.5), (0, 1.0), (1, 0.5)):
        x = (rng.standard_normal() + 1j * rng.standard_normal()) / np.sqrt(2)
        p[k + d] = abs(x + h * s) ** 2


def failures() -> None:
    g, r = 2, 16
    fig, axes = plt.subplots(1, 2, figsize=(10.4, 3.2), sharey=True)

    # (a) masking: a strong target eight cells from a weaker one
    rng = np.random.default_rng(11)
    n = 120
    p = noise_cells(rng, n)
    target(p, rng, 52, 18.0)
    target(p, rng, 60, 24.0)
    ax = axes[0]
    ax.plot(np.arange(n), db(p), color=NAVY, lw=0.8)
    for kind, col, ls in (("ca", GREEN, "-"), ("so", ORANGE, "--")):
        t = cfar_1d(p, g, r, kind)
        ax.plot(np.arange(n), db(t), color=col, lw=1.8, ls=ls)
        print(f"  masking {kind}: weak target {db(p[52]):.1f} dB vs threshold {db(t[52]):.1f} dB")
    ax.annotate("18 dB", (52, db(p[52])), xytext=(36, 6), color=NAVY, fontsize=11.5, ha="right",
                bbox=dict(fc="white", ec="none", pad=1.0),
                arrowprops=dict(arrowstyle="-", color=NAVY, lw=0.9))
    ax.annotate("24 dB", (60, db(p[60])), xytext=(90, 27), color=NAVY, fontsize=11.5,
                arrowprops=dict(arrowstyle="-", color=NAVY, lw=0.9))
    ax.text(2, -17, "cell averaging", color=GREEN, fontsize=12, bbox=dict(fc="white", ec="none", pad=1.0))
    ax.text(2, -22.5, "smallest-of", color=ORANGE, fontsize=12, bbox=dict(fc="white", ec="none", pad=1.0))
    ax.set_title("a second target in the window", fontsize=13, color=INK)
    ax.set_xlim(0, n)
    ax.set_ylim(-25, 32)
    ax.set_xlabel("range cell")
    ax.set_ylabel("power (dB)")
    tidy(ax)

    # (b) clutter edge: noise rises 15 dB at cell 60
    rng = np.random.default_rng(5)
    level = np.ones(n)
    level[60:] = 10 ** 1.5
    p = noise_cells(rng, n, level)
    ax = axes[1]
    ax.plot(np.arange(n), db(p), color=NAVY, lw=0.8)
    for kind, col, ls in (("ca", GREEN, "-"), ("go", RED, "--")):
        t = cfar_1d(p, g, r, kind)
        ax.plot(np.arange(n), db(t), color=col, lw=1.8, ls=ls)
        fa = np.nansum(p > t)
        print(f"  clutter edge {kind}: {fa} crossings")
        if kind == "ca":
            hit = np.where(p > t)[0]
            ax.plot(hit, db(p[hit]), "o", color=RED, ms=4.5)
    ax.axvline(60, color=GRAY, lw=0.9, ls=":")
    ax.text(63, -22, "clutter 15 dB higher", color=GRAY, fontsize=12)
    ax.text(2, -17, "cell averaging", color=GREEN, fontsize=12, bbox=dict(fc="white", ec="none", pad=1.0))
    ax.text(2, -22.5, "greatest-of", color=RED, fontsize=12, bbox=dict(fc="white", ec="none", pad=1.0))
    ax.set_title("a clutter edge", fontsize=13, color=INK)
    ax.set_xlim(0, n)
    ax.set_xlabel("range cell")
    tidy(ax)
    fig.tight_layout(w_pad=1.5)
    finalize(fig, "L30-failures")


def window_2d() -> None:
    gr, gv, rr, rv = 2, 2, 4, 4
    R, V = gr + rr + 1, gv + rv + 1
    fig, ax = plt.subplots(figsize=(4.6, 4.2))
    for i in range(-R, R + 1):
        for j in range(-V, V + 1):
            di, dj = abs(i), abs(j)
            if di == 0 and dj == 0:
                fc = RED
            elif di <= gr and dj <= gv:
                fc = "#e3e7ec"
            elif di <= gr + rr and dj <= gv + rv:
                fc = "#cfe0f1"
            else:
                fc = "white"
            ax.add_patch(Rectangle((j - 0.5, i - 0.5), 1, 1, fc=fc, ec="#c7d2e0", lw=0.8))
    ax.add_patch(Rectangle((-gv - 0.5, -gr - 0.5), 2 * gv + 1, 2 * gr + 1, fc="none", ec=GRAY, lw=1.6))
    ax.add_patch(Rectangle((-gv - rv - 0.5, -gr - rr - 0.5), 2 * (gv + rv) + 1, 2 * (gr + rr) + 1,
                           fc="none", ec=NAVY, lw=1.8))
    ax.text(0, R + 0.8, "144 reference cells", color=NAVY, ha="center", fontsize=12.5)
    ax.text(0, -R - 1.3, "Doppler cell", color=GRAY, ha="center", fontsize=12)
    ax.text(-V - 1.3, 0, "range cell", color=GRAY, ha="center", va="center", rotation=90, fontsize=12)
    ax.set_xlim(-V - 2.0, V + 0.6)
    ax.set_ylim(-R - 2.0, R + 1.6)
    ax.set_aspect("equal")
    ax.axis("off")
    finalize(fig, "L30-window-2d")


def rd_detections() -> None:
    """A synthetic map with the M8 burst's axes, after a 2-pulse canceller."""
    rng = np.random.default_rng(4)
    nr, nv = 64, 256                               # 0.30 m cells to 19 m; 256 Doppler cells
    r_ax = np.arange(nr) * 0.30
    v_ax = (np.arange(nv) - nv // 2) * (30.0 / nv)  # +/-15 m/s
    x = (rng.standard_normal((nr, nv)) + 1j * rng.standard_normal((nr, nv))) / np.sqrt(2)
    P = np.abs(x) ** 2
    # clutter left over at zero Doppler after MTI, stronger near the radar
    c0 = nv // 2
    for d, h in ((-1, 0.5), (0, 1.0), (1, 0.5)):
        P[:, c0 + d] *= 1 + 10 ** (np.clip(12 - 0.6 * np.arange(nr), 0, None) / 10) * h ** 2
    # a walker at 6.0 m, +1.2 m/s, and a hand at 2.1 m, -0.6 m/s (Hann main lobe)
    for rr_m, vv, snr in ((6.0, 1.2, 26.0), (2.1, -0.6, 22.0)):
        i, j = int(round(rr_m / 0.30)), int(round(vv / (30.0 / nv))) + c0
        s = 10 ** (snr / 10)
        for di, hi in ((-1, 0.5), (0, 1.0), (1, 0.5)):
            for dj, hj in ((-1, 0.5), (0, 1.0), (1, 0.5)):
                P[i + di, j + dj] += s * (hi * hj) ** 2
    rd = db(P)
    det, hits = cfar_2d(rd, (2, 2), (4, 4), db(alpha_ca(144)), axes=(r_ax, v_ax))
    print(f"  rd map: {len(hits)} detections; bias {db(alpha_ca(144)):.2f} dB")

    fig, ax = plt.subplots(figsize=(6.6, 3.4))
    im = ax.imshow(rd, origin="lower", aspect="auto", cmap="Blues", vmin=-5, vmax=30,
                   extent=(v_ax[0], v_ax[-1], r_ax[0], r_ax[-1]))
    ii, jj = np.nonzero(det)
    ax.plot(v_ax[jj], r_ax[ii], "s", ms=4.5, mfc="none", mec=RED, mew=1.2)
    ax.set_xlim(-3, 3)
    ax.set_ylim(0, 9)
    ax.set_xlabel("velocity (m/s)")
    ax.set_ylabel("range (m)")
    cb = fig.colorbar(im, ax=ax, pad=0.02)
    cb.set_label("power (dB)")
    cb.outline.set_edgecolor("#8a929c")
    finalize(fig, "L30-rd-detections")


def main() -> int:
    OUT.mkdir(parents=True, exist_ok=True)
    for n in (16, 32, 144):
        print(f"  CA bias, {n} cells: {db(alpha_ca(n)):.2f} dB")
    for n in (16,):
        print(f"  {n} a side: GO {db(alpha_go(n)):.2f} dB, SO {db(alpha_so(n)):.2f} dB")
    window()
    cfar_loss()
    failures()
    window_2d()
    rd_detections()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
