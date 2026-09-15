<!-- .slide: class="title-slide" -->

<div class="title-left">

# ECE 444

Antennas, Phased Arrays, and Radar Systems

## Lesson 5 — Field Regions

Fall 2026 · Dr. Neil Rogers

</div>

<div class="title-right">

![USAFA](./img/01-course-intro/USAFA-logo.png)

</div>

---

## Where we were

- **L2** — pattern, directivity, gain. Every one of those numbers was quoted *far away*, without ever saying so.
- **L3** — polarization and bandwidth of that same escaping wave.
- **L4** — the **terminals**: $Z_{\text{in}}$, reactance, stored energy the radio has to fight.

**Today we step outside the antenna. Where you stand changes what you measure.**

Note:
L4 looked into the terminals. Today we look out into the space around the
antenna and ask when the fields settle down into the pattern of L2.

---

## Today's plan

1. What **near** and **far** actually mean
2. The exact fields of one current element — **three terms, three powers of $r$**
3. The crossover at $kr = 1$ — and what it does *not* say
4. The **three regions** and their boundaries
5. Where $2D^{2}/\lambda$ comes from — a **phase-error budget**
6. Why an antenna range has to be so long

---

## Near and far

Walk away from a transmitting antenna and watch the field.

- **Near** — the field still remembers how the antenna is *built*. Its shape depends on how far out you are, and some of it never leaves at all.
- **Far** — the antenna has collapsed into a **point source**. The pattern shape stops changing with $r$; the amplitude just scales as $1/r$.

<div class="callout">
"The gain is 15 dBi" means <strong>in the far field</strong>. Every spec you will ever read carries that silent qualifier.
</div>

---

## Where the regions come from

The regions are not a convention someone imposed. Solve Maxwell exactly for the simplest antenna there is — an **infinitesimal dipole**, a current element $Idl$ along $\hat{\mathbf z}$ with $dl \ll \lambda$:

$$ E_\theta = \frac{jk\eta_0 Idl\sin\theta}{4\pi r}\left(1 + \frac{1}{jkr} - \frac{1}{(kr)^{2}}\right)e^{-jkr} $$

$$ H_\phi = \frac{jkIdl\sin\theta}{4\pi r}\left(1 + \frac{1}{jkr}\right)e^{-jkr} $$

**Current elements like this make up every antenna.** Whatever these fields do, real antennas do too — superposed.

---

## Read the fields by their powers of $r$

Multiply the bracket through and the field is a sum of three pieces:

$$ E_\theta \ \propto\ \frac{1}{r} \ +\ \frac{1}{kr^{2}} \ +\ \frac{1}{k^{2}r^{3}} $$

| Term | Falls off as | Physical origin | Wins where |
| :-- | :-- | :-- | :-- |
| radiation | $1/r$ | the escaping wave — L2's far field | $kr \gg 1$ |
| induction | $1/r^{2}$ | Biot–Savart field of the current | $kr \sim 1$ |
| electrostatic | $1/r^{3}$ | quasi-static field of the charge at the tips | $kr \ll 1$ |

<div class="callout">
Three regions, hiding inside one equation. The single number $kr$ sets their relative sizes <strong>entirely</strong>.
</div>

---

<!-- .slide: class="viz-cue-slide" -->

## The three terms, on log–log axes

<div class="fig" data-inline-svg="./fig/L05-term-crossover.svg" style="max-width:790px; margin:0 auto;"></div>

<p class="viz-cue">↗ Interactive on the lesson page</p>

Note:
Straight lines of slope −1, −2, −3. Drive the widget in and out and let them
watch which term is on top. Left of the crossover the stored field runs away;
right of it only radiation is left standing.

---

## The crossover is a single number

Radiation (size $1$ in the bracket) and induction (size $1/kr$) are equal when

$$ kr = 1 \qquad\Longrightarrow\qquad r = \frac{1}{k} = \frac{\lambda}{2\pi} \approx 0.16\lambda $$

- At $kr = 1$ all three terms are **the same size**. That is *all* it says.
- Reactive terms are negligible only for $kr \gg 1$: at $kr = 6$ — about one wavelength out — induction is down to $17\%$ and the electrostatic term to $3\%$.

