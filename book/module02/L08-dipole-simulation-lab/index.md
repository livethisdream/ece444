---
frame_view: true
---

# L8 - Dipole Simulation Lab

::::{frame}
:class: title-frame

<div class="course-mark">ECE 444 · Fall 2026</div>

<h1 class="frame-title">Dipole Simulation Lab</h1>

<div class="title-rule"></div>

A difference you can explain is worth more than an agreement you cannot.

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
  <li>I can explain what the method of moments does — discretize the wire, enforce the boundary condition, solve for the segment currents — and why the simulator then runs the same radiation integral you ran by hand.</li>
  <li>I can build a wire-dipole model with defensible segmentation and excitation, and run frequency sweeps and pattern computations.</li>
  <li>I can compare simulated impedance, resonant length, pattern, and gain against the analytical half-wave-dipole predictions and account for every difference.</li>
  <li>I can recognize when a simulation is misleading me — segmentation too coarse, wire radius unreasonable, source misplaced — and apply the standard convergence and energy checks.</li>
</ol>
::::

::::{frame} Where We Were
:::{present}
- Every number Lesson 7 gave you rests on one assumption: the current is a **sinusoid**.
- Today a solver computes that current instead of assuming it.
- Then you reconcile the two answers. **That reconciliation is the lab.**
:::

Lesson 7 supplied the current by assumption,
$I(z) = I_m \sin\left(k\left(\frac{L}{2} - \vert z \vert\right)\right)$, and
everything else followed from it — the pattern, the beamwidth, the
$73 + j42.5\ \Omega$ at the terminals. A difference you can explain is worth
more than an agreement you cannot, so the deliverable today is not a matching
number. It is an account of every place the two answers part company.
::::

::::{frame} What the Solver Does
:::{present}
The **method of moments** removes the assumption in three steps.

1. **Discretize.** Chop the wire into $N$ segments, each carrying one unknown current.
2. **Enforce.** $E_z^{\text{scattered}} = -E_z^{\text{source}}$, one equation per segment.
3. **Solve.** One complex matrix solve.
:::

You now have $N$ unknown numbers instead of an unknown function. The solver
then evaluates the radiation integral from Lesson 6 over that numerical
current rather than over an analytical one — the same integral you ran by
hand, fed a current nobody guessed.
::::

::::{frame} A Simulator Knows No More Physics Than You Do
:::{present}
:class: callout
It solves for the current you would otherwise have guessed, then computes the
same integral you would have computed. Everything it reports is only as
trustworthy as the segments, the wire radius, and the source you handed it.
:::

That sentence is the reason this lesson spends as long on the rules bounding
the model as it does on the model itself. Nothing in the output file announces
that the input was wrong.
::::

::::{frame} NEC and Its Front Ends
:::{present}
- **NEC** is the method of moments specialized to thin wires.
- It has no interface: it reads a text file of **cards** and writes one of results.
- Everything else is a front end. **The cards are what we teach.**
:::

Ours is **nec_lab**, written for this course; 4nec2 is the free Windows one you
will meet in the field. Both send NEC the same cards, and cards do not move
between versions the way menu items do.
::::

::::{frame} From Currents to One Impedance
:::{present}
$$Z_{\text{in}} = \frac{V_{\text{feed}}}{I_{\text{feed}}}$$

- The solve returns $N$ currents. Impedance uses **one**.
- At 1 V, it is the reciprocal of the feed current.
:::
:::{present}
- Its error becomes the antenna's.
- The rest of the current sets the **pattern**.
- A misplaced source wrecks $Z_{\text{in}}$, not the pattern.
:::

A feed current lagging the applied voltage gives a positive reactance, which
means an inductive terminal — the complex character carries straight through
the division. That third consequence is a failure mode you will meet later in
the lab, and it is hard to spot precisely because the pattern still looks
right.
::::

::::{frame} Convergence
:class: viz-frame

:::{present}
<iframe src="../../viz/mom-dipole.html"
        width="100%" height="453"
        style="border: 1px solid #cddce9; border-radius: 6px;"
        loading="lazy"
        title="Method-of-moments dipole: solved segment currents against the assumed sinusoid, the feed voltage and current that set the input impedance, and impedance versus segment count">
