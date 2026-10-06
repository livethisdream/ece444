#!/usr/bin/env python3
"""Generate the L13 horn and slot-in-service figures as inline SVG.

L13:
  - L13-horn-flare       : an open-ended waveguide, which radiates a broad,
                           low-gain beam, beside a horn, where the flare lets the
                           wave flow out through a large opening.
  - L13-horn-squares     : the same 20 x 15 cm aperture tiled in square
                           wavelengths at 10 and 20 GHz; four times as many
                           squares is 6 dB more gain.
  - L13-horn-working     : the X-band horn's 33 square wavelengths, and the
                           same tiles shaded by field strength with a hand
                           turned by phase lag: about 17 do the work.
  - L13-horn-phase       : side view of a horn: the spherical front from the
                           apex meets the flat aperture late at the edges, and
                           the phase across the aperture is a parabola.
  - L13-horn-optimum     : gain against aperture width for a horn of fixed
                           length, with and without phase error, computed
                           below. The real curve peaks where the edge lags by
                           a quarter wavelength (uniform E-plane field) and by
                           3/8 wavelength (cosine H-plane field).
  - L13-horn-comparison  : the gain-comparison measurement: the standard-gain
                           horn and the antenna under test read in turn in the
                           same spot; the difference in dB is the difference
                           in gain.
  - L13-slot-service     : a cavity-backed slot in a skin, and a waveguide slot
                           array with its slots offset from the centerline.

Schematics are not to scale. No formulas (deck figure rule), so the lesson-page
copies are the same files.

    python scripts/graphics/l13_horn_figures.py
"""

from __future__ import annotations
import cmath
import math
from pathlib import Path
from l13_patch_figures import (NAVY, BLUE, RED, GRAY, BROWN, RULE, SUB, SUB_EDGE,
                               ROOT, OUTS, text, arrow, markers, svg, ground)

GREEN = "#3f7d34"
METAL = "#dfe7f0"


def dim(x1, y1, x2, y2, color=NAVY, width=1.6) -> str:
    return (f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="{color}" '
            f'stroke-width="{width}" marker-start="url(#ah-{color[1:]})" marker-end="url(#ah-{color[1:]})"/>')


def arcs(cx, cy, radii, half_angle, color, width=2.2, opacity=1.0) -> list[str]:
    out = []
    for r in radii:
        a = math.radians(half_angle)
        x0, y0 = cx + r * math.cos(-a), cy + r * math.sin(-a)
        x1, y1 = cx + r * math.cos(a), cy + r * math.sin(a)
        out.append(f'<path d="M{x0:.1f} {y0:.1f} A {r} {r} 0 0 1 {x1:.1f} {y1:.1f}" fill="none" '
                   f'stroke="{color}" stroke-width="{width}" opacity="{opacity}"/>')
    return out


