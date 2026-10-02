<!-- .slide: class="title-slide" -->

<div class="title-left">

# ECE 444

Antennas, Phased Arrays, and Radar Systems

## Lesson 21 — Array Factor Lab

Fall 2026 · Dr. Neil Rogers

</div>

<div class="title-right">

![USAFA](./img/01-course-intro/USAFA-logo.png)

</div>

---

## Where we were

- Lesson 16 built the array factor $AF_N(\psi) = \frac{\sin(N\psi/2)}{N\sin(\psi/2)}$ from a phasor sum
- Lesson 18 turned a progressive phase ramp into a commanded beam angle
- Lesson 20 gave beamwidth its formulas: $\theta_{HP} \approx 0.886\ \lambda/(Nd)$ and $\text{FNBW} = 2\arcsin(\lambda/Nd)$
- Lesson 20 closed with an expectation table for eight, four, and two elements

<div class="callout">
Today that table goes to the bench. <strong>Predict, measure, reconcile</strong> — and name the reason for every difference.
</div>

Note:
The midterm project came in last lesson. Today is the first lab where students
own the prediction before they touch the hardware. Emphasize that the third
step, reconciling, is the graded thinking.

---

## Today's plan

1. Restate the prediction table, including the two entries that need care
2. Understand what the Rectangular sweep plots
3. Sweep eight elements, then four, then two
4. Read HPBW, FNBW, and first sidelobe level off each trace
5. Reconcile the measurement against the array factor

Note:
Roughly ten minutes of setup, thirty minutes of sweeping, twenty minutes of
reconciling. The reconciling is where they learn something.

---

## The prediction table

PHASER: $N = 8$, $d = 14$ mm. At 10.3 GHz, $\lambda = 29.1$ mm, so $d/\lambda = 0.481$.

| Active | $Nd$ | HPBW | FNBW | First SLL |
| :-- | :-- | :-- | :-- | :-- |
| 8 | 112 mm | $13^\circ$ | $30^\circ$ | $-12.8$ dB |
| 4 | 56 mm | $27^\circ$ | $62^\circ$ | $-11.3$ dB |
| 2 | 28 mm | $62^\circ$ | $180^\circ$ | none |

<div class="callout">
Both beamwidths depend on the array only through the <strong>active aperture</strong> $Nd$. Halve it and the beam doubles.
</div>

Note:
Ask why the sidelobe column is not three copies of minus thirteen. The answer
is that minus thirteen is the large-N limit; eight elements gets close, four
does not.

---

## Two entries that need care

**$62^\circ$ at $N = 2$** is not from the $0.886\ \lambda/(Nd)$ rule, which returns $53^\circ$.

That rule has a small-angle step inside it. For two elements solve the array factor directly: $\cos(\psi/2) = 1/\sqrt{2}$ gives $\psi = \pi/2$, so $\sin\theta = \lambda/4d = 0.520$ and $\theta = 31.3^\circ$.

**$180^\circ$ FNBW** is a convention, not a measurement. The first null needs $\sin\theta = \lambda/2d = 1.04$, and no real angle satisfies that.

<div class="callout">
The null exists in the mathematics but falls <strong>outside visible space</strong>. No null you can steer to means no first-null beamwidth to measure.
</div>

Note:
Derive the two-element half-power point at the board — it is three lines and it
shows them when a rule of thumb has left its range of validity.

---

## What the sweep plots

The Rectangular trace is **received power versus commanded steer angle**.

- The software steps the beam past a stationary source and records power at each step
- By reciprocity that traces the array pattern
- The x-axis is the angle you commanded, not an angle you measured
- Step size is the ADAR1000 phase LSB as a steering resolution: $2.8125^\circ$

<div class="callout">
65 points across $\pm 90^\circ$. A feature narrower than one step can fall <strong>between samples</strong> entirely.
</div>

Note:
This distinction matters again in L23 and L28. The plot is not a goniometer
trace; it is the array reporting its own sensitivity as a function of where it
was told to look.

---

## Reading the three numbers

<div class="fig" data-inline-svg="./fig/L21-read-the-trace.svg" style="max-width:750px; margin:0 auto;"></div>

