---
frame_view: true
---

# L28 - FMCW on the Phaser

::::{frame}
:class: title-frame

<div class="course-mark">ECE 444 · Fall 2026</div>

<h1 class="frame-title">FMCW on the Phaser</h1>

<div class="title-rule"></div>

Calibrate 0 m, then measure range, resolution, and a walk on your own kit.

Lesson 28 and the L28 Lab · Antennas, Phased Arrays, and Radar Systems · Dr. Neil Rogers
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
This page is the lesson and the L28 Lab together. Read the lesson half before class and do Part 1 of the lab packet from it; in class we work the lab half on your kit. <a href="../L26-range-resolution-doppler/index.html">Lesson 26</a> measured range as a round-trip delay and showed that a chirp gives a long transmission the resolution of a short pulse, $\Delta R = c/2B$. It left one problem open: a target 3 m away returns its echo after 20 ns, far too short for the PHASER's 0.6 MSPS receiver to time. The lesson shows how a frequency-modulated continuous-wave (FMCW) radar converts that delay into a frequency of a few kilohertz, how one FFT turns the frequency back into range, and what sets the resolution and the farthest range the radar can report. The lab then measures each of those on your kit, and it is the first stage of the radar your final report describes.
:::
::::

::::{frame} A Chirp and Its Echo
:class: read-only

:::{present}
<img src="../../viz/img/L28-chirp.svg" alt="Frequency against time. The transmitted chirp is a straight ramp repeated twice. The echo is the same ramp shifted right by the delay. At any instant the two differ by a fixed frequency, the beat. The ramp spans the bandwidth vertically and the chirp length horizontally" style="max-width: 620px; width: 100%; display: block; margin: 0 auto;">
:::
:::{present}
- The transmitter sweeps $B$ in $T_s$, then starts again.
- The echo is the same ramp, late by the round trip.
- The gap between them, the **beat**, is constant.
:::

An FMCW radar transmits continuously, and its frequency climbs linearly across a bandwidth $B$ during each **chirp** of length $T_s$. The echo from a target at range $R$ is a copy of the transmitted chirp delayed by the round trip,

$$
\tau = \frac{2R}{c},
$$

which is 6.7 ns for every meter. The receiver compares the echo with the chirp that is still going out. Because both ramps climb at the same rate, the echo is always below the transmitted chirp by the same frequency, and that difference is the **beat frequency** $f_b$.

The lab runs the Phaser app's presets, and the packet gives their settings. This lesson works every method on a chirp that no preset uses, $B = 400$ MHz in $T_s = 2$ ms from 10.0 GHz, so that each worked number shows the method and leaves the preset's numbers for Part 1. The figure exaggerates the delay so that it is visible: a target at 3 m delays the echo by 20 ns, 0.001% of a 2 ms chirp.
::::

::::{frame} The Beat Frequency
:class: read-only

:::{present}
$$
\begin{aligned}
f_b &= \frac{B}{T_s}\ \tau = \frac{2RB}{cT_s} \\
&= \frac{2\ (1\ \text{m})(400\ \text{MHz})}{(3.00\times 10^8\ \text{m/s})(2\ \text{ms})} \\
&= 1.33\ \text{kHz}
\end{aligned}
$$
:::

The transmitted frequency rises at the **chirp slope** $B/T_s$, which for the worked chirp is $400\ \text{MHz}/2\ \text{ms} = 0.2\ \text{MHz}$ per microsecond. In the delay $\tau$ the chirp climbs $\tau B/T_s$, so the beat frequency is

$$
\begin{aligned}
f_b &= \frac{B}{T_s}\ \tau \\
&= \frac{2RB}{cT_s} .
\end{aligned}
$$

The beat is proportional to range, so the radar reads range by measuring a frequency. For the worked chirp a target at 1 m gives 1.33 kHz and one at 3 m gives 4.00 kHz. These frequencies are low enough for the Pluto to sample directly, even though the chirp itself spans 400 MHz: comparing the echo with the outgoing chirp removes the sweep and leaves only the small difference that carries the range. <a href="https://analogdevicesinc.github.io/system-level/solutions/platforms/phaser/labs/radar-fmcw/" target="_blank" rel="noopener">ADI's FMCW lab</a> calls this stretch processing.

The PHASER adds every beat to a fixed offset, the 0 m frequency $f_0$ of a later frame, about 100 kHz. A target's peak therefore sits at $f_0 + f_b$: for the worked chirp, a target at 4 m peaks at $100 + 4 \times 1.33 = 105.33$ kHz.

The kHz per meter depends on both waveform settings. Quartering the bandwidth to 100 MHz quarters it, to 0.33 kHz per meter, and quartering the chirp length to 0.5 ms quadruples it, to 5.33 kHz per meter. As the next frames show, only the bandwidth changes the resolution.
::::

::::{frame} FMCW Explorer
:class: viz-frame read-only

