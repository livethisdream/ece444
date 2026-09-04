#!/usr/bin/env python3
"""L21 (Array Factor Lab) deck figures.

  L21-read-the-trace     : one measured sweep with HPBW, FNBW and first SLL
                           marked -- the three numbers the lab asks for
  L21-ideal-vs-measured  : ideal N=8 array factor under the same sweep as the
                           2.8125 deg sampled, noise-floored trace
  L21-aperture-halving   : 8 / 4 / 2 active elements on one axis, showing the
                           beamwidth doubling and the ~6 dB peak step

Physics matches book/extras/viz/af-measurement-compare.html exactly: same
element sum, same 2.8125 deg sweep grid, same -23 dBc floor, same seeded
noise realization (LCG seed 6618, 20 power looks per step). Deck figures carry
no equations -- the math lives in the slide text.

    python3 scripts/graphics/m3_l21_measure.py
    -> book/extras/slides/fig/L21-*.svg  (+ viz/img copies)
"""

from __future__ import annotations

import io
import math
import re
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

NAVY, BLUE, RED, GREEN, AMBER, GRAY = "#004a85", "#0067b9", "#b01e24", "#3f7d34", "#8a5a00", "#5a5a5a"
INK, RULE = "#1a1a1a", "#c7d2e0"
ROOT = Path(__file__).resolve().parents[2]
FIG = ROOT / "book/extras/slides/fig"
IMG = ROOT / "book/extras/viz/img"

LAM, DEL = 29.1e-3, 14e-3          # 10.3 GHz, PHASER element spacing
KD = 2 * math.pi * DEL / LAM
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


def finalize(fig, name: str, also_img: bool = False) -> None:
    buf = io.StringIO()
    fig.savefig(buf, format="svg", transparent=True, bbox_inches="tight", pad_inches=0.06)
    plt.close(fig)
    s = buf.getvalue()
    s = s[s.index("<svg"):]
    s = re.sub(r"font-family:[^;}]*", "font-family:inherit", s)
    (FIG / f"{name}.svg").write_text(s, encoding="utf-8")
    print(f"wrote {FIG / (name + '.svg')}")
    if also_img:
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
    t = np.array([-90.0 + i * STEP for i in range(int(round(180 / STEP)) + 1)])
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
        i = ip
        while 0 <= i + d < len(db) and db[i + d] > half:
            i += d
        got = False
        while 0 < i + d < len(db) - 1:
            i += d
            if db[i] <= db[i - 1] and db[i] < db[i + 1]:
                got = True
                break
        if not got or db[i] > pk - 12:
            return None, None, None
        na, nd = t[i], db[i]
        j, got2 = i, False
        while 0 < j + d < len(db) - 1:
            j += d
            if db[j] >= db[j - 1] and db[j] > db[j + 1]:
                got2 = True
                break
        if not got2 or db[j] - nd < 4:
            return na, nd, None
        return na, nd, (t[j], db[j])

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
    ax.annotate("first sidelobe", xy=(sa + 2.0, sd + 0.6), xytext=(sa + 16, sd + 8.5),
                color=AMBER, fontsize=12, fontweight="bold",
                arrowprops=dict(arrowstyle="-", color=AMBER, lw=1.2))
    # peak
    ax.plot([m["peak_ang"]], [m["pk"]], marker="v", ms=8, color=NAVY, zorder=4)
    ax.text(m["peak_ang"] - 4, m["pk"] + 0.6, "peak", color=NAVY, fontsize=12,
            fontweight="bold", ha="right", va="bottom")

    finalize(fig, "L21-read-the-trace", also_img=True)


