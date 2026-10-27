---
frame_view: true
---

# L28 - FMCW on the Phaser

::::{frame}
:class: title-frame

<div class="course-mark">ECE 444 · Fall 2026</div>

<h1 class="frame-title">FMCW on the Phaser</h1>

<div class="title-rule"></div>

A 500 MHz chirp turns each meter of range into 6.67 kHz of beat frequency.

Lesson 28 · Antennas, Phased Arrays, and Radar Systems · Dr. Neil Rogers
::::

::::{frame} Printing
:class: read-only

To print the slides, switch to present mode and print: one slide a sheet,
with room for notes. Print from read mode for the whole lesson and lab.
::::

::::{frame} Learning Objectives
:class: here-28

<ol class="lo-list" style="--module: '4'; counter-reset: lo 1">
  <li>I can calculate range resolution, unambiguous range, and Doppler shift for a given radar waveform.</li>
</ol>
<ol class="lo-list" style="--module: '4'; counter-reset: lo 3">
  <li>I can describe FMCW radar operation and configure an FMCW waveform on the ADALM-PHASER.</li>
  <li>I can process FMCW radar data to produce range, range-waterfall, and range-Doppler results.</li>
</ol>

```{include} ../../_snippets/m4-strip.md
```

:::{depth}
<a href="../L26-range-resolution-doppler/index.html">Lesson 26</a> measured range as a round-trip delay and showed that a chirp gives a long transmission the resolution of a short pulse, $\Delta R = c/2B$. It left one problem open: a target 3 m away returns its echo after 20 ns, far too short for the PHASER's 0.6 MSPS receiver to time. This lesson shows how a frequency-modulated continuous-wave (FMCW) radar converts that delay into a frequency of a few kilohertz, how one FFT turns the frequency back into range, and what sets the resolution and the farthest range the kit can report. The L28 Lab follows on this page. You work it on your own kit, outside class, and it is the first stage of the radar your final report describes, so this page carries the whole theory the lab needs.
:::
::::

::::{frame} A Chirp and Its Echo
:::{present}
<img src="../../viz/img/L28-chirp.svg" alt="Frequency against time. The transmitted chirp is a straight ramp repeated twice. The echo is the same ramp shifted right by the delay. At any instant the two differ by a fixed frequency, the beat. The ramp spans the bandwidth vertically and the chirp length horizontally" style="max-width: 620px; width: 100%; display: block; margin: 0 auto;">
:::
:::{present}
- The transmitter sweeps $B$ in $T_s$, then starts again.
- The echo is the same ramp, late by the round trip.
- The gap between them, the **beat**, is constant.
:::

An FMCW radar transmits continuously, and its frequency climbs linearly across a bandwidth $B$ during each **chirp** of length $T_s$. On the PHASER the chirp starts near 10 GHz and sweeps $B = 500$ MHz in $T_s = 0.5$ ms. The echo from a target at range $R$ is a copy of the transmitted chirp delayed by the round trip,

$$
\tau = \frac{2R}{c},
$$

which is 6.7 ns for every meter. The receiver compares the echo with the chirp that is still going out. Because both ramps climb at the same rate, the echo is always below the transmitted chirp by the same frequency, and that difference is the **beat frequency** $f_b$. The figure exaggerates the delay so that it is visible: on the PHASER, a target at 3 m delays the echo by 20 ns, 0.004% of a 0.5 ms chirp.
::::

::::{frame} The Beat Frequency
:::{present}
$$
\begin{aligned}
f_b &= \frac{B}{T_s}\ \tau = \frac{2RB}{cT_s} \\
&= \frac{2\ (1\ \text{m})(500\ \text{MHz})}{(3.00\times 10^8\ \text{m/s})(0.5\ \text{ms})} \\
&= 6.67\ \text{kHz per meter}
\end{aligned}
$$
:::

