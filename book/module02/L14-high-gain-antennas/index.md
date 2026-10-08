---
frame_view: true
---

# L14 - High-Gain Antennas

::::{frame}
:class: title-frame

<div class="course-mark">ECE 444 · Fall 2026</div>

<h1 class="frame-title">High-Gain Antennas</h1>

<div class="title-rule"></div>

High gain means a large radiating area driven in phase.

Lesson 14 · Antennas, Phased Arrays, and Radar Systems · Dr. Neil Rogers
::::

::::{frame} Slides
:class: read-only

:::{admonition} Slides
:class: slides
<a href="../../slides/L14-high-gain-antennas.html" target="_blank" rel="noopener">html slides</a>
<a href="../../slides/L14-high-gain-antennas.html?print-pdf" target="_blank" rel="noopener">pdf slides</a>
<a href="../../slides/L14-high-gain-antennas.md" target="_blank" rel="noopener">raw markdown slides</a>
:::
::::

::::{frame} Learning Objectives

<ol class="lo-list lo-sublist" style="--module: '2'; --lo: '4'">
  <li>I can compute an aperture antenna's gain and beamwidth from its physical size, and explain why gain is fundamentally a statement about area.</li>
  <li>I can explain how a parabolic reflector's equal-path geometry turns a spherical wave into a plane wave, and identify what f/D, feed illumination, blockage, and spillover do to aperture efficiency.</li>
  <li>I can explain how a Yagi-Uda gets gain from parasitic elements, and how detuning the reflector and directors sets the phase that puts the beam endfire.</li>
  <li>I can describe the array as the third approach to high gain, and state why the next module is devoted to it.</li>
  <li>I can select an appropriate high-gain antenna for a given application and defend the choice with numbers.</li>
</ol>
::::

::::{frame} Where We Were
:::{present}
- Lesson 13 topped out at 20 dBi, enough for a short local link.
- A satellite at 36,000 km or a target ten miles out needs more.
- Every antenna today, from 20 to 40 dBi, gets its gain from coherent area.
:::

This is the last lesson in Module 2, and it closes the loop the module opened
with. You can now predict an antenna's pattern from its geometry, simulate it,
and measure it with a quantified statement of how much of the measurement to
believe. Everything today is a gain claim we already know how to check.
::::

::::{frame} The One Idea
:::{present}
$$G = \eta_{\text{ap}}\ \frac{4\pi A}{\lambda^{2}}$$

- High gain means a large radiating **area** driven in **phase**.
- An aperture is not big in meters. It is big in **wavelengths**.
- Reflectors, Yagis, and arrays are three ways to build that area.
:::
:::{present}
<img src="../../viz/img/L14-three-approaches.svg"
     alt="A reflector, a Yagi-Uda, and an array side by side, each with the coherent aperture it builds shaded: a mirror, detuned neighbors, or electronics set the phase across it"
     style="max-width: 640px; width: 100%; display: block; margin: 0 auto;">
:::

Every high-gain antenna ever built is a different scheme for assembling a big,
coherent aperture: a reflector collects area with a mirror, a Yagi collects it
from currents induced on its parasitic elements, and an array adds the area
one element at a time. Read the physics before the algebra — $A/\lambda^2$
counts how many square wavelengths the antenna spans, $\eta_{\text{ap}}$ is the
fraction of that area the antenna uses, and $A_e = \eta_{\text{ap}}A = G\lambda^2/4\pi$ is
the number Friis cares about.

The formula is the one Lesson 13 derived for the horn, and nothing about it is
specific to horns. Straight ahead of a flat aperture every phase factor in the
radiation integral is 1, so the radiation vector is the plain sum of the
aperture field $E_a$, and Lesson 2's directivity is

$$\begin{aligned}
D &= \frac{4\pi U_{\max}}{P_{\text{rad}}} \\
&= \frac{4\pi}{\lambda^2}\ \frac{\left\vert\int_A E_a\ dS'\right\vert^2}{\int_A \vert E_a\vert^2\ dS'} \\
&= \eta_{\text{ap}}\ \frac{4\pi A}{\lambda^2}
\end{aligned}$$

with

$$\eta_{\text{ap}} = \frac{\left\vert\int_A E_a\ dS'\right\vert^2}{A\int_A \vert E_a\vert^2\ dS'} \le 1$$

A uniform, in-phase field makes the fraction exactly 1. Every loss term in
this lesson is a way of making the numerator smaller than the denominator:
a darker rim, a phase error from a bumpy surface, a patch of the aperture
blocked by the feed. Hold on to this ratio; the next five frames each
evaluate a piece of it.
::::

::::{frame} The Circular-Dish Shortcut
:::{present}
$$G = \eta_{\text{ap}}\left(\frac{\pi D}{\lambda}\right)^{2}$$

- Every doubling of **diameter** adds 6 dB.
- Every doubling of **frequency** adds 6 dB on the same dish.
:::

For a circular dish, $A = \pi D^2/4$ and the aperture formula collapses to the
one to memorize. The second consequence is why the satellite industry keeps
moving up in frequency: the same dish on the roof gains 6 dB every time the
band doubles, until the surface tolerance limits it.
::::

::::{frame} Beamwidth and Aperture Size
:::{present}
$$\theta_\text{HP} \approx 70^\circ\ \frac{\lambda}{D}$$

- Double the dish: the beam halves and the gain climbs 6 dB.
- Those are the same statement.
:::
:::{present}
<img src="../../viz/img/L14-beam-patterns.svg"
     alt="Patterns of a uniform circular aperture and of the 10 dB-rule feed's aperture against angle times D over wavelength: the taper widens the beam from 59 to 67 degrees and lowers the first sidelobe from minus 17.6 to minus 25.1 dB"
     style="max-width: 560px; width: 100%; display: block; margin: 0 auto;">
:::

Lesson 6 established the Fourier logic: a wider aperture is a narrower beam,
and the beamwidth of an aperture of size $D$ scales as $\lambda/D$. Power the
antenna no longer sends sideways goes to boresight instead.

