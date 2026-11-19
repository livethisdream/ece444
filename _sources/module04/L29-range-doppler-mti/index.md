---
frame_view: true
---

# L29 - Range-Doppler and MTI

::::{frame}
:class: title-frame read-only

<div class="course-mark">ECE 444 · Fall 2026</div>

<h1 class="frame-title">Range-Doppler and MTI</h1>

<div class="title-rule"></div>

A burst of chirps puts every target on a map of range and radial velocity, and moving target indication removes the returns that do not move.

Lesson 29 · Antennas, Phased Arrays, and Radar Systems · Dr. Neil Rogers
::::

::::{frame} Printing
:class: read-only

To print the slides, switch to present mode and print: one slide a
sheet, with room for notes. Print from read mode for the whole lesson and lab.
::::

::::{frame} Learning Objectives
:class: here-29 read-only

<ol class="lo-list" style="--module: '4'; counter-reset: lo 4">
  <li>I can process FMCW radar data to produce range, range-waterfall, and range-Doppler results.</li>
  <li>I can apply moving target indication (MTI) processing to distinguish moving targets from clutter.</li>
</ol>

```{include} ../../_snippets/m4-strip.md
```

This page is a lesson and then its lab. You read the lesson before the lab period and fill in Part 1 of the packet from it; the lab, lower on the page, is what we do in class.

The lesson has two halves, one for each objective:

1. Range-Doppler (<a href="#frame-from-one-chirp-to-a-burst">From One Chirp to a Burst</a> to <a href="#frame-short-windows-the-spectrogram">Short Windows: The Spectrogram</a>). We send a burst of chirps, take the range FFT of each chirp as in <a href="../L28-fmcw/index.html">Lesson 28</a>, and then a second FFT across the chirps. The result is the range-Doppler map, which shows every target at its range and its radial velocity.
2. MTI (<a href="#frame-clutter-at-zero-velocity">Clutter at Zero Velocity</a> to <a href="#frame-what-to-expect-at-the-kit">What to Expect at the Kit</a>). The walls, the table, and the kit's own leakage all appear at 0 m/s on that map. Moving target indication (MTI) subtracts the chirp before from each chirp, which removes them. It also weakens a slow target and strengthens a fast one, by an amount the lesson works out for each speed.

Every example on this page uses one **teaching burst**: a 10.0 GHz carrier ($\lambda = c/f_c$ = 3.0 cm), chirps of 400 MHz in 200 µs sampled at 4 MSPS, and $M$ = 128 chirps, one every $T_\text{PRI}$ = 0.4 ms. The Phaser app does not send this burst. Your kit runs the app's **Range + Velocity** preset, whose numbers the packet gives you, so every method here carries over and none of its numbers is a Part 1 answer.
::::

::::{frame} From One Chirp to a Burst
:class: read-only

In <a href="../L28-fmcw/index.html">Lesson 28</a> one chirp gave one range profile. On the teaching burst the beat rises by $2B/(cT)$ = 13.3 kHz for every meter of range, and the range cells of $\Delta R = c/2B$ = 0.375 m are $1/T$ = 5.0 kHz apart. One chirp is too short to measure velocity: by the rule of <a href="../L26-range-resolution-doppler/index.html#frame-doppler-resolution-and-ambiguity">Lesson 26</a>, 200 µs resolves frequencies 5.0 kHz apart, which corresponds to 75 m/s of velocity.

To watch the target for longer, the radar repeats the chirp. The teaching burst sends $M$ = 128 chirps, one every pulse repetition interval (PRI) of 0.4 ms, and so watches every range cell for 51.2 ms.

Velocity comes from how the echo's phase changes from one chirp to the next, so every chirp's samples must start at the same point of its ramp. The Phaser's timing engine does this, as ADI's <a href="https://analogdevicesinc.github.io/system-level/solutions/platforms/phaser/labs/chirp-sync/" target="_blank" rel="noopener">Synchronizing Radar Chirps</a> lab describes: it starts the capture and fires each chirp a fixed delay after it.

<img src="../../viz/img/L29-chirp-sync.svg" alt="Power against velocity in the range cell of a hand moving at 0.6 m/s on the teaching burst. With the chirps synchronized, one sharp peak at plus 0.6 m/s, about 40 dB above the rest. With each chirp starting at a random time, the same energy is spread over the whole velocity axis, about 21 dB down, with no peak" style="max-width: 460px; width: 100%; display: block; margin: 0 auto;">

With the chirps synchronized, the hand's energy collects into one peak at its velocity. With each chirp starting at a random time, the same energy spreads evenly over all 128 velocity cells, $10\log_{10}128$ = 21 dB lower. The hand stays at its range, but the map no longer shows its velocity.
::::

::::{frame} The Radar Data Cube
:class: read-only

<img src="../../viz/img/radar-data-cube.svg" alt="The samples of one burst drawn as a cube. Across the front face, left to right, is fast time, the samples in a chirp, which gives range. Down the front face is slow time, the chirps, which gives velocity. Back into the page is channel, the two subarrays, which gives angle. The front face is ruled into rows, one per chirp, and columns, one per sample" style="max-width: 520px; width: 100%; display: block; margin: 0 auto;">

The samples of one burst form a block with three axes, the **radar data cube**, and each axis gives the radar one coordinate of a target:

- **Fast time** runs along one chirp, the samples 0.25 µs apart on the teaching burst. Its beat frequency gives range, and the range FFT works along it.
- **Slow time** runs across the chirps, the same sample of each chirp one PRI apart. Its phase step from chirp to chirp gives velocity, and the Doppler FFT and MTI both work along it.
- Channel is the third axis. Each of the kit's two subarrays records the whole burst, and the difference between the two gives angle, which <a href="../L31-classification-tracking/index.html#frame-angle-by-monopulse">Lesson 31</a> measures by monopulse.

This lesson works on one channel, one face of the cube. The capture's `iq` array is that face, one row per chirp.

<img src="../../viz/img/L29-data-matrix.svg" alt="The real part of the beat samples of the teaching burst, drawn as an image with chirp number down and sample number across. Diagonal red and blue stripes: across a row the beat oscillates about every 33 samples, and down a column it oscillates about every 62 chirps" style="max-width: 460px; width: 100%; display: block; margin: 0 auto;">

