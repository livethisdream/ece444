# Render-verification harness

A page that builds is not a page that renders. Every defect Module 2 shipped
past the build — raw `$$` on a slide, a clipped widget, a distorted canvas, an
iframe pointing at nothing — was found by rendering the artifact in headless
chromium and measuring it. These scripts are that harness.

## Setup, once per container

```sh
pip install playwright                  # chromium is already installed
cd scripts/verify && npm install        # vendors reveal.js + mathjax
```

The CDNs (jsdelivr, Google Fonts) are blocked in the course containers, so
reveal.js and MathJax never load on their own. `npm install` puts them in
`node_modules/`, and every checker reroutes CDN requests there. Without it the
checkers stop with an error rather than quietly reporting a deck with no math
as passing.

## Usage

```sh
# everything mechanical for one lesson
scripts/verify/mech_check.sh 07 simple-resonant-antennas

# or the pieces individually
scripts/verify/check_deck.py   L07-simple-resonant-antennas
scripts/verify/check_widget.py book/extras/viz/dipole-explorer.html
scripts/verify/check_page.py   module02/L07-simple-resonant-antennas/index.html
scripts/verify/check_tables.py book/module02/L07-simple-resonant-antennas/index.md
```

`mech_check.sh` needs `TEXINPUTS` pointed at the private `latex-tools` macros
for the practice build:

```sh
TEXINPUTS=/workspace/latex-tools/tex/latex//: \
  scripts/verify/mech_check.sh 07 simple-resonant-antennas
```

`check_page.py` reads `book/_build/html`, so build first — and always with
`--all`, since an incremental build silently skips changes under
`book/extras/**`.

## What each one checks

| Script | Checks |
| :-- | :-- |
| `check_deck.py` | slide count; every slide fits the 700px stage; no raw `$$` or literal `\_` after MathJax typesets; no missing figures |
| `check_widget.py` | worst-case height across the real serving widths; zero horizontal overflow at 430/390/320; canvas aspect undistorted; no blank canvas; no console errors |
| `check_page.py` | math typeset; no raw `$$`/`$` leaking into the article; iframe targets resolve |
| `check_tables.py` | markdown table rows where a `|` inside `$...$` splits a cell |
| `mech_check.sh` | all of the above for one lesson, plus files present, LaTeX compiles without errors or overfull boxes >10pt, every `\part` has a `\begin{solution}`, LO markup matches the module, no thin spaces, no `\,`/`\;` in deck math, no `\|` inside table math, no self-vouching wording |

## Two measurement rules worth keeping

**Widget heights are measured at the widths a reader actually gets.** The
Sphinx book theme caps the article column: a lesson-page iframe renders
between 688px (at a 1280 viewport) and 790px (the cap). Height is not
monotonic in width — canvases grow as it widens, but readout and control
breakpoints add rows as it narrows — so `check_widget.py` sweeps the range and
reports the worst case. Measuring at 900px, which no reader ever sees,
under-reports it, and four Module 2 widgets shipped clipped because of that.

**Overflow is checked at phone widths.** The course is reviewed on a phone.
Zero horizontal overflow at 320px is a requirement, not a nicety.

`_static/viz-autosize.js` sizes iframes at runtime from the widget's own
`scrollHeight`, so the `height=` attribute on the iframe is only the no-JS
fallback. `check_widget.py` still prints the number to use for it.
