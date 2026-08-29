---
frame_view: true
---

# L26 - Beam Squint and Quantization

::::{frame}
:class: title-frame

<div class="course-mark">ECE 444 · Fall 2026</div>

<h1 class="frame-title">Beam Squint and Quantization</h1>

<div class="title-rule"></div>

This lesson gives you the number for each.

Lesson 26 · Antennas, Phased Arrays, and Radar Systems · Dr. Neil Rogers
::::

::::{frame}
:::{admonition} Slides
:class: slides
<a href="../../slides/L26-beam-squint-quantization.html" target="_blank" rel="noopener">html slides</a>
<a href="../../slides/L26-beam-squint-quantization.html?print-pdf" target="_blank" rel="noopener">pdf slides</a>
<a href="../../slides/L26-beam-squint-quantization.md" target="_blank" rel="noopener">raw markdown slides</a>
:::
::::

::::{frame} Learning Objectives

<ol class="lo-list lo-sublist" style="--module: '3'; --lo: '8'">
  <li>I can explain why thinning an array creates grating lobes and predict their angles from spacing and steer angle.</li>
  <li>I can state and apply the spacing criterion that keeps grating lobes out of visible space over a scan range.</li>
  <li>I can compute beam squint for a steered array operating away from its phase-set frequency.</li>
  <li>I can compute the phase-quantization limits of a B-bit phase shifter — step size, pointing granularity, and quantization sidelobe level.</li>
  <li>I can state the system impact of grating lobes, beam squint, and quantization on a radar or communications array.</li>
</ol>

:::{depth}
In the tapering lab you took control of the sidelobes with amplitude weights, and the pattern did what the theory said it would. Amplitude is now a solved problem. Three things are still capable of putting energy where you did not ask for it, and none of them are fixed by a taper: the **element spacing**, the **signal bandwidth**, and the **finite resolution of the phase shifters**. Each one produces a specific, predictable defect — a second full-height beam, a beam that walks with frequency, and a floor of sidelobes you cannot get below. This lesson gives you the number for each.
:::
::::

::::{frame} The array factor is periodic
Every array pattern in this module has been a function of one variable,

$$\psi = kd\ (\sin\theta - \sin\theta_0),$$

and the uniform array factor built on it,

$$AF_N(\psi) = \frac{\sin(N\psi/2)}{N \sin(\psi/2)}.$$

Replace $\psi$ by $\psi + 2\pi$ and both sines flip sign together, so $\vert AF_N \vert$ is unchanged. The array factor is **periodic in $\psi$ with period $2\pi$**. The main lobe is the peak at $\psi = 0$, and the same peak reappears at $\psi = \pm 2\pi, \pm 4\pi, \ldots$ — every one of them a full-height beam.
::::

::::{frame} Visible space
Whether you ever see those repeats depends on how much of the $\psi$ axis the real angles $-90^\circ \le \theta \le +90^\circ$ reach. That span is called **visible space**, and its width is set by the spacing: as $\sin\theta$ runs from $-1$ to $+1$, $\psi$ runs over a window of total width $2kd = 4\pi d/\lambda$. Widen $d$ and you drag more periods of the array factor into view. A repeat that lands inside visible space is a **grating lobe**.
::::

::::{frame} The grating condition
Set $\psi = 2\pi m$ and solve:

$$kd\ (\sin\theta_g - \sin\theta_0) = 2\pi m \quad \Longrightarrow \quad \boxed{\ \sin\theta_g = \sin\theta_0 \pm m\ \frac{\lambda}{d}\ }$$

for integer $m = 1, 2, \ldots$ Any solution with $\vert \sin\theta_g \vert \le 1$ is a real angle, and the array radiates a second beam there.

:::{callout}
A grating lobe is not a sidelobe. At $\theta_g$ every element is back in phase — one full wavelength of path difference per element instead of zero — so the grating lobe is **exactly as tall as the main lobe**. Tapering does not touch it, because the taper controls the sidelobe skirts of one beam and this is a second beam.
:::
::::

::::{frame} Worked example — thinning the PHASER row
:::{admonition} Worked example — thinning the PHASER row
:class: tip
The PHASER array is 8 patches on a $d = 14\ \text{mm}$ pitch. Feed only every third element and the fed elements sit $42\ \text{mm}$ apart. At the array's design center of $10.3\ \text{GHz}$, $\lambda = 29.1\ \text{mm}$, so $\lambda/d = 29.1/42 = 0.693$.

