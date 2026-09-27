---
frame_view: true
---

# L13 - Patch, Slot, and Horn Antennas

::::{frame}
:class: title-frame

<div class="course-mark">ECE 444 · Fall 2026</div>

<h1 class="frame-title">Patch, Slot, and Horn Antennas</h1>

<div class="title-rule"></div>

Today the antenna becomes a surface, a hole, and an opening.

Lesson 13 · Antennas, Phased Arrays, and Radar Systems · Dr. Neil Rogers
::::

::::{frame} Slides
:class: read-only

:::{admonition} Slides
:class: slides
<a href="../../slides/L13-patch-slot-horn.html" target="_blank" rel="noopener">html slides</a>
<a href="../../slides/L13-patch-slot-horn.html?print-pdf" target="_blank" rel="noopener">pdf slides</a>
<a href="../../slides/L13-patch-slot-horn.md" target="_blank" rel="noopener">raw markdown slides</a>
:::
::::

::::{frame} Learning Objectives

<ol class="lo-list lo-sublist" style="--module: '2'; --lo: '3'">
  <li>I can explain how a microstrip patch radiates &mdash; two slots at the edges of a resonant cavity &mdash; and size a rectangular patch for a given frequency and substrate.</li>
  <li>I can describe the slot antenna as the complement of a dipole, state how Babinet's principle relates their polarization and impedance, and name where slots are used.</li>
  <li>I can explain how a horn turns a waveguide mode into a radiating aperture, estimate its gain from the aperture area, and describe the optimum-horn compromise.</li>
  <li>I can choose among patch, slot, and horn for a given application from pattern, bandwidth, power, and integration constraints.</li>
</ol>

:::{depth}
Every antenna so far has been a wire. Lesson 7 developed the resonant dipole,
and Lesson 12 bent it into a loop and grounded it into a monopole; in each case
the current flowed on a thin conductor. Today the antenna becomes a
**surface**, a **hole**, and an **opening**. All three can be built into an
airframe or bolted to a waveguide, and we analyze all three the same way: once
we know the field in the aperture, the equivalence principle of Lesson 6 gives
the pattern.

We have already used one of the three on the bench. The standard-gain horn
that served as the gain reference in Lesson 11 is the last antenna in this
lesson, and we will see why its gain is known to a few tenths of a dB.
:::
::::

::::{frame} The Patch Is a Printed Half-Wave Cavity
:::{present}
$$L \approx \frac{\lambda_d}{2}, \qquad \lambda_d = \frac{\lambda_0}{\sqrt{\varepsilon_{\text{eff}}}}$$

- A $W \times L$ copper rectangle sits over a ground plane, made in one etch step.
- The patch and the ground form a cavity with two open ends.
- The edges are the antenna. The flat top is a transmission line.
:::

A **microstrip patch** sits on a substrate of thickness $h$ and relative
permittivity $\varepsilon_r$. It takes one etch step to make, which is the
main reason it is so common. When we drive it, a half-wave standing wave forms
between the two open edges, so it resonates when its length is about half a
wavelength *in the dielectric*. The flat top of the patch is a poor radiator,
because a sheet of metal a fraction of a wavelength above a ground plane is a
transmission line rather than an antenna.
::::

::::{frame} Why It Radiates: Two Slots
:::{present}
:class: callout
A patch radiates from **two slots**: the fringing fields at its open edges,
driven in phase.
:::
:::{present}
- Equal path lengths keep the beam broadside.
- The ground plane suppresses the back hemisphere.
- Directivity is 5 to 8 dBi, typically 6.
:::

Inside the cavity the electric field runs from patch to ground, and because it
is a half-wave standing wave it points down at one open edge and up at the
other. At each open edge the field does not stop at the copper; it **fringes**
out past it. Decompose each fringe into a vertical and a horizontal part: the
vertical parts at the two edges are opposite and cancel in the far field,
while the horizontal parts point the same way and add.

