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

:::{depth}
Lesson 24 ended with a weight vector on paper: eight complex numbers that hold
the beam on the target and put a pattern null on the interferer. Today we load
those numbers into the array and measure what the hardware gives back. The lab
runs four procedures, in increasing order of how much the array does for
itself: a static notch you compute yourself (A), a boresight null that comes
from subtracting the two digital channels (B), an adaptive beamformer that
finds its own null from the received data (C), and the same difference beam put
to a different use, measuring a target's angle from a single look (D). That last
one is where Module 4 begins.
:::
::::

::::{frame} What Lesson 24 Predicts
:::{present}
| Element | Gain (%) | Phase (deg) |
| :-- | --: | --: |
| 1 | 74 | $-12.0$ |
| 2 | 65 | $+3.5$ |
| 3 | 82 | $+13.0$ |
| 4 | 100 | $+6.0$ |
| 5 | 100 | $-6.0$ |
| 6 | 82 | $-13.0$ |
| 7 | 65 | $-3.5$ |
| 8 | 74 | $+12.0$ |
:::
:::{present}
- The main lobe drops about $2$ dB.
:::

The weight-subtraction rule of
<a href="../L24-null-steering/index.html#frame-the-weight-subtraction-rule">Lesson 24</a>
holds the beam at broadside and nulls an interferer at $\theta_1 = +22.5^\circ$:

$$
\mathbf{w} = \mathbf{w}_\text{d} - r_\text{n}\ \mathbf{w}_\text{n}, \qquad
r_\text{n} = \frac{\mathbf{w}_\text{n}^{H}\mathbf{w}_\text{d}}{\mathbf{w}_\text{n}^{H}\mathbf{w}_\text{n}} .
$$

The table converts the weights to what the GUI accepts: element gain as a
percentage of the largest, $100\vert w_n\vert/\max\vert w\vert$, and phase
offset as $\angle w_n$, entered with its sign. It is worked at $10.443$ GHz,
the frequency **Find HB100** reported for my kit.
Part 1 of the packet has you compute the same table at your own kit's
frequency; at the nominal $10.525$ GHz the outer gains read 75 % and the
phases of elements 2 and 7 read $\pm 3.1^\circ$, so the table moves only
slightly from kit to kit.

The predictions assume the Element Gains slider is linear in voltage, which it
is on current Phaser software. On my kit the main lobe dropped 2.5 dB
against the predicted 2.0.

<img src="../../viz/img/L24-element-settings.svg"
     alt="The eight element gains and phase offsets for a null at +22.5 degrees: gains symmetric about the array center, phases antisymmetric"
     style="max-width: 640px; width: 100%; display: block; margin: 1em auto;">

The gains are symmetric about the array center and the phases are
antisymmetric, the conjugate mirror pairs of
<a href="../L24-null-steering/index.html#frame-weights-on-a-circle">Lesson 24's weight circle</a>.
Neither column nulls anything on its own; only the eight weights together do.
::::

::::{frame} Why the Notch Goes Deep
:::{present}
- One-step channel errors allow a notch about $48$ dB below the uniform peak.
- Expect $46$ to $50$ dB open, $22$ to $24$ dB cramped.
- A shallow notch points to the room first: reflections, calibration, or a sign.
:::

<a href="../L24-null-steering/index.html#frame-quantization-and-null-depth">Lesson 24</a>
estimated the depth that small, independent channel errors allow, about
$48$ dB below the uniform peak, and my kit reached $46$ to $50$ dB in an open
room. Rounding the weights to the ADAR1000's $2.8125^\circ$ and 1 %
steps does not set that limit: the rounded table keeps its mirror symmetry, so
its null survives and moves only a fraction of a degree. On a freshly
calibrated kit the notch landed at $+21.7^\circ$. In a cramped space the same
table bottomed out $22$ to $24$ dB down, and so did the
difference null of the next frame: the HB100's own tone was still there in the
null, so a reflection arriving from another direction, about 22 dB below the
direct path, was filling both.

