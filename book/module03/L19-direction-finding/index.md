---
frame_view: true
---

# L19 - Direction Finding

::::{frame}
:class: title-frame

<div class="course-mark">ECE 444 · Fall 2026</div>

<h1 class="frame-title">Direction Finding</h1>

<div class="title-rule"></div>

An array measures the direction a signal comes from, and bearings from known places locate the transmitter.

Lesson 19 · Antennas, Phased Arrays, and Radar Systems · Dr. Neil Rogers
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

:::{depth}
L18 worked out the phase each element needs to point the beam at a commanded
angle, and the L18 Lab checked the steered pattern against that prediction.
This lesson runs the same physics in the other direction. The transmitter is
somewhere we do not know, and the array has to tell us which way it is. We
start from the phase ramp an arriving wave puts across the array, show why
sweeping the beam finds that ramp, work out how accurately the peak of the
sweep gives the direction, and then combine directions measured from two or
more known places into a position. The L19 Lab uses all of it to find one live
HB100 among several boxes.
:::
::::

::::{frame} Finding a Transmitter
:::{present}
- **Direction finding** locates a transmitter from its own signal.
- One array measures a **bearing**: the direction the wave arrives from.
- A passive receiver has no echo delay to give range.
- Bearings from two known positions cross at the transmitter.
:::

Direction finding is the problem of locating a transmitter from the signal it
emits: a radio beacon, a jammer, a lost aircraft's emergency locator, or, in
the L19 Lab, an HB100 hidden in a box. We do not control the transmitter, and
we do not know its power or its antenna pattern. The one thing we can measure
reliably is the direction its wave comes from, because that direction sets the
times at which the wave reaches each element of an array.

A direction measured from one place is a **bearing**. A bearing alone says
which way to look but not how far. A radar gets range from the delay of its own
echo, but a direction finder only listens, so there is no delay to measure.
The received power does not give range either, since it depends on the
transmitter's power and pattern, which are unknown. Distance comes instead from
geometry: two bearings taken from two known positions cross at the
transmitter. The first half of this lesson measures a bearing; the second half
turns bearings into a position.
::::

::::{frame} The Arrival Ramp
:::{present}
$$\begin{aligned}
\Delta\phi_s &= kd\sin\theta_s \\
\phi_n &= n\ kd\sin\theta_s
\end{aligned}$$

- A wave from $\theta_s$ reaches element $n$ with phase $n\ kd\sin\theta_s$ relative to element 0.
- The bearing is in that ramp: $\sin\theta_s = \Delta\phi_s/kd$.
- The PHASER sums the eight elements, so we cannot read the ramp directly.
:::
:::{present}
<img src="../../viz/img/L18-path-difference.svg"
     alt="A plane wave arriving 30 degrees off broadside reaches element 2 first; the extra path to element 1 is half the spacing d"
     style="max-width: 560px; width: 100%; display: block; margin: 0 auto;">
:::

L18 started from this picture. A plane wave arriving from $\theta_s$, measured
from broadside, travels an extra $d\sin\theta_s$ to reach each successive
element, so neighboring elements see the wave with a phase difference of
$kd\sin\theta_s$, and element $n$ sees it $n\ kd\sin\theta_s$ ahead of element 0.
In L18 we chose the steer angle and computed the ramp to command. Here the
source chooses the ramp, and the source's direction is the unknown.

If we could measure the phase on each element, the bearing would follow from
L18's inverse problem: difference neighboring phases, unwrap, and take

$$\sin\theta_s = \frac{\Delta\phi_s}{kd}.$$

Some direction finders work this way. They are **interferometers**: two or
more antennas, each with its own receiver, and a direct phase comparison
between them. The PHASER cannot do it with eight elements, because the two
ADAR1000s add their four elements each into one channel before anything is
digitized (L17, "The Hybrid Beamformer"). The individual element phases never
reach the computer. What reaches it is a sum, and the sum depends on the phase
we command.
::::

::::{frame} The Steered Sum
:::{present}
$$\begin{aligned}
\psi &= kd\sin\theta_s - kd\sin\theta_0 \\
&= kd\left(\sin\theta_s - \sin\theta_0\right)
\end{aligned}$$

- Steer to $\theta_0$: each delay takes away $n\ kd\sin\theta_0$.
- The sum is L16's $\vert AF_N(\psi)\vert$, largest at $\psi = 0$.
- It peaks at $\theta_0 = \theta_s$, so the GUI's **Angle** at the peak is the bearing.
:::
:::{present}
<img src="../../viz/img/L19-sweep.svg"
     alt="The sum of the eight elements against steer angle for a source at 30 degrees: a main lobe peaking at 30 degrees, sidelobes about 13 dB down, dots at every steer angle the sweep sets"
     style="max-width: 560px; width: 100%; display: block; margin: 0 auto;">
:::

Steer the array to $\theta_0$ and each element's phase shifter delays its
signal by $n\ kd\sin\theta_0$. The arriving wave put a lead of
$n\ kd\sin\theta_s$ on element $n$, so what is left on element $n$ after the
delay is $n\psi$, with

$$\psi = kd\left(\sin\theta_s - \sin\theta_0\right).$$

The eight signals then add to $\vert AF_N(\psi)\vert$, the array factor from L16
with $\psi$ in place of its argument. It is largest, $1$ after normalizing, at
$\psi = 0$, where the commanded delays exactly cancel the arrival lead and all
eight signals add in phase. Any other steer angle leaves a residual ramp, and
the sum falls off along the main lobe, through its nulls, and over the
sidelobes.

The **beam sweep** steps $\theta_0$ across the field of view and records the
sum at each step. The figure shows what it records for a source at $30^\circ$:
the curve is the array pattern, centered on the source. This is the same
function the L18 Lab measured, read the other way, and the curve L16 drew with
the grid and the noise floor in "The Measured Sweep". There the source sat still
and the curve showed where the beam pointed; here the beam moves and the peak
shows where the source is.
::::

::::{frame} Accuracy and Resolution
:::{present}
- The main lobe is $12.9^\circ$ wide, but the sweep locates its peak far more finely.
- Noise moves the peak about $0.3^\circ$ at $30\ \text{dB}$ SNR.
- Two sources closer than about $15^\circ$ merge into one lobe.
:::
:::{present}
<img src="../../viz/img/L19-resolution.svg"
     alt="The sweep for two equal sources: 20 degrees apart it shows two peaks with a dip between them; 8 degrees apart the two lobes merge into one peak midway between the sources"
     style="max-width: 560px; width: 100%; display: block; margin: 0 auto;">
:::

At $10.525\ \text{GHz}$, $\lambda = 28.5\ \text{mm}$ and the array's half-power
beamwidth at broadside is

$$\begin{aligned}
\theta_\text{HP} &= 0.886\ \frac{\lambda}{Nd} = 0.886\ \frac{28.5}{112} \\
&= 0.225\ \text{rad} = 12.9^\circ.
\end{aligned}$$

It is tempting to conclude that a bearing is only good to about $13^\circ$, but
the beamwidth limits something else. Finding the peak of one smooth lobe is a
location estimate, and how much noise jitters the curve sets its precision, not
how wide the curve is. The standard estimate for a beam that scans across a source is