The transmitted frequency rises at the **chirp slope** $B/T_s$, which for the PHASER is $500\ \text{MHz}/0.5\ \text{ms} = 1\ \text{MHz}$ per microsecond. In the delay $\tau$ the chirp climbs $\tau B/T_s$, so the beat frequency is

$$
\begin{aligned}
f_b &= \frac{B}{T_s}\ \tau \\
&= \frac{2RB}{cT_s} .
\end{aligned}
$$

The beat is proportional to range, so the radar reads range by measuring a frequency. A target at 1 m gives 6.67 kHz, and one at 3 m gives 20.0 kHz. These frequencies are low enough for the Pluto to sample directly, even though the chirp itself spans 500 MHz: comparing the echo with the outgoing chirp removes the sweep and leaves only the small difference that carries the range. <a href="https://analogdevicesinc.github.io/system-level/solutions/platforms/phaser/labs/radar-fmcw/" target="_blank" rel="noopener">ADI's FMCW lab</a> calls this stretch processing.

The kHz per meter depends on both waveform settings. Halving the bandwidth to 250 MHz halves it, to 3.33 kHz per meter, and so does doubling the chirp length to 1 ms. The two changes give the same beat for the same target, but as the next frames show, only one of them changes the resolution.
::::

::::{frame} FMCW Explorer
:class: viz-frame

:::{depth}
The left panel is the beat signal over one chirp, with the 0 m frequency removed, and the right panel is its range spectrum, the FFT of those samples with the frequency axis converted to range. Move the target and count the cycles: every meter adds $2B/c = 3.33$ cycles a chirp at 500 MHz. Halve the bandwidth or double the chirp length and watch the beat per meter halve. Turn on the second target and bring it in toward the first until the two peaks merge; the green bar is $c/2B$. Then set the second target 20 to 40 dB weaker and switch between the rectangular and Hann windows.
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
\Delta R &= \frac{cT_s}{2B}\ \Delta f_b = \frac{c}{2B} = 0.30\ \text{m}
\end{aligned}
$$

- Two targets separate when their beats differ by one cycle a chirp.
- The chirp length cancels: only $B$ sets the resolution.
:::

The radar sees each target's beat for one chirp, $T_s$, and an FFT over a record of length $T_s$ separates two tones only if they differ by at least $1/T_s$. Over one chirp, that is a difference of one cycle. Converting that frequency step to range with the beat per meter,

$$
\begin{aligned}
\Delta R &= \frac{cT_s}{2B}\ \Delta f_b \\
&= \frac{cT_s}{2B}\cdot\frac{1}{T_s} \\
&= \frac{c}{2B} ,
\end{aligned}
$$

the result of <a href="../L26-range-resolution-doppler/index.html#frame-resolution-is-set-by-bandwidth">Lesson 26</a>. At 500 MHz it is 0.30 m. A longer chirp makes the beat per meter smaller but lets the FFT resolve finer frequency steps in the same proportion, so $T_s$ cancels. Halving the bandwidth to 250 MHz doubles the resolution cell to 0.60 m; doubling the chirp length to 1 ms leaves it at 0.30 m.

The number of beat cycles in one chirp is $f_bT_s = 2RB/c$, which does not depend on $T_s$ either. Two plates 0.30 m apart differ by exactly one cycle a chirp at 500 MHz; closer than that, their beats stay in step for the whole chirp and the FFT returns one peak.
::::

::::{frame} The Range FFT
:::{present}
$$
R = \frac{cT_s}{2B}\left(f - f_0\right)
$$

- One chirp: 300 samples at 0.6 MSPS, one FFT.
- Each FFT bin is 2 kHz, one 0.30 m range cell.
:::
:::{present}
<img src="../../viz/img/L28-range-profile.svg" alt="Power in dBFS against range from minus 0.3 to 8 m, with a top axis of beat frequency above the 0 m frequency from 0 to 53 kHz. Three peaks: leakage at 0 m near minus 20 dBFS, a corner reflector at 2.0 m near minus 20 dBFS, and the far wall at 5.5 m near minus 31 dBFS, over a floor near minus 84 dBFS" style="max-width: 640px; width: 100%; display: block; margin: 0 auto;">
:::

