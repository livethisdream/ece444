<!-- .slide: class="title-slide" -->

<div class="title-left">

# ECE 444

Antennas, Phased Arrays, and Radar Systems

## Lesson 20 — Array Factor and Beamwidth Theory

Fall 2026 · Dr. Neil Rogers

</div>

<div class="title-right">

![USAFA](./img/01-course-intro/USAFA-logo.png)

</div>

---

## Where we were

- **L16** collapsed $N$ phasors into one closed form, $AF_N(\psi)$
- **L18** put the steering phase into $\psi$; **L19** steered the real array
- On the lab sweep the beam was about $13^\circ$ wide at boresight and visibly fatter at $45^\circ$
- The **Antenna Pattern Measurement** midterm project is due today — turn it in at the start of class

<div class="callout">
<strong>Today: every number on that lab plot comes out of one function of one variable.</strong>
</div>

Note:
Collect the midterm projects before starting. Remind them the quantities they pulled off a measured cut — half-power width, nulls, sidelobe level — are the quantities we compute today from theory.

---

## Today's plan

1. Half-power beamwidth, derived from the closed form
2. Every null, and the first-null beamwidth
3. Directivity of a uniform array
4. Sizing an array to a beamwidth specification
5. What Lesson 21 should measure

---

## The closed form, again

$$AF_N(\psi) = \frac{\sin(N\psi/2)}{N \sin(\psi/2)} \quad\text{with}\quad \psi = kd(\sin\theta - \sin\theta_0)$$

- All the shape is in $\psi$; the hardware enters only through the map $\theta \rightarrow \psi$
- Peak wherever $\psi = 0$, which is $\theta = \theta_0$
- Today we extract three numbers from it: beamwidth, nulls, directivity

Note:
Write the closed form at the board and leave it there for the whole hour. Everything today is a question about where this function takes a particular value.

---

## Step 1 — near the peak it is a sinc

Small $\psi$, so $\sin(\psi/2) \rightarrow \psi/2$:

$$AF_N \approx \frac{\sin(N\psi/2)}{N\psi/2} = \frac{\sin u}{u} \quad\text{with}\quad u = \frac{N\psi}{2}$$

- The same $\sin u/u$ as the uniform line source of Lesson 6
- An $N$-element uniform array is a **sampled aperture** of length $L = Nd$

Note:
Ask why a row of eight points behaves like a continuous bar. Near the peak the sampling is far finer than the phase variation across the aperture, so the pattern cannot tell the difference.

---

## Step 2 — where the sinc is at half power

$$\left\lvert \frac{\sin u}{u} \right\rvert = \frac{1}{\sqrt{2}} \quad\Longrightarrow\quad u = 1.392$$

$$\frac{N\psi}{2} = 1.392 \quad\Longrightarrow\quad kd(\sin\theta - \sin\theta_0) = \frac{2.784}{N}$$

- $1.392$ is a number you look up once and reuse forever
- Divide by $k = 2\pi/\lambda$: $\quad \sin\theta - \sin\theta_0 = 0.443\ \lambda/(Nd)$

Note:
Solve it numerically at the board if they ask — sinc of 1.392 is 0.7071. The point is that it is a fixed number, independent of the array.

---

## Step 3 — back to real angles

For a beam narrow compared with its distance from broadside:

$$\sin\theta - \sin\theta_0 \approx (\theta - \theta_0)\cos\theta_0$$

$$\theta_\text{HP} \approx \frac{0.886\ \lambda}{Nd \cos\theta_0}$$

<div class="callout">
<strong>Beamwidth is set by the aperture in wavelengths</strong>, <em>Nd/λ</em> — and by the scan angle, through the foreshortening factor cos θ₀.
</div>

Note:
This is the one equation from today that they should be able to write from memory. Derive it live; it is three lines.

---

## The 0.886 is not new

