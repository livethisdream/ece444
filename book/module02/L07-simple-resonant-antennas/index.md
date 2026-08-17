# L7 - Simple Resonant Antennas

:::{admonition} Slides
:class: slides
<a href="../../slides/L07-simple-resonant-antennas.html" target="_blank" rel="noopener">html slides</a>
<a href="../../slides/L07-simple-resonant-antennas.html?print-pdf" target="_blank" rel="noopener">pdf slides</a>
<a href="../../slides/L07-simple-resonant-antennas.md" target="_blank" rel="noopener">raw markdown slides</a>
:::

## Learning Objectives

<ol class="lo-list lo-sublist" style="--module: '2'; --lo: '1'">
  <li>I can explain why the isotropic radiator cannot exist yet anchors every gain specification, and use it as the 0 dBi reference.</li>
  <li>I can obtain the half-wave dipole's pattern, beamwidth, and directivity from its sinusoidal current, and explain how the pattern changes as the dipole gets longer.</li>
  <li>I can state the half-wave dipole's input impedance, explain physically why a resonant wire is slightly shorter than half a wavelength, and compute the VSWR when it is fed by a 50 or 75 ohm line.</li>
  <li>I can calculate the physical dimensions of a resonant dipole at a given frequency and predict its gain and impedance well enough to sanity-check a simulation.</li>
</ol>

Lesson 6 built the machine: assume a current on a structure, push it through the
radiation integral, and out comes the far-field pattern. Today you spend that
answer on hardware. Two antennas carry the lesson — the **isotropic radiator**,
which cannot be built but which every gain number on every datasheet secretly
refers to, and the **half-wave dipole**, which you can cut with a tape measure
and which will be sitting in the simulator next lesson. By the end you will be
able to name a frequency, cut a wire to length, and predict its pattern, its
gain, and what a network analyzer will read at its terminals.

## Part 1: The antenna that cannot exist

An **isotropic radiator** radiates equally in every direction. Wrap a sphere
around it and every square meter of that sphere receives the same power
density. Its radiation intensity is simply the radiated power spread over the
whole sphere,

$$U_\text{iso} = \frac{P_\text{rad}}{4\pi},$$

so its directivity is exactly $D = 1$, which is $0\ \text{dBi}$ — the "i" is
literally there to say *relative to isotropic*.

It cannot exist. The argument is short. In the far field the electric field is
transverse: it lies tangent to the sphere of constant $r$. A truly isotropic
radiator would need that tangential field to be nonzero everywhere on the
sphere with no direction singled out, and topology forbids it — you cannot comb
a hairy ball flat. Somewhere the field has to vanish, and a place where the
field vanishes is a **null**.

:::{admonition} Key Point
:class: key-concept
Every real antenna has at least one null. That is not a manufacturing defect,
it is a requirement of the geometry of a sphere. The isotropic radiator has no
nulls, so it is not an antenna — it is a unit of measurement.
:::

And as a unit of measurement it earns its keep. Directivity, gain, and
effective aperture are all defined as ratios against isotropic, which is why a
horn is "16 dBi" rather than "16 dB compared to some other horn we happen to
own". Two related conventions come out of the same reference:

| Quantity | Definition | Reference |
| :-- | :-- | :-- |
| dBi | gain over an isotropic radiator | the fiction |
| dBd | gain over a half-wave dipole | a real antenna |
| EIRP | $P_t G_t$ — the power an isotropic radiator would need to match your antenna's peak | the fiction |

Because a half-wave dipole is $2.15\ \text{dBi}$ (we get there in Part 3), the
two decibel scales differ by a constant:

$$\text{dBi} = \text{dBd} + 2.15$$

**EIRP** is the payoff. Feeding $5\ \text{W}$ into a half-wave dipole produces
the same peak power density as feeding $5 \times 1.64 = 8.2\ \text{W}$ into an
isotropic radiator, so the EIRP is $8.2\ \text{W}$, or $39.1\ \text{dBm}$. One
number now describes the transmitter and the antenna together, which is exactly
what a link budget needs and exactly what a spectrum regulator writes into a
license.

```{note}
Watch the units in the wild. "ERP" usually means effective radiated power
referred to a *dipole*, so ERP and EIRP differ by that same 2.15 dB. Getting
this backwards is a classic way to be 4.3 dB wrong.
```

