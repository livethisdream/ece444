# Syllabus

## Course

**ECE 444 — Antennas, Phased Arrays, and Radar Systems**
Fall 2026

## Instructor

- **Dr. Neil Rogers**
- Office hours: **by appointment only**
- Phone: **937-361-2545**

## Meeting time & location

- **M2** — see USAFA class schedule for room assignment

## Course overview

This course progresses from fundamental electromagnetics and antenna theory
through antenna measurement, phased-array beamforming with the ADALM-PHASER
platform, and FMCW radar concepts. Students combine theory and hands-on
laboratories culminating in a final project: a report, in the cadet's own
words, on a radar processing chain built on the ADALM-PHASER one lab at a time.

## Course Objectives

By the end of this course, you will be able to:

1. Describe fundamental antenna properties (gain, directivity, polarization,
   impedance) and connect them to system-level radio performance.
2. Model, simulate, and measure common antenna types using industry-standard
   tools and lab equipment.
3. Apply phased-array theory (array factor, beam steering, tapering, null
   steering) using the ADALM-PHASER platform.
4. Analyze radar performance using the radar equation, detection theory, and
   FMCW signal processing (range, Doppler, CFAR), and apply it on the
   ADALM-PHASER to detect, classify, and track a moving target.

## Learning objectives

The course is organized around specific, testable learning objectives (LOs).
Each LO is assessed at least once. LOs are assessed as **Mastered** or
**Not Yet Mastered** through module assessments.

### Module 1: Foundations

| LO | Description |
| :-: | :- |
| 1.1 | I can explain what an antenna is, describe its role in a wireless system, and recognize common antenna types by sight. |
| 1.2 | I can define and calculate fundamental antenna properties — gain, directivity, effective aperture, beamwidth, and sidelobe level — apply the reciprocity principle that links an antenna's transmit and receive behavior, and use the Friis transmission equation to predict received power in a link. |
| 1.3 | I can determine the polarization of an antenna and describe the bandwidth characteristics of common antenna types. |
| 1.4 | I can calculate input impedance, feed considerations, and the role of baluns in an antenna feed system. |
| 1.5 | I can identify and distinguish the reactive near-field, radiating near-field, and far-field regions and calculate the boundaries for a given antenna. |
| 1.6 | I can set up and interpret the radiation integrals to derive the far-field pattern of a current distribution. |

### Module 2: Antenna Types, Simulation, and Measurement

| LO | Description |
| :-: | :- |
| 2.1 | I can describe the radiation behavior of simple resonant antennas (isotropic radiator, half-wave dipole, monopole, loop) and calculate their gain and impedance. |
| 2.2 | I can simulate a dipole antenna using an EM simulation tool and interpret the results against analytical predictions. |
| 2.3 | I can describe the radiation mechanism, pattern, and typical use cases for patch, slot, and horn antennas. |
| 2.4 | I can describe how reflectors, Yagi-Uda antennas, and arrays achieve high gain, explain how a log-periodic antenna trades gain for bandwidth, and select an appropriate high-gain antenna for a given application. |
| 2.5 | I can explain the theory behind antenna pattern measurement, including anechoic chambers, near-field to far-field transformations, and standard gain horns. |
| 2.6 | I can measure the impedance and S-parameters of an antenna using a vector network analyzer and interpret the results. |
| 2.7 | I can measure the radiation pattern of an antenna and extract gain, beamwidth, sidelobe level, and polarization from the data. |

### Module 3: Arrays and ADALM-PHASER Beamforming

| LO | Description |
| :-: | :- |
| 3.1 | I can describe aperture distributions and calculate aperture efficiency for a given illumination. |
| 3.2 | I can derive the array factor for an arbitrary linear array and apply pattern multiplication. |
| 3.3 | I can identify the hardware architecture of the ADALM-PHASER and control it via SDR software. |
| 3.4 | I can calculate the phase weights required to steer a beam to a given angle and predict the resulting array pattern. |
| 3.5 | I can implement beam steering on the ADALM-PHASER and verify the steered pattern against theory. |
| 3.6 | I can distinguish between array factor and true antenna pattern and account for element pattern effects. |
| 3.7 | I can apply amplitude tapering (uniform, cosine, Chebyshev, Taylor) to control sidelobe level and predict the pattern trade-off. |
| 3.8 | I can identify beam squint and quantization effects in a phased array and describe their impact on system performance. |
| 3.9 | I can calculate null-steering weights and implement pattern nulls on the ADALM-PHASER. |

