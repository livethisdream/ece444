<!-- .slide: class="title-slide" -->

<div class="title-left">

# ECE 444

Antennas, Phased Arrays, and Radar Systems

## Lesson 2 — Basic Properties and Terminology

Fall 2026 · Dr. Neil Rogers

</div>

<div class="title-right">

![USAFA](https://livethisdream.github.io/assets/ece444/img/USAFA-logo.png)

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

<div class="callout">
Every field in this course depends on <strong>both</strong> time and space.
</div>

---

## Part 1

### From Maxwell to a wave

<small>Refresher. If any of this is unfamiliar, come see me — the rest of the course rests on it.</small>

---

## Maxwell's equations (source-free)

$$
\nabla \cdot \mathbf{E} = 0
\qquad
\nabla \cdot \mathbf{H} = 0
$$

$$
\nabla \times \mathbf{E} = -\mu\, \frac{\partial \mathbf{H}}{\partial t}
$$

$$
\nabla \times \mathbf{H} = \varepsilon\, \frac{\partial \mathbf{E}}{\partial t}
$$

<div class="callout">
A <strong>time</strong> change in one field forces a <strong>space</strong> curl in the other.
</div>

Note:
This coupling — time change in one produces space curl in the other — is
what makes waves. Slow this slide down; make sure everyone sees where the
time and space derivatives live.

---

## Guided version — the telegrapher's equations

On a two-conductor line, voltage $v(z, t)$ and current $i(z, t)$:

$$
\frac{\partial v}{\partial z} = -L\, \frac{\partial i}{\partial t}
$$

$$
\frac{\partial i}{\partial z} = -C\, \frac{\partial v}{\partial t}
$$

Same structure as the curl pair: **space on the left, time on the right.**

Note:
Ask the class: what happens if you differentiate the first with respect to
z and substitute the second? You get the 1-D wave equation for v.

---

## Both give you the wave equation

Free space, source-free:

$$
\nabla^{2} \mathbf{E} - \mu \varepsilon\, \frac{\partial^{2} \mathbf{E}}{\partial t^{2}} = 0
$$

Transmission line:

$$
\frac{\partial^{2} v}{\partial z^{2}} - L C\, \frac{\partial^{2} v}{\partial t^{2}} = 0
$$

Second derivative in space, second derivative in time, tied by a speed.

<div class="callout">
$c = 1 / \sqrt{\mu \varepsilon}$, $\quad u = 1 / \sqrt{L C}$
</div>

---

## A plane-wave solution

Traveling in $+\hat{z}$, linearly polarized along $\hat{x}$:

$$
\mathbf{E}(z, t) = \hat{x} E_{0} \cos(\omega t - k z)
$$

- $\omega = 2 \pi f \longrightarrow$  **time** frequency
- $k = 2 \pi / \lambda \longrightarrow$ **space** frequency (wave number)
- $\omega / k = c \longrightarrow$ **crest speed**

<div class="callout">
Freeze <em>t</em> $\longrightarrow$ you see a wave in space. 

Freeze <em>z</em> $\longrightarrow$ you see a wave in time.
</div>

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

<small>We'll derive that $1/r$ from the radiation integrals in L6.</small>

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

## Part 2

### Wave Parameters

---

## Radiation intensity

Power radiated per unit solid angle:

$$
U(\theta, \phi) = r^{2} S_{\text{rad}}(r, \theta, \phi)
\quad [\text{W/sr}]
$$

The $r^{2}$ cancels the $1/r^{2}$ in Poynting — $U$ depends **only on direction**.

$$
P_{\text{rad}} = \oint U(\theta, \phi) d\Omega
$$

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

## Gain and efficiency

$$
G(\theta, \phi) = e_{\text{rad}} D(\theta, \phi)
$$

$$
e_{\text{rad}} = \frac{P_{\text{rad}}}{P_{\text{in}}} \in [0, 1]
$$

With mismatch — **realized gain**:

$$
G_{\text{re}} = (1 - |\Gamma|^{2}) G
$$

<div class="callout">
Datasheet "gain, dBi" is almost always realized gain at boresight.
</div>

---

## Gain, side by side

<p style="text-align:center;">
<img src="./img/02-antenna-properties/gain-pattern-polar.png"
     alt="Polar gain plots comparing isotropic, dipole, horn, and parabolic dish"
     style="max-height:520px;">
</p>

<small>Isotropic (dashed) · λ/2 dipole · Std-gain horn · Parabolic dish (D/λ = 10)</small>

Note:
Interactive on the site — pull up the L2 lesson page, slide D/λ to watch
the dish beam narrow and its peak gain climb.

---

## Effective area

How much of an incident wave a receive antenna captures:

$$
A_{e} = \frac{P_{\text{rx}}}{S_{\text{inc}}}
$$

Reciprocity ties $A_{e}$ to $G$:

$$
\boxed{A_{e} = \frac{\lambda^{2}}{4 \pi} G}
$$

- Same physical antenna at higher $f$ → smaller $A_{e}$.
- Pairs with Friis / radar equation in Module 4.

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

## Features on a rectilinear plot

<p style="text-align:center;">
<img src="./img/02-antenna-properties/rectilinear.png"
     alt="Rectilinear radiation pattern with HPBW, FNBW, and sidelobe level annotated"
     style="max-height:520px;">
</p>

<small>Sinc² aperture, D/λ = 6. HPBW at −3 dB · FNBW at first nulls · SLL at first sidelobe peak.</small>

Note:
Interactive on the site — students can drag D/λ and watch beamwidth
narrow while sidelobes multiply. Point them there for the tradeoffs slide
that follows.

---

## Tradeoffs

**Narrower beam** ↔ **higher sidelobes** — pick your poison.

- Uniform aperture: narrowest main lobe, worst sidelobes
- Tapered aperture: broader main lobe, deeper sidelobe suppression

We'll formalize this in **Module 3** with amplitude tapering
(uniform, cosine, Chebyshev, Taylor).

---

## Next Time

<figure class="qr qr-right">
  <img src="https://livethisdream.github.io/assets/ece444/img/syllabus-qr.png" alt="QR to syllabus">
  <figcaption>Syllabus</figcaption>
</figure>

Reading:

- Balanis or Milligan chapter on **polarization** and **bandwidth**
- R&S *Antenna Basics*, Sections 3.10 – 3.13

<div class="callout">

Next lesson: **polarization and bandwidth** — the direction of $\mathbf{E}$ and how it (and everything else) changes with frequency.

</div>
