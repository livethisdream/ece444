---
frame_view: true
---

# L8 - Dipole Simulation Lab

::::{frame}
:class: title-frame

<div class="course-mark">ECE 444 · Fall 2026</div>

<h1 class="frame-title">Dipole Simulation Lab</h1>

<div class="title-rule"></div>

Today we hand the same antenna to a solver that computes the current instead of assuming it.

Lesson 8 · Antennas, Phased Arrays, and Radar Systems · Dr. Neil Rogers
::::

::::{frame} Slides
:class: read-only

:::{admonition} Slides
:class: slides
<a href="../../slides/L08-dipole-simulation-lab.html" target="_blank" rel="noopener">html slides</a>
<a href="../../slides/L08-dipole-simulation-lab.html?print-pdf" target="_blank" rel="noopener">pdf slides</a>
<a href="../../slides/L08-dipole-simulation-lab.md" target="_blank" rel="noopener">raw markdown slides</a>
:::
::::

::::{frame} Learning Objectives

<ol class="lo-list lo-sublist" style="--module: '2'; --lo: '2'">
  <li>I can explain what the method of moments does — discretize the wire, expand the current in basis functions, enforce the boundary condition, and solve for the amplitudes — and why the simulator then runs the same radiation integral you ran by hand.</li>
  <li>I can build a wire-dipole model in 4nec2 with defensible segmentation and excitation, and run frequency sweeps and pattern computations.</li>
  <li>I can compare simulated impedance, resonant length, pattern, and gain against the analytical half-wave-dipole predictions and account for every difference.</li>
  <li>I can recognize when a simulation is misleading me — segmentation too coarse, wire radius unreasonable, source misplaced — and apply the standard convergence and energy checks.</li>
</ol>
::::

::::{frame} Where We Were
:::{present}
| Quantity | Lesson 7 |
| :-- | :-- |
| $Z_{\text{in}}$ at $\lambda/2$ | $73 + j42.5\ \Omega$ |
| Resonant length | $0.47$ to $0.48\ \lambda$, about $70\ \Omega$ |
| Gain | $2.15\ \text{dBi}$ |
| E-plane HPBW | $78^\circ$ |
:::
:::{present}
- **Lesson 6**: the pattern is the radiation integral over the current.
- **Lesson 7** assumed the current:

$$I(z) = I_m \sin\left[k\left(\frac{L}{2} - \vert z \vert\right)\right]$$

- Every number rests on it.
:::

Lesson 7 handed you a set of numbers for the half-wave dipole, and every one of
them rests on a single assumption: that the current on the wire is a sinusoid.
Today you hand the same antenna to a solver that computes the current instead of
assuming it, and then you reconcile the two answers. That reconciliation is the
point of the lab, because a difference you can explain is worth more than an
agreement you cannot.
::::

::::{frame} The Method of Moments
:::{present}
- **Discretize**: $N$ segments.
- **Expand** the unknown current in $N$ known **basis functions** with unknown amplitudes:

$$I(z) \approx \sum_{n=1}^{N} I_n\ f_n(z)$$

- **Enforce** $E_{\text{tan}} = 0$ on the conductor: one equation per segment.
- **Solve** the $N \times N$ system for the $I_n$, then run the radiation integral of Lesson 6.
:::

Lesson 6 established the machinery: the far field is the radiation integral over
the current distribution. Give the integral a current and it returns a pattern.
Lesson 7 supplied the current by assumption,
$I(z) = I_m \sin\left(k\left(\frac{L}{2} - \vert z \vert\right)\right)$, and
everything else followed from it.

The **method of moments** (MoM) removes that assumption by solving for the
current. We do not know $I(z)$, so we write it as a sum of $N$ known shapes,
the **basis functions** $f_n(z)$, each one living on one short piece of the
wire, with $N$ unknown amplitudes $I_n$:

$$I(z) \approx \sum_{n=1}^{N} I_n\ f_n(z)$$

The choice of shape is the key decision. A pulse, constant across its segment,
is the simplest, but it makes the current a staircase, and a staircase puts all
of its charge in spikes at the steps, so the near field, and with it the
reactance, comes out badly. A triangle, peaking at one segment junction and
falling to zero at the next, keeps the current continuous and spreads the
charge evenly. NEC uses a short piece of a sinusoid on each segment, which is
what a standing wave looks like up close, so few segments are needed before
the sum stops changing. The convergence widget below draws the pieces.

