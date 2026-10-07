#!/usr/bin/env python3
"""Generate the L18 (Beam Steering Theory) figures as inline SVG.

  - L18-path-difference   : plane wave at 30 deg off broadside, the d sin(theta0) leg
  - L18-phase-ramp        : the 30 deg ramp, unwrapped line vs wrapped bars
  - L18-sin-space         : the 30 deg pattern vs theta and vs sin(theta), nulls marked
  - L18-broadening        : projected aperture Nd cos(theta0)
  - L18-hpbw-vs-scan      : HPBW against theta0, 1/cos rule vs exact, and scan loss
  - L18-inverse-unwrap    : the inverse example's eight settings, unwrapped to +20 deg
  - L18-steered-patterns  : N=8 array steered to 0/30/45/60 deg (deck widget fallback)

Every figure is written to the deck tree (book/extras/slides/fig/); the ones the
lesson page shows are copied to book/extras/viz/img/. None carries an equation:
symbols, numbers, and short words only, so one file serves both trees.

The page figures sit in a present block beside text: about 477 px wide at a
1280 laptop and 343 px on a phone. They are drawn about 420 units wide with no
text under 13 units, so the smallest label is 10.5 px or more on the phone;
check_text() asserts it on the written file.

Every number a figure shows is computed here and asserted against the value the
page prints, so the two cannot drift apart.

    python3 scripts/graphics/m3_l18_steering.py
"""

from __future__ import annotations

import io
import re
import shutil
from pathlib import Path
from svg_font_stack import apply_font_stack

import numpy as np
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

NAVY, BLUE, RED, GREEN, AMBER, GRAY = "#004a85", "#0067b9", "#b01e24", "#1d7a4d", "#8a5a00", "#5a5a5a"
INK, RULE, LIGHT = "#1a1a1a", "#c7d2e0", "#9fb1c2"

FIG = Path(__file__).resolve().parents[2] / "book/extras/slides/fig"
IMG = Path(__file__).resolve().parents[2] / "book/extras/viz/img"

# Course array at the workshop frequency: d = 14 mm, lambda = 29.1 mm (10.3 GHz).
N, DL = 8, 14.0 / 29.1
KD_DEG = 360.0 * DL                     # 173.2 deg of phase per unit of sin(theta0)

# The page's smallest label, 10.5 px, at the narrowest column a figure gets (a
# 343 px phone column): a label of FS_MIN units in a W_PAGE-unit drawing.
PHONE_COL, PX_MIN, W_PAGE = 343.0, 10.5, 420.0
FS_MIN = 13.0

