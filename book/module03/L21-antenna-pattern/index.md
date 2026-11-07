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
Rectangular plot. The kit builds that plot by holding the HB100 still,
stepping the beam past it, and plotting the level it receives at each
commanded angle, so each point on the trace comes from a different beam. An
antenna range measures a pattern the other way: it holds one beam still and
moves the source around it. Today we take that second measurement with the
kit's Signal vs Time mode, compare it with the sweep, and sort out which
features of a trace the two methods agree on and which they do not.
:::
::::

::::{frame} The Rectangular Plot
:::{present}
- The HB100 stays put while the kit steps the element-to-element phase, $2.8125^\circ$ at a time.
- Each step makes a different beam; the plot shows its level at the commanded angle.
- One trace is 162 steps.
:::

You built this trace step by step in the L18 Lab
(<a href="../L18-lab-beam-steering/index.html#frame-the-beam-sweep-trace">"The Beam-Sweep Trace"</a>).
With Use Bits on, as in every lab preset, the kit adds one phase-shifter LSB,
$2.8125^\circ$, to the element-to-element phase, writes that ramp to the eight
channels, reads the peak of the FFT, and plots the reading at the angle the
ramp steers to. At $10.3\ \text{GHz}$ one step moves $\sin\theta_0$ by
$2.8125^\circ/173.2^\circ = 0.0162$, which is $0.93^\circ$ of angle near
broadside and $1.07^\circ$ at $30^\circ$. The L20 Lab showed what that grid
and the trace's floor do to the readings
(<a href="../L20-lab-array-factor/index.html#frame-reading-a-sweep-for-what-it-is">"Reading a Sweep for What It Is"</a>).
::::

::::{frame} The Sweep, Step by Step
:class: viz-frame

:::{depth}
This is the sweep the kit runs, slowed down. Press **step** to add one phase
LSB at a time and watch the left panel: the beam swings past the HB100, and
the inset adds the eight element signals tip to tail. Away from the source
the chain curls up and the point lands in a sidelobe or on the floor; as the
beam reaches the source the chain straightens and the trace climbs to its
peak. Each point on the right panel comes from the beam on the left at that
moment, never from one beam held still.
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

::::{frame} Why the Sweep Traces a Pattern
:::{present}
$$
\psi = kd\left(\sin\theta_\text{src} - \sin\theta_0\right)
$$

- The array factor depends only on $\psi$, and $\vert AF\vert$ is even in $\psi$.
- Stepping the beam past a fixed source and moving the source past a fixed beam trace the same curve.
:::

Lesson 18 ("The Steered Pattern") showed that steering replaces the
array-factor argument with

$$
\psi = kd\left(\sin\theta_\text{src} - \sin\theta_0\right),
$$

where $\theta_\text{src}$ is the direction the signal arrives from and
$\theta_0$ is the angle the phase ramp steers to. The sweep holds
$\theta_\text{src}$ and steps $\theta_0$; an antenna range holds $\theta_0$
and moves $\theta_\text{src}$. Both run $\psi$ through the same values, and
$\vert AF\vert$ is the same for $\psi$ and $-\psi$, so both draw the same
curve. That is why a trace built from 162 different beams looks like the
pattern of one beam, and it is also why the two methods can differ: the
sweep's x-axis is a commanded angle, and everything the array factor leaves
out enters the two measurements differently.
::::

::::{frame} The Antenna-Range Method
:::{present}
- An antenna range holds the beam still and moves the source, or turns the antenna.
- Every point comes from the same beam.
- The x-axis is the source's physical angle.
:::
:::{present}
<img src="../../viz/img/L21-two-methods.svg"
     alt="Left: the beam sweeps electronically past a stationary HB100. Right: the beam is held fixed while the HB100 is carried around the array on a 1.2 m arc."
     style="max-width: 560px; width: 100%; display: block; margin: 0 auto;">
:::

An antenna range measures a pattern the direct way. The antenna under test
sits on a turntable with its beam fixed, a source stands at a fixed distance,
and the turntable records the received level against the angle between the
two. Every reading comes from the same beam, and each one carries the
physical angle the turntable reports. The L21 Lab does this twice: once by
carrying the HB100 around the kit by hand, and once by turning the kit on its
stand in front of the HB100.
::::

