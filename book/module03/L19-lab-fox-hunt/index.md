---
frame_view: true
---

# L19 Lab — Fox Hunt

::::{frame}
:class: title-frame

<div class="course-mark">ECE 444 · Fall 2026</div>

<h1 class="frame-title">Fox Hunt</h1>

<div class="title-rule"></div>

One HB100 is on. Find its box from bearings taken along a firing line.

L19 Lab · Antennas, Phased Arrays, and Radar Systems · Dr. Neil Rogers
::::

::::{frame} Printing
:class: read-only

To print the slides, switch to present mode and print: one slide a sheet,
with room for notes. Print from read mode for the whole lesson.
::::

::::{frame} Learning Objectives

<ol class="lo-list" style="--module: '3'; counter-reset: lo 4">
  <li>I can implement beam steering on the ADALM-PHASER and verify the steered pattern against theory.</li>
</ol>
::::

::::{frame} What Happens This Period
:::{present}
- One HB100 is on, in one of five numbered boxes downrange.
- Kits sit on a firing line, broadside pointed straight downrange.
- Bearings from stations along the line cross at the fox; amplitude breaks ties.
:::

The L19 Lab puts Lesson 19 on the bench as a firing range. A taped firing line
runs across the room, and five numbered boxes sit downrange of it at positions
the instructor measured and posted. Every box holds an HB100, powered or not, so
weight gives nothing away; one of them is live.

Your team moves its kit along the firing line, stopping at the station marks
taped every $0.75\ \text{m}$. At each station the kit faces straight downrange,
square to the tape, so every station shares one heading and the only thing that
changes is where along the line you stand. At each station you read the beam
sweep's **Angle** readout (set to Peak) and **Peak Gain**. Each angle is a line from that
station toward the fox; the lines cross at the fox, and the box nearest the
crossing is your call. Peak Gain plays a smaller part: when two boxes sit
close to the crossing, the pattern of levels along the line says which one fits.
::::

::::{frame} The Hunt in Five Steps
:::{present}
<picture>
<source media="(max-width: 600px)" srcset="../../viz/img/L19-lab-sequence-narrow.svg">
<img src="../../viz/img/L19-lab-sequence.svg" alt="The L19 Lab in five steps, each a top view of the firing range. 1, bring up: your own HB100 at boresight, then Find HB100 and Calibrate. 2, reference shot: a source toward the plus-x end sets the sign s of Angle. 3, walk the line: with the fox on, read Angle and Peak Gain at each station mark. 4, fix: the bearings cross at a box, which is your call. 5, reveal: the instructor names the live box, and Part 3 reconciles." style="max-width: 100%; display: block; margin: 0 auto;">
</picture>
:::

Steps 1 and 2 happen before the fox goes on: the bring-up on your own HB100,
then the reference shot that fixes which end of the tape positive Angle points
to. Steps 3 and 4 are the hunt: the same measurement at every station mark,
then the fix. Step 5 is the instructor's, and Part 3 of the packet starts
from it.
::::

::::{frame} The Range
:::{present}
| Element | Size |
| :-- | :-- |
| Firing line | $3.0\ \text{m}$ of tape, stations every $0.75\ \text{m}$ (5) |
| Box field | $2.0\ \text{m}$ wide, $1.0$ to $2.0\ \text{m}$ downrange |
| Box spacing | at least $0.75\ \text{m}$ center to center |
| Footprint | about $3\ \text{m} \times 2.5\ \text{m}$ |
:::

The range fits a classroom. The firing line runs $0.5\ \text{m}$ past the box
field at each end, so a box near the edge still sits within about
$\pm 45^\circ$ of several stations. The nearest boxes are $1.0\ \text{m}$ out,
past the $0.88\ \text{m}$ far-field distance of Lesson 17, and the farthest are
$2.0\ \text{m}$ out, where the tone is still well above the floor.

These sizes come from a simulation of the hunt with a bearing error of
$2.5^\circ$, a bearing off by $10^\circ$ one time in seven, and an HB100 aimed
only roughly at the line: the call names the right box about $86\%$ of the
time, and the median fix lands $0.15\ \text{m}$ from the fox. A wider room helps less than
you might expect; a deeper field hurts more, because depth is the direction a
single firing line measures worst.
::::

::::{frame} Part 1: The Plan You Bring
:::{present}
- Bearing budget with a fixed heading: about $1.5^\circ$.
- At range $R$: across range $R\tan\sigma_\beta$, in depth $\sqrt{2}\,R^2\sigma_\beta / B$.
- Use the ends of the line: the baseline $B$ sets the depth error.
- A tested script: fix, residuals, outlier, box ranking.
:::

