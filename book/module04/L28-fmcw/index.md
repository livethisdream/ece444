---
frame_view: true
---

# L28 - FMCW on the Phaser

::::{frame}
:class: title-frame

<div class="course-mark">ECE 444 · Fall 2026</div>

<h1 class="frame-title">FMCW on the Phaser</h1>

<div class="title-rule"></div>

Find your kit's 0 m frequency, then measure range, resolution, and a walk on the range waterfall.

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
<img src="../../viz/img/L28-chirp.svg" alt="Frequency against time. The transmitted chirp is a straight ramp repeated twice. The echo is the same ramp shifted right by the delay. At any instant the two differ by a fixed frequency, the beat. The ramp spans the bandwidth vertically and the chirp length horizontally. The first tenth of each ramp is shaded as settling, and the last 90% is marked as kept" style="max-width: 620px; width: 100%; display: block; margin: 0 auto;">
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

The lab runs the Phaser app's presets, and the packet gives their settings. This lesson works every method on a chirp that no preset uses, $B = 400$ MHz in $T_s = 2$ ms from 10.0 GHz, so that each worked number shows the method and leaves the preset's numbers for Part 1. The start frequency never enters the beat, only $B/T_s$ does, so a preset at another carrier follows the same rules. The figure exaggerates the delay so that it is visible: a target at 3 m delays the echo by 20 ns, 0.001% of a 2 ms chirp. The shaded start of each ramp is the part the Phaser app discards while the ramp settles, which The Range FFT frame takes up.
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

The PHASER adds every beat to a fixed offset, the kit's 0 m frequency $f_0$, 100 to 120 kHz on our kits. A target's peak therefore sits at $f_0 + f_b$: for the worked chirp and an $f_0$ of 100 kHz, a target at 4 m peaks at $100 + 4 \times 1.33 = 105.33$ kHz. Plotted against range, the peaks of a target at several ranges fall on a straight line whose slope is the beat per meter and whose intercept, at 0 m, is $f_0$.

The kHz per meter depends on both waveform settings. Quartering the bandwidth to 100 MHz quarters it, to 0.33 kHz per meter, and quartering the chirp length to 0.5 ms quadruples it, to 5.33 kHz per meter. Only the bandwidth changes the resolution, as the Range Resolution frame derives.
::::

::::{frame} FMCW Explorer
:class: viz-frame read-only

:::{depth}
The left panel is the beat signal over one chirp, with the 0 m frequency removed, and the right panel is its range spectrum, the FFT of those samples with the frequency axis converted to range. It opens on the worked chirp, 400 MHz in 2 ms, and like the app it keeps the last 90% of each chirp. Move the target and count the cycles: every meter adds $0.9 \times 2B/c = 2.4$ kept cycles at 400 MHz. Change the bandwidth or the chirp length and watch the beat per meter follow $B/T_s$. Turn on the second target and bring it in toward the first until the two peaks merge; the green bar is one cell of the kept chirp, $c/(2 \cdot 0.9B)$. Then set the second target 20 to 40 dB weaker and switch between the rectangular and Hann windows.
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

The number of beat cycles in one chirp is $f_bT_s = 2RB/c$, which does not depend on $T_s$ either. Two targets one cell apart differ by exactly one cycle a chirp; closer than that, their beats stay within one cycle of each other for the whole chirp, and the FFT returns one peak however finely it draws the spectrum.
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
<img src="../../viz/img/L28-range-profile.svg" alt="Power in dBFS, dB relative to the receiver's full scale, against range from minus 0.3 to 8 m for the worked chirp, with a top axis of beat frequency above the 0 m frequency from 0 to about 10.7 kHz. Three peaks: leakage at 0 m near minus 20 dBFS, a corner reflector at 2.0 m near minus 20 dBFS, and the far wall at 5.5 m near minus 31 dBFS, over a floor near minus 85 dBFS" style="max-width: 640px; width: 100%; display: block; margin: 0 auto;">
:::

