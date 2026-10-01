<!-- .slide: class="title-slide" -->

<div class="title-left">

# ECE 444

Antennas, Phased Arrays, and Radar Systems

## Lesson 14 — High-Gain Antennas

Fall 2026 · Dr. Neil Rogers

</div>

<div class="title-right">

![USAFA](./img/01-course-intro/USAFA-logo.png)

</div>

---

## Where We Were

- L13 covered patches, slots, and horns: single elements from 6 to 20 dBi.
- L6 showed that aperture **size** sets the beamwidth and aperture **shape** sets the sidelobes.
- L2's Friis equation makes the link budget depend directly on $G_t G_r$.
- Each of those antennas is a single radiator.

**Today covers 20 to 40 dBi, and all of it follows from one idea: gain is coherent area in square wavelengths. This is the last lesson of Module 2.**

Note:
Anchor on L13. A patch on a wall is fine for Wi-Fi. Ask what closes a link to GEO at 36000 km; nobody does it with a patch.

---

## Today's Plan

1. Gain and aperture area: the aperture formula and the beamwidth rule
2. The parabolic reflector, and why the surface must be a parabola
3. Aperture efficiency losses: taper, spillover, blockage, and surface error
4. The Yagi-Uda, which gets gain from elements that are not connected
5. Arrays, the third approach and the subject of Module 3
6. Choosing an antenna and defending the choice with numbers

Note:
Introduce item 6 as the reasoning an engineer shows when the antenna choice is still open, which is most of the time.

---

## The One Idea

<div class="callout">
<p>High gain means a large radiating <strong>area</strong>, driven in <strong>phase</strong>.</p>
<p>The reflector, the Yagi, and the array are three ways to assemble the same coherent aperture.</p>
</div>

<div class="fig" data-inline-svg="./fig/L14-three-approaches.svg" style="max-width:900px; margin:0 auto;"></div>

Note:
A reflector collects area with a mirror and its geometry sets the phase; a Yagi collects it from currents induced on parasitic elements and detuning sets the phase; an array adds the area one element at a time and electronics set the phase. Have them write this down. Everything else today follows from it. If a student keeps one sentence from L14, it should be this one.

---

## Gain and Aperture Area

$$G = \eta_{\text{ap}} \frac{4\pi A}{\lambda^2} \quad\quad A_e = \eta_{\text{ap}} A = \frac{G \lambda^2}{4\pi}$$

- $A/\lambda^2$ counts **square wavelengths**, not square meters, so an aperture is large only relative to the wavelength.
- Good reflectors reach $\eta_{\text{ap}} \approx 0.55$ to $0.7$; horns reach about $0.5$.

For a circular dish of diameter $D$:

$$G = \eta_{\text{ap}} \left( \frac{\pi D}{\lambda} \right)^2$$

Doubling $D$ adds 6 dB, and doubling the frequency adds another 6 dB.

Note:
Read the physics before the algebra. Ask why satellite links keep moving up in frequency: the same dish gains 6 dB per octave with no change to the hardware. Where the formula comes from: L13 derived it for the horn. On boresight every phase factor in the radiation integral is 1, so D = (4 pi / lambda^2) |integral of E_a|^2 / integral of |E_a|^2, and that ratio divided by A is eta_ap. A uniform, in-phase field gives exactly 1; every loss term today shrinks the numerator.

---

## Beamwidth and Aperture Size

<p class="viz-cue">↗ Interactive on the lesson page</p>

$$\theta_{\text{HP}} \approx 70^\circ \frac{\lambda}{D}$$

- L6's Fourier logic applies: a wider aperture gives a narrower beam.
- Doubling $D$ adds 6 dB of gain and halves the beam, which is one statement made twice.
- The $70^\circ$ assumes a tapered illumination; a uniform aperture gives $59^\circ$.

| $D/\lambda$ | Gain at $\eta_{\text{ap}}=0.55$ | HPBW |
| :-- | :-- | :-- |
| 10 | 27.3 dBi | $7.0^\circ$ |
| 30 | 36.9 dBi | $2.3^\circ$ |
| 100 | 47.4 dBi | $0.7^\circ$ |

