---
frame_view: true
---

# L24 - Null Steering

::::{frame}
:class: title-frame

<div class="course-mark">ECE 444 · Fall 2026</div>

<h1 class="frame-title">Null Steering</h1>

<div class="title-rule"></div>

A deep null on the interferer lowers the main lobe by only about 2 dB.

Lesson 24 · Antennas, Phased Arrays, and Radar Systems · Dr. Neil Rogers
::::

::::{frame} Printing
:class: read-only

To print the slides, switch to present mode and print: one slide a sheet,
with room for notes. Print from read mode for the whole lesson.
::::

::::{frame} Learning Objectives
:class: here-24

<ol class="lo-list" style="--module: '3'; counter-reset: lo 8">
  <li>I can calculate null-steering weights and implement pattern nulls on the ADALM-PHASER.</li>
</ol>

```{include} ../../_snippets/m3-strip.md
```

:::{depth}
Lesson 23 catalogued the three ways a steered pattern breaks on its own: grating lobes when the elements are too far apart, squint when the frequency moves off the design point, and quantization lobes when the phase shifter runs out of bits. Those were accidents, and the work was to avoid them. Today we break the pattern on purpose. We place a deep null exactly where an interferer sits, keep the main beam pointed where it was, and lose a known amount of main-lobe gain doing it.

The lesson builds the four nulls you measure in the L24 Lab. The first is a notch we compute and load into all eight elements. The second is a null at boresight that comes from subtracting the board's two digital channels and needs no computation. The third is the null an adaptive beamformer, MVDR, finds for itself from the received data. The fourth is the monopulse pair, which uses that subtraction to measure a target's angle from a single look. The Pre-Lab at the end lists the predictions you bring to class.
:::
::::

::::{frame} A Loud Signal in a Sidelobe
:::{present}
- The target is at broadside; an interferer 10 dB stronger is at $+22.5^\circ$.
- The uniform array's first sidelobe there is $-13$ dB.
- The interferer arrives at $10 - 13 = -3$ dB relative to the target.
:::
:::{present}
<img src="../../viz/img/L24-jammer-sidelobe.svg" alt="Uniform 8-element pattern with a target at broadside and an interferer entering through the first sidelobe" style="max-width: 640px; width: 100%; display: block; margin: 0 auto;">
:::

So far we have judged every array by its main lobe. Peak gain, beamwidth, and scan loss all describe where the energy goes. That is the right measure when the only thing in the field of view is the target. It is the wrong measure when something else in the field of view is louder than the target.

Consider the PHASER looking at a target on boresight, and a second transmitter at $+22.5^\circ$ that is 10 dB stronger at the aperture. The array does not reject the interferer because it is off-axis; it rejects it by the pattern level in that direction, and the first sidelobe of a uniform 8-element array is only $-13$ dB. The interferer therefore arrives at the beamformer output at $10 - 13 = -3$ dB relative to the target. A 3 dB margin leaves no room for a fade or a fluctuation in the target, and the receiver can lock onto the wrong signal.

:::{note}
The military case is the familiar one: a **jammer** placed in a sidelobe is the reason sidelobe-level specifications exist at all, and null steering is the countermeasure. The physics is the same for a base station on the same frequency, a radar altimeter on the next aircraft, or a strong multipath reflection off a hangar. Null steering handles anything loud that is not where you are looking the same way.
:::
::::

::::{frame} Null Depth Versus Transmit Power
:::{present}
- Raising the target 20 dB takes 100 times the transmit power.
- Lowering the pattern 20 dB at $+22.5^\circ$ lowers the main lobe about 2 dB.
:::
:::{present}
:class: callout

Lowering the pattern at the interferer helps more than raising it at the target.
:::

There are two remedies. We can raise the target's return by 20 dB, which for a radar means a hundredfold increase in transmit power, a much larger amplifier, and a much brighter signature for anyone listening. Or we can push the pattern level at $+22.5^\circ$ down by 20 dB, which lowers the main-lobe gain by about 2 dB and takes a weight calculation the processor finishes in microseconds. The second option is why every modern radar and electronic-warfare receiver steers nulls.

:::{callout}
We judge an array by the ratio of the wanted signal to the unwanted one. When the interferer is stronger than the target, moving the pattern *down* at one angle helps more than moving it *up* at another.
:::
::::

::::{frame} Complex Weights
:::{present}
$$
w_n = a_n e^{j\phi_n}
$$

- The **Element Gains** slider sets $a_n$; the **Phase Control** entry sets $\phi_n$.
- Lesson 18 used phase only, Lesson 22 amplitude only; a null needs both.
:::

To place a null we need control the previous lessons did not use. <a href="../L18-beam-steering/index.html#frame-sign-of-the-compensating-ramp">Lesson 18</a> steered the beam with **phase only**, holding every element at full gain. <a href="../L22-sidelobes-tapering/index.html#frame-tapers-on-the-array">Lesson 22</a> tapered the sidelobes with **amplitude only**, holding every element in phase. Null steering uses both at once, so from here on each element carries a **complex weight** $w_n$, with $a_n$ the element's amplitude setting and $\phi_n$ its phase setting. On the PHASER, $a_n$ is the Element Gains slider for that channel and $\phi_n$ is its Phase Control entry. The two ADAR1000s provide both controls on all eight elements, which is exactly the degrees of freedom this lesson uses.
::::

::::{frame} The Steering Vector
:::{present}
$$
\begin{aligned}
v_n(\theta) &= e^{jnkd\sin\theta} \\
y(\theta) &= \mathbf{w}^{T}\mathbf{v}(\theta) \\
&= \sum_{n=0}^{N-1} w_n\ e^{jnkd\sin\theta}
\end{aligned}
$$

- $\mathbf{v}(\theta)$ belongs to the direction, not to the settings.
- $y(\theta)$ is Lesson 16's array factor with general weights.
:::

Write the array response the way the elements see the world. A plane wave arriving from angle $\theta$ reaches element $n$ a distance $nd\sin\theta$ earlier than it reaches element 0, so the signal at element $n$ carries the extra phase $nkd\sin\theta$. Collect those factors into the **steering vector**

