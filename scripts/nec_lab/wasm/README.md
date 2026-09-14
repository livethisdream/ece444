# NEC-2 in the browser — a spike, not yet a product

The question: can nec_lab live on the course's GitHub Pages site, so a student
opens a link and there is nothing to install, no server, and no address to
type? The answer is yes for the hard-looking half, and the remaining work is
not the solver.

## What was proved

`build.sh` compiles nec2c to WebAssembly. Run in Chromium against the native
binary on the same decks:

| deck | WebAssembly | native `nec2c` |
| :-- | :-- | :-- |
| L8 dipole at exactly lambda/2 | 86.99 + j49.59 ohm, 2.18 dBi | 86.99 + j49.59 ohm, 2.18 dBi |
| 3-element Yagi | 22.25 + j20.23 ohm, 9.00 dBi | 22.25 + j20.23 ohm, 9.00 dBi |
| quarter-wave monopole over ground | 36.24 + j1.08 ohm, 5.15 dBi | 36.24 + j1.08 ohm, 5.15 dBi |

Identical to the printed precision, including the ground-plane case. Solves
took 2 to 28 ms in the browser, the larger number including module start-up.
The module is 255 KB of wasm plus 64 KB of loader — smaller than most photos
on the site.

## What is left, and it is the bigger half

The solver was never the expensive part. nec_lab's logic is Python:

| file | lines | what |
| :-- | --: | :-- |
| `model.py` | 446 | geometry, feeds, ground, the cards they write |
| `cards.py` | 404 | reading cards back, the field glosses, the complaints |
| `builders.py` | 270 | the antenna catalog |
| `study.py` | 142 | sweep, resonance, trim, convergence |
| `export.py` | 136 | the CSVs and the comparison table |
| | **1422** | all of it standard library only |

Only `cli.py`, `engine.py` and `serve.py` touch the OS, and `engine.py` is the
part a wasm build replaces. So there are two routes:

- **Pyodide.** Runs the 1422 lines unchanged, which means the browser runs the
  same code the 86 selftest checks already guard. Costs a several-megabyte
  first load, cached afterwards.
- **Port to JavaScript.** No download, but a second implementation of the card
  parser and the studies that the selftest cannot see. Those two copies will
  drift, and the drift will be silent and physics-shaped.

Pyodide is the recommendation for exactly that reason: one implementation, one
set of tests.

## Licensing, before any of this ships

nec2c is GPL. Publishing the built `.wasm` on a public site means the
corresponding source has to be offered with it — `build.sh` names the upstream
repository and the exact build, which is the honest version of that offer, but
check it properly before the artifact goes into `book/`.
