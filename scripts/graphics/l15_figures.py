#!/usr/bin/env python3
"""L15: the computed figures from the 2026-10-04 illustration sweep (Batches A-C).

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
  L15-rect-footprint     the X-band aperture (0.682 m by 0.152 m) to scale
                         beside the half-power contour of its beam (3 by 10
                         degrees): the long dimension makes the narrow beam
  L15-xband-flow         the X-band design chain, sidelobe spec to illumination
                         to length, elevation beam to length, area and
                         efficiency to gain, and the gain against the
                         pencil-beam bound and practical band
  L15-sidelobe-decay     uniform, cosine, and cosine-squared patterns on a log
                         u axis with their far-sidelobe envelopes, 1/u, 1/u^2,
                         1/u^3: 6, 12, and 18 dB per octave
  L15-path-difference    the 1-D aperture, the angle from broadside, and the
                         extra path x sin(theta) to a far-field direction
  L15-frequency-scaling  one 0.30 m uniform aperture from 1 to 20 GHz: exact
                         half-power beamwidth and the area-limited gain of the
                         0.30 m square, with 3 and 10 GHz marked

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


# ------------------------------------------------------- X-band design numbers
# Rounded the way the page rounds them: the table's constants, lengths to the
# millimeter, area to 0.001 square meter, efficiency to two places.
XB = dict(f=10e9, az=3.0, el=10.0, sl_spec=-20.0)


def xband():
    lam = 3e8 / XB["f"]
    rows = {r[0]: r for r in taper_numbers()}
    k_cos = round(rows["cosine"][3], 2)                 # 1.19
    k_uni = round(rows["uniform"][3], 3)                # 0.886
    sl_cos = rows["cosine"][2]
    Lx = k_cos * lam / np.radians(XB["az"])
    Ly = k_uni * lam / np.radians(XB["el"])
    A = round(round(Lx, 3) * round(Ly, 3), 3)
    eta = round(rows["cosine"][4], 2) * round(rows["uniform"][4], 2)
    G = eta * 4 * np.pi * A / lam ** 2
    return dict(lam=lam, k_cos=k_cos, k_uni=k_uni, sl_cos=sl_cos, sl_uni=rows["uniform"][2],
                Lx=Lx, Ly=Ly, A=A, eta=eta, G=G, G_dbi=10 * np.log10(G),
                bound=10 * np.log10(41253 / (XB["az"] * XB["el"])),
                band=(10 * np.log10(26000 / (XB["az"] * XB["el"])),
                      10 * np.log10(32400 / (XB["az"] * XB["el"]))))


def cos_field(u):
    """Normalized cosine-illumination pattern, cos(pi u) / (1 - 4 u^2)."""
    u = np.asarray(u, float)
    out = np.empty_like(u)
    near = np.abs(np.abs(u) - 0.5) < 1e-9
    out[~near] = np.cos(np.pi * u[~near]) / (1 - 4 * u[~near] ** 2)
    out[near] = np.pi / 4
    return out


def cos2_field(u):
    """Normalized cosine-squared pattern, sinc(u) / (1 - u^2)."""
    u = np.asarray(u, float)
    out = np.empty_like(u)
    near = np.abs(np.abs(u) - 1) < 1e-9
    out[~near] = np.sinc(u[~near]) / (1 - u[~near] ** 2)
    out[near] = 0.5
    return out


# --------------------------------------------------------- rectangle footprint
def rect_footprint():
    x = xband()
    lam, Lx, Ly = x["lam"], round(x["Lx"], 3), round(x["Ly"], 3)
    nx, ny = x["Lx"] / lam, x["Ly"] / lam      # wavelengths from the unrounded lengths
    fig, (ax, bx) = plt.subplots(1, 2, figsize=(6.0, 2.9),
                                 gridspec_kw=dict(width_ratios=[1.35, 1], wspace=0.32))
    # left: the aperture to scale, in meters
    ax.add_patch(plt.Rectangle((-Lx / 2, -Ly / 2), Lx, Ly, fc=SHADE, ec=NAVY, lw=2.0))
    ax.annotate("", (Lx / 2, -Ly / 2 - 0.05), (-Lx / 2, -Ly / 2 - 0.05),
                arrowprops=dict(arrowstyle="<|-|>", color=INK, lw=1.0, mutation_scale=9,
                                shrinkA=0, shrinkB=0))
    ax.text(0, -Ly / 2 - 0.075, f"{Lx:.3f} m = {nx:.1f}λ", color=INK, fontsize=10.5,
            ha="center", va="top")
    ax.annotate("", (Lx / 2 + 0.035, Ly / 2), (Lx / 2 + 0.035, -Ly / 2),
                arrowprops=dict(arrowstyle="<|-|>", color=INK, lw=1.0, mutation_scale=9,
                                shrinkA=0, shrinkB=0))
    ax.text(Lx / 2 - 0.02, Ly / 2 + 0.03, f"{Ly:.3f} m = {ny:.2f}λ", color=INK,
            fontsize=10.5, ha="right", va="bottom")
    ax.text(0, 0, "cosine across, uniform up", color=NAVY, fontsize=10.5, ha="center",
            va="center")
    ax.set_xlim(-Lx / 2 - 0.02, Lx / 2 + 0.06)
    ax.set_ylim(-Ly / 2 - 0.16, Ly / 2 + 0.14)
    ax.set_aspect("equal")
    ax.axis("off")
    ax.set_title("aperture: wide and short", color=INK, fontsize=12, fontweight="bold")

    # right: the half-power contour of the product pattern, in degrees
    g = np.linspace(-8, 8, 801)
    AZ, EL = np.meshgrid(g, g)
    P = (np.abs(cos_field(Lx / lam * np.sin(np.radians(AZ))))
         * np.abs(sinc_u(Ly / lam * np.sin(np.radians(EL)))))
    bx.contourf(AZ, EL, P, levels=[2 ** -0.5, 1.01], colors=[SHADE])
    bx.contour(AZ, EL, P, levels=[2 ** -0.5], colors=[NAVY], linewidths=2.0)
    # the widths, measured from the cuts of the same pattern
    w_az = 2 * brentq(lambda a: cos_field(np.array([Lx / lam * np.sin(np.radians(a))]))[0]
                      - 2 ** -0.5, 1e-4, 8)
    w_el = 2 * brentq(lambda a: sinc_u(np.array([Ly / lam * np.sin(np.radians(a))]))[0]
                      - 2 ** -0.5, 1e-4, 8)
    bx.text(w_az / 2 + 0.6, 0, f"{w_az:.1f}° wide", color=INK, fontsize=10.5,
            ha="left", va="center")
    bx.text(0, w_el / 2 + 0.4, f"{w_el:.1f}° tall", color=INK, fontsize=10.5,
            ha="center", va="bottom")
    bx.set_xlim(-8, 8)
    bx.set_ylim(-8, 8)
    bx.set_aspect("equal")
    bx.set_xticks([-5, 0, 5])
    bx.set_yticks([-5, 0, 5])
    bx.set_xticklabels([_m(t, "{:.0f}") for t in (-5, 0, 5)])
    bx.set_yticklabels([_m(t, "{:.0f}") for t in (-5, 0, 5)])
    bx.set_xlabel("azimuth (degrees)")
    bx.set_ylabel("elevation (degrees)")
    bx.set_title("beam: narrow and tall", color=INK, fontsize=12, fontweight="bold")
    clean(bx)
    fig.subplots_adjust(left=0.02, right=0.98, top=0.88, bottom=0.17)
    save(fig, "L15-rect-footprint",
         f"Left: the X-band aperture to scale, {Lx:.3f} m wide and {Ly:.3f} m tall, cosine "
         f"illumination across and uniform up. Right: the half-power contour of its beam, "
         f"{w_az:.1f} degrees wide in azimuth and {w_el:.1f} degrees tall in elevation. The long "
         f"dimension makes the narrow beam")
    return dict(Lx=Lx, Ly=Ly, Lx_lam=nx, Ly_lam=ny, w_az=w_az, w_el=w_el)


# ------------------------------------------------------------ X-band flow
def xband_flow():
    x = xband()
    lam = x["lam"]
    fig = plt.figure(figsize=(5.4, 3.9))
    ax = fig.add_axes([0, 0.30, 1, 0.70])
    ax.set_xlim(0, 102.6)
    ax.set_ylim(0, 63)
    ax.axis("off")
    W, H = 28.5, 13
    cols = [14.6, 50.6, 86.0]
    BUS = 102.0                                # both lengths join here on the way to the area

    def box(cx, cy, text, ec=NAVY, fc="white", bold=False):
        ax.add_patch(plt.Rectangle((cx - W / 2, cy - H / 2), W, H, fc=fc, ec=ec, lw=1.6))
        ax.text(cx, cy, text, color=INK, fontsize=10.5, ha="center", va="center",
                linespacing=1.2, fontweight="bold" if bold else "normal")

    def arrow(p, q):
        ax.annotate("", q, p, arrowprops=dict(arrowstyle="-|>", color=GRAY, lw=1.4,
                                              mutation_scale=12, shrinkA=0, shrinkB=0))

    y_az, y_el, y_g = 51, 30, 8
    box(cols[0], y_az, f"sidelobes below\n{_m(XB['sl_spec'], '{:.0f}')} dB in azimuth")
    box(cols[1], y_az, f"cosine, {_m(x['sl_cos'], '{:.0f}')} dB\nconstant {x['k_cos']:.2f}")
    box(cols[2], y_az, f"azimuth length\n{x['Lx']:.3f} m, {x['Lx']/lam:.1f}λ")
    box(cols[0], y_el, "no elevation\nsidelobe limit")
    box(cols[1], y_el, f"uniform, {_m(x['sl_uni'])} dB\nconstant {x['k_uni']:.3f}")
    box(cols[2], y_el, f"elevation length\n{x['Ly']:.3f} m, {x['Ly']/lam:.2f}λ")
    for y, beam in ((y_az, XB["az"]), (y_el, XB["el"])):
        arrow((cols[0] + W / 2, y), (cols[1] - W / 2, y))
        arrow((cols[1] + W / 2, y), (cols[2] - W / 2, y))
        ax.plot([cols[2] + W / 2, BUS], [y, y], color=GRAY, lw=1.4)
        # the beam requirement enters at the length box, written on top of it
        ax.text(cols[2], y + H / 2 + 0.8, f"for a {beam:.0f}° beam", color=AMBER,
                fontsize=10.5, ha="center", va="bottom", fontweight="bold")
    box(cols[1], y_g, f"area {x['A']:.3f} m²\nefficiency {x['eta']:.2f}")
    box(cols[0], y_g, f"gain\n{x['G_dbi']:.1f} dBi", ec=RED, fc=SHADE, bold=True)
    ax.plot([BUS, BUS], [y_az, y_g], color=GRAY, lw=1.4)
    arrow((BUS, y_g), (cols[1] + W / 2, y_g))
    arrow((cols[1] - W / 2, y_g), (cols[0] + W / 2, y_g))

    # the check: the gain on a dBi scale against the pencil-beam numbers
    cx = fig.add_axes([0.06, 0.10, 0.80, 0.12])
    lo, hi = x["band"]
    cx.axvspan(lo, hi, ymin=0.15, ymax=0.85, color=SHADE, lw=0)
    cx.text((lo + hi) / 2, 0.5, "practical band", color=NAVY, fontsize=10.5, ha="center",
            va="center")
    cx.axvline(x["bound"], ymin=0.1, ymax=0.9, color=GRAY, lw=1.8)
    cx.text(x["bound"] + 0.04, 0.5, f"bound\n{x['bound']:.1f}", color=GRAY, fontsize=10.5,
            ha="left", va="center", linespacing=1.1)
    cx.plot([x["G_dbi"]], [0.5], "o", color=RED, ms=9, mec="white", mew=1.2, zorder=5)
    cx.text(x["G_dbi"], 0.95, f"{x['G_dbi']:.1f}", color=RED, fontsize=10.5, ha="center",
            va="bottom", fontweight="bold")
    cx.set_xlim(29.0, 32.0)
    cx.set_ylim(0, 1)
    cx.set_yticks([])
    cx.set_xticks([lo, hi, 31.0, 32.0])
    cx.set_xticklabels([f"{lo:.1f}", f"{hi:.1f}", "31.0", "32.0"])
    for side in ("top", "right", "left"):
        cx.spines[side].set_visible(False)
    cx.set_xlabel("gain (dBi)")
    save(fig, "L15-xband-flow",
         f"The X-band design chain. The azimuth sidelobe limit of {XB['sl_spec']:.0f} dB picks the "
         f"cosine illumination, constant {x['k_cos']:.2f}, and the {XB['az']:.0f} degree beam then "
         f"fixes the azimuth length at {x['Lx']:.3f} m. Elevation has no sidelobe limit, so it stays "
         f"uniform, constant {x['k_uni']:.3f}, and the {XB['el']:.0f} degree beam fixes "
         f"{x['Ly']:.3f} m. Area {x['A']:.3f} square meters at efficiency {x['eta']:.2f} gives "
         f"{x['G_dbi']:.1f} dBi, just above the practical band of {lo:.1f} to {hi:.1f} dBi and "
         f"below the {x['bound']:.1f} dBi pencil-beam bound")
    return {k: (round(v, 4) if isinstance(v, float) else v) for k, v in x.items()}


# ----------------------------------------------------------- sidelobe decay
def sidelobe_decay():
    u = np.geomspace(0.5, 16, 40001)
    # closed forms, checked against the aperture integral
    for name, a, _ in TAPERS:
        f = {"uniform": sinc_u, "cosine": cos_field, "cosine²": cos2_field}.get(name)
        if f is not None:
            uu = np.array([0.3, 1.43, 2.6, 5.5])
            assert np.allclose(np.abs(f(uu)), space_factor(a, uu), atol=2e-5), name
    curves = [("uniform", sinc_u, lambda v: 1 / (np.pi * v), 6, NAVY),
              ("cosine", cos_field, lambda v: 1 / (4 * v ** 2), 12, BLUE),
              ("cosine²", cos2_field, lambda v: 1 / (np.pi * v ** 3), 18, RED)]
    fig, ax = plt.subplots(figsize=(5.8, 3.4))
    slopes = {}
    ue = np.geomspace(2.0, 16, 50)
    for name, f, env, rate, col in curves:
        ax.plot(u, db(f(u)), color=col, lw=0.9, alpha=0.75)
        ax.plot(ue, db(env(ue)), color=col, lw=2.2, ls=(0, (5, 3)))
        slopes[name] = db(env(np.array([8.0])))[0] - db(env(np.array([16.0])))[0]
        y_end = db(env(np.array([16.0])))[0]
        ax.text(17.0, y_end, f"{name}\n{_m(-rate, '{:.0f}')} dB per octave", color=col,
                fontsize=10.5, ha="left", va="center", fontweight="bold", linespacing=1.15,
                clip_on=False)
    ax.set_xscale("log", base=2)
    ax.set_xlim(0.5, 16)
    ax.set_xticks([0.5, 1, 2, 4, 8, 16])
    ax.set_xticklabels(["0.5", "1", "2", "4", "8", "16"])
    ax.minorticks_off()
    ax.set_ylim(-90, 3)
    ax.set_yticks([0, -20, -40, -60, -80])
    ax.set_yticklabels(["0"] + [_m(t, "{:.0f}") for t in (-20, -40, -60, -80)])
    ax.set_xlabel("space frequency u (each tick one octave)")
    ax.set_ylabel("pattern (dB)")
    clean(ax)
    fig.subplots_adjust(left=0.12, right=0.70, top=0.97, bottom=0.15)
    save(fig, "L15-sidelobe-decay",
         "Uniform, cosine, and cosine-squared patterns against space frequency on a log scale, "
         "each with the dashed envelope its sidelobes follow: the uniform sidelobes fall 6 dB per "
         "octave, the cosine's 12, and the cosine-squared's 18")
    return {k: round(v, 2) for k, v in slopes.items()}


# ---------------------------------------------------------- path difference
def path_difference():
    th = np.radians(30)
    L = 10.0
    xp = 3.4                                   # the point at x, right of center
    d = np.array([np.sin(th), np.cos(th)])     # direction to the far-field point
    fig, ax = plt.subplots(figsize=(5.4, 3.4))
    # the aperture
    ax.add_patch(plt.Rectangle((-L / 2, -0.35), L, 0.35, fc=SHADE, ec=NAVY, lw=1.8))
    ax.text(-L / 2, -0.6, "aperture", color=NAVY, fontsize=10.5, ha="left", va="top")
    ax.plot([0], [0], "o", color=INK, ms=5, zorder=5)
    ax.plot([xp], [0], "o", color=INK, ms=5, zorder=5)
    ax.text(0, -0.6, "center", color=INK, fontsize=10.5, ha="center", va="top")
    ax.annotate("", (xp, -1.55), (0, -1.55), arrowprops=dict(arrowstyle="<|-|>", color=INK,
                lw=1.0, mutation_scale=9, shrinkA=0, shrinkB=0))
    ax.text(xp / 2, -1.7, "x", color=INK, fontsize=12, ha="center", va="top", fontstyle="italic")
    # broadside, and the rays to the far-field point
    R = 6.2
    ax.plot([0, 0], [0, R], color=GRAY, lw=1.0, ls=(0, (4, 3)))
    ax.text(0, R + 0.15, "broadside", color=GRAY, fontsize=10.5, ha="center", va="bottom")
    for p0 in (np.array([0.0, 0.0]), np.array([xp, 0.0])):
        ax.annotate("", p0 + R * d, p0, arrowprops=dict(arrowstyle="-|>", color=BLUE, lw=1.6,
                    mutation_scale=12, shrinkA=0, shrinkB=0))
    ax.text(xp + R * d[0] + 0.1, R * d[1], "to the far field", color=BLUE, fontsize=10.5,
            ha="left", va="center")
    # angle from broadside at the center
    arc = np.linspace(np.pi / 2, np.pi / 2 - th, 40)
    ax.plot(1.6 * np.cos(arc), 1.6 * np.sin(arc), color=INK, lw=1.0)
    mid = np.pi / 2 - th / 2
    ax.text(1.95 * np.cos(mid), 1.95 * np.sin(mid), "θ", color=INK, fontsize=12.5,
            ha="center", va="center", fontstyle="italic")
    # the wavefront through x, and the extra path along the center ray
    s = xp * np.sin(th)
    foot = s * d
    ax.plot([xp, foot[0]], [0, foot[1]], color=GRAY, lw=1.2, ls=(0, (2, 2)))
    ax.plot([0, foot[0]], [0, foot[1]], color=RED, lw=4.0, solid_capstyle="butt", zorder=4)
    nrm = np.array([-d[1], d[0]])              # left of the ray
    lab = foot / 2 + 0.35 * nrm
    ax.text(lab[0], lab[1], "extra path x sin θ\nextra phase k x sin θ", color=RED,
            fontsize=10.5, ha="right", va="center", fontweight="bold", linespacing=1.25,
            multialignment="right", bbox=BOX)
    ax.set_xlim(-L / 2 - 0.2, L / 2 + 3.6)
    ax.set_ylim(-2.3, R + 0.7)
    ax.set_aspect("equal")
    ax.axis("off")
    fig.subplots_adjust(left=0.01, right=0.99, top=0.99, bottom=0.01)
    save(fig, "L15-path-difference",
         "A one-dimensional aperture with its center and a point a distance x from the center. "
         "Parallel rays leave both toward a far-field direction at angle theta from broadside, and "
         "the ray from the center travels an extra x sine theta, which is a phase of k x sine theta")
    return dict(theta_deg=30, x=xp, path=s)


# --------------------------------------------------------- frequency scaling
def frequency_scaling():
    L = 0.30
    uh = half_power(sinc_u)                    # 0.4429
    f = np.linspace(1, 20, 1901)
    lam = 3e8 / (f * 1e9)
    hp_exact = np.degrees(2 * np.arcsin(uh * lam / L))
    gain = 10 * np.log10(4 * np.pi * L ** 2 / lam ** 2)
    fig, (ax, bx) = plt.subplots(2, 1, figsize=(5.4, 4.4), sharex=True,
                                 gridspec_kw=dict(hspace=0.16))
    ax.plot(f, hp_exact, color=NAVY, lw=2.4)
    bx.plot(f, gain, color=RED, lw=2.4)
    marks = {}
    for f0 in (3, 10):
        l0 = 3e8 / (f0 * 1e9)
        h = np.degrees(2 * np.arcsin(uh * l0 / L))
        hs = np.degrees(2 * uh * l0 / L)
        g = 10 * np.log10(4 * np.pi * L ** 2 / l0 ** 2)
        marks[f0] = (round(L / l0, 2), round(h, 2), round(hs, 2), round(g, 2))
        ax.plot([f0], [h], "o", color=NAVY, ms=7, mec="white", mew=1.2, zorder=5)
        bx.plot([f0], [g], "o", color=RED, ms=7, mec="white", mew=1.2, zorder=5)
        hd = f"{h:.2f}" if h < 10 else f"{h:.1f}"
        ax.text(f0 + 0.5, h + 1.5, f"{f0} GHz, {L/l0:.0f}λ: {hd}°", color=NAVY,
                fontsize=10.5, ha="left", va="bottom", fontweight="bold", bbox=BOX)
        bx.text(f0 + 0.5, g - 1.2, f"{g:.1f} dBi", color=RED, fontsize=10.5, ha="left",
                va="top", fontweight="bold", bbox=BOX)
    ax.set_ylim(0, 60)
    ax.set_yticks([0, 20, 40, 60])
    ax.set_ylabel("beamwidth (deg)")
    ax.set_title("one 0.30 m uniform aperture", color=INK, fontsize=12, fontweight="bold",
                 loc="left")
    clean(ax)
    bx.set_ylim(5, 45)
    bx.set_yticks([10, 20, 30, 40])
    bx.set_ylabel("gain, 0.30 m square (dBi)")
    bx.set_xlim(1, 20)
    bx.set_xticks([1, 3, 5, 10, 15, 20])
    bx.set_xlabel("frequency (GHz)")
    clean(bx)
    fig.subplots_adjust(left=0.14, right=0.97, top=0.94, bottom=0.11)
    save(fig, "L15-frequency-scaling",
         f"One 0.30 m uniform aperture from 1 to 20 GHz. Top: the half-power beamwidth narrows "
         f"from {hp_exact[0]:.0f} degrees at 1 GHz to {marks[3][1]:.1f} at 3 GHz and "
         f"{marks[10][1]:.2f} at 10 GHz. Bottom: the gain of a uniform 0.30 m square rises 6 dB per doubling of "
         f"frequency, {marks[3][3]:.1f} dBi at 3 GHz and {marks[10][3]:.1f} dBi at 10 GHz")
    return marks


if __name__ == "__main__":
    print("shape:", shape_vs_size())
    print("trade:", taper_trade())
    print("circle:", circle_vs_square())
    print("ratio:", efficiency_ratio())
    print("footprint:", rect_footprint())
    print("xband:", xband_flow())
    print("decay:", sidelobe_decay())
    print("path:", path_difference())
    print("scaling:", frequency_scaling())
