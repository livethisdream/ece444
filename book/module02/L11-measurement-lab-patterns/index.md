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
antenna. Today you walk into the chamber and ask where that power *goes*. You
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
- Scan two principal planes from the dashboard, then a cross-pol cut.
- Swap in the reference horn for gain.
- Measure your own floor and quote it against everything.
:::

Reciprocity means it does not matter which end transmits, so the source horn
transmits and the antenna under test receives — the AUT is the thing that
rotates, and you would rather not run transmit power through a rotary joint.

:::{depth}
One instrument does both ends today. The chamber's Copper Mountain VNA drives
the source horn from port 1 and receives the AUT on port 2, so the quantity
you record at every angle is $S_{21}$ in dB: transmitted at one antenna,
received at the other, ratioed against the source so the source's own drift
divides out. That is the same argument Lesson 9 made for trusting a ratioed
measurement, now doing work on the range rather than at the connector.
:::
::::

::::{frame} The Chain and Its Failure Modes
:::{present}
| Stage | Must do | Goes wrong as |
| :-- | :-- | :-- |
| VNA port 1 | one stable sweep | a changed setting reads as pattern |
| Source horn | clean polarization | leaks into your cross-pol |
| Turntable | one centered axis | biased HPBW |
| VNA port 2 | $S_{21}$ per angle | unrecorded settings |
:::

The rig is fixed today, which removes a variable Lesson 9 left open: there is
one chain, it is cabled, and it is the same one every section uses. What is
left to you is the discipline — the settings you choose, the zero you define,
and whether you wrote any of it down.

:::{depth}
The chain is a loop rather than a line. The VNA is both the transmitter and
the receiver, the two horns are the only things between its ports, and the
positioner is a serial link the acquisition software drives in step with the
sweep. Nothing in the chain is free-running: every angle is *commanded*, then
*confirmed*, then measured. That is what makes the run file trustworthy, and
it is why the file records both the angle asked for and the angle reported.
:::
::::

::::{frame} The Chamber and the Dashboard
:::{present}
- One page drives the rig: **sweep**, **turntable**, **scan**.
- **Start scan** and **STOP** sit in the tab header.
- Every run writes `pattern.csv` and `meta.json`.
:::
:::{present}
:class: callout
The badge top right reads **HARDWARE** or **SIMULATED**. Know which one you
are looking at.
:::

Open the address given in class. The settings sidebar is four sections — **VNA**, **Turntable**,
**Simulation**, **Output** — and the plots carry four tabs: Pattern
Measurement, VNA, Turntable, Logs. Nothing else is needed to take a pattern.

:::{depth}
You can have the whole dashboard on your own laptop before the period, with no
instruments attached: run the service in simulation mode and open the frontend
beside it.

```sh
python chamber_service.py --sim
npm run dev --prefix frontend      # http://localhost:5173
```

The badge reads **SIMULATED** and the service synthesizes a plausible
array-factor pattern — a main lobe, decaying sidelobes, nulls floored around
$-45$ dB — and simulates the tower slewing at a believable rate, so live
position, progress and the stop button all have something real to exercise.
What it will not do is tell you anything about *your* antenna. Rehearse the
controls there, not the physics. Half an hour in simulation is the difference
between a period spent measuring and a period spent finding buttons.
:::
::::

::::{frame} The Chamber Range
:::{present}
- $f = 2.45\ \text{GHz}$, so $\lambda = 12.2\ \text{cm}$.
- **AUT**: pyramidal horn, $24 \times 17\ \text{cm}$, on the tower.
- **Reference**: standard-gain horn, $34 \times 25\ \text{cm}$, $G_{\text{ref}} = 15.0\ \text{dBi}$.
- Source fixed, AUT rotating, absorber everywhere else.
:::

Measure the source-to-tower separation yourself with a tape and write it down;
it is a property of the chamber, not of your run, and every geometry check
below depends on it. The worked numbers that follow are for a $3.0\ \text{m}$
range — redo them with the number you measured.