The PHASER's Pluto samples the beat at $f_s = 0.6$ MSPS, so one 0.5 ms chirp is $N = 300$ complex samples. The FFT of those samples is the **range profile**: each bin is a frequency, and the beat-per-meter relation converts it to a range,

$$
R = \frac{cT_s}{2B}\left(f - f_0\right),
$$

where $f_0$ is the 0 m frequency of the next frame. The bins are $f_s/N = 2$ kHz apart, which is 0.30 m, one resolution cell. Padding the record with zeros before the FFT, to 1024 or 4096 points, draws the same spectrum on a finer grid and makes the peaks easier to read, but it does not resolve anything new.

The figure is one chirp from the lab's recorded data: a 10 cm corner reflector at 2.0 m, the transmit antenna's direct path into the array at 0 m, and the far wall at 5.5 m. The top axis shows the same profile as beat frequency above $f_0$, at 6.67 kHz per meter.

The FFT also integrates. The 300 samples of a steady tone add in phase while the noise adds in power, so the tone rises $10\log_{10}300 = 24.8$ dB above the noise per sample, as <a href="../L27-radar-detection/index.html#frame-integrating-pulses">Lesson 27</a> described. Seen another way, each bin listens to only 2 kHz of noise. That is the narrowing <a href="../L25-radar-equation/index.html#frame-signal-to-noise-ratio">Lesson 25</a> promised: the corner at 3 m, 31.1 dB above the noise in 1 MHz, stands $31.1 + 10\log_{10}(1\ \text{MHz}/2\ \text{kHz}) = 58.1$ dB above it in one bin.
::::

::::{frame} The 0 m Frequency
:::{present}
- The kit offsets the outgoing chirp by about 100 kHz, so a 0 m echo lands at $f_0 \approx 100$ kHz.
- Each kit's $f_0$ differs slightly; calibrate it with a plate held against the array.
- The leakage spike always sits at $f_0$.
:::

The PHASER does not put a 0 m echo at zero frequency. The Pluto transmits its tone offset by `signal_freq` in ADI's scripts, about 100 kHz, from the frequency the receiver compares the echo with, so every beat lands about 100 kHz above zero. That keeps the targets clear of zero frequency, where the receiver's own offset and low-frequency noise sit. The offset is not exactly 100 kHz on every kit, and the cables and the board add a little delay of their own, so each kit has its own **0 m frequency** $f_0$, and the range equation measures beats from it.

The calibration is simple. Hold a flat metal plate against the array face, read the frequency of the peak, and record it as $f_0$; ADI's lab expects a value such as 99 or 103 kHz. With the plate gone, a peak stays at $f_0$: it is the transmit antenna's direct path into the array, the **leakage**, and it marks 0 m on every capture you take. A kit whose $f_0$ is off by 1 kHz reports every range 0.15 m long or short.
::::

::::{frame} Range the Sample Rate Allows
:::{present}
$$
\begin{aligned}
R_\text{max} &= \frac{cT_s}{2B}\left(\frac{f_s}{2} - f_0\right) \\
&= \frac{300\ \text{kHz} - 100\ \text{kHz}}{6.67\ \text{kHz/m}} = 30\ \text{m}
\end{aligned}
$$

- 250 MHz or 1 ms doubles it to 60 m.
:::

The Pluto samples complex data at $f_s$, so it can represent beat frequencies up to $f_s/2 = 300$ kHz. A target far enough away to put its beat above that limit aliases: it reappears at a wrong frequency, and the range profile shows it at a wrong range. With the 0 m frequency at 100 kHz, the beats above it have 200 kHz of room, so the farthest range the profile reports is

