#!/usr/bin/env python3
"""Generate the L19 (Direction Finding) figures as inline SVG.

  - L19-sweep        : the beam sweep's output against steer angle, source at +30 deg
  - L19-sweep-grid   : the same sweep near its peak, on the 7-bit steering grid
  - L19-two-bearings : the worked example, two kits, two bearing lines, the fix
  - L19-crossing     : the error region of a 90 deg and a 30 deg crossing

The lesson page shows all four from book/extras/viz/img/. None carries an
equation: symbols, numbers, and short words only.

Each figure sits in a present block beside text, about 477 px wide on a 1280
laptop and 343 px on a phone. They are drawn about 420 units wide with no text
under 13 units, so the smallest label is 10.5 px or more on the phone;
check_text() asserts it on the written file.

Every number a figure shows is computed here and asserted against the value the
page prints, so the two cannot drift apart.

    python3 scripts/graphics/m3_l19_direction_finding.py
"""

from __future__ import annotations

import io
import re
from pathlib import Path
from svg_font_stack import apply_font_stack

import numpy as np
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
from matplotlib.patches import Ellipse, Polygon, Rectangle  # noqa: E402

NAVY, BLUE, RED, GREEN, AMBER, GRAY = "#004a85", "#0067b9", "#b01e24", "#1d7a4d", "#8a5a00", "#5a5a5a"
INK, RULE, LIGHT = "#1a1a1a", "#c7d2e0", "#9fb1c2"

IMG = Path(__file__).resolve().parents[2] / "book/extras/viz/img"

# Course array at the HB100's frequency, with the course's c = 3e8.
C, F, D, N = 3.0e8, 10.525e9, 0.014, 8
LAM = C / F
KD_DEG = 360.0 * D / LAM                # 176.8 deg of phase per unit of sin(theta)
LSB = 360.0 / 2 ** 7                    # 2.8125 deg, the ADAR1000's phase step
S_STEP = LSB / KD_DEG                   # the sweep's step in sin(theta)
THETA_S = 30.0                          # the source in the sweep figures

PHONE_COL, PX_MIN = 343.0, 10.5

