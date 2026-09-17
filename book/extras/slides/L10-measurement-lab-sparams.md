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

## What you can wreck

| What | Cost | Ruined by |
| :-- | :-- | :-- |
| Absorber | \$750/sq ft | leaning, stacking |
| VNA port | \$85k | cross-thread, over-torque, cable stress |
| Horn | \$5k | dropping |
| Cable | \$1k | kinking |

<div class="callout">A bad measurement costs you an afternoon. <strong>Everything in that table costs the rig.</strong></div>

Note:
The RF is milliwatts and nothing here will hurt them, which is exactly why this gets skipped. Go through the mechanisms: start threads by hand and square, torque rather than feel, turn the nut and not the cable body — a cross-threaded or over-torqued port is a bench repair on an eighty-five thousand dollar instrument, and the damage transfers to the next connector it mates with, which on this rig is the calibration module. Nothing hangs off a port: side load is cable stress and is the slow version of the same failure. Two hands on a horn, and never hang it from its connector. Bend radius on cables, no tight coils, nothing where somebody will stand on it. And absorber is priced by the square foot — a crushed tip is a permanently worse quiet zone and there is no repairing one. Also: nothing that transmits goes into an analyzer port, and touch a grounded surface before touching a center pin.

---

## Good practice

- Calibrate, **verify**, then measure. In that order.
- Log the sweep settings before you calibrate.
- Change one thing at a time.
- Name and export every capture as you take it.

**Write down what you expect before you look.**

Note:
A prediction they committed to in writing is the only way a surprise can teach them anything; a prediction made after seeing the answer is not a prediction. This is also the half that shows up in the grade.

---

## Today's plan

1. Ten minutes on the widget: read a resonance three ways before you read your own.
2. Set the sweep on the dashboard, calibrate one port, **verify**.
3. Capture the antenna on the **Sweep** tab, and read four numbers off the marker.
4. Compare against your $\lambda/2$ prediction, and commit to a trim direction.
5. Perturb, one variable at a time, and export a file for each.

Note:
Budget: about fifteen minutes of briefing, then everyone on hardware. The perturbation step is the one they will remember, so protect time for it. Everything today goes through the chamber dashboard's Sweep tab — same page they will live in next lesson, with only port 1 doing anything and the tower never moving.

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

Two tabs matter today: **Sweep**, which captures without moving the tower, and **Logs**.

Note:
Same instrument as L11, same dashboard, only port 1 in use. The Sweep tab is the measurement this rig can make with nothing but an analyzer attached — the service will even run with no positioner, and says so. The foam is not optional equipment: it is what lets them take their hands off the antenna while reading the screen, and L9 explained why that matters. The Pattern and Turntable tabs have nothing to do with today; do not let them go looking for a curve there.

---

## Step 1 — Set the sweep

- **VNA** section: start and stop bracket the resonance by roughly $\pm 30\%$.
- At least **401 points**. Log the IF bandwidth and power too.
- The **Parameter** dropdown is for scans — a capture chooses its own.

Changing the sweep after calibration leaves the instrument interpolating a correction across a span it never measured.

Note:
The panel flags that mismatch and the log warns again, which is more warning than most instruments give you — but the right move is to fix the sweep first and leave it alone. The default 2–3 GHz, 101-point sweep is a 10 MHz grid: fine for a horn, useless across a 40 MHz dipole band. Points also set how finely the marker can be placed, because it steps from one measured frequency to the next and not between them.

---

## Step 2 — Calibrate, then verify

- **Calibrate…** → **1-port, port 1**. Reference plane: **the cable ends**, not the front panel.
- Acknowledge, run it, put the cable back. Then keep it still — flexing it changes its phase.

<div class="callout">
Verify: terminate the cable in $50\ \Omega$ and press <strong>Sweep</strong>. Return loss better than $30$ dB across the band. <strong>Screenshot it.</strong>
</div>