:::{depth}
The chamber does for you what the absorber block did on a bench range, and
more of it: the specular floor, wall and ceiling bounces are all absorbed
rather than aimed away, which is why the chamber's contribution shows up in
your data as a *floor* rather than as a ripple you can locate. It does not
make the range longer. The far-field criteria below are geometry, and no
amount of absorber changes them.
:::
::::

::::{frame} Is the Range Far Enough?
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
- At $3.0\ \text{m}$ that clears by 3%.
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

::::{frame} Before You Press Start
:::{present}
:class: callout
The tower turns a real antenna on a real cable. **Confirm the cable has slack
for the whole grid.**
:::
:::{present}
- Nobody inside the chamber, door closed.
- **STOP** preempts a move in progress.
- Read the latched positioner error first.
:::

Confirm on the front panel that the axis is in non-continuous mode, because
continuous mode ignores the software limits. Cable wind-up is the standing
hazard on this rig and it is a slow one — it does not announce itself until
the cable is tight. Everything else on this page can be redone in ten minutes;
a torn cable ends the period for everyone.
::::

::::{frame} Procedure — Set the Sweep
:::{present}
1. **VNA** section: start, stop, **Points**, **IF BW**, **Power**.
2. **Parameter: S21** — source on port 1, AUT on port 2.
3. Log all five before anything else.
:::
:::{present}
:class: callout
Read the **CAL / UNCAL** pill. An uncalibrated run is data, never an accident.
:::

The pill sits beside the scan button, and it is there because an uncalibrated
run is never blocked. Setting the sweep is the first step because everything
else depends on it: a calibration belongs to a sweep, and changing span, points, IF
bandwidth or power afterwards leaves the instrument interpolating a correction
across a span it never measured. The panel says so when you do it — it flags
the mismatch and the log warns again at the start of the run.

:::{depth}
Two of those five numbers are yours to argue about. **Points** sets how finely
you resolve frequency: 101 across $2$ to $3\ \text{GHz}$ is a 10 MHz grid,
which is plenty for a horn and far too coarse for a narrowband element.
**IF bandwidth** is the dynamic-range knob — narrowing it lowers the noise
floor by about 10 dB per decade and costs you sweep time on every one of your
angles, which is where a 72-angle run turns into a long one. Power is the
other floor knob and the one with a limit: the amplifier chain and the
receiver both have to stay linear.

The **Calibrate…** button opens a wizard, not a calibration. Running one means
somebody walks into the chamber, unmates the horn and the AUT from the cable
ends, mates the calibration module across them, and comes back out — so the
modal states the sweep it will calibrate at, asks **which reference plane**
you are calibrating, takes an acknowledgement, and reminds you to put the
antennas back. That dropdown is Lesson 9's reference-plane argument turned
into a required field: nothing in the data afterwards distinguishes the cable
ends from the instrument's front panel, and the difference is every dB of
cable loss in your pattern.
:::
::::

::::{frame} Procedure — Peak Up and Define Zero
:::{present}
4. **Turntable** section: jog $\pm 1^\circ$ and $\pm 10^\circ$ until the received level peaks.
5. Press **Define here as 0°**.
:::
:::{present}
:class: callout
Every number you extract afterwards is measured from that zero. Set it once,
before the grid, and do not touch it again.
:::

The VNA tab shows the sweep at the current angle while you jog, so peaking up
is a matter of watching one trace rather than guessing from the tower. Peak on
the frequency you care about, not on the broadest part of the band.

:::{depth}
Defining zero does not move anything — it renames where the axis is standing.
The run file records both the angle the software commanded and the angle the
card reported, and the difference between those two columns is your
positioning error, available afterwards without any extra work. If they
disagree by more than a small fraction of your step size, say so in the report
rather than quietly using the commanded column.
:::
::::

