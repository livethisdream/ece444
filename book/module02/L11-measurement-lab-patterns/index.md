---
frame_view: true
---

# L11 - Measurement Lab 2: Radiation Patterns

::::{frame}
:class: title-frame

<div class="course-mark">ECE 444 · Fall 2026</div>

<h1 class="frame-title">Measurement Lab 2: Radiation Patterns</h1>

<div class="title-rule"></div>

You are measuring the same antenna, describing its other half.

Lesson 11 Lab · Antennas, Phased Arrays, and Radar Systems · Dr. Neil Rogers
::::

::::{frame} Slides
:class: read-only

:::{admonition} Slides
:class: slides
<a href="../../slides/L11-measurement-lab-patterns.html" target="_blank" rel="noopener">html slides</a>
<a href="../../slides/L11-measurement-lab-patterns.html?print-pdf" target="_blank" rel="noopener">pdf slides</a>
<a href="../../slides/L11-measurement-lab-patterns.md" target="_blank" rel="noopener">raw markdown slides</a>
:::
::::

::::{frame} Learning Objectives

<ol class="lo-list lo-sublist" style="--module: '2'; --lo: '7'">
  <li>I can verify that a given range geometry is valid for both antennas before I take data, using all three far-field criteria.</li>
  <li>I can acquire principal-plane pattern cuts and normalize, plot, and annotate them correctly in dB down from the peak.</li>
  <li>I can extract half-power beamwidth, first sidelobe level, front-to-back ratio, gain by comparison, and cross-polarization discrimination from measured data.</li>
  <li>I can measure my own noise floor, state the resulting dynamic range, and say which of my extracted numbers clears it and by how much.</li>
</ol>

:::{depth}
Last period you stood at the terminals and asked whether power gets *into* the
antenna. Today you walk three meters away and ask where that power *goes*. You
are measuring the same antenna and describing its other half, and the answer
this time is not a single number but a curve: a beamwidth, a sidelobe
structure, a back level, a polarization, and a hard limit on how much of that
curve is real.

Lesson 9 supplied the reasoning — reciprocity, the far-field criterion, gain
by comparison, and why a noise floor bounds every number you extract. Bring it
with you. Today is procedure and reduction.
:::
::::

::::{frame} What You Are Doing Today
:::{present}
- Prove the range is long enough, with a tape measure.
- Cut two principal planes, then a cross-pol cut.
- Swap in the reference horn for gain.
- Measure your own noise floor and quote it against everything.
:::

Reciprocity means it does not matter which end transmits, so the source
transmits and the antenna under test receives — the AUT is the thing that
rotates, and you would rather not run transmit power through a rotary joint.
::::

::::{frame} The Chain and Its Failure Modes
:::{present}
| Stage | Must do | Goes wrong as |
| :-- | :-- | :-- |
| Transmitter | one stable level | drift reads as pattern |
| Source | clean polarization | leaks into your cross-pol |
| Rotator | one centered axis | biased HPBW |
| Receiver | log power per angle | unrecorded settings |
:::

The hardware itself is flexible. A signal generator into a source horn with a
spectrum analyzer on the AUT works; so does an SDR pair, and the course
provides a **Pluto-SDR transmit/receive tool** that runs the
measure-rotate-record loop and writes an angle-versus-power file, which is the
option most sections will use. The choice of hardware does not change the
measurement. The acquisition discipline does.
::::

::::{frame} Your Bench Range
:::{present}
- $f = 2.45\ \text{GHz}$, so $\lambda = 12.2\ \text{cm}$.
- **AUT**: pyramidal horn, $24 \times 17\ \text{cm}$.
- **Reference**: standard-gain horn, $34 \times 25\ \text{cm}$, $G_{\text{ref}} = 15.0\ \text{dBi}$.
- Separation $3.0\ \text{m}$, equal heights, absorber at the midpoint.
:::

Those four lines are the whole range, and the next frame checks whether they
are good enough. The absorber goes at the specular floor-bounce point, which
is the midpoint when both antennas are at the same height.
::::

