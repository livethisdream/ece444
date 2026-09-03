# Project 1 — Build and Characterize a Dipole

**One antenna, every measurement in the course.** You will cut a half-wave
dipole for 915 MHz, predict on paper what it should do, simulate it, put it on
a vector network analyzer, match it to a 50 ohm line, measure its pattern, and
then explain every place the four answers — predicted, simulated, measured at
the terminals, measured in the field — disagree.

This page is the single place that describes the project. The lessons it
draws on teach the methods; this page says what to build, what to record, and
what to turn in. Bookmark it and bring it to every lab in Module 2.

:::{admonition} Project 1 at a glance
:class: key-concept
- **Antenna:** a wire half-wave dipole on an SMA connector, designed for
  **915 MHz**.
- **Build:** at Lesson 7. Ten minutes with a wire cutter and a soldering iron.
- **Characterize:** resonance and VSWR (Lesson 7, right after the build), a
  balun and a 50 ohm match (before the S-parameter lab), a 4nec2 simulation
  (Lesson 8), calibrated S-parameters (Lesson 13), and a radiation pattern with
  gain (Lesson 14).
- **Report due: 2 October.** This is the midterm project. It is assessed
  **Mastered / Not Yet Mastered**, with one resubmission after feedback (see the
  <a href="../../syllabus.html#midterm-project-mastery-assessment">syllabus</a>).
- **Work in pairs** at the bench; each cadet builds and reports on their own
  antenna.
:::

## The plan

Each step lands in the lesson that teaches its method, so nothing here asks
you to do something you have not been shown. The project depends only on
Lessons 7, 8, 13, and 14 and on the Lesson 4 material; the lessons on other
antenna types (9 to 12) may be taught after the midterm, and the plan does
not change if they are. The last column is what goes into your record sheet
at the end of this page.

| Step | When | The method is taught in | What you record |
| :-- | :-- | :-- | :-- |
| 1. Design | L7 | <a href="../../module02/L07-simple-resonant-antennas/index.html">L7</a>, <a href="../../module01/L05-field-regions/index.html">L5</a> | cut length, predicted $Z_{\text{in}}$, VSWR, gain, HPBW, bandwidth |
| 2. Build | L7 | this page | arm lengths as cut, wire gauge, a photo |
| 3. Resonance and VSWR | L7 to L8 | <a href="../../module01/L04-lab-matching/index.html">L4 lab</a> | $f_\text{res}$ and VSWR at 915 MHz, before and after trimming |
| 4. Balun and match | before the S-parameter lab | <a href="../../module01/L04-impedance-feeding-baluns/index.html">L4</a>, <a href="../../module01/L04-lab-matching/index.html">L4 lab</a> | effect of the choke; matching-network design and measured VSWR |
| 5. Simulate | L8 | <a href="../../module02/L08-dipole-simulation-lab/index.html">L8</a> | simulated $Z_{\text{in}}$, $f_\text{res}$, gain, HPBW, average gain |
| 6. S-parameters | S-parameter lab (L13) | <a href="../../module02/L13-measurement-lab-sparams/index.html">L13</a> | calibrated $S_{11}$ sweep, Smith chart, −10 dB bandwidth, Touchstone file |
| 7. Pattern | pattern lab (L14) | <a href="../../module02/L12-pattern-measurement-theory/index.html">L12</a>, <a href="../../module02/L14-measurement-lab-patterns/index.html">L14</a> | E- and H-plane cuts, gain by comparison, XPD, noise floor |
| 8. Compare and report | **due 2 October** | this page | the filled record sheet and the report |

The report is graded on the comparison, not on how close the numbers land. A
2 dB gap with a named cause is a better report than a 0.2 dB gap with no
discussion.

## Step 1 — Design

Everything starts from the frequency. At $f = 915\ \text{MHz}$,

$$\lambda = \frac{c}{f} = \frac{3 \times 10^8}{915 \times 10^6} = 32.8\ \text{cm}, \qquad \frac{\lambda}{2} = 16.4\ \text{cm}.$$

Lesson 7's 5% rule shortens the wire so that it resonates instead of sitting
at $73 + j42.5\ \Omega$:

$$L = 0.475\lambda = 15.6\ \text{cm}, \qquad \text{so } 7.8\ \text{cm per arm}.$$

Cross-check with the field-manual form: $143 / 915 = 0.156\ \text{m}$. The
two agree to a millimeter.

