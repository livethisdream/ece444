<!-- .slide: class="title-slide" -->

<div class="title-left">

# ECE 444

Antennas, Phased Arrays, and Radar Systems

## Lesson 12 — Loop and Monopole Antennas

Fall 2026 · Dr. Neil Rogers

</div>

<div class="title-right">

![USAFA](./img/01-course-intro/USAFA-logo.png)

</div>

---

## Where We Were

- **L7:** the half-wave dipole, $73 + j42.5\ \Omega$, 2.15 dBi, HPBW $78^\circ$.
- **L8:** we modeled one in the simulator and reproduced those numbers.
- **L9–L11:** we measured an antenna's match, pattern, and gain.
- **L3:** a smaller antenna has a narrower bandwidth.

Today, image theory turns a dipole into a monopole, and a small loop of current behaves as the dipole's magnetic dual.

Note:
Anchor everything on the dipole numbers from L7 — today is two variations on an antenna they already own. Ask what happens to a dipole if you saw it in half. Worth saying explicitly: from here on every impedance and gain figure is a claim they know how to test, and several of today's antennas are defensible midterm choices.

---

## Today's Plan

1. Image theory — the sign rule for a current over a conductor.
2. The quarter-wave monopole: half the impedance, twice the directivity.
3. What real ground does, and the counterpoises that substitute for a ground plane.
4. The electrically small loop as a magnetic dipole.
5. The resonant loop, and the size-bandwidth limit.

Note:
Tell them parts 1-2 are the exam material and part 3 is what they will meet in the field.

---

## Image Theory

For an antenna over a large perfect conductor, tangential $E$ must be zero everywhere on the plane.

**Image theory:** delete the conductor. Add a mirror source below the plane with the sign that cancels tangential $E$ where the plane used to be.

- The same boundary condition is satisfied, so above the plane the fields are identical.
- Below the plane the image solution has no physical meaning, and the true field there is zero.

<div class="callout">
The problem becomes two sources in free space with no conductor, and we already know how to add two sources.
</div>

Note:
Emphasize uniqueness: satisfy the boundary condition any way you like and you have THE answer. Same trick as image charges in electrostatics — they have seen this in physics.

---

## The Sign Rule

<div class="fig" data-inline-svg="./fig/L12-image-theory.svg" style="max-width:760px; margin:0 auto;"></div>

Vertical (normal) currents image in phase. Horizontal (tangential) currents image reversed.

Note:
Make them say it back. Then the consequence: a vertical antenna works sitting on the ground, a horizontal wire on the ground is a dummy load. Field-expedient antennas depend on this slide.

---

## Where the Phase Comes From

<div class="fig" data-inline-svg="./fig/L12-image-paths.svg" style="max-width:520px; margin:0 auto;"></div>

The source leads the wavefront by $h\cos\theta$ and the image lags by the same amount, so the two phases are $\pm kh\cos\theta$.

$$AF(\theta) = e^{+jkh\cos\theta} \pm e^{-jkh\cos\theta}$$

Note:
The image's sign picks plus or minus: plus for a vertical current, minus for a horizontal one. This is the L6 two-element array with spacing 2h, so the phase difference between the paths is 2kh cos theta.

---

## Element and Image as a Two-Element Array

Euler's formula turns the sum into $2\cos(kh\cos\theta)$ for the vertical case and $2j\sin(kh\cos\theta)$ for the horizontal case, and the pattern is the element factor times it.

$$\vert F(\theta)\vert = \vert f_{\text{el}}(\theta)\vert \times 2\left\vert \cos(kh\cos\theta)\right\vert \quad \text{vertical}$$

$$\vert F(\theta)\vert = \vert f_{\text{el}}(\theta)\vert \times 2\left\vert \sin(kh\cos\theta)\right\vert \quad \text{horizontal}$$

At the horizon, where $\cos\theta = 0$, the vertical factor is 2 and the horizontal factor is 0.

<div class="callout">
Perfect ground puts a <strong>null on the horizon</strong> for horizontal polarization, at every height.
</div>

