# L28 - Null Steering Lab

:::{admonition} Slides
:class: slides
<a href="../../slides/L28-null-steering-lab.html" target="_blank" rel="noopener">html slides</a>
<a href="../../slides/L28-null-steering-lab.html?print-pdf" target="_blank" rel="noopener">pdf slides</a>
<a href="../../slides/L28-null-steering-lab.md" target="_blank" rel="noopener">raw markdown slides</a>
:::

## Learning Objectives

<ol class="lo-list lo-sublist" style="--module: '3'; --lo: '9'; counter-reset: lo 4">
  <li>I can implement computed null-steering weights on the PHASER and measure the resulting notch.</li>
  <li>I can place a boresight null by subtracting the two digital subarray channels.</li>
  <li>I can run the MVDR adaptive beamformer and interpret the weights it chooses against an interferer.</li>
  <li>I can compare manual null steering with adaptive beamforming and state where each wins.</li>
</ol>

Lesson 27 ended with a weight vector on paper: eight complex numbers that hold the
beam on the target and put a pattern null on the jammer. Today you type those
numbers into the array and find out what the hardware gives back. You will run
three procedures, in increasing order of how much the array does for itself — a
static notch you compute yourself, a boresight null you get for free by
subtracting the two digital channels, and an adaptive beamformer that finds its
own null from the received data. The three together are the whole null-steering
toolbox, and the last one is the capstone problem in miniature.

## Part 1: What Lesson 27 computed

The **weight-subtraction** result from Lesson 27 is one line. Start from the
weights that steer the beam where you want it, $w_d$, and the weights that would
steer it at the interferer, $w_n$, and remove the part of the first that points
along the second:

$$w = w_d - r_n w_n, \qquad r_n = \frac{w_n^H w_d}{w_n^H w_n}$$

The subtraction guarantees $w^H w_n = 0$, which is exactly the statement that the
array has no response in the direction of $w_n$. Everything else about the
pattern — where the main lobe sits, what the sidelobes do — is whatever falls out.

The course example holds the beam at broadside and nulls a jammer at
$\theta_1 = +22.5^\circ$, one first-sidelobe width off the beam. Converting the
resulting complex weights to what the GUI accepts — element gain as a percentage
of the largest, $100\vert w_n\vert/\max\vert w\vert$, and phase offset as
$\angle w_n$ — gives the eight settings you will enter.

| Element | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 |
| :-- | --: | --: | --: | --: | --: | --: | --: | --: |
| Gain (%) | 75 | 65 | 82 | 100 | 100 | 82 | 65 | 75 |
| Phase (deg) | $-12.1$ | $+3.1$ | $+13.0$ | $+6.0$ | $-6.0$ | $-13.0$ | $-3.1$ | $+12.1$ |

<img src="../../viz/img/L28-element-settings.svg"
     alt="The eight element gains and phase offsets for a null at +22.5 degrees"
     style="max-width: 700px; width: 100%; display: block; margin: 1em auto;">

Read the amplitudes first. They are symmetric about the array centre but not
monotonic — element 2 is quieter than element 1 — so this is no taper you would
have reached for. The phases are antisymmetric, equal and opposite across the
centre. Neither column means much on its own. The eight numbers together are one
vector, and only the vector nulls anything.

Three predictions come with the settings, and you will check all three:

- the notch at $+22.5^\circ$ reaches about $-21.6$ dBc, against a uniform
  reference sidelobe of $-12.8$ dBc at the same angle;
- the main lobe pays about $1.8$ dB for it;
- the notch bottoms out at roughly $-21$ dB rather than going to zero, because
  the ADAR1000 phase shifter quantizes to $2.8125^\circ$ and its gain control to
  about $1\%$ steps.

There is a second null available on this board that costs no computation at all.
Each ADAR1000 sums its four elements into one RF channel, so the PHASER hands the
Pluto two **digital subarray channels**, one for elements 1-4 and one for
elements 5-8. Adding them is the ordinary sum beam. Subtracting them — setting
Beam 1 Phase to $180^\circ$ — puts a null on boresight with twin peaks near
$\pm 11^\circ$, about $-22$ dBc deep. That is the **monopulse difference beam**,
and Module 4 uses it for angle tracking.

