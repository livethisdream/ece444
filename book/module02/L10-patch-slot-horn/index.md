# L10 - Patch, Slot, and Horn Antennas

:::{admonition} Slides
:class: slides
<a href="../../slides/L10-patch-slot-horn.html" target="_blank" rel="noopener">html slides</a>
<a href="../../slides/L10-patch-slot-horn.html?print-pdf" target="_blank" rel="noopener">pdf slides</a>
<a href="../../slides/L10-patch-slot-horn.md" target="_blank" rel="noopener">raw markdown slides</a>
:::

## Learning Objectives

<ol class="lo-list lo-sublist" style="--module: '2'; --lo: '3'">
  <li>I can explain how a microstrip patch radiates &mdash; two slots at the edges of a resonant cavity &mdash; and size a rectangular patch for a given frequency and substrate.</li>
  <li>I can describe the slot antenna as the complement of a dipole, state how Babinet's principle relates their polarization and impedance, and name where slots are used.</li>
  <li>I can explain how a horn turns a waveguide mode into a radiating aperture, estimate its gain from the aperture area, and describe the optimum-horn compromise.</li>
  <li>I can choose among patch, slot, and horn for a given application from pattern, bandwidth, power, and integration constraints.</li>
</ol>

Every antenna so far has been a wire. Lesson 7 gave you the resonant dipole, Lesson 9 bent it into
a loop and grounded it into a monopole, and in all of it the current lived on a thin conductor you
could point at. Today the antenna becomes a **surface**, a **hole**, and an **opening**. All three
are things you can build into an airframe or bolt to a waveguide, and all three are read the same
way: name the field in the aperture, and the pattern follows. That is the equivalence-principle
move from Lesson 6, finally cashed in.

## Part 1: The patch is a leaky resonator

A **microstrip patch** is a rectangle of copper of width $W$ and length $L$, etched on a substrate
of thickness $h$ and relative permittivity $\varepsilon_r$, sitting over a solid ground plane. It
costs one etch step. That is most of why it exists.

Electrically it is a **cavity**: the patch and the ground plane are two conductors separated by
$h$, and the two ends are open circuits. Drive it and a half-wave standing wave sets up between
the two open edges, so the patch resonates when its length is about half a wavelength **in the
dielectric**:

$$L \approx \frac{\lambda_d}{2}, \qquad \lambda_d = \frac{\lambda_0}{\sqrt{\varepsilon_{\text{eff}}}}$$

The flat top of the patch is a poor radiator — it is a sheet of metal parallel to a ground plane a
fraction of a wavelength away, which is a transmission line, not an antenna. **The edges are the
antenna.**

Here is the mechanism. Inside the cavity the electric field runs from patch to ground, and because
it is a half-wave standing wave it points **down at one open edge and up at the other**. At each
open edge the field does not stop at the copper; it **fringes** out past it. Decompose each fringe
into a vertical and a horizontal part. The vertical parts at the two edges are opposite, so they
cancel in the far field. The horizontal parts point in the **same** direction, so they add.

:::{admonition} Key Point
:class: key-concept
A patch radiates from **two slots** — the fringing fields at its two open edges, each of width
$W$, spaced $L \approx \lambda_d/2$ apart and driven in phase. Equal path length to broadside
means they add straight up, so the beam is always broadside and never anywhere else. This is the
**two-slot model**, and it is all the physics you need.
:::

The pattern that falls out is a fat hemispherical beam. The ground plane suppresses the back half.
Directivity runs **5 to 8 dBi** — remember 6 — with an H-plane beamwidth near $80^\circ$ and an
E-plane that stays broad, because two slots a third of a free-space wavelength apart cannot form
a narrow beam.

**Feeding it.** The patch edge is a few hundred ohms and the center is a virtual short, so
matching is a question of where you tap the standing wave. An **inset microstrip line** slides the
feed point in from the radiating edge through a pair of etched notches until the impedance reads
$50\ \Omega$ — cheap and coplanar, at the cost of a little feed radiation. A **coaxial probe**
does the same thing with a pin up through the ground plane, which keeps the feed from radiating
but needs a drilled and soldered via. **Aperture coupling** puts the feed line under a second
ground plane and couples through a slot, which isolates the feed and widens the band at the cost
of an extra layer. Same resonator each time; only the tap point changes.

## Part 2: Sizing a patch

Four closed forms take you from a frequency and a substrate to a rectangle of copper. They are
curve fits to measured microstrip behavior — Hammerstad's — not derivations, so use them as design
equations and check the result in a solver.

**Width.** Choose $W$ from the half-power width formula, the standard compromise between
radiation efficiency (wider is better) and exciting unwanted modes (narrower is better):

