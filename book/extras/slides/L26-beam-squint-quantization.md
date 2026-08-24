<!-- .slide: class="title-slide" -->

<div class="title-left">

# ECE 444

Antennas, Phased Arrays, and Radar Systems

## Lesson 26 — Beam Squint and Quantization

Fall 2026 · Dr. Neil Rogers

</div>

<div class="title-right">

![USAFA](./img/01-course-intro/USAFA-logo.png)

</div>

---

## Where we were

- L24 traced the sidelobes back to the amplitude distribution across the aperture.
- L25 put that in your hands: Hann, Blackman and Chebyshev tapers drove the sidelobes under the noise floor, and in exchange the beam widened and the peak dropped.
- Everything so far assumed the phase ramp was exact and the elements were spaced half a wavelength apart.

**Today: the three things that still break the pattern — spacing, bandwidth, and finite phase resolution.**

Note:
Reset the frame. Amplitude control is finished business after the tapering lab. The three defects today are not fixed by any taper, because none of them is an amplitude problem. Tell them the goal is one design number per defect.

---

## Today's plan

1. Why the array factor repeats, and where the repeats land.
2. The spacing criterion that keeps them out of sight.
3. Beam squint: one phase setting, a whole band of frequencies.
4. Phase quantization: the beam angles you can command.
5. What each one costs a radar or a comm link.

Note:
Three phenomena, one objective. Each gets a derivation, a number, and a demo on the kit.

---

## The array factor is periodic

Everything in Module 3 is a function of one variable, $\psi = kd\ (\sin\theta - \sin\theta_0)$:

$$AF_N(\psi) = \frac{\sin(N\psi/2)}{N\sin(\psi/2)}$$

Replace $\psi \rightarrow \psi + 2\pi$ and both sines flip sign:

$$\sin\left(\frac{N\psi}{2} + N\pi\right) = (-1)^N \sin\left(\frac{N\psi}{2}\right) \qquad \sin\left(\frac{\psi}{2} + \pi\right) = -\sin\left(\frac{\psi}{2}\right)$$

<div class="callout">The magnitude is unchanged: the array factor <strong>repeats with period 2&pi; in &psi;</strong>.</div>

Note:
Derive at the board. The point is that the peak at psi equals zero is not unique — the same peak sits at plus or minus two pi, four pi, and so on. Nothing in the algebra says only one of them is a real angle.

---

## Visible space

Real angles run $-90^\circ \le \theta \le +90^\circ$, so $\sin\theta$ runs from $-1$ to $+1$ and

$$\psi \ \text{spans a window of width} \ 2kd = 4\pi\ \frac{d}{\lambda}$$

| $d/\lambda$ | Width of visible space | Repeats in view |
| :-- | :-- | :-- |
| 0.25 | $\pi$ | none |
| 0.5 | $2\pi$ | none (one lands exactly at the horizon) |
| 1.0 | $4\pi$ | one pair |
| 1.5 | $6\pi$ | two pairs |

<div class="callout">Spacing sets <strong>how much of the repeating array factor you can see</strong>. Wider spacing brings more periods into view.</div>

Note:
This is the whole idea in one table. The array factor does not change shape when you widen d — you just look at more of it.

---

## The grating condition

A repeat is at full height wherever $\psi = 2\pi m$:

$$kd\ (\sin\theta_g - \sin\theta_0) = 2\pi m$$

$$\frac{2\pi d}{\lambda}(\sin\theta_g - \sin\theta_0) = 2\pi m$$

$$\sin\theta_g = \sin\theta_0 \pm m\ \frac{\lambda}{d} \qquad m = 1, 2, \ldots$$

Any solution with $\vert \sin\theta_g \vert \le 1$ is a real angle, and the array puts a beam there.

Note:
Three lines, do them live. Emphasise that the steer angle carries the whole lobe pattern with it: steer the main beam and every grating lobe slides by the same amount in sine space, not in degrees.

---

## A grating lobe is not a sidelobe

<div class="two-col"><div class="col-text">

