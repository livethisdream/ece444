---
frame_view: true
---

# L20 Lab — Array Factor

::::{frame}
:class: title-frame

<div class="course-mark">ECE 444 · Fall 2026</div>

<h1 class="frame-title">Array Factor</h1>

<div class="title-rule"></div>

Halve the active aperture and watch the beam double.

L20 Lab · Antennas, Phased Arrays, and Radar Systems · Dr. Neil Rogers
::::

::::{frame} Printing
:class: read-only

To print the slides, switch to present mode and print: one slide a sheet,
with room for notes. Print from read mode for the whole lesson.
::::

::::{frame} Learning Objectives

<ol class="lo-list" style="--module: '3'; counter-reset: lo 1">
  <li>I can derive the array factor for an arbitrary linear array and apply pattern multiplication.</li>
</ol>
::::

::::{frame} The Big Picture
:::{present}
- Lesson 20: the aperture in wavelengths, $Nd/\lambda$, sets the beamwidth.
- Today you halve the active aperture twice and watch the beam double.
- Then E1 and E8 alone: two elements spanning the whole row.
:::

Lesson 20 showed that the beamwidth of a uniform array depends on the array
only through its active aperture, $Nd$, measured in wavelengths. Today you
test that on your kit. You sweep the beam past a fixed HB100 three times,
switching off elements at the ends of the row so that $Nd$ halves between
sweeps, and read the half-power beamwidth, the first-null beamwidth, and the
first sidelobe off each trace. A fourth sweep leaves only E1 and E8 on: two
elements again, but spread across the whole row. You check every reading
against the prediction you made in Part 1 of the packet.
::::

::::{frame} The Flow of the Lab
:::{present}
| Steps | Task | From Part 1 |
| :-- | :-- | :-- |
| 1 to 6 | Bring up the kit | your frequency |
| 7 to 9 | Sweep 8, 4, 2 elements | prediction table |
| 10 | Sweep E1 and E8 | lobe angles, widths |
| 11 and 12 | Compare and restore | |
:::

Each sweep fills one row of Table A in Part 2 of the packet, and the E1 and
E8 sweep also fills Table B. Freeze each trace before you start the next, so
that Step 11 can compare them on one plot. Lesson 20's "What the Sweep Shows"
lists the differences to expect between a trace and the array factor.
::::

::::{frame} Equipment and Setup
:::{present}
- The HB100 at boresight, $1\ \text{m}$ out, at patch-row height.
- Leave it there for all four sweeps.
- Fill Tables A and B in Part 2 as you go.
:::

Place the HB100 at boresight, about $1\ \text{m}$ from the face of the array, at
the same height as the patch row and with its face square to the array.
Boresight placement matters more than distance in this lab: every prediction
is a broadside number, and a source offset by a few degrees shifts the
whole trace along the angle axis. Leave it there for the whole lab, because
you compare the four traces against each other at the end.
::::

::::{frame} Bring Up the Kit
:class: read-only

1. **Connect.** Browse to your kit's address from Lesson 17 and wait for the
   pill to read **Connected**.
2. **Find the source.** With the HB100 at boresight, press **Find HB100** and
   record the Signal Freq in Part 2 of the packet. If it is more than
   $50\ \text{MHz}$ from the frequency you used in Part 1, recompute your
   calculated columns before you sweep; a smaller change moves no prediction
   by more than about $0.3^\circ$.

   <div class="rec" data-lab="L20">
   <label>Step 2: Signal Freq <input data-field="f.sig"></label>
   </div>
3. **Calibrate the array.** Press **Calibrate** and wait for it to finish, with
   the HB100 still at boresight. An uncalibrated array has amplitude and phase
   errors spread across the row, which fills the nulls and raises the
   sidelobes on its own, and you would then be measuring the calibration
   rather than the array factor. If the broadside sweep in Step 6 does not
   look right, fix that first.
4. **Load the preset.** Open **Lab Presets** and press **Array Factor**; its
   buttons respond only while the section is open. The preset sets a uniform
   taper on all eight elements, zero steering phase, and Use Bits on, so each
   sweep point is one $2.8125^\circ$ phase step. It opens the **Rectangular**
   tab.
5. **Set the gain.** Set **Rx Gain (dB)** for an FFT peak of $-10 \pm 3$ dBFS,
   and record it. The preset does not set it, and the right value depends on
   your source, its battery, and its distance; about $1\ \text{dB}$ is a
   reasonable start with the source $1\ \text{m}$ out. A flat-topped
   main lobe on the Rectangular tab means the receiver has clipped, so turn
   the gain down. Leave it there for all four sweeps, so the peaks compare.

   <div class="rec" data-lab="L20">
   <label>Step 5: Rx Gain (dB) <input data-field="f.gain"></label>
   </div>
6. **Check the broadside sweep.** Press **Start**. On the **Rectangular** tab,
   the sweep should peak near $0^\circ$ with a clean pair of first sidelobes.
::::

