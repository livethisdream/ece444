#!/usr/bin/env python3
"""L09: the two floors that bound a pattern measurement.

Neil, 2026-09-16, on the stray-field frame: "the values aren't clear - why
are there 2 values?", and on the dynamic-range frame: "what does 'limited by
our 42dB floor' mean? Here's where an image would tell the story very well."
Both frames make the same argument -- an unwanted signal sets a level below
which a measurement says nothing -- so both pictures are drawn here.

L09-stray-ripple: a stray reflection at a fixed level adds to the wanted
signal with whatever phase the geometry gives it, so the reading lands
anywhere on a circle around the true value. Panel 1 draws that circle for a
-20 dB sidelobe. Panel 2 draws the dB interval it produces at three signal
levels, which is where the asymmetric pair of numbers in the frame's table
comes from: the same amplitude ripple is not the same number of decibels up
as it is down.

L09-dynamic-range: the measured pattern is the true pattern plus the
receiver's noise floor, in power. The main beam and the beamwidth are
untouched, the sidelobe still clears the floor, and the nulls simply read the
floor back.

    python3 scripts/graphics/l09_measurement_floors.py
    -> book/extras/viz/img/L09-stray-ripple.svg         (lesson page, depth)
       book/extras/slides/fig/L09-dynamic-range.svg     (deck)
       book/extras/viz/img/L09-dynamic-range.svg        (lesson page)
"""

from __future__ import annotations
import io
import re
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, Circle
from svg_font_stack import apply_font_stack

NAVY, BLUE, RED, GREEN, AMBER, GRAY = "#004a85", "#0067b9", "#b01e24", "#1d7a4d", "#8a5a00", "#5b6573"
INK, RULE = "#15202b", "#c7d2e0"
ROOT = Path(__file__).resolve().parents[2]
FIG, IMG = ROOT / "book/extras/slides/fig", ROOT / "book/extras/viz/img"

plt.rcParams.update({"svg.fonttype": "none", "font.size": 11, "text.color": INK,
                     "axes.edgecolor": GRAY, "axes.labelcolor": INK,
                     "xtick.color": GRAY, "ytick.color": GRAY})

STRAY_DB = -40.0          # the chamber specification, relative to the main-beam peak
LEVELS = (0.0, -20.0, -30.0)
FLOOR_DB = -42.0          # a plausible bench dynamic range for Lesson 11


def _svg(fig, alt):
    buf = io.StringIO()
    fig.savefig(buf, format="svg", bbox_inches="tight", pad_inches=0.04,
                facecolor="white")
    plt.close(fig)
    s = buf.getvalue()
    s = s[s.index("<svg"):]
    s = re.sub(r'<svg([^>]*)>', lambda m: f'<svg{m.group(1)} role="img" aria-label="{alt}">', s, count=1)
    return apply_font_stack(s)


def _m(x, fmt="{:+.1f}"):
    """A typographic minus, so the labels match the axis ticks."""
    return fmt.format(x).replace("-", "\u2212")


def swing(level_db, stray_db=STRAY_DB):
    """Largest and smallest dB error a stray of `stray_db` (relative to the
    main-beam peak) puts on a true level of `level_db`."""
    a, s = 10 ** (level_db / 20), 10 ** (stray_db / 20)
    return 20 * np.log10((a + s) / a), 20 * np.log10((a - s) / a)


