# L12 - Pattern Measurement Theory

:::{admonition} Slides
:class: slides
<a href="../../slides/L12-pattern-measurement-theory.html" target="_blank" rel="noopener">html slides</a>
<a href="../../slides/L12-pattern-measurement-theory.html?print-pdf" target="_blank" rel="noopener">pdf slides</a>
<a href="../../slides/L12-pattern-measurement-theory.md" target="_blank" rel="noopener">raw markdown slides</a>
:::

## Learning Objectives

<ol class="lo-list lo-sublist" style="--module: '2'; --lo: '5'">
  <li>I can state what a valid pattern measurement requires — plane-wave illumination across the antenna under test — and turn that requirement into a minimum range length.</li>
  <li>I can describe the far-field range types — outdoor, anechoic chamber, and compact range — and explain what absorber reflectivity and quiet-zone specifications actually control.</li>
  <li>I can explain how near-field scanning plus a transform substitutes for an impossibly long range, and why that transform is the same Fourier relationship that produced the pattern in the first place.</li>
  <li>I can measure gain by the comparison method with a standard gain horn, and by the two-antenna and three-antenna methods when no calibrated standard exists.</li>
  <li>I can define the standard pattern cuts and the polarization measurements that a complete characterization requires.</li>
</ol>

L10 and L11 built the high-gain antennas and told you their gain from geometry and aperture efficiency. L11 also handed you the midterm project: put an antenna on a positioner and measure its pattern. Every pattern in this course so far came out of an integral — none of them came off an instrument. This lesson is the theory that midterm measurement stands on. It runs the whole problem backwards: instead of computing a far field, you have to *build* one, and every rule that follows is a tolerance on how well you built it.

## Part 1: The range has to supply the plane wave

A pattern is defined by plane-wave illumination. Point a plane wave at the antenna from direction $(\theta,\phi)$, record what comes out of the terminals, repeat for every direction. Reciprocity says the receive pattern equals the transmit pattern, so you may run the measurement in whichever direction is convenient — and everyone runs it in receive, because it is easier to move a receiver than a transmitter.

The catch is that nobody sells plane waves. What you can buy is a **source antenna** at a finite distance, and that radiates a spherical wave. So the design question for a measurement range is not "how do I measure a pattern" but "how good a fake plane wave can I afford".

:::{admonition} Key Point
:class: key-concept
A range is a **plane-wave simulator**. Every range specification — length, absorber, quiet zone, source antenna choice — is a tolerance on the flatness of that simulated wave, in amplitude and in phase.
:::

### Two tolerances, not one

A plane wave is flat in amplitude and flat in phase across the aperture. A real range violates both, and the two violations come from different places.

**Amplitude taper** comes from the source antenna's own pattern. Seen from the source, the antenna under test (**AUT**) subtends an angle of roughly $D/r$, where $D$ is the AUT's largest dimension and $r$ is the range length. If the source pattern rolls off across that angle, the AUT is illuminated more strongly in the middle than at the edges — you have applied an amplitude taper the designer never asked for, which broadens the beam and lowers the sidelobes you report. The usual specification is **under $0.25\ \text{dB}$ of taper edge to edge**, which works out to a rule of thumb:

> The source antenna's beamwidth must be at least three to four times the angle the AUT subtends.

That is why range source antennas are modest-gain horns. Bigger is not better at the transmit end.

**Phase curvature** comes from geometry alone and is the one that sets the range length.

### Where the far-field distance comes from

Take a source a distance $r$ away on boresight. The path to a point a distance $x$ off the aperture centre is $\sqrt{r^2 + x^2}$, and for $x \ll r$ that is $r + x^2/2r$. The extra path at the aperture edge, where $x = D/2$, is

$$\Delta \ell \approx \frac{(D/2)^2}{2r} = \frac{D^2}{8r}$$

Multiply by $k = 2\pi/\lambda$ to get phase. Now make a decision — and it *is* a decision, not a derivation. Allow the edge of the aperture to lag the centre by at most an eighth of a wavelength, $\pi/8$ radians or $22.5^\circ$:

$$\Delta\phi_{\max} = k\ \Delta \ell = \frac{\pi D^2}{4 \lambda r} \le \frac{\pi}{8} \qquad \Longrightarrow \qquad r \ge \frac{2D^2}{\lambda}$$

There it is. The far-field criterion you have been quoting since L5 is nothing more than $22.5^\circ$ of edge phase error, rewritten as a distance.

:::{admonition} Worked example — how long a range does a 0.5 m antenna need?
:class: tip
A $0.5\ \text{m}$ reflector, tested at $10\ \text{GHz}$.

