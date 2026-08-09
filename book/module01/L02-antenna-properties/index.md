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

### The Telegrapher's Equations

On a two-conductor transmission line, integrating Maxwell over the
cross-section collapses the fields onto voltage $v(z,t)$ and current
$i(z,t)$:

$$
\frac{\partial v}{\partial z} = -L \frac{\partial i}{\partial t}
\qquad
\frac{\partial i}{\partial z} = -C \frac{\partial v}{\partial t}
$$

Same structure as the curl pair: a spatial derivative on one side, a
time derivative on the other. Differentiate one, substitute the other,
and both $v$ and $i$ satisfy the 1-D wave equation

$$
\frac{\partial^2 v}{\partial z^2}
= L C \frac{\partial^2 v}{\partial t^2}.
$$

The propagation speed drops out: $u = 1 / \sqrt{L C}$. On an air-filled
line this is essentially $c$.

### The 3-D wave equation

In free space, the same "curl-of-curl" trick applied to Maxwell
gives

$$
\nabla^{2} \mathbf{E}
- \mu \varepsilon \frac{\partial^{2} \mathbf{E}}{\partial t^{2}} = 0
\qquad\text{with speed}\qquad
c = \frac{1}{\sqrt{\mu \varepsilon}}.
$$

The exact same equation applies to $\mathbf{H}$. This is the equation
whose solutions the rest of the course lives in.

### A plane-wave solution

The canonical solution, propagating in $+\hat{z}$:

$$
\mathbf{E}(z, t) = \hat{x} E_{0} \cos(\omega t - k z)
$$

- $\omega = 2 \pi f$ is the **time frequency** — how fast the field
  oscillates at a fixed point.
- $k = 2 \pi / \lambda$ is the **spatial frequency** (wave number) —
  how fast the field oscillates at a fixed instant in time.
- $\omega / k = c$ ties them together: the wave crest moves through
  space at $c$.

:::{admonition} Key Point
:class: key-concept

Every field in this course is a function of
both **time** and **space**. When we suppress the $e^{j \omega t}$
factor and work with phasors, we're not throwing time away — we're
agreeing to carry it silently so we can focus on the spatial
structure. The moment we hit a bandwidth, dispersion, or pulsed-radar
problem, the time dependence comes back and matters.
:::

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

### Interactive — freeze time, freeze space

The same wave is a ripple in **space** (freeze the clock → wavelength
$\lambda$) and a ripple in **time** (stand at one point → period $T$),
tied together by the crest speed/phase velocity $c = \lambda f = \omega / k$. Drag the
sliders, or press play to watch a crest travel.

<iframe src="../../viz/plane-wave-freeze.html"
        width="100%" height="470"
        style="border: 1px solid #cddce9; border-radius: 6px;"
        loading="lazy"
        title="Plane wave — freeze time / freeze space">
</iframe>

### Interactive — a fuller 3-D view

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

## Part 2: Antenna Parameters

With the wave equation in hand, we can define the working vocabulary for the rest of Module 1.

### The Poynting vector

Before we can say how *much* power an antenna sends in a given direction,
we need the quantity that measures power flow itself. The **Poynting
vector** is

$$
\mathbf{S} = \mathbf{E} \times \mathbf{H}
\qquad [\text{W/m}^{2}],
$$

the instantaneous power per unit area carried by the field, pointing in
the direction of propagation. For a time-harmonic field we almost always
want the **time-average**,

$$
\langle \mathbf{S} \rangle
= \tfrac{1}{2}\,\operatorname{Re}\!\left\lbrace \mathbf{E} \times \mathbf{H}^{*} \right\rbrace,
$$

and in the far field — where $\mathbf{E}$ and $\mathbf{H}$ are transverse
and locally plane-wave-like with $|\mathbf{E}| / |\mathbf{H}| = \eta_{0}$
— its magnitude collapses to

$$
S_{\text{rad}} = \frac{|\mathbf{E}|^{2}}{2 \eta_{0}}.
$$