::::{frame} Procedure — The Angle Grid
:::{present}
6. **From** $0^\circ$, **To** $355^\circ$, **Step** $2^\circ$.
7. The hint under the grid reads back the angle count. Check it.
:::
:::{present}
- Step $\le$ HPBW/5 — but sidelobes are narrower than the beam.
- A $40^\circ$ beam allows $8^\circ$. Take $2^\circ$.
:::

Coarse steps do not just add noise; they systematically miss peaks and nulls,
and a sidelobe you stepped over is a sidelobe you cannot report. The cost is
time: the axis spends far longer moving than the VNA spends sweeping, so the
angle count, not the point count, is what sets the length of your period.

:::{depth}
A full circle asked for as 0 to 360 would measure the start angle twice, so
the grid stops one step short — 0 to 355 in $5^\circ$ is 72 angles, and 0 to
358 in $2^\circ$ is 180. Going all the way round is worth the time on this
rig: the back half of the pattern is where the front-to-back ratio lives, and
a $\pm 180^\circ$ cut taken as two halves has a seam in it.
:::
::::

::::{frame} Procedure — Measure Your Floor
:::{present}
8. Unmate the AUT and terminate the cable end in $50\ \Omega$.
9. Run **one angle** with the same sweep. Name it `floor`.
:::
:::{present}
:class: callout
That run is the credibility of your whole data set. Take it before you scan.
:::

Take it at the settings you are about to scan with, and not at whatever the
panel happened to be holding. Setting **From** and **To** to the same angle
gives a one-angle run — the
angle-count hint will say so — and what it records is everything that reaches
port 2 when the antenna is not connected: receiver noise, and whatever leaks
around the chamber through the cables. That is your instrument floor.

:::{depth}
There are two floors here and Lesson 9 named both. The instrument floor is the
one you just measured. The chamber contributes the other, and you cannot
measure it this way: with the AUT unmated nothing radiates, so the stray field
has nothing to scatter. It shows up instead in the back half of a real cut, as
a level that will not go deeper no matter how much you narrow the IF
bandwidth. Whichever of the two is higher is the one you actually have.

Narrowing the IF bandwidth by a decade is the cheapest 10 dB in the building
and is worth doing once as an experiment: take the floor run at two settings
and watch it drop. Do it *before* you calibrate, because changing the IF
bandwidth is exactly the change the calibration panel will warn you about.
:::
::::

::::{frame} Procedure — The Four Scans
:::{present}
10. **E-plane cut.** Name the run for what it is.
11. **H-plane cut**, by rotating both antennas $90^\circ$.
12. **Repeat one cut.** The disagreement *is* your repeatability.
13. **Gain comparison**: mount the reference horn. Change nothing else.
:::

Two scans of the same cut that disagree by 1 dB have measured your uncertainty
directly, which is far more reliable than propagating catalog tolerances. On
step 13, "nothing else" means it: same sweep, same cables, same zero, same
calibration.

:::{depth}
Name every run in the **Output** section before you start it. Left empty the
service stamps the date and time, which is enough to keep the runs apart and
useless for telling you which is which a week later. `l11_eplane_aut`,
`l11_eplane_repeat`, `l11_hplane_aut`, `l11_ref_horn` costs you four seconds
each and is the difference between a reduction session and an archaeology
session. Anything in the **Stored runs** list reloads straight back into the
plots, so a run you named is a run you can still use.
:::
::::

::::{frame} Procedure — Polarization
:::{present}
14. Reinstall the AUT and rotate the **source** $90^\circ$ about the range axis. Re-scan.
:::
:::{present}
:class: callout
Rotate the source, not the AUT. Rotating the AUT would change the cut plane
and the polarization at once, and you could not separate the two.
:::

That scan is your cross-pol pattern, and it is the last acquisition of the
period. Everything after this frame is reduction, and you can do it away from
the chamber.
::::

