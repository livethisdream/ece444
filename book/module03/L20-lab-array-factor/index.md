---
frame_view: true
---

# L20 Lab — Array Factor

::::{frame}
:class: title-frame

<div class="course-mark">ECE 444 · Fall 2026</div>

<h1 class="frame-title">Array Factor</h1>

<div class="title-rule"></div>

Halve the active aperture and watch the beam double.

L20 Lab · Antennas, Phased Arrays, and Radar Systems · Dr. Neil Rogers
::::

::::{frame} Slides
:class: read-only

:::{admonition} Slides
:class: slides
<a href="../../slides/L20-lab-array-factor.html" target="_blank" rel="noopener">html slides</a>
<a href="../../slides/L20-lab-array-factor.html?print-pdf" target="_blank" rel="noopener">pdf slides</a>
<a href="../../slides/L20-lab-array-factor.md" target="_blank" rel="noopener">raw markdown slides</a>
:::
::::

::::{frame} Learning Objectives

<ol class="lo-list" style="--module: '3'; counter-reset: lo 1">
  <li>I can derive the array factor for an arbitrary linear array and apply pattern multiplication.</li>
</ol>
::::

::::{frame} Halve the Aperture, Double the Beam
:::{present}
- Sweep the beam past a fixed source at 8, 4, and 2 active elements.
- Lesson 20's table predicts every number before you measure it.
- One kit, one setup, one L20 Lab sheet.
:::

Lesson 20 ended with a table of predictions: what the PHASER's beam should
look like at eight, four, and two active elements. Today that table goes to
the bench. You sweep the array three times, shrinking the active aperture by
half between sweeps, and read the half-power beamwidth, the first-null
beamwidth, and the first sidelobe level off each trace. The predictions are
already written down, so the work is the third step: reconciling what the plot
shows with what the array factor says, and naming the reason for every
difference.
::::

::::{frame} Beamwidth Follows the Aperture
:::{present}
$$\theta_{\text{HP}} \approx \frac{0.886\ \lambda}{Nd}, \qquad
\text{FNBW} = 2\arcsin\!\left(\frac{\lambda}{Nd}\right)$$

- Halve the active aperture $Nd$, and both beamwidths double.
:::
:::{present}
| Active | $Nd$ | HPBW | FNBW | First SLL |
| :-- | :-- | :-- | :-- | :-- |
| 8 | $112\ \text{mm}$ | $13^\circ$ | $30^\circ$ | $-12.8$ dB |
| 4 | $56\ \text{mm}$ | $27^\circ$ | $62^\circ$ | $-11.3$ dB |
| 2 | $28\ \text{mm}$ | $62^\circ$ | $180^\circ$ | none |
:::

The PHASER is an 8-element linear array with element spacing $d = 14\ \text{mm}$.
At the workshop frequency of $10.3\ \text{GHz}$ the wavelength is
$\lambda = 29.1\ \text{mm}$, so $d/\lambda = 0.481$ and the full aperture is
$Nd = 112\ \text{mm}$, just under four wavelengths. Two results from Lesson 21
set every number you are about to measure: the half-power beamwidth and the
first-null beamwidth above. Both depend on the array only through $Nd$, the
**active aperture**. Turning off elements at the ends of the row shortens $Nd$
without changing $d$, and that is the whole experiment: halve the aperture,
watch the beam double.

The expectation table is Lesson 21's, restated as the prediction column you
will fill in against: 8 is Rx1-Rx8, 4 is Rx3-Rx6, and 2 is Rx4 and Rx5. Note
that the sidelobe entries are not all the same number. The familiar
$-13\ \text{dB}$ figure is the large-$N$ limit of the uniform array factor. An
8-element array lands at $-12.8\ \text{dB}$, close enough to call
$-13\ \text{dB}$, but a 4-element array reaches only $-11.3\ \text{dB}$, and a
2-element array has no sidelobe at all.

