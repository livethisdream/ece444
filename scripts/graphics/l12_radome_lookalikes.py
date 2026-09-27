#!/usr/bin/env python3
"""Generate the L12 radome look-alikes figure as inline SVG.

L12:
  - L12-radome-lookalikes : three identical fiberglass radomes, cut away to
                            show a monopole, a sleeve dipole, and a folded
                            dipole inside. Same housing, three antennas, and
                            only the first needs a ground from its mount.

Schematic, not to scale. No formulas (deck figure rule), so the lesson-page
copy is the same file.

    python scripts/graphics/l12_radome_lookalikes.py
    -> writes book/extras/slides/fig/L12-radome-lookalikes.svg
              book/extras/viz/img/L12-radome-lookalikes.svg
"""

from __future__ import annotations
from pathlib import Path
from svg_font_stack import apply_font_stack

NAVY, BLUE, RED, GRAY, BROWN = "#004a85", "#0067b9", "#b01e24", "#5a5a5a", "#8a5a00"
RULE, DOME, DOME_EDGE = "#dbe3ee", "#eef3f8", "#9aa9bb"
ROOT = Path(__file__).resolve().parents[2]
OUTS = [ROOT / "book/extras/slides/fig", ROOT / "book/extras/viz/img"]

W, H = 552, 300
CX = (92, 276, 460)             # panel centers; compact so it reads beside bullets
TOP, BOT = 52, 226              # radome extent
FEED_Y = 140                    # dipole feed point


def radome(cx: int) -> str:
    return (f'<rect x="{cx - 24}" y="{TOP}" width="48" height="{BOT - TOP}" rx="22" '
            f'fill="{DOME}" stroke="{DOME_EDGE}" stroke-width="2"/>')


def mast(cx: int) -> str:
    return (f'<rect x="{cx - 5}" y="{BOT}" width="10" height="{H - 58 - BOT}" '
            f'fill="{GRAY}" opacity="0.55"/>')


def coax(cx: int, y_top: int, dx: int = 0) -> str:
    return (f'<line x1="{cx + dx}" y1="{y_top}" x2="{cx + dx}" y2="{BOT + 8}" '
            f'stroke="{GRAY}" stroke-width="2" stroke-dasharray="4 3"/>')


def feed(cx: int, y: int) -> str:
    return f'<circle cx="{cx}" cy="{y}" r="4.5" fill="{RED}"/>'


def text(x, y, s, color=GRAY, size=12.5, weight=None, anchor="middle") -> str:
    w = f' font-weight="{weight}"' if weight else ""
    return (f'<text x="{x}" y="{y}" fill="{color}" font-size="{size}"{w} '
            f'text-anchor="{anchor}">{s}</text>')


def panel_monopole(cx: int) -> list[str]:
    return [
        radome(cx), mast(cx),
        f'<line x1="{cx}" y1="{BOT - 10}" x2="{cx}" y2="{TOP + 12}" stroke="{NAVY}" stroke-width="4" stroke-linecap="round"/>',
        coax(cx, BOT - 8, dx=0), feed(cx, BOT - 10),
        # the ground it needs, drawn as a question at the mount
        f'<line x1="{cx - 40}" y1="{BOT + 4}" x2="{cx + 40}" y2="{BOT + 4}" stroke="{BROWN}" stroke-width="2.5" stroke-dasharray="6 5"/>',
        text(cx + 12, BOT + 24, "ground?", BROWN, anchor="start"),
    ]


def panel_sleeve(cx: int) -> list[str]:
    return [
        radome(cx), mast(cx),
        f'<line x1="{cx}" y1="{FEED_Y - 4}" x2="{cx}" y2="{TOP + 12}" stroke="{NAVY}" stroke-width="4" stroke-linecap="round"/>',
        f'<rect x="{cx - 9}" y="{FEED_Y + 4}" width="18" height="{BOT - 14 - FEED_Y}" rx="2" fill="none" stroke="{BLUE}" stroke-width="3"/>',
        coax(cx, FEED_Y + 2), feed(cx, FEED_Y),
        text(cx + 30, FEED_Y + 44, "sleeve", BLUE, anchor="start"),
    ]


def panel_folded(cx: int) -> list[str]:
    g = 8  # half-spacing of the two conductors
    return [
        radome(cx), mast(cx),
        f'<rect x="{cx - g}" y="{TOP + 12}" width="{2 * g}" height="{BOT - 22 - TOP}" rx="{g}" fill="none" stroke="{NAVY}" stroke-width="3.5"/>',
        # feed gap in the left conductor
        f'<line x1="{cx - g}" y1="{FEED_Y - 5}" x2="{cx - g}" y2="{FEED_Y + 5}" stroke="{DOME}" stroke-width="6"/>',
        # feed line leaves the gap and runs down the middle, clear of both conductors
        f'<polyline points="{cx - g},{FEED_Y} {cx},{FEED_Y + 10} {cx},{BOT + 8}" fill="none" stroke="{GRAY}" stroke-width="2" stroke-dasharray="4 3"/>',
        feed(cx - g, FEED_Y),
        text(cx + 30, FEED_Y + 4, "fold", NAVY, anchor="start"),
    ]


def build() -> str:
    parts = [f'<svg viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg" role="img" '
             'aria-label="Three identical radomes cut away: a monopole that needs a ground '
             'from its mount, a sleeve dipole whose sleeve is its lower half, and a folded '
             'dipole with both halves built in">']
    for x in (184, 368):
        parts.append(f'<line x1="{x}" y1="18" x2="{x}" y2="282" stroke="{RULE}" stroke-width="1"/>')
    titles = ("Monopole", "Sleeve dipole", "Folded dipole")
    lines1 = ("other half: the mount", "other half: the sleeve", "other half: built in")
    lines2 = ("needs a ground plane", "ground-independent", "ground-independent, 4× Z")
    colors2 = (RED, NAVY, NAVY)
    builders = (panel_monopole, panel_sleeve, panel_folded)
    for cx, t, l1, l2, c2, b in zip(CX, titles, lines1, lines2, colors2, builders):
        parts.append(text(cx, 34, t, NAVY, 14.5, "700"))
        parts += b(cx)
        parts.append(text(cx, 266, l1))
        parts.append(text(cx, 284, l2, c2, weight="700"))
    parts.append("</svg>")
    return apply_font_stack("\n".join(parts)) + "\n"


def main() -> None:
    svg = build()
    for d in OUTS:
        p = d / "L12-radome-lookalikes.svg"
        p.write_text(svg)
        print("wrote", p.relative_to(ROOT))


if __name__ == "__main__":
    main()
