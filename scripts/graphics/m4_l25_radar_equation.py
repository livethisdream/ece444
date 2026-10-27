#!/usr/bin/env python3
"""Generate the L25 (radar equation, path loss, and RCS) lesson-page figures.

  - L25-two-trips      : the radar equation as Friis twice: the outgoing
                         spreading sphere, the target re-radiating sigma times
                         the incident density, the return spreading sphere,
                         and the receive array's effective aperture
  - L25-rcs-shapes     : sphere, flat plate, and trihedral corner reflector,
                         each with an incident ray bundle and where the
                         scattered rays go
  - L25-rcs-aspect     : RCS versus aspect angle for a 10 cm square plate and
                         a trihedral with 10 cm edges at 10 GHz, with the
                         10 cm sphere as a flat line

The plate is physical optics: sigma = 4 pi (A/lambda)^2 cos^2(t) sinc^2(k a
sin t). The trihedral is geometric optics: sigma = 4 pi A_eff^2 / lambda^2,
where A_eff is the triple-bounce area, the overlap of the aperture triangle
projected along the look direction with its own point reflection through the
projected apex. On the symmetry axis that overlap is a hexagon of area
a^2/sqrt(3), which gives the textbook 4 pi a^4 / (3 lambda^2).

    python3 scripts/graphics/m4_l25_radar_equation.py
    -> book/extras/viz/img/L25-*.svg
"""

from __future__ import annotations
import io
from pathlib import Path

import numpy as np
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Arc, Circle, Polygon
from svg_font_stack import apply_font_stack

NAVY, BLUE, RED, GREEN, ORANGE, GRAY = "#004a85", "#0067b9", "#b01e24", "#1d7a4d", "#e67e22", "#5a5a5a"
INK, RULE = "#1a1a1a", "#c7d2e0"
ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "book/extras/viz/img"

C = 3e8
F = 10.0e9                      # the Module 4 carrier, COURSE_SPEC M8
LAM = C / F
A = 0.10                        # plate side, corner edge (M8, provisional), sphere diameter (m)

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


def finalize(fig, name: str) -> None:
    buf = io.StringIO()
    fig.savefig(buf, format="svg", transparent=True, bbox_inches="tight", pad_inches=0.06)
    plt.close(fig)
    s = buf.getvalue()
    s = s[s.index("<svg"):]
    s = apply_font_stack(s)
    (OUT / f"{name}.svg").write_text(s, encoding="utf-8")
    print(f"wrote {OUT / (name + '.svg')}")


def dbsm(x):
    return 10 * np.log10(np.maximum(x, 1e-30))


# ------------------------------------------------------------------ RCS models
def plate_rcs(t_deg):
    """Square plate of side A, rotated about one edge axis, physical optics."""
    t = np.deg2rad(t_deg)
    k = 2 * np.pi / LAM
    u = k * A * np.sin(t)
    sinc = np.where(np.abs(u) < 1e-9, 1.0, np.sin(u) / np.where(u == 0, 1, u))
    return 4 * np.pi * (A * A / LAM) ** 2 * np.cos(t) ** 2 * sinc ** 2


def _clip(subject, clip):
    """Sutherland-Hodgman: intersect two convex CCW polygons (lists of 2-vectors)."""
    out = subject
    for i in range(len(clip)):
        a, b = clip[i], clip[(i + 1) % len(clip)]
        edge = b - a
        inside = lambda p: edge[0] * (p[1] - a[1]) - edge[1] * (p[0] - a[0]) >= 0
        inp, out = out, []
        if not inp:
            break
        s = inp[-1]
        for e in inp:
            if inside(e):
                if not inside(s):
                    out.append(_isect(s, e, a, b))
                out.append(e)
            elif inside(s):
                out.append(_isect(s, e, a, b))
            s = e
    return out


def _isect(p1, p2, a, b):
    d1, d2 = p2 - p1, b - a
    den = d1[0] * d2[1] - d1[1] * d2[0]
    t = ((a[0] - p1[0]) * d2[1] - (a[1] - p1[1]) * d2[0]) / den
    return p1 + t * d1


def _area(poly):
    if len(poly) < 3:
        return 0.0
    x = np.array([p[0] for p in poly]); y = np.array([p[1] for p in poly])
    return 0.5 * abs(np.dot(x, np.roll(y, -1)) - np.dot(y, np.roll(x, -1)))


