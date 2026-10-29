#!/usr/bin/env python3
"""Simulated ADALM-PHASER FMCW captures, in the course's .npz capture format.

The recorded-data fallback for the L28-L31 Labs: when a bench capture fails, a
cadet loads one of these instead and runs the same code on it. Every capture is
a dict with the keys of the course contract (ROADMAP section 5, the L28 brief):

    iq      complex64, shape (n_chirps, n_samples): the beat signal of the
            summed array, one chirp a row, in full-scale units (|iq| = 1 is
            0 dBFS). n_chirps is not fixed: 32 for an L28 range capture, 256
            for a range-Doppler burst, thousands for a classification record
    iq_ch   (optional) complex64, shape (2, n_chirps, n_samples): the two
            subarray channels, whose sum is iq; the L31 monopulse needs them
    fs      sample rate, Hz
    fc      carrier, Hz (10 GHz, COURSE_SPEC section M8)
    B       chirp bandwidth, Hz
    T_ramp  chirp length, s
    PRI     time from the start of one chirp to the start of the next, s
    f0      the 0 m frequency, Hz: where an echo from zero range lands
    note    (extra) one line saying what is in the capture

A target at range R puts a tone in each chirp at f0 + 2RB/(c T_ramp), the echo
compared with the chirp still going out, with a carrier phase of -4 pi R / lambda
that advances from chirp to chirp as the target moves (L26's Doppler sign: an
approaching target has a positive Doppler shift). Echo levels follow the L25
link budget (25 uW, 6 + 15 dBi, 2 dB noise figure), referred to a noise floor
of NOISE_DBFS per sample, so the per-bin SNR a cadet measures on the recorded
data is the one the L25 budget and the L28 lesson predict.

One function per target type, each adding its echo to a capture in place:

    add_noise(cap)                  receiver noise
    add_leakage(cap)                transmit-to-receive leakage, the 0 m spike
    add_point(cap, r0, v, rcs, az)  a point target: plate, corner, wall (v > 0 closing)
    add_hand(cap, r0, ...)          a hand moving back and forth
    add_walker(cap, r_start, ...)   a person walking out and back, with limbs

A new target type is one more function that builds its scatterers' ranges as a
function of time and calls _add_scatterer for each. A new waveform is one more
entry in PRESETS. Every target takes an azimuth az (degrees, positive on the E8
side), which sets the phase between the two subarray channels: their centers
sit D_SUB = 4 x 14 mm apart, so a target at az puts k D_SUB sin(az) between
them. Each channel carries half the summed echo, so iq at broadside matches the
L25 budget, and half the noise power, so iq's noise is NOISE_DBFS.

    python3 scripts/radar/fmcw_sim.py               # the L28 sets
    python3 scripts/radar/fmcw_sim.py --out DIR     # somewhere else
    -> book/extras/radar-data/L28_*.npz
"""

from __future__ import annotations

import argparse
from pathlib import Path

import numpy as np

C = 3.00e8                      # m/s, as on the course pages
ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "book/extras/radar-data"

# Waveforms, from COURSE_SPEC section M8. f0 is a kit's calibrated 0 m
# frequency: "about 100 kHz, set per kit"; the recorded kit read 101.4 kHz.
PRESETS = {
    # The L28 Lab range chirp: 500 MHz in 0.5 ms, 6.67 kHz of beat per meter.
    # 0.6 MSPS is ADI's FMCW_RADAR_Waterfall.py rate (300 samples a chirp,
    # a 30 m reach above f0). One chirp is kept per display update, so the
    # PRI is the waterfall's line time, not the chirp length.
    "l28_range": dict(fs=0.6e6, fc=10.0e9, B=500e6, T_ramp=0.5e-3,
                      PRI=50e-3, n_chirps=32, f0=101.4e3),
    # The L29-L31 range-Doppler burst: 256 chirps of 300 us, PRI 0.5 ms,
    # 4 MSPS (11.1 kHz per meter, CPI 128 ms). Provisional until the L29 pass.
    "l29_burst": dict(fs=4.0e6, fc=10.0e9, B=500e6, T_ramp=300e-6,
                      PRI=0.5e-3, n_chirps=256, f0=101.4e3),
}

# The L25 link budget, so echo levels track the lesson's numbers.
PT_DBM = -16.0                  # transmit power, ADI's hardware page
GTGR_DB = 6.0 + 15.0            # transmit antenna + the 8-element array
NF_DB = 2.0                     # receiver noise figure
NOISE_DBFS = -60.0              # receiver noise per complex sample, summed array
D_SUB = 4 * 14e-3               # m: between the two 4-element subarray centers
R_MIN = 0.3                     # m: the echo level stops growing inside this