With the shapes fixed, the physics is the boundary condition of a perfect
conductor: the total tangential electric field on the wire is zero. The total
field is the field of the source plus the field radiated by every one of the
$N$ pieces of current, so requiring it to vanish on each segment gives $N$
equations in the $N$ unknown amplitudes:

$$E_z^{\text{scattered}}(z_m) = -E_z^{\text{source}}(z_m), \qquad m = 1, \ldots, N$$

Each equation is one row of an $N \times N$ complex matrix whose entry
$Z_{mn}$ is the field that basis function $n$ produces on segment $m$. One
matrix solve returns every $I_n$, and the sum above is the current.
::::

::::{frame} Assumptions and Consequences
:::{present}
:class: callout
A simulator knows no more physics than you do. It solves for the current
instead of assuming it, then computes the same integral. Everything it reports
is as good as the segments, the basis functions, the radius, and the source.
:::

The solver evaluates the radiation integral from Lesson 6 over that numerical
current rather than over an analytical one. It sounds simple, but there are
consequences to this approach: every number the simulator reports inherits
the choices in the model. The segments set how finely the current can vary,
the basis functions set what shape it can take between the samples, the
radius sets whether the thin-wire model describes the conductor at all, and
the source sets the one segment the impedance is read from. The program
checks none of them.
::::

::::{frame} NEC and 4nec2
:::{present}
- **NEC**, the Numerical Electromagnetics Code: Lawrence Livermore, 1970s.
- It knows **thin wires**: straight segments with a length, a radius, and a position.
- A dipole is one wire; a Yagi is several.
- **4nec2** writes the input file and plots the results.
:::

NEC — *Numerical Electromagnetics Code*, written at Lawrence Livermore in the
1970s and still the workhorse of wire-antenna modeling — is this method
specialized to thin wires. 4nec2 is a free Windows front end that writes NEC's
input file for you and plots what comes back.

NEC does not know about antennas. It knows about **thin wires**: straight
segments with a length, a radius, and a position. A dipole is one wire with a
segment count, and a Yagi is several wires. That simplicity makes NEC fast, but
we have to follow some rules to avoid divergent results.
::::

::::{frame} Finding the Impedance in MoM
:::{present}
- **One segment** carries the 1 V source and is the terminal.

$$Z_{\text{in}} = \frac{V_{\text{feed}}}{I_{\text{feed}}}$$

- At 1 V, the impedance is the reciprocal of the feed current.
- The other currents set the **pattern**.
:::
:::{present}
:class: callout
A misplaced source corrupts the impedance and barely moves the pattern.
:::

4nec2 drives **one segment** with a 1 V source, and that segment is the antenna
terminal: there is no connector, no coaxial gap, and no balun in the model.
The solve returns a whole vector of currents, one per segment, but the terminal
impedance comes from exactly one entry in that vector. You applied a known
voltage to the source segment, and the solver reports the current that flows
there, so Ohm's law finishes the job:

$$Z_{\text{in}} = \frac{V_{\text{feed}}}{I_{\text{feed}}}$$

With the customary $V_{\text{feed}} = 1\ \text{V}$ excitation, the input
impedance is simply the reciprocal of the feed-segment current, and its complex
character carries straight through: a feed current lagging the applied voltage
gives a positive reactance, which means an inductive terminal.

There are three consequences to this approach. First, the impedance of the entire
antenna comes from a single number in the solution, so it inherits whatever
error that one segment carries. Second, the rest of the current distribution
does not enter the terminal impedance at all; it sets the radiation pattern
through the radiation integral. Third, those two facts together explain a
failure mode you will meet later in the lab: a source placed on the wrong
segment corrupts the impedance badly while barely moving the pattern, because
the pattern is an integral over a current distribution that hardly changed.
::::

::::{frame} Segment Length Rules
:::{present}
| Rule | Reason | Consequence of breaking it |
| :-- | :-- | :-- |
| 10–20 segments per half wavelength | resolve the curvature of the current | pattern and gain come out smeared |
| $\Delta < \lambda/20$ | phase barely changes across a segment | impedance drifts with segmentation |
| $\Delta > 8a$ | keeps the thin-wire kernel valid | impedance becomes numerically unreliable |
:::

