# L3 - Polarization and Bandwidth

:::{admonition} Slides
:class: slides
<a href="../../slides/L03-polarization-bandwidth.html" target="_blank" rel="noopener">html slides</a>
<a href="../../slides/L03-polarization-bandwidth.html?print-pdf" target="_blank" rel="noopener">pdf slides</a>
<a href="../../slides/L03-polarization-bandwidth.md" target="_blank" rel="noopener">raw markdown slides</a>
:::

## Learning outcomes

By the end of this lesson, you will be able to:

<ol class="lo-list" style="--module: '3'">
  <li>Identify the polarization state of a plane wave (linear, circular, elliptical) from the amplitude and phase of its two orthogonal components.</li>
  <li>Compute the axial ratio of an elliptically polarized wave and know what a "3 dB axial ratio" spec means for a circularly polarized antenna.</li>
  <li>Compute the polarization loss factor (PLF) between a transmit and receive antenna with mismatched polarizations.</li>
  <li>Define the impedance, pattern, and polarization bandwidths of an antenna and compute fractional bandwidth from the endpoint frequencies.</li>
  <li>Match common antenna families (patch, dipole, horn, log-periodic, spiral, Vivaldi) to their typical bandwidth range.</li>
</ol>

## Part 1: Polarization

### What polarization is

Fix a point in space and watch the tip of the electric field vector
$\mathbf{E}(t)$ trace a curve over one period. **That curve is the
polarization.**

If the tip moves back and forth along a line, the wave is **linearly
polarized**. If it traces a circle, the wave is **circularly
polarized**. If it traces an ellipse (the general case), the wave is
**elliptically polarized**.

Polarization matters because a receive antenna is only sensitive to the
component of the incident $\mathbf{E}$ that is aligned with its own
polarization. Everything else is thrown away.

### Building any polarization from two linear components

Any plane wave propagating along $+\hat{z}$ can be written as the sum
of two orthogonal linear components:

$$
\mathbf{E}(z, t)
= \hat{x} E_{x} \cos(\omega t - k z)
+ \hat{y} E_{y} \cos(\omega t - k z + \delta).
$$

The polarization is entirely determined by three numbers: the
amplitudes $E_{x}$ and $E_{y}$, and the relative phase $\delta$
between them.

| $E_{x}$, $E_{y}$ | $\delta$ | Polarization |
| :--- | :---: | :--- |
| $E_{y} = 0$ | — | Linear, along $\hat{x}$ |
| $E_{x} = 0$ | — | Linear, along $\hat{y}$ |
| $E_{x} = E_{y}$ | $0$ or $180^{\circ}$ | Linear, slant (45° or 135°) |
| $E_{x} = E_{y}$ | $-90^{\circ}$ | **Right-hand** circular (RHCP) |
| $E_{x} = E_{y}$ | $+90^{\circ}$ | **Left-hand** circular (LHCP) |
| $E_{x} \ne E_{y}$, $\delta = \pm 90^{\circ}$ | | Elliptical, axes on $\hat{x}$ / $\hat{y}$ |
| Anything else | | Elliptical, tilted |

**IEEE convention** — point your right thumb along the direction of
propagation. If the E-vector rotates in the direction your fingers
curl, it's right-hand polarized. Left-hand is the mirror image.

#### Interactive — polarization playground

Move the sliders for $E_{x}$, $E_{y}$, and phase $\delta$ (or hit a
preset) and watch the E-vector trace at a fixed $z$ change from a line
to an ellipse to a circle. The two component waveforms below the trace
show what each linear channel sees.

<iframe src="../../viz/polarization-playground.html"
        width="100%" height="580"
        style="border: 1px solid #cddce9; border-radius: 6px;"
        loading="lazy"
        title="Polarization playground">
</iframe>

### Axial ratio

For the general elliptical case, the axial ratio is the ratio of the
major axis of the ellipse to the minor axis:

$$
\text{AR} = \frac{|E_{\text{maj}}|}{|E_{\text{min}}|}, \qquad
\text{AR} \ge 1.
$$