Because the far-field amplitude falls as $1/r$, this power density falls
as $1/r^{2}$ — the inverse-square law. This $S_{\text{rad}}$ is exactly
the quantity that appears in the radiation-intensity definition next.

<p style="text-align:center;">
<img src="../../viz/img/poynting-triad.svg"
     alt="Orthogonal E, H, and Poynting vector S of a plane wave"
     style="max-width:100%; width:640px;">
</p>

### Radiation intensity

Power radiated per unit solid angle, in a given direction:

$$
U(\theta, \phi)
= r^{2} S_{\text{rad}}(r, \theta, \phi)
\qquad [\text{W/sr}]
$$

where $S_{\text{rad}} = |\mathbf{E}|^{2} / (2 \eta_{0})$ is the
time-average Poynting magnitude in the far field. The $r^{2}$ cancels
the $1/r^{2}$ in $S_{\text{rad}}$, so $U$ depends only on direction,
not distance. Total radiated power is

$$
P_{\text{rad}} = \oint U(\theta, \phi) d\Omega.
$$

A **solid angle** $\Omega$ (in steradians) is the 3-D analogue of a planar
angle: the area a cone cuts out of a unit sphere. A cone pointed in some
direction subtends a solid angle $d\Omega$ and intercepts a patch of area
$r^{2}\,d\Omega$ on a sphere of radius $r$; the whole sphere is $4\pi$ sr.
Radiation intensity is the power flowing through that cone per unit solid
angle — which is why it is a property of *direction alone*.

#### Interactive — solid angle in 3-D

Drag to rotate the sphere; slide the cone half-angle $\alpha$ to watch the
solid angle $\Omega = 2\pi(1 - \cos\alpha)$ and the patch it carves out
grow.

<iframe src="../../viz/solid-angle.html"
        width="100%" height="490"
        style="border: 1px solid #cddce9; border-radius: 6px;"
        loading="lazy"
        title="Solid angle in 3-D">
</iframe>

### Directivity

How well the antenna concentrates power in a given direction relative
to an isotropic radiator:

$$
D(\theta, \phi)
= \frac{U(\theta, \phi)}{U_{\text{iso}}}
= \frac{4 \pi U(\theta, \phi)}{P_{\text{rad}}}.
$$

$D$ is dimensionless (or in dBi when converted to decibels).
"**Directivity**" — no losses, purely geometric.

A useful rule of thumb: for a pencil beam with half-power beamwidths
$\theta_{1}$ and $\theta_{2}$ (in radians),

$$
D \approx \frac{4 \pi}{\theta_{1} \theta_{2}}
\quad\text{or, in degrees}\quad
D \approx \frac{41{,}253}{\theta_{1}^{\circ} \theta_{2}^{\circ}}.
$$

### Gain and radiation efficiency

Gain is directivity with losses folded in:

$$
G(\theta, \phi) = \eta_{\text{rad}} D(\theta, \phi),
\qquad
\eta_{\text{rad}} = \frac{P_{\text{rad}}}{P_{\text{in}}}
\in [0, 1].
$$

Efficiency accounts for ohmic and dielectric losses in the antenna
structure. Mismatch loss at the antenna terminals is usually broken
out separately as **realized gain** $G_{\text{re}} = (1 - |\Gamma|^{2}) G$.

When your instrument or datasheet reports gain in dBi, it is almost always the realized gain in the peak direction.

#### Interactive — build the gain

Start from a directivity, then watch radiation efficiency and mismatch each
carve a few dB away. The bars trace **directivity → gain
$G = \eta_{\text{rad}} D$ → realized gain** in dBi.

<iframe src="../../viz/gain-builder.html"
        width="100%" height="500"
        style="border: 1px solid #cddce9; border-radius: 6px;"
        loading="lazy"
        title="Gain builder">
</iframe>

### $\Gamma$, VSWR, and Power Reflected

Recall:

$\Gamma = \frac{V^-}{V^+} \longrightarrow$ reflection coefficient

and

