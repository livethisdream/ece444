<!-- .slide: class="title-slide" -->

<div class="title-left">

# ECE 444

Antennas, Phased Arrays, and Radar Systems

## Lesson 9 — Loop and Monopole Antennas

Fall 2026 · Dr. Neil Rogers

</div>

<div class="title-right">

![USAFA](./img/01-course-intro/USAFA-logo.png)

</div>

---

## Where we were

- **L6:** the pattern is the radiation integral of the current — shape of the current in, shape of the beam out.
- **L7:** the half-wave dipole, $73 + j42.5\ \Omega$, 2.15 dBi, HPBW $78^\circ$.
- **L8:** you built one in the simulator and watched those numbers appear.
- **L3:** small antennas pay for their size in bandwidth.

**Today: a mirror turns a dipole into a monopole, and a ring of current turns it into its magnetic twin.**

Note:
Anchor everything on the dipole numbers from L7 — today is two variations on an antenna they already own. Ask what happens to a dipole if you saw it in half.

---

## Today's plan

1. Image theory — the sign rule for a current over a conductor.
2. The quarter-wave monopole: half the impedance, twice the directivity.
3. What real ground does, and the hardware that fakes a ground plane.
4. The electrically small loop as a magnetic dipole.
5. The resonant loop, and why small costs bandwidth.

Note:
Tell them parts 1-2 are the exam material and part 3 is what they will meet in the field.

---

## A boundary condition you do not want to solve

An antenna over a large perfect conductor: tangential $E$ must be zero everywhere on the plane.

**Image theory:** delete the conductor. Add a mirror source below the plane with the sign that cancels tangential $E$ where the plane used to be.

- Same boundary condition satisfied, so **above the plane the fields are identical**.
- Below the plane the answer is fiction — and there was no field down there anyway.

<div class="callout">
The problem becomes two sources in free space with no conductor, and you already know how to add two sources.
</div>

Note:
Emphasize uniqueness: satisfy the boundary condition any way you like and you have THE answer. Same trick as image charges in electrostatics — they have seen this in physics.

---

## The sign rule

<div class="fig" data-inline-svg="./fig/L09-image-theory.svg" style="max-width:760px; margin:0 auto;"></div>

**Vertical (normal) currents image in phase. Horizontal (tangential) currents image reversed.**

Note:
Make them say it back. Then the consequence: a vertical antenna works sitting on the ground, a horizontal wire on the ground is a dummy load. Field-expedient antennas live or die on this slide.

---

## Element plus image = a two-element array

The image sits at $-h$: the two paths differ by $2kh\cos\theta$. That is L6 pattern multiplication, with a free second element.

$$\vert F(\theta)\vert = \vert f_{\text{el}}(\theta)\vert \times 2\left\vert \cos(kh\cos\theta)\right\vert \quad \text{vertical}$$

$$\vert F(\theta)\vert = \vert f_{\text{el}}(\theta)\vert \times 2\left\vert \sin(kh\cos\theta)\right\vert \quad \text{horizontal}$$

At the horizon $\cos\theta = 0$: vertical gives 2, horizontal gives 0.

<div class="callout">
Perfect ground puts a <strong>null on the horizon</strong> for horizontal polarization, at every height.
</div>

Note:
Only the upper hemisphere means anything. Point out that height cannot remove the horizon null for horizontal — it only moves the first lobe.

---

## Height is the whole design variable

| $h/\lambda$ | Vertical: $D$ | Vertical: radiated power | Horizontal: $D$ | Horizontal: radiated power |
| :-- | :-- | :-- | :-- | :-- |
| 0.01 | 5.16 dBi | $+3.0$ dB | 9.03 dBi | $-18.9$ dB |
| 0.05 | 5.24 dBi | $+2.9$ dB | 8.98 dBi | $-11.0$ dB |
| 0.25 | 6.83 dBi | $+1.3$ dB | 7.48 dBi | $+0.7$ dB |
| 0.50 | 8.42 dBi | $-0.3$ dB | 8.42 dBi | $-0.3$ dB |

Power is referred to the same element alone in free space, at the same feed current.

<p class="viz-cue">↗ Interactive on the lesson page</p>

Note:
Demo live: vertical at h = 0.01 reads D = 3.28, peak on the horizon — that is the monopole. Switch to horizontal at the same height: directivity goes up while the radiated power collapses. Directivity is shape only; cancellation shows up in radiation resistance.

---

## Cut a dipole in half

<div class="fig" data-inline-svg="./fig/L09-monopole-image.svg" style="max-width:760px; margin:0 auto;"></div>

Keep the top half, drive it against the plane, and the image restores the bottom half.

Note:
The current distribution on the remaining metal is unchanged. Above the plane it is literally the same antenna.

---

## Impedance halves

Same feed current as the dipole. Half the structure, so half the voltage.

$$Z_{\text{in}}^{\text{mono}} = \tfrac{1}{2} Z_{\text{in}}^{\text{dip}} = \tfrac{1}{2}(73 + j42.5) = 36.5 + j21.3\ \Omega$$

