---
frame_view: true
---

# L9 - Measurement Theory

::::{frame}
:class: title-frame

<div class="course-mark">ECE 444 · Fall 2026</div>

<h1 class="frame-title">Measurement Theory</h1>

<div class="title-rule"></div>

A range is a plane-wave simulator, and a VNA measures one number.

Lesson 9 · Antennas, Phased Arrays, and Radar Systems · Dr. Neil Rogers
::::

::::{frame} Slides
:class: read-only

:::{admonition} Slides
:class: slides
<a href="../../slides/L09-pattern-measurement-theory.html" target="_blank" rel="noopener">html slides</a>
<a href="../../slides/L09-pattern-measurement-theory.html?print-pdf" target="_blank" rel="noopener">pdf slides</a>
<a href="../../slides/L09-pattern-measurement-theory.md" target="_blank" rel="noopener">raw markdown slides</a>
:::
::::

::::{frame} Learning Objectives

<ol class="lo-list lo-sublist" style="--module: '2'; --lo: '5'">
  <li>I can state what a valid pattern measurement requires — plane-wave illumination across the antenna under test — and turn that requirement into a minimum range length.</li>
  <li>I can describe the far-field range types — outdoor, anechoic chamber, and compact range — and explain what absorber reflectivity and quiet-zone specifications actually control.</li>
  <li>I can explain how near-field scanning plus a transform substitutes for an impossibly long range, and why that transform is the same Fourier relationship that produced the pattern in the first place.</li>
</ol>

:::{depth}
Lessons 7 and 8 gave you an antenna and a model of it. Every pattern in this
course so far came out of an integral; none of them came off an instrument.
This lesson is the theory that the next two lab periods stand on, and it runs
the whole problem backwards: instead of computing a far field, you have to
*build* one, and every rule that follows is a tolerance on how well you built
it.
:::
::::

::::{frame} Learning Objectives, continued

<ol class="lo-list lo-sublist" start="4" style="--module: '2'; --lo: '5'">
  <li>I can measure gain by the comparison method against a standard gain horn, and state the conditions under which the comparison is valid.</li>
  <li>I can explain what a vector network analyzer measures — the ratio of the returning wave to the outgoing wave — and translate that ratio into reflection coefficient, impedance, return loss, and VSWR.</li>
  <li>I can explain what a short-open-load calibration removes, why the reference plane decides what the numbers mean, and what a one-port measurement can never tell me.</li>
</ol>

:::{depth}
Two of those objectives belong to the radiated side of the antenna and two to
its terminals, and the lesson treats them as one subject on purpose. They are
the same question asked at two ports: how much of what an instrument reports
is the antenna, and how much is the setup around it. You will answer the
terminal half on a network analyzer in Lesson 10 and the radiated half on the
range in Lesson 11.
:::
::::

::::{frame} The Measurement Problem, Inverted
:::{present}
- A pattern is **defined** by plane-wave illumination.
- Nobody sells plane waves. A real source radiates a **spherical** one.
:::
:::{present}
:class: callout
A range is a **plane-wave simulator**. Every specification on it is a
tolerance on the flatness of that fake wave.
:::

Point a plane wave at the antenna from direction $(\theta,\phi)$, record what
comes out of the terminals, and repeat for every direction. Reciprocity says
the receive pattern equals the transmit pattern, so you may run the
measurement in whichever direction is convenient — and everyone runs it in
receive, because it is easier to move a receiver than a transmitter. That is
also why the antenna under test is the end that rotates in Lesson 11: you
would rather not run transmit power through a rotary joint.

The catch is the wave itself. What you can buy is a source antenna at a
finite distance, and a finite distance means curvature.
::::

::::{frame} Two Tolerances, Not One
:::{present}
- **Amplitude taper** comes from the source antenna's pattern.
- **Phase curvature** comes from geometry, and sets the range length.
:::
:::{present}
:class: callout
A range source is a **modest-gain** horn on purpose: its beamwidth must be
three to four times the angle the AUT subtends.
:::

A plane wave is flat in amplitude and flat in phase across the aperture, and a
real range violates both. Keeping the two apart matters because the fixes are
unrelated: amplitude taper is cured by choosing a different source antenna,
and phase curvature only by moving the source farther away or abandoning the
far-field range altogether.

The usual amplitude specification is under $0.25\ \text{dB}$ of taper edge to
edge. Seen from the source, the AUT subtends roughly $D/r$. If the source pattern
rolls off across that angle, the AUT is illuminated more strongly in the
middle than at the edges, and an unintended amplitude taper is an amplitude
taper all the same. Lesson 24 shows exactly what one does to a pattern: it
broadens the main beam and lowers the sidelobes. Measure through a tapered
illumination and you report an antenna better behaved than the one on the
positioner.
::::

