#!/usr/bin/env python3
"""L21 Lab figures, drawn as hand-built SVG.

  - L21-three-methods   : the three ways to trace a pattern -- the beam sweep,
                          the azimuth sweep by hand, the azimuth sweep on the
                          stand -- one panel each.
  - L21-bench-layout    : the bench from above: the kit on its stand, the HB100
                          on its tripod 1.2 m out, the taped 1.2 m arc with its
                          -90/0/+90 marks and the start end, E1/E8, the laptop.
  - L21-range-artifacts : a classroom (direct path plus floor and wall
                          reflections) beside an anechoic chamber.
  - L21-run3-reading    : one beam sweep at one kit position, read at 0 deg
                          (Table D) and at the sample nearest 30 deg (Table E).
                          Unnumbered level axis, so it gives no answers.
  - L21-tracking-tab    : the Signal vs Time plot as the kit draws it: the
                          title, the hover readout, the 30 s window, Stop/Start.

Every figure is drawn for an <img> that a phone shrinks to about 342 px wide,
so text is sized at 3.1 percent of the viewBox width or more: 10.5 px at 342.
Sign convention as in m3_l21_rotation_setup.py: seen from above with the
source at the top, E1 is on the left, E8 on the right, and +theta is on the
E8 side (Lesson 18).

    python3 scripts/graphics/m3_l21_lab_figures.py
"""

from __future__ import annotations
import math
from pathlib import Path

import numpy as np
from svg_font_stack import apply_font_stack

OUT = Path(__file__).resolve().parents[2] / "book/extras/viz/img"
NAVY, MID, LIGHT, RED, GRAY, INK, ORANGE, GREEN = (
    "#004a85", "#0067b9", "#cddce9", "#b01e24", "#5a5a5a", "#1f2a36", "#d9822b", "#1d7a4d")

# array model for the schematic traces (HB100 nominal, as the lab packet)
LAM = 3e8 / 10.525e9
D = 0.014
N = 8
KD = 2 * math.pi * D / LAM
LSB = math.radians(2.8125)


def defs(*colors):
    out = ["<defs>"]
    for name, c in colors:
        out.append(f'<marker id="l21{name}" viewBox="0 0 10 10" refX="8.5" refY="5" markerWidth="6" '
                   f'markerHeight="6" orient="auto-start-reverse"><path d="M0 0 L10 5 L0 10 z" fill="{c}"/></marker>')
    out.append("</defs>")
    return "".join(out)


def text(x, y, s, size, fill=INK, anchor="middle", weight="400", style=""):
    st = f' font-style="{style}"' if style else ""
    return (f'<text x="{x:.1f}" y="{y:.1f}" text-anchor="{anchor}" font-size="{size}" '
            f'font-weight="{weight}" fill="{fill}"{st}>{s}</text>')


def array(cx, cy, ang_deg=0.0, pitch=10.0, w=7.0, h=9.0):
    """Eight patches centered at (cx, cy); the row turned ang_deg (+ = face toward screen-left)."""
    a = math.radians(ang_deg)
    ux, uy = math.cos(a), -math.sin(a)
    out = []
    for i in range(8):
        off = (i - 3.5) * pitch
        ex, ey = cx + off * ux, cy + off * uy
        out.append(f'<rect x="{ex - w / 2:.1f}" y="{ey - h / 2:.1f}" width="{w}" height="{h}" rx="1.2" '
                   f'fill="{NAVY}" transform="rotate({-ang_deg:.1f} {ex:.1f} {ey:.1f})"/>')
    return "".join(out)


def wedge(cx, cy, ang_deg, length, half_deg, fill, opacity=1.0):
    """A beam: a wedge from (cx, cy), axis at ang_deg from 'up' (+ = screen-right)."""
    a0 = math.radians(ang_deg - half_deg)
    a1 = math.radians(ang_deg + half_deg)
    x0, y0 = cx + length * math.sin(a0), cy - length * math.cos(a0)
    x1, y1 = cx + length * math.sin(a1), cy - length * math.cos(a1)
    return (f'<path d="M{cx:.1f} {cy:.1f} L{x0:.1f} {y0:.1f} A{length} {length} 0 0 1 {x1:.1f} {y1:.1f} Z" '
            f'fill="{fill}" fill-opacity="{opacity}"/>')


