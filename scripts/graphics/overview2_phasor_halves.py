#!/usr/bin/env python3
"""Radar Overview 2 shows the two halves of L29-phasor.svg on different frames:
the 5.8-degree steps with the Doppler FFT, and the aliasing circle with the
velocity limit. Each half is the L29 figure with its viewBox set to one side,
so the drawing stays the L29 generator's (m4_l29_range_doppler_mti.py); run
this after that one.
"""
import pathlib
import re

IMG = pathlib.Path(__file__).resolve().parents[2] / "book/extras/viz/img"


def main() -> None:
    src = (IMG / "L29-phasor.svg").read_text()
    m = re.search(r'width="([\d.]+)pt" height="([\d.]+)pt" viewBox="0 0 ([\d.]+) ([\d.]+)"', src)
    assert m, "L29-phasor.svg header changed"
    w, h = float(m.group(3)), float(m.group(4))
    half = w / 2
    for name, x0 in (("overview2-phasor-steps", 0.0), ("overview2-phasor-alias", half)):
        head = f'width="{half:g}pt" height="{h:g}pt" viewBox="{x0:g} 0 {half:g} {h:g}"'
        (IMG / f"{name}.svg").write_text(src[:m.start()] + head + src[m.end():])
        print("wrote", name)


if __name__ == "__main__":
    main()
