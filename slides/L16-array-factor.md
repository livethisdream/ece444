<!-- .slide: class="title-slide" -->

<div class="title-left">

# ECE 444

Antennas, Phased Arrays, and Radar Systems

## Lesson 16 — The Array Factor and Pattern Multiplication

Fall 2026 · Dr. Neil Rogers

</div>

<div class="title-right">

![USAFA](./img/01-course-intro/USAFA-logo.png)

</div>

---

## Where We Were

- Lesson 6: pattern = element factor × space factor, and the space factor is the transform of the current distribution
- Lesson 15: a continuous aperture — length sets the beamwidth, taper sets the sidelobes
- Uniform aperture: $-13.3$ dB first sidelobe, HPBW $\approx 0.886\ \lambda/L$
- The PHASER has no continuous aperture; it has eight patches in a row.

Today we replace the aperture with N elements, and the integral becomes a sum, the **array factor**.

Note:
Anchor on Lesson 15. Ask the class what the uniform aperture gave us: point-eight-eight-six lambda over L, and minus thirteen decibels. Both numbers come back at the end of the hour from a different starting point.

---

## Today's Plan

1. Set up N elements on a line and derive the array factor by summing phasors
2. Set every weight to one and collapse the sum with a geometric series
3. Read the anatomy: main lobe, nulls, sidelobes
4. Multiply an element pattern by an array factor
5. Find the visible region, and the spacing where a second beam appears
6. Recover Lesson 15 by treating the array as a sampled aperture

Note:
Item one is the board derivation, and everything after it reads the result. Tell them the derivation is testable and that they need to memorize the closed form.

---

## From an Aperture to Elements

<div class="fig" data-inline-svg="./fig/L16-sampled-aperture.svg" style="max-width:760px; margin:0 auto;"></div>

The overall length is the same; the current now exists at N places instead of everywhere.

Note:
Draw the analogy before any algebra. A phased array is a sampled aperture. Everything we proved about apertures still applies, and sampling adds one new effect, the grating lobe. Ask them to guess what sampling does before we get there.

---

## The Linear Array

<div class="fig" data-inline-svg="./fig/L16-array-geometry.svg" style="max-width:720px; margin:0 auto;"></div>

The elements are identical, the spacing is $d$, and we feed element $n$ the complex weight $a_n$.

Note:
Three assumptions, written on the board and kept there: identical elements, identically oriented, uniform spacing. We use every one of them later. If the elements differ, pattern multiplication fails and we are back to summing element by element.

---

## The Scan Angle

<div class="two-col">
<div class="col-text">

**Module 3 convention**

- $\theta$ measured from **broadside**
- $-90^\circ \le \theta \le +90^\circ$
- Matches every PHASER plot and the GUI axis

**Bridge to Module 1**

$$\theta_\text{polar} = 90^\circ - \theta$$

$$\cos\theta_\text{polar} = \sin\theta$$

</div>
<div class="col-fig">

The Lesson 6 space frequency

$$k_z = k\cos\theta_\text{polar}$$

becomes

$$k\sin\theta$$

Broadside was $90^\circ$. It is now $0^\circ$.

</div>
</div>

Note:
This is the only slide in the course where both conventions are on the board at once. Make them write the mapping down. From here on, theta means scan angle from broadside, and every sine you see used to be a cosine.

---

## The Two Angle Conventions

<div class="fig" data-inline-svg="./fig/L16-scan-angle.svg" style="max-width:680px; margin:0 auto;"></div>

Note:
One ray, two angles. The scan angle is measured from broadside, the polar angle from the array axis, and they add to ninety degrees. Here the ray is thirty-five degrees off broadside, which is fifty-five degrees in the Module 1 convention.

---

## Extra Path Length

A far-field observer sees the rays from every element as parallel.

Element $n$ sits $nd$ along the axis. Along a ray at angle $\theta$ its path is shorter by

$$\Delta r_n = n\ d\sin\theta$$

<div class="callout">
Only the <strong>projection</strong> of the element spacing onto the look direction matters. At broadside the projection is zero and every element is the same distance away.
</div>

Note:
Do this at the board with a ruler. Drop a perpendicular from element zero onto the ray through element n. The little triangle has hypotenuse d and the side you want is d sine theta. Repeat it for element two so they see the n multiplying.

---

## Path Difference to Phase

Distance turns into phase through $k = 2\pi/\lambda$:

$$\text{phase lead} = k\ \Delta r_n = n\ kd\sin\theta$$

Element $n$ therefore contributes

$$a_n\ e^{\ +jn\ kd\sin\theta}$$

