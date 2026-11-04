#!/usr/bin/env python3
"""The L30 Lab's recorded data, on the Phaser app's presets (COURSE_SPEC M8.1).

Two waveforms, passed explicitly to fmcw_sim's new_capture, so this script
never needs the simulator's PRESETS changed:

    the app's `cfar` preset, Range (CFAR): 10 GHz, 500 MHz in 0.5 ms, 2 MSPS
        (1000 samples, 6.67 kHz of beat per meter, 0.30 m cells), one chirp a
        display update. The app's CFAR overlay runs on this range profile, so
        Procedures A-C use it. Each file is what the app's Save Capture writes
        on that preset: one chirp a row, PRI the display interval.
    the app's `range_doppler` preset, Range + Velocity: 9.9 GHz, 500 MHz in
        300 us, PRI 0.5 ms, 2 MSPS (600 samples, 11.1 kHz per meter), 256
        chirps: CPI 128 ms, 0.30 m by 0.118 m/s cells, +-15.2 m/s. The
        notebook's 2-D CFAR (tasks (a)-(c)) runs on these bursts.

Every file holds `iq` only (no `iq_ch`: CFAR needs no angle):

    L30_range_person.npz  [cfar] a person standing still at 3.0 m and a wall
                          at 6.0 m, 32 updates 50 ms apart: Procedure A.
    L30_walker.npz        [cfar] a person walking 1.0 m -> 4.5 m -> 1.0 m at
                          1 m/s past a wall at 6.0 m, one update every 0.1 s
                          for 7 s: Procedure B.
    L30_range_empty.npz   [cfar] noise and the kit's own leakage, 32 updates
                          50 ms apart: Procedure C.
    L30_empty.npz         [range_doppler] noise and the leakage, one burst:
                          task (a). Every detection away from 0 m and 0 m/s is
                          a false alarm.
    L30_wall_hand.npz     [range_doppler] a wall at 5.0 m and a hand waving
                          about 2.4 m (it spans about 2.3-2.6 m): tasks (b)
                          and (c). The hand stays more than a window's width
                          from the leakage and the wall.
    L30_weak_strong.npz   [range_doppler] a strong mover at 4.2 m and a weak one
                          1.2 m nearer, four range cells apart, at nearly the
                          same velocity: the masking case of task (b).

    python3 scripts/radar/make_l30_data.py           # write the six files
    python3 scripts/radar/make_l30_data.py --check   # and assert the numbers the
                                                     # page, notebook and packet quote
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

# The app's presets (livethisdream/phaser, FMCW_PRESETS), as new_capture overrides.
APP_CFAR = dict(fs=2.0e6, fc=10.0e9, B=500e6, T_ramp=0.5e-3, PRI=50e-3, n_chirps=32)
APP_RD = dict(fs=2.0e6, fc=9.9e9, B=500e6, T_ramp=300e-6, PRI=0.5e-3, n_chirps=256)

# The scenes. Ranges in m, velocities in m/s positive closing (L26).
PERSON_R, PERSON_RCS = 3.0, 0.5                 # you, standing still (Procedure A)
ROOM_WALL_R = 6.0                               # the far wall behind you (Procedures A and B)
WALL_R, WALL_RCS = 5.0, 5.0                     # a wall face, square to the beam (the bursts)
HAND_R = 2.4                                    # the hand's mean range
STRONG = dict(r0=4.2, v=0.6, rcs=0.5)           # about a person's torso
WEAK = dict(r0=3.0, v=0.5, rcs=0.02)            # about a hand
WALK_PRI, WALK_N = 0.1, 70                      # the walker: one chirp per display update


def _cap(wave: dict, **overrides) -> dict:
    return sim.new_capture("l29_burst", **{**wave, **overrides})


def _save(cap: dict, path: Path, note: str) -> Path:
    """Write the contract's .npz with iq only: the summed array, complex64."""
    path.parent.mkdir(parents=True, exist_ok=True)
    np.savez(path, iq=sim.iq(cap).astype(np.complex64),
             fs=cap["fs"], fc=cap["fc"], B=cap["B"], T_ramp=cap["T_ramp"],
             PRI=cap["PRI"], f0=cap["f0"], note=np.str_(note))
    return path


