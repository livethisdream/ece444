#!/usr/bin/env python3
"""L04: the L-match drawn as two moves on the Smith chart.

The worked example on the deck and the lesson page is a 20 - j15 ohm antenna on
a 50 ohm line. Normalized, z_L = 0.4 - j0.3. The two design moves are:

  1. series inductor  -> walk clockwise along the constant-RESISTANCE circle
     r = 0.4 until it crosses the unit-conductance (g = 1) circle, at
     z = 0.4 + j0.49. The reactance added is (0.49 + 0.30) x 50 = +39.5 ohms.
  2. shunt capacitor  -> walk along that constant-CONDUCTANCE circle into the
     center. The susceptance added is 1.225/50 S, i.e. 3.9 pF at 1 GHz.

Those are the same numbers the algebra gives, which is the point of the slide.

Deck figures carry no equations -- labels here are words and plain numbers only.

    python3 scripts/graphics/l04_lmatch_smith.py
    -> book/extras/slides/fig/L04-lmatch-smith.svg
       book/extras/viz/img/L04-lmatch-smith.svg
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
ROOT = Path(__file__).resolve().parents[2]
OUTS = [ROOT / "book/extras/slides/fig", ROOT / "book/extras/viz/img"]

plt.rcParams.update({
    "svg.fonttype": "none",
    "font.size": 13,
    "text.color": INK,
    "legend.frameon": False,
})

G = lambda z: (z - 1) / (z + 1)          # impedance -> reflection coefficient


def smith_grid(ax):
    """Constant-r circles and constant-x arcs, clipped to the unit circle."""
    th = np.linspace(0, 2 * np.pi, 720)
    rim = plt.Circle((0, 0), 1.0, transform=ax.transData, facecolor="none")
    for r in (0.2, 0.5, 1.0, 2.0, 5.0):
        c, rad = r / (1 + r), 1 / (1 + r)
        ax.plot(c + rad * np.cos(th), rad * np.sin(th), color=RULE, lw=0.9, zorder=1)
    for x in (0.2, 0.5, 1.0, 2.0, 5.0):
        for s in (+1, -1):
            rad = 1.0 / x
            line, = ax.plot(1.0 + rad * np.cos(th), s / x + rad * np.sin(th),
                            color=RULE, lw=0.9, zorder=1)
            line.set_clip_path(rim)          # keep only what falls inside the rim
    ax.plot(np.cos(th), np.sin(th), color="#7fa8c9", lw=1.5, zorder=2)
    ax.plot([-1, 1], [0, 0], color="#b9d2e5", lw=1.2, zorder=2)


def main() -> int:
    Z0, RL, XL = 50.0, 20.0, -15.0
    r = RL / Z0                                   # 0.4
    x0 = XL / Z0                                  # -0.3
    x1 = np.sqrt(r - r * r)                       # where r-circle meets g = 1
    y_mid = 1 / complex(r, x1)                    # g = 1, b = -1.225

    fig, ax = plt.subplots(figsize=(7.6, 5.0))
    smith_grid(ax)

    # move 1: series inductor, clockwise along constant resistance r
    xs = np.linspace(x0, x1, 400)
    p1 = G(r + 1j * xs)
    ax.plot(p1.real, p1.imag, color=NAVY, lw=3.0, zorder=4, solid_capstyle="round")

    # move 2: shunt capacitor, along constant conductance g = 1 into the center
    bs = np.linspace(y_mid.imag, 0.0, 400)
    p2 = G(1 / (1 + 1j * bs))
    ax.plot(p2.real, p2.imag, color=GREEN, lw=3.0, zorder=4, solid_capstyle="round")

    # arrowheads mid-path so the direction of travel is unmistakable
    for p, col in ((p1, NAVY), (p2, GREEN)):
        i = len(p) // 2
        ax.annotate("", xy=(p[i + 6].real, p[i + 6].imag), xytext=(p[i].real, p[i].imag),
                    arrowprops=dict(arrowstyle="-|>", color=col, lw=0, mutation_scale=22),
                    zorder=5)

    start, mid, end = G(complex(r, x0)), G(complex(r, x1)), 0 + 0j
    # offsets pull the labels INWARD -- placed outward their left edges ran
    # across the rim of the chart
    for pt, col, lab, off in ((start, RED, "start: the antenna", (0.34, -0.20)),
                              (mid, ORANGE, "after the series inductor", (0.38, 0.20)),
                              (end, GREEN, "matched", (0.16, -0.17))):
        ax.plot(pt.real, pt.imag, "o", color=col, ms=9, zorder=6,
                markeredgecolor="white", markeredgewidth=1.4)
        ax.annotate(lab, xy=(pt.real, pt.imag),
                    xytext=(pt.real + off[0], pt.imag + off[1]),
                    color=col, fontsize=11, fontweight="bold",
                    ha="center", va="center", zorder=6,
                    bbox=dict(boxstyle="round,pad=0.18", fc="white", ec="none", alpha=0.92),
                    arrowprops=dict(arrowstyle="-", color=col, lw=1.0))

    # legend to the RIGHT of the chart, clear of the circle entirely.
    # No swatches -- the text color matches its arc, which is enough.
    lx = 1.20
    ax.text(lx, 0.30, "series element walks a\nconstant-resistance circle",
            color=NAVY, fontsize=11, fontweight="bold", ha="left", va="top")
    ax.text(lx, -0.16, "shunt element walks a\nconstant-conductance circle",
            color=GREEN, fontsize=11, fontweight="bold", ha="left", va="top")

    ax.set_xlim(-1.10, 2.32); ax.set_ylim(-1.14, 1.14)
    ax.set_aspect("equal"); ax.axis("off")

    buf = io.StringIO()
    fig.savefig(buf, format="svg", transparent=True, bbox_inches="tight", pad_inches=0.04)
    plt.close(fig)
    s = buf.getvalue()
    s = s[s.index("<svg"):]
    s = re.sub(r"font-family:[^;}]*", "font-family:inherit", s)
    for out in OUTS:
        out.mkdir(parents=True, exist_ok=True)
        (out / "L04-lmatch-smith.svg").write_text(s, encoding="utf-8")
        print(f"wrote {out / 'L04-lmatch-smith.svg'}")

    # echo the numbers the slide quotes, so the figure and the text cannot drift
    print(f"\ncheck: series reactance = {(x1 - x0) * Z0:+.1f} ohms "
          f"-> L = {(x1 - x0) * Z0 / (2 * np.pi * 1e9) * 1e9:.1f} nH at 1 GHz")
    print(f"       shunt susceptance = {-y_mid.imag / Z0:.5f} S "
          f"-> C = {-y_mid.imag / Z0 / (2 * np.pi * 1e9) * 1e12:.1f} pF at 1 GHz")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
