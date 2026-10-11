<!-- .slide: class="title-slide" -->

<div class="title-left">

# ECE 444

Antennas, Phased Arrays, and Radar Systems

## Lesson 19 — Beam Steering Lab

Fall 2026 · Dr. Neil Rogers

</div>

<div class="title-right">

![USAFA](./img/01-course-intro/USAFA-logo.png)

</div>

---

## Where we were

- L16 built the array factor from phasor superposition: pattern = element factor × array factor.
- L17 opened the PHASER: 8 patches on a 14 mm pitch, two ADAR1000 beamformers, a Pluto behind them.
- L18 derived the steering law $\Delta\phi = kd\sin\theta_0$ from a path-length argument.
- You left L18 with a table of element phases and no evidence it works.

**Today the table meets the hardware.**

Note:
Open by asking what they predicted for thirty degrees. Someone should have
eighty-eight point four. Write it on the board and leave it up all period.

---

## Today's plan

1. Recall the prediction, and the wrapped phase table for thirty degrees.
2. Settle what the beam-sweep plot shows.
3. Bring up the GUI and load Lab Preset 1.
4. Find the beam by hand, then read back the phases the GUI applied.
5. Sweep, freeze, move the source, sweep again.
6. Size the four error sources and record the deliverables.

Note:
The lab runs long if step four is rushed. Budget ten minutes for the phase
read-back; it is the part that connects to L18.

---

## The prediction you bring

$$\Delta\phi = kd\sin\theta_0 = 360^\circ\ \frac{d}{\lambda}\ \sin\theta_0$$

At the HB100's $10.525$ GHz: $\lambda = 28.5$ mm, so $d/\lambda = 0.491$ and $\Delta\phi = 176.8^\circ \sin\theta_0$.

| $\theta_0$ | $0^\circ$ | $15^\circ$ | $30^\circ$ | $45^\circ$ |
| :-- | :-- | :-- | :-- | :-- |
| $\Delta\phi$ | $0.0^\circ$ | $45.8^\circ$ | $88.4^\circ$ | $125.0^\circ$ |

<div class="callout">
Each steer angle needs only this one number. Every element phase follows from it.
</div>

Note:
Point out that d over lambda is just under a half wavelength, so the phase
never reaches one hundred eighty degrees per element. That matters again in
lesson twenty-six when we talk about grating lobes.

---

## Element phases wrap

Element $n$ gets $n\Delta\phi$ modulo $360^\circ$. A shifter cannot produce $442^\circ$; it produces $82^\circ$, and the array cannot tell the difference.

| Element, $\theta_0 = 30^\circ$ | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 |
| :-- | :-- | :-- | :-- | :-- | :-- | :-- | :-- | :-- |
| Ramp | $0.0$ | $88.4$ | $176.8$ | $265.2$ | $353.6$ | $442.0$ | $530.5$ | $618.9$ |
| Applied | $0.0$ | $88.4$ | $176.8$ | $265.2$ | $353.6$ | $82.0$ | $170.5$ | $258.9$ |

<div class="fig" data-inline-svg="./fig/L19-phase-ramp.svg" style="max-width:520px; margin:0 auto;"></div>

Note:
Values in degrees. Have them circle element six: four hundred forty-two becomes
eighty-two, and that single check is the whole of learning outcome three. The
red crosses are the same values pushed onto the two point eight one two five
degree grid.

---

## What the sweep plot is

<div class="callout">
The x-axis is the <strong>commanded steer angle</strong>, not a measured arrival angle. The source stays still; the beamformer steps its command across the range and records power at each step.
</div>

- By reciprocity, the receive pattern equals the transmit pattern, so the trace has the shape of the array pattern.
- Its peak sits at the angle where the source is.
- Every point on the trace came from a different set of element phases.

Note:
This is the slide to slow down on. If they think the x-axis is arrival angle,
every number they record today is misinterpreted. Ask them what the plot would
look like with two sources on the arc.

