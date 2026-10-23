---
frame_view: true
---

# L21 Lab — Antenna Pattern

::::{frame}
:class: title-frame

<div class="course-mark">ECE 444 · Fall 2026</div>

<h1 class="frame-title">Antenna Pattern</h1>

<div class="title-rule"></div>

Hold the beam still and move the source past it: first by hand, then on a turntable.

L21 Lab · Antennas, Phased Arrays, and Radar Systems · Dr. Neil Rogers
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
::::

::::{frame} From Prediction to Measurement
:::{present}
- Part 1, before today: the expected patterns and two error budgets.
- Part 2, today: walk the source by hand, then turn the kit over a protractor.
- Part 3, after: which model the data support, and which method resolves it.
:::

Lesson 21 separated the array factor from the pattern the array radiates and
predicted where the two part company: the peak drops as $\cos\theta_0$ when the
beam steers, the two first sidelobes of a steered beam stop matching, and
nothing comes out the back. Today we test those predictions on the bench. The
L21 Lab packet starts from them: Part 1, the pre-lab you completed before
class, works out the patterns at your HB100's frequency and sizes the errors of
the two methods. Today you measure the pattern twice with the beam held still,
once by carrying the source around the array by hand and once by turning the
kit in front of a fixed source. Part 3, on your own before Lesson 22,
reconciles the numbers with the predictions and compares the two methods.
::::

::::{frame} Three Ways to Trace a Pattern
:::{present}
| | Sweep the beam | Walk the source | Turn the kit |
| :-- | :-- | :-- | :-- |
| x-axis | steer angle | elapsed time | protractor angle |
| Measures | array factor | element $\times$ array | element $\times$ array |
| Distance | fixed | your arm | fixed |
:::
:::{present}
<img src="../../viz/img/L21-two-methods.svg"
     alt="Left: the beam sweeps electronically past a stationary HB100. Right: the beam is held fixed while the HB100 is carried around the array on a 1.2 m arc."
     style="max-width: 560px; width: 100%; display: block; margin: 0 auto;">
:::

There are three ways to get a pattern out of an array, and they are not the
same measurement.

The first is the one you have used since the L18 Lab: put a source somewhere,
leave it there, and **sweep the beam** electronically past it, recording
received power at each steer angle. The source sits at one physical angle, so
the element pattern contributes the same constant to every point on the trace
and drops out of its shape. The trace is the array factor, plotted against the
angle the beamformer was commanded to.

The second is the one ADI's workshop uses. **Hold the beam fixed** and carry the
source around the array on an arc. Now the physical angle changes at every
instant, so the element pattern multiplies the array factor exactly as Lesson 21
described, and the trace is the antenna pattern. The GUI plots it against
elapsed time, though, so the angle axis is only as good as your walking, and
the level is only as steady as your arm.

The third is what an antenna range does. Hold the beam fixed, leave the source
on its tripod, and **turn the kit** in front of it. The trace is the antenna
pattern again, but every reading carries a real angle, and the distance to the
source never changes.
::::

::::{frame} What Lesson 21 Predicts
:::{present}
| At $10.525\ \text{GHz}$ | Beam at $0^\circ$ | Beam at $30^\circ$ |
| :-- | :-- | :-- |
| Peak | $0^\circ$, reference | $29.6^\circ$, $-0.6$ dB |
| First nulls | $\pm 14.7^\circ$ | $14.2^\circ$, $49.0^\circ$ |
| First sidelobes | $\pm 21.4^\circ$, $-13.1$ dBc | $-12.2$, $-15.1$ dBc |
| Behind the board | floor | floor |
:::

Part 1 of the packet works these out at your own kit's frequency; the dBc values
barely move with frequency, and the angles move by about $0.15^\circ$ per
$100\ \text{MHz}$, less than you can read off a protractor. With the beam at
$0^\circ$ the element pattern lowers the $\pm 21.4^\circ$ sidelobes by only
$0.3\ \text{dB}$, too little to see in a room. With the beam at $30^\circ$ it
lowers the peak by $0.6\ \text{dB}$ and the outer sidelobe, near $59^\circ$, by
$2.9\ \text{dB}$, while the inner one, near $8^\circ$, sits where the element is
flat. The array factor alone would put both at $-12.8$ dBc. The ground plane
removes the back hemisphere, so the reading with the source behind the board
should sit at the floor.
::::

::::{frame} The Walk Paints as You Go
:class: viz-frame

