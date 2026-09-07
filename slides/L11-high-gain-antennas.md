<!-- .slide: class="title-slide" -->

<div class="title-left">

# ECE 444

Antennas, Phased Arrays, and Radar Systems

## Lesson 11 — High-Gain Antennas

Fall 2026 · Dr. Neil Rogers

</div>

<div class="title-right">

![USAFA](./img/01-course-intro/USAFA-logo.png)

</div>

---

## Where we were

- L10: patches, slots, horns — single elements, 6 to 20 dBi
- L6: beamwidth is set by aperture **size**, sidelobes by aperture **shape**
- L2: Friis says the link budget lives or dies on $G_t G_r$
- Every one of those antennas is one radiator

**Today: how you get to 20, 30, 40 dBi — and the one idea behind all of it.**

Note:
Anchor on L10. Patch on a wall is fine for Wi-Fi. Ask: what closes a link to GEO at 36000 km? Nobody does it with a patch.

---

## Today's plan

1. Gain is area — the aperture formula and the beamwidth rule
2. The parabolic reflector: why a parabola, and only a parabola
3. Where the efficiency goes: taper, spillover, blockage, surface
4. The Yagi-Uda: gain from elements you never connect
5. Arrays — the third road, and the whole of Module 3
6. Choosing one, and defending it with numbers

Note:
Flag the midterm project up front — it is announced at the end of the hour and it is due at L20.

---

## The one idea

<div class="callout">
<p><strong>High gain = a large radiating area, driven in phase.</strong></p>
<p>The reflector, the Yagi, and the array are three ways to assemble the same coherent aperture.</p>
</div>

| Antenna | How it builds the area |
| :-- | :-- |
| Reflector | borrows a mirror's area, phase fixed by geometry |
| Yagi-Uda | borrows the neighbors' currents, phase fixed by detuning |
| Array | buys the area one element at a time, phase set electronically |

Note:
Make them write this down. Everything else today is a corollary. If a student can only keep one sentence from L11, this is it.

---

## Gain is area

$$G = \eta_{\text{ap}} \frac{4\pi A}{\lambda^2} \quad\quad A_e = \eta_{\text{ap}} A = \frac{G \lambda^2}{4\pi}$$

- $A/\lambda^2$ counts **square wavelengths**, not square meters
- An aperture is never simply *big* — it is big **at a frequency**
- Circular dish of diameter $D$: $\quad G = \eta_{\text{ap}} \left( \pi D / \lambda \right)^2$
- Good reflectors: $\eta_{\text{ap}} \approx 0.55$ to $0.7$; horns $\approx 0.5$

<div class="callout">
<p><strong>Doubling D adds 6 dB</strong>, and doubling the frequency adds another 6 dB.</p>
</div>

Note:
Read the physics before the algebra. Ask why satcom keeps climbing in frequency — the same dish gains 6 dB per octave for free.

---

## Beamwidth comes from the same size

<p class="viz-cue">↗ Interactive on the lesson page</p>

$$\theta_{\text{HP}} \approx 70^\circ \frac{\lambda}{D}$$

- Same Fourier logic as L6: wide aperture, narrow beam
- Double $D$: gain **+6 dB**, beam **halved** — the same statement twice
- The $70^\circ$ already assumes a tapered illumination (uniform gives $58^\circ$)

| $D/\lambda$ | Gain at $\eta_{\text{ap}}=0.55$ | HPBW |
| :-- | :-- | :-- |
| 10 | 27.3 dBi | $7.0^\circ$ |
| 30 | 36.9 dBi | $2.3^\circ$ |
| 100 | 47.4 dBi | $0.7^\circ$ |

Note:
Demo the reflector-gain widget live. Sweep D/lambda from 3 to 300 and let them watch the beam cone collapse while the gain curve climbs. Then push the surface-error slider to lambda/16 and show the amber ceiling roll over.

---

## Worked example — 1 m dish at 12 GHz

