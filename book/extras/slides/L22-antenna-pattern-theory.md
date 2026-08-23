<!-- .slide: class="title-slide" -->

<div class="title-left">

# ECE 444

Antennas, Phased Arrays, and Radar Systems

## Lesson 22 — Antenna Pattern Theory

Fall 2026 · Dr. Neil Rogers

</div>

<div class="title-right">

![USAFA](./img/01-course-intro/USAFA-logo.png)

</div>

---

## Where we were

- L16: pattern multiplication — the pattern of an array is the element pattern times the array factor
- L18–L19: the phase ramp steers the beam, and the GUI's sweep finds it
- L20–L21: HPBW, FNBW, and sidelobe level measured against array-factor theory, and most numbers matched
- The ones that did not match: low peaks, short steer angles, unequal sidelobes, structure behind the array

**Everything the array factor got wrong is the element pattern.**

Note:
Open on the L21 lab table. Ask the class which rows matched and which did not. The mismatches were all off broadside, and they were all in the same direction. That pattern is the clue.

---

## Today's plan

1. What the beam sweep actually measures
2. The patch element factor, and the model we will use for it
3. Scan loss: the decibel bookkeeping of steering off broadside
4. Coupling, edges, errors, and the room
5. Reading a real trace before we go measure one

Note:
Theory lesson, and the lab in L23 is built directly on it. The four numbers to leave with are six dBi, nine dB, minus zero point six dB at thirty degrees, and minus three dB at sixty.

---

## What the sweep measures

- The array stares straight ahead; the **beam** is swept electronically
- At each commanded angle: apply the phase ramp, record received power
- The x-axis is the **commanded steer angle**, not a measured arrival angle
- By reciprocity the trace follows the antenna pattern

<div class="callout">
A received-power sweep is a legitimate pattern measurement — but it is a measurement of the <strong>whole</strong> pattern, not of the array factor.
</div>

Note:
Reciprocity is doing real work here. The array does the same thing to an incoming wave that it would do to an outgoing one, so the sweep traces the pattern. Nothing in the sweep isolates the array factor.

---

## The pattern is a product

$$F(\theta) = EF(\theta)\ AF(\theta)$$

- $AF(\theta)$: element positions and phases — geometry
- $EF(\theta)$: the pattern of one element in the array — hardware
- L16 derived this for identical, identically-excited elements

So far we compared measurements to $AF(\theta)$ alone, and it worked.

Note:
Write the product on the board. Ask why we got away with ignoring the element factor for three lessons. Answer on the next slide.

---

## Why the array factor alone worked

$$AF_N(\psi) = \frac{\sin(N\psi/2)}{N\sin(\psi/2)}, \quad \psi = kd(\sin\theta - \sin\theta_0)$$

- Near broadside a patch radiates almost uniformly, so $EF \approx 1$
- Across a $13^\circ$ main lobe at broadside, the element pattern varies by $0.02$ dB
- Steer to $60^\circ$ and the same element pattern is $3$ dB down

<div class="callout">
The array-factor-only model is an approximation that is excellent at broadside and wrong by several decibels at wide scan.
</div>

Note:
Have them compute ten log cosine of six and a half degrees. It is two hundredths of a decibel. That is why L21 worked.

---

## The element: a microstrip patch

<div class="two-col fig-xwide"><div class="col-text">
<p>Eight patches over a continuous <strong>ground plane</strong>.</p>
<p>A patch radiates from its two open edges into one hemisphere, peak at broadside, and the ground plane takes the back hemisphere away.</p>
<p>Broad and smooth: the ideal element has a 120 degree half-power beamwidth and 6 dBi; a real patch is steeper.</p>
</div><div class="col-fig">
<div class="fig" data-inline-svg="./fig/L22-patch-element.svg" style="max-width:520px; margin:0 auto;"></div>
</div></div>

Note:
Point out the physical board. The patches are the eight copper rectangles; the ground plane is the whole back face. There is nothing radiating behind it.

---

## The working model

$$G_e(\theta) = G_e(0)\cos\theta \quad (\text{power}), \qquad EF(\theta) = \sqrt{\cos\theta} \quad (\text{field})$$

The element captures its share of the aperture, and that share projects as $\cos\theta$.

| Quantity | Ideal element | Real patch |
| :-- | :-- | :-- |
| Power roll-off | $\cos\theta$ | $\cos^{1.3}\theta$ to $\cos^{1.5}\theta$ |
| Half-power beamwidth | $120^\circ$ | about $105^\circ$ |
| Directivity | $D_e = 4$, or $6.0$ dBi | 6.0 to 6.8 dBi |

