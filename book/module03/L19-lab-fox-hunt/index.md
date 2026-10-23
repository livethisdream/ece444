---
frame_view: true
---

# L19 Lab — Fox Hunt

::::{frame}
:class: title-frame

<div class="course-mark">ECE 444 · Fall 2026</div>

<h1 class="frame-title">Fox Hunt</h1>

<div class="title-rule"></div>

One HB100 is on. Find its box from bearings you take yourself.

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
- One HB100 is on, inside one of five numbered boxes in a keep-out circle.
- Teams of two, two kits, four bearings from anywhere outside the circle.
- Cross the bearings, name the box, and turn in one packet per team.
:::

The L19 Lab puts Lesson 19 on the bench: a bearing from the peak of the beam
sweep, converted to the room's frame with the kit's heading, and bearings from
several places crossed into a fix. Every HB100 but one is switched off, so the
sweep sees a single source, and the live one sits in one of five numbered boxes
placed at random inside a keep-out circle marked on the floor. Every box holds
an HB100, powered or not, so weight gives nothing away.

You work in a team of two with both of your kits. Each kit takes a bearing from
one position, then moves and takes a second, so the team has four bearings: two
to cross and two to check them. You choose the positions, anywhere outside the
circle. An HB100 radiates mainly forward, so a kit behind or well off the side
of the live box may see a weak tone or none; if you cannot find the tone from a
position, move. Your Part 1 script turns the four bearings into a fix in
class, you name the box before the instructor opens them, and Part 3 compares
your fix with the box that was live.
::::

::::{frame} Part 1: The Plan You Bring
:::{present}
- Bearing budget: $1.9^\circ$ with the heading aimed by eye, $1.5^\circ$ taped.
- Stand at least twice the circle's radius out: every box within $\pm 30^\circ$.
- Spread four positions around the circle so bearings cross steeply.
- A tested script: fix, residuals, outlier.
:::

Part 1 of the packet does Lesson 19's numbers for this room. The grid,
multipath, and noise terms are the lesson's; the heading term is
$1.5^\circ$ because you aim each kit at the center mark by eye rather than along
a taped line, which raises the budget from $1.5^\circ$ to

$$\sigma_\beta = \sqrt{0.53^2 + 1.5^2 + 1.0^2 + 0.2^2} = 1.9^\circ.$$

A kit aimed at the center of a circle of radius $a$ sees its edge at
$\sin^{-1}(a/D)$ off broadside, so keeping every box within $\pm 30^\circ$ needs

$$D \ge \frac{a}{\sin 30^\circ} = 2a,$$

$3\ \text{m}$ for a $1.5\ \text{m}$ circle. Closer is better for cross-range
error, so stand near that distance, and spread the four positions around the
circle. Two positions a quarter of the way around from each other see a central
box along lines that cross near $90^\circ$; two opposite each other see it along
nearly the same line, and their bearings barely cross.
The script is the one you test in Part 1 on a supplied set of four bearings,
one of them a reflection; bring it on your laptop.
::::

::::{frame} Room Coordinates
:::{present}
- Origin at the center mark; $x$ and $y$ along the taped axes.
- Room angles counterclockwise from $+x$, seen from above.
- Aim broadside at the center: the heading is $h = \text{atan2}(-y, -x)$.
:::

Every bearing has to be in one frame before the bearings can cross. The
instructor marks the center of the keep-out circle and tapes two perpendicular
axes through it. Measure each kit's position from the center mark along those
axes with a tape, to the middle of the array, between E4 and E5. A $5\ \text{cm}$
error in position moves a bearing line by $5\ \text{cm}$, which is small
next to the $0.14\ \text{m}$ cross-range error of a $2^\circ$ bearing at
$4\ \text{m}$.

For the heading, aim the array's broadside at the center mark: sight along a
straightedge held square to the board, through the center mark. Broadside then
points from the kit toward the origin, so its room angle follows from the
position you measured, $h = \text{atan2}(-y, -x)$, and you do not need a separate
angle measurement. Sighting by eye holds this to about $1.5^\circ$.
::::

::::{frame} From Est. Angle to Room Bearing
:::{present}
$$\beta = h + s\ \bar\theta_\text{est}$$

- $\bar\theta_\text{est}$: mean of ten Est. Angle readings.
- $s = +1$ if positive Est. Angle is counterclockwise on your kit, $-1$ if not.
- The reference shot sets $s$ before the hunt.
:::

Est. Angle is measured from broadside, positive toward the E8 end of the array
(the L18 Lab). Whether the E8 end is the counterclockwise side depends on which
way round the kit sits on its table, so each kit carries a sign $s$. Getting $s$
wrong mirrors the bearing about broadside: a source $10^\circ$ off broadside is
drawn $20^\circ$ away from where it is. The reference shot finds $s$ with your
own HB100 at a known side before the hunt starts.

The sweep jitters a little from one pass to the next, so read Est. Angle on ten
consecutive sweeps from the **Tracking** tab and use their mean. The spread of
those ten, largest minus smallest, should be a degree or two.
::::

::::{frame} Expected Numbers
:::{present}
| Quantity | Expect |
| :-- | :-- |
| Est. Angle at each position | within $\pm 30^\circ$ |
| Spread of ten readings | $1^\circ$ to $2^\circ$ |
| Residual of a good bearing | about $0.1$ to $0.2\ \text{m}$ |
| Fix to live box | about $0.2\ \text{m}$ |
:::

