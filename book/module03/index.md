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

Lessons 15–24 · Antennas, Phased Arrays, and Radar Systems · Dr. Neil Rogers
::::

::::{frame} Where This Module Goes
:::{present}
:class: callout

**Amplitude shapes the beam: its sidelobes and beamwidth. Phase steers it.**
:::

An array is many small antennas behaving as one large one. Feed the elements
with the right phases and the beam points where you choose; feed them with the
right amplitudes and you decide how wide the beam is and how much energy leaks
into the sidelobes.

This is the longest module in the course, and the most hands-on. **Almost
every lesson has its own lab on the ADALM-PHASER**, done right after it, so you
never take the array factor on faith.

:::{depth}
The through-line is one equation — the array factor — met four times: derived,
steered, tapered, and nulled. Each time it is the same sum over elements with
different weights. If you leave this module able to write that sum from memory
and say what each term does, the rest is arithmetic.
:::
::::

::::{frame} The Module 3 Roadmap

<div class="lane-map" role="list" aria-label="Lessons 15 to 24 by what they teach: amplitude, phase, or both">
  <span class="lm-lane lm-amp" style="--lane: 1">Amplitude<small>shapes the beam</small></span>
  <span class="lm-lane lm-phase" style="--lane: 2">Phase<small>steers it</small></span>
  <span class="lm-lane lm-both" style="--lane: 3">Both<small>the full weight</small></span>
  <a class="lm-chip lm-amp" style="--lane: 1; --n: 1" href="L15-aperture-distributions/index.html"><b>L15</b> Apertures</a>
  <a class="lm-chip lm-amp" style="--lane: 1; --n: 2" href="L16-array-factor/index.html"><b>L16</b> Array Factor</a>
  <a class="lm-chip lm-both" style="--lane: 3; --n: 3" href="L17-phased-array-hardware/index.html"><b>L17</b> Hardware and Calibration<span class="lm-lab">Lab</span></a>
  <a class="lm-chip lm-phase" style="--lane: 2; --n: 4" href="L18-beam-steering/index.html"><b>L18</b> Beam Steering<span class="lm-lab">Lab</span></a>
  <a class="lm-chip lm-phase" style="--lane: 2; --n: 5" href="L19-direction-finding/index.html"><b>L19</b> Direction Finding<span class="lm-lab">Lab</span></a>
  <a class="lm-chip lm-amp" style="--lane: 1; --n: 6" href="L20-array-factor-beamwidth/index.html"><b>L20</b> Beamwidth<span class="lm-lab">Lab</span></a>
  <a class="lm-chip lm-both" style="--lane: 3; --n: 7" href="L21-antenna-pattern/index.html"><b>L21</b> Antenna Pattern<span class="lm-lab">Lab</span></a>
  <a class="lm-chip lm-amp" style="--lane: 1; --n: 8" href="L22-sidelobes-tapering/index.html"><b>L22</b> Tapering</a>
  <a class="lm-chip lm-phase" style="--lane: 2; --n: 9" href="L23-beam-squint-quantization/index.html"><b>L23</b> Squint and Quantization<span class="lm-lab">L22–L23 Lab</span></a>
  <a class="lm-chip lm-both" style="--lane: 3; --n: 10" href="L24-null-steering/index.html"><b>L24</b> Nulling<span class="lm-lab">Lab</span></a>
</div>

:::{depth}
Every lesson in this module turns one of two knobs on each element. Lessons 15,
16, 20, and 22 work the amplitude: how the illumination across the aperture
sets the beamwidth and the sidelobe level, and what a taper trades for lower
sidelobes. Lessons 18, 19, and 23 work the phase: the progressive phase that
points the beam, the bearing it lets you measure, and what goes wrong when the
phase is only right at one frequency or comes in coarse steps. Lessons 17, 21,
and 24 need both. Calibration corrects each channel's gain and phase, the
measured pattern carries the element's own pattern on top of the array
factor, and a null is placed with complex weights.
:::
::::

::::{frame} Learning Objectives 3.1-3.3

<ol class="lo-list" style="--module: '3'">
  <li>I can describe aperture distributions and calculate aperture efficiency for a given illumination.</li>
  <li>I can derive the array factor for an arbitrary linear array and apply pattern multiplication.</li>
  <li>I can identify the hardware architecture of the ADALM-PHASER and control it via SDR software.</li>
</ol>
::::

::::{frame} Learning Objectives 3.4-3.6

<ol class="lo-list" start="4" style="--module: '3'">
  <li>I can calculate the phase weights required to steer a beam to a given angle and predict the resulting array pattern.</li>
  <li>I can implement beam steering on the ADALM-PHASER and verify the steered pattern against theory.</li>
  <li>I can distinguish between array factor and true antenna pattern and account for element pattern effects.</li>
</ol>
::::

::::{frame} Learning Objectives 3.7-3.9

<ol class="lo-list" start="7" style="--module: '3'">
  <li>I can apply amplitude tapering (uniform, cosine, Chebyshev, Taylor) to control sidelobe level and predict the pattern trade-off.</li>
  <li>I can identify grating lobes, beam squint, and quantization effects in a phased array and describe their impact on system performance.</li>
  <li>I can calculate null-steering weights and implement pattern nulls on the ADALM-PHASER.</li>
