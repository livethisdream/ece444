#!/usr/bin/env python3
"""Generate the L24 Lab (null steering) lesson-page figures as inline SVG.

  - L24-element-settings : (retired; not generated) the eight gain
                           percentages and phase offsets of the dry-run table
  - L24-monopulse        : sum and delta together, and the error the GUI plots
                           (phaser #97): |delta|/|sum| signed by side, at 10.0 GHz

Array is the PHASER's: N = 8, d = 14 mm, worked at 10.443 GHz, the Find HB100
frequency of phaser-00 in the 2026-10-23 dry run (d/lambda = 0.487), with the
two ADAR1000 subarrays (elements 1-4 and 5-8) forming the digital pair. The
expected-sweep figures (L24-sweep-notch, L24-delta-beam) were retired with the
L24 Lab pass: they drew a -21 dB floor the hardware does not have, and the lab
explains the nulls rather than redrawing the bench traces.
The figures carry no equations (house rule); numbers and short words only.

    python3 scripts/graphics/m3_l24_lab.py
    -> book/extras/viz/img/L24-*.svg
"""

from __future__ import annotations

import io
import re
from pathlib import Path

import numpy as np
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from svg_font_stack import apply_font_stack

NAVY, BLUE, RED, GREEN, ORANGE, GRAY = "#004a85", "#0067b9", "#b01e24", "#1d7a4d", "#e67e22", "#5a5a5a"
INK, RULE = "#1a1a1a", "#c7d2e0"
ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "book/extras/viz/img"

N = 8
DL = 0.014 * 10.443e9 / 3.00e8   # d / lambda at phaser-00's 10.443 GHz
KD = 2 * np.pi * DL
NIDX = np.arange(N)
NULL_ANG = 22.5                  # the course example's null direction

plt.rcParams.update({
    "svg.fonttype": "none",
    "font.size": 13,
    "axes.edgecolor": "#8a929c",
    "axes.labelcolor": INK,
    "xtick.color": GRAY, "ytick.color": GRAY,
    "text.color": INK,
    "axes.linewidth": 1.0,
    "legend.frameon": False,
})


def finalize(fig, name: str) -> None:
    buf = io.StringIO()
    fig.savefig(buf, format="svg", transparent=True, bbox_inches="tight", pad_inches=0.06)
    plt.close(fig)
    s = buf.getvalue()
    s = s[s.index("<svg"):]
    s = apply_font_stack(s)
    (OUT / f"{name}.svg").write_text(s, encoding="utf-8")
    print(f"wrote {OUT / (name + '.svg')}")


# ---------------------------------------------------------------- array maths
def steer(theta_deg: float) -> np.ndarray:
    return np.exp(-1j * NIDX * KD * np.sin(np.deg2rad(theta_deg)))


def null_weights(theta1_deg: float, theta0_deg: float = 0.0):
    wd, wn = steer(theta0_deg), steer(theta1_deg)
    r = np.vdot(wn, wd) / np.vdot(wn, wn)
    return wd - r * wn, r


def response(w: np.ndarray, theta_deg) -> np.ndarray:
    A = np.exp(1j * np.outer(np.sin(np.deg2rad(np.atleast_1d(theta_deg))), NIDX) * KD)
    return np.abs(A @ w)


# ------------------------------------------------------------------ figure 1
def element_settings() -> None:
    """What the student types into Element Gains and Phase Control."""
    w, _ = null_weights(NULL_ANG)
    g = 100 * np.abs(w) / np.abs(w).max()
    p = np.rad2deg(np.angle(w))
    el = np.arange(1, N + 1)

    fig, (a1, a2) = plt.subplots(2, 1, figsize=(4.8, 5.4))
    a1.bar(el, g, width=0.62, color=NAVY)
    for x, y in zip(el, g):
        a1.text(x, y + 3, f"{y:.0f}", ha="center", va="bottom", fontsize=11, color=INK)
    a1.set_ylim(0, 118)
    a1.set_xticks(el)
    a1.set_xlabel("element")
    a1.set_ylabel("element gain (%)")
    a1.grid(axis="y", color=RULE, linewidth=0.8)
    a1.set_axisbelow(True)

    a2.axhline(0, color="#8a929c", linewidth=1.0)
    a2.vlines(el, 0, p, color=ORANGE, linewidth=2.4)
    a2.plot(el, p, "o", color=ORANGE, markersize=6)
    for x, y in zip(el, p):
        off = 2.2 if y >= 0 else -2.2
        a2.text(x, y + off, f"{y:+.1f}", ha="center",
                va="bottom" if y >= 0 else "top", fontsize=10.5, color=INK)
    a2.set_ylim(-21, 21)
    a2.set_xticks(el)
    a2.set_xlabel("element")
    a2.set_ylabel("phase offset (deg)")
    a2.grid(axis="y", color=RULE, linewidth=0.8)
    a2.set_axisbelow(True)

    fig.tight_layout()
    finalize(fig, "L24-element-settings")


