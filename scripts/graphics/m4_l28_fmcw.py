#!/usr/bin/env python3
"""Generate the L28 (FMCW on the PHASER) lesson-page figures as inline SVG.

  - L28-chirp         : the transmitted chirp and its echo, frequency against
                        time, with the delay and the beat marked (not to scale)
  - L28-range-profile : one chirp's range FFT of a 2 m corner, at the
                        lesson's worked chirp: the 0 m leakage, the corner, the far wall
  - L28-windows       : a strong target and one 30 dB weaker, 2.5 m apart, rectangular
                        against Hann window
  - L28-waterfall     : range profiles of the recorded walker, stacked in time

The data figures run on the recorded-data fallback, scripts/radar/fmcw_sim.py,
except that the range profile and the windows run on the lesson's worked chirp,
400 MHz in 2 ms at 10.0 GHz, which no app preset uses. The
figures carry no equations (house rule).

    python3 scripts/graphics/m4_l28_fmcw.py
    -> book/extras/viz/img/L28-*.svg
"""

from __future__ import annotations
import io
import sys
from pathlib import Path

import numpy as np
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from svg_font_stack import apply_font_stack

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts/radar"))
import fmcw_sim as sim                      # noqa: E402

NAVY, BLUE, RED, GREEN, ORANGE, GRAY = "#004a85", "#0067b9", "#b01e24", "#1d7a4d", "#e67e22", "#5a5a5a"
INK, RULE = "#1a1a1a", "#c7d2e0"
OUT = ROOT / "book/extras/viz/img"
C = sim.C
# The lesson's worked chirp, not an app preset, so no figure prints a Part 1
# answer (COURSE_SPEC, "Lesson and lab, one shape").
EXAMPLE = dict(B=400e6, T_ramp=2e-3, fc=10.0e9)

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


def tidy(ax) -> None:
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.grid(True, color="#e6eef6", lw=0.8)
    ax.set_axisbelow(True)


def profile_db(x: np.ndarray, cap: dict, window: str | None = "hann", n_fft: int = 4096):
    """Range axis (m) and power (dBFS) of one chirp, as the cadet's code does it."""
    w = np.hanning(x.size) if window == "hann" else np.ones(x.size)
    X = np.fft.fftshift(np.fft.fft(x * w, n_fft))
    f = np.fft.fftshift(np.fft.fftfreq(n_fft, 1 / cap["fs"]))
    r = (f - cap["f0"]) * C * cap["T_ramp"] / (2 * cap["B"])
    return r, 20 * np.log10(np.abs(X) / w.sum() + 1e-12)


# -------------------------------------------------------------------- figures
def chirp() -> None:
    T, tau = 1.0, 0.16                         # chirp length and delay, not to scale
    f_lo, f_hi = 0.0, 1.0
    fig, ax = plt.subplots(figsize=(6.6, 3.0))
    for k in range(2):
        t0 = k * T
        # the first 10% of each ramp, which the app discards while the ramp settles
        ax.axvspan(t0, t0 + 0.1 * T, color="#e6eef6", lw=0, zorder=0)
        ax.plot([t0, t0 + T], [f_lo, f_hi], color=NAVY, lw=2.2,
                label="transmitted chirp" if k == 0 else None)
        ax.plot([t0 + tau, t0 + T + tau], [f_lo, f_hi], color=RED, lw=2.0, ls="--",
                label="echo" if k == 0 else None)
    ax.text(0.05, -0.06, "settling", color=GRAY, fontsize=10.5, ha="left", va="top")
    ax.annotate("", (1.1, -0.06), (2.0, -0.06), arrowprops=dict(arrowstyle="<->", color=GREEN, lw=1.0),
                annotation_clip=False)
    ax.text(1.55, -0.10, "kept: the last 90%", color=GREEN, fontsize=11, ha="center", va="top")
    # delay, horizontal, and beat, vertical, both on the first chirp
    ta, tb = 0.30, 0.30 + tau
    fa = ta / T
    ax.annotate("", (ta, fa), (tb, fa), arrowprops=dict(arrowstyle="<->", color=INK, lw=1.0))
    ax.text(ta - 0.04, fa, "delay", ha="right", va="center", fontsize=12)
    tv = 0.75
    ax.annotate("", (tv, tv / T), (tv, (tv - tau) / T),
                arrowprops=dict(arrowstyle="<->", color=GREEN, lw=1.4))
    ax.text(tv + 0.03, (tv - tau / 2) / T, "beat", color=GREEN, fontsize=12, va="center")
    ax.annotate("", (2.28, 0.0), (2.28, 1.0), arrowprops=dict(arrowstyle="<->", color=GRAY, lw=1.0))
    ax.text(2.31, 0.5, "bandwidth", color=GRAY, fontsize=12, va="center")
    ax.annotate("", (0.0, -0.27), (1.0, -0.27), arrowprops=dict(arrowstyle="<->", color=GRAY, lw=1.0),
                annotation_clip=False)
    ax.text(0.5, -0.31, "chirp length", color=GRAY, fontsize=12, ha="center", va="top")
    ax.set_xlim(-0.05, 2.75)
    ax.set_ylim(-0.48, 1.16)
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_xlabel("time")
    ax.set_ylabel("frequency")
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.legend(loc="lower left", bbox_to_anchor=(0.12, 1.0), ncol=2, fontsize=12, handlelength=2.2)
    finalize(fig, "L28-chirp")