$$\sigma_\text{noise} \approx \frac{\theta_\text{HP}}{k\sqrt{2\ \text{SNR}}}.$$

The lobe's slope sets it. Noise adds a random voltage to every sample of the
sweep, about $1/\sqrt{2\ \text{SNR}}$ of the peak voltage, and the slope of the
lobe turns that voltage error into an angle error:

$$\delta\theta = \frac{\delta v}{dv/d\theta}.$$

The constant $k$ is that slope in units of $1/\theta_\text{HP}$. Textbook
trackers quote $k \approx 1.6$; the course array's lobe, normalized to 1 at its
peak, has a slope of $1.05/\theta_\text{HP}$ at its half-power points. With the
array's own slope, an SNR of $30\ \text{dB}$ (a factor of 1000) gives

$$\sigma_\text{noise} \approx \frac{12.9^\circ}{1.05\sqrt{2000}} = 0.3^\circ,$$

and the textbook constant gives $0.2^\circ$. Either way the noise term is a
fraction of the $1.05^\circ$ grid step at $30^\circ$ (next frame). An HB100
two meters away is tens of decibels above the noise, so noise is not what
limits the bearing.

The beamwidth sets **resolution**: the ability to tell two sources apart. Two
sources closer than about one beamwidth produce lobes that overlap into a
single peak somewhere between them, and the sweep reports one wrong bearing
instead of two right ones. The figure shows both cases for two equal sources:
$20^\circ$ apart the sweep has two peaks with a dip between them, and
$8^\circ$ apart it has one peak midway between the sources. For the course array the first null sits
$\lambda/Nd = 0.254$ away in $\sin\theta$, $14.7^\circ$ at broadside, which is
the usual measure of the separation two sources need. Only one HB100 is on
during the fox hunt, so the sweep sees one source.
::::

::::{frame} The Sweep Grid
:::{present}
$$\begin{aligned}
\delta(\sin\theta) &= \frac{2.8125^\circ}{176.8^\circ} = 0.0159 \\
\delta\theta &= \frac{0.0159}{\cos\theta}
\end{aligned}$$

- One step is $0.91^\circ$ at broadside, $1.05^\circ$ at $30^\circ$, $1.29^\circ$ at $45^\circ$.
- The Angle readout is off by up to half a step: $0.53^\circ$ at $30^\circ$.
:::
:::{present}
<img src="../../viz/img/L19-sweep-grid.svg"
     alt="The sweep near its peak for a source at 30 degrees: the dots, one grid step of 1.05 degrees apart, peak at 29.5 degrees, the nearest steer angle to the source"
     style="max-width: 560px; width: 100%; display: block; margin: 0 auto;">
:::

The sweep cannot set any steer angle it likes. The ADAR1000's phase shifters
have 7 bits, so the progressive phase moves in whole steps of
$360^\circ/128 = 2.8125^\circ$ (L18, "Phase-Shifter Resolution"). At the HB100's
frequency, $kd = 176.8^\circ$, so one step of progressive phase moves the beam
by a fixed $0.0159$ in $\sin\theta$. The same step in $\sin\theta$ is a larger step
in angle away from broadside, by the factor $1/\cos\theta$ in the slide's
second line, the same stretching that broadens the steered beam in L18.

The Angle readout is the steer angle of the largest sample, so it can only land on
the grid. Unless the source happens to sit on a grid point, the reported angle
is the nearest one, off by up to half a step. In the figure the source is at
$30.0^\circ$ and Angle reads $29.5^\circ$. This is one reason to prefer a source within about $\pm 30^\circ$ of
broadside: the grid step and the beamwidth grow as $1/\cos\theta$, and the gain
falls as $\cos\theta$ (L18, "Scan Loss"). At $45^\circ$ the step is
$1.29^\circ$ and the beam is about $18^\circ$ wide, and $45^\circ$ is where the
PHASER starts to lose tracking.
::::

::::{frame} The Cone Angle
:::{present}
$$\sin\theta_\text{meas} = \hat{\mathbf u}\cdot\hat{\mathbf x} = \sin(\text{az})\cos(\text{el})$$

- The ramp sees only the part of the arrival direction $\hat{\mathbf u}$ along the element row $\hat{\mathbf x}$.
- A source below the array shortens that part by $\cos(\text{el})$.
- Kit $0.9\ \text{m}$ above a box $1.5\ \text{m}$ out: $31^\circ$ down, and $30^\circ$ reads $25.4^\circ$.
:::
:::{present}
<img src="../../viz/img/L19-cone.svg"
     alt="Side view: a level source and one 31 degrees below the array, which reaches out only 0.86 horizontally. Top view: the box is at 30 degrees on the floor plan, but its horizontal projection is shorter, 0.86 long, so its part along the array is 0.429 instead of 0.500, the same as a level source at 25.4 degrees, which is what the kit reads"
     style="max-width: 560px; width: 100%; display: block; margin: 0 auto;">
:::

The phase ramp depends only on the extra path between neighboring elements,
and that path is $d$ times the component of the arrival direction along the
line of elements. Put $\hat{\mathbf x}$ along the element row, $\hat{\mathbf y}$
along broadside, and $\hat{\mathbf z}$ up. A unit vector $\hat{\mathbf u}$
toward a source at azimuth az, measured from broadside in the horizontal plane,
and elevation el has a horizontal part of length $\cos(\text{el})$, the
adjacent side of the elevation angle, and a vertical part $\sin(\text{el})$.
The horizontal part splits into $\cos(\text{el})\sin(\text{az})$ along the row
and $\cos(\text{el})\cos(\text{az})$ along broadside. In L18 the source was in
the horizontal plane and the component along the row was $\sin\theta_s$; here
it is

$$\sin\theta_\text{meas} = \hat{\mathbf u}\cdot\hat{\mathbf x} = \sin(\text{az})\cos(\text{el}).$$

That is where the cosine comes from: tipping the arrival direction out of the
horizontal plane shortens its projection onto the row. Every direction on a
cone around the row has the same projection, and so the same reading, which is
why a line array measures a cone angle and not a floor-plan azimuth.