The two-slot model accounts for both the shape of the pattern and its
direction. The H-plane beamwidth lands near $80^\circ$ and the E-plane stays
broad, because two slots about a quarter of a free-space wavelength apart
cannot form a narrow beam.
::::

::::{frame} Feeding a Patch
:::{present}
- **Inset line**: slide the feed in through etched notches until it reads $50\ \Omega$.
- **Coaxial probe**: a pin through the ground plane; the feed does not radiate.
- **Aperture coupling**: couple through a slot from a buried line.
:::

The patch edge presents a few hundred ohms and the center is a virtual short,
so we match the patch by choosing where to tap the standing wave. The inset
feed is inexpensive and coplanar, but the feed line radiates a little; the
probe does not radiate but requires a drilled and soldered via; aperture
coupling isolates the feed and widens the band but adds a layer. The resonator
is the same in each case, and only the tap point changes.
::::

::::{frame} Sizing a Patch
:::{present}
$$\begin{aligned}
W &= \frac{c}{2 f_r}\sqrt{\frac{2}{\varepsilon_r+1}} \\
L &= \frac{c}{2 f_r \sqrt{\varepsilon_{\text{eff}}}} - 2\Delta L
\end{aligned}$$

- $\varepsilon_{\text{eff}}$: part of the field is in air.
- $\Delta L$: fringing makes the cavity look longer.
:::
:::{present}
:class: callout
$\Delta L$ is a few percent of $L$, more than a patch's whole bandwidth, so
the correction is required.
:::

A patch etched to the full $\lambda_d/2$ resonates below $f_r$ by more than
its own bandwidth, so it is mismatched at the design frequency.

:::{depth}
The two intermediate closed forms are Hammerstad curve fits to measured
microstrip behavior rather than derivations, so we use them as design equations
and check the result in a solver:

$$\begin{aligned}
\varepsilon_{\text{eff}} &= \frac{\varepsilon_r+1}{2} + \frac{\varepsilon_r-1}{2}\left(1+\frac{12h}{W}\right)^{-1/2} \\
\frac{\Delta L}{h} &= 0.412\ \frac{(\varepsilon_{\text{eff}}+0.3)(W/h+0.264)}{(\varepsilon_{\text{eff}}-0.258)(W/h+0.8)}
\end{aligned}$$

The width formula is the standard compromise between radiation efficiency
(wider is better) and exciting unwanted modes (narrower is better).
:::
::::

::::{frame} Worked Example — a 2.45 GHz Patch on FR-4
:class: read-only

Take $\varepsilon_r = 4.4$, $h = 1.6\ \text{mm}$, $f_r = 2.45\ \text{GHz}$, so
$c/2f_r = 61.2\ \text{mm}$.

**Width.** $W = 61.2\sqrt{2/5.4} = 61.2(0.609) = 37.3\ \text{mm}$.

**Effective permittivity.** $12h/W = 12(1.6)/37.3 = 0.515$, so
$\varepsilon_{\text{eff}} = 2.70 + 1.70(1.515)^{-1/2} = 2.70 + 1.38 = 4.08$.

**Edge extension.** With $W/h = 23.3$,
$\Delta L/h = 0.412(4.381)(23.55)/[(3.823)(24.09)] = 0.462$, so
$\Delta L = 0.74\ \text{mm}$.

**Length.** $L = 61.2/\sqrt{4.08} - 2(0.74) = 30.3 - 1.5 = 28.8\ \text{mm}$.

The design is a $37 \times 29\ \text{mm}$ rectangle of copper, which is the
size of the Wi-Fi antenna in a typical laptop or access point.
::::

::::{frame} Patch Bandwidth
:::{present}
$$\text{BW} \approx 3.77\ \frac{\varepsilon_r-1}{\varepsilon_r^{2}}\ \frac{h}{\lambda_0}\ \frac{W}{L}$$

- Bandwidth rises with $h/\lambda_0$ and falls with $\varepsilon_r$.
- A higher $\varepsilon_r$ shrinks the patch and narrows its bandwidth.
:::
:::{present}
- At 2.45 GHz on 1.6 mm: $\varepsilon_r = 2.2$ gives $48 \times 40$ mm at 1.5%.
- $\varepsilon_r = 10.2$ gives $26 \times 19$ mm at 0.6%.
:::

