---
frame_view: true
---

# L31 - Classification and Tracking

::::{frame}
:class: title-frame

<div class="course-mark">ECE 444 · Fall 2026</div>

<h1 class="frame-title">Classification and Tracking</h1>

<div class="title-rule"></div>

Three numbers from a spectrogram tell a walker from a fan, and a two-gain filter holds the walker in range and angle.

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
the target is going. This lesson adds the last two stages of the chain your
[final project](../final-project/index.md) report explains. The first half
classifies a detected target from its micro-Doppler signature, which
<a href="../L26-range-resolution-doppler/index.html#frame-a-first-look-at-micro-doppler">Lesson 26</a>
introduced, and measures how often the classifier is right. The second half
joins the detections into a track in range, with an alpha-beta filter, and in
angle, with the monopulse comparison of the
<a href="../../module03/L24-lab-null-steering/index.html#frame-procedure-d-watch-it-track">L24 Lab</a>.
You will work this lesson and its lab on your own, outside class, so this
page writes out every step of the reasoning.
:::
::::

::::{frame} Micro-Doppler of a Moving Part
:::{present}
$$\begin{aligned}
f_D(t) &= \frac{2}{\lambda}\left[v_\text{body} + v_\text{part}(t)\right] \\
v_\text{part}(t) &= \Omega\rho\ \sin(\Omega t) \quad \text{(a rotor)}
\end{aligned}$$

- A walker's torso sits at $87\ \text{Hz}$, and its limbs reach $267\ \text{Hz}$ once a stride.
- A $15\ \text{cm}$ fan at $1000\ \text{rpm}$ has $7.9\ \text{m/s}$ tips, $\pm 524\ \text{Hz}$.
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
its tip. The tips move fastest, at

$$\begin{aligned}
v_\text{tip} &= \pi D\ \frac{\text{rpm}}{60} \\
&= \pi(0.15)\frac{1000}{60} = 7.9\ \text{m/s},
\end{aligned}$$

for a $15\ \text{cm}$ desk fan at $1000\ \text{rpm}$, which is
$\pm 2(7.9)/0.030 = \pm 524\ \text{Hz}$ at the course's $10\ \text{GHz}$.

A walker's arms and legs swing forward and back about the torso, once a
stride, like pendulums. L26's walker approaches at $1.3\ \text{m/s}$, so the
torso sits at $87\ \text{Hz}$, and the limbs swing up to $4.0\ \text{m/s}$, or
$267\ \text{Hz}$, on the forward stroke. The body's Doppler says how fast the
target is moving. The micro-Doppler says what is moving, which is the
property a classifier needs.
::::

::::{frame} Four Signatures
:::{present}
- The **walker** shows a torso line off zero, and its limbs swing once a stride.
- The **fan** shows a steady band to $\pm 524\ \text{Hz}$.
- The **spinner** shows steady lines at its tips, $\pm 293\ \text{Hz}$.
- The **hand** shows one trace swinging through zero.
:::
:::{present}
<img src="../../viz/img/L31-signatures.svg"
     alt="Simulated slow-time spectrograms over three seconds of the four L31 Lab targets: a walker with a torso line at 87 Hz and limb traces swinging once a second; a fan with a steady band out to plus and minus 524 Hz; a spinner with steady lines near plus and minus 293 Hz; and a hand whose single trace swings sinusoidally through zero"
     style="max-width: 520px; width: 100%; display: block; margin: 0 auto;">
:::

The L31 Lab records four targets: you walking, a desk fan, a fidget spinner,
and your hand waving. The figure simulates each one at the lesson's
$10\ \text{GHz}$, one range bin sampled once per chirp, with the spectrogram
the next frames build; the lab's $9.9\ \text{GHz}$ lowers every Doppler by 1%.

The **walker** is the only target that goes anywhere, so it is the only one
whose pattern sits off zero: the torso is the steady line at $87\ \text{Hz}$
and the limbs trace arcs above and below it, once a stride. The **fan** stays
put, so its band is centered on zero, and it is steady, because the blades
pass too often for any one of them to appear. The **spinner**, $7\ \text{cm}$
across at $1200\ \text{rpm}$, is a smaller and slower rotor, with tips at
$\pi(0.07)(20) = 4.4\ \text{m/s}$, or $293\ \text{Hz}$. Its weight sits in
three lobes near the rim rather than along a blade, and a point moving
sinusoidally spends most of its time near its extremes, so its spectrum shows
two lines near the tip speed instead of a filled band. The **hand** is one
scatterer moving back and forth. A $0.2\ \text{m}$ wave at $1.5\ \text{Hz}$
peaks at $2\pi(1.5)(0.2) = 1.9\ \text{m/s}$, or $126\ \text{Hz}$, and the
trace crosses zero twice a cycle, so the hand has no average Doppler at all.
::::