::::{frame} Where 2D²/λ Comes From
:::{present}
$$\begin{aligned}
\Delta \ell &\approx \frac{(D/2)^2}{2r} = \frac{D^2}{8r} \\
\Delta\phi_{\max} &= k\ \Delta \ell = \frac{\pi D^2}{4 \lambda r} \ \le\ \frac{\pi}{8} \\
r &\ge \frac{2D^2}{\lambda}
\end{aligned}$$
:::
:::{present}
- The $\pi/8$ is a **decision**, not a derivation.
- A $0.5\ \text{m}$ dish at $10\ \text{GHz}$ needs a 55-foot room.
- A $3\ \text{m}$ terminal at $30\ \text{GHz}$ needs $1800\ \text{m}$.
:::

Take a source a distance $r$ away on boresight. The path to a point $x$ off
the aperture center is $\sqrt{r^2 + x^2} \approx r + x^2/2r$, so the extra path
at the edge, where $x = D/2$, is $\Delta\ell$ above. Multiply by
$k = 2\pi/\lambda$ to turn path into phase, then allow the edge to lag the
center by at most an eighth of a wavelength. The criterion you have quoted
since Lesson 5 is $22.5^\circ$ of edge phase error, written as a distance, and
every other far-field number in this course descends from that one tolerance.

Nobody builds a 1.8 km anechoic chamber, and that is the reason compact ranges
and near-field scanners exist. The first number is not exotic either:
seventeen meters is an ordinary requirement for an ordinary antenna, and it is
already a large and expensive room.

:::{depth}
The arithmetic, in full. For the reflector, $\lambda = c/f = 0.03\ \text{m}$
and $D/\lambda = 16.7$, so

$$r \ge \frac{2D^2}{\lambda} = \frac{2(0.5)^2}{0.03} = 16.7\ \text{m}.$$

For the satellite terminal at $30\ \text{GHz}$, $\lambda = 0.01\ \text{m}$ and

$$r \ge \frac{2(3)^2}{0.01} = 1800\ \text{m}.$$
:::

:::{depth}
The $2D^2/\lambda$ criterion assumes $D$ is comfortably larger than $\lambda$.
For a small antenna — a dipole, a patch — the far field is set instead by the
$r \gg \lambda$ condition from Lesson 5, usually taken as $r \ge 10\lambda$.
Use whichever distance is larger. Lesson 11's bench range is exactly this
case, and there the binding criterion turns out to be neither of them.
:::
::::

::::{frame} A Short Range Is a Defocused Lens
:class: read-only

Suppose you build the range too short anyway. The quadratic phase error
$\Delta\phi(x) = \pi x^2 / \lambda r$ rides on the aperture illumination, and
the measured pattern is the same radiation integral from Lesson 6 with that
extra phase inside it:

$$F_\text{meas}(\theta) \propto \int_{-D/2}^{D/2} E(x)\ e^{-j \pi x^2 / \lambda r}\ e^{+jkx\sin\theta}\ dx$$

A quadratic phase across an aperture is a **defocus**, exactly like a lens at
the wrong distance. What matters is not that the pattern degrades but *which*
features degrade, and in what order.
::::

::::{frame} The Nulls Fill First
:class: viz-frame

:::{present}
<iframe src="../../viz/range-phase-error.html"
        width="100%" height="507"
        style="border: 1px solid #cddce9; border-radius: 6px;"
        loading="lazy"
        title="Quadratic phase error from a finite range length, and the pattern it produces compared with the true far-field pattern">
</iframe>
:::

:::{depth}
Slide the range in and watch. The left panel shows the phase error across the
aperture against the $22.5^\circ$ tolerance line; the right panel overlays the
true far-field pattern (dashed) on what the range actually measures (solid).
Notice that the nulls fill and the first sidelobe merges into a shoulder long
before the main beam does anything at all — and that everything snaps clean
right around $r = 2D^2/\lambda$, where the edge error reads exactly
$22.5^\circ$.
:::
::::

::::{frame} What 2D²/λ Actually Delivers
:::{present}
| $r \div 2D^2/\lambda$ | Edge error | Null fills to | HPBW error |
| :-- | :-- | :-- | :-- |
| 2 | $11.3^\circ$ | $-28$ dB | none |
| 1 | $22.5^\circ$ | $-22$ dB | $+0.3\%$ |
| 1/2 | $45^\circ$ | $-16$ dB | $+1.3\%$ |
| 1/4 | $90^\circ$ | $-9.5$ dB | $+6\%$ |
:::
:::{present}
:class: callout
This is a **main-beam and gain** criterion, not a sidelobe one.
:::

