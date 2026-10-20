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
shows with what the array factor says. Most of the differences have a known
cause. One of them, the size of the peak step between apertures, does not yet,
and the lab records it as an open measurement.
::::

::::{frame} Beamwidth Follows the Aperture
:::{present}
$$\theta_{\text{HP}} \approx \frac{0.886\ \lambda}{Nd}, \qquad
\text{FNBW} = 2\arcsin\!\left(\frac{\lambda}{Nd}\right)$$

- Halve the active aperture $Nd$, and both beamwidths double.
- Values at $10.3\ \text{GHz}$; yours will differ.
:::
:::{present}
| Active | $Nd$ | HPBW | FNBW | First SLL |
| :-- | :-- | :-- | :-- | :-- |
| 8 | $112\ \text{mm}$ | $13.3^\circ$ | $30.1^\circ$ | $-12.8$ dB |
| 4 | $56\ \text{mm}$ | $27.4^\circ$ | $62.6^\circ$ | $-11.3$ dB |
| 2 | $28\ \text{mm}$ | $62.6^\circ$ | $180^\circ$ | none |
:::

The PHASER is an 8-element linear array with element spacing $d = 14\ \text{mm}$.
This page works its numbers at $10.3\ \text{GHz}$ as one example. There the
wavelength is $\lambda = 29.1\ \text{mm}$, so $d/\lambda = 0.481$ and the full
aperture is $Nd = 112\ \text{mm}$, just under four wavelengths. Your HB100 runs
at its own frequency, somewhere between $10.1$ and $10.7\ \text{GHz}$, so your
numbers will differ: you will press **Find HB100** at the bench, record the
Signal Freq it reports, and compute $\lambda$, $d/\lambda$, $kd$, and every
prediction at that frequency. The kit in the dry run read $10.408\ \text{GHz}$,
where $\lambda = 28.82\ \text{mm}$ and the two-element HPBW is $61.9^\circ$
rather than $62.6^\circ$.

Two results from Lesson 20 set every number you are about to measure: the
half-power beamwidth and the first-null beamwidth above. Both depend on the
array only through $Nd$, the **active aperture**. Turning off elements at the
ends of the row shortens $Nd$ without changing $d$, and that is the whole
experiment: halve the aperture, watch the beam double. The table gives the
exact array-factor solutions. The $0.886$ rule returns $13.2^\circ$ and
$26.4^\circ$ for the first two rows, within a degree of them.

The table restates Lesson 20's predictions to one decimal place, and it is the
pattern for the calculated column you will fill in at your own frequency: 8 is
E1 to E8, 4 is E3 to E6, and 2 is E4 and E5. Note
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
- Values at $10.3\ \text{GHz}$.
:::

Two entries in that table need a word of explanation before you go to the
bench. The $62.6^\circ$ at $N = 2$ does not come from the $0.886\ \lambda/(Nd)$
rule, which returns $52.8^\circ$ there. That rule carries a small-angle step
inside it, and a beam this wide violates it. For two elements the array factor
is just $\cos(\psi/2)$ with $\psi = kd\sin\theta$, so the half-power point
solves $\cos(\psi/2) = 1/\sqrt{2}$ directly: $\psi = \pi/2$, so
$\sin\theta = \lambda/4d = 0.520$ at $10.3\ \text{GHz}$ and
$\theta = 31.3^\circ$, which doubles to $62.6^\circ$.

The $180^\circ$ in the FNBW column is a convention rather than a
measurement. The first null of $\cos(\psi/2)$ needs
$\sin\theta = \lambda/2d$, which is $1.04$ at $10.3\ \text{GHz}$, and no real
angle satisfies that. The null exists in the mathematics but falls outside
visible space, so the pattern has no null anywhere you can steer, and the
beamwidth between first nulls is quoted as the full $180^\circ$ of the scan
range. The condition $\lambda/2d > 1$ holds at every frequency below
$c/2d = 10.71\ \text{GHz}$, so it holds for your HB100 too; evaluate it at your
own Signal Freq for the lab sheet.
::::

