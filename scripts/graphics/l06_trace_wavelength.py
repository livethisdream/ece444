#!/usr/bin/env python3
"""L06 lesson-page figure: what k_z = k cos(theta) is telling you.

Three panels, one line source each, with the wavefronts of a plane wave
leaving in direction theta. Along its own direction of travel the
wavefronts are lambda apart; along the source they are lambda / cos(theta)
apart, so the phase advances k cos(theta) radians per meter along z. That
rate is k_z. Broadside (theta = 90 deg) asks for none of it: the whole
source lies on one wavefront. Endfire (theta = 0) asks for the full k.

Pure SVG, same palette and font as L06-radiation-integral-geometry.svg.
This is a lesson-page figure (viz/img), so it may carry formulas.

    python scripts/graphics/l06_trace_wavelength.py
    -> book/extras/viz/img/L06-trace-wavelength.svg
"""
from __future__ import annotations
import math
from pathlib import Path

OUT = Path(__file__).resolve().parents[2] / "book/extras/viz/img/L06-trace-wavelength.svg"
NAVY, BLUE, GREEN, AMBER, INK, INK3, EDGE = "#004a85", "#0067b9", "#3f7d34", "#8a5a00", "#15202b", "#5b6573", "#cddce9"

W, H = 720, 300
KZ = '<tspan>k</tspan><tspan dy="3" font-size="9.5">z</tspan><tspan dy="-3">'   # k_z as a real subscript
PANELS = [  # theta in degrees from +z, caption lines
    (90, "broadside, θ = 90°", KZ + " = 0: the whole source</tspan>", "sits on one wavefront"),
    (60, "θ = 60°", KZ + " = k cos 60° = k/2:</tspan>", "one cycle every 2λ along the source"),
    (0,  "endfire, θ = 0°", KZ + " = k:</tspan>", "one cycle every λ along the source"),
]
LAM = 26.0          # px per wavelength
PW = W / 3          # panel width


def panel(i: int, th_deg: int, cap1: str, cap2: str, cap3: str) -> str:
    th = math.radians(th_deg)
    x0, y0 = i * PW, 0
    cx = x0 + PW * 0.42                      # z axis
    ztop, zbot = 46, 206                     # source extent on screen
    oy = (ztop + zbot) / 2                   # origin (source center)
    # direction of travel d and wavefront direction n, screen coords (y down)
    dx, dy = math.sin(th), -math.cos(th)
    nx, ny = math.cos(th), math.sin(th)
    s = [f'<g clip-path="url(#p{i})">']
    # wavefronts: (p - O) . d = m * lambda
    for m in range(-14, 15):
        qx, qy = cx + m * LAM * dx, oy + m * LAM * dy
        T = 260
        s.append(f'<line x1="{qx - T*nx:.1f}" y1="{qy - T*ny:.1f}" x2="{qx + T*nx:.1f}" y2="{qy + T*ny:.1f}" '
                 f'stroke="{BLUE}" stroke-width="1" stroke-opacity="0.45"/>')
    s.append('</g>')
    # the source: a thick segment on the z axis, and the axis arrow above it
    s.append(f'<line x1="{cx:.1f}" y1="{zbot}" x2="{cx:.1f}" y2="{ztop}" stroke="{NAVY}" stroke-width="5" stroke-linecap="round"/>')
    s.append(f'<line x1="{cx:.1f}" y1="{ztop}" x2="{cx:.1f}" y2="{ztop - 22}" stroke="{INK3}" stroke-width="1.2" marker-end="url(#twArr)"/>')
    s.append(f'<text x="{cx + 8:.1f}" y="{ztop - 14}" font-size="12" fill="{INK3}">z</text>')
    # ray: direction of travel from the source center
    L = 78
    # at endfire the ray runs along the source itself; draw it just beside it
    rx = cx + (16 if th_deg == 0 else 0)
    s.append(f'<line x1="{rx:.1f}" y1="{oy:.1f}" x2="{rx + L*dx:.1f}" y2="{oy + L*dy:.1f}" stroke="{GREEN}" stroke-width="2.2" marker-end="url(#twGrn)"/>')
    # theta arc from +z to the ray
    if th_deg > 0:
        r = 30
        ax, ay = cx, oy - r
        bx, by = cx + r * dx, oy + r * dy
        s.append(f'<path d="M{ax:.1f} {ay:.1f} A{r} {r} 0 0 1 {bx:.1f} {by:.1f}" fill="none" stroke="{INK3}" stroke-width="1.1"/>')
        mid = th / 2
        s.append(f'<text x="{cx + (r+11)*math.sin(mid):.1f}" y="{oy - (r+11)*math.cos(mid) + 4:.1f}" font-size="12.5" fill="{INK3}" text-anchor="middle">θ</text>')
    # crossings of the wavefronts with the source, and the spacing bracket
    if th_deg < 90:
        step = LAM / math.cos(th)
        ys = [oy - m * step for m in range(-6, 7) if ztop <= oy - m * step <= zbot]
        for y in ys:
            s.append(f'<line x1="{cx - 7:.1f}" y1="{y:.1f}" x2="{cx + 7:.1f}" y2="{y:.1f}" stroke="{AMBER}" stroke-width="2"/>')
        ya, yb = oy, oy - step                  # one spacing, bracketed
        bx = cx - 16
        s.append(f'<line x1="{bx}" y1="{ya:.1f}" x2="{bx}" y2="{yb:.1f}" stroke="{AMBER}" stroke-width="1.4" marker-start="url(#twAmb)" marker-end="url(#twAmb)"/>')
        lab = "λ/cos θ" if th_deg > 0 else "λ"
        s.append(f'<text x="{bx - 6}" y="{(ya + yb)/2 + 4:.1f}" font-size="12" font-weight="700" fill="{AMBER}" text-anchor="end">{lab}</text>')
    # lambda bracket along the direction of travel (first panel only, where it is
    # clearly separate from the source spacing)
    if i == 1:
        px, py = cx + 44 * dx, oy + 44 * dy
        s.append(f'<line x1="{px + 18*nx:.1f}" y1="{py + 18*ny:.1f}" x2="{px + 18*nx + LAM*dx:.1f}" y2="{py + 18*ny + LAM*dy:.1f}" '
                 f'stroke="{BLUE}" stroke-width="1.4" marker-start="url(#twBlu)" marker-end="url(#twBlu)"/>')
        s.append(f'<text x="{px + 34*nx + LAM*dx/2:.1f}" y="{py + 34*ny + LAM*dy/2 + 4:.1f}" font-size="12" font-weight="700" fill="{BLUE}" text-anchor="middle">λ</text>')
    # captions
    s.append(f'<text x="{x0 + PW/2:.1f}" y="238" font-size="12.5" font-weight="700" fill="{NAVY}" text-anchor="middle">{cap1}</text>')
    s.append(f'<text x="{x0 + PW/2:.1f}" y="258" font-size="12" fill="{INK}" text-anchor="middle">{cap2}</text>')
    s.append(f'<text x="{x0 + PW/2:.1f}" y="275" font-size="12" fill="{INK}" text-anchor="middle">{cap3}</text>')
    return "\n".join(s)