## Part 2: From a short wire to a half-wave dipole

Lesson 6 handled the **infinitesimal dipole** — a current element so short that
the current is essentially constant along it. Its pattern is
$\vert F(\theta)\vert = \sin\theta$, a doughnut with its maximum broadside at
$\theta = 90^\circ$ and nulls off the wire ends. Its beamwidth is $90^\circ$
and its directivity is $D = 1.5$, or $1.76\ \text{dBi}$. Its radiation
resistance, however, is $R_r = 80\pi^2 (L/\lambda)^2$ — about $2\ \Omega$ for a
wire a tenth of a wavelength long. $2\ \Omega$ against a $50\ \Omega$ line is a
hopeless match, and that, not the pattern, is why nobody feeds a short dipole
directly.

Make the wire longer and the current can no longer be treated as constant. So
before we can use Lesson 6's machinery, we need a current to feed it.

### Where the standing wave comes from

Start with a two-wire transmission line, open-circuited at the far end. You
already know its current: on an open-circuited line the current must be **zero
at the open end**, and the standing wave grows sinusoidally as you walk back
from it. Measuring a distance $s$ back from the open end,

$$I(s) = I_m \sin(ks).$$

Now take the last stretch of that line and **fold the two conductors apart**
until they lie in a straight line, one arm up and one arm down. You have built
a center-fed dipole, and the standing wave came with it.

Each arm still ends in an open tip. A point at height $z$ on the upper arm sits
a distance $s = L/2 - z$ back from its tip, so $I(z) = I_m \sin[k(L/2 - z)]$.
The lower arm is the mirror image, so replacing $z$ by $\vert z \vert$ covers
both:

$$I(z) = I_m \sin\left[k\left(\frac{L}{2} - \vert z \vert\right)\right]$$

Check it against the boundary conditions, which is the only reason we believe
it:

- At the tips, $z = \pm L/2$, the sine argument is zero, so $I = 0$. **Current
  vanishes at both open ends** — charge has nowhere further to go.
- At the feed, $I(0) = I_m \sin(kL/2)$. For $L = \lambda/2$ that is
  $I_m \sin(\pi/2) = I_m$: the current *maximum* lands exactly at the feed. For
  $L = \lambda$ it is $I_m \sin(\pi) = 0$: a current *null* at the feed. Hold on
  to that contrast — it decides everything about impedance in Part 4.

:::{admonition} Key Point
:class: key-concept
This current is **assumed**, not solved for. It is justified by the
transmission-line analogy, and it is confirmed to be very close to the truth by
measurement and by numerical solvers — but it is not a solution of Maxwell's
equations for a dipole, and for thick or non-resonant wires it is visibly
wrong. Everything downstream in this lesson inherits that assumption. Lesson 8
is where you find out how much it costs.
:::

<img src="../../viz/img/L07-dipole-currents.svg"
     alt="Standing-wave current on center-fed wires of four different lengths"
     style="max-width: 700px; width: 100%; display: block; margin: 1em auto;">

## Part 3: Pattern, beamwidth, and directivity

You have a current. Lesson 6 gives you the rest, and this is the one antenna in
the course where we run that machine end to end.

### Using the radiation integral

