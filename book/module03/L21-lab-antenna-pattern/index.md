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
- Part 2, today: move the source by hand, then turn the kit on its stand.
- Part 3, after: which model the data support, and which method resolves it.
:::

Lesson 21 separated the array factor from the pattern the array radiates and
predicted where the two part company: the peak drops as $\cos\theta_0$ when the
beam steers, the two first sidelobes of a steered beam stop matching, and
nothing comes out the back. Today we test those predictions. The
L21 Lab packet starts from them: Part 1, the pre-lab you completed before
class, works out the patterns at your HB100's frequency and sizes the errors of
the two methods. Today you measure the pattern twice with the beam held still,
once by carrying the source around the array by hand and once by turning the
kit in front of a fixed source. Part 3, on your own before Lesson 22,
reconciles the numbers with the predictions and compares the two methods.
::::

::::{frame} Three Ways to Trace a Pattern
:::{present}
| | Sweep the beam | Move the source | Turn the kit |
| :-- | :-- | :-- | :-- |
| x-axis | steer angle | elapsed time | stand angle |
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
leave it there, and sweep the beam electronically past it, recording
received power at each steer angle. The source sits at one physical angle, so
the element pattern contributes the same constant to every point on the trace
and drops out of its shape. The trace is the array factor, plotted against the
angle the beamformer was commanded to.

The second is the one ADI's workshop uses. Hold the beam fixed and carry the
source around the array on an arc. Now the physical angle changes at every
instant, so the element pattern multiplies the array factor exactly as Lesson 21
described, and the trace is the antenna pattern. The GUI plots it against
elapsed time, though, so the angle axis is only as good as your pace, and
the level is only as steady as your arm.

The third is what an antenna range does. Hold the beam fixed, leave the source
on its tripod, and turn the kit in front of it. The trace is the antenna
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
| Behind the board | floor, $-25$ to $-30$ dBc | floor |
:::

Part 1 of the packet works these out at your own kit's frequency; the dBc values
barely move with frequency, and the angles move by about $0.15^\circ$ per
$100\ \text{MHz}$, less than you can read off the stand's scale. With the beam at
$0^\circ$ the element pattern lowers the $\pm 21.4^\circ$ sidelobes by only
$0.3\ \text{dB}$, too little to see in a room. With the beam at $30^\circ$ it
lowers the peak by $0.6\ \text{dB}$ and the outer sidelobe, near $59^\circ$, by
$2.9\ \text{dB}$, while the inner one, near $8^\circ$, sits where the element is
flat. The array factor alone would put both at $-12.8$ dBc. The ground plane
removes the back hemisphere, so the reading with the source behind the board
should sit at the floor.
::::

::::{frame} The Trace Paints as You Move
:class: viz-frame

:::{depth}
The widget below runs the move in simulation. Choose a steer angle and a
speed profile, then watch the trace paint as the source moves around the
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
        title="Simulated pattern measurement with a hand-moved source: the source moves along an arc around a fixed beam while the level-versus-time trace paints below">
</iframe>
:::
::::

::::{frame} Amplitudes Survive, Angles Do Not
:::{present}
- With a moved source, the x-axis is time: an uneven pace moves and stretches the lobes.
- Pace cannot change a lobe's height, but a $10\ \text{cm}$ radius drift moves it $0.7\ \text{dB}$.
:::
:::{present}
<img src="../../viz/img/L21-time-vs-angle.svg"
     alt="The same measured run plotted twice: against elapsed time, where the lobes are unevenly spaced, and against true source angle, where they are symmetric. The lobe amplitudes are identical on both."
     style="max-width: 560px; width: 100%; display: block; margin: 0 auto;">
:::

The level the GUI records at any instant is the pattern at the angle the source
occupied at that instant, and it does not depend on how fast the source was
moving. Moving slowly through a lobe draws it wider on the plot without
changing its height, so the lobe levels survive an uneven pace and the angles do
not. The level is not immune to your arm, though: received power goes as
$1/r^2$, so drifting $10\ \text{cm}$ in or out at $1.2\ \text{m}$ moves the
reading by $0.7$ to $0.8\ \text{dB}$, more than the scan loss you want to see.
Three moves, compared in the packet, show how large that scatter is in practice.
::::