Note:
This is the projected-aperture rule, and it is the model the course uses for scan-loss numbers. Say plainly that a real patch is steeper. The two differ by three tenths of a decibel at thirty degrees and about one and two tenths at sixty, so predictions use the ideal rule and measurements land between the two.

---

## What the ground plane does

- All the radiation goes forward, and the element gain is about 3 dB higher than the same patch without it
- There is no back hemisphere to steer into
- Scan range is $\pm 90^\circ$ by construction — a command past that has no pattern behind it
- The element pattern falls monotonically toward the horizon

<div class="callout">
A bump at $\pm 80^\circ$ in your trace is a wall, a bench, or a person. It is not radiation out the back of the board.
</div>

Note:
This is the single most common misreading of a lab trace. Backlobe structure on this hardware is the room, and we will prove it in L23 by moving the fixture.

---

## Steering rides the element envelope

<div class="fig" data-inline-svg="./fig/L22-pattern-multiplication.svg" style="max-width:820px; margin:0 auto;"></div>

Note:
Beam commanded to forty-five degrees. The thin curve is the array factor, unchanged in shape by steering. The dashed curve never moves. The product cannot rise above the dashed curve, and the peak lands where the two multiply largest.

---

## Scan loss: the bookkeeping, step 1

For $N$ identical elements with uniform excitation, the peak gain is the element gain times the element count:

$$G(\theta_0) = G_e(\theta_0) \times N \quad \longrightarrow \quad G(\theta_0)\ [\text{dBi}] = G_e(\theta_0)\ [\text{dBi}] + 10\log_{10} N$$

- $10\log_{10} 8 = 9.0$ dB of **array gain**
- The elements still add in phase when steered, so this term never changes

Note:
Derive it at the board. Eight coherent voltages give eight times the power over the same noise, and pattern multiplication puts that factor in the array factor's peak. The key point is that steering does not touch it.

---

## Scan loss: the bookkeeping, step 2

The element term carries all of the scan dependence:

$$G_e(\theta_0) = G_e(0) + 10\log_{10}(\cos\theta_0)$$

- The projected-aperture rule is a *power* law, so it enters with a factor of ten
- $G_e(0) = 6.0$ dBi for the ideal element

$$G(\theta_0) = 6.0 + 10\log_{10}(\cos\theta_0) + 9.0 \quad [\text{dBi}]$$

Note:
Two terms, one of which is a constant. Write the combined line and box it. Warn them explicitly: ten log, not twenty log, because the projected-aperture rule is stated in power.

---

## Scan loss: the numbers

| $\theta_0$ | Element term | Peak gain | Real patch |
| :-- | :-- | :-- | :-- |
| $0^\circ$ | $0.0$ dB | $15.0$ dBi | $0.0$ dB |
| $30^\circ$ | $-0.6$ dB | $14.4$ dBi | $-0.9$ dB |
| $45^\circ$ | $-1.5$ dB | $13.5$ dBi | $-2.1$ dB |
| $60^\circ$ | $-3.0$ dB | $12.0$ dBi | $-4.2$ dB |

Scan loss is quoted at the commanded angle, where the array factor equals one.

Note:
The last column is a steeper element, power cosine to the one point four. Measured traces land between the two columns. Ask what the sixty degree row means for a radar's detection range.

---

## Worked example: steered to 45°

| Quantity | Work | Result |
| :-- | :-- | :-- |
| Element gain, broadside | $D_e = 4$ | $6.0$ dBi |
| Element penalty | $10\log_{10}(\cos 45^\circ)$ | $-1.5$ dB |
| Array gain | $10\log_{10} 8$ | $+9.0$ dB |
| Steered peak | $6.0 - 1.5 + 9.0$ | $13.5$ dBi |
| A real patch, steeper | about $0.6$ dB more loss | $12.9$ dBi |

Note:
Walk it line by line. Then ask what the same array does at sixty degrees, and let them get twelve dBi before the next slide.

---

## Gain and beamwidth degrade together

<div class="fig" data-inline-svg="./fig/L22-scan-loss.svg" style="max-width:800px; margin:0 auto;"></div>

Note:
Left axis is the gain at the commanded angle, right axis is the beamwidth. The shaded band is the spread between the ideal element and a real patch. The dotted green line is the L20 result, zero point eight eight six lambda over N d cosine theta zero.

---

<!-- .slide: class="viz-cue-slide" -->

## Element × array, live

- Isotropic element: scan loss stays at $0$ dB, peak angle equals the command
- Ideal element: scan loss reads $-0.6$, $-1.5$, $-3.0$ dB at $30^\circ$, $45^\circ$, $60^\circ$
- Real patch: about a decibel worse at wide scan, and the peak angle lags further

<p class="viz-cue">↗ Interactive on the lesson page</p>