Note:
Only the upper hemisphere means anything. Point out that height cannot remove the horizon null for horizontal — it only moves the first lobe.

---

## Height Above Ground

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

## The Quarter-Wave Monopole

<div class="fig" data-inline-svg="./fig/L12-monopole-image.svg" style="max-width:760px; margin:0 auto;"></div>

Keep the top half, drive it against the plane, and the image restores the bottom half.

Note:
The current distribution on the remaining metal is unchanged. Above the plane it is the same antenna.

---

## Monopole Impedance

The feed current matches the dipole's, but the structure is half as long, so the feed voltage is half.

$$Z_{\text{in}}^{\text{mono}} = \tfrac{1}{2} Z_{\text{in}}^{\text{dip}} = \tfrac{1}{2}(73 + j42.5) = 36.5 + j21.3\ \Omega$$

- Trimmed to resonance at $\approx 0.24\lambda$, the monopole is $\approx 36\ \Omega$ and purely real.
- Against $50\ \Omega$ that is VSWR 1.4 with no matching network.

<div class="callout">
A trimmed monopole is close to a 50 &Omega; match without a matching network.
</div>

Note:
Ask why the current is the same but the voltage is halved — the feed point only sees half the structure. Compare with the dipole's 73 ohms from L7.

---

## Monopole Directivity

The pattern shape and peak intensity are the dipole's, but no power goes downward, so the same beam fills half the solid angle.

$$D_{\text{mono}} = 2 D_{\text{dip}} = 2(1.64) = 3.28 \quad \rightarrow \quad 5.15\ \text{dBi}$$

- The elevation beam is the upper half of the dipole's $78^\circ$ beam.
- The peak is on the horizon and the null is straight up.

<div class="callout">
No power is created. The same beam fills half the sphere, so its peak is twice the average.
</div>

Note:
Watch for the student who thinks the monopole radiates more total power. It radiates HALF the power for the same current and concentrates it into half the space.

---

## Dipole Versus Monopole

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

## Worked Example: A 146 MHz Whip

| Quantity | Work | Result |
| :-- | :-- | :-- |
| Wavelength | $3\times10^8 / 146\times10^6$ | $2.05\ \text{m}$ |
| Whip length | $\lambda/4$ | $51.4\ \text{cm}$ |
| $\vert\Gamma\vert$ | $\vert(36.5 + j21.3 - 50)/(36.5 + j21.3 + 50)\vert$ | $0.283$ |
| VSWR | $(1+0.283)/(1-0.283)$ | $1.79$ |
| Trimmed to $0.24\lambda$ | $50/36$ | VSWR $1.39$ |

Note:
Have them do the trim line themselves. Point out that the reactance, not the resistance, is what limits the match.

---

## Matching the Monopole to 50 Ω

- **Trimming** the whip a few percent short removes the $+j21.3\ \Omega$ and leaves $\approx 36\ \Omega$.
- **Drooping the radials** about $45^\circ$ raises the base impedance to roughly $50\ \Omega$.
- Together they give a VSWR near 1.0 with no added parts.

<div class="callout">
The drooping radials on a commercial ground-plane antenna are its matching network.
</div>

Note:
Drooping radials also lift the pattern slightly. The impedance effect is the reason they exist.

---

## Real Ground

<div class="fig" data-inline-svg="./fig/L12-ground-systems.svg" style="max-width:770px; margin:0 auto;"></div>

Return current in the soil adds loss in series with the feed:

$$\eta_{\text{rad}} = \frac{R_r}{R_r + R_g + R_{\text{ohmic}}}$$

Note:
120 buried quarter-wave radials is the FCC standard for AM broadcast. The radials do not radiate — they replace lossy soil with copper for the return current.

---

## Effects of Real Ground

1. **Loss resistance** in series with $R_r$ is significant when $R_r$ is small, since a short whip may have only a few ohms.
2. **Low-angle pattern loss**: real earth cannot support the grazing field, so the horizon lobe is lost and the peak rises a few degrees.
3. **Finite planes**: a car roof is several wavelengths across at 800 MHz but only about $0.15\lambda$ at 30 MHz, so the same roof is a very different ground.