### Module 4: Radar Fundamentals and FMCW

| LO | Description |
| :-: | :- |
| 4.1 | I can apply the radar equation to calculate received power for a given geometry, and account for path loss and radar cross section (RCS). |
| 4.2 | I can calculate range resolution, unambiguous range, and Doppler shift for a given radar waveform. |
| 4.3 | I can apply radar detection theory (PD, FAR, dwell time) to determine detection performance under noise. |
| 4.4 | I can describe FMCW radar operation and configure an FMCW waveform on the ADALM-PHASER. |
| 4.5 | I can process FMCW radar data to produce range, range-waterfall, and range-Doppler results. |
| 4.6 | I can implement moving target indication (MTI) processing to distinguish moving targets from clutter. |
| 4.7 | I can apply constant false-alarm rate (CFAR) processing to radar data and evaluate detection performance. |
| 4.8 | I can integrate FMCW radar processing with a phased-array front-end to track a moving target. |
| 4.9 | I can classify a detected target from its micro-Doppler signature and report the classifier's accuracy. |

## Grading

Grades in this course combine mastery-based assessment with engagement and
project-based evaluation. Four components make up your final grade:

| Component | Weight | Evaluation method |
| :- | :-: | :- |
| Learning Objective (LO) mastery | 30% | Percent of course LOs mastered, multiplied by 30% |
| Engagement | 10% | Participation, preparation, practice, EI, and course engagement |
| Midterm Project — Antenna Pattern Measurement | 30% | 100-point rubric, scored on the scale in the project packet |
| Final Project — Radar Systems Report | 30% | Rubric-based sliding scale |

### LO mastery assessment

Each learning objective is assessed as **Mastered** or **Not Yet Mastered**
through module assessments. The LO Mastery portion of the final grade is
calculated as:

```text
LO Mastery contribution = (LOs mastered / total course LOs) × 30%
```

For example, if a cadet masters 28 of 31 course LOs, the LO Mastery
contribution is:

```text
(28 / 31) × 30% = 27.1%
```

### Midterm project assessment

The Midterm Project is graded on a **100-point rubric**, published in the
project packet and weighted toward analysis rather than data collection.
**There is no resubmission** — the schedule does not allow a revision cycle
between the due date and the end of the course, so the grade you earn is the
grade.

Read the rubric before you start rather than after you finish. It is in the
packet for exactly that reason, and the checkpoints exist so that a problem
surfaces while there is still time to fix it.

### Your midterm grade

The four weights above are the **final** course grade. The **midterm grade**
reported at the midpoint is computed from the three things you have actually
done by then — the final project has not happened yet, so it carries no weight:

| Component | Weight in the midterm grade |
| :- | :-: |
| Midterm Project — Antenna Pattern Measurement | 40% |
| Engagement | 30% |
| LO mastery, on the assessments given so far | 30% |

Engagement and LO mastery count for more here than they do in the final grade,
because at the midpoint they are most of the evidence there is. The midterm
grade is a progress report, not a component of the final grade — nothing in
this table is added to the table above.

### Final project assessment

The Final Project is **one report, in your own words**, on the radar
hardware and processing you built in Module 4. The **L28, L29, L30, and L31
Labs** are its scaffolding: each is one stage of a single radar processing
chain on your own kit (range, range-Doppler and MTI, CFAR, then
classification), and each hands you the results a section of the report is
built on. The lab packets are checked and returned with feedback, but they
are not the final project, and text lifted from them earns nothing in the
report. The report is graded on a **rubric with a sliding scale**, published
with the L28 Lab packet, that rewards explaining why the results came out as
they did over reporting them. A unique extension, proposed and approved in
advance, can earn extra credit. See the
[final project page](module04/final-project/index.md).

### Engagement credits (EC)

Engagement is worth **10% of your final grade** and rewards active participation
in the course rather than single-attempt performance on graded work. You may
earn engagement points in the following ways:

- **Practice problems.** Weekly problem sets keyed to the module's learning
  objectives. These are your reps — not graded for correctness, but graded for
  a genuine, documented attempt. Correct or not, the work matters.
- **Attending Extra Instruction (EI).** Book time with me and come prepared with
  specific questions or a concept you want to work through.
