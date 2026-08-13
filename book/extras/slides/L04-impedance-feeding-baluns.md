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

- **$R_\text{rad}$** — the equivalent resistance for power carried away as radiation. The *useful* part.
- **$R_\text{loss}$** — real ohmic/dielectric loss. Becomes heat.

<div class="callout">
This split <em>is</em> the radiation efficiency from L2: &nbsp; $\eta_\text{rad}=\dfrac{R_\text{rad}}{R_\text{rad}+R_\text{loss}}$, &nbsp; $G=\eta_\text{rad}D$.
</div>

---

## Why small antennas are hard

Short dipole ($\ell \ll \lambda$):

$$ R_\text{rad} = 80\pi^2\left(\frac{\ell}{\lambda}\right)^2 $$

- $\ell = 0.05\lambda \Rightarrow R_\text{rad} \approx 2\ \Omega$
- A fraction of an ohm of conductor loss now wrecks the efficiency

Make it $\lambda/2$ long and the picture changes completely.

Note:
The (ℓ/λ)² dependence is the whole story of small-antenna inefficiency.

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

## Feeding: the reflection the source sees

Feed line of characteristic impedance $Z_0$ (coax: $50\ \Omega$):

$$ \Gamma = \frac{Z_\text{in} - Z_0}{Z_\text{in} + Z_0}, \qquad \text{VSWR} = \frac{1+|\Gamma|}{1-|\Gamma|} $$

Reflected fraction $|\Gamma|^2$ → **mismatch loss**:

$$ L_\text{mismatch} = -10\log_{10}\!\left(1-|\Gamma|^2\right)\ \text{dB} $$

<p class="viz-cue">↗ Interactive on the lesson page</p>

Note:
Same Γ/VSWR from L2–L3, now tied to the antenna's impedance. Rule of thumb:
VSWR ≤ 2 (return loss ≥ 9.5 dB). Sometimes the limit is what the transmitter can
survive — recall the diode problem.

---

## The quarter-wave transformer

A $\lambda/4$ line of impedance $Z_1$ transforms a **real** load $R_L$:

$$ Z_\text{in} = \frac{Z_1^2}{R_L} \qquad\Rightarrow\qquad Z_1 = \sqrt{Z_0R_L} $$

**Match a $70\ \Omega$ dipole to $50\ \Omega$:**

$$ Z_1 = \sqrt{(50)(70)} \approx 59\ \Omega $$

Catch: exactly $\lambda/4$ at **one** frequency → narrowband.

---

## The L-match

- Two reactances: one **cancels the load reactance**, the other **transforms the resistance**
- The minimal lumped network — reaches any $Z_0$ from a complex load
- The starting point for Smith-chart matching later in the course

<div class="callout">
Every match is <strong>band-limited</strong>. Forcing $\Gamma=0$ at one frequency is easy; holding it across a band is the size-vs-bandwidth fight from L3.
</div>

---

## Baluns: balanced meets unbalanced

- **Dipole** — *balanced*: two symmetric arms, equal & opposite currents, no ground reference
- **Coax** — *unbalanced*: center + inside-of-shield, outside-of-shield tied to ground

Connect them directly and the arms are unequal → leftover **common-mode current** flows on the **outside of the shield**.

---

## The shield-current problem

Common-mode current on the shield means:

- **The feed line radiates** — the coax becomes part of the antenna
- **Pattern skews**, front-to-back ratio degrades
- **RF on the chassis** — measurement errors, "RF in the shack"

Note:
The third conductor the ideal model forgot: the outside surface of the shield.

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

- You can read the terminals as a circuit: split $Z_\text{in}$, turn mismatch into $\Gamma$/VSWR/dB, match with a $\lambda/4$ section, specify a balun
- **L5 — Field Regions:** step back into space. *Where* do the fields settle into the far field, and how far away must you be for the pattern you measured to be the pattern you have?

Note:
Bridge to L5: reactive near-field, radiating near-field, far-field boundaries.
