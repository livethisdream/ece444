#!/usr/bin/env python3
"""Generate the L03 polarization diagrams for the deck.

Four native SVGs, drawn to the deck's palette with live <text> that carries no
font-family, so injected inline (deck-tools.js) they inherit Source Sans Pro:

  - pol-states       : the three states as E-tip loci (line / circle / ellipse)
  - pol-construction : two linear components + relative phase -> resultant trace
  - handedness       : IEEE right/left hand, viewed along the propagation axis
  - axial-ratio      : the polarization ellipse, major/minor axes, tilt angle

No equations are baked in — those live in the slide text. Labels only.

    python scripts/graphics/polarization.py
    -> writes book/extras/slides/fig/{L03-pol-states,L03-pol-construction,L03-handedness,
                                      L03-axial-ratio}.svg

Handedness note: the figure is drawn from the *temporal* IEEE definition (how E
rotates at a fixed point, looking along the direction of propagation), NOT the
fixed-time spatial helix — the two have opposite screw sense, and the temporal
one is what the convention and the slide actually state.
"""

from __future__ import annotations
import math
import re
from pathlib import Path

NAVY, BLUE, RED, GREEN, GRAY = "#004a85", "#0067b9", "#b01e24", "#1d7a4d", "#5a5a5a"
INK, RULE = "#1a1a1a", "#c7d2e0"
OUT = Path(__file__).resolve().parents[2] / "book/extras/slides/fig"

MARKERS = {"navy": NAVY, "blue": BLUE, "red": RED, "gray": GRAY, "ink": INK, "green": GREEN}
TAU = 2 * math.pi


def defs() -> str:
    m = "".join(
        f'<marker id="ar-{k}" viewBox="0 0 10 10" refX="9" refY="5" '
        f'markerWidth="6" markerHeight="6" orient="auto-start-reverse">'
        f'<path d="M0 0 L10 5 L0 10 z" fill="{v}"/></marker>'
        for k, v in MARKERS.items())
    return f"<defs>{m}</defs>"


def d_of(pts, close: bool = False) -> str:
    return "M" + " L".join(f"{x:.1f} {y:.1f}" for x, y in pts) + (" Z" if close else "")