:::{depth}
The widget below runs the walk in simulation. Choose a steer angle and a
walking-speed profile, then watch the trace paint as the source moves around the
arc. Run it once with the uniform profile and once with the hand-like profile,
and compare the two readouts: the lobe spacing changes completely and the lobe
levels do not move at all. The simulation keeps the radius perfect; your arm
will not.
:::

:::{present}
<iframe src="../../viz/pattern-measurement-sim.html"
        width="100%" height="459"
        style="border: 1px solid #cddce9; border-radius: 6px;"
        loading="lazy"
        title="Simulated hand-walk pattern measurement: a source walks an arc around a fixed beam while the level-versus-time trace paints below">
</iframe>
:::
::::

::::{frame} Amplitudes Survive, Angles Do Not
:::{present}
- The walk's x-axis is time: an uneven pace moves and stretches the lobes.
- Pace cannot change a lobe's height, but a $10\ \text{cm}$ radius drift moves it $0.7\ \text{dB}$.
:::
:::{present}
<img src="../../viz/img/L21-time-vs-angle.svg"
     alt="The same measured run plotted twice: against elapsed time, where the lobes are unevenly spaced, and against true source angle, where they are symmetric. The lobe amplitudes are identical on both."
     style="max-width: 560px; width: 100%; display: block; margin: 0 auto;">
:::

The level the GUI records at any instant is the pattern at the angle the source
occupied at that instant, and it does not depend on how fast the source was
moving. Walking slowly through a lobe draws it wider on the plot without
changing its height, so the lobe levels survive an uneven walk and the angles do
not. The level is not immune to your arm, though: received power goes as
$1/r^2$, so drifting $10\ \text{cm}$ in or out at $1.2\ \text{m}$ moves the
reading by $0.7$ to $0.8\ \text{dB}$, more than the scan loss you want to see.
Three walks, compared in the packet, show how large that scatter is in practice.
::::

::::{frame} The Paper Turntable
:::{present}
- The HB100 stays on its tripod, $1.2\ \text{m}$ out; you turn the kit about the array's center.
- Facing the patches, E1 is on the right. Turning the face toward E1 puts the source at $+\theta$.
:::
:::{present}
<img src="../../viz/img/L21-rotation-setup.svg"
     alt="Top view of the rotation setup: the HB100 fixed 1.2 m from the array, and the kit turned 30 degrees about the array center over a protractor, its face toward E1, which puts the source at plus 30 degrees on the E8 side"
     style="max-width: 560px; width: 100%; display: block; margin: 0 auto;">
:::

Turning the kit in front of a fixed source records the same pattern as walking
the source around a fixed kit, because only the angle between the array normal
and the source matters. What changes is everything else. The distance never
changes, so the levels can be compared from one reading to the next; the HB100
stays aimed at the array without effort; and each reading is taken at an angle
you can read off the protractor.

Lesson 18 put $+\theta$ on the E8 end of the array. Looking at the patches, E1
is at the right end of the row and E8 at the left. Turn the kit so that its face
swings toward the E1 end, as seen from the source, and the source ends up on the
E8 side of the normal, at $+\theta$; the kit's pointer reads the same angle on
the protractor. Part 2 starts by confirming that sign with a beam sweep, whose
**Angle** readout, set to **Peak**, reads the source's angle.

Two things set how good the rotation is. The kit must turn about the center of
the array, between E4 and E5: an axis $20\ \text{mm}$ off center moves the
source's apparent angle by up to $1^\circ$ and its distance by up to
$20\ \text{mm}$, about $0.14\ \text{dB}$. And the protractor reads to about a
degree, which is fine for a lobe $15^\circ$ wide.
::::

::::{frame} The Steered Pattern
:::{present}
- Beam held at $30^\circ$: the peak is $0.6\ \text{dB}$ below the broadside peak.
- Inner sidelobe $-12.2$ dBc, outer $-15.1$ dBc: the element pattern, not a fault.
:::
:::{present}
<img src="../../viz/img/L21-steer-compare.svg"
     alt="Broadside and 30-degree steered patterns on a true-angle axis, showing the 0.6 dB scan loss and the unequal first sidelobes of the steered beam."
     style="max-width: 560px; width: 100%; display: block; margin: 0 auto;">
:::

With the beam held at $30^\circ$, the main lobe appears when the source reaches
about $30^\circ$ instead of boresight. The peak reads lower than the broadside
run, by $0.6\ \text{dB}$ for the ideal element and about $0.9\ \text{dB}$ for a
real patch; the Module 3 dry run measured $0.7\ \text{dB}$ with the source
$1.2\ \text{m}$ out. The rotation can resolve that difference because the
distance never changes. A walk cannot, because the radius drift alone is as
large as the effect.

