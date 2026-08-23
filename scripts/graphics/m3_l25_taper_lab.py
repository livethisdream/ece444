#!/usr/bin/env python3
"""L25 (Tapering Lab) deck figures.

  - L25-taper-traces  : the four preset sweeps as the GUI draws them
                        (2.8125 deg grid, -23 dBc floor, light noise)
  - L25-gain-bars     : the four presets' element-gain bars
  - L25-two-numbers   : plotted peak drop vs directivity loss, Hann preset
  - L25-custom-target : a mild custom taper against the design target

Array model: N = 8, d = 14 mm at 10.3 GHz (d/lambda = 0.481), broadside,
isotropic elements. Traces are the array factor sampled on the sweep grid,
normalized to the uniform-taper peak, with the noise floor and a small
amount of trace noise added so the figures read like measurements.

No equations in any figure (deck rule) -- axis labels, legends and short
value tags only.

    python3 scripts/graphics/m3_l25_taper_lab.py
    -> book/extras/slides/fig/L25-*.svg  and  book/extras/viz/img/L25-*.svg
"""

from __future__ import annotations

import io
import re
from pathlib import Path

import matplotlib
import numpy as np

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

NAVY, BLUE, RED, GREEN, ORANGE, GREY = (
    "#004a85", "#0067b9", "#b01e24", "#1d7a4d", "#e67e22", "#5a5a5a")
INK, RULE = "#1a1a1a", "#c7d2e0"
ROOT = Path(__file__).resolve().parents[2]
FIG = ROOT / "book/extras/slides/fig"
IMG = ROOT / "book/extras/viz/img"

DL = 0.481          # d / lambda at 10.3 GHz, d = 14 mm
NEL = 8
STEP = 2.8125       # sweep grid = ADAR1000 phase LSB expressed as steer resolution
FLOOR = -23.0       # noise floor, dB below the uniform-taper peak

PRESETS = {
    "Uniform":   [100, 100, 100, 100, 100, 100, 100, 100],
    "Hann":      [12, 43, 77, 100, 100, 77, 43, 12],
    "Blackman":  [6, 27, 66, 100, 100, 66, 27, 6],
    "Chebyshev": [4, 23, 62, 100, 100, 62, 23, 4],
}
COLORS = {"Uniform": NAVY, "Hann": BLUE, "Blackman": GREEN, "Chebyshev": ORANGE}

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


def finalize(fig, name: str, also_img: bool = False) -> None:
    buf = io.StringIO()
    fig.savefig(buf, format="svg", transparent=True, bbox_inches="tight", pad_inches=0.06)
    plt.close(fig)
    s = buf.getvalue()
    s = s[s.index("<svg"):]
    s = re.sub(r"font-family:[^;}]*", "font-family:inherit", s)
    for d in (FIG,) + ((IMG,) if also_img else ()):
        d.mkdir(parents=True, exist_ok=True)
        (d / f"{name}.svg").write_text(s, encoding="utf-8")
        print(f"wrote {d / (name + '.svg')}")


def af(gains, theta_deg):
    """|array factor| of the 8-element line array, elements weighted by gains (%)."""
    a = np.asarray(gains, float) / 100.0
    n = np.arange(NEL)
    psi = 2 * np.pi * DL * np.outer(np.sin(np.deg2rad(theta_deg)), n)
    return np.abs((np.exp(1j * psi) * a).sum(axis=1))


UNI_PEAK = af(PRESETS["Uniform"], np.linspace(-90, 90, 20001)).max()


def swept(gains, seed=7):
    """The trace the sweep produces: grid samples, uniform-peak reference,
    noise floor, light noise."""
    th = np.arange(-90, 90 + 1e-9, STEP)
    p = (af(gains, th) / UNI_PEAK) ** 2
    rng = np.random.default_rng(seed)
    p = p + 10 ** (FLOOR / 10) * (0.55 + 0.9 * rng.random(th.size))
    return th, 10 * np.log10(p)


def taper_traces() -> None:
    fig, ax = plt.subplots(figsize=(7.6, 4.0))
    for i, (name, g) in enumerate(PRESETS.items()):
        th, db = swept(g, seed=3 + i)
        ax.plot(th, db, color=COLORS[name], lw=2.0 if name == "Uniform" else 1.7,
                label=name)
    ax.axhline(FLOOR, color=GREY, lw=1.1, ls=(0, (4, 3)))
    ax.text(-58, FLOOR - 2.6, "noise floor", color=GREY, fontsize=11.5)
    ax.set_xlim(-60, 60)
    ax.set_ylim(-30, 3)
    ax.set_xticks(range(-60, 61, 15))
    ax.set_xlabel("Commanded steer angle  (deg)")
    ax.set_ylabel("Received power  (dB rel. uniform peak)")
    ax.grid(color=RULE, linewidth=0.8)
    for sp in ("top", "right"):
        ax.spines[sp].set_visible(False)
    ax.legend(loc="upper right", fontsize=12, handlelength=1.6)
    finalize(fig, "L25-taper-traces", also_img=True)


