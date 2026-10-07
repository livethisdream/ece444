---
frame_view: true
---

# L25 - Tapering Lab

::::{frame}
:class: title-frame

<div class="course-mark">ECE 444 · Fall 2026</div>

<h1 class="frame-title">Tapering Lab</h1>

<div class="title-rule"></div>

Today that table goes to the bench.

Lesson 25 Lab · Antennas, Phased Arrays, and Radar Systems · Dr. Neil Rogers
::::

::::{frame}
:::{admonition} Slides
:class: slides
<a href="../../slides/L25-tapering-lab.html" target="_blank" rel="noopener">html slides</a>
<a href="../../slides/L25-tapering-lab.html?print-pdf" target="_blank" rel="noopener">pdf slides</a>
<a href="../../slides/L25-tapering-lab.md" target="_blank" rel="noopener">raw markdown slides</a>
:::
::::

::::{frame} Learning Objectives

<ol class="lo-list lo-sublist" style="--module: '3'; --lo: '7'; counter-reset: lo 5">
  <li>I can apply amplitude tapers on the PHASER and measure the sidelobe and beamwidth changes.</li>
  <li>I can distinguish the plotted peak drop from the directivity loss when a taper is applied.</li>
  <li>I can verify a taper's predicted beam broadening against measurement.</li>
  <li>I can design my own taper and evaluate it against the presets.</li>
</ol>

:::{depth}
Lesson 24 ended with a table of what each taper family costs: sidelobes come
down, the beam broadens, and the aperture gives up some efficiency. Today that
table goes to the bench. You will load each preset on the PHASER, sweep the
beam past the HB100, and check the measured beamwidth and peak level against
the numbers you predicted. The measurement also forces a distinction that is
easy to lose on paper — the **peak drop** you watch happen on the plot is not
the **directivity loss** the array suffers, and the gap between them
is several decibels.

Part 2 of the lab previews objective 3.8 while the kit is out: you measure
grating lobes, beam squint, and phase quantization on the PHASER today, and
Lesson 26 explains what you saw.
:::
::::

::::{frame} What Lesson 24 predicts
The expectation table below is the prediction column for every measurement you
make today. The $a_n$ column is what the GUI writes to the eight Element Gains
sliders when you press a preset button; everything to its right is what the
sweep reads relative to a uniform-taper reference.

| Preset | $a_n$ (%) | HPBW | Peak drop | $\eta_t$ |
| :-- | :-- | :-- | :-- | :-- |
| Uniform | 100 × 8 | $13.1^\circ$ | 0 dB | 1.00 (0 dB) |
| Hann | 12, 43, 77, 100, 100, 77, 43, 12 | $19.5^\circ$ | $-4.7$ dB | 0.75 ($-1.2$ dB) |
::::

::::{frame} What Lesson 24 predicts — Blackman and Chebyshev
| Preset | $a_n$ (%) | HPBW | Peak drop | $\eta_t$ |
| :-- | :-- | :-- | :-- | :-- |
| Blackman | 6, 27, 66, 100, 100, 66, 27, 6 | $23.1^\circ$ | $-6.1$ dB | 0.66 ($-1.8$ dB) |
| Chebyshev | 4, 23, 62, 100, 100, 62, 23, 4 | $24.3^\circ$ | $-6.5$ dB | 0.62 ($-2.1$ dB) |
::::

::::{frame} Record two numbers, not one
The peak drop is the **coherent receive-voltage
loss**: at broadside the eight element signals add in phase, so the summed
voltage is proportional to $\sum a_n$ instead of $N$, and the plotted peak
falls by $20\log_{10}(\sum a_n / N)$. That is the number the Rectangular plot
shows you. The directivity loss is the **taper efficiency**
$\eta_t = (\sum a_n)^2 / (N \sum a_n^2)$, which for the Hann preset is $-1.2$
dB, not $-4.7$ dB. Both numbers are real and both belong in your table, so
record them in separate columns and never let one stand in for the other.
Part 4 works through where the difference comes from.
::::