When a notch reads much shallower than $40$ dB, look at the room before the
arithmetic. A wall or a person beside the kit fills it, a stale calibration
fills it, and a sign error on the phase column moves it to $-22.5^\circ$, where
it is easy to miss.
::::

::::{frame} The Difference Beam
:::{present}
- **Beam 1 Phase** $= 180^\circ$ subtracts the two subarray channels.
- Boresight becomes a null, with peaks near $\pm 11^\circ$.
:::
:::{present}
:class: callout

A computed null sits where we solved for it; a structural null sits where the two subarrays cancel.
:::

There is a second null on this board that needs no computation at all. Each
ADAR1000 sums its four elements into one RF channel, so the PHASER hands the
Pluto two **digital subarray channels**, one for elements 1–4 and one for
elements 5–8. Adding them is the ordinary sum beam. Subtracting them, by
setting Beam 1 Phase to $180^\circ$, cancels the two halves wherever they
arrive in phase, which is boresight. The result is a null there with twin
peaks near $\pm 11^\circ$: the **monopulse difference beam**, which Procedure D
and Module 4 use for angle measurement. On my kit it measured $-41.5$ dB in
an open room and $-22$ dB in a cramped one, centered on boresight, with the
peaks at $\pm 12.0^\circ$. It needs no arithmetic, so its depth is a direct
reading of what the room lets through.

The $+22.5^\circ$ notch exists because we solved for eight weights, and it moves
only when we solve again. The boresight null exists because the two subarrays
are identical, and it stays at boresight no matter what the signal does.
::::

::::{frame} MVDR
:::{present}
$$
\mathbf{w}_\text{mvdr} = \frac{\mathbf{R}^{-1}\mathbf{s}}{\mathbf{s}^{H}\mathbf{R}^{-1}\mathbf{s}}
$$

- Minimum output power, with unit gain in the look direction $\mathbf{s}$.
- $\mathbf{R}$ is estimated from the data, so nobody supplies the interferer's angle.
:::

Procedures A and B both needed something known in advance: the interferer's
angle in A, the array's symmetry in B. The **MVDR** (minimum-variance
distortionless-response) beamformer needs neither. It estimates the covariance
of what the two channels receive over $K$ snapshots,

$$
\hat{\mathbf{R}} = \frac{1}{K}\ \mathbf{X}\mathbf{X}^{H},
$$

and solves for the weights that minimize total output power while holding unit
gain in the look direction $\mathbf{s}$. Whatever is loud and is not in the look
direction is suppressed, and the beamformer never has to be told where it is.

Unit gain means the two MVDR weights sum to 1 in the look direction, where
Manual's two weights of 1 sum to 2. The Phaser multiplies the MVDR output by 2,
the number of channels, so a target in the look direction reads the same level
under either mode and the two are compared on one scale.
::::

::::{frame} Two Limits of Two Channels
:::{present}
- Near $\pm 30^\circ$ the subarray pattern already puts the interferer 20 dB down.
- There the two channels cannot tell it from boresight, so MVDR's one null hits the target.
- Diagonal loading limits that loss; Procedure C runs at $+20^\circ$.
:::

Both limits belong to the architecture rather than to the algorithm. A
four-element subarray at $d = 14$ mm has its first null where
$\sin\theta = \lambda/4d$, about $31^\circ$, so an interferer there barely reaches
either channel and there is little left for the digital layer to remove. The
two channels sit four elements apart, so their phase difference,
$4kd\sin\theta$, runs through a full cycle across the subarray beam: a source
near $+30^\circ$ presents very nearly the same channel phase difference as one on
boresight, and the two channels cannot tell them apart. The digital layer can
only work on what the analog layer passes it, and only on directions the two
channels can distinguish.

