---
frame_view: true
---

# L13 - Patch, Slot, and Horn Antennas

::::{frame}
:class: title-frame

<div class="course-mark">ECE 444 · Fall 2026</div>

<h1 class="frame-title">Patch, Slot, and Horn Antennas</h1>

<div class="title-rule"></div>

The patch and the slot are resonant antennas; the horn is a traveling-wave antenna.

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
Lesson 3 sorted antennas into two families by what happens when the wave
reaches the end of the structure. In a **resonant** antenna it reflects, the
outgoing and reflected waves form a standing wave, and the antenna works only
near the frequency where that standing wave fits, so its band is narrow. In a
**traveling-wave** antenna the wave leaves the structure instead of coming
back, so there is no sharp resonance and the band is wide.

The dipole of Lesson 7 and the loop and monopole of Lesson 12 are resonant
wires. Today covers three antennas that are not wires. The **patch** and the
**slot** are resonant, like the dipole, and both are narrowband. The **horn**
is a traveling-wave antenna: the wave in a waveguide flows out through a
flared opening without reflecting, and a standard-gain horn covers an octave.

We have already used the horn on the bench. The standard-gain horn that
served as the gain reference in Lesson 11 is the last antenna in this lesson,
and we will see why its gain is known to a few tenths of a dB.
:::
::::

::::{frame} The Patch: A Half-Wave Line Open at Both Ends
:::{present}
<img src="../../viz/img/L13-patch-standing-wave.svg"
     alt="Side view of a patch over a ground plane: a wave travels along the patch and reflects from each open end, so the field between patch and ground is a standing wave, largest at the ends and zero at the center, and it fringes out past the two ends"
     style="max-width: 560px; width: 100%; display: block; margin: 0 auto;">
:::
:::{present}
- The patch and the ground plane are a short, wide microstrip line.
- The wave reflects from both open ends and forms a standing wave.
- Resonance: $L \approx \lambda_d/2$, half a wavelength in the substrate.
:::

A **microstrip patch** is a copper rectangle, $W$ wide and $L$ long, on a
substrate of thickness $h$ and relative permittivity $\varepsilon_r$, with a
solid ground plane on the back. It takes one etch step to make, which is the
main reason it is so common.

The easiest way to understand it is as a transmission line. The patch and the
ground plane under it are two conductors carrying equal and opposite
currents, exactly like a microstrip line on a circuit board, only much wider
and much shorter. A transmission line does not radiate: the fields of the two
opposite currents cancel at any distance large compared with the spacing $h$,
which is why a coax or a microstrip trace can carry power without losing it
to radiation. So the flat top of the patch does not radiate either.

The line is open at both ends. Lesson 3's resonant antenna is the model: a
wave launched along the patch reflects from the far open end, comes back,
reflects from the near one, and the two directions add to a standing wave.
When $L$ is half a wavelength *in the substrate*,

$$\lambda_d = \frac{\lambda_0}{\sqrt{\varepsilon_{\text{eff}}}}$$

the reflections reinforce and the patch resonates. The electric field between
patch and ground is then largest at the two ends, pointing down at one and up
at the other, and zero at the center. Textbooks often call this structure a
**cavity**: the patch and the ground are its top and bottom walls, and the two
ends are open.

At an open end the field is not confined between the conductors. It
**fringes** out past the edge of the copper into the space above the board,
and that fringing field is what radiates. This is what "the edges are the
antenna" means: the middle of the patch is a transmission line, and all of the
radiation comes from the field that leaks out at the ends.
::::

::::{frame} Two Radiating Edges, Not Four
:::{present}
<img src="../../viz/img/L13-patch-edges.svg"
     alt="Top view of a patch with the fringing field drawn on all four edges: uniform and pointing the same way along the two ends, reversing halfway along the two sides"
     style="max-width: 460px; width: 100%; display: block; margin: 0 auto;">
:::
:::{present}
- Along each end the field is uniform, and both ends point the same way, so they add.
- Along each side the field reverses halfway, so the two halves cancel.
- The beam points broadside, 5 to 8 dBi, typically 6.
:::

A rectangle has four edges, and the field fringes past all of them. What
decides whether an edge radiates is how the field varies *along* it.

The standing wave runs along $L$. Along each of the two ends, which are $W$
long, the field has the same strength and direction everywhere, so the whole
edge radiates in phase, like a slot $W$ long. The two ends are called the
**radiating edges**, and the patch is modeled as **two slots** a distance $L$
apart.

