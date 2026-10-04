<!-- .slide: class="title-slide" -->

<div class="title-left">

# ECE 444

Antennas, Phased Arrays, and Radar Systems

## Lesson 15 — Aperture Distributions and Efficiency

Fall 2026 · Dr. Neil Rogers

</div>

<div class="title-right">

![USAFA](./img/01-course-intro/USAFA-logo.png)

</div>

---

## From Measurement to Design

- Lesson 11 closed the measurement work: you turned an antenna and recorded a pattern.
- Module 1 gave us the radiation integral, the far-field distance, and the effective aperture $A_e$.
- Lesson 6 showed the far field is the Fourier transform of the source distribution.
- The midterm pattern-measurement project is due 2 Oct.

In Module 3 we design the pattern, and the aperture distribution is the design variable.

Note:
Module two was about characterizing an antenna somebody handed you. Module three is
about designing the pattern you want. Everything in this module comes out of one
relationship they already met in lesson six, so today is about turning that
relationship into design numbers they can use without deriving anything.

---

## Today's Plan

1. The aperture distribution, and why it alone sets the far field.
2. Derive the uniform aperture pattern, and read three numbers off it.
3. Aperture efficiency, from the illumination to the gain formula.
4. The taper trade: sidelobes against beamwidth and gain.
5. Sizing an aperture at X-band.

Note:
Point out that steps two and four give them numbers they will use in every remaining
lesson of the course, including both labs on the PHASER.

---

## The Aperture as Source

An **aperture** is the opening the wave leaves through — a horn mouth, a reflector face, a row of patches. The far field depends on the tangential field across that opening and on nothing else.

<div class="fig" data-inline-svg="./fig/L15-aperture-to-pattern.svg" style="max-width:720px; margin:0 auto;"></div>

Change the distribution and you change the pattern. Leave it alone and nothing behind the aperture matters.

Note:
Emphasize the second sentence. Students want to explain patterns by what is behind
the aperture — the waveguide, the feed, the subreflector. Those only matter through
the field they produce on the opening.

---

## The Transform Relationship

For an aperture of length $L$ on the $x$ axis, with $\theta$ measured from broadside:

$$S(\theta) = \int_{-L/2}^{L/2} E_a(x)\ e^{\ jkx\sin\theta}\ dx$$

The exponent is the extra path from the point at $x$, turned into phase.

Define the **space frequency** $u = (L/\lambda)\sin\theta$.

<div class="callout"><strong>Shape</strong> of the illumination sets the pattern in <em>u</em>. <strong>Size</strong> in wavelengths sets how many degrees correspond to each unit of <em>u</em>.</div>

Note:
Derive this at the board if there is time — it is one line from the radiation integral
of lesson six. The substitution to u is the move that makes every result reusable.
Write u on the board and leave it there for the rest of the hour.

---

## Path Difference Across the Aperture

<div class="fig" data-inline-svg="./fig/L15-path-difference.svg" style="max-width:640px; margin:0 auto;"></div>

Toward a far-field point at angle $\theta$, the rays from the center and from $x$ are parallel and differ in length by $x\sin\theta$.

Note:
This is where the exponent comes from. The far-field point is far enough away that
the two rays are parallel. Drop a perpendicular from the point at x onto the ray
from the center: the leftover piece of the center ray is x sine theta long, and
multiplying by k turns that length into the phase k x sine theta. Integrating that
phase against the aperture field is the Fourier transform on the previous slide.

---

## Angle Convention

Module 1 measured the polar angle from the wire axis. Module 3 measures $\theta$ from **broadside**.

That is what every phased-array plot and every PHASER readout uses.

So the space frequency carries $\sin\theta$ here, not $\cos\theta$.

Lesson 16 makes the substitution explicit once, and then we never revisit it.

Note:
Do not spend more than a minute here, but do say it out loud. Students who go read
Balanis will find cosine theta and think one of the two is wrong.
The symbol u also changes scale. Lesson six wrote the line source as sine u over u
with u equal to k L over two times cosine theta, so its nulls sat at u equal to pi
and its first sidelobe at 4.493. Today's u is that u divided by pi, with sine in place
of cosine, so the nulls land on the integers and the first sidelobe at 1.430.
Lesson fourteen's circular aperture keeps the pi: u equals pi D over lambda times sine theta.

---

## One Shape, Three Sizes

