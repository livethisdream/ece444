---
frame_view: true
---

# L10 - Measurement Lab 1: Impedance and S-parameters

::::{frame}
:class: title-frame

<div class="course-mark">ECE 444 · Fall 2026</div>

<h1 class="frame-title">Measurement Lab 1: Impedance and S-parameters</h1>

<div class="title-rule"></div>

Today the prediction meets a real piece of wire and a real instrument.

Lesson 10 Lab · Antennas, Phased Arrays, and Radar Systems · Dr. Neil Rogers
::::

::::{frame} Slides
:class: read-only

:::{admonition} Slides
:class: slides
<a href="../../slides/L10-measurement-lab-sparams.html" target="_blank" rel="noopener">html slides</a>
<a href="../../slides/L10-measurement-lab-sparams.html?print-pdf" target="_blank" rel="noopener">pdf slides</a>
<a href="../../slides/L10-measurement-lab-sparams.md" target="_blank" rel="noopener">raw markdown slides</a>
:::
::::

::::{frame} Learning Objectives

<ol class="lo-list lo-sublist" style="--module: '2'; --lo: '6'">
  <li>I can set up a one-port sweep on a vector network analyzer, run a short-open-load calibration at the correct reference plane, and verify the calibration before I trust any reading.</li>
  <li>I can measure an antenna's reflection versus frequency and read its resonance, its impedance at resonance, and its −10 dB impedance bandwidth off the trace and off the Smith chart.</li>
  <li>I can compare a measured resonance against a $\lambda/2$ prediction and say, from the sign of the reactance, which way to trim the element.</li>
  <li>I can perturb an antenna's near-field environment one variable at a time and report what moved, in which direction, and by how much.</li>
</ol>

:::{depth}
Lesson 9 did the explaining. It set out what the analyzer measures, why
calibration is a statement about where zero is rather than about accuracy,
what the reference plane does to your numbers, and what a one-port measurement
can never tell you. None of that is repeated here, and you should have it open
beside you. Today is a lab period: you will be standing at an instrument for
most of it, and everything below is procedure, judgment at the bench, and what
to write down.
:::
::::

::::{frame} What You Are Doing Today
:::{present}
- Calibrate an analyzer, then prove the calibration is good.
- Measure one antenna's resonance, impedance, and bandwidth.
- Break it three ways on purpose and record what each does.
:::

Lesson 7 told you a half-wave dipole should sit near $73 + j42.5\ \Omega$ and
resonate slightly short of $\lambda/2$. By the end of the period you will know
what your particular piece of wire actually does, how far that is from the
prediction, and which of the two you believe.

:::{depth}
The single most useful habit this lab can leave you with is the order of
operations: calibrate, *verify*, then measure. An unverified calibration is an
unmeasured antenna, and the difference costs about ninety seconds to check and
an afternoon to discover afterwards.
:::
::::

::::{frame} Rehearse the Chart First
:class: viz-frame

:::{present}
<iframe src="../../viz/s11-smith.html"
        width="100%" height="549"
        style="border: 1px solid #cddce9; border-radius: 6px;"
        loading="lazy"
        title="An antenna resonance shown as an S11 dip in dB and as a Smith-chart locus, with linked marker, impedance, VSWR, and −10 dB bandwidth readouts.">
</iframe>
:::

:::{depth}
Ten minutes on this before you touch the instrument. It shows one physical
resonance in both languages at once; drag across either plot and the marker
tracks the same frequency on both. Watch three things. First, the dip in dB,
the real-axis crossing on the chart, and the VSWR minimum are the *same event*
seen three ways — which is Lesson 9's "four names for one number" made
visible. Second, slide $R$ at resonance away from $50\ \Omega$ and the dip
gets shallower while the resonant frequency does not move: mismatch and
resonance are independent. Third, raise $Q$ and the bandwidth pinches shut,
which is why fat conductors are wideband and thin ones are not.

Everything you do on this widget you will do again in twenty minutes on your
own trace, where the curve is noisier and nobody labels the resonance for you.
:::
::::

::::{frame} Equipment
:::{present}
- A VNA, bench or NanoVNA.
- A cal kit: short, open, $50\ \Omega$ load.
- One test cable, and a torque wrench.
- A dipole with a known nominal resonance.
- A foam block.
:::

Either class of instrument works, and the steps below are written for both. A
torque wrench is worth using if the bench has one: an under-tightened SMA
connector is a slow, intermittent way to lose a calibration. The foam is
not optional equipment — it is what lets you take your hands off the antenna
while you read the screen, and Lesson 9 explained why that matters.
::::

::::{frame} Step 1 — Set the Sweep
:::{present}
- Bracket the expected resonance by roughly $\pm 30\%$.
- At least **401 points**.
- Write the settings down before you calibrate.
:::

Changing the sweep after calibration invalidates the cal on some instruments
and silently interpolates on others. Neither is something you want to discover
from your data, so fix the sweep first and leave it alone.
::::

