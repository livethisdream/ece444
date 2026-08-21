# L8 - Dipole Simulation Lab

:::{admonition} Slides
:class: slides
<a href="../../slides/L08-dipole-simulation-lab.html" target="_blank" rel="noopener">html slides</a>
<a href="../../slides/L08-dipole-simulation-lab.html?print-pdf" target="_blank" rel="noopener">pdf slides</a>
<a href="../../slides/L08-dipole-simulation-lab.md" target="_blank" rel="noopener">raw markdown slides</a>
:::

## Learning Objectives

<ol class="lo-list lo-sublist" style="--module: '2'; --lo: '2'">
  <li>I can explain what the method of moments does — discretize the wire, enforce the boundary condition, solve for the segment currents — and why the simulator then runs the same radiation integral you ran by hand.</li>
  <li>I can build a wire-dipole model in 4nec2 with defensible segmentation and excitation, and run frequency sweeps and pattern computations.</li>
  <li>I can compare simulated impedance, resonant length, pattern, and gain against the analytical half-wave-dipole predictions and account for every difference.</li>
  <li>I can recognize when a simulation is lying to me — segmentation too coarse, wire radius unreasonable, source misplaced — and apply the standard convergence and energy checks.</li>
</ol>

Lesson 7 handed you a set of numbers for the half-wave dipole, and every one of
them rests on a single assumption: that the current on the wire is a sinusoid.
Today you hand the same antenna to a solver that refuses to assume anything,
watch it compute the current instead, and reconcile the two answers. The
reconciling is the lesson — a simulation that agrees with you teaches nothing,
and a simulation that disagrees with you teaches everything, provided you can
say *why*.

## Part 1: What the solver actually does

Lesson 6 established the machinery: the far field is the radiation integral over
the current distribution. Give the integral a current and it gives you a
pattern. Lesson 7 supplied the current by assumption —
$I(z) = I_m \sin\left(k\left(\frac{L}{2} - \vert z \vert\right)\right)$ — and
everything followed.

The **method of moments** (MoM) is what you do when you refuse to guess. It is
three steps and a matrix solve:

1. **Discretize.** Chop the wire into $N$ short **segments**. Declare the
   current on each one to be an unknown number. You now have $N$ unknowns
   instead of an unknown function.
2. **Enforce the boundary condition.** On a perfect conductor, the total
   tangential electric field is zero. The total field is the source field plus
   the field radiated by all $N$ segment currents, so at each segment
   $E_z^{\text{scattered}} = -E_z^{\text{source}}$. That is one equation per
   segment.
3. **Solve.** $N$ equations, $N$ unknowns, one complex matrix inversion. Out
   comes the current on every segment — computed, not assumed.

Then the solver runs *your* integral. The radiation integral of L6, evaluated
over the numerical current instead of an analytical one. That is the whole of
it, and it is worth being blunt about the consequence:

:::{admonition} Key Point
:class: key-concept
A simulator knows no more physics than you do. It solves for the current you
would otherwise have had to guess, then computes the same integral you would
have computed. Everything it reports is only as trustworthy as the segments,
the wire radius, and the source you handed it.
:::

NEC — *Numerical Electromagnetics Code*, written at Lawrence Livermore in the
1970s and still the workhorse of wire-antenna modeling — is exactly this,
specialized to thin wires. 4nec2 is a free Windows front end that writes NEC's
input file for you and plots what comes back.

### Watch the current converge

The widget below runs an honest method-of-moments solve in your browser: thin
wire, triangle basis functions, a voltage source on the center segment, no
shortcuts. Drag the segment count from 5 upward and watch two things at once.
The current samples settle onto the sinusoid — close to it, never exactly it,
and fattest near the wire ends where the sinusoid is worst. And $Z_{in}$ stops
moving. **That plateau is what "converged" means.** It does not mean "agrees
with theory"; it means "refining the model no longer changes the answer." The
dashed green references are L7's $73\ \Omega$ and $42.5\ \Omega$, drawn when the
wire is exactly $\lambda/2$ long — note that the plateau lands *near* them, not
*on* them. Part 4 explains that gap.

