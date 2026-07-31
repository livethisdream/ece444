# L2 practice — solutions

Use these **after** a genuine attempt at [the problem set](practice.md). If your answer differs, work back through your algebra before assuming the key is wrong (though — if the key is wrong, tell me; it counts for engagement credit).

---

## Problem 1 — Wave equation sanity check

**(a)** With $v(z, t) = f(z - u t)$, let $\xi = z - u t$. Chain rule:

$$
\frac{\partial v}{\partial z} = f'(\xi),
\quad
\frac{\partial^{2} v}{\partial z^{2}} = f''(\xi)
$$

$$
\frac{\partial v}{\partial t} = -u\, f'(\xi),
\quad
\frac{\partial^{2} v}{\partial t^{2}} = u^{2}\, f''(\xi)
$$

Substituting into $\partial^{2} v / \partial z^{2} = L C\,
\partial^{2} v / \partial t^{2}$:

$$
f''(\xi) = L C\, u^{2}\, f''(\xi)
\quad\Longrightarrow\quad
u = \frac{1}{\sqrt{L C}}.
$$

**(b)** $L C = (2.5 \times 10^{-7})(1.0 \times 10^{-10}) = 2.5 \times 10^{-17}\ \text{s}^{2}/\text{m}^{2}$.

$$
u = \frac{1}{\sqrt{2.5 \times 10^{-17}}}
= 2.0 \times 10^{8}\ \text{m/s}.
$$

Velocity factor: $u / c = 2.0 / 3.0 \approx \boxed{0.67}$.

**(c)** A velocity factor of 0.66 means signals on the line travel at
about **66% of the speed of light in vacuum**. Physically, the dielectric
material between the conductors slows the wave; equivalently, the guided
wavelength on the line is 66% of the free-space wavelength at the same
frequency.

---

## Problem 2 — Time and space frequencies

**(a)** $\omega = 2 \pi f = 2 \pi (2.40 \times 10^{9})
\approx \boxed{1.51 \times 10^{10}\ \text{rad/s}}$.

$$
\lambda = \frac{c}{f} = \frac{3.00 \times 10^{8}}{2.40 \times 10^{9}}
= \boxed{0.125\ \text{m}} = 12.5\ \text{cm}.
$$

$$
k = \frac{2 \pi}{\lambda} \approx \boxed{50.3\ \text{rad/m}}.
$$

**(b)** In 1 ns the crest moves $c\, \Delta t = (3.00 \times 10^{8})(10^{-9})
= 0.30\ \text{m}$. In wavelengths:
$0.30 / 0.125 = \boxed{2.4\ \lambda}$.

**(c)** At a fixed $z$, oscillations in 1 ns: $f\, \Delta t
= (2.40 \times 10^{9})(10^{-9}) = \boxed{2.4\ \text{cycles}}$.

**(d)** Two identical cosines — one plotted vs. $z$ (period
$\lambda = 12.5\ \text{cm}$), one plotted vs. $t$ (period
$T = 1/f \approx 417\ \text{ps}$). Note that the answers to (b)
and (c) are the same number — **that is $\omega/k = c$ in disguise**:
the wave completes the same number of cycles in space per meter of
travel that it completes in time per second of elapsed time, related
by the speed of light.

---

## Problem 3 — Directivity from beamwidths

**(a)** Pencil-beam approximation:

$$
D \approx \frac{41{,}253}{(2.5)(1.8)}
= \frac{41{,}253}{4.5}
\approx 9170.
$$

In dBi: $D_{\text{dBi}} = 10 \log_{10}(9170) \approx \boxed{39.6\ \text{dBi}}$.

**(b)** Apply efficiency, then mismatch:

- $G = e_{\text{rad}}\, D = 0.88 \times 9170 \approx 8070$; in dBi
  $G \approx 39.1\ \text{dBi}$.
- Mismatch loss: $1 - |\Gamma|^{2} = 1 - 0.0625 = 0.9375$.
- $G_{\text{re}} = 0.9375 \times 8070 \approx 7560$; in dBi
  $G_{\text{re}} \approx \boxed{38.8\ \text{dBi}}$.

**(c)** $D$ is a purely geometric property of the radiation pattern.
$G$ folds in ohmic and dielectric losses inside the antenna. $G_{\text{re}}$
adds the loss caused by an impedance mismatch at the antenna terminals —
it is what you would actually measure with a source connected through a
transmission line.

---

## Problem 4 — Effective area

**(a)** At 12 GHz, $\lambda = c/f = 0.0250\ \text{m}$, so
$\lambda^{2} = 6.25 \times 10^{-4}\ \text{m}^{2}$.

$G = 47\ \text{dBi} = 10^{4.7} \approx 50{,}120$.

