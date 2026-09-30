<!-- .slide: class="title-slide" -->

<div class="title-left">

# ECE 444

Antennas, Phased Arrays, and Radar Systems

## Lesson 13 — Patch, Slot, and Horn Antennas

Fall 2026 · Dr. Neil Rogers

</div>

<div class="title-right">

![USAFA](./img/01-course-intro/USAFA-logo.png)

</div>

---

## Where We Were

- L7: the half-wave dipole — a resonant wire, $73 + j42.5\ \Omega$, $2.15$ dBi.
- L12: loops and monopoles — bent and grounded, but still wire.
- L3: a resonant antenna reflects its wave into a standing wave and is narrowband; a traveling-wave antenna does not, and is wideband.
- L11: the standard-gain horn, one of today's three, was the gain reference.

Today: the patch and the slot are resonant antennas; the horn is a traveling-wave antenna.

Note:
Three lessons of wires, and every one of them sticks out of the airframe. Today's three sit flush or bolt to a waveguide.

---

## Today's Plan

1. The **microstrip patch** — a resonant cavity that radiates from two edges.
2. Sizing one: $\varepsilon_{\text{eff}}$, the edge extension $\Delta L$, and a worked design.
3. The **slot** — Babinet's complement of the dipole.
4. The **horn** — a waveguide flared into an aperture.
5. Choosing among the three.

<div class="callout">We analyze all three as <strong>apertures</strong>: find the field in the opening, integrate it, and read the pattern.</div>

Note:
Three antennas in one lesson. The organizing question every time: what physically radiates, and what does that force the pattern and bandwidth to be? Point back at L6 — the equivalence principle lets us replace an aperture field with equivalent magnetic currents, so we never solve for current on the metal.

---

## The Microstrip Patch

<div class="two-col fig-wide"><div class="col-text">
<p>A copper rectangle, <em>W</em> by <em>L</em>, on a substrate over a ground plane. Patch and ground are a short, wide <strong>microstrip line</strong>, and a transmission line does not radiate.</p>
<p>The wave reflects from both <strong>open ends</strong> into a standing wave, which resonates at $L \approx \lambda_d/2$.</p>
<p>At the open ends the field <strong>fringes</strong> out past the copper, and that field radiates.</p>
</div><div class="col-fig">
<div class="fig" data-inline-svg="./fig/L13-patch-standing-wave.svg" style="max-width:600px; margin:0 auto;"></div>
</div></div>

Note:
Tie it to L3's resonant antenna: the wave reflects off the open end and comes back. Ask why a microstrip trace on a circuit board does not radiate; the same answer covers the middle of the patch. Then L sets the resonance, and W sets the impedance and the H-plane beamwidth.

---

## The Two-Slot Model

<div class="two-col fig-xwide"><div class="col-text">
<p>The cavity field runs <strong>patch to ground</strong> as a half-wave standing wave, so it points <strong>down at one open edge and up at the other</strong>.</p>
<p>At each edge the field <strong>fringes</strong> past the conductor. The vertical parts are opposite and <strong>cancel</strong>. The horizontal parts point the same way and <strong>add</strong>.</p>
<p>Two edges $\lambda_d/2$ apart radiate in phase: the <strong>two-slot model</strong>.</p>
</div><div class="col-fig">
<div class="fig" data-inline-svg="./fig/L13-patch-fringing.svg" style="max-width:660px; margin:0 auto;"></div>
</div></div>

Note:
Draw the standing wave on the board and let them find the sign flip themselves. Once they see it, the patch pattern follows without memorization.

---

## Two Radiating Edges, Not Four

<div class="two-col fig-wide"><div class="col-text">
<p>Along each <strong>end</strong> the field is uniform, and both ends point the same way, so they add.</p>
<p>Along each <strong>side</strong> the field reverses halfway, so the two halves cancel.</p>
<p>The beam points broadside.</p>
</div><div class="col-fig">
<div class="fig" data-inline-svg="./fig/L13-patch-edges.svg" style="max-width:520px; margin:0 auto;"></div>
</div></div>