$\text{VSWR} = \frac{V_{\text{max}}}{V_{\text{min}}} = \frac{ 1 + \vert \Gamma \vert }{1 - \vert\Gamma\vert}$

$\vert\Gamma\vert^2 =$ Reflected Power and $1-\vert\Gamma\vert^2$ = Transmitted Power 

### Quick Reference $\Gamma$ vs VSWR vs Power

<div style="display:flex; align-items:center; justify-content:center; gap:0.8em; flex-wrap:wrap; margin:0.5em 0;">
<img src="../../viz/img/vswr_vs_gamma.png"
     alt="VSWR vs reflection coefficient chart"
     style="width:270px; max-width:100%; flex:0 0 auto;">
<table style="flex:0 0 auto; width:max-content !important; display:table !important; font-size:0.76em;">
<thead>
<tr><th>VSWR</th><th>|Γ|</th><th>Reflected |Γ|²</th><th>Transmitted 1−|Γ|²</th></tr>
</thead>
<tbody>
<tr><td>1.0:1</td><td>0.00</td><td>0%</td><td>100% — Perfect</td></tr>
<tr><td>1.5:1</td><td>0.20</td><td>4%</td><td>96% — Good</td></tr>
<tr><td>2.0:1</td><td>0.33</td><td>11.1%</td><td>88.9% — Acceptable</td></tr>
<tr><td>3.0:1</td><td>0.50</td><td>25%</td><td>75% — Poor</td></tr>
</tbody>
</table>
</div>

#### Interactive — the standing wave behind VSWR

A mismatch sends part of the wave back; the forward and reflected waves add
to a **standing wave**. Slide $|\Gamma|$ and press play — the envelope's
maxima and minima set the VSWR, and the nulls stay pinned in place.

<iframe src="../../viz/vswr-standing-wave.html"
        width="100%" height="560"
        style="border: 1px solid #cddce9; border-radius: 6px;"
        loading="lazy"
        title="VSWR standing wave">
</iframe>

### Effective area (aperture)

Flip the antenna around to *receive*. A passing wave carries power density
$S_{\text{inc}}$ (W/m²); the antenna delivers some power $P_{\text{rx}}$ to
its load. The ratio has units of area and is the **effective area**
(effective aperture):

$$
A_{e}(\theta, \phi) = \frac{P_{\text{rx}}}{S_{\text{inc}}}
\qquad\Longrightarrow\qquad
P_{\text{rx}} = S_{\text{inc}}\, A_{e}.
$$

<p style="text-align:center;">
<img src="../../viz/img/effective-area-capture.svg"
     alt="A receiving aperture capturing effective area from an incident wavefront"
     style="max-width:100%; width:640px;">
</p>

So how big is that capture area — and where does the famous $\lambda^{2}/4\pi$
come from? We can derive it.

**1 · The antenna is a receiving circuit.** An incident field $E$ aligned
with the antenna induces an open-circuit voltage $V_{\text{oc}} = E\,\ell_e$,
where $\ell_e$ is the antenna's *effective length*. The antenna then behaves
like a Thévenin source with internal **radiation resistance** $R_r$; a
conjugate-**matched** load $R_L = R_r$ draws the maximum available power:

$$
P_{\text{rx}} = \frac{V_{\text{oc}}^{2}}{8 R_r}
= \frac{(E\,\ell_e)^{2}}{8 R_r}.
$$

<p style="text-align:center;">
<img src="../../viz/img/recv-circuit.svg"
     alt="Receiving antenna modeled as a Thevenin source feeding a matched load"
     style="max-width:100%; width:700px;">
</p>

<small>The $8$ (not $4$) is the time-average of a sinusoid: for a peak
amplitude $V_{\text{oc}}$ across $R_L = R_r$, the average power is
$\tfrac{1}{2}\,(V_{\text{oc}}/2)^{2}/R_r$.</small>