$$
\begin{aligned}
R_\text{max} &= \frac{cT_s}{2B}\left(\frac{f_s}{2} - f_0\right) \\
&= 30\ \text{m}.
\end{aligned}
$$

This limit comes from the sample rate, not from the transmit power; <a href="../L25-radar-equation/index.html#frame-maximum-range">Lesson 25</a> put the detection range of a 10 cm corner near 8.5 m in a 1 MHz bandwidth, and further out in the 2 kHz of one bin. A slower slope reaches further: halving $B$ or doubling $T_s$ halves the beat per meter and doubles $R_\text{max}$ to 60 m. Halving $B$ also doubles the resolution cell, so the two settings trade reach against resolution in different ways, which the lab measures.
::::

::::{frame} Windowing the Chirp
:::{present}
<img src="../../viz/img/L28-windows.svg" alt="Range profiles from 0.5 to 4 m of a strong target at 2.0 m and a target 40 dB weaker at 2.9 m. With a rectangular window the sidelobes of the strong target sit 20 to 35 dB down and hide the weak one. With a Hann window the main lobe is wider, the sidelobes fall below minus 50 dB, and the weak target shows" style="max-width: 620px; width: 100%; display: block; margin: 0 auto;">
:::
:::{present}
- Rectangular: sidelobes at $-13$ dB hide weak targets.
- Hann: sidelobes at $-31$ dB, a main lobe 1.6 times wider, 1.8 dB less SNR.
:::

An FFT of one chirp treats the record as if it started and stopped abruptly, which gives each tone a $\sin x/x$ response with sidelobes $13$ dB below the peak, falling slowly. A strong target's sidelobes then cover the bins around it, and a weak target nearby disappears under them. In the figure the second target, 40 dB weaker and 0.9 m beyond the first, is invisible with the rectangular window.

Multiplying the samples by a **window** that tapers smoothly to zero at both ends of the chirp lowers the sidelobes. The Hann window, $w[n] = \tfrac{1}{2}\left(1 - \cos(2\pi n/N)\right)$, puts the first sidelobe at $-31$ dB and the rest falling fast, and the weak target appears. This is the amplitude taper of <a href="../../module03/L22-sidelobes-tapering/index.html">Lesson 22</a> applied in time instead of across the array, with the same consequences: the main lobe widens, from a 3 dB width of 0.89 bins to 1.44 bins, so two equal targets one cell apart may merge, and the window discards some signal energy, a 1.8 dB loss in SNR. The course uses Hann by default; the rectangular window is the choice only when two equal targets must be split at the edge of the resolution.
::::

::::{frame} The Range Waterfall
:::{present}
<img src="../../viz/img/L28-waterfall.svg" alt="Range profiles from 0 to 6 m stacked in time over 10 s, darker for stronger echoes. A dark vertical band at 0 m is the leakage and one at 5.5 m is the wall. A zigzag trace runs from 1 m out to 4 m and back twice: a person walking" style="max-width: 620px; width: 100%; display: block; margin: 0 auto;">
:::
:::{present}
- Each row is one range profile; time runs up.
- Fixed objects draw vertical lines; a walker draws a zigzag.
- The slope of the trace is the walker's speed.
:::

One range profile is a snapshot. Stacking the profiles of successive chirps, one row per chirp and darker for a stronger echo, gives the **range waterfall**: range across, time up. A fixed object, the leakage at 0 m or the wall at 5.5 m, keeps the same range in every row and draws a vertical line. A person walking from 1 m out to 4 m and back draws a zigzag, and the slope of each leg is the walking speed: 3 m in 3 s is 1 m/s.

The waterfall records range against time and nothing else. Its rows here are 50 ms apart, one profile each time the display updates, and over 50 ms a walker's carrier phase changes by many cycles, so successive rows say nothing about the walker's velocity except through the range they show. <a href="../L29-range-doppler-mti/index.html">Lesson 29</a> takes chirps a fixed 0.5 ms apart and reads the velocity from that phase.
::::

