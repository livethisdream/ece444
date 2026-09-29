#!/usr/bin/env python3
"""Generate the L13 microstrip-patch figures as inline SVG.

L13:
  - L13-patch-standing-wave : side view. The patch and the ground plane are a
                              short microstrip line, open at both ends; the
                              wave reflects off each end and the field between
                              the conductors is a half-wave standing wave. It
                              leaks out only at the two open ends.
  - L13-patch-edges         : top view, all four edges with their fringing
                              field. Uniform along the two ends (they add);
                              reversing halfway along the two sides (they
                              cancel).
  - L13-patch-feeds         : the three feeds -- inset line (top view), coaxial
                              probe and aperture coupling (side views).
  - L13-patch-feed-position : input resistance against feed position for the
                              lesson's 2.45 GHz FR-4 design, computed below.

Schematics are not to scale. No formulas (deck figure rule), so the lesson-page
copies are the same files.

    python scripts/graphics/l13_patch_figures.py
    -> writes book/extras/slides/fig/L13-patch-*.svg
              book/extras/viz/img/L13-patch-*.svg
"""

from __future__ import annotations
import math
from pathlib import Path
from svg_font_stack import apply_font_stack

NAVY, BLUE, RED, GRAY, BROWN = "#004a85", "#0067b9", "#b01e24", "#5a5a5a", "#8a5a00"
RULE, SUB, SUB_EDGE, COPPER = "#dbe3ee", "#eaf2f9", "#b9d2e5", "#c9822b"
ROOT = Path(__file__).resolve().parents[2]
OUTS = [ROOT / "book/extras/slides/fig", ROOT / "book/extras/viz/img"]

# The lesson's worked example: 2.45 GHz on FR-4, h = 1.6 mm.
F0, W_MM, L_MM = 2.45e9, 37.3, 28.8


def text(x, y, s, color=GRAY, size=14, weight=None, anchor="middle", italic=False, rot=None) -> str:
    w = f' font-weight="{weight}"' if weight else ""
    i = ' font-style="italic"' if italic else ""
    r = f' transform="rotate({rot} {x} {y})"' if rot is not None else ""
    return (f'<text x="{x:.1f}" y="{y:.1f}" fill="{color}" font-size="{size}"{w}{i} '
            f'text-anchor="{anchor}"{r}>{s}</text>')


def arrow(x1, y1, x2, y2, color, width=2.4, marker="ah") -> str:
    return (f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="{color}" '
            f'stroke-width="{width}" marker-end="url(#{marker}-{color[1:]})"/>')


def markers(*colors) -> str:
    m = [f'<marker id="ah-{c[1:]}" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="5" '
         f'markerHeight="5" orient="auto-start-reverse"><path d="M0 0 L10 5 L0 10 z" fill="{c}"/></marker>'
         for c in colors]
    return "<defs>" + "".join(m) + "</defs>"


def svg(w, h, label, body, prefix) -> str:
    """Marker ids are unique per figure: a deck inlines every figure into one
    document, and a repeated id resolves to the first copy, which may sit on a
    hidden slide, and then the arrowheads vanish."""
    head = (f'<svg viewBox="0 0 {w} {h}" xmlns="http://www.w3.org/2000/svg" role="img" '
            f'aria-label="{label}">')
    out = "\n".join([head, *body, "</svg>"])
    out = out.replace('id="ah-', f'id="{prefix}-ah-').replace('url(#ah-', f'url(#{prefix}-ah-')
    return apply_font_stack(out) + "\n"


def ground(x1, x2, y) -> list[str]:
    out = [f'<line x1="{x1}" y1="{y}" x2="{x2}" y2="{y}" stroke="{NAVY}" stroke-width="5"/>']
    for x in range(x1 + 6, x2, 14):
        out.append(f'<line x1="{x}" y1="{y + 3}" x2="{x - 9}" y2="{y + 13}" stroke="{SUB_EDGE}" stroke-width="1.2"/>')
    return out