<div class="callout">
$kr = 1$ is the <strong>crossover</strong>, not the start of the far field. For a small antenna the far field is usable from roughly a wavelength out, not from $0.16\lambda$.
</div>

Note:
This is the slide students get wrong on the GR. Equality is not negligibility.

---

## Why "reactive" is the literal word

Form the complex radial Poynting vector and the cross-terms collapse to just two:

$$ \frac{1}{2}E_\theta H_\phi^{\ast} \ \propto\ \frac{1}{r^{2}} \ -\ j\frac{1}{k^{3}r^{5}} $$

- **Real part** — genuine outward power, falling as $1/r^{2}$, the inverse-square law. It contains **no near-field terms at all**: radiation is radiation at every distance.
- **Imaginary part** — reactive power, falling as $1/r^{5}$. The $j$ says $\mathbf E$ and $\mathbf H$ sit $90^{\circ}$ apart: energy flows out for a quarter cycle, then all the way back. **Nothing leaves.**

<div class="callout">
The same reactive power you met at the terminals in L4 — now seen from <em>outside</em> the antenna instead of inside it.
</div>

---

## The three regions

<div class="fig" data-inline-svg="./fig/L05-region-diagram.svg" style="max-width:790px; margin:0 auto;"></div>

---

## Reactive near-field

Right up against the antenna the field is **stored energy**, not radiation — the $1/r^{2}$ and $1/r^{3}$ terms, sloshing in and out each cycle.

- Like the field around a charged capacitor or a current-carrying inductor.
- Put a receiver here and it **loads the antenna** and changes its behavior.
- Which is also why you keep hands, heads, and hardware out of it.

**It falls off fast. Take one step out and it is gone.**

---

## Radiating near-field (Fresnel)

Energy is now leaving — **but the shape of the pattern still depends on how far away you are.**

- Different parts of the antenna are at meaningfully different distances from your observation point.
- Their contributions add with **distance-dependent phase**, so the angular pattern keeps changing as you move out.
- The wavefront is noticeably **curved**.

<div class="callout">
Measure a pattern here and you have measured <em>this range</em>, not the antenna.
</div>

---

## Far-field (Fraunhofer)

Far enough out, the antenna looks like a **point source**:

- fields fall as $1/r$, power as $1/r^{2}$
- $\mathbf E$, $\mathbf H$, and the direction of propagation are mutually perpendicular
- locally the wave is a **plane wave** — flat wavefront

**Measure at $100\ \text{m}$ or at $1\ \text{km}$ and you get the same angular pattern, just weaker.**

---

## The boundaries

Let $D$ be the antenna's **largest dimension** and $\lambda$ the wavelength:

$$ r < 0.62\sqrt{\frac{D^{3}}{\lambda}} \qquad 0.62\sqrt{\frac{D^{3}}{\lambda}} \le r < \frac{2D^{2}}{\lambda} \qquad r \ge \frac{2D^{2}}{\lambda} $$

| Region | Extent | Fields |
| :-- | :-- | :-- |
| reactive near-field | $r < 0.62\sqrt{D^{3}/\lambda}$ | stored, non-radiating; $1/r^{2}$, $1/r^{3}$ |
| radiating near-field | up to $2D^{2}/\lambda$ | radiating, but pattern varies with $r$ |
| far-field | $r \ge 2D^{2}/\lambda$ | pattern fixed; $1/r$; locally a plane wave |

**Not walls — the fields transition gradually.**

---

## Careful: these are for *large* antennas

Both formulas assume an **electrically large** antenna, $D > \lambda$ — the regime where $2D^{2}/\lambda$ means anything.

For a **small** antenna it can come out smaller than a wavelength, which is nonsense: the reactive near field runs to about $\lambda/2\pi$, the $kr = 1$ crossover we derived:

$$ r_{\text{ff}} \approx \max\left(\frac{2D^{2}}{\lambda},\ \frac{\lambda}{2\pi}\right) $$

<div class="callout">
At $\lambda/2\pi$ the stored terms are merely <em>equal</em>, so give a small antenna <strong>a few wavelengths</strong> before you trust the pattern.
</div>