Now write down what the antenna should do **before you cut anything**. These
are the numbers the rest of the project is measured against, and a prediction
written after the fact teaches you nothing.

| Quantity | Prediction | Where it comes from |
| :-- | :-- | :-- |
| Total length $L$ | $15.6\ \text{cm}$ ($0.475\lambda$) | 5% rule, L7 |
| $Z_{\text{in}}$ at resonance | $\approx 70 + j0\ \Omega$ | what real resonant dipoles measure, L7 |
| VSWR on $50\ \Omega$ | $1.40$ | $\vert\Gamma\vert = 20/120 = 0.167$, L4 |
| Return loss | $15.6\ \text{dB}$ | $-20\log_{10}\vert\Gamma\vert$ |
| Mismatch loss | $0.12\ \text{dB}$ | $-10\log_{10}(1 - \vert\Gamma\vert^2)$ |
| $-10\ \text{dB}$ bandwidth | $\approx 70\ \text{MHz}$, about 8% | induced-EMF model for 20 AWG wire; a fatter element is wider |
| Gain | $2.15\ \text{dBi}$ | $D = 1.64$, copper loss negligible |
| E-plane HPBW | $78^\circ$ | half-wave pattern, L7 |
| H-plane pattern | a circle | the dipole is symmetric about its axis |
| Far-field distance | $2D^2/\lambda = 0.15\ \text{m}$, $5D = 0.78\ \text{m}$, $10\lambda = 3.3\ \text{m}$ | L5, L12; the **$10\lambda$ rule binds** for an antenna this small |

Two of those rows need a footnote. The sinusoidal-current model in the L7
widgets predicts a resonant resistance in the low sixties; a full numerical
solver and a real measurement both land closer to $70\ \Omega$. And the exact
resonant length depends on wire gauge, insulation, and what is nearby. Carry
$70\ \Omega$ and $0.475\lambda$ as the design numbers and expect a few percent
of disagreement. Quantifying that disagreement is the project.

## Step 2 — Build

:::{admonition} Parts and tools
:class: type-along
- An **SMA female** connector: panel-mount (four-hole flange) or edge-launch.
  Either works; the flange type is easier to solder to.
- About $20\ \text{cm}$ of **20 AWG solid copper wire** (bare or enameled; if
  enameled, scrape the last centimeter clean). Radius $0.41\ \text{mm}$ — you
  will need that number in Step 5.
- Wire cutters, a metric ruler, a soldering iron, and a permanent marker.
- Optional but recommended: a few centimeters of heat-shrink, and a small piece
  of foam or a cardboard strip to hold the antenna clear of the bench.
:::

1. **Cut two arms at $7.8\ \text{cm}$.** Cut them a few millimeters long if you
   are unsure. You can always trim; you cannot un-trim. Measure each arm with
   the ruler and write both lengths on the record sheet — the number you *cut*,
   not the number you *meant to cut*.
2. **Solder one arm to the center pin** and the other to the connector
   **body or a ground tab**, so that the two arms run in opposite directions
   along one straight line through the connector. Keep the solder joints short:
   a few millimeters of extra metal at the feed is a few millimeters of extra
   antenna.
3. **Straighten both arms** and check that the pair is collinear and square to
   the connector. A bent dipole is a different antenna, and a dipole that
   changes shape between measurements will not give you the same answer twice.
4. **Mark the antenna** with your name and the frequency, and **photograph it**
   next to the ruler. The photo goes in the report.

:::{admonition} This feed has no balun, and that matters
:class: note
Soldering wire straight onto an SMA connector is the crudest possible feed: the
dipole is balanced, the coax behind it is not, and current will flow on the
outside of the shield exactly as Lesson 4 warned. The feedline becomes part of
the antenna. Expect the measured resonance and impedance to drift from the
predictions, and expect the readings to twitch when you move your hand near
the cable. That is not a botched build. It is the balun problem showing up in
your own hardware, and Step 4 is where you fix it — after you have measured
what it costs.
:::

## Step 3 — Resonance and VSWR

The first measurement is a quick one, made with a NanoVNA the way the
<a href="../../module01/L04-lab-matching/index.html">L4 lab</a> taught you.
Its purpose is to find out where the antenna actually resonates and to trim it
onto frequency. The careful, calibrated characterization comes in Step 6; do
not skip the calibration here either, but do not agonize over it.

1. **Set the sweep** to $600$ to $1200\ \text{MHz}$, at least 201 points.
2. **Calibrate** short, open, and load at the end of the test cable, then
   reconnect the load and confirm $\vert S_{11}\vert$ is below $-30\ \text{dB}$
   across the band.