# ---------------------------------------------------------------- standing wave
def standing_wave() -> str:
    W, H = 560, 276
    gy, ty = 212, 162           # ground and patch heights
    x0, x1 = 130, 430           # patch ends
    b = [markers(NAVY, BLUE, RED, BROWN)]
    b.append(f'<rect x="60" y="{ty}" width="440" height="{gy - ty}" fill="{SUB}" stroke="{SUB_EDGE}" stroke-width="1"/>')
    b += ground(60, 500, gy)
    b.append(f'<line x1="{x0}" y1="{ty}" x2="{x1}" y2="{ty}" stroke="{NAVY}" stroke-width="6" stroke-linecap="round"/>')
    # field between the conductors: a half-wave standing wave, cos(pi x / L)
    n = 11
    for k in range(n):
        xf = (k + 0.5) / n
        a = math.cos(math.pi * xf)
        x = x0 + xf * (x1 - x0)
        if abs(a) < 0.12:
            b.append(f'<circle cx="{x:.1f}" cy="{(ty + gy) / 2:.1f}" r="2.5" fill="{BLUE}"/>')
            continue
        half = 21 * abs(a)
        mid = (ty + gy) / 2
        ya, yb = (mid - half, mid + half) if a > 0 else (mid + half, mid - half)
        b.append(arrow(x, ya, x, yb, BLUE, 2.2 + 0.8 * abs(a)))
    # fringing at the two open ends
    for xe, s in ((x0, -1), (x1, 1)):
        b.append(f'<path d="M{xe} {ty + 2} C {xe + s * 34} {ty - 6}, {xe + s * 40} {gy - 8}, {xe + s * 34} {gy - 2}" '
                 f'fill="none" stroke="{RED}" stroke-width="3"/>')
        b.append(f'<path d="M{xe} {ty + 2} C {xe + s * 56} {ty - 22}, {xe + s * 66} {gy - 6}, {xe + s * 58} {gy - 2}" '
                 f'fill="none" stroke="{RED}" stroke-width="2" opacity="0.55"/>')
    # the traveling waves that make the standing wave
    b.append(arrow(x0 + 40, 80, x1 - 40, 80, BROWN, 2.4))
    b.append(text((x0 + x1) / 2, 68, "wave travels along the patch", BROWN, 18))
    b.append(arrow(x1 - 40, 100, x0 + 40, 100, BROWN, 2.4))
    b.append(text((x0 + x1) / 2, 126, "and reflects from each open end", BROWN, 18))
    b.append(text(x0, 34, "open end", NAVY, 19, "700"))
    b.append(text(x1, 34, "open end", NAVY, 19, "700"))
    for xe in (x0, x1):
        b.append(f'<line x1="{xe}" y1="42" x2="{xe}" y2="{ty - 10}" stroke="{NAVY}" stroke-width="1" stroke-dasharray="4 3"/>')
    b.append(text(76, 160, "fringing", RED, 18, "700"))
    b.append(text(484, 160, "fringing", RED, 18, "700"))
    b.append(text(280, gy + 40, "zero at the center", BLUE, 18, "700"))
    b.append(f'<line x1="280" y1="{gy + 22}" x2="280" y2="{(ty + gy) / 2 + 6:.0f}" stroke="{BLUE}" stroke-width="1.2" stroke-dasharray="3 3"/>')
    b.append(text(470, gy + 40, "ground plane", NAVY, 18, "700"))
    b.append(text(280, ty - 10, "patch", NAVY, 18, "700"))
    return svg(W, H, "Side view of a microstrip patch over a ground plane: a wave travels along the patch "
               "and reflects from each open end, so the field between patch and ground is a half-wave "
               "standing wave, largest at the ends and zero at the center, and it fringes out past the "
               "two open ends", b, "l13sw")