::::{frame} One Range Bin in Slow Time
:::{present}
- One sample per chirp gives $2\ \text{kHz}$, so the map spans $\pm 1\ \text{kHz}$, or $\pm 15\ \text{m/s}$.
- L26's $30\ \text{cm}$ fan at $1200\ \text{rpm}$ ($18.8\ \text{m/s}$ tips) aliases.
- A walker crosses a $0.30\ \text{m}$ bin in $0.23\ \text{s}$: sum the bins around it.
:::

<a href="../L29-range-doppler-mti/index.html">Lesson 29</a> forms the
range-Doppler map with an FFT across the chirps of a burst, one FFT for each
range bin. That FFT runs in **slow time**: one sample per chirp, from the
same range bin of each chirp's range profile. A spectrogram is the same FFT
taken over short, overlapping pieces of a longer recording instead of over
one whole burst, so each column of the spectrogram is a Doppler spectrum of a
few tens of milliseconds of the target.

The slow-time samples arrive at the PRI, $0.5\ \text{ms}$, so the sample rate
is $2\ \text{kHz}$ and the spectrogram covers $\pm 1\ \text{kHz}$, the
$\pm 15\ \text{m/s}$ that L29 calls $v_\text{max}$. A part faster than that
aliases, as in L26, and wraps to the wrong Doppler. The $30\ \text{cm}$ fan of
L26's CW demo, with tips at $18.8\ \text{m/s}$, aliases here, though it did
not in CW, where ADI's script sampled at $0.6\ \text{MHz}$. The lab fan is a
$15\ \text{cm}$ one, or a large one on its lowest setting.

Two more details make the spectrogram show the target and nothing else.
Stationary returns, the walls and the fan's own stand, sit at
$0\ \text{Hz}$ and are far stronger than the parts that move; subtracting the
mean of the slow-time samples removes them, which is what MTI does at
$0\ \text{Hz}$. And a target that moves in range leaves its bin: at
$1.3\ \text{m/s}$ a walker crosses a $0.30\ \text{m}$ bin in $0.23\ \text{s}$,
so the spectrogram of one bin shows the walker in pieces. For a walker,
`spectrogram` takes a slice of bins around the track's range and sums them,
flipping the sign of every other bin first: a Hann-windowed tone puts
$-\tfrac{1}{4}$, $\tfrac{1}{2}$, $-\tfrac{1}{4}$ of itself in neighboring
bins, so a plain sum cancels whenever the target sits on a bin center, while
the alternating sum makes the three add and reads the middle of each chirp,
where the window is 1.
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
:::{present}
$$\begin{aligned}
\Delta f &= \frac{1}{T_w} \\
\delta f &= \dot f_D\ T_w = \frac{2a}{\lambda}\ T_w \\
T_w &= \frac{1}{\sqrt{\dot f_D}} \\
&= \frac{1}{\sqrt{1131\ \text{Hz/s}}} = 30\ \text{ms}
\end{aligned}$$
:::
:::{present}
- A walker's limbs accelerate at $17\ \text{m/s}^2$, so we use $64$ chirps, $32\ \text{ms}$.
- Fan tips change at $55\ \text{kHz/s}$, so the best window is $4.3\ \text{ms}$, and no window follows a blade.
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
best window makes the two equal, $1/T_w = \dot f_D T_w$, which gives the slide's
$T_w = 1/\sqrt{\dot f_D}$. L26's walker swings its limbs $2.7\ \text{m/s}$ about the
torso, once a second, so their peak acceleration is
$2\pi(1.0)(2.7) = 17\ \text{m/s}^2$ and

$$\begin{aligned}
\dot f_D &= \frac{2(17)}{0.030} = 1131\ \text{Hz/s}, \\
T_w &= 30\ \text{ms},
\end{aligned}$$

about 59 chirps. We round up to 64 chirps, $32\ \text{ms}$, which resolves
$31\ \text{Hz}$ ($0.47\ \text{m/s}$) and smears the fastest-changing part of
the limb trace by $36\ \text{Hz}$. A 16-chirp window resolves only
$125\ \text{Hz}$; a 256-chirp window resolves $7.8\ \text{Hz}$ but smears the
limbs across $145\ \text{Hz}$. The torso, which hardly accelerates, is sharpest
in the longest window.