Here $\Delta$ is the segment length and $a$ the wire radius. The thin-wire
model treats each segment's current as a filament on the wire's axis and
evaluates its field on the surface, a distance $a$ away. That describes a
segment only when the segment is much longer than the radius. When $\Delta$
falls below about $8a$ the segment is closer to a ring than to a piece of a
line, the filament no longer describes it, and the matrix entries between
neighboring segments become inaccurate.
::::

::::{frame} Segment Geometry Rules
:::{present}
| Rule | Reason | Consequence of breaking it |
| :-- | :-- | :-- |
| $2\pi a \ll \lambda$ | the wire is thin compared with a wavelength | NEC solves a filament, not your conductor |
| Odd segment count | puts a segment at the center | the source lands off-center |

- Refining drives $\Delta$ toward $8a$.
:::

NEC models a wire as a single filament of axial current and enforces the
boundary condition on the surface at radius $a$. That is the problem it solves.
The problem we want solved is a conducting cylinder, whose surface current can
vary around the circumference and can have a component around the wire near
the ends. The two problems have the same answer only when the circumference is
small compared with a wavelength, $2\pi a \ll \lambda$, because then nothing
can vary around the wire within a wavelength and the surface current is the
same as a filament on the axis. For a large-radius conductor NEC still returns
a number, and it is the number for the filament, not for your antenna.

Notice that two of these rules pull against each other, because refining the
mesh drives $\Delta$ down toward $8a$. On a wire whose radius is large relative
to the segment length you eventually run out of room, and that limit is
informative rather than annoying: the segments have reached the length the
thin-wire model needs, and refining further describes your antenna worse, not
better.
::::

::::{frame} Segmentation Math at 915 MHz
:::{present}
| Quantity | Work | Result |
| :-- | :-- | :-- |
| $\lambda$, $\lambda/2$ | $c/f$ | $328$, $164\ \text{mm}$ |
| $\Delta$ | $164/21$ | $7.8\ \text{mm}$, $0.024\lambda$ |
| $\lambda/20$ | $328/20$ | $16.4\ \text{mm} > \Delta$ |
| $8a$, $a = 0.5\ \text{mm}$ | $8 \times 0.5$ | $4.0\ \text{mm} < \Delta$ |
| Ceiling | $164/4.0$ | 41 segments |

**Above 41 segments, $\Delta < 8a$: the segments are shorter than the thin-wire model allows.**
:::

:::{admonition} Worked example — segmentation math for today's dipole
:class: tip
At $f = 915\ \text{MHz}$:

$$\lambda = \frac{3\times10^8}{915\times10^6} = 0.3279\ \text{m} = 328\ \text{mm}, \qquad \frac{\lambda}{2} = 164\ \text{mm}$$

Take a wire of 1 mm diameter, so $a = 0.5\ \text{mm}$, and start with $N = 21$
segments:

$$\Delta = \frac{164\ \text{mm}}{21} = 7.8\ \text{mm} = 0.024\ \lambda$$

Now check both bounds. The upper bound is $\lambda/20 = 16.4\ \text{mm}$, and
$7.8\ \text{mm}$ clears it with room to spare. The lower bound is
$8a = 4.0\ \text{mm}$, and $7.8\ \text{mm}$ clears that as well. The thin-wire
condition also holds, since $2\pi a/\lambda = 0.0096$.

How far can you refine? The segment length may fall to $4.0\ \text{mm}$, which
corresponds to $164/4.0 \approx 41$ segments. **Past about 41 segments the
segment length falls below $8a$: the wire's radius is too large for the
thin-wire model to describe segments that short, and the extra segments make
the answer worse rather than better.** That refinement ceiling is worth
computing before you touch the keyboard.
:::
::::

::::{frame} All Models Are Wrong, Some Are Useful
:::{present}
| Symptom | Likely cause | Check |
| :-- | :-- | :-- |
| Gain drifts with $N$ | too few segments | double $N$ |
| Impedance wild or oscillating | $\Delta < 8a$ | lengthen segments |
| Impedance far from theory | misplaced source | odd count, center segment |
| Average gain not 1 | geometry or kernel error | fix first |
:::

The simulator does not report that it is wrong, so these four checks are the
questions you have to ask it. Most groups meet at least two of these symptoms
in a lab period, and the last row is the subject of the next frame.
::::

::::{frame} The Average Gain Test
:::{present}
- A **full-sphere** pattern request reports the **average power gain**.
- Lossless, free space: it must be $1.000$.
- $0.95$ to $1.05$ is acceptable; $0.6$ or $1.4$ means the model is wrong. Fix it first.
- Valid only over a full sphere.
:::

