#!/usr/bin/env python3
"""Generate the L19 (Direction Finding) figures as inline SVG.

  - L19-sweep        : the beam sweep's output against steer angle, source at +30 deg
  - L19-sweep-grid   : the same sweep near its peak, on the 7-bit steering grid
  - L19-two-bearings : the worked example, two stations on the firing line, the fix
  - L19-crossing     : the error region of a 90 deg and a 30 deg crossing
  - L19-depth        : a firing-line pair 0.75 m and 3 m apart, the same box, the depth ellipse
  - L19-reflection   : a direct lobe, a -10 dB reflection lobe, and their sum
  - L19-cone         : the cone of directions a line array cannot tell apart
  - L19-resolution   : two sources 20 deg apart and 8 deg apart
  - L19-residuals    : five bearings, one bent by a reflection, and their residuals
  - L19-room-bearing : heading, Angle, and the room bearing they add to
  - L19-bearing-line : one bearing line, its unit vectors, and n.x = n.p

The lesson page shows all eleven from book/extras/viz/img/. None carries an
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
    # The lobe's own slope at its half-power points, in units of 1/theta_HP.
    th = np.radians(np.linspace(-20, 20, 40001))
    psi = np.radians(KD_DEG) * np.sin(th)
    v = np.abs(np.exp(1j * np.multiply.outer(psi, np.arange(N))).sum(-1)) / N
    i = np.argmin(np.abs(v - 1 / np.sqrt(2)))
    out["slope_k"] = abs(np.gradient(v, th)[i]) * np.radians(out["hpbw"])
    out["noise_30dB"] = out["hpbw"] / (out["slope_k"] * np.sqrt(2 * 10 ** 3.0))
    out["noise_16"] = out["hpbw"] / (1.6 * np.sqrt(2 * 10 ** 3.0))
    out["grid_sd"] = out["step_30"] / np.sqrt(12)
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
    assert f"{v['slope_k']:.2f}" == "1.05"
    assert f"{v['noise_30dB']:.1f}" == "0.3" and f"{v['noise_16']:.1f}" == "0.2"
    assert f"{v['grid_sd']:.2f}" == "0.30"
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
    ax.text(pk + 0.3, 0.12, f"Angle {pk:.1f}°", color=NAVY, fontsize=13, va="bottom")
    # the grid step that brackets the source
    a, b = g[g <= THETA_S][-1], g[g > THETA_S][0]
    ya = -2.35
    ax.annotate("", xy=(a, ya), xytext=(b, ya),
                arrowprops=dict(arrowstyle="<->", color=GRAY, lw=1.0, shrinkA=0, shrinkB=0))
    # beside the arrow, clear of the source line that runs through its middle
    ax.text(b + 0.25, ya, f"{b - a:.2f}°", color=GRAY, fontsize=13, ha="left", va="center")
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
    """Two stations on the firing line, 2 m apart, every kit facing +y.

    Angle is positive toward +x, so a reading theta_i at station x_i puts the
    source on the line x = x_i + y tan(theta_i). Each reading is about 1 deg
    toward +x of the true angle."""
    xA, xB = -1.0, 1.0
    box = np.array([0.25, 1.75])
    thA, thB = 36.6, -22.4
    tA, tB = np.tan(np.radians(thA)), np.tan(np.radians(thB))
    y = (xB - xA) / (tA - tB)
    x = xA + y * tA
    fix = np.array([x, y])
    true = [np.degrees(np.arctan((box[0] - xi) / box[1])) for xi in (xA, xB)]
    out = dict(xA=xA, xB=xB, box=box, thA=thA, thB=thB, fix=fix,
               miss=np.linalg.norm(fix - box), true=true, gamma=thA - thB)
    # the page's numbers
    assert (f"{tA:.3f}", f"{-tB:.3f}") == ("0.743", "0.412")
    assert (f"{x:.2f}", f"{y:.2f}") == ("0.29", "1.73")
    assert f"{out['miss']:.2f}" == "0.04"
    assert (f"{true[0]:.1f}", f"{true[1]:.1f}") == ("35.5", "-23.2")
    assert (f"{thA - true[0]:.1f}", f"{thB - true[1]:.1f}") == ("1.1", "0.8")
    assert f"{out['gamma']:.1f}" == "59.0"
    # the least-squares form gives the same point (room bearing beta = 90 - theta)
    n = np.array([[-np.sin(np.radians(90 - a)), np.cos(np.radians(90 - a))] for a in (thA, thB)])
    P = np.array([[xA, 0.0], [xB, 0.0]])
    xs = np.linalg.solve(n.T @ n, n.T @ np.sum(n * P, axis=1))
    assert np.allclose(xs, fix)
    return out


def three_bearing_example() -> None:
    """The page's least-squares worked example: three stations, every number
    it prints, asserted. Nothing is drawn."""
    xs = np.array([-0.75, 0.0, 0.75])
    th = np.array([34.6, 8.8, -17.7])
    c, s = np.cos(np.radians(th)), np.sin(np.radians(th))
    n = np.stack([-c, s], axis=1)
    P = np.stack([xs, np.zeros_like(xs)], axis=1)
    d = np.sum(n * P, axis=1)
    M, b = n.T @ n, n.T @ d
    fix = np.linalg.solve(M, b)
    f3 = lambda a: [f"{v:.3f}" for v in np.ravel(a)]
    assert f3(c) == ["0.823", "0.988", "0.953"] and f3(s) == ["0.568", "0.153", "-0.304"]
    assert f3(d) == ["0.617", "0.000", "-0.714"]
    assert f3(M) == ["2.562", "-0.329", "-0.329", "0.438"] and f3(b) == ["0.173", "0.568"]
    # the page works the inverse from the rounded entries it prints
    assert f"{2.562 * 0.438 - 0.329 ** 2:.3f}" == "1.014"
    assert f"{(0.438 * 0.173 + 0.329 * 0.568) / 1.014:.2f}" == "0.26"
    assert f"{(2.562 * 0.568 + 0.329 * 0.173) / 1.014:.2f}" == "1.49"
    assert [f"{v:.2f}" for v in fix] == ["0.26", "1.49"]
    assert f"{np.linalg.norm(fix - np.array([0.25, 1.5])):.2f}" == "0.01"
    e = n @ fix - d
    assert f3(e) == ["0.016", "-0.028", "0.015"], e
    own = np.linalg.norm(fix - P, axis=1) * np.tan(np.radians(1.5))
    assert np.all(np.abs(e) < own) and np.allclose(own, 0.04, atol=0.008), own
    print(f"   three-bearing example: fix {fix.round(3)}, residuals {e.round(3)}")


def fig_two_bearings(w: dict) -> None:
    fig, ax = plt.subplots(figsize=(4.4, 3.5))
    ax.plot([-1.5, 1.5], [0, 0], color=LIGHT, lw=2.0, solid_capstyle="butt")
    for xs in np.arange(-1.5, 1.51, 0.5):
        ax.plot([xs, xs], [-0.06, 0.06], color=LIGHT, lw=1.2)
    top = 2.05
    for xi, th, lab, side in ((w["xA"], w["thA"], "A", -1), (w["xB"], w["thB"], "B", 1)):
        t = np.tan(np.radians(th))
        ax.plot([xi, xi + top * t], [0, top], color=BLUE, lw=1.4)
        ax.plot([xi - 0.22, xi + 0.22], [0, 0], color=NAVY, lw=4, solid_capstyle="butt")
        ax.annotate("", xy=(xi, 0.55), xytext=(xi, 0.0),
                    arrowprops=dict(arrowstyle="-|>", color=GRAY, lw=1.0, ls="--", mutation_scale=10))
        ax.text(xi, -0.12, lab, ha="center", va="top", fontsize=13, color=NAVY)
        # the reading, outside its line at 42% of the way up
        yl = 0.42 * top
        ax.text(xi + yl * t + side * 0.07, yl, f"{th:+.1f}°".replace("-", "−"),
                color=BLUE, fontsize=13, ha="left" if side > 0 else "right", va="center")
    # the origin at the middle of the tape, x along it, y downrange
    ax.plot(0, 0, "o", ms=4, color=GRAY)
    ax.text(0, -0.12, "0", color=GRAY, fontsize=13, ha="center", va="top")
    ax.annotate("", xy=(1.62, 0), xytext=(1.5, 0),
                arrowprops=dict(arrowstyle="-|>", color=GRAY, lw=1.0, mutation_scale=10,
                                shrinkA=0, shrinkB=0))
    ax.text(1.66, 0, "x", color=GRAY, fontsize=13, ha="left", va="center", style="italic")
    # A's right triangle: y up, then x - x_A across to the fix
    f = w["fix"]
    ax.plot([w["xA"], w["xA"]], [0.55, f[1]], color=GRAY, lw=0.9, ls=":")
    ax.plot([w["xA"], f[0]], [f[1], f[1]], color=GRAY, lw=0.9, ls=":")
    ax.text((w["xA"] + f[0]) / 2 - 0.15, f[1] + 0.06, r"$x - x_A$", color=GRAY, fontsize=14,
            ha="center", va="bottom")
    ax.text(w["xA"] - 0.06, 0.7 * f[1], r"$y$", color=GRAY, fontsize=14, ha="right", va="center")
    bx = w["box"]
    ax.add_patch(Rectangle((bx[0] - 0.11, bx[1] - 0.11), 0.22, 0.22, fill=False, ec=GRAY, lw=1.2))
    ax.plot(*w["fix"], "o", ms=5, color=RED)
    ax.text(bx[0] + 0.17, bx[1] - 0.05, "fix", color=RED, fontsize=13, ha="left", va="top")
    ax.text(bx[0] + 0.17, bx[1] + 0.03, "box", color=GRAY, fontsize=13, ha="left", va="bottom")
    ax.annotate("", xy=(w["xB"], -0.6), xytext=(w["xA"], -0.6),
                arrowprops=dict(arrowstyle="<->", color=GRAY, lw=1.0, shrinkA=0, shrinkB=0))
    ax.text(0.5, -0.56, "2 m", color=GRAY, fontsize=13, ha="center", va="bottom")
    ax.set_xlim(-1.65, 1.65)
    ax.set_ylim(-0.75, 2.1)
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


def af_mag(psi):
    """L16's normalized array factor magnitude, |AF_N(psi)|."""
    psi = np.asarray(psi, float)
    return np.abs(np.exp(1j * np.multiply.outer(psi, np.arange(N))).sum(-1)) / N


