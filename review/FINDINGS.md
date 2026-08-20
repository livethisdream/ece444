# Module 1 Review — Findings

> **Disposition (2026-08-20):** executed on `main` per Neil's decisions.
> Exceptions: F-11 rejected (no change); F-13 boxes only, nothing cut;
> F-14/F-27/F-54 deferred to the project ToDo; F-17/F-18 done minimally as
> directed; F-22 REVERSED — η_rad kept course-wide with `\text{}` subscripts
> (spec updated; M2 branch needs the sweep at merge); F-24 done excluding
> polarization-playground; F-67 skipped; F-70 moot (TikZ sources exist under
> `scripts/circuits/`); F-82 skipped. Everything else applied. All six decks
> render-verified offline (zero raw $$, zero overtall slides); all 12
> practice PDFs rebuilt with real macros, zero errors/overfull.

**Subject:** Module 1 (L01–L06) as of `main` @ `2d299b2` (lesson pages, decks, figures, widgets, practice sets L02/L03/L04/L06).
**Standard:** `COURSE_SPEC.md` as the written rubric, with **Module 2 as built** (`claude/module-2-antenna-radar-jhh1mq` @ `4bec70b`) authoritative where the spec is silent. Note: the spec and finished Module 2 are **not on `main`** — they exist only on that unmerged branch.
**Method:** Five independent single-lens reviewers (physics/math, pedagogy, consistency-vs-M2, problems/solutions, graphics/decks), each Opus in a read-only isolated worktree, capped at 25 ranked findings; a separate mechanical pass (LaTeX compile with real `latex-tools` macros, full `jupyter-book build --all`, path/orphan/grep checks). 111 raw findings were deduplicated and adjudicated to the list below; every blocker was verified at its exact location before inclusion. No lesson file was modified. The graphics lens could not read the spec file from its sandbox and calibrated against the M2 figure/widget inventory instead.

## What checked out clean (verified mechanically)

- All 8 practice PDFs (L02/L03/L04/L06 × blank/SOLUTIONS) compile with the real house macros: zero errors, zero undefined references; committed PDFs match rebuilt page counts.
- **All 47 numeric answers across the four practice sets were independently recomputed and are arithmetically correct**; blank↔SOLUTIONS answer boxes match.
- `jupyter-book build book/ --all`: exit 0, zero warnings.
- No orphaned figures in `slides/fig/` or `viz/img/`; no thin spaces (U+2009) anywhere; no broken lesson-page asset links.
- Every worked number on the L02/L03/L05/L06 lesson pages recomputes correctly except where flagged below.

---

## Blockers (3)

**F-01 · L05 deck is a 3-slide scaffold behind a live "Slides" link**
`book/extras/slides/L05-field-regions.md` (whole file, 633 bytes: title / one LO / "Coming soon")
The L05 lesson page is fully written — the module's densest derivation (three r-power terms, complex Poynting, 2D²/λ) — and links this deck as "html slides." The one class period covering LO 1.5 has no teaching artifact, and field regions is the most spatial concept in Module 1.
**Fix:** Author the deck to spec §3 (18–26 slides) from the page's existing spine: three regions → 1/r, 1/r², 1/r³ crossover at kr=1 → boundaries table → worked 1.2 m dish → why ranges are long. Minimum figures: concentric-region diagram, term-crossover plot, aperture phase-error construction. *(PED-01, CON-01, GFX-01 — flagged independently by three lenses; already on the project ToDo, confirmed as the module's top gap.)*

**F-02 · L02 deck never reaches Friis/EIRP/FSPL, but LO 1.2.6 and practice Q6 assess them**
`book/extras/slides/L02-antenna-properties.md` (deck ends before Friis; verified — its only mention is a forward pointer on the closing slide, line 508)
The lesson page teaches the link budget and Q6 grades it, but class time never gets there. The decks are the declared source of truth, so the gap is invisible to the instructor mid-lecture.
**Fix:** Add 3 slides after effective aperture: Friis assembly (S_inc → A_e), the three read-offs (EIRP, FSPL, dB addition), and the 2.4 GHz / 600 km worked example as a Quantity|Work|Result table. A link-geometry figure (Tx, R, spreading sphere, A_e capture disk) would serve both deck and page. *(PED-02, GFX-14.)*

**F-03 · L06 practice Q6 rests on facts the lesson text never states**
`latex/ECE444_Practice_L06.tex:279–311` (Q6 a–b) vs `book/module01/L06-radiation-integrals/index.md` Part 5
(a) asks students to match −23 / −26.5 / −31.5 dB to cosine, triangular, cosine² tapers; verified: those numbers appear nowhere on the page or deck (only −13.3 dB uniform). They are *demonstrable* in the `line-source-pattern` widget, but a graded key cannot rest on unprompted widget exploration. (b) expects "taper broadens the beam," while the lesson's boxed rule says only "beamwidth is bought with size; sidelobes with taper" — students reasoning from the taught rule will answer wrong.
**Fix:** Add the four-taper table (spec §7 already carries the canonical numbers) plus one sentence on the beamwidth cost (~1.2–1.45× uniform) to L06 Part 5 and the deck's Fourier slide; cite the table in the Q6 stem. *(PRB-01, PED-10, PRB-05 — two lenses independently.)*

