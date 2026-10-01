---
name: why-sweep
description: Audit one lesson (page, deck, practice set) for results stated without saying where they come from, rank the gaps, stop for Neil's pick, then fix the approved ones. Manual only -- run as /why-sweep <NN>.
argument-hint: <lesson number, e.g. 15>
disable-model-invocation: true
---

# "Why" sweep for one lesson

Run on demand, one lesson at a time: `/why-sweep 15`. The lesson is
`$ARGUMENTS`. L12 is the model for the finished shape; L13 and L14 were done
the same way (their "why" commits show the pattern).

The sweep has two phases with a hard stop between them. **Do not edit anything
in phase 1.**

## Phase 0: start clean

```sh
git fetch origin main && git checkout -B <your branch> origin/main
```

Read `project/ECE444_PROJECT.md` Status for anything recent on this lesson.

## Phase 1: audit, then stop

Read the lesson page (`book/module*/L<NN>-*/index.md`), its deck
(`book/extras/slides/L<NN>-*.md`), and the practice source
(`latex/ECE444_Practice_L<NN>.tex`) in full. List the gaps, ranked by student
impact. Look for:

- **A result with no mechanism.** L12's examples: "the current reverses around
  the loop", "2kh cos θ", "m = IA". L14's: G = η4πA/λ², the 10 dB rule, the
  70°·λ/D coefficient, "a long element lags".
- **Jargon the course never defines.** L12's "sky noise" became external noise
  defined through T_A. Before calling a term undefined, grep the earlier lessons
  for it; if it is defined there, the gap is the missing link, not the term.
- **Numbers nobody has recomputed.** Recompute every number in the lesson in
  Python now, in phase 1, and report the wrong ones as gaps. Past finds: 0.01λ
  that should have been 0.15λ, 20 dB that should have been 23, a link "13 dB
  under the noise" that was 6, a "+3 dB per doubling" rule that the lesson's
  own table put at 1.8.
- **Contradictions inside the lesson.** L14 quoted −17.6 dB for a uniform
  circular aperture in one frame and −13.3 dB (the line source) two frames later.
- **Links to earlier lessons that should be explicit**: L02's directivity, A_e,
  and pencil-beam rule; L05's field regions and 2D²/λ; L06's radiation vector
  N = ∫J e^{+jk r̂·r′} dV′; L07's dipole impedance; L12's T_A; L13's η_ap ratio.
  Use `grep -n` on those pages to confirm the notation before proposing.

Report as a table: rank, gap, one-line proposed fix, figure needed (yes / no /
optional). List the numbers you confirmed are right in one line. Recommend a
batching. **Then stop and wait for Neil to pick.**

## Phase 2: fix what Neil approved

One PR per approved batch.

**Content rules**

- The derivation goes in read mode: prose outside the present blocks (the
  extension wraps it into depth), or a `:::{depth}` block.
- Present blocks stay at 40 words or fewer. Move at most one short chain onto
  the slide.
- Use the notation of the lesson being linked to, and name that lesson.
- Run derivations general to specific as one chain aligned on `=`. Every
  non-trivial equation gets its own display line. Split a long equation onto
  aligned lines so it fits a 390px phone.
- Recompute every number in Python before it goes in. Correct an old number
  that turns out wrong, and say so in the commit message.
- Follow `VOICE.md` in the new prose.

**Figures**

If a figure earns its place, write a generator in `scripts/graphics/` that
writes to both `book/extras/viz/img/` and `book/extras/slides/fig/` and calls
`apply_font_stack()` (`scripts/graphics/l14_taper_spillover.py` is a short
model). Place labels from the data, not at fixed offsets. Screenshot it with
chromium (`executable_path="/opt/pw-browsers/chromium"`) and fix every label
collision before using it. The deck copy carries no equations.

**Deck**

Mirror every change in the deck, as a new slide or a speaker note, and follow
the marked gotchas in `CLAUDE.md`: no `\,` or `\;`, `}\_{` in markdown regions,
no `$$` continuation line starting with `+`, `-`, or `*`, and a blank line
above and below every `---`. Notes are plain text; write math there in words.

**Practice set**

Keep it at its sibling page count. A new solution line can push a question
onto its own page in the SOLUTIONS PDF even when the blank stays the same; if
it does, trim the new text.

## Pitfalls already paid for

- Edit through Python only with raw strings (`r"""..."""`). A non-raw string
  turned `\t` and `\a` into control characters and shipped two corrupted
  equations. Before committing:
  `grep -nP '[\x07\x08\x0c]' <changed files>`, plus `grep -nP '[^\t]\t'` on
  the `.tex` (leading tabs are its indentation; any other tab is a bug).
- `mech_check.sh` rebuilds the practice PDFs. If the `.tex` did not change,
  restore them with `git checkout -- book/extras/practice/` rather than
  committing timestamp-only diffs.
- Build practice PDFs only with lualatex and the real `latex-tools` macros.
  Attach `livethisdream/latex-tools`, clone it to `/workspace/latex-tools`, then
  `TEXINPUTS=/workspace/latex-tools/tex/latex//: bash latex/build_practice.sh <NN>`.
  Check `pdfinfo` reports LuaTeX as the producer.
- An older present equation can already overflow at 390px. The overflow check
  below catches it; fix it in the same PR.

## Verify before pushing

```sh
jupyter-book build book/ --all                     # 0 warnings
TEXINPUTS=/workspace/latex-tools/tex/latex//: \
  scripts/verify/mech_check.sh <NN> <slug>         # 0 failures
scripts/verify/check_density.py L<NN>              # none over 40 words
scripts/verify/check_frames.py L<NN>               # every frame fits
scripts/verify/check_deck.py L<NN>-<slug>
scripts/verify/check_page.py module0M/L<NN>-<slug>/index.html
scripts/verify/check_separators.py L<NN>-<slug>
scripts/verify/check_parity.py <baseline>          # lists only this lesson
```

Then two Playwright checks against the built page (serve `book/_build/html`
with `scripts/verify/_common.serve` and route CDNs with `make_cdn_router`):

- At 390 and 1000px, no `mjx-container[display]` has
  `scrollWidth > clientWidth` or a right edge past the viewport.
- Set `data-mode="present"` on `<html>` and screenshot every changed frame
  (`#frame-<slug>`) at both widths. Look at each one.

## Finish

Commit with a message that lists the derivations added and every number
corrected. Add **one short Status line** to `project/ECE444_PROJECT.md`.
Push, open the PR, and watch it to green.
