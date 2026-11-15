#!/usr/bin/env python3
"""The L31 page's explanatory figures, added in the 2026-11-12 reshape review.

  lesson half (the example burst and example targets of
  m4_l31_classification_tracking.py; no packet answer is printed):
  - L31-floor          : the floor plan: array, E1/E8 sides, x/y, and the
                         example walk P -> Q with u, r and theta at P
  - L31-ab-trade       : the alpha-beta trade, noise ratio and settled lag
                         against alpha, the example alpha = 0.4 marked
  - L31-shape          : held Doppler spectra normalized to the edge: a
                         full blade, a rim, an outer third, and a tilted
                         full blade that lands on the full blade
  - L31-window         : resolution 1/T_w and limb smear against T_w,
                         crossing at the best window, powers of two marked
  - L31-slow-time      : the burst as chirps x range bins, one range bin's
                         column, and overlapping windows feeding columns
  - L31-sweep-vs-mono  : a crossing walker's bearing against time, sampled
                         by a beam sweep and by monopulse frames
  lab half:
  - L31-floor-lab      : the tape marks A and B and the walk, no values
  - L31-app-settings   : the Phaser app's controls the lab sets
  - L31-notebook-strip : what the three notebook tasks show, values blanked

    python3 scripts/graphics/m4_l31_figures.py
"""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import m4_l31_classification_tracking as g          # noqa: E402
from m4_l31_classification_tracking import plt, finalize, style, NAVY, BLUE, RED, GREEN, AMBER, GRAY, INK  # noqa: E402
from matplotlib.patches import FancyArrowPatch, Rectangle, Wedge, FancyBboxPatch  # noqa: E402

ROOT = HERE.parents[1]


def arrow(ax, p, q, color=INK, lw=1.4, ms=10):
    ax.add_patch(FancyArrowPatch(p, q, arrowstyle="-|>", mutation_scale=ms, color=color, lw=lw))


def array_icon(ax, label_sides=True):
    ax.add_patch(Rectangle((-0.30, -0.08), 0.60, 0.08, color=NAVY))
    if label_sides:
        ax.text(-0.36, -0.04, "E1", ha="right", va="center", color=NAVY, fontsize=12)
        ax.text(0.36, -0.04, "E8", ha="left", va="center", color=NAVY, fontsize=12)


def fig_floor() -> None:
    """The example walk P -> Q on the floor, seen from above."""
    P, Q = np.array(g.DIAG_P), np.array(g.DIAG_Q)
    fig, ax = plt.subplots(figsize=(4.0, 4.3))
    array_icon(ax)
    arrow(ax, (0, 0), (0, 3.9), GRAY, 1.0)
    arrow(ax, (0.75, 0.25), (1.4, 0.25), GRAY, 1.0)
    ax.text(0.06, 3.9, "y, boresight", color=GRAY, fontsize=12, va="top")
    ax.text(1.4, 0.32, "x", color=GRAY, fontsize=12.5, ha="right", va="bottom")
    ax.plot([P[0], Q[0]], [P[1], Q[1]], color=AMBER, lw=1.6, ls="--")
    ax.plot([0, P[0]], [0, P[1]], color=BLUE, lw=1.0)
    for pt, name, dx in ((P, "P", 0.10), (Q, "Q", -0.10)):
        ax.plot(*pt, "o", color=INK, ms=5)
        ax.text(pt[0] + dx, pt[1], name, ha="left" if dx > 0 else "right", va="center", fontsize=13, fontweight="bold")
    u = (Q - P) / np.hypot(*(Q - P))
    r = P / np.hypot(*P)
    arrow(ax, tuple(P), tuple(P + 0.7 * u), AMBER, 1.8)
    ax.text(*(P + 0.7 * u + np.array([-0.05, 0.05])), "û", color=AMBER, fontsize=14, ha="right", va="bottom")
    arrow(ax, tuple(P), tuple(P + 0.6 * r), BLUE, 1.8)
    ax.text(*(P + 0.6 * r + np.array([0.06, 0])), "r̂", color=BLUE, fontsize=14, ha="left", va="center")
    th = np.degrees(np.arctan2(P[0], P[1]))
    ax.add_patch(Wedge((0, 0), 0.9, 90 - th, 90, fill=False, color=RED, lw=1.2))
    ax.text(-0.02, 1.02, "θ", color=RED, fontsize=14, ha="center")
    ax.set_xlim(-1.5, 1.5)
    ax.set_ylim(-0.35, 4.0)
    ax.set_aspect("equal")
    ax.axis("off")
    finalize(fig, "L31-floor")


