#!/usr/bin/env python3
"""Generate the L29 (Range-Doppler and MTI) lesson-page figures as inline SVG.

  - L29-chirp-sync    : the Doppler spectrum of one range cell, chirps
                        synchronized and chirps started at random times
  - L29-data-matrix   : the real part of the burst, chirps down, samples across
  - L29-rd-map        : a range-Doppler map of leakage, a wall, a hand, and a
                        fidget spinner
  - L29-canceller     : the 2- and 3-pulse canceller power response against
                        velocity, with the unambiguous window and blind speeds
  - L29-mti-maps      : the same map with no MTI, 2-pulse, and 3-pulse

Every map is computed the way the L29 Lab computes one, on the lesson's
teaching burst, which the Phaser app does not send (Neil, 2026-11-12: the
lesson works each method on a chirp the app does not use, so no figure prints
a Part 1 answer): 10.0 GHz, 400 MHz in 200 us, 128 chirps at a 0.4 ms PRI,
4 MSPS, a 100 kHz 0 m frequency; a Hann-windowed range FFT along each chirp,
a Hann-windowed Doppler FFT across the chirps. Every number the page prints is computed and
asserted here so the two cannot drift apart. None of the figures carries an
equation: symbols, numbers, and short words only.

    python3 scripts/graphics/m4_l29_range_doppler_mti.py
"""

from __future__ import annotations

import io
import re
from pathlib import Path

import numpy as np
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
from svg_font_stack import apply_font_stack  # noqa: E402

NAVY, BLUE, RED, GREEN, AMBER, GRAY = "#004a85", "#0067b9", "#b01e24", "#1d7a4d", "#8a5a00", "#5a5a5a"
INK, LIGHT = "#1a1a1a", "#9fb1c2"

IMG = Path(__file__).resolve().parents[2] / "book/extras/viz/img"
PHONE_COL, PX_MIN = 343.0, 10.5

# ------------------------------------------------ the lesson's teaching burst
C = 3.00e8
FC = 10.0e9
LAM = C / FC                 # 3.0 cm
B = 400e6
T_RAMP = 200e-6
PRI = 0.4e-3
M = 128
FS = 4e6
N = int(round(FS * T_RAMP))  # 800 samples on each ramp
V_HAND = 0.6                 # the lesson's hand, closing, m/s
F0 = 103e3                   # the teaching kit's 0 m frequency, set by the L28 calibration
SLOPE = B / T_RAMP

plt.rcParams.update(
    {
        "svg.fonttype": "none",
        "svg.hashsalt": "ece444-L29",
        "font.size": 13,
        "axes.edgecolor": "#8a929c",
        "axes.labelcolor": INK,
        "axes.labelsize": 13,
        "xtick.labelsize": 13,
        "ytick.labelsize": 13,
        "xtick.color": GRAY,
        "ytick.color": GRAY,
        "text.color": INK,
        "axes.linewidth": 1.0,
        "legend.frameon": False,
    }
)