def ls_fix(P, theta_deg, sigma_deg=None):
    """Least-squares fix from stations P (k x 2) on the firing line, every kit
    facing +y, Angle positive toward +x. Returns the fix, the normals, and
    (with sigma) the error covariance."""
    beta = np.radians(90.0 - np.asarray(theta_deg))
    n = np.stack([-np.sin(beta), np.cos(beta)], axis=1)
    A = n.T @ n
    x = np.linalg.solve(A, n.T @ np.sum(n * P, axis=1))
    return x, n


def depth_case(B, y=2.0, sigma_deg=1.5):
    P = np.array([[-B / 2, 0.0], [B / 2, 0.0]])
    box = np.array([0.0, y])
    R = np.hypot(B / 2, y)
    d = R * np.radians(sigma_deg)
    th = [np.degrees(np.arctan((box[0] - p[0]) / box[1])) for p in P]
    _, n = ls_fix(P, th)
    M = (n.T @ n) / d ** 2
    C = np.linalg.inv(M)
    return P, box, th, d, C


def fig_depth() -> None:
    """Choosing Where to Measure: the depth error for two baselines."""
    fig, axes = plt.subplots(1, 2, figsize=(4.6, 3.3))
    for ax, B, want in zip(axes, (0.75, 3.0), ("0.20", "0.08")):
        P, box, th, d, C = depth_case(B)
        sy = np.sqrt(C[1, 1])
        assert f"{sy:.2f}" == want, (B, sy)
        assert np.isclose(sy, np.sqrt(2) * (B ** 2 / 4 + box[1] ** 2) * np.radians(1.5) / B, rtol=1e-6)
        ax.plot([-1.6, 1.6], [0, 0], color=LIGHT, lw=2.0, solid_capstyle="butt")
        for xm in (-1.5, -0.75, 0.0, 0.75, 1.5):
            ax.plot([xm, xm], [-0.05, 0.05], color=LIGHT, lw=1.2)
        for p, a in zip(P, th):
            u = np.array([np.sin(np.radians(a)), np.cos(np.radians(a))])
            nn = np.array([-u[1], u[0]])
            far = 2.75
            # the +-delta strip at the box's range, widening from the kit
            L = np.linalg.norm(box - p)
            strip = np.array([p, p + far * u + (far / L) * d * nn, p + far * u - (far / L) * d * nn])
            ax.add_patch(Polygon(strip, closed=True, fc=BLUE, alpha=0.16, ec="none"))
            ax.plot([p[0], p[0] + far * u[0]], [p[1], p[1] + far * u[1]], color=BLUE, lw=1.1)
            ax.plot([p[0] - 0.13, p[0] + 0.13], [0, 0], color=NAVY, lw=4, solid_capstyle="butt")
        ev, evec = np.linalg.eigh(C)
        ang = np.degrees(np.arctan2(evec[1, 1], evec[0, 1]))
        ax.add_patch(Ellipse(box, 2 * np.sqrt(ev[1]), 2 * np.sqrt(ev[0]), angle=ang,
                             fill=False, ec=RED, lw=1.6))
        ax.plot(*box, "o", ms=3.5, color=RED)
        # depth label outside the triangle, left of the left-hand line
        yl = 0.8 * box[1]
        xl = P[0][0] + (box[0] - P[0][0]) * yl / box[1]
        ax.text(xl - 0.22, yl, f"±{sy:.2f} m", color=RED, fontsize=13, ha="right", va="center")
        ax.annotate("", xy=(B / 2, -0.28), xytext=(-B / 2, -0.28),
                    arrowprops=dict(arrowstyle="<->", color=GRAY, lw=1.0, shrinkA=0, shrinkB=0))
        ax.text(0.0, -0.38, f"B = {B:g} m", color=GRAY, fontsize=13, ha="center", va="top")
        ax.set_xlim(-1.65, 1.65)
        ax.set_ylim(-0.75, 2.75)
        ax.set_aspect("equal")
        ax.axis("off")
    fig.subplots_adjust(wspace=0.05)
    finalize(fig, "L19-depth")