A fan is the opposite case. Its tips accelerate at $\Omega^2 R$, which for the
$15\ \text{cm}$ fan at $1000\ \text{rpm}$ is $822\ \text{m/s}^2$, so
$\dot f_D = 55\ \text{kHz/s}$ and the best window is $4.3\ \text{ms}$, nine
chirps, which resolves only $234\ \text{Hz}$. No window follows one blade
through its turn. A long window shows the blades' band averaged over many
passes, steady in time, and a very short one shows each blade's flash as it
passes broadside. The hop between columns, 16 chirps here, sets only how
often we compute a column, not what it resolves.
::::

::::{frame} Window Explorer
:class: viz-frame

:::{present}
<iframe src="../../viz/spectrogram-window.html"
        width="100%" height="422"
        style="border: 1px solid #cddce9; border-radius: 6px;"
        loading="lazy"
        title="Slow-time spectrogram of a walker, a fan, a spinner, or a waving hand, with the window length set from 8 to 512 chirps">
</iframe>
:::

The widget computes the spectrogram of the chosen target for a window of 8 to
512 chirps; the readout gives the window in chirps and milliseconds and the
resolution $1/T_w$, and the red bar at the top right is the window's length on
the time axis. It opens on the walker at 64 chirps. Lengthen the window and
the torso line sharpens while the limb arcs blur along time; shorten it and
the limbs follow their swing while every line thickens in Doppler. Then pick
the fan and shorten the window to 16 chirps: the band breaks into the
blades' flashes, 100 a second, since each of the three blades lies across the
line of sight twice a turn at $1000\ \text{rpm}$. The
targets are the simulated ones of the previous figure.
::::

::::{frame} Three Features
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
different classes of target, and three are enough for the lab's four targets.
Each measures a different physical property, which is why they separate
targets that any one of them alone would confuse.

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
subtract each Doppler row's mean, smooth along time over $0.1\ \text{s}$ so a
rotor's blade flashes average out, and correlate the spectrogram with a copy
of itself shifted in time, normalized so a zero shift gives 1. A stride or a
wave repeats every $0.25$ to $2\ \text{s}$; the largest correlation at those
shifts is the periodicity. A steady rotor scores near zero, and a walker or a
waving hand scores near 0.8. The provided `features` computes all three:

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
:::{present}
<img src="../../viz/img/L31-features.svg"
     alt="Twenty training trials of each target in the plane of centroid against spread: walkers spread along the centroid axis from 0.3 to 1.0 meters per second; hands, spinners and fans all sit at zero centroid, hands lowest in spread, spinners and fans overlapping between about 2 and 6 meters per second; a cross marks each class's mean"
     style="max-width: 480px; width: 100%; display: block; margin: 0 auto;">
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

The figure plots 20 simulated training trials of each target, recorded the
way the lab will record them: walkers at speeds from 0.7 to
$1.5\ \text{m/s}$ and up to $60^\circ$ off the line of sight, fans from 700
to $1200\ \text{rpm}$, spinners from 600 to $1500\ \text{rpm}$, waves of
different sizes and rates, and an SNR of 3 to $15\ \text{dB}$ a chirp. The
walkers are the only class off zero in centroid, with a mean of
$0.71\ \text{m/s}$. The hands have the least spread, $0.65\ \text{m/s}$, and
the most periodicity. The fans and spinners share zero centroid and near-zero
periodicity, so only their spread separates them, a mean of $4.9$ against
$3.7\ \text{m/s}$, and the two clouds overlap: a fast spinner looks like a
slow fan.

Thresholds work too: centroid above
$0.3\ \text{m/s}$ is a walker; otherwise, periodicity above 0.5 is a hand;
otherwise, spread above about $4.3\ \text{m/s}$ is a fan. A nearest-centroid
rule picks those boundaries from the data rather than by eye. The provided
classifier is the nearest-centroid one:

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
:::{present}
| true \ called | walker | fan | spinner | hand |
| :-- | --: | --: | --: | --: |
| walker | **20** | 0 | 0 | 0 |
| fan | 0 | **14** | 6 | 0 |
| spinner | 0 | 7 | **13** | 0 |
| hand | 0 | 0 | 0 | **20** |
:::
:::{present}
- Accuracy on unseen trials is $67/80 = 84\%$.
- Every error mistakes one rotor for the other.
:::

The **confusion matrix** counts, for each true class (a row), how many trials
the classifier called each class (a column). The diagonal holds the correct
calls, and every count off the diagonal is a specific mistake. Its
**accuracy** is the diagonal's total over all trials,

$$\text{accuracy} = \frac{20 + 14 + 13 + 20}{80} = 84\%.$$

The trials in the matrix are a second set of 20 per class, drawn the same way
as the training set but not used to train. A classifier scored on its own
training trials has already seen the answers, and its accuracy overstates
what it will do on a target it has not seen; in the lab you score it on
recordings you did not train on.

