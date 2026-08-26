# Frame-view lessons — architecture

Status: **one lesson built this way.** `book/module01/L05a-field-regions-frames/`
is a real MyST page using the directives below, in the TOC, on the site. The
generated prototype at `book/extras/frames/` is the *old* approach, kept only
for comparison until L05a has been taught from.

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

## Six constraints, each of which cost a failed build

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
