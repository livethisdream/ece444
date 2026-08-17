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

An antenna that radiates **equally in every direction**. Same power density on every square metre of a sphere around it.

$$U_\text{iso} = \frac{P_\text{rad}}{4\pi} \qquad D_\text{iso} = 1 \qquad 0 \text{ dBi}$$

<div class="callout">
It is the <strong>unit of comparison</strong>, not a product. Directivity is defined as a ratio against it, so the isotropic radiator is baked into every gain number you will ever quote.
</div>

Note:
Ask: has anyone bought one? No. Then ask why the datasheet still says dBi.

---

## Why it cannot exist

A truly isotropic radiator would need a **uniform outward vector field** on a sphere with no direction picked out.

- The hairy-ball theorem forbids a nonvanishing tangential field everywhere on a sphere.
- $\mathbf{E}$ is transverse in the far field — so it *is* tangential.
- Somewhere on the sphere, the field must go to zero. That is a null.

**Every real antenna has at least one null. The isotropic radiator has none, so it is not an antenna.**

Note:
Keep it to 60 seconds. The physics point that matters: a null is not a defect, it is a topological requirement.

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
5 W into a half-wave dipole is 8.2 W EIRP — 39.1 dBm. Same power, bigger number, because the energy is not going everywhere.

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

## The half-wave dipole: the current

<div class="fig" data-inline-svg="./fig/L07-dipole-currents.svg" style="max-width:900px; margin:0 auto;"></div>

$$I(z) = I_m \sin\left[k\left(\frac{L}{2} - \vert z \vert\right)\right]$$

Note:
Standing wave on an open-circuited transmission line, bent straight. Zero at the ends because the charge has nowhere to go.

---

## From current to pattern

Feed that current to the radiation integral from L6 and the $z$-integral closes in elementary functions:

$$\vert F(\theta) \vert = \frac{\cos\left(\dfrac{kL}{2}\cos\theta\right) - \cos\dfrac{kL}{2}}{\sin\theta}$$

At $L = \lambda/2$, $kL/2 = \pi/2$, the second cosine vanishes:

$$\vert F(\theta) \vert = \frac{\cos\left(\dfrac{\pi}{2}\cos\theta\right)}{\sin\theta}$$

Note:
Emphasize that nothing new happened here. One integral, one trig identity. The $\sin\theta$ in the denominator looks alarming but the numerator vanishes with it.

---

## Reading the pattern

<div class="two-col fig-wide"><div class="col-text">
<p>Still a doughnut, broadside at $\theta = 90^\circ$, nulls straight off the wire ends.</p>
<p>$$\theta_\text{HP} = 78^\circ$$</p>
<p>$$D = 1.64 = 2.15 \text{ dBi}$$</p>
<p><strong>Only 0.39 dB better than the short dipole.</strong> Doubling the wire barely sharpened the beam — it went from $90^\circ$ to $78^\circ$.</p>
</div><div class="col-fig">
<div class="fig" data-inline-svg="./fig/L07-halfwave-pattern.svg" style="max-width:620px; margin:0 auto;"></div>
</div></div>

Note:
The obvious question: so why bother with half a wavelength? Answer on the next slide — it is not about the pattern.

---

## So why half a wavelength?

<div class="callout">
Not for the pattern. For the <strong>impedance</strong>. At $\lambda/2$ the current maximum sits at the feed, the radiation resistance climbs to ~73 Ω, and the wire will accept power from an ordinary line without a matching network.
</div>

- Short dipole: $2\ \Omega$ — hopeless.
- Half-wave dipole: $73\ \Omega$ — a 75 Ω line is nearly a perfect match.

**Resonance is a feed-point convenience, not a radiation improvement.**

Note:
This is the slide students remember. The half-wave dipole is famous for its input impedance, not its 2.15 dBi.

---

## Input impedance at exactly $\lambda/2$

$$Z_{in} \approx 73 + j42.5\ \Omega$$

- The resistive part is real radiation — power leaving, never to return.
- The **+42.5 Ω is inductive**, and it is pure nuisance: stored energy sloshing in the near field.
- Nothing is wrong with the antenna. It simply is not resonant at exactly half a wavelength.

**Resonance means $X_{in} = 0$. We are 42.5 Ω away from it.**

Note:
Point back to L5's reactive near-field region. That stored energy is exactly the near-field term that never made it into the far field.

---

## Trim it short

<div class="fig" data-inline-svg="./fig/L07-dipole-resonance.svg" style="max-width:660px; margin:0 auto;"></div>

Note:
Watch the zero crossing move left as the element gets fatter. That is the whole story of why a real dipole is never exactly half a wavelength.

---

## Why shorter, physically

The wire is a **resonant standing-wave structure**, and its ends are not electrically where they look.

- **End effect** — capacitance between the tips and to whatever is nearby stores charge past the physical end, so the wave "sees" more wire than there is.
- **Wire thickness** — a fatter element has more end capacitance and a lower characteristic impedance, so it shortens further.
- Both effects **slow the wave** on the wire relative to free space.

**Practical resonance lands at $0.47\lambda$ to $0.48\lambda$; a fat element goes below that.**

Note:
An insulated wire shortens further still — the dielectric slows the wave. Hams call the whole thing the velocity factor.

---

## The design rule of thumb

$$L_\text{resonant} \approx 0.95 \times \frac{\lambda}{2} = 0.475\ \lambda$$

Which, with $\lambda = c/f$, is the number every field manual prints:

$$L \approx \frac{143}{f_\text{MHz}} \text{ metres} \qquad \left(\frac{468}{f_\text{MHz}} \text{ feet}\right)$$

<div class="callout">
Cut it <strong>long</strong> and trim. You can always remove wire.
</div>

Note:
The 5% is an average. It depends on wire gauge, insulation, and what is nearby — which is exactly why you trim rather than compute to four digits.

---

## What the match looks like

At resonance the reactance is gone and the resistance settles near $70\ \Omega$:

| Feed line | $Z_{in}$ used | $\vert \Gamma \vert$ | VSWR |
| :-- | :-- | :-- | :-- |
| 50 Ω | $73 + j42.5$ | 0.37 | 2.18 |
| 50 Ω | $70 + j0$ | 0.17 | **1.40** |
| 75 Ω | $73 + j42.5$ | 0.28 | 1.76 |
| 75 Ω | $70 + j0$ | 0.03 | **1.07** |

**Trimming to resonance is worth more than changing the cable.**

Note:
Make them read the table as a decision: the reactance costs you more VSWR than the 50-versus-75 mismatch does.

---

## One more thing before you connect it

A dipole is a **balanced** antenna. Coax is **unbalanced**.

- Connect them directly and current flows on the outside of the shield.
- The feedline becomes part of the antenna: pattern distorts, VSWR moves when you touch the cable.
- Fix from **L4**: a balun at the feed point.

**Every dipole measurement in this course gets a balun. No exceptions.**

Note:
This is the number one reason a student's measured pattern will not match their simulation in L8 and L14.

---

## Make it longer

<p class="viz-cue">↗ Interactive on the lesson page</p>

<div class="fig" data-inline-svg="./fig/L07-dipole-currents.svg" style="max-width:900px; margin:0 auto;"></div>

Past $\lambda/2$ the standing wave **reverses phase** along the wire. Reversed current radiates out of step — and interference does the rest.

Note:
Demo the widget here: drag from 0.5 to 1.5 and watch the reversals appear one at a time, each one buying a new pair of lobes.

---

## What the lobes do

<div class="fig" data-inline-svg="./fig/L07-dipole-patterns.svg" style="max-width:1000px; margin:0 auto;"></div>

Note:
Full wave: still broadside, narrower, 3.8 dBi. At 1.25 wavelengths the broadside lobe is as good as it gets. At 1.5 the main lobes have walked off broadside entirely.

---

## Directivity and resistance against length

<div class="fig" data-inline-svg="./fig/L07-dipole-vs-length.svg" style="max-width:620px; margin:0 auto;"></div>

Note:
Two curves, two lessons. Directivity peaks near 1.25 wavelengths at about 5.2 dBi. Resistance sweeps through 50 ohms twice before the wire is a wavelength long — which is why non-resonant lengths are a matching adventure.

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

**Two 49 cm arms. That is the whole design.**

Note:
Have them notice the two routes agree to a centimetre. Also: 49 cm is a length you can eyeball, which is the point of a rule of thumb.

---

## What the analyzer should read

| Quantity | Prediction | Confidence |
| :-- | :-- | :-- |
| $Z_{in}$ | $\approx 70 + j0\ \Omega$ | good |
| VSWR on 50 Ω | $\approx 1.4$ | good |
| Gain | $2.15$ dBi, less conductor loss | good |
| HPBW | $\approx 78^\circ$ | good |
| Far-field range | $2D^2/\lambda = 0.93\ \text{m}$ | from L5 |

**If the analyzer disagrees by more than about 10%, suspect the balun before the theory.**

Note:
$D$ here is the dipole length, 0.976 m, so $2D^2/\lambda$ is 0.93 m. Anything measured closer than a metre is not a pattern.

---

## Drive it yourself

<p class="viz-cue">↗ Interactive on the lesson page</p>

The dipole explorer sweeps $L/\lambda$ from 0.05 to 1.5 and computes — honestly, by integration — the current, the pattern, the beamwidth, the directivity, and the feed-point resistance and reactance.

- Park it at $0.50$: **78.1°, 2.15 dBi, 73.1 Ω, +42.5 Ω**.
- Back off to $0.474$: the reactance crosses zero.
- Switch the wire to **fat**: resonance moves to $0.461\lambda$.

Note:
Do the fat-wire demo live. It makes the shortening rule feel like physics instead of a fudge factor.

---

## Key point

<div class="callout">
<p>A dipole's <strong>pattern</strong> is set by how many wavelengths of current fit on the wire.</p>
<p>Its <strong>impedance</strong> is set by where the current maximum lands relative to the feed.</p>
<p>Half a wavelength is famous because it puts the current maximum at the feed — and it costs you only 0.39 dB of directivity to get there.</p>
</div>

Note:
If they leave with one sentence, make it the last one.

---

## Where this is going

- **L8** — you build this exact antenna in 4nec2. Length, impedance, VSWR, pattern. **The numbers you just predicted are the ones you will check against simulation.**
- **L9** — cut the dipole in half and stand it on a ground plane, then bend one into a loop.
- **Module 3** — a dipole becomes an *element*. Put many in a row and pattern multiplication takes over from 2.15 dBi.

**Bring the 146 MHz numbers to L8. You are going to grade the simulator with them.**

Note:
Set the expectation now: NEC will not return exactly 73 ohms, and the gap between the sinusoidal-current model and a real solver is itself the lesson.
