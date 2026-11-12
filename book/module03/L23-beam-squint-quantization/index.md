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
  <li>I can identify grating lobes, beam squint, and quantization effects in a phased array and describe their impact on system performance.</li>
</ol>

```{include} ../../_snippets/m3-strip.md
```

:::{depth}
In Lesson 22 we controlled the sidelobes with amplitude weights. Three things can still put energy where we did not ask for it, and a taper fixes none of them: the element spacing, the signal bandwidth, and the finite resolution of the phase shifters. Each one produces a specific, predictable defect — a second full-height beam, a beam that moves with frequency, and a floor of sidelobes you cannot get below. This lesson gives you the number for each.
The L22–L23 Lab then measures all three on your own kit, against the numbers this
lesson derives, after it has measured Lesson 22's tapers.
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
     alt="The array factor against its argument psi over two periods each side, with the window real angles reach shaded. Top: 14 mm and 8 elements at 10.0 GHz, window plus or minus 168 degrees, the repeats at plus or minus 360 degrees outside it. Bottom: 42 mm and 3 elements, window plus or minus 504 degrees, both repeats inside it as full-height lobes"
     style="max-width: 640px; width: 100%; display: block; margin: 0 auto;">
:::

<a href="../L16-array-factor/index.html#frame-grating-lobes">Lesson 16</a> showed that the array factor repeats, and that a repeat reaching visible space is a grating lobe as tall as the main beam. This lesson turns that result into a design rule. Every array pattern in this module has been a function of one variable, Lesson 16's inter-element phase with Lesson 18's steering ramp subtracted,

$$\psi = kd\ (\sin\theta - \sin\theta_0),$$

and the uniform array factor built on it,

$$AF_N(\psi) = \frac{\sin(N\psi/2)}{N \sin(\psi/2)}.$$

Replace $\psi$ by $\psi + 2\pi$ and both sines flip sign together, so $\vert AF_N \vert$ is unchanged. The array factor is periodic in $\psi$ with period $2\pi$. The main lobe is the peak at $\psi = 0$, and the same peak reappears at $\psi = \pm 2\pi, \pm 4\pi, \ldots$ — every one of them a full-height beam.

Whether we ever see those repeats depends on how much of the $\psi$ axis the real angles $-90^\circ \le \theta \le +90^\circ$ reach. We call that span **visible space**, and the spacing sets its width: as $\sin\theta$ runs from $-1$ to $+1$, $\psi$ runs over a window of total width $2kd = 4\pi d/\lambda$. Widening $d$ brings more periods of the array factor into visible space. A repeat that lands inside visible space is a **grating lobe**. The figure draws both cases on the same axis at $10.0\ \text{GHz}$: at $14\ \text{mm}$ the window stops at $\pm 168^\circ$, short of the repeats at $\pm 360^\circ$, and at $42\ \text{mm}$ it reaches $\pm 504^\circ$ and takes in both.
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

for integer $m = 1, 2, \ldots$ Any solution with $\vert \sin\theta_g \vert \le 1$ is a real angle, and the array radiates a second beam there. The thinning example's figure shows why from the elements' side: at $45.6^\circ$ the fed elements of the $42\ \text{mm}$ row sit exactly one wavelength of path apart, so their phases read $0^\circ$, $360^\circ$ and $720^\circ$ and add exactly as they do at broadside.

:::{callout}
A grating lobe is not a sidelobe. At $\theta_g$ every element is back in phase — one full wavelength of path difference per element instead of zero — so the grating lobe is exactly as tall as the main lobe. Tapering does not reduce it, because the taper controls the sidelobe skirts of one beam and this is a second beam. Full height is an array-factor statement: <a href="../L21-antenna-pattern/index.html#frame-gain-of-the-course-array">Lesson 21</a>'s element factor scales the lobe by $EF(\theta_g)$, which the $\cos\theta$ model puts $1.6$ dB down at $\pm 46^\circ$. On my kit the lobes still read at full height.
:::
::::

