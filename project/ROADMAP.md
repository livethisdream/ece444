# ECE 444 roadmap and working rules

The plan for Modules 3–4 and the rules every working thread follows. **Read
this before starting any work.** The Integrator thread maintains this file. If
something you need is not here, ask Neil or the Integrator rather than guessing.

Last updated 2026-10-25.

## 1. Who does what

Work runs in parallel threads (sessions). Each one has a role.

- **Integrator** (one thread). Owns this roadmap, the course-wide files, and the
  order things merge in. It checks every other thread's PR against this
  roadmap and keeps `main` clean. It does not write lesson content.
- **Lesson thread** (one per lesson pass, e.g. "L22 sweep"). Owns one lesson
  and nothing else: its page, its problems, its lab packet, its figures. It
  works on one branch and opens one PR.
- **Phaser thread** (the radar app, GUI changes). Owns the `livethisdream/phaser`
  repo only. It never edits the course repo; a lesson thread updates the
  course pages once a Phaser change has merged.
- **Neil** decides content, merges, and settles anything this file marks open.

## 2. Who may touch what

A lesson thread for lesson NN may edit **only**:

| What | Path |
| :-- | :-- |
| the lesson page and its lab page | `book/moduleMM/LNN-*/index.md` (the lab is `LNN-lab-*`; in Module 4 the lab is on the lesson page) |
| its practice set, and its lab's | `latex/ECE444_Practice_LNN.tex` (`_LNNLab.tex`) and `book/extras/practice/ECE444_LNN_Practice_*.pdf` (`LNNLab`) |
| its lab packet | source `ECE444_Lab_LNN_*.tex` in `ECE444-faculty` (it holds the answers; Neil, 2026-10-23), and the blank `book/extras/labs/ECE444_Lab_LNN_*_blank.pdf` here |
| its figures | `book/extras/viz/img/LNN-*.svg` and its generator `scripts/graphics/*lNN*` |
| a widget used **only** by this lesson | `book/extras/viz/<widget>.html` |
| its own budget exception | its line in `scripts/verify/budgets.py`, removed when the lesson is cut |
| its lab key | `lab-keys/ECE444_Lab_LNN_*_KEY.pdf` in `ECE444-faculty`, written there by its `build_lab.sh` |

Everything else belongs to the Integrator. A lesson thread that needs any of
these changed lists the change under **"For the Integrator"** in its PR body
and does not make it:

- `book/syllabus.md`, `book/intro.md`, `book/materials.md`, the module index pages
- `COURSE_SPEC.md`, `CLAUDE.md`, `VOICE.md`, everything in `project/`
- `scripts/scaffold_lessons.py`, `book/_toc.yml`, `scripts/verify/`
  (budgets aside, as above), `book/_ext/`, `book/_templates/`, `book/_static/`
- a widget or figure generator used by more than one lesson
- another lesson's files, even for a one-word fix
- lesson numbers, titles, objectives, lab names, the schedule
- assessments in `ECE444-faculty`

There are no separate slide decks (Neil, 2026-10-23: the reveal.js decks were
retired). A frame lesson is its own slides; printing it from present mode is
the slide handout. Don't create, cite, or mirror changes into a deck.

`book/interactives.md` is generated. A lesson thread that adds or renames a
widget re-runs `python3 scripts/build_interactives.py` and commits the result.
That is the one shared file it may change.

## 3. How a lesson thread works

1. Branch from current `main` as `claude/lNN-<topic>`. Never stack on another
   thread's branch.
2. Read `CLAUDE.md`, `COURSE_SPEC.md`, `VOICE.md`, and this file.
3. Do the work. Before opening the PR, all of these pass for the lesson:
   `jupyter-book build book/ --all` with 0 warnings; `check_density.py LNN`;
   `check_frames.py LNN`; `mech_check.sh`; PDFs built with the real macros in
   Barlow, no overfull boxes.
4. Open one PR. In the body, list what changed, the checks, and a **"For the
   Integrator"** section (write "None" if empty).