The PHASER's Pluto samples the beat at $f_s = 0.6$ MSPS. The Phaser app discards the first 10% of each chirp, while the frequency ramp settles, and keeps the rest: for the worked chirp, $0.9 \times 2\ \text{ms} \times 0.6$ MSPS gives $N = 1080$ complex samples. The FFT of those samples is the **range profile**: each bin is a frequency, and the beat-per-meter relation converts it to a range,

$$
R = \frac{cT_s}{2B}\left(f - f_0\right),
$$

where $f_0$ is the 0 m frequency of the next frame. The bins are $f_s/N = 0.556$ kHz apart, which at 1.33 kHz per meter is 0.417 m. That is a little more than the 0.375 m of the resolution frame because the 1.8 ms the app keeps sweeps 360 MHz, not 400, and $c/(2 \cdot 360\ \text{MHz}) = 0.417$ m. Padding the record with zeros before the FFT, to 4096 points or more, draws the same spectrum on a finer grid and makes the peaks easier to read, but it does not resolve anything new.

The figure is one chirp of the worked waveform from the course's simulated room: a 10 cm corner reflector at 2.0 m, the transmit antenna's direct path into the array at 0 m, and the far wall at 5.5 m. The top axis shows the same profile as beat frequency above $f_0$, at 1.33 kHz per meter.

The power axis is in **dBFS**, decibels relative to the receiver's full scale, the largest signal its converter records. The FFT also integrates. The 1080 samples of a steady tone add in phase while the noise adds in power, so the tone rises $10\log_{10}1080 = 30.3$ dB above the noise per sample, as <a href="../L27-radar-detection/index.html#frame-integrating-pulses">Lesson 27</a> described. Seen another way, each bin collects noise from only 0.556 kHz, while each sample carries the noise of the whole 0.6 MHz the receiver samples. The two views agree at a fixed sample rate, since $f_s/N$ is the bin width. When the sample rate changes too, only the bin view holds: a faster sample rate puts more noise in every sample, which cancels the gain from having more samples. That is the narrowing <a href="../L25-radar-equation/index.html#frame-signal-to-noise-ratio">Lesson 25</a> described: the corner at 3 m, 31.1 dB above the noise in 1 MHz, stands

$$
\begin{aligned}
\text{SNR}_\text{bin} &= 31.1\ \text{dB} + 10\log_{10}\frac{1\ \text{MHz}}{0.556\ \text{kHz}} \\
&= 63.7\ \text{dB}
\end{aligned}
$$

above it in one bin. The record length sets that height, whatever the sample rate. A window-normalized FFT reads a tone at the same level whatever the record, while one bin holds the noise of $1/T$ of bandwidth, so a record a quarter as long puts four times the noise in each bin and the same target stands $10\log_{10}4 = 6$ dB lower above the floor.

<img src="../../viz/img/L28-record-length.svg" alt="Power in dBFS against range from 0 to 8 m for one target at 4 m, seen by the worked chirp at 2 ms and at 0.5 ms with the same sample rate. Both peaks read the same level and the same width. The 0.5 ms floor sits 6 dB above the 2 ms floor, marked with an arrow" style="max-width: 620px; width: 100%; display: block; margin: 0 auto;">
::::

::::{frame} The 0 m Frequency
:class: read-only

:::{present}
- A 0 m echo lands at $f_0$, 100 to 120 kHz, not at zero.
- $f_0$ differs from kit to kit and from one power-up to the next.
- **Calibrate…** reads it from a plate against the array, after every power-up.
:::

<img src="../../viz/img/L28-spectrum.svg" alt="Power in dBFS against beat frequency from 0 to 300 kHz for the worked chirp with the 0 m frequency at 100 kHz. Below 100 kHz the band is shaded as negative range. A dashed line at 100 kHz marks the leakage, the strongest peak. A target at 30 m peaks 40 kHz above it. A red line at 300 kHz marks half the sample rate, 150 m, past which beats alias" style="max-width: 620px; width: 100%; display: block; margin: 0 auto;">