class Fig:
    """Element accumulator that tracks a bounding box, so every figure ships a
    tight viewBox and scales to whatever column the slide gives it."""

    def __init__(self) -> None:
        self.body: list[str] = []
        self.xs: list[float] = []
        self.ys: list[float] = []

    def mark(self, *pts) -> None:
        for x, y in pts:
            self.xs.append(x)
            self.ys.append(y)

    def add(self, el: str, *pts) -> None:
        self.body.append(el)
        self.mark(*pts)

    def text(self, x, y, s, fill=INK, size=14, anchor="middle", weight="400", opacity=None) -> None:
        op = f' opacity="{opacity}"' if opacity is not None else ""
        self.add(f'<text x="{x:.1f}" y="{y:.1f}" fill="{fill}" font-size="{size}" '
                 f'text-anchor="{anchor}" font-weight="{weight}"{op}>{s}</text>')
        w = 0.58 * size * len(re.sub(r"<[^>]+>", "", s))
        dx = {"middle": w / 2, "start": 0.0, "end": w}[anchor]
        self.mark((x - dx, y - size), (x - dx + w, y + 0.3 * size))

    def vec(self, cx, cy, x, y, key="navy", width=2.6, opacity=1.0, gap=0.0) -> None:
        """E-field arrow from a panel origin, in math coords (y up). `gap` insets
        the tail so the arrows don't bury a symbol sitting at the origin."""
        n = math.hypot(x, y) or 1.0
        x0, y0 = cx + gap * x / n, cy - gap * y / n
        self.add(f'<line x1="{x0:.1f}" y1="{y0:.1f}" x2="{cx + x:.1f}" y2="{cy - y:.1f}" '
                 f'stroke="{MARKERS[key]}" stroke-width="{width}" opacity="{opacity}" '
                 f'marker-end="url(#ar-{key})"/>',
                 (x0, y0), (cx + x, cy - y))

    def arc_arrow(self, cx, cy, r, a0, a1, key="gray", width=2.0, ccw=True) -> None:
        """Arrowed circular arc, angles in degrees, math convention (ccw positive)."""
        x0, y0 = cx + r * math.cos(math.radians(a0)), cy - r * math.sin(math.radians(a0))
        x1, y1 = cx + r * math.cos(math.radians(a1)), cy - r * math.sin(math.radians(a1))
        self.add(f'<path d="M{x0:.1f} {y0:.1f} A{r:.1f} {r:.1f} 0 0 {0 if ccw else 1} '
                 f'{x1:.1f} {y1:.1f}" fill="none" stroke="{MARKERS[key]}" '
                 f'stroke-width="{width}" marker-end="url(#ar-{key})"/>',
                 (cx - r, cy - r), (cx + r, cy + r))

    def axes(self, cx, cy, r, label=True, size=13) -> None:
        """Light x/y cross for a transverse-plane panel."""
        self.add(f'<line x1="{cx - r:.1f}" y1="{cy}" x2="{cx + r:.1f}" y2="{cy}" '
                 f'stroke="{RULE}" stroke-width="1.2"/>', (cx - r, cy), (cx + r, cy))
        self.add(f'<line x1="{cx}" y1="{cy - r:.1f}" x2="{cx}" y2="{cy + r:.1f}" '
                 f'stroke="{RULE}" stroke-width="1.2"/>', (cx, cy - r), (cx, cy + r))
        if label:
            self.text(cx + r + 8, cy + 4, "x", GRAY, size, "start")
            # beside the axis tip, not on top of it — the top of the panel is
            # where the rotation-sense arc reads most clearly
            self.text(cx + 8, cy - r + 3, "y", GRAY, size, "start")

    def write(self, name: str, aria: str, pad: float = 12.0) -> None:
        vx, vy = min(self.xs) - pad, min(self.ys) - pad
        vw = max(self.xs) - min(self.xs) + 2 * pad
        vh = max(self.ys) - min(self.ys) + 2 * pad
        svg = (f'<svg viewBox="{vx:.0f} {vy:.0f} {vw:.0f} {vh:.0f}" '
               f'xmlns="http://www.w3.org/2000/svg" role="img" aria-label="{aria}">\n'
               f'{defs()}\n' + "\n".join(self.body) + "\n</svg>\n")
        OUT.mkdir(parents=True, exist_ok=True)
        (OUT / f"{name}.svg").write_text(svg, encoding="utf-8")
        print(f"wrote {OUT / (name + '.svg')} (viewBox {vx:.0f} {vy:.0f} {vw:.0f} {vh:.0f})")


