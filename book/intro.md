---
frame_view: true
---

# ECE 444 — Antennas, Phased Arrays, and Radar Systems

::::{frame}
:class: title-frame

<div class="course-mark">USAFA · Dept. of Electrical &amp; Computer Engineering · Fall 2026</div>

<h1 class="frame-title">Antennas, Phased Arrays, and Radar Systems</h1>

<div class="title-rule"></div>

From Maxwell's equations to a working radar.

Four modules, 31 lessons, and a final project that puts hardware in your hands
and a moving target in your sights.

<div class="hero-pills">
<div class="hero-cta hero-grid">
  <a class="cta cta-primary" href="module01/index.html">Module 1</a>
  <a class="cta cta-primary" href="module02/index.html">Module 2</a>
  <a class="cta cta-primary" href="module03/index.html">Module 3</a>
  <a class="cta cta-primary" href="module04/index.html">Module 4</a>
</div>
<div class="hero-cta hero-grid hero-links">
  <a class="cta" href="syllabus.html#course-schedule">Schedule</a>
  <a class="cta" href="syllabus.html">Syllabus</a>
  <a class="cta" href="materials.html">Materials</a>
  <a class="cta" href="interactives.html">Interactives</a>
</div>
</div>
::::

::::{frame} Modules 1-3: Build the Antenna and the Beam

<div class="block-grid">
  <a class="block-card" href="module01/index.html">
    <span class="num">01</span>
    <h3>Foundations of Electromagnetics and Antennas</h3>
    <p>From Maxwell's equations to the parameters that describe any radiator: gain, directivity, polarization, beamwidth.</p>
    <footer>Lessons 1–6</footer>
  </a>
  <a class="block-card" href="module02/index.html">
    <span class="num">02</span>
    <h3>Antenna Types, Simulation &amp; Measurement</h3>
    <p>Dipoles, loops, patches, horns, and arrays — simulated in software, then measured on the bench.</p>
    <footer>Lessons 7–14</footer>
  </a>
  <a class="block-card" href="module03/index.html">
    <span class="num">03</span>
    <h3>Arrays &amp; ADALM-PHASER Beamforming</h3>
    <p>Steer a beam, taper the sidelobes, and null a jammer — on real hardware you configure yourself.</p>
    <footer>Lessons 15–24</footer>
  </a>
</div>
::::

::::{frame} Module 4: Give It Something to Look For

<div class="block-grid">
  <a class="block-card" href="module04/index.html">
    <span class="num">04</span>
    <h3>Radar Fundamentals &amp; FMCW</h3>
    <p>Send it, receive it, and find your target: range, Doppler, MTI, and CFAR processing on the ADALM-PHASER.</p>
    <footer>Lessons 25–31</footer>
  </a>
  <a class="block-card" href="module04/final-project/index.html">
    <span class="num">FP</span>
    <h3>Final Project</h3>
    <p>One report, in your own words, on the radar you build in the L28–L31 Labs, from an FMCW capture to a detected, classified target.</p>
    <footer>Built on the L28–L31 Labs</footer>
  </a>
</div>
::::

::::{frame} What You Are Graded On

<div class="deliverable-cards">
  <div class="deliverable-card">
    <p class="d-eyebrow">Module assessments</p>
    <h3>LO Mastery</h3>
    <p class="d-weight"><span class="d-w-num">30%</span> of course grade</p>
    <p class="d-due">Each learning objective scored Mastered or Not Yet Mastered</p>
    <a class="d-link" href="syllabus.html#lo-mastery-assessment">How mastery grading works →</a>
  </div>
  <div class="deliverable-card">
    <p class="d-eyebrow">Individual deliverable</p>
    <h3>Midterm Project</h3>
    <p class="d-weight"><span class="d-w-num">30%</span> of course grade</p>
    <p class="d-due">Antenna pattern measurement · introduced <strong>Lesson 9</strong>, due <strong>2 Oct, 2359</strong></p>
    <a class="d-link" href="syllabus.html#midterm-project-assessment">How it is graded →</a>
  </div>
  <div class="deliverable-card">
    <p class="d-eyebrow">Individual deliverable</p>
    <h3>Final Project</h3>
    <p class="d-weight"><span class="d-w-num">30%</span> of course grade</p>
    <p class="d-due">Radar systems report, in your own words, built on the L28–L31 Labs · due <strong>class period 41</strong></p>
    <a class="d-link" href="syllabus.html#final-project-assessment">How it is graded →</a>
  </div>
  <div class="deliverable-card">
    <p class="d-eyebrow">Ongoing</p>
    <h3>Engagement</h3>
    <p class="d-weight"><span class="d-w-num">10%</span> of course grade</p>
    <p class="d-due">Module 3 lab packets, practice problems, EI, and course-improvement contributions</p>
    <a class="d-link" href="syllabus.html#engagement-credits-ec">Ways to earn engagement →</a>
  </div>
</div>
::::

::::{frame} Course Objectives 1-3
By the end of this course you should be able to:

1. Describe fundamental antenna properties — gain, directivity, polarization, impedance — and connect them to system-level radio performance.
2. Model, simulate, and measure common antenna types using industry-standard tools and lab equipment.
3. Apply phased-array theory — array factor, beam steering, tapering, null steering — using the ADALM-PHASER platform.
::::

::::{frame} Course Objective 4

4. Analyze radar performance using the radar equation, detection theory, and FMCW signal processing (range, Doppler, CFAR), and apply it on the ADALM-PHASER to detect, classify, and track a moving target.
::::

::::{frame} How This Course Is Graded

:::{callout}
Every learning objective is scored on a **binary 1 / 0** scale — no partial
credit. A 0 comes with detailed feedback rather than the answer, and if you
submitted real effort on time you may **revise your work** until you earn
the 1.
:::

The bar is simple: I want you to learn this material, and I would rather you
learn it late than not at all.
::::

::::{frame} Rules of Engagement
1. **The website is the course.** Lesson pages, practice problems, and slide decks are updated during the semester — pull the latest before class.
2. **Practice problems are your reps.** They are ungraded for correctness but graded for a genuine, documented attempt. Do the work.
3. **EI early and often.** It is the single best predictor of doing well in this course, and it counts toward engagement.
4. **Ask questions in public.** If you had it, someone else had it too. The person who was afraid to ask is grateful.
::::

::::{frame} What Each Lesson Contains
- **Reading.** Expanded notes on the objective — the equations worked through, the diagrams annotated, the connections to real hardware called out.
- **Slides.** The deck used in class. Open it in a browser and read along.
- **Practice problems.** Ungraded reps keyed to the lesson's learning objectives, with worked solutions on a separate page.
- **Labs and projects**, where they apply. Pre-lab plan, procedure, and rubric — plus links to the midterm and final project packets.

:::{depth}
The contents of this website are for educational use only and do not
necessarily reflect the official policy or position of the United States Air
Force Academy, the Department of the Air Force, or the U.S. Government.
:::
::::
