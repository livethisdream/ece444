#!/usr/bin/env python3
"""Check the provided radar_lab.py against fmcw_sim.py captures, function by function.

    python3 scripts/radar/test_radar_lab.py

Each check builds a capture with a known answer (a target's range, velocity,
or angle; a clutter edge; a walker against a hand) and asserts the chain
recovers it. Runs in about half a minute; no files are written.
"""

import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts/radar"))
sys.path.insert(0, str(ROOT / "book/extras/notebooks"))
import fmcw_sim as sim                          # noqa: E402
import radar_lab as rl                          # noqa: E402

DATA = ROOT / "book/extras/radar-data"
LAM = rl.C / 10e9


def as_capture(cap):
    """A simulator capture as load_capture would return it."""
    out = {k: cap[k] for k in ("fs", "fc", "B", "T_ramp", "PRI", "f0")}
    out["iq"], out["iq_ch"] = sim.iq(cap), cap["iq_ch"]
    return out


def peak(x, y, lo, hi):
    m = (x >= lo) & (x <= hi)
    return x[m][np.argmax(y[m])], y[m].max()


def check(name, ok, detail):
    print(f"  {'PASS' if ok else 'FAIL'}  {name}: {detail}")
    return ok


def l28():
    ok = True
    for r0 in (1, 2, 3):
        cap = rl.load_capture(DATA / f"L28_corner_{r0}m.npz")
        r, p = rl.range_profile(cap, n_fft=4096)
        rp, _ = peak(r, p, 0.5, 5)
        ok &= check(f"range_profile, corner at {r0} m", abs(rp - r0) < 0.05, f"peak at {rp:.3f} m")
    cap = rl.load_capture(DATA / "L28_corner_2m.npz")
    ok &= check("range_axis default length", rl.range_axis(cap).size == cap["iq"].shape[1],
                f"{rl.range_axis(cap).size} bins")
    X = rl.range_fft(cap)
    ok &= check("range_fft shape", X.shape == cap["iq"].shape, str(X.shape))
    tone = {**cap, "iq": np.exp(2j * np.pi * cap["f0"] * np.arange(300) / cap["fs"])[None, :]}
    for w in ("hann", None):
        lvl = 20 * np.log10(np.abs(rl.range_fft(tone, w, 4096)).max())
        ok &= check(f"unit tone reads 0 dBFS, window {w}", abs(lvl) < 0.05, f"{lvl:.3f} dB")
    r, t, W = rl.waterfall(rl.load_capture(DATA / "L28_walker.npz"))
    track = r[np.argmax(np.where((r > 0.5) & (r < 5), W, -300), axis=1)]
    ok &= check("waterfall walker reaches 4 m", 3.7 < track.max() < 4.3, f"max {track.max():.2f} m")
    return ok


def burst(**kw):
    return sim.new_capture("l29_burst", fs=1.0e6, **kw)    # 300 samples a chirp keeps it small


