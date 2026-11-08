---
frame_view: true
---

# L22–L23 Lab — Tapering, Squint, and Quantization

::::{frame}
:class: title-frame

<div class="course-mark">ECE 444 · Fall 2026</div>

<h1 class="frame-title">Tapering, Squint, and Quantization</h1>

<div class="title-rule"></div>

Lesson 22's taper table and Lesson 23's three departures, measured on your kit.

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

:::{depth}
Lesson 22 ended with a table of what each taper family does: sidelobes come
down, the beam broadens, and the aperture gives up some efficiency. Today that
table goes on your kit. You will load each preset on the PHASER, sweep the
beam past the HB100, and check the measured beamwidth and peak level against
the numbers you predicted. The measurement also forces a distinction that is
easy to lose on paper — the **peak drop** you watch happen on the plot is not
the **directivity loss** the array suffers, and the gap between them
is several decibels.

The second half of the lab keeps the same kit for the three departures Lesson
23 derived: grating lobes, beam squint, and phase quantization. No taper can
fix them, because they come from the element spacing, the frequency, and the
phase shifter's resolution, not from the amplitudes a taper sets. You
measure each one against the number that lesson gave you for it.
:::
::::


::::{frame} What Lesson 22 Predicts
:::{present}
| Preset | HPBW | Peak drop | $\eta_t$ |
| :-- | :-- | :-- | :-- |
| Uniform | $13.1^\circ$ | 0 dB | 0 dB |
| Hann | $18.9^\circ$ | $-4.7$ dB | $-1.2$ dB |
| Blackman | $21.4^\circ$ | $-6.1$ dB | $-1.8$ dB |
| Chebyshev | $22.6^\circ$ | $-6.5$ dB | $-2.1$ dB |
:::

The expectation table is the prediction column for every taper measurement.
The GUI writes these amplitudes to the eight Element Gains sliders when you
press a preset button; everything else is what the sweep reads relative to a
uniform-taper reference. The beamwidths are the array factor's at
$10.443\ \text{GHz}$, the frequency of my test run; repeat them at
your own kit's Find HB100 frequency in the packet's Part 1.

| Preset | $a_n$ (%) |
| :-- | :-- |
| Uniform | 100 × 8 |
| Hann | 12, 43, 77, 100, 100, 77, 43, 12 |
| Blackman | 6, 27, 66, 100, 100, 66, 27, 6 |
| Chebyshev | 4, 23, 62, 100, 100, 62, 23, 4 |

The predictions assume each slider is linear in voltage, which the Phaser
software provides once the kit has the gain-slider fix. On an older install the
slider follows the ADAR1000's register curve, about $(\%/100)^{0.68}$ in
voltage, and every taper comes out milder: my test run read Hann at
$17.2^\circ$ and $-3.7$ dB against $18.9^\circ$ and $-4.7$ dB predicted.
::::


::::{frame} Two Numbers: Peak Drop and Taper Efficiency
:::{present}
$$
\begin{aligned}
\text{peak drop} &= 20\log_{10}\frac{\sum a_n}{N} \\
\eta_t &= \frac{\left(\sum a_n\right)^2}{N \sum a_n^2}
\end{aligned}
$$

- Hann: the plot falls $4.7$ dB; directivity falls $1.2$ dB.
- Record both, in separate columns.
:::

The peak drop is the **coherent receive-voltage loss**: at broadside the eight
element signals add in phase, so the summed voltage is proportional to
$\sum a_n$ instead of $N$, and the plotted peak falls by
$20\log_{10}(\sum a_n / N)$. That is the number the Rectangular plot shows you.
The directivity loss is the **taper efficiency**, which for the Hann preset is
$-1.2$ dB, not $-4.7$ dB. Both numbers are real and both belong in your table,
so record them in separate columns and never let one stand in for the other.
The worked Hann numbers after the steps show where the difference comes
from.
::::