:::{callout}
Beamwidth is set by the active aperture $Nd$, not by the element count on its
own. Halving the number of active elements halves $Nd$ and doubles both
beamwidths. The sidelobe level is set by the shape of the amplitude
distribution, which stays uniform throughout this lab, so the sidelobe moves
only through the small-$N$ correction.
:::
::::

::::{frame} Two Entries That Need Care
:::{present}
$$\cos\frac{\psi}{2} = \frac{1}{\sqrt{2}} \quad\Longrightarrow\quad \sin\theta = \frac{\lambda}{4d} = 0.520 \quad\Longrightarrow\quad \text{HPBW} = 62.6^\circ$$

- At $N = 2$ the $0.886$ rule gives $53^\circ$; its small-angle step fails.
- The first null needs $\sin\theta = \lambda/2d = 1.04$: outside visible space, so FNBW is $180^\circ$.
:::

Two entries in that table need a word of explanation before you go to the
bench. The $62^\circ$ at $N = 2$ does not come from the $0.886\ \lambda/(Nd)$
rule, which returns $53^\circ$ there. That rule carries a small-angle step
inside it, and a beam this wide violates it. For two elements the array factor
is just $\cos(\psi/2)$ with $\psi = kd\sin\theta$, so the half-power point
solves $\cos(\psi/2) = 1/\sqrt{2}$ directly: $\psi = \pi/2$, so
$\sin\theta = \lambda/4d = 0.520$ and $\theta = 31.3^\circ$, which doubles to
$62.6^\circ$.

The $180^\circ$ in the FNBW column is a convention rather than a
measurement. The first null of $\cos(\psi/2)$ needs
$\sin\theta = \lambda/2d = 1.04$, and no real angle satisfies that. The null
exists in the mathematics but falls outside visible space, so the pattern has
no null anywhere you can steer, and the beamwidth between first nulls is
quoted as the full $180^\circ$ of the scan range.
::::

::::{frame} Reading a Sweep for What It Is
:::{present}
- Sampled: 162 points, one $2.8125^\circ$ phase step apart, about $0.9^\circ$ of angle near broadside.
- A floor about $23\ \text{dB}$ below the 8-element peak.
- Nulls read the floor, about $-23$ dBc, not $-\infty$.
:::
:::{present}
<img src="../../viz/img/L20-read-the-trace.svg"
     alt="One measured eight-element sweep annotated with the half-power beamwidth, the first-null beamwidth, the first sidelobe level, and the noise floor"
     style="max-width: 560px; width: 100%; display: block; margin: 0 auto;">
:::

The Rectangular tab does not plot the array factor. It plots received
power against **commanded steer angle**: the software steps the beam past a
stationary source and records the power at each step. By reciprocity that
traces the array pattern, but three properties of the measurement are baked
into every trace you will read.

The sweep is sampled, not continuous. With Use Bits on, as in every lab
preset, the software steps the element-to-element phase one ADAR1000 LSB,
$2.8125^\circ$, per point. One step moves $\sin\theta$ by
$2.8125^\circ/173.2^\circ = 0.0162$ at $10.3\ \text{GHz}$, which is
$0.93^\circ$ of angle at broadside and $1.32^\circ$ at $45^\circ$, widening as
$1/\cos\theta$. A sweep is 162 points: 123 of them span $\pm 82^\circ$, and
the other 39 ask for more phase than any real angle needs and plot at
$\pm 90^\circ$. A feature narrower than one step can fall between samples
entirely. The trace has a floor. Receiver noise sits about
$23\ \text{dB}$ below the peak of the uniform 8-element beam, which is the
usable dynamic range of the whole measurement. Anything the array factor puts
below that line reads as noise instead. And the nulls are the first casualties
of both effects together: a true null is infinitely deep and infinitely narrow,
so the grid usually misses its bottom, and even a sample that lands on it
reads the floor.
::::

::::{frame} Ideal Versus Measured
:class: viz-frame

