#!/usr/bin/env python3
"""The L31 Lab's recorded data: target records to classify, and a walk to track.

Built only from scripts/radar/fmcw_sim.py: its existing functions, plus the
three target functions the L31 Lab added to it (add_rotor, add_fan,
add_dismount). Two kinds of file, both in the course's capture format:

  L31_<target>_<n>.npz   n = 1..4 for each of fan, spinner, hand, walker: a
                         2.0 s record of back-to-back chirps of the L29 burst
                         (300 us, PRI 0.5 ms, 500 MHz, 10 GHz), 4000 chirps,
                         iq only. To keep each file near 1.3 MB the samples
                         of each chirp are thinned to 0.3 MSPS, 90 a chirp:
                         the range bins are still 0.30 m, and they reach
                         4.4 m instead of 171 m. Record 1 of each target is
                         the lesson's example of it (L31, Four Signatures);
                         records 2-4 change the speed, the size, the range,
                         and how the target is held. The note says which.
  L31_dismount.npz       a person walking a diagonal from A (1.5 m, 12 deg to
                         the E1 side) out to B (4.0 m, 10 deg to the E8 side),
                         turning, and walking back: iq and iq_ch, and the
                         truth (truth_t, truth_r, truth_az at the center of
                         each 128 ms frame). Every 8th chirp is kept, PRI 4 ms,
                         so a 128 ms frame is 32 chirps: the burst's velocity
                         cell of 0.12 m/s, with +/-1.9 m/s unambiguous.

Every file's iq is rounded to a 12-bit converter's steps (2^-11 of full
scale), as a capture's samples are, and saved compressed.

    python3 scripts/radar/make_l31_data.py           # write the files
    python3 scripts/radar/make_l31_data.py --check   # and assert the numbers the
                                                     # page, notebook, and packet quote
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(ROOT / "book/extras/notebooks"))
import fmcw_sim as sim                          # noqa: E402

OUT = ROOT / "book/extras/radar-data"
LSB = 2.0 ** -11                                # a 12-bit converter's step, full scale 1
FS_REC, T_REC = 0.3e6, 2.0                      # the records: 90 samples a chirp, 2.0 s
PRI_TRK, FRAME = 4.0e-3, 0.128                  # the walk: every 8th chirp, 128 ms frames
KINDS = ["walker", "fan", "spinner", "hand"]

# The records. Fans are 15 cm across, spinners 7 cm (arms at 28 and 35 mm),
# both edge-on unless tilted; tilt is degrees off edge-on. Hands swing A m
# at f Hz. Walkers: (x0, y0) m start, speed m/s along heading deg off
# boresight, positive heading toward the E8 side, negative speed toward the kit.
RECORDS = {
    "fan": [dict(r0=1.0, rpm=1000, tilt=0), dict(r0=1.2, rpm=1200, tilt=20),
            dict(r0=0.8, rpm=800, tilt=45), dict(r0=1.3, rpm=900, tilt=30)],
    "spinner": [dict(r0=0.5, rpm=1200, tilt=0), dict(r0=0.6, rpm=1500, tilt=0),
                dict(r0=0.4, rpm=1000, tilt=20), dict(r0=0.7, rpm=1300, tilt=30)],
    "hand": [dict(r0=0.8, A=0.20, f=1.5), dict(r0=1.0, A=0.25, f=1.0),
             dict(r0=0.6, A=0.10, f=2.0), dict(r0=1.2, A=0.30, f=0.8)],
    "walker": [dict(x0=0.0, y0=4.0, v=-1.3, hd=0, fst=1.0),
               dict(x0=0.3, y0=1.2, v=0.8, hd=15, fst=1.05),
               dict(x0=-0.2, y0=3.9, v=-0.75, hd=5, fst=0.95),
               dict(x0=0.0, y0=1.3, v=0.95, hd=-10, fst=1.1)],
}

# The walk: A and B as (range m, azimuth deg), 1.0 m/s, a 1 s turn at B.
WALK_A, WALK_B, WALK_V = (1.5, -12.0), (4.0, 10.0), 1.0
CHAIR = dict(r0=3.2, rcs=0.5, az=25.0, phase0=0.3)    # furniture beside the path


def _xy(r, az):
    return np.array([r * np.sin(np.radians(az)), r * np.cos(np.radians(az))])


def walk_path():
    """The dismount's torso: (t, x, y) on a 1 ms grid, and the walk's length in s.

    Out from A toward B at WALK_V; the speed swings through zero over 1 s
    (as cos), so the walker turns at B; then back to A, where the record ends.
    """
    A, B = _xy(*WALK_A), _xy(*WALK_B)
    L = np.hypot(*(B - A))
    u = (B - A) / L
    t1 = L - 1 / np.pi                           # the turn starts here, apex at B
    t_end = 2 * L + 1 - 2 / np.pi                # back at A
    t = np.arange(0.0, t_end + 0.3, 1e-3)
    v = np.where(t < t1, WALK_V, np.where(t < t1 + 1, WALK_V * np.cos(np.pi * (t - t1)), -WALK_V))
    s = np.cumsum(v) * 1e-3
    p = A[:, None] + s[None, :] * u[:, None]
    return t, p[0], p[1], t_end, t1


def _quantize(x):
    return (np.round(x.real / LSB) + 1j * np.round(x.imag / LSB)) * LSB


def _save(cap: dict, path: Path, note: str, channels: bool = False, **extra) -> Path:
    """The contract's .npz, compressed, with iq (and iq_ch) on 12-bit steps."""
    path.parent.mkdir(parents=True, exist_ok=True)
    ch = _quantize(cap["iq_ch"]).astype(np.complex64)
    more = dict(iq_ch=ch) if channels else {}
    iq = ch.sum(axis=0) if channels else _quantize(sim.iq(cap)).astype(np.complex64)
    np.savez_compressed(path, iq=iq, **more, fs=cap["fs"], fc=cap["fc"], B=cap["B"],
                        T_ramp=cap["T_ramp"], PRI=cap["PRI"], f0=cap["f0"],
                        note=np.str_(note), **extra)
    return path


