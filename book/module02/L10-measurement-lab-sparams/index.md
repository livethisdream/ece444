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
  <li>I can set up a one-port sweep on a vector network analyzer, run a one-port calibration at the correct reference plane, and verify the calibration before I trust any reading.</li>
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

::::{frame} Safety and Good Practice
:::{present}
:class: callout
The RF is milliwatts. What you can wreck today is a **connector** or a
**calibration**.
:::
:::{present}
- Ground yourself before touching a center pin.
- Torque the nut; never twist the cable.
- Calibrate, **verify**, measure. In that order.
:::

None of today's hazards are to you, which is exactly why they get skipped. The
instrument is expensive, the calibration module more so per gram, and a
measurement you cannot defend costs you the afternoon that produced it.

:::{depth}
**Connectors first, because the damage spreads.** Align the connector before
you turn anything, tighten with the wrench rather than by feel, and turn the
*nut* and not the cable body — a rotated center pin ruins that connector, and
then ruins the next one it mates with, which on this rig is a calibration
module worth more than the antenna. Cap what you are not using. Do not force a
connector that does not want to start.

**Static, second.** Touch a grounded surface before you touch a center pin. An
analyzer's front end is a receiver, and it is the cheapest thing in the room
to destroy invisibly.

**Never put power into a port.** Nothing that transmits — a signal generator, a
radio, an amplifier output — goes into an analyzer port. The port is an input,
and it is not built to be driven.

**In the chamber, mind the absorber.** The pyramids shed if you brush them and
a crushed tip is a permanently worse quiet zone. Do not lean on the walls and
do not rest tools on the floor absorber.

**And the practice half**, which is the part that shows up in your grade.
Calibrate, verify, measure, in that order. Log the sweep settings before you
calibrate. Change one thing at a time. Export and name every capture as you
take it, not afterwards. And write down what you expect before you look —
a prediction you committed to is the only way a surprise can teach you
anything.
:::
::::

::::{frame} What You Are Doing Today
:::{present}
- Calibrate one port, then prove the calibration is good.
- Capture one sweep of your antenna's reflection.
- Read resonance, impedance, VSWR and bandwidth off the marker.
- Break it three ways and export a file for each.
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

The instrument you are about to use draws the same two plots from real data,
with the same marker linking them. Everything you do on this widget you will
do again in twenty minutes on your own trace, where the curve is noisier and
nobody labels the resonance for you.
:::
::::

::::{frame} The Rig
:::{present}
- The chamber's VNA, driven from the **dashboard** in a browser.
- One test cable on **port 1**, and a torque wrench.
- The calibration module, for the **Calibrate…** wizard.
- A dipole with a known nominal resonance, on a foam block.
:::

Everything today happens on the dashboard's **Sweep** tab, which captures at
the current position and never moves the tower. It is the one measurement this
rig can make with nothing but an analyzer attached.

:::{depth}
The foam is not optional equipment — it is what lets you take your hands off
the antenna while you read the screen, and Lesson 9 explained why that
matters. Standing the antenna in the chamber enforces the rule for you: with
the door shut you cannot be holding the element and reading the trace at the
same time, which is exactly the mistake this lab is trying to train out of
you.

A torque wrench is worth using if the bench has one: an under-tightened SMA
connector is a slow, intermittent way to lose a calibration.

The service will even run with no positioner attached at all, and says so —
the scan button reads *no positioner* and everything that turns the tower is
greyed out, while the Sweep tab keeps working. That is the shape of today's
measurement: one port, one sweep, nothing moving.
:::
::::

::::{frame} Step 1 — Set the Sweep
:::{present}
1. **VNA** section: start and stop bracketing the expected resonance by $\pm 30\%$.
2. **Points** at least 401. Log the IF bandwidth and power too.
3. The **Parameter** dropdown is for scans. A capture chooses its own.
:::

A capture takes its frequency settings from this same panel, so a sweep and a
scan can never quietly disagree about what was measured. Changing any of them
after you calibrate leaves the instrument interpolating a correction across a
span it never measured; the panel flags it and the log warns again.

:::{depth}
The default span is wide enough for a horn and wrong for your element: a
101-point sweep across a gigahertz is a 10 MHz grid, and a thin dipole's whole
VSWR $\le 2$ band can be 40 MHz. Four points across a resonance will not find
its minimum and cannot give you a crossing frequency worth quoting. Points
also set how finely you can place the marker, because the marker steps from
one measured frequency to the next and not between them. This is the one
setting where the default will quietly cost you the measurement, so change it
before you calibrate, not after.
:::
::::

