#!/usr/bin/env python3
"""Generate the L15 aperture-distribution deck figures as inline SVG.

L15:
  - L15-uniform-pattern    : uniform aperture space factor in dB against the
                             space frequency u = (L/lambda) sin(theta), with the
                             half-power points, first null and -13.3 dB first
                             sidelobe marked
  - L15-taper-comparison   : two panels -- the four aperture illuminations
                             across the aperture, and their patterns in dB to a
                             -40 dB floor (the static fallback for the
                             aperture-distribution widget)

Same export convention as scripts/graphics/plots.py: SVG with live <text>
(svg.fonttype='none'), font-family rewritten to 'inherit' so the injected
figure picks up the deck font, transparent background, USAFA palette, and
**no baked equations** (deck figures carry words and numbers only).

    python3 scripts/graphics/m3_l15_apertures.py
    -> writes book/extras/slides/fig/{L15-uniform-pattern,L15-taper-comparison}.svg
       and copies both to book/extras/viz/img/ for the lesson page.

Patterns are computed from the aperture integral (trapezoid over the aperture),
not sketched; the marked numbers are the course canonical values.
"""

from __future__ import annotations

import io
import re
import shutil
from pathlib import Path

import matplotlib
import numpy as np

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

NAVY, BLUE, RED, GREEN, ORANGE, GREY = (
    "#004a85", "#0067b9", "#b01e24", "#1d7a4d", "#e67e22", "#5a5a5a",
)
INK, RULE = "#1a1a1a", "#c7d2e0"
SLIDE_BG = "#fafaf7"
ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "book/extras/slides/fig"
PAGE = ROOT / "book/extras/viz/img"

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

XI = np.linspace(-0.5, 0.5, 2001)          # x / L across the aperture

DISTS = {
    "uniform":    ("Uniform",    np.ones_like(XI),               NAVY),
    "cosine":     ("Cosine",     np.cos(np.pi * XI),             BLUE),
    "triangular": ("Triangular", 1.0 - 2.0 * np.abs(XI),         GREEN),
    "cosine2":    ("Cosine²",    np.cos(np.pi * XI) ** 2,        RED),
}


def space_factor(a: np.ndarray, u: np.ndarray) -> np.ndarray:
    """|S(u)| normalized to 1 at u = 0, u = (L/lambda) sin(theta)."""
    integ = np.trapezoid(a[None, :] * np.cos(2 * np.pi * u[:, None] * XI[None, :]),
                         XI, axis=1)
    return np.abs(integ) / np.trapezoid(a, XI)


def db(x: np.ndarray) -> np.ndarray:
    return 20.0 * np.log10(np.maximum(x, 1e-6))


def finalize(fig, name: str) -> None:
    buf = io.StringIO()
    fig.savefig(buf, format="svg", transparent=True, bbox_inches="tight", pad_inches=0.06)
    plt.close(fig)
    s = buf.getvalue()
    s = s[s.index("<svg"):]
    s = re.sub(r"font-family:[^;}]*", "font-family:inherit", s)
    (OUT / f"{name}.svg").write_text(s, encoding="utf-8")
    PAGE.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(OUT / f"{name}.svg", PAGE / f"{name}.svg")
    print(f"wrote {OUT / (name + '.svg')} (+ page copy)")