# ------------------------------------------------------------------ figure 4
def monopulse() -> None:
    """Sum and delta, and the error the GUI plots, as house-style SVG.

    Worked at 10.0 GHz, the lesson's frequency (no kit's, so no Part 1
    answer). The error is the kit's since livethisdream/phaser #97:
    sign(phase(sum * conj(delta))) * |delta| / |sum|, clamped to +/-1,
    positive when the source sits on the +theta side of the beam. With the
    two subarrays four elements apart, |delta| / |sum| = |tan(2 psi)|, so
    near the beam the error is about 2 kd theta: 0.10 per degree here.
    """
    from svg_font_stack import apply_font_stack as _afs
    kd = 2 * np.pi * 0.014 * 10.0e9 / 3.00e8
    th = np.linspace(-20, 20, 1601)
    A = np.exp(1j * np.outer(np.sin(np.deg2rad(th)), NIDX) * kd)
    sig = A @ np.ones(N)
    dlt = A @ np.r_[np.ones(4), -np.ones(4)]
    ps = np.maximum(20 * np.log10(np.maximum(np.abs(sig), 1e-9) / N), -40)
    pd = np.maximum(20 * np.log10(np.maximum(np.abs(dlt), 1e-9) / N), -40)
    side = np.sign(np.angle(sig * np.conj(dlt)))
    side *= np.sign(side[np.argmin(np.abs(th - 3))])     # the kit's convention: + on the +theta side
    err = np.clip(side * np.abs(dlt) / np.maximum(np.abs(sig), 1e-12), -1, 1)
    slope = 2 * kd * np.pi / 180

    W, PH, GAP = 560, 250, 34
    L, R, T = 72, 16, 12
    pw = W - L - R
    ph = PH - 44
    H = T + PH + GAP + ph + 58

    def X(a):
        return L + (a + 20) / 40 * pw

    out = [f'<svg viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Top: sum and '
           f'delta beam levels from minus 20 to plus 20 degrees at 10.0 GHz; the sum is flat at its peak while the '
           f'delta passes through a zero on the target. Bottom: the error the GUI plots, the delta over sum ratio '
           f'signed by side, zero on the target, close to a straight line of slope {slope:.2f} per degree near it, '
           f'clamped at plus and minus 1, and flipping sign past the sum beam\'s first nulls.">']

    def frame(y0, ylo, yhi, ticks, ylab):
        Y = lambda v: y0 + (yhi - v) / (yhi - ylo) * ph
        out.append(f'<rect x="{L}" y="{y0}" width="{pw}" height="{ph}" fill="#f6f9fc" stroke="{RULE}" stroke-width="1"/>')
        for v in ticks:
            out.append(f'<line x1="{L}" y1="{Y(v):.1f}" x2="{L + pw}" y2="{Y(v):.1f}" stroke="{RULE}" stroke-width="0.8"/>')
            lab = f"{v:g}".replace("-", "−")
            out.append(f'<text x="{L - 8}" y="{Y(v) + 6:.1f}" text-anchor="end" font-size="16" fill="{GRAY}">{lab}</text>')
        for a in (-20, -10, 0, 10, 20):
            out.append(f'<line x1="{X(a):.1f}" y1="{y0}" x2="{X(a):.1f}" y2="{y0 + ph}" stroke="{RULE}" stroke-width="0.8"/>')
            lab = f"{a}°" if a >= 0 else f"−{-a}°"
            out.append(f'<text x="{X(a):.1f}" y="{y0 + ph + 22}" text-anchor="middle" font-size="16" fill="{GRAY}">{lab}</text>')
        out.append(f'<text x="20" y="{y0 + ph / 2}" text-anchor="middle" font-size="17" fill="{INK}" '
                   f'transform="rotate(-90 20 {y0 + ph / 2})">{ylab}</text>')
        return Y

    def line(xs, ys, Y, col, lw):
        pts = " ".join(f"{X(a):.1f},{Y(v):.1f}" for a, v in zip(xs, ys))
        out.append(f'<polyline points="{pts}" fill="none" stroke="{col}" stroke-width="{lw}" stroke-linejoin="round"/>')

    # top: the two beams
    Y1 = frame(T, -40, 0, (0, -10, -20, -30, -40), "level (dB)")
    line(th, ps, Y1, "#9aa3ad", 2.0)
    line(th, pd, Y1, NAVY, 2.8)
    for k, (col, lw, lab) in enumerate((("#9aa3ad", 2.0, "Σ, sum"), (NAVY, 2.8, "Δ, difference"))):
        yy = Y1(-27 - 8 * k)
        out.append(f'<line x1="{X(4.0):.1f}" y1="{yy:.1f}" x2="{X(6.4):.1f}" y2="{yy:.1f}" stroke="{col}" stroke-width="{lw + 0.6}"/>')
        out.append(f'<text x="{X(6.9):.1f}" y="{yy + 6:.1f}" font-size="17" fill="{INK}">{lab}</text>')
    out.append(f'<text x="{X(-1.4):.1f}" y="{Y1(-36) + 6:.1f}" text-anchor="end" font-size="17" font-weight="700" fill="{NAVY}">zero on target</text>')
    # bottom: the error
    y2 = T + PH + GAP
    Y2 = frame(y2, -1.2, 1.2, (-1, 0, 1), "error")
    lin = np.abs(th) <= 6
    line(th[lin], slope * th[lin], Y2, GREEN, 6.0)
    line(th, err, Y2, NAVY, 2.6)
    out.append(f'<text x="{X(-19):.1f}" y="{Y2(0.62) + 6:.1f}" font-size="16" fill="{GREEN}" font-weight="700">'
               f'slope {slope:.2f} per degree</text>')
    out.append(f'<text x="{X(1.5):.1f}" y="{Y2(-0.62) + 6:.1f}" font-size="16" fill="{INK}">+θ side reads +</text>')
    out.append(f'<text x="{L + pw / 2}" y="{H - 12}" text-anchor="middle" font-size="17" fill="{INK}">'
               f'target angle from the beam</text>')
    out.append("</svg>")
    (OUT / "L24-monopulse.svg").write_text(_afs("\n".join(out)) + "\n", encoding="utf-8")
    print(f"wrote {OUT / 'L24-monopulse.svg'}")


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    # element_settings() is no longer generated: its table at 10.443 GHz is a
    # Part 1 answer, and no page shows it now. The SVG stays (house rule on
    # old figures); the function stays for reference.
    monopulse()


if __name__ == "__main__":
    main()