def reflection_case(adb=-10.0):
    """Worst pull on the peak over reflection offsets 5-15 deg and every phase,
    source at broadside."""
    th = np.linspace(-25, 25, 5001)
    kd = np.radians(KD_DEG)
    a = 10 ** (adb / 20)
    A0 = np.exp(1j * np.multiply.outer(kd * np.sin(np.radians(th)), np.arange(N))).sum(-1) / N
    best = (0.0, None, None)
    for sep in np.arange(5.0, 15.01, 0.25):
        A1 = np.exp(1j * np.multiply.outer(kd * (np.sin(np.radians(th)) - np.sin(np.radians(sep))),
                                           np.arange(N))).sum(-1) / N
        for ph in np.linspace(0, 2 * np.pi, 120, endpoint=False):
            s = np.abs(A0 + a * np.exp(1j * ph) * A1)
            pk = th[np.argmax(s)]
            if abs(pk) > best[0]:
                best = (abs(pk), sep, ph)
    return best, th


def fig_reflection() -> None:
    (shift, sep, ph), th = reflection_case(-10.0)
    assert f"{shift:.1f}" == "2.0", shift
    kd = np.radians(KD_DEG)
    a = 10 ** (-10 / 20)
    s0 = np.sin(np.radians(th))
    A0 = np.exp(1j * np.multiply.outer(kd * s0, np.arange(N))).sum(-1) / N
    A1 = np.exp(1j * np.multiply.outer(kd * (s0 - np.sin(np.radians(sep))), np.arange(N))).sum(-1) / N
    tot = np.abs(A0 + a * np.exp(1j * ph) * A1)
    db = lambda v: np.clip(20 * np.log10(np.maximum(v, 1e-6)), -30, 3)
    fig, ax = plt.subplots(figsize=(4.4, 2.75))
    ax.plot(th, db(np.abs(A0)), color=LIGHT, lw=1.2, ls="--")
    ax.plot(th, db(a * np.abs(A1)), color=AMBER, lw=1.2, ls="--")
    ax.plot(th, db(tot), color=BLUE, lw=1.8)
    pk = th[np.argmax(tot)]
    ax.axvline(0, color=GRAY, lw=0.8, ls=":")
    ax.annotate("", xy=(pk, 4.2), xytext=(0, 4.2),
                arrowprops=dict(arrowstyle="-|>", color=RED, lw=1.2, shrinkA=0, shrinkB=0, mutation_scale=10))
    ax.text(pk + 0.8, 4.2, f"{abs(pk):.1f}°", color=RED, fontsize=13, va="center",
            ha="left" if pk > 0 else "right")
    # labels in the empty regions: left of the direct lobe, right of the reflection
    # a stacked key in the empty upper left, above the left sidelobes
    for y, lab, col in ((3.0, "sum", BLUE), (-1.5, "direct", GRAY), (-6.0, "reflection", AMBER)):
        ax.text(-24.5, y, lab, color=col, fontsize=13, ha="left", va="center")
    ax.set_xlim(-25, 25)
    ax.set_ylim(-30, 6)
    ax.set_xticks([-20, -10, 0, 10, 20])
    ax.set_yticks([-30, -20, -10, 0])
    ax.set_xlabel("steer angle (deg)")
    ax.set_ylabel("sum (dB)")
    style(ax)
    print(f"   reflection: worst shift {shift:.2f} deg at offset {sep:.2f} deg")
    finalize(fig, "L19-reflection")