# ---------------------------------------------------------------- the numbers
def numbers() -> dict:
    v = {}
    v["kHz_per_m"] = 2 * SLOPE / C / 1e3
    v["dR"] = C / (2 * B)
    v["bin_kHz"] = FS / N / 1e3
    v["cpi_ms"] = M * PRI * 1e3
    v["dv"] = LAM / (2 * M * PRI)
    v["vmax"] = LAM / (4 * PRI)
    v["vblind"] = LAM / (2 * PRI)
    v["fd_per_mps"] = 2 / LAM
    v["fd_hand"] = 2 * V_HAND / LAM
    v["deg_per_chirp_hand"] = np.degrees(4 * np.pi * V_HAND * PRI / LAM)
    v["fb_hand"] = F0 + 2 * SLOPE * 1.5 / C            # hand at 1.5 m
    v["deg_per_us_hand"] = 360 * v["fb_hand"] * 1e-6
    v["fd_vmax"] = 2 * v["vmax"] / LAM
    v["range_err_vmax"] = v["fd_vmax"] * C / (2 * SLOPE)
    v["migrate_hand"] = V_HAND * M * PRI
    v["dv_32"] = LAM / (2 * 32 * PRI)
    v["dv_256"] = LAM / (2 * 256 * PRI)
    v["dR_160"] = C / (2 * 160e6)
    v["floor_48"] = 10 * np.log10(M / 48)
    # canceller power gains, for the hand
    x = np.pi * v["fd_hand"] * PRI
    v["h2_1"] = 10 * np.log10(4 * np.sin(x) ** 2)
    v["h3_1"] = 10 * np.log10(16 * np.sin(x) ** 4)
    v["h2_max"] = 10 * np.log10(4)
    v["h3_max"] = 10 * np.log10(16)
    v["n2"] = 10 * np.log10(2)
    v["n3"] = 10 * np.log10(6)
    v["snr2_1"] = v["h2_1"] - v["n2"]
    v["snr3_1"] = v["h3_1"] - v["n3"]
    # where the cells sit for the teaching kit's 0 m frequency, and the wall's cell
    first = np.ceil(F0 * T_RAMP) / T_RAMP
    v["cell0"] = (first - F0) * C / (2 * SLOPE)
    v["wall_cell"] = v["cell0"] + v["dR"] * round((2.9 - v["cell0"]) / v["dR"])
    # a target at 16 m/s through each canceller
    x16 = np.pi * (2 * 16 / LAM) * PRI
    v["h2_16"] = 10 * np.log10(4 * np.sin(x16) ** 2)
    v["h2_16_lin"] = 4 * np.sin(x16) ** 2
    # a still hand's tremor, 1 mm at 1 Hz, and a hand across the beam, 0.15 m at 1 Hz at 1.5 m
    v["trem_v"] = 2 * np.pi * 1.0 * 1e-3
    v["trem_h2"] = 10 * np.log10(4 * np.sin(np.pi * (2 * v["trem_v"] / LAM) * PRI) ** 2)
    v["trem_phase"] = np.degrees(4 * np.pi * 1e-3 / LAM)
    v["across_v"] = np.pi * 0.15 ** 2 * 1.0 / 1.5
    v["across_fd"] = 2 * v["across_v"] / LAM
    v["across_h2"] = 10 * np.log10(4 * np.sin(np.pi * v["across_fd"] * PRI) ** 2)
    # the spinner of the figures: three arms 2.5 cm out at 20 rev/s
    v["tip"] = 2 * np.pi * 0.025 * 20
    v["fd_tip"] = 2 * v["tip"] / LAM
    v["line_mps"] = 3 * 20 * LAM / 2
    v["line_cells"] = v["line_mps"] / v["dv"]
    v["face_swing"] = v["tip"] * np.sin(np.radians(10))
    v["sync_loss"] = 10 * np.log10(M)
    return v


V = numbers()
for key, want, tol in (
    ("kHz_per_m", 13.3, 0.05), ("dR", 0.375, 1e-9), ("bin_kHz", 5.0, 0.01),
    ("cpi_ms", 51.2, 1e-9), ("dv", 0.293, 0.0005), ("vmax", 18.75, 1e-9),
    ("vblind", 37.5, 1e-9), ("fd_per_mps", 66.7, 0.05), ("fd_hand", 40.0, 1e-9),
    ("deg_per_chirp_hand", 5.76, 0.005), ("fb_hand", 123e3, 1e-6), ("deg_per_us_hand", 44.3, 0.05),
    ("fd_vmax", 1250, 1e-6), ("range_err_vmax", 0.094, 0.0005), ("migrate_hand", 0.0307, 0.0005),
    ("dv_32", 1.17, 0.005), ("dv_256", 0.146, 0.0005), ("dR_160", 0.94, 0.005), ("floor_48", 4.3, 0.05),
    ("h2_1", -20.0, 0.05), ("h3_1", -39.9, 0.05), ("h2_max", 6.0, 0.05), ("h3_max", 12.0, 0.05),
    ("n2", 3.0, 0.05), ("n3", 7.8, 0.05), ("snr2_1", -23.0, 0.05), ("snr3_1", -47.7, 0.05),
    ("tip", 3.14, 0.005), ("fd_tip", 209, 0.5), ("line_mps", 0.90, 1e-9), ("line_cells", 3.07, 0.005),
    ("cell0", 0.15, 1e-6), ("wall_cell", 2.775, 1e-6), ("h2_16", 5.8, 0.05), ("h2_16_lin", 3.79, 0.005),
    ("trem_v", 0.00628, 0.00001), ("trem_h2", -59.6, 0.05), ("trem_phase", 24.0, 0.05),
    ("across_v", 0.0471, 0.0001), ("across_fd", 3.14, 0.005), ("across_h2", -42.1, 0.05),
    ("face_swing", 0.55, 0.005), ("sync_loss", 21.1, 0.05),
):
    assert abs(V[key] - want) <= tol, f"{key} = {V[key]} (page says {want})"


