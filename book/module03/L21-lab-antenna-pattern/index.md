---
frame_view: true
---

# L21 Lab — Antenna Pattern

::::{frame}
:class: title-frame

<div class="course-mark">ECE 444 · Fall 2026</div>

<h1 class="frame-title">Antenna Pattern</h1>

<div class="title-rule"></div>

Hold the beam still and move the HB100 around it, by hand and on the stand, then compare with the beam sweep.

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
- Part 1, before today: what each trace should show, and what counts as agreement.
- Part 2, today: the beam sweep, an azimuth sweep by hand, and one on the stand.
- Part 3, after: compare the lobe levels, method against method.
:::

Lesson 21 compared the kit's Rectangular plot, built by stepping the beam past
a fixed source, with the antenna-range method, which holds one beam still and
moves the source in azimuth. Today you take all three traces on your own kit.
Part 1 of the L21 Lab packet, the pre-lab you completed before class, works out
what each trace should show at your HB100's frequency and how closely two
traces must agree. Part 3, on your own before Lesson 22, compares the methods
lobe by lobe.
::::

::::{frame} Three Ways to Trace a Pattern
:::{present}
| | Beam sweep | Azimuth sweep, by hand | Azimuth sweep, on the stand |
| :-- | :-- | :-- | :-- |
| x-axis | steer angle | elapsed time | stand angle |
| Measures | array factor | element $\times$ array | element $\times$ array |
| Distance | fixed | your arm | fixed |
:::
:::{present}
<img src="../../viz/img/L21-three-methods.svg"
     alt="Three ways to trace a pattern. Beam sweep: the HB100 stays put and the kit steps the beam past it. By hand: the beam is held and you carry the HB100 around an arc. On the stand: the beam is held, the HB100 stays on its tripod, and the kit turns on its stand."
     style="max-width: 560px; width: 100%; display: block; margin: 0 auto;">
:::

The three methods differ in what moves.

The **beam sweep** is the one you have used since the L18 Lab: the HB100 stays
put and the kit steps the beam past it, recording the received level at each
steer angle. The HB100 sits at one physical angle, so each patch's own pattern
contributes the same constant to every point and drops out of the trace's
shape. The trace is the array factor, plotted against the angle the kit
steered to.

The **azimuth sweep by hand** holds the beam fixed while you carry the HB100
around the array on an arc. The physical angle changes at every instant, so
the trace also carries each patch's own pattern: it is the antenna pattern of
one beam. The kit plots it against elapsed time, which maps to azimuth at a
steady pace, and the level stays steady only while you hold the radius.

The **azimuth sweep on the stand** holds the beam fixed, leaves the HB100 on
its tripod, and turns the kit in front of it. The trace is the antenna pattern
again, but every reading carries an angle you read off the stand's scale, and
the distance to the source never changes.
::::

::::{frame} Bring Your Predictions
:::{present}
- Do the three traces agree on the broadside first sidelobes?
- At $30^\circ$, which first sidelobe reads lower on the azimuth sweep, and by how much?
- What does the trace read with the HB100 behind the board?
:::

Part 1 answers these at your kit's frequency (Questions 3 and 4). Bring the
answers to class, so you can tell a good trace from a bad one while you
can still repeat it. The lesson's figures use $10.3\ \text{GHz}$, so their
angles differ from yours by a few tenths of a degree; the nominal
$10.525\ \text{GHz}$ is close enough if you did not record your HB100's
frequency.
::::

::::{frame} Azimuth Sweep Simulator
:class: viz-frame

:::{depth}
The widget below runs the azimuth sweep in simulation. Choose a steer angle
and a speed profile, then watch the trace paint as the source moves around the
arc. Run it once with the uniform profile and once with the hand-like profile,
and compare the two readouts: the lobe spacing changes and the lobe levels do
not. The simulation holds the radius fixed; a hand-carried source drifts by a
few centimeters, which moves the level.
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
- At a steady pace, time maps to azimuth; an uneven pace stretches the lobes in time.
- Pace does not change a lobe's level. A drift in the radius does, as $1/r^2$.
:::
:::{present}
<img src="../../viz/img/L21-time-axis.svg"
     alt="One 22 second azimuth sweep by hand plotted twice: against time, where an uneven pace spaces the lobes unevenly, and against source angle, where they are symmetric. A dashed line at the first-sidelobe level touches the same lobes on both."
     style="max-width: 560px; width: 100%; display: block; margin: 0 auto;">
:::

