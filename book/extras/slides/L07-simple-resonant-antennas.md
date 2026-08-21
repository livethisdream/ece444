<!-- .slide: class="title-slide" -->

<div class="title-left">

# ECE 444

Antennas, Phased Arrays, and Radar Systems

## Lesson 7 — Simple Resonant Antennas

Fall 2026 · Dr. Neil Rogers

</div>

<div class="title-right">

![USAFA](./img/01-course-intro/USAFA-logo.png)

</div>

---

## Where we were

- **L5** — the far field starts at $r \ge 2D^2/\lambda$, and only there does the pattern stop changing with range.
- **L6** — the far-field pattern is the radiation integral of the current: assume a current, transform it, read the pattern.
- **L6** also handed you the half-wave dipole pattern from an assumed sinusoidal current.
- **L4** — matching, VSWR, and baluns. You now need all three on the same antenna.

**Today: two antennas — one that cannot exist, and one you can cut with a tape measure.**

Note:
Frame the lesson as cashing in L6. We did the integral; now we spend the answer on a real piece of wire.

---

## Today's plan

1. The isotropic radiator — why the reference antenna is a fiction, and why every gain spec still needs it.
2. The short dipole, in one slide, as the limiting case.
3. The half-wave dipole: current, pattern, beamwidth, directivity.
4. Impedance and resonance — why a resonant wire is short of $\lambda/2$.
5. Longer dipoles, and where the lobes come from.
6. Cut one for 146 MHz and predict what the analyzer will read.

Note:
Item 6 is the deliverable. Everything before it is the machinery.

---

## The isotropic radiator

An antenna that radiates **equally in every direction**. Same power density on every square meter of a sphere around it.

$$U_\text{iso} = \frac{P_\text{rad}}{4\pi} \qquad D_\text{iso} = 1 \qquad 0 \text{ dBi}$$

- It cannot be built. In the far field $\mathbf{E}$ is transverse, so it is *tangential* to that sphere — and the hairy-ball theorem forbids a nonvanishing tangential field everywhere on a sphere.
- Somewhere the field must go to zero. That is a null, and **every real antenna has at least one**.
- It survives anyway as the **unit of comparison**: directivity is defined as a ratio against it.

**It is not a product. It is a reference, baked into every gain number you will ever quote.**

Note:
Ask whether anyone has ever bought one, then ask why the datasheet still says dBi. Keep the hairy-ball argument to 60 seconds — the physics point that matters is that a null is not a defect, it is a topological requirement.

---

## What the fiction buys you

| Quantity | Meaning | Reference |
| :-- | :-- | :-- |
| dBi | gain over isotropic | the fiction |
| dBd | gain over a half-wave dipole | a real antenna |
| EIRP | $P_t G_t$, as if radiated isotropically | the fiction |

$$\text{dBi} = \text{dBd} + 2.15 \qquad \text{EIRP} = P_t G_t$$

<div class="callout">
EIRP collapses a transmitter and its antenna into <strong>one number</strong> that a link budget or a spectrum authority can regulate. That is worth an antenna that cannot be built.
</div>

Note:
5 W into a half-wave dipole is 8.2 W EIRP, or 39.1 dBm. The power is the same and the number is bigger because the energy is no longer spread in every direction.

---

## The short dipole, in one slide

A wire much shorter than a wavelength, $L \ll \lambda$. The current tapers linearly from the feed to zero at the ends.

- Pattern: $\vert F(\theta) \vert = \sin\theta$ — a doughnut, broadside at $\theta = 90^\circ$.
- HPBW $= 90^\circ$, $D = 1.5$ (**1.76 dBi**).
- Radiation resistance $R_r = 80\pi^2 (L/\lambda)^2$ — about $2\ \Omega$ at $L = 0.1\lambda$.

**The pattern is already almost as good as it gets. The impedance is the problem.**

Note:
This is the L6 result, recalled not re-derived. Two ohms against a fifty ohm line is the whole reason nobody feeds a short dipole directly.

---

