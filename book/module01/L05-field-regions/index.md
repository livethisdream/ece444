# L5 - Field Regions

:::{admonition} Slides
:class: slides
<a href="../../slides/L05-field-regions.html" target="_blank" rel="noopener">html slides</a>
<a href="../../slides/L05-field-regions.html?print-pdf" target="_blank" rel="noopener">pdf slides</a>
<a href="../../slides/L05-field-regions.md" target="_blank" rel="noopener">raw markdown slides</a>
:::

## Learning Objectives

<ol class="lo-list lo-sublist" style="--module: '1'; --lo: '5'">
  <li>I can distinguish the reactive near-field, radiating near-field, and far-field regions by what the fields are actually doing in each.</li>
  <li>I can calculate the boundaries between the three regions for a given antenna size and wavelength.</li>
  <li>I can explain the phase-error criterion behind the far-field distance, and why an antenna must be measured in its far field.</li>
</ol>

Lesson 4 looked *into* the antenna terminals. Now we step back *out* into the
space around the antenna and ask: as you walk away from the antenna, at what
point do the fields settle into the clean, predictable radiation pattern from
Lesson 2 — and what are they doing before that?

The space around any antenna divides into **three regions**. They are not sharp
walls; the fields transition gradually. But the boundaries are worth knowing,
because *where you stand changes what you measure.*

## Part 1: The three regions

<img src="../../viz/img/L05-field-regions.svg" alt="Concentric field regions around an antenna: reactive near-field, radiating near-field, and far-field" style="max-width: 620px; width: 100%; display: block; margin: 1em auto;">

### Reactive near-field

Right up against the antenna, the fields are dominated by **stored energy**, not
radiation. Energy sloshes back and forth between the antenna and the surrounding
space each cycle — like the field around a charged capacitor or a current-carrying
inductor. These are the terms that fall off fast, as $1/r^2$ and $1/r^3$, so they
vanish quickly with distance. A receiver here would load the antenna and change
its behavior; this is also why you keep objects away from a transmitting antenna's
immediate vicinity.

### Radiating near-field (Fresnel region)

A little farther out, the radiating part of the field takes over — energy is now
genuinely leaving the antenna. **But the shape of the pattern still depends on how
far away you are.** Because different parts of the antenna are at meaningfully
different distances from your observation point, the contributions add up with
distance-dependent phase, so the angular pattern keeps changing as you move out.
The wavefront is noticeably **curved**.

### Far-field (Fraunhofer region)

Far enough away, the antenna looks essentially like a **point source**. The
pattern shape stops changing with distance — measure it at $100\ \text{m}$ or
$1\ \text{km}$ and you get the same angular pattern, just weaker. In this region:

- the fields fall off as $1/r$ (power as $1/r^2$),
- $\mathbf{E}$, $\mathbf{H}$, and the propagation direction are mutually
  perpendicular,
- and locally the wave looks like a **plane wave** (flat wavefront).

This is the region every antenna specification implicitly refers to. "The gain
is 15 dBi" means *in the far field*.

### Where the regions come from: the fields of a short dipole

The three regions are not a convention someone imposed — they fall straight out
of the exact fields of the simplest possible antenna. Take an **infinitesimal
dipole**: a current element $Idl$ pointing along $\hat{\mathbf z}$, short enough
($dl \ll \lambda$) that the current is uniform along it. Solving Maxwell's
equations for this element gives the fields in closed form (spherical
coordinates, phasor convention with the $e^{-jkr}$ carried along as in Lesson 2,
and $k = 2\pi/\lambda$):

$$
E_r = \frac{\eta_0Idl\cos\theta}{2\pi r^2}
      \left(1 + \frac{1}{jkr}\right)e^{-jkr}
$$

$$
E_\theta = \frac{j k\eta_0Idl\sin\theta}{4\pi r}
      \left(1 + \frac{1}{jkr} - \frac{1}{(kr)^2}\right)e^{-jkr}
$$

$$
H_\phi = \frac{j kIdl\sin\theta}{4\pi r}
      \left(1 + \frac{1}{jkr}\right)e^{-jkr}
$$

with $E_\phi = H_r = H_\theta = 0$. Every antenna is built from current elements
like this, so whatever these fields do, real antennas do too — the near field is
just this, superposed.

**Read the fields by their powers of $r$.** Pull the $1/r$ out front of
$E_\theta$ and the bracket holds three terms whose relative sizes are set entirely
by $kr$. Multiplying through, the actual field is a sum of three pieces:

$$
E_\theta \propto
\underbrace{\frac{1}{r}}_{\text{radiation}}
+
\underbrace{\frac{1}{kr^{2}}}_{\text{induction}}
+
\underbrace{\frac{1}{k^{2}r^{3}}}_{\text{electrostatic}}
$$

Those are the three regions, hiding inside one equation:

| Term | Falls off as | Physical origin | Wins where |
| :-- | :-- | :-- | :-- |
| Radiation | $1/r$ | the escaping wave — Lesson 2's far field | $kr \gg 1$ |
| Induction | $1/r^2$ | Biot–Savart / Ampère field of the current | $kr \sim 1$ |
| Electrostatic | $1/r^3$ | quasi-static field of the charge $\pm q$ at the tips | $kr \ll 1$ |

**The crossover is a single number.** The radiation term (size $\propto 1$
inside the bracket) and the induction term (size $\propto 1/kr$) are equal when

$$
kr = 1
\qquad\Longrightarrow\qquad
r = \frac{1}{k} = \frac{\lambda}{2\pi} \approx 0.16\lambda .
$$

Inside $\lambda/2\pi$ the stored ($1/r^2$, $1/r^3$) terms take over and blow up as
you approach the antenna; outside it, only the $1/r$ radiation term survives. This
is exactly the $\lambda/2\pi$ figure quoted for small antennas in the next section
— now *derived*, not asserted. The $0.62\sqrt{D^3/\lambda}$ boundary is the same
idea generalized to an antenna of finite size $D$.

**Why "reactive" is the literal, correct word.** Stored energy that never leaves
is *reactive power* — the same reactive power you met at the terminals in Lesson 4,
now living in the surrounding field. Form the complex radial Poynting vector
$\tfrac12 E_\theta H_\phi^{*}$ and, remarkably, the cross-terms collapse to just
two:

$$
\tfrac12E_\theta H_\phi^{*} =
\underbrace{\tfrac12\eta_0\!\left(\tfrac{kIdl\sin\theta}{4\pi}\right)^{2}
\frac{1}{r^{2}}}_{\text{real — radiated power}\propto1/r^{2}}
- j
\underbrace{\tfrac12\eta_0\!\left(\tfrac{kIdl\sin\theta}{4\pi}\right)^{2}
\frac{1}{k^{3}r^{5}}}_{\text{imaginary — stored power}\propto1/r^{5}}
$$

Two things to read off this:

- The **real part** — genuine outward power — falls off as $1/r^2$ (the
  inverse-square law) and *does not contain the near-field terms at all*.
  Radiation is radiation at every distance; the near field adds nothing to it.
- The **imaginary part** — reactive, non-transported power — falls off as $1/r^5$.
  It is negligible far out but overwhelming close in, and the factor of $j$ says
  $\mathbf E$ and $\mathbf H$ are $90^{\circ}$ out of phase there: energy flows
  outward for a quarter cycle, then all the way back. Nothing leaves. That is the
  "sloshing" of the qualitative picture, made exact.

The minus sign ($-j$) even tells you the stored energy is predominantly
**electric** — which fits, because a short dipole is *capacitive* at its terminals.
Its large negative reactance from Lesson 4 and this near-field electric energy are
the same physics, seen from the outside versus the inside.

### Interactive — the three terms and their crossover

Slide the observation point in and out. The three field terms are straight lines
on a log–log plot (slopes $-1$, $-2$, $-3$); they all cross at $kr = 1$, i.e.
$r = \lambda/2\pi$. To the left, the $1/r^3$ stored field dominates — the reactive
near field. To the right, only the $1/r$ radiation term is left standing.

<iframe src="../../viz/near-field-terms.html"
        width="100%" height="480"
        style="border: 1px solid #cddce9; border-radius: 6px;"
        loading="lazy"
        title="Near-field term crossover">
</iframe>

## Part 2: The boundaries

Let $D$ be the antenna's **largest dimension** and $\lambda$ the wavelength. The
two boundaries are:

$$
\underbrace{r < 0.62\sqrt{\dfrac{D^3}{\lambda}}}_{\text{reactive near-field}}
\qquad
\underbrace{0.62\sqrt{\dfrac{D^3}{\lambda}} \le r < \dfrac{2D^2}{\lambda}}_{\text{radiating near-field}}
\qquad
\underbrace{r \ge \dfrac{2D^2}{\lambda}}_{\text{far-field}}
$$

