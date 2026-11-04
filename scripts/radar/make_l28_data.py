#!/usr/bin/env python3
"""The L28 Lab's recorded data, and a check of every number the lab quotes from it.

The captures themselves are written by fmcw_sim.l28_sets, at the Phaser app's
Range (Basic) preset (COURSE_SPEC M8.1). This script writes only them, so it
leaves the other labs' files alone, and --check asserts the values the L28 page,
the notebook's Check lines, and the packet key quote, read the way the notebook
reads them (its peak_table: every chirp's power averaged, Hann, 16384 points).

    python3 scripts/radar/make_l28_data.py            # write book/extras/radar-data/L28_*.npz
    python3 scripts/radar/make_l28_data.py --check    # and assert the quoted numbers
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts/radar"))
sys.path.insert(0, str(ROOT / "book/extras/notebooks"))
import fmcw_sim as sim                      # noqa: E402
import radar_lab as rl                      # noqa: E402

OUT = sim.OUT


def peak_table(c, n_fft=16384, top=4):
    """The notebook's peak readout: (kHz, dBFS, dB above the floor, width m) per peak."""
    X = rl.range_fft(c, "hann", n_fft)
    p = 10 * np.log10(np.mean(np.abs(X) ** 2, axis=0) + 1e-30)
    f = np.fft.fftfreq(n_fft, 1 / c["fs"])
    r = rl.range_axis(c, n_fft)
    cell = rl.C / (2 * c["B"])
    floor = np.median(p[(r > 8) & (r < 12)])
    bin_m = (r[1] - r[0]) * n_fft / c["iq"].shape[1]
    cand = np.flatnonzero((f[1:-1] >= 0) & (p[1:-1] > p[:-2]) & (p[1:-1] >= p[2:])
                          & (p[1:-1] > floor + 15)) + 1
    kept = []
    for k in cand[np.argsort(p[cand])[::-1]]:
        if all(abs(r[k] - r[j]) > 3 * cell for j in kept) and bin_m < width(r, p, k) < 4 * bin_m:
            kept.append(k)
        if len(kept) == top:
            break
    return [(f[k] / 1e3, p[k], p[k] - floor, width(r, p, k)) for k in sorted(kept)]


def width(x, p, i):
    lo = hi = i
    while lo > 0 and p[lo - 1] > p[i] - 3:
        lo -= 1
    while hi < len(p) - 1 and p[hi + 1] > p[i] - 3:
        hi += 1
    return x[hi] - x[lo] + (x[1] - x[0])


