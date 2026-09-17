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

## Two measurements, one question

We measure an antenna two ways, and today is the theory behind both.

- **The pattern** — what it radiates in every direction. Measured on a **range**, in L11.
- **The terminals** — how much of the power we deliver gets in. Measured as **$S_{11}$ on a VNA**, in L10.

Plan for the period: 1-4 are the range, 5 is the analyzer.

1. What a valid pattern measurement demands: a plane wave across the antenna under test.
2. Turning that demand into a range length, and what a short range costs us.
3. Range types, chambers, compact ranges, and near-field scanning.
4. Gain by comparison, pattern cuts, polarization, and dynamic range.
5. **The analyzer**: what a VNA measures, calibration, and the reference plane.

Note:
Say out loud that items 1-4 are L11's lesson and item 5 is L10's. They are together today because they are the same question asked at two ports: how much of what an instrument reports is the antenna, and how much is the setup around it. Make the two-measurement split explicit here; they will otherwise wonder halfway through the second half why we are suddenly talking about connectors.

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

## Four ways to make the plane wave

<div class="fig" data-inline-svg="./fig/L09-range-types.svg" style="max-width:1100px; margin:0 auto;"></div>

| Range | How it makes the plane wave | Watch out for |
| :-- | :-- | :-- |
| Outdoor / elevated | Brute-force distance | Weather, ground bounce, no security |
| Anechoic chamber | Distance plus absorber | Room must still be long enough |
| Compact range | A reflector collimates up close | Edge diffraction, feed spillover |
| Near-field scanner | Measure close, transform out | Needs phase, needs a good probe |

Note:
The first three are far-field ranges: they physically deliver the wave to the antenna. The fourth changes the question. Walk the four panels left to right before the table; the table is the summary, the pictures are the explanation.

---

## Which range, and when?

| Choose | When | What it takes |
| :-- | :-- | :-- |
| **Outdoor** | The antenna is too big for any room you can afford | Good weather, a hillside or two towers |
| **Anechoic** | $2D^2/\lambda$ fits indoors — most work | Absorber, shielding, and the room |
| **Compact** | It does not fit, and the antenna is directive | A precision reflector twice the quiet zone |
| **Near-field** | Nulls and low sidelobes have to be right | Phase stability, a characterized probe, time |

<div class="callout">
Compute $2D^2/\lambda$ first. A far-field range <strong>fills nulls in</strong>, so a $-40$ dB sidelobe is near-field work whatever the room.
</div>

Note:
The decision tree is one number deep: work out 2D^2/lambda and see whether it fits a room. If it does, chamber. If it does not, compact range for a directive antenna with a small quiet-zone requirement, near-field scan for anything else and for any low-sidelobe work. Outdoors is what you do when the antenna is simply too large, and you accept the weather and the lack of security for it.

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

## Stray reflections and sidelobe error

<div class="fig" data-inline-svg="./fig/L09-stray-ripple.svg" style="max-width:730px; margin:0 auto;"></div>

The absorber spec refers to the **main beam**. A $-40$ dB stray is only **10 dB** below a $-30$ dB sidelobe, and it arrives at whatever phase the room gives it.

<div class="callout">
A chamber that meets a good $-40$ dB spec still leaves a $-30$ dB sidelobe reading anywhere from <strong>2.4 dB high to 3.3 dB low</strong>.
</div>

Note:
The two numbers are the two extremes of one interval, not two separate errors. The stray adds to the wanted signal either in phase or against it, giving a + s and a - s, and the decibel is a logarithm so the two are not symmetric: the same amplitude ripple is always worth more decibels going down than going up. Work the -30 dB row out loud: the wanted amplitude is 0.0316, the stray is 0.01, so the reading runs from 0.0416 to 0.0216, which is +2.4 and -3.3 dB. The chamber spec you need is set by the lowest level you intend to believe, not by the main beam.

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

## Three rules for a near-field scan

- **Phase is not optional.** Magnitude alone does not determine the transform.
- **Sample at $\lambda/2$ or finer**, or the transform aliases into lobes the antenna does not have.
- **Stand off 3 to 5 $\lambda$**, and scan a plane wider than the aperture.

How far out is far enough? The extent of the plane sets the angle you actually measure:

$$\theta_\text{max} = \arctan\frac{(L - D)/2}{d} \qquad L \text{ scan length}, \ D \text{ aperture}, \ d \text{ standoff}$$

<div class="callout">
Outside $\theta_\text{max}$ the pattern is <strong>truncated, not measured</strong>. A planar scan is quoted with a valid angle beside it.
</div>

