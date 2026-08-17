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

- **L6:** the pattern is the radiation integral over the current — give me $I(z)$ and I will hand you the pattern.
- **L7:** we *assumed* the current was a sinusoid and got numbers: $73 + j42.5\ \Omega$, resonance near $0.47\lambda$, 2.15 dBi, 78° beamwidth.
- Every one of those numbers rests on that one assumption.

**Today a computer solves for the current instead of assuming it — and you check its homework against yours.**

Note:
Ask up front: what part of L7 was a model, and what part was physics? The
integral is physics. The sinusoid is a model. Today we replace the model.

---

## Today's plan

1. What the method of moments actually does
2. NEC's world: wires, segments, and the rules that bound them
3. Build and run a 915 MHz dipole in 4nec2
4. Sweep for resonance, record impedance, pattern, gain
5. Convergence and the sanity checks that catch a lying model

Note:
This is a lab period. The briefing is the front half; you are in 4nec2 by the
midpoint. Deliverable is a comparison table plus a paragraph per row.

---

## Why simulate at all

<div class="callout">
Hand analysis gives you the <strong>shape</strong> of the answer. Simulation gives you the <strong>number</strong> for the antenna you actually built.
</div>

- Closed forms exist for maybe six antennas. You will design more than six.
- The dipole is the one case where you can check the tool against theory you trust.
- **A tool you have never calibrated against a known answer is a random number generator with a nice GUI.**

Note:
Emphasize the last bullet — this is the entire justification for spending a lab
period on an antenna whose answer we already know.

---

## What the method of moments does

<div class="fig" data-inline-svg="./fig/L08-mom-pipeline.svg" style="max-width:790px; margin:0 auto;"></div>

Note:
Walk left to right. Step 1 and 4 are just bookkeeping around the integral they
already know. Step 2 is the physics. Step 3 is linear algebra a laptop does in
milliseconds.

---

## The condition it enforces

On a perfect conductor the total tangential field is zero. So along the wire:

$$E_z^{\text{scattered}}(z) = -E_z^{\text{source}}(z)$$

- The scattered field is produced by the unknown segment currents.
- One equation per segment; one unknown per segment; square system, one solve.
- **Nothing about a sinusoid enters anywhere.** The sinusoid was L7's guess; this is the answer.

<div class="callout">
Discretize the wire · enforce the boundary condition · solve for the currents · then integrate.
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

**Two of these fight each other on a fat wire. That is the design tension.**

Note:
Point out the fight: refining segmentation drives segment length down toward
8a. On a thick wire you run out of room, and that is NEC telling you the
thin-wire kernel does not describe your antenna.

---

## The source model

- 4nec2 drives **one segment** with a 1 V source. That segment *is* the antenna terminal — there is no connector, no gap, no coax.
- Input impedance is read straight off it: 1 V divided by the current the solve returns for that segment.
- The "gap" therefore has the width of a segment. **Refine the mesh and you quietly refine the feed too.**

<div class="callout">
Gain is an integral over the whole current. Impedance is one number read at one segment.<br>
<strong>That is why impedance converges last.</strong>
</div>

Note:
This is why impedance converges more slowly than gain: gain is an integral over
the whole current, impedance is one number read at one segment.

---

## Four ways a simulation lies to you

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
Have them write these four down. They will hit at least two today.

---

## The Average Gain Test

- Ask NEC for a **full sphere** of pattern points and it reports the **average power gain**.
- Lossless antenna, free space: the answer must be **1.000** (0.0 dB). All the power you put in came back out.
- 0.95 to 1.05 is fine. **0.6 or 1.4 means the model is broken**, and no other number on the page is trustworthy.

**It is a conservation-of-energy audit, and it is free. Run it every time.**

Note:
Average gain is the cheapest bug detector in antenna modeling. If they take one
habit from this lab, this is the one.

---

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
Demo the widget live: drag segments from 5 to 101 at half-wave length, watch the
curve flatten. Then drag length and show the plateau move. Numbers here come from
the lesson-page solver, thin wire, exactly half a wavelength long.

---

## Today's build