3. **Connect the antenna** and hold it clear of the bench, your hands, and your
   body. Set it on the foam or hang it by the cable. Read off:
   - the resonant frequency $f_\text{res}$, the real-axis crossing on the Smith
     chart (or the $\vert S_{11}\vert$ dip, which is usually close);
   - $Z$ and VSWR at $915\ \text{MHz}$;
   - VSWR at $f_\text{res}$.
4. **Decide which way to trim.** A wire cut long resonates *low*; if
   $f_\text{res}$ is below $915\ \text{MHz}$ the antenna wants to be shorter.
   Lesson 13's worked example shows the opposite case. Record the untrimmed
   numbers first — they are data — then trim **both arms equally**, a
   millimeter or two at a time, and re-sweep after each cut until
   $f_\text{res}$ sits within about $10\ \text{MHz}$ of $915$. Write down the
   final arm lengths.
5. **Perturb it** once: hand $2$ to $3\ \text{cm}$ from an arm, then a hand on
   the coax just behind the connector. Note what moves. You will explain it in
   Step 4.

:::{callout}
**Kill the reactance first.** On a $50\ \Omega$ line, trimming a $\lambda/2$
wire to resonance takes the VSWR from about $2.2$ to about $1.4$. Nothing you
do in Step 4 buys as much as that trim.
:::

## Step 4 — Balun and match to 50 ohms

A resonant dipole sits near $70\ \Omega$, and a $50\ \Omega$ line sees that as
a $1.4{:}1$ VSWR. That is a usable match — the mismatch loss is only
$0.12\ \text{dB}$ — but the project asks you to close the gap, for two reasons.
First, you cannot design a matching network until you have a stable impedance
to match, and a balun-less dipole does not have one. Second, matching a real
antenna with real parts at UHF is a skill the L4 lab only practiced at 2 MHz.

**4a. Fit a choke balun.** Lesson 4's table says the default dipole feed is a
1:1 current balun. Two ways to make one at $915\ \text{MHz}$:

- **Ferrite beads.** Slip two or three clip-on or slip-on ferrite beads (a
  mix rated for UHF, such as mix 43 or mix 61) over the coax right behind the
  SMA connector. This is the fast option and usually the better one.
- **A sleeve (bazooka) balun.** A $\lambda/4 = 8.2\ \text{cm}$ length of brass
  or copper tube slipped over the coax, open at the antenna end and soldered to
  the shield at the far end. Elegant, narrowband, and fussier to build.

Re-sweep with the choke in place and repeat the hand-on-the-coax perturbation.
Record $f_\text{res}$, $Z$ at $915\ \text{MHz}$, and how much the reading
moves when you touch the cable, with and without the choke. Both rows go in
the report; the difference between them is your measurement of the
common-mode current.

**4b. Design the match.** Take the measured $Z_{\text{in}}$ at $915\ \text{MHz}$
*with the choke fitted* and design an L-network for it exactly as Lesson 4 did:
cancel the reactance, then transform the resistance. For the design value of
$70 + j0\ \Omega$ the load resistance is larger than $50\ \Omega$, so the shunt
element goes across the antenna and the series element toward the line:

$$Q = \sqrt{\frac{70}{50} - 1} = 0.632$$

$$\vert X_\text{shunt}\vert = \frac{70}{Q} = 111\ \Omega$$

$$\vert X_\text{series}\vert = Q \times 50 = 31.6\ \Omega$$

Either of the two dual networks realizes it at $915\ \text{MHz}$:

| Network | Shunt element (across the antenna) | Series element (toward the line) |
| :-- | :-- | :-- |
| Low-pass | $C = 1.6\ \text{pF}$ | $L = 5.5\ \text{nH}$ |
| High-pass | $L = 19\ \text{nH}$ | $C = 5.5\ \text{pF}$ |

Your measured impedance will not be exactly $70 + j0$, so recompute from your
own number and check the design on the feed-match widget below before you
solder anything. Nearest standard values are fine: $1.5\ \text{pF}$ and
$5.6\ \text{nH}$ are E-series parts, and the L4 lab already taught you how to
price the substitution.

<iframe src="../../viz/feed-match.html"
        width="100%" height="529"
        style="border: 1px solid #cddce9; border-radius: 6px;"
        loading="lazy"
        title="Feed-line match explorer">
</iframe>

