---
frame_view: true
---

# L23 - Beam Squint and Quantization

::::{frame}
:class: title-frame

<div class="course-mark">ECE 444 · Fall 2026</div>

<h1 class="frame-title">Beam Squint and Quantization</h1>

<div class="title-rule"></div>

Grating lobes, beam squint, and phase quantization, each with a number to design against.

Lesson 23 · Antennas, Phased Arrays, and Radar Systems · Dr. Neil Rogers
::::

::::{frame} Printing
:class: read-only

To print the slides, switch to present mode and print: one slide a sheet,
with room for notes. Print from read mode for the whole lesson.
::::

::::{frame} Learning Objectives
:class: here-23

<ol class="lo-list" style="--module: '3'; counter-reset: lo 7">
  <li>I can identify beam squint and quantization effects in a phased array and describe their impact on system performance.</li>
</ol>

```{include} ../../_snippets/m3-strip.md
```

:::{depth}
In Lesson 22 we controlled the sidelobes with amplitude weights. Three things can still put energy where we did not ask for it, and a taper fixes none of them: the **element spacing**, the **signal bandwidth**, and the **finite resolution of the phase shifters**. Each one produces a specific, predictable defect — a second full-height beam, a beam that moves with frequency, and a floor of sidelobes you cannot get below. This lesson gives you the number for each.
The L22–L23 Lab then measures all three on your own kit, against the numbers this
lesson derives, after its Part 1 has measured Lesson 22's tapers.
:::
::::

::::{frame} The Array Factor Repeats Every 2π
:::{present}
$$
\begin{aligned}
\psi &= kd\ (\sin\theta - \sin\theta_0) \\
AF_N(\psi) &= \frac{\sin(N\psi/2)}{N \sin(\psi/2)}
\end{aligned}
$$

- Shift $\psi$ by $2\pi$ and $\vert AF_N \vert$ is unchanged.
- Real angles reach a $2kd$-wide window, **visible space**; a repeat inside it is a **grating lobe**.
:::
:::{present}
<img src="../../viz/img/L23-visible-window.svg"
     alt="The array factor against its argument psi over two periods each side, with the window real angles reach shaded. Top: 14 mm and 8 elements, window plus or minus 173 degrees, the repeats at plus or minus 360 degrees outside it. Bottom: 42 mm and 3 elements, window plus or minus 519 degrees, both repeats inside it as full-height lobes"
     style="max-width: 640px; width: 100%; display: block; margin: 0 auto;">
:::

<a href="../L16-array-factor/index.html#frame-grating-lobes">Lesson 16</a> showed that the array factor repeats, and that a repeat reaching visible space is a grating lobe as tall as the main beam. This lesson turns that result into a design rule. Every array pattern in this module has been a function of one variable, Lesson 16's inter-element phase with Lesson 18's steering ramp subtracted,

$$\psi = kd\ (\sin\theta - \sin\theta_0),$$

and the uniform array factor built on it,

$$AF_N(\psi) = \frac{\sin(N\psi/2)}{N \sin(\psi/2)}.$$

Replace $\psi$ by $\psi + 2\pi$ and both sines flip sign together, so $\vert AF_N \vert$ is unchanged. The array factor is **periodic in $\psi$ with period $2\pi$**. The main lobe is the peak at $\psi = 0$, and the same peak reappears at $\psi = \pm 2\pi, \pm 4\pi, \ldots$ — every one of them a full-height beam.

Whether we ever see those repeats depends on how much of the $\psi$ axis the real angles $-90^\circ \le \theta \le +90^\circ$ reach. We call that span **visible space**, and the spacing sets its width: as $\sin\theta$ runs from $-1$ to $+1$, $\psi$ runs over a window of total width $2kd = 4\pi d/\lambda$. Widening $d$ brings more periods of the array factor into visible space. A repeat that lands inside visible space is a **grating lobe**. The figure draws both cases on the same axis: at $14\ \text{mm}$ the window stops at $\pm 173^\circ$, short of the repeats at $\pm 360^\circ$, and at $42\ \text{mm}$ it reaches $\pm 519^\circ$ and takes in both.
::::

::::{frame} The Grating Condition
:::{present}
$$
\sin\theta_g = \sin\theta_0 \pm m\ \frac{\lambda}{d}
$$

- $m$ is any positive integer.
- Any solution with $\vert\sin\theta_g\vert \le 1$ is a real beam.
:::
:::{present}
:class: callout

At $\theta_g$ every element is back in phase. A grating lobe is a second main beam, **full height**, and no taper lowers it.
:::