def corner_rcs(t_deg):
    """Triangular trihedral, edge A, swept in azimuth about its symmetry axis."""
    bore = np.ones(3) / np.sqrt(3)
    side = np.array([1.0, -1.0, 0.0]) / np.sqrt(2)          # azimuth plane
    verts = A * np.eye(3)
    out = []
    for t in np.deg2rad(np.atleast_1d(t_deg)):
        d = np.cos(t) * bore + np.sin(t) * side               # look direction
        e1 = np.cross(d, [0, 0, 1.0]); e1 /= np.linalg.norm(e1)
        e2 = np.cross(d, e1)
        tri = [np.array([v @ e1, v @ e2]) for v in verts]     # apex projects to 0
        if (tri[1][0] - tri[0][0]) * (tri[2][1] - tri[0][1]) - (tri[1][1] - tri[0][1]) * (tri[2][0] - tri[0][0]) < 0:
            tri = tri[::-1]
        refl = [-p for p in tri]                              # point reflection
        aeff = _area(_clip(tri, refl))
        out.append(4 * np.pi * aeff ** 2 / LAM ** 2)
    return np.array(out)


SPHERE = np.pi * (A / 2) ** 2


# ------------------------------------------------------------------ figures
def rcs_aspect() -> None:
    t = np.linspace(-45, 45, 1801)
    fig, ax = plt.subplots(figsize=(7.0, 3.9))
    ax.plot(t, dbsm(plate_rcs(t)), color=NAVY, lw=2.0, label="flat plate")
    ax.plot(t, dbsm(corner_rcs(t)), color=RED, lw=2.4, label="corner reflector")
    ax.axhline(dbsm(SPHERE), color=GREEN, lw=2.0, ls="--", label="sphere")
    ax.set_xlim(-45, 45)
    ax.set_ylim(-35, 6)
    ax.set_xticks(np.arange(-45, 46, 15))
    ax.set_xlabel("aspect angle (deg)")
    ax.set_ylabel("RCS (dBsm)")
    ax.grid(color=RULE, lw=0.7)
    ax.spines[["top", "right"]].set_visible(False)
    ax.legend(loc="upper right", fontsize=11.5, ncol=3, bbox_to_anchor=(1.0, 1.13))
    finalize(fig, "L25-rcs-aspect")


def two_trips() -> None:
    fig, ax = plt.subplots(figsize=(7.4, 3.3))
    ax.set_xlim(-0.4, 10.4); ax.set_ylim(-2.0, 1.6)
    ax.set_aspect("equal"); ax.axis("off")
    up, dn = 0.55, -0.55
    # radar: transmit antenna on the upper lane, receive array on the lower
    ax.add_patch(Polygon([[0.0, up], [0.5, up + 0.3], [0.5, up - 0.3]], closed=True, fc=NAVY, ec=NAVY))
    for i in range(8):
        ax.add_patch(plt.Rectangle((0.33, dn - 0.4 + i * 0.1), 0.17, 0.07, fc=BLUE, ec="none"))
    # target: corner reflector between the lanes
    tx = 9.4
    ax.add_patch(Polygon([[tx - 0.35, 0.42], [tx + 0.35, 0.42], [tx, -0.42]], closed=True, fc="#f3d7d8", ec=RED, lw=1.5))
    for x in (tx - 0.35, tx, tx + 0.35):
        ax.plot([tx, x], [0.0, 0.42], color=RED, lw=1.0)
    ax.text(tx, -0.75, "target", ha="center", fontsize=11, color=RED)
    # wavefronts: arcs about their source that open up as they travel
    for r in (1.6, 3.4, 5.2, 7.0):
        h = 0.12 + 0.055 * r
        half = np.rad2deg(np.arcsin(h / r))
        ax.add_patch(Arc((0.5, up), 2 * r, 2 * r, theta1=-half, theta2=half, color=NAVY, lw=1.4))
        ax.add_patch(Arc((tx - 0.1, dn), 2 * r, 2 * r, theta1=180 - half, theta2=180 + half, color=RED, lw=1.4))
    ax.annotate("", xy=(8.8, up), xytext=(0.7, up),
                arrowprops=dict(arrowstyle="-|>", color=NAVY, lw=1.6, mutation_scale=14))
    ax.annotate("", xy=(0.65, dn), xytext=(8.8, dn),
                arrowprops=dict(arrowstyle="-|>", color=RED, lw=1.6, mutation_scale=14))
    ax.text(0.0, 1.3, "transmit", ha="left", fontsize=11, color=NAVY)
    ax.text(4.7, 1.3, "trip 1: spreads over 4πR²", ha="center", fontsize=11.5, color=NAVY)
    ax.text(0.0, -1.45, "receive array", ha="left", fontsize=11, color=BLUE)
    ax.text(4.7, -1.45, "trip 2: spreads over 4πR² again", ha="center", fontsize=11.5, color=RED)
    ax.annotate("", xy=(0.5, -1.85), xytext=(tx, -1.85),
                arrowprops=dict(arrowstyle="<->", color=GRAY, lw=1.0))
    ax.text((0.5 + tx) / 2, -1.82, "R", ha="center", va="bottom", fontsize=12, color=GRAY, style="italic")
    finalize(fig, "L25-two-trips")