::::{frame} Turning the Kit on Its Stand
:::{present}
- The HB100 stays on its tripod, $1.2\ \text{m}$ out; the stand turns the kit about the array's center.
- Facing the patches, E1 is on the right. Turning the face toward E1 puts the source at $+\theta$.
- The stand's scale reads $-\theta$.
:::
:::{present}
<img src="../../viz/img/L21-rotation-setup.svg"
     alt="Top view of the rotation setup: the HB100 fixed 1.2 m from the array, and the kit turned 30 degrees about the array center on its rotating stand, its face toward E1, which puts the source at plus 30 degrees on the E8 side while the pointer on the stand scale reads minus 30"
     style="max-width: 560px; width: 100%; display: block; margin: 0 auto;">
:::

Turning the kit in front of a fixed source records the same pattern as moving
the source around a fixed kit, because only the angle between the array normal
and the source matters. What changes is everything else. The distance never
changes, so the levels can be compared from one reading to the next; the HB100
stays aimed at the array without effort; and each reading is taken at an angle
you can read off the stand's scale, with a click every $5^\circ$.

Lesson 18 put $+\theta$ on the E8 end of the array. Looking at the patches, E1
is at the right end of the row and E8 at the left. Turn the kit so that its face
swings toward the E1 end, as seen from the source, and the source ends up on the
E8 side of the normal, at $+\theta$. The stand counts the other way: its scale
is engraved on the fixed base and counts clockwise as seen from above, and
turning the face toward E1 is a counterclockwise turn, so the pointer reads
$-\theta$. A source at $+30^\circ$ sits under a pointer reading $-30$. Part 2
starts by confirming that sign with a beam sweep, whose **Angle** readout, set
to **Peak**, reads the source's angle.

Two things set how good the rotation is. The kit must turn about the center of
the array, between E4 and E5: an axis $20\ \text{mm}$ off center moves the
source's apparent angle by up to $1^\circ$ and its distance by up to
$20\ \text{mm}$, about $0.14\ \text{dB}$. The stand puts the array's center on
its axis by design. And its scale, ticked every $5^\circ$, reads to a degree or
two, which is fine for a lobe $15^\circ$ wide.
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
real patch. The rotation can resolve that difference because the
distance never changes. A hand-moved source cannot, because the radius drift alone is as
large as the effect.

The pattern is no longer symmetric. The first sidelobe on the inside of the
beam, near $+8^\circ$, sits about $-12.2$ dBc; the one on the outside, near
$+59^\circ$, sits about $-15.1$ dBc. The array factor alone would make them
equal, and the element pattern lowers the outer one. A careful move can show the
direction of that $2.9\ \text{dB}$ asymmetry; the rotation can put a number on
it.
::::

::::{frame} Two Error Budgets
:::{present}
| Error | Move | Rotation |
| :-- | :-- | :-- |
| Angle axis | time, not angle | $\pm 1^\circ$ |
| Distance | $\pm 0.7$ dB | $\pm 0.14$ dB |
| Room reflections | $\pm 1$ dB | $\pm 1$ dB |
:::

The packet's Part 1 builds both budgets. The move's angle error comes from
converting time to angle at a constant pace you did not have: a hand $30\%$
fast or slow through the main lobe makes a $13.0^\circ$ beam read anywhere from
$10.0^\circ$ to $18.6^\circ$. Its level error comes from the radius. The
rotation removes both, and replaces them with the axis offset and the
stand's scale, which are small and can be measured. Neither method removes the
room: a single reflection $18\ \text{dB}$ below the direct path moves a reading
by a decibel. The rotation's advantage there is repeatability. The reflections
sit in fixed places in the room, so a reading repeated at the same angle comes
back to the same value, and a difference between two of them is more
trustworthy than either reading alone.
::::

