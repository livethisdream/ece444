---
frame_view: true
---

# L24 Lab — Null Steering

::::{frame}
:class: title-frame

<div class="course-mark">ECE 444 · Fall 2026</div>

<h1 class="frame-title">Null Steering</h1>

<div class="title-rule"></div>

A computed notch, a structural null, an adaptive null, and the monopulse pair, measured on your own kit.

L24 Lab · Antennas, Phased Arrays, and Radar Systems · Dr. Neil Rogers
::::

::::{frame} Printing
:class: read-only

To print the slides, switch to present mode and print: one slide a sheet,
with room for notes. Print from read mode for the whole lesson.
::::

::::{frame} Learning Objectives

<ol class="lo-list" style="--module: '3'; counter-reset: lo 8">
  <li>I can calculate null-steering weights and implement pattern nulls on the ADALM-PHASER.</li>
</ol>
::::

::::{frame} The Big Picture
:::{present}
| Steps | Null | You set |
| :-- | :-- | :-- |
| 1–5 | (bring up) | HB100, Calibrate, Rx Gain |
| 6–10 | A: computed notch | your gains and phases |
| 11–15 | B: difference null | Beam 1 Phase |
| 16–22 | C: adaptive null | interferer, Manual, MVDR |
| 23–27 | D: monopulse pair | Tracking preset, Mode |
:::

Lesson 24 built four nulls, and today you measure each one on your kit. In Procedure A you load the gain and phase table you computed in Part 1 and sweep it. In Procedure B you subtract the two digital channels with Beam 1 Phase. In Procedure C the Phaser software adds a simulated interferer, first at $+20^\circ$ and then at $+30^\circ$, and you compare Manual with MVDR on a beam held at boresight. In Procedure D the Tracking preset forms the sum and delta beams together, and Tracking mode follows the HB100 as it moves. Step 6 freezes the uniform trace, and every level in Procedures A and B reads against its peak. Each block checks a Part 1 prediction: its readings fill one table in Part 2 of the packet, and you compare each with what you predicted.
::::

::::{frame} Predict First
:class: viz-frame

:::{depth}
Before you sweep, predict each trace, then check yourself. Choose a setting
from the list and decide, before you press **Show**, what the trace does next
to the dashed uniform pattern: where its nulls and peaks sit, how far the main
lobe drops, and, for the error trace, which side reads positive. Then show it.
Choosing another setting hides the trace again, so each guess comes first. The
widget draws the ideal array at 10.0 GHz, not at your kit's frequency, so its
numbers are close to your Part 1 values but not equal to them, and it has no
room reflections or calibration residue, so its nulls go deeper than any kit's.
:::

:::{present}
<iframe src="../../viz/null-predict.html"
        width="100%" height="473"
        style="border: 1px solid #cddce9; border-radius: 6px;"
        loading="lazy"
        title="Choose a setting from the L24 Lab, predict its pattern or error trace, then show it">
</iframe>
:::
::::

::::{frame} Bring Up the Kit
:::{present}
- HB100 at boresight, $1.2$ m out, at patch-row height.
- Keep $\pm 40^\circ$ of the room clear of walls and people.
- Find HB100, Calibrate, then set Rx Gain for a $-10$ dBFS peak.
:::

Place the HB100 at boresight, $1.2$ m from the array face, at patch-row height
and aimed at the center of the patch row. The notch and the difference null are
deeper than anything the earlier labs measured, so anything that reflects the
HB100's tone in from another direction fills them: keep about $\pm 40^\circ$ on
each side of boresight clear of walls and people for the whole lab. Lesson 24's
<a href="../L24-null-steering/index.html#frame-measured-null-depth">"Measured Null Depth"</a>
gives the depth a cramped room allows.

1. Browse to your kit's address from Lesson 17 and wait for the pill to read
   **Connected**.
2. With the HB100 at boresight, press **Find HB100** and record the Signal Freq
   it reports and your source distance. Compare it with your Part 1 frequency:
   a change of $0.08$ GHz moves the notch only about $0.2^\circ$, so keep your table.
   <div class="rec" data-lab="L24">
   <label>Step 2: Signal Freq <input data-field="f.sig"></label>
   <label>Step 2: distance to the HB100 <input data-field="f.dist"></label>
   </div>
3. Press **Calibrate** and wait for it to finish, with the HB100 still at
   boresight. An uncalibrated array fills a null on its own, and a shallow
   notch would then measure the calibration rather than your weights.
4. Set **Rx Gain (dB)** for an FFT peak of $-10 \pm 3$ dBFS, beam at $0^\circ$,
   and record it. Leave it there for the whole lab.
   <div class="rec" data-lab="L24">
   <label>Step 4: Rx Gain (dB) <input data-field="f.gain"></label>
   </div>
