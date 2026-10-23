#!/usr/bin/env python3
"""L20 illustration-sweep figures (lesson page).

  L20-null-comb.svg       the broadside course-array pattern on a sin(theta)
                          axis, where the nulls are a comb with teeth every
                          lambda/Nd = 0.260 and the fourth falls outside the
                          visible region, and on a theta axis, where the same
                          nulls land at 15.1, 31.3, and 51.2 degrees
  L20-steering-cone.svg   the main lobe of a linear array as a band about the
                          array axis, at broadside and steered to 60 degrees:
                          the band thickens by 1/cos(theta0) and its
                          circumference shrinks by cos(theta0), so the
                          array-factor directivity barely moves

Course array: N = 8, d = 14 mm, worked at 10.3 GHz. Every number on a label
is computed here. Labels only; the equations are in the lesson text.

    python3 scripts/graphics/l20_figures.py
    -> book/extras/viz/img/L20-null-comb.svg, L20-steering-cone.svg
"""

from __future__ import annotations
import io
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import ConnectionPatch
from svg_font_stack import apply_font_stack

NAVY, BLUE, RED, GREEN, ORANGE, GRAY = "#004a85", "#0067b9", "#b01e24", "#1d7a4d", "#e67e22", "#5a5a5a"
INK, RULE, SHADE = "#1a1a1a", "#c7d2e0", "#eef1f5"
ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "book/extras/viz/img"

C = 299792458.0
LAM = C / 10.3e9 * 1000.0          # mm, the worked example's 10.3 GHz
N, D_MM = 8, 14.0
DL = D_MM / LAM                     # 0.481
SPACING = 1 / (N * DL)              # lambda/Nd = 0.260

plt.rcParams.update({
    "svg.fonttype": "none", "font.size": 12, "text.color": INK,
    "axes.edgecolor": "#8a929c", "axes.labelcolor": INK,
    "xtick.color": GRAY, "ytick.color": GRAY, "axes.linewidth": 1.0,
})


def finalize(fig, name: str) -> None:
    buf = io.StringIO()
    fig.savefig(buf, format="svg", transparent=True, bbox_inches="tight", pad_inches=0.06)
    plt.close(fig)
    s = buf.getvalue()
    s = apply_font_stack(s[s.index("<svg"):])
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / f"{name}.svg").write_text(s, encoding="utf-8")
    print(f"wrote {name}.svg -> {OUT}")


def af_db(s, s0=0.0, floor=-40.0):
    """Uniform array factor in dB against u = sin(theta), steered to sin(theta0) = s0."""
    psi = 2 * np.pi * DL * (s - s0)
    den = N * np.sin(psi / 2)
    small = np.abs(den) < 1e-12
    a = np.where(small, 1.0, np.sin(N * psi / 2) / np.where(small, 1.0, den))
    return np.clip(20 * np.log10(np.clip(np.abs(a), 1e-9, None)), floor, None)


def directivity(th0_deg: float) -> float:
    """Array-factor directivity of isotropic elements, integrated over the sphere."""
    t = np.linspace(0, np.pi, 200001)                     # angle from the array axis
    psi = 2 * np.pi * DL * (np.cos(t) - np.sin(np.deg2rad(th0_deg)))
    af2 = np.abs(np.exp(1j * np.outer(psi, np.arange(N))).sum(1)) ** 2
    return 2 * af2.max() / np.trapezoid(af2 * np.sin(t), t)


def hpbw_exact(th0_deg: float) -> float:
    deg = np.linspace(-90, 90, 360001)
    db = af_db(np.sin(np.deg2rad(deg)), np.sin(np.deg2rad(th0_deg)), floor=-200)
    i0 = np.argmin(np.abs(deg - th0_deg))
    a = i0
    while db[a] >= -3.0103:
        a -= 1
    b = i0
    while db[b] >= -3.0103:
        b += 1
    return deg[b] - deg[a]