::::{frame} Your Range Code
:::{present}
```python
C = 3.00e8

def range_axis(cap, n_fft):
    fs, B = cap["fs"], cap["B"]
    f = np.fft.fftshift(
        np.fft.fftfreq(n_fft, 1 / fs))
    k = C * cap["T_ramp"] / (2 * B)
    return (f - cap["f0"]) * k
```

- You write `range_profile` and `waterfall` in the lab.
- `radar_lab.py` grows through L29, L30, and L31.
:::

The four labs that follow chain together through one Python module, `radar_lab.py`, which you write and keep, and one capture format. A capture is an `.npz` file holding `iq`, the complex beat samples with one chirp a row, shape `n_chirps × n_samples`; the sample rate `fs`; the carrier `fc`; the bandwidth `B`; the chirp length `T_ramp`, the lesson's $T_s$; the time `PRI` from one chirp to the next; and `f0`, the 0 m frequency from your calibration. The excerpt is the start of the module. `range_axis` gives the range of each bin of an `fftshift`-ed FFT of length `n_fft`, by the range equation of the range FFT frame, with `k` the meters per hertz of beat. The module starts with a loader that turns a capture into a dictionary of numbers:

```python
def load_capture(path):
    with np.load(path) as z:
        cap = {k: z[k] for k in z.files}
    for k in ("fs", "fc", "B", "T_ramp",
              "PRI", "f0"):
        cap[k] = float(cap[k])
    return cap
```


The L28 Lab adds two functions. `range_profile(cap, chirp=0, window="hann")` windows one chirp, takes its FFT, and returns the ranges at or beyond 0 m with the power in dB, `(r, p_db)`. `waterfall(cap)` does the same for every chirp and returns `(r, t, w_db)`, with one row of `w_db` per chirp and `t` the chirp times. Normalize the FFT by the sum of the window, so that a tone of amplitude 1 reads 0 dBFS whatever the window. Use numpy, scipy, and matplotlib only. <a href="../L29-range-doppler-mti/index.html">Lesson 29</a> adds `range_doppler` and `mti`, <a href="../L30-cfar/index.html">Lesson 30</a> adds `cfar_2d`, and <a href="../L31-classification-tracking/index.html">Lesson 31</a> adds the spectrogram, a classifier, and a tracker, each calling the functions before it.
::::

::::{frame} L28 Lab: FMCW Range
:::{present}
- Calibrate $f_0$, then place a plate at 1, 2, and 3 m: measure the kHz per meter.
- Predict, then measure, 250 MHz and 1 ms.
- Read the waterfall; write your own range FFT.
:::

The L28 Lab measures everything this lesson derived, on your own kit: the 0 m frequency, the beat per meter, how the bandwidth and the chirp length change it, and the range waterfall. It ends with your own Python range FFT run on a capture you saved, which is the code the L29 Lab starts from. You work the lab on your own, outside class, and turn in one packet in three parts: **Part 1, Pre-Lab**, the predictions, before you go to the bench; **Part 2, Measurements**, from your own kit; and **Part 3, Writeup**, after it. The packet is checked and returned with feedback. It is the first piece of scaffolding for your final report, and it is not the report.

The procedure is <a href="https://analogdevicesinc.github.io/system-level/solutions/platforms/phaser/labs/radar-fmcw/" target="_blank" rel="noopener">ADI's FMCW lab</a> with the course's numbers: a 10 GHz carrier, 500 MHz in 0.5 ms, and $c = 3.00\times 10^8$ m/s. The <a href="https://analogdevicesinc.github.io/system-level/solutions/platforms/phaser/labs/radar-setup/" target="_blank" rel="noopener">radar setup page</a> describes the transmit path.
::::