When the source is at the array's height, el is zero and the two angles agree.
Below it, the reading is pulled toward broadside, and at classroom distances
the pull is not small. The figure shows it in two flat views. A kit on a table
$0.9\ \text{m}$ (3 ft) above a box on the floor $1.5\ \text{m}$ (5 ft) out sees
the box $31.0^\circ$ down, so the arrival direction reaches out only
$\cos 31^\circ = 0.86$ of the way horizontally (side view). On the floor plan
the box is still $30^\circ$ off broadside, but the **horizontal projection**
of its direction, the unit arrow toward the box with its vertical part dropped,
$(\sin\text{az}\cos\text{el},\ \cos\text{az}\cos\text{el},\ 0)$, is only
$\cos 31^\circ = 0.86$ long. Its part along the row is
$0.86 \times 0.500 = 0.429$ instead of $0.500$ (top view). The array cannot
tell that shortened projection from a level source at the angle whose part along the row is also $0.429$,
$\arcsin 0.429 = 25.4^\circ$, the dashed line in the top view, and so it
reports $25.4^\circ$: a $4.6^\circ$ error, three times the whole bearing
budget. The cosine scales the sine of the angle, not the angle itself:
$30^\circ \times \cos 31^\circ = 25.7^\circ$ comes out close only because
$\sin\theta \approx \theta$ for small angles, and the gap grows off broadside.
At $45^\circ$ it reads $37.3^\circ$. At $3.0\ \text{m}$ (10 ft) out the box is
$16.7^\circ$ down and $30^\circ$ reads $28.6^\circ$. The error is zero at
broadside, grows off it, and always pulls toward broadside. On a firing line
that shows up mostly as depth: five stations $0.9\ \text{m}$ above a box at
$(0.25,\ 1.5)\ \text{m}$ put the uncorrected fix $0.25\ \text{m}$ too far
downrange.

Two things remove it. Putting the kits at the boxes' height makes el zero.
When that is not possible, undo it. With the height difference $\Delta h$
known and a station's horizontal range $r$ to the fix,
$\text{el} = \arctan(\Delta h/r)$, and each reading converts back to a
floor-plan angle with

$$\sin(\text{az}) = \frac{\sin\theta_\text{meas}}{\cos(\text{el})}.$$

The range comes from a first, uncorrected fix: correct each reading, solve
again, and repeat once. In the example above one pass brings the fix within
$0.04\ \text{m}$ of the box and a second within $0.01\ \text{m}$.

Aiming the board does not help. Tipping it up or down toward the boxes turns
it about the row and leaves the reading alone, because the cone is centered on
the row. Raising one end of the row tilts the cone and adds the same kind of
error, so keep the row level.

The cone has a back half as well, a source behind the array at the mirror
angle, but the PHASER's patches sit over a ground plane and receive almost
nothing from behind, so a bearing is always in front of the array.
::::

::::{frame} Reflections
:::{present}
- A reflection adds a second, weaker lobe.
- Within $15^\circ$ of the source it pulls the peak: $0.6^\circ$ at $-20\ \text{dB}$, $2.0^\circ$ at $-10\ \text{dB}$, $3.2^\circ$ at $-6\ \text{dB}$.
- A bearing far off the rest is usually a reflection: clear the path.
:::
:::{present}
<img src="../../viz/img/L19-reflection.svg"
     alt="The direct lobe at broadside, a reflection lobe 10 dB down near 12 degrees, and their sum, whose peak has moved 2.0 degrees toward the reflection"
     style="max-width: 560px; width: 100%; display: block; margin: 0 auto;">
:::

A whiteboard, a metal cabinet, or a person near the line of sight sends a
second copy of the signal toward the array from a different direction. The
array adds both, so the sweep is the sum of two patterns, one centered on the
source and a weaker one centered on the reflector, with a relative phase set by
the extra path the reflection travels. When the two directions are within
about a beamwidth of each other, the lobes merge and the peak moves toward the
reflection. The worst case over every phase, for a reflection $5^\circ$ to
$15^\circ$ from the direct path, is a shift of $0.6^\circ$ for a reflection
$20\ \text{dB}$ down, $2.0^\circ$ at $10\ \text{dB}$ down, and $3.2^\circ$ at
$6\ \text{dB}$ down. The figure shows the $-10\ \text{dB}$ case at its worst,
a reflection about $12^\circ$ from the direct path.

A reflection more than about $20^\circ$ away forms its own lobe and moves the
main peak much less. It takes over the bearing if someone stands between the kit
and the source: the direct lobe drops, the reflection's lobe is now the
largest, and Angle reports the direction of the whiteboard. A bearing several
degrees off from the others most often comes from a reflection that has taken
over the peak.
::::

::::{frame} From Array Angle to Room Bearing
:::{present}
$$\beta = h + \theta_\text{est}$$

- $\theta_\text{est}$: Angle, from the kit's broadside.
- $h$: the heading of broadside from a fixed room axis.
- $\beta$: the room bearing. All three counterclockwise, seen from above.
:::
:::{present}
<img src="../../viz/img/L19-room-bearing.svg"
     alt="Top view: a kit whose broadside points at heading h from the room axis; the bearing to the source is theta_est further counterclockwise, so the room bearing beta is h plus theta_est"
     style="max-width: 380px; width: 75%; display: block; margin: 0 auto;">
:::

The Angle readout measures the angle from the array's broadside, which is wherever
the kit happens to face. To draw the bearing on a floor plan we need it in the room's
frame. Measure angles counterclockwise from a fixed room axis, seen from above.
If broadside points along heading $h$ and positive Angle is the
counterclockwise side, the room bearing is

$$\beta = h + \theta_\text{est}.$$

Which physical side of the kit is positive depends on which way the kit faces; the
L18 Lab found it by moving the source toward element E8. Get it wrong and a
source at $30^\circ$ lands on the plan at $-30^\circ$, a $60^\circ$ error, so
check it with one shot at a known position before trusting any bearing.
::::

::::{frame} The Bearing Error Budget
:::{present}
$$\begin{aligned}
\sigma_\beta &= \sqrt{\sigma_h^2 + \sigma_\theta^2} \\
&= \sqrt{1.0^2 + 0.53^2 + 1.0^2 + 0.3^2} = 1.5^\circ
\end{aligned}$$

| Error | Enters through | Source | $\sigma$ |
| :-- | :-- | :-- | :-- |
| heading | $h$ | array edge on a taped line | $1.0^\circ$ |
| grid | $\theta_\text{est}$ | half a step at $30^\circ$ | $0.53^\circ$ |
| multipath | $\theta_\text{est}$ | a weak reflection | $1.0^\circ$ |
| noise | $\theta_\text{est}$ | $30\ \text{dB}$ SNR | $0.3^\circ$ |

- In meters: $\delta_\perp = R\tan\sigma_\beta$, $0.05\ \text{m}$ at $2\ \text{m}$.
:::

Each term of $\beta = h + \theta_\text{est}$ carries an error, and the error in
$\beta$ is the two combined. The table is the budget for one bearing: one row
per independent error, the term of the equation it enters through, where it
comes from, and its one-sigma size. The heading error adds directly to the bearing error, and in the room it is the
largest term. Laying the array's edge along a taped line holds $h$ to about
$1^\circ$. The grid term is the worst case, half a step, rather than the
$0.30^\circ$ standard deviation of an error spread evenly over a $1.05^\circ$
step, which keeps the budget conservative. The grid, multipath, and noise
terms make up $\sigma_\theta$, the error in the Angle readout itself, and all
four are independent, so they add as a root sum of squares, the chain on the
slide. Setting the heading by eye, about $3^\circ$, raises the total to $3.2^\circ$.

A bearing error is an angle, but the fix is a position, so what matters is how
far the error moves the line where the source is. A line rotated by
$\sigma_\beta$ about the kit moves sideways, at range $R$, by the
**cross-range error**

$$\delta_\perp = R\tan\sigma_\beta.$$