# --------------------------------------------------------------------------
# 1. The three polarization states, as E-tip loci
# --------------------------------------------------------------------------
def pol_states() -> None:
    f = Fig()
    R, cy = 48.0, 96.0
    centers = [96.0, 268.0, 440.0]
    names = ["Linear", "Circular", "Elliptical"]

    for cx, name in zip(centers, names):
        f.axes(cx, cy, R + 14, label=False)

        if name == "Linear":
            a = math.radians(45.0)
            ex, ey = R * math.cos(a), R * math.sin(a)
            # locus drawn slightly past the arrow tips so the blue reads as the
            # locus, matching the circle/ellipse panels
            f.add(f'<line x1="{cx - 1.18 * ex:.1f}" y1="{cy + 1.18 * ey:.1f}" '
                  f'x2="{cx + 1.18 * ex:.1f}" y2="{cy - 1.18 * ey:.1f}" '
                  f'stroke="{BLUE}" stroke-width="3.0" stroke-linecap="round"/>',
                  (cx - 1.18 * ex, cy + 1.18 * ey), (cx + 1.18 * ex, cy - 1.18 * ey))
            # E oscillates back and forth along that line
            for frac, op in ((1.0, 1.0), (0.55, 0.5), (-0.8, 0.28)):
                f.vec(cx, cy, frac * ex, frac * ey, "navy", 2.6, op)
        else:
            b = 0.46 if name == "Elliptical" else 1.0
            tilt = math.radians(28.0) if name == "Elliptical" else 0.0
            pts = []
            for i in range(97):
                t = TAU * i / 96
                u, v = R * math.cos(t), R * b * math.sin(t)
                x = u * math.cos(tilt) - v * math.sin(tilt)
                y = u * math.sin(tilt) + v * math.cos(tilt)
                pts.append((cx + x, cy - y))
            f.add(f'<path d="{d_of(pts, True)}" fill="{BLUE}" fill-opacity="0.08" '
                  f'stroke="{BLUE}" stroke-width="2.6"/>', *pts)
            # opacity encodes time (faint = earlier), so the arrows and the arc
            # must agree; both run counter-clockwise, as pol-construction does
            for t_deg, op in ((25.0, 0.28), (85.0, 0.5), (145.0, 1.0)):
                t = math.radians(t_deg)
                u, v = R * math.cos(t), R * b * math.sin(t)
                x = u * math.cos(tilt) - v * math.sin(tilt)
                y = u * math.sin(tilt) + v * math.cos(tilt)
                f.vec(cx, cy, x, y, "navy", 2.6, op)
            f.arc_arrow(cx, cy, R + 20, 62, 118, "gray", 1.8, ccw=True)

        f.text(cx, cy + R + 48, name, NAVY, 16, "middle", "700")

    f.text(sum(centers) / 3, cy + R + 74, "tip of E over one period, at a fixed point",
           GRAY, 13.5)
    f.write("L03-pol-states",
            "Three polarization states: the electric-field tip traces a line, "
            "a circle, or an ellipse over one period")