The pattern is no longer symmetric. The first sidelobe on the inside of the
beam, near $+8^\circ$, sits about $-12.2$ dBc; the one on the outside, near
$+59^\circ$, sits about $-15.1$ dBc. The array factor alone would make them
equal, and the element pattern lowers the outer one. A careful walk can show the
direction of that $2.9\ \text{dB}$ asymmetry; the rotation can put a number on
it.
::::

::::{frame} Two Error Budgets
:::{present}
| Error | Walk | Rotation |
| :-- | :-- | :-- |
| Angle axis | time, not angle | $\pm 1^\circ$ |
| Distance | $\pm 0.7$ dB | $\pm 0.14$ dB |
| Room reflections | $\pm 1$ dB | $\pm 1$ dB |
:::

The packet's Part 1 builds both budgets. The walk's angle error comes from
converting time to angle at a constant pace you did not have: a hand $30\%$
fast or slow through the main lobe makes a $13.0^\circ$ beam read anywhere from
$10.0^\circ$ to $18.6^\circ$. Its level error comes from the radius. The
rotation removes both, and replaces them with the axis offset and the
protractor, which are small and can be measured. Neither method removes the
room: a single reflection $18\ \text{dB}$ below the direct path moves a reading
by a decibel. The rotation's advantage there is repeatability. The reflections
sit in fixed places in the room, so a reading repeated at the same angle comes
back to the same value, and a difference between two of them is more
trustworthy than either reading alone.
::::

::::{frame} Equipment and Setup
:::{present}
- The kit, cabled to your laptop as in Lesson 17, on a protractor centered between E4 and E5.
- The HB100 on its tripod, $1.2\ \text{m}$ out at patch-row height, and a taped $1.2\ \text{m}$ arc.
:::

You need the ADALM-PHASER kit on its stand, connected to your laptop by the
Ethernet cable as in Lesson 17; the HB100 with a fresh battery, on its tripod;
a protractor, printed or on a turntable, centered under the middle of the array
between E4 and E5 and fixed to the bench with $0^\circ$ pointing at the source;
a mark on the kit's stand along the array normal, to read the protractor
against; and masking tape.

Set the HB100 $1.2\ \text{m}$ from the array face at the height of the patch
row, facing the array. Lesson 21 put the far-field distance of this aperture at
$0.67\ \text{m}$, but level comparisons of under a decibel need more distance:
in the Module 3 dry run, scan loss read correctly at $1.2\ \text{m}$ and only
half of it at $1\ \text{m}$. Tape the walk's arc on the floor at the same
$1.2\ \text{m}$ radius, with marks at $-90^\circ$, $0^\circ$, and $+90^\circ$.
::::

::::{frame} Bring Up the Kit
:class: read-only

:::{present}
1. Browse to your kit's address from Lesson 17 and wait for the pill to read **Connected**.
2. With the HB100 $1.2\ \text{m}$ out at boresight and the kit at $0^\circ$, press **Find HB100** and record the Signal Freq in the packet.
3. Press **Calibrate** and wait for it to finish.
4. Open the **Lab Presets** section, then press **2 Array Factor**.
5. Set **Rx Gain (dB)** for an FFT peak of $-10 \pm 3$ dBFS, and record it. Leave it there for the whole lab.
6. Turn on **Show Peak Angle Marker** under **Plot Options**, press **Start**, and open the **Rectangular** tab.
:::

This is Lesson 17's order, for the same reason: **Calibrate** reads the
frequency that **Find HB100** stores, and it needs the source at boresight while
it runs. The preset buttons respond only once the Lab Presets section is open.
The Rx Gain setting is the L17 Lab's level reference: every level in the packet
is a difference between two readings taken at that gain, and the difference
holds only while the receiver stays linear. A main lobe with a flat top means
the receiver has clipped; turn the gain down and start again.
::::

::::{frame} Run 1: Check the Angle Axis
:class: read-only

:::{present}
7. With the beam sweeping, turn the kit to $+30^\circ$ on the protractor and record the **Angle** readout, set to **Peak**, in Table A.
8. Repeat at $-30^\circ$ and at $0^\circ$.
9. At $0^\circ$, record the peak, the half-power beamwidth, and both first sidelobes in Table B.
:::