At the budget's $1.5^\circ$ that is $0.05\ \text{m}$ at $2\ \text{m}$; at
$\sigma_\beta = 2^\circ$, a little worse, it is $0.03\ \text{m}$ at
$1\ \text{m}$, $0.07\ \text{m}$ at $2\ \text{m}$, and $0.14\ \text{m}$ at
$4\ \text{m}$. The error grows in proportion to range, which is why a closer
station gives a tighter line. It is also all in one direction. A bearing says
nothing about how far along the line the source is, so its uncertainty is a
narrow strip, $2\delta_\perp$ wide at one standard deviation and unbounded
along its length. A second bearing's strip is what limits the fix along the
first one, and how well it does that depends on the angle between them, "The
Crossing Angle" below.
::::

::::{frame} A Two-Bearing Fix
:::{present}
- Origin mid-tape, $x$ along it, $y$ downrange; $\theta_i$ is positive toward $+x$
- The fox is on both lines: set their $x$ values equal, solve for $y$.

$$\begin{aligned}
\tan\theta_i &= \frac{x - x_i}{y} \\
x &= x_i + y\tan\theta_i \\
x_A + y\tan\theta_A &= x_B + y\tan\theta_B \\
y &= \frac{x_B - x_A}{\tan\theta_A - \tan\theta_B}
\end{aligned}$$
:::
:::{present}
<img src="../../viz/img/L19-two-bearings.svg"
     alt="A firing line with station marks every half meter; stations A at x = -1 m and B at x = +1 m face straight downrange, and their bearing lines at +36.6 and -22.4 degrees cross at the fix, inside the box at (0.25, 1.75) m"
     style="max-width: 300px; width: 58%; display: block; margin: 0 auto;">
:::

On the L19 Lab's firing range every station faces straight downrange, so all
the stations share one heading and the bearing line takes a simpler form. Put the
origin at the middle of the tape, the station 0 mark, with $x$ along the tape
and $y$ downrange, and take Angle $\theta$ positive toward the $+x$ end of the
tape. A station at $x_i$ sits at $(x_i,\ 0)$ and faces $+y$. A source at
$(x,\ y)$ is $y$ downrange of it and $x - x_i$ across, the two legs of the
dotted right triangle in the figure, and $\theta_i$ is the angle at the
station between downrange and the source, so

$$\tan\theta_i = \frac{x - x_i}{y}.$$

Solving for $x$, a reading $\theta_i$ at station $x_i$ puts the source on the
line

$$x = x_i + y\tan\theta_i.$$

Every point on that line fits the reading, so one bearing is one equation in
the two unknowns $x$ and $y$: it says which way to look, but not how far. A
second bearing from another station is a second equation, and the two lines
cross at the source.

:::{admonition} Worked example — the crossing of two bearings
:class: tip
Station A at $x_A = -1.0\ \text{m}$ reads Angle $36.6^\circ$, and station B at
$x_B = +1.0\ \text{m}$ reads $-22.4^\circ$. Both lines pass through the
source, so setting their $x$ equal, $x_A + y\tan\theta_A = x_B + y\tan\theta_B$,
and solving for $y$ gives

$$\begin{aligned}
y &= \frac{x_B - x_A}{\tan\theta_A - \tan\theta_B} \\
&= \frac{2.0}{0.743 + 0.412} = 1.73\ \text{m},
\end{aligned}$$

and either line gives $x$:

$$\begin{aligned}
x &= x_A + y\tan\theta_A \\
&= -1.0 + 1.73 \times 0.743 \\
&= 0.29\ \text{m}.
\end{aligned}$$

The box was at $(0.25,\ 1.75)\ \text{m}$, where the true angles are
$35.5^\circ$ and $-23.2^\circ$. The readings were $1.1^\circ$ and $0.8^\circ$
toward $+x$, inside the $1.5^\circ$ budget, and the fix lands $0.04\ \text{m}$
from the box. The two lines cross at $\gamma = \theta_A - \theta_B = 59.0^\circ$.
:::
::::

::::{frame} Distance From a Line
:::{present}
$$\begin{aligned}
\hat{\mathbf u}_i &= (\sin\theta_i,\ \cos\theta_i) \\
\hat{\mathbf n}_i &= (\cos\theta_i,\ -\sin\theta_i) \\
e_i &= \hat{\mathbf n}_i\cdot(\mathbf x - \mathbf p_i)
\end{aligned}$$

- $\mathbf p_i = (x_i,\ 0)$: station $i$ on the tape. $\hat{\mathbf u}_i$: along its bearing. $\hat{\mathbf n}_i$: across it.
- $e_i$: how far a point $\mathbf x$ sits off line $i$, in meters; zero on the line.
:::
:::{present}
<img src="../../viz/img/L19-miss.svg"
     alt="A station at p_i on the tape with its bearing line at theta_i from downrange; the unit vector u points along the line and n perpendicular to it; a point x off the line, the vector x minus p_i from the station to it, and the point's perpendicular miss e_i from the line"
     style="max-width: 360px; width: 66%; display: block; margin: 0 auto;">
:::

Two bearings cross exactly, but three or more never quite meet: every bearing
carries some error, so three lines form a small triangle. To pick the point
that comes closest to all of them, we first need a way to say how far a point
is from one line. Vectors make that one line of algebra.

Start from the previous frame's triangle. From station $i$ at
$\mathbf p_i = (x_i,\ 0)$ to the source, the legs are $x - x_i$ across and
$y$ downrange, and dividing each by the hypotenuse gives $\sin\theta_i$ and
$\cos\theta_i$. So the unit vector that points from the station along the
bearing is

$$\hat{\mathbf u}_i = (\sin\theta_i,\ \cos\theta_i),$$

and turning it $90^\circ$ clockwise gives the unit vector across the line,
toward $+x$,

$$\hat{\mathbf n}_i = (\cos\theta_i,\ -\sin\theta_i).$$

Now take any point $\mathbf x = (x,\ y)$ and the arrow
$\mathbf x - \mathbf p_i$ from the station to it. That arrow splits into a part
along $\hat{\mathbf u}_i$, how far down the line the point is, and a part along
$\hat{\mathbf n}_i$, how far off the line it is. The dot product with a unit
vector picks out the part along it, so the point's perpendicular miss is

$$\begin{aligned}
e_i &= \hat{\mathbf n}_i\cdot(\mathbf x - \mathbf p_i) \\
&= (x - x_i)\cos\theta_i - y\sin\theta_i,
\end{aligned}$$

the green segment in the figure, in meters and signed: positive on the $+x$
side of the line. Setting $e_i = 0$ gives $\tan\theta_i = (x - x_i)/y$, the
previous frame's line, so the bearing line is exactly the set of points with
no miss.

Another way to see the same arithmetic is as a change of coordinates.
Subtracting $\mathbf p_i$ moves the origin to station $i$, and dotting with
$\hat{\mathbf u}_i$ and $\hat{\mathbf n}_i$ reads the point's coordinates on
axes turned by $\theta_i$, one along the bearing and one across it. In that
frame $\hat{\mathbf u}_i\cdot(\mathbf x - \mathbf p_i)$ is how far down range
the point is and $e_i$ is its **cross-range** coordinate, the same direction
the cross-range error of "The Bearing Error Budget" measures. The bearing line is where that cross-range
coordinate is zero, and least squares looks for the one point whose
cross-range coordinate is nearly zero in every station's frame at once.
::::

