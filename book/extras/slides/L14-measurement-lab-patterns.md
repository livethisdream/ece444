<!-- .slide: class="title-slide" -->

<div class="title-left">

# ECE 444

Antennas, Phased Arrays, and Radar Systems

## Lesson 14 — Measurement Lab 2: Radiation Patterns

Fall 2026 · Dr. Neil Rogers

</div>

<div class="title-right">

![USAFA](./img/01-course-intro/USAFA-logo.png)

</div>

---

## Where we were

- **L11** — high-gain antennas: aperture size sets beamwidth, illumination sets sidelobes.
- **L12** — pattern measurement theory: far field, range geometry, gain by comparison.
- **L13** — impedance lab: you measured what happens at the **terminals**.

<div class="callout"><strong>Today you measure what leaves the antenna.</strong> Same antenna, the other half of its description.</div>

Note:
L13 answered "does power get in?" Today answers "where does it go once it's in?" Both are needed before the midterm project.

---

## Today's plan

1. Build an honest range — and prove it is honest before taking data.
2. Acquire two principal-plane cuts with disciplined settings.
3. Reduce: normalize, plot, extract HPBW, sidelobe level, front-to-back.
4. Gain by the comparison method; polarization by rotating the source.
5. Decide which of your numbers you are allowed to believe.

Note:
Item 5 is the real lesson. Everything above it is procedure; item 5 is judgment.

---

## The range you are building

<div class="fig" data-inline-svg="./fig/L14-range-setup.svg" style="max-width:960px; margin:0 auto;"></div>

Note:
Walk the room through it: transmitter, source antenna fixed, AUT on the rotator, receiver logging power per angle. Point at the floor bounce — that is the error source they will actually see.

---

## Prove the geometry first

Today's AUT: a pyramidal horn, aperture $24 \times 17$ cm, at $f = 2.45$ GHz, so $\lambda = 12.2$ cm.

| Criterion | Value | Meaning |
| :-- | :-- | :-- |
| $2D^2/\lambda$ | 1.41 m | phase taper under 22.5° |
| $5D$ | 1.47 m | amplitude taper small |
| $10\lambda$ | 1.22 m | out of the reactive zone |

Range set at **3.0 m** — clears all three by about 2×.

Note:
D is the largest dimension, the 29.4 cm diagonal, not a side. Note which criterion binds: for a small antenna it is often not the famous one.

---

## The chain

| Stage | Job | Failure it causes |
| :-- | :-- | :-- |
| transmitter | one frequency, stable level | drift looks like pattern |
| source antenna | clean known polarization | leaks cross-pol into co-pol |
| AUT on rotator | one axis, centered on the phase center | tilted, off-center cut |
| receiver | power per angle, logged | ambiguous or lost data |

The instructor's **Pluto-SDR transmit/receive tool** does the measure-rotate-record loop for you.

Note:
Any hardware that gives you power at a known angle works: signal generator plus spectrum analyzer, or the SDR tool. The physics does not care; the discipline does.

---

## Acquisition discipline

1. **One frequency, fixed.** Log it. Re-tuning mid-sweep invalidates the cut.
2. **Find the peak first**, then set 0° there. A pattern referenced to the wrong angle is worthless.
3. **Step $\le$ HPBW/5.** For a 40° beam that is 8°; take 2° so the sidelobes resolve too.
4. **Record the floor**: source off, same settings, same integration.
5. **Repeat one cut.** Two sweeps that disagree by 1 dB tell you your real uncertainty.

Note:
Step 4 is the one everybody skips and the one that decides which numbers survive.

---

## Reduce the data

- Subtract the peak: every level becomes **dB down from the peak**, and the antenna's absolute level drops out.
- Plot both ways: **polar dB** shows the shape, **rectangular dB** lets you read numbers off the axis.
- Never plot pattern data on a linear scale — the sidelobes disappear at 5% of peak.

<div class="callout">Normalized pattern shape and absolute gain are <strong>two separate measurements</strong>. The sweep gives shape; the comparison gives gain.</div>

Note:
Common student error: quoting sidelobe levels in dBm. Sidelobe level is always relative.

---

## Three numbers from one cut

| Quantity | Read it as | Typical horn |
| :-- | :-- | :-- |
| HPBW | angle between the $-3$ dB crossings | 40° |
| First sidelobe | level of the first lobe past the first null | $-13$ to $-20$ dB |
| Front-to-back | peak minus the level at 180° | 15 to 25 dB |

Interpolate between samples for the $-3$ dB crossings — do not snap to the nearest grid point.

Note:
Uniform illumination gives −13.3 dB; anything tapered does better. If you measure −8 dB, suspect the range before you suspect the antenna.

---

## Worked example — extraction

Peak $-35.6$ dBm at 0°, E-plane cut.