Note:
Where the 59 comes from: a uniform disk's radiation vector is 2 J1(u)/u, u = (pi D / lambda) sin theta, the circular counterpart of L6's sinc. Half power at u = 1.616 gives 1.029 lambda/D rad = 59 degrees, with the first sidelobe at -17.6 dB. A feed at the 10 dB rule (11 dB edge taper) widens it to 67 degrees and lowers the sidelobes to -25 dB; 70 is the round design number. Eliminating D: G theta^2 = 31,400 deg^2 at eta 0.65, inside L2's 26,000 to 32,400 pencil-beam range.

Demo the reflector-gain widget live. Sweep D/lambda from 3 to 300 so they see the beam cone narrow while the gain curve climbs. Then set the surface-error slider to lambda/16 and show the amber curve level off and fall.

---

## Uniform and Tapered Apertures

<div class="fig" data-inline-svg="./fig/L14-beam-patterns.svg" style="max-width:860px; margin:0 auto;"></div>

- The 10 dB-rule taper widens the beam from 59° to 67° times λ/D.
- It lowers the first sidelobe from −17.6 dB to −25.1 dB.

Note:
Both curves come from the same radiation integral over the disk. The tapered one uses the aperture field a cos^4 feed produces on an f/D = 0.5 dish, the 10 dB-rule feed. Point out that the taper costs beamwidth and buys sidelobe level, which is the L15 trade in its first appearance.

---

## Worked Example — 1 m Dish at 12 GHz

A home satellite-TV dish receives Ku band; take $\eta_{\text{ap}} = 0.65$.

| Quantity | Work | Result |
| :-- | :-- | :-- |
| Wavelength | $\lambda = 3\times10^8 / 12\times10^9$ | $0.025$ m, so $D/\lambda = 40$ |
| Gain | $0.65\ (40\pi)^2 = 1.03\times10^4$ | **40.1 dBi** |
| Beamwidth | $70^\circ (0.025 / 1)$ | **$1.75^\circ$** |
| Effective area | $0.65 \times \pi (0.5)^2$ | $0.51$ m² |
| Far field | $2D^2/\lambda = 2/0.025$ | 80 m |

Note:
Two points. First, a dish one person can carry gives 40 dBi. Second, its far field starts at 80 m. That is L5's 2D^2/lambda, the distance where the rim-to-center path difference falls to lambda/16, so no bench range in the lab can measure this dish, which is L9's problem.

---

## Why a Parabola

<div class="fig" data-inline-svg="./fig/L14-parabola-geometry.svg" style="max-width:940px; margin:0 auto;"></div>

Note:
Walk the ray. The feed radiates a spherical wave; the surface only rearranges its phase and adds no power. Point at the aperture plane and say that this plane is where the antenna radiates from.

---

## The Equal-Path Property

The surface is $z = \rho^2 / 4f$ with the focus at $z = f$. The distance from the focus to a surface point $P$ is $f + z_P$.

$$\overline{FP} + \overline{PA} = (f + z_P) + (z_a - z_P) = f + z_a$$

- The $z_P$ cancels, so every ray takes the same path length.
- A spherical wave goes in, and a plane wave comes out with the whole aperture in phase.
- One line of algebra is the entire reason reflectors exist.

<div class="callout">
<p>A reflector does not amplify. It <em>rearranges phase</em> over a large area.</p>
</div>

Note:
Do this cancellation on the board. It is one of the few derivations in Module 2 that fits in a single line, so let them see it happen. If asked where FP = f + z_P comes from: Pythagoras gives FP^2 = rho^2 + (z_P - f)^2, and rho^2 = 4 f z_P makes it (z_P + f)^2. Every point on a parabola is as far from the focus as from the line z = -f.

---

## f/D and the Feed

<p class="viz-cue">↗ Interactive on the lesson page</p>

$$\tan \left( \theta_0 / 2 \right) = \frac{1}{4 (f/D)}$$