The level the kit records at any instant is the pattern in the direction of
the HB100 at that instant, and it does not depend on how fast the HB100 was
moving. Moving slowly through a lobe draws it wider on the plot without
changing its level, as long as the lobe gets several updates; the plot's title
shows the update rate, and Part 1 (Question 5) gives the slowest rate your
sweep can use. A drift in the radius does change the level, because received
power falls as $1/r^2$; Part 1 (Question 6) sizes it. Three sweeps by hand,
compared in Part 3, show how large that scatter is in practice.
::::

::::{frame} Turning the Kit on Its Stand
:::{present}
- The HB100 stays on its tripod, $1.2\ \text{m}$ out; the stand turns the kit about the array's center.
- Facing the patches, E1 is on the right. Turning the face toward E1 puts the source at $+\theta$.
- The stand's scale reads $-\theta$.
:::
:::{present}
<img src="../../viz/img/L21-rotation-setup.svg"
     alt="Top view of the stand setup: the HB100 fixed 1.2 m from the array, and the kit turned 30 degrees about the array center on its stand, its face toward E1, which puts the source at plus 30 degrees on the E8 side while the pointer, which turns with the kit, reads minus 30 on the scale on the fixed base"
     style="max-width: 560px; width: 100%; display: block; margin: 0 auto;">
:::

Turning the kit in front of a fixed source records the same pattern as
carrying the source around a fixed kit, because only the angle between the
array normal and the source matters. The setup changes in three ways: the
distance stays fixed, so you can compare levels from one reading to the next;
the HB100 stays aimed at the array without effort; and you take each reading
at an angle you read off the stand's scale, with a click every $5^\circ$.

A stand reading of $-30$ means the source is at $+30^\circ$. Lesson 18 put
$+\theta$ on the E8 end of the array, and turning the kit's face toward E1, as
seen from the source, puts the source on that side. The scale sits on
the fixed base and counts clockwise as seen from above, while that turn is
counterclockwise, so the pointer reads the opposite sign. Part 2 starts by
confirming the sign with a beam sweep, whose **Angle** readout, set to
**Peak**, reads the source's angle.

The stand puts the array's center on its turning axis, so the distance stays
fixed as you turn; Part 1 (Question 6) shows how far an off-center axis would
move the readings. The scale reads to about $\pm 2^\circ$, which is fine for a lobe about
$15^\circ$ wide.
::::

::::{frame} The Steered Pattern
:::{present}
- With the beam held at $30^\circ$, the main lobe appears near $30^\circ$ and is wider on its outside.
- Compare its two first sidelobes with your Part 1 prediction and with your own broadside pair.
:::

With the beam held at $30^\circ$, the main lobe appears when the source reaches
about $30^\circ$ instead of boresight. The array factor slides in $\sin\theta$,
not in $\theta$ (Lesson 18), so the lobe reaches farther on its outside than on
its inside. Lesson 21 explains why the azimuth sweep's two first sidelobes
need not match at $30^\circ$. Before you credit a difference to the patches,
compare it with the difference between your own two broadside first
sidelobes, which the room alone produces.
::::

::::{frame} Two Error Budgets
:::{present}
| Error | By hand | On the stand |
| :-- | :-- | :-- |
| Angle axis | time, at your pace | the stand's scale |
| Distance | your arm | fixed |
| Room reflections | yes | yes |
:::

Part 1 (Question 6) sizes each error and the window two traces must agree
within. By hand, the angle comes from converting time to angle at a steady
pace you did not quite hold, and the level moves as your radius drifts. On the
stand, both of those go away, and what remains is the stand's scale and how
well the array's center sits on the turning axis. Neither method removes the
room: reflections off the floor, the walls, and the people nearby add to the
direct path in both. The stand's advantage there is repeatability. The
reflections sit in fixed places in the room, so a reading you repeat at the
same angle comes back to the same value.
::::

::::{frame} Equipment and Setup
:::{present}
- The kit on its stand, cabled to your laptop, $0^\circ$ toward the HB100.
- The HB100 on its tripod at patch-row height, $1.2\ \text{m}$ out, and a taped $1.2\ \text{m}$ arc.
- The arc's $-90^\circ$ end is on the E1 side; start there.
:::
:::{present}
<img src="../../viz/img/L21-lab-layout.svg"
     alt="The setup seen from above: the kit on its stand at the center, its patches toward the HB100, E1 on the left and E8 on the right; the HB100 on its tripod 1.2 m out at 0 degrees; a taped 1.2 m arc from minus 90 degrees on the E1 side, where the sweep by hand starts, to plus 90 degrees on the E8 side; the laptop behind the kit."
     style="max-width: 420px; width: 100%; display: block; margin: 0 auto;">
:::