::::{frame} Step 2 — Calibrate, Then Verify
:::{present}
4. **Calibrate…** → **1-port, port 1**. Reference plane: **the cable ends**.
5. Acknowledge, run it, put the cable back.
:::
:::{present}
:class: callout
Verify: terminate the cable in $50\ \Omega$ and press **Sweep**. Return loss
better than $30$ dB across the band. **Screenshot it.**
:::

A one-port calibration corrects reflection on that port alone, needs only that
one cable end on the module, and is the right choice for a single antenna. The
two-port option also corrects transmission, which is what Lesson 11 needs and
what today does not.

:::{depth}
The wizard asks which plane you calibrated because nothing in the data
afterwards can tell. Lesson 9 made that argument on paper; the dropdown is the
argument made unavoidable, and the answer is written into the record — and
into the header of every file you export — so that a measurement read weeks
later still says what it was referenced to. Pick the one-port option and the
checklist rewrites itself to match: one cable end to unmate, one port of the
module to mate, and nobody sent into the chamber to disconnect an antenna for
no reason.

The **cal** pill in the strip along the bottom is the other half: it reads
**cal**, **uncal**, or **cal?** when the instrument will not say. An
uncalibrated sweep is valid data and is never blocked, but it should not be
possible to take one without noticing.

Verifying against a load is the step that catches everything else — a cable
swapped after the calibration, a loose connector, a sweep changed without
meaning to. It works because the load is a standard the calibration did not
use to define itself, so a good answer is evidence rather than arithmetic.
:::
::::

::::{frame} Step 3 — Capture the Antenna
:::{present}
6. Connect it, set it on the foam, and take your hands off.
7. **Sweep** tab, **Capture: S11 only**.
8. Press **Sweep**. The tower does not move.
:::

One sweep per parameter, so asking for all four costs four times the wait and
measures three things that are not there — your antenna has one port. The
Smith chart and the magnitude plot fill in together as the trace arrives.

:::{depth}
A capture is not a scan and is not written to `runs/`. It lives in the browser
until you export it, which is deliberate: the service ships complex
S-parameters and nothing else, and every derived number you are about to read
— dB, impedance, VSWR, return loss — is computed from them on the page. The
payload stays a measurement rather than a measurement plus somebody's
arithmetic.

If you do ask for several parameters, **STOP** declines to start the next one
rather than interrupting the sweep in flight. A single sweep is one exchange
with the instrument and there is nowhere to interrupt it.
:::
::::

::::{frame} Step 4 — Four Names for One Number
:::{present}
The **Marker** picks a frequency. The readout gives it all at once:

- $Z = R + jX$, and $\vert \Gamma \vert$,
- VSWR, and return loss in dB.
:::
:::{present}
:class: callout
The Smith chart is not a fifth quantity — it is the **same number**, plotted.
:::

The magnitude plot is $\vert S_{11} \vert$ in dB against frequency; the Smith
chart is the locus of $\Gamma$; the marker sits at one frequency on both. Move
it and watch all four numbers change together, because they are four ways of
writing one measurement down.

:::{depth}
This is Lesson 9's "four names for one number" with the instrument doing the
conversion instead of you:

$$Z = Z_0\,\frac{1 + \Gamma}{1 - \Gamma}, \qquad
\text{VSWR} = \frac{1 + \vert \Gamma \vert}{1 - \vert \Gamma \vert}, \qquad
\text{RL} = -20 \log_{10} \vert \Gamma \vert$$

with $Z_0 = 50\ \Omega$, which on this instrument is a fact and not a setting.
Two readings are worth recognizing on sight. The readout says **open** where
$\Gamma$ reaches $+1$, because the impedance there is unbounded rather than
merely large. And it says **VSWR ∞** whenever
$\vert \Gamma \vert \ge 1$: a passive antenna cannot reflect more power than it
receives, so that is noise, or a calibration that no longer matches the sweep,
and quoting a number from it would dress the problem up as a measurement.

Read the resonance twice, once as the dip in dB and once as the reactance
passing through zero — the real-axis crossing on the chart. The two readings
disagree when something is wrong with the reference plane, and that
disagreement is the cheapest diagnostic you have.
:::
::::

::::{frame} Step 5 — Bandwidth off the Marker
:::{present}
9. Step the marker out either side of resonance to the two **VSWR $= 2$** frequencies.
10. Record both, and the fractional bandwidth between them.
:::

The bar is **VSWR $\le 2$**, the same bar Lesson 4 set and Lesson 9 quoted.
Quote the bandwidth in VSWR, never in decibels: Lesson 3's rule is that the
number means nothing without the bar attached to it.