A high-$Q$ cavity is a narrowband cavity, and a patch is a very high-$Q$
cavity. Moving from $\varepsilon_r = 2.2$ to $10.2$ reduces the patch area by
a factor of four and the bandwidth by a factor of two and a half. The formula
gives the bandwidth for VSWR $\le 2$, the same bar we read off a trace in
Lesson 10.
::::

::::{frame} Substrate Against Size and Bandwidth
:class: viz-frame

:::{present}
<iframe src="../../viz/patch-designer.html"
        width="100%" height="533"
        style="border: 1px solid #cddce9; border-radius: 6px;"
        loading="lazy"
        title="Rectangular patch designer: substrate versus patch size, bandwidth, and the two-slot pattern">
</iframe>
:::

:::{depth}
Set a frequency and pick a substrate, and the designer redraws the patch
inside the fixed free-space half-wave box: the gap between the dashed box and
the copper is the size reduction the dielectric provides. As $\varepsilon_r$
steps up the list, the patch shrinks and the bandwidth pill falls. Increasing
the thickness restores the bandwidth. The patterns underneath are the two-slot model; note that
no control moves the beam off broadside, because the two slots always add in
phase along the normal. The red edges on the top view are the radiating slots;
the "dielectric half-wave" figure compares the in-substrate half-wavelength to
the free-space one shown by the dashed box.
:::
::::

::::{frame} Why Patches Become Array Elements
:::{present}
- One patch is a 6 dBi element with a broad beam, too little gain for a radar.
- Hundreds of patches etch in one step, each flat, light, conformal, and identical.
:::

Identical elements are what an array needs. The PHASER array we use in
Module 3 is a row of patch elements on a board, and in Lesson 16 the patch
pattern from this lesson becomes the *element factor* that multiplies the
array factor.
::::

::::{frame} The Slot Antenna
:::{present}
$$Z_{\text{slot}}\ Z_{\text{dipole}} = \frac{\eta_0^{2}}{4}$$

- A slot is a half-wave slit in a conducting sheet, driven across the middle.
- It is the **complement** of a dipole: metal where the dipole is air.
- Nothing protrudes, so it can sit flush on a supersonic airframe.
:::

**Babinet's principle** relates complementary structures, and that one
relation carries the dipole results of Lesson 7 over to the slot. Three
consequences matter, and students most often get the third one backwards.
::::

::::{frame} Consequences of Complementarity
:::{present}
- The **impedance** inverts: a $73\ \Omega$ dipole corresponds to a $487\ \Omega$ slot.
- The **reactance** flips sign: $73 + j42.5\ \Omega$ becomes $364 - j212\ \Omega$.
:::
:::{present}
:class: callout
The **polarization** rotates: the slot's electric field runs *across* the
cut, so a horizontal slot radiates a vertically polarized field.
:::

With $\eta_0 = 377\ \Omega$, $\eta_0^2/4 = 3.55\times10^{4}\ \Omega^2$, which
is where the number quoted as "about 485 ohms" comes from. A low-impedance
dipole is a high-impedance slot, and feeding one from $50\ \Omega$ needs a
matching transformer. Inverting a complex impedance flips the sign of its
imaginary part, so an inductive dipole is a capacitive slot — but since the
reactance crosses zero at the same length either way, a slot resonates at the
same electrical length its complementary dipole does.
::::

::::{frame} Slots in Service
:::{present}
- **Cavity-backing** makes a slot one-sided and flush: the standard skin antenna.
- Backing narrows the band from 10 to 20% to a few percent.
- A **waveguide slot array** machines the amplitude taper into the wall.
:::

A slot in a sheet radiates on both sides, which is rarely acceptable on an
airframe. Enclosing one side in a cavity gives a flush, one-sided, roughly
hemispherical radiator.