The amplitudes are equal, because 112 mm of array changes $1/r$ by less than 0.4% at 30 m.

Note:
Emphasize that we keep the phase difference and drop the amplitude difference. That is the parallel-ray approximation of Lessons 5 and 6. The PHASER's far field starts at two D squared over lambda, about point eight six meters. One over R n equals one over R, but k times R n is not k times R: the same 112 millimeters is nearly fourteen hundred degrees of phase.

---

## Superposition

$$E(\theta) = \sum_{n=0}^{N-1} a_n\ E_0(\theta)\ \frac{e^{-jkr}}{r}\ e^{\ jn\ kd\sin\theta} = E_0(\theta)\ \frac{e^{-jkr}}{r} \sum_{n=0}^{N-1} a_n\ e^{\ jn\ kd\sin\theta}$$

The elements are identical, so $E_0(\theta)$ is the same for every term and factors out of the sum.

Note:
The factoring step is where pattern multiplication comes from. Point at it and say so. It works only because every element has the same E-zero of theta. Come back to this slide in twenty minutes. If anyone asks how this connects to Lesson 6: put a point current of strength a n at each z equals n d into the radiation vector N z, and the integral collapses to the same sum. The page has that derivation in read mode.

---

## The Array Factor

$$AF(\theta) = \sum_{n=0}^{N-1} a_n\ e^{\ jn\ kd\sin\theta}$$

- One term per element
- Depends on **count, spacing, and weights** only
- Does not depend on the type of element

<div class="callout">
This sum describes any uniformly spaced linear array with any weights. Every other result today is a special case of it.
</div>

Note:
Have them write the general sum before we specialize. On the board, do a three-element example with weights one, two, one so they see it is just arithmetic with complex numbers.

---

## Steering Phase

Let the weights carry a progressive phase:

$$a_n = \vert a_n\vert\ e^{-jn\beta}$$

The geometric phase and the applied phase carry the same index, so we combine them:

$$\psi = kd\sin\theta - \beta = kd\left(\sin\theta - \sin\theta_0\right)$$

with $\beta = kd\sin\theta_0$ the steering ramp — Lesson 18.

Today $\theta_0 = 0$, so $\psi = kd\sin\theta$.

Note:
Flag psi as the variable the rest of the module works in. It absorbs frequency, spacing, look angle, and steering into one number. When a plot looks strange later, the first question is always what psi is doing.

---

## The Phasor Sum

<div class="fig" data-inline-svg="./fig/L16-phasor-sum.svg" style="max-width:740px; margin:0 auto;"></div>

<p class="viz-cue">↗ Interactive on the lesson page</p>

Note:
Walk the three panels. All in phase, the sum equals N. Fan them out, and the chain bends and the sum shortens. Fan them by exactly one N-th of a turn each, and the chain closes into a polygon, so the sum is zero. That last picture is the first null. Then demo the phasor-chain widget on the lesson page: drag theta slowly from zero and stop when the chain closes at fifteen point one degrees.

---

## Uniform Excitation

Set $a_n = 1$ for every element. The sum is geometric in $e^{\ j\psi}$:

$$AF = \sum_{n=0}^{N-1} e^{\ jn\psi} = \frac{1 - e^{\ jN\psi}}{1 - e^{\ j\psi}}$$

Note:
Remind them of the finite geometric series from calculus. Ratio is e to the j psi, N terms. If somebody asks about psi equal to zero, the ratio is one and the formula is indeterminate; we take that limit two slides from now.

---

## Summing the Geometric Series

Factor half of each exponent out, top and bottom:

$$\frac{1 - e^{\ jN\psi}}{1 - e^{\ j\psi}} = \frac{e^{\ jN\psi/2}\left(e^{-jN\psi/2} - e^{\ jN\psi/2}\right)}{e^{\ j\psi/2}\left(e^{-j\psi/2} - e^{\ j\psi/2}\right)}$$

Each bracket is $-2j\sin(\cdot)$, and those factors cancel:

$$= e^{\ j(N-1)\psi/2}\ \frac{\sin(N\psi/2)}{\sin(\psi/2)}$$

Note:
This is the one algebra step worth doing slowly at the board. The trick is symmetrizing the exponent so Euler's formula appears. Then the minus two j cancels between top and bottom.

---

## The Closed Form

The leading exponential is the phase of the array center, and referencing the phase to the center removes it. Dividing by $N$ sets the peak to one:

$$AF_N(\psi) = \frac{\sin(N\psi/2)}{N\sin(\psi/2)}$$

<div class="callout">
<strong>Memorize this line.</strong> Every lab in Module 3 predicts its measurement from it.
</div>

