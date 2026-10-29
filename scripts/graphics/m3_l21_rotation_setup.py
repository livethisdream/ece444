#!/usr/bin/env python3
"""L21 Lab: the rotation setup, seen from above.

The HB100 stays on its tripod 1.2 m out; the kit turns about the center of
the array on its rotating stand (phaser repo, hardware/stand-simple). The
figure pins down the sign convention: turning the kit's face toward E1 puts
the source on the E8 side of the array normal, at +theta. The stand's scale
is engraved on the fixed base and counts clockwise seen from above
(phaser_stand_simple.scad), while that turn is counterclockwise, so the
pointer reads -theta.

    python3 scripts/graphics/m3_l21_rotation_setup.py
    -> writes book/extras/viz/img/L21-rotation-setup.svg
"""

from __future__ import annotations
import math
from pathlib import Path

from svg_font_stack import apply_font_stack

OUT = Path(__file__).resolve().parents[2] / "book/extras/viz/img/L21-rotation-setup.svg"

NAVY, MID, RED, GRAY, INK = "#004a85", "#0067b9", "#b01e24", "#5a5a5a", "#1f2a36"
W, H = 640, 445
CX, CY = 320, 330          # rotation axis = array center
SY = 62                    # source y (straight up from the axis)
THETA = 30.0               # drawn rotation, degrees
R_PRO = 120                # radius of the stand's scale


def pt(r, ang_deg):
    """Point at radius r, angle measured from 'up' toward screen-left (+)."""
    a = math.radians(ang_deg)
    return CX - r * math.sin(a), CY - r * math.cos(a)