Note:
The question someone always asks: a rectangle has four edges, so why two slots? Point at the side arrows: the standing wave runs along L, so each side sees the field swing from outward to inward. The side edges are the main source of cross-polarization.

---

## Sizing a Patch: Width and Permittivity

**1 — Width.** $W$ sets the edge resistance and the efficiency; the formula is the standard compromise with higher-order modes:

$$W = \frac{c}{2f_r}\sqrt{\frac{2}{\varepsilon_r+1}}$$

**2 — Effective permittivity** (some field is in air, so the patch sees less than $\varepsilon_r$):

$$\varepsilon_{\text{eff}} = \frac{\varepsilon_r+1}{2} + \frac{\varepsilon_r-1}{2}\left(1+\frac{12h}{W}\right)^{-1/2}$$

Note:
These are the Hammerstad closed forms. They are curve fits to measured microstrip data, not derivations — say so out loud, so students treat them as design equations rather than physics.

---

## Sizing a Patch: Edge Extension and Length

**3 — Length extension.** The fringing field makes the patch look electrically longer than it is:

$$\frac{\Delta L}{h} = 0.412\ \frac{(\varepsilon_{\text{eff}}+0.3)(W/h+0.264)}{(\varepsilon_{\text{eff}}-0.258)(W/h+0.8)}$$

**4 — Physical length.** $L$ sets the frequency, and resonance requires an *electrical* length of $\lambda_d/2$, so the metal is cut short by $2\Delta L$:

$$L = \frac{c}{2 f_r \sqrt{\varepsilon_{\text{eff}}}} - 2\Delta L$$

<div class="callout">A 1% error in $L$ moves the resonance 1%, about a patch's whole bandwidth.</div>

Note:
Typical delta-L is a few percent of L. That is small, but it moves the resonance by more than a patch's whole bandwidth.

---

## Worked Example — 2.45 GHz on FR-4

<p class="viz-cue">↗ Interactive on the lesson page</p>

$\varepsilon_r = 4.4$, $h = 1.6$ mm, $f_r = 2.45$ GHz, so $c/2f_r = 61.2$ mm.

| Quantity | Work | Result |
| :-- | :-- | :-- |
| $W$ | $61.2\sqrt{2/5.4}$ | $37.3$ mm |
| $\varepsilon_{\text{eff}}$ | $2.7 + 1.7(1+12(1.6)/37.3)^{-1/2}$ | $4.08$ |
| $\Delta L$ | $0.412(1.6)(4.381)(23.55)/[(3.823)(24.09)]$ | $0.74$ mm |
| $L$ | $61.2/\sqrt{4.08} - 2(0.74)$ | $28.8$ mm |

The design is a $37 \times 29$ mm rectangle of copper, the size of a typical Wi-Fi antenna.

Note:
Have them hold a thumbnail up next to it. Then run the widget: swap FR-4 for alumina and the same 2.45 GHz patch drops to 26 x 19 mm.

---

## Two-Slot Pattern

<p class="viz-cue">↗ Interactive on the lesson page</p>

- The beam is **broadside** at every size, because both slots radiate in phase along the normal.
- The pattern is **hemispherical**, because the ground plane suppresses the back half.

| Cut | Pattern | Beamwidth |
| :-- | :-- | :-- |
| E-plane (across the two slots) | $\cos\!\left(\tfrac{k L_e}{2}\sin\theta\right)$ | very broad — the slots are only $\approx \lambda_0/4$ apart |
| H-plane (along each slot) | $\cos\theta\ \operatorname{sinc}\!\left(\tfrac{k W}{2}\sin\theta\right)$ | $\approx 80^\circ$ |

Directivity is 5 to 8 dBi, typically 6.

Note:
Six dBi is the number to keep. A single patch is a low-gain element; the gain comes later, from putting hundreds of them in an array. Run the widget and slide epsilon_r: the beam never leaves broadside.

---

## Patch Bandwidth

<p class="viz-cue">↗ Interactive on the lesson page</p>

A high-$Q$ cavity is narrowband. For VSWR $\le 2$:

$$\text{BW} \approx 3.77\ \frac{\varepsilon_r-1}{\varepsilon_r^{2}}\ \frac{h}{\lambda_0}\ \frac{W}{L}$$

| Substrate at 2.45 GHz | Patch size | Bandwidth |
| :-- | :-- | :-- |
| $\varepsilon_r = 2.2$, $h = 1.6$ mm | $48 \times 40$ mm | $1.5\%$ |
| $\varepsilon_r = 4.4$, $h = 1.6$ mm | $37 \times 29$ mm | $1.1\%$ |
| $\varepsilon_r = 10.2$, $h = 1.6$ mm | $26 \times 19$ mm | $0.6\%$ |

<div class="callout">High $\varepsilon_r$ shrinks the patch and <strong>reduces its bandwidth</strong>.</div>

Note:
Demo live: hold f fixed, step epsilon_r up the list, and the drawing shrinks and the bandwidth pill falls. Then increase h and the bandwidth recovers.

---

## Where to Tap the Standing Wave

<div class="two-col fig-wide"><div class="col-text">
<p>The voltage between patch and ground is largest at the ends and zero at the center.</p>
<p>So the input resistance falls from a few hundred ohms at the edge to zero at the center.</p>
<p>Feed at the point where it reads $50\ \Omega$.</p>
</div><div class="col-fig">
<div class="fig" data-inline-svg="./fig/L13-patch-feed-position.svg" style="max-width:600px; margin:0 auto;"></div>
</div></div>

Note:
Tie back to L4: this is the same impedance-matching problem, with the tap point as the variable instead of a transformer. The curve is the transmission-line model for the worked-example patch; substrate loss moves the real point a little toward the edge.

---

## Three Ways to Feed a Patch

<div class="fig" data-inline-svg="./fig/L13-patch-feeds.svg" style="max-width:900px; margin:0 auto;"></div>

- **Inset line.** Notches let a printed line reach the $50\ \Omega$ point. It is inexpensive, and the line radiates a little.
- **Coaxial probe.** A pin from below the ground plane touches the patch at that point. It does not radiate, but needs a soldered via.
- **Aperture coupling.** A line on a second board, below the ground plane, couples through a slot. It shields the feed and widens the band, but adds a layer.

Note:
Nothing on the aperture-coupled patch touches the patch: the feed line's field comes up through the slot. The ground plane is the shared middle layer between the two boards.

---

## Patches as Array Elements

<div class="fig" data-inline-svg="./fig/L13-patch-array.svg" style="max-width:600px; margin:0 auto;"></div>

- One patch gives about $6$ dBi with a broad beam, not enough gain for a radar.
- Many identical patches etch in one step, and phase shifters steer their combined beam.

Note:
The PHASER array we use in Module 3 is a row of eight patches on a board, each behind its own phase shifter.
Forward hook to L16 pattern multiplication: element factor equals the patch pattern from this lesson, space factor equals the array geometry from Module 3.

---

## The Slot Antenna

<div class="two-col fig-xwide"><div class="col-text">
<p>A slot is a $\lambda/2$ slit in a metal sheet, fed across the middle.</p>
<p>It is the <strong>complement</strong> of a dipole: metal where the dipole is air, and air where the dipole is metal.</p>
<p>Its ends are <strong>shorted</strong>, so the field across the gap is zero there and largest at the feed.</p>
<p>It is flush: no protrusion, no drag.</p>
</div><div class="col-fig">
<div class="fig" data-inline-svg="./fig/L13-slot-field.svg" style="max-width:600px; margin:0 auto;"></div>
</div></div>

Note:
This is the antenna that can sit on a Mach-2 airframe, which motivates the whole section. The slit is a short line shorted at both ends, the mirror of the patch's line open at both ends; the feed sits where the voltage is largest and the current smallest, which is why the impedance is high.

---

## Babinet's Principle

$$Z_{\text{slot}}\ Z_{\text{dipole}} = \frac{\eta_0^{2}}{4}$$

- The **pattern shape** carries over from the dipole.
- **Impedance is inverted**: a low-impedance dipole becomes a high-impedance slot.
- **Reactance flips sign**: an inductive dipole is a capacitive slot — so both resonate at the same length.

