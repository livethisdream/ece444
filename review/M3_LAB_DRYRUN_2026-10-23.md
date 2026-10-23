# PHASER Lab Dry Run: Module 3 Findings and Changes

Oct 23, 2026 · @Neil

## Summary

Every Module 3 PHASER lab (L17–L24) ran on phaser-00 on 2026-10-19 and 2026-10-23. The physics checks out everywhere it can be read from a pattern's shape: steering, beamwidth, nulls, sidelobes, grating lobes, squint, quantization and scan loss all match theory within about a degree or a decibel. What needs work is the lab text, the kit's dashboard and a few hardware assumptions. One lab, L24 Procedure C, cannot run on hardware as written, and L19 was redesigned.

- **Gain slider:** the Element Gains slider is not linear in voltage. Amplitude goes as (%/100)^0.68, which makes every taper milder than the L22 lab predicts.
- **Peak levels:** peak-level comparisons fall 1–3 dB short of theory, even with elements fully on or off. Shape measurements are unaffected.
- **Nulls:** the notches and nulls in L24 reach −40 to −50 dB, not the −21 dB floor limit the lab describes.
- **Bench conditions:** a nearby wall, a person beside the kit, or a stale calibration can each put a false lobe 9 dB below the peak.
- **Dashboard:** phaser-00 lacks two modes the labs rely on (Signal vs Time for L21, Tracking for L24). The kits need the current `phaser` install.
- **Interferer:** two HB100s are rarely on the same frequency, so L24 Procedure C needs matched pairs or a backend interferer.
- **L19:** redesigned as a firing range, with a new procedure, packet and student starter script.

## Setup

One kit ran every lab, but distance, gain and calibration changed between sessions; each lab section restates its own setup.

| Item | 2026-10-19 (L17, L18, L20) | 2026-10-23 (L19, L21, L22–L23, L24) |
| --- | --- | --- |
| Kit | phaser-00, already provisioned (L17 Part A not rerun) | same kit, moved off the wall partway through L22–L23 |
| Signal Freq (Find HB100) | 10.408 GHz | 10.443 GHz (10.4429) |
| IF | 1.690 GHz | 1.690 GHz |
| Calibration | the existing L17 calibration | recalibrated at the start of L22–L23 |
| Source distance | 1 m (L17, L18 Runs 1–2); about 4 ft / 1.22 m (L18 scan loss, L20) | 1.2–1.6 m |
| Rx Gain | 10 dB (L17 Steps 1–5, clipped); 1 dB otherwise | 1 dB; 4 dB for L21 and L24 |
| Sweep | Lab Preset 1 or 2, 7 bits, 162 points, 2.8125° LSB | same |

Predictions in this doc are recomputed at the kit's own frequency, not the labs' nominal 10.525 GHz or 10.3 GHz.

## L17: Bring-Up (Part B)

Part B passes on every check. At the lab's Rx Gain of 10 dB, however, the FFT peak goes over full scale.

| Step | Source | Rx Gain | Est. Angle | Peak Array Gain | FFT peak / floor |
| --- | --- | --- | --- | --- | --- |
| 3–5 | boresight, 1 m | 10 dB | −1.8° | 5.0 to 5.5 dB | +3 / −70 dBFS |
| 6 | \~30°, toward E1 | 1 dB | −31° | −4.0 dB | −6 / −78 dBFS |
| 7 | boresight again | 1 dB | 0° | −3.7 dB | −6 / −78 dBFS |

- At Rx 10 the tone read +2 to +3.4 dBFS, and an image tone appeared 0.19 MHz on the other side of zero.
- The peak sits 72 dB above the FFT floor; the lab asks for at least 20.
- Step 6 asks which end, E1 or E8, the source moved toward, but L17 never says where E1 is. L18 defines +θ as the E8 end, so the −31° reading means the source was toward E1.
- The Lab Preset buttons only worked once the Lab Presets section was expanded.

## L18: Beam Steering

Both runs put the peak at the commanded or physical angle, within the lab's ±2° budget except at 45°. Rx Gain was 1 dB and the source 1 m away.

