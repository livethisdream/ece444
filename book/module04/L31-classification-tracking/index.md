---
frame_view: true
---

# L31 - Classification and Tracking

::::{frame}
:class: title-frame

<div class="course-mark">ECE 444 · Fall 2026</div>

<h1 class="frame-title">Classification and Tracking</h1>

<div class="title-rule"></div>

Read four targets' micro-Doppler on your kit, then classify recorded targets and track a walker in range and angle.

Lesson 31 · Antennas, Phased Arrays, and Radar Systems · Dr. Neil Rogers
::::

::::{frame} Printing
:class: read-only

To print the slides, switch to present mode and print: one slide a sheet,
with room for notes. Print from read mode for the whole lesson.
::::

::::{frame} Learning Objectives
:class: here-31

<ol class="lo-list" style="--module: '4'; counter-reset: lo 7">
  <li>I can integrate FMCW radar processing with a phased-array front-end to track a moving target.</li>
  <li>I can classify a detected target from its micro-Doppler signature and report the classifier's accuracy.</li>
</ol>

```{include} ../../_snippets/m4-strip.md
```

:::{depth}
By the end of the <a href="../L30-cfar/index.html">L30 Lab</a> the radar
produces a list of detections, each a range, a radial velocity, and an SNR.
A detection says that something is there and how fast it is closing. It does
not say what the target is, and one detection per frame does not say where
the target is going. This page adds the last two stages of the chain your
[final project](../final-project/index.md) report explains. The lesson comes
first, and you read it before the lab: it classifies a detected target from
its micro-Doppler signature, which
<a href="../L26-range-resolution-doppler/index.html#frame-a-first-look-at-micro-doppler">Lesson 26</a>
introduced, measures how often the classifier is right, and then joins the
detections into a track in range, with an alpha-beta filter, and in angle,
with the monopulse comparison of the
<a href="../../module03/L24-lab-null-steering/index.html#frame-procedure-d-watch-it-track">L24 Lab</a>.
Its last frame, the Pre-Lab, lists the predictions you make before the lab.
The lab follows it on this page.
:::
::::

::::{frame} An Example Burst
:class: read-only

The lesson works each method on an example burst, not the lab's preset, and
on example targets, not the lab's records:

| Example burst | Value |
| :-- | :-- |
| carrier, wavelength | $10.0\ \text{GHz}$, $\lambda = 3.0\ \text{cm}$ |
| chirp | $400\ \text{MHz}$ in $300\ \mu\text{s}$, one every $0.4\ \text{ms}$ |
| frame | $256$ chirps, $102.4\ \text{ms}$ |
| range bin | $c/2B = 0.375\ \text{m}$ |

Work your own Part 1 values at the lab's preset, which the lab's
Big Picture names.
::::

::::{frame} Micro-Doppler of a Moving Part
:class: read-only

:::{present}
$$\begin{aligned}
f_D(t) &= \frac{2}{\lambda}\left[v_\text{body} + v_\text{part}(t)\right] \\
v_\text{part}(t) &= \Omega\rho\ \sin(\Omega t) \quad \text{(a rotor)}
\end{aligned}$$

- A rotor's tips set the edge of its band, $\pm v_\text{tip}$.
- A walker's torso sets a line off zero, and its limbs swing about it once a stride.
:::

Lesson 26 derived the Doppler shift of a rigid target, $f_D = 2v_r/\lambda$.
A real target is rarely rigid. Its body moves at one radial speed, and its
parts move about the body at speeds of their own, so each part's echo carries
the body's Doppler plus a shift from its own motion. The extra shifts are the
**micro-Doppler**, and they change in time with the motion that causes them.

A point on a rotor at radius $\rho$, turning at $\Omega$ radians per second
and seen edge-on, swings toward and away from the radar along the line of
sight, so its radial speed is $\Omega\rho\sin(\Omega t)$ and its Doppler
swings sinusoidally between $\pm 2\Omega\rho/\lambda$. Every point along a
blade does this at its own radius, so a blade fills the band from zero out to
its tip. The tips move fastest. For a $25\ \text{cm}$ fan at $700\ \text{rpm}$,

$$\begin{aligned}
v_\text{tip} &= \pi D\ \frac{\text{rpm}}{60} \\
&= \pi(0.25)\frac{700}{60} = 9.2\ \text{m/s},
\end{aligned}$$

which is $\pm 2(9.2)/0.030 = \pm 611\ \text{Hz}$ at $10.0\ \text{GHz}$. A rotor
held at a tilt $\psi$ off edge-on moves only $\cos\psi$ of that along the
line of sight, so the same fan turned $40^\circ$ shows tips at
$9.2\cos 40^\circ = 7.0\ \text{m/s}$.

A walker's arms and legs swing forward and back about the torso, once a
stride, like pendulums. A walker closing at $1.1\ \text{m/s}$ whose limbs
swing $2.3\ \text{m/s}$ about the torso puts the torso at $73\ \text{Hz}$, and
the limbs reach $1.1 + 2.3 = 3.4\ \text{m/s}$, or $227\ \text{Hz}$, on the
forward stroke, and $1.1 - 2.3 = -1.2\ \text{m/s}$ on the back stroke. The
body's Doppler says how fast the target is moving. The micro-Doppler says
what is moving, which is the property a classifier needs.
::::

::::{frame} Four Signatures
:class: read-only

:::{present}
- The walker shows a torso line off zero, and its limbs swing once a stride.
- The fan shows a steady band out to its tips.
- The spinner's band piles up in horns near its tips.
- The hand shows one trace swinging through zero.
:::
:::{present}
<img src="../../viz/img/L31-signatures.svg"
     alt="Simulated slow-time spectrograms over three seconds of the lesson's four example targets, each panel with its own Doppler span in hertz and, on the right, in meters per second: a walker whose torso line, dashed, sits at 73 Hz above zero with limb traces swinging 0.9 times a second; a fan with a steady band out to plus and minus 611 Hz; a spinner whose band is strongest near plus and minus 314 Hz; and a hand whose single trace swings sinusoidally through zero"
     style="max-width: 520px; width: 100%; display: block; margin: 0 auto;">
:::

The L31 Lab reads four kinds of target: you walking, a desk fan, a fidget
spinner, and your hand waving. The figure simulates the lesson's example of
each on the example burst, one range bin sampled once per chirp, with the
spectrogram the next frames build. Each panel has its own span, and the
right-hand axis reads the same scale in m/s, the unit of the app's view.

The walker is the only target that goes anywhere, so it is the only one
whose pattern sits off zero: the torso is the steady line at $73\ \text{Hz}$
and the limbs trace arcs above and below it, once a stride. The fan stays
put, so its band is centered on zero, and it is steady, because the blades
pass too often for any one of them to appear. The spinner, $6\ \text{cm}$
across at $1500\ \text{rpm}$, is a smaller rotor, with tips at
$\pi(0.06)(25) = 4.7\ \text{m/s}$, or $314\ \text{Hz}$. Its weight sits in
three lobes near the rim rather than along a blade, and a point moving
sinusoidally spends most of its time near its extremes, so its band piles up
in two horns near the tip speed instead of filling evenly. The hand is one
scatterer moving back and forth. A wave $0.15\ \text{m}$ each way at
$1.2\ \text{Hz}$ peaks at $2\pi(1.2)(0.15) = 1.1\ \text{m/s}$, or $75\ \text{Hz}$, and the
trace crosses zero twice a cycle, so the hand has no average Doppler at all.

In the app's Range-Doppler view the same targets appear at their ranges,
across velocity: watched for a few seconds, each one's band spans the speeds
its parts reach, and the walker's sits off zero.
::::

::::{frame} One Range Bin in Slow Time
:class: read-only

:::{present}
- One sample per chirp: $2.5\ \text{kHz}$ on the example burst, so $\pm 1.25\ \text{kHz}$, or $\pm 18.75\ \text{m/s}$.
- A part faster than that aliases.
- A walker crosses a $0.375\ \text{m}$ bin in $0.34\ \text{s}$: sum the bins around it.
:::

<a href="../L29-range-doppler-mti/index.html">Lesson 29</a> forms the
range-Doppler map with an FFT across the chirps of a burst, one FFT for each
range bin. That FFT runs in **slow time**: one sample per chirp, from the
same range bin of each chirp's range profile. A spectrogram is the same FFT
taken over short, overlapping pieces of a longer recording instead of over
one whole burst, so each column of the spectrogram is a Doppler spectrum of a
few tens of milliseconds of the target.

