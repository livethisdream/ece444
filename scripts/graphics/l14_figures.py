#!/usr/bin/env python3
"""L14: the static figures from the 2026-10-01 illustration sweep.

Every figure is labels only: no equations, so the same SVG serves the deck
(book/extras/slides/fig) and the lesson page (book/extras/viz/img). The math
lives in the lesson text.

  L14-three-approaches  reflector, Yagi, and array, each with the coherent
                        aperture it builds shaded
  L14-beam-patterns     uniform circular aperture against the 10 dB-rule
                        feed's aperture (cos^4 feed, f/D = 0.5), in dB against
                        angle times D/lambda: 59 vs 67 degree beamwidths,
                        -17.6 vs -25 dB first sidelobes
  L14-offset-feed       prime-focus dish with the feed's shadow in the beam,
                        beside an offset slice of a parent paraboloid
  L14-ruze              a surface bump lengthens the path by twice its height;
                        loss against RMS error with lambda/50 and lambda/16
  L14-equal-path        the equal-path property drawn: each feed-to-surface
                        leg equals the run back to the line f behind the
                        vertex, so every ray's total is one straight line
  L14-efficiency-budget the efficiency budget as a waterfall, 1.00 to 0.66,
                        with a legend for what is kept and what is lost
  L14-yagi-boom         the gain-versus-boom table against two ideal endfire
                        lines (4L and 7L over lambda), labeled in words
  L14-log-periodic      a log-periodic dipole array at two frequencies: the
                        few elements near half a wavelength radiate, and that
                        active region slides along the boom with frequency
  L14-link-budget       the cubesat link as a level diagram, with the noise
                        floor, the 14 dB margin, and the no-dish case

    python3 scripts/graphics/l14_figures.py
"""

from __future__ import annotations
import io
import re
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon, Rectangle, FancyArrowPatch, Ellipse
from scipy.special import j0, j1
from svg_font_stack import apply_font_stack

NAVY, BLUE, RED, GREEN, AMBER, GRAY = "#004a85", "#0067b9", "#b01e24", "#1d7a4d", "#8a5a00", "#5b6573"
INK, RULE, SHADE = "#15202b", "#c7d2e0", "#dbe8f4"
ROOT = Path(__file__).resolve().parents[2]
OUTS = [ROOT / "book/extras/slides/fig", ROOT / "book/extras/viz/img"]

plt.rcParams.update({"svg.fonttype": "none", "font.size": 11, "text.color": INK,
                     "axes.edgecolor": GRAY, "axes.labelcolor": INK,
                     "xtick.color": GRAY, "ytick.color": GRAY})
BOX = dict(fc="white", ec="none", alpha=0.92, pad=1.5)


def _m(x, fmt="{:.1f}"):
    """A typographic minus, so labels match the axis ticks."""
    return fmt.format(x).replace("-", "−")


def save(fig, name, alt):
    buf = io.StringIO()
    fig.savefig(buf, format="svg", bbox_inches="tight", pad_inches=0.04, facecolor="white")
    plt.close(fig)
    s = buf.getvalue()
    s = s[s.index("<svg"):]
    s = re.sub(r'<svg([^>]*)>', lambda m: f'<svg{m.group(1)} role="img" aria-label="{alt}">', s, count=1)
    s = apply_font_stack(s)
    for d in OUTS:
        (d / f"{name}.svg").write_text(s)
    print("wrote", name)


def clean(ax, keep=("left", "bottom")):
    for side in ("top", "right", "left", "bottom"):
        ax.spines[side].set_visible(side in keep)


def arrow(ax, p, q, color=NAVY, lw=1.8, ms=12, style="-|>"):
    ax.add_patch(FancyArrowPatch(p, q, arrowstyle=style, mutation_scale=ms, lw=lw,
                                 color=color, shrinkA=0, shrinkB=0))