# ---------------------------------------------------------------- four edges
def edges() -> str:
    W, H = 560, 384
    px0, px1, py0, py1 = 170, 390, 80, 260     # W across, L down
    b = [markers(NAVY, RED, GRAY)]
    b.append(f'<rect x="{px0}" y="{py0}" width="{px1 - px0}" height="{py1 - py0}" '
             f'fill="rgba(0,103,185,0.12)" stroke="{NAVY}" stroke-width="2.4"/>')
    # radiating ends: uniform field, same direction at both ends
    for k in range(6):
        x = px0 + 22 + k * (px1 - px0 - 44) / 5
        b.append(arrow(x, py0 - 4, x, py0 - 30, RED, 2.6))
        b.append(arrow(x, py1 + 30, x, py1 + 4, RED, 2.6))
    b.append(f'<line x1="{px0}" y1="{py0}" x2="{px1}" y2="{py0}" stroke="{RED}" stroke-width="5"/>')
    b.append(f'<line x1="{px0}" y1="{py1}" x2="{px1}" y2="{py1}" stroke="{RED}" stroke-width="5"/>')
    # sides: field follows cos(pi y / L), so it reverses halfway along
    n = 7
    for k in range(n):
        yf = (k + 0.5) / n
        a = math.cos(math.pi * yf)
        y = py0 + yf * (py1 - py0)
        if abs(a) < 0.15:
            for xe in (px0, px1):
                b.append(f'<circle cx="{xe + (-10 if xe == px0 else 10)}" cy="{y:.1f}" r="2.2" fill="{GRAY}"/>')
            continue
        ln = 26 * abs(a)
        for xe, out in ((px0, -1), (px1, 1)):
            s = out if a > 0 else -out
            xa, xb = (xe + out * 4, xe + out * 4 + s * ln) if s == out else (xe + out * (4 + ln), xe + out * 4)
            b.append(arrow(xa, y, xb, y, GRAY, 2.0))
    b.append(text((px0 + px1) / 2, py0 - 42, "end: uniform field", RED, 19, "700"))
    b.append(text((px0 + px1) / 2, py1 + 54, "end: same direction, adds", RED, 19, "700"))
    b.append(text(116, (py0 + py1) / 2, "side: reverses halfway", GRAY, 18, rot=-90))
    b.append(text(444, (py0 + py1) / 2, "side: halves cancel", GRAY, 18, rot=90))
    b.append(text((px0 + px1) / 2, (py0 + py1) / 2 - 4, "patch", NAVY, 20, "700"))
    b.append(text((px0 + px1) / 2, (py0 + py1) / 2 + 20, "top view", GRAY, 16))
    # dimensions
    b.append(f'<line x1="{px1 + 82}" y1="{py0}" x2="{px1 + 82}" y2="{py1}" stroke="{NAVY}" stroke-width="1.6" '
             f'marker-start="url(#ah-{NAVY[1:]})" marker-end="url(#ah-{NAVY[1:]})"/>')
    b.append(text(px1 + 96, (py0 + py1) / 2 + 8, "L", NAVY, 24, "700", "start", True))
    wy = py1 + 76
    b.append(f'<line x1="{px0}" y1="{wy}" x2="{px1}" y2="{wy}" stroke="{NAVY}" stroke-width="1.6" '
             f'marker-start="url(#ah-{NAVY[1:]})" marker-end="url(#ah-{NAVY[1:]})"/>')
    b.append(text((px0 + px1) / 2, wy + 28, "W", NAVY, 24, "700", italic=True))
    return svg(W, H, "Top view of a rectangular patch with the fringing field drawn on all four edges: "
               "along the two ends of width W the field is uniform and points the same way at both, so "
               "they radiate and add; along the two sides of length L the field reverses halfway, so each "
               "side's contributions cancel", b, "l13ed")


