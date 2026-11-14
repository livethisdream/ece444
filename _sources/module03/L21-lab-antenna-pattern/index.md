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
| Steps | Run | Beam | Moves |
| :-- | :-- | :-- | :-- |
| 1 to 6 | Bring up | | |
| 7 to 9 | 1: beam sweep | stepped | kit |
| 10 to 15 | 2: by hand | held at $0^\circ$ | HB100 |
| 16 to 19 | 3: on the stand | read at $0^\circ$, $30^\circ$ | kit |
:::
:::{present}
<img src="../../viz/img/L21-three-methods.svg"
     alt="Three ways to trace a pattern. Beam sweep: the HB100 stays put and the kit steps the beam past it. By hand: the beam is held and you carry the HB100 around an arc. On the stand: the beam is held, the HB100 stays on its tripod, and the kit turns on its stand."
     style="max-width: 560px; width: 100%; display: block; margin: 0 auto;">
:::

Lesson 21 compared the kit's beam sweep, which steps the beam past a fixed
HB100, with an azimuth sweep, which holds one beam and moves the source.
Today you take both on your own kit and compare the lobe levels in dBc
against the predictions you made in Part 1 of the packet.

Run 1 confirms that the stand's scale and the kit agree on the sign of the
source angle, then takes the beam sweep: Tables A and B in Part 2 of the
packet. Run 2 holds the beam at $0^\circ$ while you carry the HB100 along the
arc three times: Table C. Run 3 sweeps the beam again while you turn the kit
through the stand's marks, so one pass fills Table D, the beam held at
$0^\circ$, and Table E, the beam held at $30^\circ$.
::::

::::{frame} Predict First
:class: viz-frame

:::{depth}
Before you take a trace, predict it, then check yourself. Choose a beam angle
and decide, before you press **Show azimuth sweep**, how the azimuth sweep
compares with the dashed beam sweep: where its peak and first nulls fall,
whether its first sidelobes read at the beam sweep's level, and which lobes
read lower. Then show it. Choosing another angle hides the azimuth sweep
again, so each guess comes first. Both traces are in dBc of their own peak,
with the noise floor about $23\ \text{dB}$ down. The widget draws the course
model at $10.0\ \text{GHz}$, not at your kit's frequency, so its numbers are
close to your Part 1 values but not equal to them; Lesson 21's
<a href="../L21-antenna-pattern/index.html#frame-reading-your-traces">"Reading Your Traces"</a>
says which features the room and the floor leave you able to compare.
:::

:::{present}
<iframe src="../../viz/azimuth-predict.html"
        width="100%" height="485"
        style="border: 1px solid #cddce9; border-radius: 6px;"
        loading="lazy"
        title="Choose a beam angle, predict the azimuth sweep against the beam sweep, then show it">
</iframe>
:::
::::

::::{frame} Bring Up the Kit
:::{present}
- Kit on its stand at $0^\circ$; HB100 at patch-row height, $1.2\ \text{m}$ out.
- Tape a $1.2\ \text{m}$ arc with its $-90^\circ$ end on the E1 side.
- Find HB100, Calibrate, then the Array Factor preset.
- Set Rx Gain for a $-10$ dBFS peak.
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
:::{present}
- Turn the kit to $-30$, $+30$, and $0$ on the stand, and read the **Angle** readout, set to **Peak**, at each.
- Back at $0^\circ$, read the beam sweep: the peak, the half-power beamwidth, and both first sidelobes.
:::

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
   beamwidth, and both first sidelobes, and compare them with your Part 1
   predictions. This is the trace you measured in the L20 Lab, and the
   reference for the other two runs.

   <div class="rec" data-lab="L21">
   <label>Step 9: peak (dBFS) <input data-field="b.peak" data-label="Step 9: peak (dBFS)"></label>
   <label>Step 9: half-power beamwidth <input data-field="b.hpbw" data-label="Step 9: half-power beamwidth"></label>
   <label>Step 9: left first sidelobe (dBc) <input data-field="b.left" data-label="Step 9: left first sidelobe (dBc)"></label>
   <label>Step 9: right first sidelobe (dBc) <input data-field="b.right" data-label="Step 9: right first sidelobe (dBc)"></label>
   </div>