<div class="fig" data-inline-svg="./fig/L15-shape-vs-size.svg" style="max-width:500px; margin:0 auto;"></div>

Note:
Top panel: one sinc for every length. The aperture length only decides how far
along the u axis real angles reach, out to u equal to L over lambda: two for a
two-wavelength aperture, twenty for a twenty-wavelength one. Bottom panel: the same
three apertures against angle. The beams are 25.6, 10.2, and 2.5 degrees wide, and
every first sidelobe sits on the same minus 13.3 dB line. Shape sets the sidelobes;
size sets the angle scale.

---

## Derivation: Uniform Illumination

Let the field be constant, $E_a(x) = E_0$, across the whole opening. The integrand is then an exponential, so the integral is elementary:

$$S(\theta) = E_0\int_{-L/2}^{L/2} e^{\ jkx\sin\theta}\ dx$$

$$= E_0\ \frac{e^{\ jkL\sin\theta/2} - e^{-jkL\sin\theta/2}}{jk\sin\theta}$$

Note:
Do this one at the board. It is the only integral in the lesson and it takes thirty
seconds. Remind them the difference of two exponentials over two j is a sine.

---

## Derivation: The Sinc Pattern

Two exponentials over $2j$ make a sine, so the chain continues:

$$= E_0 L\ \frac{\sin\left(\tfrac{1}{2}kL\sin\theta\right)}{\tfrac{1}{2}kL\sin\theta}$$

With $k = 2\pi/\lambda$ the argument is exactly $\pi u$:

$$\vert F(u)\vert = \left\vert\frac{\sin \pi u}{\pi u}\right\vert \qquad u = \frac{L}{\lambda}\sin\theta$$

<div class="callout">A uniformly illuminated aperture radiates a <strong>sinc</strong> pattern in space frequency.</div>

Note:
The nulls, beamwidth, and first sidelobe all follow from this expression.
Stress that the L came out front and the shape did not depend on it. Size sets
beamwidth and gain; shape alone sets the sidelobes.

---

## Reading the Sinc: Nulls

$\sin \pi u$ vanishes at $u = \pm 1, \pm 2, \pm 3, \dots$

So the first null sits at $\sin\theta = \lambda/L$.

An aperture shorter than a wavelength has no null in real space, so it radiates broadly however we feed it.

Note:
Ask them what happens when L over lambda drops below one. The first null needs a sine
greater than one, which does not exist. That is why small antennas are always broad.

---

## Reading the Sinc: Beamwidth

Solve for the half-power point:

$$\frac{\sin \pi u}{\pi u} = \frac{1}{\sqrt{2}}$$

$$\pi u = 1.3916 \qquad u = \pm 0.4429$$

$$\theta_\text{HP} \approx 0.886\ \frac{\lambda}{L} \text{ rad} = 50.8^\circ\ \frac{\lambda}{L}$$

<div class="callout">Memorize <strong>0.886</strong>. It reappears in the array beamwidth formula in Lesson 20 and in every PHASER prediction you make.</div>

Note:
Point eight eight six is the single most reused number in the module. Have them write
it down. The array version is zero point eight eight six lambda over N d.
Where it comes from: the half-power points sit at sine theta equal to plus or minus
0.4429 lambda over L, so the exact beamwidth is two times the arcsine of 0.4429 lambda
over L. For a narrow beam the sine is the angle, which gives 0.886 lambda over L. The
approximation is within one percent for L of two wavelengths or more; lesson six's
two-wavelength source was 25.6 degrees exact against 25.4 approximate.

---

## Reading the Sinc: Sidelobes

The first sidelobe peaks near $u = 1.43$, where $\vert F\vert = 0.217$.

$$20\log_{10}(0.217) = -13.3\ \text{dB}$$

The first sidelobe level does not depend on $L$.

A longer uniform aperture narrows the beam, raises the gain, and leaves the first sidelobe $13.3$ dB down.

Note:
This is the main result of the first half. Size sets beamwidth and gain; shape sets
the sidelobes, and shape only. Say it twice.
The sidelobe peak is where the slope of the sinc is zero, which is where tangent of
pi u equals pi u. The first root past the main lobe is u equal to 1.430.

---

## The Uniform Aperture Pattern

<div class="fig" data-inline-svg="./fig/L15-uniform-pattern.svg" style="max-width:760px; margin:0 auto;"></div>