::::{frame} Equipment and Setup
:::{present}
- The kit on its rotating stand, $0^\circ$ toward the source.
- The HB100 on its tripod, $1.2\ \text{m}$ out at patch-row height, and a taped $1.2\ \text{m}$ arc.
- Four parts: bring up, check the angle axis, move the source, turn the kit.
:::

Tape the stand's base to the table with its $0^\circ$ mark toward the source,
and seat the kit's tripod in the platter's grooves with the patches facing the
pointer, as in
<a href="../L17-lab-bring-up/index.html#frame-the-rotating-stand">the L17 Lab</a>.
A kit without a stand can use a printed protractor instead, centered under the
middle of the array between E4 and E5 with $0^\circ$ toward the source; mark it
so that a turn toward E1 reads positive, and turn the tripod carefully about
that center.

Set the HB100 $1.2\ \text{m}$ from the array face at the height of the patch
row, facing the array. Lesson 21 put the far-field distance of this aperture at
$0.67\ \text{m}$, but level comparisons of under a decibel need more distance:
at $1\ \text{m}$ the scan loss reads only about half its value. Tape the
arc for moving the source on the floor at the same $1.2\ \text{m}$ radius, with marks at
$-90^\circ$, $0^\circ$, and $+90^\circ$.

The procedure has four parts: Steps 1 to 6 bring up the kit, Steps 7 to 9
check the angle axis, Steps 10 to 15 move the source by hand, and Steps 16 to
20 turn the kit on its stand. Each step that takes a reading has boxes for it,
which fill Part 2 of the packet.
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
3. **Calibrate the array.** Press **Calibrate** and wait for it to finish,
   with the HB100 still at boresight. Calibrate uses the frequency Find HB100
   stored, so it runs second.
4. **Load the preset.** Open **Lab Presets** and choose the **Array Factor**
   preset; its buttons respond only while the section is open.
5. **Set the gain.** Set **Rx Gain (dB)** for an FFT peak of $-10 \pm 3$
   dBFS, and record it. Every level in the packet is a difference between two
   readings at this gain, so leave it there for the whole lab. A main lobe with
   a flat top means the receiver has clipped; turn the gain down and start
   again.

   <div class="rec" data-lab="L21">
   <label>Step 5: Rx Gain (dB) <input data-field="f.gain" data-label="Step 5: Rx Gain (dB)"></label>
   </div>
6. **Start the sweep.** Turn on **Show Peak Angle Marker** under **Plot
   Options**, press **Start**, and open the **Rectangular** tab.
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
9. **The array factor.** At $0^\circ$, record the peak, the half-power
   beamwidth, and both first sidelobes. This is the trace you measured in the
   L20 Lab, and the reference for the other two runs.

   <div class="rec" data-lab="L21">
   <label>Step 9: peak (dBFS) <input data-field="b.peak" data-label="Step 9: peak (dBFS)"></label>
   <label>Step 9: half-power beamwidth <input data-field="b.hpbw" data-label="Step 9: half-power beamwidth"></label>
   <label>Step 9: left first sidelobe (dBc) <input data-field="b.left" data-label="Step 9: left first sidelobe (dBc)"></label>
   <label>Step 9: right first sidelobe (dBc) <input data-field="b.right" data-label="Step 9: right first sidelobe (dBc)"></label>
   </div>
::::

::::{frame} Run 2: Move It by Hand
:class: read-only

10. **Load the preset.** Choose the **Antenna Pattern** preset. It sets
    **Mode**, in the Beam Steering section, to **Signal vs Time**: the beam
    holds at the Steer Angle, which takes effect as you change it, with no
    Apply, and the **Tracking** tab plots the peak level in dBFS against time
    over the last $30\ \text{s}$.
11. **Hold the beam at broadside.** Set **Steer Angle (deg)** to $0$, check
    that the plot title reads "Beam held at 0.0°", and record the update rate
    the title shows.

    <div class="rec" data-lab="L21">
    <label>Step 11: updates per second <input data-field="f.rate" data-label="Step 11: updates per second"></label>
    </div>
12. **Pick up the source.** Lift the HB100 off its tripod and stand on the
    $-90^\circ$ mark, aimed at the array.