$$W = \frac{c}{2 f_r}\sqrt{\frac{2}{\varepsilon_r+1}}$$

**Effective permittivity.** Part of the field between patch and ground travels through air, not
substrate, so the wave sees less than $\varepsilon_r$:

$$\varepsilon_{\text{eff}} = \frac{\varepsilon_r+1}{2} + \frac{\varepsilon_r-1}{2}\left(1+\frac{12h}{W}\right)^{-1/2}$$

**Edge extension.** The same fringing that does the radiating also makes the cavity look
electrically longer than the copper, by $\Delta L$ at each end:

$$\frac{\Delta L}{h} = 0.412\ \frac{(\varepsilon_{\text{eff}}+0.3)(W/h+0.264)}{(\varepsilon_{\text{eff}}-0.258)(W/h+0.8)}$$

**Length.** Resonance is set by the *electrical* length, so cut the metal short by $2\Delta L$:

$$L = \frac{c}{2 f_r \sqrt{\varepsilon_{\text{eff}}}} - 2\Delta L$$

That last subtraction looks like a rounding error and is not. $\Delta L$ is typically a few
percent of $L$, and a patch's whole bandwidth is one or two percent. Etch the full $\lambda_d/2$
and the antenna resonates low, by more than its own bandwidth. It will not work.

:::{admonition} Worked example — a 2.45 GHz patch on FR-4
:class: tip
Take $\varepsilon_r = 4.4$, $h = 1.6\ \text{mm}$, $f_r = 2.45\ \text{GHz}$, so
$c/2f_r = 61.2\ \text{mm}$.

**Width.** $W = 61.2\sqrt{2/5.4} = 61.2(0.609) = 37.3\ \text{mm}$.

**Effective permittivity.** $12h/W = 12(1.6)/37.3 = 0.515$, so
$\varepsilon_{\text{eff}} = 2.70 + 1.70(1.515)^{-1/2} = 2.70 + 1.38 = 4.08$.

**Edge extension.** With $W/h = 23.3$,
$\Delta L/h = 0.412(4.381)(23.55)/[(3.823)(24.09)] = 0.462$, so
$\Delta L = 0.74\ \text{mm}$.

**Length.** $L = 61.2/\sqrt{4.08} - 2(0.74) = 30.3 - 1.5 = 28.8\ \text{mm}$.

The answer is a $37 \times 29\ \text{mm}$ rectangle of copper. That is the Wi-Fi antenna inside
half the devices in the room.
:::

**The price is bandwidth.** A high-$Q$ cavity is a narrowband cavity, and a patch is a very high-$Q$
cavity. For VSWR $\le 2$ the fractional bandwidth follows

$$\text{BW} \approx 3.77\ \frac{\varepsilon_r-1}{\varepsilon_r^{2}}\ \frac{h}{\lambda_0}\ \frac{W}{L}$$

Read what that does. Bandwidth is proportional to $h/\lambda_0$ — thicker substrate, more band —
and falls roughly as $1/\varepsilon_r$ once $\varepsilon_r$ is large. So the high-permittivity
substrate that shrinks your patch is also the one that starves it. At 2.45 GHz on 1.6 mm board,
$\varepsilon_r = 2.2$ gives a $48 \times 40\ \text{mm}$ patch with 1.5 % bandwidth, while
$\varepsilon_r = 10.2$ gives a $26 \times 19\ \text{mm}$ patch with 0.6 %. Four times less area,
two and a half times less band. Neither is free.

Drive the designer below. Set a frequency, pick a substrate, and watch the patch redraw itself
inside the fixed free-space half-wave box: the gap between the dashed box and the copper is
exactly what the dielectric bought you. Walk $\varepsilon_r$ up the list and notice two things at
once — the patch shrinks, and the bandwidth pill falls. Then push the thickness slider and watch
the bandwidth come back. The patterns underneath are the two-slot model; note that no control
moves the beam off broadside, because nothing can.

<iframe src="../../viz/patch-designer.html"
        width="100%" height="892"
        style="border: 1px solid #cddce9; border-radius: 6px;"
        loading="lazy"
        title="Rectangular patch designer: substrate versus patch size, bandwidth, and the two-slot pattern">
</iframe>

```{note}
One patch is a 6 dBi element with a fat beam — useless on its own for radar. Its real job is to be
one of hundreds. It is flat, light, conformal, cheap, and identical to its neighbors, which is
exactly the specification an array wants. The PHASER array you drive in Module 3 is a row of patch
elements on a board, and in L16 the patch pattern you just computed becomes the *element factor*
that multiplies the array factor.
```

## Part 3: The slot is a dipole turned inside out