::::{frame} The Floor Sets What You Can Report
:::{present}
- Tapered sidelobes drop below the noise floor: write "below the floor" and its level.
- My kit read floors from $-17$ to $-31$ dBc, setup to setup: read your own.
:::

Every level on this page is in **dBc**, decibels below the main-lobe peak of
the same trace: the plot reads dBFS, and subtracting the peak's reading from
each value, as in the L21 Lab, makes a sidelobe level mean the same thing on
every trace whatever its peak.

One measurement will refuse to give you a number. Every tapered preset pushes
its first sidelobe below the noise floor of the sweep, so the correct table
entry in those rows is "below the floor", with the floor's level beside it,
not a value read off the noise. Quoting $-28$ dBc from a trace whose floor is
at $-25$ dBc reports the noise, not the antenna.

The floor itself is not one fixed number. My test run read floors from
$-17$ to $-31$ dBc on the same kit, depending on the setup, and a wall beside
the kit raised a false lobe to $-9$ dBc. Read your own floor before you
record anything, and write it at the top of Part 2.
::::


::::{frame} The Measured Sweep for Each Preset
:class: viz-frame

:::{depth}
The widget below runs the same sweep in the browser. Start on Uniform and note
the first sidelobe near $-13$ dBc, then step through the presets and watch two
things happen at once: the main lobe widens and its peak drops, while the
sidelobes drop into the noise floor. The $\eta_t$ pill is the directivity loss, so
compare it against the peak drop pill each time — the two never agree.
:::

:::{present}
<iframe src="../../viz/taper-measurement.html"
        width="100%" height="500"
        style="border: 1px solid #cddce9; border-radius: 6px;"
        loading="lazy"
        title="Measured beam sweep for the PHASER taper presets, with element gains, HPBW, peak drop and taper efficiency">
</iframe>
:::
::::


::::{frame} Grating Lobes, Measured
:::{present}
- Every third element on, $42$ mm: lobes at $\pm 43.2^\circ$, peak $-8.5$ dB.
- Every fourth, $56$ mm: lobes at $\pm 30.9^\circ$, peak $-12.0$ dB.
- My kit: $-43.6^\circ$ and $+42.3^\circ$; $-33.0^\circ$ and $+29.8^\circ$.
:::

The taper runs measure the defect a taper can fix. Lesson 23 derived the three
that it cannot, because they come from the spacing, the frequency, and the
phase shifter's resolution rather than the amplitudes: **grating lobes**,
**beam squint**, and **phase quantization**.
The rest of the lab measures all three on the same kit, each the same way as
the tapers: predict, sweep, record. The predictions above are at $10.443\ \text{GHz}$; work yours at your
kit's own frequency.

The peak drops on hardware run about $1$ dB short of the element count
($-7.8$ and $-10.9$ dB on my kit), even with elements fully on or off. That
shortfall also shows up when the whole array is compared with its single
elements, and its cause is still open, so this step is graded on the lobe
angles.
::::


::::{frame} Squint, Measured
:::{present}
- Signal BW $500$ MHz: the GUI sets the phases $500$ MHz below the signal.
- Source at $45^\circ$: the sweep finds it at $48.0^\circ$, a $+3.0^\circ$ shift.
- My kit, source at $41.1^\circ$: $+2.5^\circ$ measured, $+2.6^\circ$ predicted.
:::

The Beam Squint preset sets **Signal BW** to $500\ \text{MHz}$, which tells the GUI to
compute the steering phases for a frequency $500\ \text{MHz}$ below the
Signal Freq and receive at the Signal Freq. That is what a signal at the edge
of a $500\ \text{MHz}$ band sees. The same phases are a slightly different
steer at the real frequency, so the whole beam moves and the sweep has to
command a larger angle to land on the source. Signal BW resets to 0 after
Calibrate, Find HB100, and the Rect preset, so check it before every squint
sweep.
::::


