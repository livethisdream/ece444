#!/usr/bin/env python3
"""L09: the four Smith-chart reading skills, one small chart each.

The frame "Four Smith-Chart Reading Skills" lists what a student has to see on
an analyzer trace this semester: a crossing of the real axis (resonance), a
dip inside the VSWR = 2 circle (the course match bar), a loop (two
resonances), and a whole trace that has rotated (the reference plane moved). Each panel draws
one of those on the same chart, from a circuit that actually produces it:

  1. a series-resonant antenna, R = 30 ohm at resonance, so the crossing
     sits left of center;
  2. the same antenna at R = 45 ohm, so the trace dips inside the circle;
  3. the antenna in parallel with a feed resonance 6% higher, which is what
     draws a loop;
  4. panel 1's trace and a copy rotated by 70 degrees, the same antenna seen
     through 35 electrical degrees of extra line.

Two layouts from one drawing: a 2x2 grid for the lesson page and a 1x4 strip
for the deck. Deck figures carry no equations, so the labels are words and
plain numbers.

    python3 scripts/graphics/l09_smith_skills.py
    -> book/extras/slides/fig/L09-smith-skills.svg        (2x2, lesson page)
       book/extras/slides/fig/L09-smith-skills-row.svg    (1x4, deck)
       book/extras/viz/img/L09-smith-skills.svg           (2x2 copy)
"""

from __future__ import annotations
import io, re
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from svg_font_stack import apply_font_stack
from matplotlib.patches import FancyArrowPatch

NAVY, BLUE, RED, GREEN, AMBER, GRAY = "#004a85", "#0067b9", "#b01e24", "#1d7a4d", "#8a5a00", "#5a5a5a"
INK, RULE, RIM = "#1a1a1a", "#c7d2e0", "#7fa8c9"
ROOT = Path(__file__).resolve().parents[2]
FIG, IMG = ROOT / "book/extras/slides/fig", ROOT / "book/extras/viz/img"

plt.rcParams.update({"svg.fonttype": "none", "font.size": 12, "text.color": INK})

Z0 = 50.0
G = lambda z: (z - Z0) / (z + Z0)            # impedance in ohms -> reflection coefficient
SPEC = 1.0 / 3.0                              # |Gamma| at VSWR = 2, the course bar


def mini_smith(ax):
    """A sparse grid: enough to read r = 1 and the axis, not a working chart."""
    th = np.linspace(0, 2 * np.pi, 720)
    rim = plt.Circle((0, 0), 1.0, transform=ax.transData, facecolor="none")
    for r in (0.5, 1.0, 2.0):
        c, rad = r / (1 + r), 1 / (1 + r)
        ax.plot(c + rad * np.cos(th), rad * np.sin(th), color=RULE, lw=0.8, zorder=1)
    for x in (0.5, 1.0, 2.0):
        for s in (+1, -1):
            rad = 1.0 / x
            line, = ax.plot(1.0 + rad * np.cos(th), s / x + rad * np.sin(th), color=RULE, lw=0.8, zorder=1)
            line.set_clip_path(rim)
    ax.plot(np.cos(th), np.sin(th), color=RIM, lw=1.4, zorder=2)
    ax.plot([-1, 1], [0, 0], color="#b9d2e5", lw=1.1, zorder=2)
    ax.plot(SPEC * np.cos(th), SPEC * np.sin(th), color=GREEN, lw=1.0, ls=(0, (3, 2)), zorder=2)
    ax.set_xlim(-1.08, 1.08); ax.set_ylim(-1.08, 1.08)
    ax.set_aspect("equal"); ax.axis("off")


def antenna(f, R0=30.0, Q=6.0, f0=1.0):
    """Series-resonant antenna: resistance rising slowly with frequency, a
    reactance that crosses zero at f0."""
    R = R0 * (1 + 0.6 * (f - f0))
    X = Q * R0 * (f / f0 - f0 / f)
    return R + 1j * X


def with_feed(f, f1=1.06, B1=0.02):
    """The antenna in parallel with a feed resonance at f1: a susceptance that
    passes through zero there. Two resonances close together draw a loop."""
    Y = 1 / antenna(f, R0=40.0, Q=7.0) + 1j * B1 * (f / f1 - f1 / f)
    return 1 / Y


def trace(ax, g, color=NAVY, lw=2.6, z=4, ls="-"):
    ax.plot(g.real, g.imag, color=color, lw=lw, ls=ls, zorder=z, solid_capstyle="round")


def arrowhead(ax, g, i, color, size=16):
    ax.annotate("", xy=(g[i + 4].real, g[i + 4].imag), xytext=(g[i].real, g[i].imag),
                arrowprops=dict(arrowstyle="-|>", color=color, lw=0, mutation_scale=size), zorder=5)


