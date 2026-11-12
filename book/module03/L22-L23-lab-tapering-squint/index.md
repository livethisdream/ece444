---
frame_view: true
---

# L22–L23 Lab — Tapering, Squint, and Quantization

::::{frame}
:class: title-frame

<div class="course-mark">ECE 444 · Fall 2026</div>

<h1 class="frame-title">Tapering, Squint, and Quantization</h1>

<div class="title-rule"></div>

Taper the row, thin it, set its phases off frequency, and drop phase bits.

L22–L23 Lab · Antennas, Phased Arrays, and Radar Systems · Dr. Neil Rogers
::::

::::{frame} Printing
:class: read-only

To print the slides, switch to present mode and print: one slide a sheet,
with room for notes. Print from read mode for the whole lesson.
::::

::::{frame} Learning Objectives

<ol class="lo-list" style="--module: '3'; counter-reset: lo 6">
  <li>I can apply amplitude tapering (uniform, cosine, Chebyshev, Taylor) to control sidelobe level and predict the pattern trade-off.</li>
  <li>I can identify grating lobes, beam squint, and quantization effects in a phased array and describe their impact on system performance.</li>
</ol>
::::

::::{frame} The Big Picture
:::{present}
| Steps | Run | Set |
| :-- | :-- | :-- |
| 1–6 | Bring up | HB100 at boresight |
| 7–13 | Tapers | Four presets, then yours |
| 14–16 | Grating lobes | Rx1, Rx4, Rx7; then Rx1, Rx5 |
| 17–18 | Squint | Signal BW 10, 500 MHz |
| 19–22 | Quantization | 7, 4, 3, 2 bits |
:::

Lesson 22 showed how an amplitude taper trades beamwidth and directivity for
lower sidelobes, and why the peak drop the sweep plots is not the directivity
the array loses. Lesson 23 showed three departures a taper cannot touch,
because they come from the element spacing, the frequency the phases are set
at, and the phase shifter's resolution. Today you test both on your kit in four
runs. Steps 1 to 6 bring up the kit with the HB100 at boresight. The taper runs
fill Tables A and B in Part 2 of the packet, the grating-lobe run Table C, the
squint run Table D, and the quantization run Table E, and you check every
reading against the prediction you made in Part 1.

The HB100 stays at boresight through Step 16. It moves to $45^\circ$ for the
squint run, and you sweep it in azimuth for the quantization run. Freeze the
uniform trace in Step 7 and keep it on the plot through Step 16, because every
peak drop is read against it.
::::

::::{frame} Predict First
:class: viz-frame

:::{depth}
Before each run, predict its trace, then check yourself. Choose a run and a
setting from the table above and decide, before you press **Show trace**: how
wide the main lobe is next to the dashed reference and how far its peak falls,
whether a sidelobe clears the floor, where the full-height lobes stand, how far
the squinted peak moves from the source, and which bit counts raise a lobe.
Then show it. Any change hides the trace again, so each guess comes first. The
widget draws the ideal array factor at $10.0\ \text{GHz}$, not at your kit's
frequency, so its numbers are close to your Part 1 values but not equal to
them, and it leaves out the peak drops Part 1 asks for. The floor is an example
at $23$ dB down; you read your own in Step 8.
:::

:::{present}
<iframe src="../../viz/taper-squint-predict.html"
        width="100%" height="485"
        style="border: 1px solid #cddce9; border-radius: 6px;"
        loading="lazy"
        title="Choose a run of the L22 to L23 Lab and its setting, predict the trace, then show it">
</iframe>
:::
::::

::::{frame} Bring Up the Kit
:::{present}
- HB100 at boresight, $1.2$ m out, at patch-row height; keep $\pm 40^\circ$ clear.
- Find HB100, Calibrate, then set Rx Gain for a $-10$ dBFS peak.
- Load the Tapering preset with Enforce Symmetric Taper on.
:::