1. **Geometry:** one wire, along z, centered at the origin, 163.9 mm long, 0.5 mm radius, 21 segments.
2. **Excitation:** 1 V source on the center segment.
3. **Frequency:** 915 MHz, then a sweep 800–1000 MHz.
4. **Pattern:** full sphere first (for average gain), then the two principal cuts.
5. **Trim:** shorten the wire until the reactance crosses zero. Record the length.

**Menu path in 4nec2: Edit the NEC input, then Calculate, then the pattern and sweep windows.**

Note:
Keep them off the optimizer today. Hand-trimming teaches the derivative;
the optimizer hides it.

---

## Worked example — segmentation arithmetic

At 915 MHz, wavelength is 328 mm and a half wavelength is 164 mm.

| Quantity | Work | Result |
| :-- | :-- | :-- |
| Segment count | 164 mm at 21 segments | 7.8 mm each |
| Against $\lambda/20$ | 328/20 = 16.4 mm limit | 7.8 mm, passes |
| Against 8 radii | 8 × 0.5 mm = 4 mm floor | 7.8 mm, passes |
| Headroom to refine | 7.8 mm down to 4 mm | about 41 segments |

**Above 41 segments this wire is too fat for the standard kernel — not more accurate, less.**

Note:
This is the single most useful calculation in the lab. Make them do it before
touching the keyboard, and again for the trimmed length.

---

## What you should find

| Quantity | L7 hand analysis | Expect from NEC |
| :-- | :-- | :-- |
| Impedance at exactly $\lambda/2$ | $73 + j42.5\ \Omega$ | near $86 + j47\ \Omega$ |
| Resonant length | 0.47–0.48 λ | about 0.473 λ |
| Resistance at resonance | about 70 Ω | about 72 Ω |
| Gain | 2.15 dBi | 2.1–2.2 dBi |

**The gain and the resonance land. The half-wave impedance does not — and that gap is the assignment.**

Note:
Do not let them "fix" the discrepancy. Explaining it is the deliverable. The
sinusoid resonates at 0.486 lambda; a real wire resonates shorter, so an exactly
half-wave wire is already long and inductive.

---

## Why the half-wave number misses

<div class="callout">
73 + j42.5 &#937; is the impedance of a <em>sinusoid</em>, not of a <em>wire</em>.
</div>

- Finite radius stores energy near the wire, so resonance falls to about 0.473 λ.
- A wire cut to exactly $\lambda/2$ is therefore already **5% long** — inductive, and higher in resistance.
- Trim to resonance and the two answers agree to a couple of ohms.

**Same physics. Different length. That is the whole story.**

Note:
Push on this. The disagreement is not numerical error — it is two different
antennas being compared. Trimming makes them the same antenna again.

---

## Deliverables

1. A **comparison table**: simulated vs analytical for impedance, resonant length, resistance at resonance, gain, and beamwidth — with percent difference on each row.
2. **One paragraph per row** accounting for the difference. "Simulation error" is not an explanation.
3. Your **convergence study**: impedance at 11, 21, 41, and 81 segments, and the segment count you would defend.
4. The **average gain** figure from your full-sphere run.

**Numbers without an account of why they differ earn no credit.**

Note:
Grading emphasis: the paragraphs. Anyone can copy an impedance out of a results
window.

---

## Key point

<div class="callout">
A simulator does not know more physics than you do.<br>
It solves for the current you would have had to guess — <strong>then runs your integral.</strong><br>
Everything it reports is only as good as the segments, the radius, and the source you gave it.
</div>

Note:
End the briefing here and let them build. Repeat the average-gain habit on the
way out the door.

---

## Where this is going

- **L9:** loops and monopoles. A monopole model needs a **ground plane** — a new card, and a new way to get the model wrong.
- **Module 3:** arrays. Every element you place is another wire, and segmentation rules apply to all of them at once.
- The habit you build today — predict, simulate, reconcile — is the habit for every antenna in the course.

**Predict first. Always. A simulation you cannot argue with taught you nothing.**

Note:
Preview L9 briefly: perfect ground doubles directivity and halves impedance,
and NEC's GN card is where that happens.
