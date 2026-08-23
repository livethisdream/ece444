#!/usr/bin/env python3
"""Find math spans broken across markdown table cells.

Usage: check_tables.py <file.md> [<file.md> ...]

A '|' inside $...$ splits a markdown table cell, so the row renders with a
stray column and the math never typesets. The fix is \\vert or \\lvert.

Detecting this needs a parse, not a grep: a row like

    | $50\\ \\Omega$ | $73 + j42.5$ | 0.37 |

has a '|' between two math spans, which is correct, and a naive pattern
cannot tell it from a '|' inside one. What actually marks the defect is a
cell containing an odd number of unescaped '$'.

Exit 0 = no broken rows.
"""
import pathlib
import re
import sys

# '$' preceded by a backslash is a literal dollar sign, not a math delimiter.
UNESCAPED_DOLLAR = re.compile(r"(?<!\\)\$")


def check(path):
    bad = []
    for n, line in enumerate(path.read_text().splitlines(), 1):
        stripped = line.strip()
        if not stripped.startswith("|"):
            continue
        # A table row's leading and trailing '|' are delimiters, not cells.
        cells = stripped.strip("|").split("|")
        for cell in cells:
            if len(UNESCAPED_DOLLAR.findall(cell)) % 2:
                bad.append((n, line.rstrip()))
                break
    return bad


def main():
    if len(sys.argv) < 2:
        raise SystemExit(f"usage: {sys.argv[0]} <file.md> [...]")
    total = 0
    for arg in sys.argv[1:]:
        path = pathlib.Path(arg)
        if not path.exists():
            continue
        for n, line in check(path):
            print(f"  {path}:{n}: {line[:100]}")
            total += 1
    if total:
        print(f"FAIL: {total} table row(s) with a '|' inside math; use \\vert")
        sys.exit(1)


if __name__ == "__main__":
    main()