::::{frame} Worked Example: Thinning the PHASER Row
:::{present}
- Feed every third patch: $d = 42$ mm, $\lambda/d = 0.714$ at $10.0$ GHz.
- Grating lobes at $\pm 45.6^\circ$: three full-height beams.
- Every fourth patch: $d = 56$ mm, lobes at $\pm 32.4^\circ$.
- A wide aperture with few elements gives a narrow but ambiguous beam.
:::
:::{present}
<img src="../../viz/img/L23-grating-whole-turn.svg"
     alt="Phase dials for a wave arriving from 45.6 degrees, at 10.0 GHz. Top: every third element, 42 mm apart, sees exactly one wavelength of extra path per element, so the dials read 0, 360 and 720 degrees and all point the same way. Bottom: all eight elements, 14 mm apart, see a third of a wavelength per element, so the dials step by 120 degrees and spread around the circle"
     style="max-width: 640px; width: 100%; display: block; margin: 0 auto;">
:::

:::{admonition} Worked example — thinning the PHASER row
:class: tip
The PHASER array is 8 patches on a $d = 14\ \text{mm}$ pitch. Feed only every third element and the fed elements sit $42\ \text{mm}$ apart. At $10.0\ \text{GHz}$, $\lambda = 30.0\ \text{mm}$, so $\lambda/d = 30.0/42 = 0.714$.

At broadside ($\theta_0 = 0$), the $m = 1$ solutions are

$$
\begin{aligned}
\sin\theta_g &= \pm 0.714 \\
\theta_g &= \pm 45.6^\circ.
\end{aligned}
$$

The $m = 2$ solutions need $\vert \sin\theta_g \vert = 1.43$, which is not a real angle, so there are exactly three full-height beams: $0^\circ$ and $\pm 46^\circ$. Part 1 of the L22–L23 Lab packet repeats the arithmetic at your own kit's Find HB100 frequency.

Feed every fourth element instead ($56\ \text{mm}$, $\lambda/d = 0.536$) and the pair moves in to $\pm 32.4^\circ$, with the $m = 2$ repeat just past the horizon, at $\sin\theta = \pm 1.07$, so the pattern climbs back to within $0.8$ dB of full height at $\pm 90^\circ$.
:::

Thinning has two effects. The three fed elements still span an $84\ \text{mm}$ aperture, so the main beam stays narrow, but with three elements instead of eight the array collects less signal and the pattern between the beams is poorly controlled. Each fed element adds the same voltage at the peak, so the peak falls by the fraction of elements fed, every third element and then every fourth:

$$
\begin{aligned}
20\log_{10}(3/8) &= -8.5\ \text{dB} \\
20\log_{10}(2/8) &= -12.0\ \text{dB}
\end{aligned}
$$

The narrow beam of a large aperture with the ambiguity of a sparse one is the classic thinned-array trade.
::::

::::{frame} Keeping Grating Lobes Out
:::{present}
$$
d < \frac{\lambda}{1 + \vert \sin\theta_0 \vert}
$$

- Scan to $\pm 45^\circ$: $d < 0.586\lambda$. To $\pm 60^\circ$: $d < 0.536\lambda$.
- Any angle: $d < \lambda/2$, the default in every scanning array.
:::
:::{present}
<img src="../../viz/img/L16-grating-limit.svg"
     alt="Largest grating-lobe-free scan angle against element spacing in wavelengths: the boundary runs from 1.0 wavelength at broadside down to 0.5 wavelength at 90 degrees, with the PHASER's spacing marked inside the safe region and the 45 degree scan limit at 0.586 marked"
     style="max-width: 640px; width: 100%; display: block; margin: 0 auto;">
:::

We want no grating lobe anywhere in visible space, for every angle we intend to scan to. The dangerous solution is the one closest to the horizon on the far side of the beam. For a beam steered to positive $\theta_0$, that is $m = 1$ with the minus sign, and pushing it past the horizon requires

$$
\begin{aligned}
\sin\theta_0 - \frac{\lambda}{d} &< -1 \\
d &< \frac{\lambda}{1 + \vert \sin\theta_0 \vert}
\end{aligned}
$$