def draw_panels(axes, title_size=12.5, label_size=10.5, ROW=False, captions=True):
    cap = lambda ax, text: ax.text(0.0, -0.98, text, color=GRAY, fontsize=label_size - 0.5, ha="center", va="top") if captions else None
    f = np.linspace(0.84, 1.16, 500)

    # 1. crosses the real axis, left of center
    ax = axes[0]; mini_smith(ax)
    g = G(antenna(f, R0=30.0)); trace(ax, g); arrowhead(ax, g, 120, NAVY)
    k = np.argmin(np.abs(g.imag)); ax.plot(g[k].real, g[k].imag, "o", color=RED, ms=8, zorder=6,
                                          markeredgecolor="white", markeredgewidth=1.2)
    ax.text(g[k].real - 0.06, g[k].imag - 0.19, "resonance", color=RED, fontsize=label_size,
            fontweight="bold", ha="center", va="top", zorder=6)
    cap(ax, "left of center: under 50 ohms" if not ROW else "under 50 ohms")
    ax.set_title("Crosses the real axis", color=NAVY, fontsize=title_size, fontweight="bold", pad=4)

    # 2. dips inside the VSWR = 2 circle
    ax = axes[1]; mini_smith(ax)
    th = np.linspace(0, 2 * np.pi, 200)
    ax.fill(SPEC * np.cos(th), SPEC * np.sin(th), color=GREEN, alpha=0.10, zorder=1)
    g = G(antenna(f, R0=45.0, Q=7.0)); inside = np.abs(g) < SPEC
    trace(ax, g, color="#9fb4c7", lw=2.0, z=3)
    trace(ax, np.where(inside, g, np.nan + 0j), color=GREEN, lw=3.0, z=4)
    arrowhead(ax, g, 120, "#9fb4c7")
    if captions:                       # the page's bullet beside the chart says this already
        ax.text(0.0, SPEC + 0.10, "inside the VSWR = 2 circle", color=GREEN, fontsize=label_size,
                fontweight="bold", ha="center", va="bottom", zorder=6)
    cap(ax, "matched to VSWR 2 while inside" if not ROW else "matched to VSWR 2")
    ax.set_title("Inside the small circle", color=NAVY, fontsize=title_size, fontweight="bold", pad=4)

    # 3. a loop: two resonances close together
    ax = axes[2]; mini_smith(ax)
    fl = np.linspace(0.80, 1.24, 700)
    g = G(with_feed(fl)); trace(ax, g); arrowhead(ax, g, 150, NAVY)
    cap(ax, "two resonances: element plus feed" if not ROW else "element plus feed")
    ax.set_title("A loop", color=NAVY, fontsize=title_size, fontweight="bold", pad=4)

    # 4. the whole trace rotated: the reference plane moved
    ax = axes[3]; mini_smith(ax)
    g = G(antenna(f, R0=30.0)); trace(ax, g, color="#9fb4c7", lw=2.2, z=3)
    rot = g * np.exp(-1j * np.deg2rad(70)); trace(ax, rot, color=AMBER, lw=2.8, z=4)
    k = np.argmin(np.abs(g.imag))
    a0 = np.angle(g[k]); r0 = np.abs(g[k])
    arc = np.linspace(a0, a0 - np.deg2rad(70), 60)
    ax.plot(r0 * np.cos(arc), r0 * np.sin(arc), color=AMBER, lw=1.2, ls=(0, (2, 2)), zorder=5)
    ax.annotate("", xy=(rot[k].real, rot[k].imag), xytext=(r0 * np.cos(arc[-8]), r0 * np.sin(arc[-8])),
                arrowprops=dict(arrowstyle="-|>", color=AMBER, lw=0, mutation_scale=14), zorder=6)
    cap(ax, "same antenna, longer cable to the cal plane" if not ROW else "longer cable to the cal plane")
    ax.set_title("The whole trace rotates", color=NAVY, fontsize=title_size, fontweight="bold", pad=4)


def export(fig, name: str, outs):
    """Both copies carry the shared font stack: an <img> cannot inherit."""
    buf = io.StringIO()
    fig.savefig(buf, format="svg", transparent=True, bbox_inches="tight", pad_inches=0.04)
    plt.close(fig)
    s = buf.getvalue(); s = s[s.index("<svg"):]
    s = apply_font_stack(s)
    for out in outs:
        out.mkdir(parents=True, exist_ok=True)
        (out / f"{name}.svg").write_text(s, encoding="utf-8")
        print(f"wrote {out / (name + '.svg')}")


def main() -> int:
    # wider than tall on purpose: beside four bullets on a phone the frame
    # has about 290px of height to give this figure, and a square 2x2 does not fit
    fig, axes = plt.subplots(2, 2, figsize=(7.4, 5.6))
    draw_panels(axes.ravel(), title_size=15, label_size=12, captions=False)
    fig.subplots_adjust(wspace=0.02, hspace=0.02)
    export(fig, "L09-smith-skills", [FIG, IMG])

    fig, axes = plt.subplots(1, 4, figsize=(13.0, 3.9))
    draw_panels(axes, title_size=13, label_size=10.5, ROW=True)
    fig.subplots_adjust(wspace=0.08)
    export(fig, "L09-smith-skills-row", [FIG])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
