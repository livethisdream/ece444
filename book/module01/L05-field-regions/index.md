---
frame_view: true
---

# L5 - Field Regions

::::{frame}
:class: title-frame

<div class="course-mark">ECE 444 · Fall 2026</div>

<h1 class="frame-title">Field Regions</h1>

<div class="title-rule"></div>

Where you stand changes what you see.

Lesson 5 · Antennas, Phased Arrays, and Radar Systems · Dr. Neil Rogers
::::

::::{frame}
:::{admonition} Slides
:class: slides
<a href="../../slides/L05-field-regions.html" target="_blank" rel="noopener">html slides</a>
<a href="../../slides/L05-field-regions.html?print-pdf" target="_blank" rel="noopener">pdf slides</a>
<a href="../../slides/L05-field-regions.md" target="_blank" rel="noopener">raw markdown slides</a>
:::
::::

::::{frame} Learning Objectives

<ol class="lo-list lo-sublist" style="--module: '1'; --lo: '5'">
  <li>I can distinguish the reactive near-field, radiating near-field, and far-field regions by what the fields are actually doing in each.</li>
  <li>I can calculate the boundaries between the three regions for a given antenna size and wavelength.</li>
  <li>I can explain the phase-error criterion behind the far-field distance, and why you must measure an antenna in its far field.</li>
</ol>

:::{depth}
Lesson 4 looked *into* the antenna terminals. Now we step back *out* into the
space around the antenna and ask: as you walk away from the antenna, at what
point do the fields settle into the clean, predictable radiation pattern from
Lesson 2 — and what are they doing before that?

The space around any antenna divides into **three regions**. They are not sharp
walls; the fields transition gradually. But the boundaries are worth knowing,
because *where you stand changes what you measure.*
:::
::::

::::{frame} The three regions
<img src="../../viz/img/L05-field-regions.svg" alt="Concentric field regions around an antenna: reactive near-field, radiating near-field, and far-field" style="max-width: 620px; width: 100%; display: block; margin: 1em auto;">
::::

::::{frame} Reactive near-field
Right up against the antenna, **stored energy** dominates the fields, not
radiation. Energy sloshes back and forth between the antenna and the surrounding
space each cycle — like the field around a charged capacitor or a current-carrying
inductor. These are the terms that fall off fast, as $1/r^2$ and $1/r^3$, so they
vanish quickly with distance. A receiver here would load the antenna and change
its behavior; this is also why you keep objects away from a transmitting antenna's
immediate vicinity.
::::

::::{frame} Radiating near-field (Fresnel region)
A little farther out, the radiating part of the field takes over — energy is now
genuinely leaving the antenna. **But the shape of the pattern still depends on how
far away you are.** Because different parts of the antenna are at meaningfully
different distances from your observation point, the contributions add up with
distance-dependent phase, so the angular pattern keeps changing as you move out.
The wavefront is noticeably **curved**.
::::

::::{frame} Far-field (Fraunhofer region)
Far enough away, the antenna looks essentially like a **point source**. The
pattern shape stops changing with distance — measure it at $100\ \text{m}$ or
$1\ \text{km}$ and you get the same angular pattern, just weaker. In this region:

- the fields fall off as $1/r$ (power as $1/r^2$),
- $\mathbf{E}$, $\mathbf{H}$, and the propagation direction are mutually
  perpendicular,
- and locally the wave looks like a **plane wave** (flat wavefront).

This is the region every antenna specification implicitly refers to. "The gain
is 15 dBi" means *in the far field*.
::::

::::{frame} Where the regions come from: the fields of a short dipole
The three regions are not a convention someone imposed — they fall straight out
of the exact fields of the simplest possible antenna. Take an **infinitesimal
dipole**: a current element $Idl$ pointing along $\hat{\mathbf z}$, short enough
($dl \ll \lambda$) that the current is uniform along it. Solving Maxwell's
equations for this element gives the fields in closed form (spherical
coordinates, phasor convention with the $e^{-jkr}$ carried along as in Lesson 2,
and $k = 2\pi/\lambda$):

$$
E_\theta = \frac{j k\eta_0Idl\sin\theta}{4\pi r}
      \left(1 + \frac{1}{jkr} - \frac{1}{(kr)^2}\right)e^{-jkr}
$$
::::

::::{frame} The near field is just this, superposed
$$
H_\phi = \frac{j kIdl\sin\theta}{4\pi r}
      \left(1 + \frac{1}{jkr}\right)e^{-jkr}
$$

