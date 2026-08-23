<!-- .slide: class="title-slide" -->

<div class="title-left">

# ECE 444

Antennas, Phased Arrays, and Radar Systems

## Lesson 28 — Null Steering Lab

Fall 2026 · Dr. Neil Rogers

</div>

<div class="title-right">

![USAFA](./img/01-course-intro/USAFA-logo.png)

</div>

---

## Where we were

- L26: a real array is limited by its phase shifter — 2.8125° LSB on the ADAR1000
- L27: weight subtraction puts a null exactly where you want one, at a known cost
- L27 worked example: null at +22.5°, main-lobe cost 2.0 dB in theory, 1.8 dB measured
- The eight weights came out of arithmetic and have never touched hardware

**Today the array runs those weights, and two more nulls it finds on its own.**

Note:
Remind them the L27 example is not a new problem today. Same array, same angle,
same eight numbers. The only question is what the hardware does with them.

---

## Today's plan

1. Recall the weights and convert them to GUI settings
2. Procedure A — enter them, sweep, measure the notch
3. Why the notch stops around twenty decibels down
4. Procedure B — subtract the two digital channels, get a boresight null free
5. Procedure C — MVDR finds its own null against an interferer
6. Manual against adaptive: where each one wins

Note:
The three procedures increase in how much the array does for itself. Say that
framing up front, because it is the spine of the whole lesson.

---

## The result we are implementing

Hold the beam at $\theta_0$, null the interferer at $\theta_1$:

$$w = w_d - r_n w_n \quad \text{with} \quad r_n = \frac{w_n^H w_d}{w_n^H w_n}$$

<div class="callout">
The subtraction forces <strong>w<sup>H</sup>w<sub>n</sub> = 0</strong> — no array
response along the interferer's steering vector. Everything else in the pattern
is whatever falls out.
</div>

Note:
One line of recall, no re-derivation. If they want the derivation it is L27.
Emphasise that the null is exact on paper; the whole lab is about why it is not
exact on the bench.

---

## Converting weights to GUI settings

Two columns, entered in two panels:

| Panel | What you type | From |
| :-- | :-- | :-- |
| Element Gains | percent of the largest weight | $100\vert w_n \vert / \max \vert w \vert$ |
| Phase Control | phase offset in degrees | $\angle w_n$ |

<div class="callout">
Sixteen numbers, entered by hand. The gains are symmetric about the array centre;
the phases that place the null are equal and opposite across it.
</div>

Note:
Leave Enforce Symmetric Taper off. This particular gain set is symmetric so it
would change nothing, but a student who edits one slider afterwards will find the
edit mirrored onto its partner and will chase the wrong fault.

---

## The eight settings

<div class="fig" data-inline-svg="./fig/L28-element-settings.svg" style="max-width:820px; margin:0 auto;"></div>

Note:
Ask them what taper this is. It is not one — the amplitudes are symmetric but not
monotonic, and the phases are equal and opposite across the centre. Neither
column means anything alone; the vector nulls, not the columns.

---

## Predict before you measure

| Quantity | Predicted |
| :-- | :-- |
| Uniform sidelobe at +22.5° | −12.8 dBc |
| Notch at +22.5° | −21.6 dBc |
| Main-lobe cost | 1.8 dB |
| Sweep noise floor | about −23 dBc, i.e. 23 dB below the uniform peak |

<div class="callout">
Write these down <strong>before</strong> pressing Start. A measurement you did not
predict is a number, not a result.
</div>

Note:
Every Module 3 lab runs predict, measure, reconcile. Hold them to the order.

---

## Procedure A — the static notch

1. Uniform array, **Start**, then **Freeze** — that is the reference
2. Enter the eight percentages in **Element Gains**
3. Enter the eight offsets in **Phase Control**, signs included
4. **Start** again and read the new trace against the frozen one

<div class="callout">
A sign error on the phases moves the notch to <strong>−22.5°</strong>, which is
worth seeing once.
</div>

Note:
Have one bench deliberately flip the signs so the class sees the mirrored notch.
It makes the sign convention stick better than a slide can.

---

## Procedure A — what comes back

<div class="fig" data-inline-svg="./fig/L28-sweep-notch.svg" style="max-width:790px; margin:0 auto;"></div>

Note:
Walk the three readings: sidelobe down about nine decibels at that angle, main
lobe down 1.8, and the far sidelobes moved by a decibel or two. The last one
matters — the subtraction reshaped the whole distribution, not one angle.

---

## Why the notch stops

| Limit | Value | Effect |
| :-- | :-- | :-- |
| Phase LSB | 2.8125° | notch shifts a fraction of a degree; residual still about −48 dB |
| Gain step | about 1% | same — it moves the null, it does not fill it |
| Sweep noise floor | 23 dB below the uniform peak | sets the 20 to 22 dB you can read |

<div class="callout">
<strong>The measured notch is set by the noise floor, not by the phase LSB.</strong>
The quantized weights alone would still null to about −48 dB.
</div>

