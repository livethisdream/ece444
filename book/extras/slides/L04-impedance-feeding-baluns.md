<!-- .slide: class="title-slide" -->

<div class="title-left">

# ECE 444

Antennas, Phased Arrays, and Radar Systems

## Lesson 4 — Impedance, Feeding, and Baluns

Fall 2026 · Dr. Neil Rogers

</div>

<div class="title-right">

![USAFA](./img/01-course-intro/USAFA-logo.png)

</div>

---

## Where we were

- L2: **what an antenna radiates** — gain, directivity, effective area
- L3: **which way** the E-field points, and **over what band** the antenna works
- We kept meeting Γ and VSWR at the terminals

Today: the **other side of the terminals** — what the antenna looks like to the *radio*.

Note:
Everything so far has been about the radiated field. Today we turn around and
look into the feed terminals. Before any power radiates, it has to get *onto*
the antenna — an impedance problem.

---

## Today's plan

1. **Input impedance** — $Z_\text{in} = R_\text{rad} + R_\text{loss} + jX$
2. **Feeding** — the reflection the source sees: $\Gamma$, VSWR, mismatch loss
3. **Matching** — quarter-wave transformer and the L-match
4. **Baluns** — balanced antenna, unbalanced coax, and the current on the shield

---

## The antenna is a one-port

At its terminals, at one frequency, the antenna is just a complex impedance:

$$ Z_\text{in} = R_\text{in} + jX_\text{in}, \qquad R_\text{in} = R_\text{rad} + R_\text{loss} $$

Drive it with current $I_0$:

$$ P_\text{in} = \tfrac{1}{2}|I_0|^2 R_\text{in} = \underbrace{\tfrac{1}{2}|I_0|^2 R_\text{rad}}\_{P_\text{rad}} + \underbrace{\tfrac{1}{2}|I_0|^2 R_\text{loss}}\_{P_\text{loss}} $$

Note:
Radiation resistance and loss resistance carry the two fates of the input power:
radiated away, or lost as heat.

---

## Radiation resistance is not a resistor

<div class="fig" data-inline-svg="./fig/L04-zin-split.svg" style="max-width:760px; margin:0 auto;"></div>

- **$R_\text{rad}$** — the equivalent resistance for power carried away as radiation. The *useful* part.
- **$R_\text{loss}$** — real ohmic/dielectric loss. Becomes heat.

<div class="callout">
This split <em>is</em> the radiation efficiency from L2: &nbsp; $\eta_\text{rad}=\dfrac{R_\text{rad}}{R_\text{rad}+R_\text{loss}}$, &nbsp; $G=\eta_\text{rad}D$.
</div>

Note:
Walk the diagram left to right: one pair of terminals, three things in series.
Only the green box does anything you wanted. Point out that nothing in the box
is a component you could unsolder — the split is bookkeeping for where the power
ends up.

---

## Why small antennas are hard

Infinitesimal (Hertzian) dipole, uniform current — and the practical centre-fed short dipole, whose current tapers to zero at the tips:

$$ R_\text{rad} = 80\pi^2\left(\frac{\ell}{\lambda}\right)^2 \qquad\text{vs}\qquad R_\text{rad} = 20\pi^2\left(\frac{\ell}{\lambda}\right)^2 $$

- $\ell = 0.05\lambda \Rightarrow R_\text{rad} \approx 0.49\ \Omega$ for the real thing
- A fraction of an ohm of conductor loss now wrecks the efficiency

Make it $\lambda/2$ long and the picture changes completely.

Note:
The (ℓ/λ)² dependence is the whole story of small-antenna inefficiency. The
triangular current distribution halves the effective length, which quarters the
radiation resistance — so quote 20π², not 80π², for anything you would actually
build. Half an ohm is the number they meet again in the matching lab.

---

## The half-wave dipole

At exactly $\ell = \lambda/2$:

$$ Z_\text{in} \approx 73 + j42.5\ \Omega $$

Trim to $\approx 0.48\lambda$ — reactance cancels, **resonant**:

$$ Z_\text{in} \approx 70 + j0\ \Omega $$

Naturally close to standard feed-line impedances — that's why it's the workhorse.

---

## Reading the reactance

| Condition | $X_\text{in}$ | Behavior |
| :-- | :-: | :-- |
| electrically short | $< 0$ | capacitive |
| resonant | $= 0$ | pure resistance |
| long | $> 0$ | inductive |

Matching is easiest at resonance — no reactance to cancel, only a resistance to transform.

---

## Resonance, seen on a curve

<div class="fig" data-inline-svg="./fig/L04-reactance-vs-length.svg" style="max-width:820px; margin:0 auto;"></div>

Resistance climbs smoothly. **The reactance is what swings** — and it crosses zero just short of $\lambda/2$.