<div class="callout">
With no ground plane available, build a <strong>counterpoise</strong>: drooped radials, a ground pour, a GPS ground disc, or, on a handheld, the case, the board, and your hand.
</div>

Note:
Handheld radios are tested against a phantom hand, because grip changes both impedance and pattern. Callback to L8: a monopole in NEC needs an explicit ground — a perfect plane for the textbook answer, a real-earth model for the realistic one — and the base segment is fed against it.

---

## Same Radome, Three Antennas

<div class="fig" data-inline-svg="./fig/L12-radome-lookalikes.svg" style="max-width:560px; margin:0 auto;"></div>

- A vertical in a plastic tube may be a monopole, a sleeve dipole, or a folded dipole.
- Only the monopole takes its other half from the mount. Read the datasheet, not the housing.

Note:
On a fiberglass mast a monopole's return current runs on the coax shield: the feed line becomes the counterpoise, and pattern and VSWR follow the cable routing (L4 common mode, from the other side). The sleeve is a shorted quarter-wave stub, so it is both the lower arm and a choke. The folded dipole is about 290 ohms (L7) and ships with a 4:1 balun in the base (L4); a folded monopole is about 146 ohms and needs a ground again.

---

## The Small Loop

<div class="fig" data-inline-svg="./fig/L12-loop-dipole-duality.svg" style="max-width:760px; margin:0 auto;"></div>

Circumference $C \ll \lambda$ (rule of thumb $C < 0.1\lambda$), so the current is the same everywhere around the ring.

Note:
Uniform current is the defining assumption. It is what makes the loop a pure magnetic dipole and it is what fails at C near a wavelength. Tie m = IA to Biot-Savart: far out on the axis the static loop field is mu0 m over 2 pi z cubed, the same form as an electric dipole, so only the product I times A survives. Oscillating, the loop radiates like a short dipole of length kA, and putting that into 80 pi squared (dl over lambda) squared gives the fourth-power law.

---

## Duality with the Short Dipole

| | Short dipole | Small loop |
| :-- | :-- | :-- |
| Source | $I$ along a length | $I$ around an area |
| Far field | $E_\theta$, $H_\phi$ | $E_\phi$, $H_\theta$ |
| Pattern | $\vert F \vert = \sin\theta$ | $\vert F \vert = \sin\theta$ |
| Directivity | 1.5 (1.76 dBi) | 1.5 (1.76 dBi) |
| Null | along the wire | along the loop axis |

The pattern is the same donut with orthogonal polarization, and the maximum is in the plane of the loop.

Note:
Most students expect the loop to radiate out of the hole. It does the opposite. This is the basis of direction finding: rotate for the null, because nulls are sharp and peaks are broad.

---

## The Fourth-Power Penalty

$$R_r = 20\pi^2 \left(\frac{C}{\lambda}\right)^4 = 320\pi^4 \left(\frac{A}{\lambda^2}\right)^2 \ \Omega$$

- At $C = 0.1\lambda$, $R_r = 0.0197\ \Omega$, or about 20 mΩ.
- Halve the loop and $R_r$ drops by a factor of **16**.
- The half-wave dipole, for comparison, is $73\ \Omega$.

<div class="callout">
The problem is not the match. At $C = 0.1\lambda$, 20 mΩ of radiation resistance against 114 mΩ of copper loss sends 85% of the power into heat.
</div>

Note:
Have them compute Rr for C = 0.05 lambda in their heads: divide by 16, about 1.2 milliohms.

---

## Worked Example: A 30 MHz Loop

The loop is a single turn of 4 mm copper wire with $C = 0.1\lambda$ at 30 MHz.

| Quantity | Work | Result |
| :-- | :-- | :-- |
| $R_r$ | $20\pi^2 (0.1)^4$ | $0.0197\ \Omega$ |
| $R_{\text{ohmic}}$ | $(C/2\pi b) R_s = 79.6 \times 1.43\ \text{m}\Omega$ | $0.114\ \Omega$ |
| Efficiency | $0.0197/(0.0197+0.114)$ | $14.8\%$, i.e. $-8.3$ dB |
| Gain | $1.76 - 8.3$ | $-6.5\ \text{dBi}$ |