::::{frame} The floor sets what you can report
One measurement will refuse to give you a number. The sweep's noise floor sits
about 23 dB below the uniform-taper peak, and every tapered preset pushes its
first sidelobe further down than that. The correct table entry in those rows is
**"below the noise floor"**, not a value read off the grass. Quoting $-27$ dBc
from a trace whose floor is at $-23$ dBc reports the noise, not the antenna.
::::

::::{frame} Interactive — the measured sweep for each taper preset
:class: viz-frame

:::{depth}
The widget below runs the same sweep in the browser. Start on Uniform and note
the first sidelobe near $-13$ dBc, then step through the presets and watch two
things happen at once: the main lobe widens and its peak drops, while the
sidelobes sink into the grass. The $\eta_t$ pill is the directivity loss, so
compare it against the peak drop pill each time — the two never agree.
:::

<iframe src="../../viz/taper-measurement.html"
        width="100%" height="500"
        style="border: 1px solid #cddce9; border-radius: 6px;"
        loading="lazy"
        title="Measured beam sweep for the PHASER taper presets, with element gains, HPBW, peak drop and taper efficiency">
</iframe>
::::

::::{frame} Equipment and setup
You need the ADALM-PHASER kit with its Raspberry Pi and Pluto attached, the
HB100 source and its battery, and a laptop on the same network.
::::

::::{frame} Setup
1. Place the HB100 at boresight, about 1 m from the array face, aimed at the
   center of the patch row. Leave it there for all of Part 1: every number
   there is a comparison between tapers, so the source must not move.
2. Power the PHASER, wait for the Pi to boot, and open
   `http://phaser.local:8080` in a browser.
3. In the sidebar, press **Calibrate** under Configuration and let it finish.
   An uncalibrated array carries element-to-element gain and phase errors that
   look exactly like a taper you did not ask for.
4. Press Lab preset **3 Tapering**. This loads the Configuration values for the
   HB100 and selects the **Rectangular** plot tab.
5. Under Element Gains, confirm **Enforce Symmetric Taper** is on. With it on,
   moving one slider moves its mirror-image partner, which is what you want for
   every taper in this lab.
::::

::::{frame} No hardware?
```{note}
Run the backend in simulation mode with
`python phaser_headless.py --sim` and open the same URL. The simulator places
a target at boresight, which is where this lab needs it, and the expectation
table above was measured against it. Every step below works unchanged.
```
::::

::::{frame} Step (a): the uniform reference
Press the **Uniform** taper preset, confirm all eight sliders read 100%, and
press **Start**. Read the Peak Array Gain and Est. Angle values, then press
**Freeze** to hold this trace. It stays on the plot as your reference for the
rest of the lab, and every peak drop you record is measured against it.

Record the uniform HPBW by reading the angles where the trace falls 3 dB below
its own peak. Expect about $13^\circ$, and expect it to disagree with the
$13.2^\circ$ theory value by a degree or so — the sweep steps in $2.8125^\circ$
increments, so the 3 dB crossings land between samples.
::::

::::{frame} Step (b): Hann
Press the **Hann** preset. Before sweeping, do three things:

1. Read the eight slider values and copy them into your table. They should read
   12, 43, 77, 100, 100, 77, 43, 12.
2. Compute $\sum a_n$ and predict the peak drop from
   $20\log_{10}(\sum a_n/N)$.
3. Write down the predicted HPBW from the Part 1 table, $19.5^\circ$.

Now press **Start**. The main lobe should widen from about $13^\circ$ to about
$19^\circ$, the peak should sit about 4.7 dB below the frozen uniform trace,
and the first sidelobes that were plainly visible at $\pm 22^\circ$ should be
gone into the noise. Record the peak drop, the HPBW, and "below the noise
floor" for the sidelobe level.
::::

