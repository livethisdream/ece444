# ECE 444 — working notes for Claude

Course site for **ECE 444, Antennas, Phased Arrays, and Radar Systems** (USAFA,
Fall 2026). Jupyter Book under `book/`, reveal.js decks served alongside it,
published to GitHub Pages on every push to `main`. 5 modules, 41 lessons; Module
1 is written, Modules 2–5 are mostly shells.

`project/ECE 444.md` is the running project note — status, decisions, and open
ToDos. Read it before starting substantial work, and update its Status/ToDo
sections when you finish. It is shared across concurrent sessions, so it is a
conflict magnet: keep edits to it small and localized.

## Layout

| Path | What |
| :-- | :-- |
| `book/moduleNN/<slug>/index.md` | the lesson page (MyST markdown) |
| `book/extras/slides/<slug>.md` | the reveal.js deck; `.html` wrapper is generated |
| `book/extras/slides/fig/*.svg` | deck figures, inlined at load by `deck-tools.js` |
| `book/extras/viz/*.html` | interactive widgets, iframed from lesson pages |
| `book/extras/viz/img/*.svg` | lesson-page figures |
| `book/extras/practice/*.pdf` | **committed** practice PDFs — what the site actually serves |
| `latex/ECE444_Practice_L<NN>.tex` | practice source; `_main.tex` is the harness |
| `book/_templates/` | the shell: `frame.html`, `page.html`, `_sitenav.html` |
| `book/_static/shell.*` | palette, type, the bottom bar, the index overlay — every page |
| `book/_static/frames.*` | frame lessons only; `page.*` reading pages only |
| `book/_ext/frames.py` | the `:::{frame}` directives, and which template a page gets |
| `scripts/` | deck HTML generator, lesson scaffolder, figure generators |

## Build and verify

```sh
pip install -r requirements.txt
jupyter-book build book/ --all          # ALWAYS --all (see gotchas)
```

Practice PDFs need the **private** `livethisdream/latex-tools` repo for the house
macros (`myPackages_gr`, `myShortcuts`, `exam_config`). Attach it in-session, then:

```sh
git clone --depth 1 https://github.com/livethisdream/latex-tools /workspace/latex-tools
TEXINPUTS=/workspace/latex-tools/tex/latex//: bash latex/build_practice.sh 06
```

The SessionStart hook installs both toolchains and pre-exports `TEXINPUTS`, so in
a web session only the attach + clone is left to do.

Both build scripts run **lualatex**: body text is Barlow, vendored in
`latex/fonts/Barlow/` and loaded by path through `fontspec` (`ece444_fonts.tex`).
Math is deliberately left in Computer Modern. Building with pdflatex still
compiles — the font setup is guarded by `\ifLuaTeX` — but silently falls back to
Computer Modern throughout, so the PDF is not the one we ship.

Three checks are site-wide rather than per-lesson. Run them once at the end of
a batch, not per page:

```sh
scripts/verify/check_shell.py     # every page at 390 and 1280: no sideways
                                  # scroll, no JS error, no theme asset
scripts/verify/check_bar.py       # the bottom bar's geometry, both shells
scripts/verify/check_parity.py <baseline-html-dir>
                                  # did this change quietly drop content?
```

`check_parity.py` wants a baseline built from whatever you are changing *from*
(`git worktree add /tmp/base main && cd /tmp/base && jupyter-book build book/
--all`). It compares rendered text and component counts page for page. The
pages you meant to rewrite will be listed — that is the point; the list should
be exactly the pages you touched.

**Verify by rendering, not by reading.** Headless chromium is available. The CDNs
(jsdelivr, Google Fonts) are blocked in these containers, so reveal.js and MathJax
never load on their own — vendor them from npm (`npm i reveal.js@5.1.0 mathjax@3`)
into `book/_build/` and repoint the built HTML at the local copies. Every defect
listed below was found that way and would have shipped otherwise.

## Gotchas that silently ship wrong

These do not error. They produce a page or slide that looks fine to the build and
wrong to a reader.