# ---------------------------------------------------------------- one idea
def three_approaches():
    fig, axs = plt.subplots(1, 3, figsize=(9.6, 3.4))
    for ax in axs:
        ax.set_xlim(-1.5, 1.5)
        ax.set_ylim(-0.95, 1.75)
        ax.set_aspect("equal")
        ax.axis("off")

    # reflector: dish, feed, aperture shaded across the mouth
    ax = axs[0]
    rho = np.linspace(-1, 1, 200)
    f = 0.5
    z = rho ** 2 / (4 * f) - 0.4
    ax.add_patch(Rectangle((-1, z[-1]), 2, 0.16, fc=SHADE, ec="none"))
    ax.plot(rho, z, color=NAVY, lw=3)
    ax.plot([0, 0], [-0.4 + 0.02, f - 0.4], color=GRAY, lw=1)
    ax.plot([0], [f - 0.4], "o", color=RED, ms=7)
    for x in (-0.7, 0.0, 0.7):
        arrow(ax, (x, z[-1] + 0.2), (x, 1.15), color=BLUE, lw=1.4, ms=10)
    ax.text(0, -0.75, "Reflector", ha="center", fontsize=13, fontweight="bold", color=NAVY)
    ax.text(0, 1.45, "a mirror sets the phase", ha="center", fontsize=10.5, color=GRAY)

    # Yagi: top-down, elements across a boom, effective area as an ellipse
    ax = axs[1]
    xs = np.array([-1.0, -0.65, -0.25, 0.15, 0.55, 0.95])
    half = np.array([0.55, 0.50, 0.44, 0.42, 0.40, 0.38])
    ax.add_patch(Ellipse((0.05, 0.25), 2.6, 1.55, fc=SHADE, ec="none"))
    ax.plot([-1.15, 1.1], [0.25, 0.25], color=GRAY, lw=2)
    for i, (x, h) in enumerate(zip(xs, half)):
        ax.plot([x, x], [0.25 - h, 0.25 + h], color=RED if i == 1 else NAVY, lw=3)
    arrow(ax, (1.15, 0.25), (1.45, 0.25), color=BLUE, lw=1.6, ms=11)
    ax.text(0, -0.75, "Yagi-Uda", ha="center", fontsize=13, fontweight="bold", color=NAVY)
    ax.text(0, 1.45, "detuned neighbors set the phase", ha="center", fontsize=10.5, color=GRAY)

    # array: a grid of patches, aperture shaded
    ax = axs[2]
    ax.add_patch(Rectangle((-1.05, -0.5), 2.1, 1.5, fc=SHADE, ec="none"))
    for x in np.linspace(-0.82, 0.82, 5):
        for y in np.linspace(-0.3, 0.8, 4):
            ax.add_patch(Rectangle((x - 0.13, y - 0.11), 0.26, 0.22, fc="white", ec=NAVY, lw=1.6))
    ax.text(0, -0.75, "Array", ha="center", fontsize=13, fontweight="bold", color=NAVY)
    ax.text(0, 1.45, "electronics set the phase", ha="center", fontsize=10.5, color=GRAY)

    fig.text(0.5, 0.005, "Shaded: the coherent aperture each one builds, counted in square wavelengths",
             ha="center", fontsize=11, color=INK)
    fig.subplots_adjust(left=0.01, right=0.99, top=0.98, bottom=0.08, wspace=0.05)
    save(fig, "L14-three-approaches",
         "A reflector, a Yagi-Uda, and an array side by side, each with the coherent aperture "
         "it builds shaded: a mirror, detuned neighbors, or electronics set the phase across it")


# ----------------------------------------------------------- beam patterns
def aperture_pattern(E_of_r, t_axis):
    """|N| for a circularly symmetric aperture field E(r), r in [0,1], against
    t = (D/lambda) sin(theta) in degrees-equivalent units; returns dB."""
    r = np.linspace(0, 1, 1201)
    E = E_of_r(r)
    u = np.pi * t_axis                                  # pi (D/lambda) sin(theta)
    N = np.array([np.trapezoid(E * j0(ui * r) * r, r) for ui in u])
    N = np.abs(N) / abs(N[0])
    return 20 * np.log10(np.maximum(N, 1e-6))


def feed_field(r, f_over_d=0.5, n=4.0):
    th0 = 2 * np.arctan(1 / (4 * f_over_d))
    tp = 2 * np.arctan(r * np.tan(th0 / 2))             # feed angle for this radius
    return np.sqrt(np.cos(tp) ** n) * (1 + np.cos(tp)) / 2


def first_sidelobe(db):
    mx = [i for i in range(1, len(db) - 1) if db[i] > db[i - 1] and db[i] > db[i + 1]]
    return mx[0]


