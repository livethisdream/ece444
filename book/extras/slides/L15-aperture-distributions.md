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

## Where we were

- Lesson 14 closed the measurement work: you turned an antenna and recorded a pattern.
- Module 1 gave us the radiation integral, $2D^2/\lambda$, and $A_e = G\lambda^2/4\pi$.
- Lesson 6 showed the far field is the Fourier transform of the source distribution.
- The midterm pattern-measurement project is due at Lesson 20.

**Module 3 reverses the job. You now choose the pattern, and the aperture field is the knob.**

Note:
Module two was about characterizing an antenna somebody handed you. Module three is
about designing the pattern you want. Everything in this module comes out of one
relationship they already met in lesson six, so today is about turning that
relationship into design numbers they can use without deriving anything.

---

## Today's plan

1. The aperture distribution, and why it alone sets the far field.
2. Derive the uniform aperture pattern, and read three numbers off it.
3. Aperture efficiency, from the illumination to the gain formula.
4. The taper trade: sidelobes against beamwidth and gain.
5. Sizing an aperture at X-band.

Note:
Point out that steps two and four give them numbers they will use in every remaining
lesson of the course, including both labs on the PHASER.

---

## The aperture is the source

An **aperture** is the opening the wave leaves through — a horn mouth, a reflector face, a row of patches. The far field depends on the tangential field across that opening and on nothing else.

<div class="fig" data-inline-svg="./fig/L15-aperture-to-pattern.svg" style="max-width:720px; margin:0 auto;"></div>

Change the distribution and you change the pattern. Leave it alone and nothing behind the aperture matters.

Note:
Emphasize the second sentence. Students want to explain patterns by what is behind
the aperture — the waveguide, the feed, the subreflector. Those only matter through
the field they produce on the opening.

---

## The transform relationship

For an aperture of length $L$ on the $x$ axis, with $\theta$ measured from broadside:

$$S(\theta) = \int_{-L/2}^{L/2} E_a(x)\ e^{\ jkx\sin\theta}\ dx$$

The exponent is the extra path from the point at $x$, turned into phase.

Define the **space frequency** $u = (L/\lambda)\sin\theta$.

<div class="callout"><strong>Shape</strong> of the illumination sets the pattern in <em>u</em>. <strong>Size</strong> in wavelengths sets how many degrees each unit of <em>u</em> costs.</div>

Note:
Derive this at the board if there is time — it is one line from the radiation integral
of lesson six. The substitution to u is the move that makes every result reusable.
Write u on the board and leave it there for the rest of the hour.

---

## One convention note

Module 1 measured the polar angle from the wire axis. Module 3 measures $\theta$ from **broadside**.

That is what every phased-array plot and every PHASER readout uses.

So the space frequency carries $\sin\theta$ here, not $\cos\theta$.

Lesson 16 makes the substitution explicit once, and then we never revisit it.

Note:
Do not spend more than a minute here, but do say it out loud. Students who go read
Balanis will find cosine theta and think one of the two is wrong.

---

## Derive it: uniform illumination

Constant field $E_a(x) = E_0$ across the whole opening:

$$S(\theta) = E_0\int_{-L/2}^{L/2} e^{\ jkx\sin\theta}\ dx$$

The integrand is an exponential, so the integral is elementary:

$$S(\theta) = E_0\ \frac{e^{\ jkL\sin\theta/2} - e^{-jkL\sin\theta/2}}{jk\sin\theta}$$

Note:
Do this one at the board. It is the only integral in the lesson and it takes thirty
seconds. Remind them the difference of two exponentials over two j is a sine.

---

## Derive it: the sinc

Two exponentials over $2j$ make a sine:

$$S(\theta) = E_0 L\ \frac{\sin\left(\tfrac{1}{2}kL\sin\theta\right)}{\tfrac{1}{2}kL\sin\theta}$$

With $k = 2\pi/\lambda$ the argument is exactly $\pi u$:

$$\vert F(u)\vert = \left\vert\frac{\sin \pi u}{\pi u}\right\vert \qquad u = \frac{L}{\lambda}\sin\theta$$

