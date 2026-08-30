---
frame_view: true
---

# L8 - Dipole Simulation Lab

::::{frame}
:class: title-frame

<div class="course-mark">ECE 444 · Fall 2026</div>

<h1 class="frame-title">Dipole Simulation Lab</h1>

<div class="title-rule"></div>

Today you hand the same antenna to a solver that computes the current instead of assuming it, and then you reconcile the two answers.

A difference you can explain is worth more than an agreement you cannot.

Lesson 8 · Antennas, Phased Arrays, and Radar Systems · Dr. Neil Rogers
::::

::::{frame}
:::{admonition} Slides
:class: slides
<a href="../../slides/L08-dipole-simulation-lab.html" target="_blank" rel="noopener">html slides</a>
<a href="../../slides/L08-dipole-simulation-lab.html?print-pdf" target="_blank" rel="noopener">pdf slides</a>
<a href="../../slides/L08-dipole-simulation-lab.md" target="_blank" rel="noopener">raw markdown slides</a>
:::
::::

::::{frame} Learning Objectives

<ol class="lo-list lo-sublist" style="--module: '2'; --lo: '2'">
  <li>I can explain what the method of moments does — discretize the wire, enforce the boundary condition, solve for the segment currents — and why the simulator then runs the same radiation integral you ran by hand.</li>
  <li>I can build a wire-dipole model in 4nec2 with defensible segmentation and excitation, and run frequency sweeps and pattern computations.</li>
  <li>I can compare simulated impedance, resonant length, pattern, and gain against the analytical half-wave-dipole predictions and account for every difference.</li>
  <li>I can recognize when a simulation is misleading me — segmentation too coarse, wire radius unreasonable, source misplaced — and apply the standard convergence and energy checks.</li>
</ol>
::::

::::{frame} Where we were
Lesson 7 handed you a set of numbers for the half-wave dipole, and every one of
them rests on a single assumption: that the current on the wire is a sinusoid.
Today you hand the same antenna to a solver that computes the current instead of
assuming it, and then you reconcile the two answers. That reconciliation is the
point of the lab, because a difference you can explain is worth more than an
agreement you cannot.
::::

::::{frame} Part 1 — What the solver does
Lesson 6 established the machinery: the far field is the radiation integral over
the current distribution. Give the integral a current and it returns a pattern.
Lesson 7 supplied the current by assumption,
$I(z) = I_m \sin\left(k\left(\frac{L}{2} - \vert z \vert\right)\right)$, and
everything else followed from it.

The **method of moments** (MoM) removes that assumption. It is three steps and a
matrix solve:
::::

::::{frame} The three steps
1. **Discretize.** Chop the wire into $N$ short **segments** and declare the
   current on each one to be an unknown number. You now have $N$ unknowns
   instead of an unknown function.
2. **Enforce the boundary condition.** On a perfect conductor, the total
   tangential electric field is zero. The total field is the source field plus
   the field radiated by all $N$ segment currents, so at each segment
   $E_z^{\text{scattered}} = -E_z^{\text{source}}$. That gives one equation per
   segment.
3. **Solve.** With $N$ equations in $N$ unknowns, one complex matrix solve
   returns the current on every segment.
::::

::::{frame} Consequences of this approach
The solver then evaluates the radiation integral from Lesson 6 over that
numerical current rather than over an analytical one. It sounds simple, but
there are consequences to this approach:

:::{callout}
A simulator knows no more physics than you do. It solves for the current you
would otherwise have had to guess, then computes the same integral you would
have computed. Everything it reports is only as trustworthy as the segments,
the wire radius, and the source you handed it.
:::
::::

::::{frame} NEC and 4nec2
NEC — *Numerical Electromagnetics Code*, written at Lawrence Livermore in the
1970s and still the workhorse of wire-antenna modeling — is this method
specialized to thin wires. 4nec2 is a free Windows front end that writes NEC's
input file for you and plots what comes back.
::::

::::{frame} From currents to one impedance
The solve returns a whole vector of currents, one per segment, but the terminal
impedance comes from exactly one entry in that vector. You applied a known
voltage to the source segment, and the solver reports the current that flows
there, so Ohm's law finishes the job:

$$Z_{\text{in}} = \frac{V_{\text{feed}}}{I_{\text{feed}}}$$

