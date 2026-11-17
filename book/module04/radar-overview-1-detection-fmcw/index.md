---
frame_view: true
---

# Radar Overview 1 - Detection and FMCW Range

::::{frame}
:class: title-frame

<div class="course-mark">ECE 444 · Fall 2026</div>

<h1 class="frame-title">Detection and FMCW Range</h1>

<div class="title-rule"></div>

A threshold against noise decides what the radar reports, and an FMCW chirp converts range into frequency.

Radar Overview 1 · Antennas, Phased Arrays, and Radar Systems · Dr. Neil Rogers
::::

::::{frame} Printing
:class: read-only

To print the slides, switch to present mode and print: one slide a sheet,
with room for notes. Print from read mode for the whole lesson.
::::

::::{frame} Learning Objectives

<ol class="lo-list" style="--module: '4'; counter-reset: lo 2">
  <li>I can apply radar detection theory (PD, FAR, dwell time) to determine detection performance under noise.</li>
  <li>I can describe FMCW radar operation and configure an FMCW waveform on the ADALM-PHASER.</li>
  <li>I can process FMCW radar data to produce range, range-waterfall, and range-Doppler results.</li>
</ol>

```{include} ../../_snippets/m4-strip.md
```

:::{depth}
This overview and the next cover what the L28–L31 Labs use, in two class periods. Each topic here is a summary of a full lesson, and each frame links to that lesson for the derivation. Read the lesson half of each lab's page before its lab; these two overviews do not replace it.
:::
::::

::::{frame} Two Overviews, Four Labs

:::{present}
- Overview 1: detection against noise, then range from an FMCW chirp.
- Overview 2: velocity, MTI, CFAR, classification, and tracking.
- L28–L31 Labs: range, range-Doppler and MTI, CFAR, classify and track. Each lab starts from the one before it.
:::

Today's first half is detection: every cell of a radar's output holds noise, the processor compares each cell with a threshold, and the signal-to-noise ratio (SNR) sets how often that decision is right. The second half is how the PHASER measures range: it transmits a chirp, and the echo's delay appears as a frequency that one FFT converts to range. In the L28 Lab you measure range with your kit, and in the L30 Lab you set a threshold on your own data.
::::

::::{frame} What We Already Have

:::{present}
$$
P_r = \frac{P_t G_t G_r \lambda^2 \sigma}{(4\pi)^3 R^4}
$$

$$
\begin{aligned}
P_r\ [\text{dBm}] = {} & P_t + G_t + G_r \\
&+ 10\log_{10}\lambda^2 \\
&+ \sigma\ [\text{dBsm}] \\
&- 33.0 - 40\log_{10} R
\end{aligned}
$$
:::
:::{present}
- RCS and range set the echo power, and so the SNR.
- Bandwidth sets $\Delta R = c/2B$; the PRF sets the unambiguous velocity.
:::

The radar equation of <a href="../L25-radar-equation/index.html#frame-two-way-path-loss-in-decibels">Lesson 25</a> gives the echo power from a target of radar cross section (RCS) $\sigma$ at range $R$, and dividing by the noise power $kT_\text{sys}B$ gives the SNR. Today's first half starts from that SNR. <a href="../L26-range-resolution-doppler/index.html">Lesson 26</a> gave the range resolution $c/2B$ and the limits the pulse repetition frequency (PRF) sets. An FMCW radar obeys the same relations: its chirp bandwidth sets the resolution, and the rate at which it repeats the chirp is its PRF, which sets the unambiguous velocity in Overview 2. Its farthest range comes from the receiver's sample rate, not from the PRF, as The 0 m Frequency frame shows.
::::

::::{frame} A Detection Is a Decision