with $E_\phi = H_r = H_\theta = 0$. Current elements like this make up every
antenna, so whatever these fields do, real antennas do too — the near field is
just this, superposed.

:::{depth}
$$
E_r = \frac{\eta_0Idl\cos\theta}{2\pi r^2}
      \left(1 + \frac{1}{jkr}\right)e^{-jkr}
$$
:::
::::

::::{frame} Read the fields by their powers of r
Pull the $1/r$ out front of
$E_\theta$ and the bracket holds three terms, and $kr$ alone sets their
relative sizes. Multiplying through, the actual field is a sum of three pieces:

$$
E_\theta \propto
\underbrace{\frac{1}{r}}_{\text{radiation}}
+
\underbrace{\frac{1}{kr^{2}}}_{\text{induction}}
+
\underbrace{\frac{1}{k^{2}r^{3}}}_{\text{electrostatic}}
$$
::::

::::{frame} What each term is, and where it wins
| Term | Falls off as | Physical origin | Where it matters |
| :-- | :-- | :-- | :-- |
| Radiation | $1/r$ | the escaping wave — Lesson 2's far field | $kr \gg 1$ |
| Induction | $1/r^2$ | Biot–Savart / Ampère field of the current | comparable to the other two near $kr \sim 1$ |

:::{depth}
Those are the three regions, hiding inside one equation:
:::
::::

::::{frame} Electrostatic — quasi-static field of the charge at the tips
| Term | Falls off as | Physical origin | Where it matters |
| :-- | :-- | :-- | :-- |
| Electrostatic | $1/r^3$ | quasi-static field of the charge $\pm q$ at the tips | $kr \ll 1$ |
::::

::::{frame} The crossover is a single number
The radiation term (size $\propto 1$
inside the bracket) and the induction term (size $\propto 1/kr$) are equal when

$$
kr = 1
\qquad\Longrightarrow\qquad
r = \frac{1}{k} = \frac{\lambda}{2\pi} \approx 0.16\lambda .
$$

:::{depth}
Read that carefully, because it is the single most misquoted number in the
subject. At $kr = 1$ all three terms are **the same size** — that is *all* it
says. Inside $\lambda/2\pi$ the stored ($1/r^2$, $1/r^3$) terms take over and blow
up as you approach the antenna. Outside it the radiation term does not suddenly
stand alone; it merely starts to **dominate increasingly**, because each reactive
term keeps shedding another factor of $1/kr$. Dividing the bracket through by the
radiation term makes the bookkeeping obvious — the three sizes are
$1 : 1/kr : 1/(kr)^2$:

| $kr$ | $r$ | radiation : induction : electrostatic |
| :-- | :-- | :-- |
| $1$ | $0.16\lambda$ | $1 : 1 : 1$ |
| $6$ | $\approx 1\lambda$ | $1 : 0.17 : 0.03$ |
| $10$ | $\approx 1.6\lambda$ | $1 : 0.1 : 0.01$ |

So the reactive terms are negligible only for $kr \gg 1$. They fall below about
$10\%$ near $kr \approx 10$, i.e. $r \approx 1.6\lambda$; at one wavelength out
induction is still $17\%$. **Rule of thumb: $kr = 1$ is the crossover, not the
start of the far field — for a small antenna, give it a few wavelengths before
you trust the pattern.** The $\lambda/2\pi$ figure quoted for small antennas in
the next section is this crossover, now *derived* rather than asserted, and the
$0.62\sqrt{D^3/\lambda}$ boundary is the same idea generalized to an antenna of
finite size $D$.
:::
::::

::::{frame} Why "reactive" is the literal, correct word
Stored energy that never leaves is *reactive power* — the same reactive power you met at the terminals in Lesson 4,
now living in the surrounding field. Form the complex radial Poynting vector
$\tfrac12 E_\theta H_\phi^{*}$ and the cross-terms collapse to just two: a **real**
part falling as $1/r^2$, which is genuine outward power and contains no near-field
terms at all, and an **imaginary** part falling as $1/r^5$, which is the stored
energy sloshing out and back each cycle. Radiation is radiation at every distance;
the near field adds nothing to it and carries nothing away.

:::{depth}
Multiplying $E_\theta$ by $H_\phi^{*}$ term by term, everything cancels except
two pieces:

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
  inverse-square law) and *does not contain the near-field terms at all* — no
  cross-term between a $1/r$ field and a $1/r^2$ field survives the algebra.