def main() -> None:
    s = [f'<svg viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg" role="img" '
         f'aria-label="Top view of the rotation setup: the HB100 fixed 1.2 m from the array, '
         f'and the kit turned 30 degrees about the array center on its rotating stand, its face '
         f'toward E1, which puts the source at plus 30 degrees on the E8 side while the '
         f'pointer on the stand scale reads minus 30">']
    s.append('<defs><marker id="l21rArr" viewBox="0 0 10 10" refX="8.5" refY="5" markerWidth="6.5" '
             f'markerHeight="6.5" orient="auto-start-reverse"><path d="M0 0 L10 5 L0 10 z" fill="{GRAY}"/></marker>'
             '<marker id="l21rNav" viewBox="0 0 10 10" refX="8.5" refY="5" markerWidth="6.5" '
             f'markerHeight="6.5" orient="auto-start-reverse"><path d="M0 0 L10 5 L0 10 z" fill="{NAVY}"/></marker></defs>')

    # the stand's scale, on the fixed base: + clockwise seen from above (screen-right),
    # so the E1 side the face turns toward is the minus side
    x0, y0 = pt(R_PRO, 90)
    x1, y1 = pt(R_PRO, -90)
    s.append(f'<path d="M{x0:.1f} {y0:.1f} A{R_PRO} {R_PRO} 0 0 1 {x1:.1f} {y1:.1f}" fill="#eef4fa" '
             f'stroke="{GRAY}" stroke-width="1.2"/>')
    for a in range(-90, 91, 10):
        r_in = R_PRO - (12 if a % 30 == 0 else 6)
        xa, ya = pt(R_PRO, a)
        xb, yb = pt(r_in, a)
        s.append(f'<line x1="{xa:.1f}" y1="{ya:.1f}" x2="{xb:.1f}" y2="{yb:.1f}" stroke="{GRAY}" stroke-width="1"/>')
        if a % 30 == 0:
            xl, yl = pt(R_PRO + 16, a)
            lab = "0°" if a == 0 else f"{-a:+d}°".replace("-", "−")
            if a == 0:          # clear of the dashed line of sight
                xl += 14
            s.append(f'<text x="{xl:.1f}" y="{yl + 4:.1f}" text-anchor="middle" font-size="12" fill="{GRAY}">{lab}</text>')

    # line of sight to the fixed source, with the 1.2 m dimension
    s.append(f'<line x1="{CX}" y1="{CY}" x2="{CX}" y2="{SY + 10}" stroke="{RED}" stroke-width="1.4" stroke-dasharray="6 4"/>')
    s.append(f'<circle cx="{CX}" cy="{SY}" r="8" fill="{RED}"/>')
    s.append(f'<text x="{CX}" y="{SY - 16}" text-anchor="middle" font-size="13" font-weight="700" fill="{RED}">HB100, fixed on its tripod</text>')
    dx = CX + 195
    s.append(f'<line x1="{dx}" y1="{SY}" x2="{dx}" y2="{CY}" stroke="{GRAY}" stroke-width="1.2" '
             'marker-start="url(#l21rArr)" marker-end="url(#l21rArr)"/>')
    s.append(f'<line x1="{CX + 12}" y1="{SY}" x2="{dx + 6}" y2="{SY}" stroke="{GRAY}" stroke-width="0.8" stroke-dasharray="2 3"/>')
    s.append(f'<text x="{dx + 8}" y="{(SY + CY) / 2 - 60:.0f}" font-size="13" fill="{INK}">1.2 m</text>')

    # the kit, turned THETA toward E1 (screen-left): element row perpendicular to its normal
    n = math.radians(THETA)
    ux, uy = math.cos(n), -math.sin(n)          # along the row, toward E8 (screen-right at 0)
    for i in range(8):
        off = (i - 3.5) * 13
        ex, ey = CX + off * ux, CY + off * uy
        s.append(f'<rect x="{ex - 4.5:.1f}" y="{ey - 6:.1f}" width="9" height="12" rx="1.5" fill="{NAVY}" '
                 f'transform="rotate({-THETA} {ex:.1f} {ey:.1f})"/>')
    e1x, e1y = CX - 62 * ux, CY - 62 * uy
    e8x, e8y = CX + 62 * ux, CY + 62 * uy
    s.append(f'<text x="{e1x - 22:.1f}" y="{e1y + 6:.1f}" text-anchor="middle" font-size="13" font-weight="700" fill="{NAVY}">E1</text>')
    s.append(f'<text x="{e8x + 12:.1f}" y="{e8y + 20:.1f}" text-anchor="middle" font-size="13" font-weight="700" fill="{NAVY}">E8</text>')

    # the kit's normal, which is also the platter's pointer on the scale
    nx, ny = pt(R_PRO - 2, THETA)
    s.append(f'<line x1="{CX}" y1="{CY}" x2="{nx:.1f}" y2="{ny:.1f}" stroke="{NAVY}" stroke-width="2" marker-end="url(#l21rNav)"/>')
    tx, ty = pt(R_PRO + 34, THETA + 8)
    s.append(f'<text x="{tx - 6:.1f}" y="{ty:.1f}" text-anchor="end" font-size="12" fill="{NAVY}">array normal</text>')
    s.append(f'<text x="{tx - 6:.1f}" y="{ty + 15:.1f}" text-anchor="end" font-size="12" fill="{NAVY}">(pointer reads −30°)</text>')

    # theta between the normal and the line to the source
    ra = 62
    ax0, ay0 = pt(ra, THETA)
    ax1, ay1 = pt(ra, 0)
    s.append(f'<path d="M{ax0:.1f} {ay0:.1f} A{ra} {ra} 0 0 1 {ax1:.1f} {ay1:.1f}" fill="none" stroke="{INK}" stroke-width="1.2"/>')
    lx, ly = pt(ra + 14, THETA / 2)
    s.append(f'<text x="{lx:.1f}" y="{ly + 4:.1f}" text-anchor="middle" font-size="14" font-style="italic" fill="{INK}">θ</text>')

    # rotation axis
    s.append(f'<circle cx="{CX}" cy="{CY}" r="3" fill="#fff" stroke="{INK}" stroke-width="1.2"/>')
    s.append(f'<text x="{CX}" y="{CY + 92}" text-anchor="middle" font-size="12" fill="{INK}">face toward E1: the source sits at +θ, on the E8 side; the stand reads −θ</text>')
    s.append('</svg>')
    OUT.write_text(apply_font_stack("\n".join(s)) + "\n")
    print(f"wrote {OUT}")


if __name__ == "__main__":
    main()