You need the ADALM-PHASER kit on its stand from
<a href="../L17-lab-bring-up/index.html#frame-the-rotating-stand">the L17 Lab</a>,
connected to your laptop by the Ethernet cable as in Lesson 17; the HB100 with a
fresh battery, on its tripod; and masking tape. Tape the stand's base to the
table with its $0^\circ$ mark toward the HB100, and seat the kit's tripod in
the platter's grooves with the patches facing the pointer. A kit without a
stand can use a printed protractor instead, centered under the middle of the
array between E4 and E5 with $0^\circ$ toward the HB100. Number it as the
stand does, clockwise as seen from above, so that the sign rule of
Run 1 holds, and turn the tripod carefully about that center.

Set the HB100 $1.2\ \text{m}$ from the array face at the height of the patch
row, facing the array: past the far-field distance you found in Part 1, even
with a hand-carried source drifting in and out. Tape the arc on the floor at
the same $1.2\ \text{m}$ radius, with marks at $-90^\circ$, $0^\circ$, and
$+90^\circ$. The $-90^\circ$ end is on the E1 side of the array, the right end
of the row as you face the patches.
::::

::::{frame} Bring Up the Kit
:class: read-only

1. **Connect.** Browse to your kit's address from Lesson 17 and wait for the
   pill to read **Connected**.
2. **Find the source.** With the HB100 $1.2\ \text{m}$ out at boresight and
   the kit at $0^\circ$, press **Find HB100** and record the Signal Freq and
   the source distance.

   <div class="rec" data-lab="L21">
   <label>Step 2: Signal Freq <input data-field="f.sig" data-label="Step 2: Signal Freq"></label>
   <label>Step 2: source distance <input data-field="f.dist" data-label="Step 2: source distance"></label>
   </div>
3. **Calibrate.** Press **Calibrate** and wait for it to finish, with the
   HB100 still at boresight. Calibrate reads the frequency that Find HB100
   stores, so it runs second, as in Lesson 17.
4. **Load the preset.** Open the **Lab Presets** section and choose the
   **Array Factor** preset. Its buttons respond only while the section is
   open, and a preset does not start the kit.
5. **Set the gain.** Press **Start**, open the **FFT** tab, and set **Rx Gain
   (dB)** for a peak of $-10 \pm 3$ dBFS. Record it, and leave it there for the
   whole lab: every level in the packet is a difference between two readings
   at this gain, and the difference holds only while the receiver stays
   linear. A main lobe with a flat top means the receiver has clipped; turn
   the gain down and start again.

   <div class="rec" data-lab="L21">
   <label>Step 5: Rx Gain (dB) <input data-field="f.gain" data-label="Step 5: Rx Gain (dB)"></label>
   </div>
6. **Watch the beam sweep.** Turn on **Show Peak Angle Marker** under **Plot
   Options**, and open the **Rectangular** tab.
::::

::::{frame} Run 1: Check the Angle Axis
:class: read-only

7. **Source at $+30^\circ$.** With the beam sweeping, turn the kit until the
   stand reads $-30$, which puts the source at $+30^\circ$, and record the
   **Angle** readout, set to **Peak**. If it reads near $-30^\circ$, the kit
   is turning the wrong way or the patches face away from the pointer; fix
   that before going on, because every angle in Tables D and E depends on it.
8. **Source at $-30^\circ$ and at $0^\circ$.** Repeat with the stand at $+30$
   (source at $-30^\circ$) and at $0$. A reading within $\pm 2^\circ$ of the
   source angle confirms the sign and the centering.

   <div class="rec" data-lab="L21">
   <label>Source at +30°: Angle <input data-field="a.p30" data-label="Step 7, source at +30° (stand −30): Angle"></label>
   <label>Source at −30°: Angle <input data-field="a.m30" data-label="Step 8, source at −30° (stand +30): Angle"></label>
   <label>Source at 0°: Angle <input data-field="a.0" data-label="Step 8, source at 0°: Angle"></label>
   </div>
9. **The beam sweep.** At $0^\circ$, record the peak, the half-power
   beamwidth, and both first sidelobes. This is the trace you measured in the
   L20 Lab, and the reference for the other two runs.

   <div class="rec" data-lab="L21">
   <label>Step 9: peak (dBFS) <input data-field="b.peak" data-label="Step 9: peak (dBFS)"></label>
   <label>Step 9: half-power beamwidth <input data-field="b.hpbw" data-label="Step 9: half-power beamwidth"></label>
   <label>Step 9: left first sidelobe (dBc) <input data-field="b.left" data-label="Step 9: left first sidelobe (dBc)"></label>
   <label>Step 9: right first sidelobe (dBc) <input data-field="b.right" data-label="Step 9: right first sidelobe (dBc)"></label>
   </div>
