#!/usr/bin/env python3
"""The L29 Lab's recorded data: eight range-Doppler bursts, and a check of them.

The bursts themselves are fmcw_sim.l29_sets, on the l29_burst waveform: the
Phaser app's range_doppler preset ("Range + Velocity", COURSE_SPEC M8.1),
9.9 GHz, 256 chirps of 300 us every 0.5 ms, 2 MSPS, 500 MHz. This script
writes only them, so regenerating L29 never touches another lab's files, and
--check asserts the numbers the L29 page, the notebook's Check lines, and the
packet key quote, read the way the notebook reads them.

    python3 scripts/radar/make_l29_data.py           # write the eight files
    python3 scripts/radar/make_l29_data.py --check   # and assert the quoted numbers
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


def check(out: Path) -> bool:
    import radar_lab as rl
    ok = True

    def expect(what, got, want):
        nonlocal ok
        good = got == want
        ok &= good
        print(f"  {'PASS' if good else 'FAIL'}  {what}: {got}" + ("" if good else f", expected {want}"))

    load = lambda name: rl.load_capture(out / f"L29_{name}.npz")
    r1 = lambda x: round(float(x), 1)
    r2 = lambda x: round(float(x), 2)

    # The notebook's readouts, as its helper cell defines them.
    def strongest(rd, r, v, r_lo, r_hi, v_lo, v_hi):
        m = ((r >= r_lo) & (r <= r_hi))[:, None] & ((v >= v_lo) & (v <= v_hi))[None, :]
        i, j = np.unravel_index(np.argmax(np.where(m, rd, -400)), rd.shape)
        return i, j, rd[i, j]

    def mover(rd, r, v, r_lo=0.3, r_hi=6.0):
        return max(strongest(rd, r, v, r_lo, r_hi, 0.3, 15), strongest(rd, r, v, r_lo, r_hi, -15, -0.3),
                   key=lambda c: c[2])

    def pv(row, j, v):
        a, b, c = row[j - 1], row[j], row[(j + 1) % len(row)]
        return v[j] + 0.5 * (a - c) / (a - 2 * b + c) * (v[1] - v[0])

    def floor(rd, r, v, v_lo=-15, v_hi=15):
        return np.median(rd[(r > 6) & (r < 20)][:, (v >= v_lo) & (v <= v_hi)])

    def width(row, j, step):
        top = row[j] - 3
        lo = hi = j
        while lo > 0 and row[lo - 1] > top: lo -= 1
        while hi < len(row) - 1 and row[hi + 1] > top: hi += 1
        return (hi + (row[hi] - top) / (row[hi] - row[hi + 1])
                - lo + (row[lo] - top) / (row[lo] - row[lo - 1])) * step

    # The map cell, on the closing hand, the opening hand, the 200 MHz hand.
    for name, want in (("hand_closing", (1.07, 0.98, -26.6, 0.42, 2.57, -18.6, 0.17, -21.9, -109.8)),
                       ("hand_opening", (0.77, -1.46, -23.1, 0.31, 2.57, -18.6, 0.17, -21.9, -109.8)),
                       ("hand_closing_B200", (1.19, 0.99, -26.5, 0.97, 2.69, -18.6, 0.44, -22.1, -109.8))):
        rd, r, v = rl.range_doppler(load(name))
        i, j, lv = mover(rd, r, v)
        iw, _, lw = strongest(rd, r, v, 1.5, 6.0, -0.01, 0.01)
        j0 = int(np.argmin(np.abs(v)))
        expect(f"map cell, {name}: hand r, v, dBFS, width in r; wall r, dBFS; leakage r, dBFS; floor",
               (r2(r[i]), r2(pv(rd[i], j, v)), r1(lv), r2(width(rd[:, j], i, r[1] - r[0])),
                r2(r[iw]), r1(lw), r2(r[0]), r1(rd[0, j0]), r1(floor(rd, r, v))), want)
    rd, r, v = rl.range_doppler(load("static"))
    expect("static: brightest cell is the wall, at 2.57 m", r2(r[np.unravel_index(rd.argmax(), rd.shape)[0]]), 2.57)

    # Task (a): the first M chirps of the closing hand.
    cap = load("hand_closing")
    rd, r, v = rl.range_doppler(cap)
    i_hand = mover(rd, r, v)[0]
    got = []
    for m in (256, 128, 64):
        rd_m, r_m, v_m = rl.range_doppler({**cap, "iq": cap["iq"][:m]})
        dv = v_m[1] - v_m[0]
        j = int(np.argmax(np.where(np.abs(v_m) > 0.3, rd_m[i_hand], -400)))
        got.append((round(float(dv), 3), r2(width(rd_m[i_hand], j, dv)), r1(rd_m[i_hand, j]), r1(floor(rd_m, r_m, v_m))))
    expect("task (a): dv, width, level, floor at M = 256, 128, 64", got,
           [(0.118, 0.15, -26.6, -109.8), (0.237, 0.25, -26.5, -106.8), (0.473, 0.48, -26.5, -104.1)])

    # Task (b): the cancellers on the closing hand.
    lam = rl.C / cap["fc"]
    i, j, h0 = mover(rd, r, v)
    f_d = 2 * pv(rd[i], j, v) / lam
    iw, _, w0 = strongest(rd, r, v, 1.5, 6.0, -0.01, 0.01)
    got = []
    for kind, n in (("2pulse", 1), ("3pulse", 2)):
        rd1, _, v1 = rl.range_doppler(rl.mti(cap, kind))
        h1 = rd1[i, np.argmin(np.abs(v1 - v[j]))]
        hdb = n * 10 * np.log10(4 * np.sin(np.pi * f_d * cap["PRI"]) ** 2)
        col = lambda rd_, v_, vv: floor(rd_, r, v_, vv - 0.15, vv + 0.15)
        got.append((r1(h1 - h0), r1(hdb), round(float(w0 - rd1[iw, np.argmin(np.abs(v1))])),
                    r1(col(rd, v, v[j] + 0)), r1(col(rd1, v1, pv(rd[i], j, v))),
                    r1(floor(rd, r, v, 13.5, 14.5)), r1(floor(rd1, r, v1, 13.5, 14.5))))
    expect("task (b): hand change, H_DB, wall drop, hand-column floor, 14 m/s floor", got,
           [(-13.8, -13.9, 125, -109.3, -123.7, -110.4, -104.3), (-27.7, -27.8, 159, -109.3, -138.0, -110.4, -98.5)])

    # Task (c) and Table C: the spinner's lines, and the spectrogram's band.
    def lines(row, v, v_min=0.3, below=10):
        keep = np.abs(v) > v_min
        top = row[keep].max()
        return np.array([pv(row, k, v) for k in range(1, len(row) - 1)
                         if keep[k] and row[k] >= row[k - 1] and row[k] >= row[k + 1] and row[k] > top - below])

    got = []
    for name in ("spinner", "spinner_faceon"):
        spin = load(name)
        rd, r, v = rl.range_doppler(spin)
        i = mover(rd, r, v, r_hi=2.0)[0]
        ln = lines(rd[i], v)
        pos = np.sort(ln[ln > 0])
        got.append((r2(r[i]), [r2(x) for x in pos], r2(np.mean(np.diff(np.r_[0.0, pos])))))
    expect("spinner and face-on: band range, lines above 0, spacing", got,
           [(0.47, [0.68, 1.36, 2.05, 2.73], 0.68), (0.47, [0.68], 0.68)])
    spin = load("spinner")
    k = int(np.argmin(np.abs(rl.range_axis(spin) - 0.47)))
    got = []
    for n_win in (64, 32):
        t, f, S = rl.spectrogram(spin, k, n_win=n_win, hop=n_win // 4)
        vel = f * lam / 2
        mean_db = 10 * np.log10(np.mean(10 ** (S / 10), axis=1))
        band = vel[mean_db - mean_db.max() > -10]
        got.append((r2(vel[1] - vel[0]), round(float((t[1] - t[0]) * 1e3)), r2(band.min()), r2(band.max())))
    expect("spectrogram at N_WIN 64, 32: cell, ms between columns, band", got,
           [(0.47, 8, -2.84, 2.84), (0.95, 4, -2.84, 2.84)])

    # The any-burst cell: a hand held still and one moved across the beam, at 0.8 m.
    got = []
    for name in ("hand_still", "hand_across"):
        burst = load(name)
        lv = []
        for kind in ("none", "2pulse", "3pulse"):
            rd, r, v = rl.range_doppler(rl.mti(burst, kind))
            near = np.abs(r - 0.8) <= (r[1] - r[0]) / 2
            lv.append(strongest(rd, r, v, r[near].min(), r[near].max(), -2.0, 2.0)[2])
        got.append((r1(lv[0]), r1(lv[1] - lv[0]), r1(lv[2] - lv[0])))
    expect("hand still, hand across: level, 2-pulse and 3-pulse change", got,
           [(-22.3, -58.3, -99.6), (-24.3, -33.4, -65.8)])
    return ok


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--out", type=Path, default=OUT, help="output directory")
    ap.add_argument("--check", action="store_true", help="assert the quoted numbers")
    args = ap.parse_args()
    for p in sim.l29_sets(args.out):
        print(f"wrote {p.relative_to(ROOT) if p.is_relative_to(ROOT) else p} "
              f"({p.stat().st_size / 1e6:.2f} MB)")
    if args.check:
        sys.exit(0 if check(args.out) else 1)


if __name__ == "__main__":
    main()