def arc_pts(cx, cy, r, a0, a1):
    """Arc from angle a0 to a1 (deg from 'up', + = screen-right), as SVG path."""
    x0, y0 = cx + r * math.sin(math.radians(a0)), cy - r * math.cos(math.radians(a0))
    x1, y1 = cx + r * math.sin(math.radians(a1)), cy - r * math.cos(math.radians(a1))
    sweep = 1 if a1 > a0 else 0
    large = 1 if abs(a1 - a0) > 180 else 0
    return f"M{x0:.1f} {y0:.1f} A{r} {r} 0 {large} {sweep} {x1:.1f} {y1:.1f}"


def write(name, body, w, h, label):
    s = (f'<svg viewBox="0 0 {w} {h}" xmlns="http://www.w3.org/2000/svg" role="img" '
         f'aria-label="{label}">' + body + "</svg>")
    (OUT / f"{name}.svg").write_text(apply_font_stack(s) + "\n")
    print(f"wrote {OUT / (name + '.svg')}")


# ------------------------------------------------------------ three methods
def three_methods():
    W, H, F = 600, 300, 19
    s = [defs(("G", GRAY), ("R", RED))]
    ay, sy = 222, 58
    titles = ("beam sweep", "by hand", "on the stand")
    axes = ("x: steer angle", "x: time", "x: stand angle")
    for k in range(3):
        cx = 100 + 200 * k
        s.append(text(cx, 26, titles[k], F, NAVY, weight="700"))
        s.append(text(cx, 284, axes[k], F, GRAY))
        if k:
            s.append(f'<line x1="{200 * k}" y1="10" x2="{200 * k}" y2="290" stroke="{LIGHT}" stroke-width="1.2"/>')
    # (a) source fixed, the beam stepped past it
    cx = 100
    for a in (-50, -25, 25, 50):
        s.append(wedge(cx, ay, a, 120, 7, MID, 0.18))
    s.append(wedge(cx, ay, 0, 120, 7, MID, 0.75))
    s.append(f'<path d="{arc_pts(cx, ay, 92, -42, 42)}" fill="none" stroke="{GRAY}" stroke-width="1.6" '
             'marker-start="url(#l21G)" marker-end="url(#l21G)"/>')
    s.append(f'<circle cx="{cx}" cy="{sy}" r="8" fill="{RED}"/>')
    s.append(array(cx, ay))
    # (b) beam held, source carried around the arc
    cx = 300
    s.append(wedge(cx, ay, 0, 72, 7, MID, 0.75))
    s.append(f'<path d="{arc_pts(cx, ay, 88, -80, 80)}" fill="none" stroke="{GRAY}" stroke-width="1.3" '
             'stroke-dasharray="5 4"/>')
    s.append(f'<path d="{arc_pts(cx, ay, 104, -72, -38)}" fill="none" stroke="{RED}" stroke-width="1.8" '
             'marker-end="url(#l21R)"/>')
    sx, sy2 = cx + 88 * math.sin(math.radians(-55)), ay - 88 * math.cos(math.radians(-55))
    s.append(f'<circle cx="{sx:.1f}" cy="{sy2:.1f}" r="8" fill="{RED}"/>')
    s.append(array(cx, ay))
    # (c) source fixed, the kit turned on its stand
    cx = 500
    s.append(f'<circle cx="{cx}" cy="{ay}" r="34" fill="#eef4fa" stroke="{GRAY}" stroke-width="1.2"/>')
    s.append(wedge(cx, ay, -30, 118, 7, MID, 0.75))
    s.append(f'<path d="{arc_pts(cx, ay, 52, 20, -24)}" fill="none" stroke="{GRAY}" stroke-width="1.6" '
             'marker-end="url(#l21G)"/>')
    s.append(f'<circle cx="{cx}" cy="{sy}" r="8" fill="{RED}"/>')
    s.append(array(cx, ay, 30))
    write("L21-three-methods", "".join(s), W, H,
          "Three ways to trace a pattern. Beam sweep: the HB100 stays put and the kit steps the beam "
          "past it. By hand: the beam is held and you carry the HB100 around an arc. On the stand: "
          "the beam is held, the HB100 stays on its tripod, and the kit turns on its stand.")


