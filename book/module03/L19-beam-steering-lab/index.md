---
frame_view: true
---

# L19 - Beam Steering Lab

::::{frame}
:class: title-frame

<div class="course-mark">ECE 444 · Fall 2026</div>

<h1 class="frame-title">Beam Steering Lab</h1>

<div class="title-rule"></div>

Two runs put the PHASER's peak at $30^\circ$: move the source, or apply a steer angle.

Lesson 19 · Antennas, Phased Arrays, and Radar Systems · Dr. Neil Rogers
::::

::::{frame} Slides
:class: read-only

:::{admonition} Slides
:class: slides
<a href="../../slides/L19-beam-steering-lab.html" target="_blank" rel="noopener">html slides</a>
<a href="../../slides/L19-beam-steering-lab.html?print-pdf" target="_blank" rel="noopener">pdf slides</a>
<a href="../../slides/L19-beam-steering-lab.md" target="_blank" rel="noopener">raw markdown slides</a>
:::
::::

::::{frame} Learning Objectives

<ol class="lo-list" style="--module: '3'; counter-reset: lo 4">
  <li>I can implement beam steering on the ADALM-PHASER and verify the steered pattern against theory.</li>
</ol>
::::

::::{frame} From Prediction to Measurement
:::{present}
- Part 1, before today: the phase table, the beamwidths, and the error budget.
- Part 2, today: two runs put the peak at $0^\circ$, $30^\circ$, and $45^\circ$.
- Part 3, before Lesson 20: reconcile each measurement with its prediction.
:::

In Lesson 18 we derived the steering law and used it to fill in a table of
element phases for the PHASER's eight-element array. Lab 5's packet starts from
that table: Part 1, the pre-lab you completed before class, redoes it at your
HB100's frequency, predicts the beamwidths, and sizes the error budget. Today
your team places the source at measured angles on a protractor arc, and also
commands the peak to the same angles from the GUI, and records where the trace
peaks, how wide it is, and what the GUI writes into Phase Control. Part 3, on
your own before Lesson 20, reconciles those numbers with the predictions.
::::

::::{frame} Part 1: The Steering Prediction
:::{present}
$$\begin{aligned}
\Delta\phi &= kd\sin\theta_0 \\
&= 360^\circ\ \frac{d}{\lambda}\ \sin\theta_0 \\
&= 176.8^\circ \sin\theta_0
\end{aligned}$$

- $N = 8$, $d = 14\ \text{mm}$, and $d/\lambda = 0.491$ at $10.525\ \text{GHz}$.
:::
:::{present}
| $\theta_0$ | $\sin\theta_0$ | $\Delta\phi$ |
| :-- | :-- | :-- |
| $0^\circ$ | 0.000 | $0.0^\circ$ |
| $15^\circ$ | 0.259 | $45.8^\circ$ |
| $30^\circ$ | 0.500 | $88.4^\circ$ |
| $45^\circ$ | 0.707 | $125.0^\circ$ |
:::

The array is fixed: $N = 8$ elements, E1 to E8, on a $d = 14\ \text{mm}$ pitch.
The source is an HB100 Doppler module at a nominal $10.525\ \text{GHz}$, so
$\lambda = 28.5\ \text{mm}$ and $d/\lambda = 0.491$, with
$c = 3.00\times 10^8\ \text{m/s}$. Steering to
$\theta_0$ takes a **progressive phase** of

$$\Delta\phi = kd\sin\theta_0 = 360^\circ\ \frac{d}{\lambda}\ \sin\theta_0 = 176.8^\circ\sin\theta_0.$$

Lesson 18 worked the same table at the workshop's $10.3\ \text{GHz}$, where
$kd = 173.2^\circ$ and the $30^\circ$ step is $86.6^\circ$. At $10.525\ \text{GHz}$
the step is $88.4^\circ$, and Part 1 of the packet redoes the table at the
frequency your kit reported in Lesson 17, because every phase in the lab depends
on it.
::::