def beam_patterns():
    deg = np.linspace(0.01, 160, 3200)                  # theta * (D/lambda), degrees
    t = np.sin(np.radians(deg / 40)) * 40               # D/lambda = 40, then rescale
    uni = aperture_pattern(lambda r: np.ones_like(r), t)
    tap = aperture_pattern(feed_field, t)
    fig, ax = plt.subplots(figsize=(7.8, 3.9))
    ax.plot(deg, uni, color=GRAY, lw=2.0)
    ax.plot(deg, tap, color=NAVY, lw=2.6)
    ax.axhline(-3, color=RULE, lw=1, ls=(0, (4, 3)))
    for db in (uni, tap):
        col = GRAY if db is uni else NAVY
        ax.plot([deg[int(np.argmax(db < -3.0103))]], [-3], "o", color=col, ms=6, zorder=5)
        i = first_sidelobe(db)
        ax.plot([deg[i]], [db[i]], "o", color=col, ms=6, zorder=5)
    ku = int(np.argmax(uni < -3.0103)); kt = int(np.argmax(tap < -3.0103))
    su, st = uni[first_sidelobe(uni)], tap[first_sidelobe(tap)]
    ax.text(97, -1.5, "11 dB edge taper", color=NAVY, fontsize=11, fontweight="bold", va="top")
    ax.text(97, -5.0, f"{2*deg[kt]:.0f}° beam, {_m(st)} dB sidelobe", color=NAVY, fontsize=10.5, va="top")
    ax.text(97, -8.5, "uniform", color=GRAY, fontsize=11, fontweight="bold", va="top")
    ax.text(97, -12.0, f"{2*deg[ku]:.0f}° beam, {_m(su)} dB sidelobe", color=GRAY, fontsize=10.5, va="top")
    ax.set_xlim(0, 160)
    ax.set_ylim(-40, 1.5)
    ax.set_xlabel("angle off boresight times D/λ (degrees)")
    ax.set_ylabel("pattern (dB)")
    clean(ax)
    ax.grid(color=RULE, lw=0.6)
    ax.set_axisbelow(True)
    fig.tight_layout()
    save(fig, "L14-beam-patterns",
         f"Patterns of a uniform circular aperture and of the 10 dB-rule feed's aperture: "
         f"the taper widens the beam from {2*deg[ku]:.0f} to {2*deg[kt]:.0f} degrees times "
         f"wavelength over D and lowers the first sidelobe from "
         f"{abs(uni[first_sidelobe(uni)]):.1f} to {abs(tap[first_sidelobe(tap)]):.1f} dB")
    return 2 * deg[ku], 2 * deg[kt], uni[first_sidelobe(uni)], tap[first_sidelobe(tap)]


# -------------------------------------------------------------- offset feed
def offset_feed():
    fig, axs = plt.subplots(1, 2, figsize=(9.2, 3.9))
    f = 0.75
    for ax in axs:
        ax.set_aspect("equal")
        ax.axis("off")

    # prime focus
    ax = axs[0]
    rho = np.linspace(-1, 1, 200)
    z = rho ** 2 / (4 * f)
    ax.add_patch(Rectangle((-0.12, f + 0.08), 0.24, 1.25, fc="#ececec", ec="none"))
    for x in (-0.8, -0.45, 0.45, 0.8):
        zz = x ** 2 / (4 * f)
        ax.plot([0, x], [f, zz], color=BLUE, lw=1, alpha=0.6)
        arrow(ax, (x, zz), (x, 2.05), color=BLUE, lw=1.3, ms=9)
    ax.plot(rho, z, color=NAVY, lw=3)
    ax.plot([-0.55, 0], [z[22], f], color=GRAY, lw=1.2)
    ax.plot([0.55, 0], [z[-23], f], color=GRAY, lw=1.2)
    ax.add_patch(Rectangle((-0.12, f - 0.06), 0.24, 0.14, fc=RED, ec="none"))
    ax.text(0, 2.12, "feed shadow in the beam", color=GRAY, fontsize=10.5, ha="center", va="bottom")
    ax.text(0, -0.32, "Prime focus", ha="center", fontsize=13, fontweight="bold", color=NAVY)
    ax.set_xlim(-1.3, 1.3)
    ax.set_ylim(-0.45, 2.35)

    # offset: parent paraboloid dashed, slice solid, feed outside the beam
    ax = axs[1]
    rho = np.linspace(-0.5, 2.1, 300)
    ax.plot(rho, rho ** 2 / (4 * f), color=GRAY, lw=1.3, ls=(0, (5, 4)))
    lo, hi = 0.35, 1.85
    seg = np.linspace(lo, hi, 200)
    for x in np.linspace(lo + 0.15, hi - 0.15, 4):
        zz = x ** 2 / (4 * f)
        ax.plot([0, x], [f, zz], color=BLUE, lw=1, alpha=0.6)
        arrow(ax, (x, zz), (x, 2.05), color=BLUE, lw=1.3, ms=9)
    ax.plot(seg, seg ** 2 / (4 * f), color=NAVY, lw=3)
    ax.add_patch(Rectangle((-0.12, f - 0.06), 0.24, 0.14, fc=RED, ec="none",
                           transform=matplotlib.transforms.Affine2D().rotate_deg_around(0, f, -35) + ax.transData))
    ax.text(-0.5, 0.42, "parent\nparaboloid", color=GRAY, fontsize=10.5, ha="left", va="top")
    ax.text(-0.2, f + 0.3, "feed outside\nthe beam", color=RED, fontsize=10.5, ha="center", va="bottom", bbox=BOX)
    ax.text(2.0, 0.75, "the reflector is\nthe solid slice", color=NAVY, fontsize=10.5, ha="center",
            va="top")
    ax.text(0.8, -0.32, "Offset feed", ha="center", fontsize=13, fontweight="bold", color=NAVY)
    ax.set_xlim(-0.6, 2.6)
    ax.set_ylim(-0.45, 2.35)
    fig.subplots_adjust(left=0.01, right=0.99, top=0.99, bottom=0.01, wspace=0.08)
    save(fig, "L14-offset-feed",
         "Left: a prime-focus dish, where the feed at the focus sits in the outgoing beam and "
         "casts a shadow. Right: an offset reflector, a slice cut from one side of a larger "
         "parent paraboloid, so the feed at the shared focus sits outside the beam")