def record(kind: str, p: dict, seed: int) -> dict:
    """One 2.0 s record of one target: the room's noise and leakage, and the target."""
    cap = sim.new_capture("l29_burst", fs=FS_REC, n_chirps=int(round(T_REC / 0.5e-3)))
    sim.add_noise(cap, seed=seed)
    sim.add_leakage(cap)
    if kind == "fan":
        sim.add_fan(cap, r0=p["r0"], radius=0.075, rpm=p["rpm"], tilt=p["tilt"], seed=seed)
    elif kind == "spinner":
        sim.add_rotor(cap, p["r0"], [0.028, 0.035], [7e-4, 1e-3], p["rpm"], n_blades=3,
                      spin_down_s=60.0, wobble=0.05, seed=seed, tilt=p["tilt"])
    elif kind == "hand":
        sim.add_hand(cap, r0=p["r0"], swing=p["A"], rate_hz=p["f"])
    else:
        t = np.array([0.0, T_REC + 0.2])
        d, h = p["v"] * (T_REC + 0.2), np.radians(p["hd"])
        x0, y0 = p["x0"], p["y0"]
        sim.add_dismount(cap, t, [x0, x0 + d * np.sin(h)], [y0, y0 + d * np.cos(h)],
                         stride_hz=p["fst"], seed=seed)
    return cap


def describe(kind: str, p: dict) -> str:
    if kind == "fan":
        tip = np.pi * 0.15 * p["rpm"] / 60
        held = "edge-on" if p["tilt"] == 0 else f"{p['tilt']} deg off edge-on"
        return (f"a 15 cm desk fan at {p['rpm']} rpm, {p['r0']:.1f} m out, held {held}: "
                f"tips {tip:.1f} m/s, {tip * np.cos(np.radians(p['tilt'])):.1f} m/s along the line of sight")
    if kind == "spinner":
        tip = np.pi * 0.07 * p["rpm"] / 60
        held = "edge-on" if p["tilt"] == 0 else f"{p['tilt']} deg off edge-on"
        return (f"a 7 cm fidget spinner at {p['rpm']} rpm, {p['r0']:.1f} m out, held {held}: "
                f"tips {tip:.1f} m/s, {tip * np.cos(np.radians(p['tilt'])):.1f} m/s along the line of sight")
    if kind == "hand":
        return (f"a hand waving {p['A']:.2f} m toward and away from the kit at {p['f']:.1f} Hz, "
                f"{p['r0']:.1f} m out: peak {2 * np.pi * p['f'] * p['A']:.1f} m/s")
    way = "toward" if p["v"] < 0 else "away from"
    return (f"a person walking {way} the kit at {abs(p['v']):.2f} m/s from {np.hypot(p['x0'], p['y0']):.1f} m, "
            f"{abs(p['hd'])} deg off the line of sight, {p['fst']:.2f} strides a second")


