<!-- .slide: class="title-slide" -->

<div class="title-left">

# ECE 444

Antennas, Phased Arrays, and Radar Systems

## Lesson 2 — Basic Properties and Terminology

Fall 2026 · Dr. Neil Rogers

</div>

<div class="title-right">

![USAFA](./img/01-course-intro/USAFA-logo.png)

</div>

---

## Where we were

- L1: an antenna is a **transducer** — guided wave ↔ radiated wave
- Reciprocal, doesn't create energy
- Every wireless system has at least one

Today we build the **vocabulary** for the rest of Module 1.

Note:
Two-minute recap. Move fast — most of today is new material.

---

## Today's plan

1. Physics chain: **Maxwell → telegrapher's → wave equation → solution**
2. What a "wave" actually looks like in time and space
3. Parameters: **directivity, gain, effective area, beamwidth, lobes**
4. Reciprocity, and the **Friis** link equation it makes possible

<div class="callout">
Every field in this course depends on <strong>both</strong> time and space.
</div>

---

## Maxwell's equations (source-free region)

$$
\nabla \cdot \mathbf{E} = 0
\qquad
\nabla \cdot \mathbf{H} = 0
$$

$$
\nabla \times \mathbf{E} = -\mu \frac{\partial \mathbf{H}}{\partial t}
$$

$$
\nabla \times \mathbf{H} = \varepsilon \frac{\partial \mathbf{E}}{\partial t}
$$

<div class="callout">
A <strong>time</strong> change in one field forces a <strong>space</strong> curl in the other.
</div>

Note:
This coupling — time change in one produces space curl in the other — is
what makes waves. Slow this slide down; make sure everyone sees where the
time and space derivatives live.

---

## The Telegrapher's Equations

On a two-conductor line, voltage $v(z, t)$ and current $i(z, t)$:

$$
\frac{\partial v}{\partial z} = -L \frac{\partial i}{\partial t}
$$

$$
\frac{\partial i}{\partial z} = -C \frac{\partial v}{\partial t}
$$

Same structure as the curl pair: **space on the left, time on the right.**

Note:
Ask the class: what happens if you differentiate the first with respect to
z and substitute the second? You get the 1-D wave equation for v.

---

## Both give you the wave equation

Free space, source-free region:

$$
\nabla^{2} \mathbf{E} - \mu \varepsilon \frac{\partial^{2} \mathbf{E}}{\partial t^{2}} = 0
$$

Transmission line:

$$
\frac{\partial^{2} v}{\partial z^{2}} - L C \frac{\partial^{2} v}{\partial t^{2}} = 0
$$

Second derivative in space, second derivative in time, tied by a speed.

<div class="callout">
$c = 1 / \sqrt{\mu \varepsilon}$, $\quad u = 1 / \sqrt{L C}$
</div>

---

<!-- .slide: class="viz-cue-slide" -->

## The Plane Wave Solution

Traveling in $+\hat{z}$, linearly polarized along $\hat{x}$:

$$
\mathbf{E}(z, t) = \hat{x} E_{0} \cos(\omega t - k z)
\qquad
\mathbf{H}(z, t) = \hat{y} \frac{E_{0}}{\eta_{0}} \cos(\omega t - k z)
$$

- $\omega = 2 \pi f \longrightarrow$  **time** frequency
- $k = 2 \pi / \lambda \longrightarrow$ **space** frequency (wave number)
- $\omega / k = c \longrightarrow$ **crest speed/phase velocity**
- $\mathbf{H} \perp \mathbf{E}$, in phase, with $|\mathbf{E}| / |\mathbf{H}| = \eta_{0} \approx 377\ \Omega$

<div class="callout">
Freeze <em>t</em> $\longrightarrow$ you see a wave in space. 

Freeze <em>z</em> $\longrightarrow$ you see a wave in time.
</div>

<p class="viz-cue">↗ Interactive on the lesson page</p>

Note:
Draw the two snapshots on the chalkboard. This is the intuition slide.

---

## Impedance of free space

Faraday forces $\mathbf{H} \perp \mathbf{E}$, both transverse to $\hat{z}$:

$$
\eta_{0}
= \frac{|\mathbf{E}|}{|\mathbf{H}|}
= \sqrt{\frac{\mu_{0}}{\varepsilon_{0}}}
\approx 377\ \Omega
$$

Far from any antenna, the radiated field looks **locally like a plane
wave**: transverse E and H, ratio $\eta_{0}$, amplitude falling as $1/r$.

<small>We'll derive the 1/r factor from the radiation integrals soon!</small>

---

## Why Phasors Work

We agree to write

$$
\mathbf{E}(\mathbf{r}, t)
= \operatorname{Re}\left\lbrace \tilde{\mathbf{E}}(\mathbf{r}) e^{j \omega t} \right\rbrace
$$

and then carry $\tilde{\mathbf{E}}(\mathbf{r})$ only.

<div class="callout">
Steady-state: we carry the time-dependence silently at a fixed $\omega$ 
</div>

We bring time back to deal with bandwidth, dispersion, or pulses (RADAR!)

---

## The Poynting vector

Power flow per unit area:

$$
\mathbf{S} = \mathbf{E} \times \mathbf{H}\ \ [\text{W/m}^{2}],
\qquad
\langle S \rangle = \frac{|\mathbf{E}|^{2}}{2 \eta_{0}}
$$

<div class="fig" data-inline-svg="./fig/L02-poynting.svg" style="max-width:1160px; margin:0 auto;"></div>

<p class="fig-note">$\mathbf{E}\perp\mathbf{H}\perp\mathbf{S}$ · along propagation · falls as $1/r^{2}$.</p>

Note:
S = E × H is where the power lives. Time-average gives |E|²/2η₀. This is
the quantity radiation intensity is built from — motivate the next slide.

---

<!-- .slide: class="viz-cue-slide" -->

## Radiation intensity

<div class="two-col"><div class="col-text">
<p>Power radiated per unit solid angle:</p>
$$
U(\theta, \phi) = r^{2} S_{\text{rad}}(r, \theta, \phi)
\quad [\text{W/sr}]
$$
<p>The $r^{2}$ cancels the $1/r^{2}$ in Poynting — $U$ depends <strong>only on direction</strong>.</p>
$$
P_{\text{rad}} = \oint U(\theta, \phi) d\Omega
$$
$$
\Omega = \frac{A}{r^{2}}
\qquad
A = r^{2} \Rightarrow 1\ \text{sr}
$$
$$
\Omega = 2\pi(1 - \cos\alpha)\ \text{sr}
\qquad
\Omega_{\text{sphere}} = 4\pi\ \text{sr}
$$
<p class="viz-cue">↗ Interactive on the lesson page</p>
</div><div class="col-fig">
<div data-inline-svg="./fig/L02-solid-angle.svg"></div>
</div></div>

---

## Directivity

Concentration of power relative to isotropic:

$$
D(\theta, \phi)
= \frac{4 \pi U(\theta, \phi)}{P_{\text{rad}}}
$$

Dimensionless. Reported in **dBi** (dB relative to isotropic).

Pencil-beam approximation:

$$
D \approx \frac{41{,}253}{\theta_{1}^{\circ} \theta_{2}^{\circ}}
$$

---

<!-- .slide: class="viz-cue-slide" -->

## Gain and efficiency

$$
G(\theta, \phi) = \eta_{\text{rad}} D(\theta, \phi)
$$

$$
\eta_{\text{rad}} = \frac{P_{\text{rad}}}{P_{\text{in}}} \in [0, 1]
$$

With mismatch — **realized gain**:

$$
G_{\text{re}} = (1 - |\Gamma|^{2}) G
$$

<div class="callout">
Datasheet gain (dBi) is almost always realized gain at boresight.
</div>

<p class="viz-cue">↗ Interactive on the lesson page</p>

---

## $\Gamma$, VSWR, and Power Reflected

$$
\Gamma = \frac{V^-}{V^+} \longrightarrow \text{reflection coefficient}
$$