In dB: $\text{AR}_{\text{dB}} = 20 \log_{10}(\text{AR})$.

- $\text{AR} = 1$ (0 dB) — pure **circular** polarization.
- $\text{AR} \to \infty$ ($\infty$ dB) — pure **linear** polarization.
- Everything else is elliptical, with $1 < \text{AR} < \infty$.

A "CP antenna" is really a nearly-CP antenna. Real specs read something
like **"AR ≤ 3 dB across the operating band"** — meaning the antenna's
polarization stays close enough to circular that no single linear
receiver can miss more than 3 dB of power.

### Polarization loss factor (PLF)

When a wave with polarization $\hat{\rho}_{\text{w}}$ arrives at an
antenna with polarization $\hat{\rho}_{\text{a}}$, the fraction of
incident power the antenna captures is the **polarization loss factor**:

$$
\text{PLF} = |\hat{\rho}_{\text{w}} \cdot \hat{\rho}_{\text{a}}^{*}|^{2}.
$$

The unit vectors are complex when either wave is not purely linear —
that dot product hides the phase relationship between $E_{x}$ and
$E_{y}$.

Four cases you should know cold:

| Wave | Antenna | PLF | PLF (dB) |
| :--- | :--- | :---: | :---: |
| Linear ($\hat{x}$) | Linear ($\hat{x}$) | 1 | 0 dB — co-polarized |
| Linear ($\hat{x}$) | Linear ($\hat{y}$) | 0 | $-\infty$ dB — cross-polarized |
| Linear (any) | RHCP or LHCP | 0.5 | $-3$ dB |
| RHCP | RHCP | 1 | 0 dB |
| RHCP | LHCP | 0 | $-\infty$ dB — sense mismatch |

For two linear antennas tilted by angle $\theta$ relative to each
other, $\text{PLF} = \cos^{2}\theta$ — this is why aligning your
handheld radio matters.

#### Interactive — CP wave in 3-D

The E-vector doesn't just rotate at a point — it traces a *helix* as
the wave propagates. Toggle RHCP / LHCP to see the corkscrew flip
handedness. The blue and red shadows on the back walls are the
component sinusoids $E_{x}(z, t)$ and $E_{y}(z, t)$.

<iframe src="../../viz/cp-helix.html"
        width="100%" height="500"
        style="border: 1px solid #cddce9; border-radius: 6px;"
        loading="lazy"
        title="Circular polarization helix">
</iframe>

### Why satellite and GPS links use circular polarization

Faraday rotation in the ionosphere rotates the plane of a linearly
polarized wave by an unpredictable angle as it passes through — so a
purely linear satellite downlink would fade in and out as ionospheric
conditions changed. Circular polarization, by contrast, is invariant
under rotation about the propagation axis (a rotated circle is still a
circle), so CP dodges the problem entirely. Cost: a fixed 3 dB penalty
when either end is only linear.

The same argument applies whenever the receiver's orientation isn't
fixed — cubesats tumble, handhelds rotate, aircraft bank.

## Part 2: Bandwidth

### What "bandwidth" means depends on what you're measuring

An antenna has multiple bandwidths, one for each parameter you care
about:

- **Impedance bandwidth** — range of frequencies over which the
  antenna is well matched to its feed (usually VSWR ≤ 2, i.e.
  $|\Gamma| \le 1/3$, or return loss ≥ 9.5 dB). This is the most
  common definition and the one meant by an unqualified "bandwidth."
- **Pattern bandwidth** — range where the radiation pattern (gain,
  beamwidth, sidelobe level) stays within spec.
- **Polarization bandwidth** — range where axial ratio stays below a
  threshold, typically 3 dB.

The three don't have to coincide. A patch antenna can be matched over
a wider band than it produces good CP, so its polarization bandwidth
is narrower than its impedance bandwidth.

### Fractional bandwidth

Report bandwidth as a *fraction* of the center frequency, not just Hz:

$$
\text{FBW} = \frac{f_{H} - f_{L}}{f_{c}}, \qquad
f_{c} = \frac{f_{H} + f_{L}}{2}.
$$