Delivering 100 W takes 38.7 A peak, and 85 W of it heats the wire.

Note:
The 38.7 A is the number to emphasize. Transmitting loops need copper tube, welded joints and a vacuum capacitor for exactly this reason.

---

## Low Efficiency, Same SNR

- Loss cuts the signal **and** the external noise by the same factor.
- SNR holds until the external noise falls to the receiver's floor.
- At 1 MHz, external noise is 70 dB above $kT_0$; 40 dB of loss barely changes SNR.
- Designs still raise the output: $N$ turns raise $R_r$ as $N^2$ and loss only as $N$, and a **ferrite rod** multiplies the moment again.

<div class="callout">
The bar behind the dial of an AM radio is a many-turn ferrite loop. Its efficiency is very low, and at broadcast frequencies that loss does not reduce the SNR.
</div>

Note:
Also mention loops reject local electric-field noise — a shielded loop is the standard tool for locating interference.

---

## Why the Current Reverses

<div class="fig" data-inline-svg="./fig/L12-resonant-loop.svg" style="max-width:620px; margin:0 auto;"></div>

- At $C \approx 1\lambda$ the current is a standing wave, $I_0\cos(ks)$, with nulls a quarter of the way around.
- It reverses halfway around, so the top and bottom currents point the same way and the loop stops circulating.

Note:
Walk the arrows: the reversal is measured around the loop, and on the far side the wire runs the other way, so the two flips cancel. The loop is now two parallel in-phase elements about lambda over pi apart. They add along the axis and partly cancel in the plane, which is why the maximum moves to the axis.

---

## The Resonant Loop

| | Small loop | Resonant loop |
| :-- | :-- | :-- |
| Circumference | $C < 0.1\lambda$ | $C \approx 1\lambda$ |
| Current | uniform | reverses around the loop |
| Maximum | in the plane | along the axis |
| $R_{\text{in}}$ | milliohms | $100$ to $130\ \Omega$ |
| Use | receive, direction finding | transmit element (quad) |

The pattern maximum moves to where the small loop had its null.

Note:
The quad element is exactly this. Directivity about 3.1 dBi, a bit under 1 dB over a dipole, and a clean 100-ohm-ish feed.

---

## Small Antennas and the Chu Limit

An antenna inside a sphere of radius $a$ stores far more near-field energy than it radiates each cycle. The Chu limit from L3:

$$Q \gtrsim \frac{1}{(ka)^3} \qquad \text{fractional bandwidth} \approx \frac{1}{Q}$$

- The 30 MHz loop: $ka = 0.1$, so $Q \approx 10^3$ and the match holds over roughly $0.1\%$ — about 30 kHz.
- A magnetic loop must be retuned whenever the frequency moves across the band.

Note:
One sentence of theory, no derivation — they saw the Chu curve in L3. Make the closing point explicitly: loss is the only thing that broadens a small antenna, and it does so by dissipating the power you meant to radiate.

---

## Key Points

<div class="callout">
<p>A monopole is a dipole plus its image, with half the impedance, twice the directivity, and one hemisphere of coverage.</p>
<p>A small loop is a dipole with the fields exchanged: the same donut, orthogonal polarization, and a radiation resistance that falls as the <strong>fourth power</strong> of its circumference.</p>
</div>

Note:
If they remember one slide, this is it. Both antennas are the dipole they already know, seen through a transformation.

---

## Where This Is Going

- **L13:** patch, slot, and horn — the radiator becomes a surface or an opening. The patch is two slots over a ground plane, so image theory applies there too.
- **Module 3:** a monopole is an element plus one image; an array is an element plus many neighbors. Same element-factor-times-array-factor bookkeeping.
- **L16:** when we do pattern multiplication properly, remember that today's height-above-ground curve was already a two-element array.

<div class="callout">
The wire antennas are now complete; the rest of the course covers apertures, arrays, or both.
</div>

Note:
Set up L13 by asking what happens when the current lives on a surface instead of a wire.
