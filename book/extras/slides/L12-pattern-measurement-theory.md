<!-- .slide: class="title-slide" -->

<div class="title-left">

# ECE 444

Antennas, Phased Arrays, and Radar Systems

## Lesson 12 — Pattern Measurement Theory

Fall 2026 · Dr. Neil Rogers

</div>

<div class="title-right">

![USAFA](./img/01-course-intro/USAFA-logo.png)

</div>

---

## Where we were

- L10 and L11 built the high-gain antennas — horns, reflectors, the standard gain horn — and told you their gain from geometry and aperture efficiency.
- L11 also handed you the midterm project: measure an antenna pattern.
- Every pattern we have drawn so far came out of an integral, not off an instrument.
- L5 gave us the far-field boundary $r \geq 2D^2/\lambda$ and then we filed it away.

**Today that boundary becomes the length of your range.**

Note:
Anchor the whole lesson on the midterm. They already know what they have to do; today is why the procedure looks the way it does.

---

## Today's plan

1. What a valid measurement demands: a plane wave across the antenna under test.
2. Turning that demand into a range length, and what a short range does to your data.
3. Range types: outdoor, anechoic chamber, compact range.
4. Near-field scanning, and why the transform is the same one from L6.
5. Gain by comparison, and pattern cuts and polarization.

---

## The measurement problem, inverted

Every pattern in this course is defined the same way: illuminate the antenna with a **plane wave** and record what comes out, or transmit and record the field on a distant sphere. Same thing, by reciprocity.

On a range you cannot buy a plane wave. You buy a source antenna at a finite distance, which radiates a **spherical** wave.

<div class="callout">
A range is a machine for <strong>simulating a plane wave</strong> over the volume the antenna occupies. Every design rule below is a tolerance on that approximation.
</div>

Note:
Reciprocity carries the argument: measure in receive, publish as transmit. State it explicitly, because they will ask.

---

## Two tolerances, not one

<div class="fig" data-inline-svg="./fig/L12-range-geometry.svg" style="max-width:700px; margin:0 auto;"></div>

- **Amplitude taper** — the source antenna's own pattern falls off across the AUT. Spec: under 0.25 dB edge to edge.
- **Phase curvature** — the spherical wavefront runs behind at the edges. Spec: under 22.5° edge to center, and it is the spec that sets the range length.

Note:
Two knobs, and students always remember only the second. The amplitude one is why the source antenna on a range is deliberately a modest-gain horn, not the biggest dish available.

---

## Where 2D²/λ actually comes from

The extra path from the source to the aperture edge, over the path to the center, is the sagitta of the wavefront:

$$\Delta \ell \approx \frac{(D/2)^2}{2r} = \frac{D^2}{8r}$$

Turn it into phase and demand no more than an eighth of a wavelength of error, $\pi/8$ radians:

$$\Delta\phi_{\max} = k\ \Delta \ell = \frac{\pi D^2}{4\lambda r} \leq \frac{\pi}{8} \quad \Longrightarrow \quad r \geq \frac{2D^2}{\lambda}$$

<div class="callout">
$2D^2/\lambda$ is <strong>22.5° of edge phase error</strong>, written as a distance.
</div>

Note:
Do the algebra on the board: set the pi/8 tolerance and solve for r. They have seen 2D squared over lambda since L5 and have never seen where it comes from.

---

## Worked example — how long a range?

A 0.5 m reflector, tested at 10 GHz.

| Quantity | Work | Result |
| :-- | :-- | :-- |
| Wavelength | $\lambda = c/f = (3\times10^8)/(10\times10^9)$ | $0.03\ \text{m}$ |
| Aperture in wavelengths | $D/\lambda = 0.5/0.03$ | $16.7$ |
| Far-field distance | $2D^2/\lambda = 2(0.5)^2/0.03$ | $16.7\ \text{m}$ |
| Beamwidth to resolve | $\approx 51 \lambda/D$ | $3.1°$ |

