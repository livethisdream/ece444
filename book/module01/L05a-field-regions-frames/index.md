---
frame_view: true
---

# L5a - Field Regions (frame view)

::::{frame}
:class: title-frame

<div class="course-mark">ECE 444 · Fall 2026</div>

<h1 class="frame-title">Field Regions</h1>

<div class="title-rule"></div>

Where you stand changes what you see.

Lesson 5 · Antennas, Phased Arrays, and Radar Systems · Dr. Neil Rogers
::::

::::{frame} Learning objectives
1. I can distinguish the reactive near-field, radiating near-field, and far-field regions by what the fields are actually doing in each.
2. I can calculate the boundaries between the three regions for a given antenna size and wavelength.
3. I can explain the phase-error criterion behind the far-field distance, and why you must measure an antenna in its far field.

:::{depth}
Lesson 4 looked *into* the antenna terminals. Now we step back *out* into the
space around the antenna and ask: as you walk away, at what point do the fields
settle into the clean, predictable radiation pattern from Lesson 2 — and what
are they doing before that?

The space around any antenna divides into **three regions**. They are not sharp
walls; the fields transition gradually. But the boundaries are worth knowing,
because *where you stand changes what you measure.*
:::
::::

::::{frame} Where we were
- **L2** — pattern, directivity, gain. Every one of those numbers was quoted *far away*, without ever saying so.
- **L3** — polarization and bandwidth of that same escaping wave.
- **L4** — the **terminals**: $Z_{\text{in}}$, reactance, stored energy the radio has to fight.

Today we step outside the antenna. Where you stand changes what you measure.
::::

::::{frame} Today's plan
1. What **near** and **far** actually mean
2. The exact fields of one current element — **three terms, three powers of $r$**
3. The crossover at $kr = 1$ — and what it does *not* say
4. The **three regions** and their boundaries
5. Where $2D^{2}/\lambda$ comes from — a **phase-error budget**
6. Why an antenna range has to be so long
::::

::::{frame} Near and far
Walk away from a transmitting antenna and watch the field.

- **Near** — the field still remembers how the antenna is *built*. Its shape depends on how far out you are, and some of it never leaves at all.
- **Far** — the antenna has collapsed into a **point source**. The pattern shape stops changing with $r$; the amplitude just scales as $1/r$.

:::{callout}
"The gain is 15 dBi" means **in the far field**. Every spec you will ever read
carries that silent qualifier.
:::
::::

::::{frame} Where the regions come from
The regions are not a convention someone imposed. Solve Maxwell exactly for the
simplest antenna there is — an **infinitesimal dipole**, a current element
$I\,dl$ along $\hat{\mathbf z}$ with $dl \ll \lambda$:

$$
E_\theta = \frac{jk\eta_0 I\,dl\,\sin\theta}{4\pi r}
  \left(1 + \frac{1}{jkr} - \frac{1}{(kr)^{2}}\right) e^{-jkr}
$$

$$
H_\phi = \frac{jk I\,dl\,\sin\theta}{4\pi r}
  \left(1 + \frac{1}{jkr}\right) e^{-jkr}
$$

**Current elements like this make up every antenna.** Whatever these fields do,
real antennas do too — superposed.

:::{depth}
The element is short enough ($dl \ll \lambda$) that the current is uniform along
it. These are spherical coordinates, phasor convention, with $e^{-jkr}$ carried
along as in Lesson 2, and $k = 2\pi/\lambda$.

There is a third component the slide leaves out — a purely radial field with no
radiation term at all:

$$
E_r = \frac{\eta_0 I\,dl\,\cos\theta}{2\pi r^{2}}
  \left(1 + \frac{1}{jkr}\right) e^{-jkr}
$$

with $E_\phi = H_r = H_\theta = 0$. It falls as $1/r^{2}$ at best, so it is a
near-field quantity only — it contributes nothing to the pattern you measure far
away.
:::
::::

