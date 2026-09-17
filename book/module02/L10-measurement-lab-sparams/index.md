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
  <li>I can set up a one-port sweep on a vector network analyzer, calibrate it at the correct reference plane, and verify the calibration before I trust any reading.</li>
  <li>I can measure an antenna's reflection versus frequency and read its resonance, its impedance at resonance, and its VSWR &le; 2 impedance bandwidth off the trace and off the Smith chart.</li>
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
- Calibrate from the dashboard, then prove the calibration is good.
- Record one antenna's reflection across a band, as a named run.
- Read resonance, impedance, and bandwidth out of the file.
- Break it three ways and record what each does.
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
        title="An antenna resonance shown as an S11 dip in dB and as a Smith-chart locus, with linked marker, impedance, VSWR, and VSWR-2 bandwidth readouts.">
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

::::{frame} The Rig
:::{present}
- The chamber's VNA, driven from the **dashboard** in a browser.
- One test cable, port 1, and a torque wrench.
- The calibration module, for the **Calibrate…** wizard.
- A dipole with a known nominal resonance, on a foam block.
:::

The instrument is the same one Lesson 11 uses for patterns; today only port 1
is doing anything. A torque wrench is worth using if the bench has one: an
under-tightened SMA connector is a slow, intermittent way to lose a
calibration.

:::{depth}
The foam is not optional equipment — it is what lets you take your hands off
the antenna while you read the screen, and Lesson 9 explained why that
matters. Standing the antenna in the chamber enforces the rule for you: with
the door shut you cannot be holding the element and reading the trace at the
same time, which is exactly the mistake this lab is trying to train out of
you.

Two tabs on the dashboard matter today and the rest do not. **VNA** shows the
sweep at the current angle, which is where you watch the trace live.
**Logs** is where the service says what it did, including any warning about
the calibration. The Pattern tab is a polar plot of angle against level, and a
one-angle run has nothing to draw there.
:::
::::

::::{frame} Step 1 — Set the Sweep
:::{present}
1. **VNA** section: start and stop bracketing the expected resonance by $\pm 30\%$.
2. **Points** at least 401. Log the IF bandwidth and power too.
3. **Parameter: S11** — one port, reflection only.
:::

Changing the sweep after calibration leaves the instrument interpolating a
correction across a span it never measured. The panel flags it and the log
warns about it, which is more warning than most instruments give you — but the
right move is to fix the sweep first and leave it alone.

:::{depth}
The default span is wide enough for a horn and wrong for your element: a
101-point sweep across a gigahertz is a 10 MHz grid, and a thin dipole's whole
VSWR $\le 2$ band can be 40 MHz. Four points across a resonance will not find
its minimum and cannot give you a crossing frequency worth quoting. This is
the one setting where the default will quietly cost you the measurement, so
change it before you calibrate, not after.
:::
::::

::::{frame} Step 2 — Calibrate, Then Verify
:::{present}
4. **Calibrate…**, and choose the reference plane: **the cable ends**, not the front panel.
5. Acknowledge, run it, put the cable back.
:::
:::{present}
:class: callout
Verify: terminate the cable in $50\ \Omega$ and run one angle.
$\vert S_{11}\vert < -30$ dB across the band. **Screenshot it.**
:::

That screenshot is a deliverable, and it is the evidence that your data means
anything at all. Calibrating at the cable ends is what puts the reference
plane where you want it; calibrating at the front panel leaves the whole cable
inside your device under test.

:::{depth}
The wizard asks you which plane you calibrated because nothing in the data
afterwards can tell. Lesson 9 made that argument on paper; the dropdown is the
argument made unavoidable, and the answer is written into the record so that a
run taken weeks later still says what it was referenced to. The **CAL /
UNCAL** pill beside the scan button is the other half: an uncalibrated run is
valid data and is never blocked, but it should not be possible to take one
without noticing.

Verifying against a load is the step that catches everything else — a cable
swapped after the calibration, a loose connector, a sweep changed without
meaning to. It works because the load is a standard the calibration did not
use to define itself, so a good answer is evidence rather than arithmetic.
:::
::::

::::{frame} Step 3 — Record the Antenna
:::{present}
6. Connect it, set it on the foam, and take your hands off.
7. **Output**: name the run. **Turntable**: set **From** and **To** to the same angle.
8. **Start scan**, and watch the VNA tab.
:::

Setting the two angle fields equal gives a one-angle run — the hint under the
grid will say so — and what it writes is a complete sweep of the reflection
at a fixed position. Anything you name is in the **Stored runs** list
afterwards, which is what makes three configurations comparable rather than
three screenshots.

:::{depth}
Every run writes `pattern.csv` and `meta.json` under `runs/`. The CSV is long
format, one row per angle and frequency, and the four columns that matter
today are `freq_hz`, `re`, `im` and `mag_db`. The `meta.json` beside it
records the sweep you used, whether error correction was on, and a copy of the
calibration record — copied rather than referenced, because the next
calibration overwrites the original and a finished run has to keep saying what
it was taken against.
:::
::::

