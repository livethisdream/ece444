#!/usr/bin/env python3
"""L11: the chamber range as it is actually cabled.

The lab moved onto the USAFA chamber and its dashboard (2026-09-17), and the
old drawing was a bench range: a transmitter on one side, a receiver on the
other, and an absorber block on the floor bounce. None of those three things
is what a student now stands in front of. One VNA is both ends, the room is
lined rather than patched, and the axis is a turntable the software drives in
step with the sweep -- so the picture has to show one instrument, two cables
through the wall, and the quantity that comes back, which is S21 per angle.

Deck copy only: the lesson page carries the dashboard in words and has no
room for a second figure inside its frame budget.

    python3 scripts/graphics/l11_chamber_range.py
    -> book/extras/slides/fig/L11-range-setup.svg
"""

from __future__ import annotations
from pathlib import Path
from svg_font_stack import apply_font_stack

NAVY, BLUE, RED, GREEN, AMBER, GRAY = "#004a85", "#0067b9", "#b01e24", "#1d7a4d", "#8a5a00", "#5b6573"
INK, RULE, WASH, PANEL = "#15202b", "#b9d2e5", "#eaf2f9", "#f5f9fc"

ROOT = Path(__file__).resolve().parents[2]
FIG = ROOT / "book/extras/slides/fig"

W, H = 790, 360


def _t(x, y, s, size=13, fill=INK, anchor="middle", weight="400", style="normal"):
    return (f'<text x="{x}" y="{y}" font-size="{size}" fill="{fill}" '
            f'text-anchor="{anchor}" font-weight="{weight}" font-style="{style}">{s}</text>')


def _horn(x, y, w, h, flip=False):
    """A horn with its mouth facing right, or left when flipped."""
    d = -1 if flip else 1
    return (f'<path d="M {x} {y} L {x + d*w*0.45} {y} L {x + d*w} {y - h/2} '
            f'L {x + d*w} {y + h/2} L {x + d*w*0.45} {y} Z" '
            f'fill="#ffffff" stroke="{NAVY}" stroke-width="2" stroke-linejoin="round"/>')


def chamber():
    """The room: four lined walls around a quiet zone."""
    x0, y0, x1, y1 = 40, 60, 620, 286
    g = [f'<rect x="{x0}" y="{y0}" width="{x1-x0}" height="{y1-y0}" fill="{PANEL}" '
         f'stroke="{GRAY}" stroke-width="2.4"/>']
    step, d = 20, 12
    tri = []
    for x in range(x0, x1 - step + 1, step):
        tri.append(f'M {x} {y0} L {x+step/2} {y0+d} L {x+step} {y0} Z')
        tri.append(f'M {x} {y1} L {x+step/2} {y1-d} L {x+step} {y1} Z')
    for y in range(y0, y1 - step + 1, step):
        tri.append(f'M {x0} {y} L {x0+d} {y+step/2} L {x0} {y+step} Z')
        tri.append(f'M {x1} {y} L {x1-d} {y+step/2} L {x1} {y+step} Z')
    g.append(f'<path d="{" ".join(tri)}" fill="{NAVY}" fill-opacity="0.32" stroke="none"/>')
    g.append(_t(330, 44, "absorber on every surface", size=13, fill=GRAY))
    return g


def source():
    """Fixed source horn, fed from port 1."""
    g = [_horn(92, 168, 44, 52)]
    g.append(_t(114, 118, "source horn", size=13, fill=NAVY, weight="600"))
    g.append(_t(114, 136, "fixed, known pol.", size=12, fill=GRAY))
    g.append(f'<line x1="92" y1="168" x2="62" y2="168" stroke="{INK}" stroke-width="2.2"/>')
    return g


def tower():
    """The AUT on the turntable, inside the quiet zone."""
    g = [f'<circle cx="452" cy="168" r="66" fill="{GREEN}" fill-opacity="0.10" '
         f'stroke="{GREEN}" stroke-width="1.6" stroke-dasharray="6 5"/>']
    g.append(_t(452, 90, "quiet zone", size=12.5, fill=GREEN, weight="600"))
    g.append(_horn(478, 168, 40, 48, flip=True))
    g.append(_t(452, 128, "AUT", size=13, fill=INK, weight="600"))
    # the turntable under it: a column, a plate, and the sense of rotation
    g.append(f'<line x1="452" y1="192" x2="452" y2="220" stroke="{GRAY}" stroke-width="3"/>')
    g.append(f'<ellipse cx="452" cy="224" rx="46" ry="12" fill="{WASH}" '
             f'stroke="{GRAY}" stroke-width="2"/>')
    g.append(f'<path d="M 414 238 A 46 15 0 0 0 490 238" fill="none" stroke="{AMBER}" '
             f'stroke-width="2.2" marker-end="url(#l11-amber)"/>')
    g.append(_t(452, 264, "turntable, commanded per angle", size=12.5, fill=AMBER, weight="600"))
    g.append(f'<line x1="478" y1="168" x2="600" y2="168" stroke="{INK}" stroke-width="2.2"/>')
    return g