5. Check **Signal BW**. Calibrate, Find HB100, and every preset reset it to
   zero, so check it again before each sweep you record.
::::

::::{frame} Procedure A: The Static Notch
:::{present}
- Sweep the uniform array and freeze it as the reference.
- Type in your Part 1 gains and phases, each phase with its sign.
- Sweep again, and read the peak and the notch's depth and angle.
:::

6. With the array uniform (Element Gains at 100 %, Phase Control reset), press
   **Start**. Read **Peak Gain** and **Angle** (set to **Peak**), then press
   **Freeze** to hold the trace as your reference. Record the level of the
   sidelobe nearest $+22.5^\circ$ in dBc, its reading minus the uniform peak,
   so the frozen peak is 0 dB for every level in Procedures A and B. Compare
   it with your Table A prediction. If the two first
   sidelobes differ by more than about 2 dB, calibrate again and repeat this
   step.
   <div class="rec" data-lab="L24">
   <label>Step 6: uniform sidelobe nearest +22.5° (dBc) <input data-field="a.side"></label>
   </div>
7. Enter your Part 1 gains into **Element Gains** (Rx1 through Rx8). Leave
   **Enforce Symmetric Taper** off: the set is already symmetric, and with the
   switch on a later edit to one slider is mirrored onto its partner.
8. Enter your Part 1 phases into **Phase Control**, each with its sign, and
   check every sign before you sweep. Lesson 24's
   <a href="../L24-null-steering/index.html#frame-the-phaser-settings">"The PHASER Settings"</a>
   says where a sign error puts the notch, so look there too if Step 9 shows no
   notch where you expect it.
9. Press **Start** and read the new trace against the frozen one: the new
   **Peak Gain**, the notch's depth below the frozen peak, and the notch's
   angle, and compare each with your Table A prediction. A notch much shallower
   than your prediction points to the room first: a wall or a person beside the kit, or a
   stale calibration.
   <div class="rec" data-lab="L24">
   <label>Step 9: null-steered main-lobe peak (dB) <input data-field="a.peak"></label>
   <label>Step 9: notch bottom, below the uniform peak (dB) <input data-field="a.depth"></label>
   <label>Step 9: notch angle <input data-field="a.angle"></label>
   </div>
10. Press **Reset** in Phase Control and return Element Gains to Uniform.
::::

::::{frame} Procedure B: The Difference Null
:::{present}
- Set Mode to Manual and Beam 1 Phase to $180^\circ$.
- Sweep, and read the null and the two peaks beside it.
- Set Beam 1 Phase back to $0^\circ$.
:::

11. Open **Digital Beam Forming** and set Mode to **Manual**.
12. Leave Beam 0 Gain and Phase alone, and set **Beam 1 Phase** to $180^\circ$.
13. Press **Start**. Nothing in the analog beamformers changed; only one digital
    channel's sign did.
14. Record the null's depth below the frozen uniform peak and its angle, and
    the angles of the two peaks that replace the main lobe. The sweep steps the
    phase by one $2.8125^\circ$ LSB, about $1^\circ$ of angle here, so one
    step is the reading tolerance. Compare each reading with your Table B
    prediction.
    <div class="rec" data-lab="L24">
    <label>Step 14: null depth (dB) <input data-field="b.depth"></label>
    <label>Step 14: null angle <input data-field="b.angle"></label>
    <label>Step 14: left peak angle <input data-field="b.left"></label>
    <label>Step 14: right peak angle <input data-field="b.right"></label>
    </div>
15. Set **Beam 1 Phase** back to $0^\circ$.
::::

::::{frame} Procedure C: MVDR Against an Interferer
:::{present}
- Hold the beam on the HB100 at boresight in Signal vs Time.
- Inject a simulated interferer at $+20^\circ$; read Manual, then MVDR.
- Read the held pattern on the Rectangular tab, then repeat at $+30^\circ$.
:::

% Procedure C needs livethisdream/phaser PR #98 (MVDR measures its look
% vector; the held pattern on the Rectangular tab) and #97 on the kit. Its
% expectations at +30 deg come from that PR's simulator until a kit run.

The interferer in this procedure is simulated: the Phaser software adds a
second source, at an angle and level you choose, to the real samples the kit
receives, before the digital beamformer sees them. The target stays your HB100
at boresight. In Signal vs Time the beam is held still. The **Tracking** tab
plots the held beam's level against time, the two readout tiles under the plot,
**Interferer vs Target** and **MVDR Suppression**, give the numbers, and the
**Rectangular** tab draws the held beam's pattern against arrival angle: the
conventional pattern dashed, the weighted pattern solid, and lines at the look
direction and the interferer. Procedure C needs the current Phaser software on
your kit.

16. Set **Mode** to **Signal vs Time** with **Steer Angle** at $0^\circ$. This
    holds the beam on the target, and the readout tiles fill in only while it is
    held.
