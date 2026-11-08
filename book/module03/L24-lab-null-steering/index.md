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
- Lesson 24: a small change to the weights puts a deep null on an interferer.
- Today you measure four nulls: your computed notch, the difference null, MVDR's null, and the monopulse pair.
:::
:::{present}
<img src="../../viz/img/L24-pattern-null.svg"
     alt="Uniform and null-steered patterns of the 8-element array at 10.0 GHz: the null-steered beam stays at broadside, 2.1 dB lower, and drops to an exact null at plus 22.5 degrees"
     style="max-width: 560px; width: 100%; display: block; margin: 0 auto;">
:::

Lesson 24 showed that eight complex weights can hold the beam on a target and put a pattern null on an interferer, for about 2 dB of main-lobe gain. Today you load your own table and measure that notch, then three more nulls in increasing order of how much the array does for itself: a null at boresight that comes from subtracting the two digital channels, an adaptive null that MVDR finds from the received data, and the same subtraction put to work measuring a target's angle from a single look. You check every reading against the prediction you made in Part 1 of the packet.
::::

::::{frame} The Flow of the Lab
:::{present}
| Steps | Task | From Part 1 |
| :-- | :-- | :-- |
| 1 to 5 | Bring up | Q1(a) |
| 6 to 10 | A: notch | Q1, Q2 |
| 11 to 15 | B: difference null | Q3 |
| 16 to 22 | C: MVDR | Q4 |
| 23 to 27 | D: monopulse | Q5 |
:::
:::{present}
<picture>
<source media="(max-width: 600px)" srcset="../../viz/img/L24-lab-sequence-narrow.svg">
<img src="../../viz/img/L24-lab-sequence.svg" alt="The four procedures of the L24 Lab, each with the trace to expect against the uniform pattern. A, Steps 6 to 10: your eight computed weights put a notch at plus 22.5 degrees. B, Steps 11 to 15: Beam 1 Phase at 180 degrees puts a null at boresight with a peak on each side. C, Steps 16 to 22: MVDR puts its one null on an interferer at plus 20 degrees. D, Steps 23 to 27: the sum and delta beams together, the delta zero on boresight." style="max-width: 100%; display: block; margin: 0 auto;">
</picture>
:::

Step 6 freezes the uniform trace, and every level in Procedures A and B reads against its peak.
::::

::::{frame} Equipment and Setup
:::{present}
- Set the HB100 at boresight, $1.2$ m out, at patch-row height.
- Keep $\pm 40^\circ$ of the room clear of walls and people.
- Fill Tables A to D in Part 2 as you go.
:::

Place the HB100 at boresight, $1.2$ m from the array face, at patch-row height
and aimed at the center of the patch row. The notch and the difference null are
deeper than anything the earlier labs measured, so anything that reflects the
HB100's tone in from another direction fills them: keep about $\pm 40^\circ$ on
each side of boresight clear of walls and people for the whole lab. Lesson 24's
"Measured Null Depth" gives the depth a cramped room allows.
::::

::::{frame} Bring Up the Kit
:class: read-only

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
:class: read-only

6. With the array uniform (Element Gains at 100 %, Phase Control reset), press
   **Start**. Read **Peak Gain** and **Angle** (set to **Peak**), then press
   **Freeze** to hold the trace as your reference. Record the level of the
   sidelobe nearest $+22.5^\circ$ in dBc, its reading minus the uniform peak,
   so the frozen peak is 0 dB for every level in Procedures A and B; expect
   about $-13$ dBc. If the two first
   sidelobes differ by more than about 2 dB, calibrate again and repeat this
   step.
   <div class="rec" data-lab="L24">
   <label>Step 6: uniform sidelobe nearest +22.5° (dBc) <input data-field="a.side"></label>
   </div>
7. Enter your Part 1 gains into **Element Gains** (Rx1 through Rx8). Leave
   **Enforce Symmetric Taper** off: the set is already symmetric, and with the
   switch on a later edit to one slider is mirrored onto its partner.
8. Enter your Part 1 phases into **Phase Control**, each with its sign. A sign
   error moves the notch to $-22.5^\circ$, where it is easy to miss.
9. Press **Start** and read the new trace against the frozen one: the new
   **Peak Gain**, the notch's depth below the frozen peak, and the notch's
   angle. Expect the main lobe about 2 dB down and the notch at
   $+22.5^\circ$, within one step, 46 to 50 dB down in an open room. A notch much shallower than
   40 dB points to the room first: a wall or a person beside the kit, or a
   stale calibration.
   <div class="rec" data-lab="L24">
   <label>Step 9: null-steered main-lobe peak (dB) <input data-field="a.peak"></label>
   <label>Step 9: notch bottom, below the uniform peak (dB) <input data-field="a.depth"></label>
   <label>Step 9: notch angle <input data-field="a.angle"></label>
   </div>