:::{present}
- Every range cell holds noise, and some also hold a target.
- The processor reports a target in every cell above a **threshold**.
- Noise above the threshold is a **false alarm**.
:::
:::{present}
<img src="../../viz/img/L27-range-profile.svg" alt="One range profile of 200 cells: noise power scattered from about minus 20 to plus 7 dB about the mean, one target cell at 13 dB, and a dashed threshold at 11.4 dB that only the target crosses" style="max-width: 640px; width: 100%; display: block; margin: 0 auto;">
:::

The figure is the power in each of 200 range cells, in dB above the mean noise power. Receiver noise is random, and from cell to cell it spreads over more than 25 dB. One cell also holds a target 13 dB above the mean noise. The processor does not know which cell that is, so it applies one rule to every cell: report a target where the power exceeds the threshold. A noise-only cell that crosses the threshold is a false alarm, and a target cell that falls below it is a missed detection. Raising the threshold makes false alarms rarer and misses more common. <a href="../L27-radar-detection/index.html#frame-a-detection-is-a-decision">Lesson 27</a> has the full treatment.
::::

::::{frame} Probability of False Alarm

:::{present}
$$
\begin{aligned}
P_{fa} &= e^{-T/P_n} \\
\frac{T}{P_n} &= \ln\frac{1}{P_{fa}}
\end{aligned}
$$

- $P_{fa} = 10^{-6}$ puts the threshold $T$ 11.4 dB above the mean noise power $P_n$.
- 3 dB more noise raises $P_{fa}$ to $10^{-3}$ under the same threshold, a thousand times the false alarms.
:::

The **probability of false alarm** $P_{fa}$ is the probability that a cell holding only noise crosses the threshold $T$. Noise power in one cell follows an exponential distribution with mean $P_n$, and the area of that distribution above $T$ is $e^{-T/P_n}$. We choose $P_{fa}$ and solve for the threshold: $10^{-6}$ needs $T = 13.8\ P_n$, which is 11.4 dB above the mean noise.

The threshold is a multiple of $P_n$, so the processor has to know the noise power. If the noise doubles while the threshold stays where it was, the exponent halves and $P_{fa}$ becomes $(10^{-6})^{1/2} = 10^{-3}$, a thousand times the false alarms for 3 dB of noise. Overview 2 uses that sensitivity as the reason for CFAR.

What an operator sees is the **false-alarm rate** (FAR), the false reports per second: $P_{fa}$ times the number of cells the radar tests each second. A radar that tests a million cells a second at $P_{fa} = 10^{-6}$ reports about one false target a second. The derivation is in <a href="../L27-radar-detection/index.html#frame-probability-of-false-alarm">Lesson 27</a>.
::::

::::{frame} Threshold Explorer
:class: viz-frame

:::{depth}
A cell that holds a steady target of power $P_s$ plus noise has a power distribution centered near $P_s + P_n$. The **probability of detection** $P_d$ is the area of that distribution above the threshold $T$. The area has no closed form; <a href="../L27-radar-detection/index.html#frame-target-plus-noise">Lesson 27</a> gives the function that computes it.

The widget draws the noise distribution and the target's distribution against power in dB, with the threshold between them, and beside them $P_d$ against $P_{fa}$ with the present operating point marked. It opens at 13 dB SNR with the threshold 11.4 dB above the mean noise, the setting for $P_{fa} = 10^{-6}$: 87% of the target's distribution lies above the threshold, so $P_d = 0.87$. Move the threshold, and one shaded area grows as the other shrinks. Raise the target SNR, and the target's distribution moves away from the noise. The pulses control sets the number of pulses $N$ the processor integrates, which the Integrating Pulses frame covers, and the noise control raises the noise while the threshold stays where we set it.
:::

<iframe src="../../viz/detection-threshold.html"
        width="100%" height="437"
        style="border: 1px solid #cddce9; border-radius: 6px;"
        loading="lazy"
        title="Detection threshold against the noise and target probability densities, with the operating point on the Pd versus Pfa curve">
</iframe>
::::

::::{frame} Pd Against Pfa

