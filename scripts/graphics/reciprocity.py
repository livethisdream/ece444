#!/usr/bin/env python3
"""Generate the reciprocity diagram for the L02 deck.

Two panels, same idea as a textbook reciprocity figure but drawn clean and
native to the deck. Two dipoles, A and B, each carrying its true figure-eight
pattern (|cos phi| in this plan view: broadside lobes along the link, nulls off
the wire ends):
  - Transmit:  energy flows A -> B
  - Receive:   energy flows B -> A
Both patterns are the SAME either way — that's reciprocity. The panels are
identical except for the direction of the arrow, and every lobe comes from one
shared function so they are provably identical.

No baked prose beyond the panel/flow labels; the "gain / impedance /
polarization unchanged" wording lives on the slide. Text carries no
font-family, so injected inline it inherits the deck's Source Sans Pro.

    python scripts/graphics/reciprocity.py
    -> writes book/extras/slides/fig/L02-reciprocity.svg
"""

from __future__ import annotations
import math
from pathlib import Path

R0 = 52.0
XA, XB = 86.0, 384.0
ROWS = {"Transmit": 92.0, "Receive": 252.0}
RED, BLUE, NAVY, GRAY = "#b01e24", "#0067b9", "#004a85", "#5a5a5a"


def lobe_r(phi: float) -> float:
    """Dipole field pattern, |sin(theta)| off the wire axis.

    The wire is drawn vertical, so in this plan view the pattern is |cos(phi)|
    measured from the horizontal link direction: two equal lobes pointing at the
    other antenna and away from it, with nulls straight off the wire ends.
    """
    return R0 * abs(math.cos(phi))


def lobe(cx: float, cy: float):
    pts = [(cx + lobe_r(2 * math.pi * i / 96) * math.cos(2 * math.pi * i / 96),
            cy + lobe_r(2 * math.pi * i / 96) * math.sin(2 * math.pi * i / 96)) for i in range(97)]
    return "M" + " L".join(f"{x:.1f} {y:.1f}" for x, y in pts) + " Z", pts


def dipole(cx: float, cy: float) -> str:
    return (f'<line x1="{cx}" y1="{cy-16}" x2="{cx}" y2="{cy-3}" stroke="{NAVY}" stroke-width="4" stroke-linecap="round"/>'
            f'<line x1="{cx}" y1="{cy+3}" x2="{cx}" y2="{cy+16}" stroke="{NAVY}" stroke-width="4" stroke-linecap="round"/>')


def main() -> int:
    xs, ys, body = [], [], []

    for name, cy in ROWS.items():
        body.append(f'<text x="30" y="{cy-46:.0f}" fill="{NAVY}" font-size="15" font-weight="700">{name}</text>')
        xs.append(30); ys.append(cy - 46 - 13)   # count the title's height in the bbox
        # Both antennas carry the same figure-eight — that is the whole point.
        for cx in (XA, XB):
            d, pts = lobe(cx, cy)
            for x, y in pts:
                xs.append(x); ys.append(y)
            body.append(f'<path d="{d}" fill="{BLUE}" opacity="0.15" stroke="{BLUE}" stroke-width="1.5"/>')
        body.append(dipole(XA, cy))
        body.append(dipole(XB, cy))
        body.append(f'<text x="{XA}" y="{cy+40:.0f}" fill="{GRAY}" font-size="12" text-anchor="middle">A</text>')
        body.append(f'<text x="{XB}" y="{cy+40:.0f}" fill="{GRAY}" font-size="12" text-anchor="middle">B</text>')
        xs += [XA, XB]; ys.append(cy + 40)
        if name == "Transmit":
            body.append(f'<line x1="152" y1="{cy}" x2="330" y2="{cy}" stroke="{NAVY}" stroke-width="3" marker-end="url(#txar)"/>')
            body.append(f'<text x="241" y="{cy-9:.0f}" fill="{NAVY}" font-size="13" text-anchor="middle">A → B</text>')
        else:
            body.append(f'<line x1="330" y1="{cy}" x2="152" y2="{cy}" stroke="{RED}" stroke-width="3" marker-end="url(#rxar)"/>')
            body.append(f'<text x="241" y="{cy-9:.0f}" fill="{RED}" font-size="13" text-anchor="middle">B → A</text>')

    # panel divider (the "same either way" point lives in the slide text)
    body.append('<line x1="24" y1="172" x2="452" y2="172" stroke="#dbe3ee" stroke-width="1"/>')
    xs += [24, 452]; ys += [172]

    pad = 10
    vx, vy = min(xs) - pad, min(ys) - pad
    vw, vh = max(xs) - min(xs) + 2 * pad, max(ys) - min(ys) + 2 * pad

    svg = (f'<svg viewBox="{vx:.0f} {vy:.0f} {vw:.0f} {vh:.0f}" xmlns="http://www.w3.org/2000/svg" '
           f'role="img" aria-label="Reciprocity: two dipoles with identical figure-eight patterns, drawn the same whether energy flows from A to B or from B to A">\n'
           f'<defs>'
           f'<marker id="txar" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0 0 L10 5 L0 10 z" fill="{NAVY}"/></marker>'
           f'<marker id="rxar" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0 0 L10 5 L0 10 z" fill="{RED}"/></marker>'
           f'</defs>\n' + "\n".join(body) + "\n</svg>\n")

    out = Path(__file__).resolve().parents[2] / "book/extras/slides/fig/L02-reciprocity.svg"
    out.write_text(svg, encoding="utf-8")
    print(f"wrote {out} (viewBox {vx:.0f} {vy:.0f} {vw:.0f} {vh:.0f})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
