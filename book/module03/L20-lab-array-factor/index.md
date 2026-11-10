---
frame_view: true
---

# L20 Lab — Array Factor

::::{frame}
:class: title-frame

<div class="course-mark">ECE 444 · Fall 2026</div>

<h1 class="frame-title">Array Factor</h1>

<div class="title-rule"></div>

Switch elements off, one sweep at a time, and measure what the beam does.

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
- Lesson 20: the active aperture, $Nd/\lambda$, sets the beamwidth.
- Four sweeps past a fixed HB100, each checking a Part 1 prediction.
:::
:::{present}
| Step | Active elements |
| :-- | :-- |
| 7 | E1 to E8 |
| 8 | E3 to E6 |
| 9 | E4 and E5 |
| 10 | E1 and E8 |
:::

Lesson 20 showed that the beamwidth of a uniform array depends on the array
only through its active aperture, $Nd$, measured in wavelengths. Today you
test that on your kit. You sweep the beam past a fixed HB100 three times,
switching off elements at the ends of the row so that $Nd$ halves between
sweeps, and read the half-power beamwidth, the first-null beamwidth, the
first sidelobe, and the peak off each trace. A fourth sweep leaves only E1
and E8 on: two elements again, like Step 9, but spread across the whole row.
Each sweep fills one row of Table A in Part 2 of the packet, and the E1 and
E8 sweep also fills Table B. You check every reading against the prediction
you made in Part 1.
::::

::::{frame} Predict First
:class: viz-frame

:::{depth}
Before you sweep, predict each trace, then check yourself. Switch the
elements to match a row of the table above and decide, before you press
**Show pattern**: how wide the main lobe is next to the dashed eight-element
pattern, how far the peak drops, and how many full-height lobes there are.
Then show it. Any change to the elements hides the pattern again, so each
guess comes first. The widget draws the ideal array factor at 10.0 GHz, not
at your kit's frequency, so its numbers are close to your Part 1 values but
not equal to them; the kit's trace differs from both in the ways Lesson 20's
<a href="../L20-array-factor-beamwidth/index.html#frame-what-the-sweep-shows">"What the Sweep Shows"</a>
lists.
:::

:::{present}
<iframe src="../../viz/af-element-predict.html"
        width="100%" height="485"
        style="border: 1px solid #cddce9; border-radius: 6px;"
        loading="lazy"
        title="Choose the active elements of the eight-element row, predict the array factor, then show it">
</iframe>
:::
::::

::::{frame} Bring Up the Kit
:::{present}
- HB100 at boresight, $1\ \text{m}$ out, at patch-row height; it stays there for all four sweeps.
- Find HB100, Calibrate, then the Array Factor preset.
- Set Rx Gain for a $-10$ dBFS peak.
:::

Place the HB100 at boresight, about $1\ \text{m}$ from the face of the array, at
the same height as the patch row and with its face square to the array.
Boresight placement matters more than distance in this lab: every prediction
is a broadside number, and a source offset by a few degrees shifts the
whole trace along the angle axis. Leave it there for the whole lab, because
you compare the four traces against each other at the end.

1. **Connect.** Browse to your kit's address from Lesson 17 and wait for the
   pill to read **Connected**.
2. **Find the source.** With the HB100 at boresight, press **Find HB100** and
   record the Signal Freq in Part 2 of the packet. If it is more than
   $50\ \text{MHz}$ from the frequency you used in Part 1, recompute your
   calculated columns before you sweep; a smaller change moves no prediction
   by more than about $0.5^\circ$.

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
   the sweep should peak near $0^\circ$, with its first sidelobes near
   $\pm 22^\circ$ and 11 to 14 dB below the peak. If they are higher than
   that, or differ from each other by more than a few dB, run **Calibrate**
   again before you go on.
::::