::::{frame} Reading a Sweep for What It Is
:::{present}
- Sampled: 162 points, one $2.8125^\circ$ phase step apart, about $0.9^\circ$ of angle near broadside.
- A floor about $23\ \text{dB}$ below the 8-element peak.
- Nulls read the floor, about $-23$ dBc of their trace's peak, not $-\infty$.
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
entirely. The trace has a floor. With all eight elements on, the trace stops
following the array factor about $23\ \text{dB}$ below the peak of the uniform
beam, and anything the array factor puts below that line reads as the floor
instead. The floor is not one fixed level for every trace. In the dry run the
four-element nulls filled to about $-23$ dBc of their own, lower peak, while
the two-element trace, which has no nulls, fell about $27\ \text{dB}$ from its
peak toward the edges of the scan. And the nulls are the first casualties of
both effects together: a true null is infinitely deep and infinitely narrow,
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
shrinks. The widget holds its floor $23\ \text{dB}$ below the eight-element
peak at every aperture, which leaves its two-element peak only about
$11\ \text{dB}$ above the floor. The dry-run kit's two-element trace sat about
$27\ \text{dB}$ above its floor, so read the widget's smaller apertures for how
the grid and a floor act on a pattern, not as a forecast of your bench
readings.
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
- Signal Freq from **Find HB100**; Rx Gain set for a $-10$ dBFS FFT peak.
- **2 Array Factor** under **Lab Presets**.
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

1. Browse to your kit's address from Lesson 17 and wait for the pill to read
   **Connected**.
2. With the HB100 at boresight, press **Find HB100** and record the Signal Freq
   it reports on the lab sheet.
3. Press **Calibrate** and wait for it to finish, with the HB100 still at
   boresight.
4. Press **2 Array Factor** under **Lab Presets**. Expand the section first;
   its buttons respond only while it is open.
5. Set **Rx Gain (dB)** for an FFT peak of $-10 \pm 3$ dBFS; record it.
6. Press **Start**. On the **Rectangular** tab, confirm a broadside sweep peaks
   near $0^\circ$ with a clean pair of first sidelobes.

Calibrate reads the frequency that **Find HB100** stores, which is why Find
HB100 comes before it. Your calculated columns use the same frequency: if you filled them in
before the period at a frequency more than $50\ \text{MHz}$ from the one Find
HB100 reports now, recompute them before you sweep. A change smaller than that
moves no prediction in the table by more than about $0.3^\circ$.

Step 5 is the L17 Lab's level reference, not a fixed gain. The preset does not
set **Rx Gain (dB)**, and the gain that reaches $-10$ dBFS depends on your
source, its battery, and its distance. In the dry run, $10\ \text{dB}$ drove
the peak over full scale at $1\ \text{m}$, and the L20 sweeps ran at
$1\ \text{dB}$ with the source about $1.2\ \text{m}$ out. A main lobe with a flat top on the Rectangular tab means the
receiver has clipped: turn the gain down. Leave the gain where Step 5 set it
for all three sweeps, so the three peaks compare against each other.

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
Expect it within a degree of your calculated value, about $13^\circ$. Then
find the two minima that bracket the main lobe and record the difference as
FNBW; expect about $30^\circ$. Finally read the height of the tallest sidelobe
relative to the peak, near $\pm 22^\circ$, and record it as the first SLL.
Expect $-11$ to $-14\ \text{dBc}$.

**Step A2 - Halve the aperture.** In **Element Gains**, set E1, E2, E7, and
E8 to 0, leaving E3 through E6 at 100. Before pressing anything, check your
prediction: four active elements over $56\ \text{mm}$ of aperture give about
$27^\circ$ HPBW and $62^\circ$ FNBW at your Signal Freq. The voltage sum
puts the peak $6.0\ \text{dB}$ below the eight-element peak; expect the bench
to read about $5 \pm 1\ \text{dB}$. Press **Start**, then **Freeze**. Read
the same four numbers. The main lobe is now roughly twice as wide and the
sidelobe structure has thinned out to one pair near $\pm 50^\circ$. A null
that fills to the floor reads wide: in the dry run one of the four-element
nulls filled to about $-23$ dBc and the FNBW read about $67^\circ$ against
$62.0^\circ$.