# --------------------------------------------------------------------------
# 2. Two linear components + relative phase -> any polarization
# --------------------------------------------------------------------------
def pol_construction() -> None:
    f = Fig()
    AX, AY = 1.0, 0.72              # component amplitudes
    DELTA = math.radians(-60.0)     # relative phase of Ey
    W, AMP = 268.0, 34.0            # waveform box width, amplitude in px
    x0, y0 = 0.0, 66.0              # waveform origin (y0 = zero line)

    # --- component waveforms, one period plus a little ---
    f.add(f'<line x1="{x0}" y1="{y0}" x2="{x0 + W:.1f}" y2="{y0}" '
          f'stroke="{RULE}" stroke-width="1.2"/>', (x0, y0), (x0 + W, y0))
    f.text(x0 + W + 8, y0 + 5, "ωt", GRAY, 13, "start")

    for amp, phase, color, key in ((AX, 0.0, BLUE, "blue"), (AY, DELTA, RED, "red")):
        pts = [(x0 + W * i / 240, y0 - AMP * amp * math.cos(TAU * (1.15 * i / 240) + phase))
               for i in range(241)]
        f.add(f'<path d="{d_of(pts)}" fill="none" stroke="{color}" stroke-width="2.4"/>', *pts)

    f.text(x0 + 6, y0 - AMP * AX - 10, "E<tspan font-size=\"10\" dy=\"4\">x</tspan>",
           BLUE, 15, "start", "700")
    # Ey peaks a fraction -DELTA/2pi of a period after Ex
    t_ey = (-DELTA / TAU) / 1.15
    f.text(x0 + W * t_ey + 6, y0 - AMP * AY - 10,
           "E<tspan font-size=\"10\" dy=\"4\">y</tspan>", RED, 15, "start", "700")

    # --- the relative phase, marked between the two peaks ---
    y_d = y0 - AMP - 30
    f.add(f'<line x1="{x0:.1f}" y1="{y_d:.1f}" x2="{x0 + W * t_ey:.1f}" y2="{y_d:.1f}" '
          f'stroke="{GRAY}" stroke-width="1.8" marker-start="url(#ar-gray)" '
          f'marker-end="url(#ar-gray)"/>', (x0, y_d), (x0 + W * t_ey, y_d))
    for x_tick in (x0, x0 + W * t_ey):
        f.add(f'<line x1="{x_tick:.1f}" y1="{y_d:.1f}" x2="{x_tick:.1f}" y2="{y0 - AMP * 0.55:.1f}" '
              f'stroke="{RULE}" stroke-width="1.1" stroke-dasharray="3 3"/>',
              (x_tick, y_d), (x_tick, y0))
    f.text(x0 + W * t_ey / 2, y_d - 8, "δ", GRAY, 16, "middle", "700")

    # --- resultant locus ---
    cx, cy, S = x0 + W / 2, y0 + 152.0, 52.0
    f.axes(cx, cy, S + 20)
    pts = [(cx + S * AX * math.cos(TAU * i / 96),
            cy - S * AY * math.cos(TAU * i / 96 + DELTA)) for i in range(97)]
    f.add(f'<path d="{d_of(pts, True)}" fill="{BLUE}" fill-opacity="0.08" '
          f'stroke="{NAVY}" stroke-width="2.6"/>', *pts)
    t = TAU * 0.07
    f.vec(cx, cy, S * AX * math.cos(t), S * AY * math.cos(t + DELTA), "navy", 2.6)
    # With Ey lagging Ex (DELTA < 0) this locus is traced counter-clockwise:
    # at wt=0 the tip is at (1, 0.36) and moves to (0.87, 0.62). Placed upper-left
    # so it clears the y-axis label and the wt=0 E-vector.
    f.arc_arrow(cx, cy, S + 8, 55, 125, "gray", 1.8, ccw=True)
    f.text(cx, cy + S + 52, "resultant trace", NAVY, 15, "middle", "700")

    f.write("L03-pol-construction",
            "Two orthogonal linear components with a relative phase delta combine "
            "into an elliptical resultant trace")


# --------------------------------------------------------------------------
# 3. IEEE handedness, viewed along the propagation direction
# --------------------------------------------------------------------------
def handedness() -> None:
    f = Fig()
    R, cy = 50.0, 108.0
    # thumb along propagation (into the page) -> right-hand fingers curl
    # clockwise from the reader's side; left-hand is the mirror image
    panels = [(108.0, "Right-hand", [160.0, 70.0, -20.0], False),
              (326.0, "Left-hand", [20.0, 110.0, 200.0], True)]

    for cx, name, angles, ccw in panels:
        f.add(f'<circle cx="{cx}" cy="{cy}" r="{R}" fill="none" stroke="{RULE}" '
              f'stroke-width="1.4"/>', (cx - R, cy - R), (cx + R, cy + R))
        # propagation into the page
        f.add(f'<circle cx="{cx}" cy="{cy}" r="8" fill="none" stroke="{GRAY}" stroke-width="1.6"/>'
              f'<line x1="{cx - 5.7:.1f}" y1="{cy - 5.7:.1f}" x2="{cx + 5.7:.1f}" '
              f'y2="{cy + 5.7:.1f}" stroke="{GRAY}" stroke-width="1.6"/>'
              f'<line x1="{cx - 5.7:.1f}" y1="{cy + 5.7:.1f}" x2="{cx + 5.7:.1f}" '
              f'y2="{cy - 5.7:.1f}" stroke="{GRAY}" stroke-width="1.6"/>')

        for a_deg, op, lab in zip(angles, (0.3, 0.58, 1.0), ("t₁", "t₂", "t₃")):
            a = math.radians(a_deg)
            f.vec(cx, cy, R * math.cos(a), R * math.sin(a), "navy", 2.6, op, gap=11.0)
            f.text(cx + (R + 15) * math.cos(a), cy - (R + 15) * math.sin(a) + 5,
                   lab, NAVY, 13.5, "middle", "700", opacity=op)

        span = (135.0, 45.0) if not ccw else (45.0, 135.0)
        f.arc_arrow(cx, cy, R + 32, span[0], span[1], "red", 2.2, ccw=ccw)
        f.text(cx, cy + R + 34, name, NAVY, 16, "middle", "700")

    f.text((108.0 + 326.0) / 2, cy + R + 58,
           "viewed looking along the propagation direction", GRAY, 13.5)
    f.write("L03-handedness",
            "IEEE handedness: looking along the propagation direction, the E-vector of a "
            "right-hand polarized wave rotates clockwise and a left-hand wave counter-clockwise")


