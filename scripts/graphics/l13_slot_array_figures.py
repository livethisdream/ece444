#!/usr/bin/env python3
"""Generate the L13 slot and patch-array figures as inline SVG.

L13:
  - L13-slot-field  : the dipole and its complement, the slot, side by side.
                      The dipole's current is largest at the feed and zero at
                      its open ends; the slot's field across the gap is
                      largest at the feed and zero at its shorted ends. The
                      slot is a half-wave line shorted at both ends, the mirror
                      of the patch's line open at both ends.
  - L13-patch-array : one patch and its broad beam, beside a row of eight
                      patches on one board, each behind its own phase shifter,
                      with the narrow beam they form steered off broadside.
                      The lobes are computed: the element pattern alone, and
                      the eight-element array factor (half-wave spacing,
                      steered 20 degrees) times the same element pattern.

Schematics are not to scale. No formulas (deck figure rule), so the lesson-page
copies are the same files.

    python scripts/graphics/l13_slot_array_figures.py
    -> writes book/extras/slides/fig/L13-{slot-field,patch-array}.svg
              book/extras/viz/img/L13-{slot-field,patch-array}.svg
"""

from __future__ import annotations
import cmath
import math
from pathlib import Path
from l13_patch_figures import (NAVY, BLUE, RED, GRAY, BROWN, RULE, SUB, SUB_EDGE,
                               ROOT, OUTS, text, arrow, markers, svg)

GREEN = "#3f7d34"


# ---------------------------------------------------------------- slot vs dipole
def slot_field() -> str:
    W, H = 600, 380
    top, bot = 92, 318                      # element extent
    mid = (top + bot) / 2
    b = [markers(NAVY, BLUE, RED, GREEN, BROWN)]
    b.append(text(140, 30, "Dipole", NAVY, 23, "700"))
    b.append(text(140, 54, "metal in air", GRAY, 19))
    b.append(text(440, 30, "Slot", NAVY, 23, "700"))
    b.append(text(440, 54, "air in metal", GRAY, 19))

    # dipole: two arms, feed gap, current arrows beside the wire
    dx = 120
    b.append(f'<rect x="{dx - 6}" y="{top}" width="12" height="{mid - 7 - top}" rx="4" fill="{NAVY}"/>')
    b.append(f'<rect x="{dx - 6}" y="{mid + 7}" width="12" height="{bot - mid - 7}" rx="4" fill="{NAVY}"/>')
    b.append(f'<circle cx="{dx}" cy="{mid}" r="6" fill="#fff" stroke="{BROWN}" stroke-width="2.4"/>')
    n = 9
    for k in range(n):
        z = (k + 0.5) / n                   # 0 at the top tip, 1 at the bottom tip
        a = math.cos(math.pi * (z - 0.5))   # current: largest at the feed
        y = top + z * (bot - top)
        if abs(y - mid) < 12:
            continue
        ln = 22 * a
        if ln < 4:
            b.append(f'<circle cx="{dx + 22}" cy="{y:.1f}" r="2.2" fill="{BLUE}"/>')
            continue
        b.append(arrow(dx + 22, y + ln / 2, dx + 22, y - ln / 2, BLUE, 2.2 + a))
    b.append(text(dx + 40, top + 6, "open end:", GRAY, 18, anchor="start"))
    b.append(text(dx + 40, top + 25, "current zero", GRAY, 18, anchor="start"))
    b.append(text(dx + 40, mid + 5, "current", BLUE, 19, "700", "start"))
    b.append(text(dx + 40, mid + 25, "along the wire", BLUE, 19, "700", "start"))
    b.append(text(dx - 14, mid + 5, "feed", BROWN, 18, "700", "end"))

    # complement arrow
    b.append(f'<line x1="258" y1="{mid}" x2="318" y2="{mid}" stroke="{GREEN}" stroke-width="3" '
             f'marker-start="url(#ah-{GREEN[1:]})" marker-end="url(#ah-{GREEN[1:]})"/>')
    b.append(text(288, mid - 14, "complement", GREEN, 18, "700"))

    # slot: conducting sheet with a slit, field across the gap
    sx0, sx1 = 350, 540
    sc = (sx0 + sx1) / 2
    gap = 16
    b.append(f'<defs><pattern id="l13sl-hatch" width="10" height="10" patternUnits="userSpaceOnUse" '
             f'patternTransform="rotate(45)"><line x1="0" y1="0" x2="0" y2="10" stroke="{SUB_EDGE}" '
             f'stroke-width="1.4"/></pattern></defs>')
    b.append(f'<rect x="{sx0}" y="{top - 16}" width="{sx1 - sx0}" height="{bot - top + 32}" fill="{SUB}" '
             f'stroke="{NAVY}" stroke-width="2"/>')
    b.append(f'<rect x="{sx0}" y="{top - 16}" width="{sx1 - sx0}" height="{bot - top + 32}" fill="url(#l13sl-hatch)"/>')
    b.append(f'<rect x="{sc - gap / 2}" y="{top}" width="{gap}" height="{bot - top}" fill="#fff" '
             f'stroke="{NAVY}" stroke-width="1.6"/>')
    for k in range(n):
        z = (k + 0.5) / n
        a = math.cos(math.pi * (z - 0.5))   # field across the gap: largest at the feed
        y = top + z * (bot - top)
        if abs(y - mid) < 10:
            continue
        ln = 16 + 30 * a
        if a < 0.2:
            b.append(f'<circle cx="{sc}" cy="{y:.1f}" r="2.2" fill="{RED}"/>')
            continue
        b.append(arrow(sc - ln / 2, y, sc + ln / 2, y, RED, 2.0 + 1.2 * a))
    b.append(f'<line x1="{sc - 22}" y1="{mid}" x2="{sc + 22}" y2="{mid}" stroke="{BROWN}" stroke-width="2.6"/>')
    b.append(f'<circle cx="{sc}" cy="{mid}" r="5.5" fill="#fff" stroke="{BROWN}" stroke-width="2.4"/>')
    b.append(text(sc, bot + 42, "shorted ends: field zero", GRAY, 18))
    b.append(text(sc + 30, mid - 30, "field", RED, 19, "700", "start"))
    b.append(text(sc + 30, mid - 10, "across", RED, 19, "700", "start"))
    b.append(text(sc + 30, mid + 10, "the gap", RED, 19, "700", "start"))
    b.append(text(sc + 30, mid + 34, "feed", BROWN, 18, "700", "start"))
    return svg(W, H, "A dipole beside its complement, a slot in a conducting sheet. On the dipole the "
               "current runs along the wire, largest at the center feed and zero at the open ends. On "
               "the slot the electric field runs across the gap, largest at the center feed and zero "
               "at the ends, where the metal shorts the gap", b, "l13sl")


