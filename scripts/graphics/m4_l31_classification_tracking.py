#!/usr/bin/env python3
"""Generate the L31 (Classification and Tracking) figures as inline SVG.

  - L31-signatures    : slow-time spectrograms of the four lab targets, a
                        walker, a fan, a fidget spinner, and a waving hand
  - L31-features      : the training trials in the centroid-spread plane,
                        with each class's mean
  - L31-alpha-beta    : range detections of a walker who walks out, turns,
                        and walks back, and two alpha-beta tracks of them

The lesson page shows all three from book/extras/viz/img/. None carries an
equation: symbols, numbers, and short words only.

The targets are simulated in slow time, one complex sample per chirp at the
L29-L31 burst's PRI of 0.5 ms (COURSE_SPEC M8), each as a few point
scatterers whose range changes with time; the radar's 10 GHz carrier turns
each one's range into a phase 4 pi R / lambda. spectrogram(), features(),
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
F0 = 10.0e9                  # COURSE_SPEC M8
LAM = C / F0                 # 3.0 cm
PRI = 0.5e-3                 # one slow-time sample per chirp
CPI = 256 * PRI              # one range-Doppler frame, 128 ms
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
        p.update(R=0.075, rpm=rng.uniform(700, 1200))
    elif kind == "spinner":
        p.update(R=0.035, rpm=rng.uniform(600, 1500))
    else:
        ca = rng.uniform(0.5, 1.0)
        p.update(A=rng.uniform(0.1, 0.3) * ca, f=rng.uniform(0.8, 2.0))
    return p


# The four signatures as the figure shows them: L26's walker, a 15 cm desk
# fan at 1000 rpm, a 7 cm spinner at 1200 rpm, a hand waving 0.2 m at 1.5 Hz.
TYPICAL = {
    "walker": dict(v0=1.3, fst=1.0, A=2.7, ph=0.0, snr_db=15),
    "fan": dict(R=0.075, rpm=1000, ph=0.0, snr_db=15),
    "spinner": dict(R=0.035, rpm=1200, ph=0.0, snr_db=15),
    "hand": dict(A=0.2, f=1.5, ph=0.0, snr_db=15),
}


# -------------------------------------------------- the radar_lab functions --

def spectrogram(x, pri=PRI, n_win=64, hop=16):
    """Slow-time spectrogram of one range bin: (t, f_D, S_dB), peak at 0 dB.

    On the page this takes (cap, range_bin) and pulls x from the cadet's
    range_fft; here x is the bin's samples directly."""
    x = x - x.mean()                           # stationary returns out
    w = np.hanning(n_win)
    cols = [np.fft.fftshift(np.fft.fft(x[i:i + n_win] * w))
            for i in range(0, len(x) - n_win, hop)]
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


def walk_track(seed: int = 31):
    """Out at 1.2 m/s from 2 m, a 1 s turn at 3.5 s, back at 1.2 m/s.

    One detection per 128 ms frame, at the center of the 0.30 m range bin the
    walker's detection falls in (a 0.10 m body jitter first), and 6% of frames
    missed."""
    dt = CPI
    t = np.arange(0, 8.0, dt)
    tf = np.arange(0, 8.0, 1e-3)
    vf = np.where(tf < 3.5, 1.2, np.where(tf > 4.5, -1.2, 1.2 * np.cos(np.pi * (tf - 3.5))))
    Rt = np.interp(t, tf, 2.0 + np.cumsum(vf) * 1e-3)
    rng = np.random.default_rng(seed)
    z = np.round((Rt + rng.normal(0, 0.10, t.size)) / 0.30) * 0.30
    miss = rng.random(t.size) < 0.06
    miss[0] = False
    z[miss] = np.nan
    return t, Rt, z


def ab_pair(alpha):
    return alpha, alpha ** 2 / (2 - alpha)     # Benedict-Bordner


