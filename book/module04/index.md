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

Lessons 29–38 · Antennas, Phased Arrays, and Radar Systems · Dr. Neil Rogers
::::

::::{frame} Where This Module Goes
Radar is the antenna course with a clock attached. The radar equation says
whether you will hear the echo at all; range, resolution and Doppler say what
you can tell about the thing that sent it back.

Then it gets real: **FMCW on the PHASER**, processed into range, a range
waterfall, range-Doppler, MTI, and CFAR — the same chain a fielded radar runs.

:::{depth}
Detection is a decision under noise, not a measurement. Probability of
detection and false-alarm rate move together, and CFAR exists because the
noise floor will not hold still. That is why the last two lessons of this
module are the ones the capstone leans on hardest.
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

::::{frame} Learning Objective 4.7

<ol class="lo-list" start="7" style="--module: '4'">
  <li>I can apply constant false-alarm rate (CFAR) processing to radar data and evaluate detection performance.</li>
</ol>
::::

::::{frame} Lessons 29-31: The Equation, and What It Takes to Detect

<div class="module-toc">
  <a class="mt-card mt-lesson" href="L29-radar-equation/index.html">
    <span class="mt-kind">Lesson 29</span>
    <h4>The Radar Equation, Path Loss, and RCS</h4>
    <p>Radar equation, path loss, and radar cross section. Objective 4.1.</p>
  </a>
  <a class="mt-card mt-lesson" href="L30-range-resolution-doppler/index.html">
    <span class="mt-kind">Lesson 30</span>
    <h4>Range, Resolution, and Doppler</h4>
    <p>Range resolution, unambiguous range, Doppler shift, and radar types. Objective 4.2.</p>
  </a>
  <a class="mt-card mt-lesson" href="L31-radar-detection-theory/index.html">
    <span class="mt-kind">Lesson 31</span>
    <h4>Radar Detection Theory</h4>
    <p>Detection theory: probability of detection, false-alarm rate, and dwell time under noise. Objective 4.3.</p>
  </a>
</div>
::::

::::{frame} Lessons 32-35: FMCW Range and Doppler on the Bench

<div class="module-toc">
  <a class="mt-card mt-lesson" href="L32-fmcw-intro/index.html">
    <span class="mt-kind">Lesson 32</span>
    <h4>Introduction to FMCW on Phaser</h4>
    <p>FMCW operation and configuring an FMCW waveform on the PHASER. Objective 4.4.</p>
  </a>
  <a class="mt-card mt-lesson" href="L33-range-calculations-lab/index.html">
    <span class="mt-kind">Lesson 33</span>
    <h4>Range Calculations Lab</h4>
    <p>Range calculations from FMCW data. Objective 4.2.</p>
  </a>
  <a class="mt-card mt-lesson" href="L34-range-waterfall-lab/index.html">
    <span class="mt-kind">Lesson 34</span>
    <h4>Range Waterfall Lab</h4>
    <p>Produce a range-waterfall from FMCW data. Objective 4.5.</p>
  </a>
  <a class="mt-card mt-lesson" href="L35-range-doppler-lab/index.html">
    <span class="mt-kind">Lesson 35</span>
    <h4>Range-Doppler Lab</h4>
    <p>Produce range-Doppler results from FMCW data. Objective 4.5.</p>
  </a>
</div>
::::

::::{frame} Lessons 36-38: Separating Movers from Clutter

<div class="module-toc">
  <a class="mt-card mt-lesson" href="L36-mti-lab/index.html">
    <span class="mt-kind">Lesson 36</span>
    <h4>Moving Target Indication (MTI) Lab</h4>
    <p>MTI processing to separate movers from clutter. Objective 4.6.</p>
  </a>
  <a class="mt-card mt-lesson" href="L37-cfar-theory/index.html">
    <span class="mt-kind">Lesson 37</span>
    <h4>CFAR Processing Theory</h4>
    <p>Constant false-alarm-rate processing. Objective 4.7.</p>
  </a>
  <a class="mt-card mt-lesson" href="L38-cfar-lab/index.html">
    <span class="mt-kind">Lesson 38</span>
    <h4>CFAR Processing Lab</h4>
    <p>Apply CFAR to radar data and evaluate detection performance. Objective 4.7.</p>
  </a>
</div>
::::

::::{frame} Where This Is Going
**Module 5** puts the two halves of the course together. The array from Module
3 points and nulls; the radar from Module 4 detects and tracks.

Nothing new is introduced. The capstone is the integration.
::::