::::{frame} Wrapped Element Phases
:::{present}
| Element | E1 | E2 | E3 | E4 |
| :-- | :-- | :-- | :-- | :-- |
| Wrapped (°) | 0.0 | 88.4 | 176.8 | 265.2 |
| **Element** | **E5** | **E6** | **E7** | **E8** |
| Wrapped (°) | 353.6 | 82.0 | 170.5 | 258.9 |

- The $30^\circ$ ramp; E6 to E8 wrap: $442.0^\circ$ becomes $82.0^\circ$.
:::

The phase shifters produce a value between $0^\circ$ and $360^\circ$, so element
E$(n+1)$, which is element $n$ in Lesson 18's numbering, gets $n\Delta\phi$
**wrapped** modulo $360^\circ$. Wrapping changes nothing physically at one
frequency, because a phase shift of $360^\circ$ is no phase shift at all. For
$\theta_0 = 30^\circ$ the eight values are these, and E6 through E8 are the ones
that have wrapped:

| Element | E1 | E2 | E3 | E4 | E5 | E6 | E7 | E8 |
| :-- | :-- | :-- | :-- | :-- | :-- | :-- | :-- | :-- |
| Unwrapped ramp | $0.0^\circ$ | $88.4^\circ$ | $176.8^\circ$ | $265.2^\circ$ | $353.6^\circ$ | $442.0^\circ$ | $530.5^\circ$ | $618.9^\circ$ |
| Wrapped | $0.0^\circ$ | $88.4^\circ$ | $176.8^\circ$ | $265.2^\circ$ | $353.6^\circ$ | $82.0^\circ$ | $170.5^\circ$ | $258.9^\circ$ |

Each entry is a multiple of the unrounded step, $88.41^\circ$.
::::

::::{frame} The Beam-Sweep Trace
:::{present}
- The sweep steps the beam past a fixed source and plots power against steered angle.
- The array factor depends on $\sin\theta - \sin\theta_0$: the trace peaks at the source.
- It records the array factor, scaled by the element pattern at the source.
:::
:::{present}
<img src="../../viz/img/L19-two-ways.svg"
     alt="Two ways to measure a pattern. Left: the array turns past a fixed HB100, recording element pattern times array factor. Right: the array stays fixed and the beam is swept electronically past the source, recording the array factor at the source's element-pattern level."
     style="max-width: 560px; width: 100%; display: block; margin: 0 auto;">
:::

The x-axis of the PHASER's Rectangular plot is the angle the sweep steers to, not
a measured arrival angle. With Lab Preset 1 loaded, the instrument steps the
element-to-element phase one phase-shifter LSB, $2.8125^\circ$, at a time, and
plots each step at the angle that phase steers to; the steps past endfire collect
at $\pm 90^\circ$, which is why the edges of the trace look crowded.

The trace is a picture of the pattern because of Lesson 18's "The Steered
Pattern": the array factor depends only on $\sin\theta - \sin\theta_0$, and its
magnitude is even, so power received from a source at $\theta_{\text{src}}$ as
the beam steps across $\theta_0$ traces the same curve as the pattern of a beam
steered at the source. It peaks where the steered angle equals the source angle.

Rotating the array in front of a fixed source would record a different quantity.
Turning the array moves the source across the element pattern as well, so the
rotation records the element pattern times the array factor (Lesson 16). The
sweep holds the element pattern fixed at the source's direction, so it records the
array factor alone, scaled by the element pattern's value there. That scale factor
is what a peak-level comparison between two source positions measures. Every
point of the sweep also uses a different set of element phases, so the
beamformer's own errors, phase quantization and gain imbalance, shape the trace.
::::

::::{frame} Two Ways to Steer the Peak
:::{present}
- **Physical run:** Phase Control at zero; the source moves to $30^\circ$.
- **Commanded run:** the source stays at boresight; **Apply** $30$.
- Both peak near $30^\circ$, equally wide; only the physical run loses peak level.
:::
:::{present}
<img src="../../viz/img/L19-sweep-compare.svg"
     alt="Two beam-sweep traces: the boresight trace peaking at 0 degrees and 13.0 degrees wide, and the 30-degree trace peaking near 30 degrees, 15.1 degrees wide and 0.6 dB lower"
     style="max-width: 560px; width: 100%; display: block; margin: 0 auto;">