# --------------------------------------------------------------------------
# 4. The polarization ellipse: major/minor axes and tilt
# --------------------------------------------------------------------------
def axial_ratio() -> None:
    f = Fig()
    cx, cy = 120.0, 118.0
    A, B, TILT = 92.0, 38.0, math.radians(32.0)

    f.axes(cx, cy, A + 26)

    pts = []
    for i in range(97):
        t = TAU * i / 96
        u, v = A * math.cos(t), B * math.sin(t)
        pts.append((cx + u * math.cos(TILT) - v * math.sin(TILT),
                    cy - (u * math.sin(TILT) + v * math.cos(TILT))))
    f.add(f'<path d="{d_of(pts, True)}" fill="{BLUE}" fill-opacity="0.08" '
          f'stroke="{BLUE}" stroke-width="2.6"/>', *pts)

    # major axis (navy) and minor axis (red), drawn full-width through the center
    for mag, ang, color, key, lab, off in (
            (A, TILT, NAVY, "navy", "E<tspan font-size=\"10\" dy=\"4\">maj</tspan>", 20),
            (B, TILT + math.pi / 2, RED, "red", "E<tspan font-size=\"10\" dy=\"4\">min</tspan>", 18)):
        dx, dy = mag * math.cos(ang), mag * math.sin(ang)
        f.add(f'<line x1="{cx - dx:.1f}" y1="{cy + dy:.1f}" x2="{cx + dx:.1f}" '
              f'y2="{cy - dy:.1f}" stroke="{color}" stroke-width="2.4" '
              f'stroke-dasharray="6 4"/>', (cx - dx, cy + dy), (cx + dx, cy - dy))
        f.vec(cx, cy, dx, dy, key, 2.8)
        f.text(cx + dx + off * math.cos(ang), cy - dy - off * math.sin(ang) + 5,
               lab, color, 15, "middle", "700")

    # tilt angle, measured from x to the major axis
    r_arc = 46.0
    f.add(f'<path d="M{cx + r_arc:.1f} {cy:.1f} A{r_arc} {r_arc} 0 0 0 '
          f'{cx + r_arc * math.cos(TILT):.1f} {cy - r_arc * math.sin(TILT):.1f}" '
          f'fill="none" stroke="{GREEN}" stroke-width="2.0"/>',
          (cx + r_arc, cy), (cx + r_arc, cy - r_arc))
    f.text(cx + (r_arc + 15) * math.cos(TILT / 2),
           cy - (r_arc + 15) * math.sin(TILT / 2) + 5, "τ", GREEN, 16, "middle", "700")

    # straddling the top: leftward motion there reads unambiguously as ccw
    f.arc_arrow(cx, cy, A + 8, 55, 125, "gray", 1.8, ccw=True)
    f.write("L03-axial-ratio",
            "The polarization ellipse with its major and minor axes and tilt angle tau; "
            "the axial ratio is the ratio of the two axes")


def main() -> int:
    pol_states()
    pol_construction()
    handedness()
    axial_ratio()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
