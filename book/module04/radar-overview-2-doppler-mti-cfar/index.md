---
frame_view: true
---

# Radar Overview 2 - Doppler, MTI, CFAR, and the Lab Chain

::::{frame}
:class: title-frame

<div class="course-mark">ECE 444 · Fall 2026</div>

<h1 class="frame-title">Doppler, MTI, CFAR, and the Lab Chain</h1>

<div class="title-rule"></div>

A burst of chirps measures velocity, MTI removes clutter, and CFAR sets the threshold.

Radar Overview 2 · Antennas, Phased Arrays, and Radar Systems · Dr. Neil Rogers
::::

::::{frame} Printing
:class: read-only

To print the slides, switch to present mode and print: one slide a sheet,
with room for notes. Print from read mode for the whole lesson.
::::

::::{frame} Learning Objectives

<ol class="lo-list" style="--module: '4'; counter-reset: lo 4">
  <li>I can process FMCW radar data to produce range, range-waterfall, and range-Doppler results.</li>
  <li>I can apply moving target indication (MTI) processing to distinguish moving targets from clutter.</li>
  <li>I can apply constant false-alarm rate (CFAR) processing to radar data and evaluate detection performance.</li>
  <li>I can integrate FMCW radar processing with a phased-array front-end to track a moving target.</li>
  <li>I can classify a detected target from its micro-Doppler signature and report the classifier's accuracy.</li>
</ol>

```{include} ../../_snippets/m4-strip.md
```

:::{depth}
<a href="../radar-overview-1-detection-fmcw/index.html">Overview 1</a> ended with one chirp, one FFT, and one range profile. This overview follows the rest of the processing chain that the L29–L31 Labs run. The course provides every stage in the Phaser app and in `radar_lab.py`, so the aim here is to know what each stage is for, where it sits in the chain, what its output looks like, and what each of its settings does. Each frame links to the lesson that derives it.
:::
::::

::::{frame} The Processing Chain

:::{present}
<img src="../../viz/img/overview-chain.svg" alt="The processing chain as eight boxes in two rows joined by arrows. First row: the burst of chirps, MTI, the range FFT, and the Doppler FFT. Second row: the range-Doppler map, CFAR, classify, and track. Under each box is the lab that adds it: L28 for the range FFT; L29 for MTI, the Doppler FFT, and the map; L30 for CFAR; L31 for classify and track" style="max-width: 560px; width: 100%; display: block; margin: 0 auto;">

- The first row and the map are the L28 and L29 Labs.
- CFAR then tests every cell of the map.
- The detections feed a classifier and a tracker.
:::

The figure is the whole chain, with the lab that adds each stage. The radar sends a burst of chirps. MTI, when it is on, subtracts successive chirps to remove returns that do not move. The range FFT of Overview 1 turns each chirp into a range profile, and a second FFT across the chirps measures velocity in every range cell. The next frame names the axis each of these stages works along. The result is the range-Doppler map. Two more stages follow the map: CFAR decides which cells hold a target, and the L31 Lab classifies and tracks what CFAR reports. We take the stages in the order the labs do: the map first, then MTI, CFAR, classification, and tracking.
::::

::::{frame} The Radar Data Cube

:::{present}
<img src="../../viz/img/radar-data-cube.svg" alt="The samples of one burst drawn as a cube. Across the front face, left to right, is fast time, the samples in a chirp, which gives range. Down the front face is slow time, the chirps, which gives velocity. Back into the page is channel, the two subarrays, which gives angle. The front face is ruled into rows, one per chirp, and columns, one per sample" style="max-width: 520px; width: 100%; display: block; margin: 0 auto;">
:::
:::{present}
- **Fast time** runs along one chirp; its FFT gives range.
- **Slow time** runs across the $M$ chirps, one every $T_\text{PRI}$; its FFT gives velocity.
- Channel is the kit's two subarrays; comparing them gives angle.
:::

One chirp lasts a fraction of a millisecond, which is too short to measure the velocity of anything in a room. To observe a target for longer, the radar repeats the chirp. The examples today use the teaching burst of <a href="../L29-range-doppler-mti/index.html#frame-from-one-chirp-to-a-burst">Lesson 29</a>, which no preset in the app uses: $M = 128$ chirps of 400 MHz at 10.0 GHz, one every pulse repetition interval $T_\text{PRI} = 0.4$ ms, so the burst lasts 51.2 ms.