::::{frame} Quantization: Hold the Beam, Sweep the Source
:::{present}
- The Quantization preset: beam held at $15^\circ$, Blackman taper, Signal vs Time.
- A $15^\circ$ ramp steps $45.4^\circ$: almost on the 3- and 4-bit grids.
- So 7, 4, and 3 bits should match; 2 bits puts a lobe near $-51^\circ$.
:::

The Quantization preset holds the beam at $15^\circ$ with the Blackman taper, so every true
sidelobe is below the floor and anything that appears is the phase shifter's
doing. You sweep the HB100 in azimuth across the arc and read the level against time, at
7, 4, 3, and 2 bits. Lesson 23's widget shows why the answer depends on the
angle: a $15^\circ$ ramp steps $45.4^\circ$ per element, which rounds to the
$22.5^\circ$ and $45^\circ$ grids with errors of $3^\circ$ or less, while at
2 bits every other element is off by about $44^\circ$ and the array factor puts
a lobe near $-51^\circ$ at about $-8$ dBc. Expect the 7-, 4-, and 3-bit sweeps
to read the floor, 17 to 19 dB below the peak, and the 2-bit sweep to show that
lobe near $-51^\circ$ at about $-10$ dBc, a few dB under the array factor
because a source swept in azimuth also crosses each patch's pattern, as in the
L21 Lab. If lobes appear at 3 or 4 bits on your
kit, it is rounding more than the steering ramp; record what you see.
::::


::::{frame} Equipment and Setup
:::{present}
- The HB100 at boresight, $1.2$ m out, at patch-row height.
- Keep $\pm 40^\circ$ clear: a wall made a false lobe at $-9$ dBc.
- Bring up the kit, then tapers, grating lobes, squint, and quantization.
- Record in Tables A to E.
:::

Place the HB100 at boresight, $1.2$ m from the array face, at patch-row height
and aimed at the center of the patch row. Every taper number is a comparison
between sweeps, so the source stays put until Step 17. The $1.2$ m puts the
source beyond the array's far-field distance, $2D^2/\lambda$ with
$D = 8d = 112$ mm, which is $0.87$ m at $10.443$ GHz; closer in, the pattern
itself changes with distance. A wall beside the kit put a false lobe only
$9$ dB below the peak, and a person seated beside it left a $-17$ dBc shelf,
so keep $\pm 40^\circ$ either side clear of both.

The procedure has four parts: Steps 1 to 6 bring up the kit, Steps 7 to 13
sweep the tapers, Steps 14 to 18 measure grating lobes and squint, and Steps 19
to 22 measure quantization and restore the kit.
::::


::::{frame} Bring Up the Kit
:class: read-only

1. **Place the source.** Put the HB100 at boresight, $1.2$ m out, at patch-row
   height, and record the distance.

   <div class="rec" data-lab="L22-L23">
   <label>Step 1: distance to the source <input data-field="f.dist"></label>
   </div>
2. **Connect.** Browse to your kit's address and wait for the pill to read
   **Connected**.
3. **Calibrate the array.** Press **Calibrate** and wait for it to finish. An
   uncalibrated array carries element-to-element gain and phase errors that
   look exactly like a taper you did not ask for. If the uniform trace's two
   first sidelobes differ by more than about 2 dB in Step 8, calibrate again.
4. **Find the source.** Press **Find HB100** and record the Signal Freq it
   reports. Every prediction uses this frequency, not the nominal
   $10.525\ \text{GHz}$.

   <div class="rec" data-lab="L22-L23">
   <label>Step 4: Signal Freq <input data-field="f.sig"></label>
   </div>
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


::::{frame} No Hardware?
:class: read-only

```{note}
Run the backend in simulation mode with
`python phaser_headless.py --sim` and open the same URL. The simulator places
a target at boresight, which is where the taper runs need it, so Steps 7 to 16
work unchanged. Steps 17 to 21 need a source that moves, so they have no
simulator equivalent; use the expectation tables.
```
::::


::::{frame} Taper Runs
:class: read-only