With the customary $V_{\text{feed}} = 1\ \text{V}$ excitation, the input
impedance is simply the reciprocal of the feed-segment current, and its complex
character carries straight through: a feed current lagging the applied voltage
gives a positive reactance, which means an inductive terminal.
::::

::::{frame} Three consequences of the feed segment
Three consequences are worth stating plainly. First, the impedance of the entire
antenna comes from a single number in the solution, so it inherits whatever
error that one segment carries. Second, the rest of the current distribution
does not enter the terminal impedance at all; it sets the radiation pattern
through the radiation integral. Third, those two facts together explain a
failure mode you will meet later in the lab: a source placed on the wrong
segment corrupts the impedance badly while barely moving the pattern, because
the pattern is an integral over a current distribution that hardly changed.
::::

::::{frame} Watch the current converge
:class: viz-frame

:::{depth}
The widget below runs a method-of-moments solve in your browser using a thin
wire, triangle basis functions, and a voltage source on the center segment. Drag
the segment count up from 5 and watch two things at once. The current samples
settle onto the sinusoid, staying close to it but never matching it exactly, and
running fattest near the wire ends where the sinusoid is least accurate. At the
same time $Z_{\text{in}}$ stops moving, and that plateau is what "converged"
means: it does not mean the answer agrees with theory, only that refining the
model no longer changes it. Watch the feed readouts as you drag, since
$V_{\text{feed}}$ is fixed while $I_{\text{feed}}$ moves, and every change in
$Z_{\text{in}}$ comes from that one current — the red band on the wire plot,
where the source sits. The dashed green references are
Lesson 7's $73\ \Omega$ and $42.5\ \Omega$, drawn when the wire is exactly
$\lambda/2$ long, and the plateau lands near them rather than on them. Part 5
explains that gap.
:::

<iframe src="../../viz/mom-dipole.html"
        width="100%" height="453"
        style="border: 1px solid #cddce9; border-radius: 6px;"
        loading="lazy"
        title="Method-of-moments dipole: solved segment currents against the assumed sinusoid, the feed voltage and current that set the input impedance, and impedance versus segment count">
</iframe>
::::

::::{frame} Part 2 — NEC's world, and the rules that bound it
NEC does not know about antennas. It knows about **thin wires**: straight
segments with a length, a radius, and a position. A dipole is one wire with a
segment count, and a Yagi is several wires. That simplicity makes NEC fast, but
we have to follow some rules to avoid divergent results.
::::

::::{frame} Segmentation rules — length
| Rule | Reason | Consequence of breaking it |
| :-- | :-- | :-- |
| 10–20 segments per half wavelength | resolve the curvature of the current | pattern and gain come out smeared |
| $\Delta < \lambda/20$ | phase barely changes across a segment | impedance drifts with segmentation |
| $\Delta > 8a$ | keeps the thin-wire kernel valid | impedance becomes numerically unreliable |
::::

::::{frame} Segmentation rules — geometry, and the tension between them
| Rule | Reason | Consequence of breaking it |
| :-- | :-- | :-- |
| $2\pi a \ll \lambda$ | the wire is thin compared with a wavelength | NEC is solving the wrong problem |
| Odd segment count | puts a segment at the center | the source lands off-center |

Here $\Delta$ is the segment length and $a$ the wire radius. Notice that two of
these rules pull against each other, because refining the mesh drives $\Delta$
down toward $8a$. On a fat wire you eventually run out of room, and that limit
is informative rather than annoying: it is NEC telling you that the thin-wire
approximation does not describe your antenna.
::::

::::{frame} Worked example — segmentation arithmetic for today's dipole
:::{admonition} Worked example — segmentation arithmetic for today's dipole
:class: tip
At $f = 915\ \text{MHz}$:

$$\lambda = \frac{3\times10^8}{915\times10^6} = 0.3279\ \text{m} = 328\ \text{mm}, \qquad \frac{\lambda}{2} = 164\ \text{mm}$$

Take a wire of 1 mm diameter, so $a = 0.5\ \text{mm}$, and start with $N = 21$
segments:

$$\Delta = \frac{164\ \text{mm}}{21} = 7.8\ \text{mm} = 0.024\ \lambda$$
:::
::::