The figure is that face for one hand at 1.5 m closing at 0.6 m/s. Across a row the beat oscillates once every 33 samples, which sets the range; down a column the same sample oscillates once every 62 chirps, which measures the velocity.
::::

::::{frame} The Phase From Chirp to Chirp
:class: read-only

After the range FFT of every row, a target appears in the same range cell of every chirp, and that cell's phase is set by the round trip in wavelengths:

$$
\phi = -\frac{4\pi R}{\lambda}.
$$

A target closing at $v$ is $v\ T_\text{PRI}$ nearer at each chirp, so its phase advances by the same step every chirp. That steady advance is a tone in slow time at the Doppler shift of <a href="../L26-range-resolution-doppler/index.html#frame-the-doppler-shift">Lesson 26</a>:

$$
f_D = \frac{2v}{\lambda}.
$$

A closing target has a positive frequency, and an opening one a negative frequency. For the teaching burst's hand closing at 0.6 m/s,

$$
\begin{aligned}
f_D &= \frac{2 \times 0.6\ \text{m/s}}{0.030\ \text{m}} = 40\ \text{Hz} \\
\Delta\phi &= 360° \times 40\ \text{Hz} \times 0.4\ \text{ms} = 5.8°\ \text{a chirp},
\end{aligned}
$$

and a hand opening at 0.9 m/s gives −60 Hz. The left of the figure draws the hand's phase stepping 5.8° a chirp. The right draws a target whose phase advances 240° a chirp, which The Velocity Axis takes up.

<img src="../../viz/img/L29-phasor.svg" alt="Left: twelve phasors on the unit circle, each 5.8 degrees past the last, the hand's range cell from chirp 0 to chirp 11. Right: a target whose phase advances 240 degrees a chirp, drawn at chirps 0 to 3; the dashed arc of plus 240 degrees and the shorter arc of minus 120 degrees reach the same point" style="max-width: 460px; width: 100%; display: block; margin: 0 auto;">
::::

::::{frame} The Range-Doppler Map
:class: read-only

<img src="../../viz/img/L29-rd-map.svg" alt="A range-Doppler map of the teaching burst from 0 to 4 m in range and minus 6 to plus 6 m/s in velocity, with a color bar in dB relative to the leakage. The kit's leakage at 0 m and a wall at 2.9 m sit in the 0 m/s column. A hand at 1.5 m sits at plus 0.6 m/s, about 30 dB below the leakage. A fidget spinner at 2.1 m spreads into a comb of lines from about minus 3 to plus 3 m/s" style="max-width: 500px; width: 100%; display: block; margin: 0 auto;">

The second FFT, down each column, finds the slow-time tone in every range cell. The result is the **range-Doppler map**: range on one axis, radial velocity on the other, and the power of each cell. Positive velocity is closing, as in <a href="../L26-range-resolution-doppler/index.html#frame-doppler-sign-convention">Lesson 26</a>, so a hand pushed toward the kit lands at positive velocity, and checking that on your own map is the first test of the velocity axis.

The figure is a map of the teaching burst for a scene like the one in the L29 Lab. The kit's leakage at 0 m and a wall at 2.9 m do not move, so both appear in the 0 m/s column, and they are the strongest returns on the map. A hand at 1.5 m closing at 0.6 m/s appears at +0.6 m/s. A fidget spinner at 2.1 m spreads into a band of velocities at one range.

A target lands in the range cell nearest it, and the cells fall where the range FFT's bins fall. The bins are $1/T$ apart in beat frequency, and the <a href="../L28-fmcw/index.html#frame-the-0-m-frequency">0 m frequency</a> $f_0$ need not fall on one, so cell $k$ is at

$$
R_k = \frac{k/T - f_0}{2B/(cT)}.
$$

The map starts at the first cell at or beyond 0 m, so a return at 0 m shows there even when a cell just below 0 m is nearer. With the teaching burst's 0 m frequency of 103 kHz, that first cell is the one at 105 kHz, 0.15 m out, and the cells run 0.15, 0.525, 0.90, … m. The leakage lands in that first cell, and the wall at 2.9 m lands in the cell at 2.78 m.

Both FFTs use a Hann window, as in <a href="../L28-fmcw/index.html#frame-windowing-the-chirp">Lesson 28</a>, so the wall's sidelobes in Doppler are 31 dB down instead of 13 dB and do not mask a slow target at the wall's range. The window also makes each target's spot about one and a half cells wide 3 dB down.
::::

::::{frame} The Velocity Axis
:class: read-only

The Doppler FFT of $M$ slow-time samples, $T_\text{PRI}$ apart, has bins $1/(M\ T_\text{PRI})$ apart, which converts with $v = f_D\lambda/2$ to the velocity resolution:

$$
\begin{aligned}
\Delta v &= \frac{\lambda}{2M\ T_\text{PRI}} \\
&= \frac{0.030\ \text{m}}{2 \times 128 \times 0.4\ \text{ms}} \\
&= 0.29\ \text{m/s}.
\end{aligned}
$$

The slow-time samples come once a PRI, so the FFT tells apart only frequencies within $\pm 1/(2T_\text{PRI})$. That sets the maximum unambiguous velocity, the $v_\text{ua}$ of <a href="../L26-range-resolution-doppler/index.html#frame-doppler-resolution-and-ambiguity">Lesson 26</a>:

$$
\begin{aligned}
v_\text{max} &= \pm\frac{\lambda}{4T_\text{PRI}} \\
&= \pm\frac{0.030\ \text{m}}{4 \times 0.4\ \text{ms}} \\
&= \pm 18.75\ \text{m/s}.
\end{aligned}
$$

A faster target aliases by the full width of the window, $2v_\text{max}$ = 37.5 m/s. At +25 m/s the phase advances 240° a chirp, which the FFT reads as −120°, as the right of the phasor figure shows, so the map reports $25 - 37.5 = -12.5$ m/s.
::::

::::{frame} Choosing the Burst
:class: read-only

| Teaching burst | $\Delta v$ (m/s) | $v_\text{max}$ (m/s) | $\Delta R$ (m) |
| :-- | --: | --: | --: |
| 128 chirps, 400 MHz | 0.29 | ±18.75 | 0.375 |
| 32 chirps | 1.17 | ±18.75 | 0.375 |
| 160 MHz chirp | 0.29 | ±18.75 | 0.94 |