<img src="../../viz/img/L31-slow-time.svg"
     alt="The burst drawn as a grid of range bins down and chirps across; one range bin's row is highlighted, and three overlapping windows along it each feed one spectrogram column"
     style="max-width: 460px; width: 100%; display: block; margin: 0 auto;">

The slow-time samples arrive at the PRI, $0.4\ \text{ms}$ on the example
burst, so the sample rate is $2.5\ \text{kHz}$ and the spectrogram covers
$\pm 1.25\ \text{kHz}$, the $\pm 18.75\ \text{m/s}$ that L29 calls
$v_\text{max}$. A part faster than that aliases, as in L26, and wraps to the
wrong Doppler. The $30\ \text{cm}$ fan of L26's CW demo, with tips at
$18.8\ \text{m/s}$, sits just past that edge and its tips wrap, though they
did not in CW, where ADI's script sampled at $0.6\ \text{MHz}$.

Two more details make the spectrogram show the target and nothing else.
Stationary returns, the walls and the fan's own stand, sit at
$0\ \text{Hz}$ and are far stronger than the parts that move; subtracting the
mean of the slow-time samples removes them, which is what MTI does at
$0\ \text{Hz}$. And a target that moves in range leaves its bin: at
$1.1\ \text{m/s}$ the example walker crosses a $0.375\ \text{m}$ bin in
$0.34\ \text{s}$, so the spectrogram of one bin shows the walker in pieces.
For a walker, `spectrogram` takes a slice of bins around the track's range
and sums them, flipping the sign of every other bin first: a Hann-windowed
tone puts $-\tfrac{1}{4}$, $\tfrac{1}{2}$, $-\tfrac{1}{4}$ of itself in
neighboring bins, so a plain sum cancels whenever the target sits on a bin
center, while the alternating sum makes the three add.
The range bin comes from the L30 detection list. The course provides
`radar_lab.py` complete, with a notebook for each lab; its `spectrogram` is
the one below, and the lab asks you to run it and tune it, not to write it.

```python
def spectrogram(cap, range_bin, n_win=64, hop=16):
    """Slow-time spectrogram of one range bin: (t, f_D, S_dB), peak at 0 dB."""
    X = range_fft(cap)[:, range_bin]            # one sample per chirp
    if X.ndim == 2:                             # a slice: alternate signs, sum
        X = (X * (-1.0) ** np.arange(X.shape[1])).sum(axis=1)
    x = X
    x = x - x.mean()                            # stationary returns out
    w = np.hanning(n_win)
    cols = [np.fft.fftshift(np.fft.fft(x[i:i + n_win] * w))
            for i in range(0, len(x) - n_win + 1, hop)]
    S = 20 * np.log10(np.abs(np.array(cols).T) + 1e-12)
    f = np.fft.fftshift(np.fft.fftfreq(n_win, cap["PRI"]))
    t = (np.arange(S.shape[1]) * hop + n_win / 2) * cap["PRI"]
    return t, f, S - S.max()
```
::::

::::{frame} Window Length
:class: read-only

:::{present}
$$\begin{aligned}
\Delta f &= \frac{1}{T_w} \\
\delta f &= \dot f_D\ T_w = \frac{2a}{\lambda}\ T_w \\
T_w &= \frac{1}{\sqrt{\dot f_D}} \\
&= \frac{1}{\sqrt{867\ \text{Hz/s}}} = 34\ \text{ms}
\end{aligned}$$
:::
:::{present}
- The example walker's limbs accelerate at $13.0\ \text{m/s}^2$, so 64 chirps, $25.6\ \text{ms}$, is the nearest power of two.
- The example fan's tips change at $45\ \text{kHz/s}$, so no window follows a blade.
:::

Every spectrogram trades resolution in frequency against resolution in time.
A window of length $T_w$ resolves Doppler shifts $\Delta f = 1/T_w$ apart, the
$\Delta f = 1/T$ of L26, so a long window resolves finely. But a limb's
Doppler does not hold still during the window. If it changes at a rate
$\dot f_D$, it moves by $\delta f = \dot f_D T_w$ while the window is open, and
the column smears that far. A Doppler rate comes from an acceleration $a$
along the line of sight, $\dot f_D = 2a/\lambda$, by differentiating
$f_D = 2v/\lambda$.

The resolution improves as the window grows and the smear worsens, so the
best window makes the two equal, $1/T_w = \dot f_D T_w$, which gives
$T_w = 1/\sqrt{\dot f_D}$. The example walker swings its limbs
$2.3\ \text{m/s}$ about the torso, $0.9$ times a second, so their peak
acceleration is $2\pi(0.9)(2.3) = 13.0\ \text{m/s}^2$ and

$$\begin{aligned}
\dot f_D &= \frac{2(13.0)}{0.030} = 867\ \text{Hz/s}, \\
T_w &= 34\ \text{ms},
\end{aligned}$$

about 85 chirps of the example burst. Windows come in powers of two:

| Window | $T_w$ | Resolution $1/T_w$ | Limb smear $\dot f_D T_w$ |
| :-- | --: | --: | --: |
| 16 chirps | $6.4\ \text{ms}$ | $156\ \text{Hz}$ | $6\ \text{Hz}$ |
| 64 chirps | $25.6\ \text{ms}$ | $39\ \text{Hz}$ | $22\ \text{Hz}$ |
| 128 chirps | $51.2\ \text{ms}$ | $20\ \text{Hz}$ | $44\ \text{Hz}$ |
| 256 chirps | $102.4\ \text{ms}$ | $9.8\ \text{Hz}$ | $89\ \text{Hz}$ |

Sixty-four chirps keeps the two closest, and it resolves
$0.59\ \text{m/s}$.

<img src="../../viz/img/L31-window.svg"
     alt="Resolution and limb smear in hertz against window length on log axes: resolution falls as one over the window and smear rises with it, crossing at the best window of 34 milliseconds; the 16, 64 and 256 chirp windows of the example burst are marked"
     style="max-width: 460px; width: 100%; display: block; margin: 0 auto;">

A measured line is wider than $1/T_w$. The Hann window that `spectrogram`
applies widens a line's main lobe to $1.44$ bins at its 3 dB points, the
widening <a href="../L28-fmcw/index.html">Lesson 28</a> gives for a line in range,
and a part that moves during the window widens it further, so expect a line
about $1.44/T_w$ wide or more. Sixteen chirps follows the limbs but resolves only
$156\ \text{Hz}$; 256 chirps resolves finely but smears the limbs across
$89\ \text{Hz}$. The torso, which hardly accelerates, is sharpest in the
longest window. The table changes with the PRI, so the lab's own windows have
their own numbers.

A fan is the opposite case. Its tips accelerate at $\Omega^2 R$, which for the
example fan is $672\ \text{m/s}^2$, so $\dot f_D = 45\ \text{kHz/s}$ and the
best window is $4.7\ \text{ms}$, twelve chirps, which resolves only
$212\ \text{Hz}$. No window follows one blade through its turn. A long window
shows the blades' band averaged over many passes, steady in time, and a very
short one shows each blade's flash as it passes broadside. The hop between
columns, 16 chirps here, sets only how often we compute a column, not what it
resolves.
::::

::::{frame} Window Explorer
:class: read-only

<iframe src="../../viz/spectrogram-window.html"
        width="100%" height="422"
        style="border: 1px solid #cddce9; border-radius: 6px;"
        loading="lazy"
        title="Slow-time spectrogram of the lesson's example walker, fan, spinner, or waving hand on the example burst, with the window length set from 8 to 512 chirps">
</iframe>

The widget computes the spectrogram of the chosen example target on the
example burst for a window of 8 to 512 chirps; the readout gives the window
in chirps and milliseconds and the resolution $1/T_w$, and the red bar at the
top right is the window's length on the time axis. It opens on the walker at
64 chirps. Lengthen the window and the torso line sharpens while the limb
arcs blur along time; shorten it and the limbs follow their swing while every
line thickens in Doppler. Then pick the fan and shorten the window to 16
chirps: the band breaks into the blades' flashes, 70 a second, since each of
the three blades lies across the line of sight twice a turn at
$700\ \text{rpm}$.
::::

::::{frame} Three Features
:class: read-only

