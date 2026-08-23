<!-- .slide: class="title-slide" -->

<div class="title-left">

# ECE 444

Antennas, Phased Arrays, and Radar Systems

## Lesson 25 — Tapering Lab

Fall 2026 · Dr. Neil Rogers

</div>

<div class="title-right">

![USAFA](./img/01-course-intro/USAFA-logo.png)

</div>

---

## Where we were

- L24: a taper trades sidelobe level for beamwidth and aperture efficiency
- Each family sets its own trade — cosine, triangular, cosine squared
- The PHASER's presets are the discrete, 8-element versions of those families
- The GUI hands you the amplitudes; you still have to know what they cost

**Today the table goes to the bench: predict, sweep, reconcile.**

Note:
Open by putting the L24 table back on the board. Today is the first lab where
the students carry a full prediction column in before touching the hardware.

---

## Today's plan

1. Restate the expectation table — that is the prediction column
2. Separate the two numbers: plotted peak drop and taper efficiency
3. Load Lab preset 3 and take the uniform reference sweep
4. Hann, Blackman, Chebyshev — predict first, then measure
5. Design a taper of your own against a written specification
6. Reconcile the plot with the physics

---

## The expectation table

| Preset | Element gains (%) | HPBW | Peak drop | Taper eff. |
| :-- | :-- | :-- | :-- | :-- |
| Uniform | 100 × 8 | 13.1° | 0 dB | 1.00 |
| Hann | 12, 43, 77, 100 (sym.) | 19.5° | −4.7 dB | 0.75 |
| Blackman | 6, 27, 66, 100 (sym.) | 23.1° | −6.1 dB | 0.66 |
| Chebyshev | 4, 23, 62, 100 (sym.) | 24.3° | −6.5 dB | 0.62 |

<div class="callout">Every row is a <strong>prediction</strong> before it is a measurement. Fill the predicted column in before you press Start.</div>

Note:
The gain lists are symmetric, so only the first four values are shown. On the
hardware all eight sliders are visible and students copy all eight.

---

## Two numbers, not one

The peak the plot drops:

$$\text{peak drop} = 20\log_{10}\left( \frac{\sum a_n}{N} \right)$$

The directivity the array loses:

$$\eta_t = \frac{\left( \sum a_n \right)^2}{N \sum a_n^2}$$

<div class="callout">The first is the <strong>coherent receive-voltage loss</strong>. The second is the <strong>taper efficiency</strong>. For Hann they differ by 3.5 dB.</div>

Note:
This is the central point of the lab. Write both formulas on the board and
keep them there for the whole period.

---

## What the presets do to the elements

<div class="fig" data-inline-svg="./fig/L25-gain-bars.svg" style="max-width:900px; margin:0 auto;"></div>

Blackman and Chebyshev switch the outer aperture almost off — end elements at
6% and 4% of full amplitude.

Note:
Ask which of these should give the widest beam before showing the next slide.
The answer is visible in the bars: the narrower the effective aperture, the
wider the beam.

---

<!-- .slide: class="viz-cue-slide" -->

## What the sweep shows

<div class="fig" data-inline-svg="./fig/L25-taper-traces.svg" style="max-width:820px; margin:0 auto;"></div>

<p class="viz-cue">↗ Interactive on the lesson page</p>

Note:
Demo live: step through the presets in the widget and have the class call out
the beamwidth and peak-drop pills before you read them. Point out that the
uniform sidelobes at plus and minus twenty-two degrees are the only ones
visible above the grass.

---

## The floor sets what you can report

- Noise floor sits about 23 dB below the uniform-taper peak
- Uniform's first sidelobe at −13 dBc is 10 dB clear of it and reads cleanly
- Every tapered preset pushes its first sidelobe below the floor

<div class="callout">The table entry there is <strong>"below the noise floor"</strong>. A number read off the grass reports the receiver, not the antenna.</div>

Note:
Students want to write down a number. Insist on the phrase. This is the same
discipline as reporting a limit rather than a value in any measurement.

---

## Setup

1. HB100 at boresight, about 1 m out, aimed at the centre of the patch row
2. Power up, open `http://phaser.local:8080`
3. **Calibrate** under Configuration — an uncalibrated array carries a taper
   you did not ask for
4. Lab preset **3 Tapering**, Rectangular plot tab
5. Element Gains → **Enforce Symmetric Taper** on

<div class="callout">The source does not move for the rest of the lab. Every number today is a comparison between tapers.</div>

Note:
Simulation mode covers this lab completely — the sim target sits at boresight,
which is where the lab needs it.

---

## Step (a): the uniform reference

- Uniform preset, all eight sliders at 100%
- **Start**, then **Freeze** — that trace is your reference all period
- Read HPBW from the 3 dB points: expect about 13°