- **Lab packets (Module 3).** A lab's packet has three parts: a pre-lab you do before the
  period (your predictions, and in some labs a rehearsal in the browser simulator), the data
  you record on your own kit, and a writeup you do afterward (what you
  measured against what you predicted, and why they differ). Where a lab has a
  packet, it replaces the practice problems for that lab, and for the lesson
  before it when the pre-lab draws on that lesson. The packet is one submission, turned in complete after the lab and
  graded the same way: a genuine, documented attempt. Lab packets are required. They are the first engagement
  points you earn, and the other routes here add to them up to the cap. The
  Module 4 lab packets (L28–L31) are not engagement: they are the scaffolding
  for the final project report.
- **Research paper.** You may complete a research paper on a
  relevant, pre-approved topic — an antenna, array, or radar technology, a
  measurement technique, or a mission application. Must be in **IEEE format**,
  contain at least **3 scholarly references**, and adhere to the submission
  standards in this syllabus.
- **Course improvement contributions.** Spotted a bug in a lab writeup, an
  unclear slide, a broken link on the course site? Tell me and it counts.

Engagement is capped at 10%; extra credit does not roll over.

### Grade scale

<table class="grade-scale">
  <thead>
    <tr>
      <th>A</th><th>A−</th><th>B+</th><th>B</th><th>B−</th>
      <th>C+</th><th>C</th><th>C−</th><th>D</th><th>F</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>100%</td><td>93%</td><td>90%</td><td>87%</td><td>83%</td>
      <td>80%</td><td>77%</td><td>73%</td><td>70%</td><td>≤ 60%</td>
    </tr>
  </tbody>
</table>

## Projects

Two graded projects anchor the course:

- **Midterm Project — Antenna Pattern Measurement.** Introduced at Lesson 9, due **2 Oct, 2359**. Students build a 915 MHz dipole and trim it to resonance, then match the same antenna to 50 ohms at a second frequency with a discrete network, simulate it, execute a pattern-measurement campaign on it at both frequencies, reduce the data, and report gain, beamwidth, sidelobe level, and polarization behavior against expectations. Graded on a **100-point rubric**, published in the project packet. No resubmission.
- **Final Project — Radar Systems Report.** One report, in your own words, exploring the radar hardware and processing chain you build on the ADALM-PHASER in the L28–L31 Labs, from an FMCW capture to a detected, classified target. The labs are the scaffolding; the lab packets alone are not the project. Individual. Graded on a **rubric with a sliding scale**; extra credit for an approved unique extension.

## Course policies

### Instructor philosophy

You have chosen one of the most difficult majors at USAFA — I applaud your
commitment. My role in your journey is to enable your success. My intent is to
do this by creating an inclusive environment and putting in the work *with*
you. If you work hard and communicate with me, I will do everything in my power
to make sure you succeed.

Have questions? **Ask** — there is genuinely no such thing as a stupid question.
Have concerns, especially about your learning environment? Let's talk. You face
many challenges here at USAFA; I am in your corner — so let's go.

### 1. Absences

Communicate with me **beforehand** in the event of an absence. If you will miss
any graded event due to a scheduled absence (SCA, sport team trip, scheduled
medical procedure), a makeup plan should be in place **before** the absence
occurs. In the event of bedrest, notify me **via email** as soon as possible
after receiving approval.

### 2. Academic honor

Your honor is extremely important. The course's academic security policies are
designed to help you succeed in meeting academic requirements while practicing
the honorable behavior our country rightfully demands of its military. Do not
compromise your integrity by violating academic security or by taking unfair
advantage of your classmates.

### 3. Assignment availability & late work

All work will be available through Teams, the course website, and/or Gradescope.
A **24-hour grace period** is generally observed, after which **25% of available
points will be deducted for each calendar day** the graded assignment is late.
I may waive part or all of this penalty for legitimate, pre-coordinated
extenuating circumstances.

### 4. Authorized resources

The midterm and final projects have their own resource policies described in
their assignment packets. When electronic devices are authorized for viewing
reference materials during any graded event, use of **internet, Teams, and
generative AI tools is not allowed** unless explicitly permitted.

### 5. Collaboration

**Collaboration (not copying)** on practice problems is highly encouraged. A
good litmus test: you must be able to **explain every step** on your submitted
work. If you can't, it's copying, not collaboration. All help received on graded
work must be documented per the documentation policy below.

**Module assessments are individual work.** Do not work with or get help from
anyone else, and use only the course materials.

### 6. Documentation

In accordance with the Dean's policy for documentation, all ECE assignments
must have a documentation statement. For team projects, you are not required
to document collaboration within your own team. The statement should be
clearly identified with the word **"Documentation."** If you did not
collaborate, write **"Documentation: None."** Assignments without a
documentation statement are incomplete and may be returned for completion; a
1-day-late penalty (up to 25%) may be assessed in lieu of returning the
assignment.