13. **Move.** Carry the HB100 along the arc to $+90^\circ$ in about 20 to $25\ \text{s}$,
    keeping the radius and the aim. The $30\ \text{s}$ window counts from when
    the mode starts, so begin promptly. Practice the move once before you
    record: too fast and each lobe gets only a few updates, too slow and the
    pattern runs off the edge.
14. **Read the trace.** Hover over the trace to read the main-lobe peak and
    both first sidelobes. Expect the room to make the two sidelobes unequal by
    a few decibels, with their average near $-13$ dBc, and the floor 25 to
    30 dB below the peak, so both sidelobes stand clear of it.
15. **Repeat.** Move it twice more, then return the HB100 to its tripod at
    boresight. The three moves will not agree exactly, and that disagreement
    is a measurement in its own right: record the spread, largest minus
    smallest, and Part 3 compares it with the rotation's.

    <div class="rec" data-lab="L21">
    <label>Move 1: time (s) <input data-field="c.w1.time" data-label="Step 15, move 1: time (s)"></label>
    <label>Move 1: peak (dBFS) <input data-field="c.w1.peak" data-label="Step 15, move 1: peak (dBFS)"></label>
    <label>Move 1: left first sidelobe (dBc) <input data-field="c.w1.left" data-label="Step 15, move 1: left first sidelobe (dBc)"></label>
    <label>Move 1: right first sidelobe (dBc) <input data-field="c.w1.right" data-label="Step 15, move 1: right first sidelobe (dBc)"></label>
    <label>Move 2: time (s) <input data-field="c.w2.time" data-label="Step 15, move 2: time (s)"></label>
    <label>Move 2: peak (dBFS) <input data-field="c.w2.peak" data-label="Step 15, move 2: peak (dBFS)"></label>
    <label>Move 2: left first sidelobe (dBc) <input data-field="c.w2.left" data-label="Step 15, move 2: left first sidelobe (dBc)"></label>
    <label>Move 2: right first sidelobe (dBc) <input data-field="c.w2.right" data-label="Step 15, move 2: right first sidelobe (dBc)"></label>
    <label>Move 3: time (s) <input data-field="c.w3.time" data-label="Step 15, move 3: time (s)"></label>
    <label>Move 3: peak (dBFS) <input data-field="c.w3.peak" data-label="Step 15, move 3: peak (dBFS)"></label>
    <label>Move 3: left first sidelobe (dBc) <input data-field="c.w3.left" data-label="Step 15, move 3: left first sidelobe (dBc)"></label>
    <label>Move 3: right first sidelobe (dBc) <input data-field="c.w3.right" data-label="Step 15, move 3: right first sidelobe (dBc)"></label>
    <label>Spread of the three moves: peak (dB) <input data-field="c.spread.peak" data-label="Step 15, spread of the three moves: peak (dB)"></label>
    <label>Spread: left sidelobe (dB) <input data-field="c.spread.left" data-label="Step 15, spread of the three moves: left sidelobe (dB)"></label>
    <label>Spread: right sidelobe (dB) <input data-field="c.spread.right" data-label="Step 15, spread of the three moves: right sidelobe (dB)"></label>
    </div>
::::

::::{frame} Run 3: Turn the Kit, Both Beams in One Pass
:class: read-only

16. **Sweep again.** Choose the **Steering Angle** preset so the beam sweeps,
    kit at $0^\circ$. Hover over the trace at $0^\circ$ steer and record that
    level as the reference; every level in Tables D and E is relative to it.

    <div class="rec" data-lab="L21">
    <label>Step 16: reference level (dBFS) <input data-field="d.ref" data-label="Step 16: reference level, kit at 0°, trace at 0° steer (dBFS)"></label>
    </div>