def l30_sets(out: Path = OUT) -> list[Path]:
    written = []
    app = "the app's Range (CFAR) preset, 0.5 ms chirps at 10 GHz, 2 MSPS"
    burst = "one 256-chirp burst of the app's Range + Velocity preset (300 us, PRI 0.5 ms, 9.9 GHz, 2 MSPS)"

    cap = _cap(APP_CFAR)
    sim.add_noise(cap, seed=3011)
    sim.add_leakage(cap)
    sim.add_point(cap, PERSON_R, rcs=PERSON_RCS, phase0=1.7)
    sim.add_point(cap, ROOM_WALL_R, rcs=WALL_RCS, phase0=0.4)
    written.append(_save(cap, out / "L30_range_person.npz",
                         f"L30 Lab recorded data: a person standing still at {PERSON_R:.1f} m and a wall at "
                         f"{ROOM_WALL_R:.1f} m; {app}, 32 updates 50 ms apart"))

    cap = _cap(APP_CFAR, PRI=WALK_PRI, n_chirps=WALK_N)
    sim.add_noise(cap, seed=3004)
    sim.add_leakage(cap)
    sim.add_point(cap, ROOM_WALL_R, rcs=WALL_RCS, phase0=0.4)
    sim.add_walker(cap, r_start=1.0, r_turn=4.5, speed=1.0)
    written.append(_save(cap, out / "L30_walker.npz",
                         f"L30 Lab recorded data: a person walking 1.0 m -> 4.5 m -> 1.0 m at 1 m/s, "
                         f"a wall at {ROOM_WALL_R:.1f} m; {app}, one update every {WALK_PRI:.1f} s, "
                         f"{WALK_N} updates"))

    cap = _cap(APP_CFAR)
    sim.add_noise(cap, seed=3012)
    sim.add_leakage(cap)
    written.append(_save(cap, out / "L30_range_empty.npz",
                         f"L30 Lab recorded data: an empty scene, noise and the kit's own leakage; "
                         f"{app}, 32 updates 50 ms apart"))

    cap = _cap(APP_RD)
    sim.add_noise(cap, seed=3036)
    sim.add_leakage(cap)
    written.append(_save(cap, out / "L30_empty.npz",
                         f"L30 Lab recorded data: an empty scene, noise and the kit's own leakage; {burst}"))

    cap = _cap(APP_RD)
    sim.add_noise(cap, seed=3002)
    sim.add_leakage(cap)
    sim.add_point(cap, WALL_R, rcs=WALL_RCS, phase0=0.4)
    sim.add_hand(cap, r0=HAND_R)
    written.append(_save(cap, out / "L30_wall_hand.npz",
                         f"L30 Lab recorded data: a wall at {WALL_R:.1f} m and a hand waving about "
                         f"{HAND_R:.1f} m; {burst}"))

    cap = _cap(APP_RD)
    sim.add_noise(cap, seed=3003)
    sim.add_leakage(cap)
    sim.add_point(cap, **STRONG, phase0=0.9)
    sim.add_point(cap, **WEAK, phase0=2.3)
    written.append(_save(cap, out / "L30_weak_strong.npz",
                         f"L30 Lab recorded data: a strong mover at {STRONG['r0']:.1f} m, "
                         f"{STRONG['v']:+.1f} m/s and a weak one at {WEAK['r0']:.1f} m, "
                         f"{WEAK['v']:+.1f} m/s; {burst}"))
    return written


