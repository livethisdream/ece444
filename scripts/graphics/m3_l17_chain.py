#!/usr/bin/env python3
"""L17 figures: the ADALM-PHASER receive chain and its frequency plan.

Emits two copies of each figure - a deck copy (no equations, block names and
frequencies only) and a lesson-page copy (plus the one line of mixing
arithmetic). The signal chain has one geometry; the frequency plan has two,
a present-column layout for the page and a wide one for its deck slide
(FP_LAYOUT).

    python3 scripts/graphics/m3_l17_chain.py

Writes:
    book/extras/slides/fig/L17-signal-chain.svg
    book/extras/slides/fig/L17-frequency-plan.svg
    book/extras/viz/img/L17-signal-chain.svg
    book/extras/viz/img/L17-frequency-plan.svg
"""

from __future__ import annotations

from pathlib import Path
from svg_font_stack import apply_font_stack

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

# Band edges for the frequency plan, GHz. The reachable RF band is derived
# (LO_MIN - F_IF to LO_MAX - F_IF), so a measured LO ceiling, such as the
# 12.80 GHz the installer warns about, is a change to LO_MAX alone.
LO_MIN, LO_MAX = 12.2, 13.0     # HMC735 VCO range
HB_MIN, HB_MAX = 10.1, 10.7     # HB100 unit-to-unit spread


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