:::{admonition} Key Point
:class: key-concept
A computed null and a structural null are different animals. The
$+22.5^\circ$ notch exists because you solved for eight weights, and it moves
only when you solve again. The boresight null exists because two identical
subarrays are being subtracted, and it sits at boresight no matter what the
signal does.
:::

## Part 2: Equipment and setup

| Item | Note |
| :-- | :-- |
| ADALM-PHASER (CN0566) + Raspberry Pi + ADALM-Pluto | powered, on the lab network |
| HB100 Doppler module | the target source, on boresight, at least $2\ \text{m}$ out |
| Second HB100 or X-band source | procedure C only; see the note there |
| Course Phaser GUI | `http://phaser.local:8080` in a browser |

Bring the array up the way every Module 3 lab starts. Set Signal Freq to the
HB100's measured frequency near $10.525\ \text{GHz}$, run **Calibrate**, and
confirm on the **Rectangular** tab that a uniform sweep gives a single peak
within a degree or two of $0^\circ$ with a first sidelobe near $-13$ dBc. If the
peak is off boresight or the sidelobes are lopsided, the calibration did not take
and nothing measured afterwards is worth recording.

Two controls carry this lab. **Start** runs the beam sweep, stepping the
commanded steer angle across the field of view and recording received power at
each step; the $x$ axis is the commanded angle, not a measured arrival angle.
**Freeze** holds the current trace as a reference so a later sweep is drawn on
top of it. Every measurement below is a comparison against a frozen trace.

## Part 3: Procedure A — the static notch

1. With the array uniform (Element Gains at $100\%$, Phase Control reset), press
   **Start**, then **Freeze**. This is your reference. Record the peak level and
   the level of the sidelobe nearest $+22.5^\circ$; it should be about
   $-12.8$ dBc.
2. Enter the eight percentages from Part 1 into **Element Gains** (Rx1 through
   Rx8). This set is symmetric about the array centre, so **Enforce Symmetric
   Taper** makes no difference to it; leave the switch off so that a later edit to
   one slider is not mirrored onto its partner.
3. Enter the eight phase offsets from Part 1 into **Phase Control**. Keep the
   signs; a sign error moves the notch to $-22.5^\circ$.
4. Press **Start** and read the new trace against the frozen one.

<img src="../../viz/img/L28-sweep-notch.svg"
     alt="Uniform reference sweep and null-steered sweep, with the notch at +22.5 degrees"
     style="max-width: 700px; width: 100%; display: block; margin: 1em auto;">

Three numbers come off this plot. The sidelobe at $+22.5^\circ$ has dropped from
$-12.8$ dBc to about $-21.6$ dBc, a change of roughly $9$ dB at that angle. The
main lobe has lost about $1.8$ dB to the subtraction, which matches Lesson 27's
cost curve for a null this close to the beam. And the rest of
the pattern has moved: the sidelobes on the far side are one to two decibels
different from the reference, because the subtraction reshaped the whole aperture
distribution, not just one angle.

Now ask why the notch stopped at $-21.6$ dBc when the arithmetic in Lesson 27
predicted a true zero. Two hardware limits set the floor, and both were named in
Lesson 26:

- The phase shifter has a $2.8125^\circ$ LSB, so a commanded $+13.0^\circ$ is
  applied as $+14.06^\circ$. The eight weights are each a little wrong, and the
  cancellation they were designed to produce is correspondingly incomplete.
- The gain control moves in steps of about $1\%$, which perturbs the amplitudes
  the same way.

A rounded weight vector is still a weight vector — it just nulls a slightly
different direction, a degree or two off where you asked. On top of that, the
sweep's own noise floor sits near $-22$ dBc, so even a perfect notch would read
no deeper than the floor. This is the general rule for a real array: **null depth
is set by weight accuracy, not by the null-steering algorithm**, and roughly
$20\text{-}22$ dB is what $2.8^\circ$ phase resolution buys you.

Before moving on, press **Reset** in Phase Control and return Element Gains to
Uniform.

## Part 4: Procedure B — the digital difference null

1. Open **Digital Beam Forming** and set Mode to **Manual**.
2. Leave Beam 0 Gain and Phase alone. Set **Beam 1 Phase** to $180^\circ$.
3. Press **Start**.

