<!-- .slide: class="title-slide" -->

<div class="title-left">

# ECE 444

Antennas, Phased Arrays, and Radar Systems

## Lesson 24 — Sidelobes and Tapering Theory

Fall 2026 · Dr. Neil Rogers

</div>

<div class="title-right">

![USAFA](./img/01-course-intro/USAFA-logo.png)

</div>

---

## Where we were

- **L15** gave the Fourier picture: pattern is the transform of the aperture illumination.
- **L20** gave the beamwidth rule $0.886\ \lambda/(Nd\cos\theta_0)$ — size sets the main lobe.
- **L22** and **L23** put you on the bench, and your sweep showed sidelobes near $-13$ dB at about $\pm 22^\circ$.
- Those sidelobes came from a decision nobody made deliberately: all eight elements at 100%.

<div class="callout">
Sidelobe level is set by the <strong>shape</strong> of the illumination, and shape is something you control.
</div>

Note:
Open by pointing back at their own measured trace from last lesson. The pair of
lobes at plus and minus twenty-two degrees is not a flaw in the hardware. Today
we show it is a choice, and we price the alternatives.

---

## Today's plan

1. Why an untapered aperture has sidelobes at all.
2. The three taper families: cosine on pedestal, Chebyshev, Taylor.
3. The three costs, quantified for eight elements.
4. Designing to a stated sidelobe specification.
5. Loading a taper into the PHASER's Element Gains.

Note:
Emphasize that item three is where students lose points every year, because two
of the three costs are dB numbers that look interchangeable and are not.

---

## Why sidelobes exist: the Fourier reading

<div class="fig" data-inline-svg="./fig/L24-edge-fourier.svg" style="max-width:820px; margin:0 auto;"></div>

- Uniform illumination is a rectangle, and a rectangle has an abrupt edge.
- An abrupt edge carries content at every space frequency.
- Transform of a rectangle is a sinc, whose ripples decay only as $1/u$.

Note:
The one-line version to say at the board: sharp edges in one domain mean slow
decay in the other. This is the same statement as a square wave needing infinite
harmonics.

---

## Why sidelobes exist: the phasor reading

- At broadside all eight element voltages add in phase.
- At the first null they cancel exactly.
- Just past the null they do not — seven of eight phasors still partly reinforce.
- That residue is the first sidelobe: $-12.8$ dB for $N = 8$, $-13.3$ dB for a continuous aperture.

<div class="callout">
Adding elements narrows the beam and pulls the sidelobes inward. It does <strong>not</strong> lower them. Size sets beamwidth; shape sets sidelobes.
</div>

Note:
Draw the eight phasors on the board at the first sidelobe angle. The picture of
seven-eighths of a circle with one phasor left over is what students remember.

---

## Why low sidelobes matter to a system engineer

| Situation | What comes in through the sidelobes |
| :-- | :-- |
| Search radar over terrain | Ground clutter 40 dB above the target return |
| SATCOM terminal | The adjacent satellite, received and transmitted into |
| Contested spectrum | A jammer that never has to enter your main beam |

- At $-13$ dB the array is one twentieth as sensitive off-axis. That is not enough.
- Tapering lowers **every** sidelobe at once, without knowing where the interference is.
- L27 does the opposite: one deep null aimed at one known direction.

Note:
Make the contrast explicit — tapering is the non-adaptive insurance policy,
null steering is the targeted response. A real system usually does both.

---

## What a taper is

<div class="fig" data-inline-svg="./fig/L24-taper-shapes.svg" style="max-width:720px; margin:0 auto;"></div>

Element amplitudes $a_n$, normalized so the largest is 1. Symmetric about the array center.

Note:
Point out that these are exactly the numbers that go into the Element Gains
column of the GUI. Nothing else about the array changes.

---

## Family 1: cosine on pedestal

$$a(p) = P + (1-P)\cos^2(\pi p), \qquad -\tfrac{1}{2} \le p \le \tfrac{1}{2}$$

| Pedestal $P$ | $a_n$ (%) | First SLL | HPBW |
| :-- | :-- | :-- | :-- |
| 1.00 uniform | 100, 100, 100, 100 | $-12.8$ dB | $13.2^\circ$ |
| 0.25 | 35, 57, 83, 100 | $-25.8$ dB | $16.2^\circ$ |
| 0.08 Hamming | 19, 47, 79, 100 | $-33.0$ dB | $17.9^\circ$ |
| 0.00 Hann | 12, 43, 77, 100 | $-31.8$ dB | $19.1^\circ$ |

