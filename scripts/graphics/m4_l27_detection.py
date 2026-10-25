#!/usr/bin/env python3
"""Generate the L27 (radar detection) lesson-page figures as inline SVG.

  - L27-range-profile    : one range profile of noise power, a target 13 dB
                           above the mean noise, and the Pfa = 1e-6 threshold
  - L27-pdfs             : noise-only and target-plus-noise densities on a dB
                           axis, threshold and the Pd area marked
  - L27-roc              : Pd against Pfa for four SNRs (steady target)
  - L27-integration-gain : coherent and noncoherent integration gain against N
  - L27-fixed-threshold  : a profile whose noise rises 6 dB part way out, with
                           a fixed threshold and a local-average threshold

The detector is square law on complex samples, so noise power in a cell is
exponential with mean Pn and a steady target gives a Rician envelope. Pd comes
from the noncentral chi-square survival function (Marcum Q); the noncoherent
curve is Albersheim's equation. The figures carry no equations (house rule).

    python3 scripts/graphics/m4_l27_detection.py
    -> book/extras/viz/img/L27-*.svg
"""

from __future__ import annotations
import io
from pathlib import Path

import numpy as np
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from scipy.special import i0e
from scipy.stats import chi2, ncx2
from svg_font_stack import apply_font_stack

NAVY, BLUE, RED, GREEN, ORANGE, GRAY = "#004a85", "#0067b9", "#b01e24", "#1d7a4d", "#e67e22", "#5a5a5a"
INK, RULE = "#1a1a1a", "#c7d2e0"
ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "book/extras/viz/img"

PFA = 1e-6
SNR_DB = 13.0                     # the lesson's running example

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


# ------------------------------------------------------------- detection maths
def db(x):
    return 10 * np.log10(x)


def threshold(pfa: float) -> float:
    """Threshold on |x|^2 / Pn for one square-law sample."""
    return np.log(1 / pfa)


def pd_steady(snr: float, pfa: float, n: int = 1) -> float:
    """Pd for n noncoherently summed square-law samples of a steady target."""
    t = chi2.isf(pfa, 2 * n)
    return ncx2.sf(t, 2 * n, 2 * n * snr)


def albersheim(pd: float, pfa: float, n: int = 1) -> float:
    """Required single-pulse SNR (dB), n pulses integrated noncoherently."""
    a = np.log(0.62 / pfa)
    b = np.log(pd / (1 - pd))
    return -5 * np.log10(n) + (6.2 + 4.54 / np.sqrt(n + 0.44)) * np.log10(a + 0.12 * a * b + 1.7 * b)


def pdf_db(y_db: np.ndarray, snr: float) -> np.ndarray:
    """Density of 10 log10(|x|^2/Pn) for noise (snr = 0) or target + noise."""
    z = 10 ** (y_db / 10)
    jac = np.log(10) / 10 * z
    if snr == 0:
        return jac * np.exp(-z)
    arg = 2 * np.sqrt(snr * z)
    return jac * np.exp(-(np.sqrt(z) - np.sqrt(snr)) ** 2) * i0e(arg)


def noise_cells(rng, n: int, level: np.ndarray | float = 1.0) -> np.ndarray:
    """|x|^2 of complex Gaussian noise with mean power `level`."""
    x = (rng.standard_normal(n) + 1j * rng.standard_normal(n)) / np.sqrt(2)
    return np.abs(x) ** 2 * level


# -------------------------------------------------------------------- figures
def range_profile() -> None:
    rng = np.random.default_rng(7)
    n = 200
    p = noise_cells(rng, n)
    k = 132                                    # the target's cell
    s = 10 ** (SNR_DB / 10)
    x = (rng.standard_normal() + 1j * rng.standard_normal()) / np.sqrt(2) + np.sqrt(s)
    p[k] = abs(x) ** 2
    T = threshold(PFA)

    fig, ax = plt.subplots(figsize=(6.6, 2.9))
    ax.vlines(np.arange(n), -25, db(p), color=NAVY, lw=1.1)
    ax.plot(np.arange(n), db(p), "o", ms=2.2, color=NAVY)
    ax.axhline(db(T), color=RED, lw=1.6, ls="--")
    ax.axhline(0, color=GRAY, lw=1.0, ls=":")
    ax.text(3, db(T) + 0.8, "threshold, 11.4 dB", color=RED, fontsize=12)
    ax.text(n + 4, 0, "mean\nnoise", color=GRAY, fontsize=11.5, va="center", clip_on=False)
    ax.annotate("target", (k, db(p[k])), xytext=(k + 14, db(p[k]) + 1.5),
                color=NAVY, fontsize=12, arrowprops=dict(arrowstyle="-", color=NAVY, lw=0.9))
    ax.set_xlim(-2, n + 1)
    ax.set_ylim(-25, 20)
    ax.set_xlabel("range cell")
    ax.set_ylabel("power above mean noise (dB)")
    tidy(ax)
    finalize(fig, "L27-range-profile")