def new_capture(preset: str = "l28_range", **overrides) -> dict:
    """An empty capture for a waveform in PRESETS; any field may be overridden."""
    cap = dict(PRESETS[preset])
    cap.update(overrides)
    n_samp = int(round(cap["fs"] * cap["T_ramp"]))
    cap["iq_ch"] = np.zeros((2, cap["n_chirps"], n_samp), dtype=np.complex128)
    cap["note"] = ""
    return cap


def iq(cap: dict) -> np.ndarray:
    """The summed array, n_chirps x n_samples: the contract's iq."""
    return cap["iq_ch"].sum(axis=0)


def _times(cap: dict) -> tuple[np.ndarray, np.ndarray]:
    """Fast time within each chirp and absolute time, both (n_chirps, n_samples)."""
    _, n_chirp, n_samp = cap["iq_ch"].shape
    t_fast = np.arange(n_samp) / cap["fs"]
    t_slow = np.arange(n_chirp) * cap["PRI"]
    return np.broadcast_to(t_fast, (n_chirp, n_samp)), t_slow[:, None] + t_fast


def echo_dbfs(cap: dict, r: np.ndarray | float, rcs: float) -> np.ndarray:
    """Per-sample echo level from the radar equation, referred to NOISE_DBFS."""
    r = np.maximum(r, R_MIN)
    lam = C / cap["fc"]
    pr_dbm = (PT_DBM + GTGR_DB + 10 * np.log10(lam**2 * rcs)
              - 30 * np.log10(4 * np.pi) - 40 * np.log10(r))
    noise_dbm = -174.0 + 10 * np.log10(cap["fs"]) + NF_DB
    return NOISE_DBFS + pr_dbm - noise_dbm


def _add_scatterer(cap: dict, r_t: np.ndarray, level_dbfs, phase0: float = 0.0,
                   az: float = 0.0) -> None:
    """Add the beat tone of one scatterer whose range is r_t(fast, slow), at az deg."""
    t_fast, _ = _times(cap)
    slope = cap["B"] / cap["T_ramp"]
    f_beat = cap["f0"] + 2 * r_t * slope / C
    phase = 2 * np.pi * f_beat * t_fast - 4 * np.pi * r_t * cap["fc"] / C + phase0
    x = 0.5 * 10 ** (np.asarray(level_dbfs) / 20) * np.exp(1j * phase)
    dpsi = 2 * np.pi * cap["fc"] / C * D_SUB * np.sin(np.radians(az))
    cap["iq_ch"][0] += x * np.exp(-0.5j * dpsi)
    cap["iq_ch"][1] += x * np.exp(+0.5j * dpsi)


def add_noise(cap: dict, level_dbfs: float = NOISE_DBFS, seed: int = 0) -> None:
    """Complex Gaussian receiver noise, level_dbfs per sample."""
    rng = np.random.default_rng(seed)
    sigma = 10 ** (level_dbfs / 20) / 2          # per channel, per part: half the power each
    shape = cap["iq_ch"].shape
    cap["iq_ch"] += sigma * (rng.standard_normal(shape) + 1j * rng.standard_normal(shape))


def add_leakage(cap: dict, level_dbfs: float = -20.0) -> None:
    """The transmit antenna's direct path into the array: a fixed tone at f0."""
    _add_scatterer(cap, np.zeros(cap["iq_ch"].shape[1:]), level_dbfs, phase0=0.7)


def add_point(cap: dict, r0: float, v: float = 0.0, rcs: float = 0.47,
              level_dbfs: float | None = None, phase0: float = 0.0,
              az: float = 0.0) -> None:
    """A point target starting at r0 m, of radar cross section rcs m^2, at az deg.

    v is the radial velocity in m/s, positive closing (toward the radar), the
    course convention of L26: a closing target has a positive Doppler shift.

    rcs 0.47 m^2 is the course's 10 cm corner reflector at 10 GHz (M8). Pass
    level_dbfs to set the echo level directly, as for a plate held against
    the array, where the far-field radar equation does not apply.
    """
    _, t = _times(cap)
    r_t = r0 - v * t
    lvl = echo_dbfs(cap, r_t, rcs) if level_dbfs is None else level_dbfs
    _add_scatterer(cap, r_t, lvl, phase0, az)


def add_hand(cap: dict, r0: float = 0.6, swing: float = 0.15,
             rate_hz: float = 1.0, rcs: float = 0.02, az: float = 0.0) -> None:
    """A hand moving toward and away from the array, sinusoidally.

    r0: mean range, m; swing: peak excursion, m; rate_hz: back-and-forth rate.
    """
    _, t = _times(cap)
    r_t = r0 + swing * np.sin(2 * np.pi * rate_hz * t)
    _add_scatterer(cap, r_t, echo_dbfs(cap, r_t, rcs), phase0=1.3, az=az)