$$
\begin{aligned}
\mathbf{v}(\theta) = \big[\ &1,\ e^{jkd\sin\theta},\ e^{j2kd\sin\theta}, \\
&\ldots,\ e^{j(N-1)kd\sin\theta}\ \big],
\end{aligned}
$$

<img src="../../viz/img/L18-path-difference.svg"
     alt="A plane wave arriving at angle theta from broadside on a row of elements spaced d apart: the wavefront reaches each element an extra path d sin theta later than its neighbor"
     style="max-width: 520px; width: 100%; display: block; margin: 0 auto;">

The figure is the one <a href="../L18-beam-steering/index.html#frame-path-time-and-phase">Lesson 18</a> used for the same extra path. Each element's entry in the steering vector is that path converted to phase, so the $n$-th entry is $v_n(\theta) = e^{jnkd\sin\theta}$. The steering vector is not a property of the array's settings. It is a property of the direction, and it says how a wave from that direction is spread in phase across the aperture.

The beamformer forms one number from the eight element signals by weighting and summing them, so the array's response to a wave from $\theta$ is the dot product

$$
y(\theta) = \mathbf{w}^{T}\mathbf{v}(\theta) = \sum_{n=0}^{N-1} w_n\ e^{jnkd\sin\theta}.
$$

This is the array factor of <a href="../L16-array-factor/index.html#frame-the-array-factor-from-the-radiation-vector">Lesson 16</a> with the weights left general. Every pattern in Module 3 is one evaluation of this sum.
::::

::::{frame} The Conjugate Steering Vector
:::{present}
$$
\mathbf{w}_\text{d} = \mathbf{v}^{*}(\theta_0), \qquad y(\theta_0) = N
$$

- That is the L18 phase ramp $\Delta\phi = kd\sin\theta_0$, written as a vector.
- The weight carries the **negative** of the arrival phase.
- The sign of every weight's phase follows one course-wide convention.
:::

Now read the beam-steering result of <a href="../L18-beam-steering/index.html#frame-sign-of-the-compensating-ramp">Lesson 18</a> in this language. To point the beam at $\theta_0$ we want all $N$ terms of the sum to add in phase when $\theta = \theta_0$, which happens when each weight cancels its own steering-vector phase:

$$
\begin{aligned}
w_n &= e^{-jnkd\sin\theta_0} \\
\mathbf{w}_\text{d} &= \mathbf{v}^{*}(\theta_0).
\end{aligned}
$$

The conjugate steering vector *is* the progressive phase ramp $\Delta\phi = kd\sin\theta_0$ you have been programming into the ADAR1000s since the L18 Lab. With $\mathbf{w}_\text{d}$ applied, $y(\theta_0) = N$ — every element contributes a unit phasor pointing the same way — and that is the peak of the pattern.

:::{note}
Two conventions matter and both are course-wide. We measure angles $\theta$ from broadside, and the weight that steers to $\theta_0$ carries $e^{-jnkd\sin\theta_0}$, the negative of the arrival phase. Enter every phase with that sign; Part 1 of the L24 Lab packet has you work out what a sign error does to the notch.
:::
::::

::::{frame} The Null Problem
:::{present}
- The response at the interferer must be zero: $\mathbf{w}^{T}\mathbf{v}(\theta_1) = 0$.
- Stay as close to $\mathbf{w}_\text{d}$ as possible.
- We subtract part of a beam aimed at $\theta_1$:

$$
\begin{aligned}
\mathbf{w}_\text{n} &= \mathbf{v}^{*}(\theta_1) \\
\mathbf{w} &= \mathbf{w}_\text{d} - r_\text{n}\ \mathbf{w}_\text{n}
\end{aligned}
$$
:::
:::{present}
<img src="../../viz/img/L24-projection.svg"
     alt="Schematic of the weight vectors. Left, interferer on a sidelobe with a projection of 0.23: w_d is nearly perpendicular to w_n, the removed part r_n w_n is short, and w stays close to w_d, keeping 0.95 of the look-direction response. Right, interferer near the main lobe with a projection of 0.84: w_d leans toward w_n, most of it is removed, and the look direction keeps 0.30"
     style="max-width: 600px; width: 100%; display: block; margin: 0 auto;">
:::

Here is the problem stated exactly. We have the beam-steering weights $\mathbf{w}_\text{d} = \mathbf{v}^{*}(\theta_0)$, and we want a new weight vector $\mathbf{w}$ that satisfies two conditions at once:

1. the response at the interferer angle is zero, $\mathbf{w}^{T}\mathbf{v}(\theta_1) = 0$;
2. $\mathbf{w}$ stays as close to $\mathbf{w}_\text{d}$ as possible, so the main beam does not move and does not lose more gain than it must.

The first condition is one complex equation in eight complex unknowns, so there are many solutions. The second condition picks one, and it picks a change along $\mathbf{w}_\text{n}$, the beam aimed at the interferer. Split any change $\Delta\mathbf{w} = \mathbf{w} - \mathbf{w}_\text{d}$ into a part along $\mathbf{w}_\text{n}$ and a part $\mathbf{u}$ orthogonal to it, $\mathbf{w}_\text{n}^{H}\mathbf{u} = 0$. Since $\mathbf{v}(\theta_1) = \mathbf{w}_\text{n}^{*}$, the orthogonal part contributes $\mathbf{u}^{T}\mathbf{v}(\theta_1) = \mathbf{w}_\text{n}^{H}\mathbf{u} = 0$ at the interferer. It does nothing toward the null and only lengthens the change, so the smallest change that places the null is a multiple of $\mathbf{w}_\text{n}$ alone.

The figure draws that geometry as if the eight complex weights were two-dimensional arrows; it is a schematic, not to scale. Removing the part of $\mathbf{w}_\text{d}$ that lies along $\mathbf{w}_\text{n}$ leaves $\mathbf{w}$ at right angles to $\mathbf{w}_\text{n}$, which is the null. When the interferer sits on a sidelobe, $\mathbf{w}_\text{d}$ and $\mathbf{w}_\text{n}$ are nearly perpendicular and little is removed. When it sits near the main lobe, they nearly line up, and removing the shared part removes most of the beam with it. The cosine of the angle between them is $\vert r_\text{n}\vert$, and the look direction keeps $1 - \vert r_\text{n}\vert^2$ of its response.

**Build the beam that points at the interferer.** Define the second steering weight vector exactly as we defined the first, but aimed at $\theta_1$:

$$
\mathbf{w}_\text{n} = \mathbf{v}^{*}(\theta_1), \qquad w_{\text{n},n} = e^{-jnkd\sin\theta_1}.
$$

Applied on its own, $\mathbf{w}_\text{n}$ would point a full-gain beam straight at the interferer. That is the opposite of the goal, but subtracting part of it from $\mathbf{w}_\text{d}$ produces the null.

**Subtract some of it.** Try a weight vector of the form

$$
\mathbf{w} = \mathbf{w}_\text{d} - r_\text{n}\ \mathbf{w}_\text{n},
$$

with one complex number $r_\text{n}$ still to be chosen. Any $r_\text{n}$ leaves the main beam roughly in place, because we are subtracting a small multiple of a vector that points somewhere else. One particular $r_\text{n}$ makes the response at $\theta_1$ vanish.
::::

::::{frame} The Weight-Subtraction Rule
:::{present}
$$
\begin{aligned}
y(\theta_1) &= \mathbf{w}_\text{d}^{T}\mathbf{v}(\theta_1) - r_\text{n}\ \mathbf{w}_\text{n}^{T}\mathbf{v}(\theta_1) \\
&= \mathbf{w}_\text{n}^{H}\mathbf{w}_\text{d} - r_\text{n}\ \mathbf{w}_\text{n}^{H}\mathbf{w}_\text{n} = 0 \\
r_\text{n} &= \frac{\mathbf{w}_\text{n}^{H}\mathbf{w}_\text{d}}{\mathbf{w}_\text{n}^{H}\mathbf{w}_\text{n}}
\end{aligned}
$$

- One division gives an exact null, with no iteration.
:::
:::{present}
<img src="../../viz/img/L24-cancel-phasors.svg"
     alt="Phasors at the interferer angle of 22.5 degrees, at 10.0 GHz. The desired beam's eight unit phasors turn 64.3 degrees per element and wind around to end at 1.83 at 45.0 degrees. The subtracted beam's eight phasors, each 0.229 long, lie in a straight line and end at the same point, so the difference is zero"
     style="max-width: 420px; width: 100%; display: block; margin: 0 auto;">
:::

We substitute the trial weights into the response at the interferer. The superscript $H$ is the **conjugate transpose**: $\mathbf{a}^{H}\mathbf{b} = \sum_n a_n^{*} b_n$. Because $\mathbf{w}_\text{n} = \mathbf{v}^{*}(\theta_1)$, the steering vector at the interferer is $\mathbf{v}(\theta_1) = \mathbf{w}_\text{n}^{*}$, and every product with it becomes a conjugate-transpose product:

$$
\begin{aligned}
\mathbf{w}_\text{d}^{T}\mathbf{v}(\theta_1) &= \sum_n w_{\text{d},n}\ w_{\text{n},n}^{*} = \mathbf{w}_\text{n}^{H}\mathbf{w}_\text{d} \\
\mathbf{w}_\text{n}^{T}\mathbf{v}(\theta_1) &= \sum_n \vert w_{\text{n},n}\vert^2 = \mathbf{w}_\text{n}^{H}\mathbf{w}_\text{n} = N .
\end{aligned}
$$

The first is the desired beam's own response toward the interferer; the second is $N$ because every entry of $\mathbf{w}_\text{n}$ has unit magnitude. Setting the response to zero then fixes $r_\text{n}$, the chain at the top of the frame: with that $r_\text{n}$ the two terms of the second line are equal, so the response at $\theta_1$ is zero.

The figure shows the two terms as phasor chains at $\theta_1 = 22.5^\circ$. The desired beam's eight unit phasors each turn $\psi_1 = 64.3^\circ$ from the last at the worked example's $10.0$ GHz, so they wind around and end at $N r_\text{n}$, a point $1.83$ from the origin. The subtracted beam was built to cancel that turning, so all eight of its phasors point the same way; scaled by $r_\text{n}$, each is $0.229$ long and they reach the same point in a straight line. The null is the difference between two chains that end at the same place.
::::

::::{frame} The Projection Coefficient
:::{present}
$$
\begin{aligned}
r_\text{n} &= \frac{1}{N}\sum_{n=0}^{N-1} e^{jnkd\sin\theta_1} \\
&= \frac{y_\text{uniform}(\theta_1)}{N}
\end{aligned}
$$

- On a $-13$ dB sidelobe, $\vert r_\text{n}\vert = 0.22$.
- In the main lobe, $\vert r_\text{n}\vert \to 1$.
- In a natural null, $r_\text{n} = 0$ and the weights do not change.
:::

The ratio $r_\text{n} = \mathbf{w}_\text{n}^{H}\mathbf{w}_\text{d}/\mathbf{w}_\text{n}^{H}\mathbf{w}_\text{n}$ is a **projection**: it measures how much of the null-direction beam is already contained in the desired beam. Subtracting $r_\text{n}\mathbf{w}_\text{n}$ removes precisely that much and no more, which is why the main beam survives.

There is a second reading that is more useful at the board. Expand the numerator for a broadside beam, $\mathbf{w}_\text{d} = [1, 1, \ldots, 1]$:

$$
r_\text{n} = \frac{1}{N}\sum_{n=0}^{N-1} e^{jnkd\sin\theta_1} = \frac{1}{N}\ y_\text{uniform}(\theta_1).
$$

The projection coefficient is the uniform array's own normalized pattern evaluated at the null angle. If the interferer sits on a $-13$ dB sidelobe, then $\vert r_\text{n}\vert = 0.22$. If it sits in the main lobe, $\vert r_\text{n}\vert$ approaches 1 and we are subtracting nearly the whole beam. If it happens to sit in one of the array's natural pattern nulls, $r_\text{n} = 0$, the rule returns $\mathbf{w} = \mathbf{w}_\text{d}$ unchanged, and the null was already there.

:::{callout}
$r_\text{n}$ is the uniform pattern's level at the null angle, and it sets the main-lobe loss before we compute any weight.
:::
::::

::::{frame} Weights on a Circle
:::{present}
$$
w_n = 1 - r_\text{n}\ e^{-jn kd\sin\theta_1}
$$

