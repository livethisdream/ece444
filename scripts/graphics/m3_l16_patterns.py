#!/usr/bin/env python3
"""Generate the L16 (array factor / pattern multiplication) figures as SVG.

Data plots (matplotlib):
  L16-af-anatomy            : |AF| in dB vs scan angle, N=8, d/lambda=0.481,
                              main lobe / nulls / first sidelobe annotated
  L16-pattern-multiplication: element factor, array factor, and their product
  L16-visible-region        : |AF| vs psi over three periods with the visible
                              windows for d/lambda = 0.481 and 1.0
  L16-af-builder            : static fallback for the array-factor-builder widget

Line drawings (hand-written SVG):
  L16-array-geometry        : N elements on a line, extra path length per element
  L16-phasor-sum            : element phasors adding at broadside, off broadside,
                              and at the first null
  L16-sampled-aperture      : continuous aperture vs the same length sampled

All figures carry numbers and words only -- no equations (house rule: the math
lives in the slide text so it inherits the deck font).

    python3 scripts/graphics/m3_l16_patterns.py
    -> book/extras/slides/fig/L16-*.svg  and  book/extras/viz/img/L16-*.svg
"""

from __future__ import annotations

import io
import re
from pathlib import Path

import numpy as np
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

NAVY, BLUE, RED = "#004a85", "#0067b9", "#b01e24"
GREEN, AMBER, GRAY = "#1d7a4d", "#8a5a00", "#5a5a5a"
INK, RULE = "#1a1a1a", "#c7d2e0"

ROOT = Path(__file__).resolve().parents[2]
OUTS = (ROOT / "book/extras/slides/fig", ROOT / "book/extras/viz/img")

plt.rcParams.update(
    {
        "svg.fonttype": "none",
        "font.size": 12,
        "axes.edgecolor": "#8a929c",
        "axes.labelcolor": INK,
        "xtick.color": GRAY,
        "ytick.color": GRAY,
        "text.color": INK,
        "axes.linewidth": 1.0,
        "legend.frameon": False,
    }
)

DB_FLOOR = -40.0


def write(name: str, svg: str) -> None:
    for out in OUTS:
        out.mkdir(parents=True, exist_ok=True)
        (out / f"{name}.svg").write_text(svg, encoding="utf-8")
    print(f"wrote {name}.svg -> {', '.join(str(o) for o in OUTS)}")


def finalize(fig, name: str) -> None:
    buf = io.StringIO()
    fig.savefig(buf, format="svg", transparent=True, bbox_inches="tight", pad_inches=0.06)
    plt.close(fig)
    s = buf.getvalue()
    s = s[s.index("<svg"):]
    s = re.sub(r"font-family:[^;}]*", "font-family:inherit", s)
    write(name, s)


# ---------------------------------------------------------------- physics ---
def af_uniform(theta_deg, N, d_lam, theta0_deg=0.0):
    """Normalized uniform array factor, peak = 1, scan angle from broadside."""
    th = np.radians(np.asarray(theta_deg, dtype=float))
    psi = 2 * np.pi * d_lam * (np.sin(th) - np.sin(np.radians(theta0_deg)))
    s = np.sin(psi / 2)
    out = np.where(np.abs(s) < 1e-12, 1.0, np.sin(N * psi / 2) / (N * np.where(np.abs(s) < 1e-12, 1.0, s)))
    return np.abs(out)


def af_psi(psi_deg, N):
    psi = np.radians(np.asarray(psi_deg, dtype=float))
    s = np.sin(psi / 2)
    out = np.where(np.abs(s) < 1e-12, 1.0, np.sin(N * psi / 2) / (N * np.where(np.abs(s) < 1e-12, 1.0, s)))
    return np.abs(out)


def db(x):
    return 20 * np.log10(np.maximum(np.asarray(x, dtype=float), 1e-6))


def style_db_axes(ax, xlabel="Scan angle from broadside (degrees)"):
    ax.set_xlim(-90, 90)
    ax.set_ylim(DB_FLOOR, 3)
    ax.set_xticks(np.arange(-90, 91, 30))
    ax.set_yticks(np.arange(DB_FLOOR, 1, 10))
    ax.set_xlabel(xlabel)
    ax.grid(True, color=RULE, lw=0.7, alpha=0.9)
    for side in ("top", "right"):
        ax.spines[side].set_visible(False)


