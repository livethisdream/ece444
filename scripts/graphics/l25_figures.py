#!/usr/bin/env python3
"""L25: figures from the 2026-11-03 illustration sweep.

Labels only, no derivations; the math lives in the lesson text. Every plotted
number is computed here and checked against the lesson before it is drawn.

  L25-level-diagram    the PHASER link budget as a level diagram: the echo
                       stepping down from -16 dBm to -80.8 dBm, the noise
                       building up from -174 dBm/Hz to -112 dBm, and the
                       31.1 dB SNR between them (frame "The PHASER Link Budget")
  L25-falloff          one-way (20 dB/decade) against two-way (40 dB/decade)
                       received power from 1 to 30 m, with the 6 and 12 dB
                       steps from 3 to 6 m (frame "Two-Way Path Loss in Decibels")
  L25-sphere-regions   backscatter RCS of a conducting sphere, sigma/pi a^2
                       against 2 pi a/lambda, from the exact series, with the
                       Rayleigh 9x^4 and optical 1 asymptotes and the 10 cm
                       sphere at 10.5 (frame "The Sphere")
  L25-corner-3d        a trihedral corner in isometric view, one ray traced
                       through its three bounces and out antiparallel
                       (frame "The Corner Reflector")
  L25-rcs-equivalent   a real target's scattering pattern beside the
                       isotropic scatterer of area sigma that returns the
                       same power toward the radar (frame "Radar Cross Section")

    python3 scripts/graphics/l25_figures.py
"""

from __future__ import annotations
import io
from pathlib import Path

import numpy as np
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon, Circle, FancyArrowPatch
from svg_font_stack import apply_font_stack

NAVY, BLUE, RED, GREEN, AMBER, GRAY = "#004a85", "#0067b9", "#b01e24", "#1d7a4d", "#8a5a00", "#5b6573"
INK, RULE, SHADE = "#15202b", "#c7d2e0", "#dbe8f4"
ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "book/extras/viz/img"

plt.rcParams.update({"svg.fonttype": "none", "font.size": 12.5, "text.color": INK,
                     "axes.edgecolor": GRAY, "axes.labelcolor": INK,
                     "xtick.color": GRAY, "ytick.color": GRAY,
                     "axes.spines.top": False, "axes.spines.right": False})
BOX = dict(fc="white", ec="none", alpha=0.92, pad=1.5)

# ------------------------------------------------------------- lesson numbers
C, F = 3e8, 10e9
LAM = C / F
K_B = 1.380649e-23
A_CORNER = 0.10
DB = lambda x: 10 * np.log10(x)

PT = -16.0
GAINS = 6.0 + 15.0
LAM2 = DB(LAM ** 2)
SIGMA = DB(4 * np.pi * A_CORNER ** 4 / (3 * LAM ** 2))
FOURPI3 = -DB((4 * np.pi) ** 3)
R = 3.0
R4 = -40 * np.log10(R)
PR = PT + GAINS + LAM2 + SIGMA + FOURPI3 + R4
KT0 = DB(K_B * 290 * 1e3)            # dBm/Hz
BW = 60.0                            # 1 MHz
NF = 2.0
N = KT0 + BW + NF                    # -174 + 60 + 2, with kT0 unrounded (-173.98)
SNR = PR - N

assert abs(PR - (-80.8)) < 0.05 and abs(N - (-112.0)) < 0.05 and abs(SNR - 31.1) < 0.05


def _m(x, fmt="{:.1f}"):
    """A typographic minus, so labels match the axis ticks."""
    return fmt.format(x).replace("-", "−")


def finalize(fig, name: str) -> None:
    buf = io.StringIO()
    fig.savefig(buf, format="svg", transparent=True, bbox_inches="tight", pad_inches=0.06)
    plt.close(fig)
    s = buf.getvalue()
    s = s[s.index("<svg"):]
    (OUT / f"{name}.svg").write_text(apply_font_stack(s), encoding="utf-8")
    print(f"wrote {OUT / (name + '.svg')}")


