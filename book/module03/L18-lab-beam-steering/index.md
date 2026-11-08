---
frame_view: true
---

# L18 Lab — Beam Steering

::::{frame}
:class: title-frame

<div class="course-mark">ECE 444 · Fall 2026</div>

<h1 class="frame-title">Beam Steering</h1>

<div class="title-rule"></div>

Two runs put the PHASER's peak at $30^\circ$ and $45^\circ$: move the source, or apply a steer angle.

L18 Lab · Antennas, Phased Arrays, and Radar Systems · Dr. Neil Rogers
::::

::::{frame} Printing
:class: read-only

To print the slides, switch to present mode and print: one slide a sheet,
with room for notes. Print from read mode for the whole lesson.
::::

::::{frame} Learning Objectives

<ol class="lo-list" style="--module: '3'; counter-reset: lo 4">
  <li>I can implement beam steering on the ADALM-PHASER and verify the steered pattern against theory.</li>
</ol>
::::

::::{frame} The Big Picture
:::{present}
- The sweep trace peaks where the beam meets the source.
- Run 1 moves the source; Run 2 applies a steer angle.
- Both put the peak at $45^\circ$ with the same width; only the moved source loses level, about $1.5\ \text{dB}$.
:::
:::{present}
<img src="../../viz/img/L18-sweep-compare.svg"
     alt="Three beam-sweep traces: the source at 0 degrees; the source moved to 45 degrees, peaking there 1.5 dB lower; and Apply 45 with the source at boresight, peaking at 45 degrees at full level"
     style="max-width: 560px; width: 100%; display: block; margin: 0 auto;">
:::

Lesson 18 showed that the beam-sweep trace is the array factor seen from the
source, so it peaks at the angle where the steered beam meets the source.
Today you put that peak at the same angles two ways. In Run 1, Phase Control
holds zero and you move the HB100 along an arc, so the trace follows the
source. In Run 2, the source stays at boresight and **Apply** in the Beam
Steering section writes per-element offsets that shift the trace to the angle
you type. At each angle you read the peak's angle and its half-power width
and check both against your Part 1 predictions. The two runs differ in one
reading you can see: a source moved to $45^\circ$ sits off each element's own
boresight, so its trace comes out about $1.5\ \text{dB}$ lower, and a
commanded beam does not.
::::

::::{frame} The Flow of the Lab
:::{present}
| Steps | Task | From Part 1 |
| :-- | :-- | :-- |
| 1 to 9 | Bring up the kit | your frequency |
| 10 to 15 | Run 1: move the source | HPBW, pass standard |
| 16 to 21 | Run 2: Apply 15, 30, 45 | Phase Control row |
:::
:::{present}
<img src="../../viz/img/L18-lab-sequence.svg"
     alt="The four stages of the L18 Lab, seen from above. Steps 1 to 9: the HB100 at 0 degrees on the 1 m arc for Find HB100 and Calibrate. Steps 10 to 14: Phase Control at zero, the source moved to 0, 30, and 45 degrees on the arc. Step 15: the same three lines 1.2 m out, Peak Gain on each. Steps 16 to 21: the source back at 0 degrees and the beam commanded to 15, 30, and 45 degrees with Apply."
     style="max-width: 100%; display: block; margin: 0 auto;">
:::

Run 1 fills Table A in Part 2 of the packet, and Run 2 fills Table B and the
Phase Control row. Keep the sweep running throughout: the trace redraws on
its own after you move the source or press Apply. Lesson 18's "Reading the
Trace" lists what to expect in each reading, and "How Close Is Close Enough"
explains the pass standard you sized in Part 1.
::::