The samples of one burst form the **radar data cube**, and each processing stage works along one of its axes. **Fast time** is the samples within one chirp, a row of the cube; the range FFT of Overview 1 runs along it. **Slow time** is the same sample of every chirp, one $T_\text{PRI}$ apart, a column of the cube; MTI and the Doppler FFT run along it. The third axis is the receive channel. The PHASER's eight elements reach the receiver as two subarrays, so the cube is two channels deep, and comparing the two gives the angle of a target, which the tracking frame uses.

<img src="../../viz/img/L29-data-matrix.svg" alt="The real part of the beat samples of the teaching burst, drawn as an image with chirp number down and sample number across. Diagonal red and blue stripes: across a row the beat oscillates about every 33 samples, and down a column it oscillates about every 62 chirps" style="max-width: 460px; width: 100%; display: block; margin: 0 auto;">

The figure above is one channel's slice of the cube for a hand at 1.5 m closing at 0.6 m/s. Across a row the beat oscillates at the rate that gives the hand's range. Down a column, the same sample of every chirp oscillates slowly, and that slow oscillation measures the hand's velocity. Every chirp has to start at the same point of its ramp for the columns to line up, and the PHASER's chirp synchronization does that.
::::

::::{frame} Range FFT Along Fast Time

:::{present}
<img src="../../viz/img/L28-range-profile.svg" alt="Power in dBFS, dB relative to the receiver's full scale, against range from minus 0.3 to 8 m for the worked chirp, with a top axis of beat frequency above the 0 m frequency from 0 to about 10.7 kHz. Three peaks: leakage at 0 m near minus 20 dBFS, a corner reflector at 2.0 m near minus 20 dBFS, and the far wall at 5.5 m near minus 31 dBFS, over a floor near minus 85 dBFS" style="max-width: 600px; width: 100%; display: block; margin: 0 auto;">
:::
:::{present}
- Each target puts one steady beat tone in a chirp; several targets sum.
- The **range FFT**, along fast time, splits the sum. Each frequency bin is a range bin.
- One chirp gives one range profile: a peak per target.
:::

The first FFT runs along fast time, within one chirp. Overview 1 showed that a target at range $R$ puts one steady tone in the chirp, the beat at $f_b = 2BR/(cT_s)$. Several targets at several ranges each add their own tone, so the samples of one chirp are a sum of tones. An FFT splits a sum of tones into its frequencies. Each frequency bin of that FFT is a range bin, because the beat is proportional to range.

The result is a **range profile**: one chirp becomes one plot of power against range bin, with a peak for every target, not a single range. The figure is the range profile from Overview 1, with three peaks for three things in the room: the leakage, a corner reflector, and the wall. The radar takes the range FFT of every chirp in the burst, so the rows of the data cube stay chirps and its columns become range bins. <a href="../L28-fmcw/index.html#frame-the-range-fft">Lesson 28</a> covers the range FFT.
::::

::::{frame} Doppler FFT Along Slow Time

:::{present}
$$
\Delta\phi = \frac{4\pi v\ T_\text{PRI}}{\lambda}, \qquad f_D = \frac{2v}{\lambda}
$$

<img src="../../viz/img/overview2-phasor-steps.svg" alt="Twelve phasors on the unit circle, each 5.8 degrees past the last: the hand's range cell from chirp 0 to chirp 11" style="max-width: min(300px, 35vw); width: 100%; display: block; margin: 0 auto;">
:::
:::{present}
- A target stays in one range bin, but its phase steps equally every chirp.
- A steady phase step is a tone in slow time, at $f_D$.
- The **Doppler FFT**, down each range column, finds it. Its bin is the velocity.
:::

The second FFT runs along slow time, down one range column of the range FFT's output. From chirp to chirp a target stays in the same range bin: at 1 m/s it moves 0.4 mm in one 0.4 ms interval, against a range bin of 0.375 m. Its range changes far too little to move it to another bin, but the phase of its bin is the round trip measured in wavelengths,

$$
\phi = -\frac{4\pi R}{\lambda},
$$

so a fraction of a millimeter changes the phase measurably. A target closing at $v$ is $v\ T_\text{PRI}$ nearer at each chirp, so its phase steps by the same amount $\Delta\phi = 4\pi v T_\text{PRI}/\lambda$ every chirp. A steady phase step is a tone in slow time, and its frequency is the Doppler shift $f_D = 2v/\lambda$ of <a href="../L26-range-resolution-doppler/index.html#frame-the-doppler-shift">Lesson 26</a>. The **Doppler FFT** down the column finds that tone, and the bin it lands in is the target's velocity. A closing target has a positive Doppler shift and an opening target a negative one. A wall does not move, so its phase does not step, and it lands in the 0 m/s bin.