Note:
Curves are the induced-EMF result for a thin wire — representative, not
measured. Two things to make them see: the X curve is far steeper than the R
curve, which is why a couple of percent of trim moves the reactance tens of
ohms and barely touches the resistance; and resonance lands *below* 0.5λ, which
is why every published dipole is cut short. Ask what a fatter wire does — it
resonates shorter still and flattens the swing, which is the fat-dipole
bandwidth trick from L3.

---

<!-- .slide: class="viz-cue-slide" -->

## Feeding: the reflection the source sees

Feed line of characteristic impedance $Z_0$ (coax: $50\ \Omega$):

$$ \Gamma = \frac{Z_\text{in} - Z_0}{Z_\text{in} + Z_0}, \qquad \text{VSWR} = \frac{1+|\Gamma|}{1-|\Gamma|} $$

Reflected fraction $|\Gamma|^2$ → **mismatch loss**:

$$ L_\text{mismatch} = -10\log_{10}\!\left(1-|\Gamma|^2\right)\ \text{dB} $$

<p class="viz-cue">↗ Interactive on the lesson page</p>

Note:
Demo live on the lesson page: drag the antenna impedance off 50 Ω and watch Γ,
VSWR and the mismatch loss in dB move together; park it at VSWR 2 and show the
loss is only 0.5 dB. Same Γ/VSWR from L2–L3, now tied to the antenna's
impedance. Rule of thumb: VSWR ≤ 2 (return loss ≥ 9.5 dB). Sometimes the limit
is what the transmitter can survive — recall the diode problem.

---

## The quarter-wave transformer

<div class="fig" data-inline-svg="./fig/L04-quarter-wave.svg" style="max-width:830px; margin:0 auto;"></div>

A $\lambda/4$ line of impedance $Z_1$ transforms a **real** load $R_L$:

$$ Z_\text{in} = \frac{Z_1^2}{R_L} \qquad\Rightarrow\qquad Z_1 = \sqrt{Z_0R_L} $$

Match a $70\ \Omega$ dipole to $50\ \Omega$: $Z_1 = \sqrt{(50)(70)} \approx 59\ \Omega$. Catch: exactly $\lambda/4$ at **one** frequency → narrowband.

Note:
The geometric mean is the whole design. Ask what happens at twice the frequency
— the section is a half wave, which is transparent, so the radio sees the raw
70 Ω again. Real loads only: a complex antenna needs the reactance gone first.

---

## "Real load only" is not a veto

Cancel the reactance first, and the quarter-wave transformer is back on the table. For $20 - j15\ \Omega$: add $+j15$, then a $\sqrt{(50)(20)} = 31.6\ \Omega$ section.

<div class="fig" data-inline-svg="./fig/L04-match-compare.svg" style="max-width:700px; margin:0 auto;"></div>

<div class="callout">
Two correct designs, near-identical bandwidth. What separates them is the <strong>build medium</strong>, not the physics.
</div>

Note:
Someone always asks this, and it is the right question. Put the two curves up and
let them see the answer: both designs null at 1 GHz and the VSWR-2 bands are
within a few percent of each other. So bandwidth does NOT decide it. What decides
it is on the next slide — whether you can realise the line impedance, and whether
a quarter wave is a sane length at your frequency.

---

## So which one?

| | cancel $+\lambda/4$ | L-match |
| :-- | :-- | :-- |
| needs | a $31.6\ \Omega$ line | two lumped parts |
| at 1 GHz | $\approx 4$ cm printed | millimetres |
| at 2 MHz | $\approx 25$ m of coax | millimetres |
| VSWR $\le 2$ | $\approx 49\%$ | $\approx 45\%$ |

<div class="callout">
Print any $Z_1$ you like on a board — but you cannot <em>buy</em> 31.6 $\Omega$ cable.
</div>

Note:
Microwave PCB, where any Z1 is a trace width and lumped parts have ugly
parasitics — take the transformer. HF with off-the-shelf coax, where a quarter
wave is tens of metres and only 50 and 75 Ω exist — take the L-match. That
second row is exactly why the matching lab is lumped.

---

## The L-match — solve one, learn the method

<div class="fig" data-inline-svg="./fig/L04-lmatch.svg" style="max-width:760px; margin:0 auto;"></div>

<div class="callout">
An antenna presents $Z_\text{in} = 20 - j15\ \Omega$ on a $50\ \Omega$ line at <strong>1 GHz</strong>. Match it.
</div>

Note:
Do not give them the recipe and then demonstrate it — derive it by solving this
one all the way through. Everything needed is already on the table: the
geometric mean from the transformer slide, and the Smith chart from ECE 343.
Five steps, one per slide.

---

## Steps 1-3: reduce, choose, plan

**1. Cancel the load reactance.** Add $+j15\ \Omega$ in series: $(20-j15)+j15 = 20 + j0\ \Omega$. Now it is a *real* 20 Ω to match.