# ---------------------------------------------------------------- figures ---
def anatomy() -> None:
    N, d_lam = 8, 0.481
    th = np.linspace(-90, 90, 6001)
    y = db(af_uniform(th, N, d_lam))

    fig, ax = plt.subplots(figsize=(7.9, 3.7))
    ax.plot(th, y, color=NAVY, lw=2.0)
    style_db_axes(ax)
    ax.set_ylabel("Relative power (dB)")

    null1 = np.degrees(np.arcsin(1 / (N * d_lam)))
    for s in (-1, 1):
        ax.plot([s * null1, s * null1], [DB_FLOOR, -3], color=RED, lw=1.0, ls=(0, (4, 3)))
    ax.annotate(
        "first null  15.1°",
        xy=(null1, -34), xytext=(38, -30.5),
        color=RED, fontsize=11,
        arrowprops=dict(arrowstyle="-", color=RED, lw=0.9),
    )

    slt = 21.94
    ax.plot([slt], [-12.8], marker="o", ms=4.5, color=AMBER)
    ax.annotate(
        "first sidelobe  −12.8 dB",
        xy=(slt, -12.8), xytext=(34, -8.5),
        color=AMBER, fontsize=11,
        arrowprops=dict(arrowstyle="-", color=AMBER, lw=0.9),
    )

    hp = 13.2 / 2
    ax.annotate(
        "", xy=(-hp, -3), xytext=(hp, -3),
        arrowprops=dict(arrowstyle="<->", color=GREEN, lw=1.2),
    )
    ax.text(0, 0.6, "half-power width  13.2°", color=GREEN, fontsize=11, ha="center")
    ax.text(-86, -6.5, "main lobe", color=NAVY, fontsize=11, ha="left")
    ax.text(-86, -10.2, "6 sidelobes in view", color=GRAY, fontsize=10.5, ha="left")
    ax.text(88, -37.6, "N = 8, spacing 0.481 wavelength", color=GRAY, fontsize=10.5, ha="right")
    finalize(fig, "L16-af-anatomy")


def pattern_multiplication() -> None:
    N, d_lam = 4, 0.5
    th = np.linspace(-90, 90, 6001)
    ef = np.abs(np.cos(np.radians(th)))
    af = af_uniform(th, N, d_lam)

    fig, axes = plt.subplots(1, 3, figsize=(7.9, 2.9), sharey=True)
    for ax, (y, c, ttl) in zip(
        axes,
        [
            (ef, GRAY, "Element factor"),
            (af, BLUE, "Array factor"),
            (ef * af, NAVY, "Total pattern"),
        ],
    ):
        ax.plot(th, db(y), color=c, lw=2.0)
        style_db_axes(ax, xlabel="Angle (deg)")
        ax.set_xticks([-60, 0, 60])
        ax.set_title(ttl, color=c, fontsize=12, pad=6)
    axes[0].set_ylabel("Relative power (dB)")
    axes[2].plot(th, db(af), color=BLUE, lw=0.9, ls=(0, (3, 3)))
    axes[2].text(-86, -37.5, "array factor dashed", color=BLUE, fontsize=9.5, ha="left")
    axes[0].text(-86, -37.5, "short dipole element", color=GRAY, fontsize=9.5, ha="left")
    fig.subplots_adjust(wspace=0.22)
    finalize(fig, "L16-pattern-multiplication")


