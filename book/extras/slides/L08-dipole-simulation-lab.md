<!-- .slide: class="title-slide" -->

<div class="title-left">

# ECE 444

Antennas, Phased Arrays, and Radar Systems

## Lesson 8 — Dipole Simulation Lab

Fall 2026 · Dr. Neil Rogers

</div>

<div class="title-right">

![USAFA](./img/01-course-intro/USAFA-logo.png)

</div>

---

## Where we were

- **L6:** the pattern is the radiation integral over the current, so a known $I(z)$ determines the pattern completely.
- **L7:** we *assumed* the current was a sinusoid and got numbers: $73 + j42.5\ \Omega$, resonance near $0.47\lambda$, 2.15 dBi, 78° beamwidth.
- Every one of those numbers rests on that one assumption.

**Today a computer solves for the current instead of assuming it, and you reconcile its answer with yours.**

Note:
Ask up front: what part of L7 was a model, and what part was physics? The
integral is physics. The sinusoid is a model. Today we replace the model.

---

## Today's plan

1. What the method of moments does
2. NEC's world: wires, segments, and the rules that bound them
3. Build and run a 915 MHz dipole in 4nec2
4. Sweep for resonance, record impedance, pattern, gain
5. Convergence, and the sanity checks that catch a broken model

Note:
This is a lab period. The briefing is the front half, and they should be in
4nec2 by the midpoint. The deliverable is a comparison table with a paragraph
for each row.

---

## Why simulate at all

<div class="callout">
Hand analysis gives you the <strong>shape</strong> of the answer. Simulation gives you the <strong>number</strong> for the antenna you actually built.
</div>

- Closed-form solutions exist for only a handful of antennas, and you will design more than a handful.
- The dipole is the one case where you can check the tool against theory you already trust.
- **A tool you have never checked against a known answer cannot be trusted on an unknown one.**

Note:
Emphasize the last bullet — this is the entire justification for spending a lab
period on an antenna whose answer we already know.

---

## What the method of moments does

<div class="fig" data-inline-svg="./fig/L08-mom-pipeline.svg" style="max-width:790px; margin:0 auto;"></div>

Note:
Walk left to right. Steps 1 and 4 are bookkeeping around the integral they
already know. Step 2 is the physics, and step 3 is linear algebra that a laptop
finishes in milliseconds.

---

## The condition it enforces

On a perfect conductor the total tangential field is zero. So along the wire:

$$E_z^{\text{scattered}}(z) = -E_z^{\text{source}}(z)$$

- The scattered field is produced by the unknown segment currents.
- There is one equation and one unknown per segment, so the system is square and solves in one step.
- **No sinusoid is assumed anywhere in this process.** L7 assumed the current, while the solver computes it.

<div class="callout">
The solver discretizes the wire, enforces the boundary condition, solves for the segment currents, and then integrates.
</div>

Note:
This is Pocklington's / Hallen's equation depending on the form. Do not derive
it. The takeaway is that MoM turns an integral equation into a matrix.

---

## NEC's world is made of wires

<div class="fig" data-inline-svg="./fig/L08-segment-rules.svg" style="max-width:790px; margin:0 auto;"></div>

Note:
NEC-2 knows two things: thin wires and surface patches. Everything you model in
this course is wires. A "dipole" is one wire card with a segment count.

---

## The three segmentation rules

| Rule | Why it exists | Violate it and… |
| :-- | :-- | :-- |
| 10–20 segments per half wavelength | resolve the current's curvature | pattern and gain smear |
| Segment length $< \lambda/20$ | phase changes little across a segment | impedance drifts badly |
| Segment length $> 8 \times$ radius | thin-wire kernel stays valid | numbers become fiction |
| Odd segment count | puts a segment at the feed | source lands off-center |

**Two of these rules pull against each other on a fat wire, and that tension is the design constraint.**

Note:
Point out the tension: refining the segmentation drives the segment length down
toward 8a. On a thick wire you run out of room, which is NEC telling you that
the thin-wire kernel does not describe your antenna.

---

## From currents to one impedance

4nec2 drives **one segment** with a known voltage. The solve returns the current there, and Ohm's law finishes the job:

$$Z\_{\text{in}} = \frac{V\_{\text{feed}}}{I\_{\text{feed}}}$$

- With a 1 V source, the impedance is the reciprocal of the feed-segment current.
- The other $N-1$ currents never enter this division; they set the **pattern**.

<div class="callout">
A misplaced source wrecks the impedance while barely moving the pattern.
</div>

Note:
Say the division out loud: one volt divided by the feed current, in milliamps,
gives tens of ohms. Point out that a source on the wrong segment reads a smaller
current and reports a wildly wrong impedance, while the pattern hardly changes
because the distribution as a whole hardly changed.

---

## Four ways a model misleads you

| Symptom | Likely cause | Check |
| :-- | :-- | :-- |
| Gain drifts with segment count | too few segments | double N, re-run |
| Impedance is wild or oscillates | segment shorter than 8 radii | lengthen segments |
| Feed impedance looks nothing like theory | source on the wrong segment | odd count, center tag |
| Average gain far from 1.0 | geometry or kernel error | fix before reading anything |

<div class="callout">
The simulator never reports that it is wrong. <strong>You</strong> have to ask.
</div>

Note:
Have them write these four down. Most groups will hit at least two of them
today.

---

## The Average Gain Test

- Ask NEC for a **full sphere** of pattern points and it reports the **average power gain**.
- For a lossless antenna in free space the answer must be **1.000** (0.0 dB), because all the power delivered has to leave as radiation.
- A value between 0.95 and 1.05 is healthy. **A value like 0.6 or 1.4 means the model is broken**, and no other number in the file can be trusted.