# ---------------------------------------------------------------- open waveguide vs horn
def horn_flare() -> str:
    W, H = 760, 330
    b = [markers(NAVY, BLUE, RED, GREEN, BROWN)]
    b.append(f'<line x1="300" y1="16" x2="300" y2="314" stroke="{RULE}" stroke-width="1"/>')
    cy = 170

    # open-ended waveguide
    b.append(text(150, 32, "Open-ended waveguide", NAVY, 21, "700"))
    x0, x1, hh = 30, 170, 28
    b.append(f'<rect x="{x0}" y="{cy - hh}" width="{x1 - x0}" height="{2 * hh}" fill="{SUB}" stroke="{NAVY}" stroke-width="3"/>')
    b.append(arrow(x0 + 14, cy - 8, x1 - 16, cy - 8, BLUE, 3))
    b.append(arrow(x1 - 16, cy + 10, x1 - 58, cy + 10, RED, 1.6))
    b += arcs(x1, cy, (22, 42, 62), 75, GREEN, 2.2)
    b.append(text(100, cy - 50, "in", BLUE, 18, "700"))
    b.append(text(118, cy + 60, "a little reflects", RED, 18, "700"))
    b.append(text(252, cy - 78, "a broad beam", GREEN, 17, "700"))
    b.append(text(252, cy - 58, "spills out", GREEN, 17, "700"))
    b.append(text(150, 290, "a small opening: a few dBi", GRAY, 17))

    # horn
    b.append(text(530, 32, "Horn", NAVY, 21, "700"))
    gx0, gx1, fx1, HA = 330, 410, 620, 108
    b.append(f'<path d="M{gx0} {cy - hh} H{gx1} L{fx1} {cy - HA} V{cy + HA} L{gx1} {cy + hh} H{gx0} Z" '
             f'fill="{SUB}" stroke="{NAVY}" stroke-width="3" stroke-linejoin="round"/>')
    b.append(f'<line x1="{fx1}" y1="{cy - HA}" x2="{fx1}" y2="{cy + HA}" stroke="{SUB}" stroke-width="3"/>')
    apex = gx1 - (fx1 - gx1) * hh / (HA - hh)          # virtual apex of the flare
    for r in (70, 115, 160, 205):
        rr = r + (gx1 - apex)
        half = math.degrees(math.atan((hh + (HA - hh) * r / (fx1 - gx1)) / rr)) * 0.92
        b += arcs(apex, cy, (rr,), half, BLUE, 2.2)
    b += arcs(apex, cy, (fx1 - apex + 36, fx1 - apex + 70), 13, GREEN, 2.6)
    b.append(arrow(gx0 + 12, cy, gx1 + 10, cy, BLUE, 3))
    b.append(arrow(fx1 + 94, cy, fx1 + 128, cy, GREEN, 3))
    b.append(text(fx1 + 70, cy - 102, "the wave", GREEN, 18, "700"))
    b.append(text(fx1 + 70, cy - 80, "flows out", GREEN, 18, "700"))
    b.append(text(530, 290, "a gradual flare to a large opening", GRAY, 17))
    return svg(W, H, "Left: an open-ended waveguide; only a little of the incoming wave reflects, and "
               "the rest spills out of the small opening in a broad, low-gain beam. Right: a horn; the flare lets the wave expand "
               "gradually and flow out through a large opening", b, "l13hf")


# ---------------------------------------------------------------- square wavelengths
def horn_squares() -> str:
    W, H = 640, 350
    b = [markers(NAVY)]
    aw, ah = 200, 150                      # 20 x 15 cm at 1 px per mm
    for cx, lam_px, f, n in ((215, 30, "10 GHz", 33), (500, 15, "20 GHz", 133)):
        x0, y0 = cx - aw / 2, 70
        b.append(text(cx, 50, f, NAVY, 28, "700"))
        b.append(f'<rect x="{x0}" y="{y0}" width="{aw}" height="{ah}" fill="{SUB}" stroke="{NAVY}" stroke-width="2.6"/>')
        k = lam_px
        x = x0 + k
        while x < x0 + aw - 0.5:
            b.append(f'<line x1="{x}" y1="{y0}" x2="{x}" y2="{y0 + ah}" stroke="{BLUE}" stroke-width="1" opacity="0.7"/>')
            x += k
        y = y0 + k
        while y < y0 + ah - 0.5:
            b.append(f'<line x1="{x0}" y1="{y}" x2="{x0 + aw}" y2="{y}" stroke="{BLUE}" stroke-width="1" opacity="0.7"/>')
            y += k
        b.append(f'<rect x="{x0}" y="{y0}" width="{k}" height="{k}" fill="rgba(176,30,36,0.28)" stroke="{RED}" stroke-width="1.6"/>')
        b.append(text(cx, y0 + ah + 36, f"{n} squares", NAVY, 26, "700"))
    b.append(text(105, 88, "one", RED, 19, "700", "end"))
    b.append(text(105, 110, "square", RED, 19, "700", "end"))
    b.append(text(105, 132, "wave-", RED, 19, "700", "end"))
    b.append(text(105, 154, "length", RED, 19, "700", "end"))
    b.append(text(357, 300, "same 20 × 15 cm opening", GRAY, 19))
    b.append(text(357, 334, "4× the squares: 6 dB more gain", RED, 23, "700"))
    return svg(W, H, "The same 20 by 15 centimeter aperture tiled in square wavelengths: about 33 at "
               "10 GHz and about 133 at 20 GHz. Four times as many squares is 6 dB more gain", b, "l13hs")