::::

::::{frame} Run 2: Azimuth Sweep by Hand
:class: read-only

10. **Load the preset.** Open **Lab Presets** and choose the **Antenna
    Pattern** preset. It sets **Mode**, in the Beam Steering section, to
    **Signal vs Time**: the beam holds at the Steer Angle, which takes effect
    as you change it, with no Apply, and the **Tracking** tab plots the peak
    level in dBFS against time over the last $30\ \text{s}$.
11. **Hold the beam at broadside.** Set **Steer Angle (deg)** to $0$. Check
    that the plot title reads "Beam held at 0.0°", and record the updates/s it
    shows. If it is below the minimum you found in Part 1, plan a slower sweep.

    <div class="rec" data-lab="L21">
    <label>Step 11: updates per second <input data-field="f.rate" data-label="Step 11: updates per second"></label>
    </div>
12. **Pick up the source.** Press **Stop**. Lift the HB100 off its tripod and
    hold it over the $-90^\circ$ mark, on the E1 side, aimed at the array.
13. **Sweep.** Press **Start**, which clears the trace and begins at $t = 0$,
    then carry the HB100 along the arc to $+90^\circ$ in about 20 to
    $25\ \text{s}$, keeping the radius and the aim. Practice the arc once
    before you record: too fast and each lobe gets only a few updates, too
    slow and the pattern runs off the edge.
14. **Read the trace.** Press **Stop** at $+90^\circ$; the window scrolls while
    the kit runs, and Stop freezes it. Hover over each lobe's peak to read the
    main-lobe peak in dBFS and both first sidelobes, and convert the sidelobes
    to dBc by subtracting the main-lobe peak. Expect the room to make the two
    first sidelobes unequal by a few decibels, so record both.
15. **Repeat.** Sweep twice more, pressing **Start** at $-90^\circ$ each time,
    then return the HB100 to its tripod at boresight. The three sweeps will not
    agree exactly: record the spread, largest minus smallest, and Part 3
    compares it with the stand's.

    <div class="rec" data-lab="L21">
    <label>Sweep 1: time (s) <input data-field="c.w1.time" data-label="Step 15, sweep 1: time (s)"></label>
    <label>Sweep 1: peak (dBFS) <input data-field="c.w1.peak" data-label="Step 15, sweep 1: peak (dBFS)"></label>
    <label>Sweep 1: left first sidelobe (dBc) <input data-field="c.w1.left" data-label="Step 15, sweep 1: left first sidelobe (dBc)"></label>
    <label>Sweep 1: right first sidelobe (dBc) <input data-field="c.w1.right" data-label="Step 15, sweep 1: right first sidelobe (dBc)"></label>
    <label>Sweep 2: time (s) <input data-field="c.w2.time" data-label="Step 15, sweep 2: time (s)"></label>
    <label>Sweep 2: peak (dBFS) <input data-field="c.w2.peak" data-label="Step 15, sweep 2: peak (dBFS)"></label>
    <label>Sweep 2: left first sidelobe (dBc) <input data-field="c.w2.left" data-label="Step 15, sweep 2: left first sidelobe (dBc)"></label>
    <label>Sweep 2: right first sidelobe (dBc) <input data-field="c.w2.right" data-label="Step 15, sweep 2: right first sidelobe (dBc)"></label>
    <label>Sweep 3: time (s) <input data-field="c.w3.time" data-label="Step 15, sweep 3: time (s)"></label>
    <label>Sweep 3: peak (dBFS) <input data-field="c.w3.peak" data-label="Step 15, sweep 3: peak (dBFS)"></label>
    <label>Sweep 3: left first sidelobe (dBc) <input data-field="c.w3.left" data-label="Step 15, sweep 3: left first sidelobe (dBc)"></label>
    <label>Sweep 3: right first sidelobe (dBc) <input data-field="c.w3.right" data-label="Step 15, sweep 3: right first sidelobe (dBc)"></label>
    <label>Spread: peak (dB) <input data-field="c.spread.peak" data-label="Step 15, spread of the three sweeps: peak (dB)"></label>
    <label>Spread: left sidelobe (dB) <input data-field="c.spread.left" data-label="Step 15, spread of the three sweeps: left sidelobe (dB)"></label>
    <label>Spread: right sidelobe (dB) <input data-field="c.spread.right" data-label="Step 15, spread of the three sweeps: right sidelobe (dB)"></label>
    </div>