plt.rcParams.update(
    {
        "svg.fonttype": "none",
        "svg.hashsalt": "ece444-L19",
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
    """Every label is 10.5 px or more at a 343 px column."""
    vb = re.search(r'viewBox="0 0 ([\d.]+) ([\d.]+)"', svg)
    w = float(vb.group(1))
    sizes = [float(x) for x in re.findall(r"font-size:\s*([\d.]+)px", svg)]
    smallest = min(sizes) * PHONE_COL / w
    print(f"   {name}: viewBox {w:.0f} x {float(vb.group(2)):.0f}, smallest text "
          f"{min(sizes):.1f} units = {smallest:.1f} px at a {PHONE_COL:.0f} px column")
    assert smallest >= PX_MIN - 0.05, f"{name}: {smallest:.2f} px text on a phone"


def finalize(fig, name: str) -> None:
    buf = io.StringIO()
    fig.savefig(buf, format="svg", transparent=True, bbox_inches="tight", pad_inches=0.06,
                metadata={"Date": None})
    plt.close(fig)
    s = buf.getvalue()
    s = s[s.index("<svg"):]
    s = apply_font_stack(s)
    (IMG / f"{name}.svg").write_text(s, encoding="utf-8")
    print(f"wrote {IMG / (name + '.svg')}")
    check_text(name, s)


def sweep_db(steer_deg, source_deg=THETA_S, floor=-40.0):
    """Sum of the eight elements, steered to steer_deg, for a source at source_deg.

    The arrival ramp is n kd sin(theta_s); the steering delay takes away
    n kd sin(theta_0). What is left is L16's array factor in
    psi = kd (sin theta_s - sin theta_0), normalized to its peak."""
    psi = np.radians(KD_DEG) * (np.sin(np.radians(source_deg)) - np.sin(np.radians(steer_deg)))
    n = np.arange(N)
    af = np.abs(np.exp(1j * np.multiply.outer(psi, n)).sum(-1)) / N
    return np.clip(20 * np.log10(np.clip(af, 1e-9, None)), floor, 0.0)


def grid_angles(lo=-80.0, hi=80.0):
    """The steer angles the sweep can set: whole LSBs of progressive phase."""
    m = np.arange(-60, 61)
    s = m * S_STEP
    th = np.degrees(np.arcsin(s[np.abs(s) <= 1]))
    return th[(th >= lo) & (th <= hi)]


def style(ax):
    for side in ("top", "right"):
        ax.spines[side].set_visible(False)
    ax.tick_params(length=3)


# ---------------------------------------------------------------- numbers --

def numbers() -> dict:
    out = {}
    out["lam_mm"] = LAM * 1e3
    out["kd"] = KD_DEG
    out["s_step"] = S_STEP
    for t in (0, 30, 45):
        out[f"step_{t}"] = np.degrees(S_STEP / np.cos(np.radians(t)))
    out["hpbw"] = np.degrees(0.886 * LAM / (N * D))
    out["null_sin"] = LAM / (N * D)
    out["null_deg"] = np.degrees(np.arcsin(LAM / (N * D)))
    el = np.degrees(np.arctan(0.75 / 3.0))
    out["el"] = el
    out["cone_30"] = np.degrees(np.arcsin(np.sin(np.radians(30)) * np.cos(np.radians(el))))
    out["cone_45"] = np.degrees(np.arcsin(np.sin(np.radians(45)) * np.cos(np.radians(el))))
    out["noise_30dB"] = out["hpbw"] / (1.6 * np.sqrt(2 * 10 ** 3.0))
    out["rss"] = np.sqrt((out["step_30"] / 2) ** 2 + 1.0 ** 2 + 1.0 ** 2 + out["noise_30dB"] ** 2)
    out["rss_eye"] = np.sqrt((out["step_30"] / 2) ** 2 + 3.0 ** 2 + 1.0 ** 2 + out["noise_30dB"] ** 2)
    return out


def check_numbers(v: dict) -> None:
    """The values the page prints."""
    assert f"{v['lam_mm']:.1f}" == "28.5"
    assert f"{v['kd']:.1f}" == "176.8"
    assert f"{v['s_step']:.4f}" == "0.0159"
    assert [f"{v[f'step_{t}']:.2f}" for t in (0, 30, 45)] == ["0.91", "1.05", "1.29"]
    assert f"{v['step_30'] / 2:.2f}" == "0.53"
    assert f"{v['hpbw']:.1f}" == "12.9"
    assert f"{v['null_sin']:.3f}" == "0.254" and f"{v['null_deg']:.1f}" == "14.7"
    assert f"{v['el']:.1f}" == "14.0"
    assert f"{v['cone_30']:.1f}" == "29.0" and f"{v['cone_45']:.1f}" == "43.3"
    assert f"{v['noise_30dB']:.1f}" == "0.2"
    assert f"{v['rss']:.1f}" == "1.5" and f"{v['rss_eye']:.1f}" == "3.2"


# ---------------------------------------------------------------- figures --

def fig_sweep() -> None:
    th = np.linspace(-80, 80, 3201)
    g = grid_angles()
    fig, ax = plt.subplots(figsize=(4.4, 2.75))
    ax.plot(th, sweep_db(th), color=LIGHT, lw=1.2)
    ax.plot(g, sweep_db(g), "o", ms=2.6, color=BLUE)
    pk = g[np.argmax(sweep_db(g))]
    ax.axvline(THETA_S, color=RED, lw=1.0, ls="--")
    ax.text(THETA_S + 6, -27, "source\nat 30°", color=RED, fontsize=13, va="top")
    ax.set_xlim(-80, 80)
    ax.set_ylim(-40, 3)
    ax.set_xticks([-60, -30, 0, 30, 60])
    ax.set_yticks([-40, -30, -20, -10, 0])
    ax.set_xlabel("steer angle (deg)")
    ax.set_ylabel("sum (dB)")
    style(ax)
    assert abs(pk - THETA_S) < 0.53
    finalize(fig, "L19-sweep")


def fig_sweep_grid() -> None:
    th = np.linspace(24, 36, 1201)
    g = grid_angles(24, 36)
    y = sweep_db(g)
    pk = g[np.argmax(y)]
    step = np.degrees(S_STEP / np.cos(np.radians(THETA_S)))
    fig, ax = plt.subplots(figsize=(4.4, 2.75))
    ax.plot(th, sweep_db(th), color=LIGHT, lw=1.2)
    ax.plot(g, y, "o", ms=4.5, color=BLUE)
    ax.plot([pk], [sweep_db(np.array([pk]))[0]], "o", ms=8, mfc="none", mec=NAVY, mew=1.6)
    ax.axvline(THETA_S, color=RED, lw=1.0, ls="--")
    ax.text(THETA_S - 0.25, -1.5, "source", color=RED, fontsize=13, ha="right")
    ax.text(pk + 0.3, 0.12, f"Est. Angle {pk:.1f}°", color=NAVY, fontsize=13, va="bottom")
    # the grid step that brackets the source
    a, b = g[g <= THETA_S][-1], g[g > THETA_S][0]
    ya = -2.35
    ax.annotate("", xy=(a, ya), xytext=(b, ya),
                arrowprops=dict(arrowstyle="<->", color=GRAY, lw=1.0, shrinkA=0, shrinkB=0))
    ax.text(0.5 * (a + b), ya + 0.1, f"{b - a:.2f}°", color=GRAY, fontsize=13, ha="center", va="bottom")
    ax.set_xlim(24, 36)
    ax.set_ylim(-3.2, 0.9)
    ax.set_xticks([24, 27, 30, 33, 36])
    ax.set_yticks([-3, -2, -1, 0])
    ax.set_xlabel("steer angle (deg)")
    ax.set_ylabel("sum (dB)")
    style(ax)
    assert abs(pk - THETA_S) <= step / 2
    assert f"{b - a:.2f}" in ("1.05", "1.06")
    print(f"   sweep-grid: Est. Angle {pk:.2f}, step {b - a:.3f}")
    finalize(fig, "L19-sweep-grid")


def worked_example() -> dict:
    """Kits A and B 4 m apart, box at (2, 3); each Est. Angle reads about 1 deg high."""
    pA, pB = np.array([0.0, 0.0]), np.array([4.0, 0.0])
    box = np.array([2.0, 3.0])
    hA, hB = 60.0, 120.0
    thA, thB = -2.6, 4.8
    bA, bB = hA + thA, hB + thB
    gamma = bB - bA
    b = np.linalg.norm(pB - pA)
    rA = b * np.sin(np.radians(180.0 - bB)) / np.sin(np.radians(gamma))
    fix = pA + rA * np.array([np.cos(np.radians(bA)), np.sin(np.radians(bA))])
    true = [np.degrees(np.arctan2(*(box - p)[::-1])) for p in (pA, pB)]
    out = dict(pA=pA, pB=pB, box=box, hA=hA, hB=hB, bA=bA, bB=bB, gamma=gamma, rA=rA,
               fix=fix, miss=np.linalg.norm(fix - box), true=true)
    # the page's numbers
    assert (f"{bA:.1f}", f"{bB:.1f}", f"{gamma:.1f}") == ("57.4", "124.8", "67.4")
    assert f"{rA:.2f}" == "3.56"
    assert (f"{fix[0]:.2f}", f"{fix[1]:.2f}") == ("1.92", "3.00")
    assert f"{out['miss']:.2f}" == "0.08"
    assert (f"{true[0]:.1f}", f"{true[1]:.1f}") == ("56.3", "123.7")
    # the least-squares form gives the same point
    n = np.array([[-np.sin(np.radians(x)), np.cos(np.radians(x))] for x in (bA, bB)])
    P = np.array([pA, pB])
    x = np.linalg.solve(n.T @ n, n.T @ np.sum(n * P, axis=1))
    assert np.allclose(x, fix)
    return out


def draw_kit(ax, p, heading, label, ha):
    """An array bar across the heading, and a short heading arrow."""
    h = np.radians(heading)
    u = np.array([np.cos(h), np.sin(h)])
    t = np.array([-u[1], u[0]]) * 0.28
    ax.plot([p[0] - t[0], p[0] + t[0]], [p[1] - t[1], p[1] + t[1]], color=NAVY, lw=4, solid_capstyle="butt")
    ax.annotate("", xy=p + 1.1 * u, xytext=p,
                arrowprops=dict(arrowstyle="-|>", color=GRAY, lw=1.0, ls="--", mutation_scale=10))
    ax.text(p[0], p[1] - 0.32, label, ha="center", va="top", fontsize=13, color=NAVY)


def fig_two_bearings(w: dict) -> None:
    fig, ax = plt.subplots(figsize=(4.4, 3.6))
    for p, b in ((w["pA"], w["bA"]), (w["pB"], w["bB"])):
        u = np.array([np.cos(np.radians(b)), np.sin(np.radians(b))])
        q = p + 4.3 * u
        ax.plot([p[0], q[0]], [p[1], q[1]], color=BLUE, lw=1.4)
    draw_kit(ax, w["pA"], w["hA"], "A", "center")
    draw_kit(ax, w["pB"], w["hB"], "B", "center")
    bx = w["box"]
    ax.add_patch(Rectangle((bx[0] - 0.15, bx[1] - 0.15), 0.3, 0.3, fill=False, ec=GRAY, lw=1.2))
    ax.plot(*w["fix"], "o", ms=6, color=RED)
    ax.text(w["fix"][0] - 0.25, w["fix"][1] + 0.12, "fix", color=RED, fontsize=13, ha="right")
    ax.text(bx[0] + 0.25, bx[1] - 0.2, "box", color=GRAY, fontsize=13, ha="left", va="top")
    ax.text(0.55, 0.32, f"{w['bA']:.1f}°", color=BLUE, fontsize=13)
    ax.text(3.45, 0.32, f"{w['bB']:.1f}°", color=BLUE, fontsize=13, ha="right")
    ax.annotate("", xy=(4.0, -0.75), xytext=(0.0, -0.75),
                arrowprops=dict(arrowstyle="<->", color=GRAY, lw=1.0, shrinkA=0, shrinkB=0))
    ax.text(2.0, -0.68, "4 m", color=GRAY, fontsize=13, ha="center", va="bottom")
    ax.set_xlim(-0.8, 4.8)
    ax.set_ylim(-0.95, 4.0)
    ax.set_aspect("equal")
    ax.axis("off")
    finalize(fig, "L19-two-bearings")


def crossing(gamma_deg: float, R=4.0, sigma_deg=2.0):
    """Two bearings at range R crossing at gamma: lines through the origin,
    their +-sigma strips, and the 1-sigma error ellipse."""
    angles = (90.0 - gamma_deg / 2, 90.0 + gamma_deg / 2)
    w = R * np.tan(np.radians(sigma_deg))
    J = np.zeros((2, 2))
    for b in angles:
        n = np.array([-np.sin(np.radians(b)), np.cos(np.radians(b))])
        J += np.outer(n, n) / w ** 2
    Cv = np.linalg.inv(J)
    ev, evec = np.linalg.eigh(Cv)
    rms = np.sqrt(ev.sum())
    return angles, w, ev, evec, rms


def fig_crossing() -> None:
    fig, axes = plt.subplots(1, 2, figsize=(4.6, 2.7))
    L = 0.9
    for ax, g in zip(axes, (90.0, 30.0)):
        angles, w, ev, evec, rms = crossing(g)
        for b in angles:
            u = np.array([np.cos(np.radians(b)), np.sin(np.radians(b))])
            n = np.array([-u[1], u[0]])
            far = 3.0
            strip = np.array([-far * u + w * n, far * u + w * n, far * u - w * n, -far * u - w * n])
            ax.add_patch(Polygon(strip, closed=True, fc=BLUE, alpha=0.13, ec="none"))
            ax.plot([-far * u[0], far * u[0]], [-far * u[1], far * u[1]], color=BLUE, lw=1.1)
        ang = np.degrees(np.arctan2(evec[1, 1], evec[0, 1]))
        ax.add_patch(Ellipse((0, 0), 2 * np.sqrt(ev[1]), 2 * np.sqrt(ev[0]), angle=ang,
                             fill=False, ec=RED, lw=1.6))
        ax.plot(0, 0, "o", ms=3.5, color=RED)
        ax.set_xlim(-L, L)
        ax.set_ylim(-L, L)
        ax.set_aspect("equal")
        ax.set_xticks([])
        ax.set_yticks([])
        for s in ax.spines.values():
            s.set_color(RULE)
        ax.set_title(f"{g:.0f}° crossing", fontsize=13, color=INK, pad=4)
        ax.text(0, -L + 0.06, f"RMS {rms:.2f} m", ha="center", va="bottom", fontsize=13, color=RED)
        print(f"   crossing {g:.0f}: semi-axes {np.sqrt(ev[0]):.2f}, {np.sqrt(ev[1]):.2f}, RMS {rms:.2f}")
    assert f"{crossing(90.0)[4]:.2f}" == "0.20" and f"{crossing(30.0)[4]:.2f}" == "0.40"
    fig.subplots_adjust(wspace=0.08)
    finalize(fig, "L19-crossing")


def main() -> None:
    v = numbers()
    for k, x in v.items():
        print(f"   {k:12s} {x:.4f}")
    check_numbers(v)
    fig_sweep()
    fig_sweep_grid()
    fig_two_bearings(worked_example())
    fig_crossing()


if __name__ == "__main__":
    main()