Note:
Three rules, all for the scan itself. The standoff is 3 to 5 wavelengths because that is far enough for the evanescent near field to have died and for the probe not to load the antenna, and close enough that the plane stays a sensible size. The extent is the one with the formula: energy leaving the aperture edge at angle theta lands d tan theta further out, so a plane of length L captures everything inside theta max and nothing outside it. Worked number: a 0.6 m aperture at 0.15 m standoff with a 1.5 m plane gives 71.6 degrees; halve the plane and it falls to 53.1. This is also why a planar scan says nothing whatever about back lobes.

---

## Gain by comparison

Gain is a ratio, so measure it as one. Put the AUT on the positioner, record the received power. Swap in a **standard gain horn** with a calibrated gain curve, change nothing else, record again:

$$G_\text{AUT} = G_\text{SGH} + \left( P_\text{AUT} - P_\text{SGH} \right) \quad \text{(all in dB)}$$

Transmit power, source gain, range, and cable loss are **identical in both measurements**, so they subtract out. Anything that *changes* between them does not.

<div class="callout">
The horn is the <strong>largest term</strong> in the answer. Its calibration certificate, good to about $\pm 0.3$ dB, sets the uncertainty on $G_\text{AUT}$ directly.
</div>

Note:
Also called gain transfer. Be precise about what cancels: not "everything we do not know", but the terms that are the same number in both measurements. A cable bumped during the swap, a mount that does not put the two antennas in the same place, a polarization alignment redone by eye - each of those is a real gain error that survives the subtraction. Conditions on validity: same position, same polarization, same frequency, and both antennas well matched or the mismatch corrected. And if no calibrated horn exists, the three-antenna method measures absolute gain from scratch, which is how the certificate was produced in the first place.

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

- **Great-circle cut** — hold $\phi$, sweep $\theta$. The **E-plane** contains boresight and the antenna's **polarization**; the **H-plane** is perpendicular to it.
- Run every cut twice: source aligned is **co-pol**, source rotated 90° is **cross-pol**. A good linear antenna sits 20–30 dB down on boresight.
- **Circular polarization has no E-plane.** Cut two orthogonal planes and quote **axial ratio** instead.

Note:
The principal planes are named for the antenna's polarization, not for anything about the range: E-plane is the plane through boresight containing E, which for a vertical dipole is any vertical plane through the wire. That definition needs the antenna to have one polarization direction, so it means nothing for a circularly polarized antenna - there the field rotates once per RF cycle and there is no plane holding E. Use the phi = 0 and phi = 90 cuts and quote axial ratio against angle. Spinning linear is the fast way to get it: spin the source while sweeping, and the peak-to-trough ripple in dB is the axial ratio from L3. Two principal cuts describe a well-behaved pencil beam and say nothing about the diagonal planes, where the sidelobes of a rectangular aperture often sit.

---

## How much of a pattern is real

<div class="fig" data-inline-svg="./fig/L09-dynamic-range.svg" style="max-width:660px; margin:0 auto;"></div>

- **Dynamic range** = measured peak minus measured noise floor. Here, **42 dB**.
- **Beamwidth** is 3 dB down and **nulls read the floor**, not the antenna.

<div class="callout">
"At least 25 dB deep, limited by our 42 dB dynamic range" is defensible. "25 dB deep" is not.
</div>

Note:
This closes the pattern half of the lesson, and it is the same argument as the stray-reflection slide arriving from the other direction: there an unwanted signal set the floor, here the receiver does, and in a real chamber the higher of the two wins. Read the figure left to right. The main beam, the half-power points and the 13 dB sidelobe all sit 29 dB or more clear of the floor, so none of them is in question. A true null goes to minus infinity and the floor does not, so the measured trace simply flattens onto the floor - the depth read at a null is the depth of the receiver. "Limited by our 42 dB dynamic range" means the measurement cannot resolve anything more than 42 dB below the peak, so numbers from that region are bounds, not values. L11 has them measure their own floor with the source off, then say row by row which numbers clear it.

---

## A VNA is a ratio meter

- A source sweeps frequency. **Directional couplers** split off the wave going out and the wave coming back.
- Two receivers measure both, in magnitude *and* phase — the instrument reports their **ratio**.
- It never measures impedance. It measures a reflection and computes everything else from it.

<div class="fig" data-inline-svg="./fig/L10-vna-block.svg" style="max-width:830px; margin:0.2em auto 0;"></div>

Note:
Stress "ratioed": because both waves ride the same source, source drift cancels in the ratio. That is why a pocket-sized NanoVNA can be trusted for this measurement.

---

## An antenna is a one-port device

An antenna has **one connector**, so the block diagram has **one port**. Call the wave leaving it $a_1$ and the wave returning $b_1$:

$$S_{11} = \frac{b_1}{a_1} = \Gamma \quad \text{(magnitude and phase)}$$

Both subscripts are 1: out of port 1, back into port 1. **There is no port 2 in this measurement.**

