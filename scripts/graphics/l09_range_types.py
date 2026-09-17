#!/usr/bin/env python3
"""L09: the four ways to deliver a plane wave, one small schematic each.

Neil, 2026-09-16: "for the different kind of ranges, can we add a picture or
diagram of each?" The lesson already carries a full-width drawing of the
chamber, the compact range, and the near-field scanner, but the frame that
compares all four carried only a table. These four panels are the comparison
figure: the same drawing at the same scale for each range, so the thing that
differs -- how the plane wave gets made -- is what the eye lands on.

Words in the panels are labels, not captions; the selection guidance is on
the frame beside the figure.

Two layouts from one set of drawings: a 1x4 strip for the deck and a 2x2 for
the lesson page, where the column is narrower.

    python3 scripts/graphics/l09_range_types.py
    -> book/extras/slides/fig/L09-range-types.svg     (1x4, deck)
       book/extras/viz/img/L09-range-types.svg        (2x2, lesson page)
"""

from __future__ import annotations
from pathlib import Path
from svg_font_stack import apply_font_stack

NAVY, BLUE, RED, GREEN, AMBER, GRAY = "#004a85", "#0067b9", "#b01e24", "#1d7a4d", "#8a5a00", "#5b6573"
INK, RULE, WASH, PANEL = "#15202b", "#b9d2e5", "#eaf2f9", "#f5f9fc"

ROOT = Path(__file__).resolve().parents[2]
FIG, IMG = ROOT / "book/extras/slides/fig", ROOT / "book/extras/viz/img"

# Every panel is drawn in its own 0..240 x 0..185 box and placed with a
# translate, so the two layouts share one drawing apiece.
PW, PH = 240, 185


def _t(x, y, s, size=12, fill=INK, anchor="middle", weight="400", style="normal"):
    return (f'<text x="{x}" y="{y}" font-size="{size}" fill="{fill}" '
            f'text-anchor="{anchor}" font-weight="{weight}" font-style="{style}">{s}</text>')


def _title(s):
    return _t(PW / 2, 22, s, size=15, fill=NAVY, weight="700")


def _horn(x, y, w, h, flip=False):
    """A small horn, mouth facing right (or left when flipped)."""
    d = -1 if flip else 1
    return (f'<path d="M {x} {y} L {x + d*w*0.45} {y} L {x + d*w} {y - h/2} '
            f'L {x + d*w} {y + h/2} L {x + d*w*0.45} {y} Z" '
            f'fill="#ffffff" stroke="{NAVY}" stroke-width="1.8" stroke-linejoin="round"/>')


def _dipole(x, y, h):
    return (f'<line x1="{x}" y1="{y - h}" x2="{x}" y2="{y - 4}" stroke="{INK}" stroke-width="2.6"/>'
            f'<line x1="{x}" y1="{y + 4}" x2="{x}" y2="{y + h}" stroke="{INK}" stroke-width="2.6"/>')


def panel_elevated():
    """Two towers over ground: the direct path carries the measurement, and the
    source pattern is aimed so the specular bounce misses the antenna."""
    g = [_title("Outdoor / Elevated")]
    gy = 156
    g.append(f'<rect x="14" y="{gy}" width="{PW-28}" height="16" fill="{WASH}" stroke="{RULE}" stroke-width="1"/>')
    for x in range(20, PW - 26, 13):
        g.append(f'<line x1="{x}" y1="{gy+16}" x2="{x+8}" y2="{gy+4}" stroke="{RULE}" stroke-width="1"/>')
    for x, top in ((48, 100), (196, 110)):
        g.append(f'<line x1="{x}" y1="{gy}" x2="{x}" y2="{top}" stroke="{GRAY}" stroke-width="2.4"/>')
    g.append(_horn(48, 80, 22, 26))
    g.append(_dipole(196, 80, 18))
    g.append(_t(48, 52, "source", size=11.5, fill=NAVY))
    g.append(_t(196, 52, "AUT", size=11.5, fill=INK))
    g.append(f'<line x1="74" y1="80" x2="186" y2="80" stroke="{NAVY}" stroke-width="2.4" marker-end="url(#rt-navy)"/>')
    g.append(_t(128, 70, "direct path", size=11.5, fill=NAVY, weight="600"))
    g.append(f'<path d="M 74 88 L 126 {gy} L 176 106" fill="none" stroke="{RED}" '
             f'stroke-width="1.6" stroke-dasharray="5 4"/>')
    g.append(f'<line x1="172" y1="98" x2="184" y2="110" stroke="{RED}" stroke-width="2"/>')
    g.append(f'<line x1="184" y1="98" x2="172" y2="110" stroke="{RED}" stroke-width="2"/>')
    g.append(_t(80, 134, "ground bounce", size=10.5, fill=RED))
    return g


