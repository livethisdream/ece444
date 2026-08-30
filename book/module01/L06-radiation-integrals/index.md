---
frame_view: true
---

# L6 - Radiation Integrals

::::{frame}
:class: title-frame

<div class="course-mark">ECE 444 · Fall 2026</div>

<h1 class="frame-title">Radiation Integrals</h1>

<div class="title-rule"></div>

Lesson 5 told you *where* the far field is. This lesson tells you *what it is*.

Lesson 6 · Antennas, Phased Arrays, and Radar Systems · Dr. Neil Rogers
::::

::::{frame} Slides
:::{admonition} Slides
:class: slides
<a href="../../slides/L06-radiation-integrals.html" target="_blank" rel="noopener">html slides</a>
<a href="../../slides/L06-radiation-integrals.html?print-pdf" target="_blank" rel="noopener">pdf slides</a>
<a href="../../slides/L06-radiation-integrals.md" target="_blank" rel="noopener">raw markdown slides</a>
:::
::::

::::{frame} Learning Objectives

<ol class="lo-list lo-sublist" style="--module: '1'; --lo: '6'">
  <li>I can explain why we find the radiated field through the magnetic vector potential rather than by solving for E directly, and state the three-step recipe from current to far field.</li>
  <li>I can apply the far-field approximations to the exact integral — one for amplitude, a different one for phase — and show that the leftover phase error is exactly the far-field distance criterion from Lesson 5.</li>
  <li>I can set up and evaluate the radiation integral for a given current distribution, and turn the resulting radiation vector into the far-field pattern.</li>
  <li>I can recognize the current distribution and the far-field pattern as a Fourier transform pair, and predict how a change in the current changes the pattern.</li>
</ol>
::::

::::{frame} Now we compute the pattern

Lesson 5 told you *where* the far field is. This lesson tells you *what it is*.
Everything up to now has taken the radiation pattern as a given — something you
measure, or read off a datasheet. Now we compute it. The input is the **current
distribution** on the antenna; the output is the **far-field pattern**; and the
machinery in between is a single integral.

That integral is the last piece of Module 1, and it is the piece that makes the
rest of the course possible. Every array in Module 3 — steered, tapered,
thinned, nulled — is this integral with a different current in it.
::::

::::{frame} The problem

We want $\mathbf{E}$ far away, given a known current density $\mathbf{J}$ on the
antenna. Attacking Maxwell's equations directly is unpleasant: $\mathbf{E}$ and
$\mathbf{H}$ are coupled, and the source enters through a curl. The standard
move is to introduce an intermediate quantity that absorbs the source, solve for
*that*, and differentiate at the end.
::::

::::{frame} The opening: ∇·B = 0

The opening is Gauss's law for magnetism. Because

$$
\nabla \cdot \mathbf{B} = 0
$$

*always*, and because the divergence of any curl vanishes, you can
always write $\mathbf{B}$ as the curl of some vector field. Define the **magnetic vector
potential** $\mathbf{A}$ by

$$
\mathbf{B} = \nabla \times \mathbf{A}, \qquad \mathbf{H} = \frac{1}{\mu}\nabla \times \mathbf{A}.
$$
::::

::::{frame} One equation, source on the right

Substituting this into the remaining Maxwell equations and fixing the leftover
freedom in $\mathbf{A}$ with the Lorenz condition turns two coupled first-order
equations into one **vector Helmholtz equation** with the current sitting on the
right-hand side:

$$
\nabla^2 \mathbf{A} + k^2\mathbf{A} = -\mu \mathbf{J}, \qquad k = \frac{2\pi}{\lambda}.
$$
::::

::::{frame} The radiation integral

That equation has a known solution — and this is the whole reason for the detour:

