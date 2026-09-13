#!/usr/bin/env python3
"""Assemble the hosted simulator into book/extras/simulator/.

The site is static -- GitHub Pages serves files and nothing else -- so the
whole tool has to be files: NEC-2 as WebAssembly, Python as Pyodide, and
nec_lab's own source copied in beside them. `html_extra_path: ["extras"]` puts
the result at <site>/simulator/.

    python scripts/nec_lab/wasm/assemble_site.py --pyodide DIR --nec2 DIR

Both inputs are build outputs, not source: `--nec2` is what wasm/build.sh
produced, `--pyodide` is an unpacked pyodide release. They are vendored rather
than pulled from a CDN at run time, because this tool's whole point has been
not depending on what a managed machine is allowed to reach.
"""

from __future__ import annotations

import argparse
import shutil
from pathlib import Path

HERE = Path(__file__).resolve().parent
PKG = HERE.parent
OUT = PKG.parent.parent / "book" / "extras" / "simulator"

# What Pyodide needs at run time. Its other files are types, docs and the
# package index, none of which a page that imports nothing needs.
PYODIDE_FILES = ("pyodide.js", "pyodide.mjs", "pyodide.asm.mjs",
                 "pyodide.asm.wasm", "python_stdlib.zip", "pyodide-lock.json")

# nec_lab's own modules, minus the ones that only make sense with an OS under
# them. cli and serve want a shell and a socket; engine still ships because
# WasmEngine lives in it.
PY_MODULES = ("__init__.py", "api.py", "builders.py", "cards.py", "engine.py",
              "export.py", "model.py", "reference.py", "study.py")

STATIC = ("app.js", "style.css", "boot-hosted.js")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--pyodide", required=True, type=Path,
                    help="an unpacked pyodide release")
    ap.add_argument("--nec2", required=True, type=Path,
                    help="the directory wasm/build.sh wrote nec2.js/.wasm into")
    ap.add_argument("--out", type=Path, default=OUT)
    a = ap.parse_args()

    out = a.out
    (out / "pyodide").mkdir(parents=True, exist_ok=True)
    (out / "nec_lab").mkdir(parents=True, exist_ok=True)

    for name in PYODIDE_FILES:
        src = a.pyodide / name
        if not src.exists():
            print(f"missing from the pyodide build: {name}")
            return 2
        shutil.copy2(src, out / "pyodide" / name)

    for name in ("nec2.js", "nec2.wasm"):
        src = a.nec2 / name
        if not src.exists():
            print(f"missing from the nec2 build: {name} -- run wasm/build.sh")
            return 2
        shutil.copy2(src, out / name)

    for name in PY_MODULES:
        shutil.copy2(PKG / name, out / "nec_lab" / name)
    for name in STATIC:
        shutil.copy2(PKG / "static" / name, out / name)

    # The page differs from the served one by two lines: the file list the boot
    # script fetches, and the boot script itself in place of app.js, which it
    # injects once Python and the solver are standing.
    html = (PKG / "static" / "index.html").read_text()
    files = ", ".join(f'"{n}"' for n in PY_MODULES)
    html = html.replace(
        '<script src="app.js"></script>',
        f'<script>window.NEC_LAB_PY_FILES = [{files}];</script>\n'
        '<script src="boot-hosted.js"></script>')
    html = html.replace(
        "<title>ECE 444 nec_lab -- NEC-2 wire modeling</title>",
        "<title>ECE 444 nec_lab -- NEC-2 wire modeling (in your browser)</title>")
    (out / "index.html").write_text(html)

    (out / "NOTICE.md").write_text(NOTICE)

    total = sum(f.stat().st_size for f in out.rglob("*") if f.is_file())
    print(f"wrote {out} ({total / 1048576:.1f} MB)")
    print("serve-time URL: <site>/simulator/")
    return 0


NOTICE = """# What is in this directory, and where it came from

This is nec_lab running with no server: the page loads NEC-2 compiled to
WebAssembly and nec_lab's own Python under Pyodide, and answers every request
in the browser.

| Path | What | License |
| :-- | :-- | :-- |
| `nec2.js`, `nec2.wasm` | NEC-2, from the `nec2c` C translation, compiled with Emscripten | **GPL-2.0-or-later** |
| `pyodide/` | Pyodide: CPython compiled for the browser | MPL-2.0 |
| `nec_lab/` | this course's simulator, copied from `scripts/nec_lab/` | course material |
| `app.js`, `style.css`, `boot-hosted.js` | the page | course material |

## The GPL obligation, plainly

`nec2.wasm` is a compiled form of nec2c, which is GPL. Publishing it means the
corresponding source must be available. It is:

- upstream source: <https://github.com/KJ7LNW/nec2c>
- the exact build that produced this file: `scripts/nec_lab/wasm/build.sh` in
  this repository, which names the commit it fetches and the flags it uses.

Anyone who has this page has both, and this repository is public. If that ever
stops being true -- a private mirror, a different host -- the source offer has
to travel with the binary.
"""


if __name__ == "__main__":
    raise SystemExit(main())