:::{depth}
The $70^\circ$ coefficient already assumes a tapered illumination. For a
uniform circular aperture of diameter $D$, Lesson 6's radiation vector is the
two-dimensional version of the line source's sinc: the integral of
$e^{+jk\hat{\mathbf r}\cdot\mathbf{r}'}$ over a disk, which is

$$\begin{aligned}
\vert\mathbf{N}(\theta)\vert &\propto \left\vert\frac{2J_1(u)}{u}\right\vert \\
u &= \frac{\pi D}{\lambda}\sin\theta
\end{aligned}$$

The half-power point is at $u = 1.616$, so the full beamwidth is

$$\begin{aligned}
\theta_\text{HP} &\approx 2\left(\frac{1.616}{\pi}\right)\frac{\lambda}{D} \\
&= 1.029\ \frac{\lambda}{D}\ \text{rad} \\
&= 59^\circ\ \frac{\lambda}{D}
\end{aligned}$$

with a first sidelobe at $-17.6$ dB. Nobody illuminates a dish uniformly,
and we will see why two parts from now: a feed that lights the rim 11 dB
below the center widens the beam to $67^\circ\lambda/D$ and pushes the
sidelobes to $-25$ dB. Feeds that taper harder widen it further, so $70^\circ$
is the round, slightly conservative design number. Use it for design, and use
the interactive below to build the reflex.

Eliminating $D$ between the gain formula and the beamwidth rule ties the two
together:

$$\begin{aligned}
G\ \theta_\text{HP}^2 &\approx \eta_{\text{ap}}\ \pi^2\ (70^\circ)^2 \\
&= 31{,}400\ \text{deg}^2
\end{aligned}$$

for $\eta_{\text{ap}} = 0.65$. That sits inside the 26,000 to 32,400 range
Lesson 2 gave for the pencil-beam estimate $D \approx 41{,}253/\theta_1\theta_2$,
which is the same statement from the pattern side: the narrower the beam, the
higher the gain.
:::
::::

::::{frame} Three Knobs on a Dish
:class: viz-frame

:::{present}
<iframe src="../../viz/reflector-gain.html"
        width="100%" height="401"
        style="border: 1px solid #cddce9; border-radius: 6px;"
        loading="lazy"
        title="Dish gain, beamwidth, and effective area versus diameter in wavelengths, with the Ruze surface-error penalty">
</iframe>

<p class="viz-note mathjax_process"><strong>Size</strong> \(D/\lambda\) moves gain and beam together. <strong>Efficiency</strong> and <strong>surface error</strong> only take gain away.</p>
:::

:::{depth}
The widget is the two formulas above with one more factor. The three sliders
are the three things a designer controls: how many wavelengths across the dish
is, the aperture efficiency $\eta_{\text{ap}}$, and the RMS surface error
$\sigma$. The readouts are what those buy: gain, beamwidth, effective area,
and the gain the surface error costs. Only the size appears in both formulas,
so it is the only slider that moves the beam. Surface error enters through
Ruze's formula, five frames on; for now read it as a third tax on the gain,
next to $\eta_{\text{ap}}$.

Drive the sliders and watch two numbers move together. Set $D/\lambda$ and the
dish redraws with a tick on the rim for every wavelength across it, while the
beam cone narrows on the same canvas. Notice that gain climbs 6 dB per
doubling of $D$ while the beam halves — and then open the surface-error slider
and watch the amber curve: hold the panel tolerance fixed and grow the dish,
and surface error quietly caps how far you can push it.
:::
::::

::::{frame} Worked Example — a 1 m Dish at 12 GHz
:class: read-only

A home satellite-TV dish, roughly 1 m across, receiving Ku band at 12 GHz.
Take $\eta_{\text{ap}} = 0.65$.

**Wavelength.** $\lambda = c/f = (3\times10^{8})/(12\times10^{9}) = 0.025\ \text{m}$,
so $D/\lambda = 40$ and the dish is forty wavelengths across.

**Gain.**

$$\begin{aligned}
G &= 0.65\ (\pi \cdot 40)^{2} \\
&= 0.65 \cdot 15791 \\
&= 1.03\times10^{4} \\
&= 40.1\ \text{dBi}
\end{aligned}$$

**Beamwidth.**

$$\theta_\text{HP} \approx 70^\circ\ \frac{0.025}{1} = 1.75^\circ$$

A dish that drifts two degrees off the satellite therefore loses the signal.

**Effective aperture.**

$$A_e = \eta_{\text{ap}}A = 0.65\ \pi(0.5)^2 = 0.51\ \text{m}^2$$

**Sanity check on the far field.** Lesson 5's far-field boundary is the
distance at which the path from the rim of a $D$-wide aperture is within
$\lambda/16$ of the path from its center:

$$\frac{2D^2}{\lambda} = \frac{2(1)^2}{0.025} = 80\ \text{m}$$

You could not measure this antenna on the bench range you used in Lesson 11,
and Lesson 9 explains why: it needs a compact range or a near-field scanner,
even though one person can carry the dish.
::::

::::{frame} The Parabolic Reflector
:::{present}
- A reflector amplifies nothing.
- It takes the spherical wave a small feed already radiates and **rearranges its phase**.
- A large flat area then leaves the antenna in step.
:::
:::{present}
<img src="../../viz/img/L14-parabola-geometry.svg"
     alt="Rays leaving the feed at the focus of a parabola reflect into a parallel beam, and every path from the focus to the aperture plane has the same length"
     style="max-width: 560px; width: 100%; display: block; margin: 0 auto;">
:::

The parabola is the surface that does this exactly, and Lesson 9's compact
range is the same geometry used indoors — there the collimated wave is aimed
across a chamber instead of at a satellite.
::::

::::{frame} The Equal-Path Property
:::{present}
- A parabola: every point $P$ is as far from the focus as from a line $f$ behind the vertex.

$$\begin{aligned}
\overline{FP} + \overline{PA} &= (f + z_P) + (z_a - z_P) \\
&= f + z_a
\end{aligned}$$

- No $z_P$ left: **every ray arrives in phase.**
:::
:::{present}
<img src="../../viz/img/L14-equal-path.svg"
     alt="A parabola with its focus F, a line a focal length behind its vertex, and the aperture plane in front. For two surface points P, the feed-to-surface leg equals the dashed run from P back to the line, so each ray's whole path equals the straight distance from the line to the aperture plane, the same for every ray"
     style="max-width: 520px; width: 100%; display: block; margin: 0 auto;">
:::

Put the vertex at the origin with the axis along $z$, so the surface is
$z = \rho^{2}/4f$ and the focus sits at $z = f$. The distance from the focus
to a point $P$ on the surface, at radius $\rho_P$ and height $z_P$, follows
from Pythagoras and the surface equation $\rho_P^2 = 4fz_P$:

$$\begin{aligned}
\overline{FP}^{2} &= \rho_P^{2} + (z_P - f)^{2} \\
&= 4fz_P + z_P^{2} - 2fz_P + f^{2} \\
&= (z_P + f)^{2}
\end{aligned}$$

so $\overline{FP} = f + z_P$. That is the parabola's defining property: every
point on it is as far from the focus as from the line $z = -f$ behind the
vertex. A ray from the focus to $P$ then travels parallel to the axis to an
aperture plane at $z = z_a$, covering a further $z_a - z_P$. The figure says
the same thing without algebra: replace the leg $\overline{FP}$ with its equal,
the dashed run from $P$ back to the line, and every ray's path becomes the
straight distance from that line to the aperture plane. That distance does not
depend on which ray you follow, so every point of the aperture plane is in
phase.
::::

::::{frame} f/D and the Feed
:::{present}
| $f/D$ | Edge half-angle | Character |
| :-- | :-- | :-- |
| 0.25 | $90^\circ$ | focus in the plane of the rim |
| 0.35 | $71^\circ$ | deep, needs a broad feed |
| 0.50 | $53^\circ$ | the common compromise |
| 0.60 | $45^\circ$ | shallow, feed on a long strut |
:::

The half-angle to the rim follows from the equal-path property. Measure a
ray from the focus by its length $r$ and its angle $\theta'$ from the axis,
pointing back toward the vertex. The point it reaches sits at height
$z_P = f - r\cos\theta'$, and $\overline{FP} = f + z_P$ becomes

$$\begin{aligned}
r &= 2f - r\cos\theta' \\
r &= \frac{2f}{1 + \cos\theta'}
\end{aligned}$$

The point's distance from the axis is then

$$\begin{aligned}
\rho &= r\sin\theta' \\
&= \frac{2f\sin\theta'}{1 + \cos\theta'} \\
&= 2f\tan\frac{\theta'}{2}
\end{aligned}$$

and the rim is where $\rho = D/2$:

$$\tan\frac{\theta_0}{2} = \frac{D}{4f} = \frac{1}{4(f/D)}$$

The same $r(\theta')$ says the rim is farther from the feed than the vertex
is, by the factor $2/(1 + \cos\theta_0)$, so the rim is dimmer than the
center even before the feed's own pattern rolls off. For $f/D = 0.5$ that
spreading alone puts the rim 1.9 dB below the center.

:::{depth}
A deep dish (small $f/D$) shields the feed from ground noise but demands a
feed with an almost hemispherical pattern. A shallow dish is easy to
illuminate cleanly but puts the feed far out on a wobbly strut. Most
prime-focus reflectors land between 0.3 and 0.6.
:::
::::

::::{frame} Aperture Efficiency Losses
:::{present}
- $\eta_{\text{ap}} \approx 0.55$ to $0.7$ for a good reflector.
- The missing 30 to 45% comes from spillover, taper, blockage, and surface error.
- Each one is a design tradeoff, not a manufacturing defect.
:::

The first trade is the feed's own pattern. Aim a narrow feed at the dish and
the rim sits 20 dB down: the outer part of the dish contributes little, and
the effective area shrinks. Widen the feed and the rim brightens — but now
power passes the rim entirely and is lost. On receive, spillover also adds
noise. Lesson 12's antenna temperature $T_A$ is the temperature of whatever
the pattern sees, weighted by the pattern. The main beam of an earth-station
dish sees sky at a few kelvin to a few tens of kelvin, but the spilled part of
the feed pattern looks past the rim at ground near $290\ \text{K}$, and it
raises $T_A$ and with it the noise $kT_AB$ the antenna delivers.
::::

::::{frame} The 10 dB Rule
:::{present}
<img src="../../viz/img/L14-illumination-taper.svg"
     alt="Three feed illuminations of the same dish: too narrow with a starved rim, about right with a ten decibel edge taper, and too wide with power spilling past the rim"
     style="max-width: 600px; width: 100%; display: block; margin: 0 auto;">
:::
:::{present}
$$G = \eta_\text{s}\ \eta_\text{t}\ \eta_\text{rest}\ \frac{4\pi A}{\lambda^2}$$

- Narrow feed: dark rim, area wasted, $\eta_\text{t}$ falls.
- Wide feed: power misses the dish, $\eta_\text{s}$ falls.
- **The gain peaks with the rim about 10 dB below the center.**
:::

Spillover and taper are two of the factors inside $\eta_{\text{ap}}$, and
nothing else in the gain formula depends on the feed, so their product *is*
the gain, up to a constant: the edge taper that maximizes
$\eta_\text{s}\eta_\text{t}$ is the edge taper that maximizes the dish's gain.

It is the house rule of thumb for reflector feeds, and it is why a dish's
aperture distribution always looks like one of the tapers from Lesson 6, with
lower sidelobes as a side effect. A uniform circular aperture
has its first sidelobe at $-17.6$ dB; a feed that follows the rule pushes it
to about $-25$ dB.

We can compute the optimum. Model the feed's power pattern as
$\cos^n\theta'$ and sweep $n$. Two efficiencies pull against each other. The
**spillover efficiency** is the fraction of the feed's power that lands on
the dish at all,

$$\eta_\text{s} = \frac{\int_0^{\theta_0}\cos^n\theta'\ \sin\theta'\ d\theta'}{\int_0^{\pi/2}\cos^n\theta'\ \sin\theta'\ d\theta'}$$

and the **taper efficiency** $\eta_\text{t}$ is the ratio from the frame on
the one idea,
$\left\vert\int E_a\ dS'\right\vert^2/\left(A\int\vert E_a\vert^2\ dS'\right)$,
with the aperture field set by the feed pattern and the $r(\theta')$
spreading from the frame on $f/D$:

$$E_a \propto \sqrt{\cos^n\theta'}\ \frac{1 + \cos\theta'}{2}$$

A broad feed (small $n$) gives a nearly uniform aperture and $\eta_\text{t}$
near 1, but spills. A narrow feed (large $n$) puts everything on the dish but
leaves the rim dark. For $f/D = 0.5$ the product peaks at an edge taper of
$10.7\ \text{dB}$, where $\eta_\text{s} = 0.92$, $\eta_\text{t} = 0.89$, and
$\eta_\text{s}\eta_\text{t} = 0.82$.

<img src="../../viz/img/L14-taper-spillover.svg"
     alt="Spillover efficiency rises and taper efficiency falls as the rim gets darker; their product peaks at about 0.82 for an edge taper near 11 dB, for a dish with f over D of 0.5"
     style="max-width: 640px; width: 100%; display: block; margin: 1em auto;">

The peak is broad: anything from about 8 to 14 dB is within 0.03 of the best
efficiency, which is why a rule of thumb is good enough.
::::

::::{frame} Dish and Feed
:class: viz-frame

:::{present}
<iframe src="../../viz/feed-dish.html"
        width="100%" height="425"
        style="border: 1px solid #cddce9; border-radius: 6px;"
        loading="lazy"
        title="Dish and feed: the rim angle, edge taper, spillover, and taper efficiency as the dish depth and the feed pattern change">
</iframe>

<p class="viz-note mathjax_process">Feed pattern \(\cos^n\theta'\): <strong>larger \(n\), narrower feed</strong>, darker rim, less spillover.</p>
:::

:::{depth}
The widget uses the same model as the 10 dB rule: a feed with power pattern
$\cos^n\theta'$ at the focus of a dish with the chosen $f/D$. The exponent
$n$ is just a dial on the feed's beamwidth. At $n = 0$ the feed radiates
equally into its whole forward hemisphere; at $n = 4$ it is $112^\circ$ wide
at its $-10$ dB points, which the control reports beside the value; at
$n = 20$ it is a narrow pencil.
The left panel draws the dish to scale with the feed's pattern at the focus,
shading the part that misses the rim; the right panel plots spillover, taper,
and their product against edge taper for that $f/D$. Start at the default,
$f/D = 0.5$ and $n = 4$: the rim sits at $53^\circ$, the edge is 10.8 dB
down, and the product is 0.82. Narrow the feed and spillover falls while the
taper efficiency falls with it; widen it and the reverse. Then change $f/D$
and press the best-$n$ button: from $f/D = 0.4$ up, the best product stays near 0.82 at
about an 11 dB edge taper, which is why the rule does not depend on the dish.
Below about $f/D = 0.35$ the model's best product climbs higher, because its
feed radiates nothing behind itself and a very broad feed then wastes almost
nothing. Real feeds that broad do not exist, which is one reason deep dishes
are uncommon.
:::
::::

::::{frame} Blockage and the Offset Feed
:::{present}
$$\begin{aligned}
\frac{G}{G_0} &= \left(\frac{A - A_b}{A}\right)^2 \\
&= \left[1-\left(\frac{d}{D}\right)^2\right]^2
\end{aligned}$$

- The feed shadows $A_b$. The boresight field sums the rest; gain is its square.
- An **offset feed** moves it out of the beam.
:::
:::{present}
<img src="../../viz/img/L14-offset-feed.svg"
     alt="Left: a prime-focus dish, where the feed at the focus sits in the outgoing beam and casts a shadow. Right: an offset reflector, a slice cut from one side of a larger parent paraboloid, so the feed sits outside the beam"
     style="max-width: 560px; width: 100%; display: block; margin: 0 auto;">
:::

On a 3 m dish a 15 cm feed is negligible. On a 45 cm consumer dish it is
not, which is why the dish on the roof looks oval and has its arm hanging off
the bottom: the reflector is a slice cut off-axis from a much larger imaginary
paraboloid, giving zero blockage and cleaner sidelobes, and the tilted slice is
what makes the panel look taller than it is wide.

The blockage factor is the aperture-efficiency ratio again. The feed still
radiates the power aimed at the blocked disk of area $A_b$, so the denominator
keeps all of $A$, but the blocked disk scatters that power instead of adding
it in phase on boresight, so the numerator loses the blocked area. For a uniform field,

$$\begin{aligned}
\frac{G}{G_0} &= \frac{(A - A_b)^2}{A^2} \\
&= \left[1 - \left(\frac{d}{D}\right)^2\right]^2
\end{aligned}$$

The square is the whole story: blocking a fraction $(d/D)^2$ of the area
costs that fraction of the boresight *field*, and gain goes as field squared,
while the power the feed pays for does not shrink at all. A $15\ \text{cm}$
feed loses $0.02\ \text{dB}$ on a $3\ \text{m}$ dish and $1.0\ \text{dB}$ on
a $45\ \text{cm}$ one.
::::

::::{frame} Surface Accuracy — Ruze's Formula
:::{present}
$$\begin{aligned}
G &= G_0\ e^{-(4\pi\sigma/\lambda)^{2}} \\
\text{loss (dB)} &= 685.8\left(\frac{\sigma}{\lambda}\right)^{2}
\end{aligned}$$

- $\lambda/50$ RMS loses 0.27 dB, which is negligible.
- $\lambda/16$ RMS loses 2.7 dB, which disqualifies the surface.
:::
:::{present}
<img src="../../viz/img/L14-ruze.svg"
     alt="Left: a bump in the reflector surface lengthens a ray's path by twice the bump depth, in and back out. Right: gain loss grows with the square of the RMS surface error, 0.27 dB at a fiftieth of a wavelength and 2.68 dB at a sixteenth"
     style="max-width: 560px; width: 100%; display: block; margin: 0 auto;">
:::

Phase errors from a bumpy surface reduce the gain exponentially. A bump of height $\epsilon$ on a shallow dish lengthens the path in and
back out by $2\epsilon$, a phase error $\delta = 2k\epsilon$, so an RMS surface
error $\sigma$ is an RMS phase error $\delta_\text{rms} = 4\pi\sigma/\lambda$.
In the aperture-efficiency ratio the magnitude of $E_a$ is unchanged, so the
denominator is too, but the numerator now sums $e^{j\delta}$ over the
aperture. For random, Gaussian-distributed errors that sum averages to
$e^{-\delta_\text{rms}^2/2}$, and squaring it gives

$$\begin{aligned}
\frac{G}{G_0} &= e^{-\delta_\text{rms}^{2}} \\
&= e^{-(4\pi\sigma/\lambda)^{2}}
\end{aligned}$$

In decibels the constant is $10\log_{10}(e)\ (4\pi)^2 = 685.8$. Note what it
means for a fixed piece of hardware: a dish held to 0.5 mm RMS is essentially perfect at 6 GHz and has
thrown away 1.7 dB by 30 GHz. Big dishes at short wavelengths are a machining
problem, not an electromagnetics problem.
::::

::::{frame} The Efficiency Budget
:::{present}
| Loss term | Typical | Why |
| :-- | :-- | :-- |
| Spillover | 0.90 | power past the rim |
| Taper | 0.85 | rim darker than center |
| Blockage | 0.95 | feed and struts |
| Surface | 0.94 | Ruze |
| Everything else | 0.97 | cross-pol, feed |
| **Product** | **0.66** | an ordinary reflector |
:::
:::{present}
<img src="../../viz/img/L14-efficiency-budget.svg"
     alt="The efficiency budget as a waterfall: spillover, taper, blockage, surface error, and the remaining losses take an ideal aperture from 1.00 to 0.66"
     style="max-width: 560px; width: 100%; display: block; margin: 0 auto;">
:::

In the figure, each blue bar is the efficiency left after that term and the
red cap on it is what the term took away; each bar starts where the one
before it ended, because the terms multiply. That product is where the
$\eta_{\text{ap}} \approx 0.65$ we have been assuming comes from. It is an accounting result, not a constant of
nature, and every row of it is a design decision someone made. The spillover
and taper rows sit a little below the 0.92 and 0.89 of the 10 dB rule's
optimum, because a real feed's pattern is not exactly $\cos^n\theta'$. The
cross-polarization in "everything else" is power the dish radiates in the
polarization orthogonal to the intended one, which Lesson 3 showed a matched
receiver cannot collect.
::::

::::{frame} The Yagi-Uda
:::{present}
<img src="../../viz/img/L14-yagi.svg"
     alt="Yagi-Uda antenna showing a slightly long reflector, the fed driven element, and a row of progressively shorter directors along a boom, with the main beam endfire"
     style="max-width: 600px; width: 100%; display: block; margin: 0 auto;">
:::
:::{present}
- Exactly one element is fed. The rest are **parasitic**: bare rods, no feed line.
- The driven element's field induces currents on them, and they re-radiate.
- Phased right, that re-radiation cancels behind and adds ahead: array gain from one cable.
:::

The driven element is a dipole near $0.47\lambda$. Every other element has no
feed line and no source — just a rod that the driven element's near field
induces a current on. That induced current re-radiates, and the total pattern
is the superposition of all of them. There is nothing new physically: this is
Lesson 6's radiation integral with several current filaments instead of one.

Why it matters is the cable. An array, at the end of this lesson, gets its gain
by feeding every element and setting each one's phase with electronics. A Yagi
gets most of that gain with one feed line and a row of rods, which is why it
is on every rooftop. The price is that nothing sets a parasite's phase
directly. The next two frames are about that: what phase the parasites need,
and how a rod with no feed line gets it.
::::

::::{frame} Two-Element Yagi
:class: viz-frame

:::{present}
<iframe src="../../viz/yagi-two-element.html"
        width="100%" height="451"
        style="border: 1px solid #cddce9; border-radius: 6px;"
        loading="lazy"
        title="Two-element Yagi: phasor sums toward the front and back, and the resulting pattern, as the reflector's spacing, phase, and amplitude change">
</iframe>

<p class="viz-note mathjax_process">Arrows: each element's field, added head to tail. A reflector \(0.2\lambda\) behind cancels the back when its current sits <strong>\(108^\circ\)</strong> off the driven one.</p>
:::

:::{depth}
A two-element Yagi is a driven dipole and one reflector a distance $d$ behind
it. How to read the widget: the left panel adds the two elements' fields in
two directions, drawn as arrows. The navy arrow is the driven element, always
length 1 and pointing right. The amber arrow is the reflector's contribution,
turned by the reflector's current phase $\alpha$ and by the extra trip $kd$
its wave makes (or saves). The green arrow is the sum, and its length is how
strong the antenna is in that direction: toward the front on the left, toward
the back on the right. The right panel is the whole pattern seen from above,
with the two elements as dots.

The arrows come from Lesson 6's radiation vector,
$N_z = \int I(z')\ e^{+jkz'\cos\theta}\ dz'$, with the integral now a sum over
two filaments: the driven element at $z = 0$ and the reflector a distance $d$
behind it, carrying $I_2 = aI_1e^{j\alpha}$. Straight ahead ($\theta = 0$) and
straight back ($\theta = \pi$),

$$\begin{aligned}
N_z(0) &\propto 1 + a\ e^{j(\alpha - kd)} \\
N_z(\pi) &\propto 1 + a\ e^{j(\alpha + kd)}
\end{aligned}$$

The back lobe cancels when $\alpha + kd = \pi$. For a typical spacing
$d = 0.2\lambda$, $kd = 72^\circ$, so the reflector's current must sit
$108^\circ$ from the driven element's. The forward sum is then
$\vert 1 + e^{j36^\circ}\vert = 1.90$ for $a = 1$, nearly the full 2.

Start the widget at the default, $d = 0.2\lambda$ and $\alpha = 108^\circ$:
the back sum closes to zero and the forward sum is 1.90. Then move $\alpha$
and watch the null leave the back and the front lobe shrink. Shorten the
spacing to $0.1\lambda$ and press *back null*: the canceling phase moves to
$144^\circ$, and the forward sum falls, because the two currents now nearly
oppose each other in every direction. Lower $a$ and the null fills in, which
is what a reflector cut too far from resonance does: its induced current is
too weak to cancel the driven element.
:::
::::

::::{frame} Parasitic Element Phasing
:::{present}
$$I = \frac{V}{Z} = \frac{V}{R + jX}$$

- No cable sets a parasite's phase. Its **length** does, through the sign of $X$.
- **Long**: $X > 0$, the current lags and nulls the back: a **reflector**.
- **Short**: $X < 0$, the current leads and pulls the beam toward it: a **director**.
:::

The lag and lead are Lesson 7's input impedance at work. A parasite is a
dipole with no feed, driven by the voltage $V$ the driven element's field
induces on it, so its current is $I = V/Z$ with $Z = R + jX$. Lesson 7 found
$X = +42.5\ \Omega$ at exactly $\lambda/2$, with resonance a little shorter.
Longer than resonance, $X > 0$ and the current lags $V$ by $\arctan(X/R)$;
shorter, $X < 0$ and it leads.

Why that matters is the previous frame: the reflector has to carry its
current $108^\circ$ from the driven element's, and a rod with no feed line has
only one way to be told. Most of that phase comes from the coupling, since a
parasite's induced current re-radiates roughly in opposition to the field that
drove it, delayed by the trip across the gap. The detuning trims the rest.
The reflector runs about $0.5\lambda$, and its added lag is what tips the
balance toward canceling behind. The directors run around $0.40$ to
$0.45\lambda$, and their detuning sets the phase lag from one director to the
next at slightly more than the free-space $kd$. That is a **slow traveling
wave**: a wave along the boom whose phase velocity is slightly less than the
speed of light, which is what narrows an endfire beam below what elements
phased at exactly light speed would give.

:::{depth}
This course does not use mutual-impedance matrices. To find the currents on
the parasites exactly, we would solve a coupled system with one row per
element — that is what NEC did in Lesson 8. Here, the phenomenology is
the point: long lags, short leads, and the beam goes toward the short end.
:::
::::

::::{frame} Yagi Gain and Boom Length
:::{present}
<img src="../../viz/img/L14-yagi-boom.svg"
     alt="Yagi gain against boom length on a doubling scale: typical designs climb about 1.8 dB each time the boom doubles, against two ideal endfire lines, one phased at light speed and one phased for best gain, which both climb 3 dB per doubling"
     style="max-width: 560px; width: 100%; display: block; margin: 0 auto;">
:::
:::{present}
- Each time the boom **doubles**, the gain climbs about **2 dB**.
- An ideal endfire line would climb 3 dB: its gain is proportional to its length.
- The boom length, not the element count, sets the gain.
:::

The plotted points are typical published designs:

| Elements | Boom | Gain |
| :-- | :-- | :-- |
| 3 | $0.3\lambda$ | 7.5 dBi |
| 6 | $1.0\lambda$ | 10 dBi |
| 10 | $2.2\lambda$ | 12.5 dBi |
| 16 | $4.5\lambda$ | 14.5 dBi |

The result is an **endfire** beam, main lobe along the boom (the line of the
elements) and away from the reflector, rather than broadside to it. Its
front-to-back ratio, Lesson 2's main-lobe peak over the lobe directly behind,
is 15 to 25 dB.

Why the boom sets the gain is Lesson 6's line source turned on its end. Put
a current $I(z') = I_0e^{-jkz'}$ along a boom of length $L$, phased to
travel forward at the speed of light. The radiation vector is the sinc of
Lesson 6 with its argument shifted,

$$\begin{aligned}
N_z(\theta) &= \int_{-L/2}^{L/2} I_0\ e^{+jkz'(\cos\theta - 1)}\ dz' \\
&\propto \frac{\sin u}{u} \\
u &= \frac{kL}{2}\ (\cos\theta - 1) \approx -\frac{\pi L}{2\lambda}\ \theta^{2}
\end{aligned}$$

so the beam peaks at $\theta = 0$, along the boom. The half-power point
$\vert u\vert = 1.39$ now falls at $\theta^2 \propto \lambda/L$, not
$\theta \propto \lambda/L$ as it did broadside, and the beam is a cone, that
narrow in every plane. Its solid angle goes as $\theta^2 \propto \lambda/L$,
so the directivity is proportional to $L$: the exact result is
$D \approx 4L/\lambda$, and a slow wave pushes it toward $7L/\lambda$. That
is $+3$ dB per doubling of the boom, whatever the number of elements on it.
Those are the figure's two ideal lines: the lower one is a current phased to
travel at exactly light speed ($4L/\lambda$), the upper one the slightly slow
wave of the previous frames ($7L/\lambda$). The horizontal axis doubles at
every step, so a straight line on it means a fixed number of dB per doubling.

Real Yagis fall short of that slope. The table climbs about $1.8$ dB per
doubling: a short Yagi beats the line-source estimate ($7L/\lambda$ gives
8.5 dBi at $1\lambda$ against the table's 10) because its elements are
dipoles with gain of their own, and a long one falls behind it (15.0 dBi at
$4.5\lambda$ against 14.5) because the current dies away on the far
directors. A Yagi needs only one reflector, because the first already sees
very little field behind it. Adding more directors to the same boom adds
almost nothing. Practical single Yagis range from 8 to 15 dBi; beyond that,
designers stack several and let the stack act as an array.
::::

::::{frame} Yagi Bandwidth
:::{present}
- Everything on a Yagi is a **detuned resonator**.
- Moving a few percent off the design frequency shifts the phases and degrades the pattern.
:::

That is fine for a fixed-channel TV, amateur, or point-to-point link, which is
where Yagis appear, and a poor fit for anything wideband. It is also the
easiest prediction in this lesson to check on the analyzer from Lesson 10.
::::

::::{frame} Arrays
:::{present}
$$G_\text{array} = 10\log_{10} N \quad \text{dB}$$

- Build the aperture from $N$ small antennas, fed coherently.
- Sixteen patches add 12 dB; sixty-four add 18 dB.
- Change each element's phase and the beam moves, in microseconds.
:::
:::{present}
<img src="../../viz/img/L13-patch-array.svg"
     alt="Left: one patch and its broad beam, about 6 dBi and fixed at broadside. Right: eight patches in a row on one board, half a wavelength apart, each behind its own phase shifter, forming a narrow beam steered 20 degrees off broadside"
     style="max-width: 560px; width: 100%; display: block; margin: 0 auto;">
:::

That capability is worth a module of its own, and it gets one. Module 3
develops the array factor, pattern multiplication, beam steering, grating
lobes, and tapering, and you will steer a real beam on the ADALM-PHASER
hardware. For today, file the array alongside the reflector and the Yagi as
the third approach to the same goal: coherent area.

The $10\log_{10}N$ is the radiation vector once more. Fed in phase, $N$
identical elements sum to $N$ times one element's radiation vector on
boresight, as Lesson 12's element-and-image pair summed two:

$$\begin{aligned}
\mathbf{N}_\text{array}(0) &= N\ \mathbf{N}_\text{el}(0) \\
U_{\max,\text{array}} &= N^2\ U_{\max,\text{el}} \\
P_{\text{rad,array}} &= N\ P_{\text{rad,el}} \\
D_\text{array} &= \frac{4\pi\ N^2\ U_{\max,\text{el}}}{N\ P_{\text{rad,el}}} \\
&= N\ D_\text{el}
\end{aligned}$$

The third line holds only under a condition. Total radiated power adds element by element
only when the elements are far enough apart, about $\lambda/2$, that they do
not share aperture; crowd them closer and their mutual coupling changes each
one's radiated power. So the gain grows with $N$ only if the aperture grows
with it, which is the one idea again: a $\lambda/2$ grid of $N$ elements has
area $N\lambda^2/4$, and $4\pi(N\lambda^2/4)/\lambda^2 = N\pi$.
::::

::::{frame} Choosing: Five Questions
:::{present}
1. How much gain does the link budget require? Run it first.
2. What frequency?
3. How much bandwidth?
4. Does it have to move or steer?
5. What are the cost, size, weight, and wind load?
:::

In that order, those five settle almost every real selection. Excess gain
adds cost and tightens the pointing requirement. Aperture antennas get small and cheap
as $\lambda$ shrinks while wire antennas get fragile. Reflectors and horns are
broadband; Yagis and patch arrays are not. A dish steers mechanically and
slowly, an array electronically and instantly, a Yagi mostly not at all. And a
20 dBi antenna that cannot survive local wind and ice loading is not a usable
answer.
::::

::::{frame} Three Approaches Compared
:::{present}
| | Reflector | Yagi | Array |
| :-- | :-- | :-- | :-- |
| Gain | 25–60 dBi | 8–15 dBi | 15–40 dBi |
| Bandwidth | wide | a few % | moderate |
| Steering | mechanical | fixed | electronic |
| Profile | bulky | long boom | flat panel |
| Cost driver | surface | almost none | one chain per element |
:::
::::

::::{frame} Worked Selection — 20 dBi at 2.4 GHz
:class: read-only

You need a 20 dBi ground-station antenna at 2.4 GHz for a cubesat downlink.
$\lambda = 0.125\ \text{m}$, and $G = 20\ \text{dBi} = 100$.

**Required effective aperture.**
$A_e = G\lambda^{2}/4\pi = 100(0.015625)/12.57 = 0.124\ \text{m}^{2}$. Every
candidate has to deliver that much coherent area.

**Dish.** With $\eta_{\text{ap}} = 0.6$, $A = 0.124/0.6 = 0.207\ \text{m}^{2}$,
so $D = 2\sqrt{A/\pi} = 0.51\ \text{m}$. Beamwidth
$\theta_\text{HP} \approx 70^\circ(0.125/0.51) = 17^\circ$. A half-meter dish
with a 17-degree beam is forgiving to point, cheap, and broadband, and no
other candidate here matches it on all three.

**Yagi.** A single Yagi tops out near 14.5 dBi at a $4.5\lambda$ (0.56 m)
boom, so 20 dBi needs four stacked in a 2x2 bay:
$14.5 + 10\log_{10}4 = 20.5\ \text{dBi}$. It works, but it is four booms, a phasing
harness, and a narrow band.

**Patch array.** At $\lambda/2 = 6.25\ \text{cm}$ spacing with
$\eta_{\text{ap}} = 0.75$, a $7\times7$ grid spans $0.44\ \text{m}$ square,
$A = 0.191\ \text{m}^{2}$, giving
$G = 0.75(4\pi)(0.191)/0.015625 = 115 = 20.6\ \text{dBi}$. The panel is flat,
presents low wind load, and a later design can steer it electronically, but
it needs a 49-way feed network.

**Decision.** For a fixed ground station on a rotator, take the 0.51 m dish:
fewest parts, widest band, lowest cost. Choose the patch array instead the
moment you need a flat profile or electronic steering.
::::

::::{frame} Does the Link Close?
:::{present}
$$\begin{aligned}
L_\text{fs} &= 20\log_{10}\!\left(\frac{4\pi R}{\lambda}\right) \\
&= 160.0\ \text{dB} \\
P_r &= 33.0 + 0 + 20 - 160.0 \\
&= -107.0\ \text{dBm}
\end{aligned}$$

- Against a $-121\ \text{dBm}$ noise floor, that is **14 dB of margin**.
:::
:::{present}
<img src="../../viz/img/L14-link-budget.svg"
     alt="Level diagram of the cubesat downlink: 33.0 dBm leaves the transmitter, 160.0 dB of free-space path loss takes it to minus 127.0 dBm, and the 20 dBi dish raises it to minus 107.0 dBm, 14 dB above the minus 121 dBm noise floor; without the dish the signal sits 6 dB under the noise"
     style="max-width: 560px; width: 100%; display: block; margin: 0 auto;">
:::

Cubesat at 1000 km, 2 W transmitter (33.0 dBm) into a 0 dBi antenna, and
our 20 dBi dish on the ground, at $\lambda = 0.125\ \text{m}$. The path loss
is Lesson 2's Friis factor $(\lambda/4\pi R)^2$ in decibels, with
$4\pi R/\lambda = 4\pi(10^6)/0.125 = 1.005\times10^{8}$.

The noise floor is Lesson 12's $kT_AB$ with the reference temperature
$T_0 = 290\ \text{K}$, which gives $kT_0 = -174\ \text{dBm/Hz}$, plus the
receiver's noise figure:

$$\begin{aligned}
N &= kT_0 + 10\log_{10}B + \text{NF} \\
&= -174 + 10\log_{10}(10^{5}) + 3 \\
&= -121\ \text{dBm}
\end{aligned}$$

in a 100 kHz channel with a 3 dB noise figure. A dish pointed at cold sky
sees a $T_A$ well below 290 K, so this floor is conservative. The link
closes, and it closes *because* of the 20 dB the dish contributed. Swap the
dish for a 0 dBi antenna and $P_r = -127.0\ \text{dBm}$, 6 dB under the
noise.
::::

::::{frame} Summary
:class: read-only

| Idea | What it says | Number to hold onto |
| :-- | :-- | :-- |
| $G = \eta_{\text{ap}}4\pi A/\lambda^{2}$ | gain is coherent area in square wavelengths | $\eta_{\text{ap}} \approx 0.55$–$0.7$ for reflectors |
| $G = \eta_{\text{ap}}(\pi D/\lambda)^{2}$ | circular-dish shortcut | +6 dB per doubling of $D$ |
| $\theta_\text{HP} \approx 70^\circ\lambda/D$ | beamwidth is set by size in wavelengths | 1 m at 12 GHz $\rightarrow 1.75^\circ$ |
| $A_e = \eta_{\text{ap}}A = G\lambda^{2}/4\pi$ | effective aperture — what Friis uses | 1 m dish at 12 GHz $\rightarrow 0.51\ \text{m}^2$ |
| $f/D$ | sets the edge angle the feed must cover | 0.3–0.6 typical; 0.5 $\rightarrow 53^\circ$ |
| Edge taper | spillover fights illumination taper | rim about $-10$ dB |
| Ruze, $685.8(\sigma/\lambda)^{2}$ dB | surface error reduces gain exponentially | $\lambda/50 \rightarrow 0.27$ dB; $\lambda/16 \rightarrow 2.7$ dB |
| Yagi boom length | boom length, not element count, sets gain | $\approx +2$ dB per doubling (3 ideal); 8–15 dBi |
| $10\log_{10}N$ | array gain over one element | 64 elements $\rightarrow$ 18 dB |
::::

::::{frame} Practice
:class: read-only doc-links

- <a class="doc-link" href="../../practice/ECE444_L14_Practice_blank.pdf" target="_blank" rel="noopener">Problem set (PDF)</a>
- <a class="doc-link doc-key" href="../../practice/ECE444_L14_Practice_SOLUTIONS.pdf" target="_blank" rel="noopener">Solutions (PDF)</a>
::::

::::{frame} Where This Is Going
:::{present}
- **L15:** illumination sets the sidelobes. Today's taper bought $-25$ dB for a 14% wider beam.
- **L16:** an array samples that aperture, one element at a time.
- **L19:** change each element's phase and the beam moves. You steer one.
:::
:::{present}
<img src="../../viz/img/L14-beam-patterns.svg"
     alt="Patterns of a uniform circular aperture and of the 10 dB-rule feed's aperture against angle times D over wavelength: the taper widens the beam from 59 to 67 degrees and lowers the first sidelobe from minus 17.6 to minus 25.1 dB"
     style="max-width: 560px; width: 100%; display: block; margin: 0 auto;">
:::

Today the illumination was a side effect: the feed's pattern set it, and the
10 dB rule picked it for efficiency. The figure is what it did to the beam
on the way, a first sidelobe pushed from $-17.6$ to $-25$ dB at the price of
widening the beam from $59^\circ$ to $67^\circ\lambda/D$. Lesson 15 turns that
around and asks which illumination to choose when the sidelobes are the
requirement, and what each choice costs in beamwidth and efficiency.

Lesson 16 builds the third approach from today. Sample that same aperture at
discrete points, put an element at each, and the pattern becomes the array
factor; the illumination becomes a set of element weights you can set
yourself. By Lesson 19 those weights carry phase as well as amplitude, and the
beam moves with nothing mechanical moving: you will steer the eight-element
ADALM-PHASER across the bench and measure what it costs at each angle.
::::
