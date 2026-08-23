#!/usr/bin/env python3
"""L17 figures: the ADALM-PHASER receive chain and its frequency plan.

Emits two copies of each figure - a deck copy (no equations, block names and
frequencies only) and a lesson-page copy (same geometry, plus the one line of
mixing arithmetic).

    python3 scripts/graphics/m3_l17_chain.py

Writes:
    book/extras/slides/fig/L17-signal-chain.svg
    book/extras/slides/fig/L17-frequency-plan.svg
    book/extras/viz/img/L17-signal-chain.svg
    book/extras/viz/img/L17-frequency-plan.svg
"""

from __future__ import annotations

from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
DECK = REPO / "book/extras/slides/fig"
PAGE = REPO / "book/extras/viz/img"

NAVY = "#004a85"
MID = "#0067b9"
EDGE2 = "#b9d2e5"
BG = "#f5f9fc"
INK = "#15202b"
INK3 = "#5b6573"
AMBER = "#8a5a00"
GRN = "#3f7d34"
FONT = "Inter, 'Source Sans Pro', system-ui, -apple-system, sans-serif"

# Canonical numbers (COURSE_SPEC section M3).
F_RF = 10.525       # GHz, HB100 nominal
F_IF = 2.2          # GHz, fixed IF the Pluto tunes
F_LO = F_RF + F_IF  # GHz, high-side injection


def txt(x, y, s, size=12, fill=INK, anchor="middle", weight="400"):
    return (
        f'<text x="{x}" y="{y}" font-family="{FONT}" font-size="{size}" '
        f'fill="{fill}" text-anchor="{anchor}" font-weight="{weight}">{s}</text>'
    )


def box(x, y, w, h, fill=BG, stroke=NAVY, sw=1.6, rx=5):
    return (
        f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" '
        f'fill="{fill}" stroke="{stroke}" stroke-width="{sw}"/>'
    )


def line(x1, y1, x2, y2, stroke=NAVY, sw=1.6, extra=""):
    return (
        f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{stroke}" '
        f'stroke-width="{sw}" stroke-linecap="round"{extra}/>'
    )


def arrow_defs():
    out = ["<defs>"]
    for name, color in (("aN", NAVY), ("aA", AMBER), ("aG", GRN), ("aI", INK3)):
        out.append(
            f'<marker id="{name}" viewBox="0 0 10 10" refX="9" refY="5" '
            f'markerWidth="7" markerHeight="7" orient="auto-start-reverse">'
            f'<path d="M 0 0 L 10 5 L 0 10 z" fill="{color}"/></marker>'
        )
    out.append("</defs>")
    return "".join(out)


# --------------------------------------------------------------------------
# Figure 1 - the receive chain
# --------------------------------------------------------------------------