# ------------------------------------------------------------------ the burst
def burst(targets, rng, sync=True, jitter_rad=0.002, noise=0.12) -> np.ndarray:
    """Beat samples, chirps down (M) and samples across (N).

    Each target is (amplitude, range m, closing speed m/s, micro) where micro
    is None or (arm radius m, rev/s, arms) for a spinner. Closing speed makes
    the range shrink from chirp to chirp, so the echo's phase, -4 pi R / lam,
    advances: a closing target lands at positive Doppler, as in L26.
    """
    m = np.arange(M)[:, None]
    n = np.arange(N)[None, :]
    t_slow = m * PRI
    x = np.zeros((M, N), complex)
    common = rng.normal(0, jitter_rad, (M, 1))           # chirp-to-chirp phase noise
    for amp, R0, vel, micro in targets:
        parts = [(amp, 0.0, 0.0)]
        if micro is not None:
            r, rps, arms = micro
            parts = [(amp / arms, r, 2 * np.pi * k / arms) for k in range(arms)]
        for a, r, th in parts:
            R = R0 - vel * t_slow
            if micro is not None:
                R = R + r * np.sin(2 * np.pi * micro[1] * t_slow + th)
            fb = F0 + 2 * SLOPE * R / C
            phase = -4 * np.pi * R / LAM
            if not sync:                                  # each chirp starts anywhere in a PRI
                tau = rng.uniform(0, PRI, (M, 1))
                phase = phase + 2 * np.pi * fb * tau
            x += a * np.exp(1j * (2 * np.pi * fb * n / FS + phase + common))
    x += noise * (rng.standard_normal((M, N)) + 1j * rng.standard_normal((M, N))) / np.sqrt(2)
    return x


def range_doppler(x: np.ndarray):
    """Hann in both dimensions, range FFT across, Doppler FFT down."""
    mm, nn = x.shape
    rp = np.fft.fft(x * np.hanning(nn)[None, :], axis=1)
    rd = np.fft.fftshift(np.fft.fft(rp * np.hanning(mm)[:, None], axis=0), axes=0)
    f = np.fft.fftfreq(nn, 1 / FS)
    rng_axis = (f - F0) * C / (2 * SLOPE)
    vel = np.fft.fftshift(np.fft.fftfreq(mm, PRI)) * LAM / 2
    return rd, rng_axis, vel


def mti(x: np.ndarray, kind: str) -> np.ndarray:
    if kind == "2pulse":
        return x[1:] - x[:-1]
    if kind == "3pulse":
        return x[2:] - 2 * x[1:-1] + x[:-2]
    return x


SCENE = [
    (1.0, 0.0, 0.0, None),               # transmit leakage, at the 0 m frequency
    (0.25, 2.9, 0.0, None),              # a wall
    (0.03, 1.5, V_HAND, None),           # a hand, closing at 0.6 m/s
    (0.03, 2.1, 0.0, (0.025, 20.0, 3)),  # a fidget spinner, tips at 3.14 m/s
]


# Wider figures shrink more to fit a phone's column, so their text is larger.
FSW = 14.5
WIDE = {"font.size": FSW, "axes.labelsize": FSW, "xtick.labelsize": FSW, "ytick.labelsize": FSW}


# ------------------------------------------------------------------ plumbing
def check_text(name: str, svg: str) -> None:
    """Every label is 10.5 px or more at a 343 px column."""
    vb = re.search(r'viewBox="0 0 ([\d.]+) ([\d.]+)"', svg)
    w = float(vb.group(1))
    sizes = [float(s) for s in re.findall(r"font-size:\s*([\d.]+)px", svg)]
    smallest = min(sizes) * PHONE_COL / w
    print(f"   {name}: viewBox {w:.0f} x {float(vb.group(2)):.0f}, smallest text "
          f"{min(sizes):.1f} units = {smallest:.1f} px at a {PHONE_COL:.0f} px column")
    assert smallest >= PX_MIN - 0.05, f"{name}: {smallest:.2f} px text on a phone"


def finalize(fig, name: str) -> None:
    buf = io.StringIO()
    fig.savefig(buf, format="svg", transparent=True, bbox_inches="tight", pad_inches=0.06,
                metadata={"Date": None})
    plt.close(fig)
    s = buf.getvalue()
    s = s[s.index("<svg"):]
    s = apply_font_stack(s)
    (IMG / f"{name}.svg").write_text(s, encoding="utf-8")
    print(f"wrote {IMG / (name + '.svg')}")
    check_text(name, s)


def tidy(ax) -> None:
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.grid(True, color="#e6eef6", lw=0.8)
    ax.set_axisbelow(True)


def db(x):
    return 20 * np.log10(np.abs(x) + 1e-30)