<img src="../../viz/img/L29-burst-choices.svg" alt="The hand's spot on the teaching burst's map three times, between 0.5 and 2.5 m and minus 3 to plus 3 m/s: with 128 chirps and 400 MHz a small spot at plus 0.6 m/s; with 32 chirps the same range height and four times as wide in velocity; with a 160 MHz chirp the same width in velocity and about 2.5 times as tall in range" style="max-width: 560px; width: 100%; display: block; margin: 0 auto;">

Each parameter of the burst controls one axis of the map. The number of chirps $M$ sets the velocity resolution, so 32 chirps resolve 1.17 m/s. The chirp bandwidth sets the range resolution, $c/2B$, so a 160 MHz chirp widens every target from 0.375 m to 0.94 m in range. The PRI sets the velocity limit. The L29 notebook makes a shorter burst from a long one by keeping only its first $M$ chirps.

The chirp count also moves the noise floor. The provided `range_doppler` scales each FFT so that a target's level stays where it is whatever $M$ is, and the coherent gain of <a href="../L27-radar-detection/index.html#frame-integrating-pulses">Lesson 27</a> shows up as a lower floor instead. Going from $M_1$ chirps to $M_2$ raises the floor by

$$
\begin{aligned}
\Delta_\text{floor} &= 10\log_{10}\frac{M_1}{M_2} \\
&= 10\log_{10}\frac{128}{48} = 4.3\ \text{dB}
\end{aligned}
$$

when we keep 48 of the teaching burst's 128 chirps.
::::

::::{frame} A Spinner's Micro-Doppler
:class: read-only

<img src="../../viz/img/L29-spinner-cut.svg" alt="Power against velocity in the spinner's range cell, from four teaching bursts back to back (512 chirps). Edge-on, a comb of lines 0.9 m/s apart reaching out to about plus and minus 3 m/s, inside dashed marks at the tip speed, 3.14 m/s. Face-on, held 10 degrees off, only the center line and one line either side, at plus and minus 0.9 m/s" style="max-width: 460px; width: 100%; display: block; margin: 0 auto;">

A fidget spinner held edge-on, its plane of rotation along the line of sight, moves each arm toward the kit for half a turn and away for the other half. Its echo covers every velocity out to the tip speed of an arm on a radius $a$ turning at $f_\text{rev}$ revolutions a second. For the spinner in the figures, with arms 2.5 cm from the hub at 20 revolutions a second,

$$
\begin{aligned}
v_\text{tip} &= 2\pi a f_\text{rev} \\
&= 2\pi \times 0.025\ \text{m} \times 20\ \text{rev/s} = 3.14\ \text{m/s}.
\end{aligned}
$$

The hub, and the hand that holds it, are at 0 m/s. The figure is four teaching bursts back to back, whose finer cells show the lines cleanly.

Three identical arms repeat their pattern every third of a turn, so the echo's energy falls only on lines $3f_\text{rev}$ apart in Doppler:

$$
\begin{aligned}
\Delta v_\text{line} &= \frac{\lambda}{2}\ 3f_\text{rev} \\
&= \frac{0.030\ \text{m}}{2} \times 60\ \text{Hz} = 0.90\ \text{m/s}.
\end{aligned}
$$

The outermost strong line is a little inside the tip speed. Face-on, the arms move across the beam, but a hand holds the spinner some angle $\theta$ off face-on, so $\sin\theta$ of the swing reaches the line of sight. At 10° off that is $3.14 \sin 10° = 0.55$ m/s, less than one line spacing. The energy still falls only on the lines, so the band shrinks to the first line either side, ±0.90 m/s.

This is **micro-Doppler**, the Doppler of the parts of a target that move relative to its body. <a href="../L31-classification-tracking/index.html">Lesson 31</a> uses it to tell one kind of target from another.
::::

::::{frame} Short Windows: The Spectrogram
:class: read-only

<img src="../../viz/img/L29-spectrogram.svg" alt="Two spectrograms of a hand waved along the line of sight, 0.25 m either way at 1.5 Hz, velocity against time over 0.8 s, a 2,048-chirp record at the teaching burst's PRI. With a 64-chirp window the trace is a thin sinusoid stepping in coarse time steps. With a 16-chirp window it follows the motion in finer time steps but is four times as wide in velocity" style="max-width: 560px; width: 100%; display: block; margin: 0 auto;">

One map averages a target's motion over the whole burst. A **spectrogram** shows it over time: the provided `radar_lab.spectrogram` takes one range cell's slow-time signal in windows of $N_\text{win}$ chirps, each a hop of $N_\text{hop}$ chirps after the last. Each window is a short burst, so

$$
\begin{aligned}
\Delta v_\text{win} &= \frac{\lambda}{2N_\text{win}T_\text{PRI}} \\
\Delta t &= N_\text{hop}T_\text{PRI}.
\end{aligned}
$$

The figure is a hand waved for 0.8 s at the teaching burst's PRI. A 64-chirp window with a hop of 16 gives 0.59 m/s cells and a column every 6.4 ms; a 16-chirp window with a hop of 4 gives 2.34 m/s and 1.6 ms. A shorter window follows the motion more closely and blurs it more in velocity. Either way the band still reaches the target's top speed, to within a cell.
::::

::::{frame} Clutter at Zero Velocity
:class: read-only

<img src="../../viz/img/L29-mti-maps.svg" alt="The range-Doppler map of the teaching burst three times, with one color bar in dB relative to the leakage: with no MTI, with the 2-pulse canceller, and with the 3-pulse canceller, the leakage, wall, hand, and spinner labeled in the first. With either canceller the leakage at 0 m and the wall at 2.9 m drop to the noise floor. The hand at plus 0.6 m/s is fainter with the 2-pulse canceller and drops below the color scale with the 3-pulse, together with the floor around it. The spinner's outer lines survive and its center is removed" style="max-width: 640px; width: 100%; display: block; margin: 0 auto;">

The second half of the lesson is MTI, which removes the returns that do not move. The leakage from the transmit antenna into the receiver, the walls, the table, and the stand return the same echo on every chirp. Radar engineers call these returns **clutter**. On the map they appear at 0 m/s, and in a lab room they are the strongest returns: in the map figure the leakage is 30 dB above the hand.