Read the top two rows carefully, because they state what the rule delivers.
At $r = 2D^2/\lambda$ you have not measured the true pattern. You have
measured one whose first sidelobe reads $-12.9$ dB instead of the textbook
$-13.3$ dB and whose nulls are twenty decibels shallow. What you *have*
measured correctly is the main beam, the beamwidth, and the gain. If you need
a $-40$ dB sidelobe or a null depth you can defend, go to $5D^2/\lambda$ or
further, or stop using a far-field range altogether.

This failure mode is dangerous because it is quiet. A pattern measured at a
quarter of the far-field distance still looks like a pattern: about the right
main-beam width, sidelobes present, smooth. It is wrong only in the places you
care about most.
::::

::::{frame} Three Ways to Make the Plane Wave
:::{present}
| Range type | Makes the wave by | Limited by |
| :-- | :-- | :-- |
| Outdoor | Brute distance | Weather, ground bounce |
| Anechoic | Distance plus absorber | Still needs $2D^2/\lambda$ |
| Compact | A reflector collimates | Edge diffraction |
| Near-field | Transform, not distance | Phase, probe, time |
:::

The first three are **far-field ranges**: they physically deliver an
approximate plane wave to the AUT. The fourth changes the question entirely.

:::{depth}
Distance costs nothing outdoors, so the oldest ranges are two towers, or a
tower and a hillside. Two variants matter. An **elevated range** puts both
antennas high enough, and uses directive-enough source antennas, that the
ground bounce misses the AUT. A **ground-reflection range** does the opposite:
it chooses the geometry so the direct and ground-reflected rays arrive *in
phase* at the AUT, deliberately using the ground as part of the illumination.
Both approaches work. Neither offers security, weather protection, or freedom
from interference, which is why most modern measurement happens indoors.
:::
::::

::::{frame} What the Absorber Does
:::{present}
- Pyramids give a gradual transition into a lossy medium.
- Good absorber reaches $-40$ to $-50$ dB at **normal** incidence.
- It degrades at grazing incidence — the side walls.
:::
:::{present}
:class: callout
A chamber is never "no reflections". It is **reflections below a stated
level**.
:::

Absorber is carbon-loaded foam, cut into pyramids, and it is specified by
reflectivity in dB. Performance scales with pyramid height *in wavelengths*,
so low-frequency absorber gets enormous: a chamber rated to 200 MHz has
meter-long spikes on the walls. Which reflectivity level you need is set by
the lowest signal you intend to believe, not by the main beam.
::::

::::{frame} What −40 dB of Stray Field Buys You
:::{present}
| Measuring | Error a $-40$ dB stray adds |
| :-- | :-- |
| Main beam peak | $\pm 0.09$ dB |
| A $-20$ dB sidelobe | $+0.8 / -0.9$ dB |
| A $-30$ dB sidelobe | $+2.4 / -3.3$ dB |
:::
:::{present}
:class: callout
A chamber that meets spec still puts **three decibels** on a sidelobe.
:::

As the positioner turns, the stray reflection adds in and out of phase with
the wanted signal, so the ripple it produces depends entirely on how strong
that wanted signal is. Near the peak it is invisible. Thirty decibels down, it
is most of your answer. Lesson 11 asks you to state a dynamic range next to
every number you extract for exactly this reason.
::::

::::{frame} The Quiet Zone
:::{present}
- The deliverable of a chamber is the **quiet zone**, not the room.
- Quoted as a size, a level, and a band: "1.2 m at $-45$ dB, 2 to 18 GHz".
- **The AUT must fit inside it.**
:::

The quiet zone is a specified volume, usually a sphere or cylinder centered on
the positioner, inside which the stray field is guaranteed below the
reflectivity spec. It is measured rather than assumed, typically by dragging a
probe through the volume and recording the ripple.

An antenna that overhangs the quiet zone is being measured in a room rather
than in a chamber, and no amount of care with the rest of the setup recovers
that. It is the first thing to check when a chamber measurement disagrees with
a simulation for no reason you can name.
::::

::::{frame} Compact Ranges
:::{present}
- A feed at a paraboloid's focus: every path is one length, so the wave leaves flat.
- Optics instead of distance.
:::
:::{present}
- The quiet zone is **50 to 60%** of the reflector.
- Hard rims diffract, so edges are **serrated**.
:::