The PHASER does not put a 0 m echo at zero frequency. The transmitter runs 100 kHz, the app's **IF tone**, off the frequency the receiver mixes the echo with, so an echo with no delay comes out at about 100 kHz and every beat sits on top of that. That keeps the targets clear of zero frequency, where the receiver's own offset and low-frequency noise sit. The offset is not exactly 100 kHz: on our kits the 0 m frequency $f_0$ reads 100 to 120 kHz, and it changes when the kit restarts, so calibrate it after every power-up. The range equation measures every beat from $f_0$, and the figure shows the whole spectrum the receiver records, from the negative ranges below $f_0$ to the alias limit at $f_s/2$.

To calibrate, hold a flat metal plate against the array face, read the frequency of the peak, and record it as $f_0$. With the plate gone, a peak stays within a fraction of a bin of $f_0$: it is the transmit antenna's direct path into the array, the **leakage**, a few centimeters long, which moves the beat by much less than one bin, so it marks 0 m on every capture you take. An error in $f_0$ moves every range by the same amount: for the worked chirp, 1 kHz of error reports every range 0.75 m long or short, and a kit left uncalibrated 15 kHz above the IF tone reads every range 11 m long.
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
<img src="../../viz/img/L28-windows.svg" alt="Range profiles from 0.5 to 5.5 m of a strong target at 2.0 m and a target 30 dB weaker at 4.5 m, for the worked chirp. With a rectangular window the sidelobes of the strong target sit 20 to 35 dB down and hide the weak one. With a Hann window the sidelobes fall below minus 50 dB and the weak target shows. A zoomed panel of the strong peak from 1.3 to 2.7 m brackets each window's width 3 dB down: the Hann peak is the wider" style="max-width: 620px; width: 100%; display: block; margin: 0 auto;">
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

puts the first sidelobe at $-31$ dB and the rest falling fast, and the weak target appears. This is the amplitude taper of <a href="../../module03/L22-sidelobes-tapering/index.html">Lesson 22</a> applied in time instead of across the array, with the same consequences: the main lobe widens, from a 3 dB width of 0.89 bins to 1.44 bins, so two equal targets one cell apart may merge, and the window discards some signal energy, a 1.8 dB loss in SNR. Lesson 22's Hann taper loses 1.25 dB because it samples the taper at eight elements; over a chirp's hundreds of samples the loss is 1.8 dB. A level read from the peak of its own trace, 0 dB at the peak, is in **dBc**, the unit the notebook gives a sidelobe in. In range, a peak's width 3 dB down is 1.44 bins times the meters per bin: $1.44 \times 0.417 = 0.60$ m for the worked chirp. `radar_lab` uses Hann by default; the rectangular window is the choice only when two equal targets must be split at the edge of the resolution.
::::

::::{frame} The Range Waterfall
:class: read-only

:::{present}
<img src="../../viz/img/L28-waterfall.svg" alt="Range profiles from 0 to 6 m stacked in time over 10 s, darker for stronger echoes, the newest at the top. A dark vertical band at 0 m is the leakage and one at 5.5 m is the wall. A zigzag trace runs from 1.5 m out to 3.5 m and back: a person walking" style="max-width: 620px; width: 100%; display: block; margin: 0 auto;">
:::
:::{present}
- Each row is one range profile; newest at the top, as in the app.
- Fixed objects draw vertical lines; a walker draws a zigzag.
- The slope of the trace is the walker's speed.
:::

One range profile is a snapshot. Stacking the profiles of successive chirps, one row per chirp and darker for a stronger echo, gives the **range waterfall**: range across, and time running down from the newest row at the top, as on the app's Range Waterfall tab. A fixed object, the leakage at 0 m or the wall at 5.5 m, keeps the same range in every row and draws a vertical line. A person walking out and back draws a zigzag, and the slope of each leg is the walking speed: the simulated walker in the figure covers 2 m in 4 s, 0.5 m/s.

