# Final Project — Radar Systems Report

The final project is **one report, in your own words**, on the radar you built
in Module 4: what the ADALM-PHASER hardware does, what each processing stage
does to the signal, and what your own measurements show. It is an exploration
of radar hardware and processing, written by someone who has run every stage
of it on a real kit.

## The labs are the scaffolding

The L28–L31 Labs are the steps toward the report. Each one sits on its
lesson's own page, after the lesson. Each one is a stage of a
single radar processing chain on your own kit, and each one hands you the
results, plots, and code that a section of the report is built on.

| Lab | Stage of the chain | What it gives your report | Objectives |
| :-- | :-- | :-- | :-: |
| [L28 Lab — FMCW Range](../L28-fmcw/index.md) | range, and the range waterfall, from one FMCW capture | how a chirp becomes a range measurement, and the resolution you actually got | 4.2, 4.5 |
| [L29 Lab — Range-Doppler and MTI](../L29-range-doppler-mti/index.md) | the range-Doppler map, then MTI | how velocity is measured, and what MTI removes and why | 4.5, 4.6 |
| [L30 Lab — CFAR Processing](../L30-cfar/index.md) | CFAR detections on your range-Doppler maps | how a detection is declared, and what set your false alarms | 4.7 |
| [L31 Lab — Micro-Doppler Spectrogram](../L31-classification-tracking/index.md) | classifying a detected target from its spectrogram, then tracking a walker in range and angle | what told your targets apart, how often it was right, and how well the radar held a moving person | 4.8, 4.9 |

Each lab starts from the one before it: your L29 processing begins with your
own L28 range code, the L30 Lab runs CFAR on your L29 maps, and the L31 Lab
classifies and tracks what your L30 detector found. Keep your code, data, and plots from
every lab.

## The lab packets are not the report

Turn in each lab packet as you finish the lab; it is checked and returned with
feedback so that problems surface while there is time to fix them. But a
stack of completed packets is **not** a final project. The packets answer the
questions the packet asks; the report explains the radar. Text and answers
lifted from your packets earn nothing in the report. What earns credit is
your explanation of why the results came out as they did, tied together into
one account of the system.

## When things are due

Everything is submitted on **Gradescope**. The lab packets come due one
at a time, starting at class period 32, in the order you run the labs; each
packet gives its own date. **The report is
due at class period 41**, the last class of the term. Period numbers are the
course calendar's class meetings, not the lesson numbers on this site.

## What is graded

The report is **30% of your course grade**, graded on a **rubric with a
sliding scale**: each of four areas is scored from 0 to 5, where 5 is
outstanding. Read it before you start, not after you finish. It rewards
understanding over results: a range resolution you can explain earns more
than one you merely report.

| Area | Score |
| :-- | :-: |
| Labs Completed | 0–5 |
| Engineering Analysis | 0–5 |
| Report Quality | 0–5 |
| Extra Effort | 0–5 |

## Extra credit

Do something with the radar that the labs did not ask for, and do it well:
a new kind of target, a processing stage of your own in Python, a second
moving target, a measurement the labs left out. Propose it to me in one
paragraph and get it approved **before** you start. Extra credit is earned by
the quality of the work, written up as its own section of the report.

## Individual work

The final project is individual: your own kit, your own code, and your own
report. Collaboration follows the [syllabus policy](../../syllabus.md):
discuss freely, but you must be able to explain every step you submit.