def ideal_vs_measured() -> None:
    """Where the sweep stops following the array factor: nulls and floor."""
    w = PRESETS[8]
    ti, di = ideal_db(w)
    tm, dm = meas_db(w)

    fig, ax = plt.subplots(figsize=(7.4, 4.0))
    frame(ax, (-60, 60))
    ax.axhline(FLOOR_DB, color=AMBER, lw=1.2, ls=(0, (4, 4)))
    ax.text(-57, FLOOR_DB - 1.4, "noise floor", color=AMBER, fontsize=11, va="top")
    ax.plot(ti, di, color=GRAY, lw=1.5, label="Array factor, 8 elements")
    ax.plot(tm, np.clip(dm, YMIN, None), color=BLUE, lw=2.2, marker="o", ms=3.6,
            mfc=NAVY, mec=NAVY, label="Measured sweep, 2.8125° steps", zorder=3)

    # the two departures worth naming
    ax.annotate("nulls fill in", xy=(15.5, -20.0), xytext=(27, -30.5),
                color=RED, fontsize=12, fontweight="bold",
                arrowprops=dict(arrowstyle="->", color=RED, lw=1.3))
    ax.annotate("outer lobes ride the floor", xy=(-56.5, -17.6), xytext=(-57, -33.0),
                color=AMBER, fontsize=12, fontweight="bold",
                arrowprops=dict(arrowstyle="->", color=AMBER, lw=1.3))
    ax.legend(loc="upper left", fontsize=11.5, handlelength=1.8)

    finalize(fig, "L21-ideal-vs-measured", also_img=True)


def aperture_halving() -> None:
    """Halve the aperture twice: beam doubles, peak steps down about 6 dB."""
    fig, ax = plt.subplots(figsize=(7.4, 4.0))
    frame(ax)
    ax.axhline(FLOOR_DB, color=AMBER, lw=1.1, ls=(0, (4, 4)))
    ax.text(-86, FLOOR_DB - 1.4, "noise floor", color=AMBER, fontsize=11, va="top")

    styles = {8: (NAVY, 2.4, "8 elements"), 4: (BLUE, 2.1, "4 elements (Rx3-Rx6)"),
              2: (GREEN, 2.0, "2 elements (Rx4, Rx5)")}
    for n in (8, 4, 2):
        color, lw, lab = styles[n]
        t, db = meas_db(PRESETS[n])
        m = read_metrics(t, db)
        ax.plot(t, np.clip(db, YMIN, None), color=color, lw=lw, marker="o", ms=2.6,
                mfc=color, mec=color, label=lab)
        ax.plot([m["peak_ang"]], [m["pk"]], marker="_", ms=16, mew=2.4, color=color)

    # peak-step annotation: 8 -> 4 -> 2
    peaks = []
    for n in (8, 4, 2):
        t, db = meas_db(PRESETS[n])
        peaks.append(read_metrics(t, db)["pk"])
    for pk_, xr in zip(peaks, (74, 74, 86)):
        ax.plot([0, xr], [pk_, pk_], color="#9fb1c4", lw=0.9, ls=(0, (3, 3)), zorder=1)
    ax.annotate("", xy=(74, peaks[1]), xytext=(74, peaks[0]),
                arrowprops=dict(arrowstyle="<->", color=RED, lw=1.5))
    ax.text(71, (peaks[0] + peaks[1]) / 2, f"{peaks[0] - peaks[1]:.1f} dB", color=RED,
            fontsize=12, fontweight="bold", va="center", ha="right")
    ax.annotate("", xy=(86, peaks[2]), xytext=(86, peaks[1]),
                arrowprops=dict(arrowstyle="<->", color=RED, lw=1.5))
    ax.text(83, (peaks[1] + peaks[2]) / 2, f"{peaks[1] - peaks[2]:.1f} dB", color=RED,
            fontsize=12, fontweight="bold", va="center", ha="right")

    handles = [plt.Line2D([], [], color=styles[n][0], lw=styles[n][1], label=styles[n][2])
               for n in (8, 4, 2)]
    ax.legend(handles=handles, loc="lower left", fontsize=11.5, handlelength=1.8)

    finalize(fig, "L21-aperture-halving", also_img=True)


if __name__ == "__main__":
    FIG.mkdir(parents=True, exist_ok=True)
    IMG.mkdir(parents=True, exist_ok=True)
    read_the_trace()
    ideal_vs_measured()
    aperture_halving()
    # print what the figures assert, so the prose can be checked against them
    for n in (8, 4, 2):
        t, db = meas_db(PRESETS[n])
        m = read_metrics(t, db)
        hp = None if m["l"] is None or m["r"] is None else m["r"] - m["l"]
        fn = None if m["nl"] is None or m["nr"] is None else m["nr"] - m["nl"]
        sl = None if m["sl"] is None else m["sl"][1] - m["pk"]
        print(f"  meas N={n}: peak {m['pk']:+.2f} dB  HPBW {hp}  FNBW {fn}  SLL {sl}"
              f"  null {None if m['nulldb'] is None else round(m['nulldb'] - m['pk'], 1)}")
