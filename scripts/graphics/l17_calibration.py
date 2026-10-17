#!/usr/bin/env python3
"""L17 calibration figures, drawn for a present column (Neil, 2026-10-17:
"Calibration is an important concept in arrays").

  L17-cal-patterns : the 8-element array factor with every commanded phase at
                     zero, before and after calibration, for one example set
                     of channel offsets: the uncalibrated beam squints to
                     +6.0 deg and its peak sidelobe rises from -12.8 to
                     -7.8 dB
  L17-cal-pair     : the two-element sum |1 + e^{j delta}| in dB against the
                     swept phase, with the band within 0.2 dB of the peak
                     shaded, 24.5 deg either side (a 20-deg error lowers it by
                     0.13 dB)

The channel offsets are illustrative, not measured: one example of what trace
lengths and part tolerances do, chosen so both defects show. The widget
book/extras/viz/array-calibration.html uses the same numbers (GAIN_DB,
PHASE_DEG); change them in both places.

Every plotted number is computed here, asserted, and printed for checking
against the lesson text. Lesson-page copies only: the decks are frozen, so
nothing is written to book/extras/slides/fig/.

    python3 scripts/graphics/l17_calibration.py

Writes:
    book/extras/viz/img/L17-cal-patterns.svg
    book/extras/viz/img/L17-cal-pair.svg
"""

from __future__ import annotations

import numpy as np

from l17_figures import OUTS, W, line, polyline, rect, svg_open, txt, write
from m3_l17_chain import AMBER, BG, EDGE2, INK3, NAVY

PAGE = OUTS[1:]          # book/extras/viz/img only

D_LAM = 0.491            # d / lambda at 10.525 GHz (COURSE_SPEC M3)
N = 8
# Example channel offsets, element 1 to 8. Same values as the widget.
GAIN_DB = np.array([-0.6, 0.0, -1.4, -0.3, -2.2, -0.9, -1.7, -0.5])
PHASE_DEG = np.array([0.0, -5.0, -8.0, 12.0, -30.0, -42.0, -93.0, -140.0])
FLOOR = -30.0            # dB, bottom of the pattern plot


def array_factor(w, th_deg):
    n = np.arange(N)[:, None]
    th = np.radians(th_deg)[None, :]
    return np.abs((w[:, None] * np.exp(1j * 2 * np.pi * D_LAM * n * np.sin(th))).sum(0))


def lobe_stats(th, af):
    """Peak angle and peak sidelobe (dB below the peak) of a pattern."""
    i = int(af.argmax())
    j = i
    while j < af.size - 1 and af[j + 1] < af[j]:
        j += 1
    k = i
    while k > 0 and af[k - 1] < af[k]:
        k -= 1
    side = max(af[:k].max() if k > 0 else 0.0, af[j:].max() if j < af.size - 1 else 0.0)
    return th[i], 20 * np.log10(side / af[i])


def db_from_peak(af):
    return np.maximum(20 * np.log10(af / af.max() + 1e-12), FLOOR)


# --------------------------------------------------------------------------
# before and after
# --------------------------------------------------------------------------

