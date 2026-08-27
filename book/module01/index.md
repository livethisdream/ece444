---
frame_view: true
nav: Foundations
---

# Module 1 — Foundations of Electromagnetics and Antennas

::::{frame}
:class: title-frame

<div class="course-mark">ECE 444 · Module 01</div>

<h1 class="frame-title">Foundations of Electromagnetics and Antennas</h1>

<div class="title-rule"></div>

Ground the physics before you trust a pattern.

Lessons 1–6 · Antennas, Phased Arrays, and Radar Systems · Dr. Neil Rogers
::::

::::{frame} Where this module goes
We start with what an antenna is and why it matters, then trace the chain from
Maxwell's equations to the plane wave, define the headline antenna parameters —
gain, directivity, effective aperture, beamwidth — and end with the radiation
integrals.

Those integrals are the machinery that turns a current distribution into a
far-field pattern. **Module 3 runs them backwards to design arrays**, so the
work here is the foundation the rest of the course stands on.

:::{depth}
By the end of this module you can read a radiation pattern and predict how a
real antenna will behave in a link — which is the difference between quoting a
gain figure off a datasheet and knowing what it will do at range, in the
polarization you actually have, at the distance you can actually stand.
:::
::::

::::{frame} Learning objectives — 1.1 to 1.3

<ol class="lo-list" style="--module: '1'">
  <li>I can explain what an antenna is, describe its role in a wireless system, and recognize common antenna types by sight.</li>
  <li>I can define and calculate fundamental antenna properties — gain, directivity, effective aperture, beamwidth, and sidelobe level — apply the reciprocity principle that links an antenna's transmit and receive behavior, and use the Friis transmission equation to predict received power in a link.</li>
  <li>I can determine the polarization of an antenna and describe the bandwidth characteristics of common antenna types.</li>
</ol>
::::

::::{frame} Learning objectives — 1.4 to 1.6

<ol class="lo-list" start="4" style="--module: '1'">
  <li>I can calculate input impedance, feed considerations, and the role of baluns in an antenna feed system.</li>
  <li>I can identify and distinguish the reactive near-field, radiating near-field, and far-field regions and calculate the boundaries for a given antenna.</li>
  <li>I can set up and interpret the radiation integrals to derive the far-field pattern of a current distribution.</li>
</ol>
::::

::::{frame} Lessons 1–3 — what an antenna is, and how we describe it

<div class="module-toc">
  <a class="mt-card mt-lesson" href="L01-course-intro/index.html">
    <span class="mt-kind">Lesson 1</span>
    <h4>Course Introduction</h4>
    <p>What an antenna is, why antennas matter to the Air Force mission, and how ECE 444 is organized. Objective 1.1.</p>
  </a>
  <a class="mt-card mt-lesson" href="L02-antenna-properties/index.html">
    <span class="mt-kind">Lesson 2</span>
    <h4>Basic Properties and Terminology</h4>
    <p>From Maxwell's equations to the plane wave; radiation intensity, directivity, gain, effective area, and pattern parameters. Objective 1.2.</p>
  </a>
  <a class="mt-card mt-lesson" href="L03-polarization-bandwidth/index.html">
    <span class="mt-kind">Lesson 3</span>
    <h4>Polarization and Bandwidth</h4>
    <p>Linear, circular, and elliptical polarization; axial ratio and polarization loss; impedance / pattern / polarization bandwidth; Chu-Harrington. Objective 1.3.</p>
  </a>
</div>
::::

::::{frame} Lessons 4–6 — the terminals, the space around them, and the integral

<div class="module-toc">
  <a class="mt-card mt-lesson" href="L04-impedance-feeding-baluns/index.html">
    <span class="mt-kind">Lesson 4</span>
    <h4>Impedance, Feeding, and Baluns</h4>
    <p>Input impedance, feed-point matching, and the role of baluns in an antenna feed system. Objective 1.4.</p>
  </a>
  <a class="mt-card mt-lesson" href="L05-field-regions/index.html">
    <span class="mt-kind">Lesson 5</span>
    <h4>Field Regions</h4>
    <p>Reactive near-field, radiating near-field, and far-field — boundaries and why they matter. Objective 1.5.</p>
  </a>
  <a class="mt-card mt-lesson" href="L06-radiation-integrals/index.html">
    <span class="mt-kind">Lesson 6</span>
    <h4>Radiation Integrals</h4>
    <p>Setting up the radiation integrals to get the far-field pattern from a current distribution. Objective 1.6.</p>
  </a>
</div>
::::

::::{frame} Where this is going
**Module 2** takes these foundations to real antenna types — dipoles, loops,
patches, horns — and to the bench, where you measure the numbers you have so
far only calculated.

The through-line: everything in Module 1 is about one antenna in isolation.
From Module 3 onward, antennas start working in groups.
::::