:::{depth}
On the log-magnitude trace that bar sits at $-9.5$ dB, so the magnitude plot
finds the crossings quickly and the marker confirms them exactly. Interpolate
between the two bracketing points rather than quoting whichever one happens to
be closer; with 401 points across $\pm 30\%$ of a 900 MHz resonance the grid
is about 1.3 MHz, and a 44 MHz bandwidth quoted to the nearest grid point is
carrying 3% of avoidable error.
:::
::::

::::{frame} The File Is the Record
:::{present}
11. **Export** writes a Touchstone file: `.s1p` for one reflection parameter.
:::
:::{present}
The header carries what a plot cannot:

- hardware or **simulated**,
- which parameters were actually measured,
- the calibration, its ports, and its reference plane.
:::

Export every configuration before you change anything, and name what you keep.
A trace on a screen is a measurement that cannot say what it was taken under;
this file can, and that is the difference between data you can defend in three
weeks and a screenshot.

:::{depth}
Two details in that header are there because of how easily a file lies. A
capture of a single reflection parameter is written as `.s1p` rather than an
`.s2p` with the other three columns zeroed — a zero-filled `.s2p` claims a
through path of exactly zero and an infinitely reflective second port, and a
reader will plot those numbers quite happily. And if you do capture a partial
set, the header names what was *not* measured and written as zero. The
Touchstone column order for a two-port file is $S_{11}$, $S_{21}$, $S_{12}$,
$S_{22}$, which is not the order most people expect and is the usual source of
transposed data.
:::
::::

::::{frame} Step 6 — Compare Against Prediction
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

::::{frame} Step 7 — Perturb, One Variable at a Time
:::{present}
One capture and one exported file each, same sweep, same calibration:

- held clear, in free space,
- with a hand 2 to 3 cm from the element,
- lying flat on the bench.
:::

One variable at a time, and record all three fully — you are producing the
data for the table in your report, and a configuration you measured
incompletely is one you will have to set up again. Lesson 9 predicted the
direction of each shift; your job is the magnitude.

:::{depth}
Rename each file as you save it — `l10_freespace.s1p`, `l10_hand.s1p`,
`l10_bench.s1p`. The export stamps the clock into the filename, which keeps
three captures apart and tells you nothing about which is which a week later.
Three files with the sweep unchanged between them are directly comparable,
which is the whole reason for not touching the VNA panel once you have
calibrated.
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
3. A Smith chart with the resonance marked.
4. A paragraph on the perturbations.
:::

:::{depth}
In detail:

1. **An annotated $\vert S_{11}\vert$ plot.** Resonance marked, both
   VSWR $= 2$ crossings marked, axes labeled with units.
2. **A results table**: $f_0$, $Z$ at resonance, VSWR $\le 2$ bandwidth in MHz
   and in percent, for all three perturbation configurations.
3. **A Smith chart** with the marker on the resonance, and one sentence
   identifying that point as the real-axis crossing.
4. **A paragraph on the perturbation results.** What moved, in which
   direction, by how much, and why. Connect at least one observation to the
   near-field argument from Lesson 9.

Hand in the three exported files with it, and state the reference plane you
calibrated at. A plot with no markers and no units is a screenshot rather than
a measurement, and the paragraph carries the largest share of the grade.
:::
::::

::::{frame} The Bench Card
:class: read-only

| At the bench | What to do | What good looks like |
| :-- | :-- | :-- |
| Sweep | $\pm 30\%$ around resonance, $\ge 401$ points | settings written down |
| Calibrate | 1-port, port 1, at the cable ends | reference plane recorded |
| Verify | $50\ \Omega$ load, one capture | return loss $> 30$ dB, screenshotted |
| Capture | Sweep tab, $S_{11}$ only | Smith chart and magnitude together |
| Resonance | dip in dB *and* reactance through zero | the two agree |
| Bandwidth | marker to both VSWR $= 2$ points | 3 to 10% for a thin dipole |
| Export | one Touchstone file per configuration | header states the calibration |
| Perturb | free space, hand, bench | three complete captures |

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
dashboard, two ports instead of one, and a tower that moves. Further out the
skills compound: Module 3 builds arrays from these elements, and every element
in an array sees its neighbors as a mutual impedance — precisely the $S_{11}$
shift you produced with your hand today.

:::{depth}
The midterm project, due 2 Oct, asks you to build a dipole, tune it, measure
it, and defend the numbers you report about it. The antenna itself is not in
question — everyone builds the same one — so what you defend is the
measurement. Tuning *is* this lab: capture, read the sign of the reactance,
trim, capture again. Calibration and Smith-chart fluency are the
rate-limiting skills on that project, so practice both here, where the cost of
a mistake is an afternoon rather than a week.
:::
::::