</iframe>
:::

:::{depth}
The widget runs a method-of-moments solve in your browser using a thin wire,
triangle basis functions, and a voltage source on the center segment. Drag the
segment count up from 5 and watch two things at once. The current samples
settle onto the sinusoid, staying close to it but never matching it exactly,
and running fattest near the wire ends where the sinusoid is least accurate. At
the same time $Z_{\text{in}}$ stops moving, and that plateau is what
"converged" means: it does not mean the answer agrees with theory, only that
refining the model no longer changes it. Watch the feed readouts as you drag,
since $V_{\text{feed}}$ is fixed while $I_{\text{feed}}$ moves, and every
change in $Z_{\text{in}}$ comes from that one current — the red band on the
wire plot, where the source sits. The dashed green references are Lesson 7's
$73\ \Omega$ and $42.5\ \Omega$, drawn when the wire is exactly $\lambda/2$
long, and the plateau lands near them rather than on them. The last part of
this lesson explains that gap.
:::
::::

::::{frame} The Rules That Bound the Model
:::{present}
| Rule | Reason | If you break it |
| :-- | :-- | :-- |
| 10–20 segments per $\lambda/2$ | resolve the current | pattern smeared |
| $\Delta < \lambda/20$ | phase barely changes | impedance drifts |
| $\Delta > 8a$ | thin-wire kernel valid | impedance unreliable |
| $2\pi a \ll \lambda$ | the wire is thin | wrong problem |
| Odd segment count | a segment at the center | source lands off-center |
:::

NEC does not know about antennas. It knows about **thin wires**: straight
segments with a length, a radius, and a position. A dipole is one wire with a
segment count; a Yagi is several wires. Here $\Delta$ is the segment length and
$a$ the wire radius.

Notice that two of these rules pull against each other, because refining the
mesh drives $\Delta$ down toward $8a$. On a fat wire you eventually run out of
room, and that limit is informative rather than annoying: it is NEC telling you
the thin-wire approximation does not describe your antenna.
::::

::::{frame} Worked Example — Segmentation Arithmetic for Today's Dipole
:class: read-only

At $f = 915\ \text{MHz}$:

$$\lambda = \frac{3\times10^8}{915\times10^6} = 0.3279\ \text{m} = 328\ \text{mm}, \qquad \frac{\lambda}{2} = 164\ \text{mm}$$

Take a wire of 1 mm diameter, so $a = 0.5\ \text{mm}$, and start with $N = 21$
segments:

$$\Delta = \frac{164\ \text{mm}}{21} = 7.8\ \text{mm} = 0.024\ \lambda$$

Now check both bounds. The upper bound is $\lambda/20 = 16.4\ \text{mm}$, and
$7.8\ \text{mm}$ clears it with room to spare. The lower bound is
$8a = 4.0\ \text{mm}$, and $7.8\ \text{mm}$ clears that as well. The thinness
check also passes, since $2\pi a/\lambda = 0.0096$.

How far can you refine? The segment length may fall to $4.0\ \text{mm}$, which
corresponds to $164/4.0 \approx 41$ segments. **Past about 41 segments this
wire is too fat for the standard kernel, and the extra segments make the answer
worse rather than better.** That refinement ceiling is worth computing before
you touch the keyboard.
::::

::::{frame} The Source Model
:::{present}
- NEC drives **one segment** with a 1 V source. That segment is the terminal.
- No connector, no coaxial gap, no balun exists in the model.
- The feed gap is **one segment wide**, so refining the mesh refines the feed.
:::

Two consequences follow. The source must sit on the center segment, which is
why the segment count is odd. And gain — an integral over the entire current —
settles quickly, while impedance, read from one segment, settles last. Expect
your convergence study to show exactly that.
::::

::::{frame} The Average Gain Test
:::{present}
- Ask for a **full sphere** and NEC reports average power gain.
- Lossless, in free space, it **must be 1.000**.
- An energy audit, for one extra run.
:::
:::{present}
:class: callout
0.6 or 1.4 means **no other number in the file can be trusted**.
:::