Place the HB100 at boresight, $1.2$ m from the array face, at patch-row height
and aimed at the center of the patch row. Check the $1.2$ m against the
far-field distance in your Part 1 Setup row: the sweep reads the
far-field pattern only beyond it. Every taper number is a comparison between
sweeps, so the source stays put until Step 17. Keep $\pm 40^\circ$ either side
of the kit clear of walls and people, because a reflection off either raises a
false lobe on the sweep.

1. **Place the source.** Put the HB100 at boresight, $1.2$ m out, at patch-row
   height, and record the distance.

   <div class="rec" data-lab="L22-L23">
   <label>Step 1: distance to the source <input data-field="f.dist"></label>
   </div>
2. **Connect.** Browse to your kit's address and wait for the pill to read
   **Connected**.
3. **Find the source.** Press **Find HB100** and record the Signal Freq it
   reports. If it differs by more than about 1% ($100\ \text{MHz}$) from the
   frequency you used in Part 1, rework your predictions before you sweep.

   <div class="rec" data-lab="L22-L23">
   <label>Step 3: Signal Freq <input data-field="f.sig"></label>
   </div>
4. **Calibrate the array.** Press **Calibrate** and wait for it to finish, with
   the HB100 still at boresight; it uses the frequency Find HB100 stored. An
   uncalibrated array carries element-to-element gain and phase errors that
   look exactly like a taper you did not ask for. If the uniform trace's two
   first sidelobes differ by more than about 2 dB in Step 8, calibrate again.
5. **Set the gain.** Set **Rx Gain** so the FFT peak, beam at $0^\circ$ and
   source at boresight, reads $-10 \pm 3$ dBFS, and record it. Leave it there
   for the whole lab, so every peak compares.

   <div class="rec" data-lab="L22-L23">
   <label>Step 5: Rx Gain (dB) <input data-field="f.gain"></label>
   </div>
6. **Load the preset.** Open **Lab Presets** and choose the Tapering preset; it
   loads the HB100 configuration and opens the **Rectangular** tab. Under
   Element Gains, check that **Enforce Symmetric Taper** is on, so each slider
   moves its mirror-image partner.
::::

::::{frame} Taper Runs
:::{present}
- Freeze a uniform sweep: every peak drop is read against it.
- Sweep Hann, then Blackman and Chebyshev if time allows.
- Read levels in dBc, and record the noise floor.
- Design a taper to the Step 12 specification.
:::

Read every level in **dBc**: subtract the trace's own peak from the reading,
so the peak is 0 dBc. The plot reads dBFS, and a tapered trace peaks lower
than the uniform one, so only a level taken from its own trace's peak means
the same thing on every trace. The one exception is the peak drop, which you
read against the frozen uniform trace.

7. **Freeze the reference.** Choose the **Uniform** taper, check that all eight
   sliders read 100%, press **Start**, and read **Peak Gain** and **Angle**
   (set to **Peak**). Press **Freeze**: this trace stays on the plot as the
   reference every peak drop is read against.
8. **Read the uniform trace.** Record the HPBW, the angles where the trace
   falls 3 dB below its own peak, the first sidelobe, and the noise floor.
   Compare the HPBW with your Part 1 value: the sweep steps one
   $2.8125^\circ$ phase step a point, about a degree of angle near broadside,
   so the 3 dB crossings land between samples and a degree of difference is
   within the reading. If the two first sidelobes, near $\pm 22^\circ$, differ
   by more than about 2 dB, calibrate again and repeat Steps 7 and 8.

   <div class="rec" data-lab="L22-L23">
   <label>Step 8, Uniform: HPBW <input data-field="a.uni.hpbw"></label>
   <label>Step 8, Uniform: first sidelobe (dBc) <input data-field="a.uni.sll"></label>
   <label>Step 8: noise floor (dBc) <input data-field="f.floor"></label>
   </div>
9. **Load Hann.** Choose the **Hann** taper and check the eight sliders read
   12, 43, 77, 100, 100, 77, 43, 12. Check your Part 1 row for it.