::::{frame} Worked example — segmentation arithmetic for today's dipole, continued
:::{admonition} Worked example — segmentation arithmetic for today's dipole, continued
:class: tip
Now check both bounds. The upper bound is $\lambda/20 = 16.4\ \text{mm}$, and
$7.8\ \text{mm}$ clears it with room to spare. The lower bound is
$8a = 4.0\ \text{mm}$, and $7.8\ \text{mm}$ clears that as well. The thinness
check also passes, since $2\pi a/\lambda = 0.0096$.

How far can you refine? The segment length may fall to $4.0\ \text{mm}$, which
corresponds to $164/4.0 \approx 41$ segments. **Past about 41 segments this wire
is too fat for the standard kernel, and the extra segments make the answer worse
rather than better.** That refinement ceiling is worth computing before you
touch the keyboard.
:::
::::

::::{frame} The source model in NEC
4nec2 drives **one segment** with a 1 V source, and that segment is the antenna
terminal: there is no connector, no coaxial gap, and no balun in the model. The
impedance comes out of that segment by the division you saw in Part 1.

Two modeling consequences follow. First, the source must sit on the center
segment, which is why the segment count is odd. Second, the feed gap is as wide
as a segment, so refining the mesh also refines the feed model. Gain is an
integral over the entire current and settles quickly, while impedance is read
from one segment and settles last. Expect your convergence study to show exactly
that behavior.
::::

::::{frame} The Average Gain Test
Ask NEC for a pattern over the **full sphere** and it will report the **average
power gain**. For a lossless antenna in free space that number must be
$1.000$, because every watt delivered to the terminals has to leave as
radiation. This is a conservation-of-energy audit on your model, and it costs
one extra run.
::::

::::{frame} Reading the average gain check
```{note}
An average gain between 0.95 and 1.05 is a healthy result. A value such as 0.6
or 1.4 means the model is broken, and no other number in the output file can be
trusted until you find the cause. Look for the geometry error, the
segment-length violation, or the misplaced source before you record a single
number. The test is only valid over a complete sphere in free space; adding a
ground plane changes the expected value.
```
::::

::::{frame} Part 3 — Software setup
4nec2 is free and runs on the lab PCs. Everything below is a NEC **input file**,
which is a stack of two-letter cards. 4nec2 can draw the geometry for you, but
type the cards at least once: they are the actual interface, they are identical
across every NEC front end you will meet, and they do not move between versions
the way menu items do.
::::

::::{frame} The NEC input file
Open 4nec2, choose to edit the input file, and enter:

```text
CM ECE 444 L8 -- half-wave dipole, 915 MHz
CE
GW 1 21 0 0 -0.08197 0 0 0.08197 0.0005
GE 0
EX 0 1 11 0 1 0
FR 0 1 0 0 915 0
RP 0 181 1 1000 0 0 1 0
EN
```
::::

::::{frame} Reading the cards — geometry and excitation
Line by line:

| Card | What it says |
| :-- | :-- |
| `GW 1 21 ...` | wire tag 1, 21 segments, from $z = -81.97\ \text{mm}$ to $+81.97\ \text{mm}$, radius $0.5\ \text{mm}$ (all in meters) |
| `GE 0` | geometry complete, free space, no ground |
| `EX 0 1 11 0 1 0` | voltage source, 1 V, on wire 1 segment 11 — the middle of 21 |
::::

::::{frame} Reading the cards — frequency and pattern
| Card | What it says |
| :-- | :-- |
| `FR 0 1 0 0 915 0` | one frequency, 915 MHz |
| `RP 0 181 1 1000 ...` | pattern cut: $\theta$ from $0^\circ$ to $180^\circ$ in $1^\circ$ steps at $\phi = 0$ |

The wire lies along $z$, matching the course convention, so broadside is
$\theta = 90^\circ$ and the pattern cut above is the E-plane.
::::

::::{frame} Running the model
Run the model with the Calculate or Generate command, which 4nec2 offers on the
toolbar and on the function keys, then read the results in the output-data and
pattern windows. Impedance appears with the source data, and gain appears with
the pattern.

```{note}
Menu wording drifts between 4nec2 versions, so this handout names the input
cards rather than click paths. If you cannot find a control, the input file is
always editable directly, and the run always produces the same output file.
```
::::

