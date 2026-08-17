<!-- .slide: class="title-slide" -->

<div class="title-left">

# ECE 444

Antennas, Phased Arrays, and Radar Systems

## Lesson 13 — Measurement Lab 1 — Impedance and S-parameters

Fall 2026 · Dr. Neil Rogers

</div>

<div class="title-right">

![USAFA](./img/01-course-intro/USAFA-logo.png)

</div>

---

## Where we were

- **L4** gave you $\Gamma$, VSWR, return loss, and the $-10$ dB convention — all on paper.
- **L7** predicted a half-wave dipole at $73 + j42.5\ \Omega$, resonant slightly short of $\lambda/2$.
- **L12** set up measurement theory from the *radiated* side: ranges, far field, pattern cuts.

**Today is the other terminal. One port, one cable, one number that tells you whether the antenna will accept power at all.**

Note:
Frame the two labs as a pair: L13 is what happens at the connector, L14 is what happens in the air. Remind them the L7 prediction is about to be checked against hardware.

---

## Today's plan

1. What a VNA actually measures — incident and reflected waves, ratioed.
2. Calibration: teaching the instrument where zero is.
3. Reading $S_{11}$: resonance, impedance, $-10$ dB bandwidth.
4. The same resonance on the Smith chart.
5. Bench work: cal, verify, measure, perturb.
6. What to turn in.

Note:
Budget: about 20 minutes of briefing, then everyone on hardware. The perturbation step is the one they will remember, so protect time for it.

---

## A VNA is a ratio meter

- A source sweeps frequency. **Directional couplers** split off the wave going out and the wave coming back.
- Two receivers measure both, in magnitude *and* phase — the instrument reports their **ratio**.
- It never measures impedance. It measures a reflection and computes everything else from it.

<div class="fig" data-inline-svg="./fig/L13-vna-block.svg" style="max-width:830px; margin:0.2em auto 0;"></div>

Note:
Stress "ratioed": because both waves ride the same source, source drift cancels in the ratio. That is why a pocket-sized NanoVNA can be trusted at all.

---

## The one definition

Call the wave leaving port 1 $a_1$ and the wave returning $b_1$.

$$S_{11} = \frac{b_1}{a_1} \quad \text{(magnitude and phase)}$$

For a one-port device — an antenna — that ratio *is* the reflection coefficient at the reference plane:

$$S_{11} = \Gamma$$

<div class="callout">
One port, one complex number per frequency. Everything the VNA tells you today is a re-dress of <strong>that</strong>.
</div>

Note:
Emphasize complex. Students who remember only |S11| will misread the Smith chart later.

---

## Four names for the same number

| You want | From $\Gamma$ | At $\vert\Gamma\vert = 0.316$ |
| :-- | :-- | :-- |
| Return loss | $-20\log_{10}\vert\Gamma\vert$ | $10$ dB |
| $\vert S_{11}\vert$ in dB | $20\log_{10}\vert\Gamma\vert$ | $-10$ dB |
| VSWR | $(1+\vert\Gamma\vert)/(1-\vert\Gamma\vert)$ | $1.92$ |
| Power reflected | $\vert\Gamma\vert^2$ | $10\%$ |

And the one that matters for design:

$$Z_L = Z_0\ \frac{1+\Gamma}{1-\Gamma}, \qquad Z_0 = 50\ \Omega$$

Note:
The right column is the -10 dB spec written four ways. Make them say out loud: -10 dB means 10% of the power comes back, 90% goes in.

---

## Raw data is garbage

Before calibration the VNA sees your antenna *through* its own hardware:

- **Directivity** — the coupler leaks a little forward wave into the reflected port. The VNA sees a reflection from a perfect load.
- **Source match** — the port is not exactly $50\ \Omega$, so energy the antenna returns gets re-reflected back at it.
- **Tracking** — the two receiver paths have different gain and phase versus frequency.

<div class="callout">
Three error terms. So you need <strong>three</strong> known standards.
</div>

Note:
One sentence each is enough at this level. Do not open the 12-term model. If someone asks, tell them it is a 2-port generalization of exactly this idea.

---

## Short–open–load