:::{depth}
The left panel is the beat signal over one chirp, with the 0 m frequency removed, and the right panel is its range spectrum, the FFT of those samples with the frequency axis converted to range. It opens on the worked chirp, 400 MHz in 2 ms. Move the target and count the cycles: every meter adds $2B/c = 2.67$ cycles a chirp at 400 MHz. Change the bandwidth or the chirp length and watch the beat per meter follow $B/T_s$. Turn on the second target and bring it in toward the first until the two peaks merge; the green bar is $c/2B$. Then set the second target 20 to 40 dB weaker and switch between the rectangular and Hann windows.
:::

<iframe src="../../viz/fmcw-beat.html"
        width="100%" height="435"
        style="border: 1px solid #cddce9; border-radius: 6px;"
        loading="lazy"
        title="FMCW explorer: the beat signal over one chirp and its range spectrum, for chosen range, bandwidth, chirp length, second target, and window">
</iframe>
::::

::::{frame} Range Resolution
:class: read-only

:::{present}
$$
\begin{aligned}
\Delta f_b &= \frac{1}{T_s} \\
\Delta R &= \frac{cT_s}{2B}\ \Delta f_b = \frac{c}{2B}
\end{aligned}
$$

- Two targets separate when their beats differ by one cycle a chirp.
- The chirp length cancels: only $B$ sets the resolution.
:::

The radar sees each target's beat for one chirp, $T_s$, and an FFT over a record of length $T_s$ separates two tones only if they differ by at least $1/T_s$. Over one chirp, that is a difference of one cycle. Converting that frequency step to range with the beat per meter gives

$$
\begin{aligned}
\Delta R &= \frac{cT_s}{2B}\ \Delta f_b \\
&= \frac{cT_s}{2B}\cdot\frac{1}{T_s} \\
&= \frac{c}{2B} ,
\end{aligned}
$$

which is the result of <a href="../L26-range-resolution-doppler/index.html#frame-resolution-and-bandwidth">Lesson 26</a>. At 400 MHz it is 0.375 m. A longer chirp makes the beat per meter smaller but lets the FFT resolve finer frequency steps in the same proportion, so $T_s$ cancels. Quartering the bandwidth to 100 MHz quadruples the resolution cell to 1.5 m; quartering the chirp length leaves it at 0.375 m.

The number of beat cycles in one chirp is $f_bT_s = 2RB/c$, which does not depend on $T_s$ either. Two targets one cell apart differ by exactly one cycle a chirp; closer than that, their beats stay within one cycle of each other for the whole chirp, and the FFT returns one peak however finely it is drawn.
::::

::::{frame} The Range FFT
:class: read-only

:::{present}
$$
R = \frac{cT_s}{2B}\left(f - f_0\right)
$$

- The app keeps the last 90% of each chirp; one FFT of those samples is a range profile.
- One FFT bin is $f_s/N$ in frequency, one cell in range.
:::
:::{present}
<img src="../../viz/img/L28-range-profile.svg" alt="Power in dBFS against range from minus 0.3 to 8 m for the worked chirp, with a top axis of beat frequency above the 0 m frequency from 0 to about 10.7 kHz. Three peaks: leakage at 0 m near minus 20 dBFS, a corner reflector at 2.0 m near minus 20 dBFS, and the far wall at 5.5 m near minus 31 dBFS, over a floor near minus 85 dBFS" style="max-width: 640px; width: 100%; display: block; margin: 0 auto;">
:::

The PHASER's Pluto samples the beat at $f_s = 0.6$ MSPS. The Phaser app discards the first 10% of each chirp, while the frequency ramp settles, and keeps the rest: for the worked chirp, $0.9 \times 2\ \text{ms} \times 0.6$ MSPS gives $N = 1080$ complex samples. The FFT of those samples is the **range profile**: each bin is a frequency, and the beat-per-meter relation converts it to a range,

$$
R = \frac{cT_s}{2B}\left(f - f_0\right),
$$

where $f_0$ is the 0 m frequency of the next frame. The bins are $f_s/N = 0.556$ kHz apart, which at 1.33 kHz per meter is 0.417 m. That is a little more than the 0.375 m of the resolution frame because the 1.8 ms the app keeps sweeps 360 MHz, not 400, and $c/(2 \cdot 360\ \text{MHz}) = 0.417$ m. Padding the record with zeros before the FFT, to 4096 points or more, draws the same spectrum on a finer grid and makes the peaks easier to read, but it does not resolve anything new.

The figure is one chirp of the worked waveform from the course's simulated room: a 10 cm corner reflector at 2.0 m, the transmit antenna's direct path into the array at 0 m, and the far wall at 5.5 m. The top axis shows the same profile as beat frequency above $f_0$, at 1.33 kHz per meter.

The FFT also integrates. The 1080 samples of a steady tone add in phase while the noise adds in power, so the tone rises $10\log_{10}1080 = 30.3$ dB above the noise per sample, as <a href="../L27-radar-detection/index.html#frame-integrating-pulses">Lesson 27</a> described. Seen another way, each bin collects noise from only 0.556 kHz. That is the narrowing <a href="../L25-radar-equation/index.html#frame-signal-to-noise-ratio">Lesson 25</a> described: the corner at 3 m, 31.1 dB above the noise in 1 MHz, stands