def signal_chain(page_copy: bool) -> str:
    W, H = 800, 400
    ys = [72 + 34 * i for i in range(8)]           # element centres
    px, pw, ph = 26, 32, 22                        # patch rects
    lx, lw, lh = 84, 26, 20                        # LNA triangles
    ax, aw = 132, 86                               # ADAR boxes
    mxc, mr = 300, 16                              # mixer circles
    lo_x, lo_w, lo_y, lo_h = 246, 108, 170, 42     # LO block
    pl_x, pl_w = 388, 132                          # Pluto
    pi_x, pi_w, pi_y, pi_h = 566, 196, 160, 62     # Pi
    top_a, bot_a = ys[0] - 20, ys[3] + 16
    top_b, bot_b = ys[4] - 16, ys[7] + 20
    ya, yb = (top_a + bot_a) / 2, (top_b + bot_b) / 2
    bus_y = 356

    s = [
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" '
        f'width="{W}" height="{H}" role="img" '
        f'aria-label="ADALM-PHASER receive signal chain from patches to Raspberry Pi">',
        arrow_defs(),
    ]

    # ADAR1000 blocks
    for top, bot, tag in ((top_a, bot_a, "A"), (top_b, bot_b, "B")):
        s.append(box(ax, top, aw, bot - top, fill="#eef5fb", stroke=NAVY))
        cx, cy = ax + aw / 2, (top + bot) / 2
        # rotate(-90) maps a local +y offset to a screen +x offset, so the two
        # vertical lines are separated by shifting y, not x.
        s.append(
            f'<text x="{cx}" y="{cy - 5}" font-family="{FONT}" font-size="14" '
            f'fill="{NAVY}" text-anchor="middle" font-weight="600" '
            f'transform="rotate(-90 {cx} {cy})">ADAR1000 {tag}</text>'
        )
        s.append(
            f'<text x="{cx}" y="{cy + 13}" font-family="{FONT}" font-size="10.5" '
            f'fill="{INK3}" text-anchor="middle" '
            f'transform="rotate(-90 {cx} {cy})">phase + gain, 4:1 sum</text>'
        )

    # elements: patch -> LNA -> ADAR
    for y in ys:
        s.append(box(px, y - ph / 2, pw, ph, fill="#ffffff", stroke=MID, sw=1.4, rx=3))
        s.append(f'<rect x="{px + 6}" y="{y - ph / 2 + 5}" width="{pw - 12}" '
                 f'height="{ph - 10}" fill="{EDGE2}" stroke="none"/>')
        s.append(line(px + pw, y, lx, y, MID, 1.4))
        s.append(f'<path d="M {lx} {y - lh / 2} L {lx + lw} {y} L {lx} {y + lh / 2} z" '
                 f'fill="#ffffff" stroke="{MID}" stroke-width="1.4"/>')
        s.append(line(lx + lw, y, ax, y, MID, 1.4))

    # column headers
    s.append(txt(120, 26, f"RF {F_RF} GHz", 12, NAVY, weight="600"))
    s.append(txt(px + pw / 2, 48, "patch ×8", 11.5, INK3))
    s.append(txt(lx + lw / 2 + 2, 48, "LNA", 11.5, INK3))
    s.append(txt(mxc, 48, "mixer", 11.5, INK3))
    tail = ("LO = RF + IF = 10.525 + 2.2 = 12.725 GHz" if page_copy
            else "8 elements in, 2 digital channels out")
    s.append(txt(W - 26, 26, tail, 12, INK3, anchor="end"))

    # subarray rails into the mixers
    for top, bot, yr in ((top_a, bot_a, ya), (top_b, bot_b, yb)):
        s.append(line(ax + aw, (top + bot) / 2, ax + aw + 20, (top + bot) / 2, NAVY, 2.2))
        s.append(line(ax + aw + 20, (top + bot) / 2, ax + aw + 20, yr, NAVY, 2.2))
        s.append(line(ax + aw + 20, yr, mxc - mr, yr, NAVY, 2.2,
                      ' marker-end="url(#aN)"'))

    # mixers
    for yr in (ya, yb):
        s.append(f'<circle cx="{mxc}" cy="{yr}" r="{mr}" fill="#ffffff" '
                 f'stroke="{INK}" stroke-width="1.6"/>')
        k = mr * 0.55
        s.append(line(mxc - k, yr - k, mxc + k, yr + k, INK, 1.5))
        s.append(line(mxc - k, yr + k, mxc + k, yr - k, INK, 1.5))

    # LO block feeding both mixers
    s.append(box(lo_x, lo_y, lo_w, lo_h, fill="#fdf6e8", stroke=AMBER))
    s.append(txt(lo_x + lo_w / 2, lo_y + 17, "ADF4159 + VCO", 12, AMBER, weight="600"))
    s.append(txt(lo_x + lo_w / 2, lo_y + 32, f"LO {F_LO:.3f} GHz", 11, AMBER))
    s.append(line(mxc, lo_y, mxc, ya + mr, AMBER, 1.8, ' marker-end="url(#aA)"'))
    s.append(line(mxc, lo_y + lo_h, mxc, yb - mr, AMBER, 1.8, ' marker-end="url(#aA)"'))

    # IF rails into the Pluto
    rx_h, rx_w = 26, 62
    s.append(box(pl_x, top_a - 4, pl_w, bot_b - top_a + 8, fill=BG, stroke=NAVY))
    s.append(txt(pl_x + pl_w / 2, top_a + 20, "ADALM-Pluto", 13.5, NAVY, weight="600"))
    s.append(txt(pl_x + pl_w / 2, top_a + 36, "AD9361 SDR", 11, INK3))
    for yr, name in ((ya, "Rx1"), (yb, "Rx2")):
        s.append(line(mxc + mr, yr, pl_x, yr, GRN, 2.2, ' marker-end="url(#aG)"'))
        s.append(box(pl_x + (pl_w - rx_w) / 2, yr - rx_h / 2, rx_w, rx_h,
                     fill="#ffffff", stroke=MID, sw=1.4, rx=4))
        s.append(txt(pl_x + pl_w / 2, yr + 4.5, name, 12, NAVY, weight="600"))
        s.append(txt((mxc + mr + pl_x) / 2, yr - 12, f"IF {F_IF} GHz", 11, GRN,
                     weight="600"))

    # Pi and the control bus back to the beamformers
    s.append(box(pi_x, pi_y, pi_w, pi_h, fill=BG, stroke=NAVY))
    s.append(txt(pi_x + pi_w / 2, pi_y + 26, "Raspberry Pi", 13.5, NAVY, weight="600"))
    s.append(txt(pi_x + pi_w / 2, pi_y + 44, "control + browser UI", 11, INK3))
    s.append(line(pl_x + pl_w, pi_y + pi_h / 2, pi_x, pi_y + pi_h / 2, INK3, 2.0,
                  ' marker-end="url(#aI)"'))
    s.append(f'<path d="M {pi_x + 40} {pi_y + pi_h} L {pi_x + 40} {bus_y} '
             f'L {ax + aw / 2} {bus_y} L {ax + aw / 2} {bot_b}" fill="none" '
             f'stroke="{INK3}" stroke-width="1.3" stroke-dasharray="5 4" '
             f'marker-end="url(#aI)"/>')
    s.append(txt(ax + aw / 2 + 100, bus_y - 9, "SPI: phase and gain commands", 11,
                 INK3, anchor="start"))

    # key
    ky = H - 16
    for i, (color, label) in enumerate(((NAVY, "RF"), (AMBER, "LO"), (GRN, "IF"),
                                        (INK3, "control"))):
        kx = 30 + i * 108
        s.append(line(kx, ky - 4, kx + 24, ky - 4, color, 2.6))
        s.append(txt(kx + 30, ky, label, 11.5, color, anchor="start"))

    s.append("</svg>")
    return "\n".join(s)


