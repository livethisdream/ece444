#!/usr/bin/env python3
"""L15: the computed figures from the 2026-10-04 illustration sweep (Batch A).

Every figure is labels only: no equations, so the same SVG serves the deck
(book/extras/slides/fig) and the lesson page (book/extras/viz/img). The math
lives in the lesson text. Every plotted number is computed here from the
aperture integral or its closed form, and printed so it can be checked
against the page.

  L15-shape-vs-size      the uniform pattern against u, with the edge of
                         visible space for L = 2, 5, and 20 wavelengths, over
                         the same three patterns against angle: one shape in u,
                         three widths in degrees, one -13.3 dB sidelobe
  L15-taper-trade        the four tapers as points, first sidelobe against the
                         beamwidth constant, each labeled with its gain penalty
  L15-circle-vs-square   uniform square (sinc) against uniform circle
                         (2 J1 / x) on the same (D/lambda) sin(theta) axis, with
                         the half-power widths and first sidelobes marked, and
                         the circle's projected taper as an inset
  L15-efficiency-ratio   the cosine illumination and its mean, beside its
                         square and that mean: the two integrals in the taper
                         efficiency, 0.637 squared over 0.500 = 0.811

    python3 scripts/graphics/l15_figures.py
"""

from __future__ import annotations
import io
import re
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from scipy.optimize import brentq
from scipy.special import j1
from svg_font_stack import apply_font_stack

NAVY, BLUE, RED, GREEN, AMBER, GRAY = "#004a85", "#0067b9", "#b01e24", "#1d7a4d", "#8a5a00", "#5b6573"
INK, RULE, SHADE = "#15202b", "#c7d2e0", "#dbe8f4"
ROOT = Path(__file__).resolve().parents[2]
OUTS = [ROOT / "book/extras/slides/fig", ROOT / "book/extras/viz/img"]

plt.rcParams.update({"svg.fonttype": "none", "font.size": 11.5, "text.color": INK,
                     "axes.edgecolor": GRAY, "axes.labelcolor": INK,
                     "xtick.color": GRAY, "ytick.color": GRAY,
                     "xtick.labelsize": 11, "ytick.labelsize": 11})
BOX = dict(fc="white", ec="none", alpha=0.92, pad=1.5)

XI = np.linspace(-0.5, 0.5, 4001)            # x / L across the aperture
TAPERS = [("uniform", np.ones_like(XI), NAVY),
          ("cosine", np.cos(np.pi * XI), BLUE),
          ("triangular", 1 - 2 * np.abs(XI), GREEN),
          ("cosine²", np.cos(np.pi * XI) ** 2, RED)]


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
    ax.grid(color=RULE, lw=0.6)
    ax.set_axisbelow(True)


def db(x):
    return 20 * np.log10(np.maximum(np.abs(x), 1e-6))


def sinc_u(u):
    return np.sinc(u)                         # sin(pi u) / (pi u)


def airy_v(v):
    """Uniform circle, 2 J1(pi v) / (pi v), v = (D/lambda) sin(theta)."""
    x = np.pi * np.asarray(v, float)
    out = np.ones_like(x)
    nz = np.abs(x) > 1e-9
    out[nz] = 2 * j1(x[nz]) / x[nz]
    return out


def space_factor(a, u):
    """|S(u)| / S(0) from the aperture integral, u = (L/lambda) sin(theta)."""
    u = np.atleast_1d(u)
    s = np.trapezoid(a[None, :] * np.cos(2 * np.pi * u[:, None] * XI[None, :]), XI, axis=1)
    return np.abs(s) / np.trapezoid(a, XI)


def half_power(f, hi=3.0):
    """u at which the normalized field f(u) falls to 1/sqrt 2."""
    return brentq(lambda u: f(np.array([u]))[0] - 2 ** -0.5, 1e-6, hi)


def first_sidelobe(f, u_max=6.0):
    u = np.linspace(1e-4, u_max, 60001)
    y = np.abs(f(u))
    k = next(i for i in range(1, len(y) - 1) if y[i] > y[i - 1] and y[i] >= y[i + 1])
    return u[k], db(y[k])