For the hand closing at 0.6 m/s at a 3.0 cm wavelength, the shift is 40 Hz, and over one 0.4 ms interval the phase steps

$$
360° \times 40\ \text{Hz} \times 0.4\ \text{ms} = 5.8° .
$$

The figure draws those steps for the first twelve chirps. <a href="../L29-range-doppler-mti/index.html#frame-the-phase-from-chirp-to-chirp">Lesson 29</a> has the details.
::::

::::{frame} The Two FFTs, Step by Step
:class: viz-frame

:::{depth}
The widget runs the last two frames on one small burst with three targets: a wall at 3.0 m, a target at 1.5 m closing at 4.7 m/s, and a target at 4.5 m opening at 3.5 m/s. **Play step** animates the next step, and **Next** and **Back** jump between the finished steps.

The burst is idealized so that every step is easy to see. It keeps 32 of the teaching burst's 128 chirps and shows the first 16 range bins, each target sits at the center of a bin, and there is no noise. A measured map has a noise floor, and each target spreads over a few cells.

With 32 chirps the velocity bin is

$$
\Delta v = \frac{0.030\ \text{m}}{2\ (32)(0.4\ \text{ms})} = 1.17\ \text{m/s},
$$

four times as coarse as the full burst's 0.29 m/s, so the closing target is 4 bins from zero and the opening target 3. The closing target's Doppler shift is 312 Hz and the burst lasts 12.8 ms, so its range cell turns through four cycles in the third step. The widget draws its map with range across and velocity up; the next frame's figure is the same map turned 90°.
:::

<iframe src="../../viz/rdm-two-ffts.html"
        width="100%" height="474"
        style="border: 1px solid #cddce9; border-radius: 6px;"
        loading="lazy"
        title="A stepper through four stages on one burst: the recorded matrix, the range FFT row by row, one range column chirp by chirp, and the Doppler FFT column by column, ending in the range-Doppler map">
</iframe>
::::

::::{frame} The Range-Doppler Map

:::{present}
<img src="../../viz/img/L29-rd-map.svg" alt="A range-Doppler map of the teaching burst from 0 to 4 m in range and minus 6 to plus 6 m/s in velocity, with a color bar in dB relative to the leakage. The kit's leakage at 0 m and a wall at 2.9 m sit in the 0 m/s column. A hand at 1.5 m sits at plus 0.6 m/s, about 30 dB below the leakage. A fidget spinner at 2.1 m spreads into a comb of lines from about minus 3 to plus 3 m/s" style="max-width: 500px; width: 100%; display: block; margin: 0 auto;">
:::
:::{present}
- The **range-Doppler map** is both FFTs: range on every chirp, then Doppler down every range column.
- Frequency within a chirp is range; phase change across chirps is velocity.
- The wall is at 0 m/s; the hand at +0.6 m/s.
:::

The radar takes the range FFT of every chirp, and then the Doppler FFT down every range column of the result. Together the two passes are a two-dimensional FFT of the burst, and the result is the **range-Doppler map**: range on one axis, radial velocity on the other, and the power in each cell as the color. The figure is a map of the teaching burst for a scene like the one in the L29 Lab. The kit's leakage at 0 m and a wall at 2.9 m do not move, so both are in the 0 m/s column, and they are the strongest returns on the map. The hand at 1.5 m is at +0.6 m/s, about 30 dB below the leakage. A fidget spinner at 2.1 m has arms that move toward and away from the kit, so it spreads over a band of velocities at one range.

Positive velocity is closing. The spinner's spread is taken up on the classification frame. The Doppler FFT is also the coherent integration of Overview 1: it adds the $M$ chirps in phase for a target at each velocity. <a href="../L29-range-doppler-mti/index.html#frame-the-range-doppler-map">Lesson 29</a> describes the map and where its range cells fall.
::::

::::{frame} Velocity Cell and Limit