:::{present}
$$\begin{aligned}
\bar f(t) &= \frac{\sum_f f\ P(f,t)}{\sum_f P(f,t)} \\
\sigma_f(t) &= \sqrt{\frac{\sum_f \left(f-\bar f\right)^2 P(f,t)}{\sum_f P(f,t)}}
\end{aligned}$$

- The **centroid** $\lambda\bar f/2$ is the body's speed.
- The **spread** $\lambda\sigma_f/2$ is its parts' speed about it.
- The **periodicity** is how strongly it repeats, at $0.25$ to $2\ \text{s}$.
:::

A classifier does not look at a picture; it compares numbers. A **feature**
is one number computed from the spectrogram that takes different values for
different classes of target, and three are enough to separate most of the
lab's four kinds of target. Each measures a different physical property, which is why they
separate targets that any one of them alone would confuse.

Each column of the spectrogram is a Doppler spectrum $P(f,t)$, in linear
power. Before using it we zero every bin more than $15\ \text{dB}$ below that
column's peak, so the noise floor does not count as motion. The **centroid**
$\bar f(t)$ is the power-weighted mean Doppler of the column, and averaged over
the recording and multiplied by $\lambda/2$ it is the body's radial speed. We
keep its magnitude, since a walker may approach or recede. The **spread**
$\sigma_f(t)$ is the power-weighted RMS width of the column about its
centroid; averaged and scaled the same way, it says how fast the parts move
relative to the body.

The **periodicity** asks whether the motion repeats at the pace of a body. We
subtract each Doppler row's mean, smooth along time over 12 columns, about
$0.08\ \text{s}$ on the example burst, so a rotor's blade flashes average out, and correlate the spectrogram with a copy
of itself shifted in time, normalized so a zero shift gives 1. A stride or a
wave repeats every $0.25$ to $2\ \text{s}$; the largest correlation at those
shifts is the periodicity. A steady rotor scores low, about 0.2, and a walker
or a waving hand scores near 0.8. The provided `features` computes all three:

```python
def features(t, f, S, lam, floor_db=-15):
    """Centroid and spread in m/s, and periodicity, from one spectrogram."""
    S = S - S.max(axis=0, keepdims=True)        # each column's peak at 0 dB
    P = np.where(S > floor_db, 10 ** (S / 10), 0.0)
    fc = (f[:, None] * P).sum(0) / P.sum(0)     # centroid, each column
    sd = np.sqrt(((f[:, None] - fc) ** 2 * P).sum(0) / P.sum(0))
    D = np.maximum(S, floor_db)
    D = np.array([np.convolve(row, np.ones(12) / 12, "valid") for row in D])
    D = D - D.mean(axis=1, keepdims=True)
    dt = t[1] - t[0]
    r = [np.sum(D[:, :-n] * D[:, n:]) / np.sum(D ** 2)
         for n in range(int(0.25 / dt), int(2.0 / dt))]
    return np.array([abs(fc.mean()) * lam / 2, sd.mean() * lam / 2, max(r)])
```
::::

::::{frame} Nearest-Centroid Classifier
:class: read-only

:::{present}
<img src="../../viz/img/L31-features.svg"
     alt="Twenty training trials of each example target in two panels. Left, centroid against spread: walkers spread along the centroid axis; hands, spinners and fans sit near zero centroid, most hands lowest in spread, spinners and fans overlapping between about 2 and 7 meters per second. Right, periodicity against spread: hands and walkers sit near 0.8 periodicity, rotors below about 0.5. A cross marks each class's mean"
     style="max-width: 560px; width: 100%; display: block; margin: 0 auto;">
:::
:::{present}
$$\begin{aligned}
z_i &= \frac{x_i - \mu_i}{s_i} \\
\hat c &= \arg\min_k \lVert \mathbf z - \bar{\mathbf z}_k \rVert
\end{aligned}$$

- Training stores each class's mean.
- A trial takes the nearest mean's class.
:::

A **nearest-centroid** classifier is the simplest one that learns from data.
We record a set of **training** trials of each target, compute the three
features of each, and keep each class's mean, the crosses in the figure.
A new trial gets the class whose mean is nearest. The features have different
units, m/s for two and none for periodicity, so we first scale each one by
its mean $\mu_i$ and standard deviation $s_i$ over the training set; without
that, the feature with the largest numbers would decide every distance.

The figure plots 20 simulated training trials of each example target on the
example burst: walkers at speeds from 0.7 to $1.5\ \text{m/s}$ and up to
$60^\circ$ off the line of sight, $25\ \text{cm}$ fans from 450 to
$850\ \text{rpm}$, $6\ \text{cm}$ spinners from 900 to $2000\ \text{rpm}$,
waves of different sizes and rates, and an SNR of 3 to $15\ \text{dB}$ a
chirp. The walkers are the only class well off zero in centroid, with a mean
of $0.78\ \text{m/s}$. Most hands have the least spread among the others,
under $1\ \text{m/s}$, though a few slow, large waves reach into the rotors'
range, and the right panel shows what sets the hands apart: periodicity. The fans and spinners share
zero centroid and low periodicity, so only their spread separates them, a
mean of $4.7$ against $3.6\ \text{m/s}$, and the two clouds overlap: a fast
spinner looks like a slow fan.

Thresholds work too: centroid above $0.3\ \text{m/s}$ is a walker;
otherwise, periodicity above 0.5 is a hand; otherwise, spread above about
$4.1\ \text{m/s}$ is a fan. A nearest-centroid rule picks those boundaries
from the data rather than by eye. The provided classifier is the
nearest-centroid one:

```python
def train(X, y):
    """X: one row of features per trial; y: each trial's class."""
    mu, sd = X.mean(0), X.std(0)
    cents = {c: ((X[y == c] - mu) / sd).mean(0) for c in set(y)}
    return mu, sd, cents

def classify(x, model):
    mu, sd, cents = model
    z = (x - mu) / sd
    return min(cents, key=lambda c: np.sum((z - cents[c]) ** 2))
```
::::

::::{frame} The Confusion Matrix
:class: read-only

:::{present}
| true \ called | walker | fan | spinner | hand |
| :-- | --: | --: | --: | --: |
| walker | **20** | 0 | 0 | 0 |
| fan | 0 | **16** | 2 | 2 |
| spinner | 0 | 12 | **8** | 0 |
| hand | 0 | 0 | 0 | **20** |
:::
:::{present}
- Accuracy on unseen trials is $64/80 = 80\%$.
- Fourteen of the 16 errors mistake one rotor for the other.
:::

The **confusion matrix** counts, for each true class (a row), how many trials
the classifier called each class (a column). The diagonal holds the correct
calls, and every count off the diagonal is a specific mistake. Its
**accuracy** is the diagonal's total over all trials,

$$\text{accuracy} = \frac{20 + 16 + 8 + 20}{80} = 80\%.$$

The trials in the matrix are a second set of 20 per class, drawn the same way
as the training set but not used to train. A classifier scored on its own
training trials has already seen the answers, and its accuracy overstates
what it will do on a target it has not seen. The lab scores each record with
a classifier trained on all the others, **leave-one-out**, which keeps that
rule when there are only a few records of each class.

The matrix says more than the accuracy does. Fourteen of the 16 errors are a
fan called a spinner or a spinner called a fan, the overlap the previous
figure showed, and the other two are slow fans whose small spread falls
nearer the hands' mean. Walkers and hands are never wrong. An 80% classifier
that never misses a person is a different instrument from one that misses
people 20% of the time, and only the matrix tells them apart. It also says
what to improve: a feature that separates the two rotors would address most
of the errors. Finally, the number is an estimate. Five different draws of 80
test trials score between 80% and 84%, so with 20 trials a class report the
counts, not only the percentage.
::::

::::{frame} The Band's Edge and Shape
:class: read-only

:::{present}
$$\begin{aligned}
v_\text{rms} &= v_\text{tip}\sqrt{\left\langle \sin^2 \Omega t \right\rangle \left\langle (\rho/R)^2 \right\rangle} \\
&= v_\text{tip}\sqrt{\tfrac12 \left\langle (\rho/R)^2 \right\rangle}
\end{aligned}$$

- The **edge** is the tip speed; a tilt or a rate scales it.
- The **shape**, spread over edge, says where the weight sits.
:::

