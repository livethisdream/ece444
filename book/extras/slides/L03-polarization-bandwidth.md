<!-- .slide: class="title-slide" -->

<div class="title-left">

# ECE 444

Antennas, Phased Arrays, and Radar Systems

## Lesson 3 — Polarization and Bandwidth

Fall 2026 · Dr. Neil Rogers

</div>

<div class="title-right">

![USAFA](./img/01-course-intro/USAFA-logo.png)

</div>

---

## Where we were

- L2: parameters that describe **where** and **how well** an antenna radiates
- Gain, directivity, effective area, HPBW, sidelobes
- Reflection coefficient Γ and VSWR at the antenna terminals

Today: **which way** does the E-field point, and **over what range of frequencies** does the antenna work.

Note:
One-minute recap. L2 was about *magnitude* and *shape* of the radiated
field. L3 is about *direction of E* and *frequency coverage*.

---

## Today's plan

1. **Polarization** — direction the E-field traces at a point
2. **Axial ratio & polarization loss factor** — how much power actually couples
3. **Bandwidth** — impedance, pattern, polarization; fractional and ratio BW
4. **Chu-Harrington** — why small antennas are narrowband

<div class="callout">
Polarization and bandwidth are the two most misquoted specs on a datasheet.
</div>

---

## What polarization is

Fix a point in space. Watch $\mathbf{E}(t)$ trace a curve over one period.

<div class="fig" data-inline-svg="./fig/L03-pol-states.svg" style="max-width:570px; margin:0 auto;"></div>

<div class="callout">
That curve <strong>is</strong> the polarization.
</div>

A receive antenna only picks up the component of $\mathbf{E}$ **aligned with its own polarization**. Everything else is discarded.

---

## Building any polarization from two linear components

<div class="two-col"><div class="col-text">
$$\mathbf{E}(z, t) = \hat{x} E_{x} \cos(\omega t - k z) + \hat{y} E_{y} \cos(\omega t - k z + \delta)$$
<p>Three knobs: $E_{x}$, $E_{y}$, and relative phase $\delta$.</p>
<ul>
<li>$\delta = 0$, equal amplitudes → <strong>linear</strong> at 45°</li>
<li>$\delta = -90^{\circ}$, equal amplitudes → <strong>right-hand</strong> circular</li>
<li>$\delta = +90^{\circ}$, equal amplitudes → <strong>left-hand</strong> circular</li>
<li>Everything else → <strong>elliptical</strong></li>
</ul>
</div><div class="col-fig">
<div data-inline-svg="./fig/L03-pol-construction.svg" style="max-width:330px; margin:0 auto;"></div>
</div></div>

Note:
Draw the three cases on the chalkboard. Two orthogonal linear
components + a phase difference → *any* polarization state.

---

## Right or left hand?

<div class="two-col"><div class="col-text">
<p><strong>IEEE convention</strong> — point your right thumb along the direction of propagation.</p>
<ul>
<li>Fingers curl the way E rotates → <strong>right-hand</strong> polarization</li>
<li>Otherwise → <strong>left-hand</strong> polarization</li>
</ul>
</div><div class="col-fig">
<div data-inline-svg="./fig/L03-handedness.svg"></div>
</div></div>

<div class="callout">
Two identical CP antennas of <em>opposite sense</em> receive zero from each other.
Sense mismatch is a real design bug.
<em>(Ideal CP — we price the real number at the end of the hour.)</em>
</div>

---

## Axial ratio

<div class="two-col"><div class="col-text">
<p>For the general ellipse:</p>
$$\text{AR} = \frac{|E_{\text{maj}}|}{|E_{\text{min}}|} \ge 1$$
<p>$\text{AR}_{\text{dB}} = 20 \log_{10}(\text{AR})$</p>
<ul>
<li>$\text{AR} = 1$ (0 dB) → pure <strong>circular</strong></li>
<li>$\text{AR} = \infty$ ($\infty$ dB) → pure <strong>linear</strong></li>
<li>Real CP antennas: <strong>AR ≤ 3 dB</strong> across the band</li>
</ul>
</div><div class="col-fig">
<div data-inline-svg="./fig/L03-axial-ratio.svg" style="max-width:330px; margin:0 auto;"></div>
</div></div>