---

## The bench

<div class="fig" data-inline-svg="./fig/L19-bench-setup.svg" style="max-width:760px; margin:0 auto;"></div>

Source at about one meter, at the height of the element row, aimed back at the array.

Note:
One degree of arc at one meter is seventeen millimeters. Show them that with a
ruler before they place the tripod.

---

## Setup

1. Power the board, wait for the Pi, open `http://phaser.local:8080`.
2. Confirm Configuration shows live Signal Freq and Rx Gain, then press **Calibrate**.
3. **Lab Presets → 1 Steering Angle**: uniform taper, $0^\circ$ steer, $2.8125^\circ$ steer resolution.
4. Record the frequency the GUI locked to.

The HB100 is a free-running oscillator anywhere in $10.1$–$10.7$ GHz. Your whole prediction table depends on which value it picked today.

Note:
Bring-up was done in lesson seventeen, so this should take five minutes. If a
board will not come up, pair the cadets rather than debugging in front of the
class.

---

## Steps 1–3: find the beam by hand

1. HB100 at $0^\circ$. On the **FFT** tab, one tone stands $20$ dB or more above the noise near the $1$ MHz offset.
2. Move the tripod to $+30^\circ$. The tone drops $10$ to $13$ dB — the array is still looking at boresight.
3. In **Beam Steering**, enter a Steer Angle, press **Apply**, read the amplitude. Work in $5^\circ$ steps, then $2^\circ$ steps.

Record the commanded angle that maximizes the tone. Expect it within one $2.8125^\circ$ grid step of the arc reading.

Note:
Make them do the hunt manually before the automatic sweep. Watching the tone
climb and fall as they type angles is what makes the sweep plot obvious ten
minutes later.

---

## Step 4: read the phases back

- With the peak command applied, open **Phase Control** and read Rx1 through Rx8.
- Compare with your $30^\circ$ row. They agree after wrapping.
- Each value sits on the nearest multiple of $2.8125^\circ$, so single elements differ from theory by up to $1.4^\circ$.

<div class="callout">
Element 6: theory says $442.0^\circ$, the GUI shows about $82^\circ$. It is the same array and the same beam.
</div>

Note:
If a cadet's read-back disagrees by more than one point four degrees on any
element, they either recorded the wrong frequency or the calibration did not
run.

---

## Step 5: sweep, freeze, move, sweep

<div class="fig" data-inline-svg="./fig/L19-sweep-compare.svg" style="max-width:700px; margin:0 auto;"></div>

**Rectangular** tab → **Start**, then **Freeze**. Move the source to boresight and **Start** again.

Note:
Same beam, two source positions. Have them measure the half-power width of each
trace on screen before you show the expected numbers.

---

<!-- .slide: class="viz-cue-slide" -->

## Predict before you measure

- Set the widget's frequency to what the GUI reported for your HB100.
- Set the steer angle to what you plan to command.
- Read $\Delta\phi$, the eight wrapped phases, and the predicted beamwidth.

The dots are the $2.8125^\circ$ sample grid. A $13^\circ$ beam is described by about five samples.

<p class="viz-cue">↗ Interactive on the lesson page</p>

Note:
Demo live: sweep the frequency slider from ten point one to ten point seven and
show the phases move while the beam stays put. That is the setup for the squint
discussion two slides later.

---

## Expected numbers

| Quantity | Calculated | Expect to measure |
| :-- | :-- | :-- |
| Peak of trace | at the source angle | within one $2.8125^\circ$ step |
| HPBW at $0^\circ$ | $13.0^\circ$ | $13.1^\circ$ $\pm$ a grid step |
| HPBW at $30^\circ$ | $15.1^\circ$ | $\approx 15^\circ$ $\pm$ a grid step |
| Peak level, $30^\circ$ vs $0^\circ$ | $-0.6$ dB | $-0.5$ to $-1.5$ dB |
| First sidelobes | $-12.8$ dB | $-11$ to $-13$ dBc |