def _trace(p, d, segs, bounces):
    """Follow a 2-D ray through mirror segments; return the visited points and final direction."""
    pts = [p]
    for _ in range(bounces):
        best = None
        for a, b in segs:
            e = b - a
            den = d[0] * e[1] - d[1] * e[0]
            if abs(den) < 1e-12:
                continue
            s = ((a[0] - p[0]) * e[1] - (a[1] - p[1]) * e[0]) / den
            u = ((a[0] - p[0]) * d[1] - (a[1] - p[1]) * d[0]) / den
            if s > 1e-9 and 0 <= u <= 1 and (best is None or s < best[0]):
                best = (s, e)
        if best is None:
            break
        s, e = best
        p = p + s * d
        n = np.array([-e[1], e[0]]) / np.linalg.norm(e)
        d = d - 2 * (d @ n) * n
        pts.append(p)
    return pts, d


def rcs_shapes() -> None:
    fig, axes = plt.subplots(1, 3, figsize=(8.4, 2.9))
    for ax in axes:
        ax.set_xlim(-1.6, 1.6); ax.set_ylim(-1.35, 1.2)
        ax.set_aspect("equal"); ax.axis("off")
    ys = (-0.5, -0.25, 0.0, 0.25, 0.5)
    arrow = dict(arrowstyle="-|>", lw=1.3, mutation_scale=11)

    # sphere: each ray leaves along its own surface normal's mirror direction
    ax = axes[0]
    ax.add_patch(Circle((0.6, 0), 0.55, fc="#dcebdf", ec=GREEN, lw=1.6))
    for y in ys:
        xs = 0.6 - np.sqrt(0.55 ** 2 - y ** 2)
        ax.plot([-1.5, xs], [y, y], color=NAVY, lw=1.1)
        n = np.array([xs - 0.6, y]) / 0.55
        d = np.array([1.0, 0.0])
        r = d - 2 * (d @ n) * n
        ax.annotate("", xy=(xs + 0.7 * r[0], y + 0.7 * r[1]), xytext=(xs, y), arrowprops={**arrow, "color": RED})
    ax.text(0.0, -1.25, "sphere: spreads", ha="center", fontsize=11.5)

    # plate: a mirror, so normal incidence comes straight back
    ax = axes[1]
    ax.plot([0.6, 0.6], [-0.75, 0.75], color=NAVY, lw=4)
    for y in ys:
        ax.plot([-1.5, 0.58], [y, y], color=NAVY, lw=1.1)
    ax.annotate("", xy=(-0.9, 0.05), xytext=(0.55, 0.05), arrowprops={**arrow, "color": RED})
    ax.text(0.0, -1.25, "plate: mirrors", ha="center", fontsize=11.5)

    # corner (a section through two faces): two bounces send the ray back parallel
    ax = axes[2]
    apex = np.array([1.1, 0.0])
    top, bot = apex + [-0.8, 0.8], apex + [-0.8, -0.8]
    ax.plot([top[0], apex[0], bot[0]], [top[1], apex[1], bot[1]], color=NAVY, lw=4)
    th = np.deg2rad(15)
    d0 = np.array([np.cos(th), np.sin(th)])
    for y0 in (-0.3, -0.5):
        pts, d = _trace(np.array([-1.5, y0]), d0, [(top, apex), (apex, bot)], 2)
        xs, ys_ = zip(*pts)
        ax.plot(xs, ys_, color=NAVY, lw=1.1)
        ax.annotate("", xy=pts[-1] + 2.2 * d, xytext=pts[-1], arrowprops={**arrow, "color": RED})
    ax.text(0.0, -1.25, "corner: returns", ha="center", fontsize=11.5)
    fig.subplots_adjust(wspace=0.05)
    finalize(fig, "L25-rcs-shapes")


def main() -> int:
    OUT.mkdir(parents=True, exist_ok=True)
    pk = corner_rcs([0.0])[0]
    print(f"lambda = {LAM*1e3:.2f} mm")
    print(f"corner peak {dbsm(pk):.2f} dBsm (formula {dbsm(4*np.pi*A**4/(3*LAM**2)):.2f})")
    t = np.linspace(0, 45, 4501)
    cr = dbsm(corner_rcs(t)) - dbsm(pk)
    print(f"corner -3 dB at +/-{t[np.argmax(cr < -3)]:.1f} deg, -6 dB at {t[np.argmax(cr < -6)]:.1f}")
    pl = dbsm(plate_rcs(t)) - dbsm(plate_rcs(0.0))
    print(f"plate peak {dbsm(plate_rcs(0.0)):.2f} dBsm, -3 dB at {t[np.argmax(pl < -3)]:.2f} deg, sphere {dbsm(SPHERE):.2f}")
    rcs_aspect()
    two_trips()
    rcs_shapes()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