Lesson 6's radiation vector is
$\mathbf{N} = \int \mathbf{J}\ e^{+jk\hat{\mathbf r}\cdot\mathbf{r}'}\ dV'$.
For a thin wire lying on $z$, the volume integral collapses to a line integral,
the current is $z$-directed, and $\hat{\mathbf r}\cdot\mathbf{r}' = z'\cos\theta$:

$$N_z(\theta) = \int_{-L/2}^{L/2} I(z')\ e^{+jkz'\cos\theta}\ dz'$$

The current is an **even** function of $z'$. Pair each $z'$ with $-z'$ and the
two exponentials combine into a cosine, which folds the integral onto the upper
arm and throws away the imaginary part:

$$N_z(\theta) = 2 I_m \int_0^{L/2} \sin\left[k\left(\frac{L}{2} - z'\right)\right]\cos(kz'\cos\theta)\ dz'$$

Now it is a first-year integral. The product-to-sum identity
$\sin A \cos B = \tfrac{1}{2}\left[\sin(A+B) + \sin(A-B)\right]$ turns the
integrand into two plain sines, both of which integrate on sight. Collecting
the result:

$$N_z(\theta) = \frac{2 I_m}{k}\ \frac{\cos\left(\dfrac{kL}{2}\cos\theta\right) - \cos\dfrac{kL}{2}}{\sin^2\theta}$$

One step left. Lesson 6 showed that a $z$-directed current radiates only a
$\theta$ component in the far field, obtained by projection:
$N_\theta = -N_z \sin\theta$. That kills one power of $\sin\theta$:

$$N_\theta(\theta) \propto \frac{\cos\left(\dfrac{kL}{2}\cos\theta\right) - \cos\dfrac{kL}{2}}{\sin\theta}$$

That is the pattern of a center-fed dipole of **any** length, up to a constant:

$$\vert F(\theta) \vert \propto \left\vert \frac{\cos\left(\dfrac{kL}{2}\cos\theta\right) - \cos\dfrac{kL}{2}}{\sin\theta} \right\vert$$

Both the proportionality and the magnitude bars are load-bearing. The bars
matter because for wires longer than $\lambda$ the bracket changes sign — that
sign flip is how sidelobes end up radiating out of phase with the main lobe.
The proportionality matters because **normalizing means dividing by the peak of
that expression**, and the peak is not always 1. For $L \le \lambda$ it sits at
broadside, $\theta = 90^\circ$, where the expression evaluates to
$1 - \cos\dfrac{kL}{2}$; for longer wires the peak walks off broadside
entirely, which is the story at the end of this lesson.

Set $L = \lambda/2$, so that $kL/2 = \pi/2$ and the second cosine vanishes. The
broadside peak is then $1 - 0 = 1$, so this one is already normalized and can
be written with an equals sign:

$$\vert F(\theta) \vert = \frac{\cos\left(\dfrac{\pi}{2}\cos\theta\right)}{\sin\theta}$$

That is the **half-wave dipole** pattern. The $\sin\theta$ in the denominator
looks like trouble at $\theta = 0$, but the numerator vanishes there too and
the ratio goes quietly to zero. The nulls are still straight off the wire ends.

```{note}
Notice what you actually bought. That general formula is not a half-wave
result — it holds for *any* $L$, and the multi-lobe patterns you will meet at
the end of this lesson come from the same expression with a different number in
it. One integral, every length. That is what the radiation integral is for.
```

The half-wave pattern is a doughnut again, only slightly slimmer than the short
dipole's.

<img src="../../viz/img/L07-halfwave-pattern.svg"
     alt="Polar pattern of a half-wave dipole with the half-power points and nulls marked"
     style="max-width: 620px; width: 100%; display: block; margin: 1em auto;">

Solving $\vert F(\theta)\vert^2 = 1/2$ numerically gives half-power points at
$\theta = 51.0^\circ$ and $129.0^\circ$, so

$$\theta_\text{HP} = 78^\circ.$$

Integrating $\vert F\vert^2$ over the sphere gives the directivity,

$$D = \frac{2\ \vert F\vert^2_\text{max}}{\displaystyle\int_0^\pi \vert F(\theta)\vert^2 \sin\theta\ d\theta} = 1.64 = 2.15\ \text{dBi}.$$

Now look at what doubling the wire actually bought you: the beamwidth went from
$90^\circ$ to $78^\circ$ and the directivity went from $1.76$ to
$2.15\ \text{dBi}$. **A gain of 0.39 dB.** If the half-wave dipole is famous, it
is not for its pattern.

:::{admonition} Key Point
:class: key-concept
A dipole's **pattern** is set by how many wavelengths of current fit on the
wire. Its **impedance** is set by where the current maximum lands relative to
the feed. Half a wavelength is the celebrated length because it puts the
current maximum right at the feed point, and it costs only 0.39 dB of
directivity to get there.
:::

Copper is a good conductor, so radiation efficiency for a wire dipole is above
about 98% and $G = e_{cd} D$ is within a tenth of a dB of $D$. For this antenna
you may quote gain and directivity interchangeably — but say which one you
mean, because for the lossy antennas in Module 4 they part company.

Keep stretching the wire past $\lambda/2$ and the standing wave develops
**phase reversals**: sections of the wire carry current in the opposite
direction. Reversed current radiates out of step with the rest, the
contributions interfere, and the single doughnut breaks into lobes.

<img src="../../viz/img/L07-dipole-patterns.svg"
     alt="Polar patterns of dipoles half a wavelength, one wavelength, 1.25 and 1.5 wavelengths long"
     style="max-width: 760px; width: 100%; display: block; margin: 1em auto;">

The interactive below is the fastest way to internalize all of this. Drag the
length slider from one end to the other and watch three things at once: the
standing-wave current on the wire, the pattern it produces, and the numbers in
the pills underneath. Notice that **below half a wavelength almost nothing
changes** — the pattern is essentially the short-dipole doughnut all the way
down, which is why an electrically small antenna is an impedance problem and
not a pattern problem. Then notice that directivity **creeps upward until about
1.2 to 1.25 wavelengths**, where it peaks near $5.2\ \text{dBi}$, and that past
that point **the main lobe splits** and the broadside gain collapses. Park the
slider at $0.50$ and confirm the canonical trio: $78.1^\circ$,
$2.15\ \text{dBi}$, $73.1\ \Omega$.

<iframe src="../../viz/dipole-explorer.html"
        width="100%" height="711"
        style="border: 1px solid #cddce9; border-radius: 6px;"
        loading="lazy"
        title="Dipole explorer: current, pattern, beamwidth, directivity and feed-point impedance against dipole length">
</iframe>

```{note}
The resistance and reactance in that widget are referred to the **current
maximum**, not to the terminals. At $L = \lambda/2$ the current maximum sits at
the feed and the two are the same number, which is the case you care about. For
other lengths the terminal values are larger by $1/\sin^2(kL/2)$ — a short
dipole's tiny current-maximum reactance becomes an enormous terminal reactance,
which is precisely why short antennas are so hard to feed.
```

## Part 4: Impedance and resonance

The pattern was the easy half. What the transmitter actually feels is the
**input impedance**, and for a thin half-wave dipole both parts of it can be
computed — the resistance from the pattern you just derived, the reactance from
one standard result we will name but not re-derive.

### The resistance, from the pattern

**Radiation resistance** is defined by asking what resistor, carrying the same
current, would dissipate the power the antenna radiates:

$$P_\text{rad} = \frac{1}{2}\vert I_m \vert^2 R_r$$

So compute $P_\text{rad}$ and you have $R_r$. Start from Part 3's pattern. The
radiation intensity of the half-wave dipole is

$$U(\theta) = \frac{\eta \vert I_m \vert^2}{8\pi^2}\left[\frac{\cos\left(\dfrac{\pi}{2}\cos\theta\right)}{\sin\theta}\right]^2$$

and the radiated power is that intensity integrated over the whole sphere.
Nothing depends on $\phi$, so the azimuth integral simply contributes $2\pi$:

$$P_\text{rad} = \int_0^{2\pi}\int_0^\pi U(\theta) \sin\theta\ d\theta\ d\phi = \frac{\eta \vert I_m \vert^2}{4\pi}\int_0^\pi \frac{\cos^2\left(\dfrac{\pi}{2}\cos\theta\right)}{\sin\theta}\ d\theta$$

Here the derivation stops being algebra. **That integral has no elementary
antiderivative.** You cannot write the answer in terms of sines, logs, and
powers — this is the point where a *number* enters instead of a formula.

That is not a failure, and it is not unusual. It is the same situation as
$\text{erf}$ in probability: the integral is important enough that somebody
tabulated it, gave it a name, and moved on. Antenna work leans on three such
**special functions**, and you will meet all of them again:

$$C_{in}(x) = \int_0^x \frac{1 - \cos u}{u}\ du \qquad Si(x) = \int_0^x \frac{\sin u}{u}\ du \qquad Ci(x) = -\int_x^\infty \frac{\cos u}{u}\ du$$

Look them up, or let a calculator evaluate them; do not try to integrate them.
The value this problem needs is

$$\int_0^\pi \frac{\cos^2\left(\dfrac{\pi}{2}\cos\theta\right)}{\sin\theta}\ d\theta = \frac{1}{2}C_{in}(2\pi) = 1.2188$$

Equate the two expressions for $P_\text{rad}$; the $\vert I_m \vert^2$ cancels
and the antenna's current level drops out, as it must:

$$R_r = \frac{\eta}{4\pi}C_{in}(2\pi) = 29.98 \times 2.4376 = 73.1\ \Omega$$

The $\eta/4\pi$ is just $30\ \Omega$ to slide-rule accuracy, so the whole result
is worth remembering as **30 times 2.4376**.

### The reactance, and why 42.5 is a clean number

A far-field power integral can only ever produce the real part — it accounts
for power that *leaves*. The reactance describes energy stored in the near
field and handed back every cycle, which never crosses the far-field sphere at
all, so no amount of pattern integration will produce it.

Getting it requires the **induced-EMF method**: integrate the field the antenna
produces back against its own current, along the wire. That is a near-field
calculation, we are not going to do it here, and its general answer is an
unpleasant expression involving $Si$, $Ci$, and the wire radius $a$. But at
exactly $L = \lambda/2$ something very tidy happens. Every radius-dependent
term in that expression carries a factor of $\sin(kL)$, and at $kL = \pi$,

$$\sin(kL) = \sin\pi = 0.$$

The wire radius drops straight out, and what survives is a single special
function:

$$X = \frac{\eta}{4\pi}Si(2\pi) = 29.98 \times 1.4182 = 42.5\ \Omega$$

:::{admonition} Key Point
:class: key-concept
**The reactance of a dipole is radius-independent only at exactly
$\lambda/2$.** That is why $42.5\ \Omega$ can be quoted as a clean number at
all, while at every other length the reactance depends on how fat the wire is —
which is exactly why the three curves in the figure below separate everywhere
except where they cross at $\lambda/2$.
:::

Put the two halves side by side and the whole impedance is one line, built from
two tabulated numbers:

$$Z_{in} = \frac{\eta}{4\pi}\left[C_{in}(2\pi) + j\ Si(2\pi)\right] = 29.98\left(2.4376 + j1.4182\right) = 73.1 + j42.5\ \Omega$$

So read the two parts separately. The $73\ \Omega$ is power leaving and never
coming back — the whole point of the antenna. The $+j42.5\ \Omega$ is the
reactive near field of Lesson 5, sloshing energy back and forth, doing no
useful work, and wrecking your match.

```{note}
Two honesty notes before we spend this number. $R_r$ came out referred to the
**current maximum**, because $I_m$ is the current-maximum amplitude; it equals
the *input* resistance here only because at $\lambda/2$ the maximum happens to
sit at the feed. And the induced-EMF result inherits the assumed sinusoidal
current from Part 2 — the impedance is the quantity most sensitive to that
assumption, and closing that gap against a real solver is precisely what
Lesson 8 is for.
```

**Resonance** means $X_{in} = 0$. At exactly $\lambda/2$ we are $42.5\ \Omega$
away from it, and the fix is to make the wire slightly *shorter*.

<img src="../../viz/img/L07-dipole-resonance.svg"
     alt="Feed-point reactance against dipole length for three wire thicknesses, showing zero crossings below half a wavelength"
     style="max-width: 700px; width: 100%; display: block; margin: 1em auto;">

Why shorter? Because the wire is electrically longer than it is physically.

- **End effect.** Capacitance between the tips of the dipole — and to the
  insulators, mast, and everything else nearby — lets charge accumulate past
  where the metal stops. The standing wave behaves as though the wire continued
  a little further than it does.
- **Wire thickness.** A fatter element has more end capacitance and a lower
  characteristic impedance, so it shortens further. This is why a thin wire
  resonates near $0.480\lambda$ while a fat tubular element can drop to
  $0.46\lambda$.

Both effects slow the wave traveling on the wire relative to free space, and a
slower wave needs less physical length to fit the same electrical half
wavelength. For ordinary wire the answer lands in the range
$0.47\lambda$ to $0.48\lambda$, and the resistance drops with the length, to
roughly $70\ \Omega$.

:::{admonition} Rule of thumb — the 5% rule
:class: key-concept
Cut a resonant dipole to about **95% of a half wavelength**:

$$L \approx 0.95 \times \frac{\lambda}{2} = 0.475\ \lambda \approx \frac{143}{f_\text{MHz}}\ \text{m} \qquad \left(\frac{468}{f_\text{MHz}}\ \text{ft}\right)$$

Cut it long and trim. You can always remove wire.
:::

With a resonant dipole in hand, the match is a one-line calculation. Using
$\Gamma = (Z_L - Z_0)/(Z_L + Z_0)$ and $\text{VSWR} = (1+\vert\Gamma\vert)/(1-\vert\Gamma\vert)$
from Lesson 4:

| Line | Load used | $\vert \Gamma \vert$ | VSWR |
| :-- | :-- | :-- | :-- |
| $50\ \Omega$ | $73 + j42.5$ (untrimmed) | 0.37 | 2.18 |
| $50\ \Omega$ | $70 + j0$ (resonant) | 0.17 | 1.40 |
| $75\ \Omega$ | $73 + j42.5$ (untrimmed) | 0.28 | 1.76 |
| $75\ \Omega$ | $70 + j0$ (resonant) | 0.03 | 1.07 |

Read that table as a decision. Trimming the antenna to resonance improves the
$50\ \Omega$ match more than switching to a $75\ \Omega$ cable does. **Kill the reactance
first; worry about the resistance second.**

### Reading it off a Smith chart

Those four rows are the same information a **Smith chart** shows at a glance,
and you will be reading charts for the rest of the course — every VNA in the
lab draws one. The chart is just the complex reflection coefficient plane with
a grid of constant-resistance circles and constant-reactance arcs painted on
it: the center is a perfect match, the rim is total reflection, the top half is
inductive and the bottom half capacitive.

Sweep the length slider below and watch the dipole trace a path across the
chart. Three things are worth pinning down. **Find the $\lambda/2$ marker** and
confirm it reads $73 + j42.5\ \Omega$ sitting in the inductive half, outside the
2:1 circle. **Then trim** — walk the slider down until the locus crosses the
horizontal axis, which is the resonant length, and watch the VSWR pill drop as
you cross inside the 2:1 circle. **Then flip the normalization to
$75\ \Omega$**: the antenna does not change, the impedance readout does not
change, but the whole grid re-scales underneath it and the same antenna lands
closer to the center. That last point is the one students find surprising, and
it is worth sitting with: a match is a statement about a *pair*, not about an
antenna.

<iframe src="../../viz/dipole-smith.html"
        width="100%" height="597"
        style="border: 1px solid #cddce9; border-radius: 6px;"
        loading="lazy"
        title="Smith chart showing how a dipole's input impedance moves as its length changes, with constant-VSWR circles">
</iframe>

```{note}
The resonance marker in that chart sits near $63\ \Omega$, not the $70\ \Omega$
the design rule quotes. That is the assumed-sinusoidal-current model showing
its limits again, exactly as flagged above — the model puts resonance in the
right *place* and gets the reactance slope right, but it runs a few ohms low on
the resistance. Trust the chart for the shape of the behavior and the design
rule for the number.
```

One last practical matter before you connect anything. A dipole is a
**balanced** structure and coax is **unbalanced**. Wire them together directly
and current flows on the outside of the shield, the feedline joins the
radiating structure, and your pattern and VSWR both start depending on where
you are standing. Lesson 4 gave you the fix: put a **balun** at the feed point.
Every dipole in this course gets one.

## Part 5: Cutting a real dipole

:::{admonition} Worked example — a 2 meter dipole for 146 MHz
:class: tip
**Design a resonant half-wave dipole for 146 MHz and predict what the analyzer
will show.**

*Wavelength.*

$$\lambda = \frac{c}{f} = \frac{3 \times 10^8}{146 \times 10^6} = 2.055\ \text{m}$$

*Physical length.* A half wavelength is $1.027\ \text{m}$; apply the 5% rule:

$$L = 0.475\lambda = 0.475 \times 2.055 = 0.976\ \text{m}$$

Cross-check with the field-manual form: $143/146 = 0.980\ \text{m}$. The two
agree to within a centimeter, which is about the precision the rule deserves.

*Cut list.* Two arms of $L/2 = 48.8\ \text{cm}$, fed at the center, with a
balun.

*Predicted performance.*

| Quantity | Value | Where it came from |
| :-- | :-- | :-- |
| $Z_{in}$ | $\approx 70 + j0\ \Omega$ | resonant, trimmed |
| VSWR on $50\ \Omega$ | 1.40 | $\vert\Gamma\vert = 20/120 = 0.167$ |
| VSWR on $75\ \Omega$ | 1.07 | $\vert\Gamma\vert = 5/145 = 0.034$ |
| Gain | $2.15\ \text{dBi}$ | $D = 1.64$, copper loss negligible |
| $\theta_\text{HP}$ | $78^\circ$ | half-wave pattern |
| Far-field distance | $2D^2/\lambda = 0.93\ \text{m}$ | Lesson 5, with $D = 0.976\ \text{m}$ |

*Sanity check.* Every number is boring, which is the correct outcome. A dipole
that predicts 12 dBi or $8\ \Omega$ means you made an arithmetic error, not a
discovery.
:::

```{note}
Two of those numbers deserve an honest footnote. The sinusoidal-current model
used here predicts a resonant resistance in the low sixties; a full numerical
solver and a real measurement both land closer to $70\ \Omega$. And the exact
resonant length depends on wire gauge, insulation, and what is nearby. Carry
$70\ \Omega$ and $0.475\lambda$ as the design numbers, and expect a few percent
of disagreement — quantifying that disagreement is what the next lesson is for.
```

## Summary

| Symbol / idea | What it is | Number to remember |
| :-- | :-- | :-- |
| Isotropic radiator | Equal radiation in all directions; impossible, but the reference for everything | $D = 1$, $0\ \text{dBi}$ |
| EIRP | Transmitter and antenna as one number, $P_t G_t$ | $\text{dBi} = \text{dBd} + 2.15$ |
| Assumed current | Standing wave from the unfolded open-circuited line | $I_m \sin[k(L/2 - \vert z\vert)]$ |
| Short dipole | Constant current, limiting case | $\vert F\vert = \sin\theta$, $1.76\ \text{dBi}$ |
| Dipole pattern, any length | One radiation integral, every length; normalize by the peak | $\vert F\vert \propto \left\vert\left[\cos\left(\frac{kL}{2}\cos\theta\right) - \cos\frac{kL}{2}\right]/\sin\theta\right\vert$ |
| Half-wave dipole pattern | The general result at $kL/2 = \pi/2$ | $\theta_\text{HP} = 78^\circ$ |
| Half-wave directivity | From integrating the pattern over the sphere | $D = 1.64 = 2.15\ \text{dBi}$ |
| Special functions | Tabulated, like $\text{erf}$ — do not integrate them | $C_{in}(2\pi) = 2.4376$, $Si(2\pi) = 1.4182$ |
| Half-wave impedance | Resistance from the far field, reactance from induced EMF | $\frac{\eta}{4\pi}\left[C_{in}(2\pi) + jSi(2\pi)\right] = 73 + j42.5\ \Omega$ |
| Resonance | $X_{in} = 0$, reached by trimming | $0.47\lambda$ to $0.48\lambda$, $\approx 70\ \Omega$ |
| The 5% rule | Resonant length from frequency | $143/f_\text{MHz}$ meters |
| Longer dipoles | Phase reversals build lobes | Peak $\approx 5.2\ \text{dBi}$ near $1.25\lambda$ |

## Practice

- <a href="../../practice/ECE444_L07_Practice_blank.pdf" target="_blank" rel="noopener">Problem set (PDF)</a>
- <a href="../../practice/ECE444_L07_Practice_SOLUTIONS.pdf" target="_blank" rel="noopener">Solutions (PDF)</a>

## Where this is going

Lesson 8 puts this exact antenna into 4nec2. You will model a wire, set its
length, sweep the frequency, and read back impedance, VSWR, gain, and pattern —
and then compare each one against the numbers you produced by hand today. **The
numbers you just predicted are the ones you will check against simulation.** A
simulator that agrees with a hand calculation on a dipole can be trusted a
little further on a structure you cannot solve by hand; a simulator that
disagrees is telling you that you have set something up wrong, and the only way
to know which is to bring predictions with you.

After that, Lesson 9 takes the same wire apart. Cut a dipole in half and stand
it on a ground plane and you have a monopole — half the impedance, double the
directivity, and only the upper half-space to radiate into. Bend it into a
circle and you have a loop, whose behavior depends entirely on whether the
circumference is small or comparable to a wavelength. Further out, in Module 3,
the dipole stops being an antenna and becomes an *element*: line up many of
them, control the phase of each, and pattern multiplication turns 2.15 dBi into
whatever the array is long enough to deliver.
