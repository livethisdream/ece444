#!/usr/bin/env python3
"""Generate the L21 lesson figures: the kit's beam sweep against an azimuth sweep.

L21:
  - L21-beam-vs-azimuth-0  : the beam sweep (HB100 at boresight, beam stepped;
                             the Rectangular plot, against commanded angle)
                             beside the azimuth sweep (beam held at 0 deg, HB100
                             carried around in azimuth, against source angle).
                             Both in dBc of their own main-lobe peak.
  - L21-beam-vs-azimuth-30 : the same pair at 30 deg: the beam sweep with the
                             HB100 at 30 deg, the azimuth sweep with the beam
                             held at 30 deg.
  - L21-psi-two-ways       : |AF|^2 against psi = kd(sin theta_src - sin theta_0),
                             with the points each method visits: stepping
                             theta_0 past a fixed source and moving theta_src
                             past a fixed beam land on the same curve.

Model, matching the lesson text: N = 8 uniform, d = 14 mm, 10.0 GHz (off every kit's HB100, so no figure gives a Part 1 answer)
(lambda = 30.0 mm). The beam sweep steps the element-to-element phase one
2.8125 deg LSB per point and reads |AF|^2 at a fixed source, so the element
pattern is one constant and drops out in dBc. The azimuth sweep reads
EF x AF with the ideal cos(theta) element power pattern. Both carry the same
noise floor, 23 dB below the peak (the L20 Lab), added in power.

    python3 scripts/graphics/m3_l21_scan_compare.py
    -> writes book/extras/viz/img/{L21-beam-vs-azimuth-0,L21-beam-vs-azimuth-30,
       L21-psi-two-ways}.svg
"""

from __future__ import annotations
import io
from pathlib import Path

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from svg_font_stack import apply_font_stack

NAVY, ORANGE, GRAY, RED = "#004a85", "#d9822b", "#5a5a5a", "#b01e24"
INK, RULE = "#1a1a1a", "#c7d2e0"
OUT = Path(__file__).resolve().parents[2] / "book/extras/viz/img"

C = 299792458.0
FREQ = 10.0e9
LAM = C / FREQ
D = 0.014
N = 8
LSB = np.radians(2.8125)
KD = 2 * np.pi * D / LAM
FLOOR_DB = -23.0
YMIN = -30.0