:::{depth}
The widget below draws the array factor for each of the three apertures, then
adds those three measurement effects on a toggle. Set the aperture, read HPBW,
FNBW, and first sidelobe level off the ideal curve, then switch measurement
effects on and read the same three numbers again from the sampled trace. Watch
the FNBW pill in particular: at eight elements it holds at $30.1^\circ$ when
the grid appears, because the null sits exactly 16 phase steps out and a sample
lands on it, and at two elements it reports a dash because there is no null to
find. The HPBW pill is the one that moves, and it moves more as the aperture
shrinks.
:::

:::{present}
<iframe src="../../viz/af-measurement-compare.html"
        width="100%" height="463"
        style="border: 1px solid #cddce9; border-radius: 6px;"
        loading="lazy"
        title="Ideal array factor and measured sweep at 8, 4, and 2 active elements">
</iframe>
:::
::::

::::{frame} Equipment and Setup
:::{present}
- The kit on its stand, calibrated; the HB100 at boresight, $1\ \text{m}$ out, at patch-row height.
- **Lab preset 2 (Array Factor)**.
:::

Per bench:

- ADALM-PHASER (CN0566) with its ADALM-Pluto, on its stand, with its 5 V supply
  and network connection.
- HB100 Doppler module with a fresh battery, on a tripod.
- A laptop with a browser pointed at `http://phaser.local:8080`.

Place the HB100 at boresight, about $1\ \text{m}$ from the face of the array, at
the same height as the patch row and with its face square to the array.
Boresight placement matters more than distance in this lab: every prediction
is a broadside number, and a source offset by a few degrees shifts the
whole trace along the angle axis.
::::

::::{frame} Bring Up the Kit
:class: read-only

1. Open the GUI and confirm the Configuration section reads a Signal Freq near
   $10.5\ \text{GHz}$.
2. Run **Calibrate** once, with the HB100 at boresight.
3. Load **Lab preset 2 (Array Factor)** from the Lab Presets section.
4. On the **Rectangular** tab, confirm a broadside sweep peaks near $0^\circ$
   with a clean pair of first sidelobes.

Calibrate starts the per-element gains and phases from a matched state. An
uncalibrated array has amplitude and phase errors spread across the row, which
fills the nulls and raises the sidelobes on its own, and you would then be
measuring the calibration rather than the array factor. If the broadside sweep
does not look right, fix that before going further, because everything below
assumes a calibrated array.

The preset sets a uniform taper across all eight elements, zero steering phase,
and Use Bits on, so the sweep steps one $2.8125^\circ$ phase LSB per point, and it opens the
**Rectangular** tab in the beam-sweep plot. From here the procedure names only
the controls you change.

```{note}
The HB100 is a free-running DRO and drifts across $10.1$ to $10.7\ \text{GHz}$
with temperature. The GUI hunts for the tone, so a drift of tens of megahertz
between sweeps does not affect this lab. Moving the source does,
because all three traces are compared against each other at the end.
```
::::

::::{frame} Procedure: Steps A1 to A3
:class: read-only

Each step names the control you touch and the observation you should get. Fill
the measurement table on the lab sheet as you go, and predict before you measure at
every aperture change.

**Step A1 - Sweep the full array.** With all eight Element Gains at 100, press
**Start**. The sweep runs across $\pm 90^\circ$ and settles into a trace with a
single main lobe at $0^\circ$ and three or four sidelobe pairs on each side.
Press **Freeze** to hold it as a reference trace. Read the Peak Array Gain
readout and record it. Hover along the trace to read the angles where it falls
$3\ \text{dB}$ below the peak, and record the difference as the measured HPBW.
Expect about $13^\circ$. Then find the two minima that bracket the main lobe
and record the difference as FNBW; expect $28$ to $30^\circ$. Finally read the
height of the tallest sidelobe relative to the peak, near $\pm 22^\circ$, and
record it as the first SLL. Expect $-11$ to $-13\ \text{dBc}$.