# --------------------------------------------------------------- equal path
def equal_path():
    """The parabola's definition turns every ray's path into one straight line.

    z runs left to right, the vertex at 0, the focus at f, the line z = -f
    behind the vertex, the aperture plane at z_a. For each sample point P the
    feed-to-surface leg FP is drawn solid, and its twin, the run from P back
    to the line, dashed in the same color: the two are equal by definition.
    The dashed twin plus the surface-to-aperture leg is then the straight
    line from z = -f to z_a, whatever P is.
    """
    f, za, R = 1.0, 1.75, 2.0
    fig, ax = plt.subplots(figsize=(8.4, 4.1))
    ax.set_aspect("equal")
    ax.axis("off")
    rho = np.linspace(-R, R, 300)
    ax.plot([-f - 0.1, za + 0.2], [0, 0], color=GRAY, lw=0.8, ls=(0, (6, 2, 1, 2)))
    ax.plot([-f, -f], [-R - 0.15, R + 0.15], color=GRAY, lw=1.6)
    ax.plot([za, za], [-R - 0.15, R + 0.15], color=GREEN, lw=1.6, ls=(0, (4, 3)))
    ax.plot(rho ** 2 / (4 * f), rho, color=NAVY, lw=3)
    for r, c in ((1.65, RED), (-0.8, AMBER)):
        zp = r ** 2 / (4 * f)
        ax.plot([f, zp], [0, r], color=c, lw=2.2)
        ax.plot([-f, zp], [r, r], color=c, lw=2.2, ls=(0, (3, 2)))
        ax.plot([zp, za], [r, r], color=GREEN, lw=2.2)
        ax.plot(zp, r, "o", color=c, ms=6, zorder=5)
    ax.plot(f, 0, "o", color=NAVY, ms=9, zorder=6)
    ax.text(f + 0.06, -0.12, "F (feed)", color=NAVY, fontsize=11, ha="left", va="top",
            fontweight="bold")
    ax.text(1.65 ** 2 / 4 - 0.1, 1.65 + 0.08, "P", color=RED, fontsize=11, fontweight="bold",
            ha="right", va="bottom", bbox=BOX)
    ax.text(0.8 ** 2 / 4 - 0.1, -0.8 - 0.08, "P", color=AMBER, fontsize=11, fontweight="bold",
            ha="right", va="top", bbox=BOX)
    ax.text(-f - 0.08, R + 0.2, "a line f behind\nthe vertex", color=GRAY, fontsize=10.5,
            ha="center", va="bottom")
    ax.text(za, R + 0.2, "aperture\nplane", color=GREEN, fontsize=10.5, ha="center", va="bottom")
    # the focal distance
    yf = -R - 0.3
    for z0 in (0, f):
        ax.plot([z0, z0], [yf - 0.08, -0.12 if z0 == 0 else -0.5], color=GRAY, lw=0.7,
                ls=(0, (1, 2)))
    ax.annotate("", (0, yf), (f, yf),
                arrowprops=dict(arrowstyle="<->", color=GRAY, lw=1, shrinkA=0, shrinkB=0))
    ax.text(f / 2, yf + 0.06, "f", color=GRAY, fontsize=11, ha="center", va="bottom",
            style="italic")
    # every ray's total is the line-to-plane distance
    yb = -R - 0.75
    ax.annotate("", (-f, yb), (za, yb),
                arrowprops=dict(arrowstyle="<->", color=INK, lw=1.2, shrinkA=0, shrinkB=0))
    ax.text((za - f) / 2, yb - 0.1, "every ray's path: this one length", color=INK, fontsize=11,
            ha="center", va="top", fontweight="bold")
    # key, right of the drawing
    kx, ky = za + 0.45, 1.3
    rows = [(INK, "-", "feed to surface"),
            (INK, (0, (3, 2)), "the same length, measured\nback to the line"),
            (GREEN, "-", "surface to aperture plane")]
    for i, (c, ls, t) in enumerate(rows):
        y = ky - i * 0.85
        ax.plot([kx, kx + 0.45], [y, y], color=c, lw=2.2, ls=ls)
        ax.text(kx + 0.6, y, t, color=INK, fontsize=10.5, ha="left", va="center")
    ax.set_xlim(-f - 0.6, kx + 2.9)
    ax.set_ylim(yb - 0.55, R + 0.85)
    fig.subplots_adjust(left=0.01, right=0.99, top=0.99, bottom=0.01)
    save(fig, "L14-equal-path",
         "A parabola with its focus F, a line a focal length behind its vertex, and the aperture "
         "plane in front. For two surface points P, the feed-to-surface leg equals the dashed run "
         "from P back to the line, so each ray's whole path equals the straight distance from "
         "the line to the aperture plane, the same for every ray")