::::{frame} Read the fields by their powers of r
Multiply the bracket through and the field is a sum of three pieces:

$$
E_\theta \propto \frac{1}{r} + \frac{1}{kr^{2}} + \frac{1}{k^{2}r^{3}}
$$

| Term | Falls off as | Physical origin | Wins where |
| :-- | :-- | :-- | :-- |
| radiation | $1/r$ | the escaping wave — L2's far field | $kr \gg 1$ |
| induction | $1/r^{2}$ | Biot–Savart field of the current | $kr \sim 1$ |
| electrostatic | $1/r^{3}$ | quasi-static field of the charge at the tips | $kr \ll 1$ |

:::{callout}
Three regions, hiding inside one equation. The single number $kr$ sets their
relative sizes **entirely**.
:::
::::

::::{frame} The three terms, on log–log axes
<img src="../../slides/fig/L05-term-crossover.svg" alt="The three field terms as straight lines of slope minus one, two and three on log-log axes, crossing at kr equals one">

:::{depth}
To the left of the crossover the $1/r^{3}$ stored field runs away — the reactive
near field. To the right the radiation term takes over, and its lead over the
other two grows **tenfold for every decade** you move out. That is why
"negligible" takes until $kr \approx 10$, not $kr = 1$.
:::
::::

::::{frame} Drive it yourself — the three terms
:class: viz-frame

Move the observation point in and out and watch which term is on top.

<iframe class="viz" data-autosize="1" src="../../viz/near-field-terms.html" style="height:520px" title="Near-field term crossover"></iframe>
::::

::::{frame} The crossover is a single number
Radiation (size 1 in the bracket) and induction (size $1/kr$) are equal when

$$
kr = 1 \qquad\Longrightarrow\qquad r = \frac{1}{k} = \frac{\lambda}{2\pi} \approx 0.16\lambda
$$

- At $kr = 1$ all three terms are **the same size**. That is *all* it says.
- Reactive terms are negligible only for $kr \gg 1$: at $kr = 6$ — about one wavelength out — induction is down to 17% and the electrostatic term to 3%.

:::{callout}
$kr = 1$ is the **crossover**, not the start of the far field. For a small
antenna the far field is usable from roughly a wavelength out, not from
$0.16\lambda$.
:::

:::{depth}
Read that carefully, because it is the single most misquoted number in the
subject. Inside $\lambda/2\pi$ the stored terms take over and blow up as you
approach the antenna. Outside it the radiation term does not suddenly stand
alone; it merely starts to **dominate increasingly**, because each reactive term
keeps shedding another factor of $1/kr$.

Dividing the bracket through by the radiation term makes the bookkeeping obvious
— the three sizes are $1 : 1/kr : 1/(kr)^{2}$:

| $kr$ | $r$ | radiation : induction : electrostatic |
| :-- | :-- | :-- |
| $1$ | $0.16\lambda$ | $1 : 1 : 1$ |
| $6$ | $\approx 1\lambda$ | $1 : 0.17 : 0.03$ |
| $10$ | $\approx 1.6\lambda$ | $1 : 0.1 : 0.01$ |

They fall below about 10% near $kr \approx 10$, i.e. $r \approx 1.6\lambda$. The
$0.62\sqrt{D^{3}/\lambda}$ boundary in the next section is this same idea,
generalised to an antenna of finite size $D$.
:::
::::

::::{frame} Why "reactive" is the literal word
Form the complex radial Poynting vector and the cross-terms collapse to just two:

$$
\tfrac{1}{2} E_\theta H_\phi^{*} \propto \frac{1}{r^{2}} - j\,\frac{1}{k^{3}r^{5}}
$$

- **Real part** — genuine outward power, falling as $1/r^{2}$, the inverse-square law. It contains **no near-field terms at all**: radiation is radiation at every distance.
- **Imaginary part** — reactive power, falling as $1/r^{5}$. The $j$ says $\mathbf E$ and $\mathbf H$ sit $90^{\circ}$ apart: energy flows out for a quarter cycle, then all the way back. **Nothing leaves.**

