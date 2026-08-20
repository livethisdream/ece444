#!/usr/bin/env python3
"""Generate the L06 radiation-pattern deck figures as inline SVG.

L06:
  - L06-line-source-sinc  : uniform line source (L = 6 lambda) power pattern,
                            rectilinear, first null / HPBW / -13.3 dB SLL marked
  - L06-three-patterns    : polar overlay of the three distributions L06 teaches
                            (infinitesimal dipole, half-wave dipole, uniform
                            line source L = 2 lambda), normalized, dB to -30

Same export convention as scripts/graphics/plots.py: SVG with live <text>
(svg.fonttype='none'), font-family rewritten to 'inherit' so the injected
figure picks up the deck font, transparent background, USAFA palette, and
**no baked equations** (deck figures carry words and numbers only).

    python scripts/graphics/l06_patterns.py
    -> writes book/extras/slides/fig/{L06-line-source-sinc,L06-three-patterns}.svg

Illustrative patterns computed from the closed forms in the lesson, not
measured data.
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
SLIDE_BG = "#fafaf7"          # deck --slide-bg, for label knock-outs over a curve
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


def _db(x: np.ndarray, floor: float = -30.0) -> np.ndarray:
    return np.clip(20 * np.log10(np.clip(np.abs(x), 1e-9, None)), floor, None)


def line_source_sinc() -> None:
    """Uniform line source, L = 6 lambda, plotted against angle off broadside.

    Carries the three numbers the slide quotes: first null at lambda/L, HPBW
    from 0.886 lambda/L, and the -13.3 dB first sidelobe that never moves."""
    LL = 6.0                                          # length in wavelengths
    g = np.linspace(-np.deg2rad(35), np.deg2rad(35), 6001)   # angle off broadside
    X = np.pi * LL * np.sin(g)
    with np.errstate(divide="ignore", invalid="ignore"):
        F = np.sin(X) / X
    F = np.nan_to_num(F, nan=1.0)
    deg, dB = np.rad2deg(g), _db(F, -40.0)

    fig, ax = plt.subplots(figsize=(6.6, 3.4))
    ax.plot(deg, dB, color=NAVY, lw=2.2, zorder=4)
    ax.set_xlim(-35, 35); ax.set_ylim(-40, 11)
    ax.set_xlabel("Angle off broadside  (deg)")
    ax.set_ylabel("Relative power  (dB)")
    ax.set_xticks(range(-30, 31, 10))
    ax.set_yticks([0, -10, -20, -30, -40])
    ax.grid(color=RULE, linewidth=0.8)
    for sp in ("top", "right"):
        ax.spines[sp].set_visible(False)

    hp = np.rad2deg(np.arcsin(0.886 / (2 * LL)))      # half of 0.886 lambda/L
    fn = np.rad2deg(np.arcsin(1.0 / LL))              # first null
    sl = np.rad2deg(np.arcsin(1.4303 / LL))           # first sidelobe peak

    # HPBW, measured across the -3 dB points
    ax.annotate("", xy=(hp, -3), xytext=(-hp, -3),
                arrowprops=dict(arrowstyle="<->", color=RED, lw=1.6))
    ax.text(0, 0.8, "beamwidth  8.5°", color=RED, ha="center", va="bottom",
            fontsize=12.5, fontweight="bold")

    # first null
    ax.plot([fn, fn], [-40, -34], color=GREEN, lw=1.6)
    ax.annotate("first null  9.6°", xy=(fn, -34), xytext=(fn + 2.5, -25.5),
                color=GREEN, fontsize=12, fontweight="bold", ha="left",
                bbox=dict(boxstyle="round,pad=0.18", fc=SLIDE_BG, ec="none", alpha=0.92),
                arrowprops=dict(arrowstyle="->", color=GREEN, lw=1.2))

    # first sidelobe: the level that never moves
    ax.axhline(-13.3, color=ORANGE, lw=1.2, ls=(0, (4, 3)), zorder=2)
    ax.annotate("first sidelobe  −13.3 dB\n(same at any length)",
                xy=(sl, -13.3), xytext=(15.5, -9.5),
                color=ORANGE, fontsize=11.5, fontweight="bold", ha="left",
                arrowprops=dict(arrowstyle="->", color=ORANGE, lw=1.2))

    ax.text(-34, 9.8, "Uniform line source, 6 wavelengths long",
            color=GREY, fontsize=12, ha="left", va="top")
    finalize(fig, "L06-line-source-sinc")


def three_patterns() -> None:
    """The three current distributions of L06 on one polar cut, normalized,
    radial axis in dB to -30. z is up, so broadside is left/right."""
    th = np.linspace(0, 2 * np.pi, 4001)
    s, c = np.sin(th), np.cos(th)

    with np.errstate(divide="ignore", invalid="ignore"):
        f_hw = np.cos((np.pi / 2) * c) / s            # half-wave dipole
    f_hw = np.nan_to_num(f_hw, nan=0.0, posinf=0.0, neginf=0.0)

    u = 2 * np.pi * c                                 # uniform line, L = 2 lambda
    with np.errstate(divide="ignore", invalid="ignore"):
        f_ln = np.sin(u) / u
    f_ln = np.nan_to_num(f_ln, nan=1.0)

    fig = plt.figure(figsize=(8.0, 3.6))
    ax = fig.add_axes((0.01, 0.02, 0.52, 0.96), projection="polar")
    ax.set_theta_zero_location("N"); ax.set_theta_direction(-1)
    ax.set_ylim(-30, 0.5)
    ax.set_yticks([-30, -20, -10, 0])
    ax.set_yticklabels(["-30", "-20", "-10", "0 dB"], fontsize=10)
    ax.set_rlabel_position(112)
    ax.set_thetagrids(range(0, 360, 30), fontsize=10)
    ax.grid(color=RULE, linewidth=0.8)

    ax.plot(th, _db(np.abs(s)), color=GREEN, lw=2.0, ls=(0, (6, 3)),
            label="Infinitesimal dipole\nbeamwidth 90°,  1.76 dBi")
    ax.plot(th, _db(np.abs(f_hw)), color=ORANGE, lw=2.2,
            label="Half-wave dipole\nbeamwidth 78°,  2.15 dBi")
    ax.plot(th, _db(np.abs(f_ln)), color=NAVY, lw=2.4,
            label="Uniform line source, 2 wavelengths\nbeamwidth 25.6°,  6.2 dBi")
    ax.legend(loc="center left", bbox_to_anchor=(1.03, 0.58), fontsize=11.5,
              handlelength=1.7, labelspacing=1.15, borderaxespad=0.0)

    fig.text(0.565, 0.09, "Wire axis vertical.\nBroadside is left and right.",
             color=GREY, fontsize=11, ha="left", va="bottom", linespacing=1.4)
    finalize(fig, "L06-three-patterns")


def main() -> int:
    OUT.mkdir(parents=True, exist_ok=True)
    line_source_sinc()
    three_patterns()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