::::{frame} Step (c): Blackman and Chebyshev
Repeat step (b) for the **Blackman** and **Chebyshev** presets, predicting
before each sweep. These two tapers pull the end elements down to 6% and 4%,
so most of the array's outer aperture is barely contributing: the beam widens
past $23^\circ$ and the peak drops past 6 dB, for sidelobes that were already
invisible after Hann. This is the point of diminishing returns that Lesson 24
described: here it costs 5 degrees of beamwidth and returns nothing this
measurement can see.
::::

::::{frame} Step (d): design your own taper
With Enforce Symmetric Taper still on, design a taper of your own against this
specification:

> **HPBW no wider than $17^\circ$, with the first sidelobe below $-20$ dBc.**

Start from Uniform and pull the two end elements down together, leaving the
middle elements high. A mild taper is enough: put the end elements somewhere
near 40% to 50% and step the elements between them smoothly up to 100%. Work by
iteration — set the sliders, press **Start**, read the
HPBW and the sidelobe level, and adjust. Two or three passes will get you
there.
::::

::::{frame} Step (d): design your own taper, continued
Record your final eight gain values and the measured result. A taper with the
end elements at 45% gives roughly $15^\circ$ of beamwidth, a peak drop near
$-3.3$ dB, and sidelobes that have just reached the floor.

<img src="../../viz/img/L25-custom-target.svg"
     alt="Custom mild taper sweep against the uniform reference, with the design target and noise floor marked"
     style="max-width: 700px; width: 100%; display: block; margin: 1em auto;">
::::

::::{frame} Key point
:::{callout}
Sidelobe control is not all-or-nothing. Pulling only the end elements down by
half takes the first sidelobe from $-13$ dBc to below $-20$ dBc, for 2 degrees
of beamwidth and a third of a decibel of directivity. The presets go much
further than that, at a much higher cost in both.
:::
::::

::::{frame} Step (e): restore
Press the **Uniform** preset before you move on, so Part 2 starts from a known
state.
::::

::::{frame} Part 2: The three departures no taper can fix
Everything you measured in Part 1 is a defect a taper can fix. Lesson 26
covers the three that it cannot: **grating lobes**, **beam squint**, and
**phase quantization**. The kit is on the bench, so you measure all three now
and bring the numbers to Lesson 26, where each one is derived. Three steps,
each ten minutes, each the same shape as Part 1: predict, sweep, record.

Use the Signal Freq the GUI shows for $\lambda$, about 10.5 GHz, so
$\lambda \approx 28.5\ \text{mm}$.
::::

::::{frame} Step (f): grating lobes, every third element
Turn **Enforce Symmetric Taper** off (the gain lists below are not
symmetric), leave the source at boresight, and press Lab preset
**4 Grating Lobes**. It leaves Rx1, Rx4, and Rx7 at 100% and the other five
at 0%, so the three active elements sit $3d = 42\ \text{mm}$ apart.

Before you sweep, solve $\sin\theta = m\lambda/d_\text{eff}$ for every integer
$m$ that gives a real angle. Then press **Start**. Expect three lobes of the
same height: the main lobe at $0^\circ$ and two copies near $\pm 43^\circ$.
Read their angles and their heights against the $0^\circ$ lobe, and the peak
drop against the frozen uniform trace: three elements out of eight is
$20\log_{10}(3/8) = -8.5\ \text{dB}$.
::::

::::{frame} Step (f): grating lobes, every fourth element
Now set Rx4 and Rx7 to 0% and Rx5 to 100%, so only Rx1 and Rx5 are on and
$d_\text{eff} = 4d = 56\ \text{mm}$. Solve for the lobe angles again and
sweep. Expect lobes near $\pm 31^\circ$, and the trace climbing to full
height at both ends of the plot: the $m = 2$ solution needs
$\sin\theta = 1.02$, just past the horizon, so you see its shoulder rather
than its peak. The peak drop is now $20\log_{10}(2/8) = -12\ \text{dB}$.

