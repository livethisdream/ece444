<!-- .slide: class="title-slide" -->

<div class="title-left">

# ECE 444

Antennas, Phased Arrays, and Radar Systems

## Lesson 10 — Patch, Slot, and Horn Antennas

Fall 2026 · Dr. Neil Rogers

</div>

<div class="title-right">

![USAFA](./img/01-course-intro/USAFA-logo.png)

</div>

---

## Where we were

- L7: the half-wave dipole — a resonant wire, $73 + j42.5\ \Omega$, $2.15$ dBi.
- L9: fold it, bend it, ground it — loops and monopoles, still wire.
- L6: the radiation integral does not care what carries the current. An aperture with a known field is just as good a source.
- L5: $r \ge 2D^2/\lambda$, and gain lives in electrical size.

**Today the antenna stops being a wire. It becomes a surface, a hole, and an opening.**

Note:
Anchor them: three lessons of wires, and every one of them sticks out of the airframe. Today's three all hide flush or bolt to a waveguide.

---

## Today's plan

1. The **microstrip patch** — a resonant cavity that leaks from two edges.
2. Sizing one: $\varepsilon_{\text{eff}}$, the edge extension $\Delta L$, and a worked design.
3. The **slot** — Babinet's complement of the dipole.
4. The **horn** — a waveguide that grows an aperture.
5. Choosing among the three.

<div class="callout">All three are <strong>aperture thinking</strong>: name the field in an opening, integrate it, read the pattern.</div>

Note:
Three antennas, one lesson. The organizing question every time: what physically radiates, and what does that force the pattern and bandwidth to be? Point back at L6 — the equivalence principle lets us replace an aperture field with equivalent magnetic currents, so we never solve for current on the metal.

---

## The patch: a half-wave cavity, printed

<div class="two-col fig-wide"><div class="col-text">
<p>A conductor of width <em>W</em> and length <em>L</em>, on a substrate of thickness <em>h</em> and permittivity <em>&epsilon;<sub>r</sub></em>, over a solid ground plane.</p>
<p>Drive it and it is a <strong>half-wave resonator</strong> in the dielectric: $L \approx \lambda_d/2$, with $\lambda_d = \lambda_0/\sqrt{\varepsilon_{\text{eff}}}$.</p>
<p>The metal is a poor radiator. <strong>The edges are the antenna.</strong></p>
</div><div class="col-fig">
<div class="fig" data-inline-svg="./fig/L10-patch-anatomy.svg" style="max-width:560px; margin:0 auto;"></div>
</div></div>

Note:
Stress the direction bookkeeping: L sets the resonance, W sets the impedance and the H-plane beamwidth. Students mix them up constantly.

---

## Why it radiates: two slots

<div class="two-col fig-xwide"><div class="col-text">
<p>The cavity field runs <strong>patch to ground</strong> as a half-wave standing wave, so it points <strong>down at one open edge and up at the other</strong>.</p>
<p>At each edge the field <strong>fringes</strong> past the conductor. The vertical parts are opposite and <strong>cancel</strong>. The horizontal parts point the same way and <strong>add</strong>.</p>
<p>Two edges, $\lambda_d/2$ apart, in phase: <strong>the two-slot model</strong>.</p>
</div><div class="col-fig">
<div class="fig" data-inline-svg="./fig/L10-patch-fringing.svg" style="max-width:660px; margin:0 auto;"></div>
</div></div>

Note:
Draw the standing wave on the board and let them find the sign flip themselves. Once they see it, patch patterns stop being magic.

---

## Sizing a patch: three formulas, in order

**1 — Width** (the half-power width choice, a compromise between efficiency and higher modes):

$$W = \frac{c}{2f_r}\sqrt{\frac{2}{\varepsilon_r+1}}$$

**2 — Effective permittivity** (some field is in air, so the patch sees less than $\varepsilon_r$):

$$\varepsilon_{\text{eff}} = \frac{\varepsilon_r+1}{2} + \frac{\varepsilon_r-1}{2}\left(1+\frac{12h}{W}\right)^{-1/2}$$

Note:
These are the Hammerstad closed forms. They are curve fits to measured microstrip data, not derivations — say so out loud, it buys credibility.

---

## Sizing a patch: the edge extension

**3 — Length extension.** The fringing field makes the patch look electrically longer than it is:

$$\frac{\Delta L}{h} = 0.412\ \frac{(\varepsilon_{\text{eff}}+0.3)(W/h+0.264)}{(\varepsilon_{\text{eff}}-0.258)(W/h+0.8)}$$