10. Press **Reset** in Phase Control and return Element Gains to Uniform.
::::

::::{frame} Procedure B: The Difference Null
:class: read-only

11. Open **Digital Beam Forming** and set Mode to **Manual**.
12. Leave Beam 0 Gain and Phase alone, and set **Beam 1 Phase** to $180^\circ$.
13. Press **Start**. Nothing in the analog beamformers changed; only one digital
    channel's sign did.
14. Record the null's depth below the frozen uniform peak and its angle, and
    the angles of the two peaks that replace the main lobe. The sweep steps the
    phase by one $2.8125^\circ$ LSB, about $1^\circ$ of angle here, so one
    step is the reading tolerance. The null needs no arithmetic, so
    its depth is a direct reading of what the room lets through.
    <div class="rec" data-lab="L24">
    <label>Step 14: null depth (dB) <input data-field="b.depth"></label>
    <label>Step 14: null angle <input data-field="b.angle"></label>
    <label>Step 14: left peak angle <input data-field="b.left"></label>
    <label>Step 14: right peak angle <input data-field="b.right"></label>
    </div>
15. Set **Beam 1 Phase** back to $0^\circ$.
::::

::::{frame} Procedure C: MVDR Against an Interferer
:class: read-only

The interferer in this procedure is simulated: the Phaser software adds a second
source, at an angle and level you choose, to the real samples the kit receives,
before the digital beamformer sees them. The target stays your HB100 at
boresight. Every number comes from the two readout tiles under the plot,
**Interferer vs Target** and **MVDR Suppression**, and from **Peak Gain**, with
the beam held on the target.

16. Set **Mode** to **Signal vs Time** with **Steer Angle** at $0^\circ$. This
    holds the beam on the target, and the readout tiles fill in only while it is
    held.
17. Open the **Interferer** pane, below Digital Beam Forming, and press
    **Inject Interferer**; it changes to *Interferer ON · click to stop*. Set
    **Angle (deg)** to $+20$ and **Power (dBFS)** to $0$, its maximum, which puts
    it about 10 dB above a target read at $-10$ dBFS. Leave **Offset from
    target (kHz)** at $100$ and **Coherent with target** off.
18. In **Digital Beam Forming**, set Mode to **Manual**. Watch ten updates of
    **Interferer vs Target** and **Peak Gain** and record the median of each,
    the middle value once sorted. The readings jump between updates, and the
    median ignores the odd wild one where an average would not. Expect
    Interferer vs Target near $-2$ dB.
    <div class="rec" data-lab="L24">
    <label>Step 18: Manual, Interferer vs Target (dB) <input data-field="c.man.ivt"></label>
    <label>Step 18: Manual, Peak Gain (dBFS) <input data-field="c.man.peak"></label>
    </div>
19. Set Mode to **MVDR**, Snapshots to $1024$, and Diagonal Load to $0.1$. Leave
    Steer Angle at $0^\circ$: it is MVDR's look direction. Record the medians of
    **Interferer vs Target**, **Peak Gain**, and **MVDR Suppression**. The
    suppression tile needs a Manual and an MVDR reading at the same Steer Angle;
    if it shows "--", repeat Step 18, then this step. Expect Interferer vs Target
    near $-18$ dB, a suppression near 17 dB. Peak Gain reads about 2 dB below
    Manual's, because in Manual it includes an interferer only 2 dB below the
    target.
    <div class="rec" data-lab="L24">
    <label>Step 19: MVDR, Interferer vs Target (dB) <input data-field="c.mvdr.ivt"></label>
    <label>Step 19: MVDR, Peak Gain (dBFS) <input data-field="c.mvdr.peak"></label>
    <label>Step 19: MVDR Suppression (dB) <input data-field="c.mvdr.supp"></label>
    </div>
20. Open the **Adaptive** tab, which appears with MVDR in Signal vs Time. Record
    the angle and depth of the null near $+20^\circ$, and the conventional
    pattern's level at the same angle. Expect the null at $19^\circ$ to
    $20^\circ$, well below the conventional pattern's $-13$ dB.
    <div class="rec" data-lab="L24">
    <label>Step 20: Adaptive null angle <input data-field="c.null.angle"></label>
    <label>Step 20: Adaptive null depth (dB) <input data-field="c.null.depth"></label>
    <label>Step 20: conventional pattern at the null (dB) <input data-field="c.null.conv"></label>
    </div>