:::{present}
<img src="../../viz/img/L27-roc.svg" alt="Probability of detection against probability of false alarm on a log axis from 10 to the minus 10 to 0.1, for SNRs of 8, 10, 12 and 14 dB. At Pfa = 10 to the minus 6 the 12 dB curve reads 0.68" style="max-width: 600px; width: 100%; display: block; margin: 0 auto;">
:::
:::{present}
- A lower threshold raises $P_d$ and $P_{fa}$ together.
- At $P_{fa} = 10^{-6}$: 12 dB gives $P_d = 0.68$, 14 dB gives 0.97.
- By Albersheim's fit, $P_d = 0.9$ at $P_{fa} = 10^{-6}$ needs 13.1 dB.
:::

Each curve fixes the SNR and sweeps the threshold. Lowering the threshold moves the operating point up and to the right along its curve, so detections and false alarms rise together. Only more SNR raises $P_d$ at a fixed $P_{fa}$, and it does so steeply: at $P_{fa} = 10^{-6}$, 8 dB of SNR gives $P_d = 0.06$ and 14 dB gives 0.97.

The design question runs the other way: what SNR does a required $P_d$ and $P_{fa}$ take? For a steady target, $P_d = 0.9$ at $P_{fa} = 10^{-6}$ takes 13.1 dB by Albersheim's equation, a fit that is within 0.1 dB of the exact 13.2 dB, in <a href="../L27-radar-detection/index.html#frame-albersheim-s-equation">Lesson 27</a>. The radar equation then says at what range a given target still returns that much.
::::

::::{frame} Integrating Pulses

:::{present}
$$
\begin{aligned}
\text{SNR}_N &= N\ \text{SNR}_1 \\
10\log_{10}128 &= 21.1\ \text{dB}
\end{aligned}
$$

- Echoes add in voltage, and noise adds in power.
- With 128 chirps, each chirp needs only $13.1 - 21.1 = -8.0$ dB.
- The **dwell time** is $T_\text{d} = N\ T_\text{PRI}$.
:::
:::{present}
<img src="../../viz/img/L27-integration-gain.svg" alt="Integration gain in dB against N on a log axis. Coherent is a straight line, 10 log N. Noncoherent, from Albersheim's equation, falls below it: 2.5 dB short at N = 16 and 4.8 dB short at N = 64" style="max-width: 600px; width: 100%; display: block; margin: 0 auto;">
:::

A radar does not have to decide on one chirp. If it adds the returns of $N$ chirps from the same cell before it compares with the threshold, the target's echoes add in phase, so the signal voltage grows as $N$ and its power as $N^2$. A moving target's phase steps from chirp to chirp, and the second FFT of Overview 2, across the chirps, removes that step before it adds them. The noise is independent from chirp to chirp, so its power grows as $N$. The SNR therefore grows as $N$, which is **coherent integration**, the straight line in the figure. The lower curve is noncoherent integration, which adds powers without the phase and gains less.

Lesson 29's teaching burst has 128 chirps, each 400 MHz in 200 µs, a gain of 21.1 dB, so a target at $-8.0$ dB SNR on one chirp reaches the 13.1 dB of the previous frame. The burst sends one chirp every pulse repetition interval $T_\text{PRI} = 0.4$ ms, so the dwell time is $128 \times 0.4\ \text{ms} = 51.2$ ms. The target has to stay in one range cell for that long, or its echoes do not add in one cell. <a href="../L27-radar-detection/index.html#frame-integrating-pulses">Lesson 27</a> covers the limits on the dwell.
::::

::::{frame} The Fixed Threshold

:::{present}
<img src="../../viz/img/L27-fixed-threshold.svg" alt="A 600-cell range profile whose noise rises 6 dB beyond cell 330. A fixed threshold at 11.4 dB is crossed by noise at eight cells in the noisy region. A local-average threshold steps up with the noise and is not crossed" style="max-width: 640px; width: 100%; display: block; margin: 0 auto;">
:::
:::{present}
- Where the noise rises 6 dB, noise crosses the fixed threshold eight times.
- A threshold the processor computes from the neighboring cells rises with the noise. That is **CFAR**, in Overview 2.
:::