This is Lesson 14's reflector geometry doing a different job. There the
collimated wave was aimed at a satellite; here it only has to reach the far
side of the chamber. Two costs come with it. A meter of quiet zone needs close
to a two-meter reflector, built to a fraction of a wavelength — so the
reflector is a precision instrument in its own right. And a hard edge acts as
a line source sitting right inside your test volume, which is why the rims are
shaped to scatter the edge contribution away from it.
::::

::::{frame} Near-Field Scanning
:::{present}
- The 1.8 km range is impossible, so change the measurement.
- Sample the **complex** field a few wavelengths out, then transform.
:::
:::{present}
:class: callout
Lesson 6 proved this. The far field is the **Fourier transform** of the
source, and transforms are invertible.
:::

Put a small probe a few wavelengths in front of the antenna and record
amplitude and phase at a grid of points on a surface. Because the field
sampled on a surface enclosing the antenna determines the field everywhere
outside it, that grid is enough.

Near-field to far-field transformation is not a new physical principle. It is
Lesson 6's relationship run in the other direction, and three practical
consequences follow immediately from that fact alone.
::::

::::{frame} Three Rules That Follow
:::{present}
- **Phase is not optional.** Magnitude alone does not determine the transform.
- **Sample at $\lambda/2$ or finer**, or the transform aliases.
- **Scan far enough out**, or the pattern is truncated.
:::

Phase is why a near-field range is built around a vector network analyzer and
phase-stable cables, and why the probe position has to be known to a small
fraction of a wavelength. Undersampling produces lobes in the far-field
pattern that the antenna does not have.

The middle rule is the same Nyquist argument as Lesson 6's spatial spectrum,
and the third is why a planar scan says nothing whatever about back lobes.

:::{depth}
One more step exists in a real near-field system: **probe compensation**. The
probe has its own pattern, and what it records is the true field weighted by
that pattern. Dividing it back out is standard, well understood, and firmly
beyond this course. Know that it happens; do not derive it.
:::
::::

::::{frame} The Three Scan Surfaces
:class: read-only

| Scan surface | Best suited to | Pattern coverage |
| :-- | :-- | :-- |
| Planar | High-gain, directive antennas | A forward cone, roughly $\pm 60^\circ$ |
| Cylindrical | Fan beams, sector antennas | Full azimuth, limited elevation |
| Spherical | Low-gain antennas, anything | The complete sphere |

The choice is a trade of time against coverage. A planar scan of a large
reflector is a few hours; the spherical scan that would resolve its back lobes
is a few days, and for a high-gain antenna those back lobes are usually not
the number anyone is paying for.
::::

::::{frame} Gain by Comparison
:::{present}
$$G_\text{AUT} = G_\text{SGH} + \left( P_\text{AUT} - P_\text{SGH} \right)$$

- Gain is absolute, so it needs a reference.
- Record the AUT, swap in a **standard gain horn**, subtract.
:::
:::{present}
:class: callout
Everything you do not know cancels. The horn's calibration is the only
absolute number in the room.
:::

Write Friis for each measurement and the reason is immediate: every term but
the two gains appears identically in both, so the difference of the two
received powers is the difference of the two gains. This is the method you
will use in Lesson 11 and again for the midterm.

:::{depth}
Worked example. At $9.4\ \text{GHz}$, a standard gain horn with a calibrated
gain of $16.8\ \text{dBi}$ receives $-38.6\ \text{dBm}$. Replacing it with the
AUT, everything else untouched, gives $-33.1\ \text{dBm}$.

$$\begin{aligned}
\Delta P &= -33.1 - (-38.6) = +5.5\ \text{dB} \\
G_\text{AUT} &= 16.8 + 5.5 = 22.3\ \text{dBi}
\end{aligned}$$

The AUT collects 5.5 dB more power than the standard, so it has 5.5 dB more
gain. That is the entire method.
:::

:::{depth}
The conditions on validity are worth naming, because violating one silently
biases the answer: same position, same polarization, same frequency, and both
antennas either well matched or their mismatch losses corrected. If the AUT
has a poor match, the power you measure is low for a reason that has nothing
to do with gain — which is precisely why Lesson 10 comes before Lesson 11.
:::
::::

::::{frame} When No Standard Exists
:class: read-only

$$\left( P_r - P_t \right)_{\text{dB}} = G_t + G_r + 20\log_{10}\!\left( \frac{\lambda}{4\pi R} \right)$$

Working from Friis with no calibrated antenna at all, **two identical
antennas** give $G_t = G_r = G$, so one measurement is enough. If the antennas
are not identical, use **three** and measure all three pairs. Let $M_{AB}$ be
the measured pair sum with the path term already removed, so
$M_{AB} = G_A + G_B$, and likewise for the other two. Three equations, three
unknowns:

$$G_A = \tfrac{1}{2}\left( M_{AB} + M_{AC} - M_{BC} \right)$$

The standard gain horn itself had to be calibrated somehow, and this is how.
No calibrated antenna appears anywhere in the three-antenna procedure, which
is what makes it the primary standard rather than a convenience.

:::{depth}
Worked example, two identical horns facing each other at $R = 20\ \text{m}$,
at $6\ \text{GHz}$ so $\lambda = 0.05\ \text{m}$. With $P_t = 0\ \text{dBm}$
you measure $P_r = -40.0\ \text{dBm}$:

$$\begin{aligned}
20\log_{10}\!\left( \frac{\lambda}{4\pi R} \right) &= 20\log_{10}(1.989\times10^{-4}) = -74.0\ \text{dB} \\
2G &= (P_r - P_t) - (-74.0) = -40.0 + 74.0 = 34.0\ \text{dB} \\
G &= 17.0\ \text{dBi}
\end{aligned}$$

Check the range as well: for a horn of this gain, $D$ is roughly
$0.2\ \text{m}$, so $2D^2/\lambda = 1.6\ \text{m}$. Twenty meters is
comfortably far field. In $M_{AB} = G_A + G_B$ the path term has already been
removed, which is the only bookkeeping the three-antenna version adds.
:::
::::

::::{frame} Cuts, Planes, and Polarization
:::{present}
- A **great-circle cut** holds $\phi$ fixed and sweeps $\theta$.
- The **E-plane** holds the aperture field; the **H-plane** is perpendicular.
:::
:::{present}
- Run every cut twice: aligned is **co-pol**, turned $90^\circ$ is **cross-pol**.
- Healthy linear antennas sit 20 to 30 dB down.
:::

A complete pattern is a function on a sphere, and measuring the whole sphere
finely is expensive, so you take slices. A **conical cut** does the opposite
of a great-circle one — holds $\theta$ fixed and sweeps $\phi$, tracing a ring
at a constant angle off boresight — and is used for tracking antennas and for
checking rotational symmetry. Two principal cuts fully describe a well-behaved
pencil beam and say nothing at all about the diagonal planes, where the
sidelobes of a rectangular aperture frequently sit.

Cross-pol is the power the antenna radiates into the polarization it is
supposed to reject, and it is worse off-axis than on, which is why it is
quoted as a pattern rather than as a single number.

:::{depth}
For a circularly polarized antenna there is a faster method. Spin the linear
source continuously while sweeping the cut — **spinning linear** — and the
recorded pattern comes back as a band rather than a line. The peak-to-trough
width of that band, in dB, *is* the axial ratio from Lesson 3, and a perfectly
circular antenna gives a band of zero width.
:::
::::

::::{frame} The Other Port: What a VNA Measures
:::{present}
<img src="../../slides/fig/L10-vna-block.svg"
     alt="Block diagram of a one-port VNA: source, two directional couplers feeding a reference and a test receiver, and a ratio block producing S11."
     style="max-width: 620px; width: 100%; display: block; margin: 0 auto;">
:::
:::{present}
$$S_{11} = \frac{b_1}{a_1} = \Gamma = \frac{Z_L - Z_0}{Z_L + Z_0}$$

- Couplers sample the wave going out and the one coming back.
- Both receivers record magnitude *and* phase.
:::

Everything so far measured the antenna from a distance; the rest of this
lesson stands at its terminals. It is one port, one cable, and one complex
number per frequency, and that number carries everything you have been
predicting on paper since Lesson 4. Lesson 7 told you a half-wave dipole
should sit near $73 + j42.5\ \Omega$ and resonate slightly short of
$\lambda/2$; Lesson 10 is where that prediction meets a real piece of wire.

Because both samples come from the same source, anything the source does
wrong — drift, ripple, amplifier gain variation — divides out of the ratio.
That is why a pocket NanoVNA and a bench instrument costing a thousand times
more agree on a well-calibrated one-port measurement to within a fraction of a
dB. For a one-port device, and an antenna is a one-port device, that ratio
*is* the reflection coefficient at the reference plane.
::::

::::{frame} Four Names for One Number
:::{present}
| Quantity | From $\Gamma$ | At $\vert\Gamma\vert = 0.316$ |
| :-- | :-- | :-- |
| $\vert S_{11}\vert$ dB | $20\log_{10}\vert\Gamma\vert$ | $-10.0$ dB |
| Return loss | $-20\log_{10}\vert\Gamma\vert$ | $10.0$ dB |
| VSWR | $(1 + \vert\Gamma\vert)/(1 - \vert\Gamma\vert)$ | $1.92$ |
| Power reflected | $\vert\Gamma\vert^2$ | $10\%$ |
:::
:::{present}
:class: callout
Keep the last row. −10 dB means **90% of the power gets in**.
:::