# ---------------------------------------------------------------- Ruze
def ruze():
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(9.4, 3.5), gridspec_kw={"width_ratios": [1, 1.25]})
    # bump sketch
    x = np.linspace(-1.6, 1.6, 400)
    eps = 0.22
    surf = -eps * np.exp(-(x / 0.35) ** 2)
    a1.fill_between(x, surf, -0.6, color=SHADE, lw=0)
    a1.plot(x, surf, color=NAVY, lw=3)
    a1.plot(x, np.zeros_like(x), color=GRAY, lw=1, ls=(0, (4, 3)))
    arrow(a1, (-0.95, 1.2), (-0.95, 0.02), color=BLUE, lw=1.6)
    arrow(a1, (-0.75, 0.02), (-0.75, 1.2), color=BLUE, lw=1.6)
    arrow(a1, (-0.1, 1.2), (-0.1, -eps + 0.01), color=RED, lw=1.6)
    arrow(a1, (0.1, -eps + 0.01), (0.1, 1.2), color=RED, lw=1.6)
    a1.annotate("", (0.6, 0), (0.6, -eps), arrowprops=dict(arrowstyle="<->", color=INK, lw=1))
    a1.text(0.68, -eps / 2, "bump depth", fontsize=10.5, va="center", ha="left")
    a1.text(-0.85, 1.4, "ideal\nsurface", color=BLUE, fontsize=10.5, ha="center", va="bottom")
    a1.text(0.0, 1.4, "bump: travels its\ndepth twice", color=RED, fontsize=10.5, ha="left", va="bottom")
    a1.set_xlim(-1.6, 1.6)
    a1.set_ylim(-0.6, 2.5)
    a1.set_aspect("equal")
    a1.axis("off")
    # loss curve
    s = np.linspace(0, 0.08, 400)
    loss = 685.8 * s ** 2
    a2.plot(s, loss, color=NAVY, lw=2.6)
    for frac, lab in ((1 / 50, "λ/50"), (1 / 16, "λ/16")):
        L = 685.8 * frac ** 2
        a2.plot([frac], [L], "o", color=AMBER, ms=7, zorder=5)
        a2.text(frac + 0.003, L + 0.15, f"{lab}: {L:.2f} dB", color=AMBER, fontsize=10.5,
                ha="left", va="bottom", bbox=BOX)
    a2.set_xlabel("RMS surface error (fraction of a wavelength)")
    a2.set_ylabel("gain loss (dB)")
    a2.set_xlim(0, 0.08)
    a2.set_ylim(0, 4.5)
    clean(a2)
    a2.grid(color=RULE, lw=0.6)
    a2.set_axisbelow(True)
    fig.tight_layout(w_pad=2.5)
    save(fig, "L14-ruze",
         "Left: a bump in the reflector surface lengthens the path of a ray by twice the bump "
         "depth, in and back out. Right: gain loss grows with the square of the RMS surface "
         "error: 0.27 dB at a fiftieth of a wavelength and 2.68 dB at a sixteenth")


