#!/usr/bin/env python3
"""L14: why the reflector feed's edge taper lands near 10 dB.

The 10 dB rule was asserted on the page and the deck. This draws where it
comes from. A prime-focus dish with f/D = 0.5 (rim at 53.1 degrees from the
feed) is fed by a cos^n(theta') pattern, and n is swept:

  spillover efficiency  = fraction of the feed's power that lands on the dish
                        = int_0^theta0 cos^n sin / int_0^(pi/2) cos^n sin
  taper efficiency      = L13's |int E_a dS|^2 / (A int |E_a|^2 dS), with the
                          aperture field E_a ~ sqrt(cos^n theta') (1 + cos theta')/2
                          at rho = 2f tan(theta'/2)  (feed pattern times the
                          1/r spreading from the focus to the surface)
  edge taper            = 20 log10 E_a(rim)/E_a(center), the x axis

Their product peaks at an edge taper of about 10 to 11 dB, at about 0.82.
Labels only; the formulas are in the lesson text.

    python3 scripts/graphics/l14_taper_spillover.py
    -> book/extras/slides/fig/L14-taper-spillover.svg   (deck)
       book/extras/viz/img/L14-taper-spillover.svg      (lesson page, depth)
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

NAVY, BLUE, AMBER, GRAY = "#004a85", "#0067b9", "#8a5a00", "#5b6573"
INK, RULE = "#15202b", "#c7d2e0"
ROOT = Path(__file__).resolve().parents[2]
OUTS = [ROOT / "book/extras/slides/fig", ROOT / "book/extras/viz/img"]

plt.rcParams.update({"svg.fonttype": "none", "font.size": 11, "text.color": INK,
                     "axes.edgecolor": GRAY, "axes.labelcolor": INK,
                     "xtick.color": GRAY, "ytick.color": GRAY})

F_OVER_D = 0.5


def efficiencies(n, f_over_d=F_OVER_D, pts=4001):
    """Edge taper (dB, positive down), spillover, and taper efficiency for cos^n."""
    th0 = 2 * np.arctan(1 / (4 * f_over_d))
    t = np.linspace(0, th0, pts)
    tf = np.linspace(0, np.pi / 2, pts)
    spill = np.trapezoid(np.cos(t) ** n * np.sin(t), t) / np.trapezoid(np.cos(tf) ** n * np.sin(tf), tf)
    rho = np.tan(t / 2)                                   # in units of 2f
    E = np.sqrt(np.cos(t) ** n) * (1 + np.cos(t)) / 2
    drho = np.gradient(rho, t)
    num = np.trapezoid(E * rho * drho, t) ** 2
    den = np.trapezoid(E ** 2 * rho * drho, t) * rho[-1] ** 2 / 2
    return -20 * np.log10(E[-1] / E[0]), spill, num / den


def curves():
    ns = np.linspace(0.2, 20, 400)
    rows = np.array([efficiencies(n) for n in ns])
    return rows[:, 0], rows[:, 1], rows[:, 2]


def build():
    et, sp, tp = curves()
    pr = sp * tp
    k = int(np.argmax(pr))
    fig, ax = plt.subplots(figsize=(7.6, 3.9))
    ax.plot(et, sp, color=BLUE, lw=2.0)
    ax.plot(et, tp, color=AMBER, lw=2.0)
    ax.plot(et, pr, color=NAVY, lw=3.0)
    ax.plot([et[k]], [pr[k]], "o", ms=7, color=NAVY, zorder=5)
    ax.axvline(et[k], color=NAVY, lw=1, ls=(0, (4, 3)), alpha=0.5)
    box = dict(fc="white", ec="none", alpha=0.92, pad=1.5)
    ax.annotate(f"best: {et[k]:.0f} dB edge taper, {pr[k]:.2f}", (et[k], pr[k]),
                (et[k] + 2.5, 0.42), color=NAVY, fontsize=11, fontweight="bold",
                ha="left", va="center", bbox=box,
                arrowprops=dict(arrowstyle="->", color=NAVY, lw=1.2, shrinkA=2, shrinkB=5))
    # labels placed on the curves' own values, so they move with the data
    i = int(np.argmin(np.abs(et - 22)))
    ax.text(et[i], sp[i] - 0.035, "spillover: power that hits the dish", color=BLUE,
            fontsize=10.5, ha="center", va="top", bbox=box)
    ax.text(et[0], tp[0] + 0.03, "taper: how evenly it lights the aperture",
            color=AMBER, fontsize=10.5, ha="left", va="bottom", bbox=box)
    i = int(np.argmin(np.abs(et - 3.2)))
    ax.text(et[i] + 0.6, pr[i] - 0.06, "product", color=NAVY, fontsize=11,
            fontweight="bold", ha="left", va="top", bbox=box)
    ax.set_xlim(0, 30)
    ax.set_ylim(0.3, 1.1)
    ax.set_xlabel("rim illumination below the center (dB)")
    ax.set_ylabel("efficiency")
    ax.set_yticks([0.4, 0.6, 0.8, 1.0])
    for side in ("top", "right"):
        ax.spines[side].set_visible(False)
    ax.grid(color=RULE, lw=0.7)
    ax.set_axisbelow(True)
    fig.tight_layout()
    buf = io.StringIO()
    fig.savefig(buf, format="svg", bbox_inches="tight", pad_inches=0.04, facecolor="white")
    plt.close(fig)
    s = buf.getvalue()
    s = s[s.index("<svg"):]
    alt = ("Spillover efficiency rises and taper efficiency falls as the feed narrows and the "
           "rim gets darker; their product, the part of the aperture efficiency the feed "
           f"controls, peaks at about {pr[k]:.2f} for an edge taper near {et[k]:.0f} dB, "
           "for a dish with f over D of 0.5")
    s = re.sub(r'<svg([^>]*)>', lambda m: f'<svg{m.group(1)} role="img" aria-label="{alt}">', s, count=1)
    return apply_font_stack(s), et[k], sp[k], tp[k], pr[k]


if __name__ == "__main__":
    svg, e, s, t, p = build()
    for d in OUTS:
        (d / "L14-taper-spillover.svg").write_text(svg)
    print(f"optimum: edge taper {e:.1f} dB, spillover {s:.3f}, taper {t:.3f}, product {p:.3f}")
