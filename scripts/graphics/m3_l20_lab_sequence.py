#!/usr/bin/env python3
"""L20 Lab: the four sweeps, one panel each.

7  E1-E8     Nd = 112 mm   the full aperture
8  E3-E6     Nd = 56 mm    half the aperture, twice the beam
9  E4, E5    Nd = 28 mm    a quarter: one broad lobe, no null
10 E1, E8    D = 98 mm     two elements spread across the row

Each panel shows the eight-element row with the active elements lit and a
thumbnail of the trace to expect: the array factor at 10.3 GHz in dBc,
clipped at the noise floor 23 dB below its own peak, over the real angles
of the sweep. The thumbnails are computed, not drawn by eye.

Two layouts, served through <picture> as the L19 Lab sequence is: a 2-by-2
grid for the half column beside the flow table on a laptop, and a shorter
2-by-2 for a phone, where the figure stacks under the table.

    python3 scripts/graphics/m3_l20_lab_sequence.py
    -> book/extras/viz/img/L20-lab-sequence.svg
       book/extras/viz/img/L20-lab-sequence-narrow.svg
"""

from __future__ import annotations
import math
from pathlib import Path

import numpy as np
from svg_font_stack import apply_font_stack

OUT = Path(__file__).resolve().parents[2] / "book/extras/viz/img"

NAVY, BLUE, AMBER, GRAY, INK, LIGHT = "#004a85", "#0067b9", "#8a5a00", "#5a5a5a", "#1f2a36", "#c7d2e0"

LAM, DEL = 3.00e8 / 10.3e9, 14e-3          # 10.3 GHz, element pitch
FLOOR = -23.0                               # dBc, below each trace's own peak
YMIN = -30.0

PW, PH = 220, 200                           # one panel
SQ, GAP = 14, 5                             # element squares

STEPS = [
    ("7", "E1–E8", [1, 1, 1, 1, 1, 1, 1, 1], "Nd = 112 mm"),
    ("8", "E3–E6", [0, 0, 1, 1, 1, 1, 0, 0], "Nd = 56 mm"),
    ("9", "E4 and E5", [0, 0, 0, 1, 1, 0, 0, 0], "Nd = 28 mm"),
    ("10", "E1 and E8", [1, 0, 0, 0, 0, 0, 0, 1], "98 mm apart"),
]


def trace_dbc(w):
    """Array factor in dBc at 10.3 GHz over -90..90 deg, clipped at the floor."""
    t = np.linspace(-90.0, 90.0, 721)
    s = np.sin(np.deg2rad(t))
    kd = 2 * math.pi * DEL / LAM
    v = sum(np.exp(1j * kd * (n - 3.5) * s) for n in range(8) if w[n])
    db = 20 * np.log10(np.maximum(np.abs(v) / sum(w), 1e-9))
    return t, np.maximum(db, FLOOR)


def panel(s, ox, oy, k, ph=PH):
    num, title, w, size = STEPS[k]
    s.append(f'<rect x="{ox + 4}" y="{oy + 4}" width="{PW - 8}" height="{ph - 8}" rx="8" fill="#ffffff" '
             f'stroke="{LIGHT}" stroke-width="1.2"/>')
    r = 12 if len(num) == 1 else 13
    s.append(f'<circle cx="{ox + 24}" cy="{oy + 25}" r="{r}" fill="{NAVY}"/>')
    s.append(f'<text x="{ox + 24}" y="{oy + 30}" text-anchor="middle" font-size="{14 if len(num) == 1 else 12.5}" '
             f'font-weight="700" fill="#ffffff">{num}</text>')
    s.append(f'<text x="{ox + 44}" y="{oy + 30}" font-size="16" font-weight="700" fill="{INK}">{title}</text>')

    # the eight-element row, active elements lit
    row_w = 8 * SQ + 7 * GAP
    x0, y0 = ox + (PW - row_w) / 2, oy + 48
    for n in range(8):
        on = bool(w[n])
        s.append(f'<rect x="{x0 + n * (SQ + GAP):.1f}" y="{y0}" width="{SQ}" height="{SQ}" rx="2" '
                 f'fill="{BLUE if on else "#ffffff"}" stroke="{NAVY if on else LIGHT}" stroke-width="1.2"/>')
    s.append(f'<text x="{ox + PW / 2}" y="{y0 + SQ + 17}" text-anchor="middle" font-size="13" '
             f'fill="{INK}">{size}</text>')

    # thumbnail of the expected trace
    bx, by, bw, bh = ox + 18, oy + 98, PW - 36, ph - 118
    s.append(f'<rect x="{bx}" y="{by}" width="{bw}" height="{bh}" fill="#f6f9fc" stroke="{LIGHT}" stroke-width="1"/>')
    fy = by + (0 - FLOOR) / (0 - YMIN) * bh
    s.append(f'<line x1="{bx}" y1="{fy:.1f}" x2="{bx + bw}" y2="{fy:.1f}" stroke="{AMBER}" stroke-width="1" '
             f'stroke-dasharray="3 3" opacity="0.8"/>')
    t, db = trace_dbc(w)
    pts = " ".join(f"{bx + (a + 90) / 180 * bw:.1f},{by + (0 - d) / (0 - YMIN) * bh:.1f}" for a, d in zip(t, db))
    s.append(f'<polyline points="{pts}" fill="none" stroke="{NAVY}" stroke-width="1.6" stroke-linejoin="round"/>')
    for a, lab in ((-90, "−90°"), (0, "0°"), (90, "90°")):
        s.append(f'<text x="{bx + (a + 90) / 180 * bw:.1f}" y="{by + bh + 12}" text-anchor="middle" '
                 f'font-size="10.5" fill="{GRAY}">{lab}</text>')


def build(cols: int, ph: int = PH) -> str:
    rows = math.ceil(len(STEPS) / cols)
    w, h = PW * cols, ph * rows
    s = [f'<svg viewBox="0 0 {w} {h}" xmlns="http://www.w3.org/2000/svg" role="img" '
         f'aria-label="The four sweeps of the L20 Lab. Step 7: E1 to E8 lit, Nd 112 mm, a narrow beam with '
         f'three sidelobe pairs. Step 8: E3 to E6, Nd 56 mm, a beam twice as wide. Step 9: E4 and E5, Nd 28 mm, '
         f'one broad lobe with no null. Step 10: E1 and E8, 98 mm apart, a narrow lobe repeated at full height. '
         f'Each thumbnail is the array factor at 10.3 GHz in dBc, clipped at the noise floor.">']
    for k in range(len(STEPS)):
        r, c = divmod(k, cols)
        panel(s, c * PW, r * ph, k, ph)
    s.append("</svg>")
    return apply_font_stack("\n".join(s)) + "\n"


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    # The laptop view sits beside the flow table, half a column wide, so it
    # is a 2-by-2 grid too; four across would shrink each thumbnail to a stamp.
    (OUT / "L20-lab-sequence.svg").write_text(build(2), encoding="utf-8")
    # The phone stack sits under the flow table, so its panels are shorter.
    (OUT / "L20-lab-sequence-narrow.svg").write_text(build(2, 166), encoding="utf-8")
    print("wrote L20-lab-sequence.svg, L20-lab-sequence-narrow.svg")


if __name__ == "__main__":
    main()