Note:
Walk the trace left to right on the projector. Peak first, then the two
three-decibel points, then the two minima that bracket the main lobe, then the
tallest sidelobe. That order is the order of the table they fill in.

---

## Where the measurement leaves the array factor

<div class="fig" data-inline-svg="./fig/L21-ideal-vs-measured.svg" style="max-width:750px; margin:0 auto;"></div>

Note:
Gray is the array factor, blue is what the sweep returns. Point out that the
main lobe agrees almost exactly and everything below about twenty decibels
does not.

---

## Three effects, three numbers

| Effect | What it does | Number |
| :-- | :-- | :-- |
| Noise floor | limits how far down the plot sees | $-23$ dBc |
| Grid straddle | sweep misses the true null angle | $2.8125^\circ$ step |
| Both together | nulls fill in from below | nulls read $-19$ dBc |

<div class="callout">
The 8-element null is at $15.1^\circ$; the nearest sample is $14.06^\circ$. Measured FNBW reads $28.1^\circ$, not $30.1^\circ$ — and all $2^\circ$ of that is the grid.
</div>

Note:
At fourteen point zero six degrees the array factor is already back up to minus
twenty-three decibels, which is the floor. So the sample the sweep does take
lands where the pattern and the noise are equal.

---

<!-- .slide: class="viz-cue-slide" -->

## Ideal versus measured, on a toggle

Set the active aperture to 8, 4, or 2. Read HPBW, FNBW, and first sidelobe level off the ideal curve, then switch measurement effects on and read them again.

- FNBW at $N = 8$: $30.1^\circ$ ideal, $28.1^\circ$ measured
- First SLL at $N = 8$: $-12.8$ dB ideal, $-12.4$ dB measured
- FNBW at $N = 2$: a dash, both ways — there is no null to find

<p class="viz-cue">↗ Interactive on the lesson page</p>

Note:
Demo live: start at eight elements with effects off, toggle effects on, and let
them watch the FNBW pill jump by two degrees while the HPBW pill barely moves.
Then step down to two elements so they see the dash appear.

---

## Setup

- ADALM-PHASER on its stand, 5 V supply, network up
- HB100 at **boresight**, about 1 m out, same height as the patch row, face square to the array
- GUI at `http://phaser.local:8080`; Signal Freq near 10.5 GHz
- Run **Calibrate** once
- Load **Lab preset 2 (Array Factor)** — uniform taper, no steering phase, Rectangular tab

<div class="callout">
Every prediction today is a <strong>broadside</strong> number. A source off boresight by a few degrees slides the whole trace along the angle axis.
</div>

Note:
An uncalibrated array fills its own nulls and lifts its own sidelobes. If they
skip Calibrate they will measure the calibration instead of the array factor,
and the numbers will not reconcile.

---

## Procedure, steps 1 and 2

**Step 1 — full array.** All eight Element Gains at 100. Press **Start**, then **Freeze**. Record peak, HPBW, FNBW, first SLL.

Expect $13^\circ$, $28$ to $30^\circ$, and $-11$ to $-13$ dBc near $\pm 22^\circ$.

**Step 2 — halve it.** In **Element Gains** set Rx1, Rx2, Rx7, Rx8 to 0.

**Predict before you press Start:** $27^\circ$ HPBW, $62^\circ$ FNBW, peak about 6 dB down. Then **Start**, **Freeze**, record.

Note:
Hold them to writing the prediction down before the sweep runs. If they measure
first they will rationalize whatever appears.

---

## Procedure, steps 3 to 5

**Step 3 — halve again.** Everything to 0 except Rx4 and Rx5.

Predict $62^\circ$, no visible null, peak about 12 dB down. **Start**, **Freeze**, record.

**Step 4 — compare all three frozen traces** on one plot.

**Step 5 — restore** all eight gains to 100 before leaving the bench.

<div class="callout">
The two-element trace flattens into the noise well before $\pm 90^\circ$: it falls only 24 dB from its own peak at endfire, and the floor is 11 dB below that peak.
</div>

Note:
Step five is not housekeeping trivia — the next section walks up to a kit with
six elements switched off and loses twenty minutes to it.

---

## Three apertures on one axis

<div class="fig" data-inline-svg="./fig/L21-aperture-halving.svg" style="max-width:750px; margin:0 auto;"></div>

