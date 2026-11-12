#!/usr/bin/env python3
"""L24 Lab: the four procedures, one panel each.

A  Steps 6-10    the computed notch: eight weights loaded, null at +22.5 deg
B  Steps 11-15   the difference null: Beam 1 Phase 180 deg, null at boresight
C  Steps 16-22   MVDR's null: two channels, interferer at +20 deg
D  Steps 23-27   monopulse: the sum and delta beams together, for tracking

Each panel names what the cadet sets and shows a thumbnail of the trace to
expect, computed rather than drawn by eye: the array factor at the nominal
10.525 GHz (Lesson 24's worked example), in dB below the uniform peak, clipped
at a floor 40 dB down so a deep null reads as a notch to the floor. The MVDR
panel is the analog subarray beam at boresight times the two-channel MVDR
weights for an interferer at +20 deg, 10 dB above the target, with the lab's
diagonal loading of 0.1.

Two layouts, served through <picture> as the L20 Lab sequence is: a 2-by-2
grid for the half column beside the flow table on a laptop, and a shorter
2-by-2 for a phone, where the figure stacks under the table.

    python3 scripts/graphics/m3_l24_lab_sequence.py
    -> book/extras/viz/img/L24-lab-sequence.svg
       book/extras/viz/img/L24-lab-sequence-narrow.svg
"""

from __future__ import annotations
import math
from pathlib import Path

import numpy as np
from svg_font_stack import apply_font_stack

OUT = Path(__file__).resolve().parents[2] / "book/extras/viz/img"

NAVY, BLUE, AMBER, GRAY, INK, LIGHT = "#004a85", "#0067b9", "#8a5a00", "#5a5a5a", "#1f2a36", "#c7d2e0"

LAM, DEL = 3.00e8 / 10.525e9, 14e-3        # 10.525 GHz, element pitch
KD = 2 * math.pi * DEL / LAM
N = 8
NIDX = np.arange(N)
FLOOR = -40.0                               # dB below the uniform peak
YMIN = -44.0
TMAX = 60.0                                 # thumbnails span -60..60 deg

PW, PH = 220, 200                           # one panel

T = np.linspace(-TMAX, TMAX, 1201)
PSI = KD * np.sin(np.deg2rad(T))


def to_db(v, ref=N):
    return np.maximum(20 * np.log10(np.maximum(np.abs(v) / ref, 1e-9)), FLOOR)


def uniform():
    return np.exp(1j * np.outer(PSI, NIDX)).sum(1)


def notch(theta1=22.5):
    psi1 = KD * math.sin(math.radians(theta1))
    r = np.exp(1j * NIDX * psi1).mean()
    w = 1 - r * np.exp(-1j * NIDX * psi1)
    w = w / np.abs(w).max()                  # sliders top out at 100 %
    return np.exp(1j * np.outer(PSI, NIDX)) @ w


def difference():
    e = np.exp(1j * np.outer(PSI, NIDX))
    return e[:, :4].sum(1) - e[:, 4:].sum(1)


def mvdr(theta_i=20.0, inr_db=10.0, load=0.1):
    sub = np.exp(1j * np.outer(PSI, np.arange(4))).sum(1)          # each subarray, steered to 0
    psi_i = KD * math.sin(math.radians(theta_i))
    gain_i = abs(np.exp(1j * np.arange(4) * psi_i).sum()) / 4
    s = np.array([1, 1], complex)                                     # look direction, boresight
    u = np.array([1, np.exp(1j * 4 * psi_i)]) * gain_i                # interferer at the channels
    p = 10 ** (inr_db / 10)
    snr = 10 ** (30 / 10)                                             # target well above the noise
    R = np.eye(2) + snr * np.outer(s, s.conj()) + snr * p * np.outer(u, u.conj())
    R = R + load * np.trace(R).real / 2 * np.eye(2)
    w = np.linalg.solve(R, s)
    w = 2 * w / (s.conj() @ w).conj()                                        # the Phaser's x2: Manual's scale
    chan = w[0].conj() + w[1].conj() * np.exp(1j * 4 * PSI)          # y = w^H x
    return sub * chan