<div class="callout">A uniformly illuminated aperture radiates a <strong>sinc</strong> pattern in space frequency. Everything else today is bookkeeping on this one line.</div>

Note:
Stress that the L came out front and the shape did not depend on it. That is the
whole shape-versus-size split, visible in one equation.

---

## Reading the sinc: nulls

$\sin \pi u$ vanishes at $u = \pm 1, \pm 2, \pm 3, \dots$

So the first null sits at $\sin\theta = \lambda/L$.

An aperture shorter than a wavelength has **no null in real space** — it radiates broadly no matter how you feed it.

Note:
Ask them what happens when L over lambda drops below one. The first null needs a sine
greater than one, which does not exist. That is why small antennas are always broad.

---

## Reading the sinc: beamwidth

Solve $\sin(\pi u)/(\pi u) = 1/\sqrt{2}$:

$$\pi u = 1.3916 \qquad u = \pm 0.4429$$

$$\theta_\text{HP} \approx 0.886\ \frac{\lambda}{L} \text{ rad} = 50.8^\circ\ \frac{\lambda}{L}$$

<div class="callout">Memorize <strong>0.886</strong>. It reappears in the array beamwidth formula in Lesson 20 and in every PHASER prediction you make.</div>

Note:
Point eight eight six is the single most reused number in the module. Have them write
it down. The array version is zero point eight eight six lambda over N d.

---

## Reading the sinc: sidelobes

First sidelobe peaks near $u = 1.43$, where $\vert F\vert = 0.217$.

$$20\log_{10}(0.217) = -13.3\ \text{dB}$$

Notice what is missing from that number: **$L$**.

A longer uniform aperture narrows the beam, raises the gain, and leaves the first sidelobe $13.3$ dB down.

Note:
This is the punchline of the first half. Size buys beamwidth and gain. Sidelobes are
bought with shape, and shape only. Say it twice.

---

## The uniform aperture pattern

<div class="fig" data-inline-svg="./fig/L15-uniform-pattern.svg" style="max-width:760px; margin:0 auto;"></div>

Note:
Walk the figure: main lobe, half-power width in green, first null at u equal to one,
first sidelobe at minus thirteen point three. Ask where the pattern would change if
they doubled L. Answer: only the horizontal scale.

---

## Worked example: a 10-wavelength aperture

| Quantity | Work | Result |
| :-- | :-- | :-- |
| Beamwidth | $50.8^\circ / 10$ | $5.08^\circ$ |
| First nulls | $\sin\theta = 0.1$ | $\pm 5.74^\circ$ |
| First sidelobe | uniform, any $L$ | $-13.3$ dB |
| Length at $10$ GHz | $10 \times 0.03\ \text{m}$ | $0.30$ m |
| Same $0.30$ m at $3$ GHz | now only $3\lambda$ | $16.9^\circ$ beam |

<div class="callout">The metal did not change. The size <strong>in wavelengths</strong> did.</div>

Note:
Last row is the one to dwell on. The same dish at a third of the frequency has a beam
more than three times wider. This is why radar goes up in frequency for resolution.

---

## Rectangular and circular apertures

**Rectangular**, separable illumination: the double integral factors.

$$\theta_{\text{HP},x} = 0.886\ \frac{\lambda}{L_x} \qquad \theta_{\text{HP},y} = 0.886\ \frac{\lambda}{L_y}$$

**Circular**, uniform, diameter $D$ — quoted, not derived:

$$\theta_\text{HP} = 1.02\ \frac{\lambda}{D} = 58.4^\circ\ \frac{\lambda}{D} \qquad \text{first sidelobe } -17.6\ \text{dB}$$

Note:
The circle does better on sidelobes because its edges carry less area than a
rectangle's do — it is already mildly tapered along any cut. Long dimension always
makes the narrow beam; that trips people up every year.

---

## How much of the area counts?

Module 1 left this hanging: $A_e = G\lambda^2/4\pi$, but how much of the physical area $A$ is that?

$$A_e = \eta_\text{ap} A \qquad G = \eta_\text{ap}\ \frac{4\pi A}{\lambda^2}$$