**Step A3 - Halve it again.** Set every element to 0 except E4 and E5.
Predict first: two elements over $28\ \text{mm}$ give a beam of about
$62^\circ$ and no visible null. The voltage sum puts the peak
$12.0\ \text{dB}$ below the eight-element peak; expect the bench to read
about $10 \pm 2\ \text{dB}$. Press **Start**, then **Freeze**. The trace is
now a single broad hump with no sidelobes and no null anywhere in the scan. It
falls about $27\ \text{dB}$ toward $\pm 80^\circ$, which is the two-element
array factor's own roll-off toward endfire: at $10.408\ \text{GHz}$ the array
factor reaches $-27.0\ \text{dB}$ at $90^\circ$.
::::

::::{frame} Procedure: Steps A4 and A5
:class: read-only

**Step A4 - Compare the three frozen traces.** All three are on the plot
together now. Two trends should be visible without measuring anything. The
beamwidth doubles at each halving, because $Nd$ halves and both beamwidth
formulas scale as $1/Nd$. This is the measurement to trust, and it is the one
the lab sheet grades. The peak steps down at each halving, because the elements
add in voltage at boresight: eight equal signals in phase give eight times the
voltage of one, four give four times, and the ideal steps are

$$20\log_{10}\!\left(\frac{N_{\text{active}}}{8}\right)
= -6.0\ \text{dB at } N = 4, \qquad -12.0\ \text{dB at } N = 2$$

The bench reads less than that. Expect about $5 \pm 1\ \text{dB}$ per
halving: the dry-run kit read $5.1$ and $4.8\ \text{dB}$. Record both of your
steps from the Peak Array Gain readings; Written answer 2 on the lab sheet
asks about the difference.

**Step A5 - Restore the array.** Set all eight Element Gains back to 100,
so the next lab starts from a full uniform aperture.
::::

::::{frame} What the Three Traces Show
:::{present}
- Each halving doubles the beam because $Nd$ halves. The lab grades this.
- The voltage sum predicts a $6.0\ \text{dB}$ peak step per halving.
- The dry-run kit read $5.1$ and $4.8\ \text{dB}$. The cause is still open.
:::
:::{present}
<img src="../../viz/img/L20-aperture-halving.svg"
     alt="Ideal array factors for 8, 4, and 2 active elements at 10.408 GHz, with the dry run's measured peaks: the beam doubles in width at each halving, and the peak steps 6.0 dB ideally against 5.1 and 4.8 dB measured"
     style="max-width: 560px; width: 100%; display: block; margin: 0 auto;">
:::

The figure draws the ideal array factor for each aperture at
$10.408\ \text{GHz}$, the Signal Freq of the kit in the October 2026 dry run,
and marks the three peaks that kit measured. The beam doubles at each halving
as Lesson 20 predicts, and the eight- and four-element beamwidths the kit
measured land within half a degree of the curves. The peaks do not. The voltage
sum predicts steps of $6.0$ and $6.0\ \text{dB}$; the kit read $5.1$ and
$4.8\ \text{dB}$, $9.9\ \text{dB}$ in all against $12.0$. Expect about
$5 \pm 1\ \text{dB}$ per halving on your own kit.

The cause of that shortfall is not yet known. Two explanations were tested on
the dry-run kit and ruled out. Signal leaking through the elements set to 0
accounts for at most $0.5\ \text{dB}$: with all eight gains at 0 the peak fell
$33.5\ \text{dB}$ below the full array. Receiver compression is ruled out
too: lowering every element gain from 100 to 50 lowered the signal, and the
shortfall grew, where compression would have made it shrink. The remaining candidates are
still being measured, and Written answer 2 on the lab sheet asks you to
propose one with a test that would check it.

None of this touches the shape measurements. HPBW, FNBW, and sidelobe level are
all read relative to each trace's own peak, so an error in the peak level does
not move them. The dry-run kit's numbers, against predictions computed at its
own $10.408\ \text{GHz}$:

| Active | HPBW meas / pred | FNBW meas / pred | First SLL meas / pred | Peak step meas / ideal |
| :-- | :-- | :-- | :-- | :-- |
| 8 (E1 to E8) | $13.4^\circ$ / $13.2^\circ$ | $29.8^\circ$ / $29.8^\circ$ | $-12.5$ to $-14.0$ / $-12.8$ dB | reference |
| 4 (E3 to E6) | $27.4^\circ$ / $27.1^\circ$ | about $67^\circ$ / $62.0^\circ$ | $-12$ to $-14$ / $-11.3$ dB | $-5.1$ / $-6.0$ dB |
| 2 (E4, E5) | about $56^\circ$ ($52$ to $58^\circ$) / $61.9^\circ$ | none / $180^\circ$ by convention | none | $-9.9$ / $-12.0$ dB |

The two-element HPBW is the one shape entry that does not agree. It read about
$56^\circ$, with a spread from $52$ to $58^\circ$, against $61.9^\circ$
predicted, so record it with its spread rather than as a match.
::::

::::{frame} Where the Sweep Leaves the Array Factor
:::{present}
| Feature | Array factor | Sweep reads |
| :-- | :-- | :-- |
| Floor | none | about $-23$ dBc |
| Nulls | $-\infty$ | $\approx -23$ dBc, the floor |
| FNBW, $N = 8$, $10.3\ \text{GHz}$ | $30.1^\circ$ | $30.1^\circ$ to $31.1^\circ$ |
| First SLL | $-12.8$ dB | $-11$ to $-14$ dBc |
:::

Three differences between your trace and the array factor are expected, and
each one has a number attached to it.

**The floor sits at about $-23$ dBc.** The trace stops following the array
factor about $23\ \text{dB}$ below its own peak. Every feature of the array
factor below that line — the deep parts of the nulls, and every sidelobe of a tapered
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
sample puts the measured FNBW between $30.1^\circ$ and $31.1^\circ$ at
$10.3\ \text{GHz}$, within one step of the $30.1^\circ$ the array factor
gives. The dry-run kit read $29.8^\circ$ at $10.408\ \text{GHz}$, where the
array factor gives $29.8^\circ$.

**The first sidelobe reads $-11$ to $-14$ dBc.** The array factor puts it at
$-12.8\ \text{dB}$ and $21.9^\circ$, a phase step of $64.7^\circ$. The sample
at 23 LSBs, $64.69^\circ$, catches it within a hundredth of a decibel, so grid
straddle costs nothing here, but the floor adds power to a sidelobe that is
only $10\ \text{dB}$ above it and noise
moves the reading a few tenths either way from sweep to sweep. The two first
sidelobes need not match each other either: the dry-run kit read
$-12.5$ dBc on one side and $-14.0$ dBc on the other. A single number is not
meaningful at this dynamic range; a range is.

The half-power readings get less certain as the aperture shrinks. At eight
and four elements the dry-run kit's HPBW landed within half a degree of the
array factor. At two elements it read about $56^\circ$, between $52$ and
$58^\circ$, against $61.9^\circ$. The two-element pattern is flat near its
half-power points: at $10.408\ \text{GHz}$ it falls only about
$0.2\ \text{dB}$ per degree there, against about $1\ \text{dB}$ per degree
for eight elements. An error of $0.6\ \text{dB}$ in the level you read the
$-3\ \text{dB}$ crossings against moves each crossing about $3^\circ$, and
the HPBW twice that. Report the two-element HPBW with its spread, and expect
agreement within several degrees, not within one.

<img src="../../viz/img/L20-ideal-vs-measured.svg"
     alt="The ideal eight-element array factor under the same sweep as the measurement: the sampled trace, its noise floor, and the filled nulls"
     style="max-width: 700px; width: 100%; display: block; margin: 1em auto;">
::::

::::{frame} Worked Example: A Six-Element Aperture
:class: read-only

:::{admonition} Worked example — predicting a six-element aperture
:class: tip
Suppose you turn off only E1 and E8, leaving six elements over
$Nd = 6 \times 14 = 84\ \text{mm}$. Work it at $10.3\ \text{GHz}$, where
$\lambda = 29.1\ \text{mm}$; at the bench you would use your own Signal Freq.
The beamwidth scales as $1/Nd$, so from the eight-element value,

$$\theta_{\text{HP}} \approx 13.3^\circ \times \frac{112}{84} = 17.7^\circ$$