$$
\text{VSWR} = \frac{V_{\text{max}}}{V_{\text{min}}} = \frac{1 + |\Gamma|}{1 - |\Gamma|}
$$

Read them as **fractions of the incident power**:

$$\frac{P_{\text{refl}}}{P_{\text{inc}}} = |\Gamma|^{2} \qquad \frac{P_{\text{trans}}}{P_{\text{inc}}} = 1 - |\Gamma|^{2}$$

---

<!-- .slide: class="viz-cue-slide" -->

## Quick Reference — Γ vs VSWR vs Power

<div style="display:flex; align-items:center; justify-content:center; gap:1.4em; flex-wrap:wrap;">
<div data-inline-svg="./fig/L02-vswr.svg" style="flex:0 0 auto; width:390px;"></div>
<table style="flex:0 0 auto; width:max-content;">
<thead>
<tr><th>VSWR</th><th>$\vert\Gamma\vert$</th><th>Reflected</th><th>Transmitted</th></tr>
</thead>
<tbody>
<tr><td>1.0:1</td><td>0.00</td><td>0%</td><td>100% — Perfect</td></tr>
<tr><td>1.5:1</td><td>0.20</td><td>4%</td><td>96% — Good</td></tr>
<tr><td>2.0:1</td><td>0.33</td><td>11.1%</td><td>88.9% — Acceptable</td></tr>
<tr><td>3.0:1</td><td>0.50</td><td>25%</td><td>75% — Poor</td></tr>
</tbody>
</table>
</div>

<p class="viz-cue">↗ Interactive on the lesson page</p>

---

<!-- .slide: class="viz-cue-slide" -->

## Gain Comparison

<div class="fig" data-inline-svg="./fig/L02-gain-pattern-polar.svg" style="max-width:470px; margin:0 auto;"></div>

<p class="viz-cue">↗ Interactive on the lesson page</p>

Note:
Interactive on the site — pull up the L2 lesson page, slide D/λ to watch
the dish beam narrow and its peak gain climb.

---

## Reading a radiation pattern

<div class="slide-box">

- **Boresight** — direction of peak radiation
- **HPBW** — 3 dB (half-power) beamwidth
- **FNBW** — first-null beamwidth
- **Main lobe** — contains boresight
- **Sidelobes** — everything else; reported as **SLL** in dB
- **Back lobe** — at $180^{\circ}$ from boresight; **F/B** ratio

</div>

Note:
Draw a polar pattern on the chalkboard, label all six on it.
This is the picture students need to be able to draw from memory.

---

<!-- .slide: class="viz-cue-slide" -->

## Features on a rectilinear plot

<div class="fig" data-inline-svg="./fig/L02-rectilinear.svg" style="max-width:900px; margin:0 auto;"></div>

<small>Sinc² aperture, D/λ = 6. HPBW at −3 dB · FNBW at first nulls · SLL at first sidelobe peak.</small>

<p class="viz-cue">↗ Interactive on the lesson page</p>

Note:
Interactive on the site — students can drag D/λ and watch beamwidth
narrow while sidelobes multiply. Point them there for the tradeoffs slide
that follows.

---

## Tradeoffs

<div class="callout">
<strong>Narrower beam</strong> ↔ <strong>higher sidelobes</strong> — there's no free lunch.
</div>

- Uniform aperture: narrowest main lobe, worst sidelobes
- Tapered aperture: broader main lobe, deeper sidelobe suppression

We'll formalize this in **Module 3** with amplitude tapering
(uniform, cosine, Chebyshev, Taylor).

---

## Reciprocity: Trading Places

<div class="two-col fig-wide"><div class="col-text">
<p>An antenna's <strong>transmit</strong> and <strong>receive</strong> behavior are the <em>same</em>:</p>
<ul><li>Same <strong>pattern</strong> — it radiates best where it hears best</li>
<li>Same <strong>gain / directivity</strong>, <strong>impedance</strong>, <strong>polarization</strong></li></ul>
<p>Rooted in the symmetry of Maxwell's equations (<strong>Lorentz reciprocity</strong>).</p>
<p>Measure in whichever mode is handy — <strong>gain</strong> (Tx) and <strong>effective area</strong> (Rx) are locked together, as we'll see next.</p>
</div><div class="col-fig">
<div data-inline-svg="./fig/L02-reciprocity.svg"></div>
</div></div>