Theory says 13.2°. The sweep steps in 2.8125° increments, so the crossings land
between samples and the reading comes back a degree or so off.

Note:
Have them record the Peak Array Gain readout too. Every peak drop later is
measured against this frozen trace.

---

## Step (b): Hann, prediction first

Before pressing Start:

1. Copy the eight slider values: 12, 43, 77, 100, 100, 77, 43, 12
2. Sum them: $\sum a_n = 4.64$, so the peak drop should be −4.7 dB
3. Predicted HPBW from the table: 19.5°

Then sweep. Beam widens 13° → about 19°, peak falls about 4.7 dB, and the
sidelobes at ±22° are gone.

Note:
Do not let anyone press Start before the three predictions are written down.
The whole method of the lab depends on the order.

---

## Step (c): Blackman and Chebyshev

- Same procedure, predict then sweep
- End elements at 6% and 4% — most of the outer aperture is idle
- Beam past 23°, peak past −6 dB
- Sidelobes were already invisible after Hann

<div class="callout">Those five extra degrees of beamwidth return nothing this measurement can see. That is the diminishing return L24 predicted, on the plot.</div>

Note:
Good place to ask what measurement *would* see the difference — a quieter
receiver, or a stronger source, both of which lower the floor relative to the
peak.

---

## Step (d): design your own

**Specification: HPBW no wider than 17°, first sidelobe below −20 dBc.**

<div class="fig" data-inline-svg="./fig/L25-custom-target.svg" style="max-width:700px; margin:0 auto;"></div>

End elements near 40–50% meet both conditions. Set, sweep, read, and adjust.

Note:
Enforce Symmetric Taper stays on, so they move two sliders at a time. Most
groups converge in three iterations. Instructor demo: show what happens with
the switch off and one slider moved alone.

---

## Working the Hann numbers

| Quantity | Work | Result |
| :-- | :-- | :-- |
| Amplitude sum | $0.12 + 0.43 + 0.77 + 1.00$, doubled | 4.64 |
| Square sum | $0.0144 + 0.185 + 0.593 + 1.00$, doubled | 3.584 |
| Peak drop | $20\log_{10}(4.64/8)$ | −4.7 dB |
| Taper efficiency | $21.53 / (8 \times 3.584)$ | 0.751 |
| Directivity loss | $10\log_{10}(0.751)$ | −1.2 dB |

Note:
Work this at the board while the sweeps are running. Every number here comes
from the eight slider values and nothing else.

---

## Where the other 3.5 dB went

<div class="fig" data-inline-svg="./fig/L25-two-numbers.svg" style="max-width:640px; margin:0 auto;"></div>

It was never a loss to begin with. The plot normalizes to full scale, so the
shrinking voltage sum shows up in full. Directivity compares on-axis intensity
to the all-angle average, and the average shrank too.

Note:
The test question: if you re-normalized each trace to its own peak, the 4.7 dB
would disappear from the plot and the beam shape would be unchanged. A link
budget that debits 4.7 dB for the taper overstates the loss by a factor of two
in power.

---

## Reading a disagreement

A student applies Hann, predicts −4.7 dB, and measures −6.8 dB.

$$\sum a_n = 8 \times 10^{-6.8/20} = 3.66$$

That is 0.98 short of 4.64 — one full-amplitude element is at zero.

<div class="callout">The pattern agrees independently: with a centre element dead the trace loses its symmetry and the sidelobes climb back out of the floor.</div>

Note:
This is the practice-set problem in advance. Point out that the peak drop
formula runs backwards as a diagnostic, which is why it is worth memorizing.

---

## Deliverables

1. The four-row taper table: gain list, HPBW predicted and measured, peak drop
   predicted and measured, sidelobe entry, taper efficiency computed
2. Your custom taper: eight gain values, measured HPBW and sidelobe level
3. Two written answers — why the sidelobes vanish but the beamwidth does not,
   and why the peak drop is not the directivity loss

Note:
Collect at the end of the period. The written answers are graded on the
distinction, not on length.

---

## Key point

<div class="callout">The plotted peak drop is a consequence of a shared reference. The <strong>taper efficiency</strong> is the antenna's loss. Record both, and never let one stand in for the other.</div>

Note:
If they take one thing from this lab, this is it. It will appear again in the
radar range equation in L29, where using the wrong one costs 3 dB of range.

---

## Where this is going

- L26: the pattern defects **no taper can fix**
- Grating lobes — full-height copies of the beam, set by element spacing
- Beam squint — the beam moves when the signal frequency drifts
- Phase quantization — a sidelobe floor set by the shifter's bit count

Bring today's Chebyshev sidelobe entry. Next lesson we turn on every third
element and grating lobes appear at ±44° at full height.

Note:
Read the L26 page before class. The contrast with today is the point: a taper
buries sidelobes, and none of these three responds to amplitude weighting at
all.