17. **Turn through the marks.** Turn the kit to each $10^\circ$ mark from
    $-90^\circ$ to $+90^\circ$, every second click of the stand. At each,
    record the **Angle** readout, the trace at $0^\circ$ steer (Table D), and
    the trace at the sample nearest $30^\circ$ (Table E), both relative to
    Step 16. One sweep reads both held beams at once, because each point of a
    sweep is the beam held at that steer angle for an instant; the sample
    nearest $30^\circ$ is $29.8^\circ$ near $10.44\ \text{GHz}$, on the
    $2.8125^\circ$ phase grid. Plot both tables against the Angle readout, not
    the stand's scale, because the readout catches a kit that slips; beyond
    about $\pm 70^\circ$, or near a null of the element pattern, the readout
    can wander, and there you use the mark. Turn the kit by the platter, not
    the board, so the tripod stays seated and the array stays on the axis, and
    keep the cables slack enough to follow it. Referring Table E to the
    broadside reference makes the scan loss read directly: the $30^\circ$
    beam's main-lobe level is the drop in peak gain.

    <div class="rec" data-lab="L21">
    <label>Mark −90°: Angle readout <input data-field="d.m90.angle" data-label="Step 17, mark −90°: Angle readout"></label>
    <label>Mark −90°: level, beam at 0° <input data-field="d.m90.level" data-label="Step 17, mark −90°: level, beam at 0° (Table D)"></label>
    <label>Mark −90°: level, beam at 30° <input data-field="e.m90.level" data-label="Step 17, mark −90°: level, beam at 30° (Table E)"></label>
    <label>Mark −80°: Angle readout <input data-field="d.m80.angle" data-label="Step 17, mark −80°: Angle readout"></label>
    <label>Mark −80°: level, beam at 0° <input data-field="d.m80.level" data-label="Step 17, mark −80°: level, beam at 0° (Table D)"></label>
    <label>Mark −80°: level, beam at 30° <input data-field="e.m80.level" data-label="Step 17, mark −80°: level, beam at 30° (Table E)"></label>
    <label>Mark −70°: Angle readout <input data-field="d.m70.angle" data-label="Step 17, mark −70°: Angle readout"></label>
    <label>Mark −70°: level, beam at 0° <input data-field="d.m70.level" data-label="Step 17, mark −70°: level, beam at 0° (Table D)"></label>
    <label>Mark −70°: level, beam at 30° <input data-field="e.m70.level" data-label="Step 17, mark −70°: level, beam at 30° (Table E)"></label>
    <label>Mark −60°: Angle readout <input data-field="d.m60.angle" data-label="Step 17, mark −60°: Angle readout"></label>
    <label>Mark −60°: level, beam at 0° <input data-field="d.m60.level" data-label="Step 17, mark −60°: level, beam at 0° (Table D)"></label>
    <label>Mark −60°: level, beam at 30° <input data-field="e.m60.level" data-label="Step 17, mark −60°: level, beam at 30° (Table E)"></label>
    <label>Mark −50°: Angle readout <input data-field="d.m50.angle" data-label="Step 17, mark −50°: Angle readout"></label>
    <label>Mark −50°: level, beam at 0° <input data-field="d.m50.level" data-label="Step 17, mark −50°: level, beam at 0° (Table D)"></label>
    <label>Mark −50°: level, beam at 30° <input data-field="e.m50.level" data-label="Step 17, mark −50°: level, beam at 30° (Table E)"></label>
    <label>Mark −40°: Angle readout <input data-field="d.m40.angle" data-label="Step 17, mark −40°: Angle readout"></label>
    <label>Mark −40°: level, beam at 0° <input data-field="d.m40.level" data-label="Step 17, mark −40°: level, beam at 0° (Table D)"></label>
    <label>Mark −40°: level, beam at 30° <input data-field="e.m40.level" data-label="Step 17, mark −40°: level, beam at 30° (Table E)"></label>
    <label>Mark −30°: Angle readout <input data-field="d.m30.angle" data-label="Step 17, mark −30°: Angle readout"></label>
    <label>Mark −30°: level, beam at 0° <input data-field="d.m30.level" data-label="Step 17, mark −30°: level, beam at 0° (Table D)"></label>
    <label>Mark −30°: level, beam at 30° <input data-field="e.m30.level" data-label="Step 17, mark −30°: level, beam at 30° (Table E)"></label>
    <label>Mark −20°: Angle readout <input data-field="d.m20.angle" data-label="Step 17, mark −20°: Angle readout"></label>
    <label>Mark −20°: level, beam at 0° <input data-field="d.m20.level" data-label="Step 17, mark −20°: level, beam at 0° (Table D)"></label>
    <label>Mark −20°: level, beam at 30° <input data-field="e.m20.level" data-label="Step 17, mark −20°: level, beam at 30° (Table E)"></label>
    <label>Mark −10°: Angle readout <input data-field="d.m10.angle" data-label="Step 17, mark −10°: Angle readout"></label>
    <label>Mark −10°: level, beam at 0° <input data-field="d.m10.level" data-label="Step 17, mark −10°: level, beam at 0° (Table D)"></label>
    <label>Mark −10°: level, beam at 30° <input data-field="e.m10.level" data-label="Step 17, mark −10°: level, beam at 30° (Table E)"></label>
    <label>Mark 0°: Angle readout <input data-field="d.0.angle" data-label="Step 17, mark 0°: Angle readout"></label>
    <label>Mark 0°: level, beam at 0° <input data-field="d.0.level" data-label="Step 17, mark 0°: level, beam at 0° (Table D)"></label>
    <label>Mark 0°: level, beam at 30° <input data-field="e.0.level" data-label="Step 17, mark 0°: level, beam at 30° (Table E)"></label>
    <label>Mark +10°: Angle readout <input data-field="d.p10.angle" data-label="Step 17, mark +10°: Angle readout"></label>
    <label>Mark +10°: level, beam at 0° <input data-field="d.p10.level" data-label="Step 17, mark +10°: level, beam at 0° (Table D)"></label>
    <label>Mark +10°: level, beam at 30° <input data-field="e.p10.level" data-label="Step 17, mark +10°: level, beam at 30° (Table E)"></label>
    <label>Mark +20°: Angle readout <input data-field="d.p20.angle" data-label="Step 17, mark +20°: Angle readout"></label>
    <label>Mark +20°: level, beam at 0° <input data-field="d.p20.level" data-label="Step 17, mark +20°: level, beam at 0° (Table D)"></label>
    <label>Mark +20°: level, beam at 30° <input data-field="e.p20.level" data-label="Step 17, mark +20°: level, beam at 30° (Table E)"></label>
    <label>Mark +30°: Angle readout <input data-field="d.p30.angle" data-label="Step 17, mark +30°: Angle readout"></label>
    <label>Mark +30°: level, beam at 0° <input data-field="d.p30.level" data-label="Step 17, mark +30°: level, beam at 0° (Table D)"></label>
    <label>Mark +30°: level, beam at 30° <input data-field="e.p30.level" data-label="Step 17, mark +30°: level, beam at 30° (Table E)"></label>
    <label>Mark +40°: Angle readout <input data-field="d.p40.angle" data-label="Step 17, mark +40°: Angle readout"></label>
    <label>Mark +40°: level, beam at 0° <input data-field="d.p40.level" data-label="Step 17, mark +40°: level, beam at 0° (Table D)"></label>
    <label>Mark +40°: level, beam at 30° <input data-field="e.p40.level" data-label="Step 17, mark +40°: level, beam at 30° (Table E)"></label>
    <label>Mark +50°: Angle readout <input data-field="d.p50.angle" data-label="Step 17, mark +50°: Angle readout"></label>
    <label>Mark +50°: level, beam at 0° <input data-field="d.p50.level" data-label="Step 17, mark +50°: level, beam at 0° (Table D)"></label>
    <label>Mark +50°: level, beam at 30° <input data-field="e.p50.level" data-label="Step 17, mark +50°: level, beam at 30° (Table E)"></label>
    <label>Mark +60°: Angle readout <input data-field="d.p60.angle" data-label="Step 17, mark +60°: Angle readout"></label>
    <label>Mark +60°: level, beam at 0° <input data-field="d.p60.level" data-label="Step 17, mark +60°: level, beam at 0° (Table D)"></label>
    <label>Mark +60°: level, beam at 30° <input data-field="e.p60.level" data-label="Step 17, mark +60°: level, beam at 30° (Table E)"></label>
    <label>Mark +70°: Angle readout <input data-field="d.p70.angle" data-label="Step 17, mark +70°: Angle readout"></label>
    <label>Mark +70°: level, beam at 0° <input data-field="d.p70.level" data-label="Step 17, mark +70°: level, beam at 0° (Table D)"></label>
    <label>Mark +70°: level, beam at 30° <input data-field="e.p70.level" data-label="Step 17, mark +70°: level, beam at 30° (Table E)"></label>
    <label>Mark +80°: Angle readout <input data-field="d.p80.angle" data-label="Step 17, mark +80°: Angle readout"></label>
    <label>Mark +80°: level, beam at 0° <input data-field="d.p80.level" data-label="Step 17, mark +80°: level, beam at 0° (Table D)"></label>
    <label>Mark +80°: level, beam at 30° <input data-field="e.p80.level" data-label="Step 17, mark +80°: level, beam at 30° (Table E)"></label>
    <label>Mark +90°: Angle readout <input data-field="d.p90.angle" data-label="Step 17, mark +90°: Angle readout"></label>
    <label>Mark +90°: level, beam at 0° <input data-field="d.p90.level" data-label="Step 17, mark +90°: level, beam at 0° (Table D)"></label>
    <label>Mark +90°: level, beam at 30° <input data-field="e.p90.level" data-label="Step 17, mark +90°: level, beam at 30° (Table E)"></label>
    </div>