Note:
Inner four values only; the array is symmetric. Ask why Hamming beats Hann on
both counts. Answer: the pedestal's own first sidelobe cancels the cosine
term's, which is where the 0.08 comes from.

---

## Family 2: Chebyshev — the defining property

- You state the sidelobe level. The design returns the **narrowest** main lobe that meets it.
- **Equal ripple**: every sidelobe sits at exactly the design level, none higher, none lower.
- A taper whose far sidelobes fall *below* specification spent beamwidth on suppression nobody asked for.

<div class="callout">
Equal ripple is not a coincidence of the math. It is the signature of an optimum: if any lobe were lower, the beam could have been narrower.
</div>

Note:
This is the intuition to sell. Optimality arguments almost always end in
equal ripple, and students will meet the same idea in filter design.

---

## Family 2: Chebyshev — the construction

$$AF(\psi) = T_{7}\left(x_0 \cos\frac{\psi}{2}\right), \qquad x_0 = \cosh\left(\frac{\cosh^{-1}R}{7}\right), \qquad R = 10^{\text{SLL}/20}$$

- $T_{7}$ ripples between $-1$ and $+1$, then grows without bound past $x = 1$.
- The ripples become the equal sidelobes; the growth becomes the main lobe.
- $x_0$ is the stretch that puts the peak of $T_{7}$ at the ratio $R$ you asked for.
- Expanding into element amplitudes is arithmetic, and the widget does it.

Note:
Sketch T-seven on the board between minus one and plus one, then show the
argument x-zero cosine psi over two sliding along it as the observation angle
moves. Everything else follows from that one picture.

---

## Chebyshev on eight elements

| Design | $a_n$ (%) | HPBW | Broadening |
| :-- | :-- | :-- | :-- |
| Uniform | 100, 100, 100, 100 | $13.2^\circ$ | 1.00 |
| $-20$ dB | 58, 66, 88, 100 | $14.8^\circ$ | 1.12 |
| $-30$ dB | 26, 52, 81, 100 | $17.1^\circ$ | 1.30 |
| $-40$ dB | 15, 42, 76, 100 | $18.8^\circ$ | 1.42 |

Every sidelobe of each design lands on its own line, within a tenth of a dB.

Note:
Have them read the trade off the table: seventeen dB of sidelobe suppression for
under four degrees of beamwidth on this array.

---

## Family 3: Taylor

- Chebyshev's practical cousin, used on large radar apertures.
- A true Chebyshev design on a big aperture wants current spikes at the edges, which nobody can build.
- Taylor holds only the first $\bar{n}-1$ sidelobe pairs at the design level and lets the rest decay.

| Taper | $a_n$ (%) | Highest SLL | HPBW | $\eta_t$ |
| :-- | :-- | :-- | :-- | :-- |
| Taylor $-30$ dB, $\bar{n} = 4$ | 29, 53, 82, 100 | $-28.3$ dB | $16.8^\circ$ | 0.853 |

Note:
Two sentences is all this deserves at this level. The n-bar knob is how many
sidelobes you insist on controlling; four to six is the usual range. On only
eight elements the sampled distribution misses the design line by a dB or two.

---

## Three tapers, one axis

<div class="fig" data-inline-svg="./fig/L24-taper-patterns.svg" style="max-width:800px; margin:0 auto;"></div>

Note:
Walk the three curves. The green Chebyshev sidelobes all touch the dashed line.
The orange Hann sidelobes decay away from the beam, which is suppression it did
not need, and it widened the beam to get it.

---

<!-- .slide: class="viz-cue-slide" -->

## Taper explorer

- Five tapers on the course array: $N = 8$, $d/\lambda = 0.481$, broadside.
- Watch three things move together: bar heights, main-lobe width, sidelobe level.
- Readouts: highest sidelobe, HPBW, taper efficiency, peak drop.

<p class="viz-cue">↗ Interactive on the lesson page</p>

Note:
Demo live. Start on uniform, read minus twelve point eight and thirteen point
three. Step to Chebyshev minus twenty, then minus thirty, then minus forty, and
have the class call out the beamwidth before you reveal it. Finish on Hann and
ask which of the two minus-thirty-class designs they would ship.

---

## Cost 1: the beam gets wider

- The aperture is the same size, but the outer elements now contribute less.
- The **effective** aperture shrank, so the beam widened.
- Broadening factor runs about 1.1 at $-20$ dB to 1.7 at $-50$ dB.

<div class="callout">
Beamwidth $\approx 0.886\ \lambda/(Nd)$ times the broadening factor. The taper never changes $N$ or $d$; it changes the multiplier.
</div>

