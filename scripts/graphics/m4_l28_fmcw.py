#!/usr/bin/env python3
"""Generate the L28 (FMCW on the PHASER) lesson-page figures as inline SVG.

  - L28-chirp         : the transmitted chirp and its echo, frequency against
                        time, with the delay and the beat marked (not to scale)
  - L28-range-profile : one chirp's range FFT from the recorded 2 m corner
                        capture: the 0 m leakage, the corner, the far wall
  - L28-windows       : a strong and a weak target 0.9 m apart, rectangular
                        against Hann window
  - L28-waterfall     : range profiles of the recorded walker, stacked in time

The data figures run on the recorded-data fallback, scripts/radar/fmcw_sim.py,
so the page shows what a cadet's own code will draw from those files. The
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
        ax.plot([t0, t0 + T], [f_lo, f_hi], color=NAVY, lw=2.2,
                label="transmitted chirp" if k == 0 else None)
        ax.plot([t0 + tau, t0 + T + tau], [f_lo, f_hi], color=RED, lw=2.0, ls="--",
                label="echo" if k == 0 else None)
    # delay, horizontal, and beat, vertical, both on the first chirp
    ta, tb = 0.30, 0.30 + tau
    fa = ta / T
    ax.annotate("", (ta, fa), (tb, fa), arrowprops=dict(arrowstyle="<->", color=INK, lw=1.0))
    ax.text(ta - 0.04, fa, "delay", ha="right", va="center", fontsize=12)
    tv = 0.75
    ax.annotate("", (tv, tv / T), (tv, (tv - tau) / T),
                arrowprops=dict(arrowstyle="<->", color=GREEN, lw=1.4))
    ax.text(tv + 0.03, (tv - tau / 2) / T, "beat", color=GREEN, fontsize=12, va="center")
    ax.annotate("", (1.25, 0.0), (1.25, 1.0), arrowprops=dict(arrowstyle="<->", color=GRAY, lw=1.0))
    ax.text(1.28, 0.5, "bandwidth", color=GRAY, fontsize=12, va="center")
    ax.annotate("", (1.0, -0.12), (2.0, -0.12), arrowprops=dict(arrowstyle="<->", color=GRAY, lw=1.0),
                annotation_clip=False)
    ax.text(1.5, -0.16, "chirp length", color=GRAY, fontsize=12, ha="center", va="top")
    ax.set_xlim(-0.05, 2.25)
    ax.set_ylim(-0.32, 1.12)
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_xlabel("time")
    ax.set_ylabel("frequency")
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.legend(loc="upper left", fontsize=12, handlelength=2.2)
    finalize(fig, "L28-chirp")


def range_profile() -> None:
    cap = dict(np.load(sim.OUT / "L28_corner_2m.npz"))
    for k in ("fs", "B", "T_ramp", "f0"):
        cap[k] = float(cap[k])
    r, p = profile_db(cap["iq"][0], cap)
    keep = (r >= -0.3) & (r <= 8)
    fig, ax = plt.subplots(figsize=(6.6, 3.0))
    ax.plot(r[keep], p[keep], color=NAVY, lw=1.3)
    for rr, lab, dy in ((0.0, "leakage, 0 m", 4), (2.0, "corner, 2.0 m", 4), (5.5, "wall, 5.5 m", 4)):
        i = np.argmin(np.abs(r - rr))
        j = i - 40 + np.argmax(p[i - 40:i + 40])
        ax.annotate(lab, (r[j], p[j]), xytext=(r[j] + 0.25, p[j] + dy), fontsize=12, color=INK)
    ax.set_xlim(-0.3, 8)
    ax.set_ylim(-95, 0)
    ax.set_xlabel("range (m)")
    ax.set_ylabel("power (dBFS)")
    tidy(ax)
    top = ax.secondary_xaxis("top", functions=(lambda x: x * 6.667, lambda f: f / 6.667))
    top.set_xlabel("beat above the 0 m frequency (kHz)", color=GRAY, fontsize=12)
    top.tick_params(colors=GRAY)
    finalize(fig, "L28-range-profile")


def windows() -> None:
    cap = sim.new_capture("l28_range", n_chirps=1)
    sim.add_point(cap, 2.0, level_dbfs=-10.0)
    sim.add_point(cap, 2.9, level_dbfs=-50.0, phase0=1.0)
    sim.add_noise(cap, level_dbfs=-75.0, seed=3)
    fig, ax = plt.subplots(figsize=(6.6, 3.0))
    for win, color, lab, ls in ((None, ORANGE, "rectangular", "-"), ("hann", NAVY, "Hann", "-")):
        r, p = profile_db(sim.iq(cap)[0], cap, win)
        keep = (r >= 0.5) & (r <= 4.0)
        ax.plot(r[keep], p[keep], color=color, lw=1.4, ls=ls, label=lab)
    ax.annotate("weak target, 2.9 m", (2.9, -51), xytext=(3.05, -32), fontsize=12, color=INK,
                arrowprops=dict(arrowstyle="-", color=INK, lw=0.8))
    ax.set_xlim(0.5, 4.0)
    ax.set_ylim(-100, 0)
    ax.set_xlabel("range (m)")
    ax.set_ylabel("power (dBFS)")
    ax.legend(loc="upper left", fontsize=12)
    tidy(ax)
    finalize(fig, "L28-windows")


def waterfall() -> None:
    cap = dict(np.load(sim.OUT / "L28_walker.npz"))
    for k in ("fs", "B", "T_ramp", "f0", "PRI"):
        cap[k] = float(cap[k])
    rows = [profile_db(x, cap, n_fft=1024) for x in cap["iq"]]
    r = rows[0][0]
    keep = (r >= 0) & (r <= 6)
    W = np.array([p[keep] for _, p in rows])
    t = np.arange(W.shape[0]) * cap["PRI"]
    fig, ax = plt.subplots(figsize=(6.6, 3.0))
    ax.imshow(np.clip(W, -65, -25), origin="lower", aspect="auto", cmap="Blues",
              extent=(0, 6, 0, t[-1] + cap["PRI"]), interpolation="nearest")
    top = t[-1] + cap["PRI"]
    for x, lab in ((0.0, "leakage"), (5.5, "wall")):
        ax.text(x, top + 0.2, lab, color=INK, fontsize=11.5, ha="center", va="bottom")
    ax.set_xlabel("range (m)")
    ax.set_ylabel("time (s)")
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    finalize(fig, "L28-waterfall")


if __name__ == "__main__":
    chirp()
    range_profile()
    windows()
    waterfall()