**Step A2 - Halve the aperture.** In **Element Gains**, set Rx1, Rx2, Rx7, and
Rx8 to 0, leaving Rx3 through Rx6 at 100. Before pressing anything, write down
your prediction: four active elements over $56\ \text{mm}$ of aperture give
$27^\circ$ HPBW and $62^\circ$ FNBW, and the peak should sit about
$6\ \text{dB}$ below the eight-element peak. Press **Start**, then **Freeze**.
Read the same four numbers. The main lobe is now roughly twice as wide and the
sidelobe structure has thinned out to one pair near $\pm 50^\circ$.

**Step A3 - Halve it again.** Set every element to 0 except Rx4 and Rx5.
Predict first: two elements over $28\ \text{mm}$ give a $62^\circ$ beam, no
visible null, and a peak about $12\ \text{dB}$ below the eight-element peak.
Press **Start**, then **Freeze**. The trace is now a single broad hump with no
sidelobes and no null anywhere in the scan. It flattens into the noise well
before $\pm 90^\circ$: the two-element pattern falls only about
$24\ \text{dB}$ from its own peak at endfire, but the floor sits just
$11\ \text{dB}$ below that peak, so the outer half of the roll-off is buried.
::::

::::{frame} Procedure: Steps A4 and A5
:class: read-only

**Step A4 - Compare the three frozen traces.** All three are on the plot
together now. Two trends should be visible without measuring anything. The
beamwidth doubles at each halving, because $Nd$ halves and both beamwidth
formulas scale as $1/Nd$. The peak steps down by about $6\ \text{dB}$ at each
halving, because the elements add in voltage at boresight: eight equal signals
in phase give eight times the voltage of one, four give four times, and

$$20\log_{10}\!\left(\frac{N_{\text{active}}}{8}\right)
= -6.0\ \text{dB at } N = 4, \qquad -12.0\ \text{dB at } N = 2$$

**Step A5 - Restore the array.** Set all eight Element Gains back to 100,
so the next lab starts from a full uniform aperture.
::::

::::{frame} What the Three Traces Show
:::{present}
- Each halving doubles the beam: $Nd$ halves.
- Each halving drops the peak about $6\ \text{dB}$: the elements add in voltage.
- The steps read $5.7$ and $5.3\ \text{dB}$: noise lifts the smaller peaks.
:::
:::{present}
<img src="../../viz/img/L20-aperture-halving.svg"
     alt="Measured sweeps at 8, 4, and 2 active elements on one axis: the beam doubles in width and the peak steps down about 6 dB at each halving"
     style="max-width: 560px; width: 100%; display: block; margin: 0 auto;">
:::

The figure shows the first step at $5.7\ \text{dB}$ and the second at
$5.3\ \text{dB}$, and your plot will fall short of $6\ \text{dB}$ the same way.
The shortfall comes from the noise. By the time only two elements are on, the
peak sits about $11\ \text{dB}$ above the floor, and the power the receiver
reports at the peak is the sum of signal power and noise power. Adding a floor
that is $11\ \text{dB}$ down lifts the reading by roughly $0.3\ \text{dB}$.
The rest comes from reading the highest sample: across a peak this broad, dozens
of samples sit within a few tenths of a decibel of the top, and the noise on
the highest of them lifts the reading further, by about $0.7\ \text{dB}$ more
in the figure.
::::

::::{frame} Where the Sweep Leaves the Array Factor
:::{present}
| Feature | Array factor | Sweep reads |
| :-- | :-- | :-- |
| Floor | none | $-23$ dBc |
| Nulls | $-\infty$ | $\approx -23$ dBc, the floor |
| FNBW, $N = 8$ | $30.1^\circ$ | $30.1^\circ$ to $31.1^\circ$ |
| First SLL | $-12.8$ dB | $-11$ to $-13$ dBc |
:::

Three differences between your trace and the array factor are expected, and
each one has a number attached to it.

