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

Every map is computed the way the L29 Lab computes one: a burst of beat
signals with the course's range-Doppler numbers (COURSE_SPEC M8: 10 GHz,
500 MHz in 300 us, 256 chirps at a 0.5 ms PRI, 4 MSPS, a 100 kHz 0 m
frequency), a Hann-windowed range FFT along each chirp, a Hann-windowed
Doppler FFT across the chirps. Every number the page prints is computed and
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

# ------------------------------------------------------------ M8 burst numbers
C = 3.00e8
FC = 10.0e9
LAM = C / FC                 # 3.0 cm
B = 500e6
T_RAMP = 300e-6
PRI = 0.5e-3
M = 256
FS = 4e6
N = int(round(FS * T_RAMP))  # 1200 samples on each ramp
F0 = 100e3                   # the 0 m frequency, set per kit by the L28 calibration
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
    v["deg_per_chirp_1mps"] = np.degrees(4 * np.pi * 1.0 * PRI / LAM)
    v["fb_hand"] = F0 + 2 * SLOPE * 1.5 / C            # hand at 1.5 m
    v["deg_per_us_hand"] = 360 * v["fb_hand"] * 1e-6
    v["fd_15"] = 2 * 15 / LAM
    v["range_err_15"] = v["fd_15"] * C / (2 * SLOPE)
    v["migrate_1mps"] = 1.0 * M * PRI
    v["dv_32"] = LAM / (2 * 32 * PRI)
    v["dv_128"] = LAM / (2 * 128 * PRI)
    v["dR_200"] = C / (2 * 200e6)
    # canceller power gains
    x = np.pi * v["fd_per_mps"] * 1.0 * PRI
    v["h2_1"] = 10 * np.log10(4 * np.sin(x) ** 2)
    v["h3_1"] = 10 * np.log10(16 * np.sin(x) ** 4)
    v["h2_max"] = 10 * np.log10(4)
    v["h3_max"] = 10 * np.log10(16)
    v["n2"] = 10 * np.log10(2)
    v["n3"] = 10 * np.log10(6)
    v["snr2_1"] = v["h2_1"] - v["n2"]
    v["snr3_1"] = v["h3_1"] - v["n3"]
    return v


V = numbers()
for key, want, tol in (
    ("kHz_per_m", 11.1, 0.05), ("dR", 0.30, 1e-9), ("bin_kHz", 3.33, 0.01),
    ("cpi_ms", 128, 1e-9), ("dv", 0.12, 0.005), ("vmax", 15.0, 1e-9),
    ("vblind", 30.0, 1e-9), ("fd_per_mps", 66.7, 0.05), ("deg_per_chirp_1mps", 12.0, 0.05),
    ("fb_hand", 116.7e3, 50), ("deg_per_us_hand", 42.0, 0.05), ("fd_15", 1000, 1e-6),
    ("range_err_15", 0.09, 0.005), ("migrate_1mps", 0.128, 1e-9),
    ("dv_32", 0.94, 0.005), ("dv_128", 0.23, 0.005), ("dR_200", 0.75, 1e-9),
    ("h2_1", -13.6, 0.05), ("h3_1", -27.2, 0.05), ("h2_max", 6.0, 0.05), ("h3_max", 12.0, 0.05),
    ("n2", 3.0, 0.05), ("n3", 7.8, 0.05), ("snr2_1", -16.6, 0.05), ("snr3_1", -35.0, 0.05),
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
    (0.25, 3.0, 0.0, None),              # a wall
    (0.03, 1.5, 1.0, None),              # a hand, closing at 1.0 m/s
    (0.03, 2.1, 0.0, (0.035, 10.0, 3)),  # a fidget spinner, tips at 2.2 m/s
]


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
    hand = [(0.012, 1.5, 1.0, None)]
    out = {}
    for sync in (True, False):
        rd, r, vel = range_doppler(burst(hand, np.random.default_rng(3), sync=sync, noise=0.01))
        k = np.argmin(np.abs(r - 1.5))
        out[sync] = db(rd[:, k])
    ref = out[True].max()
    fig, ax = plt.subplots(figsize=(4.4, 2.6))
    ax.plot(vel, out[False] - ref, color=RED, lw=1.0)
    ax.plot(vel, out[True] - ref, color=NAVY, lw=1.6)
    ax.text(1.6, -2, "synchronized", color=NAVY, ha="left", va="center")
    ax.text(-14.5, -15, "random start", color=RED, ha="left", va="bottom")
    ax.set_xlim(-15, 15)
    ax.set_ylim(-60, 4)
    ax.set_xticks([-15, -10, -5, 0, 5, 10, 15])
    ax.set_yticks([-60, -40, -20, 0])
    ax.set_xlabel("velocity (m/s)")
    ax.set_ylabel("power (dB)")
    tidy(ax)
    finalize(fig, "L29-chirp-sync")