Note:
"3 dB axial ratio" is the industry-standard CP spec. Say what it does and
does not buy: at AR = 3 dB the received power swings over a 3 dB range with
orientation (−1.8 to −4.8 dB against a linear antenna); we price it exactly
later this hour. The 3 dB is the peak-to-null swing, not a ceiling on loss.

---

## Example — name that polarization

$$\mathbf{E} = \hat{x} 3\cos(\omega t - kz) + \hat{y} \cos(\omega t - kz - 90^{\circ})$$

Read off the three numbers: $E_{x} = 3$, $E_{y} = 1$, $\delta = -90^{\circ}$.

- $\delta = -90^{\circ}$ → **right-hand**
- $E_{x} \ne E_{y}$ → **elliptical**, axes on $\hat{x}$ / $\hat{y}$

$$\text{AR} = \frac{3}{1} = 3 \quad \rightarrow \quad \text{AR}\_{\text{dB}} = 20 \log_{10} 3 \approx 9.5 \text{ dB}$$

<div class="callout">
Right-hand elliptical — and it misses an AR ≤ 3 dB spec badly. At 9.5 dB this is far closer to linear than to circular.
</div>

Note:
Work it in the order they should use on an exam: phase sign first
(handedness), then the amplitudes (shape), then the ratio (how close to
circular). The polarization playground on the lesson page animates this
exact case — drop Ey to 1 and set the phase to -90.

---

## Polarization loss factor

<div class="two-col"><div class="col-text">
$$\text{PLF} = |\hat{\rho}_{\text{w}} \cdot \hat{\rho}_{\text{a}}^{*}|^{2}$$
<p>Fraction of incident power an antenna captures given a polarization mismatch.</p>
</div><div class="col-fig">
<div data-inline-svg="./fig/L03-plf-cos2.svg" style="max-width:87%; margin:0 auto;"></div>
<small>Two linear antennas, tilted by $\psi$.</small>
</div></div>

<div class="callout">
Unit vectors are <em>complex</em> when either wave is not purely linear —
that dot product silently carries the phase between $E_{x}$ and $E_{y}$.
</div>

Note:
The tilt between two linear antennas is $\psi$, never $\theta$ — $\theta$ is
the polar angle and it stays booked for the pattern. Same letter, two
meanings, is how a homework problem goes wrong.

---

## PLF cheat sheet

| Wave | Antenna | PLF | dB |
| :--- | :--- | :---: | :---: |
| Linear ($\hat{x}$) | Linear ($\hat{x}$) | 1 | 0 |
| Linear ($\hat{x}$) | Linear ($\hat{y}$) | 0 | $-\infty$ |
| Linear | RHCP or LHCP | 0.5 | $-3$ |
| RHCP | RHCP | 1 | 0 |
| RHCP | LHCP | 0 | $-\infty$ |

Two linear antennas tilted by $\psi$: $\text{PLF} = \cos^{2}\psi$.

Note:
Memorize this table. Every polarization problem on a homework or an
exam reduces to it plus the $\cos^{2}\psi$ rule for linear-linear.

---

<!-- .slide: class="viz-cue-slide" -->

## Example — how much power do you lose?

**(a)** GPS satellite transmits RHCP, your receiver is a linear whip:

$$\text{PLF} = |\hat{\rho}\_{\text{w}} \cdot \hat{\rho}\_{\text{a}}^{*}|^{2} = 0.5 \quad \rightarrow \quad -3 \text{ dB}$$

Half the power is gone no matter how you turn the whip — the price of rotation immunity.

**(b)** Both ends linear: base dipole vertical, handheld tilted by $\psi = 30^{\circ}$:

$$\text{PLF} = \cos^{2}(30^{\circ}) = 0.75 \quad \rightarrow \quad -1.25 \text{ dB}$$