def cal_patterns() -> str:
    th = np.linspace(-90, 90, 3601)
    g = 10 ** (GAIN_DB / 20)
    before = array_factor(g * np.exp(1j * np.radians(PHASE_DEG)), th)
    after = array_factor(np.full(N, g.min()), th)
    a0, sl0 = lobe_stats(th, before)
    a1, sl1 = lobe_stats(th, after)
    print(f"  uncalibrated: beam {a0:+.2f} deg, peak sidelobe {sl0:.2f} dB")
    print(f"  calibrated:   beam {a1:+.2f} deg, peak sidelobe {sl1:.2f} dB")
    assert round(a0, 1) == 6.0 and round(sl0, 1) == -7.8, (a0, sl0)
    assert a1 == 0.0 and round(sl1, 1) == -12.8, (a1, sl1)

    H = 280
    x0, x1, y0, y1 = 44, 396, 78, 240        # plot box
    xm = lambda a: x0 + (a + 90) / 180 * (x1 - x0)
    ym = lambda d: y0 + (-d) / (-FLOOR) * (y1 - y0)
    s = [svg_open(H, f"Array factor of the eight elements with every commanded phase at "
                  f"zero, in dB from each pattern's peak, from -90 to +90 degrees. "
                  f"Uncalibrated, the beam points to +{a0:.1f} degrees and the highest "
                  f"sidelobe is {sl0:.1f} dB. Calibrated, the beam is at broadside and "
                  f"the highest sidelobe is {sl1:.1f} dB.")]
    s.append(rect(4, 4, W - 8, H - 8, BG, EDGE2, 1.2, 5))
    s.append(txt(16, 26, "Uncalibrated", 14, AMBER, anchor="start", weight="700"))
    s.append(txt(124, 26, f"beam at +{a0:.1f}°, sidelobes {sl0:.1f} dB".replace("-", "−"),
                 13, AMBER, anchor="start"))
    s.append(txt(16, 46, "Calibrated", 14, NAVY, anchor="start", weight="700"))
    s.append(txt(124, 46, f"beam at 0°, sidelobes {sl1:.1f} dB".replace("-", "−"),
                 13, NAVY, anchor="start"))
    for d in (0, -10, -20, -30):
        s.append(line(x0, ym(d), x1, ym(d), EDGE2, 0.9))
        s.append(txt(x0 - 6, ym(d) + 4.5, f"{d}".replace("-", "−"), 13, INK3, anchor="end"))
    for a in (-90, -45, 0, 45, 90):
        s.append(txt(xm(a), y1 + 18, f"{a}°".replace("-", "−"), 13, INK3))
    s.append(txt(x0 - 6, y0 - 6, "dB", 13, INK3, anchor="end"))
    s.append(line(xm(0), y0, xm(0), y1, INK3, 1.0, ' stroke-dasharray="3 3"'))
    s.append(polyline(xm(th), ym(db_from_peak(after)), NAVY, 2.2))
    s.append(polyline(xm(th), ym(db_from_peak(before)), AMBER, 2.0, ' stroke-dasharray="6 3"'))
    s.append(line(xm(a0), y0, xm(a0), y1, AMBER, 1.0, ' stroke-dasharray="2 3"'))
    s.append("</svg>")
    return "\n".join(s)


# --------------------------------------------------------------------------
# the pair sweep
# --------------------------------------------------------------------------

def cal_pair() -> str:
    dl = np.linspace(-180, 180, 1441)
    resp = 20 * np.log10(np.abs(1 + np.exp(1j * np.radians(dl))) / 2 + 1e-12)
    loss20 = -20 * np.log10(np.cos(np.radians(10)))
    half = 2 * np.degrees(np.arccos(10 ** (-0.2 / 20)))     # half-width within 0.2 dB
    print(f"  pair: a 20-deg error loses {loss20:.3f} dB; within 0.2 dB over +/-{half:.1f} deg")
    assert round(loss20, 2) == 0.13, loss20
    assert round(half, 1) == 24.5, half

    H = 264
    x0, x1, y0, y1 = 44, 396, 30, 210
    lo = -30.0
    xm = lambda a: x0 + (a + 180) / 360 * (x1 - x0)
    ym = lambda d: y0 + (-np.maximum(d, lo)) / (-lo) * (y1 - y0)
    s = [svg_open(H, "The sum of two elements in dB against the phase of the swept "
                  "element, from -180 to +180 degrees. It peaks at 0 degrees and falls "
                  "to a deep null at plus and minus 180. The band within 0.2 dB of the "
                  "peak is shaded and spans 49 degrees; 20 degrees off the peak, the sum "
                  "is 0.13 dB down.")]
    s.append(rect(4, 4, W - 8, H - 8, BG, EDGE2, 1.2, 5))
    s.append(rect(xm(-half), y0, xm(half) - xm(-half), y1 - y0,
                  "#fdf6e8", "none", 0, 0))
    for d in (0, -10, -20, -30):
        s.append(line(x0, ym(d), x1, ym(d), EDGE2, 0.9))
        s.append(txt(x0 - 6, ym(d) + 4.5, f"{d}".replace("-", "−"), 13, INK3, anchor="end"))
    for a in (-180, -90, 0, 90, 180):
        s.append(txt(xm(a), y1 + 18, f"{a}°".replace("-", "−"), 13, INK3))
    s.append(txt(x0 - 6, y0 - 8, "dB", 13, INK3, anchor="end"))
    s.append(polyline(xm(dl), ym(resp), NAVY, 2.2))
    s.append(txt(xm(0), ym(-6), f"±{half:.1f}°: within 0.2 dB", 13, AMBER, weight="700"))
    s.append(txt(xm(0), y1 + 36, "phase of the swept element", 13, INK3))
    s.append("</svg>")
    return "\n".join(s)


def main() -> None:
    write("L17-cal-patterns", cal_patterns(), PAGE)
    write("L17-cal-pair", cal_pair(), PAGE)


if __name__ == "__main__":
    main()