# --------------------------------------------------------------- bench layout
def bench_layout():
    W, H, F = 560, 560, 18
    cx, cy, R = 280, 400, 230
    s = [defs(("G", GRAY), ("R", RED), ("N", NAVY))]
    # taped arc with its marks
    s.append(f'<path d="{arc_pts(cx, cy, R, -90, 90)}" fill="none" stroke="{ORANGE}" stroke-width="3" '
             'stroke-dasharray="10 6"/>')
    for a in (-90, 0, 90):
        x, y = cx + R * math.sin(math.radians(a)), cy - R * math.cos(math.radians(a))
        dx, dy = math.sin(math.radians(a)), -math.cos(math.radians(a))
        s.append(f'<line x1="{x - 12 * dx:.1f}" y1="{y - 12 * dy:.1f}" x2="{x + 12 * dx:.1f}" '
                 f'y2="{y + 12 * dy:.1f}" stroke="{ORANGE}" stroke-width="4"/>')
    s.append(text(cx - R, cy + 34, "−90°", F, ORANGE, weight="700"))
    s.append(text(cx - R, cy + 56, "start here", F, ORANGE))
    s.append(text(cx + R, cy + 34, "+90°", F, ORANGE, weight="700"))
    s.append(text(cx + R, cy + 56, "end", F, ORANGE))
    # carrying direction
    s.append(f'<path d="{arc_pts(cx, cy, R + 26, -78, -48)}" fill="none" stroke="{RED}" stroke-width="2" '
             'marker-end="url(#l21R)"/>')
    # HB100 on its tripod at 0 deg, on the arc
    s.append(f'<circle cx="{cx}" cy="{cy - R}" r="11" fill="{RED}"/>')
    s.append(text(cx, cy - R - 42, "HB100 on its tripod", F, RED, weight="700"))
    s.append(text(cx, cy - R - 20, "0°, aimed at the array", F, RED))
    # line of sight and the 1.2 m radius
    s.append(f'<line x1="{cx}" y1="{cy - 14}" x2="{cx}" y2="{cy - R + 14}" stroke="{GRAY}" stroke-width="1.3" '
             'stroke-dasharray="5 4"/>')
    s.append(f'<line x1="{cx + 8}" y1="{cy - 12}" x2="{cx + 8 + (R - 26) * math.sin(math.radians(35)):.1f}" '
             f'y2="{cy - 12 - (R - 26) * math.cos(math.radians(35)):.1f}" stroke="{GRAY}" stroke-width="1.3" '
             'marker-end="url(#l21G)"/>')
    s.append(text(cx + 128, cy - 112, "1.2 m", F, INK, anchor="start"))
    # the kit on its stand
    s.append(f'<circle cx="{cx}" cy="{cy}" r="40" fill="#eef4fa" stroke="{GRAY}" stroke-width="1.3"/>')
    s.append(array(cx, cy, 0, pitch=10, w=7, h=9))
    s.append(text(cx - 66, cy + 6, "E1", F, NAVY, weight="700"))
    s.append(text(cx + 66, cy + 6, "E8", F, NAVY, weight="700"))
    s.append(text(cx, cy + 64, "kit on its stand, 0° toward the HB100", F, NAVY))
    # laptop and cable
    s.append(f'<rect x="{cx - 46}" y="{cy + 98}" width="92" height="40" rx="4" fill="#fff" stroke="{GRAY}" stroke-width="1.5"/>')
    s.append(text(cx, cy + 124, "laptop", F, GRAY))
    s.append(f'<path d="M{cx + 22} {cy + 36} C{cx + 60} {cy + 70}, {cx + 50} {cy + 90}, {cx + 30} {cy + 98}" '
             f'fill="none" stroke="{GRAY}" stroke-width="1.5"/>')
    write("L21-bench-layout", "".join(s), W, H,
          "The bench seen from above: the kit on its stand at the center, its patches toward the HB100, "
          "E1 on the left and E8 on the right; the HB100 on its tripod 1.2 m out at 0 degrees; a taped "
          "1.2 m arc from minus 90 degrees on the E1 side, where the sweep by hand starts, to plus 90 "
          "degrees on the E8 side; the laptop behind the kit.")


