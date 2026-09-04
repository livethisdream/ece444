#!/usr/bin/env python3
"""Generate the L23 (Antenna Pattern Lab) deck data-plots as inline SVG.

L23:
  - L23-time-vs-angle  : the same hand-rotation run plotted against elapsed
                         time (top) and against true source angle (bottom).
                         Lobe amplitudes are identical; lobe spacing is not.
  - L23-steer-compare  : measured pattern (element factor x array factor) for
                         a broadside beam and a 30 deg steered beam, on the
                         true-angle axis: scan loss and sidelobe asymmetry.

Pattern model: N = 8 uniform array, d = 14 mm, HB100 at 10.525 GHz
(lambda = 28.5 mm, d/lambda = 0.491), ideal element power pattern cos(theta)
-- the projected-aperture scan-loss canon. Broadside first sidelobe lands at
-13.1 dBc; the 30 deg steered peak sits 0.6 dB down.

Exported as SVG with live <text> (svg.fonttype='none'), then font-family is
rewritten to 'inherit' so the injected figure picks up the deck's Source Sans
Pro. Transparent background, USAFA palette, no baked formulas.

    python3 scripts/graphics/m3_l23_pattern_lab.py
    -> writes book/extras/slides/fig/{L23-time-vs-angle,L23-steer-compare}.svg
"""

from __future__ import annotations
import io
import re
from pathlib import Path

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

NAVY, BLUE, RED, GREEN, ORANGE, GRAY = "#004a85", "#0067b9", "#b01e24", "#1d7a4d", "#8a5a00", "#5a5a5a"
INK, RULE = "#1a1a1a", "#c7d2e0"
OUT = Path(__file__).resolve().parents[2] / "book/extras/slides/fig"

C = 3.0e8
FREQ = 10.525e9          # HB100 nominal
LAM = C / FREQ           # 28.50 mm
D = 0.014                # element spacing
N = 8

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
    s = re.sub(r"font-family:[^;}]*", "font-family:inherit", s)
    (OUT / f"{name}.svg").write_text(s, encoding="utf-8")
    print(f"wrote {OUT / (name + '.svg')}")


# ---------------------------------------------------------------- physics ---
def pattern_db(theta_deg, steer_deg):
    """Element factor x array factor, in dB, referenced to the broadside peak.

    Element power pattern cos(theta) (field sqrt(cos theta)); uniform N=8
    array factor with the standard peak-1 normalization.
    """
    th = np.radians(np.asarray(theta_deg, dtype=float))
    t0 = np.radians(steer_deg)
    psi = 2 * np.pi * (D / LAM) * (np.sin(th) - np.sin(t0))
    den = N * np.sin(psi / 2)
    small = np.abs(den) < 1e-12
    af = np.where(small, 1.0, np.sin(N * psi / 2) / np.where(small, 1.0, den))
    ef = np.clip(np.cos(th), 1e-9, None)
    return 20 * np.log10(np.abs(af) + 1e-12) + 10 * np.log10(ef)


def warp(u, coeffs=(0.45, 0.30, -0.18)):
    """Monotone time warp on [0,1]: g(0)=0, g(1)=1, g' = 1 + sum c_k sin(2 pi k u).

    Models a hand that speeds up and slows down during the walk. With
    sum|c_k| < 1 the map stays monotone, so no angle is visited twice.
    """
    u = np.asarray(u, dtype=float)
    g = u.copy()
    for k, c in enumerate(coeffs, start=1):
        g = g + (c / (2 * np.pi * k)) * (1.0 - np.cos(2 * np.pi * k * u))
    return g


def warp_inverse(gv, coeffs=(0.45, 0.30, -0.18), n=200001):
    """Numeric inverse of warp, for placing angle tick marks on the time axis."""
    u = np.linspace(0.0, 1.0, n)
    return np.interp(gv, warp(u, coeffs), u)


def first_sidelobes(steer_deg):
    """(left, right) first-sidelobe peaks as (angle_deg, dBc rel. own peak)."""
    th = np.linspace(-90.0, 90.0, 400001)
    p = pattern_db(th, steer_deg)
    peak = p.max()
    u = np.sin(np.radians(th)) - np.sin(np.radians(steer_deg))
    w = LAM / (N * D)
    band = (np.abs(u) > w) & (np.abs(u) < 2 * w)
    out = []
    for side in (u < 0, u > 0):
        m = band & side
        if not m.any():
            out.append(None)
            continue
        j = np.argmax(np.where(m, p, -1e9))
        out.append((th[j], p[j] - peak))
    return out