Note:
The noise floor sits about twenty-three dB below the peak, so the first
sidelobes are visible and the second ones are marginal.

---

## Worked example — the two steered numbers

| Quantity | Work | Result |
| :-- | :-- | :-- |
| HPBW at $30^\circ$ | $13.0^\circ / \cos 30^\circ$ | $15.0^\circ$ |
| Scan loss | $10\log_{10}(\cos 30^\circ)$ | $-0.6$ dB |

Both come from the same fact: steering tilts the beam off the aperture face, and the array presents $Nd\cos\theta_0$ instead of $Nd$.

<div class="callout">
A shorter aperture gives a wider beam and less collected power. One geometric cause produces both effects.
</div>

Note:
Real patch elements roll off faster than the ideal cosine, so measured scan
loss usually runs a few tenths worse. Lesson twenty-two makes that the topic.

---

## Where the error comes from

<div class="fig" data-inline-svg="./fig/L19-error-budget.svg" style="max-width:680px; margin:0 auto;"></div>

In quadrature these give about $2.5^\circ$ of peak-angle uncertainty.

Note:
Two and a half degrees is why one grid step is the right standard for the lab.
Agreement to a tenth of a degree means the comparison was set up wrong.

---

## The four sources, sized

- **Sweep grid**: the trace has no information between $2.8125^\circ$ points, so the peak reads to half a step, $1.41^\circ$.
- **Protractor and aim**: $1^\circ$ of arc is $17$ mm at one meter. This error is in the reference, not the array.
- **HB100 drift**: phases were computed at an assumed frequency. A $200$ MHz drift moves the beam to $\arcsin[(f_0/f)\sin\theta_0]$, which is $+0.6^\circ$ at $30^\circ$.
- **Multipath**: about $1$ dB of ripple on the main lobe and several dB on a sidelobe.

Note:
The drift line is beam squint, and it is the reason a phase-steered array is a
narrowband device. Say the word, promise lesson twenty-six, and move on.

---

## No hardware?

- `python phaser_headless.py --sim` runs the whole UI against physics-based stubs.
- The simulated target is fixed at boresight and cannot be moved, so skip the protractor steps.
- Instead: command a steer angle and watch the FFT tone stay put while the swept trace's main lobe moves to the command.
- Step 4 works unchanged — the phases do not depend on a real signal arriving.

Note:
The sim is the fallback for a cadet who misses the period. It covers learning
outcomes one, three and four; only outcome two needs the kit.

---

## Deliverables

1. **Table A** — commanded versus physical angle at $0^\circ$, $30^\circ$, $45^\circ$, with the difference in grid steps.
2. **Table B** — all eight predicted versus applied phases at $30^\circ$, and whether every difference is under half an LSB.
3. **Table C** — half-power width of both traces, calculated beside measured, plus the peak-level difference.
4. Two short written answers: why the peak quantizes, and why the trace is a pattern at all.

Note:
The two written answers are graded harder than the tables. Anyone who writes
"because the GUI plots it that way" for the second one has not understood the
reciprocity slide.

---

## Key point

<div class="callout">
The beam went where the phases sent it, to within one grid step. <strong>The steering law is not an approximation you are checking — it is the instruction set the hardware executes</strong>, and every departure you measured today has a name and a size.
</div>

Note:
Land here. The phases are commands, not predictions. What varies is the
reference you compare against and the resolution you compare at.

---

## Where this is going

- **L20** derives every feature of the trace you recorded: null positions, the $-13$ dB first sidelobe, and $0.886\ \lambda/(Nd\cos\theta_0)$.
- Bring today's traces. A derivation is easier to trust with the measurement already in hand.
- **The midterm project is due at the start of L20.**

Note:
Remind them the project turn-in is at the start of the hour, not the end.
Reading for next time is the closed-form array factor and its nulls.
