<!-- .slide: class="title-slide" -->

<div class="title-left">

# ECE 444

Antennas, Phased Arrays, and Radar Systems

## Lesson 27 — Null Steering Theory

Fall 2026 · Dr. Neil Rogers

</div>

<div class="title-right">

![USAFA](./img/01-course-intro/USAFA-logo.png)

</div>

---

## Where we were

- L18: steering the beam with **phase only**, every element at full gain
- L24: shaping the sidelobes with **amplitude only**, every element in phase
- L26: the three ways a pattern breaks on its own — grating lobes, squint, quantization
- Those were accidents, and the job was to avoid them

**Today we break the pattern on purpose, and we use amplitude and phase together.**

Note:
Set the frame in one line: for eleven lessons the main lobe has been the figure of merit. Today the figure of merit is a ratio, and the denominator is something we do not want. Everything else follows from that shift.

---

## Today's plan

1. Why a null can be worth more than gain
2. Steering vectors: writing the array response as a dot product
3. Deriving the weight-subtraction rule, one step at a time
4. The PHASER example end to end: gains, phases, pattern
5. What the null costs and what limits its depth

Note:
Step 3 is the centerpiece and we derive it at the board. Tell them now that the whole rule is one division at the end.

---

## The situation

<div class="fig" data-inline-svg="./fig/L27-jammer-sidelobe.svg" style="max-width:760px; margin:0 auto;"></div>

Target on boresight. Interferer at $+22.5^\circ$, **10 dB stronger** at the aperture.

Note:
Ask what rejects the interferer. The answer they should give: not the angle, the pattern level at that angle. An eight-element uniform array has a minus thirteen decibel first sidelobe, and here the interferer is sitting on it.

---

## The interference arithmetic

| Quantity | Value |
| :-- | :-- |
| Interferer strength at the aperture | +10 dB relative to the target |
| Uniform array pattern level at $+22.5^\circ$ | $-13$ dB |
| Interferer at the beamformer output | $-3$ dB relative to the target |

<div class="callout">
A <strong>3 dB margin</strong> is not a margin. One fade and the receiver tracks the wrong signal.
</div>

Note:
Three decibels is a factor of two in power. Target fluctuation alone routinely exceeds that, so this link is not merely marginal, it is unreliable in a way that will not show up until it matters.

---

## Two ways out

| Fix | What it takes | What it costs |
| :-- | :-- | :-- |
| Raise the target 20 dB | 100 times the transmit power | Amplifier, prime power, signature |
| Lower the pattern 20 dB at $+22.5^\circ$ | Recompute eight gains and eight phases | About 2 dB of main-lobe gain |

<div class="callout">
Moving the pattern <em>down</em> at one angle helps more than moving it <em>up</em> at another.
</div>

Note:
This is the whole motivation for the lesson. A jammer parked in a sidelobe is the reason sidelobe specifications exist; the same arithmetic applies to a co-channel emitter or a strong reflection off a hangar.

---

## The control we have not used yet

Each element carries a **complex weight**

$$w\_n = a\_n e^{j\phi\_n}$$

- $a\_n$ — the Element Gains slider for that channel
- $\phi\_n$ — its Phase Control entry
- Two ADAR1000s give both knobs on all eight elements

L18 used the phases. L24 used the amplitudes. Null steering uses both.

Note:
Emphasize that nothing new is being added to the hardware. The degrees of freedom were always there; we simply have not needed to use them at the same time.

---

## Steering vectors: how a direction looks across the aperture

A wave from angle $\theta$ reaches element $n$ a distance $nd\sin\theta$ earlier:

$$\mathbf{v}(\theta) = \left[\ 1,\ e^{jkd\sin\theta},\ e^{j2kd\sin\theta},\ \ldots\ \right], \qquad v\_n(\theta) = e^{jnkd\sin\theta}$$

<div class="callout">
The steering vector describes the <strong>direction</strong>, not the array's settings.
</div>

Note:
Draw the aperture and one plane wave at an angle on the board. The extra path to element n is n d sine theta, and the extra phase is k times that. Every array result this semester is bookkeeping on this one phase.

---

## The response is a dot product

$$y(\theta) = \mathbf{w}^{T}\mathbf{v}(\theta) = \sum\_{n=0}^{N-1} w\_n\ e^{jnkd\sin\theta}$$

- This is the L16 array factor with the weights left general
- Every pattern in Module 3 is one evaluation of this sum
- Pattern multiplication still applies: multiply by the element factor

