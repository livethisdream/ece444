# L2 - Basic Properties and Terminology


:::{admonition} Slides
:class: slides
<a href="../../slides/L02-antenna-properties.html" target="_blank" rel="noopener">html slides</a>
<a href="../../slides/L02-antenna-properties.html?print-pdf" target="_blank" rel="noopener">pdf slides</a>
<a href="../../slides/L02-antenna-properties.md" target="_blank" rel="noopener">raw markdown slides</a>
:::

## Learning outcomes

By the end of this lesson, you will be able to:

<ol class="lo-list" style="--module: '2'">
  <li>Trace the physics chain from Maxwell's equations → telegrapher's equations → the wave equation → the plane-wave solution, and identify the time and space dependencies in each.</li>
  <li>Recognize why the far-field of an antenna is a plane-wave-like transverse E-H pair falling off as 1/r.</li>
  <li>Define and compute the headline antenna parameters: radiation intensity, directivity, gain, effective area, beamwidth, boresight, main / side / back lobes.</li>
  <li>Read a radiation pattern and pull out HPBW, FNBW, and sidelobe level.</li>
</ol>

## Part 1: From Maxwell to a wave

Every antenna analysis in this course starts from Maxwell's equations.
Antennas are a boundary-condition problem: currents on the antenna set
tangential fields, those fields must match a solution that radiates
outward. To see *why* they radiate, we walk the chain once.

### Maxwell's equations (source-free, linear media)

$$
\nabla \cdot \mathbf{E} = 0
\qquad
\nabla \cdot \mathbf{H} = 0
$$

$$
\nabla \times \mathbf{E} = -\mu \frac{\partial \mathbf{H}}{\partial t}
\qquad
\nabla \times \mathbf{H} = \varepsilon \frac{\partial \mathbf{E}}{\partial t}
$$

The two curl equations are the ones that make waves. A **changing
$\mathbf{H}$ in time** creates a spatial curl in $\mathbf{E}$, and a
**changing $\mathbf{E}$ in time** creates a spatial curl in
$\mathbf{H}$. Time and space are locked together — you cannot change
one without changing the other. That coupling is the entire story of
propagation.

### Guided version — the telegrapher's equations

On a two-conductor transmission line, integrating Maxwell over the
cross-section collapses the fields onto voltage $v(z,t)$ and current
$i(z,t)$:

$$
\frac{\partial v}{\partial z} = -L\, \frac{\partial i}{\partial t}
\qquad
\frac{\partial i}{\partial z} = -C\, \frac{\partial v}{\partial t}
$$

Same structure as the curl pair: a spatial derivative on one side, a
time derivative on the other. Differentiate one, substitute the other,
and both $v$ and $i$ satisfy the 1-D wave equation

$$
\frac{\partial^2 v}{\partial z^2}
= L C\, \frac{\partial^2 v}{\partial t^2}.
$$

The propagation speed drops out: $u = 1 / \sqrt{L C}$. On an air-filled
line this is essentially $c$.

### The 3-D wave equation

In free space, the same "curl-of-curl" trick applied to Maxwell
gives

$$
\nabla^{2} \mathbf{E}
- \mu \varepsilon\, \frac{\partial^{2} \mathbf{E}}{\partial t^{2}} = 0
\qquad\text{with speed}\qquad
c = \frac{1}{\sqrt{\mu \varepsilon}}.
$$

The exact same equation applies to $\mathbf{H}$. This is the equation
whose solutions the rest of the course lives in.

### A plane-wave solution

The canonical solution, propagating in $+\hat{z}$:

$$
\mathbf{E}(z, t) = \hat{x}\, E_{0}\, \cos(\omega t - k z)
$$

- $\omega = 2 \pi f$ is the **time frequency** — how fast the field
  oscillates at a fixed point.
- $k = 2 \pi / \lambda$ is the **spatial frequency** (wave number) —
  how fast the field oscillates at a fixed instant in time.
