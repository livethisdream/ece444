#!/usr/bin/env python3
"""L16 illustration-sweep figures (the array factor and pattern multiplication).

  L16-scan-angle        : the scan angle and the Module 1 polar angle on one ray
  L16-sidelobe-vs-n     : first sidelobe level against N -- exact, the 3pi/2
                          estimate, and the line-source limit
  L16-four-dipole-zoom  : the four-dipole sidelobe -- the dB-add estimate at the
                          array-factor peak against the product's own peak
  L16-grating-limit     : largest grating-free spacing against scan limit, with
                          the PHASER's 0.481 wavelength
  L16-sinc-limit        : |AF_N| for N = 4, 8, 32 against the line-source sinc,
                          in the common variable u = N psi / 2

Every plotted number is computed here and printed for checking against the
lesson text. Words and numbers only, no equations, so one SVG serves both the
deck and the page.

    python3 scripts/graphics/l16_figures.py
    -> book/extras/slides/fig/L16-*.svg  and  book/extras/viz/img/L16-*.svg
"""

from __future__ import annotations

import numpy as np

from m3_l16_patterns import (  # noqa: F401  (shared palette and helpers)
    AMBER, BLUE, DB_FLOOR, GRAY, GREEN, INK, NAVY, RED, RULE,
    af_psi, af_uniform, db, finalize, plt, write,
)


def M(v: float) -> str:
    """A level in dB with a typographic minus, as the lesson prints it."""
    return f"{v:.1f}".replace("-", "\u2212")


def first_sidelobe(N: int) -> tuple[float, float]:
    """Exact first sidelobe of AF_N: (psi in rad, level in dB)."""
    psi = np.linspace(2 * np.pi / N, 4 * np.pi / N, 20001)
    a = np.abs(np.sin(N * psi / 2) / (N * np.sin(psi / 2)))
    i = int(np.argmax(a))
    return psi[i], float(db(a[i]))


# ------------------------------------------------------------ scan angle ---
def scan_angle() -> None:
    """One ray, two angles: theta from broadside, theta_polar from the axis."""
    cx, cy, R = 330, 300, 210
    th = np.radians(35.0)                       # scan angle from broadside
    ex, ey = cx + R * np.sin(th), cy - R * np.cos(th)
    r1, r2 = 92, 140                            # arc radii
    a1x, a1y = cx + r1 * np.sin(th), cy - r1 * np.cos(th)
    a2x, a2y = cx + r2 * np.sin(th), cy - r2 * np.cos(th)
    mid1 = th / 2                               # label positions on the arcs
    mid2 = (th + np.pi / 2) / 2
    l1x, l1y = cx + (r1 + 22) * np.sin(mid1), cy - (r1 + 22) * np.cos(mid1)
    l2x, l2y = cx + (r2 + 24) * np.sin(mid2), cy - (r2 + 24) * np.cos(mid2)
    elems = "".join(
        f'<circle cx="{cx + k * 46}" cy="{cy}" r="8" fill="{NAVY}"/>' for k in range(-3, 4)
    )
    svg = f"""<svg viewBox="0 0 700 380" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="An array on a horizontal axis with broadside straight up. One ray leaves at 35 degrees from broadside. The scan angle is measured from broadside to the ray; the Module 1 polar angle is measured from the array axis to the same ray, 55 degrees">
<defs>
<marker id="l16sa" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse"><path d="M0 0 L10 5 L0 10 z" fill="{BLUE}"/></marker>
<marker id="l16sg" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse"><path d="M0 0 L10 5 L0 10 z" fill="{GRAY}"/></marker>
</defs>
<line x1="70" y1="{cy}" x2="{cx + R + 50}" y2="{cy}" stroke="{GRAY}" stroke-width="1.4" marker-end="url(#l16sg)"/>
<text x="{cx + R + 40}" y="{cy + 26}" font-size="13" fill="{GRAY}" text-anchor="end">array axis (+z in Module 1)</text>
{elems}
<line x1="{cx}" y1="{cy}" x2="{cx}" y2="{cy - R - 20}" stroke="{GRAY}" stroke-width="1.3" stroke-dasharray="6 5" marker-end="url(#l16sg)"/>
<text x="{cx - 10}" y="{cy - R + 40}" font-size="13" fill="{GRAY}" text-anchor="end">broadside</text>
<line x1="{cx}" y1="{cy}" x2="{ex:.1f}" y2="{ey:.1f}" stroke="{BLUE}" stroke-width="2.4" marker-end="url(#l16sa)"/>
<text x="{ex + 10:.1f}" y="{ey + 4:.1f}" font-size="13" fill="{BLUE}">toward the observer</text>
<path d="M {cx} {cy - r1} A {r1} {r1} 0 0 1 {a1x:.1f} {a1y:.1f}" fill="none" stroke="{NAVY}" stroke-width="2"/>
<text x="{l1x:.1f}" y="{l1y:.1f}" font-size="15" font-weight="700" fill="{NAVY}" text-anchor="middle">&#952;</text>
<path d="M {cx + r2} {cy} A {r2} {r2} 0 0 0 {a2x:.1f} {a2y:.1f}" fill="none" stroke="{AMBER}" stroke-width="2"/>
<text x="{l2x:.1f}" y="{l2y:.1f}" font-size="15" font-weight="700" fill="{AMBER}">&#952;<tspan font-size="11" dy="4">polar</tspan></text>
<text x="40" y="44" font-size="13.5" font-weight="700" fill="{NAVY}">&#952;: scan angle, from broadside (Module 3)</text>
<text x="40" y="66" font-size="13.5" font-weight="700" fill="{AMBER}">&#952;<tspan font-size="10.5" dy="3">polar</tspan><tspan dy="-3">: from the array axis (Module 1)</tspan></text>
<text x="40" y="88" font-size="12.5" fill="{GRAY}">The two angles add to 90&#176;. Here 35&#176; and 55&#176;.</text>
</svg>
"""
    write("L16-scan-angle", svg)