| Aperture | Beamwidth constant |
| :-- | :-- |
| Uniform line source, length $L$ (L6) | $0.886\ \lambda/L$ |
| Uniform aperture distribution (L15) | $0.886\ \lambda/L$ |
| Uniform array, $N$ elements at spacing $d$ | $0.886\ \lambda/(Nd)$ |

<div class="callout">
The constant is the same because the <strong>aperture is the same</strong> — sampled at N points instead of filled continuously.
</div>

Note:
Tapering changes the constant, not the scaling: L24 trades it up to 1.19 or 1.44 in exchange for sidelobes.

---

## The beam widens as it steers

<div class="fig" data-inline-svg="./fig/L20-scan-broadening.svg" style="max-width:760px; margin:0 auto;"></div>

Note:
Same eight elements, same spacing, three commanded angles. Point out that the pattern is periodic in sine space, which is why the lobes on the far side move too.

---

## Worked example — the PHASER array

$N = 8$, $d = 14$ mm, $f = 10.3$ GHz, so $\lambda = 29.1$ mm and $Nd = 3.85\ \lambda$

| Scan angle | Work | HPBW |
| :-- | :-- | :-- |
| $0^\circ$ | $0.886/3.85$ | $13.2^\circ$ |
| $45^\circ$ | $13.2^\circ/\cos 45^\circ$ | $18.7^\circ$ |
| $60^\circ$ | formula says $26.4^\circ$ | pattern says $30.4^\circ$ |

<div class="callout">
Past about 50° the small-angle step breaks down, always in the optimistic direction.
</div>

Note:
The 13.2 degrees is the number to carry into the lab. The 60 degree row shows where our own approximation stops working — measure it in the widget on the lesson page.

---

## Nulls: kill the numerator, keep the denominator

$$\sin(N\psi/2) = 0 \quad\Longrightarrow\quad \psi = \frac{2\pi m}{N}, \quad m = 1, 2, 3, \ldots$$

- Except $m = N, 2N, \ldots$ — there the denominator vanishes too and the ratio returns to $1$
- Those are the main lobe and the **grating lobes** (L26), not nulls
- A uniform array has at most $N-1$ nulls per period

Note:
Have them check the exception: at psi equal to two pi, both sine terms are zero and l'Hopital gives one. That is the grating lobe we spend all of L26 avoiding.

---

## Nulls in angle

$$\sin\theta = \sin\theta_0 \pm \frac{m\lambda}{Nd}$$

- Nulls are **equally spaced in $\sin\theta$**, not in $\theta$
- The arcsine crowds them near broadside and spreads them toward the horizon
- A null exists only if $\lvert\sin\theta\rvert \le 1$ — the **visible region**

Note:
Sine space is the natural coordinate for arrays; every array result is uniform there and distorted in angle. We will use it again in L26 and L27.

---

## Nulls of the course array

Tooth spacing $\lambda/Nd = 0.260$ in $\sin\theta$, broadside beam:

| $m$ | $\sin\theta$ | Null angle |
| :-- | :-- | :-- |
| 1 | $0.260$ | $15.1^\circ$ |
| 2 | $0.520$ | $31.3^\circ$ |
| 3 | $0.780$ | $51.2^\circ$ |
| 4 | $1.040$ | outside visible space |

$$\text{FNBW} = 2\arcsin(\lambda/Nd) = 30.1^\circ \approx 2.3\ \theta_\text{HP}$$

Note:
There are three nulls per side, not seven. Ask why before showing the last row — the fourth null would need a direction that does not exist.

---

## Steered, the beam is not symmetric

Steer to $\theta_0 = 30^\circ$: $\quad \sin\theta = 0.5 \pm 0.260$

| Null | $\sin\theta$ | Angle | Distance from peak |
| :-- | :-- | :-- | :-- |
| lower | $0.240$ | $13.9^\circ$ | $16.1^\circ$ |
| upper | $0.760$ | $49.4^\circ$ | $19.4^\circ$ |

<div class="callout">
FNBW = 35.5° — and the peak does <em>not</em> sit in the middle of it.
</div>

Note:
This is why we quote beamwidth as a half-power number rather than half of the null-to-null width once the beam is steered.