:::{present}
$$
\begin{aligned}
\Delta v &= \frac{\lambda}{2M\ T_\text{PRI}} = 0.29\ \text{m/s} \\
v_\text{max} &= \pm\frac{\lambda}{4\ T_\text{PRI}} = \pm 18.75\ \text{m/s}
\end{aligned}
$$
:::
:::{present}
<img src="../../viz/img/overview2-phasor-alias.svg" alt="A target whose phase advances 240 degrees a chirp, drawn on the unit circle at chirps 0 to 3; the dashed arc of plus 240 degrees and the shorter arc of minus 120 degrees reach the same point" style="max-width: min(250px, 34vw); width: 100%; display: block; margin: 0 auto;">

- More chirps make the velocity cell finer.
- A shorter $T_\text{PRI}$ raises the limit.
- Past $v_\text{max}$ a target aliases: +25 m/s reads as −12.5 m/s.
:::

The Doppler FFT observes each range cell for the length of the burst, $M\ T_\text{PRI}$, so it separates Doppler tones that differ by $1/(M\ T_\text{PRI})$. Multiplying by $\lambda/2$ converts that to the velocity cell $\Delta v$. The burst samples the phase once every $T_\text{PRI}$, so the FFT distinguishes only Doppler shifts within $\pm 1/(2T_\text{PRI})$, which gives the velocity limit $v_\text{max}$. A velocity cell is one bin of the Doppler FFT, as a range cell is one bin of the range FFT. On the teaching burst,

$$
\begin{aligned}
\Delta v &= \frac{0.030\ \text{m}}{2\ (128)(0.4\ \text{ms})} = 0.29\ \text{m/s} \\
v_\text{max} &= \pm\frac{0.030\ \text{m}}{4\ (0.4\ \text{ms})} = \pm 18.75\ \text{m/s}.
\end{aligned}
$$

That limit is the unambiguous velocity of <a href="../L26-range-resolution-doppler/index.html#frame-doppler-resolution-and-ambiguity">Lesson 26</a>, with the chirp rate as the PRF.

A target faster than the limit aliases, and the circle shows why. At +25 m/s the phase advances 240° a chirp. A step of +240° and one of −120° reach the same point on the circle, so the FFT reads them as the same phase step, and the map reports −12.5 m/s.

<img src="../../viz/img/L29-burst-choices.svg" alt="The hand's spot on the teaching burst's map three times, between 0.5 and 2.5 m and minus 3 to plus 3 m/s: with 128 chirps and 400 MHz a small spot at plus 0.6 m/s; with 32 chirps the same range height and four times as wide in velocity; with a 160 MHz chirp the same width in velocity and about 2.5 times as tall in range" style="max-width: 560px; width: 100%; display: block; margin: 0 auto;">

Each setting of the burst controls one axis of the map, and the figure above shows the hand's spot for three bursts: with 32 chirps instead of 128 it is four times as wide in velocity, and with a 160 MHz chirp it is taller in range. The number of chirps sets the velocity cell, the interval between chirps sets the velocity limit, and the bandwidth sets the range cell, $c/2B$, which is 0.375 m for 400 MHz. <a href="../L29-range-doppler-mti/index.html#frame-the-velocity-axis">Lesson 29</a> works the cases.
::::

::::{frame} Clutter and MTI

:::{present}
<img src="../../viz/img/L29-mti-maps.svg" alt="The range-Doppler map of the teaching burst three times, with one color bar in dB relative to the leakage: with no MTI, with the 2-pulse canceller, and with the 3-pulse canceller, the leakage, wall, hand, and spinner labeled in the first. With either canceller the leakage at 0 m and the wall at 2.9 m drop to the noise floor. The hand at plus 0.6 m/s is fainter with the 2-pulse canceller and drops below the color scale with the 3-pulse, together with the floor around it. The spinner's outer lines survive and its center is removed" style="max-width: 630px; width: 100%; display: block; margin: 0 auto;">

- **Clutter**, the returns that do not move, is at 0 m/s. **MTI** (moving target indication), a filter along slow time, drops it to the noise floor.
- MTI also weakens slow targets: the hand at 0.6 m/s loses 20.0 dB.
:::

The leakage, the walls, the table, and the stand return the same echo on every chirp. Radar engineers call these returns **clutter**. On the map they are at 0 m/s, and in a lab room they are the strongest returns: the leakage is 30 dB above the hand. Clutter hides slow targets, because its sidelobes in Doppler spread onto the velocities near zero, and it raises a CFAR threshold computed from the cells beside it.