Ask NEC for a pattern over the **full sphere** and it will report the **average
power gain**. For a lossless antenna in free space that number must be
$1.000$, because every watt delivered to the terminals has to leave as
radiation. This is a conservation-of-energy audit on your model, and it costs
one extra run.

```{note}
An average gain between 0.95 and 1.05 is acceptable. A value near 0.6 or 1.4
means the model is wrong, and no other number in the output file can be trusted
until it is fixed. Check the geometry, the segment-length limits, and the source
placement before recording any results. The test is only valid over a complete
sphere in free space; adding a ground plane changes the expected value.
```
::::

::::{frame} Convergence
:class: viz-frame

:::{present}
<iframe src="../../viz/mom-dipole.html"
        width="100%" height="490"
        style="border: 1px solid #cddce9; border-radius: 6px;"
        loading="lazy"
        title="Method-of-moments dipole: solved segment currents against the assumed sinusoid, the feed voltage and current that set the input impedance, and impedance versus segment count">
</iframe>
:::

The widget above runs a method-of-moments solve in your browser: a thin wire,
a voltage source on the center segment, and your choice of basis function.
Check **show basis functions** and the current is drawn as what it is, a sum
of overlapping pieces, one per segment junction, each scaled by its solved
amplitude; the dots are the amplitudes and the curve through them is the sum.
Switch from triangles to sinusoidal pieces, NEC's choice, and watch the
convergence plot: the same answer arrives with fewer segments, because a piece
of a sinusoid is already the shape the current wants to take.

Drag the segment count up from 5 and watch two things at once. The current
samples settle onto the sinusoid, staying close to it but never matching it
exactly, and running largest near the wire ends where the sinusoid is least
accurate. At the
same time $Z_{\text{in}}$ stops moving, and that plateau is what "converged"
means: it does not mean the answer agrees with theory, only that refining the
model no longer changes it. Watch the feed readouts as you drag, since
$V_{\text{feed}}$ is fixed while $I_{\text{feed}}$ moves, and every change in
$Z_{\text{in}}$ comes from that one current — the red band on the wire plot,
where the source sits. The dashed green references are
Lesson 7's $73\ \Omega$ and $42.5\ \Omega$, drawn when the wire is exactly
$\lambda/2$ long, and the plateau lands near them rather than on them. The frame
on why the half-wave number misses explains that gap.

Now drag the length past $0.5\lambda$ and the single hump splits into two.
Nothing about the solver changed; that is the standing wave of Lesson 7. The
current on each arm is a piece of a sinusoid that must be zero at the open
tip, so its maximum sits a quarter wavelength in from that tip. On a half-wave
dipole each arm is a quarter wavelength long and both maxima land on the feed,
which is one hump. Lengthen the wire and each maximum stays a quarter
wavelength from its tip, so the two move apart from the feed. By $0.7\lambda$,
the end of the slider, they sit $0.1\lambda$ either side of the feed with a dip
between them, and at $L = \lambda$ that dip would be a null. The solved
current follows the same shape because the tips still force it to zero, and
the assumed sinusoid tracks it.
::::

::::{frame} Software Setup
:::{present}
- The NEC **input file** is a stack of two-letter **cards**.
- Type the cards at least once: they are the interface, identical across every NEC front end.
- Edit the file, run **Calculate**, and read the pattern and sweep windows.
:::

4nec2 is free and runs on the lab PCs. Everything below is a NEC **input file**,
which is a stack of two-letter cards. 4nec2 can draw the geometry for you, but
type the cards at least once: they are the actual interface, they are identical
across every NEC front end you will meet, and they do not move between versions
the way menu items do.
::::

::::{frame} The NEC Input File
:::{present}
```text
CM ECE 444 L8 half-wave dipole 915 MHz
CE
GW 1 21 0 0 -0.08197 0 0 0.08197 0.0005
GE 0
EX 0 1 11 0 1 0
FR 0 1 0 0 915 0
RP 0 181 1 1000 0 0 1 0
EN
```
:::

Open 4nec2, choose to edit the input file, and enter the cards above.
::::