$\eta_\text{ap}$ is the **aperture efficiency**, and the illumination decides it.

Note:
Remind them A sub e came from the Friis lesson and they have used it since without
ever asking what fraction of the dish it represents. Today they find out.

---

## Aperture efficiency: the ratio

At boresight every point on the aperture arrives in phase, so the field is the **coherent** sum $\int E_a\ da$.

The power you had to supply is proportional to $\int \vert E_a\vert^2 da$.

$$D = \frac{4\pi}{\lambda^2}\ \frac{\left\vert \int E_a\ da \right\vert^2}{\int \vert E_a\vert^2\ da} \qquad \eta_\text{ap} = \frac{\left\vert \int E_a\ da\right\vert^2}{A \int \vert E_a\vert^2\ da}$$

<div class="callout">Read it as <strong>coherent gain over available gain</strong>. Cauchy-Schwarz caps it at one, reached only for constant amplitude <em>and</em> constant phase.</div>

Note:
Do not prove Cauchy-Schwarz. Do say what it means physically: any variation in
amplitude or phase across the aperture costs you, and uniform is the best there is.

---

## Worked example: cosine illumination

Horn mouth in its broad dimension, $E_a = \cos(\pi x/L)$. Work in $\xi = x/L$, aperture length $1$:

| Quantity | Work | Result |
| :-- | :-- | :-- |
| Coherent sum | $\int \cos(\pi\xi)\ d\xi$ | $2/\pi$ |
| Available | $\int \cos^2(\pi\xi)\ d\xi$ | $1/2$ |
| Efficiency | $(2/\pi)^2 / (1 \times 1/2)$ | $8/\pi^2 = 0.811$ |
| Gain penalty | $10\log_{10}(0.811)$ | $-0.9$ dB |

Same arithmetic gives $0.75$ for triangular and $2/3$ for $\cos^2$.

Note:
Have them do the triangular case on the spot. One half squared over one third is
zero point seven five. It takes twenty seconds and it convinces them the definition
is usable.

---

## What else eats aperture efficiency

Amplitude taper is only one term. A real reflector also loses to:

- spillover past the rim
- phase error across the surface
- feed and strut blockage
- cross-polarization

<div class="callout">Horn $\approx 0.5$. Good reflector $0.55$ to $0.7$. And $\eta_\text{ap}$ is <strong>not</strong> radiation efficiency — nothing here turns into heat.</div>

Note:
The measured aperture efficiency is the product of all of these. That is why a horn
comes in near one half even though its cosine taper alone predicts zero point eight
one. Keep eta rad and eta ap separate in their heads.

---

## The taper trade

| Illumination | First sidelobe | HPBW $\times\ \lambda/L$ | $\eta_\text{ap}$ | Gain |
| :-- | :-- | :-- | :-- | :-- |
| Uniform | $-13.3$ dB | $0.886$ | $1.00$ | $0$ dB |
| Cosine | $-23$ dB | $1.19$ | $0.81$ | $-0.9$ dB |
| Triangular | $-26.5$ dB | $1.27$ | $0.75$ | $-1.2$ dB |
| Cosine$^2$ | $-31.5$ dB | $1.44$ | $0.667$ | $-1.8$ dB |

<div class="callout">Uniform to cosine squared buys <strong>18 dB</strong> of sidelobe and charges <strong>63%</strong> more beamwidth plus <strong>1.8 dB</strong> of gain. No illumination lowers sidelobes and narrows the beam at once.</div>

Note:
This table is the reason the lesson exists. Tell them it will be on every exam and in
both tapering labs. The physical story is the edge discontinuity: a step in the
illumination transforms into slowly decaying sidelobes.

---

<!-- .slide: class="viz-cue-slide" -->

## Four illuminations, four patterns

<div class="fig" data-inline-svg="./fig/L15-taper-comparison.svg" style="max-width:690px; margin:0 auto;"></div>

<p class="viz-cue">↗ Interactive on the lesson page</p>

Note:
Demo live. Open the aperture-distribution widget, step through the four illuminations
at ten wavelengths, and read the pills aloud — the sidelobe level and the beamwidth
constant move together. Then drag the length slider and show that neither pill moves
while the pattern squeezes in angle. That is shape versus size in one gesture.