The wider we intend to scan, the closer together the elements must be. Broadside operation tolerates $d < \lambda$. Scanning to $\pm 45^\circ$ demands $d < 0.586\lambda$, and $\pm 60^\circ$ demands $d < 0.536\lambda$. Take the criterion to its limit, $\theta_0 \to 90^\circ$, and you get $d < \lambda/2$ — which is why half-wavelength spacing is the default in every scanning array. It is grating-lobe-free at any scan angle we can command. The figure, from Lesson 16, draws the criterion as a boundary: any spacing and scan angle below the curve is free of grating lobes, and the PHASER's $14\ \text{mm}$ pitch, under half a wavelength at every kit frequency, sits below it everywhere.

```{note}
Grating lobes are not always a defect. Interferometers and sparse radio-astronomy arrays use them on purpose, resolving fine detail with a small number of widely spaced elements and removing the ambiguity by other means. A designer can choose grating lobes; they should never be found after the array is built.
```
::::

::::{frame} The PHASER Has No Grating Lobe
:::{present}
- At $10.0$ GHz, $\lambda/d = 30.0/14 = 2.14$.
- Needs $\vert\sin\theta_0\vert < 1.14$: every real angle passes.
- $14$ mm is half a wavelength at $10.7$ GHz, the top of the HB100 range.
:::

:::{admonition} Worked example — is the PHASER safe?
:class: tip
At $10.0\ \text{GHz}$, $\lambda = 30.0\ \text{mm}$, so $\lambda/d = 30.0/14 = 2.14$.

The criterion requires $1 + \vert\sin\theta_0\vert < \lambda/d = 2.14$, or $\vert\sin\theta_0\vert < 1.14$. Every real angle satisfies that, so the array has no grating lobe at any scan angle. The margin shrinks as the frequency rises and $\lambda$ shortens, and it runs out where $d = \lambda/2$: $14\ \text{mm}$ is half a wavelength at $10.7\ \text{GHz}$, so the full row shows no grating lobe at any HB100 frequency, $10.1$ to $10.7\ \text{GHz}$.
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
     alt="Left: the phase lag the shifters apply across the eight elements, set for 45 degrees at 9.5 GHz, against the lag a 10.0 GHz signal needs at 45 degrees. Right: their difference grows by 5.9 degrees per element, a straight ramp"
     style="max-width: 700px; width: 100%; display: block; margin: 0 auto;">
:::

The beam-steering computer sets each phase shifter once, in degrees. The angle that setting steers to is not fixed, because the phase a given path length produces depends on frequency. The figure shows the result across the aperture for a signal at $10.0\ \text{GHz}$ with the phases computed $500\ \text{MHz}$ below it, which is what the GUI's **Signal BW** setting does: the shifters apply $112.9^\circ$ per element, set for $45^\circ$ at $9.5\ \text{GHz}$, and the $10.0\ \text{GHz}$ signal needs $118.8^\circ$ per element to add in phase at $45^\circ$. The difference, $5.9^\circ$ per element, is itself a straight ramp, and a straight ramp is a steer: the beam moves to a new angle and stays intact. <a href="../L18-beam-steering/index.html#frame-time-delay-versus-phase-delay">Lesson 18</a> named the result, beam squint, and the <a href="../L18-lab-beam-steering/index.html">L18 Lab</a> showed it once on the kit; here we compute it.

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

A signal above $f_0$ has $f_0/f < 1$, and the beam moves toward broadside; a signal below $f_0$ moves it toward the horizon. Either way it moves fastest when the beam is already far off broadside.

<img src="../../viz/img/L23-squint-vs-scan.svg"
     alt="Squint toward broadside in degrees against commanded angle from 0 to 70 degrees, for a 10.0 GHz signal with the phases set 500 MHz and 1000 MHz below it, exact as solid lines and the small-offset form as dashed lines; at 45 degrees the exact squint is 2.8 and 5.5 degrees, and the two forms separate as the angle grows"
     style="max-width: 640px; width: 100%; display: block; margin: 0 auto;">

The figure plots both forms for a $10.0\ \text{GHz}$ signal with the phases set $500$ and $1000\ \text{MHz}$ below it, so the beam moves toward broadside. Squint is under a degree near broadside, $2.8^\circ$ and $5.5^\circ$ at $45^\circ$, and $4.6^\circ$ and $8.8^\circ$ at $60^\circ$. The small-offset form tracks the exact one at small angles and overstates it at wide scan, by $2.2^\circ$ at $60^\circ$ for the $1000\ \text{MHz}$ offset, so a budget at wide scan should use the exact form.
::::