# --------------------------------------------------------------------------
# Figure 2 - the frequency plan on one axis
# --------------------------------------------------------------------------

def frequency_plan(page_copy: bool) -> str:
    W, H = 800, 300
    axy = 210
    # Piecewise axis: an IF window, a break, then the X-band window.
    seg1 = (1.8, 2.6, 60.0, 190.0)
    seg2 = (9.9, 13.2, 225.0, 750.0)

    def fx(f):
        lo, hi, a, b = seg1 if f < 6 else seg2
        return a + (f - lo) / (hi - lo) * (b - a)

    s = [
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" '
        f'width="{W}" height="{H}" role="img" '
        f'aria-label="PHASER frequency plan: X-band RF, LO band, and the 2.2 GHz IF">',
        arrow_defs(),
    ]

    bars = (
        (fx(10.1), fx(10.7), NAVY, "#eaf2f9", "RF", "10.1 - 10.7"),
        (fx(12.2), fx(13.0), AMBER, "#fdf6e8", "LO", "12.2 - 13.0"),
        (fx(2.2) - 27, fx(2.2) + 27, GRN, "#eef6ec", "IF", "2.2 fixed"),
    )
    for a, b, color, fill, name, rng in bars:
        s.append(f'<rect x="{a:.1f}" y="{axy - 46}" width="{b - a:.1f}" height="46" '
                 f'rx="3" fill="{fill}" stroke="{color}" stroke-width="1.5"/>')
        s.append(txt((a + b) / 2, axy - 27, name, 13, color, weight="700"))
        s.append(txt((a + b) / 2, axy - 11, rng, 10.5, color))

    # axis with a break between the two windows
    s.append(line(46, axy, seg1[3] + 6, axy, INK, 1.6))
    s.append(line(seg2[2] - 6, axy, 766, axy, INK, 1.6, ' marker-end="url(#aI)"'))
    for bx in (200, 212):
        s.append(f'<path d="M {bx - 5} {axy + 7} L {bx + 5} {axy - 7}" stroke="{INK}" '
                 f'stroke-width="1.4" fill="none"/>')
    for f in (2.0, 2.5, 10.0, 11.0, 12.0, 13.0):
        s.append(line(fx(f), axy, fx(f), axy + 6, INK3, 1.2))
        s.append(txt(fx(f), axy + 21, f"{f:g}", 11, INK3))
    s.append(txt(766, axy + 21, "GHz", 11, INK3, anchor="end"))

    # the worked point on each bar
    for f, color, lab in ((2.2, GRN, "2.200 GHz"), (F_RF, NAVY, "10.525 GHz"),
                          (F_LO, AMBER, "12.725 GHz")):
        s.append(f'<circle cx="{fx(f):.1f}" cy="{axy - 46}" r="4" fill="{color}"/>')
        s.append(txt(fx(f), axy + 44, lab, 11.5, color, weight="600"))

    # arcs: RF up to LO, RF down to IF
    s.append(f'<path d="M {fx(F_RF):.1f} {axy - 50} C {fx(F_RF):.1f} 74, '
             f'{fx(F_LO):.1f} 74, {fx(F_LO):.1f} {axy - 50}" fill="none" '
             f'stroke="{AMBER}" stroke-width="1.8" marker-end="url(#aA)"/>')
    s.append(txt((fx(F_RF) + fx(F_LO)) / 2, 66, "LO set 2.2 GHz above the RF", 12,
                 AMBER, weight="600"))
    s.append(f'<path d="M {fx(F_RF):.1f} {axy - 50} C {fx(F_RF):.1f} 120, '
             f'{fx(2.2):.1f} 120, {fx(2.2):.1f} {axy - 50}" fill="none" '
             f'stroke="{GRN}" stroke-width="1.8" marker-end="url(#aG)"/>')
    s.append(txt(206, 112, "mixer difference is the IF", 12, GRN, weight="600"))

    tail = ("IF = LO - RF = 12.725 - 10.525 = 2.200 GHz" if page_copy
            else "the Pluto only ever tunes 2.2 GHz")
    s.append(txt(W / 2, H - 14, tail, 12, INK3))
    s.append("</svg>")
    return "\n".join(s)


def main():
    DECK.mkdir(parents=True, exist_ok=True)
    PAGE.mkdir(parents=True, exist_ok=True)
    for name, fn in (("L17-signal-chain", signal_chain),
                     ("L17-frequency-plan", frequency_plan)):
        (DECK / f"{name}.svg").write_text(fn(False), encoding="utf-8")
        (PAGE / f"{name}.svg").write_text(fn(True), encoding="utf-8")
        print(f"wrote {name}.svg (deck + page)")


if __name__ == "__main__":
    main()
