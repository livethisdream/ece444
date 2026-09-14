#!/usr/bin/env python3
"""One font declaration for every figure SVG, in both trees.

A deck figure is inlined by deck-tools.js and inherits the deck's Source Sans
Pro, so for a long time the generators wrote `font-family:inherit`. A lesson
page loads the same file through <img>, and an <img> is an isolated document:
nothing is there to inherit from, so `inherit` falls to the browser's default
serif, and a hand-authored SVG with no font-family at all does the same.
Found on 2026-09-14 on the L08 and L09 figures; every earlier page copy had
it too.

The fix is the same explicit stack everywhere. It names the deck's face first,
so an inlined deck figure looks exactly as it did, and it names the system
sans faces a browser can reach from inside an <img>.

Two uses:

    from svg_font_stack import apply_font_stack     # in a generator, on the
    s = apply_font_stack(s)                          # SVG text before writing

    python3 scripts/graphics/svg_font_stack.py      # sweep both trees in place
"""

from __future__ import annotations
import re
import sys
from pathlib import Path

FONT_STACK = "'Source Sans Pro', 'Segoe UI', Roboto, Helvetica, Arial, sans-serif"

ROOT = Path(__file__).resolve().parents[2]
TREES = (ROOT / "book/extras/viz/img", ROOT / "book/extras/slides/fig")

_STYLE = re.compile(r"font-family\s*:\s*[^;}\"]+")          # inside style="..." or <style>
_ATTR = re.compile(r'font-family="[^"]*"')                  # the attribute form
_ROOT = re.compile(r"<svg\b")


def apply_font_stack(svg: str) -> str:
    """Rewrite every font-family in `svg` to FONT_STACK; if there is none,
    put one on the root element so every <text> inherits it."""
    svg = _STYLE.sub("font-family:" + FONT_STACK, svg)
    svg = _ATTR.sub('font-family="' + FONT_STACK + '"', svg)
    if "font-family" not in svg:
        svg = _ROOT.sub('<svg font-family="' + FONT_STACK + '"', svg, count=1)
    return svg


def main() -> int:
    changed = 0
    for tree in TREES:
        for p in sorted(tree.glob("*.svg")):
            before = p.read_text(encoding="utf-8")
            after = apply_font_stack(before)
            if after != before:
                p.write_text(after, encoding="utf-8")
                changed += 1
    print(f"rewrote {changed} SVG(s) to the shared font stack")
    return 0


if __name__ == "__main__":
    sys.exit(main())