At broadside ($\theta_0 = 0$), the $m = 1$ solutions are

$$\sin\theta_g = \pm 0.693 \quad \Longrightarrow \quad \theta_g = \pm 43.9^\circ.$$

The $m = 2$ solutions need $\vert \sin\theta_g \vert = 1.386$, which is not a real angle, so there are exactly three full-height beams: $0^\circ$ and $\pm 44^\circ$.
:::
::::

::::{frame} Worked example — thinning the PHASER row, continued
:::{admonition} Worked example — thinning the PHASER row, continued
:class: tip
Feed every fourth element instead ($56\ \text{mm}$, $\lambda/d = 0.520$) and the pair moves in to $\pm 31.3^\circ$, with the $m = 2$ repeat pressing right up against the horizon — the pattern comes back to within a fraction of a dB of full height at $\pm 90^\circ$.
:::
::::

::::{frame} The thinned-array trade
Thinning has two effects. The three fed elements still span an $84\ \text{mm}$ aperture, so the main beam stays narrow, but with three elements instead of eight the array collects less signal and the pattern between the beams is poorly controlled. The narrow beam of a large aperture with the ambiguity of a sparse one is the classic thinned-array trade.
::::

::::{frame} Keeping them out of sight
You want no grating lobe anywhere in visible space, for every angle you intend to scan to. The dangerous solution is the one closest to the horizon on the far side of the beam. For a beam steered to positive $\theta_0$, that is $m = 1$ with the minus sign, and pushing it past the horizon requires

$$\sin\theta_0 - \frac{\lambda}{d} < -1 \quad \Longrightarrow \quad \boxed{\ d < \frac{\lambda}{1 + \vert \sin\theta_0 \vert}\ }$$
::::

::::{frame} Design numbers
Read the physics: the wider you intend to scan, the closer together the elements must be. Broadside operation tolerates $d < \lambda$. Scanning to $\pm 45^\circ$ demands $d < 0.586\lambda$, and $\pm 60^\circ$ demands $d < 0.536\lambda$. Take the criterion to its limit, $\theta_0 \to 90^\circ$, and you get $d < \lambda/2$ — which is why **half-wavelength spacing is the default in every scanning array**. It is grating-lobe-free at any scan angle you can command.
::::

::::{frame} Worked example — is the PHASER safe?
:::{admonition} Worked example — is the PHASER safe?
:class: tip
Use the highest frequency the array is specified for, $10.5\ \text{GHz}$, because $\lambda$ is shortest there and the criterion is tightest: $\lambda = 28.6\ \text{mm}$, so $\lambda/d = 28.6/14 = 2.04$.

The criterion requires $1 + \vert\sin\theta_0\vert < \lambda/d = 2.04$, or $\vert\sin\theta_0\vert < 1.04$. Every real angle satisfies that, so the array has **no grating lobe at any scan angle in its band**. That margin is not an accident: the $14\ \text{mm}$ pitch is $0.49\lambda$ at the band edge, deliberately just inside the half-wavelength rule.
:::
::::

::::{frame} Grating lobes, on purpose
```{note}
Grating lobes are not always a defect. Interferometers and sparse radio-astronomy arrays use them on purpose, resolving fine detail with a small number of widely spaced elements and removing the ambiguity by other means. The rule is that grating lobes must be *chosen*, not discovered after the array is built.
```
::::

::::{frame} Beam squint: the setup
A phase shifter is set once, in degrees. The angle that setting steers to is not fixed, because the phase a given path length produces depends on frequency.
::::

::::{frame} Where the beam points, and where it was commanded
Suppose the beam-steering computer sets element $n$ to a lag of $n\ k_0 d \sin\theta_0$, computed at the design frequency $f_0$ where $k_0 = 2\pi/\lambda_0$. Now a signal arrives at some other frequency $f$ in the band. The elements add in phase toward whatever angle $\theta$ makes the arrival phase cancel the applied lag:

$$kd \sin\theta = k_0 d \sin\theta_0 \quad \Longrightarrow \quad \sin\theta = \frac{\lambda}{\lambda_0}\sin\theta_0 = \frac{f_0}{f}\sin\theta_0,$$
::::

::::{frame} The squint formula
so the beam actually points at