The other major application is the waveguide slot array. A row of slots
cut into the wall of a waveguide each couples out a little of the guided
power: the spacing sets where the beam points, and the offset of each slot
from the centerline sets how much power it takes. Marine and airborne
surveillance radars are built this way, and the result is a ready-made
aperture distribution — the same taper theory Module 3 develops in Lesson 24,
realized in the geometry of a machined wall.
::::

::::{frame} The Horn Antenna
:::{present}
- An open-ended waveguide is a fraction of a wavelength across and badly mismatched to free space.
- Flaring the walls expands the mode and makes the impedance transition gradual.
- The result is a large, well-illuminated **aperture**.
:::

A waveguide carries a single mode efficiently but radiates it poorly, because
most of the power reflects at an open end. By the equivalence principle of
Lesson 6 the flared opening is itself the source: we replace it with its
equivalent surface currents and integrate.
::::

::::{frame} Gain Is Area in Square Wavelengths
:::{present}
$$G = \eta_{\text{ap}}\ \frac{4\pi A}{\lambda^{2}}$$

- This is $A_e = G\lambda^2/4\pi$ from Lesson 2, read right to left.
- Doubling the frequency on a fixed horn raises the gain by **6 dB**.
- Horns run $\eta_{\text{ap}} \approx 0.5$; good reflectors reach 0.55 to 0.7.
:::

$A$ is the physical aperture area and $\eta_{\text{ap}}$ is the fraction of it
that contributes to the gain. The next two frames show that the horn's
geometry sets the 0.5; it is not a fudge factor.
::::

::::{frame} Worked Example — an X-Band Horn
:class: read-only

A pyramidal horn with a $20 \times 15\ \text{cm}$ aperture at
$10\ \text{GHz}$, with $\eta_{\text{ap}} = 0.5$. Here $\lambda = 3.0\ \text{cm}$
and $A = 0.030\ \text{m}^2$, so

$$\frac{4\pi A}{\lambda^{2}} = \frac{4\pi(0.030)}{(0.030)^{2}} = 419, \qquad G = 0.5(419) = 209 = 23.2\ \text{dBi}$$

Next we find where its far field starts. The largest aperture dimension is the
diagonal, $D = 25\ \text{cm}$, so

$$r \ge \frac{2D^{2}}{\lambda} = \frac{2(0.25)^{2}}{0.030} = 4.2\ \text{m}$$

Even a horn this small needs a $4.2\ \text{m}$ range. The far-field distance
is the constraint that most often sets the layout of a measurement range, and
it is the same calculation we ran for the bench range in Lesson 11.
::::

::::{frame} Phase Error in the Aperture
:::{present}
- The wave leaves the apex on a **spherical** front, but the aperture is **flat**.
- The edge is farther from the apex, so its field arrives late.
- This quadratic phase error broadens the beam, fills the nulls, and reduces the gain.
:::

Making the horn longer for the same aperture flattens the wavefront and
reduces the error. This is the same reasoning as the $2D^2/\lambda$ criterion
from Lesson 9, in a different geometry: there the curvature came from a source
too close, here from an apex too near the mouth, and in both cases the
tolerance is written as a fraction of a wavelength across the aperture.
::::

::::{frame} The Optimum Horn
:::{present}
- At fixed length, a larger aperture lowers $\eta_{\text{ap}}$, so gain peaks and then falls.
- The peak is the **optimum horn**: edge phase error $\lambda/4$ (E), $3\lambda/8$ (H).
:::
:::{present}
:class: callout
Area sets a horn's maximum gain; phase error sets how much it reaches.
:::

At the optimum, $\eta_{\text{ap}} \approx 0.5$: the design gives up about half
the aperture to keep the horn short enough to be practical.
::::

::::{frame} The Standard-Gain Horn
:::{present}
- It is a horn built to the optimum design, with gain measured at the factory and tabulated across its band.
- Its value is not performance but a **known** gain.
:::

We used one in Lesson 11 as the reference whose $15.0\ \text{dBi}$ we
subtracted to find the gain of our own antenna. Its calibration was the only
absolute gain in that measurement, and it is accurate to a few tenths of a dB
because a horn at the optimum design is the one aperture antenna whose
efficiency is predictable enough to certify.
::::

