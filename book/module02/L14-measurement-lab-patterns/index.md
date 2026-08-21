# L14 - Measurement Lab 2: Radiation Patterns

:::{admonition} Slides
:class: slides
<a href="../../slides/L14-measurement-lab-patterns.html" target="_blank" rel="noopener">html slides</a>
<a href="../../slides/L14-measurement-lab-patterns.html?print-pdf" target="_blank" rel="noopener">pdf slides</a>
<a href="../../slides/L14-measurement-lab-patterns.md" target="_blank" rel="noopener">raw markdown slides</a>
:::

## Learning Objectives

<ol class="lo-list lo-sublist" style="--module: '2'; --lo: '7'">
  <li>I can set up a pattern measurement — source antenna, rotating antenna under test, one fixed frequency, adequate separation — and verify that the range geometry is honest before I trust any data.</li>
  <li>I can acquire principal-plane pattern cuts and normalize, plot, and annotate them correctly in dB down from the peak.</li>
  <li>I can extract half-power beamwidth, first sidelobe level, front-to-back ratio, and gain by the comparison method from measured pattern data.</li>
  <li>I can measure polarization by rotating the source antenna, compute cross-polarization discrimination, and state how the system's dynamic range limits every one of these numbers.</li>
</ol>

Last lesson you stood at the terminals and asked whether power gets *into* the antenna. Today you walk 3 meters away and ask where that power *goes*. Same antenna, the other half of its description — and this time the answer is not a single number but a curve, with a beamwidth, a sidelobe structure, a back level, a polarization, and a hard limit on how much of that curve is real. Everything Module 2 predicted, you now measure.

## Part 1: Background

A radiation pattern is the far-field power of an antenna as a function of angle. You cannot measure "the far field" directly; you measure **received power at a fixed distance while you rotate the antenna**, and you rely on the range being far enough away that the pattern has stopped changing shape with distance. Lesson 12 derived that condition — the phase across the aperture must be flat to within about $\pi/8$, which gives $r \ge 2D^2/\lambda$ with $D$ the antenna's largest dimension. Today you verify it with a tape measure and then take data.

Reciprocity does the rest of the work. The pattern you measure with the antenna under test (AUT) receiving is identical to the pattern it would transmit, so it does not matter which end you put the AUT on. In this lab the source transmits and the AUT receives, because the AUT is the thing that rotates and you would rather not run transmit power through a rotary joint.

:::{admonition} Key Point
:class: key-concept
A pattern measurement produces two independent products: a **normalized shape** (dB down from the peak, from the rotation sweep) and an **absolute gain** (dBi, from a comparison against a known antenna). Neither one gives you the other. You need both sweeps.
:::

## Part 2: Equipment and range setup

The chain has four links, and each one has a characteristic way of ruining your day.

| Stage | What it must do | What goes wrong |
| :-- | :-- | :-- |
| Transmitter | one frequency, stable output level | level drift reads as pattern structure |
| Source antenna | known gain, clean known polarization | its own cross-pol leaks into your cross-pol cut |
| AUT on rotator | rotate about one axis, centered | tilted or off-center cut, biased HPBW |
| Receiver | log power at each angle | unrecorded settings, unusable data |

The hardware is flexible. A signal generator into a source horn with a spectrum analyzer on the AUT works. So does an SDR-based transmitter and receiver: the course provides a **Pluto-SDR transmit/receive tool** that runs the measure-rotate-record loop and writes an angle-versus-power file, which is the option most sections will use. The physics does not care which you pick — the acquisition discipline in Part 3 does.

Your bench range for this lab:

- Frequency $f = 2.45\ \text{GHz}$, so $\lambda = 12.2\ \text{cm}$.
- **AUT**: a pyramidal horn with a $24 \times 17\ \text{cm}$ aperture.
- **Reference**: a calibrated standard-gain horn, $34 \times 25\ \text{cm}$ aperture, $G_{\text{ref}} = 15.0\ \text{dBi}$.
- Separation $r = 3.0\ \text{m}$, both antennas at the same height, absorber on the floor at the midpoint.

:::{admonition} Worked example — is 3.0 m far enough?
:class: tip
Run all three far-field criteria on both antennas, not just the famous one.

For the AUT, $D$ is the aperture **diagonal**, not a side:

$$D = \sqrt{(0.24)^2 + (0.17)^2} = 0.294\ \text{m}$$