def app_profile(cap: dict, k: int, range_max: float = 20.0):
    """Update k's range profile as the Phaser app draws it (frontend-radar dsp.js
    rangeProfile): Blackman, no zero padding, 0 m to Range Max. The notebook's copy."""
    iq = cap["iq"][k]
    n = iq.size
    w = np.blackman(n)
    X = np.fft.fft(iq * w)[: n // 2] / w.sum()
    r = (np.arange(n // 2) * cap["fs"] / n - cap["f0"]) * sim.C * cap["T_ramp"] / (2 * cap["B"])
    keep = (r >= 0) & (r <= range_max)
    return r[keep], 20 * np.log10(np.abs(X[keep]) + 1e-15)


def threshold_1d(p_db, guard, ref, bias_db):
    """The app's ca_cfar (phaser_radar_dsp.py): guard and ref cells a side, power
    averaged, the reference cells that exist used at the ends."""
    n, P = p_db.size, 10 ** (p_db / 10)
    cs, i = np.r_[0, np.cumsum(P)], np.arange(p_db.size)
    lo, hi = np.maximum(i - guard - ref, 0), np.minimum(i + guard + ref + 1, n)
    glo, ghi = np.maximum(i - guard, 0), np.minimum(i + guard + 1, n)
    noise = ((cs[hi] - cs[lo]) - (cs[ghi] - cs[glo])) / ((hi - lo) - (ghi - glo))
    thr = 10 * np.log10(noise) + bias_db
    return thr, p_db > thr


def crossings(det, r):
    e = np.flatnonzero(np.diff(np.r_[0, det.astype(int), 0]))
    return [(r[a] + r[b - 1]) / 2 for a, b in zip(e[::2], e[1::2])]


def check(out: Path = OUT) -> bool:
    """Recompute the numbers the L30 page, notebook, and packet quote, and assert them."""
    import radar_lab as rl
    from scipy import ndimage, stats

    ok = True

    def expect(name, got, want):
        nonlocal ok
        good = got == want
        ok &= good
        print(f"  {'PASS' if good else 'FAIL'}  {name}: {got}" + ("" if good else f", expected {want}"))

    def bias_db(n, pfa):
        return 10 * np.log10(n * (pfa ** (-1 / n) - 1))

    expect("biases, N = 8", [round(bias_db(8, p), 1) for p in (1e-3, 1e-4, 1e-6)], [10.4, 12.4, 15.7])
    expect("biases, N = 32", [round(bias_db(32, p), 2) for p in (1e-3, 1e-4, 1e-6)], [8.87, 10.28, 12.37])
    expect("biases, N = 144", [round(bias_db(144, p), 2) for p in (1e-3, 1e-4, 1e-6)], [8.5, 9.78, 11.61])

    # Procedure A: the app's CFAR on update 0 of the person, and noise crossings in 32 updates.
    person = rl.load_capture(out / "L30_range_person.npz")
    r, p = app_profile(person, 0)
    near = np.abs(r - PERSON_R) < 1.0
    ip = np.flatnonzero(near)[np.argmax(p[near])]
    objects = (r < 1.0) | (np.abs(r - r[ip]) < 1.0) | (np.abs(r - ROOM_WALL_R) < 1.0)
    got = []
    for g, ref, b in ((4, 16, 6.0), (2, 16, 12.4), (3, 4, 13.0), (0, 4, 13.0)):
        thr, _ = threshold_1d(p, g, ref, b)
        fa = sum(bool((threshold_1d(app_profile(person, k)[1], g, ref, b)[1] & ~objects).any())
                 for k in range(person["iq"].shape[0]))
        got.append((round(float(p[ip] - thr[ip]), 1), round(float(np.max((p - thr)[~objects])), 1), fa))
    expect("procedure A: peak margin, noise margin, updates with a noise crossing; app / lesson / key / no guard",
           got, [(-5.1, -0.4, 15), (-11.2, -6.3, 0), (39.3, -6.3, 0), (-3.5, -7.8, 0)])
    rise = threshold_1d(p, 0, 4, 13.0)[0][ip] - threshold_1d(p, 3, 4, 13.0)[0][ip]
    expect("procedure A: threshold rise at the peak with 0 guard cells, dB", round(float(rise), 1), 42.7)
    expect("procedure A: cells beyond 1 m", int((r > 1.0).sum()), 63)

    walker = rl.load_capture(out / "L30_walker.npz")
    got = []
    for b in (13.0, 16.0):
        found = others = 0
        seen = []
        for k in range(walker["iq"].shape[0]):
            r, p = app_profile(walker, k)
            xs = [x for x in crossings(threshold_1d(p, 3, 4, b)[1], r)
                  if not (x <= 1.0 or 5.0 <= x <= 7.0)]
            near = [x for x in xs if x < 5.0]
            found += bool(near); others += bool(set(xs) - set(near)); seen += near
        got.append((found, round(min(seen), 2), round(max(seen), 2), others))
    expect("procedure B: walker updates, nearest, farthest, other updates", got,
           [(29, 2.79, 3.39, 0), (27, 2.79, 3.39, 0)])

    empty_r = rl.load_capture(out / "L30_range_empty.npz")
    got = []
    for b in (13.0, 10.0, 7.0):
        hits = total = 0
        for k in range(30):
            r, p = app_profile(empty_r, k)
            xs = [x for x in crossings(threshold_1d(p, 3, 4, b)[1], r) if x > 1.0]
            hits += bool(xs); total += len(xs)
        got.append((hits, total))
    expect("procedure C: updates of 30 with a crossing, crossings", got, [(1, 1), (3, 3), (20, 31)])
    pred = [round(30 * (1 - (1 - (1 + 10 ** (b / 10) / 8) ** -8) ** 63), 1) for b in (13.0, 10.0, 7.0)]
    expect("procedure C: predicted updates of 30, N = 8, 63 cells", pred, [0.1, 2.7, 21.8])

    # Task (a): false alarms in the quiet cells of the empty burst.
    empty = rl.load_capture(out / "L30_empty.npz")
    counts = []
    for window, pfa in (("hann", 1e-3), ("hann", 1e-4), (None, 1e-3)):
        rd, rng, vel = rl.range_doppler(empty, window=window)
        j0 = np.argmin(np.abs(vel))
        test = (rng > 1.0)[:, None] & (np.abs(np.arange(vel.size) - j0) > 7)[None, :]
        det, _ = rl.cfar_2d(rd, 2, 4, bias_db(144, pfa))
        counts.append((int(test.sum()), int(det[test].sum())))
    expect("task (a) cells tested and false alarms", counts, [(64106, 91), (64106, 9), (64106, 63)])

    # Task (b): cells in each cluster, by method.
    def clusters(cap, method, mti=False):
        rd, rng, vel = rl.range_doppler(rl.mti(cap, "2pulse") if mti else cap)
        det, hits = rl.cfar_2d(rd, 2, 4, 11.6, axes=(rng, vel), method=method)
        lab, n = ndimage.label(det)
        res = []
        for k in range(1, n + 1):
            i, j = np.nonzero(lab == k)
            b = np.argmax(rd[i, j])
            res.append((round(float(rng[i[b]]), 2), round(float(vel[j[b]]), 2), len(i)))
        return sorted(res)

    wall_hand = rl.load_capture(out / "L30_wall_hand.npz")
    weak_strong = rl.load_capture(out / "L30_weak_strong.npz")
    for method, want in (("ca", [8, 6, 9, 0]), ("go", [8, 6, 9, 0]), ("so", [9, 21, 20, 0])):
        c = clusters(wall_hand, method)
        leak = sum(n for r, v, n in c if r < 1.0 and abs(v) < 0.2)
        hand = sum(n for r, v, n in c if 1.5 < r < 3.5 and 0.3 < abs(v) < 2)
        wall = sum(n for r, v, n in c if 3.5 < r < 6.5 and abs(v) < 0.2)
        other = len(c) - sum(1 for r, v, n in c if (r < 1.0 and abs(v) < 0.2)
                             or (1.5 < r < 3.5 and 0.3 < abs(v) < 2) or (3.5 < r < 6.5 and abs(v) < 0.2))
        expect(f"task (b) wall_hand {method}: leakage, hand, wall cells; other clusters", [leak, hand, wall, other], want)
    for method, want in (("ca", [9, 7, 0, 0]), ("go", [9, 7, 0, 0]), ("so", [9, 22, 7, 3])):
        c = clusters(weak_strong, method)
        leak = sum(n for r, v, n in c if r < 1.0 and abs(v) < 0.2)
        strong = sum(n for r, v, n in c if 3.6 < r < 6.5 and abs(v) > 0.3)
        weak = sum(n for r, v, n in c if 2.5 < r < 3.6 and abs(v) > 0.3)
        other = sum(1 for r, v, n in c if not ((r < 1.0 and abs(v) < 0.2) or (2.5 < r < 6.5 and abs(v) > 0.3)))
        expect(f"task (b) weak_strong {method}: leakage, strong, weak cells; other clusters",
               [leak, strong, weak, other], want)

    # Task (c): the predictions for the hand at 12 dB (the measured Pd is the notebook's 50 trials).
    N, snr = 144, 10 ** 1.2
    x = np.linspace(0.3, 2.5, 2001)
    got = []
    for b in (11.6, 8.50):
        a = 10 ** (b / 10)
        known = stats.ncx2.sf(2 * a, 2, 2 * snr)
        cfar = np.sum(stats.ncx2.sf(2 * a * x, 2, 2 * snr) * stats.gamma.pdf(x, N, scale=1 / N)) * (x[1] - x[0])
        swer = (1 + a / (N * (1 + snr))) ** -N
        got.append((round(float(known), 2), round(float(cfar), 2), round(float(swer), 2)))
    expect("task (c) predictions: steady known, steady CA-CFAR, Swerling 1 CA-CFAR", got,
           [(0.63, 0.63, 0.43), (0.98, 0.97, 0.66)])
    # The detection list: after the 2-pulse canceller, the hand alone.
    expect("detection list, (range, velocity, cells)", clusters(wall_hand, "ca", mti=True), [(2.57, -0.83, 10)])
    return ok


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--out", type=Path, default=OUT, help="output directory")
    ap.add_argument("--check", action="store_true", help="assert the quoted numbers")
    args = ap.parse_args()
    for p in l30_sets(args.out):
        print(f"wrote {p.relative_to(ROOT) if p.is_relative_to(ROOT) else p} "
              f"({p.stat().st_size / 1e6:.2f} MB)")
    if args.check:
        sys.exit(0 if check(args.out) else 1)


if __name__ == "__main__":
    main()
