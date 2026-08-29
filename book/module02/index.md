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
and a measurement is where engineering judgement lives, and it is far more
useful than either number on its own.
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

::::{frame} Lessons 7-9: The Canonical Radiators

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
  <a class="mt-card mt-lesson" href="L09-loop-monopole-antennas/index.html">
    <span class="mt-kind">Lesson 9</span>
    <h4>Loop and Monopole Antennas</h4>
    <p>Small loops and monopoles: radiation behavior, gain, and impedance. Objective 2.1.</p>
  </a>
</div>
::::

::::{frame} Lessons 10-11: Shaped Apertures and High Gain

<div class="module-toc">
  <a class="mt-card mt-lesson" href="L10-patch-slot-horn/index.html">
    <span class="mt-kind">Lesson 10</span>
    <h4>Patch, Slot, and Horn Antennas</h4>
    <p>Radiation mechanism, pattern, and use cases for patch, slot, and horn antennas. Objective 2.3.</p>
  </a>
  <a class="mt-card mt-lesson" href="L11-high-gain-antennas/index.html">
    <span class="mt-kind">Lesson 11</span>
    <h4>High-Gain Antennas</h4>
    <p>Reflectors, Yagi-Uda, and arrays — how they get gain. Midterm project introduced. Objective 2.4.</p>
  </a>
</div>
::::

::::{frame} Lessons 12-14: Measuring What You Built

<div class="module-toc">
  <a class="mt-card mt-lesson" href="L12-pattern-measurement-theory/index.html">
    <span class="mt-kind">Lesson 12</span>
    <h4>Pattern Measurement Theory</h4>
    <p>Anechoic chambers, near-field / far-field transformations, and standard gain horns. Objective 2.5.</p>
  </a>
  <a class="mt-card mt-lesson" href="L13-measurement-lab-sparams/index.html">
    <span class="mt-kind">Lesson 13</span>
    <h4>Measurement Lab 1 — Impedance and S-parameters</h4>
    <p>Measure impedance and S-parameters on a vector network analyzer. Objective 2.6.</p>
  </a>
  <a class="mt-card mt-lesson" href="L14-measurement-lab-patterns/index.html">
    <span class="mt-kind">Lesson 14</span>
    <h4>Measurement Lab 2 — Radiation Patterns</h4>
    <p>Measure a radiation pattern and extract gain, beamwidth, sidelobe level, and polarization. Objective 2.7.</p>
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