def null_comb() -> None:
    nulls_s = SPACING * np.arange(1, 5)                   # 0.260 ... 1.040
    vis = nulls_s[nulls_s <= 1]
    nulls_deg = np.rad2deg(np.arcsin(vis))
    assert np.allclose(np.round(nulls_deg, 1), [15.1, 31.3, 51.2]), nulls_deg

    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(6.6, 4.1),
                                   gridspec_kw=dict(hspace=0.45))
    s = np.linspace(-1.3, 1.3, 20001)
    ax1.axvspan(-1.3, -1, color=SHADE, lw=0)
    ax1.axvspan(1, 1.3, color=SHADE, lw=0)
    ax1.plot(s, af_db(s), color=NAVY, lw=1.6)
    ax1.set_xlim(-1.3, 1.3)
    ax1.set_ylim(-40, 3)
    ax1.set_yticks([-40, -20, 0])
    ax1.set_xticks([-1, -0.5, 0, 0.5, 1])
    ax1.set_xlabel("sine of the angle from broadside")
    ax1.xaxis.tick_top()
    ax1.xaxis.set_label_position("top")
    ax1.set_ylabel("power (dB)")
    for x in nulls_s:
        for sgn in (-1, 1):
            ax1.plot([sgn * x] * 2, [-40, -33], color=RED if x <= 1 else GRAY, lw=1.4)
    ax1.text(1.15, -9, "no real\nangle", ha="center", va="center", color=GRAY, fontsize=10.5)
    ax1.text(-1.15, -9, "no real\nangle", ha="center", va="center", color=GRAY, fontsize=10.5)
    ax1.annotate("", xy=(2 * SPACING, -37), xytext=(SPACING, -37),
                 arrowprops=dict(arrowstyle="<->", color=GREEN, lw=1.2))
    ax1.text(1.5 * SPACING, -35.5, f"{SPACING:.3f}", ha="center", va="bottom",
             color=GREEN, fontsize=11, fontweight="bold",
             bbox=dict(boxstyle="round,pad=0.1", fc="white", ec="none", alpha=0.9))
    ax1.annotate("", xy=(3 * SPACING, -37), xytext=(2 * SPACING, -37),
                 arrowprops=dict(arrowstyle="<->", color=GREEN, lw=1.2))
    ax1.text(2.5 * SPACING, -35.5, f"{SPACING:.3f}", ha="center", va="bottom",
             color=GREEN, fontsize=11, fontweight="bold",
             bbox=dict(boxstyle="round,pad=0.1", fc="white", ec="none", alpha=0.9))

    deg = np.linspace(-90, 90, 20001)
    ax2.plot(deg, af_db(np.sin(np.deg2rad(deg))), color=NAVY, lw=1.6)
    ax2.set_xlim(-90, 90)
    ax2.set_ylim(-40, 3)
    ax2.set_yticks([-40, -20, 0])
    ax2.set_xticks([-90, -60, -30, 0, 30, 60, 90])
    ax2.set_xlabel("angle from broadside (deg)")
    ax2.set_ylabel("power (dB)")
    for x, th in zip(vis, nulls_deg):
        for sgn in (-1, 1):
            ax2.plot([sgn * th] * 2, [-40, -33], color=RED, lw=1.4)
            con = ConnectionPatch(xyA=(sgn * x, -40), coordsA=ax1.transData,
                                  xyB=(sgn * th, 3), coordsB=ax2.transData,
                                  color=RED, lw=0.9, ls=(0, (3, 3)), alpha=0.7)
            fig.add_artist(con)
        ax2.text(th, -31, f"{th:.1f}°", ha="center", va="bottom", color=RED,
                 fontsize=10.5, fontweight="bold",
                 bbox=dict(boxstyle="round,pad=0.12", fc="white", ec="none", alpha=0.85))
    ax1.spines[["bottom", "right"]].set_visible(False)
    ax2.spines[["top", "right"]].set_visible(False)
    finalize(fig, "L20-null-comb")


def band(ax, th0_deg: float, width_deg: float, color: str, label: bool) -> None:
    """The main lobe as a band of directions about the array axis (x)."""
    alpha_c = np.deg2rad(90 - th0_deg)                   # cone half-angle from the axis
    half = np.deg2rad(width_deg / 2)
    phi = np.linspace(0, 2 * np.pi, 121)
    a = np.linspace(max(alpha_c - half, 0.0), alpha_c + half, 9)
    P, A = np.meshgrid(phi, a)
    X, Y, Z = np.cos(A), np.sin(A) * np.cos(P), np.sin(A) * np.sin(P)
    ax.plot_surface(X, Y, Z, color=color, alpha=0.55, linewidth=0, shade=False)
    for edge in (a[0], a[-1]):
        ax.plot(np.cos(edge) * np.ones_like(phi), np.sin(edge) * np.cos(phi),
                np.sin(edge) * np.sin(phi), color=NAVY, lw=0.9)
    ax.plot([-1.25, 1.25], [0, 0], [0, 0], color=INK, lw=1.4)
    if label:
        ax.text(-1.25, 0, 0.1, "array axis", color=GRAY, fontsize=12, ha="left", va="bottom")
    ax.set_xlim(-1, 1); ax.set_ylim(-1, 1); ax.set_zlim(-1, 1)
    ax.set_box_aspect((1, 1, 1), zoom=1.45)
    ax.view_init(elev=18, azim=-62)
    ax.set_axis_off()


def steering_cone() -> None:
    w0, w60 = hpbw_exact(0), hpbw_exact(60)
    d0, d60 = 10 * np.log10(directivity(0)), 10 * np.log10(directivity(60))
    assert abs(d0 - 8.86) < 0.01 and abs(d60 - 9.12) < 0.01, (d0, d60)
    fig = plt.figure(figsize=(7.0, 3.4))
    ax1 = fig.add_subplot(1, 2, 1, projection="3d")
    ax2 = fig.add_subplot(1, 2, 2, projection="3d")
    band(ax1, 0, w0, BLUE, label=False)
    band(ax2, 60, w60, ORANGE, label=True)
    fig.text(0.27, 0.95, "broadside", ha="center", fontsize=14, fontweight="bold", color=INK)
    fig.text(0.75, 0.95, "steered to 60°", ha="center", fontsize=14, fontweight="bold", color=INK)
    fig.text(0.27, 0.02, f"band {w0:.1f}° thick, full circle\ndirectivity {d0:.2f} dB",
             ha="center", fontsize=13, color=INK)
    fig.text(0.75, 0.02, f"band {w60:.1f}° thick, circumference halved\ndirectivity {d60:.2f} dB",
             ha="center", fontsize=13, color=INK)
    fig.subplots_adjust(left=0, right=1, top=0.95, bottom=0.14, wspace=0.02)
    finalize(fig, "L20-steering-cone")


if __name__ == "__main__":
    null_comb()
    steering_cone()