::::{frame} Part 4 — Procedure
Work through these steps in order and record your results as you go. Write every
prediction down before you run the corresponding case, because a prediction
written after the fact teaches you nothing.
::::

::::{frame} Step 1 — Predict
Before running anything, write down what Lesson 7 says
this antenna should do: $Z_{\text{in}}$, resonant length, gain in dBi, and
E-plane HPBW. These are your reference numbers, and they should not change once
you see the simulated values.
::::

::::{frame} Step 2 — Segmentation arithmetic
Compute $\Delta$, check it against
$\lambda/20$ and $8a$, and compute your refinement ceiling. Do this on paper.
::::

::::{frame} Step 3 — Baseline run
Run the file from Part 3 at 915 MHz and record
$Z_{\text{in}}$ and the gain. Compare both against your prediction immediately,
and record the differences before you change anything in the model.
::::

::::{frame} Step 4 — Average gain
Change the pattern request to a full sphere with the
averaging flag on:

```text
RP 0 19 36 1001 0 0 10 10
```

That request sweeps $\theta$ from $0^\circ$ to $180^\circ$ in $10^\circ$ steps
and $\phi$ from $0^\circ$ to $350^\circ$ in $10^\circ$ steps, and the final digit
of the fourth field is what asks for the average gain. Record the value.
**If it is not close to 1.000, stop and fix the model before continuing.**
::::

::::{frame} Step 5 — Frequency sweep
Replace the `FR` card with

```text
FR 0 41 0 0 800 5
```

which sweeps 800 to 1000 MHz in 5 MHz steps. Plot $R_{\text{in}}$ and
$X_{\text{in}}$ against frequency and read off the frequency where
$X_{\text{in}} = 0$. A wire cut to $\lambda/2$ at 915 MHz will not resonate at
915 MHz, so determine where it does resonate and by how much it misses.
::::

::::{frame} Step 6 — Trim to resonance
Now hold the frequency at 915 MHz and shorten
the wire instead. Change the `GW` end coordinates in steps of a millimetre or
two until $X_{\text{in}}$ crosses zero. Record the resonant length as a fraction
of $\lambda$ and the resistance there. Keep the segment count odd throughout,
and recheck $\Delta$ against $8a$ after each change.
::::

::::{frame} Step 7 — Pattern cuts
At the resonant length, take the E-plane cut
($\phi = 0$, $\theta$ swept) and the H-plane cut ($\theta = 90^\circ$, $\phi$
swept):

```text
RP 0 1 361 1000 90 0 0 1
```

Record the peak gain, the HPBW in the E-plane, and the depth of the nulls along
the wire axis. Confirm that the H-plane cut is a circle to within a small
fraction of a decibel.
::::

::::{frame} Step 8 — Convergence study
Re-run the resonant model at $N = 11$, 21, 41,
and 81 segments and tabulate $Z_{\text{in}}$ and gain for each. Identify the
point where the answer stops moving, and the point where the $\Delta > 8a$ rule
begins to bite.
::::

::::{frame} Part 5 — Deliverables
Turn in a single short report containing:

1. **The comparison table** below, filled in, with a percent difference on every
   row.
2. **One paragraph per row** accounting for the difference. "Simulation error"
   is not an account of anything, so name the mechanism instead.
3. **Your convergence table** from Step 8, plus one sentence defending the
   segment count you would use if this were a real design.
4. **The average gain figure** from Step 4.
::::

::::{frame} The comparison table
| Quantity | L7 analytical | Simulated | Difference | Why |
| :-- | :-- | :-- | :-- | :-- |
| $Z_{\text{in}}$ at exactly $\lambda/2$ | $73 + j42.5\ \Omega$ | | | |
| Resonant length | $0.47\text{–}0.48\ \lambda$ | | | |
| $R_{\text{in}}$ at resonance | $\approx 70\ \Omega$ | | | |
::::

::::{frame} The comparison table, continued
| Quantity | L7 analytical | Simulated | Difference | Why |
| :-- | :-- | :-- | :-- | :-- |
| Gain | $2.15\ \text{dBi}$ | | | |
| E-plane HPBW | $78^\circ$ | | | |

Four of those rows should land within a few percent. The first row will not, so
the mechanism behind it is worth stating here rather than leaving you to
discover it by accident.
::::