def visible_region() -> None:
    """Two windows onto the same periodic array factor."""
    N = 8
    psi = np.linspace(-620, 620, 14001)
    y = db(af_psi(psi, N))

    fig, axes = plt.subplots(2, 1, figsize=(7.9, 4.6), sharex=True)
    cases = [
        (173.2, GREEN, "spacing 0.481 wavelength — one main lobe in view"),
        (360.0, RED, "spacing 1.0 wavelength — the repeats reach the edge of view"),
    ]
    for ax, (half, color, ttl) in zip(axes, cases):
        ax.plot(psi, y, color=NAVY, lw=1.6)
        ax.axvspan(-620, -half, color="#ffffff", alpha=0.0, lw=0)
        ax.add_patch(plt.Rectangle((-620, -40), 620 - half, 44, color=GRAY, alpha=0.16, lw=0))
        ax.add_patch(plt.Rectangle((half, -40), 620 - half, 44, color=GRAY, alpha=0.16, lw=0))
        for s_ in (-1, 1):
            ax.plot([s_ * half, s_ * half], [-40, 4], color=color, lw=1.8)
        ax.set_xlim(-620, 620)
        ax.set_ylim(-40, 4)
        ax.set_yticks([-40, -20, 0])
        ax.set_ylabel("Power (dB)")
        ax.grid(True, color=RULE, lw=0.7, alpha=0.9)
        for side in ("top", "right"):
            ax.spines[side].set_visible(False)
        ax.set_title(ttl, color=color, fontsize=11.5, pad=5)
    axes[1].set_xticks(np.arange(-540, 541, 180))
    axes[1].set_xlabel("Array-factor argument (degrees)")
    for x in (-360, 360):
        axes[1].plot([x], [0], marker="o", ms=5, color=RED)
    axes[1].annotate(
        "repeat of the main lobe",
        xy=(360, 0), xytext=(505, -14),
        color=RED, fontsize=10.5, ha="center",
        arrowprops=dict(arrowstyle="-", color=RED, lw=0.9),
    )
    axes[0].text(-600, -34, "out of view", color=GRAY, fontsize=10, ha="left")
    fig.subplots_adjust(hspace=0.42)
    finalize(fig, "L16-visible-region")


def builder_static() -> None:
    N, d_lam = 8, 0.481
    th = np.linspace(-90, 90, 6001)
    af = af_uniform(th, N, d_lam)
    ef = np.abs(np.cos(np.radians(th)))

    fig, ax = plt.subplots(figsize=(7.9, 3.5))
    ax.plot(th, db(ef), color=GRAY, lw=1.2, ls=(0, (4, 3)))
    ax.plot(th, db(af), color=NAVY, lw=2.0)
    ax.plot(th, db(af * ef), color=BLUE, lw=1.5)
    style_db_axes(ax)
    ax.set_ylim(DB_FLOOR, 7)
    ax.set_ylabel("Relative power (dB)")
    ax.text(-88, 3.4, "array factor", color=NAVY, fontsize=10.5, ha="left")
    ax.text(0, 3.4, "element × array", color=BLUE, fontsize=10.5, ha="center")
    ax.text(88, 3.4, "element factor", color=GRAY, fontsize=10.5, ha="right")
    fig.text(
        0.5, -0.135,
        "N = 8   ·   spacing 0.481 wavelength   ·   half-power width 13.2°   ·   "
        "first null 15.1°   ·   first sidelobe −12.8 dB   ·   no grating lobes",
        color=GRAY, fontsize=9.5, ha="center",
    )
    finalize(fig, "L16-af-builder")