def add_walker(cap: dict, r_start: float = 1.0, r_turn: float = 4.0,
               speed: float = 1.0, stride_hz: float = 0.9,
               rcs_body: float = 0.5, az: float = 0.0, seed: int = 1) -> None:
    """A person walking straight out from r_start to r_turn and back, at speed m/s.

    The torso carries most of the echo. Two legs and two arms swing about it at
    the stride rate, half a cycle apart, so their ranges oscillate around the
    torso's: the micro-Doppler the L29 and L31 Labs look for.
    """
    _, t = _times(cap)
    leg = 2 * (r_turn - r_start) / speed           # one out-and-back, s
    s = np.mod(t, leg) / leg
    r_torso = r_start + (r_turn - r_start) * (1 - np.abs(2 * s - 1))
    # Limb swing: peak excursion along the line of sight, m, and share of rcs.
    limbs = [(0.25, 0.0, 0.08), (0.25, np.pi, 0.08),      # legs
             (0.15, np.pi, 0.04), (0.15, 0.0, 0.04)]      # arms, opposite legs
    rng = np.random.default_rng(seed)
    _add_scatterer(cap, r_torso, echo_dbfs(cap, r_torso, rcs_body), rng.uniform(0, 6.28), az)
    for swing, ph, share in limbs:
        r_t = r_torso + swing * np.sin(2 * np.pi * stride_hz * t + ph)
        _add_scatterer(cap, r_t, echo_dbfs(cap, r_t, share * rcs_body),
                       rng.uniform(0, 6.28), az)


def save(cap: dict, path: Path, note: str) -> Path:
    """Write a capture in the contract's .npz format: iq and iq_ch as complex64."""
    path.parent.mkdir(parents=True, exist_ok=True)
    np.savez(path, iq=iq(cap).astype(np.complex64),
             iq_ch=cap["iq_ch"].astype(np.complex64),
             fs=cap["fs"], fc=cap["fc"], B=cap["B"], T_ramp=cap["T_ramp"],
             PRI=cap["PRI"], f0=cap["f0"], note=np.str_(note))
    return path


def room(cap: dict) -> None:
    """What every bench capture holds besides the target: noise, leakage, a wall."""
    add_noise(cap, seed=int(cap["n_chirps"]))
    add_leakage(cap)
    add_point(cap, 5.5, rcs=2.0, phase0=0.4)       # the far wall, weak and fixed


def l28_sets(out: Path = OUT) -> list[Path]:
    """The L28 Lab's recorded data: calibration, three static ranges, two waveforms, two close corners, a walker."""
    written = []

    cap = new_capture("l28_range")
    room(cap)
    add_point(cap, 0.02, level_dbfs=-8.0, phase0=2.0)  # plate against the array
    written.append(save(cap, out / "L28_cal_0m.npz",
                        "L28 Lab recorded data: a metal plate held against the array, for the 0 m calibration"))

    for r in (1.0, 2.0, 3.0):
        cap = new_capture("l28_range")
        room(cap)
        add_point(cap, r, rcs=0.47)
        written.append(save(cap, out / f"L28_corner_{r:.0f}m.npz",
                            f"L28 Lab recorded data: a 10 cm corner reflector at {r:.1f} m, B 500 MHz, T_ramp 0.5 ms"))

    for tag, kw in (("B250", dict(B=250e6)), ("T1ms", dict(T_ramp=1.0e-3))):
        cap = new_capture("l28_range", **kw)
        room(cap)
        add_point(cap, 2.0, rcs=0.47)
        written.append(save(cap, out / f"L28_corner_2m_{tag}.npz",
                            f"L28 Lab recorded data: the corner at 2.0 m, B {cap['B']/1e6:.0f} MHz, "
                            f"T_ramp {cap['T_ramp']*1e3:.1f} ms"))

    cap = new_capture("l28_range")
    room(cap)
    add_point(cap, 2.0, rcs=0.47)
    add_point(cap, 2.2, rcs=0.47, phase0=1.9)
    written.append(save(cap, out / "L28_two_corners.npz",
                        "L28 Lab recorded data: two corners at 2.0 and 2.2 m, inside one 0.30 m resolution cell"))

    cap = new_capture("l28_range", n_chirps=200)    # 10 s at 50 ms a line
    room(cap)
    add_walker(cap, r_start=1.0, r_turn=4.0, speed=1.0)
    written.append(save(cap, out / "L28_walker.npz",
                        "L28 Lab recorded data: a person walking from 1 m out to 4 m and back, at 1 m/s, for 10 s"))
    return written


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--out", type=Path, default=OUT, help="output directory")
    args = ap.parse_args()
    for p in l28_sets(args.out):
        print(f"wrote {p.relative_to(ROOT) if p.is_relative_to(ROOT) else p} "
              f"({p.stat().st_size / 1e3:.0f} kB)")


if __name__ == "__main__":
    main()