Two more features can separate the rotors. The **edge** is the speed at the
outside of each column's band, the bins within $15\ \text{dB}$ of the
column's peak, averaged over the record: for a rotor it is the tip speed
along the line of sight, $v_\text{tip}\cos\psi$. The spread measures the
same motion in a different way, as an RMS. Both grow with the rate and both
shrink with the tilt, so a fast spinner and a slow or tilted fan can share
either one.

Their ratio does not. Every point on a rotor moves at
$v_\text{tip}(\rho/R)\sin\Omega t$ along the line of sight, so its RMS speed
over a turn and over the points is the first line above. The mean of
$\sin^2$ over a turn is $\tfrac12$. The mean of $(\rho/R)^2$ depends only on
where along the radius the weight sits. For a blade whose weight is spread
evenly over its outer third, from $\rho = 2R/3$ to $R$,

$$\begin{aligned}
\left\langle (\rho/R)^2 \right\rangle &= \frac{1}{R/3}\int_{2R/3}^{R}\frac{\rho^2}{R^2}\ d\rho = \frac{1 - (2/3)^3}{3(1/3)} = 0.704, \\
\frac{v_\text{rms}}{v_\text{tip}} &= \sqrt{\tfrac12(0.704)} = 0.59.
\end{aligned}$$

A tilt or a rate scales every speed in the band by the same factor, so the
**shape**, the spread over the edge, is the same at any tilt and any rate: it
measures where the weight sits, not how fast it moves. A rotor whose weight
sits farther out has a larger shape.

<img src="../../viz/img/L31-shape.svg"
     alt="Held Doppler spectra in decibels against radial speed divided by the band's edge, for a blade weighted evenly from hub to tip, the same blade tilted 40 degrees, a rotor with its weight at the rim, and a blade weighted on its outer third; the tilted blade's curve lies on the untilted one, the rim's piles up at the edges, and dashed lines mark the outer third's RMS speed"
     style="max-width: 460px; width: 100%; display: block; margin: 0 auto;">

The figure normalizes each held spectrum to its own edge. The tilted blade
lands on the untilted one, because a tilt scales every speed by the same
$\cos\psi$; the rim and the outer third differ from the full blade because
their weight sits elsewhere. The notebook's task (b) adds the edge
and then the shape to the three features and compares the matrices.
::::

::::{frame} The Alpha-Beta Filter
:class: read-only

:::{present}
$$\begin{aligned}
\hat R_k^- &= \hat R_{k-1} + \hat v_{k-1}\ \Delta t \\
e_k &= z_k - \hat R_k^- \\
\hat R_k &= \hat R_k^- + \alpha\ e_k \\
\hat v_k &= \hat v_{k-1} + \frac{\beta}{\Delta t}\ e_k
\end{aligned}$$

- Predict, compare with the detection $z_k$, correct.
- $\Delta t$ is one range-Doppler frame.
- On a missed frame, the filter only predicts.
:::

A detection list is noisy. Each range is the center of a range bin, a
walker's body is larger than a bin, some frames miss the target, and nothing
in the list says that the detection at $3.1\ \text{m}$ in one frame is the
same person as the one at $3.4\ \text{m}$ in the next. A **track** joins the
detections of one target into a single estimate of its range and velocity,
frame after frame. A military radar calls a person on foot a **dismount**;
tracking one is the second half of the L31 Lab.

The **alpha-beta filter** is the simplest tracker. It assumes the target moves
at a constant velocity over one frame. Each frame it **predicts** where the
target should be, $\hat R_k^-$, from the last estimate. It compares the
prediction with the frame's detection $z_k$; the difference $e_k$ is the
**residual**. It then **corrects** both estimates by fixed fractions of the
residual: $\alpha$ of it moves the range, and $\beta/\Delta t$ of it moves the
velocity. A frame with no detection near the prediction keeps the prediction
and corrects nothing, which is how a track coasts through a miss. The
detection a track accepts is the one nearest its prediction, inside a gate of
a few bins, which is also how two targets keep separate tracks. On the
example burst one frame is 256 chirps of $0.4\ \text{ms}$,
$\Delta t = 102.4\ \text{ms}$. The provided `alpha_beta` is the filter as
written above:

```python
def alpha_beta(track_meas, alpha, beta, dt):
    """Range track from one detection per frame (NaN for a missed frame)."""
    r, v = track_meas[0], 0.0
    out = []
    for z in track_meas:
        r = r + v * dt                          # predict
        if not np.isnan(z):
            e = z - r                           # residual
            r, v = r + alpha * e, v + beta / dt * e
        out.append((r, v))
    return np.array(out)
```
::::

::::{frame} Choosing Alpha and Beta
:class: read-only

:::{present}
$$\begin{aligned}
\beta &= \frac{\alpha^2}{2-\alpha} \\
\frac{\sigma_\text{track}}{\sigma_z} &= \sqrt{\frac{2\alpha^2 + 2\beta - 3\alpha\beta}{\alpha(4 - 2\alpha - \beta)}} \\
\text{lag} &= \frac{a\ \Delta t^2}{\beta}
\end{aligned}$$
:::
:::{present}
<img src="../../viz/img/L31-alpha-beta.svg"
     alt="Range against time for eight seconds: a walker walks out from 2 to about 6.6 meters, turns, and walks back; the detections step in 0.375 meter bins around the truth; the alpha equals 0.4 track follows the truth closely through the turn, and the alpha equals 0.15 track lags it by up to 0.9 meters"
     style="max-width: 520px; width: 100%; display: block; margin: 0 auto;">
:::

The two gains set how much weight the track gives a new detection. A large $\alpha$
follows each detection closely, noise and all; a small one averages over many
frames and smooths the noise, but it is slow to notice a change in velocity,
so it lags a target that turns. The usual choice ties the two gains together,
$\beta = \alpha^2/(2-\alpha)$, the Benedict-Bordner choice, which balances the
track's noise against its lag and leaves one number to choose.

The other two lines say what that number trades. For detection noise
$\sigma_z$ that is independent from frame to frame, the track's settled RMS
error is $\sigma_\text{track}$, the second line: the filter's output is a
weighted sum of past detections, and the line is the RMS of that sum's
weights. Under a steady acceleration $a$ the track trails the target by the
third line. The target gains $a\Delta t$ of speed each frame, and once the
track settles its velocity must gain the same, so the velocity correction
$(\beta/\Delta t)e$ equals $a\Delta t$ and the residual is $e = a\Delta t^2/\beta$. Work both for $\alpha = 0.4$ on the example
burst:

$$\begin{aligned}
\beta &= \frac{0.4^2}{2 - 0.4} = 0.100, \\
\frac{\sigma_\text{track}}{\sigma_z} &= \sqrt{\frac{2(0.16) + 2(0.1) - 3(0.4)(0.1)}{0.4\left(4 - 0.8 - 0.1\right)}} = 0.57.
\end{aligned}$$

A walker who turns by swinging from $+1.2$ to $-1.2\ \text{m/s}$ over
$1\ \text{s}$, as a cosine, has a peak acceleration of
$\pi(1.2) = 3.8\ \text{m/s}^2$, so the settled lag would be

$$\text{lag} = \frac{3.8\ (0.1024)^2}{0.100} = 0.40\ \text{m}.$$

<img src="../../viz/img/L31-ab-trade.svg"
     alt="The alpha-beta trade on the example burst: the noise ratio rises from about 0.2 toward 1 as alpha grows, and the settled lag, on a log axis, falls from tens of meters toward a few centimeters; alpha equal to 0.4 is marked on both curves"
     style="max-width: 460px; width: 100%; display: block; margin: 0 auto;">

A small $\alpha$ gives a low noise ratio and a long lag, and a large one the
reverse; the choice depends on how much the target maneuvers.

The figure simulates that walk on the example burst: out from
$2\ \text{m}$ at $1.2\ \text{m/s}$, the one-second turn, and back. The
detections are the centers of the $0.375\ \text{m}$ bins the walker falls in,
with $0.12\ \text{m}$ of body jitter, $0.15\ \text{m}$ RMS from the truth in
all, and 5 of the 79 frames missed. With $\alpha = 0.4$ the track holds
$0.12\ \text{m}$ RMS on the straights, better than the detections, and is off
by at most $0.23\ \text{m}$ at the turn, less than the settled $0.40$,
because the turn ends before the lag builds up. With $\alpha = 0.15$ the
track is smoother, but it trails the turn by up to $0.9\ \text{m}$ and is
still catching up on the way back. The track's velocity is a second check: it
should agree with the Doppler velocity of the detections it accepts.
::::

