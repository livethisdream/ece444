<!-- .slide: class="title-slide" -->

<div class="title-left">

# ECE 444

Antennas, Phased Arrays, and Radar Systems

## Lesson 23 — Antenna Pattern Lab

Fall 2026 · Dr. Neil Rogers

</div>

<div class="title-right">

![USAFA](./img/01-course-intro/USAFA-logo.png)

</div>

---

## Where we were

- L22 split the radiated pattern into element factor times array factor.
- The element factor costs you $0.6\ \text{dB}$ of peak at a $30^\circ$ scan, and it is why a steered beam's two first sidelobes stop matching.
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
6. What an anechoic chamber buys.

Note:
Two walks and one sweep. Budget ten minutes for practice walks — the first two
attempts are always unusable and that is fine.

---

## Two ways to trace a pattern

<div class="fig" data-inline-svg="./fig/L23-two-methods.svg" style="max-width:1000px; margin:0 auto;"></div>

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

**Calibrate first.** A broadside sweep with clean, equal first sidelobes, or stop and fix it.

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

Expect two unusable practice runs. Too fast crams the pattern into the left quarter; too slow runs off the right edge.

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

<div class="fig" data-inline-svg="./fig/L23-time-vs-angle.svg" style="max-width:760px; margin:0 auto;"></div>

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

<div class="fig" data-inline-svg="./fig/L23-steer-compare.svg" style="max-width:790px; margin:0 auto;"></div>

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

Same amplitudes. Different axis, different meaning.

Note:
The agreement in amplitude is the point: two completely different measurements
of the same array land on the same sidelobe level.

---

## What a chamber buys

<div class="fig" data-inline-svg="./fig/L23-range-artifacts.svg" style="max-width:820px; margin:0 auto;"></div>

| Artifact | In your data | What a range does |
| :-- | :-- | :-- |
| Angle | time axis, no calibration | turntable + encoder |
| Amplitude | radius varies with your arm | fixed source mount |
| Reflections | $\pm 1\ \text{dB}$ room ripple | absorber on every surface |
| Far field | taped at $1\ \text{m}$ vs $0.66\ \text{m}$ | fixed, documented separation |

Note:
Four artifacts, and they have one of each sitting in their own data. A ten
centimetre radius error at one metre is about zero point eight decibels, which
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