$$\lambda = \frac{c}{f} = \frac{3\times10^{8}}{10\times10^{9}} = 0.03\ \text{m}, \qquad \frac{D}{\lambda} = \frac{0.5}{0.03} = 16.7$$

$$r \ge \frac{2D^2}{\lambda} = \frac{2(0.5)^2}{0.03} = 16.7\ \text{m}$$

Seventeen metres — about 55 feet — of chamber, to measure an antenna the size of a dinner plate. That is a large, expensive room, and it is completely ordinary.

Run the same arithmetic on a $3\ \text{m}$ satellite terminal reflector at $30\ \text{GHz}$, where $\lambda = 0.01\ \text{m}$:

$$r \ge \frac{2(3)^2}{0.01} = 1800\ \text{m}$$

Nobody builds a $1.8\ \text{km}$ anechoic chamber. That single number is the reason compact ranges and near-field scanners exist.
:::

```{note}
The $2D^2/\lambda$ criterion assumes $D$ is comfortably larger than $\lambda$. For a small antenna — a dipole, a patch — the far field is set instead by the $r \gg \lambda$ condition from L5, usually taken as $r \ge 10\lambda$. Use whichever distance is larger.
```

## Part 2: What a short range does to your data

Suppose you build the range too short anyway. The quadratic phase error $\Delta\phi(x) = \pi x^2 / \lambda r$ rides on the aperture illumination, and the measured pattern is the same radiation integral from L6 with that extra phase inside it:

$$F_\text{meas}(\theta) \propto \int_{-D/2}^{D/2} E(x)\ e^{-j \pi x^2 / \lambda r}\ e^{+jkx\sin\theta}\ dx$$

Nothing here is subtle: a quadratic phase across an aperture is a **defocus**, exactly like a lens at the wrong distance. The interesting part is *which* pattern features it damages, and in what order.

Slide the range in and watch. The left panel shows the phase error across the aperture against the $22.5^\circ$ tolerance line; the right panel overlays the true far-field pattern (dashed) on what the range actually measures (solid). Notice that the nulls fill and the first sidelobe merges into a shoulder long before the main beam does anything at all — and that everything snaps clean right around $r = 2D^2/\lambda$, where the edge error reads exactly $22.5^\circ$.

<iframe src="../../viz/range-phase-error.html"
        width="100%" height="657"
        style="border: 1px solid #cddce9; border-radius: 6px;"
        loading="lazy"
        title="Quadratic phase error from a finite range length, and the pattern it produces compared with the true far-field pattern">
</iframe>

The damage, tabulated for a uniform aperture:

| Range as a fraction of $2D^2/\lambda$ | Edge phase error | First null fills to | First sidelobe | HPBW error |
| :-- | :-- | :-- | :-- | :-- |
| 2 | $11.3^\circ$ | $-28$ dB | $-13.2$ dB | negligible |
| 1 | $22.5^\circ$ | $-22$ dB | $-12.9$ dB | $+0.3\%$ |
| 1/2 | $45^\circ$ | $-16$ dB | $-12.0$ dB | $+1.3\%$ |
| 1/4 | $90^\circ$ | $-9.5$ dB | $-9.0$ dB | $+6\%$ |

Read the top two rows carefully, because they carry the honest version of the rule. At exactly $r = 2D^2/\lambda$ you have **not** measured the true pattern. You have measured one whose deepest nulls are wrong by twenty decibels and whose first sidelobe reads $-12.9$ dB instead of the textbook $-13.3$ dB. What you *have* measured correctly is the main beam, the beamwidth, and the gain.

:::{admonition} Key Point
:class: key-concept
$2D^2/\lambda$ is a **main-beam and gain** criterion, not a sidelobe criterion. If you need a $-40$ dB sidelobe or a null depth you can defend, go to $5D^2/\lambda$ or further — or stop using a far-field range altogether.
:::

The failure mode here is nasty precisely because it is quiet. A pattern measured at a quarter of the far-field distance still looks like a pattern. It has a main beam of about the right width, it has sidelobes, it is smooth. It is simply wrong in the places you care about most.

## Part 3: Three ways to make the plane wave

| Range type | How it makes the plane wave | What limits it |
| :-- | :-- | :-- |
| Outdoor / elevated | Brute-force distance | Weather, ground reflection, no security, RF interference |
| Anechoic chamber | Distance plus absorber | Still needs the full $2D^2/\lambda$ |
| Compact range | A reflector collimates it up close | Edge diffraction, feed spillover, reflector accuracy |
| Near-field scanner | Measures close in and transforms | Needs phase, probe correction, and time |