At $\theta_g$ the path difference between neighbouring elements is a **whole wavelength** instead of zero.

Every element is back in phase. The array cannot tell the two directions apart.

So the grating lobe is **exactly as tall as the main lobe**, and a taper does nothing to it — a taper shapes the skirts of one beam, and this is a second beam.

</div><div class="col-fig">

| | Sidelobe | Grating lobe |
| :-- | :-- | :-- |
| Height | −13 dB and down | 0 dB |
| Set by | amplitude taper | element spacing |
| Cure | taper | closer elements |

</div></div>

Note:
This is the misconception to kill. Students who just finished the tapering lab will reach for a taper. Say plainly that the taper cannot see the difference between the two beams.

---

<div class="fig" data-inline-svg="./fig/L26-grating-thinning.svg" style="max-width:1060px; margin:0 auto;"></div>

Note:
Walk left to right. Fourteen millimeters: one beam, nothing else in view. Twenty-eight: still one beam, but the horizon has come up to full height. Forty-two and fifty-six: two extra beams, same height as the main one, marching inward as the spacing grows.

---

<!-- .slide: class="viz-cue-slide" -->

## Thinning the PHASER row

Eight patches on a 14 mm pitch, broadside, $\lambda = 29.1$ mm at 10.3 GHz:

| Fed elements | $d_{\text{eff}}$ | $\lambda/d$ | Predicted lobes | Measured |
| :-- | :-- | :-- | :-- | :-- |
| all 8 | 14 mm | 2.08 | none | none |
| every 2nd | 28 mm | 1.04 | none (at the horizon) | rise at $\pm 90^\circ$ |
| every 3rd | 42 mm | 0.693 | $0^\circ, \pm 43.9^\circ$ | $\pm 42^\circ$ |
| every 4th | 56 mm | 0.520 | $0^\circ, \pm 31.3^\circ$ | $\pm 31^\circ, \pm 85\text{–}90^\circ$ |

<p class="viz-cue">↗ Interactive on the lesson page</p>

Note:
Demo on the kit: Lab preset 4, Grating Lobes — or from a clean state, Element Gains, Aperture Presets, Sparse lambda. Run a sweep with all eight on, freeze the trace, then thin to every third element and sweep again. Two new beams appear at plus and minus forty-two degrees at the same height as the main one. Predict the angles on the board before pressing Start.

---

## Keeping them out of sight

The dangerous solution is the one nearest the horizon on the far side of the beam. For $\theta_0 > 0$ take $m = 1$ with the minus sign and push it past $-90^\circ$:

$$\sin\theta_0 - \frac{\lambda}{d} < -1 \qquad \Longrightarrow \qquad \frac{\lambda}{d} > 1 + \sin\theta_0$$

$$d < \frac{\lambda}{1 + \vert \sin\theta_0 \vert}$$

<div class="callout">The wider you intend to scan, <strong>the closer together the elements must be</strong>.</div>

Note:
Derive it, then read it out loud in words. Scan range and spacing trade against each other, and the trade is set before the array is built.

---

## Design numbers

| Scan range | Max spacing |
| :-- | :-- |
| broadside only | $d < \lambda$ |
| $\pm 30^\circ$ | $d < 0.667\lambda$ |
| $\pm 45^\circ$ | $d < 0.586\lambda$ |
| $\pm 60^\circ$ | $d < 0.536\lambda$ |
| any angle | $d \le \lambda/2$ |

The PHASER at the HB100's 10.525 GHz: $d/\lambda = 14/28.5 = 0.491$, so $\lambda/d = 2.04 > 1 + \vert\sin\theta_0\vert$ for **every** real angle.

<div class="callout"><strong>Half-wavelength spacing is the default</strong> because it is grating-lobe-free at any scan angle you can command.</div>

Note:
Ask them why the board designer chose fourteen millimeters. Answer: it is just inside half a wavelength at the top of the band, which gives the full scan range with no ambiguity.

---

## Beam squint: the setup

A phase shifter is set **once**, in degrees, at one frequency.