$$
\begin{aligned}
\text{SNR}_\text{bin} &= 31.1\ \text{dB} + 10\log_{10}\frac{1\ \text{MHz}}{0.556\ \text{kHz}} \\
&= 63.7\ \text{dB}
\end{aligned}
$$

above it in one bin. The record length sets that height. A window-normalized FFT reads a tone at the same level whatever the record, while the noise in one bin is spread over $1/T$ of bandwidth, so a record a quarter as long puts four times the noise in each bin and the same target stands $10\log_{10}4 = 6$ dB lower above the floor.
::::

::::{frame} The 0 m Frequency
:class: read-only

:::{present}
- The kit offsets the outgoing chirp by about 100 kHz, so a 0 m echo lands at $f_0 \approx 100$ kHz.
- Each kit's $f_0$ differs; **Calibrate…** reads it from a plate against the array.
- The leakage spike always sits at $f_0$.
:::

The PHASER does not put a 0 m echo at zero frequency. The Pluto transmits its tone offset by `signal_freq` in ADI's scripts, the app's 100 kHz IF tone, from the frequency the receiver compares the echo with, so every beat lands about 100 kHz above zero. That keeps the targets clear of zero frequency, where the receiver's own offset and low-frequency noise sit. The offset is not exactly 100 kHz on every kit, and the cables and the board add a little delay of their own, so each kit has its own **0 m frequency** $f_0$, and the range equation measures beats from it.

The calibration is simple. Hold a flat metal plate against the array face, read the frequency of the peak, and record it as $f_0$; ADI's lab expects a value such as 99 or 103 kHz. With the plate gone, a peak stays at $f_0$: it is the transmit antenna's direct path into the array, the **leakage**, and it marks 0 m on every capture you take. An error in $f_0$ moves every range by the same amount: for the worked chirp, 1 kHz of error reports every range 0.75 m long or short.
::::

::::{frame} Maximum Range from the Sample Rate
:class: read-only

:::{present}
$$
\begin{aligned}
R_\text{max} &= \frac{cT_s}{2B}\left(\frac{f_s}{2} - f_0\right) \\
&= \frac{300\ \text{kHz} - 100\ \text{kHz}}{1.33\ \text{kHz/m}} \\
&= 150\ \text{m}
\end{aligned}
$$
:::

The Pluto samples complex data at $f_s$, so it can represent beat frequencies up to $f_s/2$, 300 kHz at 0.6 MSPS. A target far enough away to put its beat above that limit aliases: it reappears at a wrong frequency, and the range profile shows it at a wrong range. With the 0 m frequency at 100 kHz, the beats above it have 200 kHz of room, so the farthest range the worked chirp reports is 150 m.

This limit comes from the sample rate, not from the transmit power; <a href="../L25-radar-equation/index.html#frame-maximum-range">Lesson 25</a> put the detection range of a 10 cm corner near 8.5 m in a 1 MHz bandwidth, and farther out in the narrow bin of one FFT. A slower slope reaches farther and a steeper one less far at the same sample rate, so a preset with a steeper chirp also samples faster. Narrowing $B$ reaches farther too, but it widens the resolution cell in the same proportion.
::::

::::{frame} Windowing the Chirp
:class: read-only

:::{present}
<img src="../../viz/img/L28-windows.svg" alt="Range profiles from 0.5 to 5.5 m of a strong target at 2.0 m and a target 30 dB weaker at 4.5 m, for the worked chirp. With a rectangular window the sidelobes of the strong target sit 20 to 35 dB down and hide the weak one. With a Hann window the main lobe is wider, the sidelobes fall below minus 50 dB, and the weak target shows" style="max-width: 620px; width: 100%; display: block; margin: 0 auto;">
:::
:::{present}
- Rectangular: sidelobes at $-13$ dB hide weak targets.
- Hann lowers the sidelobes to $-31$ dB but widens the main lobe 1.6 times and loses 1.8 dB of SNR.
:::

An FFT of one chirp treats the record as if it started and stopped abruptly, which gives each tone a $\sin x/x$ response with sidelobes $13$ dB below the peak, falling slowly. A strong target's sidelobes then cover the bins around it, and a weak target nearby disappears under them. In the figure the second target, 30 dB weaker and 2.5 m beyond the first, is invisible with the rectangular window.

Multiplying the samples by a **window** that tapers smoothly to zero at both ends of the chirp lowers the sidelobes. The Hann window,

$$
w[n] = \frac{1}{2}\left(1 - \cos\frac{2\pi n}{N}\right),
$$