::::{frame} Signal vs Time Mode
:::{present}
- The kit holds the beam at the Steer Angle and plots the peak level against time.
- You carry the HB100 from $-90^\circ$ to $+90^\circ$ on a $1.2\ \text{m}$ arc.
- The trace is one beam's pattern, drawn as you walk.
:::

Lab Preset 7, **Antenna Pattern**, sets **Mode** to **Signal vs Time**. In
that mode the kit stops sweeping: it holds every element at the phase for the
**Steer Angle** you set and the Tracking tab plots the FFT peak against
elapsed time. As you carry the HB100 around the arc, the level at each
instant is the held beam's response in the direction the HB100 occupies at
that instant. This is the measurement in ADI's PHASER workshop, "Measuring
the Actual Antenna Pattern," and the L21 Lab's hand walk.
::::

::::{frame} The Walk, Simulated
:class: viz-frame

:::{depth}
The widget runs the walk in simulation. Choose a steer angle and a walking
profile, then watch the trace paint as the source moves around the arc. Run
it once with the uniform profile and once with the hand-like profile, and
compare the readouts: the lobe spacing changes and the lobe levels do not.
The simulation holds the radius perfectly; your arm will not.
:::

:::{present}
<iframe src="../../viz/pattern-measurement-sim.html"
        width="100%" height="461"
        style="border: 1px solid #cddce9; border-radius: 6px;"
        loading="lazy"
        title="Simulated hand-walk pattern measurement: a source walks an arc around a fixed beam while the level-versus-time trace paints below">
</iframe>
:::
::::

::::{frame} Amplitudes Survive, Angles Do Not
:::{present}
- Each instant's level is the pattern at where the source is, whatever its speed.
- An uneven pace moves and stretches the lobes in time; it cannot change their heights.
:::
:::{present}
<img src="../../viz/img/L21-time-vs-angle.svg"
     alt="The same walked run plotted twice: against elapsed time, where the lobes are unevenly spaced, and against true source angle, where they are symmetric. The lobe levels are identical on both."
     style="max-width: 560px; width: 100%; display: block; margin: 0 auto;">
:::

The x-axis of a walk is time, and time becomes angle only at a constant pace.
Walking slowly through a lobe draws it wider on the plot, and hurrying
through it draws it narrower, but the level at each instant is still the
pattern at the source's angle, so the lobe heights come through unchanged.
ADI's workshop says the same thing: "we can't really get angular
measurements from this ... but we can get accurate lobe amplitudes." We
compare a walk with a sweep by lobe level, not by angle.

Your arm still moves the level in one way. Received power falls as $1/r^2$,
so drifting $10\ \text{cm}$ in or out at $1.2\ \text{m}$ changes a reading by
$20\log_{10}(1.3/1.2) = 0.7\ \text{dB}$ to
$20\log_{10}(1.2/1.1) = 0.8\ \text{dB}$. Turning the kit on its stand holds the
distance fixed and reads each angle off the stand's scale, which is why the
L21 Lab does both.
::::

::::{frame} Sweep and Walk at Broadside
:::{present}
- The main lobe and first sidelobes match: about $-13$ dBc on both traces.
- Farther out, the sweep sits on its $-23$ dBc floor and the walk reads lower.
:::
:::{present}
<img src="../../viz/img/L21-sweep-walk-0.svg"
     alt="Predicted sweep and walk at broadside, in dBc of their own peaks: the main lobes and first sidelobes coincide near minus 13 dBc; beyond 30 degrees the sweep's points sit on a floor near minus 17 to minus 20 dBc while the walk's lobes fall to about minus 17 and minus 20 dBc and its nulls to minus 27"
     style="max-width: 560px; width: 100%; display: block; margin: 0 auto;">
:::

The figure predicts both traces for a beam at broadside. The sweep holds the
HB100 at boresight and steps the beam; the walk holds the beam at $0^\circ$
and moves the HB100. Out to the first sidelobes, at $\pm 21.9^\circ$, the two
lie on top of each other, and both put the first sidelobes about 13 dB below
the peak. That is the comparison the L21 Lab asks for, and it is the part of
a trace that holds up in a classroom.

