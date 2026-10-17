# ECE 444 roadmap and working rules

The plan for Modules 3–4 and the rules every working thread follows. **Read
this before starting any work.** The Integrator thread maintains this file. If
something you need is not here, ask Neil or the Integrator rather than guessing.

Last updated 2026-10-17.

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
| the lesson page and its lab page | `book/moduleMM/LNN-*/index.md` (the lab is `LNN-lab-*`) |
| its practice set, and its lab's | `latex/ECE444_Practice_LNN.tex` (`_LNNLab.tex`) and `book/extras/practice/ECE444_LNN_Practice_*.pdf` (`LNNLab`) |
| its lab packet or sheet | `latex/ECE444_Lab_LNN_*.tex` and `book/extras/labs/ECE444_Lab_LNN_*_blank.pdf` |
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

- **Lessons are topics, not periods** (Neil, 2026-10-13: "do the lesson in the
  time it takes, then do the lab"). A lab is a child page of its lesson,
  `LNN-lab-<slug>`, titled "LNN Lab — <Topic>", never a lesson of its own.
  Project days and open-lab time are calendar. Modules 1-2 keep their numbers.
- **A lesson page is at most 20 slides** in present mode, 40 words a slide
  (`scripts/verify/budgets.py`); a lab page's pre-bench frames count against
  the same budget.
- **Every cadet has their own kit.** Kits never leave the room, so bench time
  is in class and homework is everything either side of it. Lab measurements
  are individual, with one exception: the **L19 Lab fox hunt runs in teams of
  two**, one packet per team, measured from anywhere outside the keep-out zone
  (no stations). The **final project is individual** (Neil, 2026-10-13).
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
  superhet). Hardware limits stay out of the student story.
- **Assessments** never hand students the formula. They live in
  `ECE444-faculty` only.
- **Python only, never MATLAB.** American spelling. No thin spaces.
- **The midterm is done.** Nothing in Modules 3–4 refers to its due date.
- **There is no Module 5** (Neil, 2026-10-15). Objectives 5.2 and 5.3 are now
  4.8 and 4.9; 5.1 and 5.4 are dropped. The capstone is parked in
  `project/FINAL_PROJECT_CAPSTONE.md`.

## 5. Schedule and status

Status as of 2026-10-17. "Cut" means the page fits the 20-slide budget.
"Sweeps" means the voice, why, and illustration passes. Lessons are topics,
not periods; each lab follows its lesson on the bench and is listed under it.

**Module 3: phased arrays (L15–L24)**

| Lesson | Title | Homework | Status | Next |
| :-- | :-- | :-- | :-- | :-- |
| L15 | Aperture Distributions and Efficiency | practice | cut 20/20, sweeps done; opening reworked (#91) | trim frame 6, "Key Point: Shape and Size", 8 px over on a phone |
| L16 | The Array Factor and Pattern Multiplication | practice | cut 20/20, sweeps done, two-element widget (#92, #93, #98) | ready |
| L17 | Introduction to Phased Array Hardware | none (L17 Lab packet) | 12/20 | ready |
| L17 Lab | Phased Array Bring-Up | **L17 Lab** packet | cadets build their own kit from stock Kuiper, 17/20 (#96, #97) | hardware dry run |
| L18 | Beam Steering | none (pre-lab of the L18 Lab) | 20/20, sweeps done | ready |
| L18 Lab | Beam Steering | **L18 Lab** packet | packet built, 13/20 | hardware-day checks |
| L19 | Direction Finding | none yet | shell, 5/20 | page + problems |
| L19 Lab | Fox Hunt | **L19 Lab** packet | placeholder | Neil is adding the fox hunt |
| L20 | Array Factor and Beamwidth | practice | cut 18/20 | sweeps |
| L20 Lab | Array Factor | **L20 Lab** (old-style sheet) + practice | 11/20 | convert to packet; widget label overlaps at phone width (from the merged lab) |
| L21 | Antenna Pattern | practice | 37/20 | cut + sweeps |
| L21 Lab | Antenna Pattern | **L21 Lab** (old-style sheet) + practice | 12/20 | convert to packet |
| L22 | Sidelobes and Tapering | practice | 46/20 | cut + sweeps |
| L23 | Beam Squint and Quantization | practice | 40/20 | cut + sweeps |
| L22–L23 Lab | Tapering, Squint, and Quantization (one lab for both lessons, after L23) | **L22–L23 Lab** (old-style sheet) + practice | 46/20, uncut | cut + sweeps + packet |
| L24 | Null Steering | practice | 46/20 | cut + sweeps |
| L24 Lab | Null Steering | **L24 Lab** (old-style sheet) + practice | 51/20 | cut + sweeps + packet |

**Module 4: radar (L25–L31) and the final project.** Placeholder pages. They
need the FMCW mode in the Phaser app (Neil is building it, with the lab
packets). The L28–L31 Labs scaffold the final project report, so each needs a packet
and a recorded-data fallback in case a bench FMCW capture fails; the report
needs its rubric, published with the L28 Lab packet.

| Lesson | Title |
| :-- | :-- |
| L25 | The Radar Equation, Path Loss, and RCS |
| L26 | Range, Resolution, and Doppler (adds micro-Doppler) |
| L27 | Radar Detection |
| L28 | FMCW on the Phaser |
| L28 Lab | FMCW Range (range and waterfall) |
| L29 | Range-Doppler and MTI |
| L29 Lab | Range-Doppler and MTI (adds the spectrogram) |
| L30 | CFAR Processing |
| L30 Lab | CFAR Processing |
| L31 | Classification and Tracking |
| L31 Lab | Micro-Doppler Spectrogram |
| Final Project | Radar Systems Report: one report on the L28–L31 Labs, in the cadet's words (`module04/final-project`) |

## 6. Work queue, in order

1. **Before L17:** a hardware dry run of the stock-Kuiper bring-up on a real kit.
2. **L19**, direction finding: page and problems. The **L19 Lab**, the fox
   hunt, is Neil's (2026-10-17). Plan in `MODULE45_BUILDOUT_PLAN.md` §2 and §7.
3. **Lesson passes in teaching order:** L20–L24 with their labs,
   each before it is taught. A lesson's pass converts its lab's sheet to a
   packet.
4. **Phaser:** the FMCW radar mode, plus the carrier-frequency fix for the
   continuous-wave mode that is still on an unmerged branch.
5. **Module 4 build-out**, once the radar mode runs on hardware: L25–L27
   taught in class, then the L28–L31 Labs as the final project's scaffolding,
   each packet built to start from the lab before it, plus the report rubric.

## 7. Open decisions (Neil)

- **Gradescope.** One assignment per lab: the L17, L18, L19, L20, L21,
  L22–L23, and L24 Labs. Retire the L17 and L18 practice entries and the old L19
  (Beam Steering Lab) one. Neil sets this
  up; nothing in the repo tracks it.
- **L23's practice set covers grating lobes**, which objective 3.8's wording
  does not mention.
- **Image-build homework:** does each kit get a second card, and do cadets have
  Python on their laptops? The L17 Lab rewrite (#96) has cadets build their own
  card in class, which may settle this.
- **Frozen decks.** #91 edited the L15 deck to drop the stale midterm date.
  Keep the decks frozen, or allow edits that keep a deck in step with its
  lesson?

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
