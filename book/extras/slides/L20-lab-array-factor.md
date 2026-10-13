<!-- .slide: class="title-slide" -->

<div class="title-left">

# ECE 444

Antennas, Phased Arrays, and Radar Systems

## L20 Lab — Array Factor

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

<div class="fig" data-inline-svg="./fig/L20-read-the-trace.svg" style="max-width:750px; margin:0 auto;"></div>

Note:
Walk the trace left to right on the projector. Peak first, then the two
three-decibel points, then the two minima that bracket the main lobe, then the
tallest sidelobe. That order is the order of the table they fill in.

---

## Where the measurement leaves the array factor

<div class="fig" data-inline-svg="./fig/L20-ideal-vs-measured.svg" style="max-width:750px; margin:0 auto;"></div>

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

<div class="fig" data-inline-svg="./fig/L20-aperture-halving.svg" style="max-width:750px; margin:0 auto;"></div>

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

---

## Where we were

- L22 split the radiated pattern into element factor times array factor.
- The element factor takes $0.6\ \text{dB}$ off the peak at a $30^\circ$ scan, and it is why a steered beam's two first sidelobes stop matching.
- Every sweep you have run so far measures the array factor against a **commanded** angle.
- Nothing you have measured yet has a physical angle on its x-axis.

**Today the beam holds still and the source moves.**

Note:
Anchor the period in the L22 prediction. Ask for the three predictions before
showing the next slide: scan loss, sidelobe asymmetry, no back radiation. They
should be able to produce all three from last lesson.

---

## Today's plan

1. Two ways to trace a pattern, and what each one measures.
2. Bring up the array and load Lab Preset 7.
3. Walk the HB100 around the arc at broadside.
4. Steer to $30^\circ$ and walk it again.
5. Compare against an electrical beam sweep.
6. What an anechoic chamber provides.

Note:
Two walks and one sweep. Budget ten minutes for practice walks — a usable run
takes seven to eight seconds across the arc, and that pace takes practice.

---

## Two ways to trace a pattern

<div class="fig" data-inline-svg="./fig/L21-two-methods.svg" style="max-width:1000px; margin:0 auto;"></div>

Note:
Left is every lab since L19. Right is what an antenna range does, and what they
already did once on the midterm project with a single antenna. Same physics,
completely different axis.

---

## They are not the same measurement

| | Sweep the beam | Move the source |
| :-- | :-- | :-- |
| x-axis | commanded steer angle | elapsed time |
| Measures | mostly the array factor | element factor $\times$ array factor |
| Element factor | constant, cancels out | included, shades the trace |
| Angles are | calibrated by the LSB | calibrated by nothing |

<div class="callout">
Hold the source still and the element factor is the <strong>same constant</strong> at every point on the trace. Move the source and it rides on top of the array factor.
</div>

Note:
This is the slide the whole lab turns on. The element factor drops out of a
sweep because the physical angle never changes during it.

---

## What L22 says you will see

- **Scan loss.** Beam at $30^\circ$ peaks about $0.6\ \text{dB}$ below broadside.
- **Sidelobe asymmetry.** Inner first sidelobe $-12.2$ dBc, outer $-15.2$ dBc.
- **No back radiation.** The trace dies toward $\pm 90^\circ$ and there is nothing behind the array.

<div class="callout">
Predict first, measure second, reconcile third. Write the three numbers down <em>before</em> you pick up the HB100.
</div>

Note:
Make them commit to the numbers on the board before the hardware comes out.
The reconciliation at the end is worth much more when the prediction is public.

---

## Kit

- PHASER + Pluto, powered, on the network, GUI at `phaser.local:8080`.
- HB100 on a handheld mount, fresh battery.
- $1\ \text{m}$ of string as a radius gauge, and masking tape.
- Tape the arc on the floor: marks at $-90^\circ$, $0^\circ$, $+90^\circ$, and every $30^\circ$ if there is time.

**Calibrate first.** Confirm a broadside sweep with clean, equal first sidelobes before going on.

Note:
Insist on the calibration check. A stale cal shows up as unequal broadside
sidelobes, and they will spend the period chasing an asymmetry that is not
physics.

---

## Lab Preset 7 — Antenna Pattern

Loads the array in a mode you have not used: **Signal vs Time** on the **Tracking** tab.

- The plot streams received amplitude against wall-clock time.
- The beamformer stops sweeping and **holds** the applied Steer Angle.
- The only thing changing the amplitude is where the source is.

<div class="callout">
Everything you have plotted so far had angle on the x-axis. This one has <strong>seconds</strong>.
</div>

Note:
Walk them through the tab switch on the projector. The mental shift from an
angle axis to a time axis is the part they get wrong on the first run.

---

## Step 1 — the broadside run

1. **Steer Angle** $= 0$, press **Apply**.
2. Stand at $-90^\circ$, HB100 aimed at the array.
3. Start the Tracking plot and walk smoothly to $+90^\circ$ at $1\ \text{m}$.
4. Take seven or eight seconds. Keep the module aimed the whole way.

Practice the walk before recording. Too fast crams the pattern into the left quarter; too slow runs off the right edge.

Note:
Demo one deliberately bad walk — sprint it — so they see the failure mode
before they own it. Then one good one.

---

<!-- .slide: class="viz-cue-slide" -->

## The trace paints as you walk

<p class="viz-cue">↗ Interactive on the lesson page</p>

- Uniform speed and hand-like speed give **completely different** lobe spacing.
- They give the **same** lobe amplitudes: $0.1\ \text{dB}$ peak, $-13.1$ dBc first sidelobe, both ways.
- Switch the steer angle to $30^\circ$ and the main lobe moves to the $30^\circ$ crossing.