The waterfall records range against time and nothing else. Its rows are one display update apart, tens of milliseconds, and over that time a walker's carrier phase changes by many cycles, so successive rows say nothing about the walker's velocity except through the range they show. <a href="../L29-range-doppler-mti/index.html">Lesson 29</a> takes chirps a fixed 0.5 ms apart and reads the velocity from that phase.
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
| A | nothing: $f_0$ is each kit's own, measured | The 0 m Frequency | Steps 3 to 5 and 17 |
| B | the beat above $f_0$ at each range, and the beat per meter | The Beat Frequency | Steps 6 to 8 and 18 |
| C | kHz per meter, width, and height for three waveforms | The Beat Frequency, The Range FFT, Windowing the Chirp | Steps 9 to 11 and 19 |
| E | the peaks two corners 0.20 m apart make | Range Resolution | Step 21 |

- <a class="doc-link" href="../../labs/ECE444_Lab_L28_FMCWRange_blank.pdf" target="_blank" rel="noopener">L28 Lab packet (PDF)</a>
::::

::::{frame} The Big Picture
:::{present}
<img src="../../viz/img/L28-flow.svg" alt="Five boxes left to right, joined by arrows. Steps 1 to 5, the 0 m frequency, Table A. Steps 6 to 8, static ranges, Table B. Steps 9 to 11, change the chirp, Table C. Steps 12 to 15, a walk, Table D. Steps 16 to 22, the notebook, Tables B, C and E. A line from the first three boxes, labeled saved captures, feeds the notebook" style="max-width: 760px; width: 100%; display: block; margin: 0 auto;">
:::

The lab measures each thing the lesson derived, on your own kit, with the Phaser app's **Range (Basic)** preset as the reference waveform. Steps 1 to 5 bring the kit up and find its 0 m frequency. Steps 6 to 8 put the plate at three ranges and save a capture at each. Steps 9 to 11 change one setting at a time, the chirp length on the kit and the bandwidth from a recorded capture. Steps 12 to 15 read a walk on the range waterfall, yours and the course's recorded one. Steps 16 to 22 run the course's notebook on the captures you saved: the app shows range, and the notebook reads the frequencies the range came from. Each block fills one packet table, against your Part 1 prediction.
::::

::::{frame} Predict First
:class: viz-frame

:::{depth}
Before you change the waveform on the kit, predict what each change does to one target's peak, then check yourself. The widget starts from the lesson's worked chirp, 400 MHz in 2 ms, with one target at 4 m. Choose a chirp length and a bandwidth and decide, before you press **Show profile**: where the peak moves, whether it widens, and whether it stands higher or lower above the floor. Any change to the chirp hides the profile again, so each guess comes first. The axis opens in range, as the app's Range tab shows it; switch it to beat frequency to see where the same peak sits in kHz. The factors carry over to the kit.
:::

:::{present}
<iframe src="../../viz/fmcw-predict.html"
        width="100%" height="523"
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
2. **Open the radar app.** Browse to `http://phaser-NN.local:8081`, with your kit's number, the radar half of the Phaser app. Choose the **FMCW** mode tab and open the **FMCW** section. Its status line should read **FMCW ready**; if it reads **FMCW limited**, hover over it for the reason and tell me, because a kit without chirp sync does not run the preset's chirp, and the recorded data then stand in for Tables B and C. Set **Preset** to **Range (Basic)**, leave **Range Max (m)** empty, and press **Start**. The **Range** tab shows one range profile per display update. If **0 m Beat (kHz)** holds a value from an earlier session, open **Calibrate…** and press **Reset**: the 0 m frequency changes each time the kit powers up.
3. **Read the leakage.** Clear everything from in front of the kit and stand to one side, out of the beam. Open **Calibrate…**: the **Strongest return** is the leakage from the transmit antenna into the array, and its frequency is **New 0 m beat**. Record it, press **Cancel**, and press **Save Capture**. The app downloads `phaser_range_<date>-<time>.npz`; move it into your Module 4 folder and note its name.

   <div class="rec" data-lab="L28">
   <label>Step 3: leakage, New 0 m beat (kHz) <input data-field="a.leak.app"></label>
   </div>