**The floor sits at about $-23$ dBc.** Receiver and quantization noise put a
hard limit on how far down the plot can see. Every feature of the array factor
below that line — the deep parts of the nulls, and every sidelobe of a tapered
array — reads as noise instead of as pattern. This is the usable dynamic range
of the measurement, and it is why the lab asks for the first sidelobe rather
than the second or third.

**Nulls read about $-23$ dBc instead of $-\infty$.** Two effects fill them, and
it is worth keeping them separate. Grid straddle is the smaller one. The
8-element null sits at a phase step of $360^\circ/8 = 45^\circ$, exactly 16
LSBs, so with the source on boresight a sample lands on it at $15.1^\circ$. A
source half a step off boresight, $0.47^\circ$, leaves the nearest sample at
$-30\ \text{dB}$, still below the floor. The floor is what fills the null: it
adds its own power to every sample near it. Reading each null at its lowest
sample puts the measured FNBW between $30.1^\circ$ and $31.1^\circ$, within
one step of the $30.1^\circ$ the array factor gives.

**The first sidelobe reads $-11$ to $-13$ dBc.** The array factor puts it at
$-12.8\ \text{dB}$ and $21.9^\circ$, a phase step of $64.7^\circ$. The sample
at 23 LSBs, $64.69^\circ$, catches it within a hundredth of a decibel, so grid
straddle costs nothing here, but the floor adds power to a sidelobe that is
only $10\ \text{dB}$ above it and noise
moves the reading a few tenths either way from sweep to sweep. A single number
is not meaningful at this dynamic range; a range is.

Notice how these three effects grow as the aperture shrinks. At eight elements
the measured HPBW lands within a tenth of a degree of theory. At four elements
the peak is $6\ \text{dB}$ closer to the floor and the reading comes out
$26.1^\circ$ against $27.4^\circ$. At two elements the peak is
$12\ \text{dB}$ closer and the reading comes out $50.6^\circ$ against
$62.6^\circ$, narrow by $12^\circ$: the two-element pattern is so flat near
its half-power points that a few tenths of a decibel of noise on the peak
sample moves each $-3$ dB crossing by several degrees. Every one of those
errors is a consequence of the shrinking gap between the trace and the noise
floor.

<img src="../../viz/img/L20-ideal-vs-measured.svg"
     alt="The ideal eight-element array factor under the same sweep as the measurement: the sampled trace, its noise floor, and the filled nulls"
     style="max-width: 700px; width: 100%; display: block; margin: 1em auto;">
::::

::::{frame} Worked Example: A Six-Element Aperture
:class: read-only

:::{admonition} Worked example — predicting a six-element aperture
:class: tip
Suppose you turn off only Rx1 and Rx8, leaving six elements over
$Nd = 6 \times 14 = 84\ \text{mm}$. The beamwidth scales as $1/Nd$, so from the
eight-element measurement,

$$\theta_{\text{HP}} \approx 13.2^\circ \times \frac{112}{84} = 17.6^\circ$$

and the first-null beamwidth is
$2\arcsin(29.1/84) = 2 \times 20.3^\circ = 40.6^\circ$. The peak falls by
$20\log_{10}(6/8) = -2.5\ \text{dB}$. The predicted HPBW is about six sweep
steps wide, so the measurement has enough resolution to confirm it, and you
should expect a reading within a degree or two of $17.6^\circ$.
:::
::::

::::{frame} No Hardware?
:class: read-only

```{note}
Run `python phaser_headless.py --sim` and open the same URL. The lab reproduces
step for step in simulation, because the simulated source already sits at
boresight and nothing in the procedure requires moving it. The sim's sweep
reads $13.1^\circ$, $29.1^\circ$, and $65.4^\circ$ for the three apertures,
and the peak steps are the same. Record those as your measured column and
reconcile them against the calculated column exactly as you would on the
bench.
```
::::

::::{frame} Deliverables
:class: read-only

Submit the L20 Lab sheet, one per cadet, at the start of the next period.

