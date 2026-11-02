#!/usr/bin/env python3
"""The L30 Lab's recorded data: three range-Doppler bursts for CFAR.

Each capture is one burst of the l29_burst waveform in scripts/radar/fmcw_sim.py
(256 chirps of 300 us, PRI 0.5 ms, 4 MSPS, B 500 MHz, 10 GHz), the same
waveform as the L29 Lab's maps, built only from fmcw_sim's own functions so
this script never needs the simulator changed. Each file holds `iq` only (no
`iq_ch`: CFAR needs no angle), about 2.5 MB:

    L30_empty.npz        noise and the kit's own leakage: no target. Every
                         detection away from 0 m and 0 m/s is a false alarm.
    L30_wall_hand.npz    a wall at 5.0 m and a hand waving at 2.4 m: the wall
                         is a strong fixed return on the zero-velocity column.
                         The hand stays more than a window's width from the
                         leakage and the wall, so neither reaches its
                         reference cells (task (c) measures its Pd).
    L30_weak_strong.npz  a strong mover at 4.2 m and a weak one 1.2 m nearer,
                         four range cells apart, at nearly the same velocity:
                         the masking case.

    python3 scripts/radar/make_l30_data.py           # write the three files
    python3 scripts/radar/make_l30_data.py --check   # and assert the numbers the
                                                     # page and packet quote (task (c)'s
                                                     # Pd is checked by running the notebook)
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

# The scenes. Ranges in m, velocities in m/s positive closing (L26).
WALL_R, WALL_RCS = 5.0, 5.0                     # a wall face, square to the beam
HAND_R = 2.4                                    # the hand's mean range
STRONG = dict(r0=4.2, v=0.6, rcs=0.5)           # about a person's torso
WEAK = dict(r0=3.0, v=0.5, rcs=0.02)            # about a hand


def _save(cap: dict, path: Path, note: str) -> Path:
    """Write the contract's .npz with iq only: the summed array, complex64."""
    path.parent.mkdir(parents=True, exist_ok=True)
    np.savez(path, iq=sim.iq(cap).astype(np.complex64),
             fs=cap["fs"], fc=cap["fc"], B=cap["B"], T_ramp=cap["T_ramp"],
             PRI=cap["PRI"], f0=cap["f0"], note=np.str_(note))
    return path


def l30_sets(out: Path = OUT) -> list[Path]:
    written = []

    cap = sim.new_capture("l29_burst")
    sim.add_noise(cap, seed=3001)
    sim.add_leakage(cap)
    written.append(_save(cap, out / "L30_empty.npz",
                         "L30 Lab recorded data: an empty scene, noise and the kit's own leakage, "
                         "one 256-chirp burst"))

    cap = sim.new_capture("l29_burst")
    sim.add_noise(cap, seed=3002)
    sim.add_leakage(cap)
    sim.add_point(cap, WALL_R, rcs=WALL_RCS, phase0=0.4)
    sim.add_hand(cap, r0=HAND_R)
    written.append(_save(cap, out / "L30_wall_hand.npz",
                         f"L30 Lab recorded data: a wall at {WALL_R:.1f} m and a hand waving at "
                         f"{HAND_R:.1f} m, one 256-chirp burst"))

    cap = sim.new_capture("l29_burst")
    sim.add_noise(cap, seed=3003)
    sim.add_leakage(cap)
    sim.add_point(cap, **STRONG, phase0=0.9)
    sim.add_point(cap, **WEAK, phase0=2.3)
    written.append(_save(cap, out / "L30_weak_strong.npz",
                         f"L30 Lab recorded data: a strong mover at {STRONG['r0']:.1f} m, "
                         f"{STRONG['v']:+.1f} m/s and a weak one at {WEAK['r0']:.1f} m, "
                         f"{WEAK['v']:+.1f} m/s, one 256-chirp burst"))
    return written