::::{frame} Sweep Four Apertures
:class: read-only

Before each sweep, check your Part 1 row for it. For each one, press
**Start**, then **Freeze** to hold the trace, and record four numbers in the
boxes under the step, which fill Table A: the Peak Gain readout; the HPBW, between the two angles where the
trace falls $3\ \text{dB}$ below its peak; the FNBW, between the two minima
that bracket the main lobe; and the first SLL, the tallest sidelobe relative
to the peak.

7. **Eight elements.** With all eight Element Gains at 100, sweep. Expect one
   main lobe at $0^\circ$ and three or four sidelobe pairs on each side, an
   HPBW within a degree of your calculated value, and a first SLL near
   $\pm 22^\circ$ at $-11$ to $-14\ \text{dBc}$.

   <div class="rec" data-lab="L20">
   <label>Peak Gain (dBFS) <input data-field="a8.peak" data-label="Step 7, 8 elements: Peak Gain (dBFS)"></label>
   <label>HPBW <input data-field="a8.hpbw" data-label="Step 7, 8 elements: HPBW"></label>
   <label>FNBW <input data-field="a8.fnbw" data-label="Step 7, 8 elements: FNBW"></label>
   <label>First SLL (dBc) <input data-field="a8.sll" data-label="Step 7, 8 elements: first SLL (dBc)"></label>
   </div>
8. **Four elements, E3 to E6.** Set E1, E2, E7, and E8 to 0, and sweep. The
   main lobe is roughly twice as wide, the sidelobes thin to one pair near
   $\pm 50^\circ$, and the peak drops about $6\ \text{dB}$, which the kit
   reads as 5 to 6 dB. A null that fills to the floor reads wide, so this FNBW
   can come out a few degrees wider than your prediction.

   <div class="rec" data-lab="L20">
   <label>Peak Gain (dBFS) <input data-field="a4.peak" data-label="Step 8, E3 to E6: Peak Gain (dBFS)"></label>
   <label>Change from 8 elements (dB) <input data-field="a4.step" data-label="Step 8, E3 to E6: change from 8 elements (dB)"></label>
   <label>HPBW <input data-field="a4.hpbw" data-label="Step 8, E3 to E6: HPBW"></label>
   <label>FNBW <input data-field="a4.fnbw" data-label="Step 8, E3 to E6: FNBW"></label>
   <label>First SLL (dBc) <input data-field="a4.sll" data-label="Step 8, E3 to E6: first SLL (dBc)"></label>
   </div>
9. **Two elements, E4 and E5.** Set every element to 0 except E4 and E5, and
   sweep. The peak sits about $12\ \text{dB}$ below the eight-element peak,
   which the kit reads as 10 to 12 dB. The trace falls about $20\ \text{dB}$
   toward $\pm 80^\circ$: that is the two-element array factor's own roll-off
   toward endfire, not a fault.

   <div class="rec" data-lab="L20">
   <label>Peak Gain (dBFS) <input data-field="a2.peak" data-label="Step 9, E4 and E5: Peak Gain (dBFS)"></label>
   <label>Change from 8 elements (dB) <input data-field="a2.step" data-label="Step 9, E4 and E5: change from 8 elements (dB)"></label>
   <label>HPBW <input data-field="a2.hpbw" data-label="Step 9, E4 and E5: HPBW"></label>
   <label>FNBW <input data-field="a2.fnbw" data-label="Step 9, E4 and E5: FNBW"></label>
   <label>First SLL (dBc) <input data-field="a2.sll" data-label="Step 9, E4 and E5: first SLL (dBc)"></label>
   </div>
10. **Two elements, E1 and E8.** Set E4 and E5 to 0 and E1 and E8 to 100, and
    sweep. Record in Table B the peak, the HPBW and FNBW of the lobe at
    $0^\circ$, and the angle and level of every full-height lobe. The lobes
    are numbered $m = -3$ to $+3$ from the most negative angle, $m = 0$ at
    $0^\circ$.

    <div class="rec" data-lab="L20">
    <label>Peak Gain (dBFS) <input data-field="a18.peak" data-label="Step 10, E1 and E8: Peak Gain (dBFS)"></label>
    <label>Change from 8 elements (dB) <input data-field="a18.step" data-label="Step 10, E1 and E8: change from 8 elements (dB)"></label>
    <label>HPBW <input data-field="a18.hpbw" data-label="Step 10, E1 and E8: HPBW"></label>
    <label>FNBW <input data-field="a18.fnbw" data-label="Step 10, E1 and E8: FNBW"></label>
    <label>First SLL (dBc) <input data-field="a18.sll" data-label="Step 10, E1 and E8: first SLL (dBc)"></label>
    <label>Angle <input data-field="lobe.m3.angle" data-label="Step 10, lobe −3: angle"></label>
    <label>Level (dBc) <input data-field="lobe.m3.level" data-label="Step 10, lobe −3: level (dBc)"></label>
    <label>Angle <input data-field="lobe.m2.angle" data-label="Step 10, lobe −2: angle"></label>
    <label>Level (dBc) <input data-field="lobe.m2.level" data-label="Step 10, lobe −2: level (dBc)"></label>
    <label>Angle <input data-field="lobe.m1.angle" data-label="Step 10, lobe −1: angle"></label>
    <label>Level (dBc) <input data-field="lobe.m1.level" data-label="Step 10, lobe −1: level (dBc)"></label>
    <label>Angle <input data-field="lobe.0.angle" data-label="Step 10, lobe 0: angle"></label>
    <label>Angle <input data-field="lobe.p1.angle" data-label="Step 10, lobe +1: angle"></label>
    <label>Level (dBc) <input data-field="lobe.p1.level" data-label="Step 10, lobe +1: level (dBc)"></label>
    <label>Angle <input data-field="lobe.p2.angle" data-label="Step 10, lobe +2: angle"></label>
    <label>Level (dBc) <input data-field="lobe.p2.level" data-label="Step 10, lobe +2: level (dBc)"></label>
    <label>Angle <input data-field="lobe.p3.angle" data-label="Step 10, lobe +3: angle"></label>
    <label>Level (dBc) <input data-field="lobe.p3.level" data-label="Step 10, lobe +3: level (dBc)"></label>
    </div>