def l31_sets(out: Path = OUT) -> list[Path]:
    written = []
    for kind in KINDS:
        for n, p in enumerate(RECORDS[kind], start=1):
            seed = 3100 + 10 * KINDS.index(kind) + n
            cap = record(kind, p, seed)
            written.append(_save(cap, out / f"L31_{kind}_{n}.npz",
                                 f"L31 Lab recorded data: {describe(kind, p)}; 2.0 s of 300 us chirps "
                                 f"every 0.5 ms, thinned to 90 samples a chirp (0.3 MSPS)"))

    t, x, y, t_end, _ = walk_path()
    n_frames = int(t_end / FRAME)
    n_per = int(round(FRAME / PRI_TRK))
    cap = sim.new_capture("l29_burst", fs=FS_REC, PRI=PRI_TRK, n_chirps=n_frames * n_per)
    sim.add_noise(cap, seed=3150)
    sim.add_leakage(cap)
    sim.add_point(cap, **CHAIR)
    sim.add_dismount(cap, t, x, y, stride_hz=1.0, seed=3151)
    tf = (np.arange(n_frames) + 0.5) * FRAME
    xf, yf = np.interp(tf, t, x), np.interp(tf, t, y)
    written.append(_save(
        cap, out / "L31_dismount.npz",
        f"L31 Lab recorded data: a person walking from A ({WALK_A[0]:.1f} m, {-WALK_A[1]:.0f} deg to the E1 side) "
        f"to B ({WALK_B[0]:.1f} m, {WALK_B[1]:.0f} deg to the E8 side) at {WALK_V:.1f} m/s, turning, and back; "
        f"a chair at {CHAIR['r0']:.1f} m, {CHAIR['az']:.0f} deg; every 8th chirp (PRI 4 ms), "
        f"{n_frames} frames of 128 ms, both subarray channels; truth_t, truth_r, truth_az",
        channels=True, truth_t=tf, truth_r=np.hypot(xf, yf), truth_az=np.degrees(np.arctan2(xf, yf))))
    return written


# ---------------------------------------------------------------------------
# The notebook's own helpers: --check runs the helper cell of the shipped
# notebook, so the numbers it asserts are the ones the notebook prints.
NOTEBOOK = ROOT / "book/extras/notebooks/L31_classify_track.ipynb"


def notebook_helpers():
    import json
    import radar_lab as rl
    from scipy import ndimage
    from scipy.signal import peak_widths
    cells = json.loads(NOTEBOOK.read_text())["cells"]
    src = next("".join(c["source"]) for c in cells
               if c["cell_type"] == "code" and "".join(c["source"]).startswith("# Helpers used by the tasks"))
    ns = dict(np=np, rl=rl, ndimage=ndimage, peak_widths=peak_widths)
    exec(src, ns)
    return rl, ns