$$\boxed{\ \Delta\theta = \arcsin\!\left(\frac{f_0}{f}\sin\theta_0\right) - \theta_0\ }$$

away from where it was commanded.
::::

::::{frame} Reading the squint formula
This is **beam squint**. Note what it does and does not depend on. It does not depend on $N$ or on $d$ — the phase ramp and the path lengths scale together, and only the ratio $f_0/f$ survives. It vanishes at broadside, where the ramp is zero and there is nothing to scale. For small fractional offsets $\delta = (f - f_0)/f_0$, expanding the arcsine gives the form worth remembering:

$$\Delta\theta \approx -\delta\ \tan\theta_0 \quad \text{(radians).}$$

The beam walks toward the horizon as the frequency drops, and it walks fastest when you are already scanned far off broadside.
::::

::::{frame} Worked example — squint on the PHASER
:::{admonition} Worked example — squint on the PHASER
:class: tip
Phases are set for $\theta_0 = 45^\circ$ at the HB100's $f_0 = 10.525\ \text{GHz}$. A signal arrives $500\ \text{MHz}$ lower, at $10.025\ \text{GHz}$:

$$\sin\theta = \frac{10.525}{10.025}\ \sin 45^\circ = 1.0499 \times 0.7071 = 0.7424 \quad \Longrightarrow \quad \theta = 47.9^\circ.$$

The beam has squinted $\Delta\theta = +2.9^\circ$. The approximation gives $-(-0.0475)(1.000) = 0.0475\ \text{rad} = 2.7^\circ$, close enough for a budget.
:::
::::

::::{frame} Worked example — squint on the PHASER, continued
:::{admonition} Worked example — squint on the PHASER, continued
:class: tip
At $45^\circ$ the beam is about $18^\circ$ wide, so $2.9^\circ$ of squint costs only $0.25\ \text{dB}$ at the aimpoint. Push the offset to $1\ \text{GHz}$ and the squint reaches $6.4^\circ$, roughly a third of a beamwidth, and the loss grows to $1.0\ \text{dB}$.
:::
::::

::::{frame} Why squint matters
Two systems care about this for different reasons. A **wideband radar** transmits a pulse whose spectrum is the bandwidth; each frequency component in that pulse points somewhere slightly different, so the compressed pulse is smeared in angle and the effective beam is broadened and depointed. A **communications link** running a modulated carrier loses gain at the band edges relative to the center, which shows up as amplitude tilt across the channel rather than as an angle error.
::::

::::{frame} The cure is time, not phase
The cure is to stop steering with phase. If instead of a phase lag you insert a **true time delay** of $\tau_n = n\ d \sin\theta_0 / c$ in each element, the delay compensates the geometric path difference itself, which is a length and not a phase. Every frequency in the band then arrives in phase at the same angle, and the squint is gone at all offsets. True time delay is expensive in analog hardware, which is why large wideband arrays usually compromise: time delay at the subarray level to control the squint across the aperture, phase shifters inside each subarray where the residual path differences are small.
::::

::::{frame} Phase quantization
The ADAR1000 does not accept an arbitrary phase. It has a $B$-bit phase shifter, and $B$ bits divide the circle into $2^B$ steps of

$$\text{LSB} = \frac{360^\circ}{2^B}.$$

The ADAR1000 uses $B = 7$, giving 128 states and an LSB of $2.8125^\circ$.
Everything the beamformer commands gets rounded to that grid, with two separate
consequences.
::::

::::{frame} Pointing granularity
The inter-element phase for a beam at $\theta_0$ is $\Delta\phi = 360^\circ (d/\lambda) \sin\theta_0$. If the controller can only command multiples of the LSB, only a discrete set of beam angles exists:

$$\sin\theta_0 = \frac{m\ \text{LSB}}{360^\circ\ (d/\lambda)}, \qquad \text{step near broadside} \quad \Delta\theta_0 \approx \frac{\text{LSB}}{360^\circ\ (d/\lambda)}\ \text{rad}.$$

For the PHASER at $10.525\ \text{GHz}$, $d/\lambda = 0.491$, so the step is $2.8125/(360 \times 0.491) = 0.0159\ \text{rad} = 0.91^\circ$ at broadside. Compared with the $13.2^\circ$ beamwidth that is about one-fourteenth of a beam, which is fine. The step grows as $1/\cos\theta_0$ off broadside, reaching $1.8^\circ$ at $60^\circ$. Drop to $B = 2$ and the same calculation gives $29^\circ$ per step: a 2-bit array can only point at broadside and at about $\pm 31^\circ$.
::::