::::{frame} Equipment and Setup
:::{present}
- The kit on its stand, cabled to your laptop as in Lesson 17.
- The HB100 at patch-row height on a $1\ \text{m}$ arc centered between E4 and E5.
- Facing the patches, $+\theta$ is to your left, toward E8.
:::
:::{present}
<img src="../../viz/img/L18-lab-setup.svg"
     alt="The setup from above: the eight-element array, a 1 m protractor arc centered between E4 and E5, and the HB100 positions at 0, 30, and 45 degrees on the plus side, toward E8, filled on the 1 m arc for the angle readings and hollow 1.2 m out on the same lines for the levels; confirm the plus side with the Angle readout"
     style="max-width: 560px; width: 100%; display: block; margin: 0 auto;">
:::

Set up the HB100 on a tripod about $1\ \text{m}$ from the array face, at the
height of the patch row, and lay a protractor arc of $1\ \text{m}$ radius
centered under the middle of the array, between E4 and E5. One meter clears
Lesson 17's far-field distance for this array, $0.88\ \text{m}$, which is
enough for the angles and beamwidths. Center the arc on the array, not on the
board's edge: an arc centered $10\ \text{mm}$ off the middle shifts the
reference angle by about $0.5^\circ$.

Lesson 18's sign convention puts $+\theta$ on the E8 end of the array. Facing
the patch side, E1 is at the right end of the row and E8 at the left, as in
the L17 Lab, so $+\theta$ is to your left. The figure looks down from above,
which puts E8 on the right. Step 11 confirms the sign on your kit.
::::

::::{frame} Bring Up the Kit
:class: read-only

1. **Connect.** Browse to your kit's address from Lesson 17 and wait for the
   pill to read **Connected**.
2. **Place the source.** Set the powered HB100 $1\ \text{m}$ out at $0^\circ$
   on the arc, facing the array.
3. **Find the source.** Press **Find HB100** and record the Signal Freq. If it
   is more than $25\ \text{MHz}$ from the frequency you used in Part 1, redo
   your Phase Control row before Run 2: a $25\ \text{MHz}$ difference moves
   E8's value by about $1.5^\circ$.

   <div class="rec" data-lab="L18">
   <label>Step 3: Signal Freq after <b>Find HB100</b> <input data-field="freq"></label>
   </div>
4. **Calibrate the array.** Press **Calibrate** and wait for it to finish,
   with the source still at boresight. A source off boresight while
   Calibrate runs bakes a steering ramp into the calibration offsets, and
   every trace after it peaks in the wrong place.
5. **Load the preset.** Open the **Lab Presets** section and choose the
   Steering Angle preset. It loads a uniform taper on E1 to E8, zeros Phase
   Control, turns **Use Bits** on, and sets **Signal BW** to
   $10\ \text{MHz}$, so each sweep point is one $2.8125^\circ$ phase step. It
   keeps the Signal Freq that Find HB100 stored and opens the **FFT** tab.
6. **Set the gain.** Set **Rx Gain (dB)** for an FFT peak of $-10 \pm 3$ dBFS,
   as in the L17 Lab; the preset does not set it.
7. **Mark the peak.** Turn on **Show Peak Angle Marker** under
   **Plot Options**.
8. **Check the tone.** Press **Start**. The **FFT** tab should show one narrow
   tone within about $\pm 1\ \text{MHz}$ of $0\ \text{MHz}$, at least
   $20\ \text{dB}$ above the floor. If the noise buries it, re-aim the HB100 or press
   **Find HB100** again.
9. **Open the trace.** Open the **Rectangular** tab. The sweep keeps running
   from here on, and the button reads **Stop**.
::::

::::{frame} Run 1: Move the Source
:class: read-only

Read every half-power beamwidth as the distance between the two angles where
the trace falls $3\ \text{dB}$ below its own peak. The difference box is
**Angle** minus the arc angle; compare it with the pass standard you sized in
Part 1.

10. **Zero the offsets.** Press **Reset** under **Phase Control**.
11. **Source at $0^\circ$.** Record **Angle** and the half-power beamwidth,
    then press **Freeze** to hold this trace. Expect the peak within your pass
    standard of $0^\circ$ and the width within a degree of your Part 1 value.
    If **Angle** reads near $-30^\circ$ when you later move the source, the
    source is on the negative side of the arc; move it across.

    <div class="rec" data-lab="L18">
    <label>Table A, source at 0°: Angle <input data-field="a.0.angle"></label>
    <label>Table A, source at 0°: difference from the arc angle <input data-field="a.0.diff"></label>
    <label>Table A, source at 0°: half-power beamwidth <input data-field="a.0.hpbw"></label>
    </div>