Note:
Keep it at phasor-sum level. Sum of N phasors, each with an amplitude we choose and a phase we choose, plus a phase the geometry imposes.

---

## Beam steering, rewritten

To point at $\theta\_0$, make every term add in phase there:

$$w\_n = e^{-jnkd\sin\theta\_0} \qquad \Longleftrightarrow \qquad \mathbf{w}\_\text{d} = \mathbf{v}^{*}(\theta\_0)$$

- The conjugate steering vector **is** the L18 progressive ramp $\Delta\phi = kd\sin\theta\_0$
- With it applied, $y(\theta\_0) = N$ — the peak of the pattern

Note:
This is a change of notation, not of physics. Say so. They programmed exactly this into the ADAR1000s in L19; today we write it as a vector so we can subtract things from it.

---

## The problem, stated exactly

Find $\mathbf{w}$ such that

1. **the response at the interferer is zero:** $\mathbf{w}^{T}\mathbf{v}(\theta\_1) = 0$
2. **$\mathbf{w}$ stays as close as possible to $\mathbf{w}\_\text{d}$**

One complex equation, eight complex unknowns. Condition 1 leaves many solutions; condition 2 picks one.

Note:
Point out the counting. Under-determined problems are normal in array processing, and the second condition is what makes the answer unique and cheap.

---

## Step 1 — build the beam that points at the interferer

$$\mathbf{w}\_\text{n} = \mathbf{v}^{*}(\theta\_1), \qquad w\_{\text{n},n} = e^{-jnkd\sin\theta\_1}$$

- On its own, this points a **full-gain beam straight at the interferer**
- That is the opposite of what we want, and exactly the tool we need

Note:
Ask them what this vector does if you load it alone. Once someone says it points the beam at the jammer, the subtraction on the next slide is obvious rather than magical.

---

## Step 2 — subtract some of it

$$\mathbf{w} = \mathbf{w}\_\text{d} - r\_\text{n}\ \mathbf{w}\_\text{n}$$

- One complex number $r\_\text{n}$ left to choose
- Any $r\_\text{n}$ leaves the main beam roughly in place
- One particular $r\_\text{n}$ makes the response at $\theta\_1$ vanish

Note:
Stress the shape of the move: we are not redesigning the array, we are perturbing the weights we already had by a small multiple of another steering vector.

---

## Step 3 — evaluate at the interferer

$$y(\theta\_1) = \mathbf{w}\_\text{d}^{T}\mathbf{v}(\theta\_1) - r\_\text{n}\ \mathbf{w}\_\text{n}^{T}\mathbf{v}(\theta\_1)$$

Second term: $\mathbf{w}\_\text{n}$ was built to cancel the phase at $\theta\_1$, so

$$\mathbf{w}\_\text{n}^{T}\mathbf{v}(\theta\_1) = N = \mathbf{w}\_\text{n}^{H}\mathbf{w}\_\text{n}$$

First term: the same bookkeeping gives $\mathbf{w}\_\text{d}^{T}\mathbf{v}(\theta\_1) = \mathbf{w}\_\text{n}^{H}\mathbf{w}\_\text{d}$

Note:
Do both dot products on the board. The second one is eight unit phasors all pointing the same way, which is N. The first one is the desired beam's own response toward the jammer, and it is the number that will decide the cost.

---

## Step 4 — solve

Set $y(\theta\_1) = 0$:

$$\mathbf{w}\_\text{n}^{H}\mathbf{w}\_\text{d} - r\_\text{n}\ \mathbf{w}\_\text{n}^{H}\mathbf{w}\_\text{n} = 0$$

<div class="callout">
$$\mathbf{w} = \mathbf{w}_\text{d} - r_\text{n}\ \mathbf{w}_\text{n}, \qquad r_\text{n} = \frac{\mathbf{w}_\text{n}^{H}\mathbf{w}_\text{d}}{\mathbf{w}_\text{n}^{H}\mathbf{w}_\text{n}}$$
</div>

Note:
This is the result of the lesson. It takes one division, with no iteration and no optimizer. Write it on the board and leave it there for the rest of the hour.

---

## Step 5 — verify by substitution

$$y(\theta\_1) = \mathbf{w}\_\text{n}^{H}\mathbf{w}\_\text{d} - \frac{\mathbf{w}\_\text{n}^{H}\mathbf{w}\_\text{d}}{\mathbf{w}\_\text{n}^{H}\mathbf{w}\_\text{n}}\ \mathbf{w}\_\text{n}^{H}\mathbf{w}\_\text{n} = 0$$

<div class="callout">
The null is <strong>exact</strong>, not approximate — before quantization gets to it.
</div>