<img src="../../viz/img/L28-delta-beam.svg"
     alt="Sum and difference beams from the two digital channels"
     style="max-width: 700px; width: 100%; display: block; margin: 1em auto;">

The peak that was at boresight is now a null about $-22$ dBc deep, with two lobes
of nearly equal height near $\pm 11^\circ$. Nothing in the analog beamformers
changed — all eight elements still carry the same phases they had a moment ago.
The only change is a sign on one of the two digital channels, applied after the
signal was digitized, and it is enough to cancel the two subarray outputs against
each other on boresight.

Record the null depth and the two peak angles. This is the monopulse difference
beam: the sum beam tells you a target is there, the difference beam tells you
which side of boresight it is on, and Module 4 turns the ratio of the two into an
angle estimate accurate to a small fraction of a beamwidth. Set Beam 1 Phase back
to $0^\circ$ before continuing.

## Part 5: Procedure C — adaptive nulling with MVDR

Procedures A and B both required you to know something in advance: the jammer's
angle in A, the array's symmetry in B. The **MVDR** beamformer requires neither.
It estimates the covariance of what the two channels are actually receiving,
$\hat R = \frac{1}{K} X X^H$ over $K$ snapshots, and solves

$$w_{\text{mvdr}} = \frac{R^{-1}s}{s^H R^{-1} s}$$

for the weights that minimize total output power subject to holding unit gain in
the look direction $s$. Whatever is loud and is not in the look direction gets a
null, and the beamformer never has to be told where it is.

1. Set **Digital Beam Forming** Mode to **MVDR**. Set Snapshots to $128$ and
   Diagonal Load to $0.001$. The look direction is the current **Steer Angle**,
   so leave it at $0^\circ$.
2. Press **Start** with only the boresight HB100 running. The pattern keeps its
   main lobe on boresight and looks much like the manual sum beam. With nothing
   to reject, MVDR has nothing to do.
3. Introduce a second X-band source off to one side — a second HB100 held at
   roughly $+30^\circ$, and stronger than the target if you can manage it, about
   $10$ dB. Sweep again with Mode set to Manual, then with Mode set to MVDR, and
   compare the two traces.

The manual beamformer is captured by the interferer: with $10$ dB in its favour,
the second source dominates the received power and the trace peaks toward it.
MVDR holds the look direction and pushes its response toward the interferer down
by $17$ to $19$ dB. That difference between the two traces, read at the
interferer's angle, is the measurement.

```{note}
Both HB100s are nominally on the same frequency, so the **FFT** tab cannot show
you two separate tones. The sources are not resolvable in frequency, and a
free-running DRO drifts. The evidence for what MVDR did is the shape of the
sweep trace and the fact that the look-direction peak survives, not a spectrum
plot.
```

```{note}
**No hardware?** Simulation mode (`python phaser_headless.py --sim`) runs
procedures A and B exactly as written — the weights, the notch, and the
difference null are all in the physics model. It carries only one source, fixed
at boresight, so procedure C has no simulated equivalent; your instructor will
run that demonstration.
```

The widget below is the two-channel digital layer on its own, with the analog
subarrays parked at boresight rather than sweeping. Move the interferer to about
$+20^\circ$ and watch MVDR put a null on it while the boresight response stays
within about a decibel of where the manual weights left it. Then move the
interferer out toward $\pm 30^\circ$ and watch the suppression fall away. Two
limits are doing that, and both belong to the architecture rather than to the
algorithm. An interferer near $\pm 30^\circ$ sits in the null of the four-element
analog subarray, so almost none of its power reaches either channel and there is
nothing left for the digital layer to remove. Beyond that, the two channels sit
four elements apart, and their phase difference wraps through a full cycle across
the width of the subarray beam, so a source near $+30^\circ$ presents very nearly
the same channel phase difference as one on boresight. The digital layer can only
work on what the analog layer passes it, and only on directions the two channels
can tell apart. On the bench the analog beam is sweeping rather than parked, so
the number you record there is the gap between the manual and MVDR sweep traces
at the interferer's angle.

<iframe src="../../viz/mvdr-interferer.html"
        width="100%" height="556"
        style="border: 1px solid #cddce9; border-radius: 6px;"
        loading="lazy"
        title="Two-channel MVDR beamformer against an interferer">