def fig_cone() -> None:
    """Directions with the same Angle form a cone around the array's axis."""
    from mpl_toolkits.mplot3d import Axes3D  # noqa: F401
    v = numbers()
    s = np.sin(np.radians(v["cone_30"]))          # x-component every cone direction shares
    fig = plt.figure(figsize=(4.4, 3.3))
    ax = fig.add_axes([0.0, 0.0, 0.62, 1.0], projection="3d")
    ax.view_init(elev=16, azim=-58)
    ax.plot([-0.3, 0.3], [0, 0], [0, 0], color=NAVY, lw=5, solid_capstyle="butt")
    phi = np.linspace(-np.pi / 2 + 0.05, np.pi / 2 - 0.05, 121)
    r = np.sqrt(1 - s ** 2)
    rim = np.stack([np.full_like(phi, s), r * np.cos(phi), r * np.sin(phi)])
    ax.plot(*rim, color=BLUE, lw=1.4)
    for p in np.linspace(-1.3, 1.3, 7):
        q = np.array([s, r * np.cos(p), r * np.sin(p)])
        ax.plot([0, q[0]], [0, q[1]], [0, q[2]], color=BLUE, lw=0.6, alpha=0.45)
    az, el = np.radians(30.0), np.radians(-v["el"])
    flat = np.array([np.sin(az), np.cos(az), 0.0])
    src = np.array([np.sin(az) * np.cos(el), np.cos(az) * np.cos(el), np.sin(el)])
    assert np.isclose(src[0], s)                      # the source sits on the 29.0 deg cone
    ax.plot([0, flat[0]], [0, flat[1]], [0, flat[2]], color=GRAY, lw=1.2, ls="--")
    ax.plot([0, src[0]], [0, src[1]], [0, src[2]], color=RED, lw=1.8)
    ax.set_xlim(-0.4, 0.8)
    ax.set_ylim(0, 1.1)
    ax.set_zlim(-0.6, 0.6)
    ax.set_box_aspect((1.2, 1.1, 1.2))
    ax.set_axis_off()
    # the key sits in its own column to the right, clear of the drawing
    for y, lab, col in ((0.80, "array", NAVY),
                        (0.64, "30° on the\nfloor plan", GRAY),
                        (0.40, f"source {v['el']:.0f}°\ndown: reads\n{v['cone_30']:.1f}°", RED),
                        (0.14, f"every line on\nthe cone reads\n{v['cone_30']:.1f}°", BLUE)):
        fig.text(0.64, y, lab, color=col, fontsize=13, ha="left", va="center")
    finalize(fig, "L19-cone")