| Run | Target | Est. Angle | Peak | HPBW (meas / pred) | Sidelobes (dBc) |
| --- | --- | --- | --- | --- | --- |
| A (move source) | 0° | +0.9° | −3.94 dB | 13.8° / 13.2° | −14.2 / −12.1 |
| A | +30° | +29.9° | −4.16 dB | 15.8° / 15.3° | −15.0 / −12.1 |
| A | +45° | +47.7° | −4.35 dB | 21.0° / 18.9° | −13.5 / −13.3 |
| B (Apply) | 15° | +16.8° | −3.95 dB | 14.5° / 13.6° | −13.8 / −12.4 |
| B | 30° | +32.1° | −3.95 dB | 16.5° / 15.3° | −13.8 / −12.4 |
| B | 45° | +47.7° | −3.90 dB | 21.2° / 18.9° | −13.5 / −12.7 |

- **Phase Control after Apply 30:** 0, −87, −175, −262, −350, −437, −525, −612. That is exactly −n·87.5° at 10.408 GHz, so the sign and the unwrapped values match the lab.
- **Angle offsets:** the commanded runs read 1.8° to 2.7° high. This most likely comes from where the source sat at boresight. Apply shifts the peak from wherever the source actually is.
- **Grid check:** the plot's angle axis matches kd at 10.4 GHz, so the offsets are not a frequency mismatch.
- **Peak marker:** at 45° the GUI's angle readout sometimes jumps to −90°, because the crowded points at the plot's edge briefly read higher than the main lobe.

**Scan loss, measured at about 4 ft:**

| Angle | Measured | Ideal cos θ | Patch, cos^1.3–1.5 θ |
| --- | --- | --- | --- |
| 30° | −0.7 dB | −0.6 dB | −0.8 to −0.9 dB |
| 45° | −1.0 dB | −1.5 dB | −2.0 to −2.3 dB |

The 30° point matches theory. The 45° point shows less loss than even the ideal bound, which points to multipath or HB100 aim. At 1 m the measured drop was only 0.2 to 0.4 dB, so 1 m is too close for this measurement.

## L19: Fox Hunt (Single-Kit Rehearsal)

The three tripod bearings fixed the HB100 to 21 cm, meeting the lab's \~0.2 m expectation. Aiming by eye was the dominant error. The HB100 sat at a known spot, the origin, so this tested the method rather than a blind hunt. Rx Gain was 1 dB.

Reference shot: with the source to the right of broadside, seen from behind the array, Est. Angle read +17.3°, so s = −1 on this kit. E8 is on the right as seen from behind the array.