---

## Anatomy of a uniform-array pattern

<div class="fig" data-inline-svg="./fig/L20-beamwidth-anatomy.svg" style="max-width:760px; margin:0 auto;"></div>

Note:
Every marked number on this plot was derived in the last ten minutes. The one that was not is the sidelobe level, and that is L24.

---

<!-- .slide: class="viz-cue-slide" -->

## Try it: beamwidth, nulls, directivity

- Slide $N$ from 2 to 16 and watch the aperture, not the element count, set the width
- The solid green bar is the measured width; the dotted bar is the $0.886$ formula
- Steer to $\pm 60^\circ$ and the formula falls short of the pattern
- Push $d/\lambda$ toward $1.0$ while steered and a grating lobe walks into view

<p class="viz-cue">↗ Interactive on the lesson page</p>

Note:
Demo live: 8 elements broadside reads 13.2 degrees and 30.1 degrees, matching the table for L21. Drop to 4 and to 2 in front of them, then steer to 60 to show the formula and the pattern separating.

---

## Directivity of a uniform array

Peak intensity over its average, for isotropic elements:

$$D = \frac{N^2}{\displaystyle\sum_m \sum_n \frac{\sin(kd(m-n))}{kd(m-n)}}$$

- The diagonal terms give $N$
- The cross terms are sincs of the element separations

Note:
Do not grind the integral at the board. State that averaging the squared array factor over the sphere leaves a double sum of sincs, and go straight to the special case.

---

## The sum collapses at half-wavelength spacing

At $d = \lambda/2$, every cross term contains $\sin(\pi(m-n)) = 0$:

$$D = \frac{N^2}{N} = N = \frac{2Nd}{\lambda}$$

$$D \approx \frac{2Nd}{\lambda} = \frac{2L}{\lambda} \quad\text{for any } d < \lambda$$

- Same as the uniform line source of Lesson 15, with $L = Nd$
- Directivity grows with **aperture in wavelengths**, linearly

Note:
Half-wave spacing makes the elements' contributions orthogonal, which is the deeper reason lambda-over-two is the default. Anything closer and the elements are redundant.

---

## Numbers for the course array

| Configuration | $2Nd/\lambda$ | $D$ | dB |
| :-- | :-- | :-- | :-- |
| 8 elements | $2(8)(0.481)$ | $7.7$ | $8.9$ dB |
| Center 4 | $2(4)(0.481)$ | $3.85$ | $5.9$ dB |
| Center 2 | $2(2)(0.481)$ | $1.92$ | $2.8$ dB |

<div class="callout">
Halving the array costs exactly <strong>3 dB</strong> and doubles the beamwidth. Both come from the same aperture.
</div>

Note:
Predict this before the lab. In L21 they will turn elements off and watch the peak drop by three decibels a step.

---

## Real elements: add the decibels

$$G_\text{total}\ [\text{dBi}] = G_\text{element}\ [\text{dBi}] + D_\text{array}\ [\text{dB}]$$

- Pattern multiplication becomes addition in dB
- Eight half-wave dipoles: $2.15 + 8.9 = 11.1$ dBi
- Holds while the element pattern is flat across the main lobe

<div class="callout">
The array factor alone loses almost no directivity as it steers. The <strong>scan loss you measure comes from the element pattern</strong> — that is L22.
</div>

Note:
The linear array's main lobe is a cone about the array axis: steering thickens the cone wall by one over cosine and shrinks its circumference by cosine, so the solid angle barely changes. Real patches roll off, and that is the loss they will see at the edges of the scan volume.

---

## Sizing an array: three steps

1. **Beamwidth sets the aperture.** $Nd = 0.886\lambda/\theta_\text{HP}$, then divide by $\cos\theta_0$ at the widest scan angle
2. **Scan volume sets the spacing.** $d < \lambda/(1 + \lvert\sin\theta_0\rvert_\text{max})$ — L26
3. **Element count is what is left.** $N = Nd/d$, rounded up