<img src="../../viz/img/L21-tracking-tab.svg"
     alt="The Signal vs Time plot on the Tracking tab: the title reads Beam held at 0.0 degrees and the update rate; the trace of one 22 second sweep by hand sits in a 30 second window of level in dBFS against time; hovering over a lobe peak reads its level."
     style="max-width: 560px; width: 100%; display: block; margin: 1em auto;">
::::

::::{frame} Run 3: Turn the Kit, Both Beams in One Pass
:class: read-only

16. **Sweep the beam again.** Choose the **Array Factor** preset and press
    **Start**, so the beam sweeps again on the Rectangular tab, kit at
    $0^\circ$. Hover over the trace at $0^\circ$ steer and record that level as
    the reference; every level in Tables D and E is relative to it.

    <div class="rec" data-lab="L21">
    <label>Step 16: reference level (dBFS) <input data-field="d.ref" data-label="Step 16: reference level, kit at 0°, trace at 0° steer (dBFS)"></label>
    </div>
17. **Turn through the marks.** Turn the kit to each $10^\circ$ mark from
    $-90^\circ$ to $+90^\circ$, every second click of the stand. At each,
    record the trace at $0^\circ$ steer (Table D) and at the sample nearest
    $30^\circ$ (Table E), both relative to Step 16, at the source angle: the
    stand reading with its sign flipped, as in Table A. Each point of a beam
    sweep is the beam held at that steer angle for an instant, so one sweep
    reads both held beams at once. Turn the kit by the platter, not by the
    board, so the tripod stays seated in its grooves and the array on the axis,
    and keep the cables slack enough to follow it.

    <div class="rec" data-lab="L21">
    <label>Source at −90°: beam at 0° <input data-field="d.m90.level" data-label="Step 17, source at −90°: level, beam at 0° (Table D)"></label>
    <label>beam at 30° <input data-field="e.m90.level" data-label="Step 17, source at −90°: level, beam at 30° (Table E)"></label>
    <label>Source at −80°: beam at 0° <input data-field="d.m80.level" data-label="Step 17, source at −80°: level, beam at 0° (Table D)"></label>
    <label>beam at 30° <input data-field="e.m80.level" data-label="Step 17, source at −80°: level, beam at 30° (Table E)"></label>
    <label>Source at −70°: beam at 0° <input data-field="d.m70.level" data-label="Step 17, source at −70°: level, beam at 0° (Table D)"></label>
    <label>beam at 30° <input data-field="e.m70.level" data-label="Step 17, source at −70°: level, beam at 30° (Table E)"></label>
    <label>Source at −60°: beam at 0° <input data-field="d.m60.level" data-label="Step 17, source at −60°: level, beam at 0° (Table D)"></label>
    <label>beam at 30° <input data-field="e.m60.level" data-label="Step 17, source at −60°: level, beam at 30° (Table E)"></label>
    <label>Source at −50°: beam at 0° <input data-field="d.m50.level" data-label="Step 17, source at −50°: level, beam at 0° (Table D)"></label>
    <label>beam at 30° <input data-field="e.m50.level" data-label="Step 17, source at −50°: level, beam at 30° (Table E)"></label>
    <label>Source at −40°: beam at 0° <input data-field="d.m40.level" data-label="Step 17, source at −40°: level, beam at 0° (Table D)"></label>
    <label>beam at 30° <input data-field="e.m40.level" data-label="Step 17, source at −40°: level, beam at 30° (Table E)"></label>
    <label>Source at −30°: beam at 0° <input data-field="d.m30.level" data-label="Step 17, source at −30°: level, beam at 0° (Table D)"></label>
    <label>beam at 30° <input data-field="e.m30.level" data-label="Step 17, source at −30°: level, beam at 30° (Table E)"></label>
    <label>Source at −20°: beam at 0° <input data-field="d.m20.level" data-label="Step 17, source at −20°: level, beam at 0° (Table D)"></label>
    <label>beam at 30° <input data-field="e.m20.level" data-label="Step 17, source at −20°: level, beam at 30° (Table E)"></label>
    <label>Source at −10°: beam at 0° <input data-field="d.m10.level" data-label="Step 17, source at −10°: level, beam at 0° (Table D)"></label>
    <label>beam at 30° <input data-field="e.m10.level" data-label="Step 17, source at −10°: level, beam at 30° (Table E)"></label>
    <label>Source at 0°: beam at 0° <input data-field="d.0.level" data-label="Step 17, source at 0°: level, beam at 0° (Table D)"></label>
    <label>beam at 30° <input data-field="e.0.level" data-label="Step 17, source at 0°: level, beam at 30° (Table E)"></label>
    <label>Source at +10°: beam at 0° <input data-field="d.p10.level" data-label="Step 17, source at +10°: level, beam at 0° (Table D)"></label>
    <label>beam at 30° <input data-field="e.p10.level" data-label="Step 17, source at +10°: level, beam at 30° (Table E)"></label>
    <label>Source at +20°: beam at 0° <input data-field="d.p20.level" data-label="Step 17, source at +20°: level, beam at 0° (Table D)"></label>
    <label>beam at 30° <input data-field="e.p20.level" data-label="Step 17, source at +20°: level, beam at 30° (Table E)"></label>
    <label>Source at +30°: beam at 0° <input data-field="d.p30.level" data-label="Step 17, source at +30°: level, beam at 0° (Table D)"></label>
    <label>beam at 30° <input data-field="e.p30.level" data-label="Step 17, source at +30°: level, beam at 30° (Table E)"></label>
    <label>Source at +40°: beam at 0° <input data-field="d.p40.level" data-label="Step 17, source at +40°: level, beam at 0° (Table D)"></label>
    <label>beam at 30° <input data-field="e.p40.level" data-label="Step 17, source at +40°: level, beam at 30° (Table E)"></label>
    <label>Source at +50°: beam at 0° <input data-field="d.p50.level" data-label="Step 17, source at +50°: level, beam at 0° (Table D)"></label>
    <label>beam at 30° <input data-field="e.p50.level" data-label="Step 17, source at +50°: level, beam at 30° (Table E)"></label>
    <label>Source at +60°: beam at 0° <input data-field="d.p60.level" data-label="Step 17, source at +60°: level, beam at 0° (Table D)"></label>
    <label>beam at 30° <input data-field="e.p60.level" data-label="Step 17, source at +60°: level, beam at 30° (Table E)"></label>
    <label>Source at +70°: beam at 0° <input data-field="d.p70.level" data-label="Step 17, source at +70°: level, beam at 0° (Table D)"></label>
    <label>beam at 30° <input data-field="e.p70.level" data-label="Step 17, source at +70°: level, beam at 30° (Table E)"></label>
    <label>Source at +80°: beam at 0° <input data-field="d.p80.level" data-label="Step 17, source at +80°: level, beam at 0° (Table D)"></label>
    <label>beam at 30° <input data-field="e.p80.level" data-label="Step 17, source at +80°: level, beam at 30° (Table E)"></label>
    <label>Source at +90°: beam at 0° <input data-field="d.p90.level" data-label="Step 17, source at +90°: level, beam at 0° (Table D)"></label>
    <label>beam at 30° <input data-field="e.p90.level" data-label="Step 17, source at +90°: level, beam at 30° (Table E)"></label>
    </div>