$$\frac{2D^2}{\lambda} = \frac{2(0.294)^2}{0.1224} = 1.41\ \text{m}, \qquad 5D = 1.47\ \text{m}, \qquad 10\lambda = 1.22\ \text{m}$$

The binding criterion is $5D$, not $2D^2/\lambda$ — for a physically small antenna the aperture-phase rule is often not the one that decides. The AUT needs 1.5 m and you have 3.0 m.

Now the reference horn, $D = \sqrt{(0.34)^2 + (0.25)^2} = 0.422\ \text{m}$:

$$\frac{2D^2}{\lambda} = \frac{2(0.422)^2}{0.1224} = 2.91\ \text{m}$$

The **reference** sizes the range, and 3.0 m clears it by only 3%. That is the honest answer, and it belongs in your report: the gain comparison is the measurement standing closest to the edge of the far field.
:::

```{note}
Both antennas must be in each other's far field, and both must see the same illumination. Set the heights with a tape, not by eye. A 5 cm height mismatch over a 3 m range is a 1° pointing error, which is small — but it is a *bias*, and biases do not average out over repeated sweeps.
```

## Part 3: Procedure

Work through these in order. Do not skip step 5 — it decides which of your later numbers survive.

1. **Set up and align.** Both antennas at the same height, boresights facing, co-polarized. Absorber on the specular floor-bounce point at the midpoint of the range.
2. **Set one frequency and log it.** Fix the transmit level, the receiver's resolution bandwidth, and the averaging. Retuning anything mid-sweep invalidates the cut.
3. **Peak up first.** Rotate the AUT until received power is maximum, and *define that angle as* $0^\circ$. A pattern referenced to the wrong angle is worthless, and every extracted number depends on the peak.
4. **Choose the angle step.** The rule of thumb is **step $\le$ HPBW/5**. This horn's beam is about $40^\circ$, so $8^\circ$ would satisfy the rule for beamwidth — but the sidelobes are much narrower than the beam, so take $2^\circ$ and resolve them too. Coarse steps do not just add noise; they systematically miss peaks and nulls.
5. **Measure the noise floor.** Turn the source off, leave everything else exactly as it is, and record the receiver's reading. This single number sets the credibility of your entire data set.
6. **Sweep the E-plane cut**, a full $\pm 180^\circ$ if your rotator allows it, otherwise $\pm 90^\circ$ plus a back-lobe spot check at $180^\circ$.
7. **Sweep the H-plane cut**, either by rotating both antennas $90^\circ$ about the range axis or by remounting the AUT on its side.
8. **Repeat one cut.** Two sweeps of the same cut that disagree by 1 dB have just told you your real uncertainty — better than any error propagation you could write down.
9. **Gain comparison.** Swap the AUT for the reference horn, peak it up, record the level. Change *nothing else*: same range, same cables, same source, same transmit level.
10. **Polarization.** Reinstall the AUT, rotate the **source** $90^\circ$ about the range axis, and re-sweep. That cut is your cross-pol pattern.

```{note}
Why rotate the source and not the AUT for the cross-pol cut? Rotating the AUT would change which plane you are cutting at the same time as it changes the polarization, and you would not be able to separate the two effects. Rotate the source, and the only thing that changes is polarization.
```

## Part 4: Reduction — getting numbers out

**Normalize first.** Subtract the peak level from every sample. Your data is now in dB down from the peak, and the transmit power, cable loss, and range loss have all dropped out. Plot it twice: **polar dB** shows the shape at a glance, **rectangular dB** lets you read values off an axis. Never plot pattern data on a linear scale — a $-13\ \text{dB}$ sidelobe is 5% of peak and simply disappears.

Then extract four things from the shape:

| Quantity | How you read it | Sanity range |
| :-- | :-- | :-- |
| HPBW | angle between the two $-3\ \text{dB}$ crossings, interpolated | matches $\approx 26000/(\theta_E \theta_H)$ vs. gain |
| First sidelobe | level of the first lobe past the first null | $-13$ to $-25\ \text{dB}$ |
| Front-to-back | peak minus the level at $180^\circ$ | 15 to 25 dB for a horn |
| Null depth | the minimum between lobes | usually a lie — see Part 5 |

Interpolate between samples for the $-3\ \text{dB}$ crossings. Snapping to the nearest grid point throws away most of the precision your $2^\circ$ step bought you.

