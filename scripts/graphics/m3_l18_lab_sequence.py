#!/usr/bin/env python3
"""L18 Lab: the four stages, one panel each, seen from above.

1-9    bring up      the HB100 at 0 deg on the 1 m arc; Find HB100, Calibrate
10-14  Run 1         Phase Control at zero; move the source to 0, 30, 45 deg
15-19  Run 2         the source back at 0 deg; Apply 15, 30, 45
20     reset         Phase Control back to zero for the next lab

Each panel is a top view: the eight-element row at the bottom, the arc
centered between E4 and E5, and the source positions. The view is from
above, so +theta, toward E8, is to the right, as in L18-lab-setup.svg.

One 2-by-2 layout serves both widths: beside the flow table on a laptop,
under it on a phone, where present mode gives it about 310 px. Text is 15.5
units or more on a 440-unit viewBox, so 10.9 px or more there.

    python3 scripts/graphics/m3_l18_lab_sequence.py
    -> book/extras/viz/img/L18-lab-sequence.svg
"""

from __future__ import annotations
import math
from pathlib import Path

from svg_font_stack import apply_font_stack

OUT = Path(__file__).resolve().parents[2] / "book/extras/viz/img"

NAVY, BLUE, AMBER, GRAY, INK, LIGHT = "#004a85", "#0067b9", "#8a5a00", "#5a5a5a", "#1f2a36", "#c7d2e0"

PW, PH = 220, 200                 # one panel
R1 = 92                           # the 1 m arc, in units
SQ, GAP = 9, 3                    # element squares

STAGES = [
    ("1–9", "Bring up", "Find HB100, Calibrate"),
    ("10–14", "Run 1: move", "Phase Control at 0"),
    ("15–19", "Run 2: Apply", "source back at 0°"),
    ("20", "Reset", "Phase Control to 0"),
]


def pos(cx, cy, r, deg):
    a = math.radians(deg)
    return cx + r * math.sin(a), cy - r * math.cos(a)


def pill(s, x, y, text):
    w = 12 + 10.4 * len(text)
    s.append(f'<rect x="{x:.1f}" y="{y - 12:.1f}" width="{w:.1f}" height="24" rx="12" fill="{NAVY}"/>')
    s.append(f'<text x="{x + w / 2:.1f}" y="{y + 5:.1f}" text-anchor="middle" font-size="16" '
             f'font-weight="700" fill="#ffffff">{text}</text>')
    return w


def source(s, x, y, filled=True, col=AMBER):
    fill = col if filled else "#ffffff"
    s.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="5.5" fill="{fill}" stroke="{col}" stroke-width="2"/>')


def panel(s, ox, oy, k):
    steps, title, note = STAGES[k]
    s.append(f'<rect x="{ox + 4}" y="{oy + 4}" width="{PW - 8}" height="{PH - 8}" rx="8" fill="#ffffff" '
             f'stroke="{LIGHT}" stroke-width="1.2"/>')
    w = pill(s, ox + 14, oy + 25, steps)
    s.append(f'<text x="{ox + 14 + w + 8:.1f}" y="{oy + 30}" font-size="17" font-weight="700" '
             f'fill="{INK}">{title}</text>')

    cx, cy = ox + PW / 2, oy + 160
    # the arc, -60..+60 deg, and the boresight line
    x0, y0 = pos(cx, cy, R1, -60)
    x1, y1 = pos(cx, cy, R1, 60)
    s.append(f'<path d="M {x0:.1f} {y0:.1f} A {R1} {R1} 0 0 1 {x1:.1f} {y1:.1f}" fill="none" '
             f'stroke="{LIGHT}" stroke-width="2"/>')
    xb, yb = pos(cx, cy, R1 + 12, 0)
    s.append(f'<line x1="{cx:.1f}" y1="{cy:.1f}" x2="{xb:.1f}" y2="{yb:.1f}" stroke="{LIGHT}" '
             f'stroke-width="1" stroke-dasharray="3 3"/>')
    # the array: eight elements, E1 on the left, E8 on the right (view from above)
    row = 8 * SQ + 7 * GAP
    for n in range(8):
        s.append(f'<rect x="{cx - row / 2 + n * (SQ + GAP):.1f}" y="{cy - SQ / 2:.1f}" width="{SQ}" '
                 f'height="{SQ}" rx="1.5" fill="{BLUE}" stroke="{NAVY}" stroke-width="1"/>')

    if k == 0:
        source(s, *pos(cx, cy, R1, 0))
    elif k == 1:
        for d in (0, 30, 45):
            source(s, *pos(cx, cy, R1, d))
        for d in (30, 45):
            xl, yl = pos(cx, cy, R1 + 19, d)
            s.append(f'<text x="{xl:.1f}" y="{yl + 5:.1f}" text-anchor="middle" font-size="15.5" '
                     f'fill="{AMBER}">{d}°</text>')
    elif k == 3:
        source(s, *pos(cx, cy, R1, 0))
    else:
        for d in (15, 30, 45):
            xe, ye = pos(cx, cy, R1 - 10, d)
            s.append(f'<line x1="{cx:.1f}" y1="{cy - 6:.1f}" x2="{xe:.1f}" y2="{ye:.1f}" stroke="{BLUE}" '
                     f'stroke-width="1.6" stroke-dasharray="5 3"/>')
        source(s, *pos(cx, cy, R1, 0))

    s.append(f'<text x="{cx:.1f}" y="{oy + PH - 14}" text-anchor="middle" font-size="15.5" '
             f'fill="{GRAY}">{note}</text>')


def build() -> str:
    w, h = PW * 2, PH * 2
    s = [f'<svg viewBox="0 0 {w} {h}" xmlns="http://www.w3.org/2000/svg" role="img" '
         f'aria-label="The four stages of the L18 Lab, seen from above. Steps 1 to 9: the HB100 at 0 degrees '
         f'on the 1 m arc for Find HB100 and Calibrate. Steps 10 to 14: Phase Control at zero, the source '
         f'moved to 0, 30, and 45 degrees on the arc. Steps 15 to 19: the source back at 0 degrees and the '
         f'beam commanded to 15, 30, and 45 degrees with Apply. Step 20: Phase Control reset to zero.">']
    for k in range(len(STAGES)):
        r, c = divmod(k, 2)
        panel(s, c * PW, r * PH, k)
    s.append("</svg>")
    return apply_font_stack("\n".join(s)) + "\n"


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "L18-lab-sequence.svg").write_text(build(), encoding="utf-8")
    print("wrote L18-lab-sequence.svg")


if __name__ == "__main__":
    main()
