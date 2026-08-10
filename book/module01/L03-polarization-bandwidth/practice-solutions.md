# L3 practice — solutions

Use these **after** a genuine attempt at [the problem set](practice.md). If your
answer differs, work back through your algebra before assuming the key is wrong
(though — if the key is wrong, tell me; it counts for engagement credit).

---

## Problem 1 — Identify the polarization

**(a)** Only an $\hat{x}$ component — **linear, along $\hat{x}$ (0°)**.

**(b)** Equal amplitudes on $\hat{x}$ and $\hat{y}$, in phase
($\delta = 0$). Trace: E-vector always along $\hat{x} + \hat{y}$.
**Linear, tilted $+45^{\circ}$ from $\hat{x}$**.

**(c)** Equal amplitudes, $\delta = -90^{\circ}$. At $t = 0$: $E_{x}$
is at its peak on $\hat{x}$; $E_{y} = 5 \cos(-90^{\circ}) = 0$. A
quarter period later ($\omega t = 90^{\circ}$): $E_{x} = 0$,
$E_{y} = 5 \cos(0) = 5$ on $\hat{y}$. Vector rotates from $\hat{x}$
toward $\hat{y}$ — with the propagation direction $+\hat{z}$, that is
**right-hand circular (RHCP)** by the IEEE convention.

**(d)** Same amplitudes, $\delta = +90^{\circ}$. Rotation is reversed
→ **left-hand circular (LHCP)**.

**(e)** Unequal amplitudes with $\delta = -90^{\circ}$: axes align
with $\hat{x}$ and $\hat{y}$, major axis $= 3$, minor axis $= 1$. Sign
of $\delta$ says right-hand sense. **Right-hand elliptical**,
$\text{AR} = 3$ (about 9.5 dB).

---

## Problem 2 — Axial ratio

**(a)** $\text{AR} = 10^{3/20} \approx \boxed{1.41}$
(equivalently $\sqrt{2}$).

**(b)** Taking the major axis along $\hat{x}$ with unit major
amplitude, $E_{\text{maj}} = 1$ and $E_{\text{min}} = 1/1.41
\approx 0.707$. The two orthogonal linear components are:

$$
E_{x}(t) = 1 \cdot \cos(\omega t), \qquad
E_{y}(t) = 0.707 \cos(\omega t \pm 90^{\circ}).
$$

Sign of the 90° phase determines RHCP vs LHCP sense.

**(c)** Powers ratio to amplitude squared:

$$
\frac{P_{x}}{P_{y}} = \left( \frac{1.0}{0.707} \right)^{2} = 2.0.
$$

In dB: $10 \log_{10}(2.0) \approx \boxed{3.0\ \text{dB}}$. Yes, it
matches — the axial ratio is exactly the peak-to-peak amplitude ratio
between what an aligned linear receiver picks off on each axis, so
$\text{AR}_{\text{dB}}$ equals the difference in received *power*
between the two orthogonal linear receivers.

---

## Problem 3 — Polarization loss factor

**(a)** Linear ↔ CP → PLF $= 0.5 = \boxed{-3\ \text{dB}}$. The CP
antenna "sees" only the co-rotating half of the incoming linear wave.

**(b)** Same 3 dB penalty — an ideal LHCP antenna picks up the same
0.5 fraction of a linear wave as an RHCP antenna does. Sense mismatch
between two **CP** antennas would give $-\infty$ dB, but linear-to-CP
does not care about sense. $\boxed{-3\ \text{dB}}$.

**(c)** Two linear antennas tilted at angle $\theta$:

$$
\text{PLF} = \cos^{2}(30^{\circ}) = (0.866)^{2} \approx 0.75.
$$

In dB: $10 \log_{10}(0.75) \approx \boxed{-1.2\ \text{dB}}$.

**(d)** Aircraft roll, pitch, and yaw during a mission — a linearly
polarized aircraft antenna will drift through every tilt angle
relative to the ground station over the course of a maneuver, so a
linear-linear pair would fade unpredictably. Making at least one end
CP caps the worst-case polarization loss at 3 dB regardless of
airframe attitude.

---

## Problem 4 — Impedance bandwidth from a VSWR spec

**(a)** $f_{H} - f_{L} = 2.55 - 2.30 = \boxed{250\ \text{MHz}}$.

**(b)** $f_{c} = (2.55 + 2.30) / 2 = 2.425\ \text{GHz}$.

$$
\text{FBW} = \frac{250}{2425} \approx 0.103 = \boxed{10.3\%}.
$$

**(c)** From $\text{VSWR} = 2$:

$$
|\Gamma| = \frac{\text{VSWR} - 1}{\text{VSWR} + 1}
        = \frac{1}{3} \approx 0.333.
$$

Return loss:

$$
\text{RL} = -20 \log_{10}(|\Gamma|) = -20 \log_{10}(0.333)
         \approx \boxed{9.5\ \text{dB}}.
$$

**(d)** FBW ≈ 10% puts this squarely in the **broadband** category —
comfortably wider than a patch, but not UWB. This is exactly the
range where a **standard-gain horn** or a well-designed **half-wave
dipole** lives. A patch would need matching-network tricks to reach
10%; a log-periodic would be overkill.