**Moving target indication** (MTI) removes the clutter. The figure is the same scene with MTI off, with the 2-pulse canceller, and with the 3-pulse canceller, on one color scale. With either canceller the leakage and the wall drop to the noise floor. The hand at 0.6 m/s is fainter with the 2-pulse canceller and fainter still with the 3-pulse, and the spinner keeps the lines of its fastest arms and loses its center. <a href="../L29-range-doppler-mti/index.html#frame-clutter-at-zero-velocity">Lesson 29</a> covers the three maps.
::::

::::{frame} Pulse Cancellers

:::{present}
<img src="../../viz/img/L29-canceller.svg" alt="Power gain in dB against velocity from minus 45 to plus 45 m/s for the 2-pulse and 3-pulse cancellers on the teaching burst. Both are zero at 0 and at plus and minus 37.5 m/s, the blind speeds, and peak at plus and minus 18.75 m/s. The 3-pulse notch is wider and deeper and its peak twice as high in dB. The unambiguous window, plus and minus 18.75 m/s, is shaded, and dots mark the gains at 0.6 and 16 m/s from the table" style="max-width: 460px; width: 100%; display: block; margin: 0 auto;">
:::
:::{present}
- The 2-pulse canceller subtracts the previous chirp from each, so a fixed return cancels.
- The 3-pulse canceller subtracts twice.
- A hand at 0.6 m/s loses 20.0 dB (2-pulse) or 39.9 dB (3-pulse), and so does its noise.
:::

<img src="../../viz/img/L29-canceller-blocks.svg" alt="Block diagrams. The 2-pulse canceller: the input chirp x_m goes straight to a summer with a plus sign, and through a delay of one PRI to the summer with a minus sign, giving the output y_m. The 3-pulse canceller: two of those stages in a row" style="max-width: 460px; width: 100%; display: block; margin: 0 auto;">

The block diagrams show both cancellers. The **2-pulse canceller** subtracts the previous chirp from each chirp, sample by sample, before the FFTs. A stationary return is the same in both chirps, so it subtracts to zero. A moving target's phase has advanced between the two chirps, so some of it survives, and the faster the target, the more survives. The **3-pulse canceller** applies the same subtraction twice in a row, which removes more of everything near 0 m/s.

A canceller is a filter with a notch at 0 m/s, and a slow target is inside the notch. The plot is the gain of each canceller against velocity on the teaching burst, with dots at the hand's 0.6 m/s: the hand loses 20.0 dB through the 2-pulse canceller and 39.9 dB through the 3-pulse. The noise in the hand's own velocity cell passes through the same filter, so the hand stands as high above its own floor as before, but it is lower on the map's color scale, and in the 3-pulse map of the last frame it drops off the scale. The gain is also zero at the blind speeds, every 37.5 m/s on this burst, which nothing in the labs reaches. In the app, the MTI setting chooses off, 2-pulse, or 3-pulse. <a href="../L29-range-doppler-mti/index.html#frame-canceller-response-and-blind-speeds">Lesson 29</a> gives the canceller's gain at every velocity.
::::

::::{frame} Range-Doppler Explorer
:class: viz-frame

:::{depth}
The widget computes a map from the teaching burst: leakage at 0 m, a wall at 2.9 m, and a hand at 1.5 m whose closing speed we set, beside the canceller's gain against velocity. Change the number of chirps, and the hand's spot narrows or widens in velocity. Move the hand past +18.75 m/s, and it aliases. Turn chirp sync off, and the hand's energy spreads over the whole velocity axis. Then step through the MTI settings at a slow and a fast hand speed.
:::

<iframe src="../../viz/range-doppler-mti.html"
        width="100%" height="450"
        style="border: 1px solid #cddce9; border-radius: 6px;"
        loading="lazy"
        title="Range-Doppler map of leakage, a wall, and a moving hand on the teaching burst, with chirp count, chirp sync, and MTI, beside the canceller's gain against velocity">
</iframe>
::::

::::{frame} CFAR: A Threshold From the Neighbors

:::{present}
<img src="../../viz/img/L30-window.svg" alt="A row of range cells. The cell under test in the center is red. Two gray guard cells sit on each side of it, then four blue reference cells on each side. A bracket joins the reference cells: their average times the bias is the threshold the cell under test must cross" style="max-width: 640px; width: 100%; display: block; margin: 0 auto;">

- **CFAR** (constant false-alarm rate) detection sets each cell's threshold from its neighbors.
- **Reference** cells estimate the noise; **guard** cells keep the target out of the estimate.
- The threshold is the estimate times a **bias**.
:::