::::{frame} Many Bearings: Least Squares
:::{present}
- Three bearing lines never meet exactly: errors leave a small triangle.
- The fix makes $e_1^2 + e_2^2 + e_3^2$ smallest.
- Each line pulls the fix toward itself, harder the more it misses. At the fix the pulls balance.
- In Python: `numpy.linalg.lstsq`.
:::
:::{present}
<img src="../../viz/img/L19-pulls.svg"
     alt="Three stations on the firing line whose bearings nearly cross; magnified, the three lines form a small triangle, and arrows e1, e2, e3 run from the least-squares fix to each line"
     style="max-width: 560px; width: 100%; display: block; margin: 0 auto;">
:::

With two bearings the crossing is exact. A third bearing adds a third line,
and because every bearing carries some error, the three lines form a small
triangle rather than meeting at a point. The figure magnifies it: no point
lies on all three lines, so no point has all three misses $e_i$ of the
previous frame equal to zero. The fix has to be a compromise.

The usual compromise is **least squares**: choose the point that makes the
sum of the squared misses, $e_1^2 + e_2^2 + e_3^2$, as small as it can be.
Squaring keeps a miss on either side of a line from canceling one on the other
side, gives one smooth bowl with a single bottom, and counts a large miss
more heavily than two small ones, which suits bearings whose errors are
mostly small.

There is a physical picture of where the bottom of that bowl is. Tie the
candidate point to each line with a spring that pulls it straight toward the
line, along $\hat{\mathbf n}_i$, with a force proportional to the miss $e_i$.
The point comes to rest where the pulls balance,

$$\sum_i e_i\ \hat{\mathbf n}_i = 0,$$

and that resting point is exactly the least-squares fix: the arrows in the
figure are those pulls, and they add to zero. The picture also says what a
bad bearing does. A reflection that bends one line pulls the fix toward it,
and because the other lines pull back, that line ends up with the largest
miss, which is how "Residuals and Outliers" below finds it.

Nobody solves this by hand in the fox hunt. The L19 Lab's pre-lab has you
write it as a short Python function around `numpy.linalg.lstsq` and test it
on a supplied set of bearings; "The General Form" next shows what that call
computes, and the two frames after it work an example.

Unweighted least squares treats every line as equally reliable. A bearing from
a kit far from the source is less reliable in meters, as the cross-range error
showed, so if the ranges differ a lot, weighting each term by $1/r_i^2$ gives
the better fix. In the fox hunt every bearing that counts is within about
$\pm 45^\circ$ of broadside, so the ranges from the stations to one box differ
by at most a factor of $\sqrt{2}$, the weights by a factor of 2, and the
unweighted form is close enough.
::::

::::{frame} The General Form
:::{present}
$$x\cos\theta_i - y\sin\theta_i = x_i\cos\theta_i$$

$$\begin{aligned}
\mathbf A &= \begin{bmatrix} \cos\theta_1 & -\sin\theta_1 \\ \cos\theta_2 & -\sin\theta_2 \\ \cos\theta_3 & -\sin\theta_3 \end{bmatrix} \\
\mathbf b &= \begin{bmatrix} x_1\cos\theta_1 \\ x_2\cos\theta_2 \\ x_3\cos\theta_3 \end{bmatrix}
\end{aligned}$$
:::
:::{present}
- $\mathbf x = (x,\ y)$: the fox, unknown.
- Station $i$: tape mark $x_i$, Angle readout $\theta_i$ (positive toward $+x$).
- Row $i$ of $\mathbf A\mathbf x - \mathbf b$ is the miss $e_i$. The fix minimizes $\sum e_i^2$: $\mathbf A^{\mathsf T}\mathbf A\ \mathbf x = \mathbf A^{\mathsf T}\mathbf b$.
:::

Each station's bearing line is one linear equation in the unknown point. Its
miss from "Distance From a Line",
$e_i = (x - x_i)\cos\theta_i - y\sin\theta_i$, is zero on the line, and
moving the known part to the right-hand side writes the line as

$$\cos\theta_i\ x - \sin\theta_i\ y = x_i\cos\theta_i.$$

Write one such equation per station, one under the other, as on the slide.
In matrix form this is $\mathbf A\mathbf x = \mathbf b$:

$$\underbrace{\begin{bmatrix} \cos\theta_1 & -\sin\theta_1 \\ \cos\theta_2 & -\sin\theta_2 \\ \cos\theta_3 & -\sin\theta_3 \end{bmatrix}}_{\mathbf A}
\underbrace{\begin{bmatrix} x \\ y \end{bmatrix}}_{\mathbf x} =
\underbrace{\begin{bmatrix} x_1\cos\theta_1 \\ x_2\cos\theta_2 \\ x_3\cos\theta_3 \end{bmatrix}}_{\mathbf b}.$$

$\mathbf A$ holds the coefficients of $x$ and $y$, one row per station; each
row is that station's $\hat{\mathbf n}_i$. $\mathbf b$ holds the right-hand
sides. With $N$ stations $\mathbf A$ is $N\times 2$, and
$\mathbf A\mathbf x - \mathbf b$ is the list of misses
$(e_1,\ e_2,\ \dots,\ e_N)$.

With two stations the two equations have one exact solution, the crossing of
"A Two-Bearing Fix". With three or more there are more equations than
unknowns, and no point satisfies them all. The least-squares point satisfies
two combinations of them instead, the **normal equations**,

$$\mathbf A^{\mathsf T}\mathbf A\ \mathbf x = \mathbf A^{\mathsf T}\mathbf b.$$

Multiplying by $\mathbf A^{\mathsf T}$ adds up the $N$ equations twice, once
weighted by each station's $\cos\theta_i$ and once by its $-\sin\theta_i$,
leaving two equations in two unknowns, which always have one answer unless the
lines are all parallel. They are the balance of pulls in another form:
$\mathbf A^{\mathsf T}(\mathbf A\mathbf x - \mathbf b) = \sum_i e_i\ \hat{\mathbf n}_i = 0$.
They are also what setting the derivatives of $\sum_i e_i^2$ with respect to
$x$ and $y$ to zero gives.

`numpy.linalg.lstsq(A, b)` solves the normal equations in one line, and the
next two frames build $\mathbf A$ and $\mathbf b$ for three real readings and
solve them by hand.
::::

::::{frame} Three Bearings: Build A and b
:::{present}
| $\theta_i$ | $34.6^\circ$ | $8.8^\circ$ | $-17.7^\circ$ |
| :-- | :-- | :-- | :-- |
| $x_i$ | $-0.75\ \text{m}$ | $0$ | $+0.75\ \text{m}$ |