::::{frame} Choosing Among the Three
:::{present}
| | Patch | Slot | Horn |
| :-- | :-- | :-- | :-- |
| Gain | 5–8 dBi | 2–5 dBi | 10–25 dBi |
| Bandwidth | 1–5% | 10–20% | an octave |
| Power | low | moderate | high |
| Integration | printed | flush in a skin | bulky, 3-D |
:::

Read it as three answers to three different design problems. To get an antenna
onto a circuit board and copy it four hundred times, choose the patch. To put
one on an airframe at Mach 2, choose the slot. To get 20 dBi with a gain
trustworthy to a few tenths of a dB, choose the horn.

:::{depth}
The fuller comparison:

| | Patch | Slot | Horn |
| :-- | :-- | :-- | :-- |
| What radiates | fringing fields at two edges | the field across a cut | a flared, illuminated opening |
| Pattern | broadside hemisphere, always | dipole-like; one-sided if cavity-backed | directive pencil or fan beam |
| Gain | 5–8 dBi | 2–5 dBi | 10–25 dBi |
| Bandwidth | 1–5 % (thin substrate) | 10–20 %; a few % cavity-backed | an octave or more |
| Power handling | low | moderate | high (waveguide-fed) |
| Integration | printed, planar, arrays etched in one step | flush in an existing conducting skin | bulky, 3-D, needs a waveguide feed |
| Typical uses | GPS, Wi-Fi, phased-array elements | aircraft and missile skins, waveguide slot arrays for marine radar | range references, reflector feeds, chamber sources |
:::
::::

::::{frame} Summary
:class: read-only

| Symbol / idea | Meaning | Number to keep |
| :-- | :-- | :-- |
| $L \approx \lambda_d/2$ | patch resonates as a half-wave cavity in the dielectric | shorten by $2\Delta L$ |
| $\varepsilon_{\text{eff}}$ | effective permittivity of the substrate and air | between 1 and $\varepsilon_r$ |
| two-slot model | patch radiates from the two fringing edges, in phase | broadside, 5–8 dBi |
| patch bandwidth | rises with $h/\lambda_0$, falls with $\varepsilon_r$ | 1–5 %, few % typical |
| $Z_{\text{slot}} Z_{\text{dipole}} = \eta_0^2/4$ | Babinet complementarity | resonant slot $\approx 485\ \Omega$ |
| slot polarization | field runs across the cut, not along it | horizontal slot, vertical polarization |
| $G = \eta_{\text{ap}} 4\pi A/\lambda^2$ | aperture gain | horns $\eta_{\text{ap}} \approx 0.5$ |
| optimum horn | shortest horn whose edge phase error is tolerable | $\lambda/4$ E-plane, $3\lambda/8$ H-plane |
| standard-gain horn | calibrated reference for gain measurement | the Lesson 11 reference |
::::

::::{frame} Practice
:class: read-only doc-links

- <a class="doc-link" href="../../practice/ECE444_L13_Practice_blank.pdf" target="_blank" rel="noopener">Problem set (PDF)</a>
- <a class="doc-link doc-key" href="../../practice/ECE444_L13_Practice_SOLUTIONS.pdf" target="_blank" rel="noopener">Solutions (PDF)</a>
::::

::::{frame} Where This Is Going
:::{present}
- Of the three, only the horn clears 10 dBi.
- Lesson 14 goes after the rest: **reflectors, Yagis, and arrays**.
- Each reaches a large electrical aperture by a different route, with different size and bandwidth.
:::

Lesson 14 also closes Module 2, and it is the last new material before the
midterm is due.

:::{depth}
The patch is the one we will keep using. Module 3 builds on the idea that a
hundred inexpensive, identical, low-gain elements can outperform one high-gain
antenna, because we can steer the array electronically without moving
anything. The element in that array is the patch we sized today, and its
pattern becomes the element factor in Lesson 16.
:::
::::