Part 1 of the packet does Lesson 19's numbers for this range. Squaring the kit
to the tape replaces the aimed heading of a free-standing kit: the grid,
multipath, and noise terms are the lesson's, and squaring by eye adds about
$1^\circ$, so

$$\sigma_\beta = \sqrt{0.53^2 + 1.0^2 + 1.0^2 + 0.3^2} \approx 1.5^\circ.$$

The geometry has a weak direction. Bearings from a firing line all look
downrange, so they cross steeply only when the stations are far apart compared
with the depth. Two stations a baseline $B$ apart fix a box at range $R$ across
range to about $R\tan\sigma_\beta$, $0.05\ \text{m}$ at $2\ \text{m}$, but in
depth only to about $\sqrt{2}\,R^2\sigma_\beta/B$ (Lesson 19 derives it): for a
box $2\ \text{m}$ out between the two stations, $0.08\ \text{m}$ with the
ends of the line, $B = 3\ \text{m}$; $0.11\ \text{m}$ with $B = 1.5\ \text{m}$;
and $0.20\ \text{m}$ with neighbors, $B = 0.75\ \text{m}$. Plan to use the
stations farthest apart that still hear the fox.

The script is yours. Start from the
<a href="../../labs/foxhunt_starter.py" download>starter file</a>, which reads the
station and box files and prints the results, and write its four functions in
Part 1. Test it there on a supplied set of bearings with one bad station in it,
and bring it on your laptop.
::::

::::{frame} Range Coordinates
:::{present}
- $x$ along the tape, $y$ straight downrange; origin at station 0.
- Every kit faces $+y$, so a bearing is the line $x = x_i + y\tan\theta_i$.
- The reference shot sets which end of the tape positive Angle points to.
:::

The instructor tapes the firing line and marks station 0 at its middle, with
stations at $x = -1.5, -0.75, 0, +0.75, +1.5\ \text{m}$, and posts the measured
center of every box in the same frame. Place the middle of the array, between E4
and E5, on the station mark, and square the board's patch face to the tape with
a straightedge or a square, so broadside points straight downrange.

Because every station faces the same way, there is no heading to work out. Est.
Angle $\theta_i$ at station $x_i$ says the fox lies on the line
$x = x_i + y\tan\theta_i$, with $\theta_i$ positive toward the $+x$ end of the
tape. Whether positive Angle points to $+x$ depends on which way round the
board sits on its stand, which is what the reference shot checks.

The sweep jitters a little from one pass to the next, so read Angle on ten
consecutive sweeps from the **Tracking** tab and use their mean. The spread of
those ten, largest minus smallest, should be a degree or two.
::::

::::{frame} Expected Numbers
:::{present}
| Quantity | Expect |
| :-- | :-- |
| Stations hearing the fox | 2 to 4 of 5 |
| Angle at a useful station | within $\pm 45^\circ$ |
| Spread of ten readings | $1^\circ$ to $2^\circ$ |
| Good-bearing residual | under $0.15\ \text{m}$ |
| Fix to live box | $0.15$ to $0.2\ \text{m}$ |
:::

An HB100 radiates mainly forward, so stations far off its axis may see a weak
tone or none; skip those and keep going. A residual far larger than the rest
flags a bad bearing, usually a reflection or a person in the path: retake it,
or let your script drop it. The boxes are at least $0.75\ \text{m}$ apart, so a
fix within $0.2\ \text{m}$ names the right one.

Peak Gain is useful only when **Rx Gain (dB)** is the same at every
station. Your script compares the levels along the line with the shape a source
in each candidate box would produce, free-space spreading plus the element
roll-off you measured in the L18 Lab, with the overall level fitted out. It
cannot give a range on its own: the fox's aim and the room's reflections move
the level by several dB.
::::

::::{frame} Bring Up the Kit
:class: read-only

:::{present}
1. Browse to your kit's address and wait for the pill to read **Connected**.
2. Place your own powered HB100 $1\ \text{m}$ out at boresight, facing the array.
3. Press **Find HB100** and record the Signal Freq in the packet.
4. Press **Calibrate** and wait for it to finish.
5. Open **Lab Presets**, press **1 Steering Angle**, and set **Rx Gain (dB)** for an FFT peak of $-10 \pm 3$ dBFS.
6. Press **Start**, and check the **FFT** tab for one tone near $0\ \text{MHz}$, at least $20\ \text{dB}$ above the floor.
:::

