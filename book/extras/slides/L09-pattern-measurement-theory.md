<!-- .slide: class="title-slide" -->

<div class="title-left">

# ECE 444

Antennas, Phased Arrays, and Radar Systems

## Lesson 9 — Measurement Theory

Fall 2026 · Dr. Neil Rogers

</div>

<div class="title-right">

![USAFA](./img/01-course-intro/USAFA-logo.png)

</div>

---

## Where we were

- L7 gave us a dipole on paper; L8 put one in a simulator.
- Every pattern we have drawn came out of an integral, not off an instrument.
- L5 gave us the far-field boundary $r \geq 2D^2/\lambda$ and then we filed it away.

**Today that boundary becomes the length of your range — and the midterm project goes out.**

Note:
Open with the project. It is announced at the end of the hour but flag it now: an antenna pattern measurement, due L20, and this lesson is the reason the procedure looks the way it does. The measurement block runs here, ahead of the remaining antenna families, so they have eleven lessons of bench time instead of six.

---

## Today's plan

All the measurement theory, in one period. The next two lessons are hands-on.

1. What a valid measurement demands: a plane wave across the antenna under test.
2. Turning that demand into a range length, and what a short range costs you.
3. Range types, chambers, compact ranges, and near-field scanning.
4. Gain by comparison, pattern cuts, and polarization.
5. **The other port**: what a VNA measures, calibration, and the reference plane.

Note:
Say out loud that items 1-4 are L11's lesson and item 5 is L10's. They are together today because they are the same question asked at two ports: how much of what an instrument reports is the antenna, and how much is the setup around it.

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

<div class="fig" data-inline-svg="./fig/L09-range-geometry.svg" style="max-width:700px; margin:0 auto;"></div>

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

| Antenna | $\lambda$ | $2D^2/\lambda$ |
| :-- | :-- | :-- |
| 0.5 m reflector at 10 GHz | $0.03\ \text{m}$ | $16.7\ \text{m}$ |
| 3 m terminal at 30 GHz | $0.01\ \text{m}$ | $1800\ \text{m}$ |

A 17 m chamber is large, expensive, and entirely ordinary for that first antenna.

<div class="callout">
Nobody builds a <strong>1.8 km</strong> range. That single number is why compact ranges and near-field scanners exist.
</div>

Note:
16.7 m is about 55 feet. Get them to picture that chamber before the second row scales the problem up by a hundred. The second row is the hinge of the lesson: everything after it is a way of avoiding a 1.8 km room.

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

## Three ways to make the plane wave

| Range | How it fakes the plane wave | Watch out for |
| :-- | :-- | :-- |
| Outdoor / elevated | Brute-force distance | Weather, ground bounce, no security |
| Anechoic chamber | Distance plus absorber | Room must still be long enough |
| Compact range | A reflector collimates up close | Edge diffraction, feed spillover |
| Near-field scanner | Measure close, transform out | Needs phase, needs a good probe |

The first three are far-field ranges: they physically deliver the wave. The fourth changes the question.

---

## Inside a chamber: what the absorber does

<div class="fig" data-inline-svg="./fig/L09-anechoic-chamber.svg" style="max-width:440px; margin:0 auto;"></div>

- A good pyramid is $-40$ to $-50$ dB at normal incidence, and **worse at grazing** — the side walls are the hard problem.
- Taller in wavelengths is better, so low-frequency absorber gets enormous.

<div class="callout">
A chamber is never "no reflections". It is <strong>reflections below a stated level</strong>.
</div>

Note:
Carbon-loaded foam pyramids: the taper is a gradual impedance transition into a lossy medium, so the wave gets in without a reflection and then dies. The walls are not uniformly treated in a real chamber — the specular regions get the tall absorber, the rest gets shorter and cheaper stuff. Which level you need is set by the lowest signal you intend to believe, not by the main beam.

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

<div class="fig" data-inline-svg="./fig/L09-compact-range.svg" style="max-width:680px; margin:0 auto;"></div>

- The L14 parabola run backwards: feed at the focus, every path to the aperture plane the same length, plane wave a few meters later.
- Quiet zone is roughly **50–60% of the reflector aperture**, so the reflector is much bigger than the AUT.
- The rim is **serrated or rolled** — a hard edge diffracts, and that diffraction is a second source sitting inside your quiet zone.

Note:
Far-field conditions in a room a small fraction of 2D squared over lambda long, paid for with a precision reflector. There the plane wave left for space; here it only has to cross the room.

---

## Near-field scanning — change the question

<div class="fig" data-inline-svg="./fig/L09-nearfield-scan.svg" style="max-width:790px; margin:0 auto;"></div>

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

