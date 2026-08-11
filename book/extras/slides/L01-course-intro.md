<!-- .slide: class="title-slide" -->

<div class="title-left">

# ECE 444

Antennas, Phased Arrays, and Radar Systems

## Lesson 1 — Course Introduction

Fall 2026 · Dr. Neil Rogers

</div>

<div class="title-right">

![USAFA](./img/01-course-intro/USAFA-logo.png)

</div>

---

## Welcome

- Who I am
- Who you are
- What this course is going to ask of you

Note:
Instructor bio; ask each student for name, background, one thing they hope to learn.

---

## About your instructor

**Lt Col Neil Rogers, USAF (Ret.)**

<small>BS — TU · MSEE — AFIT · PhD — AFIT</small>

**Erdle Chair**, USAFA
**Field Applications Engineer**, Analog Devices

---

## Where I've been

![Duty stations](./img/01-course-intro/Duty_stations.png)

<small>DF/USAFA · AFRL Directed Energy · NASIC · AFIT ×2 · AFLCMC</small>

---

## Antennas, radar, and high-power RF

<div style="display:grid;grid-template-columns:repeat(3,1fr);gap:0.4em;align-items:center;">
  <img src="./img/01-course-intro/nr-ots.jpg" alt="OTS" style="max-height:180px;object-fit:cover;">
  <img src="./img/01-course-intro/ads2.jpg" alt="Active Denial System 2" style="max-height:180px;object-fit:cover;">
  <img src="./img/01-course-intro/ig-team.JPG" alt="379th AEW" style="max-height:180px;object-fit:cover;">
  <img src="./img/01-course-intro/E8C.jpg" alt="E-8C Joint STARS" style="max-height:180px;object-fit:cover;">
  <img src="./img/01-course-intro/Rogers_UAS_Lab.jpg" alt="ACUASR UAS Lab" style="max-height:180px;object-fit:cover;">
  <img src="./img/01-course-intro/usafa-retirement.jpg" alt="Retirement" style="max-height:180px;object-fit:cover;">
</div>

<small>OTS · ADS2 · 379th AEW · E-8C · ACUASR · retirement</small>

Note:
Section chief for Active Denial and High-Power Sources at AFRL Directed Energy.
E-8C Joint STARS work at NASIC.
Directed the Academy Center for UAS Research (ACUASR) at USAFA through 2025.

---

## Now — Analog Devices

<p style="text-align:center;">
<img src="./img/01-course-intro/nr-adi.jpg" alt="Analog Devices">
</p>

**Field Applications Engineer** with the team behind the
**ADALM-PHASER** you'll use in Module 3.

---

## Off the clock

<div style="display:grid;grid-template-columns:auto 1fr;gap:0.6em 1em;align-items:center;max-width:720px;margin:0 auto;">
  <img src="./img/01-course-intro/fam_newhouse.jpg" alt="Family" style="height:130px;width:220px;object-fit:cover;">
  <div style="font-size:0.75em;">Family — four kids (11 · 13 · 15 · 17)</div>

  <img src="./img/01-course-intro/CF_dying.png" alt="CrossFit" style="height:130px;width:220px;object-fit:cover;">
  <div style="font-size:0.75em;">CrossFit</div>

  <img src="./img/01-course-intro/trace_guitar.jpg" alt="Guitar" style="height:130px;width:220px;object-fit:cover;">
  <div style="font-size:0.75em;">Guitar with the band at <strong>Trace</strong> church</div>
</div>

---

## How I teach

- **We're learning this together** — I don't know it all.
- **Mistakes are part of learning** — make them, and make them count.
- **Ask questions** — there is no such thing as a dumb one.

---

## What is an antenna?

<div class="slide-box">

An antenna is a **transducer**. It converts a **guided wave** on a
cable or waveguide into a **radiating wave** in free space, and
vice versa.

Two ideas we'll keep coming back to:

1. Antennas are **reciprocal** — the same antenna transmits and receives with the same pattern.
2. Antennas do **not create energy** — they shape *where* the energy goes.

</div>

Note:
Reciprocity: same antenna, same pattern, transmit or receive.
Antennas do not create energy — they shape where the energy goes.

---

## Every wireless system has one