def uniform_pattern() -> None:
    """The one figure the uniform-aperture result lives on: sinc in dB, with
    the half-power width, the first null and the first sidelobe called out."""
    u = np.linspace(-4.2, 4.2, 3001)
    y = db(space_factor(DISTS["uniform"][1], u))

    fig, ax = plt.subplots(figsize=(8.4, 4.3))
    ax.plot(u, y, color=NAVY, lw=2.4)
    ax.set_xlim(-4.2, 4.2)
    ax.set_ylim(-40, 3)
    ax.set_yticks([0, -10, -13.3, -20, -30, -40])
    ax.set_yticklabels(["0", "-10", "-13.3", "-20", "-30", "-40"])
    ax.set_xticks([-4, -3, -2, -1, 0, 1, 2, 3, 4])
    ax.set_xlabel("space frequency   (sine of angle x aperture length in wavelengths)")
    ax.set_ylabel("relative power  (dB)")
    ax.grid(True, color="#eef3f8", lw=1)
    ax.set_axisbelow(True)

    # first sidelobe level
    ax.axhline(-13.26, color=ORANGE, lw=1.4, ls=(0, (5, 3)))
    ax.annotate("first sidelobe  -13.3 dB", xy=(1.43, -13.26), xytext=(1.9, -8.4),
                color=ORANGE, fontsize=12.5,
                arrowprops=dict(arrowstyle="-", color=ORANGE, lw=1.1))

    # half-power width
    uh = 0.4429
    ax.plot([-uh, uh], [-3.01, -3.01], color=GREEN, lw=2.6, solid_capstyle="butt")
    ax.plot([-uh, -uh], [-3.01, 0], color=GREEN, lw=1.0, ls=":")
    ax.plot([uh, uh], [-3.01, 0], color=GREEN, lw=1.0, ls=":")
    ax.annotate("half-power width  0.886", xy=(0, -3.01), xytext=(-4.0, 1.0),
                color=GREEN, fontsize=12.5,
                arrowprops=dict(arrowstyle="->", color=GREEN, lw=1.1))

    # first null
    ax.annotate("first null at 1.0", xy=(1.0, -38.2), xytext=(1.28, -33.6),
                color=RED, fontsize=12.5,
                arrowprops=dict(arrowstyle="->", color=RED, lw=1.1))
    ax.plot([1.0, 1.0], [-40, -38.5], color=RED, lw=1.6)
    ax.plot([-1.0, -1.0], [-40, -38.5], color=RED, lw=1.6)

    finalize(fig, "L15-uniform-pattern")


def taper_comparison() -> None:
    """Distributions on top, their patterns below -- the static fallback for
    the aperture-distribution widget."""
    u = np.linspace(-4.5, 4.5, 3001)
    fig, (ax0, ax1) = plt.subplots(
        2, 1, figsize=(8.6, 6.3), gridspec_kw=dict(height_ratios=[1, 2.0], hspace=0.42)
    )

    for label, a, col in DISTS.values():
        ax0.plot(XI, a, color=col, lw=2.2, label=label)
    ax0.set_xlim(-0.5, 0.5)
    ax0.set_ylim(-0.05, 1.12)
    ax0.set_xticks([-0.5, -0.25, 0, 0.25, 0.5])
    ax0.set_xticklabels(["edge", "", "center", "", "edge"])
    ax0.set_yticks([0, 0.5, 1.0])
    ax0.set_ylabel("field\namplitude", fontsize=12)
    ax0.grid(True, color="#eef3f8", lw=1)
    ax0.set_axisbelow(True)
    ax0.legend(loc="upper center", ncol=4, fontsize=11.5, handlelength=1.5,
               columnspacing=1.6, bbox_to_anchor=(0.5, 1.34))

    for label, a, col in DISTS.values():
        ax1.plot(u, db(space_factor(a, u)), color=col, lw=2.1)
    ax1.set_xlim(-4.5, 4.5)
    ax1.set_ylim(-40, 3)
    ax1.set_yticks([0, -10, -20, -30, -40])
    ax1.set_xticks([-4, -3, -2, -1, 0, 1, 2, 3, 4])
    ax1.set_xlabel("space frequency   (sine of angle x aperture length in wavelengths)")
    ax1.set_ylabel("relative power  (dB)")
    ax1.grid(True, color="#eef3f8", lw=1)
    ax1.set_axisbelow(True)

    for lev, col, txt, xy, xytext in [
        (-13.26, NAVY,  "-13.3 dB", (1.43, -13.26), (2.05, -9.0)),
        (-23.00, BLUE,  "-23 dB",   (1.87, -23.00), (2.55, -19.0)),
        (-26.52, GREEN, "-26.5 dB", (2.86, -26.52), (3.25, -24.0)),
        (-31.47, RED,   "-31.5 dB", (2.36, -31.47), (2.75, -35.5)),
    ]:
        ax1.annotate(txt, xy=xy, xytext=xytext, color=col, fontsize=12,
                     arrowprops=dict(arrowstyle="-", color=col, lw=1.0),
                     bbox=dict(boxstyle="round,pad=0.14", fc=SLIDE_BG, ec="none"))

    finalize(fig, "L15-taper-comparison")