5. Do not merge. The Integrator checks the diff stays inside section 2, then
   Neil (or the Integrator, on Neil's word) merges.

## 4. Rules that are settled

- **Lessons are topics, not periods** (Neil, 2026-10-13: "do the lesson in the
  time it takes, then do the lab"). A lab is a child page of its lesson,
  `LNN-lab-<slug>`, titled "LNN Lab — <Topic>", never a lesson of its own.
  Project days and open-lab time are calendar. Modules 1-2 keep their numbers.
  **Module 4 is the exception** (Neil, 2026-10-25): the L28–L31 Labs sit on
  their lesson's own page, lesson first, then the lab, with no `LNN-lab-*`
  page. The lab keeps its name ("L28 Lab") and its packet.
- **A lesson page is at most 20 slides** in present mode, 40 words a slide
  (`scripts/verify/budgets.py`); a lab page's pre-bench frames count against
  the same budget.
- **Every cadet has their own kit.** Kits never leave the room, so bench time
  is in class and homework is everything either side of it. Lab measurements
  are individual, with one exception: the **L19 Lab fox hunt runs in teams of
  two**, one packet per team, run as a firing range (2026-10-23): one kit per
  team on a taped firing line, bearings from its station marks. The **final project is individual** (Neil, 2026-10-13).
- **Labs are named by lesson**: "L17 Lab", "L18 Lab", never a running lab number.
  One lab serves two lessons: the **L22–L23 Lab** (tapering, then grating
  lobes, squint, and quantization) runs after L23 and hangs off it
  (Neil, 2026-10-13); L22 has no lab of its own.
- **A lab is one packet, one submission, one Gradescope assignment.**
  - *Part 1, Pre-Lab*: individual, before the period.
  - *Part 2, Measurements*: your own kit, in class.
  - *Part 3, Writeup*: after the lab.
  - The packet replaces the lab's own practice set, and its lesson's when the
    pre-lab draws on it. A **Module 3** packet counts toward engagement as a
    genuine, documented attempt.
  - **The Module 4 packets (L28–L31 Labs) are the scaffolding for the final
    project** (Neil, 2026-10-15): one report, in the cadet's own words, on
    the radar hardware and processing, 30% of the course on one rubric with a
    sliding scale. Packets are checked and returned with feedback; they are
    neither engagement credit nor the project itself, and the report must not
    be a restatement of them. Each packet ends by naming what the cadet
    carries into the report. Extra credit: a unique extension, proposed and
    approved in advance. **Due dates** (Neil, 2026-10-15): the
    packets come due in sequence from class period 32, and the report
    at class period 41. Periods are calendar meetings, not site lesson
    numbers; each packet states its own date.
  - **The L28–L31 Labs build on each other.** Each lab pass writes its packet
    to start from the cadet's own code and data from the lab before (L29 from
    the L28 range code, L30 runs CFAR on the L29 maps, L31 classifies the L30
    detections) and says what to keep for the next one.
  - **A lab's problems are the lab** (Neil, 2026-10-13: "shouldn't we just
    call them labs?"). No new `LNNLab` practice sets. The existing ones (L20,
    L21, L22 for the L22–L23 Lab, L24) fold into their packet's Pre-Lab and
    Writeup in that lab's lesson pass, and then come off the site.
- **Objectives** are the syllabus's two-level course objectives, quoted word for
  word.
- **No receiver-course vocabulary** for cadets (mixer, LO, IF, VCO,
  superhet). Hardware limits stay out of the student story. One exception
  (Neil, 2026-10-21): **IF characterization** is a necessary step, so a lab
  may name the GUI's Characterize IF button and the IF it measures, with
  the IF defined once in plain words at first use.
- **Assessments** never hand students the formula. They live in
  `ECE444-faculty` only.
- **Python only, never MATLAB.** American spelling. No thin spaces.
- **The midterm is done.** Nothing in Modules 3–4 refers to its due date.
- **There is no Module 5** (Neil, 2026-10-15). Objectives 5.2 and 5.3 are now
  4.8 and 4.9; 5.1 and 5.4 are dropped. The capstone is parked in
  `project/FINAL_PROJECT_CAPSTONE.md`.