18. **Find each lobe and null.** The $10^\circ$ marks sketch the patterns but
    miss the sidelobe peaks, which fall between marks. Turn slowly through each
    lobe and null of both beams and record the source angle and level of each
    extreme, the highest reading for a lobe and the lowest for a null; an
    antenna range finds a lobe peak the same way. Where the level stops
    changing as you turn, it has reached the noise floor: write "floor".

    <div class="rec" data-lab="L21">
    <label>Beam at 0°, main lobe: angle <input data-field="d.main.angle" data-label="Step 18, Beam at 0°, main lobe: source angle"></label>
    <label>Beam at 0°, main lobe: level <input data-field="d.main.level" data-label="Step 18, Beam at 0°, main lobe: level"></label>
    <label>Beam at 0°, left first null: angle <input data-field="d.lnull.angle" data-label="Step 18, Beam at 0°, left first null: source angle"></label>
    <label>Beam at 0°, left first null: level <input data-field="d.lnull.level" data-label="Step 18, Beam at 0°, left first null: level"></label>
    <label>Beam at 0°, right first null: angle <input data-field="d.rnull.angle" data-label="Step 18, Beam at 0°, right first null: source angle"></label>
    <label>Beam at 0°, right first null: level <input data-field="d.rnull.level" data-label="Step 18, Beam at 0°, right first null: level"></label>
    <label>Beam at 0°, left first sidelobe: angle <input data-field="d.lsl.angle" data-label="Step 18, Beam at 0°, left first sidelobe: source angle"></label>
    <label>Beam at 0°, left first sidelobe: level <input data-field="d.lsl.level" data-label="Step 18, Beam at 0°, left first sidelobe: level"></label>
    <label>Beam at 0°, right first sidelobe: angle <input data-field="d.rsl.angle" data-label="Step 18, Beam at 0°, right first sidelobe: source angle"></label>
    <label>Beam at 0°, right first sidelobe: level <input data-field="d.rsl.level" data-label="Step 18, Beam at 0°, right first sidelobe: level"></label>
    <label>Beam at 30°, main lobe: angle <input data-field="e.main.angle" data-label="Step 18, Beam at 30°, main lobe: source angle"></label>
    <label>Beam at 30°, main lobe: level <input data-field="e.main.level" data-label="Step 18, Beam at 30°, main lobe: level"></label>
    <label>Beam at 30°, inner first null: angle <input data-field="e.inull.angle" data-label="Step 18, Beam at 30°, inner first null: source angle"></label>
    <label>Beam at 30°, inner first null: level <input data-field="e.inull.level" data-label="Step 18, Beam at 30°, inner first null: level"></label>
    <label>Beam at 30°, outer first null: angle <input data-field="e.onull.angle" data-label="Step 18, Beam at 30°, outer first null: source angle"></label>
    <label>Beam at 30°, outer first null: level <input data-field="e.onull.level" data-label="Step 18, Beam at 30°, outer first null: level"></label>
    <label>Beam at 30°, inner first sidelobe: angle <input data-field="e.isl.angle" data-label="Step 18, Beam at 30°, inner first sidelobe: source angle"></label>
    <label>Beam at 30°, inner first sidelobe: level <input data-field="e.isl.level" data-label="Step 18, Beam at 30°, inner first sidelobe: level"></label>
    <label>Beam at 30°, outer first sidelobe: angle <input data-field="e.osl.angle" data-label="Step 18, Beam at 30°, outer first sidelobe: source angle"></label>
    <label>Beam at 30°, outer first sidelobe: level <input data-field="e.osl.level" data-label="Step 18, Beam at 30°, outer first sidelobe: level"></label>
    </div>
