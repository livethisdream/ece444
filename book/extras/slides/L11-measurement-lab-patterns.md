<!-- .slide: class="title-slide" -->

<div class="title-left">

# ECE 444

Antennas, Phased Arrays, and Radar Systems

## Lesson 11 — Measurement Lab 2: Radiation Patterns

Fall 2026 · Dr. Neil Rogers

</div>

<div class="title-right">

![USAFA](./img/01-course-intro/USAFA-logo.png)

</div>

---

## Where we were

- **L9** — the theory: far field, range geometry, gain by comparison, dynamic range.
- **L10** — the impedance lab: you measured what happens at the **terminals**.

<div class="callout"><strong>Today you measure what leaves the antenna.</strong> It is the same antenna, described from its other half.</div>

**This is a lab period. Bring L9 with you.**

Note:
L10 answered "does power get in?" Today answers "where does it go once it's in?" Both are needed before the midterm project, and both are procedure — the reasoning was all in L9.

---

## Safety and good practice

<div class="callout"><strong>The tower turns a real antenna on a real cable.</strong> Nobody inside during a scan, door closed, and <strong>STOP</strong> always reachable.</div>

- Cable slack for the **whole grid**, and the axis in **non-continuous** mode.
- Torque connectors; turn the nut, never the cable body.
- Calibrate, **verify**, then measure. Log the sweep. Name every run.

Note:
Say this every period, and say why. Cable wind-up is the standing hazard and it is slow — it does not announce itself until the cable is tight, and continuous mode ignores the software limits entirely. Check the latched error line in the Turntable section while you are there. The RF is milliwatts and is not the hazard; the hazards are mechanical and electrostatic. Absorber is consumable: the pyramids shed if you brush them and a crushed tip is a permanently worse quiet zone, so nobody leans on the walls and nothing gets rested on the floor absorber. Device Emulation on the front panel is NOT simulation and does not inhibit the motor.

---

## Today's plan

1. Verify the range geometry before taking any data.
2. Scan two principal-plane cuts from the dashboard, with the settings logged.
3. Reduce: normalize, plot, extract HPBW, sidelobe level, front-to-back.
4. Gain by the comparison method; polarization by rotating the source.
5. Decide which of your numbers are meaningful.

Note:
Item 5 is the judgment call; items 1 through 4 are procedure. The rig is fixed and cabled today — one VNA, two horns, one turntable, one browser page driving all of it — so the variable that is left is their discipline.

---

## The range you are measuring on

<div class="fig" data-inline-svg="./fig/L11-range-setup.svg" style="max-width:960px; margin:0 auto;"></div>

Note:
Walk the room through it: one VNA, port 1 out to the fixed source horn, port 2 back from the AUT on the turntable, absorber on every surface. The quantity recorded at each angle is S21 in dB. Point at the quiet zone, and at the stray field that sets the floor they will meet later in the period.

---

## Prove the geometry first

Today's AUT: a pyramidal horn, aperture $24 \times 17$ cm, at $f = 2.45$ GHz, so $\lambda = 12.2$ cm.

| Criterion | AUT | Meaning |
| :-- | :-- | :-- |
| $2D^2/\lambda$ | 1.41 m | phase taper under 22.5° |
| $5D$ | **1.47 m** | amplitude taper small |
| $10\lambda$ | 1.22 m | out of the reactive zone |

The **reference horn** is bigger: $D = 0.422$ m, so it needs **2.91 m**.

At a **3.0 m** separation that clears the reference by only 3%.

**Measure the chamber's separation yourself, and redo these with your number.**

Note:
D is the largest dimension, the 29.4 cm diagonal, not a side. The separation is a property of the chamber, not of their run, but it is theirs to measure once and write down — the worked numbers here are an example, not a datasheet. Two things to draw out: for a small antenna the binding criterion is often $5D$, not $2D^2/\lambda$; and the reference sizes the range, so the gain comparison is the measurement standing closest to the edge of the far field. That 3% belongs in their report.

---

## The chain