# ------------------------------------------------------------- level diagram
def level_diagram() -> None:
    """A horizontal waterfall: one row per term, so every label has its own line."""
    sig = [(r"$P_t$", PT), (r"$G_t + G_r$", GAINS), (r"$\lambda^2$", LAM2), (r"$\sigma$", SIGMA),
           (r"$(4\pi)^3$", FOURPI3), (r"$R^4$", R4)]
    noi = [(r"$kT_0$", KT0), (r"$B$ (1 MHz)", BW), (r"$F$", NF)]
    rows = [s[0] for s in sig] + [r"$P_r$"] + [n[0] for n in noi] + [r"$N$"]
    fig, ax = plt.subplots(figsize=(5.4, 4.6))
    h = 0.56
    lvl = None
    for i, (name, d) in enumerate(sig):
        if i == 0:
            lvl = d
            ax.plot([lvl, lvl], [i - h / 2, i + h / 2], color=NAVY, lw=2.6)
            ax.text(lvl + 3, i, _m(lvl, "{:.0f}") + " dBm", va="center", fontsize=12, color=NAVY)
            continue
        new = lvl + d
        col = GREEN if d > 0 else RED
        ax.add_patch(plt.Rectangle((min(lvl, new), i - h / 2), abs(d), h, fc=col, alpha=0.30, ec=col, lw=0.8))
        ax.plot([lvl, lvl], [i - 1 + h / 2, i - h / 2], color=NAVY, lw=0.8, ls=(0, (2, 2)))
        txt = ("+" if d > 0 else "") + _m(d)
        if d > 0:
            ax.text(new + 3, i, txt, va="center", ha="left", fontsize=12, color=col)
        else:
            ax.text(new - 3, i, txt, va="center", ha="right", fontsize=12, color=col)
        lvl = new
    ipr = len(sig)
    ax.plot([lvl, lvl], [ipr - 1 + h / 2, ipr + h / 2], color=NAVY, lw=0.8, ls=(0, (2, 2)))
    ax.plot([PR, PR], [ipr - h / 2, ipr + h / 2], color=NAVY, lw=2.6)
    ax.text(PR + 3, ipr, _m(PR) + " dBm", va="center", fontsize=12, color=NAVY, fontweight="bold")
    # the noise, built up from kT0
    j = ipr + 1
    lvl = KT0
    ax.plot([lvl, lvl], [j - h / 2, j + h / 2], color=AMBER, lw=2.6)
    ax.text(lvl + 3, j, _m(lvl, "{:.0f}") + " dBm/Hz", va="center", fontsize=12, color=AMBER)
    for k, (name, d) in enumerate(noi[1:], 1):
        new = lvl + d
        ax.add_patch(plt.Rectangle((lvl, j + k - h / 2), d, h, fc=AMBER, alpha=0.30, ec=AMBER, lw=0.8))
        ax.plot([lvl, lvl], [j + k - 1 + h / 2, j + k - h / 2], color=AMBER, lw=0.8, ls=(0, (2, 2)))
        ax.text(new + 3, j + k, "+" + _m(d, "{:.0f}"), va="center", fontsize=12, color=AMBER)
        lvl = new
    jn = j + len(noi)
    ax.plot([N, N], [jn - 1 + h / 2, jn + h / 2], color=AMBER, lw=0.8, ls=(0, (2, 2)))
    ax.plot([N, N], [jn - h / 2, jn + h / 2], color=AMBER, lw=2.6)
    ax.text(N - 3, jn, _m(N) + " dBm", va="center", ha="right", fontsize=12, color=AMBER, fontweight="bold")
    # the SNR: the horizontal gap between P_r and N, drawn below the N row
    ys = jn + 0.95
    ax.plot([PR, PR], [ipr + h / 2, ys + 0.15], color=NAVY, lw=0.8, ls=(0, (1, 2)))
    ax.plot([N, N], [jn + h / 2, ys + 0.15], color=AMBER, lw=0.8, ls=(0, (1, 2)))
    ax.add_patch(FancyArrowPatch((N, ys), (PR, ys), arrowstyle="<|-|>", mutation_scale=10, color=INK, lw=1.2))
    ax.text(PR + 3, ys, "SNR " + _m(SNR) + " dB", va="center", fontsize=12.5, fontweight="bold")
    ax.set_yticks(range(len(rows)))
    ax.set_yticklabels(rows, fontsize=12.5)
    ax.tick_params(axis="y", length=0)
    ax.set_ylim(ys + 0.6, -0.7)
    ax.set_xlim(-185, 22)
    ax.set_xticks(range(-180, 1, 30))
    ax.set_xticklabels([_m(v, "{:.0f}") for v in range(-180, 1, 30)])
    ax.set_xlabel("level (dBm)")
    ax.grid(axis="x", color=RULE, lw=0.6)
    ax.spines["left"].set_visible(False)
    ax.set_axisbelow(True)
    finalize(fig, "L25-level-diagram")