19. **Behind the board.** Turn the kit to $180^\circ$, source behind the
    board, and record the trace nearest $30^\circ$.

    <div class="rec" data-lab="L21">
    <label>Step 19, kit at 180°: level <input data-field="e.180.level" data-label="Step 19, kit at 180°: level, beam at 30° (Table E)"></label>
    </div>
20. **Restore.** Turn the kit back to $0^\circ$ before you leave.

<img src="../../viz/img/L21-run3-reading.svg"
     alt="One beam sweep at one kit position, against steer angle, with an unnumbered level axis. The sample at 0 degrees steer goes in Table D and the sample nearest 30 degrees goes in Table E."
     style="max-width: 560px; width: 100%; display: block; margin: 1em auto;">
::::

::::{frame} Worked Example: Reading dBc off a Trace
:class: read-only

:::{admonition} Worked example — reading dBc off a trace
:class: tip
A beam-held trace gives peak readings of $-16.2$ dBFS for the main lobe,
$-29.6$ dBFS for the left first sidelobe, and $-28.0$ dBFS for the right first
sidelobe. The full-scale reference cancels when you take the ratio, so subtract:

$$
\begin{aligned}
L_\text{left} &= -29.6 + 16.2 \\
&= -13.4\ \text{dBc} \\
L_\text{right} &= -28.0 + 16.2 \\
&= -11.8\ \text{dBc}
\end{aligned}
$$

The $1.6\ \text{dB}$ difference between the two is the kind a classroom's
reflections produce. A pair reading $-6$ and $-7$ dBc would not be a uniform
illumination, and would send you back to Calibrate and to the element gain
sliders.
:::
::::

::::{frame} Classroom Against Chamber
:::{present}
- The stand reads angle to $\pm 2^\circ$; a range's encoder reads far finer.
- The stand and a range both fix the distance.
- A chamber absorbs reflections; a room adds them.
- Closer than the far-field distance, the nulls fill in.
:::
:::{present}
<img src="../../viz/img/L21-range-artifacts.svg"
     alt="Left, a classroom seen from the side: the direct path from the HB100 to the kit, plus reflections off the floor and a wall that add to it. Right, an anechoic chamber: absorber on every wall, a turntable under the antenna, and only the direct path."
     style="max-width: 560px; width: 100%; display: block; margin: 0 auto;">
:::

The azimuth sweep on the stand is the measurement an antenna range makes,
without the range's encoder or its absorber. Comparing the two shows what the
classroom still leaves in your data.

A range turns the antenna on a turntable with a shaft encoder, so
every sample carries its angle to a fraction of a degree. The stand's scale
gives each stop's angle to about $\pm 2^\circ$; the time axis of a sweep by
hand gives it only as well as you hold a steady pace.

A range bolts the source at a fixed distance. So does the stand;
a sweep by hand does not.