:::{callout}
The same reactive power you met at the terminals in L4 — now seen from *outside*
the antenna instead of inside it.
:::

:::{depth}
Multiplying $E_\theta$ by $H_\phi^{*}$ term by term, everything cancels except
two pieces, with the constant written out:

$$
\tfrac{1}{2} E_\theta H_\phi^{*} =
\tfrac{1}{2}\eta_0\!\left(\frac{k I\,dl\,\sin\theta}{4\pi}\right)^{2}\frac{1}{r^{2}}
- j\,\tfrac{1}{2}\eta_0\!\left(\frac{k I\,dl\,\sin\theta}{4\pi}\right)^{2}\frac{1}{k^{3}r^{5}}
$$

No cross-term between a $1/r$ field and a $1/r^{2}$ field survives the algebra —
which is *why* the real part carries no near-field content.

The minus sign on the $j$ even tells you the stored energy is predominantly
**electric**, which fits: a short dipole is *capacitive* at its terminals. Its
large negative reactance from Lesson 4 and this near-field electric energy are
the same physics, seen from the outside versus the inside.
:::
::::

::::{frame} The three regions
<img src="../../slides/fig/L05-region-diagram.svg" alt="Three concentric field regions around an antenna: a small reactive near field, a radiating near field around it, and the far field extending outward">

Not to scale, and the boundaries are gradual, not walls. Both radii depend on
antenna size and wavelength.
::::

::::{frame} Reactive near-field
Right up against the antenna the field is **stored energy**, not radiation — the
$1/r^{2}$ and $1/r^{3}$ terms, sloshing in and out each cycle.

- Like the field around a charged capacitor or a current-carrying inductor.
- Put a receiver here and it **loads the antenna** and changes its behaviour.
- Which is also why you keep hands, heads, and hardware out of it.

It falls off fast. Take one step out and it is gone.
::::

::::{frame} Radiating near-field (Fresnel)
Energy is now genuinely leaving — **but the shape of the pattern still depends on
how far away you are.**

- Different parts of the antenna are at meaningfully different distances from your observation point.
- Their contributions add with **distance-dependent phase**, so the angular pattern keeps changing as you move out.
- The wavefront is noticeably **curved**.

:::{callout}
Measure a pattern here and you have measured *this range*, not the antenna.
:::
::::

::::{frame} Far-field (Fraunhofer)
Far enough out, the antenna looks like a **point source**:

- fields fall as $1/r$, power as $1/r^{2}$
- $\mathbf E$, $\mathbf H$, and the direction of propagation are mutually perpendicular
- locally the wave is a **plane wave** — flat wavefront

Measure at 100 m or at 1 km and you get the same angular pattern, just weaker.

:::{depth}
This is the region every antenna specification implicitly refers to. "The gain
is 15 dBi" means *in the far field* — and nobody writes that down, because
everyone in the field assumes it.
:::
::::

::::{frame} The boundaries
Let $D$ be the antenna's **largest dimension** and $\lambda$ the wavelength.

| Region | Extent | Fields |
| :-- | :-- | :-- |
| reactive near-field | $r < 0.62\sqrt{D^{3}/\lambda}$ | stored, non-radiating; $1/r^{2}$, $1/r^{3}$ |
| radiating near-field | $0.62\sqrt{D^{3}/\lambda} \le r < 2D^{2}/\lambda$ | radiating, pattern varies with $r$; curved wavefront |
| far-field | $r \ge 2D^{2}/\lambda$ | pattern fixed; $1/r$; locally a plane wave |

Not walls — the fields transition gradually.

:::{depth}
These formulas apply to **electrically large** antennas ($D > \lambda$), where
$2D^{2}/\lambda$ is the meaningful distance. For an electrically **small**
antenna the reactive near-field simply extends out to about $\lambda/2\pi$ —
precisely the $kr = 1$ crossover derived from the dipole fields. Take the larger
of the two:

$$
r_\text{ff} \approx \max\!\left(\frac{2D^{2}}{\lambda},\ \frac{\lambda}{2\pi}\right)
$$

But do not read $\lambda/2\pi$ as "the far field begins here". At that radius the
stored terms are merely *equal* to the radiation term, not gone. In practice give
a small antenna **a few wavelengths** — $kr$ of order 10 — before you trust its
pattern.
:::
::::

::::{frame} Where 2D²/λ comes from
<img src="../../slides/fig/L05-phase-error.svg" alt="A spherical wavefront from a point source arriving across an aperture of size D, with the extra path length to the aperture edge marked">

The source sits at a finite distance, so the wavefront reaching the aperture is a
sphere, not a plane. The far-field distance is the range at which that sphere is
flat enough across $D$.
::::

::::{frame} The phase-error budget
Extra path from the source to the aperture **edge** over the path to its
**centre**:

$$
\Delta \approx \frac{(D/2)^{2}}{2r} = \frac{D^{2}}{8r}
$$

Tolerance: $\Delta \le \lambda/16$, a peak phase error of $22.5^{\circ}$
($\pi/8$). Set $\Delta = \lambda/16$:

$$
\frac{D^{2}}{8r} = \frac{\lambda}{16} \qquad\Longrightarrow\qquad r = \frac{2D^{2}}{\lambda}
$$

:::{callout}
$2D^{2}/\lambda$ is a **budget**, not a wall — inside it aperture phase distorts
the pattern, beyond it the pattern stops changing.
:::

:::{depth}
Picture a point source a distance $r$ away, radiating a **spherical** wavefront
onto an aperture of size $D$. Because the wavefront is a sphere, the path from
the source to the *edge* of the aperture is slightly longer than the path to the
*centre*. A plane wave, by definition, would have no such difference — and the
plane-wave limit is exactly what you earn once this criterion is met.

Inside this distance the phase across the aperture curves enough to distort the
pattern; beyond it the wavefront is "flat enough" and the pattern is stable. That
is the whole content of the criterion: a statement about how flat a sphere looks
over a finite width, not about where radiation starts.
:::
::::

::::{frame} Drive it yourself — the boundaries
:class: viz-frame

Hold $f$ and double $D$: the far-field distance goes up by **four**. Hold $D$ and
double $f$: it doubles.

<iframe class="viz" data-autosize="1" src="../../viz/field-regions.html" style="height:600px" title="Field-region explorer"></iframe>
::::

::::{frame} Worked example — a 1.2 m dish at 10 GHz
| Quantity | Work | Result |
| :-- | :-- | :-- |
| wavelength | $3\times10^{8} \div 10\times10^{9}$ | $0.03\ \text{m}$ |
| electrical size | $D/\lambda = 1.2 \div 0.03$ | $40$ — electrically large |
| reactive boundary | $0.62\sqrt{1.728 \div 0.03} = 0.62\sqrt{57.6}$ | $4.7\ \text{m}$ |
| far-field distance | $2(1.2)^{2} \div 0.03$ | $96\ \text{m}$ |
| radiating near-field | everything between | $4.7$ to $96\ \text{m}$ |

Almost a hundred metres of separation to measure a dish you can carry.

:::{depth}
Written out, so the arithmetic is checkable:

$$
\lambda = \frac{c}{f} = \frac{3\times10^{8}}{10\times10^{9}} = 0.03\ \text{m}
$$

$$
r_\text{ff} = \frac{2D^{2}}{\lambda} = \frac{2(1.2)^{2}}{0.03} = 96\ \text{m}
$$

$$
r_\text{reactive} = 0.62\sqrt{\frac{D^{3}}{\lambda}} = 0.62\sqrt{\frac{1.728}{0.03}} = 0.62\sqrt{57.6} \approx 4.7\ \text{m}
$$

Notice the $D^{2}$: go to 20 GHz and the far field starts at 192 m for the same
dish.
:::
::::