<div class="callout">
Tilt that handheld all the way to horizontal and $\cos^{2}(90^{\circ}) = 0$ — in theory the link dies.
</div>

<p class="viz-cue">↗ Interactive on the lesson page</p>

Note:
DEMO HERE — run demos/antenna_link on a Pluto and rotate the receive
antenna while the class watches received power track cos^2(psi). That is
part (b) live, and it is the reason the backend forces manual gain: AGC
would quietly claw the loss back and kill the point. Use --sim if there is
no hardware in the room. The lesson-page widget runs the same sweep if the
hardware is not in the room.

Ask why (b) never actually reaches zero on the screen: multipath scatters
energy back into the orthogonal polarization, so a real null bottoms out
around -20 dB.

---

## Why sat and GPS links use CP

<div class="two-col fig-wide"><div class="col-text">
<p><strong>Faraday rotation</strong> in the ionosphere turns a linear wave's polarization through an angle you cannot predict.</p>
<ul>
<li>Linear TX + linear RX → unpredictable fading</li>
<li>Linear TX + CP RX → fixed 3 dB penalty, no fading</li>
<li>CP TX + CP RX, same sense → 0 dB penalty, no fading</li>
</ul>
<p>Same argument wherever the receiver's orientation is not fixed: <strong>cubesats, handhelds, aircraft.</strong></p>
</div><div class="col-fig">
<div data-inline-svg="./fig/L03-faraday-rotation.svg" style="max-width:98%; margin:0 auto;"></div>
</div></div>

Note:
The trade is certainty, not power. CP does not recover the lost half —
it converts a random, deep, time-varying loss into a fixed one you can
put in a link budget.

---

## An antenna has multiple bandwidths

<div class="two-col"><div class="col-text">
<ul>
<li><strong>Impedance bandwidth</strong> — VSWR ≤ 2. The most common definition.</li>
<li><strong>Pattern bandwidth</strong> — beamwidth and sidelobes stay in spec.</li>
<li><strong>Polarization bandwidth</strong> — AR stays under ~3 dB.</li>
</ul>
<div class="callout">
They need not coincide. A patch often holds CP over a much narrower
band than it stays matched.
</div>
</div><div class="col-fig">
<div data-inline-svg="./fig/L03-bandwidth-intersection.svg" style="max-width:95%; margin:0 auto;"></div>
</div></div>

Note:
Point at the shaded strip. You do not get to pick which bandwidth you
live in — the antenna hands you the intersection, and the datasheet
almost never plots it.

---

## Impedance bandwidth — what "VSWR ≤ 2" means

<div class="two-col"><div class="col-text">
$$\text{VSWR} = 2 \Longleftrightarrow |\Gamma| = 1/3 \Longleftrightarrow \text{RL} = 9.5\ \text{dB}$$
<p>Reflected power: $|\Gamma|^{2} = 11\%$. Transmitted: $89\%$.</p>
<div class="callout">
"VSWR ≤ 2:1" is the industry-standard bar. Some radar specs push to
1.5:1 or lower; some consumer parts relax to 3:1.
</div>
</div><div class="col-fig">
<div data-inline-svg="./fig/L02-vswr.svg" style="max-width:95%; margin:0 auto;"></div>
</div></div>

---

## Fractional and ratio bandwidth

$$\text{FBW} = \frac{f_{H} - f_{L}}{f_{c}}, \qquad \text{RBW} = \frac{f_{H}}{f_{L}}$$

Rough categories:

- **Narrowband**: FBW ≲ 5% (patches, small loops)
- **Broadband**: FBW 5 – 50% (dipoles, slots, horns)
- **UWB**: RBW ≥ 2:1, i.e. FBW ≥ 67% (log-periodic, spiral, Vivaldi)

100 MHz means different things at 500 MHz and 50 GHz — **always report as a fraction.**

---

## Bandwidth is limited by size