::::{frame} Worked Example: Squint on the PHASER
:::{present}
- Signal at $10.0$ GHz; Signal BW $500$ MHz sets the phases for $9.5$ GHz.
- A source at $40^\circ$ peaks at a commanded $42.6^\circ$, a $+2.6^\circ$ shift.
- Commanded to $40^\circ$, the beam lands at $37.6^\circ$, $0.2$ dB down there.
:::

:::{admonition} Worked example — squint on the PHASER
:class: tip
The signal arrives at $f = 10.0\ \text{GHz}$, and the GUI computes the phases for $f_0 = 9.5\ \text{GHz}$, $500\ \text{MHz}$ below it, which is what its **Signal BW** setting does. A beam commanded to $\theta_c$ points where $\sin\theta = (f_0/f)\sin\theta_c$, so the beam sweep peaks on a source at $\theta_s = 40^\circ$ at the commanded angle that puts the beam on it:

$$
\begin{aligned}
\sin\theta_c &= \frac{f}{f_0}\ \sin\theta_s \\
&= \frac{10.0}{9.5}\ \sin 40^\circ = 1.0526 \times 0.6428 = 0.6766 \\
\theta_c &= 42.6^\circ.
\end{aligned}
$$

The Angle readout, which reports the commanded angle at the peak, moves $+2.6^\circ$ from the source. The small-offset form, with $\delta = 0.5/9.5 = 0.0526$ and $\tan 40^\circ = 0.839$, gives

$$\delta\ \tan\theta_s = 0.0442\ \text{rad} = 2.5^\circ,$$

close enough for a budget. The L22–L23 Lab makes the same measurement on your kit's HB100 frequency, and Part 1 of the packet works it out there.

