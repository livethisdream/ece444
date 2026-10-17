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

::::{frame} Slides
:class: read-only

:::{admonition} Slides
:class: slides
<a href="../../slides/L19-lab-fox-hunt.html" target="_blank" rel="noopener">html slides</a>
<a href="../../slides/L19-lab-fox-hunt.html?print-pdf" target="_blank" rel="noopener">pdf slides</a>
<a href="../../slides/L19-lab-fox-hunt.md" target="_blank" rel="noopener">raw markdown slides</a>
:::
::::

::::{frame} Learning Objectives

<ol class="lo-list" style="--module: '3'; counter-reset: lo 4">
  <li>I can implement beam steering on the ADALM-PHASER and verify the steered pattern against theory.</li>
</ol>
::::

::::{frame} What Happens This Period
:::{present}
- One HB100 is on, inside one of several numbered boxes.
- Teams of two: take bearings from anywhere outside the keep-out zone.
- Cross the bearings, name the box, and write one report per team.
:::

The L19 Lab puts Lesson 19 on the bench: a bearing from the peak of the beam
sweep, converted to the room's frame with the kit's heading, and bearings from
two or more places crossed into a fix. Every HB100 but one is switched off, so
the sweep sees a single source, and the live one sits in one of several numbered boxes
placed at random inside a keep-out zone marked on the floor. You work in a team
of two with both of your kits, and you can measure from wherever you like as
long as you stay outside the zone. Note where each kit sits and which way its
array faces, then read the source's angle off the beam sweep's
**Est. Angle**, exactly as in the L18 Lab, and add the heading to get the room
bearing. A short Python script solves for the point closest to all of the
bearing lines, and the box nearest that fix is your answer. Plan where to stand
before the period: the crossing angle between your two bearings sets the error
of the fix as much as the instrument does. There is no class-combined answer: each team finds the fox from its
own two kits and turns in one report.
::::

::::{frame} Under Construction
:class: read-only

```{note}
Lesson material is under construction. This shell maps to objective 3.5. The
L19 Lab packet is coming: a pre-lab (the bearing error budget, the choice of
where to measure from, and the triangulation script on a supplied bearing set), the bench
measurements, and the report, one per team of two. The procedure frames and the
packet arrive with it.
```
::::
