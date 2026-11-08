#!/usr/bin/env python3
"""L21 Lab: the three runs, one panel each.

Run 1  Steps 7-9    the HB100 fixed, the kit steps the beam: a beam sweep
Run 2  Steps 10-15  the beam held at 0 deg, the HB100 carried along the arc
Run 3  Steps 16-19  the HB100 fixed, the kit turned on its stand: the 0 and
                    30 deg beams read at the stand's 10 deg marks

Each panel pairs a top-view sketch of what moves with a thumbnail of the trace
to expect, computed, not drawn by eye: the array factor at 10.3 GHz in dBc for
the beam sweep, and the array factor times the course's cos(theta) element
pattern for the azimuth sweeps, all clipped at the noise floor 23 dB below
each trace's own peak.

Two layouts, served through <picture> as the L20 Lab sequence is: three rows
for the half column beside the flow table on a laptop, and shorter rows for a
phone, where the figure stacks under the table.

    python3 scripts/graphics/m3_l21_lab_sequence.py
    -> book/extras/viz/img/L21-lab-sequence.svg
       book/extras/viz/img/L21-lab-sequence-narrow.svg
"""

from __future__ import annotations
import math
from pathlib import Path

import numpy as np
from svg_font_stack import apply_font_stack

OUT = Path(__file__).resolve().parents[2] / "book/extras/viz/img"

NAVY, BLUE, AMBER, GRAY, INK, LIGHT = "#004a85", "#0067b9", "#8a5a00", "#5a5a5a", "#1f2a36", "#c7d2e0"

LAM, DEL, N = 3.00e8 / 10.3e9, 14e-3, 8    # 10.3 GHz, element pitch, elements
FLOOR = -23.0                               # dBc, below each trace's own peak
YMIN = -30.0

PW, PH = 420, 150                           # one panel (a row)

RUNS = [
    ("1", "Run 1: beam sweep", "Steps 7 to 9", "steer angle"),
    ("2", "Run 2: sweeps by hand", "Steps 10 to 15", "elapsed time"),
    ("3", "Run 3: pass on the stand", "Steps 16 to 19", "source angle"),
]


def af_db(theta_src_deg, theta0_deg):
    """Uniform eight-element array factor in dB (0 dB peak)."""
    kd = 2 * math.pi * DEL / LAM
    psi = kd * (np.sin(np.deg2rad(theta_src_deg)) - np.sin(np.deg2rad(theta0_deg)))
    v = np.abs(sum(np.exp(1j * n * psi) for n in range(N))) / N
    return 20 * np.log10(np.maximum(v, 1e-9))


def element_db(theta_deg):
    return 10 * np.log10(np.maximum(np.cos(np.deg2rad(theta_deg)), 1e-9))


def to_dbc(db):
    return np.maximum(db - db.max(), FLOOR)


def sketch(s, run, x, y, w, h):
    """A top view: the array as a bar, the HB100 as a dot, and what moves."""
    cx, ay = x + w / 2, y + h - 30
    # array bar, rotated for Run 3
    ang = -18 if run == "3" else 0
    s.append(f'<g transform="rotate({ang} {cx} {ay})">'
             f'<rect x="{cx - 30}" y="{ay - 4}" width="60" height="8" rx="2" fill="{BLUE}"/></g>')
    if run == "3":
        s.append(f'<path d="M {cx + 22} {ay - 22} A 32 32 0 0 1 {cx + 34} {ay + 2}" fill="none" '
                 f'stroke="{AMBER}" stroke-width="1.6" marker-end="url(#arr)"/>')
        s.append(f'<text x="{cx}" y="{ay + 24}" text-anchor="middle" font-size="10.5" fill="{AMBER}">kit turns on its stand</text>')
    sy = y + 8
    if run == "2":
        r = h - 40
        s.append(f'<path d="M {cx - r} {ay} A {r} {r} 0 0 1 {cx + r} {ay}" fill="none" stroke="{AMBER}" '
                 f'stroke-width="1.6" stroke-dasharray="4 3"/>')
        hx, hy = cx - r * math.cos(math.radians(55)), ay - r * math.sin(math.radians(55))
        s.append(f'<circle cx="{hx:.1f}" cy="{hy:.1f}" r="6" fill="{NAVY}"/>')
        s.append(f'<text x="{cx}" y="{ay + 20}" text-anchor="middle" font-size="10.5" fill="{AMBER}">HB100 carried along the arc</text>')
        # held beam, straight ahead
        s.append(f'<line x1="{cx}" y1="{ay - 6}" x2="{cx}" y2="{ay - r + 10}" stroke="{NAVY}" '
                 f'stroke-width="1.4" stroke-dasharray="2 3"/>')
    else:
        s.append(f'<circle cx="{cx}" cy="{sy}" r="6" fill="{NAVY}"/>')
        s.append(f'<text x="{cx + 10}" y="{sy + 4}" font-size="10.5" fill="{GRAY}">HB100</text>')
    if run == "1":
        fan = (ay - 6) - (sy + 12)           # stop short of the HB100, at any panel height
        for a in (-35, -15, 5, 25):
            ex = cx + fan * math.sin(math.radians(a))
            ey = ay - 6 - fan * math.cos(math.radians(a))
            s.append(f'<line x1="{cx}" y1="{ay - 6}" x2="{ex:.1f}" y2="{ey:.1f}" stroke="{AMBER}" '
                     f'stroke-width="1.4" opacity="0.85"/>')
        s.append(f'<text x="{cx}" y="{ay + 20}" text-anchor="middle" font-size="10.5" fill="{AMBER}">kit steps the beam</text>')