| Standard | Known $\Gamma$ | Pins down |
| :-- | :-- | :-- |
| Short | $-1$ | phase reference |
| Open | $+1$ | the other phase extreme |
| Load | $0$ | the leakage floor |

Three measurements, three unknowns, solved at every frequency point in the sweep.

<div class="callout">
Calibration does not make the instrument better. It <strong>teaches it where zero is</strong> — and zero is wherever you put the standards.
</div>

Note:
That last sentence is the whole slide. It sets up the reference-plane problem on the next slide.

---

## Where is "zero"?

- You calibrate at the **end of the test cable**. That connector is now the reference plane.
- Anything past it — pigtail, adapter, balun leg — is invisible to the correction and shows up as extra phase.
- Magnitude survives; **phase does not**. Fix it by calibrating at the antenna connector, or with port extension.

<div class="fig" data-inline-svg="./fig/L13-cal-planes.svg" style="max-width:830px; margin:0.2em auto 0;"></div>

Note:
Warn them: port extension is a phase-only fix. It cannot undo loss, and it cannot undo a mismatch inside the adapter.

---

## How far does a pigtail rotate you?

A wave travels the extra length **twice** — out and back. So the phase error is

$$\Delta\phi = 2\beta \ell = 2\ (360^\circ)\ \frac{\ell}{\lambda_g}, \qquad \lambda_g = \frac{c\ v_f}{f}$$

10 cm of RG-58 ($v_f = 0.66$) at 915 MHz: $\lambda_g = 21.6$ cm, so $\ell = 0.46\lambda_g$ and $\Delta\phi = 333^\circ$.

<div class="callout">
Almost a full turn. $\vert S_{11}\vert$ is untouched, the impedance you read is <strong>nonsense</strong>.
</div>

Note:
Point out the trap: the dB plot looks perfect, so students trust the Z readout. Half a guided wavelength repeats the impedance exactly - here that is 990 MHz.

---

## Reading the sweep

<p class="viz-cue">↗ Interactive on the lesson page</p>

- **Dip** = a resonance. **Depth** = how well matched — not how well it radiates.
- **Width at $-10$ dB** = the usable impedance bandwidth.
- Same event on the chart: the locus crosses the **real axis** and dives inside the $-10$ dB circle.

<div class="fig" data-inline-svg="./fig/L13-three-views.svg" style="max-width:790px; margin:0.2em auto 0;"></div>

Note:
Demo the widget live: sweep R away from 50 and watch the dip get shallow while the resonant frequency does not move. Then raise Q and watch the band pinch shut.

---

## Smith chart, three reading skills

You met the chart in ECE 343. You do not have to build one today — you have to **read** one.

- **Crosses the real axis** → reactance is zero → resonance. Left of centre means $R < 50\ \Omega$, right means $R > 50\ \Omega$.
- **Inside the small circle** → $\vert\Gamma\vert < 0.316$ → you are under $-10$ dB.
- **A loop** → two resonances close together, or a resonance plus a feed structure.
- **The whole trace spins** → your reference plane moved, not your antenna.

Note:
The last bullet is the diagnostic. If a student's Smith trace looks like a spiral of noodles, ask what is between the cal plane and the antenna.

---

## Worked example — $S_{11}$ to impedance

Measured at 915 MHz: $S_{11} = 0.28\ \angle-140^\circ$.

| Quantity | Work | Result |
| :-- | :-- | :-- |
| $\Gamma$ | $0.28(\cos(-140^\circ) + j\sin(-140^\circ))$ | $-0.215 - j0.180$ |
| $\vert S_{11}\vert$ | $20\log_{10}(0.28)$ | $-11.1$ dB |
| VSWR | $1.28/0.72$ | $1.78$ |
| $Z_L$ | $50(1+\Gamma)/(1-\Gamma)$ | $30.6 - j11.9\ \Omega$ |

Passes the $-10$ dB spec, and it is **capacitive** — the element is running short.

Note:
Make them predict the sign before you reveal it: negative reactance, below resonance, antenna electrically short. That is the physical read, and it is what they will do on the bench in ten minutes.

---

## Worked example — bandwidth

