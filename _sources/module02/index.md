---
nav: Antenna Types
frame_view: true
---

# Module 2 — Antenna Types, Simulation, and Measurement

::::{frame}
:class: title-frame

<div class="course-mark">ECE 444 · Module 02</div>

<h1 class="frame-title">Antenna Types, Simulation, and Measurement</h1>

<div class="title-rule"></div>

Theory is cheap. Build it, simulate it, then measure it.

Lessons 7–14 · Antennas, Phased Arrays, and Radar Systems · Dr. Neil Rogers
::::

::::{frame} Where This Module Goes
Module 1 described *any* radiator in the abstract. This module meets the real
families — dipoles, loops, monopoles, patches, slots, horns, reflectors, Yagis
— and asks what each one is actually good for.

Then it puts numbers on them twice over: **once in a simulator, once on the
bench**. When those two disagree, one of them is wrong, and finding out which
is the skill.

:::{depth}
You will simulate a dipole and predict its impedance, then walk to the VNA and
measure the same antenna. Expect the two to differ. The gap between a model
and a measurement is where engineering judgment lives, and it is far more
useful than either number on its own.
:::
::::

::::{frame} Measurement Comes Early
The measurement block sits at Lessons 9–11, ahead of the remaining antenna
families, because the midterm project is a pattern-measurement campaign and it
is due at Lesson 20. Learning the range and the analyzer first buys you eleven
lessons of bench time instead of six.

:::{depth}
The order costs you something and it is worth naming. When you measure in
Lesson 11 you will have met the dipole and not yet met the patch, the horn, or
the reflector, so the antenna you characterize is a simpler one than it would
have been. Lessons 12–14 then read differently: every gain figure and every
pattern in them is a claim you already know how to check, and several of them
are claims you will want to check for your project report.
:::
::::

::::{frame} Learning Objectives 2.1-2.3

<ol class="lo-list" style="--module: '2'">
  <li>I can describe the radiation behavior of simple resonant antennas (isotropic radiator, half-wave dipole, monopole, loop) and calculate their gain and impedance.</li>
  <li>I can simulate a dipole antenna using an EM simulation tool and interpret the results against analytical predictions.</li>
  <li>I can describe the radiation mechanism, pattern, and typical use cases for patch, slot, and horn antennas.</li>
</ol>
::::

::::{frame} Learning Objectives 2.4-2.6

<ol class="lo-list" start="4" style="--module: '2'">
  <li>I can describe how reflectors, Yagi-Uda antennas, and arrays achieve high gain, and select an appropriate high-gain antenna for a given application.</li>
  <li>I can explain the theory behind antenna pattern measurement, including anechoic chambers, near-field to far-field transformations, and standard gain horns.</li>
  <li>I can measure the impedance and S-parameters of an antenna using a vector network analyzer and interpret the results.</li>
</ol>
::::

::::{frame} Learning Objective 2.7

<ol class="lo-list" start="7" style="--module: '2'">
  <li>I can measure the radiation pattern of an antenna and extract gain, beamwidth, sidelobe level, and polarization from the data.</li>
</ol>
::::

::::{frame} Lessons 7-8: The Canonical Radiator, Modeled

<div class="module-toc">
  <a class="mt-card mt-lesson" href="L07-simple-resonant-antennas/index.html">
    <span class="mt-kind">Lesson 7</span>
    <h4>Simple Resonant Antennas</h4>
    <p>Isotropic radiators and the half-wave dipole: pattern, gain, and impedance. Objective 2.1.</p>
  </a>
  <a class="mt-card mt-lesson" href="L08-dipole-simulation-lab/index.html">
    <span class="mt-kind">Lesson 8</span>
    <h4>Dipole Simulation Lab</h4>
    <p>Simulate a dipole in an EM tool and compare against analytical predictions. Objective 2.2.</p>
  </a>
</div>
::::

::::{frame} Lessons 9-11: Measuring What You Built

<div class="module-toc">
  <a class="mt-card mt-lesson" href="L09-pattern-measurement-theory/index.html">
    <span class="mt-kind">Lesson 9</span>
    <h4>Measurement Theory</h4>
    <p>Ranges and chambers, what a VNA measures and how it is calibrated, gain by comparison, and dynamic range. Midterm project introduced. Objectives 2.5, 2.6.</p>
  </a>
  <a class="mt-card mt-lesson" href="L10-measurement-lab-sparams/index.html">
    <span class="mt-kind">Lesson 10</span>
    <h4>Measurement Lab 1 — Impedance and S-parameters</h4>
    <p>Hands on the analyzer: calibrate, sweep, and reduce an antenna's impedance and bandwidth. Objective 2.6.</p>
  </a>
  <a class="mt-card mt-lesson" href="L11-measurement-lab-patterns/index.html">
    <span class="mt-kind">Lesson 11</span>
    <h4>Measurement Lab 2 — Radiation Patterns</h4>
    <p>Hands on the range: cut two planes, then extract gain, beamwidth, sidelobe level, and polarization. Objective 2.7.</p>
  </a>
</div>
::::

::::{frame} Lessons 12-14: The Rest of the Families

<div class="module-toc">
  <a class="mt-card mt-lesson" href="L12-loop-monopole-antennas/index.html">
    <span class="mt-kind">Lesson 12</span>
    <h4>Loop and Monopole Antennas</h4>
    <p>Small loops and monopoles: radiation behavior, gain, and impedance. Objective 2.1.</p>
  </a>
  <a class="mt-card mt-lesson" href="L13-patch-slot-horn/index.html">
    <span class="mt-kind">Lesson 13</span>
    <h4>Patch, Slot, and Horn Antennas</h4>
    <p>Radiation mechanism, pattern, and use cases for patch, slot, and horn antennas. Objective 2.3.</p>
  </a>
  <a class="mt-card mt-lesson" href="L14-high-gain-antennas/index.html">
    <span class="mt-kind">Lesson 14</span>
    <h4>High-Gain Antennas</h4>
    <p>Reflectors, Yagi-Uda, and arrays — how they get gain. Objective 2.4.</p>
  </a>
</div>
::::

::::{frame} Where This Is Going
**Module 3** stops treating an antenna as one object. Put several in a row,
control the phase of each, and the pattern becomes something you steer rather
than something you accept.

Everything you measure here — pattern, gain, beamwidth, sidelobe level — is
what you will steer there.
::::