::::{frame} Predict Before You Measure
:::{present}
| $B$ | $T_s$ | kHz per meter | $\Delta R$ | $R_\text{max}$ |
| :-- | :-- | --: | --: | --: |
| 500 MHz | 0.5 ms | 6.67 | 0.30 m | 30 m |
| 250 MHz | 0.5 ms | 3.33 | 0.60 m | 60 m |
| 500 MHz | 1 ms | 3.33 | 0.30 m | 60 m |
:::

The table is the core of Part 1. Every number in it follows from the beat-frequency and resolution frames, with $f_s = 0.6$ MSPS and $f_0 = 100$ kHz, and the bench checks each column. The beat per meter is the slope of the line through your 1, 2, and 3 m readings. The resolution shows as the width of the peak: at 250 MHz the peak from the same plate is twice as wide in range. The reach is not something the lab can walk out to, but your own range axis shows where it ends. Doubling the chirp length also doubles the samples in each chirp, so the noise floor of the range profile should drop by 3 dB while the target stays where it was.
::::

::::{frame} Bench Rules
:::{present}
- Transmit antenna on **OUT2**, before you power the kit.
- Stand clear of the beam while you measure a static target.
- Use a flat metal plate, square to the array, at array height.
:::

A static target is only static if nothing else moves. Your own body is a larger reflector than a small plate, so step behind the kit or well to one side while you read a static range; otherwise your echo adds a moving peak near the target's and the profile you save is not the one you meant to save. Keep the beam's path clear of walls and furniture for at least 4 m if you can, and expect the far wall to show up as a peak of its own.

Any flat metal plate about 20 cm on a side works, and so does aluminum foil glued smoothly to cardboard. A plate reflects strongly only when it faces the array squarely, so turn it slowly until its peak is highest before you read the frequency. A trihedral folded from three foil-covered cardboard squares is more forgiving of its angle. The course has only one or two commercial corner reflectors; no step needs one, and if one is free, Part 2 has an optional reading for it. Measure range from the array face to the plate's front with a tape measure.
::::

::::{frame} What You Keep
:::{present}
- `radar_lab.py`, with your four L28 functions.
- Your captures: the 2 m plate and the walk.
- Your $f_0$ and your measured kHz per meter.
:::

The L29 Lab starts from your own L28 code and data, so keep the module and the captures you saved, with their file names written in your packet. For the final report, keep three results from this lab: the beat per meter you measured against the 6.67 kHz the lesson predicts, the resolution you saw at 500 and 250 MHz, and a waterfall you can explain line by line. The report asks you to explain how a chirp becomes a range measurement and what resolution you actually reached, in your own words; the packet's tables are the evidence for it, not the explanation.
::::

::::{frame} Equipment and Setup
:class: read-only

You need:

- the ADALM-PHASER kit with its Raspberry Pi and Pluto attached, and its transmit antenna;
- a flat metal plate about 20 cm on a side, or foil glued to cardboard;
- a tape measure and about 4 m of clear floor in front of the kit;
- a laptop on the kit's network with Python 3, numpy, scipy, and matplotlib.

The course's Phaser app runs the radar in its FMCW mode. That mode is still being finished, so its control names and layout are not yet known; this page names each setting by the quantity it sets, and where the app's label differs, use the app's. ADI's <a href="https://github.com/analogdevicesinc/system-level/blob/main/docs/solutions/platforms/phaser/labs/resources/python/FMCW_RADAR_Waterfall.py" target="_blank" rel="noopener">`FMCW_RADAR_Waterfall.py`</a> makes the same measurements from a script, with a bandwidth slider, a range toggle, and a chirp length set in its `ramp_time` variable; its 12.145 GHz carrier does not change the beat per meter.

1. With the kit powered off, connect the transmit antenna to **OUT2**.
2. Power the kit, wait for the Pi to boot, open the Phaser app, and select its FMCW mode.
3. Set the chirp bandwidth to **500 MHz** and the chirp length to **0.5 ms**. Show the FFT against **frequency**, not range, for Procedures A to C.
4. Find the app's control that saves a capture, and check that it writes an `.npz` file with the keys of the capture format. Write each file name in the packet as you save it.
::::