def fig_resolution() -> None:
    """Two incoherent sources: 20 deg apart resolve, 8 deg apart merge."""
    th = np.linspace(-30, 30, 3001)
    kd = np.radians(KD_DEG)
    fig, axes = plt.subplots(1, 2, figsize=(4.6, 2.6), sharey=True)
    for ax, sep in zip(axes, (20.0, 8.0)):
        a, b = -sep / 2, sep / 2
        pa = af_mag(kd * (np.sin(np.radians(th)) - np.sin(np.radians(a)))) ** 2
        pb = af_mag(kd * (np.sin(np.radians(th)) - np.sin(np.radians(b)))) ** 2
        tot = pa + pb
        db = 10 * np.log10(tot / tot.max())
        ax.plot(th, np.clip(db, -20, 1), color=BLUE, lw=1.6)
        # local maxima above -3 dB
        pk = [th[i] for i in range(1, len(th) - 1)
              if tot[i] >= tot[i - 1] and tot[i] > tot[i + 1] and db[i] > -3]
        for s in (a, b):
            ax.axvline(s, color=RED, lw=0.9, ls="--")
        assert len(pk) == (2 if sep == 20.0 else 1), (sep, pk)
        ax.set_title(f"{sep:.0f}° apart: {'two peaks' if len(pk) == 2 else 'one peak'}",
                     fontsize=13, color=INK, pad=4)
        ax.set_xlim(-30, 30)
        ax.set_ylim(-20, 1.5)
        ax.set_xticks([-20, 0, 20])
        ax.set_xlabel("steer angle (deg)")
        style(ax)
    axes[0].set_ylabel("sum (dB)")
    axes[0].set_yticks([-20, -10, 0])
    fig.subplots_adjust(wspace=0.1)
    finalize(fig, "L19-resolution")