plt.rcParams.update({
    "svg.fonttype": "none",
    "font.size": 13,
    "axes.edgecolor": "#8a929c",
    "axes.labelcolor": INK,
    "xtick.color": GRAY, "ytick.color": GRAY,
    "xtick.labelsize": 13, "ytick.labelsize": 13,
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


def af_power(psi):
    """|AF|^2 of the uniform N-element array, peak 1."""
    den = N * np.sin(psi / 2)
    small = np.abs(den) < 1e-12
    af = np.where(small, 1.0, np.sin(N * psi / 2) / np.where(small, 1.0, den))
    return af ** 2


def with_floor_db(p):
    """Add the noise floor in power, then express in dB of the trace's peak."""
    q = p + 10 ** (FLOOR_DB / 10)
    return 10 * np.log10(q / q.max())


def beam_sweep(source_deg):
    """The Rectangular plot: commanded angle and dBc, one point per LSB."""
    k = np.arange(-400, 401)
    s0 = k * LSB / KD
    s0 = s0[np.abs(s0) <= 1.0]
    psi = KD * (np.sin(np.radians(source_deg)) - s0)
    return np.degrees(np.arcsin(s0)), with_floor_db(af_power(psi))


def azimuth_sweep(beam_deg):
    """Beam held, source moved in azimuth: source angle and dBc."""
    th = np.radians(np.linspace(-90, 90, 3601))
    psi = KD * (np.sin(th) - np.sin(np.radians(beam_deg)))
    ef = np.clip(np.cos(th), 0, None)
    return np.degrees(th), with_floor_db(af_power(psi) * ef)


def draw(angle_deg: float, name: str) -> None:
    fig, ax = plt.subplots(figsize=(5.8, 3.5))
    xa, ya = azimuth_sweep(angle_deg)
    xb, yb = beam_sweep(angle_deg)
    ax.axhline(FLOOR_DB, color=GRAY, lw=1.0, ls=(0, (4, 3)), zorder=1)
    ax.plot(xb, yb, "o", mfc="none", mec=ORANGE, mew=1.1, ms=3.6, zorder=2,
            label="beam sweep")
    ax.plot(xa, ya, color=NAVY, lw=1.6, zorder=3, label="azimuth sweep")
    ax.set_xlim(-90, 90)
    ax.set_ylim(YMIN, 1.5)
    ax.set_xticks(np.arange(-90, 91, 30))
    ax.set_yticks(np.arange(-30, 1, 10))
    ax.set_xlabel("angle (deg)")
    ax.set_ylabel("level (dBc)")
    ax.grid(color=RULE, lw=0.7, zorder=0)
    ax.spines[["top", "right"]].set_visible(False)
    # legend in the empty upper corner away from the main lobe
    corner = "upper left" if angle_deg >= 0 else "upper right"
    ax.legend(loc=corner, fontsize=13, handlelength=1.4, borderaxespad=0.2)
    # floor label in the empty strip just above the dashed line, on the side
    # away from the main lobe, placed between lobes from the data
    x_lab = -88 if angle_deg >= 0 else 88
    ax.text(x_lab, FLOOR_DB - 0.6, "noise floor", color=GRAY, fontsize=12,
            ha="left" if angle_deg >= 0 else "right", va="top")
    finalize(fig, name)


def psi_two_ways() -> None:
    """|AF|^2 in dB against psi, with each method's sample points on it."""
    fig, ax = plt.subplots(figsize=(5.8, 3.3))
    psi = np.radians(np.linspace(-180, 180, 3601))
    ax.plot(np.degrees(psi), 10 * np.log10(af_power(psi) + 1e-6), color=GRAY,
            lw=1.2, zorder=1)
    # beam sweep: source at boresight, theta_0 stepped one LSB at a time
    k = np.arange(-400, 401)
    s0 = k * LSB / KD
    s0 = s0[np.abs(s0) <= 1.0][::3]
    pb = KD * (0.0 - s0)
    # azimuth sweep: beam at 0, source moved every 3 deg
    th = np.radians(np.arange(-90, 91, 3))
    pa = KD * np.sin(th)
    ax.plot(np.degrees(pb), 10 * np.log10(af_power(pb) + 1e-6), "o", mfc="none",
            mec=ORANGE, mew=1.1, ms=5, zorder=2, label=r"beam sweep: $\theta_0$ stepped")
    ax.plot(np.degrees(pa), 10 * np.log10(af_power(pa) + 1e-6), "o", color=NAVY,
            ms=2.6, zorder=3, label=r"azimuth sweep: $\theta_\mathrm{src}$ moved")
    ax.set_xlim(-180, 180)
    ax.set_ylim(-30, 1.5)
    ax.set_xticks(np.arange(-180, 181, 60))
    ax.set_yticks(np.arange(-30, 1, 10))
    ax.set_xlabel(r"$\psi$ (deg)")
    ax.set_ylabel(r"$|AF|^2$ (dB)")
    ax.grid(color=RULE, lw=0.7, zorder=0)
    ax.spines[["top", "right"]].set_visible(False)
    ax.legend(loc="lower center", bbox_to_anchor=(0.5, 1.0), ncol=1, fontsize=13,
              handlelength=1.2)
    finalize(fig, "L21-psi-two-ways")


def report() -> None:
    """Print the numbers the lesson quotes, for checking against the text."""
    for a in (0, 30):
        for nm, (x, y) in (("azimuth", azimuth_sweep(a)), ("beam", beam_sweep(a))):
            lo = [i for i in range(1, len(y) - 1) if y[i] > y[i - 1] and y[i] >= y[i + 1]]
            print(f"{nm} {a}:", [(round(x[i], 1), round(y[i], 1)) for i in lo if y[i] > -22])


if __name__ == "__main__":
    report()
    draw(0.0, "L21-beam-vs-azimuth-0")
    draw(30.0, "L21-beam-vs-azimuth-30")
    psi_two_ways()