::::{frame} Angle by Monopulse
:class: read-only

:::{present}
$$\begin{aligned}
\Delta\phi &= \frac{2\pi D}{\lambda}\ \sin\theta \\
\theta &= \arcsin\frac{\lambda\ \Delta\phi}{2\pi D}
\end{aligned}$$

- Two subarray channels $D = 56\ \text{mm}$ apart give the angle in one look, with no sweep.
- Unambiguous within $\pm 15.5^\circ$ of broadside at $10.0\ \text{GHz}$.
- Read in the detection's range-Doppler cell.
:::

Range comes from the FMCW processing; angle comes from the array.
<a href="../../module03/L19-direction-finding/index.html">Lesson 19</a> found a
bearing by sweeping the beam across the field and taking the peak, one sweep
at a time. The <a href="../../module03/L24-lab-null-steering/index.html#frame-procedure-d-watch-it-track">L24 Lab</a>
measured it in one look with **monopulse**, comparing the two subarray
channels, and that is the method a tracker needs.

The two subarrays' centers sit four elements, $D = 56\ \text{mm}$, apart. A
wave from angle $\theta$ reaches one center a path $D\sin\theta$ before the
other, so the two channels differ in phase by

$$\Delta\phi = \frac{2\pi D}{\lambda}\sin\theta,$$

<img src="../../viz/img/L24-monopulse.svg"
     alt="The monopulse geometry of Lesson 24: two subarray centers a distance D apart, a plane wave arriving at angle theta, and the extra path D sine theta to the farther center"
     style="max-width: 360px; width: 100%; display: block; margin: 0 auto;">

$672^\circ$ per unit of $\sin\theta$ at $10.0\ \text{GHz}$, and the second line
turns a measured phase back into an angle. A phase is known only
within $\pm 180^\circ$, so the angle is unambiguous while $\sin\theta$ stays
within $\lambda/(2D) = 0.268$ of the steer direction's $\sin\theta_0$, which is
$\pm 15.5^\circ$ at broadside and a little more in angle when the beam is
steered. The L24 Lab's error function,

$$\frac{\text{Im}\lbrace\Delta\Sigma^*\rbrace}{\vert\Sigma\vert^2},$$

is the same comparison written for the sum and difference beams.

In the radar we take the two channels' values in the range bin where CFAR
declared the target. That bin holds the target's echo with the 256-chirp
integration gain of L27, and none of the clutter at other ranges, which
would pull the angle toward itself. So the lab saves both subarray channels.
Which side of broadside reads a positive angle depends on the order of the
kit's channels, so the lab checks it once, with a person on a mark to one
side.
::::

::::{frame} A Walker on a Diagonal
:class: read-only

:::{present}
$$\begin{aligned}
R &= \sqrt{x^2 + y^2}, \qquad \theta = \arctan\frac{x}{y} \\
v_r &= -v\ \hat{\mathbf u}\cdot\hat{\mathbf r}
\end{aligned}$$

- A diagonal walk changes the range and the angle together.
- Its radial speed is the part of the walk along the line of sight.
:::

Put the array at the origin, $y$ straight out along boresight and $x$ to the
side, positive on the E8 side. A point on the floor at $(x, y)$ sits at the
range and angle of the first line. A walker moving at speed $v$ in the
direction of the unit vector $\hat{\mathbf u}$ closes at the radial speed of
the second line, where $\hat{\mathbf r}$ is the unit vector from the array to
the walker; the minus sign makes a closing walker positive, as on every page
of this module.

<img src="../../viz/img/L31-floor.svg"
     alt="The floor seen from above: the array at the origin with E1 on the left and E8 on the right as drawn, boresight straight up as y, x to the side; the example walker at P on the E8 side walks toward Q on the E1 side, with the unit vector u along the walk, the unit vector r from the array to P, and the angle theta from boresight to P"
     style="max-width: 360px; width: 100%; display: block; margin: 0 auto;">

Work it for a walker who starts at $P$, $0.4\ \text{m}$ to the E8 side and
$1.8\ \text{m}$ out, and walks at $1.2\ \text{m/s}$ toward $Q$,
$0.9\ \text{m}$ to the E1 side and $3.4\ \text{m}$ out:

$$\begin{aligned}
R_P &= \sqrt{0.4^2 + 1.8^2} = 1.84\ \text{m}, \qquad \theta_P = \arctan\frac{0.4}{1.8} = +12.5^\circ, \\
\hat{\mathbf u} &= \frac{(-1.3,\ 1.6)}{2.06} = (-0.631,\ 0.776), \qquad \hat{\mathbf r}_P = \frac{(0.4,\ 1.8)}{1.84} = (0.217,\ 0.976), \\
v_{r,P} &= -1.2\left[(-0.631)(0.217) + (0.776)(0.976)\right] = -0.75\ \text{m/s}.
\end{aligned}$$

At $P$ the walker opens at $0.75\ \text{m/s}$, less than its $1.2\ \text{m/s}$
pace, because part of the walk runs across the line of sight. At $Q$,
$3.52\ \text{m}$ out and $-14.8^\circ$, the walk lines up more nearly with
the line of sight and the walker opens at $1.09\ \text{m/s}$. A walker who
turns and walks back has the same radial speeds with the sign reversed, and
at the turn itself the speed, and with it the radial speed, passes through
zero. That is the moment the 2-pulse canceller cuts the torso, and the
moment the filter's predict step carries the track.

A walker moving exactly across the line of sight has
$v_r = v\cos 90^\circ = 0$ (L26), so the torso's echo sits at
$0\ \text{Hz}$ and MTI removes it. A diagonal path keeps the Doppler from
vanishing except at the turn.
::::

::::{frame} Why Monopulse Holds a Walker
:class: read-only

:::{present}
- At $1\ \text{m/s}$ and $4\ \text{m}$ a crossing walker moves $14.3^\circ/\text{s}$.
- A beam sweep about a second long lets it leave the $13.6^\circ$ beam between looks.
- Between monopulse frames it moves $1.5^\circ$.
:::

A walker crossing in front of the radar at $1\ \text{m/s}$, $4\ \text{m}$
away, changes bearing at $v/R = 0.25\ \text{rad/s}$, or $14.3^\circ$ a second.
A beam sweep looks in each direction once a sweep, so between two looks the
walker moves $14.3^\circ/\text{s}$ times the sweep's length. The array's
beamwidth at $10.0\ \text{GHz}$ is

$$\theta_\text{3dB} = \frac{0.886\lambda}{Nd} = 13.6^\circ,$$

so any sweep longer than $13.6/14.3 = 0.95\ \text{s}$ lets the walker cross a
whole beamwidth between looks. The figure draws a sweep every
$1.1\ \text{s}$, the walker moving $15.9^\circ$ between looks.

<img src="../../viz/img/L31-sweep-vs-mono.svg"
     alt="A crossing walker's bearing against time over four seconds, from minus 27 to plus 27 degrees: beam-sweep looks every 1.1 seconds, each with its 13.6 degree beam shaded, are far apart, while monopulse frames every 0.1 seconds follow the bearing closely"
     style="max-width: 460px; width: 100%; display: block; margin: 0 auto;">

A sweep can find a walker who stands still, but a crossing walker can leave
the beam between one look and the next. Monopulse measures once a frame, and
in the example burst's $102.4\ \text{ms}$ the walker moves $1.5^\circ$, well
inside the $\pm 15.5^\circ$ monopulse window.

The tracker closes the loop. A second alpha-beta filter runs on the monopulse
angles, and its prediction for the next frame can become the next frame's
steer angle, so the walker stays near boresight, where the L24 Lab found the
monopulse response straight (about $\pm 5^\circ$). Objective 4.8 asks for
exactly this integration: range from the FMCW processing, angle from the
array, and a beam the track points.
::::

::::{frame} Summary
:class: read-only

