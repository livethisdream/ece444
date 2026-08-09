# L4 practice — solutions

Use these **after** a genuine attempt at [the problem set](practice.md). If your
answer differs, work back through your algebra before assuming the key is wrong
(though — if the key is wrong, tell me; it counts for engagement credit).

---

## Problem 1 — Radiation resistance and efficiency

**(a)** $R_\text{rad} = 80\pi^2 (0.08)^2 = 789.6 \times 0.0064 \approx
\boxed{5.05\ \Omega}$.

**(b)**

$$
\eta_\text{rad} = \frac{R_\text{rad}}{R_\text{rad} + R_\text{loss}}
= \frac{5.05}{5.05 + 1.5} = \frac{5.05}{6.55} \approx \boxed{0.77\ (77\%)}.
$$

**(c)** $G_\text{dBi} = D_\text{dBi} + 10\log_{10}\eta_\text{rad}
= 1.76 + 10\log_{10}(0.77) = 1.76 - 1.13 \approx \boxed{0.6\ \text{dBi}}$.

Even at 77% efficiency the short dipole barely beats isotropic — most of the
"loss" here is really the tiny directivity, but the point stands: keep
$R_\text{rad}$ well above $R_\text{loss}$.

---

## Problem 2 — Feeding a half-wave dipole with 50 Ω coax

**(a)** Resonant, $Z_\text{in} = 70 + j0$:

$$
\Gamma = \frac{70 - 50}{70 + 50} = \frac{20}{120} = \boxed{0.167},
\qquad
\text{VSWR} = \frac{1 + 0.167}{1 - 0.167} \approx \boxed{1.40}.
$$

$$
\text{RL} = -20\log_{10}(0.167) \approx \boxed{15.6\ \text{dB}}, \qquad
L_\text{mm} = -10\log_{10}(1 - 0.167^2) \approx \boxed{0.12\ \text{dB}}.
$$

**(b)** Untrimmed, $Z_\text{in} = 73 + j42.5$:

$$
\Gamma = \frac{(73-50) + j42.5}{(73+50) + j42.5} = \frac{23 + j42.5}{123 + j42.5}.
$$

$$
|\Gamma| = \frac{\sqrt{23^2 + 42.5^2}}{\sqrt{123^2 + 42.5^2}}
= \frac{48.3}{130.1} \approx \boxed{0.371},
\qquad
\text{VSWR} = \frac{1.371}{0.629} \approx \boxed{2.18}.
$$

**(c)** Trimming to resonance killed the $+j42.5\ \Omega$ reactance, dropping VSWR
from $\approx 2.2$ to $1.4$ — the reactance, not the resistance, was doing most of
the damage.

---

## Problem 3 — Quarter-wave transformer

**(a)** $Z_1 = \sqrt{Z_0 R_L} = \sqrt{(50)(36)} = \sqrt{1800} \approx
\boxed{42.4\ \Omega}$.

**(b)** At the design frequency the transformer makes the input impedance
$Z_1^2 / R_L = 1800/36 = 50\ \Omega = Z_0$, so $\boxed{\Gamma = 0}$ (perfect
match).

**(c)** The section is exactly $\lambda/4$ only at the design frequency; off
frequency its electrical length is no longer $90^\circ$, the transformation
$Z_1^2/R_L$ no longer holds, and $|\Gamma|$ climbs — the match is **narrowband**.

---

## Problem 4 — VSWR, reflection, and the impedance behind it

**(a)** $|\Gamma| = \dfrac{\text{VSWR} - 1}{\text{VSWR} + 1}
= \dfrac{0.5}{2.5} = \boxed{0.20}$.

**(b)** $\text{RL} = -20\log_{10}(0.20) \approx \boxed{14\ \text{dB}}$.

**(c)** $L_\text{mm} = -10\log_{10}(1 - 0.20^2) = -10\log_{10}(0.96)
\approx \boxed{0.18\ \text{dB}}$.

**(d)** For a real load, $Z_\text{in} = Z_0 \dfrac{1 \pm |\Gamma|}{1 \mp |\Gamma|}$:

$$
Z_\text{in} = 50 \times \frac{1.2}{0.8} = \boxed{75\ \Omega}
\quad\text{or}\quad
Z_\text{in} = 50 \times \frac{0.8}{1.2} = \boxed{33.3\ \Omega}.
$$

A given VSWR does not tell you which side of $Z_0$ you are on.

---

## Problem 5 — Baluns

**(a)** Coax is unbalanced, so the two dipole arms present unequal impedances to
it. The imbalance drives a **common-mode current on the outside of the shield**;
that shield current radiates, so the feed line becomes part of the antenna and
skews the pattern.

**(b)** A **4:1 (half-wave) balun**. It both balances the feed *and* transforms
impedance by 4:1, taking $292\ \Omega$ down to $\approx 73\ \Omega$ — a good match
to $75\ \Omega$ coax.

**(c)** A **1:1 current (choke) balun**. The $70\ \Omega$ dipole is already a
good match to $50\ \Omega$ (VSWR $\approx 1.4$), so no impedance transformation is
wanted — you only need to choke off the shield current. Using a 4:1 balun here
would *ruin* the match.

---

**Documentation:**