The direct path is not the only path from the HB100 to the
array. Reflections off the floor, the walls, and the whiteboard arrive too and
add to the direct signal in and out of phase, in both of your azimuth sweeps.
An anechoic chamber lines every surface with absorber so only the direct path
survives.

The far-field distance is set by the antenna's size and the
wavelength, not by the room. A chamber, like a classroom, works only if it is
long enough to reach that distance for the antenna and frequency being
measured.
::::

::::{frame} No Hardware?
:class: read-only

```{note}
The hosted simulator at
[livethisdream.github.io/phaser](https://livethisdream.github.io/phaser/) runs
the beam sweep of Table B and an azimuth sweep of the array factor alone. For
the azimuth sweep, choose the Antenna Pattern preset, turn on **Show HB100** under
**Plot Options**, open the **Polar** tab, and drag the HB100 from $-90^\circ$ to
$+90^\circ$; then open the **Tracking** tab to read the trace. The simulator has
no patch pattern, so its trace is the array factor, and it has no stand to turn.
```
::::

::::{frame} Your Part 2 Entries
:class: read-only

Every box you filled in on this page, in one place. Your entries stay in this
browser only, saved as you type. **Download my packet** writes them into Part 2
of the blank packet and saves the PDF; do Parts 1 and 3 on paper or in the PDF
viewer, and upload one PDF to Gradescope. If you have already typed Part 1 into
the packet PDF, use **Fill my own copy** and choose that file instead: your Part 1
is kept, and Part 2 is added to it. Either way the result is locked, so finish
any typing in the PDF first. **Export entries** saves a small backup file you
can **Import** on another laptop or after clearing your browser. The boxes are
optional: the blank packet is in the next frame, to fill on paper or in a PDF
viewer instead.

<div class="rec-summary" data-lab="L21" data-pdf="../../labs/ECE444_Lab_L21_Pattern_blank.pdf" data-file="ECE444_L21_Lab"></div>
::::

::::{frame} Lab Packet
:class: read-only doc-links

The L21 Lab packet is one submission for the whole lab, turned in complete before Lesson 22. It has three parts:

1. **Part 1, Pre-Lab** (individual, before the lab period, because you need it in class): what each trace should show with the beam at $0^\circ$ and $30^\circ$, how to pace the sweep by hand, reading dBc off a trace, and what counts as agreement.
2. **Part 2, Measurements** (your own kit's data, recorded in class): the angle check, the beam sweep, three azimuth sweeps by hand, and one pass on the stand.
3. **Part 3, Writeup** (individual, after the lab): where the methods agree on lobe levels, the sweep by hand against the pass on the stand, and a far-field problem.

- <a class="doc-link" href="../../labs/ECE444_Lab_L21_Pattern_blank.pdf" target="_blank" rel="noopener">L21 Lab packet (PDF)</a>
::::

::::{frame} Summary: The Pattern, Measured
:class: read-only

| Idea | What it is | Where it comes from |
| :-- | :-- | :-- |
| Beam sweep | beam stepped past a fixed source | the array factor; x-axis is steer angle |
| Azimuth sweep, by hand | HB100 carried around a held beam | x-axis is time; the level moves with your radius |
| Azimuth sweep, on the stand | kit turned in front of a fixed HB100 | physical angle from the scale, fixed distance |
| Sidelobes at $30^\circ$ | the patch pattern, seen only by the azimuth sweeps | Part 1, Question 4 |
| Pacing | updates per lobe on a sweep by hand | Part 1, Question 5 |
| Agreement window | room reflections on a dBc value | Part 1, Question 6 |
| Source distance | past the far-field distance | Part 1, Question 1 |
::::

::::{frame} Looking Ahead
:::{present}
- Uniform illumination set the first sidelobe level you measured today.
- Lesson 22 makes that level a design choice: taper the Element Gains.
- Lower sidelobes widen the beam and lower the peak gain.
:::

You now have a measured first-sidelobe level in your packet, and so far it has
been a fact about uniform illumination rather than a choice. Lesson 22 turns it
into a design variable. Feeding the eight elements unequally, with more power
in the middle and less at the edges, pushes the sidelobes down, and the Element
Gains sliders you have been leaving at 100% are how you do it on this hardware.

A taper that lowers the first sidelobes by $10\ \text{dB}$ widens the main lobe
and lowers the peak gain, and Lesson 22 derives how much of each. Before the
next period, look back at your broadside pass on the stand and decide how much
beamwidth you would give up to put those first sidelobes at $-25$ dBc, then
check your guess against the numbers.
::::