1. **The measurement table.** One row per aperture, with the calculated columns
   filled in before you measured and the measured columns filled in at the
   bench.

   | Active elements | Peak (dBFS) | HPBW meas | HPBW calc | FNBW meas | FNBW calc | First SLL |
   | :-- | :-- | :-- | :-- | :-- | :-- | :-- |
   | 8 (Rx1-Rx8) | | | $13^\circ$ | | $30^\circ$ | |
   | 4 (Rx3-Rx6) | | | $27^\circ$ | | $62^\circ$ | |
   | 2 (Rx4, Rx5) | | | $62^\circ$ | | $180^\circ$ | |

2. **Written answer.** Explain why the first-null beamwidth of the two-element
   array is quoted as $180^\circ$ rather than measured. Name the condition on
   $\lambda/2d$ that decides whether a null exists in visible space, and
   evaluate it for $d = 14\ \text{mm}$ at $10.3\ \text{GHz}$.
3. **Written answer.** The gain of each individual patch element is the same
   whether the other seven elements are on or off, and the amplifier behind
   each element is unchanged. Explain why the peak of the sweep nonetheless
   drops by about $6\ \text{dB}$ every time you halve the number of active
   elements.
::::

::::{frame} Lab Sheet
:class: read-only doc-links

The L20 Lab sheet is the turn-in document.

- <a class="doc-link" href="../../labs/ECE444_Lab_L20_ArrayFactor_blank.pdf" target="_blank" rel="noopener">L20 Lab sheet (PDF)</a>
::::

::::{frame} Practice
:class: read-only doc-links

- <a class="doc-link" href="../../practice/ECE444_L20Lab_Practice_blank.pdf" target="_blank" rel="noopener">Problem set (PDF)</a>
- <a class="doc-link doc-key" href="../../practice/ECE444_L20Lab_Practice_SOLUTIONS.pdf" target="_blank" rel="noopener">Solutions (PDF)</a>
::::

::::{frame} Summary: The Array Factor on the Bench
:class: read-only

| Symbol / idea | What it is | Number to remember |
| :-- | :-- | :-- |
| $Nd$ | active aperture; sets both beamwidths | $112\ \text{mm}$ at $N = 8$, $d = 14\ \text{mm}$ |
| $\theta_{\text{HP}} \approx 0.886\ \lambda/Nd$ | half-power beamwidth, broadside | $13^\circ$, $27^\circ$, $62^\circ$ for $N = 8, 4, 2$ |
| $\text{FNBW} = 2\arcsin(\lambda/Nd)$ | first-null beamwidth | $30^\circ$ at $N = 8$; no null when $\lambda/2d > 1$ |
| First SLL, uniform | set by distribution shape, not size | $-12.8$ dB at $N = 8$, $-11.3$ dB at $N = 4$; measured $-11$ to $-13$ dBc |
| $20\log_{10}(N_{\text{active}}/8)$ | peak drop from coherent voltage sum | $-6$ dB per halving of the aperture |
| Sweep grid | one ADAR1000 phase LSB per point | $2.8125^\circ$ of phase, $0.93^\circ$ of angle at broadside; 162 points |
| Dynamic range | peak of uniform beam above noise | $\approx 23$ dB; nulls read the floor, $\approx -23$ dBc |
::::

::::{frame} Looking Ahead
:::{present}
- Today's traces are the array factor, read against a commanded angle.
- Lesson 21 adds the element pattern: what the patches do to the beam.
- The L21 Lab holds the beam still and walks the source around it.
:::

Every trace you took today plots received power against the angle you asked
the beamformer for, with the source fixed, so the element pattern contributed
the same constant to every point and dropped out of the shape. Lesson 21 puts
it back: the patches have their own pattern, and the array radiates the element
pattern times the array factor. Keep your three frozen traces. The L21 Lab
measures the full pattern by moving the source instead of the beam, and the
far edges of today's eight-element trace are where the two part company.
::::