def thumb(s, run, x, y, w, h):
    s.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="#f6f9fc" stroke="{LIGHT}" stroke-width="1"/>')
    fy = y + (0 - FLOOR) / (0 - YMIN) * h
    s.append(f'<line x1="{x}" y1="{fy:.1f}" x2="{x + w}" y2="{fy:.1f}" stroke="{GRAY}" stroke-width="1" '
             f'stroke-dasharray="3 3" opacity="0.7"/>')

    def py(d):
        return y + (0 - d) / (0 - YMIN) * h

    def px(a):
        return x + (a + 90) / 180 * w

    t = np.linspace(-90.0, 90.0, 721)
    if run == "1":
        db = to_dbc(af_db(0.0, -t))          # source at 0, beam stepped: AF vs steer angle
        pts = " ".join(f"{px(a):.1f},{py(d):.1f}" for a, d in zip(t, db))
        s.append(f'<polyline points="{pts}" fill="none" stroke="{NAVY}" stroke-width="1.6" stroke-linejoin="round"/>')
    elif run == "2":
        db = to_dbc(af_db(t, 0.0) + element_db(t))
        # an uneven hand: slow in the middle, so time stretches the main lobe
        u = (t + 90) / 180
        tt = u + 0.06 * np.sin(2 * math.pi * u)
        pts = " ".join(f"{x + v * w:.1f},{py(d):.1f}" for v, d in zip(tt, db))
        s.append(f'<polyline points="{pts}" fill="none" stroke="{NAVY}" stroke-width="1.6" stroke-linejoin="round"/>')
    else:
        marks = np.arange(-90, 91, 10, dtype=float)
        for th0, col in ((0.0, NAVY), (30.0, AMBER)):
            curve = af_db(t, th0) + element_db(t)
            ref = (af_db(np.array([0.0]), 0.0) + element_db(np.array([0.0])))[0]
            db = np.maximum(curve - ref, FLOOR)
            pts = " ".join(f"{px(a):.1f},{py(d):.1f}" for a, d in zip(t, db))
            s.append(f'<polyline points="{pts}" fill="none" stroke="{col}" stroke-width="1" opacity="0.45"/>')
            mk = np.maximum(af_db(marks, th0) + element_db(marks) - ref, FLOOR)
            for a, d in zip(marks, mk):
                s.append(f'<circle cx="{px(a):.1f}" cy="{py(d):.1f}" r="2.4" fill="{col}"/>')
        s.append(f'<text x="{x + w - 4}" y="{y + 11}" text-anchor="end" font-size="10.5" fill="{NAVY}">beam 0°</text>')
        s.append(f'<text x="{x + w - 4}" y="{y + 23}" text-anchor="end" font-size="10.5" fill="{AMBER}">beam 30°</text>')


def panel(s, k, oy, ph):
    num, title, steps, xlab = RUNS[k]
    s.append(f'<rect x="4" y="{oy + 4}" width="{PW - 8}" height="{ph - 8}" rx="8" fill="#ffffff" '
             f'stroke="{LIGHT}" stroke-width="1.2"/>')
    s.append(f'<circle cx="24" cy="{oy + 24}" r="12" fill="{NAVY}"/>')
    s.append(f'<text x="24" y="{oy + 29}" text-anchor="middle" font-size="14" font-weight="700" fill="#ffffff">{num}</text>')
    s.append(f'<text x="44" y="{oy + 22}" font-size="14.5" font-weight="700" fill="{INK}">{title}</text>')
    s.append(f'<text x="44" y="{oy + 37}" font-size="11.5" fill="{GRAY}">{steps}</text>')
    sketch(s, num, 14, oy + 46, 150, ph - 52)
    tx, tw = 176, PW - 176 - 16
    thumb(s, num, tx, oy + 46, tw, ph - 74)
    s.append(f'<text x="{tx + tw / 2}" y="{oy + ph - 14}" text-anchor="middle" font-size="10.5" fill="{GRAY}">{xlab}</text>')


def build(ph: int) -> str:
    w, h = PW, ph * len(RUNS)
    s = [f'<svg viewBox="0 0 {w} {h}" xmlns="http://www.w3.org/2000/svg" role="img" '
         f'aria-label="The three runs of the L21 Lab. Run 1, Steps 7 to 9: the HB100 fixed while the kit steps '
         f'the beam, a broadside beam-sweep trace against steer angle. Run 2, Steps 10 to 15: the beam held at '
         f'0 degrees while you carry the HB100 along the arc, the same pattern against elapsed time. Run 3, '
         f'Steps 16 to 19: the HB100 fixed and the kit turned on its stand, the 0 and 30 degree beams read at '
         f'the stand\'s 10 degree marks. Each thumbnail is in dBc at 10.3 GHz, clipped at the noise floor.">']
    s.append(f'<defs><marker id="arr" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" '
             f'orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="{AMBER}"/></marker></defs>')
    for k in range(len(RUNS)):
        panel(s, k, k * ph, ph)
    s.append("</svg>")
    return apply_font_stack("\n".join(s)) + "\n"


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "L21-lab-sequence.svg").write_text(build(PH), encoding="utf-8")
    (OUT / "L21-lab-sequence-narrow.svg").write_text(build(136), encoding="utf-8")
    print("wrote L21-lab-sequence.svg, L21-lab-sequence-narrow.svg")


if __name__ == "__main__":
    main()