A 17 m chamber is large and expensive, and entirely ordinary for this class of antenna.

Note:
16.7 m is about 55 feet. Ask them to picture the chamber before the next slide scales the problem up.

---

## The same arithmetic, one step further

A 3 m reflector at 30 GHz — a perfectly normal satellite terminal.

| Quantity | Work | Result |
| :-- | :-- | :-- |
| Wavelength | $\lambda = (3\times10^8)/(30\times10^9)$ | $0.01\ \text{m}$ |
| Far-field distance | $2D^2/\lambda = 2(9)/0.01$ | $1800\ \text{m}$ |

<div class="callout">
A far-field range for this antenna would be <strong>1.8 km long</strong>. Nobody builds that, and this single number is why compact ranges and near-field scanners exist.
</div>

Note:
This is the hinge of the lesson: everything after it is a way of avoiding a 1.8 km room.

---

## What a short range actually costs you

<p class="viz-cue">↗ Interactive on the lesson page</p>

Quadratic phase is a taper you did not ask for. It fills the nulls long before it touches the beamwidth.

| Range, as a fraction of $2D^2/\lambda$ | Edge phase error | First null fills to |
| :-- | :-- | :-- |
| 2 | 11.3° | $-28$ dB |
| 1 | 22.5° | $-22$ dB |
| 1/2 | 45° | $-16$ dB |
| 1/4 | 90° | $-9.5$ dB |

<div class="callout">
$2D^2/\lambda$ is a <strong>main-beam and gain</strong> criterion. Chasing a $-40$ dB sidelobe, go to $5D^2/\lambda$ — or stop using a far-field range.
</div>

Note:
Demo live: start at 2, slide down to a quarter. Point out that the first null collapses into a shoulder while the main beam keeps its width, so the pattern still looks correct at a glance. Low-sidelobe work is where near-field scanning wins; foreshadow it here.

---

## Why the source antenna is modest-gain

The amplitude spec bites from the other direction. The AUT subtends an angle $D/r$ as seen from the source.

- For under 0.25 dB of taper, the source pattern must stay flat over that whole angle.
- Rule of thumb: **source beamwidth at least 3–4× the angle the AUT subtends**.
- So range source antennas are modest-gain horns. A high-gain source would taper the illumination and widen every beamwidth you report.

<div class="callout">
A higher-gain source antenna makes the illumination <strong>worse</strong>, not better.
</div>

---

## Three ways to make the plane wave

| Range | How it fakes the plane wave | Watch out for |
| :-- | :-- | :-- |
| Outdoor / elevated | Brute-force distance | Weather, ground bounce, no security |
| Anechoic chamber | Distance plus absorber | Room must still be long enough |
| Compact range | A reflector collimates up close | Edge diffraction, feed spillover |
| Near-field scanner | Measure close, transform out | Needs phase, needs a good probe |

The first three are far-field ranges: they physically deliver the wave. The fourth changes the question.

---

## Inside an anechoic chamber

<div class="fig" data-inline-svg="./fig/L12-anechoic-chamber.svg" style="max-width:760px; margin:0 auto;"></div>

Note:
Point out that the walls are not uniformly treated in a real chamber — the specular regions get the tall absorber, the rest gets shorter and cheaper stuff.

---

## What the absorber does

Carbon-loaded foam pyramids. The taper is a gradual impedance transition into a lossy medium — the wave gets in without a reflection, then dies.

- Quoted as **reflectivity in dB**: a good pyramid is $-40$ to $-50$ dB at normal incidence.
- It gets **worse at grazing incidence** — which is why the side walls, hit at a slant, are the hard problem.
- Taller pyramids in wavelengths means better absorption. At low frequencies the absorber gets enormous.

<div class="callout">
A chamber is never "no reflections". It is <strong>reflections below a stated level</strong>.
</div>

---

## What −40 dB of stray field buys you