Note:
Substitution takes ten seconds and it is worth doing in front of them, because it shows there is no approximation hiding anywhere in the derivation.

---

## Reading $r\_\text{n}$: a projection

$$r\_\text{n} = \frac{\mathbf{w}\_\text{n}^{H}\mathbf{w}\_\text{d}}{\mathbf{w}\_\text{n}^{H}\mathbf{w}\_\text{n}}$$

- Measures **how much of the null-direction beam is already inside the desired beam**
- Subtracting $r\_\text{n}\mathbf{w}\_\text{n}$ removes exactly that much and no more
- That is why the main beam survives the operation

Note:
Say the word projection once and define it by the formula. Same structure as resolving a vector onto another direction; the inner product on top, the length squared on the bottom.

---

## Reading $r\_\text{n}$: it is the pattern you already have

For a broadside beam, $\mathbf{w}\_\text{d} = [1, 1, \ldots, 1]$:

$$r\_\text{n} = \frac{1}{N}\sum\_{n=0}^{N-1} e^{jnkd\sin\theta\_1} = \frac{1}{N}\ y\_\text{uniform}(\theta\_1)$$

| Where the interferer sits | $\vert r\_\text{n}\vert$ | Consequence |
| :-- | :-- | :-- |
| On a $-13$ dB sidelobe | 0.22 | Cheap null |
| In the main lobe | $\to 1$ | Subtracting the whole beam |
| In a natural pattern null | 0 | Null already there, free |

Note:
This is the takeaway students should carry into the lab. Before computing anything, look at where the interferer falls on the pattern you already have. That level is the cost.

---

## The weights ride a circle

<div class="fig" data-inline-svg="./fig/L27-weight-phasors.svg" style="max-width:720px; margin:0 auto;"></div>

Each weight is $1$ minus a phasor of length $\vert r\_\text{n}\vert$ that rotates element to element.

Note:
Amplitudes spread between one minus r and one plus r; phases wobble either side of the ramp. When r approaches one the circle reaches the origin and the weights can cancel completely. That is the picture behind the cost curve two slides from now.

---

## Worked example — the PHASER, null at $+22.5^\circ$

Eight elements, $d = 14$ mm, HB100 at $10.525$ GHz, broadside beam.

| Quantity | Work | Result |
| :-- | :-- | :-- |
| $kd$ | $2\pi(0.491)$ | $3.085$ rad |
| $\psi\_1 = kd\sin\theta\_1$ | $3.085 \times \sin 22.5^\circ$ | $67.6^\circ$ |
| $r\_\text{n}$ | $\frac{1}{8}\sum e^{jn\psi\_1}$ | $0.225\ \angle\ 56.7^\circ$ |
| $20\log\_{10}\vert r\_\text{n}\vert$ | | $-13.0$ dB |

Note:
Point out that the minus thirteen decibels is not a coincidence: twenty-two and a half degrees is the first sidelobe of this array, which is exactly why the interferer was a problem in the first place.

---

## Worked example — the settings

$$w\_n = 1 - (0.225\ \angle\ 56.7^\circ)\ e^{-jn(67.6^\circ)}$$

$$\text{gain}\_n = \frac{100\ \vert w\_n\vert}{\max\_m \vert w\_m\vert}\ \%, \qquad \phi\_n = \angle w\_n$$

| Element | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 |
| :-- | --: | --: | --: | --: | --: | --: | --: | --: |
| Gain (%) | 75 | 65 | 82 | 100 | 100 | 82 | 65 | 75 |
| Phase (deg) | $-12.1$ | $+3.1$ | $+13.0$ | $+6.0$ | $-6.0$ | $-13.0$ | $-3.1$ | $+12.1$ |

Note:
These sixteen numbers go straight into Element Gains and Phase Control in the lab. Gains symmetric, phases antisymmetric, largest phase thirteen degrees. The changes are small, and a sign error is easy to make.

---

## The result

<div class="fig" data-inline-svg="./fig/L27-pattern-null.svg" style="max-width:740px; margin:0 auto;"></div>

Response at $+22.5^\circ$ is zero. Beam stays at broadside. The main lobe loses 2.0 dB.

Note:
Of the two decibels, four tenths come from the subtraction itself and the rest from rescaling so no element exceeds one hundred percent gain. The measured cost on the sweep is one point eight decibels.

---

<!-- .slide: class="viz-cue-slide" -->

## Watch the trade happen