With every position $3$ to $4\ \text{m}$ from the box and a bearing budget near
$2^\circ$, each bearing line passes within about
$R\tan\sigma_\beta = 0.10$ to $0.14\ \text{m}$ of the source, and a well-spread
set of four puts the fix about $0.2\ \text{m}$ from it. The boxes are at least
$0.75\ \text{m}$ apart, so a fix that close names the right one.

A residual much larger than $0.2\ \text{m}$ flags a bad bearing. Retake it if
there is time; otherwise drop it and solve with the other three, as Part 1 does
on the practice set. A spread of ten readings near $5^\circ$ usually means the
receiver is near full scale; lower **Rx Gain (dB)** by $10\ \text{dB}$ and read
again.
::::

::::{frame} Bring Up Both Kits
:class: read-only

:::{present}
1. Each partner browses to their own kit's address and waits for the pill to read **Connected**.
2. Place your own powered HB100 $1\ \text{m}$ out at boresight, facing the array.
3. Press **Find HB100** and record the Signal Freq in the packet.
4. Press **Calibrate** and wait for it to finish.
5. Open the **Lab Presets** section, press **1 Steering Angle**, and set **Rx Gain (dB)** for an FFT peak of $-10 \pm 3$ dBFS; record it.
6. Press **Start**, and check the **FFT** tab for one tone near $0\ \text{MHz}$, at least $20\ \text{dB}$ above the floor.
:::

This is the L18 Lab's bring-up, done on both kits. Calibrate needs your own
HB100 at boresight while it runs; it is the only time today that a source sits
there on purpose. Set the kits on tables at the height of the boxes: a kit below
the boxes reads every bearing too close to broadside (Lesson 19, "The Cone
Angle").
::::

::::{frame} Reference Shot
:class: read-only

:::{present}
7. Move your HB100 to $2\ \text{m}$ out and about $20^\circ$ to the left of broadside, seen from behind the array.
8. Read **Est. Angle** and record $s$: $+1$ if it is positive, $-1$ if negative.
9. Switch your HB100 off and disconnect its power. Leave it off for the rest of the period.
10. When the instructor starts the hunt, press **Find HB100** again on both kits, and record the fox's Signal Freq. Do not press **Calibrate**.
:::

The reference shot checks two things. The sign tells you $s$, and the size
checks the setup: a reading far from $20^\circ$ means the source or the kit is
not where you think. The instructor starts the hunt only once every team's
HB100 is off, because a second live source in the room pulls every sweep's peak
toward it (Lesson 19, "Accuracy Is Not Resolution").

Step 10 matters. Every HB100 runs at a slightly different frequency, often tens
of megahertz apart, and the receiver sees only a few megahertz around the
frequency Find HB100 stored. A kit still tuned to your own HB100 shows no tone
from the fox at all. Pressing Find HB100 with only the fox on tunes the kit to
it, and the steering phases follow the new frequency. Both kits should report
the same frequency to within a few megahertz; if they do not, one has found
something else. Keep the calibration from bring-up.
::::

::::{frame} The Hunt
:class: read-only

:::{present}
11. Set each kit at its first planned position, on a table, outside the circle.
12. Aim broadside at the center mark, and measure the position along the taped axes.
13. Open the **Tracking** tab and record ten consecutive Est. Angle readings and **Peak Array Gain**.
14. Move each kit to its second position and repeat steps 12 and 13.
15. Compute each room bearing, $\beta = h + s\ \bar\theta_\text{est}$, in the packet.
:::

Stay out of the lines of sight while the other kit is reading: a person near the
path between a kit and the boxes reflects enough to move its peak. If Est. Angle
falls outside $\pm 30^\circ$, the position is too close or aimed too far off;
move it and measure again. The fox is farther away than your own HB100 was, so
its tone is weaker: raise **Rx Gain (dB)** until its FFT peak is back near
$-10$ dBFS, and record the new setting. If there is still no tone, the live box may face away
from you: move the kit around the circle and look again.
::::

::::{frame} The Call and the Reveal
:class: read-only

:::{present}
16. Run your Part 1 script on the four bearings and record the fix and the residuals.
17. If one residual is far larger than the rest, drop it and solve again.
18. Name the box nearest the fix and tell the instructor before the boxes are opened.
19. Record the live box after the reveal, then press **Stop** and leave each kit where it is.
:::

The fix is your team's call, made in class from your own data; there is no
class-combined answer. The instructor posts the live box's measured position
after the period, and Part 3 compares your fix with it.
::::

::::{frame} Lab Packet
:class: read-only doc-links

The L19 Lab packet is one submission per team for the whole lab, turned in complete before Lesson 20. It has three parts:

1. **Part 1, Pre-Lab** (both partners, before the lab period): the bearing error budget, a plan for where to stand, and the triangulation script, tested on a supplied set of four bearings.
2. **Part 2, Measurements** (your team, in class): the reference shot, the four bearings, and the call.
3. **Part 3, Writeup** (your team, after the lab): the fix against the live box, the error of each bearing, and what changes with the geometry.

- <a class="doc-link" href="../../labs/ECE444_Lab_L19_FoxHunt_blank.pdf" target="_blank" rel="noopener">L19 Lab packet (PDF)</a>
::::

::::{frame} Looking Ahead
:::{present}
- Keep your bearings and your script: Part 3 reuses both.
- L20 returns to the pattern the sweep traces: nulls, sidelobes, and beamwidth.
:::

Lesson 20 derives the features of the trace you used today to find the peak,
starting from the closed-form array factor: where the nulls fall, why the first
sidelobe sits $12.8\ \text{dB}$ down, and how the beamwidth depends on the number
of elements.
::::