def geometry_schematic() -> None:
    """Hand-composed schematic: the field across the aperture on the left, the
    far-field pattern it transforms into on the right. The lobe outline is the
    uniform-aperture space factor at two wavelengths of aperture, so the
    sidelobe sizes on the drawing are the ones the lesson quotes."""
    W, H = 780, 310
    ap_x, ap_c, ap_h = 232.0, 150.0, 88.0        # aperture line, center, half-length
    org_x, org_y, rmax = 398.0, 150.0, 296.0     # pattern origin and radius scale

    # uniform aperture, L = 2 lambda, polar outline of |S| against angle
    th = np.linspace(-np.pi / 2, np.pi / 2, 721)
    s_of = np.abs(space_factor(np.ones_like(XI), 2.0 * np.sin(th)))
    px = org_x + rmax * s_of * np.cos(th)
    py = org_y - rmax * s_of * np.sin(th)
    lobe = "M " + " L ".join(f"{x:.1f},{y:.1f}" for x, y in zip(px, py))

    prof_w = 58.0
    dim_x = ap_x - prof_w - 26.0
    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" '
        f'width="{W}" height="{H}" role="img" '
        f'aria-label="Field across an aperture on the left and the far-field '
        f'pattern it produces, a main lobe with sidelobes, on the right">',
        '<defs>'
        '<marker id="ah" viewBox="0 0 10 10" refX="9" refY="5" '
        'markerWidth="5" markerHeight="5" orient="auto">'
        f'<path d="M 0,0 L 10,5 L 0,10 z" fill="{BLUE}"/></marker>'
        '<marker id="ag" viewBox="0 0 10 10" refX="9" refY="5" '
        'markerWidth="6" markerHeight="6" orient="auto">'
        f'<path d="M 0,0 L 10,5 L 0,10 z" fill="{GREY}"/></marker>'
        '<marker id="ad" viewBox="0 0 10 10" refX="9" refY="5" '
        'markerWidth="6" markerHeight="6" orient="auto">'
        f'<path d="M 0,0 L 10,5 L 0,10 z" fill="{INK}"/></marker>'
        '</defs>',
        '<g fill="none" stroke-linecap="round" stroke-linejoin="round">',
        f'<path d="M {org_x:.0f},{org_y:.0f} L {W - 30},{org_y:.0f}" stroke="{GREY}" '
        'stroke-width="1.2" stroke-dasharray="6 5"/>',
        f'<path d="{lobe} Z" fill="{NAVY}" fill-opacity="0.13" stroke="{NAVY}" '
        'stroke-width="2.2"/>',
        f'<path d="M {ap_x - 40:.0f},{ap_c - ap_h - 30:.0f} L {ap_x:.0f},'
        f'{ap_c - ap_h - 30:.0f} L {ap_x:.0f},{ap_c - ap_h:.0f}" stroke="{GREY}" '
        'stroke-width="3.2"/>',
        f'<path d="M {ap_x - 40:.0f},{ap_c + ap_h + 30:.0f} L {ap_x:.0f},'
        f'{ap_c + ap_h + 30:.0f} L {ap_x:.0f},{ap_c + ap_h:.0f}" stroke="{GREY}" '
        'stroke-width="3.2"/>',
        f'<path d="M {ap_x - prof_w:.0f},{ap_c - ap_h:.0f} L {ap_x:.0f},'
        f'{ap_c - ap_h:.0f} L {ap_x:.0f},{ap_c + ap_h:.0f} L {ap_x - prof_w:.0f},'
        f'{ap_c + ap_h:.0f} Z" fill="{BLUE}" fill-opacity="0.16" '
        f'stroke="{BLUE}" stroke-width="2"/>',
        # aperture length dimension
        f'<path d="M {dim_x:.0f},{ap_c - ap_h + 4:.0f} L {dim_x:.0f},'
        f'{ap_c + ap_h - 4:.0f}" stroke="{INK}" stroke-width="1.3" '
        'marker-end="url(#ad)"/>',
        f'<path d="M {dim_x:.0f},{ap_c + ap_h - 4:.0f} L {dim_x:.0f},'
        f'{ap_c - ap_h + 4:.0f}" stroke="{INK}" stroke-width="1.3" '
        'marker-end="url(#ad)"/>',
        f'<path d="M {dim_x - 7:.0f},{ap_c - ap_h:.0f} L {ap_x:.0f},'
        f'{ap_c - ap_h:.0f}" stroke="{INK}" stroke-width="0.9" stroke-dasharray="4 3"/>',
        f'<path d="M {dim_x - 7:.0f},{ap_c + ap_h:.0f} L {ap_x:.0f},'
        f'{ap_c + ap_h:.0f}" stroke="{INK}" stroke-width="0.9" stroke-dasharray="4 3"/>',
        f'<path d="M {ap_x:.0f},{ap_c - ap_h:.0f} L {ap_x:.0f},{ap_c + ap_h:.0f}" '
        f'stroke="{INK}" stroke-width="3.4"/>',
        "</g>",
    ]
    for k in range(7):
        y = ap_c - ap_h + (2 * k + 1) * ap_h / 7.0
        parts.append(
            f'<path d="M {ap_x - prof_w + 6:.0f},{y:.1f} L {ap_x - 7:.0f},{y:.1f}" '
            f'stroke="{BLUE}" stroke-width="1.6" marker-end="url(#ah)"/>'
        )
    # sidelobe caller -- points at the first sidelobe of the drawn pattern
    sl_th = np.deg2rad(48.0)
    sl_r = rmax * np.abs(space_factor(np.ones_like(XI),
                                      np.array([2.0 * np.sin(sl_th)])))[0]
    sx, sy = org_x + sl_r * np.cos(sl_th), org_y - sl_r * np.sin(sl_th)
    parts.append(
        f'<path d="M 486,46 L {sx - 6:.0f},{sy - 8:.0f}" stroke="{GREY}" '
        'stroke-width="1.2" marker-end="url(#ag)"/>'
    )
    txt = 'font-family="inherit" font-size="15" fill="{c}" text-anchor="{a}"'
    parts += [
        f'<text x="{ap_x - prof_w / 2:.0f}" y="{ap_c + ap_h + 52:.0f}" '
        + txt.format(c=BLUE, a="middle") + ">field across the aperture</text>",
        f'<text x="{dim_x - 12:.0f}" y="{ap_c:.0f}" '
        + txt.format(c=INK, a="middle")
        + f' transform="rotate(-90 {dim_x - 12:.0f} {ap_c:.0f})">aperture length</text>',
        f'<text x="{W - 18}" y="{org_y - 12:.0f}" '
        + txt.format(c=GREY, a="end") + ">boresight</text>",
        f'<text x="600" y="{ap_c + ap_h + 52:.0f}" '
        + txt.format(c=NAVY, a="middle") + ">far-field pattern</text>",
        f'<text x="482" y="50" ' + txt.format(c=GREY, a="end") + ">sidelobes</text>",
    ]
    parts.append("</svg>")
    svg = "\n".join(parts)
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "L15-aperture-to-pattern.svg").write_text(svg, encoding="utf-8")
    PAGE.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(OUT / "L15-aperture-to-pattern.svg",
                    PAGE / "L15-aperture-to-pattern.svg")
    print(f"wrote {OUT / 'L15-aperture-to-pattern.svg'} (+ page copy)")


if __name__ == "__main__":
    OUT.mkdir(parents=True, exist_ok=True)
    uniform_pattern()
    taper_comparison()
    geometry_schematic()