def main() -> None:
    parts = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" font-family="Inter, system-ui, -apple-system, sans-serif" role="img" '
             'aria-label="Three line sources with the wavefronts of a plane wave leaving at 90, 60, and 0 degrees from the source axis. The wavefronts are one wavelength apart along the direction of travel and one wavelength over cos theta apart along the source, so the spatial frequency along the source is k cos theta.">',
             '<defs>',
             f'<marker id="twArr" viewBox="0 0 10 10" refX="8.5" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse"><path d="M0 0 L10 5 L0 10 z" fill="{INK3}"/></marker>',
             f'<marker id="twGrn" viewBox="0 0 10 10" refX="8.5" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0 0 L10 5 L0 10 z" fill="{GREEN}"/></marker>',
             f'<marker id="twAmb" viewBox="0 0 10 10" refX="8.5" refY="5" markerWidth="5" markerHeight="5" orient="auto-start-reverse"><path d="M0 0 L10 5 L0 10 z" fill="{AMBER}"/></marker>',
             f'<marker id="twBlu" viewBox="0 0 10 10" refX="8.5" refY="5" markerWidth="5" markerHeight="5" orient="auto-start-reverse"><path d="M0 0 L10 5 L0 10 z" fill="{BLUE}"/></marker>']
    for i in range(3):
        parts.append(f'<clipPath id="p{i}"><rect x="{i*PW + 6:.1f}" y="20" width="{PW - 12:.1f}" height="200" rx="6"/></clipPath>')
    parts.append('</defs>')
    for i in range(3):
        parts.append(f'<rect x="{i*PW + 6:.1f}" y="20" width="{PW - 12:.1f}" height="200" rx="6" fill="none" stroke="{EDGE}" stroke-width="1"/>')
        parts.append(panel(i, *PANELS[i]))
    parts.append(f'<text x="{W/2}" y="296" font-size="11.5" fill="{INK3}" text-anchor="middle">blue: wavefronts, λ apart along the green direction of travel · amber: where they cross the source</text>')
    parts.append('</svg>')
    OUT.write_text("\n".join(parts) + "\n", encoding="utf-8")
    print("wrote", OUT)


if __name__ == "__main__":
    main()