<div class="callout">
$-3$ dB at $60^\circ$ for an ideal element and about $-4$ dB for a real one, with the beam twice as wide — that is the $\pm 60^\circ$ practical scan limit.
</div>

Note:
Demo: set isotropic, sweep the steer slider end to end, and read the pill — zero decibels the whole way. Switch to the ideal element and repeat. Then park at sixty degrees and point at the peak angle pill reading fifty-six point eight.

---

## The sidelobes are no longer symmetric

Beam commanded to $30^\circ$, array factor predicts $-12.8$ dB on both sides:

| Sidelobe | Array factor | Element factor | Measured |
| :-- | :-- | :-- | :-- |
| Inboard, $+7.2^\circ$ | $-12.8$ dBc | $0.0$ dB | $-12.2$ dBc |
| Outboard, $+59.6^\circ$ | $-12.8$ dBc | $-3.0$ dB | $-15.2$ dBc |

<div class="callout">
Sidelobe level is measured <em>relative to the peak</em>, and the element factor moved the peak. The inboard lobe reads higher than theory without getting any stronger.
</div>

Note:
This trips people up every year. Nothing about the sidelobe changed. The reference fell by six tenths of a decibel, so the ratio went up.

---

## Mutual coupling

- Neighbors are a few tenths of a wavelength apart, close enough to induce current on each other
- Each element radiates an **embedded** pattern, not its isolated pattern
- Input impedance shifts too, and it shifts with scan angle
- The eight elements are therefore not identical, which is the one assumption pattern multiplication needs

Effect on the trace: nulls fill in, far sidelobes move by a decibel or two.

Note:
No math today. The point is structural: pattern multiplication uses one average element for all eight, and coupling is exactly the part that difference cannot represent.

---

## Edges and errors

- **Edge elements** have a neighbor on one side only, so their embedded patterns differ most
- On an eight-element array that is a quarter of the aperture behaving differently
- **Phase and gain errors**: $2.8125^\circ$ phase steps, finite gain steps, unequal trace lengths, stale calibration
- Random errors raise the sidelobe floor and limit null depth

Quantization and squint get their own treatment in L26.

Note:
Small arrays wear their edges. A sixty-four element array averages this away; ours cannot. Flag L26 as the lesson that makes the error budget quantitative.

---

## The room is in your data

- Reflections off benches, walls, and people arrive from directions the source is not in
- The error is largest where the true pattern is weakest — far sidelobes and any apparent backlobe
- The range has to be long enough: $r \ge 2D^2/\lambda$ from Module 1
- $D = 98$ mm, $\lambda = 29.1$ mm at 10.3 GHz

$$r \ge \frac{2(0.098)^2}{0.0291} = 0.66\ \text{m}$$

The lab's 1 m separation clears it.

Note:
Ninety-eight millimeters is the span between the outer element centers, seven spacings of fourteen millimeters. Have them check that a half-meter range would not qualify.

---

## What L23 will look like

<div class="fig" data-inline-svg="./fig/L22-measured-vs-predicted.svg" style="max-width:820px; margin:0 auto;"></div>

Note:
Three zones. Main lobe and first sidelobes: the prediction holds to about a decibel. Middle sidelobes: recognizable, not quantitative. Below twenty-three decibels down: the sweep's noise floor, where a null depth means only that the null is deeper than the floor.

---

## Two mechanical effects, not antenna effects

- The sweep steps in $2.8125^\circ$, so peaks and nulls report to the nearest grid point — worth 1 to 3 degrees of apparent beamwidth error
- Hand rotation sets the angle axis, and a fixture offset shifts the whole trace sideways

<div class="callout">
A trace whose <em>shape</em> matches theory but whose peak sits at $31.8^\circ$ for a $30^\circ$ command is a fixture problem, not an antenna problem.
</div>

Note:
Separating instrument error from antenna behavior is half of what the lab teaches. Shape versus position is the fastest diagnostic.

---

## Key point

<div class="callout">
<p>The array factor is what the element <strong>positions and phases</strong> contribute. The pattern is that product with the element's own pattern.</p>
<p><strong>Total gain in dB = element gain at the steer angle + array gain.</strong> The array gain never changes; every decibel of scan loss is the element pattern.</p>
</div>

Note:
If they leave with one line, leave with the second one. It turns every scan-loss question into addition.

---

## Where this is going

- **L23:** measure the pattern two ways — electronic sweep and mechanical rotation — and compare both to array-factor and element-times-array predictions
- **L24:** stop explaining the sidelobes and start designing them, by tapering the element amplitudes
- Bring your L21 measurement table; the rows that missed tolerance are the rows this lesson explains

Note:
Assign the review of the L21 table explicitly. Students who come to L23 with their own mismatches in hand get much more out of the reconciliation step.
