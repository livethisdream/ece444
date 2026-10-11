---
frame_view: true
---

# L23 - Array Factor and Pattern Lab

::::{frame}
:class: title-frame

<div class="course-mark">ECE 444 · Fall 2026</div>

<h1 class="frame-title">Array Factor and Pattern Lab</h1>

<div class="title-rule"></div>

Sweep the beam past the source, then walk the source past the beam.

Lesson 23 · Antennas, Phased Arrays, and Radar Systems · Dr. Neil Rogers
::::

::::{frame} Slides
:class: read-only

:::{admonition} Slides
:class: slides
<a href="../../slides/L23-array-pattern-lab.html" target="_blank" rel="noopener">html slides</a>
<a href="../../slides/L23-array-pattern-lab.html?print-pdf" target="_blank" rel="noopener">pdf slides</a>
<a href="../../slides/L23-array-pattern-lab.md" target="_blank" rel="noopener">raw markdown slides</a>
:::
::::

::::{frame} Learning Objectives

<ol class="lo-list" style="--module: '3'; counter-reset: lo 1">
  <li>I can derive the array factor for an arbitrary linear array and apply pattern multiplication.</li>
</ol>
<ol class="lo-list" style="--module: '3'; counter-reset: lo 5">
  <li>I can distinguish between array factor and true antenna pattern and account for element pattern effects.</li>
</ol>
::::

::::{frame} One Bench, Two Experiments
:::{present}
- **Part A:** sweep the beam past a fixed source at 8, 4, and 2 active elements.
- **Part B:** hold the beam, walk the source around it, broadside then $30^\circ$.
- One kit, one setup, one Lab 7 sheet.
:::

Lesson 21 ended with a table of predictions: what the PHASER's beam should
look like at eight, four, and two active elements. Lesson 22 then separated
the array factor from the pattern the array radiates, and predicted three
places where the two part company: the peak sags as $\cos\theta_0$ when you
steer, the sidelobes on either side of a steered beam stop matching each
other, and nothing comes out the back. Today both go to the bench, in two
parts that share one setup.

In **Part A** you sweep the array three times, shrinking the active aperture
by half between sweeps, and read the half-power beamwidth, the first-null
beamwidth, and the first sidelobe level off each trace. The predictions are
already written down, so the work is the third step: reconciling what the plot
shows with what the array factor says, and naming the reason for every
difference. In **Part B** the technique changes: the beam stays where you put
it and the source moves, and by the end of the period you will have a pattern
trace with real physical angles on it, plus the limits of a hand-held
measurement.
::::

::::{frame} Part A: Beamwidth Follows the Aperture
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
distribution, which stays uniform throughout Part A, so the sidelobe moves
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
<img src="../../viz/img/L23-read-the-trace.svg"
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

::::{frame} Part B: Two Ways to Trace a Pattern
:::{present}
| | Sweep the beam | Move the source |
| :-- | :-- | :-- |
| x-axis | steer angle | elapsed time |
| Measures | array factor | element $\times$ array factor |
| Behind the array | never visited | visibly empty |
:::
:::{present}
<img src="../../viz/img/L23-two-methods.svg"
     alt="Left: the beam sweeps electronically past a stationary HB100. Right: the beam is held fixed while the HB100 is carried around the array on a 1 m arc."
     style="max-width: 560px; width: 100%; display: block; margin: 0 auto;">
:::

There are two ways to get a pattern out of an array, and they are not the same
measurement.

The first way is the one you have used in every lab since Lesson 19, and in
Part A. Put a source somewhere and leave it there, then **sweep the beam**
electronically past it, recording received power at each commanded steer
angle. That is what the Rectangular tab's Start button does. The trace it
paints is close to the array factor, plotted against the angle you *asked* the
beamformer for.