Overview 1 set the threshold from $P_{fa}$ and a known noise power, and showed that 3 dB more noise under a fixed threshold raises the false alarms a thousand times. **Constant false-alarm rate** (CFAR) processing measures the noise instead of assuming it. The detector tests one cell at a time, the **cell under test**. On each side it skips a few **guard cells**, because a target's peak spreads into its neighbors, and then it averages a block of **reference cells**. That average is the estimate of the noise power at this cell, and the threshold is the estimate multiplied by a **bias**. The window then moves one cell and the detector repeats the test, so every cell has a threshold computed from its own neighbors. Where the noise is higher, the estimate and the threshold are higher by the same factor. <a href="../L30-cfar/index.html#frame-cell-under-test-guard-and-reference">Lesson 30</a> has the details.
::::

::::{frame} The Bias and the False-Alarm Probability

:::{present}
$$
\begin{aligned}
T &= \alpha\ \hat{P}_n \\
P_{fa} &= \left(1 + \frac{\alpha}{N}\right)^{-N}
\end{aligned}
$$

- $P_{fa}$ depends on $\alpha$ and $N$, not on the noise power.
- $P_{fa} = 10^{-6}$ with $N = 32$ takes 12.4 dB; known noise took 11.4 dB.
:::
:::{present}
<img src="../../viz/img/L30-cfar-loss.svg" alt="Extra SNR needed for Pd = 0.9 at Pfa = 10 to the minus 6, against the number of reference cells on a log axis from 4 to 256. It falls from about 8 dB at 5 cells to 2.1 dB at 16 and 1.0 dB at 32, and below half a dB past about 70" style="max-width: 600px; width: 100%; display: block; margin: 0 auto;">

- Fewer reference cells need more SNR: 2.1 dB at 16, 1.0 dB at 32.
:::

With $\hat{P}_n$ the average of the $N$ reference cells, the threshold is $T = \alpha\hat{P}_n$. The bias $\alpha$ is the number we choose, and it sets the probability of false alarm. The noise power does not appear in the expression for $P_{fa}$, which is what "constant false-alarm rate" means: the false alarms stay at the design value wherever the noise level is.

For $P_{fa} = 10^{-6}$ and 32 reference cells the bias is 17.3, or 12.4 dB. Overview 1's threshold for the same $P_{fa}$ with the noise known was 11.4 dB. The extra 1.0 dB comes from estimating the noise from a finite number of cells: the estimate scatters, and a higher bias covers the times it comes out low. The figure shows what that estimate takes from detection: for $P_d = 0.9$ a target needs 1.0 dB more SNR with 32 reference cells and 2.1 dB more with 16. More reference cells bring the bias closer to 11.4 dB, but a wider window is more likely to reach cells where the noise is at a different level.

The three controls each do one thing. A higher bias gives fewer false alarms and fewer detections of weak targets. More guard cells keep a wide target out of its own estimate. More reference cells steady the estimate and make it less local. <a href="../L30-cfar/index.html#frame-the-bias-from-the-false-alarm-probability">Lesson 30</a> derives the bias.
::::

::::{frame} CFAR Explorer
:class: viz-frame

:::{depth}
The widget draws one range profile of 240 cells with the CFAR threshold over it in green. Cells from 168 on hold clutter 15 dB above the quiet noise, and triangles along the top mark five targets, dark when found and pale when missed. Noise crossings are red dots, and the widget counts them as false alarms. Start at 2 guard and 16 reference cells a side with a 12.4 dB bias. Set the guard cells to 0, and each target raises its own threshold. Lower the bias until false alarms appear. Then switch the method to greatest-of and smallest-of, which the next frame covers.
:::

<iframe src="../../viz/cfar-explorer.html"
        width="100%" height="468"
        style="border: 1px solid #cddce9; border-radius: 6px;"
        loading="lazy"
        title="CFAR threshold over a range profile with clutter and five targets, with guard, reference, bias and method controls">
</iframe>
::::

::::{frame} Greatest-Of and Smallest-Of

:::{present}
<img src="../../viz/img/L30-failures.svg" alt="Two range profiles. Left: an 18 dB target eight cells from a 24 dB target; the cell-averaging threshold rises to about 23 dB over both, above the weaker target, while the smallest-of threshold stays near 13 dB. Right: noise that rises 15 dB at cell 60; the cell-averaging threshold ramps up across the edge, and the greatest-of threshold rises earlier and stays at the clutter level" style="max-width: 760px; width: 100%; display: block; margin: 0 auto;">