# -------------------------------------------------------------------- figures
def chirp_sync() -> None:
    hand = [(0.012, 1.5, V_HAND, None)]
    out = {}
    for sync in (True, False):
        rd, r, vel = range_doppler(burst(hand, np.random.default_rng(3), sync=sync, noise=0.01))
        k = np.argmin(np.abs(r - 1.5))
        out[sync] = db(rd[:, k])
    ref = out[True].max()
    fig, ax = plt.subplots(figsize=(4.4, 2.6))
    ax.plot(vel, out[False] - ref, color=RED, lw=1.0)
    ax.plot(vel, out[True] - ref, color=NAVY, lw=1.6)
    ax.text(1.2, -2, "synchronized", color=NAVY, ha="left", va="center")
    ax.text(-18, -15, "random start", color=RED, ha="left", va="bottom")
    ax.set_xlim(-V["vmax"], V["vmax"])
    ax.set_ylim(-60, 4)
    ax.set_xticks([-15, -10, -5, 0, 5, 10, 15])
    ax.set_yticks([-60, -40, -20, 0])
    ax.set_xlabel("velocity (m/s)")
    ax.set_ylabel("power (dB)")
    tidy(ax)
    finalize(fig, "L29-chirp-sync")


def data_matrix() -> None:
    hand = [(1.0, 1.5, V_HAND, None)]
    x = burst(hand, np.random.default_rng(1), jitter_rad=0, noise=0.05)
    mm, nn = 128, 160
    fig, ax = plt.subplots(figsize=(4.4, 3.0))
    ax.imshow(x[:mm, :nn].real, origin="upper", aspect="auto", cmap="RdBu_r",
              vmin=-1.3, vmax=1.3, extent=(-0.5, nn - 0.5, mm - 0.5, -0.5), interpolation="nearest")
    ax.set_xlabel("sample n, 0.25 µs apart (fast time)")
    ax.set_ylabel("chirp m, 0.4 ms apart\n(slow time)")
    ax.set_xticks([0, 40, 80, 120, 160])
    ax.set_yticks([0, 32, 64, 96, 128])
    for s in ax.spines.values():
        s.set_visible(False)
    finalize(fig, "L29-data-matrix")


MAP = matplotlib.colors.LinearSegmentedColormap.from_list(
    "l29", [(0.0, "#ffffff"), (0.2, "#dbe7f2"), (0.4, "#7fb0dc"), (0.6, "#0067b9"), (0.8, "#004a85"), (1.0, "#00213d")])


def rd_panel(ax, P, r, vel, lo=-75, rmax=4.0, vlim=6.0):
    keep = (r >= -0.15) & (r <= rmax)
    rr = r[keep]
    order = np.argsort(rr)
    img = P[:, keep][:, order]
    im = ax.imshow(np.clip(img.T, lo, 0), origin="lower", aspect="auto", cmap=MAP,
                   extent=(vel[0], vel[-1], rr[order][0], rr[order][-1]), interpolation="nearest",
                   vmin=lo, vmax=0)
    ax.set_xlim(-vlim, vlim)
    ax.set_ylim(-0.15, rmax)
    ax.set_xticks([-5, 0, 5])
    return im


def colorbar(fig, im, ax, ticks=(-75, -50, -25, 0)) -> None:
    cb = fig.colorbar(im, ax=ax, fraction=0.06, pad=0.03, ticks=list(ticks))
    fs = plt.rcParams["font.size"]
    cb.set_label("dB re leakage", fontsize=fs)
    cb.ax.tick_params(labelsize=fs, colors=GRAY)
    cb.outline.set_edgecolor("#8a929c")


def rd_map() -> None:
    rd, r, vel = range_doppler(burst(SCENE, np.random.default_rng(5)))
    P = db(rd)
    P -= P.max()
    fig, ax = plt.subplots(figsize=(4.8, 3.2))
    im = rd_panel(ax, P, r, vel)
    ax.set_xlabel("velocity (m/s)")
    ax.set_ylabel("range (m)")
    lab = dict(fontsize=13, va="center")
    ax.text(0.5, 0.15, "leakage", color=RED, ha="left", **lab)
    ax.text(0.5, 2.9, "wall", color=RED, ha="left", **lab)
    ax.text(1.2, 1.5, "hand", color=NAVY, ha="left", **lab)
    ax.text(3.6, 2.1, "spinner", color=NAVY, ha="left", **lab)
    colorbar(fig, im, ax)
    finalize(fig, "L29-rd-map")