Set $\psi = 2\pi m$ and solve:

$$
\begin{aligned}
kd\ (\sin\theta_g - \sin\theta_0) &= 2\pi m \\
\sin\theta_g &= \sin\theta_0 \pm m\ \frac{\lambda}{d}
\end{aligned}
$$

for integer $m = 1, 2, \ldots$ Any solution with $\vert \sin\theta_g \vert \le 1$ is a real angle, and the array radiates a second beam there. The thinning example's figure shows why from the elements' side: at $43.9^\circ$ the fed elements of the $42\ \text{mm}$ row sit exactly one wavelength of path apart, so their phases read $0^\circ$, $360^\circ$ and $720^\circ$ and add exactly as they do at broadside.

:::{callout}
A grating lobe is not a sidelobe. At $\theta_g$ every element is back in phase — one full wavelength of path difference per element instead of zero — so the grating lobe is **exactly as tall as the main lobe**. Tapering does not reduce it, because the taper controls the sidelobe skirts of one beam and this is a second beam. Full height is an array-factor statement: <a href="../L21-antenna-pattern/index.html#frame-the-ideal-element">Lesson 21</a>'s element factor scales the lobe by $EF(\theta_g)$, which the $\cos\theta$ model puts $1.4$ dB down at $\pm 43^\circ$. The phaser-00 test run still read the lobes at full height.
:::
::::

::::{frame} Worked Example: Thinning the PHASER Row
:::{present}
- Feed every third patch: $d = 42$ mm, $\lambda/d = 0.693$ at $10.3$ GHz.
- Grating lobes at $\pm 43.9^\circ$: three full-height beams.
- Every fourth patch: $d = 56$ mm, lobes at $\pm 31.3^\circ$.
- A wide aperture with few elements gives a narrow but ambiguous beam.
:::
:::{present}
<img src="../../viz/img/L23-grating-whole-turn.svg"
     alt="Phase dials for a wave arriving from 43.9 degrees. Top: every third element, 42 mm apart, sees exactly one wavelength of extra path per element, so the dials read 0, 360 and 720 degrees and all point the same way. Bottom: all eight elements, 14 mm apart, see a third of a wavelength per element, so the dials step by 120 degrees and spread around the circle"
     style="max-width: 640px; width: 100%; display: block; margin: 0 auto;">
:::

:::{admonition} Worked example — thinning the PHASER row
:class: tip
The PHASER array is 8 patches on a $d = 14\ \text{mm}$ pitch. Feed only every third element and the fed elements sit $42\ \text{mm}$ apart. At the array's design center of $10.3\ \text{GHz}$, $\lambda = 29.1\ \text{mm}$, so $\lambda/d = 29.1/42 = 0.693$.

At broadside ($\theta_0 = 0$), the $m = 1$ solutions are

$$
\begin{aligned}
\sin\theta_g &= \pm 0.693 \\
\theta_g &= \pm 43.9^\circ.
\end{aligned}
$$

The $m = 2$ solutions need $\vert \sin\theta_g \vert = 1.386$, which is not a real angle, so there are exactly three full-height beams: $0^\circ$ and $\pm 44^\circ$. In the L22–L23 Lab, repeat the arithmetic at your own kit's Find HB100 frequency. On phaser-00, one of the course kits, a test run of the lab at $10.443\ \text{GHz}$ predicts $\pm 43.1^\circ$ and measured $-43.6^\circ$ and $+42.3^\circ$.

Feed every fourth element instead ($56\ \text{mm}$, $\lambda/d = 0.520$) and the pair moves in to $\pm 31.3^\circ$ ($\pm 30.8^\circ$ at $10.443\ \text{GHz}$, where phaser-00 measured $-33.0^\circ$ and $+29.8^\circ$), with the $m = 2$ repeat just past the horizon, at $\sin\theta = \pm 1.04$ — the pattern comes back to within a fraction of a dB of full height at $\pm 90^\circ$.
:::

Thinning has two effects. The three fed elements still span an $84\ \text{mm}$ aperture, so the main beam stays narrow, but with three elements instead of eight the array collects less signal and the pattern between the beams is poorly controlled. Each fed element adds the same voltage at the peak, so the peak falls by the fraction of elements fed, every third element and then every fourth:

$$
\begin{aligned}
20\log_{10}(3/8) &= -8.5\ \text{dB} \\
20\log_{10}(2/8) &= -12.0\ \text{dB}
\end{aligned}
$$

The phaser-00 test run measured $-7.8$ and $-10.9$ dB, about $1$ dB short of both. The same shortfall appears when the full array is compared with its single elements, and its cause is still open. The narrow beam of a large aperture with the ambiguity of a sparse one is the classic thinned-array trade.
::::