**2. Two ways to get 20 Ω to 50 Ω.** A $\lambda/4$ line of $\sqrt{(50)(20)} = 31.6\ \Omega$ — correct, but no such cable exists and the length is awkward. Or an L-network: one more series element plus a shunt element.

**3. The plan.** The pair must present $50 + j0$ to the line:

- **series** element → make the branch magnitude $= 31.6\ \Omega$
- **shunt** element → clean up the excess reactance

Note:
Step 1 is the move that makes the problem recognisable. Step 2 is where they see
the transformer is not disqualified, just impractical here. Step 3 is the whole
strategy in two bullets — and note the transformer realises 31.6 as a LINE
impedance while the L-network realises it as a BRANCH magnitude. Same number.

---
## Step 4: size the series element

Resistance is stuck at 20 Ω — a series element cannot move it — so the magnitude must come from the reactance:

$$ \vert 20 + jX \vert = 31.6 \quad\Longrightarrow\quad X = \sqrt{31.6^2 - 20^2} = 24.5\ \Omega $$

**Do not forget the $+j15$ from Step 1** — same branch, so the part you install supplies the sum:

$$ X_\text{series} = 15 + 24.5 = 39.5\ \Omega \quad\Longrightarrow\quad L = \frac{39.5}{2\pi(10^9)} = 6.3\ \text{nH} $$

Note:
This is the step they get wrong: 24.5 is what the BRANCH needs, not what you
solder in. The load already brought -j15, so the inductor pays that off first and
then supplies the 24.5.

---

## Step 5: size the shunt element

It sits in **parallel**, and admittances add in parallel — so transform:

$$ Y = \frac{1}{20 + j24.5} = \frac{20 - j24.5}{20^2 + 24.5^2} = 0.0200 - j0.0245\ \text{S} $$

$\frac{1}{\text{Re}\lbrace Y \rbrace} = 50\ \Omega$ — **that is what Step 4 bought.** Cancel the rest with $+j0.0245$ (a capacitor):

$$ \omega C = 0.0245 \quad\Longrightarrow\quad C = \frac{0.0245}{2\pi(10^9)} = 3.9\ \text{pF} $$

<div class="callout">
<strong>6.3 nH series, 3.9 pF shunt.</strong> The antenna looks like 50 Ω — at 1 GHz and nowhere else.
</div>

Note:
Land on the real part: setting the magnitude to the geometric mean IS the
condition that makes 1/Re{Y} come out at 50. Everything after that is one
cancellation. Then the punchline — two lossless parts, and a 20 - j15 antenna
now looks like 50 Ω.
---

<!-- .slide: class="viz-cue-slide" -->

## Why switch to admittance?

Impedances add in **series**. Admittances add in **parallel**. An L-network has one of each — so you must change currency in the middle.

| | cannot change | steers |
| :-- | :-- | :-- |
| **series** element | $\text{Re}(Z)$ — stuck at $20\ \Omega$ | $\text{Re}(Y)$ |
| **shunt** element | $\text{Re}(Y)$ | $\text{Re}(Z)$ |

<div class="callout">
Exact duals. So: steer $\text{Re}(Y)$ to $\frac{1}{50}$ with the series part — then the shunt part <strong>cannot undo it</strong>, and only cancels the leftover.
</div>

Note:
This is the step that feels like a rabbit out of a hat, so name it plainly: the
topology forces it. Then the duality, which is the real payoff. Two series
elements could never work — they only sum reactance and Re(Z) sits at 20 forever.
You need one of each kind. And the reason we read the middle state in parallel
terms is that "20 + j24.5" tells you nothing, the 20 has not moved; "50 Ω
alongside −j40.8" tells you that you have arrived with one cancellation to go.

---

## The same two moves, on the Smith chart

<div class="fig" data-inline-svg="./fig/L04-lmatch-smith.svg" style="max-width:560px; margin:0 auto;"></div>

<p class="viz-cue">↗ Interactive on the lesson page</p>

Note:
This is the picture, and they already own the tool from ECE 343 — same chart,
same circles. Walk it live: the antenna sits low and left of centre, capacitive.
A SERIES element can only move you along a constant-resistance circle, so walk
up that circle until you cross the unit-conductance circle. Now a SHUNT element
moves you along constant conductance, straight into the centre. Two moves, two
elements. Emphasise that the series element cannot change the resistance and the
shunt element cannot change it back — that is why the order is forced.

---

## How does a lossless part change the resistance?

<div class="fig" data-inline-svg="./fig/L04-series-parallel.svg" style="max-width:880px; margin:0 auto;"></div>

<div class="callout">
The reactance is a <strong>lever on voltage that costs no power</strong>. Same 10 W, more volts — so the source infers a bigger resistance.
</div>

