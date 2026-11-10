---
frame_view: true
---

# L21 Lab — Antenna Pattern

::::{frame}
:class: title-frame

<div class="course-mark">ECE 444 · Fall 2026</div>

<h1 class="frame-title">Antenna Pattern</h1>

<div class="title-rule"></div>

Hold the beam still and sweep the HB100 in azimuth, by hand and on the stand.

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

::::{frame} The Big Picture
:::{present}
- The beam sweep steps beams past a fixed HB100; an azimuth sweep moves the HB100 past one beam.
- Today you take both on your kit and compare lobe levels in dBc.
- Part 1 predicts what each trace shows.
:::
:::{present}
<img src="../../viz/img/L21-three-methods.svg"
     alt="Three ways to trace a pattern. Beam sweep: the HB100 stays put and the kit steps the beam past it. By hand: the beam is held and you carry the HB100 around an arc. On the stand: the beam is held, the HB100 stays on its tripod, and the kit turns on its stand."
     style="max-width: 560px; width: 100%; display: block; margin: 0 auto;">
:::

Lesson 21 compared the kit's beam sweep, which steps the beam past a fixed
HB100, with an azimuth sweep, which holds one beam and moves the source.
Today you take both on your own kit: a beam sweep, three azimuth sweeps by
hand, and one pass of the kit on its stand that reads a beam held at
$0^\circ$ and one held at $30^\circ$ together. You compare the lobe levels in
dBc against the predictions you made in Part 1 of the packet, which say where
the two methods should agree, where they should not, and how closely two
traces must match before you call them the same.
::::

::::{frame} The Flow of the Lab
:::{present}
| Steps | Run | Part 1 |
| :-- | :-- | :-- |
| 1 to 6 | Bring up the kit | Q1 |
| 7 to 9 | Run 1: beam sweep | Q2, Q3 |
| 10 to 15 | Run 2: by hand | Q3, Q5 |
| 16 to 19 | Run 3: on the stand | Q3, Q4 |
:::
:::{present}
<picture>
<source media="(max-width: 600px)" srcset="../../viz/img/L21-lab-sequence-narrow.svg">
<img src="../../viz/img/L21-lab-sequence.svg" alt="The three runs of the L21 Lab, each with a sketch of the setup and a thumbnail of the trace to expect. Run 1, Steps 7 to 9: the HB100 fixed, the kit steps the beam, a broadside beam-sweep trace against steer angle. Run 2, Steps 10 to 15: the beam held at 0 degrees while you carry the HB100 along the arc, the same pattern against elapsed time. Run 3, Steps 16 to 19: the HB100 fixed and the kit turned on its stand, the 0 and 30 degree beams read at the stand's 10 degree marks." style="max-width: 100%; display: block; margin: 0 auto;">
</picture>
:::

Run 1 confirms that the stand's scale and the kit agree on the sign of the
source angle and takes the beam sweep, Table A and Table B in Part 2 of the
packet. Run 2 holds the beam at $0^\circ$ and has you carry the HB100 around
the arc three times, Table C. Run 3 sweeps the beam again while you turn the
kit through the stand's marks, so one pass fills Table D, the beam held at
$0^\circ$, and Table E, the beam held at $30^\circ$. Lesson 21's
<a href="../L21-antenna-pattern/index.html#frame-reading-your-traces">"Reading Your Traces"</a>
lists what each comparison should show.
::::

