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

Track the mover. Ignore the jammer. Defend the design.

Lessons 39–41 · Antennas, Phased Arrays, and Radar Systems · Dr. Neil Rogers
::::

::::{frame} Where This Module Goes
Everything the course has built arrives here at once: beam steering and null
steering from Module 3, FMCW detection and tracking from Module 4, on the
hardware you have been using all semester.

**No new theory.** Three lessons, one working demonstration, and a technical
briefing in which you explain the trade-offs you chose and why.

:::{depth}
The scenario is deliberately over-constrained: a moving target you must hold,
a static jammer you must reject, and one array to do both. Every weight that
deepens the null costs you somewhere in the main beam. Knowing where you spent
it, and being able to say so under questioning, is the point of the briefing.
:::
::::

::::{frame} Learning Objectives 5.1-5.3

<ol class="lo-list" style="--module: '5'">
  <li>I can integrate beam-steering and null-steering weights to optimize array performance against a specified scenario.</li>
  <li>I can integrate FMCW radar processing with a phased-array front-end to track a moving target.</li>
  <li>I can suppress a static jammer using null steering while maintaining detection of a moving target.</li>
</ol>
::::

::::{frame} Learning Objective 5.4

<ol class="lo-list" start="4" style="--module: '5'">
  <li>I can present system performance results and defend engineering trade-offs in a technical briefing.</li>
</ol>
::::

::::{frame} Lessons 39-41: The Capstone

<div class="module-toc">
  <a class="mt-card mt-lesson" href="L39-final-project-kickoff/index.html">
    <span class="mt-kind">Lesson 39</span>
    <h4>Final Project Kickoff</h4>
    <p>Capstone scenario, teams, and plan: track a mover while suppressing a jammer. Objective 5.1.</p>
  </a>
  <a class="mt-card mt-lesson" href="L40-array-optimization/index.html">
    <span class="mt-kind">Lesson 40</span>
    <h4>Phase 1 — Array Optimization</h4>
    <p>Design beam-steering weights, implement null steering, and evaluate array performance. Objective 5.1.</p>
  </a>
  <a class="mt-card mt-lesson" href="L41-radar-integration/index.html">
    <span class="mt-kind">Lesson 41</span>
    <h4>Phase 2 — Radar Integration and Demonstration</h4>
    <p>Integrate FMCW + Doppler tracking, overlay tracks on the array pattern, and brief the results. Objectives 5.2, 5.3, 5.4.</p>
  </a>
</div>
::::