All four appear on instrument menus, and all four are re-dresses of the single
complex number the analyzer measured. Nothing else is being measured. The
−10 dB convention from Lesson 4 is not arbitrary: it is the band over which at
least 90% of the power you deliver actually reaches the antenna.
::::

::::{frame} Impedance from the Ratio
:::{present}
$$Z_L = Z_0\ \frac{1 + \Gamma}{1 - \Gamma}, \qquad Z_0 = 50\ \Omega$$

- Invert the bilinear relation and you have what the antenna presents.
- The **sign of the reactance** is the actionable part: negative is capacitive, so the element is electrically short.
:::

Read the physics, not the arithmetic. A marker reading
$S_{11} = 0.28\ \angle-140^\circ$ works out to $30.6 - j11.9\ \Omega$: it
passes the −10 dB spec, but the resistance is low against the $\sim 70\ \Omega$
a resonant dipole should show, and the negative reactance says resonance sits
above this frequency. The antenna wants to be trimmed *longer*. That single
inference is most of what Lesson 10 asks you to do at the bench.

:::{depth}
The arithmetic in full. Rectangular form first:

$$\Gamma = 0.28\left[\cos(-140^\circ) + j\sin(-140^\circ)\right] = -0.215 - j0.180$$

Magnitude quantities come straight off $\vert\Gamma\vert = 0.28$:

$$\vert S_{11}\vert = 20\log_{10}(0.28) = -11.1\ \text{dB}, \qquad \text{VSWR} = \frac{1.28}{0.72} = 1.78$$

Then the impedance:

$$Z_L = 50\ \frac{1 + \Gamma}{1 - \Gamma} = 50\ \frac{0.785 - j0.180}{1.215 + j0.180} = 30.6 - j11.9\ \Omega$$
:::

:::{depth}
The same conversion is worth running on the textbook numbers. A perfect
half-wave dipole at $73 + j42.5\ \Omega$ gives $\vert\Gamma\vert = 0.371$, or
$-8.6$ dB, VSWR $2.18$ — it **fails** the −10 dB test. Shorten it to
resonance, where it settles near $70\ \Omega$ real, and you get $-15.6$ dB and
VSWR $1.40$. That $42.5\ \Omega$ of reactance is the entire difference between
a marginal antenna and a good one, and it is why nobody builds a dipole
exactly $\lambda/2$ long.
:::
::::

::::{frame} Three Error Terms, Three Standards
:::{present}
- Three unknowns — **directivity**, **source match**, **tracking** — need three known standards.
:::
:::{present}
| Standard | $\Gamma$ | Pins down |
| :-- | :-- | :-- |
| Short | $-1$ | one extreme |
| Open | $+1$ | the other |
| Load | $0$ | the floor |
:::

Three error terms dominate a one-port measurement. **Directivity** is the
coupler leaking a little of the outgoing wave into the receiver that is
supposed to see only the returning one, so the VNA reads a reflection even
from a perfect load. **Source match** is the test port not being exactly
$50\ \Omega$, so energy the antenna sends back is partly re-reflected at the
port and sent to the antenna again. **Tracking** is the reference path and the
test path having different gain and different phase, both varying with
frequency.

Three unknowns need three knowns, and that is all a **short-open-load**
calibration is. You measure all three, the instrument solves three equations
at every point in the sweep, and from then on it subtracts its own error
before showing you anything. Two-port work adds a **through** standard — hence
SOLT — but a one-port antenna measurement needs only the three.
::::

::::{frame} The Reference Plane
:::{present}
<img src="../../slides/fig/L10-cal-planes.svg"
     alt="Reference planes: A at the VNA port, B at the end of the test cable where SOL is performed, C at the antenna terminals. The pigtail between B and C rotates the measured phase."
     style="max-width: 560px; width: 100%; display: block; margin: 0 auto;">
:::
:::{present}
:class: callout
Calibration teaches the instrument **where zero is**, and zero is wherever you
attached the standards.
:::

Calibration does not make the instrument more accurate. The plane where you
attached the standards becomes the plane where $S_{11} = 0$ means "perfectly
matched", and everything on the far side of it is part of your device under
test whether you meant it to be or not.
::::

::::{frame} The Pigtail Problem
:::{present}
$$\Delta\phi = 2\beta\ell = 2\ (360^\circ)\ \frac{\ell}{\lambda_g}$$

