#!/usr/bin/env python3
"""Generate the L20 (Array Factor and Beamwidth Theory) deck figures as SVG.

L20:
  - L20-beamwidth-anatomy   : N = 8, d = 0.481 lambda uniform array, broadside,
                              dB pattern with HPBW, first nulls, FNBW and the
                              -13 dB first sidelobe marked
  - L20-scan-broadening     : the same array steered to 0, 30 and 60 degrees,
                              labelled with the beamwidth read off each curve
  - L20-aperture-vs-beamwidth : HPBW against aperture length in wavelengths,
                              broadside and 45-degree scan, with the PHASER
                              array and a 5-degree design target marked

Same export convention as scripts/graphics/l06_patterns.py: SVG with live
<text> (svg.fonttype='none'), font-family rewritten to 'inherit' so the
injected figure picks up the deck font, transparent background, USAFA palette,
and no baked equations (deck figures carry words and numbers only).

    python3 scripts/graphics/m3_l20_beamwidth.py
    -> writes book/extras/slides/fig/L20-*.svg  (and copies to viz/img/)

Patterns are the closed-form uniform array factor, not measured data.
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
SLIDE_BG = "#fafaf7"
ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "book/extras/slides/fig"
OUT2 = ROOT / "book/extras/viz/img"

LAM = 3e8 / 10.3e9 * 1000.0      # mm, the workshop's 10.3 GHz
DEL = 14.0 / LAM                 # PHASER element spacing in wavelengths

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
    s = s[s.index("<svg"):]
    s = re.sub(r"font-family:[^;}]*", "font-family:inherit", s)
    for dest in (OUT, OUT2):
        dest.mkdir(parents=True, exist_ok=True)
        (dest / f"{name}.svg").write_text(s, encoding="utf-8")
    print(f"wrote {name}.svg -> {OUT}, {OUT2}")


def af_db(N, dl, deg, th0=0.0, floor=-40.0):
    psi = 2 * np.pi * dl * (np.sin(np.deg2rad(deg)) - np.sin(np.deg2rad(th0)))
    den = N * np.sin(psi / 2)
    num = np.sin(N * psi / 2)
    a = np.where(np.abs(den) < 1e-12, 1.0, num / np.where(np.abs(den) < 1e-12, 1.0, den))
    return np.clip(20 * np.log10(np.clip(np.abs(a), 1e-9, None)), floor, None)


def hpbw_exact(N, dl, th0=0.0):
    """Half-power width read off the pattern itself, in degrees."""
    deg = np.linspace(-90, 90, 400001)
    db = af_db(N, dl, deg, th0, floor=-200.0)
    i = int(np.argmax(np.where(np.abs(deg - th0) < 35, db, -300)))
    edges = []
    for step in (-1, +1):
        j = i
        while 0 <= j < len(deg) and db[j] > -3:
            j += step
        edges.append(deg[j])
    return edges[1] - edges[0]


def beamwidth_anatomy() -> None:
    """Every number L20 extracts from the closed form, on one broadside cut."""
    N, dl = 8, DEL
    deg = np.linspace(-90, 90, 8001)
    db = af_db(N, dl, deg)

    fig, ax = plt.subplots(figsize=(7.0, 3.6))
    ax.plot(deg, db, color=NAVY, lw=2.2, zorder=4)
    ax.set_xlim(-90, 90); ax.set_ylim(-40, 12)
    ax.set_xlabel("Angle from broadside  (deg)")
    ax.set_ylabel("Relative power  (dB)")
    ax.set_xticks(range(-90, 91, 30))
    ax.set_yticks([0, -10, -20, -30, -40])
    ax.grid(color=RULE, linewidth=0.8)
    for sp in ("top", "right"):
        ax.spines[sp].set_visible(False)

    hp = 13.2 / 2
    ax.fill_between([-hp, hp], -40, 12, color=GREEN, alpha=0.10, zorder=1)
    ax.annotate("", xy=(hp, -3), xytext=(-hp, -3),
                arrowprops=dict(arrowstyle="<->", color=GREEN, lw=1.6))
    ax.text(0, 1.0, "half-power width  13.2°", color=GREEN, ha="center", va="bottom",
            fontsize=12.5, fontweight="bold")

    nulls = [np.degrees(np.arcsin(m / (N * dl))) for m in (1, 2, 3)]
    for s in (+1, -1):
        for x in nulls:
            ax.plot([s * x, s * x], [-40, -35.5], color=RED, lw=1.8, zorder=5)
    ax.annotate("first null  15.1°", xy=(nulls[0], -35.5), xytext=(24, -30.5),
                color=RED, fontsize=12, fontweight="bold", ha="left",
                bbox=dict(boxstyle="round,pad=0.18", fc=SLIDE_BG, ec="none", alpha=0.92),
                arrowprops=dict(arrowstyle="->", color=RED, lw=1.2))
    ax.annotate("", xy=(nulls[0], -24.5), xytext=(-nulls[0], -24.5),
                arrowprops=dict(arrowstyle="<->", color=RED, lw=1.4))
    ax.text(0, -23.8, "null-to-null  30.1°", color=RED, ha="center", va="bottom",
            fontsize=12, fontweight="bold",
            bbox=dict(boxstyle="round,pad=0.16", fc=SLIDE_BG, ec="none", alpha=0.92))

    ax.axhline(-12.8, color=ORANGE, lw=1.2, ls=(0, (4, 3)), zorder=2)
    ax.annotate("first sidelobe  −13 dB", xy=(21.5, -12.8), xytext=(40, -7.5),
                color=ORANGE, fontsize=11.5, fontweight="bold", ha="left",
                bbox=dict(boxstyle="round,pad=0.18", fc=SLIDE_BG, ec="none", alpha=0.92),
                arrowprops=dict(arrowstyle="->", color=ORANGE, lw=1.2))

    ax.text(-88, 11.0, "8 elements, half-wavelength spacing, broadside",
            color=GREY, fontsize=12, ha="left", va="top")
    finalize(fig, "L20-beamwidth-anatomy")


def scan_broadening() -> None:
    """The same aperture costs beamwidth as it steers off broadside."""
    N, dl = 8, DEL
    deg = np.linspace(-90, 90, 12001)
    fig, ax = plt.subplots(figsize=(7.0, 3.5))
    for th0, color, lab in ((0, NAVY, "broadside"), (30, BLUE, "30° scan"), (60, ORANGE, "60° scan")):
        db = af_db(N, dl, deg, th0)
        w = hpbw_exact(N, dl, th0)
        ax.plot(deg, db, color=color, lw=2.1, zorder=4,
                label=f"{lab}  —  {w:.0f}° wide")
    ax.axhline(-3, color=GREEN, lw=1.2, ls=(0, (4, 3)), zorder=2)
    ax.text(-88, -2.4, "half-power level", color=GREEN, fontsize=11,
            fontweight="bold", ha="left", va="bottom",
            bbox=dict(boxstyle="round,pad=0.16", fc=SLIDE_BG, ec="none", alpha=0.92))

    ax.set_xlim(-90, 90); ax.set_ylim(-40, 15)
    ax.set_xlabel("Angle from broadside  (deg)")
    ax.set_ylabel("Relative power  (dB)")
    ax.set_xticks(range(-90, 91, 30))
    ax.set_yticks([0, -10, -20, -30, -40])
    ax.grid(color=RULE, linewidth=0.8)
    for sp in ("top", "right"):
        ax.spines[sp].set_visible(False)
    ax.legend(loc="upper left", fontsize=11.5, handlelength=1.4, borderaxespad=0.2,
              ncol=3, columnspacing=1.1, frameon=True, framealpha=0.94,
              facecolor=SLIDE_BG, edgecolor="none")
    finalize(fig, "L20-scan-broadening")


def aperture_vs_beamwidth() -> None:
    """The design chart: beamwidth is set by aperture length, in wavelengths."""
    L = np.linspace(1.5, 30, 900)
    hp0 = np.degrees(0.886 / L)
    hp45 = hp0 / np.cos(np.deg2rad(45))

    fig, ax = plt.subplots(figsize=(6.8, 3.5))
    ax.plot(L, hp0, color=NAVY, lw=2.3, label="broadside", zorder=4)
    ax.plot(L, hp45, color=ORANGE, lw=2.0, ls=(0, (5, 3)), label="steered to 45°", zorder=4)

    ax.set_xscale("log"); ax.set_yscale("log")
    ax.set_xlim(1.5, 30); ax.set_ylim(1.4, 40)
    ax.set_xlabel("Aperture length  (wavelengths)")
    ax.set_ylabel("Half-power beamwidth  (deg)")
    ax.set_xticks([2, 3, 5, 10, 20, 30]); ax.set_yticks([2, 3, 5, 10, 20, 30])
    ax.get_xaxis().set_major_formatter(matplotlib.ticker.ScalarFormatter())
    ax.get_yaxis().set_major_formatter(matplotlib.ticker.ScalarFormatter())
    ax.get_xaxis().set_minor_formatter(matplotlib.ticker.NullFormatter())
    ax.get_yaxis().set_minor_formatter(matplotlib.ticker.NullFormatter())
    ax.grid(which="both", color=RULE, linewidth=0.8)
    for sp in ("top", "right"):
        ax.spines[sp].set_visible(False)

    ax.plot([3.85], [13.2], marker="o", ms=7, color=NAVY, zorder=6)
    ax.annotate("PHASER, 8 elements\n3.9 wavelengths, 13.2°", xy=(3.85, 13.2), xytext=(1.75, 3.1),
                color=NAVY, fontsize=11.5, fontweight="bold", ha="left",
                bbox=dict(boxstyle="round,pad=0.18", fc=SLIDE_BG, ec="none", alpha=0.92),
                arrowprops=dict(arrowstyle="->", color=NAVY, lw=1.2))
    ax.plot([10.15], [5.0], marker="o", ms=7, color=RED, zorder=6)
    ax.annotate("5° target\n10.2 wavelengths", xy=(10.15, 5.0), xytext=(12.5, 12.0),
                color=RED, fontsize=11.5, fontweight="bold", ha="left",
                bbox=dict(boxstyle="round,pad=0.18", fc=SLIDE_BG, ec="none", alpha=0.92),
                arrowprops=dict(arrowstyle="->", color=RED, lw=1.2))
    ax.legend(loc="lower left", fontsize=11.5, handlelength=1.8, borderaxespad=0.4)
    finalize(fig, "L20-aperture-vs-beamwidth")


if __name__ == "__main__":
    beamwidth_anatomy()
    scan_broadening()
    aperture_vs_beamwidth()