::::{frame} Which is why ranges are enormous
To measure a true pattern, gain, or sidelobe level, the antenna under test must
sit in the **far field** of the source — and the source in the far field of the
antenna.

- A large dish at high frequency wants **hundreds of metres** of clear, reflection-free range.
- Often impractical, sometimes impossible indoors.

So instead: measure close in, on a surface in the radiating near-field, and
propagate the result out mathematically — near-field scanning, in Module 2.

:::{depth}
The far-field distance is not academic — it sets the size of your test range.
That is exactly why **near-field scanning** exists: you measure the fields on a
surface *close* to the antenna, in the radiating near-field, then mathematically
propagate them out.

You will see this in Module 2's measurement lessons. But it only works because
the near-field distribution **completely determines** the far-field pattern —
which is the subject of the next lesson.
:::
::::

::::{frame} Key point
:::{callout}
Where you stand changes what you see. Close in, the field is **stored energy**
that never leaves. A bit farther out it **radiates, but the pattern is still
forming**. Only beyond $2D^{2}/\lambda$ does the antenna show its **true,
distance-independent pattern**.

Every gain number, every pattern plot, every sidelobe spec assumes you are out
there in the far field.
:::
::::

::::{frame} Summary
| Symbol / idea | What it is | Number to remember |
| :-- | :-- | :-- |
| Three field terms | One dipole equation holds all three regions | $1 : 1/kr : 1/(kr)^{2}$ |
| $kr = 1$ crossover | Where all three terms are *equal* — not where the far field starts | $r = \lambda/2\pi \approx 0.16\lambda$ |
| True far field | Reactive terms actually negligible | $kr \gg 1$; under 10% near $kr \approx 10$ ($r \approx 1.6\lambda$) |
| Reactive near-field edge | Inner boundary for an electrically large antenna | $r = 0.62\sqrt{D^{3}/\lambda}$ |
| Far-field distance | Outer boundary; pattern stops changing with $r$ | $r \ge 2D^{2}/\lambda$ |
| Phase-error tolerance | What the criterion $2D^{2}/\lambda$ comes from | $\Delta \le \lambda/16$, i.e. $\pi/8 = 22.5^{\circ}$ |
| Worked dish | $D = 1.2\ \text{m}$ at $10\ \text{GHz}$ | reactive to $4.7\ \text{m}$; far field beyond $96\ \text{m}$ |
::::

::::{frame} Practice
The set opens with a which-term-dominates part: evaluate the ratio
$1 : 1/kr : 1/(kr)^{2}$ at $kr = 0.1$ and $kr = 10$, and name the winner in each.
Do it by hand once and the crossover stops being a number to memorise.

- <a href="../../practice/ECE444_L05_Practice_blank.pdf" target="_blank" rel="noopener">Problem set (PDF)</a>
- <a href="../../practice/ECE444_L05_Practice_SOLUTIONS.pdf" target="_blank" rel="noopener">Solutions (PDF)</a>
::::

::::{frame} Where this is going
- You now know **where** the far-field pattern lives and how far away it starts.
- **L6 (Radiation Integrals)** answers **what** that pattern is: given the current on the antenna, one integral produces the far field directly.
- And the criterion comes back immediately — the quadratic term L6 has to throw away is **exactly** $\Delta \le \lambda/16$. Same $2D^{2}/\lambda$, derived from the other direction.

Same number, two stories. That is usually a sign you have the physics right.

:::{depth}
Watch for one specific move in that derivation. Expanding the distance from a
source point to the observer gives a linear term and a quadratic one, and
*throwing the quadratic term away* is what defines the far field. That discarded
term is the path difference $D^{2}/8r$ from this lesson, and the licence to drop
it is the $\pi/8$ tolerance.

So "the far-field approximation" in Lesson 6 and $r \ge 2D^{2}/\lambda$ here are
the same statement — one written as an integral, one as a distance.
:::
::::