$$
\boxed{
\mathbf{A}(\mathbf{r}) = \frac{\mu}{4\pi}\int_{V'}
\mathbf{J}(\mathbf{r}')\ \frac{e^{-jkR}}{R}\ dV',
\qquad R = \vert\mathbf{r} - \mathbf{r}'\vert }
$$

**Read the integrand, not the integral.** Each little piece of current
$\mathbf{J}(\mathbf{r}')\ dV'$ launches its own outgoing spherical wave,
$e^{-jkR}/R$, and that wave arrives at the observation point with an amplitude
set by $1/R$ and a phase delay set by $kR$. The integral is nothing more
profound than **adding up those contributions** — superposition, with the
bookkeeping done in phase. A definite integral over something we can
write down has replaced the unknown field.

:::{depth}
```{note}
There is a **second** radiation integral. Antennas that radiate through an
opening rather than off a wire — slots, horns, reflector feeds — are handled by
replacing the aperture with an equivalent **magnetic** current $\mathbf{M}$,
which produces an electric vector potential $\mathbf{F}$ through an integral of
exactly the same form. Balanis writes the pair as $\mathbf{N}$ (from
$\mathbf{J}$) and $\mathbf{L}$ (from $\mathbf{M}$). We will need $\mathbf{L}$ in
Module 2 for slots and horns; everything in this lesson carries over by duality.
```
:::
::::

::::{frame} The three-step recipe
:::{callout}
$$
\mathbf{J}
\ \xrightarrow[\text{(the integral)}]{}\
\mathbf{A}
\ \xrightarrow[\ \mathbf{H} = \frac{1}{\mu}\nabla\times\mathbf{A}\ ]{}\
\mathbf{H}
\ \xrightarrow[\ \mathbf{E} = \frac{1}{j\omega\varepsilon}\nabla\times\mathbf{H}\ ]{}\
\mathbf{E}
$$

Only the first step involves the source. The last two are differentiation — and
in the far field, as we are about to see, they collapse into multiplication.
:::
::::

::::{frame} Far field: the rays go parallel

The exact integral is correct everywhere — near field included — but it is
awkward, because $R$ changes as you move around the source. In the far field it
simplifies dramatically, and the way it simplifies is worth being careful about:
**amplitude and phase get different approximations.**

<img src="../../viz/img/L06-radiation-integral-geometry.svg" alt="Exact geometry with the vector R from a source point to the field point, and the far-field limit in which the rays are parallel and only the path difference r-hat dot r-prime survives" style="max-width: 700px; width: 100%; display: block; margin: 1em auto;">
::::

::::{frame} Expanding the exact distance

Start with the exact distance and expand it for $r' \ll r$:

$$
R = |\mathbf{r} - \mathbf{r}'|
  = r\sqrt{1 - \frac{2\ \hat{\mathbf r}\cdot\mathbf{r}'}{r} + \frac{r'^2}{r^2}}
  = r - \hat{\mathbf r}\cdot\mathbf{r}'
    + \frac{r'^2 - (\hat{\mathbf r}\cdot\mathbf{r}')^2}{2r} + \cdots
$$

Now treat the two places $R$ appears differently.
::::

::::{frame} Two approximations, not one

**Amplitude.** In the $1/R$ factor, the correction $\hat{\mathbf r}\cdot\mathbf{r}'$
is a *fractional* change of order $r'/r$. At any useful distance that is a
fraction of a percent, and nobody can measure it. So

$$
\frac{1}{R} \approx \frac{1}{r}.
$$
::::

::::{frame} The entire content of far field

**Phase.** In $e^{-jkR}$ the same correction is multiplied by $k$, and what
matters is whether $k\ \hat{\mathbf r}\cdot\mathbf{r}'$ is comparable to a
radian. For a source a few wavelengths across it is *several* radians — it
flips contributions from adding to cancelling. Dropping it would destroy the
pattern. So we keep the linear term and only discard the quadratic one:

$$
R \approx r - \hat{\mathbf r}\cdot\mathbf{r}'.
$$

This is the entire content of "far field": **the rays from every part of the
antenna to the observation point are parallel**, so the only thing that
distinguishes one source point from another is a *path difference*
$\hat{\mathbf r}\cdot\mathbf{r}'$ — the projection of its position onto the
viewing direction.
::::

::::{frame} The term we threw away is L5's boundary

The term we threw away is the quadratic one. Its worst case is
$r'_{\max}{}^2/2r$, and for an antenna of largest dimension $D$ the source
extends to $r'_{\max} = D/2$, so the leftover **phase error** is at most

$$
\Delta\phi = k\ \frac{(D/2)^2}{2r} = \frac{2\pi}{\lambda}\cdot\frac{D^2}{8r}
           = \frac{\pi D^2}{4\lambda r}.
$$

Demand that this stay under $\pi/8$ radians — the $22.5^{\circ}$ tolerance from
Lesson 5 — and it rearranges to

$$
r \ge \frac{2D^2}{\lambda}.
$$
::::

::::{frame} Not a coincidence, not a second criterion

That is not a coincidence and not a second criterion. **The far-field distance
is precisely the distance at which the parallel-ray approximation becomes
honest.** Lesson 5 derived it from the geometry of a curved wavefront; here it
falls out of the term we need to drop to make the integral tractable. Same
number, same physics, arrived at from opposite directions.
::::

::::{frame} The radiation vector

Put the two approximations back into the integral. The $e^{-jkr}/r$ factor no
longer depends on $\mathbf{r}'$, so it comes straight out:

$$
\mathbf{A}(\mathbf{r}) = \frac{\mu e^{-jkr}}{4\pi r}
\underbrace{\int_{V'}\mathbf{J}(\mathbf{r}')\ e^{+jk\hat{\mathbf r}\cdot\mathbf{r}'}\ dV'}_{\textstyle \mathbf{N}(\theta,\phi)}
$$

The integral that is left is the **radiation vector** $\mathbf{N}(\theta,\phi)$.
This split is the payoff of the whole lesson:
::::

::::{frame} What each factor carries

| Factor | Depends on | What it carries |
| :-- | :-- | :-- |
| $e^{-jkr}/r$ | distance only | the outgoing spherical wave — *identical for every antenna ever built* |
| $\mathbf{N}(\theta,\phi)$ | direction only | everything that makes **this** antenna different from any other |

An antenna's pattern, its polarization, its directivity, its sidelobes — all of
it lives in $\mathbf{N}$, and $\mathbf{N}$ is a single integral over the
currents. Note also what became of the recipe's second and third steps: with the
$\mathbf{r}$-dependence reduced to $e^{-jkr}/r$, taking a curl in the far field
just multiplies by $-jk\hat{\mathbf r}$. Differentiation has collapsed into
multiplication, exactly as promised.
::::

::::{frame} From the radiation vector to the field

In the far field the wave is locally a plane wave travelling radially outward
(Lesson 5), so it can have **no radial field component**. Only the transverse
parts of $\mathbf{A}$ survive, and they map straight onto $\mathbf{E}$:

$$
E_\theta = -j\omega\mu\ \frac{e^{-jkr}}{4\pi r}\ N_\theta,
\qquad
E_\phi   = -j\omega\mu\ \frac{e^{-jkr}}{4\pi r}\ N_\phi,
\qquad
E_r \approx 0.
$$
::::

::::{frame} The magnetic field and intensity

The magnetic field follows for free from the plane-wave relation, with no new
integral:

$$
\mathbf{H} = \frac{1}{\eta_0}\ \hat{\mathbf r}\times\mathbf{E},
\qquad \eta_0 \approx 377\ \Omega .
$$

Then radiation intensity — the quantity Lesson 2 built directivity and gain on —
is

$$
U(\theta,\phi) = \frac{r^2|\mathbf{E}|^2}{2\eta_0}
= \frac{\eta_0 k^2}{32\pi^2}\Big(|N_\theta|^2 + |N_\phi|^2\Big),
$$

The normalized power pattern is $U/U_{\max}$; its square root is the
**field pattern** $|F(\theta,\phi)|$ used for the rest of this lesson.
::::

::::{frame} Careful: the sin θ factor is a projection

```{note}
Watch the components. The integral naturally produces $\mathbf{N}$ in Cartesian
components, but only the **spherical** transverse components radiate. For the
$z$-directed currents that dominate this lesson,

$$
N_\theta = -N_z\sin\theta, \qquad N_\phi = 0,
$$

so that $\sin\theta$ is not part of the integral at all — it is the projection
of a $z$-directed current onto $\hat{\boldsymbol\theta}$. It is also the reason
no wire antenna radiates off its own ends: at $\theta = 0$ the current has no
transverse component to project.
```
::::

::::{frame} The radiation integral as a coherent phasor sum
:class: viz-frame

:::{depth}
Before evaluating anything, get a feel for what the integral *does*. The source
below is chopped into elements; each one contributes a phasor whose angle is
$k z' \cos\theta$ — its path difference in radians. At broadside every phasor
points the same way and they stack into a long straight chain. Swing off
broadside and the chain curls up; when it closes on itself, you are looking at a
null.
:::

<iframe src="../../viz/radiation-integral.html"
        width="100%" height="440"
        style="border: 1px solid #cddce9; border-radius: 6px;"
        loading="lazy"
        title="The radiation integral as a coherent phasor sum">
</iframe>
::::

::::{frame} The radiation integral is a Fourier transform

Specialize to a **line source** on the $z$-axis carrying current $I(z')$. Then
$\hat{\mathbf r}\cdot\mathbf{r}' = z'\cos\theta$ and the whole radiation vector
is one scalar integral:

$$
N_z(\theta) = \int_{-L/2}^{L/2} I(z')\ e^{+jkz'\cos\theta}\ dz'.
$$

Now define the **space frequency** $k_z = k\cos\theta$ and look again:

$$
N_z(k_z) = \int I(z')\ e^{+jk_z z'}\ dz' .
$$

That is a Fourier transform. **The far-field pattern is the Fourier transform of
the current distribution**, evaluated over the *visible region*
$-k \le k_z \le +k$ and then bent onto angle by $k_z = k\cos\theta$.
::::

::::{frame} Part of the transform is invisible

That restriction is worth a second look. The transform $N_z(k_z)$ exists for
every real $k_z$, but only $|k_z| \le k$ corresponds to a real direction, because
$k_z = k\cos\theta$ and $\cos\theta$ can only run from $-1$ to $+1$. **Part of the
transform is invisible** — it describes stored, non-radiating field near the
aperture rather than anything you can measure at range, so the pattern is a
window onto the transform, not the whole of it.
::::

::::{frame} Grating lobes

Keep that window in mind, because it does not stay closed. When Module 3 samples
a continuous aperture into a discrete array, the transform *repeats* at intervals
of $2\pi/d$, and if the element spacing $d$ is large enough one of those repeats
slides inside $|k_z| \le k$. Energy that was safely invisible becomes a second
beam you did not ask for — a **grating lobe**, and the reason Lesson 16 spends so
much effort on element spacing.
::::

::::{frame} What Fourier buys you

Everything a Fourier transform does, an antenna does:

| Fourier property | Antenna consequence | Where you will use it |
| :-- | :-- | :-- |
| Stretch the function → squeeze its transform | Longer aperture → **narrower beam**: $\theta_\text{HP} \approx 0.886\ \lambda/L$ | L15, L20 |
| Sharp edges → high-frequency content | Abrupt current cutoff → **high sidelobes** ($-13.3$ dB for uniform); smooth taper buys them down | L15, L24, L25 |
| Multiply by $e^{-j\alpha z'}$ → shift the transform | Linear phase across the aperture → the **beam steers** | L18, L19, L26 |
::::

::::{frame} What Fourier buys you — sampling and linearity

| Fourier property | Antenna consequence | Where you will use it |
| :-- | :-- | :-- |
| Sample a function → its transform repeats | Discrete elements instead of a continuous line → **grating lobes** | L16, L26 |
| Transform is linear | Superposing currents superposes patterns → **pattern multiplication** | L16 |
::::

::::{frame} Choosing a function, not solving Maxwell's equations

This is why Module 3 works the way it does. An array designer is not really
solving Maxwell's equations — they are choosing a function whose Fourier
transform has the beamwidth, sidelobe level, and null placement they want, then
building a current distribution that realizes it.
::::

::::{frame} Line-source current distribution and its far-field pattern
:class: viz-frame

Choose a distribution, stretch it, taper it, put a linear phase slope across it,
and watch the pattern respond. Three habits worth building here: **length sets
beamwidth**, **taper sets sidelobes**, **phase slope sets pointing direction**.

<iframe src="../../viz/line-source-pattern.html"
        width="100%" height="630"
        style="border: 1px solid #cddce9; border-radius: 6px;"
        loading="lazy"
        title="Line-source current distribution and its far-field pattern">
</iframe>
::::

::::{frame} The infinitesimal dipole — recovering Lesson 5

A current element $I_0\ dl$ at the origin, pointing along $\hat{\mathbf z}$. It
is so short that $e^{+jkz'\cos\theta} \approx 1$ across it, so the integral is
trivial:

$$
N_z = I_0\ dl, \qquad N_\theta = -I_0\ dl\ \sin\theta .
$$

$$
E_\theta = \frac{j\ \eta_0 k I_0\ dl\ \sin\theta}{4\pi r}\ e^{-jkr}
$$

This is exactly the $1/r$ radiation term of the exact short-dipole field quoted
in Lesson 5 — the term that survived once $kr \gg 1$. What took a page of exact
spherical-wave algebra there comes out here in one line. The pattern is
$|F| = \sin\theta$: a doughnut, maximum broadside, null along the wire, and
$D = 1.5$ (1.76 dBi).
::::

::::{frame} Worked example — the doughnut integrated
:::{admonition} Worked example — the doughnut integrated
:class: tip

That $D = 1.5$ has been quoted since Lesson 2 and taken on faith ever since.
Now you can earn it. Directivity is peak intensity over average intensity, and
with the pattern in hand both are just integrals. Normalize the intensity to its
peak, $U = \sin^2\theta$ (intensity goes as the *square* of the field pattern),
and integrate over the whole sphere:

$$
P_\text{rad} = \oint U\ d\Omega
= \int_0^{2\pi}\!\!\int_0^{\pi} \sin^2\theta\ \cdot\ \sin\theta\ d\theta\ d\phi
= 2\pi \int_0^{\pi} \sin^3\theta\ d\theta
= 2\pi \cdot \frac{4}{3}
= \frac{8\pi}{3}.
$$
:::
::::

::::{frame} Worked example — the doughnut integrated (cont.)
:::{admonition} Worked example — the doughnut integrated (cont.)
:class: tip

The extra $\sin\theta$ is the solid-angle element $d\Omega = \sin\theta\ d\theta\ d\phi$,
not part of the pattern — a bookkeeping trap worth naming. Then

$$
D = \frac{4\pi\ U_{\max}}{P_\text{rad}} = \frac{4\pi}{8\pi/3} = 1.5
\quad (1.76\ \text{dBi}).
$$

The number is small because the doughnut is generous: a current element throws
power almost everywhere except along its own axis, so concentrating it 1.5 times
over isotropic is all the shape can do.
:::
::::

::::{frame} The uniform line source — the sinc

Now let the current be constant, $I(z') = I_0$, over a length $L$. The integral
is an exponential:

$$
N_z(\theta) = I_0\int_{-L/2}^{L/2} e^{+jkz'\cos\theta}\ dz'
            = I_0 L\ \frac{\sin\!\left(\tfrac{kL}{2}\cos\theta\right)}
                          {\tfrac{kL}{2}\cos\theta}
$$

so with $u = \tfrac{kL}{2}\cos\theta$ the integral has collapsed to the classic

$$
S(\theta) = \left|\frac{\sin u}{u}\right| .
$$
::::

::::{frame} The space factor and pattern multiplication

```{note}
$S(\theta)$ is the **space factor** — the contribution of the *distribution*
alone. The radiated pattern still needs the projection from Part 3:

$$
|F(\theta)| \propto \underbrace{\sin\theta}_{\text{element factor}}\ \cdot\
\underbrace{S(\theta)}_{\text{space factor}} .
$$

For a beam near broadside the $\sin\theta$ is essentially 1 and changes nothing
you would notice ($25.6^{\circ}$ becomes $24.8^{\circ}$ for the example below).
Near endfire it matters a great deal. This factorization — element pattern times
distribution — is **pattern multiplication**, and Lesson 16 builds all of array
theory on it.
```
::::

::::{frame} The uniform line source pattern

Plotted against angle, that one expression is the shape you measure every
aperture antenna in this course against:

<img src="../../viz/img/L06-line-source-sinc.svg" alt="Space factor of a uniform line source plotted in dB against angle: a main beam at broadside, nulls where cos theta is a multiple of lambda over L, and a first sidelobe 13.3 dB below the peak marked by a dashed line" style="max-width: 700px; width: 100%; display: block; margin: 1em auto;">
::::

::::{frame} The space factor's three headline numbers

Read off the space factor's three headline numbers:

- **Peak** at $u = 0$, i.e. $\theta = 90^{\circ}$ — **broadside**. All elements are
  equidistant from the observer, every phasor is aligned, and the sum is the
  full length $L$.
- **First null** where $u = \pi$, i.e. $\cos\theta_\text{null} = \lambda/L$.
- **First sidelobe** at $u \approx 4.493$, height $-13.3$ dB — a fixed number,
  independent of $L$. Uniform illumination *always* costs you $13.3$ dB
  sidelobes; only tapering changes that.
::::

::::{frame} Worked example — a 2λ uniform line source
:::{admonition} Worked example — a $2\lambda$ uniform line source
:class: tip

Take $L = 2\lambda$, so $kL/2 = 2\pi$.

**First null.** $\cos\theta_\text{null} = \lambda/L = 0.5 \Rightarrow
\theta_\text{null} = 60^{\circ}$ and $120^{\circ}$. Null-to-null beamwidth
$= 60^{\circ}$.

**Half-power beamwidth.** $|\sin u / u| = 0.707$ at $u = 1.392$, so

$$
\cos\theta_\text{HP} = \frac{1.392}{2\pi} = 0.2215
\quad\Rightarrow\quad \theta_\text{HP} = 77.2^{\circ},
$$
:::
::::

::::{frame} Worked example — a 2λ uniform line source (cont.)
:::{admonition} Worked example — a $2\lambda$ uniform line source (cont.)
:class: tip

and by symmetry about broadside the beamwidth is
$2(90^{\circ} - 77.2^{\circ}) = 25.6^{\circ}$. Compare the rule of thumb
$0.886\ \lambda/L = 0.443\ \text{rad} = 25.4^{\circ}$ — within a fifth of a
degree, which is why that rule of thumb is worth memorizing.

**Sidelobes.** $-13.3$ dB, whatever $L$ is.

Double the length to $4\lambda$ and the beamwidth halves to $12.7^{\circ}$,
while the sidelobes do not move at all. Beamwidth is bought with **size**;
sidelobes are bought with **taper**.
:::
::::

::::{frame} What a taper buys — and what it costs

Since the transform's high-frequency content comes from the *edges* of the
distribution, softening the edges must soften the sidelobes. It does, and the
prices are known. Same length $L$, four ways to illuminate it:

| Distribution | First sidelobe | HPBW constant ($\times\ \lambda/L$) |
| :-- | :-: | :-: |
| Uniform | $-13.3$ dB | 0.886 |
| Cosine | $-23$ dB | 1.19 |
| Triangular | $-26.5$ dB | 1.27 |
| Cosine² | $-31.5$ dB | 1.44 |
::::

::::{frame} You buy sidelobe suppression with beamwidth

Read the second column as the cost. Relative to uniform, a taper broadens the
main beam by a factor of **1.34 to 1.63** — you buy every dB of sidelobe
suppression with beamwidth, and there is no distribution that gives you both.
The ranking is the thing to carry forward: uniform is narrowest and worst on
sidelobes, cosine² is widest and best, and everything useful in between is a
Taylor or Chebyshev compromise. This table is a preview — **Lesson 15** derives
it for apertures and **Lesson 24** turns it into a design procedure for arrays.
::::

::::{frame} The half-wave dipole — a real antenna

A thin wire cannot carry uniform current: the current has to vanish at the open
ends. The standing wave on a resonant wire of length $L$ is well approximated by

$$
I(z') = I_0 \sin\!\left[k\left(\frac{L}{2} - |z'|\right)\right],
$$

which for $L = \lambda/2$ is a single cosine hump — maximum at the feed, zero at
both tips. Putting that into the radiation integral gives a standard (if
tedious) result:

$$
N_z(\theta) = \frac{2I_0}{k}\
\frac{\cos\!\left(\tfrac{\pi}{2}\cos\theta\right)}{\sin^2\theta},
\qquad
N_\theta = -N_z\sin\theta ,
$$
::::

::::{frame} A sharper doughnut

and therefore

$$
E_\theta = \frac{j\eta_0 I_0 e^{-jkr}}{2\pi r}\
\left[\frac{\cos\!\left(\tfrac{\pi}{2}\cos\theta\right)}{\sin\theta}\right],
\qquad
|F(\theta)| = \left|\frac{\cos\!\left(\tfrac{\pi}{2}\cos\theta\right)}{\sin\theta}\right| .
$$

The bracket is *not* $\sin\theta$, but it is close: it is a slightly **sharper**
doughnut, because the tapered current is concentrated near the middle rather
than spread over the whole length. That small difference is worth real numbers —
$\theta_\text{HP} = 78.1^{\circ}$ versus $90^{\circ}$, and $D = 1.64$
(2.15 dBi) versus 1.5 (1.76 dBi).
::::

::::{frame} Three distributions, side by side

| Distribution | Pattern $\vert F(\theta)\vert$ | HPBW | $D$ |
| :-- | :-- | :-: | :-: |
| Infinitesimal dipole | $\sin\theta$ | $90^{\circ}$ | 1.50 (1.76 dBi) |
| Half-wave dipole | $\cos\!\left(\tfrac{\pi}{2}\cos\theta\right)/\sin\theta$ | $78.1^{\circ}$ | 1.64 (2.15 dBi) |
| Uniform line source, $L = 2\lambda$ | $\vert\sin u/u\vert$, with $u = \tfrac{kL}{2}\cos\theta$ | $25.6^{\circ}$ | 4.21 (6.2 dBi) *(space factor only; 4.45 / 6.5 dBi with the element factor)* |
::::

::::{frame} Walking the polar plot left to right

<img src="../../viz/img/L06-three-patterns.svg" alt="Polar patterns in dB for the three distributions side by side: the infinitesimal dipole and half-wave dipole as nearly identical doughnuts, and the two-wavelength uniform line source as a narrow broadside beam with sidelobes" style="max-width: 700px; width: 100%; display: block; margin: 1em auto;">

Walk the polar plot left to right and the trade is visible: the two dipoles are
nearly the same doughnut, and the line source has traded its skirt for a beam
and a set of sidelobes.
::::

::::{frame} Correcting for the element factor

The last row's headline number is the space factor on its own; multiply in the
$\sin\theta$ element factor and it becomes $24.8^{\circ}$ and $D = 4.45$
(6.5 dBi) — a small correction, as promised for a broadside beam. Either way the comparison holds: a
$2\lambda$ line source is four times longer than a half-wave dipole, and it buys
about 2.6 times the directivity with a beam three times narrower. For a long
uniform line source $D \to 2L/\lambda$ — directivity sold by the wavelength.
::::

::::{frame} The catch — you have to know the current

The radiation integral is exact given $\mathbf{J}$. The difficulty is that
$\mathbf{J}$ is not given: the fields set the current on a
conductor, and the current sets the fields. Solving that self-consistently is the
genuinely hard part of antenna analysis, and the radiation integral does not
touch it.

What saves us is that for many antennas the current can be **assumed** with good
accuracy:

- **Thin wires** — the sinusoidal standing wave used above. Excellent for
  $\ell/\text{diameter} \gtrsim 100$, and it is why hand analysis of dipoles
  works so well.
- **Apertures** — assume the field in the opening (often the incident waveguide
  mode) and integrate that instead. This is the standard treatment of horns and
  reflectors in Module 2.
- **Arrays** — assume each element keeps its isolated pattern and only the
  excitation changes. That assumption is what pattern multiplication rests on in
  Module 3, and mutual coupling is where it starts to fray.
::::

::::{frame} When the assumption fails

When the assumption fails — thick elements, tightly coupled arrays, antennas
close to a ground plane or an airframe — you solve for the current numerically.
The **method of moments** discretizes the structure, enforces the boundary
condition on each segment, and solves a linear system for the segment currents;
then it runs the very same radiation integral to get the pattern. That is
literally what NEC is doing under the hood in the **Lesson 8 simulation lab**.

There is a measurement version of the same idea, too. Near-field scanning
(Lesson 5, and Module 2's measurement labs) samples the field on a surface close
to the antenna and transforms it to the far field — which is possible for
exactly one reason: the transform between the source distribution and the
far-field pattern is invertible.
::::

::::{frame} Key point
:::{callout}
Radiation is superposition with phase bookkeeping. Every current element sends
out a spherical wave; in the far field the rays run parallel, so an element's
only signature is the path difference $\hat{\mathbf r}\cdot\mathbf{r}'$. Summing
those contributions gives the radiation vector

$$
\mathbf{N}(\theta,\phi) = \int_{V'}\mathbf{J}(\mathbf{r}')\ e^{+jk\hat{\mathbf r}\cdot\mathbf{r}'}\ dV',
$$

which is a **Fourier transform of the current distribution** — and the entire
pattern, from beamwidth to sidelobes to where you point the beam, is a property
of that transform.
:::
::::

::::{frame} Summary — the machinery

| Symbol / idea | What it is | Number to remember |
| :-- | :-- | :-- |
| $\mathbf{A}$ | magnetic vector potential; the integral of the source, $\mathbf{B} = \nabla\times\mathbf{A}$ | one integral, then two curls — and in the far field the curls become multiplication by $-jk$ |
| $e^{-jkr}/r$ | spherical-wave factor — distance only, identical for every antenna ever built | field $\propto 1/r$, power $\propto 1/r^2$ |
| $\mathbf{N}(\theta,\phi)$ | radiation vector — direction only; all of the antenna's individuality | $E_\theta = -j\omega\mu\ e^{-jkr}N_\theta/4\pi r$, and $E_r \approx 0$ |
::::

::::{frame} Summary — the far-field approximation and the intensity

| Symbol / idea | What it is | Number to remember |
| :-- | :-- | :-- |
| far-field approximation | parallel rays: keep $\hat{\mathbf r}\cdot\mathbf{r}'$ in the phase, drop it in the amplitude | valid for $r \ge 2D^2/\lambda$, the $\pi/8$ ($22.5^{\circ}$) phase-error budget |
| $U(\theta,\phi)$ | radiation intensity; feeds $D$ and $G$ from Lesson 2 | $\dfrac{\eta_0 k^2}{32\pi^2}\left(\vert N_\theta\vert^2 + \vert N_\phi\vert^2\right)$, $\eta_0 \approx 377\ \Omega$ |
::::

::::{frame} Summary — the patterns

| Symbol / idea | What it is | Number to remember |
| :-- | :-- | :-- |
| $I(z') \leftrightarrow N_z(k_z)$ | current and pattern are a Fourier transform pair | $k_z = k\cos\theta$, visible only over $-k \le k_z \le +k$ |
| Infinitesimal dipole | $\vert F\vert = \sin\theta$ — the reference doughnut | HPBW $90^{\circ}$, $D = 1.5$ (1.76 dBi) |
| Half-wave dipole | $\vert F\vert = \cos\!\left(\tfrac{\pi}{2}\cos\theta\right)/\sin\theta$ — a sharper doughnut | HPBW $78.1^{\circ}$, $D = 1.64$ (2.15 dBi) |
| Uniform line source | space factor $\vert\sin u/u\vert$, $u = \tfrac{kL}{2}\cos\theta$; taper trades sidelobes for beamwidth | $\theta_\text{HP} \approx 0.886\ \lambda/L$, first sidelobe $-13.3$ dB; tapers reach $-23$ to $-31.5$ dB at 1.34–1.63× the beamwidth |
::::

::::{frame} Practice
- <a href="../../practice/ECE444_L06_Practice_blank.pdf" target="_blank" rel="noopener">Problem set (PDF)</a>
- <a href="../../practice/ECE444_L06_Practice_SOLUTIONS.pdf" target="_blank" rel="noopener">Solutions (PDF)</a>
::::

::::{frame} Where this is going

Module 1 is complete. You can describe an antenna's pattern and gain (L2), its
polarization and bandwidth (L3), its terminals (L4), where its far field starts
(L5), and now how to compute the pattern from the current (L6).

**Module 2** puts real currents into the integral: dipoles, monopoles, loops,
patches, slots, and horns, each one a different $\mathbf{J}$ producing a
different $\mathbf{N}$ — and the Lesson 8 simulation lab solves for the current
the integral needs. Then **Module 3** turns the Fourier relationship around and
uses it as a design tool: choose the pattern you want, and synthesize the
current distribution that produces it.
::::