Command the same beam to $40^\circ$ instead and it lands at $\sin\theta = 0.95 \sin 40^\circ$, or $37.6^\circ$. At $40^\circ$ the beam is $17.8^\circ$ wide (Lesson 20's $13.6^\circ$ at $10.0\ \text{GHz}$, divided by $\cos 40^\circ$), so $2.4^\circ$ of squint loses only $0.2\ \text{dB}$ at the aimpoint. That loss is the array factor evaluated at the aimpoint, which now sits off the beam's peak. At $10.0\ \text{GHz}$, $kd = 2.93$ rad, and the aimpoint's $\sin\theta$ sits $\sin 40^\circ - \sin 37.6^\circ = 0.0321$ from the peak's:

$$
\begin{aligned}
\psi &= 2.93 \times 0.0321 \\
&= 0.094\ \text{rad} \\
\vert AF_8(\psi) \vert &= 0.977 \\
&= -0.20\ \text{dB}
\end{aligned}
$$

With the phases set $1\ \text{GHz}$ low, at $9.0\ \text{GHz}$, the beam lands at $35.3^\circ$, $4.7^\circ$ off, about a quarter of a beamwidth, and the loss grows to $0.8\ \text{dB}$.
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
:::{present}
<img src="../../viz/img/L23-ttd-vs-phase.svg"
     alt="Phase lag at the second element for a 45 degree steer against frequency: a true time delay of 33.0 ps gives a straight line through the origin, a phase shifter set at 9.5 GHz gives a flat line at 112.9 degrees, and the two cross only at 9.5 GHz; at 10.0 GHz they differ by 5.9 degrees"
     style="max-width: 640px; width: 100%; display: block; margin: 0 auto;">
:::

The cure is to stop steering with phase. If instead of a phase lag you insert a **true time delay** of $\tau_n = n\ d \sin\theta_0 / c$ in each element, the delay compensates the geometric path difference itself, which is a length and not a phase. Every frequency in the band then arrives in phase at the same angle, and the squint is gone at all offsets. True time delay is expensive in analog hardware, which is why large wideband arrays usually compromise: time delay at the level of the **subarray** (a group of elements combined before the rest, as on the PHASER's two four-element halves in <a href="../L17-phased-array-hardware/index.html#frame-the-hybrid-beamformer">Lesson 17</a>) to control the squint across the aperture, phase shifters inside each subarray where the residual path differences are small. The figure shows why for one element of a $45^\circ$ steer: a $33.0\ \text{ps}$ delay produces a phase that grows in step with frequency, while a phase shifter holds its $112.9^\circ$ at every frequency, so the two agree only at $9.5\ \text{GHz}$ and differ by $5.9^\circ$ at $10.0\ \text{GHz}$.
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

- PHASER at $10.0$ GHz: $0.96^\circ$ at broadside, one-fourteenth of a beam.
- Grows as $1/\cos\theta_0$: $1.9^\circ$ at $60^\circ$.
- 2 bits: $31^\circ$ steps, so broadside and about $\pm 32^\circ$ only.
:::

The inter-element phase for a beam at $\theta_0$ is $\Delta\phi = 360^\circ (d/\lambda) \sin\theta_0$. If the controller can only command multiples of the LSB, only a discrete set of beam angles exists:

$$\sin\theta_0 = \frac{m\ \text{LSB}}{360^\circ\ (d/\lambda)},$$

so the step near broadside is

$$\Delta\theta_0 \approx \frac{\text{LSB}}{360^\circ\ (d/\lambda)}\ \text{rad}.$$

For the PHASER at $10.0\ \text{GHz}$, $d/\lambda = 14/30 = 0.467$, so the step is $2.8125/(360 \times 0.467) = 0.0167\ \text{rad} = 0.96^\circ$ at broadside. Compared with the $13.6^\circ$ beamwidth that is about one-fourteenth of a beam, which is fine. Off broadside the same step in $\sin\theta_0$ spans a wider angle, because $\Delta(\sin\theta_0) = \cos\theta_0\ \Delta\theta_0$. The step therefore grows as $1/\cos\theta_0$, reaching $1.9^\circ$ at $60^\circ$. Drop to $B = 2$ and the same calculation gives $31^\circ$ per step: a 2-bit array can only point at broadside and at about $\pm 32^\circ$.

<img src="../../viz/img/L23-pointing-grid.svg"
     alt="The beam angles a phase shifter can command on the course array at 10.0 GHz, as ticks from 0 to 90 degrees: 2 bits gives 0 and 32.4 degrees; 3 bits adds 15.5 and 53.5; 4 bits gives eight angles out to 69.6 degrees; 7 bits gives a dense set whose gaps widen toward wide scan"
     style="max-width: 640px; width: 100%; display: block; margin: 0 auto;">

The figure shows the angles each bit count can reach on the course array. With 3 bits they are $0^\circ$, $15.5^\circ$, $32.4^\circ$ and $53.5^\circ$ at $10.0\ \text{GHz}$, equally spaced in $\sin\theta_0$ and so spreading apart in angle as the scan widens. A real controller rounds each element on its own, which fills in the angles between these and brings in the quantization lobes below.
::::

::::{frame} Quantization Sidelobes
:::{present}
$$
\text{QSLL} \approx -6B\ \text{dB}
$$

- Rounding leaves a periodic sawtooth phase error, and it radiates a lobe.
- Rule: each bit lowers the lobe 6 dB; 5 bits, $-30$ dB.
- On eight elements the worst lobe sits about 4 dB above the rule.
:::
:::{present}
<img src="../../viz/img/L23-quant-staircase.svg"
     alt="Top: the exact phase ramp for a beam at 28 degrees and the 3-bit staircase the shifters can set, in steps of 45 degrees. Bottom: the rounding error at each element, never more than 22.5 degrees either way, rising and falling across the aperture"
     style="max-width: 640px; width: 100%; display: block; margin: 0 auto;">
:::

A real controller does better than a uniform quantized increment. It computes the exact ramp for every element, then rounds each element independently, which puts the beam much closer to the commanded angle. What is left behind is a staircase: the difference between the exact ramp and the rounded one is a sawtooth error, bounded by half an LSB, that repeats across the aperture. A periodic phase error radiates, and where it radiates is a **quantization sidelobe**. The figure shows the staircase for a beam at $28^\circ$ with 3 bits at $10.0\ \text{GHz}$: the exact ramp climbs $78.9^\circ$ per element, the shifters can only set multiples of $45^\circ$, and the error left at each element rises and falls within $\pm 22.5^\circ$.

Its level follows from the size of the error. Rounding leaves at most half an LSB at each element. For a small phase error $e^{j\phi} \approx 1 + j\phi$, so the error adds a small field to each element in proportion to $\phi$, and the lobe that field radiates scales with the sawtooth's peak:

$$
\begin{aligned}
\phi_\text{max} &= \frac{\text{LSB}}{2} = \frac{\pi}{2^B}\ \text{rad} \\
\frac{E_\text{lobe}}{E_\text{beam}} &\approx \frac{\phi_\text{max}}{\pi} = 2^{-B} \\
\text{QSLL} &= 20\log_{10} 2^{-B} = -6.02B\ \text{dB}
\end{aligned}
$$

Each extra bit halves the error, which halves the lobe's field and lowers the **quantization sidelobe level (QSLL)** by $6$ dB. That gives the rule of thumb: 5 bits puts a lobe near $-30$ dB and 6 bits near $-36$ dB. Treat this as an RMS estimate for a large array. On an aperture as short as eight elements there are only a couple of sawtooth periods, so individual lobes scatter several dB either side of the rule. Taken at face value, the rule says that from 3 bits up the quantization lobes drop below the array's own $-13$ dB sidelobes and no longer set the sidelobe level.

Whether a given beam shows a quantization lobe at all depends on how its ramp falls on the grid, not only on the bit count. The L22–L23 Lab is built around that. It holds the beam at $15^\circ$ with the Blackman taper, so every true sidelobe sits under the noise floor and any lobe that rises comes from rounding. It sweeps the source in azimuth on **Signal vs Time** instead of sweeping the beam, so the rounded weights stay fixed while you read the pattern they make. Part 1 of the packet predicts, for each bit count, the strongest lobe that trace shows and where it sits. A lobe the azimuth sweep shows reads a few dB under the array factor's value, because a source swept in azimuth also crosses each patch's own pattern, as in the L21 Lab.

To predict a quantization lobe, divide the ramp by the LSB. If the ramp is close to a whole number of LSBs, every element rounds by only a few degrees, and the error is too small to raise a lobe out of the floor. If it is close to a whole number and a half, every other element rounds by almost half an LSB in the same direction, so the error repeats every two elements. A pattern that repeats every two elements radiates $180^\circ$ of $\psi$ away from the beam:

$$
\begin{aligned}
\psi_q &= \Delta\phi - 180^\circ \\
\sin\theta_q &= \frac{\psi_q}{360^\circ\ (d/\lambda)}
\end{aligned}
$$

:::{admonition} Worked example — rounding a ramp onto the grid
:class: tip
Hold a beam at $53^\circ$ at $10.0\ \text{GHz}$, where $d/\lambda = 0.467$. The ramp is

$$
\begin{aligned}
\Delta\phi &= 360^\circ\ (d/\lambda) \sin\theta_0 \\
&= 360^\circ \times 0.467 \times 0.799 = 134.2^\circ.
\end{aligned}
$$

At 3 bits the LSB is $45^\circ$, and the ramp is $134.2/45 = 2.98$ LSB. The controller asks element $n$ for $2.98n$ LSB and rounds it to $3n$, so the error grows by $0.8^\circ$ per element to $5.8^\circ$ at the far end of the row: too small for a lobe, so the 3-bit trace matches the 7-bit one.

At 2 bits the LSB is $90^\circ$, and the ramp is $1.49$ LSB. The commanded phases are $0^\circ$, $134.2^\circ$, $268.3^\circ$, $402.5^\circ$, and so on; they round to $0^\circ$, $90^\circ$, $270^\circ$, $360^\circ$, so elements $n = 1, 3, 5, 7$ lose $39^\circ$ to $44^\circ$ and the others almost nothing. That error repeats every two elements, and the lobe sits at

$$
\begin{aligned}
\psi_q &= 134.2^\circ - 180^\circ = -45.8^\circ \\
\sin\theta_q &= \frac{-45.8^\circ}{360^\circ \times 0.467} = -0.273 \\
\theta_q &= -15.8^\circ.
\end{aligned}
$$

With the lab's Blackman taper the full array factor puts it at $-15.2^\circ$ and $-7.7$ dBc, well above the $-12$ dB the $-6B$ rule gives, because a pattern that repeats every two elements adds up in one lobe instead of spreading.
:::

<img src="../../viz/img/L23-qsll-vs-bits.svg"
     alt="Worst lobe in dB below the beam against phase-shifter bits from 2 to 7: the minus 6B rule; the simulated worst quantization lobe on the course array over steer angles 0 to 50 degrees, about 4 dB above the rule at every bit count; and the uniform array's own sidelobes at minus 13.3 dB"
     style="max-width: 600px; width: 100%; display: block; margin: 0 auto;">

The figure adds a second curve: the worst quantization lobe the course array can produce at any steer angle up to $50^\circ$, computed from the field the rounding error radiates on its own. It sits about $4$ dB above the rule at every bit count, because the rule is an average for a large array and eight elements leave room for a worst case: at 2 bits the worst lobe reaches $-8.3$ dB.

More bits improve two things: finer pointing, which scales as the LSB, and a lower sidelobe floor, which scales as $6$ dB per bit. Seven bits is the standard choice because it puts the quantization floor far below every other error in the array.
::::

::::{frame} Dither
:::{present}
- The same sawtooth on every beam position radiates coherently into one lobe.
- A small known offset per element before rounding breaks the period.
- The same error spreads over many angles: a lower peak lobe, no new hardware.
:::

Dither lowers the peak quantization lobe without new hardware. If the rounding error is the same sawtooth on every beam position, it radiates coherently into one lobe. Adding a small known phase offset per element before rounding breaks the periodicity, which spreads the same total error energy over many angles instead of concentrating it in one.

<img src="../../viz/img/L23-dither-error.svg"
     alt="Rounding error at each element of a 32-element, 3-bit array steered to 15.8 degrees. Top, plain rounding: the error drifts by about 4 degrees per element and repeats as a sawtooth, radiating an error lobe at minus 16.9 dB. Bottom, with a fixed phase offset per element: the error stays within plus or minus 22.5 degrees but no longer repeats, and the error lobe falls to minus 21.8 dB"
     style="max-width: 640px; width: 100%; display: block; margin: 0 auto;">

The effect needs a longer aperture than eight elements to see, so the figure uses 32. With plain rounding the error drifts about $4^\circ$ per element and repeats as a sawtooth, and the field it radiates peaks at $-16.9$ dB. With a fixed, known offset built into each element and the command rounded around it, the error stays within the same $\pm 22.5^\circ$ but no longer repeats, and for a typical set of offsets its peak falls to $-21.8$ dB.
::::

::::{frame} Null Depth
:class: read-only

Quantization moves a null slightly off its commanded angle but does not fill it; <a href="../L24-null-steering/index.html#frame-quantization-and-null-depth">Lesson 24</a> works out how deep a null the course array can hold.
::::

::::{frame} Three Departures on the Course Array
:class: viz-frame

:::{depth}
The widget's left panel is the pattern; its right panel shows why the pattern looks that way. At the two angles marked 1 and 2 on the pattern, it adds the eight element contributions head to tail, the same sum Lesson 22 drew for the first sidelobe, and the chain's length is the level at that angle. Start in **Grating** at $14\ \text{mm}$: the chain at the sidelobe curls almost shut. Step to $42\ \text{mm}$ and the chain at $45.6^\circ$ comes out straight, because each fed element is a whole turn behind its neighbor. Switch to **Squint** and drag the offset: the chain at the commanded $45^\circ$ bends into an arc, while the chain at the new peak is straight, so the beam has moved rather than broken. Switch to **Quantization**: it opens at 3 bits with the beam at $30^\circ$, where the rounding error lines the chain up partway and a lobe rises to $-9$ dB near $61^\circ$. Move the steer angle and the lobe comes and goes, because whether rounding matters depends on how the ramp falls on the grid, not only on the number of bits. The widget runs at $10.0\ \text{GHz}$ with a uniform taper, so its angles differ from both the worked examples and your kit.
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
| $\sin\theta_g = \sin\theta_0 \pm m\lambda/d$ | Grating-lobe angles, from the $2\pi$ periodicity of the array factor | $42\ \text{mm}$ at $10.0\ \text{GHz}$ gives $\pm 45.6^\circ$; $56\ \text{mm}$ gives $\pm 32.4^\circ$ |
| $d < \lambda/(1+\vert\sin\theta_0\vert)$ | Spacing that keeps grating lobes out of visible space | $d \le \lambda/2$ is safe at every scan angle |
| Grating-lobe height | It is a second main lobe, not a sidelobe | Equal to the main beam; a taper does not reduce it |
::::

::::{frame} Summary: Beam Squint
:class: read-only

| Symbol / idea | What it is | Number to remember |
| :-- | :-- | :-- |
| $\Delta\theta = \arcsin((f_0/f)\sin\theta_0) - \theta_0$ | Beam squint when the signal is off the phase-set frequency | Phases $500\ \text{MHz}$ below a $10.0\ \text{GHz}$ signal: a source at $40^\circ$ peaks at a commanded $42.6^\circ$ |
| $\Delta\theta \approx -(\Delta f/f_0)\tan\theta_0$ | Small-offset squint, for a budget | Zero at broadside, worst at wide scan |
| True time delay | Delays the signal instead of rotating its phase | Removes squint at all offsets |
::::

::::{frame} Summary: Quantization
:class: read-only

| Symbol / idea | What it is | Number to remember |
| :-- | :-- | :-- |
| $\text{LSB} = 360^\circ/2^B$ | Phase step of a $B$-bit shifter | ADAR1000: $B = 7$, LSB $= 2.8125^\circ$ |
| $\Delta\theta_0 \approx \text{LSB}/(360^\circ d/\lambda)$ | Pointing granularity near broadside | $0.96^\circ$ on the PHASER at $10.0\ \text{GHz}$, one-fourteenth of a beam |
| $\text{QSLL} \approx -6B$ dB | Quantization sidelobe rule of thumb | 5 bits gives $-30$ dB; on eight elements the worst lobe sits about 4 dB above the rule |
::::

::::{frame} Pre-Lab
:class: read-only doc-links

Tables C to E of Part 1 in the L22–L23 Lab packet are this lesson's share of
the pre-lab; the Setup row and Tables A and B go with Lesson 22. Do them at the
same frequency, before the lab period, and bring them to class.

| Part 1 table | You predict | Checked in | Method |
| :-- | :-- | :-- | :-- |
| Table C | lobe angles, their height against the $0^\circ$ lobe, and the peak drop, for 42 and 56 mm | Table C; Steps 15 and 16 | "Worked Example: Thinning the PHASER Row," "The Grating Condition" |
| Table D | the Angle readout at a Signal BW of 10 and 500 MHz, and the shift | Table D; Steps 17 and 18 | "Worked Example: Squint on the PHASER" |
| Table E | the strongest lobe outside the main lobe, and where, at 7, 4, 3, and 2 bits | Table E; Steps 19 to 21 | the rounding example under "Quantization Sidelobes" |

Every method has a worked example at $10.0\ \text{GHz}$, below every kit, in
the frame named beside it.

- <a class="doc-link" href="../../labs/ECE444_Lab_L22_L23_TaperSquint_blank.pdf" target="_blank" rel="noopener">L22–L23 Lab packet, Part 1 (PDF)</a>
::::

::::{frame} Looking Ahead
:::{present}
- The L22–L23 Lab measures all three departures on your own kit.
- L24 places a null on purpose; quantization nudges it without filling it.
- Bring the LSB of a $B$-bit shifter, its pointing step, and the weights $w_n$.
:::

The second half of the [L22–L23 Lab](../L22-L23-lab-tapering-squint/index.md) measures all three of today's departures on your own kit. Lesson 24 then extends pattern control from the whole beam to one chosen angle. So far you have shaped the beam and the sidelobes as a whole; next you will place a null at a chosen angle on purpose, which is what an array does when a jammer or an interfering transmitter sits somewhere you know about. The weights come from subtracting one steering vector from another, and the arithmetic is short.

Before Lesson 24, be able to state the LSB of a $B$-bit shifter and the pointing step it implies on the course array, and review the element phases of <a href="../L18-beam-steering/index.html">Lesson 18</a> and the amplitudes $a_n$ of <a href="../L22-sidelobes-tapering/index.html">Lesson 22</a>: the null-steering weights combine the two.
::::