---

## Majors — physics correctness (5)

**F-04 · Axial-ratio ≤ 3 dB misstatement, contradicting the lesson's own later derivation**
`book/module01/L03-polarization-bandwidth/index.md:99` ("no single linear receiver can miss more than 3 dB of power", verified) and `book/extras/slides/L03-polarization-bandwidth.md` "Axial ratio" speaker note ("caps polarization loss to any linear receiver at 3 dB regardless of alignment").
False — 3 dB is the peak-to-null *swing*; the lesson's own "Misquote 2" section correctly computes −1.8 to −4.8 dB. Students carry the wrong link-budget number from the first statement they read, and the instructor says it aloud.
**Fix:** Rewrite both as "received power swings over a 3 dB range with orientation (−1.8 to −4.8 dB against a linear antenna)" and forward-reference the Misquote 2 derivation. *(PHY-01, PHY-02.)*

**F-05 · Short-dipole radiation resistance quoted 4× high**
`book/module01/L04-impedance-feeding-baluns/index.md:73` and `book/module01/L02-antenna-properties/index.md:466` (verified)
R_rad = 80π²(ℓ/λ)² with ℓ_e = ℓ is the *infinitesimal/uniform-current* value, presented as "a short dipole … carrying a (roughly uniform) current." A real center-fed short dipole has triangular current: ℓ_e = ℓ/2, R_rad = 20π²(ℓ/λ)². The quoted "0.05λ ⇒ ≈2 Ω" is really ≈0.49 Ω, and Module 2 builds real short dipoles on this.
**Fix:** Name the 80π² case *infinitesimal (Hertzian)*, add one line with 20π²(ℓ/λ)² for the practical triangular-current dipole, requote the 0.05λ number. *(PHY-03.)*

**F-06 · L05 says a small antenna's far field begins at kr = 1 — off by an order of magnitude**
`book/module01/L05-field-regions/index.md:124` ("outside it, only the 1/r radiation term survives"), `:197` ("the far field begins there"), plus the term table's "wins where kr∼1" row (all verified/quoted).
At kr = 1 the three terms are *equal*, not negligible; reactive terms fall below ~10% only near kr ≈ 10 (r ≈ 1.6λ). As written it justifies bad measurement distances (far field at 0.16λ).
**Fix:** Call kr = 1 the *crossover*; state reactive terms are negligible only for kr ≫ 1 and quote a working figure (r ≳ λ) for where a small antenna's far field actually begins; fix the table row ("comparable near kr∼1"). *(PHY-04, PHY-11.)*

**F-07 · Friis and A_e = λ²G/4π boxed with no validity conditions**
`book/module01/L02-antenna-properties/index.md` — the boxed Friis result and the boxed A_e relation (also the "conjugate-matched load R_L = R_r" step, which silently assumes reactance tuned out, zero loss, polarization aligned).
Friis is the most-used equation in the course; applied bare it silently overpredicts by exactly the PLF and mismatch terms L3 and L4 spend pages on.
**Fix:** One bulleted "valid when…" line under each box (far field both ends, polarization matched, conjugate matched or use realized gain, free space); one-line assumptions note before the A_e box. *(PHY-05, PHY-13.)*