plt.rcParams.update(
    {
        "svg.fonttype": "none",
        "svg.hashsalt": "ece444-L18",    # stable clip-path ids: deterministic output
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


def check_text(name: str, svg: str, page: bool) -> None:
    """Every label on a page figure is 10.5 px or more at a 343 px column."""
    vb = re.search(r'viewBox="0 0 ([\d.]+) ([\d.]+)"', svg)
    w = float(vb.group(1))
    sizes = [float(x) for x in re.findall(r"font-size:\s*([\d.]+)px", svg)]
    smallest = min(sizes) * PHONE_COL / w
    print(f"   {name}: viewBox {w:.0f} x {float(vb.group(2)):.0f}, smallest text "
          f"{min(sizes):.1f} units = {smallest:.1f} px at a {PHONE_COL:.0f} px column")
    if page:
        assert smallest >= PX_MIN - 0.05, f"{name}: {smallest:.2f} px text on a phone"


def finalize(fig, name: str, also_page: bool = False) -> None:
    buf = io.StringIO()
    fig.savefig(buf, format="svg", transparent=True, bbox_inches="tight", pad_inches=0.06,
                metadata={"Date": None})
    plt.close(fig)
    s = buf.getvalue()
    s = s[s.index("<svg"):]
    s = apply_font_stack(s)
    (FIG / f"{name}.svg").write_text(s, encoding="utf-8")
    print(f"wrote {FIG / (name + '.svg')}")
    check_text(name, s, also_page)
    if also_page:
        shutil.copyfile(FIG / f"{name}.svg", IMG / f"{name}.svg")
        print(f"wrote {IMG / (name + '.svg')}")


def af(theta_deg, t0_deg):
    """Uniform N-element array factor (field), normalized to unity peak."""
    psi = 2 * np.pi * DL * (np.sin(np.radians(theta_deg)) - np.sin(np.radians(t0_deg)))
    num = np.sin(N * psi / 2.0)
    den = N * np.sin(psi / 2.0)
    with np.errstate(divide="ignore", invalid="ignore"):
        return np.where(np.abs(den) < 1e-12, 1.0, num / den)


def af_db(theta_deg, t0_deg, floor: float = -40.0):
    db = 20 * np.log10(np.clip(np.abs(af(theta_deg, t0_deg)), 1e-9, None))
    return np.clip(db, floor, 0.0)


def hpbw_rule(t0_deg):
    """L15's uniform-aperture width with the projected length Nd cos(theta0)."""
    return np.degrees(0.886 / (N * DL * np.cos(np.radians(t0_deg))))


def hpbw_exact(t0_deg: float) -> float:
    """The -3 dB width read off the array factor: half-power crossings found
    by bisection either side of the peak at theta0."""
    def edge(sign):
        lo, hi = t0_deg, t0_deg + sign * 40.0
        hi = float(np.clip(hi, -90.0, 90.0))
        for _ in range(80):
            mid = 0.5 * (lo + hi)
            if af(mid, t0_deg) ** 2 > 0.5:
                lo = mid
            else:
                hi = mid
        return 0.5 * (lo + hi)
    return edge(+1) - edge(-1)


def scan_loss_db(t0_deg):
    return 10 * np.log10(np.cos(np.radians(t0_deg)))


def clean(ax, left=True):
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    if not left:
        ax.spines["left"].set_visible(False)


# --------------------------------------------------------------------------- 1
def path_difference() -> None:
    """Two adjacent elements, a wave arriving 30 deg off broadside, and the
    extra leg the wavefront still has to travel to reach the farther element.
    Drawn at the page's angle, where that leg is exactly half of d."""
    T0 = 30.0
    t0 = np.radians(T0)
    u = np.array([np.sin(t0), np.cos(t0)])          # toward the source
    v = np.array([np.cos(t0), -np.sin(t0)])         # along a wavefront, down-right

    a, b = np.array([1.0, 0.0]), np.array([2.0, 0.0])   # the pair, d = 1
    leg = (b - a) @ u                                    # d sin(theta0)
    assert abs(leg - 0.5) < 1e-12, leg                   # half of d at 30 deg
    assert abs(14.0 * leg - 7.0) < 1e-9                  # the page's 7 mm
    dt_ps = 14e-3 * leg / 2.998e8 * 1e12
    assert round(dt_ps) == 23, dt_ps                     # "about 23 ps"
    foot = a + leg * u

    fig, ax = plt.subplots(figsize=(5.9, 3.0))
    ax.set_aspect("equal")
    ax.axis("off")

    xs = np.arange(4) * 1.0
    ax.plot([-0.35, 3.35], [0, 0], color=GRAY, lw=1.2, zorder=1)
    for x in xs:
        ax.add_patch(plt.Rectangle((x - 0.12, -0.08), 0.24, 0.16,
                                   facecolor="white", edgecolor=NAVY, lw=1.6, zorder=3))
    for i, x in enumerate(xs):
        if i in (1, 2):
            continue
        ax.text(x, -0.17, f"{i}", color=GRAY, fontsize=13, ha="center", va="top")
    ax.text(a[0], -0.17, "1", color=NAVY, fontsize=13, ha="center", va="top")
    ax.text(b[0], -0.17, "2", color=NAVY, fontsize=13, ha="center", va="top")
    ax.text(3.55, 0.0, "…", color=GRAY, fontsize=14, ha="center", va="center")

    # the spacing d: the pair's own segment of the array line
    ax.plot([a[0], b[0]], [0, 0], color=NAVY, lw=2.6, zorder=2)
    ax.text((a[0] + b[0]) / 2, -0.17, "d", color=NAVY, fontsize=15, ha="center", va="top",
            style="italic")

    # the wavefront that has just reached element 2
    reach = 2.25
    wf = np.array([b - reach * v, b + 0.15 * v])
    ax.plot(wf[:, 0], wf[:, 1], color=BLUE, lw=1.6, zorder=2)
    end = b - reach * v
    lab = end + 0.06 * u
    ax.text(lab[0], lab[1], "wavefront", color=BLUE, fontsize=13, ha="left", va="bottom",
            rotation=np.degrees(np.arctan2(v[1], v[0])), rotation_mode="anchor")

    # the extra leg, element 1 to that wavefront, with its right-angle mark
    ax.plot([a[0], foot[0]], [a[1], foot[1]], color=RED, lw=2.8, zorder=5,
            solid_capstyle="butt")
    m = 0.07
    corner = np.array([foot - m * u, foot - m * u + m * v, foot + m * v])
    ax.plot(corner[:, 0], corner[:, 1], color=INK, lw=0.9, zorder=5)

    # "extra path": its anchor is derived from the leg, not a fixed offset. It
    # sits off the leg's midpoint on the side away from element 2 (the -v
    # side), so it can never land inside the triangle, and its corner nearest
    # the leg is the anchor, so it clears the leg at any angle.
    mid = (a + foot) / 2
    off = mid - 0.11 * v
    ax.text(off[0], off[1], "extra path", color=RED, fontsize=13.5, ha="right", va="bottom",
            zorder=6)

    # broadside at element 2, the ray toward the source, and theta0 between them
    ax.plot([b[0], b[0]], [0, 1.55], color=GRAY, lw=1.1, ls=":", zorder=2)
    ax.text(b[0], 1.6, "broadside", color=GRAY, fontsize=13, ha="center", va="bottom")
    ax.plot([b[0], b[0] + 1.6 * u[0]], [0, 1.6 * u[1]], color=INK, lw=1.2, zorder=2)
    arc = np.linspace(0, t0, 60)
    r = 0.62
    ax.plot(b[0] + r * np.sin(arc), r * np.cos(arc), color=INK, lw=1.1)
    ax.text(b[0] + (r + 0.17) * np.sin(t0 / 2), (r + 0.17) * np.cos(t0 / 2),
            r"$\theta_0$", color=INK, fontsize=19, ha="center", va="center")

    # incoming wave, from the upper right along -u
    for s in (0.35, 0.75):
        start = b + s * v + 1.75 * u
        ax.annotate("", xy=start - 0.62 * u, xytext=start,
                    arrowprops=dict(arrowstyle="-|>", color=BLUE, lw=1.4, alpha=0.85))
    lab = b + 0.55 * v + 1.75 * u
    ax.text(lab[0] + 0.12, lab[1] + 0.05, "incoming\nwave", color=BLUE, fontsize=13,
            ha="left", va="bottom", linespacing=1.1)

    ax.set_xlim(-0.45, 4.05)
    ax.set_ylim(-0.42, 1.9)
    finalize(fig, "L18-path-difference", also_page=True)


# --------------------------------------------------------------------------- 2
def phase_ramp() -> None:
    """Commanded phases for theta0 = 30 deg: the straight unwrapped ramp and
    the sawtooth the hardware is actually given. The setting is +n dphi (a
    delay cancelling element n's lead), so the ramp rises."""
    dphi = KD_DEG * np.sin(np.radians(30.0))
    n = np.arange(N)
    unwrapped = n * dphi
    wrapped = unwrapped % 360.0
    assert np.allclose(np.round(unwrapped, 1),
                       [0, 86.6, 173.2, 259.8, 346.4, 433.0, 519.6, 606.2])
    assert np.allclose(np.round(wrapped, 1),
                       [0, 86.6, 173.2, 259.8, 346.4, 73.0, 159.6, 246.2])
    turned = unwrapped >= 360.0                     # one whole turn removed
    assert list(np.flatnonzero(turned)) == [5, 6, 7]

    fig, axes = plt.subplots(1, 2, figsize=(5.9, 2.1), gridspec_kw={"wspace": 0.42})
    ax = axes[0]
    ax.axhline(360, color=AMBER, lw=1.0, ls="--", zorder=1)
    ax.text(-0.3, 372, "one turn", color=AMBER, fontsize=13, ha="left", va="bottom")
    ax.plot(n, unwrapped, color=NAVY, lw=2.0, zorder=3)
    ax.scatter(n[~turned], unwrapped[~turned], s=30, color=NAVY, zorder=4)
    ax.scatter(n[turned], unwrapped[turned], s=30, color=AMBER, zorder=4)
    ax.set_title("commanded ramp", color=INK, fontsize=13.5, pad=6)
    ax.set_ylabel("phase (deg)")
    ax.set_ylim(-25, 660)
    ax.set_yticks([0, 180, 360, 540])

    ax = axes[1]
    ax.axhline(360, color=AMBER, lw=1.0, ls="--", zorder=1)
    ax.bar(n, wrapped, width=0.62, color=np.where(turned, AMBER, BLUE),
           edgecolor=np.where(turned, AMBER, NAVY), lw=1.0, zorder=3)
    ax.text(6.0, 300, "−360", color=AMBER, fontsize=13, ha="center", va="bottom")
    ax.set_title("what the hardware is given", color=INK, fontsize=13.5, pad=6)
    ax.set_ylim(0, 400)
    ax.set_yticks([0, 180, 360])
    for a in axes:
        a.set_xticks(n)
        a.set_xlim(-0.6, 7.6)
        a.set_xlabel("element number")
        clean(a)
    finalize(fig, "L18-phase-ramp", also_page=True)


# --------------------------------------------------------------------------- 3
def sin_space() -> None:
    """The steered pattern is a rigid shift in sin(theta), not in theta. At
    30 deg the first nulls sit +/-0.260 either side of 0.500 in sine (equal),
    which is 16.1 deg below and 19.5 deg above the peak in angle (not)."""
    T0 = 30.0
    step = 1.0 / (N * DL)                            # lambda / Nd
    s0 = np.sin(np.radians(T0))
    s_null = np.array([s0 - step, s0 + step])
    assert round(step, 3) == 0.260
    assert np.allclose(np.round(s_null, 3), [0.240, 0.760])
    # The page works from the sines as printed, 0.240 and 0.760: arcsin(0.760)
    # is 49.46 deg, so 49.5 and 19.5. (Unrounded, the null is at 49.45 deg.)
    th_null = np.degrees(np.arcsin(np.round(s_null, 3)))
    assert np.allclose(np.round(th_null, 1), [13.9, 49.5])
    assert np.allclose(np.round([T0 - th_null[0], th_null[1] - T0], 1), [16.1, 19.5])
    assert np.all(np.abs(np.degrees(np.arcsin(s_null)) - th_null) < 0.02)
    s_m2 = s0 + 2 * step
    assert round(s_m2, 3) == 1.020 and s_m2 > 1.0    # the m = +2 null is off the axis
    # the pattern is zero at the nulls, not merely low
    assert np.all(np.abs(af(np.degrees(np.arcsin(s_null)), T0)) < 1e-9)

    th = np.linspace(-90, 90, 6001)
    s = np.sin(np.radians(th))
    # No panel titles: the x-axis labels already say which is which, and the
    # figure has to fit beside four lines of text on a phone.
    fig, axes = plt.subplots(1, 2, figsize=(5.9, 2.45), sharey=True,
                             gridspec_kw={"wspace": 0.12})
    # null labels sit centered over their lines in a band above 0 dB; the
    # lines stop short of them, so each number reads as its own line's
    TOP, LINE_TOP = 10.0, 2.0

    ax = axes[0]
    ax.plot(th, af_db(th, 0.0), color=LIGHT, lw=1.5)
    ax.plot(th, af_db(th, T0), color=NAVY, lw=2.0)
    for x in th_null:
        ax.plot([x, x], [-40, LINE_TOP], color=RED, lw=1.1, ls=(0, (3, 2)), zorder=1)
        ax.text(x, TOP, f"{x:.1f}", color=RED, fontsize=13, ha="center", va="top")
    ax.text(-88, -9, "broadside", color=GRAY, fontsize=13, ha="left", va="center")
    ax.text(88, -9, "30°", color=NAVY, fontsize=13, ha="right", va="center")
    ax.set_xlim(-90, 90)
    ax.set_xticks([-90, -45, 0, 45, 90])
    ax.set_xlabel("angle (deg)")
    ax.set_ylabel("power (dB)")

    ax = axes[1]
    ax.axvspan(1.0, 1.1, color="#e9eef4", zorder=0, lw=0)
    ax.plot(s, af_db(th, 0.0), color=LIGHT, lw=1.5)
    ax.plot(s, af_db(th, T0), color=NAVY, lw=2.0)
    for x in s_null:
        ax.plot([x, x], [-40, LINE_TOP], color=RED, lw=1.1, ls=(0, (3, 2)), zorder=1)
        ax.text(x, TOP, f"{x:.3f}", color=RED, fontsize=13, ha="center", va="top")
    # the m = +2 null, past sin = 1 in the shaded strip no real angle reaches
    ax.plot([s_m2, s_m2], [-40, LINE_TOP], color=RED, lw=1.1, ls=(0, (3, 2)), zorder=1)
    ax.annotate("", xy=(s0, -9), xytext=(0.0, -9),
                arrowprops=dict(arrowstyle="-|>", color=RED, lw=1.5, shrinkA=0, shrinkB=0))
    ax.set_xlim(-1.0, 1.1)
    ax.set_xticks([-0.5, 0, 0.5, 1])
    ax.set_xticklabels(["−0.5", "0", "0.5", "1"])
    ax.set_xlabel("sine of angle")

    for a in axes:
        a.set_ylim(-40, TOP)
        a.set_yticks([-40, -20, 0])
        a.grid(True, axis="y", color=RULE, lw=0.7, alpha=0.7)
        clean(a)
    finalize(fig, "L18-sin-space", also_page=True)


# --------------------------------------------------------------------------- 4
def broadening() -> None:
    """Projected aperture: the array looks shorter from off broadside."""
    t0 = np.radians(40.0)
    u = np.array([np.sin(t0), np.cos(t0)])
    v = np.array([np.cos(t0), -np.sin(t0)])
    L = float(N - 1)

    fig, ax = plt.subplots(figsize=(7.6, 4.4))
    ax.set_aspect("equal")
    ax.axis("off")

    xs = np.arange(N) * 1.0
    ax.plot([-0.5, L + 0.5], [0, 0], color=GRAY, lw=1.2)
    for x in xs:
        ax.add_patch(plt.Rectangle((x - 0.16, -0.12), 0.32, 0.24,
                                   facecolor="white", edgecolor=NAVY, lw=1.6, zorder=3))
    ax.annotate("", xy=(L, -0.62), xytext=(0, -0.62),
                arrowprops=dict(arrowstyle="<|-|>", color=NAVY, lw=1.4))
    ax.text(L / 2, -0.95, "array length", color=NAVY, fontsize=14.5, ha="center", va="top")

    # rays toward the source from the two ends
    base = 5.5 * u                                  # foot of the bracket on the left ray
    endp = base + (L * np.cos(t0)) * v              # lands on the right ray
    for p0, tmax in ((np.array([0.0, 0.0]), 6.6), (np.array([L, 0.0]), 3.6)):
        ax.plot([p0[0], p0[0] + tmax * u[0]], [p0[1], p0[1] + tmax * u[1]],
                color=BLUE, lw=1.3, alpha=0.85)
    ax.annotate("", xy=endp, xytext=base,
                arrowprops=dict(arrowstyle="<|-|>", color=RED, lw=2.0))
    mid = (base + endp) / 2
    # Below the bracket, between the two rays, clear of the broadside label.
    # The bracket is diagonal and the label is not, so its distance off the
    # bracket is computed from the label's own measured box: far enough along
    # -u that the box's nearest corner still clears the line.
    ax.set_xlim(-1.0, L + 3.4)
    ax.set_ylim(-1.6, 5.0)
    lab = ax.text(0, 0, "projected length", color=RED, fontsize=14.5, ha="center",
                  va="center")
    bb = lab.get_window_extent(fig.canvas.get_renderer()).transformed(ax.transData.inverted())
    hw, hh = bb.width / 2, bb.height / 2
    D = hw * abs(u[0]) + hh * abs(u[1]) + 0.15
    lab.set_position((mid[0] - D * u[0], mid[1] - D * u[1]))

    ax.plot([L, L], [0, 3.4], color=GRAY, lw=1.1, ls=":")
    ax.text(L, 3.5, "broadside", color=GRAY, fontsize=14.5, ha="center", va="bottom")
    arc = np.linspace(0, t0, 60)
    r = 2.0
    ax.plot(L + r * np.sin(arc), r * np.cos(arc), color=INK, lw=1.1)
    ax.text(L + (r + 0.36) * np.sin(t0 / 2), (r + 0.36) * np.cos(t0 / 2),
            r"$\theta_0$", color=INK, fontsize=21, ha="center", va="center")

    ax.set_xlim(-1.0, L + 3.4)
    ax.set_ylim(-1.6, 5.0)
    finalize(fig, "L18-broadening", also_page=True)


# --------------------------------------------------------------------------- 5
def hpbw_vs_scan() -> None:
    """HPBW against steer angle: the 1/cos(theta0) rule against the -3 dB
    width read off the exact array factor, with the scan loss on a second
    axis. The rule reads narrow past about 50 deg."""
    pts = np.array([0.0, 30.0, 45.0, 60.0])
    rule = hpbw_rule(pts)
    exact = np.array([hpbw_exact(t) for t in pts])
    loss = scan_loss_db(pts)
    assert np.allclose(np.round(rule, 1), [13.2, 15.2, 18.7, 26.4]), rule
    assert np.allclose(np.round(exact, 1), [13.3, 15.4, 19.1, 30.5]), exact
    assert np.allclose(np.round(loss, 1) + 0.0, [0.0, -0.6, -1.5, -3.0]), loss
    assert round(exact[3] / exact[0], 1) == 2.3        # "2.3 times, exactly"

    t = np.linspace(0.0, 65.0, 261)
    r_t = hpbw_rule(t)
    # Past about 62 deg the upper half-power edge would need sin(theta) > 1:
    # the beam runs into endfire and has no -3 dB width in real space, so the
    # exact curve stops where its upper edge reaches 90 deg.
    real = af(90.0, t) ** 2 < 0.5
    te = t[real]
    e_t = np.array([hpbw_exact(x) for x in te])
    assert 61.0 < te[-1] < 64.0, te[-1]
    l_t = scan_loss_db(t)
    # where the two widths part by more than a degree: the page's "about 50"
    gap = te[np.argmax(e_t - r_t[real] > 1.0)]
    assert 45.0 <= gap <= 55.0, gap

    fig, ax = plt.subplots(figsize=(5.9, 2.9))
    ax2 = ax.twinx()
    ax.plot(te, e_t, color=NAVY, lw=2.2, zorder=3)
    ax.plot(t, r_t, color=NAVY, lw=1.6, ls=(0, (5, 3)), zorder=3)
    ax.scatter(pts, exact, s=26, color=NAVY, zorder=4)
    ax.scatter(pts, rule, s=26, facecolor="white", edgecolor=NAVY, lw=1.3, zorder=4)
    ax2.plot(t, l_t, color=AMBER, lw=1.8, zorder=2)
    ax2.scatter(pts, loss, s=22, color=AMBER, zorder=4)

    ax.set_xlim(0, 65)
    ax.set_xticks([0, 15, 30, 45, 60])
    ax.set_ylim(10, 40)
    ax.set_yticks([10, 20, 30, 40])
    ax.set_xlabel("steer angle (deg)")
    ax.set_ylabel("HPBW (deg)", color=NAVY)
    ax2.set_ylim(-6, 0)
    ax2.set_yticks([-6, -4, -2, 0])
    ax2.set_yticklabels(["−6", "−4", "−2", "0"])
    ax2.set_ylabel("scan loss (dB)", color=AMBER)
    ax2.tick_params(axis="y", colors=AMBER)
    ax.grid(True, color=RULE, lw=0.7, alpha=0.7)
    ax.spines["top"].set_visible(False)
    ax2.spines["top"].set_visible(False)
    ax2.spines["left"].set_visible(False)
    ax2.spines["bottom"].set_visible(False)

    # curve labels, placed from the curves themselves at 50 deg, where the
    # two widths have just parted and the scan-loss curve is well above both
    x_lab = 50.0
    ax.text(x_lab - 1.0, float(np.interp(x_lab, te, e_t)) + 1.5, "exact", color=NAVY,
            fontsize=13, ha="right", va="bottom")
    ax.text(x_lab + 1.0, float(np.interp(x_lab, t, r_t)) - 1.5, "1/cos rule", color=NAVY,
            fontsize=13, ha="left", va="top")
    xl = 20.0
    ax2.text(xl, float(np.interp(xl, t, l_t)) - 0.3, "scan loss", color=AMBER, fontsize=13,
             ha="center", va="top")
    finalize(fig, "L18-hpbw-vs-scan", also_page=True)


# --------------------------------------------------------------------------- 6
def inverse_unwrap() -> None:
    """The inverse example: eight wrapped settings, the step between each
    pair, and the one step that needs a whole turn put back. The settings are
    the page's table as printed (0.1 deg rounding included)."""
    phi = np.array([0.0, 59.2, 118.5, 177.7, 237.0, 296.2, 355.4, 54.7])
    steps = np.round(np.diff(phi), 1)
    assert np.allclose(steps, [59.2, 59.3, 59.2, 59.3, 59.2, 59.2, -300.7]), steps
    assert round(steps[6] + 360.0, 1) == 59.3            # a turn restored
    unwrapped7 = phi[7] + 360.0
    assert round(unwrapped7, 1) == 414.7
    dphi = unwrapped7 / 7
    assert round(dphi, 2) == 59.24
    sin0 = dphi / round(KD_DEG, 1)
    assert round(sin0, 3) == 0.342
    theta0 = np.degrees(np.arcsin(sin0))
    assert round(theta0, 1) == 20.0                      # +20.0 deg: a rising ramp
    # the table is the +20 deg ramp, wrapped, to within its 0.1 deg rounding
    true = (np.arange(N) * KD_DEG * np.sin(np.radians(20.0))) % 360.0
    assert np.all(np.abs(true - phi) < 0.06), true - phi

    n = np.arange(N)
    fig, ax = plt.subplots(figsize=(5.6, 3.1))
    fig.subplots_adjust(left=0.01, right=0.99, top=0.99, bottom=0.2)
    W = 0.56
    ax.bar(n, phi, width=W, color=BLUE, edgecolor=NAVY, lw=1.0, zorder=3)

    # each step sits over the pair it joins, just above the taller bar of the
    # two; the rising bars stagger the labels, so neighbors never touch
    pad = 14.0
    for i in range(N - 2):
        ax.text(i + 0.5, phi[i + 1] + pad, f"+{steps[i]:.1f}", color=GREEN, fontsize=13,
                ha="center", va="bottom")
    # the odd step goes a row higher than the others, so it cannot be read as
    # part of the +59.2 beside it
    ax.text(6.5, unwrapped7 + pad * 0.6, f"\u2212{abs(steps[6]):.1f}", color=RED, fontsize=13,
            ha="center", va="bottom")
    # the turn put back: element 7 lifted from 54.7 to 414.7, drawn up the
    # right edge of its bar so it stays clear of the -300.7 label to its left
    xr = 7 + W / 2
    ax.plot([xr, xr], [phi[7], unwrapped7], color=AMBER, lw=1.4, ls=(0, (3, 2)), zorder=4)
    ax.plot([7.1, xr], [unwrapped7, unwrapped7], color=AMBER, lw=1.6, zorder=4)
    ax.text(xr + 0.08, (phi[7] + unwrapped7) / 2, "+360", color=AMBER, fontsize=13,
            ha="left", va="center")
    ax.text(xr + 0.08, unwrapped7, f"{unwrapped7:.1f}", color=AMBER, fontsize=13,
            ha="left", va="center")

    # the eight settings, under their element numbers
    YN, YV = -38.0, -88.0
    for i in range(N):
        ax.text(i, YN, f"{i}", color=GRAY, fontsize=13, ha="center", va="center")
        ax.text(i, YV, f"{phi[i]:.1f}" if i else "0", color=NAVY, fontsize=13,
                ha="center", va="center")
    ax.text(-0.45, YN, "n", color=GRAY, fontsize=13, ha="right", va="center", style="italic")
    ax.text(-0.45, YV, "set", color=NAVY, fontsize=13, ha="right", va="center")

    ax.text(-0.4, 470.0, f"seven steps of {dphi:.2f}\u00b0\nrising: steer angle +{theta0:.1f}\u00b0",
            color=INK, fontsize=13, ha="left", va="top", linespacing=1.35)

    ax.set_xlim(-1.25, 8.2)
    ax.set_ylim(-110, 480)
    ax.set_xticks([])
    ax.set_yticks([])
    for side in ("left", "top", "right"):
        ax.spines[side].set_visible(False)
    ax.spines["bottom"].set_position(("data", 0))
    finalize(fig, "L18-inverse-unwrap", also_page=True)


# --------------------------------------------------------------------------- 7
def steered_patterns() -> None:
    """Static fallback for the widget: four commanded angles on one axis."""
    th = np.linspace(-90, 90, 6001)
    fig, ax = plt.subplots(figsize=(8.6, 4.1))
    for t0, c, lw in ((0, GRAY, 1.6), (30, BLUE, 1.7), (45, NAVY, 1.9), (60, AMBER, 1.9)):
        ax.plot(th, af_db(th, t0), color=c, lw=lw, label=f"{t0}°")
    ax.axhline(-3, color=GREEN, lw=1.0, ls="--")
    ax.text(88, -2.6, "half power", color=GREEN, fontsize=11, ha="right", va="bottom")
    ax.set_xlim(-90, 90)
    ax.set_ylim(-40, 2)
    ax.set_xticks([-90, -60, -30, 0, 30, 60, 90])
    ax.set_xlabel("scan angle (deg)")
    ax.set_ylabel("relative power (dB)")
    ax.grid(True, color=RULE, lw=0.7, alpha=0.7)
    clean(ax)
    ax.legend(loc="upper left", fontsize=11, title="commanded", title_fontsize=11)
    fig.tight_layout()
    finalize(fig, "L18-steered-patterns")


if __name__ == "__main__":
    FIG.mkdir(parents=True, exist_ok=True)
    IMG.mkdir(parents=True, exist_ok=True)
    path_difference()
    phase_ramp()
    sin_space()
    broadening()
    hpbw_vs_scan()
    inverse_unwrap()
    steered_patterns()
