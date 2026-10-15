# Final Project — Radar Lab Portfolio

The final project is the four Module 4 labs, taken together. Each one is a
stage of a single radar processing chain on your own ADALM-PHASER, and by the
end of the L31 Lab that chain takes a raw FMCW capture all the way to a
detected, classified target.

## What is graded

| Lab | Stage of the chain | Objectives |
| :-- | :-- | :-: |
| [L28 Lab — FMCW Range](../L28-lab-fmcw-range/index.md) | range, and the range waterfall, from one FMCW capture | 4.2, 4.5 |
| [L29 Lab — Range-Doppler and MTI](../L29-lab-range-doppler-mti/index.md) | the range-Doppler map, then MTI to separate movers from clutter | 4.5, 4.6 |
| [L30 Lab — CFAR Processing](../L30-lab-cfar/index.md) | CFAR detections on your range-Doppler maps | 4.7 |
| [L31 Lab — Micro-Doppler Spectrogram](../L31-lab-spectrogram/index.md) | classify a detected target from its micro-Doppler signature | 4.9 |

Together the four lab reports are **30% of your course grade**, in equal
parts. Each is graded on a **rubric with a sliding scale**, published with its
lab packet, so read it before the lab, not after. These reports are graded on
quality; they are not engagement credit, which comes from the Module 3 lab
packets.

## One chain, built a stage at a time

Each lab starts from the one before it. Your L29 processing begins with your
own L28 range code, the L30 Lab runs CFAR on your L29 maps, and the L31 Lab
classifies the targets your L30 detector found. Keep your code and your data
from every lab; the next one needs them.

## Individual work

The final project is individual: your own kit, your own code, and your own
reports. Collaboration follows the [syllabus policy](../../syllabus.md):
discuss freely, but you must be able to explain every step you submit.