Clutter hides slow targets. Its Doppler sidelobes, and any small change in it from chirp to chirp, spread its energy onto the velocities near zero where a slow target is. The CFAR detector of <a href="../L30-cfar/index.html">Lesson 30</a> also sets its threshold from the cells around each cell, so a clutter ridge raises the threshold beside it. **Moving target indication** (MTI) removes the clutter before the range and Doppler FFTs.

The figure is the scene of the map figure with MTI off, with the 2-pulse canceller, and with the 3-pulse canceller, on one color scale. What to Expect at the Kit explains each change.
::::

::::{frame} Pulse Cancellers
:class: read-only

<img src="../../viz/img/L29-chain.svg" alt="The processing chain as five boxes in a row: the burst of chirps, MTI, the range FFT of each chirp, the Doppler FFT of each range cell, and the range-Doppler map. The MTI box is highlighted and labeled off, 2-pulse, or 3-pulse" style="max-width: 560px; width: 100%; display: block; margin: 0 auto;">

MTI comes before the range and Doppler FFTs. The app's MTI setting and the notebook's `KIND` choose one of three: off, the 2-pulse canceller, or the 3-pulse canceller.

The **2-pulse canceller** subtracts the chirp before from each chirp, sample by sample. A stationary return is the same in both chirps, so it subtracts to zero; a moving target's phase has advanced between them, so it survives. The **3-pulse canceller** applies the same subtraction twice in a row, which removes more of everything near 0 m/s. ADI's <a href="https://analogdevicesinc.github.io/system-level/solutions/platforms/phaser/labs/radar-mti/" target="_blank" rel="noopener">MTI Radar Processing</a> lab uses the same two filters.

<img src="../../viz/img/L29-canceller-blocks.svg" alt="Block diagrams. The 2-pulse canceller: the input chirp x_m goes straight to a summer with a plus sign, and through a delay of one PRI to the summer with a minus sign, giving the output y_m. The 3-pulse canceller: two of those stages in a row" style="max-width: 460px; width: 100%; display: block; margin: 0 auto;">

The subtraction removes clutter only as well as each chirp repeats the last. On the course's recorded bursts every chirp repeats exactly, and the wall drops more than 100 dB. On a kit, chirp-to-chirp timing jitter and changes in the room limit the drop.
::::

::::{frame} Canceller Response and Blind Speeds
:class: read-only

<img src="../../viz/img/L29-canceller.svg" alt="Power gain in dB against velocity from minus 45 to plus 45 m/s for the 2-pulse and 3-pulse cancellers on the teaching burst. Both are zero at 0 and at plus and minus 37.5 m/s, the blind speeds, and peak at plus and minus 18.75 m/s. The 3-pulse notch is wider and deeper and its peak twice as high in dB. The unambiguous window, plus and minus 18.75 m/s, is shaded, and dots mark the gains at 0.6 and 16 m/s from the table" style="max-width: 460px; width: 100%; display: block; margin: 0 auto;">

Between two chirps a target's phase advances by $2\pi f_D T_\text{PRI}$, and the difference of two equal phasors that far apart has a power gain of

$$
\vert H_2\vert^2 = 4\sin^2\left(\pi f_D T_\text{PRI}\right).
$$

The 3-pulse canceller is two of these in a row, so its gain in dB is twice the 2-pulse gain. On the teaching burst, with the dots in the figure:

| Target | $f_D T_\text{PRI}$ | 2-pulse | 3-pulse |
| :-- | --: | --: | --: |
| hand at 0.6 m/s | 0.016 | −20.0 dB | −39.9 dB |
| fast target at 16 m/s | 0.427 | +5.8 dB | +11.6 dB |

A slow target is deep in the notch at 0 m/s. A fast one near $\pm v_\text{max}$ comes out stronger than it went in.

The gain is also zero wherever $f_D T_\text{PRI}$ is a whole number $k$: the phase then advances a whole number of turns a chirp, and the canceller removes the target as it removes clutter. Those are the **blind speeds**,

$$
v_\text{blind} = k\ \frac{\lambda}{2T_\text{PRI}},
$$

every 37.5 m/s for the teaching burst, twice $v_\text{max}$; a target there aliases to 0 m/s. Nothing in the L29 Lab moves that fast.
::::

::::{frame} What to Expect at the Kit
:class: read-only

MTI changes each return in the lab by the canceller's gain at that return's speed:

- The leakage and the wall drop to the noise floor, as far as the timing allows.
- A pushed hand drops by the gain at its speed, −20.0 dB with the 2-pulse canceller at 0.6 m/s on the teaching burst, and twice that in dB with the 3-pulse.
- The noise floor passes through the same filter. The noise in the hand's own velocity cell drops with the hand, so the hand stands as high above its own floor as it did without MTI. Toward $\pm v_\text{max}$ the floor rises by the canceller's gain there.
- A spinner keeps the lines of its fastest arms and loses its center.

A hand held still, or moved across the beam, still has a small radial speed. That speed stays below its peak most of the time, so the gain at the peak speed is the least the canceller removes. A motion $A\sin(2\pi f t)$ along the line of sight, such as a tremor, peaks at $2\pi A f$. For a tremor of 1 mm either way at 2 Hz,

$$
\begin{aligned}
v_\text{peak} &= 2\pi A f = 2\pi \times 1\ \text{mm} \times 2\ \text{Hz} = 12.6\ \text{mm/s} \\
f_D &= \frac{2v_\text{peak}}{\lambda} = 0.84\ \text{Hz} \\
\vert H_2\vert^2 &= 4\sin^2\left(\pi \times 0.84\ \text{Hz} \times 0.4\ \text{ms}\right) = -53.5\ \text{dB}.
\end{aligned}
$$

<img src="../../viz/img/L29-hand-moves.svg" alt="Two sketches of the kit and a hand: pushed and pulled along the line of sight, and moved across the beam, which gives it almost no radial speed" style="max-width: 420px; width: 100%; display: block; margin: 0 auto;">

A hand moved a distance $x = A\sin(2\pi f t)$ to the side at range $R_0$ changes its range only by

$$
\Delta R \approx \frac{x^2}{2R_0},
$$

so its radial speed peaks at

$$
v_\text{peak} = \frac{\pi A^2 f}{R_0}.
$$