::::{frame} No Hardware?
:class: read-only

```{note}
If your kit will not produce a clean capture, use the course's recorded data
instead and run every procedure on it with your own code. The files are in the
lab's capture format, from a simulation of the PHASER at the course's settings
with a kit whose 0 m frequency is 101.4 kHz; a 10 cm corner reflector stands in
for the plate. Say in your packet which captures are recorded rather than your own.

- <a href="../../radar-data/L28_cal_0m.npz">L28_cal_0m.npz</a>: a plate against the array, for Procedure A
- <a href="../../radar-data/L28_corner_1m.npz">L28_corner_1m.npz</a>, <a href="../../radar-data/L28_corner_2m.npz">L28_corner_2m.npz</a>, <a href="../../radar-data/L28_corner_3m.npz">L28_corner_3m.npz</a>: Procedure B
- <a href="../../radar-data/L28_corner_2m_B250.npz">L28_corner_2m_B250.npz</a>, <a href="../../radar-data/L28_corner_2m_T1ms.npz">L28_corner_2m_T1ms.npz</a>: Procedure C
- <a href="../../radar-data/L28_walker.npz">L28_walker.npz</a>: a person walking from 1 m to 4 m and back, Procedure D
```
::::

::::{frame} Procedure A: Calibrate the 0 m Frequency
:class: read-only

1. Clear the bench in front of the kit and start the radar. One peak stands near 100 kHz: the leakage from the transmit antenna into the array. Record its frequency in Table A.
2. Hold the plate flat against the array face, covering the patches. Read the frequency of the strongest peak and record it as $f_0$ in Table A. ADI's lab expects a value near 100 kHz, such as 99 or 103 kHz.
3. If the app has a 0 m calibration setting, enter $f_0$ there, so that its range axis reads 0 m at your kit's 0 m frequency. If it does not, keep your $f_0$ for your own range axis; the capture's `f0` field should carry it.
4. Save a capture with the plate against the array.
::::

::::{frame} Procedure B: Static Ranges
:class: read-only

1. Stand the plate at **1.00 m** from the array face, at array height, facing the array squarely. Step out of the beam.
2. Turn the plate slowly until its peak is highest. Read the peak's frequency and record it in Table B with the tape-measure range.
3. Save a capture.
4. Repeat at **2.00 m** and **3.00 m**. At each range, check that the peak moved by about 6.7 kHz a meter before you record it; a peak that did not move is the leakage or the wall.
5. If one of the course's corner reflectors is free, put it at 3.00 m instead of the plate and record its peak level and the noise floor near 10 m, in dBFS, in the optional row of Table B.
::::

::::{frame} Procedure C: Bandwidth and Chirp Length
:class: read-only

Write your Part 1 predictions in Table C before you change anything.

1. Put the plate back at **2.00 m**, step clear, and record its frequency at 500 MHz and 0.5 ms as the reference row.
2. Set the bandwidth to **250 MHz**. Record the peak's frequency, and save a capture.
3. Set the bandwidth back to 500 MHz and the chirp length to **1 ms**. Record the peak's frequency, and save a capture.
4. Return the chirp length to **0.5 ms**.

In ADI's script the bandwidth takes effect when you press **Set RF Bandwidth**, and the chirp length is the `ramp_time` variable in microseconds, set before you run it. Whether the Phaser app changes the chirp length from its panel is not yet known.
::::

::::{frame} Procedure D: Read the Waterfall
:class: read-only

