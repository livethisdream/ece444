#!/usr/bin/env python3
"""Generate the L02 deck data-plots as inline SVG.

Three plots that were committed only as foreign-font PNGs:
  - gain-pattern-polar : normalized patterns, isotropic/dipole/horn/dish
  - rectilinear        : uniform line-source sinc^2, HPBW/FNBW/SLL annotated
  - vswr               : VSWR vs reflection-coefficient magnitude

Exported as SVG with live <text> (svg.fonttype='none'), then font-family is
rewritten to 'inherit' so the injected figure picks up the deck's Source Sans
Pro. Transparent background, USAFA palette, no baked formulas (axis labels /
legends / pattern annotations only).

    python scripts/graphics/plots.py
    -> writes book/extras/slides/fig/{gain-pattern-polar,rectilinear,vswr}.svg

These are illustrative patterns with representative parameters, not measured data.
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
    s = s[s.index("<svg"):]                                   # drop xml decl/doctype
    s = re.sub(r"font-family:[^;}]*", "font-family:inherit", s)  # inherit deck font
    (OUT / f"{name}.svg").write_text(s, encoding="utf-8")
    print(f"wrote {OUT / (name + '.svg')}")


def gain_polar() -> None:
    phi = np.linspace(0, 2 * np.pi, 2001)          # 0 = up (North)
    def dB(p): return 10 * np.log10(np.clip(p, 1e-4, None))

    iso = np.ones_like(phi)                          # isotropic
    # lambda/2 dipole, broadside (max) pointing up
    s, c = np.abs(np.sin(phi)), np.abs(np.cos(phi))
    with np.errstate(divide="ignore", invalid="ignore"):
        Fd = np.cos((np.pi / 2) * s) / c
    dip = np.nan_to_num(Fd, nan=0.0, posinf=0.0) ** 2
    up = np.clip(np.cos(phi), 0, None)
    horn = up ** 22                                  # ~30 deg main lobe up
    dish = up ** 220                                 # very narrow main lobe up

    fig = plt.figure(figsize=(4.6, 4.6))
    ax = fig.add_subplot(111, projection="polar")
    ax.set_theta_zero_location("N"); ax.set_theta_direction(-1)
    ax.set_ylim(-30, 0); ax.set_yticks([-30, -20, -10, 0])
    ax.set_yticklabels(["-30", "-20", "-10", "0 dB"], fontsize=10)
    ax.set_rlabel_position(112)
    ax.set_thetagrids(range(0, 360, 30), fontsize=10)
    ax.grid(color=RULE, linewidth=0.8)
    ax.plot(phi, dB(iso), color=GREY, lw=1.6, ls=(0, (5, 4)), label="Isotropic  0 dBi")
    ax.plot(phi, dB(dip), color=GREEN, lw=2.0, label="λ/2 dipole  2 dBi")
    ax.plot(phi, dB(horn), color=BLUE, lw=2.2, label="Horn  16 dBi")
    ax.plot(phi, dB(dish), color=NAVY, lw=2.4, label="Dish (D/λ=10)  28 dBi")
    ax.legend(loc="lower center", bbox_to_anchor=(0.5, -0.28), ncol=2, fontsize=11.5,
              handlelength=1.6, columnspacing=1.3)
    finalize(fig, "gain-pattern-polar")


def rectilinear() -> None:
    DL = 6.0
    th = np.linspace(-np.deg2rad(40), np.deg2rad(40), 4000)
    X = np.pi * DL * np.sin(th)
    with np.errstate(divide="ignore", invalid="ignore"):
        p = (np.sin(X) / X) ** 2
    p[np.isnan(p)] = 1.0
    dB = 10 * np.log10(np.clip(p, 1e-6, None))
    deg = np.rad2deg(th)

    fig, ax = plt.subplots(figsize=(6.4, 3.7))
    ax.plot(deg, dB, color=NAVY, lw=2.2)
    ax.set_xlim(-40, 40); ax.set_ylim(-40, 5)
    ax.set_xlabel("Angle from boresight  (deg)")
    ax.set_ylabel("Normalized gain  (dB)")
    ax.set_xticks(range(-40, 41, 10))
    ax.grid(color=RULE, linewidth=0.8)
    for sp in ("top", "right"):
        ax.spines[sp].set_visible(False)

    hp = np.rad2deg(np.arcsin(0.4429 / DL))          # -3 dB half-angle
    fn = np.rad2deg(np.arcsin(1.0 / DL))             # first null
    # HPBW
    ax.annotate("", xy=(hp, -3), xytext=(-hp, -3),
                arrowprops=dict(arrowstyle="<->", color=RED, lw=1.6))
    ax.text(0, 1.4, "HPBW", color=RED, ha="center", va="bottom", fontsize=12, fontweight="bold")
    # FNBW
    ax.annotate("", xy=(fn, -34), xytext=(-fn, -34),
                arrowprops=dict(arrowstyle="<->", color=GREEN, lw=1.4))
    ax.text(0, -33, "FNBW", color=GREEN, ha="center", va="bottom", fontsize=12, fontweight="bold")
    # SLL (first sidelobe ~ -13.3 dB)
    sll_x = np.rad2deg(np.arcsin(1.43 / DL))
    ax.axhline(-13.3, color=ORANGE, lw=1.2, ls=(0, (4, 3)))
    ax.annotate("SLL  −" "13 dB", xy=(sll_x, -13.3), xytext=(24, -9),
                color=ORANGE, fontsize=12, fontweight="bold",
                arrowprops=dict(arrowstyle="->", color=ORANGE, lw=1.2))
    finalize(fig, "rectilinear")


def vswr() -> None:
    g = np.linspace(0, 0.82, 500)
    v = (1 + g) / (1 - g)
    fig, ax = plt.subplots(figsize=(5.2, 3.7))
    ax.plot(g, v, color=NAVY, lw=2.4)
    ax.set_xlim(0, 0.82); ax.set_ylim(1, 10)
    ax.set_xlabel("Reflection coefficient  |Γ|")
    ax.set_ylabel("VSWR")
    ax.grid(color=RULE, linewidth=0.8)
    for sp in ("top", "right"):
        ax.spines[sp].set_visible(False)
    for gm, lab in [(0.2, "1.5:1"), (0.333, "2:1"), (0.5, "3:1")]:
        vm = (1 + gm) / (1 - gm)
        ax.plot([gm, gm], [1, vm], color=RULE, lw=1.0, ls=(0, (3, 3)))
        ax.plot([0, gm], [vm, vm], color=RULE, lw=1.0, ls=(0, (3, 3)))
        ax.plot(gm, vm, "o", color=RED, ms=6)
        ax.annotate(lab, xy=(gm, vm), xytext=(gm + 0.02, vm + 0.5),
                    color=RED, fontsize=11.5, fontweight="bold")
    finalize(fig, "vswr")


def main() -> int:
    OUT.mkdir(parents=True, exist_ok=True)
    gain_polar(); rectilinear(); vswr()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
