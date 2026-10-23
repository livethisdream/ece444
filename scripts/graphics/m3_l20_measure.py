#!/usr/bin/env python3
"""L20 Lab (Array Factor) figures.

  L20-read-the-trace     : one measured sweep with HPBW, FNBW and first SLL
                           marked -- the three numbers the lab asks for
  L20-ideal-vs-measured  : ideal N=8 array factor under the same sweep as the
                           phase-step sampled, noise-floored trace
  L20-aperture-halving   : ideal 8 / 4 / 2 element array factors at the dry
                           run's 10.408 GHz, with the dry run's measured peaks:
                           the beam doubles, the peak steps 6.0 dB ideally and
                           5.1 and 4.8 dB measured

The first two match book/extras/viz/af-measurement-compare.html exactly: same
element sum, same sweep grid, same -23 dBc floor, same seeded noise
realization (LCG seed 6618, 20 power looks per step). The figures carry
no equations -- the math lives in the lesson text.

The sweep grid is the GUI's with Use Bits on, which every lab preset sets: one
2.8125 deg ADAR1000 phase LSB per point, so the samples are uniform in
sin(theta) -- 2.8125/173.2 = 0.0162 apart at 10.3 GHz, 0.93 deg of angle at
broadside -- not 2.8125 deg of angle apart. Phase steps past kd ask for no real
angle (the GUI piles them at +/-90 deg) and are left out.

    python3 scripts/graphics/m3_l20_measure.py
    -> book/extras/viz/img/L20-*.svg
"""

from __future__ import annotations

import io
import math
import re
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from svg_font_stack import apply_font_stack
import numpy as np

NAVY, BLUE, RED, GREEN, AMBER, GRAY = "#004a85", "#0067b9", "#b01e24", "#3f7d34", "#8a5a00", "#5a5a5a"
INK, RULE = "#1a1a1a", "#c7d2e0"
ROOT = Path(__file__).resolve().parents[2]
IMG = ROOT / "book/extras/viz/img"

LAM, DEL = 29.1e-3, 14e-3          # 10.3 GHz, PHASER element spacing
KD = 2 * math.pi * DEL / LAM
KD_DEG = math.degrees(KD)          # 173.2 deg of phase per unit sin(theta)
NEL, STEP, FLOOR_DB, LOOKS, SEED = 8, 2.8125, -23.0, 20, 6618
YMIN, YMAX = -40.0, 3.0

plt.rcParams.update({
    "svg.fonttype": "none",
    "font.size": 13,
    "axes.edgecolor": "#8a929c",
    "axes.labelcolor": INK,
    "xtick.color": GRAY, "ytick.color": GRAY,
    "text.color": INK,
    "axes.linewidth": 1.0,
    "legend.frameon": False,
})

PRESETS = {8: [1] * 8, 4: [0, 0, 1, 1, 1, 1, 0, 0], 2: [0, 0, 0, 1, 1, 0, 0, 0]}


def finalize(fig, name: str) -> None:
    buf = io.StringIO()
    fig.savefig(buf, format="svg", transparent=True, bbox_inches="tight", pad_inches=0.06)
    plt.close(fig)
    s = buf.getvalue()
    s = s[s.index("<svg"):]
    s = apply_font_stack(s)
    (IMG / f"{name}.svg").write_text(s, encoding="utf-8")
    print(f"wrote {IMG / (name + '.svg')}")


# ---------------------------------------------------------------- array model
def af_complex(theta_deg, w):
    """Element sum, normalized so the 8-element broadside peak = 1."""
    s = np.sin(np.deg2rad(theta_deg))
    re = np.zeros_like(s, dtype=float)
    im = np.zeros_like(s, dtype=float)
    for n in range(NEL):
        if not w[n]:
            continue
        ph = KD * (n - (NEL - 1) / 2) * s
        re += np.cos(ph)
        im += np.sin(ph)
    return re / NEL, im / NEL


def ideal_db(w, step=0.05):
    t = np.arange(-90.0, 90.0 + 1e-9, step)
    re, im = af_complex(t, w)
    return t, 10 * np.log10(np.maximum(re * re + im * im, 1e-9))