1. Switch the FFT's axis from frequency to **range**, and open the waterfall.
2. Stand 1 m in front of the kit, facing it. Walk slowly straight out to about 4 m and back, about one step a second, twice. Then hold a hand 0.5 m from the array and move it toward and away from the array.
3. If clutter fills the waterfall, raise its low intensity limit until the fixed lines are faint and your trace is still dark; ADI's script calls these the LOW and HIGH levels.
4. Save a capture of the walk covering at least 5 s. Record in Table D the nearest and farthest ranges your trace reached and the time of one leg.
::::

::::{frame} Procedure E: Your Own Range FFT
:class: read-only

Do this part on your laptop after the bench, from your saved captures.

1. Start `radar_lab.py` with `import numpy as np`, then `load_capture` and `range_axis` from the Your Range Code frame, and add `range_profile(cap, chirp=0, window="hann")` and `waterfall(cap)` as that frame describes.
2. Run `range_profile` on your 2 m capture. Find the peak beyond 0.5 m and record its range and level, and the floor near 10 m, in Table E. Plot it from 0 to 8 m.
3. Run it again with `window=None` (rectangular) on the same chirp, and plot the two together. Record the level of the strongest sidelobe of the plate's peak for each window.
4. Run `range_profile` on your 250 MHz and 1 ms captures and compare their peaks with the 500 MHz, 0.5 ms one: the width in range, and the floor.
5. Run `waterfall` on your walk capture and plot it with time up and range across, from 0 to 6 m. Mark the leakage, the wall, and your trace.
6. Keep `radar_lab.py`, the captures, and the plots. The L29 Lab starts from them.
::::

::::{frame} Lab Packet
:class: read-only doc-links

- <a class="doc-link" href="../../labs/ECE444_Lab_L28_FMCWRange_blank.pdf" target="_blank" rel="noopener">L28 Lab packet (PDF)</a>
::::

::::{frame} Summary
:class: read-only

| Idea | What it is | Number to remember |
| :-- | :-- | :-- |
| Beat frequency | $f_b = 2RB/(cT_s)$, the echo compared with the chirp still going out | 6.67 kHz per meter at 500 MHz, 0.5 ms |
| Beat cycles a chirp | $f_bT_s = 2RB/c$ | 3.33 cycles per meter at 500 MHz |
| Range resolution | one FFT bin, $1/T_s$, is $c/2B$ in range | 0.30 m at 500 MHz, 0.60 m at 250 MHz |
| Range from frequency | $R = cT_s(f - f_0)/2B$ | bins 2 kHz apart at 0.6 MSPS, 0.5 ms |
| 0 m frequency | $f_0$, calibrated per kit; the leakage sits there | about 100 kHz |
| Reach | $R_\text{max} = cT_s(f_s/2 - f_0)/2B$ | 30 m at 0.6 MSPS |
| FFT integration | 300 samples add in phase | 24.8 dB, a 2 kHz noise bandwidth |
| Hann window | sidelobes $-31$ dB instead of $-13$ dB | main lobe 1.6 times wider, 1.8 dB SNR loss |
| Waterfall | range profiles stacked in time | slope of a trace is the speed |
::::

::::{frame} Looking Ahead
:::{present}
- **L29** stacks 256 chirps, 0.5 ms apart, and reads velocity from their phase.
- Your `range_profile` is the first FFT of its range-Doppler map.
:::

This lesson used one chirp at a time and threw away its phase. <a href="../L29-range-doppler-mti/index.html">Lesson 29</a> keeps it. A burst of 256 chirps, each 300 µs long and repeated every 0.5 ms, gives each target a phase that advances from chirp to chirp at its Doppler frequency, and a second FFT across the chirps reads that frequency as a velocity, with the resolution $\lambda/(2MT_\text{PRI}) = 0.12$ m/s of <a href="../L26-range-resolution-doppler/index.html#frame-doppler-resolution-and-ambiguity">Lesson 26</a>. The first FFT of that map is the range FFT you wrote here, applied to every chirp of the burst. Moving target indication, in the same lesson, removes the fixed lines of the waterfall, the leakage and the wall, so that only what moves remains.
::::
