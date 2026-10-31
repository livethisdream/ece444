#!/usr/bin/env python3
"""L19 Lab: the sequence of the hunt, five small top views of the firing range.

1 Bring up      own HB100 at boresight; Find HB100, Calibrate
2 Reference     a source toward +x sets the sign s of Angle
3 Walk          the fox is on; read Angle and Peak Gain at each station mark
4 Fix           the bearings cross; the nearest box is the call
5 Reveal        I name the live box; writeup compares

Every panel is drawn to one scale from the range in the lab: a 3.0 m firing
line with five station marks 0.75 m apart, and five boxes in a 2.0 m wide
field 1.0 to 2.0 m downrange, at least 0.75 m apart. The bearings in panels 3
and 4 are computed from the station and box positions, not drawn by eye.

Two layouts: a 5-across strip for a laptop column, and a 2-across stack for
a phone, served through <picture> by the lab page.

    python3 scripts/graphics/m3_l19_lab_sequence.py
    -> book/extras/viz/img/L19-lab-sequence.svg
       book/extras/viz/img/L19-lab-sequence-narrow.svg
"""

from __future__ import annotations
import math
from pathlib import Path

from svg_font_stack import apply_font_stack

OUT = Path(__file__).resolve().parents[2] / "book/extras/viz/img"

NAVY, RED, GRAY, INK, FIELD, LIGHT = "#004a85", "#b01e24", "#5a5a5a", "#1f2a36", "#eef4fa", "#c7d2e0"

PW, PH = 200, 292            # one panel
SCALE = 56.0                 # px per meter
LINE_Y = 200                 # firing line, panel coordinates
STATIONS = [-1.5 + 0.75 * i for i in range(5)]
BOXES = [(-0.85, 1.15), (0.0, 1.0), (0.85, 1.25), (-0.4, 1.85), (0.45, 1.95)]
LIVE = 3                     # index into BOXES: box 4
REF = (0.5, 1.0)             # reference-shot source, 26.6 deg toward +x

STEPS = [
    ("1", "Bring up", ["Own HB100 at", "boresight: Find", "HB100, Calibrate"]),
    ("2", "Reference shot", ["Source toward +x", "sets the sign s", "of Angle"]),
    ("3", "Walk the line", ["Fox on: Angle and", "Peak Gain at", "each station"]),
    ("4", "Fix", ["Bearings cross;", "the nearest box", "is your call"]),
    ("5", "Reveal", ["I name", "the live box;", "writeup compares"]),
]


def check_geometry() -> None:
    for i, a in enumerate(BOXES):
        assert -1.0 <= a[0] <= 1.0 and 1.0 <= a[1] <= 2.0, a
        for b in BOXES[i + 1:]:
            assert math.dist(a, b) >= 0.75, (a, b)
    ref = math.degrees(math.atan2(REF[0], REF[1]))
    assert abs(ref - 26.6) < 0.1, ref


def xy(ox, oy, x, y):
    """Range meters (x along the tape, y downrange) to SVG coordinates."""
    return ox + PW / 2 + x * SCALE, oy + LINE_Y - y * SCALE


def kit(s, ox, oy, x, faded=False):
    px, py = xy(ox, oy, x, 0)
    op = ' opacity="0.35"' if faded else ""
    s.append(f'<rect x="{px - 9:.1f}" y="{py - 3:.1f}" width="18" height="7" rx="1.5" fill="{NAVY}"{op}/>')