The first three are **far-field ranges**: they physically deliver an approximate plane wave to the AUT. The fourth changes the question entirely, and gets Part 4 to itself.

### Outdoor ranges

Distance is free outdoors, so the oldest ranges are two towers, or a tower and a hillside. Two variants matter. An **elevated range** puts both antennas high enough, and uses directive-enough source antennas, that the ground bounce misses the AUT. A **ground-reflection range** does the opposite: it chooses the geometry so the direct and ground-reflected rays arrive *in phase* at the AUT, deliberately using the ground as part of the illumination. Both work. Neither is private, dry, or free of interference, which is why most modern measurement happens indoors.

### Anechoic chambers

An anechoic chamber is a shielded room lined with **absorber** — carbon-loaded foam, cut into pyramids. The pyramid shape is the whole trick: it is a gradual impedance transition from free space into a lossy medium, so the wave enters without a strong reflection at the surface and then dies inside the foam.

Absorber is specified by **reflectivity in dB**. Good pyramidal absorber reaches $-40$ to $-50$ dB at normal incidence, and performance degrades at grazing incidence — which is exactly the condition on the side walls. Performance also scales with pyramid height *in wavelengths*, so low-frequency absorber gets enormous, and a chamber rated to 200 MHz has metre-long spikes on the walls.

:::{admonition} Key Point
:class: key-concept
A chamber is never "no reflections". It is **reflections below a stated level**. Which level you need is set by the lowest signal you intend to believe, not by the main beam.
:::

That last sentence deserves numbers. Suppose one stray reflection arrives $-40$ dB below the main beam. As the positioner turns, it adds in and out of phase with whatever you are measuring, and the peak-to-peak ripple depends entirely on how strong that "whatever" is:

| What you are measuring | Error a $-40$ dB stray adds |
| :-- | :-- |
| Main beam peak (0 dB) | $\pm 0.09$ dB |
| A $-20$ dB sidelobe | $+0.8 / -0.9$ dB |
| A $-30$ dB sidelobe | $+2.4 / -3.3$ dB |

A three-decibel error on a sidelobe, in a chamber that meets a perfectly respectable $-40$ dB spec. This is the single most common way a measurement report overstates its own precision.

### The quiet zone

The deliverable of a chamber is not the room; it is the **quiet zone** — a specified volume, usually a sphere or cylinder centred on the positioner, inside which the stray field is guaranteed below the reflectivity spec. It is quoted as a size *and* a level and a frequency band: "1.2 m quiet zone at $-45$ dB, 2 to 18 GHz". It is measured rather than assumed, typically by dragging a probe through the volume and recording the ripple.

The practical consequence is blunt: **the AUT must fit inside the quiet zone.** An antenna that overhangs it is being measured in a room, not in a chamber.

### Compact ranges

A **compact range** stops fighting the range equation and cheats it. Put a feed at the focus of a precision offset paraboloid and you get the L11 geometry again: every path from the focus to the reflector to the aperture plane has the same length, so the reflected wave leaves with flat phase. In L11 that plane wave was headed for a satellite. Here it only has to cross the room.

Two costs come with it. The usable quiet zone is only about **50 to 60% of the reflector aperture**, so the reflector must be substantially larger than the AUT — a metre of quiet zone needs close to a two-metre reflector, built to a fraction of a wavelength. And the reflector rim diffracts: a hard edge acts as a line source sitting right inside your quiet zone. Compact-range reflectors therefore have **serrated or rolled edges**, which scatter the edge contribution away from the test volume instead of into it.

## Part 4: Near-field scanning

Return to the 1.8 km problem. The far-field range is impossible, the compact range would need a reflector bigger than the antenna, and you still need the pattern. So change the measurement.

Put a small probe a few wavelengths in front of the antenna and record the complex field — **amplitude and phase** — at a grid of points on a surface. Then transform.

:::{admonition} Key Point
:class: key-concept
L6 already proved this works. The far field is the **Fourier transform** of the source distribution, with $k\sin\theta$ playing the role of frequency. Fourier transforms are invertible, so the complex field sampled on a surface enclosing the antenna determines the field everywhere outside it. Near-field to far-field transformation is not a new physical principle — it is L6's relationship, run in the other direction.
:::

Three consequences follow immediately, and they are all the practical content of near-field scanning at this level.

**Phase is not optional.** A transform needs the complex field. Magnitude alone does not determine it, which is why a near-field range is built around a vector network analyzer and phase-stable cables, and why the probe position has to be known to a small fraction of a wavelength.

