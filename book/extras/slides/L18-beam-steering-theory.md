<!-- .slide: class="title-slide" -->

<div class="title-left">

# ECE 444

Antennas, Phased Arrays, and Radar Systems

## Lesson 18 — Beam Steering Theory

Fall 2026 · Dr. Neil Rogers

</div>

<div class="title-right">

![USAFA](./img/01-course-intro/USAFA-logo.png)

</div>

---

## Where we were

- L15: an aperture's size sets its beamwidth, its taper sets its sidelobes.
- L16: the array factor $AF_N(\psi)$ multiplies the element pattern.
- L17: the PHASER has eight elements and a phase control for every one of them.
- **Today we work out what number to put in each of those eight boxes.**

Note:
Last lesson they turned the phase knobs and watched the beam move. Nobody said
where the numbers come from. That is the whole of today.

---

## Today's plan

1. Derive the element-to-element phase from the path difference.
2. Turn it into eight numbers, wrapped the way the hardware wants them.
3. Predict the steered pattern by shifting the array-factor argument.
4. Quantify how much the beam broadens as you scan.
5. Work the inverse problem: phases in, steer angle out.

Note:
Item five is next lesson's lab in reverse, so spend real time on it.

---

## The steering idea

A wave arriving off broadside does not hit all eight elements at once.

- The far elements are reached **later** — they sit farther from the source.
- Add the eight received signals as they are and the late ones partly cancel.
- Delay the early elements to match the late ones and all eight add in phase.

<div class="callout">
Steering is <strong>time alignment</strong>. The array points where its eight
signals arrive together.
</div>

Note:
Ask which element the wave from the right reaches first. Establish that the
array does not move, and that the only thing being changed is when each
element's signal is counted.

---

## Step 1: the geometry

<div class="fig" data-inline-svg="./fig/L18-path-difference.svg" style="max-width:1000px; margin:0 auto;"></div>

Note:
Draw this at the board while it is on the screen. Elements on a line, spacing
d, wave coming in theta-zero off broadside, wavefronts perpendicular to the
direction of travel.

---

## Step 2: the extra path

Between one element and its neighbor, the wave travels one extra leg of a right
triangle: the hypotenuse is $d$ and the angle at the element is $\theta_0$.

$$\text{extra path} = d\sin\theta_0$$

Element $n$ is $n$ steps along, so it runs $n\ d\sin\theta_0$ ahead of element 0.

Note:
The triangle is the whole derivation. Everything after this is unit
conversion.

---

## Step 3: path becomes time

Dividing by the speed of light turns that length into an arrival-time
difference:

$$\Delta t = \frac{d\sin\theta_0}{c}$$

At $\theta_0 = 30^\circ$ on the course array that is $7\ \text{mm}$ of path, or
about $23\ \text{ps}$ per element.

Note:
Twenty-three picoseconds. Say the number out loud — it is why we do not build
this with cables and switches at X-band.

---

## Step 4: time becomes phase

A sinusoid advanced by $\Delta t$ is a sinusoid advanced by $\omega\Delta t$ in
phase:

$$\Delta\phi = \omega\Delta t = \frac{2\pi f}{c}d\sin\theta_0 = kd\sin\theta_0$$

<div class="callout">
<strong>Progressive phase:</strong> $\Delta\phi = kd\sin\theta_0 = 2\pi (d/\lambda)\sin\theta_0$
</div>

Note:
This is the equation the whole module runs on. Derive it live, then box it.

---

## Read the equation

$$\Delta\phi = 2\pi\frac{d}{\lambda}\sin\theta_0$$

- Broadside ($\theta_0 = 0$) needs no phase at all.
- The phase grows with $\sin\theta_0$, not with $\theta_0$ — it flattens out near
  endfire.
- Wider spacing $d/\lambda$ means more phase per element.

Note:
The sine, not the angle. That single fact explains beam broadening later in
this lesson and grating lobes in L26.

---

## One frequency only

$\Delta t$ is a **delay**. $\Delta\phi$ is a **phase shift**, and it equals that
delay at exactly one frequency.

| | Set at | Correct at |
| :-- | :-- | :-- |
| True time delay | any frequency | all frequencies |
| Phase shift | one frequency | that frequency |

<div class="callout">
A phased array is a delay line built out of phase shifters. Change the
frequency and the beam moves.
</div>

Note:
Plant it here, do not develop it. L26 turns this into beam squint and puts a
number on it: half a gigahertz at forty-five degrees costs about three degrees.

---

## Compensation: which way?

The wave reaches high-numbered elements **early**, so we hold them back.

$$\phi_n = -n\ \Delta\phi \quad (n = 0, 1, \ldots, 7)$$

- Element 0 is the reference and gets zero.
- Each element after it is one more step behind.
- Flip the sign of $\theta_0$ and the ramp runs the other way.

