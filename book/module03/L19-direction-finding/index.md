---
frame_view: true
---

# L19 - Direction Finding

::::{frame}
:class: title-frame

<div class="course-mark">ECE 444 · Fall 2026</div>

<h1 class="frame-title">Direction Finding</h1>

<div class="title-rule"></div>

One bearing says which way; two bearings from known places say where.

Lesson 19 · Antennas, Phased Arrays, and Radar Systems · Dr. Neil Rogers
::::

::::{frame} Slides
:class: read-only

:::{admonition} Slides
:class: slides
<a href="../../slides/L19-direction-finding.html" target="_blank" rel="noopener">html slides</a>
<a href="../../slides/L19-direction-finding.html?print-pdf" target="_blank" rel="noopener">pdf slides</a>
<a href="../../slides/L19-direction-finding.md" target="_blank" rel="noopener">raw markdown slides</a>
:::
::::

::::{frame} Learning Objectives

<ol class="lo-list" style="--module: '3'; counter-reset: lo 4">
  <li>I can implement beam steering on the ADALM-PHASER and verify the steered pattern against theory.</li>
</ol>
::::

::::{frame} A Bearing from the Beam Sweep
:::{present}
- The sweep peaks where the beam points at the source: **Est. Angle** is a bearing.
- Bearing error at $30^\circ$, heading taped to $1^\circ$: about $1.5^\circ$ RSS.
- Keep the source within $\pm 30^\circ$ of broadside.
:::

The L18 Lab showed that the beam sweep peaks at the source, so the angle of
that peak is a bearing from the array to the source, measured from the
array's broadside. In the field the array's heading is the new term in the
error budget: how well broadside is known in the room. Taping the array's edge
to a heading line holds it to about $1^\circ$, and with the $0.53^\circ$ grid
half-step at $30^\circ$ and $1^\circ$ of multipath the bearing error is
$\sqrt{0.53^2 + 1.0^2 + 1.0^2} = 1.5^\circ$. The sweep grid widens as
$1/\cos\theta$, so the source is best kept within $\pm 30^\circ$ of broadside.
::::

::::{frame} Triangulation
:::{present}
- Each bearing from a known station is a line on the floor plan.
- Two lines cross at the source; three give an outlier check.
- A least-squares fix is about 20 lines of Python.
:::

A bearing alone says which way, not how far. Take a second bearing from a
different, known position and heading, draw both as lines on the floor plan,
and they cross at the source. Real bearings carry error, so with three or more
lines the crossing is a small triangle rather than a point; the least-squares
fix is the point closest to all of the lines, and a bearing that misses the
others badly is the outlier to check (a reflection off a whiteboard is the
usual culprit).
::::

::::{frame} How the Crossing Angle Sets the Error
:::{present}
| Geometry, kits $4\ \text{m}$ out, $\sigma = 2^\circ$ | RMS fix error |
| :-- | :-- |
| 2 kits, $90^\circ$ crossing | $0.20\ \text{m}$ |
| 2 kits, $30^\circ$ | $0.39\ \text{m}$ |
| 2 kits, $15^\circ$ | $0.76\ \text{m}$ |
| 3 kits over $120^\circ$ | $0.16\ \text{m}$ |
:::

Each bearing error $\sigma$ moves its line sideways by the cross-range
$R\tan\sigma$: $0.10\ \text{m}$ at $3\ \text{m}$ and $0.14\ \text{m}$ at
$4\ \text{m}$ for $\sigma = 2^\circ$. Two lines that cross steeply pin the
source in both directions; two that cross at a shallow angle $\gamma$ leave an
error ellipse whose long axis grows as $1/\sin\gamma$. Choosing stations is
therefore part of the measurement: spread them around the source, and keep
every box at the array's height, since a horizontal line array measures the
cone angle and a source below it reads a smaller bearing.
::::

::::{frame} Under Construction
:class: read-only

```{note}
Lesson material is under construction. This shell maps to objective 3.5. The
lesson's frames, figures, and problems arrive with the L19 Lab packet; the
numbers above are from the Module 4-5 build-out plan.
```
::::

::::{frame} The L19 Lab
:class: read-only doc-links

The bench half of this lesson is the L19 Lab, the fox hunt: find the one live
HB100 among numbered boxes from bearings you and a partner take on your two kits.

- <a class="doc-link" href="../L19-lab-fox-hunt/index.html">L19 Lab — Fox Hunt</a>
::::