puts the first sidelobe at $-31$ dB and the rest falling fast, and the weak target appears. This is the amplitude taper of <a href="../../module03/L22-sidelobes-tapering/index.html">Lesson 22</a> applied in time instead of across the array, with the same consequences: the main lobe widens, from a 3 dB width of 0.89 bins to 1.44 bins, so two equal targets one cell apart may merge, and the window discards some signal energy, a 1.8 dB loss in SNR. In range, a peak's width 3 dB down is 1.44 bins times the meters per bin: $1.44 \times 0.417 = 0.60$ m for the worked chirp. `radar_lab` uses Hann by default; the rectangular window is the choice only when two equal targets must be split at the edge of the resolution.
::::

::::{frame} The Range Waterfall
:class: read-only

:::{present}
<img src="../../viz/img/L28-waterfall.svg" alt="Range profiles from 0 to 6 m stacked in time over 10 s, darker for stronger echoes. A dark vertical band at 0 m is the leakage and one at 5.5 m is the wall. A zigzag trace runs from 1 m out to 4 m and back twice: a person walking" style="max-width: 620px; width: 100%; display: block; margin: 0 auto;">
:::
:::{present}
- Each row is one range profile; time runs up.
- Fixed objects draw vertical lines; a walker draws a zigzag.
- The slope of the trace is the walker's speed.
:::

One range profile is a snapshot. Stacking the profiles of successive chirps, one row per chirp and darker for a stronger echo, gives the **range waterfall**: range across, time up. A fixed object, the leakage at 0 m or the wall at 5.5 m, keeps the same range in every row and draws a vertical line. A person walking from 1 m out to 4 m and back draws a zigzag, and the slope of each leg is the walking speed: a 3 m leg in 3 s gives 1 m/s.

The waterfall records range against time and nothing else. Its rows here are 50 ms apart, one profile each time the display updates, and over 50 ms a walker's carrier phase changes by many cycles, so successive rows say nothing about the walker's velocity except through the range they show. <a href="../L29-range-doppler-mti/index.html">Lesson 29</a> takes chirps a fixed 0.5 ms apart and reads the velocity from that phase.
::::

::::{frame} The Provided Range FFT
:class: read-only

:::{present}
```python
def range_fft(cap, window="hann",
              n_fft=None):
    iq = cap["iq"]
    w = _window(window, iq.shape[1])
    X = np.fft.fft(iq * w, n_fft or
                   iq.shape[1], axis=1)
    return X / w.sum()
```

- The course provides `radar_lab.py`, complete.
- Each lab's notebook changes a line or two of it.
:::

The four labs that follow share one Python module, <a href="../../notebooks/radar_lab.py">`radar_lab.py`</a>, and one capture format. The course provides the module complete: you run it from a notebook, one for each lab, and each lab's tasks change a parameter or a line or two, never a whole function. The excerpt is the function this lesson describes: it windows every chirp, takes the FFT along each one, and divides by the sum of the window, so that a tone of amplitude 1 reads 0 dBFS whatever the window. `n_fft` larger than the samples in a chirp zero-pads it. The result has one row per chirp and one column per range bin.

A capture is an `.npz` file holding `iq`, the complex beat samples of the summed array with one chirp a row, shape `n_chirps × n_samples`; optionally `iq_ch`, the same samples from the array's two halves, shape `2 × n_chirps × n_samples`, which <a href="../L31-classification-tracking/index.html">Lesson 31</a> uses to measure angle; the sample rate `fs`; the carrier `fc`; the bandwidth `B`; the chirp length `T_ramp`, the lesson's $T_s$; the time `PRI` from one chirp to the next; and `f0`, the 0 m frequency from your calibration, or the 100 kHz IF tone in a capture saved before it. The number of chirps is not fixed: 32 in an L28 range capture, 256 in the L29 burst, and thousands in a record of several seconds. The range of each bin comes from `range_axis`, the range equation of the range FFT frame with `k` the meters per hertz of beat:

```python
def range_axis(cap, n_fft=None):
    n = n_fft or cap["iq"].shape[1]
    f = np.fft.fftfreq(n, 1 / cap["fs"])
    k = C * cap["T_ramp"] / (2 * cap["B"])
    return (f - cap["f0"]) * k
```

The bins come out in the order `np.fft.fft` returns them, and the bins below $f_0$ come out as negative ranges. Two more L28 functions build on `range_fft`: `range_profile(cap, chirp=0, window="hann")` returns one chirp's ranges at or beyond 0 m and its power in dB, `(r, p_db)`, and `waterfall(cap)` returns `(r, t, w_db)`, one row per chirp. <a href="../L29-range-doppler-mti/index.html">Lesson 29</a> uses `range_doppler` and `mti`, <a href="../L30-cfar/index.html">Lesson 30</a> uses `cfar_2d`, and <a href="../L31-classification-tracking/index.html">Lesson 31</a> uses the spectrogram, a classifier, and a tracker, all in the same module. The L28 notebook is <a href="../../notebooks/L28_range.ipynb">`L28_range.ipynb`</a>.
::::

::::{frame} Pre-Lab
:class: read-only doc-links