For 0.15 m either way at 1 Hz, 1.5 m out, that is 0.047 m/s, 3.1 Hz, and −42.1 dB. Both drop far more than the pushed hand at 0.6 m/s.

With strong clutter and fast targets, the 3-pulse canceller gives the cleanest map; for a slow hand, the 2-pulse canceller or none keeps more of the target.
::::

::::{frame} Range-Doppler Explorer
:class: viz-frame read-only

The widget computes a map from the teaching burst: leakage at 0 m, a wall at 2.9 m, and a hand at 1.5 m whose closing speed you set, beside the canceller's gain against velocity. Change the number of chirps and watch the hand's spot and the floor. Move the hand past +18.75 m/s and watch it alias. Turn chirp sync off, then step through the MTI settings at a few speeds.

<iframe src="../../viz/range-doppler-mti.html"
        width="100%" height="450"
        style="border: 1px solid #cddce9; border-radius: 6px;"
        loading="lazy"
        title="Range-Doppler map of leakage, a wall, and a moving hand on the teaching burst, with chirp count, chirp sync, and MTI, beside the canceller's gain against velocity">
</iframe>
::::

::::{frame} Summary
:class: read-only

| Range-Doppler | Relation | Teaching burst |
| :-- | :-- | :-- |
| Doppler shift | $f_D = 2v/\lambda$, positive closing | 40 Hz at 0.6 m/s |
| Range cells | $R_k = (k/T - f_0)/(2B/cT)$, from the first at or beyond 0 m | 0.15 m first, at $f_0$ = 103 kHz |
| Range resolution | $\Delta R = c/2B$ | 0.375 m; 0.94 m at 160 MHz |
| Velocity resolution | $\Delta v = \lambda/(2M\ T_\text{PRI})$ | 0.29 m/s; 1.17 m/s at 32 chirps |
| Maximum velocity | $v_\text{max} = \pm\lambda/(4T_\text{PRI})$ | ±18.75 m/s |
| Floor and $M$ | $10\log_{10}$ of the chirp ratio | +4.3 dB keeping 48 of 128 |
| Spinner | edge at $\pm 2\pi a f_\text{rev}$, lines $3f_\text{rev}$ apart | ±3.14 m/s and 0.90 m/s |
| Spectrogram | cell $\lambda/(2N_\text{win}T_\text{PRI})$, columns $N_\text{hop}T_\text{PRI}$ apart | 0.59 m/s and 6.4 ms |

| MTI | Relation | Teaching burst |
| :-- | :-- | :-- |
| 2-pulse canceller | gain $4\sin^2(\pi f_D T_\text{PRI})$ | −20.0 dB at 0.6 m/s, +5.8 dB at 16 m/s |
| 3-pulse canceller | twice the 2-pulse gain in dB | −39.9 dB at 0.6 m/s, +11.6 dB at 16 m/s |
| Nearly still | gain at the peak radial speed, $2\pi A f$ or $\pi A^2 f/R_0$ | tremor −53.5 dB; across the beam −42.1 dB |
| Blind speeds | $v_\text{blind} = k\lambda/(2T_\text{PRI})$ | every 37.5 m/s |
::::

::::{frame} Pre-Lab
:class: read-only

Part 1 of the <a href="../../labs/ECE444_Lab_L29_RangeDoppler_blank.pdf" target="_blank" rel="noopener">L29 Lab packet</a> is the shaded Predicted cells of its tables, worked at the Range + Velocity preset's numbers, which the packet gives. The lesson above works each method on the teaching burst:

| Packet table | Predict | Method | Checked in |
| :-- | :-- | :-- | :-- |
| A, the static scene | where the leakage and the wall land | <a href="#frame-the-range-doppler-map">The Range-Doppler Map</a> | Step 4 |
| B, a hand | the velocity and Doppler of a push and a pull | <a href="#frame-the-phase-from-chirp-to-chirp">The Phase From Chirp to Chirp</a> | Steps 5 and 6 |
| C, a spinner | the band's edges, the line spacing, face-on | <a href="#frame-a-spinner-s-micro-doppler">A Spinner's Micro-Doppler</a> | Steps 7 to 9 |
| D, chirp count and bandwidth | $\Delta v$, the floor, and $\Delta R$ | <a href="#frame-the-velocity-axis">The Velocity Axis</a>, <a href="#frame-choosing-the-burst">Choosing the Burst</a> | Steps 14 and 15 |
| E, MTI | each canceller's gain on each return | <a href="#frame-canceller-response-and-blind-speeds">Canceller Response and Blind Speeds</a>, <a href="#frame-what-to-expect-at-the-kit">What to Expect at the Kit</a> | Steps 10 to 12, 16 |
| F, the spectrogram | its cell, its column spacing, its band | <a href="#frame-short-windows-the-spectrogram">Short Windows: The Spectrogram</a> | Step 17 |

Show your work for one row of each table on your own paper and attach it.
::::

::::{frame}
:class: title-frame

<div class="course-mark">ECE 444 · Fall 2026</div>

<h1 class="frame-title">L29 Lab: Range-Doppler and MTI</h1>

<div class="title-rule"></div>

Read a hand and a spinner on the range-Doppler map, then cancel the returns that do not move.

L29 Lab · Antennas, Phased Arrays, and Radar Systems · Dr. Neil Rogers
::::

::::{frame} Learning Objectives
:class: here-29

<ol class="lo-list" style="--module: '4'; counter-reset: lo 4">
  <li>I can process FMCW radar data to produce range, range-waterfall, and range-Doppler results.</li>
  <li>I can apply moving target indication (MTI) processing to distinguish moving targets from clutter.</li>
</ol>
::::

::::{frame} The Big Picture
:::{present}
- Read velocity, then cancel what does not move.
:::
:::{present}
| Steps | Set | Read | Table |
| :-- | :-- | :-- | :-- |
| 1–4 | clear scene | leakage, wall | A |
| 5–9 | hand, spinner | velocity, band | B, C |
| 10–13 | MTI | levels | E |
| 14–17 | notebook | cells, spectrogram | D–F |
:::

The Phaser app's **Range + Velocity** preset sends one burst and draws its range-Doppler map. You read the static scene first, then a hand pushed and pulled along the line of sight, then a fidget spinner edge-on and face-on. You switch the app's MTI between off, 2-pulse, and 3-pulse with the wall, your hand, and your still hand in the beam. After class the notebook runs the same chirp count, canceller, and spectrogram readings on the bursts you saved. Every reading fills a white Measured cell in the packet, beside the shaded Predicted cell you filled in from the lesson.
::::