<div class="callout">That one relation carries the dipole results of L7 over to the slot.</div>

Note:
They spent L7 on the dipole; Babinet carries that work over to the slot without redoing it.

---

## The 485 Ω Slot

$$\frac{\eta_0^{2}}{4} = \frac{(377)^2}{4} = 3.55\times10^{4}\ \Omega^2$$

| Complementary dipole | Slot impedance |
| :-- | :-- |
| resonant, $73\ \Omega$ real | $\approx 487\ \Omega$ — quoted as **485** $\Omega$ |
| $73 + j42.5\ \Omega$ | $364 - j212\ \Omega$ |

- A resonant slot is a **near-$500\ \Omega$** load. Feeding it from $50\ \Omega$ needs a matching transformer.
- The second row shows the sign flip: Babinet inverts the reactance too.

Note:
Make them do the second row on the board — complex division is where the relation becomes concrete.

---

## Slot Polarization

- The dipole's **E** field runs **along the wire**.
- The slot's **E** field runs **across the cut**.
- A **horizontal** slot therefore radiates a **vertically** polarized field.

<div class="callout">Students most often reverse this result: the slot's <strong>E</strong> field is <strong>perpendicular</strong> to the cut, not along it.</div>

Note:
Ask them to predict before you tell them. Many will guess wrong, which is what makes the correction stick.

---

## Slots in Service

<div class="fig" data-inline-svg="./fig/L13-slot-service.svg" style="max-width:720px; margin:0 auto;"></div>

- **Cavity-backed slot.** A cavity behind the slot makes it one-sided and flush, the standard airframe antenna, but narrows the band.
- **Waveguide slot array.** Each slot couples out a little power; its offset from the centerline sets how much, so the wall carries the taper.

Note:
Show a marine radar slotted-waveguide photo if you have one loaded. Leaky-wave and skin apertures appear on missiles, radomes, and any surface that cannot carry a protrusion. A slot array is a ready-made aperture distribution: Module 3's tapering theory, realized in the waveguide wall. Forward-point at L24 sidelobe tapering.

---

## The Horn Antenna

<div class="fig" data-inline-svg="./fig/L13-horn-flare.svg" style="max-width:720px; margin:0 auto;"></div>

- An open-ended waveguide is small and badly matched: most of the power reflects.
- Flaring the walls makes the transition gradual, so the wave flows out through a large aperture.
- By L6's equivalence principle, that aperture field *is* the source.

Note:
The horn is the lesson's traveling-wave antenna: nothing sends the wave back, so there is no sharp resonance and a standard-gain horn covers an octave. It is also the cleanest physical realization of everything L6 set up; say that explicitly.

---

## Aperture Gain

<div class="two-col fig-wide"><div class="col-text">
<p>$$G = \eta_{\text{ap}}\ \frac{4\pi A}{\lambda^{2}}$$</p>
<p>Gain counts the <strong>square wavelengths</strong> in the aperture. Double the frequency and four times as many fit: $+6$ dB.</p>
<p>Horns run $\eta_{\text{ap}} \approx 0.5$; good reflectors reach $0.55$ to $0.7$.</p>
</div><div class="col-fig">
<div class="fig" data-inline-svg="./fig/L13-horn-squares.svg" style="max-width:600px; margin:0 auto;"></div>
</div></div>

Note:
This is the same A_e = G lambda^2 / 4 pi from L2, read right to left. The value is 0.5, not 0.9. Ask why a horn gives up half its aperture, and let the next two slides answer.

---

## Worked Example — an X-Band Horn

A pyramidal horn, aperture $20 \times 15$ cm, at $10$ GHz. Take $\eta_{\text{ap}} = 0.5$.

| Quantity | Work | Result |
| :-- | :-- | :-- |
| $\lambda$ | $c/f$ | $3.0$ cm |
| $A$ | $0.20 \times 0.15$ | $0.030\ \text{m}^2$ |
| $4\pi A/\lambda^{2}$ | $4\pi(0.030)/(0.03)^2$ | $419$ |
| $G$ | $0.5 \times 419$ | $209 = 23.2$ dBi |
| far field | $2D^2/\lambda$, $D = 25$ cm diagonal | $4.2$ m |