**4 — Physical length.** Resonance needs the *electrical* length to be $\lambda_d/2$, so cut the metal short by $2\Delta L$:

$$L = \frac{c}{2 f_r \sqrt{\varepsilon_{\text{eff}}}} - 2\Delta L$$

<div class="callout">Etch it at $\lambda_d/2$ and it resonates <strong>low</strong>. The fringe is why.</div>

Note:
Typical delta-L is a few percent of L — small, but it moves the resonance by more than a patch's whole bandwidth. That is the punchline.

---

## Worked example — 2.45 GHz on FR-4

<p class="viz-cue">↗ Interactive on the lesson page</p>

$\varepsilon_r = 4.4$, $h = 1.6$ mm, $f_r = 2.45$ GHz, so $c/2f_r = 61.2$ mm.

| Quantity | Work | Result |
| :-- | :-- | :-- |
| $W$ | $61.2\sqrt{2/5.4}$ | $37.3$ mm |
| $\varepsilon_{\text{eff}}$ | $2.7 + 1.7(1+12(1.6)/37.3)^{-1/2}$ | $4.08$ |
| $\Delta L$ | $0.412(1.6)(4.381)(23.55)/[(3.823)(24.09)]$ | $0.74$ mm |
| $L$ | $61.2/\sqrt{4.08} - 2(0.74)$ | $28.8$ mm |

**A 37 x 29 mm rectangle of copper. That is a Wi-Fi antenna.**

Note:
Have them hold a thumbnail up next to it. Then drive the widget: swap FR-4 for alumina and watch the same 2.45 GHz patch drop to 26 x 19 mm.

---

## What the two-slot model predicts

<p class="viz-cue">↗ Interactive on the lesson page</p>

- **Broadside, always.** Both slots radiate in phase along the normal.
- **Hemispherical.** The ground plane kills the back half.

| Cut | Pattern | Beamwidth |
| :-- | :-- | :-- |
| E-plane (across the two slots) | $\cos\!\left(\tfrac{k L_e}{2}\sin\theta\right)$ | very broad — the slots are only $\approx \lambda_0/3$ apart |
| H-plane (along each slot) | $\cos\theta\ \operatorname{sinc}\!\left(\tfrac{k W}{2}\sin\theta\right)$ | $\approx 80^\circ$ |

**Directivity 5 to 8 dBi. Memorize 6.**

Note:
Six dBi is the number to keep. A single patch is a low-gain element — the gain comes later, from putting hundreds of them in an array. Run the widget and slide epsilon_r: the beam never leaves broadside.

---

## The price: bandwidth

<p class="viz-cue">↗ Interactive on the lesson page</p>

A high-$Q$ cavity is narrowband. For VSWR $\le 2$:

$$\text{BW} \approx 3.77\ \frac{\varepsilon_r-1}{\varepsilon_r^{2}}\ \frac{h}{\lambda_0}\ \frac{W}{L}$$

| Substrate at 2.45 GHz | Patch size | Bandwidth |
| :-- | :-- | :-- |
| $\varepsilon_r = 2.2$, $h = 1.6$ mm | $48 \times 40$ mm | $1.5\%$ |
| $\varepsilon_r = 4.4$, $h = 1.6$ mm | $37 \times 29$ mm | $1.1\%$ |
| $\varepsilon_r = 10.2$, $h = 1.6$ mm | $26 \times 19$ mm | $0.6\%$ |

<div class="callout">High $\varepsilon_r$ shrinks the patch and <strong>spends its bandwidth</strong>.</div>

Note:
Demo live: hold f fixed, walk epsilon_r up the list, watch the drawing shrink and the bandwidth pill fall. Then push h up and watch bandwidth recover.

---

## Feeding a patch

- **Inset microstrip line.** The edge is a few hundred ohms; the center is a short. Cut a notch and slide the feed point in until you find $50\ \Omega$. Cheap, coplanar, radiates a little on its own.
- **Coaxial probe.** Pin through the ground plane to the right point inside the patch. Same match logic, no feed radiation, harder to build.
- **Aperture-coupled.** Feed line under a second ground plane, coupled through a slot. Isolates the feed, buys bandwidth, costs a layer.

<div class="callout">Same resonator every time. All you are choosing is <strong>where to tap the standing wave</strong>.</div>

Note:
Tie back to L4: this is the same impedance-matching conversation, just with the tap point as the variable instead of a transformer.

---

## Patches want to be arrays

- One patch: $\approx 6$ dBi, a fat hemispherical beam, useless for radar.
- A hundred patches on the same board: printed in the same etch step, fed by printed lines, steered by phase shifters.
- The element is **flat, light, conformal, and identical to its neighbors** — which is exactly what an array needs.