# ------------------------------------------------------- efficiency budget
def efficiency_budget():
    terms = [("spillover", 0.90), ("taper", 0.85), ("blockage", 0.95),
             ("surface", 0.94), ("everything else", 0.97)]
    fig, ax = plt.subplots(figsize=(7.8, 3.6))
    level = 1.0
    ax.bar(0, 1.0, color=SHADE, ec=NAVY, lw=1.2, width=0.62)
    ax.text(0, 1.015, "1.00", ha="center", va="bottom", fontsize=10.5, color=NAVY)
    for i, (name, fac) in enumerate(terms, start=1):
        new = level * fac
        ax.bar(i, new, color=SHADE, ec=NAVY, lw=1.2, width=0.62)
        ax.bar(i, level - new, bottom=new, color="#f3d6d7", ec=RED, lw=1.0, width=0.62)
        ax.text(i, level + 0.015, f"×{fac:.2f}", ha="center", va="bottom", fontsize=10.5, color=RED)
        ax.text(i, new / 2, f"{new:.2f}", ha="center", va="center", fontsize=10.5, color=NAVY,
                fontweight="bold")
        level = new
    ax.set_xticks(range(len(terms) + 1))
    ax.set_xticklabels(["ideal"] + [t for t, _ in terms], fontsize=10.5)
    ax.set_ylim(0, 1.12)
    ax.bar([-5], [0], color=SHADE, ec=NAVY, lw=1.2, label="efficiency left after this term")
    ax.bar([-5], [0], color="#f3d6d7", ec=RED, lw=1.0, label="what this term takes away")
    ax.set_xlim(-0.5, len(terms) + 0.5)
    ax.legend(loc="upper right", frameon=False, fontsize=10.5, bbox_to_anchor=(1.0, 1.04))
    ax.set_ylabel("aperture efficiency")
    clean(ax, keep=("bottom",))
    ax.set_yticks([])
    fig.tight_layout()
    save(fig, "L14-efficiency-budget",
         f"The efficiency budget as a waterfall: spillover, taper, blockage, surface error, "
         f"and the remaining losses take an ideal aperture from 1.00 to {level:.2f}. Blue is the "
         f"efficiency left after each term, red is what that term takes away")
    return level


# ----------------------------------------------------------- Yagi boom
def yagi_boom():
    boom = np.array([0.3, 1.0, 2.2, 4.5])
    gain = np.array([7.5, 10.0, 12.5, 14.5])
    L = np.geomspace(0.25, 8, 200)
    fig, ax = plt.subplots(figsize=(7.6, 3.9))
    ax.plot(L, 10 * np.log10(7 * L), color=NAVY, lw=1.8, ls=(0, (6, 3)))
    ax.plot(L, 10 * np.log10(4 * L), color=GRAY, lw=1.8, ls=(0, (2, 2)))
    slope, icpt = np.polyfit(np.log2(boom), gain, 1)
    Lf = np.geomspace(0.25, 8, 50)
    ax.plot(Lf, icpt + slope * np.log2(Lf), color=AMBER, lw=1.4, alpha=0.8)
    ax.plot(boom, gain, "o", color=AMBER, ms=9, zorder=5, mec="white", mew=1.5)
    fit = lambda x: icpt + slope * np.log2(x)
    ax.annotate("ideal line source, best phasing: +3 dB per doubling", (6.0, 10 * np.log10(42)), (0.27, 18.2),
                color=NAVY, fontsize=10.5, ha="left", va="center",
                arrowprops=dict(arrowstyle="->", color=NAVY, lw=1, shrinkB=3))
    ax.annotate(f"typical Yagis: +{slope:.1f} dB per doubling", (0.5, fit(0.5)), (0.27, 14.0),
                color=AMBER, fontsize=10.5, ha="left", va="center",
                arrowprops=dict(arrowstyle="->", color=AMBER, lw=1, shrinkB=4))
    ax.annotate("ideal line source, phased at light speed:\nalso +3 dB per doubling", (6.0, 10 * np.log10(24)), (7.6, 4.6),
                color=GRAY, fontsize=10.5, ha="right", va="center",
                arrowprops=dict(arrowstyle="->", color=GRAY, lw=1, shrinkB=3))
    ax.set_xscale("log", base=2)
    ax.set_xticks([0.25, 0.5, 1, 2, 4, 8])
    ax.set_xticklabels(["0.25", "0.5", "1", "2", "4", "8"])
    ax.set_xlim(0.25, 8)
    ax.set_ylim(0, 20)
    ax.set_xlabel("boom length (wavelengths): each step right doubles the boom")
    ax.set_ylabel("gain (dBi)")
    clean(ax)
    ax.grid(color=RULE, lw=0.6)
    ax.set_axisbelow(True)
    fig.tight_layout()
    save(fig, "L14-yagi-boom",
         f"Yagi gain against boom length on a doubling scale: the typical designs climb about "
         f"{slope:.1f} dB each time the boom doubles, against two ideal endfire lines, one phased at "
         f"light speed and one phased for best gain, which both climb 3 dB per doubling")
    return slope