Along each of the two sides, which are $L$ long, the field follows the
standing wave: outward near one end, zero at the middle, and inward near the
other end. The two halves of each side are equal and opposite, so broadside
their contributions cancel. These are the **non-radiating edges**. They are
not perfectly silent off broadside, and they are the main source of the
patch's cross-polarized radiation, but the pattern comes from the two ends.

<img src="../../viz/img/L13-patch-fringing.svg"
     alt="Side view of a patch: the field inside points down at one open edge and up at the other, and at each edge the fringing field curls out past the copper; the horizontal parts at the two edges point the same way and add toward broadside"
     style="max-width: 560px; width: 100%; display: block; margin: 1em auto;">

The side view shows why the two ends add even though the field between the
plates points down at one end and up at the other. Decompose each fringing
field into a vertical and a horizontal part: the vertical parts at the two
ends are opposite and cancel in the far field, while the horizontal parts
point the same way and add.

The two-slot model accounts for both the shape of the pattern and its
direction. The two slots are equidistant from any point straight overhead, so
the beam always points broadside, and the ground plane suppresses the back
hemisphere. The H-plane beamwidth lands near $80^\circ$ and the E-plane stays
broad, because two slots about a quarter of a free-space wavelength apart
cannot form a narrow beam.
::::

::::{frame} Sizing a Patch
:::{present}
$$\begin{aligned}
W &= \frac{c}{2 f_r}\sqrt{\frac{2}{\varepsilon_r+1}} \\
L &= \frac{c}{2 f_r \sqrt{\varepsilon_{\text{eff}}}} - 2\Delta L
\end{aligned}$$
:::
:::{present}
- $L$ sets the frequency: a 1% error in $L$ moves it 1%, about the whole bandwidth.
- $W$ sets the edge resistance and the efficiency.
- $\Delta L$ is the fringing correction; omitting it detunes the patch.
:::

The dimensions matter for three reasons.

**The length sets the frequency.** The patch resonates when $L$ is half a
wavelength in the substrate, so the resonant frequency is inversely
proportional to $L$: a length 1% too long resonates 1% low. A patch's whole
bandwidth is only one or two percent, so the length has to be right to a
fraction of a percent. That is also why the fringing correction matters. The
fringing field extends each end by $\Delta L$, which is a few percent of $L$,
so a patch etched to the full $\lambda_d/2$ resonates below $f_r$ by more
than its own bandwidth and is mismatched at the design frequency.

**The width sets the impedance and the efficiency.** Each radiating edge is a
slot $W$ long, and a longer slot radiates more easily, so a wider patch has a
lower edge resistance and radiates more of its power before it is lost in the
substrate. Too wide, and the patch can resonate across its width as well. The
width formula is the standard compromise.

**The overall size decides where the patch fits.** A patch on a
high-permittivity substrate is smaller, which matters in a handset and
matters more in an array, where the elements sit about half a free-space
wavelength apart and each one has to fit in its cell. Shrinking the patch
narrows its bandwidth, as the frames after the worked example show.

:::{depth}
Here $\varepsilon_{\text{eff}}$ is the permittivity the wave actually
sees: part of the field runs through the substrate and part through the air
above it, so $\varepsilon_{\text{eff}}$ lies between 1 and
$\varepsilon_r$. The two intermediate closed forms are Hammerstad curve fits
to measured microstrip behavior rather than derivations, so we use them as
design equations and check the result in a solver:

$$\begin{aligned}
\varepsilon_{\text{eff}} &= \frac{\varepsilon_r+1}{2} + \frac{\varepsilon_r-1}{2}\left(1+\frac{12h}{W}\right)^{-1/2} \\
\frac{\Delta L}{h} &= 0.412\ \frac{(\varepsilon_{\text{eff}}+0.3)(W/h+0.264)}{(\varepsilon_{\text{eff}}-0.258)(W/h+0.8)}
\end{aligned}$$
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

::::{frame} Where to Tap the Standing Wave
:::{present}
<img src="../../viz/img/L13-patch-feed-position.svg"
     alt="Input resistance of the 2.45 GHz FR-4 patch against feed position: about 320 ohms at the radiating edge, falling to zero at the center, and crossing 50 ohms 10.7 mm in from the edge"
     style="max-width: 560px; width: 100%; display: block; margin: 0 auto;">