# ------------------------------------------------------------ range artifacts
def range_artifacts():
    W, H, F = 600, 300, 19
    s = [defs(("G", GRAY), ("R", RED))]
    for k, title in enumerate(("classroom", "anechoic chamber")):
        s.append(text(150 + 300 * k, 28, title, F, NAVY, weight="700"))
    s.append(f'<line x1="300" y1="12" x2="300" y2="290" stroke="{LIGHT}" stroke-width="1.2"/>')
    # classroom: side view, source left, kit right, floor and wall paths
    fy, wx = 236, 284
    s.append(f'<line x1="14" y1="{fy}" x2="{wx - 6}" y2="{fy}" stroke="{GRAY}" stroke-width="3"/>')
    s.append(text(150, fy + 30, "floor", F, GRAY))
    s.append(f'<line x1="{wx - 6}" y1="56" x2="{wx - 6}" y2="{fy}" stroke="{GRAY}" stroke-width="3"/>')
    srcx, srcy, kx, ky = 44, 130, 214, 130
    s.append(f'<circle cx="{srcx}" cy="{srcy}" r="9" fill="{RED}"/>')
    s.append(f'<rect x="{kx - 4}" y="{ky - 30}" width="8" height="60" fill="{NAVY}"/>')
    s.append(f'<line x1="{kx}" y1="{ky + 30}" x2="{kx}" y2="{fy}" stroke="{GRAY}" stroke-width="2"/>')
    s.append(f'<line x1="{srcx + 10}" y1="{srcy}" x2="{kx - 8}" y2="{ky}" stroke="{RED}" stroke-width="2.2" marker-end="url(#l21R)"/>')
    mx = (srcx + kx) / 2
    s.append(f'<polyline points="{srcx + 6},{srcy + 8} {mx},{fy - 2} {kx - 8},{ky + 14}" fill="none" '
             f'stroke="{ORANGE}" stroke-width="1.8" stroke-dasharray="6 4" marker-end="url(#l21G)"/>')
    s.append(f'<polyline points="{srcx + 8},{srcy - 8} {wx - 8},{86} {kx + 6},{ky - 16}" fill="none" '
             f'stroke="{ORANGE}" stroke-width="1.8" stroke-dasharray="6 4" marker-end="url(#l21G)"/>')
    s.append(text(150, 76, "reflections add", F, ORANGE))
    # chamber: absorber wedges on every wall, direct path only, turntable
    x0, x1, y0, y1 = 316, 586, 52, 262
    s.append(f'<rect x="{x0}" y="{y0}" width="{x1 - x0}" height="{y1 - y0}" fill="none" stroke="{GRAY}" stroke-width="2"/>')
    for i in range(12):
        x = x0 + 6 + i * 22.5
        s.append(f'<path d="M{x:.1f} {y0} L{x + 11:.1f} {y0 + 16} L{x + 22:.1f} {y0}" fill="{LIGHT}"/>')
        s.append(f'<path d="M{x:.1f} {y1} L{x + 11:.1f} {y1 - 16} L{x + 22:.1f} {y1}" fill="{LIGHT}"/>')
    for j in range(9):
        y = y0 + 4 + j * 22.8
        s.append(f'<path d="M{x0} {y:.1f} L{x0 + 16} {y + 11:.1f} L{x0} {y + 22:.1f}" fill="{LIGHT}"/>')
        s.append(f'<path d="M{x1} {y:.1f} L{x1 - 16} {y + 11:.1f} L{x1} {y + 22:.1f}" fill="{LIGHT}"/>')
    sx2, kx2, yy = 354, 534, 150
    s.append(f'<circle cx="{sx2}" cy="{yy}" r="9" fill="{RED}"/>')
    s.append(f'<rect x="{kx2 - 4}" y="{yy - 30}" width="8" height="60" fill="{NAVY}"/>')
    s.append(f'<ellipse cx="{kx2}" cy="{yy + 44}" rx="26" ry="8" fill="#eef4fa" stroke="{GRAY}" stroke-width="1.3"/>')
    s.append(f'<line x1="{kx2}" y1="{yy + 30}" x2="{kx2}" y2="{yy + 40}" stroke="{GRAY}" stroke-width="2"/>')
    s.append(f'<line x1="{sx2 + 10}" y1="{yy}" x2="{kx2 - 8}" y2="{yy}" stroke="{RED}" stroke-width="2.2" marker-end="url(#l21R)"/>')
    s.append(text(450, 236, "direct path only", F, RED))
    write("L21-range-artifacts", "".join(s), W, H,
          "Left, a classroom seen from the side: the direct path from the HB100 to the kit, plus "
          "reflections off the floor and a wall that add to it. Right, an anechoic chamber: absorber on "
          "every wall, a turntable under the antenna, and only the direct path.")