def residual_case():
    """All five stations; the middle one reads 10 deg off, as a reflection that
    took over the peak would make it. The other bearings are exact, so their
    residuals are only the pull of the bad line on the fix."""
    xs = np.array([-1.5, -0.75, 0.0, 0.75, 1.5])
    P = np.stack([xs, np.zeros_like(xs)], axis=1)
    src = np.array([0.25, 1.5])
    meas = np.degrees(np.arctan((src[0] - xs) / src[1]))
    meas[2] -= 10.0
    fix, n = ls_fix(P, meas)
    e = np.sum(n * (fix - P), axis=1)
    R = np.linalg.norm(fix - P, axis=1)          # each station's range to the fix
    return xs, P, src, meas, fix, n, e, R


def fig_residuals() -> None:
    xs, P, src, meas, fix, n, e, R = residual_case()
    ok = np.abs(e) * 100
    own = R * np.tan(np.radians(2.0)) * 100
    # the bad bearing has the largest residual, about 2.5 times the next and
    # over 3 times its own R tan(2 deg); one bad line pulls the others up too
    assert np.argmax(ok) == 2 and ok[2] > 2.5 * np.delete(ok, 2).max() and ok[2] > 3 * own[2], ok
    # the page's test: only the bad bearing misses by more than 3 R_i tan(sigma)
    assert list(np.flatnonzero(ok > 3 * own)) == [2], (ok, own)
    fig, ax = plt.subplots(figsize=(4.4, 3.2))
    ax.plot([-1.6, 1.6], [0, 0], color=LIGHT, lw=2.0, solid_capstyle="butt")
    for i, (p, a) in enumerate(zip(P, meas)):
        u = np.array([np.sin(np.radians(a)), np.cos(np.radians(a))])
        bad = i == 2
        ax.plot([p[0], p[0] + 1.75 / u[1] * u[0]], [0, 1.75],
                color=RED if bad else BLUE, lw=1.6 if bad else 1.1)
        ax.plot([p[0] - 0.13, p[0] + 0.13], [0, 0], color=NAVY, lw=4, solid_capstyle="butt")
        ax.text(p[0], -0.1, f"{ok[i]:.0f} cm", color=RED if bad else INK, fontsize=13,
                ha="center", va="top")
    ax.plot(*fix, "+", ms=11, mew=2, color=INK)
    # the bad station's R (to the fix) and e (the fix's perpendicular miss)
    ax.plot([P[2][0], fix[0]], [0, fix[1]], color=GRAY, lw=1.0, ls="--")
    mid = (P[2] + fix) / 2
    ax.text(mid[0] + 0.06, mid[1], r"$R$", color=GRAY, fontsize=15, ha="left", va="center")
    foot = fix - e[2] * n[2]
    ax.plot([fix[0], foot[0]], [fix[1], foot[1]], color=RED, lw=2.0)
    ax.text(foot[0] - 0.06, foot[1] + 0.02, r"$e$", color=RED, fontsize=15, ha="right", va="center")
    ax.add_patch(Rectangle((src[0] - 0.1, src[1] - 0.1), 0.2, 0.2, fill=False, ec=GRAY, lw=1.2))
    ax.set_xlim(-1.65, 1.65)
    ax.set_ylim(-0.4, 1.8)
    ax.set_aspect("equal")
    ax.axis("off")
    print(f"   residuals (cm) {ok.round(1)}, fix {fix.round(3)}, own R tan2 (cm) {own.round(1)}")
    finalize(fig, "L19-residuals")