Beyond the first sidelobes the traces part for two reasons. The sweep has a
floor about $23\ \text{dB}$ below its peak (the L20 Lab), and its outer
sidelobes, which the array factor puts at $-16$ to $-18$ dB, sit only a few
decibels above that floor, so the floor adds to them. The walk also moves the
HB100 across the pattern of each patch, which falls toward $\pm 90^\circ$
because the ground plane blocks everything behind the board; the sweep holds
the HB100 in one place, so that pattern is the same for every point and drops
out of a trace read in dBc. The patch pattern lowers the walk's lobes near
$\pm 63^\circ$ by about $3.6\ \text{dB}$ and its first sidelobes by only
$0.3\ \text{dB}$.
::::

::::{frame} Sweep and Walk at 30°
:::{present}
- Walk: the beam held at $30^\circ$. Sweep: the HB100 placed at $30^\circ$.
- Both put the first nulls at $13.9^\circ$ and $49.5^\circ$, so the lobe is wider on the outside.
:::
:::{present}
<img src="../../viz/img/L21-sweep-walk-30.svg"
     alt="Predicted sweep and walk for a 30 degree beam, in dBc of their own peaks: both peak near 30 degrees with nulls at 13.9 and 49.5 degrees; the inner first sidelobes match near minus 12 dBc, while the outer one near 60 degrees reads about minus 12 dBc on the sweep and minus 15 dBc on the walk"
     style="max-width: 560px; width: 100%; display: block; margin: 0 auto;">
:::

Steering does not change the agreement. For the walk, set the Steer Angle to
$30^\circ$ and carry the HB100 around the arc; for the sweep, put the HB100
at $30^\circ$ and let the kit step the beam past it. The array factor slides
in $\sin\theta$, not in $\theta$ (Lesson 18, "Rigid Shift in Sine Space"), so
at $10.3\ \text{GHz}$ the first nulls fall at $\sin\theta = 0.5 \pm 0.260$,
which is $13.9^\circ$ and $49.5^\circ$. The main lobe reaches $16.1^\circ$
below its peak and $19.5^\circ$ above it, on both traces.

The outer first sidelobe, near $60^\circ$, is where the two differ most:
about $-12$ dBc on the sweep and $-15$ dBc on the walk. The patch pattern
causes that difference. The walk carries the HB100 out to $60^\circ$, where
each patch receives about $3\ \text{dB}$ less than at broadside, while the
sweep keeps the HB100 at $30^\circ$ for every point. On my kit the room alone
made the two first sidelobes of a broadside walk differ by about
$3\ \text{dB}$ (11.5 and 14.8 dBc), so a single walk cannot separate the
patch pattern from the room. The sweep with the HB100 at $30^\circ$ also
peaks about $0.6\ \text{dB}$ below the sweep with the HB100 at boresight,
which is the scan loss you measured in the L18 Lab (Lesson 18, "Scan Loss").
::::

::::{frame} What Bends a Measured Trace
:::{present}
| Error | Size | Trace |
| :-- | :-- | :-- |
| Room reflections | $\pm 1$ dB a reading | both |
| Radius drift, $10\ \text{cm}$ | $0.7$ dB | walk |
| Uneven pace | angles, not levels | walk |
| Phase grid | up to $1^\circ$ on a width | sweep |
| Floor | about $-23$ dBc | sweep |
:::

**Room reflections.** The lab is not an anechoic chamber. Signals from the
HB100 also reach the array off the floor, the ceiling, the benches, and the
people nearby, and they add to the direct signal in and out of phase. One
reflection $18\ \text{dB}$ below the direct path moves a reading by about a
decibel. The effect is largest where the pattern is weakest, so the far
sidelobes are the least trustworthy part of either trace, and a lobe that
moves when you move the kit or a person comes from the room.

**Radius drift and pace** belong to the walk alone, for the reasons in
"Amplitudes Survive, Angles Do Not." **The phase grid** places each sweep
point one step apart, so each half-power crossing can be off by half a step
and a beamwidth by up to a step, about $1^\circ$. **The floor** is where the
sweep stops following the array factor; the L20 Lab found it about
$23\ \text{dB}$ below the peak of each trace.
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

Lesson 5 put the far-field boundary at $r \ge 2D^2/\lambda$, with $D$ the
largest dimension of the aperture. For a pattern measurement the HB100 must
sit past it, or the wavefront curves across the array and the edge elements
see more than the $22.5^\circ$ ($\lambda/16$ of path) of phase error the
criterion allows, which fills the nulls and raises the sidelobes. Lesson 18
took the aperture as $D = Nd = 112\ \text{mm}$, since each element accounts
for one spacing of aperture, which puts the boundary at $0.86\ \text{m}$ at
$10.3\ \text{GHz}$ and $0.88\ \text{m}$ at $10.525\ \text{GHz}$. The L21 Lab
uses $1.2\ \text{m}$, which stays past the boundary even with the walk's
radius drift.
::::