Part 1 of the L28 Lab packet is the pre-lab: the shaded Predicted cells of its tables, at the preset settings the packet gives. Do it before class from the frames above, and bring it: you check every reading you take in class against it.

| Packet table | You predict | Worked in | Checked in |
| :-- | :-- | :-- | :-- |
| Setup | samples per chirp, Range (Basic) and Range (Fast) | The Range FFT | Step 16 |
| A | the leakage and the plate's frequency, before calibration | The 0 m Frequency | Steps 3 to 5 |
| B | each plate's peak frequency, the beat per meter, and the intercept | The Beat Frequency | Steps 7 to 9 and 17 |
| C | peak frequency, kHz per meter, width, and height for three waveforms | The Beat Frequency, The Range FFT, Windowing the Chirp | Steps 10 to 12 and 17 |
| E | the peaks two corners 0.20 m apart make | Range Resolution | Step 19 |

The worked examples use 400 MHz in 2 ms at 10.0 GHz, which no preset runs, so they show each method and leave every Part 1 answer to you.

- <a class="doc-link" href="../../labs/ECE444_Lab_L28_FMCWRange_blank.pdf" target="_blank" rel="noopener">L28 Lab packet (PDF)</a>
::::

::::{frame} The Big Picture
:::{present}
| Steps | Set or switched | Table |
| :-- | :-- | :-- |
| 1–6 | clear range; plate on array | A |
| 7–9 | plate at 1, 2, 3 m | B |
| 10–12 | Range (Fast); 250 MHz capture | C |
| 13–15 | a walk | D |
| 16–20 | the notebook | B, C, E |
:::

The lab measures each thing the lesson derived, on your own kit, with the Phaser app's **Range (Basic)** preset as the reference waveform. Steps 1 to 6 bring the kit up and find its 0 m frequency. Steps 7 to 9 put the plate at three ranges and save a capture at each. Steps 10 to 12 change one setting at a time, the chirp length on the kit and the bandwidth from a recorded capture. Steps 13 to 15 read a walk on the range waterfall. Steps 16 to 20 run the course's notebook on what you saved: the app shows range, and the notebook reads the frequencies the range came from.
::::

::::{frame} Predict First
:class: viz-frame

:::{depth}
Before you change the waveform on the kit, predict what each change does to one target's peak, then check yourself. The widget starts from the lesson's worked chirp, 400 MHz in 2 ms, with one target at 4 m. Choose a chirp length and a bandwidth and decide, before you press **Show profile**: where the peak moves, whether it widens, and whether it stands higher or lower above the floor. Any change hides the profile again, so each guess comes first. The widget's chirp is not a preset, so its numbers are not your Part 1 values; the factors carry over to the kit.
:::

:::{present}
<iframe src="../../viz/fmcw-predict.html"
        width="100%" height="485"
        style="border: 1px solid #cddce9; border-radius: 6px;"
        loading="lazy"
        title="Choose a chirp length and bandwidth, predict the range profile of a target at 4 m, then show it against the reference chirp">
</iframe>
:::
::::

::::{frame} Bring Up and Calibrate
:::{present}
- Port 8081 of your kit, the **FMCW** tab, **Range (Basic)**, **Start**.
- Clear range: read the leakage in **Calibrate…**, then save.
- Plate on the array: save, then **Calibrate**.
:::

You need the kit with its transmit antenna, a flat metal plate about 20 cm on a side (or foil glued smoothly to cardboard), a tape measure, about 4 m of clear floor in front of the kit, and your laptop on the kit's network with the notebook set up as the Notebook Setup frame describes.

1. **Connect the antenna.** With the kit powered off, connect the transmit antenna to **OUT2**, then power the kit.
2. **Open the radar app.** Browse to `http://phaser-NN.local:8081`, with your kit's number, the radar half of the Phaser app. Choose the **FMCW** mode tab and open the **FMCW** section. Its status line should read **FMCW ready**; if it reads **FMCW limited**, hover over it for the reason and tell me, because a kit without chirp sync does not run the preset's chirp, and the recorded data then stand in for Tables B and C. Set **Preset** to **Range (Basic)**, leave **Range Max (m)** empty, and press **Start**. The **Range** tab shows one range profile per display update. If **0 m Beat (kHz)** holds a value from an earlier session, open **Calibrate…** and press **Reset**.
3. **Read the leakage.** Clear everything from in front of the kit and stand to one side, out of the beam. Open **Calibrate…**: the **Strongest return** is the leakage from the transmit antenna into the array, and its frequency is **New 0 m beat**. Record it, press **Cancel**, and press **Save Capture**. The app downloads `phaser_range_<date>-<time>.npz`; move it into your Module 4 folder and note its name.

   <div class="rec" data-lab="L28">
   <label>Step 3: leakage, New 0 m beat (kHz) <input data-field="a.leak.app"></label>
   </div>