100 MHz means very different things at 500 MHz and at 50 GHz.

For wideband antennas the more useful figure is the **ratio bandwidth**:

$$
\text{RBW} = \frac{f_{H}}{f_{L}}.
$$

Rough categories:

- **Narrowband** — FBW $\lesssim 1\%$. Resonant antennas: patches,
  small loops, dielectric resonator antennas.
- **Broadband** — FBW $10 – 40\%$. Dipoles, horns, most practical
  designs.
- **Ultra-wideband (UWB)** — RBW $\ge 2{:}1$ (equivalently FBW $\ge 67\%$
  by FCC definition). Log-periodic, spiral, Vivaldi/TSA, biconical.

### Bandwidth is limited by size

There is no free lunch. The **Chu-Harrington limit** ties minimum
antenna Q to the smallest sphere that encloses the antenna:

$$
Q \gtrsim \frac{1}{(ka)^{3}} + \frac{1}{ka},
\qquad
\text{BW} \approx \frac{1}{Q}
$$

where $a$ is the sphere radius and $k = 2\pi/\lambda$. Small antennas
(small $ka$) inevitably have high $Q$ and narrow bandwidth. This is
why AM broadcast receivers use physically small ferrite-loaded loops
and get by with narrow bandwidth, while a WiFi router's antenna is
already close to $\lambda/2$ and can afford tens of percent bandwidth.

### Bandwidth by antenna family

| Antenna | Typical FBW | Typical use |
| :--- | :---: | :--- |
| Patch (single element) | 1 – 5% | GPS, cell handsets, tags |
| Half-wave dipole | 8 – 15% | Broadcast, generic |
| Slot antenna | 5 – 10% | Aircraft skins |
| Horn (standard gain) | 30 – 50% | Test ranges, feeds |
| Log-periodic | 10 : 1 ratio BW | Broadband probing |
| Spiral / helix | 10 : 1+ | Electronic warfare, DF |
| Vivaldi / TSA | 10 : 1+ | UWB radar, phased arrays |
| Biconical | 3 : 1+ | EMC testing |

The rule of thumb: **resonant antennas are narrowband, traveling-wave
and self-scaling antennas are wideband.** A log-periodic looks the
same electrical size at every frequency in its band because it's a
scaled-copy structure; a patch has one resonant length and only works
near its resonance.

## Summary

| Concept | Take-away |
| :--- | :--- |
| Polarization | Direction of the E-field trace at a point |
| Axial ratio | 0 dB = pure CP, $\infty$ dB = pure linear |
| PLF (co-pol) | 0 dB |
| PLF (cross-pol linear) | $-\infty$ dB |
| PLF (linear ↔ CP) | $-3$ dB |
| Impedance BW | Range with VSWR ≤ 2 (usually) |
| Fractional BW | $(f_{H} - f_{L}) / f_{c}$ |
| Chu-Harrington | Smaller antennas → narrower BW |
| Wideband antennas | Log-periodic, spiral, Vivaldi (self-scaling) |

## Where this shows up next

- **L4 (Impedance, Feeding, Baluns)** — the impedance side of
  matching, $S_{11}$, and how the return-loss curve *defines* the
  impedance bandwidth we just introduced.
- **Module 3 (Arrays)** — array patterns inherit the element
  polarization; a linearly polarized element in a circularly
  polarized array is a design mistake with expensive consequences.
- **Module 4 (Radar)** — polarization diversity as a target
  discrimination tool; some radars alternate H and V transmit pulses
  to extract target scattering matrices.

## Practice

- <a href="../../practice/ECE444_L03_Practice_blank.pdf" target="_blank" rel="noopener">Problem set (PDF)</a>
- <a href="../../practice/ECE444_L03_Practice_SOLUTIONS.pdf" target="_blank" rel="noopener">Solutions (PDF)</a>

## Preparing for L4

Read the assigned sections on **input impedance, feed lines, and
baluns**. Come ready to explain what a "50 Ω antenna" actually means
and why a dipole fed by coax needs a balun.