</iframe>

## Part 6: Manual against adaptive

| Question | Manual null steering | MVDR |
| :-- | :-- | :-- |
| What must you know first? | the interferer's angle | nothing |
| Interferer moves | recompute and re-enter eight weights | tracks it, sweep by sweep |
| Digital channels needed | none — all eight analog elements | both, and the data behind them |
| Null depth | quantization-limited, about $20\text{-}22$ dB | covariance-limited, $17\text{-}19$ dB here |
| Where it wins | a known, fixed direction; full aperture control | unknown or moving interference |

The two rows in the middle are the trade. Manual null steering has eight degrees
of freedom and can place several nulls at once, but every one of them is your
arithmetic, computed for a geometry you assumed. MVDR has two degrees of freedom
on this board — one constraint and one null — and it finds that null itself, from
data, several times a second. On a larger array with per-element digitization,
adaptive beamforming has both advantages at once; on the PHASER you can see
precisely what the hybrid architecture costs, because the analog sums destroyed
the per-element information before the algorithm ever saw it.

That is the end of Module 3. Module 5's capstone is this lab with the target
moving: track a maneuvering target with the sum and difference beams while an
adaptive null holds a jammer down, which is procedures B and C running at the
same time.

## Part 7: Deliverables

Record and submit the following.

1. **The static notch.** A table with the frozen reference level and the
   null-steered level at $+22.5^\circ$, the depth change between them, and the
   main-lobe peak level before and after. Compare each against the predicted
   $-12.8$ dBc, $-21.6$ dBc, and $1.8$ dB.
2. **The difference null.** Null depth in dBc and the two peak angles, against
   the predicted $-22$ dBc and $\pm 11^\circ$.
3. **MVDR against manual.** From the instructor's demonstration, the response at
   the interferer angle under both modes and the difference between them, plus
   the look-direction level under both.
4. **Two written answers.** (a) Why the measured notch depth is limited by
   quantization rather than by the null-steering computation, with the numbers
   that set the limit. (b) One situation where a computed static null is the
   better choice than MVDR, and one where it is not, with a reason for each.

## Summary

| Idea | What it is | Number to remember |
| :-- | :-- | :-- |
| Weight subtraction | $w = w_d - r_n w_n$, then convert to gain % and phase | main-lobe cost $1.8$ dB for a null at $+22.5^\circ$ |
| Measured notch | what the quantized weights actually produce | $-21.6$ dBc, against a $-12.8$ dBc reference sidelobe |
| Depth limit | phase LSB and gain step, not the algorithm | $2.8125^\circ$ LSB gives $20\text{-}22$ dB |
| Difference beam | Beam 1 Phase $= 180^\circ$ subtracts the two channels | null on boresight, $-22$ dBc, peaks at $\pm 11^\circ$ |
| MVDR | $w = R^{-1}s / (s^H R^{-1} s)$ from $K$ snapshots | $17\text{-}19$ dB suppression, look direction held |
| Degrees of freedom | one constraint plus one null per digital channel pair | 2 channels null 1 interferer |
| Hybrid cost | analog sums discard per-element data | 8 elements, 2 adaptive degrees of freedom |

## Practice

- <a href="../../practice/ECE444_L28_Practice_blank.pdf" target="_blank" rel="noopener">Problem set (PDF)</a>
- <a href="../../practice/ECE444_L28_Practice_SOLUTIONS.pdf" target="_blank" rel="noopener">Solutions (PDF)</a>

## Where this is going

Module 4 begins radar. Lesson 29 derives the radar range equation and asks the
question this module never had to: how much power comes back from a target that
does not transmit anything of its own. Everything Module 3 built — beamwidth,
sidelobes, scan loss, steering — becomes the antenna terms in that equation, and
the array you have been sweeping becomes the front end of a radar.

The difference beam from Part 4 returns first. Monopulse angle tracking forms the
sum and difference beams at the same time and uses their ratio to measure where a
target is inside the beam, far more finely than the beamwidth alone would allow.
Read the radar range equation section of the text before Lesson 29, and bring
your Part 4 numbers; the twin peaks at $\pm 11^\circ$ are the slope that
monopulse tracking rides.