The last row shows that this horn needs a $4.2$ m range.

Note:
The far-field row is the one that constrains the lab: a hand-sized horn already needs more range than the bench provides.

---

## Phase Error in the Aperture

<div class="two-col fig-wide"><div class="col-text">
<p>The wave leaves the apex on a <strong>spherical</strong> front, but the aperture is <strong>flat</strong>.</p>
<p>The edge is farther from the apex, so its phase <strong>lags</strong>: a parabola across the aperture.</p>
<p>That error broadens the beam, fills the nulls, and <strong>reduces the gain</strong>. A longer horn reduces it.</p>
</div><div class="col-fig">
<div class="fig" data-inline-svg="./fig/L13-horn-phase.svg" style="max-width:620px; margin:0 auto;"></div>
</div></div>

Note:
This is the same 22.5-degree tolerance as the far-field criterion in L5, applied to a different geometry.

---

## The Optimum Horn

<div class="fig" data-inline-svg="./fig/L13-horn-three.svg" style="max-width:720px; margin:0 auto;"></div>

- Same flare length, wider mouth: more area, but the edges lag more.
- Past about $\lambda/4$ of edge lag, the edge strips cancel the center: gain falls.

Note:
Flare length is along the axis, apex to mouth. Each strip of the mouth adds an arrow turned by its lag; the red arrow is the total straight ahead. Narrow: few arrows, short total. Optimum: more arrows, still gaining. Too wide: the outer arrows point backward and the total shrinks. The optimum is the best width for a given length; a longer horn moves it wider and higher. The full curve (in the reading) peaks at lambda/4 in the E-plane and 3 lambda/8 in the H-plane; 0.78 x 0.78 x 0.81 is about 0.5, which is eta_ap.

---

## The Standard-Gain Horn

<div class="fig" data-inline-svg="./fig/L13-horn-comparison.svg" style="max-width:700px; margin:0 auto;"></div>

- Built to the optimum design and calibrated at the factory to a few tenths of a dB.
- In L11 it was the reference: same spot, swap antennas, and the dB difference in power is the dB difference in gain.

Note:
Point at the actual horn in the chamber if the deck is being run in the lab space. Its value is not performance but a known gain.

---

## Choosing Among the Three

| | Patch | Slot | Horn |
| :-- | :-- | :-- | :-- |
| Pattern | broadside hemisphere | dipole-like; one-sided if cavity-backed | directive pencil or fan beam |
| Gain | $5$–$8$ dBi | $2$–$5$ dBi | $10$–$25$ dBi |
| Bandwidth | $1$–$5\%$ | $10$–$20\%$; a few % backed | an octave or more |
| Power | low | moderate | high (waveguide-fed) |
| Integration | printed, planar, arrays etched in one step | flush in an existing skin | bulky, needs a waveguide feed |

Note:
Walk one scenario per column: a CubeSat downlink, a missile telemetry link, a chamber reference. Let them argue.

---

## Key Points

<div class="callout">
<p>A <strong>patch</strong> is a resonant cavity that radiates from its edges: the substrate sets its size and its bandwidth.</p>
<p>A <strong>slot</strong> is the complement of a dipole: it has the same pattern shape, an inverted impedance, and rotated polarization.</p>
<p>A <strong>horn</strong> is an aperture: gain is area in square wavelengths, and phase error is what reduces it.</p>
</div>

Note:
These three sentences are the takeaway; students should be able to restate them.

---

## Where This Is Going

- **L14** — reflectors, Yagis, and arrays: gain past 25 dBi, and the close of Module 2.
- **Module 3** — arrays of hundreds of phased, steered patches. The PHASER's elements are the patch we sized today.

<div class="callout">The patch is the element; Module 3 builds the <strong>array</strong>.</div>

Note:
Close on the PHASER. Every patch equation from today reappears in the element factor when we do pattern multiplication. The standard-gain horn thread closed today rather than opening one: they already used it as a reference in L11, and now they know why its gain is known.
