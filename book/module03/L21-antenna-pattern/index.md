---
frame_view: true
---

# L21 - Antenna Pattern

::::{frame}
:class: title-frame

<div class="course-mark">ECE 444 · Fall 2026</div>

<h1 class="frame-title">Antenna Pattern</h1>

<div class="title-rule"></div>

The kit builds its pattern plot from many beams. Today we measure one beam directly and compare the two.

Lesson 21 · Antennas, Phased Arrays, and Radar Systems · Dr. Neil Rogers
::::

::::{frame} Printing
:class: read-only

To print the slides, switch to present mode and print: one slide a sheet,
with room for notes. Print from read mode for the whole lesson.
::::

::::{frame} Learning Objectives

<ol class="lo-list" style="--module: '3'; counter-reset: lo 5">
  <li>I can distinguish between array factor and true antenna pattern and account for element pattern effects.</li>
</ol>

:::{depth}
Every pattern you have read since the L18 Lab came from the PHASER's
Rectangular plot, the **beam sweep**: the kit holds the HB100 still, steps the
beam past it, and plots the level it receives at each commanded angle, so each
point comes from a different beam. An antenna range measures a pattern the
other way. It holds one beam still and moves the source around it in azimuth.
Today we take that **azimuth sweep** with the kit's Signal vs Time mode and
compare it with the beam sweep. The two agree on the main lobe and the first
sidelobes, and they part farther out, where each patch's own pattern, the
noise floor, and the room decide the level.
:::
::::

::::{frame} The Rectangular Plot
:::{present}
- The HB100 stays put while the kit steps the element-to-element phase, $2.8125^\circ$ at a time.
- Each step makes a different beam; the plot puts the level received through it at that beam's commanded angle.
- One trace is 162 steps.
:::

You built this trace step by step in the L18 Lab
(<a href="../L18-lab-beam-steering/index.html#frame-the-beam-sweep-trace">"The Beam-Sweep Trace"</a>).
With Use Bits on, as in every lab preset, the kit adds one phase-shifter LSB,
$2.8125^\circ$, to the element-to-element phase, writes that ramp to the eight
channels, reads the peak of the FFT, and plots the reading at the angle the
ramp steers to. At $10.3\ \text{GHz}$ one step moves $\sin\theta_0$ by
$2.8125^\circ/173.2^\circ = 0.0162$, which is $0.93^\circ$ of angle near
broadside and $1.07^\circ$ at $30^\circ$. Of the 162 steps, 123 fall inside
$\pm 82^\circ$; the rest ask for more phase than any real angle needs and
plot at $\pm 90^\circ$. The L20 Lab showed what that grid and the noise floor
do to the readings
(<a href="../L20-lab-array-factor/index.html#frame-reading-a-sweep-for-what-it-is">"Reading a Sweep for What It Is"</a>).
::::

::::{frame} Beam Sweep, Step by Step
:class: viz-frame

:::{depth}
This is the beam sweep the kit runs, slowed down. Press **step** to add one
phase LSB at a time and watch the left panel: the beam swings past the HB100,
and the inset adds the eight element signals tip to tail. Away from the
source the element signals arrive out of phase and their sum is small, so the
point lands in a sidelobe or near the noise floor; as the beam reaches the
source the signals line up and the trace rises to its peak. Each point on the
right panel comes from the beam on the left at that moment, never from one
beam held still.
:::

:::{present}
<iframe src="../../viz/sweep-trace.html"
        width="100%" height="441"
        style="border: 1px solid #cddce9; border-radius: 6px;"
        loading="lazy"
        title="The beam-sweep trace built one phase step at a time: the beam swinging past the HB100, the eight element signals summed, and each step's power plotted at the angle it steers to">
</iframe>
:::
::::

::::{frame} Why the Beam Sweep Traces a Pattern
:::{present}
$$
\psi = kd\left(\sin\theta_\text{src} - \sin\theta_0\right)
$$

