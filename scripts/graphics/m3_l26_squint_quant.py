#!/usr/bin/env python3
"""Generate the L26 deck figures (grating lobes, beam squint, phase quantization).

L26:
  - L26-grating-thinning : broadside patterns of the 8-element PHASER row thinned
                           to 14 / 28 / 42 / 56 mm effective spacing, grating
                           lobes marked (10.3 GHz).
  - L26-squint-band      : one phase ramp set for 45 deg at 10.525 GHz, evaluated
                           at 10.025 / 10.525 / 11.025 GHz; peaks marked.
  - L26-quant-staircase  : commanded element phase (ideal ramp vs 2-bit and 4-bit
                           staircases) and the patterns they produce.

Exported as SVG with live <text> (svg.fonttype='none'), then font-family is
rewritten to 'inherit' so the injected figure picks up the deck font.
Transparent background, USAFA palette, and NO equations in the graphic --
axis labels, legends and measured numbers only (COURSE_SPEC 3.4).

    python3 scripts/graphics/m3_l26_squint_quant.py
    -> writes book/extras/slides/fig/L26-{grating-thinning,squint-band,
                                          quant-staircase}.svg
"""

from __future__ import annotations
import io
import re
from pathlib import Path

import numpy as np
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

NAVY, BLUE, RED, GREEN, AMBER, GREY = (
    "#004a85", "#0067b9", "#b01e24", "#1d7a4d", "#8a5a00", "#5a5a5a")
INK, RULE = "#1a1a1a", "#c7d2e0"
OUT = Path(__file__).resolve().parents[2] / "book/extras/slides/fig"

C = 2.99792458e8
FLOOR = -40.0