def canceller() -> None:
    v = np.linspace(-45, 45, 3601)
    x = np.pi * (2 * v / LAM) * PRI
    h2 = 10 * np.log10(4 * np.sin(x) ** 2 + 1e-12)
    h3 = 10 * np.log10(16 * np.sin(x) ** 4 + 1e-12)
    fig, ax = plt.subplots(figsize=(4.6, 2.7))
    ax.axvspan(-V["vmax"], V["vmax"], color="#eef4fa", lw=0)
    ax.plot(v, h2, color=NAVY, lw=1.8)
    ax.plot(v, h3, color=AMBER, lw=1.8)
    for vb in (-V["vblind"], 0, V["vblind"]):
        ax.axvline(vb, color=RED, lw=1.0, ls="--")
    for vb in (-V["vblind"], V["vblind"]):
        ax.text(vb, 19, "blind", color=RED, ha="center", va="bottom", fontsize=13)
    ax.text(0, 19, "±18.75 m/s", color=GRAY, ha="center", va="bottom", fontsize=13)
    ax.text(-V["vmax"], 13, "3-pulse", color=AMBER, ha="center", va="bottom")
    ax.text(V["vmax"], 4, "2-pulse", color=NAVY, ha="center", va="top")
    ax.set_xlim(-45, 45)
    ax.set_ylim(-40, 19)
    ax.set_xticks([-37.5, -18.75, 0, 18.75, 37.5])
    ax.set_xticklabels(["−37.5", "−18.75", "0", "18.75", "37.5"])
    ax.set_yticks([-40, -20, 0])
    ax.set_xlabel("velocity (m/s)")
    ax.set_ylabel("gain (dB)")
    tidy(ax)
    finalize(fig, "L29-canceller")


def mti_maps() -> None:
    with plt.rc_context(WIDE):
        _mti_maps()


def _mti_maps() -> None:
    x = burst(SCENE, np.random.default_rng(5))
    maps = []
    for kind in ("none", "2pulse", "3pulse"):
        rd, r, vel = range_doppler(mti(x, kind))
        maps.append((kind, db(rd), r, vel))
    ref = maps[0][1].max()
    fig, axs = plt.subplots(1, 3, figsize=(6.6, 3.0), sharey=True)
    for ax, (kind, P, r, vel), title in zip(axs, maps, ("no MTI", "2-pulse", "3-pulse")):
        im = rd_panel(ax, P - ref, r, vel)
        ax.set_title(title, fontsize=FSW, color=INK)
        ax.set_xticks([-5, 0, 5])
    axs[0].set_ylabel("range (m)")
    axs[1].set_xlabel("velocity (m/s)")
    fig.subplots_adjust(wspace=0.08)
    colorbar(fig, im, list(axs))
    finalize(fig, "L29-mti-maps")
    # the hand's peak, against no MTI, as the page quotes it
    k = np.argmin(np.abs(maps[0][2] - 1.5))
    peaks = [P[:, k].max() for _, P, _, _ in maps]
    print(f"   hand peak: 2-pulse {peaks[1] - peaks[0]:+.1f} dB, 3-pulse {peaks[2] - peaks[0]:+.1f} dB")


# ----------------------------------------------- figures added in the reshape
def slow_time(n, rng, parts, noise=0.003):
    """One range cell's slow-time signal: parts are (amp, R(t) function)."""
    t = np.arange(n) * PRI
    x = np.zeros(n, complex)
    for a, R in parts:
        x += a * np.exp(-1j * 4 * np.pi * R(t) / LAM)
    return x + noise * (rng.standard_normal(n) + 1j * rng.standard_normal(n)) / np.sqrt(2)


def spinner_parts(swing_scale=1.0, hub=0.02):
    parts = [(hub, lambda t: 2.1 + 0 * t)]
    for k in range(3):
        parts.append((0.012, lambda t, k=k: 2.1 + 0.025 * swing_scale * np.sin(2 * np.pi * 20 * t + 2 * np.pi * k / 3)))
    return parts


def doppler_cut(x):
    w = np.hanning(len(x))
    X = np.fft.fftshift(np.fft.fft(x * w)) / w.sum()
    v = np.fft.fftshift(np.fft.fftfreq(len(x), PRI)) * LAM / 2
    return v, db(X)


def spinner_cut() -> None:
    with plt.rc_context(WIDE):
        _spinner_cut()


def _spinner_cut() -> None:
    rng = np.random.default_rng(7)
    fig, axs = plt.subplots(2, 1, figsize=(4.6, 3.6), sharex=True)
    for ax, scale, title in ((axs[0], 1.0, "edge-on"), (axs[1], np.sin(np.radians(10)), "face-on, 10° off")):
        v, P = doppler_cut(slow_time(4 * M, rng, spinner_parts(scale)))
        ax.plot(v, P - P.max(), color=NAVY, lw=1.4)
        for s_ in (-1, 1):
            ax.axvline(s_ * V["tip"], color=RED, lw=1.0, ls="--")
        ax.set_ylim(-45, 3)
        ax.set_yticks([-40, -20, 0])
        ax.set_xlim(-5, 5)
        ax.text(-4.8, -6, title, color=INK, ha="left", va="center")
        tidy(ax)
    axs[0].text(-V["tip"] - 0.12, -36, "tip speed", color=RED, ha="right", va="center")
    y = 1.5
    axs[0].annotate("", xy=(1.8, y), xytext=(0.9, y), arrowprops=dict(arrowstyle="<->", color=AMBER, lw=1.3))
    axs[0].text(1.35, y + 1.0, "line spacing", color=AMBER, ha="center", va="bottom")
    axs[1].set_xlabel("velocity (m/s)")
    fig.text(-0.04, 0.55, "power (dB)", rotation=90, va="center", ha="left", fontsize=FSW)
    fig.subplots_adjust(hspace=0.15)
    finalize(fig, "L29-spinner-cut")