class LCG:
    """Same generator as the widget, so both tell the same measurement story."""

    def __init__(self, seed):
        self.s = seed & 0xFFFFFFFF

    def u(self):
        self.s = (self.s * 1664525 + 1013904223) & 0xFFFFFFFF
        return (self.s + 0.5) / 4294967296.0

    def gauss(self):
        u1, u2 = self.u(), self.u()
        r = math.sqrt(-2 * math.log(u1))
        return r * math.cos(2 * math.pi * u2), r * math.sin(2 * math.pi * u2)


def meas_db(w):
    rng = LCG(SEED)
    sg = math.sqrt(10 ** (FLOOR_DB / 10) / 2)
    n_max = int(math.floor(KD_DEG / STEP))
    t = np.array([math.degrees(math.asin(i * STEP / KD_DEG))
                  for i in range(-n_max, n_max + 1)])
    re, im = af_complex(t, w)
    out = []
    for k in range(len(t)):
        acc = 0.0
        for _ in range(LOOKS):
            g1, g2 = rng.gauss()
            acc += (re[k] + g1 * sg) ** 2 + (im[k] + g2 * sg) ** 2
        out.append(10 * math.log10(max(acc / LOOKS, 1e-12)))
    return t, np.array(out)


def read_metrics(t, db):
    """Read peak, HPBW, first nulls and first sidelobe off a drawn trace."""
    ip = int(np.argmax(db))
    pk = db[ip]
    half = pk - 3.0103

    def cross(d):
        i = ip
        while 0 <= i + d < len(db):
            if db[i + d] <= half:
                y0, y1 = db[i], db[i + d]
                f = 0.0 if y0 == y1 else (y0 - half) / (y0 - y1)
                return t[i] + f * (t[i + d] - t[i])
            i += d
        return None

    def outward(d):
        # First null: the lowest sample once the trace is 12 dB down, accepted
        # only when the trace then climbs 4 dB back out of it. A sample grid
        # ~1 deg apart puts noise ripples on the main-lobe skirt, and a plain
        # "first local minimum" stops on one of them.
        i = ip
        while 0 <= i + d < len(db) and db[i + d] > half:
            i += d
        mi, found = None, False
        while 0 <= i + d < len(db):
            i += d
            if mi is None or db[i] < db[mi]:
                mi = i
            if db[mi] <= pk - 12 and db[i] > db[mi] + 4:
                found = True
                break
        if not found:
            return None, None, None
        na, nd = t[mi], db[mi]
        # First sidelobe: the highest sample past the null before the trace
        # falls 4 dB from it, if it stands 4 dB clear of the null.
        j, mx = mi, None
        while 0 <= j + d < len(db):
            j += d
            if mx is None or db[j] > db[mx]:
                mx = j
            if db[j] < db[mx] - 4:
                break
        if mx is None or db[mx] - nd < 4 or mx in (0, len(db) - 1):
            return na, nd, None
        return na, nd, (t[mx], db[mx])

    ln, ld, ls = outward(-1)
    rn, rd, rs = outward(1)
    sl = [x for x in (ls, rs) if x is not None]
    sl.sort(key=lambda p: -p[1])
    return {
        "pk": pk, "peak_ang": t[ip], "half": half,
        "l": cross(-1), "r": cross(1),
        "nl": ln, "nr": rn, "nulldb": ld if ld is not None else rd,
        "sl": sl[0] if sl else None,
    }


def frame(ax, xlim=(-90, 90)):
    ax.set_xlim(*xlim)
    ax.set_ylim(YMIN, YMAX)
    ax.set_xlabel("Steer angle from broadside  (deg)")
    ax.set_ylabel("Received power  (dB)")
    ax.set_xticks(range(xlim[0], xlim[1] + 1, 30))
    ax.set_yticks(range(-40, 1, 10))
    ax.grid(color=RULE, linewidth=0.8)
    for sp in ("top", "right"):
        ax.spines[sp].set_visible(False)