| Region | Extent | Fields |
| :-- | :-- | :-- |
| Reactive near-field | $r < 0.62\sqrt{D^3/\lambda}$ | stored, non-radiating; $1/r^2$, $1/r^3$ |
| Radiating near-field | $0.62\sqrt{D^3/\lambda} \le r < 2D^2/\lambda$ | radiating, but pattern varies with $r$; curved wavefront |
| Far-field | $r \ge 2D^2/\lambda$ | pattern fixed; $1/r$; locally plane wave |

```{note}
These formulas apply to **electrically large** antennas ($D > \lambda$), where
the $2D^2/\lambda$ distance is the meaningful one. For an electrically **small**
antenna the reactive near-field simply extends out to about $\lambda / 2\pi$, and
the far field begins there — this is precisely the $kr = 1$ crossover we derived
from the dipole fields above.
```

### Where the far-field distance comes from

The far-field distance $2D^2/\lambda$ is a **phase-error** criterion. Picture a
plane wavefront arriving at an aperture of size $D$ from a source a distance $r$
away. The path from the source to the *edge* of the aperture is slightly longer
than the path to the *center*. That extra path length is approximately

$$
\Delta \approx \frac{(D/2)^2}{2r} = \frac{D^2}{8r}.
$$

The agreed-upon tolerance is that this path difference should be no more than
$\lambda/16$, which corresponds to a **maximum phase error of $22.5^{\circ}$**
across the aperture. Setting $\Delta = \lambda/16$:

$$
\frac{D^2}{8r} = \frac{\lambda}{16}
\qquad\Longrightarrow\qquad
r = \frac{2D^2}{\lambda}.
$$

Inside this distance the phase across the aperture curves enough to distort the
pattern; beyond it, the wavefront is "flat enough" and the pattern is stable.

### Worked example

A reflector antenna has diameter $D = 1.2\ \text{m}$ and operates at
$f = 10\ \text{GHz}$.

$$
\lambda = \frac{c}{f} = \frac{3\times10^8}{10\times10^9} = 0.03\ \text{m}
$$

$$
r_\text{ff} = \frac{2D^2}{\lambda} = \frac{2(1.2)^2}{0.03} = 96\ \text{m}
$$

$$
r_\text{reactive} = 0.62\sqrt{\frac{D^3}{\lambda}}
= 0.62\sqrt{\frac{1.728}{0.03}} = 0.62\sqrt{57.6} \approx 4.7\ \text{m}
$$

So the reactive near-field ends at $\approx 4.7\ \text{m}$, the radiating
near-field runs from there to $96\ \text{m}$, and only beyond $96\ \text{m}$ is
the antenna in its far field. To measure this dish's pattern on a conventional
range you would need almost a **hundred metres** of separation.

### Interactive — field-region explorer

Set the antenna's largest dimension $D$ and the frequency, and watch the three
region boundaries move along a distance axis. The phase error across the aperture
is shown so you can see why the far-field distance grows with $D^2$.

<iframe src="../../viz/field-regions.html"
        width="100%" height="430"
        style="border: 1px solid #cddce9; border-radius: 6px;"
        loading="lazy"
        title="Field-region explorer">
</iframe>

## Part 3: Why the far-field distance matters

The far-field distance is not academic — it sets the size of your test range. To
measure an antenna's true pattern, gain, and sidelobes, the antenna under test
must sit in the **far field** of the source (and vice versa). For a large dish at
high frequency that can mean hundreds of metres, which is often impractical.

That is exactly why **near-field scanning** exists: you measure the fields on a
surface *close* to the antenna (in the radiating near-field), then mathematically
propagate them out to the far field. You will see this in Module 2's measurement
lessons — but it only works because the far-field pattern is completely determined
by the near-field distribution, which is the subject of the next lesson.

:::{admonition} Key Point
:class: key-concept

Where you stand changes what you see. Close in, the field is **stored energy**
that doesn't radiate; a bit farther, it **radiates but the pattern is still
forming**; and only beyond $2D^2/\lambda$ does the antenna show its **true,
distance-independent pattern**. Every gain and pattern spec assumes you are out
there in the far field.
:::

## Where this is going

You now know *where* the far-field pattern lives and how far away it starts. Next,
**Lesson 6 (Radiation Integrals)** answers *what* that pattern is: given the
current distribution on the antenna, we set up the radiation integrals that
produce the far-field pattern directly — the mathematical machinery behind
everything we have described qualitatively so far.