# ------------------------------------------------------------- falloff
def falloff() -> None:
    r = np.logspace(0, np.log10(30), 200)
    fig, ax = plt.subplots(figsize=(5.2, 3.8))
    ax.plot(r, -20 * np.log10(r), color=BLUE, lw=2.2)
    ax.plot(r, -40 * np.log10(r), color=RED, lw=2.2)
    ax.text(22, -20 * np.log10(22) + 3, "one-way\n20 dB/decade", color=BLUE, ha="center", va="bottom", fontsize=12)
    ax.text(14, -40 * np.log10(14) - 5, "two-way\n40 dB/decade", color=RED, ha="right", va="top", fontsize=12)
    for slope, col in ((20, BLUE), (40, RED)):
        y3, y6 = -slope * np.log10(3), -slope * np.log10(6)
        ax.plot([3, 6], [y3, y6], "o", color=col, ms=5)
        ax.annotate("", xy=(6, y6), xytext=(6, y3), arrowprops=dict(arrowstyle="-|>", color=col, lw=1.1, mutation_scale=9))
        ax.plot([3, 6], [y3, y3], color=col, lw=0.8, ls=(0, (2, 2)))
        ax.text(6.4, (y3 + y6) / 2, _m(y6 - y3, "{:.0f}") + " dB", color=col, va="center", fontsize=12)
    ax.set_xscale("log")
    ax.set_xticks([1, 3, 6, 10, 30]); ax.set_xticklabels(["1", "3", "6", "10", "30"])
    ax.set_yticks(range(-60, 1, 10)); ax.set_yticklabels([_m(v, "{:.0f}") for v in range(-60, 1, 10)])
    ax.set_xlim(1, 30); ax.set_ylim(-62, 3)
    ax.set_xlabel("range (m)")
    ax.set_ylabel("received power re 1 m (dB)")
    ax.grid(color=RULE, lw=0.6, which="major")
    ax.set_axisbelow(True)
    finalize(fig, "L25-falloff")


# ------------------------------------------------------------- sphere regions
def _sph_jy(nmax, x):
    """Spherical Bessel j_n (downward recurrence) and y_n (upward), n = 0..nmax+1."""
    y = np.zeros(nmax + 2)
    y[0] = -np.cos(x) / x
    y[1] = -np.cos(x) / x ** 2 - np.sin(x) / x
    for n in range(1, nmax + 1):
        y[n + 1] = (2 * n + 1) / x * y[n] - y[n - 1]
    top = nmax + int(2 * x) + 30
    j = np.zeros(top + 2)
    j[top] = 1e-30
    for n in range(top, 0, -1):
        j[n - 1] = (2 * n + 1) / x * j[n] - j[n + 1]
    j *= (np.sin(x) / x) / j[0]
    return j[: nmax + 2], y


def sphere_backscatter(x):
    """Monostatic RCS of a perfectly conducting sphere, normalized to pi a^2."""
    nmax = int(x + 4 * x ** (1 / 3) + 4)
    j, y = _sph_jy(nmax, x)
    h = j + 1j * y
    s = 0j
    for n in range(1, nmax + 1):
        an = j[n] / h[n]
        bn = (x * j[n - 1] - n * j[n]) / (x * h[n - 1] - n * h[n])
        s += (-1) ** n * (2 * n + 1) * (an - bn)
    return abs(s) ** 2 / x ** 2