![RF link block diagram: RF Source → Amp → Transmission Line → TX Antenna → Channel → RX Antenna → LNA → Radio](./img/01-course-intro/rf-link-block-diagram.svg)

<div class="callout">
If the antenna is wrong, nothing downstream can fix it.
</div>

---

## Why you should care — the AF mission

- **Comms** — HF/VHF/UHF/SATCOM, tactical radios, data links
- **Radar** — surveillance, tracking, targeting, weather
- **EW** — direction finding, jamming, protection
- **Nav** — GPS, TACAN, ILS, IFF
- **ISR** — SIGINT, synthetic aperture radar

---

## Course roadmap

1. Foundations of Electromagnetics and Antennas
2. Antenna types, simulation, measurement
3. Arrays and ADALM-PHASER beamforming
4. Radar fundamentals and FMCW
5. Capstone Project — beamforming + radar

<small>41 lessons, ~15 labs, 2 projects.</small>

---

## Course schedule

<div class="schedule-grid">
  <!-- Row 1: module number + title -->
  <div class="mod-top"><span class="mod-num">1</span><span class="mod-title">Foundations</span></div>
  <div class="mod-top"><span class="mod-num">2</span><span class="mod-title">Antenna Types &amp; Measurement</span></div>
  <div class="mod-top"><span class="mod-num">3</span><span class="mod-title">Arrays &amp; Beamforming</span></div>
  <div class="mod-top"><span class="mod-num">4</span><span class="mod-title">Radar &amp; FMCW</span></div>
  <div class="mod-top"><span class="mod-num">5</span><span class="mod-title">Capstone Project</span></div>

  <!-- Row 2: lesson range -->
  <div class="mod-lessons">L1 – L6</div>
  <div class="mod-lessons">L7 – L14</div>
  <div class="mod-lessons">L15 – L28</div>
  <div class="mod-lessons">L29 – L38</div>
  <div class="mod-lessons">L39 – L41</div>

  <!-- Row 3: activities + project milestones -->
  <div class="mod-bottom">
    <div>EM &amp; antenna theory</div>
  </div>
  <div class="mod-bottom">
    <div>3 labs</div>
    <div><span class="milestone">Midterm intro · L11</span></div>
  </div>
  <div class="mod-bottom">
    <div>7 labs · ADALM-PHASER</div>
    <div><span class="milestone">Midterm due · L20</span></div>
  </div>
  <div class="mod-bottom">
    <div>6 labs</div>
  </div>
  <div class="mod-bottom">
    <div><span class="milestone">Beamforming + radar</span></div>
  </div>
</div>

---

## Two projects

**Midterm** — Antenna Pattern Measurement
- Introduced L11, due L20

**Final** — Combined Beamforming + Radar
- Track a moving target while suppressing a static jammer

---

## Homework

---

## Show & tell

Real antennas + a software-defined radio.

<!-- physical antennas laid out on bench:
     dipole · monopole · patch · horn · Yagi · small array -->

<!-- SDR (RTL-SDR / HackRF / Phaser) tuned to a live signal;
     swap antennas and observe the spectrum change -->

Note:
Have students predict which antenna will work best for which signal,
then show them the result on the SDR waterfall.

---

## Demo — acoustic beam

Phased array, but audible.

<!-- multi-channel audio interface + Class-D amp
     driving a small speaker line array;
     sweep steering angle so students hear the null / peak -->

Note:
This is our stand-in for phased-array intuition
until we get to Module 3 with the Phaser.

---

## For next time

<!-- TODO: source syllabus-qr.png and place at book/module01/L01-course-intro/img/syllabus-qr.png
<figure class="qr qr-right">
  <img src="./img/01-course-intro/syllabus-qr.png" alt="QR to syllabus">
  <figcaption>Syllabus</figcaption>
</figure>
-->

Reference:

- Sections 1-1 through 1-11.7 in [Milligan — *Modern Antenna Design*](../_static/materials/Antenna-design-Milligan.pdf)
- Sections 3.1 through 3.9 in [Rohde &amp; Schwarz — *Antenna Basics*](../_static/materials/Antenna_Basics_8GE01_1e_Rohde-Schwarz.pdf)

<div class="callout">

Next lesson: the fundamental **antenna properties**.

</div>