# ------------------------------------------------------------ shape vs size
def shape_vs_size():
    Ls = [(2, AMBER), (5, BLUE), (20, NAVY)]
    uh = half_power(sinc_u)
    usl, sl = first_sidelobe(sinc_u)
    U_MAX = 6.0
    fig = plt.figure(figsize=(5.0, 5.3))
    gs = fig.add_gridspec(4, 1, height_ratios=[0.40, 1, 0.46, 1], hspace=0.08)
    strip = fig.add_subplot(gs[0])
    top = fig.add_subplot(gs[1], sharex=strip)
    bot = fig.add_subplot(gs[3])             # gs[2] is the gap for the axis label and title

    # strip: how much of the u axis each length can see (visible space is |u| <= L/lambda)
    for row, (L, col) in enumerate(Ls):
        y = len(Ls) - 1 - row
        end = min(L, U_MAX)
        if L <= U_MAX:
            strip.plot([0, end], [y, y], color=col, lw=5, solid_capstyle="butt")
            strip.text(end + 0.08, y, f"L = {L}λ", color=col, fontsize=10.5,
                       ha="left", va="center", fontweight="bold")
        else:
            strip.annotate("", (U_MAX, y), (0, y), arrowprops=dict(arrowstyle="-|>", color=col,
                           lw=5, mutation_scale=16, shrinkA=0, shrinkB=0))
            strip.text(U_MAX / 2, y, f"L = {L}λ: to u = {L}", color=col, fontsize=10.5,
                       ha="center", va="center", fontweight="bold",
                       bbox=dict(fc="white", ec="none", pad=2))
        if L <= U_MAX:                       # carry the edge down into the pattern
            top.axvline(L, color=col, lw=1.4, ls=(0, (2, 2)))
    strip.text(0, len(Ls) - 0.35, "visible part of the u axis", color=GRAY, fontsize=10.5,
               ha="left", va="bottom")
    strip.set_ylim(-0.7, len(Ls) + 0.35)
    strip.axis("off")
    strip.set_title("Shape: one curve in u", color=INK, fontsize=12.5,
                    fontweight="bold", loc="left")

    u = np.linspace(0, U_MAX, 3001)
    top.plot(u, db(sinc_u(u)), color=INK, lw=2.2)
    top.axhline(sl, color=RED, lw=1.1, ls=(0, (4, 3)))
    top.text(U_MAX - 0.05, sl + 1.2, f"first sidelobe {_m(sl)} dB", color=RED, fontsize=10.5,
             ha="right", va="bottom", bbox=BOX)
    top.set_xlim(0, U_MAX)
    top.set_ylim(-40, 2)
    top.set_yticks([0, -10, -20, -30, -40])
    top.set_xlabel("space frequency u")
    top.set_ylabel("pattern (dB)")
    clean(top)

    # bottom: the same shape against angle, three widths
    th = np.linspace(0, 90, 9001)
    hp = {}
    for L, col in reversed(Ls):              # widest drawn last, on top
        y = db(sinc_u(L * np.sin(np.radians(th))))
        bot.plot(th, y, color=col, lw=1.2 if L == 20 else 2.0)
        hp[L] = 2 * np.degrees(np.arcsin(uh / L))
        bot.plot([hp[L] / 2], [-3.01], "o", color=col, ms=6, mec="white", mew=1, zorder=5)
    bot.axhline(sl, color=RED, lw=1.1, ls=(0, (4, 3)))
    # labels stacked in the empty band above the 2-wavelength sidelobe (which peaks at
    # the sidelobe level), right of its main lobe; spaced by the band's own height
    x_lab = 2 * hp[2]
    band = np.linspace(0.8, sl + 5.0, len(Ls))
    for (L, col), y in zip(sorted(Ls, key=lambda p: -p[0]), band):
        bot.text(x_lab, y, f"{L}λ: {hp[L]:.1f}° beam", color=col, fontsize=10.5,
                 ha="left", va="top", fontweight="bold", bbox=BOX)
    bot.set_xlim(0, 90)
    bot.set_ylim(-40, 2)
    bot.set_xticks([0, 15, 30, 45, 60, 75, 90])
    bot.set_yticks([0, -10, -20, -30, -40])
    bot.set_xlabel("angle from broadside (degrees)")
    bot.set_ylabel("pattern (dB)")
    bot.set_title("Size: rescales the angle", color=INK, fontsize=12.5, fontweight="bold", loc="left")
    clean(bot)
    fig.subplots_adjust(left=0.15, right=0.97, top=0.95, bottom=0.08)
    save(fig, "L15-shape-vs-size",
         "Top: the uniform aperture pattern against space frequency u is one curve for every "
         "length; an aperture 2, 5, or 20 wavelengths long sees it out to u = 2, 5, or 20. "
         "Bottom: the same three apertures against angle have beams "
         f"{hp[2]:.1f}, {hp[5]:.1f}, and {hp[20]:.1f} degrees wide, and all three first sidelobes "
         f"sit at {sl:.1f} dB")
    return dict(u_hp=uh, u_sl=usl, sl=sl, hpbw={k: round(v, 2) for k, v in hp.items()})


# --------------------------------------------------------------- taper trade
def taper_numbers():
    rows = []
    for name, a, col in TAPERS:
        f = lambda u, a=a: space_factor(a, u)
        uh = half_power(f)
        _, sl = first_sidelobe(f)
        eta = np.trapezoid(a, XI) ** 2 / np.trapezoid(a ** 2, XI)
        rows.append((name, col, sl, 2 * uh, eta, 10 * np.log10(eta)))
    return rows