def panel(s, ox, oy, k):
    num, title, caption = STEPS[k]
    s.append(f'<rect x="{ox + 4}" y="{oy + 4}" width="{PW - 8}" height="{PH - 8}" rx="8" fill="#ffffff" '
             f'stroke="{LIGHT}" stroke-width="1.2"/>')
    s.append(f'<circle cx="{ox + 22}" cy="{oy + 24}" r="11" fill="{NAVY}"/>')
    s.append(f'<text x="{ox + 22}" y="{oy + 29}" text-anchor="middle" font-size="14" font-weight="700" '
             f'fill="#ffffff">{num}</text>')
    s.append(f'<text x="{ox + 40}" y="{oy + 29}" font-size="16" font-weight="700" fill="{INK}">{title}</text>')

    # box field and boxes
    fx0, fy0 = xy(ox, oy, -1.0, 2.0)
    s.append(f'<rect x="{fx0:.1f}" y="{fy0:.1f}" width="{2.0 * SCALE:.1f}" height="{1.0 * SCALE:.1f}" '
             f'fill="{FIELD}" stroke="none"/>')
    for i, (bx, by) in enumerate(BOXES):
        px, py = xy(ox, oy, bx, by)
        live = k == 4 and i == LIVE
        fill = RED if live else "#ffffff"
        s.append(f'<rect x="{px - 7:.1f}" y="{py - 7:.1f}" width="14" height="14" rx="2" fill="{fill}" '
                 f'stroke="{RED if live else GRAY}" stroke-width="1.3"/>')
        s.append(f'<text x="{px:.1f}" y="{py + 4.5:.1f}" text-anchor="middle" font-size="11" font-weight="700" '
                 f'fill="{"#ffffff" if live else GRAY}">{i + 1}</text>')

    # firing line with its five station marks
    lx0, ly = xy(ox, oy, -1.5, 0)
    lx1, _ = xy(ox, oy, 1.5, 0)
    s.append(f'<line x1="{lx0:.1f}" y1="{ly:.1f}" x2="{lx1:.1f}" y2="{ly:.1f}" stroke="{GRAY}" stroke-width="2"/>')
    for x in STATIONS:
        px, _ = xy(ox, oy, x, 0)
        s.append(f'<line x1="{px:.1f}" y1="{ly + 5:.1f}" x2="{px:.1f}" y2="{ly + 10:.1f}" stroke="{GRAY}" stroke-width="1.2"/>')

    if k == 0:
        kit(s, ox, oy, 0.0)
        hx, hy = xy(ox, oy, 0.0, 0.55)
        kx, ky = xy(ox, oy, 0.0, 0)
        s.append(f'<line x1="{kx:.1f}" y1="{ky - 4:.1f}" x2="{hx:.1f}" y2="{hy + 6:.1f}" stroke="{RED}" '
                 f'stroke-width="1.4" stroke-dasharray="4 3"/>')
        s.append(f'<circle cx="{hx:.1f}" cy="{hy:.1f}" r="5.5" fill="{RED}"/>')
    elif k == 1:
        kit(s, ox, oy, 0.0)
        kx, ky = xy(ox, oy, 0.0, 0)
        rx, ry = xy(ox, oy, *REF)
        s.append(f'<line x1="{kx:.1f}" y1="{ky - 4:.1f}" x2="{rx:.1f}" y2="{ry:.1f}" stroke="{RED}" '
                 f'stroke-width="1.4" stroke-dasharray="4 3"/>')
        s.append(f'<circle cx="{rx:.1f}" cy="{ry:.1f}" r="5.5" fill="{RED}"/>')
        ex, ey = xy(ox, oy, 1.5, 0)
        s.append(f'<text x="{ex:.1f}" y="{ey - 9:.1f}" text-anchor="end" font-size="12" font-weight="700" '
                 f'fill="{INK}">+x</text>')
    elif k in (2, 3):
        fox = BOXES[LIVE]
        used = [STATIONS[i] for i in ((2,) if k == 2 else (0, 1, 2, 3))]
        for x in STATIONS:
            kit(s, ox, oy, x, faded=x not in used)
        for x in used:
            kx, ky = xy(ox, oy, x, 0)
            # the bearing, carried 0.3 m past the fox so the crossing shows
            d = math.dist((x, 0), fox)
            ux, uy = (fox[0] - x) / d, fox[1] / d
            tx, ty = xy(ox, oy, fox[0] + 0.3 * ux, fox[1] + 0.3 * uy)
            s.append(f'<line x1="{kx:.1f}" y1="{ky - 4:.1f}" x2="{tx:.1f}" y2="{ty:.1f}" stroke="{NAVY}" '
                     f'stroke-width="1.3"/>')
        if k == 2:
            px, _ = xy(ox, oy, used[0], 0)
            s.append(f'<line x1="{px + 14:.1f}" y1="{ly + 17:.1f}" x2="{px + 44:.1f}" y2="{ly + 17:.1f}" stroke="{GRAY}" '
                     f'stroke-width="1.2" marker-end="url(#l19sArr)"/>')
        else:
            cx, cy = xy(ox, oy, *fox)
            s.append(f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="13" fill="none" stroke="{RED}" stroke-width="1.8"/>')
    else:
        for x in STATIONS:
            kit(s, ox, oy, x, faded=True)

    for j, line in enumerate(caption):
        s.append(f'<text x="{ox + PW / 2}" y="{oy + PH - 50 + 16 * j:.0f}" text-anchor="middle" '
                 f'font-size="13" fill="{INK}">{line}</text>')


def legend(s, ox, oy):
    """The key, in the cell the stacked layout leaves empty."""
    y = oy + 60
    s.append(f'<text x="{ox + 24}" y="{oy + 30}" font-size="15" font-weight="700" fill="{INK}">Key</text>')
    s.append(f'<rect x="{ox + 24}" y="{y - 4}" width="18" height="7" rx="1.5" fill="{NAVY}"/>')
    s.append(f'<text x="{ox + 52}" y="{y + 4}" font-size="13" fill="{INK}">your kit, on the line</text>')
    y += 32
    s.append(f'<line x1="{ox + 18}" y1="{y}" x2="{ox + 48}" y2="{y}" stroke="{GRAY}" stroke-width="2"/>')
    s.append(f'<text x="{ox + 52}" y="{y + 4}" font-size="13" fill="{INK}">firing line, 5 marks</text>')
    y += 32
    s.append(f'<rect x="{ox + 26}" y="{y - 7}" width="14" height="14" rx="2" fill="#ffffff" stroke="{GRAY}" stroke-width="1.3"/>')
    s.append(f'<text x="{ox + 52}" y="{y + 4}" font-size="13" fill="{INK}">numbered box</text>')
    y += 32
    s.append(f'<circle cx="{ox + 33}" cy="{y}" r="5.5" fill="{RED}"/>')
    s.append(f'<text x="{ox + 52}" y="{y + 4}" font-size="13" fill="{INK}">a live HB100</text>')
    y += 32
    s.append(f'<line x1="{ox + 18}" y1="{y}" x2="{ox + 48}" y2="{y}" stroke="{NAVY}" stroke-width="1.3"/>')
    s.append(f'<text x="{ox + 52}" y="{y + 4}" font-size="13" fill="{INK}">a bearing</text>')


def build(cols: int) -> str:
    rows = math.ceil(len(STEPS) / cols)
    w, h = PW * cols, PH * rows
    s = [f'<svg viewBox="0 0 {w} {h}" xmlns="http://www.w3.org/2000/svg" role="img" '
         f'aria-label="The L19 Lab in five steps, each a top view of the firing range: bring the kit up '
         f'on your own HB100; take the reference shot toward plus x to set the sign of Angle; with the '
         f'fox on, walk the station marks reading Angle and Peak Gain; the bearings cross at a box, which '
         f'is your call; I reveal the live box">']
    s.append(f'<defs><marker id="l19sArr" viewBox="0 0 10 10" refX="8.5" refY="5" markerWidth="6" '
             f'markerHeight="6" orient="auto"><path d="M0 0 L10 5 L0 10 z" fill="{GRAY}"/></marker></defs>')
    for k in range(len(STEPS)):
        r, c = divmod(k, cols)
        panel(s, c * PW, r * PH, k)
    if len(STEPS) % cols:
        r, c = divmod(len(STEPS), cols)
        legend(s, c * PW, r * PH)
    s.append("</svg>")
    return apply_font_stack("\n".join(s)) + "\n"


def main() -> None:
    check_geometry()
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "L19-lab-sequence.svg").write_text(build(5), encoding="utf-8")
    (OUT / "L19-lab-sequence-narrow.svg").write_text(build(2), encoding="utf-8")
    print("wrote L19-lab-sequence.svg, L19-lab-sequence-narrow.svg")


if __name__ == "__main__":
    main()
