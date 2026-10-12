# ECE 444 roadmap and working rules

The plan for Modules 3–5 and the rules every working thread follows. **Read
this before starting any work.** The Integrator thread maintains this file. If
something you need is not here, ask Neil or the Integrator rather than guessing.

Last updated 2026-10-12.

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
| the lesson page | `book/moduleMM/LNN-*/index.md` |
| its practice set | `latex/ECE444_Practice_LNN.tex` and `book/extras/practice/ECE444_LNN_Practice_*.pdf` |
| its lab packet (lab lessons) | `latex/ECE444_Lab_LNN_*.tex` and `book/extras/labs/ECE444_Lab_LNN_*_blank.pdf` |
| its figures | `book/extras/viz/img/LNN-*.svg` and its generator `scripts/graphics/*lNN*` |
| a widget used **only** by this lesson | `book/extras/viz/<widget>.html` |
| its own budget exception | its line in `scripts/verify/budgets.py`, removed when the lesson is cut |
| its lab key | `lab-keys/ECE444_Lab_LNN_*_KEY.pdf` in `ECE444-faculty` |

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

The reveal.js decks are frozen. Nobody edits them (renames by the Integrator
excepted).

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

- **One period is 20 slides** in present mode, 40 words a slide
  (`scripts/verify/budgets.py`).
- **Every cadet has their own kit.** Kits never leave the room, so bench time
  is in class and homework is everything either side of it. Lab measurements
  are individual.
- **Labs are named by lesson**: "L17 Lab", "L19 Lab", never a running lab number.
- **A lab is one packet, one submission, one Gradescope assignment.**
  - *Part 1, Pre-Lab*: individual, before the period.
  - *Part 2, Measurements*: your own kit, in class.
  - *Part 3, Writeup*: after the lab.
  - The packet replaces the lab's own practice set, and the preceding lesson's
    when the pre-lab draws on it. It counts toward engagement as a genuine,
    documented attempt.
- **Objectives** are the syllabus's two-level course objectives, quoted word for
  word.
- **No receiver-course vocabulary** for cadets (mixer, LO, IF, VCO,
  superhet). Hardware limits stay out of the student story.
- **Assessments** never hand students the formula. They live in
  `ECE444-faculty` only.
- **Python only, never MATLAB.** American spelling. No thin spaces.
- **The midterm is done.** Nothing in Modules 3–5 refers to its due date.

## 5. Schedule and status

Status as of 2026-10-12. "Cut" means the lesson fits the 20-slide budget.
"Sweeps" means the voice, why, and illustration passes.

**Module 3: phased arrays (L15–L28)**

| Lesson | Title | Homework | Status | Next |
| :-- | :-- | :-- | :-- | :-- |
| L15 | Aperture Distributions and Efficiency | practice | cut 20/20, sweeps done | ready |
| L16 | The Array Factor and Pattern Multiplication | practice | 29/20, sweeps done | cut |
| L17 | Introduction to Phased Array Hardware | **L17 Lab** | packet built, 14/20 | golden image + hardware dry run |
| L18 | Beam Steering Theory | none (pre-lab of L19 Lab) | 20/20, sweeps done | ready |
| L19 | Beam Steering Lab | **L19 Lab** | packet built, 13/20 | hardware-day checks |
| L20 | Fox Hunt Lab | **L20 Lab** | placeholder | page + packet |
| L21 | Array Factor and Beamwidth Theory | practice | cut 18/20 | sweeps |
| L22 | Antenna Pattern Theory | practice | 37/20 | cut + sweeps |
| L23 | Array Factor and Pattern Lab | **L23 Lab** (old-style sheet) + practice | merged, 18/20 | convert to packet; widget label overlaps at phone width |
| L24 | Sidelobes and Tapering Theory | practice | 46/20 | cut + sweeps |
| L25 | Tapering Lab | **L25 Lab** (old-style sheet) + practice | 46/20 | cut + sweeps + packet |
| L26 | Beam Squint and Quantization | practice | 40/20 | cut + sweeps |
| L27 | Null Steering Theory | practice | 46/20 | cut + sweeps |
| L28 | Null Steering Lab | **L28 Lab** (old-style sheet) + practice | 51/20 | cut + sweeps + packet |

**Module 4: radar (L29–L38).** Placeholder pages. They need the FMCW mode in
the Phaser app, which starts the week of 2026-10-12.

| Lesson | Title |
| :-- | :-- |
| L29 | The Radar Equation, Path Loss, and RCS |
| L30 | Range, Resolution, and Doppler (adds micro-Doppler) |
| L31 | Radar Detection Theory |
| L32 | Introduction to FMCW on Phaser |
| L33 | FMCW Range Lab (range and waterfall) |
| L34 | Range-Doppler and MTI Lab (adds the spectrogram) |
| L35 | CFAR Processing Theory |
| L36 | CFAR Processing Lab |
| L37 | Classification and Tracking |
| L38 | Radar Open Lab (make-up, radar-chain rehearsal) |

**Module 5: final project (L39–L41).** Detect, classify, and track one moving
target; the jammer is out (option A of `MODULE45_BUILDOUT_PLAN.md`). Needs the
project packet and the rubric.

## 6. Work queue, in order

1. **Before L17:** the golden card image and a hardware dry run on a real kit.
2. **L20 Lab**, the fox hunt: page and packet. Plan in
   `MODULE45_BUILDOUT_PLAN.md` §2 and §7.
3. **Lesson passes in teaching order:** L16, then L21–L28, each before it is
   taught. A lab lesson's pass converts its sheet to a packet.
4. **Phaser:** the FMCW radar mode, plus the carrier-frequency fix for the
   continuous-wave mode that is still on an unmerged branch.
5. **Module 4 and 5 build-out**, once the radar mode runs on hardware.
6. **Integrator cleanup:** the syllabus schedule still lists Module 2 in its
   pre-2026-09-12 order (the measurement labs as 13 and 14, not L10 and L11).

## 7. Open decisions (Neil)

- **Gradescope.** One assignment per lab: L17 Lab, L19 Lab, L20 Lab, L23 Lab,
  L25 Lab, L28 Lab. Retire the L17, L18 and L19 practice entries. Neil sets this
  up; nothing in the repo tracks it.
- **L26's practice set covers grating lobes**, which objective 3.8's wording
  does not mention.
- **Image-build homework:** does each kit get a second card, and do cadets have
  Python on their laptops?

## 8. Hardware-day checklist

Things only a real kit can settle:

- which side of the arc reads positive angles
- the peak drop when steering to 30°, measured on the kit
- the Rx Gain level where the receiver starts to compress
- signal level from the transmitter at 3–5 m (fox hunt)
- how much signal the boxes absorb
- interference with many kits running in one room
- the radar's carrier frequency
- a transmit antenna for every kit