## Pattern cuts, planes, and polarization

<div class="fig" data-inline-svg="./fig/L09-pattern-cuts.svg" style="max-width:560px; margin:0 auto;"></div>

- **Great-circle cut** — hold $\phi$, sweep $\theta$. The **E-plane** holds the aperture field and boresight; the **H-plane** is perpendicular.
- Run every cut twice: source aligned is **co-pol**, source rotated 90° is **cross-pol**. A good linear antenna sits 20–30 dB down on boresight.
- **Spinning linear** — spin the source while sweeping, and the peak-to-trough ripple in dB *is* the axial ratio from L3.

Note:
Two principal cuts describe a well-behaved pencil beam and say nothing about the diagonal planes, where the sidelobes of a rectangular aperture often sit. Spinning linear is the fastest axial-ratio measurement available, and it pays off the polarization ellipse work from L3.

---

## A VNA is a ratio meter

- A source sweeps frequency. **Directional couplers** split off the wave going out and the wave coming back.
- Two receivers measure both, in magnitude *and* phase — the instrument reports their **ratio**.
- It never measures impedance. It measures a reflection and computes everything else from it.

<div class="fig" data-inline-svg="./fig/L10-vna-block.svg" style="max-width:830px; margin:0.2em auto 0;"></div>

Note:
Stress "ratioed": because both waves ride the same source, source drift cancels in the ratio. That is why a pocket-sized NanoVNA can be trusted for this measurement.

---

## The one definition

Call the wave leaving port 1 $a_1$ and the wave returning $b_1$.

$$S_{11} = \frac{b_1}{a_1} \quad \text{(magnitude and phase)}$$

For a one-port device — an antenna — that ratio *is* the reflection coefficient at the reference plane:

$$S_{11} = \Gamma$$

<div class="callout">
One port, one complex number per frequency. Everything the VNA tells you today is a re-dress of <strong>that</strong>.
</div>

Note:
Emphasize complex. Students who remember only |S11| will misread the Smith chart later.

---

## Four names for the same number

| You want | From $\Gamma$ | At $\vert\Gamma\vert = 0.316$ |
| :-- | :-- | :-- |
| Return loss | $-20\log_{10}\vert\Gamma\vert$ | $10$ dB |
| $\vert S_{11}\vert$ in dB | $20\log_{10}\vert\Gamma\vert$ | $-10$ dB |
| VSWR | $(1+\vert\Gamma\vert)/(1-\vert\Gamma\vert)$ | $1.92$ |
| Power reflected | $\vert\Gamma\vert^2$ | $10\%$ |

And the one that matters for design:

$$Z_L = Z_0\ \frac{1+\Gamma}{1-\Gamma}, \qquad Z_0 = 50\ \Omega$$

Note:
The right column is the -10 dB spec written four ways. Make them say out loud: -10 dB means 10% of the power comes back, 90% goes in.

---

## Uncorrected data is not the antenna.

Before calibration the VNA sees your antenna *through* its own hardware:

- **Directivity** — the coupler leaks a little forward wave into the reflected port. The VNA sees a reflection from a perfect load.
- **Source match** — the port is not exactly $50\ \Omega$, so energy the antenna returns gets re-reflected back at it.
- **Tracking** — the two receiver paths have different gain and phase versus frequency.

<div class="callout">
Three error terms require <strong>three</strong> known standards.
</div>

Note:
One sentence each is enough at this level. Do not open the 12-term model. If someone asks, tell them it is a 2-port generalization of exactly this idea.

---

## Short–open–load, and where zero is

| Standard | Known $\Gamma$ | Pins down |
| :-- | :-- | :-- |
| Short | $-1$ | phase reference |
| Open | $+1$ | the other phase extreme |
| Load | $0$ | the leakage floor |

Three measurements, three unknowns, solved at every frequency point.

<div class="callout">
Calibration does not make the instrument better. It <strong>teaches it where zero is</strong> — and zero is wherever you put the standards.
</div>

Note:
The callout is the point of the slide, and it sets up the reference plane on the next one. Three error terms, so three standards: directivity, source match, tracking.

---

## How far does a pigtail rotate the trace?

A wave travels the extra length **twice** — out and back. So the phase error is

$$\Delta\phi = 2\beta \ell = 2\ (360^\circ)\ \frac{\ell}{\lambda_g}, \qquad \lambda_g = \frac{c\ v_f}{f}$$

10 cm of RG-58 ($v_f = 0.66$) at 915 MHz: $\lambda_g = 21.6$ cm, so $\ell = 0.46\lambda_g$ and $\Delta\phi = 333^\circ$.