$$
A_{e} = \frac{G \lambda^{2}}{4 \pi}
= \frac{50{,}120 \times 6.25 \times 10^{-4}}{4 \pi}
\approx \boxed{2.49\ \text{m}^{2}}.
$$

**(b)** Physical area: $A_{\text{phys}} = \pi (D/2)^{2} = \pi (1.2)^{2}
\approx 4.52\ \text{m}^{2}$.

$$
\eta_{\text{ap}} = \frac{A_{e}}{A_{\text{phys}}}
= \frac{2.49}{4.52}
\approx \boxed{0.55}.
$$

That's a realistic value — real dishes typically fall in the
$\eta_{\text{ap}} \approx 0.5$ – $0.7$ range once you account for
illumination taper, spillover, blockage from the feed and struts,
and surface roughness.

**(c)** If $\eta_{\text{ap}}$ is preserved, then $A_{e}$ is unchanged
and $G = 4 \pi A_{e} / \lambda^{2}$ scales as $1/\lambda^{2} = f^{2}$.

Going from 12 GHz to 30 GHz is a factor of 2.5 in frequency, i.e. 6.25
in gain (linear), or $10 \log_{10}(6.25) \approx 8.0\ \text{dB}$ of
improvement.

$$
G_{30} \approx 47 + 8 = \boxed{55\ \text{dBi}}.
$$

**Caveat:** in practice, higher frequencies expose surface roughness
and pointing errors that reduce $\eta_{\text{ap}}$ — so this is an
optimistic upper bound, not a guarantee.

---

## Problem 5 — Reading a pattern

Answers depend on the specific polar plot handed out. Grade rubric:

- **Boresight** — within $\pm 2^{\circ}$ of the true peak
- **HPBW** — within $\pm 10\%$ of the plotted value
- **FNBW** — within $\pm 10\%$; "no null visible" is a legitimate answer
  if the pattern is monotonic to the plot edge
- **SLL** — within $\pm 2\ \text{dB}$ of the plotted peak sidelobe
- **F/B** — within $\pm 2\ \text{dB}$

The habit we're building here is **reading pattern plots consistently**
— every subsequent lesson uses these same measurements.

---

## Problem 6 — Friis link with gain and effective area

**Given:** $f = 400\ \text{MHz}$, $P_{t} = 20\ \text{W}$,
$G_{t} = 8\ \text{dBi} \Rightarrow 6.31$, $G_{r} = 3\ \text{dBi}
\Rightarrow 2.00$, $r = 800\ \text{km} = 8.0 \times 10^{5}\ \text{m}$.

$\lambda = c/f = 0.75\ \text{m}$, $\lambda^{2} = 0.5625\ \text{m}^{2}$.

**(a)** On-axis power density from the transmitter:

$$
S_{\text{inc}} = \frac{P_{t}\, G_{t}}{4 \pi r^{2}}
= \frac{20 \times 6.31}{4 \pi (8.0 \times 10^{5})^{2}}
$$

$$
= \frac{126.2}{8.04 \times 10^{12}}
\approx \boxed{1.57 \times 10^{-11}\ \text{W/m}^{2}}.
$$

**(b)** Receive effective area:

$$
A_{e,r} = \frac{G_{r} \lambda^{2}}{4 \pi}
= \frac{2.00 \times 0.5625}{4 \pi}
\approx \boxed{0.0895\ \text{m}^{2}}.
$$

**(c)** Received power:

$$
P_{r} = S_{\text{inc}}\, A_{e,r}
= (1.57 \times 10^{-11})(0.0895)
\approx 1.40 \times 10^{-12}\ \text{W}.
$$

In dBm:
$P_{r,\text{dBm}} = 10 \log_{10}(1.40 \times 10^{-12} / 10^{-3})
= \boxed{-88.5\ \text{dBm}}$.

**(d)** Friis directly:

$$
\left( \frac{\lambda}{4 \pi r} \right)^{2}
= \left( \frac{0.75}{4 \pi \times 8.0 \times 10^{5}} \right)^{2}
= (7.46 \times 10^{-8})^{2}
\approx 5.56 \times 10^{-15}.
$$

$$
P_{r} = P_{t}\, G_{t}\, G_{r}\, \left( \frac{\lambda}{4 \pi r} \right)^{2}
= 20 \times 6.31 \times 2.00 \times 5.56 \times 10^{-15}
$$

$$
\approx 1.40 \times 10^{-12}\ \text{W}
\;\checkmark
$$

Same answer. Two lessons here:

1. **Friis is just $S_{\text{inc}} \times A_{e,r}$** with $A_{e,r}$ written
   out in terms of $G_{r}$ and $\lambda$. Same physics.
2. **$-88\ \text{dBm}$ into a decent LNA is plenty of link margin at
   UHF.** This is roughly where a healthy amateur cubesat downlink sits.