plt.rcParams.update({
    "svg.fonttype": "none",
    "font.size": 13,
    "axes.edgecolor": "#8a929c",
    "axes.labelcolor": INK,
    "xtick.color": GREY, "ytick.color": GREY,
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


def af_db(theta_deg, n_on, d_m, lam, phase=None):
    """Array factor in dB for `n_on` isotropic elements at spacing d_m, with an
    optional per-element commanded phase (radians). Peak normalised to 0 dB."""
    n = np.arange(n_on)
    kd = 2 * np.pi * d_m / lam
    a = np.zeros(n_on) if phase is None else phase
    e = np.exp(1j * (n[:, None] * kd * np.sin(np.radians(theta_deg))[None, :] + a[:, None]))
    mag = np.abs(e.sum(0)) / n_on
    db = 20 * np.log10(np.maximum(mag, 1e-9))
    return db - db.max()


def style_db_axis(ax, xlo=-90, xhi=90, xstep=30):
    ax.set_ylim(FLOOR, 2)
    ax.set_xlim(xlo, xhi)
    ax.set_xticks(np.arange(xlo, xhi + 1, xstep))
    ax.set_yticks(np.arange(FLOOR, 1, 10))
    ax.grid(True, color=RULE, lw=0.7)
    ax.set_axisbelow(True)


# --------------------------------------------------------------------------
def grating_thinning() -> None:
    """Thin the 14 mm row and watch full-height lobes walk into visible space."""
    lam = C / 10.3e9                       # array design centre, 29.1 mm
    th = np.linspace(-90, 90, 6001)
    cases = [(14e-3, 8, "14 mm - all 8 elements"),
             (28e-3, 4, "28 mm - every 2nd element"),
             (42e-3, 3, "42 mm - every 3rd element"),
             (56e-3, 2, "56 mm - every 4th element")]

    fig, axes = plt.subplots(2, 2, figsize=(10.0, 5.6), sharex=True, sharey=True)
    for ax, (d, non, title) in zip(axes.ravel(), cases):
        db = af_db(th, non, d, lam)
        ax.plot(th, db, color=NAVY, lw=2.0)
        ax.set_title(title, fontsize=12.5, color=NAVY, pad=6)
        style_db_axis(ax)
        # mark every full-height lobe away from broadside
        ratio = lam / d
        for m in (1, 2):
            for sgn in (1, -1):
                v = sgn * m * ratio
                if abs(v) <= 1:
                    g = np.degrees(np.arcsin(v))
                    ax.axvline(g, color=AMBER, lw=1.3, ls=(0, (4, 3)))
                    ax.annotate(f"{g:+.0f}°", xy=(g, -3), xytext=(g, -12),
                                color=AMBER, fontsize=11.5, ha="center",
                                fontweight="bold")
        if db[-1] > -6.0:
            ax.annotate("full height at\nthe horizon", xy=(89, -2.5), xytext=(48, -27),
                        color=AMBER, fontsize=10.5, ha="center",
                        bbox=dict(fc="white", ec="none", pad=1.5),
                        arrowprops=dict(arrowstyle="->", color=AMBER, lw=1.1))
        if non == 8:
            ax.text(0, -34, "no full-height lobe anywhere in view",
                    color=GREEN, fontsize=11, ha="center",
                    bbox=dict(fc="white", ec="none", pad=1.5))
    for ax in axes[1]:
        ax.set_xlabel("angle from broadside (deg)")
    for ax in axes[:, 0]:
        ax.set_ylabel("relative power (dB)")
    fig.tight_layout()
    finalize(fig, "L26-grating-thinning")


# --------------------------------------------------------------------------
def squint_band() -> None:
    """One phase ramp, three frequencies: the beam walks with frequency."""
    d, n_on, th0 = 14e-3, 8, 45.0
    f0 = 10.525e9
    lam0 = C / f0
    n = np.arange(n_on)
    ramp = -n * (2 * np.pi * d / lam0) * np.sin(np.radians(th0))
    th = np.linspace(5, 85, 8001)

    fig, ax = plt.subplots(figsize=(9.4, 4.5))
    series = [(11.025e9, GREEN, "11.025 GHz", -7.5, 8.0),
              (f0, NAVY, "10.525 GHz (phases set here)", 0.0, 3.6),
              (10.025e9, RED, "10.025 GHz", +7.5, 8.0)]
    for f, col, lab, dx, dy in series:
        db = af_db(th, n_on, d, C / f, phase=ramp)
        ax.plot(th, db, color=col, lw=2.1, label=lab)
        pk = th[db.argmax()]
        ax.plot([pk], [0.0], marker="v", color=col, ms=8, clip_on=False)
        ax.annotate(f"{pk:.1f}°", xy=(pk, 0.8), xytext=(pk + dx, dy),
                    color=col, fontsize=12, ha="center", fontweight="bold",
                    arrowprops=None if dx == 0 else
                    dict(arrowstyle="-", color=col, lw=1.0))

    ax.axvline(th0, color=GREY, lw=1.1, ls=(0, (3, 3)))
    ax.annotate("commanded 45°", xy=(th0, -33), xytext=(th0 - 1.5, -33),
                color=GREY, fontsize=11, ha="right")
    style_db_axis(ax, xlo=15, xhi=75, xstep=10)
    ax.set_ylim(FLOOR, 11)
    ax.set_yticks(np.arange(FLOOR, 1, 10))
    ax.set_xlabel("angle from broadside (deg)")
    ax.set_ylabel("relative power (dB)")
    ax.legend(loc="lower right", fontsize=11.5)
    fig.tight_layout()
    finalize(fig, "L26-squint-band")


# --------------------------------------------------------------------------
def quant_staircase() -> None:
    """Left: the commanded phase the hardware can actually produce.
       Right: what the staircase error does to the pattern."""
    d, n_on, th0 = 14e-3, 8, 45.0
    lam = C / 10.525e9
    n = np.arange(n_on)
    ideal = -n * (2 * np.pi * d / lam) * np.sin(np.radians(th0))

    def q(bits):
        lsb = 2 * np.pi / 2 ** bits
        return np.round(ideal / lsb) * lsb

    lag = lambda a: np.degrees(-a)          # commanded lag, unwrapped
    th = np.linspace(-90, 90, 12001)

    fig, (axL, axR) = plt.subplots(1, 2, figsize=(10.6, 4.5),
                                   gridspec_kw={"width_ratios": [1.0, 1.25]})

    en = n + 1                                   # Rx1..Rx8, as the GUI labels them
    axL.plot(en, lag(ideal), color=GREY, lw=1.6, ls=(0, (4, 3)),
             marker="o", ms=5, mfc="white", label="ideal ramp")
    axL.step(en, lag(q(2)), where="mid", color=RED, lw=2.2, label="2-bit steps")
    axL.step(en, lag(q(4)), where="mid", color=NAVY, lw=2.0, label="4-bit steps")
    axL.set_xlabel("element number")
    axL.set_ylabel("commanded phase lag (deg)")
    axL.set_xticks(en)
    axL.set_yticks(np.arange(0, 1081, 180))
    axL.set_ylim(-60, 1010)
    axL.grid(True, color=RULE, lw=0.7)
    axL.set_axisbelow(True)
    axL.legend(loc="upper left", fontsize=11)

    for bits, col, lw, lab in ((None, GREY, 1.5, "ideal"),
                               (4, NAVY, 2.0, "4 bits"),
                               (2, RED, 2.2, "2 bits")):
        ph = ideal if bits is None else q(bits)
        db = af_db(th, n_on, d, lam, phase=ph)
        axR.plot(th, db, color=col, lw=lw, label=lab,
                 ls=(0, (4, 3)) if bits is None else "-")
    style_db_axis(axR)
    axR.set_xlabel("angle from broadside (deg)")
    axR.set_ylabel("relative power (dB)")
    axR.legend(loc="lower right", fontsize=11)
    axR.annotate("quantization lobe", xy=(-8.1, -7.8), xytext=(-52, -4.5),
                 color=RED, fontsize=11.5, fontweight="bold",
                 arrowprops=dict(arrowstyle="->", color=RED, lw=1.3))
    fig.tight_layout()
    finalize(fig, "L26-quant-staircase")


if __name__ == "__main__":
    OUT.mkdir(parents=True, exist_ok=True)
    grating_thinning()
    squint_band()
    quant_staircase()
