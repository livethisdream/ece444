# Seed prompt — Module 3

Copy everything below the line into a new Claude Code session on this repo.
Fill in the one bracketed slot first.

---

You're orchestrating additions to this antenna & radar course: **Module 3,
Lessons 15–28 (Arrays and ADALM-PHASER Beamforming)**. This is an
undergraduate course — keep the depth appropriate for undergraduates.

Modules 1 and 2 are complete. Module 3's lesson skeletons are in place. Work
on a branch named for Module 3.

## Read these first, before anything else

Three contract documents at the repo root, written during the Module 2 build.
They encode decisions already made — follow them rather than re-deriving them:

- **`COURSE_SPEC.md`** — file layout, section order, notation, LaTeX macros,
  deck rules and their parser gotchas, widget conventions, practice-set
  format, difficulty calibration, self-checks. It is the authoring contract.
- **`VOICE.md`** — the course's prose voice, captured as before/after pairs
  from my own review corrections. Read it before writing any prose. It also
  records what *not* to flatten.
- **`REVIEW.md`** — the review rubric: which checks are mechanical and which
  need judgement.

Also read `project/ECE444_PROJECT.md` for running status and decisions, and
update its Status/ToDo sections when you finish. It is shared across
concurrent sessions, so keep edits small.

## Source material for the second half of the course

[PASTE THE LINK FROM YOUR module3.md HERE — the CN0566 / ADALM-PHASER lab and
slide material. Also say whether you want Module 3 built *from* that material
or merely consistent with it, and whether any of it can be reused directly
versus rewritten in course voice.]

The ADALM-PHASER (CN0566) is the hardware for Modules 3 and 4. Lessons 17, 19,
21, 23, 25, and 28 are hands-on lab lessons on it. Before authoring those,
confirm what the source material actually specifies — do not invent hardware
details, register names, pyadi-iio call signatures, or lab procedures. Where
the source is silent, say so and ask.

## Scope

Module 3 objectives, from the syllabus:

- 3.1 aperture distributions and aperture efficiency
- 3.2 array factor for an arbitrary linear array; pattern multiplication
- 3.3 ADALM-PHASER hardware architecture and SDR control
- 3.4 phase weights for beam steering; predicting the steered pattern
- 3.5 implementing beam steering on the PHASER, verified against theory
- 3.6 array factor versus true antenna pattern; element-pattern effects
- 3.7 amplitude tapering (uniform, cosine, Chebyshev, Taylor) and the
  sidelobe/beamwidth trade
- 3.8 beam squint and quantization effects
- 3.9 null-steering weights, implemented on the PHASER

The midterm project (Antenna Pattern Measurement, introduced at L11) is **due
at L20** — that lesson should acknowledge it.

## Done means

For each lesson: lesson page, slide deck, practice problems with solutions in
LaTeX (one source, key switch, compiles cleanly), and at least one interactive
graphic — all consistent with each other and indistinguishable in form from
Modules 1 and 2. The final deliverable is an assessment covering every 3.x
objective, in LaTeX with solutions, built the same way as the practice sets.

## How to work

You orchestrate; you don't author. Spawn one lesson-author subagent (Opus) per
lesson, in parallel where lessons don't depend on each other. Each brief
contains: lesson number, title, learning objectives, concepts to cover, which
graphic(s), and "follow COURSE_SPEC.md and VOICE.md." Nothing more — agents
must not read other modules' lessons; the spec is their only context.

Each agent returns ≤20 lines: paths written, self-check results, assumptions,
ambiguities. Never lesson content. Keep your own context lean — work from the
spec, paths, and agent reports; read artifacts only where a report flags
something or where you're sampling.

Push mechanical checks down to bash or a cheap subagent: compiles, files
present, macros defined, refs resolve, every problem has a solution, answers
match. There is a read-only `reviewer` agent type for single-lens sweeps
(`.claude/agents/reviewer.md`) — it was useful for catching prose problems
across many files at once.

You adjudicate substance: physics correctness, dimensional consistency,
derivation steps, whether each graphic exposes the concept it claims, whether
difficulty matches prior modules. **Verify claims yourself rather than
trusting agent reports** — during Module 2, agents reported numbers that were
stale, overstated, or measured wrong, and independent re-measurement caught
each one. Sample rather than read everything.

Send fixes back to the authoring agent as specific instructions; don't rewrite
it yourself unless it's a one-liner. Two revision rounds max, then escalate.

## Things Module 2 got wrong — don't repeat them

**Put my verbal instructions into `COURSE_SPEC.md` immediately.** Twice, a
subagent correctly followed the written spec and undid something I had asked
for in conversation (a derivation was collapsed to meet a slide-count limit I
had verbally waived). If I ask for something that contradicts the spec, amend
the spec in the same turn.

**Derivations are shown, not asserted.** I asked for the current distribution,
the pattern, and the input impedance to all be derived in L07 so students
watch the machinery work. Expect the same in Module 3: the array factor, the
steering phase, and the taper trade should be derived, not quoted. Decks carry
the derivation one step per slide, with speaker notes that support deriving it
live.

**Prose.** Complete sentences. No fragments used for punch, no text vouching
for its own honesty or rigor, no cheeky asides, no scolding the reader. This
took 301 rewrites to fix across Module 2 because the spec originally
prescribed "occasionally wry." `VOICE.md` now carries the calibration set.

**Widgets.**
- Minimal words inside the graphic; explanation belongs in the surrounding
  text. A legend is a color key, not a paragraph.
- Readouts laid out symmetrically on a grid, equal cells, tabular numerals —
  short labels with any comparison in the value field, never a label so long
  it collides.
- Size the canvas bitmap from `clientWidth` with `box-sizing: border-box`; do
  not clamp with `Math.max(380, …)`. Verify the drawn aspect is undistorted at
  1280 / 790 / 688 / 430 / 390 / 320.
- Measure heights at the **real serving widths**: the article column is
  688 px at a 1280 viewport and caps at 790 px. Never measure at 900. Height
  is not monotonic in width. `scratchpad`-style harnesses from Module 2 sweep
  correctly; `_static/viz-autosize.js` already sizes frames at runtime, so the
  `height=` attribute is only the no-JS fallback.
- I review on a phone. Zero horizontal overflow at 320 px is a requirement,
  not a nicety.

**Verification.** Decks and pages must be render-verified, not read. The CDNs
are blocked in these containers, so vendor reveal.js and MathJax from npm and
reroute requests to them. A page that builds is not a page that renders.

**Commits.** Small commits per unit of work, pushed as you go. Never leave the
branch dirty at the end of a turn.

## Environment

- Practice and assessment PDFs need the private `livethisdream/latex-tools`
  repo for the house macros — attach it in-session, clone it, then
  `TEXINPUTS=/workspace/latex-tools/tex/latex//: bash latex/build_practice.sh <NN>`.
- Assessments are **exam material** and never go in the public repo. They live
  in `livethisdream/ece444-faculty` — attach it and push to a branch there.
  Module 2's assessment is on `claude/module-2-assessment`; match its harness.
- Always `jupyter-book build book/ --all`. An incremental build silently skips
  changes under `book/extras/**`.

## Preview

Build me a private preview as claude.ai Artifacts, as was done for Module 2:
one self-contained page per lesson laid out exactly like the real lesson page
(title, the three slide pill links, learning objectives, then content with the
widget inline — no invented chrome), plus one standalone deck page per lesson
opened from the "html slides" pill, plus a hub page linking everything. Every
page must be fully self-contained: no network requests at all, everything
inlined, verified in all three theme states and at 1280 / 390 / 320.

## Report back

A lesson × artifact table with pass/fail and open questions.