$$\begin{aligned}
\mathbf A &= \begin{bmatrix} 0.823 & -0.568 \\ 0.988 & -0.153 \\ 0.953 & 0.304 \end{bmatrix} \\
\mathbf b &= (-0.617,\ 0,\ 0.714)^{\mathsf T}
\end{aligned}$$
:::

Stations at $x_i = -0.75$, $0$, and $+0.75\ \text{m}$ on the tape read Angle
$34.6^\circ$, $8.8^\circ$, and $-17.7^\circ$; each $\theta_i$ is that
station's Angle readout, measured from broadside and positive toward the $+x$
end of the tape, not a room bearing. Building the system takes three numbers
per station. Its row of $\mathbf A$ is $\cos\theta_i$ and $-\sin\theta_i$, the
coefficients of $x$ and $y$ in its line equation, and its entry of
$\mathbf b$ is $x_i\cos\theta_i$; station 1, for example, gives
$\cos 34.6^\circ = 0.823$, $-\sin 34.6^\circ = -0.568$, and
$-0.75 \times 0.823 = -0.617$. Stack the three rows and the three entries and
the system is the one on the slide: three equations, two unknowns.
::::

::::{frame} Three Bearings: The Fix
:::{present}
- Fix $(0.26,\ 1.49)\ \text{m}$; box at $(0.25,\ 1.50)\ \text{m}$.
- The arrows are the residuals, $\mathbf e = \mathbf A\mathbf x - \mathbf b$: $-1.6$, $2.8$, $-1.5\ \text{cm}$.
- All under $R_i\tan\sigma_\beta \approx 4\ \text{cm}$: three good bearings. One several times larger is an outlier.
- Python: `numpy.linalg.lstsq(A, b)`.
:::
:::{present}
<img src="../../viz/img/L19-three-fix.svg"
     alt="The three bearings of the worked example; magnified near the fix, arrows e1, e2, e3 run from the fix to each line, and the box sits 1 centimeter away"
     style="max-width: 560px; width: 100%; display: block; margin: 0 auto;">
:::

To check by hand: $\mathbf A^{\mathsf T}\mathbf A$ sums $\cos^2\theta_i$,
$-\cos\theta_i\sin\theta_i$, and $\sin^2\theta_i$ over the three stations, and
$\mathbf A^{\mathsf T}\mathbf b$ sums $x_i\cos^2\theta_i$ and
$-x_i\cos\theta_i\sin\theta_i$; for the first entry,
$0.823^2 + 0.988^2 + 0.953^2 = 2.562$. The normal equations are

$$\begin{bmatrix} 2.562 & -0.329 \\ -0.329 & 0.438 \end{bmatrix}
\begin{bmatrix} x \\ y \end{bmatrix} =
\begin{bmatrix} 0.173 \\ 0.568 \end{bmatrix}.$$

The determinant is $2.562 \times 0.438 - 0.329^2 = 1.014$, and the
$2\times 2$ inverse gives

$$\begin{aligned}
x &= \frac{0.438 \times 0.173 + 0.329 \times 0.568}{1.014} = 0.26\ \text{m} \\
y &= \frac{2.562 \times 0.568 + 0.329 \times 0.173}{1.014} = 1.49\ \text{m}.
\end{aligned}$$

The box was at $(0.25,\ 1.50)\ \text{m}$, so the fix lands $0.01\ \text{m}$
from it. The misses, $\mathbf A\mathbf x - \mathbf b$, are $-0.016$, $0.028$,
and $-0.015\ \text{m}$, all under each station's own $R_i\tan\sigma_\beta$ of
about $0.04\ \text{m}$ at $1.5^\circ$: three good bearings (the check in
"Residuals and Outliers" below). In Python the whole frame is two lines:
build `A` and `b` from the readings as on the previous frame, then
`numpy.linalg.lstsq(A, b)`.
::::

::::{frame} The Crossing Angle
:class: viz-frame

:::{present}
<iframe src="../../viz/df-fix.html"
        width="100%" height="464"
        style="border: 1px solid #cddce9; border-radius: 6px;"
        loading="lazy"
        title="A direction-finding fix: drag two to four kits around a keep-out circle, or along a firing line, with a hidden source, and watch the least-squares fix, its error ellipse, and each bearing's residual">
</iframe>

- A shallow crossing stretches the error region as $1/\sin\gamma$: $0.20\ \text{m}$ at $90^\circ$, $0.76\ \text{m}$ at $15^\circ$.
- A reflection moves the fix, and only a third bearing shows it.
:::

Where the two strips overlap is where the source can be. When the lines cross
at $90^\circ$, each strip limits the other's long direction, and the overlap is
a small square; its error ellipse is a circle of radius $\delta_\perp$ in both
directions. When they cross at a shallow angle $\gamma$, the strips run almost
parallel, and the overlap stretches into a long diamond along the bisector of
the two lines.

The least-squares fix puts a number on this. Divide each row of $\mathbf A$,
the unit vector $\hat{\mathbf n}_i$ across line $i$, by that bearing's
$\delta_\perp$, and the matrix

$$\mathbf M = \sum_i \frac{\hat{\mathbf n}_i\hat{\mathbf n}_i^{\mathsf T}}{\delta_{\perp,i}^2}$$

describes the error region. The eigenvectors of $\mathbf M^{-1}$ point along
the axes of the one-sigma error ellipse, its eigenvalues are the squared
semi-axes, and the RMS error of the fix is the square root of their sum. Two
unit rows at an angle $\gamma$, which is also the angle between the lines, give
$\sum\hat{\mathbf n}_i\hat{\mathbf n}_i^{\mathsf T} = \mathbf A^{\mathsf T}\mathbf A$ a trace of 2 and a
determinant of $\sin^2\gamma$, so its eigenvalues are $1 + \cos\gamma$ and
$1 - \cos\gamma$. For two bearings with the same $\delta_\perp$,

$$\begin{aligned}
\sigma_\text{fix} &= \delta_\perp\sqrt{\frac{1}{1 + \cos\gamma} + \frac{1}{1 - \cos\gamma}} \\
&= \frac{\sqrt{2}\ \delta_\perp}{\sin\gamma},
\end{aligned}$$

so a $15^\circ$ crossing is almost four times worse than a $90^\circ$ one with
the same bearings.

<img src="../../viz/img/L19-crossing.svg"
     alt="Two bearing lines with their plus and minus one sigma strips and the one-sigma error ellipse: crossing at 90 degrees the ellipse is a circle, RMS 0.20 meters; crossing at 30 degrees it stretches along the bisector, RMS 0.40 meters"
     style="max-width: 480px; width: 100%; display: block; margin: 0 auto;">

| Kits $4\ \text{m}$ out, $\sigma_\beta = 2^\circ$ | RMS fix error |
| :-- | :-- |
| 2 kits, $90^\circ$ crossing | $0.20\ \text{m}$ |
| 2 kits, $30^\circ$ | $0.40\ \text{m}$ |
| 2 kits, $15^\circ$ | $0.76\ \text{m}$ |
| 3 kits over $120^\circ$ | $0.16\ \text{m}$ |