::::{frame} Sweep Four Apertures
:::{present}
- For each row: set the Element Gains, **Start**, then **Freeze**.
- Record Peak Gain, HPBW, FNBW, and first SLL in Table A.
- Read levels in dBc, from each trace's own peak.
- Ignore the column standing at $\pm 90^\circ$.
:::

Before each sweep, check your Part 1 row for it. For each one, press
**Start**, then **Freeze** to hold the trace, and record four numbers in the
boxes under the step, which fill Table A: the Peak Gain readout; the HPBW, between the two angles where the
trace falls $3\ \text{dB}$ below its peak; the FNBW, between the two minima
that bracket the main lobe; and the first SLL, the tallest sidelobe.

Read every level in **dBc**: subtract the trace's own peak from the reading,
so the peak is 0 dBc. Peak Gain reads in dBFS and drops each time you switch
elements off, so only a level taken from its own trace's peak compares with
the array factor and with the other traces. The last few dozen points of every sweep
ask for more phase than any real angle needs, and all of them plot at
$\pm 90^\circ$, so the trace stands up in that column. That column is the
array factor at the extra phase, not a lobe: leave it out of Steps 7 to 10.

7. **Eight elements.** With all eight Element Gains at 100, sweep. Your HPBW
   should land within a degree of your calculated value.

   <div class="rec" data-lab="L20">
   <label>Peak Gain (dBFS) <input data-field="a8.peak" data-label="Step 7, 8 elements: Peak Gain (dBFS)"></label>
   <label>HPBW <input data-field="a8.hpbw" data-label="Step 7, 8 elements: HPBW"></label>
   <label>FNBW <input data-field="a8.fnbw" data-label="Step 7, 8 elements: FNBW"></label>
   <label>First SLL (dBc) <input data-field="a8.sll" data-label="Step 7, 8 elements: first SLL (dBc)"></label>
   </div>
8. **Four elements, E3 to E6.** Set E1, E2, E7, and E8 to 0, and sweep. The
   peak drops by the change you predicted in Part 1, or up to about 1.5 dB
   less on the kit. A null that fills to the noise floor reads wide, so this
   FNBW can come out a few degrees wider than your prediction.

   <div class="rec" data-lab="L20">
   <label>Peak Gain (dBFS) <input data-field="a4.peak" data-label="Step 8, E3 to E6: Peak Gain (dBFS)"></label>
   <label>Change from 8 elements (dB) <input data-field="a4.step" data-label="Step 8, E3 to E6: change from 8 elements (dB)"></label>
   <label>HPBW <input data-field="a4.hpbw" data-label="Step 8, E3 to E6: HPBW"></label>
   <label>FNBW <input data-field="a4.fnbw" data-label="Step 8, E3 to E6: FNBW"></label>
   <label>First SLL (dBc) <input data-field="a4.sll" data-label="Step 8, E3 to E6: first SLL (dBc)"></label>
   </div>
9. **Two elements, E4 and E5.** Set every element to 0 except E4 and E5, and
   sweep. The peak drops from the eight-element peak by your predicted change,
   or up to about 3 dB less on the kit. A trace that keeps falling toward
   $\pm 80^\circ$ is the two-element array factor's own roll-off toward
   endfire, not a fault.

   <div class="rec" data-lab="L20">
   <label>Peak Gain (dBFS) <input data-field="a2.peak" data-label="Step 9, E4 and E5: Peak Gain (dBFS)"></label>
   <label>Change from 8 elements (dB) <input data-field="a2.step" data-label="Step 9, E4 and E5: change from 8 elements (dB)"></label>
   <label>HPBW <input data-field="a2.hpbw" data-label="Step 9, E4 and E5: HPBW"></label>
   <label>FNBW <input data-field="a2.fnbw" data-label="Step 9, E4 and E5: FNBW"></label>
   <label>First SLL (dBc) <input data-field="a2.sll" data-label="Step 9, E4 and E5: first SLL (dBc)"></label>
   </div>