Note:
Walk the figure: main lobe, half-power width in green, first null at u equal to one,
first sidelobe at minus thirteen point three. Ask where the pattern would change if
they doubled L. Answer: only the horizontal scale.

---

## Worked Example: A 10λ Aperture

| Quantity | Work | Result |
| :-- | :-- | :-- |
| Beamwidth | $50.8^\circ / 10$ | $5.08^\circ$ |
| First nulls | $\sin\theta = 0.1$ | $\pm 5.74^\circ$ |
| First sidelobe | uniform, any $L$ | $-13.3$ dB |
| Length at $10$ GHz | $10 \times 0.03\ \text{m}$ | $0.30$ m |
| Same $0.30$ m at $3$ GHz | now only $3\lambda$ | $16.9^\circ$ beam |

<div class="callout">The same 0.30 m is 10λ at 10 GHz and 3λ at 3 GHz, so the beam widens from 5.08° to 16.9°.</div>

Note:
Last row is the one to dwell on. The same dish at a third of the frequency has a beam
more than three times wider. This is why radar goes up in frequency for resolution.

---

## Rectangular and Circular Apertures

A **rectangular** aperture with separable illumination factors into two line sources:

$$\theta_{\text{HP},x} = 0.886\ \frac{\lambda}{L_x} \qquad \theta_{\text{HP},y} = 0.886\ \frac{\lambda}{L_y}$$

A uniform **circular** aperture of diameter $D$ gives a Bessel pattern (Lesson 14):

$$\theta_\text{HP} = 1.029\ \frac{\lambda}{D} = 59^\circ\ \frac{\lambda}{D} \qquad \text{first sidelobe } -17.6\ \text{dB}$$

Note:
The circle does better on sidelobes because its edges carry less area than a
rectangle's do — it is already mildly tapered along any cut. Long dimension always
makes the narrow beam; that trips people up every year.
The circle's numbers are lesson fourteen's: the disk integral is two J one of u over u,
with u equal to pi D over lambda times sine theta, and its half-power point at u equal
to 1.616 gives 1.029 lambda over D, or 59 degrees.
A separable illumination also splits the aperture efficiency: both integrals factor,
so eta ap equals eta x times eta y. The X-band example uses that.

---

## Rectangular Aperture and Its Beam

<div class="fig" data-inline-svg="./fig/L15-rect-footprint.svg" style="max-width:780px; margin:0 auto;"></div>

The long dimension makes the narrow beam: $0.682$ m gives $3^\circ$ in azimuth, and $0.152$ m gives $10^\circ$ in elevation.

Note:
This is the X-band aperture we size at the end of the hour, drawn to scale. The
beam's footprint is the aperture turned ninety degrees: wide aperture, narrow beam
in that plane. Students get this backwards every year, so point at each dimension
and its beamwidth in turn. The contour is the half-power contour of the product of
the two line-source patterns, cosine across and uniform up.

---

## Circle Against Square

<div class="fig" data-inline-svg="./fig/L15-circle-vs-square.svg" style="max-width:820px; margin:0 auto;"></div>

The circle's beam is $1.029$ against $0.886$, and its first sidelobe is $-17.6$ dB against $-13.3$ dB.

Note:
Both patterns are plotted against sine theta times the width in wavelengths, so the
square's width and the circle's diameter are the same number. The inset is the
reason for the difference: seen along one cut, the circle's area falls off toward
the edges like the square root of one minus x squared. It is a mildly tapered
aperture, so it trades a little beamwidth for lower sidelobes, the same trade the
taper table makes on purpose.

---

## How Much of the Area Counts?

Lesson 2 defined the **aperture efficiency** as the fraction of the physical area $A$ the antenna uses, $A_e = \eta_\text{ap} A$.

$$D = \eta_\text{ap}\ \frac{4\pi A}{\lambda^2} \qquad G = \eta_\text{rad} D$$

Lesson 13 derived $\eta_\text{ap}$ from the aperture field. Today we evaluate it for four illuminations.

Note:
A sub e came from lesson two, and lessons thirteen and fourteen already used the
ratio on the horn and the reflector. Horns and reflectors dissipate almost nothing,
so eta rad is about one and gain equals directivity: G is about eta ap times four pi
A over lambda squared.

---

## Aperture Efficiency as a Ratio

At boresight every point on the aperture arrives in phase, so the field is the **coherent** sum $\int E_a\ dS'$.