# ---------------------------------------------------------------- three feeds
def feeds() -> str:
    W, H = 870, 290
    b = [markers(NAVY, RED, GRAY)]
    for x in (290, 580):
        b.append(f'<line x1="{x}" y1="16" x2="{x}" y2="284" stroke="{RULE}" stroke-width="1"/>')
    titles = ("Inset line", "Coaxial probe", "Aperture coupling")
    subs = ("top view", "side view", "side view")
    for cx, t, s in zip((145, 435, 725), titles, subs):
        b.append(text(cx, 36, t, NAVY, 22, "700"))
        b.append(text(cx, 60, s, GRAY, 17))

    # (a) inset: top view
    x0, x1, y0, y1 = 60, 230, 84, 204
    nw, nd, lw = 16, 52, 14                    # notch half-gap, inset depth, line width
    cx = (x0 + x1) / 2
    b.append(f'<rect x="30" y="70" width="230" height="200" rx="4" fill="{SUB}" stroke="{SUB_EDGE}"/>')
    b.append(f'<path d="M{x0} {y0} H{x1} V{y1} H{cx + lw / 2 + nw} V{y1 - nd} H{cx - lw / 2 - nw} V{y1} H{x0} Z" '
             f'fill="rgba(0,103,185,0.14)" stroke="{NAVY}" stroke-width="2.2"/>')
    b.append(f'<rect x="{cx - lw / 2}" y="{y1 - nd}" width="{lw}" height="{270 - (y1 - nd)}" fill="{BLUE}"/>')
    b.append(f'<circle cx="{cx}" cy="{y1 - nd}" r="5" fill="{RED}"/>')
    b.append(f'<line x1="{x1 + 14}" y1="{y1}" x2="{x1 + 14}" y2="{y1 - nd}" stroke="{NAVY}" stroke-width="1.4" '
             f'marker-start="url(#ah-{NAVY[1:]})" marker-end="url(#ah-{NAVY[1:]})"/>')
    b.append(text(x1 + 8, y1 - nd - 10, "inset", NAVY, 18, "700", "end"))
    b.append(text(cx - 16, 252, "feed line", BLUE, 18, "700", "end"))

    # (b) coaxial probe: side view
    ox = 290
    gy, ty = 196, 150
    b.append(f'<rect x="{ox + 30}" y="{ty}" width="230" height="{gy - ty}" fill="{SUB}" stroke="{SUB_EDGE}"/>')
    b += ground(ox + 30, ox + 260, gy)
    b.append(f'<line x1="{ox + 60}" y1="{ty}" x2="{ox + 230}" y2="{ty}" stroke="{NAVY}" stroke-width="6" stroke-linecap="round"/>')
    px = ox + 110
    b.append(f'<rect x="{px - 14}" y="{gy + 3}" width="28" height="{278 - gy}" fill="{GRAY}" opacity="0.35"/>')
    b.append(f'<rect x="{px - 7}" y="{gy + 3}" width="14" height="{278 - gy}" fill="#ffffff"/>')
    b.append(f'<line x1="{px}" y1="{ty}" x2="{px}" y2="278" stroke="{COPPER}" stroke-width="4"/>')
    b.append(f'<circle cx="{px}" cy="{ty}" r="5" fill="{RED}"/>')
    b.append(text(ox + 145, ty - 16, "patch", NAVY, 18, "700"))
    b.append(text(px + 24, 228, "pin through", COPPER, 18, "700", "start"))
    b.append(text(px + 24, 250, "the board", COPPER, 18, "700", "start"))
    b.append(text(px + 24, 276, "coax below", GRAY, 17, anchor="start"))

    # (c) aperture coupling: side view, two boards
    ox = 580
    ty, g, by = 118, 168, 218                   # patch, ground, bottom of lower board
    b.append(f'<rect x="{ox + 30}" y="{ty}" width="230" height="{g - ty}" fill="{SUB}" stroke="{SUB_EDGE}"/>')
    b.append(f'<rect x="{ox + 30}" y="{g}" width="230" height="{by - g}" fill="#f4f0e6" stroke="#dccfb2"/>')
    b.append(f'<line x1="{ox + 60}" y1="{ty}" x2="{ox + 230}" y2="{ty}" stroke="{NAVY}" stroke-width="6" stroke-linecap="round"/>')
    sx = ox + 145
    b.append(f'<line x1="{ox + 30}" y1="{g}" x2="{sx - 12}" y2="{g}" stroke="{NAVY}" stroke-width="5"/>')
    b.append(f'<line x1="{sx + 12}" y1="{g}" x2="{ox + 260}" y2="{g}" stroke="{NAVY}" stroke-width="5"/>')
    b.append(f'<line x1="{ox + 70}" y1="{by}" x2="{ox + 200}" y2="{by}" stroke="{BLUE}" stroke-width="6" stroke-linecap="round"/>')
    b.append(arrow(sx, by - 6, sx, g + 4, RED, 2.2))
    b.append(arrow(sx, g - 4, sx, ty + 8, RED, 2.2))
    b.append(text(ox + 145, ty - 16, "patch", NAVY, 18, "700"))
    b.append(text(ox + 34, g - 8, "ground", NAVY, 17, "700", "start"))
    b.append(text(sx + 14, g - 8, "slot", RED, 17, "700", "start"))
    b.append(text(ox + 145, by + 26, "feed line on a", BLUE, 17, "700"))
    b.append(text(ox + 145, by + 48, "second board", BLUE, 17, "700"))
    return svg(W, H, "Three ways to feed a patch: an inset microstrip line that reaches into the patch "
               "through two notches; a coaxial probe whose center pin comes up through the ground plane "
               "and the substrate to touch the patch; and aperture coupling, where a feed line on a second "
               "board below the ground plane couples to the patch through a slot in the ground plane", b, "l13fd")


# ---------------------------------------------------------------- feed position
def edge_resistance(f=F0, w_mm=W_MM, l_mm=L_MM, n=20001) -> float:
    """Transmission-line model edge resistance, 1 / (2 (G1 + G12)), lossless."""
    k0 = 2 * math.pi * f / 3e8
    w, l = w_mm * 1e-3, l_mm * 1e-3

    def j0(z, m=400):
        s = 0.0
        for i in range(m + 1):
            p = math.pi * i / m
            c = 0.5 if i in (0, m) else 1.0
            s += c * math.cos(z * math.sin(p))
        return s / m

    g1 = g12 = 0.0
    dt = math.pi / (n - 1)
    for i in range(1, n - 1):
        t = i * dt
        ct = math.cos(t)
        if abs(ct) < 1e-9:
            base = (k0 * w / 2) ** 2 * math.sin(t) ** 3
        else:
            base = (math.sin(k0 * w / 2 * ct) / ct) ** 2 * math.sin(t) ** 3
        g1 += base
        if i % 20 == 0:                         # J0 is smooth; sample it coarsely
            g12 += 20 * base * j0(k0 * l * math.sin(t))
    g1 *= dt / (120 * math.pi ** 2)
    g12 *= dt / (120 * math.pi ** 2)
    return 1 / (2 * (g1 + g12))