| Elements on | $d_\text{eff}$ | Lobes, calculated | Lobes, measured | Peak drop |
| :-- | :-- | :-- | :-- | :-- |
| Rx1, Rx4, Rx7 | 42 mm | $\pm 43^\circ$ | $\pm 42$ to $\pm 43^\circ$ | $-8$ to $-9$ dB |
| Rx1, Rx5 | 56 mm | $\pm 31^\circ$, $\pm 90^\circ$ | $\pm 30$ to $\pm 33^\circ$, both ends | $-11$ to $-12$ dB |
::::

::::{frame} Step (g): beam squint
Move the HB100 to about $45^\circ$ on the protractor arc, press **Uniform**,
and press Lab preset **5 Beam Squint**. The preset sets **Signal BW** to
500 MHz, which tells the GUI to compute the steering phases for a frequency
500 MHz *below* the Signal Freq and measure at the Signal Freq. That is what a
signal at the edge of a 500 MHz band sees.

Set Signal BW to 10 MHz first, press **Start**, read **Est. Angle** (it should
report the source, about $45^\circ$), and press **Freeze**. Then set Signal BW
back to 500 MHz and sweep again. The peak moves even though the source did
not.
::::

::::{frame} Step (g): beam squint, what to expect
A beam commanded to $\theta_0$ with its phases set at $f_0$ points at
$\sin^{-1}[(f_0/f)\sin\theta_0]$ when observed at $f$. With $f = 10.525$ GHz
and $f_0 = 10.025$ GHz, the beam commanded to $45^\circ$ points at $42.3^\circ$,
so the sweep finds the source only when it commands $47.9^\circ$.

| Signal BW | Est. Angle | Shift, calculated | Shift, measured |
| :-- | :-- | :-- | :-- |
| 10 MHz | $\approx 45^\circ$ | $0.1^\circ$ | reference |
| 500 MHz | $\approx 48^\circ$ | $+2.9^\circ$ | $+2.5$ to $+3.5^\circ$ |

Record both readings and the shift. Lesson 26 derives the relation.
::::

::::{frame} Step (h): phase quantization
Put the HB100 back at boresight and press Lab preset **6 Quantization**. It
loads the Blackman taper, so every true sidelobe is below the floor and
anything that appears from here on is the phase shifter's doing. Turn
**Use Bits** off: the sweep then keeps stepping the commanded angle by
$2.8125^\circ$ while the **Phase Shift Bits** slider coarsens the phase each
element can take.

Sweep at 7 bits, then 4, 3, and 2. At each setting record the LSB,
$360^\circ/2^B$, and the highest lobe **beyond $\pm 35^\circ$** relative to
the peak. The Blackman main lobe is about $24^\circ$ wide and its skirt only
reaches the floor near $\pm 35^\circ$, so anything closer in is the main
lobe, not a quantization lobe.
::::

::::{frame} Step (h): phase quantization, what to expect
| Bits | LSB | Highest lobe beyond $\pm 35^\circ$ | Rule of thumb, $-6B$ dB |
| :-- | :-- | :-- | :-- |
| 7 | $2.8^\circ$ | below the noise floor | $-42$ |
| 4 | $22.5^\circ$ | $-15$ to $-21$ dBc, just above the floor | $-24$ |
| 3 | $45^\circ$ | $-12$ to $-15$ dBc | $-18$ |
| 2 | $90^\circ$ | $-8$ to $-10$ dBc | $-12$ |

The lobes come up out of the floor a few decibels at a time as the bits come
away, and sit 3 to 6 dB above the rule of thumb. The 7-bit row has no number
for the same reason the tapered sidelobes had none in Part 1: this trace's
floor is only 17 to 18 dB under the Blackman peak. Lesson 26 explains the gap
between the rule and the measurement.
::::

::::{frame} Step (i): restore
Before you leave: **Use Bits** on, Phase Shift Bits 7, Signal BW 10 MHz, and
the **Uniform** preset.
::::

::::{frame} No hardware? Part 2
```{note}
Steps (f) and (h) run unchanged in the simulator, since its source sits at
boresight. Step (g) does not: squint is zero at broadside by definition, and
the simulator's source cannot be moved, so that step has no simulator
equivalent. Use the expectation table.
```
::::

