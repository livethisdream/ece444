# Frame-view lessons — architecture

Status: **the format is the site's lesson format.** `book/module01/L05-field-regions/`
is the worked example — a real MyST page using the directives below, in the TOC,
on the site — and so are the landing page and all five module overviews. The
L05a experimental copy that proved the format is retired (2026-08-29): once L05
itself was converted the two were near-duplicates, and its extra beats were
ported into L05 before deletion. The generated prototype
that used to sit at `book/extras/frames/`, built by `scripts/build_frames.py`,
is gone: it was the *old* approach, it still carried the old bottom-right bar,
and the L05 page linked to it as "frame view", so a reader following that link
landed on a stale duplicate of the lesson rather than on L05a.

**Decks stay** (2026-08-29, Neil): converting a lesson to a frame page does not
retire its reveal.js deck. They are a parallel pair while the frame view is
proven in front of real classes, and `mech_check.sh` still requires and
render-checks the deck for every lesson. This is the "keep it until I'm sure I
don't need it" call, not a permanent answer.

The question this answers: if a lesson's deck and its page become one
scroll-frame document, where does the source live and what generates what?

## The decision

**A frame lesson stays an ordinary Sphinx page.** One MyST file per lesson, in
its existing location, marked `frame_view: true` in front matter. A local
extension supplies two directives and swaps the HTML template for that page.

Rejected: generating frame HTML with a script and committing it to
`book/extras/`, which is what the L05 prototype does. It works, but it leaves
the lesson outside Sphinx — no MathJax, no cross-references, no search index,
no prev/next — and it puts the lecture prose in Python string literals.

## What the spike proved

Each of these was verified against a real build, not assumed.

| Question | Answer |
| :-- | :-- |
| Can a local extension register MyST directives? | Yes. `sphinx: local_extensions: {frames: _ext}`, `colon_fence` is already on, so `:::{frame}` works. |
| Can the sidebar be dropped per page? | Yes. `html-page-context` returns a template name; the theme is bypassed for that page only. Verified: frame page `bd-sidebar` = 0, L05 unchanged at 2. |
| Does math still work? | Yes. Sphinx renders it and MathJax loads as usual — **no hand-set HTML fractions**. That whole class of work disappears. |
| Is the page still searchable? | Yes, indexed. Sphinx indexes the doctree regardless of template. The `extras/` approach is not indexed at all. |
| Can a chrome-free page still navigate? | **Yes, and this is the finding that settles it.** The template gets Sphinx's own `prev` / `next` context. The spike rendered "prev: L1 - Course Introduction / next: L2 - Basic Properties". Navigation comes from the TOC, free and always correct. |
| Do normal pages stay normal? | Yes. Opt-in by front matter; everything else builds as before. |

Navigation was the objection to replacement. It is answered: a frame lesson is
in `_toc.yml` like any other, so prev/next/module-index are available to the
HUD without inventing a second nav system.

## Source syntax

```markdown
---
frame_view: true
---

# L5 - Field Regions

:::{frame} The crossover is a single number
Radiation and induction are equal when

$$ kr = 1 \quad\Longrightarrow\quad r = \frac{\lambda}{2\pi} $$

:::{depth}
Read that carefully, because it is the single most misquoted number in the
subject. Inside $\lambda/2\pi$ the stored terms take over...
:::
:::
```

`depth` is the lesson-page material a deck would not carry. It is always in the
DOM; present mode hides it with CSS. Presenting can therefore never lose it.

## The present layer (2026-09-03)

Neil, after a term's worth of frames on screen: the site's format and its
single source are right, but the frames are too dense to talk to, and a lesson
has too many of them for one period. Measured the day he said it, on the
source: the median frame carried 55-93 words in present mode and the lessons
ran 28-76 frames. The conversion had wrapped the lesson prose in frames and
used `depth` sparingly, so the prose *was* the slide.

The fix inverts the default per frame rather than site-wide. `:::{present}`
marks what a frame shows on screen; a frame that carries one shows only its
present blocks and its title, and `_ext/frames.py` wraps everything else in
that frame into `depth` at build time, in document order. A frame with no
present block behaves as before, so a lesson can be re-cut one frame at a
time without blanking the other twenty-seven.

```markdown
::::{frame} Radiating near-field (Fresnel region)
:::{present}
A little farther out, energy leaves the antenna, **but the shape of the
pattern still depends on how far away you are.**
:::

Different parts of the antenna are at meaningfully different distances from
your observation point, so their contributions add up with distance-dependent
phase ...                       <- becomes depth; "More detail +" in class
::::
```

Three rules that came with it:

* **Two present blocks in a row share a stage.** In present mode they sit
  side by side (`grid`, `auto-fit`, 21rem floor via `min()`), which is Neil's
  brief in one line: key points beside the graphic or the widget, to be
  talked to. On a phone they stack. In read mode neither wrapper has a box.
* **`:class: read-only` on a frame** removes it from present mode and from
  the counter and contents overlay in both modes. That is how the beat count
  comes down without deleting a derivation from the page. Leave a blank line
  after the option or MyST reads the next line as YAML and the build errors.
* **Budgets, and a static check.** 40 words a present frame, 30 present
  frames a lesson. `scripts/verify/check_density.py` counts from the markdown
  (display math is not words, inline math is one word, the LO frame is
  exempt) and `mech_check.sh` gates on it once a lesson has opted in.

The writing discipline is what makes read mode survive it: the present block
is the frame's topic sentence or its figure, and the prose after it continues
that sentence. Where the L05 pilot restated the sentence in the paragraph, the
paragraph was trimmed, not the sentence. **L05 is the worked example**: 30
frames became 24 beats, 19 of them cut, none over 40 words.

