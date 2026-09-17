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
2. Set the sweep on the dashboard, calibrate, **verify**.
3. Record the antenna as a named run, and read four numbers out of the file.
4. Compare against your $\lambda/2$ prediction, and commit to a trim direction.
5. Perturb, one variable at a time.

Note:
Budget: about fifteen minutes of briefing, then everyone on hardware. The perturbation step is the one they will remember, so protect time for it. Everything today goes through the chamber dashboard — same page they will live in next lesson, with only port 1 doing anything.

---

## Rehearse the chart first

Open `viz/s11-smith.html` before you touch the instrument. Drag across either plot and the marker tracks the same frequency on both.

- The dip in dB, the real-axis crossing, and the VSWR minimum are the **same event** seen three ways.
- Move $R$ at resonance off $50\ \Omega$: the dip gets shallower and the resonant frequency does **not** move.
- Raise $Q$ and the band pinches shut. Fat conductors are wideband; thin ones are not.

Note:
This is L9's "four names for one number" made draggable. In twenty minutes they do the same reading on a noisier curve with nobody labeling the resonance for them.

---

## The rig

- The chamber's VNA, driven from the **dashboard** in a browser.
- One test cable on **port 1**, and a torque wrench if the bench has one.
- The calibration module, for the **Calibrate…** wizard.
- A supplied dipole or monopole with a known nominal resonance.
- A foam block or non-metallic stand.

Two tabs matter today: **VNA** for the live trace, **Logs** for what the service says it did.

Note:
Same instrument as L11, same dashboard, only port 1 in use. The foam is not optional equipment — it is what lets them take their hands off the antenna while reading the screen, and L9 explained why that matters. The Pattern tab has nothing to draw for a one-angle run; do not let them go looking for a curve there.

---

## Step 1 — Set the sweep

- **VNA** section: start and stop bracket the resonance by roughly $\pm 30\%$.
- At least **401 points**. Log the IF bandwidth and power too.
- **Parameter: S11** — one port, reflection only.

Changing the sweep after calibration leaves the instrument interpolating a correction across a span it never measured.

Note:
The panel flags that mismatch and the log warns again at the start of the run, which is more warning than most instruments give you — but the right move is to fix the sweep first and leave it alone. The default 2–3 GHz, 101-point sweep is a 10 MHz grid: fine for a horn, useless across a 40 MHz dipole band.

---

## Step 2 — Calibrate, then verify

- **Calibrate…** opens a wizard. Choose the reference plane: **the cable ends**, not the front panel.
- Acknowledge, run it, put the cable back. Then keep it still — flexing it changes its phase.

<div class="callout">
Verify: terminate the cable in $50\ \Omega$ and run one angle. $\vert S_{11}\vert$ below $-30$ dB across the band. <strong>Screenshot it.</strong>
</div>

Note:
The wizard asks which plane they calibrated because nothing in the data afterwards can tell, and the answer is written into the record. That dropdown is L9's reference-plane argument turned into a required field. The load verifies because it is a standard the calibration did not use to define itself. Watch the CAL / UNCAL pill: an uncalibrated run is valid data and is never blocked, but nobody should take one by accident.

---

## Step 3 — Record the antenna

Connect it, set it on the foam, and take your hands off.

- **Output**: name the run. `l10_freespace` beats a timestamp.
- **Turntable**: set **From** and **To** to the same angle — the hint reads "1 angle".
- **Start scan**, and watch the VNA tab.

Every run writes `pattern.csv` and `meta.json` under `runs/`, and anything named comes back from **Stored runs**.

Note:
A one-angle run is a complete frequency sweep at a fixed position — that is all they need today. The meta file records the sweep, whether correction was on, and a copy of the calibration record, so a finished run keeps saying what it was taken against.

---

## Step 4 — Four names for one number

The file gives you $\Gamma$ at every frequency. Everything else is arithmetic:

$$\Gamma = \text{re} + j\ \text{im}, \qquad Z = Z_0 \frac{1 + \Gamma}{1 - \Gamma}, \qquad \text{VSWR} = \frac{1 + \vert \Gamma \vert}{1 - \vert \Gamma \vert}$$

- Resonance: the dip in `mag_db`, **and** the reactance zero crossing.
- Bandwidth: the two frequencies where VSWR $= 2$.

Note:
This is L9's "four names for one number" with their own hands instead of a marker readout. Plotting Gamma on the unit disk IS the Smith chart — the chart is a grid drawn over that disk, not a different measurement. Reading the resonance twice is not busywork: the two readings disagree when something is wrong with the reference plane, and that is the cheapest diagnostic they have.

---

## Step 5 — Compare against prediction

- Is the measured resonance **above or below** a $\lambda/2$ calculation?
- Which way would you trim the element?
- **Write the answer down before you move on.**

The sign of the reactance answers the second question on its own: negative is capacitive, the element is electrically short, and it wants to be longer.

Note:
Committing to an answer in writing before checking it is the whole point of the step. This is the exact skill the midterm project needs.

---

## Worked example — bandwidth

A trace dips to $-19$ dB and crosses VSWR $= 2$ at 878 MHz and 922 MHz.

| Quantity | Work | Result |
| :-- | :-- | :-- |
| Center | dip location | $900$ MHz |
| Absolute BW | $922 - 878$ | $44$ MHz |
| Fractional BW | $44/900$ | $4.9\%$ |

A thin wire dipole lands in the 3–10% range. A fatter conductor lowers $Q$ and widens the band, which is the same trade you saw in L3.

Note:
Quote the bandwidth with the bar attached: VSWR <= 2, never "dB". On a log-magnitude trace that bar sits at −9.5 dB. If their measured bandwidth is 1%, the antenna is probably not the problem — a resonant feed cable is. Fractional bandwidth is the number to compare across frequencies.

---

## Step 6 — Perturb, one variable at a time

One named run each, same sweep, same calibration:

- held clear, in free space,
- with a hand 2–3 cm from the element,
- lying flat on the bench.

L9 predicted the direction of each shift. Your job is the **magnitude**.

Note:
Record all three fully. A configuration measured incompletely is one they have to set up again — and with named runs, one they can reload instead. This is also the one-element preview of mutual impedance in Module 3.

---

## Three failure modes

<div class="callout">
<strong>Calibrating with one cable and measuring with another.</strong><br>
<strong>Changing the sweep after you calibrated.</strong><br>
<strong>Gripping the coax at the feed point</strong> while you read the screen.
</div>

The dashboard warns you about the first two. Nothing warns you about the third, and the trace looks entirely plausible.

Note:
Set the antenna down on the foam and take your hands off it. Say this twice during the period; they will still do it. The chamber helps: with the door shut you cannot hold the element and read the trace at the same time.

---

## What you turn in

- An annotated $\vert S_{11}\vert$ plot: resonance and both VSWR $= 2$ crossings marked.
- A table: $f_0$, $Z$ at resonance, VSWR $\le 2$ bandwidth in MHz and in percent, all three configurations.
- A Smith-chart plot of your measured $\Gamma$, with the resonance point marked.
- One paragraph on the perturbation results: what moved, which direction, and why.

**One page, with units on every number. The paragraph carries the largest share of the grade.**

Note:
Tell them explicitly: a plot with no markers and no units is a screenshot, not a measurement. Quote the run name behind every figure and the reference plane they calibrated at. Due at the start of L15.

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
