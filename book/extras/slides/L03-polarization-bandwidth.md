<!-- .slide: class="title-slide" -->

<div class="title-left">

# ECE 444

Antennas, Phased Arrays, and Radar Systems

## Lesson 3 — Polarization and Bandwidth

Fall 2026 · Dr. Neil Rogers

</div>

<div class="title-right">

![USAFA](https://livethisdream.github.io/assets/ece444/img/USAFA-logo.png)

</div>

---

## Where we were

- L2: parameters that describe **where** and **how well** an antenna radiates
- Gain, directivity, effective area, HPBW, sidelobes
- Reflection coefficient Γ and VSWR at the antenna terminals

Today: **which way** does the E-field point, and **over what range of frequencies** does the antenna work.

Note:
One-minute recap. L2 was about *magnitude* and *shape* of the radiated
field. L3 is about *direction of E* and *frequency coverage*.

---

## Today's plan

1. **Polarization** — direction the E-field traces at a point
2. **Axial ratio & polarization loss factor** — how much power actually couples
3. **Bandwidth** — impedance, pattern, polarization; fractional and ratio BW
4. **Chu-Harrington** — why small antennas are narrowband

<div class="callout">
Polarization and bandwidth are the two most misquoted specs on a datasheet.
</div>

---

## Part 1

### Polarization

<small>Direction of the E-vector at a fixed point over one period.</small>

---

## What polarization is

Fix a point in space. Watch $\mathbf{E}(t)$ trace a curve over one period.

<div class="callout">
That curve <strong>is</strong> the polarization.
</div>

- **Line** → linear polarization
- **Circle** → circular polarization
- **Ellipse** → elliptical (the general case)

A receive antenna only picks up the component of $\mathbf{E}$ **aligned with its own polarization**. Everything else is discarded.

---

## Building any polarization from two linear components

$$
\mathbf{E}(z, t)
= \hat{x} E_{x} \cos(\omega t - k z)
+ \hat{y} E_{y} \cos(\omega t - k z + \delta)
$$

Three knobs: $E_{x}$, $E_{y}$, and relative phase $\delta$.

- $\delta = 0$, equal amplitudes → **linear** at 45°
- $\delta = \pm 90^{\circ}$, equal amplitudes → **circular**
- Everything else → **elliptical**

Note:
Draw the three cases on the chalkboard. Two orthogonal linear
components + a phase difference → *any* polarization state.

---

## Right or left hand?

**IEEE convention** — point your right thumb along the direction of propagation.

- Fingers curl the way E rotates → **right-hand** polarization
- Otherwise → **left-hand** polarization

<div class="callout">
Two identical CP antennas of <em>opposite sense</em> receive zero from each other.
Sense mismatch is a real design bug.
</div>

---

## Axial ratio

For the general ellipse:

$$
\text{AR} = \frac{|E_{\text{maj}}|}{|E_{\text{min}}|} \ge 1
$$

$\text{AR}_{\text{dB}} = 20 \log_{10}(\text{AR})$

- $\text{AR} = 1$ (0 dB) → pure **circular**
- $\text{AR} = \infty$ ($\infty$ dB) → pure **linear**
- Real CP antennas: **AR ≤ 3 dB** across the band

Note:
"3 dB axial ratio" is the industry-standard CP spec. It caps
polarization loss to any linear receiver at 3 dB regardless of alignment.

---

## Polarization loss factor

$$
\text{PLF} = |\hat{\rho}_{\text{w}} \cdot \hat{\rho}_{\text{a}}^{*}|^{2}
$$

Fraction of incident power an antenna captures given a polarization mismatch.

<div class="callout">
Unit vectors are <em>complex</em> when either wave is not purely linear —
that dot product silently carries the phase between $E_{x}$ and $E_{y}$.
</div>

---

## PLF cheat sheet

| Wave | Antenna | PLF | dB |
| :--- | :--- | :---: | :---: |
| Linear ($\hat{x}$) | Linear ($\hat{x}$) | 1 | 0 |
| Linear ($\hat{x}$) | Linear ($\hat{y}$) | 0 | $-\infty$ |
| Linear | RHCP or LHCP | 0.5 | $-3$ |
| RHCP | RHCP | 1 | 0 |
| RHCP | LHCP | 0 | $-\infty$ |

Two linear antennas tilted by $\theta$: $\text{PLF} = \cos^{2}\theta$.

Note:
Memorize this table. Every polarization problem on a homework or an
exam reduces to it plus the $\cos^{2}\theta$ rule for linear-linear.

---

## Why sat and GPS links use CP

**Faraday rotation** in the ionosphere rotates a linear wave's polarization by an unpredictable angle.

- Linear TX + linear RX → unpredictable fading
- Linear TX + CP RX → fixed 3 dB penalty, no fading
- CP TX + CP RX (same sense) → 0 dB penalty, no fading

Same argument applies whenever the receiver's orientation isn't fixed: **cubesats, handhelds, aircraft.**

---

## Part 2

### Bandwidth

<small>How much of the RF spectrum this antenna actually works over.</small>

---

## An antenna has multiple bandwidths

- **Impedance bandwidth** — VSWR ≤ 2 (usually). Most common definition.
- **Pattern bandwidth** — beamwidth, sidelobes stay within spec.
- **Polarization bandwidth** — AR stays below ~3 dB.

<div class="callout">
The three do not have to coincide. A patch can be matched over a
wider band than it holds CP — its polarization BW is narrower.
</div>

---

## Impedance bandwidth — what "VSWR ≤ 2" means

$$
\text{VSWR} = 2 \;\Longleftrightarrow\; |\Gamma| = 1/3
\;\Longleftrightarrow\; \text{RL} = 9.5\ \text{dB}
$$

Reflected power: $|\Gamma|^{2} = 11\%$. Transmitted: $89\%$.

<div class="callout">
"VSWR ≤ 2:1" is the industry-standard bar. Some radar specs push to
1.5:1 or lower; some consumer parts relax to 3:1.
</div>

---

## Fractional and ratio bandwidth

$$
\text{FBW} = \frac{f_{H} - f_{L}}{f_{c}},
\qquad
\text{RBW} = \frac{f_{H}}{f_{L}}
$$

Rough categories:

- **Narrowband**: FBW ≲ 1% (patches, small loops)
- **Broadband**: FBW 10 – 40% (dipoles, horns)
- **UWB**: RBW ≥ 2:1, i.e. FBW ≥ 67% (log-periodic, spiral, Vivaldi)

100 MHz means different things at 500 MHz and 50 GHz — **always report as a fraction.**

---

## Bandwidth is limited by size

**Chu-Harrington bound** — for an antenna in a sphere of radius $a$:

$$
Q \gtrsim \frac{1}{(k a)^{3}} + \frac{1}{k a},
\qquad
\text{BW} \approx \frac{1}{Q}
$$

<div class="callout">
Small antennas (small $ka$) → high Q → narrow BW. There is no free lunch.
</div>

You can beat it with **loss** (resistive loading) but only by trading gain.

Note:
Intuition: cramming a resonator into a small volume forces a high
stored-energy-to-radiated-power ratio. That's exactly Q.

---

## Bandwidth by antenna family

| Antenna | Typical FBW | Notes |
| :--- | :---: | :--- |
| Patch | 1 – 5% | GPS, tags — resonant |
| Dipole (λ/2) | 8 – 15% | Broadcast, generic |
| Horn | 30 – 50% | Test ranges |
| Log-periodic | 10:1 RBW | Broadband probing |
| Spiral | 10:1+ RBW | EW, DF |
| Vivaldi / TSA | 10:1+ RBW | UWB radar, arrays |

<div class="callout">
Resonant → narrow. Traveling-wave and self-scaling → wide.
</div>

---

## Tradeoffs

- **Narrow BW ⇔ high gain, small size.** Every knob fights.
- **Wideband** antennas usually pay in **gain**, **volume**, or **CP purity**.
- **Small** antennas (IoT, wearables) pay in **BW** by Chu-Harrington.

Every real design is picking two of {gain, size, bandwidth} and letting the third suffer.

---

## Next Time

<figure class="qr qr-right">
  <img src="https://livethisdream.github.io/assets/ece444/img/syllabus-qr.png" alt="QR to syllabus">
  <figcaption>Syllabus</figcaption>
</figure>

Reading:

- Balanis or Milligan chapter on **input impedance and matching**
- R&S *Antenna Basics*, sections on feed lines and baluns

<div class="callout">

Next lesson: **impedance, feeding, and baluns** — the transmission-line side of the antenna terminals.

</div>