<div class="callout">The <strong>PHASER</strong> array you will drive in Module 3 is a row of patch elements on a board. Today you learned what one of them is.</div>

Note:
Forward hook to L16 pattern multiplication: element factor equals the patch pattern from this lesson, space factor equals the array geometry from Module 3.

---

## The slot: cut the metal, not the wire

<div class="two-col fig-xwide"><div class="col-text">
<p>Cut a $\lambda/2$ slit in a conducting sheet and drive it across the middle.</p>
<p>The <strong>complement</strong> of a dipole: metal where the dipole is air, air where the dipole is metal.</p>
<p>No protrusion, no drag, nothing to shear off.</p>
</div><div class="col-fig">
<div class="fig" data-inline-svg="./fig/L10-slot-babinet.svg" style="max-width:680px; margin:0 auto;"></div>
</div></div>

Note:
This is the antenna you can put on a Mach-2 airframe. That single sentence sells the whole section.

---

## Babinet: what complementarity buys

$$Z_{\text{slot}}\ Z_{\text{dipole}} = \frac{\eta_0^{2}}{4}$$

- The **pattern shape** carries over from the dipole.
- **Impedance is inverted**: a low-impedance dipole becomes a high-impedance slot.
- **Reactance flips sign**: an inductive dipole is a capacitive slot — so both resonate at the same length.

<div class="callout">One relation, and every dipole result you already own transfers to a slot.</div>

Note:
Emphasize "you already own". They spent L7 on the dipole; Babinet says that work was not single-use.

---

## The 485 ohm number

$$\frac{\eta_0^{2}}{4} = \frac{(377)^2}{4} = 3.55\times10^{4}\ \Omega^2$$

| Complementary dipole | Slot impedance |
| :-- | :-- |
| resonant, $73\ \Omega$ real | $\approx 487\ \Omega$ — quoted as **485** $\Omega$ |
| $73 + j42.5\ \Omega$ | $364 - j212\ \Omega$ |

- A resonant slot is a **near-500 ohm** load. Feeding it from $50\ \Omega$ needs a real transformer.
- Note the sign flip in the second row. Babinet inverts the reactance too.

Note:
Make them do the second row on the board — complex division is where this stops feeling like a slogan.

---

## Polarization turns ninety degrees

- The dipole's **E** field runs **along the wire**.
- The slot's **E** field runs **across the cut**.
- A **horizontal** slot therefore radiates a **vertically** polarized field.

<div class="callout">Want vertical polarization out of a flat skin? Cut a <strong>horizontal</strong> slot. This trips up everyone exactly once.</div>

Note:
Ask them to predict before you tell them. Roughly half will guess wrong, and then they never forget it.

---

## Slots in service

- **Cavity-backed slot.** A slot radiates both ways. Box one side in and you get a one-sided, flush, hemispherical radiator — the standard airframe antenna. The cavity costs you bandwidth.
- **Waveguide slot arrays.** Cut slots along a waveguide wall; each one taps a little power. Spacing sets the beam, offset sets the amplitude taper. Marine and airborne surveillance radars are built this way.
- **Leaky-wave and skin apertures.** Missiles, radomes, anything that cannot afford a bump.

<div class="callout">A slot array is a <strong>ready-made aperture distribution</strong> — Module 3's tapering theory applied with a milling machine.</div>

Note:
Show a marine radar slotted-waveguide photo if you have one loaded. Then forward-point at L24 sidelobe tapering.

---

## The horn: give the waveguide an opening

<div class="two-col fig-xwide"><div class="col-text">
<p>A waveguide carries one mode. Cut it off and it barely radiates — the opening is a fraction of a wavelength and badly mismatched.</p>
<p><strong>Flare it out.</strong> The mode expands, the mismatch smooths out, and you finish with a large, well-illuminated aperture.</p>
<p>By L6's equivalence principle, that aperture field <em>is</em> the source.</p>
</div><div class="col-fig">
<div class="fig" data-inline-svg="./fig/L10-horn-aperture.svg" style="max-width:660px; margin:0 auto;"></div>
</div></div>

Note:
The horn is the cleanest physical realization of everything L6 set up. Say that explicitly — it retroactively justifies the vector-potential work.

---

## Gain from area

$$G = \eta_{ap}\ \frac{4\pi A}{\lambda^{2}}$$

- $A$ is the **physical** aperture; $\eta_{ap}$ is what fraction of it works.
- Horns run $\eta_{ap} \approx 0.5$. Good reflectors reach $0.55$ to $0.7$.
- Gain is set by **area in square wavelengths**. Double the frequency at fixed size, gain climbs $6$ dB.