# ---------------------------------------------------------------- run 3 read
def af_db(psi):
    den = N * np.sin(psi / 2)
    small = np.abs(den) < 1e-12
    af = np.where(small, 1.0, np.sin(N * psi / 2) / np.where(small, 1.0, den))
    return 10 * np.log10(af ** 2 + 10 ** (-2.3))


def run3_reading():
    W, H, F = 600, 330, 19
    X0, X1, Y0, Y1 = 60, 560, 40, 250          # plot box
    s = [defs(("N", NAVY))]
    src = 40.0                                  # the kit turned so the source sits at +40
    k = np.arange(-400, 401)
    s0 = k * LSB / KD
    s0 = s0[np.abs(s0) <= 1.0]
    ang = np.degrees(np.arcsin(s0))
    lev = af_db(KD * (math.sin(math.radians(src)) - s0))
    lev = lev - lev.max()

    def px(a):
        return X0 + (a + 90) / 180 * (X1 - X0)

    def py(db):
        return Y0 + (-db) / 26 * (Y1 - Y0)

    s.append(f'<rect x="{X0}" y="{Y0}" width="{X1 - X0}" height="{Y1 - Y0}" fill="none" stroke="{LIGHT}" stroke-width="1.2"/>')
    pts = " ".join(f"{px(a):.1f},{py(max(l, -26)):.1f}" for a, l in zip(ang, lev))
    s.append(f'<polyline points="{pts}" fill="none" stroke="{NAVY}" stroke-width="2"/>')
    for a in (-90, 0, 30, 90):
        lab = "0°" if a == 0 else f"{a:+d}°".replace("-", "−")
        s.append(f'<line x1="{px(a):.1f}" y1="{Y1}" x2="{px(a):.1f}" y2="{Y1 + 6}" stroke="{GRAY}" stroke-width="1.2"/>')
        s.append(text(px(a), Y1 + 28, lab, F, GRAY))
    s.append(text((X0 + X1) / 2, Y1 + 62, "steer angle", F, GRAY))
    s.append(text(26, (Y0 + Y1) / 2, "level", F, GRAY, anchor="middle")
             .replace("<text", f'<text transform="rotate(-90 26 {(Y0 + Y1) / 2})"'))
    # the two samples read at this kit position
    i0 = int(np.argmin(np.abs(ang - 0.0)))
    i30 = int(np.argmin(np.abs(ang - 30.0)))
    for i, lab, col in ((i0, "Table D", GREEN), (i30, "Table E", ORANGE)):
        x, y = px(ang[i]), py(max(lev[i], -26))
        s.append(f'<line x1="{x:.1f}" y1="{Y0}" x2="{x:.1f}" y2="{Y1}" stroke="{col}" stroke-width="1.5" stroke-dasharray="5 4"/>')
        s.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="6.5" fill="{col}"/>')
    s.append(text(px(0) - 10, Y0 + 26, "Table D", F, GREEN, anchor="end", weight="700"))
    s.append(text(px(ang[i30]) - 10, Y0 + 26, "Table E", F, ORANGE, anchor="end", weight="700"))
    write("L21-run3-reading", "".join(s), W, H,
          "One beam sweep at one kit position, against steer angle, with an unnumbered level axis. "
          "The sample at 0 degrees steer goes in Table D and the sample nearest 30 degrees goes in Table E.")