Note:
Run the widget live. Uniform profile first, note the two pill values, then
switch to hand-like without touching anything else and read the same two pills
back. That single comparison is the lesson.

---

## Amplitudes survive, angles do not

<div class="fig" data-inline-svg="./fig/L21-time-vs-angle.svg" style="max-width:760px; margin:0 auto;"></div>

Note:
Same samples both panels. Orange ticks are where the source actually was.
Uneven on top, even on the bottom, and the lobe heights are identical.

---

## Step 2 — read the lobe structure

Record three amplitudes relative to the main-lobe peak:

| Lobe | Read as | Expect |
| :-- | :-- | :-- |
| Main lobe | $0$ dBc by definition | reference |
| First sidelobe, left | peak minus main peak | $-11$ to $-13$ dBc |
| First sidelobe, right | peak minus main peak | $-11$ to $-13$ dBc |

<div class="callout">
The amplitudes are trustworthy. The angles are not — the x-axis is time, and your hand speed was not uniform.
</div>

Note:
Have them read their own trace here, not the slide. Two minutes, then collect
a few numbers on the board and look at the spread across benches.

---

## Worked example — dBc off a raw trace

| Quantity | Work | Result |
| :-- | :-- | :-- |
| Main lobe | $-18.4$ dBFS | reference |
| Left sidelobe | $-31.2 - (-18.4)$ | $-12.8$ dBc |
| Right sidelobe | $-29.9 - (-18.4)$ | $-11.5$ dBc |
| Spread | $12.8 - 11.5$ | $1.3\ \text{dB}$ |

The full-scale reference cancels in the ratio. Both readings straddle $-13$ dBc, and the $1.3\ \text{dB}$ spread is about what room multipath produces.

Note:
Emphasize that dBFS to dBc is a subtraction and the reference cancels. A pair
reading minus six and minus seven would not be uniform illumination, and would
send them back to Calibrate.

---

## Step 3 — steer to $30^\circ$ and walk again

<div class="fig" data-inline-svg="./fig/L21-steer-compare.svg" style="max-width:790px; margin:0 auto;"></div>

Note:
Point at the main lobe crossing thirty degrees. That is the most direct
confirmation of beam steering they get all semester — they found the beam by
walking into it.

---

## Three things change

- The main lobe appears at the $30^\circ$ crossing, not at boresight.
- The peak reads lower. Theory says $0.6\ \text{dB}$.
- The sidelobes stop matching: $-12.2$ dBc inner, $-15.2$ dBc outer.

<div class="callout">
Hand wobble is worth about <strong>&plusmn;0.5 dB</strong> on its own. One pair of runs will not resolve a 0.6 dB scan loss. Record the number, state the uncertainty next to it, and say whether the runs are distinguishable.
</div>

Note:
Do not let them claim they measured scan loss from a single pair of walks.
Averaging three runs per steer angle tightens it enough to be worth five extra
minutes.

---

## Step 4 — compare against an electrical sweep

Source back on the $0^\circ$ mark and **left there**. Steer Angle $= 0$, Rectangular tab, **Start**.

| | Mechanical walk | Electrical sweep |
| :-- | :-- | :-- |
| First sidelobes | $-11$ to $-13$ dBc | $-11$ to $-13$ dBc |
| x-axis | elapsed time | commanded steer angle |
| Grid | your gait | $2.8125^\circ$ phase LSB |
| Noise floor | room ripple, $\pm 1\ \text{dB}$ | $23\ \text{dB}$ below peak |

The amplitudes agree; the axes do not mean the same thing.

Note:
The agreement in amplitude is the point: two completely different measurements
of the same array land on the same sidelobe level.

---

## What a chamber provides

<div class="fig" data-inline-svg="./fig/L21-range-artifacts.svg" style="max-width:820px; margin:0 auto;"></div>

| Artifact | In your data | What a range does |
| :-- | :-- | :-- |
| Angle | time axis, no calibration | turntable + encoder |
| Amplitude | radius varies with your arm | fixed source mount |
| Reflections | $\pm 1\ \text{dB}$ room ripple | absorber on every surface |
| Far field | taped at $1\ \text{m}$ vs $0.66\ \text{m}$ | fixed, documented separation |

Note:
Four artifacts, and they have one of each sitting in their own data. A ten
centimeter radius error at one meter is about zero point eight decibels, which
is larger than the scan loss they were trying to measure. That comparison lands
better than any of the others.

---

## Key point

<div class="callout">
Moving the source measures the <strong>pattern</strong>. Sweeping the beam measures the <strong>array factor</strong>. Both give you the same sidelobe amplitudes; only one of them puts a real physical angle on the x-axis, and neither of them gets that angle for free.
</div>

Note:
If they leave with one sentence, this is it.

---

## Deliverables

1. **Annotated trace** — best broadside run, main lobe and both first sidelobes labeled in dBc.
2. **Comparison table** — three lobes, mechanical vs electrical vs calculated.
3. **Two written answers** — why amplitudes survive a sloppy walk but angles do not; which artifacts a chamber removes and which remain.

Note:
Due at the start of next period. The second written answer is the one that
separates students who understood Part 4 from students who read it.

---

## Where this is going

You have a measured $-13$ dBc in your notebook. So far it has been a fact about uniform illumination, not a choice.

**L24 makes it a design variable.** Feed the eight elements unequally — more in the middle, less at the edges — and the sidelobes come down.

The trade is real: $10\ \text{dB}$ of sidelobe suppression widens the main lobe and costs peak gain, and L24 derives how much of each.

Note:
Send them off with the guess: how much beamwidth would you trade to put those
first sidelobes at minus twenty-five dBc? They check it against the numbers
next lesson.