def spectrogram_fig() -> None:
    with plt.rc_context(WIDE):
        _spectrogram_fig()


def _spectrogram_fig() -> None:
    rng = np.random.default_rng(11)
    # A hand waved along the line of sight, 0.3 m either way at 1.5 Hz (2.8 m/s at
    # most), for 2048 chirps: slow enough for a short window to follow it.
    n = 2048
    x = slow_time(n, rng, [(0.03, lambda t: 1.5 + 0.3 * np.sin(2 * np.pi * 1.5 * t))])
    fig, axs = plt.subplots(1, 2, figsize=(5.6, 2.9), sharey=True)
    for ax, (nw, hop) in zip(axs, ((64, 16), (16, 4))):
        w = np.hanning(nw)
        cols = [np.fft.fftshift(np.fft.fft(x[i:i + nw] * w)) for i in range(0, n - nw + 1, hop)]
        S = db(np.array(cols).T)
        S -= S.max()
        vel = np.fft.fftshift(np.fft.fftfreq(nw, PRI)) * LAM / 2
        t = (np.arange(S.shape[1]) * hop + nw / 2) * PRI * 1e3
        ax.pcolormesh(t, vel, np.clip(S, -25, 0), cmap=MAP, shading="nearest", vmin=-25, vmax=0)
        ax.set_ylim(-4.5, 4.5)
        ax.set_title(f"N_win = {nw}, hop {hop}", fontsize=FSW, color=INK)
        ax.set_xlabel("time (ms)")
    axs[0].set_ylabel("velocity (m/s)")
    fig.subplots_adjust(wspace=0.08)
    finalize(fig, "L29-spectrogram")


def burst_choices() -> None:
    with plt.rc_context(WIDE):
        _burst_choices()


def _burst_choices() -> None:
    def hand_map(mc, bw):
        slope = bw / T_RAMP
        m = np.arange(mc)[:, None]
        nn = np.arange(N)[None, :]
        R = 1.5 - V_HAND * m * PRI
        fb = F0 + 2 * slope * R / C
        x = np.exp(1j * (2 * np.pi * fb * nn / FS - 4 * np.pi * R / LAM))
        x = x + 0.01 * (np.random.default_rng(3).standard_normal(x.shape))
        rp = np.fft.fft(x * np.hanning(N)[None, :], axis=1)
        rd = np.fft.fftshift(np.fft.fft(rp * np.hanning(mc)[:, None], axis=0), axes=0)
        f = np.fft.fftfreq(N, 1 / FS)
        r = (f - F0) * C / (2 * slope)
        vel = np.fft.fftshift(np.fft.fftfreq(mc, PRI)) * LAM / 2
        P = db(rd)
        return P - P.max(), r, vel
    fig, axs = plt.subplots(1, 3, figsize=(6.0, 2.8), sharey=True)
    for ax, (mc, bw, title) in zip(axs, ((M, B, "128 chirps, 400 MHz"), (32, B, "32 chirps"), (M, 160e6, "160 MHz"))):
        P, r, vel = hand_map(mc, bw)
        keep = (r > 0.3) & (r < 2.8)
        order = np.argsort(r[keep])
        ax.imshow(np.clip(P[:, keep][:, order].T, -30, 0), origin="lower", aspect="auto", cmap=MAP,
                  extent=(vel[0], vel[-1], r[keep][order][0], r[keep][order][-1]), interpolation="nearest",
                  vmin=-30, vmax=0)
        ax.set_xlim(-3, 3)
        ax.set_ylim(0.5, 2.5)
        ax.set_xticks([-2, 0, 2])
        ax.set_title(title, fontsize=FSW, color=INK)
    axs[0].set_ylabel("range (m)")
    axs[1].set_xlabel("velocity (m/s)")
    fig.subplots_adjust(wspace=0.08)
    finalize(fig, "L29-burst-choices")


def phasor_fig() -> None:
    with plt.rc_context(WIDE):
        _phasor_fig()