def l29():
    ok = True
    cap = burst()
    sim.add_noise(cap)
    sim.add_leakage(cap)
    sim.add_point(cap, 5.0, rcs=2.0)                     # wall
    sim.add_point(cap, 2.0, v=+1.0, rcs=0.47)            # closing at 1 m/s
    sim.add_point(cap, 3.5, v=-0.6, rcs=0.47, phase0=1)  # opening at 0.6 m/s
    cap = as_capture(cap)
    rd, rng, vel = rl.range_doppler(cap)
    ok &= check("range_doppler shape [range, velocity]", rd.shape == (rng.size, vel.size), str(rd.shape))
    dv = vel[1] - vel[0]
    ok &= check("velocity resolution", abs(dv - 0.117) < 0.002, f"{dv:.4f} m/s")
    for r0, v0 in ((2.0, 1.0), (3.5, -0.6)):
        m = (np.abs(rng - r0) < 0.5)[:, None] & (np.abs(vel) > 0.2)[None, :]
        i, j = np.unravel_index(np.argmax(np.where(m, rd, -300)), rd.shape)
        ok &= check(f"target at {r0} m, {v0:+} m/s", abs(rng[i] - r0) < 0.4 and abs(vel[j] - v0) < 0.15,
                    f"found {rng[i]:.2f} m, {vel[j]:+.2f} m/s")
    j0 = np.argmin(np.abs(vel))
    iw = np.argmin(np.abs(rng - 5.0))
    # The canceller's response at Doppler f_D is |2 sin(pi f_D PRI)| per stage,
    # so a slow mover loses a predictable amount: 13.6 dB a stage at 1 m/s.
    stage = -20 * np.log10(2 * np.sin(np.pi * (2 * 1.0 / LAM) * cap["PRI"]))
    for kind, n in (("2pulse", 1), ("3pulse", 2)):
        rd2, rng2, vel2 = rl.range_doppler(rl.mti(cap, kind))
        drop = rd[iw, j0] - rd2[iw, np.argmin(np.abs(vel2))]
        m = (np.abs(rng2 - 2.0) < 0.5)[:, None] & (np.abs(vel2 - 1.0) < 0.3)[None, :]
        keep = rd[np.ix_(np.abs(rng - 2.0) < 0.5, np.abs(vel - 1.0) < 0.3)].max() - np.where(m, rd2, -300).max()
        ok &= check(f"mti {kind}: wall cancelled, mover down as predicted", drop > 60 and abs(keep - n * stage) < 1.5,
                    f"wall down {drop:.0f} dB, mover down {keep:.1f} dB, predicted {n * stage:.1f}")
    ok &= check("mti keeps iq_ch in step", rl.mti(cap, "3pulse")["iq_ch"].shape[1] == cap["iq"].shape[0] - 2, "")
    return ok


def l30():
    ok = True
    rng = np.random.default_rng(5)
    n_r, n_v = 300, 256
    P = rng.exponential(1.0, (n_r, n_v))
    N = (2 * 6 + 1) * (2 * 6 + 1) - (2 * 2 + 1) * (2 * 2 + 1)
    pfa = 1e-3
    alpha = N * (pfa ** (-1 / N) - 1)
    det, _ = rl.cfar_2d(10 * np.log10(P), (2, 2), (4, 4), 10 * np.log10(alpha))
    meas = det.mean()
    ok &= check("ca false-alarm rate near design", pfa / 2.5 < meas < pfa * 2.5, f"{meas:.1e} for {pfa:.0e}")
    P2 = P.copy()
    P2[150:, :] *= 100                              # 20 dB clutter step at range cell 150
    P2[100, 40] = 400                               # a target 26 dB up, short of the step
    d_ca, hits = rl.cfar_2d(10 * np.log10(P2), 2, 4, 13, axes=(np.arange(n_r) * 0.3, np.arange(n_v)))
    d_go, _ = rl.cfar_2d(10 * np.log10(P2), 2, 4, 13, method="go")
    d_so, _ = rl.cfar_2d(10 * np.log10(P2), 2, 4, 13, method="so")
    edge = slice(146, 156)
    fa = [d[edge].sum() for d in (d_ca, d_go, d_so)]
    ok &= check("go fewest, so most false alarms at a clutter edge", fa[1] <= fa[0] <= fa[2] and fa[1] < fa[2],
                f"ca {fa[0]}, go {fa[1]}, so {fa[2]}")
    hit = [h for h in hits if abs(h[0] - 30.0) < 1e-9 and h[1] == 40]
    ok &= check("target in the hit list, with axes", len(hit) == 1 and hit[0][2] > 20,
                f"{hit[0][2]:.1f} dB over its estimate" if hit else "missing")
    return ok


