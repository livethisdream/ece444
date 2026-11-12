---
frame_view: true
---

# L30 - CFAR Processing

::::{frame}
:class: title-frame

<div class="course-mark">ECE 444 · Fall 2026</div>

<h1 class="frame-title">CFAR Processing</h1>

<div class="title-rule"></div>

A threshold set from 32 neighboring cells holds one false alarm in a million at any noise level, losing 1 dB of SNR.

Lesson 30 · Antennas, Phased Arrays, and Radar Systems · Dr. Neil Rogers
::::

::::{frame} Printing
:class: read-only

To print the slides, switch to present mode and print: one slide a sheet,
with room for notes. Print from read mode for the whole lesson.
::::

::::{frame} Learning Objectives
:class: here-30

<ol class="lo-list" style="--module: '4'; counter-reset: lo 6">
  <li>I can apply constant false-alarm rate (CFAR) processing to radar data and evaluate detection performance.</li>
</ol>

```{include} ../../_snippets/m4-strip.md
```

:::{depth}
<a href="../L27-radar-detection/index.html">Lesson 27</a> set a detection threshold from the probability of false alarm, assuming the processor knows the noise power, and ended by showing what happens when it does not. This lesson replaces the assumed noise power with one measured from the data around each cell. That is constant false-alarm rate (CFAR) processing. The lesson derives the threshold, the SNR it gives up, how it fails when the reference cells hold more than noise, and how to check it by counting false alarms. The L30 Lab then runs it twice: on your kit's live range profile in the Phaser app, and on range-Doppler maps in the notebook.

The lesson is reading, done before the lab with Part 1 of the packet. Its examples use a 400 MHz chirp, so its cells are 0.375 m; the app's presets are different, and the numbers you predict for them are yours to work out. The L30 Lab follows the lesson on this page, from The Big Picture on.
:::
::::

::::{frame} A Moving Noise Floor
:class: read-only
:::{present}
- A fixed threshold assumes the noise power $P_n$ is known.
- 3 dB more noise turns $P_{fa} = 10^{-6}$ into $10^{-3}$.
- CFAR measures $P_n$ around each cell it tests.
:::

<a href="../L27-radar-detection/index.html#frame-probability-of-false-alarm">Lesson 27</a> found that noise power in one cell is exponentially distributed with mean $P_n$, so noise alone crosses a threshold $T$ with probability

$$
P_{fa} = e^{-T/P_n} .
$$

The threshold for $P_{fa} = 10^{-6}$ is $T = 13.8\ P_n$, 11.4 dB above the mean noise. If the noise rises by a factor $g$ while $T$ stays put, the probability becomes $P_{fa}^{1/g}$, and a 3 dB rise turns $10^{-6}$ into $10^{-3}$. At a million decisions a second, a modest rate for a range-Doppler radar, that is a thousand false targets a second.

The noise on a real map does move. Stationary clutter fills the cells near zero velocity, strong reflections fill the cells nearest the radar, and the receiver gain sets the level of everything. A fixed threshold high enough for the worst of these misses targets everywhere else. <a href="../L27-radar-detection/index.html#frame-the-fixed-threshold">Lesson 27's last figure</a> showed the alternative: estimate the noise power from the cells around the one being tested, and set the threshold from that estimate.
::::

::::{frame} Cell Under Test, Guard, and Reference
:class: read-only
:::{present}
<img src="../../viz/img/L30-window.svg" alt="A row of range cells. The cell under test in the center is red. Two gray guard cells sit on each side of it, then four blue reference cells on each side. A bracket joins the reference cells: their average times the bias is the threshold the cell under test must cross" style="max-width: 640px; width: 100%; display: block; margin: 0 auto;">

- **Reference** cells estimate the local noise.
- **Guard** cells keep the target's own energy out of the estimate.
- The window slides, so every cell gets its own threshold.
:::

The detector tests one cell at a time, the **cell under test**. On each side of it, it skips a few **guard cells** and then averages a block of **reference cells**. The average is the estimate of the noise power at this cell, and the threshold is that estimate multiplied by a **bias**. If the cell under test exceeds the threshold, the detector declares a target there. Then the window moves one cell and the detector repeats the test, so the detector recomputes the threshold at every cell from that cell's own neighbors.

The figure draws 2 guard and 4 reference cells a side so that the cells are readable. The running example in this lesson uses 2 guard and 16 reference cells a side, $N = 32$ reference cells in all, which is the local-average threshold in Lesson 27's last figure. ADI's <a href="https://analogdevicesinc.github.io/system-level/solutions/platforms/phaser/labs/radar-cfar/" target="_blank" rel="noopener">CFAR lab</a> lists the same steps for the PHASER: pick the cell, skip the guard cells, average the reference cells, multiply by the bias, and compare.
::::

::::{frame} Cell-Averaging CFAR
:class: read-only
:::{present}
$$
\begin{aligned}
\hat{P}_n &= \frac{1}{N}\sum_{i=1}^{N} z_i \\
T &= \alpha\ \hat{P}_n \\
P_{fa} &= \left(1 + \frac{\alpha}{N}\right)^{-N}
\end{aligned}
$$

- $P_{fa}$ depends on $\alpha$ and $N$, and not on $P_n$.
:::

With $z_i$ the power in reference cell $i$, the **cell-averaging** (CA) CFAR estimate of the noise power is the sample mean $\hat{P}_n$, and the threshold is $T = \alpha\hat{P}_n$. The bias $\alpha$ is the number we choose.

For a given estimate, the cell under test crosses the threshold with probability $e^{-T/P_n}$, the Lesson 27 result. The estimate is itself random, so the probability of false alarm is the average of that over the reference cells. Each $z_i$ is independent and exponential with mean $P_n$, and for one such cell the average of $e^{-cz_i/P_n}$ is $1/(1 + c)$. The exponential of a sum is a product, so