def arc(ax, c, r, a0, a1, color=INK, lw=1.1):
    """An arc of radius r about c from angle a0 to a1, in degrees CCW from +x."""
    t = np.radians(np.linspace(a0, a1, 60))
    ax.plot(c[0] + r * np.cos(t), c[1] + r * np.sin(t), color=color, lw=lw)


def fig_room_bearing() -> None:
    """Room axis, the kit's broadside at heading h, Angle from broadside, and the
    room bearing beta = h + theta_est, all CCW seen from above."""
    h, th = 30.0, 35.0
    b = h + th
    fig, ax = plt.subplots(figsize=(4.4, 2.9))
    p = np.array([0.0, 0.0])
    u = lambda a: np.array([np.cos(np.radians(a)), np.sin(np.radians(a))])
    # room axis, beta = 0
    ax.plot([0, 2.25], [0, 0], color=GRAY, lw=1.1, ls="--")
    ax.text(2.25, -0.08, "room axis", color=GRAY, fontsize=13, ha="right", va="top")
    # the array, perpendicular to broadside, and broadside itself
    v = u(h + 90)
    ax.plot(*np.stack([p - 0.3 * v, p + 0.3 * v]).T, color=NAVY, lw=5, solid_capstyle="butt")
    ax.plot(*np.stack([p, p + 1.55 * u(h)]).T, color=GRAY, lw=1.1, ls=":")
    ax.text(*(p + 1.6 * u(h)), "broadside", color=GRAY, fontsize=13, ha="left", va="bottom")
    # the bearing toward the source
    ax.annotate("", xy=p + 1.6 * u(b), xytext=p,
                arrowprops=dict(arrowstyle="-|>", color=BLUE, lw=1.6, mutation_scale=12))
    ax.plot(*(p + 1.7 * u(b)), "o", ms=7, color=RED)
    ax.text(*(p + 1.7 * u(b) + np.array([-0.1, 0.0])), "source", color=RED, fontsize=13,
            ha="right", va="center")
    ax.text(*(p + np.array([0.05, -0.3])), "kit", color=NAVY, fontsize=13, ha="left", va="top")
    # the three angles
    arc(ax, p, 0.5, 0, h, color=GRAY)
    ax.text(*(p + 0.66 * u(h / 2)), r"$h$", color=GRAY, fontsize=16, ha="center", va="center")
    arc(ax, p, 0.9, h, b, color=INK)
    ax.text(*(p + 1.12 * u(h + th / 2)), r"$\theta_\mathrm{est}$", color=INK, fontsize=16,
            ha="center", va="center")
    arc(ax, p, 1.3, 0, b, color=BLUE)
    ax.text(*(p + 1.45 * u(22)), r"$\beta$", color=BLUE, fontsize=17, ha="center", va="center")
    ax.set_xlim(-0.45, 2.3)
    ax.set_ylim(-0.4, 1.75)
    ax.set_aspect("equal")
    ax.axis("off")
    finalize(fig, "L19-room-bearing")