<div class="callout">
One port, one complex number per frequency. Everything the VNA tells you today is a re-dress of <strong>that</strong>.
</div>

Note:
Head off the double-subscript question before it is asked. S_mn is the general scattering-parameter convention - the wave leaving port m for a wave incident on port n - and with a single port the only entry that exists is S11. Two-port work, S21 and insertion loss and a through standard, belongs to a filter or an amplifier, and to the pair of antennas on the range in L11. Not to the antenna on the bench in L10. Emphasize complex: students who remember only |S11| will misread the Smith chart later.

---

## Four names for the same number

| Quantity | From $\Gamma$ | At $\vert\Gamma\vert = 0.316$ |
| :-- | :-- | :-- |
| $\vert S_{11}\vert$ (dB) | $20\log_{10}\vert\Gamma\vert$ | $-10.0$ |
| Return loss (dB) | $-20\log_{10}\vert\Gamma\vert$ | $10.0$ |
| VSWR (ratio) | $(1+\vert\Gamma\vert)/(1-\vert\Gamma\vert)$ | $1.92$ |
| Power reflected (%) | $100\vert\Gamma\vert^2$ | $10$ |

<div class="callout">
All four re-dress one complex number. At the $-10$ dB spec, $10\%$ of the power comes back and <strong>$90\%$ reaches the antenna</strong>.
</div>

Note:
Watch the units down the column, because they are not the same: the first two rows are decibels and differ only in sign, the third is a dimensionless ratio, and the fourth is a percentage of power. Say the last row out loud - |Gamma| is an amplitude ratio, so the power fraction is |Gamma| squared, and 0.316 squared is 0.10. That is where the -10 dB convention comes from: 90% of the power we deliver reaches the antenna, and the rest stops being worth chasing.

---

## Impedance from the ratio

$$Z_L = Z_0\ \frac{1+\Gamma}{1-\Gamma}, \qquad Z_0 = 50\ \Omega$$

A marker reads $\Gamma = 0.28\ \angle{-140^\circ}$, so $Z_L = 30.6 - j11.9\ \Omega$:

- $\vert\Gamma\vert = 0.28$ is $-11.1$ dB — it **clears the $-10$ dB spec**.
- $R = 31\ \Omega$, against the $\approx 70\ \Omega$ a resonant dipole shows.
- $X = -12\ \Omega$ is **capacitive**, so the element is electrically short.

<div class="callout">
A dipole is capacitive <strong>below</strong> resonance. $X &lt; 0$ means resonance sits above this frequency: <strong>trim it longer</strong>.
</div>

Note:
Gamma and Z carry the same information; the analyzer measures Gamma and displays Z. Gamma tells you whether the antenna is acceptable, Z tells you what to do about it. Work the three lines in order at the board. The low resistance says power is going somewhere other than radiation - a lossy balun, a nearby conductor, a poor ground. The sign of the reactance is the actionable part, and that inference is most of what L10 asks them to do at the bench.

---

## Calibration: three error terms

Before **calibration** the VNA sees your antenna *through* its own hardware, and reports the pair:

- **Directivity** — the coupler leaks a little forward wave into the reflected port. The VNA sees a reflection from a perfect load.
- **Source match** — the port is not exactly $50\ \Omega$, so energy the antenna returns gets re-reflected back at it.
- **Tracking** — the two receiver paths have different gain and phase versus frequency.

<div class="callout">
Three error terms require <strong>three</strong> known standards. That is all a <strong>calibration</strong> is.
</div>

Note:
One sentence each is enough at this level. Do not open the 12-term model. If someone asks, tell them it is a 2-port generalization of exactly this idea. Say the word calibration several times on this slide and the next - this pair is the first thing they will do at the instrument in L10, and it needs to be labeled as such.

---

## Short–open–load calibration, and where zero is

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

A lossless line multiplies the wave by $e^{-j\beta\ell}$ going out and again coming back, so

$$\Gamma_\text{measured} = \Gamma_\text{antenna}\ e^{-j2\beta\ell}, \qquad \Delta\phi = 2\beta\ell = 2\ (360^\circ)\ \frac{\ell}{\lambda_g}, \qquad \lambda_g = \frac{c\ v_f}{f}$$

10 cm of RG-58 ($v_f = 0.66$) at 915 MHz: $\lambda_g = 21.6$ cm, so $\ell = 0.46\lambda_g$ and $\Delta\phi = 333^\circ$.

<div class="callout">
That exponential has <strong>magnitude 1</strong>. $\vert S_{11}\vert$ is untouched, so the dB plot looks right while the impedance reading is <strong>meaningless</strong>.
</div>