::::{frame} Working the Hann numbers
Work the Hann preset all the way through. The eight amplitudes are
$a_n = 0.12,\ 0.43,\ 0.77,\ 1.00,\ 1.00,\ 0.77,\ 0.43,\ 0.12$, giving

$$\sum a_n = 4.64, \qquad \sum a_n^2 = 3.584 .$$
::::

::::{frame} Peak drop and directivity loss
The plotted peak drop follows from the first sum alone:

$$20\log_{10}\!\left(\frac{4.64}{8}\right) = 20\log_{10}(0.580) = -4.7\ \text{dB}.$$

The directivity loss follows from both sums:

$$\eta_t = \frac{\left(\sum a_n\right)^2}{N \sum a_n^2} = \frac{21.53}{8 \times 3.584} = 0.751 \quad \rightarrow \quad -1.2\ \text{dB}.$$
::::

::::{frame} The plotted drop and the directivity loss compared
<img src="../../viz/img/L25-two-numbers.svg"
     alt="Bar comparison: the plotted peak falls 4.7 dB while directivity falls 1.2 dB, a 3.5 dB difference"
     style="max-width: 620px; width: 100%; display: block; margin: 1em auto;">
::::

::::{frame} Where the other 3.5 dB went
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
::::

::::{frame} The practical statement
The practical statement is short. **The peak drop is a plot artifact of a
common reference; the taper efficiency is the antenna's actual loss.** A system
budget that debits 4.7 dB for the taper overstates the loss by a factor of two
in power.
::::

::::{frame} Worked example — reading a disagreement
:::{admonition} Worked example — reading a disagreement
:class: tip
A student applies the Hann preset, predicts a $-4.7$ dB peak drop, and measures
$-6.8$ dB. Inverting the peak-drop formula gives the sum the array
achieved:

$$\sum a_n = N \times 10^{-6.8/20} = 8 \times 0.457 = 3.66 .$$

That is 0.98 short of 4.64, which is one full-amplitude element. A center
element is set to 0% — either its slider was dragged while Enforce Symmetric
Taper was off, or its channel failed. The pattern gives the same verdict
independently: with one center element dead the trace loses its symmetry and
the sidelobes climb back up instead of staying buried.
:::
::::

::::{frame} Deliverables — the taper table
Submit the following.

**1. The taper table**, one row per preset, with these columns filled in:

| Column | Where it comes from |
| :-- | :-- |
| Preset and the eight $a_n$ values | read off the Element Gains sliders |
| HPBW, predicted and measured | Part 1 table; 3 dB points on your sweep |
| Peak drop, predicted and measured | $20\log_{10}(\sum a_n/N)$; the frozen uniform trace |
::::

::::{frame} Deliverables — the taper table, continued
| Column | Where it comes from |
| :-- | :-- |
| First sidelobe | a value in dBc, or "below the noise floor" |
| $\eta_t$, computed | $(\sum a_n)^2 / (N \sum a_n^2)$, reported as a ratio and in dB |
::::

::::{frame} Deliverables — your taper and written answers
**2. Your custom taper**: the eight gain values you settled on, the measured
HPBW and sidelobe level, and one sentence on how you arrived at them.

**3. Two written answers**, a short paragraph each:

- The tapered sidelobes disappear from the plot, but the beamwidth change is
  easy to see and easy to measure. Explain why the measurement gives you a good
  number for one and no number at all for the other.
- Explain, in your own words, why the peak drop you measured is not the
  directivity your array lost, and what each number would be used for.
::::

::::{frame} Deliverables — Part 2
**4. The three Part 2 tables**, with the calculated columns filled in before
the sweep and one sentence under each:

- Grating lobes: lobe angles and heights for the 42 mm and 56 mm cases, the
  peak drop, and why a grating lobe stands as tall as the main lobe when a
  sidelobe never does.