| $f/D$ | Edge half-angle | Character |
| :-- | :-- | :-- |
| 0.25 | $90^\circ$ | focus in the rim plane; very deep |
| 0.35 | $71^\circ$ | deep; needs a very broad feed |
| 0.50 | $53^\circ$ | the common compromise |
| 0.60 | $45^\circ$ | shallow; directive feed on a long strut |

A deep dish shields the feed from warm ground; a shallow dish is easier to illuminate cleanly.

Note:
Demo the feed-dish widget: deepen the dish to f/D = 0.25 and show the rim angle open to 90 degrees, then narrow the feed and watch spillover fall while the taper efficiency falls with it. f/D is the first number on any reflector data sheet. It tells the feed designer how much of the sky the feed must cover. Where the formula comes from: FP = f + z_P in polar form from the focus is r = 2f / (1 + cos theta'), so rho = r sin theta' = 2f tan(theta'/2), and the rim is at rho = D/2. The same r(theta') says the rim is farther from the feed than the vertex is, which puts the rim 1.9 dB below the center at f/D = 0.5 before the feed pattern rolls off at all.

---

## Illumination Taper and Spillover

<div class="fig" data-inline-svg="./fig/L14-illumination-taper.svg" style="max-width:860px; margin:0 auto;"></div>

<div class="callout">
<p>Rule of thumb: illuminate the rim about <strong>10 dB below center</strong>.</p>
</div>

Note:
Two losses that pull opposite ways have an optimum; the next slide computes it. On receive, spillover also adds noise: the spilled beam looks at 290 K ground instead of a few kelvin of sky, which raises the antenna temperature T_A from L12 and the noise kT_A B that the dish delivers.

---

## Why 10 dB

<div class="fig" data-inline-svg="./fig/L14-taper-spillover.svg" style="max-width:860px; margin:0 auto;"></div>

- The model uses f/D = 0.5 and sweeps the feed pattern from broad to narrow.
- The product peaks at **0.82** for an **11 dB** edge taper, and anything from 8 to 14 dB is within 0.03.

Note:
The feed power pattern is cos^n theta', with n swept. Spillover efficiency is the fraction of the feed's power inside the rim angle. Taper efficiency is L13's |integral of E_a|^2 over A times integral of |E_a|^2, with E_a set by the feed pattern and the 1/r spreading. The optimum is at 10.7 dB: spillover 0.92, taper 0.89, product 0.82. The peak is broad, which is why a rule of thumb is good enough.

---

## Blockage and the Offset Feed

- A prime-focus feed and its struts sit **in the beam**.
- A blocked diameter $d$ lowers the gain by the factor below and raises the sidelobes.

$$\left[ 1 - \left( \frac{d}{D} \right)^2 \right]^2$$

- A 15 cm feed loses 0.02 dB on a 3 m dish and 1.0 dB on a 45 cm dish.
- An **offset feed** uses a slice cut off-axis from a larger paraboloid.

Note:
Most students have seen an offset dish on a roof. Connect the shape they already know to the blockage argument. Where the square comes from: in the aperture-efficiency ratio the feed still radiates the power aimed at the blocked disk, so the denominator keeps all of A, but that power does not add on boresight, so the numerator loses A_b. G/G0 = (A - A_b)^2 / A^2.

---

## Prime Focus and Offset Feed

<div class="fig" data-inline-svg="./fig/L14-offset-feed.svg" style="max-width:860px; margin:0 auto;"></div>

An offset feed gives zero blockage and lower sidelobes, and the tilted slice is why an offset dish looks taller than it is wide.

Note:
The offset reflector is a slice cut from one side of a larger parent paraboloid. It shares that paraboloid's focus, so the feed still sits at the focus, but the slice reflects the beam past it instead of through it.

---

## Surface Accuracy — Ruze

$$G = G_0\ e^{-(4 \pi \sigma / \lambda)^2} \quad\quad \text{loss (dB)} = 685.8 \left( \sigma / \lambda \right)^2$$

- $\sigma$ is the **RMS** surface error, and the loss grows exponentially with it.
- $\sigma = \lambda/50$ loses 0.27 dB, and $\sigma = \lambda/16$ loses 2.7 dB.
- The same dish at 0.5 mm RMS is essentially perfect at 6 GHz and 1.7 dB down at 30 GHz.

<div class="callout">
<p>Big dishes at short wavelengths are a <strong>machining</strong> problem, not an electromagnetics problem.</p>
</div>

Note:
The derivation is two lines if asked. A bump epsilon lengthens the path in and out by 2 epsilon, so the RMS phase error is 4 pi sigma / lambda. In the aperture-efficiency ratio the numerator now sums e^(j delta); for Gaussian errors that averages to e^(-delta_rms^2 / 2), and squaring it gives the Ruze exponential. 685.8 is 10 log10(e) times (4 pi)^2. Phase error enters as an exponential, which is why surface tolerance dominates millimeter-wave reflector design.

---

## Surface Error and Gain

<div class="fig" data-inline-svg="./fig/L14-ruze.svg" style="max-width:860px; margin:0 auto;"></div>

Note:
Left: a bump lengthens the path by twice its depth, in and back out, which is where the 4 pi sigma / lambda comes from. Right: the loss grows with the square of the RMS error, so halving the error cuts the loss by four.

---

## The Efficiency Budget

| Loss term | Typical | Why |
| :-- | :-- | :-- |
| Spillover | 0.90 | power that passes the rim |
| Illumination taper | 0.85 | rim darker than center |
| Blockage | 0.95 | feed and struts in the beam |
| Surface (Ruze) | 0.94 | phase errors across the aperture |
| Everything else | 0.97 | cross-pol, feed loss, other |

**Product: 0.66.** That product is where $\eta_{\text{ap}} \approx 0.55$ to $0.7$ comes from: spillover, taper, blockage, and surface error, each a design tradeoff.

Note:
Have them multiply it on their calculators. The 0.65 is not an arbitrary factor; it is a budget they can check line by line. Spillover and taper sit a little below the 0.92 and 0.89 of the optimum on the earlier slide because real feeds are not exactly cos^n. Cross-pol is power radiated in the orthogonal polarization, which L3 showed a matched receiver cannot collect.

---

## The Efficiency Budget, Term by Term

<div class="fig" data-inline-svg="./fig/L14-efficiency-budget.svg" style="max-width:860px; margin:0 auto;"></div>

Note:
Each bar multiplies the one before it. The two largest steps are spillover and taper, the pair the 10 dB rule trades against each other.

---

## The Yagi-Uda

<div class="fig" data-inline-svg="./fig/L14-yagi.svg" style="max-width:980px; margin:0 auto;"></div>

Note:
Exactly one element is connected. Every other element is a rod in the near field. Students often assume every element is fed, so correct that here.

---

## Parasitic Element Phasing

<p class="viz-cue">↗ Interactive on the lesson page</p>

- The **driven element**, about $0.47\lambda$ long, is the only one connected.
- The **parasites** carry current *induced* by the driven element's near field.
- A slightly **long** element is inductive, and its current **lags** its induced voltage; that is the reflector, behind.
- A slightly **short** element is capacitive, and its current **leads**; those are the directors, in front.
- The result is a slow traveling wave forward, an **endfire** beam, and 15–25 dB front-to-back.

<div class="callout">
<p>The long element lags, the short elements lead, and the beam goes toward the short end.</p>
</div>

Note:
Demo the two-element Yagi widget: at d = 0.2 lambda and alpha = 108 degrees the back sum closes to zero; move alpha and the null leaves the back. This is L6's radiation integral with several filaments instead of one. This course does not use mutual-impedance matrices; NEC solved that system in L8. The lag is L7's impedance: I = V/Z, and past resonance X is positive, so the current lags the induced V by arctan(X/R). The phase the reflector needs: with the reflector d behind, the back lobe goes as 1 + a e^(j(alpha + kd)), so it cancels at alpha = 180 - kd. At d = 0.2 lambda that is 108 degrees, and the forward sum is |1 + e^(j36)| = 1.90 of a possible 2. A slow traveling wave means the phase lag per director is slightly more than the free-space kd, a wave along the boom slower than light, which narrows the endfire beam.

---

## Yagi Gain and Boom Length

| Elements | Boom | Typical gain |
| :-- | :-- | :-- |
| 3 | $0.3\lambda$ | 7.5 dBi |
| 6 | $1.0\lambda$ | 10 dBi |
| 10 | $2.2\lambda$ | 12.5 dBi |
| 16 | $4.5\lambda$ | 14.5 dBi |

- Gain rises about **2 dB per doubling of the boom**; the endfire ideal is 3 dB.
- More directors on the *same* boom add almost nothing.
- Practical Yagis reach 8–15 dBi, with a bandwidth of a few percent.
- They suit TV, amateur, and fixed point-to-point links, where the frequency does not change.

Note:
A Yagi needs only one reflector; a second sees almost no field. Above 15 dBi, designers stack Yagis and the stack becomes an array. Why the boom sets the gain: L6's line source turned on its end. A current phased to travel forward gives a sinc in u = (kL/2)(cos theta - 1), about -(pi L / 2 lambda) theta^2, so the half-power angle squared goes as lambda/L. The beam is a cone that narrow in every plane, its solid angle goes as lambda/L, and D goes as L: 4L/lambda in step, toward 7L/lambda with a slow wave. That is 3 dB per doubling. The table shows about 1.8: short Yagis beat the estimate because their elements are dipoles with gain, and long ones fall behind because the current dies away on the far directors.

---

## Yagi Gain Against the Endfire Lines

<div class="fig" data-inline-svg="./fig/L14-yagi-boom.svg" style="max-width:860px; margin:0 auto;"></div>

Note:
The points are the table on the previous slide. The two lines are the endfire line source in step (4L/lambda) and with a slow wave (7L/lambda); both climb 3 dB per doubling. Real Yagis sit between them and climb about 1.8.

---

## Arrays

$$G_{\text{array}} = 10 \log_{10} N \quad \text{dB over one element}$$

- Sixteen elements add 12 dB, and sixty-four add 18 dB.
- The gain grows only if the **aperture grows** with $N$; elements cannot share the same area.
- The beam is not fixed to the structure: changing the element phases moves the beam.
- The beam moves in microseconds with no moving parts, which is why modern radars and 5G base stations use arrays.

<div class="callout">
<p>That is <strong>Module 3</strong>: array factor, pattern multiplication, steering, grating lobes, tapering — and a real beam on the ADALM-PHASER.</p>
</div>

Note:
Introduce Module 3 here; the PHASER hardware is what they will use in the labs. Why 10 log N: on boresight N in-phase elements sum to N times one element's radiation vector, so U_max goes as N^2. Radiated power goes as N only if the elements are about lambda/2 apart and do not share aperture. N^2 over N is N. A lambda/2 grid of N elements has area N lambda^2/4, so the one idea gives the same result.

---

## Steering an Array

<div class="fig" data-inline-svg="./fig/L13-patch-array.svg" style="max-width:860px; margin:0 auto;"></div>

Note:
This is the L13 figure: one patch and its broad, fixed beam, beside eight patches on a half-wavelength grid, each behind a phase shifter, steering a narrow beam 20 degrees. The steering is Module 3.

---

## Choosing: Five Questions

1. **How much gain does the link budget require?** Run it first.
2. **What frequency?** Apertures shrink with $\lambda$, and wires get fragile.
3. **How much bandwidth?** Reflectors are wideband, and Yagis are narrowband.
4. **Does it steer?** The options are mechanical, fixed, or electronic.
5. **What are the cost, size, weight, and wind load?** A 20 dBi antenna that cannot survive local wind and ice loading is not a usable answer.

Note:
Order matters. Students tend to start at question 5 and work backward; have them start at question 1.

---

## Three Approaches Compared

| | Reflector | Yagi-Uda | Planar array |
| :-- | :-- | :-- | :-- |
| Practical gain | 25–60 dBi | 8–15 dBi | 15–40 dBi |
| Bandwidth | wide | a few % | moderate |
| Steering | mechanical, slow | fixed | electronic, instant |
| Profile | bulky, 3-D | long boom | flat panel |
| Cost driver | surface accuracy | almost nothing | a chain per element |

Note:
Practicing engineers argue most about the cost row. An array gives the best electrical performance and carries the highest cost.

---

## Worked Selection — 20 dBi at 2.4 GHz

For a cubesat ground station, $\lambda = 0.125$ m and $G = 20$ dBi $= 100$, so $A_e = G \lambda^2 / 4\pi = 0.124$ m².

| Candidate | Work | Result |
| :-- | :-- | :-- |
| Dish | $A = 0.124/0.6$, $\ D = 2\sqrt{A/\pi}$ | **0.51 m**, HPBW $17^\circ$ |
| Yagi | 14.5 dBi each, four stacked: $+10\log_{10}4$ | 20.5 dBi, four 0.56 m booms |
| Patch array | $7 \times 7$ at $\lambda/2$, 0.44 m square | 20.6 dBi, 49-way feed |

**Take the dish:** it has the fewest parts, the widest band, and the lowest cost. Take the array when the design needs a flat profile or electronic steering.

Note:
Every candidate has to deliver the same 0.124 square meters of coherent area, and that single number drives the whole comparison.

---

## Does the Link Close?

A cubesat at 1000 km sends 2 W (33.0 dBm) from a 0 dBi antenna to our 20 dBi dish on the ground. The path loss is L2's Friis factor in decibels.

$$L_{\text{fs}} = 20 \log_{10} \left( 4 \pi R / \lambda \right) = 20 \log_{10} \left( 4 \pi \times 10^6 / 0.125 \right) = 160.0 \text{ dB}$$

$$P_r = 33.0 + 0 + 20 - 160.0 = -107.0 \text{ dBm}$$

- The noise floor is $kT_0 B$ plus a 3 dB noise figure in 100 kHz: $-174 + 50 + 3 = -121$ dBm.
- **Margin: 14 dB.** With a 0 dBi antenna in place of the dish, the signal sits 6 dB *under* the noise.

Note:
This is the key result. The 20 dB of antenna gain is the difference between a working downlink and no downlink. The -174 dBm/Hz is kT at the 290 K reference, L12's kT_A B with T_A = T_0. A dish looking at cold sky sees less, so the floor is conservative.

---

## The Link as a Level Diagram

<div class="fig" data-inline-svg="./fig/L14-link-budget.svg" style="max-width:860px; margin:0 auto;"></div>

Note:
Read it left to right: 33.0 dBm out of the transmitter, 160.0 dB of path loss, 20 dB back from the dish, landing 14 dB above the noise floor. The gray dash is the same link with a 0 dBi antenna on the ground: 6 dB under the noise.

---

## Key Point

<div class="callout">
<p><strong>Gain</strong> is coherent area, counted in square wavelengths.</p>
<p>A reflector rearranges phase with a mirror. A Yagi uses currents induced on its parasitic elements. An array adds the area element by element. All three approaches build the same coherent aperture.</p>
</div>

Note:
Close the loop on the opening slide. If they leave with one sentence, it should be this one.

---

## Where This Is Going

- Every gain number today was a **claim**: 0.65 was an assumption, and $70^\circ \lambda / D$ was a rule of thumb.
- We already know how to test a claim: L9's theory, L10's analyzer, and L11's range.
- **Module 2 closes here:** predict, simulate, measure, and state how much to believe.
- **L15 opens Module 3:** aperture size set the beamwidth, so what sets the sidelobe level?

**A gain figure belongs on a data sheet only after someone has measured it, and you now know how.**

Note:
Tie the 80 m far-field number from the worked example back to L9's compact range and near-field scanner: one person can carry this dish, and no ordinary room can test it. Then point them to L15: the answer to the sidelobe question is the illumination taper they met today at −10 dB, generalized.