| Symbol / idea | What it is | On the example burst |
| :-- | :-- | :-- |
| $f_D = 2(v_\text{body} + v_\text{part})/\lambda$ | micro-Doppler of a moving part | $25\ \text{cm}$ fan at $700\ \text{rpm}$: tips $9.2\ \text{m/s}$, $\pm 611\ \text{Hz}$ |
| slow time | one sample per chirp | $2.5\ \text{kHz}$: $\pm 1.25\ \text{kHz}$, $\pm 18.75\ \text{m/s}$ |
| $\Delta f = 1/T_w$, $\delta f = \dot f_D T_w$ | window: resolution against smear | best $T_w = 1/\sqrt{\dot f_D}$; $64$ chirps for the example walker |
| centroid, spread, periodicity | three features | $\lambda\bar f/2$, $\lambda\sigma_f/2$, autocorrelation at $0.25$-$2\ \text{s}$ |
| edge, shape | the band's outside, and spread over edge | weight on the outer third: shape $0.59$ |
| nearest centroid | the class whose mean is nearest, in scaled features | train and test on different trials |
| confusion matrix | true class against the call | $64/80 = 80\%$; most errors confuse the two rotors |
| alpha-beta | predict, residual, correct | $\alpha = 0.4$: $\beta = 0.100$, noise $0.57$, lag $0.40\ \text{m}$ |
| monopulse | $\Delta\phi = 2\pi D\sin\theta/\lambda$ | $D = 56\ \text{mm}$; $\pm 15.5^\circ$ at broadside |
| a diagonal walk | $v_r = -v\ \hat{\mathbf u}\cdot\hat{\mathbf r}$ | $-0.75\ \text{m/s}$ at $P$ |
::::

::::{frame} Pre-Lab
:class: read-only doc-links

Part 1 of the L31 Lab packet is the pre-lab: the shaded Predicted cells of
Tables A to E, each beside the Measured cell you fill in during the lab. Do
it before the lab, at the lab's preset and the givens the packet lists, and
bring it with you: you check every reading against the prediction next to it.

| Predicted cells | You predict | Checked in | Method |
| :-- | :-- | :-- | :-- |
| Table A | each target's largest speed on each side of $0\ \text{m/s}$, and whether its band is centered | Table A; Steps 5 to 8 | "Micro-Doppler of a Moving Part," "Four Signatures" |
| Table B | each tape mark's range and angle, the walker's range near A both ways and at the turn, its radial speed near A both ways, and the angle at B | Table B; Steps 9, 10, and 13 | "A Walker on a Diagonal," "Angle by Monopulse" |
| Table C | the resolution of each spectrogram window | Table C; Step 14 | "Window Length" |
| Table D | the shape of a fan's band and of a spinner's | Table D; Step 15 | "The Band's Edge and Shape" |
| Table E | the noise ratio and the settled lag of each $\alpha$ | Table E; Step 16 | "Choosing Alpha and Beta" |

Part 1 also asks you to attach your work for one row of each table, on your
own paper.

- <a class="doc-link" href="../../labs/ECE444_Lab_L31_ClassifyTrack_blank.pdf" target="_blank" rel="noopener">L31 Lab packet, Part 1 (PDF)</a>
::::

::::{frame} The Big Picture
:::{present}
| Steps | Set | Read |
| :-- | :-- | :-- |
| 5-8 | four targets | largest speeds |
| 9-11, 13 | walk A-B-A; sway on B | range, radial speed, angle |
| 14 | window 64, 16, 256 | line widths |
| 15 | features, + edge, + shape | confusion matrix |
| 16 | $\alpha$ 0.5, 0.2, 0.8 | track errors |
:::

The L31 Lab is the last stage of the chain your
[final project](../final-project/index.md) report explains, in four parts.
Bring Up the Kit (Steps 1 to 4) sets the Phaser app to its Range + Velocity
preset. Four Targets (Steps 5 to 8) reads the micro-Doppler of a fan, a
fidget spinner, your hand, and you walking in the Range-Doppler view. A
Crossing Walker (Steps 9 to 11) reads a walk on a diagonal and back, and
saves one burst on the far mark with both subarray channels. Run the
Notebook (Steps 12 to 17) runs the provided `radar_lab.py` on that burst and
on the course's recorded data: it reads the angle at the far mark, finds each
target with the L30 detector, classifies 16
records, and tracks a recorded walk in range and angle, while you change the
spectrogram window, add a feature, and tune $\alpha$. Each step that takes a
reading has boxes under it, and each fills a Measured cell of the packet,
beside the prediction you made in Part 1.

The app's **Save Capture** keeps one burst, 256 chirps or 128 ms. A stride
takes about a second, so the notebook classifies the course's 2 s records and
tracks the course's recorded walk, which carries its truth, with or without a
kit.
::::

::::{frame} Predict First
:class: viz-frame

:::{depth}
Before you read a target, predict its band, then check yourself. Pick a
target, set its size, rate, and tilt, or the walker's torso speed and limb
swing, and decide before you press **Show band** how far the band reaches on
each side of $0\ \text{m/s}$ and whether it is centered. Then show it. Any
change hides the band again, so each guess comes first. The widget opens on
the lesson's example targets; set it to the givens in Part 1 to check your
Table A predictions. It draws the band the Range-Doppler view holds over a
few seconds, without the kit's noise, leakage, or window skirts.
:::

:::{present}
<iframe src="../../viz/microdoppler-predict.html"
        width="100%" height="450"
        style="border: 1px solid #cddce9; border-radius: 6px;"
        loading="lazy"
        title="Choose a target and its size, rate and tilt, predict its micro-Doppler band, then show it">
</iframe>
:::
::::

::::{frame} Bring Up the Kit
:::{present}
- Transmit antenna on **OUT2** before you power the kit.
- FMCW, the Range + Velocity preset, then **Calibrate…** for 0 m.
- MTI on, 2-pulse; the **Range-Doppler** view; **Start**.
:::
:::{present}
<img src="../../viz/img/L31-app-settings.svg"
     alt="The Phaser app controls the lab sets: Mode FMCW, Preset Range + Velocity, 0 m Beat set by Calibrate, MTI on, MTI Mode 2-pulse, the Range-Doppler view, Subarray Channels on for Step 11, and Save Capture in Step 11"
     style="max-width: 400px; width: 100%; display: block; margin: 0 auto;">
:::

The preset is the lab's waveform: 300 µs chirps of 500 MHz, one every
0.5 ms, at 9.9 GHz, and 256 chirps a frame, 128 ms. Your Part 1 predictions
use it.

1. **Connect the transmit antenna.** With the kit powered off, connect the
   transmit antenna to **OUT2**. Connecting it with the kit on can damage the
   output stage.
2. **Load the preset.** Power the kit, open the Phaser app, select **FMCW**,
   and set **Preset** to **Range + Velocity**.
3. **Calibrate 0 m.** Set the 0 m frequency for this preset with
   **Calibrate…**, as in the L28 Lab, so that **0 m Beat (kHz)** holds your
   kit's value.
4. **Show the view.** Turn **MTI** on with **MTI Mode** at 2-pulse, open the
   **Range-Doppler** view, and press **Start**. The canceller removes
   everything that stands still, so the room drops out and only what moves
   stays. The FMCW mode holds the beam at broadside, $0^\circ$. The readouts
   give the **Peak Range** and **Peak Velocity** of the view's strongest
   cell.
::::

::::{frame} Four Targets
:::{present}
- Fan at 1 m, spinner at 0.5 m, hand at 0.8 m; then walk toward the kit.
- Read the largest speed on each side of $0\ \text{m/s}$.
- Note whether the band is centered, and compare each with your prediction.
:::

For each target, watch the Range-Doppler view for a few seconds and read,
from the velocity axis, the largest speed its band reaches on each side of
$0\ \text{m/s}$, positive closing, and whether the band is centered on
$0\ \text{m/s}$. Compare each reading with your Part 1 prediction before you
move on. A rotor shows micro-Doppler only where its parts move along the
line of sight, so hold the fan and the spinner edge-on, the plane they turn
in pointing at the array. Stand to the side while you read a rotor: your own
breathing and fidgeting move too.

5. **Fan.** Set a fan with a guard about 1 m in front of the kit, edge-on, on
   a setting whose speed you know, and keep your fingers clear of it. Read
   it. Then turn it about $45^\circ$ off edge-on and watch the band narrow,
   and face-on, where it nearly disappears: that is the check that your
   reading was edge-on.

   <div class="rec" data-lab="L31">
   <label>Step 5: fan, largest − (m/s) <input data-field="a.fan.neg"></label>
   <label>Largest + (m/s) <input data-field="a.fan.pos" data-label="Step 5: fan, largest + (m/s)"></label>
   <label>Centered? <input data-field="a.fan.ctr" data-label="Step 5: fan, centered?"></label>
   </div>