- A strong target in the window hides a weaker one. **Smallest-of** keeps the lower side's average and finds it.
- A clutter edge mixes two noise levels. **Greatest-of** keeps the higher side's average and holds $P_{fa}$.
:::

Cell averaging assumes every reference cell holds noise at the same level as the cell under test. The figure shows the two common ways that fails. On the left, an 18 dB target is eight cells from a 24 dB target. The stronger target is inside the weaker one's reference window, it raises the average, and the threshold rises above the weaker target. This is **masking**. On the right, the noise rises 15 dB at the edge of a clutter region, and a window that straddles the edge averages two noise levels: the threshold is too high just before the edge and too low just past it.

Both variants average the two sides of the window separately and keep one. **Smallest-of** keeps the smaller, so a second target on one side does not raise the threshold. **Greatest-of** keeps the larger, so a cell just inside the clutter has a threshold set by the clutter. Each fixes one failure and worsens the other. <a href="../L30-cfar/index.html#frame-greatest-of-and-smallest-of">Lesson 30</a> compares the three.
::::

::::{frame} Detections From the Map

:::{present}
<img src="../../viz/img/L30-rd-detections.svg" alt="A range-Doppler map from 0 to 9 m and minus 3 to plus 3 meters per second after MTI. Red squares mark the CFAR detections: a cluster of nine cells on a walker at 6 m and plus 1.2 meters per second, a cluster of five on a hand at 2.1 m and minus 0.6 meters per second, and one cell of leftover clutter at 0 m and zero velocity" style="max-width: 620px; width: 100%; display: block; margin: 0 auto;">
:::
:::{present}
- On the map the window is a guard box inside a reference ring.
- Each detection is a range, a velocity, and an SNR.
- One target gives a cluster of detections.
- Without MTI, CFAR reports the 0 m/s clutter as targets.
:::

The range-Doppler map has two axes, so the CFAR window does too: the guard cells are a box around the cell under test, and the reference cells are the ring around that box. The figure is a simulated map after MTI, with a walker at 6.0 m and a hand at 2.1 m. The red squares are the cells CFAR declares. Each target produces a cluster of detections, because its peak spreads into the cells beside it, and the notebook reduces each cluster to its strongest cell. The output is a list of detections, each with a range, a radial velocity, and an SNR.

Without MTI, the clutter at 0 m/s is a ridge along the map. To the CFAR window that ridge is a clutter edge, and CFAR reports its cells as targets. MTI removes most of the ridge before CFAR runs, and the one square at 0 m in the figure is clutter the canceller left. <a href="../L30-cfar/index.html#frame-2d-cfar-on-the-range-doppler-map">Lesson 30</a> covers the two-dimensional window.
::::

::::{frame} Classification by Micro-Doppler

:::{present}
- **Micro-Doppler** is the Doppler of a target's moving parts.
- The walker, fan, spinner, and hand each draw a different pattern of velocity against time.
- A classifier names the target from features of that pattern.
:::
:::{present}
<img src="../../viz/img/L31-signatures.svg" alt="Simulated slow-time spectrograms over three seconds of the lesson's four example targets, each panel with its own Doppler span in hertz and, on the right, in meters per second: a walker whose torso line, dashed, sits at 73 Hz above zero with limb traces swinging 0.9 times a second; a fan with a steady band out to plus and minus 611 Hz; a spinner whose band is strongest near plus and minus 314 Hz; and a hand whose single trace swings sinusoidally through zero" style="max-width: 520px; width: 100%; display: block; margin: 0 auto;">
:::

A detection says that something is at a range and a velocity. It does not say what the target is. The parts of a target that move relative to its body, a rotor's blades or a walker's arms and legs, each have their own Doppler shift, and that is **micro-Doppler**. A **spectrogram** shows it: the Doppler FFT of one range cell taken in short windows, one after another, so that velocity is on one axis and time on the other.

The figure is the spectrogram of four example targets. A walker shows a line at the torso's speed with the limbs swinging about it once a stride. A fan shows a steady band out to the speed of its blade tips. A spinner's band is strongest near its tips (this one is a larger example than the spinner on the map, with tips at 4.7 m/s), and a waved hand draws one trace that swings through zero. The L31 Lab measures three features of each spectrogram, such as how wide the band is and how strongly it repeats, and a classifier assigns the class whose stored features are nearest. You then count how often it is right. <a href="../L31-classification-tracking/index.html#frame-four-signatures">Lesson 31</a> covers the signatures, the features, and the classifier.
::::

