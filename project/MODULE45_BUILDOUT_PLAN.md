# Modules 4 and 5 build-out plan: the fox hunt and the final project

Written 2026-10-10 from Neil's two asks that day (a fox-hunt period, and a
final project that is "still in flux, but I'm thinking target detection and
classification and tracking using the phaser"), the Module 4 and 5 shells,
`scripts/scaffold_lessons.py`, the Phaser repo at `main` (`0824259`) and its
unmerged radar branch, and the ADI workshop labs PDF (internal reference,
paraphrased here, never copied). A working note: decisions go into
`COURSE_SPEC.md` and `project/ECE444_PROJECT.md` the same turn. Every number
was computed in Python; **(unverified)** marks what a container cannot check.

## 1. Where Modules 4 and 5 stand

L29 to L41 are 20-line shells (objectives block, "under construction"), each
with a frozen 39-41-line deck shell that gets no work (§M7); no practice
sets, packets, or widgets. The current list: theory L29-L32 (4.1-4.4), labs
L33-L36 (4.2, 4.5, 4.5, 4.6), CFAR theory and lab L37-L38 (4.7), project
L39-L41 (5.1, 5.1, 5.2-5.4). §4 gives the list under this plan.

**The platform, verified in the Phaser repo:**

- `main` has the beamforming GUI and a **CW Doppler radar** mode
  (`phaser_cw_radar.py`, `frontend-radar/`: velocity spectrum and waterfall).
  On `main` that mode never programs the Phaser's LO, so its velocities are
  computed against a carrier the board is not using; the fix sits on the
  unmerged branch `claude/radar-capability-ophmxc` (last commit 2026-09-04).
- **The headless app has no FMCW mode** (`git grep -i fmcw` on `main` finds
  only notes). The same unmerged branch adds the FMCW DSP (range,
  range-Doppler, MTI, CA-CFAR) and an FMCW simulator, tested in software. The
  hardware half (ADF4159 ramp, chirp-synchronized capture, a GUI mode) is
  "Phase C" and does not exist.
- The ADI workshop runs its radar labs (pp. 29-38) through ADI's own Python
  scripts on the Pi desktop, with a transmit antenna on OUT2 and a corner
  reflector about 1 m out. It has no tracking lab beyond monopulse (p. 28)
  and no classification beyond waving a hand or a fidget spinner at the
  range-Doppler display.

**So Module 4's labs (L33-L38) need an FMCW mode the course GUI does not
have yet,** whatever Neil decides about the project (Decision 6).

## 2. The fox hunt

One HB100 (10.525 GHz nominal, free-running) is on, inside one of several
boxes; every other HB100 is off. Each kit measures a bearing with the beam
sweep (Est. Angle, the L19 skill), and bearings from kits at known positions
and headings intersect at the box.

### 2.1 Placement

The course stays at 41 periods, so the fox hunt takes a slot from something.

| Option | Where | What it displaces | Renumbering |
| :-- | :-- | :-- | :-- |
| **1** | New **L29 Fox Hunt Lab**, end of Module 3 | **L33 and L34 merge** into one FMCW Range Lab (4.2, 4.5). ADI runs them as one lab (pp. 30-32): the waterfall is the same capture plotted over time | L29-L34 shift by one (6 folders) |
| 2 | New L29 Fox Hunt Lab | **L37 CFAR Theory and L38 CFAR Lab merge** | L29-L37 shift (9 folders) |
| 3 | Fox hunt takes the **L39** slot | The kickoff becomes a read-only frame in L38 plus the packet; the project keeps L40-L41 | one slug renamed |