:::

The bench puts the peak at the same angles two ways. In the physical run, Phase
Control holds zero, the sweep's own ramp is the only steering, and the trace peaks
at the source's angle on the arc. In the commanded run, the source stays at
boresight and **Apply** in the Beam Steering section loads per-element offsets
that shift the trace: Apply $30$ puts a boresight source's peak at $+30^\circ$.

The two traces have the same width, because both shift the same function of
$\sin\theta - \sin\theta_0$ to the same place. Their peak levels differ. In the
physical run the source sits $30^\circ$ off each element's own boresight, and the
element pattern lowers the whole trace by its roll-off at $30^\circ$. In the
commanded run the source never leaves the elements' boresight, so the peak level
matches the $0^\circ$ trace. That difference is the measurement of scan loss
(Lesson 18, "Scan Loss").
::::

::::{frame} The Sign in Phase Control
:::{present}
| Element | E1 | E2 | E3 | E4 |
| :-- | :-- | :-- | :-- | :-- |
| Phase Control | 0 | −88 | −177 | −265 |
| **Element** | **E5** | **E6** | **E7** | **E8** |
| Phase Control | −354 | −442 | −531 | −619 |

- Apply $30$ writes $-n\Delta\phi$, whole degrees, unwrapped.
- The sweep adds $+n\Delta\phi_s$; the sum vanishes at $+30^\circ$.
:::
:::{present}
<img src="../../viz/img/L19-phase-ramp.svg"
     alt="The 30-degree ramp at 10.525 GHz: the unwrapped ramp rising to 618.9 degrees, the wrapped settings, and the falling whole-degree offsets Phase Control shows after Apply 30, from 0 to minus 619"
     style="max-width: 560px; width: 100%; display: block; margin: 0 auto;">
:::

When you type $30$ into **Steer Angle (deg)** and press **Apply**, the GUI
computes $\Delta\phi$ from the Signal Freq on screen and writes $-n\Delta\phi$ into
the Phase Control boxes, rounded to whole degrees and not wrapped. At
$10.525\ \text{GHz}$ the boxes read 0, −88, −177, −265, −354, −442, −531, and
−619. The sliders beside the boxes stop at $\pm 180^\circ$; read the boxes.

The minus sign is deliberate. During a sweep the backend adds its own ramp,
$+n\Delta\phi_s$, to whatever Phase Control holds, so element $n$ carries
$n(\Delta\phi_s - \Delta\phi_0)$. A boresight source needs no ramp at all, so the
array points at it where $\Delta\phi_s = \Delta\phi_0$, which is the plotted
angle $+30^\circ$. Apply is therefore the offset that makes a boresight source
look like a source at $+\theta_0$ on the sweep plot. On their own, with no sweep
ramp added, the offsets would point the beam to $-30^\circ$. To compare the
read-back with the wrapped ramp, reduce it modulo $360^\circ$: E6's
$-442^\circ$ is $278^\circ$, which is $360^\circ - 82.0^\circ$.

The GUI computes $\Delta\phi$ with $c = 299792458\ \text{m/s}$, not the
$3.00\times 10^8\ \text{m/s}$ of our prediction, so one element can differ by
$1^\circ$ after rounding: our $-n(88.41^\circ)$ gives $-530$ for E7, and the GUI's
$-n(88.47^\circ)$ gives $-531$.
::::

::::{frame} Predicted Sweep
:class: viz-frame

