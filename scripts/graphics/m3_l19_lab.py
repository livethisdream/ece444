#!/usr/bin/env python3
"""Generate the L19 (Beam Steering Lab) figures as inline SVG.

  - L19-sweep-compare   : two beam-sweep traces, source at 0 and at +30 deg,
                          sampled where the instrument samples them
  - L19-expected-sweep  : the same pair, annotated with what the bench measures
  - L19-phase-ramp      : the 30 deg ramp, unwrapped and wrapped, beside what
                          Phase Control shows after Apply 30
  - L19-bench-setup     : top view of the bench, 1 m arc, 0 / 30 / 45 deg
  - L19-two-ways        : rotating the array versus sweeping the command
  - L19-error-budget    : the three error sources at 30 deg and their RSS

Every figure goes to book/extras/viz/img/ (the lesson page) only. The reveal.js
decks are frozen (2026-10-10), so this script does not touch the deck's own
copies in book/extras/slides/fig/L19-*.svg; those were written by the previous
version of this file (see git history) and stay byte-identical.

The page figures sit in a present block beside text: about 477 px wide at a
1280 laptop and 343 px on a phone. They are drawn about 420 units wide with no
text under 13 units, so the smallest label is 10.5 px or more on the phone;
check_text() asserts it on the written file (L18's rule).

How the instrument samples. Lab Preset 1 turns Use Bits on (ignore_res) and
sets Signal BW to 10 MHz. do_sweep() then steps the per-element phase delta
one 2.8125 deg ADAR1000 LSB at a time, from -227.8125 to +225 deg, and plots
each step at the angle ConvertPhaseToSteerAngle() gives it, computed at
Signal Freq - BW with the GUI's c = 299792458 and its truncated 3.14159
(phaser_headless.py, do_sweep and ConvertPhaseToSteerAngle). So the samples
are one LSB of PHASE apart: 0.91 deg of angle at broadside, 1.05 at 30, 1.29
at 45 -- not 2.8125 deg of angle. sweep_axis() below is that conversion.

What the trace is. With the source fixed at theta_s, the power at sweep step
dphi is EF(theta_s) |AF|^2 with psi = kd sin(theta_s) - dphi. The array
factor alone moves; the element pattern is evaluated once, at the source, so
moving the source drops the whole trace by a constant EF(theta_s)/EF(0) --
the scan loss belongs to the element pattern (L18 "Scan Loss"), drawn here at
the ideal-element bound cos(theta) (COURSE_SPEC M4). The sweep's noise floor
sits about 23 dB below the uniform peak; the trace is clamped there.

What Phase Control shows. Beam Steering -> Apply writes
round(k * phDeltaDeg), phDeltaDeg = -(360 d sin(theta) f / c), c = 299792458,
into Phase Control: negated, unwrapped, whole degrees (frontend/src/main.js,
the btn-apply-steer handler). JavaScript's Math.round rounds half up.

Every number a figure shows is computed here and asserted against the value
the page prints, so the two cannot drift apart.

    python3 scripts/graphics/m3_l19_lab.py
"""

from __future__ import annotations

import io
import math
import re
from pathlib import Path
from svg_font_stack import apply_font_stack

import numpy as np
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
from matplotlib.patches import Arc, FancyArrowPatch, Polygon, Rectangle  # noqa: E402

NAVY, BLUE, RED, GREEN, AMBER, GRAY = "#004a85", "#0067b9", "#b01e24", "#1d7a4d", "#8a5a00", "#5a5a5a"
INK, RULE, LIGHT = "#1a1a1a", "#c7d2e0", "#9fb1c2"

ROOT = Path(__file__).resolve().parents[2]
IMG = ROOT / "book/extras/viz/img"

# The course array and the HB100's nominal frequency.
N, D, FREQ = 8, 0.014, 10.525e9
C_COURSE = 3e8                         # the course's c: lambda = 28.50 mm, dphi = 88.4
LAM = C_COURSE / FREQ
KD_DEG = 360.0 * D / LAM               # 176.8 deg of phase per unit of sin(theta)

# The GUI's own constants (phaser_headless.py, main.js).
C_GUI, STEER_PI = 299792458.0, 3.14159
LSB = 2.8125                           # 7-bit ADAR1000 phase step
BW_HZ = 10e6                           # Lab Preset 1: Signal BW 10 MHz
M_STEPS = np.arange(-81, 81)           # PhaseValues = arange(-227.8125, 227.8125, LSB)
FLOOR_DB = -23.0                       # sweep noise floor below the uniform peak