7. **Freeze the reference.** Choose the **Uniform** taper, check that all eight
   sliders read 100%, press **Start**, and read **Peak Gain** and **Angle**
   (set to **Peak**). Press **Freeze**: this trace stays on the plot as the
   reference every peak drop is read against.
8. **Read the uniform trace.** Record the HPBW, the angles where the trace
   falls 3 dB below its own peak, the first sidelobe, and the floor. Expect
   about $13^\circ$, within a degree of the $13.1^\circ$ prediction: the sweep
   steps in $2.8125^\circ$, so the 3 dB crossings land between samples. If the
   two first sidelobes, near $\pm 22^\circ$, differ by more than about 2 dB,
   calibrate again and repeat Steps 7 and 8.

   <div class="rec" data-lab="L22-L23">
   <label>Step 8, Uniform: HPBW <input data-field="a.uni.hpbw"></label>
   <label>Step 8, Uniform: first sidelobe (dBc) <input data-field="a.uni.sll"></label>
   <label>Step 8: floor (dBc) <input data-field="f.floor"></label>
   </div>
9. **Predict Hann.** Choose the **Hann** taper and copy the eight slider values:
   12, 43, 77, 100, 100, 77, 43, 12. Predict the peak drop from
   $20\log_{10}(\sum a_n/N)$ and the HPBW, $18.9^\circ$ at
   $10.443\ \text{GHz}$ or your own from Part 1 of the packet.
10. **Sweep Hann.** Press **Start** and record the HPBW, the peak drop against
    the frozen uniform trace, and the first sidelobe, written "below the floor"
    if it is. Expect the main lobe to widen to about $19^\circ$ and the peak to
    fall about 4.7 dB, with the first sidelobes gone into the floor; on an
    older install, without the gain-slider fix, expect about $17^\circ$ and
    $-3.7$ dB.

    <div class="rec" data-lab="L22-L23">
    <label>Step 10, Hann: HPBW <input data-field="a.hann.hpbw"></label>
    <label>Step 10, Hann: peak drop (dB) <input data-field="a.hann.drop"></label>
    <label>Step 10, Hann: first sidelobe <input data-field="a.hann.sll"></label>
    </div>
11. **Blackman and Chebyshev.** Repeat Steps 9 and 10 for each, predicting
    before each sweep. Their end elements sit at 6% and 4%, so the beam widens
    past $21^\circ$ and the peak drops past 6 dB, for sidelobes that were
    already below the floor after Hann: the diminishing returns of Lesson 22.

    <div class="rec" data-lab="L22-L23">
    <label>Step 11, Blackman: HPBW <input data-field="a.black.hpbw"></label>
    <label>Step 11, Blackman: peak drop (dB) <input data-field="a.black.drop"></label>
    <label>Step 11, Blackman: first sidelobe <input data-field="a.black.sll"></label>
    <label>Step 11, Chebyshev: HPBW <input data-field="a.cheb.hpbw"></label>
    <label>Step 11, Chebyshev: peak drop (dB) <input data-field="a.cheb.drop"></label>
    <label>Step 11, Chebyshev: first sidelobe <input data-field="a.cheb.sll"></label>
    </div>
12. **Design your own taper.** With Enforce Symmetric Taper on, meet this
    specification: HPBW no wider than $17^\circ$, with the first sidelobe
    below $-20$ dBc. Start from Uniform, pull the end elements down to about
    25% to 30%, and step smoothly up to 100% in the middle; 30, 55, 90, 100 is
    a good start, and with a linear slider it predicts $16.5^\circ$, a
    $-3.3$ dB peak drop, and a first sidelobe at $-25$ dBc. Set the sliders,
    sweep, read the HPBW and sidelobe, and adjust; two or three passes get
    there. Record your final gains and the result.

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
:class: read-only

14. **Check the reference.** Leave the source at boresight with the
    **Uniform** taper loaded, and check that the frozen uniform trace from
    Step 7 is still on the plot. If it is not, press **Start** and **Freeze**
    again: every peak drop below is read against it.