| Position | Kit (x, y) | Range | Est. Angle | Bearing β | Peak Array Gain | Line misses HB100 by |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | (0, 63") | 1.60 m | +2.75° | −92.8° | −6.6 dB | 7.7 cm |
| 2 | (−23", 52") | 1.44 m | +2.66° | −68.8° | −6.8 dB | 6.7 cm |
| 3 | (+23", 52") | 1.44 m | −3.67° | −110.2° | −13.5 dB | 9.2 cm |
| 4 | (40", 28"), hand-held | 1.24 m | +16.2° | −161.2° | −29.0 dB | 35 cm |

- **Fix error is mostly in depth.** Positions 1–3 fix to (−0.02, −0.21) m, because all three look in from one side.
- **Leave-one-out can miss a bad bearing.** With all four positions, it could not tell bearing 4 from bearing 3 (6.2 vs 6.5 cm).
- **The aiming error isn't a fixed bias.** The readings change sign between mirrored positions, and hand-holding gave 16°.
- **HB100 facing matters for level.** Mirrored positions at the same range differed by 6.7 dB.

**Outcome: L19 redesigned as a firing range.** The kits sit on a taped line, square to it and pointed straight downrange, and move along station marks. Every station shares one heading, so there is no per-station aim. Bearings give the fix, and Peak Array Gain ranks the boxes nearest it. A Monte Carlo sized the layout, assuming 2.5° bearings, 1 in 7 off by 10°, and the HB100 aimed ±20° at the line:

| Layout | Box field | Stations | Right box | Median fix error |
| --- | --- | --- | --- | --- |
| 2.0 m line | 1.5 m wide, 1.0–2.0 m deep | 7 | 90% | 0.15 m |
| **3.0 m line (chosen)** | **2.0 m wide, 1.0–2.0 m deep** | **7** | **93%** | **0.16 m** |
| 4.0 m line | 3.0 m wide, 1.0–2.0 m deep | 7 | 96% | 0.16 m |

The chosen layout fits in about 3 m × 2.5 m.

## L20: Array Factor

Beamwidth tracks the active aperture as predicted. The peak steps between apertures fall short of 6 dB. Source at about 4 ft, Rx Gain 1 dB, element gains 100.

| Active | HPBW (meas / pred) | FNBW (meas / pred) | First SLL (dBc) | Peak (dBFS) | Drop vs. 8 (meas / pred) |
| --- | --- | --- | --- | --- | --- |
| 8 (E1–E8) | 13.4° / 13.2° | 29.8° / 29.8° | −12.5 / −14.0 (pred −12.8) | −5.25 | 0 / 0 dB |
| 4 (E3–E6) | 27.4° / 27.1° | \~67° / 62.0° | −12 to −14 (pred −11.3) | −10.4 | −5.1 / −6.0 dB |
| 2 (E4, E5) | \~56° (52–58) / 61.9° | none / 180° | none | −15.1 | −9.9 / −12.0 dB |

- **4-element FNBW:** reads wide because the left null fills to the noise floor, about −23 dBc, so its position is uncertain.
- **2-element trace:** sits well above the floor. It falls about 27 dB to near −40 dBFS at ±80°, which is the 2-element array factor's own roll-off toward endfire. The lab's claim that this peak is only 11 dB above the floor did not hold on this kit.
- **Clearing frozen traces:** a press-and-hold on Freeze clears them, as the GUI describes.

## L21: Antenna Pattern (Trimmed)

The rotation confirms both of Lesson 21's element-pattern predictions. The walk couldn't run: phaser-00's dashboard lacks the Signal vs Time mode that preset 7 needs. Instead, one rotation pass read both beam-held runs from each sweep's 0° and 29.8° points, and the sweep's Est. Angle supplied the true angle when the kit slid about 5°. Setup: about 1.2 m out, Rx Gain 4 dB.

| Prediction | Measured | Lab |
| --- | --- | --- |
| Scan loss, beam at 30° | −0.9 dB at a true 33° | −0.6 ideal, −0.9 patch |
| Inner first sidelobe, beam at 30° | −10.8 dBc at 6.5° | −12.2 dBc near 8° |
| Outer first sidelobe, beam at 30° | −14.2 dBc at 56.5° | −15.1 dBc near 59° |
| Asymmetry | 3.4 dB | 2.9 dB |
| First null, beam at 0° | 14.9° | 14.7° |
| Behind the board, 180° | −28.8 dB, beam at 0° | floor |

## L22–L23: Tapering, Squint, and Quantization

Every Part 2 measurement matched the lab. Part 1's tapers came out consistently milder than their slider values. The setup was about 4 ft at Rx Gain 1 dB and 10.443 GHz, recalibrated at the start.

**Part 1, tapers.** Predictions assume slider % equals voltage, at 10.443 GHz.

| Preset | Sliders (%) | HPBW meas / pred | Peak drop meas / pred | First sidelobe |
| --- | --- | --- | --- | --- |
| Uniform | 100 × 8 | 13.5° / 13.1° | 0 (ref −7.38 dBFS) | −12.5 / −12.2 dBc |
| Hann | 12, 43, 77, 100 | 17.2° / 18.9° | −3.7 / −4.7 dB | below the floor (\~−31 dBc) |
| Blackman | 6, 27, 66, 100 | 18.3° / 21.4° | −4.7 / −6.1 dB | at the floor (−22 to −25 dBc) |
| Chebyshev | 4, 23, 62, 100 | 18.9° / 22.6° | −5.1 / −6.5 dB | at the floor (−20 to −22 dBc) |
| Custom (d) | 25, 50, 90, 100 | 16.2° (spec ≤ 17°) | −2.8 dB | −23 dBc (spec < −20) |

- **The slider is not linear in voltage.** Taking the amplitude as (%/100)^0.68 fits all three peak drops within 0.1 dB, and it predicts the beamwidths within about 0.5° without being fitted to them. The backend maps the slider linearly onto the ADAR1000 gain register, so the curve is the chip's own response.
- **The same curve fits L20.** It puts 50% at −4.1 dB, and a single element at 50% measured −3.8 dB.
- **The lab's numbers need updating.** Its peak drops overshoot by 1.0–1.4 dB and its beamwidths by 2–5°, and computed η\_t overstates the loss. The suggested custom taper, with ends at 45%, gave −18 dBc and missed the spec; ends at 25% passed.

**Part 2.**

| Step | Measured | Lab expects |
| --- | --- | --- |
| (f) Rx1, Rx4, Rx7 | lobes −43.6° / +42.3°, full height; drop −7.8 dB | ±43°; −8 to −9 dB |
| (f) Rx1, Rx5 | lobes −33.0° / +29.8°; both ends climbing; drop −10.9 dB | ±30 to ±33°; −11 to −12 dB |
| (g) Squint, source at 41.1° | +41.1° → +43.6°, shift +2.5° | +2.6° for 41.1° |
| (h) 7 / 4 / 3 / 2 bits | −17.4 (floor) / −15.5 / −12.0 / −8.5 dBc beyond ±35° | floor / −15 to −21 / −12 to −15 / −8 to −10 dBc |

- **Reflections near the bench matter most.** Beside a wall, a lobe appeared at −37° to −41°, 9 dB below the peak. In open space it fell to the floor, about −17 dBc.
- **Est. Angle moves at low bit counts.** It read +8.4° at 4, 3 and 2 bits, against +1.8° at 7, with the source fixed.
- **Signal BW resets to 0** after Calibrate and after the Rect preset, and step (g) depends on it.
- **The slider curve isn't the whole story.** Grating-lobe peak drops also fall short (−7.8 vs −8.5, −10.9 vs −12.0 dB) with elements fully on or off, so the curve alone doesn't explain the L20 shortfall.

## L24: Null Steering

Procedures A, B and D ran on hardware, with nulls far deeper than the lab predicts. Procedure C could not run on hardware.

| Procedure | Measured | Lab |
| --- | --- | --- |
| A: main-lobe loss | −1.78 dB | −1.8 dB |
| A: notch bottom | −46 to −50 dB below the uniform peak, at +25.7° | about −21 dB, floor-limited |
| B: difference null | −41.5 dB, on the source at +0.9° | about −22 dBc |
| D: delta null and error zero | −39.7 dBc at +0.9°; error zero at +1.4° | −21.8 dBc at boresight |

- **Procedure C on hardware:** the two HB100s sat 15 MHz apart, outside the ±1.5 MHz receiver window, and the tuning screw barely moved. The dashboard's interferer setting is simulator-only. A hand-held metal plate made a reflection of only −12 dBc.
- **Procedure C in the hosted simulator** (interferer 10 dB stronger): at ±20°, MVDR suppressed the interferer by 16 dB but also cut the target by 30 dB. At ±30° it suppressed 12 dB with a 4.5 dB target loss. The lab says MVDR holds the look direction, and here it doesn't. Coherent simulated sources are a likely cause.
- **The lab disagrees with itself:** Procedure C uses +30°, but its "Two limits" frame says suppression falls away there and recommends +20°.

## Cross-Cutting Findings

These show up in more than one lab, and most of the needed changes trace back to them.

### 1. The Element Gains slider is not linear in voltage

The element amplitude goes as (%/100)^0.68, not %/100. One exponent, fitted to the three L22 peak drops, reproduces them within 0.1 dB and predicts the beamwidths within about 0.5°. The same curve puts 50% at −4.1 dB, against −3.8 dB measured for a single element in L20. The backend maps the slider linearly onto the ADAR1000's 0–127 gain register (`_apply_gain_cal` in `phaser_headless.py`), so the curve is the chip's register response. It is fixable once, in the backend, with a measured lookup table. Labs affected: L20 (gain-50 test), L22–L23 Part 1, and L24 Procedure A (weights of 65–82%).

### 2. Bench conditions dominate the small numbers

- **Reflections:** with the kit beside a wall, a lobe appeared at −37° to −41°, only 9 dB below the peak. In open space it fell to the floor. A person seated beside the kit still left a −17 dBc shelf on that side.
- **Calibration:** a stale calibration can produce the same lopsided uniform trace; recalibrating fixed it once.
- **Distance:** at 1 m, scan loss read 0.2–0.4 dB; at 1.2 m it read correctly (−0.7 dB at 30°). Level comparisons under 1 dB need at least 1.2 m.
- **Placement:** the kit slid about 5° on the protractor in L21, and aiming by eye cost 3–16° per bearing in the L19 rehearsal.

### 3. The kit's dashboard is behind the current code

phaser-00 lacks the Signal vs Time mode (the L21 walk) and the Tracking mode (L24 Procedure D, step 4) that the current `phaser` repository has. Its preset 8 also loads Blackman rather than uniform, and doesn't reset Beam 1 Phase. Signal BW resets to 0 after Calibrate, Find HB100 and the Rect preset, and Find HB100 also resets Rx Gain and can leave the sweep frozen until it is restarted.

### 4. Every kit sits at its own frequency

The two sessions found 10.408 and 10.443 GHz, and a second HB100 sat at 10.4575 GHz, 15 MHz from the first. The receiver sees about ±1.5 MHz, so predictions must use each kit's own Find HB100 value, and any lab that needs two sources at once (L24 Procedure C) needs them matched within about 1 MHz. Find HB100 with only one source on reads that source to about 10 kHz.

### 5. Rx Gain 10 dB clips at the labs' distances

At 1 m and Rx Gain 10 dB the FFT peak read +2 to +3 dBFS, with an image tone. Rx 1–4 dB kept the FFT peak at −9 to −14 dBFS, inside the −10 ± 3 dBFS window that L19 and L21 specify.

### 6. Peak levels fall 1–3 dB short of theory

The array's peak reads 2–3 dB below the in-phase sum of its single elements. The shortfall grows with the number of elements (0.3, 1.3 and 2.2 dB at 2, 4 and 8 elements), and it also appears in L22's grating-lobe runs, where every element is fully on or off (−7.8 against −8.5 dB, and −10.9 against −12.0 dB). Three tests ran in L20.

**Test 1, element leakage (ruled out).** With all eight gains at 0, the residual peak was −38.8 dBFS, 33.5 dB below the full array. That is about 2% voltage per element, enough to explain at most 0.5 dB of the shortfall.

**Test 2, single elements at gain 100.** E1–E4 and E7–E8 each read about −21.1 dBFS, E5 −20.5 and E6 −22.0. The element gains match within ±0.6 dB. Adding those voltages in phase predicts each aperture's peak:

| Active | Predicted from singles | Measured | Shortfall |
| --- | --- | --- | --- |
| 2 (E4, E5) | −14.8 dBFS | −15.1 dBFS | 0.3 dB |
| 4 (E3–E6) | −9.1 dBFS | −10.4 dBFS | 1.3 dB |
| 8 (E1–E8) | −3.0 dBFS | −5.25 dBFS | 2.2 dB |

**Test 3, all gains at 50 (rules out compression).** The 8-element peak fell to −10.2 dBFS and E4 alone to −24.9 dBFS. The step is 14.7 dB against an ideal 18.1, so the shortfall grew to 3.4 dB. If compression were the cause, lowering the level would have shrunk the shortfall. Beamwidth (13.1°) and sidelobes did not change.

**What remains:**

- **The slider curve explains part of it.** Finding 1 accounts for the gain-50 single-element reading, but not the shortfall with elements fully on or off.
- **Single-element readings may read high.** A single element's sweep is flat, and Peak Array Gain takes the highest of 162 noisy samples; the lift grows near the floor.
- **Channel phase may shift with gain setting.** The calibration was done at 100; if other settings move each channel's phase unevenly, the signals stop adding fully in phase. This is inferred, not measured.

Shape measurements (HPBW, FNBW, sidelobes, steering angle, null positions) are all read relative to each trace's own peak, so none of this affects them. Only peak-to-peak comparisons between configurations need care.

## Needed Changes

Grouped by who does the work. Checked items are drafted in the patch on branch `review/l19-firing-range`, which is not yet merged.

### Kits and benches, before class

- [ ] Re-run `install.sh` on every kit, so the dashboard has Signal vs Time and Tracking modes.
- [ ] Give every kit a stand at box height (L19), and clamp or key it to its protractor (L21).
- [ ] Set up each bench with about ±40° either side of broadside clear of walls and people, and the HB100 at least 1.2 m out.
- [ ] For L24 Procedure C, either match an interferer HB100 to each kit within 1 MHz (check with Find HB100, one source on at a time), or wait for the backend interferer.

### Backend and dashboard (phaser thread)

- [ ] Add a hardware interferer: synthetic, injected into the real receive samples before beamforming, incoherent with the target (frequency offset or random phase). Check that MVDR keeps 0° within about 1 dB while suppressing it.
- [ ] Linearize the Element Gains slider with a measured lookup table, from one element swept over the register.
- [ ] Make preset 8 load a uniform taper and reset Beam 1 Phase to 0°.
- [ ] Keep Signal BW and Rx Gain across Calibrate, Find HB100 and the Rect preset, and restart the sweep after Find HB100.
- [ ] Check the simulator's MVDR, which nulls the target along with an interferer at ±20°.

### Lab text, by lab

**L17**

- [ ] Replace the Rx Gain 10 dB reference, which clips, with a setting that puts the FFT peak at −10 ± 3 dBFS.
- [ ] Say where E1 and E8 are on the board, or have students infer it from the sign of Est. Angle (+θ toward E8).
- [ ] Note that the preset buttons only work once Lab Presets is expanded.

**L18**

- [ ] Recompute predictions at the kit's Find HB100 frequency, not 10.525 GHz.
- [ ] Take the scan-loss positions at 1.2 m or more; expect about −0.7 dB at 30°.
- [ ] Warn that at 45° the peak marker can read −90°.

**L19**

- [x] Procedure rewritten for the firing range.
- [x] Packet source rewritten for the firing range.
- [x] Student starter script added; the reference solver kept out of the public repo.

**L20**

- [ ] Expect peak steps of about 5 ± 1 dB per halving rather than 6, and grade on beamwidths.
- [ ] Revise the noise-floor explanation in "What the Three Traces Show".

**L21**

- [ ] Read the true angle from the sweep's Est. Angle at each stop.
- [ ] Read Runs 3 and 4 from one rotation pass, using each sweep's 0° and 30° points.

**L22–L23**

- [ ] Recompute the taper prediction table with the measured slider curve, or after the backend fix.
- [ ] Move the custom-taper hint to ends near 25%.
- [ ] Tell students to recalibrate if the uniform sidelobes look lopsided.
- [ ] Step (g): check Signal BW before sweeping. Step (h): note that Est. Angle shifts several degrees at 4 bits and below.

**L24**

- [ ] Replace the floor-limited explanation of notch depth; expect −40 to −50 dB.
- [ ] Procedure D: set a uniform taper and reset Beam 1 Phase, until the preset does it.
- [ ] Procedure C: pick one interferer angle (+20°, per the "Two limits" frame), restate the expected suppression from a run, and update the "No hardware?" note; the hosted simulator has an interferer.

### Repo and keys

- [ ] Apply the patch (six commits) with `git am` and push; GitHub refused pushes from the session.
- [ ] Rebuild the L19 blank and KEY PDFs with the real house macros.
- [ ] Put `ECE444_Lab_L19_foxhunt_KEY.py` in `ECE444-faculty/lab-keys/`.
- [ ] Decide whether packet `.tex` solution blocks belong in the public repo; every lab's source currently publishes its answers.

## Open Questions

- [ ] Why do peak levels fall short with elements fully on or off? Compare a single element's trace median with its maximum to test the readout bias.
- [ ] Does each channel's phase shift with the element-gain setting? Measure each channel's phase at gains 100 and 50.
- [ ] Would recalibrating with the source exactly at boresight remove the +1–2° boresight offset seen in L18, L20 and L24?
- [ ] Is the simulator's MVDR failure due to coherent sources, or a look-direction mismatch in the sweep?
- [x] Where does the slider curve come from? The ADAR1000's register response; the backend maps the slider linearly.
