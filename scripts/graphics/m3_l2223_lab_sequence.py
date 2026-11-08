#!/usr/bin/env python3
"""L22-L23 Lab: the four runs, one panel each.

Steps 7-13   Tapers          uniform against Hann, on the uniform peak's scale
Steps 14-16  Grating lobes   Rx1, Rx4, Rx7 on, 42 mm apart: three full-height lobes
Steps 17-18  Squint          source at 45 deg; Signal BW 10 MHz against 500 MHz
Steps 19-21  Quantization    beam held at 15 deg, Blackman taper; 7 bits against 2

Each panel shows the eight-element row (shaded by amplitude, or lit where an
element is on) and a thumbnail of the trace to expect, computed from the
array factor at 10.3 GHz and clipped at the noise floor 23 dB down. The
thumbnails are computed, not drawn by eye.

Two layouts, served through <picture> as the L20 Lab sequence is: a 2-by-2
grid for the half column beside the flow table on a laptop, and a shorter
2-by-2 for a phone, where the figure stacks under the table.

    python3 scripts/graphics/m3_l2223_lab_sequence.py
    -> book/extras/viz/img/L22-L23-lab-sequence.svg
       book/extras/viz/img/L22-L23-lab-sequence-narrow.svg
"""

from __future__ import annotations
import math
from pathlib import Path

import numpy as np
from svg_font_stack import apply_font_stack

OUT = Path(__file__).resolve().parents[2] / "book/extras/viz/img"

NAVY, BLUE, AMBER, GRAY, INK, LIGHT = "#004a85", "#0067b9", "#8a5a00", "#5a5a5a", "#1f2a36", "#c7d2e0"

F, DEL = 10.3e9, 14e-3                      # 10.3 GHz, element pitch
LAM = 3.00e8 / F
FLOOR = -23.0                               # dB, the sweep's noise floor
YMIN = -30.0

PW, PH = 220, 200                           # one panel
SQ, GAP = 14, 5                             # element squares

UNIFORM = np.ones(8)
HANN = np.array([.12, .43, .77, 1, 1, .77, .43, .12])
BLACKMAN = np.array([.06, .27, .66, 1, 1, .66, .27, .06])
GRATING = np.array([1, 0, 0, 1, 0, 0, 1, 0], dtype=float)
N = np.arange(8) - 3.5


def field(a, th, phase=None, f=F):
    """Array factor magnitude over angles th (deg), weights a, element phases (rad)."""
    k = 2 * math.pi * f / 3.00e8
    s = np.sin(np.deg2rad(th))
    ph = np.zeros(8) if phase is None else phase
    return np.abs((a[None, :] * np.exp(1j * (k * DEL * N[None, :] * s[:, None] - ph[None, :]))).sum(1))


def taper_traces(th):
    """Uniform and Hann on the uniform peak's scale, so the peak drop shows."""
    ref = field(UNIFORM, th).max()
    return [(20 * np.log10(np.maximum(field(a, th) / ref, 1e-9)), col, w)
            for a, col, w in ((UNIFORM, GRAY, 1.2), (HANN, NAVY, 1.7))]


def grating_traces(th):
    v = field(GRATING, th)
    return [(20 * np.log10(np.maximum(v / v.max(), 1e-9)), NAVY, 1.6)]


def squint_traces(th):
    """Received level against commanded angle, source fixed at 45 deg.

    The phases are set for the commanded angle at f0 = f - Signal BW; the
    signal arrives at f from 45 deg.
    """
    out = []
    s_src = math.sin(math.radians(45))
    for bw, col, w in ((10e6, GRAY, 1.2), (500e6, NAVY, 1.7)):
        f0 = F - bw
        k, k0 = 2 * math.pi * F / 3.00e8, 2 * math.pi * f0 / 3.00e8
        psi = DEL * (k * s_src - k0 * np.sin(np.deg2rad(th)))
        v = np.abs(np.exp(1j * np.outer(psi, N)).sum(1))
        out.append((20 * np.log10(np.maximum(v / v.max(), 1e-9)), col, w))
    return out


def quant_traces(th):
    """Blackman beam held at 15 deg, phases rounded to 7 and to 2 bits; dB
    below each trace's own peak, against the source's azimuth."""
    k = 2 * math.pi * F / 3.00e8
    exact = np.arange(8) * k * DEL * math.sin(math.radians(15))
    out = []
    for bits, col, w in ((7, GRAY, 1.2), (2, NAVY, 1.7)):
        lsb = 2 * math.pi / 2 ** bits
        q = np.round(exact / lsb) * lsb
        v = field(BLACKMAN, th, q)
        out.append((20 * np.log10(np.maximum(v / v.max(), 1e-9)), col, w))
    return out


RUNS = [
    ("7–13", "Tapers", HANN, "uniform, then Hann", taper_traces, (-90, 90)),
    ("14–16", "Grating lobes", GRATING, "Rx1, Rx4, Rx7: 42 mm", grating_traces, (-90, 90)),
    ("17–18", "Squint", UNIFORM, "source at 45°, 500 MHz", squint_traces, (20, 70)),
    ("19–21", "Quantization", BLACKMAN, "15° beam, 7 and 2 bits", quant_traces, (-90, 90)),
]


