---
frame_view: true
---

# L21 - Array Factor Lab

::::{frame}
:class: title-frame

<div class="course-mark">ECE 444 · Fall 2026</div>

<h1 class="frame-title">Array Factor Lab</h1>

<div class="title-rule"></div>

Today that table goes to the bench.

The work of this lab is the third step: reconciling what the plot shows with what the array factor says, and naming the reason for every difference.

Lesson 21 · Antennas, Phased Arrays, and Radar Systems · Dr. Neil Rogers
::::

::::{frame}
:::{admonition} Slides
:class: slides
<a href="../../slides/L21-array-factor-lab.html" target="_blank" rel="noopener">html slides</a>
<a href="../../slides/L21-array-factor-lab.html?print-pdf" target="_blank" rel="noopener">pdf slides</a>
<a href="../../slides/L21-array-factor-lab.md" target="_blank" rel="noopener">raw markdown slides</a>
:::
::::

::::{frame} Learning Objectives

<ol class="lo-list lo-sublist" style="--module: '3'; --lo: '2'; counter-reset: lo 9">
  <li>I can measure half-power beamwidth, first-null beamwidth, and first sidelobe level from a beam-sweep trace.</li>
  <li>I can compare measured beamwidths at eight, four, and two active elements against calculation.</li>
  <li>I can explain why a measured sweep departs from the ideal array factor near its nulls and floor.</li>
  <li>I can reduce an array's active aperture and predict the resulting pattern before measuring it.</li>
</ol>

:::{depth}
Lesson 20 ended with a table of predictions: what the PHASER's beam should
look like at eight, four, and two active elements. Today that table goes to
the bench. You will sweep the array three times, shrinking the active
aperture by half between sweeps, and read the half-power beamwidth, the
first-null beamwidth, and the first sidelobe level off each trace. The
predictions are already written down, so the work of this lab is the third
step: reconciling what the plot shows with what the array factor says, and
naming the reason for every difference.
:::
::::

::::{frame} Part 1: What the array factor predicts

The PHASER is an 8-element linear array with element spacing $d = 14\ \text{mm}$.
At the workshop frequency of $10.3\ \text{GHz}$ the wavelength is
$\lambda = 29.1\ \text{mm}$, so $d/\lambda = 0.481$ and the full aperture is
$Nd = 112\ \text{mm}$, just under four wavelengths. Two results from Lesson 20
set every number you are about to measure:

$$\theta_{\text{HP}} \approx \frac{0.886\ \lambda}{Nd}, \qquad
\text{FNBW} = 2\arcsin\!\left(\frac{\lambda}{Nd}\right)$$

Both depend on the array only through $Nd$, the **active aperture**. Turning
off elements at the ends of the row shortens $Nd$ without changing $d$, and
that is the whole experiment: halve the aperture, watch the beam double.
::::

::::{frame} The prediction table

The expectation table below is Lesson 20's, restated as the prediction column
you will fill in against. Note that the sidelobe entries are not all the same
number. The familiar $-13\ \text{dB}$ figure is the large-$N$ limit of the
uniform array factor. An 8-element array lands at $-12.8\ \text{dB}$, close
enough to call $-13\ \text{dB}$, but a 4-element array reaches only
$-11.3\ \text{dB}$, and a 2-element array has no sidelobe at all.

| Active elements | $Nd$ | HPBW (calc) | FNBW (calc) | First SLL (calc) |
| :-- | :-- | :-- | :-- | :-- |
| 8 (Rx1-Rx8) | $112\ \text{mm}$ | $13^\circ$ | $30^\circ$ | $-12.8$ dB |
| 4 (Rx3-Rx6) | $56\ \text{mm}$ | $27^\circ$ | $62^\circ$ | $-11.3$ dB |
| 2 (Rx4, Rx5) | $28\ \text{mm}$ | $62^\circ$ | $180^\circ$ | none |
::::

::::{frame} Two entries that need care

