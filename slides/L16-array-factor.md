<!-- .slide: class="title-slide" -->

<div class="title-left">

# ECE 444

Antennas, Phased Arrays, and Radar Systems

## Lesson 16 — The Array Factor and Pattern Multiplication

Fall 2026 · Dr. Neil Rogers

</div>

<div class="title-right">

![USAFA](./img/01-course-intro/USAFA-logo.png)

</div>

---

## Where we were

- Lesson 6: pattern = element factor × space factor, and the space factor is the transform of the current distribution
- Lesson 15: a continuous aperture — length sets the beamwidth, taper sets the sidelobes
- Uniform aperture: $-13.3$ dB first sidelobe, HPBW $\approx 0.886\ \lambda/L$
- The PHASER has no continuous aperture. It has eight patches in a row.

**Today: cut the aperture into N elements and the sum becomes the array factor.**

Note:
Anchor on Lesson 15. Ask the class what the uniform aperture gave us: point-eight-eight-six lambda over L, and minus thirteen decibels. Both numbers come back today from a completely different starting point, which is the payoff at the end of the hour.

---

## Today's plan

1. Set up N elements on a line and derive the array factor by summing phasors
2. Set every weight to one and collapse the sum with a geometric series
3. Read the anatomy: main lobe, nulls, sidelobes
4. Multiply an element pattern by an array factor
5. Find the visible region, and the spacing where a second beam appears
6. Recover Lesson 15 by treating the array as a sampled aperture

Note:
Item one is the board derivation. Everything after it is reading the result. Tell them the derivation is testable and the closed form has to be memorized.

---

## From an aperture to elements

<div class="fig" data-inline-svg="./fig/L16-sampled-aperture.svg" style="max-width:760px; margin:0 auto;"></div>

The overall length is the same; the current now lives in N places instead of everywhere.

Note:
Draw the analogy before any algebra. A phased array is a sampled aperture. Everything we proved about apertures still applies, plus one new failure mode that sampling introduces. Ask them to guess what sampling does before we get there.

---

## The setup

<div class="fig" data-inline-svg="./fig/L16-array-geometry.svg" style="max-width:720px; margin:0 auto;"></div>

The elements are identical, the spacing is $d$, and element $n$ is fed the complex weight $a_n$.

Note:
Three assumptions, written on the board and kept there: identical elements, identically oriented, uniform spacing. Every one of them is used later. If the elements differ, pattern multiplication fails and you are back to summing element by element.

---

## The scan angle

<div class="two-col">
<div class="col-text">

**Module 3 convention**

- $\theta$ measured from **broadside**
- $-90^\circ \le \theta \le +90^\circ$
- Matches every PHASER plot and the GUI axis

**Bridge to Module 1**

$$\theta_\text{polar} = 90^\circ - \theta$$

$$\cos\theta_\text{polar} = \sin\theta$$

</div>
<div class="col-fig">

The Lesson 6 space frequency

$$k_z = k\cos\theta_\text{polar}$$

becomes

$$k\sin\theta$$

Broadside was $90^\circ$. It is now $0^\circ$.

</div>
</div>

Note:
This is the only slide in the course where both conventions are on the board at once. Make them write the mapping down. From here on, theta means scan angle from broadside, and every sine you see used to be a cosine.

---

## Step 1 — the extra path

A far-field observer sees the rays from every element as parallel.

Element $n$ sits $nd$ along the axis. Along a ray at angle $\theta$ it advances by

$$\Delta r_n = n\ d\sin\theta$$

<div class="callout">
Only the <strong>projection</strong> of the element spacing onto the look direction matters. At broadside the projection is zero and every element is the same distance away.
</div>

Note:
Do this at the board with a ruler. Drop a perpendicular from element zero onto the ray through element n. The little triangle has hypotenuse d and the side you want is d sine theta. Repeat it for element two so they see the n multiplying.

---

## Step 2 — path becomes phase

Distance turns into phase through $k = 2\pi/\lambda$:

$$\text{phase lead} = k\ \Delta r_n = n\ kd\sin\theta$$

Element $n$ therefore contributes

$$a_n\ e^{\ +jn\ kd\sin\theta}$$

Amplitudes are equal: a few centimeters of array against tens of meters of range.

Note:
Emphasize that we keep the phase difference and throw away the amplitude difference. That is the far-field approximation from Lesson 5, used here for the second time. One over R n equals one over R, but k times R n is not k times R.

---

## Step 3 — superposition

$$E(\theta) = \sum_{n=0}^{N-1} a_n\ E_0(\theta)\ \frac{e^{-jkr}}{r}\ e^{\ jn\ kd\sin\theta}$$

