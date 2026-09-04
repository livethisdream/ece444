#!/usr/bin/env python3
"""Generate the Poynting / plane-wave triad diagram for the L02 deck.

A transverse plane wave in isometric 3-D: E oscillates in the vertical plane
(red), H in the perpendicular depth plane (blue, foreshortened up-right), both
propagating along S (navy, to the right). Drawing H along a depth axis rather
than in-screen is what makes E perp H legible — a flat 2-D pair of sines
cannot show the perpendicularity.

No baked equations or units — those live on the slide. Text carries no
font-family, so when the file is injected inline (deck-tools.js inlineSVGs) it
inherits the deck's Source Sans Pro.

    python scripts/graphics/poynting.py
    -> writes book/extras/slides/fig/L02-poynting.svg
"""

from __future__ import annotations
import math
from pathlib import Path

OX, OY = 100.0, 210.0          # origin on the canvas
L = 540.0                      # propagation length
AE, AH = 66.0, 44.0            # E (vertical) and H (depth) amplitudes
PERIODS = 2.25
K = PERIODS * 2 * math.pi / L
DX, DY = 0.55, -0.32           # isometric depth-axis unit (H points up-right)

RED, BLUE, NAVY, GRAY = "#b01e24", "#0067b9", "#004a85", "#5a5a5a"
AXCOL = "#8a929c"              # subtle coordinate frame


def e_pt(z: float) -> tuple[float, float]:
    return (OX + z, OY - AE * math.sin(K * z))


def h_pt(z: float) -> tuple[float, float]:
    s = AH * math.sin(K * z)
    return (OX + z + s * DX, OY + s * DY)


def polyline(fn, n=170) -> str:
    pts = [fn(L * i / n) for i in range(n + 1)]
    return "M" + " L".join(f"{x:.1f} {y:.1f}" for x, y in pts), pts