Two entries in that table need a word of explanation before you go to the
bench. The $62^\circ$ at $N = 2$ does not come from the $0.886\ \lambda/(Nd)$
rule, which returns $53^\circ$ there. That rule carries a small-angle step
inside it, and a beam this wide violates it. For two elements the array factor
is just $\cos(\psi/2)$ with $\psi = kd\sin\theta$, so the half-power point
solves $\cos(\psi/2) = 1/\sqrt{2}$ directly:

$$\psi = \frac{\pi}{2} \quad\Longrightarrow\quad \sin\theta = \frac{\lambda}{4d} = 0.520
\quad\Longrightarrow\quad \theta = 31.3^\circ$$

which doubles to $62.6^\circ$.
::::

::::{frame} Falls outside visible space

The $180^\circ$ in the FNBW column is a convention rather than a
measurement. The first null of $\cos(\psi/2)$ needs
$\sin\theta = \lambda/2d = 1.04$, and no real angle satisfies that. The null
exists in the mathematics but falls outside visible space, so the pattern has
no null anywhere you can steer, and the beamwidth between first nulls is
quoted as the full $180^\circ$ of the scan range.
::::

::::{frame} Key point
:::{callout}
Beamwidth is set by the active aperture $Nd$, not by the element count on its
own. Halving the number of active elements halves $Nd$ and doubles both
beamwidths. The sidelobe level is set by the shape of the amplitude
distribution, which stays uniform throughout this lab, so the sidelobe moves
only through the small-$N$ correction.
:::
::::

::::{frame} Reading a sweep for what it is

The Rectangular tab does not plot the array factor. It plots received
power against **commanded steer angle**: the software steps the beam past a
stationary source and records the power at each step. By reciprocity that
traces the array pattern, but three properties of the measurement are baked
into every trace you will read.
::::

::::{frame} The sweep is sampled, not continuous

The sweep is sampled, not continuous. The default step is $2.8125^\circ$, the
ADAR1000 phase LSB expressed as a steering resolution, so the trace is 65
points across $\pm 90^\circ$ and a feature narrower than one step can fall
between samples entirely. The trace has a floor. Receiver noise sits about
$23\ \text{dB}$ below the peak of the uniform 8-element beam, which is the
usable dynamic range of the whole measurement. Anything the array factor puts
below that line reads as noise instead. And the nulls are the first casualties
of both effects together: a true null is infinitely deep and infinitely narrow,
so the sampling grid rarely lands on it and the floor fills in whatever the
grid does reach.
::::

::::{frame} Ideal versus measured, on a toggle
:class: viz-frame

The widget below draws the array factor for each of the three apertures, then
adds those three measurement effects on a toggle. Set the aperture, read HPBW,
FNBW, and first sidelobe level off the ideal curve, then switch measurement
effects on and read the same three numbers again from the sampled trace. Watch
the FNBW pill in particular: at eight elements it moves from $30.1^\circ$ to
$28.1^\circ$ the moment the grid appears, and at two elements it reports a dash
because there is no null to find.

<iframe src="../../viz/af-measurement-compare.html"
        width="100%" height="593"
        style="border: 1px solid #cddce9; border-radius: 6px;"
        loading="lazy"
        title="Ideal array factor and measured sweep at 8, 4, and 2 active elements">
</iframe>
::::

::::{frame} Part 2: Equipment and setup

You need the ADALM-PHASER kit on its tripod or stand, its 5 V supply and
network connection, and an HB100 Doppler module with a battery pack as the
signal source. Place the HB100 at boresight, about $1\ \text{m}$ from the face
of the array, at the same height as the patch row and with its face square to
the array. Boresight placement matters more than distance here: every
prediction in Part 1 is a broadside number, and a source offset by a few
degrees shifts the whole trace along the angle axis.
::::

::::{frame} Run Calibrate once

Bring up the GUI at `http://phaser.local:8080` and confirm the Configuration
section reads a Signal Freq near $10.5\ \text{GHz}$. Run **Calibrate** once so
the per-element gains and phases start from a matched state. An uncalibrated
array has amplitude and phase errors spread across the row, which fills the
nulls and raises the sidelobes on its own, and you would then be measuring the
calibration rather than the array factor.
::::