Note:
Sign errors here are the single most common lab defect. The ramp compensates
the arrival difference, so it is the negative of it.

---

## The course array

Eight elements, $d = 14\ \text{mm}$, working at $10.3\ \text{GHz}$:

$$\lambda = 29.1\ \text{mm}, \quad \frac{d}{\lambda} = 0.481, \quad kd = 173.2^\circ$$

| $\theta_0$ | $\sin\theta_0$ | $\Delta\phi$ |
| :-- | :-- | :-- |
| $15^\circ$ | 0.259 | $44.8^\circ$ |
| $30^\circ$ | 0.500 | $86.6^\circ$ |
| $45^\circ$ | 0.707 | $122.5^\circ$ |
| $60^\circ$ | 0.866 | $150.0^\circ$ |

Note:
Have them check one row on a calculator. 173.2 degrees per unit of sine is
worth remembering for this hardware.

---

## Eight numbers, $\theta_0 = 30^\circ$

<div class="fig" data-inline-svg="./fig/L18-phase-ramp.svg" style="max-width:900px; margin:0 auto;"></div>

Note:
Left is the arithmetic, right is what goes into the chip. Same physics, and
the sawtooth looks nothing like a ramp — that is the point of the next slide.

---

## Wrapping

The ADAR1000 accepts $0^\circ$ to $360^\circ$. A phase of $-433^\circ$ and a phase
of $+287^\circ$ are the same setting.

| $n$ | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 |
| :-- | :-- | :-- | :-- | :-- | :-- | :-- | :-- | :-- |
| ramp | 0 | $-86.6$ | $-173.2$ | $-259.8$ | $-346.4$ | $-433.0$ | $-519.6$ | $-606.2$ |
| set | 0 | 273.4 | 186.8 | 100.2 | 13.6 | 287.0 | 200.4 | 113.8 |

<div class="callout">
Wrapping changes the number, not the beam. Nothing is lost — <em>at this
frequency</em>.
</div>

Note:
The italic caveat is the seed again. A true delay line would have kept the
extra turns.

---

<!-- .slide: class="viz-cue-slide" -->

## The ramp and the beam together

<p class="viz-cue">↗ Interactive on the lesson page</p>

- Drag the steer angle and watch eight bars and one main lobe move together.
- Toggle wrapped and unwrapped to see the sawtooth appear.
- Check the pills: $\Delta\phi$, HPBW, peak angle.

Note:
Demo live. Set thirty degrees and read the phase table off the bars against
the previous slide. Then push to sixty and let them see the lobe fatten before
we derive why.

---

## The steered pattern

Each element carries the propagation phase $kd\sin\theta$ and the ramp
$-\Delta\phi$, so the array factor argument becomes:

$$\psi = kd\sin\theta - \Delta\phi = kd\left(\sin\theta - \sin\theta_0\right)$$

$$AF_N(\psi) = \frac{\sin(N\psi/2)}{N\sin(\psi/2)}$$

The peak is wherever $\psi = 0$, which is now $\theta = \theta_0$.

Note:
Nothing about the array factor changed. We moved its zero.

---

## The shift is in sine space

<div class="fig" data-inline-svg="./fig/L18-sin-space.svg" style="max-width:860px; margin:0 auto;"></div>

Note:
Left: the lobe moved and got fatter. Right: in sine of angle it is the same
shape slid sideways. Every feature of the pattern is rigid in sine space.

---

## Where the nulls land

Nulls sit where $N\psi/2$ is a multiple of $\pi$:

$$\sin\theta_{\text{null}} = \sin\theta_0 \pm \frac{m\lambda}{Nd}$$

For the course array, $\lambda/Nd = 0.260$. Steered to $30^\circ$:

| $m$ | $\sin\theta$ | $\theta$ |
| :-- | :-- | :-- |
| $-1$ | 0.240 | $13.9^\circ$ |
| $+1$ | 0.760 | $49.5^\circ$ |
| $+2$ | 1.020 | none — outside visible space |

Note:
The nulls are not symmetric about the beam any more, and the far one has run
off the end of visible space. Both are consequences of the sine.

---

## Beam broadening

<div class="fig" data-inline-svg="./fig/L18-broadening.svg" style="max-width:720px; margin:0 auto;"></div>

Note:
From off broadside the array looks shorter. This is the same projected-aperture
argument as a tilted wall in sunlight.

---

## The broadening rule

Seen from $\theta_0$, the eight elements span only $Nd\cos\theta_0$. Put that
projected length into the L15 beamwidth rule:

$$\theta_{\text{HP}} \approx \frac{0.886\ \lambda}{Nd\cos\theta_0} = \frac{\theta_{\text{HP}}(0)}{\cos\theta_0}$$

<div class="callout">
<strong>Rule of thumb:</strong> the beam broadens as $1/\cos\theta_0$. Scan to
$60^\circ$ and it is twice as wide.
</div>