:::{depth}
The widget below is the prediction tool for today's lab. Set the frequency to
$10.525\ \text{GHz}$, or at the bench to the value **Find HB100** reports, and
the knob to the source's angle on the arc, which is where the trace should peak.
Then read $\Delta\phi$, the predicted half-power beamwidth, and the peak drop,
and two rows of phases: the beam ramp $+n\Delta\phi$ wrapped to $0^\circ$ to
$360^\circ$, and what Phase Control shows after Apply at the same angle, the
falling whole-degree offsets. Two things to notice before the bench: the dots
mark the angles the sweep samples, one $2.8125^\circ$ phase step apart, about
$1^\circ$ near broadside and wider toward endfire; and the beam widens as the
peak moves away from broadside while the sidelobe structure stretches with it.
:::

:::{present}
<iframe src="../../viz/steering-predictor.html"
        width="100%" height="538"
        style="border: 1px solid #cddce9; border-radius: 6px;"
        loading="lazy"
        title="Predicted beam-sweep trace and element phases for the PHASER array">
</iframe>
:::
::::

::::{frame} Part 2: Equipment and Setup
:::{present}
- The kit on its stand, cabled to your laptop as in Lesson 17.
- The HB100 on a tripod, $1\ \text{m}$ out, at patch-row height.
- A protractor arc centered on the array; $+\theta$ is toward E8.
:::
:::{present}
<img src="../../viz/img/L19-bench-setup.svg"
     alt="Bench geometry from above: the eight-element array, a 1 m protractor arc centered between E4 and E5, and the HB100 positions at 0, 30, and 45 degrees on the plus side, toward E8; confirm the plus side with Est. Angle"
     style="max-width: 560px; width: 100%; display: block; margin: 0 auto;">
:::

You need the ADALM-PHASER kit on its stand, connected to your laptop by the
Ethernet cable as in Lesson 17; the HB100 on a tripod about $1\ \text{m}$ from the
array face, at the height of the patch row; and a protractor arc of
$1\ \text{m}$ radius centered under the middle of the array, between E4 and E5.

One meter is Lesson 17's far-field distance for this array,
$2D^2/\lambda = 0.88\ \text{m}$ with $D = Nd = 112\ \text{mm}$. Center the arc on
the array, not on the board's edge: an arc centered $10\ \text{mm}$ off the middle
of the array shifts the reference angle by about $0.5^\circ$.

Lesson 18's sign convention puts $+\theta$ on the E8 end of the array, the end the
wave reaches first. Confirm it on your kit before you record anything: with the
source on the $+$ side, **Est. Angle** reads positive.
::::

::::{frame} Bring Up the Kit
:class: read-only

:::{present}
1. Browse to your kit's address from Lesson 17 (team 03: `http://192.168.7.13:8080`) and wait for the pill to read **Connected**.
2. Place the powered HB100 $1\ \text{m}$ out at $0^\circ$ on the arc, facing the array.
3. Press **Find HB100** and record the Signal Freq it reports in the packet.
4. Press **Calibrate** and wait for it to finish.
5. Press **1 Steering Angle** under **Lab Presets**.
6. Set **Rx Gain (dB)** to 10.
7. Turn on **Show Peak Angle Marker** under **Plot Options**.
8. Press **Start**, and check the **FFT** tab for one tone near $0\ \text{MHz}$, at least $20\ \text{dB}$ above the floor.
9. Open the **Rectangular** tab.
:::

This is Lesson 17's order, for the same reason: **Calibrate** reads the frequency
that **Find HB100** stores, and it needs the source at boresight while it runs,
or it bakes a steering ramp into the calibration offsets. The pill sits at the
bottom right and changes from **Checking...** to **Connected**; **Start** stays
grayed out until the backend is ready, and nothing plots until you press it.

The preset loads a uniform taper on E1 to E8, zeros Phase Control, sets 7 phase
bits with **Use Bits** on and **Signal BW** at $10\ \text{MHz}$, and opens the FFT
tab. It leaves **Signal Freq** at the value Find HB100 stored, and it does not set
**Rx Gain (dB)**; the Pi starts at 30 dB, where Lesson 17 measured the receiver
compressing, so step 6 sets the 10 dB reference.