Every number so far assumed the processor knows $P_n$. In a real scene the noise level changes from one part of the profile to another. In the figure the noise rises 6 dB beyond cell 330. The fixed threshold, set for $P_{fa} = 10^{-6}$ in the quiet cells, has $P_{fa} = 0.03$ in the noisy ones, and noise crosses it eight times. The green line is a threshold computed from the cells around each cell under test, so it rises where the noise rises. That is constant false-alarm rate (CFAR) detection. <a href="../L27-radar-detection/index.html#frame-the-fixed-threshold">Lesson 27</a> works the numbers, and the L30 Lab runs CFAR on your own data.
::::

::::{frame} A Chirp and Its Echo

:::{present}
<img src="../../viz/img/L28-chirp.svg" alt="Frequency against time. The transmitted chirp is a straight ramp repeated twice. The echo is the same ramp shifted right by the delay. At any instant the two differ by a fixed frequency, the beat. The ramp spans the bandwidth vertically and the chirp length horizontally. The first tenth of each ramp is shaded as settling, and the last 90% is marked as kept" style="max-width: 620px; width: 100%; display: block; margin: 0 auto;">
:::
:::{present}
- The transmitter sweeps a bandwidth $B$ in a chirp length $T_s$, then repeats.
- The echo is the same ramp, late by the round trip $2R/c$.
- Their frequency difference, the **beat**, is constant.
:::

The second half of today is how the PHASER measures range. A target 3 m away returns its echo after 20 ns, which is too short for the PHASER's receiver to time directly. A frequency-modulated continuous-wave (FMCW) radar transmits continuously while its frequency climbs linearly across a bandwidth $B$ during each **chirp** of length $T_s$. The echo is a copy of that chirp, delayed by the round trip. The receiver compares the echo with the chirp still going out. Both ramps climb at the same rate, so the echo is below the outgoing chirp by the same frequency for the whole chirp. That difference is the **beat frequency** $f_b$.

The range examples use a chirp that no preset in the Phaser app uses, 400 MHz in 2 ms from 10.0 GHz, as <a href="../L28-fmcw/index.html#frame-a-chirp-and-its-echo">Lesson 28</a> does. The methods carry over to the presets, and the lab packets ask for the presets' numbers.
::::

::::{frame} The Beat Frequency

:::{present}
$$
\begin{aligned}
f_b &= \frac{B}{T_s}\ \frac{2R}{c} = \frac{2RB}{cT_s} \\
&= \frac{2\ (1\ \text{m})(400\ \text{MHz})}{(3.00\times 10^8\ \text{m/s})(2\ \text{ms})} \\
&= 1.33\ \text{kHz}
\end{aligned}
$$

- The beat is proportional to range: 1.33 kHz for every meter.
:::

The transmitted frequency rises at the chirp slope $B/T_s$. During the round-trip delay $2R/c$ the outgoing chirp climbs by the slope times the delay, and that is the beat. The beat is proportional to range, so the radar reads range by measuring a frequency. On the worked chirp a target at 1 m gives 1.33 kHz and a target at 3 m gives 4.00 kHz. The chirp spans 400 MHz, but the beats are a few kilohertz, which the PHASER samples directly.

Both waveform settings change the beat per meter. A wider bandwidth or a shorter chirp steepens the slope and raises it. <a href="../L28-fmcw/index.html#frame-the-beat-frequency">Lesson 28</a> works both cases.
::::

::::{frame} FMCW Explorer
:class: viz-frame