def numbers() -> dict:
    v = {}
    v["fd_torso"] = 2 * 1.3 / LAM
    v["fd_limb"] = 2 * 4.0 / LAM
    v["fs_slow"] = 1 / PRI
    v["vmax"] = LAM / (4 * PRI)
    # rotors: tip speed pi D rpm / 60
    v["fan30_tip"] = np.pi * 0.30 * 1200 / 60
    v["fan15_tip"] = np.pi * 0.15 * 1000 / 60
    v["fan15_fd"] = 2 * v["fan15_tip"] / LAM
    v["spin_tip"] = np.pi * 0.07 * 1200 / 60
    v["spin_fd"] = 2 * v["spin_tip"] / LAM
    v["hand_v"] = 2 * np.pi * 1.5 * 0.2
    v["hand_fd"] = 2 * v["hand_v"] / LAM
    # a walker crosses a 0.30 m range bin in
    v["bin_cross_s"] = 0.30 / 1.3
    # window trade: limb acceleration, Doppler rate, best window
    v["limb_acc"] = 2 * np.pi * 1.0 * 2.7
    v["fdot"] = 2 * v["limb_acc"] / LAM
    v["Tw_best_ms"] = 1e3 / np.sqrt(v["fdot"])
    v["Tw_best_chirps"] = v["Tw_best_ms"] / (PRI * 1e3)
    v["df_64"] = 1 / (64 * PRI)
    v["dv_64"] = LAM * v["df_64"] / 2
    v["smear_64"] = v["fdot"] * 64 * PRI
    v["df_16"] = 1 / (16 * PRI)
    v["smear_256"] = v["fdot"] * 256 * PRI
    v["df_256"] = 1 / (256 * PRI)
    # the fan's tip acceleration: no window resolves it
    om = 2 * np.pi * 1000 / 60
    v["fan_fdot"] = 2 * om ** 2 * 0.075 / LAM
    v["fan_Tw_ms"] = 1e3 / np.sqrt(v["fan_fdot"])
    v["fan_acc"] = om ** 2 * 0.075
    v["fan_df"] = 1e3 / v["fan_Tw_ms"]
    v["fan_flashes"] = 2 * 3 * 1000 / 60          # each blade across the line of sight twice a turn
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
    for a in (0.2, 0.5, 0.8):
        al, be = ab_pair(a)
        o = alpha_beta(z, al, be, CPI)
        e = o[:, 0] - Rt
        key = f"{a:.1f}"
        v[f"beta_{key}"] = be
        v[f"rms_{key}"] = np.sqrt(np.mean(e[st] ** 2))
        v[f"turn_{key}"] = np.abs(e[turn]).max()
        v[f"ratio_{key}"] = np.sqrt((2 * al ** 2 + 2 * be - 3 * al * be) / (al * (4 - 2 * al - be)))
    # angle: the array at 10 GHz, monopulse, and a crossing walker
    v["bw_deg"] = np.degrees(0.886 * LAM / (8 * 0.014))
    v["mono_deg"] = np.degrees(np.arcsin(LAM / (2 * 0.056)))
    v["kD_deg"] = 360 * 0.056 / LAM
    v["cross_rate"] = np.degrees(1.0 / 4.0)
    v["per_sweep"] = v["cross_rate"] / 0.9
    v["per_cpi"] = v["cross_rate"] * CPI
    return v


def check_numbers(v: dict) -> None:
    """The values the page prints."""
    assert f"{v['fd_torso']:.0f}" == "87" and f"{v['fd_limb']:.0f}" == "267"
    assert f"{v['fs_slow']:.0f}" == "2000" and f"{v['vmax']:.0f}" == "15"
    assert f"{v['fan30_tip']:.1f}" == "18.8"
    assert f"{v['fan15_tip']:.1f}" == "7.9" and f"{v['fan15_fd']:.0f}" == "524"
    assert f"{v['spin_tip']:.1f}" == "4.4" and f"{v['spin_fd']:.0f}" == "293"
    assert f"{v['hand_v']:.1f}" == "1.9" and f"{v['hand_fd']:.0f}" == "126"
    assert f"{v['bin_cross_s']:.2f}" == "0.23"
    assert f"{v['limb_acc']:.0f}" == "17" and f"{v['fdot']:.0f}" == "1131"
    assert f"{v['Tw_best_ms']:.0f}" == "30" and f"{v['Tw_best_chirps']:.0f}" == "59"
    assert f"{v['df_64']:.0f}" == "31" and f"{v['dv_64']:.2f}" == "0.47"
    assert f"{v['smear_64']:.0f}" == "36"
    assert f"{v['df_16']:.0f}" == "125" and f"{v['smear_256']:.0f}" == "145"
    assert f"{v['df_256']:.1f}" == "7.8"
    assert f"{v['fan_fdot'] / 1e3:.0f}" == "55" and f"{v['fan_Tw_ms']:.1f}" == "4.3"
    assert f"{v['fan_acc']:.0f}" == "822" and f"{v['fan_df']:.0f}" == "234"
    assert f"{v['fan_Tw_ms'] / (PRI * 1e3):.0f}" == "9" and f"{v['fan_flashes']:.0f}" == "100"
    m = {k: np.round(x, 2).tolist() for k, x in v["means"].items()}
    assert m["walker"][0] == 0.71 and m["hand"][1] == 0.65, m
    assert f"{v['means']['fan'][1]:.1f}" == "4.9" and f"{v['means']['spinner'][1]:.1f}" == "3.7", m
    assert len(v["track"][0]) == 63
    assert v["M"].tolist() == [[20, 0, 0, 0], [0, 14, 6, 0], [0, 7, 13, 0], [0, 0, 0, 20]], v["M"]
    assert np.trace(v["M"]) == 67 and f"{v['acc'] * 100:.0f}" == "84"
    assert f"{min(v['accs']) * 100:.0f}" == "80" and f"{max(v['accs']) * 100:.0f}" == "91", v["accs"]
    assert v["n_miss"] == 5 and f"{v['meas_rms']:.2f}" == "0.10"
    assert f"{v['beta_0.5']:.3f}" == "0.167" and f"{v['beta_0.2']:.3f}" == "0.022"
    assert f"{v['rms_0.5']:.2f}" == "0.08" and f"{v['turn_0.5']:.2f}" == "0.31"
    assert f"{v['turn_0.2']:.1f}" == "1.2" and f"{v['rms_0.2']:.2f}" == "0.33"
    assert f"{v['ratio_0.5']:.2f}" == "0.64"
    assert f"{v['bw_deg']:.1f}" == "13.6" and f"{v['mono_deg']:.1f}" == "15.5"
    assert f"{v['kD_deg']:.0f}" == "672"
    assert f"{v['cross_rate']:.1f}" == "14.3" and f"{v['per_sweep']:.1f}" == "15.9"
    assert f"{v['per_cpi']:.1f}" == "1.8"


