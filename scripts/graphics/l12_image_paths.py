#!/usr/bin/env python3
"""Generate the L12 source-and-image path-difference figure as inline SVG.

L12:
  - L12-image-paths : a source at height h, its image at -h, and parallel rays
                      toward a distant observer at angle theta from vertical.
                      A wavefront through the old ground point shows the source
                      ahead by h cos(theta) and the image behind by the same
                      amount, which is where the array factor's
                      exp(+-jkh cos(theta)) terms come from.

Labels only (h, theta, h cos theta); the array factor itself is in the text.

    python scripts/graphics/l12_image_paths.py
    -> writes book/extras/slides/fig/L12-image-paths.svg
              book/extras/viz/img/L12-image-paths.svg
"""

from __future__ import annotations
import math
from pathlib import Path
from svg_font_stack import apply_font_stack

NAVY, BLUE, RED, GRAY = "#004a85", "#0067b9", "#b01e24", "#5a5a5a"
RULE = "#c7d2e0"
ROOT = Path(__file__).resolve().parents[2]
OUTS = [ROOT / "book/extras/slides/fig", ROOT / "book/extras/viz/img"]

W, H = 560, 324
OX, OY = 200, 200            # old ground point (origin)
HPX = 80                     # h in pixels
TH = math.radians(40)        # observation angle from vertical
UX, UY = math.sin(TH), -math.cos(TH)   # unit vector toward the observer (screen coords)
RAY = 200                    # distance from the wavefront to where every ray stops


def pt(x, y):
    return f"{x:.1f},{y:.1f}"


def text(x, y, s, color=GRAY, size=14, anchor="middle", style=""):
    st = f' font-style="{style}"' if style else ""
    return (f'<text x="{x:.1f}" y="{y:.1f}" fill="{color}" font-size="{size}"{st} '
            f'text-anchor="{anchor}">{s}</text>')


def build() -> str:
    sx, sy = OX, OY - HPX           # source
    ix, iy = OX, OY + HPX           # image
    d = HPX * math.cos(TH)          # h cos(theta) in pixels
    fsx, fsy = sx - d * UX, sy - d * UY   # foot of source on the wavefront
    fix, fiy = ix + d * UX, iy + d * UY   # foot of image on the wavefront
    wx, wy = math.cos(TH), math.sin(TH)   # wavefront direction (perpendicular to rays)

    p = [f'<svg viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg" role="img" '
         'aria-label="A source at height h and its image at minus h radiate toward a distant '
         'observer at angle theta; measured from a wavefront through the old ground point, the '
         'source is ahead by h cos theta and the image is behind by h cos theta">',
         '<defs><marker id="l12p-ar" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" '
         'markerHeight="7" orient="auto-start-reverse"><path d="M0 0 L10 5 L0 10 z" '
         f'fill="{GRAY}"/></marker></defs>']
    # old ground plane, faint, and the vertical axis
    p.append(f'<line x1="30" y1="{OY}" x2="{W - 30}" y2="{OY}" stroke="{RULE}" '
             'stroke-width="2" stroke-dasharray="7 5"/>')
    p.append(text(40, OY - 8, "old ground plane", GRAY, 12.5, "start"))
    p.append(f'<line x1="{OX}" y1="{OY - 130}" x2="{OX}" y2="{OY + 130}" stroke="{GRAY}" '
             'stroke-width="1" stroke-dasharray="3 4"/>')
    # wavefront through the origin
    L = 150
    p.append(f'<line x1="{OX - L * wx:.1f}" y1="{OY - L * wy:.1f}" x2="{OX + L * wx:.1f}" '
             f'y2="{OY + L * wy:.1f}" stroke="{BLUE}" stroke-width="1.5" stroke-dasharray="5 4"/>')
    p.append(text(OX + (L - 6) * wx + 6, OY + (L - 6) * wy + 18, "wavefront", BLUE, 12.5, "start"))
    # parallel rays toward the observer
    # every ray stops the same distance past the wavefront, so the ends line up
    for (x, y, back, col) in ((sx, sy, d, NAVY), (OX, OY, 0, RULE), (ix, iy, -d, NAVY)):
        ln = RAY - back
        p.append(f'<line x1="{x}" y1="{y}" x2="{x + ln * UX:.1f}" y2="{y + ln * UY:.1f}" '
                 f'stroke="{col}" stroke-width="1.6" marker-end="url(#l12p-ar)"/>')
    ex, ey = ix + (RAY + d) * UX, iy + (RAY + d) * UY
    p.append(text(ex + 10, ey + 6, "to a distant observer", GRAY, 12.5, "start"))
    # the two path-difference segments
    for (x0, y0, x1, y1, lx, ly) in ((fsx, fsy, sx, sy, -26, -12), (ix, iy, fix, fiy, -50, 16)):
        p.append(f'<line x1="{x0:.1f}" y1="{y0:.1f}" x2="{x1:.1f}" y2="{y1:.1f}" '
                 f'stroke="{RED}" stroke-width="4" stroke-linecap="round"/>')
        mx, my = (x0 + x1) / 2, (y0 + y1) / 2
        p.append(text(mx + lx, my + ly, "h cos θ", RED, 14, "middle", "italic"))
    # heights
    p.append(text(OX - 14, OY - HPX / 2 + 5, "h", GRAY, 14, "end", "italic"))
    p.append(text(OX - 14, OY + HPX / 2 + 5, "h", GRAY, 14, "end", "italic"))
    # angle arc at the origin, from vertical to the ray
    r = 34
    ax, ay = OX + r * UX, OY + r * UY
    p.append(f'<path d="M {OX} {OY - r} A {r} {r} 0 0 1 {ax:.1f} {ay:.1f}" fill="none" '
             f'stroke="{GRAY}" stroke-width="1.2"/>')
    p.append(text(OX + 15, OY - r - 6, "θ", GRAY, 14, "middle", "italic"))
    # the source and the image
    p.append(f'<circle cx="{sx}" cy="{sy}" r="7" fill="{NAVY}"/>')
    p.append(f'<circle cx="{ix}" cy="{iy}" r="7" fill="#ffffff" stroke="{NAVY}" '
             'stroke-width="2" stroke-dasharray="3 2"/>')
    p.append(text(sx - 12, sy - 20, "source", NAVY, 14, "end"))
    p.append(text(ix - 16, iy + 20, "image", NAVY, 14, "end"))
    p.append("</svg>")
    return apply_font_stack("\n".join(p)) + "\n"


def main() -> None:
    svg = build()
    for d in OUTS:
        f = d / "L12-image-paths.svg"
        f.write_text(svg)
        print("wrote", f.relative_to(ROOT))


if __name__ == "__main__":
    main()