# ---------------------------------------------------------- sidelobe vs N ---
def sidelobe_vs_n() -> None:
    Ns = np.arange(3, 33)
    exact = np.array([first_sidelobe(int(n))[1] for n in Ns])
    est = db(1 / (Ns * np.sin(3 * np.pi / (2 * Ns))))
    limit = first_sidelobe(4000)[1]
    for n in (4, 8, 16, 32):
        print(f"  sidelobe N={n}: exact {exact[n - 3]:.2f} dB, estimate {est[n - 3]:.2f} dB")
    print(f"  sidelobe limit {limit:.2f} dB, 2/(3pi) {db(2 / (3 * np.pi)):.2f} dB")

    fig, ax = plt.subplots(figsize=(7.4, 3.4))
    ax.axhline(limit, color=GRAY, lw=1.1, ls=(0, (5, 4)))
    ax.plot(Ns, est, color=AMBER, lw=1.6, ls=(0, (4, 3)))
    ax.plot(Ns, exact, color=NAVY, lw=2.0, marker="o", ms=3.4)
    ax.set_xlim(2, 33)
    ax.set_ylim(-14.2, -8.6)
    ax.set_xticks([4, 8, 12, 16, 20, 24, 28, 32])
    ax.set_xlabel("Number of elements N")
    ax.set_ylabel("First sidelobe (dB)")
    ax.grid(True, color=RULE, lw=0.7)
    for side in ("top", "right"):
        ax.spines[side].set_visible(False)
    for n, dx, dy in ((4, 1.0, 0.55), (8, 1.0, 0.55)):
        v = exact[n - 3]
        ax.annotate(f"N = {n}:  {M(v)} dB", xy=(n, v), xytext=(n + dx, v + dy),
                    color=NAVY, fontsize=11,
                    arrowprops=dict(arrowstyle="-", color=NAVY, lw=0.8))
    ax.text(32.5, est[-1] - 0.1, "dashed: halfway-between-nulls estimate",
            color=AMBER, fontsize=10.5, ha="right", va="top")
    ax.text(32.5, est[-1] - 0.45, f"gray: continuous line source, {M(limit)} dB",
            color=GRAY, fontsize=10.5, ha="right", va="top")
    ax.text(32.5, exact[-1] + 0.62, "solid: exact peak", color=NAVY, fontsize=10.5,
            ha="right", va="bottom")
    finalize(fig, "L16-sidelobe-vs-n")