::::{frame} Quantization sidelobes
A real controller does better than a uniform quantized increment. It computes the exact ramp for every element, then rounds each element independently, which puts the beam much closer to the commanded angle. What is left behind is a staircase: the difference between the exact ramp and the rounded one is a sawtooth error, bounded by half an LSB, that repeats across the aperture. A periodic phase error radiates, and where it radiates is a **quantization sidelobe**. The rule of thumb is

$$\text{QSLL} \approx -6B\ \text{dB},$$
::::

::::{frame} Quantization sidelobes, continued
so 2 bits puts a lobe near $-12$ dB, 3 bits near $-18$ dB, and the ADAR1000's 7 bits near $-42$ dB. Treat this as an RMS estimate for a large array. On an aperture as short as eight elements there are only a couple of sawtooth periods, individual lobes scatter several dB either side of the rule, and for $B \ge 3$ they drop below the array's own $-13$ dB sidelobes and stop mattering.
::::

::::{frame} What more bits buy
More bits buy two different things. They buy finer pointing, which scales as the LSB, and they buy a lower sidelobe floor, which scales as $6$ dB per bit. Seven bits is the standard choice because it puts the quantization floor far below every other error in the array.
::::

::::{frame} What quantization does not set
One thing quantization does *not* set is how deep a null can go. It is tempting to assume that a cancellation is only as good as the phase resolution behind it, but the weights that place a null are not fighting the LSB: rounding them to a $2.8125^\circ$ grid with 1% gain steps still produces a notch near $-48$ dB at the angle it was designed for. What rounding does instead is move the notch a fraction of a degree off its commanded angle, which is a pointing effect, not a depth effect.
::::

::::{frame} The measured limit comes from the receiver
The measured limit comes from the receiver. A beam sweep on the PHASER has a noise floor about $23$ dB below the uniform-taper peak, and the weights that create a null cost roughly $2$ dB of main-lobe gain, so nothing deeper than about $21$ dB below the new peak can be seen at all. That is why the nulls measured in the next two lessons land at $20$ to $22$ dB: the pattern goes further down than that, and the sweep cannot follow it.
::::

::::{frame} Key point
:::{callout}
Separate the two floors. **Quantization** sets a sidelobe floor at roughly $-6B$ dB and a pointing granularity of about one LSB, and on the course array it still allows a $-48$ dB null. The **noise floor** of the measurement sets what you can observe: on the PHASER sweep it sits about $23$ dB below the uniform-taper peak, and once the null weights cost roughly $2$ dB of main lobe the deepest observable notch is $20$ to $22$ dB. A shallow measured null usually means the second limit, not the first.
:::
::::

::::{frame} The three departures side by side
The widget below runs the same array-factor calculation for all three effects on the course array, so you can compare their signatures directly. Start in **Grating** and step the spacing from $14$ to $56\ \text{mm}$, watching the predicted and measured lobe angles agree and the horizon reading climb. Switch to **Squint** and drag the offset: the leftover phase error stays a straight ramp, which is why the beam moves rather than degrades. Switch to **Quantization** and pull the bits down to 2, where the leftover error becomes a staircase and the power that used to be in the beam appears as a lobe tens of degrees away.
::::

::::{frame} Interactive — grating, squint, and phase quantization on the course array
:class: viz-frame

<iframe src="../../viz/squint-quantization.html"
        width="100%" height="699"
        style="border: 1px solid #cddce9; border-radius: 6px;"
        loading="lazy"
        title="Grating lobes, beam squint and phase quantization on the 8-element course array">
</iframe>
::::

::::{frame} Three departures — grating and squint
The three failures look different on a sweep and they are fixed in different places in the design.

| Phenomenon | Cause | Predict it with | Design cure |
| :-- | :-- | :-- | :-- |
| Grating lobe | Element spacing too wide for the scan range | $\sin\theta_g = \sin\theta_0 \pm m\lambda/d$ | Keep $d < \lambda/(1+\vert\sin\theta_0\vert)$; $d \le \lambda/2$ is safe everywhere |
| Thinned-array ambiguity | Feeding a subset of a filled aperture | Same criterion, using the effective spacing | Fill the aperture, or accept and resolve the ambiguity |
| Beam squint | One phase setting used across a band | $\Delta\theta = \arcsin((f_0/f)\sin\theta_0) - \theta_0$ | True time delay, at the element or the subarray |
::::

