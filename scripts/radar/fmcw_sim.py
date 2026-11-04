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
    fc      carrier, Hz (the app preset's, COURSE_SPEC section M8.1)
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
    add_spinner(cap, r0, ...)       a fidget spinner, edge-on: arms on a circle
    add_rotor(cap, r0, rho, ...)    any rotor, edge-on, its rate drifting or spinning down
    add_fan(cap, r0, ...)           a desk fan, edge-on: blades of points, hub to tip
    add_dismount(cap, t, x, y, ...) a person walking any path on the floor (L31)

A new target type is one more function that builds its scatterers' ranges as a
function of time and calls _add_scatterer for each. A new waveform is one more
entry in PRESETS. Every target takes an azimuth az (degrees, positive on the E8
side), which sets the phase between the two subarray channels: their centers
sit D_SUB = 4 x 14 mm apart, so a target at az puts k D_SUB sin(az) between
them. Each channel carries half the summed echo, so iq at broadside matches the
L25 budget, and half the noise power, so iq's noise is NOISE_DBFS.

    python3 scripts/radar/fmcw_sim.py               # the L28 and L29 sets
    python3 scripts/radar/fmcw_sim.py --out DIR     # somewhere else
    -> book/extras/radar-data/L28_*.npz, L29_*.npz
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
    # The L28 Lab range chirp: the Phaser app's Range (Basic) preset as it
    # ships (COURSE_SPEC M8.1), 500 MHz in 1 ms at 12.145 GHz, 0.6 MSPS:
    # 3.33 kHz of beat per meter, a 60 m reach above f0. l28_capture keeps
    # the 540 samples the app keeps of each chirp. One chirp is kept per
    # display update, so the PRI is the waterfall's line time, 50 ms.
    "l28_range": dict(fs=0.6e6, fc=12.145e9, B=500e6, T_ramp=1.0e-3,
                      PRI=50e-3, n_chirps=32, f0=101.4e3),
    # The L29-L31 range-Doppler burst: 256 chirps of 300 us, PRI 0.5 ms,
    # 4 MSPS (11.1 kHz per meter, CPI 128 ms; 1200 samples a chirp).
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


def add_spinner(cap: dict, r0: float = 0.5, radius: float = 0.03,
                rev_hz: float = 15.0, n_arms: int = 3, rcs_arm: float = 1e-3,
                rcs_hub: float = 0.02, az: float = 0.0) -> None:
    """A fidget spinner held edge-on, its plane of rotation along the line of sight.

    The hub, and the hand holding it, sit still at r0 (rcs_hub). n_arms
    equal weights turn on a circle of the given radius at rev_hz revolutions
    a second, so each arm's range swings radius cos(2 pi rev_hz t + 2 pi k /
    n_arms) about r0 and its radial speed reaches the tip speed 2 pi radius
    rev_hz either way: a band of Doppler out to +/- the tip speed, in lines
    n_arms rev_hz apart, since the arms are identical. A fan is the same
    target with more arms, a larger radius, and a slower turn.
    """
    _, t = _times(cap)
    _add_scatterer(cap, np.full_like(t, r0), echo_dbfs(cap, r0, rcs_hub), phase0=0.9, az=az)
    for k in range(n_arms):
        r_t = r0 + radius * np.cos(2 * np.pi * rev_hz * t + 2 * np.pi * k / n_arms)
        _add_scatterer(cap, r_t, echo_dbfs(cap, r_t, rcs_arm), az=az)


def add_rotor(cap: dict, r0: float, rho, rcs_pts, rpm: float, n_blades: int = 3,
              spin_down_s: float | None = None, wobble: float = 0.0, seed: int = 0,
              rcs_hub: float = 0.02, tilt: float = 0.0, phase0: float = 0.0,
              az: float = 0.0) -> None:
    """Any rotor seen edge-on: n_blades identical blades, each a set of points.

    rho (m) and rcs_pts (m^2) list one blade's points: their radii and their
    cross sections. The hub, and whatever holds the rotor, sits still at r0
    (rcs_hub). A point at radius rho turns through the rotor's angle theta(t),
    so its range swings rho cos(theta + 2 pi b / n_blades) about r0. Held
    tilt degrees off edge-on, only cos(tilt) of that swing lies along the
    line of sight: the Doppler band shrinks, but keeps its shape.

    A real rotor's rate is not constant. spin_down_s is the time constant of
    a free spin slowing down (a fidget spinner); wobble is the RMS fractional
    wander of a driven rotor's rate (a fan), slow next to a turn. Either keeps
    the spectrogram's fine structure from repeating exactly, as a recording
    of a real rotor does not. Added for the L31 Lab.
    """
    _, t = _times(cap)
    _add_scatterer(cap, np.full_like(t, r0), echo_dbfs(cap, r0, rcs_hub), phase0=0.9, az=az)
    # the turn rate, rev/s, on a fine grid, integrated to the angle
    tg = np.arange(0.0, t.max() + 2e-3, 1e-3)
    rate = np.full(tg.size, rpm / 60.0)
    if spin_down_s:
        rate = rate * np.exp(-tg / spin_down_s)
    if wobble:
        rng = np.random.default_rng(seed)
        w = np.convolve(rng.standard_normal(tg.size + 400), np.hanning(401), "valid")[:tg.size]
        rate = rate * (1 + wobble * w / w.std())
    theta = np.interp(t, tg, 2 * np.pi * np.cumsum(rate) * 1e-3) + phase0
    for b in range(n_blades):
        c = np.cos(theta + 2 * np.pi * b / n_blades)
        for rh, rcs in zip(np.atleast_1d(rho), np.atleast_1d(rcs_pts)):
            r_t = r0 + rh * np.cos(np.radians(tilt)) * c
            _add_scatterer(cap, r_t, echo_dbfs(cap, r_t, rcs), phase0=11.0 * rh, az=az)


def add_fan(cap: dict, r0: float = 1.0, radius: float = 0.075, rpm: float = 1000.0,
            n_blades: int = 3, n_pts: int = 25, rcs_blade: float = 0.01,
            rcs_stand: float = 0.05, wobble: float = 0.02, seed: int = 0,
            tilt: float = 0.0, az: float = 0.0) -> None:
    """A desk fan seen edge-on: n_blades blades, each a line of n_pts points.

    The points run evenly from the hub, 15 mm out, to the tip at radius, and
    share rcs_blade evenly, so a blade fills the Doppler band from zero out
    to the tip speed pi (2 radius) rpm / 60. That filled band sets a fan
    apart from a spinner, whose weight sits at its rim. The stand sits still
    at r0 (rcs_stand); the motor's rate wanders by wobble; tilt is as
    add_rotor's. Added for the L31 Lab.
    """
    rho = np.linspace(0.015, radius, n_pts)
    add_rotor(cap, r0, rho, np.full(n_pts, rcs_blade / n_pts), rpm, n_blades,
              wobble=wobble, seed=seed, rcs_hub=rcs_stand, tilt=tilt, az=az)


def add_dismount(cap: dict, t_path, x_path, y_path, stride_hz: float = 0.9,
                 rcs_body: float = 0.5, seed: int = 1) -> None:
    """A person walking along any path on the floor, with swinging limbs.

    The torso is at (x, y) m at the times t_path s, interpolated between them:
    y is straight out from the kit along its boresight, and x is to the side,
    positive on the E8 side (fmcw_sim's positive az). Range is hypot(x, y)
    and azimuth atan2(x, y), so a diagonal walk changes both, and the two
    subarray channels see the azimuth change. The limbs of add_walker swing
    along the direction of walking, so only the part of their swing along the
    line of sight shows as micro-Doppler, as for L26's walker at an aspect.
    A stretch with no motion has no heading; the limbs then hold still.
    Added for the L31 Lab's dismount track and its walker records.
    """
    _, t = _times(cap)
    tt = np.asarray(t_path, float)
    x = np.interp(t, tt, np.asarray(x_path, float))
    y = np.interp(t, tt, np.asarray(y_path, float))
    # heading: the unit vector of the walking direction, from the path itself
    dt = 1e-3
    hx = np.interp(t + dt, tt, x_path) - np.interp(t - dt, tt, x_path)
    hy = np.interp(t + dt, tt, y_path) - np.interp(t - dt, tt, y_path)
    hn = np.hypot(hx, hy)
    hx, hy = np.where(hn > 0, hx / np.maximum(hn, 1e-12), 0.0), np.where(hn > 0, hy / np.maximum(hn, 1e-12), 0.0)
    # Limb swing along the walk, m, and share of rcs. At a 1 Hz stride the legs
    # reach 2 pi (0.42) = 2.6 m/s about the torso, L26's walker (add_walker's
    # 0.25 m legs, written for the L28 waterfall, reach 1.6 m/s).
    limbs = [(0.42, 0.0, 0.08), (0.42, np.pi, 0.08),      # legs
             (0.25, np.pi, 0.04), (0.25, 0.0, 0.04)]      # arms, opposite legs
    rng = np.random.default_rng(seed)

    def scatter(px, py, rcs):
        r_t = np.hypot(px, py)
        az_t = np.degrees(np.arctan2(px, py))
        _add_scatterer(cap, r_t, echo_dbfs(cap, r_t, rcs), rng.uniform(0, 6.28), az_t)

    scatter(x, y, rcs_body)
    for swing, ph, share in limbs:
        s = swing * np.sin(2 * np.pi * stride_hz * t + ph)
        scatter(x + s * hx, y + s * hy, share * rcs_body)


def save(cap: dict, path: Path, note: str, channels: bool = True) -> Path:
    """Write a capture in the contract's .npz format: iq and iq_ch as complex64.

    channels=False leaves iq_ch out, halving the file; L29 captures do that
    to stay small (a 256-chirp burst is 2.5 MB with iq alone).
    """
    path.parent.mkdir(parents=True, exist_ok=True)
    extra = dict(iq_ch=cap["iq_ch"].astype(np.complex64)) if channels else {}
    np.savez(path, iq=iq(cap).astype(np.complex64), **extra,
             fs=cap["fs"], fc=cap["fc"], B=cap["B"], T_ramp=cap["T_ramp"],
             PRI=cap["PRI"], f0=cap["f0"], note=np.str_(note))
    return path


def room(cap: dict) -> None:
    """What every bench capture holds besides the target: noise, leakage, a wall."""
    add_noise(cap, seed=int(cap["n_chirps"]))
    add_leakage(cap)
    add_point(cap, 5.5, rcs=2.0, phase0=0.4)       # the far wall, weak and fixed


# The L28 Lab's kit and bench. The app keeps the last 90% of each chirp, after
# the ramp settles (phaser_radar_dsp.chirp_plan, RAMP_SETTLE_FRACTION): 540
# of the 600 samples of a 1 ms chirp. A capture saved before the 0 m
# calibration carries the IF tone, 100 kHz, as its f0, as the app writes it;
# one saved after it carries the kit's 101.4 kHz. The tape is read with the
# few-centimeter errors of a real bench, so a fitted slope is not exact.
L28_IF_TONE = 100e3
L28_SETTLE = 0.1
L28_TAPE = {1: 0.99, 2: 2.01, 3: 3.03}          # tape range -> true range, m
L28_CORNER_RCS = 0.47 * (12.145 / 10.0) ** 2    # the 10 cm corner at 12.145 GHz
L28_FAST = dict(fs=5.0e6, fc=10.0e9, T_ramp=0.5e-3)   # the app's Range (Fast)


def l28_capture(**overrides) -> dict:
    """An empty L28 capture, trimmed to the samples the app keeps of each chirp."""
    cap = new_capture("l28_range", **overrides)
    ramp = cap["T_ramp"]
    n = int((ramp - L28_SETTLE * ramp) * cap["fs"])      # chirp_plan's arithmetic
    cap["iq_ch"] = np.zeros(cap["iq_ch"].shape[:2] + (n,), dtype=np.complex128)
    return cap


def l28_sets(out: Path = OUT) -> list[Path]:
    """The L28 Lab's recorded data, at the app's Range (Basic) preset unless named."""
    written = []
    basic = "Range (Basic): 12.145 GHz, B 500 MHz, T_ramp 1 ms, 0.6 MSPS"

    def write(cap, name, note, f0_field=None):
        if f0_field is not None:
            cap["f0"] = f0_field
        written.append(save(cap, out / name, f"L28 Lab recorded data: {note}", channels=False))

    cap = l28_capture()
    room(cap)
    write(cap, "L28_clear.npz", f"the bench clear, before the 0 m calibration (f0 is the IF tone); {basic}",
          L28_IF_TONE)

    cap = l28_capture()
    room(cap)
    add_point(cap, 0.02, level_dbfs=-8.0, phase0=2.0)  # plate against the array
    write(cap, "L28_cal_0m.npz", "a metal plate held against the array, before the 0 m calibration "
          f"(f0 is the IF tone); {basic}", L28_IF_TONE)

    for tape, r in L28_TAPE.items():
        cap = l28_capture()
        room(cap)
        add_point(cap, r, rcs=L28_CORNER_RCS)
        write(cap, f"L28_corner_{tape}m.npz", f"a 10 cm corner reflector at {tape:.2f} m by the tape; {basic}")

    for name, kw, words in (
            ("L28_corner_2m_fast.npz", L28_FAST,
             "the corner at 2.00 m by the tape, Range (Fast): 10 GHz, B 500 MHz, T_ramp 0.5 ms, 5 MSPS"),
            ("L28_corner_2m_B250.npz", dict(B=250e6),
             "the corner at 2.00 m by the tape, B 250 MHz; otherwise Range (Basic)")):
        cap = l28_capture(**kw)
        room(cap)
        add_point(cap, L28_TAPE[2], rcs=L28_CORNER_RCS * (cap["fc"] / 12.145e9) ** 2)
        write(cap, name, words)

    cap = l28_capture()
    room(cap)
    add_point(cap, 2.0, rcs=L28_CORNER_RCS)
    add_point(cap, 2.2, rcs=L28_CORNER_RCS, phase0=0.4)   # in phase: one peak midway
    write(cap, "L28_two_corners.npz", f"two corners at 2.0 and 2.2 m, inside one resolution cell; {basic}")

    cap = l28_capture(n_chirps=200)    # 10 s at 50 ms a line
    room(cap)
    add_walker(cap, r_start=1.0, r_turn=4.0, speed=1.0)
    write(cap, "L28_walker.npz", f"a person walking from 1 m out to 4 m and back, at 1 m/s, for 10 s; {basic}")
    return written


# The L29 Lab's scene: the room, plus a wall 2.5 m in front of the kit, the
# strong static return the MTI procedure removes. The hand speeds are the
# lesson's 1.0 m/s closing (-13.6 dB through the 2-pulse canceller) and a
# 1.5 m/s opening; the spinner's tip speed is 2 pi (0.03 m)(15 rev/s) = 2.83 m/s.
L29_WALL = dict(r0=2.5, rcs=5.0, phase0=2.6)
L29_HAND_CLOSE = dict(r0=1.0, v=+1.0, rcs=0.02, phase0=1.3)
L29_HAND_OPEN = dict(r0=0.7, v=-1.5, rcs=0.02, phase0=1.3)
L29_SPINNER = dict(r0=0.5, radius=0.03, rev_hz=15.0, n_arms=3)


def l29_room(cap: dict) -> None:
    """The L28 room plus the L29 wall."""
    room(cap)
    add_point(cap, **L29_WALL)


def l29_sets(out: Path = OUT) -> list[Path]:
    """The L29 Lab's recorded data: 256-chirp bursts, iq only, about 2.5 MB each."""
    written = []
    burst = "256 chirps of 300 us every 0.5 ms, 4 MSPS"

    cap = new_capture("l29_burst")
    l29_room(cap)
    written.append(save(cap, out / "L29_static.npz",
                        f"L29 Lab recorded data: no mover, the leakage and a wall at 2.5 m; {burst}, B 500 MHz",
                        channels=False))

    for tag, kw, words in (("closing", L29_HAND_CLOSE, "from 1.0 m toward the kit at 1.0 m/s"),
                           ("opening", L29_HAND_OPEN, "from 0.7 m away from the kit at 1.5 m/s")):
        cap = new_capture("l29_burst")
        l29_room(cap)
        add_point(cap, **kw)
        written.append(save(cap, out / f"L29_hand_{tag}.npz",
                            f"L29 Lab recorded data: a hand moving {words}, the wall at 2.5 m; {burst}, B 500 MHz",
                            channels=False))

    cap = new_capture("l29_burst", B=200e6)
    l29_room(cap)
    add_point(cap, **L29_HAND_CLOSE)
    written.append(save(cap, out / "L29_hand_closing_B200.npz",
                        f"L29 Lab recorded data: the closing hand at B 200 MHz; {burst}",
                        channels=False))

    cap = new_capture("l29_burst")
    l29_room(cap)
    add_spinner(cap, **L29_SPINNER)
    written.append(save(cap, out / "L29_spinner.npz",
                        "L29 Lab recorded data: a fidget spinner held edge-on at 0.5 m, three arms on a "
                        f"3 cm radius at 15 rev/s; {burst}, B 500 MHz", channels=False))
    return written


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--out", type=Path, default=OUT, help="output directory")
    args = ap.parse_args()
    for p in l28_sets(args.out) + l29_sets(args.out):
        print(f"wrote {p.relative_to(ROOT) if p.is_relative_to(ROOT) else p} "
              f"({p.stat().st_size / 1e3:.0f} kB)")


if __name__ == "__main__":
    main()
