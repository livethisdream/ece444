#!/usr/bin/env python3
"""L17 illustration-sweep figures (phased-array hardware), drawn for a present
column rather than a full page.

  L17-hybrid-split   : all-analog, the PHASER's hybrid, and fully digital, side
                       by side, with the phase-shifter / receiver /
                       digital-weight counts under each (8/1/0, 8/2/2, 0/8/8)
  L17-adar-align     : four adjacent elements receiving a wave from 20 degrees
                       off broadside, the same four after their phase shifters
                       remove the step, and the two sums (4 against 1.70)
  L17-hb100-spread   : the 10.1-10.7 GHz HB100 unit-to-unit spread against the
                       Pluto's 3 MHz window drawn to scale, and a zoom on that
                       window with one tone at +1 MHz over a flat floor

Every plotted number is computed here, asserted, and printed for checking
against the lesson text. Words and numbers only, no equations, so one SVG
serves both the deck and the page. (The fourth L17 figure, the frequency
plan, lives with the signal chain in m3_l17_chain.py.)

Sizing: a present column is 477 px wide at 1280x800 and 343 px at 390x844.
The viewBox is 420 units wide and the smallest label is 13 units, so the
smallest rendered label is 13 x 343/420 = 10.6 px on a phone and 14.8 px on a
laptop. The width attribute (560) is larger than either column, so the image
always fills its column.

    python3 scripts/graphics/l17_figures.py

Writes:
    book/extras/slides/fig/L17-hybrid-split.svg
    book/extras/slides/fig/L17-adar-align.svg
    book/extras/slides/fig/L17-hb100-spread.svg
    book/extras/viz/img/L17-hybrid-split.svg
    book/extras/viz/img/L17-adar-align.svg
    book/extras/viz/img/L17-hb100-spread.svg
"""

from __future__ import annotations

from pathlib import Path

import numpy as np

from m3_l17_chain import AMBER, BG, EDGE2, FONT, GRN, INK, INK3, MID, NAVY
from svg_font_stack import apply_font_stack

REPO = Path(__file__).resolve().parents[2]
OUTS = (REPO / "book/extras/slides/fig", REPO / "book/extras/viz/img")

W = 420                 # viewBox width, drawn for a present column
SCALE = 560 / W         # intrinsic size: wider than any column, so it fills
MIN_FONT = 13           # smallest label, in viewBox units
NAVY_L = "#eaf2f9"
AMBER_L = "#fdf6e8"
GRN_L = "#eef6ec"
MINUS = "−"

# Canonical numbers (COURSE_SPEC section M3).
D_LAM = 0.491           # d / lambda at the HB100's 10.525 GHz
THETA = 20.0            # arrival angle off broadside, degrees, for the figure
F_NOM = 10.525          # GHz, HB100 nominal
HB_LO, HB_HI = 10.1, 10.7   # GHz, HB100 unit-to-unit spread
FS_MHZ = 3.0            # Pluto sample rate in the GUI, MSPS = window width, MHz


# --------------------------------------------------------------------------
# drawing helpers (everything in viewBox units)
# --------------------------------------------------------------------------

def txt(x, y, s, size=13, fill=INK, anchor="middle", weight="400", extra=""):
    assert size >= MIN_FONT, f"label {s!r} at {size} is below {MIN_FONT}"
    return (f'<text x="{x:.1f}" y="{y:.1f}" font-family="{FONT}" font-size="{size}" '
            f'fill="{fill}" text-anchor="{anchor}" font-weight="{weight}"{extra}>{s}</text>')


def rect(x, y, w, h, fill="none", stroke=NAVY, sw=1.4, rx=3, extra=""):
    return (f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" rx="{rx}" '
            f'fill="{fill}" stroke="{stroke}" stroke-width="{sw}"{extra}/>')


def line(x1, y1, x2, y2, stroke=INK3, sw=1.3, extra=""):
    return (f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" '
            f'stroke="{stroke}" stroke-width="{sw}" stroke-linecap="round"{extra}/>')


def circle(cx, cy, r, fill="#ffffff", stroke=NAVY, sw=1.4):
    return (f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="{r}" fill="{fill}" '
            f'stroke="{stroke}" stroke-width="{sw}"/>')


def polyline(xs, ys, stroke=NAVY, sw=1.8, extra=""):
    pts = " ".join(f"{x:.1f},{y:.1f}" for x, y in zip(xs, ys))
    return (f'<polyline points="{pts}" fill="none" stroke="{stroke}" '
            f'stroke-width="{sw}" stroke-linejoin="round"{extra}/>')