$$
\begin{aligned}
P_{fa} &= \left\langle e^{-\alpha\hat{P}_n/P_n} \right\rangle
= \prod_{i=1}^{N}\left\langle e^{-\alpha z_i/(NP_n)} \right\rangle \\
&= \left(1 + \frac{\alpha}{N}\right)^{-N} ,
\end{aligned}
$$

where the angle brackets mean the average over the noise. $P_n$ has dropped out. Wherever the noise sits, whether 0 dB or 15 dB, the probability that noise alone crosses the threshold is the same, which is what *constant false-alarm rate* means. Two assumptions came with it: the reference cells hold only noise, and their noise has the same mean as the noise in the cell under test. The rest of the lesson is about what happens when either one fails.
::::

::::{frame} The Bias From the False-Alarm Probability
:class: read-only
:::{present}
$$
\begin{aligned}
\alpha &= N\left(P_{fa}^{-1/N} - 1\right) \\
&= 32\left(10^{6/32} - 1\right) = 17.3 \\
&= 12.4\ \text{dB}
\end{aligned}
$$

- A known $P_n$ needs 11.4 dB; 32 reference cells need 12.4 dB.
:::

Inverting the false-alarm expression gives the bias for a chosen $P_{fa}$:

$$
\alpha = N\left(P_{fa}^{-1/N} - 1\right) .
$$

For $P_{fa} = 10^{-6}$ and $N = 32$, $\alpha = 32(10^{6/32} - 1) = 17.3$, or 12.4 dB. With 16 reference cells it is 21.9, 13.4 dB; with 144 it is 14.5, 11.6 dB. As $N$ grows,

$$
\begin{aligned}
\alpha &= N\left(e^{\ln(1/P_{fa})/N} - 1\right) \\
&\approx N\left(1 + \frac{\ln(1/P_{fa})}{N} - 1\right) \\
&= \ln(1/P_{fa}) = 13.8 ,
\end{aligned}
$$

which is the 11.4 dB threshold of Lesson 27, because an average over infinitely many cells equals the noise power.

The bias is larger with fewer cells because the estimate scatters. Sometimes it comes out low, the threshold drops with it, and noise crosses more often than it would with the true $P_n$. Raising $\alpha$ compensates for those low estimates. In the code later in this lesson, `bias_db` is $10\log_{10}\alpha$.

:::{note}
ADI's `target_detection_dbfs.py` averages the reference cells **in dB** and adds the bias in dB. That is a different estimator: the average of $10\log_{10}z$ over exponential noise sits 2.5 dB below $10\log_{10}P_n$, so a bias in ADI's code is not the $\alpha$ of this lesson. Its threshold still follows the noise, so it is still a CFAR, but this lesson's numbers do not apply to it. Read ADI's code beside the provided `cfar_2d`, which averages power.
:::
::::

::::{frame} CFAR Loss
:class: read-only
:::{present}
<img src="../../viz/img/L30-cfar-loss.svg" alt="Extra SNR needed for Pd = 0.9 at Pfa = 10 to the minus 6, against the number of reference cells on a log axis from 4 to 256. It falls from about 8 dB at 5 cells to 2.1 dB at 16, 1.0 dB at 32 and 0.2 dB at 144" style="max-width: 600px; width: 100%; display: block; margin: 0 auto;">
:::
:::{present}
- A higher bias needs more SNR for the same $P_d$.
- 32 cells lose 1.0 dB; 16 lose 2.1 dB.
- A higher bias shortens the range: $R \propto \text{SNR}^{-1/4}$.
:::

