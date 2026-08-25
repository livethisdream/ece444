#!/usr/bin/env python3
"""Annotate the NanoVNA screen photo with the marker-readout callouts.

Produces latex/figures/annotated_vna_readout.jpg for the L4 matching lab
(Figure "An example readout of a VNA measurement..."). The source photo is
latex/figures/nano_vna_initial.jpg; this script only adds a white band above
it carrying three labels, each with a red leader down to the line it names,
matching the callout style of vna_annotated.png.

    python3 scripts/graphics/l04_lab_vna_readout.py
"""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[2]
SRC = ROOT / "latex" / "figures" / "nano_vna_initial.jpg"
OUT = ROOT / "latex" / "figures" / "annotated_vna_readout.jpg"
PRINT_W = 1300            # the packet prints it at \textwidth (~6.5 in)

SCALE = 2                  # upscale the photo so the callout text sits well
BAND = 210 * SCALE         # white band above the photo, in output pixels
RED = (208, 32, 32)
INK = (17, 17, 17)
FONT = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"

# Callout targets, in ORIGINAL photo pixels (762 x 601). Each is the point the
# leader line ends on; see the screen rows:
#   row 1  CH0 LOGMAG 10dB/  -0.07dB       CH1 LOGMAG 10dB/  -88.14dB
#   row 2  CH0 SMITH 1.0FS   2.36ohm 2.90pF  CH0 PHASE 90/    -34.44deg
#   row 3                                   1 340.000 000 MHz
CALLOUTS = [
    dict(text="Trace: channel,\nquantity, scale\nper division",
         target=(110, 37), box_cx=140),
    dict(text="Marker value\non that trace",
         target=(270, 53), box_cx=380),
    dict(text="Marker number\nand frequency",
         target=(570, 72), box_cx=620),
]


def main():
    photo = Image.open(SRC).convert("RGB")
    ow, oh = photo.size
    photo = photo.resize((ow * SCALE, oh * SCALE), Image.LANCZOS)
    w, h = photo.size

    canvas = Image.new("RGB", (w, h + BAND), "white")
    canvas.paste(photo, (0, BAND))
    d = ImageDraw.Draw(canvas)
    font = ImageFont.truetype(FONT, 26 * SCALE // 2 + 6)

    for c in CALLOUTS:
        tx, ty = c["target"][0] * SCALE, c["target"][1] * SCALE + BAND
        lines = c["text"].split("\n")
        tw = max(d.textlength(ln, font=font) for ln in lines)
        lh = font.size + 6
        th = lh * len(lines)
        pad = 10
        bw, bh = tw + 2 * pad, th + 2 * pad
        bx = min(max(c["box_cx"] * SCALE - bw / 2, 6), w - bw - 6)
        by = BAND - bh - 26

        # leader first, so the box paints over its tail
        d.line([(bx + bw / 2, by + bh), (tx, ty)], fill=RED, width=3)
        d.ellipse([tx - 6, ty - 6, tx + 6, ty + 6], fill=RED)
        d.rectangle([bx, by, bx + bw, by + bh], fill="white", outline=RED, width=3)
        for i, ln in enumerate(lines):
            d.text((bx + bw / 2, by + pad + i * lh), ln, font=font,
                   fill=INK, anchor="ma")

    if canvas.size[0] > PRINT_W:
        canvas = canvas.resize(
            (PRINT_W, round(canvas.size[1] * PRINT_W / canvas.size[0])),
            Image.LANCZOS)
    canvas.save(OUT, quality=92, subsampling=0, optimize=True)
    print(f"wrote {OUT.relative_to(ROOT)}  {canvas.size[0]}x{canvas.size[1]}")


if __name__ == "__main__":
    main()