def markers(prefix, colors):
    out = ["<defs>"]
    for name, color in colors:
        out.append(
            f'<marker id="{prefix}{name}" viewBox="0 0 10 10" refX="9" refY="5" '
            f'markerWidth="6" markerHeight="6" orient="auto-start-reverse">'
            f'<path d="M 0 0 L 10 5 L 0 10 z" fill="{color}"/></marker>')
    out.append("</defs>")
    return "".join(out)


def svg_open(h, label):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {h}" '
            f'width="{W * SCALE:.0f}" height="{h * SCALE:.0f}" role="img" '
            f'aria-label="{label}">')


def write(name, svg):
    svg = apply_font_stack(svg)
    for out in OUTS:
        out.mkdir(parents=True, exist_ok=True)
        (out / f"{name}.svg").write_text(svg, encoding="utf-8")
    print(f"wrote {name}.svg (deck + page)")


# --------------------------------------------------------------------------
# ILL-01 - the hybrid split
# --------------------------------------------------------------------------

def hybrid_split() -> str:
    H = 232
    PW, GAP, X0 = 132, 8, 4
    TOP, BOT = 27, 153                       # diagram band
    ry = [38 + 15 * i for i in range(8)]     # element rows
    mid = (ry[0] + ry[7]) / 2
    subs = ((ry[0] + ry[3]) / 2, (ry[4] + ry[7]) / 2)

    s = [svg_open(H, "Three receive architectures for eight elements: all analog "
                  "with 8 phase shifters, 1 receiver and no digital weights; the "
                  "PHASER hybrid with 8 phase shifters, 2 receivers and 2 digital "
                  "weights; fully digital with no phase shifters, 8 receivers and "
                  "8 digital weights. Shading marks the digital side of the ADC."),
         markers("hy", (("I", INK3), ("A", AMBER)))]

    def shifter(x, y):
        return rect(x, y - 5, 11, 10, "#ffffff", MID, 1.3, 2)

    def receiver(x, y, w=26, h=20, label=True):
        out = [rect(x, y - h / 2, w, h, "#ffffff", GRN, 1.5, 3)]
        if label:
            out.append(txt(x + w / 2, y + 4.5, "Rx", 13, GRN, weight="700"))
        return "".join(out)

    def summer(cx, cy, r, color):
        return circle(cx, cy, r, "#ffffff", color, 1.5) + \
            txt(cx, cy + 4.6, "Σ", 13, color, weight="700")

    def weight(cx, cy, r=8, label=True):
        out = circle(cx, cy, r, "#ffffff", AMBER, 1.5)
        if label:
            out += txt(cx, cy + 4.2, "w", 13, AMBER, weight="700")
        return out

    panels = (
        ("All analog", (8, 1, 0)),
        ("PHASER hybrid", (8, 2, 2)),
        ("Fully digital", (0, 8, 8)),
    )
    for k, (title, counts) in enumerate(panels):
        x = X0 + k * (PW + GAP)
        bnd = x + (98, 81, 44)[k]            # the ADC: analog left, digital right
        s.append(rect(x, TOP, PW, BOT - TOP, BG, EDGE2, 1.2, 5))
        s.append(f'<path d="M {bnd:.1f} {TOP} H {x + PW - 5:.1f} '
                 f'a 5 5 0 0 1 5 5 V {BOT - 5} a 5 5 0 0 1 -5 5 H {bnd:.1f} z" '
                 f'fill="{AMBER_L}" stroke="none"/>')
        s.append(line(bnd, TOP, bnd, BOT, AMBER, 1.2, ' stroke-dasharray="3 3"'))
        s.append(txt(x + PW / 2, 18, title, 13.5, NAVY, weight="700"))
        for y in ry:                          # the eight patches
            s.append(f'<rect x="{x + 4:.1f}" y="{y - 4.5:.1f}" width="5" height="9" '
                     f'fill="{NAVY}"/>')

        if k == 0:                            # all analog
            sx, rx = x + 52, x + 66
            for y in ry:
                s.append(line(x + 9, y, x + 16, y, MID, 1.2))
                s.append(line(x + 27, y, sx, mid, MID, 1.1))
                s.append(shifter(x + 16, y))
            s.append(summer(sx, mid, 10, NAVY))
            s.append(line(sx + 10, mid, rx, mid, NAVY, 1.8))
            s.append(receiver(rx, mid))
            s.append(line(rx + 26, mid, x + PW - 6, mid, INK3, 1.6,
                          ' marker-end="url(#hyI)"'))
        elif k == 1:                          # the PHASER
            sx, rx, wx, dx = x + 45, x + 56, x + 91, x + 108
            for j, cy in enumerate(subs):
                for y in ry[4 * j:4 * j + 4]:
                    s.append(line(x + 9, y, x + 16, y, MID, 1.2))
                    s.append(line(x + 27, y, sx, cy, MID, 1.1))
                    s.append(shifter(x + 16, y))
            for cy in subs:
                s.append(summer(sx, cy, 9, NAVY))
                s.append(line(sx + 9, cy, rx, cy, NAVY, 1.8))
                s.append(receiver(rx, cy, 22))
                s.append(line(rx + 22, cy, wx - 8, cy, INK3, 1.4))
                s.append(line(wx, cy, dx, mid, AMBER, 1.4))
                s.append(weight(wx, cy))
            s.append(summer(dx, mid, 8.5, AMBER))
            s.append(line(dx + 8.5, mid, x + PW - 4, mid, INK3, 1.6,
                          ' marker-end="url(#hyI)"'))
        else:                                 # fully digital
            wx, dx = x + 56, x + 100
            for y in ry:
                s.append(line(x + 9, y, x + 16, y, GRN, 1.2))
                s.append(receiver(x + 16, y, 22, 11, label=False))
                s.append(line(x + 38, y, wx - 5.5, y, INK3, 1.2))
                s.append(line(wx, y, dx, mid, AMBER, 1.1))
                s.append(weight(wx, y, 5.5, label=False))
            s.append(summer(dx, mid, 11, AMBER))
            s.append(line(dx + 11, mid, x + PW - 6, mid, INK3, 1.6,
                          ' marker-end="url(#hyI)"'))

        n_ps, n_rx, n_w = counts
        cx = x + PW / 2
        s.append(txt(cx, 173, f"{n_ps} phase shifters", 13, MID, weight="600"))
        s.append(txt(cx, 190, f"{n_rx} receiver{'' if n_rx == 1 else 's'}", 13, GRN,
                     weight="600"))
        s.append(txt(cx, 207, f"{n_w} digital weights", 13, AMBER, weight="600"))

    s.append(txt(W / 2, H - 5, "Rx: mixer and ADC. Shaded: digital.", 13, INK3))
    s.append("</svg>")
    return "\n".join(s)