The second way is what an antenna range does. **Hold the beam fixed** and carry
the source around the array on an arc, recording received power as it goes. The
trace this paints is the full radiated pattern — element factor and array factor
together — plotted against a physical angle you can point at in the room. You have
done this once before: the midterm project measured a single antenna's pattern by
moving a source around it, and Part B applies the same idea to a beam you are
steering electronically.

| | Sweep the beam | Move the source |
| :-- | :-- | :-- |
| x-axis | commanded steer angle | elapsed time (angle is where your hand was) |
| What is measured | mostly the array factor | element factor $\times$ array factor |
| Element factor | fixed, so it cancels out | included, and it shades the trace |
| Angle accuracy | set by the $2.8125^\circ$ phase LSB, about $0.9^\circ$ near broadside | set by how steadily you walk |
| Behind the array | never visited | visibly empty |

Sweeping the beam holds the source at one physical angle, so the element factor
contributes the same constant to every point on the trace and drops out of the
shape. Moving the source changes the physical angle at every instant, so the
element pattern rides on top of the array factor exactly as Lesson 22 described.
::::

::::{frame} What Lesson 22 Says You Will See
:::{present}
:class: callout
- **Scan loss:** a $30^\circ$ beam peaks $0.6\ \text{dB}$ below broadside.
- **Sidelobe asymmetry:** the inner first sidelobe sits higher than the outer.
- **No back radiation:** the trace dies toward $\pm 90^\circ$.
:::

Three differences, all of them measurable this period. **Scan loss**: with the beam
at $30^\circ$ the peak reads about $0.6\ \text{dB}$ below the broadside peak,
because the projected aperture shrinks as $\cos\theta_0$. **Sidelobe asymmetry**:
the first sidelobe on the inside of a steered beam sits higher than the one on the
outside, because the element factor falls off faster at large angles. **No back
radiation**: the trace dies away toward $\pm 90^\circ$ and there is nothing behind
the array, because the patch elements radiate into the forward hemisphere only.
::::

::::{frame} Equipment and Setup
:::{present}
- The kit on its stand, calibrated; the HB100 at boresight, $1\ \text{m}$ out, at patch-row height.
- Part A: **Lab preset 2 (Array Factor)**.
- Part B: **Lab Preset 7 (Antenna Pattern)**, and a taped $1\ \text{m}$ arc.
:::

Per bench:

- ADALM-PHASER (CN0566) with its ADALM-Pluto, on its stand, with its 5 V supply
  and network connection.
- HB100 Doppler module with a fresh battery, on a tripod for Part A and on a
  handheld mount for Part B.
- A camera tripod or a length of string cut to $1\ \text{m}$, used as a radius gauge.
- A laptop with a browser pointed at `http://phaser.local:8080`.
- Masking tape to mark the arc on the floor.

Place the HB100 at boresight, about $1\ \text{m}$ from the face of the array, at
the same height as the patch row and with its face square to the array.
Boresight placement matters more than distance in Part A: every prediction
there is a broadside number, and a source offset by a few degrees shifts the
whole trace along the angle axis.