def fig_floor_lab() -> None:
    """The lab's tape marks: the measurements that place them, no ranges or angles."""
    A, B = np.array([-0.31, 1.47]), np.array([0.69, 3.94])
    fig, ax = plt.subplots(figsize=(4.0, 4.5))
    array_icon(ax)
    arrow(ax, (0, 0), (0, 4.5), GRAY, 1.0)
    ax.text(0, 4.55, "boresight", color=GRAY, fontsize=12, va="bottom", ha="center")
    ax.plot([A[0], B[0]], [A[1], B[1]], color=AMBER, lw=1.8)
    arrow(ax, tuple(A + 0.35 * (B - A)), tuple(A + 0.55 * (B - A)), AMBER, 1.8, 14)
    for pt, name in ((A, "A"), (B, "B")):
        ax.plot([0, pt[0]], [0, pt[1]], color=BLUE, lw=0.9, ls=":")
        ax.plot([0, pt[0]], [pt[1], pt[1]], color=GRAY, lw=0.8)
        ax.plot(*pt, "s", color=INK, ms=7)
    ax.text(A[0] - 0.12, A[1], "A", ha="right", va="center", fontsize=14, fontweight="bold")
    ax.text(B[0] + 0.12, B[1], "B", ha="left", va="center", fontsize=14, fontweight="bold")
    ax.text(A[0] - 0.05, A[1] - 0.14, "0.31 m", ha="right", va="top", fontsize=12.5, color=GRAY)
    ax.text(B[0] / 2 + 0.12, B[1] + 0.08, "0.69 m", ha="center", va="bottom", fontsize=12.5, color=GRAY)
    ax.text(0.06, A[1] / 2, "1.47 m", ha="left", va="center", fontsize=12.5, color=GRAY)
    ax.text(-0.06, B[1] - 0.8, "3.94 m", ha="right", va="center", fontsize=12.5, color=GRAY)
    ax.text(0.62, 2.35, "walk,\nturn at B,\nwalk back", color=AMBER, fontsize=12.5, ha="left", va="center")
    ax.text(0, -0.30, "facing the patches, E1 is on your right", ha="center", va="top", fontsize=12.5, color=GRAY)
    ax.set_xlim(-1.4, 1.6)
    ax.set_ylim(-0.6, 4.95)
    ax.set_aspect("equal")
    ax.axis("off")
    finalize(fig, "L31-floor-lab")


def ab_curves(alpha):
    beta = alpha ** 2 / (2 - alpha)
    ratio = np.sqrt((2 * alpha ** 2 + 2 * beta - 3 * alpha * beta) / (alpha * (4 - 2 * alpha - beta)))
    return beta, ratio


def fig_ab_trade() -> None:
    a = np.linspace(0.05, 1.0, 400)
    beta, ratio = ab_curves(a)
    lag = np.pi * 1.2 * g.CPI ** 2 / beta        # the example turn's peak acceleration
    fig, ax = plt.subplots(figsize=(4.4, 2.9))
    ax.plot(a, ratio, color=BLUE, lw=1.8, label="noise ratio")
    ax.set_xlabel("α")
    ax.set_ylabel("noise ratio", color=BLUE)
    ax.set_ylim(0, 1.05)
    ax.set_xlim(0, 1.0)
    ax2 = ax.twinx()
    ax2.plot(a, lag, color=RED, lw=1.8)
    ax2.set_yscale("log")
    ax2.set_ylim(0.03, 30)
    ax2.set_ylabel("settled lag (m)", color=RED)
    ax2.set_yticks([0.1, 1, 10])
    ax2.set_yticklabels(["0.1", "1", "10"])
    ax2.yaxis.set_minor_formatter(plt.NullFormatter())
    ax2.tick_params(colors=GRAY, labelsize=13)
    b4, r4 = ab_curves(0.4)
    l4 = np.pi * 1.2 * g.CPI ** 2 / b4
    ax.plot([0.4], [r4], "o", color=BLUE, ms=6)
    ax2.plot([0.4], [l4], "o", color=RED, ms=6)
    ax.axvline(0.4, color=GRAY, lw=0.8, ls=":")
    ax.text(0.42, 0.08, "α = 0.4", color=GRAY, fontsize=12)
    style(ax)
    for s in ("top",):
        ax2.spines[s].set_visible(False)
    finalize(fig, "L31-ab-trade")