4. **Save the plate on the array.** Hold the plate flat against the array face, covering the patches, and press **Save Capture**.
5. **Calibrate.** With the plate still there, open **Calibrate…**, wait for Strongest return to settle, record New 0 m beat as the app's $f_0$, and press **Calibrate**. **0 m Beat (kHz)** now holds it, the range axis reads 0 m there, and every capture you save from now on carries it as its `f0`. Expect a value between 100 and 120 kHz, within a bin of the leakage in Step 3; the app reads to the nearest bin, so the two can differ by one. If the kit restarts during the lab, calibrate again before the next save, because a capture saved before recalibrating carries the old $f_0$. The range axis starts at 0 m, so a kit whose $f_0$ is below the 100 kHz IF tone puts the plate at a negative range, off the plot, and Strongest return finds something else; if the plate's peak is missing, type 95 in 0 m Beat (kHz) and open Calibrate… again.

   <div class="rec" data-lab="L28">
   <label>Step 5: f0, New 0 m beat (kHz) <input data-field="a.f0.app"></label>
   </div>
::::

::::{frame} Static Ranges
:::{present}
- Plate at 1, 2, and 3 m by the tape; hover over its peak for its range.
- **Save Capture** at each range.
:::
:::{present}
<img src="../../viz/img/L28-setup.svg" alt="Top view. The kit at the left with its array face. A tape runs straight out from the face with marks at 1, 2, and 3 m, inside the shaded beam. The plate stands at 2 m, square to the array. A red cross off to the side, outside the beam, marks where to stand" style="max-width: 560px; width: 100%; display: block; margin: 0 auto;">
:::

6. **Plate at 1.00 m.** Stand the plate 1.00 m from the array face by the tape, at array height. A plate reflects strongly only when it faces the array squarely, so on the **Range** tab turn it slowly until its peak is highest, then step out of the beam: your body is a larger reflector than the plate. Hover over the plate's peak, record its range, and press **Save Capture**. **Peak Range** shows the strongest return, which can be the leakage near 0 m rather than the plate, so read the plate's own peak. The app draws its range axis from the beat per meter it assumes, so these ranges do not test that number; the plate frequencies the notebook reads in Step 17 do.

   <div class="rec" data-lab="L28">
   <label>Step 6: range in the app, 1 m (m) <input data-field="b.1.app"></label>
   </div>
7. **Plate at 2.00 m.** Repeat at 2.00 m. Check that the plate's peak moved out by about 1 m before you save; a peak that did not move is the leakage or the wall.

   <div class="rec" data-lab="L28">
   <label>Step 7: range in the app, 2 m (m) <input data-field="b.2.app"></label>
   </div>
8. **Plate at 3.00 m.** Repeat at 3.00 m.

   <div class="rec" data-lab="L28">
   <label>Step 8: range in the app, 3 m (m) <input data-field="b.3.app"></label>
   </div>
::::

::::{frame} Change the Chirp
:::{present}
- Plate at 2 m: **Range (Fast)**, half the chirp length; save.
- The 250 MHz capture, by **Load Recording**: half the bandwidth.
- Compare each peak with your 2 m reference and your Part 1.
:::

9. **Half the chirp length.** Leave the plate at 2.00 m and set Preset to **Range (Fast)**, 500 MHz in 0.5 ms at 5 MSPS. The app rescales its range axis to the new chirp, so the plate should still read about 2 m. Compare the width of its peak with the Range (Basic) peak, and press **Save Capture**.
10. **Half the bandwidth.** The app has no bandwidth setting, so everyone uses the course's 250 MHz capture, `L28_corner_2m_B250.npz`, from the lab's bundle. Press **Load Recording** and choose it: the app plays it through every view as if it were live. Compare the width of the corner's peak with your own 500 MHz peak, then press **Stop**.
11. **Return to Range (Basic).** Set Preset back to **Range (Basic)** and press **Start**.
::::

