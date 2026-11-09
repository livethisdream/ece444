#!/usr/bin/env python3
"""L20 Lab (Array Factor) figures.

  L20-read-the-trace     : one measured sweep with HPBW, FNBW and first SLL
                           marked -- the three numbers the lab asks for
  L20-ideal-vs-measured  : no longer generated (2026-11-08); the file stays in
                           book/extras/viz/img, unreferenced
  L20-aperture-halving   : ideal 8 / 4 / 2 element array factors at 10.0 GHz:
                           the beam doubles at each halving and the peak
                           steps down; the step is a Part 1 answer, so the
                           figure does not print it

L20-read-the-trace matches book/extras/viz/af-measurement-compare.html exactly: same
element sum, same sweep grid, same -23 dBc floor (below each trace's own peak), same seeded noise
realization (LCG seed 6618, 20 power looks per step). The figures carry
no equations -- the math lives in the lesson text.

The sweep grid is the GUI's with Use Bits on, which every lab preset sets: one
2.8125 deg ADAR1000 phase LSB per point, so the samples are uniform in
sin(theta) -- 2.8125/168.0 = 0.0167 apart at 10.0 GHz, 0.96 deg of angle at
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

LAM, DEL = 3.00e8 / 10.0e9, 14e-3  # 10.0 GHz (30.0 mm), below every kit; PHASER spacing
KD = 2 * math.pi * DEL / LAM
KD_DEG = math.degrees(KD)          # 168.0 deg of phase per unit sin(theta)
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


def floor_db(w):
    """The floor sits FLOOR_DB below each trace's own peak (the widget's model)."""
    return FLOOR_DB + 20 * math.log10(sum(w) / NEL)


def meas_db(w):
    rng = LCG(SEED)
    sg = math.sqrt(10 ** (floor_db(w) / 10) / 2)
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


def frame(ax, xlim=(-90, 90), ylabel="Received power  (dB)"):
    ax.set_xlim(*xlim)
    ax.set_ylim(YMIN, YMAX)
    ax.set_xlabel("Steer angle from broadside  (deg)")
    ax.set_ylabel(ylabel)
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
    frame(ax, ylabel="Received power  (dBc)")
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


def aperture_halving() -> None:
    """Ideal 8 / 4 / 2 element array factors at 10.0 GHz, below every kit: the
    beam doubles at each halving and the peak steps down by the voltage sum.
    No measured points, and no printed step size: the step is a Part 1 answer.
    """
    t = np.arange(-90.0, 90.0 + 1e-9, 0.05)

    fig, ax = plt.subplots(figsize=(7.4, 4.0))
    frame(ax)
    styles = {8: (NAVY, 2.4, "8 elements (E1–E8)"), 4: (BLUE, 2.1, "4 elements (E3–E6)"),
              2: (GREEN, 2.0, "2 elements (E4, E5)")}
    for n in (8, 4, 2):
        color, lw, lab = styles[n]
        tt, db = ideal_db(PRESETS[n])
        ax.plot(tt, np.clip(db, YMIN, None), color=color, lw=lw, label=lab)

    ideal = [20 * math.log10(n / 8) for n in (8, 4, 2)]
    x = 72
    for y in ideal:
        ax.plot([x - 3, x + 3], [y, y], color=GRAY, lw=1.4)
    for p, q in zip(ideal[:-1], ideal[1:]):
        ax.annotate("", xy=(x, q), xytext=(x, p),
                    arrowprops=dict(arrowstyle="<->", color=GRAY, lw=1.4,
                                    shrinkA=0, shrinkB=0))
    ax.text(x, 1.2, "peak step", color=GRAY, fontsize=11.5, fontweight="bold",
            ha="center", va="bottom")
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