---

## Problem 5 — Fractional and ratio bandwidth

**(a)** Low band, $698 – 960\ \text{MHz}$:

$$
f_{c} = (960 + 698) / 2 = 829\ \text{MHz}
$$

$$
\text{FBW} = (960 - 698) / 829 \approx 0.316 = \boxed{31.6\%}, \qquad
\text{RBW} = 960 / 698 \approx \boxed{1.38:1}.
$$

High band, $1710 – 2690\ \text{MHz}$:

$$
f_{c} = (2690 + 1710) / 2 = 2200\ \text{MHz}
$$

$$
\text{FBW} = (2690 - 1710) / 2200 \approx 0.445 = \boxed{44.5\%}, \qquad
\text{RBW} = 2690 / 1710 \approx \boxed{1.57:1}.
$$

**(b)** UWB, $3.1 – 10.6\ \text{GHz}$:

$$
\text{RBW} = 10.6 / 3.1 \approx \boxed{3.42:1}.
$$

Well above the 2:1 FCC UWB threshold — yes, it counts as UWB.

**(c)** Reasonable picks:

- **Low cellular band (0.7 – 1.0 GHz), FBW ≈ 32%.** A modified
  dipole/monopole or a broadband PIFA (planar inverted-F). Too wide for
  a single-resonance patch; a good match for a resonant structure with
  parasitic tuning.
- **High cellular band (1.7 – 2.7 GHz), FBW ≈ 45%.** A slot antenna
  in the phone's chassis or a stacked-patch design — both can cover
  that range without going to a full log-periodic.
- **UWB radar (3.1 – 10.6 GHz), RBW = 3.4:1.** A **Vivaldi (tapered
  slot)** or a **log-periodic dipole array**. Both are self-scaling
  and comfortably cover 3:1 or wider without impedance-matching
  tricks.

---

## Problem 6 — Chu-Harrington intuition

**(a)** $\lambda = c / f = (3.0 \times 10^{8}) / (915 \times 10^{6})
\approx 0.328\ \text{m} = 32.8\ \text{cm}$.

$$
k = 2 \pi / \lambda \approx 19.2\ \text{rad/m}.
$$

$$
k a = 19.2 \times 0.015 = \boxed{0.288}.
$$

**(b)**

$$
Q_{\min} \approx \frac{1}{(0.288)^{3}} + \frac{1}{0.288}
       \approx \frac{1}{0.0239} + 3.47
       \approx 41.9 + 3.47
       \approx \boxed{45}.
$$

**(c)** Maximum FBW ≈ $1/Q_{\min} \approx 1/45 \approx 0.022 = \boxed{2.2\%}$.
At 915 MHz that is roughly $0.022 \times 915 \approx 20\ \text{MHz}$
of bandwidth at VSWR ≤ 2.

**(d)** No — 100 MHz at 915 MHz is FBW ≈ 11%, roughly **five times**
the Chu-Harrington ceiling for a 15 mm sphere. Physically achievable
only by **enlarging the antenna** (increase $a$ until $Q_{\min}$
drops enough), or by **resistive loading / matching-network
absorption**, both of which trade gain for bandwidth. The bound is a
statement about lossless antennas; you can beat it with loss, but
never for free.

---

## Problem 7 — Mismatch that kills the amplifier

**(a)** Using $P[\text{W}] = 10^{(P[\text{dBm}] - 30)/10}$:

$$
P_{\text{fwd}} = 10^{(40 - 30)/10} = 10^{1} = 10\ \text{W}, \qquad
P_{\max} = 10^{(30 - 30)/10} = 10^{0} = 1\ \text{W}.
$$

**(b)** A fraction $|\Gamma|^{2}$ of the forward power is reflected:

$$
P_{\text{ref}} = |\Gamma|^{2} P_{\text{fwd}}.
$$

**(c)** The diode fails when $P_{\text{ref}} = P_{\max}$, so

$$
|\Gamma|_{\max} = \sqrt{\frac{P_{\max}}{P_{\text{fwd}}}}
              = \sqrt{\frac{1}{10}} = \sqrt{0.1} \approx \boxed{0.316}.
$$

**(d)** VSWR from $|\Gamma|_{\max}$:

$$
\text{VSWR}_{\max} = \frac{1 + |\Gamma|_{\max}}{1 - |\Gamma|_{\max}}
                  = \frac{1.316}{0.684} \approx \boxed{1.93}.
$$

Return loss:

$$
\text{RL}_{\min} = -20 \log_{10}|\Gamma|_{\max}
                = -10 \log_{10}(0.1) = \boxed{10\ \text{dB}}.
$$

Datasheet rule: **keep VSWR ≤ 1.9 (return loss ≥ 10 dB)** at the PA
output, or the diode cooks. Equivalently: the reflected power must stay
at least 10 dB below the forward power.

**(e)** A **circulator or isolator** routes the reflected wave into a
matched dump-port load instead of back into the PA, so the diode no
longer sees the reflected power — the antenna can then run at much
higher VSWR without destroying the output stage (paid for by the
isolator's insertion loss, size, cost, and finite bandwidth).

---

**Documentation:**