def stray_ripple(stacked=False):
    """`stacked` draws the two panels one above the other, for the lesson page,
    where the figure sits in half a frame and a 3:1 strip sets its type too
    small to read. The deck gets the wide version."""
    if stacked:
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(6.4, 5.5),
                                       gridspec_kw={"height_ratios": [0.78, 1.0]})
    else:
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(9.6, 3.4),
                                       gridspec_kw={"width_ratios": [1.0, 1.5]})

    # ---- panel 1: the amplitudes, for the -30 dB sidelobe ----------------
    # Neil, 2026-09-17: "how do you get a 5.5dB swing from a -40dB stray field?
    # I truly don't understand". The panel used to show the circle and the two
    # dB errors and never the amplitudes, so the arithmetic looked like magic.
    # It now carries every number: the stray is 0.0100, the sidelobe is 0.0316,
    # and the sum and difference are what the two dB figures come from.
    lev = LEVELS[2]
    a = 1.0
    s = 10 ** ((STRAY_DB - lev) / 20)              # stray, relative to this signal
    amp_a, amp_s = 10 ** (lev / 20), 10 ** (STRAY_DB / 20)
    ax1.add_patch(FancyArrowPatch((0, 0), (a, 0), arrowstyle="-|>", mutation_scale=14,
                                  lw=2.6, color=NAVY, shrinkA=0, shrinkB=0, zorder=4))
    # anchored clear of the stray circle, whose left edge is at a - s
    ax1.text(a - s - 0.03, 0.14, "sidelobe, −30 dB", ha="right", color=NAVY,
             fontsize=11.5, fontweight="bold")
    ax1.text(a - s - 0.03, -0.19, f"amplitude {amp_a:.4f}", ha="right", color=NAVY, fontsize=11)
    ax1.add_patch(Circle((a, 0), s, fill=False, ec=RED, lw=1.8, ls=(0, (5, 4)), zorder=3))
    ang = 58
    ax1.add_patch(FancyArrowPatch((a, 0), (a + s * np.cos(np.radians(ang)), s * np.sin(np.radians(ang))),
                                  arrowstyle="-|>", mutation_scale=12, lw=2.0, color=RED,
                                  shrinkA=0, shrinkB=0, zorder=5))
    ax1.text(a + 0.08, 0.46, "stray, −40 dB", color=RED, fontsize=11.5,
             fontweight="bold", ha="left")
    ax1.text(a + 0.08, 0.31, f"amplitude {amp_s:.4f}", color=RED, fontsize=11, ha="left")
    for x, amp, ha in ((a - s, amp_a - amp_s, "right"), (a + s, amp_a + amp_s, "left")):
        db = 20 * np.log10(amp)
        ax1.plot([x], [0], "o", ms=6, color=RED, zorder=6)
        ax1.plot([x, x], [0, -0.34], color=RED, lw=1, ls=":", zorder=3)
        dx = 0.03 if ha == "left" else -0.03
        ax1.text(x + dx, -0.46, f"{amp:.4f}", color=RED, fontsize=11.5, ha=ha, fontweight="bold")
        ax1.text(x + dx, -0.63, _m(db, "{:.1f}") + " dB", color=RED, fontsize=11, ha=ha)
    ripple = 20 * np.log10((amp_a + amp_s) / (amp_a - amp_s))
    ax1.text(a, -0.88, f"{ripple:.1f} dB peak to trough", color=INK, fontsize=11.5,
             ha="center", fontweight="bold")
    ax1.set_xlim(-0.14, 1.86)
    ax1.set_ylim(-1.02, 0.70)
    ax1.set_aspect("equal")
    ax1.axis("off")

    # ---- panel 2: the dB interval at three true levels --------------------
    ys = np.arange(len(LEVELS))[::-1]
    for y, lev in zip(ys, LEVELS):
        hi, lo = swing(lev)
        ax2.plot([lo, hi], [y, y], color=RED, lw=8, solid_capstyle="butt", alpha=0.32, zorder=2)
        ax2.plot([0, 0], [y - 0.26, y + 0.26], color=NAVY, lw=2.4, zorder=4)
        for x in (lo, hi):
            ax2.plot([x, x], [y - 0.2, y + 0.2], color=RED, lw=2, zorder=4)
        ax2.text(hi + 0.18, y, _m(hi), color=RED, fontsize=11, va="center", ha="left")
        ax2.text(lo - 0.18, y, _m(lo), color=RED, fontsize=11, va="center", ha="right")
    ax2.set_yticks(ys)
    ax2.set_yticklabels(["main beam\npeak", "sidelobe\nat −20 dB", "sidelobe\nat −30 dB"],
                        fontsize=11, color=INK)
    ax2.set_xlabel("error on the reading (dB)", color=INK)
    ax2.set_xlim(-4.3, 3.4)
    ax2.set_ylim(-0.7, len(LEVELS) - 0.3)
    ax2.axvline(0, color=NAVY, lw=1, alpha=0.35, zorder=1)
    for side in ("top", "right", "left"):
        ax2.spines[side].set_visible(False)
    ax2.tick_params(axis="y", length=0)
    ax2.grid(axis="x", color=RULE, lw=0.7)
    ax2.set_axisbelow(True)

    if stacked:
        fig.tight_layout(rect=(0, 0, 1, 0.93), h_pad=3.0)
        fig.text(0.02, 0.975, "the amplitudes add, at any phase", color=NAVY,
                 fontsize=13, fontweight="bold", ha="left")
        fig.text(0.02, 0.500, "so the reading is an interval, not a number", color=NAVY,
                 fontsize=13, fontweight="bold", ha="left")
    else:
        fig.tight_layout(rect=(0, 0, 1, 0.90))
        fig.text(0.015, 0.955, "the amplitudes add, at any phase", color=NAVY,
                 fontsize=12.5, fontweight="bold", ha="left")
        fig.text(0.44, 0.955, "so the reading is an interval, not a number", color=NAVY,
                 fontsize=12.5, fontweight="bold", ha="left")
    return _svg(fig, "Left: a phasor diagram in which a stray signal forty decibels below "
                     "the main beam adds to a sidelobe thirty decibels down at any phase, so "
                     "the measured amplitude lies anywhere on a circle around the true value, "
                     "between plus 2.4 and minus 3.3 decibels. Right: the resulting error "
                     "interval at three true levels, negligible at the main beam peak and "
                     "several decibels wide on a sidelobe thirty decibels down.")


