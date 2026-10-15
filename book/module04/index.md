---
nav: Radar
frame_view: true
---

# Module 4 — Radar Fundamentals and FMCW

::::{frame}
:class: title-frame

<div class="course-mark">ECE 444 · Module 04</div>

<h1 class="frame-title">Radar Fundamentals and FMCW</h1>

<div class="title-rule"></div>

Send it, hear it come back, and work out what is out there.

Lessons 25–31 · Antennas, Phased Arrays, and Radar Systems · Dr. Neil Rogers
::::

::::{frame} Where This Module Goes
Radar is the antenna course with a clock attached. The radar equation says
whether you will hear the echo at all; range, resolution and Doppler say what
you can tell about the thing that sent it back.

Then it gets real: **FMCW on the PHASER**, processed into range, a range
waterfall, range-Doppler, MTI, and CFAR — the same chain a fielded radar runs.
You build that chain one lab at a time, and **the four labs are the final
project**.

:::{depth}
Detection is a decision under noise, not a measurement. Probability of
detection and false-alarm rate move together, and CFAR exists because the
noise floor will not hold still. The module then ends on what a radar does
with a detection once it has one: classify it from its micro-Doppler
signature, and track it in range and angle.
:::
::::

::::{frame} Learning Objectives 4.1-4.3

<ol class="lo-list" style="--module: '4'">
  <li>I can apply the radar equation to calculate received power for a given geometry, and account for path loss and radar cross section (RCS).</li>
  <li>I can calculate range resolution, unambiguous range, and Doppler shift for a given radar waveform.</li>
  <li>I can apply radar detection theory (PD, FAR, dwell time) to determine detection performance under noise.</li>
</ol>
::::

::::{frame} Learning Objectives 4.4-4.6

<ol class="lo-list" start="4" style="--module: '4'">
  <li>I can describe FMCW radar operation and configure an FMCW waveform on the ADALM-PHASER.</li>
  <li>I can process FMCW radar data to produce range, range-waterfall, and range-Doppler results.</li>
  <li>I can implement moving target indication (MTI) processing to distinguish moving targets from clutter.</li>
</ol>
::::

::::{frame} Learning Objectives 4.7-4.9

<ol class="lo-list" start="7" style="--module: '4'">
  <li>I can apply constant false-alarm rate (CFAR) processing to radar data and evaluate detection performance.</li>
  <li>I can integrate FMCW radar processing with a phased-array front-end to track a moving target.</li>
  <li>I can classify a detected target from its micro-Doppler signature and report the classifier's accuracy.</li>
</ol>
::::

::::{frame} Lessons 25-27: The Equation, and What It Takes to Detect

<div class="module-toc">
  <a class="mt-card mt-lesson" href="L25-radar-equation/index.html">
    <span class="mt-kind">Lesson 25</span>
    <h4>The Radar Equation, Path Loss, and RCS</h4>
    <p>Radar equation, path loss, and radar cross section. Objective 4.1.</p>
  </a>
  <a class="mt-card mt-lesson" href="L26-range-resolution-doppler/index.html">
    <span class="mt-kind">Lesson 26</span>
    <h4>Range, Resolution, and Doppler</h4>
    <p>Range resolution, unambiguous range, Doppler shift, and radar types. Objective 4.2.</p>
  </a>
  <a class="mt-card mt-lesson" href="L27-radar-detection/index.html">
    <span class="mt-kind">Lesson 27</span>
    <h4>Radar Detection</h4>
    <p>Detection theory: probability of detection, false-alarm rate, and dwell time under noise. Objective 4.3.</p>
  </a>
</div>
::::

::::{frame} Lessons 28-29: FMCW Range and Doppler on the Bench

<div class="module-toc">
  <a class="mt-card mt-lesson" href="L28-fmcw/index.html">
    <span class="mt-kind">Lesson 28</span>
    <h4>FMCW on the Phaser</h4>
    <p>FMCW operation and configuring an FMCW waveform on the PHASER. Objective 4.4.</p>
  </a>
  <a class="mt-card mt-practice mt-lab" href="L28-lab-fmcw-range/index.html">
    <span class="mt-kind">L28 Lab</span>
    <h4>FMCW Range</h4>
    <p>Range and the range waterfall from one FMCW capture. Objectives 4.2, 4.5.</p>
  </a>
  <a class="mt-card mt-lesson" href="L29-range-doppler-mti/index.html">
    <span class="mt-kind">Lesson 29</span>
    <h4>Range-Doppler and MTI</h4>
    <p>Range-Doppler processing of a burst of chirps, and MTI to separate movers from clutter. Objectives 4.5, 4.6.</p>
  </a>
  <a class="mt-card mt-practice mt-lab" href="L29-lab-range-doppler-mti/index.html">
    <span class="mt-kind">L29 Lab</span>
    <h4>Range-Doppler and MTI</h4>
    <p>The range-Doppler map and MTI on your own kit.</p>
  </a>
</div>
::::

::::{frame} Lessons 30-31: Detect, Classify, and Track

<div class="module-toc">
  <a class="mt-card mt-lesson" href="L30-cfar/index.html">
    <span class="mt-kind">Lesson 30</span>
    <h4>CFAR Processing</h4>
    <p>Constant false-alarm-rate processing. Objective 4.7.</p>
  </a>
  <a class="mt-card mt-practice mt-lab" href="L30-lab-cfar/index.html">
    <span class="mt-kind">L30 Lab</span>
    <h4>CFAR Processing</h4>
    <p>Apply CFAR to radar data and evaluate detection performance.</p>
  </a>
  <a class="mt-card mt-lesson" href="L31-classification-tracking/index.html">
    <span class="mt-kind">Lesson 31</span>
    <h4>Classification and Tracking</h4>
    <p>Micro-Doppler classification and range and angle tracking. Objectives 4.8, 4.9.</p>
  </a>
  <a class="mt-card mt-practice mt-lab" href="L31-lab-spectrogram/index.html">
    <span class="mt-kind">L31 Lab</span>
    <h4>Micro-Doppler Spectrogram</h4>
    <p>Record a moving target's spectrogram and classify it. Objective 4.9.</p>
  </a>
</div>
::::

::::{frame} The Final Project
- **The L28-L31 Labs are the final project**, 30% of the course grade.
- One radar chain, a stage per lab: range, range-Doppler and MTI, CFAR, classification.
- Each lab starts from your code and data from the one before.

<div class="module-toc">
  <a class="mt-card mt-lesson" href="final-project/index.html">
    <span class="mt-kind">Final Project</span>
    <h4>Radar Lab Portfolio</h4>
    <p>What is graded, how the four labs build on each other, and how they are scored.</p>
  </a>
</div>
::::