::::{frame} Is 3.0 m Far Enough?
:::{present}
$$\begin{aligned}
D_\text{AUT} &= \sqrt{0.24^2 + 0.17^2} = 0.294\ \text{m} \\
2D^2/\lambda &= 1.41\ \text{m}, \quad 5D = 1.47\ \text{m}, \quad 10\lambda = 1.22\ \text{m}
\end{aligned}$$

- Use the aperture **diagonal**, not a side.
- The binding criterion here is $5D$, not $2D^2/\lambda$.
:::
:::{present}
- The **reference** horn is the bigger antenna: $D = 0.422\ \text{m}$, so it needs $2.91\ \text{m}$.
- $3.0\ \text{m}$ clears it by 3%.
:::

Run all three criteria on both antennas, not just $2D^2/\lambda$ on the AUT.
For a physically small antenna the aperture-phase rule is often not the one
that decides, and here it is not. The reference sizes the range, and a 3%
margin is the correct statement of where you stand: the gain comparison is the
measurement sitting closest to the edge of the far field, and that belongs in
your report.

:::{depth}
Both antennas must be in each other's far field, and both must see the same
illumination. Set the heights with a tape, not by eye. A 5 cm height mismatch
over a 3 m range is a 1° pointing error, which is small — but it is a *bias*,
and biases do not average out over repeated sweeps.
:::
::::

::::{frame} Procedure — Align and Peak Up
:::{present}
1. Both antennas at equal height, boresights facing, co-polarized.
2. Fix one frequency, transmit level, resolution bandwidth, and averaging. Log them.
3. Rotate until received power peaks, and **define that angle as** $0^\circ$.
:::

Retuning anything mid-sweep invalidates the cut. A pattern referenced to the
wrong angle is worthless, because every number you extract afterwards is
measured from the peak.
::::

::::{frame} Procedure — Step Size and the Floor
:::{present}
4. Step $\le$ HPBW/5 — but take $2^\circ$, because sidelobes are narrower.
5. **Turn the source off and record the reading.**
:::
:::{present}
:class: callout
That number sets the credibility of your whole data set. Do it before you
sweep.
:::

This horn's beam is about $40^\circ$, so $8^\circ$ would satisfy the rule for
beamwidth alone. Coarse steps do not just add noise; they systematically miss
peaks and nulls, and a sidelobe you stepped over is a sidelobe you cannot
report.
::::

::::{frame} Procedure — The Four Sweeps
:::{present}
6. **E-plane cut**, $\pm 180^\circ$ if the rotator allows.
7. **H-plane cut**, by rotating both antennas $90^\circ$.
8. **Repeat one cut.** The disagreement *is* your repeatability.
9. **Gain comparison**: swap in the reference horn. Change nothing else.
:::

Two sweeps of the same cut that disagree by 1 dB have measured your
uncertainty directly, which is far more reliable than propagating catalog
tolerances. On step 9, "nothing else" means it: same range, same cables, same
source, same transmit level.
::::

::::{frame} Procedure — Polarization
:::{present}
10. Reinstall the AUT and rotate the **source** $90^\circ$ about the range axis. Re-sweep.
:::
:::{present}
:class: callout
Rotate the source, not the AUT. Rotating the AUT would change the cut plane
and the polarization at once, and you could not separate the two.
:::

That cut is your cross-pol pattern, and it is the last acquisition of the
period. Everything after this frame is reduction, and you can do it away from
the bench.
::::

::::{frame} Reduction — Normalize First
:::{present}
- Subtract the peak from every sample.
- Transmit power, cable loss, and range loss all drop out.
- Plot **polar dB** for shape, **rectangular dB** for values.
:::
:::{present}
:class: callout
Never plot pattern data linear. A $-13\ \text{dB}$ sidelobe is 5% of peak and
disappears.
:::
::::

::::{frame} Reduction — Four Numbers from the Shape
:::{present}
| Quantity | Read it as | Sanity |
| :-- | :-- | :-- |
| HPBW | the $-3$ dB crossings | vs. $26000/(\theta_E \theta_H)$ |
| First sidelobe | first lobe past the null | $-13$ to $-25$ dB |
| Front-to-back | peak minus $180^\circ$ | 15 to 25 dB |
| Null depth | minimum between lobes | floor-limited |
:::