def held_spectrum(rho_lo, rho_hi, tilt=0.0, n=4000):
    """Time- and point-averaged |v|/v_tip distribution of a rotor whose weight is
    spread evenly from rho_lo to rho_hi (fractions of R), in dB of its peak."""
    th = np.linspace(0, 2 * np.pi, n, endpoint=False)
    rho = np.linspace(rho_lo, rho_hi, 60) if rho_hi > rho_lo else np.array([rho_hi])
    v = (rho[:, None] * np.sin(th)[None, :] * np.cos(np.radians(tilt))).ravel()
    edges = np.linspace(-1.1, 1.1, 111)
    h, _ = np.histogram(v, edges)
    h = np.convolve(h, [0.25, 0.5, 1, 0.5, 0.25], "same")
    c = 0.5 * (edges[1:] + edges[:-1])
    edge = np.abs(v).max()
    return c / edge, 10 * np.log10(np.maximum(h / h.max(), 1e-4)), np.sqrt(np.mean(v ** 2)) / edge


def fig_shape() -> None:
    fig, ax = plt.subplots(figsize=(4.4, 3.5))
    cases = [((0.0, 1.0, 0), "full blade", RED, "-"), ((0.0, 1.0, 40), "full blade, 40° tilt", RED, ":"),
             ((1.0, 1.0, 0), "rim", AMBER, "-"), ((2 / 3, 1.0, 0), "outer third", BLUE, "-")]
    for (lo, hi, tilt), lab, col, ls in cases:
        x, d, _ = held_spectrum(lo, hi, tilt)
        ax.plot(x, d, color=col, lw=1.6 if ls == "-" else 2.4, ls=ls, label=lab)
    _, _, s3 = held_spectrum(2 / 3, 1.0)
    for sgn in (-1, 1):
        ax.axvline(sgn * s3, color=BLUE, lw=0.9, ls="--")
    ax.text(s3 + 0.03, -15, "rms", color=BLUE, fontsize=12.5)
    ax.set_xlim(-1.15, 1.15)
    ax.set_ylim(-30, 2)
    ax.set_xticks([-1, 0, 1])
    ax.set_xticklabels(["−edge", "0", "+edge"])
    ax.set_yticks([-30, -20, -10, 0])
    ax.set_xlabel("radial speed, over the band's edge")
    ax.set_ylabel("dB")
    fig.subplots_adjust(bottom=0.36)
    ax.legend(loc="upper center", bbox_to_anchor=(0.5, -0.32), fontsize=12.5, ncol=2, handlelength=1.4,
              columnspacing=0.8, borderaxespad=0.1)
    style(ax)
    finalize(fig, "L31-shape")


def fig_window() -> None:
    v = g.numbers()
    T = np.logspace(np.log10(3e-3), np.log10(0.3), 200)
    fig, ax = plt.subplots(figsize=(4.4, 2.9))
    ax.loglog(T * 1e3, 1 / T, color=BLUE, lw=1.8, label="resolution 1/T_w")
    ax.loglog(T * 1e3, v["fdot"] * T, color=RED, lw=1.8, label="limb smear")
    tb = 1 / np.sqrt(v["fdot"])
    ax.plot([tb * 1e3], [1 / tb], "o", color=INK, ms=5)
    ax.text(tb * 1e3 * 1.12, 1 / tb * 1.15, f"best, {tb * 1e3:.0f} ms", fontsize=12.5)
    for n in (16, 64, 256):
        ax.axvline(n * g.PRI * 1e3, color=GRAY, lw=0.8, ls=":")
        ax.text(n * g.PRI * 1e3 * 1.05, 2.2, f"{n}", fontsize=12.5, color=GRAY)
    for axis in (ax.xaxis, ax.yaxis):
        axis.set_minor_formatter(plt.NullFormatter())
    ax.set_xticks([3, 10, 30, 100, 300])
    ax.set_xticklabels(["3", "10", "30", "100", "300"])
    ax.set_yticks([3, 10, 30, 100, 300])
    ax.set_yticklabels(["3", "10", "30", "100", "300"])
    ax.set_xlabel("window T_w (ms)")
    ax.set_ylabel("Hz")
    ax.set_ylim(2, 400)
    ax.legend(loc="upper center", fontsize=12.5, borderaxespad=0.1)
    style(ax)
    finalize(fig, "L31-window")