::::{frame} Predict First
:class: viz-frame

:::{depth}
Before you measure, predict each picture, then check yourself. Choose a target, an MTI setting, and a chirp count, and decide before you press **Show map**: where on the map the target lands, at what sign of velocity, how wide in velocity, and what the canceller does to it. Then show it. Any change hides the map again, so each guess comes first. The widget runs the lesson's teaching burst, not the kit's preset, so its numbers are not your Part 1 values; its pictures are the ones your kit should draw.
:::

:::{present}
<iframe src="../../viz/rd-predict.html"
        width="100%" height="460"
        style="border: 1px solid #cddce9; border-radius: 6px;"
        loading="lazy"
        title="Choose a target, an MTI setting, and a chirp count, predict the range-Doppler map, then show it">
</iframe>
:::
::::

::::{frame} Bring Up the Kit
:::{present}
- Tx on OUT2; Range + Velocity, MTI off, the Range-Doppler view.
- Calibrate 0 m, then read the leakage and the wall.
:::
:::{present}
<img src="../../viz/img/L29-setup.svg" alt="Top-down sketch of the setup: the kit with its transmit antenna on OUT2 at the left, its beam opening to the right, a spinner about 0.5 m out, a hand about 1 m out, a wall or plate about 2.5 m out, and you standing behind and to one side of the kit, clear of the beam" style="max-width: 420px; width: 100%; display: block; margin: 0 auto;">
:::

You need a wall or the L28 plate standing on its own about 2.5 m in front of the kit, a tape measure, a ruler, and a fidget spinner. The burst sees everything that moves in the beam, and your body is the largest moving return in the room, so step behind the kit or well to one side for every static and MTI reading; otherwise your breathing and sway appear as a smear of slow velocities at your range.

1. **Connect.** With the kit powered off, connect the transmit antenna to **OUT2**, then power it and wait for the Pi to boot. On your laptop open the radar app at `http://phaser-NN.local:8081`, with your kit's number for NN, and choose the **FMCW** tab.
2. **Calibrate 0 m.** In the FMCW section, set **Preset** to **Range + Velocity**. Press **Calibrate…**, hold the plate against the array, wait for the strongest return to settle, and press **Calibrate**: the app writes your kit's 0 m frequency into **0 m Beat (kHz)**. Or type your L28 Table A value there. The app measures every range on the map from this frequency, so a wrong value moves every return by the same distance.

   <div class="rec" data-lab="L29">
   <label>Step 2: 0 m Beat (kHz) <input data-field="a.f0"></label>
   </div>
3. **Start the map.** Leave **MTI** off, open the **Range-Doppler** view, and press **Start**. Velocity runs across, positive closing, and range runs up. Hover over any cell to read its velocity, range, and level in dB. **Peak Range**, **Peak Velocity**, and **Peak Magnitude** below the plot read the strongest cell that moves: they skip the cells within 0.3 m/s of zero, so read a static return by hovering. The colors run from each frame's own peak down **Color Span (dB)**, so read levels by hovering, never by color. The app's levels sit about 18 dB below the notebook's dBFS on the same burst, because the app windows each FFT with a Blackman window and scales it differently from `range_doppler`; compare a change in dB between the two, never a level.
4. **Read the static scene.** Step clear of the beam. Hover over the leakage, which sits in the first range cell at 0 m/s, and over the wall's spot at 0 m/s, and record each range, velocity, and level, and the wall's tape range. Compare each with your Table A prediction; a spot within half a range cell of it agrees. Press **Save Capture**: it downloads the current burst as `phaser_range_doppler_<date>-<time>.npz`, 256 raw chirps whatever the MTI setting, so the notebook applies the canceller itself. Rename it for what it holds and move it into your Module 4 folder.

   <div class="rec" data-lab="L29">
   <label>Step 4: leakage, range and velocity <input data-field="a.leak"></label>
   <label>Leakage level (dB) <input data-field="a.leak.db"></label>
   <label>Wall, tape range <input data-field="a.wall.tape"></label>
   <label>Wall, range and velocity on the map <input data-field="a.wall"></label>
   <label>Wall level (dB) <input data-field="a.wall.db"></label>
   <label>Static-scene file <input data-field="a.file"></label>
   </div>
::::

::::{frame} A Hand
:::{present}
- A flat hand about 1 m out, at array height.
- Push it in, then pull it out, along the line of sight.
- Read Peak Range and Peak Velocity; save a push.
:::
:::{present}
<img src="../../viz/img/L29-hand-moves.svg" alt="Two sketches of the kit and a hand: pushed and pulled along the line of sight, and moved across the beam, which gives it almost no radial speed" style="max-width: 420px; width: 100%; display: block; margin: 0 auto;">
:::

Moving the hand across the beam gives it almost no radial velocity, so keep it on the line of sight and at a steady pace.

5. **Push.** Stand to one side of the kit and push a flat hand straight toward the array from about 1 m, about half a meter in half a second. Record its range and velocity from **Peak Range** and **Peak Velocity**, and convert the velocity to its Doppler frequency, $f_D = 2v/\lambda$. Repeat a few times and record a typical push. Your push will not be exactly 1 m/s, so compare its sign with Table B, and check that your Doppler equals $2v/\lambda$ at the velocity you read. Press **Save Capture** during a push, with the wall still in view: the burst lasts 128 ms, so start the push before you press it and keep moving until it saves.

   <div class="rec" data-lab="L29">
   <label>Step 5: push, range <input data-field="b.close.r"></label>
   <label>Velocity <input data-field="b.close.v"></label>
   <label>Doppler (Hz) <input data-field="b.close.fd"></label>
   <label>Push file <input data-field="b.file"></label>
   </div>
6. **Pull.** Pull the hand straight away from the array and record the same.

   <div class="rec" data-lab="L29">
   <label>Step 6: pull, range <input data-field="b.open.r"></label>
   <label>Velocity <input data-field="b.open.v"></label>
   <label>Doppler (Hz) <input data-field="b.open.fd"></label>
   </div>
::::