<div class="two-col"><div class="col-text">
<p><strong>Chu-Harrington bound</strong> — antenna inside a sphere of radius $a$:</p>
$$Q \gtrsim \frac{1}{(k a)^{3}} + \frac{1}{k a}, \qquad \text{FBW} \approx \frac{1}{Q}$$
<p>Half-power form; at the VSWR ≤ 2 bar, $\text{FBW} \approx 0.71/Q$. Beat the bound with <strong>loss</strong> — and pay in gain.</p>
<div class="callout">
Small $ka$ → high Q → narrow BW. There is no free lunch.
</div>
</div><div class="col-fig">
<div data-inline-svg="./fig/L03-chu-q-vs-ka.svg" style="max-width:95%; margin:0 auto;"></div>
</div></div>

Note:
Intuition: cramming a resonator into a small volume forces a high
stored-energy-to-radiated-power ratio. That's exactly Q.

---

## What the current does at the end

<div class="fig" data-inline-svg="./fig/L03-antenna-classes.svg" style="max-width:1040px; margin:0 auto;"></div>

<div class="callout">
Reflection makes a resonance. A resonance is a <strong>narrow band</strong>.
</div>

Note:
Walk the three panels left to right and let the picture do the talking.
Panel 1: the reflected current adds to the outgoing current and only
survives if the length fits — that is a resonance. Panel 2: kill the
reflection and there is nothing to be sharp about. Panel 3: the structure
hands a different section to each frequency.

---

## Three classes, three bandwidths

- **Resonant** — the current reflects, so the length has to fit. One resonance → **one narrow band**.
- **Traveling-wave** — the current radiates away or dies in a **termination** before it returns. No standing wave, no sharp resonance → **wide**.
- **Self-scaling** — a scaled copy of itself, with a different section active at each frequency → **very wide**.

| Resonant | Traveling-wave | Self-scaling |
| :--- | :--- | :--- |
| patch, dipole, slot | Vivaldi, helix, terminated long wire | log-periodic, spiral |

Note:
Watch the word "resonant" — in L4 it comes back meaning the frequency
where X_in = 0. Same idea seen from the terminals: a resonant structure
is one you operate at that frequency, which is why it is narrowband.

If they ask about the termination: yes, the power dumped in that
resistor is wasted, so a terminated traveling-wave antenna trades
efficiency for bandwidth. Same trade as the resistive loading on the
Chu-Harrington slide.

---

## Bandwidth by Antenna Type

| Antenna | Typical FBW | Application |
| :--- | :---: | :--- |
| Patch | 1 – 5% | GPS, tags — resonant |
| Slot | 5 – 10% | Aircraft skins |
| Dipole (λ/2) | 8 – 15% | Broadcast, generic |
| Horn | 30 – 50% | Test ranges |
| Log-periodic | 10:1 RBW | Broadband probing |
| Spiral | 10:1+ RBW | EW, DF |
| Vivaldi / TSA | 10:1+ RBW | UWB radar, arrays |

<div class="callout">
Resonant → narrow.<br>
Traveling-wave and self-scaling → wide.
</div>

---

## Tradeoffs

- **Narrow BW ⇔ high gain, small size.** Every knob fights.
- **Wideband** antennas usually pay in **gain**, **volume**, or **CP purity**.
- **Small** antennas (IoT, wearables) pay in **BW** by Chu-Harrington.

Every real design is picking two of {gain, size, bandwidth} and letting the third suffer.

---

## Back to the datasheet

I opened with a claim: polarization and bandwidth are the **two most misquoted specs**. Here is the evidence.

- **Polarization** — the *sense* depends on whose convention, and "circular" gets sold at 3 – 6 dB axial ratio
- **Bandwidth** — the number quoted is almost always the *widest* of three different bandwidths

<div class="callout">
None of these are lies. Each is a defensible reading of a real measurement —
which is exactly why they survive to the design review.
</div>

Note:
This is the payoff for the callout on the "Today's plan" slide — I promised
it at the top of the hour, so cash it out here. The goal is that they leave
able to *interrogate* a datasheet, not just read one.

---

## "RHCP" — according to whom?

- **IEEE convention** — observer looks **along** the direction of propagation (wave travels away from you)
- **Optics / physics convention** — observer looks **toward** the source (wave comes at you)