# ------------------------------------------------- fig 1: time vs angle -----
def time_vs_angle() -> None:
    """One hand-rotation run, drawn twice: against elapsed time and against
    the true source angle. Same peaks, different spacing."""
    rng = np.random.default_rng(444)
    T = 7.4                                    # seconds for the -90 -> +90 walk
    u = np.linspace(0.0, 1.0, 3000)
    t = u * T
    theta = -90.0 + 180.0 * warp(u)            # hand-like: angle vs time
    trace = pattern_db(theta, 0.0)
    trace = np.maximum(trace, -34.0)
    trace = trace + rng.normal(0.0, 0.18, trace.size)

    fig, (ax_t, ax_a) = plt.subplots(2, 1, figsize=(9.6, 7.0))
    YLO, YHI = -34, 11

    # --- top: what the GUI paints (Signal vs Time) ---
    ax_t.plot(t, trace, color=NAVY, lw=1.7)
    ax_t.set_xlim(0, T)
    ax_t.set_ylim(YLO, YHI)
    ax_t.set_yticks(np.arange(-30, 1, 10))
    ax_t.set_xlabel("elapsed time (s)")
    ax_t.set_ylabel("received amplitude (dBc)")
    ax_t.set_title("what the plot shows: amplitude against time", color=INK,
                   fontsize=13.5, pad=8)
    ax_t.grid(True, color=RULE, lw=0.7, alpha=0.7)
    ax_t.set_axisbelow(True)

    # tick marks at the instants the source crossed each 30 deg: under a
    # hand-like walk these land unevenly, which is the whole point.
    marks = np.arange(-60, 61, 30)
    tm = T * warp_inverse((marks + 90.0) / 180.0)
    for ang, tt in zip(marks, tm):
        lab = "0°" if ang == 0 else f"{ang:+d}°".replace("-", "−")
        ax_t.plot([tt, tt], [YLO, -31.0], color=ORANGE, lw=2.0, solid_capstyle="butt")
        ax_t.text(tt, -30.2, lab, color=ORANGE,
                  fontsize=10.5, ha="center", va="bottom")

    # --- bottom: the same samples against true angle ---
    ax_a.plot(theta, trace, color=NAVY, lw=1.7)
    ax_a.set_xlim(-90, 90)
    ax_a.set_ylim(YLO, YHI)
    ax_a.set_yticks(np.arange(-30, 1, 10))
    ax_a.set_xticks(np.arange(-90, 91, 30))
    ax_a.set_xlabel("true source angle (deg)")
    ax_a.set_ylabel("received amplitude (dBc)")
    ax_a.set_title("what it means: amplitude against angle", color=INK,
                   fontsize=13.5, pad=8)
    ax_a.grid(True, color=RULE, lw=0.7, alpha=0.7)
    ax_a.set_axisbelow(True)

    # annotate the three lobes on both panels at the same amplitudes
    lobes = [(0.0, 0.0, NAVY, "0 dBc")]
    for (ang, db) in first_sidelobes(0.0):
        lobes.append((ang, db, RED, f"{db:.1f} dBc"))
    for ang, db, color, label in lobes:
        tt = T * warp_inverse((ang + 90.0) / 180.0)
        for ax, x in ((ax_t, tt), (ax_a, ang)):
            ax.annotate(label, xy=(x, db + 0.4), xytext=(x, db + 6.2),
                        color=color, fontsize=11, ha="center", va="bottom",
                        arrowprops=dict(arrowstyle="-", color=GRAY, lw=0.9))

    fig.tight_layout(h_pad=2.0)
    finalize(fig, "L23-time-vs-angle")


# ------------------------------------------------ fig 2: steer compare ------
def steer_compare() -> None:
    """Broadside and 30 deg steered runs on the true-angle axis."""
    th = np.linspace(-90, 90, 6001)
    p0 = np.maximum(pattern_db(th, 0.0), -34.0)
    p30 = np.maximum(pattern_db(th, 30.0), -34.0)

    fig, ax = plt.subplots(figsize=(9.6, 4.6))
    ax.plot(th, p0, color=NAVY, lw=2.0, label="beam at 0 deg")
    ax.plot(th, p30, color=ORANGE, lw=2.0, label="beam at 30 deg")

    ax.set_xlim(-90, 90)
    ax.set_ylim(-34, 4)
    ax.set_xticks(np.arange(-90, 91, 30))
    ax.set_xlabel("true source angle (deg)")
    ax.set_ylabel("received amplitude (dB, broadside peak = 0)")
    ax.grid(True, color=RULE, lw=0.7, alpha=0.7)
    ax.set_axisbelow(True)
    ax.legend(loc="upper left", fontsize=12)

    # scan loss marker
    pk30 = p30.max()
    a30 = th[np.argmax(p30)]
    ax.plot([a30, a30], [pk30, 0.0], color=GREEN, lw=1.6)
    ax.plot([-90, a30], [0.0, 0.0], color=GREEN, lw=0.9, ls=(0, (4, 4)))
    ax.annotate(f"scan loss {pk30:.1f} dB", xy=(a30, pk30 / 2),
                xytext=(a30 + 16, -6.0), color=GREEN, fontsize=11.5,
                va="center", arrowprops=dict(arrowstyle="-", color=GREEN, lw=0.9))

    # asymmetric first sidelobes of the steered run
    for (ang, db) in first_sidelobes(30.0):
        ax.annotate(f"{db:.1f} dBc", xy=(ang, db + pk30), xytext=(ang, db + pk30 + 5.0),
                    color=RED, fontsize=11, ha="center",
                    arrowprops=dict(arrowstyle="-", color=GRAY, lw=0.9))
    ax.text(-87, -7.5, "equal sidelobes at broadside, unequal when steered",
            color=GRAY, fontsize=11, va="center")

    fig.tight_layout()
    finalize(fig, "L23-steer-compare")


if __name__ == "__main__":
    OUT.mkdir(parents=True, exist_ok=True)
    time_vs_angle()
    steer_compare()
    print("first sidelobes, broadside:", first_sidelobes(0.0))
    print("first sidelobes, 30 deg   :", first_sidelobes(30.0))