:::
:::{present}
- The voltage is largest at the ends and zero at the center.
- So the input resistance falls from about $320\ \Omega$ at the edge to zero.
- $50\ \Omega$ lies $10.7$ mm in from the edge of our design.
:::

Feeding a patch is an impedance-matching problem, and the standing wave
solves it. At the radiating edge the voltage between patch and ground is at
its maximum and the current is near zero, so the impedance is high: a few
hundred ohms. At the center the voltage is zero and the current is at its
maximum, so the impedance is zero, a virtual short. Between the two the input
resistance follows

$$R_{\text{in}}(y_0) = R_{\text{edge}}\cos^2\left(\frac{\pi y_0}{L}\right)$$

where $y_0$ is the distance of the feed point in from the radiating edge.
Somewhere between edge and center it passes through $50\ \Omega$, and that is
where we connect the feed.

For the $2.45\ \text{GHz}$ FR-4 design, the transmission-line model gives
$R_{\text{edge}} \approx 320\ \Omega$ and puts the $50\ \Omega$ point
$10.7\ \text{mm}$ in from the edge, a little over a third of the way to the
center. Substrate loss lowers the edge resistance of a real FR-4 patch, so the
measured point sits somewhat closer to the edge; a solver or a trim on the
bench finds it.
::::

::::{frame} Three Ways to Feed a Patch
:::{present}
<img src="../../viz/img/L13-patch-feeds.svg"
     alt="Three ways to feed a patch: an inset microstrip line that reaches into the patch through two notches; a coaxial probe whose pin comes up through the ground plane and the substrate; and aperture coupling, where a feed line on a second board below the ground plane couples through a slot in the ground plane"
     style="max-width: 760px; width: 100%; display: block; margin: 0 auto;">

- **Inset line**: notches let a printed line reach the $50\ \Omega$ point.
- **Coaxial probe**: a pin from below touches the patch at that point.
- **Aperture coupling**: a line on a second board couples through a ground-plane slot.
:::

All three feeds connect to the same resonator at, or near, the same
$50\ \Omega$ point; they differ in how they get there.

The **inset line** is printed in the same etch step as the patch. Two notches
cut into the radiating edge let the microstrip line reach in to the
$50\ \Omega$ point without touching the patch on either side. It is the
least expensive feed and keeps everything on one side of the board, but the
feed line is itself a conductor above the ground plane, and it radiates a
little.

The **coaxial probe** comes up from behind. The coax's outer conductor is
soldered to the ground plane, and its center pin passes through a hole in the
substrate and is soldered to the patch at the $50\ \Omega$ point. The feed
is behind the ground plane, so it does not radiate, but every element needs a
drilled and soldered connection.

**Aperture coupling** uses two circuit boards. The patch sits on the top
board. The ground plane is between the two boards and has a small slot cut in
it under the patch. The feed line runs on the bottom board, below the ground
plane, and crosses under the slot, and the field of the line couples up
through the slot to the patch. Nothing touches the patch. The ground plane
shields the feed network from the radiating side, and the slot's own
resonance widens the band, but the design needs a second layer.
::::

::::{frame} The Patch Designer
:class: viz-frame

:::{present}
<iframe src="../../viz/patch-designer.html"
        width="100%" height="562"
        style="border: 1px solid #cddce9; border-radius: 6px;"
        loading="lazy"
        title="Rectangular patch designer: the patch to scale with its feed point, VSWR against frequency, and the two-slot pattern">
</iframe>
:::

:::{depth}
Pick a frequency, a substrate, and a thickness, and the designer sizes the
patch with the design set above. The top view is drawn to scale inside the
dashed outline of the same patch built in air, so the difference between the
two is the size reduction the substrate provides. The shading along the patch
is the standing wave, strongest at the two radiating edges and zero at the
center, and the inset feed reaches in to the $50\ \Omega$ point.

The VSWR curve shows the bandwidth. Step $\varepsilon_r$ up the list and the
dip narrows; increase the thickness and it widens again. The **length error**
control etches the patch longer or shorter than the design. At $+5\%$, about
the size of the $2\Delta L$ correction for the FR-4 design, the resonance
moves below the band and the VSWR at the design frequency climbs past 5. That
is why the length has to be right to a fraction of a percent.