def panel_chamber():
    """A shielded room lined with absorber; the quiet zone is the deliverable."""
    g = [_title("Anechoic Chamber")]
    x0, y0, x1, y1 = 18, 54, PW - 18, 160
    g.append(f'<rect x="{x0}" y="{y0}" width="{x1-x0}" height="{y1-y0}" fill="{PANEL}" '
             f'stroke="{GRAY}" stroke-width="2.2"/>')
    step, d = 11, 10
    tri = []
    for x in range(x0, x1 - step + 1, step):
        tri.append(f'M {x} {y0} L {x+step/2} {y0+d} L {x+step} {y0} Z')
        tri.append(f'M {x} {y1} L {x+step/2} {y1-d} L {x+step} {y1} Z')
    for y in range(y0, y1 - step + 1, step):
        tri.append(f'M {x0} {y} L {x0+d} {y+step/2} L {x0} {y+step} Z')
        tri.append(f'M {x1} {y} L {x1-d} {y+step/2} L {x1} {y+step} Z')
    g.append(f'<path d="{" ".join(tri)}" fill="{NAVY}" fill-opacity="0.34" stroke="none"/>')
    g.append(_t(PW / 2, 44, "absorber lining", size=11.5, fill=GRAY))
    g.append(_horn(48, 102, 20, 24))
    g.append(_t(58, 80, "source", size=11, fill=NAVY))
    g.append(f'<circle cx="176" cy="102" r="27" fill="{GREEN}" fill-opacity="0.13" '
             f'stroke="{GREEN}" stroke-width="1.6" stroke-dasharray="5 4"/>')
    g.append(_dipole(176, 102, 16))
    g.append(f'<line x1="72" y1="102" x2="143" y2="102" stroke="{NAVY}" '
             f'stroke-width="2.2" marker-end="url(#rt-navy)"/>')
    g.append(_t(176, 136, "quiet zone", size=10.5, fill=GREEN, weight="600"))
    return g


def panel_compact():
    """An offset paraboloid collimates the feed's spherical wave a few meters
    from the antenna: optics in place of distance."""
    g = [_title("Compact Range")]
    # offset section of a paraboloid, upper half only, opening to the right
    pts = []
    for i in range(41):
        y = 48 + i * (70 / 40)
        u = (y - 138) / 90.0
        x = 44 + 42 * u * u
        pts.append(f"{x:.1f},{y:.1f}")
    g.append(f'<polyline points="{" ".join(pts)}" fill="none" stroke="{NAVY}" stroke-width="3"/>')
    # serrated rims, top and bottom of the reflector
    g.append(f'<path d="M 86 48 l 8 -3 l -3 6 l 8 -2" fill="none" stroke="{NAVY}" stroke-width="1.8"/>')
    g.append(f'<path d="M 46 118 l 5 7 l 3 -6 l 5 7" fill="none" stroke="{NAVY}" stroke-width="1.8"/>')
    g.append(_t(18, 160, "offset reflector", size=11, fill=NAVY, anchor="start"))
    # feed below boresight, illuminating the reflector
    g.append(_horn(122, 140, 18, 22, flip=True))
    g.append(_t(128, 144, "feed", size=11, fill=NAVY, anchor="start"))
    g.append(f'<line x1="102" y1="136" x2="60" y2="114" stroke="{AMBER}" stroke-width="1.5" stroke-dasharray="4 3"/>')
    g.append(f'<line x1="102" y1="132" x2="86" y2="54" stroke="{AMBER}" stroke-width="1.5" stroke-dasharray="4 3"/>')
    # collimated wavefronts leaving the reflector
    for x in (118, 140, 162):
        g.append(f'<line x1="{x}" y1="52" x2="{x}" y2="116" stroke="{BLUE}" stroke-width="1.5" opacity="0.6"/>')
    g.append(f'<line x1="108" y1="84" x2="196" y2="84" stroke="{BLUE}" stroke-width="2.2" marker-end="url(#rt-blue)"/>')
    g.append(_t(150, 42, "plane wave", size=11.5, fill=BLUE, weight="600"))
    g.append(_dipole(206, 84, 17))
    g.append(_t(206, 122, "AUT", size=11.5, fill=INK))
    return g