Look for the geometry error, the segment-length violation, or the misplaced
source before you record a single number. The test is only valid over a
complete sphere in free space; adding a ground plane changes the expected
value, which is worth remembering when you model a monopole in Lesson 12.
::::

::::{frame} Getting to the Tool
:::{present}
**nec_lab** runs in a browser, two ways — your instructor will say which:

- **A shared copy.** Open the address given in class. Nothing to install.
- **Your own copy.** `python scripts/nec_lab/run.py serve`, or double-click `nec_lab.bat` on Windows.
:::

Either way the page is the same, and so are your answers. The page has a form
at the left and a **NEC input file** at the bottom right: the form writes that
file, and the file is what NEC runs.

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
2. **Do the arithmetic.** $\Delta$ against $\lambda/20$ and $8a$, on paper.
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
One short report:

1. **The comparison table**, percent difference on every row.
2. **A paragraph per row** naming the mechanism.
3. **Your convergence table**, and the segment count you would ship.
4. **The average gain figure.**
:::
::::

::::{frame} The Comparison Table
:::{present}
| Quantity | L7 analytical | Simulated | Why |
| :-- | :-- | :-- | :-- |
| $Z_{\text{in}}$ at exactly $\lambda/2$ | $73 + j42.5\ \Omega$ | | |
| Resonant length | $0.47\text{–}0.48\ \lambda$ | | |
| $R_{\text{in}}$ at resonance | $\approx 70\ \Omega$ | | |
| Gain | $2.15\ \text{dBi}$ | | |
| E-plane HPBW | $78^\circ$ | | |
:::

Four of those rows should land within a few percent. The first will not, and
the mechanism behind it is worth stating here rather than leaving you to
discover it by accident.
::::

::::{frame} Why the Half-Wave Number Misses
:::{present}
- $73 + j42.5\ \Omega$ is the impedance of a **sinusoid**, not a **wire**.
- A sinusoid resonates at $0.486\lambda$; this wire at $0.473\lambda$.
- Cut to $\lambda/2$ it is 5% long, so inductive.
:::
:::{present}
:class: callout
Expect near $86 + j47\ \Omega$. Not a 17% error in NEC — two different
antennas.
:::

A real wire has finite radius and stores energy in the near field around it, so
it resonates shorter. Step 6 trims the wire to resonance, and once you do, the
two answers agree to within a couple of ohms.
::::

::::{frame} The End Effect
:::{present}
- The assumed sinusoid goes to zero at the tips with a clean slope.
- The real current approaches the tips **gradually**, because charge accumulates there.
- That fattened tip current is what pushes resonance shorter and resistance higher.
:::

You already watched it happen: it is the visible discrepancy between the solved
current and the dashed sinusoid in the convergence widget earlier.

:::{depth}
A useful habit for the rest of the course is this: whenever a simulation and a
hand calculation disagree, first ask whether the two are describing the same
antenna. More often than not they are not, and the disagreement resolves itself
once you make the two models match.
:::
::::

::::{frame} Summary
:class: read-only

| Symbol / idea | What it is | Number to remember |
| :-- | :-- | :-- |
| Method of moments | discretize the wire, enforce $E_{\text{tan}} = 0$, solve, then integrate | $N$ unknowns, one matrix solve |
| $Z_{\text{in}} = V_{\text{feed}}/I_{\text{feed}}$ | terminal impedance from the one segment carrying the source | 1 V drive makes it $1/I_{\text{feed}}$ |
| Segments $N$ | segmentation of the wire; odd, so a segment sits at the feed | 10–20 per half wavelength |
| $\Delta$ against $\lambda$ | upper bound on segment length, set by phase change | $\Delta < \lambda/20$ |
| $\Delta$ against $a$ | lower bound on segment length, set by the thin-wire kernel | $\Delta > 8a$ |
| Convergence | the answer stops moving under refinement, which is not the same as matching theory | change $< 1\%$ per doubling |
| Average power gain | conservation-of-energy audit on a lossless free-space model | $1.000$, accept 0.95–1.05 |
| $Z_{\text{in}}$ at exactly $\lambda/2$ | the wire is about 5% long, so it is inductive | near $86 + j47\ \Omega$ |
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