The table's rows come from the same $\mathbf M$, summed over two or three
kits. A third kit helps less by adding
a measurement than by guaranteeing that at least two of the three lines cross
steeply: three kits spread over $120^\circ$ do better than the best pair.

The widget is a room seen from above, with the keep-out circle and a source
hidden somewhere inside it. Each kit draws its measured bearing, the true
bearing plus an error drawn with the $\sigma_\beta$ you set, and a shaded
wedge of $\pm\sigma_\beta$. The cross is the least-squares fix and the
ellipse around it is its one-sigma error region. Drag the kits and watch the
ellipse: it stays round while the crossing angle $\gamma$ is near $90^\circ$
and stretches along the bisector as $\gamma$ closes. To reproduce a row of the
table, tick **reveal**, set $\sigma_\beta$ to $2^\circ$, and drag the kits
onto the $4\ \text{m}$ ring, where they snap at $5^\circ$ steps around the
source. The RMS beside the fix error is the table's number. The fix error
itself is one draw of the bearing errors; press **new bearings** a few times
and it scatters about the RMS. With the source hidden, the crossing angles and
the RMS come from the measured bearings, as they would in the room.

Tick **reflection** to bend kit A's bearing by $10^\circ$, the size of error
a reflection makes when it takes over the peak. With two kits the fix moves
about $0.7\ \text{m}$ and both residuals stay at zero, because two lines
always meet. With three, A and C both miss the fix by about twice their own
$R_i\tan\sigma_\beta$ and turn red: the residuals show that a bearing is bad,
but with three lines they rise and fall together and cannot say which. A
fourth kit separates them, and only A's residual stands out. That is the check
in "Residuals and Outliers" below.

Set **Layout** to **firing line** to see the L19 Lab's range: a $3\ \text{m}$
tape with five station marks $0.75\ \text{m}$ apart, every kit facing straight
downrange, and the source hidden in the box field $1$ to $2\ \text{m}$ out.
Kits snap to the marks. The fix-error readout now splits into depth and
cross-range. Put two kits on the inner marks, then move them to the ends: the
ellipse shortens downrange and the depth error falls as $1/B$, the result
derived in "Choosing Where to Measure" below.
::::

::::{frame} Choosing Where to Measure
:::{present}
- Use the end stations that hear the fox: depth error falls as $1/B$.
- Best within $\pm 30^\circ$ of broadside; tracking starts to fail at $\pm 45^\circ$.
- Point each array at the boxes, path clear.
- Take a third bearing as a check.
:::
:::{present}
<img src="../../viz/img/L19-depth.svg"
     alt="Two pairs of stations on a firing line and a box 2 meters downrange: neighboring stations 0.75 meters apart give an error ellipse plus or minus 0.20 meters long in depth; the end stations, 3 meters apart, plus or minus 0.08 meters"
     style="max-width: 560px; width: 100%; display: block; margin: 0 auto;">
:::

Choosing where to stand is part of the measurement, because the geometry sets
the error as much as the instrument does. On a firing line every bearing looks
downrange, so the lines cross steeply only when the stations are far apart
compared with the depth, and depth is the direction the fix measures worst.

Take two stations a baseline $B$ apart and a box midway between them at depth
$y$, a range $R$ from each. Each line moves sideways by
$\delta_\perp = R\sigma_\beta$, with $\sigma_\beta$ in radians, and the two
lines cross at $\gamma$, with

$$\sin\frac{\gamma}{2} = \frac{B/2}{R}.$$

The two lines sit symmetrically about the downrange direction, so the axes of
the error ellipse point across and down range. The eigenvalues of $\mathbf M$
are $2\cos^2(\gamma/2)/\delta_\perp^2$ across range and
$2\sin^2(\gamma/2)/\delta_\perp^2$ in depth, and the depth error is the inverse
square root of the second:

$$\begin{aligned}
\sigma_y &= \frac{\delta_\perp}{\sqrt{2}\ \sin(\gamma/2)} \\
&= \frac{\sqrt{2}\ R^2\sigma_\beta}{B}.
\end{aligned}$$

With the taped-heading budget, $\sigma_\beta = 1.5^\circ$, and the L19 Lab's
station marks $0.75\ \text{m}$ apart, the end stations, $3\ \text{m}$ apart,
fix a box $2\ \text{m}$ downrange to $0.08\ \text{m}$ in depth, stations
$1.5\ \text{m}$ apart to $0.11\ \text{m}$, and neighboring stations,
$0.75\ \text{m}$ apart, to $0.20\ \text{m}$. Across range the same pairs fix
it to $0.04$ to $0.06\ \text{m}$. The depth error grows as $R^2$ and
falls as $1/B$, so the stations farthest apart that still hear the fox give the
best fix.