**F-08 · The gain-comparison figure actively teaches the wrong lesson**
`book/extras/slides/fig/gain-pattern-polar.svg` via `scripts/graphics/plots.py:60–88`
All four patterns are self-normalized (`ylim(-30,0)`), so isotropic/dipole/horn/dish all touch the 0 dB ring — the 0/2/16/28 dBi difference exists only in the legend, on a slide titled "Gain Comparison." The horn/dish are also modeled as cosⁿ lobes with zero sidelobes, while two slides later students are asked to identify sidelobes/SLL/back lobe on exactly this kind of plot. The widget it advertises (`polar-gain.html`) plots absolute dBi, so figure and interactive disagree.
**Fix:** Replot on an absolute dBi radial axis (0–30 dBi, matching the widget) and model the dish with a sinc²/Airy pattern with real sidelobes (the `rectilinear()` generator already does this). *(GFX-03, GFX-13; the project ToDo already flags plots.py's representative shapes.)*

## Majors — assessment and LO alignment (11)

**F-09 · The two authoritative LO lists disagree, and 30% of the grade is per-LO**
`book/syllabus.md` Module 1 LO table vs `book/module01/index.md` objectives 1.1/1.2
Syllabus 1.1 includes reciprocity and omits antenna recognition; the module page adds "recognize antennas by sight" to 1.1 and moves reciprocity + Friis into 1.2 (syllabus 1.2 has neither). Students study one list and are graded against another.
**Fix:** Reconcile to one list — recommend the module page's, which matches the lessons — and update `book/syllabus.md` and the four practice-set LO banners verbatim. *(PED-06.)*

**F-10 · L05 has no practice set and no Practice section**
`latex/` (no `ECE444_Practice_L05.tex`); `book/module01/L05-field-regions/index.md`
LO 1.5's three sub-LOs get zero written reps though L05 is fully quantitative (both boundary formulas, a worked 96 m / 4.7 m example); every M2 lesson L07–L14 including labs ships a set. The only place 2D²/λ is practiced is L06 Q2, framed as a phase-error problem.
**Fix:** Author `ECE444_Practice_L05.tex` on the M2 template (LO 1.5 banner): boundary calcs at two D/λ extremes, a "which region am I in" range-design part, one concept part on why the pattern still changes inside 2D²/λ, and a which-term-dominates-at-this-kr part (also closes F-39's unused algebra). Then add the Practice section to the page. *(PED-04, CON-03, PRB-02 — three lenses; known on the project ToDo.)*

**F-11 · The only pattern-reading practice is an ungradeable find-your-own-datasheet task**
`latex/ECE444_Practice_L02.tex:218–234` (Q5, all 5 parts)
"Find a published pattern and annotate it" — answers antenna-dependent, key grades method only, no M2 set contains any such research item, and pattern reading recurs in the midterm project and L12/L14/L22–L25. Students get no calibrated feedback on the course's most-used skill.
**Fix:** Move the datasheet hunt to the lesson page as an exercise; replace Q5 with a determinate problem against one supplied labeled plot (HPBW/FNBW/SLL/F-B read-offs), and add the same annotated plot as a worked example on the L2 page. *(PED-14, PRB-08.)*

**F-12 · L03 keys demand antenna families the course hasn't taught — one contradicts the lesson's own table**
`latex/ECE444_Practice_L03.tex:81–83` (Q4d) and `:101–103` (Q5c)
Q5c's key answers with PIFA, chassis slot, stacked patch — none in the L03 "Bandwidth by Antenna Type" table (families are M2 L07–L11 content). Q4d's key names "a standard-gain horn or half-wave dipole" for FBW ≈ 10.3%, but the lesson's own table lists horns at 30–50% — a student answering from the taught table contradicts the key.
**Fix:** Rewrite both keys from the taught table only (dipole 8–15% for Q4d, dropping the horn; broadband monopole/slot/Vivaldi/log-periodic for Q5c), listing PIFA/stacked patch as optional extras; require justification via the resonant/traveling-wave/self-scaling mechanism. *(PED-13, PRB-12, PRB-04.)*

**F-13 · The L03 set is ~40% over the workload calibration and has zero answer boxes**
`latex/ECE444_Practice_L03.tex` (whole set: 7 questions / 29 parts; verified 0 `\ansbox` against ~13 numeric answers)
M2 sets run 5–6 questions / 18–23 parts, max 4 parts per question, 11–20 answer boxes; spec §5 targets 45–60 min. Students triage away the back half (Chu–Harrington, the datasheet question) that carries the hardest material, and the blank copy gives no place to record a final answer.
**Fix:** Cut to 5–6 questions of ≤4 parts (fold Q2 into Q7 — both axial ratio; trim Q1 to 4 waves; drop Q7d, which duplicates Q7c's algebra) and wrap every numeric part in the standard minipage + `\ansbox` pattern with units. *(PRB-03, PRB-06, CON-24.)*

**F-14 · Reciprocity is a named LO with zero practice reps**
`latex/ECE444_Practice_L02.tex` (whole set) vs the L02 page's full reciprocity section
It is the hinge that justifies A_e = Gλ²/4π and every receive-side measurement in Module 2; with no reps it stays a slogan. (Assessments live in the private faculty repo and were out of scope — this finding is about practice reps only.)
**Fix:** Add a part to Q4 or Q6: given a measured receive pattern/gain, state the transmit gain and justify; plus one concept part naming a medium where reciprocity fails. *(PED-05.)*

**F-15 · Half of LO 1.4.3 (the L-match) is neither taught to a usable level nor practiced**
`book/module01/L04-impedance-feeding-baluns/index.md` "The L-match" (three prose sentences, no formula/schematic/example); `ECE444_Practice_L04.tex` Q3 is λ/4 only.
**Fix:** Add a small figure plus the two-line design recipe (cancel X, then transform R) and one worked complex-load example; add an L-match part to Q3. *(PED-09.)*

**F-16 · LO 1.1.4 (recognize real antennas) is backed by a TBD stub**
`book/module01/L01-course-intro/index.md` "Show & tell" ("Hardware checklist: _TBD_"); no labeled antenna image on page or deck.
It's the exact vocabulary L3's bandwidth table and practice assume.
**Fix:** Add a labeled gallery (dipole, monopole, patch, horn, Yagi, spiral, dish) with one geometry→job line each, on page and deck; keep show-and-tell as live reinforcement. *(PED-12.)*

**F-17 · The A_e derivation runs on three quantities not yet established**
`book/module01/L02-antenna-properties/index.md` "Effective aperture" steps 1–2
Effective length ℓ_e (defined in half a clause), R_r = 80π²(ℓ/λ)² (R_rad not introduced until L4), D = 1.5 (derived in L6). The densest derivation in L2 with every input unexplained at that moment — the classic stall point.
**Fix:** Precede it with a 3-line box defining R_r and ℓ_e and flagging D = 1.5 as an L6 result being borrowed (or move the derivation after L4). Coordinate with F-05's correction in the same lines. *(PED-07.)*

**F-18 · Γ is used two lessons before it is defined**
`book/module01/L02-antenna-properties/index.md` "Γ, VSWR, and Power Reflected" ("Recall:") and L03 "Impedance bandwidth" — L04 defines Z_in and Γ = (Z_in−Z0)/(Z_in+Z0); nothing earlier establishes forward/reflected waves.
**Fix:** Add 3–4 sentences at the L2 Γ section deriving Γ from the mismatch on a Z0 line with a forward pointer to L4. *(PED-08.)*

**F-19 · P_rad = ∮U dΩ is stated but never once evaluated in Module 1**
`book/module01/L02-antenna-properties/index.md` "Radiation intensity"; no worked example, deck example, or practice part integrates a pattern.
Directivity is *defined* by that integral and L6 hands U(θ,φ) back to it; students can only use the 41,253 rule.
**Fix:** One worked example — D of the sinθ doughnut integrated to 1.5 — in L2 or L6 Part 5.1, plus a matching practice part. *(PED-11.)*

## Majors — structure and form vs Module 2 (9)

Every divergence below was adjudicated: in all cases **Module 2 / the spec is right** and Module 1 should change. No `[M2-DEFECT]` survived review.

**F-20 · Section order and closer naming drift**
`L02/index.md:592–612`, `L03/index.md:496–517`: Summary → "Where this shows up next" → Practice → "Preparing for LN". Spec §2 and all of M2: Summary → Practice → "Where this is going". Practice links are buried and the closer has two names inside one module (L04–L06 already say "Where this is going").
**Fix:** Reorder, rename, and fold the reading assignment into the closer's prose. *(CON-02.)*

**F-21 · L04 and L05 have no Summary table; L04 also lacks the prep note**
Spec §2 requires a 5–9 row table; all five M2 lessons carry one. The consolidation sheet vanishes exactly where notation load peaks (R_r, R_loss, X_in, Γ, VSWR, RL, mismatch loss).
**Fix:** Add `## Summary` tables in the M2 3-column shape before Practice in both. *(CON-04, PED-21.)*

**F-22 · Symbol harmonization cluster — four renames, all toward spec §6 / M2**
(a) η_rad → η_cd (L02/L04 pages + decks, 11 occurrences; G = η_cd·D per spec); (b) R_rad/R_loss → R_r/R_ℓ (L04 page + deck; L02:446 and all of M2 already use R_r); (c) η₀ → η (19 occurrences in L02/L05; L06 and M2 use bare η ≈ 377 Ω); (d) `\text{in}` upright subscripts → italic (Z_in, R_in, X_in in L04; η_ap in L02).
A student reading L07 sees unintroduced symbols for quantities L02/L04 already defined — the M1/M2 seam made visible.
**Fix:** Mechanical sweep across the four files and their decks; verify with the build. *(CON-05, CON-06, CON-12, CON-13.)*

**F-23 · L01–L03 decks close without the Key point / "Where this is going" pair**
Spec §3 items 6–7; every M2 deck has both. The one-sentence takeaway is never isolated.
**Fix:** Insert a `## Key point` callout slide and rename/rebuild the closer; keep reading+QR as a trailing slide. *(CON-07.)*

**F-24 · Eight of fourteen M1 widgets use ad-hoc control markup**
`cp-helix, effective-area, feed-match, gain-builder, pattern-features, polar-gain, polarization-playground, vswr-standing-wave` use `.panel/.readout/.slider-block/...` instead of the spec §4 `.controls`+`.ctl` bar and `.pills` readouts all nine M2 widgets share. Students relearn the interface each lesson.
**Fix:** Refactor to the `app → canvas → .controls → .pills` layout (the palette is already right). Defensible to defer behind content fixes. *(CON-09.)*

**F-25 · L02 and L03 open cold — no hook paragraph; L03's is a broken callback**
Spec §2/§9 requires a one-paragraph hook; L04–L06 and all of M2 have one. L03's "Reading a datasheet" section says "This lesson opened with a claim…" but the page has no opener — the claim exists only on the deck (an artifact of the datasheet section being added later).
**Fix:** Add 3–5 sentence hooks after each LO list; state the misquoted-specs claim in L03's so the callback lands. *(CON-10, PED-18.)*

**F-26 · Worked examples aren't findable — bold-lead paragraphs instead of admonitions**
`L02:511, 559; L03:101, 159; L05:225` vs spec §2 / M2 / L06's own correct `:::{admonition} Worked example — …\n:class: tip`.
**Fix:** Wrap each in the tip admonition with a descriptive title. *(CON-11.)*

**F-27 · L02 is drastically overloaded relative to every other lesson**
Maxwell → telegrapher's → wave equation → plane wave → Poynting → solid angle → U → D → G → Γ/VSWR → pattern features → reciprocity → A_e → Friis, with 6 widgets, in 2 Parts (~580 lines); spec says 3–6 Parts, L3–L6 carry 3–5 sub-LOs each. The median student leaves with vocabulary, not fluency, and everything later assumes L2 stuck. (The 41-lesson manifest is fixed, so the reviewers' "split into two lessons" fix is rejected.)
**Fix within one lesson:** restructure into 4–5 Parts (physics chain / power & pattern quantities / reciprocity + A_e / Friis), demote the Part-1 refresher to assigned pre-reading keeping only the plane-wave slide in class, and split the deck's radiation-intensity slide (F-33). *(PED-03, CON-24, GFX-12.)*

**F-28 · L04 deck contains not one figure**
16 slides, zero `data-inline-svg`, for the most drawable topics in M1 (λ/4 transformer, L-match, shield current, three balun types); M2's L07/L09 got 5–6 figures for comparable material. A balun lesson without a picture of current on the outside of the shield teaches nothing visual. Deck is also under the 18-slide floor.
**Fix:** Add ≥4 figures (`l04-zin-split`, `l04-quarter-wave`, `l04-lmatch`, `l04-balun-currents` — the last adapts `viz/img/balun-currents.svg`) and 2–4 content slides. Matches the existing ToDo to extend the SVG pipeline to L01/L04. *(GFX-02, CON-24.)*

## Majors — graphics and decks (6)

**F-29 · The L05 page promises a phase-error view its widget doesn't have**
`book/module01/L05-field-regions/index.md:201–259` says "The phase error across the aperture is shown so you can see why the far-field distance grows with D²"; `field-regions.html` draws only a 1-D log ruler with two markers. Nothing in M1 pictures the curved-wavefront construction behind 2D²/λ — the derivation both L05 and L06 rest on (M2 built `range-phase-error` for exactly this).
**Fix:** Add a wavefront-across-aperture panel (edge-vs-center Δ, phase error in degrees, green at 22.5°) to the widget, or ship it as a static deck figure and fix the page text. *(GFX-04.)*

**F-30 · The L03 page has zero static figures for the most geometric lesson in M1**
Only two iframes; the polarization ellipse, handedness, AR, cos²ψ PLF, and Chu bound all already exist as `slides/fig/*.svg` but none is mirrored to the page a student revises from.
**Fix:** Mirror `pol-states`, `axial-ratio`, `plf-cos2`, `chu-q-vs-ka` into `viz/img/` and place at matching sections. Near-zero drawing effort. *(GFX-05.)*

**F-31 · Neither the L06 deck nor page plots a single radiation pattern**
The sinc pattern, first null, −13.3 dB SLL, half-wave dipole pattern, and three-distributions comparison are all tables and formulas. The lesson's thesis — change the current, change the pattern — pays off only as a picture, and "−13.3 dB independent of L" is unbelievable without seeing two sidelobe sets at one level.
**Fix:** Add `l06-line-source-sinc` (annotated null/HPBW/SLL) and `l06-three-patterns` (sinθ vs half-wave vs sinc overlay), reusing the `rectilinear.py` style. *(GFX-06.)*

**F-32 · The slide titled "The integral, as a picture" has no picture**
`book/extras/slides/L06-radiation-integrals.md:201–215` — three bullets describing a phasor chain, deferring wholly to the lesson-page widget; in a live lecture the phasor chain never appears on screen.
**Fix:** Add `l06-phasor-chain` (straight at broadside, curled off-broadside, closed at first null). *(GFX-07.)*

**F-33 · A finished 4-control widget is orphaned exactly where L02 needs it most**
`book/extras/viz/effective-area.html` (verified: referenced from no page anywhere) — dish diameter/η_ap/gain/frequency with a physical-dish↔gain toggle, i.e. the A_e = λ²G/4π ↔ η_ap·A_phys duality that is L02's hardest idea.
**Fix:** Iframe it into the L02 "Effective aperture" section with the standard 2–4 sentence caption, at measured height. *(GFX-08, PED-25.)*

**F-34 · No `.reveal table` CSS rule — eleven slides carry tables at the 30px base font**
`book/extras/slides/course-slides.css`; worst offenders L03 #19 (9×3), L06 #15 (5×3 with prose cells). L02 #16 hard-codes `font-size:0.74em` inline — proof the author already hit the problem.
**Fix:** Add `.reveal table { font-size: 0.62em; }` plus tighter cell padding to the house CSS; drop the inline override. One rule fixes eleven slides. *(GFX-11.)*

---

## Minors (37)

Physics and numbers:
- **F-35** `L03/index.md` "Bandwidth is limited by size" (+ deck): BW ≈ 1/Q is dimensionally loose and is the half-power form; at the VSWR ≤ 2 bar used everywhere else, FBW ≈ 0.71/Q (~40% less optimistic). Write FBW explicitly and add the (s−1)/(Q√s) parenthetical. *(PHY-06.)*
- **F-36** `L03/index.md` UWB bullet: "FBW ≥ 67% by FCC definition" misattributes — FCC UWB is FBW ≥ 0.20 or ≥ 500 MHz. Keep 2:1/67% as the course's own bar; state the FCC criterion correctly. *(PHY-07.)*
- **F-37** `L02` page + deck: "|Γ|² = Reflected Power" — they're fractions of incident power. Write P_refl/P_inc = |Γ|². *(PHY-08.)*
- **F-38** `L05/index.md` "Where the far-field distance comes from": opens "Picture a **plane** wavefront…" — a plane wavefront has zero edge-to-center path difference; the derivation needs *spherical*. One-word fix. *(PHY-09.)*
- **F-39** `L05/index.md` complex-Poynting expansion (to 1/r⁵) is the heaviest algebra in M1, before L6's machinery, with nothing asking students to use it. Demote to a collapsible aside marked optional; the kr-dominance practice part in F-10 gives it a payoff. *(PED-15.)*
- **F-40** `L03/index.md` "Misquote 2": ρ̂_a uses +j whose handedness is never stated under the lesson's own convention. Half a sentence fixes it. *(PHY-10.)*
- **F-41** `L02/index.md` telegrapher's: L and C never identified as per-unit-length (H/m, F/m), so u = 1/√(LC) reads dimensionally wrong in the course's dimensional-analysis warm-up. *(PHY-12.)*
- **F-42** `L03` page + deck: θ used for polarization tilt collides with the course-wide polar θ (spec §6). Use ψ throughout L3. *(PHY-14.)*
- **F-43** `L02/index.md` A_e footnote: "the 8 (not 4) is the time-average" misattributes the factor split (4 from the divider at match, ×2 from time-averaging); the deck's speaker note has it right, so page and deck disagree. *(PHY-15.)*
- **F-44** `ECE444_Practice_L03.tex:156–164` Q7e: key's headline −9.5 dB (A² = 2 shortcut) vs the lesson page and Summary's −9.6 dB (exact A). **The lesson is right.** Box −9.6, demote the shortcut to the parenthetical. *(PRB-07.)*

Practice-set mechanics:
- **F-45** `ECE444_Practice_L04.tex` Q5(a)(c)(d) numeric with no `\ansbox` while Q1–Q4 box everything; Q2(a) prompts four quantities but boxes two. Convert to the set's own pattern. *(PRB-09, PRB-11.)*
- **F-46** `ECE444_Practice_L02.tex:75, 254`: boxes print bare numbers — add rad/s and W/m². *(PRB-10.)*
- **F-47** `ECE444_Practice_L02.tex` Q1c: "velocity factor 0.66" key runs on dielectric filling and λ_g, taught nowhere in L02. Add a clause to the telegrapher's section or reduce the key. *(PRB-13.)*
- **F-48** Four questions exceed the 4-part max M2 never breaks (L02 Q5, L03 Q1/Q7, L04 Q5); L03 Q7 spills a lone part onto page 8. Split or trim. *(PRB-14.)*
- **F-49** `ECE444_Practice_L06.tex:304–311` Q6c key asserts "L of order 25λ" without the two-line conversion spec §5 requires solutions to show. *(PRB-15.)*
- **F-50** `ECE444_Practice_L04.tex` Q2/Q4/Q5 are the same Γ→VSWR→RL arithmetic thrice while matching and baluns get one question each — the set doesn't ramp. Fold Q4 into Q2; give matching a full question. *(PED-17.)*
- **F-51** Raw LaTeX where house macros exist: `50$\Omega$` (L04:56), `\hat{r}` ×3 (L06:33–44). Sweep all four files. *(CON-23.)*

Lesson-page form:
- **F-52** `L04/index.md` Part 2 cites "the amplifier/diode problem in Lesson 3" — it's Q5 of L4's own set; no such L3 problem exists. Make it a forward reference. *(PED-16.)*
- **F-53** L02's Summary table: 3 of 7 rows are concepts L2 never teaches (polarization, bandwidth, impedance) while U, A_e, reciprocity, Friis are absent. Fold into the F-21/spec-shape conversion: all four M1 summaries → 3-column `Symbol | What it is | Number to remember`, numbers populated. *(PED-20, CON-17.)*
- **F-54** Chu–Harrington/Q/antenna-class taxonomy is taught and graded but appears in no LO. Add a sixth L03 sub-LO. *(PED-19.)*
- **F-55** `book/module01/index.md` synopsis says the module "end[s] with the trade-offs every array design has to make" — it ends with radiation integrals; arrays are M3. Reword the closing clause. *(PED-23.)*
- **F-56** `L06/index.md` Part 4 introduces the visible region in a subordinate clause and never uses it — the concept that later makes grating lobes intelligible. Give it two sentences and the L16 pointer. *(PED-24.)*
- **F-57** `L03/index.md:343` "Reading a datasheet" sits outside the Part numbering. Renumber as Part 3. *(CON-18.)*
- **F-58** `L03/index.md:421` a Key Point admonition uses `:class: tip` while line 313 uses `key-concept` correctly — the takeaway color-code breaks on one page. *(CON-19.)*
- **F-59** `L02/index.md:426, 440` "capture area" — spec §6 explicitly forbids it. Use "effective aperture". *(CON-20.)*
- **F-60** `L02` four figures wrapped in `<p style="text-align:center">` instead of the standard bare `<img>` pattern the rest of M1 uses. *(CON-16.)*
- **F-61** `L02/index.md:310` serves `vswr_vs_gamma.png` (raster, underscore name) inside a hand-rolled flex div whose raw `<table>` carries literal untypeset `|Γ|`; a crisp `slides/fig/vswr.svg` already exists. Point the page at an SVG copy and use a MyST table with `$\vert\Gamma\vert$`. *(CON-15, GFX-19.)*
- **F-62** `L03/index.md:104–105` uses `\,` in display math — course rule is `\ `. *(mechanical pass.)*

Decks:
- **F-63** `slides/L01-course-intro.md` references `img/01-course-intro/syllabus-qr.png`; the file is at `img/syllabus-qr.png` — the slide ships a dead image (verified). One-line path fix. *(mechanical pass.)*
- **F-64** L01's "## Homework" slide is a bare title; the course's least-familiar mechanics (practice = engagement credit, LO mastery = 30%, resubmission) are never delivered in class. Three lines fill it. *(PED-22.)*
- **F-65** L02/L03 carry bare "## Part N" divider slides no M2 deck uses — four contentless slides. Delete. *(CON-21.)*
- **F-66** viz-cue slides lack M2's `<!-- .slide: class="viz-cue-slide" -->` class (10 slides across L02/L03/L04/L06); L03:224's "▶ Live demo" cue is nonstandard. *(CON-22.)*
- **F-67** Speaker-note coverage is partial (L01 5/18 … L06 11/24) vs M2's ~every slide; several viz-cue slides — where spec *requires* a note — have none. Prioritize those. *(CON-14.)*
- **F-68** `slides/L03` "Resonant vs traveling-wave" is the densest slide in M1 (116 words + table, no figure). Split it; the three-panel current figure is F-77. *(GFX-15.)*
- **F-69** `slides/L02:458–479` a 22-line raw `<svg>` pasted inline, unlike every sibling figure. Extract to `fig/short-dipole-incident.svg`. *(GFX-22.)*

Figures:
- **F-70** `viz/img/antenna-input-z.svg`, `recv-circuit.svg`: 66/85 KB dvisvgm outputs with CM glyph outlines, no committed TikZ source; `recv-circuit` exists in two inconsistent styles (deck vs page). Redraw as house-style hand SVG or commit the source. *(GFX-18.)*
- **F-71** `fig/reciprocity.svg` draws a dipole with a single unidirectional cardioid lobe — students just taught pattern reading will see a contradiction. Draw the true figure-eight on both antennas. *(GFX-20.)*
- **F-72** `fig/solid-angle.svg` cone fill at opacity 0.05 — the solid angle is the least visible element of its own figure. *(GFX-21.)*
- **F-73** `fig/chu-q-vs-ka.svg` has an unexplained orange marker at (ka=1, Q=2). Label or remove. *(GFX-23.)*
- **F-74** `fig/recv-circuit.svg` shows no reactance and no R_L = R_r label though the factor-of-8 result depends on the conjugate match. *(GFX-24.)*
- **F-75** Rename M1's unprefixed figures (`vswr.svg`, `solid-angle.svg`, `poynting.svg`, …) to the M2 `L<NN>-<name>.svg` scheme in both `slides/fig/` and `viz/img/`, updating references — 41 lessons share two flat directories and M3 will want its own `vswr`/`solid-angle`. *(CON-08 — demoted from major: zero student impact today, real collision risk later.)*

---

## Ideas (13)

- **F-76** Add the practical directivity constant (26,000–32,400) beside the exact 41,253 rule; note real horns/dishes lose 1–2 dB to sidelobes. *(PHY-16.)*
- **F-77** Three-panel current figure for resonant / traveling-wave / self-scaling (pairs with F-68). *(GFX-15.)*
- **F-78** "η_ap is set by the metal, doesn't change with frequency" deserves a "to first order" — illumination taper and Ruze loss drift it, which is why real dishes stop gaining at high f. *(PHY-17.)*
- **F-79** L06 three-distributions table: label the D = 4.21 row "space factor only" and add the honest 4.45 (6.5 dBi) in the cell, not just the prose below. *(PHY-18.)*
- **F-80** Bandwidth-intersection figure (three spec bands vs frequency, intersection shaded) for L03's headline claim. *(GFX-09.)*
- **F-81** R_in/X_in vs ℓ/λ plot for L04 resonance — note M2's L07 already builds `dipole-resonance` for this in depth; a thumbnail + forward pointer may suffice. *(GFX-10.)*
- **F-82** PLF interactive: add an antenna-polarization pane + live PLF dB readout to `polarization-playground` so −3 dB linear↔CP and cos²ψ fall out by dragging. *(GFX-16.)*
- **F-83** Day-one transducer figure (guided wave → flare → spherical wavefronts, reciprocity arrow). *(GFX-17.)*
- **F-84** Faraday-rotation two-panel (linear arrives rotated; CP survives) for the why-CP motivator. *(GFX-25.)*
- **F-85** Friis link-geometry figure for the page (the deck part is in F-02). *(GFX-14.)*
- **F-86** L06 set: raise answer-box density toward M2's 11–20 (currently 8/22 parts). *(PRB-16.)*
- **F-87** L02 set has no explicit trade-off part (spec targets ~15%); convert Q6d into "you're 6 dB short — buy it from P_t, G_t, or G_r?" *(PRB-17.)*
- **F-88** L01 practice set: M1 ships 4 sets for 6 lessons vs M2's 8-for-8. Defensible exception (LO 1.1 is recognition-level) — either add a short 2-question identification set or record the exception deliberately in the spec (see spec gaps). *(PRB-18, CON-03.)*

---

## Adjudications, downgrades, and kills

- **No Module 2 defects surfaced.** Lenses 3 and 4 were licensed to file `[M2-DEFECT]` where Module 1 was more correct; none survived. The one right-vs-wrong call inside M1 (F-44) went to the lesson page over its own practice key.
- **CON-25 (prose "L6" vs "Lesson 6") killed as a defect** — spec §2 explicitly permits both forms; recorded as taste only.
- **"Split L02 into two lessons" rejected as a fix** — the 41-lesson manifest is fixed; F-27 keeps the overload finding with an in-lesson restructure.
- **F-03 softened but kept blocker** — the taper numbers do exist in the `line-source-pattern` widget (verified in the project note), but a graded key cannot rest on unprompted widget exploration.
- **"Never assessed" claims softened to "no practice reps"** — summative assessments live in the private faculty repo, outside this review's scope.
- **GFX severities normalized** — missing-figure findings kept major only where a page/deck *promises* a visual it lacks (F-29, F-32) or a core concept has zero visual support anywhere (F-28, F-30, F-31); the rest moved to ideas.
- **F-75 (figure renaming) demoted major→minor** — preventative, no student impact today.

## Gaps in COURSE_SPEC.md (it should capture what Module 2 actually does)

1. **Merge `COURSE_SPEC.md` to `main`.** It currently exists only on the module-2 branch; it is the course's rubric and Module 1's fixes will be made against it.
2. Summary tables: specify the M2 3-column shape — `Symbol / idea | What it is | Number to remember` — not just "a symbol/idea table, 5-9 rows".
3. Figure naming: mandate `L<NN>-<name>.svg` in both `slides/fig/` and `viz/img/`.
4. Deck: viz-cue slides also carry `<!-- .slide: class="viz-cue-slide" -->`; a `Note:` on (essentially) every slide, not only viz-cue slides.
5. Notation (§6): polarization tilt angle is ψ, never θ.
6. Canonical numbers (§7): add the CP-vs-linear swing −1.8 / −4.8 dB and the −9.6 dB worst case at AR = 3 dB (L03's own derivation, now also a practice answer); if F-76 is adopted, add the practical 26,000 beamwidth-product constant beside 41,253.
7. Practice: every numeric part gets an `\ansbox` with units, 11–20 boxes per set (M2's actual range); hard max 4 parts per question.
8. Section flow: state where the "read before next lesson" note lives (M2 folds it into "Where this is going" — M1's separate "Preparing for LN" is retired by F-20).
9. Practice-set policy for intro-type lessons: M2 ships a set for every lesson including labs; state explicitly whether an L01-type intro lesson is exempt (see F-88).

## Best impact-to-effort (do these first)

1. **F-03 — taper table + one beamwidth sentence into L06** (~30 min): unblocks a graded question two lenses flagged as unanswerable.
2. **F-04 — rewrite the AR ≤ 3 dB sentence, page + speaker note** (~15 min): kills a physics misconception the instructor would otherwise say aloud.
3. **F-34 — one CSS rule for deck tables** (~10 min): fixes legibility on eleven slides at once.
4. **F-33 — embed the orphaned effective-area widget in L02** (~20 min): activates finished work at the lesson's hardest section.
5. **F-22 — the four-symbol harmonization sweep** (~1–2 h, mechanical): removes the M1/M2 notation seam before students hit it at L07.

## Effort to bring Module 1 to Module 2's standard

Roughly **7–9 focused working days** for everything defect-tier, or **~5 days** deferring the widget-UI refactor (F-24) and all ideas:

- Blockers: L05 deck ~1–1.5 d; L02 Friis slides ~0.5 d; F-03 ~0.5 h.
- L05 practice set (+ optional L01): 0.5–1 d.
- Physics corrections (F-04..F-08): ~0.5 d.
- Practice repairs (L03 restructure + boxes, keys, L02 Q5 replacement, minors): ~1 d.
- Structure/consistency sweep (F-20..F-27 + page minors): ~1 d.
- Graphics (L04 deck figures, L06 patterns, L03 mirrors, phasor chain, gain-polar replot, figure minors): ~1.5–2 d.
- Widget UI refactor (F-24): ~1–1.5 d, deferrable.
