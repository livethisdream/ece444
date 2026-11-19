# What is in this directory, and where it came from

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