- $\omega / k = c$ ties them together: the wave crest moves through
  space at $c$.

**The point to hammer:** every field in this course is a function of
both **time** and **space**. When we suppress the $e^{j \omega t}$
factor and work with phasors, we're not throwing time away — we're
agreeing to carry it silently so we can focus on the spatial
structure. The moment we hit a bandwidth, dispersion, or pulsed-radar
problem, the time dependence comes back and matters.

### Impedance of free space and the far-field structure

Plugging the plane-wave $\mathbf{E}$ back into Faraday's law forces
$\mathbf{H}$ to be transverse, perpendicular to $\mathbf{E}$, and

$$
\eta_{0} = \frac{|\mathbf{E}|}{|\mathbf{H}|}
= \sqrt{\frac{\mu_{0}}{\varepsilon_{0}}}
\approx 377\ \Omega.
$$

Far from an antenna, the radiated field looks locally like a plane
wave — transverse E and H, ratio $\eta_{0}$ — with a $1/r$ amplitude
fall-off that we'll derive from the radiation integrals in L6. That
$1/r$ (equivalently $1/r^{2}$ in power) is why the antenna's
directional properties even *matter* — they set how much power lands
on your receiver in a given direction.

### Interactive — visualize the plane wave

<iframe src="https://emanim.szialab.org/index.html"
        width="100%" height="700"
        style="border: 1px solid #cddce9; border-radius: 6px;"
        loading="lazy"
        title="EM wave animation (Szialab)">
</iframe>

<p><small>
Interactive EM wave animation by Szilárd Szabó (Szialab).
<a href="https://emanim.szialab.org/index.html" target="_blank" rel="noopener">Open in a new tab →</a>
</small></p>

## Part 2: Wave Parameters

With the wave equation in hand, we can define the working vocabulary
for the rest of Module 1.

### Radiation intensity

Power radiated per unit solid angle, in a given direction:

$$
U(\theta, \phi)
= r^{2}\, S_{\text{rad}}(r, \theta, \phi)
\qquad [\text{W/sr}]
$$

where $S_{\text{rad}} = |\mathbf{E}|^{2} / (2 \eta_{0})$ is the
time-average Poynting magnitude in the far field. The $r^{2}$ cancels
the $1/r^{2}$ in $S_{\text{rad}}$, so $U$ depends only on direction,
not distance. Total radiated power is

$$
P_{\text{rad}} = \oint U(\theta, \phi)\, d\Omega.
$$

### Directivity

How well the antenna concentrates power in a given direction relative
to an isotropic radiator:

$$
D(\theta, \phi)
= \frac{U(\theta, \phi)}{U_{\text{iso}}}
= \frac{4 \pi\, U(\theta, \phi)}{P_{\text{rad}}}.
$$

$D$ is dimensionless (or in dBi when converted to decibels).
"**Directivity**" — no losses, purely geometric.

A useful rule of thumb: for a pencil beam with half-power beamwidths
$\theta_{1}$ and $\theta_{2}$ (in radians),

$$
D \approx \frac{4 \pi}{\theta_{1}\, \theta_{2}}
\quad\text{or, in degrees}\quad
D \approx \frac{41{,}253}{\theta_{1}^{\circ}\, \theta_{2}^{\circ}}.
$$

### Gain and radiation efficiency

Gain is directivity with losses folded in:

$$
G(\theta, \phi) = \eta_{\text{rad}}\, D(\theta, \phi),
\qquad
\eta_{\text{rad}} = \frac{P_{\text{rad}}}{P_{\text{in}}}
\in [0, 1].
$$

Efficiency accounts for ohmic and dielectric losses in the antenna
structure. Mismatch loss at the antenna terminals is usually broken
out separately as **realized gain** $G_{\text{re}} = (1 - |\Gamma|^{2})\, G$.