- The **imaginary part** — reactive, non-transported power — falls off as $1/r^5$.
  It is negligible far out but overwhelming close in, and the factor of $j$ says
  $\mathbf E$ and $\mathbf H$ are $90^{\circ}$ out of phase there: energy flows
  outward for a quarter cycle, then all the way back. Nothing leaves. That is the
  "sloshing" of the qualitative picture, made exact.

The minus sign ($-j$) even tells you the stored energy is predominantly
**electric** — which fits, because a short dipole is *capacitive* at its terminals.
Its large negative reactance from Lesson 4 and this near-field electric energy are
the same physics, seen from the outside versus the inside.
:::
::::

::::{frame} A preview from the practice set
The practice set for this lesson opens with a which-term-dominates part: you
evaluate the ratio $1 : 1/kr : 1/(kr)^2$ at $kr = 0.1$ and $kr = 10$ and name the
winner in each. Do it by hand once and the crossover stops being a number to
memorize.
::::

::::{frame} Interactive — the three terms and their crossover
:class: viz-frame

Slide the observation point in and out. The three field terms are straight lines
on a log–log plot (slopes $-1$, $-2$, $-3$); they all cross at $kr = 1$, i.e.
$r = \lambda/2\pi$. To the left, the $1/r^3$ stored field runs away — the reactive
near field. To the right the radiation term takes over, and its lead over the
other two grows tenfold for every decade you move out — which is why "negligible"
takes until $kr \approx 10$, not $kr = 1$.

<iframe src="../../viz/near-field-terms.html"
        width="100%" height="521"
        style="border: 1px solid #cddce9; border-radius: 6px;"
        loading="lazy"
        title="Near-field term crossover">
</iframe>
::::

::::{frame} The boundaries
Let $D$ be the antenna's **largest dimension** and $\lambda$ the wavelength. The
two boundaries are:

$$
\underbrace{r < 0.62\sqrt{\dfrac{D^3}{\lambda}}}_{\text{reactive near-field}}
\qquad
\underbrace{0.62\sqrt{\dfrac{D^3}{\lambda}} \le r < \dfrac{2D^2}{\lambda}}_{\text{radiating near-field}}
\qquad
\underbrace{r \ge \dfrac{2D^2}{\lambda}}_{\text{far-field}}
$$
::::

::::{frame} Region, extent, and fields
| Region | Extent | Fields |
| :-- | :-- | :-- |
| Reactive near-field | $r < 0.62\sqrt{D^3/\lambda}$ | stored, non-radiating; $1/r^2$, $1/r^3$ |
| Radiating near-field | $0.62\sqrt{D^3/\lambda} \le r < 2D^2/\lambda$ | radiating, but pattern varies with $r$; curved wavefront |
| Far-field | $r \ge 2D^2/\lambda$ | pattern fixed; $1/r$; locally plane wave |

:::{depth}
These formulas apply to **electrically large** antennas ($D > \lambda$), where
the $2D^2/\lambda$ distance is the meaningful one. For an electrically **small**
antenna the reactive near-field simply extends out to about $\lambda / 2\pi$ —
precisely the $kr = 1$ crossover we derived from the dipole fields above. Take the
larger of the two distances:

$$
r_\text{ff} \approx \max\left(\frac{2D^2}{\lambda},\ \frac{\lambda}{2\pi}\right).
$$

But do not read $\lambda/2\pi$ as "the far field begins here". At that radius the
stored terms are merely *equal* to the radiation term, not gone. In practice give
a small antenna **a few wavelengths** — $kr$ of order 10 — before you trust its
pattern.
:::
::::

::::{frame} Where the far-field distance comes from
The far-field distance $2D^2/\lambda$ is a **phase-error** criterion. Picture a
point source a distance $r$ away, radiating a **spherical** wavefront onto an
aperture of size $D$. Because the wavefront is a sphere, the path from the source
to the *edge* of the aperture is slightly longer than the path to the *center* —
a plane wave, by definition, would have no such difference, and the plane-wave
limit is exactly what you earn once this criterion is met. That extra path length
is approximately

$$
\Delta \approx \frac{(D/2)^2}{2r} = \frac{D^2}{8r}.
$$
::::

::::{frame} The phase-error budget
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
::::

::::{frame} Worked example
A reflector antenna has diameter $D = 1.2\ \text{m}$ and operates at
$f = 10\ \text{GHz}$.

So the reactive near-field ends at $\approx 4.7\ \text{m}$, the radiating
near-field runs from there to $96\ \text{m}$, and only beyond $96\ \text{m}$ is
the antenna in its far field. To measure this dish's pattern on a conventional
range you would need almost a **hundred metres** of separation.