# --------------------------------------------------------------------------
# ILL-02 - the ADAR1000 lines four elements up
# --------------------------------------------------------------------------

def adar_align() -> str:
    step = 360.0 * D_LAM * np.sin(np.radians(THETA))     # degrees per element
    n = np.arange(4)
    ph = np.exp(-1j * np.radians(step) * n)               # as received
    raw = np.abs(ph.sum())
    aligned = np.abs((ph * np.exp(1j * np.radians(step) * n)).sum())
    print(f"  ADAR1000: step {step:.2f} deg at d/lambda {D_LAM}, theta {THETA:g} deg; "
          f"|uncorrected sum| {raw:.4f}, |aligned sum| {aligned:.4f}")
    assert round(raw, 2) == 1.70, raw
    assert abs(aligned - 4.0) < 1e-12, aligned
    # 360 x 0.491 x sin 20 deg = 60.46 deg, which prints as 60.5 (the audit's
    # 60.4 truncated it); the sum 1.70 is the same either way.
    assert round(step, 1) == 60.5, step
    step_lbl = f"{step:.1f}"

    H = 326
    s = [svg_open(H, f"Four adjacent elements receive a wave from {THETA:g} degrees "
                  f"off broadside, each {step_lbl} degrees behind the last. After "
                  f"the phase shifters the four line up. Their sum has amplitude 4, "
                  f"against {raw:.2f} for the uncorrected sum."),
         ]

    # top row: (a) as received, (b) after the phase shifters
    PW, XS = 202, (6, 212)
    t0, t1 = 30, 194                          # trace x span inside a panel
    period = 110.0
    base = [52, 80, 108, 136]
    amp = 10.5
    x = np.linspace(0, t1 - t0, 220)
    for k, (title, shift) in enumerate((("(a) Received", True),
                                        ("(b) After the shifters", False))):
        x0 = XS[k]
        s.append(rect(x0, 4, PW, 150, BG, EDGE2, 1.2, 5))
        s.append(txt(x0 + 10, 24, title, 13.5, NAVY, anchor="start", weight="700"))
        # a guide through the first element's crest
        crest = x0 + t0 + period * 0.25
        s.append(line(crest, 34, crest, 148, INK3, 1.0, ' stroke-dasharray="3 3"'))
        for i, yb in enumerate(base):
            lag = np.radians(step * i) if shift else 0.0
            y = yb - amp * np.sin(2 * np.pi * x / period - lag)
            s.append(txt(x0 + 10, yb + 4.5, f"E{i + 1}", 13, INK3, anchor="start"))
            s.append(polyline(x0 + t0 + x, y, MID, 1.8))
    s.append(txt(XS[0] + PW / 2, 170, f"{THETA:g}° arrival, {step_lbl}° step", 13, INK3))
    s.append(txt(XS[1] + PW / 2, 170, "equal gains, aligned", 13, INK3))

    # bottom: (c) the sums
    y0, ppu = 264, 12.0                       # zero line, px per unit amplitude
    s.append(rect(6, 180, 408, 142, BG, EDGE2, 1.2, 5))
    s.append(txt(16, 200, "(c) The sum", 13.5, NAVY, anchor="start", weight="700"))
    xs = np.linspace(0, 236, 300)
    xl = 22
    s.append(line(xl, y0, xl + 236, y0, EDGE2, 1.0))
    sum_raw = ph.sum()
    y_al = y0 - ppu * aligned * np.sin(2 * np.pi * xs / period)
    y_rw = y0 - ppu * raw * np.sin(2 * np.pi * xs / period + np.angle(sum_raw))
    s.append(polyline(xl + xs, y_rw, AMBER, 2.0, ' stroke-dasharray="5 3"'))
    s.append(polyline(xl + xs, y_al, NAVY, 2.4))
    for level, color in ((aligned, NAVY), (raw, AMBER)):
        s.append(line(xl + 236, y0 - ppu * level, 272, y0 - ppu * level, color, 1.0,
                      ' stroke-dasharray="2 3"'))
    s.append(txt(278, y0 - ppu * aligned + 4.5, f"aligned: {aligned:.0f}", 13, NAVY,
                 anchor="start", weight="700"))
    s.append(txt(278, y0 - ppu * raw + 4.5, f"uncorrected: {raw:.2f}", 13, AMBER,
                 anchor="start", weight="700"))
    s.append(txt(278, y0 + 30, "one element = 1", 13, INK3, anchor="start"))
    s.append("</svg>")
    return "\n".join(s)