::::{frame} Keeping Grating Lobes Out
:::{present}
$$
d < \frac{\lambda}{1 + \vert \sin\theta_0 \vert}
$$

- Scan to $\pm 45^\circ$: $d < 0.586\lambda$. To $\pm 60^\circ$: $d < 0.536\lambda$.
- Any angle: $d < \lambda/2$, the default in every scanning array.
:::

We want no grating lobe anywhere in visible space, for every angle we intend to scan to. The dangerous solution is the one closest to the horizon on the far side of the beam. For a beam steered to positive $\theta_0$, that is $m = 1$ with the minus sign, and pushing it past the horizon requires

$$
\begin{aligned}
\sin\theta_0 - \frac{\lambda}{d} &< -1 \\
d &< \frac{\lambda}{1 + \vert \sin\theta_0 \vert}
\end{aligned}
$$

The wider we intend to scan, the closer together the elements must be. Broadside operation tolerates $d < \lambda$. Scanning to $\pm 45^\circ$ demands $d < 0.586\lambda$, and $\pm 60^\circ$ demands $d < 0.536\lambda$. Take the criterion to its limit, $\theta_0 \to 90^\circ$, and you get $d < \lambda/2$ — which is why **half-wavelength spacing is the default in every scanning array**. It is grating-lobe-free at any scan angle we can command.

```{note}
Grating lobes are not always a defect. Interferometers and sparse radio-astronomy arrays use them on purpose, resolving fine detail with a small number of widely spaced elements and removing the ambiguity by other means. A designer can choose grating lobes; they should never be found after the array is built.
```
::::

::::{frame} The PHASER Has No Grating Lobe
:::{present}
- Worst case is the shortest $\lambda$: $10.5$ GHz, $\lambda/d = 28.6/14 = 2.04$.
- Needs $\vert\sin\theta_0\vert < 1.04$: every real angle passes.
- The $14$ mm pitch is $0.49\lambda$, just inside the half-wavelength rule.
:::

:::{admonition} Worked example — is the PHASER safe?
:class: tip
Use the highest frequency the array is specified for, $10.5\ \text{GHz}$, because $\lambda$ is shortest there and the criterion is tightest: $\lambda = 28.6\ \text{mm}$, so $\lambda/d = 28.6/14 = 2.04$.

The criterion requires $1 + \vert\sin\theta_0\vert < \lambda/d = 2.04$, or $\vert\sin\theta_0\vert < 1.04$. Every real angle satisfies that, so the array has **no grating lobe at any scan angle in its band**. The $14\ \text{mm}$ pitch is $0.49\lambda$ at the band edge, chosen to sit just inside the half-wavelength rule.
:::
::::

::::{frame} Phase Is Set at One Frequency
:::{present}
$$
\begin{aligned}
kd \sin\theta &= k_0 d \sin\theta_0 \\
\sin\theta &= \frac{f_0}{f}\sin\theta_0
\end{aligned}
$$

- The phase ramp is computed once, at $f_0$.
- A signal at another frequency adds in phase at another angle.
:::
:::{present}
<img src="../../viz/img/L23-squint-ramp.svg"
     alt="Left: the phase lag the shifters apply across the eight elements, set for 45 degrees at 10.525 GHz, against the lag a 10.025 GHz signal needs at 45 degrees. Right: their difference grows by 5.9 degrees per element, a straight ramp"
     style="max-width: 700px; width: 100%; display: block; margin: 0 auto;">
:::

The beam-steering computer sets each phase shifter once, in degrees. The angle that setting steers to is not fixed, because the phase a given path length produces depends on frequency. The figure shows the result across the aperture for the worked example below: the shifters apply $125.1^\circ$ per element, set for $45^\circ$ at $10.525\ \text{GHz}$, and a $10.025\ \text{GHz}$ signal needs $119.2^\circ$ per element to add in phase at $45^\circ$. The difference, $5.9^\circ$ per element, is itself a straight ramp, and a straight ramp is a steer: the beam moves to a new angle and stays intact. <a href="../L18-beam-steering/index.html#frame-time-delay-versus-phase-delay">Lesson 18</a> named the result, beam squint, and the <a href="../L18-lab-beam-steering/index.html#frame-part-3-the-peak-angle-error-budget">L18 Lab</a> showed it once on the kit; here we compute it.