<div class="callout">
That is almost a full turn: $\vert S_{11}\vert$ is untouched, but the impedance reading is <strong>meaningless</strong>.
</div>

Note:
Point out the trap: the dB plot still looks correct, so the Z readout looks trustworthy. Half a guided wavelength repeats the impedance exactly - here that is 990 MHz.

---

## Reading the sweep

<p class="viz-cue">↗ Interactive on the lesson page</p>

- **Dip** = a resonance. **Depth** = how well matched — not how well it radiates.
- **Width at $-10$ dB** = the usable impedance bandwidth.
- Same event on the chart: the locus crosses the **real axis** and dives inside the $-10$ dB circle.

<div class="fig" data-inline-svg="./fig/L10-three-views.svg" style="max-width:790px; margin:0.2em auto 0;"></div>

Note:
Demo the widget live: sweep R away from 50 and watch the dip get shallow while the resonant frequency does not move. Then raise Q and watch the band pinch shut.

---

## Smith chart, three reading skills

You met the chart in ECE 343. You do not have to build one today — you have to **read** one.

- **Crosses the real axis** → reactance is zero → resonance. Left of center means $R < 50\ \Omega$, right means $R > 50\ \Omega$.
- **Inside the small circle** → $\vert\Gamma\vert < 0.316$ → you are under $-10$ dB.
- **A loop** → two resonances close together, or a resonance plus a feed structure.
- **The whole trace spins** → your reference plane moved, not your antenna.

Note:
The last bullet is the diagnostic. If a student's trace rotates much further than the antenna alone would explain, ask what is between the cal plane and the antenna.

---

## What $S_{11}$ cannot tell you

<div class="callout">
A $50\ \Omega$ resistor has $S_{11} \rightarrow -\infty$ dB, VSWR $= 1.00$, and radiates <strong>nothing</strong>.
</div>

$S_{11}$ measures **mismatch only**. The VNA cannot tell the difference between

- power that left as radiation, and
- power that died as heat in a lossy conductor, a resistive load, or damp packaging material.

Efficiency needs a second measurement — a gain comparison or a Wheeler cap. Neither is available today, and neither comes from a one-port measurement.

Note:
This slide addresses the assumption that a deep S11 implies a good antenna. A lossy or poorly built antenna can measure very well on a VNA.

---

## The environment is part of your antenna

| Perturbation | What moves | Why |
| :-- | :-- | :-- |
| Hand near the element | $f_0$ down, dip shallower | body loading adds C and loss |
| Flat on the bench | $f_0$ shifts, loop appears | metal bench acts as a ground plane |
| Near a wall or monitor | small wiggles in the dip | re-radiated energy returns to the port |

<div class="callout">
Near-field coupling changes the antenna itself. If it changed the reading, it was <strong>inside</strong> the near field.
</div>

Note:
Tie back to L5: the reactive near field is where energy is stored, not radiated. Anything you put in it becomes part of the antenna.

---

## How much of a pattern is real

Your receiver has a noise floor, and measured power is the true signal **plus** that floor, added in power.

- **Dynamic range** = peak level minus measured floor. It bounds every number you extract.
- **Beamwidth** is measured 3 dB down, far above any practical floor. Trust it first.
- **Sidelobes** are conditional; quote the floor beside every one.
- **Nulls** measure your floor, not the antenna.

<div class="callout">
"At least 25 dB deep, limited by our 42 dB dynamic range" is defensible. "25 dB deep" is not.
</div>

Note:
Same argument as the −40 dB stray-field table, arriving from the other direction: there an unwanted signal set the floor, here the receiver does. L11 has them measure their own floor with the source off, then say row by row which numbers clear it.

---

## Key point

<div class="callout">
<p>Both instruments measure the setup as well as the antenna.</p>
<p>The range fakes a plane wave to a stated tolerance — 22.5° of phase, 0.25 dB of taper, a quiet zone at −45 dB — and gain comes from differencing against a calibrated standard. The analyzer reports one ratio, referenced to wherever you put the standards. Every number you report is only as good as the tolerance behind it.</p>
</div>

---

## Where this is going

- **L10** puts an antenna on the analyzer: calibrate, verify, sweep, read the match.
- **L11** puts one on the positioner: cut two planes, extract gain and beamwidth.
- Both are procedure. The reasons are all here, so bring this lesson to the bench.
- The **midterm project, due L20**, is the same work with no procedure handed to you. Range length, quiet zone, and horn calibration are your **error budget**.

Note:
Send them out knowing that "I measured it" is not an engineering result, while "I measured it, and here is what the range could and could not tell me" is. Remind them the project is announced today and the labs are the dress rehearsal.