def gain_bars() -> None:
    fig, axes = plt.subplots(1, 4, figsize=(9.4, 2.5), sharey=True)
    x = np.arange(1, NEL + 1)
    for ax, (name, g) in zip(axes, PRESETS.items()):
        ax.bar(x, g, color=COLORS[name], width=0.72)
        ax.set_title(name, fontsize=13, color=INK, pad=6)
        ax.set_ylim(0, 112)
        ax.set_xticks([1, 4, 8])
        ax.set_xlabel("Element", fontsize=11.5)
        ax.grid(axis="y", color=RULE, linewidth=0.8)
        ax.set_axisbelow(True)
        for sp in ("top", "right"):
            ax.spines[sp].set_visible(False)
    axes[0].set_ylabel("Gain  (%)", fontsize=12)
    fig.subplots_adjust(wspace=0.18)
    finalize(fig, "L25-gain-bars")


def two_numbers() -> None:
    """Two bars for the Hann preset: what the sweep plot drops, and what the
    array's directivity drops. Values only -- the argument lives in the text."""
    fig, ax = plt.subplots(figsize=(6.6, 3.3))
    labels = ["Plotted peak", "Directivity"]
    vals = [-4.7, -1.2]
    cols = [ORANGE, GREEN]
    bars = ax.barh(labels, vals, color=cols, height=0.40)
    for b, v, c in zip(bars, vals, cols):
        ax.text(v - 0.18, b.get_y() + b.get_height() / 2, f"−{abs(v):.1f} dB",
                va="center", ha="right", color=c, fontsize=13.5, fontweight="bold")
    ax.axvline(0, color=GREY, lw=1.2)
    ax.set_xlim(-6.0, 1.2)
    ax.set_xlabel("Change from uniform  (dB)")
    ax.set_xticks([-6, -5, -4, -3, -2, -1, 0])
    ax.grid(axis="x", color=RULE, linewidth=0.8)
    ax.set_axisbelow(True)
    ax.invert_yaxis()
    for sp in ("top", "right", "left"):
        ax.spines[sp].set_visible(False)
    ax.tick_params(axis="y", length=0, labelsize=13)
    ax.annotate("", xy=(-4.7, 0.5), xytext=(-1.2, 0.5),
                arrowprops=dict(arrowstyle="<->", color=RED, lw=1.5))
    ax.text(-2.95, 0.40, "3.5 dB", color=RED, ha="center", va="bottom",
            fontsize=12.5, fontweight="bold")
    finalize(fig, "L25-two-numbers", also_img=True)


def custom_target() -> None:
    """A mild custom taper (end elements at 40%) against the uniform trace."""
    u = np.abs(np.arange(NEL) - 3.5) / 3.5
    g = 100 * (1 - 0.60 * u)
    fig, ax = plt.subplots(figsize=(7.4, 3.7))
    th, db = swept(PRESETS["Uniform"], seed=3)
    ax.plot(th, db, color=GREY, lw=1.4, label="Uniform")
    th, db = swept(g, seed=11)
    ax.plot(th, db, color=NAVY, lw=2.1, label="Custom  40 / 57 / 74 / 91 %")
    ax.axhline(-20, color=RED, lw=1.3, ls=(0, (5, 3)), label="Design target")
    ax.axhline(FLOOR, color=GREY, lw=1.1, ls=(0, (4, 3)), label="Noise floor")
    ax.set_xlim(-60, 60)
    ax.set_ylim(-30, 3)
    ax.set_xticks(range(-60, 61, 15))
    ax.set_xlabel("Commanded steer angle  (deg)")
    ax.set_ylabel("Received power  (dB rel. uniform peak)")
    ax.grid(color=RULE, linewidth=0.8)
    for sp in ("top", "right"):
        ax.spines[sp].set_visible(False)
    ax.legend(loc="upper center", bbox_to_anchor=(0.5, -0.24), ncol=4,
              fontsize=11.5, handlelength=1.7, columnspacing=1.4)
    finalize(fig, "L25-custom-target", also_img=True)


if __name__ == "__main__":
    taper_traces()
    gain_bars()
    two_numbers()
    custom_target()