# ------------------------------------------------------------ line drawings --
def array_geometry() -> None:
    """Five elements on a line; the wave leaves each one d*sin(theta) later."""
    xs = [150, 250, 350, 450, 550]
    y0 = 300
    tilt = 32.0  # degrees off broadside
    t = np.radians(tilt)
    dx, dy = np.sin(t), -np.cos(t)  # unit vector toward the far field

    rays = []
    for i, x in enumerate(xs):
        rays.append(
            f'<line x1="{x}" y1="{y0}" x2="{x + 190 * dx:.1f}" y2="{y0 + 190 * dy:.1f}" '
            f'stroke="{BLUE}" stroke-width="1.6" marker-end="url(#l16arrow)"/>'
        )
    ray_svg = "\n".join(rays)

    # equiphase front through the last element, drawn back across the array
    fx, fy = xs[-1], y0
    front = []
    for x in xs:
        proj = (x - fx) * dx + (y0 - fy) * dy
        px, py = x - proj * dx, y0 - proj * dy
        front.append(
            f'<line x1="{x}" y1="{y0}" x2="{px:.1f}" y2="{py:.1f}" '
            f'stroke="{RED}" stroke-width="2.4"/>'
        )
    front_svg = "\n".join(front)
    x_end = xs[0] - ((xs[0] - fx) * dx) * dx
    y_end = y0 - ((xs[0] - fx) * dx) * dy

    svg = f"""<svg viewBox="0 0 790 400" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Five array elements on a straight line radiating toward a far-field direction tilted off broadside, with the extra path length each element adds marked in red between the element line and a common equiphase front">
<defs>
<marker id="l16arrow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse"><path d="M0 0 L10 5 L0 10 z" fill="{BLUE}"/></marker>
<marker id="l16grey" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse"><path d="M0 0 L10 5 L0 10 z" fill="{GRAY}"/></marker>
</defs>
<g style="font-family:inherit">

<line x1="90" y1="{y0}" x2="660" y2="{y0}" stroke="{GRAY}" stroke-width="1.2" stroke-dasharray="6 5"/>
<text x="96" y="{y0 - 12}" font-size="12.5" fill="{GRAY}">array axis</text>

{ray_svg}
<line x1="{xs[2]}" y1="{y0}" x2="{xs[2]}" y2="{y0 - 190}" stroke="{GRAY}" stroke-width="1.2" stroke-dasharray="5 4" marker-end="url(#l16grey)"/>
<text x="{xs[2] - 8}" y="{y0 - 196}" font-size="12.5" fill="{GRAY}" text-anchor="end">broadside</text>
<path d="M {xs[2]} {y0 - 96} A 96 96 0 0 1 {xs[2] + 96 * np.sin(t):.1f} {y0 - 96 * np.cos(t):.1f}" fill="none" stroke="{GRAY}" stroke-width="1.2"/>
<text x="{xs[2] + 30}" y="{y0 - 110}" font-size="15" font-weight="700" fill="{INK}">&#952;</text>

{front_svg}
<line x1="{x_end:.1f}" y1="{y_end:.1f}" x2="{fx}" y2="{fy}" stroke="{RED}" stroke-width="1.4" stroke-dasharray="5 4"/>
<text x="34" y="58" font-size="13.5" font-weight="700" fill="{RED}">equal-phase front</text>
<text x="34" y="78" font-size="12.5" fill="{RED}">red = extra path each element adds</text>

<g>
{"".join(f'<circle cx="{x}" cy="{y0}" r="11" fill="{NAVY}"/><text x="{x}" y="{y0 + 40}" font-size="12.5" fill="{NAVY}" text-anchor="middle">{i}</text>' for i, x in enumerate(xs))}
</g>
<line x1="{xs[0]}" y1="{y0 + 62}" x2="{xs[1]}" y2="{y0 + 62}" stroke="{INK}" stroke-width="1.2" marker-start="url(#l16grey)" marker-end="url(#l16grey)"/>
<text x="{(xs[0] + xs[1]) / 2}" y="{y0 + 80}" font-size="15" font-weight="700" fill="{INK}" text-anchor="middle">d</text>
<text x="660" y="{y0 + 44}" font-size="12.5" fill="{GRAY}">element number</text>
</g>
</svg>
"""
    write("L16-array-geometry", svg)


def phasor_sum() -> None:
    """Three phasor fans: aligned, partly canceling, and closing on a null."""
    panels = [
        (0.0, "all in phase", "peak", NAVY),
        (26.0, "fanned out", "partial cancellation", AMBER),
        (45.0, "closes on itself", "null", RED),
    ]
    N = 8
    L = 30.0  # phasor length, px
    blocks = []
    for k, (step_deg, ttl, sub, color) in enumerate(panels):
        cx = 132 + k * 262
        cy = 170
        # walk the phasor chain, then center it in the panel
        pts = [(0.0, 0.0)]
        for n in range(N):
            a = np.radians(-n * step_deg)
            pts.append((pts[-1][0] + L * np.cos(a), pts[-1][1] + L * np.sin(a)))
        xs = [p[0] for p in pts]
        ys = [p[1] for p in pts]
        ox = cx - (min(xs) + max(xs)) / 2
        oy = cy - (min(ys) + max(ys)) / 2
        seg = "".join(
            f'<line x1="{pts[i][0] + ox:.1f}" y1="{pts[i][1] + oy:.1f}" '
            f'x2="{pts[i + 1][0] + ox:.1f}" y2="{pts[i + 1][1] + oy:.1f}" '
            f'stroke="{color}" stroke-width="2.2" marker-end="url(#l16ph{k})"/>'
            for i in range(N)
        )
        res = ""
        if step_deg > 0.1:
            res = (
                f'<line x1="{pts[0][0] + ox:.1f}" y1="{pts[0][1] + oy:.1f}" '
                f'x2="{pts[-1][0] + ox:.1f}" y2="{pts[-1][1] + oy:.1f}" '
                f'stroke="{INK}" stroke-width="2.6" stroke-dasharray="7 4"/>'
            )
        blocks.append(
            f"""<g>
<rect x="{cx - 122}" y="46" width="244" height="250" rx="8" fill="#f5f9fc" stroke="{RULE}" stroke-width="1"/>
{seg}
{res}
<text x="{cx}" y="{cy + 128}" font-size="13.5" font-weight="700" fill="{color}" text-anchor="middle">{ttl}</text>
<text x="{cx}" y="{cy + 148}" font-size="12.5" fill="{GRAY}" text-anchor="middle">{sub}</text>
</g>"""
        )
    markers = "".join(
        f'<marker id="l16ph{k}" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="5" markerHeight="5" orient="auto-start-reverse"><path d="M0 0 L10 5 L0 10 z" fill="{c}"/></marker>'
        for k, (_, _, _, c) in enumerate(panels)
    )
    svg = f"""<svg viewBox="0 0 790 340" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Eight element phasors added tip to tail in three cases: all aligned giving the largest sum, fanned out giving a shorter sum, and stepped by one eighth of a turn so the chain closes into a circle and the sum is zero">
<defs>{markers}</defs>
<g style="font-family:inherit">
<text x="395" y="26" font-size="13.5" fill="{GRAY}" text-anchor="middle">Eight element phasors added tip to tail; the sum runs from the first tail to the last tip</text>
{"".join(blocks)}
</g>
</svg>
"""
    write("L16-phasor-sum", svg)


