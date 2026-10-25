#!/usr/bin/env python3
"""Generate the L26 (Range, Resolution, and Doppler) figures as inline SVG.

  - L26-pulse-train   : transmitted pulses, a near echo, and a far echo that
                        arrives after the next pulse (unambiguous range)
  - L26-resolution    : two echoes a pulse length apart in time (resolved) and
                        a third of one apart (merged)
  - L26-radial        : a target's velocity and its radial component
  - L26-fan-spectrum  : the CW Doppler spectrum of a fan viewed edge-on
  - L26-micro-doppler : the spectrogram of a walker, torso and two limbs

The lesson page shows all five from book/extras/viz/img/. None carries an
equation: symbols, numbers, and short words only.

Each figure sits in a present block beside text, about 477 px wide on a 1280
laptop and 343 px on a phone. They are drawn about 420 units wide with no text
under 13 units, so the smallest label is 10.5 px or more on the phone;
check_text() asserts it on the written file.

Every number a figure shows, and every number the page and the practice set
print, is computed here and asserted, so the three cannot drift apart.

    python3 scripts/graphics/m4_l26_range_doppler.py
"""

from __future__ import annotations

import io
import re
from pathlib import Path
from svg_font_stack import apply_font_stack

import numpy as np
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
from matplotlib.patches import FancyArrowPatch, Rectangle  # noqa: E402

NAVY, BLUE, RED, GREEN, AMBER, GRAY = "#004a85", "#0067b9", "#b01e24", "#1d7a4d", "#8a5a00", "#5a5a5a"
INK, RULE, LIGHT = "#1a1a1a", "#c7d2e0", "#9fb1c2"

IMG = Path(__file__).resolve().parents[2] / "book/extras/viz/img"

C = 3.0e8                    # the course's c
F0 = 10.0e9                  # a radar near 10 GHz, as in ADI's radar labs
LAM = C / F0                 # 3.0 cm
MPH = 0.44704                # m/s per mph

PHONE_COL, PX_MIN = 343.0, 10.5