and the first-null beamwidth is
$2\arcsin(29.1/84) = 2 \times 20.27^\circ = 40.5^\circ$. Solving the
six-element array factor directly gives $17.9^\circ$ for the HPBW. The
voltage sum puts the peak $20\log_{10}(6/8) = -2.5\ \text{dB}$ below the
eight-element peak, and the bench will most likely read a smaller drop, as in
Step A4. The predicted HPBW spans about 19 sweep steps, so the measurement has
enough resolution to confirm it, and you should expect a reading within a
degree or two of $17.9^\circ$.
:::
::::

::::{frame} No Hardware?
:class: read-only

```{note}
Run `python phaser_headless.py --sim` and open the same URL. The lab reproduces
step for step in simulation, because the simulated source already sits at
boresight and nothing in the procedure requires moving it. Its Signal Freq is
$10.525\ \text{GHz}$, so compute the calculated columns there. The sim's
sweep reads $13.1^\circ$, $29.1^\circ$, and $65.4^\circ$ for the three
apertures. It adds the element signals exactly in voltage, so its peak steps
come out at the ideal $6.0\ \text{dB}$ rather than the bench's $5\ \text{dB}$,
and it does not model **Rx Gain (dB)**. Record those as your measured column
and reconcile them against the calculated column exactly as you would on the
bench.
```
::::

::::{frame} Deliverables
:class: read-only

Submit the L20 Lab sheet, one per cadet, at the start of the next period.

1. **Your kit's settings.** The Signal Freq that **Find HB100** reported and
   the Rx Gain (dB) you set at bring-up, with $\lambda$, $d/\lambda$, and
   $kd$ at that Signal Freq.
2. **The measurement table.** One row per aperture, with the calculated
   columns, at your Signal Freq, filled in before you measured and the
   measured columns filled in at the bench.

   | Active elements | Peak (dBFS) | Step from 8 (dB) | HPBW meas | HPBW calc | FNBW meas | FNBW calc | First SLL |
   | :-- | :-- | :-- | :-- | :-- | :-- | :-- | :-- |
   | 8 (E1 to E8) | | reference | | | | | |
   | 4 (E3 to E6) | | | | | | | |
   | 2 (E4, E5) | | | | | | $180^\circ$ | none |

3. **Written answer 1.** Explain why the first-null beamwidth of the two-element
   array is quoted as $180^\circ$ rather than measured. Name the condition on
   $\lambda/2d$ that decides whether a null exists in visible space, and
   evaluate it for $d = 14\ \text{mm}$ at your Signal Freq.
4. **Written answer 2.** The voltage sum predicts a peak step of
   $6.0\ \text{dB}$ per halving. Compare your two measured steps with it.
   Leakage through the elements set to 0 and receiver compression were ruled
   out on the dry-run kit; propose one other possible cause of a shortfall, and
   describe a measurement on your kit that would test it.
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
| $\theta_{\text{HP}} \approx 0.886\ \lambda/Nd$ | half-power beamwidth, broadside | $13.3^\circ$, $27.4^\circ$, $62.6^\circ$ for $N = 8, 4, 2$ at $10.3\ \text{GHz}$, solved exactly; the rule fails at $N = 2$ |
| $\text{FNBW} = 2\arcsin(\lambda/Nd)$ | first-null beamwidth | $30.1^\circ$ at $N = 8$, $10.3\ \text{GHz}$; no null when $\lambda/2d > 1$, below $10.71\ \text{GHz}$ |
| First SLL, uniform | set by distribution shape, not size | $-12.8$ dB at $N = 8$, $-11.3$ dB at $N = 4$; measured $-11$ to $-14$ dBc |
| $20\log_{10}(N_{\text{active}}/8)$ | ideal peak drop from the coherent voltage sum | $-6.0$ dB per halving; the bench reads about $5 \pm 1$ dB, cause open |
| Sweep grid | one ADAR1000 phase LSB per point | $2.8125^\circ$ of phase, $0.93^\circ$ of angle at broadside at $10.3\ \text{GHz}$; 162 points |
| Dynamic range | a trace's peak above its floor | $\approx 23$ dB; nulls read the floor, $\approx -23$ dBc |
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