On the FFT tab, one narrow tone stands well above the noise near $0\ \text{MHz}$,
within about $\pm 1\ \text{MHz}$. If it is buried, re-aim the HB100 or press
**Find HB100** again.
::::

::::{frame} Run 1: Move the Source
:class: read-only

:::{present}
10. Press **Reset** under **Phase Control**.
11. With the source at $0^\circ$, record **Est. Angle**, **Peak Array Gain**, and the half-power beamwidth in Table A.
12. Press **Freeze** to hold the boresight trace.
13. Move the HB100 along the arc to $+30^\circ$, still $1\ \text{m}$ out and facing the array.
14. Record the $30^\circ$ row of Table A.
15. Move the HB100 to $+45^\circ$ and record the last row.
:::

Read the half-power beamwidth as the distance between the two angles where the
trace falls $3\ \text{dB}$ below its own peak. The sweep runs continuously and
the button now reads **Stop**, so leave it running: the trace redraws on its own
after you move the source. If Est. Angle reads near $-30^\circ$, the source is on
the negative side of the arc; move it across.
::::

::::{frame} Run 2: Apply the Steer Angle
:class: read-only

:::{present}
16. Move the HB100 back to $0^\circ$ on the arc.
17. In **Beam Steering**, leave **Taper** on Uniform, enter 15 in **Steer Angle (deg)**, and press **Apply**.
18. Record **Est. Angle**, **Peak Array Gain**, and the beamwidth in Table B.
19. Repeat for 30, and copy the eight **Phase Control** boxes into Table B.
20. Repeat for 45.
21. Press **Reset** under **Phase Control** before you leave the station.
:::

Apply also rewrites **Element Gains** with the chosen taper, so leave it on
Uniform. The offsets stay loaded until you press Reset, and they add to every
sweep: with Apply $30$ still loaded and the source moved to $+30^\circ$, the trace
would peak at $90^\circ$. Step 21 leaves the station at zero for the next team.
::::

::::{frame} Expected Numbers
:::{present}
| Quantity | Calculated | Expect |
| :-- | :-- | :-- |
| HPBW at $0^\circ$, $30^\circ$, $45^\circ$ | $13.0^\circ$, $15.1^\circ$, $18.7^\circ$ | each $\pm 1^\circ$ |
| Peak drop, source at $30^\circ$ | $-0.6$ dB | $-0.6$ to $-1.5$ dB |
| Peak drop, Apply $30$ | 0 dB | 0 dB |
| First sidelobe | $-12.8$ dB | $-11$ to $-13$ dBc |
:::
:::{present}
<img src="../../viz/img/L19-expected-sweep.svg"
     alt="The expected Rectangular-tab traces for a source at 0 and at 30 degrees, sampled about 1 degree apart, with the 13.0 and 15.1 degree half-power spans, the 0.6 dB lower peak at 30 degrees, and the first sidelobes 12.8 dB down"
     style="max-width: 560px; width: 100%; display: block; margin: 0 auto;">
:::

The calculated column comes from the array factor for $N = 8$ at
$d/\lambda = 0.491$. The $1/\cos\theta_0$ broadening of Lesson 18 gives
$12.9^\circ/\cos 30^\circ = 14.9^\circ$ from the rule's broadside width, and the
exact array factor gives $13.0^\circ$, $15.1^\circ$, and $18.7^\circ$. A sweep
sampled about a degree apart reads each width to about a degree. dBc is dB
relative to the main-lobe peak; the sweep's floor sits about $23\ \text{dB}$ below
the peak, and the first sidelobes come up out of it at $-11$ to $-13$ dBc.

The peak drop is the element pattern's roll-off, the scan loss of Lesson 18. Its
ideal-element bound is

$$\Delta G = 10\log_{10}(\cos 30^\circ) = -0.6\ \text{dB},$$