- $\vert AF\vert$ depends only on $\psi$, and it is even in $\psi$.
- Stepping $\theta_0$ or moving $\theta_\text{src}$ visits the same curve.
:::
:::{present}
<img src="../../viz/img/L21-psi-two-ways.svg"
     alt="The array factor in decibels against psi from minus 180 to 180 degrees. Open orange circles, the beam sweep stepping theta zero with the source fixed, and small navy dots, the azimuth sweep moving the source with the beam fixed, both fall on the same curve."
     style="max-width: 560px; width: 100%; display: block; margin: 0 auto;">
:::

Lesson 18 ("The Steered Pattern") showed that steering replaces the
array-factor argument with

$$
\psi = kd\left(\sin\theta_\text{src} - \sin\theta_0\right),
$$

where $\theta_\text{src}$ is the direction the signal arrives from and
$\theta_0$ is the angle the phase ramp steers to. The beam sweep holds
$\theta_\text{src}$ and steps $\theta_0$; the azimuth sweep holds $\theta_0$
and moves $\theta_\text{src}$. Both run $\psi$ through the same values, and
$\vert AF\vert$ is the same for $\psi$ and $-\psi$, so both trace the same
curve. That is why a trace built from 162 different beams looks like the
pattern of one beam.

The two differ only in what the array factor leaves out. The azimuth sweep
carries the source across each patch's own pattern, so it records the
product of the element pattern and the array factor that Lesson 16 derived
(<a href="../L16-array-factor/index.html#frame-from-two-patterns-to-one">"From Two Patterns to One"</a>).
The beam sweep keeps the source in one direction, so each patch receives the
same level at every step and the element pattern is a single constant.
::::

::::{frame} The Antenna-Range Method
:::{present}
- An antenna range holds the beam still and moves the source, or turns the antenna.
- Every point comes from the same beam.
- The x-axis is the source's physical angle.
:::
:::{present}
<img src="../../viz/img/L21-two-methods.svg"
     alt="Left: the kit steps the beam electronically past a stationary HB100. Right: the kit holds the beam fixed while you carry the HB100 around the array on a 1.2 m arc."
     style="max-width: 560px; width: 100%; display: block; margin: 0 auto;">
:::

Lesson 9 described how an antenna range measures a pattern
(<a href="../../module02/L09-pattern-measurement-theory/index.html#frame-two-measurements-one-question">"Two Measurements, One Question"</a>).
The antenna under test sits on a turntable with its beam fixed, a source
stands at a fixed distance, and the turntable records the received level
against the angle between the two. Every reading comes from the same beam,
and each one carries a physical angle. The L21 Lab takes this azimuth sweep
twice: once with you carrying the HB100 around the kit on a taped arc, and
once with the kit turning on its stand in front of the HB100.
::::

::::{frame} Signal vs Time Mode
:::{present}
- The kit holds the beam at the Steer Angle and plots the peak level against time.
- You carry the HB100 from $-90^\circ$ to $+90^\circ$ on a $1.2\ \text{m}$ arc.
- The trace is one beam's pattern across azimuth.
:::

Lab Preset 7, **Antenna Pattern**, sets **Mode** to **Signal vs Time**. In
that mode the kit stops stepping the beam: it holds every element at the
phase for the **Steer Angle** you set, and the Tracking tab plots the FFT
peak against elapsed time. As you carry the HB100 around the arc, the level
at each instant is the held beam's response in the direction of the HB100 at
that instant. This is the measurement in ADI's PHASER workshop, "Measuring
the Actual Antenna Pattern."
::::

::::{frame} Azimuth Sweep Simulator
:class: viz-frame

:::{depth}
The widget runs the azimuth sweep in simulation. Choose a steer angle and a
speed profile, then watch the trace paint as the source moves around the arc.
Run it once with the uniform profile and once with the hand-like profile, and
compare the readouts: the lobe spacing changes and the lobe levels do not.
The simulation holds the radius fixed; a hand-carried source drifts by a few
centimeters, which moves the level (next frame).
:::