::::{frame} Tracking in Range and Angle

:::{present}
<div style="display: flex; flex-wrap: wrap; gap: 8px 16px; justify-content: center; align-items: center;">
<img src="../../viz/img/L31-alpha-beta.svg" alt="Range against time for eight seconds: a walker walks out from 2 to about 6.6 meters, turns, and walks back; the detections step in 0.375 meter bins around the truth; the alpha equals 0.4 track follows the truth closely through the turn, and the alpha equals 0.15 track lags it by up to 0.9 meters" style="width: clamp(200px, 40vw, 385px); height: auto;">
<img src="../../viz/img/L31-sweep-vs-mono.svg" alt="A crossing walker's bearing against time over four seconds, from minus 27 to plus 27 degrees: beam-sweep looks every 1.1 seconds, each with its 13.6 degree beam shaded, are far apart, while monopulse frames every 0.1 seconds follow the bearing closely" style="width: clamp(200px, 40vw, 385px); height: auto;">
</div>

- The **alpha-beta filter** predicts the range, then corrects toward the detection.
- At $\alpha = 0.15$ the track is smoother but lags the turn 0.9 m.
- **Monopulse** compares the two channels for the angle every 0.1 s; a sweep looks every 1.1 s.
:::

A detection list is noisy: each range is the center of a range cell, and some bursts miss the target. A **track** joins one target's detections into a single estimate of its range and velocity, burst after burst. The **alpha-beta filter** is the simplest tracker. After each burst it predicts where the target should be from its last estimate, compares the prediction with the new detection, and corrects the range by a fraction $\alpha$ of the difference and the velocity by a fraction set by $\beta$. In the first figure a walker goes out and back. The track with $\alpha = 0.4$ follows the walker through the turn, and the track with $\alpha = 0.15$ is smoother but lags the turn by up to 0.9 m.

Range comes from the FMCW processing, and angle comes from the array. **Monopulse**, from the <a href="../../module03/L24-lab-null-steering/index.html#frame-procedure-d-watch-it-track">L24 Lab</a>, compares the phases of the two subarray channels, the third axis of the data cube, in the detection's own cell, so it gives the angle in one look, with no beam sweep. The second figure is the bearing of a walker crossing the room. A beam sweep looks every 1.1 s, and the walker leaves its 13.6° beam between looks; monopulse measures the angle on every burst, 0.1 s apart on Lesson 31's example burst, and follows the walker. <a href="../L31-classification-tracking/index.html#frame-the-alpha-beta-filter">Lesson 31</a> covers both.
::::

::::{frame} Four Labs, One Report

:::{present}
| Lab | What it adds |
| :-- | :-- |
| L28 | range profile and waterfall |
| L29 | range-Doppler map, MTI |
| L30 | CFAR detections |
| L31 | classification and tracking |

- Each lab starts from the lab before it.
- The report explains the whole chain in your own words.
:::

The four labs are one processing chain, built a stage at a time. The range FFT of the L28 Lab is the first step of the L29 Lab's range-Doppler map, the L30 Lab runs CFAR on those maps, and the L31 Lab classifies and tracks what CFAR detects. The course provides the chain in the Phaser app and in `radar_lab.py`; you run it, change its settings, and explain what you see. Keep your captures, notebooks, and plots from every lab in one folder, because each lab uses the ones before it.

Each lab has a packet: you predict before class, measure in class, and analyze afterward. The packets are not the report. The <a href="../final-project/index.html">final project</a> is one report on the radar as a system, and I grade it on your explanation of why your results came out as they did.
::::

::::{frame} Looking Ahead
:class: read-only

:::{present}
- Before each lab, read the lesson half of its page and do Part 1 of its packet.
- The <a href="../L28-fmcw/index.html">L28 Lab</a> is first: it measures the 0 m frequency, the range to a target, and a walk on the range waterfall.
:::

Each of the four pages, <a href="../L28-fmcw/index.html">Lesson 28</a>, <a href="../L29-range-doppler-mti/index.html">Lesson 29</a>, <a href="../L30-cfar/index.html">Lesson 30</a>, and <a href="../L31-classification-tracking/index.html">Lesson 31</a>, has a lesson half that works every method Part 1 of its packet asks for, and a Pre-Lab frame that maps each packet table to the frame that covers it.
::::
