#!/usr/bin/env python3
"""Generate the L04 dipole-impedance data plot as inline SVG.

L04:
  - L04-reactance-vs-length : R_in and X_in of a center-fed dipole vs length,
    0.3 to 0.7 wavelengths, with the X = 0 crossing (resonance, just under
    0.5 lambda) and the 73 ohm point at 0.5 lambda marked.

Curves come from the classical induced-EMF (Carter) result for a thin
center-fed dipole with an assumed sinusoidal current, referred to the input
terminals by 1/sin^2(kl/2).  Sine and cosine integrals are evaluated by
quadrature so the script needs nothing beyond numpy/matplotlib (checked
against scipy.special.sici to 7 digits).

The wire radius a = 1e-4 lambda is REPRESENTATIVE, not a measurement: the
induced-EMF reactance depends on how thin the wire is, and this value puts
resonance at ~0.485 lambda with ~67 ohms, matching the textbook "trim to
about 0.48 lambda for roughly 70 ohms real" that the deck and lesson page
quote.  A fatter wire resonates shorter; a thinner one longer.

Exported as SVG with live <text> (svg.fonttype='none'), then font-family is
rewritten to 'inherit' so the injected figure picks up the deck's Source Sans
Pro.  Transparent background, USAFA palette, no baked formulas (axis labels,
legend and annotations only).

    python scripts/graphics/l04_reactance.py
    -> writes book/extras/slides/fig/L04-reactance-vs-length.svg
"""

from __future__ import annotations
import io, re
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

NAVY, BLUE, RED, GREEN, ORANGE, GREY = "#004a85", "#0067b9", "#b01e24", "#1d7a4d", "#e67e22", "#5a5a5a"
INK, RULE = "#1a1a1a", "#c7d2e0"
OUT = Path(__file__).resolve().parents[2] / "book/extras/slides/fig"

GAMMA = 0.5772156649015329          # Euler-Mascheroni
ETA0 = 376.73                       # free-space impedance, ohms

plt.rcParams.update({
    "svg.fonttype": "none",
    "font.size": 13,
    "axes.edgecolor": "#8a929c",
    "axes.labelcolor": INK,
    "xtick.color": GREY, "ytick.color": GREY,
    "text.color": INK,
    "axes.linewidth": 1.0,
    "legend.frameon": False,
})


def finalize(fig, name: str) -> None:
    buf = io.StringIO()
    fig.savefig(buf, format="svg", transparent=True, bbox_inches="tight", pad_inches=0.06)
    plt.close(fig)
    s = buf.getvalue()
    s = s[s.index("<svg"):]                                      # drop xml decl/doctype
    s = re.sub(r"font-family:[^;}]*", "font-family:inherit", s)  # inherit deck font
    (OUT / f"{name}.svg").write_text(s, encoding="utf-8")
    print(f"wrote {OUT / (name + '.svg')}")


def _si(x: np.ndarray, n: int = 4001) -> np.ndarray:
    """Sine integral Si(x) = int_0^x sin(t)/t dt, by quadrature."""
    x = np.atleast_1d(np.asarray(x, float))
    u = np.linspace(0.0, 1.0, n)
    out = np.empty_like(x)
    for i, xi in enumerate(x):
        t = u * xi
        safe = np.where(t == 0.0, 1.0, t)
        f = np.where(t == 0.0, 1.0, np.sin(safe) / safe)
        out[i] = np.trapezoid(f, t)
    return out


def _ci(x: np.ndarray, n: int = 4001) -> np.ndarray:
    """Cosine integral Ci(x) = gamma + ln(x) + int_0^x (cos t - 1)/t dt."""
    x = np.atleast_1d(np.asarray(x, float))
    u = np.linspace(0.0, 1.0, n)
    out = np.empty_like(x)
    for i, xi in enumerate(x):
        t = u * xi
        safe = np.where(t == 0.0, 1.0, t)
        f = np.where(t == 0.0, 0.0, (np.cos(safe) - 1.0) / safe)
        out[i] = GAMMA + np.log(xi) + np.trapezoid(f, t)
    return out