:::{present}
<iframe src="../../viz/pattern-measurement-sim.html"
        width="100%" height="461"
        style="border: 1px solid #cddce9; border-radius: 6px;"
        loading="lazy"
        title="Simulated azimuth sweep: a source moves around an arc in front of a fixed beam while the level-versus-time trace paints below">
</iframe>
:::
::::

::::{frame} The Time Axis
:::{present}
- At a steady pace, time on the plot maps directly to azimuth.
- An uneven pace stretches or squeezes a lobe in time; its level stays the same if the lobe gets several updates.
:::
:::{present}
<img src="../../viz/img/L21-time-vs-angle.svg"
     alt="The same azimuth sweep plotted twice: against elapsed time, where an uneven pace spaces the lobes unevenly, and against source angle, where they are symmetric. The lobe levels are identical on both."
     style="max-width: 560px; width: 100%; display: block; margin: 0 auto;">
:::

The Signal vs Time plot puts time on its x-axis, and at a steady pace time
and azimuth are the same axis with a scale factor: a $180^\circ$ arc in
$25\ \text{s}$ is $7.2^\circ$ per second. A hand is not perfectly steady.
Moving slowly through a lobe draws it wider on the plot and hurrying draws it
narrower, but the level at each instant is still the pattern in the source's
direction, so the lobe levels come through. The one limit is the update
rate, which the plot's title shows: a lobe crossed in a fraction of a second
gets only a few readings, and its peak can fall between them. For angles
read to a degree or two, the L21 Lab turns the kit on its stand and reads
the stand's scale.

A drift in the arc's radius changes the level. Received power falls as
$1/r^2$, so drifting $10\ \text{cm}$ in or out at $1.2\ \text{m}$ changes a
reading by

$$
\begin{aligned}
20\log_{10}\frac{1.3\ \text{m}}{1.2\ \text{m}} &= 0.7\ \text{dB} \\
20\log_{10}\frac{1.2\ \text{m}}{1.1\ \text{m}} &= 0.8\ \text{dB} .
\end{aligned}
$$

Turning the kit on its stand holds the distance fixed, which is why the L21
Lab does both.
::::

::::{frame} Levels in dBc
:::{present}
$$
L_\text{dBc} = L_\text{dBFS} - L_\text{dBFS,\ peak}
$$

- dBFS: level relative to the receiver's full scale, which the kit plots.
- dBc: level relative to the trace's own main-lobe peak.
- The subtraction removes Rx Gain, distance, and source power.
:::

The kit reports every level in **dBFS**, decibels relative to the full scale
of the receiver's analog-to-digital converter. A dBFS reading depends on
everything between the HB100 and the converter: the Rx Gain setting, the
distance, the HB100's battery, and the direction of the source. Two traces
taken at different gains or distances therefore sit at different dBFS
levels even when the patterns are identical.

**dBc** removes that. Subtract the main-lobe peak of the same trace from
every reading, and each level becomes a ratio to the peak: a first sidelobe
at $-31.2$ dBFS under a main lobe at $-18.4$ dBFS reads
$-31.2 - (-18.4) = -12.8$ dBc. Everything common to the two readings cancels,
which is what lets us lay a beam sweep and an azimuth sweep on the same axes.
The lesson and the L21 Lab quote every lobe level in dBc.
::::

::::{frame} Beam Sweep and Azimuth Sweep at Broadside
:::{present}
- The main lobe and first sidelobes match: about $-13$ dBc on both.
- The nulls drop to the noise floor, about $-23$ dBc, on both.
- Past $\pm 50^\circ$ the azimuth sweep reads lower.
:::
:::{present}
<img src="../../viz/img/L21-beam-vs-azimuth-0.svg"
     alt="Predicted beam sweep and azimuth sweep at broadside, in dBc: the main lobes and first sidelobes coincide near minus 13 dBc and every null drops to a dashed noise floor at minus 23 dBc; the outer lobes read about minus 17 dBc on the beam sweep and minus 19 dBc on the azimuth sweep."
     style="max-width: 560px; width: 100%; display: block; margin: 0 auto;">