Interpolate between samples for the $-3\ \text{dB}$ crossings. Snapping to the
nearest grid point throws away most of the precision your $2^\circ$ step
bought you.

:::{depth}
Worked example, one E-plane cut. The peak reads $-35.6\ \text{dBm}$ at
$0^\circ$, so the $-3\ \text{dB}$ level is $-38.6\ \text{dBm}$. Interpolating
between samples puts the crossings at $-19.8^\circ$ and $+20.2^\circ$:

$$\theta_\text{HP} = 20.2 - (-19.8) = 40.0^\circ$$

The first sidelobe peaks at $-51.4\ \text{dBm}$, and the level at $180^\circ$
is $-54.0\ \text{dBm}$:

$$\begin{aligned}
\text{SLL} &= -51.4 - (-35.6) = -15.8\ \text{dB} \\
\text{F/B} &= -35.6 - (-54.0) = 18.4\ \text{dB}
\end{aligned}$$

Cross-check the beamwidths against the gain: with an H-plane HPBW of
$42^\circ$, $26000/(40 \times 42) = 15.5$, or $11.9\ \text{dBi}$.
:::
::::

::::{frame} Reduction — Gain and XPD
:::{present}
$$\begin{aligned}
G_{\text{AUT}} &= G_{\text{ref}} + \left( P_{\text{AUT}} - P_{\text{ref}} \right) = 15.0 - 3.2 = 11.8\ \text{dBi} \\
\text{XPD} &= -35.6 - (-59.9) = 24.3\ \text{dB}
\end{aligned}$$

- Gain by comparison is one subtraction in dB.
- A healthy linear antenna gives 20 to 30 dB of XPD.
:::

The aperture formula with $\eta_{\text{ap}} = 0.5$ predicts $12.3\ \text{dBi}$,
so the measurement is 0.5 dB low — and the reference horn's own calibration is
good to about 0.5 dB. That is *agreement*, and your report should state it as
agreement rather than assign it a physical cause. Below about 15 dB of XPD,
check the mount alignment before blaming the antenna.
::::

::::{frame} How Much of Your Pattern Is Real
:class: viz-frame

:::{present}
<iframe src="../../viz/pattern-floor.html"
        width="100%" height="488"
        style="border: 1px solid #cddce9; border-radius: 6px;"
        loading="lazy"
        title="A true radiation pattern compared with the same pattern measured through a receiver with a finite noise floor">
</iframe>
:::

:::{depth}
Work your own numbers first: a peak at $-35.6\ \text{dBm}$ against a floor of
$-78\ \text{dBm}$ with the source off is a **dynamic range of 42.4 dB**. Any
feature within a few dB of $-42.4\ \text{dB}$ relative is a measurement of
your receiver, not of your antenna.

The widget makes the effect concrete. It takes a known pattern — a uniform
$8\lambda$ aperture, first sidelobe exactly $-13.3\ \text{dB}$, HPBW
$6.3^\circ$ — and "measures" it through a receiver with the dynamic range you
choose. Drag the floor from $-45\ \text{dB}$ up toward $-15\ \text{dB}$ and
watch the three readouts separately: the beamwidth barely moves, the first
sidelobe creeps upward by about a dB as the noise adds to it, and the nulls
stop dead at the floor. Each readout shows the measured figure against the
true one, and the null cell reads true / measured in that order. Then switch
averaging from 1 sweep to 16 and notice what averaging does and does not buy
you.
:::
::::

::::{frame} What to Trust, in Order
:::{present}
- **Beamwidth** is measured 3 dB down, far above any practical floor. Trust it first.
- **Sidelobes** are conditional. Quote the floor next to every one.
- **Nulls** measure your floor. Report them as lower bounds.
:::

