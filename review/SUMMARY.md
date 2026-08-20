# Module 1 Review — Summary

**Reviewed:** Module 1 (L01–L06) on `main` @ `2d299b2`, measured against `COURSE_SPEC.md` and Module 2 as built (`claude/module-2-antenna-radar-jhh1mq` @ `4bec70b`). Five independent Opus lens reviews (physics, pedagogy, consistency, problems, graphics) plus a mechanical pass; 111 raw findings adjudicated down to **3 blockers, 31 majors, 37 minors, 13 ideas** in `review/FINDINGS.md`. Read-only — no lesson file touched. One operational note first: **the spec and finished Module 2 are not on `main`** — merge that branch (or at least `COURSE_SPEC.md`) so Module 1's fixes are made against the real rubric.

## The verdict

Module 1's substance is sound. All 47 practice-set numeric answers recompute correctly; all 8 PDFs build clean against the real macros; the book builds with zero warnings; nearly every worked number on the pages checks out. What the review found is not rot — it is (a) two lessons short of the per-lesson bundle, (b) three places where **graded work outruns taught content**, (c) a handful of genuine physics misstatements, and (d) systematic form drift against the standard Module 2 set.

## Blockers

1. **The L05 deck is a 3-slide "Coming soon" scaffold** behind a live Slides link, on the module's most spatial lesson. (Known on your ToDo; three lenses independently ranked it the top gap. L05 also has no practice set — LO 1.5 gets zero written reps.)
2. **The L02 deck never reaches Friis/EIRP/FSPL**, though LO 1.2.6 and practice Q6 assess them — class time never touches what the homework grades.
3. **L06 Q6 is unanswerable from taught content**: the taper sidelobe numbers (−23/−26.5/−31.5 dB) and the taper-costs-beamwidth fact appear nowhere on the page or deck (only inside a widget), and the expected answer contradicts the lesson's own boxed rule of thumb.

## Physics fixes worth knowing about

- L03 (page **and** speaker note) claims AR ≤ 3 dB caps polarization loss at 3 dB — false, and contradicted by the lesson's own −1.8/−4.8 dB derivation later on the same page.
- L04/L02 present the Hertzian 80π²(ℓ/λ)² as the practical short dipole — the quoted 0.05λ ⇒ 2 Ω design number is 4× high (triangular current gives 20π², ≈0.49 Ω).
- L05 twice says a small antenna's far field begins at kr = 1 — the crossover, not the far field; off by an order of magnitude.
- The "Gain Comparison" figure self-normalizes all four patterns to 0 dB, so the 0→28 dBi difference it exists to show lives only in the legend (and its horn/dish have no sidelobes for the pattern-reading slide that follows).

## Structural themes

- **Assessment alignment:** the syllabus and module-page LO lists disagree while 30% of the grade is per-LO; reciprocity and the L-match are named LOs with no reps; L02's only pattern-reading practice is an ungradeable find-your-own-datasheet task; L03's set is ~40% over the workload calibration with zero answer boxes.
- **The M1/M2 seam:** four symbol renames (η_rad→η_cd, R_rad→R_r, η₀→η, upright→italic subscripts), section order, missing hooks/Summary tables, deck closers, and 8 of 14 widgets on ad-hoc control markup. All mechanical; all adjudicated toward Module 2. **No case surfaced where Module 1 was more correct than Module 2.**
- **Under-figured decks:** L04's deck has zero figures; L06 never plots a radiation pattern; L03's page has no static figures though the SVGs already exist; one CSS rule (`.reveal table` font size) fixes eleven overflowing table slides at once.

## Do these five first (best impact-to-effort)

1. Taper table + one sentence into L06 (~30 min) — unblocks a graded question.
2. Rewrite the AR ≤ 3 dB sentence, page + note (~15 min).
3. Add the `.reveal table` CSS rule (~10 min) — eleven slides.
4. Embed the orphaned `effective-area.html` widget in L02 (~20 min) — finished work, currently unreachable.
5. Symbol harmonization sweep (~1–2 h, mechanical) — removes the notation seam before students hit L07.

## Effort to reach Module 2's standard

**~7–9 focused days** total; **~5 days** if the widget-UI refactor and idea-tier items are deferred. The big rocks are the L05 deck (~1.5 d), graphics (~2 d), and the practice-set repairs (~1 d).

Nine additions to `COURSE_SPEC.md` are listed at the end of FINDINGS.md so the spec ends up capturing what Module 2 actually does (summary-table shape, figure naming, note coverage, ψ for tilt, canonical CP numbers, answer-box calibration, and the intro-lesson practice-set policy).