:::{admonition} Worked example — one E-plane cut, reduced
:class: tip
The peak reads $-35.6\ \text{dBm}$ at $0^\circ$, so the $-3\ \text{dB}$ level is $-38.6\ \text{dBm}$. Interpolating between samples puts the crossings at $-19.8^\circ$ and $+20.2^\circ$:

$$\theta_\text{HP} = 20.2 - (-19.8) = 40.0^\circ$$

The first sidelobe peaks at $-51.4\ \text{dBm}$, and the level at $180^\circ$ is $-54.0\ \text{dBm}$:

$$\text{SLL} = -51.4 - (-35.6) = -15.8\ \text{dB}, \qquad \text{F/B} = -35.6 - (-54.0) = 18.4\ \text{dB}$$

Cross-check the beamwidths against the gain: with an H-plane HPBW of $42^\circ$, $26000/(40 \times 42) = 15.5$, or $11.9\ \text{dBi}$. Hold that thought for the gain comparison below.
:::

**Gain by comparison** is Lesson 12's substitution method, and in dB it is one subtraction. Everything common to the two measurements — transmit power, path loss, cable loss, source gain — cancels:

$$G_{\text{AUT}} = G_{\text{ref}} + \left( P_{\text{AUT}} - P_{\text{ref}} \right)$$

:::{admonition} Worked example — gain and XPD
:class: tip
The reference horn reads $-32.4\ \text{dBm}$ at its peak; the AUT reads $-35.6\ \text{dBm}$:

$$G_{\text{AUT}} = 15.0 + (-35.6 + 32.4) = 15.0 - 3.2 = 11.8\ \text{dBi}$$

Predicted from the aperture with $\eta_{ap} = 0.5$: $G = 0.5 \cdot 4\pi(0.0408)/(0.1224)^2 = 17.1$, or $12.3\ \text{dBi}$. Measured is 0.5 dB low, and the reference horn's own calibration is good to about 0.5 dB — that is agreement, and your report should say so rather than inventing a physical cause.

Rotating the source $90^\circ$ drops the boresight level to $-59.9\ \text{dBm}$:

$$\text{XPD} = -35.6 - (-59.9) = 24.3\ \text{dB}$$

A well-behaved linear antenna gives 20 to 30 dB. Below about 15 dB, suspect a tilted mount before you blame the antenna.
:::

## Part 5: Dynamic range — how much of your pattern is real

Your receiver has a noise floor. The measured power at every angle is the true signal **plus** that floor, added in power, so no measured level can ever sit meaningfully below it. This one fact governs which of your extracted numbers you are allowed to believe.

Work it out for this lab. Peak at $-35.6\ \text{dBm}$, floor at $-78\ \text{dBm}$ with the source off: your **dynamic range is 42.4 dB**. Any pattern feature within a few dB of $-42.4\ \text{dB}$ relative is not a measurement of the antenna; it is a measurement of your receiver.

The widget below makes the damage concrete. It takes a known pattern — a uniform $8\lambda$ aperture, first sidelobe exactly $-13.3\ \text{dB}$, HPBW $6.3^\circ$ — and "measures" it through a receiver with the dynamic range you choose. Drag the floor from $-45\ \text{dB}$ up toward $-15\ \text{dB}$ and watch the three readouts separately: the beamwidth barely moves, the first sidelobe creeps upward by about a dB as the noise adds to it, and the nulls stop dead at the floor. Then switch averaging from 1 sweep to 16 and notice what averaging does and does not buy you.

<iframe src="../../viz/pattern-floor.html"
        width="100%" height="498"
        style="border: 1px solid #cddce9; border-radius: 6px;"
        loading="lazy"
        title="A true radiation pattern compared with the same pattern measured through a receiver with a finite noise floor">
</iframe>

Three lessons come out of that widget, and they are the reason this lab exists:

- **Beamwidth is robust.** It is measured 3 dB down from the peak, where the signal is 40 dB above any sane floor. Trust it first.
- **Sidelobe levels are conditional.** A lobe 10 dB above the floor reads about 0.4 dB high; a lobe 3 dB above the floor reads 3 dB high and is nearly meaningless. Quote the floor next to every sidelobe number.
- **Null depths are almost always fiction.** A null measures your floor, not the antenna. Averaging 16 sweeps smooths the fuzz — incoherent power averaging shrinks the *variance* like $1/N$ — but it leaves the mean noise power exactly where it was. To actually lower the floor you need more transmit power, a narrower resolution bandwidth, or a quieter receiver.