The matrix says more than the accuracy does. All 13 errors are a fan called a
spinner or a spinner called a fan, the overlap the previous figure showed,
while walkers and hands are never wrong. An 84% classifier that never misses
a person is a different instrument from one that misses people 16% of the
time, and only the matrix tells them apart. It also says what to improve: a
feature that measures tip speed better than the RMS spread does, such as the
band's edge, would address the only errors the classifier makes. Finally, the number is
an estimate. Five different draws of 80 test trials score between 80% and
91%, so with 20 trials a class report the counts, not only the percentage.
::::

::::{frame} The Alpha-Beta Filter
:::{present}
$$\begin{aligned}
\hat R_k^- &= \hat R_{k-1} + \hat v_{k-1}\ \Delta t \\
e_k &= z_k - \hat R_k^- \\
\hat R_k &= \hat R_k^- + \alpha\ e_k \\
\hat v_k &= \hat v_{k-1} + \frac{\beta}{\Delta t}\ e_k
\end{aligned}$$

- Predict, compare with the detection $z_k$, correct.
- $\Delta t = 128\ \text{ms}$, one range-Doppler frame.
- On a missed frame, the filter only predicts.
:::

A detection list is noisy. Each range is the center of a $0.30\ \text{m}$ bin,
a walker's body is larger than a bin, some frames miss the target, and
nothing in the list says that the detection at $3.1\ \text{m}$ in one frame is
the same person as the one at $3.3\ \text{m}$ in the next. A **track** joins
the detections of one target into a single estimate of its range and
velocity, frame after frame. A military radar calls a person on foot a
**dismount**; tracking one is the second half of the L31 Lab.

The **alpha-beta filter** is the simplest tracker. It assumes the target moves
at a constant velocity over one frame. Each frame it **predicts** where the
target should be, $\hat R_k^-$, from the last estimate. It compares the
prediction with the frame's detection $z_k$; the difference $e_k$ is the
**residual**. It then **corrects** both estimates by fixed fractions of the
residual: $\alpha$ of it moves the range, and $\beta/\Delta t$ of it moves the
velocity. A frame with no detection near the prediction keeps the prediction
and corrects nothing, which is how a track coasts through a miss. The
detection a track accepts is the one nearest its prediction, inside a gate of
a few bins, which is also how two targets keep separate tracks. With 256
chirps of $0.5\ \text{ms}$ back to back, one frame is $128\ \text{ms}$. The
provided `alpha_beta` is the filter as written above:

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
:::{present}
$$\beta = \frac{\alpha^2}{2-\alpha}$$

- This $\beta$ balances noise against lag.
- With $\alpha = 0.5$, the track holds $0.08\ \text{m}$ RMS and is $0.31\ \text{m}$ off at the turn.
- With $\alpha = 0.2$, it is smoother but trails the turn by $1.2\ \text{m}$.
:::
:::{present}
<img src="../../viz/img/L31-alpha-beta.svg"
     alt="Range against time for eight seconds: a walker walks out from 2 to 6.6 meters, turns, and walks back; the detections step in 0.30 meter bins around the truth; the alpha equals 0.5 track follows the truth closely through the turn, and the alpha equals 0.2 track lags it by up to 1.2 meters"
     style="max-width: 520px; width: 100%; display: block; margin: 0 auto;">
:::

The two gains set how much weight the track gives a new detection. A large $\alpha$
follows each detection closely, noise and all; a small one averages over many
frames and smooths the noise, but it is slow to notice a change in velocity,
so it lags a target that turns. The usual choice ties the two gains together,

$$\beta = \frac{\alpha^2}{2-\alpha},$$

which minimizes the track's noise and its lag together (the Benedict-Bordner
relation), and leaves one number to choose.

The figure simulates the lab's walk: out from $2\ \text{m}$ at
$1.2\ \text{m/s}$, a turn lasting a second, and back. The detections are the
centers of the $0.30\ \text{m}$ bins the walker falls in, with
$0.10\ \text{m}$ of body jitter, $0.10\ \text{m}$ RMS from the truth in all,
and 5 of the 63 frames missed. With $\alpha = 0.5$ and $\beta = 0.167$ the
track holds $0.08\ \text{m}$ RMS on the straights, better than the detections
themselves, and is off by at most $0.31\ \text{m}$ at the turn. For
steady-state noise alone, theory gives this filter $0.64$ of the detection
noise. With $\alpha = 0.2$ and $\beta = 0.022$ the track is smoother, but it
trails the turn by up to $1.2\ \text{m}$ and is still catching up on the way
back. The track's velocity is a second check: it should agree with the
Doppler velocity of the detections it accepts.
::::