- The beam-steering computer computes the lag from $k_0 = 2\pi/\lambda_0$ at the design frequency $f_0$.
- The signal occupies a band, so it arrives at some other $f$.
- The path lengths did not change. The phase those path lengths produce **did**.

<div class="callout">A phase ramp is only the right ramp <strong>at one frequency</strong>.</div>

Note:
Set this up physically before any algebra. The delay across the array is a length; the shifter works in degrees; degrees per unit length is proportional to frequency.

---

## Beam squint: where the beam points, and where it was commanded

Applied lag on element $n$, computed at $f_0$:

$$\alpha_n = n\ k_0 d \sin\theta_0$$

The elements add in phase toward whichever $\theta$ cancels it at the frequency in use:

$$kd\sin\theta = k_0 d\sin\theta_0 \quad \Longrightarrow \quad \sin\theta = \frac{\lambda}{\lambda_0}\sin\theta_0 = \frac{f_0}{f}\sin\theta_0$$

$$\Delta\theta = \arcsin\left(\frac{f_0}{f}\sin\theta_0\right) - \theta_0$$

Note:
Two lines at the board. Point out what cancelled: N is gone, d is gone. Only the frequency ratio survives, so squint is a property of the steer angle and the band, not of the array size.

---

## Read the squint formula

- **Zero at broadside.** No ramp, nothing to scale.
- **Independent of $N$ and $d$.** Ramp and path lengths scale together.
- **Grows with scan angle.** For a small fractional offset $\delta = (f - f_0)/f_0$:

$$\Delta\theta \approx -\delta\ \tan\theta_0 \quad \text{(radians)}$$

- **Beam walks toward the horizon as the frequency drops.**

<div class="callout">Squint is a <strong>fractional-bandwidth times tangent</strong> problem. Narrow band or near broadside, it is negligible.</div>

Note:
The tangent is the part to remember. At sixty degrees the tangent is one point seven three; at seventy-five it is three point seven. Wide-scan wideband arrays are where this becomes a design driver.

---

<div class="fig" data-inline-svg="./fig/L26-squint-band.svg" style="max-width:960px; margin:0 auto;"></div>

Note:
One phase ramp, three frequencies, three different peak angles. The lower the frequency, the further from broadside the beam sits. Nothing about the array changed between the three traces.

---

<!-- .slide: class="viz-cue-slide" -->

## Worked example — 500 MHz at 45°

Phases set for $\theta_0 = 45^\circ$ at $f_0 = 10.525$ GHz; signal arrives at 10.025 GHz.

| Quantity | Work | Result |
| :-- | :-- | :-- |
| Frequency ratio | $10.525/10.025$ | $1.0499$ |
| New sine | $1.0499 \times 0.7071$ | $0.7424$ |
| Peak angle | $\arcsin 0.7424$ | $47.9^\circ$ |
| Squint | $47.9 - 45$ | $+2.9^\circ$ |
| Quick check | $-\delta\tan\theta_0 = 0.0475$ rad | $+2.7^\circ$ |
| Loss at the aimpoint | from the pattern | $-0.25$ dB |

<p class="viz-cue">↗ Interactive on the lesson page</p>

Note:
Demo on the kit: Lab preset 5, Beam Squint. Steer to forty-five degrees, turn on the squint readout under Plot Options, then move the Signal BW slider and watch the peak angle move while the commanded angle stays put. Compare the readout with the two point nine degrees on the board.

---

## Why squint matters

<div class="two-col"><div class="col-text">

**Wideband radar.** Every frequency in the pulse points somewhere slightly different. The compressed pulse is smeared in angle, the effective beam is broadened, and the reported target angle is biased.

**Communications.** A modulated carrier loses gain at the band edges relative to the center, which appears as amplitude tilt across the channel.

</div><div class="col-fig">

| Fractional offset | Squint at 45° |
| :-- | :-- |
| 0.5% | 0.3° |
| 2.4% | 1.4° |
| 4.8% | 2.9° |
| 9.5% | 6.4° |