Same physical wave. **Opposite name.**

<div class="callout">
An optics-convention "RHCP" part is IEEE <strong>LHCP</strong>. Order its mate and you have
built a sense mismatch — the one polarization error that costs you the entire link.
</div>

Note:
This is not a hypothetical. Optics-trained vendors and some older European
sources use the receiver-looking-back convention. The fix is procedural:
on any CP datasheet, confirm the convention *before* you order the other end.
Ask which way the observer is facing.

---

## "Circularly polarized" — at what axial ratio?

A nominally CP antenna of axial ratio $A$ (linear, $\ge 1$) meets a **linear** antenna. Sweep the linear antenna's orientation; captured power runs between

$$p_{\max} = \frac{A^{2}}{A^{2}+1} \qquad p_{\min} = \frac{1}{A^{2}+1}$$

These are the powers in the major and minor axes, so $p_{\max} + p_{\min} = 1$, and their ratio is

$$\frac{p_{\max}}{p_{\min}} = A^{2} \quad\Longrightarrow\quad 10\log_{10}\left(\frac{p_{\max}}{p_{\min}}\right) = 20\log_{10} A = \text{AR}\_{\text{dB}}$$

<div class="callout">
The peak-to-null swing in received power, in dB, <strong>equals the axial ratio in dB.</strong>
</div>

Note:
Exact, not a rule of thumb. It is the same fact as the practice problem where
two orthogonal linear receivers differ by the axial ratio — this is just the
swept-orientation version of it. Worth putting on the board.

---

## What 3 dB of axial ratio actually costs

| Actual AR | Loss to a linear antenna | Worst-case opposite-sense rejection |
| :---: | :---: | :---: |
| 0 dB (ideal CP) | −3.0 dB, flat | $-\infty$ |
| **3 dB** (the industry bar) | −1.8 to −4.8 dB | **−9.6 dB** |
| 6 dB ("still circular") | −1.0 to −7.0 dB | **−4.5 dB** |

Rejection worst case (major axes aligned) is $\left[\dfrac{A^{2}-1}{A^{2}+1}\right]^{2}$.

<div class="callout">
Earlier I said opposite-sense CP antennas receive <em>zero</em> from each other.
At 3 dB axial ratio that rejection is only about <strong>10 dB</strong>.
</div>

Note:
Land the callback deliberately — they wrote down "zero" an hour ago. The
idealization was fine for teaching the concept and useless for budgeting a
link. At 6 dB AR the cross-pol rejection is 4.5 dB, which is essentially
no isolation at all.

---

## "4% bandwidth" — of what?

- The quoted number is nearly always **impedance** BW (VSWR ≤ 2) — the **widest** of the three
- **Pattern** BW and **axial-ratio** BW are narrower, and usually go unquoted
- Axial ratio is typically specified **at boresight only**, and degrades off-axis

<div class="callout">
The usable band is the <strong>intersection</strong>, not the headline.
A CP patch matched over 4% may hold AR ≤ 3 dB over barely 1% — and only near boresight.
</div>

Note:
Tie back to the "multiple bandwidths" slide. The point is not that vendors
are dishonest; it is that "bandwidth" is underspecified until you say
*which* bandwidth, *at what threshold*, and *over what scan angle*.

---

## Key point

<div class="callout">
Polarization decides <strong>how much of the wave your antenna can even see</strong>, and
bandwidth decides <strong>where it still behaves</strong>. Both are quoted as one number and
neither is one number: ask <em>at what axial ratio</em>, and <em>which bandwidth, at what
threshold, over what scan angle</em>.
</div>

---

## Where this is going

<figure class="qr qr-right">
  <img src="./img/syllabus-qr.png" alt="QR to syllabus">
  <figcaption>Syllabus</figcaption>
</figure>

Reading:

- Balanis or Milligan chapter on **input impedance and matching**
- R&S *Antenna Basics*, sections on feed lines and baluns

<div class="callout">

Next lesson: **impedance, feeding, and baluns** — the transmission-line side of the antenna terminals.

</div>