::::{frame} Equipment and Setup
:::{present}
- Seat the kit on its stand, $0^\circ$ toward the HB100.
- Set the HB100 on its tripod at patch-row height, $1.2\ \text{m}$ out.
- Tape a $1.2\ \text{m}$ arc. Its $-90^\circ$ end is on the E1 side, where each sweep by hand starts.
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
$+90^\circ$. The $-90^\circ$ end is on the E1 side of the array: on your left
as you stand at the laptop behind the kit, as the figure shows from above,
and on the right as seen from the HB100.
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
   stand reads $-30$, which puts the source at $+30^\circ$ (Lesson 21,
   <a href="../L21-antenna-pattern/index.html#frame-turning-the-kit-on-its-stand">"Turning the Kit on Its Stand"</a>), and record the
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
    then carry the HB100 along the arc to $+90^\circ$ in about
    $22\ \text{s}$, keeping the radius and the aim. Practice the arc once
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
    stand reading with its sign flipped, as in Table A. One pass reads both
    held beams, as Lesson 21's
    <a href="../L21-antenna-pattern/index.html#frame-turning-the-kit-on-its-stand">"Turning the Kit on Its Stand"</a>
    shows. Turn the kit by the platter, not by the
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
    extreme, the highest reading for a lobe and the lowest for a null, every
    level relative to Step 16 as in Step 17; Part 3 converts the lobes to dBc.
    An antenna range finds a lobe peak the same way. Where the level stops
    changing as you turn, it has reached the noise floor: write "floor".
    Last, turn back to the main lobe of the beam held at $0^\circ$ and to its
    right first sidelobe, and read each again: the change from your first
    reading is the stand's repeatability, which Part 3 compares with the spread
    of your sweeps by hand.

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
    <label>Main lobe, read again: level <input data-field="d.rep.main" data-label="Step 18, Beam at 0°, main lobe read again: level"></label>
    <label>Right first sidelobe, read again: level <input data-field="d.rep.rsl" data-label="Step 18, Beam at 0°, right first sidelobe read again: level"></label>
    </div>
19. **Restore.** Turn the kit back to $0^\circ$ before you leave.
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

This frame collects every box you filled in on this page. Your entries stay in this
browser only, saved as you type. **Download my packet** writes them into Part 2
of the blank packet and saves the PDF; do Parts 1 and 3 on paper or in the PDF
viewer, and upload one PDF to Gradescope. If you have already typed Part 1 into
the packet PDF, use **Fill my own copy** and choose that file instead: your Part 1
is kept, and the page adds Part 2 to it. Either way the result is locked, so finish
any typing in the PDF first. **Export entries** saves a small backup file you
can **Import** on another laptop or after clearing your browser. The boxes are
optional: the blank packet is in the next frame, to fill on paper or in a PDF
viewer instead.

<div class="rec-summary" data-lab="L21" data-pdf="../../labs/ECE444_Lab_L21_Pattern_blank.pdf" data-file="ECE444_L21_Lab"></div>
::::

::::{frame} Lab Packet
:class: read-only doc-links

The L21 Lab packet is one submission for the whole lab, turned in complete before Lesson 22. It has three parts:

1. Part 1, Pre-Lab (individual, before the lab period, because you need it in class): what each trace should show with the beam at $0^\circ$ and $30^\circ$, how to pace the sweep by hand, reading dBc off a trace, and what counts as agreement.
2. Part 2, Measurements (your own kit's data, recorded in class): the angle check, the beam sweep, three azimuth sweeps by hand, and one pass on the stand.
3. Part 3, Writeup (individual, after the lab): where the methods agree on lobe levels, the sweep by hand against the pass on the stand, and a far-field problem.

- <a class="doc-link" href="../../labs/ECE444_Lab_L21_Pattern_blank.pdf" target="_blank" rel="noopener">L21 Lab packet (PDF)</a>
::::

::::{frame} For Part 3
:class: read-only

Part 3 of the packet is the writeup, done after class with your Part 2
entries beside you. Convert the lobe levels of Tables D and E to dBc first:
subtract each table's main-lobe level. Then it asks three things:

1. Do the three methods agree on the broadside first sidelobes, within the
   window you found in Part 1? At $30^\circ$, do the two first sidelobes
   differ in the direction you predicted, and by more than your own
   broadside pair?
2. How does the spread of your three sweeps by hand compare with the stand's
   repeatability from Step 18? Convert a sweep's peak time to an angle at a
   steady pace, and say what an uneven pace moves: the lobe positions, the
   levels, or both. Could either method certify a sidelobe below
   $-25$ dBc?
3. A far-field problem for a larger panel at a higher frequency.

Lesson 21's
<a href="../L21-antenna-pattern/index.html#frame-measurement-errors">"Measurement Errors"</a>
and
<a href="../L21-antenna-pattern/index.html#frame-classroom-against-chamber">"Classroom Against Chamber"</a>
give the size of each effect.
::::

::::{frame} Looking Ahead
:class: read-only

Lesson 22 tapers the Element Gains to push the first sidelobes below the
level you measured today, which widens the main lobe.
::::