- Each weight tip sits on a circle of radius $\vert r_\text{n}\vert$ around 1.
- Amplitudes stay within $1 \pm \vert r_\text{n}\vert$; phases move a few degrees.
- A null is a small change to the original beam.
:::
:::{present}
<img src="../../viz/img/L24-weight-circle.svg"
     alt="The eight weights for a null at 22.5 degrees at 10.0 GHz, plotted in the complex plane on a circle of radius 0.229 about 1. Elements 1 and 8, 2 and 7, 3 and 6, 4 and 5 are mirror images across the real axis. A line from the origin to element 3 shows its phase of plus 13.1 degrees"
     style="max-width: 520px; width: 100%; display: block; margin: 0 auto;">
:::

Geometrically, each element weight is the number 1 minus a phasor of length $\vert r_\text{n}\vert$ that rotates by $kd\sin\theta_1$ from element to element. The eight weight tips lie on a circle of radius $\vert r_\text{n}\vert$ centered on the original weight, so the amplitudes spread between $1 - \vert r_\text{n}\vert$ and $1 + \vert r_\text{n}\vert$ and the phases vary a few degrees either side of the ramp. A null is a small, structured perturbation of the original beam. The figure plots the eight weights of the $22.5^\circ$ example. Each one's gain is its distance from the origin and its phase is the angle of the line from the origin, which is why the phases stay within $13^\circ$. Elements mirrored about the array center land at mirror points across the real axis, the conjugate pairs that make the gains symmetric and the phases antisymmetric.
::::

::::{frame} Worked Example: Null at +22.5°
:::{present}
$$
\begin{aligned}
\psi_1 &= kd\sin\theta_1 = 2.932\ \sin 22.5^\circ \\
&= 64.3^\circ \\
r_\text{n} &= \frac{1}{8}\sum_{n=0}^{7} e^{jn(64.3^\circ)} \\
&= 0.229\ \angle\ 45.0^\circ
\end{aligned}
$$

- $\vert r_\text{n}\vert$ is $-12.8$ dB, the first sidelobe level.
:::

Take the course array, eight elements on a $d = 14\ \text{mm}$ pitch, and work the example at $10.0\ \text{GHz}$, so $\lambda = 30.0\ \text{mm}$, $d/\lambda = 0.467$, and $kd = 2\pi(0.467) = 2.932$ rad. That frequency is well away from any kit's HB100, so the numbers here show the method without answering your Part 1, which you work at your own kit's frequency. Point the beam at broadside and null an interferer at $\theta_1 = +22.5^\circ$.

The chain on the slide runs in two steps. The element-to-element phase at the null angle is $\psi_1 = kd\sin\theta_1 = 64.3^\circ$. The beam is broadside, so $\mathbf{w}_\text{d}$ is all ones and $r_\text{n}$ is the uniform pattern at $22.5^\circ$: $0.229$ at $45.0^\circ$, or $20\log_{10}(0.229) = -12.8$ dB, the first sidelobe level of the uniform 8-element array. Element by element, the weights are $w_n = 1 - r_\text{n}\ e^{-jn\psi_1}$, and their eight magnitudes lie between 0.79 and 1.20, inside the circle's bounds $1 \pm 0.229$.
::::

::::{frame} The PHASER Settings
:::{present}
| Element | Gain (%) | Phase (deg) |
| :-- | --: | --: |
| 1 | 71 | $-10.9$ |
| 2 | 66 | $+5.5$ |
| 3 | 83 | $+13.1$ |
| 4 | 100 | $+5.8$ |
| 5 | 100 | $-5.8$ |
| 6 | 83 | $-13.1$ |
| 7 | 66 | $-5.5$ |
| 8 | 71 | $+10.9$ |

- A sign error in these $13^\circ$ offsets is easy to miss.
:::

The Element Gains sliders are percentages of full scale, so scale the largest weight to 100 % and enter the weight angles as phase offsets:

$$
\text{gain}_n = \frac{100\ \vert w_n\vert}{\max_m \vert w_m\vert}\ \%, \qquad \phi_n = \angle w_n .
$$

The table assumes the Element Gains slider is linear in voltage, as it is on current Phaser software. Enter each phase with its sign. A Phase Control offset is the weight's own phase, the same convention **Apply** uses when it writes $-n\Delta\phi$ to steer to $+\theta_0$ (<a href="../L18-lab-beam-steering/index.html#frame-the-sign-in-phase-control">L18 Lab</a>). <a href="../L18-beam-steering/index.html#frame-sign-of-the-compensating-ramp">Lesson 18</a>'s $+n\Delta\phi$ is the backend's delay setting, which carries the opposite sign, so these offsets are entered as computed and not converted to it.

The gains are symmetric and the phases are antisymmetric, and every null placed to one side of a broadside beam produces that pattern. The reason is in $r_\text{n}$. Summing the geometric series gives

$$
r_\text{n} = e^{j(N-1)\psi_1/2}\ \frac{\sin(N\psi_1/2)}{N\sin(\psi_1/2)},
$$

a real number times the phase $(N-1)\psi_1/2$, so $w_n = 1 - r_\text{n}e^{-jn\psi_1}$ carries the phase $(N-1-2n)\psi_1/2$ in its second term. Replacing $n$ with $N-1-n$ flips the sign of that phase, so $w_{N-1-n} = w_n^{*}$: elements mirrored about the center have equal gains and opposite phases. Note how small the phase offsets are: the largest is 13 degrees. Null steering is not a large change to the array's settings, and that is precisely why it is so easy to get wrong by a sign.
::::

::::{frame} The Notch on the Pattern
:::{present}
<img src="../../viz/img/L24-pattern-null.svg" alt="Uniform and null-steered patterns of the 8-element array at 10.0 GHz: the null-steered beam stays at broadside, 2.1 dB lower, and drops to an exact null at plus 22.5 degrees" style="max-width: 640px; width: 100%; display: block; margin: 0 auto;">
:::
:::{present}
- The response at $+22.5^\circ$ is exactly zero, and the beam stays at broadside.
- The peak drops 2.1 dB, and the beam stays at broadside.
:::

The response at $+22.5^\circ$ is exactly zero. The main beam stays at broadside and its peak drops 2.1 dB, of which 0.5 dB is the subtraction itself and the rest is the rescaling that keeps every gain at or below 100 %.
::::