21. Move the interferer to $+30^\circ$. Record Peak Gain in Manual, then in MVDR
    at Diagonal Load $0.001$ and at $0.1$. Expect the target about 10 dB down at
    $0.001$ and about 2 dB down at $0.1$: there the two channels cannot tell the
    interferer from the target, and loading keeps the null off it.
    <div class="rec" data-lab="L24">
    <label>Step 21: +30°, Manual Peak Gain (dBFS) <input data-field="c.30.man"></label>
    <label>Step 21: +30°, MVDR load 0.001 Peak Gain (dBFS) <input data-field="c.30.load001"></label>
    <label>Step 21: +30°, MVDR load 0.1 Peak Gain (dBFS) <input data-field="c.30.load01"></label>
    </div>
22. Press the interferer button to turn it off, and set Mode back to
    **Manual** and **Beam Sweep**.
::::

::::{frame} Procedure D: Watch It Track
:class: read-only

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
    each side of it: the kit reads a positive error when the source sits on the
    $+\theta$ side of the beam, so expect it positive at negative steer angles
    and negative at positive ones.
    <div class="rec" data-lab="L24">
    <label>Step 26: error zero crossing <input data-field="d.zero"></label>
    <label>Step 26: sign below and above the crossing <input data-field="d.sign"></label>
    </div>
27. Choose **Tracking** from the **Mode** menu and open the **Tracking** tab,
    which plots the tracked steering angle against update number. The first
    update sweeps and locks on the HB100; after that each update holds the beam
    and steps it one phase LSB toward the side the error points, and the
    Rectangular plot marks where the beam sits. Move the HB100 slowly in
    azimuth along the $1.2$ m arc and watch the tracked angle follow it. If the
    beam walks away from the source instead, the kit's direction setting is
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
of the blank packet and saves the PDF; do Parts 1 and 3 on paper or in the PDF
viewer, and upload one PDF to Gradescope. If you have already typed Part 1 into
the packet PDF, use **Fill my own copy** and choose that file instead: your Part 1
is kept, and Part 2 is added to it. Either way the result is locked, so finish
any typing in the PDF first. **Export entries** saves a small backup file you
can **Import** on another laptop or after clearing your browser. The boxes are
optional: the blank packet is in the next frame, to fill on paper or in a PDF
viewer instead.

<div class="rec-summary" data-lab="L24" data-pdf="../../labs/ECE444_Lab_L24_NullSteering_blank.pdf" data-file="ECE444_L24_Lab"></div>
::::

::::{frame} Lab Packet
:class: read-only doc-links

The L24 Lab packet is one submission for the whole lab, turned in complete before Lesson 25. It has three parts:

1. Part 1, Pre-Lab (individual, before the lab period, because you need it in class): your gain and phase table and main-lobe loss, the notch depth, the difference null's peaks, Manual's Interferer vs Target and the channel phase differences for Procedure C, and the delta null for Procedure D.
2. Part 2, Measurements (your own kit's data, recorded in class): Tables A to D, one per procedure.
3. Part 3, Writeup (individual, after the lab): reconcile the measurements with the predictions, and two analysis problems.

- <a class="doc-link" href="../../labs/ECE444_Lab_L24_NullSteering_blank.pdf" target="_blank" rel="noopener">L24 Lab packet (PDF)</a>
::::

::::{frame} For Part 3
:class: read-only

Part 3 of the packet is the writeup, done after class with your Part 2
entries beside you. Its first three questions ask:

1. How does your notch depth compare with the Part 1 estimate, and what set it on your kit?
2. Reading a null-steered sweep: the notch depth against the null-steered peak, a notch on the wrong side, and which error is large enough to move a notch $3^\circ$.
3. How did Manual and MVDR compare at $+20^\circ$, and why did the target drop at $+30^\circ$ with almost no loading?

Lesson 24's
<a href="../L24-null-steering/index.html#frame-measured-null-depth">"Measured Null Depth"</a>
and <a href="../L24-null-steering/index.html#frame-two-limits-of-two-channels">"Two Limits of Two Channels"</a>
give the mechanisms; "Closing the Loop" explains the tracker. Procedure D's
tracking needs the current Phaser software, with closed-loop Tracking,
installed on your kit. For the notch angle, and for the boresight offset the
monopulse question asks about, Lesson 19's
<a href="../L19-direction-finding/index.html#frame-the-bearing-error-budget">"The Bearing Error Budget"</a>
sizes the error of aligning a kit by eye, and the L19 Lab's
<a href="../L19-lab-fox-hunt/index.html#frame-reference-shot">"Reference Shot"</a>
checks a setup against a known angle. The two analysis problems that follow
choose between manual and adaptive nulling, and read the monopulse pair.
::::

::::{frame} Looking Ahead
:class: read-only

Lesson 25 begins radar: the range equation puts a power budget behind the angle your monopulse tracker measured today.
::::
