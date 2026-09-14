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
  <li>I can build a wire-dipole model with defensible segmentation and excitation, and run frequency sweeps and pattern computations.</li>
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

::::{frame} NEC and Its Front Ends
:::{present}
- **NEC**: the Numerical Electromagnetics Code, 1970s.
- It knows **thin wires**: segments with a length, a radius, and a position.
- It reads **cards** from a text file; everything else is a front end.
- Ours is **nec_lab**; in the field, 4nec2.
:::

NEC — *Numerical Electromagnetics Code*, written at Lawrence Livermore in the
1970s and still the workhorse of wire-antenna modeling — is this method
specialized to thin wires. It has no interface of its own: it reads a text
file of cards and writes a text file of results, and every front end writes
the same cards. Ours is **nec_lab**, written for this course and served from
the course site; 4nec2 is the free Windows front end you will meet in the
field. The cards do not move between versions the way menu items do, so the
cards are what we teach.

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

NEC drives **one segment** with a 1 V source, and that segment is the antenna
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
sphere in free space; adding a ground plane changes the expected value, which is
worth remembering when you model a monopole in Lesson 12.
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

::::{frame} Getting to the Tool
:::{present}
**nec_lab** runs in your browser:

- **On the course site.** Open <a href="../../simulator/" target="_blank" rel="noopener">Simulator</a>. Nothing to install.
- **Or a copy your instructor is serving** — the address is given in class.
:::

Every route runs the same tool and gives the same answers. The page has a form
at the left and a **NEC input file** at the bottom right: the form writes that
file, and the file is what NEC runs.

:::{depth}
The course-site version downloads about 6 MB the first time — NEC-2 and Python,
both compiled for the browser — and is cached afterwards, so it opens at once
and works with no network at all. Nothing you build there leaves your machine.

You can also run it yourself from a clone of the course repository:
`python scripts/nec_lab/run.py serve`, or double-click
`scripts\nec_lab\nec_lab.bat` on Windows.
:::

:::{depth}
Type the cards yourself at least once, because they are the real interface.
They are identical in nec_lab, 4nec2 and every other front end you will meet,
and they do not move between versions the way menu items do. The **Copy**
button under the deck puts the cards on your clipboard; they will run unchanged
in 4nec2 if you would rather work there, or want to check one tool against the
other.
:::
::::

::::{frame} The NEC Input File
:::{present}
Four cards carry the model.

```text
GW 1 21 0 0 -0.08197 0 0 0.08197 0.0005
EX 0 1 11 0 1 0
FR 0 1 0 0 915 0
RP 0 181 1 1000 0 0 1 0
```
:::

Choose **Dipole** in the antenna picker and press **Build & solve**, and the
full deck is what appears. Read it before you read the plots, and type it out
once by hand into the editor to prove you can:

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

`CM` and `CE` open the comment block, `GE 0` closes the geometry in free space,
and `EN` ends the deck.

:::{depth}
**Build & solve** runs what the form describes; **Run these cards** runs what is
in the editor, which is how you run a deck you typed or changed yourself.
Either way the answers land in the same places: $Z_{\text{in}}$, VSWR, peak
gain, HPBW and the average power gain across the top, the pattern cuts below
them, and the segmentation rules down the left. Beside the editor, every field
of every card is labeled — hover one to see what it means.

This handout names cards, not buttons. Cards are the part that does not change:
if a control moves, or you end up in 4nec2 instead, the deck still says exactly
what the model is.
:::
::::

::::{frame} Reading the Cards
:::{present}
| Card | What it says |
| :-- | :-- |
| `GW` | wire 1, 21 segments, $\pm 81.97\ \text{mm}$, radius $0.5\ \text{mm}$ |
| `GE 0` | free space |
| `EX` | 1 V source, segment 11 of 21 |
| `FR` | one frequency, 915 MHz |
| `RP` | $\theta$ swept, $1^\circ$ steps |
:::

All coordinates are in meters. The wire lies along $z$, matching the course
convention, so broadside is $\theta = 90^\circ$ and the pattern cut above is
the E-plane.
::::

::::{frame} When the Tool Disagrees With You
:::{present}
:class: callout
The rules panel and the average-gain readout both warn you. **Neither stops a
run.** NEC will solve a broken model and report the result with the same
confidence it reports a good one.
:::

That is the whole point of the segmentation rules: **you** are the check. The
tool can tell you that a number looks wrong; it cannot tell you that a model
describes the antenna you meant to build.
::::

::::{frame} Procedure — Predict, Then Run
:::{present}
1. **Predict.** Lesson 7's $Z_{\text{in}}$, resonant length, gain, and HPBW.
2. **Do the math.** $\Delta$ against $\lambda/20$ and $8a$, on paper.
3. **Baseline run.** 915 MHz. Record the differences before changing anything.
:::