15. **Every third element.** Turn **Enforce Symmetric Taper** off, since the
    gains below are not symmetric, and choose the Grating Lobes preset. It
    leaves Rx1, Rx4, and Rx7 at 100% and the other five at 0%, so the active
    elements sit $3d = 42\ \text{mm}$ apart. Press **Start** and record the
    lobe angles, their heights against the $0^\circ$ lobe, and the peak drop
    against the frozen uniform trace. Expect three lobes of the same height:
    the main lobe at $0^\circ$ and two copies near $\pm 43^\circ$.

    <div class="rec" data-lab="L22-L23">
    <label>Step 15, Rx1, Rx4, Rx7: lobe angles <input data-field="c.147.lobes"></label>
    <label>Step 15, Rx1, Rx4, Rx7: height against the 0° lobe <input data-field="c.147.height"></label>
    <label>Step 15, Rx1, Rx4, Rx7: peak drop (dB) <input data-field="c.147.drop"></label>
    </div>
16. **Every fourth element.** Set Rx4 and Rx7 to 0% and Rx5 to 100%, so only
    Rx1 and Rx5 are on, $4d = 56\ \text{mm}$ apart, and sweep again. Record the
    same three. Expect lobes near $\pm 31^\circ$, and the trace climbing to
    full height at both ends of the plot: the $m = 2$ solution needs
    $\sin\theta$ just past 1, so you see its shoulder rather than its peak.

    <div class="rec" data-lab="L22-L23">
    <label>Step 16, Rx1, Rx5: lobe angles <input data-field="c.15.lobes"></label>
    <label>Step 16, Rx1, Rx5: height against the 0° lobe <input data-field="c.15.height"></label>
    <label>Step 16, Rx1, Rx5: peak drop (dB) <input data-field="c.15.drop"></label>
    </div>

    | Elements on | $d_\text{eff}$ | Lobes at 10.443 GHz | Peak drop |
    | :-- | :-- | :-- | :-- |
    | Rx1, Rx4, Rx7 | 42 mm | $\pm 43.2^\circ$ | $-8.5$ dB |
    | Rx1, Rx5 | 56 mm | $\pm 30.9^\circ$, both ends | $-12.0$ dB |

    The measured peak drops run about 1 dB short of these, even with elements
    fully on or off, for a reason that is still open, so this step is graded
    on the lobe angles.
17. **Squint reference.** Place the HB100 at $45^\circ$ on the $1.2$ m arc and
    choose the **Uniform** taper. Set **Signal BW** to 10 MHz, press
    **Start**, record **Angle** (set to **Peak**; about $45^\circ$, the
    source), and press **Freeze**.

    <div class="rec" data-lab="L22-L23">
    <label>Step 17, Signal BW 10 MHz: Angle <input data-field="d.10.angle"></label>
    </div>
18. **Squint.** Choose the Beam Squint preset, check that **Signal BW** reads
    500 MHz, and sweep again. Record **Angle** and its shift from Step 17. The
    peak moves even though the source did not: a beam commanded to
    $\theta_c$ with its phases set at $f_0$ points at
    $\sin^{-1}[(f_0/f)\sin\theta_c]$ when the signal is at $f$, so with
    $f = 10.443$ GHz and $f_0 = 9.943$ GHz the sweep lands on a source at
    $45^\circ$ only when it commands $48.0^\circ$. Calibrate, Find HB100, and
    the Rect preset all reset Signal BW to 0, so check it before every squint
    sweep.

    <div class="rec" data-lab="L22-L23">
    <label>Step 18, Signal BW 500 MHz: Angle <input data-field="d.500.angle"></label>
    <label>Step 18: shift <input data-field="d.shift"></label>
    </div>

    | Signal BW | Angle (Peak) | Shift, calculated | Shift, measured |
    | :-- | :-- | :-- | :-- |
    | 10 MHz | $\approx 45^\circ$ | $0.05^\circ$ | reference |
    | 500 MHz | $\approx 48^\circ$ | $+3.0^\circ$ | $+2.5$ to $+3.5^\circ$ |