</ol>
::::

::::{frame} Lessons 15-17: From Aperture to Array, and the Hardware

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
  <a class="mt-card mt-practice mt-lab" href="L17-lab-bring-up/index.html">
    <span class="mt-kind">L17 Lab</span>
    <h4>Phased Array Bring-Up</h4>
    <p>Bring your own kit up from a blank card, then prove it works.</p>
  </a>
</div>
::::

::::{frame} Lessons 18-19: Steering the Beam, and Using It

<div class="module-toc">
  <a class="mt-card mt-lesson" href="L18-beam-steering/index.html">
    <span class="mt-kind">Lesson 18</span>
    <h4>Beam Steering</h4>
    <p>Phase weights to steer a beam and the resulting array pattern. Objective 3.4.</p>
  </a>
  <a class="mt-card mt-practice mt-lab" href="L18-lab-beam-steering/index.html">
    <span class="mt-kind">L18 Lab</span>
    <h4>Beam Steering</h4>
    <p>Steer the peak two ways on the PHASER and check it against theory. Objective 3.5.</p>
  </a>
  <a class="mt-card mt-lesson" href="L19-direction-finding/index.html">
    <span class="mt-kind">Lesson 19</span>
    <h4>Direction Finding</h4>
    <p>Bearings from the beam sweep, crossed from known positions. Objective 3.5.</p>
  </a>
  <a class="mt-card mt-practice mt-lab" href="L19-lab-fox-hunt/index.html">
    <span class="mt-kind">L19 Lab</span>
    <h4>Fox Hunt</h4>
    <p>Find the one live HB100 among numbered boxes from your own bearings.</p>
  </a>
</div>
::::

::::{frame} Lessons 20-21: The Beam, and the Real Pattern

<div class="module-toc">
  <a class="mt-card mt-lesson" href="L20-array-factor-beamwidth/index.html">
    <span class="mt-kind">Lesson 20</span>
    <h4>Array Factor and Beamwidth</h4>
    <p>Array factor and beamwidth in depth. Objective 3.2.</p>
  </a>
  <a class="mt-card mt-practice mt-lab" href="L20-lab-array-factor/index.html">
    <span class="mt-kind">L20 Lab</span>
    <h4>Array Factor</h4>
    <p>Measure the array factor at 8, 4, and 2 active elements.</p>
  </a>
  <a class="mt-card mt-lesson" href="L21-antenna-pattern/index.html">
    <span class="mt-kind">Lesson 21</span>
    <h4>Antenna Pattern</h4>
    <p>True antenna pattern vs. array factor; element-pattern effects. Objective 3.6.</p>
  </a>
  <a class="mt-card mt-practice mt-lab" href="L21-lab-antenna-pattern/index.html">
    <span class="mt-kind">L21 Lab</span>
    <h4>Antenna Pattern</h4>
    <p>Walk the source around a fixed beam to see the element pattern.</p>
  </a>
</div>
::::

::::{frame} Lessons 22-23: Shaping the Pattern, and Where It Misbehaves

<div class="module-toc">
  <a class="mt-card mt-lesson" href="L22-sidelobes-tapering/index.html">
    <span class="mt-kind">Lesson 22</span>
    <h4>Sidelobes and Tapering</h4>
    <p>Amplitude tapering (uniform, cosine, Chebyshev, Taylor) and the sidelobe trade-off. Objective 3.7.</p>
  </a>
  <a class="mt-card mt-lesson" href="L23-beam-squint-quantization/index.html">
    <span class="mt-kind">Lesson 23</span>
    <h4>Beam Squint and Quantization</h4>
    <p>Grating lobes, beam squint, and phase quantization. Objective 3.8.</p>
  </a>
  <a class="mt-card mt-practice mt-lab" href="L22-L23-lab-tapering-squint/index.html">
    <span class="mt-kind">L22–L23 Lab</span>
    <h4>Tapering, Squint, and Quantization</h4>
    <p>Measure the taper trade-off, then the three departures no taper can fix.</p>
  </a>
</div>
::::

::::{frame} Lesson 24: Nulling

<div class="module-toc">
  <a class="mt-card mt-lesson" href="L24-null-steering/index.html">
    <span class="mt-kind">Lesson 24</span>
    <h4>Null Steering</h4>
    <p>Null-steering weights and pattern nulls. Objective 3.9.</p>
  </a>
  <a class="mt-card mt-practice mt-lab" href="L24-lab-null-steering/index.html">
    <span class="mt-kind">L24 Lab</span>
    <h4>Null Steering</h4>
    <p>Implement pattern nulls on the PHASER.</p>
  </a>
</div>
::::

::::{frame} Where This Is Going
**Module 4** gives the array something to look for. The same hardware becomes
a radar: send a chirp, listen for the echo, and work out how far away the
target is and how fast it is moving.

The steering and tapering you learn in this module point and shape the
radar's beam.
::::