Cut a narrow slit about half a wavelength long in a large conducting sheet and drive it across the
middle. That is a **slot antenna**, and it is the **complement** of the dipole: metal wherever the
dipole is air, air wherever the dipole is metal. Nothing protrudes, so it survives supersonic
airframes, radomes, and anything else that cannot afford a bump.

Complementary structures are linked by **Babinet's principle**, which for antennas takes the form

$$Z_{\text{slot}}\ Z_{\text{dipole}} = \frac{\eta^{2}}{4}$$

One relation, and every dipole result you already own transfers. Three consequences matter.

**Impedance inverts.** With $\eta = 377\ \Omega$, $\eta^2/4 = 3.55\times10^{4}\ \Omega^2$. A
resonant dipole presents about $73\ \Omega$ real, so its complementary slot presents
$3.55\times10^{4}/73 \approx 487\ \Omega$ — the number you will see quoted as **about
485 ohms**. A low-impedance dipole is a high-impedance slot, and feeding one from $50\ \Omega$
takes a real transformer.

**Reactance flips sign.** Inverting a complex impedance flips the sign of its imaginary part. The
untrimmed half-wave dipole at $73 + j42.5\ \Omega$ becomes a slot at $364 - j212\ \Omega$:
inductive dipole, capacitive slot. Since the reactance crosses zero at the same length either way,
a slot resonates at the same electrical length its complementary dipole does.

**Polarization rotates.** The fields swap roles. The dipole's electric field runs **along** the
wire; the slot's electric field runs **across** the cut. So a *horizontal* slot radiates a
*vertically* polarized field. Everyone gets this backwards exactly once — get it over with now.

A slot in a sheet radiates on both sides, which is rarely what you want on an airframe.
**Cavity-backing** boxes one side in, giving a flush, one-sided, roughly hemispherical radiator at
the cost of bandwidth: an open slot is dipole-like at 10 to 20 %, and a cavity-backed one drops to
a few percent. That is the standard aircraft and missile skin antenna.

The other place slots earn their keep is the **waveguide slot array**. Cut a row of slots into the
wall of a waveguide and each one couples out a little of the guided power. The spacing sets where
the beam points and the offset of each slot from the centerline sets how much power it takes,
which means the array's amplitude taper is machined in. Marine and airborne surveillance radars
are built this way. You are looking at a ready-made aperture distribution — the same taper theory
Module 3 develops in L24, implemented with a milling machine.

## Part 4: The horn is an aperture

A waveguide carries a single mode very efficiently and radiates it very badly. Cut a guide off and
the open end is a fraction of a wavelength across and grossly mismatched to free space: most of
the power reflects. **Flare it out** and two things improve together — the mode expands to fill a
large opening, and the impedance transition to free space becomes gradual. What you end up with is
a big, well-illuminated **aperture**, which by the equivalence principle of Lesson 6 is itself the
source: replace the opening with its equivalent surface currents and integrate.

Gain then comes from area, exactly as it did in Lesson 2:

$$G = \eta_{ap}\ \frac{4\pi A}{\lambda^{2}}$$

where $A$ is the physical aperture area and $\eta_{ap}$ is the fraction of it that works.
This is $A_e = G\lambda^2/4\pi$ read right to left. Gain is **area in square wavelengths** — hold
the horn fixed and double the frequency and the gain climbs 6 dB. Horns run
$\eta_{ap} \approx 0.5$; good reflectors reach 0.55 to 0.7.

:::{admonition} Worked example — an X-band horn
:class: tip
A pyramidal horn with a $20 \times 15\ \text{cm}$ aperture at $10\ \text{GHz}$, with
$\eta_{ap} = 0.5$.

$\lambda = 3.0\ \text{cm}$ and $A = 0.030\ \text{m}^2$, so

$$\frac{4\pi A}{\lambda^{2}} = \frac{4\pi(0.030)}{(0.030)^{2}} = 419, \qquad G = 0.5(419) = 209 = 23.2\ \text{dBi}$$

Now check where its far field starts. The largest aperture dimension is the diagonal,
$D = 25\ \text{cm}$, so

$$r \ge \frac{2D^{2}}{\lambda} = \frac{2(0.25)^{2}}{0.030} = 4.2\ \text{m}$$

A hand-sized horn already needs a four-meter range. This is the row that ruins lab schedules.
:::

**Why the flare has to be gradual.** The wave leaving the flare spreads on a roughly **spherical**
front, centered on the horn's virtual apex behind the throat. The aperture, however, is **flat**.
The edge of a flat aperture is farther from the apex than its center, so the field there arrives
late — a quadratic **phase error** across the aperture. Phase error is not benign: it broadens the
main beam, fills in the nulls, raises the sidelobes, and takes gain off the top. Making the horn
longer for the same aperture flattens the wavefront and shrinks the error. Same accounting as the
$2D^2/\lambda$ criterion from Lesson 5, different geometry.