def pattern_db(theta_deg, n=8.0):
    """A uniform line source n wavelengths long, normalized, in dB."""
    u = np.pi * n * np.sin(np.radians(theta_deg))
    f = np.where(np.abs(u) < 1e-9, 1.0, np.sin(u) / np.where(u == 0, 1, u))
    return 20 * np.log10(np.maximum(np.abs(f), 1e-12))


def dynamic_range():
    fig, ax = plt.subplots(figsize=(9.2, 4.0))
    th = np.linspace(-52, 52, 8001)
    true_db = pattern_db(th, n=3.0)
    meas_db = 10 * np.log10(10 ** (true_db / 10) + 10 ** (FLOOR_DB / 10))

    ax.plot(th, meas_db, color=NAVY, lw=2.4, label="what the receiver records", zorder=4)
    ax.plot(th, true_db, color=GRAY, lw=1.5, ls=(0, (5, 4)), label="the antenna's pattern", zorder=5)
    ax.axhline(FLOOR_DB, color=RED, lw=1.8, ls=(0, (4, 3)), zorder=2)
    ax.text(51, FLOOR_DB + 3.2, "noise floor, " + _m(FLOOR_DB, "{:.0f}") + " dB", color=RED,
            fontsize=11, ha="right", fontweight="bold",
            bbox=dict(fc="white", ec="none", alpha=0.92, pad=1.5))

    ax.annotate("", (0, 0), (0, FLOOR_DB),
                arrowprops=dict(arrowstyle="<|-|>", color=GREEN, lw=1.8, shrinkA=0, shrinkB=0))
    ax.text(-1.6, -21, "dynamic range\n42 dB", color=GREEN, fontsize=11,
            fontweight="bold", ha="right", va="center")

    box = dict(fc="white", ec="none", alpha=0.92, pad=1.5)
    ax.annotate("first sidelobe, −13 dB:\n29 dB clear of the floor", (28.8, -13.3), (23, -4.5),
                color=NAVY, fontsize=10.5, ha="left", bbox=box,
                arrowprops=dict(arrowstyle="->", color=NAVY, lw=1.2))
    ax.annotate("the nulls read the floor,\nnot the antenna", (19.4, -41), (3.0, -31),
                color=RED, fontsize=10.5, ha="left", bbox=box,
                arrowprops=dict(arrowstyle="->", color=RED, lw=1.2))

    ax.set_xlabel("angle from boresight (degrees)", color=INK)
    ax.set_ylabel("relative power (dB)", color=INK)
    ax.set_xlim(-52, 52)
    ax.set_ylim(-56, 6)
    ax.set_yticks([0, -10, -20, -30, -40, -50])
    ax.grid(color=RULE, lw=0.7)
    ax.set_axisbelow(True)
    for side in ("top", "right"):
        ax.spines[side].set_visible(False)
    ax.legend(loc="upper left", frameon=False, fontsize=10.5, labelcolor=INK)
    fig.tight_layout()
    return _svg(fig, "A measured antenna pattern drawn against the antenna's true pattern. "
                     "The two agree through the main beam and the first sidelobes; below the "
                     "receiver's forty-two decibel noise floor the measured trace flattens "
                     "onto the floor, so the nulls read the floor rather than the antenna.")


def main():
    # Only the stacked page copy: the ripple arithmetic is depth on the
    # absorber frame, not a slide, so nothing on the deck loads a wide one.
    (IMG / "L09-stray-ripple.svg").write_text(stray_ripple(stacked=True), encoding="utf-8")
    dr = dynamic_range()
    (FIG / "L09-dynamic-range.svg").write_text(dr, encoding="utf-8")
    (IMG / "L09-dynamic-range.svg").write_text(dr, encoding="utf-8")
    print("wrote L09-stray-ripple (stacked page copy) and L09-dynamic-range")


if __name__ == "__main__":
    main()
