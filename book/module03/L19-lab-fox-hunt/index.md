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

::::{frame} The Fox Hunt
:::{present}
- One HB100 is on, hidden in one of several numbered boxes.
- Take measurements at different points on the table and determine which box contains the HB100.
:::

The L19 Lab puts Lesson 19 on the bench as a fox hunt. A taped firing line runs
along the table, and numbered boxes sit downrange of it at positions I
measured and posted. Every box holds an HB100, powered or not, so
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
<img src="../../viz/img/L19-lab-sequence.svg" alt="The L19 Lab in five steps, each a top view of the firing range. 1, bring up: your own HB100 at boresight, then Find HB100 and Calibrate. 2, reference shot: a source toward the plus-x end sets the sign s of Angle. 3, walk the line: with the fox on, read Angle and Peak Gain at each station mark. 4, fix: the bearings cross at a box, which is your call. 5, reveal: I name the live box, and the Part 3 writeup compares it with your fix." style="max-width: 100%; display: block; margin: 0 auto;">
</picture>
:::

Steps 1 and 2 happen before the fox goes on: the bring-up on your own HB100,
then the reference shot that fixes which end of the tape positive Angle points
to. Steps 3 and 4 are the hunt: the same measurement at every station mark,
then the fix. Step 5 is mine, and the Part 3 writeup starts
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
$\pm 45^\circ$ of several stations, the edge of what the PHASER can track. The nearest boxes are $1.0\ \text{m}$ out,
past the $0.88\ \text{m}$ far-field distance of Lesson 17, and the farthest are
$2.0\ \text{m}$ out, where the tone is still well above the floor.

These sizes come from a simulation of the hunt with a bearing error of
$2.5^\circ$, a bearing off by $10^\circ$ one time in seven, and an HB100 aimed
only roughly at the line: the call names the right box about $86\%$ of the
time, and the median fix lands $0.15\ \text{m}$ from the fox. A wider room helps less than
you might expect; a deeper field hurts more, because depth is the direction a
single firing line measures worst.
::::

::::{frame} Pre-Lab
:::{present}
- Bring the <a href="../../notebooks/L19_foxhunt.ipynb" download>fox-hunt notebook</a>, tested, on your laptop.
- It finds where the bearings cross, flags a bad one, and ranks the boxes.
- <a href="../../labs/ECE444_Lab_L19_FoxHunt_blank.pdf" target="_blank" rel="noopener">Part 1 of the packet</a> walks you through it.
:::

The Pre-Lab is Part 1 of the packet, done before the lab period and listed at
the end of
<a href="../L19-direction-finding/index.html">Lesson 19</a>. What you need at
the bench is the notebook,
<a href="../../notebooks/L19_foxhunt.ipynb" download>`L19_foxhunt.ipynb`</a>:
it holds the practice set, draws every bearing line over the boxes, and prints
the results. Write its four functions and run it on the practice set, which
has one bad station in it. The
error budget and station plan in Part 1 tell you what to expect: use the
stations farthest apart that still detect the fox, because the distance
between them sets how well the fix is pinned down in depth.
::::

::::{frame} Range Coordinates
:::{present}
- Origin is at the center of the table, on the middle station.
- $x$ runs along the tape, $y$ straight downrange.
- Each Angle draws a line from its station toward the fox.
- The reference shot sets which end is positive.
:::

I tape the firing line and mark station 0 at its middle, with
stations at $x = -1.5, -0.75, 0, +0.75, +1.5\ \text{m}$, and post the measured
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

::::{frame} What to Expect
:::{present}
- Most stations detect the fox, but the far ends may not.
- Ten readings at one station agree within a degree or two.
- The bearing lines cross within a hand's width of the live box.
:::