10. **Sweep Hann.** Press **Start** and record the HPBW, the peak drop against
    the frozen uniform trace, and the first sidelobe, and compare each with
    your Part 1 row for Table A. On a
    kit without the gain-slider fix, the slider is not linear in voltage, and
    every taper comes out milder than your Part 1 row, its beam narrower and
    its peak drop smaller by about the same fraction on every taper. Record
    what you measure; Part 3 asks you to account for any difference.

    <div class="rec" data-lab="L22-L23">
    <label>Step 10, Hann: HPBW <input data-field="a.hann.hpbw"></label>
    <label>Step 10, Hann: peak drop (dB) <input data-field="a.hann.drop"></label>
    <label>Step 10, Hann: first sidelobe <input data-field="a.hann.sll"></label>
    </div>
11. **Blackman and Chebyshev (optional).** Repeat Steps 9 and 10 for each, if
    time allows, and compare with your Part 1 rows.

    <div class="rec" data-lab="L22-L23">
    <label>Step 11, Blackman: HPBW <input data-field="a.black.hpbw"></label>
    <label>Step 11, Blackman: peak drop (dB) <input data-field="a.black.drop"></label>
    <label>Step 11, Blackman: first sidelobe <input data-field="a.black.sll"></label>
    <label>Step 11, Chebyshev: HPBW <input data-field="a.cheb.hpbw"></label>
    <label>Step 11, Chebyshev: peak drop (dB) <input data-field="a.cheb.drop"></label>
    <label>Step 11, Chebyshev: first sidelobe <input data-field="a.cheb.sll"></label>
    </div>
12. **Design your own taper.** With Enforce Symmetric Taper on, meet this
    specification: HPBW no wider than $16^\circ$, with the first sidelobe
    below $-20$ dBc. Start from the taper you designed in Part 1, Table B.
    Set the sliders, sweep, read the HPBW and sidelobe, and
    adjust: raise the end elements to narrow the beam, and lower them if the
    sidelobe rises past $-20$ dBc. Record your final gains and the result.

    <div class="rec" data-lab="L22-L23">
    <label>Step 12: Rx1, Rx8 (%) <input data-field="b.g1"></label>
    <label>Step 12: Rx2, Rx7 (%) <input data-field="b.g2"></label>
    <label>Step 12: Rx3, Rx6 (%) <input data-field="b.g3"></label>
    <label>Step 12: Rx4, Rx5 (%) <input data-field="b.g4"></label>
    <label>Step 12: HPBW <input data-field="b.hpbw"></label>
    <label>Step 12: peak drop (dB) <input data-field="b.drop"></label>
    <label>Step 12: first sidelobe (dBc) <input data-field="b.sll"></label>
    </div>
13. **Restore.** Choose the **Uniform** taper again, so the next runs start
    from a known state.
::::

::::{frame} Grating Lobes and Squint
:::{present}
- Rx1, Rx4, Rx7 on, then Rx1 and Rx5: read each lobe's angle and height.
- Source to $45^\circ$: sweep at Signal BW 10 MHz, then 500 MHz.
- Check Signal BW before every squint sweep.
:::

14. **Check the reference.** Leave the source at boresight with the
    **Uniform** taper loaded, and check that the frozen uniform trace from
    Step 7 is still on the plot. If it is not, press **Start** and **Freeze**
    again: every peak drop below is read against it.
15. **Every third element.** Turn **Enforce Symmetric Taper** off, since the
    gains below are not symmetric, and choose the Grating Lobes preset. It
    leaves Rx1, Rx4, and Rx7 at 100% and the other five at 0%, so the active
    elements sit $3d = 42\ \text{mm}$ apart. Press **Start** and record the
    lobe angles, their heights against the $0^\circ$ lobe, and the peak drop
    against the frozen uniform trace. Compare each with your Part 1 row.

    <div class="rec" data-lab="L22-L23">
    <label>Step 15, Rx1, Rx4, Rx7: lobe angles <input data-field="c.147.lobes"></label>
    <label>Step 15, Rx1, Rx4, Rx7: height against the 0° lobe <input data-field="c.147.height"></label>
    <label>Step 15, Rx1, Rx4, Rx7: peak drop (dB) <input data-field="c.147.drop"></label>
    </div>