4. **Save the plate on the array.** Hold the plate flat against the array face, covering the patches, and press **Save Capture**.
5. **Calibrate.** With the plate still there, open **Calibrate…**, wait for Strongest return to settle, record New 0 m beat as the app's $f_0$, and press **Calibrate**. **0 m Beat (kHz)** now holds it, the range axis reads 0 m there, and every capture you save from now on carries it as its `f0`. The range axis starts at 0 m, so a kit whose $f_0$ is below the 100 kHz IF tone puts the plate at a negative range, off the plot, and Strongest return finds something else; if the plate's peak is missing, type 95 in 0 m Beat (kHz) and open Calibrate… again.

   <div class="rec" data-lab="L28">
   <label>Step 5: f0, New 0 m beat (kHz) <input data-field="a.f0.app"></label>
   </div>
6. **Compare with Part 1.** The app reads frequencies to the nearest FFT bin, so its two readings can differ from your prediction by up to half a bin. The notebook reads both captures to 0.01 kHz in Step 17.
::::

::::{frame} Static Ranges
:::{present}
- Plate at 1, 2, and 3 m by the tape, square to the array.
- Hover over the plate's peak; record its range.
- **Save Capture** at each range.
:::

7. **Plate at 1.00 m.** Stand the plate 1.00 m from the array face by the tape, at array height. A plate reflects strongly only when it faces the array squarely, so on the **Range** tab turn it slowly until its peak is highest, then step out of the beam: your body is a larger reflector than the plate. Hover over the plate's peak, record its range, and press **Save Capture**. **Peak Range** shows the strongest return, which can be the leakage near 0 m rather than the plate, so read the plate's own peak.

   <div class="rec" data-lab="L28">
   <label>Step 7: range in the app, 1 m (m) <input data-field="b.1.app"></label>
   </div>
8. **Plate at 2.00 m.** Repeat at 2.00 m. Check that the plate's peak moved out by about 1 m before you save; a peak that did not move is the leakage or the wall.

   <div class="rec" data-lab="L28">
   <label>Step 8: range in the app, 2 m (m) <input data-field="b.2.app"></label>
   </div>
9. **Plate at 3.00 m.** Repeat at 3.00 m. The app's range axis comes from the beat per meter it assumes, so these ranges cannot test that number; the frequencies the notebook reads from your three captures in Step 17 can.

   <div class="rec" data-lab="L28">
   <label>Step 9: range in the app, 3 m (m) <input data-field="b.3.app"></label>
   </div>
::::

::::{frame} Change the Chirp
:::{present}
- Plate at 2 m: **Range (Fast)**, half the chirp length; save.
- The 250 MHz capture, by **Load Recording**: half the bandwidth.
- Compare each peak with your 2 m reference and your Part 1.
:::

10. **Half the chirp length.** Leave the plate at 2.00 m and set Preset to **Range (Fast)**, 500 MHz in 0.5 ms at 5 MSPS. The app rescales its range axis to the new chirp, so the plate should still read about 2 m. Compare the width of its peak with the Range (Basic) peak, and press **Save Capture**.
11. **Half the bandwidth.** The app has no bandwidth setting, so everyone uses the course's 250 MHz capture, `L28_corner_2m_B250.npz`, from the lab's bundle. Press **Load Recording** and choose it: the app plays it through every view as if it were live. Compare the width of the corner's peak with your own 500 MHz peak, then press **Stop**.
12. **Return to Range (Basic).** Set Preset back to **Range (Basic)** and press **Start**. The notebook gives each waveform's peak frequency, width, and height in Step 17.
::::

::::{frame} Walk the Waterfall
:::{present}
- **Range Waterfall** tab, Waterfall Depth 200, Range Max 6 m.
- Walk out from 1 m to about 4 m and back, twice.
- Screenshot it; record the ranges, the frames a leg took, and the Frame Rate.
:::

13. **Set up the waterfall.** Open the **Range Waterfall** tab. Under **Display**, set **Waterfall Depth** to **200**, and in the FMCW section set **Range Max (m)** to **6**. Time runs down the plot in display updates, frames ago. If the fixed lines crowd your trace, lower **Color Span (dB)** until they are faint and your trace is still bright.
14. **Walk.** Stand 1 m in front of the kit, facing it. Walk slowly straight out to about 4 m and back, about one step a second, twice.
15. **Read the walk.** Take a screenshot of the waterfall with both walks on it. Hover over the trace to record the nearest and farthest ranges it reached and the number of frames one leg took, and record the **Frame Rate** readout. A saved capture holds only 32 chirps, a fraction of a second, so the notebook's waterfall uses the course's 10 s walk instead; load `L28_walker.npz` with **Load Recording** and read it the same way for the recorded column.

    <div class="rec" data-lab="L28">
    <label>Step 15: nearest range (m) <input data-field="d.near"></label>
    <label>Step 15: farthest range (m) <input data-field="d.far"></label>
    <label>Step 15: frames for one leg <input data-field="d.frames"></label>
    <label>Step 15: Frame Rate (fps) <input data-field="d.fps"></label>
    <label>Recorded walk: nearest range (m) <input data-field="d.rec.near"></label>
    <label>Recorded walk: farthest range (m) <input data-field="d.rec.far"></label>
    <label>Recorded walk: frames for one leg <input data-field="d.rec.frames"></label>
    <label>Recorded walk: Frame Rate (fps) <input data-field="d.rec.fps"></label>
    </div>
