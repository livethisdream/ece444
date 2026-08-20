#!/usr/bin/env python3
"""Generate the L05 (Field Regions) deck data-plot as inline SVG.

L05:
  - L05-term-crossover : the three field terms of an infinitesimal dipole
                         (1/kr radiation, 1/(kr)^2 induction, 1/(kr)^3
                         electrostatic) on log-log axes, all crossing at
                         kr = 1, with the kr >> 1 region shaded.

Exported as SVG with live <text> (svg.fonttype='none'), then font-family is
rewritten to 'inherit' so the injected figure picks up the deck's Source Sans
Pro. Transparent background, USAFA palette, no baked formulas (axis labels /
legends / annotations only).

    python scripts/graphics/l05_regions.py
    -> writes book/extras/slides/fig/L05-term-crossover.svg

The curves are the exact bracket terms of the infinitesimal-dipole field,
normalized so that all three equal 1 at kr = 1.
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
OUT = Path(__file__).resolve().parents[2] / "book/extras/slides/fig"

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


def finalize(fig, name: str) -> None:
    buf = io.StringIO()
    fig.savefig(buf, format="svg", transparent=True, bbox_inches="tight", pad_inches=0.06)
    plt.close(fig)
    s = buf.getvalue()
    s = s[s.index("<svg"):]                                      # drop xml decl/doctype
    s = re.sub(r"font-family:[^;}]*", "font-family:inherit", s)  # inherit deck font
    (OUT / f"{name}.svg").write_text(s, encoding="utf-8")
    print(f"wrote {OUT / (name + '.svg')}")


def term_crossover() -> None:
    """Straight lines of slope -1, -2, -3 on log-log axes, normalized to meet
    at kr = 1. Left of the meeting point the stored terms run away; right of
    it they fall off the bottom of the plot and only radiation is left."""
    kr = np.logspace(np.log10(0.1), np.log10(20.0), 900)
    rad = 1.0 / kr
    ind = 1.0 / kr ** 2
    est = 1.0 / kr ** 3

    fig, ax = plt.subplots(figsize=(6.6, 4.0))

    # the two halves of the story, as background
    ax.axvspan(0.1, 1.0, color=RED, alpha=0.055, lw=0, zorder=0)
    ax.axvspan(3.0, 20.0, color=RULE, alpha=0.45, lw=0, zorder=0)

    ax.loglog(kr, est, color=ORANGE, lw=2.4, label="electrostatic  (1/r³)", zorder=3)
    ax.loglog(kr, ind, color=GREEN, lw=2.4, label="induction  (1/r²)", zorder=3)
    ax.loglog(kr, rad, color=NAVY, lw=2.8, label="radiation  (1/r)", zorder=4)

    ax.set_xlim(0.1, 20.0)
    ax.set_ylim(2e-4, 2e3)
    ax.set_xlabel("Electrical distance  kr")
    ax.set_ylabel("Relative size of the term")
    ax.set_xticks([0.1, 0.2, 0.5, 1.0, 2.0, 5.0, 10.0, 20.0])
    ax.set_xticklabels(["0.1", "0.2", "0.5", "1", "2", "5", "10", "20"])
    ax.grid(color=RULE, linewidth=0.8, which="major")
    for sp in ("top", "right"):
        ax.spines[sp].set_visible(False)

    # the crossover itself
    ax.axvline(1.0, color=GREY, lw=1.4, ls=(0, (4, 3)), zorder=2)
    ax.plot(1.0, 1.0, "o", color=RED, ms=9, zorder=6)
    ax.annotate("all three equal here", xy=(1.0, 1.0), xytext=(1.55, 40.0),
                color=RED, fontsize=12.5, fontweight="bold", ha="left", va="center",
                arrowprops=dict(arrowstyle="->", color=RED, lw=1.4))
    ax.text(1.08, 3.2e-4, "kr = 1", color=GREY, fontsize=12, fontweight="bold",
            ha="left", va="bottom")

    # what each half means
    ax.text(0.105, 1700, "stored terms dominate\nreactive near field",
            color=RED, fontsize=11.5, fontweight="bold", ha="left", va="top")
    ax.text(19.0, 1700, "kr ≫ 1\nradiation term alone",
            color=GREY, fontsize=11.5, fontweight="bold", ha="right", va="top")

    ax.legend(loc="lower left", bbox_to_anchor=(0.015, 0.02), fontsize=11.5,
              handlelength=1.7, labelspacing=0.35)
    finalize(fig, "L05-term-crossover")


if __name__ == "__main__":
    OUT.mkdir(parents=True, exist_ok=True)
    term_crossover()