</div></div>

Note:
Two failure modes, two different customers. Radar cares about angle accuracy; the comm link cares about flatness across the channel.

---

## The cure is time, not phase

Replace the phase lag with a **true time delay**:

$$\tau_n = \frac{n\ d \sin\theta_0}{c}$$

- The delay compensates the geometric path difference itself, which is a **length**.
- Every frequency in the band then arrives in phase at the same angle.
- Squint is gone at all offsets, not reduced.

<div class="callout">True time delay is expensive in analog hardware. Large wideband arrays compromise: <strong>time delay between subarrays, phase shifters inside them</strong>.</div>

Note:
One slide, no implementation. The idea students should carry is that squint exists because we approximated a delay with a phase, and the fix is to stop approximating.

---

## Phase quantization

The ADAR1000 does not accept an arbitrary phase. $B$ bits divide the circle into $2^B$ steps:

$$\text{LSB} = \frac{360^\circ}{2^B}$$

| $B$ | States | LSB |
| :-- | :-- | :-- |
| 2 | 4 | $90^\circ$ |
| 3 | 8 | $45^\circ$ |
| 5 | 32 | $11.25^\circ$ |
| 7 | 128 | $2.8125^\circ$ |

<div class="callout">The ADAR1000 is a <strong>7-bit</strong> shifter: every commanded phase is rounded to the nearest 2.8125&deg;.</div>

Note:
Write the LSB on the board and leave it there for the rest of the hour. It reappears in the next two lessons as the limit on null depth.

---

## Consequence 1 — pointing granularity

Inter-element phase for a beam at $\theta_0$:

$$\Delta\phi = 360^\circ\ \frac{d}{\lambda}\ \sin\theta_0$$

Only multiples of the LSB exist, so only a discrete set of beam angles exists:

$$\sin\theta_0 = \frac{m\ \text{LSB}}{360^\circ\ (d/\lambda)} \qquad \Delta\theta_0 \approx \frac{\text{LSB}}{360^\circ\ (d/\lambda)}\ \text{rad near broadside}$$

PHASER, $d/\lambda = 0.491$, $B = 7$: $\Delta\theta_0 = 0.0159$ rad $= 0.91^\circ$, about one-fourteenth of the $13.2^\circ$ beam.

Note:
Do the arithmetic live. Then run it at two bits: twenty-nine degrees per step, so a two-bit array can only point at broadside and at about plus or minus thirty-one degrees.

---

## Consequence 2 — quantization sidelobes

A real controller computes the exact ramp, then rounds **each element separately**.

- The beam still lands close to the commanded angle.
- What is left is a **staircase error**, bounded by half an LSB, repeating across the aperture.
- A periodic phase error radiates. Where it radiates is a quantization sidelobe.

$$\text{QSLL} \approx -6B\ \text{dB}$$

<div class="callout">Rule of thumb, RMS, large arrays: <strong>2 bits gives −12 dB, 7 bits gives −42 dB</strong>. Six decibels per bit.</div>

Note:
Name it as a rule of thumb and do not derive the RMS analysis. Add the caveat: on eight elements there are only a couple of sawtooth periods, individual lobes scatter several decibels either side, and from three bits up they hide under the array's own minus thirteen decibel sidelobes.

---

<div class="fig" data-inline-svg="./fig/L26-quant-staircase.svg" style="max-width:1060px; margin:0 auto;"></div>

Note:
Left panel: the ramp the beamformer wants and the steps the hardware can produce. Right panel: at four bits the pattern is on top of the ideal one; at two bits a lobe appears near minus eight degrees at about minus eight decibels, and the main beam has lost most of a decibel.

---

<!-- .slide: class="viz-cue-slide" -->

## Worked example — bits on the course array

Eight elements, $d/\lambda = 0.491$, steered to $15^\circ$:

| $B$ | LSB | Pointing step | $-6B$ rule | Worst sidelobe measured |
| :-- | :-- | :-- | :-- | :-- |
| 2 | $90^\circ$ | $29^\circ$ | $-12$ dB | $-6.7$ dB |
| 3 | $45^\circ$ | $14.6^\circ$ | $-18$ dB | $-12.8$ dB (the natural one) |
| 7 | $2.8125^\circ$ | $0.91^\circ$ | $-42$ dB | $-12.6$ dB (the natural one, as the 7-bit weights render it at $15^\circ$) |

<p class="viz-cue">↗ Interactive on the lesson page</p>

Note:
Demo on the kit: the Quantization section, Phase Shift Bits slider, with Use Bits ticked. Say up front what they will see — in sweep mode the same slider also coarsens the sweep grid, so at two bits the whole trace goes stair-stepped rather than showing a clean extra lobe. The clean version of the effect is the widget on the lesson page. Also note the fifteen degree coincidence: at this spacing the ideal ramp is about forty-six degrees per element, which three bits reproduce almost exactly, so three bits look free at this one angle and would not at another.

---

## Two different floors

<div class="two-col"><div class="col-text">

**Quantization does not cap a null.** Round the null weights onto the 2.8125&deg; grid with 1% gain steps and the notch is still about <strong>&minus;48 dB</strong> at its design angle. Rounding <em>moves</em> the notch a fraction of a degree; it does not fill it.

**The receiver caps what you can see.** The sweep's noise floor sits 23 dB under the uniform peak, and the null weights give up about 2 dB of main lobe.

</div><div class="col-fig">

| Floor | Set by | Value |
| :-- | :-- | :-- |
| Sidelobes | bits | $-6B$ dB |
| Pointing | LSB | 0.91° |
| Notch depth | quantization | −48 dB |
| Notch measured | noise floor | 20–22 dB |

</div></div>

Note:
This is the hook into the next two lessons. Correct the intuitive story before they build it: a cancellation is not limited by the phase resolution here. Quantized null weights still hold about minus forty-eight decibels at the designed angle. What they will measure in Lesson 28 is twenty-one decibels, and that number is the sweep's noise floor — twenty-three decibels below the uniform peak, less the two decibels of main lobe the null weights give up. The pattern goes deeper than the plot can show.

---

## Three departures, three cures

| Phenomenon | Cause | Predict it with | Design cure |
| :-- | :-- | :-- | :-- |
| Grating lobes | spacing too wide for the scan | $\sin\theta_g = \sin\theta_0 \pm m\lambda/d$ | $d < \lambda/(1+\vert\sin\theta_0\vert)$ |
| Beam squint | one phase setting across a band | $\Delta\theta \approx -(\Delta f/f_0)\tan\theta_0$ | true time delay |
| Quantization | finite phase steps | LSB $= 360^\circ/2^B$, QSLL $\approx -6B$ dB | more bits, or dither |

Dither breaks the periodicity of the rounding error, spreading it over many angles instead of one lobe — the same total error, a lower peak.

Note:
The summary table. Each row is a defect they have now seen on a plot and on the kit.

---

## Key point

<div class="callout">A steered array departs from the ideal pattern in three independent ways. <strong>Spacing</strong> decides whether a second beam exists, <strong>bandwidth</strong> decides where the beam actually points, and <strong>bits</strong> decide how far down the pattern floor goes. None of the three is an amplitude problem, so none of them is fixed by a taper.</div>

Note:
If they remember one slide, this is it. Three causes, three cures, none of them the taper they just learned.

---

## Where this is going

- **L27 — Null steering theory.** Stop shaping the beam as a whole and place a null exactly where an interferer sits. The weights come from subtracting one steering vector from another.
- **L28 — Null steering lab.** Enter those weights on the kit and measure the notch. It will read near 21 dB — not because quantization filled it, but because that is where the sweep's noise floor sits.

**Before L27:** be able to state the LSB of a $B$-bit shifter and the pointing step it implies on the course array, and review the complex element weights from L24.

Note:
Close by connecting quantization forward. Today it was a nuisance in the sidelobes; in L27 and L28 it is the number that decides whether the null is good enough.