## 5. Schedule and status

Status as of 2026-10-23. "Cut" means the page fits the 20-slide budget.
"Sweeps" means the voice, why, and illustration passes. Lessons are topics,
not periods; each lab follows its lesson on the bench and is listed under it.

**Module 3: phased arrays (L15–L24)**

| Lesson | Title | Homework | Status | Next |
| :-- | :-- | :-- | :-- | :-- |
| L15 | Aperture Distributions and Efficiency | practice | cut 20/20, sweeps done; tagline callout and "you are here" strip (#109) | ready |
| L16 | The Array Factor and Pattern Multiplication | practice | cut 20/20, sweeps done, two-element widget (#92, #93, #98) | ready |
| L17 | Introduction to Phased Array Hardware | none (L17 Lab packet) | 15/20; calibration frames and Calibrate widget (#105) | ready |
| L17 Lab | Phased Array Bring-Up | **L17 Lab** packet | 18/20; hardware dry run 2026-10-19 on phaser-00, fixes merged (#118, #121) | ready |
| L18 | Beam Steering | none (pre-lab of the L18 Lab) | 20/20, sweeps done | ready |
| L18 Lab | Beam Steering | **L18 Lab** packet | 14/21; dry run 2026-10-19, fixes merged (#110, #121): E1 side, 45° marker, scan loss at 1.2 m | ready |
| L19 | Direction Finding | none (L19 Lab packet) | rewritten (#103), 19/20, fix widget (#123); voice, why and illustration sweeps (#151) | ready |
| L19 Lab | Fox Hunt | **L19 Lab** packet, one per team | firing range: 3.0 m line, 5 stations 0.75 m apart (Neil, 10-25), 2.0 m × 1.0–2.0 m box field; starter script; 8/20 | hardware-day checks |
| L20 | Array Factor and Beamwidth | practice | 18/20, sweeps done (#128) | ready |
| L20 Lab | Array Factor | **L20 Lab** packet (`68f9454`, 2026-10-22); L20Lab practice set retired | 11/20; dry-run fixes merged (#122): set the level, own frequency, ~5 dB steps | ready |
| L21 | Antenna Pattern | practice | cut 20/20, sweeps done (#127) | ready |
| L21 Lab | Antenna Pattern | **L21 Lab** packet: walk the HB100, then rotate the kit at 1.2 m, both held beams read from one sweep pass | 13/20 (#127); rotation dry-run 2026-10-23; walk validated 2026-10-25 (sidelobes 11.5 / 14.8 dBc, floor 25–30 dBc) | ready |
| L22 | Sidelobes and Tapering | practice | cut 20/20; voice, why and illustration sweeps done (#132, #137, #142) | ready |
| L23 | Beam Squint and Quantization | practice | cut 20/20, all three sweeps, ten figures and a reworked squint widget (#131) | ready |
| L22–L23 Lab | Tapering, Squint, and Quantization (one lab for both lessons, after L23) | **L22–L23 Lab** packet (#131, faculty #34); dry-run lessons folded in | 12/20; preset-6 walk validated on phaser-00 2026-10-25 | ready |
| L24 | Null Steering | practice | cut 20/20 (#148), voice, why and illustration sweeps (#149) | ready |
| L24 Lab | Null Steering | **L24 Lab** packet (faculty #38); L24Lab practice set retired | 14/20, dry-run findings applied (#149) | all four procedures run on phaser-00 2026-10-25 (A, B, D angles and loss validated; nulls room-limited to about −22 dB in a cramped space) | ready |

**Module 4: radar (L25–L31) and the final project.** Placeholder pages.
L25–L27 are taught in class; L28–L31 are the final project, each one page
with its lesson and then its lab. The FMCW mode in the Phaser app is in
progress (Neil); build the lessons and labs now **assuming it works**, and
reconcile with the GUI when it lands. Source: ADI's Phaser radar labs
(Neil, 2026-10-25: newer than the slide deck), public at
`analogdevicesinc.github.io/system-level/solutions/platforms/phaser/labs/`,
source in `analogdevicesinc/system-level` under
`docs/solutions/platforms/phaser/labs/`: `radar-setup`, `radar-cw`,
`radar-fmcw`, `chirp-sync`, `radar-doppler`, `radar-mti`, `radar-cfar`,
with Python scripts in `resources/python/` (the docs host is blocked in
these containers; clone the repo sparse). Cite and link them; translate
any MATLAB to Python. They have no micro-Doppler, classification, or
tracking lab (L31 is ours), and the recorded drone data their MTI lab
plays is not in the repo, so the recorded-data fallback is ours too. The L28–L31 Labs scaffold the final project report, so each needs a packet
and a recorded-data fallback in case a bench FMCW capture fails; the report
needs its rubric, published with the L28 Lab packet.

| Lesson | Title |
| :-- | :-- |
| L25 | The Radar Equation, Path Loss, and RCS |
| L26 | Range, Resolution, and Doppler (adds micro-Doppler) |
| L27 | Radar Detection |
| L28 | FMCW on the Phaser, with the L28 Lab: FMCW Range (range and waterfall) |
| L29 | Range-Doppler and MTI, with the L29 Lab (adds the spectrogram) |
| L30 | CFAR Processing, with the L30 Lab |
| L31 | Classification and Tracking, with the L31 Lab: Micro-Doppler Spectrogram |
| Final Project | Radar Systems Report: one report on the L28–L31 Labs, in the cadet's words (`module04/final-project`) |

**Module 4 outlines** (Neil approved, 2026-10-25). Each lesson thread writes
to its outline; ADI pages are named by their slug under `labs/`. Across
all of them: Python only, the GUI's own FMCW settings (ADI's scripts
disagree: 12.145 GHz in FMCW, 9.9 GHz in range-Doppler), ADI cited and
linked, never copied, and no receiver vocabulary (the beat frequency is
"the echo compared with the chirp still going out").

- **L25 Radar Equation, Path Loss, and RCS** (4.1, taught). Friis twice
  (from L02), so 1/R⁴; RCS of a sphere, a plate and a corner reflector, and
  its aspect dependence; kTB and SNR; the Phaser link budget for a corner
  reflector at a few meters. Practice set; radar-equation widget.
- **L26 Range, Resolution, and Doppler** (4.2, taught). Range from delay,
  unambiguous range, resolution c/2B, Doppler 2v/λ and its sign; pulsed vs
  CW (`radar-setup`); the CW fan demo (`radar-cw`: speed but no range);
  micro-Doppler introduced. Practice set.
- **L27 Radar Detection** (4.3, taught). A threshold against noise; PD vs
  PFA; the SNR a detection needs (Albersheim); dwell and pulse integration;
  why a fixed threshold fails, which sets up CFAR. Practice set; a threshold
  widget on the noise and target densities.
- **L28 FMCW on the Phaser + L28 Lab** (4.2, 4.4, 4.5; `radar-fmcw`).
  Lesson: the chirp, f_b = 2RB/(cT_s), resolution and the range the sample
  rate allows, the range FFT and windowing, the 0 m calibration. Lab: OUT2
  transmit antenna and calibration; corner reflector at 1, 2, 3 m and the
  kHz per meter; predict, then measure, B = 250 MHz and T_s = 1 ms; the
  waterfall; the cadet's own Python range FFT from a saved capture, kept
  for L29. The report rubric and the recorded-data fallback ship with it.
- **L29 Range-Doppler and MTI + L29 Lab** (4.5, 4.6; `chirp-sync`,
  `radar-doppler`, `radar-mti`). Lesson: chirp sync as "every chirp starts
  at a known time", fast and slow time, the data matrix and 2D FFT,
  velocity resolution λ/(2M·PRI) and maximum λ/(4·PRI), the 2- and 3-pulse
  cancellers, their response and blind speeds. Lab: range-Doppler from the
  cadet's L28 code; a hand and a fidget spinner; vary the chirp count and
  bandwidth; MTI none, 2-pulse, 3-pulse; one range bin's spectrogram,
  kept for L31. Recorded-data fallback is ours (ADI's drone file is not
  in their repo).
- **L30 CFAR Processing + L30 Lab** (4.7; `radar-cfar`). Lesson: cell
  averaging with guard and reference cells, the bias from PFA, greatest-
  and smallest-of, edges, 2D CFAR on the range-Doppler map. Lab: CFAR on
  the cadet's L29 maps; tune; measure the false-alarm rate and PD against
  L27; detection lists kept for L31. CFAR widget.
- **L31 Classification and Tracking + L31 Lab** (4.8, 4.9; ours, no ADI
  page). Lesson: micro-Doppler physics (blades, limbs), spectrogram
  trade-offs, features (Doppler spread, periodicity, centroid), a simple
  classifier, the confusion matrix; alpha-beta range tracking and monopulse
  angle (from L24). Lab: fan, spinner, walker, hand; classify the L30
  detections and report the accuracy; **Part B tracks a walker (dismount)
  in range and angle** (Neil, 2026-10-27), which is where 4.8 is measured.
- **Shared code contract** (2026-10-27, so the labs chain though written in
  parallel). One cadet module, `radar_lab.py`, grows lab by lab; one capture
  format, an `.npz` with `iq` (complex, `n_chirps × n_samples`), `fs`, `fc`,
  `B`, `T_ramp`, `PRI`, `f0` (the 0 m frequency). L28: `load_capture`,
  `range_axis`, `range_profile`, `waterfall`. L29: `range_doppler`, `mti`.
  L30: `cfar_2d(rd_map, guard, ref, bias_db)` → detection map and
  `[(range_m, vel_mps, snr_db), ...]`. L31: `spectrogram`, features, a
  classifier, `alpha_beta`. The recorded-data fallback is
  `scripts/radar/fmcw_sim.py` and `book/extras/radar-data/`, created by the
  L28 thread; later labs ask the Integrator to extend them.
- **Passes.** L28 is written whole (lesson, lab, packet, fallback); L29–L31
  get their lesson halves first, and their labs in a second pass once the
  lab before them has merged.
- **Final project.** Each lab ends with what it carries into the report.
  Everything is submitted on Gradescope. **Rubric** (Neil, 2026-10-27):
  Labs Completed, Engineering Analysis, Report Quality, Extra Effort, each
  0–5, 5 outstanding (on `final-project`). **Report due 11 Dec**
  (Neil, 2026-10-27). **Open, Neil:** the packet dates (given as 9, 16 and
  23 Nov, three dates for four packets), whether Extra Effort is the
  approved-extension extra credit, and the cap (5% proposed). The corner reflector's size is still open: no lab step may
  need one per kit, and the cadet stands clear of the beam.

## 6. Work queue, in order

1. **Lesson passes in teaching order:** L22–L24 with the L22–L23 and L24
   Labs, each before it is taught. The three sweeps are user-invoked only:
   Neil types `/voice-sweep NN` (then why, then illustration) in the lesson
   thread's own session; a thread cannot start them or replay them by hand. A lesson's pass converts its lab's sheet to a
   packet and folds in the dry-run lessons (`review/M3_LAB_DRYRUN.md`):
   set the level to −10 dBFS, compute at the kit's own Find HB100
   frequency, open Lab Presets first, E1 on the right facing the patches,
   level comparisons at 1.2 m or more. Two Phaser changes ride along:
   the readouts are now **Angle** (Peak/Centroid) and **Peak Gain**, not
   "Est. Angle" and "Peak Array Gain" (still stale in L24), and preset 6 Quantization now holds the beam at 15° with
   Blackman for a Signal vs Time walk (phaser #48). The second dry run
   (`review/M3_LAB_DRYRUN_2026-10-23.md`, all of L17–L24) adds, for the
   remaining passes:
   - **L24 Lab** (done in #149 but Procedure C): notches and nulls reach −40 to −50 dB, so the
     "floor-limited at −21 dB" explanation goes, in the text and in
     `L24-quant-depth.svg`; Procedure D sets a uniform
     taper and resets Beam 1 Phase until preset 8 does; Procedure C runs at
     +20° only, against Neil's software interferer, with the expected
     suppression filled in from his first run, and its "No hardware?" note
     updated.
2. **Phaser (Neil's Phaser thread):** linearize the Element Gains slider
   with a measured lookup table (amplitude goes as (%/100)^0.68 today, the
   ADAR1000 register response; Neil, 2026-10-23: fix it in software, not in
   the labs); preset 8 loads uniform and resets Beam 1
   Phase; Signal BW and Rx Gain survive Calibrate, Find HB100 and the Rect
   preset; restart the sweep after Find HB100. Phaser #55 (2026-10-25 bench
   run): MVDR output on Manual's scale (the "lost target" was 6 dB of
   scaling), interferer and MVDR settings survive Calibrate, interferer
   readout follows HB100 drift. From the 2026-10-25 L24 run: preset 8
   resets Beam 1 Phase but not the taper; the error function jumps around
   boresight; and every null (notch, difference, delta) bottomed at −34 to
   −36 dBFS with the HB100 tone still in it, most likely room reflections
   in a cramped space, but worth ruling out leakage on an open bench. The 3- and 4-bit lobes in the old
   quantization sweep sit above even the worst-case simulation of rounding
   the steering ramp, and Angle shifted +8.4° at 4 bits and below: does the
   kit also round its calibration offsets? Evidence (2026-10-25, phaser-00):
   the preset-6 walk, beam held at 15°, read the floor (−17 to −19 dBc) at
   4 and 3 bits where the 10-23 sweep read −15.5 and −12.0 dBc, and its
   2-bit lobe was −10.1 dBc near −53° against the sweep's −8.5. Open from the dry run: why array
   peaks read 1–3 dB under the in-phase sum of single elements even with
   elements fully on or off; whether each channel's phase moves with its
   gain setting; whether recalibrating with the source exactly at boresight
   removes the +1–2° offset.
3. **Phaser:** the FMCW radar mode, plus the carrier-frequency fix for the
   continuous-wave mode that is still on an unmerged branch.
4. **Module 4 build-out**, now, assuming the radar mode works (Neil,
   2026-10-25); hardware numbers are reconciled when it runs: L25–L27
   taught in class, then the L28–L31 Labs as the final project's scaffolding,
   each packet built to start from the lab before it, plus the report rubric.

## 7. Open decisions (Neil)

- **Gradescope.** One assignment per lab: the L17, L18, L19, L20, L21,
  L22–L23, and L24 Labs. Retire the L17 and L18 practice entries and the old L19
  (Beam Steering Lab) one. Neil sets this
  up; nothing in the repo tracks it.
- **Image-build homework:** does each kit get a second card, and do cadets have
  Python on their laptops? The L17 Lab rewrite (#96) has cadets build their own
  card in class, which may settle this.

## 8. Hardware-day checklist

Before class, on every kit and bench (from the 2026-10-23 dry run):

- re-run `install.sh`, so the dashboard has Signal vs Time (L21 walk) and
  Tracking (L24 Procedure D), and later the gain-slider fix and interferer
- a stand at box height (L19) and the kit clamped or keyed to its
  protractor (L21; the dry-run kit slid 5°)
- ±40° either side of broadside clear of walls and people, the HB100 at
  least 1.2 m out (a wall put a false lobe 9 dB below the peak)

Things only a real kit can settle:

- which side of the arc reads positive angles
- the peak drop when steering to 30°, measured on the kit
- the Rx Gain level where the receiver starts to compress
- signal level from the transmitter at 3–5 m (fox hunt)
- how much signal the boxes absorb
- interference with many kits running in one room
- the radar's carrier frequency
- a transmit antenna for every kit