Suppose the beam-steering computer sets element $n$ to a lag of $n\ k_0 d \sin\theta_0$, computed at the design frequency $f_0$ where $k_0 = 2\pi/\lambda_0$. Now a signal arrives at some other frequency $f$ in the band. The elements add in phase toward whatever angle $\theta$ makes the arrival phase cancel the applied lag:

$$
\begin{aligned}
kd \sin\theta &= k_0 d \sin\theta_0 \\
\sin\theta &= \frac{\lambda}{\lambda_0}\sin\theta_0 \\
&= \frac{f_0}{f}\sin\theta_0,
\end{aligned}
$$
::::

::::{frame} The Squint Formula
:::{present}
$$
\begin{aligned}
\Delta\theta &= \arcsin\!\left(\frac{f_0}{f}\sin\theta_0\right) - \theta_0 \\
&\approx -\delta\ \tan\theta_0, \qquad \delta = \frac{f - f_0}{f_0}
\end{aligned}
$$

- No $N$, no $d$: only $f_0/f$ survives.
- Zero at broadside, fastest at wide scan.
:::

so the beam points at

$$\boxed{\ \Delta\theta = \arcsin\!\left(\frac{f_0}{f}\sin\theta_0\right) - \theta_0\ }$$

away from the commanded angle.

This is **beam squint**. It does not depend on $N$ or on $d$ — the phase ramp and the path lengths scale together, and only the ratio $f_0/f$ survives. It vanishes at broadside, where the ramp is zero and there is nothing to scale. For small fractional offsets $\delta = (f - f_0)/f_0$, expanding the arcsine gives the small-offset form:

$$\Delta\theta \approx -\delta\ \tan\theta_0 \quad \text{(radians).}$$

The beam moves toward the horizon as the frequency drops, and it moves fastest when the beam is already far off broadside.
::::

::::{frame} Worked Example: Squint on the PHASER
:::{present}
- Phases set for $45^\circ$ at $10.525$ GHz; the signal arrives $500$ MHz lower.
- The beam lands at $47.9^\circ$: $+2.9^\circ$ of squint, $0.25$ dB lost at the aimpoint.
- $1$ GHz off: $6.4^\circ$, a third of a beam, $1.0$ dB.
:::

:::{admonition} Worked example — squint on the PHASER
:class: tip
Phases are set for $\theta_0 = 45^\circ$ at the HB100's $f_0 = 10.525\ \text{GHz}$. A signal arrives $500\ \text{MHz}$ lower, at $10.025\ \text{GHz}$:

$$
\begin{aligned}
\sin\theta &= \frac{10.525}{10.025}\ \sin 45^\circ \\
&= 1.0499 \times 0.7071 = 0.7424 \\
\theta &= 47.9^\circ.
\end{aligned}
$$

The beam has squinted $\Delta\theta = +2.9^\circ$. The small-offset form, with $\delta = -0.0475$ and $\tan 45^\circ = 1$, gives

$$\Delta\theta \approx 0.0475\ \text{rad} = 2.7^\circ,$$

close enough for a budget. This is the $+3^\circ$ your **Angle** readout will move in the L22–L23 Lab when the Signal BW goes from 10 to 500 MHz: the GUI sets the phases 500 MHz below the signal, so the sweep has to command $47.9^\circ$ to land on a source at $45^\circ$. The phaser-00 test run agreed: with the source at $41.1^\circ$, the prediction is $+2.6^\circ$ and phaser-00 measured $+2.5^\circ$.