<div class="callout">This is the same $A_e = G\lambda^2/4\pi$ from L2, read right to left.</div>

Note:
Half. Not 0.9. Ask why a horn throws away half its aperture and let the next two slides answer it.

---

## Worked example — an X-band horn

A pyramidal horn, aperture $20 \times 15$ cm, at $10$ GHz. Take $\eta_{ap} = 0.5$.

| Quantity | Work | Result |
| :-- | :-- | :-- |
| $\lambda$ | $c/f$ | $3.0$ cm |
| $A$ | $0.20 \times 0.15$ | $0.030\ \text{m}^2$ |
| $4\pi A/\lambda^{2}$ | $4\pi(0.030)/(0.03)^2$ | $419$ |
| $G$ | $0.5 \times 419$ | $209 = 23.2$ dBi |
| far field | $2D^2/\lambda$, $D = 25$ cm diagonal | $4.2$ m |

**Note the last row: this horn needs a 4-meter range.**

Note:
The far-field row is the one that bites them in the lab. A hand-sized horn already outruns the bench.

---

## Why flare slowly

- Energy leaves the flare on a **spherical** wavefront centerd near the horn's virtual apex.
- The aperture is **flat**. So the edge is farther from the apex than the center — its phase **lags**.
- That quadratic phase error broadens the beam, fills the nulls, raises the sidelobes, and **costs gain**.
- Longer horn, same aperture ⟹ flatter wavefront ⟹ smaller error.

<div class="callout">Aperture buys gain. <strong>Phase error spends it.</strong></div>

Note:
Same 22.5-degree tolerance idea as the far-field criterion in L5. Different geometry, identical accounting.

---

## The optimum horn

- Make the aperture bigger at fixed length: $4\pi A/\lambda^2$ rises, but $\eta_{ap}$ falls. Gain peaks and then **turns over**.
- The **optimum horn** is that peak — the shortest horn for a given aperture whose edge phase error is still tolerable (roughly $\lambda/4$ in the E-plane, $3\lambda/8$ in the H-plane).
- At the optimum, $\eta_{ap} \approx 0.5$. That is where the number comes from.

<div class="callout">Half your aperture is the <strong>rent you pay</strong> for a horn short enough to carry.</div>

Note:
If they only keep one thing: aperture efficiency is not a fudge factor, it is a design decision with a peak.

---

## The standard-gain horn

- Built to the optimum design, measured at the factory, gain tabulated across the band to a few tenths of a dB.
- It is not a good communication antenna. It is a **known** antenna.
- Use it as the reference in the gain-comparison method: measure the unknown, measure the standard, take the ratio.

<div class="callout">In <strong>L12</strong> the standard-gain horn is the ruler you measure every other antenna against.</div>

Note:
Point at the actual horn in the chamber if the deck is being run in the lab space.

---

## Choosing among the three

| | Patch | Slot | Horn |
| :-- | :-- | :-- | :-- |
| Pattern | broadside hemisphere | dipole-like; one-sided if cavity-backed | directive pencil or fan beam |
| Gain | $5$–$8$ dBi | $2$–$5$ dBi | $10$–$25$ dBi |
| Bandwidth | $1$–$5\%$ | $10$–$20\%$; a few % backed | an octave or more |
| Power | low | moderate | high — it is waveguide |
| Integration | printed, planar, arrays free | flush in an existing skin | bulky, needs a waveguide feed |

Note:
Walk one scenario per column: a CubeSat downlink, a missile telemetry link, a chamber reference. Let them argue.

---

## Key point

<div class="callout">
<p>A <strong>patch</strong> is a leaky resonator: the substrate sets its size and steals its bandwidth.</p>
<p>A <strong>slot</strong> is a dipole turned inside out: same pattern, inverted impedance, rotated polarization.</p>
<p>A <strong>horn</strong> is an aperture: gain is area in square wavelengths, and phase error is what you pay for it.</p>
</div>

Note:
Three sentences. If they can say these back, the lesson landed.

---

## Where this is going

- **L11** — reflectors, Yagis, and arrays: how to get past 25 dBi.
- **L12** — pattern and gain measurement, with the standard-gain horn as the reference.
- **Module 3** — hundreds of patches, phased, steered. The PHASER's elements are exactly the antenna you sized today.

<div class="callout">You have met the element. Next you build the <strong>array</strong>.</div>

Note:
Close on the PHASER. Every patch equation from today reappears in the element factor when we do pattern multiplication.
