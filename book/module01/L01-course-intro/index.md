# L1 - Course Introduction


:::{admonition} Slides
:class: slides
<a href="../../slides/L01-course-intro.html" target="_blank" rel="noopener">html slides</a>
<a href="../../slides/L01-course-intro.html?print-pdf" target="_blank" rel="noopener">pdf slides</a>
<a href="../../slides/L01-course-intro.md" target="_blank" rel="noopener">raw markdown slides</a>
:::

## Learning Outcomes

By the end of this lesson, you will be able to:

<ol class="lo-list" style="--module: '1'">
  <li>State in plain language what an antenna is and what it does in a radio system.</li>
  <li>Explain why antennas matter to operators and engineers in the Air Force mission set (comms, radar, EW, SATCOM, GPS).</li>
  <li>Identify the five modules of ECE 444 and how they build toward the final capstone.</li>
  <li>Recognize several real antennas by sight and connect their geometry to the job they do.</li>
</ol>

## Welcome & Introductions

_Instructor and student introductions — background, career interests, prior exposure to RF or radar._

## About Your Instructor

**Lt Col Neil Rogers, USAF (Ret)** — BS from TU; MSEE and PhD from AFIT.
Currently the **Erdle Chair** at USAFA and a **Field Applications Engineer** at **Analog Devices**.

![Duty stations across the career](img/Duty_stations.png)
_DF/USAFA · AFRL Directed Energy, Kirtland AFB · NASIC and AFIT (×2), WPAFB · AFLCMC, Hanscom AFB._

![OTS commissioning](img/nr-ots.jpg)
_Officer Training School — where it started._

![Active Denial System 2](img/ads2.jpg)
_Active Denial System 2 at AFRL Directed Energy. Section chief for Active Denial and High-Power Sources._

![379th AEW deployment](img/ig-team.JPG)
_Deployment with the 379th AEW._

![E-8C Joint STARS](img/E8C.jpg)
_E-8C Joint STARS — airborne ground surveillance radar._

![ACUASR UAS Lab at USAFA](img/Rogers_UAS_Lab.jpg)
_Directed the Academy Center for UAS Research (ACUASR) at USAFA through 2025._

![USAFA retirement](img/usafa-retirement.jpg)
_Retirement from active duty — cadets sent me off with "No More Blues."_

My day job with **Analog Devices** puts me shoulder-to-shoulder with the team designing the **ADALM-PHASER** you'll use in Module 3, and customers designing advanced Comms and RADAR systems based on its technology.

![Analog Devices booth](img/nr-adi.jpg)
_Field Applications Engineer at Analog Devices — the folks who make the ADALM-PHASER._

## Outside the lab

![Family in the new house](img/fam_newhouse.jpg)
_Four kids (ages 11, 13, 15, 17). We just moved into a new house — fixing it up is a running hobby._

![CrossFit](img/CF_dying.png)
_CrossFit._

![Guitar at Trace church](img/trace_guitar.jpg)
_Playing guitar with the band at Trace, my church._

## How I teach

- **We're learning this together.** I don't have all the answers, and I'll say so when I don't.
- **Mistakes are part of learning.** Make them cheaply, and make them count.
- **Ask questions.** There is no such thing as a dumb question — if something isn't clicking for you, it's almost certainly not clicking for someone else.

## What is an antenna?

An antenna is the **transducer between a guided electromagnetic wave** (a signal traveling on a cable or waveguide) **and a freely propagating wave** (a signal traveling through space). Every wireless system on Earth has at least one on each end of the link.

Two ideas we'll keep coming back to:

1. Antennas are **reciprocal** — the same antenna transmits and receives with the same pattern.
2. Antennas do **not create energy** — they shape *where* the energy goes.

![RF link block diagram: RF Source → Amp → Transmission Line → TX Antenna → Channel → RX Antenna → LNA → Radio](img/rf-link-block-diagram.svg)
_A generic RF link. The antennas are the only components that touch free space; everything else is guided-wave._

## Why this matters to you

Antennas are the front door of every RF system the Air Force fields. If the antenna is wrong, nothing downstream can fix it.

- **Communications** — HF/VHF/UHF/SATCOM links, tactical radios, data links.
- **Radar** — surveillance, tracking, targeting, weather, altimeters.
- **Electronic warfare** — direction finding, jamming, protection.
- **Navigation** — GPS, TACAN, ILS, IFF.
- **ISR** — SIGINT payloads, synthetic aperture radar.

By the end of this course you will have designed, measured, and steered real antennas — the same class of hardware sitting on the aircraft, satellite, or ground station you may one day operate or specify.

## Course roadmap

Five modules, forty-one lessons, culminating in an integrated beamforming + radar capstone:

| Module | Focus |
| :-: | :- |
| 1 | Foundations of Electromagnetics and Antennas |
| 2 | Antenna Types, Simulation, and Measurement |
| 3 | Arrays and ADALM-PHASER Beamforming |
| 4 | Radar Fundamentals and FMCW |
| 5 | Final Capstone Project |

See the [syllabus](../../syllabus.md) for the full schedule and both project descriptions.

## Show & tell - real antennas + SDR

_Bring in a set of physical antennas (dipole, monopole, patch, horn, Yagi, small array) and demonstrate reception with an SDR (RTL-SDR / HackRF / Phaser) tuned to a live signal. Discuss what students see on the spectrum as antennas are swapped._

_Hardware checklist:_ `_TBD_`

## Demo - acoustic beam pattern

_Live demonstration of a small speaker array driven by a multi-channel audio interface, showing how phasing multiple sources produces a directional acoustic beam. Serves as an audible, tangible analog for the phased-array behavior we'll formalize in Module 3._

See the [acoustic antenna simulator concept](../../materials.md) for the build plan.

## Preparing for L2

Read the assigned sections on **field regions** before the next class — we'll formalize the boundary between the reactive near field, radiating near field, and far field, and connect these regions to how (and where) antennas are actually measured.