::::

::::{frame} Compare and Restore
:class: read-only

11. **Compare the frozen traces.** The three uniform apertures are on the plot
    together. The beamwidth doubles at each halving, because $Nd$ halves and
    both beamwidth formulas scale as $1/Nd$; this is the main result of the
    lab. The peak steps down at each halving, because the elements add in
    voltage at boresight. The ideal steps are

    $$\begin{aligned}
    \Delta P &= 20\log_{10}\!\left(\frac{N_{\text{active}}}{8}\right) \\
    &= -6.0\ \text{dB} \quad (N = 4) \\
    &= -12.0\ \text{dB} \quad (N = 2)
    \end{aligned}$$

    and the kit reads about 5 to 6 dB per halving, consistent with the ideal
    within the spread of its readings. Your two steps are the change column of
    Steps 8 and 9.
12. **Restore the array.** Set all eight Element Gains back to 100, so the next
    lab starts from a full uniform aperture.
::::

::::{frame} No Hardware?
:class: read-only

```{note}
Run `python phaser_headless.py --sim` and open the same URL. The lab reproduces
step for step in simulation, because the simulated source already sits at
boresight and nothing in the procedure requires moving it. Its Signal Freq is
$10.525\ \text{GHz}$, so compute the calculated columns there. It adds the element signals exactly in voltage, so its peak steps
come out at the ideal $6.0\ \text{dB}$ rather than the kit's 5 to 6 dB,
and it does not model **Rx Gain (dB)**. Record those as your measured column
and reconcile them against the calculated column exactly as you would with the
kit.
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

<div class="rec-summary" data-lab="L20" data-pdf="../../labs/ECE444_Lab_L20_ArrayFactor_blank.pdf" data-file="ECE444_L20_Lab"></div>
::::

::::{frame} Lab Packet
:class: read-only doc-links

The L20 Lab packet is one submission for the whole lab, turned in complete before Lesson 21. It has three parts:

1. **Part 1, Pre-Lab** (individual, before the lab period, because you need it in class): your kit's frequency, the prediction table for the three uniform apertures, the array factor and lobe angles for E1 and E8, and a rehearsal of the E1 and E8 sweep on the hosted simulator.
2. **Part 2, Measurements** (your own kit's data, recorded in class): Table A, one row per sweep, and Table B, the E1 and E8 lobes.
3. **Part 3, Writeup** (individual, after the lab): reconcile the measurements with the predictions, and two analysis problems.

- <a class="doc-link" href="../../labs/ECE444_Lab_L20_ArrayFactor_blank.pdf" target="_blank" rel="noopener">L20 Lab packet (PDF)</a>
::::

::::{frame} For Part 3
:class: read-only

Part 3 of the packet is the writeup, done after class with your Part 2
entries beside you. Its first question asks three things:

1. Does the beam double at each halving? Expect the eight- and four-element
   HPBW within about a degree of your Part 1 values, and the two-element HPBW
   within several degrees. Name the cause of any larger difference.
2. Why do the E1 and E8 peak and the E4 and E5 peak agree while their beams
   do not? Use the span of each pair in wavelengths.
3. How do your two peak changes compare with the $6.0\ \text{dB}$ voltage sum,
   given the spread of your readings?

Lesson 20's
<a href="../L20-array-factor-beamwidth/index.html#frame-what-the-sweep-shows">"What the Sweep Shows"</a>
gives the expected size of each difference. The two analysis problems that
follow work from Lesson 20 alone.
::::

::::{frame} Looking Ahead
:class: read-only

Lesson 21 holds one beam still and sweeps the source around it in azimuth,
and the L21 Lab compares that trace with today's beam sweep.
::::