:::{depth}
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
:::
::::

::::{frame} Interactive — field-region explorer
:class: viz-frame

Set the antenna's largest dimension $D$ and the frequency, and watch the three
region boundaries slide along the distance axis in the top panel. Then drag the
range $r$: the lower panel redraws the spherical wavefront arriving over the
aperture and plots the phase error it produces across $D$, turning green the
moment that error drops under the $22.5^{\circ}$ limit. Notice that green arrives
exactly as $r$ crosses $2D^2/\lambda$, and that doubling $D$ pushes it four times
farther out — the $D^2$ in the formula, on screen.

<iframe src="../../viz/field-regions.html"
        width="100%" height="656"
        style="border: 1px solid #cddce9; border-radius: 6px;"
        loading="lazy"
        title="Field-region explorer">
</iframe>
::::

::::{frame} Why the far-field distance matters
The far-field distance is not academic — it sets the size of your test range. To
measure an antenna's true pattern, gain, and sidelobes, the antenna under test
must sit in the **far field** of the source (and vice versa). For a large dish at
high frequency that can mean hundreds of metres, which is often impractical.

That is exactly why **near-field scanning** exists: you measure the fields on a
surface *close* to the antenna (in the radiating near-field), then mathematically
propagate them out to the far field. You will see this in Module 2's measurement
lessons — but it only works because the near-field distribution completely
determines the far-field pattern, which is the subject of the next lesson.
::::

::::{frame} Key point
:::{callout}
Where you stand changes what you see. Close in, the field is **stored energy**
that doesn't radiate; a bit farther, it **radiates but the pattern is still
forming**; and only beyond $2D^2/\lambda$ does the antenna show its **true,
distance-independent pattern**. Every gain and pattern spec assumes you are out
there in the far field.
:::
::::

::::{frame} Summary — the three terms and the crossover
| Symbol / idea | What it is | Number to remember |
| :-- | :-- | :-- |
| Three field terms | One dipole equation holds all three regions | $1 : 1/kr : 1/(kr)^2$ |
| $kr = 1$ crossover | Where all three terms are *equal* — not where the far field starts | $r = \lambda/2\pi \approx 0.16\lambda$ |
::::

::::{frame} Summary — the true far field
| Symbol / idea | What it is | Number to remember |
| :-- | :-- | :-- |
| True far field | Reactive terms actually negligible | $kr \gg 1$; under $10\%$ near $kr \approx 10$ ($r \approx 1.6\lambda$), so allow $r \gtrsim \lambda$ and a few wavelengths in practice |
::::

::::{frame} Summary — the boundaries
| Symbol / idea | What it is | Number to remember |
| :-- | :-- | :-- |
| Reactive near-field edge | Inner boundary for an electrically large antenna | $r = 0.62\sqrt{D^3/\lambda}$ |
| Far-field distance | Outer boundary; pattern stops changing with $r$ | $r \ge 2D^2/\lambda$ |
| Phase-error tolerance | What the criterion $2D^2/\lambda$ comes from | $\Delta \le \lambda/16$, i.e. $\pi/8 = 22.5^{\circ}$ |
| Worked dish | $D = 1.2\ \text{m}$ at $10\ \text{GHz}$ ($\lambda = 0.03\ \text{m}$) | reactive to $4.7\ \text{m}$; far field beyond $96\ \text{m}$ |
::::

::::{frame} Practice
- <a href="../../practice/ECE444_L05_Practice_blank.pdf" target="_blank" rel="noopener">Problem set (PDF)</a>
- <a href="../../practice/ECE444_L05_Practice_SOLUTIONS.pdf" target="_blank" rel="noopener">Solutions (PDF)</a>
::::

::::{frame} Where this is going
You now know *where* the far-field pattern lives and how far away it starts. Next,
**Lesson 6 (Radiation Integrals)** answers *what* that pattern is: given the
current distribution on the antenna, we set up the radiation integrals that
produce the far-field pattern directly — the mathematical machinery behind
everything we have described qualitatively so far.

:::{depth}
Watch for one specific move in that derivation. Expanding the distance from a
source point to the observer gives a linear term and a quadratic one, and *throwing the quadratic
term away* is what defines the far field. That discarded term is the
path difference $D^2/8r$ from this lesson, and the licence to drop it is the
$\pi/8$ tolerance — so "the far-field approximation" in Lesson 6 and
$r \ge 2D^2/\lambda$ here are the same statement, one written as an integral and
one as a distance.
:::
::::
