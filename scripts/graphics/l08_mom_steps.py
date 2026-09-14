#!/usr/bin/env python3
"""L08: the method of moments in four steps, drawn on one dipole.

The lesson's opening beats are pattern-first: the source becomes N small
radiators, the current is expanded in known shapes with unknown weights, the
weights come from requiring zero tangential field on every segment, and the
pattern is the weighted sum of the segment patterns. Each panel draws one of
those on the same nine-segment half-wave dipole, so the eye carries the wire
from step to step.

  1. the wire cut into segments, the source segment marked, and the small
     donut each segment radiates on its own;
  2. triangle basis shapes on the junctions, heights not yet known, and the
     dashed sum they will add up to;
  3. the field every segment puts on one chosen segment, and the row of the
     matrix that says their total on that segment is zero (the boundary
     condition of a perfect conductor: no tangential field on the metal);
  4. the segment donuts, now weighted, and the half-wave pattern they sum to.

Two layouts from one drawing: a 1x4 strip for the deck and a 2x2 grid for
the lesson page. Deck figures carry no equations, so the labels are words.

    python3 scripts/graphics/l08_mom_steps.py
    -> book/extras/slides/fig/L08-mom-pipeline.svg     (1x4, deck)
       book/extras/viz/img/L08-mom-steps.svg           (2x2, lesson page)
"""

from __future__ import annotations
import io, re
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, Polygon, Rectangle

NAVY, BLUE, RED, GREEN, AMBER, GRAY = "#004a85", "#0067b9", "#b01e24", "#1d7a4d", "#8a5a00", "#5a5a5a"
INK, RULE = "#1a1a1a", "#c7d2e0"
ROOT = Path(__file__).resolve().parents[2]
FIG, IMG = ROOT / "book/extras/slides/fig", ROOT / "book/extras/viz/img"

plt.rcParams.update({"svg.fonttype": "none", "font.size": 12, "text.color": INK})

N = 9                                   # segments, odd so one sits at the feed
L = 1.0                                 # wire length in the drawing's units
D = L / N                               # segment length
ZJ = np.array([-L / 2 + (n + 1) * D for n in range(N - 1)])      # junction positions
ZC = np.array([-L / 2 + (n + 0.5) * D for n in range(N)])        # segment centers
WEIGHT = np.cos(np.pi * ZJ / L)         # the half-wave standing wave, sampled at the junctions


def wire(ax, x=0.0, source=True, lw=3.2, ticks=True, color=NAVY):
    ax.plot([x, x], [-L / 2, L / 2], color=color, lw=lw, solid_capstyle="round", zorder=3)
    if ticks:
        for zj in ZJ:
            ax.plot([x - 0.02, x + 0.02], [zj, zj], color="white", lw=1.6, zorder=4)
    if source:
        ax.plot([x, x], [-D / 2, D / 2], color=RED, lw=lw + 3, solid_capstyle="butt", zorder=5)


def donut(ax, cx, cz, r, color, lw=1.2, alpha=1.0, fill=False):
    """The pattern of one short segment, |sin theta|, as a figure of eight
    around the wire axis: theta measured from the wire, so the lobes sit
    broadside."""
    th = np.linspace(0, 2 * np.pi, 361)
    rr = r * np.abs(np.sin(th))
    xs, zs = cx + rr * np.sin(th), cz + rr * np.cos(th)
    ax.plot(xs, zs, color=color, lw=lw, alpha=alpha, zorder=2)
    if fill:
        ax.fill(xs, zs, color=color, alpha=0.08, zorder=1)


def halfwave(ax, cx, cz, r, color=NAVY, lw=2.6):
    th = np.linspace(1e-3, 2 * np.pi - 1e-3, 721)
    F = np.abs(np.cos(np.pi / 2 * np.cos(th)) / np.sin(th))
    xs, zs = cx + r * F * np.sin(th), cz + r * F * np.cos(th)
    ax.plot(xs, zs, color=color, lw=lw, zorder=6)
    ax.fill(xs, zs, color=color, alpha=0.10, zorder=1)


def frame(ax, title, size):
    ax.set_xlim(-0.78, 0.78); ax.set_ylim(-0.74, 0.74)
    ax.set_aspect("equal"); ax.axis("off")
    ax.set_title(title, color=NAVY, fontsize=size, fontweight="bold", pad=4)