**The test is a conservation-of-energy audit that costs one extra run, so run it every time.**

Note:
Average gain is the cheapest error check in antenna modeling. If they take one
habit away from this lab, it should be this one.

---

<!-- .slide: class="viz-cue-slide" -->

## Convergence: what "converged" means

<p class="viz-cue">↗ Interactive on the lesson page</p>

| Segments | Input resistance | Input reactance |
| :-- | :-- | :-- |
| 5 | 79.9 Ω | +35.9 Ω |
| 11 | 81.9 Ω | +43.9 Ω |
| 21 | 83.4 Ω | +45.6 Ω |
| 41 | 84.5 Ω | +46.5 Ω |
| 81 | 85.4 Ω | +47.2 Ω |

**Converged is not "matches theory" — it is "stops moving when I refine."**

Note:
Demo the widget live: drag the segment count from 5 to 101 at half-wave length
and watch the curve flatten, then drag the length and show the plateau move.
Point at the feed readouts while dragging, because only the feed current is
changing. These numbers come from the lesson-page solver on a thin wire exactly
half a wavelength long.

---

## Today's build

1. **Geometry:** one wire, along z, centered at the origin, 163.9 mm long, 0.5 mm radius, 21 segments.
2. **Excitation:** 1 V source on the center segment.
3. **Frequency:** 915 MHz, then a sweep 800–1000 MHz.
4. **Pattern:** full sphere first (for average gain), then the two principal cuts.
5. **Trim:** shorten the wire until the reactance crosses zero. Record the length.

**In 4nec2 you edit the NEC input file, run Calculate, and then read the pattern and sweep windows.**

Note:
Keep them off the optimizer today. Trimming by hand shows them how impedance
responds to length, and the optimizer hides that relationship.

---

## Worked example — segmentation arithmetic

At 915 MHz, wavelength is 328 mm and a half wavelength is 164 mm.

| Quantity | Work | Result |
| :-- | :-- | :-- |
| Segment count | 164 mm at 21 segments | 7.8 mm each |
| Against $\lambda/20$ | 328/20 = 16.4 mm limit | 7.8 mm, passes |
| Against 8 radii | 8 × 0.5 mm = 4 mm floor | 7.8 mm, passes |
| Headroom to refine | 7.8 mm down to 4 mm | about 41 segments |

**Above 41 segments this wire is too fat for the standard kernel, so the extra segments make the answer less accurate rather than more.**

Note:
This is the most useful calculation in the lab. Make them do it before they
touch the keyboard, and again for the trimmed length.

---

## What you should find

| Quantity | L7 hand analysis | Expect from NEC |
| :-- | :-- | :-- |
| Impedance at exactly $\lambda/2$ | $73 + j42.5\ \Omega$ | near $86 + j47\ \Omega$ |
| Resonant length | 0.47–0.48 λ | about 0.473 λ |
| Resistance at resonance | about 70 Ω | about 72 Ω |
| Gain | 2.15 dBi | 2.1–2.2 dBi |

**The gain and the resonant length agree, while the half-wave impedance does not, and explaining that gap is the assignment.**

Note:
Do not let them "fix" the discrepancy, because explaining it is the deliverable.
The sinusoid resonates at 0.486 lambda, and a real wire resonates shorter, so an
exactly half-wave wire is already long and therefore inductive.

---

## Why the half-wave number misses

<div class="callout">
73 + j42.5 &#937; is the impedance of a <em>sinusoid</em>, not of a <em>wire</em>.
</div>

- Finite radius stores energy near the wire, so resonance falls to about 0.473 λ.
- A wire cut to exactly $\lambda/2$ is therefore already **5% long**, which makes it inductive and raises its resistance.
- Trim to resonance and the two answers agree to a couple of ohms.

**The physics is the same in both cases, and only the length differs.**

Note:
Push on this. The disagreement is not numerical error, because two different
antennas are being compared. Trimming makes them the same antenna again.

---

## Deliverables

1. A **comparison table**: simulated vs analytical for impedance, resonant length, resistance at resonance, gain, and beamwidth — with percent difference on each row.
2. **One paragraph per row** accounting for the difference. "Simulation error" is not an explanation.
3. Your **convergence study**: impedance at 11, 21, 41, and 81 segments, and the segment count you would defend.
4. The **average gain** figure from your full-sphere run.

**Numbers without an account of why they differ earn no credit.**

Note:
The grading emphasis is on the paragraphs, because anyone can copy an impedance
out of a results window.

---

## Key point

<div class="callout">
A simulator does not know more physics than you do.<br>
It solves for the current you would have had to guess — <strong>then runs your integral.</strong><br>
Everything it reports is only as good as the segments, the radius, and the source you gave it.
</div>

Note:
End the briefing here and let them build. Remind them once more to run the
average-gain check before they record anything.

---

## Where this is going

- **L9:** loops and monopoles. A monopole model needs a **ground plane**, which adds a new card and a new way for the model to go wrong.
- **Module 3:** arrays. Every element you place is another wire, and segmentation rules apply to all of them at once.
- The habit you build today — predict, simulate, reconcile — is the habit for every antenna in the course.

**Always predict first, because a simulation you cannot argue with has taught you nothing.**

Note:
Preview L9 briefly: perfect ground doubles the directivity and halves the
impedance, and NEC's GN card is where that happens. Ask them to review the L7
sinusoid assumption before that lesson.