def dipole_zin(L: np.ndarray, a: float = 1e-4) -> tuple[np.ndarray, np.ndarray]:
    """Input R and X of a center-fed dipole of length L (wavelengths), wire
    radius a (wavelengths), induced-EMF method, sinusoidal current."""
    k = 2.0 * np.pi
    kl = k * L
    Rm = (ETA0 / (2 * np.pi)) * (
        GAMMA + np.log(kl) - _ci(kl)
        + 0.5 * np.sin(kl) * (_si(2 * kl) - 2 * _si(kl))
        + 0.5 * np.cos(kl) * (GAMMA + np.log(kl / 2) + _ci(2 * kl) - 2 * _ci(kl))
    )
    Xm = (ETA0 / (4 * np.pi)) * (
        2 * _si(kl)
        + np.cos(kl) * (2 * _si(kl) - _si(2 * kl))
        - np.sin(kl) * (2 * _ci(kl) - _ci(2 * kl) - _ci(2 * k * a ** 2 / L))
    )
    s = np.sin(kl / 2.0) ** 2          # refer current-maximum values to the terminals
    return Rm / s, Xm / s


def reactance_vs_length() -> None:
    L = np.linspace(0.30, 0.70, 601)
    R, X = dipole_zin(L)

    # resonance: first X = 0 crossing (interpolated)
    i = int(np.where(np.diff(np.sign(X)))[0][0])
    Lres = float(np.interp(0.0, [X[i], X[i + 1]], [L[i], L[i + 1]]))

    fig, ax = plt.subplots(figsize=(6.7, 3.9))
    ax.axhline(0.0, color=GREY, lw=1.1, ls=(0, (4, 3)), zorder=1)
    ax.plot(L, R, color=NAVY, lw=2.6, label="Resistance  R", zorder=3)
    ax.plot(L, X, color=ORANGE, lw=2.6, label="Reactance  X", zorder=3)

    ax.set_xlim(0.30, 0.70)
    ax.set_ylim(-400, 620)
    ax.set_xlabel("Dipole length  (wavelengths)")
    ax.set_ylabel("Terminal impedance  (ohms)")
    ax.set_xticks(np.arange(0.30, 0.71, 0.05))
    ax.set_xticklabels(["0.30", "", "0.40", "", "0.50", "", "0.60", "", "0.70"])
    ax.set_yticks(range(-400, 601, 200))
    ax.grid(color=RULE, linewidth=0.8)
    for sp in ("top", "right"):
        ax.spines[sp].set_visible(False)

    # resonance: X crosses zero just short of half a wavelength
    ax.plot(Lres, 0.0, "o", color=RED, ms=7.5, zorder=5)
    ax.annotate("X = 0 just under 0.5 λ\n— resonance",
                xy=(Lres, 0.0), xytext=(0.335, 170), color=RED,
                fontsize=12, fontweight="bold", ha="left", va="center",
                arrowprops=dict(arrowstyle="->", color=RED, lw=1.3))

    # the canonical half-wave point
    ax.plot(0.5, 73.1, "o", color=NAVY, ms=7.5, zorder=5)
    ax.annotate("73 Ω at 0.5 λ", xy=(0.5, 73.1), xytext=(0.523, -175),
                color=NAVY, fontsize=12, fontweight="bold", ha="left", va="center",
                arrowprops=dict(arrowstyle="->", color=NAVY, lw=1.3))

    ax.text(0.365, -330, "too short → capacitive", color=GREY, fontsize=12,
            fontweight="bold", ha="left", va="center")
    ax.text(0.625, 530, "too long → inductive", color=GREY, fontsize=12,
            fontweight="bold", ha="right", va="center")

    ax.legend(loc="upper left", fontsize=12.5, handlelength=1.7)
    finalize(fig, "L04-reactance-vs-length")


def main() -> int:
    OUT.mkdir(parents=True, exist_ok=True)
    reactance_vs_length()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