::::

::::{frame} Run the Notebook
:::{present}
- Open `L28_range.ipynb`; point it at your 2 m capture.
- Peak readout: every capture Tables A to C name.
- Tasks (a) to (c), one changed line each.
:::

16. **Open the notebook.** With the folder set up as the Notebook Setup frame describes, open `L28_range.ipynb`, set `CAPTURE` in the first code cell to your 2 m capture, and run the cells from the top. The first cell prints the samples per chirp; record it, and do the same for your Range (Fast) capture.

    <div class="rec" data-lab="L28">
    <label>Step 16: samples per chirp, Range (Basic) <input data-field="s.n"></label>
    <label>Step 16: samples per chirp, Range (Fast) <input data-field="s.n.fast"></label>
    </div>
17. **Peak readout.** Set `NAME` to each capture in turn and record the frequency of the peak the table asks for: the leakage of the clear-range capture, the plate of the capture on the array, the plate at 1, 2, and 3 m, and the plate of each waveform, with its width and its height above the floor. Fit a line through the three plate frequencies against the tape ranges for the beat per meter and its intercept, and divide each waveform's beat above your $f_0$ by 2 m for its kHz per meter. A capture the app saves holds the receiver's raw counts, so its levels print tens of dB higher than the recorded data's; compare heights above the floor, not levels.

    <div class="rec" data-lab="L28">
    <label>Leakage, clear range (kHz) <input data-field="a.leak.nb"></label>
    <label>f0, plate on the array (kHz) <input data-field="a.f0.nb"></label>
    <label>Plate at 1 m (kHz) <input data-field="b.1.f"></label>
    <label>Plate at 2 m (kHz) <input data-field="b.2.f"></label>
    <label>Plate at 3 m (kHz) <input data-field="b.3.f"></label>
    <label>Beat per meter, the slope (kHz/m) <input data-field="b.slope"></label>
    <label>Intercept (kHz) <input data-field="b.icpt"></label>
    <label>Range (Basic): peak (kHz) <input data-field="c.basic.f"></label>
    <label>Range (Basic): kHz per meter <input data-field="c.basic.k"></label>
    <label>Range (Basic): width 3 dB (m) <input data-field="c.basic.w"></label>
    <label>Range (Fast): peak (kHz) <input data-field="c.fast.f"></label>
    <label>Range (Fast): kHz per meter <input data-field="c.fast.k"></label>
    <label>Range (Fast): width 3 dB (m) <input data-field="c.fast.w"></label>
    <label>Range (Fast): height re Range (Basic) (dB) <input data-field="c.fast.h"></label>
    <label>250 MHz: peak (kHz) <input data-field="c.b250.f"></label>
    <label>250 MHz: kHz per meter <input data-field="c.b250.k"></label>
    <label>250 MHz: width 3 dB (m) <input data-field="c.b250.w"></label>
    <label>250 MHz: height re Range (Basic) (dB) <input data-field="c.b250.h"></label>
    </div>
18. **Task (a), the window.** Run the range-profile cell with `WINDOW = "hann"`, then change that one line to `WINDOW = None` and run it again. Record the strongest sidelobe and the floor near 10 m for each window.

    <div class="rec" data-lab="L28">
    <label>Hann: strongest sidelobe (dBc) <input data-field="e.sl.hann"></label>
    <label>Rectangular: strongest sidelobe (dBc) <input data-field="e.sl.rect"></label>
    <label>Hann: floor near 10 m (dBFS) <input data-field="e.fl.hann"></label>
    <label>Rectangular: floor near 10 m (dBFS) <input data-field="e.fl.rect"></label>
    </div>
19. **Task (b), zero-padding.** In the two-corner cell, the only cell with an `N_FFT` line, run it with `N_FFT = None`, then change that line to `N_FFT = 4096`. Record how many peaks it finds and the width 3 dB down each time.

    <div class="rec" data-lab="L28">
    <label>No padding: peaks <input data-field="e.pk.none"></label>
    <label>4096 points: peaks <input data-field="e.pk.4096"></label>
    <label>No padding: width (m) <input data-field="e.w.none"></label>
    <label>4096 points: width (m) <input data-field="e.w.4096"></label>
    </div>
20. **Task (c), range from your $f_0$.** Set `F0` to your notebook $f_0$ from Step 17 and replace `R = None` with the range of the peak, from `f_peak`, `F0`, and the capture's `B` and `T_ramp`. Record `R`, run the waterfall cell, and save the notebook with its edits and plots. Upload the `.ipynb` with the packet, and leave the task cells' names and variables as they are.

    <div class="rec" data-lab="L28">
    <label>Step 20: R, 2 m capture (m) <input data-field="b.R"></label>
    </div>