Mark the arc before you touch the hardware for Part B. Measure $1\ \text{m}$ from
the face of the array, tape a mark on the floor at $-90^\circ$, $0^\circ$, and
$+90^\circ$, and add marks every $30^\circ$ if you have time. Lesson 22 put the
far-field boundary of this aperture at $0.66\ \text{m}$, so a $1\ \text{m}$ radius
is far enough out that the pattern has settled, and walking it consistently is
what makes the amplitudes comparable from run to run.
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
between sweeps does not affect this lab. Moving the source does in Part A,
because all three traces are compared against each other at the end.
```
::::

::::{frame} Part A Procedure: Steps A1 to A3
:class: read-only

Each step names the control you touch and the observation you should get. Fill
the Part A table on the lab sheet as you go, and predict before you measure at
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

::::{frame} Part A Procedure: Steps A4 and A5
:class: read-only

**Step A4 - Compare the three frozen traces.** All three are on the plot
together now. Two trends should be visible without measuring anything. The
beamwidth doubles at each halving, because $Nd$ halves and both beamwidth
formulas scale as $1/Nd$. The peak steps down by about $6\ \text{dB}$ at each
halving, because the elements add in voltage at boresight: eight equal signals
in phase give eight times the voltage of one, four give four times, and

$$20\log_{10}\!\left(\frac{N_{\text{active}}}{8}\right)
= -6.0\ \text{dB at } N = 4, \qquad -12.0\ \text{dB at } N = 2$$

**Step A5 - Restore the array.** Set all eight Element Gains back to 100.
Part B starts from a full uniform aperture.
::::

::::{frame} Part A: What the Three Traces Show
:::{present}
- Each halving doubles the beam: $Nd$ halves.
- Each halving drops the peak about $6\ \text{dB}$: the elements add in voltage.
- The steps read $5.7$ and $5.3\ \text{dB}$: noise lifts the smaller peaks.
:::
:::{present}
<img src="../../viz/img/L23-aperture-halving.svg"
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

::::{frame} Part A: Where the Sweep Leaves the Array Factor
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

<img src="../../viz/img/L23-ideal-vs-measured.svg"
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

::::{frame} Part B Procedure: The Broadside Walk
:class: read-only

Load **Lab Preset 7 (Antenna Pattern)** from the Lab Presets section. The
preset does one thing you have not seen before: it puts the GUI in **Signal vs
Time** mode on the **Tracking** tab. In this mode the plot streams received
amplitude against wall-clock time rather than against steering angle. The
beamformer stops sweeping and holds whatever Steer Angle you have applied, so
the only thing that changes the received amplitude is where the source is.

**Step B1 - The broadside run.** Set **Steer Angle** to $0$ in the Beam
Steering section and press **Apply**. Stand at the $-90^\circ$ mark holding the
HB100 aimed at the array, start the Tracking plot, and walk smoothly around the
arc to $+90^\circ$, keeping the module pointed at the array the whole way and
keeping the radius at $1\ \text{m}$. Take about seven or eight seconds for the
walk. The amplitude trace paints the pattern as you go.

Practice the walk before recording. A walk that is too fast crams the whole
pattern into the left quarter of the plot, and one that is too slow runs off
the right edge before you reach $+90^\circ$. Practice until one full rotation
spans the plot with the main lobe somewhere near the middle, then record that
run.

**Step B2 - Read the lobe structure.** Freeze the trace and read it. The
amplitudes are trustworthy and the angles are not, because the x-axis is time
and your hand speed was not uniform. A stretch of the walk where you slowed
down spreads a lobe wider on the plot; a stretch where you hurried squeezes one
narrower. Neither changes how tall the lobe is. Record three numbers as
amplitudes relative to the main-lobe peak, in dBc: the main lobe itself, which
is $0$ dBc by definition, and the first sidelobe on each side of it. The
uniform 8-element array puts its first sidelobes at $-13$ dBc, and a
hand-walked trace in a classroom should land within a decibel or two of that.
::::

::::{frame} The Trace Paints as You Walk
:class: viz-frame

:::{depth}
The widget below runs the same walk in simulation. Choose a steer angle and a
rotation speed profile, then watch the trace paint as the source moves around the
arc. Run it once with the uniform profile and once with the hand-like profile, and
compare the two pill readouts: the lobe spacing changes completely and the lobe
amplitudes do not move at all. That is the result the rest of Part B depends on.
:::

:::{present}
<iframe src="../../viz/pattern-measurement-sim.html"
        width="100%" height="459"
        style="border: 1px solid #cddce9; border-radius: 6px;"
        loading="lazy"
        title="Simulated hand-rotation pattern measurement: a source walks an arc around a fixed beam while the amplitude-versus-time trace paints below">
</iframe>
:::
::::

::::{frame} Amplitudes Survive, Angles Do Not
:::{present}
- The x-axis is time: an uneven walk moves and stretches the lobes.
- It cannot change their height, so report lobes in dBc.
:::
:::{present}
<img src="../../viz/img/L23-time-vs-angle.svg"
     alt="The same measured run plotted twice: against elapsed time, where the lobes are unevenly spaced, and against true source angle, where they are symmetric. The lobe amplitudes are identical on both."
     style="max-width: 560px; width: 100%; display: block; margin: 0 auto;">
:::
::::

::::{frame} Part B Procedure: Steer, Then Sweep
:class: read-only

**Step B3 - Steer the beam and walk it again.** Set **Steer Angle** to $30$ and
press **Apply**. Walk the same arc at the same radius and record a second trace.
Three things change, and the next frame shows them.

**Step B4 - Compare against an electrical sweep.** Put the HB100 back on the
$0^\circ$ mark and leave it there. Set Steer Angle back to $0$, switch to the
**Rectangular** tab, and press **Start** to run a normal beam sweep. Do not
move the source for this one.

Put the two traces side by side. The lobe amplitudes agree: the first sidelobes
measure $-11$ to $-13$ dBc on the sweep, the same window your walk produced. The
x-axes do not mean the same thing. The sweep's axis is the commanded steer angle,
sampled on a grid set by the $2.8125^\circ$ phase LSB, and it is calibrated
because the beamformer knows exactly what it commanded. Your walk's axis is time,
and it is calibrated by nothing.
::::

::::{frame} Part B: The Steered Walk
:::{present}
- The main lobe arrives near $30^\circ$: you walked into the steered beam.
- Scan loss, $0.6\ \text{dB}$, against $\pm 0.5\ \text{dB}$ of hand wobble.
- Inner sidelobe $-12.2$ dBc, outer $-15.2$ dBc.
:::
:::{present}
<img src="../../viz/img/L23-steer-compare.svg"
     alt="Broadside and 30-degree steered patterns on a true-angle axis, showing the 0.6 dB scan loss and the unequal first sidelobes of the steered beam."
     style="max-width: 560px; width: 100%; display: block; margin: 0 auto;">
:::

The main lobe now appears when you cross about $30^\circ$ instead of at boresight,
which is the most direct confirmation of beam steering you will get all semester:
the beam is pointing where the phases say it should, and you found it by walking
into it.

The peak reads lower than the broadside run. Theory says $0.6\ \text{dB}$ lower.
Your hand wobble is worth roughly $\pm 0.5\ \text{dB}$ on its own, so a single pair
of runs will not resolve a $0.6\ \text{dB}$ difference. Record what you measure,
state the uncertainty next to it, and say whether the two runs are distinguishable.
Averaging three runs at each steer angle tightens this enough to be worth the extra
five minutes.

The pattern is no longer symmetric. The first sidelobe on the inside of the beam,
near $+8^\circ$, sits about $-12.2$ dBc; the one on the outside, near $+59^\circ$,
sits about $-15.2$ dBc. The array factor alone would have made them equal, and the
element factor is what pulls the outer one down.
::::

::::{frame} Worked Example: Reading dBc off a Raw Trace
:class: read-only

:::{admonition} Worked example — reading dBc off a raw trace
:class: tip
A Tracking-tab run gives peak amplitudes of $-18.4$ dBFS for the main lobe,
$-31.2$ dBFS for the left first sidelobe, and $-29.9$ dBFS for the right first
sidelobe. The full-scale reference cancels when you take the ratio, so subtract:

$$-31.2 - (-18.4) = -12.8\ \text{dBc} \qquad -29.9 - (-18.4) = -11.5\ \text{dBc}$$

Both straddle the $-13$ dBc value for a uniform 8-element array, and the
$1.3\ \text{dB}$ spread between them is about what a classroom's multipath ripple
produces. A pair reading $-12.8$ and $-11.5$ dBc is a uniform illumination measured
in a room. A pair reading $-6$ and $-7$ dBc would not be, and would send you back to
Calibrate and to the element gain sliders.
:::
::::

::::{frame} Part B: Expectation Table
:::{present}
| Quantity | Calculated | Electrical sweep |
| :-- | :-- | :-- |
| First sidelobes, broadside | $-13.1$ dBc | $-11$ to $-13$ dBc |
| Peak, beam at $30^\circ$ | $-0.6$ dB | $-0.6$ dB |
| Inner, outer sidelobe at $30^\circ$ | $-12.2$, $-15.2$ dBc | below the floor |
:::

The lab sheet's Part B table adds a mechanical column, filled from your walks,
beside these two:

| Quantity | Calculated | Mechanical (measured) | Electrical sweep (measured) |
| :-- | :-- | :-- | :-- |
| First sidelobe, left | $-13.1$ dBc | | $-11$ to $-13$ dBc |
| First sidelobe, right | $-13.1$ dBc | | $-11$ to $-13$ dBc |
| Peak, beam at $30^\circ$ | $-0.6$ dB | | $-0.6$ dB |
| Inner sidelobe, beam at $30^\circ$ | $-12.2$ dBc | | below the sweep's floor |
| Outer sidelobe, beam at $30^\circ$ | $-15.2$ dBc | | below the sweep's floor |

The calculated $-13.1$ dBc is the $-12.8$ dB array-factor sidelobe plus about
$0.3$ dB of element-pattern roll-off at the $\pm 22^\circ$ where those sidelobes
sit. The sweep's noise floor sits about $23\ \text{dB}$ below the peak, which is
why two of the steered entries have nothing to compare against on that side of
the table.
::::

::::{frame} What the Hand Measurement Cannot Do
:::{present}
- **Angle:** time is not angle; a range uses an encoder.
- **Amplitude:** $10\ \text{cm}$ of radius is $0.8\ \text{dB}$.
- **Reflections:** $\pm 1\ \text{dB}$ of ripple; a chamber absorbs them.
- **Far field:** taped by hand, not fixed.
:::
:::{present}
<img src="../../viz/img/L23-range-artifacts.svg"
     alt="A classroom measurement with floor and ceiling reflections beside an anechoic chamber measurement with absorber-lined walls, a turntable, and a single direct path."
     style="max-width: 560px; width: 100%; display: block; margin: 0 auto;">
:::

Four things separate what you just did from a pattern measured on an antenna range,
and you have an artifact of each one sitting in your data.

**Angle calibration.** Your x-axis is time, and converting it to angle requires
assuming a constant walking speed you did not have — that is why the lobes moved
between your uniform and hand-like runs in the widget. A range mounts the antenna
on a **turntable** with a shaft **encoder**, so every recorded sample carries the
angle it was taken at to a fraction of a degree.

**Amplitude stability.** Your radius varied by whatever your arm did, and received
power goes as $1/r^2$, so a $10\ \text{cm}$ error at $1\ \text{m}$ is worth about
$0.8\ \text{dB}$ — comparable to the scan loss you were trying to measure. A range
bolts the source at a fixed distance and never moves it.

**Reflection control.** The direct path is not the only path from the HB100 to the
array. Reflections off the floor, the ceiling, and the whiteboard arrive too, and
they add to the direct signal in and out of phase as you walk, which is the source
of the $\pm 1\ \text{dB}$ ripple you saw riding on the trace. An anechoic chamber
lines every surface with absorber so only the direct path survives.

**Guaranteed far field.** You taped the arc at $1\ \text{m}$ against Lesson 22's
$0.66\ \text{m}$ criterion, held to whatever tolerance a hand-held source allows.
A range fixes the separation once, documents it, and the far-field condition is
then a documented property of the facility rather than of the operator.
::::

::::{frame} No Hardware?
:class: read-only

```{note}
Run `python phaser_headless.py --sim` and open the same URL. Part A reproduces
step for step in simulation, because the simulated source already sits at
boresight and nothing in that procedure requires moving it. The sim's sweep
reads $13.1^\circ$, $29.1^\circ$, and $65.4^\circ$ for the three apertures,
and the peak steps are the same. Record those as your measured column and
reconcile them against the calculated column exactly as you would on the
bench.