plt.rcParams.update(
    {
        "svg.fonttype": "none",
        "svg.hashsalt": "ece444-L26",
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


def check_text(name: str, svg: str) -> None:
    """Every label is 10.5 px or more at a 343 px column."""
    vb = re.search(r'viewBox="0 0 ([\d.]+) ([\d.]+)"', svg)
    w = float(vb.group(1))
    sizes = [float(x) for x in re.findall(r"font-size:\s*([\d.]+)px", svg)]
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


def style(ax):
    for side in ("top", "right"):
        ax.spines[side].set_visible(False)
    ax.tick_params(length=3)


def doppler(v, lam=LAM):
    """Two-way Doppler shift, positive for a closing target."""
    return 2.0 * v / lam


# ---------------------------------------------------------------- numbers --

def numbers() -> dict:
    v = {}
    v["ns_per_m"] = 2.0 / C * 1e9                       # round-trip delay per meter
    v["tau_3m_ns"] = 2.0 * 3.0 / C * 1e9
    v["R_40us_km"] = C * 40e-6 / 2 / 1e3                # an echo at 40 us
    v["Rua_1k_km"] = C / (2 * 1e3) / 1e3                # PRF 1 kHz
    v["fold_170_km"] = 170.0 - v["Rua_1k_km"]           # 170 km target at PRF 1 kHz
    v["dR_1us_m"] = C * 1e-6 / 2
    v["dR_500M_m"] = C / (2 * 500e6)
    v["lam_cm"] = LAM * 100
    v["fd_1mps"] = doppler(1.0)
    v["v100"] = 100 * MPH
    v["fd100_2g4"] = doppler(v["v100"], C / 2.4e9)
    v["fd100_10g"] = doppler(v["v100"])
    # ADI's own quotes come from c = 2.998e8
    v["adi_2g4"] = 2 * v["v100"] * 2.4e9 / 2.998e8
    v["adi_10g"] = 2 * v["v100"] * 10e9 / 2.998e8
    v["ratio_10g"] = v["fd100_10g"] / F0
    v["vr_60"] = 200 * np.cos(np.radians(60))
    v["fd_vr_60_khz"] = doppler(v["vr_60"]) / 1e3
    # a burst of pulses (ADI's range-Doppler example: 0.5 ms PRI, 256 chirps)
    pri, m = 0.5e-3, 256
    v["T_burst_ms"] = pri * m * 1e3
    v["df_burst"] = 1 / (pri * m)
    v["dv_burst"] = LAM / (2 * pri * m)
    v["vua_burst"] = LAM / (4 * pri)
    v["Rua_burst_km"] = C * pri / 2 / 1e3
    v["product"] = C * LAM / 8
    v["Rua_1k_vua"] = LAM * 1e3 / 4                    # PRF 1 kHz
    # ADI's CW script: 65,536 samples at 0.6 MHz
    ncw, fs = 64 * 1024, 0.6e6
    v["cw_T_ms"] = ncw / fs * 1e3
    v["cw_bin"] = fs / ncw
    v["cw_dv"] = LAM * v["cw_bin"] / 2
    # a 0.3 m fan at 1200 rpm, seen edge-on
    v["tip"] = np.pi * 0.30 * 1200 / 60
    v["fd_tip"] = doppler(v["tip"])
    # a walker: torso 1.3 m/s, limbs to 4.0 m/s
    v["fd_torso"] = doppler(1.3)
    v["fd_limb"] = doppler(4.0)
    return v


def check_numbers(v: dict) -> None:
    """The values the page and the practice set print."""
    assert f"{v['ns_per_m']:.2f}" == "6.67"
    assert f"{v['tau_3m_ns']:.0f}" == "20"
    assert f"{v['R_40us_km']:.0f}" == "6"
    assert f"{v['Rua_1k_km']:.0f}" == "150" and f"{v['fold_170_km']:.0f}" == "20"
    assert f"{v['dR_1us_m']:.0f}" == "150" and f"{v['dR_500M_m']:.2f}" == "0.30"
    assert f"{v['lam_cm']:.1f}" == "3.0" and f"{v['fd_1mps']:.1f}" == "66.7"
    assert f"{v['v100']:.1f}" == "44.7"
    assert f"{v['fd100_2g4']:.0f}" == "715" and f"{v['fd100_10g']:.0f}" == "2980"
    assert f"{v['adi_2g4']:.0f}" == "716" and f"{v['adi_10g']:.0f}" == "2982"
    assert f"{v['ratio_10g'] * 1e7:.1f}" == "3.0"
    assert f"{v['vr_60']:.0f}" == "100" and f"{v['fd_vr_60_khz']:.2f}" == "6.67"
    assert f"{v['T_burst_ms']:.0f}" == "128" and f"{v['df_burst']:.1f}" == "7.8"
    assert f"{v['dv_burst']:.2f}" == "0.12" and f"{v['vua_burst']:.0f}" == "15"
    assert f"{v['Rua_burst_km']:.0f}" == "75"
    assert f"{v['product']:.3g}" == "1.12e+06" and f"{v['Rua_1k_vua']:.1f}" == "7.5"
    assert f"{v['cw_T_ms']:.0f}" == "109" and f"{v['cw_bin']:.1f}" == "9.2"
    assert f"{v['cw_dv']:.2f}" == "0.14"
    assert f"{v['tip']:.1f}" == "18.8" and f"{v['fd_tip']:.0f}" == "1257"
    assert f"{v['fd_torso']:.0f}" == "87" and f"{v['fd_limb']:.0f}" == "267"


# ---------------------------------------------------------------- figures --

def pulse(ax, t0, width, y0, h, color, ls="-", fill=True, alpha=1.0):
    if fill:
        ax.add_patch(Rectangle((t0, y0), width, h, color=color, alpha=alpha, lw=0))
    else:
        ax.add_patch(Rectangle((t0, y0), width, h, fill=False, ec=color, lw=1.4, ls=ls))


def fig_pulse_train() -> None:
    """PRI 1 ms (150 km); a near target at 60 km and a far one at 170 km."""
    pri, w = 1.0, 0.05                      # ms
    t_near = 2 * 60e3 / C * 1e3             # 0.40 ms
    t_far = 2 * 170e3 / C * 1e3             # 1.133 ms
    fig, ax = plt.subplots(figsize=(4.6, 2.5))
    ytx, yrx, h = 1.6, 0.0, 0.8
    for k in range(3):
        pulse(ax, k * pri, w, ytx, h, NAVY)
        pulse(ax, k * pri + t_near, w, yrx, h * 0.55, BLUE)
        if k * pri + t_far < 2.6:
            pulse(ax, k * pri + t_far, w, yrx, h * 0.3, RED)
    ax.text(-0.04, ytx + h / 2, "sent", ha="right", va="center", color=NAVY)
    ax.text(-0.04, yrx + 0.25, "echo", ha="right", va="center", color=BLUE)
    # PRI
    ya = ytx + h + 0.25
    ax.annotate("", xy=(0, ya), xytext=(pri, ya),
                arrowprops=dict(arrowstyle="<->", color=GRAY, lw=1.0, shrinkA=0, shrinkB=0))
    ax.text(pri / 2, ya + 0.08, "PRI", ha="center", va="bottom", color=GRAY)
    # near delay
    yb = yrx + h * 0.55 + 0.2
    ax.annotate("", xy=(0, yb), xytext=(t_near, yb),
                arrowprops=dict(arrowstyle="<->", color=BLUE, lw=1.0, shrinkA=0, shrinkB=0))
    ax.text(t_near / 2, yb + 0.06, "60 km", ha="center", va="bottom", color=BLUE)
    # far echo, read against the pulse just before it
    ax.plot([pri, pri, t_far, t_far], [-0.15, -0.35, -0.35, -0.15], color=RED, lw=1.2)
    ax.text(t_far + 0.08, -0.35, "170 km reads 20 km", ha="left", va="center", color=RED)
    ax.set_xlim(-0.05, 2.6)
    ax.set_ylim(-0.7, 3.0)
    ax.set_yticks([])
    ax.set_xticks([0, 1, 2])
    ax.set_xlabel("time (ms)")
    for side in ("top", "right", "left"):
        ax.spines[side].set_visible(False)
    finalize(fig, "L26-pulse-train")


def fig_resolution() -> None:
    """Two equal echoes from a 1 us pulse, 225 m apart and 75 m apart."""
    tau = 1.0
    fig, axs = plt.subplots(2, 1, figsize=(4.4, 2.9), sharex=True)
    for ax, dR, ok in ((axs[0], 225.0, True), (axs[1], 75.0, False)):
        dt = 2 * dR / C * 1e6
        ax.add_patch(Rectangle((0, 0), tau, 1, color=BLUE, alpha=0.35, lw=0))
        ax.add_patch(Rectangle((dt, 0), tau, 1, color=AMBER, alpha=0.35, lw=0))
        # the receiver sees the sum: exact corners, no sampling
        edges = sorted({-0.3, 0.0, tau, dt, dt + tau, 2.7})
        tt, yy = [], []
        for lo, hi in zip(edges[:-1], edges[1:]):
            mid = 0.5 * (lo + hi)
            lev = float(0 <= mid < tau) + float(dt <= mid < dt + tau)
            tt += [lo, hi]
            yy += [lev, lev]
        ax.plot(tt, yy, color=NAVY, lw=1.4)
        ax.text(4.6, 1.5, f"{dR:.0f} m apart", ha="right", va="center",
                color=GREEN if ok else RED)
        ax.text(4.6, 0.75, "two echoes" if ok else "one echo", ha="right", va="center",
                color=GREEN if ok else RED)
        ax.set_ylim(0, 2.2)
        ax.set_yticks([])
        for side in ("top", "right", "left"):
            ax.spines[side].set_visible(False)
    axs[1].set_xlim(-0.3, 4.6)
    axs[1].set_xticks([0, 1, 2])
    axs[1].set_xlabel("echo time (µs)")
    fig.subplots_adjust(hspace=0.25)
    finalize(fig, "L26-resolution")


def fig_radial() -> None:
    """A target moving at v, alpha off the line of sight to the radar."""
    fig, ax = plt.subplots(figsize=(4.4, 2.3))
    tgt = np.array([3.4, 0.0])
    alpha = np.radians(55)
    vlen = 1.6
    vtip = tgt + vlen * np.array([-np.cos(alpha), np.sin(alpha)])
    p = tgt + np.array([-vlen * np.cos(alpha), 0.0])
    ax.plot([0, tgt[0]], [0, 0], color=LIGHT, lw=1.0, ls="--")
    ax.plot(0, 0, "s", ms=9, color=NAVY)
    ax.text(0, -0.22, "radar", ha="center", va="top", color=NAVY)
    ax.text(1.1, 0.08, "line of sight", ha="center", va="bottom", color=GRAY)
    ax.plot(*tgt, "o", ms=8, color=INK)
    ax.add_patch(FancyArrowPatch(tgt, vtip, arrowstyle="-|>", mutation_scale=14, color=INK, lw=1.6))
    ax.text(vtip[0] - 0.1, vtip[1], "v", color=INK, fontsize=15, style="italic", ha="right",
            va="center")
    ax.add_patch(FancyArrowPatch(tgt, p, arrowstyle="-|>", mutation_scale=14, color=RED, lw=2.2))
    ax.text(0.5 * (tgt[0] + p[0]), -0.12, "v cos α", color=RED, ha="center", va="top")
    ax.plot([p[0], vtip[0]], [0, vtip[1]], color=GRAY, lw=0.8, ls=":")
    arc = np.linspace(np.pi - alpha, np.pi, 30)
    ax.plot(tgt[0] + 0.45 * np.cos(arc), 0.45 * np.sin(arc), color=GRAY, lw=1.0)
    am = np.pi - alpha / 2
    ax.text(tgt[0] + 0.62 * np.cos(am), 0.62 * np.sin(am), "α", color=GRAY, ha="center",
            va="center")
    ax.set_xlim(-0.5, 3.7)
    ax.set_ylim(-0.6, 1.5)
    ax.set_aspect("equal")
    ax.axis("off")
    finalize(fig, "L26-radial")


def fig_fan_spectrum(v: dict) -> None:
    """A 0.3 m, three-blade fan at 1200 rpm, seen edge-on by a CW radar at 10 GHz.

    Each blade is a line of point scatterers from the hub to the tip. A point
    at radius rho moves along the line of sight as rho cos(Omega t + phase), so
    its Doppler swings between +-2 Omega rho / lambda; the tips set the edges.
    The hub and the stand do not move and sit at 0 Hz.  One 109 ms spectrum,
    as ADI's CW script takes, averaged over a few frames."""
    fs, T = 8000.0, v["cw_T_ms"] / 1e3
    n = int(round(fs * T))
    om = 2 * np.pi * 1200 / 60
    rho = np.linspace(0.03, 0.15, 60)
    rng = np.random.default_rng(26)
    spec = np.zeros(n)
    for frame in range(6):
        t = frame * T + np.arange(n) / fs
        s = 2.0 * np.ones(n, dtype=complex)                       # hub and stand
        for b in range(3):
            ph = om * t[:, None] + 2 * np.pi * b / 3
            x = rho[None, :] * np.cos(ph)
            s += (0.08 * np.exp(1j * 4 * np.pi * x / LAM)).sum(axis=1)
        s += (rng.standard_normal(n) + 1j * rng.standard_normal(n)) * 0.05
        S = np.fft.fftshift(np.fft.fft(s * np.hanning(n)))
        spec += np.abs(S) ** 2
    f = np.fft.fftshift(np.fft.fftfreq(n, 1 / fs))
    db = 10 * np.log10(spec / spec.max())
    fig, ax = plt.subplots(figsize=(4.4, 2.7))
    ax.plot(f / 1e3, db, color=BLUE, lw=0.8)
    edge = v["fd_tip"] / 1e3
    for s in (-1, 1):
        ax.axvline(s * edge, color=RED, lw=1.0, ls="--")
    ax.text(edge + 0.06, -8, "tips\n±1.26 kHz", color=RED, ha="left", va="top")
    ax.text(0.08, -2, "hub", color=NAVY, ha="left", va="center")
    ax.set_xlim(-2.0, 2.0)
    ax.set_ylim(-60, 3)
    ax.set_xticks([-2, -1, 0, 1, 2])
    ax.set_yticks([-60, -40, -20, 0])
    ax.set_xlabel("Doppler (kHz)")
    ax.set_ylabel("power (dB)")
    style(ax)
    finalize(fig, "L26-fan-spectrum")


def fig_micro_doppler(v: dict) -> None:
    """A walker at 1.3 m/s toward the radar, with two limbs swinging in
    opposite phase at one stride a second, each reaching 4.0 m/s. Spectrogram
    with a 64 ms Hann window."""
    fs, T = 1000.0, 3.0
    t = np.arange(int(fs * T)) / fs
    vt = 1.3 * np.ones_like(t)
    v1 = 1.3 + 2.7 * np.sin(2 * np.pi * t)
    v2 = 1.3 - 2.7 * np.sin(2 * np.pi * t)
    def ret(vel, a):
        x = np.cumsum(vel) / fs                 # closing distance
        return a * np.exp(1j * 4 * np.pi * x / LAM)
    rng = np.random.default_rng(31)
    s = ret(vt, 1.0) + ret(v1, 0.35) + ret(v2, 0.35)
    s += (rng.standard_normal(t.size) + 1j * rng.standard_normal(t.size)) * 0.02
    nw, hop = 64, 8
    win = np.hanning(nw)
    cols = []
    for i in range(0, t.size - nw, hop):
        S = np.fft.fftshift(np.fft.fft(s[i:i + nw] * win, 256))
        cols.append(np.abs(S) ** 2)
    P = np.array(cols).T
    P = 10 * np.log10(P / P.max())
    f = np.fft.fftshift(np.fft.fftfreq(256, 1 / fs))
    tc = (np.arange(P.shape[1]) * hop + nw / 2) / fs
    fig, ax = plt.subplots(figsize=(4.4, 2.8))
    # an embedded bitmap: a vector mesh of every cell would be megabytes
    ax.imshow(np.clip(P, -40, 0), origin="lower", aspect="auto", cmap="Blues",
              extent=(tc[0], tc[-1], f[0], f[-1]), interpolation="bilinear")
    ax.axhline(0, color=GRAY, lw=0.6)
    ax.text(3.08, v["fd_torso"], "torso", color=NAVY, ha="left", va="center")
    ax.text(3.08, 200, "limbs", color=RED, ha="left", va="center")
    ax.set_xlim(0, 3)
    ax.set_ylim(-200, 330)
    ax.set_yticks([-200, 0, 87, 267])
    ax.set_xticks([0, 1, 2, 3])
    ax.set_xlabel("time (s)")
    ax.set_ylabel("Doppler (Hz)")
    style(ax)
    finalize(fig, "L26-micro-doppler")


def main() -> None:
    v = numbers()
    check_numbers(v)
    for k, x in v.items():
        print(f"   {k:14s} {x:.6g}")
    fig_pulse_train()
    fig_resolution()
    fig_radial()
    fig_fan_spectrum(v)
    fig_micro_doppler(v)


if __name__ == "__main__":
    main()