::::{frame} Step 4 — Four Names for One Number
:::{present}
$$\Gamma = \text{re} + j\ \text{im}, \qquad
Z = Z_0 \frac{1 + \Gamma}{1 - \Gamma}, \qquad
\text{VSWR} = \frac{1 + \vert \Gamma \vert}{1 - \vert \Gamma \vert}$$

- Resonance: the dip in `mag_db`, **and** the $\text{Im}\{Z\} = 0$ crossing.
- Bandwidth: the two frequencies where VSWR $= 2$.
:::

The bar is **VSWR $\le 2$**, the same bar Lesson 4 set and Lesson 9 quoted.
Quote the bandwidth in VSWR, never in decibels: Lesson 3's rule is that the
number means nothing without the bar attached to it.

:::{depth}
This is Lesson 9's "four names for one number" done with your own hands
instead of a marker readout. The file gives you $\Gamma$ as a complex number
at every frequency; the log magnitude, the VSWR, the impedance and the
Smith-chart position are four ways of writing it down, and three lines of
Python turn any one into the others. Plotting $\Gamma$ on the unit disk *is*
the Smith chart — the chart is a grid drawn over that disk, not a different
measurement.

Reading the resonance twice, once as the dip and once as the reactance
crossing, is not busywork. The two readings disagree when something is wrong
with the reference plane, and that disagreement is the cheapest diagnostic you
have.
:::
::::

::::{frame} Step 5 — Compare Against Prediction
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

::::{frame} Step 6 — Perturb, One Variable at a Time
:::{present}
One named run each, same sweep, same calibration:

- held clear, in free space,
- with a hand 2 to 3 cm from the element,
- lying flat on the bench.
:::

One variable at a time, and record all three fully — you are producing the
data for the table in your report, and a configuration you measured
incompletely is one you will have to set up again. Lesson 9 predicted the
direction of each shift; your job is the magnitude.

:::{depth}
Name them for what they are, not for the clock: `l10_freespace`, `l10_hand`,
`l10_bench` costs four seconds each and is the difference between a reduction
session and an archaeology session. Left empty, the run name is stamped from
the date and time, which is enough to keep the runs apart and useless for
telling you which is which a week later.
:::
::::

::::{frame} Three Failure Modes
:::{present}
:class: callout
**Calibrating with one cable and measuring with another.**
**Changing the sweep after you calibrated.**
**Gripping the coax at the feed point** while you read the screen.
:::

The first two the dashboard can warn you about, and it does. The third one is
the cruel one, because nothing warns you: you have perturbed the very
measurement you are recording, and the trace looks entirely plausible. Set the
antenna down on the foam stand and take your hands off it.
::::

::::{frame} Deliverables
:::{present}
One page, at the start of Lesson 15:

1. An annotated $\vert S_{11}\vert$ plot, both crossings marked.
2. A results table for all three configurations.
3. A Smith-chart plot of $\Gamma$, resonance identified.
4. A paragraph on the perturbations.
:::

:::{depth}
In detail:

1. **An annotated $\vert S_{11}\vert$ plot.** Resonance marked, both
   VSWR $= 2$ crossings marked, axes labeled with units.
2. **A results table**: $f_0$, $Z$ at resonance, VSWR $\le 2$ bandwidth in MHz
   and in percent, for all three perturbation configurations.
3. **A Smith-chart plot of your measured $\Gamma$**, with the resonance point
   marked, and one sentence identifying it as the real-axis crossing.
4. **A paragraph on the perturbation results.** What moved, in which
   direction, by how much, and why. Connect at least one observation to the
   near-field argument from Lesson 9.

Quote the run name behind every figure, and state the reference plane you
calibrated at. A plot with no markers and no units is a screenshot rather than
a measurement, and the paragraph carries the largest share of the grade.
:::
::::

::::{frame} The Bench Card
:class: read-only

| At the bench | What to do | What good looks like |
| :-- | :-- | :-- |
| Sweep | $\pm 30\%$ around resonance, $\ge 401$ points, $S_{11}$ | settings written down |
| Calibrate | the wizard, at the cable ends | reference plane recorded |
| Verify | $50\ \Omega$ load, one-angle run | $\vert S_{11}\vert < -30$ dB, screenshotted |
| Record | one angle, named run | `pattern.csv` you can find again |
| Resonance | dip *and* reactance crossing | the two agree |
| Bandwidth | width where VSWR $\le 2$ | 3 to 10% for a thin dipole |
| Perturb | free space, hand, bench | three complete runs |

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
leaves open is answered on the range next period — same instrument, same
dashboard, the other port. Further out the skills compound: Module 3 builds
arrays from these elements, and every element in an array sees its neighbors
as a mutual impedance — precisely the $S_{11}$ shift you produced with your
hand today.

:::{depth}
The midterm project, due 2 Oct, asks you to build a dipole, tune it, measure
it, and defend the numbers you report about it. The antenna itself is not in
question — everyone builds the same one — so what you defend is the
measurement. Tuning *is* this lab: measure, read the sign of the
reactance, trim, measure again. Calibration and Smith-chart fluency are the
rate-limiting skills on that project, so practice both here, where the cost of
a mistake is an afternoon rather than a week.
:::
::::