::::{frame} Angle by Monopulse
:::{present}
$$\begin{aligned}
\Delta\phi &= \frac{2\pi D}{\lambda}\ \sin\theta \\
\theta &= \arcsin\frac{\lambda\ \Delta\phi}{2\pi D}
\end{aligned}$$

- Two subarray channels $D = 56\ \text{mm}$ apart give the angle in one look, with no sweep.
- Unambiguous within $\pm 15.5^\circ$ of the steer direction.
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

$672^\circ$ per unit of $\sin\theta$ at $10\ \text{GHz}$, and the second line
of the slide turns a measured phase back into an angle. A phase is known only
within $\pm 180^\circ$, so the angle is unambiguous while
$\vert\sin\theta\vert < \lambda/(2D) = 0.268$, which is $\pm 15.5^\circ$ about
the direction the array is steered. The L24 Lab's error function,

$$\frac{\text{Im}\lbrace\Delta\Sigma^*\rbrace}{\vert\Sigma\vert^2},$$

is the same comparison written for the sum and difference beams.

In the radar we take the two channels' values in the range-Doppler cell where
CFAR declared the target. That cell holds the target's echo with the 256-chirp
integration gain of L27, and none of the clutter at other ranges and
velocities, which would pull the angle toward itself. Part B therefore
records both subarray channels. Which side of broadside reads a positive angle
is a hardware-day check, as it was in L19.
::::

::::{frame} A Crossing Walker
:::{present}
- At $1\ \text{m/s}$ and $4\ \text{m}$ the walker moves $14.3^\circ/\text{s}$.
- Between sweeps the walker moves $15.9^\circ$, more than the $13.6^\circ$ beam.
- Between monopulse frames it moves $1.8^\circ$.
:::
:::{present}
:class: callout
The track's predicted angle steers the next frame's beam.
:::

A walker crossing in front of the radar at $1\ \text{m/s}$, $4\ \text{m}$
away, changes bearing at $v/R = 0.25\ \text{rad/s}$, or $14.3^\circ$ a second.
The GUI's beam sweep completes about 0.9 sweeps a second, so between two looks
the walker moves

$$\frac{14.3^\circ/\text{s}}{0.9\ \text{s}^{-1}} = 15.9^\circ,$$

more than the array's beamwidth at $10\ \text{GHz}$,

$$\theta_\text{3dB} = \frac{0.886\lambda}{Nd} = 13.6^\circ.$$

A sweep can find a walker who stands still;
it cannot hold one who crosses, because the walker can leave the beam between
one look and the next. Monopulse measures once a frame, and in
$128\ \text{ms}$ the walker moves $1.8^\circ$, well inside the $\pm 15.5^\circ$
monopulse window.

The tracker closes the loop. A second alpha-beta filter runs on the monopulse
angles, and its prediction for the next frame becomes the next frame's steer
angle, so the walker stays near boresight, where the L24 Lab found the
monopulse response straight (about $\pm 5^\circ$). Objective 4.8 asks for
exactly this integration: range from the FMCW processing, angle from the
array, and a beam the track points.

Part B needs one caution. A walker moving exactly across the line of sight has
$v_r = v\cos 90^\circ = 0$ (L26), so the torso's echo sits at
$0\ \text{Hz}$ and MTI removes it. Part B's walker takes a diagonal path, so
the range and the angle both change and the Doppler never vanishes.
::::

::::{frame} Summary
:class: read-only

| Symbol / idea | What it is | Number to remember |
| :-- | :-- | :-- |
| $f_D = 2(v_\text{body} + v_\text{part})/\lambda$ | micro-Doppler of a moving part | walker limbs to $267\ \text{Hz}$; fan tips $\pm 524\ \text{Hz}$ |
| slow time | one sample per chirp | $2\ \text{kHz}$: $\pm 1\ \text{kHz}$, $\pm 15\ \text{m/s}$ |
| $\Delta f = 1/T_w$, $\delta f = \dot f_D T_w$ | window: resolution against smear | best $T_w = 1/\sqrt{\dot f_D}$; $64$ chirps for a walker |
| centroid, spread, periodicity | three features | $\lambda\bar f/2$, $\lambda\sigma_f/2$, autocorrelation at $0.25$-$2\ \text{s}$ |
| nearest centroid | the class whose mean is nearest, in scaled features | train and test on different trials |
| confusion matrix | true class against the call | $67/80 = 84\%$; every error confuses the two rotors |
| alpha-beta | predict, residual, correct | $\alpha = 0.5$, $\beta = \alpha^2/(2-\alpha) = 0.167$ |
| monopulse | $\Delta\phi = 2\pi D\sin\theta/\lambda$ | $D = 56\ \text{mm}$; $\pm 15.5^\circ$ |
| crossing walker | beam sweep against monopulse | $15.9^\circ$ a sweep, $1.8^\circ$ a frame |
::::

