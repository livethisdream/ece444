<!-- .slide: class="title-slide" -->

<div class="title-left">

# ECE 444

Antennas, Phased Arrays, and Radar Systems

## Lesson 6 — Radiation Integrals

Fall 2026 · Dr. Neil Rogers

</div>

<div class="title-right">

![USAFA](./img/01-course-intro/USAFA-logo.png)

</div>

---

## Where we were

- L2: gain, directivity, pattern — all **given** to us
- L4: the **terminals** — what the radio sees
- L5: **where** the far field starts, $r \ge 2D^{2}/\lambda$

Today: stop taking the pattern as given. **Compute it** — from the current on the antenna.

Note:
Every pattern so far has been handed to us: measured, or off a datasheet. Today
is the machinery that produces it. This is the last lesson of Module 1 and the
one that makes Module 3 possible.

---

## Today's plan

1. **Why a potential** — the detour through $\mathbf{A}$
2. **The far-field approximation** — two approximations, not one
3. **The radiation vector** $\mathbf{N}(\theta,\phi)$ — where the pattern lives
4. **It's a Fourier transform** — and what that buys you
5. **Three current distributions** worth knowing cold

---

## The problem

**Given:** the current $\mathbf{J}(\mathbf{r}')$ on the antenna
**Wanted:** the field $\mathbf{E}$ far away

Attacking Maxwell directly is unpleasant — $\mathbf{E}$ and $\mathbf{H}$ are coupled and the source enters through a curl.

<div class="callout">
Standard move: invent an intermediate quantity that <strong>absorbs the source</strong>, solve for that, and differentiate at the end.
</div>

---

## The opening: $\nabla\cdot\mathbf{B} = 0$

A divergence-free field is always the curl of something. Define the **magnetic vector potential**:

$$ \mathbf{B} = \nabla\times\mathbf{A}, \qquad \mathbf{H} = \frac{1}{\mu}\nabla\times\mathbf{A} $$

Substitute, fix the gauge, and the coupled equations become **one** equation with the source on the right:

$$ \nabla^{2}\mathbf{A} + k^{2}\mathbf{A} = -\mu\mathbf{J}, \qquad k = \frac{2\pi}{\lambda} $$

Note:
Gauss's law for magnetism is always true, so A always exists. The Lorenz
condition removes the leftover freedom. What we get is the vector Helmholtz
equation — and crucially, one we already know the solution to.

---

## The radiation integral

$$ \mathbf{A}(\mathbf{r}) = \frac{\mu}{4\pi}\int_{V'} \mathbf{J}(\mathbf{r}')\ \frac{e^{-jkR}}{R}\ dV', \qquad R = |\mathbf{r}-\mathbf{r}'| $$

**Read the integrand, not the integral:**

- each piece of current launches its own spherical wave $e^{-jkR}/R$
- it arrives with amplitude $1/R$ and phase delay $kR$
- the integral just **adds them up**

<div class="callout">
Radiation is <strong>superposition with phase bookkeeping</strong>. Nothing more.
</div>

---

## The three-step recipe

$$ \mathbf{J} \quad\longrightarrow\quad \mathbf{A} \quad\longrightarrow\quad \mathbf{H} = \frac{1}{\mu}\nabla\times\mathbf{A} \quad\longrightarrow\quad \mathbf{E} = \frac{1}{j\omega\varepsilon}\nabla\times\mathbf{H} $$

- Only the **first** step involves the source
- The last two are differentiation — and in the far field they collapse into **multiplication**

Note:
Worth flagging now so nobody panics at the curls: in the far field the
r-dependence is only exp(-jkr)/r, so a curl becomes multiplication by -jk r-hat.

---

## Far field: the rays go parallel

<div class="fig" data-inline-svg="./fig/L06-radiation-integral-geometry.svg" style="max-width:790px; margin:0 auto;"></div>

Note:
Top: exact — every source point has its own R. Bottom: far field — the rays to P
are parallel, so a source point's only signature is its path difference.

---

## Two approximations, not one

Expand the exact distance for $r' \ll r$:

$$ R = r - \hat{\mathbf r}\cdot\mathbf{r}' + \frac{r'^{2} - (\hat{\mathbf r}\cdot\mathbf{r}')^{2}}{2r} + \cdots $$

| Where $R$ appears | Approximation | Why |
| :-- | :-- | :-- |
| amplitude $1/R$ | $1/R \approx 1/r$ | correction is a fraction of a percent |
| phase $e^{-jkR}$ | $R \approx r - \hat{\mathbf r}\cdot\mathbf{r}'$ | $k\hat{\mathbf r}\cdot\mathbf{r}'$ is **several radians** |

<div class="callout">
Sloppy on amplitude, careful on phase. Phase is what turns "adding" into "cancelling."
</div>

---

## The term we threw away is L5's boundary

Worst-case quadratic term, with $r'_\text{max} = D/2$:

$$ \Delta\phi = k\frac{(D/2)^{2}}{2r} = \frac{\pi D^{2}}{4\lambda r} \quad\le\quad \frac{\pi}{8} \quad(22.5^{\circ}) $$

$$ \Longrightarrow \qquad r \ \ge\ \frac{2D^{2}}{\lambda} $$

<div class="callout">
Not a coincidence. The far-field distance <em>is</em> the distance at which the parallel-ray approximation becomes honest.
</div>

Note:
L5 got this from a curved wavefront across an aperture. Here it falls out of the
term we must drop to make the integral tractable. Same number, opposite
directions — worth pausing on.

---

## The radiation vector

Pull the constant factor out of the integral:

$$ \mathbf{A}(\mathbf{r}) = \frac{\mu e^{-jkr}}{4\pi r}\underbrace{\int_{V'} \mathbf{J}(\mathbf{r}')\ e^{+jk\hat{\mathbf r}\cdot\mathbf{r}'} dV'}\_{\mathbf{N}(\theta,\phi)} $$

| Factor | Depends on | Carries |
| :-- | :-- | :-- |
| $e^{-jkr}/r$ | distance | the spherical wave — **same for every antenna ever built** |
| $\mathbf{N}(\theta,\phi)$ | direction | **everything** that makes this antenna different |

Note:
This split is the payoff of the lesson. Pattern, polarization, directivity,
sidelobes — all of it lives in N, and N is one integral over the currents.

---

## From $\mathbf{N}$ to the field

Locally a plane wave → **no radial component**. Only the transverse parts radiate:

$$ E_\theta = -j\omega\mu\frac{e^{-jkr}}{4\pi r}N_\theta, \qquad E_\phi = -j\omega\mu\frac{e^{-jkr}}{4\pi r}N_\phi, \qquad E_r \approx 0 $$

$\mathbf{H}$ comes free from the plane-wave relation — no second integral:

$$ \mathbf{H} = \frac{1}{\eta_0}\hat{\mathbf r}\times\mathbf{E}, \qquad U(\theta,\phi) = \frac{\eta_0 k^{2}}{32\pi^{2}}\left(|N_\theta|^{2} + |N_\phi|^{2}\right) $$

Note:
U is the radiation intensity from L2 — so this is where directivity and gain
actually come from.

---

## Careful: the $\sin\theta$ is a projection

For a $z$-directed current:

$$ N_\theta = -N_z\sin\theta, \qquad N_\phi = 0 $$

- The $\sin\theta$ is **not** part of the integral
- It is the projection of a $z$-directed current onto $\hat{\boldsymbol\theta}$

<div class="callout">
This is why no wire antenna radiates off its own ends: at $\theta = 0$ there is no transverse component left to project.
</div>

---

<!-- .slide: class="viz-cue-slide" -->

## The integral, as a picture

Chop the source into elements. Each contributes a phasor turned by its own path difference, $kz'\cos\theta$.

<div class="fig" data-inline-svg="./fig/L06-phasor-chain.svg" style="max-width:790px; margin:0 auto;"></div>

- Every null in every pattern in this course is a phasor chain that **closes on itself**

<p class="viz-cue">↗ Interactive on the lesson page</p>

Note:
Run the widget live. Set L = 2λ, hit "first null", and show the phasor chain
closing into a circle. Then add elements and show the sum stops changing —
that's the integral converging.

---

## It is a Fourier transform

Line source on the $z$-axis, $\hat{\mathbf r}\cdot\mathbf{r}' = z'\cos\theta$:

$$ N_z(\theta) = \int_{-L/2}^{L/2} I(z')\ e^{+jkz'\cos\theta} dz' $$

Set the **space frequency** $k_z = k\cos\theta$:

$$ N_z(k_z) = \int I(z')\ e^{+jk_z z'} dz' $$

<div class="callout">
The far-field pattern is the <strong>Fourier transform of the current distribution</strong>, read out over the visible region $-k \le k_z \le k$.
</div>

---

<!-- .slide: class="viz-cue-slide" -->

## What Fourier buys you

| Transform property | Antenna consequence | Later |
| :-- | :-- | :-- |
| stretch → squeeze | longer aperture → **narrower beam**, $\theta_\text{HP}\approx 0.886\lambda/L$ | L15, L20 |
| sharp edges → high frequencies | abrupt current cutoff → **high sidelobes**; taper buys them down | L24, L25 |
| multiply by a linear phase → shift | phase slope across the aperture → the **beam steers** | L18, L19 |
| sampling → repetition | discrete elements → **grating lobes** | L16, L26 |
| linearity | superposed currents → **pattern multiplication** | L16 |

<p class="viz-cue">↗ Interactive on the lesson page</p>

Note:
This is the slide Module 3 rests on. An array designer is choosing a function
whose transform has the beamwidth, sidelobes, and nulls they want.

---

## What a taper actually buys

Same length $L$, four ways to illuminate it:

| Current across the aperture | First sidelobe | HPBW |
| :-- | :-: | :-: |
| uniform | $-13.3$ dB | $0.886\ \lambda/L$ |
| cosine | $-23$ dB | $1.19\ \lambda/L$ |
| triangular | $-26.5$ dB | $1.27\ \lambda/L$ |
| cosine² | $-31.5$ dB | $1.44\ \lambda/L$ |

<div class="callout">
Sidelobes are set by the distribution's <strong>shape</strong>, not its size — but the taper is never free: the beam comes out <strong>1.3 to 1.6 times wider</strong> than the uniform beam of the same length.
</div>

Note:
Q6 on the practice set is exactly this table. The ranking is the thing to
remember: uniform is narrowest and worst on sidelobes, cosine-squared is widest
and best. Everything between is a Taylor or Chebyshev compromise — L15 and L25.

---

## Example 1 — the infinitesimal dipole

Current element $I_0 dl$, too short for the exponential to change across it:

$$ N_z = I_0 dl, \qquad N_\theta = -I_0 dl \sin\theta $$

$$ E_\theta = \frac{j\eta_0 k I_0 dl \sin\theta}{4\pi r}e^{-jkr} $$

<div class="callout">
Exactly L5's $1/r$ term — the one that survived $kr\gg1$. A page of exact algebra there; one line here. Pattern $\sin\theta$, $D = 1.5$ (1.76 dBi).
</div>

---

## Example 2 — the uniform line source

$I(z') = I_0$ over length $L$ → the integral is an exponential, and out falls a sinc: $N_z(\theta) = I_0 L \sin u/u$ with $u = (kL/2)\cos\theta$.

<div class="fig" data-inline-svg="./fig/L06-line-source-sinc.svg" style="max-width:760px; margin:0 auto;"></div>

Peak at **broadside**, first null at $\cos\theta = \lambda/L$, first sidelobe $-13.3$ dB **however long you build it**. That is the **space factor** — times the element factor $\sin\theta$ it gives the full pattern: **pattern multiplication**, all of L16.

Note:
Point at the dashed line on the plot. Uniform illumination always costs 13.3 dB
sidelobes, no matter how big you build it — the beam narrows with length, the
sidelobe level does not move. Only tapering changes that, which we just priced.

---

## Worked — a $2\lambda$ uniform line source

$L = 2\lambda \Rightarrow kL/2 = 2\pi$

| Quantity | Work | Result |
| :-- | :-- | :-- |
| first null | $\cos\theta = \lambda/L = 0.5$ | $60^{\circ}$ and $120^{\circ}$ |
| half power | $u = 1.392 \Rightarrow \cos\theta = 0.2215$ | $\theta = 77.2^{\circ}$ |
| HPBW | $2(90^{\circ} - 77.2^{\circ})$ | $25.6^{\circ}$ |
| rule of thumb | $0.886\lambda/L$ | $25.4^{\circ}$ ✓ |

<div class="callout">
Double $L$ → beamwidth halves to $12.7^{\circ}$; sidelobes <strong>do not move</strong>. Beamwidth is bought with <strong>size</strong>, sidelobes with <strong>taper</strong>.
</div>

---

## Example 3 — the half-wave dipole

A wire cannot carry uniform current — it has to vanish at the open ends:

$$ I(z') = I_0\sin\left[k\left(\frac{L}{2}-|z'|\right)\right] $$

Through the integral, for $L = \lambda/2$:

$$ |F(\theta)| = \left|\frac{\cos\left(\frac{\pi}{2}\cos\theta\right)}{\sin\theta}\right| $$

Not $\sin\theta$ — a **sharper** doughnut, because the current is concentrated near the middle.

---

## Three distributions, side by side

| Distribution | Pattern | HPBW | $D$ |
| :-- | :-- | :-: | :-: |
| infinitesimal dipole | $\sin\theta$ | $90^{\circ}$ | 1.50 (1.76 dBi) |
| half-wave dipole | $\cos(\frac{\pi}{2}\cos\theta)/\sin\theta$ | $78.1^{\circ}$ | 1.64 (2.15 dBi) |
| uniform line, $L=2\lambda$ | $\vert\sin u/u\vert$ | $25.6^{\circ}$ | 4.21 (6.2 dBi) |

<div class="fig" data-inline-svg="./fig/L06-three-patterns.svg" style="max-width:740px; margin:0 auto;"></div>

Note:
Same integral, three currents — change the current, change the antenna. Walk the
polar plot left to right: the two dipoles are nearly the same doughnut, and the
line source is the one that has traded its skirt for a beam and sidelobes.

---

## The catch: you have to know the current

The integral is **exact given $\mathbf{J}$**. But $\mathbf{J}$ is set by the fields, which are set by $\mathbf{J}$.

Assumptions that work:

- **thin wires** → sinusoidal standing wave (used above)
- **apertures** → assume the field in the opening (horns, reflectors — M2)
- **arrays** → each element keeps its isolated pattern (M3, until mutual coupling bites)

When they fail: solve numerically — **method of moments**, then run this same integral. That is NEC, in **L8**.

---

## Key point

<div class="callout">
Every current element sends out a spherical wave. In the far field the rays run parallel, so an element's only signature is its path difference $\hat{\mathbf r}\cdot\mathbf{r}'$. Summing them gives the radiation vector $\mathbf{N}(\theta,\phi)$ — a <strong>Fourier transform of the current distribution</strong> — and the whole pattern is a property of that transform.
</div>

---

## Where this is going

- **Module 1 is done:** pattern and gain (L2), polarization and bandwidth (L3), terminals (L4), where the far field starts (L5), and now how to compute the pattern (L6)
- **Module 2:** real currents in the integral — dipoles, loops, patches, slots, horns; L8 solves for the current numerically
- **Module 3:** run the Fourier relationship **backwards** — choose the pattern, synthesize the current

Note:
Land the arc: Module 1 built the vocabulary and the machinery. From here on
every antenna is a different J in the same integral.