| Stage | Job | Failure it causes |
| :-- | :-- | :-- |
| VNA port 1 | one sweep, unchanged | a changed setting looks like pattern |
| source horn | clean known polarization | leaks cross-pol into co-pol |
| AUT on the turntable | one axis, centered on the phase center | tilted, off-center cut |
| VNA port 2 | $S_{21}$ per angle, logged | ambiguous or lost data |

One instrument is both ends. Every angle is **commanded, confirmed, then measured**.

Note:
The chain is a loop, not a line. Ratioing against the source is why source drift divides out — the same argument L9 made for the one-port measurement, now doing work on the range. The run file records both the commanded angle and the angle the card reported, so their positioning error is recoverable afterwards for free.

---

## The dashboard

- **Settings sidebar**: VNA, Turntable, Simulation, Output.
- **Tabs over the plots**: Pattern Measurement, VNA, Turntable, Sweep, Logs.
- **Start scan** and **STOP** sit in the tab header — STOP is never a scroll away.

<div class="callout">The strip along the bottom says what you are talking to: <strong>hardware</strong> or <strong>simulated</strong>, <strong>cal</strong> or <strong>uncal</strong>, connected or not.</div>

Note:
Show them the page before anyone touches hardware. One command brings up the service and the frontend on their own laptop — `./start.sh --sim` — so the controls can be rehearsed the night before. What simulation will not tell them is anything about their antenna: it synthesizes an array-factor pattern for a scan, and for a sweep it returns a mismatched load behind a line, which has no resonance in it anywhere. Rehearse the buttons there, not the physics. Sweep is L10's tab and they will use it twice today: peaking up, and the floor.

---

## Acquisition discipline

1. **Set the sweep first.** Span, points, IF BW, power, $S_{21}$ — log all five. A calibration belongs to a sweep.
2. **Check the cal / uncal pill.** An uncalibrated run is data, never an accident. A pattern wants the **2-port** calibration.
3. **Jog, Sweep, read — then Define here as 0°.** Every number you extract is measured from it.
4. **Step $\le$ HPBW/5.** For a 40° beam that is 8°; take 2° so the sidelobes resolve too.
5. **Repeat one cut.** Two scans that disagree by 1 dB tell you your real uncertainty.

Note:
Order matters: the sweep, then the calibration, then the zero, then the grid. Changing the sweep afterwards leaves the instrument interpolating a correction across a span it never measured — the panel flags it and the log warns again. On step 3, be explicit that nothing shows a live trace while the tower is standing still: the VNA tab draws the last MEASURED angle, so peaking up is jog, capture, read, repeat, with the Sweep tab's marker parked on the frequency they care about. Two minutes of that is also their through check — a peak 20 dB down means a cable, a connector or a horn, and it is cheaper to find now than at angle 90 of 180. Name every run in the Output section; left empty it is stamped from the clock, which keeps runs apart and tells them nothing a week later.

---

## Measure your own floor

- Unmate the AUT and terminate the cable in $50\ \Omega$.
- **Sweep** tab, **Capture: S11 + S21**. Press Sweep, then **Export**.

<div class="callout">Two floors, and you get the higher one. The <strong>instrument</strong> floor is what you just measured. The <strong>chamber</strong> contributes the other, and it shows up as a back level that will not go deeper.</div>

Note:
With the AUT unmated nothing radiates, so the stray field has nothing to scatter — this capture cannot see the chamber's contribution, only the receiver and the leakage. That is exactly L9's two-floor argument. There is no S21-only capture, so the pair costs two sweeps and the S11 trace comes back as a free check that the termination is really a termination. Narrowing the IF bandwidth by a decade buys about 10 dB and costs sweep time on every angle; worth doing once as an experiment, and worth doing before they calibrate.

---

## Reduce the data

- Subtract the peak: every level becomes **dB down from the peak**, and the antenna's absolute level drops out.
- Plot both ways: **polar dB** shows the shape, **rectangular dB** lets you read numbers off the axis.
- Never plot pattern data on a linear scale — the sidelobes disappear at 5% of peak.
- One scan holds **every frequency in the span**. The **Cut freq** selector replots it; label the one you used.