::::{frame} The Cards: Geometry and Excitation
:::{present}
| Card | What it says |
| :-- | :-- |
| `GW 1 21 ...` | wire tag 1, 21 segments, from $z = -81.97\ \text{mm}$ to $+81.97\ \text{mm}$, radius $0.5\ \text{mm}$ |
| `GE 0` | free space |
| `EX 0 1 11 0 1 0` | 1 V source on wire 1, segment 11 of 21 |
:::

Line by line: the `GW` card gives every coordinate in meters, so the wire runs
from $z = -81.97\ \text{mm}$ to $+81.97\ \text{mm}$ with a radius of
$0.5\ \text{mm}$; `GE 0` says the geometry is complete, in free space with no
ground; and `EX 0 1 11 0 1 0` places a 1 V voltage source on wire 1, segment 11,
the middle of 21.
::::

::::{frame} The Cards: Frequency and Pattern
:::{present}
| Card | What it says |
| :-- | :-- |
| `FR 0 1 0 0 915 0` | one frequency, 915 MHz |
| `RP 0 181 1 1000 ...` | E-plane cut, $\theta$ from $0^\circ$ to $180^\circ$ by $1^\circ$, $\phi = 0$ |

- The wire lies along $z$, so broadside is $\theta = 90^\circ$.
:::

The wire lies along $z$, matching the course convention, so broadside is
$\theta = 90^\circ$ and the pattern cut above is the E-plane.

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

::::{frame} The Procedure
:::{present}
1. Predict
2. Segmentation math
3. Baseline run
4. Average gain
5. Frequency sweep
6. Trim to resonance
7. Pattern cuts
8. Convergence study

**Write every prediction down before you run the case.**
:::

Work through these steps in order and record your results as you go. Write every
prediction down before you run the corresponding case, because a prediction
written after the fact teaches you nothing.
::::

::::{frame} Steps 1 and 2: Predict and Segment
:::{present}
**Step 1: predict.** Write down Lesson 7's $Z_{\text{in}}$, resonant length,
gain, and E-plane HPBW. They do not change afterward.
:::
:::{present}
**Step 2: segmentation math.** Compute $\Delta$, check it against
$\lambda/20$ and $8a$, and compute the refinement ceiling, on paper.
:::

Before running anything, write down what Lesson 7 says
this antenna should do: $Z_{\text{in}}$, resonant length, gain in dBi, and
E-plane HPBW. These are your reference numbers, and they should not change once
you see the simulated values. Then compute $\Delta$, check it against
$\lambda/20$ and $8a$, and compute your refinement ceiling. Do this on paper.
::::

::::{frame} Step 3: Baseline Run
:::{present}
- Run the input file at 915 MHz.
- Record $Z_{\text{in}}$ and the gain.
- Record the differences from your prediction before changing anything.
:::

Run the input file above at 915 MHz and record
$Z_{\text{in}}$ and the gain. Compare both against your prediction immediately,
and record the differences before you change anything in the model.
::::

::::{frame} Step 4: Average Gain
:::{present}
Request a full sphere with averaging on:

```text
RP 0 19 36 1001 0 0 10 10
```

**If it is not close to $1.000$, stop and fix the model.**
:::

Change the pattern request to a full sphere with the averaging flag on. That
request sweeps $\theta$ from $0^\circ$ to $180^\circ$ in $10^\circ$ steps
and $\phi$ from $0^\circ$ to $350^\circ$ in $10^\circ$ steps, and the final digit
of the fourth field is what asks for the average gain. Record the value.
**If it is not close to 1.000, stop and fix the model before continuing.**
::::

::::{frame} Step 5: Frequency Sweep
:::{present}
Sweep 800 to 1000 MHz in 5 MHz steps:

```text
FR 0 41 0 0 800 5
```

- Plot $R_{\text{in}}$ and $X_{\text{in}}$; read where $X_{\text{in}} = 0$.
- The wire will not resonate at 915 MHz. By how much does it miss?
:::

Replace the `FR` card with the sweep above, which covers 800 to 1000 MHz in
5 MHz steps. Plot $R_{\text{in}}$ and
$X_{\text{in}}$ against frequency and read off the frequency where
$X_{\text{in}} = 0$. A wire cut to $\lambda/2$ at 915 MHz will not resonate at
915 MHz, so determine where it does resonate and by how much it misses.
::::

::::{frame} Step 6: Trim to Resonance
:::{present}
- Hold 915 MHz. Shorten the `GW` end coordinates a millimeter or two at a time until $X_{\text{in}}$ crosses zero.
- Record the resonant length as a fraction of $\lambda$, and $R_{\text{in}}$ there.
- Keep $N$ odd. Recheck $\Delta > 8a$ after each change.
:::