10. **Two elements, E1 and E8.** Set E4 and E5 to 0 and E1 and E8 to 100, and
    sweep. Record in Table A the peak, the change from eight elements, and the
    HPBW and FNBW of the lobe at $0^\circ$, and in its First SLL box the level
    of the first full-height lobe on either side of it, $m = \pm 1$. Record in Table B the angle and level of
    every full-height lobe, numbered $m = -3$ to $+3$ from the most negative
    angle, $m = 0$ at $0^\circ$. The $m = \pm 4$ lobes need more phase than any
    real angle and stand at full height in the $\pm 90^\circ$ column; leave
    them out.

    <div class="rec" data-lab="L20">
    <label>Peak Gain (dBFS) <input data-field="a18.peak" data-label="Step 10, E1 and E8: Peak Gain (dBFS)"></label>
    <label>Change from 8 elements (dB) <input data-field="a18.step" data-label="Step 10, E1 and E8: change from 8 elements (dB)"></label>
    <label>HPBW <input data-field="a18.hpbw" data-label="Step 10, E1 and E8: HPBW"></label>
    <label>FNBW <input data-field="a18.fnbw" data-label="Step 10, E1 and E8: FNBW"></label>
    <label>Level of the m = ±1 lobe (dBc) <input data-field="a18.sll" data-label="Step 10, E1 and E8: level of the m = ±1 lobe (dBc)"></label>
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
:::{present}
- Overlay the three frozen uniform traces.
- Does the beamwidth scale as $1/Nd$? Does each peak step match your Part 1 voltage sum?
- Restore all eight Element Gains to 100.
:::

11. **Compare the frozen traces.** The three uniform apertures are on the plot
    together. Set each HPBW and FNBW beside its $Nd$, and each peak change
    beside the voltage sum you used in Part 1, from Lesson 20's
    <a href="../L20-array-factor-beamwidth/index.html#frame-halving-the-active-aperture">"Halving the Active Aperture"</a>.
    The kit reads up to about 1.5 dB less than the voltage sum per halving,
    3 dB less over both; a shortfall that size is within the spread of its
    readings. Part 3 asks you to explain what you see.
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
come out at the ideal voltage-sum value, without the kit's shortfall of up to 1.5 dB,
and it does not model **Rx Gain (dB)**. Record those as your measured column
and reconcile them against the calculated column exactly as you would with the
kit.
```
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

<div class="rec-summary" data-lab="L20" data-pdf="../../labs/ECE444_Lab_L20_ArrayFactor_blank.pdf" data-file="ECE444_L20_Lab"></div>
::::

::::{frame} Lab Packet
:class: read-only doc-links

The L20 Lab packet is one submission for the whole lab, turned in complete before Lesson 21. It has three parts:

1. Part 1, Pre-Lab (individual, before the lab period, because you need it in class): your kit's frequency, the prediction table for the three uniform apertures, the array factor and lobe angles for E1 and E8, and a rehearsal of the E1 and E8 sweep on the hosted simulator.
2. Part 2, Measurements (your own kit's data, recorded in class): Table A, one row per sweep, and Table B, the E1 and E8 lobes.
3. Part 3, Writeup (individual, after the lab): reconcile the measurements with the predictions, and two analysis problems.

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
   do not? Use where each pair puts its weight along the row.
3. How do your two peak changes compare with the voltage sum's step,
   given the spread of your readings?

Lesson 20's
<a href="../L20-array-factor-beamwidth/index.html#frame-what-the-sweep-shows">"What the Sweep Shows"</a>
gives the expected size of each difference. The two analysis problems that
follow use Lesson 20's results, and the last part of the second compares a
Hann taper, from Lesson 22, with switching elements off.
::::

::::{frame} Looking Ahead
:class: read-only

Lesson 21 holds one beam still and sweeps the source around it in azimuth,
and the L21 Lab compares that trace with today's beam sweep.
::::