Note:
Tie this back to L20 explicitly. The rule they already know still applies, with
one extra factor they now know how to look up.

---

## Cost 2: taper efficiency — the setup

Array on receive, source on boresight, so every element sees the same signal in phase.

- Output signal voltage $= \sum a_n$ times the per-element voltage.
- Output signal **power** goes as $\left(\sum a_n\right)^2$.
- Each channel adds its own noise, independently, so noise **powers** add: $\sum a_n^2$.

$$\text{SNR} \propto \frac{\left(\sum a_n\right)^2}{\sum a_n^2}$$

Note:
The independence of the channel noise is the step to say out loud. Signals add
as voltages because they are coherent; noise adds as power because it is not.

---

## Cost 2: taper efficiency — the result

Uniform gives $\left(\sum a_n\right)^2 / \sum a_n^2 = N^2/N = N$. Normalize by that:

$$\eta_t = \frac{\left(\sum a_n\right)^2}{N \sum a_n^2}$$

- Same expression comes out of the transmit calculation: peak intensity over total radiated power.
- So $\eta_t$ is the fraction of the uniform array's **directivity** you keep.
- Scale-invariant: multiply every $a_n$ by two and $\eta_t$ does not move.

Note:
Scale invariance is the property that separates this from the next slide. Write
that on the board and leave it there.

---

## Cost 3: the peak of the measured trace drops

The GUI's sweep plots received power and does not renormalize between runs.

$$\text{peak drop} = 20\log_{10}\left(\frac{\sum a_n}{N}\right)$$

- Turning six sliders down throws away signal voltage, so the trace peak falls.
- This is a **coherent voltage loss**, not a directivity loss.
- The noise came down with it, so the array's sensitivity did not fall by this much.

Note:
Stress that this number depends on the overall scale, unlike eta-t. That is the
whole reason they are different quantities.

---

## The two dB numbers are not the same

$$20\log_{10}\left(\frac{\sum a_n}{N}\right) = 10\log_{10}\eta_t + 10\log_{10}\left(\frac{\sum a_n^2}{N}\right)$$

| Preset | Peak drop | of which directivity | of which attenuation |
| :-- | :-- | :-- | :-- |
| Hann | $-4.7$ dB | $-1.2$ dB | $-3.5$ dB |
| Blackman | $-6.1$ dB | $-1.8$ dB | $-4.2$ dB |
| Chebyshev $-30$ dB | $-3.8$ dB | $-0.75$ dB | $-3.0$ dB |

<div class="callout">
Only the middle column is lost antenna performance. The right-hand column is gain you turned down and could turn back up, if 100% were not already full scale.
</div>

Note:
This slide is the one to slow down on. Every year somebody reports the Hann
taper as a four point seven dB directivity loss, which is off by a factor of
three in power.

---

## Designing to a specification

1. Pick the family — Chebyshev for a hard ceiling on a small array, Taylor for a large one, a window when the beamformer only offers presets.
2. Compute the amplitudes; normalize the largest to 1.
3. Price the three costs: broadening, $\eta_t$, peak drop.
4. Check against the hardware's amplitude resolution.

<div class="callout">
Step 4 is not a formality. A taper the hardware cannot set is a taper you do not have.
</div>

Note:
Step four is where the ADAR1000's roughly one percent gain step enters, and it
is why nobody specifies minus fifty dB on this array.

---

## Worked example: $-30$ dB on eight elements

| Quantity | Work | Result |
| :-- | :-- | :-- |
| Voltage ratio | $R = 10^{30/20}$ | $31.62$ |
| Stretch | $x_0 = \cosh(\cosh^{-1}(31.62)/7)$ | $1.181$ |
| Amplitudes | Dolph expansion, normalized | 26, 52, 81, 100 (%) |
| Sums | $\sum a_n$, $\sum a_n^2$ | $5.18$, $3.988$ |

Note:
Walk the first two rows live. The third is the expansion we are not doing by
hand. The fourth is arithmetic they must be able to do in an exam.

---

## Worked example: the numbers

| Quantity | Work | Result |
| :-- | :-- | :-- |
| Taper efficiency | $(5.18)^2 / (8 \times 3.988)$ | $0.841 = -0.75$ dB |
| Peak drop | $20\log_{10}(5.18/8)$ | $-3.8$ dB |
| Beamwidth | measured on the pattern | $17.1^\circ$, broadening 1.30 |
| Sidelobes | every one of them | $-30.0$ dB |