<iframe src="../../viz/mom-dipole.html"
        width="100%" height="755"
        style="border: 1px solid #cddce9; border-radius: 6px;"
        loading="lazy"
        title="Method-of-moments dipole: solved segment currents against the assumed sinusoid, and input impedance versus segment count">
</iframe>

## Part 2: NEC's world, and the rules that bound it

NEC does not know about antennas. It knows about **thin wires**: straight
segments with a length, a radius, and a position. A dipole is one wire with a
segment count. A Yagi is several. That simplicity is why NEC is fast, and the
rules below are the price.

| Rule | Reason | Consequence of breaking it |
| :-- | :-- | :-- |
| 10–20 segments per half wavelength | resolve the curvature of the current | pattern and gain come out smeared |
| $\Delta < \lambda/20$ | phase barely changes across a segment | impedance drifts with segmentation |
| $\Delta > 8a$ | keeps the thin-wire kernel valid | impedance becomes numerical fiction |
| $2\pi a \ll \lambda$ | the wire is thin compared with a wavelength | NEC is solving the wrong problem |
| Odd segment count | puts a segment at the center | the source lands off-center |

Here $\Delta$ is the segment length and $a$ the wire radius. Notice that two of
these rules pull against each other: refining the mesh drives $\Delta$ down
toward $8a$. On a fat wire you run out of room, and that is not a nuisance —
it is NEC telling you the thin-wire approximation does not describe your
antenna.

:::{admonition} Worked example — segmentation arithmetic for today's dipole
:class: tip
At $f = 915\ \text{MHz}$:

$$\lambda = \frac{3\times10^8}{915\times10^6} = 0.3279\ \text{m} = 328\ \text{mm}, \qquad \frac{\lambda}{2} = 164\ \text{mm}$$

Take a wire of 1 mm diameter, so $a = 0.5\ \text{mm}$, and start with $N = 21$
segments:

$$\Delta = \frac{164\ \text{mm}}{21} = 7.8\ \text{mm} = 0.024\ \lambda$$

Check both bounds. The upper: $\lambda/20 = 16.4\ \text{mm}$, and
$7.8 < 16.4$ — passes with room to spare. The lower: $8a = 4.0\ \text{mm}$, and
$7.8 > 4.0$ — passes. Also $2\pi a/\lambda = 0.0096$, comfortably thin.

How far can you refine? $\Delta$ may fall to $4.0\ \text{mm}$, which is
$164/4.0 \approx 41$ segments. **Past about 41 segments this wire is too fat for
the standard kernel, and the extra segments make the answer worse, not better.**
That number — the refinement ceiling — is worth computing before you touch the
keyboard.
:::

### The source model

4nec2 drives **one segment** with a 1 V source. That segment *is* the antenna
terminal: no connector, no coaxial gap, no balun. Input impedance is read
straight off it as $Z_{in} = 1\ \text{V} / I_{\text{feed}}$.

Two consequences follow. First, the source must sit on the center segment, which
is why the segment count is odd. Second, the "gap" is as wide as a segment, so
refining the mesh quietly refines the feed model along with it. Gain is an
integral over the entire current and settles quickly; impedance is one number
read at one segment and settles last. Expect your convergence study to show
exactly that.

### The Average Gain Test

Ask NEC for a pattern over the **full sphere** and it will report the **average
power gain**. For a lossless antenna in free space that number must be
$1.000$ — every watt in came back out. This is a conservation-of-energy audit
on your model, and it costs one extra run.

```{note}
Read the average gain as: 0.95 to 1.05, fine. 0.6 or 1.4, your model is broken
and nothing else on the page means anything — go find the geometry error, the
segment-length violation, or the misplaced source before you record a single
number. The test only works over a complete sphere in free space; with a ground
plane the expected value changes.
```

## Part 3: Software setup

4nec2 is free and runs on the lab PCs. Everything below is a NEC **input file** —
a stack of two-letter cards. 4nec2 will happily draw the geometry for you, but
type the cards at least once: they are the actual interface, they are identical
across every NEC front end you will ever meet, and they do not move between
versions the way menu items do.

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