::::{frame} Walk the Waterfall
:::{present}
- **Range Waterfall** tab: walk from 1 m to about 4 m and back, twice.
- Read your walk, then the course's recorded walk.
:::
:::{present}
<img src="../../viz/img/L28-waterfall.svg" alt="A simulated range waterfall from 0 to 6 m over 10 s, newest at the top: vertical bands at 0 m and 5.5 m, and a zigzag trace of a walk between 1.5 and 3.5 m" style="max-width: 560px; width: 100%; display: block; margin: 0 auto;">
:::

12. **Set up the waterfall.** Open the **Range Waterfall** tab. Under **Display**, set **Waterfall Depth** to 200, and in the FMCW section set **Range Max (m)** to 6. Time runs down the plot in display updates, frames ago, with the newest row at the top. If the fixed lines crowd your trace, lower **Color Span (dB)** until they are faint and your trace is still bright.
13. **Walk.** Stand 1 m in front of the kit, facing it. Walk slowly straight out to about 4 m and back, about one step a second, twice.
14. **Read your walk.** Take a screenshot of the waterfall with both walks on it. Hover over the trace to record the nearest and farthest ranges it reached and the number of frames one leg took, and record the **Frame Rate** readout.

    <div class="rec" data-lab="L28">
    <label>Step 14: nearest range (m) <input data-field="d.near"></label>
    <label>Step 14: farthest range (m) <input data-field="d.far"></label>
    <label>Step 14: frames for one leg <input data-field="d.frames"></label>
    <label>Step 14: Frame Rate (fps) <input data-field="d.fps"></label>
    </div>
15. **Read the recorded walk.** Press **Load Recording**, choose `L28_walker.npz` from the bundle, and read it the same way, then press **Stop**. A capture you save holds only 32 chirps, a fraction of a second, so the notebook's waterfall uses this 10 s recording too.

    <div class="rec" data-lab="L28">
    <label>Step 15: nearest range (m) <input data-field="d.rec.near"></label>
    <label>Step 15: farthest range (m) <input data-field="d.rec.far"></label>
    <label>Step 15: frames for one leg <input data-field="d.rec.frames"></label>
    <label>Step 15: Frame Rate (fps) <input data-field="d.rec.fps"></label>
    </div>
::::

::::{frame} Run the Notebook
:::{present}
- Open `L28_range.ipynb`; point it at your 2 m capture.
- Peak readout on each capture; fit the line.
- Tasks (a) to (c), one changed line each.
:::

16. **Open the notebook.** With the folder set up as the Notebook Setup frame describes, open `L28_range.ipynb`, set `CAPTURE` in the first code cell to your 2 m capture, and run the cells from the top. Each cell's markdown states the result to check against, for the recorded data. The first cell prints the samples per chirp; record it, and do the same for your Range (Fast) capture.

    <div class="rec" data-lab="L28">
    <label>Step 16: samples per chirp, Range (Basic) <input data-field="s.n"></label>
    <label>Step 16: samples per chirp, Range (Fast) <input data-field="s.n.fast"></label>
    </div>
17. **Read the peaks.** In the peak readout cell, set `NAME` to each capture in turn and record the frequency of the peak named below: the leakage of the clear-range capture, the plate on the array, and the plate at each range. A capture the app saves holds the receiver's raw counts, so its levels print tens of dB higher than the recorded data's; compare heights above the floor, not levels.

    <div class="rec" data-lab="L28">
    <label>Leakage, clear range (kHz) <input data-field="a.leak.nb"></label>
    <label>f0, plate on the array (kHz) <input data-field="a.f0.nb"></label>
    <label>Plate at 1 m (kHz) <input data-field="b.1.f"></label>
    <label>Plate at 2 m (kHz) <input data-field="b.2.f"></label>
    <label>Plate at 3 m (kHz) <input data-field="b.3.f"></label>
    </div>
18. **Fit the line.** Subtract your notebook $f_0$ from each plate frequency for its beat, and fit a line through the three peak frequencies against the tape ranges: its slope is the beat per meter, and its intercept is the frequency it puts at 0 m.

    <div class="rec" data-lab="L28">
    <label>Beat above f0, 1 m (kHz) <input data-field="b.1.beat"></label>
    <label>Beat above f0, 2 m (kHz) <input data-field="b.2.beat"></label>
    <label>Beat above f0, 3 m (kHz) <input data-field="b.3.beat"></label>
    <label>Beat per meter, the slope (kHz/m) <input data-field="b.slope"></label>
    <label>Intercept (kHz) <input data-field="b.icpt"></label>
    </div>