**2 · Do it for the simplest antenna — a short dipole.** Its effective
length is just its physical length, $\ell_e = \ell$, and its radiation
resistance is $R_r = 80\pi^{2}(\ell/\lambda)^{2}$. The incident power density
is $S = E^{2}/2\eta_{0}$ with $\eta_0 = 120\pi\ \Omega$. Divide, and watch the
$\ell$'s cancel:

$$
A_{e} = \frac{P_{\text{rx}}}{S}
= \frac{\eta_{0}\,\ell_e^{2}}{4 R_r}
= \frac{120\pi\,\ell^{2}}{4\cdot 80\pi^{2}(\ell/\lambda)^{2}}
= \frac{3\lambda^{2}}{8\pi}
= 1.5\cdot\frac{\lambda^{2}}{4\pi}.
$$

<p style="text-align:center;">
<img src="../../viz/img/short-dipole-field.svg"
     alt="Short dipole aligned with the incident E field, inducing an open-circuit voltage"
     style="max-width:100%; width:600px;">
</p>

**3 · Recognize the number.** That $1.5$ is exactly the short dipole's
**directivity** $D$. So $A_e = D\,\lambda^{2}/4\pi$; folding in ohmic losses
($G = \eta_{\text{rad}}D$),

$$
\boxed{A_{e} = \frac{\lambda^{2}}{4 \pi}\, G.}
$$

**4 · It's universal.** We computed only one antenna — but **reciprocity**
guarantees the ratio $A_e/G$ is the *same* constant for *every* antenna, from
a short dipole to a giant dish. (Equivalently, a thermodynamic argument — an
antenna in a blackbody cavity must absorb and re-radiate equally in each
direction — pins down the same constant.) So the boxed relation is truly
universal.

**Physical vs. effective aperture.** An antenna with a real opening of area
$A_{\text{phys}}$ (a horn, a dish) never uses all of it perfectly —
illumination taper, spillover, and feed blockage waste some. The **aperture
efficiency** $\varepsilon_{\text{ap}}$ (typically 0.5–0.7 for a dish)
captures this:

$$
A_{e} = \varepsilon_{\text{ap}}\, A_{\text{phys}}.
$$

**Worked example.** A 1.2 m dish has
$A_{\text{phys}} = \pi(0.6)^{2} = 1.13\ \text{m}^{2}$; with
$\varepsilon_{\text{ap}} = 0.6$ that is $A_{e} = 0.68\ \text{m}^{2}$. At
10 GHz ($\lambda = 3\ \text{cm}$) the gain is
$G = 4\pi A_{e} / \lambda^{2} \approx 9500$, or **39.8 dBi**. A wave of
density $S_{\text{inc}} = 1\ \mu\text{W/m}^{2}$ then delivers
$P_{\text{rx}} = S_{\text{inc}} A_{e} \approx 0.68\ \mu\text{W}$.

**A subtlety worth pinning down.** People often say "effective area shrinks
with frequency," but that is only true if you hold *gain* fixed — then
$A_{e} = (\lambda^{2}/4\pi)\,G$ falls as $\lambda^{2}$. For a **fixed
physical dish**, $A_{e} = \varepsilon_{\text{ap}} A_{\text{phys}}$ is set by
the metal and does *not* change with frequency; instead the **gain climbs
as $f^{2}$**, because the same aperture spans many more wavelengths. Both
statements are the same universal relation read in opposite directions.

Combining $A_{e}$ on the receive end with $G$ on the transmit end gives the
**Friis transmission equation**, the backbone of the link budget and radar
range equation in Module 4.

#### Interactive — compare gain patterns

Toggle antenna types on/off to compare their **E-plane** gain patterns
against an isotropic reference. Slide the dish diameter to watch the
parabolic beam narrow and its peak gain climb — a direct look at how a
larger $A_{\text{phys}} / \lambda^{2}$ buys gain.

<iframe src="../../viz/polar-gain.html"
        width="100%" height="620"
        style="border: 1px solid #cddce9; border-radius: 6px;"
        loading="lazy"
        title="Polar gain patterns">
</iframe>

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
        width="100%" height="660"
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