:::

The figure predicts both traces for a beam at broadside. The beam sweep
holds the HB100 at boresight and steps the beam; the azimuth sweep holds the
beam at $0^\circ$ and moves the HB100. Out to the first sidelobes, at
$\pm 21.9^\circ$, the two lie on top of each other, and both put the first
sidelobes about 13 dB below the peak. That comparison is the one the L21 Lab
asks for, because the main lobe and first sidelobes stand well above the
noise floor and the room's reflections.

Every null drops to the noise floor, about $23\ \text{dB}$ below the peak,
which the L20 Lab measured. The floor also lifts the outer sidelobes, which
the array factor puts at $-16$ to $-18$ dB, by a decibel or two on both
traces. The difference between the traces near $\pm 63^\circ$, about
$2.5\ \text{dB}$, comes from each patch's own pattern. A patch over a ground plane radiates nothing
behind the board and less and less toward the horizon; the course models it
as the ideal element of "Gain of the Course Array" below, whose power falls
as $\cos\theta$, $3.4\ \text{dB}$ down at $63^\circ$. The azimuth sweep moves
the HB100 out there, and the beam sweep never does. A real patch falls off
faster than the ideal element, so expect the outer lobes of your azimuth
sweep to read lower still. At the first sidelobes the patch pattern changes
the level by only $0.3\ \text{dB}$.
::::

::::{frame} Beam Sweep and Azimuth Sweep at 30°
:::{present}
- Both put the nulls at $13.9^\circ$ and $49.5^\circ$: the lobe is wider outside.
- The outer first sidelobe reads about 2 dB lower on the azimuth sweep.
:::
:::{present}
<img src="../../viz/img/L21-beam-vs-azimuth-30.svg"
     alt="Predicted beam sweep and azimuth sweep for a 30 degree beam, in dBc: both peak near 30 degrees with nulls at 13.9 and 49.5 degrees on the dashed noise floor; the inner first sidelobes match near minus 12 dBc, while the outer one near 60 degrees reads about minus 12 dBc on the beam sweep and minus 14.5 dBc on the azimuth sweep."
     style="max-width: 560px; width: 100%; display: block; margin: 0 auto;">
:::