---

## An array is a sampled aperture

The same trade appears with sums in place of integrals.

$$\eta_t = \frac{\left(\sum a_n\right)^2}{N \sum a_n^2}$$

That is the identical ratio of coherent to available gain, over $N$ element amplitudes.

The PHASER's Hann and Blackman presets are the discrete cousins of the cosine and $\cos^2$ rows.

Note:
Forward reference only. Lessons twenty-four and twenty-five do this on the hardware.
Mention that the peak drop they will see on the plot is not the same number as the
taper efficiency, and that we will keep those straight when we get there.

---

## Designing in wavelengths

Every result today depends on $L/\lambda$ and $A/\lambda^2$, never on $L$ or $A$ alone.

- Beamwidth scales as $\lambda/L$. Double the aperture in wavelengths, halve the beam.
- Gain scales as $A/\lambda^2$. Double both dimensions, gain up $6$ dB.

<div class="callout">Move an antenna from 10 to 20 GHz and it doubles in wavelengths: both beamwidths halve and gain rises <strong>6 dB</strong> — provided the feed still illuminates it the same way.</div>

Note:
The proviso is real. A feed horn's own pattern changes with frequency, so the
illumination taper on a reflector is not constant across a wide band. It is still the
right first estimate.

---

## Worked example: sizing at X-band

Spec: $3^\circ$ azimuth, $10^\circ$ elevation, azimuth sidelobes below $-20$ dB. At $10$ GHz, $\lambda = 0.03$ m.

| Quantity | Work | Result |
| :-- | :-- | :-- |
| Illumination | uniform is $-13.3$ dB; cosine is $-23$ dB | cosine, $1.19$ |
| Azimuth | $1.19(0.03)/0.05236$ | $0.68$ m $= 22.7\lambda$ |
| Elevation | $0.886(0.03)/0.1745$ | $0.15$ m $= 5.1\lambda$ |
| Gain | $0.81\ (4\pi)(0.104)/(0.03)^2$ | $30.7$ dBi |

Note:
Walk the order deliberately. Sidelobe spec picks the illumination, illumination fixes
the beamwidth constant, beamwidth spec fixes the length, and gain falls out last.
Gain is the output of an aperture design, not an input.

---

## Sanity-check the answer

Pencil-beam estimate from Lesson 2:

$$\frac{41{,}253}{3 \times 10} = 1375 \rightarrow 31.4\ \text{dBi (lossless bound)}$$

Practical constant $26{,}000$ to $32{,}400$ gives $29.4$ to $30.3$ dBi.

Our $30.7$ dBi sits just above that band — right for an aperture whose only loss is a known taper.

Far field: $2D^2/\lambda = 2(0.68)^2/0.03 = 31$ m. This antenna cannot be tested in a room.

Note:
Two takeaways. First, always cross-check an aperture gain against the pencil-beam
number. Second, the far-field distance is why the midterm project uses small antennas
and why real ranges are expensive.

---

## Key point

<div class="callout">The far field is the <strong>Fourier transform</strong> of the aperture field. <strong>Size in wavelengths</strong> sets beamwidth and gain; <strong>shape of the illumination</strong> sets sidelobes and aperture efficiency. Every antenna and array design in this course is an argument about how to set those two.</div>

Note:
If they remember one slide from lesson fifteen, this is it. Ask them to state it back
before moving on.

---

## Where this is going

**Lesson 16** samples the aperture: $N$ elements spaced $d$ apart, sum instead of integral, and the space factor becomes the **array factor**. Same $0.886$, same taper trade, now in weights you can change electronically.

The Fourier view carries the whole module — steering is a phase ramp, tapering is the table above, grating lobes are undersampling.

Before Lesson 16: know $0.886\ \lambda/L$, $-13.3$ dB, and the definition of $\eta_\text{ap}$ cold.

Note:
Remind them the midterm pattern-measurement project is due at lesson twenty, and the
predicted beamwidth and sidelobe numbers in that report come from today.