# ------------------------------------------------------------ log-periodic
def log_periodic():
    """The same LPDA drawn at a low and a high frequency.

    Ten dipoles scaled by tau = 0.88 (longest 3.2 times the shortest), spaced
    in proportion to their length. An element radiates strongly when its
    length is within about 15% of half a wavelength; those are drawn in red
    as the active region. Longer elements behind it are drawn as reflectors,
    shorter ones ahead as directors, the Yagi's long-lags / short-leads rule.
    Element heights are drawn at 0.75 scale so the two panels fit a slide.
    """
    tau, sigma, N = 0.88, 0.16, 10
    L = tau ** np.arange(N)                       # element lengths, longest = 1
    x = np.concatenate([[0], np.cumsum(2 * sigma * L[:-1])])
    H = 1.0                                       # drawn height per unit length
    fig, axs = plt.subplots(2, 1, figsize=(7.2, 5.0))
    cases = [(0.86, "Low frequency: the long end radiates"),
             (0.40, "High frequency: the short end radiates")]
    for k, (ax, (half_lam, title)) in enumerate(zip(axs, cases)):
        ax.axis("off")
        ax.plot([x[0] - 0.05, x[-1] + 0.05], [0, 0], color=GRAY, lw=2.2, solid_capstyle="butt")
        for a, b in zip(x[:-1], x[1:]):           # the feed line crosses over
            m = (a + b) / 2
            ax.plot([m - 0.025, m + 0.025], [-0.05, 0.05], color=GRAY, lw=1)
            ax.plot([m - 0.025, m + 0.025], [0.05, -0.05], color=GRAY, lw=1)
        act = np.abs(L / half_lam - 1) <= 0.15
        for xi, li, a in zip(x, L, act):
            c, lw = (RED, 3.4) if a else ((NAVY, 2) if li > half_lam else (BLUE, 2))
            ax.plot([xi, xi], [-H * li / 2, H * li / 2], color=c, lw=lw, solid_capstyle="butt")
        xa = x[act]
        ax.add_patch(Rectangle((xa.min() - 0.08, -0.56), xa.max() - xa.min() + 0.16, 1.12,
                               fc=RED, alpha=0.08, ec="none"))
        ax.text(xa.mean(), -0.6, "active region:\nnear half a wavelength", color=RED,
                fontsize=13, ha="center", va="top")
        arrow(ax, (x[-1] + 0.2, 0), (x[-1] + 0.7, 0), color=RED, lw=2.4, ms=16)
        ax.text(x[-1] + 0.45, 0.07, "beam", color=RED, fontsize=13, ha="center", va="bottom",
                fontweight="bold")
        ax.text(x[0] - 0.12, 0.66, title, color=INK, fontsize=14, fontweight="bold",
                ha="left", va="bottom")
        if k == 0:
            ax.text(x[6], -0.6, "shorter: directors", color=BLUE, fontsize=13,
                    ha="center", va="top")
        else:
            ax.text(x[2], -0.6, "longer: reflectors", color=NAVY, fontsize=13,
                    ha="center", va="top")
        ax.set_xlim(x[0] - 0.15, x[-1] + 0.8)
        ax.set_ylim(-0.95, 0.85)
    axs[0].text(x[-1] + 0.45, -0.2, "×: the feed line\ncrosses over\nbetween neighbors",
                color=GRAY, fontsize=13, ha="center", va="top", style="italic")
    fig.subplots_adjust(left=0.01, right=0.99, top=0.99, bottom=0.01, hspace=0.1)
    save(fig, "L14-log-periodic",
         "The same log-periodic dipole array, ten dipoles shrinking toward the front, drawn at "
         "two frequencies. At the low frequency the few long elements near half a wavelength "
         "radiate and the shorter ones ahead act as directors; at the high frequency the active "
         "region has slid to the short end and the longer ones behind act as reflectors. The "
         "beam points toward the short end both times")