At $+30^\circ$ both limits act at once, and the measurement shows what follows. MVDR
still spends its one null on the interferer, but to the two channels the
interferer looks like the look direction, and the HB100 sits a fraction of a
degree off it, so the null lands on the target too. On my kit the target
dropped about 10 dB, and MVDR did worse against the interferer than Manual.
**Diagonal loading** is the guard: the Phaser adds
$\delta\ \text{tr}(\hat{\mathbf{R}})/2$ to the diagonal of $\hat{\mathbf{R}}$
before inverting it, which caps how far the weights can move from Manual's. At
$\delta = 0.1$ the target loss at $+30^\circ$ fell to about 2 dB, and at
$+20^\circ$ MVDR still suppressed the interferer by about 17 dB, so Procedure C
uses $\delta = 0.1$. At $\delta = 1$ the weights stay so close to Manual's that
the suppression falls to about 5 dB.

Procedure C also uses $K = 1024$ snapshots rather than 128. At the kit's
3 MSPS, 128 samples span only four cycles of the 100 kHz offset between target
and interferer, so the two are partly correlated in each estimate of
$\hat{\mathbf{R}}$ and the null wanders from one update to the next. 1024
samples span 34 cycles; on my kit the spread of ten suppression readings
fell from about 25 dB to under 10.
::::

::::{frame} What MVDR Chooses
:class: viz-frame

:::{depth}
The widget is the two-channel digital layer on its own, with the analog
subarrays parked at boresight. Move the interferer to about $+20^\circ$ and
watch MVDR place a null on it. Then move it out toward $\pm 30^\circ$ and watch
the suppression fall away, for the two reasons on the previous frame. In the
lab you hold the beam on the target in Signal vs Time and read the
suppression from the two readout tiles under the plot. A beam-sweep trace is
the total power at each angle, interferer and target together, so it shows the
null but does not measure it.
:::

<iframe src="../../viz/mvdr-interferer.html"
        width="100%" height="489"
        style="border: 1px solid #cddce9; border-radius: 6px;"
        loading="lazy"
        title="Two-channel MVDR beamformer against an interferer">
</iframe>
::::

::::{frame} Manual Versus Adaptive
:::{present}
| | Manual null | MVDR |
| :-- | :-- | :-- |
| Needs first | the interferer's angle | nothing |
| Interferer moves | recompute eight weights | follows it |
| Nulls on this board | up to seven | one |
:::

Manual null steering has eight degrees of freedom and can place several nulls
at once, but every one of them is our arithmetic, computed for a geometry we
assumed. MVDR has two degrees of freedom on this board, one constraint and one
null, and it finds that null itself, from data, several times a second. On an
array with a digitizer behind every element, adaptive beamforming has both
advantages at once. On the PHASER we can see what the hybrid architecture
loses: the analog sums discard the per-element information before the
algorithm sees it.
::::

::::{frame} Sum and Delta
:::{present}
<img src="../../viz/img/L24-monopulse.svg"
     alt="Left: sum and delta channel levels from minus 20 to plus 20 degrees; the sum is flat at its peak while the delta passes through an exact zero on boresight. Right: the error function, zero on boresight and straight within about plus or minus 5 degrees with a slope of 0.11 per degree"
     style="max-width: 640px; width: 100%; display: block; margin: 0 auto;">
:::
:::{present}
- The sum is flat at boresight; the delta climbs out of a zero.
- Their ratio turns one look into a signed angle.
:::

Every measurement so far has come from a sweep: the array steps its commanded
angle across the field of view and records power at each step. A sweep takes
time, and a tracking radar does not have it. **Monopulse** forms both beams at
once from the two subarray channels, adding them for $\Sigma$ and subtracting
them for $\Delta$. The sum beam is flat at its peak, so its level barely changes
as the target drifts a degree off axis. The delta beam is zero on boresight and
climbs steeply out of that zero, so its level changes a great deal over the same
degree. Dividing one by the other turns that small angle into a large, readable
number.
::::

::::{frame} The Error Function
:::{present}
$$
\varepsilon(\theta) = -\ \frac{\text{Im}\lbrace \Delta\ \Sigma^{*} \rbrace}{\vert \Sigma \vert^{2}}
$$

- Zero on boresight, with opposite signs on the two sides.
- Slope $0.11$ per degree, straight within about $\pm 5^\circ$.
:::