def fig_bearing_line() -> None:
    """One bearing from a kit at p: the ray along u, the normal n, and why every
    point x on the line has the same n.x: its distance from the origin along n.

    The hats are combining circumflexes in plain text; mathtext's \\hat comes
    apart under svg.fonttype none."""
    beta = 35.0
    u = np.array([np.cos(np.radians(beta)), np.sin(np.radians(beta))])
    n = np.array([-u[1], u[0]])
    p = np.array([0.4, 0.9])
    x = p + 1.3 * u
    foot = n * (n @ p)
    fig, ax = plt.subplots(figsize=(4.4, 3.3))
    # room axes from the origin
    for d, lab in (((1, 0), "x"), ((0, 1), "y")):
        ax.annotate("", xy=(0.4 * d[0], 0.4 * d[1]), xytext=(0, 0),
                    arrowprops=dict(arrowstyle="-|>", color=GRAY, lw=1.0, mutation_scale=10,
                                    shrinkA=0, shrinkB=0))
        ax.text(0.47 * d[0], 0.47 * d[1], lab, color=GRAY, fontsize=13,
                ha="center", va="center", style="italic")
    ax.plot(0, 0, "o", ms=4, color=GRAY)
    ax.text(0.04, -0.06, "0", color=GRAY, fontsize=13, ha="left", va="top")
    # the bearing line: dashed behind the kit, solid ahead
    ax.plot(*np.stack([foot - 0.25 * u, p]).T, color=BLUE, lw=1.0, ls="--")
    ax.plot(*np.stack([p, p + 1.7 * u]).T, color=BLUE, lw=1.6)
    # position vectors from the origin
    for q, lab, off in ((p, "p", (0.12, -0.02)), (x, "x", (0.1, -0.1))):
        ax.annotate("", xy=q, xytext=(0, 0),
                    arrowprops=dict(arrowstyle="-|>", color=INK, lw=1.0, mutation_scale=10,
                                    shrinkA=0, shrinkB=4))
        ax.text(q[0] + off[0], q[1] + off[1], lab, color=INK, fontsize=15, ha="left",
                va="center", weight="bold")
    ax.plot(*x, "o", ms=5, color=INK)
    ax.plot(*p, "s", ms=8, color=NAVY, zorder=3)
    ax.text(p[0] - 0.1, p[1] + 0.06, "kit", color=NAVY, fontsize=13, ha="right", va="bottom")
    # the unit vectors at the kit
    for vec, lab, off in ((u, "u\u0302", (0.06, -0.14)), (n, "n\u0302", (-0.12, 0.02))):
        ax.annotate("", xy=p + 0.45 * vec, xytext=p,
                    arrowprops=dict(arrowstyle="-|>", color=RED, lw=1.6, mutation_scale=12,
                                    shrinkA=0, shrinkB=0))
        ax.text(*(p + 0.5 * vec + np.array(off)), lab, color=RED, fontsize=15,
                ha="center", va="center", weight="bold")
    # n.p: the distance from the origin to the line, the same for every point on it
    ax.plot(*np.stack([(0, 0), foot]).T, color=GREEN, lw=1.6)
    m = 0.55 * foot
    ax.text(m[0] - 0.08, m[1], "n\u0302\u00b7p", color=GREEN, fontsize=15, ha="right",
            va="center", weight="bold")
    ax.set_xlim(-0.85, 2.35)
    ax.set_ylim(-0.25, 1.95)
    ax.set_aspect("equal")
    ax.axis("off")
    finalize(fig, "L19-bearing-line")

def main() -> None:
    v = numbers()
    for k, x in v.items():
        print(f"   {k:12s} {x:.4f}")
    check_numbers(v)
    fig_sweep()
    fig_sweep_grid()
    fig_two_bearings(worked_example())
    three_bearing_example()
    fig_crossing()
    fig_depth()
    fig_reflection()
    fig_cone()
    fig_resolution()
    fig_residuals()
    fig_room_bearing()
    fig_bearing_line()


if __name__ == "__main__":
    main()