def panel(s, ox, oy, k, ph=PH):
    num, title, w, caption, traces, (lo, hi) = RUNS[k]
    s.append(f'<rect x="{ox + 4}" y="{oy + 4}" width="{PW - 8}" height="{ph - 8}" rx="8" fill="#ffffff" '
             f'stroke="{LIGHT}" stroke-width="1.2"/>')
    pw = 12 + 8.2 * len(num)
    s.append(f'<rect x="{ox + 12}" y="{oy + 14}" width="{pw:.0f}" height="22" rx="11" fill="{NAVY}"/>')
    s.append(f'<text x="{ox + 12 + pw / 2:.1f}" y="{oy + 29.5}" text-anchor="middle" font-size="12.5" '
             f'font-weight="700" fill="#ffffff">{num}</text>')
    s.append(f'<text x="{ox + 20 + pw:.1f}" y="{oy + 30}" font-size="15" font-weight="700" fill="{INK}">{title}</text>')

    # the eight-element row: shaded by amplitude, empty where off
    row_w = 8 * SQ + 7 * GAP
    x0, y0 = ox + (PW - row_w) / 2, oy + 48
    for n in range(8):
        a = float(w[n])
        fill = BLUE if a > 0 else "#ffffff"
        op = f' fill-opacity="{0.15 + 0.85 * a:.2f}"' if a > 0 else ""
        s.append(f'<rect x="{x0 + n * (SQ + GAP):.1f}" y="{y0}" width="{SQ}" height="{SQ}" rx="2" '
                 f'fill="{fill}"{op} stroke="{NAVY if a > 0 else LIGHT}" stroke-width="1.2"/>')
    s.append(f'<text x="{ox + PW / 2}" y="{y0 + SQ + 17}" text-anchor="middle" font-size="12.5" '
             f'fill="{INK}">{caption}</text>')

    # thumbnail of the expected trace(s)
    bx, by, bw, bh = ox + 18, oy + 98, PW - 36, ph - 118
    s.append(f'<rect x="{bx}" y="{by}" width="{bw}" height="{bh}" fill="#f6f9fc" stroke="{LIGHT}" stroke-width="1"/>')
    fy = by + (0 - FLOOR) / (0 - YMIN) * bh
    s.append(f'<line x1="{bx}" y1="{fy:.1f}" x2="{bx + bw}" y2="{fy:.1f}" stroke="{AMBER}" stroke-width="1" '
             f'stroke-dasharray="3 3" opacity="0.8"/>')
    th = np.linspace(lo, hi, 721)
    for db, col, lw in traces(th):
        db = np.maximum(db, FLOOR)
        pts = " ".join(f"{bx + (a - lo) / (hi - lo) * bw:.1f},{by + (0 - d) / (0 - YMIN) * bh:.1f}"
                       for a, d in zip(th, db))
        s.append(f'<polyline points="{pts}" fill="none" stroke="{col}" stroke-width="{lw}" '
                 f'stroke-linejoin="round"/>')
    ticks = ((lo, f"{lo}°".replace("-", "−")), ((lo + hi) / 2, f"{(lo + hi) // 2}°"), (hi, f"{hi}°"))
    for a, lab in ticks:
        s.append(f'<text x="{bx + (a - lo) / (hi - lo) * bw:.1f}" y="{by + bh + 12}" text-anchor="middle" '
                 f'font-size="10.5" fill="{GRAY}">{lab}</text>')


def build(cols: int, ph: int = PH) -> str:
    rows = math.ceil(len(RUNS) / cols)
    w, h = PW * cols, ph * rows
    s = [f'<svg viewBox="0 0 {w} {h}" xmlns="http://www.w3.org/2000/svg" role="img" '
         f'aria-label="The four runs of the L22 to L23 Lab. Steps 7 to 13, tapers: the Hann trace is wider '
         f'than the uniform trace and its peak sits lower. Steps 14 to 16, grating lobes: with Rx1, Rx4 and '
         f'Rx7 on, three full-height lobes. Steps 17 to 18, squint: with the source at 45 degrees, the 500 MHz '
         f'trace peaks a few degrees past the 10 MHz trace. Steps 19 to 21, quantization: a Blackman beam held '
         f'at 15 degrees; at 2 bits a lobe rises near minus 51 degrees. Each thumbnail is the array factor at '
         f'10.3 GHz, clipped at the noise floor.">']
    for k in range(len(RUNS)):
        r, c = divmod(k, cols)
        panel(s, c * PW, r * ph, k, ph)
    s.append("</svg>")
    return apply_font_stack("\n".join(s)) + "\n"


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "L22-L23-lab-sequence.svg").write_text(build(2), encoding="utf-8")
    (OUT / "L22-L23-lab-sequence-narrow.svg").write_text(build(2, 166), encoding="utf-8")
    print("wrote L22-L23-lab-sequence.svg, L22-L23-lab-sequence-narrow.svg")


if __name__ == "__main__":
    main()