Note:
Two trends, both readable without measuring: the beam doubles at each halving,
and the peak steps down about six decibels. The second step reads five and a
half, which is the next slide.

---

## Why the peak drops about 6 dB

At boresight the elements add **in voltage**, not in power.

$$20\log_{10}\left(\frac{N_{\text{active}}}{8}\right) = -6.0 \text{ dB at } N = 4, \quad -12.0 \text{ dB at } N = 2$$

| Step | Predicted | Plot reads |
| :-- | :-- | :-- |
| 8 to 4 | $-6.0$ dB | $-6.0$ dB |
| 4 to 2 | $-6.0$ dB | $-5.5$ dB |

<div class="callout">
The missing half decibel is the <strong>noise floor</strong>: at two elements the peak is only 11 dB above it.
</div>

Note:
Adding a floor eleven decibels down lifts a reading by about three tenths of a
decibel. That accounts for most of the shortfall, and it is the same arithmetic
that fills the nulls.

---

## Worked example — a six-element aperture

Turn off only Rx1 and Rx8. Six elements, $Nd = 84$ mm.

| Quantity | Work | Result |
| :-- | :-- | :-- |
| HPBW | $13.2^\circ \times 112/84$ | $17.6^\circ$ |
| FNBW | $2\arcsin(29.1/84)$ | $40.6^\circ$ |
| Peak drop | $20\log_{10}(6/8)$ | $-2.5$ dB |

<div class="callout">
$17.6^\circ$ is about six sweep steps wide, so the $2.8125^\circ$ grid has enough resolution to confirm it within a degree or two.
</div>

Note:
Good board problem before the lab starts. It also sets up the practice set,
which asks them to do the same thing for three elements.

---

## The errors grow as the aperture shrinks

| Active | Peak above floor | HPBW calc | HPBW meas | Error |
| :-- | :-- | :-- | :-- | :-- |
| 8 | 23 dB | $13.2^\circ$ | $13.1^\circ$ | $0.1^\circ$ |
| 4 | 17 dB | $27^\circ$ | $29.1^\circ$ | $2.1^\circ$ |
| 2 | 11 dB | $62^\circ$ | $65.4^\circ$ | $3.4^\circ$ |

<div class="callout">
Every one of those errors is the <strong>shrinking gap</strong> between the trace and the noise floor. The array factor did not get worse; the measurement did.
</div>

Note:
This is the slide to come back to in L25, when tapered sidelobes disappear
below the floor entirely and the lab table has to say "below the noise floor"
instead of quoting a number.

---

## Deliverables

**Measurement table**, one row per aperture, calculated columns filled in *before* the bench:

Peak (dBFS) | HPBW meas | HPBW calc | FNBW meas | FNBW calc | First SLL

**Written answer 1.** Why is FNBW quoted as $180^\circ$ at $N = 2$ rather than measured? Name the condition on $\lambda/2d$ and evaluate it.

**Written answer 2.** Each element's own gain is unchanged when the others are off. Why does the peak still drop 6 dB per halving?

Note:
Answer two is the one they get wrong. Watch for students who say the array
"loses gain because it has fewer amplifiers" — the amplifiers are unchanged and
the loss is entirely coherent voltage summation.

---

## Key point

<div class="callout">
<strong>Beamwidth is set by the active aperture; sidelobe level is set by the shape of the distribution.</strong><br><br>
Halving $Nd$ doubled both beamwidths and cost 6 dB of peak, while the uniform taper held the sidelobe near the array-factor value the whole way down.
</div>

Note:
This is the sentence to be able to say without notes. It is also the setup for
L24, where the distribution shape changes and the sidelobe moves while the
aperture stays put.

---

## Where this is going

- Every prediction today treated each element as an **isotropic point**
- That holds near boresight, which is where all three beams pointed
- It fails across a full scan: the array factor says a steered beam keeps its peak height, and the hardware disagrees
- **L22:** the element pattern, and pattern $= EF \times AF$

<div class="callout">
Review pattern multiplication from Lesson 16, and <strong>keep your three frozen traces</strong> — L23 measures the element pattern against them.
</div>

Note:
Close by pointing at the far edges of the eight-element trace. The array factor
alone cannot tell them what happens out there, and that gap is exactly the next
lesson.