One stray reflection at $-40$ dB, adding in and out of phase as the positioner turns, ripples your measurement:

| What you are measuring | Error a $-40$ dB stray adds |
| :-- | :-- |
| Main beam peak (0 dB) | $\pm 0.09$ dB |
| A $-20$ dB sidelobe | $+0.8 / -0.9$ dB |
| A $-30$ dB sidelobe | $+2.4 / -3.3$ dB |

<div class="callout">
The chamber spec you need is set by the <strong>lowest level you intend to believe</strong>, not by the main beam.
</div>

Note:
Draw attention to the third row: a 3 dB error on a sidelobe is large, and the chamber that produced it still meets a good specification.

---

## The quiet zone

The deliverable of a chamber is not the room. It is a **volume** — usually a sphere or cylinder around the positioner — inside which the stray field is guaranteed below the spec.

- Specified as a size **and** a level: "1.2 m quiet zone at $-45$ dB, 2–18 GHz".
- Measured, not assumed: a free-space VSWR probe sweep maps the ripple through the volume.
- **The AUT must fit inside it.** An antenna that overhangs the quiet zone is being measured in a room, not a chamber.

---

## Compact range — a reflector does the collimating

<div class="fig" data-inline-svg="./fig/L12-compact-range.svg" style="max-width:680px; margin:0 auto;"></div>

- The L11 parabola run backwards: feed at the focus, every path to the aperture plane the same length, plane wave a few meters later.
- Quiet zone is roughly **50–60% of the reflector aperture**, so the reflector is much bigger than the AUT.
- The rim is **serrated or rolled** — a hard edge diffracts, and that diffraction is a second source sitting inside your quiet zone.

Note:
Far-field conditions in a room a small fraction of 2D squared over lambda long, paid for with a precision reflector. There the plane wave left for space; here it only has to cross the room.

---

## Near-field scanning — change the question

<div class="fig" data-inline-svg="./fig/L12-nearfield-scan.svg" style="max-width:790px; margin:0 auto;"></div>

---

## Why the transform works

L6 gave you the machinery: the far field is the **Fourier transform** of the source distribution. A radiation integral is a Fourier integral with $k\sin\theta$ as the frequency variable.

- Fourier transforms are **invertible**. Given the complex field on a surface enclosing the antenna, the field everywhere outside it is determined.
- So sampling tangential $\mathbf{E}$ on a plane a few wavelengths out, then transforming, gives the same far field the long range would have measured.
- There is no new physics here: the same relationship that *produced* the pattern is being run in the other direction.

<div class="callout">
You must measure <strong>amplitude and phase</strong>. Magnitude alone does not determine a transform.
</div>

Note:
Press the phase point. This is why a near-field range needs a vector network analyzer and a phase-stable cable, and why a swept-magnitude setup cannot do it.

---

## The three scan surfaces

| Surface | Best for | Pattern coverage |
| :-- | :-- | :-- |
| Planar | High-gain, directive antennas | A forward cone, roughly ±60° |
| Cylindrical | Fan beams, sector antennas | Full azimuth, limited elevation |
| Spherical | Low gain, anything | The complete sphere |