::::{frame} Reduction — One Scan, Every Frequency
:::{present}
- Each angle stores the **whole sweep**, not one number.
- The **Cut freq** selector replots the same run at any frequency in the span.
- `pattern.csv` is long format: angle, frequency, real, imaginary, dB, phase.
:::

A pattern is a function of frequency, and this is where that stops being a
sentence and starts being a slider. Step the cut frequency across the band and
watch the beam narrow and the sidelobe structure move. Quote the frequency on
every plot you produce; a cut without one is not a measurement of anything.

:::{depth}
The file gives you more than the dashboard plots. Both angle columns are
there, so positioning error is recoverable; the real and imaginary parts are
there, so phase is too, which matters in Module 3 when the thing you are
measuring is an array and the interesting quantity is the phase across it.
Reduce it in Python, one `csv` read and a reshape — the grid is
angles $\times$ frequencies and it is complete, with every angle present at
every frequency.
:::
::::

::::{frame} Reduction — Normalize First
:::{present}
- Subtract the peak from every sample.
- Cable loss, source gain, and range loss all drop out.
- Plot **polar dB** for shape, **rectangular dB** for values.
:::
:::{present}
:class: callout
Never plot pattern data linear. A $-13\ \text{dB}$ sidelobe is 5% of peak and
disappears.
:::

The dashboard's **Normalize** toggle does this on screen for you. Do it again
in your own reduction rather than trusting the screenshot, because the number
you subtracted is one of the things your report has to state.
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
Worked example, one E-plane cut. The peak reads $-35.6\ \text{dB}$ at
$0^\circ$, so the $-3\ \text{dB}$ level is $-38.6\ \text{dB}$. Interpolating
between samples puts the crossings at $-19.8^\circ$ and $+20.2^\circ$:

$$\theta_\text{HP} = 20.2 - (-19.8) = 40.0^\circ$$

The first sidelobe peaks at $-51.4\ \text{dB}$, and the level at $180^\circ$
is $-54.0\ \text{dB}$:

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

Both levels are peak $\vert S_{21}\vert$ in dB at the same cut frequency, one
run each, and everything the two runs have in common subtracts out. The
aperture formula with $\eta_{\text{ap}} = 0.5$ predicts $12.3\ \text{dBi}$, so
the measurement is 0.5 dB low — and the reference horn's own calibration is
good to about 0.5 dB. That is *agreement*, and your report should state it as
agreement rather than assign it a physical cause. Below about 15 dB of XPD,
check the mount alignment before blaming the antenna.
::::

::::{frame} Reduction — Against the Simulation
:::{present}
- **Simulation** section: import the pattern CSV your solver wrote in Lesson 8.
- Both traces are normalized to their own peak, so dBi and $S_{21}$ compare.
- **Rotate** takes out a known mount offset. The footer reports **RMS deviation**.
:::

This is the first time in the course that a predicted pattern and a measured
one are on the same axes, and the number in the footer is the whole argument
of Module 2 in one readout. Import your own model, not somebody else's.

:::{depth}
The comparison is clamped 30 dB below the peak before differencing, which
matters more than it sounds. Nulls are where a model and a measurement
disagree most and where the disagreement means least — a null one degree off
its predicted angle differences to tens of dB against a neighboring lobe.
Un-clamped, the RMS would report null alignment rather than pattern agreement.

Parsing happens in the browser, so nothing is uploaded and the service never
learns a comparison is running. If the RMS comes back large, check **Rotate**
before you check the physics: a mount offset is a rigid shift of the whole
curve and it is the most common reason a good model disagrees with a good
measurement.
:::
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
Work your own numbers first: a peak at $-35.6\ \text{dB}$ against a floor of
$-78\ \text{dB}$ on the terminated run is a **dynamic range of 42.4 dB**. Any
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
floor reads 3 dB high and is nearly meaningless. Averaging smooths the fuzz —
incoherent power averaging shrinks the *variance* like $1/N$ — but it leaves
the mean noise power exactly where it was. To lower the floor you need more
power, a narrower IF bandwidth, or a quieter receiver.
::::