The power you had to supply is proportional to $\int \vert E_a\vert^2 dS'$.

$$D = \frac{4\pi}{\lambda^2}\ \frac{\left\vert \int E_a\ dS' \right\vert^2}{\int \vert E_a\vert^2\ dS'} \qquad \eta_\text{ap} = \frac{\left\vert \int E_a\ dS'\right\vert^2}{A \int \vert E_a\vert^2\ dS'}$$

<div class="callout">Read it as <strong>coherent gain over available gain</strong>. Cauchy-Schwarz caps it at one, reached only for constant amplitude <em>and</em> constant phase.</div>

Note:
Do not prove Cauchy-Schwarz. Do say what it means physically: any variation in
amplitude or phase across the aperture lowers the efficiency, and uniform is the best there is.
This is lesson thirteen's chain, in its notation. U max is k squared over eight pi
squared eta naught times the coherent sum squared; P rad is one over two eta naught
times the integral of the field magnitude squared. Four pi U max over P rad is the
directivity on the slide. Evaluated with the amplitude alone, the ratio is lesson
fourteen's taper efficiency, eta t.

---

## Worked Example: Cosine Illumination

A horn mouth carries $E_a = \cos(\pi x/L)$ across its broad dimension. Work in $\xi = x/L$, so the aperture length is $1$:

| Quantity | Work | Result |
| :-- | :-- | :-- |
| Coherent sum | $\int \cos(\pi\xi)\ d\xi$ | $2/\pi$ |
| Available | $\int \cos^2(\pi\xi)\ d\xi$ | $1/2$ |
| Taper efficiency | $(2/\pi)^2 / (1 \times 1/2)$ | $8/\pi^2 = 0.811$ |
| Gain penalty | $10\log_{10}(0.811)$ | $-0.9$ dB |

Same arithmetic gives $0.75$ for triangular and $2/3$ for $\cos^2$.

Note:
Have them do the triangular case on the spot. One half squared over one third is
zero point seven five. It takes twenty seconds and it convinces them the definition
is usable.

---

## Coherent Sum and Available Power

<div class="fig" data-inline-svg="./fig/L15-efficiency-ratio.svg" style="max-width:860px; margin:0 auto;"></div>

The taper efficiency is the square of the left mean over the right mean: $(2/\pi)^2/(1/2) = 0.811$.

Note:
The left panel is the numerator: the field across the aperture, whose mean is the
coherent sum, two over pi. The right panel is the denominator: the field squared,
whose mean is the power the aperture radiates, one half. Uniform illumination
would put both means at one. The taper pulls the field mean down faster than the
power mean, and that is the 0.9 dB.

---

## Other Aperture-Efficiency Losses

Amplitude taper is only one term. A real reflector also loses to:

- spillover past the rim
- phase error across the surface
- feed and strut blockage
- cross-polarization

<div class="callout">A horn typically reaches $\eta_\text{ap} \approx 0.5$ and a good reflector $0.55$ to $0.7$. $\eta_\text{ap}$ is not radiation efficiency — none of these losses turns into heat.</div>

Note:
The measured aperture efficiency is the product of all of these. That is why a horn
comes in near one half even though its cosine taper alone predicts zero point eight
one: lesson thirteen found 0.78 times 0.77 times 0.81, or 0.49, with the first two
factors from the flare's phase error. Lesson fourteen's efficiency budget took an
ordinary reflector to 0.66 with a taper factor of 0.85 and spillover, eta s, of 0.90.
Keep eta rad and eta ap separate in their heads.

---

## The Reflector Efficiency Budget

<div class="fig" data-inline-svg="./fig/L14-efficiency-budget.svg" style="max-width:820px; margin:0 auto;"></div>

Lesson 14's ordinary reflector: the taper factor is $0.85$, and the product of all five factors is $0.66$.

Note:
The same waterfall as lesson fourteen. Each bar multiplies the one before it:
spillover 0.90, taper 0.85, blockage 0.95, surface 0.94, everything else 0.97. None
of these is heat. The taper bar is the only one today's integrals compute; the rest
come from the feed, the struts, and the surface.

---

## Edge Smoothness and Sidelobe Decay

<div class="fig" data-inline-svg="./fig/L15-sidelobe-decay.svg" style="max-width:760px; margin:0 auto;"></div>