- 10 cm of RG-58 at 915 MHz rotates the trace $333^\circ$.
- Loss is negligible, so the dB plot still looks right.
:::
:::{present}
- **Fix 1**: calibrate at the antenna connector.
- **Fix 2**: use port extension, which is phase-only.
:::

With $\lambda_g = c\ v_f / f$, that pigtail is $0.46\lambda_g$ long — nearly a
full rotation of the Smith chart, and the impedance you read off is not the
antenna's in any useful sense. Port extension rotates the reference plane
forward by a known length but cannot undo loss, and it cannot undo a real
mismatch inside an adapter.

The wave traverses the extra length twice, out and back, which is where the
factor of two comes from. At 990 MHz that same pigtail is exactly a half
guided wavelength and the impedance repeats — the one frequency where the
un-de-embedded reading happens to be correct, and a good illustration of why
"it looked fine at one marker" is not a check.

:::{depth}
Always verify a calibration before you trust it. Reconnect the load standard
and look: $\vert S_{11}\vert$ should sit below $-30$ dB across the whole
sweep. If it does not, something moved, a connector is loose, or you swapped
cables after calibrating. Re-do it. An unverified cal is an unmeasured
antenna, and Lesson 10 makes the verification screenshot a deliverable for
exactly that reason.
:::
::::

::::{frame} Reading the Sweep
:::{present}
- A **dip** marks a resonance.
- The **depth** says how well matched it is, not how well it radiates.
- The **width** below −10 dB is the impedance bandwidth.
- Quote it in MHz *and* in percent.
:::

Fractional bandwidth is what lets you compare a 900 MHz antenna to a 2.4 GHz
one, and it is the number with a sanity range attached: a thin-wire dipole
lands between 3 and 10%. A trace bottoming out at $-19$ dB and crossing −10 dB
at 878 and 922 MHz gives $\text{BW} = 44\ \text{MHz}$ on $f_0 = 900\ \text{MHz}$,
or 4.9% — entirely believable. If you measure 1%, suspect the setup before you
suspect the antenna; a resonant length of feed cable can manufacture a narrow
dip that has nothing to do with the element.
::::

::::{frame} Four Smith-Chart Reading Skills
:::{present}
- **Crosses the real axis**: resonance. Left of center is $R < 50\ \Omega$.
- **Inside the 0.316 circle**: the −10 dB spec, drawn.
- A **loop**: two resonances, often element plus feed.
- The **whole trace rotating**: your reference plane moved.
:::

You met the Smith chart in ECE 343 as a graphical impedance calculator. Today
you only need to *read* one: it is the complex $\Gamma$ plane with a
normalized-impedance grid on top, center $50\ \Omega$, left edge a short,
right edge an open, upper half inductive and lower half capacitive. Those four
skills cover almost everything you will see this semester, and you will
rehearse them on a widget at the start of Lesson 10 before you read your own
trace.
::::

::::{frame} What One Port Cannot Tell You
:::{present}
- Solder a $50\ \Omega$ resistor across the connector: VSWR $1.00$, marker dead center.
- A **perfect** match. It radiates **nothing**.
:::
:::{present}
:class: callout
$S_{11}$ measures **mismatch only**. Efficiency needs a second, independent
measurement.
:::

This cuts both ways on the bench. A deep, wide dip is *necessary* for a good
antenna, not *sufficient*, and an antenna with a mediocre $-8$ dB match may
still be the better radiator. It is also the reason the two labs come as a
pair: Lesson 10 establishes that power went in, and only Lesson 11 establishes
that it came back out, and in which direction.
::::

::::{frame} The Environment Is Part of Your Antenna
:::{present}
| Perturbation | What you see | Why |
| :-- | :-- | :-- |
| A hand near it | $f_0$ down, dip shallower | tissue adds loss |
| Flat on the bench | $f_0$ shifts, a loop | partial ground plane |
| Near a wall | wiggles around the dip | energy returns |
:::

Lesson 5 defined the reactive near field as the region where energy is stored
rather than radiated. Anything you put in that region becomes part of the
antenna, and the analyzer will tell you so immediately. None of this is
instrument error. It is a real change in input impedance, and the same physics
reappears in Module 3 as **mutual impedance** between array elements — when
you put your hand near a dipole in Lesson 10 you are running a one-element
preview of what neighbors in an array do to each other.
::::