def check(out: Path = OUT) -> bool:
    """Recompute the numbers the L31 page, notebook, and packet quote, and assert them."""
    rl, h = notebook_helpers()
    ok = True

    def expect(name, got, want):
        nonlocal ok
        good = got == want
        ok &= good
        print(f"  {'PASS' if good else 'FAIL'}  {name}: {got}" + ("" if good else f", expected {want}"))

    sizes = {p.name: p.stat().st_size for p in out.glob("L31_*.npz")}
    expect("17 files, each under 5 MB, all under 25 MB",
           (len(sizes), max(sizes.values()) < 5e6, sum(sizes.values()) < 25e6), (17, True, True))
    print(f"        L31 total {sum(sizes.values()) / 1e6:.1f} MB")

    caps = {(k, n): rl.load_capture(out / f"L31_{k}_{n}.npz") for k in KINDS for n in range(1, 5)}
    lam = rl.C / 10e9

    # The Pre-Lab's predictions, record 1 of each target: largest speed, m/s.
    expect("pre-lab: fan, spinner, hand tips; walker torso and limbs, m/s",
           [round(np.pi * 0.15 * 1000 / 60, 1), round(np.pi * 0.07 * 1200 / 60, 1),
            round(2 * np.pi * 1.5 * 0.2, 1), 1.3, round(1.3 + 2.7, 1)],
           [7.9, 4.4, 1.9, 1.3, 4.0])
    speeds = (np.pi * 0.15 * 1000 / 60, np.pi * 0.07 * 1200 / 60, 2 * np.pi * 1.5 * 0.2, 1.3, 4.0)
    expect("pre-lab: the same as Doppler, Hz", [round(2 * v / lam) for v in speeds], [524, 293, 126, 87, 267])

    # Procedure A without a kit: each record 1's speeds in the max-hold view, 20 dB.
    got = []
    for k in KINDS:
        rd, rng, vel = h["max_hold"](caps[(k, 1)])
        prof = rd[(rng > 0.3) & (rng < 4.4)].max(axis=0)
        band = vel[prof > prof.max() - 20]
        got.append((k, round(float(band.min()), 1), round(float(band.max()), 1)))
    expect("procedure A, record 1 speeds within 20 dB, m/s",
           got, [("walker", -1.3, 3.9), ("fan", -8.6, 8.7), ("spinner", -4.9, 4.9), ("hand", -2.0, 2.0)])

    # Procedure B without a kit: three frames of the walk.
    walk = rl.load_capture(out / "L31_dismount.npz")
    n = int(round(FRAME / walk["PRI"]))
    nf = walk["iq"].shape[0] // n
    got = []
    for k in (1, nf // 2, nf - 3):
        sl = slice(k * n, (k + 1) * n)
        rd, rng, vel = rl.range_doppler(rl.mti({**walk, "iq": walk["iq"][sl]}, "2pulse"))
        det, hits = rl.cfar_2d(rd, (2, 2), (4, 4), 11.6, axes=(rng, vel))
        c = h["clusters"](det, hits, rd)[0]
        got.append((k, round(float(c[0]), 2), round(float(c[1]), 2)))
    expect("procedure B: frame, walker range m, velocity m/s", got, [(1, 1.67, -0.85), (22, 3.77, -1.81), (41, 1.97, 0.85)])
    t, x, y, t_end, t1 = walk_path()
    tf = walk["truth_t"]
    vr = np.gradient(walk["truth_r"], tf)
    print(f"        truth: radial velocity at those frames {[round(float(-vr[k]), 2) for k in (1, nf // 2, nf - 3)]} "
          f"(+ closing); turn from {t1:.2f} s to {t1 + 1:.2f} s; walk {t_end:.2f} s")

    # Task (a): the window.
    got = []
    for n_win in (16, 64, 256):
        row = [n_win, round(1 / (n_win * 0.5e-3), 1)]
        for k in ("spinner", "walker"):
            cap = caps[(k, 1)]
            r, v, *_ = h["detect"](cap)
            t, f, S = rl.spectrogram(cap, h["target_bins"](cap, r, v), n_win=n_win)
            row.append(round(float(h["line_width"](f, S))))
            if k == "walker":
                row.append(round(float(rl.features(t, f, S, lam)[1]), 2))
        got.append(tuple(row))
    expect("task (a): n_win, resolution Hz, spinner line Hz, walker torso Hz, walker spread m/s", got,
           [(16, 125.0, 192, 246, 1.28), (64, 31.2, 72, 56, 0.68), (256, 7.8, 41, 11, 0.48)])

    # Task (b): the confusion matrix, three features, + edge, + shape.
    def my_features(t, f, S, extra):
        x = rl.features(t, f, S, lam)
        band = S - S.max(axis=0) > -15
        edge = (np.abs(f)[:, None] * band).max(axis=0)
        if extra == "edge":
            x = np.append(x, edge.mean() * lam / 2)
        elif extra == "shape":
            x = np.append(x, x[1] / (edge.mean() * lam / 2))
        return x

    X = {e: [] for e in (None, "edge", "shape")}
    y, names, dets = [], [], []
    for k in KINDS:
        for n in range(1, 5):
            cap = caps[(k, n)]
            r, v, *_ = h["detect"](cap)
            dets.append((f"{k}_{n}", round(float(r), 2), round(float(v), 2)))
            t, f, S = rl.spectrogram(cap, h["target_bins"](cap, r, v), n_win=64)
            for e in X:
                X[e].append(my_features(t, f, S, e))
            y.append(k)
            names.append(f"{k}_{n}")
    print("        L30 detections:", dets)
    y = np.array(y)
    want = {None: ([[4, 0, 0, 0], [0, 2, 2, 0], [0, 1, 3, 0], [0, 0, 0, 4]], ["fan_2", "fan_3", "spinner_2"]),
            "edge": ([[4, 0, 0, 0], [0, 3, 1, 0], [0, 1, 3, 0], [0, 0, 0, 4]], ["fan_3", "spinner_2"]),
            "shape": ([[4, 0, 0, 0], [0, 3, 1, 0], [0, 0, 4, 0], [0, 0, 0, 4]], ["fan_3"])}
    for e in X:
        Xe = np.array(X[e])
        pred = h["leave_one_out"](Xe, y)
        M = rl.confusion_matrix(y, pred, KINDS)
        wrong = [nm for nm, a, b in zip(names, y, pred) if a != b]
        expect(f"task (b) confusion and the records called wrong, extra feature {e}", (M.tolist(), wrong), want[e])
        print("        " + "\n        ".join(f"{nm:10s} {np.round(x, 2)}" for nm, x in zip(names, Xe)))

    # Task (c): the walk.
    zr, za = h["track_meas"](walk)
    Rt, At = walk["truth_r"], walk["truth_az"]
    expect("task (c): frames, frames missed", (len(zr), int(np.isnan(zr).sum())), (44, 0))
    expect("task (c): detections RMS, range m and angle deg",
           (round(float(np.sqrt(np.nanmean((zr - Rt) ** 2))), 2),
            round(float(np.sqrt(np.nanmean((za - At) ** 2))), 2)), (0.1, 0.19))
    settled = tf > 1.0
    turn = settled & (np.abs(tf - tf[np.argmax(Rt)]) < 0.8)
    got = []
    for a in (0.2, 0.5, 0.8):
        b = a * a / (2 - a)
        er = rl.alpha_beta(zr, a, b, FRAME)[:, 0] - Rt
        ea = rl.alpha_beta(za, a, b, FRAME)[:, 0] - At
        got.append((a, round(b, 3), round(float(np.sqrt(np.mean(er[settled] ** 2))), 2),
                    round(float(np.abs(er[settled]).max()), 2), round(float(np.abs(er[turn]).max()), 2),
                    round(float(np.sqrt(np.mean(ea[settled] ** 2))), 2),
                    round(float(np.abs(ea[settled]).max()), 2)))
    expect("task (c): alpha, beta, range RMS, largest, at the turn; angle RMS, largest", got,
           [(0.2, 0.022, 0.37, 0.61, 0.58, 2.56, 3.9), (0.5, 0.167, 0.06, 0.16, 0.16, 0.31, 0.62),
            (0.8, 0.533, 0.08, 0.22, 0.22, 0.16, 0.76)])
    return ok


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--out", type=Path, default=OUT, help="output directory")
    ap.add_argument("--check", action="store_true", help="assert the quoted numbers")
    ap.add_argument("--no-write", action="store_true", help="check the files already there")
    args = ap.parse_args()
    if not args.no_write:
        for p in l31_sets(args.out):
            print(f"wrote {p.relative_to(ROOT) if p.is_relative_to(ROOT) else p} "
                  f"({p.stat().st_size / 1e6:.2f} MB)")
    if args.check:
        sys.exit(0 if check(args.out) else 1)


if __name__ == "__main__":
    main()