# ------------------------------------------------------- four-dipole zoom ---
def four_dipole_zoom() -> None:
    N, d_lam = 4, 0.5
    th = np.linspace(25, 80, 11001)
    ef = np.cos(np.radians(th))
    af = af_uniform(th, N, d_lam)
    prod = ef * af
    i_af, i_pr = int(np.argmax(af)), int(np.argmax(prod))
    th_af, th_pr = th[i_af], th[i_pr]
    est = db(af[i_af]) + db(ef[i_af])
    print(f"  four dipoles: AF peak {db(af[i_af]):.2f} dB at {th_af:.1f}, "
          f"EF there {db(ef[i_af]):.2f} dB, estimate {est:.2f} dB; "
          f"product peak {db(prod[i_pr]):.2f} dB at {th_pr:.1f}")

    fig, ax = plt.subplots(figsize=(7.4, 3.4))
    ax.plot(th, db(af), color=BLUE, lw=1.6, ls=(0, (5, 3)))
    ax.plot(th, db(ef), color=GRAY, lw=1.5)
    ax.plot(th, db(prod), color=NAVY, lw=2.2)
    ax.set_xlim(25, 80)
    ax.set_ylim(-26, 1)
    ax.set_xlabel("Scan angle from broadside (degrees)")
    ax.set_ylabel("Relative power (dB)")
    ax.grid(True, color=RULE, lw=0.7)
    for side in ("top", "right"):
        ax.spines[side].set_visible(False)
    ax.plot([th_af], [db(af[i_af])], "o", color=BLUE, ms=5)
    ax.plot([th_af], [est], "o", color=AMBER, ms=5)
    ax.plot([th_pr], [db(prod[i_pr])], "o", color=RED, ms=5)
    ax.plot([th_af, th_af], [est, db(af[i_af])], color=AMBER, lw=1.0, ls=(0, (2, 2)))
    ax.annotate(f"array factor peak  {M(db(af[i_af]))} dB at {th_af:.1f}°",
                xy=(th_af, db(af[i_af])), xytext=(28.5, -8.0), color=BLUE, fontsize=11,
                arrowprops=dict(arrowstyle="-", color=BLUE, lw=0.8))
    ax.annotate(f"estimate at {th_af:.1f}°:  {M(est)} dB",
                xy=(th_af, est), xytext=(55, -17.0), color=AMBER, fontsize=11,
                arrowprops=dict(arrowstyle="-", color=AMBER, lw=0.8))
    ax.annotate(f"product peak  {M(db(prod[i_pr]))} dB at {th_pr:.1f}°",
                xy=(th_pr, db(prod[i_pr])), xytext=(36, -23.8), color=RED, fontsize=11,
                arrowprops=dict(arrowstyle="-", color=RED, lw=0.8))
    ax.text(26, -1.6, "element factor", color=GRAY, fontsize=11, va="top")
    ax.text(79, -1.6, "dashed: array factor  ·  solid: product", color=INK,
            fontsize=10.5, ha="right", va="top")
    finalize(fig, "L16-four-dipole-zoom")