**Sample at half-wavelength spacing or finer.** This is the same Nyquist argument as in L6's spatial spectrum: undersample the aperture field and the transform aliases, producing lobes in the far-field pattern that the antenna does not have.

**Scan far enough out.** The transform assumes you captured everything. Truncate the scan plane before the field has decayed and you get truncation error, which is why planar scanning gives a trustworthy pattern only over a forward cone — roughly $\pm 60^\circ$ — and says nothing about the back lobes.

| Scan surface | Best suited to | Pattern coverage |
| :-- | :-- | :-- |
| Planar | High-gain, directive antennas | A forward cone, roughly $\pm 60^\circ$ |
| Cylindrical | Fan beams, sector antennas | Full azimuth, limited elevation |
| Spherical | Low-gain antennas, anything | The complete sphere |

```{note}
One more step exists in a real near-field system: **probe compensation**. The probe has its own pattern, and what it records is the true field weighted by that pattern. Dividing it back out is standard, well understood, and firmly beyond this course. Know that it happens; do not derive it.
```

## Part 5: Measuring gain

A pattern is a shape, and a shape is easy — normalize and you are done. Gain is an absolute number, and absolute numbers are hard. There are two honest ways to get one.

### The comparison method

Gain is a ratio, so measure it as one. This is the **comparison** or **gain-transfer** method, and it is what you will use for the midterm.

1. Put the AUT on the positioner, point it at the source, and record the received power $P_\text{AUT}$.
2. Take it off. Put a **standard gain horn** — the calibrated pyramidal horn from L10, supplied with a gain-versus-frequency curve traceable to a national standard — in exactly the same place, pointed the same way, at the same frequency and polarization. Record $P_\text{SGH}$.
3. Subtract.

$$G_\text{AUT}\ [\text{dBi}] = G_\text{SGH}\ [\text{dBi}] + \left( P_\text{AUT} - P_\text{SGH} \right)\ [\text{dB}]$$

The reason this works is that everything you do not know is common to both measurements. Write Friis for each: the transmit power, the source gain, the range, the wavelength, the cable losses all appear identically, and they all cancel in the difference. The horn's calibration is the only absolute number anywhere in the room.

:::{admonition} Worked example — comparison-method gain
:class: tip
At $9.4\ \text{GHz}$, a standard gain horn with a calibrated gain of $16.8\ \text{dBi}$ receives $-38.6\ \text{dBm}$. Replacing it with the AUT, everything else untouched, gives $-33.1\ \text{dBm}$.

$$\Delta P = -33.1 - (-38.6) = +5.5\ \text{dB}$$

$$G_\text{AUT} = 16.8 + 5.5 = 22.3\ \text{dBi}$$

The AUT collects 5.5 dB more power than the standard, so it has 5.5 dB more gain. That is the entire method.
:::

The conditions on validity are worth naming, because violating one silently biases the answer: same position, same polarization, same frequency, and both antennas either well matched or their mismatch losses corrected. If the AUT has a poor match, the power you measure is low for a reason that has nothing to do with gain.

### When no standard exists

Somebody had to calibrate that horn. Working from Friis (L2) with no calibrated antenna at all:

$$P_r = P_t G_t G_r \left( \frac{\lambda}{4\pi R} \right)^2 \qquad \Longrightarrow \qquad \left( P_r - P_t \right)_{\text{dB}} = G_t + G_r + 20\log_{10}\!\left( \frac{\lambda}{4\pi R} \right)$$

If you have **two identical antennas**, then $G_t = G_r = G$ and one measurement is enough.

:::{admonition} Worked example — two-antenna method
:class: tip
Two identical horns face each other at $R = 20\ \text{m}$, at $6\ \text{GHz}$ so $\lambda = 0.05\ \text{m}$. With $P_t = 0\ \text{dBm}$ you measure $P_r = -40.0\ \text{dBm}$.

$$20\log_{10}\!\left( \frac{\lambda}{4\pi R} \right) = 20\log_{10}\!\left( \frac{0.05}{4\pi (20)} \right) = 20\log_{10}(1.989\times10^{-4}) = -74.0\ \text{dB}$$

$$2G = (P_r - P_t) - (-74.0) = -40.0 + 74.0 = 34.0\ \text{dB} \qquad \Longrightarrow \qquad G = 17.0\ \text{dBi}$$

Check the range while you are here: for a horn of this gain, $D$ is roughly $0.2\ \text{m}$, so $2D^2/\lambda = 1.6\ \text{m}$. Twenty metres is comfortably far field.
:::