Note:
Say the normalization out loud: peak equals one, which is why the N sits in the denominator. Different books normalize differently and the sidelobe numbers do not change, but the peak does.

---

## Main Lobe and Nulls

**Peak.** At $\psi = 0$ the ratio is zero over zero, and the limit is one, so the beam points where $\sin\theta = \sin\theta_0$.

**Nulls.** The numerator vanishes and the denominator does not:

$$\psi_m = \frac{2\pi m}{N} \qquad\Longrightarrow\qquad \sin\theta_m = \sin\theta_0 + \frac{m\lambda}{Nd}$$

The **total length** $Nd$ sets the nulls, not $d$ alone.

Note:
Take the limit at the board with L'Hopital or with the small-angle argument. Then stress the N d dependence: doubling the element count at fixed spacing halves the beamwidth, and so does doubling the spacing at fixed count, but the second one brings in grating lobes, which we reach in the visible-region slides.

---

## Sidelobes

- One sidelobe between each pair of nulls: $N-2$ per period
- Heights fall as $1/\sin(\psi/2)$, so the first is the tallest
- The first peaks near $N\psi/2 = 3\pi/2$, halfway between the first two nulls:

$$AF_N \approx \frac{1}{N\sin(3\pi/2N)} \quad\longrightarrow\quad \frac{2}{3\pi} \approx -13.5\ \text{dB}$$

- The exact peak gives $-13.3$ dB for large $N$ and $-12.8$ dB at $N = 8$

The first sidelobe sits about $-13$ dB down, the same level the uniform aperture gave in Lesson 15.

Note:
This is the result promised at the start. The exact peak sits a little inside three pi over two, toward the main lobe, because the denominator is still growing across the gap. A discrete uniform array and a continuous uniform aperture have the same first sidelobe, because in the many-element limit the array factor becomes the sinc. Uniform excitation leaves the first sidelobe about thirteen decibels down, whether the current is continuous or sampled.

---

## First Sidelobe Against N

<div class="fig" data-inline-svg="./fig/L16-sidelobe-vs-n.svg" style="max-width:740px; margin:0 auto;"></div>

Note:
The exact first sidelobe rises toward minus thirteen point three as N grows: minus eleven point three at four elements, minus twelve point eight at eight, and within two tenths of a decibel of the line source by sixteen. The halfway-between-nulls estimate runs a little low at every N because the true peak sits slightly inside three pi over two.

---

## The Eight-Element Array Factor

<div class="fig" data-inline-svg="./fig/L16-af-anatomy.svg" style="max-width:770px; margin:0 auto;"></div>

Note:
Have them count the sidelobes on the plot: six, which is N minus two. Then ask why the pattern stops just short of a repeat at plus and minus ninety degrees. That question is the visible region, coming up in ten minutes.

---

## Reading the Closed Form

| Feature | Condition | Uniform value |
| :-- | :-- | :-- |
| Peak | $\psi = 0$ | $\theta = \theta_0$ |
| Null $m$ | $\psi = 2\pi m/N$ | $\sin\theta_m = \sin\theta_0 + m\lambda/Nd$ |
| FNBW | $m = \pm 1$ | $2\arcsin(\lambda/Nd)$ |
| HPBW | $L = Nd$ | $\approx 0.886\ \lambda/(Nd\cos\theta_0)$ |
| First sidelobe | $N\psi/2 \approx 3\pi/2$ | $-13$ dB |

Lesson 20 derives the beamwidth closed forms.

Note:
Tell them to copy this table into their notes. It is the reference sheet for the next six lessons, and the lab expectation tables come from these five rows. The half-power row uses the line-source constant with L equals N d; for the PHASER the exact width is thirteen point three degrees against thirteen point two.

---

<!-- .slide: class="viz-cue-slide" -->

## Array Factor Builder

<div class="fig" data-inline-svg="./fig/L16-af-builder.svg" style="max-width:760px; margin:0 auto;"></div>

<p class="viz-cue">↗ Interactive on the lesson page</p>

Note:
Demo live. Start at N equals eight and spacing point four eight one and read the pills against the table: thirteen point two degrees, first null fifteen point one, first sidelobe minus twelve point eight. Sweep N and let them see that the sidelobe level stays near minus thirteen. Then push the spacing past one and stop before explaining the second beam that moves in; that sets up the visible region.

---

## Pattern Multiplication

Back on the superposition slide, $E_0(\theta)$ came out of the sum because the elements are identical.

$$\vert F(\theta)\vert = \vert EF(\theta)\vert \times \vert AF(\theta)\vert$$