:::{admonition} Key Point
:class: key-concept
A pattern measurement is a dynamic-range measurement in disguise. "The null is at least 25 dB deep, limited by our 42 dB dynamic range" is a defensible engineering sentence. "The null is 25 dB deep" is not.
:::

**The rest of the uncertainty budget.** The floor is the hard limit; these are the everyday errors, and all of them are visible in your data if you look.

| Source | What it looks like | Typical size |
| :-- | :-- | :-- |
| Floor and wall reflections | periodic ripple riding on the whole pattern | $\pm 1\ \text{dB}$ |
| Cable flex on the rotator | slow drift between repeated sweeps | 0.2 to 0.5 dB |
| Pointing misalignment | peak reads low, HPBW biased | 0.2 dB at HPBW/8 off |
| Reference tolerance | a fixed offset on every gain number | 0.3 to 0.5 dB |

Ripple is diagnostic rather than merely annoying: a reflected path 20 dB below the direct path adds and subtracts to give $20\log_{10}(1.1) = +0.8\ \text{dB}$ and $20\log_{10}(0.9) = -0.9\ \text{dB}$, a peak-to-peak ripple of about 1.7 dB. Count the ripples per degree and you can work backward to where the reflection is coming from.

## Part 6: Deliverables

Turn in the following, as one document.

1. **Two principal-plane cuts** (E-plane and H-plane), plotted in polar dB, normalized to the peak, with the angle convention and the frequency labeled on each.
2. **An extracted table** — HPBW, first sidelobe level, front-to-back ratio, gain, XPD — with an **uncertainty estimate on every row**. Your repeated sweep from step 8 is the honest basis for most of them.
3. **Your measured noise floor**, stated as a level and as a dynamic range, with one sentence per table row saying whether that number clears the floor and by how much.
4. **A comparison against prediction** — the aperture-formula gain, the $26000/(\theta_E \theta_H)$ beamwidth cross-check, and the datasheet values where you have them — with every discrepancy larger than your uncertainty named and explained.

Unexplained is not the same as unexplainable. A 2 dB gap with a named cause is a better report than a 0.2 dB gap with no discussion.

## Summary

| Idea | What it says | Number to remember |
| :-- | :-- | :-- |
| $r \ge 2D^2/\lambda$ | far-field separation, largest dimension $D$ | check $5D$ and $10\lambda$ too |
| Angle step | resolve the beam and the sidelobes | step $\le$ HPBW/5 |
| Normalization | pattern shape is always relative to the peak | dB down from peak |
| $\theta_\text{HP}$ | angle between the $-3\ \text{dB}$ crossings, interpolated | robust, trust it first |
| $G_{\text{AUT}} = G_{\text{ref}} + (P_{\text{AUT}} - P_{\text{ref}})$ | gain by comparison is one subtraction in dB | accuracy = reference + alignment |
| XPD | co-pol minus cross-pol at boresight | 20 to 30 dB is healthy |
| Dynamic range | peak level minus measured noise floor | 42 dB on this bench |
| Null depth | measures the floor, not the antenna | quote it as a lower bound |

## Practice

- <a href="../../practice/ECE444_L14_Practice_blank.pdf" target="_blank" rel="noopener">Problem set (PDF)</a>
- <a href="../../practice/ECE444_L14_Practice_SOLUTIONS.pdf" target="_blank" rel="noopener">Solutions (PDF)</a>

## Where this is going

This lab is the **dress rehearsal for the midterm Antenna Pattern Measurement project, due at L20**. Same range, same extraction, same uncertainty discussion — but with more antennas, a written analysis, and no procedure handed to you. Everything you get wrong today is free; get it wrong in three weeks and it costs you.

Module 2 closes here, and it closes with a complete loop. You can predict an antenna's pattern from its geometry, simulate it, and now measure it, with an honest statement of how much of the measurement to believe. Lesson 15 opens Module 3 by going back to the beginning of that loop and asking a sharper question: the aperture *size* set the beamwidth you just measured, but what set the sidelobe level? The answer is the illumination across the aperture, and choosing it deliberately is how every high-performance antenna and phased array is designed.