def pdfs() -> None:
    y = np.linspace(-25, 22, 1200)
    s = 10 ** (SNR_DB / 10)
    pn, ps = pdf_db(y, 0), pdf_db(y, s)
    Tdb = db(threshold(PFA))

    fig, ax = plt.subplots(figsize=(6.6, 3.0))
    ax.plot(y, pn, color=GRAY, lw=2.0)
    ax.plot(y, ps, color=NAVY, lw=2.2)
    m = y >= Tdb
    ax.fill_between(y[m], 0, ps[m], color=NAVY, alpha=0.18, lw=0)
    ax.axvline(Tdb, color=RED, lw=1.6, ls="--")
    top = ps.max()
    ax.text(Tdb - 0.4, 1.02 * top, "threshold", color=RED, fontsize=12, ha="right")
    ax.text(0, pn.max() + 0.02 * top, "noise only", color=GRAY, fontsize=12, ha="center", va="bottom")
    ax.text(16.6, 0.62 * top, "target + noise", color=NAVY, fontsize=12, ha="left")
    ax.text(16.6, 0.45 * top, "Pd = 0.87", color=NAVY, fontsize=12, ha="left")
    ax.text(16.6, 0.14 * top, "Pfa = 10⁻⁶,\ntoo small to see", color=GRAY, fontsize=11, ha="left")
    ax.set_xlim(-25, 26)
    ax.set_ylim(0, 1.12 * top)
    ax.set_yticks([])
    ax.set_xlabel("power in the cell, above mean noise (dB)")
    ax.set_ylabel("probability density")
    tidy(ax)
    finalize(fig, "L27-pdfs")


def roc() -> None:
    pfa = np.logspace(-10, -1, 300)
    fig, ax = plt.subplots(figsize=(6.4, 3.4))
    for snr_db, c in [(8, "#9aa7b4"), (10, BLUE), (12, NAVY), (14, GREEN)]:
        pd = [pd_steady(10 ** (snr_db / 10), f) for f in pfa]
        ax.semilogx(pfa, pd, color=c, lw=2.0)
        pd = np.asarray(pd)
        j = np.argmax(pd >= 0.5) if pd[0] < 0.5 else np.searchsorted(pfa, 3e-10)
        ax.text(pfa[j] * 1.5, pd[j] - 0.03, f"{snr_db} dB", color=c, fontsize=12, ha="left", va="top",
                bbox=dict(fc="white", ec="none", pad=0.6))
    ax.axvline(PFA, color=RED, lw=1.2, ls="--")
    ax.plot([PFA], [pd_steady(10 ** 1.2, PFA)], "o", color=NAVY, ms=6)
    ax.text(PFA * 1.6, 0.04, "Pfa = 10⁻⁶", color=RED, fontsize=12)
    ax.set_xlim(1e-10, 1e-1)
    ax.set_ylim(0, 1.02)
    ax.set_xlabel("probability of false alarm")
    ax.set_ylabel("probability of detection")
    tidy(ax)
    finalize(fig, "L27-roc")


def integration_gain() -> None:
    n = np.unique(np.round(np.logspace(0, 2.5, 120)).astype(int))
    coh = db(n)
    nonc = albersheim(0.9, PFA) - albersheim(0.9, PFA, n)
    fig, ax = plt.subplots(figsize=(6.4, 3.2))
    ax.semilogx(n, coh, color=NAVY, lw=2.2)
    ax.semilogx(n, nonc, color=ORANGE, lw=2.2)
    for k in (16, 64):
        g = albersheim(0.9, PFA) - albersheim(0.9, PFA, k)
        ax.plot([k, k], [g, db(k)], "o", color=GRAY, ms=4)
        ax.text(k * 1.15, (g + db(k)) / 2, f"{db(k) - g:.1f} dB", color=GRAY, fontsize=11.5, va="center")
    ax.text(5, db(5) + 1.6, "coherent", color=NAVY, fontsize=12, ha="right")
    ax.text(12, 4.0, "noncoherent", color=ORANGE, fontsize=12, ha="left")
    ax.set_xlim(1, 320)
    ax.set_ylim(0, 26)
    ax.set_xlabel("pulses integrated, N")
    ax.set_ylabel("integration gain (dB)")
    tidy(ax)
    finalize(fig, "L27-integration-gain")


def fixed_threshold() -> None:
    rng = np.random.default_rng(3)
    n = 600
    level = np.ones(n)
    level[330:] = 10 ** 0.6                   # noise rises 6 dB beyond cell 330
    p = noise_cells(rng, n, level)
    T = threshold(PFA)
    # local-average threshold: 16 reference cells each side, 2 guard cells
    nref, ng = 16, 2
    alpha = 2 * nref * (PFA ** (-1 / (2 * nref)) - 1)
    loc = np.full(n, np.nan)
    for i in range(nref + ng, n - nref - ng):
        ref = np.r_[p[i - ng - nref:i - ng], p[i + ng + 1:i + ng + 1 + nref]]
        loc[i] = alpha * ref.mean()

    fig, ax = plt.subplots(figsize=(6.6, 3.0))
    ax.plot(np.arange(n), db(p), color=NAVY, lw=0.7)
    hits = db(p) > db(T)
    ax.plot(np.arange(n)[hits], db(p)[hits], "o", color=RED, ms=4.5)
    ax.axhline(db(T), color=RED, lw=1.6, ls="--")
    ax.plot(np.arange(n), db(loc), color=GREEN, lw=1.8)
    ax.text(30, 6.0, "fixed threshold", color=RED, fontsize=12,
            bbox=dict(fc="white", ec="none", pad=1.0))
    ax.text(n - 4, 27.5, "local-average threshold", color=GREEN, fontsize=12, ha="right")
    ax.text(345, -22, "noise 6 dB higher", color=GRAY, fontsize=12)
    ax.axvline(330, color=GRAY, lw=0.9, ls=":")
    ax.set_xlim(0, n)
    ax.set_ylim(-25, 30)
    ax.set_xlabel("range cell")
    ax.set_ylabel("power (dB)")
    tidy(ax)
    finalize(fig, "L27-fixed-threshold")
    print(f"  fixed-threshold crossings: {hits.sum()}, alpha = {db(alpha):.2f} dB")


def main() -> int:
    OUT.mkdir(parents=True, exist_ok=True)
    range_profile()
    pdfs()
    roc()
    integration_gain()
    fixed_threshold()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