::::{frame} Null Steering on the PHASER
:class: viz-frame

:::{depth}
The widget below applies the weight-subtraction rule to the course array and draws the result. Drag the null angle and watch three things: where the notch lands, how the eight element gains and phases redistribute, and how the main-lobe loss pill tracks $\vert r_\text{n}\vert$ rather than the null angle itself. Then switch the weights from Ideal to PHASER, which rounds every phase to the ADAR1000's $2.8125^\circ$ step and every gain to 1 %, and adds a floor at the shallow end of the depth my kit measured, so the notch is no longer infinitely deep and settles near what the hardware showed. The widget works at the lesson's $10.0$ GHz.
:::

<iframe src="../../viz/null-steering.html"
        width="100%" height="438"
        style="border: 1px solid #cddce9; border-radius: 6px;"
        loading="lazy"
        title="Null steering on the 8-element PHASER array: pattern, element weights, and null depth">
</iframe>
::::

::::{frame} Main-Lobe Loss Versus Null Angle
:::{present}
<img src="../../viz/img/L24-cost-vs-angle.svg" alt="Main-lobe loss versus null angle for the 8-element array at 10.0 GHz, split into the subtraction term, which climbs steeply toward the main lobe, the rescaling term, which turns negative inside about 6 degrees, and their total, 2.1 dB at plus 22.5 degrees" style="max-width: 640px; width: 100%; display: block; margin: 0 auto;">
:::
:::{present}
- The loss grows from 2.1 dB at $22.5^\circ$ to 3.3 dB at $10^\circ$ and 8.6 dB at $5^\circ$.
- Two sources inside one beamwidth can't be separated; move the beam.
:::

**The main-lobe loss is set by $\vert r_\text{n}\vert$.** The subtracted beam's response in the look direction is the conjugate of the projection: since $\mathbf{v}(\theta_0) = \mathbf{w}_\text{d}^{*}$, the product $\mathbf{w}_\text{n}^{T}\mathbf{v}(\theta_0) = \mathbf{w}_\text{d}^{H}\mathbf{w}_\text{n} = N r_\text{n}^{*}$. So the response at $\theta_0$ is

$$
\begin{aligned}
y(\theta_0) &= \mathbf{w}_\text{d}^{T}\mathbf{v}(\theta_0) - r_\text{n}\ \mathbf{w}_\text{n}^{T}\mathbf{v}(\theta_0) \\
&= N - r_\text{n}\ N r_\text{n}^{*} = N\left(1 - \vert r_\text{n}\vert^2\right),
\end{aligned}
$$

a loss of $0.47$ dB for the $22.5^\circ$ example at $10.0$ GHz. The Element Gains sliders then divide every weight by the largest magnitude, $\max\vert w_n\vert = 1.200$, which loses another $20\log_{10}(1.200) = 1.58$ dB, so the total loss is

$$
\begin{aligned}
L &= -20\log_{10}\frac{1 - \vert r_\text{n}\vert^2}{\max_n \vert w_n\vert} \\
&= 0.47 + 1.58 = 2.1\ \text{dB}.
\end{aligned}
$$

Move the null in toward the beam and the subtraction term grows fast: 1.9 dB at $\theta_1 = 10^\circ$, 5.8 dB at $7^\circ$, and 10.5 dB at $5^\circ$. The rescaling term does the opposite. It is 1.4 dB at $10^\circ$ and 0.2 dB at $7^\circ$, and at $5^\circ$ every weight magnitude is below 1, so scaling the largest up to 100 % raises the beam 1.9 dB. The totals are 3.3, 6.0, and 8.6 dB. As $\theta_1$ enters the main lobe $\vert r_\text{n}\vert \to 1$, the eight weights cancel one another, and what is left after rescaling is a split beam with a hole where the target used to be. Two sources inside one beamwidth can't be separated by a null; the answer is to move the beam or wait for the geometry to change.
::::

::::{frame} Quantization and Null Depth
:::{present}
$$
\begin{aligned}
\frac{\vert y(\theta_1)\vert}{N} &\approx \frac{\epsilon_\text{rms}}{\sqrt{N}} \\
\epsilon_\text{rms} &= \sqrt{\sigma_\phi^2 + \sigma_a^2} \\
\sigma_\phi &= \frac{\text{LSB}}{\sqrt{12}}
\end{aligned}
$$

- One-step channel errors set how deep a null can go.
- Three bits allow only about 22 dB.
:::
:::{present}
<img src="../../viz/img/L24-error-phasors.svg"
     alt="The eight weight errors as phasors at the null angle, referred to the array center. Left, rounding this table: the errors come in mirror pairs whose sums lie on the real axis, so the total stays real. Right, independent channel errors of one step: the eight phasors point in random directions and add up to a point near a dashed circle of radius root N times epsilon"
     style="max-width: 600px; width: 100%; display: block; margin: 0 auto;">
:::

The weights above are exact real numbers, and the ADAR1000 accepts neither. Each element's phase lands on a $2.8125^\circ$ grid and each gain on a 1 % grid, so each weight carries a small error $\delta w_n$. If those errors are independent, at the null angle they add in RMS rather than coherently, and the residual response relative to the beam peak is the estimate on the slide. The figure draws the eight errors at the null, each turned by its own steering-vector phase. Each piece of that estimate has a mechanism. Rounding to the nearest step leaves an error spread evenly between $-\text{LSB}/2$ and $+\text{LSB}/2$, and a uniform spread of width LSB has an RMS value of $\text{LSB}/\sqrt{12}$. A small phase error $\delta\phi$ moves a weight of magnitude near 1 by about $\delta\phi$, so the phase and gain errors both count as fractions of a unit weight and add in quadrature to $\epsilon_\text{rms}$. At the null the exact weights sum to zero, so the response is the sum of the eight errors alone, each turned by its own steering-vector phase. Independent errors add in power, not in voltage, so their sum has an RMS size of $\sqrt{N}\ \epsilon_\text{rms}$, and dividing by the beam peak $N$ gives $\epsilon_\text{rms}/\sqrt{N}$.