- Trim to resonance at $\approx 0.24\lambda$ and you get $\approx 36\ \Omega$ real.
- Against $50\ \Omega$ that is VSWR 1.4 with no matching network at all.

<div class="callout">
A monopole is the rare antenna that is <em>almost</em> matched to 50 &Omega; out of the box.
</div>

Note:
Ask why the current is the same but the voltage is halved — the feed point only sees half the structure. Compare with the dipole's 73 ohms from L7.

---

## Directivity doubles

Same pattern shape, same peak intensity, but **no power goes downward** — so the same beam is packed into half the solid angle.

$$D_{\text{mono}} = 2 D_{\text{dip}} = 2(1.64) = 3.28 \quad \rightarrow \quad 5.15\ \text{dBi}$$

- Elevation beam: the upper half of the dipole's $78^\circ$ beam.
- Peak on the horizon, null straight up.

<div class="callout">
The 3 dB is free in the same sense a mirror gives you free light: nothing was created, the power simply stopped going the wrong way.
</div>

Note:
Watch for the student who thinks the monopole radiates more total power. It radiates HALF the power for the same current and concentrates it into half the space.

---

## Dipole vs monopole

| Quantity | Half-wave dipole | Quarter-wave monopole |
| :-- | :-- | :-- |
| Length | $0.5\lambda$ | $0.25\lambda$ |
| $Z_{\text{in}}$ | $73 + j42.5\ \Omega$ | $36.5 + j21.3\ \Omega$ |
| Trimmed | $0.47\lambda$, $\approx 70\ \Omega$ | $0.24\lambda$, $\approx 36\ \Omega$ |
| Directivity | 1.64 (2.15 dBi) | 3.28 (5.15 dBi) |
| Coverage | all space | upper hemisphere |

Note:
This table is worth memorizing. Every number on the right is the left column divided or multiplied by two.

---

## Worked example — a 146 MHz whip

| Quantity | Work | Result |
| :-- | :-- | :-- |
| Wavelength | $3\times10^8 / 146\times10^6$ | $2.05\ \text{m}$ |
| Whip length | $\lambda/4$ | $51.4\ \text{cm}$ |
| $\vert\Gamma\vert$ | $\vert(36.5 + j21.3 - 50)/(36.5 + j21.3 + 50)\vert$ | $0.283$ |
| VSWR | $(1+0.283)/(1-0.283)$ | $1.79$ |
| Trimmed to $0.24\lambda$ | $50/36$ | VSWR $1.39$ |

Note:
Have them do the trim line themselves. Point out the reactance is what costs the match, not the resistance.

---

## Making 36 ohms into 50 ohms

- **Trim** the whip a few percent short — kills the $+j21.3\ \Omega$, leaves $\approx 36\ \Omega$ real.
- **Droop the radials** about $45^\circ$ — raises the base impedance to roughly $50\ \Omega$.
- Result: VSWR near 1.0 with zero added parts.

<div class="callout">
The sagging radials on a commercial ground-plane antenna are a matching network, not a manufacturing defect.
</div>

Note:
Drooping radials also lift the pattern slightly. The impedance effect is the reason they exist.

---

## Real ground is not a mirror

<div class="fig" data-inline-svg="./fig/L09-ground-systems.svg" style="max-width:770px; margin:0 auto;"></div>

Return current in dirt is loss in series with your feed: $\eta_{\text{rad}} = R_r/(R_r + R_g + R_{\text{ohmic}})$.

Note:
120 buried quarter-wave radials is the FCC standard for AM broadcast. The radials do not radiate — they replace lossy soil with copper for the return current.

---

## Three ways real ground bites

1. **Loss resistance** in series with $R_r$ — brutal when $R_r$ is small, since a short whip may only have a few ohms.
2. **Low-angle pattern damage** — real earth cannot support the grazing field, so the horizon lobe is eaten and the peak lifts a few degrees.
3. **Finite planes** — a car roof is many wavelengths at 800 MHz and a hundredth of a wavelength at 30 MHz. Same roof, different antenna.

<div class="callout">
With no ground plane available, build a <strong>counterpoise</strong>: drooped radials, a ground pour, a GPS ground disc, or, on a handheld, the case, the board, and your hand.
</div>

Note:
Handheld radios are tested against a phantom hand, because grip changes both impedance and pattern. Callback to L8: a monopole in NEC needs an explicit ground — a perfect plane for the textbook answer, a real-earth model for the realistic one — and the base segment is fed against it.

---

## The small loop: uniform current

<div class="fig" data-inline-svg="./fig/L09-loop-dipole-duality.svg" style="max-width:760px; margin:0 auto;"></div>

Circumference $C \ll \lambda$ (rule of thumb $C < 0.1\lambda$), so the current is the same everywhere around the ring.

Note:
Uniform current is the defining assumption. It is what makes the loop a pure magnetic dipole and it is what fails at C near a wavelength.

---

## The dual of the short dipole

| | Short dipole | Small loop |
| :-- | :-- | :-- |
| Source | $I$ along a length | $I$ around an area |
| Far field | $E_\theta$, $H_\phi$ | $E_\phi$, $H_\theta$ |
| Pattern | $\vert F \vert = \sin\theta$ | $\vert F \vert = \sin\theta$ |
| Directivity | 1.5 (1.76 dBi) | 1.5 (1.76 dBi) |
| Null | along the wire | along the loop axis |

