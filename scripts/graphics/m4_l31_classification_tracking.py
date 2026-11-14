#!/usr/bin/env python3
"""Generate the L31 (Classification and Tracking) figures as inline SVG.

  - L31-signatures    : slow-time spectrograms of the four kinds of lab target,
                        a walker, a fan, a fidget spinner, and a waving hand
  - L31-features      : the training trials in the centroid-spread plane,
                        with each class's mean
  - L31-alpha-beta    : range detections of a walker who walks out, turns,
                        and walks back, and two alpha-beta tracks of them

The lesson page shows all three from book/extras/viz/img/. None carries an
equation: symbols, numbers, and short words only.

The targets are simulated in slow time, one complex sample per chirp, each
as a few point scatterers whose range changes with time; the carrier turns
each one's range into a phase 4 pi R / lambda. The lesson half of the L31
page is read before the lab and works every Part 1 method on an example
burst the Phaser app does not use (Neil, 2026-11-12): 10.0 GHz, 400 MHz
chirps of 300 us every 0.4 ms, 256 a frame, so the CPI is 102.4 ms and the
range bin 0.375 m. The example targets differ from the lab's records too, so
no number here is a packet answer. spectrogram(), features(),
classify() and alpha_beta() below are the functions the page excerpts, with
the same names as the shared radar_lab.py contract, so the page and this
script cannot drift apart.

Every number the page prints is computed here and asserted.

    python3 scripts/graphics/m4_l31_classification_tracking.py
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

NAVY, BLUE, RED, GREEN, AMBER, GRAY = "#004a85", "#0067b9", "#b01e24", "#1d7a4d", "#8a5a00", "#5a5a5a"
INK = "#1a1a1a"

IMG = Path(__file__).resolve().parents[2] / "book/extras/viz/img"

C = 3.0e8
F0 = 10.0e9                  # the lesson's example carrier, not a kit's preset
LAM = C / F0                 # 3.0 cm
B_EX = 400e6                 # the example chirp's bandwidth
PRI = 0.4e-3                 # one slow-time sample per chirp
CPI = 256 * PRI              # one range-Doppler frame, 102.4 ms
BIN = C / (2 * B_EX)         # one range bin, 0.375 m
KINDS = ["walker", "fan", "spinner", "hand"]
COLORS = {"walker": NAVY, "fan": RED, "spinner": AMBER, "hand": GREEN}
MARKERS = {"walker": "o", "fan": "s", "spinner": "^", "hand": "D"}

PHONE_COL, PX_MIN = 343.0, 10.5

plt.rcParams.update(
    {
        "svg.fonttype": "none",
        "svg.hashsalt": "ece444-L31",
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


# ----------------------------------------------------------------- targets --

def echo(x, a):
    """The slow-time return of one point scatterer that has closed by x meters."""
    return a * np.exp(1j * 4 * np.pi * x / LAM)


def target(kind: str, p: dict, T: float, rng) -> np.ndarray:
    """One range bin's slow-time samples for one target, plus noise.

    walker  : torso closing at v0, two limbs swinging in opposite phase about
              it at the stride rate, each reaching v0 +- A (L26's model)
    fan     : three blades of point scatterers from hub to tip, edge-on
    spinner : three weighted arms near its rim
    hand    : one scatterer swinging back and forth
    Rotors also carry a stationary hub, which the spectrogram's mean
    subtraction removes as MTI would."""
    t = np.arange(int(round(T / PRI))) * PRI
    s = np.zeros(t.size, complex)
    if kind == "walker":
        x0 = p["v0"] * t
        s += echo(x0, 1.0)
        for sgn in (1, -1):
            s += echo(x0 - sgn * p["A"] / (2 * np.pi * p["fst"]) * np.cos(2 * np.pi * p["fst"] * t + p["ph"]), 0.35)
    elif kind in ("fan", "spinner"):
        if kind == "fan":
            rho, a = np.linspace(0.015, p["R"], 25), 0.05
        else:
            rho, a = np.array([0.8 * p["R"], p["R"]]), 0.25
        om = 2 * np.pi * p["rpm"] / 60
        for b in range(3):
            ph = om * t + p["ph"] + 2 * np.pi * b / 3
            s += (a * np.exp(1j * 4 * np.pi * rho[None, :] * np.cos(ph)[:, None] / LAM)).sum(axis=1)
        s += 2.0
    else:
        s += echo(p["A"] * np.sin(2 * np.pi * p["f"] * t + p["ph"]), 0.6)
    pw = np.mean(np.abs(s - s.mean()) ** 2)
    n = np.sqrt(pw / 10 ** (p["snr_db"] / 10) / 2)
    return s + n * (rng.standard_normal(t.size) + 1j * rng.standard_normal(t.size))


def draw_params(kind: str, rng) -> dict:
    """One lab trial: the spread a class shows from trial to trial.

    A walker or a hand at aspect alpha off the line of sight shows only
    cos(alpha) of its motion (L26). SNR per chirp 3-15 dB."""
    p = {"snr_db": rng.uniform(3, 15), "ph": rng.uniform(0, 2 * np.pi)}
    if kind == "walker":
        ca = rng.uniform(0.5, 1.0)
        p.update(v0=rng.uniform(0.7, 1.5) * rng.choice([-1, 1]) * ca,
                 fst=rng.uniform(0.8, 1.1), A=rng.uniform(2.0, 3.0) * ca)
    elif kind == "fan":
        p.update(R=0.125, rpm=rng.uniform(450, 850))
    elif kind == "spinner":
        p.update(R=0.03, rpm=rng.uniform(900, 2000))
    else:
        ca = rng.uniform(0.5, 1.0)
        p.update(A=rng.uniform(0.1, 0.3) * ca, f=rng.uniform(0.8, 2.0))
    return p


# The four signatures as the figure shows them, the lesson's examples: a walker
# closing at 1.1 m/s with limbs swinging 2.3 m/s at 0.9 strides a second, a
# 25 cm fan at 700 rpm, a 6 cm spinner at 1500 rpm, a hand waving 0.15 m at 1.2 Hz.
TYPICAL = {
    "walker": dict(v0=1.1, fst=0.9, A=2.3, ph=0.0, snr_db=15),
    "fan": dict(R=0.125, rpm=700, ph=0.0, snr_db=15),
    "spinner": dict(R=0.03, rpm=1500, ph=0.0, snr_db=15),
    "hand": dict(A=0.15, f=1.2, ph=0.0, snr_db=15),
}


# -------------------------------------------------- the radar_lab functions --

def spectrogram(x, pri=PRI, n_win=64, hop=16):
    """Slow-time spectrogram of one range bin: (t, f_D, S_dB), peak at 0 dB.

    On the page this takes (cap, range_bin) and pulls x from the cadet's
    range_fft; here x is the bin's samples directly."""
    x = x - x.mean()                           # stationary returns out
    w = np.hanning(n_win)
    cols = [np.fft.fftshift(np.fft.fft(x[i:i + n_win] * w))
            for i in range(0, len(x) - n_win + 1, hop)]
    S = 20 * np.log10(np.abs(np.array(cols).T) + 1e-12)
    f = np.fft.fftshift(np.fft.fftfreq(n_win, pri))
    t = (np.arange(S.shape[1]) * hop + n_win / 2) * pri
    return t, f, S - S.max()


def features(t, f, S, lam, floor_db=-15):
    """Centroid and spread in m/s, and periodicity, from one spectrogram.

    The 12-column smoothing is 0.1 s at the 16-chirp hop."""
    S = S - S.max(axis=0, keepdims=True)        # each column's peak at 0 dB
    P = np.where(S > floor_db, 10 ** (S / 10), 0.0)
    fc = (f[:, None] * P).sum(0) / P.sum(0)     # centroid, each column
    sd = np.sqrt(((f[:, None] - fc) ** 2 * P).sum(0) / P.sum(0))
    D = np.maximum(S, floor_db)
    D = np.array([np.convolve(row, np.ones(12) / 12, "valid") for row in D])
    D = D - D.mean(axis=1, keepdims=True)
    dt = t[1] - t[0]
    r = [np.sum(D[:, :-n] * D[:, n:]) / np.sum(D ** 2)
         for n in range(int(0.25 / dt), int(2.0 / dt))]
    return np.array([abs(fc.mean()) * lam / 2, sd.mean() * lam / 2, max(r)])


def train(X, y):
    """Nearest-centroid model: the feature scaling and each class's mean."""
    mu, sd = X.mean(0), X.std(0)
    cents = {c: ((X[y == c] - mu) / sd).mean(0) for c in KINDS}
    return mu, sd, cents


def classify(x, model):
    mu, sd, cents = model
    z = (x - mu) / sd
    return min(cents, key=lambda c: np.sum((z - cents[c]) ** 2))


def alpha_beta(track_meas, alpha, beta, dt):
    """Range track from one detection per frame (NaN for a missed frame)."""
    r, v = track_meas[0], 0.0
    out = []
    for z in track_meas:
        r = r + v * dt                         # predict
        if not np.isnan(z):
            e = z - r                          # residual
            r, v = r + alpha * e, v + beta / dt * e
        out.append((r, v))
    return np.array(out)


# ---------------------------------------------------------------- numbers --

def trials(seed: int, n: int = 20, T: float = 4.0):
    """n training and n test trials per class, the test set drawn separately."""
    rng = np.random.default_rng(seed)

    def draw():
        X, y = [], []
        for k in KINDS:
            for _ in range(n):
                X.append(features(*spectrogram(target(k, draw_params(k, rng), T, rng)), LAM))
                y.append(k)
        return np.array(X), np.array(y)

    Xtr, ytr = draw()
    Xte, yte = draw()
    model = train(Xtr, ytr)
    M = np.zeros((4, 4), int)
    for x, k in zip(Xte, yte):
        M[KINDS.index(k), KINDS.index(classify(x, model))] += 1
    return Xtr, ytr, model, M


def walk_track(seed: int = 36):
    """Out at 1.2 m/s from 2 m, a 1 s turn at 3.5 s, back at 1.2 m/s.

    One detection per 102.4 ms frame, at the center of the 0.375 m range bin the
    walker's detection falls in (a 0.12 m body jitter first), and 6% of frames
    missed."""
    dt = CPI
    t = np.arange(0, 8.0, dt)
    tf = np.arange(0, 8.0, 1e-3)
    vf = np.where(tf < 3.5, 1.2, np.where(tf > 4.5, -1.2, 1.2 * np.cos(np.pi * (tf - 3.5))))
    Rt = np.interp(t, tf, 2.0 + np.cumsum(vf) * 1e-3)
    rng = np.random.default_rng(seed)
    z = np.round((Rt + rng.normal(0, 0.12, t.size)) / BIN) * BIN
    miss = rng.random(t.size) < 0.06
    miss[0] = False
    z[miss] = np.nan
    return t, Rt, z


def ab_pair(alpha):
    return alpha, alpha ** 2 / (2 - alpha)     # Benedict-Bordner


def numbers() -> dict:
    v = {}
    # the example targets' Doppler at 10.0 GHz
    v["walker_v"], v["limb_A"], v["stride"] = 1.1, 2.3, 0.9
    v["limb_max"] = v["walker_v"] + v["limb_A"]
    v["fd_torso"] = 2 * v["walker_v"] / LAM
    v["fd_limb"] = 2 * v["limb_max"] / LAM
    v["fs_slow"] = 1 / PRI
    v["fmax"] = 1 / (2 * PRI)
    v["vmax"] = LAM / (4 * PRI)
    v["dv"] = LAM / (2 * CPI)
    # rotors: tip speed pi D rpm / 60
    v["fan30_tip"] = np.pi * 0.30 * 1200 / 60
    v["fan_tip"] = np.pi * 0.25 * 700 / 60
    v["fan_fd"] = 2 * v["fan_tip"] / LAM
    v["spin_tip"] = np.pi * 0.06 * 1500 / 60
    v["spin_fd"] = 2 * v["spin_tip"] / LAM
    v["hand_v"] = 2 * np.pi * 1.2 * 0.15
    v["hand_fd"] = 2 * v["hand_v"] / LAM
    # the band's shape: a blade with its weight on its outer third, 2R/3 to R
    v["shape_mean_sq"] = (1 - (2 / 3) ** 3) / (3 * (1 / 3))
    v["shape_outer"] = np.sqrt(v["shape_mean_sq"] / 2)
    # a walker crosses a range bin in
    v["bin_cross_s"] = BIN / v["walker_v"]
    # window trade: limb acceleration, Doppler rate, best window
    v["limb_acc"] = 2 * np.pi * v["stride"] * v["limb_A"]
    v["fdot"] = 2 * v["limb_acc"] / LAM
    v["Tw_best_ms"] = 1e3 / np.sqrt(v["fdot"])
    v["Tw_best_chirps"] = v["Tw_best_ms"] / (PRI * 1e3)
    for n in (16, 64, 128, 256):
        v[f"Tw_{n}"] = n * PRI * 1e3
        v[f"df_{n}"] = 1 / (n * PRI)
        v[f"smear_{n}"] = v["fdot"] * n * PRI
    v["dv_64"] = LAM * v["df_64"] / 2
    # the fan's tip acceleration: no window resolves it
    om = 2 * np.pi * 700 / 60
    v["fan_acc"] = om ** 2 * 0.125
    v["fan_fdot"] = 2 * v["fan_acc"] / LAM
    v["fan_Tw_ms"] = 1e3 / np.sqrt(v["fan_fdot"])
    v["fan_df"] = 1e3 / v["fan_Tw_ms"]
    v["fan_flashes"] = 2 * 3 * 700 / 60          # each blade across the line of sight twice a turn
    # classification
    Xtr, ytr, model, M = trials(31)
    v["M"] = M
    v["acc"] = np.trace(M) / M.sum()
    v["accs"] = [np.trace(trials(s)[3]) / 80 for s in range(31, 36)]
    v["Xtr"], v["ytr"], v["model"] = Xtr, ytr, model
    v["means"] = {k: Xtr[ytr == k].mean(0) for k in KINDS}
    # tracking
    t, Rt, z = walk_track()
    v["track"] = (t, Rt, z)
    v["meas_rms"] = np.sqrt(np.nanmean((z - Rt) ** 2))
    v["n_miss"] = int(np.isnan(z).sum())
    st = (t > 1.5) & ((t < 3.5) | (t > 5.5))
    turn = (t > 3.3) & (t < 5.5)
    v["turn_acc"] = np.pi * 1.2                  # the cosine turn's peak acceleration
    for a in ALPHAS:
        al, be = ab_pair(a)
        o = alpha_beta(z, al, be, CPI)
        e = o[:, 0] - Rt
        key = f"{a:.2f}"
        v[f"beta_{key}"] = be
        v[f"rms_{key}"] = np.sqrt(np.mean(e[st] ** 2))
        v[f"turn_{key}"] = np.abs(e[turn]).max()
        v[f"ratio_{key}"] = np.sqrt((2 * al ** 2 + 2 * be - 3 * al * be) / (al * (4 - 2 * al - be)))
        v[f"lag_{key}"] = v["turn_acc"] * CPI ** 2 / be
    # angle: the array at 10 GHz, monopulse, and a crossing walker
    v["bw_deg"] = np.degrees(0.886 * LAM / (8 * 0.014))
    v["mono_deg"] = np.degrees(np.arcsin(LAM / (2 * 0.056)))
    v["kD_deg"] = 360 * 0.056 / LAM
    v["cross_rate"] = np.degrees(1.0 / 4.0)
    v["per_sweep"] = v["cross_rate"] / 0.9
    v["per_cpi"] = v["cross_rate"] * CPI
    # radial speed on a diagonal: from P to Q at 1.2 m/s, (x to the side, y out)
    P, Q = np.array(DIAG_P), np.array(DIAG_Q)
    u = (Q - P) / np.hypot(*(Q - P))
    v["diag_P_r"], v["diag_P_az"] = np.hypot(*P), np.degrees(np.arctan2(P[0], P[1]))
    v["diag_Q_r"], v["diag_Q_az"] = np.hypot(*Q), np.degrees(np.arctan2(Q[0], Q[1]))
    v["diag_vr_P"] = -1.2 * u @ (P / np.hypot(*P))   # + closing
    v["diag_vr_Q"] = -1.2 * u @ (Q / np.hypot(*Q))
    return v


ALPHAS = (0.15, 0.4)
DIAG_P, DIAG_Q = (0.4, 1.8), (-0.9, 3.4)


def check_numbers(v: dict) -> None:
    """The values the page prints: see main()'s printout; asserted by CHECK."""
    assert v["M"].tolist() == [[20, 0, 0, 0], [0, 16, 2, 2], [0, 12, 8, 0], [0, 0, 0, 20]], v["M"]
    assert f"{min(v['accs']):.2f}" == "0.80" and f"{max(v['accs']):.2f}" == "0.84", v["accs"]
    m = v["means"]
    assert (f"{m['walker'][0]:.2f}", f"{m['fan'][1]:.1f}", f"{m['spinner'][1]:.1f}") == ("0.78", "4.7", "3.6"), m
    assert m["hand"][1] < 1.0 and v["n_miss"] == 5 and len(v["track"][0]) == 79
    for name, want in CHECK.items():
        got = v[name]
        assert f"{got:{want[1]}}" == want[0], (name, f"{got:{want[1]}}", want[0])


CHECK = {
    "fd_torso": ("73", ".0f"), "limb_max": ("3.4", ".1f"), "fd_limb": ("227", ".0f"),
    "fs_slow": ("2500", ".0f"), "vmax": ("18.75", ".2f"), "fan30_tip": ("18.8", ".1f"),
    "fan_tip": ("9.2", ".1f"), "fan_fd": ("611", ".0f"), "spin_tip": ("4.7", ".1f"),
    "spin_fd": ("314", ".0f"), "hand_v": ("1.1", ".1f"), "hand_fd": ("75", ".0f"),
    "bin_cross_s": ("0.34", ".2f"), "limb_acc": ("13.0", ".1f"), "fdot": ("867", ".0f"),
    "Tw_best_ms": ("34", ".0f"), "Tw_best_chirps": ("85", ".0f"),
    "df_16": ("156", ".0f"), "smear_16": ("6", ".0f"), "df_64": ("39", ".0f"), "smear_64": ("22", ".0f"),
    "df_128": ("20", ".0f"), "smear_128": ("44", ".0f"), "df_256": ("9.8", ".1f"), "smear_256": ("89", ".0f"),
    "dv_64": ("0.59", ".2f"), "fan_acc": ("672", ".0f"), "fan_Tw_ms": ("4.7", ".1f"),
    "fan_df": ("212", ".0f"), "fan_flashes": ("70", ".0f"),
    "shape_mean_sq": ("0.704", ".3f"), "shape_outer": ("0.59", ".2f"),
    "acc": ("0.80", ".2f"), "meas_rms": ("0.15", ".2f"),
    "beta_0.40": ("0.100", ".3f"), "ratio_0.40": ("0.57", ".2f"), "lag_0.40": ("0.40", ".2f"),
    "rms_0.40": ("0.12", ".2f"), "turn_0.40": ("0.23", ".2f"), "turn_0.15": ("0.9", ".1f"),
    "bw_deg": ("13.6", ".1f"), "mono_deg": ("15.5", ".1f"), "kD_deg": ("672", ".0f"),
    "cross_rate": ("14.3", ".1f"), "per_sweep": ("15.9", ".1f"), "per_cpi": ("1.5", ".1f"),
    "diag_P_r": ("1.84", ".2f"), "diag_P_az": ("12.5", ".1f"), "diag_vr_P": ("-0.75", ".2f"),
    "diag_Q_r": ("3.52", ".2f"), "diag_Q_az": ("-14.8", ".1f"), "diag_vr_Q": ("-1.09", ".2f"),
}


# ---------------------------------------------------------------- figures --

def fig_signatures() -> None:
    """The lesson's four example targets, 3 s each, 64-chirp window. Each panel
    has its own Doppler span, so the walker's off-zero torso line shows; the
    right axis gives the same scale in m/s, the unit of the app's view."""
    rng = np.random.default_rng(310)
    fig, axs = plt.subplots(2, 2, figsize=(4.9, 3.9), sharex=True)
    span = {"walker": 300, "hand": 300, "fan": 800, "spinner": 800}
    ticks = {300: ([-200, 0, 200], [-3, 0, 3]), 800: ([-500, 0, 500], [-8, 0, 8])}
    for ax, k in zip(axs.flat, KINDS):
        t, f, S = spectrogram(target(k, TYPICAL[k], 3.0, rng))
        # an embedded bitmap: a vector mesh of every cell would be megabytes
        ax.imshow(np.clip(S, -40, 0), origin="lower", aspect="auto", cmap="Blues",
                  extent=(t[0], t[-1], f[0], f[-1]), interpolation="bilinear")
        F = span[k]
        ax.text(0.12, 0.88 * F, k, color=COLORS[k], ha="left", va="top", fontweight="bold")
        if k == "walker":
            ft = 2 * TYPICAL[k]["v0"] / LAM
            ax.axhline(ft, color=RED, lw=1.0, ls="--")
            ax.text(2.92, ft + 12, "torso", color=RED, ha="right", va="bottom", fontsize=13)
        ax.set_xlim(0, 3)
        ax.set_ylim(-F, F)
        ax.set_xticks([1, 2])
        ax.set_yticks(ticks[F][0])
        style(ax)
        sec = ax.secondary_yaxis("right", functions=(lambda x: x * LAM / 2, lambda vv: 2 * vv / LAM))
        sec.set_yticks(ticks[F][1])
        sec.tick_params(colors=GRAY, labelsize=13)
    for ax in axs[1]:
        ax.set_xlabel("time (s)")
    for ax in axs[:, 0]:
        ax.set_ylabel("Hz")
    for ax in axs[:, 1]:
        ax.text(1.32, 0.5, "m/s", rotation=90, va="center", ha="center", transform=ax.transAxes, fontsize=13)
    fig.subplots_adjust(wspace=0.62, hspace=0.14)
    finalize(fig, "L31-signatures")


def fig_features(v: dict) -> None:
    """Two views of the training trials: centroid against spread, where the
    walkers stand apart, and periodicity against spread, where the hands do."""
    X, y = v["Xtr"], v["ytr"]
    fig, axs = plt.subplots(1, 2, figsize=(5.6, 3.0))
    for ax, (i, xl) in zip(axs, ((0, "centroid (m/s)"), (2, "periodicity"))):
        for k in KINDS:
            m = y == k
            ax.scatter(X[m, i], X[m, 1], s=18, marker=MARKERS[k], facecolor="none",
                       edgecolor=COLORS[k], linewidth=1.0, label=k)
            mu = v["means"][k]
            ax.scatter([mu[i]], [mu[1]], s=90, marker="X", color=COLORS[k], edgecolor="white", linewidth=0.8)
        ax.set_xlabel(xl)
        ax.set_ylim(0, 7.5)
        ax.set_yticks([0, 2, 4, 6])
        ax.set_xticks([0, 0.5, 1.0])
        style(ax)
    axs[0].set_xlim(-0.05, 1.4)
    axs[0].set_ylabel("spread (m/s)")
    axs[1].set_xlim(-0.05, 1.05)
    axs[1].set_yticklabels([])
    axs[0].legend(loc="upper right", fontsize=13, handletextpad=0.2, borderaxespad=0.1, labelspacing=0.25)
    fig.subplots_adjust(wspace=0.08)
    finalize(fig, "L31-features")


def fig_alpha_beta(v: dict) -> None:
    t, Rt, z = v["track"]
    fig, ax = plt.subplots(figsize=(4.4, 2.8))
    ax.plot(t, Rt, color=GRAY, lw=1.0, ls="--", label="truth")
    ax.plot(t, z, ls="none", marker="o", ms=3.2, mfc="none", mec=INK, mew=0.8, label="detections")
    for a, col in zip(ALPHAS, (AMBER, BLUE)):
        o = alpha_beta(z, *ab_pair(a), CPI)
        ax.plot(t, o[:, 0], color=col, lw=1.6, label=f"α = {a:g}")
    ax.set_xlim(0, 8)
    ax.set_ylim(1.5, 9.5)
    ax.set_xticks([0, 2, 4, 6, 8])
    ax.set_yticks([2, 4, 6])
    ax.set_xlabel("time (s)")
    ax.set_ylabel("range (m)")
    ax.legend(loc="upper left", fontsize=13, ncol=2, handlelength=1.2, columnspacing=0.8,
              handletextpad=0.3, borderaxespad=0.1)
    style(ax)
    finalize(fig, "L31-alpha-beta")


def main() -> None:
    v = numbers()
    for k, x in v.items():
        if isinstance(x, float):
            print(f"   {k:14s} {x:.6g}")
    print("   confusion\n", v["M"], "\n   accuracies", v["accs"])
    for k in KINDS:
        print(f"   mean {k:8s}", np.round(v["means"][k], 2))
    check_numbers(v)
    fig_signatures()
    fig_features(v)
    fig_alpha_beta(v)


if __name__ == "__main__":
    main()