::::{frame} L31 Lab: Micro-Doppler Classification and Dismount Tracking
:::{present}
- Read four targets' micro-Doppler in the app's Range-Doppler view.
- Watch a walker cross on a diagonal; save one burst on mark B with both channels.
- In the notebook: tune the window, add a feature, tune $\alpha$.
:::

The L31 Lab is the last stage of the chain your
[final project](../final-project/index.md) report explains. It starts in the
Phaser app: in **Procedure A** you read the micro-Doppler of a fan, a fidget
spinner, a waving hand, and yourself walking in the Range-Doppler view; in
**Procedure B** you walk in front of the kit on a diagonal and back, read the
walk in the same view, and save one burst on the far mark with both subarray
channels, which gives the sign of the angle. The rest runs in the lab's
notebook, which calls the provided `radar_lab.py`: it finds each target with
the L30 detector, computes its spectrogram and features, classifies every
record with a classifier trained on the others, and tracks a walk in range and
angle. Your tasks are small changes to it: tune the spectrogram window, add
one feature and see whether the confusion matrix improves, and tune $\alpha$
against the walk's truth. You work the lab on your own, outside class, and
turn in one packet in three parts: **Part 1, Pre-Lab**, the predictions;
**Part 2, Measurements**, from the app and the notebook; and **Part 3,
Writeup**. I check the packet and return it with feedback. It is scaffolding
for your final report, not the report.

The app's **Save Capture** keeps one burst, 256 chirps or 128 ms. That is
too short to hold a stride, which lasts about a second, or a turn, so the
notebook classifies the course's 2 s records and tracks the course's recorded
walk, with or without a kit. The recorded walk also carries its truth, which
is what scores a track.

ADI's Phaser labs stop at CFAR, so this lab is the course's own. Its settings
are the app's **Range + Velocity** preset: 300 µs chirps of 500 MHz, one every
0.5 ms, at 9.9 GHz, so $\lambda = 3.03\ \text{cm}$ and the slow-time
spectrogram spans $\pm 1\ \text{kHz}$, or $\pm 15.2\ \text{m/s}$. Each Doppler
is 1% below the lesson's round 10 GHz values.
::::

::::{frame} Pre-Lab Predictions
:::{present}
| Target | Largest speed | Doppler |
| :-- | --: | --: |
| Walker | limbs $4.0\ \text{m/s}$ | $264\ \text{Hz}$ |
| Fan, $1000\ \text{rpm}$ | $\pm 7.9\ \text{m/s}$ | $\pm 518\ \text{Hz}$ |
| Spinner, $1200\ \text{rpm}$ | $\pm 4.4\ \text{m/s}$ | $\pm 290\ \text{Hz}$ |
| Hand, $1.5\ \text{Hz}$ | $\pm 1.9\ \text{m/s}$ | $\pm 124\ \text{Hz}$ |
:::

The table is the core of Part 1, from the lesson's Micro-Doppler frame, for
the lesson's targets: a $15\ \text{cm}$ fan and a $7\ \text{cm}$ spinner,
whose tips move at $\pi D\ \text{rpm}/60$; a hand waving $0.2\ \text{m}$
each way, which peaks at $2\pi f A$; and a walker whose limbs swing up to
$2.7\ \text{m/s}$ about a torso closing at $1.3\ \text{m/s}$. Doppler is $2v/\lambda$ with
$\lambda = 3.03\ \text{cm}$. Use your own fan's diameter and speed setting,
and your own walk, in place of these.

Part 1 also predicts two things the bench checks. A rotor held off edge-on
shows only $\cos\psi$ of its tip speed, where $\psi$ is the tilt, so a fan
turned $45^\circ$ reads like a fast spinner; a feature that measures the
shape of the band, rather than its width, is unaffected by the tilt. And
the walk of Procedure B turns at B: the torso's radial speed passes through
zero there, so the 2-pulse canceller cuts it, and the predict step of the
alpha-beta filter carries the track through the turn. Pre-Lab Question 4
predicts how far each $\alpha$ trails the turn.
::::

::::{frame} Bench Rules
:::{present}
- Connect the transmit antenna to **OUT2** before you power the kit.
- Hold rotors edge-on, and keep your fingers clear of the fan.
- Walkers agree on a lane, because other cadets in your beam are targets.
:::

A rotor shows micro-Doppler only where its parts move along the line of
sight, so hold the fan and the spinner edge-on, with the plane they turn in
pointing at the array. Face-on, the blades cross the beam and show almost
nothing. Use a fan with a guard, keep your fingers out of it, and stand to
the side while you read it; your own breathing and fidgeting are targets too.