<div class="callout">
Each element adds an antenna, a phase shifter, an amplifier and a control line, so <strong>$N$ sets what the array costs to build</strong>.
</div>

Note:
Steps one and two are independent: aperture sets beamwidth, spacing sets scan volume. Students routinely try to solve both with one knob.

---

## Beamwidth against aperture

<div class="fig" data-inline-svg="./fig/L20-aperture-vs-beamwidth.svg" style="max-width:700px; margin:0 auto;"></div>

Note:
A straight line on log-log, slope minus one. Ten times the aperture, one tenth the beamwidth. The dashed curve is the same array steered to 45 degrees.

---

## Worked example — 5° at X-band

Specification: $\theta_\text{HP} \le 5^\circ$ at $10$ GHz, scan to $\pm 45^\circ$. $\lambda = 30$ mm.

| Quantity | Work | Result |
| :-- | :-- | :-- |
| Aperture | $0.886(30)/0.0873$ | $305$ mm $= 10.2\ \lambda$ |
| Spacing | $d < \lambda/(1+\sin 45^\circ)$ | $d = \lambda/2 = 15$ mm |
| Elements | $305/15 = 20.3$, round up | $N = 21$ |
| Result | $0.886(30)/315$ | $4.8^\circ$, $13.2$ dB |

Note:
Round up, never down — rounding down misses the specification by construction. Half-wave spacing is comfortably inside the grating-lobe limit of 0.586 wavelengths.

---

## What the last 45° of scan costs

| At $\theta_0 = 45^\circ$ | Value |
| :-- | :-- |
| Beamwidth of the 21-element array | $6.8^\circ$ — misses the spec |
| Aperture needed to hold $5^\circ$ | $431$ mm |
| Elements at $\lambda/2$ | $N = 29$ |
| Directivity | $14.6$ dB |

<div class="callout">
The last 45° of scan volume is what added the eight extra channels. Ask for the scan volume before you fix the aperture.
</div>

Note:
Worth a minute of discussion: is the beam out at 45 degrees often enough to justify a 38 percent larger array? That question belongs to the system engineer, but the array engineer has to raise it.

---

## What Lesson 21 should measure

| Configuration | Aperture | HPBW | FNBW | First sidelobe |
| :-- | :-- | :-- | :-- | :-- |
| 8 elements | $3.85\ \lambda$ | $13.2^\circ$ | $30.1^\circ$ | $-13$ dB |
| Center 4 | $1.92\ \lambda$ | $27^\circ$ | $62^\circ$ | $-11$ dB |
| Center 2 | $0.96\ \lambda$ | $62^\circ$ | $180^\circ$ by convention | none |

- Two elements: $\lambda/Nd > 1$, so there is **no null in visible space**
- Sweep grid is $2.8125^\circ$, so measured widths land $1$ to $3^\circ$ off

Note:
Have them fill the calculated column before the lab. The two-element row is the one that catches people — the small-angle formula gives 53 degrees there and the pattern gives 62.

---

## Key point

<div class="callout">
<strong>Size sets the beam, spacing sets the scan volume, taper sets the sidelobes.</strong><br>
Aperture <em>Nd/λ</em> fixes both the half-power width and every null position. Spacing <em>d</em> decides how far you can steer before a grating lobe appears. Neither one moves the −13 dB sidelobe — only the amplitude distribution does.
</div>

Note:
There are three knobs with three nearly independent effects. If they leave with this slide they can size an array.

---

## Where this is going

- **L21 (next):** measure the table above on the PHASER — predict, measure, reconcile
- **L22:** the element pattern, which is everything the array factor left out
- **L24:** trade beamwidth for sidelobes with an amplitude taper
- **L26:** the grating-lobe criterion we quoted today, derived

<div class="callout">
Today's pattern assumed the elements are isotropic points. They are patches, and the difference is where the scan loss lives.
</div>

Note:
Read the Part 5 table and the L21 procedure before the lab. Bring calculated numbers, not blank columns.