# --------------------------------------------------------------------------
# ILL-03 - the HB100 spread against the Pluto's window
# --------------------------------------------------------------------------

def hb100_spread() -> str:
    spread_mhz = (HB_HI - HB_LO) * 1e3
    ratio = spread_mhz / FS_MHZ
    print(f"  HB100: spread {spread_mhz:.0f} MHz over a {FS_MHZ:g} MHz window = {ratio:.0f}:1")
    assert round(ratio) == 200, ratio

    # the zoom: one tone at +1 MHz over a flat floor (seeded, reproducible)
    rng = np.random.default_rng(17)
    nb = 512
    f = np.linspace(-FS_MHZ / 2, FS_MHZ / 2, nb + 1)
    floor_db = -32.0
    noise = rng.exponential(1.0, (8, f.size)).mean(axis=0)    # 8-average periodogram
    p = 10 ** (floor_db / 10) * noise
    p += np.exp(-((f - 1.0) / 0.012) ** 2)                    # the tone, 0 dB peak
    lvl = 10 * np.log10(p)
    i_pk = int(np.argmax(lvl))
    away = np.abs(f - 1.0) > 0.1
    sep_med = lvl[i_pk] - np.median(lvl[away])
    sep_max = lvl[i_pk] - lvl[away].max()
    print(f"  HB100 zoom: peak {lvl[i_pk]:.2f} dB at {f[i_pk]:+.3f} MHz; "
          f"{sep_med:.1f} dB over the median floor, {sep_max:.1f} dB over its highest bin")
    assert abs(f[i_pk] - 1.0) < 0.01
    assert sep_max >= 20.0, sep_max

    H = 318
    s = [svg_open(H, f"Top: an axis from 10.0 to 10.8 GHz with the HB100 unit-to-unit "
                  f"spread, 10.1 to 10.7 GHz, as a band, and the Pluto's 3 MHz window "
                  f"drawn to scale as a hairline at {F_NOM} GHz, one two-hundredth of "
                  f"the spread. Bottom: the 3 MHz window magnified, one tone at plus 1 "
                  f"MHz from Signal Freq standing {sep_med:.0f} dB above a flat noise "
                  f"floor."),
         markers("hb", (("A", AMBER), ("I", INK3)))]

    # top: the spread, to scale
    gx0, gx1, f0, f1 = 24.0, 352.0, 10.0, 10.8
    gx = lambda v: gx0 + (v - f0) / (f1 - f0) * (gx1 - gx0)   # noqa: E731
    ay = 96
    s.append(rect(gx(HB_LO), 56, gx(HB_HI) - gx(HB_LO), 34, NAVY_L, NAVY, 1.4, 3))
    s.append(txt(gx(HB_LO) + 8, 70, "HB100 units", 13.5, NAVY, anchor="start",
                 weight="700"))
    s.append(txt(gx(HB_LO) + 8, 85, "10.1 – 10.7 GHz", 13, NAVY, anchor="start"))
    win = FS_MHZ * 1e-3 / (f1 - f0) * (gx1 - gx0)               # 1.3 units, to scale
    xw = gx(F_NOM)
    s.append(f'<rect x="{xw - win / 2:.2f}" y="46" width="{win:.2f}" height="{ay - 46}" '
             f'fill="{AMBER}"/>')
    s.append(line(xw - 2, 44, xw - 26, 26, AMBER, 1.2))
    s.append(txt(xw - 30, 24, "3 MHz window, to scale", 13, AMBER, anchor="end",
                 weight="700"))
    s.append(line(gx0, ay, gx1, ay, INK, 1.4))
    for v in (10.0, 10.2, 10.4, 10.6, 10.8):
        s.append(line(gx(v), ay, gx(v), ay + 5, INK3, 1.1))
        s.append(txt(gx(v), ay + 19, f"{v:.1f}", 13, INK3))
    s.append(txt(gx1 + 22, ay + 19, "GHz", 13, INK3, anchor="start"))

    # zoom wedge from the hairline down to the window plot
    px0, px1, py0, py1 = 52.0, 404.0, 158.0, 266.0
    s.append(line(xw, ay, xw, 122, AMBER, 1.0, ' stroke-dasharray="2 2"'))
    s.append(f'<path d="M {xw:.1f} 122 L {px0} {py0} L {px1} {py0} z" '
             f'fill="{AMBER_L}" stroke="{AMBER}" stroke-width="1" '
             f'stroke-dasharray="3 3"/>')

    # bottom: the window, magnified
    lo_db, hi_db = -45.0, 3.0
    fx = lambda v: px0 + (v + FS_MHZ / 2) / FS_MHZ * (px1 - px0)  # noqa: E731
    fy = lambda v: py1 - (v - lo_db) / (hi_db - lo_db) * (py1 - py0)  # noqa: E731
    s.append(rect(px0, py0, px1 - px0, py1 - py0, "#ffffff", EDGE2, 1.0, 0))
    for v in (0, -20, -40):
        s.append(line(px0, fy(v), px1, fy(v), EDGE2, 0.8))
        s.append(txt(px0 - 6, fy(v) + 4.5, f"{v:g}".replace("-", MINUS), 13, INK3,
                     anchor="end"))
    for v in (-1.5, -1.0, -0.5, 0.0, 0.5, 1.0, 1.5):
        s.append(line(fx(v), py1, fx(v), py1 + 5, INK3, 1.1))
        lab = f"{v:+g}".replace("-", MINUS) if v else "0"
        s.append(txt(fx(v), py1 + 19, lab, 13, INK3))
    s.append(txt((px0 + px1) / 2, py1 + 39, "Offset from Signal Freq (MHz)", 13, INK))
    s.append(txt(14, (py0 + py1) / 2, "dB", 13, INK,
                 extra=f' transform="rotate(-90 14 {(py0 + py1) / 2:.1f})"'))
    s.append(polyline(fx(f), fy(lvl), NAVY, 1.4))
    # the separation, peak to median floor
    fl = float(np.median(lvl[away]))
    xd = fx(1.25)
    s.append(line(xd, fy(lvl[i_pk]) + 2, xd, fy(fl) - 2, INK3, 1.2,
                  ' marker-start="url(#hbI)" marker-end="url(#hbI)"'))
    s.append(txt(xd + 6, (fy(lvl[i_pk]) + fy(fl)) / 2 + 4.5, f"{sep_med:.0f} dB", 13,
                 INK, anchor="start", weight="700"))
    s.append(txt(fx(1.0) - 8, fy(lvl[i_pk]) + 12, "tone at +1 MHz", 13, NAVY,
                 anchor="end", weight="700"))
    s.append("</svg>")
    return "\n".join(s)


def main() -> None:
    write("L17-hybrid-split", hybrid_split())
    write("L17-adar-align", adar_align())
    write("L17-hb100-spread", hb100_spread())


if __name__ == "__main__":
    main()