def taper_trade():
    rows = taper_numbers()
    fig, ax = plt.subplots(figsize=(5.4, 3.9))
    xs = [r[2] for r in rows]
    ys = [r[3] for r in rows]
    ax.plot(xs, ys, color=RULE, lw=2.0, zorder=1)
    for name, col, sl, hp, eta, g in rows:
        ax.plot([sl], [hp], "o", color=col, ms=11, mec="white", mew=1.5, zorder=4)
    # labels alternate sides of the rising line: below-right, then above-left.
    # Both regions are empty because the line climbs monotonically.
    for i, (name, col, sl, hp, eta, g) in enumerate(rows):
        gain = "full gain" if abs(g) < 1e-3 else f"{_m(g, '{:.2f}')} dB gain"
        below = i % 2 == 0
        ax.text(sl + (-0.7 if below else 0.7), hp + (-0.035 if below else 0.035),
                f"{name}\n{_m(sl)} dB, {hp:.3f}\n{gain}", color=col, fontsize=10.5,
                ha="left" if below else "right", va="top" if below else "bottom",
                bbox=BOX, zorder=5, linespacing=1.15, multialignment="left")
    # the trend, in the empty corner below-right of the rising line
    ax.text(-36.5, 0.69, "lower sidelobes widen\nthe beam and lose gain", color=GRAY, fontsize=10.5,
            ha="right", va="bottom", fontstyle="italic", multialignment="right")
    ax.set_xlim(-10, -37)                        # lower sidelobes to the right
    ax.set_ylim(0.66, 1.62)
    ax.set_xticks([-10, -20, -30])
    ax.set_xticklabels([_m(t, "{:.0f}") for t in [-10, -20, -30]])
    ax.set_xlabel("first sidelobe (dB)")
    ax.set_ylabel("beamwidth constant (× λ/L)")
    clean(ax)
    fig.tight_layout()
    save(fig, "L15-taper-trade",
         "The four illuminations as points of first sidelobe against beamwidth constant: "
         + "; ".join(f"{n} {sl:.1f} dB, {hp:.3f}, {g:.2f} dB gain" for n, _, sl, hp, _, g in rows)
         + ". Every step to lower sidelobes widens the beam and loses gain")
    return [(n, round(sl, 2), round(hp, 3), round(e, 3), round(g, 2)) for n, _, sl, hp, e, g in rows]


# ----------------------------------------------------------- circle vs square
def circle_vs_square():
    vh_s, vh_c = half_power(sinc_u), half_power(airy_v)
    vsl_s, sl_s = first_sidelobe(sinc_u)
    vsl_c, sl_c = first_sidelobe(airy_v)
    v = np.linspace(0, 3.2, 3201)
    fig, ax = plt.subplots(figsize=(5.4, 2.6))
    ax.plot(v, db(sinc_u(v)), color=GRAY, lw=2.0)
    ax.plot(v, db(airy_v(v)), color=NAVY, lw=2.6)
    ax.axhline(-3.01, color=RULE, lw=1, ls=(0, (4, 3)))
    for vh, sl, vsl, col, name in ((vh_s, sl_s, vsl_s, GRAY, "square"),
                                   (vh_c, sl_c, vsl_c, NAVY, "circle")):
        ax.plot([vh], [-3.01], "o", color=col, ms=6, zorder=5)
        ax.plot([vsl], [sl], "o", color=col, ms=6, zorder=5)
    # half-power widths: a block in the empty corner under the main lobes, below
    # where either main lobe has fallen past the block's right edge
    ax.text(0.04, -24.5, "half-power beam", color=INK, fontsize=10.5, ha="left", va="top")
    ax.text(0.04, -28.5, f"square  {2*vh_s:.3f}", color=GRAY, fontsize=10.5, ha="left",
            va="top", fontweight="bold")
    ax.text(0.04, -32.5, f"circle  {2*vh_c:.3f}", color=NAVY, fontsize=10.5, ha="left",
            va="top", fontweight="bold")
    # sidelobe labels: above each sidelobe peak
    ax.text(vsl_s, sl_s + 1.4, f"{_m(sl_s)} dB", color=GRAY, fontsize=10.5, ha="center",
            va="bottom", fontweight="bold", bbox=BOX)
    # the circle's label sits up and to the right of its peak, in the gap between
    # the square's falling sidelobe and the inset, with a leader to the peak
    ax.annotate(f"{_m(sl_c)} dB", (vsl_c, sl_c), (vsl_c + 0.17, sl_c + 3.2), color=NAVY,
                fontsize=10.5, ha="left", va="center", fontweight="bold", bbox=BOX,
                arrowprops=dict(arrowstyle="-", color=NAVY, lw=0.9, shrinkA=0, shrinkB=3))
    ax.set_xlim(0, 3.2)
    ax.set_ylim(-40, 1.5)
    ax.set_yticks([0, -10, -20, -30, -40])
    ax.set_xlabel("sine of angle × width in wavelengths")
    ax.set_xticks([0, 1, 2, 3])
    ax.set_ylabel("pattern (dB)")
    clean(ax)

    # inset: what each aperture looks like projected onto one cut
    ins = ax.inset_axes([0.58, 0.68, 0.41, 0.29])
    x = np.linspace(-1, 1, 401)
    ins.fill_between(x, np.sqrt(1 - x ** 2), color=SHADE, lw=0)
    ins.plot([-1, -1, 1, 1], [0, 1, 1, 0], color=GRAY, lw=1.6)
    ins.plot(x, np.sqrt(1 - x ** 2), color=NAVY, lw=2.0)
    ins.text(0, 1.06, "square: flat", color=GRAY, fontsize=10.5, ha="center", va="bottom")
    ins.text(0, 0.45, "circle: tapered", color=NAVY, fontsize=10.5, ha="center", va="center")
    ins.set_xlim(-1.15, 1.15)
    ins.set_ylim(0, 1.5)
    ins.set_xticks([])
    ins.set_yticks([])
    for side in ("top", "right", "left"):
        ins.spines[side].set_visible(False)
    ins.set_facecolor("white")
    fig.tight_layout()
    save(fig, "L15-circle-vs-square",
         f"Uniform square and uniform circular apertures of the same width against sine of angle "
         f"times width in wavelengths: the circle's beam is {2*vh_c:.3f} against {2*vh_s:.3f} and "
         f"its first sidelobe {sl_c:.1f} dB against {sl_s:.1f} dB, because projected onto one cut "
         f"the circle is already tapered toward its edges")
    return dict(hp_square=2 * vh_s, hp_circle=2 * vh_c, sl_square=sl_s, sl_circle=sl_c,
                v_sl_square=vsl_s, v_sl_circle=vsl_c, u_hp_circle_with_pi=np.pi * vh_c)