An HB100 radiates mainly forward, so expect two to four of the stations to
detect it; a station far off its axis may see a weak tone or none, and one that
reads beyond $\pm 45^\circ$ is past what the PHASER tracks. Skip those and keep
going. A good bearing passes within about $0.15\ \text{m}$ of the fix; one that
misses by far more than the rest is a bad bearing, usually a reflection or a
person in the path: retake it, or let your notebook drop it. The fix should land
$0.15$ to $0.2\ \text{m}$ from the live box, and the boxes are at least
$0.75\ \text{m}$ apart, so that is close enough to name the right one.

Peak Gain is useful only when **Rx Gain (dB)** is the same at every
station. Your notebook compares the levels along the line with the shape a source
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

<div class="rec" data-lab="L19">
<label>Step 3: your own HB100's Signal Freq <input data-field="f.own"></label>
</div>

This is the L18 Lab's bring-up. Calibrate needs your own HB100 at boresight
while it runs; it is the only time today a source sits there on purpose. The
kit stays on its stand for every reading, pointed at the boxes with its element
row level: raising one end of the row tilts the cone of directions and pulls
every bearing toward broadside (Lesson 19, "The Cone Angle"), and a kit held by
hand reads it wrong by far more than the budget.

If the boxes sit lower than the kit, as they do when the boxes are on the
floor and the kit is on a table, every reading is pulled toward broadside too,
by several degrees at these ranges. Measure the height difference between the
middle of the array and the boxes, record it with your readings, and correct
each Angle before you trust the fix, as Lesson 19's "The Cone Angle" shows.
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

<div class="rec" data-lab="L19">
<label>Step 9: Angle, source toward +x <input data-field="ref.angle"></label>
<label>Step 9: the sign s <input data-field="ref.s"></label>
<label>Step 11: the fox's Signal Freq, after re-tune <input data-field="f.fox"></label>
</div>

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
15. Repeat at every station that detects the fox, ends first.
16. Type each station into the notebook and run the plot. Retake any station whose line misses the crossing, then press **Stop**.
:::

<div class="rec" data-lab="L19">
<label>Step 12: Rx Gain for the hunt <input data-field="f.gain"></label>
<label>Station −1.5 m: s times the mean Angle <input data-field="h.m150.theta"></label>
<label>Station −1.5 m: spread <input data-field="h.m150.spread"></label>
<label>Station −1.5 m: Peak Gain <input data-field="h.m150.gain"></label>
<label>Station −1.5 m: use it? <input data-field="h.m150.use"></label>
<label>Station −0.75 m: s times the mean Angle <input data-field="h.m075.theta"></label>
<label>Station −0.75 m: spread <input data-field="h.m075.spread"></label>
<label>Station −0.75 m: Peak Gain <input data-field="h.m075.gain"></label>
<label>Station −0.75 m: use it? <input data-field="h.m075.use"></label>
<label>Station 0.0 m: s times the mean Angle <input data-field="h.0.theta"></label>
<label>Station 0.0 m: spread <input data-field="h.0.spread"></label>
<label>Station 0.0 m: Peak Gain <input data-field="h.0.gain"></label>
<label>Station 0.0 m: use it? <input data-field="h.0.use"></label>
<label>Station +0.75 m: s times the mean Angle <input data-field="h.p075.theta"></label>
<label>Station +0.75 m: spread <input data-field="h.p075.spread"></label>
<label>Station +0.75 m: Peak Gain <input data-field="h.p075.gain"></label>
<label>Station +0.75 m: use it? <input data-field="h.p075.use"></label>
<label>Station +1.5 m: s times the mean Angle <input data-field="h.p150.theta"></label>
<label>Station +1.5 m: spread <input data-field="h.p150.spread"></label>
<label>Station +1.5 m: Peak Gain <input data-field="h.p150.gain"></label>
<label>Station +1.5 m: use it? <input data-field="h.p150.use"></label>
</div>

Take the end stations first: they set the baseline, and the baseline sets the
depth error. Stay out of the line of sight while the kit is reading; a person
near the path reflects enough to move the peak. If a station shows no clear tone
or reads beyond $\pm 45^\circ$, record that and move on rather than turning the
kit toward the fox, because a turned kit no longer shares the heading of the
others.