::::{frame} The Rest of the Uncertainty Budget
:::{present}
| Source | Looks like | Size |
| :-- | :-- | :-- |
| Chamber stray field | fills the back lobes | sets the floor |
| Cable flex | drift between scans | 0.2 to 0.5 dB |
| Misalignment | peak low, HPBW biased | 0.2 dB |
| Reference tolerance | offset on every gain | 0.3 to 0.5 dB |
:::

Each leaves a recognizable signature. Cable flex is the one this rig makes
easy to check: repeat a cut without touching anything and difference the two,
and what you see is drift plus noise and nothing else.

:::{depth}
A fifth entry belongs in the budget on any run the panel flags, and it is not
a small one. A calibration is only meaningful at the sweep it was taken at,
and a run set up at a different span, point count, IF bandwidth or power is
flagged in the VNA section and warned about in the log. Correction
interpolated across a span it never measured is a plausible-looking answer of
unknown quality, and "the dashboard warned me and I scanned anyway" is not a
sentence you want in a report.
:::
::::

::::{frame} Deliverables
:::{present}
1. **Two principal-plane cuts**, polar dB, normalized, labeled.
2. **An extracted table**, with an uncertainty on every row.
3. **Your floor**, as a level and a dynamic range.
4. **A comparison against prediction**, discrepancies named.
:::

:::{depth}
In detail:

1. **Two principal-plane cuts** (E-plane and H-plane), plotted in polar dB,
   normalized to the peak, with the angle convention and the **cut frequency**
   labeled on each.
2. **An extracted table** — HPBW, first sidelobe level, front-to-back ratio,
   gain, XPD — with an **uncertainty estimate on every row**. Your repeated
   scan from step 12 is the basis for most of them.
3. **Your measured floor**, stated as a level and as a dynamic range, with one
   sentence per table row saying whether that number clears the floor and by
   how much.
4. **A comparison against prediction** — your Lesson 8 model overlaid, with
   the RMS deviation quoted, plus the aperture-formula gain and the
   $26000/(\theta_E \theta_H)$ beamwidth cross-check — with every discrepancy
   larger than your uncertainty named and explained.

Quote the **run names** for every figure, and state the calibration and mode
your runs were taken under; both are written into each run's `meta.json` and
neither is recoverable afterwards from the pattern alone. A 2 dB gap with a
named cause is a better report than a 0.2 dB gap with no discussion.
:::
::::

::::{frame} The Range Card
:class: read-only

| At the chamber | What to do | Number to remember |
| :-- | :-- | :-- |
| Check geometry | all three criteria, both antennas | the reference sizes the range |
| Set the sweep | span, points, IF BW, power, $S_{21}$ | log all five before calibrating |
| Check the pill | CAL or UNCAL, before the scan | an uncal run is data, not an accident |
| Peak up | jog, then define here as $0^\circ$ | every number is measured from it |
| Angle step | resolve beam *and* sidelobes | step $\le$ HPBW/5, use $2^\circ$ |
| Floor | terminate port 2, one angle | 42 dB dynamic range on this rig |
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
- This lab is the **dress rehearsal** for the midterm, due 2 Oct.
- Same chamber, same extraction, same uncertainty discussion.
- With a written analysis, and no procedure handed to you.
:::

Mistakes made today carry no grade penalty; the same mistakes in the graded
project do. You now have nine lessons of chamber access before the project is
due, which is the reason the measurement block was pulled forward to sit here.

:::{depth}
Lessons 12 to 14 go back to antenna families — loops and monopoles, patches
and slots and horns, reflectors and Yagis — and every gain figure in them is
now a claim you know how to check. Several of those antennas are defensible
choices for your project, and you will be reading their published patterns
with a measurer's eye rather than a reader's.
:::
::::