- Drag the null angle: the notch follows, the beam does not move
- Watch the eight gains and phases redistribute
- The loss pill tracks $\vert r\_\text{n}\vert$, not the null angle

<p class="viz-cue">↗ Interactive on the lesson page</p>

Note:
Demo live. Start at twenty-two and a half degrees and read the pills. Then walk the null in toward the beam and let them watch the loss climb through five and eight decibels. Finish by switching to PHASER mode so they see the notch stop at the sweep floor. In the instructor build of the simulator the Interferer panel can put a real jammer at the null angle for the same demonstration.

---

## What the null costs

<div class="fig" data-inline-svg="./fig/L27-cost-vs-angle.svg" style="max-width:720px; margin:0 auto;"></div>

| Null angle | $22.5^\circ$ | $10^\circ$ | $7^\circ$ | $5^\circ$ |
| :-- | --: | --: | --: | --: |
| Loss at the look direction | 2.0 dB | 2.9 dB | 5.6 dB | 8.2 dB |

Note:
Before rescaling the look direction loses twenty log of one minus r squared. Inside the half power beamwidth the weights cancel and rescaling leaves a split beam with a hole where the target was. A null inside the beam is a resolution problem, not a null steering problem.

---

## Quantization sets a floor on depth

Each weight lands on a grid, so each carries an error $\delta w\_n$. The errors are independent, so they add in RMS at the null angle:

$$\frac{\vert y(\theta\_1)\vert}{N} \approx \frac{\epsilon\_\text{rms}}{\sqrt{N}}, \qquad \epsilon\_\text{rms} = \sqrt{\sigma\_\phi^2 + \sigma\_a^2}, \quad \sigma\_\phi = \frac{\text{LSB}}{\sqrt{12}}$$

- ADAR1000: LSB $= 2.8125^\circ$, gains in 1 % steps $\Rightarrow \epsilon\_\text{rms} = 0.0145$
- Floor $\approx -48$ dB numerically; this RMS estimate gives $-46$ dB — the same $-6B$ scale as the L26 quantization sidelobes
- A 3-bit phase shifter cannot hold a null deeper than about 22 dB

Note:
Connect it to L26 explicitly. There the quantization error raised sidelobes; here the same error fills in the null. Six decibels per bit either way.

---

## What the sweep can actually show

<div class="fig" data-inline-svg="./fig/L27-quant-depth.svg" style="max-width:600px; margin:0 auto;"></div>

<div class="callout">
Floor 23 dB below the uniform peak, nulled beam 2 dB below that: achievable notch <strong>20 to 22 dB</strong>, measured <strong>−21.6 dBc</strong>.
</div>

Note:
The weights are good to about forty-eight decibels, which is what the RMS estimate of forty-six is pointing at, and the measurement is good to twenty-one. What limits the plot is the floor, not the arithmetic. Twenty-one decibels is enough: the interferer that was three decibels below the target ends up more than ten decibels below it.

---

## How many nulls can we place?

- $N$ complex weights, one spent holding the main beam
- At most $N - 1$ independent nulls — seven on the PHASER
- Each extra null is another subtracted term and a larger system to solve
- Two interferers is the practical limit before the main lobe stops being recognizable

Note:
State it, do not derive it. The counting argument is enough at this level and the generalization is straightforward once they have the one-null case.

---

## The limitation this lesson cannot fix

- Every number came from an angle **you had to know in advance**
- If the interferer moves, the null stays where it was
- Someone must recompute and reload eight gains and eight phases

<div class="callout">
The weights are <strong>static</strong>. The array is not watching anything.
</div>

Note:
This is the hinge into L28. Ask them how the array could find the interferer angle on its own; the answer they will grope toward is that the received data already contains it.

---

## Key point

<div class="callout">
$r_\text{n}$ is the whole story: it is the uniform pattern's level at the null angle, and it tells you the main-lobe loss before you compute anything.
</div>

Note:
If they remember one thing, this is it. Look at where the interferer falls on the pattern you already have, and you know the main-lobe loss in decibels.

---

## Where this is going

- **L28 lab:** compute the table, type it into Element Gains and Phase Control, sweep, measure the notch you predicted
- **Then MVDR:** the array estimates the interference from the received data and computes its own weights — and it needs the two *digital* channels, not the analog sums
- **Module 5 capstone:** hold a track on a moving target while a jammer of unknown strength sits in the sidelobes

Read the Digital Beam Forming section of the GUI inventory before the lab.

Note:
Close by naming the hybrid architecture from L17: the analog beamformers destroy the per-element information that MVDR needs, which is why the adaptive work happens across the two digital channels.