Do not change Rx Gain once the hunt starts. The bearings do not care, but the
amplitude ranking compares levels across stations and assumes one gain for all
of them.

The plot is your last check before you leave the bench. It draws each station's
bearing line over the posted boxes, even before your functions are finished, and
the lines should cross near one box. A line that misses the crossing is a station
to retake now, while the kit is still set up; once you leave, a bad bearing can
only be dropped.
::::

::::{frame} The Call and the Reveal
:class: read-only

:::{present}
17. Type the posted boxes into the notebook, run it, and record the fix, the residuals, and the ranking.
18. If one residual is far larger than the rest, accept the notebook's drop.
19. Submit the box you name before the reveal, at the bench or after class.
20. Record the live box after the reveal.
:::

<div class="rec" data-lab="L19">
<label>Step 17: the fix (m) <input data-field="call.fix"></label>
<label>Step 17: largest residual <input data-field="call.resid"></label>
<label>Step 18: station dropped <input data-field="call.dropped"></label>
<label>Step 19: the box you named <input data-field="call.named"></label>
<label>Step 20: the live box <input data-field="call.live"></label>
</div>

The instructor posts the box centers. Your notebook fixes the source from the
bearings alone, ranks the boxes by distance from the fix, and, when the two
nearest are within $0.15\ \text{m}$ of each other in distance, uses the amplitude
pattern to choose between them. The call is your team's, made from your own
data. The notebook needs only your laptop, so you can make the call at the bench
or after class, wherever you are; I reveal the live box once every team's call
is in. The Part 3 writeup compares your fix with the live box and asks what
changes with the baseline and the depth.
::::

::::{frame} Your Part 2 Entries
:class: read-only

Every box you filled in on this page, in one place. Your entries stay in this
browser only, saved as you type. **Download my packet** writes them into Part 2
of the blank packet and saves the PDF; do Parts 1 and 3 on paper or in the PDF
viewer, and upload one PDF to Gradescope. If you have already typed Part 1 into
the packet PDF, use **Fill my own copy** and choose that file instead: your Part 1
is kept, and Part 2 is added to it. Either way the result is locked, so finish
any typing in the PDF first. **Export entries** saves a small backup file you
can **Import** on another laptop or after clearing your browser. The boxes are
optional: the blank packet is in the next frame, to fill on paper or in a PDF
viewer instead.

<div class="rec-summary" data-lab="L19" data-pdf="../../labs/ECE444_Lab_L19_FoxHunt_blank.pdf" data-file="ECE444_L19_Lab"></div>
::::

::::{frame} Lab Packet
:class: read-only doc-links

The L19 Lab packet is one submission per team for the whole lab, turned in complete before Lesson 20. It has three parts:

1. **Part 1, Pre-Lab** (before the lab period): the bearing budget with a fixed heading, the across-range and depth errors for this range, a station plan, and the notebook tested on a supplied set of bearings.
2. **Part 2, Measurements** (your team): the reference shot and the bearings and levels from every station, in class; the call, at the bench or after class, before the reveal.
3. **Part 3, Writeup** (after the reveal): the fix against the live box, the error of each bearing, and what the baseline and the depth did to the fix.

- <a class="doc-link" href="../../labs/ECE444_Lab_L19_FoxHunt_blank.pdf" target="_blank" rel="noopener">L19 Lab packet (PDF)</a>
::::

::::{frame} Looking Ahead
:::{present}
- Use your recorded data in the notebook to solve for the fox's location.
- L20 returns to shaping and steering the beam.
:::

Part 3 is the writeup, done as a team after the reveal: how far your fix landed
from the live box, the error of each bearing, and what the baseline and the
depth did to the fix.

Lesson 20 returns to shaping and steering the beam, starting from the
closed-form array factor: where the nulls fall, why the first sidelobe sits
$12.8\ \text{dB}$ down, and how the beamwidth depends on the number of elements.
::::