That sets up the trade. Enlarge the aperture at a fixed flare length and $4\pi A/\lambda^2$ rises
while $\eta_{ap}$ falls. Gain climbs, flattens, and then turns over. The **optimum horn**
is that peak: the shortest horn for a given aperture whose edge phase error is still tolerable,
about $\lambda/4$ in the E-plane and $3\lambda/8$ in the H-plane. At the optimum the aperture
efficiency lands near 0.5, which is where the 0.5 you have been using comes from. Half your
aperture is the rent you pay for a horn short enough to carry.

:::{admonition} Key Point
:class: key-concept
Aperture buys gain; phase error spends it. $\eta_{ap} \approx 0.5$ for a horn is not a
fudge factor — it is the value at a deliberate design optimum.
:::

A **standard-gain horn** is a horn built to that optimum design, measured at the factory, and
tabulated across its band to a few tenths of a dB. It is not a good communication antenna. It is a
**known** antenna, and that is the entire point: in L12 you will measure an unknown antenna's gain
by comparing it against a standard-gain horn on the same range. It is the ruler.

## Part 5: Choosing among the three

| | Patch | Slot | Horn |
| :-- | :-- | :-- | :-- |
| What radiates | fringing fields at two edges | the field across a cut | a flared, illuminated opening |
| Pattern | broadside hemisphere, always | dipole-like; one-sided if cavity-backed | directive pencil or fan beam |
| Gain | 5–8 dBi | 2–5 dBi | 10–25 dBi |
| Bandwidth | 1–5 % (thin substrate) | 10–20 %; a few % cavity-backed | an octave or more |
| Power handling | low | moderate | high — it is waveguide |
| Integration | printed, planar, arrays almost free | flush in an existing conducting skin | bulky, 3-D, needs a waveguide feed |
| Typical uses | GPS, Wi-Fi, phased-array elements | aircraft and missile skins, waveguide slot arrays for marine radar | range references, reflector feeds, chamber sources |

Read it as three answers to three different questions. *How do I get an antenna onto a circuit
board and copy it four hundred times?* Patch. *How do I put an antenna on something moving at
Mach 2?* Slot. *How do I get 20 dBi with a gain I can trust to a few tenths of a dB?* Horn.

## Summary

| Symbol / idea | Meaning | Number to keep |
| :-- | :-- | :-- |
| $L \approx \lambda_d/2$ | patch resonates as a half-wave cavity in the dielectric | shorten by $2\Delta L$ |
| $\varepsilon_{\text{eff}}$ | permittivity the wave actually sees (part of it is in air) | between 1 and $\varepsilon_r$ |
| two-slot model | patch radiates from the two fringing edges, in phase | broadside, 5–8 dBi |
| patch bandwidth | rises with $h/\lambda_0$, falls with $\varepsilon_r$ | 1–5 %, few % typical |
| $Z_{\text{slot}} Z_{\text{dipole}} = \eta^2/4$ | Babinet complementarity | resonant slot $\approx 485\ \Omega$ |
| slot polarization | field runs across the cut, not along it | horizontal slot, vertical polarization |
| $G = \eta_{ap} 4\pi A/\lambda^2$ | aperture gain | horns $\eta_{ap} \approx 0.5$ |
| optimum horn | shortest horn whose edge phase error is still tolerable | $\lambda/4$ E-plane, $3\lambda/8$ H-plane |
| standard-gain horn | calibrated reference for gain measurement | used in L12 |

## Practice

- <a href="../../practice/ECE444_L10_Practice_blank.pdf" target="_blank" rel="noopener">Problem set (PDF)</a>
- <a href="../../practice/ECE444_L10_Practice_SOLUTIONS.pdf" target="_blank" rel="noopener">Solutions (PDF)</a>

## Where this is going

Three antennas, and only one of them clears 10 dBi. L11 goes after the rest: reflectors, Yagis,
and arrays — the three standard routes to a big electrical aperture, and how each of them pays for
it. L12 then turns the horn around and uses it as an instrument, measuring pattern and gain
against a calibrated reference on a range whose length you now know how to compute.

The patch has the longer tail. Module 3 is built on the idea that a hundred cheap, identical,
low-gain elements beat one expensive high-gain one, because you can steer the hundred without
moving anything. The element in that story is the antenna you sized today, and every number in
Part 2 comes back when its pattern becomes the element factor in L16.
