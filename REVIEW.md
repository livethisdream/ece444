# Module 2 REVIEW rubric

Every lesson (L07-L14) is judged artifact by artifact. Mechanical checks are
scripted; substance checks are adjudicated by the orchestrator by sampling.
Two revision rounds per lesson max, then escalate to Neil.

## A. Mechanical (scripted; all must pass)

Per lesson NN/slug:

1. Files exist: `book/module02/L<NN>-<slug>/index.md` (non-stub),
   `book/extras/slides/<slug>.md`, `<slug>.html`,
   `latex/ECE444_Practice_L<NN>.tex`,
   `book/extras/practice/ECE444_L<NN>_Practice_{blank,SOLUTIONS}.pdf`,
   widget under `book/extras/viz/`.
2. Practice compiles: `build_practice.sh <NN>` exit 0 both copies; no LaTeX
   errors; no `Overfull` > 10pt in logs; SOLUTIONS pagecount >= blank pagecount;
   every `\part` inside a `\begin{parts}` has a `\begin{solution}`.
3. Deck renders: `check_deck.py <slug>` PASS (fits 700px, no raw `$$`, no
   literal `\_`, no missing resources, slide count in 14-27).
4. Widget renders: `check_widget.py` PASS (no console errors, canvas paints,
   controls respond); lesson-page iframe height within +-40px of measured.
5. Greps: no U+2009 anywhere; no `\,`/`\;` inside `$...$` in deck md; no
   `$|...|$` in markdown table rows; LO block uses
   `lo-list lo-sublist` with `--module: '2'` and correct `--lo`/offset;
   practice banner says the right `LO 2.X`.
6. Site build: one central `jupyter-book build book/ --all` — no new warnings
   vs baseline; every module02 page emits HTML; iframes/links resolve to
   files that exist.
7. Practice links present on lesson page ONLY if both PDFs are committed.

## B. Substance (orchestrator; sample >= 2 questions + 1 derivation + the
   widget per lesson, full read where a report flags anything)

1. **Physics**: canonical numbers match COURSE_SPEC §7 wherever they appear;
   spot-recompute 2 numeric practice answers per set; dimensional consistency
   in worked examples; no radar-range-equation derivation (preview only).
2. **Derivations**: steps follow at undergrad level; approximations named
   when invoked; no graduate detours (no full cavity Green's functions, no
   GTD, no spherical-mode NF-FF math — describe, don't derive).
3. **Widget honesty**: manipulate it; readouts must match theory at 2+ spot
   points (e.g. dipole D=2.15 dBi at L=lambda/2; SLL -13.3 dB uniform).
   The graphic must expose the one concept its caption claims — if the
   caption can't say "notice X happening as you drag Y", fail it.
4. **Difficulty**: practice set comparable to the L06 exemplar — 4-6
   questions, 45-60 min strong-student time, >= 1 "why in words" part,
   >= 1 rule-of-thumb tie-in, plausible engineering numbers.
5. **Deck**: one idea per slide; callouts carry the takeaway; speaker notes
   on demo slides; no equations inside figures; consistent nomenclature with
   lesson page (deck wins on conflicts).
6. **Continuity**: opening hook references the actual previous lesson;
   "Where this is going" points to the actual next one; L07/L09 sub-LO
   numbering doesn't collide (L09 starts at 2.1.5); lab pages (L08, L13,
   L14) carry Background -> Equipment/Setup -> Procedure -> Deliverables.

## C. Assessment (final deliverable; faculty repo)

- `ECE444_Assessment_M02.tex` compiles under the M01 assessment harness
  pattern; every 2.x LO (2.1-2.7) has >= 1 question tagged to it; solutions
  complete; same key-switch build as practice sets; NOT committed to the
  public repo (gitignored path or faculty repo only).

## Verdict table

Maintained by the orchestrator in the final report: lesson x {page, deck,
practice, PDFs, widget} -> pass/fail(round) + open questions.