Part 1 of the L24 Lab packet puts the ADAR1000's numbers into this estimate: its $2.8125^\circ$ phase step and 1 % gain step. The result sits on the same $-6B$ scale as the quantization sidelobes of <a href="../L23-beam-squint-quantization/index.html#frame-quantization-sidelobes">Lesson 23</a>, a few decibels deeper because the error is spread over eight elements. Halve the bits and the floor rises fast: a 3-bit phase shifter cannot hold a null deeper than about 22 dB.

Rounding this particular table does less damage than the estimate, as the left half of the figure shows. Rounding keeps the gains symmetric and the phases antisymmetric (the mirror pairs of <a href="#frame-the-phaser-settings">The PHASER Settings</a>), so each pair sums to a real number, the pattern referred to the array center stays real and still passes through zero, and the null only moves a fraction of a degree. What fills a null on the kit is error that does not share that symmetry: each channel's own calibration residue in gain and phase. The estimate is the depth those errors allow when they are about one step in size.
::::

::::{frame} Measured Null Depth
:::{present}
<img src="../../viz/img/L24-quant-depth.svg" alt="Exact and ADAR1000-rounded null patterns at 10.0 GHz, both still reaching zero near plus 22.5 degrees, and the band from minus 46 to minus 50 dB measured on a course kit" style="max-width: 640px; width: 100%; display: block; margin: 0 auto;">
:::
:::{present}
- In an open room the notch reaches 46 to 50 dB below the uniform peak.
- In a cramped room reflections fill it to 22 to 24 dB.
- The interferer ends up 34 to 38 dB below the target.
:::

The estimate is what the hardware shows. With the table above loaded, my kit's notch bottomed out 46 to 50 dB below the uniform peak in an open room, the depth one-step channel errors allow. The interferer of the first frame, 10 dB stronger than the target, now arrives 34 to 38 dB below it, where the uniform taper left it at $-3$ dB.

The room sets a second limit. In a cramped space the same table bottomed out only 22 to 24 dB down: the HB100's own tone was still there in the notch, because a reflection arriving from another direction, about 22 dB below the direct path, filled it. So when a notch reads much shallower than 40 dB, look at the room before the arithmetic. A wall or a person beside the kit fills it, a stale calibration fills it, and a sign error on the phase column puts it on the wrong side of the sweep, where it is easy to miss.
::::

::::{frame} Up to N−1 Nulls, All Static
:::{present}
- One of the eight weights holds the beam, which leaves at most seven nulls.
- Nulls at both $\pm 22.5^\circ$ lower the main lobe 3.6 dB.
- Every weight assumed a known $\theta_1$. If the interferer moves, recompute.
:::

An $N$-element array has $N$ complex weights. One holds the main beam, which leaves at most $N-1$ independent nulls. The PHASER can therefore null up to seven directions at once, though long before that the pattern has been so heavily reshaped that the main lobe is barely recognizable. The procedure generalizes by subtracting one term per interferer and solving the resulting small system. Each null lowers the main lobe further: at $10.0$ GHz, nulls at both $\pm 22.5^\circ$ lower it 3.6 dB, against 2.1 dB for the one at $+22.5^\circ$.

We computed every number so far from an angle we had to know in advance. If the interferer moves, the null stays where it was and someone has to recompute and reload eight gains and eight phases. The next two nulls need no such angle: one comes from the array's symmetry, and one from the data the array receives.
::::

::::{frame} The Difference Beam
:::{present}
- **Beam 1 Phase** $= 180^\circ$ subtracts the two channels.
- The halves cancel where they arrive in phase; a peak rises on each side.
:::
:::{present}
:class: callout

A computed null sits where we solved for it; a structural null sits where the two subarrays cancel.
:::

There is a second null on this board that needs no computation at all. Each ADAR1000 sums its four elements into one RF channel, so the PHASER hands the Pluto two **digital subarray channels**, one for elements 1–4 and one for elements 5–8. Adding them is the ordinary sum beam. Subtracting them, by setting Beam 1 Phase to $180^\circ$, gives the **difference beam**:

$$
\Delta(\theta) = \sum_{n=0}^{3} e^{jn\psi} - \sum_{n=4}^{7} e^{jn\psi},
\qquad \psi = kd\sin\theta .
$$

Wherever the two halves arrive in phase they cancel, and on each side of that null a peak rises. Part 1 of the lab packet has you show where the null sits and find the two peaks. This is the **monopulse difference beam**, which the monopulse frames at the end of this lesson use for angle measurement.

The $+22.5^\circ$ notch exists because we solved for eight weights, and it moves only when we solve again. The difference null exists because the two subarrays are identical, and it stays put no matter what the signal does. With no arithmetic behind it, its depth on the kit is a direct reading of what the room lets through: about 40 dB in an open room, and the same 22 dB or so as the notch in a cramped one.
::::

::::{frame} MVDR
:::{present}
$$
\mathbf{w}_\text{mvdr} = \frac{\mathbf{R}^{-1}\mathbf{s}}{\mathbf{s}^{H}\mathbf{R}^{-1}\mathbf{s}}
$$

- Minimum output power, with unit gain in the look direction $\mathbf{s}$.
- It estimates $\mathbf{R}$ from the data; nobody supplies the interferer's angle.
- Two channels leave one null, and the target must sit where the beam points.
:::

The computed notch needed the interferer's angle, and the difference null needed the array's symmetry. The **MVDR** (minimum-variance distortionless-response) beamformer needs neither. It estimates the covariance of what the two channels receive over $K$ snapshots,

$$
\hat{\mathbf{R}} = \frac{1}{K}\ \mathbf{X}\mathbf{X}^{H},
$$

and solves for the weights that minimize total output power while holding unit gain in the look direction $\mathbf{s}$. MVDR suppresses whatever is loud and is not in the look direction, and nobody has to tell it where that is. With two digital channels it has two weights: one holds the look direction and the other places one null, so it can place one null. The Phaser measures $\mathbf{s}$ from the target itself, from the samples taken before the interferer is added, so MVDR protects the HB100 as the two channels actually receive it. That works only when the target sits where the beam points.

Unit gain means the two MVDR weights sum to 1 in the look direction, where Manual's two weights of 1 sum to 2. The Phaser multiplies the MVDR output by 2, the number of channels, so a target in the look direction reads the same level under either mode, and we compare the two on one scale.
::::