def feed_position() -> tuple[str, float, float]:
    r_edge = edge_resistance()
    y50 = L_MM / math.pi * math.acos(math.sqrt(50 / r_edge))
    W, H = 560, 330
    X0, X1, Y0, Y1 = 80, 530, 38, 262           # plot box
    xmax, rmax = L_MM / 2, 350

    def px(x): return X0 + x / xmax * (X1 - X0)
    def py(r): return Y1 - r / rmax * (Y1 - Y0)

    b = [markers(NAVY, RED, GRAY)]
    for r in range(0, 351, 50):
        b.append(f'<line x1="{X0}" y1="{py(r):.1f}" x2="{X1}" y2="{py(r):.1f}" stroke="{RULE}" stroke-width="1"/>')
        b.append(text(X0 - 8, py(r) + 6, str(r), GRAY, 16, anchor="end"))
    for x in range(0, 15, 2):
        b.append(f'<line x1="{px(x):.1f}" y1="{Y1}" x2="{px(x):.1f}" y2="{Y1 + 5}" stroke="{GRAY}" stroke-width="1"/>')
        b.append(text(px(x), Y1 + 24, str(x), GRAY, 16))
    b.append(f'<rect x="{X0}" y="{Y0}" width="{X1 - X0}" height="{Y1 - Y0}" fill="none" stroke="{SUB_EDGE}"/>')
    pts = " ".join(f"{px(x):.1f},{py(r_edge * math.cos(math.pi * x / L_MM) ** 2):.1f}"
                   for x in [xmax * i / 200 for i in range(201)])
    b.append(f'<polyline points="{pts}" fill="none" stroke="{NAVY}" stroke-width="3"/>')
    b.append(f'<line x1="{X0}" y1="{py(50):.1f}" x2="{X1}" y2="{py(50):.1f}" stroke="{RED}" stroke-width="1.8" stroke-dasharray="7 5"/>')
    b.append(f'<line x1="{px(y50):.1f}" y1="{py(50):.1f}" x2="{px(y50):.1f}" y2="{Y1}" stroke="{RED}" stroke-width="1.4" stroke-dasharray="3 3"/>')
    b.append(f'<circle cx="{px(y50):.1f}" cy="{py(50):.1f}" r="5.5" fill="{RED}"/>')
    b.append(text(px(y50) - 12, py(50) + 26, f"50 Ω at {y50:.1f} mm", RED, 18, "700", "end"))
    b.append(text(px(0) + 12, py(r_edge) - 10, f"about {round(r_edge, -1):.0f} Ω at the edge", NAVY, 18, "700", "start"))
    b.append(text(X1 - 6, py(100), "0 Ω at the center", NAVY, 18, "700", "end"))
    b.append(arrow(X1 - 30, py(88), X1 - 5, py(6), NAVY, 1.6))
    b.append(text((X0 + X1) / 2, Y1 + 52, "feed point, mm in from the edge", GRAY, 17))
    b.append(text(22, (Y0 + Y1) / 2, "input resistance (Ω)", GRAY, 17, rot=-90))
    b.append(text(X0 + 2, 24, "2.45 GHz patch on FR-4", GRAY, 16, anchor="start"))
    s = svg(W, H, f"Input resistance of the 2.45 GHz FR-4 patch against feed position: about "
            f"{round(r_edge, -1):.0f} ohms at the radiating edge, falling to zero at the center, and "
            f"crossing 50 ohms {y50:.1f} mm in from the edge", b, "l13fp")
    return s, r_edge, y50


def main() -> None:
    fp, r_edge, y50 = feed_position()
    figs = {
        "L13-patch-standing-wave.svg": standing_wave(),
        "L13-patch-edges.svg": edges(),
        "L13-patch-feeds.svg": feeds(),
        "L13-patch-feed-position.svg": fp,
    }
    for d in OUTS:
        for name, s in figs.items():
            p = d / name
            p.write_text(s)
            print("wrote", p.relative_to(ROOT))
    print(f"edge resistance {r_edge:.0f} ohm, 50 ohm point {y50:.2f} mm from the edge")


if __name__ == "__main__":
    main()