Note:
Derive it in two lines: L equals N d at broadside, L equals N d cosine
theta-zero off broadside, substitute.

---

## Broadening, in numbers

| $\theta_0$ | $\cos\theta_0$ | HPBW | Gain vs broadside |
| :-- | :-- | :-- | :-- |
| $0^\circ$ | 1.000 | $13.2^\circ$ | reference |
| $30^\circ$ | 0.866 | $15.2^\circ$ | $-0.6$ dB |
| $45^\circ$ | 0.707 | $18.7^\circ$ | $-1.5$ dB |
| $60^\circ$ | 0.500 | $26.4^\circ$ | $-3.0$ dB |

The rule reads a little narrow past about $50^\circ$; the exact $-3$ dB width at
$60^\circ$ is closer to $30^\circ$.

Note:
Peak gain falls as cosine theta-zero, from the same projected aperture. Say
where that loss lives: the array factor alone keeps its directivity as it
scans, and the element pattern is what rolls off. L22 does it properly. Three
decibels at sixty degrees is why scanned arrays are specified over a limited
field of view.

---

## Pattern at four commanded angles

<div class="fig" data-inline-svg="./fig/L18-steered-patterns.svg" style="max-width:880px; margin:0 auto;"></div>

Note:
Four sweeps of the same eight elements. Peaks land where commanded, and the
lobes widen from left to right across the plot.

---

## Worked example: $\theta_0 = 45^\circ$

| Quantity | Work | Result |
| :-- | :-- | :-- |
| $\Delta\phi$ | $173.2^\circ \times 0.707$ | $122.5^\circ$ |
| $\phi_3$ | $-3 \times 122.5^\circ$ | $-367.5^\circ \to 352.5^\circ$ |
| $\phi_7$ | $-7 \times 122.5^\circ$ | $-857.5^\circ \to 222.5^\circ$ |
| HPBW | $13.2^\circ / 0.707$ | $18.7^\circ$ |

Note:
Work phi-three at the board and let them do phi-seven. Two wraps, so 720
degrees come back.

---

## The inverse problem

The lab hands you eight phases and asks where the beam is pointing. Read the
recipe backwards.

1. Difference neighboring elements: $\phi_{n+1} - \phi_n$.
2. Unwrap — add or subtract $360^\circ$ until the steps agree.
3. That common step is $-\Delta\phi$.
4. Solve $\sin\theta_0 = \Delta\phi / kd$.

Note:
Step two is where everyone loses a sign. The differences must all be equal;
if they are not, you unwrapped wrong or the array is not uniformly steered.

---

## Inverse problem, worked

Phases read out of the hardware:

| $n$ | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 |
| :-- | :-- | :-- | :-- | :-- | :-- | :-- | :-- | :-- |
| $\phi_n$ | 0 | 59.3 | 118.5 | 177.8 | 237.0 | 296.3 | 355.6 | 54.8 |

Steps are $+59.3^\circ$ six times, then $-300.8^\circ$, which is $+59.3^\circ$ once
$360^\circ$ is restored.

$$\Delta\phi = -59.3^\circ, \quad \sin\theta_0 = \frac{-59.3^\circ}{173.2^\circ} = -0.342, \quad \theta_0 = -20.0^\circ$$

Note:
Positive ramp, negative steer angle. Make them say why: the ramp is minus n
delta-phi, so a rising ramp means a negative delta-phi.

---

## What the hardware can actually set

The ADAR1000 phase shifter has 7 bits, so its smallest step is
$360^\circ/128 = 2.8125^\circ$ — your $122.5^\circ$ becomes $123.75^\circ$.

<div class="callout">
The ideal ramp is a real number. The hardware takes a grid. L26 puts a number
on what that costs.
</div>

Note:
One sentence today. Do not start on quantization sidelobes; that is L26 with
the null-depth measurement to back it up.

---

## Key point

<div class="callout">
<strong>One equation runs the module:</strong> $\Delta\phi = kd\sin\theta_0$.
Set element <em>n</em> to $-n\Delta\phi$, wrap it into $0$ to $360^\circ$, and the
pattern shifts to $\sin\theta_0$ in sine space — broadened by $1/\cos\theta_0$.
</div>

Note:
If they leave with one thing, this is it.

---

## Where this is going

- **L19 (next):** you type these numbers into the PHASER and sweep. The phase
  table you built today is the prediction column of the lab sheet.
- **L20-L21:** beamwidth and the array factor measured against theory.
- **L26:** the three ways this ideal breaks — grating lobes, beam squint, and
  the 2.8125-degree grid.

Read the L19 lab procedure before class and bring the $\theta_0 = 30^\circ$ phase
table with you.

Note:
Tell them the lab sheet has a calculated column and a measured column, and
that the calculated column is homework they have already done.
