---
frame_view: true
---

# L23 Lab — Grating Lobes, Squint, and Quantization

::::{frame}
:class: title-frame

<div class="course-mark">ECE 444 · Fall 2026</div>

<h1 class="frame-title">Grating Lobes, Squint, and Quantization</h1>

<div class="title-rule"></div>

Three departures no taper can fix, measured on your own kit.

L23 Lab · Antennas, Phased Arrays, and Radar Systems · Dr. Neil Rogers
::::

::::{frame} Learning Objectives

<ol class="lo-list" style="--module: '3'; counter-reset: lo 7">
  <li>I can identify beam squint and quantization effects in a phased array and describe their impact on system performance.</li>
</ol>
::::

::::{frame} The three departures no taper can fix
The L22 Lab measured the defect a taper can fix. Lesson 23 derived the three
that it cannot: **grating lobes**, **beam squint**, and **phase
quantization**. Today you measure all three on your own kit. Three steps, each
ten minutes, each the same shape as the taper lab: predict, sweep, record.

Use the Signal Freq the GUI shows for $\lambda$, about 10.5 GHz, so
$\lambda \approx 28.5\ \text{mm}$.
::::

::::{frame} Setup
1. Place the HB100 at boresight, about 1 m from the array face, and mark a
   protractor arc at 1 m for step (b).
2. Open `http://phaser.local:8080`, press **Calibrate** under Configuration,
   and let it finish.
3. Press the **Uniform** taper preset, then **Start**, and **Freeze** the
   trace: it is the reference every peak drop below is read against.
::::

::::{frame} Step (a): grating lobes, every third element
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

::::{frame} Step (a): grating lobes, every fourth element
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

::::{frame} Step (b): beam squint
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

::::{frame} Step (b): beam squint, what to expect
A beam commanded to $\theta_0$ with its phases set at $f_0$ points at
$\sin^{-1}[(f_0/f)\sin\theta_0]$ when observed at $f$. With $f = 10.525$ GHz
and $f_0 = 10.025$ GHz, the beam commanded to $45^\circ$ points at $42.3^\circ$,
so the sweep finds the source only when it commands $47.9^\circ$.

| Signal BW | Est. Angle | Shift, calculated | Shift, measured |
| :-- | :-- | :-- | :-- |
| 10 MHz | $\approx 45^\circ$ | $0.1^\circ$ | reference |
| 500 MHz | $\approx 48^\circ$ | $+2.9^\circ$ | $+2.5$ to $+3.5^\circ$ |

Record both readings and the shift. Lesson 23 derived the relation.
::::

::::{frame} Step (c): phase quantization
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

::::{frame} Step (c): phase quantization, what to expect
| Bits | LSB | Highest lobe beyond $\pm 35^\circ$ | Rule of thumb, $-6B$ dB |
| :-- | :-- | :-- | :-- |
| 7 | $2.8^\circ$ | below the noise floor | $-42$ |
| 4 | $22.5^\circ$ | $-15$ to $-21$ dBc, just above the floor | $-24$ |
| 3 | $45^\circ$ | $-12$ to $-15$ dBc | $-18$ |
| 2 | $90^\circ$ | $-8$ to $-10$ dBc | $-12$ |

The lobes come up out of the floor a few decibels at a time as the bits come
away, and sit 3 to 6 dB above the rule of thumb. The 7-bit row has no number
for the same reason the tapered sidelobes had none in the L22 Lab: this trace's
floor is only 17 to 18 dB under the Blackman peak. Lesson 23 accounts for the gap
between the rule and the measurement.
::::

::::{frame} Step (d): restore
Before you leave: **Use Bits** on, Phase Shift Bits 7, Signal BW 10 MHz, and
the **Uniform** preset.
::::

::::{frame} No hardware?
```{note}
Steps (a) and (c) run unchanged in the simulator, since its source sits at
boresight. Step (b) does not: squint is zero at broadside by definition, and
the simulator's source cannot be moved, so that step has no simulator
equivalent. Use the expectation table.
```
::::

::::{frame} Deliverables
Submit the L23 Lab sheet: **the three tables**, with the calculated columns filled in before
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
The lab sheet is the turn-in document: <a href="../../labs/ECE444_Lab_L23_SquintQuant_blank.pdf" target="_blank" rel="noopener">L23 Lab sheet (PDF)</a>.
::::

::::{frame} Summary — the three departures
| Symbol / idea | What it is | Number to remember |
| :-- | :-- | :-- |
| Grating lobe | a full-height copy of the beam where $\sin\theta = m\lambda/d_\text{eff}$ is real | every third element on: $\pm 43^\circ$ |
| Beam squint | the beam leans toward broadside when $f$ rises above the phase-set $f_0$ | 500 MHz at $45^\circ$: $3^\circ$ |
| Phase quantization | lobes that rise out of the floor as the LSB coarsens | 2 bits: lobes 8 to 10 dB down |
::::

::::{frame} Where this is going
A taper buried the sidelobes in the L22 Lab; today you watched three lobes no
taper touches. Grating lobes are the array factor doing exactly what the
geometry tells it to, squint is the price of setting phases at one frequency
and receiving at another, and quantization lobes rise as the shifter loses
bits. Lesson 24 turns from pattern defects to pattern control: placing a null
at a chosen angle on purpose, with weights that change both amplitude and
phase. The floors you met today come back there, because the sweep's floor
decides how much of a null you can see.
::::