Card by card:

| Card | What it says |
| :-- | :-- |
| `GW 1 21 ...` | wire tag 1, 21 segments, from $z = -81.97\ \text{mm}$ to $+81.97\ \text{mm}$, radius $0.5\ \text{mm}$ (all in metres) |
| `GE 0` | geometry complete, free space, no ground |
| `EX 0 1 11 0 1 0` | voltage source, 1 V, on wire 1 segment 11 — the middle of 21 |
| `FR 0 1 0 0 915 0` | one frequency, 915 MHz |
| `RP 0 181 1 1000 ...` | pattern cut: $\theta$ from $0^\circ$ to $180^\circ$ in $1^\circ$ steps at $\phi = 0$ |

The wire lies along $z$, matching the course convention, so broadside is
$\theta = 90^\circ$ and the pattern cut above is the E-plane.

Run it (the Calculate or Generate command; 4nec2 offers it on the toolbar and on
the function keys), then read results in the output-data and pattern windows.
Impedance appears with the source data; gain appears with the pattern.

```{note}
Menu wording drifts between 4nec2 versions, so this handout names *cards*, not
click paths. If you cannot find a control, the input file is always editable
directly, and the run always produces the same output file.
```

## Part 4: Procedure

Work through these in order and record as you go. Predictions before results —
if you write the prediction after seeing the answer, you have learned nothing
and you will be able to tell.

**Step 1 — Predict.** Before running anything, write down what L7 says this
antenna should do: $Z_{in}$, resonant length, gain in dBi, and E-plane HPBW.
These are your reference numbers, and you do not get to change them later.

**Step 2 — Segmentation arithmetic.** Compute $\Delta$, check it against
$\lambda/20$ and $8a$, and compute your refinement ceiling. Do this on paper.

**Step 3 — Baseline run.** Run the file from Part 3 at 915 MHz. Record $Z_{in}$
and the gain. Compare with your prediction *now*, and write down your reaction
before you do anything else.

**Step 4 — Average gain.** Change the pattern request to a full sphere with the
averaging flag on:

```text
RP 0 19 36 1001 0 0 10 10
```

That is $\theta$ over $0^\circ$ to $180^\circ$ in $10^\circ$ steps and $\phi$
over $0^\circ$ to $350^\circ$ in $10^\circ$ steps; the final digit of the fourth
field is what asks for the average gain. Record it. **If it is not close to
1.000, stop and fix the model.**

**Step 5 — Frequency sweep.** Replace the `FR` card with

```text
FR 0 41 0 0 800 5
```

which sweeps 800 to 1000 MHz in 5 MHz steps. Plot $R_{in}$ and $X_{in}$ against
frequency and read off the frequency where $X_{in} = 0$. A wire cut to
$\lambda/2$ at 915 MHz will not resonate at 915 MHz — find out where it does,
and by how much it misses.

**Step 6 — Trim to resonance.** Now hold the frequency at 915 MHz and shorten
the wire instead. Change the `GW` end coordinates in steps of a millimetre or
two until $X_{in}$ crosses zero. Record the resonant length as a fraction of
$\lambda$ and the resistance there. Keep the segment count odd throughout, and
recheck $\Delta$ against $8a$ after each change.

**Step 7 — Pattern cuts.** At the resonant length, take the E-plane cut
($\phi = 0$, $\theta$ swept) and the H-plane cut ($\theta = 90^\circ$, $\phi$
swept):

```text
RP 0 1 361 1000 90 0 0 1
```

Record the peak gain, the HPBW in the E-plane, and the depth of the nulls along
the wire axis. Confirm the H-plane is a circle to within a small fraction of a
decibel.

**Step 8 — Convergence study.** Re-run the resonant model at $N = 11$, 21, 41,
and 81 segments. Tabulate $Z_{in}$ and gain for each. Identify where the answer
stops moving, and where the $\Delta > 8a$ rule starts to bite.

## Part 5: Deliverables

Turn in a single short report containing:

1. **The comparison table** below, filled in, with a percent difference on every
   row.
2. **One paragraph per row** accounting for the difference. "Simulation error"
   is not an account of anything. Name the mechanism.