def arrow_defs(prefix=""):
    """Arrowhead markers. A deck inlines every figure into one document, where
    a second marker with the same id resolves to the first, so a figure that
    shares a deck with another passes its own prefix."""
    out = ["<defs>"]
    for name, color in (("aN", NAVY), ("aA", AMBER), ("aG", GRN), ("aI", INK3)):
        out.append(
            f'<marker id="{prefix}{name}" viewBox="0 0 10 10" refX="9" refY="5" '
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
    ys = [72 + 34 * i for i in range(8)]           # element centers
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
# Figure 2 - the frequency plan: the LO band projected down onto the RF axis
# --------------------------------------------------------------------------

# Two layouts of one drawing. The page copy sits in a present column (477 px
# at 1280x800, 343 px on a phone): viewBox 420 wide with 13-unit labels, so
# 10.6 px on a phone and larger everywhere else. The deck copy is inlined at
# up to 790 px on a slide whose height budget is 700 px, so it keeps the wide,
# short aspect the slide was laid out for, with larger labels.
FP_LAYOUT = {
    True: dict(W=420, H=300, px=560, X0=30, X1=400, fs=13, fb=13.5, lo_ax=38,
               lo_bot=80, br_y=168, hb_top=196, rf_ax=238, if_y=124, tick=(10, 19),
               line2=16, row_x=8),
    False: dict(W=800, H=300, px=800, X0=64, X1=772, fs=15, fb=16, lo_ax=40,
                lo_bot=88, br_y=166, hb_top=196, rf_ax=246, if_y=124, tick=(11, 22),
                line2=19, row_x=12),
}


def frequency_plan(page_copy: bool) -> str:
    """Two axes, LO above and RF below, offset by the IF so that every LO sits
    directly above the RF it receives. The LO band's edges then drop straight
    down onto the RF axis as the reachable band, and the HB100 spread sits
    inside it. The fixed IF is the vertical arrow from the nominal source's LO
    down to the source."""
    g = FP_LAYOUT[page_copy]
    W, H, X0, X1, fs, fb = g["W"], g["H"], g["X0"], g["X1"], g["fs"], g["fb"]
    S = g["px"] / W
    RF0, RF1 = 9.9, 11.0                           # RF axis span, GHz
    ppg = (X1 - X0) / (RF1 - RF0)                  # units per GHz, both axes

    def xr(f):                                     # an RF frequency
        return X0 + (f - RF0) * ppg

    def xl(f):                                     # an LO frequency, IF above
        return xr(f - F_IF)

    reach_lo, reach_hi = LO_MIN - F_IF, LO_MAX - F_IF
    lo_ax, lo_bot, br_y = g["lo_ax"], g["lo_bot"], g["br_y"]
    hb_top, rf_ax, l2 = g["hb_top"], g["rf_ax"], g["line2"]
    up, down = g["tick"]

    def t(x, y, s_, size=fs, fill=INK, anchor="middle", weight="400"):
        return txt(f"{x:.1f}", f"{y:.1f}", s_, size, fill, anchor, weight)

    def ghz(v):
        return f"{v:.1f}"

    s = [
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" '
        f'width="{W * S:.0f}" height="{H * S:.0f}" role="img" '
        f'aria-label="PHASER frequency plan. The LO tunes {ghz(LO_MIN)} to '
        f'{ghz(LO_MAX)} GHz; shifted down by the fixed {F_IF} GHz IF, that range '
        f'reaches RF from {ghz(reach_lo)} to {ghz(reach_hi)} GHz, which encloses '
        f'the {ghz(HB_MIN)} to {ghz(HB_MAX)} GHz spread of HB100 units.">',
        arrow_defs("fp"),
    ]

    # the reachable band on the RF row: the LO band's shadow, shaded to the axis
    s.append(f'<rect x="{xr(reach_lo):.1f}" y="{br_y}" '
             f'width="{xr(reach_hi) - xr(reach_lo):.1f}" height="{rf_ax - br_y}" '
             f'fill="#fdf6e8" stroke="none"/>')
    for f in (LO_MIN, LO_MAX):                     # the projections
        s.append(line(f"{xl(f):.1f}", lo_bot, f"{xl(f):.1f}", rf_ax, AMBER, 1.3,
                      ' stroke-dasharray="4 3"'))
    s.append(line(f"{xr(reach_lo):.1f}", br_y, f"{xr(reach_hi):.1f}", br_y, AMBER, 2.0))
    s.append(t(xr(reach_lo) + 6, br_y - 7 - l2, "reachable", fb, AMBER, "start", "700"))
    s.append(t(xr(reach_lo) + 6, br_y - 7,
               f"{ghz(reach_lo)} – {ghz(reach_hi)} GHz", fs, AMBER, "start"))

    # LO axis on top, ticks and labels above it, the VCO band hanging below
    s.append(line(X0, lo_ax, X1, lo_ax, INK, 1.4))
    for f in (12.2, 12.4, 12.6, 12.8, 13.0):
        s.append(line(f"{xl(f):.1f}", lo_ax, f"{xl(f):.1f}", lo_ax - 5, INK3, 1.1))
        s.append(t(xl(f), lo_ax - up, ghz(f), fs, INK3))
    s.append(t(X1 + 4, lo_ax - up, "GHz", fs, INK3, "end"))
    s.append(f'<rect x="{xl(LO_MIN):.1f}" y="{lo_ax}" '
             f'width="{xl(LO_MAX) - xl(LO_MIN):.1f}" height="{lo_bot - lo_ax}" '
             f'rx="3" fill="#fdf6e8" stroke="{AMBER}" stroke-width="1.5"/>')
    cx = (xl(LO_MIN) + xl(F_LO)) / 2 - 6
    mid = (lo_ax + lo_bot) / 2
    s.append(t(cx, mid - l2 / 2 + 4, "LO, the VCO", fb, AMBER, weight="700"))
    s.append(t(cx, mid + l2 / 2 + 4, f"{ghz(LO_MIN)} – {ghz(LO_MAX)} GHz", fs, AMBER))
    s.append(t(g["row_x"], mid + 5, "LO", fs + 1, AMBER, "start", "700"))

    # RF axis below, the HB100 spread sitting on it
    s.append(f'<rect x="{xr(HB_MIN):.1f}" y="{hb_top}" '
             f'width="{xr(HB_MAX) - xr(HB_MIN):.1f}" height="{rf_ax - hb_top}" '
             f'rx="3" fill="#eaf2f9" stroke="{NAVY}" stroke-width="1.5"/>')
    cx = (xr(HB_MIN) + xr(F_RF)) / 2 - 4
    mid = (hb_top + rf_ax) / 2
    s.append(t(cx, mid - l2 / 2 + 4, "HB100 spread", fb, NAVY, weight="700"))
    s.append(t(cx, mid + l2 / 2 + 4, f"{ghz(HB_MIN)} – {ghz(HB_MAX)} GHz", fs, NAVY))
    s.append(line(X0, rf_ax, X1, rf_ax, INK, 1.4))
    for f in (10.0, 10.2, 10.4, 10.6, 10.8):
        s.append(line(f"{xr(f):.1f}", rf_ax, f"{xr(f):.1f}", rf_ax + 5, INK3, 1.1))
        s.append(t(xr(f), rf_ax + down, ghz(f), fs, INK3))
    s.append(t(X1 + 4, rf_ax + down, "GHz", fs, INK3, "end"))
    s.append(t(g["row_x"], mid + 5, "RF", fs + 1, NAVY, "start", "700"))

    # the fixed IF: the worked source and its LO, one IF apart
    xw = xr(F_RF)
    s.append(f'<circle cx="{xw:.1f}" cy="{lo_bot}" r="4" fill="{AMBER}"/>')
    s.append(f'<circle cx="{xw:.1f}" cy="{hb_top}" r="4" fill="{NAVY}"/>')
    s.append(line(f"{xw:.1f}", lo_bot + 6, f"{xw:.1f}", hb_top - 7, GRN, 2.2,
                  ' marker-end="url(#fpaG)"'))
    # right of the arrow, unless a lower LO ceiling brings the right-hand
    # projection in under it; then left, where the reachable label sits lower
    right = xl(LO_MAX) - xw > 7.1 * fs
    lx, anc = (xw + 8, "start") if right else (xw - 8, "end")
    s.append(t(lx, g["if_y"], f"IF {F_IF} GHz", fb, GRN, anc, "700"))
    s.append(t(lx, g["if_y"] + l2, "fixed", fs, GRN, anc))

    tail = (f"IF = LO − RF = {F_LO:.3f} − {F_RF} = {F_IF:.3f} GHz" if page_copy
            else f"the Pluto only ever tunes {F_IF} GHz")
    s.append(t(W / 2, H - 10, tail, fs, INK3))
    s.append("</svg>")
    return "\n".join(s)


def main():
    DECK.mkdir(parents=True, exist_ok=True)
    PAGE.mkdir(parents=True, exist_ok=True)
    for name, fn in (("L17-signal-chain", signal_chain),
                     ("L17-frequency-plan", frequency_plan)):
        (DECK / f"{name}.svg").write_text(apply_font_stack(fn(False)), encoding="utf-8")
        (PAGE / f"{name}.svg").write_text(apply_font_stack(fn(True)), encoding="utf-8")
        print(f"wrote {name}.svg (deck + page)")


if __name__ == "__main__":
    main()