16. **Every fourth element.** Set Rx4 and Rx7 to 0% and Rx5 to 100%, so only
    Rx1 and Rx5 are on, $4d = 56\ \text{mm}$ apart, and sweep again. Record the
    same three, and compare them with your Part 1 row, including what it says
    about both ends of the plot. The measured peak drops in Steps 15 and 16 run
    about 1 dB short of the element count, even with elements fully on or off,
    for a reason that is still open, so I grade these two steps on the lobe
    angles.

    <div class="rec" data-lab="L22-L23">
    <label>Step 16, Rx1, Rx5: lobe angles <input data-field="c.15.lobes"></label>
    <label>Step 16, Rx1, Rx5: height against the 0° lobe <input data-field="c.15.height"></label>
    <label>Step 16, Rx1, Rx5: peak drop (dB) <input data-field="c.15.drop"></label>
    </div>
17. **Squint reference.** Place the HB100 at $45^\circ$ on the $1.2$ m arc and
    choose the **Uniform** taper. Set **Signal BW** to 10 MHz, press
    **Start**, record **Angle** (set to **Peak**; about $45^\circ$, the
    source), and press **Freeze**.

    <div class="rec" data-lab="L22-L23">
    <label>Step 17, Signal BW 10 MHz: Angle <input data-field="d.10.angle"></label>
    </div>
18. **Squint.** Choose the Beam Squint preset, check that **Signal BW** reads
    500 MHz, and sweep again. Record **Angle** and its shift from Step 17, and
    compare the shift with your Part 1 answer. The source has not moved; only
    the frequency the GUI computes the phases at has. Calibrate, Find HB100,
    and the Rect preset all reset Signal BW to 0, so check it before every
    squint sweep.

    <div class="rec" data-lab="L22-L23">
    <label>Step 18, Signal BW 500 MHz: Angle <input data-field="d.500.angle"></label>
    <label>Step 18: shift <input data-field="d.shift"></label>
    </div>
::::

::::{frame} Quantization and Restore
:::{present}
- HB100 to the arc's $-90^\circ$ end; the Quantization preset holds a Blackman beam at $15^\circ$.
- Sweep the source in azimuth at 7, 4, 3, then 2 bits.
- Record the strongest lobe outside the main lobe, then restore the kit.
:::

19. **Load the preset.** Put the HB100 at the arc's $-90^\circ$ end and choose
    the Quantization preset. It holds the beam at $15^\circ$ with the Blackman
    taper, so every true sidelobe sits under the noise floor and any lobe that
    rises comes from rounding, and it opens **Signal vs Time** on the Tracking
    tab.
20. **Sweep at 7 bits.** With **Use Bits** checked, set **Phase Shift Bits** to
    7, then sweep the HB100 in azimuth from $-90^\circ$ to $+90^\circ$ along the
    $1.2$ m arc, aimed at the array, in about 20 s. Record the strongest lobe
    outside the main lobe, in dBc, and where it is; write "floor" where nothing
    rises out of it. Signal vs Time records 30 s from when the mode starts, so
    begin the sweep promptly; a slower sweep runs off its end.

    <div class="rec" data-lab="L22-L23">
    <label>Step 20, 7 bits: strongest lobe (dBc) <input data-field="e.7.lobe"></label>
    <label>Step 20, 7 bits: where <input data-field="e.7.where"></label>
    </div>