---

## Where $2D^{2}/\lambda$ comes from

<div class="fig" data-inline-svg="./fig/L05-phase-error.svg" style="max-width:790px; margin:0 auto;"></div>

Note:
The source is at a finite distance, so the wavefront reaching the aperture is a
sphere, not a plane. The far-field distance is the range at which that sphere is
flat enough across D.

---

## The phase-error budget

Extra path from the source to the aperture **edge** over the path to its **center**:

$$ \Delta \approx \frac{(D/2)^{2}}{2r} = \frac{D^{2}}{8r} $$

Tolerance: $\Delta \le \lambda/16$, a peak phase error of $22.5^{\circ}$ ($\pi/8$). Set $\Delta = \lambda/16$:

$$ \frac{D^{2}}{8r} = \frac{\lambda}{16} \qquad\Longrightarrow\qquad r = \frac{2D^{2}}{\lambda} $$

<div class="callout">
$2D^{2}/\lambda$ is a <strong>budget</strong>, not a wall — inside it aperture phase distorts the pattern, beyond it the pattern stops moving.
</div>

---

## Worked example — a 1.2 m dish at 10 GHz

| Quantity | Work | Result |
| :-- | :-- | :-- |
| wavelength | $3\times10^{8} / 10\times10^{9}$ | $0.03\ \text{m}$ |
| electrical size | $D/\lambda = 1.2/0.03$ | $40$ — electrically large ✓ |
| reactive boundary | $0.62\sqrt{1.728/0.03} = 0.62\sqrt{57.6}$ | $4.7\ \text{m}$ |
| far-field distance | $2(1.2)^{2}/0.03$ | $\mathbf{96\ m}$ |
| radiating near-field | everything between | $4.7$ to $96\ \text{m}$ |

**Almost a hundred meters of separation to measure a dish you can carry.**

Note:
Have them notice the D-squared: go to 20 GHz and the far field starts at 192 m,
for the same dish.

---

## Which is why ranges are enormous

To measure a true pattern, gain, or sidelobe level, the antenna under test must sit in the **far field** of the source — and the source in the far field of the antenna.

- A large dish at high frequency wants **hundreds of meters** of clear, reflection-free range.
- Often impractical, sometimes impossible indoors.

**So instead: measure close in, on a surface in the radiating near-field, and propagate the result out mathematically — near-field scanning, in Module 2.**

Note:
Near-field scanning works only because the far-field pattern is completely
determined by the near-field distribution — which is exactly what L6 sets up.

---

<!-- .slide: class="viz-cue-slide" -->

## Drive it yourself

Set $D$ and the frequency; watch the two boundaries slide along the distance axis, with the phase error across the aperture shown alongside.

- Hold $f$ fixed and double $D$: the far-field distance goes up by **four**.
- Hold $D$ fixed and double $f$: it doubles.
- Shrink $D$ below a wavelength and watch $2D^{2}/\lambda$ stop being the useful number.

<p class="viz-cue">↗ Interactive on the lesson page</p>

Note:
Run the field-region explorer live. Do the doubling demos in that order — the
D-squared scaling is the one thing from this lesson they will use in the lab.

---

## Key point

<div class="callout">
<p>Where you stand changes what you see. Close in, the field is <strong>stored energy</strong> that never leaves. A bit farther out it <strong>radiates, but the pattern is still forming</strong>. Only beyond $2D^2/\lambda$ does the antenna show its <strong>true, distance-independent pattern</strong>.</p>
<p>Every gain number, every pattern plot, every sidelobe spec assumes you are out there in the far field.</p>
</div>

---

## Where this is going

- You now know **where** the far-field pattern lives and how far away it starts.
- **L6 (Radiation Integrals)** answers **what** that pattern is: given the current on the antenna, one integral produces the far field directly.
- And the criterion comes back immediately — the quadratic term L6 has to throw away to make that integral tractable is **exactly** $\Delta \le \lambda/16$. Same $2D^{2}/\lambda$, derived from the other direction.

**Same number, two stories. That is usually a sign you have the physics right.**