::::{frame} Two Limits of Two Channels
:::{present}
- Near $\pm 30^\circ$ the subarray pattern already puts the interferer in a null.
- There the channel phase difference wraps a full cycle: nulling the interferer would null the target.
- The lab runs MVDR at $+20^\circ$.
:::

Both limits belong to the architecture rather than to the algorithm. A four-element subarray at $d = 14$ mm has its first null where $\sin\theta = \lambda/4d$, about $31^\circ$, so an interferer there barely reaches either channel and there is little left for the digital layer to remove. The two channels sit four elements apart, so their phase difference, $4kd\sin\theta$, runs through a full cycle across the subarray beam: a source near $+30^\circ$ presents very nearly the same channel phase difference as one on boresight, and the two channels cannot tell them apart. The digital layer can only work on what the analog layer passes it, and only on directions the two channels can distinguish.

At $+30^\circ$ both limits act at once. To the two channels the interferer looks almost like the target, so a null on it would land on the target too, and MVDR keeps the target it measured: it leaves the interferer where the subarray pattern put it. **Diagonal loading** guards the weights. The Phaser adds $\delta\ \text{tr}(\hat{\mathbf{R}})/2$ to the diagonal of $\hat{\mathbf{R}}$ before inverting it, which caps how far the weights can move from Manual's and keeps a source near the look direction from driving them to large values that amplify the noise. At $\delta = 0.1$ the weights still move far enough to suppress an interferer at $+20^\circ$ by 10 dB or more on a kit, so the lab uses $\delta = 0.1$. At $\delta = 1$ the weights barely move from Manual's and the suppression mostly disappears.

The lab also uses $K = 1024$ snapshots rather than 128. At the kit's 3 MSPS, 128 samples span only four cycles of the 100 kHz offset between target and interferer, so the two are partly correlated in each estimate of $\hat{\mathbf{R}}$ and the null wanders from one update to the next. 1024 samples span 34 cycles, which holds the null still.
::::

::::{frame} What MVDR Chooses
:class: viz-frame

:::{depth}
The widget is the two-channel digital layer on its own, with the analog subarrays parked at boresight. Move the interferer to about $+20^\circ$ and watch MVDR place a null on it. Then move it out toward $\pm 30^\circ$ and watch the suppression fall away, for the two reasons on the previous frame. Watch what the null takes from the rest of the pattern, too: the sidelobes rise elsewhere, and the null repeats, because two channels four elements apart respond the same to directions $\lambda/4d$ apart in $\sin\theta$. In the lab you hold the beam on the target in Signal vs Time: the readout tiles give the suppression, and the Rectangular tab draws the held beam's pattern with the interferer marked. A beam-sweep trace is the total power at each angle, interferer and target together, so it shows the null but does not measure it.
:::

<iframe src="../../viz/mvdr-interferer.html"
        width="100%" height="489"
        style="border: 1px solid #cddce9; border-radius: 6px;"
        loading="lazy"
        title="Two-channel MVDR beamformer against an interferer">
</iframe>
::::

::::{frame} Manual Versus Adaptive
:::{present}
| | Manual null | MVDR |
| :-- | :-- | :-- |
| Needs first | the interferer's angle | nothing |
| Interferer moves | recompute eight weights | follows it |
| Nulls on this board | up to seven | one |
:::

Manual null steering has eight degrees of freedom and can place several nulls at once, but every one of them is our arithmetic, computed for a geometry we assumed. MVDR has two degrees of freedom on this board, one constraint and one null, and it finds that null itself, from data, several times a second. On an array with a digitizer behind every element, adaptive beamforming has both advantages at once. On the PHASER we can see what the hybrid architecture of <a href="../L17-phased-array-hardware/index.html#frame-the-hybrid-beamformer">Lesson 17</a> loses: the analog sums discard the per-element information before the algorithm sees it.
::::

::::{frame} Sum and Delta
:::{present}
<img src="../../viz/img/L24-monopulse.svg"
     alt="Top: sum and delta beam levels from minus 20 to plus 20 degrees at 10.0 GHz; the sum is flat at its peak while the delta passes through a zero on the target. Bottom: the error the GUI plots, the delta over sum ratio signed by side, zero on the target, close to a straight line of slope 0.10 per degree near it, clamped at plus and minus 1, and flipping sign past the sum beam's first nulls"
     style="max-width: 520px; width: 100%; display: block; margin: 0 auto;">
:::
:::{present}
- The sum is flat on the target; the delta climbs out of a zero.
- Their ratio, signed by side, turns one look into an angle.
:::

Every measurement so far has come from a sweep: the array steps its commanded angle across the field of view and records power at each step. A sweep takes time, and a tracking radar does not have it. **Monopulse** forms two beams at once from the two subarray channels: their sum, $\Sigma$, and their difference, $\Delta$, the channel of elements 5–8 subtracted from the channel of elements 1–4. The sum beam is flat at its peak, so its level barely changes as the target drifts a degree off the beam. The delta beam is zero where the two channels arrive in phase and climbs steeply out of that zero, so its level changes a great deal over the same degree. Dividing one by the other turns that small angle into a large, readable number.
::::

::::{frame} The Error Function
:::{present}
$$
\begin{aligned}
\varepsilon &= \text{sign}\left(\angle\ \Sigma\Delta^{*}\right) \frac{\vert\Delta\vert}{\vert\Sigma\vert} \\
&= \pm\ \vert\tan 2\psi\vert \\
&\approx 2kd\ \theta
\end{aligned}
$$

- Its sign says which side of the beam the target is on.
- At $10.0$ GHz the slope is $0.10$ per degree, straight within about $\pm 5^\circ$.
:::

With each subarray summing four elements, the two channels differ only by the phase $4\psi$ between their centers, so $\Sigma \propto 1 + e^{j4\psi}$ and $\Delta \propto 1 - e^{j4\psi}$. Their ratio has magnitude $\vert\tan 2\psi\vert$, which is zero on the target and, for a small offset, close to $2\psi = 2kd\sin\theta \approx 2kd\ \theta$, with $\theta$ the target's angle from the beam in radians. The magnitude alone cannot say which side the target is on. The phase can: $\Sigma\Delta^{*}$ is purely imaginary, $\Delta$ arriving a quarter cycle ahead of $\Sigma$ on one side of the beam and a quarter cycle behind on the other, so the sign of that phase is the side. The kit reads a positive error when the target sits on the $+\theta$ side of the beam.