12. **Watch the move.** Keep the frozen trace on the plot for the next two
    positions, so you see the peak travel and the beam widen.
13. **Source at $+30^\circ$.** Move the HB100 along the arc to $+30^\circ$,
    still $1\ \text{m}$ out and facing the array, and record the same three
    boxes. The beam is wider than at $0^\circ$, by the $1/\cos\theta_0$ of
    Lesson 18.

    <div class="rec" data-lab="L18">
    <label>Table A, source at 30°: Angle <input data-field="a.30.angle"></label>
    <label>Table A, source at 30°: difference from the arc angle <input data-field="a.30.diff"></label>
    <label>Table A, source at 30°: half-power beamwidth <input data-field="a.30.hpbw"></label>
    </div>
14. **Source at $+45^\circ$.** Move it to $+45^\circ$ and record the same
    three. If **Angle** jumps to about $-90^\circ$, read the main lobe's angle
    off the trace and record that. The sweep's last steps take the
    element-to-element phase out to $-227.8^\circ$, the same ramp as
    $+132.2^\circ$, which points within a few degrees of a $45^\circ$ source;
    the GUI plots all of them at $-90^\circ$, so they read almost as high as
    the main lobe, and noise can lift one above it.

    <div class="rec" data-lab="L18">
    <label>Table A, source at 45°: Angle <input data-field="a.45.angle"></label>
    <label>Table A, source at 45°: difference from the arc angle <input data-field="a.45.diff"></label>
    <label>Table A, source at 45°: half-power beamwidth <input data-field="a.45.hpbw"></label>
    </div>
15. **Levels, $1.2\ \text{m}$ out.** Move the HB100 straight out to
    $1.2\ \text{m}$ (4 ft) or more on the $+45^\circ$ line and record **Peak
    Gain**; repeat on the $+30^\circ$ and $0^\circ$ lines at the same
    distance, and record the distance. At $1\ \text{m}$ the level differences
    read smaller than the element pattern gives, so take them farther out; if
    the room will not allow it, record the distance you used. Expect the
    $45^\circ$ level 1 to 2 dB below the $0^\circ$ level. The $30^\circ$ level
    should sit within about a dB of the $0^\circ$ level: its $0.6\ \text{dB}$
    drop is smaller than the ripple a reflection puts on the main lobe, so
    one reading cannot show it.

    <div class="rec" data-lab="L18">
    <label>Table A, source at 0°: Peak Gain <input data-field="a.0.gain"></label>
    <label>Table A, source at 30°: Peak Gain <input data-field="a.30.gain"></label>
    <label>Table A, source at 45°: Peak Gain <input data-field="a.45.gain"></label>
    <label>Table A: distance for the Peak Gain column <input data-field="a.dist"></label>
    </div>
::::

::::{frame} Run 2: Apply the Steer Angle
:class: read-only

16. **Source back to boresight.** Move the HB100 back to $0^\circ$ on the arc,
    $1\ \text{m}$ out.
17. **Apply 15.** In **Beam Steering**, leave **Taper** on Uniform, enter 15 in
    **Steer Angle (deg)**, and press **Apply**. Apply also rewrites
    **Element Gains** with the chosen taper, which is why it stays on Uniform.
18. **Record.** Record **Angle**, **Peak Gain**, and the half-power
    beamwidth. The trace peaks near $15^\circ$ with a boresight source,
    because the sweep's own ramp cancels the offsets there. The difference
    box is **Angle** minus the Apply value.

    <div class="rec" data-lab="L18">
    <label>Table B, Apply 15: Angle <input data-field="b.15.angle"></label>
    <label>Table B, Apply 15: difference from the Apply value <input data-field="b.15.diff"></label>
    <label>Table B, Apply 15: half-power beamwidth <input data-field="b.15.hpbw"></label>
    <label>Table B, Apply 15: Peak Gain <input data-field="b.15.gain"></label>
    </div>