A step at the edge gives sidelobes that fall $6$ dB per octave, a zero reached with a slope gives $12$ dB, and a zero reached with zero slope gives $18$ dB.

Note:
This is the physical reason tapering works. The axis is logarithmic in u, so each
tick is an octave and each envelope is a straight line. The uniform illumination
steps to zero at the edge and its sidelobes fall as one over u. The cosine reaches
zero continuously but with a slope, one over u squared. Cosine squared arrives with
zero slope too, one over u cubed. Each order of smoothness at the edge adds one
power of u.

---

## The Taper Trade

| Illumination | First sidelobe | HPBW $\times\ \lambda/L$ | $\eta_t$ | Gain |
| :-- | :-- | :-- | :-- | :-- |
| Uniform | $-13.3$ dB | $0.886$ | $1.00$ | $0$ dB |
| Cosine | $-23$ dB | $1.19$ | $0.81$ | $-0.9$ dB |
| Triangular | $-26.5$ dB | $1.28$ | $0.75$ | $-1.25$ dB |
| Cosine$^2$ | $-31.5$ dB | $1.44$ | $0.667$ | $-1.8$ dB |

<div class="callout">Going from uniform to $\cos^2$ lowers the first sidelobe by 18 dB, widens the beam by 63%, and loses 1.8 dB of gain. No illumination lowers sidelobes and narrows the beam at once.</div>

Note:
This table carries the main design numbers of the lesson. Tell them it will be on every exam and in
both tapering labs. The physical story is the edge discontinuity: a step in the
illumination transforms into slowly decaying sidelobes.

---

## Sidelobe Against Beamwidth

<div class="fig" data-inline-svg="./fig/L15-taper-trade.svg" style="max-width:700px; margin:0 auto;"></div>

Every step toward lower sidelobes widens the beam and loses gain.

Note:
The same four rows as the table, as points. Read it left to right: each
illumination buys lower sidelobes with a wider beam and a fraction of a dB of gain.
There is no point below the line, which is the statement that no illumination
lowers sidelobes and narrows the beam at once.

---

<!-- .slide: class="viz-cue-slide" -->

## Four Illuminations and Their Patterns

<div class="fig" data-inline-svg="./fig/L15-taper-comparison.svg" style="max-width:690px; margin:0 auto;"></div>

<p class="viz-cue">↗ Interactive on the lesson page</p>

Note:
Demo live. Open the aperture-distribution widget, step through the four illuminations
at ten wavelengths, and read the pills aloud — the sidelobe level and the beamwidth
constant move together. Then drag the length slider and show that neither pill moves
while the pattern squeezes in angle. Size sets beamwidth and gain; shape alone sets the sidelobes.

---

## Arrays as Sampled Apertures

The same trade appears with sums in place of integrals.

$$\eta_t = \frac{\left(\sum a_n\right)^2}{N \sum a_n^2}$$

That is the identical ratio of coherent to available gain, over $N$ element amplitudes.

The PHASER's Hann preset is the $\cos^2$ row sampled at the elements. Blackman tapers harder than any row.

<div class="fig" data-inline-svg="./fig/L16-sampled-aperture.svg" style="max-width:560px; margin:0 auto;"></div>

Note:
Forward reference only. Lessons twenty-four and twenty-five do this on the hardware.
Mention that the peak drop they will see on the plot is not the same number as the
taper efficiency, and that we will keep those straight when we get there.

---

## Designing in Wavelengths

Every result today depends on $L/\lambda$ and $A/\lambda^2$, never on $L$ or $A$ alone.

- Beamwidth scales as $\lambda/L$. Doubling the aperture in wavelengths halves the beam.
- Gain scales as $A/\lambda^2$. Doubling both dimensions raises the gain by $6$ dB.

<div class="callout">Move an antenna from 10 to 20 GHz and it doubles in wavelengths: both beamwidths halve and gain rises 6 dB — provided the feed still illuminates it the same way.</div>

Note:
The proviso is real. A feed horn's own pattern changes with frequency, so the
illumination taper on a reflector is not constant across a wide band. It is still the
right first estimate.

---

## One Aperture Across Frequency

<div class="fig" data-inline-svg="./fig/L15-frequency-scaling.svg" style="max-width:580px; margin:0 auto;"></div>