PHONE_COL, PX_MIN = 343.0, 10.5

plt.rcParams.update(
    {
        "svg.fonttype": "none",
        "svg.hashsalt": "ece444-L19",    # stable clip-path ids: deterministic output
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
    """Every label on a page figure is 10.5 px or more at a 343 px column."""
    vb = re.search(r'viewBox="0 0 ([\d.]+) ([\d.]+)"', svg)
    w = float(vb.group(1))
    sizes = [float(x) for x in re.findall(r"font-size:\s*([\d.]+)px", svg)]
    smallest = min(sizes) * PHONE_COL / w
    print(f"   {name}: viewBox {w:.0f} x {float(vb.group(2)):.0f}, smallest text "
          f"{min(sizes):.1f} units = {smallest:.1f} px at a {PHONE_COL:.0f} px column")
    assert smallest >= PX_MIN - 0.05, f"{name}: {smallest:.2f} px text on a phone"
    assert "\u2009" not in svg, f"{name}: thin space"


def finalize(fig, name: str) -> None:
    buf = io.StringIO()
    fig.savefig(buf, format="svg", transparent=True, bbox_inches="tight", pad_inches=0.06,
                metadata={"Date": None})
    plt.close(fig)
    s = buf.getvalue()
    s = s[s.index("<svg"):]
    s = apply_font_stack(s)
    check_text(name, s)
    (IMG / f"{name}.svg").write_text(s, encoding="utf-8")
    print(f"wrote {IMG / (name + '.svg')}")


def clean(ax):
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)


# ------------------------------------------------------------------ physics
def sweep_axis(dphi_deg):
    """ConvertPhaseToSteerAngle(dphi, SignalFreq - BW), vectorized: the angle
    the GUI plots a sweep step at."""
    dphi_deg = np.asarray(dphi_deg, dtype=float)
    f_calc = FREQ - BW_HZ
    v = C_GUI * np.radians(np.abs(dphi_deg)) / (2 * STEER_PI * f_calc * D)
    return np.sign(dphi_deg) * np.degrees(np.arcsin(np.clip(v, -1.0, 1.0)))


def af2(dphi_deg, source_deg):
    """|AF|^2 at sweep step dphi for a source at source_deg (real physics:
    exact c, real pi), normalized to unity peak."""
    kd = 360.0 * D * FREQ / C_GUI
    psi = np.radians(kd * np.sin(np.radians(source_deg)) - np.asarray(dphi_deg, dtype=float))
    num = np.sin(N * psi / 2.0)
    den = N * np.sin(psi / 2.0)
    with np.errstate(divide="ignore", invalid="ignore"):
        r = np.where(np.abs(den) < 1e-12, 1.0, num / den)
    return r ** 2


def ef(theta_deg):
    """Element power pattern at the ideal-element bound (COURSE_SPEC M4)."""
    return np.cos(np.radians(theta_deg))


def trace_db(dphi_deg, source_deg):
    """The sweep trace: EF at the source times |AF|^2, clamped at the floor."""
    db = 10 * np.log10(np.clip(ef(source_deg) * af2(dphi_deg, source_deg), 1e-12, None))
    return np.maximum(db, FLOOR_DB)


def bisect(fn, lo, hi, n=80):
    flo = fn(lo)
    for _ in range(n):
        mid = 0.5 * (lo + hi)
        if (fn(mid) > 0) == (flo > 0):
            lo, flo = mid, fn(mid)
        else:
            hi = mid
    return 0.5 * (lo + hi)


def peak_dphi(source_deg):
    return 360.0 * D * FREQ / C_GUI * np.sin(np.radians(source_deg))


def hpbw_on_axis(source_deg):
    """Half-power crossings of the trace, read on the GUI's angle axis."""
    p0 = peak_dphi(source_deg)
    g = lambda p: af2(p, source_deg) - 0.5
    lo = sweep_axis(bisect(g, p0 - 40, p0))
    hi = sweep_axis(bisect(g, p0, p0 + 40))
    return float(lo), float(hi)


def first_sidelobes(source_deg):
    """The two first-sidelobe peaks: (axis angle, dB below the trace's peak)."""
    p0 = peak_dphi(source_deg)
    out = []
    for s in (-1, 1):
        ps = p0 + s * np.linspace(30, 90, 60001)
        a = af2(ps, source_deg)
        # past the first null, the first local maximum
        i0 = int(np.argmin(a[: len(a) // 2]))
        j = i0 + int(np.argmax(a[i0:]))
        out.append((float(sweep_axis(ps[j])), float(10 * np.log10(a[j]))))
    return out


def samples(source_deg):
    ph = M_STEPS * LSB
    x = sweep_axis(ph)
    keep = np.abs(x) < 89.999            # the steps past endfire pile up at +/-90
    return x[keep], trace_db(ph[keep], source_deg)


def curve(source_deg, n=8001):
    ph = np.linspace(M_STEPS[0] * LSB, M_STEPS[-1] * LSB, n)
    x = sweep_axis(ph)
    keep = np.abs(x) < 89.999
    return x[keep], trace_db(ph[keep], source_deg)


def grid_step_at(theta_deg):
    """Spacing of the two sweep samples either side of theta_deg."""
    x = sweep_axis(M_STEPS * LSB)
    i = int(np.searchsorted(x, theta_deg))
    return float(x[i] - x[i - 1])


def phase_control(theta_deg):
    """What Apply writes into Phase Control (main.js, btn-apply-steer)."""
    ph = -(360 * D * math.sin(math.radians(theta_deg)) * FREQ / C_GUI)
    return [int(math.floor(k * ph + 0.5)) for k in range(N)]    # JS Math.round


# ----------------------------------------------------------- shared checks
def check_numbers():
    assert round(LAM * 1e3, 2) == 28.50 and round(D / LAM, 3) == 0.491
    assert round(KD_DEG, 1) == 176.8
    for t, v in ((0, 0.0), (15, 45.8), (30, 88.4), (45, 125.0)):
        assert round(KD_DEG * math.sin(math.radians(t)), 1) == v
    # the sweep grid, one LSB of phase per sample
    x = sweep_axis(M_STEPS * LSB)
    assert len(x) == 162 and int(np.sum(np.abs(x) >= 89.999)) == 37
    assert round(grid_step_at(0.0), 2) == 0.91
    assert round(grid_step_at(30.0), 2) == 1.05
    assert round(grid_step_at(45.0), 2) == 1.29
    # the samples either side of 30 deg (the audit's check values)
    i = int(np.searchsorted(x, 30.0))
    assert np.allclose(np.round(x[i - 1:i + 1], 2), [29.55, 30.61]), x[i - 1:i + 2]
    # half a step at 30 deg: the error budget's grid bar
    assert round(grid_step_at(30.0) / 2, 2) == 0.53
    # Phase Control after Apply 30 and Apply 45
    assert phase_control(30) == [0, -88, -177, -265, -354, -442, -531, -619]
    assert phase_control(45) == [0, -125, -250, -375, -500, -626, -751, -876]
    # HPBW on the trace, and the first sidelobe
    for t, w in ((0, 13.0), (30, 15.1)):
        lo, hi = hpbw_on_axis(t)
        assert round(hi - lo, 1) == w, (t, hi - lo)
    # at 45 the exact array factor gives 18.7; the GUI's axis (phases computed
    # at Signal Freq - 10 MHz) stretches it to 18.76, still 18.7-18.8
    lo, hi = hpbw_on_axis(45)
    assert 18.7 <= hi - lo < 18.8, hi - lo
    for t in (0, 30):
        for _, lev in first_sidelobes(t):
            assert round(lev, 1) == -12.8, lev
    assert round(10 * math.log10(ef(30)), 1) == -0.6
    assert round(10 * math.log10(ef(45)), 1) == -1.5


# --------------------------------------------------------------------------- 1
def sweep_compare() -> None:
    """The measurement: one beam traced twice, the source moved between."""
    fig, ax = plt.subplots(figsize=(5.9, 3.0))
    for src, col in ((0.0, NAVY), (30.0, AMBER)):
        x, y = curve(src)
        ax.plot(x, y, color=col, lw=1.3, alpha=0.55, zorder=2)
        xs, ys = samples(src)
        ax.plot(xs, ys, ls="none", marker="o", ms=2.6, color=col, zorder=3)

    ax.axhline(FLOOR_DB, color=GRAY, lw=1.0, ls=(0, (5, 4)), zorder=1)
    ax.text(-58, FLOOR_DB - 1.0, "noise floor", fontsize=13, color=GRAY, va="top")
    ax.text(-4.0, 1.0, "source at 0°", fontsize=13, color=NAVY, ha="right", va="bottom")
    ax.text(34.0, 0.4, "source at +30°", fontsize=13, color=AMBER, ha="left", va="bottom")

    ax.set_xlim(-60, 60)
    ax.set_ylim(-29, 4)
    ax.set_xticks(range(-60, 61, 30))
    ax.set_xticklabels(["−60", "−30", "0", "30", "60"])
    ax.set_yticks([-20, -10, 0])
    ax.set_yticklabels(["−20", "−10", "0"])
    ax.set_xlabel("sweep steering angle (deg)")
    ax.set_ylabel("power (dB)")
    ax.grid(color=RULE, lw=0.7, alpha=0.7)
    ax.set_axisbelow(True)
    clean(ax)
    finalize(fig, "L19-sweep-compare")


# --------------------------------------------------------------------------- 2
def expected_sweep() -> None:
    """The pair again, marked with what the bench reads: the two half-power
    spans, the first sidelobes, the element-pattern drop on the moved trace,
    the sample spacing, and the floor."""
    fig, ax = plt.subplots(figsize=(5.9, 3.5))
    spans = {}
    for src, col in ((0.0, NAVY), (30.0, AMBER)):
        x, y = curve(src)
        ax.plot(x, y, color=col, lw=1.3, alpha=0.55, zorder=2)
        xs, ys = samples(src)
        ax.plot(xs, ys, ls="none", marker="o", ms=2.8, color=col, zorder=3)
        spans[src] = hpbw_on_axis(src)

    drop = 10 * math.log10(ef(30.0))
    # the half-power spans, each at 3 dB below its own trace's peak
    for src, col in ((0.0, NAVY), (30.0, AMBER)):
        lo, hi = spans[src]
        yb = -3.0 + (drop if src else 0.0)
        ax.annotate("", xy=(hi, yb), xytext=(lo, yb), zorder=4,
                    arrowprops=dict(arrowstyle="<|-|>", color=GREEN, lw=1.5,
                                    shrinkA=0, shrinkB=0, mutation_scale=9))
        ax.text((lo + hi) / 2, yb - 1.0, f"{hi - lo:.1f}°", color=GREEN, fontsize=13,
                ha="center", va="top", zorder=5)

    # first sidelobes: a tick on each, one label
    for src, col in ((0.0, NAVY), (30.0, AMBER)):
        off = drop if src else 0.0
        for xa, lev in first_sidelobes(src):
            if -40 < xa < 70:
                ax.plot([xa - 3, xa + 3], [lev + off, lev + off], color=RED, lw=1.8, zorder=5)
    xa, lev = first_sidelobes(0.0)[0]
    ax.text(xa, lev + 1.0, f"−{abs(lev):.1f} dB", color=RED, fontsize=13, ha="center", va="bottom")

    # the element-pattern drop on the moved trace's peak
    # the 0 dB reference carried over the moved peak, so the drop can be seen
    ax.plot([23, 37], [0, 0], color=AMBER, lw=1.0, ls=(0, (2, 2)), zorder=4)
    ax.annotate(f"peak −{abs(drop):.1f} dB:\nelement pattern", xy=(37.5, -0.3),
                xytext=(46, 1.6), color=AMBER, fontsize=13, ha="left", va="top",
                linespacing=1.15,
                arrowprops=dict(arrowstyle="-", color=AMBER, lw=1.0, shrinkA=1, shrinkB=1))

    ax.axhline(FLOOR_DB, color=GRAY, lw=1.0, ls=(0, (5, 4)), zorder=1)
    ax.text(69, FLOOR_DB - 0.7, f"floor −{abs(FLOOR_DB):.0f} dB", fontsize=13, color=GRAY,
            ha="right", va="top")
    s0, s30 = grid_step_at(0.0), grid_step_at(30.0)
    ax.text(-38, -25.0, f"one dot per 2.8125° phase step:\n{s0:.2f}° apart at 0°, "
            f"{s30:.2f}° at 30°", fontsize=13, color=GRAY, va="top", linespacing=1.2)

    ax.set_xlim(-40, 70)
    ax.set_ylim(-33, 3)
    ax.set_xticks([-30, 0, 30, 60])
    ax.set_xticklabels(["−30", "0", "30", "60"])
    ax.set_yticks([-20, -10, 0])
    ax.set_yticklabels(["−20", "−10", "0"])
    ax.set_xlabel("sweep steering angle (deg)")
    ax.set_ylabel("power (dB)")
    ax.grid(color=RULE, lw=0.7, alpha=0.7)
    ax.set_axisbelow(True)
    clean(ax)
    finalize(fig, "L19-expected-sweep")


# --------------------------------------------------------------------------- 3
def phase_ramp() -> None:
    """The 30 deg prediction against the readout: +n dphi rising, the same
    ramp wrapped into 0-360, and the falling, unwrapped whole degrees that
    Phase Control shows after Apply 30."""
    dphi = KD_DEG * math.sin(math.radians(30.0))
    n = np.arange(N)
    unwrapped = n * dphi
    wrapped = unwrapped % 360.0
    shown = np.array(phase_control(30.0))
    assert np.allclose(np.round(unwrapped, 1),
                       [0, 88.4, 176.8, 265.2, 353.6, 442.0, 530.5, 618.9])
    assert np.allclose(np.round(wrapped, 1),
                       [0, 88.4, 176.8, 265.2, 353.6, 82.0, 170.5, 258.9])
    # the readout is the prediction negated, to within the whole-degree rounding
    # and the GUI's c (0.07 % from the course's 3e8)
    assert np.all(np.abs(shown + unwrapped) < 1.0), shown + unwrapped

    el = n + 1
    fig, ax = plt.subplots(figsize=(5.9, 3.6))
    ax.axhline(0, color="#8a929c", lw=1.0, zorder=1)
    for yv in (360, -360):
        ax.axhline(yv, color=LIGHT, lw=0.9, ls=(0, (4, 3)), zorder=1)
    ax.plot(el, unwrapped, color=NAVY, lw=1.8, marker="o", ms=5, zorder=3)
    ax.plot(el, wrapped, ls="none", marker="o", ms=7, mfc="white", mec=BLUE, mew=1.8,
            zorder=4)
    ax.plot(el, shown, color=RED, lw=1.8, marker="s", ms=5, zorder=3)
    # Phase Control's values, under each point (the line falls, so they stagger)
    for e, v in zip(el[1:], shown[1:]):
        ax.text(e - 0.1, v - 18, f"−{abs(v)}", color=RED, fontsize=13, ha="right", va="top")

    ax.text(1.0, 640, "predicted, +nΔφ", color=NAVY, fontsize=13, ha="left", va="center")
    ax.text(1.0, 520, "wrapped into 0–360", color=BLUE, fontsize=13, ha="left", va="center")
    ax.text(1.0, -560, "Phase Control shows", color=RED, fontsize=13, ha="left", va="center")
    ax.text(1.0, -660, "after Apply 30", color=RED, fontsize=13, ha="left", va="center")

    ax.set_xlim(0.6, 8.9)
    ax.set_ylim(-760, 700)
    ax.set_xticks(el)
    ax.set_yticks([-360, 0, 360])
    ax.set_yticklabels(["−360", "0", "360"])
    ax.set_xlabel("element")
    ax.set_ylabel("phase (deg)")
    clean(ax)
    finalize(fig, "L19-phase-ramp")


# --------------------------------------------------------------------------- 4
def bench_setup() -> None:
    """Top view: the array, the 1 m arc centered between E4 and E5, the
    HB100 positions at 0, +30, +45 deg, and the + side, which is the E8 end
    by the +n dphi convention (L18) -- to be confirmed on the kit."""
    R = 1.0
    fig, ax = plt.subplots(figsize=(5.9, 4.0))
    ax.set_aspect("equal")
    ax.axis("off")

    # the array, element row along x, boresight up the page
    pitch = 0.055
    xs = (np.arange(N) - (N - 1) / 2) * pitch
    ax.add_patch(Rectangle((xs[0] - 0.04, -0.075), xs[-1] - xs[0] + 0.08, 0.06,
                           facecolor="#e9eef4", edgecolor=GRAY, lw=1.0, zorder=2))
    for x in xs:
        ax.add_patch(Rectangle((x - 0.018, -0.015), 0.036, 0.03, facecolor=NAVY,
                               edgecolor="none", zorder=3))
    ax.text(xs[0] - 0.06, -0.045, "E1", color=NAVY, fontsize=13, ha="right", va="center")
    ax.text(0, -0.10, "array", color=GRAY, fontsize=13, ha="center",
            va="top")
    ax.text(-0.95, 1.36, "top view", color=GRAY, fontsize=13, ha="left", va="top")

    # the arc and its ticks every 15 deg
    a = np.radians(np.linspace(-60, 60, 400))
    ax.plot(R * np.sin(a), R * np.cos(a), color=GRAY, lw=1.3, ls=(0, (6, 4)), zorder=1)
    for t in range(-60, 61, 15):
        ar = np.radians(t)
        ax.plot([0.965 * R * np.sin(ar), 1.035 * R * np.sin(ar)],
                [0.965 * R * np.cos(ar), 1.035 * R * np.cos(ar)], color=GRAY, lw=1.1)

    # boresight and the 1 m range
    ax.plot([0, 0], [0.02, R], color=GRAY, lw=1.0, ls=(0, (2, 3)), zorder=1)
    ax.text(-0.03, 0.5 * R, "1 m", color=INK, fontsize=13, ha="right", va="center")

    # the three source positions
    for t, col in ((0, GREEN), (30, AMBER), (45, AMBER)):
        ar = np.radians(t)
        px, py = R * np.sin(ar), R * np.cos(ar)
        if t:
            ax.plot([0, px], [0.02, py], color=col, lw=1.2, alpha=0.7, zorder=1)
        ax.add_patch(Rectangle((px - 0.035, py - 0.025), 0.07, 0.05, angle=-t,
                               rotation_point="center", facecolor=col, edgecolor="none",
                               zorder=4))
        lab = f"{t}°" if t == 0 else f"+{t}°"
        ax.text(1.13 * px, 1.13 * py, lab, color=col, fontsize=13, ha="center",
                va="center")
    ax.text(0, 1.22 * R, "HB100", color=GREEN, fontsize=13, ha="center", va="bottom")

    # the + side
    ax.text(xs[-1] + 0.06, -0.045, "E8", color=NAVY, fontsize=13, ha="left", va="center")
    ax.annotate("", xy=(0.68, -0.045), xytext=(0.42, -0.045),
                arrowprops=dict(arrowstyle="-|>", color=INK, lw=1.3))
    ax.text(0.72, 0.0, "+ side: toward E8", color=INK, fontsize=13, ha="left",
            va="bottom")
    ax.text(0.72, -0.07, "confirm with Est. Angle", color=GRAY, fontsize=13, ha="left",
            va="top")

    ax.set_xlim(-0.95, 1.9)
    ax.set_ylim(-0.24, 1.38)
    finalize(fig, "L19-bench-setup")


# --------------------------------------------------------------------------- 5
def _lobe(ax, x0, y0, aim_deg, length, col, alpha, lw=1.4):
    """A beam drawn as the array factor's main lobe, in polar form."""
    th = np.linspace(-14, 14, 120)
    # main lobe of the N = 8 pattern about its own axis
    kd = 360.0 * D / LAM
    psi = np.radians(kd * np.sin(np.radians(th)))
    with np.errstate(divide="ignore", invalid="ignore"):
        r = np.where(np.abs(psi) < 1e-9, 1.0, np.sin(N * psi / 2) / (N * np.sin(psi / 2)))
    r = np.clip(r, 0, None) * length
    phi = np.radians(aim_deg + th)
    px = x0 + r * np.sin(phi)
    py = y0 + r * np.cos(phi)
    ax.fill(px, py, color=col, alpha=alpha, lw=0, zorder=2)
    ax.plot(px, py, color=col, lw=lw, alpha=min(1.0, alpha * 2.5), zorder=2)


def _array(ax, x0, y0, rot_deg, col=NAVY):
    """A short element row at (x0, y0), rotated rot_deg (positive clockwise)."""
    c, s = math.cos(math.radians(rot_deg)), math.sin(math.radians(rot_deg))
    u = np.array([c, -s])                 # along the row
    v = np.array([s, c])                  # boresight
    half = 0.20
    p = np.array([x0, y0])
    corners = [p - half * u - 0.03 * v, p + half * u - 0.03 * v,
               p + half * u + 0.01 * v, p - half * u + 0.01 * v]
    ax.add_patch(Polygon(corners, closed=True, facecolor=col, edgecolor="none", zorder=4))
    return v


def two_ways() -> None:
    """Left: the array turns past a fixed source; power against rotation is
    EF x AF, the full pattern (L16). Right: nothing moves; the sweep steps the
    commanded beam past the source; power against the command is AF alone,
    because AF depends only on sin(theta_s) - sin(theta), with EF frozen at
    the source's angle (L18 'The Steered Pattern')."""
    fig, axes = plt.subplots(1, 2, figsize=(5.9, 3.3), gridspec_kw={"wspace": 0.05})
    for ax in axes:
        ax.set_aspect("equal")
        ax.axis("off")
        ax.set_xlim(-0.62, 0.62)
        ax.set_ylim(-0.78, 1.12)

    # left: rotate the array
    ax = axes[0]
    rot = 22.0
    ax.add_patch(Rectangle((-0.05, 0.86), 0.10, 0.07, facecolor=GREEN, edgecolor="none",
                           zorder=4))
    ax.text(0.09, 0.895, "source", color=GREEN, fontsize=13, ha="left", va="center")
    ax.plot([0, 0], [0.02, 0.84], color=GREEN, lw=1.0, ls=(0, (2, 3)), zorder=1)
    _lobe(ax, 0, 0, rot, 0.62, NAVY, 0.16)
    _array(ax, 0, 0, rot)
    # the turn: a curved arrow under the array's ends
    ax.add_patch(FancyArrowPatch((-0.34, -0.06), (0.34, -0.06), connectionstyle="arc3,rad=0.25",
                                 arrowstyle="<|-|>", mutation_scale=10, color=INK, lw=1.1,
                                 zorder=5))
    ax.text(0, -0.22, "turn the array", color=INK, fontsize=13, ha="center", va="top")
    ax.text(0, -0.42, "traces EF × AF", color=NAVY, fontsize=13, ha="center", va="top")

    # right: sweep the command
    ax = axes[1]
    ts = 30.0
    sx, sy = 0.88 * math.sin(math.radians(ts)), 0.88 * math.cos(math.radians(ts))
    ax.add_patch(Rectangle((sx - 0.05, sy - 0.035), 0.10, 0.07, angle=-ts,
                           rotation_point="center", facecolor=GREEN, edgecolor="none",
                           zorder=4))
    ax.plot([0, sx * 0.95], [0.02, sy * 0.95], color=GREEN, lw=1.0, ls=(0, (2, 3)),
            zorder=1)
    for aim, al in ((-30, 0.07), (0, 0.10), (ts, 0.20)):
        _lobe(ax, 0, 0, aim, 0.62, NAVY if aim == ts else BLUE, al)
    _array(ax, 0, 0, 0.0)
    ax.add_patch(Arc((0, 0), 1.46, 1.46, theta1=90 - 52, theta2=90 + 52, color=INK,
                     lw=1.1, ls=(0, (3, 3)), zorder=1))
    ax.text(0, -0.22, "sweep the command", color=INK, fontsize=13, ha="center", va="top")
    ax.text(0, -0.42, "traces AF only", color=NAVY, fontsize=13, ha="center", va="top")
    ax.text(0, -0.60, "(EF fixed at the source)", color=GRAY, fontsize=13, ha="center",
            va="top")
    finalize(fig, "L19-two-ways")


# --------------------------------------------------------------------------- 6
def multipath_shift(r=0.1, src=30.0):
    """Largest peak shift a reflection r (20 dB down) can cause on the 30 deg
    trace, over image angles 3-60 deg away and every relative phase. The
    sweep adds the two arrivals' fields; this is the bound behind the 1 deg
    allowance."""
    ph = np.linspace(peak_dphi(src) - 20, peak_dphi(src) + 20, 4001)
    kd = 360.0 * D * FREQ / C_GUI

    def field(p, t):
        psi = np.radians(kd * np.sin(np.radians(t)) - p)
        with np.errstate(divide="ignore", invalid="ignore"):
            return np.where(np.abs(np.sin(psi / 2)) < 1e-12, 1.0 + 0j,
                            np.exp(1j * (N - 1) * psi / 2) * np.sin(N * psi / 2)
                            / (N * np.sin(psi / 2)))
    base = sweep_axis(ph[np.argmax(np.abs(field(ph, src)))])
    worst = 0.0
    for dt in np.arange(3, 61, 0.5):
        for t_img in (src - dt, src + dt):
            for rel in np.radians(np.arange(0, 360, 10)):
                tot = np.abs(field(ph, src) + r * np.exp(1j * rel) * field(ph, t_img))
                worst = max(worst, abs(sweep_axis(ph[np.argmax(tot)]) - base))
    return worst


def error_budget() -> None:
    """The error sources at the 30 deg test case, and their root-sum-square.
    No drift bar: a drift that keeps the tone inside the 3 MHz window moves
    the beam less than 0.01 deg (L19 audit WHY-04)."""
    half_step = grid_step_at(30.0) / 2
    aim_mm = 25.0
    aim_exact = math.degrees(math.atan(aim_mm / 1000.0))
    aim = 1.5                       # the page's allowance, 25 mm at 1 m rounded up
    multipath = 1.0
    ripple = (20 * math.log10(1.1), 20 * math.log10(0.9))
    rss = math.sqrt(half_step ** 2 + aim ** 2 + multipath ** 2)
    assert round(half_step, 2) == 0.53
    assert round(aim_exact, 2) == 1.43
    assert np.allclose(np.round(ripple, 1), [0.8, -0.9])
    assert round(rss, 1) == 1.9 and rss < 2.0
    # one reflection 20 dB down moves the 30 deg peak 0.72 deg at worst; the
    # 1.0 deg bar is that, rounded up to allow for more than one
    worst = multipath_shift()
    assert 0.6 < worst <= multipath, worst
    print(f"   error budget: half step {half_step:.3f}, aim {aim_exact:.2f} -> {aim}, "
          f"multipath {multipath} (one reflection, worst {worst:.2f}), RSS {rss:.3f}")

    rows = [
        ("sweep grid, half a step at 30°", half_step, NAVY, f"{half_step:.2f}°"),
        ("aim: 25 mm at 1 m", aim, BLUE, f"{aim:.1f}°"),
        ("multipath: a reflection 20 dB down", multipath, GRAY, f"{multipath:.1f}°"),
        ("root-sum-square total", rss, AMBER, f"{rss:.1f}°"),
    ]
    fig, ax = plt.subplots(figsize=(5.9, 3.3))
    H = 0.42
    for i, (lab, v, col, txt) in enumerate(rows):
        y = -i * 1.0
        ax.barh(y, v, height=H, color=col, alpha=0.9, zorder=3)
        ax.text(0.0, y + H / 2 + 0.06, lab, color=INK, fontsize=13, ha="left", va="bottom")
        if v > 1.7:     # the total sits against the pass line: label it inside
            ax.text(v - 0.05, y, txt, color="white", fontsize=13, ha="right", va="center",
                    zorder=4)
        else:
            ax.text(v + 0.05, y, txt, color=col, fontsize=13, ha="left", va="center")
    ax.axvline(2.0, color=RED, lw=1.4, ls=(0, (4, 3)), zorder=2)
    ax.text(2.04, 0.55, "pass: within ±2°", color=RED, fontsize=13, ha="left", va="center")
    ax.set_xlim(0, 2.9)
    ax.set_ylim(-3.45, 0.85)
    ax.set_yticks([])
    ax.set_xticks([0, 0.5, 1.0, 1.5, 2.0, 2.5])
    ax.set_xticklabels(["0", "0.5", "1", "1.5", "2", "2.5"])
    ax.set_xlabel("peak-angle error (deg)")
    ax.grid(color=RULE, lw=0.7, axis="x", alpha=0.7)
    ax.set_axisbelow(True)
    for s in ("top", "right", "left"):
        ax.spines[s].set_visible(False)
    finalize(fig, "L19-error-budget")


def main() -> int:
    IMG.mkdir(parents=True, exist_ok=True)
    check_numbers()
    sweep_compare()
    expected_sweep()
    phase_ramp()
    bench_setup()
    two_ways()
    error_budget()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
