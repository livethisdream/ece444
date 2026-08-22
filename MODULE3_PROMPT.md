# Seed prompt — Module 3

Copy everything below the line into a new Claude Code session on this repo.

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

## The tooling: Neil's Phaser GUI (this is the lab platform)

**`https://github.com/livethisdream/phaser` — attach it with `add_repo` and
clone it before authoring any lab lesson.** Neil built this, it is the
software the labs run on, and it replaces ADI's own tooling. It is Python and
vanilla JS, consistent with the no-MATLAB rule.

What it is: a headless Python backend (`phaser_headless.py`) that runs on the
Raspberry Pi shipped with the Phaser kit, driving the ADAR1000 beamformer, an
ADI Pluto for IQ, and an ADF4159 LO through `pyadi-iio`. A browser UI
(vanilla JS + Plotly) connects over WebSocket from any machine on the network.
A second frontend serves a CW Doppler radar app — that one is Module 4's.

**Module 4 is not ready to author.** Neil is still building the radar GUI, so
the FMCW work in Modules 4-5 has no finished platform yet. Module 3 is
unaffected; do not scope Module 4 lessons against the current radar frontend
without asking.

Three things about it shape how Module 3 should be written:

1. **Simulation mode means you can actually run the labs.** `python
   phaser_headless.py --sim` brings up the whole UI against physics-based
   stubs — beam sweeps, per-element phase, taper presets, Beam Steering,
   Manual and MVDR digital beamforming — synthesizing element-level IQ from
   an HB100 target so beamwidths, sidelobe roll-off, grating lobes on sparse
   tapers, and MVDR nulls all come out physically consistent. **Use it.** Do
   not write a lab procedure you have not executed. Verify the numbers a
   student will read against theory, the way Module 2 verified every widget.
   (CW Doppler radar is not simulated.)
2. **The GUI already has lab presets**, selected by lab index, aligned to
   `docs/2025_Phaser_labs_Python.pdf` in that repo. **Neil built the GUI to
   follow those labs exactly**, so that document defines the lab sequence —
   Module 3's lab lessons follow it rather than inventing a parallel
   procedure. Read the PDF before writing any lab.
3. **Instructor mode** (`?instructor=1`, sim only) exposes a configurable
   interferer for MVDR nulling demos, hidden from students. That is the
   natural vehicle for objective 3.9 and for the Module 5 jammer capstone.

Feature-to-objective mapping, to check rather than assume: beam sweep and
per-element phase serve 3.4 and 3.5; taper presets serve 3.7; grating lobes on
sparse tapers serve 3.8; MVDR and the interferer serve 3.9; comparing the
array factor against a measured sweep serves 3.6.

**Check whether `docs/2025_Phaser_labs_Python.pdf` is in the clone.** It is
the canonical workshop lab document, and `.gitignore` excluded `docs/*.pdf`
as of the Module 2 session; Neil intended to un-ignore it (the repo is
private, so the PDF is internal use, not redistribution). If it is still
missing, ask him for it rather than reconstructing the labs from the GUI's
preset code.

**Clone note:** the repo's default branch is `browser-based`, not `main`.

## Background reading on the hardware

ADI's own material describes the CN0566 hardware. It is background, not the
lab source — the labs use Neil's GUI.

- https://analogdevicesinc.github.io/documentation/solutions/platforms/phaser/index.html#adc-adalm-phaser
- Circuit note (hardware detail) — https://www.analog.com/media/en/reference-design-documentation/reference-designs/cn0566.pdf
- Older wiki page — https://wiki.analog.com/resources/eval/user-guides/circuits-from-the-lab/cn0566

**Both ADI hosts were blocked by the container egress proxy during Module 2**,
so this material may be unreadable from inside a container. The Phaser repo
itself clones fine, and its README carries the architecture you actually need.
Do not invent register names, `pyadi-iio` call signatures, IF frequencies, or
lab procedures: read them from Neil's repo, or ask.

The PHASER is the hardware for Modules 3 and 4; L17, L19, L21, L23, L25, and
L28 are the hands-on lab lessons.

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