**4c. Build and verify it.** At $915\ \text{MHz}$ a few picofarads and a few
nanohenries are parts the size of a grain of rice, and every millimeter of lead
is a fraction of a nanohenry you did not design in. Use 0603 or 0805 surface
mount parts, solder them directly across the SMA connector's pin and flange,
and keep the leads as short as physically possible. Then re-sweep.

| What "good" looks like | Target |
| :-- | :-- |
| VSWR at $915\ \text{MHz}$, matched | $\le 1.2$ (return loss $\ge 20\ \text{dB}$) |
| Bandwidth over which VSWR $\le 2$ | narrower than before — record by how much |

If the network makes things worse, that is a result, not a failure. The L4
lab's lesson applies verbatim: state the VSWR you actually hold, the mismatch
loss it costs, and argue ship / re-source / redesign. Keep the unmatched
antenna's numbers too — the pattern measurement in Step 7 works fine at
$1.4{:}1$, and a network that loses its match when the antenna is handled is
worse than no network.

:::{admonition} Save both configurations
:class: note
From here on you have two antennas: the bare dipole with its choke, and the
matched dipole. Keep the matching network on a separate short SMA adapter if
you can, so that you can remove it without unsoldering. Steps 6 and 7 measure
both.
:::

## Step 5 — Simulate

Lesson 8 walks you through 4nec2 with a generic $915\ \text{MHz}$ dipole. For
the project, model **your** antenna: the total length you actually cut, after
trimming, and the real wire radius.

- Start from the L8 input file and change three numbers: the two `GW` end
  coordinates (half your trimmed length each way) and the wire radius
  ($0.41\ \text{mm} = 0.00041$ in meters for 20 AWG).
- Re-check the segmentation arithmetic. With $L = 15.6\ \text{cm}$ and 21
  segments, $\Delta = 7.4\ \text{mm}$, which clears $\lambda/20 = 16\ \text{mm}$
  from above and $8a = 3.3\ \text{mm}$ from below. Keep the count odd.
- Run the **average gain test** and do not report anything from a model whose
  average gain is not close to $1.000$.
- Run the frequency sweep ($800$ to $1000\ \text{MHz}$, $5\ \text{MHz}$ steps),
  the E- and H-plane pattern cuts at $915\ \text{MHz}$, and the convergence
  study, exactly as L8 Steps 5 to 8 describe.

Record simulated $Z_{\text{in}}$ at $915\ \text{MHz}$, $f_\text{res}$, the
resistance at resonance, peak gain, E-plane HPBW, and the average gain. Note
what the model does **not** contain: no connector, no coax, no choke, no
bench. Every one of those is a candidate explanation when the measured numbers
in Steps 6 and 7 disagree with it.

:::{admonition} Optional — model the feed
:class: tip
If you want to see how large the feed effects are, add a second wire to the
NEC model representing $10\ \text{cm}$ of coax shield hanging off one arm
at right angles and watch the impedance and the pattern move. This is exactly
the current the choke exists to block.
:::

## Step 6 — S-parameters

This is Lesson 13's lab, run on your antenna. Follow L13 Part 5 exactly, on
whichever VNA your bench has, and take the full data set for both
configurations from Step 4.

1. **Sweep** $600$ to $1200\ \text{MHz}$, at least 401 points.
2. **Calibrate** at the end of the test cable and **verify** on the load
   standard. Screenshot the verification.
3. **Measure the bare dipole with its choke**: $f_\text{res}$ as the real-axis
   crossing, $Z$ at resonance and at $915\ \text{MHz}$, both $-10\ \text{dB}$
   crossing frequencies, and the Smith chart with the resonance marked.
4. **Measure the matched dipole** the same way. Its locus should now pass
   through, or near, the center of the chart.
5. **Perturb** the bare antenna, one variable at a time, as L13 Part 5
   describes: free space, a hand near the element, flat on the bench.
6. **Save the data**, not just screenshots. Export each sweep as a Touchstone
   `.s1p` file (NanoVNA-Saver and every bench analyzer can do this) and plot
   it yourself in Python. `scikit-rf` reads Touchstone files directly;
   `matplotlib` does the rest. A plot you made from the data can carry your
   own annotations, and the same script will overlay the simulated sweep from
   Step 5 on top of it.

:::{callout}
$S_{11}$ measures **mismatch only**. A deep dip is necessary for a good
antenna, not sufficient: a $50\ \Omega$ resistor gives a perfect match and
radiates nothing. The efficiency question is answered in Step 7, by the gain
comparison, and nowhere else.
:::