::::

::::{frame} Run 2: Azimuth Sweep by Hand
:::{present}
- Choose the Antenna Pattern preset and hold the beam at $0^\circ$.
- Carry the HB100 along the arc from $-90^\circ$ to $+90^\circ$, three times.
- Read each sweep's peak and both first sidelobes in dBc.
:::

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
    to dBc by subtracting the main-lobe peak, and compare them with your Part 1
    predictions. The room can make the two first sidelobes unequal by a few
    decibels, so record both.
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
:::{present}
- Choose the Array Factor preset again, kit at $0^\circ$, and read the reference level.
- Turn the kit through every $10^\circ$ mark; read the beam at $0^\circ$ and at $30^\circ$.
- Turn slowly through each lobe and null for its extreme.
:::

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
18. **Find each lobe and null.** Turn slowly through each lobe and null of
    both beams and record the source angle and level of each extreme, the
    highest reading for a lobe and the lowest for a null, every level relative
    to Step 16 as in Step 17, and compare each with your Part 1 predictions;
    Part 3 converts the lobes to dBc. Where the level stops
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
browser only, saved as you type. **Download my packet** writes them into the Measured
cells of the blank packet and saves the PDF. The download locks every field, the Predicted cells and Part 3
included, so type those into your own copy of the packet first, then use **Fill
my own copy** and choose that file: your predictions and Part 3 are kept, and
the page adds your measurements beside them. If you work Parts 1 and 3 on paper, download the packet
and write on the printout. Upload one PDF to Gradescope. **Export entries**
saves a small backup file you can **Import** on another laptop or after
clearing your browser. The boxes are optional: the blank packet is in the next
frame, to fill on paper or in a PDF viewer instead.

<div class="rec-summary" data-lab="L21" data-pdf="../../labs/ECE444_Lab_L21_Pattern_blank.pdf" data-file="ECE444_L21_Lab"></div>
::::

::::{frame} Lab Packet
:class: read-only doc-links

The L21 Lab packet is one submission for the whole lab, turned in complete before Lesson 22. It has three parts:

1. Part 1, Predict (individual, before the lab period, because you need it in class): the shaded Predicted cells of every table, at your kit's frequency, with your work for one row of each attached on your own paper.
2. Part 2, Measure (your own kit's readings, recorded in class): the white Measured cells of the same tables, from the angle check, the beam sweep, three azimuth sweeps by hand, and one pass on the stand.
3. Part 3, Analyze (individual, after the lab): three open prompts, each answered from your own readings.

- <a class="doc-link" href="../../labs/ECE444_Lab_L21_Pattern_blank.pdf" target="_blank" rel="noopener">L21 Lab packet (PDF)</a>
::::

::::{frame} For Part 3
:class: read-only

Part 3 is done after class with your Part 2 entries and your Part 1
predictions beside you. Convert the lobe levels of Tables D and E to dBc
first: subtract each table's main-lobe level. Then it asks about three
comparisons:

1. Broadside, three ways: compare the beam sweep, the sweeps by hand, and
   the measurement on the stand with your predictions.
2. The beam at $30^\circ$: compare your measurement at $30^\circ$ (Table E)
   with your measurement at broadside (Table D) and with your predictions.
3. By hand against the stand: what you would report from each method, and
   the broadside first-sidelobe level as you would report it from today's
   data.

I grade each answer on a claim, the evidence from your own numbers, the
reasoning that connects them, and the uncertainty. Lesson 21's
<a href="../L21-antenna-pattern/index.html#frame-measurement-errors">"Measurement Errors"</a>
lists the error sources to size from your own readings.

::::

::::{frame} Looking Ahead
:class: read-only

Lesson 22 tapers the Element Gains to push the first sidelobes below the
level you measured today, which widens the main lobe.
::::