18. **Find each lobe and null.** The $10^\circ$ marks sketch the patterns but
    miss the sidelobe peaks, which fall between marks. Turn slowly through each
    lobe and null of both beams and record the angle and level of each
    extreme, the highest reading for a lobe and the lowest for a null. Where
    the level stops changing as you turn, write "floor". Take the $30^\circ$
    main lobe twice, a few minutes apart, if you have time: a drop that repeats
    is a measurement, and one that does not is a reflection.

    <div class="rec" data-lab="L21">
    <label>Beam at 0°, main lobe: angle <input data-field="d.main.angle" data-label="Step 18, beam at 0°, main lobe: angle"></label>
    <label>Beam at 0°, main lobe: level <input data-field="d.main.level" data-label="Step 18, beam at 0°, main lobe: level"></label>
    <label>Beam at 0°, left first null: angle <input data-field="d.lnull.angle" data-label="Step 18, beam at 0°, left first null: angle"></label>
    <label>Beam at 0°, left first null: level <input data-field="d.lnull.level" data-label="Step 18, beam at 0°, left first null: level"></label>
    <label>Beam at 0°, right first null: angle <input data-field="d.rnull.angle" data-label="Step 18, beam at 0°, right first null: angle"></label>
    <label>Beam at 0°, right first null: level <input data-field="d.rnull.level" data-label="Step 18, beam at 0°, right first null: level"></label>
    <label>Beam at 0°, left first sidelobe: angle <input data-field="d.lsl.angle" data-label="Step 18, beam at 0°, left first sidelobe: angle"></label>
    <label>Beam at 0°, left first sidelobe: level <input data-field="d.lsl.level" data-label="Step 18, beam at 0°, left first sidelobe: level"></label>
    <label>Beam at 0°, right first sidelobe: angle <input data-field="d.rsl.angle" data-label="Step 18, beam at 0°, right first sidelobe: angle"></label>
    <label>Beam at 0°, right first sidelobe: level <input data-field="d.rsl.level" data-label="Step 18, beam at 0°, right first sidelobe: level"></label>
    <label>Beam at 30°, main lobe: angle <input data-field="e.main.angle" data-label="Step 18, beam at 30°, main lobe: angle"></label>
    <label>Beam at 30°, main lobe: level <input data-field="e.main.level" data-label="Step 18, beam at 30°, main lobe: level"></label>
    <label>Beam at 30°, inner first null: angle <input data-field="e.inull.angle" data-label="Step 18, beam at 30°, inner first null: angle"></label>
    <label>Beam at 30°, inner first null: level <input data-field="e.inull.level" data-label="Step 18, beam at 30°, inner first null: level"></label>
    <label>Beam at 30°, outer first null: angle <input data-field="e.onull.angle" data-label="Step 18, beam at 30°, outer first null: angle"></label>
    <label>Beam at 30°, outer first null: level <input data-field="e.onull.level" data-label="Step 18, beam at 30°, outer first null: level"></label>
    <label>Beam at 30°, inner first sidelobe: angle <input data-field="e.isl.angle" data-label="Step 18, beam at 30°, inner first sidelobe: angle"></label>
    <label>Beam at 30°, inner first sidelobe: level <input data-field="e.isl.level" data-label="Step 18, beam at 30°, inner first sidelobe: level"></label>
    <label>Beam at 30°, outer first sidelobe: angle <input data-field="e.osl.angle" data-label="Step 18, beam at 30°, outer first sidelobe: angle"></label>
    <label>Beam at 30°, outer first sidelobe: level <input data-field="e.osl.level" data-label="Step 18, beam at 30°, outer first sidelobe: level"></label>
    </div>