def sphere_regions() -> None:
    x = np.logspace(np.log10(0.05), np.log10(30), 1500)
    s = np.array([sphere_backscatter(v) for v in x])
    assert abs(s[0] / (9 * x[0] ** 4) - 1) < 0.01 and abs(s[-1] - 1) < 0.05
    x10 = 2 * np.pi * 0.05 / LAM
    s10 = sphere_backscatter(x10)
    ipk = np.argmax(s)
    fig, ax = plt.subplots(figsize=(5.4, 3.9))
    for lo, hi, name in ((0.05, 0.5, "Rayleigh"), (0.5, 4.0, "resonance"), (4.0, 30, "optical")):
        if name == "resonance":
            ax.axvspan(lo, hi, color=SHADE, alpha=0.7, lw=0)
        ax.text(np.sqrt(lo * hi), 7.5, name, ha="center", va="center", fontsize=12.5, color=GRAY)
    xr = x[x < 0.9]
    ax.plot(xr, 9 * xr ** 4, color=GRAY, lw=1.0, ls=(0, (4, 3)))
    ax.text(0.16, 9 * 0.16 ** 4 * 2.2, r"$9x^4$", color=GRAY, fontsize=12, ha="right")
    ax.axhline(1, color=GRAY, lw=1.0, ls=(0, (4, 3)))
    ax.plot(x, s, color=NAVY, lw=2.2)
    ax.plot(x10, s10, "o", color=RED, ms=6, zorder=5)
    ax.annotate("10 cm sphere\nat 10 GHz", xy=(x10, s10), xytext=(x10, 0.12), ha="center", va="top",
                fontsize=12, color=RED, arrowprops=dict(arrowstyle="-", color=RED, lw=0.8))
    ax.annotate(f"peak {s[ipk]:.1f}", xy=(x[ipk], s[ipk]), xytext=(0.3, 2.2), ha="right", va="center",
                fontsize=12, color=NAVY, arrowprops=dict(arrowstyle="-", color=NAVY, lw=0.8))
    ax.set_xscale("log"); ax.set_yscale("log")
    ax.set_xlim(0.05, 30); ax.set_ylim(1e-4, 14)
    ax.set_xticks([0.1, 1, 10]); ax.set_xticklabels(["0.1", "1", "10"])
    ax.set_yticks([1e-4, 1e-3, 1e-2, 1e-1, 1, 10])
    ax.set_yticklabels(["0.0001", "0.001", "0.01", "0.1", "1", "10"])
    ax.set_xlabel(r"circumference in wavelengths, $2\pi a/\lambda$")
    ax.set_ylabel(r"$\sigma\ /\ \pi a^2$")
    ax.grid(color=RULE, lw=0.6, which="major")
    ax.set_axisbelow(True)
    print(f"sphere: peak {s[ipk]:.2f} at x = {x[ipk]:.2f}; 10 cm sphere x = {x10:.2f}, sigma/pi a^2 = {s10:.3f}")
    finalize(fig, "L25-sphere-regions")


# ------------------------------------------------------------- corner in 3D
_VIEW = np.array([1.0, 0.42, 0.55]); _VIEW /= np.linalg.norm(_VIEW)
_RIGHT = np.cross([0, 0, 1.0], _VIEW); _RIGHT /= np.linalg.norm(_RIGHT)
_UP = np.cross(_VIEW, _RIGHT)


def _iso(p):
    """Orthographic view from _VIEW, z up, so the inside of the corner shows."""
    p = np.asarray(p, float)
    return np.array([p @ _RIGHT, p @ _UP])


def corner_3d() -> None:
    a = 1.0
    faces = {  # each face is a right triangle with legs a, on one coordinate plane
        "x": [(0, 0, 0), (0, a, 0), (0, 0, a)],
        "y": [(0, 0, 0), (a, 0, 0), (0, 0, a)],
        "z": [(0, 0, 0), (a, 0, 0), (0, a, 0)],
    }
    # trace one ray: it reverses one component of its direction at each face
    d = -np.array([0.316, 0.89, 0.329]); d /= np.linalg.norm(d)
    p = np.array([0.0, 0.428, 0.389]) - 1.3 * d         # aimed at the back wall, from outside
    start = p.copy()
    hits = []
    for _ in range(3):
        ts = [(-p[k] / d[k], k) for k in range(3) if d[k] < 0]
        t, k = min(ts)
        p = p + t * d
        q = p.copy(); q[k] = 0
        assert q.min() >= -1e-9 and q.sum() - q[k] <= a + 1e-9, "bounce lands off the face"
        hits.append((p.copy(), k))
        d = d.copy(); d[k] = -d[k]
    assert np.all(d > 0)
    end = p + 1.7 * d
    fig, ax = plt.subplots(figsize=(4.6, 4.2))
    fills = {"x": "#dbe8f4", "y": "#e6eef6", "z": "#cfdfee"}
    for key in ("z", "x", "y"):
        poly = np.array([_iso(v) for v in faces[key]])
        ax.add_patch(Polygon(poly, closed=True, fc=fills[key], ec=NAVY, lw=1.6, alpha=0.95))
    pts = [start] + [h[0] for h in hits] + [end]
    P = np.array([_iso(v) for v in pts])
    ax.plot(P[:-1, 0], P[:-1, 1], color=RED, lw=1.5)
    ax.add_patch(FancyArrowPatch(P[0], P[0] + 0.55 * (P[1] - P[0]), arrowstyle="-|>", mutation_scale=13, color=RED, lw=1.5))
    ax.add_patch(FancyArrowPatch(P[-2], P[-1], arrowstyle="-|>", mutation_scale=13, color=RED, lw=1.5))
    names = {0: "x", 1: "y", 2: "z"}
    hq = np.array([_iso(h) for h, _ in hits])
    centroid = hq.mean(axis=0)
    for i, ((h, k), q) in enumerate(zip(hits, hq), 1):
        ax.plot(*q, "o", color=RED, ms=5, zorder=5)
        u = q - centroid; u /= np.linalg.norm(u)            # label away from the other bounces
        ax.text(*(q + 0.09 * u), f"{i}: flips ${names[k]}$", fontsize=12, color=INK, bbox=BOX,
                ha="left" if u[0] >= 0 else "right", va="bottom" if u[1] >= 0 else "top")
    ax.text(*(P[0] + np.array([0.0, 0.07])), "in", color=RED, fontsize=12, ha="center", va="bottom")
    ax.text(*(P[-1] + np.array([0.0, 0.07])), "out", color=RED, fontsize=12, ha="center", va="bottom")
    allp = np.vstack([P] + [np.array([_iso(v) for v in f]) for f in faces.values()])
    pad = 0.18
    ax.set_xlim(allp[:, 0].min() - pad, allp[:, 0].max() + pad + 0.25)
    ax.set_ylim(allp[:, 1].min() - pad, allp[:, 1].max() + pad)
    ax.set_aspect("equal"); ax.axis("off")
    finalize(fig, "L25-corner-3d")