def draw(axes, title_size=12.5, label_size=10.5):
    # 1. cut the source into small radiators
    ax = axes[0]
    wire(ax)
    for zc in ZC[::2]:
        donut(ax, 0.0, zc, 0.13, RED, lw=1.0, alpha=0.55)
    ax.text(0.20, 0.0, "source", color=RED, fontsize=label_size, fontweight="bold", va="center")
    ax.text(0.0, -0.66, "one small radiator per segment", color=GRAY, fontsize=label_size - 0.5,
            ha="center", va="top")
    frame(ax, "1. Cut into segments", title_size)

    # 2. expand the current in known shapes with unknown weights
    ax = axes[1]
    wire(ax, x=-0.45)
    x0 = -0.45
    for n, zj in enumerate(ZJ):
        h = 0.55 * WEIGHT[n]
        tri = Polygon([[x0, zj - D], [x0 + h, zj], [x0, zj + D]], closed=True,
                      facecolor=BLUE, edgecolor=BLUE, alpha=0.18, lw=1.0, zorder=2)
        ax.add_patch(tri)
        ax.plot([x0, x0 + h, x0], [zj - D, zj, zj + D], color=BLUE, lw=1.0, alpha=0.7, zorder=3)
    zz = np.linspace(-L / 2, L / 2, 200)
    ax.plot(x0 + 0.55 * np.interp(zz, np.r_[-L / 2, ZJ, L / 2], np.r_[0, WEIGHT, 0]), zz,
            color=NAVY, lw=2.0, ls=(0, (4, 3)), zorder=4)
    ax.text(0.30, 0.30, "one shape per junction,\nheight unknown", color=BLUE, fontsize=label_size,
            fontweight="bold", ha="center", va="center")
    ax.text(0.30, -0.30, "their sum is\nthe current", color=NAVY, fontsize=label_size,
            fontweight="bold", ha="center", va="center")
    frame(ax, "2. Expand in shapes", title_size)

    # 3. zero tangential field on every segment: one row of the matrix
    ax = axes[2]
    xw = -0.36
    wire(ax, x=xw)
    m = 6                                                       # the segment we look at, in the upper arm
    zm = ZC[m]
    ax.plot([xw, xw], [zm - D / 2, zm + D / 2], color=AMBER, lw=7, solid_capstyle="butt", zorder=6)
    for n in (0, 2, 4, 8):
        rad = -(0.22 + 0.05 * abs(n - m))
        arr = FancyArrowPatch((xw - 0.03, ZC[n]), (xw - 0.03, zm), connectionstyle=f"arc3,rad={rad}",
                              arrowstyle="-|>", mutation_scale=11, color=BLUE, lw=1.1, alpha=0.8, zorder=5)
        ax.add_patch(arr)
    ax.text(xw - 0.05, -0.66, "field from every segment", color=BLUE, fontsize=label_size - 0.5,
            ha="center", va="top")
    ax.text(xw + 0.06, zm, "no tangential\nfield", color=AMBER, fontsize=label_size, fontweight="bold",
            ha="left", va="center")
    # the matrix: one row per segment, shaded by how strongly n is felt at m
    x1, z1, cell = 0.12, 0.46, 0.070
    # rows run top to bottom in the same order as the segments on the wire,
    # so the highlighted row sits at the height of the highlighted segment
    for i in range(N):
        for j in range(N):
            w = 1.0 / (1.0 + 1.6 * abs(i - j))
            fc = NAVY if i != m else AMBER
            ax.add_patch(Rectangle((x1 + j * cell, z1 - (N - i) * cell), cell, cell,
                                   facecolor=fc, alpha=0.12 + 0.75 * w, edgecolor="white", lw=0.6, zorder=3))
    ax.text(x1 + N * cell / 2, z1 - N * cell - 0.04, "one row per segment", color=GRAY,
            fontsize=label_size - 0.5, ha="center", va="top")
    ax.text(x1 + N * cell + 0.03, z1 - (N - m - 0.5) * cell, "this\nrow", color=AMBER, fontsize=label_size - 0.5,
            fontweight="bold", ha="left", va="center")
    frame(ax, "3. Apply the boundary condition", title_size)

    # 4. sum the segment patterns
    ax = axes[3]
    wire(ax, ticks=False)
    for n, zc in enumerate(ZC):
        w = np.cos(np.pi * zc / L)
        donut(ax, 0.0, zc, 0.17 * w, RED, lw=0.9, alpha=0.45)
    halfwave(ax, 0.0, 0.0, 0.62)
    ax.text(0.0, -0.66, "the weighted sum is the pattern", color=GRAY,
            fontsize=label_size - 0.5, ha="center", va="top")
    frame(ax, "4. Sum the patterns", title_size)


def export(fig, name: str, outs):
    """Deck copies inherit the deck font (deck-tools.js inlines them). A copy
    under viz/img is loaded through <img>, an isolated document that cannot
    inherit anything, so it carries the page's sans stack explicitly."""
    buf = io.StringIO()
    fig.savefig(buf, format="svg", transparent=True, bbox_inches="tight", pad_inches=0.04)
    plt.close(fig)
    s = buf.getvalue(); s = s[s.index("<svg"):]
    for out in outs:
        stack = "inherit" if out == FIG else "\'Source Sans Pro\', \'Segoe UI\', Roboto, Helvetica, Arial, sans-serif"
        t = re.sub(r"font-family:[^;}]*", "font-family:" + stack, s)
        out.mkdir(parents=True, exist_ok=True)
        (out / f"{name}.svg").write_text(t, encoding="utf-8")
        print(f"wrote {out / (name + '.svg')}")


def main() -> int:
    fig, axes = plt.subplots(1, 4, figsize=(13.0, 4.0))
    draw(axes, title_size=11.5, label_size=10.5)
    fig.subplots_adjust(wspace=0.12)
    export(fig, "L08-mom-pipeline", [FIG])

    fig, axes = plt.subplots(2, 2, figsize=(7.4, 7.4))
    draw(axes.ravel(), title_size=15, label_size=12)
    fig.subplots_adjust(wspace=0.04, hspace=0.14)
    export(fig, "L08-mom-steps", [IMG])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