19. **Behind the board.** Turn the kit to $180^\circ$, source behind the
    board, and record the trace nearest $30^\circ$. The patches face away from
    the source and the ground plane sits between them, so expect the floor.

    <div class="rec" data-lab="L21">
    <label>Step 19, kit at 180°: level <input data-field="e.180.level" data-label="Step 19, kit at 180°: level, beam at 30° (Table E)"></label>
    </div>
20. **Restore.** Turn the kit back to $0^\circ$ before you leave.
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
- Angle: the rotation reads it; a range encodes it.
- Distance: the rotation fixes it.
- Reflections: $\pm 1$ dB in a room; a chamber absorbs them.
- Far field: set by the room's size, chamber or not.
:::
:::{present}
<img src="../../viz/img/L21-range-artifacts.svg"
     alt="A classroom measurement with floor and ceiling reflections beside an anechoic chamber measurement with absorber-lined walls, a turntable, and a single direct path."
     style="max-width: 560px; width: 100%; display: block; margin: 0 auto;">
:::

The rotation is a paper version of an antenna range, and comparing the two
shows what the classroom still leaves in your data.

**Angle.** A range turns the antenna on a turntable with a shaft encoder, so
every sample carries its angle to a fraction of a degree. Your sweep's Angle
readout gives each stop's angle to about a degree, which the moved source's time axis
cannot.

