# Render-verification harness

A page that builds is not a page that renders. Every defect Module 2 shipped
past the build — a frame too tall to present, a clipped widget, a distorted canvas, an
iframe pointing at nothing — was found by rendering the artifact in headless
chromium and measuring it. These scripts are that harness.

## Setup, once per container

```sh
pip install playwright                  # chromium is already installed
cd scripts/verify && npm install        # vendors MathJax
```

The CDNs (jsdelivr, Google Fonts) are blocked in the course containers, so
MathJax never loads on its own. `npm install` puts it in `node_modules/`, and
every checker reroutes CDN requests there. Without it the checkers stop with an
error rather than quietly reporting a page with no math as passing.

## Usage

```sh
# everything mechanical for one lesson
scripts/verify/mech_check.sh 07 simple-resonant-antennas

# or the pieces individually
scripts/verify/check_widget.py book/extras/viz/dipole-explorer.html
scripts/verify/check_page.py   module02/L07-simple-resonant-antennas/index.html
```

## Site-wide, after any change to the shell

These two take no arguments -- they sweep the whole build, so run them after
touching `book/_templates/`, `book/_static/shell.css`, `page.css`, `frames.css`,
or `_ext/frames.py`. Both need `jupyter-book build book/ --all` first.

```sh
scripts/verify/check_shell.py    # every page: no sideways scroll at 390px, no
                                 # JS error, the HUD's site button with its
                                 # panel closed, no theme asset sneaking back
scripts/verify/check_frames.py   # every frame fits one screen in present mode
scripts/verify/check_bar.py      # the bottom bar: centerd in the window, outer
                                 # runs equal, middle run centerd in the pill,
                                 # nothing wrapped, panels clickable
scripts/verify/check_print.py    # every frame page prints one sheet per frame,
                                 # and a slide-only handout from present mode;
                                 # every long reading page prints more than one
scripts/verify/check_parity.py <baseline-html-dir>
                                 # did the change quietly drop content?
```

`check_parity.py` needs a baseline built from whatever you are changing *from*:

```sh
git worktree add /tmp/base main
(cd /tmp/base && jupyter-book build book/ --all)
scripts/verify/check_parity.py /tmp/base/book/_build/html
```

It compares the rendered text and the component counts (callouts, two-col, LO
lists, module TOCs, math nodes, tables) of every page present in both builds.
A run that compares **zero** pages fails rather than passes — it was silently
vacuous once, when a new template's content region matched none of its
patterns.

`check_frames.py` takes an optional path filter, which is how the per-lesson
gate holds one converted lesson to the budget without sweeping all 41:

```sh
scripts/verify/check_frames.py L07-simple-resonant-antennas
```

`check_frames.py` holds every frame to one screen. A frame taller than the viewport is clipped in present mode with
nothing to say so -- it found five such frames on L05a that had been live for
weeks. Frames that scroll on purpose (the widget frames, which stack their own
controls as they narrow) are exempt and counted separately in the output.
```
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
| `check_widget.py` | worst-case height across the real serving widths; zero horizontal overflow at 430/390/320; canvas aspect undistorted; no blank canvas; no console errors |
| `check_page.py` | math typeset; no raw `$$`/`$` leaking into the article; iframe targets resolve |
| `check_tables.py` | markdown table rows where a `|` inside `$...$` splits a cell |
| `check_print.py` | `.deck`'s scroller does not clip `@media print` to one sheet; read mode prints the depth; present mode prints the slide handout (no depth, no read-only frames, a sheet per slide); the bar/rail/overlay/laser/spotlight are gone on paper |
| `check_records.py` | every field a lab page's Part 2 boxes ask for (`data-field`) exists in the packet PDF its summary frame fills (`data-pdf`); a renamed `\kv[name]` in the faculty LaTeX or a typo on the page would otherwise save, download, and silently leave the value out |
| `mech_check.sh` | all of the above for one lesson, plus files present, LaTeX compiles without errors or overfull boxes >10pt, every `\part` has a `\begin{solution}`, LO markup matches the module, no thin spaces, no `\|` inside table math, no self-vouching wording |

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