Note:
Point out the trap: the dB plot still looks correct, so the Z readout looks trustworthy. Half a guided wavelength repeats the impedance exactly - here that is 990 MHz, where 2 beta l is a full 720 degrees - and that is why "it looked fine at one marker" is not a check.

---

## Two fixes, and what each one can do

$$\Gamma_\text{antenna} = \Gamma_\text{measured}\ e^{+j2\beta\ell}$$

- **Fix 1 — calibrate *to* the antenna connector.** Put the pigtail inside the cal path, so the standards define zero at the antenna itself. Removes phase *and* loss *and* adapter mismatch.
- **Fix 2 — port extension.** Tell the instrument $\ell$, and it multiplies every point in the sweep by that exponential.

<div class="callout">
Port extension is a <strong>pure phase rotation</strong>. It cannot undo loss, and it cannot undo a real mismatch inside an adapter.
</div>

Note:
Show that fix 2 is just the inverse of the equation on the previous slide - multiply by e^{+j2 beta l} and the antenna's own Gamma comes back. That is literally what the instrument's port-extension control does, and most analyzers will find l for you from an open. The reason it is second best is in the callout: the correction has unit magnitude, so anything lossy or mismatched between the cal plane and the antenna stays in the data. When it matters, calibrate to the connector.

---

## Reading a VNA sweep

<p class="viz-cue">↗ Interactive on the lesson page</p>

- **Dip** = a resonance. **Depth** = how well matched — not how well it radiates.
- **Width at $-10$ dB** = the usable impedance bandwidth.
- Same event on the chart: the locus crosses the **real axis** and dives inside the $-10$ dB circle.

<div class="fig" data-inline-svg="./fig/L10-three-views.svg" style="max-width:790px; margin:0.2em auto 0;"></div>

Note:
Demo the widget live: sweep R away from 50 and watch the dip get shallow while the resonant frequency does not move. Then raise Q and watch the band pinch shut.

---

## Smith chart, four reading skills

You met the chart in ECE 343. You do not have to build one today — you have to **read** one.

- **Crosses the real axis** → reactance is zero → resonance. Left of center means $R < 50\ \Omega$, right means $R > 50\ \Omega$.
- **Inside the small circle** → $\vert\Gamma\vert < 0.316$ → you are under $-10$ dB.
- **A loop** → two resonances close together, or a resonance plus a feed structure.
- **The whole trace spins** → your reference plane moved, not your antenna.

<div class="fig" data-inline-svg="./fig/L09-smith-skills-row.svg" style="max-width:790px; margin:0 auto;"></div>

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

## Key point

<div class="callout">
<p>Both instruments measure the setup as well as the antenna.</p>
<p>The range fakes a plane wave to a stated tolerance — 22.5° of phase, 0.25 dB of taper, a quiet zone at −45 dB — and gain comes from differencing against a calibrated standard. The analyzer reports one ratio, referenced to wherever you put the standards. Every number you report is only as good as the tolerance behind it.</p>
</div>

---

## The midterm project

<div class="callout">
<strong>Build a dipole, measure its pattern</strong>, and report gain, beamwidth, sidelobe level, and polarization <strong>with an error budget</strong>. Due L20.
</div>

Everyone builds the same antenna, and everything since L1 lands on it: the definitions from L1–L3, the far-field boundary from L5, the radiation integral from L6, the dipole solution from L7, the model from L8, and both instruments from today.

| Error-budget line | Where it comes from |
| :-- | :-- |
| Range length | $r$ against $2D^2/\lambda$ |
| Amplitude taper | Source beamwidth against $D/r$ |
| Quiet zone | Stray field level, and whether the AUT fits inside it |
| Horn calibration | The certificate, about $\pm 0.3$ dB |
| Dynamic range | Measured peak minus measured floor |
| Polarization alignment | Angular error between source and AUT |

Note:
Say why everyone builds the same antenna: the pattern, the gain and the impedance are all predictable before anyone measures anything, so the work of the project is the comparison and the uncertainty rather than the build. Thirty measurements of one known object also makes disagreement between them worth talking about. Six error-budget lines, not three, and every one of them came out of today. The quiet zone is the one most often assumed rather than measured - check the spec, check the antenna's largest dimension against it, and say in the report which one you were working inside. Full requirements are in the handout.

---

## Where this is going

- **L10** puts an antenna on the analyzer: calibrate, verify, sweep, read the match.
- **L11** puts one on the positioner: cut two planes, extract gain and beamwidth.
- Both are procedure. The reasons are all here, so bring this lesson to the bench.
- The **midterm project, due L20**, is the same work with no procedure handed to you.

Note:
Send them out knowing that "I measured it" is not an engineering result, while "I measured it, here is what it should have been, and here is what my range could and could not tell me" is. The labs are the dress rehearsal: same antenna, same instruments, same extraction, same uncertainty discussion.