and $-1.5\ \text{dB}$ at $45^\circ$. A patch element rolls off faster, closer to
$\cos^{1.3}\theta$ to $\cos^{1.5}\theta$ in power, so expect $-0.8$ to
$-0.9\ \text{dB}$ at $30^\circ$; Lesson 22 derives the element pattern. The
commanded run keeps the source on the elements' boresight, so its peak does not
drop. The peak-drop rows are hardware measurements: the simulator has no element
pattern and reads $0.0\ \text{dB}$ in both runs.
::::

::::{frame} No Hardware?
:class: read-only

:::{admonition} No hardware?
:class: tip
Open the hosted simulator at
[livethisdream.github.io/phaser](https://livethisdream.github.io/phaser/), the
same dashboard with nothing to install. At a station whose hardware has failed,
add `?sim=1` to the station's URL or turn on **Simulator Mode** under
**Configuration**; an orange **SIMULATION** pill marks simulated data. With a
checkout of the Phaser repository, `python phaser_headless.py --sim` serves the
same page at `http://localhost:8080`.

The simulated source is fixed at boresight, so Run 1's moves have no simulated
version. Run 2 works as written, and it is the rehearsal in Part 1 of the packet:
Apply $30$ gives the trace a source at $+30^\circ$ would, with **Est. Angle**
$29.6^\circ$ and a $15^\circ$ beamwidth, and Phase Control shows the same
offsets as the hardware. The simulator has no element pattern, so **Peak Array
Gain** does not drop; it does not model **Rx Gain (dB)**; its tone sits at
$-1\ \text{MHz}$; and **Find HB100** and **Calibrate** run scripted scans.
:::
::::

::::{frame} Part 3: The Peak-Angle Error Budget
:::{present}
- Sweep grid, half a step at $30^\circ$: $0.53^\circ$.
- Arc placement and aim: $1.5^\circ$.
- Room multipath: $1.0^\circ$.
- Root sum of squares $1.9^\circ$: a peak within $\pm 2^\circ$ passes.
:::
:::{present}
<img src="../../viz/img/L19-error-budget.svg"
     alt="Bar chart of the peak-angle error sources at 30 degrees in degrees: sweep grid 0.53, arc placement and aim 1.5, multipath 1.0, and their root sum of squares 1.9"
     style="max-width: 560px; width: 100%; display: block; margin: 0 auto;">
:::

The measured peak angle will not equal the arc angle exactly, and the
beamwidths will not equal $13.0^\circ$ and $15.1^\circ$ exactly. Three
independent effects account for the difference, and Part 1 of the packet sized
all three before the measurement.

**Sweep grid.** With Use Bits on, the sweep steps the element phase one
$2.8125^\circ$ LSB at a time. One step moves $\sin\theta$ by
$2.8125^\circ/176.8^\circ = 0.0159$, which is $0.91^\circ$ of angle at broadside
and $1.05^\circ$ at $30^\circ$, widening as $1/\cos\theta$. The trace holds no
information between samples, so a peak read off it can be wrong by half a step,
$0.53^\circ$ at $30^\circ$.

**Arc placement and aim.** At $1\ \text{m}$, one degree of arc is
$17.5\ \text{mm}$, so a tripod placed by eye to within $25\ \text{mm}$ gives a
$1.4^\circ$ error in the reference angle; centering the arc and pointing the
module bring the budget figure to $1.5^\circ$. This error is in the reference,
not in the array.

**Multipath.** The bench, the walls, and the people nearby return copies of the
tone. A reflection $20\ \text{dB}$ below the direct path has an amplitude ratio of
0.1, so, depending on its phase, it raises or lowers the level by

$$20\log_{10}(1 \pm 0.1) = +0.8\ \text{dB}\ \text{or}\ -0.9\ \text{dB},$$

a ripple on the main lobe that moves the apparent peak by up to about a degree.
Absorber behind the array and a clear arc both reduce it.

Because the three are independent, they combine as a root sum of squares:

$$\sqrt{0.53^2 + 1.5^2 + 1.0^2} = 1.9^\circ.$$

A peak within $\pm 2^\circ$ of the reference meets the standard, and agreement to
$0.1^\circ$ would point to a mistake in the comparison rather than an unusually
good measurement.

:::{depth}
**Why HB100 drift is not in the budget.** The GUI sets the receiver from Signal
Freq, and the SDR sees only a $3\ \text{MHz}$ window. A source that drifts far
enough to steer the beam measurably leaves the window and the tone disappears;
**Find HB100** finds it again. A drift that keeps the tone in view, under
$1.5\ \text{MHz}$, moves the beam by less than $0.01^\circ$. The arithmetic is
worth seeing once as a preview of Lesson 26's beam squint: phases set for
$10.525\ \text{GHz}$ and observed at $10.325\ \text{GHz}$ point a $30^\circ$ beam
$0.6^\circ$ farther out, and a $45^\circ$ beam $1.1^\circ$ farther.
:::
::::

::::{frame} Lab Packet
:class: read-only doc-links

The Lab 5 packet is the turn-in document for the whole lab, in three parts:

1. **Part 1, Pre-Lab** (individual, before the lab period): the prediction table at your kit's frequency, what Phase Control will show, the beamwidths and the error budget, and a rehearsal of Run 2 on the hosted simulator.
2. **Part 2, Bench** (team, in class): Tables A and B, from Run 1 and Run 2.
3. **Part 3, Writeup** (individual, before Lesson 20): reconcile the measurements with the predictions, and three analysis problems.

- <a class="doc-link" href="../../labs/ECE444_Lab_L19_Steering_blank.pdf" target="_blank" rel="noopener">Lab 5 packet (PDF)</a>
::::

::::{frame} Summary: The Steering Law
:class: read-only

| Symbol / idea | What it is | Number to remember |
| :-- | :-- | :-- |
| $\Delta\phi = kd\sin\theta_0$ | progressive element phase for a beam at $\theta_0$ | $176.8^\circ\sin\theta_0$ at $10.525\ \text{GHz}$ |
| Wrapped phase | $n\Delta\phi$ modulo $360^\circ$, what the shifter can produce | E8 at $30^\circ$: $258.9^\circ$ |
| Phase Control after Apply | $-n\Delta\phi$, whole degrees, unwrapped | E8 at $30^\circ$: $-619$ |
::::

::::{frame} Summary: The Trace
:class: read-only

| Symbol / idea | What it is | Number to remember |
| :-- | :-- | :-- |
| Beam-sweep trace | power against steered angle, source fixed | peaks at the source angle, or at the Apply angle for a boresight source |
| Sweep grid | one $2.8125^\circ$ phase LSB per step | $0.91^\circ$ at $0^\circ$, $1.05^\circ$ at $30^\circ$ |
| HPBW | half-power width, broadens off broadside | $13.0^\circ$ at $0^\circ$, $15.1^\circ$ at $30^\circ$ |
| Scan loss | element-pattern roll-off, physical run only | $-0.6\ \text{dB}$ bound at $30^\circ$ |
| Peak-angle budget | grid, aim, multipath, root sum of squares | $1.9^\circ$; pass within $\pm 2^\circ$ |
::::

::::{frame} Looking Ahead
:::{present}
- Lesson 20 derives the trace's features: nulls, the $-12.8$ dB sidelobe, and the beamwidth.
- Bring today's Tables A and B; the derivation starts from them.
:::

Today we compared measured beamwidths and sidelobes with values from Lesson 16's
closed form and Lesson 18's broadening rule. Lesson 20 takes the closed form

$$AF_N(\psi) = \frac{\sin(N\psi/2)}{N\sin(\psi/2)}$$

and extracts every feature of the trace you just recorded from it: where the
nulls fall, why the first sidelobe sits $12.8\ \text{dB}$ down, how the beamwidth
follows

$$\theta_{\text{HP}} \approx \frac{0.886\ \lambda}{Nd\cos\theta_0},$$

and what changes when elements are switched off. Bring today's traces to that
lesson; the derivation is easier to trust with the measurement in front of you.
::::
