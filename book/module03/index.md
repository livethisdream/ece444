---
nav: Arrays
frame_view: true
---

# Module 3 — Arrays and ADALM-PHASER Beamforming

::::{frame}
:class: title-frame

<div class="course-mark">ECE 444 · Module 03</div>

<h1 class="frame-title">Arrays and ADALM-PHASER Beamforming</h1>

<div class="title-rule"></div>

Point the beam without moving the antenna.

Lessons 15–28 · Antennas, Phased Arrays, and Radar Systems · Dr. Neil Rogers
::::

::::{frame} Where this module goes
An array is many small antennas behaving as one large one. Feed the elements
with the right phases and the beam points where you choose; feed them with the
right amplitudes and you decide how much energy leaks into the sidelobes.

This is the longest module in the course, and the most hands-on. **Every
theory lesson is followed by a lab on the ADALM-PHASER**, so you never take
the array factor on faith.

:::{depth}
The through-line is one equation — the array factor — met four times: derived,
steered, tapered, and nulled. Each time it is the same sum over elements with
different weights. If you leave this module able to write that sum from memory
and say what each term does, the rest is arithmetic.
:::
::::

::::{frame} Learning objectives — 3.1 to 3.3

<ol class="lo-list" style="--module: '3'">
  <li>I can describe aperture distributions and calculate aperture efficiency for a given illumination.</li>
  <li>I can derive the array factor for an arbitrary linear array and apply pattern multiplication.</li>
  <li>I can identify the hardware architecture of the ADALM-PHASER and control it via SDR software.</li>
</ol>
::::

::::{frame} Learning objectives — 3.4 to 3.6

<ol class="lo-list" start="4" style="--module: '3'">
  <li>I can calculate the phase weights required to steer a beam to a given angle and predict the resulting array pattern.</li>
  <li>I can implement beam steering on the ADALM-PHASER and verify the steered pattern against theory.</li>
  <li>I can distinguish between array factor and true antenna pattern and account for element pattern effects.</li>
</ol>
::::

::::{frame} Learning objectives — 3.7 to 3.9

<ol class="lo-list" start="7" style="--module: '3'">
  <li>I can apply amplitude tapering (uniform, cosine, Chebyshev, Taylor) to control sidelobe level and predict the pattern trade-off.</li>
  <li>I can identify beam squint and quantization effects in a phased array and describe their impact on system performance.</li>
  <li>I can calculate null-steering weights and implement pattern nulls on the ADALM-PHASER.</li>
</ol>
::::

::::{frame} Lessons 15–17 — from aperture to array, and the hardware

<div class="module-toc">
  <a class="mt-card mt-lesson" href="L15-aperture-distributions/index.html">
    <span class="mt-kind">Lesson 15</span>
    <h4>Aperture Distributions and Efficiency</h4>
    <p>Aperture distributions and aperture efficiency for a given illumination. Objective 3.1.</p>
  </a>
  <a class="mt-card mt-lesson" href="L16-array-factor/index.html">
    <span class="mt-kind">Lesson 16</span>
    <h4>The Array Factor and Pattern Multiplication</h4>
    <p>Array factor for a linear array and pattern multiplication. Objective 3.2.</p>
  </a>
  <a class="mt-card mt-lesson" href="L17-phased-array-hardware/index.html">
    <span class="mt-kind">Lesson 17</span>
    <h4>Introduction to Phased Array Hardware</h4>
    <p>ADALM-PHASER architecture and SDR control. Objective 3.3.</p>
  </a>
</div>
::::

::::{frame} Lessons 18–21 — steering the beam, and proving it

<div class="module-toc">
  <a class="mt-card mt-lesson" href="L18-beam-steering-theory/index.html">
    <span class="mt-kind">Lesson 18</span>
    <h4>Beam Steering Theory</h4>
    <p>Phase weights to steer a beam and the resulting array pattern. Objective 3.4.</p>
  </a>
  <a class="mt-card mt-lesson" href="L19-beam-steering-lab/index.html">
    <span class="mt-kind">Lesson 19</span>
    <h4>Beam Steering Lab</h4>
    <p>Implement beam steering on the PHASER and verify against theory. Objective 3.5.</p>
  </a>
  <a class="mt-card mt-lesson" href="L20-array-factor-beamwidth/index.html">
    <span class="mt-kind">Lesson 20</span>
    <h4>Array Factor and Beamwidth Theory</h4>
    <p>Array factor and beamwidth in depth. Midterm project due. Objective 3.2.</p>
  </a>
  <a class="mt-card mt-lesson" href="L21-array-factor-lab/index.html">
    <span class="mt-kind">Lesson 21</span>
    <h4>Array Factor Lab</h4>
    <p>Measure the array factor on the PHASER. Objective 3.2.</p>
  </a>
</div>
::::

::::{frame} Lessons 22–25 — the real pattern, and shaping it

<div class="module-toc">
  <a class="mt-card mt-lesson" href="L22-antenna-pattern-theory/index.html">
    <span class="mt-kind">Lesson 22</span>
    <h4>Antenna Pattern Theory</h4>
    <p>True antenna pattern vs. array factor; element-pattern effects. Objective 3.6.</p>
  </a>
  <a class="mt-card mt-lesson" href="L23-antenna-pattern-lab/index.html">
    <span class="mt-kind">Lesson 23</span>
    <h4>Antenna Pattern Lab</h4>
    <p>AUT pattern measurement using the PHASER. Objective 3.6.</p>
  </a>
  <a class="mt-card mt-lesson" href="L24-sidelobes-tapering/index.html">
    <span class="mt-kind">Lesson 24</span>
    <h4>Sidelobes and Tapering Theory</h4>
    <p>Amplitude tapering (uniform, cosine, Chebyshev, Taylor) and the sidelobe trade-off. Objective 3.7.</p>
  </a>
  <a class="mt-card mt-lesson" href="L25-tapering-lab/index.html">
    <span class="mt-kind">Lesson 25</span>
    <h4>Tapering Lab</h4>
    <p>Apply tapers on the PHASER and measure the sidelobe trade-off. Objective 3.7.</p>
  </a>
</div>
::::

::::{frame} Lessons 26–28 — where arrays misbehave, and nulling

<div class="module-toc">
  <a class="mt-card mt-lesson" href="L26-beam-squint-quantization/index.html">
    <span class="mt-kind">Lesson 26</span>
    <h4>Beam Squint and Quantization</h4>
    <p>Beam squint and phase-quantization effects on array performance. Objective 3.8.</p>
  </a>
  <a class="mt-card mt-lesson" href="L27-null-steering-theory/index.html">
    <span class="mt-kind">Lesson 27</span>
    <h4>Null Steering Theory</h4>
    <p>Null-steering weights and pattern nulls. Objective 3.9.</p>
  </a>
  <a class="mt-card mt-lesson" href="L28-null-steering-lab/index.html">
    <span class="mt-kind">Lesson 28</span>
    <h4>Null Steering Lab</h4>
    <p>Implement pattern nulls on the PHASER. Objective 3.9.</p>
  </a>
</div>
::::

::::{frame} Where this is going
**Module 4** gives the array something to look for. The same hardware becomes
a radar: send a chirp, listen for the echo, and work out how far away the
target is and how fast it is moving.

The null steering you learn at the end of this module is what the capstone
uses to ignore a jammer.
::::