## Where the current comes from

<div class="fig" data-inline-svg="./fig/L07-dipole-currents.svg" style="max-width:700px; margin:0 auto; display:block;"></div>

$$I(z) = I_m \sin\left[k\left(\frac{L}{2} - \vert z \vert\right)\right]$$

- Tips $z = \pm L/2$: sine argument zero, **current vanishes**.
- Feed: $I(0) = I_m \sin(kL/2)$ — a *maximum* at $\lambda/2$, a *null* at $1\lambda$.

Note:
Build it on the board: open-circuited two-wire line, current zero at the open end, then fold the last stretch apart into two arms and the standing wave comes with it. Then say it out loud: this current is assumed, not solved for. It is a very good guess with a transmission-line pedigree, confirmed by measurement, but it is not a solution of Maxwell's equations for a dipole — and everything downstream in this lesson inherits it. L8 is where they find out what the guess costs. Flag the feed-point contrast now, maximum at half a wave versus null at a full wave, because it decides the impedance story in Part 4.

---

## Step 1: set up the radiation integral

L6's radiation vector, for a thin wire on $z$ where $\hat{\mathbf r}\cdot\mathbf{r}' = z'\cos\theta$:

$$N_z(\theta) = \int_{-L/2}^{L/2} I(z')\ e^{+jkz'\cos\theta}\ dz'$$

The current is **even** in $z'$. Pair $z'$ with $-z'$, the two exponentials combine into a cosine, and the integral folds onto one arm:

$$N_z(\theta) = 2 I_m \int_0^{L/2} \sin\left[k\left(\frac{L}{2} - z'\right)\right]\cos(kz'\cos\theta)\ dz'$$

**No approximation has entered yet — this step is only symmetry.**

Note:
Do this one live on the board — it is the only antenna in the course where the whole machine runs end to end, and seeing it once is what makes L6 stick. Write the radiation vector, then ask them what makes the dot product collapse to z prime cos theta. Draw the pairing of plus z prime with minus z prime and let them tell you the exponentials become a cosine. Emphasize that folding by symmetry is free and that it also kills the imaginary part — students who grind through the full complex integral get the same answer with three times the algebra.

---

## Step 2: evaluate it

Product-to-sum turns the integrand into two plain sines:

$$\sin A \cos B = \frac{1}{2}\left[\sin(A+B) + \sin(A-B)\right]$$

Both integrate directly. Collecting terms:

$$N_z(\theta) = \frac{2 I_m}{k}\ \frac{\cos\left(\frac{kL}{2}\cos\theta\right) - \cos\frac{kL}{2}}{\sin^2\theta}$$

<div class="callout">
The calculus is elementary. The hard part was choosing the current.
</div>

Note:
Put the identity up, integrate the two sines in front of them, and evaluate at the limits — it is about four lines and worth every one of them. If the class is following easily, hand them the collecting step and let them find the two cosines themselves. The point to land: the integral is elementary once the current is sinusoidal, and that is exactly why the sinusoidal assumption is worth making.

---

## Step 3: project and normalize

A $z$-directed current radiates only a $\theta$ component. L6's projection costs one power of $\sin\theta$:

$$N_\theta = -N_z \sin\theta \quad \Longrightarrow \quad \vert F(\theta) \vert \propto \left\vert \frac{\cos\left(\frac{kL}{2}\cos\theta\right) - \cos\frac{kL}{2}}{\sin\theta} \right\vert$$

The bars are there because the bracket flips sign past $L = \lambda$. The proportionality is there because normalizing divides by the peak — at broadside that is $1 - \cos\frac{kL}{2}$, which is **1** at $\lambda/2$ but **2** at $1\lambda$.

At $L = \lambda/2$ the second cosine vanishes and the peak is exactly 1, so this one is already normalized:

$$\vert F(\theta) \vert = \frac{\cos\left(\frac{\pi}{2}\cos\theta\right)}{\sin\theta}$$

**One integral covers every length — the multi-lobe patterns later come from this same formula.**

Note:
Finish the derivation here, then stop and point at what is on the board. This is the payoff for the whole radiation-integral thread that started in L6: assumed a current, transformed it, projected it, read the pattern. Say the two warnings out loud as you write them — the bars because the bracket flips sign past a full wavelength, the proportionality because normalizing divides by the broadside peak and that peak is one at half a wavelength but two at a full wavelength, so only the half-wave case comes out already normalized. Then the closing line: nothing about any of this was half-wave specific until the last step.

---

## So why half a wavelength?

<div class="callout">
The reason is not the pattern; it is the <strong>impedance</strong>. At $\lambda/2$ the current maximum sits at the feed, the radiation resistance climbs to ~73 Ω, and the wire will accept power from an ordinary line without a matching network.
</div>

$$Z_{\text{in}} \approx 73 + j42.5\ \Omega$$

- Short dipole: $2\ \Omega$ — hopeless. Half-wave: $73\ \Omega$, and a 75 Ω line nearly matches it.
- The resistive part is real radiation. The **+42.5 Ω is inductive** — stored energy sloshing in the near field, pure nuisance.

**Resonance means $X_{\text{in}} = 0$. At exactly half a wavelength we are 42.5 Ω away from it.**

Note:
This is the slide students remember: the half-wave dipole is famous for its input impedance, not its 2.15 dBi. Point back to L5's reactive near-field region — that stored energy is exactly the near-field term that never made it into the far field. Nothing is wrong with the antenna; it simply is not resonant at exactly half a wavelength.

---

## Where the 73 ohms comes from

Radiation resistance is whatever resistor would burn the power the antenna radiates:

$$P_\text{rad} = \frac{1}{2}\vert I_m \vert^2 R_r$$

Take Part 3's pattern, square it, and add it up over the sphere. Nothing depends on $\phi$, so azimuth just hands you a $2\pi$:

$$P_\text{rad} = \frac{\eta_0 \vert I_m \vert^2}{4\pi}\int_0^\pi \frac{\cos^2\left(\frac{\pi}{2}\cos\theta\right)}{\sin\theta}\ d\theta$$

<div class="callout">
That integral has <strong>no elementary antiderivative</strong>. This is where a <em>number</em> enters the lesson instead of a formula.
</div>

Note:
Nothing new is assumed here — it is the same pattern from Part 3, squared and summed over the sphere. The current amplitude will cancel, so it never needed a value. The integral is the cosine integral Cin: the integral of one minus cos u, over u, from zero to x. Look it up or evaluate it numerically.

---

## The result: 73 ohms

$$\int_0^\pi \frac{\cos^2\left(\frac{\pi}{2}\cos\theta\right)}{\sin\theta}\ d\theta = \frac{1}{2}C_{in}(2\pi) = 1.2188$$

| Quantity | Work | Result |
| :-- | :-- | :-- |
| $C_{in}(2\pi)$ | twice the integral | $2.4376$ |
| $\eta_0/4\pi$ | $377/4\pi$ | $29.98 \approx 30$ |
| $R_r$ | $\left(\eta_0/4\pi\right) C_{in}(2\pi)$ | $\mathbf{73.1\ \Omega}$ |

<div class="callout">
This resistance is referred to the <strong>current maximum</strong>, which at $\lambda/2$ <em>is</em> the feed. That coincidence is the only reason this lands on the input resistance.
</div>

Note:
Thirty times two point four is seventy-two, so a head check catches a slipped factor. Then the two warnings. First: R sub r came out referred to the current maximum, because I sub m is the current-maximum amplitude. At half a wavelength the current maximum sits at the feed, so radiation resistance and input resistance are the same number — that coincidence is the only reason this lands on the input impedance. Second: a far-field power integral accounts for power that leaves, so it can never produce stored near-field energy. The forty-two point five ohms of reactance requires the induced-EMF method, a near-field calculation, and we take it on faith.

---

## What the induced-EMF method does

A far-field power integral counts only what **leaves**. Reactance is energy stored close to the wire and handed back every cycle — it never crosses the far-field sphere, so no pattern integral can reveal it.

The induced-EMF method works where that energy actually is:

1. Take the current on the wire — the same assumed standing wave.
2. Compute the electric field **that current produces back at the wire itself**, in the near field.
3. Integrate that field against the current, along the wire.

<div class="callout">
That product is a complex power: <strong>real part = radiated power, imaginary part = stored energy.</strong> It is near-field bookkeeping, done at the antenna instead of on a distant sphere.
</div>

Note:
The physical picture: an antenna induces a voltage back along itself, hence induced EMF. Integrating field against current gives complex power, and the imaginary part is exactly the reactive energy a far-field integral throws away. Worth saying that it reproduces the seventy-three ohms as its real part, which is a good consistency check on both methods.

---

## The reactance, and why 42.5 is clean

The general result contains the wire radius, so **a dipole's reactance normally depends on how thick the wire is**. But every term carrying the radius is multiplied by $\sin(kL)$, and at $kL = \pi$ that factor is **zero**:

$$X = \frac{\eta_0}{4\pi}Si(2\pi) = 30 \times 1.4182 = 42.5\ \Omega$$

$$Z_{\text{in}} = \frac{\eta_0}{4\pi}\left[C_{in}(2\pi) + j\ Si(2\pi)\right] = 73.1 + j42.5\ \Omega$$

<div class="callout">
The reactance is radius-independent <strong>only at exactly $\lambda/2$</strong>, which is why 42.5 is quotable at all.
</div>

Note:
Induced EMF means integrating the antenna's own field back against its own current — a near-field calculation, and we take its result on faith. This slide also explains the next figure before they see it: the three wire-thickness curves cross at exactly half a wavelength and separate everywhere else. That crossing is the sine of pi being zero. Note too that the reactance inherits the assumed sinusoidal current, so it is the number L8's solver will disagree with first.

---

## Trim it short

<div class="fig" data-inline-svg="./fig/L07-dipole-resonance.svg" style="max-width:620px; margin:0 auto; display:block;"></div>

These are **computed data, not a sketch**: the induced-EMF expression evaluated at hundreds of lengths, for three wire radii, and plotted.

Note:
Say plainly how the figure was made — sweep the length, sweep the wire radius, evaluate the induced-EMF impedance at every combination, plot the answers. Nothing here is drawn by hand. Then watch the zero crossing move left as the element gets fatter: that is the whole story of why a real dipole is never exactly half a wavelength. Note also that all three curves meet at exactly half a wavelength, which is the sine of pi being zero from the previous slide. Ask them why the crossing moves before you advance — the next slide is the answer.

---

## Why shorter, physically

The wire is a **resonant standing-wave structure**, and its ends are not electrically where they look.

- **End effect** — capacitance between the tips and to whatever is nearby stores charge past the physical end, so the wave "sees" more wire than there is.
- **Wire thickness** — a fatter element has more end capacitance and a lower characteristic impedance, so it shortens further.
- Both effects **slow the wave** on the wire relative to free space.

**Practical resonance lands at $0.47\lambda$ to $0.48\lambda$; a fat element goes below that.**

Note:
This is the physical answer to the previous figure. An insulated wire shortens further still, because the dielectric slows the wave; hams call the whole thing the velocity factor. Tie it back to L4: the wire behaves like a slightly slow transmission line, and everything you know about electrical length applies.

---

## The design rule of thumb

$$L_\text{resonant} \approx 0.95 \times \frac{\lambda}{2} = 0.475\ \lambda$$

With $\lambda = c/f$, that is the number every field manual prints:

$$L \approx \frac{143}{f_\text{MHz}} \text{ meters} \qquad \left(\frac{468}{f_\text{MHz}} \text{ feet}\right)$$

<div class="callout">
Cut it <strong>long</strong> and trim. You can always remove wire.
</div>

Note:
The 5% is an average. It depends on wire gauge, insulation, and what is nearby — which is exactly why you trim rather than compute to four digits.

---

## What the match looks like

At resonance the reactance is gone and the resistance settles near $70\ \Omega$:

| Feed line | $Z_{\text{in}}$ used | $\vert \Gamma \vert$ | VSWR |
| :-- | :-- | :-- | :-- |
| 50 Ω | $73 + j42.5$ | 0.37 | 2.18 |
| 50 Ω | $70 + j0$ | 0.17 | **1.40** |
| 75 Ω | $73 + j42.5$ | 0.28 | 1.76 |
| 75 Ω | $70 + j0$ | 0.03 | **1.07** |

<div class="callout">
<strong>Trimming to resonance is worth more than changing the cable.</strong> Removing the reactance takes 2.18 to 1.40. Changing the cable instead takes 2.18 to 1.76.
</div>

Note:
Make them read the table as a decision: the reactance costs more VSWR than the fifty-versus-seventy-five mismatch does. Kill the reactance first, worry about the resistance second.

---

## The same four rows, on a Smith chart

<p class="viz-cue">↗ Interactive on the lesson page</p>

<div class="two-col fig-wide"><div class="col-text">
<p>Center is a perfect match, rim is total reflection, top half inductive, bottom half capacitive.</p>
<p>The dipole traces a path as the wire grows. <strong>Exactly $\lambda/2$</strong> sits in the inductive half, outside the 2:1 circle. <strong>Trimming</strong> walks it down onto the axis and inside 2:1.</p>
<p>Re-normalize to $75\ \Omega$ and the antenna does not move — <em>the grid does</em>.</p>
</div><div class="col-fig">
<div class="fig" data-inline-svg="./fig/L07-smith-dipole.svg" style="max-width:760px; margin:0 auto;"></div>
</div></div>

Note:
Demo live: park at half a wavelength, read seventy-three plus j forty-two point five, note it is outside the two-to-one circle. Trim to resonance and watch it cross onto the real axis. Then flip to seventy-five ohms and make the point that a match is a property of a pair, not of an antenna. Every VNA in the lab draws this chart, so they need to be fluent.

---

## Make it longer

<p class="viz-cue">↗ Interactive on the lesson page</p>

Past $\lambda/2$ the standing wave **reverses phase** along the wire. Reversed current radiates out of step, interference does the rest, and each reversal buys a new pair of lobes.

<div class="fig" data-inline-svg="./fig/L07-dipole-patterns.svg" style="max-width:1000px; margin:0 auto;"></div>

Note:
Demo the widget here: drag from 0.5 to 1.5 and watch the reversals appear one at a time. At a full wave the pattern is still broadside, narrower, and 3.8 dBi. At 1.25 wavelengths the broadside lobe is as good as it gets. At 1.5 the main lobes have walked off broadside entirely.

---

## Directivity and resistance against length

<div class="fig" data-inline-svg="./fig/L07-dipole-vs-length.svg" style="max-width:620px; margin:0 auto;"></div>

Note:
Two curves carry two lessons. Directivity peaks near 1.25 wavelengths at about 5.2 dBi. Resistance sweeps through 50 ohms twice before the wire is a wavelength long — which is why non-resonant lengths are hard to match.

---

## The numbers worth memorizing

| Length | HPBW | Directivity | $R$ at current max |
| :-- | :-- | :-- | :-- |
| short | $90^\circ$ | 1.76 dBi | $\approx 2\ \Omega$ |
| $0.5\lambda$ | $78^\circ$ | **2.15 dBi** | $73\ \Omega$ |
| $1.0\lambda$ | $48^\circ$ | 3.82 dBi | $199\ \Omega$ |
| $1.25\lambda$ | $33^\circ$ | 5.16 dBi | $106\ \Omega$ |
| $1.5\lambda$ | — | 3.48 dBi | $105\ \Omega$ |

**Below $\lambda/2$ nothing changes. Above $1.25\lambda$ the beam falls apart.**

Note:
At 1.5 wavelengths the main lobes are off broadside, so a single broadside HPBW is meaningless. Say that out loud.

---

## Worked example: cut one for 146 MHz

| Quantity | Work | Result |
| :-- | :-- | :-- |
| Wavelength | $3\times 10^8 / 146\times 10^6$ | $2.055\ \text{m}$ |
| Half wave | $\lambda/2$ | $1.027\ \text{m}$ |
| Trimmed | $0.475\lambda$ | $\mathbf{0.976\ m}$ |
| Each arm | half of that | $48.8\ \text{cm}$ |
| Check | $143 / 146$ | $0.980\ \text{m}$ |

**The whole design is two 49 cm arms.**

Note:
Have them notice the two routes agree to a centimeter. Also note that 49 cm is a length you can eyeball, which is the point of a rule of thumb.

---

## What the analyzer should read

| Quantity | Prediction | Confidence |
| :-- | :-- | :-- |
| $Z_{\text{in}}$ | $\approx 70 + j0\ \Omega$ | good |
| VSWR on 50 Ω | $\approx 1.4$ | good |
| Gain | $2.15$ dBi, less conductor loss | good |
| HPBW | $\approx 78^\circ$ | good |
| Far-field range | $2D^2/\lambda = 0.93\ \text{m}$ | from L5 |

**A dipole is balanced and coax is not — fit L4's balun, then trust the table. If the analyzer disagrees by more than about 10%, suspect the balun before the theory.**

Note:
$D$ here is the dipole length, 0.976 m, so $2D^2/\lambda$ is 0.93 m. Anything measured closer than a meter is not a pattern. On the balun: connect coax straight to a dipole and current flows on the outside of the shield, the feedline joins the radiating structure, and the pattern and VSWR both start depending on where you are standing. It is the number one reason a student's measured pattern will not match their simulation in L8 and L14.

---

## Drive it yourself

<p class="viz-cue">↗ Interactive on the lesson page</p>

The dipole explorer sweeps $L/\lambda$ from 0.05 to 1.5 and computes, by numerical integration, the current, the pattern, the beamwidth, the directivity, and the feed-point resistance and reactance.

- Park it at $0.50$: **78.1°, 2.15 dBi, 73.1 Ω, +42.5 Ω**.
- Back off to $0.474$: the reactance crosses zero.
- Switch the wire to **fat**: resonance moves to $0.461\lambda$.

Note:
Do the fat-wire demo live. It makes the shortening rule feel like physics instead of a fudge factor.

---

## Key points

- A dipole's **pattern** is set by how many wavelengths of current fit on the wire.
- Its **impedance** is set by where the current maximum sits relative to the feed.
- Half a wavelength is the useful length because it puts the current maximum at the feed. It costs only 0.39 dB of directivity to get there.
- The resistance comes from a far-field power integral; the reactance does not and cannot.
- A resonant dipole is about $0.475\lambda$, near $70\ \Omega$, $2.15\ \text{dBi}$, $78^\circ$ wide.
- Every number here rests on the assumed sinusoidal current.

Note:
Walk down the list. The last bullet is the bridge to L8 — every number on this slide is a prediction from a model, and next lesson they test it.

---

## Where this is going

- **L8** — you build this exact antenna in **4nec2**, a front end to NEC-2. It *does not assume a current*: it chops the wire into segments, solves for the current on each, then runs the same radiation integral you ran today. **The numbers you just predicted are the ones you will check against simulation.**
- **L9** — cut the dipole in half and stand it on a ground plane, then bend one into a loop.
- **Module 3** — a dipole becomes an *element*. Put many in a row and pattern multiplication takes over from 2.15 dBi.

**Bring the 146 MHz numbers to L8. You are going to grade the simulator with them.**

Note:
They should not meet the name cold next lesson. Method of moments in one sentence: turn the integral equation into a matrix equation, invert it, get the current. This lesson assumed the current and everything followed; NEC solves for it, and where the two disagree, the assumption is what is being measured. Set the expectation now: NEC will not return exactly 73 ohms, and that gap is itself the lesson.
