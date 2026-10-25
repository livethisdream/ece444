#!/usr/bin/env python3
"""L23 lesson-page figures: why each departure happens, and when it matters.

The pattern sweeps are what the PHASER kit already draws, so these figures show
the mechanism behind them instead (Neil, 2026-10-24: "illustrate why and when
things happen", not what the kit shows).

  - L23-grating-whole-turn : why a grating lobe is full height. A plane wave
                             from 43.9 deg reaches the fed elements of the
                             42 mm row exactly one wavelength apart, so every
                             element's phase dial reads the same; the full
                             14 mm row at the same angle sees a third of a
                             wavelength per element, and its dials spread out.
  - L23-visible-window     : when a grating lobe appears. The same periodic
                             array factor against psi, with the window real
                             angles reach shaded: 14 mm (8 elements) stops
                             short of the repeats, 42 mm (3 elements) takes in
                             two of them.
  - L23-squint-ramp        : why squint moves the beam instead of breaking it.
                             The ramp the phase shifters apply (set for 45 deg
                             at 10.525 GHz) against the ramp a 10.025 GHz
                             signal needs at 45 deg; their difference is a
                             straight ramp, which is just a steer.
  - L23-quant-staircase    : why rounding makes a lobe. The exact ramp for 28
                             deg, its 3-bit staircase, and the error left over:
                             bounded by half an LSB and close to repeating.
  - L23-qsll-vs-bits       : when quantization matters. The -6B rule, the
                             simulated worst lobe on the course array over
                             steer angles 0 to 50 deg, the uniform array's own
                             -13 dB sidelobes, and the phaser-00 test run.

Every plotted number is computed here and matches the lesson text.

    python3 scripts/graphics/l23_figures.py
    -> book/extras/viz/img/L23-*.svg
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

NAVY, BLUE, AMBER, RED, GRAY = "#004a85", "#0067b9", "#8a5a00", "#b01e24", "#5b6573"
INK, RULE, SHADE = "#15202b", "#c7d2e0", "#e3edf6"
ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "book/extras/viz/img"

plt.rcParams.update({"svg.fonttype": "none", "font.size": 11, "text.color": INK,
                     "axes.edgecolor": GRAY, "axes.labelcolor": INK,
                     "xtick.color": GRAY, "ytick.color": GRAY})

C = 2.99792458e8
PITCH = 14e-3
N = 8
LAM_103 = C / 10.3e9 * 1e3          # mm, the array design center
LAM_0 = C / 10.525e9 * 1e3          # mm, the HB100


def save(fig, name):
    buf = io.StringIO()
    fig.savefig(buf, format="svg", transparent=True, bbox_inches="tight", pad_inches=0.06)
    plt.close(fig)
    s = re.sub(r"<metadata>.*?</metadata>", "", buf.getvalue(), flags=re.S)
    s = apply_font_stack(s)
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / f"{name}.svg").write_text(s, encoding="utf-8")
    print(f"wrote {OUT / (name + '.svg')}")


def af_db(xs_mm, alpha, th_deg, lam_mm):
    """|AF| in dB (normalized to the element count) for elements at xs_mm with phases alpha."""
    k = 2 * np.pi / lam_mm
    s = np.sin(np.radians(th_deg))
    v = np.abs(np.exp(1j * (np.outer(s, k * np.asarray(xs_mm)) + alpha)).sum(1)) / len(xs_mm)
    return 20 * np.log10(np.maximum(v, 1e-9))


# --------------------------------------------------------------- grating ---
def grating_whole_turn():
    thg = np.degrees(np.arcsin(LAM_103 / 42.0))            # 43.9 deg
    assert abs(thg - 43.9) < 0.05
    rows = [("every third element, 42 mm", 42.0, 3, AMBER),
            ("all eight, 14 mm", 14.0, 8, BLUE)]
    fig, axes = plt.subplots(2, 1, figsize=(5.6, 4.2))
    for ax, (label, d, n, col) in zip(axes, rows):
        path = d * np.sin(np.radians(thg))                  # mm per element
        frac = path / LAM_103                               # wavelengths per element
        xs = np.arange(n) * d
        ax.set_xlim(-14, 112)
        ax.set_ylim(-1.15, 1.35)
        ax.set_aspect("equal")
        ax.axis("off")
        r = 5.2 if n == 3 else 4.6
        for i, x in enumerate(xs):
            ph = 2 * np.pi * frac * i                       # the phase each element sees
            ax.add_patch(plt.Circle((x, 0), r, fill=False, ec=RULE, lw=1.2))
            ax.annotate("", (x + r * np.sin(ph), r * np.cos(ph)), (x, 0),
                        arrowprops=dict(arrowstyle="-|>", color=col, lw=1.8, mutation_scale=9,
                                        shrinkA=0, shrinkB=0))
            ax.text(x, -r - 3.2, f"{360 * frac * i:.0f}°", ha="center", va="top",
                    fontsize=9.5, color=GRAY)
        ax.text(-14, r + 6.5, f"{label}: {frac:.2f} λ of extra path per element",
                ha="left", va="bottom", fontsize=10.5, color=col, fontweight="bold")
        ax.set_ylim(-r - 9, r + 12)
    axes[0].text(112, -14.2, f"wave arriving from {thg:.1f}°", ha="right", va="top",
                 fontsize=9.5, color=GRAY)
    fig.subplots_adjust(hspace=0.05)
    save(fig, "L23-grating-whole-turn")


def visible_window():
    psi = np.linspace(-720, 720, 6001)                      # degrees
    def af(n):
        p = np.radians(psi) / 2
        with np.errstate(invalid="ignore", divide="ignore"):
            v = np.abs(np.sin(n * p) / (n * np.sin(p)))
        v[~np.isfinite(v)] = 1.0
        return 20 * np.log10(np.maximum(v, 1e-6))
    cases = [(14.0, 8, BLUE, "14 mm, 8 elements"), (42.0, 3, AMBER, "42 mm, 3 elements")]
    fig, axes = plt.subplots(2, 1, figsize=(6.0, 3.1), sharex=True)
    for ax, (d, n, col, label) in zip(axes, cases):
        half = 360 * d / LAM_103                            # kd in degrees: the window edge
        ax.axvspan(-half, half, color=SHADE, zorder=0)
        ax.plot(psi, af(n), color=col, lw=1.8, zorder=2)
        for rep in (-360, 360):
            inside = abs(rep) <= half
            ax.plot([rep], [0], "o", ms=6, zorder=3,
                    color=col if inside else "white", mec=col, mew=1.5)
        ax.set_ylim(-30, 4)
        ax.set_yticks([0, -15, -30])
        ax.grid(axis="y", color=RULE, lw=0.8)
        for sp in ("top", "right"):
            ax.spines[sp].set_visible(False)
        ax.set_ylabel("dB")
        txt = f"{label}: window ±{half:.0f}°"
        ax.text(-712, 2.2, txt, ha="left", va="bottom", fontsize=10.5, color=col, fontweight="bold")
    axes[1].set_xticks([-720, -360, 0, 360, 720])
    axes[1].set_xlabel("array-factor argument ψ (degrees)")
    fig.subplots_adjust(hspace=0.35)
    save(fig, "L23-visible-window")


# ---------------------------------------------------------------- squint ---
def squint_ramp():
    f0, f = 10.525e9, 10.025e9
    lam0, lam = C / f0 * 1e3, C / f * 1e3
    n = np.arange(N)
    s45 = np.sin(np.radians(45))
    applied = 360 * (PITCH * 1e3 / lam0) * s45 * n          # set at f0
    needed = 360 * (PITCH * 1e3 / lam) * s45 * n            # what f needs at 45 deg
    err = applied - needed
    th = np.degrees(np.arcsin(f0 / f * s45))
    assert abs(th - 47.9) < 0.05
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(6.4, 3.0), gridspec_kw={"width_ratios": [1.25, 1]})
    a1.plot(n + 1, applied, "o-", color=NAVY, lw=1.8, ms=4.5)
    a1.plot(n + 1, needed, "o--", color=GRAY, lw=1.4, ms=4)
    a1.text(4.6, applied[4] + 70, "applied", color=NAVY, fontsize=10, ha="right", va="bottom",
            fontweight="bold")
    a1.text(5.4, needed[4] - 70, "needed", color=GRAY, fontsize=10, ha="left", va="top",
            fontweight="bold")
    a1.set_xlim(0.6, 8.4)
    a1.set_ylabel("phase lag (degrees)")
    a1.set_xlabel("element")
    a1.set_xticks(range(1, 9))
    a2.bar(n + 1, err, color=RED, width=0.55)
    a2.set_xlabel("element")
    a2.set_ylabel("difference (degrees)")
    a2.set_xticks(range(1, 9))
    a2.text(0.6, err[-1] * 1.02, f"{err[1]:.1f}° per element", color=RED, fontsize=10,
            va="bottom", fontweight="bold")
    a2.set_ylim(0, err[-1] * 1.22)
    for ax in (a1, a2):
        ax.grid(axis="y", color=RULE, lw=0.8)
        for sp in ("top", "right"):
            ax.spines[sp].set_visible(False)
    fig.tight_layout(w_pad=1.6)
    save(fig, "L23-squint-ramp")
    return err[1]


# ---------------------------------------------------------- quantization ---
def quant_staircase(th0=28, bits=3):
    n = np.arange(N)
    exact = 360 * (PITCH * 1e3 / LAM_0) * np.sin(np.radians(th0)) * n
    lsb = 360 / 2 ** bits
    q = np.round(exact / lsb) * lsb
    err = q - exact
    assert np.all(np.abs(err) <= lsb / 2 + 1e-9)
    fig, (a1, a2) = plt.subplots(2, 1, figsize=(6.0, 3.3), sharex=True,
                                 gridspec_kw={"height_ratios": [1.6, 1]})
    for v in np.arange(0, q.max() + lsb, lsb):
        a1.axhline(v, color=RULE, lw=0.8, zorder=0)
    a1.step(n + 1, q, where="mid", color=NAVY, lw=2.0)
    a1.plot(n + 1, exact, "o--", color=GRAY, lw=1.3, ms=4)
    a1.text(1.2, q.max() * 0.92, f"{bits}-bit staircase, steps of {lsb:.0f}°", color=NAVY,
            fontsize=10, fontweight="bold", va="top")
    a1.text(1.2, q.max() * 0.80, f"exact ramp for {th0}°", color=GRAY, fontsize=10, va="top")
    a1.set_ylabel("phase lag (degrees)")
    a2.axhspan(-lsb / 2, lsb / 2, color=SHADE, zorder=0)
    a2.bar(n + 1, err, color=AMBER, width=0.55, zorder=2)
    a2.axhline(0, color=GRAY, lw=0.8)
    a2.set_ylim(-lsb / 2 * 1.35, lsb / 2 * 1.35)
    a2.set_yticks([-lsb / 2, 0, lsb / 2])
    a2.set_yticklabels([f"−{lsb/2:.1f}°", "0", f"+{lsb/2:.1f}°"])
    a2.set_ylabel("error")
    a2.set_xlabel("element")
    a2.set_xticks(range(1, 9))
    for ax in (a1, a2):
        for sp in ("top", "right"):
            ax.spines[sp].set_visible(False)
    fig.subplots_adjust(hspace=0.12)
    save(fig, "L23-quant-staircase")


def qsll_vs_bits():
    th = np.linspace(-90, 90, 7201)
    xs = np.arange(N) * PITCH * 1e3
    k = 2 * np.pi / LAM_0
    B = np.arange(2, 8)
    # The quantization lobe on its own: the field the rounding error radiates,
    # (quantized pattern) - (exact pattern), relative to the beam, at the worst
    # steer angle from 0 to 50 deg.  Taking the whole quantized pattern instead
    # would also count the ordinary sidelobes and the scan effects at wide angle.
    s = np.sin(np.radians(th))
    sim = []
    for b in B:
        lsb = 2 * np.pi / 2 ** b
        worst = -99
        for t0 in range(0, 51):
            a = -k * xs * np.sin(np.radians(t0))
            q = np.round(a / lsb) * lsb
            ph = np.outer(s, k * xs)
            diff = np.abs((np.exp(1j * (ph + q)) - np.exp(1j * (ph + a))).sum(1)) / N
            worst = max(worst, 20 * np.log10(diff.max()))
        sim.append(worst)
    sim = np.array(sim)
    meas_b, meas_v = [2, 3, 4], [-8.5, -12.0, -15.5]
    fig, ax = plt.subplots(figsize=(5.4, 3.4))
    ax.axhline(-13.3, color=GRAY, lw=1.2, ls=(0, (5, 4)))
    ax.text(7.05, -13.3 + 0.6, "uniform array's own sidelobes", ha="right", va="bottom",
            fontsize=9.5, color=GRAY)
    ax.plot(B, -6 * B, "-", color=AMBER, lw=1.8)
    ax.text(5.1, -6 * 5.1 - 1.4, "rule: −6B", color=AMBER, fontsize=10, fontweight="bold",
            ha="left", va="top")
    ax.plot(B, sim, "o-", color=BLUE, lw=1.8, ms=5)
    ax.text(B[-1] + 0.1, sim[-1] - 1.2, "simulated,\nworst steer", color=BLUE, fontsize=9.5,
            ha="right", va="top", fontweight="bold")
    ax.plot(meas_b, meas_v, "s", color=RED, ms=7)
    ax.plot([7], [-17.4], "s", ms=7, mfc="white", mec=RED, mew=1.5)
    ax.text(4.12, -15.5, "phaser-00", color=RED, fontsize=10, fontweight="bold",
            ha="left", va="center")
    ax.text(6.92, -17.4, "floor", color=RED, fontsize=9.5, ha="right", va="center")
    ax.set_xlabel("phase-shifter bits B")
    ax.set_ylabel("worst lobe (dB below the beam)")
    ax.set_xticks(B)
    ax.set_ylim(-44, -4)
    ax.grid(axis="y", color=RULE, lw=0.8)
    for sp in ("top", "right"):
        ax.spines[sp].set_visible(False)
    save(fig, "L23-qsll-vs-bits")
    return dict(zip(B.tolist(), np.round(sim, 1).tolist()))


# --------------------------------------------------- true time delay ------
def ttd_vs_phase():
    """Phase lag at element 2 for a 45 deg steer: a delay against a phase shift."""
    tau = PITCH * np.sin(np.radians(45)) / C               # s, one element's delay
    f = np.linspace(0, 12e9, 400)
    ttd = 360 * f * tau
    ps = np.full_like(f, 360 * 10.525e9 * tau)
    gap = 360 * 10.525e9 * tau - 360 * 10.025e9 * tau
    assert abs(360 * 10.525e9 * tau - 125.1) < 0.1 and abs(gap - 5.9) < 0.05
    fig, ax = plt.subplots(figsize=(5.6, 3.2))
    ax.axvspan(10.0, 11.0, color=SHADE, zorder=0)
    ax.plot(f / 1e9, ttd, color=NAVY, lw=2.0)
    ax.plot(f / 1e9, ps, color=AMBER, lw=2.0)
    ax.plot([10.525], [360 * 10.525e9 * tau], "o", color=INK, ms=5, zorder=4)
    ax.plot([10.025, 10.025], [360 * 10.025e9 * tau, ps[0]], color=RED, lw=2.2)
    ax.text(5.6, 360 * 5.6e9 * tau + 9, "true time delay", color=NAVY, fontsize=10,
            fontweight="bold", ha="right", va="bottom", rotation=0)
    ax.text(0.4, ps[0] + 5, "phase shifter, set at 10.525 GHz", color=AMBER, fontsize=10,
            fontweight="bold", ha="left", va="bottom")
    ax.text(10.15, 360 * 10.025e9 * tau - 7, f"{gap:.1f}°", color=RED, fontsize=10,
            fontweight="bold", ha="left", va="top")
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 150)
    ax.set_xlabel("frequency (GHz)")
    ax.set_ylabel("phase lag, element 2 (degrees)")
    ax.grid(axis="y", color=RULE, lw=0.8)
    for sp in ("top", "right"):
        ax.spines[sp].set_visible(False)
    save(fig, "L23-ttd-vs-phase")


# ------------------------------------------------------- squint vs scan ---
def squint_vs_scan():
    f0 = 10.525
    th0 = np.linspace(0, 70, 701)
    fig, ax = plt.subplots(figsize=(5.4, 3.2))
    for off, col in ((-0.5, BLUE), (-1.0, NAVY)):
        f = f0 + off
        v = f0 / f * np.sin(np.radians(th0))
        ok = v <= 1
        exact = np.degrees(np.arcsin(v[ok])) - th0[ok]
        approx = np.degrees(-(off / f0) * np.tan(np.radians(th0)))
        ax.plot(th0[ok], exact, color=col, lw=2.0)
        ax.plot(th0, approx, color=col, lw=1.2, ls=(0, (4, 3)))
        i = np.searchsorted(th0, 45)
        ax.plot([45], [exact[i]], "o", color=col, ms=5)
        lx, ly, ha = ((46, 10.2, "right") if off < -0.75 else (69, 2.4, "right"))
        ax.text(lx, ly, f"{abs(off)*1000:.0f} MHz low", color=col, fontsize=10,
                fontweight="bold", ha=ha, va="bottom")
    ax.text(3, 13.2, "solid: exact     dashed: −δ tan θ₀", color=GRAY, fontsize=9.5,
            ha="left", va="top")
    ax.set_xlim(0, 70)
    ax.set_ylim(0, 15)
    ax.set_xlabel("commanded angle (degrees)")
    ax.set_ylabel("squint (degrees)")
    ax.grid(axis="y", color=RULE, lw=0.8)
    for sp in ("top", "right"):
        ax.spines[sp].set_visible(False)
    save(fig, "L23-squint-vs-scan")


# --------------------------------------------------- pointing grid --------
def pointing_grid():
    dl = PITCH * 1e3 / LAM_0
    fig, ax = plt.subplots(figsize=(5.8, 2.4))
    rows = [(2, AMBER), (3, BLUE), (4, NAVY), (7, GRAY)]
    for r, (b, col) in enumerate(rows):
        step = (360 / 2 ** b) / (360 * dl)
        m = np.arange(0, int(1 / step) + 1)
        ang = np.degrees(np.arcsin(m * step))
        y = len(rows) - 1 - r
        ax.vlines(ang, y - 0.28, y + 0.28, color=col, lw=1.6 if b < 7 else 0.8)
        ax.text(-3, y, f"{b} bits", ha="right", va="center", color=col, fontsize=10,
                fontweight="bold")
    ax.set_xlim(0, 90)
    ax.set_ylim(-0.6, len(rows) - 0.4)
    ax.set_yticks([])
    ax.set_xticks([0, 15, 30, 45, 60, 75, 90])
    ax.set_xlabel("beam angles the shifter can command (degrees)")
    for sp in ("top", "right", "left"):
        ax.spines[sp].set_visible(False)
    save(fig, "L23-pointing-grid")


# ------------------------------------------------------- dither -----------
def dither_error(n_el=32, bits=3, th0=15.8, dl=0.5):
    """Rounding error across a longer array, plain and with a fixed per-element offset."""
    L = 360 / 2 ** bits
    n = np.arange(n_el)
    a = 360 * dl * np.sin(np.radians(th0)) * n
    th = np.radians(np.linspace(-90, 90, 7201))
    ph = np.outer(np.sin(th), 2 * np.pi * dl * n)
    def err_pattern(err):
        v = np.abs(np.exp(1j * (ph - np.radians(a))) @ (np.exp(1j * np.radians(err)) - 1)) / n_el
        return 20 * np.log10(np.maximum(v, 1e-6))
    plain = np.round(a / L) * L - a
    draws = []
    for seed in range(30):
        u = np.random.default_rng(seed).uniform(-L / 2, L / 2, n_el)
        e = np.round((a - u) / L) * L - (a - u)
        draws.append((err_pattern(e).max(), seed, e))
    draws.sort(key=lambda z: z[0])
    lvl_d, seed, dith = draws[len(draws) // 2]                # a typical draw, not the best
    lvl_p = err_pattern(plain).max()
    fig, (a1, a2) = plt.subplots(2, 1, figsize=(6.0, 3.6), sharex=True)
    for ax, err, col, lab in ((a1, plain, AMBER, f"plain rounding: error lobe {lvl_p:.1f} dB"),
                              (a2, dith, BLUE, f"with a fixed offset per element: {lvl_d:.1f} dB")):
        ax.axhspan(-L / 2, L / 2, color=SHADE, zorder=0)
        ax.bar(n + 1, err, color=col, width=0.7, zorder=2)
        ax.axhline(0, color=GRAY, lw=0.8)
        ax.set_ylim(-L / 2 * 1.5, L / 2 * 1.9)
        ax.set_yticks([-L / 2, 0, L / 2])
        ax.set_yticklabels([f"−{L/2:.1f}°", "0", f"+{L/2:.1f}°"])
        ax.text(0.5, L / 2 * 1.85, lab, color=col, fontsize=10, fontweight="bold", va="top")
        for sp in ("top", "right"):
            ax.spines[sp].set_visible(False)
    a2.set_xlabel(f"element ({n_el}-element array, {bits} bits, steered to {th0}°)")
    fig.subplots_adjust(hspace=0.15)
    save(fig, "L23-dither-error")
    return round(lvl_p, 1), round(lvl_d, 1)


# ------------------------------------------------------- null depth -------
def null_depth_levels():
    fig, ax = plt.subplots(figsize=(5.4, 3.6))
    pred = [(-48, "one-step channel\nerrors: −48 dB", NAVY),
            (-21, "first estimate from\nthe sweep floor: −21 dB", GRAY)]
    for y, lab, col in pred:
        ax.plot([0.15, 0.85], [y, y], color=col, lw=3)
        ax.text(0.5, y + 1.2, lab, ha="center", va="bottom", color=col, fontsize=9.5,
                fontweight="bold")
    meas = [((-50, -46), "L24 notch"), ((-41.5, -41.5), "L24 difference null"),
            ((-39.7, -39.7), "L24 delta null"), ((-31, -17), "L22–L23 sweep floors")]
    xs = [1.25, 1.55, 1.85, 2.15]
    for x, ((lo, hi), lab) in zip(xs, meas):
        if lo == hi:
            ax.plot([x], [lo], "s", color=RED, ms=7)
        else:
            ax.plot([x, x], [lo, hi], color=RED, lw=6, solid_capstyle="butt")
        ax.text(x + 0.07, (lo + hi) / 2, lab, rotation=90, ha="left", va="center",
                color=RED, fontsize=9.5)
    ax.set_xlim(0, 2.45)
    ax.set_ylim(-55, 0)
    ax.set_xticks([0.5, 1.7])
    ax.set_xticklabels(["predicted", "measured, phaser-00"])
    ax.tick_params(axis="x", length=0)
    ax.set_ylabel("dB below the uniform peak")
    ax.grid(axis="y", color=RULE, lw=0.8)
    for sp in ("top", "right"):
        ax.spines[sp].set_visible(False)
    save(fig, "L23-null-depth-levels")


if __name__ == "__main__":
    grating_whole_turn()
    visible_window()
    print("squint error per element:", round(squint_ramp(), 2), "deg")
    quant_staircase()
    print("simulated worst lobe by bits:", qsll_vs_bits())
    ttd_vs_phase()
    squint_vs_scan()
    pointing_grid()
    print("dither, plain and typical draw:", dither_error())
    null_depth_levels()