def sampled_aperture() -> None:
    N = 8
    x0, x1 = 120, 660
    step = (x1 - x0) / (N - 1)
    dots = "".join(
        f'<circle cx="{x0 + i * step:.1f}" cy="255" r="10" fill="{NAVY}"/>' for i in range(N)
    )
    ticks = "".join(
        f'<line x1="{x0 + i * step:.1f}" y1="255" x2="{x0 + i * step:.1f}" y2="205" '
        f'stroke="{BLUE}" stroke-width="2"/>'
        for i in range(N)
    )
    svg = f"""<svg viewBox="0 0 790 330" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="A continuous uniform aperture of length L above, and below it the same length occupied by eight equally spaced elements carrying the same total excitation">
<g style="font-family:inherit">
<text x="30" y="34" font-size="13.5" font-weight="700" fill="{GRAY}">Continuous aperture</text>
<rect x="{x0}" y="60" width="{x1 - x0}" height="34" fill="{GRAY}" opacity="0.30"/>
<line x1="{x0}" y1="60" x2="{x1}" y2="60" stroke="{GRAY}" stroke-width="2.4"/>
<line x1="{x0}" y1="94" x2="{x1}" y2="94" stroke="{GRAY}" stroke-width="1.2"/>
<text x="30" y="196" font-size="13.5" font-weight="700" fill="{NAVY}">Sampled by N elements</text>
{ticks}
<line x1="{x0}" y1="255" x2="{x1}" y2="255" stroke="{RULE}" stroke-width="1.4"/>
{dots}
<line x1="{x0}" y1="295" x2="{x0 + step:.1f}" y2="295" stroke="{INK}" stroke-width="1.2"/>
<text x="{x0 + step / 2:.1f}" y="313" font-size="15" font-weight="700" fill="{INK}" text-anchor="middle">d</text>
<line x1="{x0}" y1="156" x2="{x1}" y2="156" stroke="{RED}" stroke-width="1.6"/>
<line x1="{x0}" y1="148" x2="{x0}" y2="164" stroke="{RED}" stroke-width="1.6"/>
<line x1="{x1}" y1="148" x2="{x1}" y2="164" stroke="{RED}" stroke-width="1.6"/>
<text x="{(x0 + x1) / 2}" y="140" font-size="14" font-weight="700" fill="{RED}" text-anchor="middle">same overall length</text>
<text x="690" y="259" font-size="12.5" fill="{GRAY}">beam width follows the length; the sampling sets what repeats</text>
</g>
</svg>
"""
    # keep the trailing note inside the frame
    svg = svg.replace(
        f'<text x="690" y="259" font-size="12.5" fill="{GRAY}">beam width follows the length; the sampling sets what repeats</text>',
        f'<text x="{(x0 + x1) / 2}" y="{330 - 8}" font-size="12.5" fill="{GRAY}" text-anchor="middle">the length sets the beam width; the spacing sets what repeats</text>',
    )
    write("L16-sampled-aperture", svg)


def main() -> None:
    anatomy()
    pattern_multiplication()
    visible_region()
    builder_static()
    array_geometry()
    phasor_sum()
    sampled_aperture()


if __name__ == "__main__":
    main()