19. **Apply 30.** Repeat for 30, then copy the eight **Phase Control** boxes
    beside your Part 1 prediction. Read the boxes, not the sliders: the
    sliders stop at $\pm 180^\circ$, and Apply writes unwrapped values. The
    read-back should match your prediction to within $1^\circ$ on every
    element; a difference that grows with element number means your Part 1
    frequency differs from the Signal Freq on screen.

    <div class="rec" data-lab="L18">
    <label>Table B, Apply 30: Angle <input data-field="b.30.angle"></label>
    <label>Table B, Apply 30: difference from the Apply value <input data-field="b.30.diff"></label>
    <label>Table B, Apply 30: half-power beamwidth <input data-field="b.30.hpbw"></label>
    <label>Table B, Apply 30: Peak Gain <input data-field="b.30.gain"></label>
    <label>Phase Control, E1: predicted (your Question 2(a)) <input data-field="pc.pred.1"></label>
    <label>Phase Control, E2: predicted (your Question 2(a)) <input data-field="pc.pred.2"></label>
    <label>Phase Control, E3: predicted (your Question 2(a)) <input data-field="pc.pred.3"></label>
    <label>Phase Control, E4: predicted (your Question 2(a)) <input data-field="pc.pred.4"></label>
    <label>Phase Control, E5: predicted (your Question 2(a)) <input data-field="pc.pred.5"></label>
    <label>Phase Control, E6: predicted (your Question 2(a)) <input data-field="pc.pred.6"></label>
    <label>Phase Control, E7: predicted (your Question 2(a)) <input data-field="pc.pred.7"></label>
    <label>Phase Control, E8: predicted (your Question 2(a)) <input data-field="pc.pred.8"></label>
    <label>Phase Control, E1: read back <input data-field="pc.read.1"></label>
    <label>Phase Control, E2: read back <input data-field="pc.read.2"></label>
    <label>Phase Control, E3: read back <input data-field="pc.read.3"></label>
    <label>Phase Control, E4: read back <input data-field="pc.read.4"></label>
    <label>Phase Control, E5: read back <input data-field="pc.read.5"></label>
    <label>Phase Control, E6: read back <input data-field="pc.read.6"></label>
    <label>Phase Control, E7: read back <input data-field="pc.read.7"></label>
    <label>Phase Control, E8: read back <input data-field="pc.read.8"></label>
    <label>Phase Control, E1: difference <input data-field="pc.diff.1"></label>
    <label>Phase Control, E2: difference <input data-field="pc.diff.2"></label>
    <label>Phase Control, E3: difference <input data-field="pc.diff.3"></label>
    <label>Phase Control, E4: difference <input data-field="pc.diff.4"></label>
    <label>Phase Control, E5: difference <input data-field="pc.diff.5"></label>
    <label>Phase Control, E6: difference <input data-field="pc.diff.6"></label>
    <label>Phase Control, E7: difference <input data-field="pc.diff.7"></label>
    <label>Phase Control, E8: difference <input data-field="pc.diff.8"></label>
    </div>
20. **Apply 45.** Repeat for 45. If **Angle** jumps to about $-90^\circ$,
    record the main lobe's angle off the trace, as in Step 14. Compare the
    Peak Gain with the $0^\circ$ row of Table A: the commanded beam keeps the
    source on the elements' boresight, so it does not lose the
    $1.5\ \text{dB}$ the moved source did.

    <div class="rec" data-lab="L18">
    <label>Table B, Apply 45: Angle <input data-field="b.45.angle"></label>
    <label>Table B, Apply 45: difference from the Apply value <input data-field="b.45.diff"></label>
    <label>Table B, Apply 45: half-power beamwidth <input data-field="b.45.hpbw"></label>
    <label>Table B, Apply 45: Peak Gain <input data-field="b.45.gain"></label>
    </div>