17. Open the **Interferer** pane, below Digital Beam Forming, and press
    **Inject Interferer**; the plot shows an *Interferer ON* badge. Set
    **Angle (deg)** to $+20$ and **Power (dBFS)** to $0$, its maximum, which puts
    it about 10 dB above a target read at $-10$ dBFS. Leave **Offset from
    target (kHz)** at $100$ and **Coherent with target** off.
18. In **Digital Beam Forming**, set Mode to **Manual**. In Manual the
    interferer only adds signal, and the Rectangular plot shows its line sitting
    on a sidelobe of the pattern. Watch ten updates of **Interferer vs Target**
    and **Peak Gain** and record the median of each, the middle value once
    sorted. The readings jump between updates, and the median ignores the odd
    wild one where an average would not. Compare Interferer vs Target with
    your Table C prediction.
    <div class="rec" data-lab="L24">
    <label>Step 18: Manual, Interferer vs Target (dB) <input data-field="c.man.ivt"></label>
    <label>Step 18: Manual, Peak Gain (dBFS) <input data-field="c.man.peak"></label>
    </div>
19. Set Mode to **MVDR**, Snapshots to $1024$, and Diagonal Load to $0.1$. Leave
    Steer Angle at $0^\circ$: it is MVDR's look direction. MVDR has one null to
    place, because the board has two digital channels. It places it on the
    interferer while protecting the target it measures in the look direction,
    so the target must be where the beam points. Record the medians of
    **Interferer vs Target**, **Peak Gain**, and **MVDR Suppression**. The
    suppression tile needs a Manual and an MVDR reading at the same Steer Angle;
    if it shows "--", repeat Step 18, then this step. A suppression well under
    10 dB at $+20^\circ$ points to the beam first: check that Steer Angle is
    $0^\circ$ and the HB100 still sits at boresight.
    <div class="rec" data-lab="L24">
    <label>Step 19: MVDR, Interferer vs Target (dB) <input data-field="c.mvdr.ivt"></label>
    <label>Step 19: MVDR, Peak Gain (dBFS) <input data-field="c.mvdr.peak"></label>
    <label>Step 19: MVDR Suppression (dB) <input data-field="c.mvdr.supp"></label>
    </div>
20. Open the **Rectangular** tab. Record the angle and depth of the solid
    weighted pattern's null near $+20^\circ$, and the dashed conventional
    pattern's level at the same angle. The weighted pattern changes elsewhere
    too; Lesson 24's
    <a href="../L24-null-steering/index.html#frame-what-mvdr-chooses">"What MVDR Chooses"</a>
    says what to look for.
    <div class="rec" data-lab="L24">
    <label>Step 20: MVDR null angle <input data-field="c.null.angle"></label>
    <label>Step 20: MVDR null depth (dB) <input data-field="c.null.depth"></label>
    <label>Step 20: conventional pattern at the null (dB) <input data-field="c.null.conv"></label>
    </div>
21. Move the interferer to $+30^\circ$. Record Peak Gain in Manual, then in MVDR
    at Diagonal Load $0.001$ and at $0.1$, and watch Interferer vs Target. Compare
    the Peak Gains with your Table C prediction.
    <div class="rec" data-lab="L24">
    <label>Step 21: +30°, Manual Peak Gain (dBFS) <input data-field="c.30.man"></label>
    <label>Step 21: +30°, MVDR load 0.001 Peak Gain (dBFS) <input data-field="c.30.load001"></label>
    <label>Step 21: +30°, MVDR load 0.1 Peak Gain (dBFS) <input data-field="c.30.load01"></label>
    </div>
22. Press the interferer button to turn it off, and set Mode back to
    **Manual** and **Beam Sweep**.
::::

::::{frame} Procedure D: Watch It Track
:::{present}
- Choose the Tracking preset and sweep the sum, delta, and error traces.
- Read the delta null, the error's zero, and its sign on each side.
- Choose Tracking mode, then move the HB100 and turn the kit.
:::

% Steps 26-27 need livethisdream/phaser PR #97 (closed-loop Tracking, the
% linear |delta|/|sum| error) installed on the kit; before it, Tracking was a
% plain beam sweep and the error a dB ratio.

23. Open **Lab Presets** and choose the **Tracking** preset; its buttons respond
    only while the section is open. It turns on the delta and error traces,
    sets both digital beams to $0^\circ$, and leaves the beam sweeping. Check
    **Signal BW** again, which the preset resets.
24. Check that the taper is **Uniform** under Element Gains, and that Digital
    Beam Forming reads Mode **Manual** with **Beam 0 Phase** and **Beam 1
    Phase** at $0^\circ$. MVDR forms no delta beam, so the tracker holds still
    under it.