def range_profile() -> None:
    cap = sim.l28_capture(**EXAMPLE)
    sim.room(cap)
    sim.add_point(cap, 2.0, rcs=0.47)
    r, p = profile_db(sim.iq(cap)[0], cap)
    keep = (r >= -0.3) & (r <= 8)
    fig, ax = plt.subplots(figsize=(6.6, 3.0))
    ax.plot(r[keep], p[keep], color=NAVY, lw=1.3)
    for rr, lab, dy in ((0.0, "leakage, 0 m", 4), (2.0, "corner, 2.0 m", 4), (5.5, "wall, 5.5 m", 4)):
        near = np.flatnonzero(np.abs(r - rr) < 0.4)
        j = near[np.argmax(p[near])]
        ax.annotate(lab, (r[j], p[j]), xytext=(r[j] + 0.25, p[j] + dy), fontsize=12, color=INK)
    ax.set_xlim(-0.3, 8)
    ax.set_ylim(-95, 0)
    ax.set_xlabel("range (m)")
    ax.set_ylabel("power (dBFS)")
    tidy(ax)
    kpm = 2 * cap["B"] / (C * cap["T_ramp"]) / 1e3            # kHz of beat per meter
    top = ax.secondary_xaxis("top", functions=(lambda x: x * kpm, lambda f: f / kpm))
    top.set_xlabel("beat above the 0 m frequency (kHz)", color=GRAY, fontsize=12)
    top.tick_params(colors=GRAY)
    finalize(fig, "L28-range-profile")


def windows() -> None:
    cap = sim.l28_capture(n_chirps=1, **EXAMPLE)
    sim.add_point(cap, 2.0, level_dbfs=-10.0)
    sim.add_point(cap, 4.5, level_dbfs=-40.0, phase0=1.0)
    sim.add_noise(cap, level_dbfs=-75.0, seed=3)
    fig, (ax, az) = plt.subplots(1, 2, figsize=(7.4, 3.0), gridspec_kw=dict(width_ratios=[1.75, 1]))
    for win, color, lab in ((None, ORANGE, "rectangular"), ("hann", NAVY, "Hann")):
        r, p = profile_db(sim.iq(cap)[0], cap, win, n_fft=16384)
        keep = (r >= 0.5) & (r <= 5.5)
        ax.plot(r[keep], p[keep], color=color, lw=1.4, label=lab)
        z = (r >= 1.3) & (r <= 2.7)
        az.plot(r[z], p[z], color=color, lw=1.6)
        # the width 3 dB down, bracketed on the zoom
        i = np.flatnonzero(z)[np.argmax(p[z])]
        lo = hi = i
        while p[lo - 1] > p[i] - 3: lo -= 1
        while p[hi + 1] > p[i] - 3: hi += 1
        y = p[i] - 3 - (1.2 if win else 3.2)
        az.annotate("", (r[lo], y), (r[hi], y), arrowprops=dict(arrowstyle="<->", color=color, lw=1.1))
    ax.annotate("weak target, 4.5 m", (4.5, -40), xytext=(4.0, -18), fontsize=12, color=INK,
                arrowprops=dict(arrowstyle="-", color=INK, lw=0.8))
    ax.set_xlim(0.5, 5.5)
    ax.set_ylim(-100, 0)
    ax.set_xlabel("range (m)")
    ax.set_ylabel("power (dBFS)")
    ax.legend(loc="upper left", fontsize=11.5)
    tidy(ax)
    az.set_xlim(1.3, 2.7)
    az.set_ylim(-20, -9)
    az.set_xlabel("range (m), zoomed")
    az.set_title("width 3 dB down", fontsize=11.5, color=GRAY)
    tidy(az)
    fig.tight_layout(w_pad=1.2)
    finalize(fig, "L28-windows")