# ---------------------------------------------------------------- figures --

def fig_signatures() -> None:
    """The four targets, 3 s each, 64-chirp window, as the lab records them."""
    rng = np.random.default_rng(310)
    fig, axs = plt.subplots(2, 2, figsize=(4.6, 3.7), sharex=True, sharey=True)
    for ax, k in zip(axs.flat, KINDS):
        t, f, S = spectrogram(target(k, TYPICAL[k], 3.0, rng))
        # an embedded bitmap: a vector mesh of every cell would be megabytes
        ax.imshow(np.clip(S, -40, 0), origin="lower", aspect="auto", cmap="Blues",
                  extent=(t[0], t[-1], f[0], f[-1]), interpolation="bilinear")
        ax.text(0.12, 520, k, color=COLORS[k], ha="left", va="top", fontweight="bold")
        ax.set_xlim(0, 3)
        ax.set_ylim(-600, 600)
        ax.set_xticks([1, 2])
        ax.set_yticks([-500, 0, 500])
        style(ax)
    for ax in axs[1]:
        ax.set_xlabel("time (s)")
    for ax in axs[:, 0]:
        ax.set_ylabel("Doppler (Hz)")
    fig.subplots_adjust(wspace=0.1, hspace=0.14)
    finalize(fig, "L31-signatures")


def fig_features(v: dict) -> None:
    X, y = v["Xtr"], v["ytr"]
    fig, ax = plt.subplots(figsize=(4.4, 3.0))
    for k in KINDS:
        m = y == k
        ax.scatter(X[m, 0], X[m, 1], s=22, marker=MARKERS[k], facecolor="none",
                   edgecolor=COLORS[k], linewidth=1.1, label=k)
        mu = v["means"][k]
        ax.scatter([mu[0]], [mu[1]], s=110, marker="X", color=COLORS[k], edgecolor="white", linewidth=0.8)
    ax.set_xlim(-0.05, 1.4)
    ax.set_ylim(0, 7.2)
    ax.set_xticks([0, 0.5, 1.0])
    ax.set_yticks([0, 2, 4, 6])
    ax.set_xlabel("centroid (m/s)")
    ax.set_ylabel("spread (m/s)")
    ax.legend(loc="upper right", fontsize=13, handletextpad=0.2, borderaxespad=0.1,
              labelspacing=0.25)
    style(ax)
    finalize(fig, "L31-features")


def fig_alpha_beta(v: dict) -> None:
    t, Rt, z = v["track"]
    fig, ax = plt.subplots(figsize=(4.4, 2.8))
    ax.plot(t, Rt, color=GRAY, lw=1.0, ls="--", label="truth")
    ax.plot(t, z, ls="none", marker="o", ms=3.2, mfc="none", mec=INK, mew=0.8, label="detections")
    for a, col in ((0.2, AMBER), (0.5, BLUE)):
        o = alpha_beta(z, *ab_pair(a), CPI)
        ax.plot(t, o[:, 0], color=col, lw=1.6, label=f"α = {a:.1f}")
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