Part B has no simulation equivalent. The simulator's target is fixed at
boresight and cannot be moved, so there is no way to reproduce a walk around
the array in `--sim`. Work the electrical sweep on the Rectangular tab instead,
and use the walk widget above to see what the mechanical trace would have
looked like.
```
::::

::::{frame} Deliverables
:class: read-only

Submit the Lab 7 sheet, one per cadet, at the start of the next period.

**Part A**

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

**Part B**

4. **An annotated trace.** One screenshot of your best broadside run, with the
   main lobe and both first sidelobes labeled with their dBc values.
5. **The amplitude comparison table.** Three lobes — main lobe, left first
   sidelobe, right first sidelobe — with a mechanical column, an
   electrical-sweep column, and a calculated column filled from theory. State
   the difference between the mechanical and electrical readings for each lobe.
6. **Two written answers**, three or four sentences each:
   - Why do the lobe amplitudes survive a sloppy rotation while the lobe angles
     do not? Refer to what the time axis does and does not record.
   - Which of the four artifacts of the hand measurement does an anechoic
     chamber remove, and which of them would still be present in a chamber
     measurement?
::::

::::{frame} Lab Sheet
:class: read-only doc-links

The Lab 7 sheet is the turn-in document for both parts.

- <a class="doc-link" href="../../labs/ECE444_Lab_L23_ArrayPattern_blank.pdf" target="_blank" rel="noopener">Lab 7 sheet (PDF)</a>
::::

::::{frame} Practice
:class: read-only doc-links

- <a class="doc-link" href="../../practice/ECE444_L23_Practice_blank.pdf" target="_blank" rel="noopener">Problem set (PDF)</a>
- <a class="doc-link doc-key" href="../../practice/ECE444_L23_Practice_SOLUTIONS.pdf" target="_blank" rel="noopener">Solutions (PDF)</a>
::::

::::{frame} Summary: Part A, the Array Factor on the Bench
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

::::{frame} Summary: Part B, the Pattern by Hand
:class: read-only

| Idea | What it is | Number to remember |
| :-- | :-- | :-- |
| Beam sweep | beam swept past a fixed source | x-axis is commanded steer angle |
| Mechanical cut | source walked around a fixed beam | x-axis is time, angle is physical |
| Scan loss | projected aperture falls off as $\cos\theta_0$ | $-0.6$ dB at $30^\circ$ |
| Sidelobe asymmetry | element factor shades the outer lobe | $-12.2$ vs $-15.2$ dBc at $30^\circ$ |
| Far-field radius | $r \ge 2D^2/\lambda$ from Lesson 22 | $0.66\ \text{m}$; walk the arc at $1\ \text{m}$ |
| Classroom multipath | direct path plus room reflections | about $\pm 1\ \text{dB}$ of ripple |
| Hand wobble | radius and speed both vary | about $\pm 0.5\ \text{dB}$ on the peak |
::::

::::{frame} Looking Ahead
:::{present}
- Uniform illumination fixed the first sidelobes at $-13$ dBc today.
- Lesson 24 makes that number a design choice: taper the Element Gains.
- Lower sidelobes cost beamwidth and peak gain.
:::

You now have a measured $-13$ dBc sitting in your lab notebook, and so far it has
been a fact about uniform illumination rather than a choice. Lesson 24 turns it
into a design variable. Feeding the eight elements unequally — more power in the
middle, less at the edges — pushes the sidelobes down, and the Element Gains
sliders you have been leaving at 100% are how you do it on this hardware.

A taper that lowers the first sidelobes by $10\ \text{dB}$ widens the main lobe
and lowers the peak gain, and Lesson 24 derives exactly how much of each. Before
the next period, look back at your broadside trace and decide how much
beamwidth you would give up to put those first sidelobes at $-25$ dBc, then
check your guess against the numbers.
::::