Every cadet has a kit, so every beam crosses someone. For Procedure B you
need about 4.5 m of clear floor in front of the kit and a lane no one else
walks through while you walk it. Walk at a steady pace you can repeat, about
1 m/s. No step needs a corner reflector.
::::

::::{frame} Results
:::{present}
- Your confusion matrices, before and after your feature.
- Your track, the $\alpha$ you chose, and why.
- Everything from the L28 to L31 Labs, for the report.
:::

This is the last lab, so what you keep is the material for the final report,
not for a next lab. From this lab, keep three results: the confusion matrix
and accuracy with three features and with yours, with your explanation of
which records were wrong and why; the track in range and angle against the
truth, with the $\alpha$ you chose and the noise and lag that come with it; and your
Procedure A readings of the four targets against your predictions. The report
asks you to explain, in your own words, how your radar decides what a target
is and where it is going. Keep this notebook, `L31_track.csv`, your burst from
mark B, and `radar_lab.py` with the L28 to L30 work.
::::

::::{frame} Equipment and Setup
:class: read-only

You need:

- the ADALM-PHASER kit with its Raspberry Pi and Pluto attached, and its transmit antenna;
- a desk fan with a guard, 15 cm across or a larger one on its lowest setting, and a fidget spinner;
- a tape measure, masking tape, and about 4.5 m of clear floor in front of the kit;
- your laptop, on the kit's network for the Phaser app, with the lab's bundle unzipped as the Notebook Setup frame below describes.

1. With the kit powered off, connect the transmit antenna to **OUT2**.
2. Power the kit, open the Phaser app, and select **FMCW**. Set **Preset** to **Range + Velocity**.
3. Set the 0 m frequency for this preset with **Calibrate…**, as in the L28 Lab, so that **0 m Beat (kHz)** holds your kit's value.
4. Turn **MTI** on, with **MTI Mode** at 2-pulse, open the **Range-Doppler** view, and press **Start**. The FMCW mode holds the beam at broadside, $0^\circ$. The view's readouts give the **Peak Range** and **Peak Velocity** of its strongest cell.
::::

::::{frame} No Hardware?
:class: read-only

```{note}
The whole lab can be done without a kit, in the Phaser app's browser
simulator and the notebook. Open the simulator at
[livethisdream.github.io/phaser/radar](https://livethisdream.github.io/phaser/radar/),
select **FMCW**, set **Preset** to **Range + Velocity**, turn **MTI** on at
2-pulse, and open the **Range-Doppler** view. Its **Scene** list (`static`,
`corners`, `walker`, `hand`) shows a live hand and walker, but it has no fan
or spinner, so every procedure below uses **Load Recording**, which plays one
of the course's recorded files through the same view as if it were live,
looping. The files are in the lab's bundle (Notebook Setup, below). They come
from a simulation of the PHASER at this preset, with a kit whose 0 m frequency
is 101.4 kHz. Each target record is 2.0 s of back-to-back chirps; to keep the
files small, each chirp keeps 90 samples, so the range bins are the same
0.30 m and the view ends at 4.1 m. Say in your packet which results are
recorded rather than your own.

- **Procedure A**, four targets: load `L31_walker_1.npz`, `L31_fan_1.npz`, `L31_spinner_1.npz`, and `L31_hand_1.npz` in turn, and read each as Procedure A says. The notebook's Procedure A cell prints the speeds the key uses, from the same four files, so check your readings against it. This fills Table A.
- **Procedure B**, the crossing walker: load `L31_dismount.npz`, a person walking at 1 m/s from A, 1.5 m out and $12^\circ$ to the E1 side, to B, 4.0 m out and $10^\circ$ to the E8 side, turning, and walking back, past a chair at 3.2 m. A and B are the tape marks of Table B. The file keeps every 4th chirp, so the view spans $\pm 3.8\ \text{m/s}$ and each of its updates covers 0.5 s of walking, which blurs the range; the notebook's Procedure B cell prints three 128 ms frames of it, which fill Table B's rows. The angle at B is the notebook's angle cell, run as shipped on this file; it is the angle task (c)'s plot shows at the turn, and + is the E8 side.
- **Procedure C**, the notebook's tasks: these run on the bundle's files with or without a kit. Table C comes from the notes the first code cell prints.
```
::::

::::{frame} Procedure A: Four Targets
:class: read-only

For each target, watch the Range-Doppler view for a few seconds, and read the
largest speed its pattern reaches on each side of 0 m/s from the velocity
axis. Record your prediction, the two speeds read, and whether the pattern is
centered on 0 m/s in Table A. You save nothing here: a saved
burst is 128 ms, and the classifier needs records of 2 s.