def fig_slow_time() -> None:
    fig, ax = plt.subplots(figsize=(4.6, 2.7))
    nb, nc = 10, 14
    for i in range(nb):
        for j in range(nc):
            ax.add_patch(Rectangle((j, i), 0.92, 0.92, color="#dfe9f3" if i != 6 else "#9fc3e3"))
    ax.text(nc / 2, nb + 0.5, "chirps, one every PRI (slow time) →", ha="center", fontsize=12.5)
    ax.text(-0.6, nb / 2, "range bin", rotation=90, ha="right", va="center", fontsize=12.5)
    ax.text(nc + 0.3, 6.45, "the target's bin", va="center", fontsize=12.5, color=NAVY)
    for k, (j0, col) in enumerate(((0, RED), (3, AMBER), (6, GREEN))):
        ax.add_patch(Rectangle((j0 - 0.05, 5.9), 6.0, 1.1, fill=False, ec=col, lw=1.6))
        ax.annotate("", xy=(nc + 2.4 + 0.9 * k, 2.0), xytext=(j0 + 3, 5.85),
                    arrowprops=dict(arrowstyle="-|>", color=col, lw=1.0))
        ax.add_patch(Rectangle((nc + 2.0 + 0.9 * k, 0), 0.8, 2.0, color=col, alpha=0.55))
    ax.text(nc + 3.3, -0.5, "spectrogram\ncolumns", ha="center", va="top", fontsize=12.5)
    ax.text(3, -0.5, "each window: an FFT\nacross its chirps", ha="center", va="top", fontsize=12.5)
    ax.set_xlim(-1.2, nc + 5.2)
    ax.set_ylim(-2.2, nb + 1.2)
    ax.set_aspect("equal")
    ax.axis("off")
    finalize(fig, "L31-slow-time")


def fig_sweep_vs_mono() -> None:
    v_w, R, Ts = 1.0, 4.0, 1.1
    t = np.linspace(0, 4, 400)
    th = np.degrees(np.arctan2(v_w * (t - 2), R))
    fig, ax = plt.subplots(figsize=(4.4, 2.9))
    ax.plot(t, th, color=GRAY, lw=1.0, ls="--", label="walker")
    ts = np.arange(0.2, 4, Ts)
    for x in ts:
        y = np.degrees(np.arctan2(v_w * (x - 2), R))
        ax.add_patch(Rectangle((x - 0.04, y - 13.6 / 2), 0.08, 13.6, color=AMBER, alpha=0.35))
    ax.plot(ts, np.degrees(np.arctan2(v_w * (ts - 2), R)), "s", color=AMBER, ms=6, label="beam sweep")
    tm = np.arange(0.05, 4, g.CPI)
    ax.plot(tm, np.degrees(np.arctan2(v_w * (tm - 2), R)), "o", color=BLUE, ms=2.8, label="monopulse frames")
    ax.set_xlabel("time (s)")
    ax.set_ylabel("bearing (°)")
    ax.set_xlim(0, 4)
    ax.set_ylim(-32, 32)
    ax.set_yticks([-20, 0, 20])
    ax.legend(loc="upper left", fontsize=12.5, borderaxespad=0.1)
    style(ax)
    finalize(fig, "L31-sweep-vs-mono")