## Step 7 — Pattern

This is Lesson 14's lab, run on your antenna instead of the horn. The range,
the acquisition discipline, and the reduction are the same; the numbers
change.

**Range check first.** For your dipole $D = 15.6\ \text{cm}$, and the three
far-field criteria from L12 give $2D^2/\lambda = 0.15\ \text{m}$,
$5D = 0.78\ \text{m}$, and $10\lambda = 3.3\ \text{m}$. The last one binds. The
L14 bench range is $3.0\ \text{m}$, which is about 9% short of $10\lambda$.
State that margin in your report, say which of the three criteria it
violates and what that criterion protects against, and argue whether it
matters for a dipole.

**Setup.**

- The source and the reference are whatever the instructor supplies for
  $915\ \text{MHz}$. The course's Pluto-SDR transmit/receive tool tunes there.
- Mount the dipole **vertically** on the rotator, connector down, with the coax
  and its choke running straight down the axis of rotation. A cable that
  leaves the feed sideways is in the pattern.
- Co-polarize the source (vertical too), peak up, and define that angle as
  $0^\circ$.
- Measure the noise floor with the source off. That number caps everything
  that follows.

**Cuts.**

1. **E-plane**: the cut containing the wire. Rotate the dipole about a
   horizontal axis through its center, or, if the rotator only turns about a
   vertical axis, mount the dipole horizontally and rotate it in azimuth. Take
   a full $\pm 180^\circ$ in $5^\circ$ steps (HPBW/5 is about $15^\circ$;
   $5^\circ$ resolves the nulls).
2. **H-plane**: rotate the vertical dipole in azimuth. The prediction is a
   circle; the measurement will show ripple. The peak-to-peak ripple is your
   first estimate of range quality.
3. **Repeat one cut.** The disagreement between two sweeps of the same cut is
   your repeatability.
4. **Gain by comparison.** Swap in the reference antenna, peak it up, record
   the level, change nothing else. If no calibrated reference exists at
   $915\ \text{MHz}$, use the **two-antenna method** from L12 with a
   classmate's dipole, and state the assumption it rests on.
5. **Cross-polarization.** Rotate the source $90^\circ$ and re-sweep the
   E-plane. A dipole's XPD should be high; a low number points at the feed
   cable radiating.
6. **The matched antenna.** Repeat the gain comparison only. The pattern
   shape should not change; the level should move by the difference in
   mismatch loss, about $0.1\ \text{dB}$, which is inside your repeatability.
   Say so, with the numbers.

Reduce the data as L14 Part 4 describes: normalize to the peak, plot polar dB
and rectangular dB, and extract HPBW, front-to-back ratio, gain, and XPD, each
with an uncertainty from your repeated sweep. A dipole has no sidelobes, so
report the depth of the nulls along the wire axis instead, and quote it as a
lower bound set by the noise floor.

## Step 8 — Compare and report

The record sheet is the spine of the report. Every row must be filled, and
every measured row must carry a percent difference against both the
prediction and the simulation.

### Record sheet

| Quantity | Predicted (Step 1) | Simulated (Step 5) | Measured | Difference | Why |
| :-- | :-- | :-- | :-- | :-- | :-- |
| Arm lengths as cut | $7.8\ \text{cm}$ | — | ______ / ______ cm | | |
| Arm lengths after trimming | — | — | ______ / ______ cm | | |
| $f_\text{res}$, untrimmed, no choke | — | — | ______ MHz | | |
| $f_\text{res}$, trimmed, no choke | $915\ \text{MHz}$ | ______ MHz | ______ MHz | | |
| $f_\text{res}$, trimmed, with choke | $915\ \text{MHz}$ | — | ______ MHz | | |
| $Z_{\text{in}}$ at $915\ \text{MHz}$, with choke | $70 + j0\ \Omega$ | ______ | ______ $\Omega$ | | |
| VSWR at $915\ \text{MHz}$, with choke | $1.40$ | ______ | ______ | | |
| VSWR at $915\ \text{MHz}$, matched | $\le 1.2$ (target) | — | ______ | | |
| $-10\ \text{dB}$ bandwidth, with choke | $\approx 70\ \text{MHz}$ | ______ MHz | ______ MHz | | |
| $-10\ \text{dB}$ bandwidth, matched | narrower | — | ______ MHz | | |
| Shift in $f_\text{res}$ from a hand on the coax, no choke / with choke | — | — | ______ / ______ MHz | | |
| Gain | $2.15\ \text{dBi}$ | ______ dBi | ______ $\pm$ ______ dBi | | |
| E-plane HPBW | $78^\circ$ | ______ | ______ $\pm$ ______ | | |
| H-plane ripple, peak to peak | $0\ \text{dB}$ | $0\ \text{dB}$ | ______ dB | | |
| Null depth along the wire axis | $-\infty$ | ______ dB | $\le$ ______ dB (floor) | | |
| XPD at boresight | high | — | ______ dB | | |
| Range margin against $10\lambda$ | $3.3\ \text{m}$ | — | ______ m | | |