Each notebook cell's markdown states the result to check against for the recorded data. Anything you do beyond the three tasks belongs in your report's Extra Effort.
::::

::::{frame} No Hardware?
:class: read-only

```{note}
If your kit will not run, every step works in the app's simulator, in a
browser with no kit and no install, on the course's recorded data. Open
[livethisdream.github.io/phaser/radar](https://livethisdream.github.io/phaser/radar/),
choose the FMCW mode tab, and follow the steps as written. **Load Recording**
plays one of the course's captures through every view as if it were live,
Calibrate and the readouts included; the recording sets the waveform, so the
app grays out Preset while it plays, and **Stop** ends it. **Scene**, in the
simulator only, picks a live simulated room: **Walker** walks from 1 m to
4 m and back.

Load `L28_clear.npz` for Step 3, `L28_cal_0m.npz` for Steps 4 and 5,
`L28_corner_1m.npz`, `L28_corner_2m.npz`, and `L28_corner_3m.npz` for Steps 7
to 9, `L28_corner_2m_fast.npz` for Step 10, and `L28_walker.npz` or the Walker
scene for Steps 13 to 15, and run the notebook on the same files. They are in
the lab's bundle with the notebook: a simulation of the PHASER at each preset,
with a kit whose 0 m frequency is 101.4 kHz, a 10 cm corner reflector standing
in for the plate, and tape readings a few centimeters off, as a real room's
are. Mark in your packet which rows come from the recorded data.
```
::::

::::{frame} Notebook Setup
:class: read-only

The notebook runs on your own laptop, with Python 3 and four packages: numpy, scipy, matplotlib, and Jupyter. You need nothing else, and once they are installed the notebook runs without a network connection.

1. Install Python 3.10 or newer from <a href="https://www.python.org/downloads/" target="_blank" rel="noopener">python.org</a> if your laptop does not have it. Then, in a terminal, install the four packages in one line:

   ```sh
   python -m pip install numpy scipy matplotlib jupyterlab
   ```

2. Make a folder for the Module 4 labs, such as `ece444-radar`, download the lab's bundle, <a href="../../bundles/L28_lab.zip" download>`L28_lab.zip`</a>, and unzip it into the folder. It holds `L28_range.ipynb`, `radar_lab.py`, every recorded capture the steps name, and a README that lists them.
3. Move your own captures into the same folder.
4. In a terminal, change to the folder and start Jupyter with `jupyter lab`. Open `L28_range.ipynb` and run its first cell. If it reports that `radar_lab` is missing, the module is not in the same folder as the notebook.

Keep this folder for the whole module. Each later lab adds its own bundle to it, and they all use the same `radar_lab.py`.
::::

::::{frame} Your Part 2 Entries
:class: read-only

This frame collects every box you filled in on this page. Your entries stay in this
browser only, and the page saves them as you type. **Download my packet** writes them into Part 2
of the blank packet and saves the PDF; do Parts 1 and 3 on paper or in the PDF
viewer, and upload one PDF to Gradescope. If you have already typed Part 1 into
the packet PDF, use **Fill my own copy** and choose that file instead: the download keeps
your Part 1 and adds Part 2 to it. Either way the result is locked, so finish
any typing in the PDF first. **Export entries** saves a small backup file you
can **Import** on another laptop or after clearing your browser. The boxes are
optional: the blank packet is in the next frame, to fill on paper or in a PDF
viewer instead.

<div class="rec-summary" data-lab="L28" data-pdf="../../labs/ECE444_Lab_L28_FMCWRange_blank.pdf" data-file="ECE444_L28_Lab"></div>
::::

::::{frame} Lab Packet
:class: read-only doc-links

The L28 Lab packet is one submission, turned in complete before Lesson 29, with the notebook uploaded beside it. It has three parts:

1. Part 1, Predict (before class): the shaded Predicted cells of each table.
2. Part 2, Measure (in class): the white Measured cells, from your own kit and the notebook.
3. Part 3, Analyze (after class): three open prompts on what you measured.

- <a class="doc-link" href="../../labs/ECE444_Lab_L28_FMCWRange_blank.pdf" target="_blank" rel="noopener">L28 Lab packet (PDF)</a>
::::

::::{frame} For Part 3
:class: read-only

Part 3 asks about three things you measured: the beat per meter and its intercept against your 0 m frequency, the three waveforms of Table C, and the walk on your waterfall. Bring your Part 2 numbers, your Part 1 predictions, and your screenshot. Each answer states a claim, the evidence from your own tables, the reasoning that connects them, and how large a difference your measurement can resolve.
::::

::::{frame} Looking Ahead
:class: read-only

Lesson 29 keeps the phase this lab discarded: a burst of chirps 0.5 ms apart, and a second FFT across them, reads each target's velocity.
::::