The patterns are the two-slot model. No control moves the beam off
broadside, because the two radiating edges always add in phase along the
normal. The model assumes an infinite ground plane, so the E-plane stays broad
out to the horizon; a real, finite ground plane rolls it off and puts a few dB
of radiation behind the board. The VSWR curve treats the patch near resonance
as a parallel resonant circuit matched at its own resonant frequency, with its
$Q$ set so that the VSWR $\le 2$ band equals the closed-form bandwidth.
:::
::::

::::{frame} Why Patches Become Array Elements
:::{present}
<img src="../../viz/img/L13-patch-array.svg"
     alt="Left: one patch and its broad beam, about 6 dBi and fixed at broadside. Right: eight patches in a row on one board, half a wavelength apart, each behind its own phase shifter, forming a narrow beam steered 20 degrees off broadside"
     style="max-width: 720px; width: 100%; display: block; margin: 0 auto;">

- One patch is a 6 dBi element with a broad beam, too little gain for a radar.
- Many identical patches etch in one step, and phase shifters steer their combined beam.
:::

Identical elements are what an array needs. The same etch step that makes
one patch makes a whole row of them, along with the printed lines that feed
them, and every element comes out flat, light, conformal, and the same as its
neighbors. Put a phase shifter behind each element and the array's beam can be
pointed electronically, with nothing on the board moving. The PHASER array we
use in Module 3 is a row of eight patches, half a wavelength apart, each behind
its own phase shifter. In Lesson 16 the patch pattern from this lesson becomes
the *element factor* that multiplies the array factor, which is why the
narrow array beam in the figure still sits inside the broad single-patch beam.
::::

::::{frame} The Slot Antenna
:::{present}
<img src="../../viz/img/L13-slot-field.svg"
     alt="A dipole beside its complement, a slot in a conducting sheet: the dipole's current runs along the wire, largest at the feed and zero at the open ends; the slot's field runs across the gap, largest at the feed and zero at the shorted ends"
     style="max-width: 560px; width: 100%; display: block; margin: 0 auto;">
:::
:::{present}
$$Z_{\text{slot}}\ Z_{\text{dipole}} = \frac{\eta_0^{2}}{4}$$

- A slot is a half-wave slit in a metal sheet, fed at the middle.
- It is the **complement** of a dipole: metal where the dipole is air.
- Its shorted ends force the field to zero; it peaks at the feed.
:::

A slot is the patch's idea turned around. The two edges of the slit are two
conductors facing each other across a narrow gap, so the slit is a short
transmission line, and the metal at each end of the slit shorts it. A wave
launched at the feed reflects from both shorted ends, and when the slit is
half a wavelength long the reflections reinforce and the slot resonates. A
short forces the voltage to zero, so the field across the gap is zero at the
two ends and largest at the center, where the feed is. That is the mirror of
the dipole, whose open ends force the *current* to zero.

It also explains the slot's high input impedance. The feed sits where the
voltage across the gap is largest and the current is smallest, and the ratio
of the two is large: a few hundred ohms. Babinet's principle puts a number on
it.

**Babinet's principle** relates complementary structures, and that one
relation carries the dipole results of Lesson 7 over to the slot. Three
consequences matter, and students most often get the third one backwards. The
slot is also flush: nothing protrudes, so it can sit on a supersonic airframe.
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

::::{frame} What 487 Ω Means
:::{present}
<img src="../../viz/img/L13-slot-feed.svg"
     alt="Half of a resonant slot, from its center to its shorted end, above a plot of input resistance against feed position: 487 ohms at the center, falling to zero at the end and crossing 50 ohms 0.20 wavelengths from the center"
     style="max-width: 560px; width: 100%; display: block; margin: 0 auto;">
:::
:::{present}
- Center-fed on $50\ \Omega$, a slot reflects 66% of its power: VSWR 9.7.
- Feeding toward a shorted end lowers the resistance: $50\ \Omega$ is $0.20\lambda$ from center.
- A waveguide slot needs no match: its offset sets its power.
:::

A center-fed resonant slot presents about $487\ \Omega$, and on a
$50\ \Omega$ line that is a reflection coefficient of

$$\Gamma = \frac{487 - 50}{487 + 50} = 0.81$$

so 66% of the power reflects and the VSWR is 9.7. This is the short dipole's
problem from Lesson 7 in the other direction: there the resistance was far too
low, here it is far too high, and either way the slot must be matched before
it is useful on coax.

