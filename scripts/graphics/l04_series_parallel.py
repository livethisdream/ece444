#!/usr/bin/env python3
"""L04: why a series reactance makes a small resistor look like a big one.

Drive the series branch 20 + j24.5 ohm with 1 A. The resistor dissipates 10 W --
that never changes. But the branch voltage is |Z| = 31.6 V, not 20 V, because the
reactor's voltage adds in quadrature. A source at the terminals sees 31.6 V and
10 W and concludes R = |V|^2 / 2P = 50 ohm.

The reactance is a lever on voltage that costs no power, and the lever ratio is
R_p / R_s = |Z|^2 / R_s^2 = 1 + Q^2.

Left panel: the voltage phasors as a right triangle.
Right panel: the two circuits a source cannot tell apart.

Deck figures carry no equations -- labels are words and plain numbers.

    python3 scripts/graphics/l04_series_parallel.py
    -> book/extras/slides/fig/L04-series-parallel.svg
       book/extras/viz/img/L04-series-parallel.svg
"""

from __future__ import annotations
import io, re
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

NAVY, BLUE, RED, GREEN, ORANGE, GRAY = "#004a85", "#0067b9", "#b01e24", "#1d7a4d", "#e67e22", "#5a5a5a"
INK, RULE = "#1a1a1a", "#c7d2e0"
ROOT = Path(__file__).resolve().parents[2]
OUTS = [ROOT / "book/extras/slides/fig", ROOT / "book/extras/viz/img"]

plt.rcParams.update({"svg.fonttype": "none", "font.size": 13, "text.color": INK})

RS, XS = 20.0, 24.5


def phasors(ax):
    Zm = np.hypot(RS, XS)
    ax.annotate("", xy=(RS, 0), xytext=(0, 0),
                arrowprops=dict(arrowstyle="-|>", color=NAVY, lw=2.6, mutation_scale=18))
    ax.annotate("", xy=(RS, XS), xytext=(RS, 0),
                arrowprops=dict(arrowstyle="-|>", color=ORANGE, lw=2.6, mutation_scale=18))
    ax.annotate("", xy=(RS, XS), xytext=(0, 0),
                arrowprops=dict(arrowstyle="-|>", color=GREEN, lw=3.0, mutation_scale=20))
    ax.plot([RS - 2.2, RS - 2.2, RS], [0, 2.2, 2.2], color=GRAY, lw=1.0)

    ax.text(RS / 2, -2.6, "20 V across the resistor", color=NAVY,
            fontsize=11.5, fontweight="bold", ha="center", va="top")
    ax.text(RS + 1.2, XS / 2, "24.5 V across\nthe reactance\n(no power)", color=ORANGE,
            fontsize=11.5, fontweight="bold", ha="left", va="center")
    ax.text(1.5, XS * 0.88, "31.6 V total", color=GREEN,
            fontsize=12.5, fontweight="bold", ha="left", va="bottom")
    ax.text(0, -6.4, "Drive 1 A through the branch. The resistor still burns 10 W —\n"
                     "but the terminals now show 31.6 V instead of 20 V.",
            fontsize=11, color=INK, ha="left", va="top")

    ax.set_xlim(-2, 40); ax.set_ylim(-12, 30)
    ax.set_aspect("equal"); ax.axis("off")


def circuits(ax):
    ax.axis("off")
    ax.set_xlim(0, 10); ax.set_ylim(0, 10)

    # left: series R + X
    ax.plot([0.6, 1.6], [8.2, 8.2], color=INK, lw=1.6)
    ax.add_patch(plt.Rectangle((1.6, 7.7), 1.5, 1.0, fc="none", ec=NAVY, lw=2.0))
    ax.text(2.35, 8.2, "20 Ω", ha="center", va="center", fontsize=11, color=NAVY, fontweight="bold")
    ax.plot([3.1, 3.9], [8.2, 8.2], color=INK, lw=1.6)
    ax.add_patch(plt.Rectangle((3.9, 7.7), 1.5, 1.0, fc="none", ec=ORANGE, lw=2.0))
    ax.text(4.65, 8.2, "+j24.5", ha="center", va="center", fontsize=11, color=ORANGE, fontweight="bold")
    ax.plot([5.4, 6.2], [8.2, 8.2], color=INK, lw=1.6)
    ax.text(0.6, 9.3, "what is really there", fontsize=11.5, color=GRAY, fontweight="bold")

    # right: parallel R_p + X_p
    ax.plot([0.6, 3.0], [3.6, 3.6], color=INK, lw=1.6)
    ax.plot([3.0, 3.0], [3.6, 2.2], color=INK, lw=1.6)
    ax.add_patch(plt.Rectangle((2.25, 1.2), 1.5, 1.0, fc="none", ec=GREEN, lw=2.0))
    ax.text(3.0, 1.7, "50 Ω", ha="center", va="center", fontsize=11, color=GREEN, fontweight="bold")
    ax.plot([3.0, 3.0], [1.2, 0.4], color=INK, lw=1.6)
    ax.plot([3.0, 5.2], [0.4, 0.4], color=INK, lw=1.6)
    ax.plot([5.2, 5.2], [3.6, 2.2], color=INK, lw=1.6)
    ax.add_patch(plt.Rectangle((4.45, 1.2), 1.5, 1.0, fc="none", ec=ORANGE, lw=2.0))
    ax.text(5.2, 1.7, "−j40.8", ha="center", va="center", fontsize=11, color=ORANGE, fontweight="bold")
    ax.plot([5.2, 5.2], [1.2, 0.4], color=INK, lw=1.6)
    ax.plot([3.0, 6.2], [3.6, 3.6], color=INK, lw=1.6)
    ax.text(0.6, 4.7, "what the source sees", fontsize=11.5, color=GRAY, fontweight="bold")

    ax.annotate("", xy=(3.4, 5.4), xytext=(3.4, 7.2),
                arrowprops=dict(arrowstyle="-|>", color=GRAY, lw=2.0, mutation_scale=20))
    ax.text(3.8, 6.3, "identical at one frequency", fontsize=11.5, color=GRAY,
            fontweight="bold", va="center")
    ax.text(0.2, -0.9, "Cancel the −j40.8 with a shunt element and a clean 50 Ω is left.",
            fontsize=11, color=INK, ha="left", va="top")


def main() -> int:
    fig, axes = plt.subplots(1, 2, figsize=(11.4, 4.3),
                             gridspec_kw={"width_ratios": [1.05, 1.0]})
    phasors(axes[0])
    circuits(axes[1])
    fig.subplots_adjust(wspace=0.05)

    buf = io.StringIO()
    fig.savefig(buf, format="svg", transparent=True, bbox_inches="tight", pad_inches=0.06)
    plt.close(fig)
    s = buf.getvalue()
    s = s[s.index("<svg"):]
    s = re.sub(r"font-family:[^;}]*", "font-family:inherit", s)
    for out in OUTS:
        out.mkdir(parents=True, exist_ok=True)
        (out / "L04-series-parallel.svg").write_text(s, encoding="utf-8")
        print(f"wrote {out / 'L04-series-parallel.svg'}")

    Zm = np.hypot(RS, XS)
    print(f"\ncheck: |Z| = {Zm:.2f} = sqrt(20*50) = {np.sqrt(20*50):.2f}")
    print(f"       R_p = |Z|^2/Rs = {Zm**2/RS:.2f} ohms, X_p = |Z|^2/Xs = {Zm**2/XS:.1f} ohms")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
