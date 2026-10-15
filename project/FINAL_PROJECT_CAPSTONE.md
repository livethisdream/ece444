# Capstone final project: parked for a future offering

**Status: parked (Neil, 2026-10-15).** Fall 2026 runs out of calendar before a
separate capstone fits, so Module 5 folded into Module 4 and the final project
became the L28-L31 Labs graded together (see `COURSE_SPEC.md` §M7, "Module 5
folds into Module 4"). Neil wants this design kept for future offerings. It is
the plan as it stood on 2026-10-15: option A of `MODULE45_BUILDOUT_PLAN.md`
§3.2, plus the scaffolding and the multi-target extension discussed that day.
Nothing here is on the site.

## 1. Scenario

Detect, classify, and track a moving target with the ADALM-PHASER, then brief
the results. Individual: each cadet on their own kit. One target at a time on
a taped course (walker on a radial line, pendulum, fan on a stool, reflector on
a cart); the jammer is out. Detect with CFAR on range-Doppler, classify from a
micro-Doppler spectrogram, track range with an alpha-beta filter and angle with
monopulse. The kit's numbers (resolution, aliasing, monopulse limits, RCS) are
in `MODULE45_BUILDOUT_PLAN.md` §3.1.

**The taped course** is masking tape on the floor at measured positions: a
radial line out from the Phaser with a mark every 0.5 m, and a few marks at
known angles off boresight. A phone video shows when the target crossed each
mark, which gives true range and angle against time to score the tracker
against. The instructor lays out one standard course and publishes its
dimensions, so every cadet scores against the same truth.

## 2. Objectives as they were (Module 5)

- **5.1** I can choose and justify array steering and taper weights to optimize detection performance for a specified scenario.
- **5.2** I can integrate FMCW radar processing with a phased-array front-end to track a moving target. *(now 4.8)*
- **5.3** I can classify a detected target from its micro-Doppler signature and report the classifier's accuracy. *(now 4.9)*
- **5.4** I can present system performance results and defend engineering trade-offs in a technical briefing.

Course objective 5: "Integrate array beamforming and radar signal processing
into a working demonstration that detects, classifies, and tracks a moving
target." Reinstating the capstone means restoring 5.1 and 5.4 (or their
successors) everywhere an objective is quoted; see `CLAUDE.md`, Conventions.

## 3. Shape

A kickoff lesson (L32), then two phases on the calendar:

- **Phase 1, Array Optimization.** Choose steering and taper weights and
  evaluate detection performance. (5.1)
- **Phase 2, Radar Integration and Demonstration.** Integrate FMCW detection,
  micro-Doppler classification, and tracking; overlay tracks on the array
  pattern; brief the results. (5.2, 5.3, 5.4)

## 4. Rubric (100 points, sliding scale per row)

| Row | Points |
| :-- | :-: |
| Detection: measured P_D and false alarms | 15 |
| Classification: accuracy and confusion matrix | 20 |
| Tracking: RMS error and continuity against truth | 20 |
| Array choices (5.1) | 10 |
| Live demo | 15 |
| Briefing and defense (5.4) | 20 |

## 5. Incremental deliverables (the scaffolding cadets asked for)

Each checkpoint builds one rubric row, so nothing done early is thrown away.
Grade D0-D3 as low-stakes pass/revise checkpoints that feed the final rubric,
not as separate grades.

- **D0, Plan memo (1 page, at kickoff).** Target classes chosen, the course
  layout, and a predicted-performance table: range and velocity resolution,
  unambiguous velocity, expected Doppler of each target. (5.1 groundwork)
- **D1, Array choice (end of Phase 1).** Steering angle and taper for the
  scenario, with a simulated pattern and the trade-off stated (sidelobes
  against beamwidth against SNR loss), plus measured P_D and false-alarm count
  from a short recorded run. (5.1, detection row)
- **D2, Data and pipeline.** One labeled `.npz` capture per target class and a
  notebook that goes raw data → range-Doppler → CFAR detections, checked
  against the tape marks. The biggest risk, so first in Phase 2. Ship a starter
  notebook on recorded data with it so a cadet whose bench FMCW mode fails is
  not blocked. (5.2)
- **D3, Classifier.** Three features per window (Doppler spread, symmetry about
  zero, cadence) and a threshold or nearest-centroid rule; confusion matrix on
  held-out captures. (5.3)
- **D4, Tracker and dress rehearsal.** Alpha-beta range track and monopulse
  angle, RMS error against the taped truth; a 5-minute practice brief with
  peer feedback before the graded demo and brief. (5.2, 5.4)

## 6. Extension: the taped course as development, a real scenario as the test

Discussed 2026-10-15 and not adopted, for a future offering with more time.
The taped course becomes the calibration range where D1-D3 are built and
scored against known truth; the final demo is an uncontrolled scenario with
two targets. What that adds:

- **Data association.** An alpha-beta filter assumes every detection is its
  target. Two targets need gating, nearest-neighbor association, and track
  start and drop logic; one lesson of theory.
- **Monopulse per cell.** Two targets in one beam blend into one angle. They
  must separate in range (more than 0.3 m) or Doppler (more than 0.2 m/s), and
  angle is computed per range-Doppler cell.
- **Per-target classification.** A CW spectrogram mixes every mover, so the
  spectrogram comes from slow time in each detected range bin of the FMCW
  data. The fan's blade tips alias there (±6.25 m/s unambiguous), so swap the
  fan class for a pendulum or a cart.
- **Two tiers.** The single target on the taped course is the graded baseline
  and most of the points; the two-target run is the capstone demo, scored on
  how well the system degrades rather than on perfection.