The usual match is the one the patch uses: move the feed. The field across the
gap is largest at the center and falls to zero at the shorted ends, and the
input resistance falls with the square of that field,

$$R_{\text{in}}(x) = R_{\text{center}}\cos^2\left(\frac{2\pi x}{\lambda}\right)$$

where $x$ is the distance of the feed from the center. The resistance crosses
$50\ \Omega$ at $x = 0.20\lambda$, about $0.05\lambda$ from the shorted end.
A quarter-wave transformer or a lumped matching network at the center feed
works too.

Two consequences follow for real installations. A cavity-backed slot radiates
from one side only, so for the same gap voltage it radiates about half the
power, and its resistance roughly doubles, toward $1\ \text{k}\Omega$ in the
ideal case, which makes the match more important, not less. And a high
resistance means a high voltage across the gap for a given power,

$$V = \sqrt{2 P R}$$

so $100\ \text{W}$ into $487\ \Omega$ puts about $310\ \text{V}$ peak across
the slot, against $70\ \text{V}$ on a $50\ \Omega$ line. At altitude, where
air breaks down at lower voltage, that sets a power limit on airborne slots.

In a waveguide slot array none of this is a problem. Each slot is fed by the
guide's own fields rather than by a coax, and its offset from the centerline
sets how much of the guided power it takes, so there is nothing to match slot
by slot.
::::

::::{frame} Slots in Service
:::{present}
<img src="../../viz/img/L13-slot-service.svg"
     alt="Left: a cavity-backed slot in an aircraft skin, side view, radiating outward only. Right: a waveguide slot array, top view of the broad wall, with slots alternating sides of the centerline and offset more in the middle"
     style="max-width: 720px; width: 100%; display: block; margin: 0 auto;">

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
<img src="../../viz/img/L13-horn-flare.svg"
     alt="Left: an open-ended waveguide, where the incoming wave mostly reflects and only a little leaks out. Right: a horn, where the flare lets the wave expand gradually and flow out through a large opening"
     style="max-width: 720px; width: 100%; display: block; margin: 0 auto;">

- An open-ended waveguide is a fraction of a wavelength across and badly mismatched to free space.
- Flaring the walls expands the mode and makes the impedance transition gradual.
- The result is a large, well-illuminated **aperture**.
:::

A waveguide carries a single mode efficiently but radiates it poorly, because
most of the power reflects at an open end. By the equivalence principle of
Lesson 6 the flared opening is itself the source: we replace it with its
equivalent surface currents and integrate.

This is the traveling-wave antenna of the lesson. Nothing in a horn sends the
wave back: the flare widens slowly enough that the wave never meets an abrupt
change, so it flows out through the mouth instead of reflecting. With no
standing wave there is no sharp resonance, which is why a standard-gain horn
covers an octave while a patch covers a few percent.
::::

::::{frame} Gain Is Area in Square Wavelengths
:::{present}
<img src="../../viz/img/L13-horn-squares.svg"
     alt="The same 20 by 15 centimeter aperture tiled in square wavelengths: about 33 at 10 GHz and about 133 at 20 GHz"
     style="max-width: 560px; width: 100%; display: block; margin: 0 auto;">
:::
:::{present}
$$G = \eta_{\text{ap}}\ \frac{4\pi A}{\lambda^{2}}$$

- This is $A_e = G\lambda^2/4\pi$ from Lesson 2, read right to left.
- Doubling the frequency on a fixed horn raises the gain by **6 dB**.
- Horns run $\eta_{\text{ap}} \approx 0.5$; good reflectors reach 0.55 to 0.7.
:::

$A$ is the physical aperture area and $\eta_{\text{ap}}$ is the fraction of it
that contributes to the gain. The next two frames show that the horn's
geometry sets the 0.5; it is not a fudge factor.

The figure makes the formula concrete. Tile the aperture in squares one
wavelength on a side: the gain is proportional to how many squares fit. The
X-band horn of the worked example below holds about 33 of them at
$10\ \text{GHz}$. At $20\ \text{GHz}$ the wavelength halves, so four times
as many squares fit in the same opening, and the gain rises by a factor of
four, or 6 dB.
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
<img src="../../viz/img/L13-horn-phase.svg"
     alt="Side view of a horn: the spherical front from the apex reaches the flat aperture first at the center and later at the edges, so the phase lag across the aperture is a parabola"
     style="max-width: 560px; width: 100%; display: block; margin: 0 auto;">