::::{frame} Load Lab preset 2 (Array Factor)

Load **Lab preset 2 (Array Factor)** from the Lab Presets section. The preset
sets a uniform taper across all eight elements, zero steering phase, and the
default $2.8125^\circ$ steer resolution, and it opens the **Rectangular** tab
in the beam-sweep plot. From here the procedure names only the controls you
change.
::::

::::{frame} The HB100 drifts during the lab
```{note}
The HB100 is a free-running DRO and drifts across $10.1$ to $10.7\ \text{GHz}$
with temperature. The GUI hunts for the tone, so a drift of tens of megahertz
between sweeps does not affect this lab. Moving the source does, because all
three traces are compared against each other at the end.
```
::::

::::{frame} Part 3: Procedure

Each step names the control you touch and the observation you should get. Fill
the measurement table in Part 5 as you go, and predict before you measure at
every aperture change.
::::

::::{frame} Step 1 - Sweep the full array

With all eight Element Gains at 100, press **Start**. The sweep runs across
$\pm 90^\circ$ and settles into a trace with a single main lobe at $0^\circ$
and three or four sidelobe pairs on each side. Press **Freeze** to hold it as
a reference trace. Read the Peak Array Gain readout and record it. Hover
along the trace to read the angles where it falls $3\ \text{dB}$ below the
peak, and record the difference as the measured HPBW. Expect about $13^\circ$.
Then find the two minima that bracket the main lobe and record the difference
as FNBW; expect $28$ to $30^\circ$. Finally read the height of the tallest
sidelobe relative to the peak, near $\pm 22^\circ$, and record it as the first
SLL. Expect $-11$ to $-13\ \text{dBc}$.
::::

::::{frame} Step 2 - Halve the aperture

In **Element Gains**, set Rx1, Rx2, Rx7, and Rx8 to 0, leaving Rx3 through Rx6
at 100. Before pressing anything, write down your prediction: four active
elements over $56\ \text{mm}$ of aperture give $27^\circ$ HPBW and $62^\circ$
FNBW, and the peak should sit about $6\ \text{dB}$ below the eight-element
peak. Press **Start**, then **Freeze**. Read the same four numbers. The main
lobe is now roughly twice as wide and the sidelobe structure has thinned out
to one pair near $\pm 50^\circ$.
::::

::::{frame} Step 3 - Halve it again

Set every element to 0 except Rx4 and Rx5. Predict first: two elements over
$28\ \text{mm}$ give a $62^\circ$ beam, no visible null, and a peak about
$12\ \text{dB}$ below the eight-element peak. Press **Start**, then
**Freeze**. The trace is now a single broad hump with no sidelobes and no
null anywhere in the scan. It flattens into the noise well before $\pm
90^\circ$: the two-element pattern falls only about $24\ \text{dB}$ from its
own peak at endfire, but the floor sits just $11\ \text{dB}$ below that peak,
so the outer half of the roll-off is buried.
::::

::::{frame} Step 4 - Compare the three frozen traces

All three are on the plot together now. Two trends should be visible without
measuring anything. The beamwidth doubles at each halving, because $Nd$ halves
and both beamwidth formulas scale as $1/Nd$. The peak steps down by about
$6\ \text{dB}$ at each halving, because the elements add in voltage at
boresight: eight equal signals in phase give eight times the voltage of one,
four give four times, and

$$20\log_{10}\!\left(\frac{N_{\text{active}}}{8}\right)
= -6.0\ \text{dB at } N = 4, \qquad -12.0\ \text{dB at } N = 2$$
::::

::::{frame} The missing half decibel

The plot will show the first step at very close to $6.0\ \text{dB}$ and the
second at more like $5.5\ \text{dB}$. The shortfall is the noise
floor. By the time only two elements are on, the peak sits about $11\
\text{dB}$ above the floor, and the power the receiver reports at the peak is
the sum of signal power and noise power. Adding a floor that is $11\
\text{dB}$ down lifts the reading by roughly $0.3\ \text{dB}$, which is most
of the missing half decibel.
::::