::::{frame} Reading Your Two Traces
:::{present}
| Feature | What to expect |
| :-- | :-- |
| Main lobe | same level on both; the walk's width follows your pace |
| First sidelobes | about $-13$ dBc on both, within $\pm 2$ dB |
| Farther sidelobes | recognizable, not quantitative |
| Below $-23$ dBc | the floor |
:::

The L21 Lab gives you a sweep, three walks, and a turn of the kit on its
stand. Compare them lobe by lobe. The main lobe and the first sidelobes are
where the methods should agree: a first sidelobe reads about 13 dB below the
peak on every trace, and the room moves each dBc value by up to about
$2\ \text{dB}$, since a dBc value is the difference of two readings that
each carry $\pm 1\ \text{dB}$. The farther sidelobes are recognizable but not
quantitative, because the floor, the room, and the patch pattern all act
there. Read angles from the sweep or from the stand's scale, never from the
walk's time axis.
::::

::::{frame} Gain of the Course Array
:class: read-only

Later lessons use one gain figure for the course array, and it comes from a
simple model of each patch. Model each patch as an ideal element that
collects its share of the aperture. Lesson 2 tied gain to effective aperture,
$G = 4\pi A_e/\lambda^2$, and seen from $\theta$ off broadside that share
presents its projected area $A\cos\theta$, so the element's power pattern is

$$
G_e(\theta) = G_e(0)\cos\theta ,
$$

the same projection that sets scan loss in Lesson 18 ("Scan Loss"). The
ground plane blocks the back hemisphere, so Lesson 2's
$D = 4\pi U_\text{max}/P_\text{rad}$ with $U = U_0\cos\theta$ over the front
hemisphere gives

$$
\begin{aligned}
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
$12.0\ \text{dBi}$ steered to $30^\circ$, $45^\circ$, and $60^\circ$.
::::

::::{frame} Summary
:class: read-only

| Idea | What it is | Number to remember |
| :-- | :-- | :-- |
| Rectangular plot | the beam stepped past a fixed source; one point from each beam | 162 steps of $2.8125^\circ$; $0.93^\circ$ near broadside |
| Why it traces a pattern | $\vert AF\vert$ depends only on $\sin\theta_\text{src} - \sin\theta_0$ | moving the beam or the source gives the same curve |
| Antenna-range method | one beam held, source moved or antenna turned | Signal vs Time; x-axis is time |
| Walk | lobe levels survive, angles do not | $0.7$ dB for $10\ \text{cm}$ of radius drift |
| Agreement | main lobe and first sidelobes | about $-13$ dBc, $\pm 2$ dB |
| Patch pattern | seen by the walk, not by the sweep | outer sidelobe of a $30^\circ$ beam about $3$ dB lower; the room adds as much |
| Source distance | $r \ge 2D^2/\lambda$, $D = Nd = 112\ \text{mm}$ | $0.86\ \text{m}$; measure at $1.2\ \text{m}$ |

::::

::::{frame} Practice
:class: read-only doc-links

- <a class="doc-link" href="../../practice/ECE444_L21_Practice_blank.pdf" target="_blank" rel="noopener">Problem set (PDF)</a>
- <a class="doc-link doc-key" href="../../practice/ECE444_L21_Practice_SOLUTIONS.pdf" target="_blank" rel="noopener">Solutions (PDF)</a>

::::

::::{frame} Looking Ahead
:::{present}
- The L21 Lab: sweep, walk, and turn the kit, then compare lobe levels.
- Lesson 22: taper the Element Gains to push the first sidelobes below $-13$ dBc.
:::

In the L21 Lab you take the same pattern three ways and compare the lobe
levels, with the error table above as the yardstick for what counts as
agreement. Every trace so far has had uniform illumination, which fixes the
first sidelobes near $-13$ dBc. Lesson 22 feeds the eight elements
unequally, with more power in the middle and less at the edges, which pushes
the sidelobes down and widens the main lobe.
::::