::::


::::{frame} Quantization and Restore
:class: read-only

19. **Load the preset.** Put the HB100 at the arc's $-90^\circ$ end and choose
    the Quantization preset. It holds the beam at $15^\circ$ with the Blackman
    taper and opens **Signal vs Time** on the Tracking tab.
20. **Sweep at 7 bits.** With **Use Bits** checked, set **Phase Shift Bits** to
    7, then sweep the HB100 in azimuth from $-90^\circ$ to $+90^\circ$ along the $1.2$ m arc,
    aimed at the array, in about 20 s. Record the strongest lobe outside the
    main lobe, and where it is; write "floor" where nothing rises out of it.
    The trace keeps the last 30 s, counted from when the mode starts, so begin
    the sweep promptly; a slower sweep runs off its end.

    <div class="rec" data-lab="L22-L23">
    <label>Step 20, 7 bits: strongest lobe (dBc) <input data-field="e.7.lobe"></label>
    <label>Step 20, 7 bits: where <input data-field="e.7.where"></label>
    </div>
21. **Sweep at 4, 3, and 2 bits.** Repeat Step 20 at each, checking the bit
    count and the box before each sweep. Lobes at 3 or 4 bits would point to
    the kit rounding more than the steering ramp; record what you see.

    <div class="rec" data-lab="L22-L23">
    <label>Step 21, 4 bits: strongest lobe (dBc) <input data-field="e.4.lobe"></label>
    <label>Step 21, 4 bits: where <input data-field="e.4.where"></label>
    <label>Step 21, 3 bits: strongest lobe (dBc) <input data-field="e.3.lobe"></label>
    <label>Step 21, 3 bits: where <input data-field="e.3.where"></label>
    <label>Step 21, 2 bits: strongest lobe (dBc) <input data-field="e.2.lobe"></label>
    <label>Step 21, 2 bits: where <input data-field="e.2.where"></label>
    </div>

    | Bits | LSB | Rule of thumb, $-6B$ dB | Expected strongest lobe outside the main lobe |
    | :-- | :-- | :-- | :-- |
    | 7 | $2.8^\circ$ | $-42$ | the floor, $-17$ to $-19$ dBc |
    | 4 | $22.5^\circ$ | $-24$ | the floor, as at 7 bits |
    | 3 | $45^\circ$ | $-18$ | the floor, as at 7 bits |
    | 2 | $90^\circ$ | $-12$ | about $-10$ dBc, near $-51^\circ$ |
22. **Restore.** Before you leave: **Use Bits** on, Phase Shift Bits 7, Signal
    BW 10 MHz, and the **Uniform** taper.
::::


::::{frame} Working the Hann Numbers
:class: read-only

Work the Hann preset all the way through. The eight amplitudes are
$a_n = 0.12,\ 0.43,\ 0.77,\ 1.00,\ 1.00,\ 0.77,\ 0.43,\ 0.12$, giving

$$\sum a_n = 4.64, \qquad \sum a_n^2 = 3.584 .$$

The plotted peak drop follows from the first sum alone:

$$
\begin{aligned}
20\log_{10}\!\left(\frac{4.64}{8}\right) &= 20\log_{10}(0.580) \\
&= -4.7\ \text{dB}.
\end{aligned}
$$

The directivity loss follows from both sums:

$$
\begin{aligned}
\eta_t &= \frac{\left(\sum a_n\right)^2}{N \sum a_n^2} = \frac{21.53}{8 \times 3.584} \\
&= 0.751 \quad \rightarrow \quad -1.2\ \text{dB}.
\end{aligned}
$$