::::{frame} Step 5 - Restore the array

Set all eight Element Gains back to 100 before you leave the bench or hand the
kit to the next section. The next lab starts from a full uniform aperture.
::::

::::{frame} Worked example — predicting a six-element aperture
:::{admonition} Worked example — predicting a six-element aperture
:class: tip
Suppose you turn off only Rx1 and Rx8, leaving six elements over
$Nd = 6 \times 14 = 84\ \text{mm}$. The beamwidth scales as $1/Nd$, so from the
eight-element measurement,

$$\theta_{\text{HP}} \approx 13.2^\circ \times \frac{112}{84} = 17.6^\circ$$

and the first-null beamwidth is
$2\arcsin(29.1/84) = 2 \times 20.3^\circ = 40.6^\circ$. The peak falls by
$20\log_{10}(6/8) = -2.5\ \text{dB}$. The predicted HPBW is about six sweep
steps wide, so the measurement has enough resolution to confirm it, and you
should expect a reading within a degree or two of $17.6^\circ$.
:::
::::

::::{frame} No hardware?
```{note}
Run `python phaser_headless.py --sim` and open the same URL. Simulation mode
reproduces this lab step for step, because the simulated source already sits
at boresight and nothing in the procedure requires moving it. The sim's sweep
reads $13.1^\circ$, $29.1^\circ$, and $65.4^\circ$ for the three apertures,
and the peak steps are the same. Record those as your measured column and
reconcile them against the calculated column exactly as you would on the
bench.
```
::::

::::{frame} Part 4: Where the sweep leaves the array factor

Three differences between your trace and the array factor are expected, and
each one has a number attached to it.
::::

::::{frame} The floor sits at about -23 dBc

Receiver and quantization noise put a hard limit on how far down the plot can
see. Every feature of the array factor below that line — the deep parts of
the nulls, and every sidelobe of a tapered array — reads as noise instead of
as pattern. This is the usable dynamic range of the measurement, and it is
why the lab asks for the first sidelobe rather than the second or third.
::::

::::{frame} Nulls read about -19 dBc instead of -infinity

Two effects fill them, and it is worth keeping them separate. Grid straddle
comes first: the 8-element null falls at $15.1^\circ$, but the sweep samples
at multiples of $2.8125^\circ$, so the nearest sample is at $14.06^\circ$,
where the array factor is already back up to $-23\ \text{dB}$. The floor then
adds its own power on top. The measured FNBW comes out as $2 \times 14.06 =
28.1^\circ$ rather than $30.1^\circ$, and the entire $2^\circ$ discrepancy is
the sampling grid, not the array.
::::

::::{frame} The first sidelobe reads -11 to -13 dBc

The array factor puts it at $-12.8\ \text{dB}$ and $21.9^\circ$. The nearest
sample at $22.5^\circ$ catches it within a tenth of a decibel, so grid
straddle costs little here, but the floor adds power to a sidelobe that is
only $10\ \text{dB}$ above it and noise moves the reading a few tenths either
way from sweep to sweep. A single number is not meaningful at this dynamic
range; a range is.
::::

::::{frame} The errors grow as the aperture shrinks

Notice how these three effects grow as the aperture shrinks. At eight elements
the measured HPBW lands within a tenth of a degree of theory. At four elements
the peak is $6\ \text{dB}$ closer to the floor and the reading is off by about
$2^\circ$. At two elements the peak is $12\ \text{dB}$ closer and the reading
is off by more than $3^\circ$. Every one of those errors is a consequence of
the shrinking gap between the trace and the noise floor.
::::

::::{frame} Part 5: Deliverables

Submit the completed measurement table and two short written answers.
::::

::::{frame} Measurement table

One row per aperture, with the calculated columns filled in from Part 1
before you measured and the measured columns filled in at the bench.