The two subarrays sit four elements apart, so $\Delta$ arrives in quadrature
with $\Sigma$, and the useful quantity is the imaginary part of their product.
The error function is zero on boresight, positive on one side and negative on
the other, and straight within about $\pm 5^\circ$, well inside the array's
$13^\circ$ beamwidth. A target one degree off axis reads about $0.11$, and a
tracker that drives that reading back to zero holds the beam on the target far
more finely than the beamwidth alone would allow, from one look and with no
sweep.

The GUI plots a normalized form of the same comparison, taking its sign from
the phase difference between the two channels and its magnitude from the two
channel levels in dB,

$$
\text{sign}(\Delta\phi)\ \frac{\Sigma_{\text{dB}} - \Delta_{\text{dB}}}{\Sigma_{\text{dB}} + \Delta_{\text{dB}}},
$$

so the trace stays bounded and on screen however strong the target is.
::::

::::{frame} Equipment and Setup
:::{present}
- The HB100 at boresight, $1.2$ m out, at patch-row height.
- Keep $\pm 40^\circ$ of the room clear of walls and people.
- Bring up the kit, then four procedures; fill Tables A to D as you go.
:::

Place the HB100 at boresight, $1.2$ m from the array face, at patch-row height
and aimed at the center of the patch row. The notch and the difference null are
deeper than anything the earlier labs measured, so anything that reflects the
HB100's tone in from another direction fills them: keep about $\pm 40^\circ$ on
each side of boresight clear of walls and people for the whole lab.

The procedure has five parts. Steps 1 to 5 bring up the kit. Steps 6 to 10 are
Procedure A, the static notch (Table A); Steps 11 to 15 are Procedure B, the
difference null (Table B); Steps 16 to 22 are Procedure C, MVDR against an
interferer (Table C); and Steps 23 to 27 are Procedure D, tracking (Table D).
::::

::::{frame} Bring Up the Kit
:class: read-only

1. Browse to your kit's address from Lesson 17 and wait for the pill to read
   **Connected**.
2. With the HB100 at boresight, press **Find HB100** and record the Signal Freq
   it reports and your source distance. Your Part 1 table uses the frequency.
   <div class="rec" data-lab="L24">
   <label>Step 2: Signal Freq <input data-field="f.sig"></label>
   <label>Step 2: distance to the HB100 <input data-field="f.dist"></label>
   </div>
3. Press **Calibrate** and wait for it to finish, with the HB100 still at
   boresight. An uncalibrated array fills a null on its own, and a shallow
   notch would then measure the calibration rather than your weights. If the
   uniform sweep in Step 6 shows first sidelobes more than about 2 dB apart,
   calibrate again.
4. Set **Rx Gain (dB)** for an FFT peak of $-10 \pm 3$ dBFS, beam at $0^\circ$,
   and record it. Leave it there for the whole lab.
   <div class="rec" data-lab="L24">
   <label>Step 4: Rx Gain (dB) <input data-field="f.gain"></label>
   </div>
5. Check **Signal BW**. Calibrate, Find HB100, and every preset reset it to
   zero, so check it again before each sweep you record.
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

::::{frame} Procedure A: The Static Notch
:class: read-only

6. With the array uniform (Element Gains at 100 %, Phase Control reset), press
   **Start**. Read **Peak Gain** and **Angle** (set to **Peak**), then press
   **Freeze** to hold the trace as your reference. Record the level of the
   sidelobe nearest $+22.5^\circ$; expect about $-13$ dBc. If the two first
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
   angle. Expect the main lobe about 2 dB down and the notch near
   $+22^\circ$, 46 to 50 dB down in an open room. A notch much shallower than
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
14. Record the null's depth and angle, and the angles of the two peaks that
    replace the main lobe. The peaks fall on the sweep's $2.8125^\circ$ grid, so
    one grid step is the reading tolerance. The null needs no arithmetic, so
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

23. Open **Lab Presets** and choose the **Tracking** preset; its buttons respond
    only while the section is open. It sets the digital layer up to form both
    beams at once. Check **Signal BW** again, which the preset resets.