6. **Spinner.** Spin the fidget spinner and hold it edge-on about 0.5 m out,
   steady. Read it while it is fresh.

   <div class="rec" data-lab="L31">
   <label>Step 6: spinner, largest − (m/s) <input data-field="a.spinner.neg"></label>
   <label>Largest + (m/s) <input data-field="a.spinner.pos" data-label="Step 6: spinner, largest + (m/s)"></label>
   <label>Centered? <input data-field="a.spinner.ctr" data-label="Step 6: spinner, centered?"></label>
   </div>
7. **Hand.** Wave your hand toward and away from the kit, about 0.2 m each
   way, about 1.5 times a second, 0.8 m out. Read it.

   <div class="rec" data-lab="L31">
   <label>Step 7: hand, largest − (m/s) <input data-field="a.hand.neg"></label>
   <label>Largest + (m/s) <input data-field="a.hand.pos" data-label="Step 7: hand, largest + (m/s)"></label>
   <label>Centered? <input data-field="a.hand.ctr" data-label="Step 7: hand, centered?"></label>
   </div>
8. **Walker.** Set the laptop beside the kit, its screen toward you, and walk
   straight toward the kit from 4 m at a normal pace, watching the view as
   you come. Read the largest speed on each side of $0\ \text{m/s}$.

   <div class="rec" data-lab="L31">
   <label>Step 8: walker, largest − (m/s) <input data-field="a.walker.neg"></label>
   <label>Largest + (m/s) <input data-field="a.walker.pos" data-label="Step 8: walker, largest + (m/s)"></label>
   <label>Centered? <input data-field="a.walker.ctr" data-label="Step 8: walker, centered?"></label>
   </div>
::::

::::{frame} A Crossing Walker
:::{present}
- Tape A and B; measure each one's range and angle.
- Walk A to B to A; read near A both ways and at the turn.
- Sway on B; save one burst with both channels.
:::
:::{present}
<img src="../../viz/img/L31-floor-lab.svg"
     alt="The floor plan for the walk: the array at the bottom with E1 on the left and E8 on the right as drawn, boresight up; mark A 1.47 meters out and 0.31 meters to the E1 side, mark B 3.94 meters out and 0.69 meters to the E8 side, and the walk from A to B, a turn at B, and back"
     style="max-width: 340px; width: 100%; display: block; margin: 0 auto;">
:::

You need about 4.5 m of clear floor in front of the kit and a lane no one
else walks through, because anyone moving in the beam shows up in the view as
a second walker. Put the array
at the origin: $y$ straight out from it, $x$ to the side, positive on the E8
side. Facing the patches, E1 is on your right.

9. **Tape the marks.** Tape mark **A** 1.47 m straight out from the array and
   0.31 m to the E1 side, and mark **B** 3.94 m out and 0.69 m to the E8
   side. Measure each mark's range and angle from the array's center and
   compare them with your prediction.

   <div class="rec" data-lab="L31">
   <label>Step 9: mark A, range (m) <input data-field="b.a.range"></label>
   <label>Mark A, angle <input data-field="b.a.angle" data-label="Step 9: mark A, angle"></label>
   <label>Mark B, range (m) <input data-field="b.b.range" data-label="Step 9: mark B, range (m)"></label>
   <label>Mark B, angle <input data-field="b.b.angle" data-label="Step 9: mark B, angle"></label>
   </div>
10. **Walk it.** With MTI on, walk from A to B at about 1 m/s, turn at B, and
    walk back to A. Read the walker's range and velocity just after A, at B,
    and just before A on the way back, and compare them with your
    predictions. At B, read the torso line, not a limb's. Walking out, your
    back is to the screen, so have a partner read the view, or start a screen
    recording on the laptop, walk, and read the three moments from the
    recording afterward. If your ranges at A and B are both off by the same
    amount, the 0 m frequency is off: calibrate again (Step 3).

    <div class="rec" data-lab="L31">
    <label>Step 10: just after A, range (m) <input data-field="b.out.range"></label>
    <label>Velocity (m/s) <input data-field="b.out.vel" data-label="Step 10: just after A, velocity (m/s)"></label>
    <label>At B, range (m) <input data-field="b.turn.range" data-label="Step 10: at B, range (m)"></label>
    <label>Velocity (m/s) <input data-field="b.turn.vel" data-label="Step 10: at B, velocity (m/s)"></label>
    <label>Just before A, range (m) <input data-field="b.back.range" data-label="Step 10: just before A, range (m)"></label>
    <label>Velocity (m/s) <input data-field="b.back.vel" data-label="Step 10: just before A, velocity (m/s)"></label>
    </div>
11. **Save a burst on B.** Stand on mark B and sway, shifting your weight
    toward and away from the kit, because the canceller removes a person who
    stands still. Turn **Subarray Channels** on and press **Save Capture**.
    The app downloads one burst with both channels,
    `phaser_range_doppler_<date>-<time>.npz`; rename it `L31_sway_B.npz` and
    keep it for Step 13.
::::

::::{frame} Run the Notebook
:::{present}
- Task (a): the window, 64, then 16, then 256 chirps.
- Task (b): three features, then add the edge, then the shape.
- Task (c): $\alpha$ = 0.5, 0.2, 0.8, then your choice.
:::
:::{present}
<img src="../../viz/img/L31-notebook-strip.svg"
     alt="What the three notebook tasks show, with values left out: a walker's spectrogram for task (a), a four-by-four confusion matrix with its diagonal shaded for task (b), and a range track over the walk's truth and detections for task (c)"
     style="max-width: 520px; width: 100%; display: block; margin: 0 auto;">
:::

The notebook runs on your burst from Step 11 and on the course's recorded
data, with or without a kit, in about 30 to 45 minutes. The notebook finds
each record's target with the L30 chain, run on the record's first burst, the
2-pulse canceller, the range-Doppler map, and `cfar_2d`, and its detection's
range and velocity pick the range bins the spectrogram sums.

12. **Set up the notebook.** Download the lab's bundle,
    <a href="../../bundles/L31_lab.zip" download>`L31_lab.zip`</a>, and unzip
    it into a folder of its own in your Module 4 folder. It holds the
    notebook, `L31_classify_track.ipynb`; the provided `radar_lab.py`; every
    recorded file the notebook loads, `L31_*.npz`; and the data README. Move
    `L31_sway_B.npz` into the same folder. Python with numpy, scipy,
    matplotlib, and Jupyter is the setup from the
    <a href="../L28-fmcw/index.html#frame-notebook-setup">L28 Lab's Notebook Setup</a>
    frame. Start Jupyter in the folder with `jupyter lab`, and open the
    notebook. Its first code cell names the files it loads, `RECORDS` and
    `WALK`; leave them as shipped.
13. **Run it to the angle at B.** Run the cells in order from the top. In the
    angle cell, after Procedure B, set `B_REC = "L31_sway_B.npz"` and run it.
    It prints your range and angle at B. Which side of broadside reads
    positive depends on the order of the kit's channels, so compare the sign
    with your prediction; if it is reversed, the kit's channels are the other
    way around, and you say so in the packet.

    <div class="rec" data-lab="L31">
    <label>Step 13: angle at B <input data-field="b.angleB"></label>
    </div>
14. **Task (a), the window.** Run the window cell with `N_WIN = 64`, then 16,
    then 256. Each run prints the resolution and three widths; compare the
    walker's torso line with your predicted resolution.

    <div class="rec" data-lab="L31">
    <label>Step 14, 16 chirps: torso line (Hz) <input data-field="c.16.torso"></label>
    <label>Spinner line (Hz) <input data-field="c.16.spin" data-label="Step 14, 16 chirps: spinner line (Hz)"></label>
    <label>Walker spread (m/s) <input data-field="c.16.spread" data-label="Step 14, 16 chirps: walker spread (m/s)"></label>
    <label>64 chirps: torso line (Hz) <input data-field="c.64.torso" data-label="Step 14, 64 chirps: torso line (Hz)"></label>
    <label>Spinner line (Hz) <input data-field="c.64.spin" data-label="Step 14, 64 chirps: spinner line (Hz)"></label>
    <label>Walker spread (m/s) <input data-field="c.64.spread" data-label="Step 14, 64 chirps: walker spread (m/s)"></label>
    <label>256 chirps: torso line (Hz) <input data-field="c.256.torso" data-label="Step 14, 256 chirps: torso line (Hz)"></label>
    <label>Spinner line (Hz) <input data-field="c.256.spin" data-label="Step 14, 256 chirps: spinner line (Hz)"></label>
    <label>Walker spread (m/s) <input data-field="c.256.spread" data-label="Step 14, 256 chirps: walker spread (m/s)"></label>
    </div>
