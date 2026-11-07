#!/usr/bin/env python3
"""Generate the L21 lesson figures: the kit's sweep against a walked trace.

L21:
  - L21-sweep-walk-0  : source at boresight, beam swept (the Rectangular
                        plot, against commanded steer angle) beside the beam
                        held at 0 deg with the source walked (against true
                        source angle). Both in dBc of their own peak.
  - L21-sweep-walk-30 : the same pair at 30 deg: the sweep with the source at
                        30 deg, and the walk with the beam held at 30 deg.

Model, matching the lesson text: N = 8 uniform, d = 14 mm, 10.3 GHz
(lambda = 29.1 mm). The sweep steps the element-to-element phase one
2.8125 deg LSB per point and reads |AF|^2 at a fixed source, so the element
pattern is one constant and drops out of the dBc trace; a floor 23 dB below
the peak (L20 Lab) is added in power. The walk reads EF x AF with an ideal
cos(theta) element power pattern and a floor 27 dB down (the L21 Lab's 25-30
dBc behind the board).

    python3 scripts/graphics/m3_l21_sweep_walk.py
    -> writes book/extras/viz/img/{L21-sweep-walk-0,L21-sweep-walk-30}.svg
"""

from __future__ import annotations
import io
from pathlib import Path

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from svg_font_stack import apply_font_stack

NAVY, ORANGE, GRAY = "#004a85", "#d9822b", "#5a5a5a"
INK, RULE = "#1a1a1a", "#c7d2e0"
OUT = Path(__file__).resolve().parents[2] / "book/extras/viz/img"

C = 299792458.0
FREQ = 10.3e9
LAM = C / FREQ
D = 0.014
N = 8
LSB = np.radians(2.8125)
KD = 2 * np.pi * D / LAM
SWEEP_FLOOR_DB = -23.0
WALK_FLOOR_DB = -27.0
YMIN = -32.0

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


def af_power(psi):
    """|AF|^2 of the uniform N-element array, peak 1."""
    den = N * np.sin(psi / 2)
    small = np.abs(den) < 1e-12
    af = np.where(small, 1.0, np.sin(N * psi / 2) / np.where(small, 1.0, den))
    return af ** 2


def with_floor_db(p, floor_db):
    """Add a floor in power, then express in dB of the trace's own peak."""
    q = p + 10 ** (floor_db / 10)
    return 10 * np.log10(q / q.max())


def sweep(source_deg):
    """The Rectangular plot: commanded angle and dBc, one point per LSB."""
    k = np.arange(-400, 401)
    s0 = k * LSB / KD
    s0 = s0[np.abs(s0) <= 1.0]
    psi = KD * (np.sin(np.radians(source_deg)) - s0)
    return np.degrees(np.arcsin(s0)), with_floor_db(af_power(psi), SWEEP_FLOOR_DB)


def walk(beam_deg):
    """A walked trace: true source angle and dBc, element pattern included."""
    th = np.radians(np.linspace(-90, 90, 3601))
    psi = KD * (np.sin(th) - np.sin(np.radians(beam_deg)))
    ef = np.clip(np.cos(th), 0, None)
    return np.degrees(th), with_floor_db(af_power(psi) * ef, WALK_FLOOR_DB)


def draw(angle_deg: float, name: str) -> None:
    fig, ax = plt.subplots(figsize=(7.4, 3.6))
    xw, yw = walk(angle_deg)
    xs, ys = sweep(angle_deg)
    ax.plot(xw, yw, color=NAVY, lw=2.0, label="walk: beam held, source moved")
    ax.plot(xs, ys, color=ORANGE, lw=0.9, alpha=0.9)
    ax.plot(xs, ys, "o", color=ORANGE, ms=2.6, label="sweep: source held, beam stepped")
    ax.set_xlim(-90, 90)
    ax.set_ylim(YMIN, 2)
    ax.set_xticks(np.arange(-90, 91, 30))
    ax.set_yticks(np.arange(-30, 1, 10))
    ax.set_xlabel("angle (deg)")
    ax.set_ylabel("level (dBc)")
    ax.grid(color=RULE, lw=0.7)
    ax.spines[["top", "right"]].set_visible(False)
    ax.legend(loc="upper center", bbox_to_anchor=(0.5, -0.2), ncol=2,
              fontsize=11.5, handlelength=1.6, columnspacing=1.4)
    finalize(fig, name)


def report() -> None:
    """Print the numbers the lesson quotes, for checking against the text."""
    for a in (0, 30):
        xw, yw = walk(a)
        xs, ys = sweep(a)
        pk = int(np.argmax(yw))
        lo = [i for i in range(1, len(yw) - 1) if yw[i] > yw[i - 1] and yw[i] >= yw[i + 1]]
        print(f"walk {a}: peak {xw[pk]:.1f}",
              [(round(xw[i], 1), round(yw[i], 1)) for i in lo if yw[i] > -20])
        lo = [i for i in range(1, len(ys) - 1) if ys[i] > ys[i - 1] and ys[i] >= ys[i + 1]]
        print(f"sweep {a}:", [(round(xs[i], 1), round(ys[i], 1)) for i in lo if ys[i] > -20])


if __name__ == "__main__":
    report()
    draw(0.0, "L21-sweep-walk-0")
    draw(30.0, "L21-sweep-walk-30")