# ---------------------------------------------------------------- patch array
def element(t: float) -> float:
    """Broadside element pattern over a ground plane, amplitude."""
    return max(0.0, math.cos(t)) ** 0.7


def array8(t: float, steer: float) -> float:
    n, kd = 8, math.pi                     # half-wave spacing
    s = sum(cmath.exp(1j * i * kd * (math.sin(t) - math.sin(steer))) for i in range(n))
    return abs(s) / n


def lobe(cx, cy, r, fn) -> str:
    pts = []
    for i in range(361):
        t = -math.pi / 2 + math.pi * i / 360
        a = fn(t)
        pts.append(f"{cx + r * a * math.sin(t):.1f},{cy - r * a * math.cos(t):.1f}")
    return " ".join(pts)


def patch_array() -> str:
    W, H = 760, 400
    steer = math.radians(20)
    by = 250                                # board top
    b = [markers(NAVY, BLUE, RED, GREEN, GRAY)]
    b.append(f'<line x1="232" y1="16" x2="232" y2="384" stroke="{RULE}" stroke-width="1"/>')

    # one patch
    cx = 116
    b.append(text(cx, 30, "One patch", NAVY, 23, "700"))
    b.append(f'<polygon points="{lobe(cx, by - 6, 150, element)}" fill="rgba(0,103,185,0.12)" '
             f'stroke="{NAVY}" stroke-width="2.6"/>')
    b.append(f'<rect x="{cx - 60}" y="{by}" width="120" height="14" fill="{SUB}" stroke="{SUB_EDGE}"/>')
    b.append(f'<line x1="{cx - 60}" y1="{by + 14}" x2="{cx + 60}" y2="{by + 14}" stroke="{NAVY}" stroke-width="3"/>')
    b.append(f'<rect x="{cx - 16}" y="{by - 5}" width="32" height="5" fill="{RED}"/>')
    b.append(text(cx, by + 50, "broad beam", NAVY, 19, "700"))
    b.append(text(cx, by + 72, "about 6 dBi", GRAY, 18))
    b.append(text(cx, by + 94, "fixed at broadside", GRAY, 18))

    # eight patches, each behind a phase shifter
    x0, pitch = 290, 58
    xs = [x0 + i * pitch for i in range(8)]
    ax = (xs[0] + xs[-1]) / 2
    b.append(text(ax, 30, "Eight patches, one board", NAVY, 23, "700"))
    b.append(f'<line x1="{ax}" y1="{by - 8}" x2="{ax}" y2="60" stroke="{GRAY}" stroke-width="1.2" stroke-dasharray="5 4"/>')
    b.append(f'<polygon points="{lobe(ax, by - 6, 186, lambda t: array8(t, steer) * element(t))}" '
             f'fill="rgba(63,125,52,0.14)" stroke="{GREEN}" stroke-width="2.6"/>')
    # steering angle arc
    r = 96
    a0, a1 = -math.pi / 2, -math.pi / 2 + steer
    b.append(f'<path d="M{ax + r * math.cos(a0):.1f} {by - 6 + r * math.sin(a0):.1f} A {r} {r} 0 0 1 '
             f'{ax + r * math.cos(a1):.1f} {by - 6 + r * math.sin(a1):.1f}" fill="none" stroke="{GREEN}" '
             f'stroke-width="1.6" marker-end="url(#ah-{GREEN[1:]})"/>')
    b.append(text(ax - 12, 150, "steered 20°", GREEN, 18, "700", "end"))
    b.append(f'<rect x="{xs[0] - 26}" y="{by}" width="{xs[-1] - xs[0] + 52}" height="14" fill="{SUB}" stroke="{SUB_EDGE}"/>')
    b.append(f'<line x1="{xs[0] - 26}" y1="{by + 14}" x2="{xs[-1] + 26}" y2="{by + 14}" stroke="{NAVY}" stroke-width="3"/>')
    for x in xs:
        b.append(f'<rect x="{x - 16}" y="{by - 5}" width="32" height="5" fill="{RED}"/>')
        b.append(f'<line x1="{x}" y1="{by + 16}" x2="{x}" y2="{by + 34}" stroke="{BLUE}" stroke-width="2"/>')
        b.append(f'<rect x="{x - 14}" y="{by + 34}" width="28" height="24" rx="3" fill="#fff" stroke="{NAVY}" stroke-width="1.6"/>')
        b.append(text(x, by + 52, "φ", NAVY, 18, "700"))
        b.append(f'<line x1="{x}" y1="{by + 58}" x2="{x}" y2="{by + 74}" stroke="{BLUE}" stroke-width="2"/>')
    b.append(f'<line x1="{xs[0]}" y1="{by + 74}" x2="{xs[-1]}" y2="{by + 74}" stroke="{BLUE}" stroke-width="2.4"/>')
    b.append(f'<line x1="{ax}" y1="{by + 74}" x2="{ax}" y2="{by + 94}" stroke="{BLUE}" stroke-width="2.4"/>')
    b.append(text(ax, by + 114, "phase shifters, then one port", BLUE, 18, "700"))
    b.append(f'<line x1="{xs[0]}" y1="{by - 22}" x2="{xs[1]}" y2="{by - 22}" stroke="{NAVY}" stroke-width="1.4" '
             f'marker-start="url(#ah-{NAVY[1:]})" marker-end="url(#ah-{NAVY[1:]})"/>')
    b.append(text(xs[0] - 22, by - 30, "half a wavelength", NAVY, 17, "700", "start"))
    b.append(text(xs[-1] + 4, 84, "narrow beam", GREEN, 19, "700", "end"))
    return svg(W, H, "Left: one patch on a small board and its broad beam, about 6 dBi and fixed at "
               "broadside. Right: eight patches in a row on one board, half a wavelength apart, each fed "
               "through its own phase shifter into one port; together they form a narrow beam, steered "
               "off broadside by the phase shifters", b, "l13pa")


def main() -> None:
    figs = {"L13-slot-field.svg": slot_field(), "L13-patch-array.svg": patch_array()}
    for d in OUTS:
        for name, s in figs.items():
            p = d / name
            p.write_text(s)
            print("wrote", p.relative_to(ROOT))


if __name__ == "__main__":
    main()
