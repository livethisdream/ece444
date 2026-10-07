# Module 3 build-out plan — from the existing materials to the site

Written 2026-10-07 from Neil's ADI beamforming deck (97 slides, attached that
day), the Phaser GUI repo at `main` (2026-10-06), and the state of
`book/module03/`. This is the plan Neil asked for: what we have, what each
source contributes, and the order of work. It is a working note; update it as
decisions land, and mirror the decisions into `COURSE_SPEC.md` and
`project/ECE444_PROJECT.md` the same turn.

## 1. Where Module 3 actually stands

"Build out the lessons" is not a from-scratch job. The August build
(2026-08-23, branch `claude/module-3-antenna-beamforming-qet0pj`) left every
Module 3 lesson with the full bundle, and the ADI numbers in the deck Neil
attached are already in `COURSE_SPEC.md` §M4, because that build worked from
the same workshop material (`docs/2025_Phaser_labs_Python.pdf` in the Phaser
repo) and the GUI's lab presets.

| Lesson | Page | Deck | Practice PDFs | Widget | Lab sheet | Sweeps + present cut |
| :-- | :-- | :-- | :-- | :-- | :-- | :-- |
| L15 Aperture Distributions | yes | yes | yes | yes | n/a | done (10-03 to 10-05) |
| L16 Array Factor | yes | yes | yes | 4 | n/a | done (10-04 to 10-05) |
| L17 Phased Array Hardware (lab) | yes | yes | yes | yes | Lab 4 | **none**, 55 frames |
| L18 Beam Steering Theory | yes | yes | yes | yes | n/a | none, 37 frames |
| L19 Beam Steering Lab | yes | yes | yes | yes | Lab 5 | none, 42 frames |
| L20 AF and Beamwidth | yes | yes | yes | yes | n/a | none, 39 frames |
| L21 Array Factor Lab | yes | yes | yes | yes | Lab 6 | none, 40 frames |
| L22 Antenna Pattern Theory | yes | yes | yes | yes | n/a | none, 37 frames |
| L23 Antenna Pattern Lab | yes | yes | yes | yes | Lab 7 | none, 43 frames |
| L24 Sidelobes and Tapering | yes | yes | yes | yes | n/a | none, 46 frames |
| L25 Tapering Lab | yes | yes | yes | yes | Lab 8 | none, 35 frames |
| L26 Squint and Quantization | yes | yes | yes | yes | n/a | none, 40 frames |
| L27 Null Steering Theory | yes | yes | yes | yes | n/a | none, 46 frames |
| L28 Null Steering Lab | yes | yes | yes | yes | Lab 9 | none, 51 frames |

So the work is: (a) the three quality sweeps and the present cut on L17 to
L28, in teaching order, using the ADI deck as the figure and nomenclature
source; (b) re-executing and updating the six labs against the GUI as it is
*now*, which has moved since August; (c) a hardware validation day. Nothing
here is a rewrite.

## 2. The materials, and what each one is for

### A. The ADI beamforming deck (attached 2026-10-07, 97 slides)

ADI's phased-array workshop deck (Jon Kraft), with the RadarConf'24
"Hands On Adaptive Digital Beamforming" section spliced in at slides 46 to
66. Slides 38, 45, 58, 67, 71, 84, 97 are black separators. It is reference
and figure inspiration, **not** something to copy: it is ADI's copyright and
its figures are raster screenshots. Every figure we take from it is redrawn
as a house SVG from a committed generator, with our notation
(`COURSE_SPEC.md` §M2), and its lab procedures are rewritten against our GUI
(§M3), never against the Tk GUI, Thonny, or MATLAB shown in the slides.

Slide-by-slide map onto the lessons. "Have" means the existing page already
carries the content; "take" means the deck gives us something the page lacks.