Now hold the frequency at 915 MHz and shorten
the wire instead. Change the `GW` end coordinates in steps of a millimeter or
two until $X_{\text{in}}$ crosses zero. Record the resonant length as a fraction
of $\lambda$ and the resistance there. Keep the segment count odd throughout,
and recheck $\Delta$ against $8a$ after each change.
::::

::::{frame} Step 7: Pattern Cuts
:::{present}
At the resonant length, take both principal cuts:

```text
RP 0 1 361 1000 90 0 0 1
```

- Record peak gain, E-plane HPBW, and the null depth on the wire axis.
- The H-plane cut should be a circle.
:::

At the resonant length, take the E-plane cut
($\phi = 0$, $\theta$ swept) and the H-plane cut ($\theta = 90^\circ$, $\phi$
swept). The E-plane cut is the `RP` card in the input file above; the card
above is the H-plane cut. Record the peak gain, the HPBW in the E-plane, and the
depth of the nulls along the wire axis. Confirm that the H-plane cut is a circle
to within a small fraction of a decibel.
::::

::::{frame} Step 8: Convergence Study
:::{present}
- Re-run the resonant model at $N = 11$, 21, 41, and 81 segments.
- Tabulate $Z_{\text{in}}$ and gain for each.
- Find where the answer stops moving, and where $\Delta > 8a$ begins to fail.
:::

Re-run the resonant model at $N = 11$, 21, 41,
and 81 segments and tabulate $Z_{\text{in}}$ and gain for each. Identify the
point where the answer stops moving, and the point where the $\Delta > 8a$ rule
begins to bite.
::::

::::{frame} Deliverables
:::{present}
For your midterm antenna:

1. **Pattern**: E- and H-plane cuts, HPBW, sidelobes, gain.
2. **Impedance**: $Z_{\text{in}}$ and VSWR across the band.
3. **Checks**: average gain, convergence table.
4. **Comparison** with hand analysis, every difference explained.
:::

Today's dipole is the rehearsal. The product of this lab is the **Analysis**
section of the midterm project: the simulated prediction for the antenna you
will put on the range in Lessons 13 and 14. The project handout governs what
that section must contain; this is how to build it.

1. **Pattern.** Predict the E-plane and H-plane cuts, and read the half-power
   beamwidth, the sidelobe level, and the gain from them.
2. **Impedance.** Predict $Z_{\text{in}}$ and VSWR across the band you will
   measure, and the resonant frequency.
3. **Checks.** Run the average-gain test before recording anything, and show a
   convergence table so the reader knows the numbers have stopped moving.
4. **Comparison.** Set the simulation beside your hand analysis and account
   for every difference. "Simulation error" is not an account of anything, so
   name the mechanism. When the measurement comes in at Lesson 14 you will add
   a third column.

Build it the way you built the dipole today: predict by hand first, model the
antenna, check the model, then compare. The dipole comparison table below,
filled in, is the worked example.
::::

::::{frame} The Comparison Table
:::{present}
| Quantity | L7 | NEC | Diff. | Why |
| :-- | :-- | :-- | :-- | :-- |
| $Z_{\text{in}}$ at $\lambda/2$ | $73 + j42.5\ \Omega$ | | | |
| Resonant length | $0.47\text{–}0.48\ \lambda$ | | | |
| $R_{\text{in}}$ at resonance | $\approx 70\ \Omega$ | | | |
| Gain | $2.15\ \text{dBi}$ | | | |
| E-plane HPBW | $78^\circ$ | | | |

Four rows should land within a few percent. The first will not.
:::

Four of those rows should land within a few percent. The first row will not, so
the mechanism behind it is worth stating here rather than leaving you to
discover it by accident.
::::

::::{frame} Why the Half-Wave Number Misses
:::{present}
- $73 + j42.5\ \Omega$ is the impedance of a **sinusoid**, not a **wire**.
- Exactly $\lambda/2$ is about 5% long: inductive, near $86 + j47\ \Omega$.
- **End effect**: the tip current exceeds the sinusoid, raising the resistance.
- Trimmed, the two agree within a few ohms.
:::