What it does not do, yet: the reveal.js deck is still a parallel copy. Once
every lesson carries a present layer, the deck could be generated from it
(present blocks as slides, the rest as speaker notes) and the "decks are the
source of truth for nomenclature" rule would retire with the second copy.
That waits on the decision to keep the decks.

## Ten constraints, each of which cost a failed build

docutils/Sphinx facts, not preferences.

1. **A frame title must be a directive argument, not a heading.** docutils
   demotes a header nested in a container to a rubric
   (`myst.nested_header` warning), and a `title` node whose parent is not a
   `section` trips an assertion in the HTML writer. So `:::{frame} Title`, and
   the extension emits a `rubric`. This is also the truer model: the title
   names the frame rather than opening a subsection.
2. **`templates_path` must be appended, not declared.** Setting it in
   `_config.yml` replaces the one jupyter-book assembles, and the build dies
   inside `pydata_sphinx_theme` looking for `toggle-primary-sidebar.html`.
3. **Append it on `config-inited`, not `builder-inited`.** The builder
   constructs its Jinja loader from `templates_path` during init, so
   `builder-inited` is already too late — `TemplateNotFound: frame.html`.
4. **A frame holding a `depth` or `callout` needs a longer fence.** MyST
   requires the outer fence to out-length the inner, so frames open `::::` and
   nested blocks `:::`. Get it wrong and the frame silently swallows its
   siblings — 25 frames parsed as 11, with no warning.
5. **Do not emit `script_files` wholesale.** It drags the theme's JS onto a page
   with no theme DOM and it throws on every selector it owns. Filter to
   MathJax. And use `js_tag(js)`, not `pathto(js, 1)` — the latter renders
   `None` and requests `/None`.
6. **Scope `display: contents` carefully.** A blanket rule on
   `.docutils.container` also hits `.depth` and `.callout`, which then have no
   box, so read mode shows nothing. `:not(.depth):not(.callout)`.
7. **jupyter-book auto-links every file in `_static` onto every page.** So
   `frames.css` -- which carries bare `body`, `h1`, `p`, `table` and `:root`
   rules -- silently restyled the whole book. Nothing errors; the theme pages
   just quietly stop looking like themselves. `_ext/frames.py` strips
   `frames.css`/`frames.js` from `css_files` and `script_files` on every
   non-frame page, `search.html` and `genindex.html` included -- those two
   arrive with `doctree is None`, so an early return skips them.
8. **`[hidden]` loses to a class that sets `display`.** The attribute's
   `display: none` comes from the UA stylesheet, so `.hud .pop { display:
   flex }` beats it and a panel meant to be shut is permanently open. Any
   component toggled by the `hidden` property needs an explicit
   `.thing[hidden] { display: none; }`.
9. **A component's own button rule outranks a single-class override.** `.hud
   button` and `.index button` are (0,1,1); `.index-close` is (0,1,0) and lost,
   so the close button inherited `width: 100%` and spanned the viewport with
   its glyph in the corner. Anything styling a button inside those components
   needs the type selector too -- `.index button.index-close`, `.hud .pop
   button`.
10. **`min-width: auto` is what breaks a frame on a phone.** A flex or grid
   item's automatic minimum is its min-content width, and display math and
   tables do not wrap. The `overflow-x: auto` further down never fires,
   because the box has already grown to fit. Measured at 390px: four L05a
   frames ran 354-482px wide and the deck panned sideways. `.wrap` and the
   jump overlay's columns need an explicit `min-width: 0`, and an
   `auto-fill` track floor needs `minmax(min(19rem, 100%), 1fr)`.

## What is still open

**Frame budgets.** A slide that overflows is a deck bug today, caught by
`check_deck.py`. A frame that overflows is the same bug. The check has to be
rewritten against the new output — and unlike a deck, a frame page has two
modes, so "does it fit" only applies to present mode.

**Does every frame stand alone with its depth hidden?** The L05 pass suggests
yes where the deck line is the section's topic sentence, which is how the pages
were already written. It reads thin on the two widget frames, whose deck line is
a pure visual cue. Those need a real claim written for them.

**Print / PDF.** `?print-pdf` on a reveal deck produces handouts today. A
scroll-snap page has no equivalent. Whether that matters depends on whether
anyone uses it.

**The migration itself.** 41 lessons. Module 1 is written and would have to be
converted; Modules 2–5 are mostly shells and would be authored this way from
the start, which is the argument for deciding soon rather than later.

## What replacement would retire

- `scripts/make_deck_html.py`, `deck-tools.js`, the vendored chalkboard, and
  every `book/extras/slides/*.html` wrapper.
- The whole `marked`-mangles-LaTeX gotcha class in `CLAUDE.md`, because there
  is no second markdown parser. Sphinx renders the math once.
- `scripts/verify/check_separators.py` and the dead-separator failure mode with
  it — there are no separators.
- The deck/page reconciliation problem: "the decks are the source of truth for
  nomenclature" stops being a rule anyone has to follow, because there is one
  document.

And it would lose chalkboard annotation and second-screen speaker notes. Neil
does not use either; the laser pointer and spotlight in the prototype cover what
he does use.

## Two findings worth acting on regardless

- **Committed SVGs can be made theme-aware with no generator changes.** CSS
  attribute selectors beat SVG presentation attributes, so
  `[fill="#5a5a5a"] { fill: var(--fig-line); }` retargets the house palette in
  all 24 figures. Twelve rules cover every colour in use.
- **`mjlabel.js` fetches MathJax from a CDN.** Where that is blocked — the
  course containers included — `MJ.draw` returns 0 *and* the widgets' first
  paint never fires, because they kick it from `MJ.onReady`. A canvas can sit
  blank. This is the state `check_widget.py` has been testing them in. The
  prototype carries a 40-line no-network shim that fixes it.