Identical elements, so $E_0(\theta)$ is the same for every term and pulls out:

$$E(\theta) = E_0(\theta)\ \frac{e^{-jkr}}{r} \sum_{n=0}^{N-1} a_n\ e^{\ jn\ kd\sin\theta}$$

Note:
The factoring step is where pattern multiplication is born. Point at it and say so. It works only because every element has the same E-zero of theta. Come back to this slide in twenty minutes.

---

## Step 4 — the array factor

$$AF(\theta) = \sum_{n=0}^{N-1} a_n\ e^{\ jn\ kd\sin\theta}$$

- One term per element
- Depends on **count, spacing, and weights** only
- Says nothing about what kind of antenna the elements are

<div class="callout">
Any linear array, any weights, uniform spacing: this sum is the whole story. Everything else today is a special case of it.
</div>

Note:
Have them write the general sum before we specialize. On the board, do a three-element example with weights one, two, one so they see it is just arithmetic with complex numbers.

---

## Step 5 — collect the phases

Let the weights carry a progressive phase, $a_n = \vert a_n\vert\ e^{-jn\beta}$.

Geometric phase and applied phase carry the same index, so combine them:

$$\psi = kd\sin\theta - \beta = kd\left(\sin\theta - \sin\theta_0\right)$$

with $\beta = kd\sin\theta_0$ the steering ramp — Lesson 18.

**Today $\theta_0 = 0$, so $\psi = kd\sin\theta$.**

Note:
Flag psi as the variable the rest of the module lives in. It absorbs frequency, spacing, look angle, and steering into one number. When a plot looks strange later, the first question is always what psi is doing.

---

## What the sum looks like

<div class="fig" data-inline-svg="./fig/L16-phasor-sum.svg" style="max-width:740px; margin:0 auto;"></div>

Note:
Walk the three panels. All in phase, sum equals N. Fan them out, the chain bends and the sum shortens. Fan them by exactly one N-th of a turn each and the chain closes into a polygon, so the sum is zero. That last picture is the first null, and students who see it never forget where nulls come from.

---

## Uniform excitation

Set $a_n = 1$ for every element. The sum is geometric in $e^{\ j\psi}$:

$$AF = \sum_{n=0}^{N-1} e^{\ jn\psi} = \frac{1 - e^{\ jN\psi}}{1 - e^{\ j\psi}}$$

This is the standard finite geometric series.

Note:
Remind them of the finite geometric series from calculus. Ratio is e to the j psi, N terms. If somebody asks about psi equal to zero, the ratio is one and the formula is indeterminate; we take that limit two slides from now.

---

## Closing the series

Factor half of each exponent out, top and bottom:

$$\frac{1 - e^{\ jN\psi}}{1 - e^{\ j\psi}} = \frac{e^{\ jN\psi/2}\left(e^{-jN\psi/2} - e^{\ jN\psi/2}\right)}{e^{\ j\psi/2}\left(e^{-j\psi/2} - e^{\ j\psi/2}\right)}$$

Each bracket is $-2j\sin(\cdot)$, and those factors cancel:

$$= e^{\ j(N-1)\psi/2}\ \frac{\sin(N\psi/2)}{\sin(\psi/2)}$$

Note:
This is the one algebra step worth doing slowly at the board. The trick is symmetrizing the exponent so Euler's formula appears. Then the minus two j cancels between top and bottom.

---

## The closed form

The leading exponential is the phase of the array center. Reference the phase to the center and it disappears. Divide by $N$ so the peak is one:

$$AF_N(\psi) = \frac{\sin(N\psi/2)}{N\sin(\psi/2)}$$

<div class="callout">
<strong>Memorize this line.</strong> Every lab in Module 3 predicts its measurement from it.
</div>

Note:
Say the normalization out loud: peak equals one, which is why the N sits in the denominator. Different books normalize differently and the sidelobe numbers do not change, but the peak does.

---

## Anatomy: main lobe and nulls

**Peak.** $\psi = 0$ gives zero over zero; the limit is one. So the beam points where $\sin\theta = \sin\theta_0$.

**Nulls.** Numerator zero, denominator not:

$$\psi_m = \frac{2\pi m}{N} \qquad\Longrightarrow\qquad \sin\theta_m = \sin\theta_0 + \frac{m\lambda}{Nd}$$

Nulls are set by the **total length** $Nd$, not by $d$ alone.