25. On the **Rectangular** tab, press **Start**. The sum trace peaks on
    boresight and the delta trace nulls there. Record the delta null's depth in
    dBc, below the sum trace's peak, and its angle.
    <div class="rec" data-lab="L24">
    <label>Step 25: delta null depth (dBc) <input data-field="d.depth"></label>
    <label>Step 25: delta null angle <input data-field="d.angle"></label>
    </div>
26. Read the **Error** trace. It crosses zero once near boresight, where the
    beam points at the HB100. Record that angle, and the sign of the error on
    each side of it, and compare both with your Table D prediction.
    <div class="rec" data-lab="L24">
    <label>Step 26: error zero crossing <input data-field="d.zero"></label>
    <label>Step 26: sign below and above the crossing <input data-field="d.sign"></label>
    </div>
27. Choose **Tracking** from the **Mode** menu and open the **Tracking** tab,
    which plots the tracked steering angle against update number; Tracking
    mode needs the current Phaser software on your kit. The first
    update sweeps and locks on the HB100; after that each update holds the beam
    and steps it one phase LSB toward the side the error points, and the
    Rectangular plot marks where the beam sits. Move the HB100 slowly in
    azimuth along the $1.2$ m arc and watch the tracked angle follow it. If the
    beam moves away from the source instead, the kit's direction setting is
    reversed: stop and tell me. Then bring the HB100 back to boresight, turn
    the kit on its stand to $10^\circ$ and $20^\circ$ each way by the stand's
    scale, and record the tracked angle at each, once it settles.
    <div class="rec" data-lab="L24">
    <label>Step 27: how far it followed the moving HB100 <input data-field="d.track"></label>
    <label>Step 27: stand at −20°, tracked angle <input data-field="d.t.m20"></label>
    <label>Step 27: stand at −10°, tracked angle <input data-field="d.t.m10"></label>
    <label>Step 27: stand at +10°, tracked angle <input data-field="d.t.p10"></label>
    <label>Step 27: stand at +20°, tracked angle <input data-field="d.t.p20"></label>
    </div>
::::

::::{frame} No Hardware?
:class: read-only

```{note}
Run the backend in simulation mode with `python phaser_headless.py --sim`, or
use the hosted simulator, and open the same URL. The simulator places a target
at boresight, so procedures A, B, and D run as written: the weights, the notch,
the difference null, and the error function are all in its physics model. It
also carries a simulated interferer, so procedure C runs there too.
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

<div class="rec-summary" data-lab="L24" data-pdf="../../labs/ECE444_Lab_L24_NullSteering_blank.pdf" data-file="ECE444_L24_Lab"></div>
::::

::::{frame} Lab Packet
:class: read-only doc-links

The L24 Lab packet is one submission for the whole lab, turned in complete before Lesson 25. It has three parts:

1. Part 1, Predict (individual, before the lab period, because you need it in class): one prediction table for each Part 2 table, and the gains and phases you type in for Procedure A, at your kit's frequency, with your work for one row of each.
2. Part 2, Measure (your own kit's readings, recorded in class): Tables A to D, one per procedure.
3. Part 3, Analyze (individual, after the lab): three open prompts, each answered from your own readings.

- <a class="doc-link" href="../../labs/ECE444_Lab_L24_NullSteering_blank.pdf" target="_blank" rel="noopener">L24 Lab packet (PDF)</a>
::::

::::{frame} For Part 3
:class: read-only

Part 3 is done after class with your Part 2 entries and your Part 1
predictions beside you. It asks about three comparisons:

1. Three nulls: compare your notch (Table A), your difference null
   (Table B) and your delta null (Table D) with each other and with your
   predictions.
2. MVDR at two angles: compare your Manual and MVDR readings, with the
   interferer at $+20^\circ$ and at $+30^\circ$ (Table C), with your
   predictions, and say which conclusions would hold for a real interferer.
3. The tracker: compare your Table D readings, the beam sweep and the tracked
   angles, with your predictions and with the stand's scale.

I grade each answer on a claim, the evidence from your own numbers, the
reasoning that connects them, and the uncertainty. Lesson 24's
<a href="../L24-null-steering/index.html#frame-measured-null-depth">"Measured Null Depth"</a>,
<a href="../L24-null-steering/index.html#frame-two-limits-of-two-channels">"Two Limits of Two Channels"</a>
and <a href="../L24-null-steering/index.html#frame-closing-the-loop">"Closing the Loop"</a>
give the mechanisms. For alignment, Lesson 19's
<a href="../L19-direction-finding/index.html#frame-the-bearing-error-budget">"The Bearing Error Budget"</a>
sizes the error of aligning a kit by eye.
::::

::::{frame} Looking Ahead
:class: read-only

Lesson 25 begins radar: the range equation puts a power budget behind the angle your monopulse tracker measured today.
::::