1. **Fan.** Set the fan about 1 m in front of the kit, edge-on, on a setting you can name. Measure its diameter, and predict its tip speed from the diameter and the setting's rpm. Read and record it. Then turn it about $45^\circ$ off edge-on and watch the band narrow, and face-on, where it nearly disappears.
2. **Spinner.** Spin the fidget spinner and hold it edge-on about 0.5 m out, steady. Read and record it. Estimate the spin from how long it runs, or use the lesson's 1200 rpm.
3. **Hand.** Wave your hand toward and away from the kit, about 0.2 m each way, about 1.5 times a second, at 0.8 m. Read and record it.
4. **Walker.** Set the laptop beside the kit, its screen toward you, and walk straight toward the kit from 4 m at a normal pace, watching the view as you come. Read and record the torso's speed, the strongest line off zero, and the largest speed of the limbs.
::::

::::{frame} Procedure B: A Crossing Walker
:class: read-only

1. Facing the patches, E1 is on your right. Tape mark **A** on the floor 1.47 m straight out from the array and 0.31 m to the E1 side, and mark **B** 3.94 m out and 0.69 m to the E8 side. Measure each mark's range and angle from the array's center, and record both in Table B. The angles are within the monopulse window, $\pm 15.7^\circ$ at 9.9 GHz (the lesson's $\pm 15.5^\circ$ at 10 GHz).
2. With MTI on, walk from A to B at about 1 m/s, turn at B, and walk back to A. Read the walker's range and velocity just after A, at B, and just before A on the way back, and record them in Table B. Walking out, your back is to the screen: have a partner read the view, or start a screen recording on the laptop, walk, and read the three moments from the recording afterwards.
3. Stand on mark B and sway, shifting your weight toward and away from the kit, because the canceller removes a person standing still. Turn **Subarray Channels** on and press **Save Capture**. The app downloads one burst with both channels, `phaser_range_doppler_<date>-<time>.npz`; rename it `L31_sway_B.npz` and move it into the notebook's folder.
4. In the notebook, set `B_REC = "L31_sway_B.npz"` in the angle cell after Procedure B, and run it. It prints the range and angle of your detection; record the sign in Table B. Which side of broadside reads positive depends on the kit's channel order.
::::

::::{frame} Notebook Setup
:class: read-only

Download the lab's bundle, <a href="../../bundles/L31_lab.zip" download>`L31_lab.zip`</a>, and unzip it into a folder of its own in your Module 4 folder. It holds the notebook, `L31_classify_track.ipynb`; the provided `radar_lab.py`; every recorded file the notebook loads, `L31_*.npz`; and the data README. Python with numpy, scipy, matplotlib, and Jupyter is the setup from the <a href="../L28-fmcw/index.html#frame-notebook-setup">L28 Lab's Notebook Setup</a> frame. Start Jupyter in the unzipped folder with `jupyter lab`, and open `L31_classify_track.ipynb`.
::::

::::{frame} Procedure C: Run the Notebook
:class: read-only

Do this part after the bench, in about 30 to 45 minutes. The notebook's first code cell names the files it loads, `RECORDS` and `WALK`; leave them as shipped. Its Procedure A and B cells print the numbers the No Hardware? frame uses; with a kit, they still run, and the angle cell takes your burst from mark B. Each record's target is found by the L30 chain, run on the record's first burst: the 2-pulse canceller, the range-Doppler map, and `cfar_2d`; its detection's range and velocity pick the range bins the spectrogram sums.

1. Run the first code cell. It prints each record's note: copy the setting, the tilt or the pace, and the range of each into Table C.
2. **Task (a):** run the window cell with `N_WIN = 64`, then `16`, then `256`. Record the resolution and the three widths in Table D, and compare the plots.
3. **Task (b):** run the two classifier cells as they stand. Then add one line to `my_features` to append the band's edge, and run both again; then change it to append the band's shape, the spread over the edge, and run both again. Record the three confusion matrices and accuracies in Table E.
4. **Task (c):** run the tracking cell with `ALPHA = 0.5`, then `0.2`, then `0.8`, on the recorded walk, whose truth scores the track. Record each row in Table F. Then set `ALPHA` to the value you would use and run it once more; it writes `L31_track.csv`.
5. Save the notebook with its edits and plots, and upload the `.ipynb` with the packet.

Each task's markdown cell states the result to check against. Anything you do beyond the three tasks belongs in your report's Extra Effort.
::::

::::{frame} Lab Packet
:class: read-only doc-links

- <a class="doc-link" href="../../labs/ECE444_Lab_L31_ClassifyTrack_blank.pdf" target="_blank" rel="noopener">L31 Lab packet (PDF)</a>
::::