Note:
Take the limit at the board with L'Hopital or with the small-angle argument. Then stress the N d dependence: doubling the element count at fixed spacing halves the beamwidth, and so does doubling the spacing at fixed count, but the second one has a cost we reach in Part 5.

---

## Anatomy: sidelobes

- One sidelobe between each pair of nulls: $N-2$ per period
- Heights fall as $1/\sin(\psi/2)$, so the first is the tallest
- First peak near $N\psi/2 = 3\pi/2$:

$$AF_N \approx \frac{1}{N\sin(3\pi/2N)} \quad\longrightarrow\quad \frac{2}{3\pi} \approx -13.5\ \text{dB}$$

- Exact peak location gives $-13.3$ dB; at $N = 8$ it is $-12.8$ dB

**Call it $-13$ dB — the same number the uniform aperture gave in Lesson 15.**

Note:
This is the payoff promised at the start. A discrete uniform array and a continuous uniform aperture have the same first sidelobe, because in the many-element limit the array factor becomes the sinc. Uniform excitation leaves the first sidelobe about thirteen decibels down, whether the current is continuous or sampled.

---

## The eight-element array factor

<div class="fig" data-inline-svg="./fig/L16-af-anatomy.svg" style="max-width:770px; margin:0 auto;"></div>

Note:
Have them count the sidelobes on the plot: six, which is N minus two. Then ask why the pattern stops just short of a repeat at plus and minus ninety degrees. That question is the visible region, coming up in ten minutes.

---

## Reading the closed form

| Feature | Condition | Uniform value |
| :-- | :-- | :-- |
| Peak | $\psi = 0$ | $\theta = \theta_0$ |
| Null $m$ | $\psi = 2\pi m/N$ | $\sin\theta_m = \sin\theta_0 + m\lambda/Nd$ |
| FNBW | $m = \pm 1$ | $2\arcsin(\lambda/Nd)$ |
| HPBW | $L = Nd$ | $\approx 0.886\ \lambda/(Nd\cos\theta_0)$ |
| First sidelobe | $N\psi/2 \approx 3\pi/2$ | $-13$ dB |

Beamwidth closed forms are derived in Lesson 20.

Note:
Tell them to copy this table into their notes. It is the entire reference sheet for the next six lessons, and the lab expectation tables are built from these five rows.

---

<!-- .slide: class="viz-cue-slide" -->

## Build one yourself

<div class="fig" data-inline-svg="./fig/L16-af-builder.svg" style="max-width:760px; margin:0 auto;"></div>

<p class="viz-cue">↗ Interactive on the lesson page</p>

Note:
Demo live. Start at N equals eight and spacing point four eight one and read the pills against the table: thirteen point two degrees, first null fifteen point one, first sidelobe minus twelve point eight. Sweep N and let them see the sidelobe level refuse to move. Then push the spacing past one and stop before explaining what walked in — that sets up the visible region.

---

## Pattern multiplication

Go back to Step 3: $E_0(\theta)$ came out of the sum because the elements are identical.

$$\vert F(\theta)\vert = \vert EF(\theta)\vert \times \vert AF(\theta)\vert$$

- $EF$ = what one element does alone
- $AF$ = what the arrangement adds
- In decibels the two curves **add**

<div class="callout">
Holds for identical, identically oriented elements. Mixed element types break it.
</div>

Note:
This is the most useful theorem in array work. It also tells you what you can and cannot fix. A bad element pattern cannot be fixed with weights, and a bad array factor cannot be fixed by picking a better element.

---

## Element × array

<div class="fig" data-inline-svg="./fig/L16-pattern-multiplication.svg" style="max-width:770px; margin:0 auto;"></div>

Four collinear short dipoles, $d = \lambda/2$

Note:
Point out the two effects. The element factor pulls the outer sidelobes down hard and leaves the main lobe alone, because cosine is flat near broadside. Then ask which curve owns the beamwidth. The array does.

---

## Worked example — four short dipoles

$d = \lambda/2$, fed in phase, element pattern $EF = \cos\theta$

| Quantity | Work | Result |
| :-- | :-- | :-- |
| AF nulls | $\sin\theta_m = m/2$ | $\pm 30^\circ$, $\pm 90^\circ$ |
| AF first sidelobe | peak of $AF_4$ | $-11.3$ dB at $47.1^\circ$ |
| Element at that angle | $\cos 47.1^\circ = 0.681$ | $-3.3$ dB |
| Total sidelobe | add in dB | $-14.6$ dB |

Note:
Work the last two rows live. The element factor put three more decibels of suppression on that sidelobe, purely because the sidelobe sits well off broadside. That is why array designers care about element patterns even though the array factor gets all the attention.