::::{frame} Step 2 — Calibrate, Then Verify
:::{present}
- Short, open, and load at the **far end of the cable**, not the front panel.
- Then keep the cable still. Flexing it changes its phase.
:::
:::{present}
:class: callout
Reconnect the load: $\vert S_{11}\vert < -30$ dB across the band.
**Screenshot it.**
:::

That screenshot is a deliverable, and it is the evidence that your data means
anything at all. Calibrating at the far end of the cable is what makes the
reference plane sit where you want it; calibrating at the front panel leaves
the whole cable inside your device under test.
::::

::::{frame} Step 3 — Measure the Antenna
:::{present}
Connect it, set it on the foam, and take your hands off. Record:

- the resonant frequency, as the dip **and** as the real-axis crossing,
- $Z$ at resonance, from the marker,
- both −10 dB crossing frequencies.
:::

Reading the resonance twice, once on each plot, is not busywork. The two
readings disagree when something is wrong with the reference plane, and that
disagreement is the cheapest diagnostic you have.
::::

::::{frame} Step 4 — Compare Against Prediction
:::{present}
- Is the measured resonance **above or below** a $\lambda/2$ calculation?
- Which way would you trim the element?
- Write the answer down before you move on.
:::

The sign of the reactance answers the second question on its own, and Lesson 9
worked the inference: negative reactance is capacitive, the element is
electrically short, and it wants to be longer. Committing to an answer in
writing before you check it is the whole point of the step.
::::

::::{frame} Step 5 — Perturb, One Variable at a Time
:::{present}
Repeat resonance, impedance, and bandwidth for three configurations:

- held clear, in free space,
- with a hand 2 to 3 cm from the element,
- lying flat on the bench.
:::

One variable at a time, and record all three fully — you are producing the
data for the table in your report, and a configuration you measured
incompletely is one you will have to set up again. Lesson 9 predicted the
direction of each shift; your job is the magnitude.
::::

::::{frame} Two Failure Modes
:::{present}
:class: callout
Most bad lab data comes from two mistakes: **calibrating with one cable and
measuring with another**, and **gripping the coax at the feed point** while
you read the screen.
:::

The second one is the cruel one, because you have then perturbed the very
measurement you are recording, and the trace looks entirely plausible. Set the
antenna down on the foam stand and take your hands off it.
::::

::::{frame} Deliverables
:::{present}
One page, at the start of Lesson 15:

1. An annotated $\vert S_{11}\vert$ plot, resonance and both crossings marked.
2. A results table for all three configurations.
3. A Smith-chart screenshot with the resonance identified.
4. A paragraph on the perturbations.
:::

:::{depth}
In detail:

1. **An annotated $\vert S_{11}\vert$ plot.** Resonance marked, both −10 dB
   crossings marked, axes labeled with units.
2. **A results table**: $f_0$, $Z$ at resonance, −10 dB bandwidth in MHz and
   in percent, for all three perturbation configurations.
3. **A Smith-chart screenshot** with the resonance point marked, and one
   sentence identifying it as the real-axis crossing.
4. **A paragraph on the perturbation results.** What moved, in which
   direction, by how much, and why. Connect at least one observation to the
   near-field argument from Lesson 9.

A plot with no markers and no units is a screenshot rather than a measurement,
and the paragraph carries the largest share of the grade.
:::
::::

::::{frame} The Bench Card
:class: read-only

| At the bench | What to do | What good looks like |
| :-- | :-- | :-- |
| Sweep | $\pm 30\%$ around resonance, $\ge 401$ points | settings written down |
| Calibrate | short, open, load at the cable end | cable then left alone |
| Verify | reconnect the load | $\vert S_{11}\vert < -30$ dB, screenshotted |
| Measure | dip *and* real-axis crossing | the two agree |
| Bandwidth | width below −10 dB | 3 to 10% for a thin dipole |
| Perturb | free space, hand, bench | three complete rows |

The sanity range in the bandwidth row is the one number worth memorizing: if
you measure 1%, suspect the setup before you suspect the antenna, because a
resonant length of feed cable can manufacture a narrow dip that has nothing to
do with the element.
::::

::::{frame} Practice
:class: read-only

- <a href="../../practice/ECE444_L10_Practice_blank.pdf" target="_blank" rel="noopener">Problem set (PDF)</a>
- <a href="../../practice/ECE444_L10_Practice_SOLUTIONS.pdf" target="_blank" rel="noopener">Solutions (PDF)</a>
::::

::::{frame} Where This Is Going
:::{present}
- Today established that power went **in**.
- Lesson 11 establishes that it came back **out**, and in which direction.
- Together they are the complete characterization of one element.
:::

A VNA cannot see radiation, only mismatch, so the efficiency question this lab
leaves open is answered on the range next period. Further out the skills
compound: Module 3 builds arrays from these elements, and every element in an
array sees its neighbors as a mutual impedance — precisely the $S_{11}$ shift
you produced with your hand today.

:::{depth}
The midterm project due at Lesson 20 asks you to design, build, tune, and
defend an antenna. Tuning *is* this lab: measure, read the sign of the
reactance, trim, measure again. Calibration and Smith-chart fluency are the
rate-limiting skills on that project, so practice both here, where the cost of
a mistake is an afternoon rather than a week.
:::
::::