::::{frame} Three departures — quantization
| Phenomenon | Cause | Predict it with | Design cure |
| :-- | :-- | :-- | :-- |
| Pointing granularity | Finite phase steps in the beam-steering command | $\Delta\theta_0 \approx \text{LSB}/(360^\circ d/\lambda)$ | More bits |
| Quantization sidelobes | Staircase error left after rounding the ramp | $\text{QSLL} \approx -6B$ dB | More bits, or dither the rounding across elements |
::::

::::{frame} The low-cost fix: dither
Dither is the low-cost fix. If the rounding error is the same sawtooth on every beam position, it radiates coherently into one lobe. Adding a small known phase offset per element before rounding breaks the periodicity, which spreads the same total error energy over many angles instead of concentrating it in one, lowering the peak quantization lobe at no hardware cost.
::::

::::{frame} Summary — grating lobes
| Symbol / idea | What it is | Number to remember |
| :-- | :-- | :-- |
| $\sin\theta_g = \sin\theta_0 \pm m\lambda/d$ | Grating-lobe angles, from the $2\pi$ periodicity of the array factor | $42\ \text{mm}$ at $10.3\ \text{GHz}$ gives $\pm 43.9^\circ$; $56\ \text{mm}$ gives $\pm 31.3^\circ$ |
| $d < \lambda/(1+\vert\sin\theta_0\vert)$ | Spacing that keeps grating lobes out of visible space | $d \le \lambda/2$ is safe at every scan angle |
::::

::::{frame} Summary — grating-lobe height
| Symbol / idea | What it is | Number to remember |
| :-- | :-- | :-- |
| Grating-lobe height | It is a second main lobe, not a sidelobe | Equal to the main beam; a taper does not reduce it |
::::

::::{frame} Summary — beam squint
| Symbol / idea | What it is | Number to remember |
| :-- | :-- | :-- |
| $\Delta\theta = \arcsin((f_0/f)\sin\theta_0) - \theta_0$ | Beam squint when the signal is off the phase-set frequency | $500\ \text{MHz}$ at $45^\circ$ gives $+2.9^\circ$ |
| $\Delta\theta \approx -(\Delta f/f_0)\tan\theta_0$ | Squint in one line, for a budget | Zero at broadside, worst at wide scan |
| True time delay | Delays the signal instead of rotating its phase | Removes squint at all offsets |
::::

::::{frame} Summary — quantization
| Symbol / idea | What it is | Number to remember |
| :-- | :-- | :-- |
| $\text{LSB} = 360^\circ/2^B$ | Phase step of a $B$-bit shifter | ADAR1000: $B = 7$, LSB $= 2.8125^\circ$ |
| $\Delta\theta_0 \approx \text{LSB}/(360^\circ d/\lambda)$ | Pointing granularity near broadside | $0.91^\circ$ on the PHASER, one-fourteenth of a beam |
| $\text{QSLL} \approx -6B$ dB | Quantization sidelobe rule of thumb | 2 bits gives $-12$ dB; 7 bits gives $-42$ dB |
::::

::::{frame} Practice
- <a href="../../practice/ECE444_L26_Practice_blank.pdf" target="_blank" rel="noopener">Problem set (PDF)</a>
- <a href="../../practice/ECE444_L26_Practice_SOLUTIONS.pdf" target="_blank" rel="noopener">Solutions (PDF)</a>
::::

::::{frame} Where this is going
Lesson 27 turns pattern control up a notch. So far you have shaped the beam and the sidelobes as a whole; next you will place a null at a chosen angle on purpose, which is what an array does when a jammer or an interfering transmitter sits somewhere you know about. The weights come from subtracting one steering vector from another, and the arithmetic is short.

Both of today's floors come back with it. Quantization moves the notch slightly off its commanded angle without filling it, and the sweep's noise floor decides how much of the notch you can see, which is why the measured depth in Lesson 28 stops near $21$ dB while the designed null is far deeper. Before Lesson 27, be able to state the LSB of a $B$-bit shifter and the pointing step it implies on the course array, and review the complex element weights $w_n$ from Lesson 24 — the null-steering result is written entirely in that notation.
::::
