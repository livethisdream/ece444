#!/usr/bin/env python3
"""Generate the Radar Overview 2 processing-chain figure as inline SVG.

  - overview-chain : the whole L28-L31 chain as eight boxes in two rows,
                     burst to track, each stage tagged with the lab that
                     adds it

L29-chain.svg stops at the range-Doppler map; this one carries on through
CFAR, classification, and tracking, for the overview's opening frame. Two
rows of four, so the text is still 10.5 px or more in a 343 px phone column.
Words only, no equation.

    python3 scripts/graphics/m4_overview_chain.py
"""

from __future__ import annotations

from pathlib import Path

from svg_font_stack import apply_font_stack

NAVY, RED, GREEN, AMBER, GRAY, INK = "#004a85", "#b01e24", "#1d7a4d", "#8a5a00", "#5a5a5a", "#1a1a1a"
LAB = {"L28": NAVY, "L29": RED, "L30": GREEN, "L31": AMBER}
FILL = {"L28": "#eef4fa", "L29": "#f8e3e4", "L30": "#e6f3ec", "L31": "#f6eedd", None: "#f4f5f7"}

IMG = Path(__file__).resolve().parents[2] / "book/extras/viz/img"
PHONE_COL, PX_MIN = 343.0, 10.5

W, BW, BH, GAP = 520, 108, 46, 26
FS = 17
ROWS = (
    (("burst", None), ("MTI", "L29"), ("range FFT", "L28"), ("Doppler FFT", "L29")),
    (("map", "L29"), ("CFAR", "L30"), ("classify", "L31"), ("track", "L31")),
)
Y = (10, 112)          # top of each row of boxes
TAG_DY = BH + 20       # baseline of the lab tag under a box
H = Y[1] + TAG_DY + 10

assert FS * PHONE_COL / W >= PX_MIN, "text falls under 10.5 px in a phone column"


def x_of(k: int) -> float:
    return (W - 4 * BW - 3 * GAP) / 2 + k * (BW + GAP)


def build() -> str:
    out = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" '
           f'font-family="sans-serif" font-size="{FS}">',
           '<defs><marker id="a" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" '
           f'orient="auto"><path d="M0,0 L10,5 L0,10 z" fill="{GRAY}"/></marker></defs>']
    for r, row in enumerate(ROWS):
        for k, (label, lab) in enumerate(row):
            x, y = x_of(k), Y[r]
            color = LAB.get(lab, GRAY)
            out.append(f'<rect x="{x:.1f}" y="{y}" width="{BW}" height="{BH}" rx="5" fill="{FILL[lab]}" '
                       f'stroke="{color}" stroke-width="1.6"/>')
            out.append(f'<text x="{x + BW / 2:.1f}" y="{y + BH / 2 + 6}" text-anchor="middle" fill="{INK}">{label}</text>')
            if lab:
                out.append(f'<text x="{x + BW / 2:.1f}" y="{y + TAG_DY}" text-anchor="middle" fill="{color}" '
                           f'font-weight="600">{lab} Lab</text>')
            if k:
                out.append(f'<line x1="{x - GAP + 3:.1f}" y1="{y + BH / 2}" x2="{x - 3:.1f}" y2="{y + BH / 2}" '
                           f'stroke="{GRAY}" stroke-width="1.6" marker-end="url(#a)"/>')
    # from the end of the first row down and back to the start of the second
    x_end, x_start, y_mid = x_of(3) + BW + 8, x_of(0) - 8, (Y[0] + TAG_DY + Y[1]) / 2 + 4
    out.append(f'<path d="M{x_of(3) + BW:.1f},{Y[0] + BH / 2} H{x_end:.1f} V{y_mid:.1f} H{x_start:.1f} '
               f'V{Y[1] + BH / 2} H{x_of(0) - 3:.1f}" fill="none" stroke="{GRAY}" stroke-width="1.6" '
               f'marker-end="url(#a)"/>')
    out.append("</svg>")
    return apply_font_stack("\n".join(out))


if __name__ == "__main__":
    path = IMG / "overview-chain.svg"
    path.write_text(build() + "\n", encoding="utf-8")
    print(f"wrote {path}")
