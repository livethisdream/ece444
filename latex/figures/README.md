# Figures for the L4 matching lab

`ECE444_Lab_L04_Matching.tex` looks for these here. They are detected with
`\IfFileExists`, so the packet compiles either way — with the photographs if
they are present, with labelled placeholder boxes if not. Nothing in the
source needs editing to switch between the two.

| File | What it shows | Used in |
| :-- | :-- | :-- |
| `vna_annotated.jpg` | The NanoVNA with callouts: on/off switch, touch screen, input buttons, Ch 0 (source / reflection), Ch 1 (transmission), SMA cable | Familiarization views, left panel |
| `nano_vna_initial.jpg` | The NanoVNA screen with the four default traces overlaid | Familiarization views, right panel |
| `annotated_vna_readout.jpg` | The same screen with the marker readout called out — trace/scale, marker value, marker frequency | Reading the display, Part I |
| `cal_standards_annotated.jpg` | The three SMA calibration standards, labelled load / short / open | Calibration, Part I |
| `vna_front.jpg` | The unannotated NanoVNA — the source photograph `vna_annotated.png` was drawn over. Not used by the packet; kept so the callouts can be redrawn. | — |

`annotated_vna_readout.jpg` is **generated**, not photographed:
`scripts/graphics/l04_lab_vna_readout.py` crops the callouts onto
`nano_vna_initial.jpg`. Re-run it after replacing that photograph, or delete
the script and drop in a hand-annotated screenshot under the same name.

These are stored at print resolution, not at camera resolution: the packet
prints them between 3 and 6 inches wide, so 900-1600 px on the long edge is
about 200 dpi and nothing is lost. The full-resolution uploads are in git
history at `a776d04` if a bigger crop is ever needed. Keeping them small
matters -- the photographs are embedded in the published PDF, and the
originals made it an 11 MB download instead of 1.5 MB.

The blank Smith chart the packet includes as a plotting page is not here — it
is a published course handout and lives at
`book/extras/handouts/SmithChart_blank.pdf`, pulled in from there so there is
only one copy.