### 7. Extra Instruction (EI)

EI is one of the best and easiest ways to succeed in this class. Walk-in EI is
not generally available — please book with me directly.

### 8. Generative AI

I am **pro-AI**; however, I expect you to use generative AI platforms
(ChatGPT, Copilot, Claude, etc.) as a **tool**, not as a replacement for your
own learning. It will be very clear if you are using AI irresponsibly: these
tools frequently generate incorrect solutions to the RF and array-theory
problems you'll encounter here, and often suggest approaches that don't align
with our course objectives. **If you use generative AI on any assignment,
include a documentation statement** as outlined in the Documentation policy.

## Schedule

Lessons are topics, not class periods: a lesson takes the time it takes, and
its lab, where it has one, follows it on the bench. Project days and open-lab
time are on the course calendar, not in this list. Lessons link to notes on the
[course home](intro.md).

### Module 1: Foundations of Electromagnetics and Antennas

- **L1** Course Introduction — what an antenna is, why it matters to Air Force operators, course roadmap, SDR + acoustic-beam demos
- **L2** Basic Properties and Terminology — gain, directivity, effective area, beamwidth, boresight, lobes
- **L3** Polarization and Bandwidth
- **L4** Impedance, Feeding, and Baluns
  - **L4 Lab** — Matching Procedures
- **L5** Field Regions — reactive near-field, radiating near-field, far-field
- **L6** Radiation Integrals

### Module 2: Antenna Types, Simulation, and Measurement

- **L7** Simple Resonant Antennas — isotropic radiators, half-wave dipoles
- **L8** Dipole Simulation Lab **(LAB)**
- **L9** Measurement Theory — anechoic chambers, near-field / far-field transformations, standard gain horns, the vector network analyzer &nbsp; · &nbsp; **Midterm project introduced**
- **L10** Measurement Lab — Impedance and S-parameters **(LAB)**
- **L11** Measurement Lab — Radiation Patterns **(LAB)**
- **L12** Loop and Monopole Antennas
- **L13** Patch, Slot, and Horn Antennas
- **L14** High-Gain Antennas — reflectors, Yagi-Uda, arrays

### Module 3: Arrays and ADALM-PHASER Beamforming

- **L15** Aperture Distributions and Efficiency
- **L16** The Array Factor and Pattern Multiplication
- **L17** Introduction to Phased Array Hardware — ADALM-PHASER, SDR control
  - **L17 Lab** — Phased Array Bring-Up
- **L18** Beam Steering
  - **L18 Lab** — Beam Steering
- **L19** Direction Finding — bearings and triangulation
  - **L19 Lab** — Fox Hunt: find the live HB100 by triangulating bearings
- **L20** Array Factor and Beamwidth
  - **L20 Lab** — Array Factor: beamwidth vs. aperture
- **L21** Antenna Pattern — true pattern vs. array factor
  - **L21 Lab** — Antenna Pattern: the pattern measured by moving the source
- **L22** Sidelobes and Tapering
- **L23** Beam Squint and Quantization — grating lobes, squint, quantization
  - **L22–L23 Lab** — Tapering, Squint, and Quantization: one lab for both lessons, after Lesson 23
- **L24** Null Steering
  - **L24 Lab** — Null Steering

### Module 4: Radar Fundamentals and FMCW

The L28–L31 Labs are the scaffolding for the final project, a report on the radar they build.

- **L25** The Radar Equation, Path Loss, and Radar Cross Section (RCS)
- **L26** Range, Resolution, Doppler Effect, and Radar Types
- **L27** Radar Detection — PD, FAR, dwell time
- **L28** FMCW on the Phaser
  - **L28 Lab** — FMCW Range: range calculations and the range waterfall
- **L29** Range-Doppler and MTI
  - **L29 Lab** — Range-Doppler and MTI
- **L30** CFAR Processing
  - **L30 Lab** — CFAR Processing
- **L31** Classification and Tracking — micro-Doppler classification, range and angle tracking
  - **L31 Lab** — Micro-Doppler Spectrogram

## Textbooks & materials

See the [materials page](materials.md).

## Software & hardware

- ADALM-PHASER
- Antenna simulation software — nec_lab (NEC-2), provided with the course
- Vector network analyzer (VNA) — the chamber's Copper Mountain analyzer, for both measurement labs
- Anechoic chamber — the USAFA chamber and its browser dashboard (calibration, VNA sweeps and impedance, pattern scans, Touchstone export), for the measurement labs