def check(out: Path = OUT) -> bool:
    ok = True

    def expect(what, got, want, tol):
        nonlocal ok
        good = abs(got - want) <= tol
        ok &= good
        print(f"  {'PASS' if good else 'FAIL'}  {what}: {got:.3f} (quoted {want}, +/- {tol})")

    load = lambda n: rl.load_capture(out / n)              # noqa: E731
    near = lambda rows, khz: min(rows, key=lambda row: abs(row[0] - khz))   # noqa: E731

    print("Table A")
    rows = peak_table(load("L28_clear.npz"))
    expect("clear bench: leakage, kHz", near(rows, 101.4)[0], 101.40, 0.005)
    expect("clear bench: wall, kHz", near(rows, 119.75)[0], 119.75, 0.01)
    rows = peak_table(load("L28_cal_0m.npz"))
    expect("plate against the array: f0, kHz", rows[0][0], 101.48, 0.005)
    expect("plate over leakage, dB", rows[0][1] - (-20.0), 10.4, 0.2)
    for n in ("L28_clear.npz", "L28_cal_0m.npz"):
        expect(f"{n} f0 field is the IF tone, kHz", load(n)["f0"] / 1e3, 100.0, 1e-9)

    print("Table B")
    f_b = []
    for tape, khz in ((1, 104.70), (2, 108.11), (3, 111.51)):
        c = load(f"L28_corner_{tape}m.npz")
        f_b.append(near(peak_table(c), khz)[0])
        expect(f"corner at {tape} m by the tape, kHz", f_b[-1], khz, 0.005)
        expect(f"  its f0 field, kHz", c["f0"] / 1e3, 101.4, 1e-9)
    slope, icpt = np.polyfit([1, 2, 3], f_b, 1)
    expect("fitted slope, kHz/m", slope, 3.41, 0.005)
    expect("fitted intercept, kHz", icpt, 101.29, 0.005)

    print("Table C")
    basic = near(peak_table(load("L28_corner_2m.npz")), 108.11)
    fast_c = load("L28_corner_2m_fast.npz")
    fast = near(peak_table(fast_c), 114.75)
    b250 = near(peak_table(load("L28_corner_2m_B250.npz")), 104.74)
    expect("Range (Fast) samples a chirp", fast_c["iq"].shape[1], 2250, 0)
    expect("Range (Fast): peak, kHz", fast[0], 114.75, 0.005)
    expect("B 250 MHz: peak, kHz", b250[0], 104.74, 0.005)
    expect("Range (Basic): width, m", basic[3], 0.48, 0.005)
    expect("Range (Fast): width, m", fast[3], 0.50, 0.005)
    expect("B 250 MHz: width, m", b250[3], 0.99, 0.005)
    expect("Range (Basic): height above floor, dB", basic[2], 65.4, 0.05)
    expect("Range (Fast): height above floor, dB", fast[2], 63.0, 0.05)
    expect("B 250 MHz: height above floor, dB", b250[2], 65.3, 0.05)

    print("Table E")
    cap = load("L28_corner_2m.npz")
    for win, sl, fl in (("hann", -31.4, -86.3), (None, -12.4, -55.9)):
        r, p = rl.range_profile(cap, window=win, n_fft=4096)
        m = (r >= 0.5) & (r <= 8)
        i = np.flatnonzero(m)[np.argmax(p[m])]
        a = b = i
        while p[a + 1] < p[a]:
            a += 1
        while p[b - 1] < p[b]:
            b -= 1
        side = (np.abs(r - r[i]) < 1.2)
        side[b:a + 1] = False
        expect(f"task (a) {win}: peak, m", r[i], 2.01, 0.005)
        expect(f"task (a) {win}: peak, dBFS", p[i], -19.6, 0.05)
        expect(f"task (a) {win}: sidelobe, dBc", p[side].max() - p[i], sl, 0.05)
        expect(f"task (a) {win}: floor near 10 m, dBFS", np.median(p[(r > 8) & (r < 12)]), fl, 0.05)
    two = load("L28_two_corners.npz")
    for n_fft, at, w in ((None, 2.25, 0.67), (4096, 2.10, 0.53)):
        r, p = rl.range_profile(two, n_fft=n_fft)
        m = (r > 1.5) & (r < 2.7)
        i = np.flatnonzero(m)[np.argmax(p[m])]
        pk = np.flatnonzero(m[1:-1] & (p[1:-1] > p[:-2]) & (p[1:-1] > p[2:]) & (p[1:-1] > p[m].max() - 6)) + 1
        expect(f"task (b) n_fft {n_fft}: peaks", len(pk), 1, 0)
        expect(f"task (b) n_fft {n_fft}: peak, m", r[i], at, 0.005)
        expect(f"task (b) n_fft {n_fft}: width, m", width(r, p, i), w, 0.005)
    X = rl.range_fft(cap, "hann", 4096)[0]
    f = np.fft.fftfreq(4096, 1 / cap["fs"])
    k = 2 * cap["B"] / (rl.C * cap["T_ramp"])
    s = (f > 101.48e3 + 0.5 * k) & (f < cap["fs"] / 2)
    f_peak = f[s][np.argmax(np.abs(X[s]))]
    expect("task (c): f_peak, kHz", f_peak / 1e3, 108.11, 0.005)
    expect("task (c): R with F0 = 101.48 kHz, m", (f_peak - 101.48e3) / k, 1.99, 0.005)

    print("Waterfall")
    r, t, w = rl.waterfall(load("L28_walker.npz"))
    m = (r > 0.5) & (r < 5)
    track = r[m][np.argmax(w[:, m], axis=1)]
    expect("walker, nearest, m", np.percentile(track, 2), 1.0, 0.15)
    expect("walker, farthest, m", np.percentile(track, 98), 4.0, 0.25)
    expect("walker, seconds a chirp", float(load("L28_walker.npz")["PRI"]), 0.05, 1e-9)
    print("all L28 checks pass" if ok else "SOME L28 CHECKS FAIL")
    return ok


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--out", type=Path, default=OUT, help="output directory")
    ap.add_argument("--check", action="store_true", help="assert the quoted numbers")
    args = ap.parse_args()
    for p in sim.l28_sets(args.out):
        print(f"wrote {p.relative_to(ROOT) if p.is_relative_to(ROOT) else p} ({p.stat().st_size / 1e3:.0f} kB)")
    if args.check:
        sys.exit(0 if check(args.out) else 1)


if __name__ == "__main__":
    main()