Home satellite-TV dish, Ku band, $\eta_{\text{ap}} = 0.65$.

| Quantity | Work | Result |
| :-- | :-- | :-- |
| Wavelength | $\lambda = 3\times10^8 / 12\times10^9$ | $0.025$ m, so $D/\lambda = 40$ |
| Gain | $0.65\ (40\pi)^2 = 1.03\times10^4$ | **40.1 dBi** |
| Beamwidth | $70^\circ (0.025 / 1)$ | **$1.75^\circ$** |
| Effective area | $0.65 \times \pi (0.5)^2$ | $0.51$ m² |
| Far field | $2D^2/\lambda = 2/0.025$ | 80 m |

Note:
Two takeaways. First: a dish you can carry gives 40 dBi. Second: its far field is 80 m — you cannot measure this thing in the lab, which is exactly L12's problem.

---

## Why a parabola

<div class="fig" data-inline-svg="./fig/L11-parabola-geometry.svg" style="max-width:940px; margin:0 auto;"></div>

Note:
Walk the ray. Feed radiates a sphere; the surface only rearranges phase, never adds power. Point at the aperture plane and say: this is where the antenna actually is.

---

## The equal-path property

Surface $z = \rho^2 / 4f$, focus at $z = f$. Distance from focus to a surface point $P$ is $f + z_P$.

$$\overline{FP} + \overline{PA} = (f + z_P) + (z_a - z_P) = f + z_a$$

- $z_P$ cancels — **every ray takes the same path length**
- Spherical wave in, plane wave out, whole aperture in phase
- One line of algebra is the entire reason reflectors exist

<div class="callout">
<p>A reflector does not amplify. It <em>rearranges phase</em> over a large area.</p>
</div>

Note:
Do this cancellation on the board. It is one of the few derivations in Module 2 that fits in a single line, so make them see it happen.

---

## f/D sets the feed's job

$$\tan \left( \theta_0 / 2 \right) = \frac{1}{4 (f/D)}$$

| $f/D$ | Edge half-angle | Character |
| :-- | :-- | :-- |
| 0.25 | $90^\circ$ | focus in the rim plane — very deep |
| 0.35 | $71^\circ$ | deep; needs a very broad feed |
| 0.50 | $53^\circ$ | the common compromise |
| 0.60 | $45^\circ$ | shallow; directive feed on a long strut |

Deep dish shields the feed from warm ground; shallow dish is easier to illuminate cleanly.

Note:
f/D is the first number on any reflector data sheet. It tells the feed designer the only thing he needs: how much sky to cover.

---

## Illumination: taper fights spillover

<div class="fig" data-inline-svg="./fig/L11-illumination-taper.svg" style="max-width:860px; margin:0 auto;"></div>

<div class="callout">
<p>Rule of thumb: illuminate the rim about <strong>10 dB below center</strong>.</p>
</div>

Note:
Two losses pulling opposite ways means there is an optimum, and the answer has been 10 dB since the 1950s. On receive, spillover is worse than it looks — that beam is staring at 290 K ground instead of 5 K sky.

---

## Blockage, and why your dish is oval

- Prime-focus feed and struts sit **in the beam**
- A blocked diameter $d$ costs roughly $\left[ 1 - (d/D)^2 \right]^2$ in gain, and raises sidelobes
- 15 cm feed on a 3 m dish: negligible. On a 45 cm dish: a measurable loss.
- **Offset feed** — cut the reflector as a slice off-axis from a bigger paraboloid

<div class="callout">
<p>An offset feed gives zero blockage and cleaner sidelobes, and the tilted slice is why an offset dish looks taller than it is wide.</p>
</div>

Note:
Most students have seen an offset dish on a roof. Connect the shape they already know to the blockage argument.

---

## Surface accuracy — Ruze

$$G = G_0\ e^{-(4 \pi \sigma / \lambda)^2} \quad\quad \text{loss (dB)} = 685.8 \left( \sigma / \lambda \right)^2$$