:::
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
<img src="../../viz/img/L13-horn-three.svg"
     alt="Three horns with the same flare length and mouths too narrow, optimum, and too wide, whose edges lag by a sixteenth, a quarter, and three quarters of a wavelength. Under each, the strips of the mouth add as arrows head to tail: few arrows in a line, more arrows curving a little, and a chain that curls back. The optimum has the highest gain; the narrow mouth is 2.1 dB lower and the wide one 5.7 dB lower"
     style="max-width: 760px; width: 100%; display: block; margin: 0 auto;">

- Same flare length, wider mouth: more area, more edge lag.
- Past $\lambda/4$ of edge lag, the edge strips cancel the center.
:::

The **flare length** is the distance along the axis from the apex to the
mouth. Hold it fixed and widen the mouth, and two things happen at once. The
aperture grows, which raises the gain. But the edges of the mouth move farther
from the apex than its center is, so the wave reaches them later, and that lag
grows with the square of the width.

The arrows show why the lag matters. Split the mouth into narrow strips; each
strip contributes to the field straight ahead, and its contribution is turned
by its lag. Adding the contributions head to tail gives the total. A narrow
mouth has few strips, all nearly in step: a short, straight chain. The optimum
mouth has more strips, and the outer ones turn by up to a quarter wavelength,
so the chain bends but still gains length. Past that, the outer strips turn so
far that they point backward, and adding them makes the total *shorter*: the
extra area costs gain instead of adding it. The optimum horn is the widest
mouth that still helps, at a given length. A longer horn flattens the
wavefront, lowers the lag at every width, and moves the optimum to a wider
mouth and a higher gain; the price is length.

At the optimum, $\eta_{\text{ap}} \approx 0.5$: the design gives up about half
the aperture to keep the horn short enough to be practical.

<img src="../../viz/img/L13-horn-optimum.svg"
     alt="Relative gain of a horn of fixed length against aperture width: without phase error it keeps rising; with it, it peaks where the edge lags a quarter wavelength in the E-plane and three eighths of a wavelength in the H-plane"
     style="max-width: 560px; width: 100%; display: block; margin: 1em auto;">

The plot is the same effect computed continuously, for a horn with a flare
length of ten wavelengths, widening the mouth in one plane at a time. The
E-plane field is uniform across the aperture, and its gain peaks when the edge
lags the center by a quarter wavelength. The H-plane field follows the
waveguide's cosine, which is weak at the edges, so the edges matter less and
the peak comes later, at three eighths of a wavelength. Past the peak the
curve ripples as successive bands of the mouth alternately add and cancel. At
each peak the phase error costs about 22% of the gain in that plane, and the
cosine taper costs another 19%; together,
$0.78 \times 0.78 \times 0.81 \approx 0.5$, which is where the horn's aperture
efficiency comes from.
::::

::::{frame} The Standard-Gain Horn
:::{present}
<img src="../../viz/img/L13-horn-comparison.svg"
     alt="The gain-comparison measurement: the standard-gain horn, known to be 15.0 dBi, reads minus 40.0 dBm at the receive spot; the antenna under test, in the same spot, reads minus 52.9 dBm, so it is 12.9 dB lower: 2.1 dBi"
     style="max-width: 680px; width: 100%; display: block; margin: 0 auto;">

- It is a horn built to the optimum design, with gain measured at the factory and tabulated across its band.
- Its value is not performance but a **known** gain.
:::

We used one in Lesson 11 as the reference whose $15.0\ \text{dBi}$ we
subtracted to find the gain of our own antenna. Its calibration was the only
absolute gain in that measurement, and it is accurate to a few tenths of a dB
because a horn at the optimum design is the one aperture antenna whose
efficiency is predictable enough to certify.

The figure is the gain-comparison method. With the transmitter fixed, the
horn and then the antenna under test occupy the same receive spot. Everything
else in the link, the power, the range, the cable, is the same for both, so
the difference in received power in dB is the difference in gain. A dipole
that reads $12.9\ \text{dB}$ below a $15.0\ \text{dBi}$ horn is
$2.1\ \text{dBi}$.
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
| feed position | $R_{\text{in}}$ falls from $R_{\text{edge}}$ at the edge to 0 at the center | $50\ \Omega$ about a third of the way in |
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