| Active elements | Peak (dBFS) | HPBW meas | HPBW calc | FNBW meas | FNBW calc | First SLL |
| :-- | :-- | :-- | :-- | :-- | :-- | :-- |
| 8 (Rx1-Rx8) | | | $13^\circ$ | | $30^\circ$ | |
| 4 (Rx3-Rx6) | | | $27^\circ$ | | $62^\circ$ | |
| 2 (Rx4, Rx5) | | | $62^\circ$ | | $180^\circ$ | |
::::

::::{frame} Written answer 1

Explain why the first-null beamwidth of the two-element array is quoted as
$180^\circ$ rather than measured. Your answer should name the condition on
$\lambda/2d$ that decides whether a null exists in visible space, and evaluate
it for $d = 14\ \text{mm}$ at $10.3\ \text{GHz}$.
::::

::::{frame} Written answer 2

The gain of each individual patch element is the same whether the other seven
elements are on or off, and the amplifier behind each element is unchanged.
Explain why the peak of the sweep nonetheless drops by about $6\ \text{dB}$
every time you halve the number of active elements.
::::

::::{frame} Lab sheet

The lab sheet is the turn-in document for all of it: <a href="../../labs/ECE444_Lab_L21_ArrayFactor_blank.pdf" target="_blank" rel="noopener">Lab sheet (PDF)</a>.
::::

::::{frame} Summary — beamwidth

| Symbol / idea | What it is | Number to remember |
| :-- | :-- | :-- |
| $Nd$ | active aperture; sets both beamwidths | $112\ \text{mm}$ at $N = 8$, $d = 14\ \text{mm}$ |
| $\theta_{\text{HP}} \approx 0.886\ \lambda/Nd$ | half-power beamwidth, broadside | $13^\circ$, $27^\circ$, $62^\circ$ for $N = 8, 4, 2$ |
| $\text{FNBW} = 2\arcsin(\lambda/Nd)$ | first-null beamwidth | $30^\circ$ at $N = 8$; no null when $\lambda/2d > 1$ |
::::

::::{frame} Summary — sidelobe and peak drop

| Symbol / idea | What it is | Number to remember |
| :-- | :-- | :-- |
| First SLL, uniform | set by distribution shape, not size | $-12.8$ dB at $N = 8$; $-11.3$ dB at $N = 4$ |
| $20\log_{10}(N_{\text{active}}/8)$ | peak drop from coherent voltage sum | $-6$ dB per halving of the aperture |
::::

::::{frame} Summary — the sweep and noise floor

| Symbol / idea | What it is | Number to remember |
| :-- | :-- | :-- |
| Sweep grid | steer step = ADAR1000 phase LSB | $2.8125^\circ$, 65 points across $\pm 90^\circ$ |
| Dynamic range | peak of uniform beam above noise | $\approx 23$ dB; nulls read $\approx -19$ dBc |
::::

::::{frame} Practice

- <a href="../../practice/ECE444_L21_Practice_blank.pdf" target="_blank" rel="noopener">Problem set (PDF)</a>
- <a href="../../practice/ECE444_L21_Practice_SOLUTIONS.pdf" target="_blank" rel="noopener">Solutions (PDF)</a>
::::

::::{frame} Where this is going

Every prediction in this lab came from the array factor alone, and the array
factor treats each element as an isotropic point radiating equally in all
directions. That assumption is good near boresight, which is where all three of
today's beams pointed, so the numbers reconciled to within the measurement's
own resolution. Push the beam out toward the edge of the scan and it fails. The
array factor says a steered beam keeps its peak height at every scan angle,
which is not what the hardware does.
::::

::::{frame} Where this is going, continued

Lesson 22 supplies the missing factor. A patch element has a pattern of its own
— broad, but falling off steadily away from boresight — and the full array
pattern is the product of that element factor with the array factor. That
product accounts for the part of the measurement the array factor cannot: why
the peak of a steered beam drops as it scans, and why the far-out sidelobes on
a real trace do not match a pure array-factor calculation. Before the next
lesson, review pattern multiplication from Lesson 16 and keep your three frozen
traces, since Lesson 23 measures the element pattern against them.
::::