21. **Reset.** Press **Reset** under **Phase Control** before you leave the
    station. The offsets stay loaded until you do, and they add to every
    sweep: with Apply 30 still loaded and the source moved to $+30^\circ$, the
    trace would peak at $90^\circ$.
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

The simulator holds its source at boresight, so Run 1's moves have no
simulated version. Run 2 works as written, and it is the rehearsal in Part 1 of the
packet: Apply 30 gives the trace a source at $+30^\circ$ would, and Phase
Control shows the same offsets as the hardware. The simulator has no element
pattern, so Peak Gain does not drop in either run; it does not model
**Rx Gain (dB)**; its tone sits at $-1\ \text{MHz}$; and **Find HB100** and
**Calibrate** run scripted scans.
:::
::::

::::{frame} Your Part 2 Entries
:class: read-only

This frame collects every box you filled in on this page. Your entries stay in this
browser only, saved as you type. **Download my packet** writes them into Part 2
of the blank packet and saves the PDF; do Parts 1 and 3 on paper or in the PDF
viewer, and upload one PDF to Gradescope. If you have already typed Part 1 into
the packet PDF, use **Fill my own copy** and choose that file instead: your Part 1
is kept, and Part 2 is added to it. Either way the result is locked, so finish
any typing in the PDF first. **Export entries** saves a small backup file you
can **Import** on another laptop or after clearing your browser. The boxes are
optional: the blank packet is in the next frame, to fill on paper or in a PDF
viewer instead.

<div class="rec-summary" data-lab="L18" data-pdf="../../labs/ECE444_Lab_L18_Steering_blank.pdf" data-file="ECE444_L18_Lab"></div>
::::

::::{frame} Lab Packet
:class: read-only doc-links

The L18 Lab packet is one submission for the whole lab, turned in complete before Lesson 19. It has three parts:

1. Part 1, Pre-Lab (individual, before the lab period, because you need it in class): the phase table at your kit's frequency, what Phase Control will show, the beamwidths, the pass standard, and a rehearsal of Run 2 on the hosted simulator.
2. Part 2, Measurements (your own kit's data, recorded in class): Tables A and B, from Run 1 and Run 2.
3. Part 3, Writeup (individual, after the lab): reconcile the measurements with the predictions, and three analysis problems.

- <a class="doc-link" href="../../labs/ECE444_Lab_L18_Steering_blank.pdf" target="_blank" rel="noopener">L18 Lab packet (PDF)</a>
::::

::::{frame} For Part 3
:class: read-only

Part 3 of the packet is the writeup, done after class with your Part 2
entries beside you. Its first question asks four things:

1. Does every peak in Table A fall within your pass standard? For a row
   outside it, name the error source most likely responsible.
2. Compare the $45^\circ$ rows of Tables A and B. Why do the angle and width
   agree while only the moved source loses level? Why does the packet not
   ask you to compare the $30^\circ$ levels?
3. Does the Phase Control read-back match your prediction? Explain the sign,
   and any difference.
4. Do the beamwidths match your predictions, and why does the lab quote them
   to the nearest degree?

Lesson 18's
<a href="../L18-beam-steering/index.html#frame-two-ways-to-steer-the-peak">"Two Ways to Steer the Peak"</a>,
<a href="../L18-beam-steering/index.html#frame-the-sign-in-phase-control">"The Sign in Phase Control"</a>,
and
<a href="../L18-beam-steering/index.html#frame-how-close-is-close-enough">"How Close Is Close Enough"</a>
give the reasoning. The three analysis problems that follow read a classmate's
sweep, recover a steer angle from Phase Control, and compare two frozen traces.
::::

::::{frame} Looking Ahead
:class: read-only

The L19 Lab uses today's skill: the peak of a sweep is a bearing, and bearings
from several stations cross at the hidden HB100.
::::