# ------------------------------------------------------------- RCS equivalent
def rcs_equivalent() -> None:
    phi = np.linspace(0, 2 * np.pi, 721)
    # a target's scattered power pattern: a few lobes, one of them toward the radar (phi = pi)
    lobes = [(np.pi, 0.62, 0.22), (np.deg2rad(115), 1.0, 0.18), (np.deg2rad(250), 0.75, 0.2),
             (np.deg2rad(20), 0.45, 0.3)]
    rr = 0.08 + sum(g * np.exp(-0.5 * ((np.angle(np.exp(1j * (phi - c)))) / w) ** 2) for c, g, w in lobes)
    back = 0.08 + sum(g * np.exp(-0.5 * ((np.angle(np.exp(1j * (np.pi - c)))) / w) ** 2) for c, g, w in lobes)
    fig, axes = plt.subplots(1, 2, figsize=(5.4, 2.7))
    for ax in axes:
        ax.set_aspect("equal"); ax.axis("off")
        ax.set_xlim(-2.35, 1.35); ax.set_ylim(-1.25, 1.25)
        # the radar, off to the left
        ax.add_patch(Polygon([(-2.25, -0.16), (-2.25, 0.16), (-1.95, 0.0)], closed=True, fc=NAVY, ec="none"))
        ax.text(-2.1, -0.3, "radar", ha="center", va="top", fontsize=12, color=NAVY)
        ax.plot([-1.9, -back], [0, 0], color=GRAY, lw=0.8, ls=(0, (2, 2)))
        ax.plot(-back, 0, "o", color=RED, ms=6, zorder=6)
    ax = axes[0]
    ax.fill(rr * np.cos(phi), rr * np.sin(phi), color=SHADE, ec=BLUE, lw=1.6)
    ax.add_patch(Polygon([(-0.12, -0.09), (0.1, -0.12), (0.16, 0.06), (-0.04, 0.14)], closed=True, fc=INK, ec="none"))
    ax.text(0.0, -1.2, "real target", ha="center", va="bottom", fontsize=12.5)
    ax = axes[1]
    ax.add_patch(Circle((0, 0), back, fc=SHADE, ec=BLUE, lw=1.6))
    ax.add_patch(Circle((0, 0), 0.13, fc=INK, ec="none"))
    ax.text(0.0, -1.2, r"isotropic, area $\sigma$", ha="center", va="bottom", fontsize=12.5)
    fig.subplots_adjust(wspace=0.04)
    finalize(fig, "L25-rcs-equivalent")


def main() -> int:
    OUT.mkdir(parents=True, exist_ok=True)
    print(f"P_r = {PR:.2f} dBm, N = {N:.1f} dBm, SNR = {SNR:.2f} dB")
    level_diagram()
    falloff()
    sphere_regions()
    corner_3d()
    rcs_equivalent()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