24. Set the taper to **Uniform** under Element Gains, and check that **Beam 1
    Phase** reads $0^\circ$ in Digital Beam Forming. The preset resets the phase
    but not yet the taper, and a leftover taper changes every reading below.
25. In **Plot Options**, turn on **Show Monopulse Delta Beam** and **Show
    Monopulse Error Function**.
26. On the **Rectangular** tab, press **Start**. The sum trace peaks on
    boresight and the delta trace nulls there. Record the delta null's depth and
    angle, and the angle where the error trace crosses zero.
    <div class="rec" data-lab="L24">
    <label>Step 26: delta null depth (dBc) <input data-field="d.depth"></label>
    <label>Step 26: delta null angle <input data-field="d.angle"></label>
    <label>Step 26: error-function zero crossing <input data-field="d.zero"></label>
    </div>
27. Open the **Tracking** tab and press **Start**. Its y-axis is the steering
    angle, plotted against sweep count. Move the HB100 slowly across the front
    of the array along the $1.2$ m arc. The tracker reads the error function,
    drives it back toward zero, and follows the source without sweeping. Expect
    it to follow smoothly to about $\pm 45^\circ$; past about $\pm 48^\circ$ it
    loses the source and snaps to the $\pm 90^\circ$ limits or to a sidelobe near
    $+60^\circ$ to $+70^\circ$, rather than drifting, and locks on again within
    one sweep once the source is back inside $\pm 45^\circ$. Record how far it
    followed and how it behaved when it lost the source.
    <div class="rec" data-lab="L24">
    <label>Step 27: how far it followed, and how it lost the source <input data-field="d.track"></label>
    </div>
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

<div class="rec-summary" data-lab="L24" data-pdf="../../labs/ECE444_Lab_L24_NullSteering_blank.pdf" data-file="ECE444_L24_Lab"></div>
::::

::::{frame} Lab Packet
:class: read-only

The packet is the turn-in document for the whole lab: Part 1 before the period,
Part 2 in class, Part 3 after. <a href="../../labs/ECE444_Lab_L24_NullSteering_blank.pdf" target="_blank" rel="noopener">L24 Lab packet (PDF)</a>.
::::

::::{frame} Summary
:class: read-only

| Idea | What it is | Number to remember |
| :-- | :-- | :-- |
| Weight subtraction | $\mathbf{w} = \mathbf{w}_\text{d} - r_\text{n}\mathbf{w}_\text{n}$, as gain % and phase | main lobe drops about $2$ dB for a null at $+22.5^\circ$ |
| Notch depth | set by one-step channel errors, not by rounding, until the room limits it | about $-48$ dB; my kit $-46$ to $-50$ dB open, $-22$ to $-24$ dB cramped |
| Difference beam | Beam 1 Phase $= 180^\circ$ subtracts the two channels | boresight null, peaks near $\pm 11^\circ$; my kit $-41.5$ dB open, $-22$ dB cramped |
| MVDR | $\mathbf{w} = \mathbf{R}^{-1}\mathbf{s} / (\mathbf{s}^{H}\mathbf{R}^{-1}\mathbf{s})$ from $K$ snapshots | one null from two channels; my kit about $17$ dB at $+20^\circ$, $K = 1024$, loading $0.1$ |
| Monopulse error | signed ratio of delta to sum, from one look | zero on boresight, slope $0.11$ per degree |
::::

::::{frame} Looking Ahead
:::{present}
- Turn in the packet, all three parts, before Lesson 25.
- Module 4 begins radar: the range equation puts a power budget behind this angle measurement.
:::

Lesson 25 derives the radar range equation and asks the question this module
never had to: how much power comes back from a target that transmits nothing of
its own. Everything Module 3 built, beamwidth, sidelobes, scan loss, and
steering, becomes the antenna terms in that equation, and the array you have
been sweeping becomes the front end of a radar. The monopulse pair of Procedure D
measures a target's angle from a single look, which is what a radar needs to
track something that moves; the range equation supplies the signal that feeds
it. Keep your Table D numbers: the slope of the error function near boresight
sets how finely a tracking radar can measure angle, and Module 4 returns to it.
::::