<img src="../../viz/img/L22-two-numbers.svg"
     alt="Bar comparison: the plotted peak falls 4.7 dB while directivity falls 1.2 dB, a 3.5 dB difference"
     style="max-width: 620px; width: 100%; display: block; margin: 1em auto;">

So the trace drops 4.7 dB and the antenna loses 1.2 dB of directivity. The
remaining 3.5 dB did not go anywhere, because it was never a loss. The sweep
plots received power normalized to full scale, and the tapered array collects
less signal voltage from the source — that part is real and it is the 4.7 dB.
But the tapered array also responds to less of everything else arriving from
off-boresight, and the noise-equivalent aperture shrinks along with the signal
sum. Directivity is the ratio of on-axis intensity to the average over all
angles, and that ratio only falls by $\eta_t$. If you re-normalized each trace
to its own peak instead of to the uniform peak, the 4.7 dB would vanish from
the plot entirely and the beam shape would be unchanged.

The practical statement is short. The peak drop is a plot artifact of a
common reference; the taper efficiency is the antenna's actual loss. A system
budget that debits 4.7 dB for the taper overstates the loss by a factor of two
in power.
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

<div class="rec-summary" data-lab="L22-L23" data-pdf="../../labs/ECE444_Lab_L22_L23_TaperSquint_blank.pdf" data-file="ECE444_L22_L23_Lab"></div>
::::


::::{frame} Lab Packet
:class: read-only

The packet is the turn-in document for the whole lab: Part 1 before the period,
Part 2 in class, Part 3 after. <a href="../../labs/ECE444_Lab_L22_L23_TaperSquint_blank.pdf" target="_blank" rel="noopener">L22–L23 Lab packet (PDF)</a>.
::::


::::{frame} Summary: Tapering
:class: read-only

| Symbol / idea | What it is | Number to remember |
| :-- | :-- | :-- |
| $\sum a_n / N$ | coherent receive-voltage fraction at broadside | Hann: $4.64/8 \rightarrow -4.7$ dB |
| $\eta_t = (\sum a_n)^2/(N\sum a_n^2)$ | taper efficiency — the directivity the array loses | Hann: 0.75, or $-1.2$ dB |
| HPBW with taper | broadens as the aperture is de-weighted | $13.1^\circ$ uniform, $18.9^\circ$ Hann, $22.6^\circ$ Chebyshev |
| Floor | the limit on any sidelobe reading | $-17$ to $-31$ dBc on my kit; tapered sidelobes drop below it |
| Mild taper | most of the sidelobe benefit, little directivity lost | ends at 30%: $16.5^\circ$, $-0.7$ dB of $\eta_t$ |
::::


::::{frame} Summary: The Three Departures
:class: read-only

| Symbol / idea | What it is | Number to remember |
| :-- | :-- | :-- |
| Grating lobe | a full-height copy of the beam where $\sin\theta = m\lambda/d_\text{eff}$ is real | every third element on: $\pm 43^\circ$ |
| Beam squint | the beam moves when the signal is off the phase-set frequency | 500 MHz at $45^\circ$: $3^\circ$ |
| Phase quantization | lobes that appear when the ramp falls between grid points | 2 bits at $15^\circ$: a lobe near $-10$ dBc; 3 and 4 bits at the floor |
::::


::::{frame} Looking Ahead
:::{present}
- Turn in the packet, all three parts, before Lesson 24.
- L24 places a null on purpose; my kit measured nulls $-40$ to $-50$ dB deep.
:::

The taper runs measured the defect a taper can fix: the sidelobes came down,
and the beam widened, with a peak drop that is not the directivity you lost.
The rest of the lab measured the three it cannot. Grating lobes are the array factor doing exactly
what the geometry tells it to, squint is what setting the phases at one
frequency and receiving at another does to the beam, and quantization lobes
appear when the steering ramp falls between the shifter's grid points.
Lesson 24 turns from pattern defects to pattern control: placing a null at a
chosen angle on purpose, with weights that change both amplitude and phase.
::::