- $EF$ is the pattern of one element alone
- $AF$ is what the arrangement adds
- In decibels the two curves add

<div class="callout">
Pattern multiplication holds for identical, identically oriented elements. Mixed element types break it.
</div>

Note:
This is the most useful theorem in array work. It also tells us what we can and cannot fix. Weights cannot fix a bad element pattern, and a better element cannot fix a bad array factor. This is Lesson 6's element factor times space factor, with a sum in place of the integral.

---

## Element Factor Times Array Factor

<div class="fig" data-inline-svg="./fig/L16-pattern-multiplication.svg" style="max-width:770px; margin:0 auto;"></div>

Four collinear short dipoles at $d = \lambda/2$

Note:
Point out the two effects. The element factor pulls the outer sidelobes down and leaves the main lobe nearly alone, because cosine is flat near broadside. Then ask which curve sets the beamwidth. The array factor does.

---

## Worked Example: Four Short Dipoles

$d = \lambda/2$, fed in phase, element pattern $EF = \cos\theta$ (Lesson 7's short dipole in scan angle)

| Quantity | Work | Result |
| :-- | :-- | :-- |
| AF nulls | $\sin\theta_m = m/2$ | $\pm 30^\circ$, $\pm 90^\circ$ |
| AF first sidelobe | peak of $AF_4$ | $-11.3$ dB at $47.1^\circ$ |
| Element at that angle | $\cos 47.1^\circ = 0.681$ | $-3.3$ dB |
| Total sidelobe | add in dB | $\approx -14.6$ dB |
| Exact product peak | maximize $EF \cdot AF$ | $-14.4$ dB at $44.2^\circ$ |

Note:
Work the dB rows live. Adding the levels at forty-seven point one degrees is an estimate; the product peaks a little closer to broadside, at forty-four point two, where the cosine is larger, and sits at minus fourteen point four. The element factor added about three decibels of suppression because the sidelobe sits well off broadside. The main lobe narrows only from twenty-six point three to twenty-five point four degrees. That is why array designers care about element patterns even though the array factor gets most of the attention.

---

## The Four-Dipole Sidelobe

<div class="fig" data-inline-svg="./fig/L16-four-dipole-zoom.svg" style="max-width:740px; margin:0 auto;"></div>

Note:
Adding decibels at the array factor's peak gives the amber point, minus fourteen point six. The product's own peak is the red point, three degrees closer to broadside and two tenths of a decibel higher, because the array factor is flat at its own peak while the element factor keeps rising toward broadside.

---

## The Visible Region

Real angles tie $\psi$ to a window. As $\theta$ sweeps $\pm 90^\circ$:

$$kd\left(-1 - \sin\theta_0\right) \le \psi \le kd\left(+1 - \sin\theta_0\right)$$

- The window width is $2kd = 4\pi d/\lambda$, fixed by the spacing
- The window **slides** as we steer
- Values of $\psi$ outside it match no real angle, so the array never radiates them

Note:
Two motions to keep separate. Changing the spacing changes the width of the window. Changing the steer angle slides the window without resizing it. Width alone does not make a grating lobe: at half-wavelength spacing the window is already one full period wide, from minus pi to plus pi. A second beam appears only when an edge of the window reaches a repeat at plus or minus two pi.

---

## Visible Region at Two Spacings

<div class="fig" data-inline-svg="./fig/L16-visible-region.svg" style="max-width:730px; margin:0 auto;"></div>

<p class="viz-cue">↗ Interactive on the lesson page</p>

Note:
Top panel is the PHASER: the window stops just short of the repeat. Bottom panel is one-wavelength spacing, where the repeat sits exactly at the edge of view. Ask what happens between those two cases and then at one point five wavelengths. Then demo the visible-region widget: widen the spacing and watch the window grow, then steer and watch it slide, and stop when a repeat crosses the window edge.

---

## Grating Lobes

$AF_N$ has period $2\pi$. A window whose edge reaches $\psi = \pm 2\pi$ admits a **full-height** copy of the main lobe:

$$\sin\theta_g = \sin\theta_0 \pm \frac{m\lambda}{d}$$

<div class="callout">
Avoidance criterion: <strong>d &lt; &lambda; / (1 + |sin &theta;<sub>0</sub>|)</strong> &nbsp;&mdash;&nbsp; broadside only: d &lt; &lambda;. To scan to &plusmn;90&deg;: d &lt; &lambda;/2.
</div>

Lesson 26 treats grating lobes in full, with beam squint and quantization.

Note:
At psi equals two pi, every element is one whole wavelength farther than its neighbor, after the applied phase, so they all add in phase again. That is why the lobe is full height. Derive the criterion at the board: the lobe nearest real space is m equals one on the far side of the steer, sine theta zero minus lambda over d, and it stays hidden while that is below minus one. Then say plainly what a grating lobe does: the array transmits or receives just as strongly in an unintended direction. In radar that is a false target bearing. In a comm link it is an interference path. This is why half-wavelength spacing is the default everywhere.

---

## Spacing Limit Against Scan Angle

<div class="fig" data-inline-svg="./fig/L16-grating-limit.svg" style="max-width:740px; margin:0 auto;"></div>

Note:
The curve is the grating-lobe criterion. One wavelength at broadside, point five eight six for a forty-five degree scan, half a wavelength for ninety. The PHASER's point four eight one sits under the curve everywhere, so it can scan anywhere without a grating lobe.

---

## The Array as a Sampled Aperture

$$AF_N = \frac{\sin(N\psi/2)}{N\sin(\psi/2)} \approx \frac{\sin(N\psi/2)}{N\psi/2}$$

| Parameter | What it controls |
| :-- | :-- |
| Total length $Nd$ | beamwidth, $\approx 0.886\ \lambda/Nd$ |
| Excitation shape | sidelobe level, $-13$ dB uniform |
| Spacing $d$ | what repeats — the grating lobe |

Sampling makes the pattern periodic. A continuous aperture has no grating lobes because it is not sampled.

Note:
Close the loop opened in slide four. Near the main lobe psi is small, so sine of psi over two is about psi over two, and the array factor becomes the sinc with u equal to k L over two times sine theta, the Lesson 6 line source with L equal to N d. Two arrays with the same total length have the same beam whether it is eight elements or thirty-two. The element count provides grating-lobe headroom and steering range, not beamwidth. The array samples the current only at multiples of d, so its phases cannot tell psi from psi plus two pi.

---

## The Large-N Limit

<div class="fig" data-inline-svg="./fig/L16-sinc-limit.svg" style="max-width:740px; margin:0 auto;"></div>

Note:
Plotted against u, the four, eight, and thirty-two element patterns all match the line-source sinc near the main lobe. They part where psi is no longer small: an N-element array repeats its main lobe N nulls out, so four elements repeat at four and eight at eight, while thirty-two follows the sinc across the whole plot.

---

## Worked Example: The Course Array

8 patches, $d = 14$ mm, $f = 10.3$ GHz, $\lambda = 29.1$ mm, $d/\lambda = 0.481$

| Quantity | Work | Result |
| :-- | :-- | :-- |
| Visible region | $\psi = \pm kd$ | $\pm 173.2^\circ$ — no repeat |
| Nulls | $\sin\theta_m = m/3.85$ | $15.1^\circ$, $31.3^\circ$, $51.2^\circ$ |
| FNBW | $2\arcsin(1/3.85)$ | $30.1^\circ$ |
| HPBW | $0.886\ \lambda/Nd$ | $13.2^\circ$ |
| First sidelobe | $N = 8$ | $-12.8$ dB at $21.9^\circ$ |

Note:
These five numbers are the Lesson 21 expectation table. Tell them now that the measured sweep will read thirteen point one degrees for the beamwidth and eleven to thirteen decibels for the sidelobes, and that the two point eight degree sweep grid and the noise floor near minus twenty-three decibels account for the difference. Lesson 20 derives the directivity, seven point seven, or eight point nine decibels. The lesson page carries the Lesson 21 measured-sweep widget; toggle the measurement effects to show the nulls fill in.

---

## Key Point

<div class="callout">
The array factor is a sum of element phasors, uniform weights collapse it to a closed form, and the element pattern multiplies it.<br>
Add the element phasors to get <em>AF</em>. Uniform weights collapse it to sin(N&psi;/2) over N sin(&psi;/2). Multiply by the element pattern for the real thing. Length sets the beam, weights set the sidelobes, spacing sets what repeats.
</div>

Note:
If they leave with one slide, this is it. Have them state the three sentences back before the bell.

---

## Looking Ahead

- **Lesson 17** — the hardware that produces $a_n$: ADAR1000 beamformers, per-element gain and phase, the receive chain
- **Lesson 18** — set the progressive ramp $\beta$ and steer the beam to $\theta_0$
- **Lesson 20** — beamwidth closed forms, and $D \approx 2Nd/\lambda$
- **Lessons 21, 25, 28** — measure this pattern, taper it, notch it

**Before next lesson:** be able to write $AF_N$ from memory and locate its nulls.

Note:
Every lab in this module measures some feature of today's array factor. We finish the theory before the hardware arrives on purpose: predict first, measure second, reconcile third.