Steering does not change the agreement. For the azimuth sweep, set the Steer
Angle to $30^\circ$ and carry the HB100 around the arc; for the beam sweep,
put the HB100 at $30^\circ$ and let the kit step the beam past it. The array
factor slides in $\sin\theta$, not in $\theta$ (Lesson 18, "Rigid Shift in
Sine Space"), so at $10.3\ \text{GHz}$ the first nulls fall at
$\sin\theta = 0.5 \pm 0.260$, which is $13.9^\circ$ and $49.5^\circ$. The main
lobe reaches $16.1^\circ$ below its peak and $19.5^\circ$ above it, on both
traces.

The outer first sidelobe, near $60^\circ$, reads about $-12$ dBc on the beam
sweep and about $-14.5$ dBc on the azimuth sweep. The patch pattern causes
that difference. The azimuth sweep reads in dBc of its own peak at
$30^\circ$, where the ideal element is down $0.6\ \text{dB}$, and carries the
HB100 out to $60^\circ$, where it is down $3.0\ \text{dB}$; the sidelobe
therefore drops by the difference, about $2.4\ \text{dB}$, which the noise
floor trims to about $2\ \text{dB}$. The beam sweep keeps the HB100 at
$30^\circ$ for every step. On my kit the room alone made the two first
sidelobes of a broadside azimuth sweep differ by about $3\ \text{dB}$ (11.5
and 14.8 dBc), so a single azimuth sweep cannot separate the patch pattern
from the room.
::::

::::{frame} Measurement Errors
:::{present}
| Error | Size | Trace |
| :-- | :-- | :-- |
| Room reflections | $\pm 1$ dB a reading | both |
| Radius drift, $10\ \text{cm}$ | $0.7$ dB | azimuth |
| Uneven pace | stretches lobes in time | azimuth |
| Phase grid | beamwidth off by up to $1^\circ$ | beam |
| Noise floor | about $-23$ dBc | both |
:::

**Room reflections.** The lab is not an anechoic chamber. Signals from the
HB100 also reach the array off the floor, the ceiling, the benches, and the
people nearby, and they add to the direct signal in and out of phase. A
reflection $18\ \text{dB}$ below the level being read moves that reading by
about a decibel, and the same reflection moves a weaker lobe by more. The
far sidelobes are therefore the least trustworthy part of either trace, and a
lobe that moves when you move the kit or a person comes from the room. Lesson
9 shows why the nulls feel this first
(<a href="../../module02/L09-pattern-measurement-theory/index.html#frame-the-nulls-fill-first">"The Nulls Fill First"</a>).

**Radius drift and pace** belong to the azimuth sweep by hand, for the reasons
in "The Time Axis." **The phase grid** places each beam-sweep point one step
apart, so each half-power crossing can be off by half a step and a beamwidth
by up to a step, about $1^\circ$. **The noise floor** is the level the nulls
drop to; the L20 Lab found it about $23\ \text{dB}$ below the peak of each
trace.
::::

::::{frame} Source Distance
:::{present}
$$
\begin{aligned}
r &\ge \frac{2D^2}{\lambda} = \frac{2(0.112\ \text{m})^2}{0.0291\ \text{m}} \\
&= 0.86\ \text{m}
\end{aligned}
$$

- $D = Nd = 112\ \text{mm}$, as in Lesson 18.
- The L21 Lab sets the HB100 $1.2\ \text{m}$ out, clear of the far-field distance.
:::

The HB100 must sit past Lesson 5's far-field distance, or the wavefront
curves across the array and the edge elements see more than the
$22.5^\circ$ ($\lambda/16$ of path) of phase error the criterion allows,
which fills the nulls and raises the sidelobes (Lesson 9,
<a href="../../module02/L09-pattern-measurement-theory/index.html#frame-where-2d-comes-from">"Where 2D²/λ Comes From"</a>).
Lesson 18 took the aperture as $D = Nd = 112\ \text{mm}$, since each element
accounts for one spacing of aperture, which puts the boundary at
$0.86\ \text{m}$ at $10.3\ \text{GHz}$ and $0.88\ \text{m}$ at
$10.525\ \text{GHz}$. The L21 Lab uses $1.2\ \text{m}$, which stays past the
boundary even with a hand-carried source drifting in and out.
::::

::::{frame} Reading Your Two Traces
:::{present}
| Feature | What to expect |
| :-- | :-- |
| Main lobe | same level on both |
| First sidelobes, broadside | $-13$ dBc on both, $\pm 2$ dB |
| Outer sidelobe at $30^\circ$ | 2 dB lower on the azimuth sweep |
| Farther sidelobes | qualitative only |
| Nulls | noise floor, about $-23$ dBc |
:::

The L21 Lab gives you a beam sweep, three azimuth sweeps by hand, and one
pass of the kit on its stand that reads the $0^\circ$ and $30^\circ$ beams
together. Compare them lobe by lobe, in dBc. The main lobe and the first
sidelobes are where the methods should agree: a first sidelobe of a
broadside beam reads about 13 dB below the peak on every trace, and the room
moves each dBc value by up to about $2\ \text{dB}$, since a dBc value is the
difference of two readings that each carry about $\pm 1\ \text{dB}$. The
farther sidelobes are recognizable but not quantitative, because the noise
floor, the room, and the patch pattern all act there. Read angles from the
stand's scale.
::::

::::{frame} Gain of the Course Array
:class: read-only

Later lessons use one gain figure for the course array, which we get by
modeling each patch as an ideal element that collects its share of the
aperture. Lesson 2 tied gain to effective aperture,

$$
G = \frac{4\pi A_e}{\lambda^2} ,
$$

and seen from $\theta$ off broadside that share presents its projected area
$A\cos\theta$, so the element's power pattern is

$$
G_e(\theta) = G_e(0)\cos\theta ,
$$

the same projection that sets scan loss in Lesson 18 ("Scan Loss"). The
ground plane blocks the back hemisphere, so with $U = U_0\cos\theta$ over the
front hemisphere only, Lesson 2's directivity gives

$$
\begin{aligned}
D_e &= \frac{4\pi U_\text{max}}{P_\text{rad}} \\
P_\text{rad} &= \int_0^{2\pi}\!\!\int_0^{\pi/2} U_0\cos\theta\ \sin\theta\ d\theta\ d\phi \\
&= \pi U_0 \\
D_e &= \frac{4\pi U_0}{\pi U_0} = 4 = 6.0\ \text{dBi} .
\end{aligned}
$$

Eight such elements tile the aperture, so the array collects eight times one
element's share and adds $10\log_{10} 8 = 9.0\ \text{dB}$:

$$
\begin{aligned}
G(\theta_0) &= G_e(0) + 10\log_{10} N \\
&\quad + 10\log_{10}(\cos\theta_0) \\
&= 15.0 + 10\log_{10}(\cos\theta_0)\ \text{dBi} ,
\end{aligned}
$$

which is $15.0\ \text{dBi}$ at broadside and $14.4$, $13.5$, and
$12.0\ \text{dBi}$ steered to $30^\circ$, $45^\circ$, and $60^\circ$. Lesson
20 wrote the same sum with the array factor's directivity, $8.9\ \text{dB}$,
in place of $10\log_{10} 8$; the two agree within $0.2\ \text{dB}$.
::::

::::{frame} Summary
:class: read-only

| Idea | What it is | Number to remember |
| :-- | :-- | :-- |
| Beam sweep | the Rectangular plot: beam stepped past a fixed source, one point from each beam | 162 steps of $2.8125^\circ$; $0.93^\circ$ near broadside |
| Why it traces a pattern | $\vert AF\vert$ depends only on $\sin\theta_\text{src} - \sin\theta_0$ | stepping the beam or moving the source visits the same curve |
| Azimuth sweep | one beam held, source moved in azimuth or antenna turned | Signal vs Time by hand; the stand's scale for angles |
| dBc | level relative to the trace's own main-lobe peak | removes Rx Gain, distance, and source power |
| Agreement | main lobe and first sidelobes | about $-13$ dBc at broadside, $\pm 2$ dB |
| Patch pattern | seen by the azimuth sweep, not by the beam sweep | outer sidelobe of a $30^\circ$ beam about 2 dB lower; the room adds as much |
| Source distance | $r \ge 2D^2/\lambda$, $D = Nd = 112\ \text{mm}$ | $0.86\ \text{m}$; measure at $1.2\ \text{m}$ |

::::

::::{frame} Preparing for the Lab
:class: read-only doc-links

Part 1 of the L21 Lab packet works out what you should see at the bench, so you can tell a good trace from a bad one while you are still at the kit. Complete it before the lab period.

- <a class="doc-link" href="../../labs/ECE444_Lab_L21_Pattern_blank.pdf" target="_blank" rel="noopener">L21 Lab packet, Part 1 (PDF)</a>
::::

::::{frame} Looking Ahead
:::{present}
- The L21 Lab: a beam sweep, an azimuth sweep by hand, and one on the stand; compare lobe levels.
- Lesson 22: taper the Element Gains to push the first sidelobes below $-13$ dBc.
:::

In the L21 Lab you take the same pattern three ways and compare the lobe
levels in dBc, using the error table above to judge whether two values
agree. Every trace so far has had uniform illumination, which fixes the
first sidelobes near $-13$ dBc. Lesson 22 feeds the eight elements
unequally, with more power in the middle and less at the edges, which pushes
the sidelobes down and widens the main lobe.
::::