| Slides | Content | Lesson | Status |
| :-- | :-- | :-- | :-- |
| 1 | Workshop goals: theory + hardware = understanding | Module 3 overview | have (framing only) |
| 2 to 14 | Delay-line animation: a wavefront arrives at an angle, per-element delay lines bring the 8 signals into phase, then the two 4-element sums combine | L18 | **take**: the single best picture of what steering *is*. Build as a widget (source-angle slider, delay bars fill, phasors align), replacing or joining the static wavefront figure |
| 15, 16 | Steering geometry: $L = d\sin\theta$; delay $\Delta t = d\sin\theta/c$; phase $\Delta\phi = 2\pi d\sin\theta/\lambda$, "three ways to describe this delay" | L18 | have (the derivation runs the same three forms); check the deck shows all three as one chain |
| 17 | Worked example: 30° at 10.3 GHz, d = 14 mm, gives 86° per element, wrapped ramp 0, 86, 172, 258, 344, 70, 156, 242 | L18, L19 | have (86.6° with exact constants; the deck rounds 0.52 rad and c = 3e8). Keep 86.6° and the wrapped-ramp table |
| 18 | "Standard configuration" block diagram: Phaser, Pluto, Pi, HB100 | L17 | have (`L17-signal-chain.svg`) |
| 19 | ADAR1000: signals arrive at an angle (time-domain plot), phase-shift and weight, sum in phase | L17 | **take** as a three-panel figure: arriving waveforms offset in time, the chip's phase/gain per channel, the coherent sum. Pairs with the delay-line widget |
| 20 | HB100: 10.525 GHz DRO, Tx + Rx patches + mixer, 40 mA at 5 V, azimuth and elevation patterns | L17 | partial. Add the two-line "why it drifts" (free-running DRO) and that it is a Doppler module we use as a tone source |
| 21 | Element factor + array factor, gain in dB adds | L22 | have |
| 22 | Array factor as the phasor sum, closed form $\sin(N\Delta\phi/2)/(N\sin(\Delta\phi/2))$ | L16 | have |
| 23 to 25 | Normalized AF for N = 2, 4, 8; HPBW 62°, 27°, 13°; FNBW 180°, 62°, 30° | L20, L21 | have (§M4) |
| 26 to 30 | Lab: array factor and beamwidth, record peak dBFS / HPBW / FNBW / first sidelobe for N = 8, 4, 2 by disabling Rx1, 2, 7, 8 | L21 | have (lab sheet table matches) |
| 31 | MATLAB sensorArrayAnalyzer | none | **skip** (no MATLAB; our widgets do this) |
| 32 to 36 | Sidelobes: the interference-in-a-sidelobe picture; uniform weights are a boxcar window, FFT analogy, first sidelobe −13 dBc; Boxcar / Hann / Blackman windows; uniform vs Hamming element weights and patterns | L24 | **take** the DSP-window analogy. L24 currently names windows but never makes the "a taper is the window you already know from signals" link. One present frame plus one figure (element weights beside the pattern, uniform and Hann) |
| 37 | Lab: tapering, copy plot to memory, try presets, invent a symmetric taper | L25 | have (GUI Freeze = ADI's Copy Plot to Memory) |
| 39 to 42 | Null steering: $w = w_d - r_n w_n$, $r_n = w_n^H w_d / w_n^H w_n$, before and after patterns, hardware demo | L27 | have (§M4) |
| 43, 44 | Lab: null steering, enable Null 1 at a sidelobe, rotate the HB100, the null stays put | L28 | have (Procedure A/B) |
| 46 to 49 | Digital beamforming: $y = w^H x$; "a monumental shift": analog aims then gathers, digital gathers then aims | L27 | **take** the aim-then-gather / gather-then-aim contrast as a key-point callout; it is the hybrid-architecture lesson in one line |
| 50 to 54 | Adaptive beamforming, MVDR objective, covariance matrix $\hat R = XX^H/K$, sample matrix inversion | L27 | have; check the covariance frame derives $P_\text{out} = w^H R w$ rather than quoting it |
| 55 | Making Phaser an all-digital beamformer: attenuate 3 of 4 elements per subarray, leaving two digital channels | L27, L28 | have (2-Elem aperture preset); make sure the page says *why* in the deck's words |
| 56 | `w_mvdr(theta, X)` in eight lines of numpy | L27 | **take** as the code excerpt (§M6 allows ≤ 15 lines; this one is Python and matches the backend) |
| 57 | Lab: two-element MVDR, rotate the HB100, watch the weights | L28 | have (Procedure C against a second HB100) |
| 59 to 61 | Repeats of 47, 51, 52 | | skip |
| 62 to 66 | Quad MxFE 16-channel digital beamformer, backyard DOA, MVDR with training | none | **skip** as procedure (not our hardware). At most one "where this is going" line in L28: with 16 digital channels the same equation places nulls on two jammers at once |
| 68 to 70 | Measuring the actual pattern: electrical scan vs mechanical scan vs HFSS overlay; rotate the HB100 by hand from −90° to +90° | L22, L23 | **take** the three-trace overlay as an L22 figure (the deck's data redrawn, or our own sim vs AF). L23's hand-rotation procedure is now a candidate for the rotating stand (§2D) |
| 72 to 79 | Grating lobes as spatial aliasing; AF at d = 0.5, 0.75, 1.0, 1.5, 2.0, 2.5 λ | L26 | partial. The sampling analogy is one sentence on the page; the d/λ sweep belongs in the widget or as a six-panel figure |
| 80 | Why only m = 0 is real: arcsin of a value outside [−1, 1] on the arcsin curve | L26 | **take** as a figure. It is the picture behind the "visible region" argument L16 and L26 both make in words |
| 81 | $d_\text{max} = \lambda/(1 + \lvert\sin\theta_\text{max}\rvert)$; at 11.5 GHz and 14 mm, grating lobe appears at 60° | L26 | have the criterion; **take** the 11.5 GHz case as a practice problem |
| 82, 83 | Cases 2 and 3: every 3rd element (42 mm) gives 0°, ±44°; every 4th (56 mm) gives 0°, ±31°, ±90° | L26 | have (§M4, Lab preset 4) |
| 85 to 94 | Monopulse: sum and delta beams, the two subarrays, delta null, gain and phase error functions | L28 | have (§M7, end of L28) |
| 95, 96 | Lab: monopulse with Blackman taper; Tracking mode; rotate the Phaser; 2.8° per step | L28 | have (Procedure D). Rotating the *array* is what the new stand is for |

Not in this deck at all: **beam squint** and **quantization sidelobes**. Those
come from the Python labs PDF (pages 19 and 21) and are already in L26 and
Lab presets 5 and 6.

### B. ADI's *Phased Array Radar Workshop*, Python edition (40 pages)

This is the "Python lab notebook" (resolved 2026-10-07: Neil attached it,
and it is byte-identical to `docs/2025_Phaser_labs_Python.pdf` in the Phaser
repo, the file the August build worked from; there is no `.ipynb` anywhere).
It is the canonical lab sequence the GUI presets follow, with the FMCW,
range-Doppler, MTI, and CFAR labs (pages 29 to 38) that are Module 4, and
the frequency-plan appendix (page 39). Private: read in-session, never
copied into this repo.

Beyond the deck it carries the *procedure* detail, and three things came
out of reading it against the lessons and the GUI:

| Workshop lab (page) | Procedure specifics | Lesson | Status |
| :-- | :-- | :-- | :-- |
| SDR and software control (7, 8) | run the minimal example; what it does in nine bullets (10.525 GHz in, 2.2 GHz IF, 30 MSPS, 20 MHz filter, 1024 samples, FFT); change the LO offset and re-run | L17 | have; the nine-bullet list is a good present frame |
| Steering angle (9, 10) | HB100 at about 30° with a protractor on the Pi; find the steer angle that maximizes the FFT peak; then the Rectangular plot | L19 | have (protractor arc, 30° case). Note L18 quotes 86.6° per element at 10.3 GHz and L19 quotes 88.4° at 10.525 GHz; both are right for their frequency, and the why-sweep should say so in one line |
| Array factor and beamwidth (11 to 13) | N = 8, 4, 2 record table | L21 | have |
| Measuring the actual pattern (14, 15) | Signal vs Time mode, HB100 walked from −90° to +90°, broadside then 30°; "we cannot get angles from this, only lobe amplitudes" | L23 | have (Lab preset 7, the walk, "amplitudes survive, angles do not") |
| Sidelobes and tapering (16) | Copy Plot A, try the presets, invent a symmetric taper | L25 | have |
| Grating lobes (17, 18) | every 3rd element (42 mm) then every 4th (56 mm) | L26 theory; Lab preset 4 | have as theory and preset; **no course lab runs preset 4** |
| Beam squint (19, 20) | HB100 at about 50°, Copy Plot A, Signal BW to 500 MHz, record the new peak; the note that the GUI moves the *calculated* frequency rather than the source | L26 theory; Lab preset 5 | **no course lab runs preset 5** |
| Quantization sidelobes (21, 22) | Blackman, steer 15°, walk the HB100; Phase Shift Bits to 2 and walk again | L26 theory; Lab preset 6 | **no course lab runs preset 6** |
| Null steering (23, 24) | Enable Null 1 on a sidelobe, rotate the HB100 | L28 | have |
| Adaptive beamforming (25 to 27) | 2-element MVDR; the script is `Phaser_MVDR.py` from `github.com/jonkraft/PhaserExamples` (public) | L27, L28 | have; the public repo is a legitimate code source for the ≤ 15-line excerpt, alongside our backend |
| Monopulse (28) | Blackman, Tracking mode, rotate the array | L28 | have |

The gap: objective 3.8 (grating lobes, squint, quantization) is the one
Module 3 objective with GUI presets and workshop procedures but no
hands-on lesson. L26 is scheduled as theory and has no lab sheet. Options,
for Neil to pick (§6): (a) add a short sim-runnable "see it" procedure to
L26 for all three presets, no lab sheet; (b) fold presets 4 to 6 into the
L25 lab sheet as a second part, since L25 already has the kit out; (c)
leave 3.8 as practice-only, as it is now.

### D. The Phaser GUI, `livethisdream/phaser` at `main` (2026-10-06)

The lab platform, and it has moved since the August build. Default branch is
now `main` (was `browser-based`). What changed that the labs must absorb:

- **A browser simulator with no install**, hosted at
  `https://livethisdream.github.io/phaser/` and reachable on the Pi with
  `?sim=1`. Same controls and physics as `--sim`. Every lab's "No hardware?"
  frame still says `python phaser_headless.py --sim`; the hosted page is the
  lower barrier and should be the first thing named (link it, never iframe
  it, per CLAUDE.md).
- **Instructor mode works in the browser simulator** (`?sim=1&instructor=1`),
  so the interferer demo no longer needs a Python checkout.
- **A rotating stand** (`hardware/stand/`, PR #23 merged 2026-10-06): manual
  azimuth turntable, 5° detents, ±180° engraved scale, array phase center on
  the axis, provisioned for a stepper later. L23 (pattern measurement) and
  L28 Procedure D (tracking) currently rotate the HB100 or the array by hand.
- **Beam-pattern fix** (`docs/beam-pattern-handoff.md`): the latch and init
  defects that flattened hardware patterns are fixed; the August sim numbers
  were never checked on hardware (open ToDo in the project note).
- **Calibration** and **CTF mode** exist; neither is course material. CTF
  mode could become a Module 5 capstone element but is out of scope here.

The §M3 GUI inventory was written in August. Before touching any lab page,
re-verify every control name in it against `frontend/index.html` on `main`
and amend §M3 where they differ.

## 3. The lesson pass: L17 to L28 in teaching order

One lesson per session, one or two lessons ahead of the calendar (the
standing rule from the present-cut ToDo). L17 is next. For each lesson, in
this order, and `mech_check.sh` at the end of each:

1. **Reconcile against the sources.** Walk the slide map in §2A for the
   lesson; apply the "take" items as content edits or as candidates for step
   5. Check nomenclature against the deck (ours is the source of truth for
   our own names, §M2; the ADI deck is a check that we have not drifted from
   what the GUI's labels say).
2. **`/voice-sweep <NN>`** on page, deck, practice set.
3. **`/why-sweep <NN>`**: mechanisms stated, jargon defined, numbers
   recomputed, links back to L15/L16 and Module 1.
4. **Present cut** to the L07 shape: two to four bullets, a figure, an
   equation chain, or a callout per frame; 40 words a frame, 30 present
   frames a lesson; derivations as one aligned chain; a slide states the
   point. `check_density.py` and `check_frames.py` gate it. L15 (44 to 29
   beats) and L16 (0 to 27) are the module's worked examples.
5. **`/illustration-sweep <NN>`** with the deck's "take" figures as the
   candidate list, each redrawn as a generated SVG or a house widget.
6. Lab lessons only: the lab pass in §4.
7. Site-wide checks once per batch: `check_shell.py`, `check_bar.py`,
   `check_parity.py` against a `main` baseline.

Effort, from the L15/L16 record: three to four sessions per theory lesson,
one more for a lab lesson. Twelve lessons, so roughly 40 sessions; the
calendar sets the pace, not the count.

## 4. The lab pass: L17, L19, L21, L23, L25, L28

Done inside the lesson pass for each lab lesson, after steps 1 to 5:

1. **Re-execute the procedure** on the GUI at `main`, in both simulators
   (`--sim` over WebSocket and the hosted browser page). Fix every control
   name, tab name, and preset that moved. Record what the sweep reads and
   diff it against the §M4 "measured" column; a disagreement is a spec edit
   or a bug report to the Phaser repo, never a silent page edit.
2. **Rewrite the "No hardware?" frame** to name the hosted simulator first
   and `--sim` second, and to say which steps have no sim equivalent (the
   sim target is fixed at boresight).
3. **Decide the stand** (open question below). If it is built for class:
   L23 measures the pattern by turning the array on the stand in 5° detents
   with the HB100 fixed, which is the chamber procedure students already know
   from L11; L28 Procedure D tracks a stand rotation. If not, the
   hand-rotation procedures stay and say so.
4. **Lab sheets**: edit the `.tex` to match the revised Deliverables part,
   rebuild with the real macros, commit the blank only, push the KEY to
   `ece444-faculty/lab-keys/`. Relink from the page only once the blank PDF
   is committed.
5. **Hardware validation day** (one session, all five measurement labs,
   after the pass): run L19/L21/L23/L25/L28 on the real kit with the
   beam-pattern fix in place; reconcile §M4 and the lab-sheet keys where the
   bench disagrees. This closes the open ToDo from August.

## 5. After the lessons

- **M03 assessment** (`ece444-faculty`, branch `claude/module-3-assessment`):
  re-check every question against the revised pages; add the 11.5 GHz
  grating-lobe case and a window-analogy question if L24/L26 gain them.
  Monopulse stays untested (§M7).
- **L20 and the midterm**: the project is due at L20; the page acknowledges
  it in one paragraph and states no date (`635518f`). Keep it that way.
- **COURSE_SPEC.md**: every verbal decision from the pass goes in the same
  turn; the Module 2 lesson was that an unrecorded waiver gets undone by the
  next agent.

## 6. Open questions for Neil

1. **Objective 3.8 hands-on: decided** (Neil, 2026-10-07: "Go with option
   1, add it to the L25 lab sheet"). Done the same day as Lab 8 Part 2,
   Steps (f) to (i) on the L25 page and deck, three sheet questions, every
   step executed against the simulator first; the numbers and the GUI
   quirks it exposed are in `COURSE_SPEC.md` §M7. Note the ordering: L25
   runs before L26, so the part is framed as measure-now, explain-in-L26.
2. **The rotating stand.** Will it be printed and in the classroom this
   term? L23 and L28 Procedure D change shape if so (§4.3).
3. **The hosted simulator.** OK to point students at
   `livethisdream.github.io/phaser` as the pre-lab and no-hardware path? It
   is public and carries the SIMULATION pill, so a synthesized sweep cannot
   be mistaken for a measurement.
4. **The 16-channel MVDR material** (slides 62 to 66). Assumed out of scope
   beyond one "where this is going" line in L28. Say so if you want more.
5. **Teaching order and pace.** Assumed L17 next, one lesson per session,
   one or two ahead of the class. Say so if the calendar needs a different
   order (for example, the theory lessons L18/L20/L22 before their labs in
   a block).

## 7. Assumptions this plan makes

- Nothing from the ADI deck is reproduced as-is: no screenshots, no ADI
  photographs, no ADI block diagrams. Figures are regenerated in the house
  style; the slides are a reference for *what* to draw.
- The existing Module 3 content is kept and refined, not regenerated. The
  present cut and sweeps are the mechanism; the August build is the base.
- The deck's numbers that already live in §M4 are not re-derived here. The
  one rounding difference found (86° vs 86.6° per element at 30°) is the
  deck's, and ours stands.
