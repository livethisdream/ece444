#!/usr/bin/env python3
"""Generate the L12 small-loop vs resonant-loop current figure as inline SVG.

L12:
  - L12-resonant-loop : current arrows around a small loop (uniform, circulating)
                        and around a one-wavelength loop fed at the bottom,
                        where the standing wave I(s) = I0 cos(ks) goes through
                        zero a quarter of the way around and reverses sign at
                        the top. Arrow length follows |I|; arrow direction is
                        the sign of I times the counterclockwise tangent, so the
                        top and bottom currents point the same way in space.

Labels only; the current distribution itself is in the lesson text.

    python scripts/graphics/l12_resonant_loop.py
    -> writes book/extras/slides/fig/L12-resonant-loop.svg
              book/extras/viz/img/L12-resonant-loop.svg
"""

from __future__ import annotations
import math
from pathlib import Path
from svg_font_stack import apply_font_stack

NAVY, BLUE, RED, GRAY = "#004a85", "#0067b9", "#b01e24", "#5a5a5a"
RULE, WIRE = "#dbe3ee", "#9aa9bb"
ROOT = Path(__file__).resolve().parents[2]
OUTS = [ROOT / "book/extras/slides/fig", ROOT / "book/extras/viz/img"]

W, H = 560, 300
R = 82
CY = 150
ARROW = 34                    # full-length arrow at |I| = 1


def text(x, y, s, color=GRAY, size=13, anchor="middle", weight=None, style=None):
    w = f' font-weight="{weight}"' if weight else ""
    st = f' font-style="{style}"' if style else ""
    return (f'<text x="{x:.1f}" y="{y:.1f}" fill="{color}" font-size="{size}"{w}{st} '
            f'text-anchor="{anchor}">{s}</text>')


def point(cx, phi):
    """Point on the loop; phi = 0 at the bottom (the feed), increasing counterclockwise."""
    return cx + R * math.sin(phi), CY + R * math.cos(phi)


def arrow(cx, phi, amp):
    """Arrow centered on the loop at phi, along amp times the counterclockwise tangent."""
    x, y = point(cx, phi)
    tx, ty = math.cos(phi), -math.sin(phi)      # counterclockwise tangent on screen
    L = ARROW * abs(amp)
    sgn = 1 if amp >= 0 else -1
    x0, y0 = x - sgn * tx * L / 2, y - sgn * ty * L / 2
    x1, y1 = x + sgn * tx * L / 2, y + sgn * ty * L / 2
    return (f'<line x1="{x0:.1f}" y1="{y0:.1f}" x2="{x1:.1f}" y2="{y1:.1f}" stroke="{NAVY}" '
            f'stroke-width="3" stroke-linecap="round" marker-end="url(#l12r-ar)"/>')


def loop(cx):
    return (f'<circle cx="{cx}" cy="{CY}" r="{R}" fill="none" stroke="{WIRE}" stroke-width="2.5"/>'
            f'<circle cx="{cx}" cy="{CY + R}" r="5.5" fill="{RED}"/>'
            + text(cx, CY + R + 22, "feed", RED, 12.5))


def build() -> str:
    p = [f'<svg viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg" role="img" '
         'aria-label="Current around a small loop is uniform and circulates; around a '
         'one-wavelength loop fed at the bottom it falls to zero a quarter of the way around '
         'and reverses, so the currents at the top and bottom point the same way">',
         '<defs><marker id="l12r-ar" viewBox="0 0 10 10" refX="7" refY="5" markerWidth="4.5" '
         f'markerHeight="4.5" orient="auto"><path d="M0 0 L10 5 L0 10 z" fill="{NAVY}"/></marker></defs>',
         f'<line x1="{W / 2}" y1="16" x2="{W / 2}" y2="{H - 16}" stroke="{RULE}" stroke-width="1"/>']
    left, right = 140, 420
    # small loop: uniform, circulating
    p.append(text(left, 30, "Small loop, C ≪ λ", NAVY, 14.5, weight="700"))
    p.append(loop(left))
    for deg in range(30, 360, 45):
        p.append(arrow(left, math.radians(deg), 0.8))
    p.append(text(left, H - 14, "uniform current circulates"))
    # resonant loop: standing wave, I = cos(phi) with phi = ks
    p.append(text(right, 30, "Resonant loop, C = λ", NAVY, 14.5, weight="700"))
    p.append(loop(right))
    for deg in (30, 60, 120, 150, 180, 210, 240, 300, 330):
        phi = math.radians(deg)
        p.append(arrow(right, phi, math.cos(phi)))
    for deg, anchor, dx in ((90, "start", 12), (270, "end", -12)):
        x, y = point(right, math.radians(deg))
        p.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="5" fill="#ffffff" stroke="{BLUE}" stroke-width="2"/>')
        p.append(text(x + dx, y + 5, "null", BLUE, 12.5, anchor))
    p.append(text(right, H - 14, "top and bottom currents point the same way"))
    p.append("</svg>")
    return apply_font_stack("\n".join(p)) + "\n"


def main() -> None:
    svg = build()
    for d in OUTS:
        f = d / "L12-resonant-loop.svg"
        f.write_text(svg)
        print("wrote", f.relative_to(ROOT))


if __name__ == "__main__":
    main()