Note:
This is the slide that answers "but why 24.5 Ω?" physically. Walk it: 1 A in, the
resistor burns 10 W and that never changes. But the branch voltage is 31.6 V, not
20 V, because the reactor's volts add in quadrature. Stand at the terminals — 31.6
V and 10 W means R = V²/2P = 50 Ω. Nothing was dissipated to achieve it. Then the
punchline: a SHUNT element across 20 Ω can only ever make it look smaller — 17 Ω,
19 Ω, never past 20 — so only a series element can climb, which is why the order
is forced. If they are with you, mention that |Z| = 31.6 Ω is exactly sqrt(20x50),
the same geometric mean as the quarter-wave transformer.

---

## Where Q comes from

References state the design with a network $Q$. It is worth deriving, not quoting — $R$ and $X$ do **not** define $Q$. Energy defines it, exactly as in L3:

$$ Q = \omega\,\frac{\text{peak energy stored}}{\text{average power dissipated}} $$

Drive the branch with current amplitude $I_0$:

$$ W_\text{peak} = \tfrac{1}{2}LI_0^2, \qquad P_\text{avg} = \tfrac{1}{2}I_0^2 R \quad\Longrightarrow\quad Q = \frac{\omega L}{R} = \frac{X}{R} $$

<div class="callout">
$X/R$ is not a definition — it is what the <strong>energy ratio evaluates to</strong> for a series branch. Here $Q = \frac{24.5}{20} = 1.22$.
</div>

Note:
This is the slide that stops Q being a magic symbol. Same energy definition as
the antenna Q in L3; for a series branch it just happens to evaluate to X/R.
Do the two-line evaluation on the board — the I0 squared cancels and you are
left with omega L over R.

---

## What Q costs you

Divide the Step 4 condition $R_L^2 + X^2 = Z_0R_L$ by $R_L^2$:

$$ 1 + Q^2 = \frac{Z_0}{R_L} \qquad\Longrightarrow\qquad Q = \sqrt{\frac{R_\text{big}}{R_\text{small}} - 1} $$

- **You do not choose $Q$** — the ratio $\frac{Z_0}{R_L}$ sets it
- Stored-over-dissipated energy is what set **bandwidth** in L3

<div class="callout">
Transform further → higher $Q$ → less bandwidth. A small antenna with a fraction of an ohm of $R_\text{rad}$ needs an enormous $Q$ to reach 50 Ω.
</div>

Note:
Close the loop with L3 and Chu-Harrington. High Q means a lot of energy sloshing
between L and C for every watt delivered — that is what makes the match
narrowband. And the small-antenna case is the one they meet in the lab.

---

## Baluns: balanced meets unbalanced

- **Dipole** — *balanced*: two symmetric arms, equal & opposite currents, no ground reference
- **Coax** — *unbalanced*: center + inside-of-shield, outside-of-shield tied to ground

Connect them directly and the arms are unequal → leftover **common-mode current** flows on the **outside of the shield**.

---

## The shield-current problem

<div class="fig" data-inline-svg="./fig/L04-balun-currents.svg" style="max-width:880px; margin:0 auto;"></div>

- **The feed line radiates** — the coax becomes part of the antenna
- **Pattern skews**, front-to-back ratio degrades
- **RF on the chassis** — measurement errors, "RF in the shack"

Note:
The third conductor the ideal model forgot: the outside surface of the shield.
Skin effect is the reason it is a separate conductor at all — inside and outside
of the shield do not talk to each other at RF. Left panel is what you build by
accident; right panel is a 30-cent ferrite.

---

## The fix: a balun

**BAL**anced-to-**UN**balanced, at the feed point.

| Balun | Does | Use |
| :-- | :-- | :-- |
| choke / current (ferrite, coil, sleeve) | high common-mode $Z$ on shield | default 1:1 dipole feed |
| voltage (transformer) | balances *voltages* | symmetric drive |
| half-wave 4:1 | balances **and** transforms 4:1 | $300\to75\ \Omega$ folded dipole |

A balun can balance **and** transform impedance at once.

---

## Key point

<div class="callout">
Impedance is where the antenna meets the radio. <strong>Radiation resistance</strong> sets how much power leaves as radiation; the <strong>reactance and mismatch</strong> set how much even makes it onto the antenna; the <strong>balun</strong> makes sure it's the antenna radiating and not your feed line.
</div>

---

## Where this is going

- You can read the terminals as a circuit: split $Z_\text{in}$, turn mismatch into $\Gamma$/VSWR/dB, match with a $\lambda/4$ section or an L-network, specify a balun
- **L5 — Field Regions:** step back into space. *Where* do the fields settle into the far field, and how far away must you be for the pattern you measured to be the pattern you have?

Note:
Bridge to L5: reactive near-field, radiating near-field, far-field boundaries.