**Lesson pages (MyST)**

- **Math inside a raw-HTML block is not processed.** The LO list is a raw
  `<ol><li>`, so `$2D^2/\lambda$` there ships as literal TeX — MyST does not touch
  `$...$` inside raw HTML, and the site's MathJax only handles `\(...\)` there.
  Keep math out of LO items, or use `\(...\)`.
- **A `|` inside `$...$` splits a markdown table cell.** Use `\vert` / `\lvert`
  in tables: `$\vert F(\theta)\vert$`, never `$|F(\theta)|$`.
- Use `\ ` for spacing, not `\,` or `\;` — matches every existing page.

**Decks (reveal.js + marked)**

The markdown parser mangles LaTeX in four specific ways:

- `\<punct>` escapes inside `$…$` are eaten. Use `\lbrace`/`\rbrace`; drop
  `\,`/`\;`. Word macros (`\quad`, `\text{ }`) are safe.
- `}_{…}` reads as `_italic_` and the underscores vanish, rendering a raw `$$`.
  Escape as `}\_{` in markdown regions. Inside a raw-HTML block (`two-col`) do
  the **opposite** — marked passes it through, so write a plain `_`.
- Inside a multi-line `$$…$$`, no continuation line may start with `+`, `-`, or
  `*` — markdown reads a list bullet, splits the `$$` pair, and the slide shows a
  raw `$$`. Put the operator at the end of the previous line, or keep each `$$`
  on one line (simplest, and what L06 does).
- MyST is immune to all of this, so the *same equation* can render on the lesson
  page and break on the slide. Check the deck itself.
- **A `---` needs a blank line above *and* below** to separate slides. The
  wrapper's `data-separator` regex requires both; miss either and the `---`
  renders as an `<hr>` (or, with nothing blank above it, promotes the line
  before it to an `<h2>`), the two slides merge, and the first one's speaker
  notes appear on screen. It then reads as a too-tall slide rather than a dead
  separator — L04 shipped two merged pairs measuring 1235px and 1710px. Run
  `scripts/verify/check_separators.py` before trimming any slide for height.

**Frame lessons (`frame_view: true`)**

A frame lesson is an ordinary MyST page whose body is `:::{frame}` directives —
the lesson page and its deck merged into one document, one full-viewport frame
per beat. `book/module01/L05a-field-regions-frames/` is the worked example; the
landing page and the five module overviews are built the same way.

- **A frame's title is a directive ARGUMENT, not a heading.** `::::{frame} The
  three regions`, never `## The three regions` inside the frame. docutils
  demotes a heading inside a container to a rubric, so the `##` form silently
  loses its place in the document structure.
- **Fence lengths nest.** The frame is `::::`, anything inside it — `callout`,
  `depth`, `note` — is `:::`. Same-length fences close the outer block early
  and the rest of the frame lands outside it.
- **Every frame must fit one screen in present mode.** This is the deck's
  "slide too tall" defect in a new place: nothing errors, the build is happy,
  and the bottom of the frame is simply gone when you present it. Five such
  frames sat on L05a for weeks. `scripts/verify/check_frames.py <LNN>` measures
  it, and `mech_check.sh` gates on it for any page with `frame_view` set.
- **A bare `<img>` is capped at 58vh** in present mode, and a widget frame
  (`:class: viz-frame`) is allowed to scroll — a widget stacks its own controls
  as it narrows and genuinely cannot be shrunk to fit. Nothing else may scroll.
- **`:::{depth}` is the detail that shows in read mode and hides in present.**
  It is always in the DOM, so it stays searchable and stays in the page's text.
- MyST is immune to the whole `marked` gotcha class above — Sphinx renders the
  math once. The raw-HTML rule still bites: no `$…$` inside a raw `<ol><li>`.

**The shell**

Every page is chrome-free: no sidebar, no header, one centred bar at the bottom
(`ECE 444 | present tools | 12/27`). `book/_ext/frames.py` routes each page to
`frame.html`, `page.html`, or the theme. Two things to know before touching it:

