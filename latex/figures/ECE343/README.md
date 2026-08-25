# VNA photographs for the L4 matching lab

`ECE444_Lab_L04_Matching.tex` looks for four images here. Drop them in with
these exact basenames (`.png` or `.jpg` both work) and the next build picks
them up automatically — no source edit needed. If any are missing the packet
still compiles, substituting a labelled placeholder box, so a partial set is
fine while you collect the rest.

| Basename | What it shows | Used in |
| :-- | :-- | :-- |
| `vna_annotated` | The NanoVNA with callouts: on/off switch, touch-screen display, input buttons, Ch 0 (source / reflection), Ch 1 (transmission), SMA cable | Fig. "Familiarization views", left panel |
| `nano_vna_initial` | The NanoVNA as it looks at power-on, before any calibration | Fig. "Familiarization views", right panel |
| `annotated_vna_readout` | A screen capture of the display with the traces and marker readout called out | Reading the display, Part I |
| `cal_standards_annotated` | The three SMA calibration standards, each labelled load / short / open | Calibration, Part I |

Source: these are the same photographs used in the ECE 343 VNA lab. They live
here rather than in a OneDrive folder so that a fresh clone of this repo builds
the identical packet on any machine.

Keep them modest in size — the packet includes them at `scale=0.23` (the two
familiarization views) and `scale=0.5` (the readout and the cal standards), so
roughly 1200-1600 px on the long edge is plenty.
