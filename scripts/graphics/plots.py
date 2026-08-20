#!/usr/bin/env python3
"""Generate the Module 1 deck data-plots as inline SVG.

L02:
  - L02-gain-pattern-polar : absolute-dBi patterns, isotropic/dipole/horn/dish
  - L02-rectilinear        : uniform line-source sinc^2, HPBW/FNBW/SLL annotated
  - L02-vswr               : VSWR vs reflection-coefficient magnitude (reused by L03)

L03:
  - L03-plf-cos2           : polarization loss factor vs tilt, two linear antennas
  - L03-chu-q-vs-ka        : Chu-Harrington minimum Q vs electrical size

Exported as SVG with live <text> (svg.fonttype='none'), then font-family is
rewritten to 'inherit' so the injected figure picks up the deck's Source Sans
Pro. Transparent background, USAFA palette, no baked formulas (axis labels /
legends / pattern annotations only).

    python scripts/graphics/plots.py
    -> writes book/extras/slides/fig/{L02-gain-pattern-polar,L02-rectilinear,
                                      L02-vswr,L03-plf-cos2,L03-chu-q-vs-ka}.svg

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
    """Absolute-dBi polar comparison: peak radius encodes gain, so the
    0/2.15/16/28 dBi difference is visible on the plot, not just the legend.
    Horn and dish carry real sidelobes (tapered- and uniform-aperture space
    factors), since the pattern-reading slide points back at this figure."""
    phi = np.linspace(-np.pi, np.pi, 4001)           # 0 = up (North)
    FLOOR = -12.0                                     # radial floor, dBi

    def line_source_dBi(peak_dbi: float, DL: float, taper: str) -> np.ndarray:
        # space factor of a line source of length DL (in wavelengths), main
        # lobe up; behind +/-90 deg hold the far-out sidelobe floor.
        u = np.sin(np.clip(phi, -np.pi / 2, np.pi / 2))
        X = np.pi * DL * u
        with np.errstate(divide="ignore", invalid="ignore"):
            if taper == "uniform":                    # SLL -13.3 dB
                F = np.sin(X) / X
            else:                                     # triangular: SLL -26.5 dB
                F = (np.sin(X / 2) / (X / 2)) ** 2
        F = np.nan_to_num(F, nan=1.0)
        db = peak_dbi + 20 * np.log10(np.clip(np.abs(F), 1e-6, None))
        back = np.abs(phi) > np.pi / 2
        db[back] = np.maximum(db[back], peak_dbi - 40.0)  # modest back level
        return np.clip(db, FLOOR, None)

    iso = np.zeros_like(phi)                          # isotropic: 0 dBi everywhere
    # lambda/2 dipole, broadside (max) pointing up: D = 2.15 dBi
    s, c = np.abs(np.sin(phi)), np.abs(np.cos(phi))
    with np.errstate(divide="ignore", invalid="ignore"):
        Fd = np.cos((np.pi / 2) * s) / c
    Fd = np.nan_to_num(Fd, nan=0.0, posinf=0.0)
    dip = np.clip(2.15 + 20 * np.log10(np.clip(np.abs(Fd), 1e-6, None)), FLOOR, None)
    horn = line_source_dBi(16.0, 2.6, "triangular")   # tapered aperture, ~20 deg lobe
    dish = line_source_dBi(28.0, 10.0, "uniform")     # D/lambda = 10, SLL -13.3 dB

    fig = plt.figure(figsize=(4.9, 4.9))
    ax = fig.add_subplot(111, projection="polar")
    ax.set_theta_zero_location("N"); ax.set_theta_direction(-1)
    ax.set_ylim(FLOOR, 30); ax.set_yticks([-10, 0, 10, 20, 28])
    ax.set_yticklabels(["-10", "0 dBi", "10", "20", "28"], fontsize=10)
    ax.set_rlabel_position(112)
    ax.set_thetagrids(range(0, 360, 30), fontsize=10)
    ax.grid(color=RULE, linewidth=0.8)
    ax.plot(phi, iso, color=GREY, lw=1.6, ls=(0, (5, 4)), label="Isotropic  0 dBi")
    ax.plot(phi, dip, color=GREEN, lw=2.0, label="λ/2 dipole  2.15 dBi")
    ax.plot(phi, horn, color=BLUE, lw=2.2, label="Horn  16 dBi")
    ax.plot(phi, dish, color=NAVY, lw=2.4, label="Dish (D/λ=10)  28 dBi")
    ax.legend(loc="lower center", bbox_to_anchor=(0.5, -0.28), ncol=2, fontsize=11.5,
              handlelength=1.6, columnspacing=1.3)
    finalize(fig, "L02-gain-pattern-polar")


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
    finalize(fig, "L02-rectilinear")


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
    finalize(fig, "L02-vswr")


def plf_cos2() -> None:
    """PLF between two linear antennas tilted by theta — the continuous curve
    behind the L03 cheat-sheet table's linear-linear row."""
    th = np.linspace(0, 90, 600)
    plf = np.cos(np.deg2rad(th)) ** 2

    fig, ax = plt.subplots(figsize=(5.8, 3.8))
    ax.plot(th, plf, color=NAVY, lw=2.6)
    ax.set_xlim(0, 90); ax.set_ylim(0, 1.08)
    ax.set_xlabel("Tilt between the two antennas  ψ  (deg)")
    ax.set_ylabel("PLF")
    ax.set_xticks(range(0, 91, 15))
    ax.grid(color=RULE, linewidth=0.8)
    for sp in ("top", "right"):
        ax.spines[sp].set_visible(False)

    # the three rows of the cheat sheet, marked on the curve
    for t, lab, col, xy in ((0.0, "0 dB", GREEN, (7, 0.85)),
                            (45.0, "−3 dB", RED, (52, 0.64)),
                            (90.0, "−∞ dB", GREY, (58, 0.17))):
        v = float(np.cos(np.deg2rad(t)) ** 2)
        ax.plot(t, v, "o", color=col, ms=7, zorder=5)
        ax.annotate(lab, xy=(t, v), xytext=xy, color=col, fontsize=12.5, fontweight="bold",
                    arrowprops=dict(arrowstyle="->", color=col, lw=1.2))
    ax.plot([45, 45], [0, 0.5], color=RULE, lw=1.0, ls=(0, (3, 3)), zorder=1)
    ax.plot([0, 45], [0.5, 0.5], color=RULE, lw=1.0, ls=(0, (3, 3)), zorder=1)

    # inset: the tilt angle being plotted, as two linear elements
    ins = ax.inset_axes((0.60, 0.56, 0.36, 0.42))
    tilt = np.deg2rad(38.0)
    ins.plot([-1, 1], [0, 0], color=BLUE, lw=3.2, solid_capstyle="round")
    ins.plot([-np.cos(tilt), np.cos(tilt)], [-np.sin(tilt), np.sin(tilt)],
             color=RED, lw=3.2, solid_capstyle="round")
    a = np.linspace(0, tilt, 60)
    ins.plot(0.45 * np.cos(a), 0.45 * np.sin(a), color=GREY, lw=1.4)
    ins.text(0.62 * np.cos(tilt / 2), 0.62 * np.sin(tilt / 2), "ψ",
             color=GREY, fontsize=13, fontweight="bold", ha="center", va="center")
    ins.set_xlim(-1.25, 1.25); ins.set_ylim(-1.05, 1.05)
    ins.set_aspect("equal"); ins.set_xticks([]); ins.set_yticks([])
    ins.patch.set_alpha(0)
    for sp in ins.spines.values():
        sp.set_visible(False)

    finalize(fig, "L03-plf-cos2")