:::{depth}
The left panel is the beat signal over one chirp, and the right panel is its range spectrum: the FFT of those samples, with the frequency axis converted to range. The widget opens on the worked chirp. Like the Phaser app, it keeps the last 90% of each chirp, the part the chirp figure marks as kept, so its resolution readout is $c/(2 \times 0.9B) = 0.42$ m, a little more than the 0.375 m the next frame derives for the whole chirp. Move the target and count the cycles of the beat. Change the bandwidth or the chirp length, and the beat per meter follows $B/T_s$. Turn on the second target and bring it toward the first until the two peaks merge, which is the subject of the next frame.
:::

<iframe src="../../viz/fmcw-beat.html"
        width="100%" height="435"
        style="border: 1px solid #cddce9; border-radius: 6px;"
        loading="lazy"
        title="FMCW explorer: the beat signal over one chirp and its range spectrum, for chosen range, bandwidth, chirp length, second target, and window">
</iframe>
::::

::::{frame} Range Resolution

:::{present}
$$
\begin{aligned}
\Delta f_b &= \frac{1}{T_s} \\
\Delta R &= \frac{cT_s}{2B}\ \Delta f_b = \frac{c}{2B} \\
&= \frac{3.00\times 10^8\ \text{m/s}}{2\ (400\ \text{MHz})} \\
&= 0.375\ \text{m}
\end{aligned}
$$

- The chirp length cancels: only the bandwidth sets the resolution.
:::

The radar observes each beat for one chirp, $T_s$, and an FFT over a record of that length separates two tones only if they differ by at least $1/T_s$. Dividing that frequency step by the beat per meter converts it to range, and the result is the $c/2B$ of <a href="../L26-range-resolution-doppler/index.html#frame-resolution-and-bandwidth">Lesson 26</a>. A longer chirp lowers the beat per meter, and it lets the FFT resolve finer frequency steps in the same proportion, so $T_s$ cancels. Two targets closer than one cell return one peak. <a href="../L28-fmcw/index.html#frame-range-resolution">Lesson 28</a> has the details.
::::

::::{frame} The 0 m Frequency

:::{present}
<img src="../../viz/img/L28-spectrum.svg" alt="Power in dBFS against beat frequency from 0 to 300 kHz for the worked chirp with the 0 m frequency at 100 kHz. Below 100 kHz the band is shaded as negative range. A dashed line at 100 kHz marks the leakage, the strongest peak. The room's wall at 5.5 m peaks 7.3 kHz above it, labeled. A target at 30 m peaks 40 kHz above it. A red line at 300 kHz marks half the sample rate, 150 m, past which beats alias" style="max-width: 620px; width: 100%; display: block; margin: 0 auto;">
:::
:::{present}
- The PHASER puts a 0 m echo at $f_0$, 100 to 120 kHz; every beat adds to it.
- $f_0$ changes at every power-up, so calibrate it first.
- Beats above half the sample rate alias: 150 m on the worked chirp.
:::

The PHASER does not put a 0 m echo at zero frequency. It adds every beat to a fixed offset, the kit's **0 m frequency** $f_0$, so a target's peak is at $f_0 + f_b$. The offset keeps the targets clear of zero frequency, where the receiver's own offset and low-frequency noise are. On our kits $f_0$ reads 100 to 120 kHz, it differs from kit to kit, and it changes when the kit restarts. The first step of the L28 Lab is to measure it, with a metal plate held against the array.

The figure is the whole spectrum the receiver records for the worked chirp with $f_0$ at 100 kHz. Its power axis is in **dBFS**, decibels relative to the largest signal the receiver's converter records. Frequencies below $f_0$ are negative ranges. The strongest peak, at $f_0$, is the **leakage**: the transmit antenna's direct path into the array, a few centimeters long. The receiver samples at 0.6 MSPS and represents frequencies up to half that, 300 kHz, so the beats have $300 - 100 = 200$ kHz of room above $f_0$. At 1.33 kHz per meter that is 150 m, and a beat from farther away aliases to a wrong range. <a href="../L28-fmcw/index.html#frame-the-0-m-frequency">Lesson 28</a> covers the calibration and the range limit.
::::