def record(kind, seed):
    """A 4 s record at 0.5 ms a chirp of one target type."""
    cap = sim.new_capture("l29_burst", fs=1.0e6, n_chirps=8000)
    sim.add_noise(cap, seed=seed)
    sim.add_leakage(cap)
    if kind == "walker":
        sim.add_walker(cap, r_start=1.5, r_turn=3.5, speed=1.0 + 0.1 * (seed % 3), seed=seed)
    elif kind == "hand":
        sim.add_hand(cap, r0=1.0, swing=0.12 + 0.02 * (seed % 3), rate_hz=1.5 + 0.2 * (seed % 3))
    else:                                           # a steady mover: a cart, say
        sim.add_point(cap, 3.5, v=0.4 + 0.1 * (seed % 3), rcs=0.3, phase0=seed)
    return as_capture(cap)


def l31():
    ok = True
    X, y = [], []
    for kind in ("walker", "hand", "cart"):
        for seed in range(6):
            cap = record(kind, seed)
            r = rl.range_axis(cap)
            bins = np.nonzero((r > 0.5) & (r < 4.0))[0]
            t, f, S = rl.spectrogram(cap, slice(bins[0], bins[-1] + 1), n_win=128, hop=32)
            X.append(rl.features(t, f, S, LAM))
            y.append(kind)
    X, y = np.array(X), np.array(y)
    print("        mean features [centroid m/s, spread m/s, periodicity]:")
    for kind in ("walker", "hand", "cart"):
        print(f"          {kind:6s} {np.round(X[y == kind].mean(0), 2)}")
    train = np.arange(len(y)) % 2 == 0
    model = rl.train(X[train], y[train])
    pred = [rl.classify(x, model) for x in X[~train]]
    acc = np.mean(np.array(pred) == y[~train])
    cm = rl.confusion_matrix(y[~train], pred, ["walker", "hand", "cart"])
    ok &= check("nearest-centroid accuracy on held-out records", acc >= 0.8, f"{acc:.2f}; confusion {cm.tolist()}")
    rng = np.random.default_rng(2)
    dt, v0 = 0.128, 1.2
    truth = 2.0 + v0 * dt * np.arange(60)
    meas = truth + rng.normal(0, 0.15, truth.size)
    meas[[10, 25, 26]] = np.nan
    est = rl.alpha_beta(meas, 0.5, 0.2, dt)
    ok &= check("alpha_beta settles on the walker's speed", abs(est[-10:, 1].mean() - v0) < 0.15,
                f"{est[-10:, 1].mean():.2f} m/s for {v0}")
    # A steady mover crossing range bins keeps its slow-time level in a slice sum.
    cap = sim.new_capture("l29_burst", fs=1.0e6, n_chirps=4000)
    sim.add_noise(cap)
    sim.add_point(cap, 3.0, v=0.4, level_dbfs=-30.0)        # fixed level: only the sum moves it
    cap = as_capture(cap)
    r = rl.range_axis(cap)
    b = np.nonzero((r > 1.0) & (r < 4.0))[0]
    x = rl._sum_bins(rl.range_fft(cap), slice(b[0], b[-1] + 1))
    a_db = 20 * np.log10(np.abs(x))
    ok &= check("slice sum holds a mover's level across bins", a_db.max() - a_db.min() < 3,
                f"{a_db.max() - a_db.min():.2f} dB swing over {0.4 * 2:.1f} m")
    for az in (+8.0, -5.0):
        cap = burst(n_chirps=16)
        sim.add_noise(cap)
        sim.add_point(cap, 2.5, rcs=0.47, az=az)
        cap = as_capture(cap)
        rb = np.argmin(np.abs(rl.range_axis(cap) - 2.5))
        ang = np.median(rl.monopulse_angle(cap, rb))
        ok &= check(f"monopulse_angle at {az:+} deg", abs(ang - az) < 0.3, f"{ang:+.2f} deg")
    return ok


if __name__ == "__main__":
    results = []
    for name, fn in (("L28", l28), ("L29", l29), ("L30", l30), ("L31", l31)):
        print(name)
        results.append(fn())
    print("all checks pass" if all(results) else "SOME CHECKS FAILED")
    sys.exit(0 if all(results) else 1)