def waterfall() -> None:
    """A simulated walk, 1.5 m out to 3.5 m and back at 0.5 m/s, on the worked chirp.

    Not the recorded walk: the recorded walk is a Table D column. Time runs
    down, newest row at the top, as on the app's Range Waterfall tab.
    """
    cap = sim.l28_capture(n_chirps=200, **EXAMPLE)
    sim.room(cap)
    sim.add_walker(cap, r_start=1.5, r_turn=3.5, speed=0.5)
    x = sim.iq(cap)
    rows = [profile_db(c, cap, n_fft=2048) for c in x]
    r = rows[0][0]
    keep = (r >= 0) & (r <= 6)
    W = np.array([p[keep] for _, p in rows])[::-1]          # newest first
    span = W.shape[0] * cap["PRI"]
    fig, ax = plt.subplots(figsize=(6.6, 3.0))
    ax.imshow(np.clip(W, -55, -22), origin="upper", aspect="auto", cmap="Blues",
              extent=(0, 6, span, 0), interpolation="nearest")
    for xx, lab in ((0.0, "leakage"), (5.5, "wall")):
        ax.text(xx, -0.2, lab, color=INK, fontsize=11.5, ha="center", va="bottom")
    ax.set_xlabel("range (m)")
    ax.set_ylabel("time ago (s)")
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    finalize(fig, "L28-waterfall")


def spectrum_abs() -> None:
    """The worked chirp's whole beat spectrum, 0 to 300 kHz, with f0 at 100 kHz."""
    cap = sim.l28_capture(n_chirps=32, f0=100e3, **EXAMPLE)
    sim.room(cap)
    sim.add_point(cap, 30.0, level_dbfs=-58.0, phase0=0.3)   # a strong reflector at 30 m
    x = sim.iq(cap)
    n = 8192
    w = np.hanning(x.shape[1])
    X = np.fft.fftshift(np.fft.fft(x * w, n, axis=1), axes=1)
    f = np.fft.fftshift(np.fft.fftfreq(n, 1 / cap["fs"])) / 1e3
    p = 10 * np.log10(np.mean(np.abs(X) ** 2, axis=0) / w.sum() ** 2 + 1e-30)
    keep = (f >= 0) & (f <= 300)
    fig, ax = plt.subplots(figsize=(6.6, 3.0))
    ax.axvspan(0, 100, color="#f1f3f5", lw=0, zorder=0)
    ax.plot(f[keep], p[keep], color=NAVY, lw=1.1)
    ax.axvline(100, color=GREEN, lw=1.0, ls="--")
    ax.text(50, -8, "below $f_0$:\nnegative range", color=GRAY, fontsize=10.5, ha="center", va="top")
    ax.text(103, -8, "$f_0$, 0 m:\nthe leakage", color=GREEN, fontsize=10.5, ha="left", va="top")
    ax.annotate("target at 30 m,\n$f_0 + 40$ kHz", (140, -62), xytext=(160, -30), fontsize=10.5, color=INK,
                arrowprops=dict(arrowstyle="-", color=INK, lw=0.8))
    ax.annotate("", (300, -95), (300, -5), arrowprops=dict(arrowstyle="-", color=RED, lw=1.2))
    ax.text(296, -8, "$f_s/2$: 150 m,\nthen aliasing", color=RED, fontsize=10.5, ha="right", va="top")
    ax.set_xlim(0, 310)
    ax.set_ylim(-100, 0)
    ax.set_xlabel("beat frequency (kHz)")
    ax.set_ylabel("power (dBFS)")
    tidy(ax)
    finalize(fig, "L28-spectrum")


def record_length() -> None:
    """One target, the worked chirp at 2 ms and at a quarter of that, same sample rate."""
    fig, ax = plt.subplots(figsize=(6.6, 3.0))
    floors = []
    for T, color, lab in ((2e-3, NAVY, "2 ms"), (0.5e-3, ORANGE, "0.5 ms")):
        cap = sim.l28_capture(n_chirps=32, B=400e6, T_ramp=T, fc=10.0e9)
        sim.add_noise(cap, seed=5)
        sim.add_point(cap, 4.0, level_dbfs=-30.0)
        x = sim.iq(cap)
        n = 16384
        w = np.hanning(x.shape[1])
        X = np.fft.fft(x * w, n, axis=1)
        f = np.fft.fftfreq(n, 1 / cap["fs"])
        r = (f - cap["f0"]) * C * T / (2 * cap["B"])
        p = 10 * np.log10(np.mean(np.abs(X) ** 2, axis=0) / w.sum() ** 2 + 1e-30)
        o = np.argsort(r); r, p = r[o], p[o]
        k = (r >= 0) & (r <= 8)
        ax.plot(r[k], p[k], color=color, lw=1.3, label=lab)
        floors.append(np.median(p[(r > 6) & (r < 8)]))
    for fl, color in zip(floors, (NAVY, ORANGE)):
        ax.axhline(fl, color=color, lw=0.9, ls="--")
    ax.annotate("", (0.5, floors[1]), (0.5, floors[0]), arrowprops=dict(arrowstyle="<->", color=INK, lw=1.0))
    ax.text(0.5, floors[1] + 2.5, "6 dB", color=INK, fontsize=11.5, ha="center", va="bottom")
    ax.set_xlim(0, 8)
    ax.set_ylim(-100, -20)
    ax.set_xlabel("range (m)")
    ax.set_ylabel("power (dBFS)")
    ax.legend(loc="upper right", fontsize=11.5, title="chirp", title_fontsize=11)
    tidy(ax)
    finalize(fig, "L28-record-length")