<div class="callout">Normalized pattern shape and absolute gain are <strong>two separate measurements</strong>. The sweep gives shape; the comparison gives gain.</div>

Note:
Sidelobe level is always relative to the peak, and is never quoted as an absolute level.

---

## Three numbers from one cut

| Quantity | Read it as | Typical horn |
| :-- | :-- | :-- |
| HPBW | angle between the $-3$ dB crossings | 40° |
| First sidelobe | level of the first lobe past the first null | $-13$ to $-20$ dB |
| Front-to-back | peak minus the level at 180° | 15 to 25 dB |

Interpolate between samples for the $-3$ dB crossings — do not snap to the nearest grid point.

Note:
Uniform illumination gives −13.3 dB, and a tapered illumination does better. A measured −8 dB points to a range problem before an antenna problem.

---

## Worked example — extraction

Peak $\vert S_{21} \vert = -35.6$ dB at 0°, E-plane cut.

| Quantity | Work | Result |
| :-- | :-- | :-- |
| $-3$ dB level | $-35.6 - 3$ | $-38.6$ dB |
| crossings | $-19.8°$ and $+20.2°$ | HPBW $= 40.0°$ |
| first sidelobe | $-51.4$ dB measured | $-15.8$ dB |
| back level | $-54.0$ dB at 180° | F/B $= 18.4$ dB |

Note:
Everything in the middle column is subtraction. The engineering is in deciding whether the numbers are above the floor.

---

## Gain by comparison

Mount the reference horn in place of the AUT and scan again. **Change nothing else** — same sweep, same cables, same zero, same calibration.

$$G_{AUT} = G_{ref} + \left( P_{AUT} - P_{ref} \right)$$

Everything common to both measurements — transmit power, path loss, cable loss, source gain — cancels in the difference.

<div class="callout">In dB, gain by comparison is <strong>one subtraction</strong>. Its accuracy is the accuracy of the reference plus your alignment.</div>

Note:
This is L9's substitution method, executed. Stress "change nothing else" — moving a cable between the two measurements is a common way to lose 0.5 dB.

---

## Polarization and XPD

- Rotate the **source** 90° about the range axis; the AUT stays put.
- The first cut is **co-pol**; the second is **cross-pol**.
- **Cross-polarization discrimination** is the gap at boresight:

$$\text{XPD} = P_{co} - P_{cross} \quad \text{(dB)}$$

A good linear antenna gives 20 to 30 dB. Below about 15 dB, check the mount alignment before attributing the result to the antenna.

Note:
Ask why we rotate the source and not the AUT: rotating the AUT would also change which cut you are taking.

---

## Worked example — gain and XPD

| Quantity | Work | Result |
| :-- | :-- | :-- |
| reference level | $-32.4$ dB, $G_{ref} = 15.0$ dBi | — |
| AUT level | $-35.6$ dB | $\Delta = -3.2$ dB |
| AUT gain | $15.0 - 3.2$ | $11.8$ dBi |
| predicted | $\eta_{\text{ap}} = 0.5$ aperture formula | $12.3$ dBi |
| cross-pol peak | $-59.9$ dB | XPD $= 24.3$ dB |

Note:
0.5 dB below prediction with a 0.5 dB reference tolerance is agreement, not a discrepancy. Say so in the report — and say why.

---

## Against the simulation

Import the pattern CSV your solver wrote in **L8** into the **Simulation** section.

- Both traces are normalized to their own peak, so dBi and $S_{21}$ dB compare.
- **Rotate** takes out a known mount offset. The footer reports the **RMS deviation**.
- The difference is clamped 30 dB below peak before it is taken.

Note:
First time in the course a predicted pattern and a measured one are on the same axes. The clamp matters more than it sounds: a null one degree off its predicted angle differences to tens of dB against a neighboring lobe, so un-clamped the RMS would report null alignment rather than pattern agreement. If the RMS comes back large, check Rotate before checking the physics.

---

<!-- .slide: class="viz-cue-slide" -->