def data_matrix() -> None:
    hand = [(1.0, 1.5, 1.0, None)]
    x = burst(hand, np.random.default_rng(1), jitter_rad=0, noise=0.05)
    mm, nn = 96, 160
    fig, ax = plt.subplots(figsize=(4.4, 3.0))
    ax.imshow(x[:mm, :nn].real, origin="upper", aspect="auto", cmap="RdBu_r",
              vmin=-1.3, vmax=1.3, extent=(-0.5, nn - 0.5, mm - 0.5, -0.5), interpolation="nearest")
    ax.set_xlabel("sample n, 0.25 µs apart (fast time)")
    ax.set_ylabel("chirp m, 0.5 ms apart\n(slow time)")
    ax.set_xticks([0, 40, 80, 120, 160])
    ax.set_yticks([0, 32, 64, 96])
    for s in ax.spines.values():
        s.set_visible(False)
    finalize(fig, "L29-data-matrix")


MAP = matplotlib.colors.LinearSegmentedColormap.from_list(
    "l29", [(0.0, "#ffffff"), (0.2, "#dbe7f2"), (0.4, "#7fb0dc"), (0.6, "#0067b9"), (0.8, "#004a85"), (1.0, "#00213d")])


def rd_panel(ax, P, r, vel, lo=-75, rmax=4.0) -> None:
    keep = (r >= -0.15) & (r <= rmax)
    rr = r[keep]
    order = np.argsort(rr)
    img = P[:, keep][:, order]
    ax.imshow(np.clip(img.T, lo, 0), origin="lower", aspect="auto", cmap=MAP,
              extent=(vel[0], vel[-1], rr[order][0], rr[order][-1]), interpolation="nearest",
              vmin=lo, vmax=0)
    ax.set_xlim(-6, 6)
    ax.set_ylim(-0.15, rmax)
    ax.set_xticks([-5, 0, 5])


def rd_map() -> None:
    rd, r, vel = range_doppler(burst(SCENE, np.random.default_rng(5)))
    P = db(rd)
    P -= P.max()
    fig, ax = plt.subplots(figsize=(4.4, 3.2))
    rd_panel(ax, P, r, vel)
    ax.set_xlabel("velocity (m/s)")
    ax.set_ylabel("range (m)")
    lab = dict(fontsize=13, va="center")
    ax.text(0.5, 0.15, "leakage", color=RED, ha="left", **lab)
    ax.text(0.5, 3.0, "wall", color=RED, ha="left", **lab)
    ax.text(1.5, 1.5, "hand", color=NAVY, ha="left", **lab)
    ax.text(2.8, 2.1, "spinner", color=NAVY, ha="left", **lab)
    finalize(fig, "L29-rd-map")


def canceller() -> None:
    v = np.linspace(-35, 35, 2801)
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
    ax.text(0, 19, "±15 m/s", color=GRAY, ha="center", va="bottom", fontsize=13)
    ax.text(-15, 13, "3-pulse", color=AMBER, ha="center", va="bottom")
    ax.text(15, 4, "2-pulse", color=NAVY, ha="center", va="top")
    ax.set_xlim(-35, 35)
    ax.set_ylim(-40, 19)
    ax.set_xticks([-30, -15, 0, 15, 30])
    ax.set_yticks([-40, -20, 0])
    ax.set_xlabel("velocity (m/s)")
    ax.set_ylabel("gain (dB)")
    tidy(ax)
    finalize(fig, "L29-canceller")


def mti_maps() -> None:
    x = burst(SCENE, np.random.default_rng(5))
    maps = []
    for kind in ("none", "2pulse", "3pulse"):
        rd, r, vel = range_doppler(mti(x, kind))
        maps.append((kind, db(rd), r, vel))
    ref = maps[0][1].max()
    fig, axs = plt.subplots(1, 3, figsize=(5.4, 2.9), sharey=True)
    for ax, (kind, P, r, vel), title in zip(axs, maps, ("no MTI", "2-pulse", "3-pulse")):
        rd_panel(ax, P - ref, r, vel)
        ax.set_title(title, fontsize=13, color=INK)
        ax.set_xticks([-5, 0, 5])
    axs[0].set_ylabel("range (m)")
    axs[1].set_xlabel("velocity (m/s)")
    fig.subplots_adjust(wspace=0.08)
    finalize(fig, "L29-mti-maps")
    # the hand's peak, against no MTI, as the page quotes it
    k = np.argmin(np.abs(maps[0][2] - 1.5))
    peaks = [P[:, k].max() for _, P, _, _ in maps]
    print(f"   hand peak: 2-pulse {peaks[1] - peaks[0]:+.1f} dB, 3-pulse {peaks[2] - peaks[0]:+.1f} dB")


if __name__ == "__main__":
    for kk, vv in V.items():
        print(f"   {kk:20s} {vv:.4g}")
    chirp_sync()
    data_matrix()
    rd_map()
    canceller()
    mti_maps()