Two more rules that matter: sample at **half-wavelength spacing or finer** (undersampling aliases into false lobes, exactly as in L6's spatial spectrum), and scan a plane **wide enough** that the field has died at the edges.

Note:
Probe compensation — dividing out the probe's own pattern — is a real and necessary step. Name it, do not derive it.

---

## Gain by comparison

Gain is a ratio, so measure it as one. Put the AUT on the positioner, record the received power. Swap in a **standard gain horn** with a calibrated gain curve, change nothing else, record again:

$$G_\text{AUT} = G_\text{SGH} + \left( P_\text{AUT} - P_\text{SGH} \right) \quad \text{(all in dB)}$$

Everything in Friis that you do not know — transmit power, source gain, range, cable loss — is identical in both measurements and subtracts out.

<div class="callout">
The method is also called <strong>gain transfer</strong>. The horn's calibration is the only absolute number in the room.
</div>

Note:
Conditions on validity: same position, same polarization, same frequency, and both antennas well matched or the mismatch corrected.

---

## Worked example — comparison method

| Quantity | Work | Result |
| :-- | :-- | :-- |
| Standard gain horn power | measured | $-38.6\ \text{dBm}$ |
| AUT power | measured | $-33.1\ \text{dBm}$ |
| Difference | $-33.1 - (-38.6)$ | $+5.5\ \text{dB}$ |
| Horn gain at this frequency | from the calibration curve | $16.8\ \text{dBi}$ |
| AUT gain | $16.8 + 5.5$ | $22.3\ \text{dBi}$ |

The whole method is five numbers, one subtraction, and one addition.

---

## When there is no standard

Two identical antennas, Friis in dB, and one unknown:

$$P_r - P_t = 2G + 20\log_{10}\!\left(\frac{\lambda}{4\pi R}\right)$$

At $R = 20\ \text{m}$ and $6\ \text{GHz}$, with $P_t = 0\ \text{dBm}$ and $P_r = -40.0\ \text{dBm}$: the path term is $-74.0$ dB, so $2G = 34.0$ dB and $G = 17.0\ \text{dBi}$.

If the antennas are **not** identical, use three of them and measure all three pairs:

$$G_A = \tfrac{1}{2}\left( M_{AB} + M_{AC} - M_{BC} \right)$$

Note:
M is the measured pair sum with the path loss already removed. Three equations give three unknowns, with no calibrated standard involved, which is how the standard gain horns themselves are calibrated.

---

## Pattern cuts and principal planes

<div class="fig" data-inline-svg="./fig/L12-pattern-cuts.svg" style="max-width:640px; margin:0 auto;"></div>

- **Great-circle cut** — hold $\phi$, sweep $\theta$ through the poles. **Conical cut** — hold $\theta$, sweep $\phi$: a ring at a fixed angle off boresight.
- **Principal planes** — the E-plane holds the aperture electric field and boresight, the H-plane is perpendicular. For a horn, those are the two cuts you always publish.
- Two principal cuts describe a well-behaved pencil beam, and say nothing about the diagonal planes, where the sidelobes often sit.

---

## Polarization measurements

Run the same cut twice.

- **Co-pol** — source antenna aligned with the AUT's nominal polarization.
- **Cross-pol** — rotate the source 90° about the range axis and repeat. A good linear antenna sits 20–30 dB down on boresight, and much worse off-axis.
- **Spinning linear** — spin the linear source continuously while sweeping. The pattern comes back as an envelope, and the **peak-to-trough ripple in dB is the axial ratio** (L3). A perfect circular antenna gives no ripple at all.

Note:
Spinning linear is the fastest axial-ratio measurement available, and it pays off the polarization ellipse work from L3.

---

## Key point

<div class="callout">
<p>A pattern measurement is a <strong>plane-wave simulator plus a subtraction</strong>.</p>
<p>The range fakes the plane wave to a stated tolerance — 22.5° of phase, 0.25 dB of taper, a quiet zone at −45 dB. The gain comes from differencing against a calibrated standard. Every number you report is only as good as the tolerance behind it.</p>
</div>

---

## Where this is going

- **L13 and L14** are the labs. L13 measures S-parameters — match and bandwidth on the bench. L14 puts an antenna on the positioner and takes the cuts.
- The **midterm project, due L20**, is exactly this: measure a pattern, extract HPBW and sidelobe level, measure gain by comparison, and defend the numbers.
- When you write that report, the range length, the quiet-zone spec, and the standard horn's calibration are your **error budget**. Today was how to build one.

Note:
Send them out knowing that "I measured it" is not an engineering result, while "I measured it, and here is what the range could and could not tell me" is.