Note:
Push on this, because the intuitive answer is wrong. The rounded vector is still a
valid weight vector — it nulls a direction a fraction of a degree away from the one
asked for, and at the designed angle the residual is still down near −48 dB. What
caps the plot is the sweep's own noise floor, 23 dB below the uniform peak, less
the 2 dB of main lobe the null weights cost. That is the 20 to 22 dB they measure.

---

## The board has two digital channels

<div class="two-col"><div class="col-text">

- Each ADAR1000 sums four elements into one RF channel
- Elements 1–4 form one channel, 5–8 the other
- Analog beamforming inside each subarray, digital beamforming across the pair
- The digital layer sees two numbers per snapshot, not eight

</div><div class="col-fig">

<div class="callout">
Add the two channels and you have the sum beam. Subtract them and boresight
cancels.
</div>

</div></div>

Note:
This is the hybrid architecture from L17, and it is about to explain both the
free null in procedure B and the limits in procedure C.

---

## Procedure B — the difference null

1. **Digital Beam Forming** → Mode **Manual**
2. Set **Beam 1 Phase** to 180°
3. **Start**

<div class="callout">
Nothing in the analog beamformers changed. One sign, applied after digitizing,
cancels the two subarrays against each other on boresight.
</div>

Note:
Make them state what did not change. All eight elements still carry the same
phases. That is the point: this null is structural, not computed.

---

## Procedure B — the monopulse pair

<div class="fig" data-inline-svg="./fig/L28-delta-beam.svg" style="max-width:790px; margin:0 auto;"></div>

Note:
Sum says a target is there, difference says which side of boresight. Module 4
turns the ratio into an angle far finer than a beamwidth. Point at the steep
slope through boresight — that slope is the measurement.

---

## MVDR: let the array find the null

$$w_{\text{mvdr}} = \frac{R^{-1}s}{s^H R^{-1} s} \quad \text{with} \quad \hat R = \frac{1}{K} X X^H$$

- Minimize total output power, subject to unit gain toward $s$
- Whatever is loud and is not $s$ gets a null
- $K$ snapshots build $\hat R$; diagonal loading keeps the inverse well behaved
- Needs the **digital** channels — the analog sums already threw the rest away

Note:
Read the formula as a sentence before reading it as algebra: keep the look
direction, spend everything else on making the output quiet.

---

## Procedure C — adaptive against an interferer

1. Mode **MVDR**, Snapshots 128, Diagonal Load 0.001, Steer Angle 0°
2. **Start** with only the boresight source — MVDR has nothing to reject
3. Bring in a second X-band source near +30°, about 10 dB stronger
4. Sweep in **Manual**, then in **MVDR**, and compare the traces

<div class="callout">
Manual is captured by the interferer. MVDR holds boresight and pushes the
response toward the interferer down <strong>17 to 19 dB</strong>.
</div>

Note:
Instructor demo: the simulator's instructor view has a configurable interferer
panel — set angle and power there and the class sees the same numbers without a
second HB100. Say plainly that both sources are on the same nominal frequency, so
the FFT tab cannot separate them; the sweep trace is the evidence.

---

<!-- .slide: class="viz-cue-slide" -->

## What MVDR chooses

<div class="fig" data-inline-svg="./fig/L28-mvdr-vs-manual.svg" style="max-width:790px; margin:0 auto;"></div>

<p class="viz-cue">↗ Interactive on the lesson page</p>

Note:
Demo live: slide the interferer to twenty degrees and the null is deep with
boresight held within about a decibel. Slide it to thirty and the suppression
falls away, because the four-element subarray has already nulled that direction
and two channels four elements apart read plus thirty as almost the same phase
difference as boresight. Note that the widget parks the analog beam at boresight
while the GUI sweep moves it, so this is the digital layer on its own. Two
degrees of freedom buy one constraint and one null.

---

## Manual against adaptive

| Question | Manual | MVDR |
| :-- | :-- | :-- |
| Must know first | interferer angle | nothing |
| Interferer moves | recompute eight weights | tracks it |
| Channels needed | none extra | both digital |
| Null depth | 20–22 dB, noise floor | 17–19 dB, covariance |

<div class="callout">
You can compute eight analog degrees of freedom yourself, or let the array
compute two digital ones for you.
</div>

Note:
For a larger array, per-element digitization gives both at once. The PHASER shows
what the hybrid compromise costs.

---

## Key point

<div class="callout">
A null is only as deep as your measurement can show. Compute it and you own the
angle and the arithmetic, and you read a 20 dB notch set by the receiver noise
floor. Let MVDR compute it and you own neither the angle nor the arithmetic, but
you get only as many nulls as you have digital channels.
</div>

Note:
If they remember one sentence from this lab, this is it.

---

## Where this is going

- L29 opens Module 4 with the radar range equation
- Every Module 3 quantity becomes an antenna term in it
- The difference beam returns as monopulse angle tracking
- Module 5 capstone: track a target while an adaptive null holds a jammer down

**Deliverables: record notch depth and main-lobe cost, difference-null depth and peak angles, MVDR against manual, and two written answers.**

Note:
Point at the capstone explicitly. Procedures B and C running at the same time,
with the target moving, is the whole final project in one sentence.