# --------------------------------------------------------------- the figures
def read_the_trace() -> None:
    """One measured 8-element sweep, with the three lab numbers marked."""
    w = PRESETS[8]
    t, db = meas_db(w)
    m = read_metrics(t, db)

    fig, ax = plt.subplots(figsize=(7.4, 4.0))
    frame(ax)
    ax.axhline(FLOOR_DB, color=AMBER, lw=1.2, ls=(0, (4, 4)))
    ax.text(-86, FLOOR_DB - 1.4, "noise floor", color=AMBER, fontsize=11, va="top")
    ax.plot(t, np.clip(db, YMIN, None), color=BLUE, lw=2.0, marker="o", ms=3.0,
            mfc=NAVY, mec=NAVY, zorder=3)

    # HPBW
    ax.annotate("", xy=(m["r"], m["half"]), xytext=(m["l"], m["half"]),
                arrowprops=dict(arrowstyle="<->", color=GREEN, lw=1.8))
    ax.text(m["r"] + 3, m["half"], "HPBW", color=GREEN, fontsize=12.5,
            fontweight="bold", va="center", ha="left")
    # FNBW
    ax.annotate("", xy=(m["nr"], -34), xytext=(m["nl"], -34),
                arrowprops=dict(arrowstyle="<->", color=RED, lw=1.6))
    ax.text(0, -33.0, "FNBW", color=RED, fontsize=12.5, fontweight="bold",
            ha="center", va="bottom")
    # first sidelobe
    sa, sd = m["sl"]
    ax.plot([sa], [sd], marker="o", ms=10, mfc="none", mec=AMBER, mew=1.8, zorder=4)
    # label on the outside of whichever lobe the reader picked, clear of HPBW
    side = 1 if sa > 0 else -1
    ax.annotate("first sidelobe", xy=(sa + side * 2.0, sd + 0.6),
                xytext=(sa + side * 16, sd + 8.5), ha="left" if side > 0 else "right",
                color=AMBER, fontsize=12, fontweight="bold",
                arrowprops=dict(arrowstyle="-", color=AMBER, lw=1.2))
    # peak
    ax.plot([m["peak_ang"]], [m["pk"]], marker="v", ms=8, color=NAVY, zorder=4)
    ax.text(m["peak_ang"] - 4, m["pk"] + 0.6, "peak", color=NAVY, fontsize=12,
            fontweight="bold", ha="right", va="bottom")

    finalize(fig, "L20-read-the-trace")


def ideal_vs_measured() -> None:
    """Where the sweep stops following the array factor: nulls and floor."""
    w = PRESETS[8]
    ti, di = ideal_db(w)
    tm, dm = meas_db(w)

    fig, ax = plt.subplots(figsize=(7.4, 4.0))
    frame(ax, (-60, 60))
    ax.axhline(FLOOR_DB, color=AMBER, lw=1.2, ls=(0, (4, 4)))
    ax.text(34, FLOOR_DB - 1.4, "noise floor", color=AMBER, fontsize=11, va="top")
    ax.plot(ti, di, color=GRAY, lw=1.5, label="Array factor, 8 elements")
    ax.plot(tm, np.clip(dm, YMIN, None), color=BLUE, lw=2.2, marker="o", ms=3.6,
            mfc=NAVY, mec=NAVY, label="Measured sweep, 2.8125° phase steps", zorder=3)

    # the two departures worth naming
    m = read_metrics(tm, dm)
    ax.annotate("nulls fill in", xy=(m["nr"] + 0.4, m["nulldb"] - 0.3), xytext=(27, -30.5),
                color=RED, fontsize=12, fontweight="bold",
                arrowprops=dict(arrowstyle="->", color=RED, lw=1.3))
    ax.annotate("outer lobes ride the floor", xy=(-56.5, -17.6), xytext=(-57, -33.0),
                color=AMBER, fontsize=12, fontweight="bold",
                arrowprops=dict(arrowstyle="->", color=AMBER, lw=1.3))
    ax.legend(loc="lower center", bbox_to_anchor=(0.5, 1.0), ncol=2,
              fontsize=11.5, handlelength=1.8)

    finalize(fig, "L20-ideal-vs-measured")


# The dry run (phaser-00, 2026-10-19, review/M3_LAB_DRYRUN.md): Find HB100 read
# 10.408 GHz, and the three peaks read -5.25, -10.4 and -15.1 dBFS, steps of
# 5.1 and 4.8 dB against the voltage sum's 6.0 and 6.0. The cause of the
# shortfall is not known, so this figure shows the ideal array factor and the
# measured peaks side by side and claims nothing about why they differ.
DRY_F = 10.408e9
DRY_STEPS = (5.1, 4.8)             # measured, 8 -> 4 and 4 -> 2