A prediction written after the fact teaches you nothing, so step 1 is not
optional and it is not a formality. Your reference numbers should not change
once you see the simulated values.
::::

::::{frame} Procedure — Audit the Model
:::{present}
4. Tick **average power gain**, or request a full sphere yourself:

```text
RP 0 19 36 1001 0 0 10 10
```

**If it is not close to 1.000, stop and fix the model.**
:::

That request sweeps $\theta$ from $0^\circ$ to $180^\circ$ in $10^\circ$ steps
and $\phi$ from $0^\circ$ to $350^\circ$ in $10^\circ$ steps, and the final
digit of the fourth field is what asks for the average gain. Record the value —
it is a deliverable, and it is the one number that licenses all the others.
::::

::::{frame} Procedure — Sweep, Then Trim
:::{present}
5. `FR 0 41 0 0 800 5` sweeps 800 to 1000 MHz. Read off where $X_{\text{in}} = 0$.
6. Hold 915 MHz and shorten the wire until $X_{\text{in}}$ crosses zero.
:::

A wire cut to $\lambda/2$ at 915 MHz will not resonate at 915 MHz, so determine
where it does and by how much it misses. Then record the resonant length as a
fraction of $\lambda$ and the resistance there, keeping the segment count odd
throughout and rechecking $\Delta$ against $8a$ after each change.

:::{depth}
**Trim to resonance** does this search for you, and you should not press it
until you have done it by hand. Then press it: if your length and the tool's
agree, you have learned something about both. If they do not, one of you missed
the reactance crossing.
:::
::::

::::{frame} Procedure — Cuts and Convergence
:::{present}
7. At resonance take the E-plane cut and the H-plane cut:

```text
RP 0 1 361 1000 90 0 0 1
```

8. Re-run at $N = 11$, 21, 41, 81 and tabulate $Z_{\text{in}}$ and gain.
:::

Record the peak gain, the E-plane HPBW, and the depth of the nulls along the
wire axis, and confirm the H-plane cut is a circle to within a small fraction
of a decibel. In the convergence study, identify both the point where the
answer stops moving and the point where the $\Delta > 8a$ rule begins to bite.
::::

::::{frame} Keep the Pattern File
:::{present}
- Press **Pattern CSV** and keep what it saves.
- In Lesson 11 it drops straight onto your measured cut, on one plot.
- This file is absolute **dBi**; a chamber measures raw $S_{21}$.
:::

Comparing the two means normalizing each to its own peak, which compares
*shape*. Comparing absolute levels is a gain-transfer measurement against a
standard-gain horn — Lesson 9's material, not something a file can fix. Save it
somewhere you will find it in three lessons' time.
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
will put on the range in Lessons 10 and 11. The project handout governs what
that section must contain; this is how to build it.

1. **Pattern.** Predict the E-plane and H-plane cuts, and read the half-power
   beamwidth, the sidelobe level, and the gain from them.
2. **Impedance.** Predict $Z_{\text{in}}$ and VSWR across the band you will
   measure, and the resonant frequency.
3. **Checks.** Run the average-gain test before recording anything, and show a
   convergence table so the reader knows the numbers have stopped moving.
4. **Comparison.** Set the simulation beside your hand analysis and account
   for every difference. "Simulation error" is not an account of anything, so
   name the mechanism. When the measurement comes in at Lesson 11 you will add
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
- You have predicted an antenna and simulated it. You have not **measured** it.
- A simulation nobody has checked against hardware is a very confident opinion.
- **Lesson 9** is the theory of checking; **L10 and L11** put you on the instruments.
:::

The dipole you modeled today is the antenna you will hang on the analyzer next
week, so keep your predicted impedance and resonant length where you can find
them. Lesson 9 also introduces the midterm project, an antenna pattern
measurement due at Lesson 20 — the measurement block runs early for that
reason.

:::{depth}
The remaining antenna families come back at Lessons 12 to 14 — loops and
monopoles, then patches, slots and horns, then reflectors and Yagis. The
monopole is where your new NEC habits get their first real test, because a
quarter-wave monopole is only half an antenna and the other half is the ground
plane. NEC models ground with its own card, and getting that card wrong is a
common way to produce a confident and completely incorrect result, including an
average gain that no longer has to equal one.

Beyond that, Module 3 is built entirely on arrays, and an array is just more
wires. The segmentation rules you applied to one dipole today apply to every
element at once, and the matrix you solved for 21 unknowns becomes a matrix for
several hundred. The physics does not change and only the bookkeeping grows, so
the habit of predicting before simulating matters more as the models get large
enough that nobody can check the answer by eye.
:::
::::