def panel_nearfield():
    """A probe samples amplitude and phase a few wavelengths out; the transform
    does the rest, so the room never has to be 2D-squared-over-lambda long."""
    g = [_title("Near-Field Scanner")]
    g.append(f'<rect x="28" y="58" width="15" height="88" fill="{NAVY}" fill-opacity="0.28" '
             f'stroke="{NAVY}" stroke-width="2.2"/>')
    g.append(f'<line x1="20" y1="102" x2="28" y2="102" stroke="{NAVY}" stroke-width="2.2"/>')
    g.append(_t(36, 166, "AUT", size=11.5, fill=NAVY))
    g.append(f'<rect x="76" y="50" width="44" height="104" fill="none" stroke="{BLUE}" '
             f'stroke-width="1.6" stroke-dasharray="5 4"/>')
    for i in range(6):
        for j in range(3):
            g.append(f'<circle cx="{84 + j*14}" cy="{62 + i*16}" r="2.4" fill="{BLUE}"/>')
    g.append(_t(98, 42, "λ/2 grid", size=11.5, fill=BLUE, weight="600"))
    g.append(_t(98, 170, "amplitude, phase", size=10.5, fill=GRAY))
    g.append(f'<line x1="128" y1="102" x2="158" y2="102" stroke="{GREEN}" stroke-width="2.4" '
             f'marker-end="url(#rt-green)"/>')
    g.append(_t(143, 90, "transform", size=11, fill=GREEN, weight="600"))
    g.append(f'<path d="M 166 102 C 190 62 222 78 222 102 C 222 126 190 142 166 102 Z" '
             f'fill="{GREEN}" fill-opacity="0.16" stroke="{GREEN}" stroke-width="1.8"/>')
    g.append(_t(196, 156, "far field", size=11.5, fill=GREEN))
    return g


PANELS = (panel_elevated, panel_chamber, panel_compact, panel_nearfield)

_DEFS = f'''<defs>
<marker id="rt-navy" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6.5" markerHeight="6.5" orient="auto-start-reverse"><path d="M0 0 L10 5 L0 10 z" fill="{NAVY}"/></marker>
<marker id="rt-blue" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6.5" markerHeight="6.5" orient="auto-start-reverse"><path d="M0 0 L10 5 L0 10 z" fill="{BLUE}"/></marker>
<marker id="rt-green" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6.5" markerHeight="6.5" orient="auto-start-reverse"><path d="M0 0 L10 5 L0 10 z" fill="{GREEN}"/></marker>
</defs>'''

ALT = ("Four schematics of the ways a range delivers a plane wave: an elevated "
       "outdoor range with two towers and a ground bounce that misses the antenna, "
       "an anechoic chamber lined with absorber around a quiet zone, a compact "
       "range where an offset reflector collimates the feed, and a near-field "
       "scanner sampling amplitude and phase on a grid and transforming to the "
       "far field.")


def compose(cols, rows, scale=1.0):
    w, h = PW * cols, PH * rows
    out = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" role="img" '
           f'aria-label="{ALT}">', _DEFS,
           f'<rect x="0" y="0" width="{w}" height="{h}" fill="#ffffff"/>']
    for i, p in enumerate(PANELS):
        cx, cy = (i % cols) * PW, (i // cols) * PH
        out.append(f'<g transform="translate({cx},{cy})">')
        out.append(f'<rect x="6" y="6" width="{PW-12}" height="{PH-12}" rx="7" fill="#ffffff" '
                   f'stroke="{RULE}" stroke-width="1.4"/>')
        out.extend(p())
        out.append('</g>')
    out.append('</svg>')
    return apply_font_stack("\n".join(out))


def main():
    (FIG / "L09-range-types.svg").write_text(compose(4, 1), encoding="utf-8")
    (IMG / "L09-range-types.svg").write_text(compose(2, 2), encoding="utf-8")
    print("wrote L09-range-types.svg (1x4 deck, 2x2 page)")


if __name__ == "__main__":
    main()