Note:
Holds for linear, passive, isotropic media — ordinary antennas in air. Breaks
only in non-reciprocal media (biased ferrite, magnetized plasma), the guts of a
circulator/isolator. This is the hinge between the Tx story (gain) and the Rx
story (effective area) on the next few slides.

---

## Effective Aperture

<div class="two-col fig-xwide"><div class="col-text">
<p>Turn the antenna to <strong>receive</strong>: received power per incident wave density — an <strong>area</strong>:</p>
$$
\boxed{A_{e} \equiv \frac{P_{\text{rx}}}{S_{\text{inc}}}}
$$
<p>A real aperture captures a fraction $\eta_{\text{ap}} \in [0,1]$ of its physical area:</p>
$$
A_{e} = \eta_{\text{ap}} A_{\text{phys}}
$$
</div><div class="col-fig">
<div data-inline-svg="./fig/L02-effective-aperture.svg"></div>
</div></div>

Note:
This is the definition. The next three slides derive the value of A_e.

---

## The antenna as a receiver

<div class="two-col fig-wide"><div class="col-text">
<p>The incident field induces an open-circuit voltage; the antenna acts as a source with its <strong>radiation resistance</strong> $R_{\text{rad}}$. A conjugate-<strong>matched</strong> load draws the most power:</p>
$$V_{\text{oc}} = E\ell_{e} \qquad P_{\text{rx}} = \frac{V_{\text{oc}}^{2}}{8 R_{\text{rad}}}$$
</div><div class="col-fig">
<div data-inline-svg="./fig/L02-recv-circuit.svg"></div>
</div></div>

Note:
ℓ_e = effective length, R_rad = radiation resistance. Max power transfer gives
the /8R_rad (the ½ from time-averaging a sinusoid turns the usual 4 into 8).

---

## Example: A Short Dipole

<div class="two-col"><div class="col-text">
<p>Use the simplest antenna. Plug in $\ell_e = \ell$, $R_{\text{rad}} = 80\pi^{2}(\ell/\lambda)^{2}$, $S = E^{2}/2\eta_{0}$ — the $\ell$'s cancel:</p>
$$A_{e} = \frac{P_{\text{rx}}}{S} = \frac{\eta_{0}\ell_{e}^{2}}{4 R_{\text{rad}}} = \frac{3\lambda^{2}}{8\pi} = 1.5\cdot\frac{\lambda^{2}}{4\pi}$$
</div><div class="col-fig">
<div data-inline-svg="./fig/L02-short-dipole-incident.svg"></div>
</div></div>

Note:
η0 = 120π. Work the algebra on the board — ℓ² cancels, leaving a pure λ²
times a number. Keep students' eyes on that number.

---

## Extend to the General Case

That **1.5 is the short dipole's directivity** $D$. With losses folded in ($G=\eta_{\text{rad}}D$):

$$
A_{e} = D\frac{\lambda^{2}}{4\pi}
\Longrightarrow
\boxed{A_{e} = \frac{\lambda^{2}}{4\pi} G}
$$

**Reciprocity** makes the ratio $A_e/G$ the *same* for every antenna — so it holds universally. For real apertures, $A_{e} = \eta_{\text{ap}} A_{\text{phys}}$.

<div class="callout">
Fixed dish → $A_e$ fixed, gain $\propto f^{2}$.

Fixed gain → $A_e \propto \lambda^{2}$.
</div>

Note:
We proved it for one antenna; reciprocity generalizes it to all. It is also the
hinge into Friis on the next three slides.

---

## Friis: assemble the link

<div class="fig" data-inline-svg="./fig/L02-friis-geometry.svg" style="max-width:660px; margin:0 auto;"></div>

Spread $P_t G_t$ over a sphere of radius $R$, then let the receiver's effective aperture catch its share:

$$S_{\text{inc}} = \frac{P_t G_t}{4\pi R^{2}} \qquad P_r = S_{\text{inc}}\ A_e \qquad A_e = G_r \frac{\lambda^{2}}{4\pi}$$

$$P_r = P_t G_t G_r \left(\frac{\lambda}{4\pi R}\right)^{2}$$

Valid when: **far field at both ends** · **polarizations matched** · **loads matched** (else use realized gain) · **free space** — no ground bounce, no atmosphere, no obstruction.

Note:
Two lines, no new physics — power density from gain, captured power from
effective aperture. Say the four validity conditions out loud; every one of them
is a term someone adds back later in a real link budget.

---

## Three things to read off it

- **EIRP** $= P_t G_t$ — the whole transmit side as one number: the power an isotropic radiator *would* need to match you on boresight.
- **Free-space path loss** is the $(4\pi R/\lambda)^{2}$ factor, or $20\log_{10}(4\pi R/\lambda)$ in dB. It climbs with **both** range and frequency, and it dominates every link.
- **Everything multiplies**, so in decibels a link budget is just addition:

$$P_r\ [\text{dBm}] = P_t + G_t + G_r - \text{FSPL}$$

<div class="callout">
Antenna gain buys back <strong>tens</strong> of dB. The path takes <strong>hundreds</strong>.
</div>

Note:
EIRP is what a spectrum authority regulates, because it is the only number that
matters at the far end. Emphasize that FSPL is not absorption — nothing is lost,
the power just spreads.

---

## Worked example: a 600 km link

10 W at 2.4 GHz through a 20 dBi ground antenna, to a 6 dBi antenna on a satellite 600 km up.

| Quantity | Work | Result |
| :-- | :-- | :-- |
| $\lambda$ | $3\times10^{8} / 2.4\times10^{9}$ | $0.125\ \text{m}$ |
| $P_t$ | 10 W in dBm | $40\ \text{dBm}$ |
| FSPL | $20\log_{10}(4\pi \times 6\times10^{5} / 0.125)$ | $156\ \text{dB}$ |
| $P_r$ | $40 + 20 + 6 - 156$ | $\mathbf{-90\ \text{dBm}}$ |

**About a picowatt — and a perfectly ordinary receive level.**

Note:
Have them check the exponent by hand: 4 pi R over lambda is about 6e10, and 20
log of that is 156. Then make the point that minus 90 dBm is 20 dB above a
typical receiver noise floor, so the link closes with margin.

---

## Key point

<div class="callout">
<p>Every parameter today is a <strong>ratio</strong>: directivity against isotropic, gain against input power, effective aperture against incident power density, VSWR against a perfect match.</p>
<p><strong>Reciprocity</strong> locks the transmit ratio to the receive one — $A_e = G\lambda^2/4\pi$, for every antenna ever built.</p>
<p>Friis is nothing more than that sentence, written down at both ends of a link.</p>
</div>

Note:
If they leave with one sentence, make it the last one.

---

## Where this is going

- **L3** — polarization and bandwidth: the direction of $\mathbf{E}$, and how every parameter defined today moves with frequency.
- **L4** — the terminals behind the $\Gamma$ you just met: matching, $S_{11}$, and baluns.
- **L5 and L6** — where the far field starts, and the radiation integral that *produces* a pattern instead of assuming one.
- **Module 4 (L29)** — send Friis out, let a target scatter it, collect the echo. Friis applied twice is the radar range equation.

**Every link budget you write from here on is the two lines you just assembled.**

Note:
Point out that nothing in Module 1 gets thrown away — L3 through L6 all refine
parameters defined today.

---

## Before next lesson

<figure class="qr qr-right">
  <img src="./img/syllabus-qr.png" alt="QR to syllabus">
  <figcaption>Syllabus</figcaption>
</figure>

Reading:

- Balanis or Milligan chapter on **polarization** and **bandwidth**
- R&S *Antenna Basics*, Sections 3.10 – 3.13

<div class="callout">

Next lesson: **polarization and bandwidth** — the direction of $\mathbf{E}$ and how it (and everything else) changes with frequency.

</div>