# ---------------------------------------------------------- grating limit ---
def grating_limit() -> None:
    t0 = np.linspace(0, 90, 901)
    dmax = 1 / (1 + np.sin(np.radians(t0)))
    phaser = 14 / 29.126
    d45 = 1 / (1 + np.sin(np.radians(45)))
    print(f"  grating limit: 45 deg -> {d45:.3f} lambda = {d45 * 29.126:.1f} mm; "
          f"PHASER {phaser:.3f}; 90 deg -> {dmax[-1]:.3f}")

    fig, ax = plt.subplots(figsize=(7.4, 3.4))
    ax.fill_between(t0, dmax, 1.15, color=RED, alpha=0.10, lw=0)
    ax.plot(t0, dmax, color=RED, lw=2.0)
    ax.axhline(phaser, color=GREEN, lw=1.8)
    ax.plot([45], [d45], "o", color=NAVY, ms=5)
    ax.set_xlim(0, 90)
    ax.set_ylim(0.3, 1.15)
    ax.set_xticks(np.arange(0, 91, 15))
    ax.set_xlabel("Largest scan angle (degrees)")
    ax.set_ylabel("Spacing (wavelengths)")
    ax.grid(True, color=RULE, lw=0.7)
    for side in ("top", "right"):
        ax.spines[side].set_visible(False)
    ax.text(58, 0.98, "grating lobe in view", color=RED, fontsize=12, fontweight="bold")
    ax.text(3, 0.36, "no grating lobe", color=INK, fontsize=12, fontweight="bold")
    ax.text(88, phaser - 0.025, f"PHASER, {phaser:.3f}", color=GREEN, fontsize=11,
            ha="right", va="top")
    ax.annotate(f"scan to 45°:  {d45:.3f}", xy=(45, d45), xytext=(50, 0.70),
                color=NAVY, fontsize=11,
                arrowprops=dict(arrowstyle="-", color=NAVY, lw=0.8))
    ax.text(1.5, 1.015, "1.0 at broadside", color=RED, fontsize=10.5, va="bottom")
    ax.text(88.5, 0.515, "0.5 at 90°", color=RED, fontsize=10.5, ha="right", va="bottom")
    finalize(fig, "L16-grating-limit")


# ------------------------------------------------------------- sinc limit ---
def sinc_limit() -> None:
    x = np.linspace(0, 9, 9001)                 # u / pi, with u = N psi / 2
    u = np.pi * x
    sinc = np.where(u == 0, 1.0, np.abs(np.sin(u) / np.where(u == 0, 1, u)))
    curves = ((4, AMBER), (8, BLUE), (32, NAVY))
    fig, ax = plt.subplots(figsize=(7.4, 3.5))
    ax.plot(x, db(sinc), color=GRAY, lw=2.6, alpha=0.55)
    for N, c in curves:
        psi_deg = np.degrees(2 * u / N)
        ax.plot(x, db(af_psi(psi_deg, N)), color=c, lw=1.5)
    for N in (4, 8, 32):
        print(f"  sinc limit: N={N} first sidelobe {first_sidelobe(N)[1]:.2f} dB, "
              f"repeat at u/pi = {N}")
    ax.set_xlim(0, 9)
    ax.set_ylim(DB_FLOOR, 4)
    ax.set_xticks(range(0, 10))
    ax.set_xlabel("Distance from the main lobe, in nulls of the line source")
    ax.set_ylabel("Relative power (dB)")
    ax.grid(True, color=RULE, lw=0.7)
    for side in ("top", "right"):
        ax.spines[side].set_visible(False)
    ax.annotate("N = 4 repeats", xy=(4, 0), xytext=(2.35, 1.6), color=AMBER, fontsize=11,
                arrowprops=dict(arrowstyle="-", color=AMBER, lw=0.8))
    ax.annotate("N = 8 repeats", xy=(8, 0), xytext=(5.8, 1.6), color=BLUE, fontsize=11,
                arrowprops=dict(arrowstyle="-", color=BLUE, lw=0.8))
    ax.text(1.15, -4.0, "N = 32 tracks", color=NAVY, fontsize=10.5, ha="left")
    ax.text(1.15, -6.8, "the line source", color=NAVY, fontsize=10.5, ha="left")
    ax.text(1.15, -9.6, "gray: line source", color=GRAY, fontsize=10.5, ha="left")
    finalize(fig, "L16-sinc-limit")


def main() -> None:
    scan_angle()
    sidelobe_vs_n()
    four_dipole_zoom()
    grating_limit()
    sinc_limit()


if __name__ == "__main__":
    main()
