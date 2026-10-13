---
nav: Capstone
frame_view: true
---

# Module 5 — Capstone Project

::::{frame}
:class: title-frame

<div class="course-mark">ECE 444 · Module 05</div>

<h1 class="frame-title">Capstone Project</h1>

<div class="title-rule"></div>

Detect it. Classify it. Track it. Defend the design.

Lessons 39–41 · Antennas, Phased Arrays, and Radar Systems · Dr. Neil Rogers
::::

::::{frame} Where This Module Goes
Everything the course has built arrives here at once: beam steering and
tapering from Module 3, FMCW detection from Module 4, on the hardware you have
been using all semester.

**One target, three jobs.** Detect it, classify it from its micro-Doppler
signature, and track it, then brief the trade-offs you chose and why.

:::{depth}
The scenario is deliberately over-constrained: one moving target on a taped
course, one array, and three questions to answer about it: is something there,
what is it, and where is it going. Every choice spends something. A taper that
lowers the sidelobes widens the beam the angle track leans on, and a longer
window that sharpens the spectrogram slows the track's updates. Knowing where
you spent it, and being able to say so under questioning, is the point of the
briefing.
:::
::::

::::{frame} Learning Objectives 5.1-5.3

<ol class="lo-list" style="--module: '5'">
  <li>I can choose and justify array steering and taper weights to optimize detection performance for a specified scenario.</li>
  <li>I can integrate FMCW radar processing with a phased-array front-end to track a moving target.</li>
  <li>I can classify a detected target from its micro-Doppler signature and report the classifier's accuracy.</li>
</ol>
::::

::::{frame} Learning Objective 5.4

<ol class="lo-list" start="4" style="--module: '5'">
  <li>I can present system performance results and defend engineering trade-offs in a technical briefing.</li>
</ol>
::::

::::{frame} Lessons 39-41: The Capstone

<div class="module-toc">
  <a class="mt-card mt-lesson" href="L32-final-project/index.html">
    <span class="mt-kind">Lesson 39</span>
    <h4>Final Project Kickoff</h4>
    <p>Capstone scenario, teams, and plan: detect, classify, and track a moving target. Objective 5.1.</p>
  </a>
  <a class="mt-card mt-lesson" href="L40-array-optimization/index.html">
    <span class="mt-kind">Lesson 40</span>
    <h4>Phase 1 — Array Optimization</h4>
    <p>Choose steering and taper weights and evaluate detection performance. Objective 5.1.</p>
  </a>
  <a class="mt-card mt-lesson" href="L41-radar-integration/index.html">
    <span class="mt-kind">Lesson 41</span>
    <h4>Phase 2 — Radar Integration and Demonstration</h4>
    <p>Integrate FMCW detection, micro-Doppler classification, and tracking, overlay tracks on the array pattern, and brief the results. Objectives 5.2, 5.3, 5.4.</p>
  </a>
</div>
::::