**Distance.** A range bolts the source at a fixed distance. So does the
rotation; moving the source does not.

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
Moving the source and turning the kit have no simulated version: the simulator's source is
fixed at boresight and cannot be moved, and turning a simulated kit changes
nothing. Run the electrical sweep of Table B in the hosted simulator at
[livethisdream.github.io/phaser](https://livethisdream.github.io/phaser/), and
use the widget above to see what a hand-moved trace looks like.
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

1. **Part 1, Pre-Lab** (individual, before the lab period, because you need it in class): the patterns to expect with the beam at $0^\circ$ and $30^\circ$, the error budgets of moving the source and the rotation, and reading dBc off a trace.
2. **Part 2, Measurements** (your own kit's data, recorded in class): the angle check, the electrical sweep, three moves, and two rotations.
3. **Part 3, Writeup** (individual, after the lab): which model the data support, moving the source against the rotation, and a far-field problem.

- <a class="doc-link" href="../../labs/ECE444_Lab_L21_Pattern_blank.pdf" target="_blank" rel="noopener">L21 Lab packet (PDF)</a>
::::

::::{frame} Summary: The Antenna Pattern, Measured
:class: read-only

| Idea | What it is | Number to remember |
| :-- | :-- | :-- |
| Beam sweep | beam swept past a fixed source | the array factor; x-axis is steer angle |
| Moved source | source carried around a held beam | x-axis is time; $\pm 0.7$ dB from a $10\ \text{cm}$ radius drift |
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