21. **Sweep at 4, 3, and 2 bits.** Repeat Step 20 at each, checking the bit
    count and the Use Bits box before each sweep, and compare each trace with
    your Part 1 prediction.

    <div class="rec" data-lab="L22-L23">
    <label>Step 21, 4 bits: strongest lobe (dBc) <input data-field="e.4.lobe"></label>
    <label>Step 21, 4 bits: where <input data-field="e.4.where"></label>
    <label>Step 21, 3 bits: strongest lobe (dBc) <input data-field="e.3.lobe"></label>
    <label>Step 21, 3 bits: where <input data-field="e.3.where"></label>
    <label>Step 21, 2 bits: strongest lobe (dBc) <input data-field="e.2.lobe"></label>
    <label>Step 21, 2 bits: where <input data-field="e.2.where"></label>
    </div>
22. **Restore.** Before you leave: **Use Bits** on, Phase Shift Bits 7, Signal
    BW 10 MHz, and the **Uniform** taper.
::::

::::{frame} No Hardware?
:class: read-only

```{note}
Run the backend in simulation mode with
`python phaser_headless.py --sim` and open the same URL. The simulator places
a target at boresight, which is where the taper and grating-lobe runs need it,
so Steps 7 to 16 work unchanged; its Signal Freq is $10.525\ \text{GHz}$, so
work your predictions there. Steps 17 to 21 need a source that moves, so they
have no simulator equivalent; use your Part 1 predictions in their place.
```
::::

::::{frame} Your Part 2 Entries
:class: read-only

This frame collects every box you filled in on this page. Your entries stay in this
browser only, saved as you type. **Download my packet** writes them into Part 2
of the blank packet and saves the PDF. The download locks every field, Parts 1
and 3 included, so type those into your own copy of the packet first, then use **Fill
my own copy** and choose that file: your Parts 1 and 3 are kept, and the page
adds Part 2 to them. If you work Parts 1 and 3 on paper, download the packet
and write on the printout. Upload one PDF to Gradescope. **Export entries**
saves a small backup file you can **Import** on another laptop or after
clearing your browser. The boxes are optional: the blank packet is in the next
frame, to fill on paper or in a PDF viewer instead.

<div class="rec-summary" data-lab="L22-L23" data-pdf="../../labs/ECE444_Lab_L22_L23_TaperSquint_blank.pdf" data-file="ECE444_L22_L23_Lab"></div>
::::

::::{frame} Lab Packet
:class: read-only doc-links

The L22–L23 Lab packet is one submission for the whole lab, turned in complete before Lesson 24. It has three parts:

1. Part 1, Predict (individual, before the lab period, because you need it in class): one prediction table for each Part 2 table, at your kit's frequency, and your work for one row of each.
2. Part 2, Measure (your own kit's readings, recorded in class): the four presets, your own taper, two thinned rows, the squint pair, and four quantization sweeps.
3. Part 3, Analyze (individual, after the lab): three open prompts, each answered from your own readings.

- <a class="doc-link" href="../../labs/ECE444_Lab_L22_L23_TaperSquint_blank.pdf" target="_blank" rel="noopener">L22–L23 Lab packet (PDF)</a>
::::

::::{frame} For Part 3
:class: read-only

Part 3 is done after class with your Part 2 entries and your Part 1
predictions beside you. It asks about three comparisons:

1. The tapers: compare your taper measurements (Tables A and B) with your
   predictions, and choose a taper for this kit.
2. Grating lobes and squint: compare your grating-lobe run (Table C) and your
   squint run (Table D) with your predictions.
3. Phase bits: compare your four quantization sweeps (Table E) with each
   other and with your predictions.

I grade each answer on a claim, the evidence from your own numbers, the
reasoning that connects them, and the uncertainty. Lesson 22's
<a href="../L22-sidelobes-tapering/index.html#frame-reading-a-tapered-sweep">"Reading a Tapered Sweep"</a>
says how to read each kind of level against its reference.
::::

::::{frame} Looking Ahead
:class: read-only

Lesson 24 places a null at a chosen angle on purpose, with weights that set
both the amplitude and the phase of each element.
::::