### The report

One document, submitted by **2 October**. It should be readable by an
engineer who has not taken this course.

1. **Design.** The frequency, the length calculation, and the prediction table
   from Step 1, as written before the build. A photo of the antenna next to a
   ruler.
2. **Build and first measurement.** Arm lengths as cut and as trimmed. The
   untrimmed and trimmed sweeps, and which way you trimmed and why.
3. **Balun and match.** The with-choke / without-choke comparison, with the
   hand-on-the-coax numbers. The matching-network design from your measured
   impedance, the parts you actually used, the measured result, and the
   ship / re-source / redesign argument.
4. **Simulation.** The NEC model as run (the card deck, verbatim), the average
   gain figure, the frequency sweep, the two pattern cuts, and the convergence
   table with one sentence defending your segment count.
5. **S-parameters.** The calibration verification screenshot. Annotated
   $\vert S_{11}\vert$ plots and Smith charts for both configurations, plotted
   from the Touchstone data, with the simulated sweep overlaid. The perturbation
   results and a paragraph connecting at least one of them to the near-field
   argument in L13.
6. **Pattern.** The range-margin argument. Both principal-plane cuts in polar
   dB, the repeated cut, the noise floor and dynamic range, and the extracted
   table with an uncertainty on every row.
7. **Comparison.** The filled record sheet, and **one paragraph per row that
   disagrees by more than your uncertainty**, naming the mechanism.
   "Simulation error" and "measurement error" are not mechanisms. End effect,
   finite wire radius, feed-line radiation, bench coupling, range reflections,
   reference-antenna gain uncertainty, and parasitic lead inductance are.

### What Mastered looks like

The project is assessed Mastered when all of the following hold. A report
that misses one comes back with feedback and can be resubmitted once.

- Predictions were written before the build and are reported unchanged.
- The antenna resonates within $\pm 2\%$ of $915\ \text{MHz}$ after trimming,
  or the report explains why it could not be brought there.
- The choke's effect is measured and reported, not just asserted.
- A matching network is designed from a measured impedance, built, and its
  result is measured and judged — whatever that result was.
- The simulation passes the average gain test and is run at the as-built
  dimensions.
- Every plot is annotated, has units, and was produced from saved data.
- The gain carries an uncertainty, and the null depth and XPD are quoted
  against the measured noise floor.
- Every disagreement larger than the stated uncertainty has a named physical
  mechanism.

## Resources

- <a href="../../module02/L07-simple-resonant-antennas/index.html">Lesson 7</a>
  — the design numbers, and the dipole explorer and Smith-chart widgets that
  produced them.
- <a href="../../module01/L04-impedance-feeding-baluns/index.html">Lesson 4</a>
  — the L-network method and the balun table;
  <a href="../../module01/L04-lab-matching/index.html">L4 lab</a> — NanoVNA
  calibration and the matching procedure.
- <a href="../../module02/L08-dipole-simulation-lab/index.html">Lesson 8</a>
  — the NEC card deck and the segmentation rules.
- <a href="../../module02/L13-measurement-lab-sparams/index.html">Lesson 13</a>
  — S-parameter measurement, the reference plane, and the pigtail problem.
- <a href="../../module02/L12-pattern-measurement-theory/index.html">Lesson 12</a>
  and <a href="../../module02/L14-measurement-lab-patterns/index.html">Lesson 14</a>
  — range criteria, gain-comparison and two-antenna methods, pattern reduction.
- <a href="../../handouts/SmithChart_blank.pdf" target="_blank" rel="noopener">Blank Smith chart (PDF)</a>
  and the
  <a href="../../handouts/SmithChart_Lynch_tutorial.pdf" target="_blank" rel="noopener">Smith chart walkthrough (PDF)</a>
  from the Materials page.
- <a href="https://nanorfe.com/nanovna-v2-user-manual.html" target="_blank" rel="noopener">NanoVNA user's guide</a>.