def _phasor_fig() -> None:
    fig, axs = plt.subplots(1, 2, figsize=(5.6, 2.9))
    th = np.linspace(0, 2 * np.pi, 400)
    for ax in axs:
        ax.plot(np.cos(th), np.sin(th), color=LIGHT, lw=1.0)
        ax.set_aspect("equal")
        ax.set_xlim(-1.35, 1.35)
        ax.set_ylim(-1.35, 1.35)
        ax.axis("off")
    step = np.radians(V["deg_per_chirp_hand"])
    for m in range(12):
        a = m * step
        axs[0].annotate("", xy=(np.cos(a), np.sin(a)), xytext=(0, 0),
                        arrowprops=dict(arrowstyle="-|>", color=NAVY, lw=1.1, alpha=0.35 + 0.05 * m))
    axs[0].text(0, -1.25, "chirps 0 to 11: 5.8° a chirp", ha="center", va="center", fontsize=FSW, color=INK)
    true = np.radians(240)
    for m in range(4):
        a = m * true
        axs[1].plot(np.cos(a), np.sin(a), "o", color=NAVY, ms=6)
        axs[1].text(1.17 * np.cos(a), 1.17 * np.sin(a), str(m), ha="center", va="center", fontsize=FSW, color=NAVY)
    arc = np.linspace(0, true, 100)
    axs[1].plot(0.55 * np.cos(arc), 0.55 * np.sin(arc), color=RED, lw=1.3, ls="--")
    arc2 = np.linspace(0, -np.radians(120), 60)
    axs[1].plot(0.8 * np.cos(arc2), 0.8 * np.sin(arc2), color=AMBER, lw=1.6)
    axs[1].text(0, -1.25, "+240° reads as −120°", ha="center", va="center", fontsize=FSW, color=INK)
    axs[1].text(-0.55, 0.62, "+240°", color=RED, ha="center", fontsize=FSW)
    axs[1].text(0.55, -0.42, "−120°", color=AMBER, ha="center", fontsize=FSW)
    finalize(fig, "L29-phasor")


def box(ax, x, y, w, h, text, color=NAVY):
    from matplotlib.patches import FancyBboxPatch
    ax.add_patch(FancyBboxPatch((x - w / 2, y - h / 2), w, h, boxstyle="round,pad=0.02",
                                fc="#eef4fa", ec=color, lw=1.2))
    ax.text(x, y, text, ha="center", va="center", fontsize=FSW, color=INK)


def arrow(ax, x0, y0, x1, y1, color=GRAY):
    ax.annotate("", xy=(x1, y1), xytext=(x0, y0), arrowprops=dict(arrowstyle="-|>", color=color, lw=1.2))


def canceller_blocks() -> None:
    with plt.rc_context(WIDE):
        _canceller_blocks()


def _canceller_blocks() -> None:
    fig, ax = plt.subplots(figsize=(5.4, 2.4))
    ax.set_xlim(0, 10.6)
    ax.set_ylim(0, 4.2)
    ax.axis("off")
    for y0, label in ((3.0, "2-pulse"), (1.0, "3-pulse")):
        ax.text(0.05, y0 + 0.75, label, fontsize=FSW, color=NAVY, ha="left", va="center")
        stages = 1 if label == "2-pulse" else 2
        x = 0.4
        ax.text(x, y0, "x_m", fontsize=FSW, ha="left", va="center", color=INK)
        x += 0.8
        for sidx in range(stages):
            arrow(ax, x, y0, x + 0.9, y0)
            ax.plot([x + 0.4, x + 0.4], [y0, y0 - 0.55], color=GRAY, lw=1.2)
            box(ax, x + 1.5, y0 - 0.55, 1.3, 0.55, "delay")
            arrow(ax, x + 0.4, y0 - 0.55, x + 0.85, y0 - 0.55)
            ax.plot([x + 2.15, x + 2.55], [y0 - 0.55, y0 - 0.55], color=GRAY, lw=1.2)
            arrow(ax, x + 2.55, y0 - 0.55, x + 2.55, y0 - 0.2)
            ax.add_patch(plt.Circle((x + 2.55, y0), 0.2, fc="white", ec=NAVY, lw=1.2))
            ax.text(x + 2.55, y0, "Σ", ha="center", va="center", fontsize=FSW, color=NAVY)
            ax.text(x + 2.8, y0 - 0.38, "−", ha="left", va="center", fontsize=FSW, color=RED)
            arrow(ax, x + 0.9, y0, x + 2.35, y0)
            x += 2.75
        arrow(ax, x, y0, x + 0.6, y0)
        ax.text(x + 0.7, y0, "y_m", fontsize=FSW, ha="left", va="center", color=INK)
    finalize(fig, "L29-canceller-blocks")


def setup_fig() -> None:
    with plt.rc_context(WIDE):
        _setup_fig()