The number $73 + j42.5\ \Omega$ is the impedance of the assumed **sinusoid**
at exactly $\lambda/2$, not of the **wire**. The solved current differs from
the sinusoid near the tips and at the feed, and the impedance is read at the
feed, where that difference is largest, so the resistance comes out near
$86\ \Omega$. Both models agree on where the wire resonates: the sinusoid at
about $0.476\lambda$ for this radius, which is where Lesson 7's reactance
curve crosses zero, and the solved current at about $0.473\lambda$. A wire cut
to exactly $\lambda/2$ is therefore about 5% long under either model, which
is why both call it inductive. The $13\ \Omega$ of resistance is the current
shape, not the length; it is the same gap Lesson 7 noted between the model's
$63\ \Omega$ and a real dipole's $70\ \Omega$ at resonance, and trimming
does not remove it.

The difference in current shape has a name, the **end effect**. The assumed
sinusoid goes to zero at the wire tips with a clean slope, while the real
current approaches the tips more gradually because charge accumulates there.
That larger current near the tips is visible in the convergence widget, and it
is what raises the resistance and moves resonance slightly shorter.

```{note}
A useful habit for the rest of the course is this: whenever a simulation and a
hand calculation disagree, first ask whether the two are describing the same
antenna. More often than not they are not, and the disagreement resolves itself
once you make the two models match.
```
::::

::::{frame} Summary
:class: read-only

| Symbol / idea | What it is | Number to remember |
| :-- | :-- | :-- |
| Method of moments | discretize the wire, expand the current in basis functions, enforce $E_{\text{tan}} = 0$, solve for the amplitudes, then integrate | $N$ unknowns, one matrix solve |
| Basis functions | the shapes the current is built from; NEC uses a piece of a sinusoid per segment | $I(z) \approx \sum I_n f_n(z)$ |
| $Z_{\text{in}} = V_{\text{feed}}/I_{\text{feed}}$ | terminal impedance from the one segment carrying the source | 1 V drive makes it $1/I_{\text{feed}}$ |
| Segments $N$ | segmentation of the wire; odd, so a segment sits at the feed | 10–20 per half wavelength |
| $\Delta$ against $\lambda$ | upper bound on segment length, set by phase change | $\Delta < \lambda/20$ |
| $\Delta$ against $a$ | lower bound on segment length, set by the thin-wire kernel | $\Delta > 8a$ |
| Convergence | the answer stops moving under refinement, which is not the same as matching theory | change $< 1\%$ per doubling |
| Average power gain | conservation-of-energy audit on a lossless free-space model | $1.000$, accept 0.95–1.05 |
| $Z_{\text{in}}$ at exactly $\lambda/2$ | inductive because the wire is about 5% long; the resistance is higher because the solved current is not the sinusoid | near $86 + j47\ \Omega$ |
| Resonant length and gain | where $X_{\text{in}} = 0$, and the gain there | $\approx 0.473\lambda$, $2.15\ \text{dBi}$, $78^\circ$ |
::::

::::{frame} Practice
:class: read-only

- <a href="../../practice/ECE444_L08_Practice_blank.pdf" target="_blank" rel="noopener">Problem set (PDF)</a>
- <a href="../../practice/ECE444_L08_Practice_SOLUTIONS.pdf" target="_blank" rel="noopener">Solutions (PDF)</a>
::::

::::{frame} Where This Is Going
:::{present}
- **Lesson 9**: monopoles need a **ground plane**: a new card, and a new way for the model to be wrong.
- **Module 3**: arrays are more wires, and the same rules apply to every element.
- The habit is predict, simulate, reconcile.
:::

Lesson 9 returns to theory with loops and monopoles. The monopole is where your
new NEC habits get their first real test, because a quarter-wave monopole is
only half an antenna and the other half is the ground plane. NEC models ground
with its own card, and getting that card wrong is a common way to produce a
confident and completely incorrect monopole result, including an average gain
that no longer has to equal one. Before Lesson 9, review your Lesson 7 notes on
the sinusoidal current assumption, and be ready to state how a quarter-wave
monopole over perfect ground relates to the half-wave dipole in both impedance
and directivity.

Beyond that, Module 3 is built entirely on arrays, and an array is just more
wires. The segmentation rules you applied to one dipole today apply to every
element at once, and the matrix you solved for 21 unknowns becomes a matrix for
several hundred. The physics does not change and only the bookkeeping grows, so
the habit of predicting before simulating matters more as the models get large
enough that nobody can check the answer by eye.
::::