If the Angle readout reads near $-30^\circ$ when the protractor reads $+30^\circ$, the
kit is turning the wrong way, or the protractor is labeled backward; fix the
labels before going on, because every angle in Tables D and E depends on them. A
reading within $\pm 2^\circ$ of the protractor confirms the sign and the
centering. Table B is the array factor, the trace you measured in the L20 Lab,
and the reference for the other three runs.
::::

::::{frame} Run 2: Walk It by Hand
:class: read-only

:::{present}
10. Open **Lab Presets**, press **7 Antenna Pattern**, and set **Steer Angle (deg)** to $0$.
11. Lift the HB100 off its tripod and stand on the $-90^\circ$ mark, aimed at the array.
12. Walk the arc to $+90^\circ$ in about $10\ \text{s}$, keeping the radius and the aim.
13. Read the main-lobe peak and both first sidelobes off the trace and record them in Table C.
14. Repeat twice more, then return the HB100 to its tripod at boresight.
:::

Preset 7 sets **Mode**, in the Beam Steering section, to **Signal vs Time**: the
beam holds at the Steer Angle, which takes effect as you change it, with no
Apply, and the Tracking tab plots the peak level in dBFS against time over the
last $30\ \text{s}$. The plot's title shows the held angle and the update rate;
check that it reads "Beam held at 0.0°" before you walk. Practice the walk once before you record: too fast and the pattern crowds
into one part of the plot, too slow and it runs off the edge. Read each lobe's
peak by hovering over the trace. The three walks will not agree exactly, and
that disagreement is a measurement in its own right: Part 3 compares it with the
rotation's.
::::

::::{frame} Run 3: Turn the Kit, Beam at 0°
:class: read-only

:::{present}
15. Kit at $0^\circ$, beam held at $0^\circ$: record **Peak Gain** as the reference.
16. Turn the kit to each $10^\circ$ mark from $-90^\circ$ to $+90^\circ$ and record the level relative to the reference in Table D.
17. Turn slowly through the main lobe, each first null, and each first sidelobe, and record the angle and level of each extreme.
:::

Turn the kit by its base, not by the board, so the array stays centered over
the protractor, and keep the cables slack enough to follow it. The $10^\circ$
marks sketch the pattern; they cannot give the sidelobe levels, because a
sidelobe peaks between marks and the marks at $\pm 30^\circ$ and $\pm 50^\circ$
sit almost on nulls. Turning slowly through a lobe while you watch the level and
recording its highest reading is how an antenna range finds a lobe peak. Where
the level stops changing as you turn, write "floor".
::::

::::{frame} Run 4: Turn the Kit, Beam at 30°
:class: read-only

:::{present}
18. Set **Steer Angle (deg)** to $30$, kit back at $0^\circ$, and check the plot title reads "Beam held at 30.0°".
19. Repeat Steps 16 and 17 for Table E, with each level relative to Step 15's reference.
20. Turn the kit to $180^\circ$, source behind the board, and record that level.
21. Set **Steer Angle (deg)** back to $0$ and the kit to $0^\circ$ before you leave.
:::

Referring Table E to Run 3's reference makes the scan loss read directly: the
main lobe's level is the drop in peak gain. Take the main-lobe peak twice, a few
minutes apart, if you have time; a drop that repeats is a measurement, and one
that does not is a reflection. At $180^\circ$ the patches face away from the
source and the ground plane sits between them.
::::

::::{frame} Worked Example: Reading dBc off a Trace
:class: read-only

:::{admonition} Worked example — reading dBc off a trace
:class: tip
A beam-held trace gives peak readings of $-18.4$ dBFS for the main lobe,
$-31.2$ dBFS for the left first sidelobe, and $-29.9$ dBFS for the right first
sidelobe. The full-scale reference cancels when you take the ratio, so subtract:

$$
\begin{aligned}
L_\text{left} &= -31.2 + 18.4 \\
&= -12.8\ \text{dBc} \\
L_\text{right} &= -29.9 + 18.4 \\
&= -11.5\ \text{dBc}
\end{aligned}
$$

Both straddle the $-13.1$ dBc expected at broadside, and the $1.3\ \text{dB}$
spread between them is about what a classroom's reflections produce. A pair
reading $-6$ and $-7$ dBc would not be a uniform illumination, and would send
you back to Calibrate and to the element gain sliders.
:::
::::