Spreading the stations has a limit: a station far to one side sees the box well
off broadside. Within $\pm 30^\circ$ the grid step and the beamwidth stay near
their broadside values. At $\pm 45^\circ$ the step is $1.29^\circ$, the beam is
about $18^\circ$ wide, the gain is $1.5\ \text{dB}$ down (L18, "Scan
Loss"), and the PHASER starts to lose tracking. A station that sees a box
farther out than that gives no bearing worth using, and the HB100's own beam,
aimed only roughly at the line, may leave it too weak a tone to read anyway.

Two systematic errors from earlier in the lesson remain. The cone-angle error
pulls every bearing toward broadside when the source is above or below the
array. Put the kits at the boxes' height, or correct each reading as "The
Cone Angle" describes, and keep each element row level. A
reflector near the line of sight shifts the peak or replaces it, so keep the
path from each kit to the box field clear, people included. Finally, two bearings always cross somewhere,
right or wrong. A third bearing is the only check that the first two are
consistent.

The geometry also sets how close two boxes can be and still be told apart. A
simulation of a row of boxes, with the fix assigned to the nearest box, names
the right one 99% of the time at $0.75\ \text{m}$ spacing with two kits
$4\ \text{m}$ out crossing at $90^\circ$ and $\sigma_\beta = 2^\circ$, and 93%
of the time at $0.5\ \text{m}$. The L19 Lab's boxes sit at least
$0.75\ \text{m}$ apart for the same reason.
::::

::::{frame} Residuals and Outliers
:class: read-only

:::{present}
$$\begin{aligned}
R_i &= \sqrt{(x - x_i)^2 + y^2} \\
e_i &= \hat{\mathbf n}_i\cdot(\mathbf x - \mathbf p_i)
\end{aligned}$$

- At the fix $(x,\ y)$: $R_i$ is station $i$'s range, $e_i$ how far the fix sits off line $i$.
- $\lvert e_i\rvert > 3R_i\tan\sigma_\beta$ flags a bad bearing: retake it, or drop it and solve again.
:::
:::{present}
<img src="../../viz/img/L19-residuals.svg"
     alt="Five stations on the firing line; the middle bearing, bent 10 degrees, misses the least-squares fix by 19 centimeters, the others by 4 to 7 centimeters"
     style="max-width: 560px; width: 100%; display: block; margin: 0 auto;">
:::

Once the least-squares fix $\mathbf x = (x,\ y)$ is in hand, the
perpendicular distance from the fix to each line is that line's **residual**,
$e_i$. It is the miss of "Distance From a Line",
$(x - x_i)\cos\theta_i - y\sin\theta_i$, entry $i$ of
$\mathbf A\mathbf x - \mathbf b$, now evaluated at the answer: one line of
Python per station. On the line itself $x - x_i = y\tan\theta_i$ and $e_i$ is
zero.

To judge a residual, compare it with what that bearing's own error would
produce. $R_i$ is the distance from station $i$ to the fix, and a bearing
error of $\sigma_\beta$ moves line $i$ sideways at the fix by
$R_i\tan\sigma_\beta$, the cross-range error of "The Bearing Error Budget" above:
about $0.05\ \text{m}$ for a station $1.5\ \text{m}$ from the fox at
$\sigma_\beta = 2^\circ$. A good bearing's residual is about that size. One
more than three times that size says the bearing disagrees with the rest.

What to do with it is the procedure on the slide: solve the fix from every
bearing, compute $R_i$ and $e_i$ for each station, and flag any station whose
$\lvert e_i\rvert$ is more than $3R_i\tan\sigma_\beta$.

The usual causes are the two errors that the budget does not cover because they
are blunders rather than noise: a reflection that took over the peak, and a
heading or sign mistake that put the line on the wrong side of broadside.
Check that kit's setup and retake the bearing; if it still disagrees, drop it
and solve again with the others. Drop one at a time, the worst first, because
one bad line pulls the fix and raises every other residual a little. In the
figure the middle station's bearing is $10^\circ$ off: its
residual $e$ is $19\ \text{cm}$ against its own $R_i\tan\sigma_\beta$ of
$5\ \text{cm}$, almost four times, and the bad line pulls the other residuals
up to 4 to $7\ \text{cm}$, each under one and a half times its own. With only two bearings the residuals are always zero, because two lines
always meet exactly, so two bearings cannot check each other.

The L19 Lab adds one more check, the **Peak Gain** readout. Received power
cannot give range on its own, because the transmitter's power is unknown, but
every station hears the same transmitter, so comparing levels between stations
removes that unknown. Free-space spreading then sets the difference: a station
at range $R_2$ reads $20\log_{10}(R_2/R_1)$ dB below one at $R_1$, which is
$2.5\ \text{dB}$ for $2.0\ \text{m}$ against $1.5\ \text{m}$, and a source off
broadside reads lower by the scan loss of L18. The HB100's own pattern does not
cancel: the fox points only roughly at the line, and two stations at the same
range can differ by several decibels. Levels therefore rank the two or three
boxes the bearings already put near the fix; they do not locate the fox by
themselves.
::::

::::{frame} Summary: Measuring a Bearing
:class: read-only

| Symbol / idea | What it is | Number to remember |
| :-- | :-- | :-- |
| $\psi = kd(\sin\theta_s - \sin\theta_0)$ | residual phase step after steering to $\theta_0$ | sum peaks where $\theta_0 = \theta_s$ |
| Angle | steer angle of the largest sample in the sweep | on a grid $0.0159$ apart in $\sin\theta$ |
| $\theta_\text{HP}$ | sets resolution of two sources, not accuracy for one | $12.9^\circ$ at broadside |
| $\sin\theta_\text{meas} = \sin(\text{az})\cos(\text{el})$ | the cone angle a line array measures | $25.4^\circ$ for $30^\circ$ at $31^\circ$ down |
| $\beta = h + \theta_\text{est}$ | room bearing from heading and Angle | $\sigma_\beta \approx 1.5^\circ$ with a taped heading |
::::

::::{frame} Summary: Locating the Source
:class: read-only

| Symbol / idea | What it is | Number to remember |
| :-- | :-- | :-- |
| $x = x_i + y\tan\theta_i$ | one bearing line from station $x_i$ | one equation, two unknowns |
| $e_i = \hat{\mathbf n}_i\cdot(\mathbf x - \mathbf p_i)$ | a point's miss from line $i$; $\hat{\mathbf n}_i = (\cos\theta_i,\ -\sin\theta_i)$ | zero on the line |
| $\mathbf A^{\mathsf T}\mathbf A\ \mathbf x = \mathbf A^{\mathsf T}\mathbf b$ | least-squares fix; row $i$ of $\mathbf A$ is $\hat{\mathbf n}_i$, $b_i = x_i\cos\theta_i$ | a $2\times 2$ solve |
| $\delta_\perp = R\tan\sigma_\beta$ | cross-range error of one line | $0.14\ \text{m}$ at $4\ \text{m}$, $2^\circ$ |
| $\sigma_\text{fix} = \sqrt{2}\ \delta_\perp/\sin\gamma$ | RMS error of a two-bearing fix crossing at $\gamma$ | $0.20\ \text{m}$ at $90^\circ$, $0.76\ \text{m}$ at $15^\circ$ |
| $\sigma_y = \sqrt{2}\ R^2\sigma_\beta/B$ | depth error from two stations $B$ apart on a firing line | $0.08\ \text{m}$ at $2\ \text{m}$ deep, $B = 3\ \text{m}$ |
| residual $e_i$ | the fix's perpendicular distance from line $i$ | flags an outlier above $3R_i\tan\sigma_\beta$ |
::::

::::{frame} The L19 Lab
:class: read-only doc-links

The bench half of this lesson is the L19 Lab, the fox hunt: find the one live
HB100 among numbered boxes from bearings your team takes at stations along a
firing line.

- <a class="doc-link" href="../L19-lab-fox-hunt/index.html">L19 Lab — Fox Hunt</a>
::::

::::{frame} Pre-Lab
:class: read-only doc-links

The L19 Lab's pre-lab is Part 1 of its packet, one per team, done before the
lab period. It works this lesson's error budget for the range and has you
write the fox-hunt script: start from the starter file, write its four
functions, and test it on the supplied bearings. Bring the tested script to
the lab on your laptop.

- <a class="doc-link" href="../../labs/ECE444_Lab_L19_FoxHunt_blank.pdf" target="_blank" rel="noopener">L19 Lab packet, Part 1 (PDF)</a>
- <a class="doc-link" href="../../labs/foxhunt_starter.py" download>Fox-hunt starter script</a>
::::

::::{frame} Looking Ahead
:::{present}
- In the L19 Lab, one kit takes a bearing from each station on a taped firing line.
- Bring your tested script from the Pre-Lab.
- L20 returns to shaping and steering the beam.
:::

In the L19 Lab you and a partner find the one live HB100 among the numbered
boxes. You move one kit along a taped firing line, square to the tape at every
station, read Angle off the beam sweep at each station mark, convert it to a
room bearing, and solve for the fix. Come with the Pre-Lab script, tested.

:::{depth}
The rest of Module 3 returns to the pattern the sweep traces. L20 measures
beamwidth against element count, L21 separates the array factor from the
element pattern, L22 trades sidelobe level for beamwidth with a taper, L23
covers beam squint and phase quantization, of which this lesson's sweep grid is
one consequence, and L24 steers nulls, which is how a direction finder or a
radar rejects a second source that would otherwise pull its peak.
:::
::::