When your instrument or datasheet reports "gain in dBi," it is
almost always the realized gain in the peak direction.

#### Interactive — compare gain patterns

Toggle antenna types on/off to compare their **E-plane** gain patterns
against an isotropic reference. Slide the dish diameter to watch the
parabolic beam narrow (and its peak gain climb).

<iframe src="../../viz/polar-gain.html"
        width="100%" height="620"
        style="border: 1px solid #cddce9; border-radius: 6px;"
        loading="lazy"
        title="Polar gain patterns">
</iframe>

### Effective area (aperture)

The area of a plane wave that a receiving antenna "captures":

$$
A_{e}(\theta, \phi) = \frac{P_{\text{rx}}}{S_{\text{inc}}}.
$$

Reciprocity ties $A_{e}$ to $G$ through a universal relation:

$$
A_{e} = \frac{\lambda^{2}}{4 \pi}\, G.
$$

Two consequences you'll use over and over:

1. For a fixed physical antenna, **effective area shrinks with
   frequency** (higher $f$ → smaller $\lambda^{2}$). This is why
   high-gain dishes are frequency-scaled.
2. Combining $A_{e}$ on the receive end with $G$ on the transmit end
   gives the **Friis transmission equation** we'll need for the radar
   equation in Module 4.

### Beamwidth, boresight, and lobes

Read on a radiation pattern:

- **Boresight** — the direction of peak radiation. Antennas are
  usually aimed along boresight.
- **Half-power beamwidth (HPBW)** — angular width where the pattern
  drops by 3 dB (to $1/2$ in power).
- **First-null beamwidth (FNBW)** — angular width between the first
  nulls on either side of the main lobe. Roughly $2\times$ HPBW for
  most simple patterns.
- **Main lobe** — the lobe containing boresight.
- **Sidelobes** — every other lobe. Reported by **sidelobe level
  (SLL)** in dB below the main lobe peak.
- **Back lobe** — the lobe centered at $180^{\circ}$ from boresight.
  The **front-to-back ratio (F/B)** is main-lobe peak divided by
  back-lobe peak.

Beamwidth and sidelobe level are the two knobs you'll trade against
each other in every array-tapering problem in Module 3.

#### Interactive — read features off a pattern

The plot below shows the **rectilinear** ($\theta$ vs. dB) view of the
same aperture pattern we used for the horn and dish in the polar plot.
Slide **D/λ** to change the aperture size; the HPBW, FNBW, and SLL
markers move with it.

<iframe src="../../viz/pattern-features.html"
        width="100%" height="720"
        style="border: 1px solid #cddce9; border-radius: 6px;"
        loading="lazy"
        title="Rectilinear pattern features">
</iframe>

## Summary

| Quantity          | Intuition                           |
| ----------------- | ----------------------------------- |
| Radiation pattern | In what direction energy goes       |
| Gain              | How concentrated the energy is      |
| Directivity       | Gain without losses                 |
| Polarization      | Orientation of E-field              |
| Bandwidth         | Range of useful frequencies         |
| Efficiency        | How much power is actually radiated |
| Impedance         | How easily power enters antenna     |


## Where this shows up next

- **L3 (Polarization and Bandwidth)** — the direction of $\mathbf{E}$
  and how the parameters we just defined change with frequency.
- **L4 (Impedance, Feeding, and Baluns)** — the transmission-line
  side of the antenna terminals: matching, $S_{11}$, VSWR.
- **L5 (Field Regions)** — where the plane-wave approximation is
  valid and where it isn't, and what that means for measurement.
- **L6 (Radiation Integrals)** — deriving the $1/r$ far field from an
  arbitrary current distribution.

## Practice

- [Problems](practice.md)
- [Solutions](practice-solutions.md)

## Preparing for L3

Read the assigned sections on **polarization and bandwidth** before
class. Come ready to explain what "vertical polarization" means in
terms of the plane-wave solution we wrote today.