def main() -> int:
    e_d, e_pts = polyline(e_pt)
    h_d, h_pts = polyline(h_pt)

    # sample vectors at the field peaks (|sin| = 1)
    arrows, tips = [], []
    n = 0
    while True:
        z = (n + 0.5) * math.pi / K
        if z > L - 8:
            break
        ex, ey = e_pt(z)
        hx, hy = h_pt(z)
        base = OX + z
        arrows.append(f'<line x1="{base:.1f}" y1="{OY:.1f}" x2="{ex:.1f}" y2="{ey:.1f}" '
                      f'stroke="{RED}" stroke-width="1.5" marker-end="url(#pE)"/>')
        arrows.append(f'<line x1="{base:.1f}" y1="{OY:.1f}" x2="{hx:.1f}" y2="{hy:.1f}" '
                      f'stroke="{BLUE}" stroke-width="1.5" marker-end="url(#pH)"/>')
        tips += [(ex, ey), (hx, hy)]
        n += 1

    # labels: first up-peak (sin = +1)
    z1 = math.pi / (2 * K)
    ex1, ey1 = e_pt(z1)
    hx1, hy1 = h_pt(z1)
    e_lbl = (ex1, ey1 - 12)
    h_lbl = (hx1 + 12, hy1 - 2)
    s_lbl = (OX + L + 16, OY + 6)
    prop_lbl = (OX + L + 16, OY + 26)

    axis = (f'<line x1="{OX-8:.1f}" y1="{OY:.1f}" x2="{OX+L+8:.1f}" y2="{OY:.1f}" '
            f'stroke="{NAVY}" stroke-width="2" marker-end="url(#pS)"/>')

    # coordinate frame at the origin: E parallel to x, H parallel to y, S
    # parallel to z — matching the slide's E = x_hat E0 cos(wt-kz), H = y_hat ...
    xax = (OX, OY - (AE + 24))                       # x: up (E direction)
    yax = (OX + (AH + 28) * DX, OY + (AH + 28) * DY)  # y: depth (H direction)
    triad = (
        f'<line x1="{OX}" y1="{OY}" x2="{xax[0]:.1f}" y2="{xax[1]:.1f}" stroke="{AXCOL}" stroke-width="1.3" marker-end="url(#pA)"/>'
        f'<line x1="{OX}" y1="{OY}" x2="{yax[0]:.1f}" y2="{yax[1]:.1f}" stroke="{AXCOL}" stroke-width="1.3" marker-end="url(#pA)"/>'
    )
    triad_lbl = (
        f'<text x="{xax[0]:.1f}" y="{xax[1]-8:.1f}" fill="{AXCOL}" font-size="14" font-style="italic" text-anchor="middle">x</text>'
        f'<text x="{yax[0]+8:.1f}" y="{yax[1]-1:.1f}" fill="{AXCOL}" font-size="14" font-style="italic">y</text>'
        f'<text x="{OX+50:.1f}" y="{OY+18:.1f}" fill="{AXCOL}" font-size="14" font-style="italic">z</text>'
    )

    # bounding box over geometry + label boxes -> viewBox with padding
    xs, ys = [], []
    for x, y in e_pts + h_pts + tips + [(OX - 8, OY), (OX + L + 8, OY), xax, yax]:
        xs.append(x); ys.append(y)
    # label extents (approx: w x 20)
    for (lx, ly), w, anc in [(e_lbl, 16, "m"), (h_lbl, 16, "s"),
                             (s_lbl, 16, "s"), (prop_lbl, 90, "s"),
                             ((xax[0], xax[1] - 8), 12, "m"),
                             ((yax[0] + 8, yax[1] - 1), 12, "s"),
                             ((OX + 50, OY + 18), 12, "s")]:
        x0 = lx - (w / 2 if anc == "m" else 0)
        xs += [x0, x0 + w]
        ys += [ly - 15, ly + 5]
    pad = 14
    vx, vy = min(xs) - pad, min(ys) - pad
    vw, vh = max(xs) - min(xs) + 2 * pad, max(ys) - min(ys) + 2 * pad

    svg = f"""<svg viewBox="{vx:.0f} {vy:.0f} {vw:.0f} {vh:.0f}" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Plane wave: E vertical, H perpendicular in depth, power flow S along propagation">
<defs>
<marker id="pE" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0 0 L10 5 L0 10 z" fill="{RED}"/></marker>
<marker id="pH" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0 0 L10 5 L0 10 z" fill="{BLUE}"/></marker>
<marker id="pS" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="8" markerHeight="8" orient="auto-start-reverse"><path d="M0 0 L10 5 L0 10 z" fill="{NAVY}"/></marker>
<marker id="pA" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse"><path d="M0 0 L10 5 L0 10 z" fill="{AXCOL}"/></marker>
</defs>
{triad}
{axis}
{chr(10).join(arrows)}
<path d="{h_d}" fill="none" stroke="{BLUE}" stroke-width="2.4" opacity="0.9"/>
<path d="{e_d}" fill="none" stroke="{RED}" stroke-width="2.6"/>
<text x="{e_lbl[0]:.1f}" y="{e_lbl[1]:.1f}" fill="{RED}" font-size="18" font-weight="700" text-anchor="middle">E</text>
<text x="{h_lbl[0]:.1f}" y="{h_lbl[1]:.1f}" fill="{BLUE}" font-size="18" font-weight="700">H</text>
<text x="{s_lbl[0]:.1f}" y="{s_lbl[1]:.1f}" fill="{NAVY}" font-size="18" font-weight="700">S</text>
<text x="{prop_lbl[0]:.1f}" y="{prop_lbl[1]:.1f}" fill="{GRAY}" font-size="12">propagation</text>
{triad_lbl}
</svg>
"""
    out = Path(__file__).resolve().parents[2] / "book/extras/slides/fig/L02-poynting.svg"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(svg, encoding="utf-8")
    print(f"wrote {out} (viewBox {vx:.0f} {vy:.0f} {vw:.0f} {vh:.0f})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