**Recommend option 1.** The fox hunt uses only Module 3 skills, so it ends
Module 3, ten periods after L19 instead of twenty. The merge follows the
source lab's own boundary, drops no content, and moves FMCW one period later,
which helps the Phase C schedule. Option 2 thins CFAR, the step the Module 4
index says "the capstone leans on hardest"; option 3 takes a period from a
project that needs more of them. Option 1 touches the `LESSONS` manifest
(then regenerate the TOC), the Module 3 and 4 index cards, the syllabus
schedule, §M1, six `git mv`s, and `mech_check.sh` (the fox hunt is the first
lesson with no deck, which triggers §M7's "deck gate if present").

### 2.2 Sizing the physics

**Bearing error.** L19's budget, on the pilot branch
`claude/l19-lab-packet-pilot` (not yet on `main`, where L19 still says 2.5°
with a drift term): grid half-step 0.53° at 30°, arc and aim 1.5°, multipath
1.0°, RSS 1.9°. In the hunt, "arc and aim" becomes the **kit heading
reference**, how well each array's broadside is known in the room frame:
1.0° (array edge on a taped heading line) gives √(0.53² + 1.0² + 1.0²) =
1.5°; 1.5° gives 1.9°; 3.0° (by eye) gives 3.2°. The grid step is one
2.8125° LSB over kd = 176.9°, 0.0159 in sin θ: 0.91° at 0°, 1.05° at 30°,
1.29° at 45°. Keep the box field within ±30° of each kit's broadside.

**A reference shot catches blunders; it does not shrink the budget.**
Measuring a source at a surveyed point moves the shot's own grid and
multipath error into the heading, √(0.46² + 1.0²) = 1.1°, no better than a
taped line. It does catch a mirrored bearing (the + side is still a
hardware-day item from L19), which at 30° is a 60° error, and a kit placed
5-10° off.

**Cross-range** is R·tan σ: at σ = 2°, 0.10 m at 3 m, 0.14 m at 4 m, 0.17 m
at 5 m. **Crossing angle**, kits 4 m from the box, σ = 2°, least-squares
covariance (each bearing adds n nᵀ/(Rσ)²):

| Geometry | RMS fix error | Ellipse semi-axes |
| :-- | :-- | :-- |
| 2 kits, 90° crossing | 0.20 m | 0.14, 0.14 m |
| 2 kits, 30° | 0.39 m | 0.10, 0.38 m |
| 2 kits, 15° | 0.76 m | 0.10, 0.76 m |
| 3 kits over 120° | 0.16 m | 0.11, 0.11 m |

The long axis grows as 1/sin γ; students compute that in the pre-lab.

**Box spacing.** Monte Carlo, 4 boxes in a row, fix assigned to the nearest
box; probability of naming the right one at σ = 2° / 3°:

| Spacing | 2 kits at 90° | 3 kits over 120° |
| :-- | :-- | :-- |
| 0.30 m | 0.73 / 0.52 | 0.81 / 0.62 |
| 0.50 m | 0.93 / 0.78 | 0.97 / 0.86 |
| 0.75 m | 0.99 / 0.93 | 1.00 / 0.97 |
| 1.00 m | 1.00 / 0.99 | 1.00 / 1.00 |

**Boxes at least 0.75 m apart**, 1 m if headings are set by eye. Two kits
crossing at 30° scored 0.98 at 0.5 m in this layout, because their long
error axis ran across the row: a good pre-lab design question.

**Elevation.** A horizontal line array measures the cone angle, sin θ_meas =
sin(az)·cos(el). A box on the floor 0.75 m below a tabletop kit at 3 m
(el = 14.0°) reads 29.0° for 30° and 43.3° for 45°. **Put the boxes on
tables at array height.**

**Far field** 2D²/λ = 2(0.112)²/0.0285 = 0.88 m, so 3-5 m is far field.
**Cardboard** at normal incidence (εr 1.2-3, tan δ 0.05-0.1, 4-7 mm walls):
0.2 to 1.8 dB of loss, near transparent if dry and unprinted; the material
values are textbook ranges **(unverified for Neil's boxes)**. Put an unpowered
HB100 in each decoy so weight gives nothing away.

**Link at 3-5 m.** Free-space loss at 10.525 GHz is 52.9 dB at 1 m, 62.4 dB
at 3 m, 66.9 dB at 5 m: 9.5 to 14.0 dB below the L19 bench. The Phaser repo's
CTF notes measured a lit HB100 about 50 dB above the unlit sweep peak (range
not recorded), so tens of dB should remain, but the level, Rx Gain, and the
HB100's off-axis pattern are a **hardware-day item**. Less signal also helps:
the same notes saw the argmax wander 4.8° peak to peak on a fixed source with
the receiver near full scale.

**Multipath.** Worst-case peak shift from one reflection 5-15° off the
direct path, any phase, on the 8-element array factor: 0.6° at −20 dB, 1.8°
at −10 dB, 3.1° at −6 dB. Beyond about 20° a reflection forms its own lobe
(0.8° shift at −6 dB), which becomes the peak if someone blocks the direct
path. A whiteboard near the line of sight is the largest single risk; a
third bearing is the outlier check.

### 2.3 Lab packet shape (the L19 model)

- **Part 1, Pre-Lab (individual).** The bearing σ from the L19 budget with
  the heading term; cross-range at the given ranges; pick two or three taped
  stations from the room map, predict the error ellipse, and state the box
  spacing that geometry can resolve; run your triangulation script on a
  supplied synthetic bearing set.
- **Part 2, Bench (team, tables only).** Reference shot, then Est. Angle and
  Peak Array Gain over 10 sweeps at each of two or three stations. Bearings
  also go on the board for a class fix.
- **Part 3, Writeup (individual).** A Python script (numpy least squares on
  the bearing lines, about 20 lines; never MATLAB): the fix, residuals, the
  box named, the error after the reveal, and the dominant budget term.

Each team moves its own kit between stations, so every cadet has a fix from
their own data. About 8 present beats; procedure frames read-only.
Instructor-side only: every kit on **Tx Mode Disabled** and out of CW radar
mode, decoy HB100s off, and the live one switched on behind a lid opened on
every box.

### 2.4 Software

On `main`: **Est. Angle** is the argmax of the sweep, shown to 0.1° on a
0.9-1.3° grid; the Tracking tab plots it against sweep count (last 100
sweeps), which shows the spread a team averages. The backend also sends a
power-weighted centroid, `peak_angle_deg`, in every sweep, but no readout
shows it. The sweep runs at about 0.9 per second. **A triangulation helper
in the Phaser repo is not worth adding**: the intersection is the writeup's
analysis and runs on a laptop. Two small optional GUI changes (Decision 4):
show the centroid beside Est. Angle, and export the Tracking tab as CSV.

### 2.5 Objective

None fits exactly. The closest is **3.5**: "I can implement beam steering on
the ADALM-PHASER and verify the steered pattern against theory." It covers
the sweep and the budget, not the intersection. If Neil wants it assessed,
a new **3.10**: "I can measure the bearing of a signal source with the
ADALM-PHASER, predict the bearing's uncertainty, and locate the source by
combining bearings from known positions." That makes 34 objectives (6 + 7 +
10 + 7 + 4), and the syllabus example "30 of 33" changes. Recommend 3.5 this
term: the packet counts toward engagement, so mastery need not move
mid-semester.

## 3. The final project

### 3.1 What the kit can do (computed; carrier taken as 10 GHz)

- **FMCW** (once built): ΔR = c/2B = 0.30 m at B = 500 MHz; 3,336 Hz of beat
  per meter at T_s = 1 ms. With 64 chirps at a 1.2 ms PRI: 77 ms CPI, velocity
  resolution λ/(2M·PRI) = 0.20 m/s, unambiguous ±λ/(4·PRI) = ±6.25 m/s.
  **CW** (exists, fix unmerged): 9.2 Hz bins, 0.14 m/s, 109 ms frames, ±30 m/s.
- **Micro-Doppler** (f_d = 2v/λ): walker torso 1.3 m/s → 87 Hz, limbs 4 m/s
  → 267 Hz; a 0.3-0.4 m fan at 1200 rpm has 19-25 m/s tips (1.3-1.7 kHz),
  which **aliases in range-Doppler but fits CW**; a 1 m pendulum (2.0 s period)
  at 15-30° peaks at 0.8-1.6 m/s (55-108 Hz) and reverses every second.
- **Angle by beam scan cannot hold a crossing target**: at 0.9 sweeps per
  second, a walker crossing at 1 m/s and 4 m moves 14.3°/s, 15.8° per sweep,
  more than the 13° beam. **Monopulse** (phase between the two subarray
  channels, centers 56 mm apart) gives angle in one CPI, unambiguous within
  ±arcsin(λ/2D) = ±14.7° of the steer direction at 10.525 GHz.
- **RCS** of a trihedral corner reflector, σ = 4πa⁴/(3λ²): 0.47 m² at
  a = 0.10 m, 2.4 m² at 0.15 m.
- **An HB100 cannot jam the radar.** Its tone reaches the Pluto only while
  the ramp passes within the 0.6 MHz receive window, 0.12% of a 500 MHz chirp
  (1.2 µs of 1 ms), and never if it sits outside the sweep (it can be anywhere
  in 10.1-10.7 GHz). The jammer works in passive beamforming (L28's MVDR),
  not against the radar. The carrier itself is open: the branch's default
  `output_freq` of 12.2 GHz implies an LO of 12.2 + 0.0001 + 2.2 = 14.4 GHz,
  above §M3's 12.2-13.0 GHz VCO **(unverified; hardware day)**.

### 3.2 Three options

**A. Detect, classify, track; the jammer leaves the project.** One target at
a time on a taped course (walker on a radial line, pendulum, fan on a stool,
reflector on a cart). Detect with CFAR on range-Doppler; classify walker /
fan / pendulum from a CW Doppler spectrogram; track range with an alpha-beta
filter on the detections and angle with monopulse. Truth from tape marks and
a phone video.

- Objectives, old → new. **5.1** "...integrate beam-steering and
  null-steering weights to optimize array performance against a specified
  scenario." → "I can choose and justify array steering and taper weights to
  optimize detection performance for a specified scenario." **5.3** "I can
  suppress a static jammer using null steering while maintaining detection
  of a moving target." → "I can classify a detected target from its
  micro-Doppler signature and report the classifier's accuracy." 5.2 and 5.4
  unchanged. **Course objective 5** → "...into a working demonstration that
  detects, classifies, and tracks a moving target."
- Module 4 feed (current numbers): L30 adds micro-Doppler (bullets and a figure);
  L35 adds a spectrogram part (fan, pendulum); L38's detections feed the
  tracker. L39 carries the new theory (alpha-beta filter, spectrogram
  features, the monopulse recap from L28) with the kickoff, so the Module 5
  index drops "No new theory". No lesson added or cut.
- Classification: three features per window (Doppler spread, symmetry about
  zero, cadence from the envelope's autocorrelation), thresholds or a
  nearest-centroid rule in numpy, scored as a confusion matrix on trials the
  instructor runs blind at the demo. RCS steadiness (reflector against a
  person) is an optional fourth.
- Build: the FMCW mode (Module 4 needs it anyway), a frame recorder (CPI
  cubes and spectrogram frames to `.npz`, downloaded through the browser),
  the CW fix merged; course side, the packet and rubric, the L39 page, and a
  Python starter notebook on recorded data.
- Rubric, 100 points, sliding scale per row: detection with measured P_D
  and false alarms 15; classification accuracy and confusion matrix 20; track
  RMS error and continuity against truth 20; array choices (5.1) 10; live
  demo 15; briefing and defense (5.4) 20.
- Risks: Phase C slips, and Module 4 with it; the Pi's processing rate (ADI's
  CFAR lab tells students to move slowly); classroom clutter; fan blades and
  reflector edges.

**B. Keep the jammer, add classification.** 5.1-5.4 stay and a new 5.5
(A's 5.3 wording) makes 34 objectives. It needs a fourth project period that
does not exist, and per §3.1 the jammer has no physical effect on the radar.
**Not recommended.**

**C. CW only: detect, classify, track bearing.** CFAR on the CW Doppler
spectrum (4.7), micro-Doppler classes (the fan does not alias), bearing from
Tracking mode or a held beam. 5.2 → "I can process Doppler radar data from
the ADALM-PHASER to detect a moving target and track its bearing"; 5.1 and
5.3 as in A. Build: merge the CW fix and add the recorder. Least effort and
risk, but no range, and the project stops using the FMCW chain Module 4
teaches.

| | A | B | C |
| :-- | :-- | :-- | :-- |
| Objectives changed | 5.1, 5.3, course 5 | add 5.5 | 5.1, 5.2, 5.3, course 5 |
| Extra periods | 0 (theory in L39) | 1 or more | 0 |
| Phaser repo work | FMCW mode + recorder (shared with M4) | as A | CW fix + recorder |
| Module 4 FMCW used | all | all | CFAR only |

**Recommend A**, one target at a time on a taped course, with C as the
fallback if the FMCW mode is not running on hardware when Module 4 starts.
The decision is Neil's.

### 3.3 Touch points for an objective change (one commit)

`book/syllabus.md`: course objective 5, the 5.x table, the Projects bullet,
the Module 5 "Scenario" line. `book/intro.md`: capstone card, deliverable
card, objectives list. `book/module05/index.md`: tagline ("Track the mover.
Ignore the jammer."), depth paragraph, LO lists, L39 card. The L39-L41
shells. `scripts/scaffold_lessons.py`: the `LO` dict, the Module 5 synopsis,
the L39-L41 synopses. Forward pointers in L27 and L28. The structure line in
`project/ECE444_PROJECT.md`. No Module 5 practice banners exist. The L01,
L27, L28, and L41 decks mention the jammer and stay as built (§M7).

## 4. Module 4 under both recommendations

L29 Fox Hunt Lab (3.5); L30 Radar Equation (4.1); L31 Range, Resolution,
and Doppler (4.2, plus micro-Doppler); L32 Detection Theory (4.3); L33 FMCW
on Phaser (4.4); L34 FMCW Range Lab (4.2, 4.5; old L33 and L34); L35
Range-Doppler Lab (4.5, plus the spectrogram); L36 MTI Lab (4.6); L37 and L38
CFAR (4.7); L39-L41 the project. Each lab pair gets an L19-style packet. The
dechirp is taught as L17's mixer (multiply two tones, keep the difference),
with no receiver-course vocabulary, and bench quirks stay in instructor notes.

## 5. Unverified, for the hardware day

The radar carrier and LO; a transmit antenna for OUT2 on every kit; the kit
count (the plan assumes 4-5 for a class of ten); received level and Rx Gain at
3-5 m; the + side of the arc (from L19); the HB100's off-axis pattern;
cardboard loss on the real boxes. No calendar is in the repo, so the date L29
falls on, and with it the Phase C deadline, is unknown.

## 6. Decisions for Neil

1. **Fox-hunt placement.** (1) L29, merging L33 and L34; (2) L29, merging
   L37 and L38; (3) the L39 slot. Recommend 1.
2. **Fox-hunt objective.** Quote 3.5, or add 3.10 (§2.5). Recommend 3.5 this
   term.
3. **Who triangulates.** Each team from its own stations, the class fix, or
   both. Recommend both: own fix graded, class fix as a cross-check.
4. **Fox-hunt GUI changes.** Centroid beside Est. Angle and a Tracking-tab
   CSV export, or nothing. Recommend both; the hunt runs without them.
5. **Final project.** A (detect, classify, track; jammer out), B (jammer plus
   classification), C (CW only). Recommend A, with C as the fallback.
6. **FMCW platform for Module 4.** Build the mode in the course GUI (merge
   `claude/radar-capability-ophmxc`, then Phase C), run ADI's Python scripts
   on the Pi desktop, or teach from recorded data. Recommend starting Phase C
   now, with recorded data as the fallback.
7. **Fox-hunt layout.** Boxes at least 0.75 m apart, on tables at array
   height, decoys weighted the same. Recommend as stated.