<div class="callout">
Against Hann at $-31.8$ dB: the Chebyshev design is $2^\circ$ narrower and keeps $0.5$ dB more directivity. That is Dolph optimality earning its keep.
</div>

Note:
End on the comparison. The window function was easier to write down and it lost
on every axis that matters.

---

## The whole design space, on one curve

<div class="fig" data-inline-svg="./fig/L24-sll-vs-cost.svg" style="max-width:760px; margin:0 auto;"></div>

- Chebyshev designs run along the curve; windows sit above it.
- The beam costs about $0.2^\circ$ per dB of suppression, right across the range.
- What stops you going deeper is the hardware and the instrument, not the curve.

Note:
Have them read Blackman off the plot: it reaches minus fifty dB with a twenty-one
point seven degree beam, where the Chebyshev design at that level needs twenty
point one. A degree and a half of beamwidth, given away for nothing. Then make
the second point explicitly, because the curve does not show it: a minus fifty dB
design puts its outer elements at nine percent of full scale, where the one
percent gain step is an eleven percent error, and the sweep floor is only
twenty-three dB down anyway.

---

## Loading a taper into the PHASER

$$\text{Rx}\_{n} = 100 \times \frac{a\_{n}}{\max a\_{n}} \quad \text{percent of full scale}$$

- Normalize to the **largest** element, never to the sum — the sliders stop at 100%.
- Turn on **Enforce Symmetric Taper** so a slip on one slider is mirrored.
- Gain word resolves to about 1%: rounding the $-30$ dB design moves its worst sidelobe to $-29.9$ dB.
- You can only go down, so every taper costs peak signal on the trace.

Note:
Have them convert the worked example on the spot: twenty-six, fifty-two,
eighty-one, one hundred, and mirrored. That is what they will type next lesson.

---

## What L25 will measure

| Preset | $a_n$ (%) | Theory HPBW | Measured HPBW | Peak drop | First SLL |
| :-- | :-- | :-- | :-- | :-- | :-- |
| Uniform | 100, 100, 100, 100 | $13.2^\circ$ | $13.1^\circ$ | $0$ dB | $-11$ to $-13$ dBc |
| Hann | 12, 43, 77, 100 | $19.1^\circ$ | $19.5^\circ$ | $-4.7$ dB | below the floor |
| Blackman | 6, 27, 66, 100 | $21.7^\circ$ | $23.1^\circ$ | $-6.1$ dB | below the floor |
| Chebyshev | 4, 23, 62, 100 | $22.9^\circ$ | $24.3^\circ$ | $-6.5$ dB | below the floor |

Measured beamwidths run wide because the sweep steps by the $2.8125^\circ$ phase LSB. The noise floor sits about 23 dB down, so tapered sidelobes give an upper bound, not a value.

Note:
Tell them to copy this table into the lab notebook tonight. Predicting first and
measuring second is the entire structure of next lesson.

---

## A note on the GUI's Chebyshev preset

- Its gain list, 4, 23, 62, 100, is a far more aggressive design than the one we worked.
- The resulting pattern never rises above $-70$ dB anywhere in visible space.
- There is no sidelobe to measure on any equipment in this lab.
- So the prediction that matters for it is beamwidth: $22.9^\circ$ theory, $24.3^\circ$ measured.

<div class="callout">
Specifying 40 dB below what the hardware can show gains nothing measurable, and the beam ends up almost twice as wide as uniform.
</div>

Note:
This is a live example of over-specification, and it is worth naming as such.
The preset is useful for showing a very wide beam, not for showing low sidelobes.

---

## Key point

<div class="callout">
Size sets the beamwidth. <strong>Shape sets the sidelobes.</strong> A taper lowers the sidelobes and widens the beam. Two separate dB numbers fall out of it: <em>taper efficiency</em>, the loss in directivity, and the <em>peak drop</em>, the raw signal you turned down. Keep them apart.
</div>

Note:
If they leave with one sentence, this is it.

---

## Where this is going

- **L25** takes the four presets to the bench, plus the $-30$ dB design you now know how to compute.
- **L26** covers the three failures a taper cannot fix: grating lobes, beam squint, phase quantization.
- **L27** trades the broad suppression for one deep null, aimed where it is needed.
- **Module 4** brings it back for good, because radar clutter arrives through the sidelobes.

Read the Part 5 table on the lesson page before class and copy it into your notebook.

Note:
Close by naming the through-line: everything in Module 3 so far has been about
where the beam points and how wide it is. The rest of the module is about what
else is in the pattern.