# --------------------------------------------------------- efficiency ratio
def efficiency_ratio():
    a = np.cos(np.pi * XI)
    m1 = np.trapezoid(a, XI)                  # length 1, so the integral is the mean
    m2 = np.trapezoid(a ** 2, XI)
    eta = m1 ** 2 / m2
    fig, axs = plt.subplots(1, 2, figsize=(5.6, 2.15), sharey=True)
    for ax, y, m, col, title, what in (
            (axs[0], a, m1, BLUE, "field", "coherent sum"),
            (axs[1], a ** 2, m2, AMBER, "field squared", "available power")):
        ax.fill_between(XI, y, color=SHADE, lw=0)
        ax.plot(XI, y, color=col, lw=2.4)
        ax.axhline(m, xmin=0, xmax=1, color=INK, lw=1.4, ls=(0, (5, 3)))
        ax.text(0, m - 0.05, f"mean {m:.3f}", color=INK, fontsize=10.5, ha="center", va="top",
                fontweight="bold", bbox=dict(fc=SHADE, ec="none", pad=1.5))
        ax.text(0, m / 2 - 0.05, what, color=INK, fontsize=10.5, ha="center", va="center")
        ax.set_title(title, color=col, fontsize=12, fontweight="bold")
        ax.set_xlim(-0.5, 0.5)
        ax.set_ylim(0, 1.08)
        ax.set_xticks([-0.5, 0, 0.5])
        ax.set_xticklabels(["edge", "center", "edge"])
        ax.get_xticklabels()[0].set_ha("left"); ax.get_xticklabels()[-1].set_ha("right")
        ax.set_yticks([0, 0.5, 1.0])
        clean(ax)
    fig.text(0.5, 0.0, f"taper efficiency = {m1:.3f}² / {m2:.3f} = {eta:.3f}",
             ha="center", va="bottom", fontsize=12, fontweight="bold", color=NAVY)
    fig.subplots_adjust(left=0.09, right=0.97, top=0.88, bottom=0.30, wspace=0.28)
    save(fig, "L15-efficiency-ratio",
         f"Left: the cosine illumination across the aperture with its mean, {m1:.3f}, the coherent "
         f"sum. Right: its square with mean {m2:.3f}, the available power. The taper efficiency is "
         f"{m1:.3f} squared over {m2:.3f}, or {eta:.3f}")
    return dict(mean_field=m1, mean_power=m2, eta=eta, two_over_pi=2 / np.pi)


if __name__ == "__main__":
    print("shape:", shape_vs_size())
    print("trade:", taper_trade())
    print("circle:", circle_vs_square())
    print("ratio:", efficiency_ratio())