- $\sigma$ = **RMS** surface error. Exponential, not linear.
- $\sigma = \lambda/50 \rightarrow 0.27$ dB. $\quad \sigma = \lambda/16 \rightarrow 2.7$ dB.
- Same dish, 0.5 mm RMS: perfect at 6 GHz, **1.7 dB down** at 30 GHz

<div class="callout">
<p>Big dishes at short wavelengths are a <strong>machining</strong> problem, not an electromagnetics problem.</p>
</div>

Note:
Do not derive it. Note that phase error enters as an exponential, which is why surface tolerance dominates millimetre-wave reflector design.

---

## The efficiency budget

| Loss term | Typical | Why |
| :-- | :-- | :-- |
| Spillover | 0.90 | power sails past the rim |
| Illumination taper | 0.85 | rim darker than center |
| Blockage | 0.95 | feed and struts in the beam |
| Surface (Ruze) | 0.94 | phase errors across the aperture |
| Everything else | 0.97 | cross-pol, feed loss, misc. |

**Product: 0.66.** That is where $\eta_{\text{ap}} \approx 0.55$ to $0.7$ comes from — four unavoidable trades, not sloppiness.

Note:
Have them multiply it on their calculators. The point is that 0.65 is not a fudge factor someone made up; it is a budget you can audit line by line.

---

## The Yagi-Uda

<div class="fig" data-inline-svg="./fig/L11-yagi.svg" style="max-width:980px; margin:0 auto;"></div>

Note:
Exactly one element is connected. Everything else is a piece of metal in the near field. Students often assume every element is fed, so correct that here.

---

## Detuning sets the phase

- **Driven element** $\approx 0.47\lambda$ — the only one connected
- **Parasites** carry current *induced* by the driven element's near field
- Slightly **long** = inductive = current **lags** $\rightarrow$ reflector, behind
- Slightly **short** = capacitive = current **leads** $\rightarrow$ directors, in front
- Net effect: a slow traveling wave forward, **endfire** beam, 15–25 dB front-to-back

<div class="callout">
<p>The long element lags, the short elements lead, and the beam goes toward the short end.</p>
</div>

Note:
This is L6's radiation integral with several filaments instead of one. No mutual-impedance matrices in this course; NEC did that for you in L8.

---

## Boom length buys the gain

| Elements | Boom | Typical gain |
| :-- | :-- | :-- |
| 3 | $0.3\lambda$ | 7.5 dBi |
| 6 | $1.0\lambda$ | 10 dBi |
| 10 | $2.2\lambda$ | 12.5 dBi |
| 16 | $4.5\lambda$ | 14.5 dBi |

- Roughly **+3 dB per doubling of boom**, and it flattens
- More directors on the *same* boom buy almost nothing
- Practical range 8–15 dBi; bandwidth a few percent
- TV, amateur, fixed point-to-point — anywhere the frequency does not move

Note:
One reflector is all you get; a second sees almost no field. If you need more than 15 dBi, you stack Yagis and it becomes an array.

---

## The third road: arrays

$$G_{\text{array}} = 10 \log_{10} N \quad \text{dB over one element}$$

- 16 elements: +12 dB. 64 elements: +18 dB.
- Only if the **aperture grows** with $N$ — you cannot stack elements on top of each other
- The beam is not welded to the structure: change the phases, move the beam
- Microseconds, no moving parts — every modern radar and 5G base station

<div class="callout">
<p>That is <strong>Module 3</strong>: array factor, pattern multiplication, steering, grating lobes, tapering — and a real beam on the ADALM-PHASER.</p>
</div>

Note:
Sell Module 3 here. The PHASER hardware is the payoff and they should be looking forward to it.

---

## Choosing: five questions

1. **How much gain do I actually need?** Run the link budget first.
2. **What frequency?** Apertures shrink with $\lambda$; wires get fragile.
3. **How much bandwidth?** Reflectors wide, Yagis narrow.
4. **Does it steer?** Mechanical, fixed, or electronic.
5. **Cost, size, weight, wind load?** A 20 dBi antenna that cannot survive local wind and ice loading is not a usable answer.