- Beam squint: Est. Angle at 10 MHz and at 500 MHz, the shift, and what moved
  when the source did not.
- Quantization: the LSB and the highest lobe beyond $\pm 35^\circ$ at 7, 4,
  3, and 2 bits beside the rule of thumb, and why the 7-bit row has no
  number.
::::

::::{frame} Lab sheet
The lab sheet is the turn-in document for all of it: <a href="../../labs/ECE444_Lab_L25_Tapering_blank.pdf" target="_blank" rel="noopener">Lab sheet (PDF)</a>.
::::

::::{frame} Summary — the two numbers
| Symbol / idea | What it is | Number to remember |
| :-- | :-- | :-- |
| $\sum a_n / N$ | coherent receive-voltage fraction at broadside | Hann: $4.64/8 \rightarrow -4.7$ dB |
| $\eta_t = (\sum a_n)^2/(N\sum a_n^2)$ | taper efficiency — the directivity the array loses | Hann: 0.75, or $-1.2$ dB |
::::

::::{frame} Summary — peak drop and beamwidth
| Symbol / idea | What it is | Number to remember |
| :-- | :-- | :-- |
| Peak drop vs $\eta_t$ | the plot reads one, the aperture loses the other | 3.5 dB apart for Hann |
| HPBW with taper | broadens as the aperture is de-weighted | $13.1^\circ$ uniform, $19.5^\circ$ Hann, $24.3^\circ$ Chebyshev |
::::

::::{frame} Summary — noise floor and sweep grid
| Symbol / idea | What it is | Number to remember |
| :-- | :-- | :-- |
| Noise floor | the limit on any sidelobe reading | $\approx -23$ dBc; tapered sidelobes sit below it |
| Sweep grid | steer resolution equals the phase LSB | $2.8125^\circ$, worth 1 to $3^\circ$ of HPBW read error |
::::

::::{frame} Summary — the mild taper
| Symbol / idea | What it is | Number to remember |
| :-- | :-- | :-- |
| Mild taper | most of the sidelobe benefit, little of the cost | ends at 40 to 50%: $15^\circ$, $-0.3$ dB of $\eta_t$ |
::::

::::{frame} Summary — the three departures (Part 2)
| Symbol / idea | What it is | Number to remember |
| :-- | :-- | :-- |
| Grating lobe | a full-height copy of the beam where $\sin\theta = m\lambda/d_\text{eff}$ is real | every third element on: $\pm 43^\circ$ |
| Beam squint | the beam leans toward broadside when $f$ rises above the phase-set $f_0$ | 500 MHz at $45^\circ$: $3^\circ$ |
| Phase quantization | lobes that rise out of the floor as the LSB coarsens | 2 bits: lobes 8 to 10 dB down |
::::

::::{frame} Practice
:class: doc-links

- <a class="doc-link" href="../../practice/ECE444_L25_Practice_blank.pdf" target="_blank" rel="noopener">Problem set (PDF)</a>
- <a class="doc-link doc-key" href="../../practice/ECE444_L25_Practice_SOLUTIONS.pdf" target="_blank" rel="noopener">Solutions (PDF)</a>
::::

::::{frame} Where this is going
Part 1 measured the defect a taper can fix. Part 2 measured the three it
cannot, and Lesson 26 explains them. Grating lobes appear when the element
spacing is too large for the scan angle, and they are full-height copies of
the main beam — no amplitude weighting removes them, because they are the
array factor doing exactly what the geometry tells it to. Beam squint moves
the beam when the signal frequency drifts away from the frequency the phase
shifts were computed for. Phase quantization scatters energy into lobes set
by the shifter's bit count, and you watched them rise by taking bits away.
::::

::::{frame} Before Lesson 26
Read the Lesson 26 page before class, and bring your Part 2 tables with you:
the Chebyshev sidelobe entry from Part 1 beside the grating lobes you measured
at full height with every third element on. The contrast between a taper's
neatly buried sidelobes and a lobe no taper can touch is the whole point, and
Lesson 26 opens on your numbers.
::::