PANELS = [
    ("A", "Computed notch", "Steps 6–10", "Load the eight weights", [(uniform(), LIGHT, 1.3), (notch(), NAVY, 1.6)], 22.5),
    ("B", "Difference null", "Steps 11–15", "Beam 1 Phase at 180°", [(uniform(), LIGHT, 1.3), (difference(), NAVY, 1.6)], 0.0),
    ("C", "MVDR's null", "Steps 16–22", "Interferer at +20°", [(uniform(), LIGHT, 1.3), (mvdr(), NAVY, 1.6)], 20.0),
    ("D", "Monopulse", "Steps 23–27", "Sum and delta at once", [(uniform(), BLUE, 1.5), (difference(), NAVY, 1.6)], None),
]


def panel(s, ox, oy, k, ph=PH):
    letter, title, steps, setting, traces, mark = PANELS[k]
    s.append(f'<rect x="{ox + 4}" y="{oy + 4}" width="{PW - 8}" height="{ph - 8}" rx="8" fill="#ffffff" '
             f'stroke="{LIGHT}" stroke-width="1.2"/>')
    s.append(f'<circle cx="{ox + 24}" cy="{oy + 25}" r="12" fill="{NAVY}"/>')
    s.append(f'<text x="{ox + 24}" y="{oy + 30}" text-anchor="middle" font-size="14" '
             f'font-weight="700" fill="#ffffff">{letter}</text>')
    s.append(f'<text x="{ox + 44}" y="{oy + 30}" font-size="16" font-weight="700" fill="{INK}">{title}</text>')
    s.append(f'<text x="{ox + PW / 2}" y="{oy + 56}" text-anchor="middle" font-size="13" '
             f'fill="{INK}">{setting}</text>')
    s.append(f'<text x="{ox + PW / 2}" y="{oy + 74}" text-anchor="middle" font-size="12" '
             f'fill="{GRAY}">{steps}</text>')

    bx, by, bw, bh = ox + 18, oy + 88, PW - 36, ph - 108
    s.append(f'<rect x="{bx}" y="{by}" width="{bw}" height="{bh}" fill="#f6f9fc" stroke="{LIGHT}" stroke-width="1"/>')

    def X(a):
        return bx + (a + TMAX) / (2 * TMAX) * bw

    def Y(d):
        return by + (0 - d) / (0 - YMIN) * bh

    if mark is not None:
        s.append(f'<line x1="{X(mark):.1f}" y1="{by}" x2="{X(mark):.1f}" y2="{by + bh}" stroke="{AMBER}" '
                 f'stroke-width="1" stroke-dasharray="3 3" opacity="0.9"/>')
    for v, color, lw in traces:
        db = to_db(v)
        pts = " ".join(f"{X(a):.1f},{Y(d):.1f}" for a, d in zip(T, db))
        s.append(f'<polyline points="{pts}" fill="none" stroke="{color}" stroke-width="{lw}" stroke-linejoin="round"/>')
    for a, lab in ((-TMAX, "−60°"), (0, "0°"), (TMAX, "60°")):
        s.append(f'<text x="{X(a):.1f}" y="{by + bh + 12}" text-anchor="middle" '
                 f'font-size="10.5" fill="{GRAY}">{lab}</text>')


def build(cols: int, ph: int = PH) -> str:
    rows = math.ceil(len(PANELS) / cols)
    w, h = PW * cols, ph * rows
    s = [f'<svg viewBox="0 0 {w} {h}" xmlns="http://www.w3.org/2000/svg" role="img" '
         f'aria-label="The four procedures of the L24 Lab, each with the trace to expect against the uniform '
         f'pattern. A, Steps 6 to 10: the eight computed weights put a notch at plus 22.5 degrees. B, Steps 11 '
         f'to 15: Beam 1 Phase at 180 degrees puts a null at boresight with a peak on each side. C, Steps 16 to '
         f'22: MVDR puts its one null on an interferer at plus 20 degrees. D, Steps 23 to 27: the sum and delta '
         f'beams together, the delta zero on boresight.">']
    for k in range(len(PANELS)):
        r, c = divmod(k, cols)
        panel(s, c * PW, r * ph, k, ph)
    s.append("</svg>")
    return apply_font_stack("\n".join(s)) + "\n"


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "L24-lab-sequence.svg").write_text(build(2), encoding="utf-8")
    (OUT / "L24-lab-sequence-narrow.svg").write_text(build(2, 166), encoding="utf-8")
    print("wrote L24-lab-sequence.svg, L24-lab-sequence-narrow.svg")


if __name__ == "__main__":
    main()