At $45^\circ$ the beam is $18.7^\circ$ wide (Lesson 20's $13.2^\circ/\cos 45^\circ$), so $2.9^\circ$ of squint loses only $0.25\ \text{dB}$ at the aimpoint. That loss is the array factor evaluated at the aimpoint, which now sits off the beam's peak. At $10.025\ \text{GHz}$, $kd = 2.94$ rad, and the aimpoint's $\sin\theta$ sits $\sin 45^\circ - \sin 47.9^\circ = -0.0353$ from the peak's:

$$
\begin{aligned}
\psi &= 2.94 \times (-0.0353) \\
&= -0.104\ \text{rad} \\
\vert AF_8(\psi) \vert &= 0.972 \\
&= -0.25\ \text{dB}
\end{aligned}
$$
 At a $1\ \text{GHz}$ offset the squint reaches $6.4^\circ$, roughly a third of a beamwidth, and the loss grows to $1.0\ \text{dB}$.
:::
::::

::::{frame} Why Squint Matters
:::{present}
- **Wideband radar**: each frequency in the pulse points somewhere else, so the beam smears and depoints.
- **Communications**: gain falls at the band edges, a tilt across the channel.
:::

Squint affects two kinds of system differently. A **wideband radar** transmits a pulse whose spectrum is the bandwidth; each frequency component in that pulse points somewhere slightly different, so the pulse's energy is spread in angle and the effective beam is broadened and depointed. A **communications link** running a modulated carrier loses gain at the band edges relative to the center, which shows up as amplitude tilt across the channel rather than as an angle error.
::::

::::{frame} True Time Delay
:::{present}
$$
\tau_n = \frac{n\ d \sin\theta_0}{c}
$$

- A delay matches a path length at every frequency: no squint.
- Delay is costly, so large arrays delay per subarray and phase-shift inside each one.
:::

The cure is to stop steering with phase. If instead of a phase lag you insert a **true time delay** of $\tau_n = n\ d \sin\theta_0 / c$ in each element, the delay compensates the geometric path difference itself, which is a length and not a phase. Every frequency in the band then arrives in phase at the same angle, and the squint is gone at all offsets. True time delay is expensive in analog hardware, which is why large wideband arrays usually compromise: time delay at the level of the **subarray** (a group of elements combined before the rest, as on the PHASER's two four-element halves in <a href="../L17-phased-array-hardware/index.html#frame-the-hybrid-beamformer">Lesson 17</a>) to control the squint across the aperture, phase shifters inside each subarray where the residual path differences are small.
::::

::::{frame} Phase Quantization
:::{present}
$$
\text{LSB} = \frac{360^\circ}{2^B}
$$

- ADAR1000: $B = 7$, 128 states, LSB $= 2.8125^\circ$.
- Rounding to that grid coarsens the pointing and adds sidelobes.
:::

The ADAR1000 does not accept an arbitrary phase. It has a $B$-bit phase shifter, and $B$ bits divide the circle into $2^B$ steps. The smallest step, one **least significant bit (LSB)**, is the grid <a href="../L18-beam-steering/index.html#frame-phase-shifter-resolution">Lesson 18</a> rounded its $30^\circ$ phase table onto:

$$\text{LSB} = \frac{360^\circ}{2^B}.$$

The ADAR1000 uses $B = 7$, giving 128 states and an LSB of $2.8125^\circ$.
The ADAR1000 rounds every commanded phase to that grid, which has two
consequences.
::::

::::{frame} Pointing Granularity
:::{present}
$$
\Delta\theta_0 \approx \frac{\text{LSB}}{360^\circ\ (d/\lambda)}\ \text{rad}
$$

- PHASER: $0.91^\circ$ at broadside, one-fourteenth of a beam.
- Grows as $1/\cos\theta_0$: $1.8^\circ$ at $60^\circ$.
- 2 bits: $29^\circ$ steps, so broadside and about $\pm 31^\circ$ only.
:::

The inter-element phase for a beam at $\theta_0$ is $\Delta\phi = 360^\circ (d/\lambda) \sin\theta_0$. If the controller can only command multiples of the LSB, only a discrete set of beam angles exists:

$$\sin\theta_0 = \frac{m\ \text{LSB}}{360^\circ\ (d/\lambda)},$$

so the step near broadside is

$$\Delta\theta_0 \approx \frac{\text{LSB}}{360^\circ\ (d/\lambda)}\ \text{rad}.$$

For the PHASER at $10.525\ \text{GHz}$, $d/\lambda = 0.491$, so the step is $2.8125/(360 \times 0.491) = 0.0159\ \text{rad} = 0.91^\circ$ at broadside. Compared with the $13.2^\circ$ beamwidth that is about one-fourteenth of a beam, which is fine. Off broadside the same step in $\sin\theta_0$ spans a wider angle, because $\Delta(\sin\theta_0) = \cos\theta_0\ \Delta\theta_0$. The step therefore grows as $1/\cos\theta_0$, reaching $1.8^\circ$ at $60^\circ$. Drop to $B = 2$ and the same calculation gives $29^\circ$ per step: a 2-bit array can only point at broadside and at about $\pm 31^\circ$.
::::

::::{frame} Quantization Sidelobes
:::{present}
$$
\text{QSLL} \approx -6B\ \text{dB}
$$

- Rounding leaves a periodic sawtooth phase error, and it radiates a lobe.
- Rule: 2 bits $-12$ dB, 3 bits $-18$, 4 bits $-24$.
- Phaser-00 measured $-8.5$, $-12.0$, and $-15.5$ dBc: above the rule.
:::
:::{present}
<img src="../../viz/img/L23-quant-staircase.svg"
     alt="Top: the exact phase ramp for a beam at 28 degrees and the 3-bit staircase the shifters can set, in steps of 45 degrees. Bottom: the rounding error at each element, never more than 22.5 degrees either way, rising and falling across the aperture"
     style="max-width: 640px; width: 100%; display: block; margin: 0 auto;">
:::

A real controller does better than a uniform quantized increment. It computes the exact ramp for every element, then rounds each element independently, which puts the beam much closer to the commanded angle. What is left behind is a staircase: the difference between the exact ramp and the rounded one is a sawtooth error, bounded by half an LSB, that repeats across the aperture. A periodic phase error radiates, and where it radiates is a **quantization sidelobe**. The figure shows the staircase for a beam at $28^\circ$ with 3 bits: the exact ramp climbs $83.1^\circ$ per element, the shifters can only set multiples of $45^\circ$, and the error left at each element rises and falls within $\pm 22.5^\circ$.

Its level follows from the size of the error. Rounding leaves at most half an LSB at each element. For a small phase error $e^{j\phi} \approx 1 + j\phi$, so the error adds a small field to each element in proportion to $\phi$, and the lobe that field radiates scales with the sawtooth's peak:

$$
\begin{aligned}
\phi_\text{max} &= \frac{\text{LSB}}{2} = \frac{\pi}{2^B}\ \text{rad} \\
\frac{E_\text{lobe}}{E_\text{beam}} &\approx \frac{\phi_\text{max}}{\pi} = 2^{-B} \\
\text{QSLL} &= 20\log_{10} 2^{-B} = -6.02B\ \text{dB}
\end{aligned}
$$

Each extra bit halves the error, which halves the lobe's field and lowers the **quantization sidelobe level (QSLL)** by $6$ dB. That gives the rule of thumb, so 2 bits puts a lobe near $-12$ dB, 3 bits near $-18$ dB, and the ADAR1000's 7 bits near $-42$ dB. Treat this as an RMS estimate for a large array. On an aperture as short as eight elements there are only a couple of sawtooth periods, so individual lobes scatter several dB either side of the rule. Taken at face value, the rule says that from 3 bits up the quantization lobes drop below the array's own $-13$ dB sidelobes and no longer set the sidelobe level.

The hardware disagrees. In the phaser-00 test run, with the source fixed, the kit read the strongest lobe beyond $\pm 35^\circ$ at $-8.5$ dBc with 2 bits, $-12.0$ dBc with 3, $-15.5$ dBc with 4, and $-17.4$ dBc, the floor of that sweep, with 7. Every reading sits above the rule, by $3.5$ dB at 2 bits and by $6$ to $8.5$ dB at 3 and 4 bits, so on this kit 3 bits is not enough to hide the quantization lobes under the $-13$ dB sidelobes. The **Angle** readout moved too: it read $+8.4^\circ$ at 4, 3, and 2 bits against $+1.8^\circ$ at 7, several times the pointing step derived above. The cause of the extra error has not been confirmed. At low bit counts, read the lobe levels on the sweep rather than the Angle readout.

<img src="../../viz/img/L23-qsll-vs-bits.svg"
     alt="Worst lobe in dB below the beam against phase-shifter bits from 2 to 7: the minus 6B rule; the simulated worst quantization lobe on the course array over steer angles 0 to 50 degrees, about 4 dB above the rule at every bit count; the uniform array's own sidelobes at minus 13.3 dB; and the phaser-00 readings, minus 8.5, minus 12.0 and minus 15.5 dBc at 2, 3 and 4 bits, with the sweep floor at 7 bits"
     style="max-width: 600px; width: 100%; display: block; margin: 0 auto;">

The figure adds a third curve: the worst quantization lobe the course array can produce at any steer angle up to $50^\circ$, computed from the field the rounding error radiates on its own. It sits about $4$ dB above the rule at every bit count, because the rule is an average for a large array and eight elements leave room for a worst case. That accounts for the 2-bit reading, $-8.3$ dB simulated against $-8.5$ dBc measured. The 3- and 4-bit readings still sit $2.5$ and $4.7$ dB above even the worst case, so rounding the steering ramp does not explain them by itself.

More bits improve two things: finer pointing, which scales as the LSB, and a lower sidelobe floor, which scales as $6$ dB per bit. Seven bits is the standard choice because it puts the quantization floor far below every other error in the array.
::::

::::{frame} Dither
:::{present}
- The same sawtooth on every beam position radiates coherently into one lobe.
- A small known offset per element before rounding breaks the period.
- The same error spreads over many angles: a lower peak lobe, no new hardware.
:::

Dither lowers the peak quantization lobe without new hardware. If the rounding error is the same sawtooth on every beam position, it radiates coherently into one lobe. Adding a small known phase offset per element before rounding breaks the periodicity, which spreads the same total error energy over many angles instead of concentrating it in one.
::::

::::{frame} Null Depth: Predicted and Measured
:::{present}
:class: callout

- Quantization alone still allows a $-48$ dB null.
- Our sweep-floor estimate capped measured nulls near $21$ dB.
- Phaser-00 measured $-40$ to $-50$ dB nulls in L24, but sweep floors from $-17$ to $-31$ dBc.
:::

One thing quantization does *not* set is how deep a null can go. It is tempting to assume that a cancellation is only as good as the phase resolution behind it, but the LSB does not limit the null weights: rounding them to a $2.8125^\circ$ grid with 1% gain steps still produces a notch near $-48$ dB at the angle it was designed for. What rounding does instead is move the notch a fraction of a degree off its commanded angle, which is a pointing effect, not a depth effect.

Our first estimate of the measured limit came from the receiver. Earlier sweeps on the PHASER showed a noise floor about $23$ dB below the uniform-taper peak, and the weights that create a null reduce the main-lobe gain by about $2$ dB, so we expected a sweep to show nothing deeper than about $21$ dB below the new peak.

The phaser-00 test run did not bear that out. In the L24 Lab the notch reached $-46$ to $-50$ dB below the uniform peak, the difference null $-41.5$ dB, and the delta null $-39.7$ dBc. The deepest of these sits close to the $-48$ dB that quantization alone allows, so on that kit the sweep followed the pattern most of the way down. The same session's L22–L23 Lab sweeps, however, read floors between $-17$ and $-31$ dBc, and a wall or a person beside the kit raised lobes as high as $-9$ dBc. The floor a sweep shows is therefore not one fixed number: it changed from lab to lab on the same kit, and the bench around the kit changed it further.

:::{callout}
Separate the two limits. **Quantization** sets a sidelobe floor at roughly $-6B$ dB and a pointing granularity of about one LSB, and on the course array it still allows a $-48$ dB null. The **floor of the measurement** sets what you can observe. We predicted that floor would cap a measured null near $21$ dB; on phaser-00 the L24 nulls reached $-40$ to $-50$ dB, while the L22–L23 sweeps on the same kit read floors from $-17$ to $-31$ dBc. A shallow measured null points to the bench first, not to the phase shifter.
:::
::::

::::{frame} Three Departures on the Course Array
:class: viz-frame

:::{depth}
The widget's left panel is the pattern; its right panel shows why the pattern looks that way. At the two angles marked 1 and 2 on the pattern, it adds the eight element contributions head to tail, the same sum Lesson 22 drew for the first sidelobe, and the chain's length is the level at that angle. Start in **Grating** at $14\ \text{mm}$: the chain at the sidelobe curls almost shut. Step to $42\ \text{mm}$ and the chain at $43.9^\circ$ comes out straight, because each fed element is a whole turn behind its neighbor. Switch to **Squint** and drag the offset: the chain at the commanded $45^\circ$ bends into an arc, while the chain at the new peak is straight, so the beam has moved rather than broken. Switch to **Quantization**, set 3 bits, and move the steer angle: at $15^\circ$ the ramp lands almost exactly on the $45^\circ$ grid and nothing changes, while at $28^\circ$ the rounding error lines the chain up partway and a lobe rises to $-9$ dB. Whether rounding matters depends on how the ramp falls on the grid, not only on the number of bits.
:::

:::{present}
<iframe src="../../viz/squint-quantization.html"
        width="100%" height="424"
        style="border: 1px solid #cddce9; border-radius: 6px;"
        loading="lazy"
        title="Grating lobes, beam squint and phase quantization on the 8-element course array">
</iframe>
:::
::::

::::{frame} Three Departures, Three Cures
:::{present}
| Departure | Set by | Cure |
| :-- | :-- | :-- |
| Grating lobe | $\lambda/d$ | $d \le \lambda/2$ |
| Beam squint | $\delta\ \tan\theta_0$ | True time delay |
| Pointing step | the LSB | More bits |
| Quantization lobe | $-6B$ dB | More bits, dither |
:::

The three failures look different on a sweep and a designer fixes each one in a different place.

| Phenomenon | Cause | Predict it with | Design cure |
| :-- | :-- | :-- | :-- |
| Grating lobe | Element spacing too wide for the scan range | $\sin\theta_g = \sin\theta_0 \pm m\lambda/d$ | Keep $d < \lambda/(1+\vert\sin\theta_0\vert)$; $d \le \lambda/2$ is safe everywhere |
| Thinned-array ambiguity | Feeding a subset of a filled aperture | Same criterion, using the effective spacing | Fill the aperture, or accept and resolve the ambiguity |
| Beam squint | One phase setting used across a band | $\Delta\theta = \arcsin((f_0/f)\sin\theta_0) - \theta_0$ | True time delay, at the element or the subarray |
| Pointing granularity | Finite phase steps in the beam-steering command | $\Delta\theta_0 \approx \text{LSB}/(360^\circ d/\lambda)$ | More bits |
| Quantization sidelobes | Staircase error left after rounding the ramp | $\text{QSLL} \approx -6B$ dB | More bits, or dither the rounding across elements |
::::

::::{frame} Summary: Grating Lobes
:class: read-only

| Symbol / idea | What it is | Number to remember |
| :-- | :-- | :-- |
| $\sin\theta_g = \sin\theta_0 \pm m\lambda/d$ | Grating-lobe angles, from the $2\pi$ periodicity of the array factor | $42\ \text{mm}$ at $10.3\ \text{GHz}$ gives $\pm 43.9^\circ$; $56\ \text{mm}$ gives $\pm 31.3^\circ$ |
| $d < \lambda/(1+\vert\sin\theta_0\vert)$ | Spacing that keeps grating lobes out of visible space | $d \le \lambda/2$ is safe at every scan angle |
| Grating-lobe height | It is a second main lobe, not a sidelobe | Equal to the main beam; a taper does not reduce it |
::::

::::{frame} Summary: Beam Squint
:class: read-only

| Symbol / idea | What it is | Number to remember |
| :-- | :-- | :-- |
| $\Delta\theta = \arcsin((f_0/f)\sin\theta_0) - \theta_0$ | Beam squint when the signal is off the phase-set frequency | $500\ \text{MHz}$ at $45^\circ$ gives $+2.9^\circ$ |
| $\Delta\theta \approx -(\Delta f/f_0)\tan\theta_0$ | Small-offset squint, for a budget | Zero at broadside, worst at wide scan |
| True time delay | Delays the signal instead of rotating its phase | Removes squint at all offsets |
::::

::::{frame} Summary: Quantization
:class: read-only

| Symbol / idea | What it is | Number to remember |
| :-- | :-- | :-- |
| $\text{LSB} = 360^\circ/2^B$ | Phase step of a $B$-bit shifter | ADAR1000: $B = 7$, LSB $= 2.8125^\circ$ |
| $\Delta\theta_0 \approx \text{LSB}/(360^\circ d/\lambda)$ | Pointing granularity near broadside | $0.91^\circ$ on the PHASER, one-fourteenth of a beam |
| $\text{QSLL} \approx -6B$ dB | Quantization sidelobe rule of thumb | 2 bits gives $-12$ dB; 7 bits gives $-42$ dB; phaser-00 read $-8.5$ dBc at 2 bits and $-12.0$ at 3 |
::::

::::{frame} Practice
:class: read-only doc-links

- <a class="doc-link" href="../../practice/ECE444_L23_Practice_blank.pdf" target="_blank" rel="noopener">Problem set (PDF)</a>
- <a class="doc-link doc-key" href="../../practice/ECE444_L23_Practice_SOLUTIONS.pdf" target="_blank" rel="noopener">Solutions (PDF)</a>
::::

::::{frame} Looking Ahead
:::{present}
- The L22–L23 Lab measures all three departures on your own kit.
- L24 places a null: quantization nudges it; phaser-00 measured $-40$ to $-50$ dB.
- Bring the LSB of a $B$-bit shifter, its pointing step, and the weights $w_n$.
:::

Part 2 of the [L22–L23 Lab](../L22-L23-lab-tapering-squint/index.md) measures all three of today's departures on your own kit. Lesson 24 then extends pattern control from the whole beam to one chosen angle. So far you have shaped the beam and the sidelobes as a whole; next you will place a null at a chosen angle on purpose, which is what an array does when a jammer or an interfering transmitter sits somewhere you know about. The weights come from subtracting one steering vector from another, and the arithmetic is short.

Both of today's floors appear again in L24. Quantization moves the notch slightly off its commanded angle without filling it, and the floor of the sweep decides how much of the notch you can see. We predicted a measured depth near $21$ dB; phaser-00 reached $-40$ to $-50$ dB, so in the L24 Lab compare your own notch against both numbers. Before Lesson 24, be able to state the LSB of a $B$-bit shifter and the pointing step it implies on the course array, and review the complex element weights $w_n$ from Lesson 22 — the null-steering result is written entirely in that notation.
::::
