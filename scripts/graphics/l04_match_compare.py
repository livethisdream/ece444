#!/usr/bin/env python3
"""L04: the two ways to match 20 - j15 ohm to 50 ohm, compared across frequency.

Design A -- L-match: series 6.3 nH, shunt 3.9 pF.
Design B -- cancel the reactance with 2.39 nH, then a quarter-wave section of
            Z1 = sqrt(50 x 20) = 31.6 ohm.

Both are exact at 1 GHz. The point of the plot is that they are also close in
BANDWIDTH, so bandwidth is not what chooses between them -- the build medium is
(you can print any Z1 on microstrip; you cannot buy 31.6 ohm cable, and a
quarter wave is 4 cm on FR-4 at 1 GHz but 25 m of coax at 2 MHz).

Plotted as S11 in dB, which is what the NanoVNA shows in the matching lab.

    python3 scripts/graphics/l04_match_compare.py
    -> book/extras/slides/fig/L04-match-compare.svg
       book/extras/viz/img/L04-match-compare.svg
"""

from __future__ import annotations
import io, re
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

NAVY, BLUE, RED, GREEN, ORANGE, GREY = "#004a85", "#0067b9", "#b01e24", "#1d7a4d", "#e67e22", "#5a5a5a"
INK, RULE = "#1a1a1a", "#c7d2e0"
ROOT = Path(__file__).resolve().parents[2]
OUTS = [ROOT / "book/extras/slides/fig", ROOT / "book/extras/viz/img"]

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

Z0, F0, R, X0 = 50.0, 1e9, 20.0, -15.0
CL = 1 / (2 * np.pi * F0 * abs(X0))       # load capacitance giving -j15 at f0
LA = 39.5 / (2 * np.pi * F0)              # L-match series inductor
CA = 1 / (2 * np.pi * F0 * 40.8)          # L-match shunt capacitor
LB = abs(X0) / (2 * np.pi * F0)           # cancelling inductor
Z1 = np.sqrt(Z0 * R)                      # quarter-wave line impedance

zload = lambda f: complex(R, -1 / (2 * np.pi * f * CL))
gamma = lambda Z: abs((Z - Z0) / (Z + Z0))


def g_lmatch(f):
    w = 2 * np.pi * f
    Z = zload(f) + 1j * w * LA
    return gamma(1 / (1 / Z + 1j * w * CA))


def g_quarter(f):
    w = 2 * np.pi * f
    ZL = zload(f) + 1j * w * LB
    t = np.tan((np.pi / 2) * (f / F0))
    return gamma(Z1 * (ZL + 1j * Z1 * t) / (Z1 + 1j * ZL * t))


def band(fn, fs):
    ok = fs[np.array([fn(f) for f in fs]) <= 1 / 3.0]
    return ok.min(), ok.max()


def main() -> int:
    fs = np.linspace(0.5e9, 1.5e9, 4001)
    dB = lambda fn: 20 * np.log10(np.clip([fn(f) for f in fs], 1e-4, None))

    bw = {k: band(fn, fs) for k, fn in (("L", g_lmatch), ("Q", g_quarter))}
    bwmhz = {k: (hi - lo) / 1e6 for k, (lo, hi) in bw.items()}

    fig, ax = plt.subplots(figsize=(6.6, 3.9))
    ax.plot(fs / 1e9, dB(g_lmatch), color=NAVY, lw=2.4,
            label=f"L-match, two lumped parts — {bwmhz['L']:.0f} MHz")
    ax.plot(fs / 1e9, dB(g_quarter), color=ORANGE, lw=2.4,
            label=f"cancel, then 31.6 Ω quarter-wave — {bwmhz['Q']:.0f} MHz")

    ax.axhline(-9.54, color=RED, lw=1.3, ls=(0, (5, 4)))
    ax.text(0.52, -8.6, "VSWR = 2", color=RED, fontsize=11.5, fontweight="bold", va="bottom")

    # tick the band edges on the threshold line so the legend numbers are visible
    for k, col in (("L", NAVY), ("Q", ORANGE)):
        for f in bw[k]:
            ax.plot([f / 1e9], [-9.54], marker="|", color=col, ms=11, mew=2.2, zorder=5)

    ax.axvline(1.0, color=GREY, lw=1.1, ls=(0, (3, 3)))
    ax.text(1.012, -2.0, "design\nfrequency", color=GREY, fontsize=10.5, va="top")

    ax.set_xlim(0.5, 1.5); ax.set_ylim(-40, 0)
    ax.set_xlabel("Frequency  (GHz)")
    ax.set_ylabel("Reflection  $S_{11}$  (dB)")
    ax.grid(color=RULE, linewidth=0.8)
    for sp in ("top", "right"):
        ax.spines[sp].set_visible(False)
    ax.legend(loc="lower left", fontsize=11, handlelength=1.8,
              borderpad=0.5, labelspacing=0.4)

    buf = io.StringIO()
    fig.savefig(buf, format="svg", transparent=True, bbox_inches="tight", pad_inches=0.06)
    plt.close(fig)
    s = buf.getvalue()
    s = s[s.index("<svg"):]
    s = re.sub(r"font-family:[^;}]*", "font-family:inherit", s)
    for out in OUTS:
        out.mkdir(parents=True, exist_ok=True)
        (out / "L04-match-compare.svg").write_text(s, encoding="utf-8")
        print(f"wrote {out / 'L04-match-compare.svg'}")

    for name, fn in (("L-match", g_lmatch), ("cancel + quarter-wave", g_quarter)):
        lo, hi = band(fn, fs)
        print(f"  {name:>22}: {lo/1e9:.3f}-{hi/1e9:.3f} GHz "
              f"({(hi-lo)/1e6:.0f} MHz, {(hi-lo)/F0*100:.0f}%)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