def check(out: Path = OUT) -> bool:
    """Recompute the numbers the L30 page, notebook, and packet quote, and assert them."""
    import radar_lab as rl
    from scipy import ndimage

    ok = True

    def expect(name, got, want):
        nonlocal ok
        good = got == want
        ok &= good
        print(f"  {'PASS' if good else 'FAIL'}  {name}: {got}" + ("" if good else f", expected {want}"))

    def bias_db(n, pfa):
        return 10 * np.log10(n * (pfa ** (-1 / n) - 1))

    expect("biases, N = 32", [round(bias_db(32, p), 2) for p in (1e-3, 1e-4, 1e-6)], [8.87, 10.28, 12.37])
    expect("biases, N = 144", [round(bias_db(144, p), 2) for p in (1e-3, 1e-4, 1e-6)], [8.5, 9.78, 11.61])

    # Task (a): false alarms in the quiet cells of the empty burst.
    empty = rl.load_capture(out / "L30_empty.npz")
    counts = []
    for window, pfa in (("hann", 1e-3), ("hann", 1e-4), (None, 1e-3)):
        rd, rng, vel = rl.range_doppler(empty, window=window)
        j0 = np.argmin(np.abs(vel))
        test = (rng > 1.0)[:, None] & (np.abs(np.arange(vel.size) - j0) > 7)[None, :]
        det, _ = rl.cfar_2d(rd, 2, 4, bias_db(144, pfa))
        counts.append((int(test.sum()), int(det[test].sum())))
    expect("task (a) cells tested and false alarms", counts, [(136406, 172), (136406, 29), (136406, 147)])

    # Task (b): cells in each cluster, by method.
    def clusters(cap, method, mti=False):
        rd, rng, vel = rl.range_doppler(rl.mti(cap, "2pulse") if mti else cap)
        det, hits = rl.cfar_2d(rd, 2, 4, 11.6, axes=(rng, vel), method=method)
        lab, n = ndimage.label(det)
        out = []
        for k in range(1, n + 1):
            i, j = np.nonzero(lab == k)
            b = np.argmax(rd[i, j])
            out.append((round(float(rng[i[b]]), 2), round(float(vel[j[b]]), 2), len(i)))
        return sorted(out)

    wall_hand = rl.load_capture(out / "L30_wall_hand.npz")
    weak_strong = rl.load_capture(out / "L30_weak_strong.npz")
    for method, want in (("ca", [8, 6, 9, 1]), ("go", [8, 6, 9, 0]), ("so", [10, 22, 19, 5])):
        c = clusters(wall_hand, method)
        leak = sum(n for r, v, n in c if r < 1.0 and abs(v) < 0.2)
        hand = sum(n for r, v, n in c if 1.5 < r < 3.5 and 0.3 < abs(v) < 2)
        wall = sum(n for r, v, n in c if 3.5 < r < 6.5 and abs(v) < 0.2)
        other = len(c) - sum(1 for r, v, n in c if (r < 1.0 and abs(v) < 0.2)
                             or (1.5 < r < 3.5 and 0.3 < abs(v) < 2) or (3.5 < r < 6.5 and abs(v) < 0.2))
        expect(f"task (b) wall_hand {method}: leakage, hand, wall cells; other clusters", [leak, hand, wall, other], want)
    for method, want in (("ca", [7, 0, 0]), ("go", [7, 0, 0]), ("so", [21, 6, 2])):
        c = clusters(weak_strong, method)
        strong = sum(n for r, v, n in c if 3.6 < r < 6.5 and abs(v) > 0.3)
        weak = sum(n for r, v, n in c if 2.5 < r < 3.6 and abs(v) > 0.3)
        other = sum(1 for r, v, n in c if r > 8)
        expect(f"task (b) weak_strong {method}: strong, weak cells; far clusters", [strong, weak, other], want)

    # The detection list: after the 2-pulse canceller, the hand and one false alarm.
    expect("detection list, (range, velocity, cells)", clusters(wall_hand, "ca", mti=True),
           [(2.57, -0.82, 10), (10.97, -1.65, 1)])
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