- `ece444_shell: false` in `_config.yml` reverts the whole site to the theme in
  one line. `shell: false` in a page's front matter does it for one page.
- `custom.css` is **load-bearing and mis-scoped**: 149 of its 256 rules are
  scoped `.bd-article`, the theme's wrapper, and that is where every content
  component lives. Both templates carry `class="bd-article"` for exactly that
  reason. Do not remove it without rewriting those rules.

**Build**

- A change touching only `book/extras/**` leaves Sphinx with no out-of-date
  target: it prints "no targets are out of date", skips copying extra files, and
  serves the *previous* deck. Always `jupyter-book build book/ --all`.

## Conventions

- **Per-lesson bundle** = lesson page + deck + practice set + solutions
  (+ lab packet for lab lessons) + interactives where they earn their place.
- **Learning objectives** use "I can…" voice under a `## Learning Objectives`
  header. Fleshed-out lessons render 3-level numbers via
  `<ol class="lo-list lo-sublist" style="--module: '1'; --lo: '6'">`; stub lessons
  use base `.lo-list` with a counter offset for a 2-level echo number.
- **The decks are the source of truth for nomenclature.** Reconcile lesson pages
  to the decks, not the other way round.
- **Figures are native inline SVG**, generated by committed scripts in
  `scripts/graphics/` where they are data plots. Deck figures carry **no
  equations** — put the math in the slide text so it inherits the deck font.
  Lesson-page copies live in `viz/img/` and may include formulas.
- **Widgets** are vanilla canvas + `mjlabel.js`, in the house palette. MathJax is
  for symbols only; words, units, and numbers are drawn in the sans UI font.
  Set the iframe height to the widget's measured height.
- **No thin spaces** (U+2009) anywhere in markdown or LaTeX — course rule.
- Practice problems are labeled at the **2nd LO level**, one `LO 1.X` banner per
  set.

## Don'ts

- **Never use MATLAB.** Course software is Python or another FOSS language —
  labs, examples, analysis scripts, and anything a cadet is asked to run. This
  applies to the ADALM-PHASER labs in Modules 3-5, where vendor material is
  often MATLAB-first: translate it to Python (`pyadi-iio`) rather than adopt
  it. MATLAB sources may be read as reference; they are never a deliverable
  and are never assigned.
- **Don't hand-edit `book/_toc.yml`** — `scripts/scaffold_lessons.py` regenerates
  it wholesale from its `LESSONS` manifest. Edit the manifest and re-run.
- **Don't commit practice PDFs built with stand-in macros.** Reimplementing the
  house macros well enough to compile is easy and useful for syntax-checking the
  source without `latex-tools`; it is *not* good enough to ship. Measured: a stub
  build diverges from the real one by 2–4% of pixels, with the error accumulating
  into visibly different vertical placement down each page, so the set would not
  match its siblings in front of students. Real macros or no PDF.
- **Don't delete a lesson's reveal.js deck when it becomes a frame page.**
  Course decision (2026-08-29): the decks stay while the frame view is still
  being proven in front of real classes. A frame lesson and its deck are a
  parallel pair on purpose — `mech_check.sh` still requires the deck `.md` and
  `.html` for every lesson, and still render-checks it. Revisit only when Neil
  says the decks are no longer needed.
- **Don't switch the decks to Beamer.** reveal.js is a deliberate choice — the
  course is demo-heavy and the decks integrate with the interactive widgets.
- **Don't link a practice PDF that has not been built yet.** Add the Practice
  section to a lesson page only once the PDFs exist under `book/extras/practice/`.
- Don't delete the older rasters under `book/extras/slides/img/` or
  `book/extras/viz/img/` — some are still referenced by lesson pages.

## Note for Neil's own machine

The authoritative working tree on Neil's host is the OneDrive clone
(`.../USAFA/ece444`), **not** `~/src/ece444`. In a web session none of that
applies — the fresh clone you are in is the working tree, and only what you
commit and push survives the container.