# --------------------------------------------------------------- tracking tab
def tracking_tab():
    W, H, F = 600, 360, 19
    X0, X1, Y0, Y1 = 60, 584, 64, 262
    s = [defs(("G", GRAY))]
    s.append(f'<rect x="4" y="4" width="{W - 8}" height="{H - 8}" rx="8" fill="#f7fafd" stroke="{LIGHT}" stroke-width="1.5"/>')
    s.append(text(W / 2, 40, "Beam held at 0.0° · N updates/s", F, INK, weight="700"))
    s.append(f'<rect x="{X0}" y="{Y0}" width="{X1 - X0}" height="{Y1 - Y0}" fill="#fff" stroke="{LIGHT}" stroke-width="1.2"/>')
    # a 22 s sweep by hand in a 30 s window, pace uneven
    T, Twin = 22.0, 30.0
    u = np.linspace(0, 1, 1500)
    g = u + (0.45 / (2 * np.pi)) * (1 - np.cos(2 * np.pi * u)) + (0.30 / (4 * np.pi)) * (1 - np.cos(4 * np.pi * u))
    th = np.radians(-90 + 180 * g)
    lev = af_db(KD * np.sin(th)) + 10 * np.log10(np.clip(np.cos(th), 1e-9, None))
    lev = np.maximum(lev - lev.max(), -26)
    t0 = 3.0

    def px(t):
        return X0 + t / Twin * (X1 - X0)

    def py(db):
        return Y0 + 14 + (-db) / 26 * (Y1 - Y0 - 20)

    pts = " ".join(f"{px(t0 + t):.1f},{py(l):.1f}" for t, l in zip(u * T, lev))
    s.append(f'<polyline points="{pts}" fill="none" stroke="{NAVY}" stroke-width="1.8"/>')
    for t in (0, 10, 20, 30):
        s.append(f'<line x1="{px(t):.1f}" y1="{Y1}" x2="{px(t):.1f}" y2="{Y1 + 6}" stroke="{GRAY}" stroke-width="1.2"/>')
        s.append(text(px(t), Y1 + 28, f"{t}", F, GRAY))
    s.append(text((X0 + X1) / 2, Y1 + 56, "time (s), the last 30 s", F, GRAY))
    s.append(text(26, (Y0 + Y1) / 2, "level (dBFS)", F, GRAY)
             .replace("<text", f'<text transform="rotate(-90 26 {(Y0 + Y1) / 2})"'))
    # hover readout on the main-lobe peak
    ipk = int(np.argmax(lev))
    xp, yp = px(t0 + u[ipk] * T), py(lev[ipk])
    s.append(f'<circle cx="{xp:.1f}" cy="{yp:.1f}" r="6" fill="{ORANGE}"/>')
    bx = xp + 16
    s.append(f'<rect x="{bx:.1f}" y="{yp - 6:.1f}" width="150" height="34" rx="4" fill="#fff" stroke="{ORANGE}" stroke-width="1.5"/>')
    s.append(text(bx + 75, yp + 18, "hover: dBFS", F, INK))
    write("L21-tracking-tab", "".join(s), W, H,
          "The Signal vs Time plot on the Tracking tab: the title reads Beam held at 0.0 degrees and "
          "the update rate; the trace of one 22 second sweep by hand sits in a 30 second window of "
          "level in dBFS against time; hovering over a lobe peak reads its level.")


if __name__ == "__main__":
    three_methods()
    bench_layout()
    range_artifacts()
    run3_reading()
    tracking_tab()
