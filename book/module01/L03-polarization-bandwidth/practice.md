# L3 practice problems

**LO 1.3** — I can determine the polarization of an antenna and describe
the bandwidth characteristics of common antenna types.

Show your work. A **Documentation** line at the bottom is required
(write **None** if you did not collaborate).

Solutions: see [solutions](practice-solutions.md) once you have made a
genuine attempt.

---

## Problem 1 — Identify the polarization

For each plane wave propagating in $+\hat{z}$, identify the
polarization (linear, RHCP, LHCP, or elliptical) and — where linear —
the tilt angle relative to $\hat{x}$.

**(a)** $\mathbf{E} = \hat{x} 3 \cos(\omega t - k z)$

**(b)** $\mathbf{E} = \hat{x} 2 \cos(\omega t - k z)
                    + \hat{y} 2 \cos(\omega t - k z)$

**(c)** $\mathbf{E} = \hat{x} 5 \cos(\omega t - k z)
                    + \hat{y} 5 \cos(\omega t - k z - 90^{\circ})$

**(d)** $\mathbf{E} = \hat{x} 5 \cos(\omega t - k z)
                    + \hat{y} 5 \cos(\omega t - k z + 90^{\circ})$

**(e)** $\mathbf{E} = \hat{x} 3 \cos(\omega t - k z)
                    + \hat{y} 1 \cos(\omega t - k z - 90^{\circ})$

---

## Problem 2 — Axial ratio

A satellite downlink antenna is spec'd as circularly polarized with
$\text{AR} \le 3\ \text{dB}$ across its operating band.

**(a)** Convert the 3 dB axial ratio spec to a linear ratio (major /
minor axis).

**(b)** Suppose the antenna is producing the linear axial ratio you
just found. Write down the two orthogonal linear components $E_{x}$
and $E_{y}$ (up to a common scale factor) with the appropriate 90°
phase relationship. Assume the ellipse major axis is along $\hat{x}$.

**(c)** A perfect linear receiver aligned with $\hat{x}$ picks off the
$E_{x}$ component. A second linear receiver aligned with $\hat{y}$
picks off $E_{y}$. Compute the ratio of received *power* between the
two, in dB. Should this match part (a)?

---

## Problem 3 — Polarization loss factor

**(a)** A ground station transmits a **linearly polarized** signal
along $\hat{x}$. A satellite receiver antenna is **RHCP** and pointed
correctly. Compute the PLF in dB.

**(b)** Same ground station, but this time the satellite receiver is
**LHCP**. Compute the PLF.

**(c)** Two handheld radios, each with a **linear** whip antenna, are
being used at an angle. Radio A's antenna points straight up; radio
B's antenna is tilted $30^{\circ}$ from vertical. Compute the PLF.

**(d)** In one sentence, explain why aircraft-to-ground data links
almost always specify circular polarization on at least one end.

---

## Problem 4 — Impedance bandwidth from a VSWR spec

An antenna manufacturer specs an antenna as **"VSWR ≤ 2:1 from
$2.30\ \text{GHz}$ to $2.55\ \text{GHz}$"**.

**(a)** What is the impedance bandwidth in MHz?

**(b)** What is the fractional bandwidth (FBW) in percent?

**(c)** Convert VSWR = 2 to reflection coefficient magnitude
$|\Gamma|$ and to return loss in dB.

**(d)** Would you classify this antenna as narrowband, broadband, or
ultra-wideband? Which antenna family is a likely match — patch, horn,
or log-periodic?

---

## Problem 5 — Fractional and ratio bandwidth

**(a)** A cellular antenna covers $698 – 960\ \text{MHz}$ (low band)
and $1{.}71 – 2{.}69\ \text{GHz}$ (high band). Compute the fractional
bandwidth of each band, and the ratio bandwidth of each band.

**(b)** A UWB radar antenna covers $3.1 – 10.6\ \text{GHz}$. Compute
its ratio bandwidth. Does it meet the FCC UWB threshold of RBW ≥ 2:1?

**(c)** Sketch (or describe) what kind of antenna family — resonant
patch, tapered slot, log-periodic — you would pick for each of the
three bands in (a) and (b), and give a one-sentence reason.

---

## Problem 6 — Chu-Harrington intuition

A designer needs an antenna to fit inside a sphere of radius
$a = 15\ \text{mm}$ and operate at $f = 915\ \text{MHz}$ (ISM band).

**(a)** Compute $\lambda$, $k$, and the electrical size $ka$.

**(b)** Estimate the minimum Q from the Chu-Harrington bound

$$
Q_{\min} \approx \frac{1}{(k a)^{3}} + \frac{1}{k a}.
$$

**(c)** Estimate the maximum fractional bandwidth
$\text{FBW}_{\max} \approx 1 / Q_{\min}$ (for a VSWR ≤ 2 spec).

**(d)** The designer wants 100 MHz of usable bandwidth at 915 MHz. Is
that physically possible in a 15 mm sphere, or does the design require
either a larger antenna or a matching network with lossy tricks (e.g.
resistive loading) to synthesize more bandwidth at a gain penalty?

---

## Problem 7 — Mismatch that kills the amplifier

A power amplifier (PA) feeds a transmit antenna. The PA delivers a
forward power of **$P_{\text{fwd}} = +40\ \text{dBm}$** toward the
antenna. A protection/detector **diode** sits at the PA output; it
fails catastrophically if it must dissipate more than
**$P_{\max} = +30\ \text{dBm}$**. When the antenna is mismatched, the
reflected wave travels back down the feed and is absorbed at the PA
output stage — model **all** of the reflected power as landing on the
diode.

**(a)** Convert $P_{\text{fwd}}$ and $P_{\max}$ to watts.

**(b)** In terms of the reflection-coefficient magnitude $|\Gamma|$ at
the antenna, how much power is reflected back toward the PA?

**(c)** Find the largest $|\Gamma|$ the system can tolerate before the
diode is destroyed.

**(d)** Convert that $|\Gamma|_{\max}$ to a **VSWR** limit and a
**return-loss** limit. State the one-line rule you would put on the
datasheet ("keep VSWR below ___ / return loss above ___ dB").

**(e)** In one sentence: real transmitters put a **circulator or
isolator** between the PA and the antenna. How does that change the
picture you just computed?

---

**Documentation:**