::::{frame} A Fidget Spinner
:::{present}
- Measure the arm radius.
- Edge-on, about 0.5 m out: read the band and its lines.
- Face-on: read the band again.
:::
:::{present}
<img src="../../viz/img/L29-spinner-orient.svg" alt="Two top-down sketches of the kit and a spinner: edge-on, its plane of rotation holding the line of sight so the arms move toward and away from the kit; face-on, its plane across the beam so the arms move across it" style="max-width: 420px; width: 100%; display: block; margin: 0 auto;">
:::

7. **Measure the arm.** Measure the spinner's arm radius $a$, from the center of the hub to the center of a weight.

   <div class="rec" data-lab="L29">
   <label>Step 7: arm radius a <input data-field="c.a"></label>
   </div>
8. **Edge-on.** Spin it hard and hold it by the hub, edge-on to the kit, its plane of rotation pointed at the array, about 0.5 m out at array height. A spinner with metal weights in its arms reflects more than an all-plastic one. Hover along the band's row to read its range, the velocities of its two edges, and, where the lines within it are visible, their spacing; then work out the spin rate from the edge and from the lines. A real spinner slows as it runs, so read both within a few seconds of each other, and press **Save Capture** while it spins fast.

   <div class="rec" data-lab="L29">
   <label>Step 8: band range <input data-field="c.r"></label>
   <label>Band edges <input data-field="c.edge"></label>
   <label>Line spacing <input data-field="c.space"></label>
   <label>Spin rate from the edge <input data-field="c.rev.edge"></label>
   <label>Spin rate from the lines <input data-field="c.rev.lines"></label>
   <label>Spinner file <input data-field="c.file"></label>
   </div>
9. **Face-on.** Turn the spinner face-on to the kit and record where the band's edges are now.

   <div class="rec" data-lab="L29">
   <label>Step 9: face-on, band edges <input data-field="c.face"></label>
   </div>
::::

::::{frame} Cancel the Clutter
:::{present}
- MTI off, then 2-pulse, then 3-pulse, at each return.
- The wall with the beam clear, then a pushing hand.
- A hand held still, then one moved across the beam.
:::

Read every level here by hovering, at the return's range: the wall at 0 m/s, a hand at its spot. Record the level with MTI off, and with each canceller the change from it in dB. After MTI the map rescales to the strongest thing left, so a weakened return can still look bright.

10. **The wall.** Step clear of the beam with **MTI** off and read the wall's level. Turn **MTI** on with **MTI Mode** at **2-pulse**, then **3-pulse**, and read the same cell each time. If the return drops to the noise floor, record it as gone.

    <div class="rec" data-lab="L29">
    <label>Step 10: wall, MTI off (dB) <input data-field="e.wall.off"></label>
    <label>2-pulse change <input data-field="e.wall.2"></label>
    <label>3-pulse change <input data-field="e.wall.3"></label>
    </div>
11. **A pushing hand.** Push your hand as in Step 5 and read its spot the same three ways.

    <div class="rec" data-lab="L29">
    <label>Step 11: hand, MTI off (dB) <input data-field="e.hand.off"></label>
    <label>2-pulse change <input data-field="e.hand.2"></label>
    <label>3-pulse change <input data-field="e.hand.3"></label>
    </div>
12. **Still, and across.** Hold your hand still in the beam about 0.8 m out and read it the same three ways; then move it side to side across the beam at the same range, about 0.2 m either way, once a second, and do the same. Compare all four rows with your Table E predictions.

    <div class="rec" data-lab="L29">
    <label>Step 12: still hand, MTI off (dB) <input data-field="e.still.off"></label>
    <label>2-pulse change <input data-field="e.still.2"></label>
    <label>3-pulse change <input data-field="e.still.3"></label>
    <label>Hand across, MTI off (dB) <input data-field="e.across.off"></label>
    <label>2-pulse change <input data-field="e.across.2"></label>
    <label>3-pulse change <input data-field="e.across.3"></label>
    </div>
13. **Restore.** Turn **MTI** off.
::::

::::{frame} Run the Notebook
:::{present}
- Run it on your push burst.
- Task (a): shorten the burst to 128, then 64 chirps.
- Task (b): enter your predicted gain, then run 2-pulse and 3-pulse.
- Task (c): the spinner's spectrogram, 64- then 32-chirp windows.
:::

Do this part after class, from your saved bursts, with the notebook set up as the Notebook Setup frame describes. Each task's markdown cell states what to check, and each prints the numbers its step records. The notebook's levels are dBFS, about 18 dB above the app's hover levels on the same burst, because `range_doppler` uses a Hann window and divides each FFT by the window's sum; compare changes between the two, never levels. The app's presets all send 256 chirps of 500 MHz, so the 128- and 64-chirp rows are the first $M$ chirps of your own burst, and the 200 MHz row is a recorded burst for everyone.

14. **The chirp count.** Open `L29_range_doppler.ipynb`, set `CAPTURE` in the first code cell to your push burst from Step 5, and run the cells from the top. In task (a), run the chirp-count cell with `M = 256`, then change that one line to `M = 128` and to `M = 64`. Record `dv` and the hand's width 3 dB down for each, the floor at `M = 256` in dBFS, and the floor's change from it at 128 and 64.

    <div class="rec" data-lab="L29">
    <label>Step 14: M = 256, dv <input data-field="d.256.dv"></label>
    <label>Width 3 dB down <input data-field="d.256.w"></label>
    <label>Floor (dBFS) <input data-field="d.256.fl"></label>
    <label>M = 128, dv <input data-field="d.128.dv"></label>
    <label>Width 3 dB down <input data-field="d.128.w"></label>
    <label>Floor change from 256 (dB) <input data-field="d.128.fl"></label>
    <label>M = 64, dv <input data-field="d.64.dv"></label>
    <label>Width 3 dB down <input data-field="d.64.w"></label>
    <label>Floor change from 256 (dB) <input data-field="d.64.fl"></label>
    </div>
15. **The bandwidth.** Set `CAPTURE` to `L29_hand_closing_B200.npz` and run the map cell again. Record the hand's width in range, and set `CAPTURE` back to your own burst.

    <div class="rec" data-lab="L29">
    <label>Step 15: 200 MHz, width in range <input data-field="d.b200.w"></label>
    </div>