def aperture_halving() -> None:
    """Ideal 8 / 4 / 2 element array factors at the dry run's frequency, with
    the dry run's measured peak levels: the beam doubles, the peak steps 6.0 dB
    ideally and about 5 dB measured.
    """
    kd = 2 * math.pi * DEL / (3.00e8 / DRY_F)
    t = np.arange(-90.0, 90.0 + 1e-9, 0.05)
    s = np.sin(np.deg2rad(t))

    def af_db(w):
        re = sum(np.cos(kd * (n - 3.5) * s) for n in range(NEL) if w[n])
        im = sum(np.sin(kd * (n - 3.5) * s) for n in range(NEL) if w[n])
        return 10 * np.log10(np.maximum((re / NEL) ** 2 + (im / NEL) ** 2, 1e-9))

    fig, ax = plt.subplots(figsize=(7.4, 4.0))
    frame(ax)
    styles = {8: (NAVY, 2.4, "8 elements (E1–E8)"), 4: (BLUE, 2.1, "4 elements (E3–E6)"),
              2: (GREEN, 2.0, "2 elements (E4, E5)")}
    for n in (8, 4, 2):
        color, lw, lab = styles[n]
        ax.plot(t, np.clip(af_db(PRESETS[n]), YMIN, None), color=color, lw=lw, label=lab)

    ideal = [20 * math.log10(n / 8) for n in (8, 4, 2)]
    meas = [0.0, -DRY_STEPS[0], -DRY_STEPS[0] - DRY_STEPS[1]]
    ax.plot([0, 0, 0], meas, ls="none", marker="o", ms=8, mfc="white", mec=RED, mew=2.0,
            zorder=5, label="measured peak")

    def ladder(x, levels, color, head):
        for y in levels:
            ax.plot([x - 3, x + 3], [y, y], color=color, lw=1.4)
        for a, b in zip(levels[:-1], levels[1:]):
            ax.annotate("", xy=(x, b), xytext=(x, a),
                        arrowprops=dict(arrowstyle="<->", color=color, lw=1.4,
                                        shrinkA=0, shrinkB=0))
            ax.text(x - 4.5, (a + b) / 2, f"{a - b:.1f} dB", color=color, fontsize=11.5,
                    fontweight="bold", va="center", ha="right")
        ax.text(x, 1.2, head, color=color, fontsize=11.5, fontweight="bold",
                ha="center", va="bottom")

    ladder(60, ideal, GRAY, "ideal")
    ladder(84, meas, RED, "measured")
    ax.legend(loc="upper left", fontsize=11, handlelength=1.8, borderaxespad=0.3)

    buf = io.StringIO()
    fig.savefig(buf, format="svg", transparent=True, bbox_inches="tight", pad_inches=0.06)
    plt.close(fig)
    out = buf.getvalue()
    out = apply_font_stack(out[out.index("<svg"):])
    (IMG / "L20-aperture-halving.svg").write_text(out, encoding="utf-8")
    print(f"wrote {IMG / 'L20-aperture-halving.svg'}")


if __name__ == "__main__":
    IMG.mkdir(parents=True, exist_ok=True)
    read_the_trace()
    ideal_vs_measured()
    aperture_halving()
    # print what the first two figures assert (the widget's model), so the
    # prose can be checked against them
    for n in (8, 4, 2):
        t, db = meas_db(PRESETS[n])
        m = read_metrics(t, db)
        hp = None if m["l"] is None or m["r"] is None else m["r"] - m["l"]
        fn = None if m["nl"] is None or m["nr"] is None else m["nr"] - m["nl"]
        sl = None if m["sl"] is None else m["sl"][1] - m["pk"]
        print(f"  meas N={n}: peak {m['pk']:+.2f} dB  HPBW {hp}  FNBW {fn}  SLL {sl}"
              f"  null {None if m['nulldb'] is None else round(m['nulldb'] - m['pk'], 1)}")