| Quantity | Work | Result |
| :-- | :-- | :-- |
| $-3$ dB level | $-35.6 - 3$ | $-38.6$ dBm |
| crossings | $-19.8°$ and $+20.2°$ | HPBW $= 40.0°$ |
| first sidelobe | $-51.4$ dBm measured | $-15.8$ dB |
| back level | $-54.0$ dBm at 180° | F/B $= 18.4$ dB |

Note:
Everything in the middle column is subtraction. The engineering is in deciding whether the numbers are above the floor.

---

## Gain by comparison

Swap the AUT for a calibrated reference horn. **Change nothing else** — same range, same cables, same source, same alignment.

$$G_{AUT} = G_{ref} + \left( P_{AUT} - P_{ref} \right)$$

Everything common to both measurements — transmit power, path loss, cable loss, source gain — cancels in the difference.

<div class="callout">In dB, gain by comparison is <strong>one subtraction</strong>. Its accuracy is the accuracy of the reference plus your alignment.</div>

Note:
This is L12's substitution method, executed. Stress "change nothing else" — moving a cable between the two measurements is the classic way to lose 0.5 dB.

---

## Polarization and XPD

- Rotate the **source** 90° about the range axis; the AUT stays put.
- The first cut is **co-pol**; the second is **cross-pol**.
- **Cross-polarization discrimination** is the gap at boresight:

$$\text{XPD} = P_{co} - P_{cross} \quad \text{(dB)}$$

A good linear antenna gives 20 to 30 dB. Below about 15 dB, suspect a tilted mount before you blame the antenna.

Note:
Ask why we rotate the source and not the AUT: rotating the AUT would also change which cut you are taking.

---

## Worked example — gain and XPD

| Quantity | Work | Result |
| :-- | :-- | :-- |
| reference level | $-32.4$ dBm, $G_{ref} = 15.0$ dBi | — |
| AUT level | $-35.6$ dBm | $\Delta = -3.2$ dB |
| AUT gain | $15.0 - 3.2$ | $11.8$ dBi |
| predicted | $\varepsilon_{ap} = 0.5$ aperture formula | $12.3$ dBi |
| cross-pol peak | $-59.9$ dBm | XPD $= 24.3$ dB |

Note:
0.5 dB below prediction with a 0.5 dB reference tolerance is agreement, not a discrepancy. Say so in the report — and say why.

---

<!-- .slide: class="viz-cue-slide" -->

## The floor eats your pattern

<p class="viz-cue">↗ Interactive on the lesson page</p>

<div class="fig" data-inline-svg="./fig/L14-floor-effect.svg" style="max-width:830px; margin:0 auto;"></div>

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

<div class="callout"><strong>Beamwidth</strong> — robust, it lives near the peak.<br>
<strong>Sidelobes</strong> — only if the lobe is well above the floor.<br>
<strong>Null depths</strong> — almost never; a null measures the floor.</div>

Quote every extracted number with the floor beside it, and refuse to claim any feature within a few dB of it.

Note:
"The null is at least 25 dB deep, limited by our 42 dB dynamic range" is a defensible sentence. "The null is 25 dB deep" is not.

---

## Where the error comes from

| Source | Signature | Size |
| :-- | :-- | :-- |
| floor/wall reflections | ripple riding on the pattern | $\pm 1$ dB |
| cable flex on the rotator | drift between sweeps | 0.2 to 0.5 dB |
| pointing misalignment | peak reads low, HPBW biased | 0.2 dB at HPBW/8 |
| reference tolerance | fixed offset on every gain | 0.3 to 0.5 dB |

Note:
Ripple is diagnostic: count the ripples per degree and you can back out the path-length difference of the reflection.

---

## Deliverables

1. Two **principal-plane cuts**, polar dB, normalized and annotated.
2. A table: HPBW, first sidelobe, front-to-back, gain, XPD — each with an uncertainty.
3. Your measured **noise floor**, and a sentence per row saying whether that number clears it.
4. Comparison against the predicted or datasheet values, with every discrepancy explained.

<div class="callout">Unexplained is not the same as unexplainable. <strong>Explain it.</strong></div>

Note:
Item 4 is where the grade is. A 2 dB gap with a named cause beats a 0.2 dB gap with no discussion.

---

## Key point

<div class="callout">A pattern measurement is a <strong>dynamic-range measurement</strong> in disguise.<br>
Every number you extract is only as deep as your floor lets you see.</div>

Note:
If they remember one sentence from this lab, this is it.

---

## Where this is going

- This lab is the **dress rehearsal** for the midterm Antenna Pattern Measurement project, due at L20 — same range, same extraction, more antennas and a written analysis.
- **Module 2 closes here.** You can now predict a pattern, simulate it, and measure it.
- **L15 opens Module 3**: aperture distributions — how the illumination across an aperture chooses the sidelobe level you just measured.

Note:
Point back at the −13.3 dB sidelobe from the widget: next lesson explains why that number is what it is, and how to trade it against beamwidth.
