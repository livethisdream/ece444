# L2 practice problems

**LO 1.2** — I can define and calculate fundamental antenna properties:
gain, directivity, effective aperture, beamwidth, and sidelobe level.

Show your work. A **Documentation** line at the bottom is required
(write **None** if you did not collaborate).

Solutions: see [solutions](practice-solutions.md) once you have made a genuine attempt.

---

## Problem 1 — Wave equation sanity check

The 1-D wave equation from a lossless transmission line is

$$
\frac{\partial^{2} v}{\partial z^{2}}
= L C \frac{\partial^{2} v}{\partial t^{2}}.
$$

**(a)** Show by direct substitution that $v(z, t) = f(z - u t)$ is a solution
for any twice-differentiable $f$, and find $u$ in terms of $L$ and $C$.

**(b)** For a coaxial cable with $L = 250\ \text{nH/m}$ and
$C = 100\ \text{pF/m}$, compute the propagation speed and the velocity
factor $u / c$.

**(c)** In one sentence, explain what a "velocity factor of 0.66" (typical
of RG-58 coax) means physically.

---

## Problem 2 — Time and space frequencies

A plane wave in free space is written as

$$
\mathbf{E}(z, t) = \hat{x} E_{0} \cos(\omega t - k z).
$$

**(a)** For a signal at $f = 2.40\ \text{GHz}$ (Wi-Fi channel 6), compute
$\omega$, $\lambda$, and $k$.

**(b)** How far does the wave crest travel in **one nanosecond**?
Express your answer in wavelengths.

**(c)** At a fixed point in space, how many full oscillations does the
field complete in **one nanosecond**?

**(d)** Sketch (by hand) $\mathbf{E}$ vs. $z$ at $t = 0$ over a range of
two wavelengths, then $\mathbf{E}$ vs. $t$ at $z = 0$ over a range of
two periods. Label the axes.

---

## Problem 3 — Directivity from beamwidths

A ground-based tracking antenna has half-power beamwidths of
$\theta_{1} = 2.5^{\circ}$ in azimuth and $\theta_{2} = 1.8^{\circ}$
in elevation.

**(a)** Estimate the directivity in dBi using the pencil-beam
approximation
$D \approx 41{,}253 / (\theta_{1}^{\circ} \theta_{2}^{\circ})$.

**(b)** The antenna is measured to have a **radiation efficiency of 88%**
and an **impedance mismatch of $|\Gamma| = 0.25$**. What is the
**realized gain** at boresight, in dBi?

**(c)** In one sentence, explain the difference between $D$, $G$, and
$G_{\text{re}}$ for this antenna.

---

## Problem 4 — Effective area

**(a)** A parabolic dish for a satellite ground terminal has
$G = 47\ \text{dBi}$ at $f = 12\ \text{GHz}$. Compute the effective
area $A_{e}$ using $A_{e} = G \lambda^{2} / (4 \pi)$.

**(b)** The dish is physically $2.4\ \text{m}$ in diameter. What is its
**aperture efficiency** $\eta_{\text{ap}} = A_{e} / A_{\text{phys}}$?
Is that a reasonable value for a real dish?

**(c)** If we could keep the same physical dish but re-illuminate it
efficiently at $f = 30\ \text{GHz}$ (Ka-band uplink), what gain (dBi)
would you expect, assuming aperture efficiency does not change?

---

## Problem 5 — Reading a real pattern

**Find your own antenna.** Track down a published radiation-pattern plot
for a real antenna — a manufacturer datasheet, an application note, or a
journal figure. A polar or rectilinear gain cut both work, as long as the
axis is labeled in dB. (Horns, patch antennas, Yagis, and reflector dishes
all have easy-to-find patterns.) **Print it or sketch it, and mark each
feature directly on the plot.** Hand in the annotated pattern along with
your readings below.

From *your* plot, identify and annotate:

**(a)** Boresight direction (in degrees off nose)

**(b)** Half-power beamwidth (HPBW)

**(c)** First-null beamwidth (FNBW), or state if no null is visible
inside the plotted range

**(d)** Peak sidelobe level (SLL) in dB below the main lobe

**(e)** Front-to-back ratio (F/B) in dB

<small>Cite the source (manufacturer + part number, or the paper). If your
pattern genuinely lacks a feature — some cuts show no distinct back lobe —
say so and explain why.</small>

---

## Problem 6 — Friis link with gain and effective area

A UHF ground station at $f = 400\ \text{MHz}$ transmits **$P_{t} = 20\ \text{W}$**
into an antenna with **$G_{t} = 8\ \text{dBi}$**. A cubesat at
$r = 800\ \text{km}$ carries a receive antenna with
**$G_{r} = 3\ \text{dBi}$** and is on boresight for both antennas.

**(a)** Compute the on-axis power density $S_{\text{inc}}$ at the
cubesat.

**(b)** Compute the cubesat receive antenna's effective area $A_{e,r}$.

**(c)** Compute the received power $P_{r} = S_{\text{inc}} A_{e,r}$
and express the result in dBm.

**(d)** Verify your answer by computing $P_{r}$ directly from the Friis
equation

$$
P_{r} = P_{t} G_{t} G_{r} \left( \frac{\lambda}{4 \pi r} \right)^{2}.
$$

---

**Documentation:**