def _setup_fig() -> None:
    fig, ax = plt.subplots(figsize=(5.4, 2.6))
    ax.set_xlim(-0.9, 3.0)
    ax.set_ylim(-1.0, 1.0)
    ax.set_aspect("equal")
    ax.axis("off")
    ax.fill([0, 2.8, 2.8], [0, 0.95, -0.95], color="#eef4fa", lw=0)
    ax.add_patch(plt.Rectangle((-0.18, -0.3), 0.18, 0.6, fc=NAVY, ec=NAVY))
    ax.text(-0.25, 0.42, "kit, Tx on OUT2", ha="center", va="bottom", fontsize=FSW, color=NAVY)
    ax.plot([2.5, 2.5], [-0.8, 0.8], color=RED, lw=3)
    ax.text(2.5, -0.92, "wall or plate,\nabout 2.5 m", ha="center", va="top", fontsize=FSW, color=RED)
    ax.plot(1.0, 0.0, "o", color=AMBER, ms=8)
    ax.text(1.0, 0.13, "hand, 1 m", ha="center", va="bottom", fontsize=FSW, color=AMBER)
    ax.plot(0.5, -0.05, "s", color=GREEN, ms=7)
    ax.text(0.5, -0.2, "spinner, 0.5 m", ha="center", va="top", fontsize=FSW, color=GREEN)
    ax.plot(-0.6, -0.65, "o", color=GRAY, ms=12, mfc="white", mew=1.5)
    ax.text(-0.6, -0.82, "you, clear\nof the beam", ha="center", va="top", fontsize=FSW, color=GRAY)
    finalize(fig, "L29-setup")


def hand_moves() -> None:
    with plt.rc_context(WIDE):
        _hand_moves()


def _hand_moves() -> None:
    fig, axs = plt.subplots(1, 2, figsize=(5.4, 2.0))
    for ax, title, along in ((axs[0], "push and pull: along", True), (axs[1], "across: no radial speed", False)):
        ax.set_xlim(-0.3, 1.6)
        ax.set_ylim(-0.6, 0.7)
        ax.set_aspect("equal")
        ax.axis("off")
        ax.add_patch(plt.Rectangle((-0.12, -0.25), 0.12, 0.5, fc=NAVY, ec=NAVY))
        ax.plot([0, 1.5], [0, 0], color=LIGHT, lw=1, ls=":")
        ax.plot(1.0, 0, "o", color=AMBER, ms=9)
        if along:
            ax.annotate("", xy=(0.6, 0), xytext=(1.4, 0), arrowprops=dict(arrowstyle="<->", color=AMBER, lw=2))
        else:
            ax.annotate("", xy=(1.0, 0.45), xytext=(1.0, -0.45), arrowprops=dict(arrowstyle="<->", color=AMBER, lw=2))
        ax.text(0.7, 0.62, title, ha="center", va="top", fontsize=FSW, color=INK)
    finalize(fig, "L29-hand-moves")


def spinner_orient() -> None:
    with plt.rc_context(WIDE):
        _spinner_orient()


def _spinner_orient() -> None:
    fig, axs = plt.subplots(1, 2, figsize=(5.4, 2.1))
    th = np.linspace(0, 2 * np.pi, 200)
    for ax, title, edge in ((axs[0], "edge-on: in and out", True), (axs[1], "face-on: across", False)):
        ax.set_xlim(-0.3, 1.6)
        ax.set_ylim(-0.6, 0.7)
        ax.set_aspect("equal")
        ax.axis("off")
        ax.add_patch(plt.Rectangle((-0.12, -0.25), 0.12, 0.5, fc=NAVY, ec=NAVY))
        ax.plot([0, 1.5], [0, 0], color=LIGHT, lw=1, ls=":")
        if edge:                      # seen from above, the plane of rotation holds the line of sight
            ax.plot(1.0 + 0.3 * np.cos(th), 0.3 * np.sin(th), color=GREEN, lw=2)
            ax.annotate("", xy=(0.72, -0.1), xytext=(0.72, 0.1), arrowprops=dict(arrowstyle="-|>", color=GREEN, lw=1.5))
        else:                         # seen from above, the spinner is a line across the beam
            ax.plot([1.0, 1.0], [-0.3, 0.3], color=GREEN, lw=4)
            ax.annotate("", xy=(1.0, 0.45), xytext=(1.0, 0.33), arrowprops=dict(arrowstyle="-|>", color=GREEN, lw=1.5))
        ax.text(0.7, 0.66, title, ha="center", va="top", fontsize=FSW, color=INK)
    finalize(fig, "L29-spinner-orient")


if __name__ == "__main__":
    for kk, vv in V.items():
        print(f"   {kk:20s} {vv:.4g}")
    chirp_sync()
    data_matrix()
    rd_map()
    canceller()
    mti_maps()
    spinner_cut()
    spectrogram_fig()
    burst_choices()
    phasor_fig()
    canceller_blocks()
    setup_fig()
    hand_moves()
    spinner_orient()