::::{frame} The Range Profile

:::{present}
$$
R = \frac{cT_s}{2B}\left(f - f_0\right)
$$

- One FFT of one chirp is a **range profile**.
- The figure shows the leakage at 0 m, a corner reflector at 2.0 m, and the wall at 5.5 m.
:::
:::{present}
<img src="../../viz/img/L28-range-profile.svg" alt="Power in dBFS, dB relative to the receiver's full scale, against range from minus 0.3 to 8 m for the worked chirp, with a top axis of beat frequency above the 0 m frequency from 0 to about 10.7 kHz. Three peaks: leakage at 0 m near minus 20 dBFS, a corner reflector at 2.0 m near minus 20 dBFS, and the far wall at 5.5 m near minus 31 dBFS, over a floor near minus 85 dBFS" style="max-width: 640px; width: 100%; display: block; margin: 0 auto;">
:::

The FFT of one chirp's samples is the **range profile**. Each FFT bin is a frequency, and subtracting $f_0$ and dividing by the beat per meter converts it to a range. The figure is one chirp of the worked waveform from the course's simulated room. The top axis shows the same profile as beat frequency above $f_0$, at 1.33 kHz per meter.

The power axis is in dBFS, as in the last frame. The Phaser app and the course's Python module, `radar_lab.py`, both compute this profile for you. The L28 Lab has you read it: where each peak is, how wide it is, and how high it stands above the noise floor. <a href="../L28-fmcw/index.html#frame-the-range-fft">Lesson 28</a> covers the FFT, the window applied before it, and what sets the floor.
::::

::::{frame} The Range Waterfall

:::{present}
<img src="../../viz/img/L28-waterfall.svg" alt="Range profiles from 0 to 6 m stacked in time over 10 s, darker for stronger echoes, the newest at the top. A dark vertical band at 0 m is the leakage and one at 5.5 m is the wall. A zigzag trace runs from 1.5 m out to 3.5 m and back: a person walking" style="max-width: 620px; width: 100%; display: block; margin: 0 auto;">
:::
:::{present}
- Each row is one range profile, with the newest at the top.
- Fixed objects draw vertical lines; a walker draws a zigzag.
- A leg's range change over its time gives the walker's speed.
:::

Stacking successive range profiles, one row per display update and darker for a stronger echo, gives the **range waterfall**: range across and time down, with the newest row at the top, as the Phaser app draws it. The leakage at 0 m and the wall at 5.5 m keep the same range in every row and draw vertical lines. A person walking out and back draws a zigzag, and the slope of each leg is the walking speed: the simulated walker in the figure covers 2 m in 4 s, which is 0.5 m/s.

The waterfall gives velocity only as a change of range over seconds. Its rows are tens of milliseconds apart, and over that time a walker's echo changes phase by many cycles, so the rows do not give velocity from phase. Overview 2 reads velocity from the echo's phase across chirps a fraction of a millisecond apart. <a href="../L28-fmcw/index.html#frame-the-range-waterfall">Lesson 28</a> describes the waterfall, and in the L28 Lab you walk out and back to record one.
::::

::::{frame} Looking Ahead

:::{present}
- Before the L28 Lab, read <a href="../L28-fmcw/index.html">Lesson 28</a> and do Part 1 of its packet.
- Overview 2 covers velocity from chirp-to-chirp phase, MTI, CFAR, classification, and tracking.
:::

The lesson half of the <a href="../L28-fmcw/index.html">Lesson 28</a> page works every method that Part 1 of the L28 Lab packet asks for, and its Pre-Lab frame maps each packet table to the frame that covers it. <a href="../radar-overview-2-doppler-mti-cfar/index.html">Overview 2</a> covers the rest of the chain.
::::
