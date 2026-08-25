# L4 Lab — Matching Procedures

This lab is the measurement half of Lesson 4. You designed an L-network on
paper; here you build one and watch a vector network analyzer tell you whether
you were right.

## Learning Objectives

<ol class="lo-list lo-sublist" style="--module: '1'; --lo: '4'">
  <li>I can calibrate a VNA to a defined reference plane and explain why every cable change invalidates the calibration.</li>
  <li>I can measure the complex impedance of a load and read its position on the Smith chart.</li>
  <li>I can design, build, and verify an L-network that matches a complex load to a 50 ohm line.</li>
  <li>I can measure the bandwidth a match holds and connect it to the network's quality factor.</li>
</ol>

## What you will do

**Part I — measurement.** Calibrate the NanoVNA over 50 kHz to 5 MHz with an
open, short, and load, then measure a series of known loads: an open, a short, a
capacitor across a frequency sweep, a matched 50 Ω resistor, and a 1 kΩ
mismatch. You finish by characterizing an unknown filter as a black box.

**Part II — design and build.** You are handed a stand-in for an electrically
small antenna: a 15 Ω resistor in series with a 1 nF capacitor, which at 2 MHz
presents about $15 - j79.6\ \Omega$ — a small radiation resistance behind a
large capacitive reactance, exactly the situation Lesson 4 described. Unmatched,
that is a 12:1 VSWR. You design an L-network for it, build it, and measure the
improvement, then sweep to find the band over which the match survives.

## Equipment

Beyond the VNA and its cables, each team needs four components:

| Part | Marked | Role |
| :-- | :-- | :-- |
| 15 Ω resistor | 15 Ω | mock antenna, radiation resistance |
| 1 nF capacitor | 0.001 µF | mock antenna, series reactance |
| 8.2 µH inductor | 8.2 µH | matching network, series element |
| 2.2 nF capacitor | 0.0022 µF | matching network, shunt element |

Watch the units on the two capacitors — 0.001 µF and 0.0022 µF differ by
roughly a factor of two, and swapping them will not work. **Measure your actual
capacitors before you build**; a part marked 0.0022 µF may well measure 2.14 nF,
and you will need that number to explain your results.

## Before lab

Read the whole packet, skim the
<a href="https://nanorfe.com/nanovna-v2-user-manual.html" target="_blank" rel="noopener">VNA user's guide</a>,
and **work the Part II design by hand** so you arrive with component values
already in front of you. The
<a href="../L04-impedance-feeding-baluns/index.html">Lesson 4 page</a> walks the
same design one step at a time, and the feed-match widget there lets you check
your answer on a Smith chart before you touch a component.

## Lab packet

The lab sheet is the turn-in document:
<a href="../../labs/ECE444_Lab_L04_Matching_blank.pdf" target="_blank" rel="noopener">Lab sheet (PDF)</a>.
It already contains a blank Smith chart to plot on. If you want spares, or a
combined impedance-admittance chart for the Part II design:

- <a href="../../handouts/SmithChart_blank.pdf" target="_blank" rel="noopener">Blank Smith chart (PDF, print)</a> — the same chart bound into the packet.
- <a href="../../handouts/SmithChart_ZY_colour.pdf" target="_blank" rel="noopener">Impedance-admittance chart (PDF, colour)</a> — red impedance grid over blue admittance grid. This is the one to use when you cross from $Z$ to $Y$ in Step 5 of the design.
- <a href="../../handouts/SmithChart_blank.svg" target="_blank" rel="noopener">Blank Smith chart (SVG)</a> — vector, for zooming on screen.

## Where this is going

Matching is the last piece of the antenna-as-a-circuit picture. From here Lesson
5 leaves the terminals behind and asks where the radiated field actually
begins — the field regions — which is the question you have to answer before you
can measure a pattern at all. The VNA skills you build here return in Module 2,
where S-parameters become the standard language for describing every antenna and
network you meet.