# ------------------------------------------------------------- link budget
def link_budget():
    lam = 3e8 / 2.4e9
    Pt = 10 * np.log10(2000)
    Lfs = 20 * np.log10(4 * np.pi * 1e6 / lam)
    floor = -174 + 10 * np.log10(1e5) + 3
    steps = [("transmitter\n2 W", Pt), ("cubesat\nantenna", Pt + 0), ("free-space\npath", Pt - Lfs),
             ("ground\ndish", Pt - Lfs + 20)]
    xs = np.arange(len(steps))
    fig, (top, bot) = plt.subplots(2, 1, sharex=True, figsize=(8.0, 4.3),
                                   gridspec_kw={"height_ratios": [1, 1.9], "hspace": 0.08})
    lv = [v for _, v in steps]
    for ax in (top, bot):
        for i in range(len(xs)):
            ax.plot([xs[i] - 0.32, xs[i] + 0.32], [lv[i], lv[i]], color=NAVY, lw=3)
            if i:
                ax.plot([xs[i - 1] + 0.32, xs[i] - 0.32], [lv[i - 1], lv[i]], color=NAVY, lw=1.2,
                        ls=(0, (3, 2)))
        ax.grid(axis="y", color=RULE, lw=0.6)
        ax.set_axisbelow(True)
    top.set_ylim(25, 40)
    bot.set_ylim(-135, -95)
    top.spines["bottom"].set_visible(False)
    bot.spines["top"].set_visible(False)
    for ax in (top, bot):
        ax.spines["right"].set_visible(False)
    top.tick_params(axis="x", length=0)
    top.text(0, Pt + 1.2, f"{Pt:.1f} dBm", color=NAVY, ha="center", va="bottom", fontsize=10.5)
    top.text(1, Pt + 1.2, "+0 dBi", color=NAVY, ha="center", va="bottom", fontsize=10.5)
    bot.text(2, lv[2] - 2.0, f"−{Lfs:.1f} dB path loss\n{_m(lv[2])} dBm", color=NAVY, ha="center",
             va="top", fontsize=10.5)
    bot.text(3, lv[3] + 1.5, f"+20 dBi dish: {_m(lv[3])} dBm", color=NAVY, ha="center",
             va="bottom", fontsize=10.5, bbox=BOX)
    bot.axhline(floor, color=RED, lw=1.8, ls=(0, (4, 3)))
    bot.text(-0.35, floor + 1.0, f"noise floor {_m(floor, '{:.0f}')} dBm", color=RED, fontsize=10.5,
             ha="left", va="bottom", fontweight="bold")
    bot.annotate("", (3.45, lv[3]), (3.45, floor),
                 arrowprops=dict(arrowstyle="<->", color=GREEN, lw=1.6, shrinkA=0, shrinkB=0))
    bot.text(3.52, (lv[3] + floor) / 2, f"margin\n{lv[3]-floor:.0f} dB", color=GREEN, fontsize=10.5,
             va="center", ha="left", fontweight="bold")
    bot.plot([3 - 0.32, 3 + 0.32], [lv[2], lv[2]], color=GRAY, lw=2, ls=(0, (2, 2)))
    bot.text(3.4, lv[2], f"0 dBi instead:\n{floor-lv[2]:.0f} dB under the noise",
             color=GRAY, fontsize=10.5, ha="left", va="center")
    d = 0.012
    kw = dict(transform=top.transAxes, color=GRAY, clip_on=False, lw=1)
    top.plot((-d, +d), (-d * 1.9, +d * 1.9), **kw)
    kw.update(transform=bot.transAxes)
    bot.plot((-d, +d), (1 - d, 1 + d), **kw)
    bot.set_xticks(xs)
    bot.set_xticklabels([s for s, _ in steps], fontsize=10.5)
    bot.set_xlim(-0.5, 4.3)
    fig.text(0.015, 0.5, "signal level (dBm)", rotation=90, va="center", ha="center", fontsize=11)
    fig.subplots_adjust(left=0.1, right=0.98, top=0.98, bottom=0.14)
    save(fig, "L14-link-budget",
         f"Level diagram of the cubesat downlink: {Pt:.1f} dBm leaves the transmitter, free-space "
         f"path loss of {Lfs:.1f} dB takes it to {lv[2]:.1f} dBm, and the 20 dBi dish raises it to "
         f"{lv[3]:.1f} dBm, {lv[3]-floor:.0f} dB above the {floor:.0f} dBm noise floor; without "
         f"the dish the signal sits {floor-lv[2]:.0f} dB under the noise")
    return Pt, Lfs, lv[3], floor


if __name__ == "__main__":
    three_approaches()
    print("beam:", beam_patterns())
    offset_feed()
    equal_path()
    ruze()
    print("budget product:", efficiency_budget())
    print("yagi slope:", yagi_boom())
    log_periodic()
    print("link:", link_budget())