def chu_q_vs_ka() -> None:
    """Chu-Harrington lower bound on Q vs electrical size, with the bandwidth
    it implies on the right-hand axis. Bound only — a real antenna sits above."""
    ka = np.logspace(np.log10(0.15), np.log10(3.0), 800)
    Q = 1 / ka ** 3 + 1 / ka

    fig, ax = plt.subplots(figsize=(5.9, 3.9))
    ax.axvspan(0.15, 1.0, color=RULE, alpha=0.35, lw=0, zorder=0)
    ax.loglog(ka, Q, color=NAVY, lw=2.8, zorder=3)
    ax.set_xlim(0.15, 3.0); ax.set_ylim(0.3, 400)
    ax.set_xlabel("Electrical size  ka")
    ax.set_ylabel("Minimum Q")
    ax.grid(color=RULE, linewidth=0.8, which="major")
    for sp in ("top",):
        ax.spines[sp].set_visible(False)
    ax.set_xticks([0.2, 0.3, 0.5, 1.0, 2.0, 3.0])
    ax.set_xticklabels(["0.2", "0.3", "0.5", "1", "2", "3"])

    ax.axvline(1.0, color=GREY, lw=1.4, ls=(0, (4, 3)), zorder=2)
    ax.text(0.98, 250, "ka = 1", color=GREY, fontsize=12, fontweight="bold",
            ha="right", va="center")
    ax.text(0.165, 0.45, "electrically small", color=GREY, fontsize=12,
            fontweight="bold", ha="left", va="bottom")

    ax.plot(1.0, 2.0, "o", color=ORANGE, ms=7, zorder=5)
    ax.annotate("ka = 1, Q ≈ 2 —\nthe practical small-antenna knee",
                xy=(1.0, 2.0), xytext=(1.25, 6.5), color=ORANGE,
                fontsize=11, fontweight="bold", ha="left", va="bottom",
                arrowprops=dict(arrowstyle="->", color=ORANGE, lw=1.2))

    # what the Q actually costs you, on the same picture
    sec = ax.secondary_yaxis("right", functions=(lambda q: 1 / q, lambda b: 1 / b))
    sec.set_ylabel("Approx. fractional bandwidth")

    # inset: the enclosing sphere that sets ka
    ins = ax.inset_axes((0.56, 0.58, 0.38, 0.40))
    t = np.linspace(0, 2 * np.pi, 200)
    ins.plot(np.cos(t), np.sin(t), color=GREY, lw=1.5, ls=(0, (4, 3)))
    zx = np.linspace(-0.45, 0.45, 200)
    ins.plot(zx, 0.42 * np.sin(2 * np.pi * zx / 0.30), color=NAVY, lw=2.4)
    ins.annotate("", xy=(np.cos(np.pi / 4), np.sin(np.pi / 4)), xytext=(0, 0),
                 arrowprops=dict(arrowstyle="->", color=RED, lw=1.6))
    ins.text(0.30, 0.62, "a", color=RED, fontsize=13, fontweight="bold",
             ha="right", va="center")
    ins.set_xlim(-1.15, 1.15); ins.set_ylim(-1.15, 1.15)
    ins.set_aspect("equal"); ins.set_xticks([]); ins.set_yticks([])
    ins.patch.set_alpha(0)
    for sp in ins.spines.values():
        sp.set_visible(False)

    finalize(fig, "L03-chu-q-vs-ka")


def main() -> int:
    OUT.mkdir(parents=True, exist_ok=True)
    gain_polar(); rectilinear(); vswr()
    plf_cos2(); chu_q_vs_ka()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