::::{frame} Classroom Against Chamber
:::{present}
- **Angle:** the rotation reads it; a range encodes it.
- **Distance:** the rotation fixes it.
- **Reflections:** $\pm 1$ dB in a room; a chamber absorbs them.
- **Far field:** set by the room's size, chamber or not.
:::
:::{present}
<img src="../../viz/img/L21-range-artifacts.svg"
     alt="A classroom measurement with floor and ceiling reflections beside an anechoic chamber measurement with absorber-lined walls, a turntable, and a single direct path."
     style="max-width: 560px; width: 100%; display: block; margin: 0 auto;">
:::

The rotation is a paper version of an antenna range, and comparing the two
shows what the classroom still leaves in your data.

**Angle.** A range turns the antenna on a turntable with a shaft encoder, so
every sample carries its angle to a fraction of a degree. Your protractor reads
to about a degree, which the walk's time axis cannot.

**Distance.** A range bolts the source at a fixed distance. So does the
rotation; the walk does not.

**Reflections.** The direct path is not the only path from the HB100 to the
array. Reflections off the floor, the ceiling, and the whiteboard arrive too and
add to the direct signal in and out of phase, which is the $\pm 1\ \text{dB}$ of
ripple in both of your methods. An anechoic chamber lines every surface with
absorber so only the direct path survives.

**Far field.** You set $1.2\ \text{m}$ against Lesson 21's $0.67\ \text{m}$. A
chamber satisfies the far-field condition only if it is long enough for the
antenna and frequency; a large antenna in a short chamber has the same problem
as a large antenna in a classroom.
::::

::::{frame} No Hardware?
:class: read-only

```{note}
The walk and the rotation have no simulated version: the simulator's source is
fixed at boresight and cannot be moved, and turning a simulated kit changes
nothing. Run the electrical sweep of Table B in the hosted simulator at
[livethisdream.github.io/phaser](https://livethisdream.github.io/phaser/), and
use the walk widget above to see what a walked trace looks like.
```
::::

::::{frame} Lab Packet
:class: read-only doc-links

The L21 Lab packet is one submission for the whole lab, turned in complete before Lesson 22. It has three parts:

1. **Part 1, Pre-Lab** (individual, before the lab period, because you need it at the bench): the patterns to expect with the beam at $0^\circ$ and $30^\circ$, the error budgets of the walk and the rotation, and reading dBc off a trace.
2. **Part 2, Measurements** (your own kit's data, recorded in class): the angle check, the electrical sweep, three walks, and two rotations.
3. **Part 3, Writeup** (individual, after the lab): which model the data support, the walk against the rotation, and a far-field problem.

- <a class="doc-link" href="../../labs/ECE444_Lab_L21_Pattern_blank.pdf" target="_blank" rel="noopener">L21 Lab packet (PDF)</a>
::::

::::{frame} Summary: The Pattern on the Bench
:class: read-only

| Idea | What it is | Number to remember |
| :-- | :-- | :-- |
| Beam sweep | beam swept past a fixed source | the array factor; x-axis is steer angle |
| Hand walk | source carried around a held beam | x-axis is time; $\pm 0.7$ dB from a $10\ \text{cm}$ radius drift |
| Rotation | kit turned in front of a fixed source | real angles, fixed distance; $\pm 1^\circ$ |
| Scan loss | element pattern at the steer angle | $-0.6$ dB ideal, $-0.9$ dB patch, at $30^\circ$ |
| Sidelobe asymmetry | element pattern lowers the outer lobe | $-12.2$ vs $-15.1$ dBc at $30^\circ$ |
| Source distance | far field and level accuracy | $0.67\ \text{m}$ far field; measure at $1.2\ \text{m}$ |
| Room reflections | direct path plus copies | $\pm 1$ dB a reading, $\pm 2$ dB on a dBc value |
::::

::::{frame} Looking Ahead
:::{present}
- Uniform illumination fixed the first sidelobes near $-13$ dBc today.
- Lesson 22 makes that number a design choice: taper the Element Gains.
- Lower sidelobes widen the beam and lower the peak gain.
:::

You now have a measured $-13$ dBc in your packet, and so far it has been a fact
about uniform illumination rather than a choice. Lesson 22 turns it into a
design variable. Feeding the eight elements unequally, with more power in the
middle and less at the edges, pushes the sidelobes down, and the Element Gains
sliders you have been leaving at 100% are how you do it on this hardware.

A taper that lowers the first sidelobes by $10\ \text{dB}$ widens the main lobe
and lowers the peak gain, and Lesson 22 derives exactly how much of each. Before
the next period, look back at your broadside rotation and decide how much
beamwidth you would give up to put those first sidelobes at $-25$ dBc, then
check your guess against the numbers.
::::
