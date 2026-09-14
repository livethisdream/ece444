<!-- .slide: class="title-slide" -->

<div class="title-left">

# ECE 444

Antennas, Phased Arrays, and Radar Systems

## Lesson 10 — Measurement Lab 1: Impedance and S-parameters

Fall 2026 · Dr. Neil Rogers

</div>

<div class="title-right">

![USAFA](./img/01-course-intro/USAFA-logo.png)

</div>

---

## Where we were

- **L4** gave you $\Gamma$, VSWR, return loss, and the $-10$ dB convention — all on paper.
- **L7** predicted a half-wave dipole at $73 + j42.5\ \Omega$, resonant slightly short of $\lambda/2$.
- **L9** explained the instrument: what a VNA measures, what calibration fixes, and what one port can never tell you.

**Today you use it. This is a lab period, not a lecture.**

Note:
Keep the briefing short. Everything on the theory side was covered last lesson, and they should have it open beside them. Frame the two labs as a pair: L10 is what happens at the connector, L11 is what happens in the air.

---

## Today's plan

1. Ten minutes on the widget: read a resonance three ways before you read your own.
2. Set the sweep, calibrate, **verify**.
3. Measure: resonance, impedance, $-10$ dB bandwidth.
4. Compare against your $\lambda/2$ prediction, and commit to a trim direction.
5. Perturb, one variable at a time.

Note:
Budget: about fifteen minutes of briefing, then everyone on hardware. The perturbation step is the one they will remember, so protect time for it.

---

## Rehearse the chart first

Open `viz/s11-smith.html` before you touch the instrument. Drag across either plot and the marker tracks the same frequency on both.

- The dip in dB, the real-axis crossing, and the VSWR minimum are the **same event** seen three ways.
- Move $R$ at resonance off $50\ \Omega$: the dip gets shallower and the resonant frequency does **not** move.
- Raise $Q$ and the band pinches shut. Fat conductors are wideband; thin ones are not.

Note:
This is L9's "four names for one number" made draggable. In twenty minutes they do the same reading on a noisier curve with nobody labeling the resonance for them.

---

## Equipment

- A VNA — bench instrument or NanoVNA. Either works.
- A calibration kit for your connector: short, open, $50\ \Omega$ load.
- One test cable, and a torque wrench if the bench has one.
- A supplied dipole or monopole with a known nominal resonance.
- A foam block or non-metallic stand.

Note:
The foam is not optional equipment. It is what lets them take their hands off the antenna while reading the screen, and L9 explained why that matters.

---

## Step 1 — Set the sweep

- Bracket the expected resonance by roughly $\pm 30\%$.
- At least **401 points**.
- Write the settings down *before* you calibrate.

Changing the sweep after calibration invalidates the cal on some instruments and silently interpolates on others.

Note:
Neither behavior is something you want to discover from your data. Fix the sweep first and leave it alone.

---

## Step 2 — Calibrate, then verify

- Short, open, and load at the **far end of the test cable**, not the front panel.
- Then keep the cable still. Flexing it changes its phase.

<div class="callout">
Reconnect the load: $\vert S_{11}\vert$ below $-30$ dB across the band. <strong>Screenshot it.</strong> If it fails, calibrate again.
</div>

Note:
That screenshot is a deliverable and it is the evidence their data means anything. Common failure: they cal with one cable and measure with another. Calibrating at the front panel leaves the whole cable inside the device under test.

---

## Step 3 — Measure the antenna

Connect it, set it on the foam, and take your hands off. Record:

- the resonant frequency, as the **dip** and as the **real-axis crossing**,
- $Z$ at resonance, from the marker,
- both $-10$ dB crossing frequencies.

Note:
Reading the resonance twice is not busywork. The two readings disagree when something is wrong with the reference plane, and that disagreement is the cheapest diagnostic they have.

---

## Step 4 — Compare against prediction

- Is the measured resonance **above or below** a $\lambda/2$ calculation?
- Which way would you trim the element?
- **Write the answer down before you move on.**

The sign of the reactance answers the second question on its own: negative is capacitive, the element is electrically short, and it wants to be longer.

Note:
Committing to an answer in writing before checking it is the whole point of the step. This is the exact skill the midterm project needs.

---

## Worked example — bandwidth

A trace dips to $-19$ dB and crosses $-10$ dB at 878 MHz and 922 MHz.

| Quantity | Work | Result |
| :-- | :-- | :-- |
| Center | dip location | $900$ MHz |
| Absolute BW | $922 - 878$ | $44$ MHz |
| Fractional BW | $44/900$ | $4.9\%$ |

A thin wire dipole lands in the 3–10% range. A fatter conductor lowers $Q$ and widens the band, which is the same trade you saw in L3.

Note:
If their measured bandwidth is 1%, the antenna is probably not the problem — a resonant feed cable is. Fractional bandwidth is the number to compare across frequencies.

---

## Step 5 — Perturb, one variable at a time

Repeat resonance, impedance, and bandwidth for three configurations:

- held clear, in free space,
- with a hand 2–3 cm from the element,
- lying flat on the bench.

L9 predicted the direction of each shift. Your job is the **magnitude**.

Note:
Record all three fully. A configuration measured incompletely is one they have to set up again. This is also the one-element preview of mutual impedance in Module 3.

---

## Two failure modes

<div class="callout">
Most bad lab data comes from two mistakes: <strong>calibrating with one cable and measuring with another</strong>, and <strong>gripping the coax at the feed point</strong> while you read the screen.
</div>

The second is the cruel one: you have perturbed the very measurement you are recording, and the trace looks entirely plausible.

Note:
Set the antenna down on the foam and take your hands off it. Say this twice during the period; they will still do it.

---

## What you turn in

- An annotated $\vert S_{11}\vert$ plot: resonance and both $-10$ dB crossings marked.
- A table: $f_0$, $Z$ at resonance, $-10$ dB bandwidth in MHz and in percent, all three configurations.
- A Smith-chart screenshot with the resonance point marked.
- One paragraph on the perturbation results: what moved, which direction, and why.

**One page, with units on every number. The paragraph carries the largest share of the grade.**

Note:
Tell them explicitly: a plot with no markers and no units is a screenshot, not a measurement. Due at the start of L15.

---

## Key point

<div class="callout">
<p>The VNA gives you one complex number per frequency, referenced to a plane <strong>you</strong> chose.</p>
<p>Read it four ways — dB, VSWR, impedance, Smith chart. It still reports only what came <em>back</em>.</p>
</div>

Note:
If they leave with one sentence, make it this one. It sets up the next lab, where they finally measure what went out.

---

## Where this is going

- **L11** measures what this lab cannot: the pattern, and with it the gain and the efficiency question you just left open.
- **Module 3** builds arrays out of these elements — and every element in an array sees its neighbors as a *mutual impedance*, which is exactly the $S_{11}$ shift you produced with your hand today.
- **Midterm project (L20)**: tuning an antenna means driving that dip onto your target frequency with the skills from this lab.

Note:
Make the project link explicit: calibration and Smith-chart fluency are the rate-limiting skills on the midterm. This lab is where the cost of a mistake is an afternoon rather than a week.