**Same donut. Orthogonal polarization. Maximum in the plane of the loop.**

Note:
Most students expect the loop to radiate out of the hole. It does the opposite. This is the basis of direction finding: rotate for the null, because nulls are sharp and peaks are broad.

---

## The fourth-power penalty on circumference

$$R_r = 20\pi^2 \left(\frac{C}{\lambda}\right)^4 = 320\pi^4 \left(\frac{A}{\lambda^2}\right)^2 \ \Omega$$

- At $C = 0.1\lambda$: $R_r = 0.0197\ \Omega$. Twenty milliohms.
- Halve the loop and $R_r$ drops by a factor of **16**.
- Compare: the half-wave dipole sits at $73\ \Omega$.

<div class="callout">
The problem is not the match. The radiation resistance is smaller than the loss resistance of the wire itself.
</div>

Note:
Have them compute Rr for C = 0.05 lambda in their heads: divide by 16, about 1.2 milliohms.

---

## Worked example — a 30 MHz loop

Single turn, $C = 0.1\lambda$ at 30 MHz, 4 mm copper wire.

| Quantity | Work | Result |
| :-- | :-- | :-- |
| $R_r$ | $20\pi^2 (0.1)^4$ | $0.0197\ \Omega$ |
| $R_{\text{ohmic}}$ | $(C/2\pi b) R_s = 79.6 \times 1.43\ \text{m}\Omega$ | $0.114\ \Omega$ |
| Efficiency | $0.0197/(0.0197+0.114)$ | $14.8\%$, i.e. $-8.3$ dB |
| Gain | $1.76 - 8.3$ | $-6.5\ \text{dBi}$ |

For 100 W delivered you need 38.7 A peak — and 85 W of it heats the wire.

Note:
The 38.7 A is the number to emphasize. Transmitting loops need copper tube, welded joints and a vacuum capacitor for exactly this reason.

---

## Why receive loops are everywhere anyway

- On receive you are fighting **external noise**, not efficiency — below VHF the sky is far noisier than the receiver.
- A lossy antenna still delivers a sky-noise-limited signal-to-noise ratio.
- $N$ turns: $R_r$ goes as $N^2$, loss only as $N$.
- Wind those turns on a **ferrite rod** and the effective permeability multiplies the moment again.

<div class="callout">
The bar behind the dial of an AM radio is a many-turn ferrite loop. Its efficiency is very low, and at broadcast frequencies that costs nothing that matters.
</div>

Note:
Also mention loops reject local electric-field noise — a shielded loop is the standard tool for sniffing out interference.

---

## Grow it to one wavelength

| | Small loop | Resonant loop |
| :-- | :-- | :-- |
| Circumference | $C < 0.1\lambda$ | $C \approx 1\lambda$ |
| Current | uniform | reverses around the loop |
| Maximum | in the plane | along the axis |
| $R_{\text{in}}$ | milliohms | $100$ to $130\ \Omega$ |
| Use | receive, direction finding | transmit element (quad) |

**The pattern maximum moves to where the small loop had its null.**

Note:
The quad element is exactly this. Directivity about 3.1 dBi, a bit under 1 dB over a dipole, and a clean 100-ohm-ish feed.

---

## Small costs bandwidth — again

An antenna inside a sphere of radius $a$ stores far more near-field energy than it radiates each cycle. The Chu limit from L3:

$$Q \gtrsim \frac{1}{(ka)^3} \qquad \text{fractional bandwidth} \approx \frac{1}{Q}$$

- The 30 MHz loop: $ka = 0.1$, so $Q \approx 10^3$ and the match holds over roughly $0.1\%$ — about 30 kHz.
- Retune every time you move across the band.

Note:
One sentence of theory, no derivation — they saw the Chu curve in L3. Make the closing point explicitly: loss is the only thing that broadens a small antenna, and it does so by dissipating the power you meant to radiate.

---

## Key point

<div class="callout">
<p>A monopole is a dipole plus a mirror: <strong>half the impedance, twice the directivity, one hemisphere</strong>.</p>
<p>A small loop is a dipole with the fields swapped: same donut, orthogonal polarization, and a radiation resistance that dies as the <strong>fourth power</strong> of its circumference.</p>
</div>

Note:
If they remember one slide, this is it. Both antennas are the dipole they already know, seen through a transformation.

---

## Where this is going

- **L10:** patch, slot, and horn — the radiator becomes a surface or an opening. The patch is two slots over a ground plane, so you will use image theory again on day one.
- **Module 3:** a monopole is an element plus one image; an array is an element plus many neighbors. Same element-factor-times-array-factor bookkeeping.
- **L16:** when we do pattern multiplication properly, remember that today's height-above-ground curve was already a two-element array.

<div class="callout">
You now own the whole wire-antenna toolkit. Everything after this is aperture, array, or both.
</div>

Note:
Set up L10 by asking what happens when the current lives on a surface instead of a wire.
