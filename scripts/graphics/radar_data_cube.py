#!/usr/bin/env python3
"""Generate the radar data cube figure as inline SVG.

  - radar-data-cube : the samples of one burst as a cube with three axes:
                      fast time along a chirp (range), slow time across the
                      chirps (velocity), and channel, the kit's two subarrays
                      (angle)

A generic figure, not tied to one lesson's numbers: it carries words only, so
any page that names fast time, slow time, or the channel axis can show it.
Every label is 17 px in a 520 px drawing, which is 11.2 px in a 343 px phone
column, above the 10.5 px floor.

    python3 scripts/graphics/radar_data_cube.py
"""

from __future__ import annotations

from pathlib import Path

from svg_font_stack import apply_font_stack

NAVY, RED, GREEN, GRAY, INK = "#004a85", "#b01e24", "#1d7a4d", "#5a5a5a", "#1a1a1a"
FACE, SIDE, TOP, GRID = "#eef4fa", "#d7e4f1", "#e3edf6", "#b9cbdc"

IMG = Path(__file__).resolve().parents[2] / "book/extras/viz/img"
PHONE_COL, PX_MIN = 343.0, 10.5

W, H, FS = 520, 392, 17
X0, Y0, FW, FH = 78, 98, 300, 236      # the front face: fast time across, slow time down
DX, DY = 34, -22                       # one channel's step back into the page
N_CH, N_ROWS, N_COLS = 2, 8, 10

assert FS * PHONE_COL / W >= PX_MIN, "text falls under 10.5 px in a phone column"


def arrow_defs() -> str:
    out = ["<defs>"]
    for name, color in (("f", NAVY), ("s", RED), ("c", GREEN)):
        out.append(f'<marker id="{name}" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" '
                   f'orient="auto"><path d="M0,0 L10,5 L0,10 z" fill="{color}"/></marker>')
    out.append("</defs>")
    return "".join(out)


def slab(k: int) -> list[str]:
    """One channel: its front face, and the top and right faces that show behind the one in front."""
    x, y = X0 + k * DX, Y0 + k * DY
    out = [
        f'<path d="M{x},{y} l{DX},{DY} h{FW} l{-DX},{-DY} z" fill="{TOP}" stroke="{NAVY}" stroke-width="1.2"/>',
        f'<path d="M{x + FW},{y} l{DX},{DY} v{FH} l{-DX},{-DY} z" fill="{SIDE}" stroke="{NAVY}" stroke-width="1.2"/>',
        f'<rect x="{x}" y="{y}" width="{FW}" height="{FH}" fill="{FACE}" stroke="{NAVY}" stroke-width="1.4"/>',
    ]
    if k == 0:                         # the front channel shows its chirps as rows and its samples as columns
        for r in range(1, N_ROWS):
            yy = y + r * FH / N_ROWS
            out.append(f'<line x1="{x}" y1="{yy:.1f}" x2="{x + FW}" y2="{yy:.1f}" stroke="{GRID}" stroke-width="1"/>')
        for c in range(1, N_COLS):
            xx = x + c * FW / N_COLS
            out.append(f'<line x1="{xx:.1f}" y1="{y}" x2="{xx:.1f}" y2="{y + FH}" stroke="{GRID}" stroke-width="0.6"/>')
    return out


def build() -> str:
    out = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" '
           f'font-family="sans-serif" font-size="{FS}">', arrow_defs()]
    for k in reversed(range(N_CH)):    # back channel first
        out += slab(k)
    # fast time: along a chirp, under the front face
    ya = Y0 + FH + 16
    out.append(f'<line x1="{X0}" y1="{ya}" x2="{X0 + FW}" y2="{ya}" stroke="{NAVY}" stroke-width="1.8" marker-end="url(#f)"/>')
    out.append(f'<text x="{X0 + FW / 2}" y="{ya + 24}" text-anchor="middle" fill="{NAVY}">'
               f'fast time (samples in a chirp) → range</text>')
    # slow time: across the chirps, down the left of the front face
    xa = X0 - 16
    out.append(f'<line x1="{xa}" y1="{Y0}" x2="{xa}" y2="{Y0 + FH}" stroke="{RED}" stroke-width="1.8" marker-end="url(#s)"/>')
    out.append(f'<text transform="translate({xa - 12},{Y0 + FH / 2}) rotate(-90)" text-anchor="middle" fill="{RED}">'
               f'slow time (chirps) → velocity</text>')
    # channel: back into the page, along the top right edge
    xc, yc = X0 + FW + 12, Y0 - 12
    out.append(f'<line x1="{xc}" y1="{yc}" x2="{xc + N_CH * DX}" y2="{yc + N_CH * DY}" stroke="{GREEN}" '
               f'stroke-width="1.8" marker-end="url(#c)"/>')
    out.append(f'<text x="{W - 6}" y="{Y0 + N_CH * DY - 24}" text-anchor="end" fill="{GREEN}">'
               f'channel (subarrays) → angle</text>')
    out.append("</svg>")
    return apply_font_stack("\n".join(out))


if __name__ == "__main__":
    path = IMG / "radar-data-cube.svg"
    path.write_text(build() + "\n", encoding="utf-8")
    print(f"wrote {path}")