# ---------------------------------------------------------------- working squares
def horn_working() -> str:
    """The X-band horn's 20 x 15 cm mouth at 10 GHz tiled in square wavelengths
    (33 of them), and the same tiles shaded by what each contributes: field
    strength from the waveguide's cosine across the 20 cm (H-plane) side, and a
    clock hand turned by the phase lag of the optimum horn, 3/8 wavelength at the
    H-plane edges and 1/4 at the E-plane edges. Their aperture efficiency is
    0.51, so about 17 of the 33 squares do the work."""
    W, H = 580, 340
    s = 36                                         # px per wavelength (3 cm)
    nx, ny = 20 / 3, 15 / 3                        # mouth in wavelengths
    aw, ah = nx * s, ny * s
    y0 = 64
    b = [markers(NAVY, RED)]

    def tiles(x0, shaded):
        out = [f'<rect x="{x0}" y="{y0}" width="{aw:.1f}" height="{ah:.1f}" fill="#ffffff" stroke="{NAVY}" stroke-width="2.6"/>']
        # 6 2/3 columns, centered: a third of a column at each side wall, six whole ones between
        cols, left = [1 / 3] + [1.0] * 6 + [1 / 3], 0.0
        for wcol in cols:
            for j in range(int(ny)):
                tx, ty = x0 + left * s, y0 + j * s
                u = (left + wcol / 2) / nx - 0.5       # -1/2 .. 1/2 across the 20 cm side
                v = (j + 0.5) / ny - 0.5               # -1/2 .. 1/2 across the 15 cm side
                if shaded:
                    amp = math.cos(math.pi * u)
                    out.append(f'<rect x="{tx:.1f}" y="{ty:.1f}" width="{wcol * s:.1f}" height="{s}" '
                               f'fill="{BLUE}" fill-opacity="{0.08 + 0.72 * amp:.2f}" stroke="#ffffff" stroke-width="1.5"/>')
                    if wcol < 1:                           # the slivers at the walls: shade only
                        continue
                    lag = 3 / 8 * (2 * u) ** 2 + 1 / 4 * (2 * v) ** 2      # in wavelengths
                    a = 2 * math.pi * lag
                    cx, cy, r = tx + wcol * s / 2, ty + s / 2, 0.36 * s
                    hx, hy = cx + r * math.sin(a), cy - r * math.cos(a)
                    out.append(f'<line x1="{cx:.1f}" y1="{cy:.1f}" x2="{hx:.1f}" y2="{hy:.1f}" stroke="#ffffff" stroke-width="5" stroke-linecap="round"/>')
                    out.append(f'<line x1="{cx:.1f}" y1="{cy:.1f}" x2="{hx:.1f}" y2="{hy:.1f}" stroke="{NAVY}" stroke-width="2.4" stroke-linecap="round"/>')
                    out.append(f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="2.4" fill="{NAVY}"/>')
                else:
                    out.append(f'<rect x="{tx:.1f}" y="{ty:.1f}" width="{wcol * s:.1f}" height="{s}" '
                               f'fill="{SUB}" stroke="{BLUE}" stroke-width="1" stroke-opacity="0.7"/>')
            left += wcol
        out.append(f'<rect x="{x0}" y="{y0}" width="{aw:.1f}" height="{ah:.1f}" fill="none" stroke="{NAVY}" stroke-width="2.6"/>')
        return out

    xl, xr = 14, W - 14 - aw
    b += tiles(xl, False)
    b += tiles(xr, True)
    b.append(text(xl + aw / 2, 40, "33 squares", NAVY, 26, "700"))
    b.append(text(xr + aw / 2, 40, "17 doing the work", RED, 26, "700"))
    mid = (xl + aw + xr) / 2
    b.append(arrow(mid - 22, y0 + ah / 2, mid + 22, y0 + ah / 2, NAVY, 3))
    b.append(text(xl + aw / 2, y0 + ah + 36, "20 × 15 cm, 10 GHz", GRAY, 21))
    b.append(text(xr + aw / 2, y0 + ah + 36, "dim: walls zero the field", GRAY, 21))
    b.append(text(xr + aw / 2, y0 + ah + 64, "turned: edges arrive late", GRAY, 21))
    return svg(W, H, "The X-band horn's 20 by 15 centimeter mouth at 10 GHz tiled in 33 square wavelengths, "
               "and the same tiles shaded by what each contributes: strong in the middle and weak at the "
               "side walls, with a clock hand on each tile turned by its phase lag, upright at the center and "
               "turned most at the corners. About 17 of the 33 squares' worth does the work", b, "l13hw")


# ---------------------------------------------------------------- phase error
def horn_phase() -> str:
    W, H = 720, 340
    b = [markers(NAVY, RED, GRAY)]
    cy = 170
    ax, gx0, gx1, fx1, hh, HA = 70, 150, 230, 520, 26, 118
    apex = gx1 - (fx1 - gx1) * hh / (HA - hh)
    b.append(f'<path d="M{gx0} {cy - hh} H{gx1} L{fx1} {cy - HA} V{cy + HA} L{gx1} {cy + hh} H{gx0} Z" '
             f'fill="{SUB}" stroke="{NAVY}" stroke-width="3" stroke-linejoin="round"/>')
    b.append(f'<line x1="{fx1}" y1="{cy - HA}" x2="{fx1}" y2="{cy + HA}" stroke="{NAVY}" stroke-width="2" stroke-dasharray="6 4"/>')
    # rays from the apex
    for yy in (cy - HA, cy + HA):
        b.append(f'<line x1="{apex:.1f}" y1="{cy}" x2="{fx1}" y2="{yy}" stroke="{GRAY}" stroke-width="1.2" stroke-dasharray="4 4"/>')
    b.append(f'<line x1="{apex:.1f}" y1="{cy}" x2="{fx1 + 10}" y2="{cy}" stroke="{GRAY}" stroke-width="1.2" stroke-dasharray="4 4"/>')
    b.append(f'<circle cx="{apex:.1f}" cy="{cy}" r="4.5" fill="{GRAY}"/>')
    b.append(text(apex, cy + 58, "virtual apex", GRAY, 16, anchor="middle"))
    b.append(f'<line x1="{apex:.1f}" y1="{cy + 6}" x2="{apex:.1f}" y2="{cy + 42}" stroke="{GRAY}" stroke-width="1"/>')
    # the spherical front through the aperture center
    R = fx1 - apex
    half = math.degrees(math.asin(HA / R))
    b += arcs(apex, cy, (R,), half, RED, 3.2)
    # the lag at the edge
    xe = apex + R * math.cos(math.radians(half))
    b.append(dim(xe, cy - HA - 14, fx1, cy - HA - 14, RED, 1.6))
    b.append(text((xe + fx1) / 2, cy - HA - 26, "edge lags", RED, 17, "700"))
    b.append(text(fx1 - 14, cy + HA + 30, "flat aperture", NAVY, 17, "700", "end"))
    b.append(text(xe - 16, cy + 60, "spherical", RED, 17, "700", "end"))
    b.append(text(xe - 16, cy + 80, "front", RED, 17, "700", "end"))
    # phase across the aperture: a parabola
    px = 610
    b.append(f'<line x1="{px}" y1="{cy - HA}" x2="{px}" y2="{cy + HA}" stroke="{GRAY}" stroke-width="1.2"/>')
    pts = " ".join(f"{px + 70 * (t * t):.1f},{cy + HA * t:.1f}" for t in [i / 40 - 1 for i in range(81)])
    b.append(f'<polyline points="{pts}" fill="none" stroke="{RED}" stroke-width="3"/>')
    b.append(text(px + 36, cy - HA - 26, "phase lag", RED, 17, "700"))
    b.append(text(px + 36, cy - HA - 8, "across it", RED, 17, "700"))
    b.append(text(px + 8, cy + 6, "0 at center", GRAY, 15, anchor="start"))
    return svg(W, H, "Side view of a horn: the wave leaves the apex on a spherical front, which reaches "
               "the flat aperture first at the center and later at the edges; the phase lag across the "
               "aperture is a parabola, zero at the center and largest at the edges", b, "l13hp")


# ---------------------------------------------------------------- optimum horn
def rel_gain(D: float, R: float, taper: bool) -> tuple[float, float]:
    """Relative gain of a horn of slant length R (in wavelengths) and aperture
    width D (in wavelengths) in one plane: proportional to D times the phase
    efficiency of a quadratic phase error whose edge value is s = D^2/(8R)."""
    s = D * D / (8 * R)
    n = 800
    F = F0 = 0
    for i in range(n + 1):
        u = -0.5 + i / n
        w = 0.5 if i in (0, n) else 1.0
        a = math.cos(math.pi * u) if taper else 1.0
        F += w * a * cmath.exp(-1j * 2 * math.pi * s * (2 * u) ** 2)
        F0 += w * a
    return D * abs(F / F0) ** 2, s


def horn_optimum() -> str:
    Rl = 10.0                                         # slant length, wavelengths
    Ds = [1 + 17 * i / 340 for i in range(341)]
    E = [rel_gain(D, Rl, False)[0] for D in Ds]
    Hc = [rel_gain(D, Rl, True)[0] for D in Ds]
    ref = max(E)
    db = lambda v: 10 * math.log10(v / ref)
    iE, iH = E.index(max(E)), Hc.index(max(Hc))
    sE, sH = rel_gain(Ds[iE], Rl, False)[1], rel_gain(Ds[iH], Rl, True)[1]

    W, H = 600, 350
    X0, X1, Y0, Y1 = 80, 570, 40, 270
    dmin, dmax, ymin, ymax = 1, 18, -10, 8
    px = lambda d: X0 + (d - dmin) / (dmax - dmin) * (X1 - X0)
    py = lambda y: Y1 - (y - ymin) / (ymax - ymin) * (Y1 - Y0)
    b = [markers(NAVY, RED, GREEN)]
    for y in range(ymin, ymax + 1, 2):
        b.append(f'<line x1="{X0}" y1="{py(y):.1f}" x2="{X1}" y2="{py(y):.1f}" stroke="{RULE}" stroke-width="1"/>')
        b.append(text(X0 - 8, py(y) + 6, str(y), GRAY, 16, anchor="end"))
    for d in range(2, 19, 4):
        b.append(text(px(d), Y1 + 24, str(d), GRAY, 16))
    b.append(f'<rect x="{X0}" y="{Y0}" width="{X1 - X0}" height="{Y1 - Y0}" fill="none" stroke="{SUB_EDGE}"/>')

    def line(vals, color, width, dash=""):
        pts = " ".join(f"{px(d):.1f},{py(max(ymin, min(ymax, db(v)))):.1f}" for d, v in zip(Ds, vals))
        d = f' stroke-dasharray="{dash}"' if dash else ""
        return f'<polyline points="{pts}" fill="none" stroke="{color}" stroke-width="{width}"{d}/>'

    b.append(line(Ds, GRAY, 2.2, "7 5"))                                   # no phase error: gain grows with D
    b.append(line(E, NAVY, 3))
    b.append(line(Hc, GREEN, 3))
    for i, s, col, lab, dy in ((iE, sE, NAVY, "E-plane peak: edge lags λ/4", -16),
                               (iH, sH, GREEN, "H-plane peak: edge lags 3λ/8", -16)):
        x, y = px(Ds[i]), py(db([E, Hc][col == GREEN][i]))
        b.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="6" fill="{col}"/>')
    b.append(f'<line x1="{px(Ds[iE]) - 5:.1f}" y1="{py(db(E[iE])) - 4:.1f}" x2="{px(2.6):.1f}" y2="{py(4.1):.1f}" stroke="{NAVY}" stroke-width="1.2"/>')
    b.append(text(px(1.3), py(4.6), "edge lags λ/4", NAVY, 17, "700", "start"))
    b.append(f'<line x1="{px(Ds[iH]) + 6:.1f}" y1="{py(db(Hc[iH])) - 3:.1f}" x2="{px(9.2):.1f}" y2="{py(2.0):.1f}" stroke="{GREEN}" stroke-width="1.2"/>')
    b.append(text(px(9.3), py(2.0) + 1, "edge lags 3λ/8", GREEN, 17, "700", "start"))
    b.append(text(px(14.6), py(6.6), "no phase error", GRAY, 16, "700"))
    b.append(text(px(8.5), py(-8.9), "E-plane", NAVY, 17, "700"))
    b.append(text(px(15.5), py(-2.3), "H-plane", GREEN, 17, "700"))
    b.append(text((X0 + X1) / 2, Y1 + 52, "aperture width, wavelengths (horn length fixed)", GRAY, 17))
    b.append(text(24, (Y0 + Y1) / 2, "relative gain (dB)", GRAY, 17, rot=-90))
    s = svg(W, H, "Relative gain of a horn of fixed length against aperture width. Without phase error "
            "the gain keeps rising; with it, the gain peaks and falls. The peak, the optimum horn, "
            "comes where the edge lags by a quarter wavelength for the uniform E-plane field and by "
            "three eighths of a wavelength for the tapered H-plane field", b, "l13ho")
    return s, sE, sH



# ---------------------------------------------------------------- the optimum, in three horns
def horn_three() -> str:
    """Three horns with the same flare length (10 wavelengths, apex to mouth)
    and mouths that are too narrow, optimum, and too wide. Under each, the
    mouth split into strips whose contributions add head to tail (one half of
    the mouth; the other half is its mirror), and a bar for the gain."""
    Rl = 10.0
    cases = (("Narrow mouth", 0.0625, "edge lags λ/16"),
             ("Optimum", 0.25, "edge lags λ/4"),
             ("Too wide", 0.75, "edge lags 3λ/4"))
    gains = [rel_gain(math.sqrt(8 * Rl * sl), Rl, False)[0] for _, sl, _ in cases]
    gbest = max(gains)
    W, H = 900, 480
    px_per_lam = 15.0
    b = [markers(NAVY, RED, GRAY, GREEN)]
    for x in (300, 600):
        b.append(f'<line x1="{x}" y1="16" x2="{x}" y2="{H - 16}" stroke="{RULE}" stroke-width="1"/>')
    base_step = None
    for (title, sl, lag), g, cx in zip(cases, gains, (150, 450, 750)):
        D = math.sqrt(8 * Rl * sl)                       # mouth width, wavelengths
        b.append(text(cx, 36, title, NAVY, 27, "700"))
        # --- horn, side view, mouth on the right; apex 10 wavelengths behind it
        cy, mx = 128, cx + 110
        R = Rl * px_per_lam
        ax = mx - R
        hm = D / 2 * px_per_lam
        ht = 8
        tx = ax + R * ht / hm
        b.append(f'<path d="M{tx - 28:.1f} {cy - ht} H{tx:.1f} L{mx:.1f} {cy - hm:.1f} V{cy + hm:.1f} '
                 f'L{tx:.1f} {cy + ht} H{tx - 28:.1f} Z" fill="{SUB}" stroke="{NAVY}" stroke-width="2.4" stroke-linejoin="round"/>')
        half = math.degrees(math.asin(min(0.999, hm / R)))
        b += arcs(ax, cy, (R,), half, RED, 2.4)
        b.append(f'<circle cx="{ax:.1f}" cy="{cy}" r="3.5" fill="{GRAY}"/>')
        if sl < 0.2:
            b.append(text(ax, cy - 16, "apex", GRAY, 19))
        dy = cy + 78
        b.append(dim(ax, dy, mx, dy, GRAY, 1.3))
        b.append(text((ax + mx) / 2, dy + 24, "same flare length", GRAY, 19))
        b.append(text(cx, dy + 56, lag, RED, 23, "700"))
        # --- phasor chain for one half of the mouth, strips of fixed physical width
        n = max(2, round(D / 2 / 0.37))
        step = 22
        ox, oy = cx - 100, 386
        x, y = ox, oy
        b.append(f'<circle cx="{ox}" cy="{oy}" r="3" fill="{NAVY}"/>')
        for k in range(n):
            u = (k + 0.5) / n                            # position across the half mouth, 0..1
            phi = 2 * math.pi * sl * u * u               # lag of this strip, in radians
            nx, ny = x + step * math.cos(phi), y - step * math.sin(phi)
            b.append(arrow(x, y, nx, ny, NAVY, 2.2))
            x, y = nx, ny
        b.append(arrow(ox, oy, x, y, RED, 3.2))
        # --- gain bar, linear in gain, relative to the best
        by, bl = 408, 190 * g / gbest
        b.append(f'<rect x="{cx - 95}" y="{by}" width="{bl:.1f}" height="22" rx="3" fill="{GREEN if g == gbest else BLUE}" opacity="0.85"/>')
        b.append(f'<rect x="{cx - 95}" y="{by}" width="190" height="22" rx="3" fill="none" stroke="{SUB_EDGE}"/>')
        db = 10 * math.log10(g / gbest)
        b.append(text(cx, by + 56, "highest gain" if g == gbest else f"{-db:.1f} dB lower", GREEN if g == gbest else NAVY, 24, "700"))
    return svg(W, H, "Three horns with the same flare length and mouths too narrow, optimum, and too "
               "wide. Their edges lag the center by a sixteenth, a quarter, and three quarters of a "
               "wavelength. Under each, the strips of the mouth add as arrows head to tail, each turned "
               "by its lag: the narrow mouth has few arrows in a straight line, the optimum has more "
               "arrows that curve a little, and the too-wide mouth has so many that the chain curls back "
               "and the total shrinks. The optimum has the highest gain; the narrow mouth is about 2 dB "
               "lower and the wide one about 6 dB lower", b, "l13h3")

# ---------------------------------------------------------------- gain comparison
def mini_horn(x, y, s=1.0, facing=-1, color=NAVY) -> str:
    """A small horn at (x, y), mouth facing left (facing=-1) or right."""
    L, h0, h1, g = 46 * s, 8 * s, 26 * s, 18 * s
    m = x + facing * 0                       # mouth x
    t = x - facing * L                       # throat x
    return (f'<path d="M{m} {y - h1} L{t} {y - h0} H{t - facing * g} V{y + h0} H{t} L{m} {y + h1} Z" '
            f'fill="{SUB}" stroke="{color}" stroke-width="2.4" stroke-linejoin="round"/>')


def mini_dipole(x, y, color=NAVY) -> str:
    return (f'<line x1="{x}" y1="{y - 34}" x2="{x}" y2="{y - 4}" stroke="{color}" stroke-width="5" stroke-linecap="round"/>'
            f'<line x1="{x}" y1="{y + 4}" x2="{x}" y2="{y + 34}" stroke="{color}" stroke-width="5" stroke-linecap="round"/>'
            f'<circle cx="{x}" cy="{y}" r="4" fill="#fff" stroke="{BROWN}" stroke-width="2"/>')


def horn_comparison() -> str:
    W, H = 760, 360
    b = [markers(NAVY, GREEN, GRAY)]
    tx, ty = 110, 180
    b.append(f'<line x1="{tx}" y1="{ty + 30}" x2="{tx}" y2="{ty + 110}" stroke="{GRAY}" stroke-width="5"/>')
    b.append(mini_horn(tx + 24, ty, 1.1, facing=1))
    b.append(text(tx, ty - 50, "transmit", NAVY, 18, "700"))
    b.append(text(tx, ty - 30, "fixed power", GRAY, 16))
    for yy in (100, 262):
        b.append(f'<line x1="{tx + 40}" y1="{ty}" x2="440" y2="{yy}" stroke="{GREEN}" stroke-width="1.6" stroke-dasharray="7 5"/>')
    b.append(text(292, ty + 4, "same range, same spot", GREEN, 16, "700"))
    rows = ((100, "1  standard-gain horn", "known: 15.0 dBi", "reads −40.0 dBm", "horn"),
            (262, "2  antenna under test", "unknown", "reads −52.9 dBm", "dipole"))
    for yy, title, known, reads, kind in rows:
        b.append(f'<rect x="448" y="{yy - 62}" width="296" height="124" rx="8" fill="#fff" stroke="{SUB_EDGE}" stroke-width="1.6"/>')
        if kind == "horn":
            b.append(mini_horn(484, yy + 6, 1.0, facing=-1))
        else:
            b.append(mini_dipole(492, yy + 6))
        b.append(text(470, yy - 36, title, NAVY, 18, "700", "start"))
        b.append(text(572, yy + 2, known, GRAY, 16, anchor="start"))
        b.append(text(572, yy + 30, reads, NAVY, 17, "700", "start"))
    b.append(text(380, 350, "12.9 dB less power, so 12.9 dB less gain: 2.1 dBi", NAVY, 19, "700"))
    return svg(W, H, "The gain-comparison measurement. A transmitter sends fixed power across the "
               "range. First the standard-gain horn, of known gain 15.0 dBi, sits at the receive spot "
               "and reads minus 40.0 dBm; then the antenna under test sits in the same spot and reads "
               "minus 52.9 dBm. 12.9 dB less power means 12.9 dB less gain, so the antenna under test "
               "is 2.1 dBi", b, "l13hc")


# ---------------------------------------------------------------- slots in service
def slot_service() -> str:
    W, H = 760, 330
    b = [markers(NAVY, BLUE, RED, GREEN)]
    b.append(f'<line x1="330" y1="16" x2="330" y2="314" stroke="{RULE}" stroke-width="1"/>')

    # cavity-backed slot, side view
    b.append(text(165, 32, "Cavity-backed slot", NAVY, 21, "700"))
    b.append(text(165, 54, "side view", GRAY, 16))
    sy, sx = 190, 165
    b.append(f'<line x1="30" y1="{sy}" x2="{sx - 16}" y2="{sy}" stroke="{NAVY}" stroke-width="6"/>')
    b.append(f'<line x1="{sx + 16}" y1="{sy}" x2="300" y2="{sy}" stroke="{NAVY}" stroke-width="6"/>')
    b.append(f'<path d="M{sx - 60} {sy + 3} V{sy + 70} H{sx + 60} V{sy + 3}" fill="{SUB}" stroke="{NAVY}" stroke-width="3"/>')
    b += [s for s in (
        f'<path d="M{sx - 34} {sy - 20} A 34 34 0 0 1 {sx + 34} {sy - 20}" fill="none" stroke="{GREEN}" stroke-width="2.4"/>',
        f'<path d="M{sx - 62} {sy - 34} A 66 66 0 0 1 {sx + 62} {sy - 34}" fill="none" stroke="{GREEN}" stroke-width="2.4"/>',
        f'<path d="M{sx - 90} {sy - 44} A 98 98 0 0 1 {sx + 90} {sy - 44}" fill="none" stroke="{GREEN}" stroke-width="2.4"/>')]
    b.append(text(58, sy - 12, "skin", NAVY, 17, "700", "start"))
    b.append(text(sx, sy + 46, "cavity", NAVY, 17, "700"))
    b.append(text(sx, 84, "radiates outward only", GREEN, 17, "700"))
    b.append(text(sx, sy + 110, "flush, one-sided, narrowband", GRAY, 16))

    # waveguide slot array, top view of the broad wall
    b.append(text(545, 32, "Waveguide slot array", NAVY, 21, "700"))
    b.append(text(545, 54, "top view of the broad wall", GRAY, 16))
    gx0, gx1, gy0, gy1 = 360, 740, 120, 220
    gc = (gy0 + gy1) / 2
    b.append(f'<rect x="{gx0}" y="{gy0}" width="{gx1 - gx0}" height="{gy1 - gy0}" fill="{METAL}" stroke="{NAVY}" stroke-width="2.6"/>')
    b.append(f'<line x1="{gx0}" y1="{gc}" x2="{gx1}" y2="{gc}" stroke="{GRAY}" stroke-width="1.2" stroke-dasharray="6 4"/>')
    offs = [6, 12, 17, 20, 20, 17, 12, 6]      # larger offset near the middle: the taper
    for i, o in enumerate(offs):
        x = gx0 + 36 + i * 44
        yc = gc + (o if i % 2 else -o)
        b.append(f'<rect x="{x - 15}" y="{yc - 3.5}" width="30" height="7" rx="3.5" fill="#fff" stroke="{NAVY}" stroke-width="1.6"/>')
    b.append(arrow(gx0 - 30, gc, gx0 - 4, gc, BLUE, 3))
    b.append(text(gx0 - 2, gy0 - 14, "wave in", BLUE, 16, "700", "start"))
    b.append(text(gx1 - 4, gy0 - 14, "centerline dashed", GRAY, 15, anchor="end"))
    b.append(text(545, gy1 + 34, "offset from the centerline", NAVY, 17, "700"))
    b.append(text(545, gy1 + 56, "sets how much power each slot takes", NAVY, 17, "700"))
    b.append(text(545, gy1 + 86, "larger in the middle: a tapered aperture", GRAY, 16))
    return svg(W, H, "Left: a cavity-backed slot in an aircraft skin, side view; the cavity behind the "
               "slot makes it radiate outward only. Right: a waveguide slot array, top view of the broad "
               "wall; slots alternate sides of the centerline, and their offset, larger in the middle, "
               "sets how much power each takes, so the wall carries a tapered aperture", b, "l13ss")


def main() -> None:
    opt, sE, sH = horn_optimum()
    figs = {
        "L13-horn-flare.svg": horn_flare(),
        "L13-horn-squares.svg": horn_squares(),
        "L13-horn-working.svg": horn_working(),
        "L13-horn-phase.svg": horn_phase(),
        "L13-horn-optimum.svg": opt,
        "L13-horn-comparison.svg": horn_comparison(),
        "L13-slot-service.svg": slot_service(),
        "L13-horn-three.svg": horn_three(),
    }
    for d in OUTS:
        for name, s in figs.items():
            p = d / name
            p.write_text(s)
            print("wrote", p.relative_to(ROOT))
    print(f"optimum edge phase error: E-plane {sE:.3f} wavelengths, H-plane {sH:.3f} wavelengths")


if __name__ == "__main__":
    main()