The $0.30$ m aperture has a $17.0^\circ$ beam at $3$ GHz and a $5.08^\circ$ beam at $10$ GHz, and a $0.30$ m square gains $20.5$ dBi and $31.0$ dBi.

Note:
The ten-wavelength worked example, swept across frequency. The beamwidth uses the
exact two arcsine of 0.4429 lambda over L, which gives 17.0 degrees at 3 gigahertz;
the small-angle formula gives 16.9. The gain is for a uniform 0.30 meter square, four
pi A over lambda squared, and it rises 6 dB for every doubling of frequency.

---

## Worked Example: Sizing at X-Band

Spec: $3^\circ$ azimuth, $10^\circ$ elevation, azimuth sidelobes below $-20$ dB. At $10$ GHz, $\lambda = 0.03$ m.

| Quantity | Work | Result |
| :-- | :-- | :-- |
| Illumination | uniform is $-13.3$ dB; cosine is $-23$ dB | cosine, $1.19$ |
| Azimuth | $1.19(0.03)/0.05236$ | $0.682$ m $= 22.7\lambda$ |
| Elevation | $0.886(0.03)/0.1745$ | $0.152$ m $= 5.08\lambda$ |
| Gain | $0.81\ (4\pi)(0.104)/(0.03)^2$ | $30.7$ dBi |

Note:
Walk the order deliberately. Sidelobe spec picks the illumination, illumination fixes
the beamwidth constant, beamwidth spec fixes the length, and gain falls out last.
Gain is the output of an aperture design, not an input.
The area is 0.682 times 0.152, or 0.104 square meters. The efficiency is eta x times
eta y, 0.81 for the cosine in azimuth times 1.00 for uniform in elevation.

---

## Checking the Gain

Pencil-beam estimate from Lesson 2:

$$\frac{41{,}253}{3 \times 10} = 1375 \rightarrow 31.4\ \text{dBi (lossless bound)}$$

Practical constant $26{,}000$ to $32{,}400$ gives $29.4$ to $30.3$ dBi.

Our $30.7$ dBi sits just above that band — right for an aperture whose only loss is a known taper.

Far field: the largest dimension is the diagonal, $0.699$ m, so $2D^2/\lambda = 33$ m. A $33$ m far-field distance rules out pattern testing in an ordinary room.

Note:
Two takeaways. First, always cross-check an aperture gain against the pencil-beam
number. Second, the far-field distance is why the midterm project uses small antennas
and why real ranges are expensive.
Lesson five defined D as the largest dimension, which for a rectangle is the diagonal:
the square root of 0.682 squared plus 0.152 squared is 0.699 meters.

---

## The X-Band Design Chain

<div class="fig" data-inline-svg="./fig/L15-xband-flow.svg" style="max-width:640px; margin:0 auto;"></div>

The sidelobe specification picks the illumination, the beamwidth fixes each length, and the gain comes out last.

Note:
Read it left to right, row by row. Minus twenty dB rules out uniform, so azimuth is
cosine with constant 1.19, and the 3 degree beam fixes 0.682 meters. Elevation has no
sidelobe limit, so it stays uniform at 0.886, and 10 degrees fixes 0.152 meters. The
area and the efficiency give 30.7 dBi, which lands just above the practical band and
under the pencil-beam bound.

---

## Key Point: Shape and Size

<div class="callout">The far field is the <strong>Fourier transform</strong> of the aperture field. <strong>Shape of the illumination</strong> sets the sidelobe level, the beamwidth constant, and the taper efficiency. <strong>Size in wavelengths</strong> scales the beamwidth and the gain and leaves the sidelobe level alone. Every antenna and array design in this course sets both.</div>

Note:
If they remember one slide from lesson fifteen, this is it. Ask them to state it back
before moving on.

---

## Looking Ahead to Lesson 16

**Lesson 16** samples the aperture: $N$ elements spaced $d$ apart, sum instead of integral, and the space factor becomes the **array factor**. The $0.886$ constant and the taper trade carry over, now set by element weights that the hardware can change electronically.

The Fourier view carries the whole module — steering is a phase ramp, tapering is the table above, grating lobes are undersampling.

Before Lesson 16, be able to state $0.886\ \lambda/L$, $-13.3$ dB, and the definition of $\eta_\text{ap}$ from memory.

Note:
Remind them the midterm pattern-measurement project is due at lesson twenty, and the
predicted beamwidth and sidelobe numbers in that report come from today.