16. **The cancellers.** In task (b), replace `H_DB = None` with the canceller's predicted gain at the hand's Doppler, in dB, and run the MTI cell with `KIND = "2pulse"`; then change it to `KIND = "3pulse"`. Record the hand's change beside your `H_DB`, and the floor's change near 14 m/s.

    <div class="rec" data-lab="L29">
    <label>Step 16: 2-pulse, hand change; H_DB <input data-field="e.nb.hand.2"></label>
    <label>Floor change near 14 m/s <input data-field="e.nb.fl14.2"></label>
    <label>3-pulse, hand change; H_DB <input data-field="e.nb.hand.3"></label>
    <label>Floor change near 14 m/s <input data-field="e.nb.fl14.3"></label>
    </div>
17. **The spectrogram.** In task (c), set `SPIN` to your spinner burst and run its map cell, which prints the band's lines; set `R_SPIN` to the band's range and run the spectrogram with `N_WIN = 64`, then `N_WIN = 32`. Record the Doppler cell, the time between columns, and the band within 10 dB of its peak. Save the notebook with its edits and plots and upload the `.ipynb` with the packet.

    <div class="rec" data-lab="L29">
    <label>Step 17: N_WIN = 64, Doppler cell <input data-field="f.64.cell"></label>
    <label>Time between columns <input data-field="f.64.dt"></label>
    <label>Band <input data-field="f.64.band"></label>
    <label>N_WIN = 32, Doppler cell <input data-field="f.32.cell"></label>
    <label>Time between columns <input data-field="f.32.dt"></label>
    <label>Band <input data-field="f.32.band"></label>
    </div>
::::

::::{frame} No Hardware?
:class: read-only

```{note}
Every step works without a kit. Open the Phaser app's simulator in a
browser,
<a href="https://livethisdream.github.io/phaser/radar/" target="_blank" rel="noopener">livethisdream.github.io/phaser/radar</a>:
the same radar app, with a **Scene** menu in its FMCW section and a pill that
reads **Simulated**. A **Scene** moves simulated targets live on the Range +
Velocity preset: `hand` waves a hand at 0.6 m, `corners` holds three corners
at 1, 2, and 3 m, and `static` holds a still target at 1 m with movers at 3.5
and 7 m. **Load Capture** plays one of the course's recorded bursts through
the same views as if it were live, with the MTI switch working on it. Leave
**0 m Beat (kHz)** empty: a recording uses its own 0 m frequency, which the
**Logs** tab prints when it loads. The recordings are in the lab's bundle,
<a href="../../bundles/L29_lab.zip" download>L29_lab.zip</a>, with the
notebook. They simulate the PHASER on the app's preset, with a wall at
2.5 m; the simulation times the chirps perfectly, so the cancellers remove
the wall completely, which no kit does. Say in your packet which readings are
recorded rather than your own.

- Steps 1 to 4 and 10: `L29_static.npz`
- Steps 5, 11, 14, and 16: `L29_hand_closing.npz`; Step 6: `L29_hand_opening.npz`
- Steps 7 to 9 and 17: `L29_spinner.npz` and `L29_spinner_faceon.npz`; the arm radius is 3.0 cm
- Step 12: `L29_hand_still.npz` and `L29_hand_across.npz`
- Step 15: `L29_hand_closing_B200.npz`, the same for everyone
```
::::

::::{frame} Notebook Setup
:class: read-only

Download the lab's bundle, <a href="../../bundles/L29_lab.zip" download>`L29_lab.zip`</a>, and unzip it into the Module 4 folder you set up in the L28 Lab's <a href="../L28-fmcw/index.html#frame-notebook-setup">Notebook Setup</a>, with the same Python and packages. It holds `L29_range_doppler.ipynb`, a fresh `radar_lab.py`, the data README, and all eight recorded bursts, which the notebook opens by default, so it runs as shipped before you change anything. Move the bursts you saved with **Save Capture** into the same folder. Start Jupyter in the folder with `jupyter lab` and open `L29_range_doppler.ipynb`.
::::

::::{frame} Your Part 2 Entries
:class: read-only

This frame collects every box you filled in on this page. Your entries stay in this
browser only, saved as you type. **Download my packet** writes them into Part 2
of the blank packet and saves the PDF; do Parts 1 and 3 on paper or in the PDF
viewer, and upload one PDF to Gradescope with your notebook. If you have already typed Part 1 into
the packet PDF, use **Fill my own copy** and choose that file instead: your Part 1
is kept, and Part 2 is added to it. Either way the result is locked, so finish
any typing in the PDF first. **Export entries** saves a small backup file you
can **Import** on another laptop or after clearing your browser. The boxes are
optional: the blank packet is in the next frame, to fill on paper or in a PDF
viewer instead.

<div class="rec-summary" data-lab="L29" data-pdf="../../labs/ECE444_Lab_L29_RangeDoppler_blank.pdf" data-file="ECE444_L29_Lab"></div>
::::

::::{frame} Lab Packet
:class: read-only doc-links

The L29 Lab packet is one submission, turned in complete before Lesson 30, with the notebook. It has three parts:

1. Part 1, Predict (before the lab period): the shaded Predicted cells of Tables A to F, at the Range + Velocity preset.
2. Part 2, Measure (your own kit, in class, and the notebook after): the white Measured cells of the same tables.
3. Part 3, Analyze (after the lab): three prompts about what you measured.

- <a class="doc-link" href="../../labs/ECE444_Lab_L29_RangeDoppler_blank.pdf" target="_blank" rel="noopener">L29 Lab packet (PDF)</a>
::::

::::{frame} For Part 3
:class: read-only

Part 3 asks you to compare your Table D readings at the three chirp counts with your predictions, to find your spinner's spin rate every way Table C allows and say which you would report, and to compare what each canceller did to each return in Table E with your predictions. I grade each answer on a claim, your own numbers as evidence, the reasoning between them, and how large a difference your readings can resolve. For the final report, keep your bursts, your notebook, and your tables: the report asks you to explain, in your own words, how a burst of chirps becomes a velocity and what MTI does to a scene.
::::

::::{frame} Looking Ahead
:class: read-only

<a href="../L30-cfar/index.html">Lesson 30</a> decides which cells of this map hold targets, setting the threshold from the cells around each one, and the L30 Lab runs that detector on range-Doppler maps of this burst.
::::