15. **Task (b), one more feature.** Run the two classifier cells as they
    stand, and record the confusion matrix in Table D of the packet. Then add
    one line at the `TASK (b)` mark of `my_features` to append the band's
    edge in m/s, `x = np.append(x, edge.mean() * lam / 2)`, and run both
    again; then change it to append the shape, the spread over that edge, and
    run both again. With the shape, average the fans' fourth feature and the
    spinners' from the printout, and compare with your prediction.

    <div class="rec" data-lab="L31">
    <label>Step 15: accuracy, three features <input data-field="d.acc3"></label>
    <label>Accuracy, + edge <input data-field="d.accE" data-label="Step 15: accuracy, + edge"></label>
    <label>Accuracy, + shape <input data-field="d.accS" data-label="Step 15: accuracy, + shape"></label>
    <label>Shape, fans' mean <input data-field="d.shape.fan" data-label="Step 15: shape, fans' mean"></label>
    <label>Shape, spinners' mean <input data-field="d.shape.spin" data-label="Step 15: shape, spinners' mean"></label>
    <label>Records still called wrong <input data-field="d.wrong" data-label="Step 15: records still called wrong"></label>
    </div>
16. **Task (c), the track.** Run the tracking cell with `ALPHA = 0.5`, then
    0.2, then 0.8, then the value you would use, which writes
    `L31_track.csv`. Each run prints the detections' RMS error and the
    track's, from the walk's truth after the first second. The noise ratio is
    the track's range RMS over the detections'; compare it with your
    predicted noise ratio, and the range error at the turn with your
    predicted settled lag.

    <div class="rec" data-lab="L31">
    <label>Step 16: detections, range RMS (m) <input data-field="e.det.range"></label>
    <label>Detections, angle RMS (°) <input data-field="e.det.angle" data-label="Step 16: detections, angle RMS (°)"></label>
    <label>α 0.2: range RMS (m) <input data-field="e.02.rms" data-label="Step 16, α 0.2: range RMS (m)"></label>
    <label>Noise ratio <input data-field="e.02.ratio" data-label="Step 16, α 0.2: noise ratio"></label>
    <label>At the turn (m) <input data-field="e.02.turn" data-label="Step 16, α 0.2: range error at the turn (m)"></label>
    <label>Angle RMS (°) <input data-field="e.02.angle" data-label="Step 16, α 0.2: angle RMS (°)"></label>
    <label>α 0.5: range RMS (m) <input data-field="e.05.rms" data-label="Step 16, α 0.5: range RMS (m)"></label>
    <label>Noise ratio <input data-field="e.05.ratio" data-label="Step 16, α 0.5: noise ratio"></label>
    <label>At the turn (m) <input data-field="e.05.turn" data-label="Step 16, α 0.5: range error at the turn (m)"></label>
    <label>Angle RMS (°) <input data-field="e.05.angle" data-label="Step 16, α 0.5: angle RMS (°)"></label>
    <label>α 0.8: range RMS (m) <input data-field="e.08.rms" data-label="Step 16, α 0.8: range RMS (m)"></label>
    <label>Noise ratio <input data-field="e.08.ratio" data-label="Step 16, α 0.8: noise ratio"></label>
    <label>At the turn (m) <input data-field="e.08.turn" data-label="Step 16, α 0.8: range error at the turn (m)"></label>
    <label>Angle RMS (°) <input data-field="e.08.angle" data-label="Step 16, α 0.8: angle RMS (°)"></label>
    <label>Your α <input data-field="e.my.alpha" data-label="Step 16: your α"></label>
    <label>Range RMS (m) <input data-field="e.my.rms" data-label="Step 16, your α: range RMS (m)"></label>
    <label>At the turn (m) <input data-field="e.my.turn" data-label="Step 16, your α: range error at the turn (m)"></label>
    <label>Angle RMS (°) <input data-field="e.my.angle" data-label="Step 16, your α: angle RMS (°)"></label>
    </div>
17. **Save the notebook.** Save it with its edits and plots, and upload the
    `.ipynb` with the packet.
::::

::::{frame} No Hardware?
:class: read-only

```{note}
The whole lab can be done without a kit, in the Phaser app's browser
simulator and the notebook. Open the simulator at
[livethisdream.github.io/phaser/radar](https://livethisdream.github.io/phaser/radar/),
select **FMCW**, set **Preset** to **Range + Velocity**, turn **MTI** on at
2-pulse, and open the **Range-Doppler** view. Its **Scene** list has no fan or
spinner, so Steps 5 to 10 use **Load Recording**, which plays one of the
course's recorded files through the same view as if it were live, looping.
The files are in the lab's bundle (Step 12). They come from a simulation of the PHASER
at this preset; each target record is 2.0 s of chirps that keep 90 samples
each, so the range bins are the same 0.30 m and the view ends at 4.1 m. Mark
in the packet which rows come from recorded data.

- **Steps 5 to 8:** load `L31_fan_1.npz`, `L31_spinner_1.npz`, `L31_hand_1.npz`, and `L31_walker_1.npz` in turn, and read each. Each file's note, printed by the notebook's first code cell, gives the target's size and rate. The notebook's Procedure A cell prints the speeds from the same four files; check your readings against it.
- **Steps 9 and 10:** load `L31_dismount.npz`, a person walking at 1 m/s from A to B, turning, and walking back, past a chair at 3.2 m. Its note gives A's and B's ranges and angles, which stand in for your tape. The file keeps every 4th chirp, so the view spans $\pm 3.8\ \text{m/s}$ and each update covers 0.5 s of walking, which blurs the range; the notebook's Procedure B cell prints three 128 ms frames of it, near A going out, at the turn, and near A coming back, which fill Step 10's boxes.
- **Steps 11 and 13:** skip the burst; in Step 13 run the angle cell as shipped, on `L31_dismount.npz`. Its farthest frame is the turn at B.
- **Steps 12 to 17** run on the bundle's files with or without a kit.
```
::::

::::{frame} Your Part 2 Entries
:class: read-only

This frame collects every box you filled in on this page. Your entries stay in this
browser only, saved as you type. **Download my packet** writes them into Part 2
of the blank packet and saves the PDF; do Parts 1 and 3 on paper or in the PDF
viewer, and upload one PDF to Gradescope with the notebook. If you have already
typed Part 1 into the packet PDF, use **Fill my own copy** and choose that file
instead: your Part 1 is kept, and Part 2 is added to it. Either way the result
is locked, so finish any typing in the PDF first. Type the three confusion matrices
of Table D into the packet itself. **Export entries** saves a small
backup file you can **Import** on another laptop or after clearing your
browser. The boxes are optional: the blank packet is in the next frame, to fill
on paper or in a PDF viewer instead.

<div class="rec-summary" data-lab="L31" data-pdf="../../labs/ECE444_Lab_L31_ClassifyTrack_blank.pdf" data-file="ECE444_L31_Lab"></div>
::::

::::{frame} Lab Packet
:class: read-only doc-links

The L31 Lab packet is one submission for the whole lab, turned in complete
after the lab and before you write the final report. It has three parts:

1. Part 1, Predict (before the lab): the shaded Predicted cells of Tables A to E.
2. Part 2, Measure (your readings and the notebook's): the white Measured cells of the same tables.
3. Part 3, Analyze (after the lab): three open prompts about what you measured.

- <a class="doc-link" href="../../labs/ECE444_Lab_L31_ClassifyTrack_blank.pdf" target="_blank" rel="noopener">L31 Lab packet (PDF)</a>
::::

::::{frame} For Part 3
:class: read-only

Part 3 asks you to analyze your own Part 2 readings against your own Part 1
predictions, in three prompts: your speeds and your window widths (Tables A
and C); your three confusion matrices and the features behind them
(Table D); and your track at each $\alpha$, in range and in angle (Table E).
Keep the notebook's printouts beside you: the features of every record and
the track's errors are the evidence.
::::

::::{frame} Looking Ahead
:class: read-only

This is the last lab. The final project report explains, in your own words,
the chain the L28 to L31 Labs built, from a capture to a classified, tracked
target; its page lists what it asks for.
::::