def fig_app_settings() -> None:
    rows = [("Mode", "FMCW"), ("Preset", "Range + Velocity"), ("0 m Beat (kHz)", "set by Calibrate…"),
            ("MTI", "on"), ("MTI Mode", "2-pulse"), ("View", "Range-Doppler"), ("Subarray Channels", "on, for Step 11"),
            ("Save Capture", "Step 11")]
    fig, ax = plt.subplots(figsize=(4.6, 3.0))
    ax.add_patch(FancyBboxPatch((0, 0), 12, len(rows) + 0.6, boxstyle="round,pad=0.1,rounding_size=0.3",
                                fc="#f5f9fc", ec="#cddce9", lw=1.2))
    for i, (k, val) in enumerate(rows[::-1]):
        y = 0.55 + i
        ax.text(0.4, y, k, va="center", fontsize=12, color=GRAY, fontweight="bold")
        ax.add_patch(FancyBboxPatch((6.1, y - 0.36), 5.6, 0.72, boxstyle="round,pad=0.02,rounding_size=0.15",
                                    fc="white", ec="#b9d2e5", lw=1.0))
        ax.text(6.3, y, val, va="center", fontsize=12, color=NAVY)
    ax.set_xlim(-0.2, 12.2)
    ax.set_ylim(-0.2, len(rows) + 0.9)
    ax.axis("off")
    finalize(fig, "L31-app-settings")


def fig_notebook_strip() -> None:
    """Thumbnails of what tasks (a) to (c) show, from the recorded data, with no
    tick labels or values, so the strip shows the shape of each result only."""
    sys.path.insert(0, str(ROOT / "scripts/radar"))
    sys.path.insert(0, str(ROOT / "book/extras/notebooks"))
    import make_l31_data as m
    rl, h = m.notebook_helpers()
    cap = rl.load_capture(m.OUT / "L31_walker_1.npz")
    r, vv, *_ = h["detect"](cap)
    t, f, S = rl.spectrogram(cap, h["target_bins"](cap, r, vv), n_win=64)
    walk = rl.load_capture(m.OUT / "L31_dismount.npz")
    zr, _ = h["track_meas"](walk)
    tk = walk["truth_t"]
    trk = rl.alpha_beta(zr, 0.5, 0.5 ** 2 / 1.5, 0.128)[:, 0]
    fig, axs = plt.subplots(1, 3, figsize=(6.6, 2.2))
    axs[0].imshow(np.clip(S, -40, 0), origin="lower", aspect="auto", cmap="Blues",
                  extent=(t[0], t[-1], f[0], f[-1]), interpolation="bilinear")
    axs[0].set_ylim(-400, 400)
    axs[0].set_title("(a) spectrogram", fontsize=12)
    axs[1].set_title("(b) confusion matrix", fontsize=12)
    for i in range(5):
        axs[1].axhline(i, color=GRAY, lw=0.8)
        axs[1].axvline(i, color=GRAY, lw=0.8)
    for i in range(4):
        axs[1].add_patch(Rectangle((i, 3 - i), 1, 1, color="#dfe9f3"))
    for i, k in enumerate(["W", "F", "S", "H"]):
        axs[1].text(i + 0.5, 4.25, k, ha="center", fontsize=12.5, color=GRAY)
        axs[1].text(-0.25, 3.5 - i, k, ha="right", va="center", fontsize=12.5, color=GRAY)
    axs[1].set_xlim(-0.6, 4.1)
    axs[1].set_ylim(-0.1, 4.7)
    axs[1].set_aspect("equal")
    axs[2].plot(tk, walk["truth_r"], color=GRAY, ls="--", lw=1.0)
    axs[2].plot(tk, zr, "o", mfc="none", mec=INK, ms=2.5, mew=0.6)
    axs[2].plot(tk, trk, color=BLUE, lw=1.5)
    axs[2].set_title("(c) track", fontsize=12)
    for ax in axs:
        ax.set_xticks([])
        ax.set_yticks([])
        for s in ax.spines.values():
            s.set_visible(ax is not axs[1])
            s.set_color("#8a929c")
    fig.subplots_adjust(wspace=0.12)
    finalize(fig, "L31-notebook-strip")


def main() -> None:
    fig_floor()
    fig_floor_lab()
    fig_ab_trade()
    fig_shape()
    fig_window()
    fig_slow_time()
    fig_sweep_vs_mono()
    fig_app_settings()
    fig_notebook_strip()


if __name__ == "__main__":
    main()