---

## The visible region

$\psi$ is not free. As $\theta$ sweeps $\pm 90^\circ$:

$$kd\left(-1 - \sin\theta_0\right) \le \psi \le kd\left(+1 - \sin\theta_0\right)$$

- Window width $= 2kd = 4\pi d/\lambda$, fixed by spacing
- The window **slides** as you steer
- Outside it, $AF_N$ is mathematics, not radiation

Note:
Two motions to keep separate. Changing the spacing changes the width of the window. Changing the steer angle slides the window without resizing it. Students who confuse the two get grating-lobe problems wrong every time.

---

## One window, two spacings

<div class="fig" data-inline-svg="./fig/L16-visible-region.svg" style="max-width:730px; margin:0 auto;"></div>

Note:
Top panel is the PHASER: the window stops just short of the repeat. Bottom panel is one-wavelength spacing, where the repeat sits exactly at the edge of view. Ask what happens between those two cases and then at one point five wavelengths.

---

## Grating lobes

$AF_N$ has period $2\pi$. A window wider than one period admits a **full-height** copy of the main lobe:

$$\sin\theta_g = \sin\theta_0 \pm \frac{m\lambda}{d}$$

<div class="callout">
Avoidance criterion: <strong>d &lt; &lambda; / (1 + |sin &theta;<sub>0</sub>|)</strong> &nbsp;&mdash;&nbsp; broadside only: d &lt; &lambda;. To scan to &plusmn;90&deg;: d &lt; &lambda;/2.
</div>

Full treatment — with beam squint and quantization — in Lesson 26.

Note:
Say plainly what a grating lobe costs: the array transmits or receives just as strongly in a direction you did not ask for. In radar that is a false target bearing. In a comm link it is an interference path. This is why half-wavelength spacing is the default everywhere.

---

## The array is a sampled aperture

| Parameter | What it controls |
| :-- | :-- |
| Total length $Nd$ | beamwidth, $\approx 0.886\ \lambda/Nd$ |
| Excitation shape | sidelobe level, $-13$ dB uniform |
| Spacing $d$ | what repeats — the grating lobe |

Sampling periodizes the pattern. A continuous aperture has no grating lobes because it is not sampled.

Note:
Close the loop opened in slide four. Two arrays with the same total length have the same beam whether it is eight elements or thirty-two. The element count gives you grating-lobe headroom and steering range, not beamwidth.

---

## Worked example — the course array

8 patches, $d = 14$ mm, $f = 10.3$ GHz, $\lambda = 29.1$ mm, $d/\lambda = 0.481$

| Quantity | Work | Result |
| :-- | :-- | :-- |
| Visible region | $\psi = \pm kd$ | $\pm 173.2^\circ$ — no repeat |
| Nulls | $\sin\theta_m = m/3.85$ | $15.1^\circ$, $31.3^\circ$, $51.2^\circ$ |
| FNBW | $2\arcsin(1/3.85)$ | $30.1^\circ$ |
| HPBW | $0.886\ \lambda/Nd$ | $13.2^\circ$ |
| First sidelobe | $N = 8$ | $-12.8$ dB at $21.9^\circ$ |

Note:
These five numbers are the Lesson 21 expectation table. Tell them now that the measured sweep will read thirteen point one degrees for the beamwidth and eleven to thirteen decibels for the sidelobes, and that the difference is the sweep grid and the noise floor, not bad theory.

---

## Key point

<div class="callout">
<strong>The array factor is one sum, uniform weights collapse it to one closed form, and the element pattern multiplies it.</strong><br>
Add the element phasors to get <em>AF</em>. Uniform weights collapse it to sin(N&psi;/2) over N sin(&psi;/2). Multiply by the element pattern for the real thing. Length sets the beam, weights set the sidelobes, spacing sets what repeats.
</div>

Note:
If they leave with one slide, this is it. Have them state the three sentences back before the bell.

---

## Where this is going

- **Lesson 17** — the hardware that produces $a_n$: ADAR1000 beamformers, per-element gain and phase, the receive chain
- **Lesson 18** — set the progressive ramp $\beta$ and steer the beam to $\theta_0$
- **Lesson 20** — beamwidth closed forms, and $D \approx 2Nd/\lambda$
- **Lessons 21, 25, 28** — measure this pattern, taper it, notch it

**Before next lesson:** be able to write $AF_N$ from memory and locate its nulls.

Note:
Every lab in this module measures some feature of today's array factor. The theory is finished before the hardware arrives, which is deliberate: predict first, measure second, reconcile third.