If the antennas are not identical, use **three** of them and measure all three pairs. Let $M_{AB}$ be the measured pair sum $(P_r - P_t)_{\text{dB}}$ with the path term already removed, so $M_{AB} = G_A + G_B$, and likewise for the other two pairs. Three equations, three unknowns:

$$G_A = \tfrac{1}{2}\left( M_{AB} + M_{AC} - M_{BC} \right)$$

with $G_B$ and $G_C$ following by symmetry. No calibrated antenna appears anywhere. This is how standard gain horns get their curves in the first place.

## Part 6: Cuts and polarization

A complete pattern is a function on a sphere, and measuring the whole sphere finely is expensive. In practice you take slices.

- A **great-circle cut** holds $\phi$ fixed and sweeps $\theta$ through the poles. This is the natural cut for a positioner that rotates the AUT about a single axis, and it is what almost every published pattern is.
- A **conical cut** holds $\theta$ fixed and sweeps $\phi$ — a ring at a constant angle off boresight. Useful for tracking antennas and for checking rotational symmetry.
- The **principal planes** are two particular great-circle cuts. The **E-plane** contains the aperture electric field and the boresight direction; the **H-plane** contains the magnetic field and boresight, perpendicular to the E-plane. For a rectangular horn or a patch, these are the two cuts you always publish.

Two principal cuts fully describe a well-behaved pencil beam, and say nothing whatsoever about the diagonal planes — where, for rectangular apertures, the sidelobes frequently live.

### Co-polarization and cross-polarization

Then run every cut twice. With the source antenna aligned to the AUT's nominal polarization you measure the **co-polarized** pattern. Rotate the source $90^\circ$ about the range axis, change nothing else, and repeat: that is the **cross-polarized** pattern, the power the antenna radiates into the polarization it is supposed to reject. A well-built linear antenna sits 20 to 30 dB below co-pol on boresight and is considerably worse off-axis, which is why cross-pol is quoted as a pattern and not as a single number.

For a circularly polarized antenna there is a faster trick. Spin the linear source continuously while sweeping the cut — **spinning linear** — and the recorded pattern comes back as a band rather than a line. The peak-to-trough width of that band, in dB, *is* the axial ratio from L3. A perfectly circular antenna gives a band of zero width.

## Summary

| Symbol / idea | What it is | The number to remember |
| :-- | :-- | :-- |
| $r \ge 2D^2/\lambda$ | Minimum far-field range length | $22.5^\circ$ of edge phase error, written as a distance |
| $\Delta\phi_{\max} = \pi D^2 / 4\lambda r$ | Quadratic phase error at the aperture edge | $\pi/8$ at the far-field distance |
| Amplitude taper | Source pattern rolling off across the AUT | Under $0.25$ dB; source beamwidth 3-4× the subtended angle |
| Absorber reflectivity | How much a wall reflects | $-40$ to $-50$ dB at normal incidence, worse at grazing |
| Quiet zone | Volume where the stray field meets spec | A size *and* a level; the AUT must fit inside |
| Compact range | Reflector collimates a spherical wave up close | Quiet zone $\approx$ 50-60% of the reflector |
| Near-field scan | Sample amplitude and phase close in, transform | Half-wavelength sampling; phase is mandatory |
| Comparison method | Gain by differencing against a standard | $G_\text{AUT} = G_\text{SGH} + (P_\text{AUT} - P_\text{SGH})$ |
| Three-antenna method | Gain with no calibrated standard | $G_A = \tfrac{1}{2}(M_{AB} + M_{AC} - M_{BC})$ |

## Practice

- <a href="../../practice/ECE444_L12_Practice_blank.pdf" target="_blank" rel="noopener">Problem set (PDF)</a>
- <a href="../../practice/ECE444_L12_Practice_SOLUTIONS.pdf" target="_blank" rel="noopener">Solutions (PDF)</a>

## Where this is going

L13 and L14 are the two lessons where this becomes hardware. L13 puts an antenna on a vector network analyzer and measures S-parameters — match, resonance, bandwidth, the L4 material made real. L14 puts one on the positioner and takes the cuts, with the range length, the quiet zone, and the standard gain horn all sitting exactly where this lesson said they would.

The midterm project, due L20, is the full bundle: measure a pattern, extract half-power beamwidth and sidelobe level, measure gain by comparison against the standard horn, and defend the numbers. That last part is what today was really about. "I measured it" is not a result. "I measured it, and here is precisely what my range could and could not tell me" is an engineering result — and the range length, the quiet-zone specification, and the horn's calibration uncertainty are the three lines of your error budget.