::::{frame} How Much of a Pattern Is Real
:::{present}
- Measured power is signal **plus** noise floor.
- **Dynamic range** = peak minus floor.
- Beamwidth is robust; **nulls measure your floor**.
:::
:::{present}
:class: callout
"At least 25 dB deep, limited by our 42 dB dynamic range" is defensible.
"25 dB deep" is not.
:::

This is the same argument as the $-40$ dB stray-field table earlier, arriving
from the other direction: there an unwanted signal set the floor, here the
receiver does. Lesson 11 asks you to measure your own floor with the source
switched off, and then to say, row by row, which of your extracted numbers
clears it and by how much.
::::

::::{frame} Summary — The Far-Field Range
:class: read-only

| Symbol / idea | What it is | The number to remember |
| :-- | :-- | :-- |
| $r \ge 2D^2/\lambda$ | Minimum far-field range length | $22.5^\circ$ of edge phase error, written as a distance |
| $\Delta\phi_{\max} = \pi D^2 / 4\lambda r$ | Quadratic phase error at the aperture edge | $\pi/8$ at the far-field distance |
| Amplitude taper | Source pattern rolling off across the AUT | Under $0.25$ dB; source beamwidth 3-4× the subtended angle |
| Absorber reflectivity | How much a wall reflects | $-40$ to $-50$ dB at normal incidence, worse at grazing |
| Quiet zone | Volume where the stray field meets spec | A size *and* a level; the AUT must fit inside |
| Compact range | Reflector collimates a spherical wave up close | Quiet zone $\approx$ 50-60% of the reflector |
| Near-field scan | Sample amplitude and phase close in, transform | Half-wavelength sampling; phase is mandatory |
::::

::::{frame} Summary — Gain and the Terminals
:class: read-only

| Symbol / idea | What it is | The number to remember |
| :-- | :-- | :-- |
| Comparison method | Gain by differencing against a standard | $G_\text{AUT} = G_\text{SGH} + (P_\text{AUT} - P_\text{SGH})$ |
| Three-antenna method | Gain with no calibrated standard | $G_A = \tfrac{1}{2}(M_{AB} + M_{AC} - M_{BC})$ |
| $S_{11} = b_1/a_1$ | One-port scattering parameter | equals $\Gamma$ at the reference plane |
| $Z_L = Z_0(1+\Gamma)/(1-\Gamma)$ | Impedance from reflection | sign of $X$ tells you short (−) or long (+) |
| $\vert S_{11}\vert \le -10$ dB | The match spec | $\vert\Gamma\vert \le 0.316$; VSWR $\le 1.92$; 90% of power in |
| Directivity, source match, tracking | The three one-port error terms | three unknowns, hence three SOL standards |
| Reference plane | Where the standards were attached | line length past it = pure rotation on the chart |
| Dynamic range | Peak level minus measured noise floor | bounds every extracted number |
::::

::::{frame} The Midterm Project
:::{present}
:class: callout
**Midterm Project — Antenna Pattern Measurement.** Introduced today, due at
Lesson 20. Measure an antenna's pattern and report gain, beamwidth, sidelobe
level, and polarization with an error budget.
:::
:::{present}
- Three error-budget lines, all named today: **range length**, **quiet zone**, **horn calibration**.
:::

"I measured it" is not an engineering result. "I measured it, and here is what
my range could and could not tell me" is, and that second sentence is what
this lesson exists to let you write.

Full requirements come in the project handout distributed in class. Start
thinking now about which antenna you want to build. Lessons 10 and 11 are the
dress rehearsal — same instruments, same extraction, same uncertainty
discussion — and Lessons 12 to 14 will put several more antenna families in
front of you, any of which is a defensible choice for the project. The
selection framework at the end of Lesson 14 is the reasoning your report will
have to show.
::::

::::{frame} Practice
:class: read-only

- <a href="../../practice/ECE444_L09_Practice_blank.pdf" target="_blank" rel="noopener">Problem set (PDF)</a>
- <a href="../../practice/ECE444_L09_Practice_SOLUTIONS.pdf" target="_blank" rel="noopener">Solutions (PDF)</a>
::::

::::{frame} Where This Is Going
:::{present}
- **Lesson 10** puts an antenna on the analyzer: calibrate, sweep, read the match.
- **Lesson 11** puts one on the positioner: cut two planes, extract gain and beamwidth.
- Both lessons are procedure. The reasons are all here.
:::

The next two periods are hands-on and deliberately thin on theory — you will
be standing at an instrument, not at the board. Everything you need to justify
what you do there has been said today, so bring this lesson with you: the
range length you check with a tape in Lesson 11 is the $2D^2/\lambda$ above,
and the reference plane you calibrate at in Lesson 10 is the one drawn on the
cal-plane figure.
::::