Note:
A one-port calibration corrects reflection on that port alone and needs only that one cable end on the module — the two-port option also corrects transmission, which is L11's problem, not today's. Pick one port and the wizard's checklist rewrites itself to match, so nobody is sent in to disconnect an antenna for no reason. The wizard asks which plane they calibrated because nothing in the data afterwards can tell, and the answer is written into the record and into every exported file. The load verifies because it is a standard the calibration did not use to define itself. Watch the cal / uncal pill in the bottom strip.

---

## Step 3 — Capture the antenna

Connect it, set it on the foam, and take your hands off.

- **Sweep** tab, **Capture: S11 only**.
- Press **Sweep**. The tower does not move.
- The Smith chart and the magnitude plot fill in together.

One sweep per parameter, so asking for all four costs four times the wait and measures three things that are not there.

Note:
A capture is not a scan and is not written to runs/ — it lives in the browser until they export it. That is deliberate: the service ships complex S-parameters and nothing else, and every derived number on the page is computed from them, so the payload stays a measurement rather than a measurement plus somebody's arithmetic. If they do ask for several parameters, STOP declines to start the next one rather than interrupting the sweep in flight.

---

## Step 4 — Four names for one number

Park the **Marker** on a frequency and the readout gives all of it at once — $Z$, $\vert \Gamma \vert$, VSWR, return loss:

$$Z = Z_0 \frac{1 + \Gamma}{1 - \Gamma}, \qquad \text{VSWR} = \frac{1 + \vert \Gamma \vert}{1 - \vert \Gamma \vert}, \qquad \text{RL} = -20 \log_{10} \vert \Gamma \vert$$

- Resonance: the dip in dB, **and** the reactance through zero.
- Bandwidth: step the marker to both VSWR $= 2$ frequencies.

<div class="callout">The Smith chart is not a fifth quantity. It is the <strong>same complex number</strong>, plotted where you can see it.</div>

Note:
This is L9's "four names for one number" with the instrument doing the conversion. Two readings worth recognizing on sight: the readout says "open" where Gamma reaches +1, because the impedance there is unbounded rather than merely large; and it says VSWR infinity whenever |Gamma| is at or above 1, which a passive antenna cannot do — that is noise or a calibration that no longer matches the sweep, not a measurement. Reading the resonance twice is not busywork: the two disagree when something is wrong with the reference plane, and that is the cheapest diagnostic they have.

---

## The file is the record

**Export** writes a Touchstone file — `.s1p` for one reflection parameter — and its header carries what a plot cannot:

- hardware or **simulated**,
- which parameters were actually measured,
- the calibration, its ports, and its reference plane.

Export every configuration before you change anything.

Note:
A trace on a screen is a measurement that cannot say what it was taken under. Two details in that header exist because of how easily a file lies: a single reflection parameter is written as .s1p rather than an .s2p with three columns zeroed — that file would claim a through path of exactly zero and an infinitely reflective second port, and a reader will plot those numbers happily — and a partial capture names in the header what was not measured. Touchstone 2-port column order is S11 S21 S12 S22, which is not the order anyone expects and is the usual source of transposed data.

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

One capture and one exported file each, same sweep, same calibration:

- held clear, in free space,
- with a hand 2–3 cm from the element,
- lying flat on the bench.

L9 predicted the direction of each shift. Your job is the **magnitude**.

Note:
Record all three fully. A configuration measured incompletely is one they have to set up again. Have them rename each file as they save it — l10_freespace.s1p, l10_hand.s1p, l10_bench.s1p — because the export stamps the clock into the filename, which keeps three captures apart and says nothing about which is which a week later. This is also the one-element preview of mutual impedance in Module 3.

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
- A Smith chart with the marker on the resonance.
- One paragraph on the perturbation results: what moved, which direction, and why.

**One page, with units on every number. The paragraph carries the largest share of the grade.**

Note:
Tell them explicitly: a plot with no markers and no units is a screenshot, not a measurement. The three exported files come in with it, and they state the reference plane they calibrated at. Due at the start of L15.

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