3. **Your convergence table** from Step 8, plus one sentence defending the
   segment count you would use if this were a real design.
4. **The average gain figure** from Step 4.

| Quantity | L7 analytical | Simulated | Difference | Why |
| :-- | :-- | :-- | :-- | :-- |
| $Z_{in}$ at exactly $\lambda/2$ | $73 + j42.5\ \Omega$ | | | |
| Resonant length | $0.47\text{–}0.48\ \lambda$ | | | |
| $R_{in}$ at resonance | $\approx 70\ \Omega$ | | | |
| Gain | $2.15\ \text{dBi}$ | | | |
| E-plane HPBW | $78^\circ$ | | | |

Two of those rows will land within a couple of percent. One will not, and it is
the first one — so here is the mechanism, since arguing about it is more useful
than discovering it by accident.

The number $73 + j42.5\ \Omega$ is the impedance of a **sinusoid**, not of a
**wire**. A sinusoidal current resonates when the wire is about $0.486\lambda$
long. A real wire has finite radius, stores energy in the near field around
that radius, and resonates shorter — near $0.473\lambda$ for the wire you are
modeling today. A wire cut to exactly $\lambda/2$ is therefore already about 5%
*long*: inductive, with a resistance well up the curve. Expect something near
$86 + j47\ \Omega$ from the simulator, which is not a 17% error in NEC. It is
two different antennas being compared. Trim to resonance and the two answers
agree to a couple of ohms — that is Step 6, and it is the point of Step 6.

The second mechanism worth naming is the **end effect**. The assumed sinusoid
goes to zero at the wire tips with a clean slope; the real current does not
quite, because charge piles up at the ends. That fattened current near the tips
is visible in the widget in Part 1, and it is what pushes resonance shorter and
resistance higher.

```{note}
A useful habit for the rest of the course: whenever a simulation and a hand
calculation disagree, first ask whether they are describing the same antenna.
More often than not they are not, and the disagreement evaporates once you make
them match.
```

## Summary

| Idea | What to hold on to |
| :-- | :-- |
| Method of moments | discretize the wire, enforce $E_{\text{tan}} = 0$, solve for segment currents, then integrate |
| Segments $N$ | 10–20 per half wavelength; odd, so the source lands at the center |
| $\Delta$ vs $\lambda$ | keep $\Delta < \lambda/20$ or impedance drifts |
| $\Delta$ vs $a$ | keep $\Delta > 8a$ or the thin-wire kernel fails |
| Converged | the answer stops moving under refinement — not "matches theory" |
| Average gain | must be $1.000$ for a lossless free-space model; it is an energy audit |
| $Z_{in}$ at $\lambda/2$ | near $86 + j47\ \Omega$, not $73 + j42.5\ \Omega$ — the wire is 5% long |
| Resonance | about $0.473\lambda$ for a $0.0015\lambda$-radius wire; fatter wire resonates shorter |
| Gain and HPBW | converge fast and match theory: $\approx 2.15\ \text{dBi}$, $78^\circ$ |

## Practice

- <a href="../../practice/ECE444_L08_Practice_blank.pdf" target="_blank" rel="noopener">Problem set (PDF)</a>
- <a href="../../practice/ECE444_L08_Practice_SOLUTIONS.pdf" target="_blank" rel="noopener">Solutions (PDF)</a>

## Where this is going

Lesson 9 returns to theory with loops and monopoles. The monopole is where your
new NEC habits get their first real test: a quarter-wave monopole is only half
an antenna, and the other half is the ground plane. NEC models ground with its
own card, and getting it wrong is the single most common way to produce a
beautiful, confident, completely wrong monopole result — including an average
gain that no longer has to equal one.

Beyond that, everything in Module 3 is arrays, and an array is just more wires.
The segmentation rules you applied to one dipole today apply simultaneously to
every element, and the matrix you inverted for 21 unknowns becomes a matrix for
several hundred. The physics does not change. Only the bookkeeping does — and
the habit of predicting before simulating matters more, not less, as the models
get big enough that nobody can eyeball the answer.
