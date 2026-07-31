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
laboratories culminating in a capstone project integrating beamforming and
radar signal processing.

## Course goals

By the end of this course, you will be able to:

1. Describe fundamental antenna properties (gain, directivity, polarization,
   impedance) and connect them to system-level radio performance.
2. Model, simulate, and measure common antenna types using industry-standard
   tools and lab equipment.
3. Apply phased-array theory (array factor, beam steering, tapering, null
   steering) using the ADALM-PHASER platform.
4. Analyze radar performance using the radar equation, detection theory, and
   FMCW signal processing (range, Doppler, CFAR).
5. Integrate array beamforming and radar signal processing into a working
   demonstration of tracking a moving target while suppressing a jammer.

## Learning objectives

The course is organized around specific, testable learning objectives (LOs).
Each LO is assessed at least once. Mastery of every LO earns an "A" on the
mastery-based portion of the grade.

### Module 1 — Foundations

| LO | Description |
| :-: | :- |
| 1.1 | I can define what an antenna is, articulate the reciprocity principle, and describe the role of an antenna in a wireless system. |
| 1.2 | I can define and calculate fundamental antenna properties: gain, directivity, effective aperture, beamwidth, and sidelobe level. |
| 1.3 | I can determine the polarization of an antenna and describe the bandwidth characteristics of common antenna types. |
| 1.4 | I can calculate input impedance, feed considerations, and the role of baluns in an antenna feed system. |
| 1.5 | I can identify and distinguish the reactive near-field, radiating near-field, and far-field regions and calculate the boundaries for a given antenna. |
| 1.6 | I can set up and interpret the radiation integrals to derive the far-field pattern of a current distribution. |

### Module 2 — Antenna Types, Simulation, and Measurement

| LO | Description |
| :-: | :- |
| 2.1 | I can describe the radiation behavior of simple resonant antennas (isotropic radiator, half-wave dipole, monopole, loop) and calculate their gain and impedance. |
| 2.2 | I can simulate a dipole antenna using an EM simulation tool and interpret the results against analytical predictions. |
| 2.3 | I can describe the radiation mechanism, pattern, and typical use cases for patch, slot, and horn antennas. |
| 2.4 | I can describe how reflectors, Yagi-Uda antennas, and arrays achieve high gain, and select an appropriate high-gain antenna for a given application. |
| 2.5 | I can explain the theory behind antenna pattern measurement, including anechoic chambers, near-field to far-field transformations, and standard gain horns. |
| 2.6 | I can measure the impedance and S-parameters of an antenna using a vector network analyzer and interpret the results. |
| 2.7 | I can measure the radiation pattern of an antenna and extract gain, beamwidth, sidelobe level, and polarization from the data. |

### Module 3 — Arrays and ADALM-PHASER Beamforming

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

### Module 4 — Radar Fundamentals and FMCW

| LO | Description |
| :-: | :- |
| 4.1 | I can apply the radar equation to calculate received power for a given geometry, and account for path loss and radar cross section (RCS). |
| 4.2 | I can calculate range resolution, unambiguous range, and Doppler shift for a given radar waveform. |
| 4.3 | I can apply radar detection theory (PD, FAR, dwell time) to determine detection performance under noise. |
| 4.4 | I can describe FMCW radar operation and configure an FMCW waveform on the ADALM-PHASER. |
| 4.5 | I can process FMCW radar data to produce range, range-waterfall, and range-Doppler results. |
| 4.6 | I can implement moving target indication (MTI) processing to distinguish moving targets from clutter. |
| 4.7 | I can apply constant false-alarm rate (CFAR) processing to radar data and evaluate detection performance. |

### Module 5 — Capstone

| LO | Description |
| :-: | :- |
| 5.1 | I can integrate beam-steering and null-steering weights to optimize array performance against a specified scenario. |
| 5.2 | I can integrate FMCW radar processing with a phased-array front-end to track a moving target. |
| 5.3 | I can suppress a static jammer using null steering while maintaining detection of a moving target. |
| 5.4 | I can present system performance results and defend engineering trade-offs in a technical briefing. |

## Grading

Grades in this course are based on **mastery** of learning objectives, not
single-attempt performance. Three components make up your final grade:

| Component | Weight |
| :- | :-: |
| Engagement | 25% |
| Midterm project | 35% |
| Final project | 40% |

### Mastery-based assessment

The Midterm and Final Projects are assessed against the learning objectives on
a **binary scale**:

- **1** — you have mastered the objective.
- **0** — you have not *yet* mastered the objective.

You may **revise your work** based on the detailed feedback provided, unless no
effort is evident (the assessment is blank, incomplete, or significantly late).
In those cases, a retake may be earned by giving a **5-minute technical
presentation** during class on a relevant, pre-approved topic.

The bar is simple: I want you to *learn this material*, and I would rather you
learn it late than not at all.

### Engagement credits (EC)

Engagement is worth **25% of your final grade** and rewards active participation
in the course rather than single-attempt performance on graded work. You may
earn engagement points in the following ways:

- **Practice problems.** Weekly problem sets keyed to the module's learning
  objectives. These are your reps — not graded for correctness, but graded for
  a genuine, documented attempt. Correct or not, the work matters.
- **Attending Extra Instruction (EI).** Book time with me and come prepared with
  specific questions or a concept you want to work through.
- **Lab prep and lab writeup engagement.** Coming to lab prepared with a
  pre-lab plan, and turning in a thoughtful writeup, both count.
- **Research paper (up to 5 EC).** You may complete a research paper on a
  relevant, pre-approved topic — an antenna, array, or radar technology, a
  measurement technique, or a mission application. Must be in **IEEE format**,
  contain at least **3 scholarly references**, and adhere to the submission
  standards in this syllabus.
- **Course improvement contributions.** Spotted a bug in a lab writeup, an
  unclear slide, a broken link on the course site? Tell me and it counts.

Engagement is capped at 25%; extra credit does not roll over.

### Grade scale

| F | D | C− | C | C+ | B− | B | B+ | A− | A |
| :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: |
| ≤ 60% | 70% | 73% | 77% | 80% | 83% | 87% | 90% | 93% | 100% |

## Projects

Two graded projects anchor the course:

- **Midterm Project — Antenna Pattern Measurement.** Introduced at Lesson 11, due at Lesson 20. Students design and execute a pattern-measurement campaign on an antenna under test, reduce the data, and report gain, beamwidth, sidelobe level, and polarization behavior against expectations.
- **Final Project — Combined Beamforming + Radar.** Track a moving target while suppressing a static jammer using the ADALM-PHASER. Runs across Lessons 39–41 (Module 5).

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

**Collaboration (not copying)** on practice problems and assessments is highly
encouraged, unless your instructor provides direction otherwise. A good litmus
test: you must be able to **explain every step** on your submitted work.
If you can't, it's copying, not collaboration. All help received on graded work
must be documented per the documentation policy below.

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

Lessons link to notes on the [course home](intro.md).
Labs are marked **LAB**.

### Module 1 — Foundations of Electromagnetics and Antennas

1. Course Introduction — what an antenna is, why it matters to Air Force operators, course roadmap, SDR + acoustic-beam demos
2. Basic Properties and Terminology — gain, directivity, effective area, beamwidth, boresight, lobes
3. Polarization and Bandwidth
4. Impedance, Feeding, and Baluns
5. Field Regions — reactive near-field, radiating near-field, far-field
6. Radiation Integrals

### Module 2 — Antenna Types, Simulation, and Measurement

7. Simple Resonant Antennas — isotropic radiators, half-wave dipoles
8. Dipole Simulation Lab **(LAB)**
9. Loop and Monopole Antennas
10. Patch, Slot, and Horn Antennas
11. High-Gain Antennas — reflectors, Yagi-Uda, arrays &nbsp; · &nbsp; **Midterm project introduced**
12. Pattern Measurement Theory — anechoic chambers, near-field / far-field transformations, standard gain horns
13. Measurement Lab Part 1 — Impedance and S-parameters **(LAB)**
14. Measurement Lab Part 2 — Radiation Patterns **(LAB)**

### Module 3 — Arrays and ADALM-PHASER Beamforming

15. Aperture Distributions and Efficiency
16. The Array Factor and Pattern Multiplication
17. Introduction to Phased Array Hardware — ADALM-PHASER, SDR control
18. Beam Steering Theory
19. Beam Steering Lab **(LAB)**
20. Array Factor and Beamwidth Theory &nbsp; · &nbsp; **Midterm project due**
21. Array Factor Lab **(LAB)**
22. Antenna Pattern Theory — true pattern vs. array factor
23. Antenna Pattern Lab **(LAB)** — AUT measurement using Phaser
24. Sidelobes and Tapering Theory
25. Tapering Lab **(LAB)**
26. Beam Squint and Quantization
27. Null Steering Theory
28. Null Steering Lab **(LAB)**

### Module 4 — Radar Fundamentals and FMCW

29. The Radar Equation, Path Loss, and Radar Cross Section (RCS)
30. Range, Resolution, Doppler Effect, and Radar Types
31. Radar Detection Theory — PD, FAR, dwell time
32. Introduction to FMCW on Phaser
33. Range Calculations Lab **(LAB)**
34. Range Waterfall Lab **(LAB)**
35. Range-Doppler Lab **(LAB)**
36. Moving Target Indication (MTI) Lab **(LAB)**
37. CFAR Processing Theory
38. CFAR Processing Lab **(LAB)**

### Module 5 — Final Capstone Project

**Scenario:** Track a moving target while suppressing a static jammer.

39. Final Project Kickoff
40. Phase 1 — Array Optimization: design beam-steering weights, implement null-steering weights, evaluate array performance
41. Phase 2 — Radar Integration and Demonstration: integrate FMCW radar processing, perform Doppler target tracking, overlay radar tracking results onto the optimized antenna array pattern

## Textbooks & materials

See the [materials page](materials.md).

## Software & hardware

- ADALM-PHASER
- Antenna simulation software _(TBD)_
- Vector network analyzer (VNA) — for measurement labs
- Anechoic chamber — for pattern measurement labs