A trace dips to $-19$ dB and crosses $-10$ dB at 878 MHz and 922 MHz.

| Quantity | Work | Result |
| :-- | :-- | :-- |
| Centre | dip location | $900$ MHz |
| Absolute BW | $922 - 878$ | $44$ MHz |
| Fractional BW | $44/900$ | $4.9\%$ |

A thin wire dipole lands in the 3–10% range. Fatter conductor, lower $Q$, wider band — the same trade you saw in L3.

Note:
If their measured bandwidth is 1%, the antenna is probably not the problem - a resonant feed cable is. Fractional bandwidth is the number to compare across frequencies.

---

## The honest caveat

<div class="callout">
A $50\ \Omega$ resistor has $S_{11} \rightarrow -\infty$ dB, VSWR $= 1.00$, and radiates <strong>nothing</strong>.
</div>

$S_{11}$ measures **mismatch only**. The VNA cannot tell the difference between

- power that left as radiation, and
- power that died as heat in a lossy conductor, a resistive load, or wet cardboard.

Efficiency needs a second measurement — a gain comparison or a Wheeler cap. Not today, and not from one port.

Note:
This is the slide that stops "my S11 is -30 dB so my antenna is great." A shorted, lossy, badly built antenna can look superb on a VNA.

---

## The environment is part of your antenna

| Perturbation | What moves | Why |
| :-- | :-- | :-- |
| Hand near the element | $f_0$ down, dip shallower | body loading adds C and loss |
| Flat on the bench | $f_0$ shifts, loop appears | metal bench acts as a ground plane |
| Near a wall or monitor | small wiggles in the dip | re-radiated energy returns to the port |

<div class="callout">
Near-field coupling is the antenna's business. If it changed the reading, it was <strong>inside</strong> the near field.
</div>

Note:
Tie back to L5: the reactive near field is where energy is stored, not radiated. Anything you put in it becomes part of the antenna.

---

## Bench procedure

1. Set the sweep: start/stop around the expected resonance, ≥ 401 points.
2. **Calibrate** short–open–load at the far end of the test cable.
3. **Verify**: reconnect the load. $\vert S_{11}\vert$ below $-30$ dB across the band, or re-cal.
4. Connect the antenna. Hold it clear of the bench, hands, and bodies.
5. Record: resonant frequency, $Z$ at resonance, $-10$ dB band edges, Smith screenshot.
6. **Perturb**: hand near, flat on bench, held clear. Record all three.

<div class="callout">
Step 3 is not optional. An unverified cal is an unmeasured antenna.
</div>

Note:
Common failure: they cal with the standards, then swap to a different cable. Also watch for people gripping the coax right at the feed - that is a perturbation they will not notice they applied.

---

## What you turn in

- An annotated $\vert S_{11}\vert$ plot: resonance and both $-10$ dB crossings marked.
- A table: $f_0$, $Z$ at resonance, $-10$ dB bandwidth in MHz and in percent.
- A Smith-chart screenshot with the resonance point marked.
- One paragraph on the perturbation results: what moved, which direction, and why.

**One page. Numbers with units. The paragraph is where the grade lives.**

Note:
Tell them explicitly: a plot with no markers and no units is a screenshot, not a measurement. Due at the start of L15.

---

## Key point

<div class="callout">
<p>The VNA gives you one complex number per frequency, referenced to a plane <strong>you</strong> chose.</p>
<p>Read it four ways if you like — dB, VSWR, impedance, Smith chart. It still only tells you what came <em>back</em>.</p>
</div>

Note:
If they leave with one sentence, make it this one. It sets up the next lab, where they finally measure what went out.

---

## Where this is going

- **L14** measures what this lab cannot: the pattern, and with it the gain and the efficiency question you just left open.
- **Module 3** builds arrays out of these elements — and every element in an array sees its neighbours as a *mutual impedance*, which is exactly the $S_{11}$ shift you produced with your hand today.
- **Midterm project (L20)**: you will design, build, tune, and defend an antenna. Tuning means driving that dip onto your target frequency with the skills from this lab.

Note:
Sell the project link hard. Every student who can cal, measure, and read a Smith chart will finish the project; the ones who cannot will burn a week.