This is the L18 Lab's bring-up. Calibrate needs your own HB100 at boresight
while it runs; it is the only time today a source sits there on purpose. The
kit goes on a stand or a table at the height of the boxes for every reading:
a kit below the boxes reads every bearing too close to broadside (Lesson 19,
"The Cone Angle"), and a kit held by hand reads it wrong by far more than the
budget.
::::

::::{frame} Reference Shot
:class: read-only

:::{present}
7. Put the kit on station 0, squared to the tape.
8. Place your HB100 $1\ \text{m}$ downrange and $0.5\ \text{m}$ toward the $+x$ end, facing the kit.
9. Read **Angle**: about $27^\circ$. Record $s = +1$ if it is positive, $-1$ if negative.
10. Switch your HB100 off and disconnect its power for the rest of the period.
11. When the hunt starts, press **Find HB100** again and record the fox's Signal Freq. Do not press **Calibrate**.
:::

The reference shot checks two things. The sign gives $s$, which you apply to
every reading so that $s\,\theta$ is positive toward $+x$; the size checks the
setup, since $\tan^{-1}(0.5/1.0) = 26.6^\circ$. A reading far from that means
the kit is not square to the tape or the source is not where you think.

Step 11 matters. Every HB100 runs at a slightly different frequency, often tens
of megahertz apart, and the receiver sees only a few megahertz around the
frequency Find HB100 stored. Pressing Find HB100 with only the fox on tunes the
kit to it. Keep the calibration from bring-up.
::::

::::{frame} The Hunt
:class: read-only

:::{present}
12. Set **Rx Gain (dB)** for a clear tone from the fox at station 0 and record it. Leave it there.
13. Put the kit on a station mark, squared to the tape, broadside downrange.
14. On the **Tracking** tab, record ten consecutive Angle readings and **Peak Gain**.
15. Repeat at every station that hears the fox, ends first.
16. Write each row as $x_i$, $s\,\bar\theta_i$, Peak Gain into `stations.csv`.
:::

Take the end stations first: they set the baseline, and the baseline sets the
depth error. Stay out of the line of sight while the kit is reading; a person
near the path reflects enough to move the peak. If a station shows no clear tone
or reads beyond $\pm 45^\circ$, record that and move on rather than turning the
kit toward the fox, because a turned kit no longer shares the heading of the
others.

Do not change Rx Gain once the hunt starts. The bearings do not care, but the
amplitude ranking compares levels across stations and assumes one gain for all
of them.
::::

::::{frame} The Call and the Reveal
:class: read-only

:::{present}
17. Run your Part 1 script on `stations.csv` and `boxes.csv`, and record the fix, the residuals, and the ranking.
18. If one residual is far larger than the rest, retake that station or accept your script's drop.
19. Name the box and tell the instructor before the boxes are opened.
20. Record the live box after the reveal, then press **Stop**.
:::

`boxes.csv` holds the posted box centers. Your script fixes the source from the
bearings alone, ranks the boxes by distance from the fix, and, when the two
nearest are within $0.15\ \text{m}$ of each other in distance, uses the amplitude
pattern to choose between them. The call is your team's, made in class from your
own data. Part 3 compares your fix with the live box and asks what changes with
the baseline and the depth.
::::

::::{frame} Lab Packet
:class: read-only doc-links

The L19 Lab packet is one submission per team for the whole lab, turned in complete before Lesson 20. It has three parts:

1. **Part 1, Pre-Lab** (before the lab period): the bearing budget with a fixed heading, the across-range and depth errors for this range, a station plan, and the script tested on a supplied set of bearings.
2. **Part 2, Measurements** (your team, in class): the reference shot, the bearings and levels from every station, and the call.
3. **Part 3, Writeup** (after the lab): the fix against the live box, the error of each bearing, and what the baseline and the depth did to the fix.

- <a class="doc-link" href="../../labs/ECE444_Lab_L19_FoxHunt_blank.pdf" target="_blank" rel="noopener">L19 Lab packet (PDF)</a>
::::

::::{frame} Looking Ahead
:::{present}
- Keep your bearings, levels, and script: Part 3 reuses all three.
- L20 returns to the pattern the sweep traces: nulls, sidelobes, and beamwidth.
:::

Lesson 20 derives the features of the trace you used today to find the peak,
starting from the closed-form array factor: where the nulls fall, why the first
sidelobe sits $12.8\ \text{dB}$ down, and how the beamwidth depends on the number
of elements.
::::