19. **Read the three waveforms.** Run the readout on your 2 m capture, your Range (Fast) capture, and `L28_corner_2m_B250.npz`. Record each plate's peak, its beat above your $f_0$ divided by 2 m for its kHz per meter, its width 3 dB down, and its height above the floor less the Range (Basic) height.

    <div class="rec" data-lab="L28">
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
20. **Task (a), the window.** Run the range-profile cell with `WINDOW = "hann"`, then change that one line to `WINDOW = None` and run it again. Record the strongest sidelobe, in dBc, and the floor near 10 m for each window.

    <div class="rec" data-lab="L28">
    <label>Hann: strongest sidelobe (dBc) <input data-field="e.sl.hann"></label>
    <label>Rectangular: strongest sidelobe (dBc) <input data-field="e.sl.rect"></label>
    <label>Hann: floor near 10 m (dBFS) <input data-field="e.fl.hann"></label>
    <label>Rectangular: floor near 10 m (dBFS) <input data-field="e.fl.rect"></label>
    </div>
21. **Task (b), zero-padding.** In the two-corner cell, the only cell with an `N_FFT` line, run it with `N_FFT = None`, then change that line to `N_FFT = 4096`. Record how many peaks it finds and the width 3 dB down each time.

    <div class="rec" data-lab="L28">
    <label>No padding: peaks <input data-field="e.pk.none"></label>
    <label>4096 points: peaks <input data-field="e.pk.4096"></label>
    <label>No padding: width (m) <input data-field="e.w.none"></label>
    <label>4096 points: width (m) <input data-field="e.w.4096"></label>
    </div>
22. **Task (c), range from your $f_0$.** Set `F0` to your notebook $f_0$ from Step 17 and replace `R = None` with the range of the peak, from `f_peak`, `F0`, and the capture's `B` and `T_ramp`. Record `R`, run the waterfall cell, and save the notebook with its edits and plots. Upload the `.ipynb` with the packet, and leave the task cells' names and variables as they are. Anything you do beyond the three tasks belongs in your report's Extra Effort.

    <div class="rec" data-lab="L28">
    <label>Step 22: R, 2 m capture (m) <input data-field="b.R"></label>
    </div>
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
simulator only, picks a live simulated room: **Walker** walks out and back.

Load `L28_clear.npz` for Step 3, `L28_cal_0m.npz` for Steps 4 and 5,
`L28_corner_1m.npz`, `L28_corner_2m.npz`, and `L28_corner_3m.npz` for Steps 6
to 8, `L28_corner_2m_fast.npz` for Step 9, and the Walker scene for Steps 12 to
14, and run the notebook on the same files. They are in the lab's bundle with
the notebook: a simulation of the PHASER at each preset, with a 10 cm corner
reflector standing in for the plate and tape readings a few centimeters off,
as a real room's are. Mark in your packet which rows come from the recorded
data.
```
::::

::::{frame} Notebook Setup
:class: read-only

The notebook runs on your own laptop, with Python 3 and four packages: numpy, scipy, matplotlib, and Jupyter. You need nothing else, and once you install them the notebook runs without a network connection.

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
viewer instead. The packet's time for one leg and walking speed come from your
Step 14 and 15 entries.

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

Part 3 asks about three things you measured: the beat per meter and its intercept against your 0 m frequency, the three waveforms of Table C, and the walks of Table D. Bring your Part 2 numbers, your Part 1 predictions, and your screenshot. Each answer states a claim, the evidence from your own tables, the reasoning that connects them, and how large a difference your measurement can resolve.
::::

::::{frame} Looking Ahead
:class: read-only

Lesson 29 keeps the phase this lab discarded: a burst of chirps 0.5 ms apart, and a second FFT across them, reads each target's velocity.
::::