At $10.0$ GHz, $kd = 2.932$ rad, so the slope is $2kd = 5.86$ per radian, or $0.10$ per degree. The ratio does not depend on the signal level, because both beams scale together. The GUI clamps the plotted error at $\pm 1$, which it reaches about $8^\circ$ off the beam here. Past the sum beam's first nulls the sign flips, so the error points the wrong way once the target is more than a beamwidth off.
::::

::::{frame} Closing the Loop
:::{present}
- One sweep finds the target; after that the beam holds and reads $\varepsilon$.
- Each update steps the steering phase one LSB, about $1^\circ$, toward the side $\varepsilon$ points.
- A radar steps in proportion to $\varepsilon$, so it closes faster.
:::

A tracker turns the error into motion. On the PHASER, choosing Tracking from the Mode menu runs ADI's monopulse loop. The first update is an ordinary sweep that locks the beam on the strongest return. Every update after that holds the beam at its current steering phase, forms $\Sigma$ and $\Delta$ there, and moves the steering phase one $2.8125^\circ$ LSB, about $1^\circ$ of angle near boresight, toward the side the sign of $\varepsilon$ points. On the target the sign dithers, and the beam settles within one step of it. The loop keeps running until the mode changes.

Stepping by the sign alone is the simplest loop that works: it needs no slope, and a level change cannot upset it. It is also slow: a source that moves more than about one step per update outruns it, and one that moves past the sum beam's first null, where the sign flips, is lost. A tracking radar steps in proportion to the error, a large correction when the target is far off and a small one near it, which is why the slope matters: it converts the reading into degrees. The loop uses the two digital channels as the manual beamformer forms them, with both digital beams at $0^\circ$; MVDR forms no delta beam, so there is no error to track under it.
::::

::::{frame} Summary
:class: read-only

| Symbol / idea | What it is | Number to remember |
| :-- | :-- | :-- |
| $\mathbf{v}(\theta)$ | steering vector, $v_n = e^{jnkd\sin\theta}$ | the direction, not the setting |
| $\mathbf{w}_\text{d} = \mathbf{v}^{*}(\theta_0)$ | beam-steering weights | the L18 phase ramp, written as a vector |
| $\mathbf{w} = \mathbf{w}_\text{d} - r_\text{n}\mathbf{w}_\text{n}$ | weight-subtraction rule | zero response at $\theta_1$ |
| $r_\text{n} = \mathbf{w}_\text{n}^{H}\mathbf{w}_\text{d} / \mathbf{w}_\text{n}^{H}\mathbf{w}_\text{n}$ | projection of the null beam on the desired beam | $= $ uniform pattern level at $\theta_1$ |
| Main-lobe loss, null at $+22.5^\circ$, $10.0$ GHz | subtraction plus rescaling | 2.1 dB |
| PHASER settings, null at $+22.5^\circ$, $10.0$ GHz | gains | 71, 66, 83, 100, 100, 83, 66, 71 % |
| Notch depth | one-step channel errors, then the room | $-46$ to $-50$ dB open, $-22$ to $-24$ dB cramped |
| Difference beam | Beam 1 Phase $= 180^\circ$ subtracts the two channels | a structural null, no computed weight |
| MVDR | $\mathbf{w} = \mathbf{R}^{-1}\mathbf{s} / (\mathbf{s}^{H}\mathbf{R}^{-1}\mathbf{s})$ from $K$ snapshots | one null from two channels; loading $0.1$, $K = 1024$ |
| Monopulse error | $\vert\Delta\vert/\vert\Sigma\vert$, signed by side, from one look | zero on the target, slope $2kd$ per radian; $0.10$ per degree at $10.0$ GHz |
| Tracking | one LSB per update, by the error's sign | settles within one step of the target |
| Maximum nulls | one weight holds the beam | $N - 1 = 7$ manual, one adaptive |
::::

::::{frame} Looking Ahead
:::{present}
- The **L24 Lab** measures all four nulls on your kit.
- Lesson 25 begins radar: the range equation puts a power budget behind the monopulse angle measurement.
:::

In the L24 Lab you load your own gain and phase table and measure the notch, set Beam 1 Phase to $180^\circ$ and measure the difference null, run MVDR against a simulated interferer and watch its null on the held beam's pattern, and watch the monopulse tracker follow the HB100. Read the Digital Beam Forming section of the GUI inventory before class, so the Mode, Snapshots, and Diagonal Load controls are not new to you.

Lesson 25 derives the radar range equation and asks how much power comes back from a target that transmits nothing of its own. Everything Module 3 built, beamwidth, sidelobes, scan loss, and steering, becomes the antenna terms in that equation, and the array becomes the front end of a radar. The monopulse pair measures a target's angle from a single look, which is what a radar needs to track something that moves.
::::

::::{frame} Pre-Lab
:class: read-only doc-links

Part 1 of the L24 Lab packet is the pre-lab. Do it before the lab period, at the HB100 frequency your kit reported in an earlier lab, and bring it to class: you check every reading you take in Part 2 against it.

| Part 1 | You predict | Checked in |
| :-- | :-- | :-- |
| Question 1 | $\psi_1$, the gain and phase table, $\vert r_\text{n}\vert$, the main-lobe loss, and what a sign error or a missing phase column does | Steps 6 to 9, Table A |
| Question 2 | the notch depth that one-step channel errors allow | Step 9, Table A |
| Question 3 | the difference null and the angles of its two peaks | Step 14, Table B |
| Question 4 | Manual's Interferer vs Target at $+20^\circ$, the channel phase difference at $+20^\circ$ and $+30^\circ$, and whether MVDR can remove an interferer at $+30^\circ$ | Steps 18 to 21, Table C |
| Question 5 | where the delta null and the error's zero sit, which side reads positive, the error's slope at your frequency, and how deep the delta null reads | Steps 25 to 27, Table D |

This lesson works its examples at $10.0\ \text{GHz}$, well away from any kit's HB100, so it shows the method without giving your answers. Work yours at your kit's frequency: that is the table you type in.

- <a class="doc-link" href="../../labs/ECE444_Lab_L24_NullSteering_blank.pdf" target="_blank" rel="noopener">L24 Lab packet, Part 1 (PDF)</a>
::::