::::{frame} Why the half-wave number misses
The number $73 + j42.5\ \Omega$ is the impedance of a **sinusoid**, not of a
**wire**. A sinusoidal current resonates when the wire is about $0.486\lambda$
long. A real wire has finite radius, stores energy in the near field around that
radius, and resonates shorter, at roughly $0.473\lambda$ for the wire you are
modeling today. A wire cut to exactly $\lambda/2$ is therefore already about 5%
long, which makes it inductive and raises its resistance well up the curve.
Expect something near $86 + j47\ \Omega$ from the simulator. That is not a 17%
error in NEC, because the two numbers describe two different antennas. Step 6
trims the wire to resonance, and once you do the two answers agree to within a
couple of ohms.
::::

::::{frame} The end effect
The second mechanism worth naming is the **end effect**. The assumed sinusoid
goes to zero at the wire tips with a clean slope, while the real current
approaches the tips more gradually because charge accumulates there. That
fattened current near the tips is visible in the widget in Part 1, and it is
what pushes resonance shorter and resistance higher.

```{note}
A useful habit for the rest of the course is this: whenever a simulation and a
hand calculation disagree, first ask whether the two are describing the same
antenna. More often than not they are not, and the disagreement resolves itself
once you make the two models match.
```
::::

::::{frame} Summary — the method of moments
| Symbol / idea | What it is | Number to remember |
| :-- | :-- | :-- |
| Method of moments | discretize the wire, enforce $E_{\text{tan}} = 0$, solve for the segment currents, then integrate | $N$ unknowns, one matrix solve |
| $Z_{\text{in}} = V_{\text{feed}}/I_{\text{feed}}$ | terminal impedance from the one segment carrying the source | 1 V drive makes it $1/I_{\text{feed}}$ |
| Segments $N$ | segmentation of the wire; odd, so a segment sits at the feed | 10–20 per half wavelength |
::::

::::{frame} Summary — segmentation and convergence
| Symbol / idea | What it is | Number to remember |
| :-- | :-- | :-- |
| $\Delta$ against $\lambda$ | upper bound on segment length, set by phase change | $\Delta < \lambda/20$ |
| $\Delta$ against $a$ | lower bound on segment length, set by the thin-wire kernel | $\Delta > 8a$ |
| Convergence | the answer stops moving under refinement, which is not the same as matching theory | change $< 1\%$ per doubling |
::::

::::{frame} Summary — checks and today's numbers
| Symbol / idea | What it is | Number to remember |
| :-- | :-- | :-- |
| Average power gain | conservation-of-energy audit on a lossless free-space model | $1.000$, accept 0.95–1.05 |
| $Z_{\text{in}}$ at exactly $\lambda/2$ | the wire is about 5% long, so it is inductive | near $86 + j47\ \Omega$ |
| Resonant length and gain | where $X_{\text{in}} = 0$, and the gain there | $\approx 0.473\lambda$, $2.15\ \text{dBi}$, $78^\circ$ |
::::

::::{frame} Practice
- <a href="../../practice/ECE444_L08_Practice_blank.pdf" target="_blank" rel="noopener">Problem set (PDF)</a>
- <a href="../../practice/ECE444_L08_Practice_SOLUTIONS.pdf" target="_blank" rel="noopener">Solutions (PDF)</a>
::::

::::{frame} Where this is going
Lesson 9 returns to theory with loops and monopoles. The monopole is where your
new NEC habits get their first real test, because a quarter-wave monopole is
only half an antenna and the other half is the ground plane. NEC models ground
with its own card, and getting that card wrong is a common way to produce a
confident and completely incorrect monopole result, including an average gain
that no longer has to equal one. Before Lesson 9, review your Lesson 7 notes on
the sinusoidal current assumption, and be ready to state how a quarter-wave
monopole over perfect ground relates to the half-wave dipole in both impedance
and directivity.
::::

::::{frame} Where this is going, continued
Beyond that, Module 3 is built entirely on arrays, and an array is just more
wires. The segmentation rules you applied to one dipole today apply to every
element at once, and the matrix you solved for 21 unknowns becomes a matrix for
several hundred. The physics does not change and only the bookkeeping grows, so
the habit of predicting before simulating matters more as the models get large
enough that nobody can check the answer by eye.
::::