Note:
Order matters. Students always start at 5 and work backwards. Make them start at 1.

---

## Three roads, side by side

| | Reflector | Yagi-Uda | Planar array |
| :-- | :-- | :-- | :-- |
| Practical gain | 25–60 dBi | 8–15 dBi | 15–40 dBi |
| Bandwidth | wide | a few % | moderate |
| Steering | mechanical, slow | fixed | electronic, instant |
| Profile | bulky, 3-D | long boom | flat panel |
| Cost driver | surface accuracy | almost nothing | a chain per element |

Note:
The cost row is the one practicing engineers argue about. An array gives the best electrical performance and carries the highest cost.

---

## Worked selection — 20 dBi at 2.4 GHz

Cubesat ground station. $\lambda = 0.125$ m, $G = 20$ dBi $= 100$, so $A_e = G \lambda^2 / 4\pi = 0.124$ m².

| Candidate | Work | Result |
| :-- | :-- | :-- |
| Dish | $A = 0.124/0.6$, $\ D = 2\sqrt{A/\pi}$ | **0.51 m**, HPBW $17^\circ$ |
| Yagi | 15 dBi each, four stacked: $+10\log_{10}4$ | 21 dBi, four 0.56 m booms |
| Patch array | $7 \times 7$ at $\lambda/2$, 0.44 m square | 20.6 dBi, 49-way feed |

**Take the dish:** fewest parts, widest band, lowest cost. Take the array the moment you need a flat profile or electronic steering.

Note:
Every candidate has to deliver the same 0.124 square meters of coherent area. That is the whole selection argument in one number.

---

## Does the link close? (Friis, L2)

Cubesat at 1000 km, 2 W (33.0 dBm) into a 0 dBi antenna, our 20 dBi dish on the ground.

$$L_{\text{fs}} = 20 \log_{10} \left( 4 \pi R / \lambda \right) = 20 \log_{10} \left( 4 \pi \times 10^6 / 0.125 \right) = 160.1 \text{ dB}$$

$$P_r = 33.0 + 0 + 20 - 160.1 = -107.1 \text{ dBm}$$

- Noise floor in 100 kHz with a 3 dB NF: $\approx -121$ dBm
- **Margin: 14 dB.** Drop the dish for a patch and you are 13 dB *under* the noise.

Note:
This is the payoff slide. The 20 dB of antenna gain is the difference between a working downlink and silence.

---

## Midterm Project — Antenna Pattern Measurement

<div class="callout">
<p><strong>Introduced today, due at L20.</strong></p>
</div>

- **Design or select** an antenna
- **Measure its pattern** with the techniques from L12–L14
- **Report** gain, beamwidth, sidelobe levels, and polarization
- Full requirements are in the project handout, distributed in class

Start deciding now which antenna you want — the selection framework from this lesson is the reasoning your report has to show.

Note:
Hand out the packet here. Take questions on scope only; the details are in the handout.

---

## Key point

<div class="callout">
<p><strong>Gain is coherent area, counted in square wavelengths.</strong></p>
<p>A reflector rearranges phase with a mirror. A Yagi borrows its neighbors' currents. An array buys the area element by element. All three roads reach the same destination.</p>
</div>

Note:
Close the loop on the opening slide. If they leave with one sentence, this is the one.

---

## Where this is going

- Every gain number today was a **claim** — 0.65 was an assumption, $70^\circ \lambda / D$ a rule of thumb
- **L12:** pattern measurement theory — far-field ranges, gain comparison, three-antenna method
- **L13–L14:** on the instruments, measuring S-parameters and patterns
- **Module 3:** the third road, in full, with the PHASER

**Before you may write a gain on a data sheet, you have to measure it.**

Note:
Tie the 80 m far-field number from the worked example straight into L12. That is the hook.