def setup() -> None:
    """Top view of the range measurement: the kit, the plate on the tape, and where to stand."""
    from matplotlib.patches import Rectangle, Polygon
    fig, ax = plt.subplots(figsize=(6.6, 2.6))
    ax.add_patch(Polygon([[0.25, 0.0], [4.2, 0.95], [4.2, -0.95]], closed=True, color="#eef4fa", lw=0))
    ax.add_patch(Rectangle((-0.35, -0.45), 0.35, 0.9, color=NAVY))
    ax.text(-0.18, -0.62, "kit", color=INK, fontsize=11.5, ha="center", va="top")
    ax.plot([0.0, 0.0], [-0.42, 0.42], color=GREEN, lw=3)
    ax.text(0.06, 0.55, "array face", color=GREEN, fontsize=10.5, ha="left")
    ax.plot([0, 3.6], [-0.05, -0.05], color=GRAY, lw=1.0)
    for m in (1, 2, 3):
        ax.plot([m, m], [-0.12, 0.02], color=GRAY, lw=1.0)
        ax.text(m, -0.2, f"{m} m", color=GRAY, fontsize=10.5, ha="center", va="top")
    ax.add_patch(Rectangle((1.97, -0.32), 0.06, 0.64, color=INK))
    ax.text(2.1, 0.42, "plate, square to the array", color=INK, fontsize=10.5, ha="left")
    ax.plot([1.6], [-1.35], marker="x", color=RED, ms=10, mew=2)
    ax.text(1.75, -1.35, "stand here, out of the beam", color=RED, fontsize=10.5, va="center")
    ax.set_xlim(-0.6, 4.4)
    ax.set_ylim(-1.6, 1.0)
    ax.set_aspect("equal")
    ax.axis("off")
    finalize(fig, "L28-setup")


def flow() -> None:
    """The lab's five blocks, the packet table each fills, and the captures the notebook reads."""
    from matplotlib.patches import FancyBboxPatch
    blocks = [("Steps 1–5", "0 m\nfrequency", "A"), ("Steps 6–8", "static\nranges", "B"),
              ("Steps 9–11", "change\nthe chirp", "C"), ("Steps 12–15", "a walk", "D"),
              ("Steps 16–22", "the\nnotebook", "B, C, E")]
    fig, ax = plt.subplots(figsize=(7.2, 2.3))
    W, H, gap = 1.3, 1.15, 0.2
    xs = [i * (W + gap) for i in range(len(blocks))]
    for x, (st, what, tab) in zip(xs, blocks):
        ax.add_patch(FancyBboxPatch((x, 0.6), W, H, boxstyle="round,pad=0.02,rounding_size=0.08",
                                    fc="#eef4fa", ec=BLUE, lw=1.2))
        ax.text(x + W / 2, 0.6 + H - 0.2, st, ha="center", va="center", fontsize=10.5, color=GRAY)
        ax.text(x + W / 2, 0.6 + H / 2 + 0.02, what, ha="center", va="center", fontsize=11, color=INK, linespacing=1.1)
        ax.text(x + W / 2, 0.6 + 0.17, f"Table {tab}", ha="center", va="center", fontsize=10.5, color=NAVY,
                fontweight="bold")
    for x in xs[:-1]:
        ax.annotate("", (x + W + gap, 0.6 + H / 2), (x + W, 0.6 + H / 2),
                    arrowprops=dict(arrowstyle="->", color=GRAY, lw=1.1))
    # the captures saved in the first three blocks feed the notebook
    y = 0.32
    ax.plot([xs[0] + W / 2, xs[4] + W / 2], [y, y], color=ORANGE, lw=1.1)
    for x in xs[:3]:
        ax.plot([x + W / 2, x + W / 2], [0.6, y], color=ORANGE, lw=1.1)
    ax.annotate("", (xs[4] + W / 2, 0.6), (xs[4] + W / 2, y), arrowprops=dict(arrowstyle="->", color=ORANGE, lw=1.1))
    ax.text((xs[0] + xs[2]) / 2 + W / 2, y - 0.1, "saved captures", color=ORANGE, fontsize=10.5, ha="center", va="top")
    ax.set_xlim(-0.05, xs[-1] + W + 0.05)
    ax.set_ylim(0.0, 1.82)
    ax.axis("off")
    finalize(fig, "L28-flow")


if __name__ == "__main__":
    chirp()
    range_profile()
    windows()
    waterfall()
    spectrum_abs()
    record_length()
    setup()
    flow()