A lobe 10 dB above the floor reads about 0.4 dB high; a lobe 3 dB above the
floor reads 3 dB high and is nearly meaningless. Averaging 16 sweeps smooths
the fuzz — incoherent power averaging shrinks the *variance* like $1/N$ — but
it leaves the mean noise power exactly where it was. To lower the floor you
need more transmit power, a narrower resolution bandwidth, or a quieter
receiver.
::::

::::{frame} The Rest of the Uncertainty Budget
:::{present}
| Source | Looks like | Size |
| :-- | :-- | :-- |
| Wall reflections | periodic ripple | $\pm 1$ dB |
| Cable flex | drift between sweeps | 0.2 to 0.5 dB |
| Misalignment | peak low, HPBW biased | 0.2 dB |
| Reference tolerance | offset on every gain | 0.3 to 0.5 dB |
:::

Each leaves a recognizable signature, and ripple is the most diagnostic of
them. A reflected path 20 dB below the direct path adds and subtracts to give
$+0.8\ \text{dB}$ and $-0.9\ \text{dB}$, a peak-to-peak ripple of about
1.7 dB. Count the ripples per degree and you can work backward to where the
reflection is coming from.
::::

::::{frame} Deliverables
:::{present}
1. **Two principal-plane cuts**, polar dB, normalized, labeled.
2. **An extracted table**, with an uncertainty on every row.
3. **Your noise floor**, as a level and a dynamic range.
4. **A comparison against prediction**, discrepancies named.
:::

:::{depth}
In detail:

1. **Two principal-plane cuts** (E-plane and H-plane), plotted in polar dB,
   normalized to the peak, with the angle convention and the frequency
   labeled on each.
2. **An extracted table** — HPBW, first sidelobe level, front-to-back ratio,
   gain, XPD — with an **uncertainty estimate on every row**. Your repeated
   sweep from step 8 is the basis for most of them.
3. **Your measured noise floor**, stated as a level and as a dynamic range,
   with one sentence per table row saying whether that number clears the floor
   and by how much.
4. **A comparison against prediction** — the aperture-formula gain, the
   $26000/(\theta_E \theta_H)$ beamwidth cross-check, and the datasheet values
   where you have them — with every discrepancy larger than your uncertainty
   named and explained.

A 2 dB gap with a named cause is a better report than a 0.2 dB gap with no
discussion.
:::
::::

::::{frame} The Range Card
:class: read-only

| At the range | What to do | Number to remember |
| :-- | :-- | :-- |
| Check geometry | all three criteria, both antennas | the reference sizes the range |
| Angle step | resolve beam *and* sidelobes | step $\le$ HPBW/5, use $2^\circ$ |
| Peak up | define the peak as $0^\circ$ | every number is measured from it |
| Noise floor | source off, record | 42 dB dynamic range on this bench |
| Normalize | dB down from the peak | never plot linear |
| HPBW | interpolate the $-3$ dB crossings | robust, trust it first |
| Gain | $G_{\text{ref}} + (P_{\text{AUT}} - P_{\text{ref}})$ | accuracy = reference + alignment |
| XPD | co-pol minus cross-pol at boresight | 20 to 30 dB is healthy |
::::

::::{frame} Practice
:class: read-only

- <a href="../../practice/ECE444_L11_Practice_blank.pdf" target="_blank" rel="noopener">Problem set (PDF)</a>
- <a href="../../practice/ECE444_L11_Practice_SOLUTIONS.pdf" target="_blank" rel="noopener">Solutions (PDF)</a>
::::

::::{frame} Where This Is Going
:::{present}
- This lab is the **dress rehearsal** for the midterm, due at Lesson 20.
- Same range, same extraction, same uncertainty discussion.
- With more antennas, a written analysis, and no procedure handed to you.
:::

Mistakes made today carry no grade penalty; the same mistakes in the graded
project do. You now have nine lessons of bench access before the project is
due, which is the reason the measurement block was pulled forward to sit here.

:::{depth}
Lessons 12 to 14 go back to antenna families — loops and monopoles, patches
and slots and horns, reflectors and Yagis — and every gain figure in them is
now a claim you know how to check. Several of those antennas are defensible
choices for your project, and you will be reading their published patterns
with a measurer's eye rather than a reader's.
:::
::::