A target that a known-noise detector finds with $P_d = 0.9$ at $P_{fa} = 10^{-6}$ needs 13.2 dB of SNR (Albersheim's fit in <a href="../L27-radar-detection/index.html#frame-albersheim-s-equation">Lesson 27</a> gave 13.1 dB). The CA-CFAR detector needs more, because its threshold is higher on average and scatters with the estimate. The difference is the **CFAR loss**. The figure computes it by averaging the Lesson 27 detection probability over the scatter of $\hat{P}_n$: 2.1 dB with 16 reference cells, 1.0 dB with 32, and 0.2 dB with 144.

The figure favors many reference cells, but a wider window is more likely to reach noise of a different level. The estimate assumes that every reference cell has the same mean noise as the cell under test. A window 32 cells wide in range spans 12 m at the 0.375 m cells of a 400 MHz chirp, $c/2B$, and the clutter near the radar does not stay level over 12 m. The number of reference cells trades the CFAR loss against how local the estimate is.

Any extra SNR the detector needs shortens the range. The echo power falls as $R^{-4}$ (<a href="../L25-radar-equation/index.html">Lesson 25</a>), so a target that just reaches the threshold at range $R_1$ reaches a threshold $\Delta$ dB higher only out to

$$
\begin{aligned}
\frac{R_2}{R_1} &= 10^{-\Delta/40} \\
&= 10^{-6/40} = 0.71 \quad \text{for } \Delta = 6\ \text{dB},
\end{aligned}
$$

29% less range for 6 dB more bias, if nothing but the noise sets where the target is lost.
::::

::::{frame} Choosing the Guard Cells
:class: read-only
:::{present}
- A Hann window puts −6 dB of the target in each neighboring cell.
- Without guard cells, the target raises its own threshold.
- Guard cells cover the target's extent, in range and in Doppler.
:::

A target does not occupy exactly one cell. The window applied before the FFT, Hann in ADI's scripts and in the <a href="../L29-range-doppler-mti/index.html">L29</a> range-Doppler map, widens the target's peak so that each neighboring cell holds a quarter of its power, 6 dB down. A person is also larger than one 0.375 m range cell of a 400 MHz chirp, and moving arms and legs spread the echo over several Doppler cells.

Without guard cells, that spill lands in the reference cells. Take a 20 dB target with no guard cells and 32 reference cells. Its two neighbors hold 14 dB each, 25 times the noise power, and they raise the estimate from $P_n$ to about $(30 + 2 \times 26)/32 = 2.6\ P_n$, which lifts the threshold by 4.1 dB. The target still crosses, but its margin shrinks from 7.6 dB to 3.5 dB, and a weaker target would not. One or two guard cells a side remove the problem. More guard cells than the target's extent do no harm to the target, but they push the reference cells farther out, where the noise is less likely to match.
::::

::::{frame} CFAR Explorer
:class: viz-frame read-only

:::{depth}
The widget draws one range profile of 240 cells, in dB, with the CFAR threshold over it in green. Cells from 168 on hold clutter 15 dB above the quiet noise. Triangles along the top mark five targets, each with the Hann window's −6 dB neighbors, dark when found and pale when missed: a pair eight cells apart near cell 56, one alone near 104, one in the clear just short of the clutter at 160, and one inside the clutter. Found targets are ringed; noise crossings are red dots, and the widget counts them as false alarms. The readout gives the design $P_{fa}$ for the method, bias, and number of reference cells.

Start at 2 guard and 16 reference cells a side with a 12.4 dB bias, the lesson's running example. Set the guard cells to 0 and watch each target lift its own threshold. Lower the bias until false alarms appear, and compare where they appear with the design $P_{fa}$. Then switch the method to greatest-of and smallest-of, the subject of the next frames, and press New noise for another draw of the same scene.
:::

<iframe src="../../viz/cfar-explorer.html"
        width="100%" height="468"
        style="border: 1px solid #cddce9; border-radius: 6px;"
        loading="lazy"
        title="CFAR threshold over a range profile with clutter and five targets, with guard, reference, bias and method controls">
</iframe>
::::

::::{frame} Failures of Cell Averaging
:class: read-only
:::{present}
<img src="../../viz/img/L30-failures.svg" alt="Two range profiles. Left: an 18 dB target eight cells from a 24 dB target; the cell-averaging threshold rises to about 23 dB over both, above the weaker target, while the smallest-of threshold stays near 13 dB. Right: noise that rises 15 dB at cell 60; the cell-averaging threshold ramps up across the edge, and the greatest-of threshold rises earlier and stays at the clutter level" style="max-width: 760px; width: 100%; display: block; margin: 0 auto;">

- A second target in the window hides the weaker one: **masking**.
- At a clutter edge, one average mixes two noise levels.
:::

Cell averaging assumes that every reference cell holds noise of the same mean as the cell under test. The figure shows the two common ways that fails.

On the left, an 18 dB target sits eight cells from a 24 dB target. When the weaker target is the cell under test, the stronger one and its two neighbors are in its reference window, and they hold about $251 + 2 \times 63$ times the noise power. Spread over 32 cells, that raises the estimate by a factor of about 12.7, 11 dB, so the threshold rises to 23.5 dB and the detector misses the 18 dB target. This is **masking**, and it happens wherever targets are close together: two people walking side by side, or a hand in front of a body.

On the right, the noise rises 15 dB at cell 60, the edge of a clutter region. A cell in the clear just before the edge has half its reference cells in the clutter, so its threshold rises by about 12 dB and a target there is masked. A cell in the clutter just past the edge has half its reference cells in the clear, so its estimate is half what it should be, the threshold sits 3 dB low, and its $P_{fa}$ rises from $10^{-6}$ to $(1 + \alpha/32)^{-16} = 10^{-3}$. The clutter edge produces false alarms on one side and misses on the other.
::::

::::{frame} Greatest-Of and Smallest-Of
:class: read-only
:::{present}
$$
\begin{aligned}
\hat{P}_\text{GO} &= \max\left(\hat{P}_\text{near},\ \hat{P}_\text{far}\right) \\
\hat{P}_\text{SO} &= \min\left(\hat{P}_\text{near},\ \hat{P}_\text{far}\right)
\end{aligned}
$$

- Greatest-of holds $P_{fa}$ at a clutter edge.
- Smallest-of finds a target beside another.
- Each needs its own bias, and loses 0.2 or 0.7 dB more than cell averaging.
:::

Both variants average the two sides of the window separately, $\hat{P}_\text{near}$ over the reference cells nearer the radar and $\hat{P}_\text{far}$ over those farther away, and then keep one of the two.

**Greatest-of** (GO) keeps the larger. At a clutter edge, the side in the clutter wins, so GO compares a cell just inside the clutter with the clutter level, and its false alarms stay near the design value; the dashed red line in the right panel of the last figure does that. GO misses targets in the clear cells just before the edge, which it also compares with the clutter, and it makes masking worse.

**Smallest-of** (SO) keeps the smaller. When a second target sits on one side, the clean side wins and the weaker target is found, as the dashed orange line in the left panel shows. SO fails at clutter edges instead, where it takes the quiet side and lets the clutter through.

Neither max nor min of two averages is an average, so each has its own relation between $\alpha$ and $P_{fa}$. With 16 cells a side and $P_{fa} = 10^{-6}$, GO needs a bias of 12.0 dB on its larger half and SO 13.7 dB on its smaller half, against 12.4 dB for CA. For $P_d = 0.9$, GO needs 0.2 dB more SNR than CA and SO 0.7 dB more. ADI's `cfar()` takes the three methods as `'average'`, `'greatest'`, and `'smallest'`; the widget switches among them.
::::

::::{frame} The Ends of the Map
:class: read-only
:::{present}
- The first and last range cells have reference cells on one side only.
- One-sided with the same bias, $P_{fa}$ rises from $10^{-6}$ to $8 \times 10^{-6}$.
- Doppler wraps: the cell past $+v_\text{max}$ is $-v_\text{max}$.
:::

The window runs out at the ends of the data. In range, a cell within $g + n$ of the first or last cell has fewer reference cells on one side, or none. There are three choices: skip those cells and never declare a detection there; average whatever reference cells exist, which is what this lesson's code does; or raise the bias for the cells with fewer neighbors. With the second choice, 16 reference cells instead of 32, and the bias left at 12.4 dB, $P_{fa}$ rises to $(1 + 17.3/16)^{-16} = 8 \times 10^{-6}$, a small increase that keeps those cells in the test. The one choice to avoid is padding with zeros and counting them, which drags the estimate down and the false alarms up. ADI's `cfar()` does not test the end cells against their own neighbors: it gives them the lowest threshold found anywhere in the profile, so a strong return near either end is reported whatever the noise around it. The cells nearest 0 m on the PHASER hold the kit's own transmit-to-receive leakage, so they are usually excluded in any case.

Doppler is different. The Doppler FFT is periodic: the cell above the highest velocity, $+v_\text{max}$, is the lowest, $-v_\text{max}$. A reference window that runs off one end of the Doppler axis continues at the other, so it never runs out, and the Doppler edge needs no special case.
::::

::::{frame} 2D CFAR on the Range-Doppler Map
:class: read-only
:::{present}
<img src="../../viz/img/L30-window-2d.svg" alt="A grid of range cells by Doppler cells. The red cell under test is in the center of a gray five by five block of guard cells, inside a blue thirteen by thirteen block whose 144 cells outside the guard block are the reference cells" style="max-width: 300px; width: 100%; display: block; margin: 0 auto;">
:::
:::{present}
- The guard and reference cells become nested boxes.
- 2 guard and 4 reference cells each way give 144 cells: 11.6 dB, 0.2 dB loss.
- The zero-velocity clutter ridge is an edge: run MTI first.
:::

The <a href="../L29-range-doppler-mti/index.html">range-Doppler map</a> has two axes, so the window does too. The guard cells become a box around the cell under test, and the reference cells are the ring between that box and a larger one. With 2 guard and 4 reference cells each way from the cell under test, in both range and Doppler, the outer box is 13 by 13 cells and the guard box 5 by 5, so $N = 169 - 25 = 144$. The bias for $P_{fa} = 10^{-6}$ is 11.6 dB and the CFAR loss is 0.2 dB, far better than any one-dimensional window can do while staying within a few cells of the cell under test.

The two directions need not match. With range cells near 0.4 m and velocity cells near 0.1 m/s, a walking person spans a cell or two in range but many cells in Doppler, because the arms and legs move at different speeds from the body. A wider guard band in Doppler than in range keeps that spread out of the estimate.

Without MTI, every stationary object puts its echo at zero velocity, so the map has a ridge of clutter along the zero-Doppler column. To a CFAR window, that ridge is a clutter edge in the Doppler direction: cells on the ridge are compared with an average that is mostly noise, and they are declared targets. MTI from Lesson 29 removes most of the ridge before CFAR runs.

A map of $256 \times 128$ cells, with 144 reference cells each, is 4.7 million additions. A Python loop over every cell is slow, but a convolution of the map with the window does the same sums in a fraction of a second, and the next frame's code works that way.
::::

::::{frame} Detections From the Map
:class: read-only
:::{present}
<img src="../../viz/img/L30-rd-detections.svg" alt="A range-Doppler map from 0 to 9 m and minus 3 to plus 3 meters per second after MTI. Red squares mark the CFAR detections: a cluster of nine cells on a walker at 6 m and plus 1.2 meters per second, a cluster of five on a hand at 2.1 m and minus 0.6 meters per second, and one cell of leftover clutter at 0 m and zero velocity" style="max-width: 620px; width: 100%; display: block; margin: 0 auto;">
:::
:::{present}
- The provided `cfar_2d` returns a detection map and a list of (range, velocity, SNR).
- One target produces a cluster of detections.
- CFAR also detects the clutter that MTI leaves.
:::

The map is synthetic: a walker at 6.0 m and $+1.2$ m/s, a hand at 2.1 m and $-0.6$ m/s, and the clutter a 2-pulse canceller leaves at zero velocity near the radar. CFAR with 2 guard and 4 reference cells each way and an 11.6 dB bias declares both targets and the strongest clutter cell. Each target produces a cluster of detections, because its peak spreads into its neighbors and those neighbors are well above the noise too. A detection list that feeds a classifier or a tracker needs one entry per object, so we reduce each cluster to its strongest cell.

The excerpt is the cell-averaging path of the provided `cfar_2d` in `radar_lab.py`, which the L30 Lab notebook calls; the provided version also takes `method="ca"`, `"go"`, or `"so"` for the variants above. It takes the map in dB, as Lesson 29 plots it, and converts it back to power, because the CFAR statistics of this lesson are for power. `guard` and `ref` are (range, Doppler) pairs of half-widths. The two convolutions sum each cell's reference window and count how many cells it held, so an end cell in range averages only the cells that exist; the code wraps the Doppler axis. Pass the map's axes, and the detection list comes back in meters and meters per second.

```python
import numpy as np
from scipy import signal
def cfar_2d(rd_map, guard, ref, bias_db, axes=None):
    P = 10 ** (rd_map / 10)                                  # dB back to power
    (gr, gv), (rr, rv) = guard, ref                          # (range, Doppler) half-widths
    win = np.ones((2 * (gr + rr) + 1, 2 * (gv + rv) + 1))
    win[rr:rr + 2 * gr + 1, rv:rv + 2 * gv + 1] = 0          # guard cells and the cell under test
    def pad(A): return np.pad(np.pad(A, ((0, 0), (gv + rv,) * 2), "wrap"), ((gr + rr,) * 2, (0, 0)))
    total = signal.fftconvolve(pad(P), win, mode="valid")
    count = signal.fftconvolve(pad(np.ones_like(P)), win, mode="valid")
    snr_db = 10 * np.log10(P / (total / count))              # each cell over its local noise
    det = snr_db > bias_db
    r_ax, v_ax = axes or (np.arange(P.shape[0]), np.arange(P.shape[1]))
    hits = [(r_ax[i], v_ax[j], snr_db[i, j]) for i, j in zip(*np.nonzero(det))]
    return det, hits
```

The SNR in each entry is the cell's power over its own local noise estimate, the same quantity the threshold tests, so it is the number to compare with Lesson 27.
::::

::::{frame} Measuring the False-Alarm Rate
:class: read-only
:::{present}
$$
\hat{P}_{fa} = \frac{\text{false detections}}{\text{cells tested}}
$$

- At $10^{-6}$, a $256 \times 128$ map averages one false alarm every 31 maps.
- Check the design at a lower bias, where false alarms are common.
- $P_d$ is the fraction of maps that find the target.
:::

We set the bias from a design $P_{fa}$ and check it by counting. On maps with no target, or in the cells far from any target, every detection is a false alarm, and the measured probability is the number of false detections over the number of cells tested.

Counting false alarms at the design rate takes many maps: a map of $256 \times 128$ cells is 32 768 decisions, so at $10^{-6}$ it averages 0.03 false alarms, one every 31 maps. Counting ten of them to get the rate within about a third takes 305 maps. Instead, we lower the bias to a design $P_{fa}$ of $10^{-3}$ or $10^{-4}$, where a single map has 3 to 33 false alarms, and check the measured rate against $(1 + \alpha/N)^{-N}$ at a few biases. The expected count is $P_{fa}$ times the cells tested, and a count of rare, independent events scatters by about its own square root: $33 \pm 6$, and $3 \pm 2$. If the counts follow the curve, the extrapolation to $10^{-6}$ is sound; if they come out high, the noise in the reference cells does not match the noise in the cells under test.

A display that redraws one range profile at a time asks a different question: in how many updates does anything cross? With $M$ cells tested an update, the chance that at least one crosses is

$$
\begin{aligned}
P_\text{any} &= 1 - \left(1 - P_{fa}\right)^M .
\end{aligned}
$$

Take 6 reference cells a side, $N = 12$, a 9 dB bias, and 100 cells an update. Then $P_{fa} = (1 + 7.94/12)^{-12} = 2.3\times 10^{-3}$, $P_\text{any} = 0.20$, and about 6 of 30 updates hold a crossing.

We measure the probability of detection the same way, against a target you placed: the fraction of maps in which CFAR declares it. To predict it, read <a href="../L27-radar-detection/index.html#frame-pd-against-pfa">Lesson 27's curves</a>, or invert Albersheim's equation, at the target's SNR less the CFAR loss of the window. A steady target with 13 dB of SNR, tested by a 32-cell window at $10^{-6}$, loses 1.0 dB and is found as often as a 12 dB target with the noise known: $P_d = 0.68$. Which curve applies depends on what changes from map to map. If only the noise changes, the target is steady, and Lesson 27's steady curves apply. A hand or a person whose own echo changes from map to map follows the Swerling numbers of Lesson 27 instead, which are lower at the same average SNR.
::::

::::{frame} Summary
:class: read-only

| Symbol / idea | What it is | Number to remember |
| :-- | :-- | :-- |
| Fixed threshold, noise up by $g$ | $P_{fa}' = P_{fa}^{1/g}$ | 3 dB: $10^{-6} \to 10^{-3}$ |
| Cell under test, guard, reference | test one cell; skip its neighbors; average the next ones | 2 guard and 16 reference cells a side |
| CA-CFAR | $T = \alpha\hat{P}_n$, $P_{fa} = (1 + \alpha/N)^{-N}$ | independent of $P_n$ |
| Bias | $\alpha = N(P_{fa}^{-1/N} - 1)$ | 12.4 dB for 32 cells at $10^{-6}$; 11.4 dB as $N \to \infty$ |
| CFAR loss | extra SNR for the same $P_d$ | 2.1 dB at 16 cells, 1.0 dB at 32, 0.2 dB at 144 |
| Guard cells | keep the target's spread out of the estimate | Hann: −6 dB one cell away |
| Masking | a second target raises the threshold | 24 dB eight cells away hides 18 dB |
| Clutter edge | one average over two noise levels | $P_{fa}$ to $10^{-3}$ just inside the clutter |
| Greatest-of, smallest-of | keep the larger or smaller half | GO for edges, SO for close targets; 0.2 and 0.7 dB more loss |
| Ends of the map | range: one-sided; Doppler: wraps | one-sided at the same bias: $8 \times 10^{-6}$ |
| 2D CFAR | nested boxes on the range-Doppler map | 144 cells: 11.6 dB, 0.2 dB loss |
| Measured $P_{fa}$ | false detections over cells tested | $10^{-6}$ on $256 \times 128$: one every 31 maps |
| Updates with a crossing | $1 - (1 - P_{fa})^M$ for $M$ cells an update | 6 of 30 for $N = 12$, 9 dB, 100 cells |
| Bias and range | $R_2/R_1 = 10^{-\Delta/40}$ | 6 dB more: 0.71 of the range |
::::

::::{frame} Pre-Lab
:class: read-only doc-links

Part 1 of the L30 Lab packet is the pre-lab. Do it before the lab and bring it with you: every Part 2 table has a shaded Predicted cell beside the Measured cell that checks it. The lesson works each method on its own example, so the numbers on this page are not your answers.

| Part 1 | You predict | Method | Checked in |
| :-- | :-- | :-- | :-- |
| Table A | whether a target 3 m out is found at the app's opening setting, at the lesson's window, and with no guard cells | Choosing the Guard Cells; Failures of Cell Averaging; The Ends of the Map | Steps 6 to 8 |
| Table B | how much a 3 dB higher bias shortens the farthest range | CFAR Loss | Steps 10 to 12 |
| Table C | updates of 30 with a noise crossing at three biases | The Bias From the False-Alarm Probability; Measuring the False-Alarm Rate | Steps 13 to 15 |
| Table D | the 2D bias for two false-alarm rates, and the false alarms on an empty map | 2D CFAR on the Range-Doppler Map; Measuring the False-Alarm Rate | Step 17 |
| Table E | whether each method finds a weak target beside a strong one | Failures of Cell Averaging; Greatest-Of and Smallest-Of | Step 18 |
| Table F | $P_d$ at two biases | CFAR Loss; Measuring the False-Alarm Rate | Step 19 |

- <a class="doc-link" href="../../labs/ECE444_Lab_L30_CFAR_blank.pdf" target="_blank" rel="noopener">L30 Lab packet (PDF)</a>
::::

::::{frame} The Big Picture
:::{present}
| Steps | You set | You measure |
| :-- | :-- | :-- |
| 1–4 | Range (CFAR), CFAR on | the range profile |
| 5–8 | window and bias | a target: found? |
| 9–12 | bias, then +3 dB | the walker's ranges |
| 13–16 | three biases, empty beam | crossings |
| 17–21 | notebook tasks | false alarms, $P_d$ |
:::

The L30 Lab runs the lesson's detector twice. In the Phaser app, on its **Range (CFAR)** preset, the kit draws one range profile each display update with a one-dimensional CFAR threshold over it. You place the threshold against a target and the room's clutter, walk through the beam with it applied, and count what crosses it with the beam empty. In the notebook, the provided `cfar_2d` runs on range-Doppler bursts of the **Range + Velocity** preset, the L29 burst: you set the bias for a false-alarm rate and count, compare cell averaging, greatest-of, and smallest-of, measure $P_d$, and make a detection list. Each row of the table fills one table of Part 2 of the packet, beside the prediction you made in Part 1.
::::

::::{frame} Predict First
:class: viz-frame

:::{depth}
Before you tune the app, predict what its threshold does. The widget draws one range profile with the app's processing and the app's three CFAR controls: the kit's leakage at 0 m, a person, and a wall. Set Guard Cells, Ref Cells, and CFAR Bias, and decide before you press **Show threshold** whether the person is found and in how many of 30 updates the noise crosses. Then show it. Any change hides the threshold again, so each guess comes first. The widget runs the lesson's 400 MHz example chirp, with 0.375 m cells over 30 m, not the app's preset, so its answers are not your Part 1 answers; the method is the same.
:::

:::{present}
<iframe src="../../viz/cfar-predict.html"
        width="100%" height="474"
        style="border: 1px solid #cddce9; border-radius: 6px;"
        loading="lazy"
        title="Choose the guard cells, reference cells, and bias of the app's CFAR, predict whether a person is found and how often the noise crosses, then show the threshold">
</iframe>
:::
::::

::::{frame} Bring Up the Kit
:::{present}
- Transmit antenna on **OUT2** before power; the kit faces a clear line, 4 m or longer.
- **Range (CFAR)** preset, your 0 m frequency, Range Max 20 m.
- Range view, CFAR on, Show Threshold.
:::

You need the kit, a tape measure laid along the floor in front of it, a stand-in target (a chair with a backpack on it, or a metal trash can), and a screen recorder on your laptop for Step 9.

1. **Connect the transmit antenna** to **OUT2** with the kit powered off.
2. **Power the kit and open the Phaser app**, and select **FMCW**. Point the kit along a clear line at least 4 m long. Every kit in the room transmits, so anyone in your beam is a target: agree with your neighbors who walks when.
3. **Set the preset.** Choose **Range (CFAR)**. Enter your 0 m frequency from the L28 Lab in **0 m Beat (kHz)**, or press **Calibrate…** and follow it. Leave **Range Max (m)** at 20 and the **FFT Window** at Blackman: Part 1's cell count is for that 0 to 20 m profile.
4. **Turn on CFAR.** Open the **Range** view, turn **CFAR** on, and set **CFAR Mode** to **Show Threshold**: a dashed threshold over the trace, with a marker on every cell that crosses it. The app counts **Guard Cells** and **Ref Cells** on each side of the cell under test and averages the reference cells as power, so Ref Cells $= n$ is the lesson's $N = 2n$. Leave the plot's dB limits alone while you tune: making the clutter fade from the plot hides it from you, not from the detector.
::::

::::{frame} Place the Threshold
:::{present}
- Stand-in at 3 m: you cannot tune the app from inside the beam.
- The app's opening setting, the lesson's window, then your own.
- Your own: the target 3 dB over, every noise peak 3 dB under.
:::

5. **Place the stand-in** 3 m out on the tape. Find its peak in the Range view, and the clutter: the leakage at 0 m, the far wall, any furniture. The leakage and the walls are real echoes and cross any CFAR threshold; note them, but do not tune them away.
6. **The app's opening setting.** With 4 Guard Cells, 16 Ref Cells, and 6 dB, record whether the target is found, its margin over the threshold (negative if it sits below), and the margin of the highest noise peak, from the plot's hover readout. Compare with your prediction.

   <div class="rec" data-lab="L30">
   <label>Step 6: found? <input data-field="a.open.found"></label>
   <label>target margin (dB) <input data-field="a.open.peak"></label>
   <label>noise margin (dB) <input data-field="a.open.noise"></label>
   </div>
7. **The lesson's window.** Set 2 Guard Cells, 16 Ref Cells, and type 12.4 into **CFAR Bias (dB)**. Record the same three readings and compare with your prediction. If the threshold misses the target in Step 6 or here, look at what lies inside the window, $g + n$ cells each side of it.

   <div class="rec" data-lab="L30">
   <label>Step 7: found? <input data-field="a.lesson.found"></label>
   <label>target margin (dB) <input data-field="a.lesson.peak"></label>
   <label>noise margin (dB) <input data-field="a.lesson.noise"></label>
   </div>
8. **Your setting.** Change the three controls until the target sits at least 3 dB over the threshold and the highest noise peak at least 3 dB under it, and record them with both margins. Then set **Guard Cells** to 0, record how far the threshold at the target rises and whether the target is still found, and compare with your prediction. Set the guard cells back, and move the stand-in out of the beam.

   <div class="rec" data-lab="L30">
   <label>Step 8: Guard Cells <input data-field="a.your.g"></label>
   <label>Ref Cells <input data-field="a.your.r"></label>
   <label>CFAR Bias (dB) <input data-field="a.your.b"></label>
   <label>target margin (dB) <input data-field="a.your.peak"></label>
   <label>noise margin (dB) <input data-field="a.your.noise"></label>
   <label>0 guard: rise (dB) <input data-field="a.g0.rise"></label>
   <label>0 guard: found? <input data-field="a.g0.found"></label>
   </div>
::::

::::{frame} Walk the Line
:::{present}
- Detections Only, at your setting, with the screen recording on.
- Walk slowly out from 1 m to the end of the line, and back.
- Again with the bias 3 dB higher; read both recordings afterward.
:::

9. **Apply the threshold.** Set **CFAR Mode** to **Detections Only**, so the plot blanks everything below the threshold, and start your screen recording (Win+Alt+R in the Xbox Game Bar on Windows, Shift+Cmd+5 on a Mac). You cannot walk and read the laptop at once; the recording reads it for you.
10. **Walk the line.** Walk slowly straight out along the tape from 1 m to the far end of the clear line, and back. A fast walk smears your echo across updates. Stop the recording.
11. **Raise the bias 3 dB**, record a second walk the same way, and set the bias back.
12. **Read the recordings.** Play each back and read, from the plot's range axis, the nearest and the farthest range at which your peak stays detected, and anything else that crossed. Divide the second walk's farthest range by the first's and compare the ratio with your prediction.

   <div class="rec" data-lab="L30">
   <label>Step 12, your setting: nearest (m) <input data-field="b.w1.near"></label>
   <label>farthest (m) <input data-field="b.w1.far"></label>
   <label>other crossings <input data-field="b.w1.other"></label>
   <label>+3 dB: nearest (m) <input data-field="b.w2.near"></label>
   <label>farthest (m) <input data-field="b.w2.far"></label>
   <label>other crossings <input data-field="b.w2.other"></label>
   <label>ratio of farthest ranges <input data-field="b.ratio"></label>
   </div>
::::

::::{frame} Count on an Empty Scene
:::{present}
- 3 Guard Cells, 4 Ref Cells, beam clear.
- Watch the crossings at 13, 10, and 7 dB.
- Save Capture; the notebook counts 30 updates at each bias.
- Save two Range + Velocity bursts for the notebook.
:::

13. **Clear the beam.** Set 3 Guard Cells, 4 Ref Cells, and 13 dB, still in **Detections Only**, and step behind the kit. Watch a few seconds of updates at 13 dB, then 10, then 7, and note where the crossings land. A crossing that stays at one range update after update is clutter, not noise. Set the bias back to 13 dB.
14. **Press Save Capture.** It saves 32 updates of the empty scene. The saved chirps do not depend on the CFAR settings, so one capture serves all three biases.
15. **Count in the notebook.** In the first cell set `EMPTY_FILE` to your capture's name; in the Procedure A cell set `G1, R1, BIAS1 = 3, 4, 13.0` and run it; then run the Procedure C cell. It counts the updates, of 30, with a crossing beyond 1 m at 13, 10, and 7 dB. Compare each count with your prediction.

    <div class="rec" data-lab="L30">
    <label>Step 15: updates of 30 at 13 dB <input data-field="c.13"></label>
    <label>at 10 dB <input data-field="c.10"></label>
    <label>at 7 dB <input data-field="c.7"></label>
    <label>where they land <input data-field="c.where"></label>
    <label>capture file <input data-field="c.file"></label>
    </div>
16. **Save two bursts.** Set **Preset** to **Range + Velocity** and press **Save Capture** with the scene still empty; then save one with a hand waving about 2 m out. These are your own versions of `L30_empty.npz` and `L30_wall_hand.npz`, for the notebook.
::::

::::{frame} Run the Notebook
:::{present}
- Task (a): the bias for a false-alarm rate, then count.
- Task (b): cell averaging, greatest-of, smallest-of.
- Task (c): $P_d$ over 50 maps, and the detection list.
:::

Each task names the line to change. To run a task on your own burst, change the file name in the first cell.

17. **Task (a).** Set `BIAS_DB` from `PFA` and `N` (one line) and run the cell at $10^{-3}$; then set `PFA = 1e-4`; then set `WINDOW = None` with `PFA` back at $10^{-3}$. Record what it prints beside your predictions.

    <div class="rec" data-lab="L30">
    <label>Step 17, Hann 1e-3: BIAS_DB <input data-field="d.h3.bias"></label>
    <label>false alarms <input data-field="d.h3.count"></label>
    <label>Hann 1e-4: BIAS_DB <input data-field="d.h4.bias"></label>
    <label>false alarms <input data-field="d.h4.count"></label>
    <label>rectangular 1e-3: false alarms <input data-field="d.r3.count"></label>
    </div>
18. **Task (b).** Run the method cell with `METHOD = "ca"`, then `"go"`, then `"so"`. For each, record whether the weak target in `L30_weak_strong.npz` is found, and how many clusters of false alarms appear in either scene.

    <div class="rec" data-lab="L30">
    <label>Step 18, weak target, "ca" <input data-field="e.ca"></label>
    <label>"go" <input data-field="e.go"></label>
    <label>"so" <input data-field="e.so"></label>
    <label>false-alarm clusters, "ca" <input data-field="e.fa.ca"></label>
    <label>"go" <input data-field="e.fa.go"></label>
    <label>"so" <input data-field="e.fa.so"></label>
    </div>
19. **Task (c), steps 1 and 2.** Run the detection cell at `BIAS_DB_C = 11.6`, then at your Step 17 bias for $10^{-3}$, and record each measured $P_d$. With 50 maps, a measured $P_d$ scatters by about 0.07.

    <div class="rec" data-lab="L30">
    <label>Step 19: P<sub>d</sub> at 11.6 dB <input data-field="f.pd1"></label>
    <label>your 1e-3 bias (dB) <input data-field="f.bias2"></label>
    <label>P<sub>d</sub> at it <input data-field="f.pd2"></label>
    </div>
20. **Task (c), step 3.** Add `axes=(rng, vel)` to the `cfar_2d` call in the last cell and run it. Record each entry of the list, and say which are targets. The cell writes `L30_detections.csv`, every entry kept.

    <div class="rec" data-lab="L30">
    <label>Step 20, entry 1: range (m) <input data-field="f.l1.range"></label>
    <label>velocity (m/s) <input data-field="f.l1.vel"></label>
    <label>SNR (dB) <input data-field="f.l1.snr"></label>
    <label>cells <input data-field="f.l1.cells"></label>
    <label>target or false alarm <input data-field="f.l1.what"></label>
    <label>entry 2: range (m) <input data-field="f.l2.range"></label>
    <label>velocity (m/s) <input data-field="f.l2.vel"></label>
    <label>SNR (dB) <input data-field="f.l2.snr"></label>
    <label>cells <input data-field="f.l2.cells"></label>
    <label>target or false alarm <input data-field="f.l2.what"></label>
    </div>
21. **Save the notebook** with its edits and plots, and upload the `.ipynb` with the packet. Keep the task cells and their variable names as they are.
::::

::::{frame} No Hardware?
:class: read-only

```{note}
You can fill every Measured cell without a kit. Open the Phaser app's
simulator at
<a href="https://livethisdream.github.io/phaser/" target="_blank" rel="noopener">livethisdream.github.io/phaser</a>,
select **FMCW**, and set it up as Steps 3 and 4 describe. Its **Scene** list
gives live targets to tune on: **corners**, three corner reflectors at 1, 2,
and 3 m; **walker**, a person walking out to 4 m and back; and **static**. For
the numbers, press **Load Recording** and open the recording from this lab's
bundle that each block names: the app plays it through the same CFAR, one
update at a time, and loops. The notebook's No Kit cells compute exactly what
the app draws on the same files and print each reading. Tick Recorded on each
table you fill this way.

- **Steps 5 to 8**, Table A: `L30_range_person.npz`, a person standing still 3.0 m out in front of a wall at 6.0 m. In the notebook's Procedure A cell, set `G1, R1, BIAS1` to each row's setting and run it: it prints found or missed and both margins. With 0 guard cells, the rise of the threshold is the drop in the target's margin.
- **Steps 9 to 12**, Table B: `L30_walker.npz`, a person walking from 1.0 m to 4.5 m and back toward a wall at 6.0 m, one update every 0.1 s. The Procedure B cell, at `EXTRA_DB = 0` and then `3`, prints the nearest and farthest ranges.
- **Steps 13 to 15**, Table C: `L30_range_empty.npz`, noise and the kit's leakage with no target. Set `G1, R1, BIAS1 = 3, 4, 13.0` in the Procedure A cell, and run the Procedure C cell.
- **Steps 17 to 21**, Tables D to F: the notebook as shipped, on the recorded bursts.
```

Load Recording sets the waveform and the 0 m frequency from the file, so leave **0 m Beat (kHz)** empty: a value there overrides the file's. The app draws a course recording about 66 dB lower on its dB axis than the notebook's dBFS, because the course files hold full-scale units and the app expects the kit's raw counts. Every number the tables ask for is a difference in dB, so the two agree.
::::

::::{frame} Notebook Setup
:class: read-only

Download this lab's bundle, <a href="../../bundles/L30_lab.zip" download>`L30_lab.zip`</a>, and unzip it into your Module 4 folder from the <a href="../L28-fmcw/index.html#frame-notebook-setup">L28 Lab's Notebook Setup</a>, which has the Python steps. It holds everything the notebook loads: `L30_cfar.ipynb`, the current `radar_lab.py` (replace the copy you have), the six `L30_*.npz` recordings, and the data `README.txt`. Put your own Save Capture files in the same folder. Start Jupyter in the folder with `jupyter lab` and open `L30_cfar.ipynb`. Its first cell prints each file it found; if it reports that `radar_lab` is missing, the module is not in the same folder as the notebook.
::::

::::{frame} Your Part 2 Entries
:class: read-only

This frame collects every box you filled in on this page. Your entries stay in this
browser only, saved as you type. **Download my packet** writes them into Part 2
of the blank packet and saves the PDF; do Parts 1 and 3 on paper or in the PDF
viewer, and upload one PDF to Gradescope with the notebook. If you have already typed Part 1 into
the packet PDF, use **Fill my own copy** and choose that file instead: your Part 1
is kept, and the page adds Part 2 to it. Either way the result is locked, so finish
any typing in the PDF first. **Export entries** saves a small backup file you
can **Import** on another laptop or after clearing your browser. The boxes are
optional: the blank packet is in the next frame, to fill on paper or in a PDF
viewer instead.

<div class="rec-summary" data-lab="L30" data-pdf="../../labs/ECE444_Lab_L30_CFAR_blank.pdf" data-file="ECE444_L30_Lab"></div>
::::

::::{frame} Lab Packet
:class: read-only doc-links

The L30 Lab packet is one submission, turned in complete before Lesson 31, with the notebook. It has three parts:

1. Part 1, Predict (before the lab): the shaded Predicted cells of Tables A to F.
2. Part 2, Measure (your kit or the recorded data): the white Measured cells of the same tables.
3. Part 3, Analyze (after the lab): three prompts about what you measured.

- <a class="doc-link" href="../../labs/ECE444_Lab_L30_CFAR_blank.pdf" target="_blank" rel="noopener">L30 Lab packet (PDF)</a>
::::

::::{frame} For Part 3
:class: read-only

Part 3 asks about three things you measured, each from your own Part 2 numbers and your Part 1 predictions: what set the ranges at which your threshold found you and the walker (Tables A and B); how your false-alarm counts compare with the design (Tables C and D); and which method and bias you would run on the L31 Lab's records, from Tables E and F. Keep `L30_detections.csv`, your captures, and the notebook with your L28 and L29 work. The L31 Lab runs the same chain on its own records, so the file is your record of what this chain found.
::::

::::{frame} Looking Ahead
:class: read-only

Lesson 31 takes the detections CFAR declares and asks what each target is and where it goes next: classification from micro-Doppler, and tracking.
::::