def path_and_stray():
    """The direct path that carries the measurement, and the stray that sets the floor."""
    g = [f'<line x1="136" y1="168" x2="428" y2="168" stroke="{NAVY}" stroke-width="3" '
         f'marker-end="url(#l11-navy)"/>']
    g.append(_t(282, 156, "direct path", size=13.5, fill=NAVY, weight="700"))
    g.append(_t(282, 190, "measure the separation", size=12, fill=GRAY))
    g.append(f'<path d="M 140 184 C 232 244 320 244 414 190" fill="none" stroke="{RED}" '
             f'stroke-width="1.8" stroke-dasharray="6 5"/>')
    g.append(_t(228, 262, "stray field: absorbed, not removed", size=12, fill=RED))
    return g


def instrument():
    """One VNA, two ports, and the software that drives the pair."""
    g = [f'<rect x="632" y="128" width="126" height="104" rx="7" fill="#ffffff" '
         f'stroke="{NAVY}" stroke-width="2.4"/>']
    g.append(_t(695, 152, "VNA", size=14.5, fill=NAVY, weight="700"))
    g.append(f'<rect x="648" y="162" width="94" height="34" fill="{WASH}" stroke="{RULE}" stroke-width="1.2"/>')
    g.append(f'<path d="M 652 188 C 664 188 668 170 678 170 C 690 170 692 190 700 190 '
             f'C 712 190 714 172 738 172" fill="none" stroke="{BLUE}" stroke-width="1.8"/>')
    g.append(_t(695, 214, "port 1 out, port 2 in", size=11.5, fill=GRAY))
    # the two cables, drawn as the walls they pass through
    g.append(f'<path d="M 632 176 L 614 176 L 614 168 L 600 168" fill="none" stroke="{INK}" stroke-width="2.2"/>')
    g.append(f'<path d="M 632 190 L 626 190 L 626 330 L 62 330 L 62 168" fill="none" '
             f'stroke="{INK}" stroke-width="2.2"/>')
    g.append(f'<rect x="632" y="250" width="126" height="56" rx="7" fill="{PANEL}" '
             f'stroke="{GRAY}" stroke-width="2"/>')
    g.append(_t(695, 272, "dashboard", size=13, fill=INK, weight="600"))
    g.append(_t(695, 291, "sweep, grid, run", size=11.5, fill=GRAY))
    g.append(f'<line x1="695" y1="232" x2="695" y2="250" stroke="{GRAY}" stroke-width="1.8" '
             f'stroke-dasharray="4 3"/>')
    g.append(_t(695, 120, "S21 per angle", size=13, fill=BLUE, weight="600"))
    return g


_DEFS = f'''<defs>
<marker id="l11-navy" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0 0 L10 5 L0 10 z" fill="{NAVY}"/></marker>
<marker id="l11-amber" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0 0 L10 5 L0 10 z" fill="{AMBER}"/></marker>
</defs>'''

ALT = ("The chamber range: a room lined with absorber on every surface, a fixed "
       "source horn on the left fed from the analyzer's port 1, the antenna under "
       "test on a turntable inside the quiet zone and cabled back to port 2, the "
       "direct path between them, a stray path absorbed by the lining, and one "
       "analyzer outside the chamber driven by the dashboard, recording S21 at "
       "every commanded angle.")


def compose():
    out = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" '
           f'width="{W}" height="{H}" role="img" aria-label="{ALT}">', _DEFS,
           f'<rect x="0" y="0" width="{W}" height="{H}" fill="#ffffff"/>']
    for part in (chamber, path_and_stray, source, tower, instrument):
        out.extend(part())
    out.append('</svg>')
    return apply_font_stack("\n".join(out))


def main():
    (FIG / "L11-range-setup.svg").write_text(compose(), encoding="utf-8")
    print("wrote L11-range-setup.svg (deck)")


if __name__ == "__main__":
    main()