## What the noise floor removes

<p class="viz-cue">↗ Interactive on the lesson page</p>

<div class="fig" data-inline-svg="./fig/L11-floor-effect.svg" style="max-width:830px; margin:0 auto;"></div>

Note:
Demo live: drag the floor from −45 dB up to −20 dB. HPBW barely moves, the first sidelobe creeps up about 1 dB, the nulls stop at the floor. Then switch averaging to 16 and show that the fuzz smooths but the floor does not drop.

---

## What the floor did

An $8\lambda$ aperture measured with 20 dB of dynamic range:

| Quantity | True | Measured |
| :-- | :-- | :-- |
| HPBW | 6.3° | 6.4° |
| first sidelobe | $-13.3$ dB | $-12.7$ dB |
| first null | below $-40$ dB | $-19.1$ dB |

Averaging 16 sweeps smooths the fuzz. It does **not** move the floor.

Note:
Incoherent power averaging shrinks the variance as 1/N and leaves the mean noise power exactly where it was. To lower the floor you need more transmit power, a narrower resolution bandwidth, or a quieter receiver.

---

## What to trust, in order

<div class="callout"><strong>Beamwidth</strong> is robust, because it is read near the peak.<br>
<strong>Sidelobe levels</strong> are valid only when the lobe sits well above the floor.<br>
<strong>Null depths</strong> are floor-limited and belong in a report as bounds.</div>

Quote every extracted number with the floor beside it, and do not claim any feature within a few dB of it.

Note:
"The null is at least 25 dB deep, limited by our 42 dB dynamic range" is a defensible sentence. "The null is 25 dB deep" is not.

---

## Where the error comes from

| Source | Signature | Size |
| :-- | :-- | :-- |
| chamber stray field | back lobes fill in | sets your floor |
| cable flex on the tower | drift between scans | 0.2 to 0.5 dB |
| pointing misalignment | peak reads low, HPBW biased | 0.2 dB at HPBW/8 |
| reference tolerance | fixed offset on every gain | 0.3 to 0.5 dB |

A fifth, on any run the panel flags: a **calibration that does not match the sweep**.

Note:
Cable flex is the one this rig makes easy to check — repeat a cut untouched and difference the two. On the fifth: correction interpolated across a span it never measured is a plausible-looking answer of unknown quality, and "the dashboard warned me and I scanned anyway" is not a sentence anyone wants in a report.

---

## Deliverables

1. Two **principal-plane cuts**, polar dB, normalized and annotated, with the cut frequency labeled.
2. A table: HPBW, first sidelobe, front-to-back, gain, XPD — each with an uncertainty.
3. Your measured **floor**, and a sentence per row saying whether that number clears it.
4. Comparison against your L8 model, with the RMS deviation quoted and every discrepancy explained.

<div class="callout">Every discrepancy larger than your uncertainty needs a <strong>named cause</strong>. Quote the <strong>run name</strong> behind every figure.</div>

Note:
Item 4 carries most of the grade. A 2 dB gap with a named cause beats a 0.2 dB gap with no discussion. The calibration state and hardware-or-simulation mode are in each run's meta.json and nowhere else — a pattern alone cannot say what it was taken under.

---

## Key point

<div class="callout">Every number you extract from a pattern is bounded by the system's <strong>dynamic range</strong>.<br>
Report each one with the measured floor beside it.</div>

Note:
If they remember one sentence from this lab, this is it.

---

## Where this is going

- This lab is the **dress rehearsal** for the midterm Antenna Pattern Measurement project, due 2 Oct — same chamber, same extraction, a written analysis and no procedure handed to you.
- You now have nine lessons of chamber access before it is due. That is why the measurement block runs here.
- **L12 to L14** go back to antenna families: loops and monopoles, patches and horns, reflectors and Yagis. Every gain figure in them is now a claim you know how to check.

Note:
Several of those antennas are defensible project choices, and they will be reading published patterns with a measurer's eye from here on. Point back at the −13.3 dB sidelobe from the widget: L15 explains why that number is what it is.
