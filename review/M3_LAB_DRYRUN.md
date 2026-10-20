# Module 3 Lab Dry Run — L17, L18, L20 Findings

**Date:** 2026-10-19 · **Kit:** phaser-00 · **Run by:** Neil, with Claude driving the GUI
**Living copy:** [Claude Doc](https://claude.ai/code/artifact/40002b11-6a90-42f7-a618-01f13506ae67)

## Summary

The L17, L18 and L20 labs work on phaser-00. Beam position, beamwidth, nulls
and sidelobes all match theory to within a degree or a dB. Absolute
peak-level comparisons do not: they come out 1 to 3 dB short of theory, and
the cause is not yet known. L19 was skipped because it is still under
construction.

- **Steering and shape:** verified. Physical and commanded steering track the source, and HPBW matches the array factor within 0.5° at 8 and 4 elements.
- **Scan loss:** about −0.7 dB at 30° and −1.0 dB at 45°, measured at about 4 ft. The 30° point matches theory.
- **Peak steps:** halving the aperture costs about 5 dB, not 6. Compression and element leakage were tested and ruled out as the main cause.
- **Lab text:** several fixes needed. The Rx Gain 10 reference clips at 1 m, E1/E8 orientation is missing from L17, and the GUI's peak marker can lock onto −90° at 45°.

## Setup

All runs used one kit and one calibration. Distance and gain changed partway
through, as noted.

| Item | Value |
| :-- | :-- |
| Kit | phaser-00, already provisioned (L17 Part A not rerun) |
| Signal Freq (Find HB100) | 10.408 GHz, not the lab's nominal 10.525 GHz |
| IF | 1.690 GHz |
| Calibration | the existing L17 calibration, kept for all labs |
| Source distance | 1 m (L17, L18 Runs 1–2); about 4 ft / 1.22 m (L18 scan loss, L20) |
| Rx Gain | 10 dB (L17 Steps 1–5 only, clipped); 1 dB everywhere else |
| Sweep | Lab Preset 1 or 2, 7 phase bits, 162 points, 2.8125° LSB |

Predictions in this file are recomputed at 10.408 GHz (d/λ = 0.486, kd = 174.9°).

## L17: Bring-Up (Part B)

Part B passes on every check. At the lab's Rx Gain of 10 dB, however, the FFT
peak goes over full scale.

| Step | Source | Rx Gain | Est. Angle | Peak Array Gain | FFT peak / floor |
| :-- | :-- | :-- | :-- | :-- | :-- |
| 3–5 | boresight, 1 m | 10 dB | −1.8° | 5.0 to 5.5 dB | +3 / −70 dBFS |
| 6 | ~30°, toward E1 | 1 dB | −31° | −4.0 dB | −6 / −78 dBFS |
| 7 | boresight again | 1 dB | 0° | −3.7 dB | −6 / −78 dBFS |

- At Rx 10 the tone read +2 to +3.4 dBFS, and an image tone appeared 0.19 MHz on the other side of zero.
- The peak sits 72 dB above the FFT floor; the lab asks for at least 20.
- Step 6 asks which end, E1 or E8, the source moved toward, but L17 never says where E1 is. L18 defines +θ as the E8 end, so the −31° reading means the source was toward E1.
- The Lab Preset buttons only worked once the Lab Presets section was expanded.

## L18: Beam Steering

Both runs put the peak at the commanded or physical angle, within the lab's
±2° budget except at 45°. Rx Gain was 1 dB and the source 1 m away.

| Run | Target | Est. Angle | Peak | HPBW (meas / pred) | Sidelobes (dBc) |
| :-- | :-- | :-- | :-- | :-- | :-- |
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
| :-- | :-- | :-- | :-- |
| 30° | −0.7 dB | −0.6 dB | −0.8 to −0.9 dB |
| 45° | −1.0 dB | −1.5 dB | −2.0 to −2.3 dB |

The 30° point matches theory. The 45° point shows less loss than even the
ideal bound, which points to multipath or HB100 aim. At 1 m the measured drop
was only 0.2 to 0.4 dB, so 1 m is too close for this measurement.

## L20: Array Factor

Beamwidth tracks the active aperture as predicted. The peak steps between
apertures fall short of 6 dB. Source at about 4 ft, Rx Gain 1 dB, element
gains 100.

| Active | HPBW (meas / pred) | FNBW (meas / pred) | First SLL (dBc) | Peak (dBFS) | Drop vs. 8 (meas / pred) |
| :-- | :-- | :-- | :-- | :-- | :-- |
| 8 (E1–E8) | 13.4° / 13.2° | 29.8° / 29.8° | −12.5 / −14.0 (pred −12.8) | −5.25 | 0 / 0 dB |
| 4 (E3–E6) | 27.4° / 27.1° | ~67° / 62.0° | −12 to −14 (pred −11.3) | −10.4 | −5.1 / −6.0 dB |
| 2 (E4, E5) | ~56° (52–58) / 61.9° | none / 180° | none | −15.1 | −9.9 / −12.0 dB |

- **4-element FNBW:** reads wide because the left null fills to the noise floor, about −23 dBc, so its position is uncertain.
- **2-element trace:** sits well above the floor. It falls about 27 dB to near −40 dBFS at ±80°, which is the 2-element array factor's own roll-off toward endfire. The lab's claim that this peak is only 11 dB above the floor did not hold on this kit.
- **Clearing frozen traces:** a press-and-hold on Freeze clears them, as the GUI describes.

## Peak-Level Investigation

The array's peak reads 2 to 3 dB below the in-phase sum of its single
elements. Two candidate causes were tested and ruled out, and two remain.

**Test 1, element leakage (ruled out).** With all eight gains at 0, the
residual peak was −38.8 dBFS, 33.5 dB below the full array. That is about 2%
voltage per element, enough to explain at most 0.5 dB of the shortfall.

**Test 2, single elements at gain 100.** E1–E4 and E7–E8 each read about
−21.1 dBFS, E5 −20.5 and E6 −22.0. The element gains match within ±0.6 dB.
Adding those voltages in phase predicts each aperture's peak:

| Active | Predicted from singles | Measured | Shortfall |
| :-- | :-- | :-- | :-- |
| 2 (E4, E5) | −14.8 dBFS | −15.1 dBFS | 0.3 dB |
| 4 (E3–E6) | −9.1 dBFS | −10.4 dBFS | 1.3 dB |
| 8 (E1–E8) | −3.0 dBFS | −5.25 dBFS | 2.2 dB |

**Test 3, all gains at 50 (rules out compression).** The 8-element peak fell
to −10.2 dBFS and E4 alone to −24.9 dBFS. The step is 14.7 dB against an
ideal 18.1, so the shortfall grew to 3.4 dB. If compression were the cause,
lowering the level would have shrunk the shortfall. Beamwidth (13.1°) and
sidelobes did not change.

**What remains:**

- **Single-element readings read high.** A single element's sweep is flat across all angles, and Peak Array Gain takes the highest of 162 noisy samples. The lift grows as the signal nears the floor.
- **Channel phase or gain shifts with the gain setting.** The calibration was done at 100. If other settings move each channel's phase or amplitude unevenly, the signals stop adding fully in phase. This is inferred, not measured.

Shape measurements (HPBW, FNBW, sidelobes, steering angle) are all read
relative to each trace's own peak, so they are not affected by this.

## Recommended Course Changes

- [ ] **L17, L18, L20:** replace the Rx Gain 10 dB reference with a setting that keeps the FFT peak below full scale at the bench distance. Rx 1 dB worked here.
- [ ] **L17, Step 6:** say where E1 and E8 are on the board, or tell students to infer it from the sign of Est. Angle, with +θ toward E8.
- [ ] **L17, Step 1:** note that Lab Preset buttons need the Lab Presets section expanded.
- [ ] **L18:** warn that at 45° the peak marker can read −90°, and have students read the main lobe instead.
- [ ] **L18:** take the scan-loss positions at 4 ft or more rather than 1 m. Expect about −0.7 dB at 30° and treat 45° as multipath-limited.
- [ ] **L18, L20:** tell students to recompute predictions at their kit's Find HB100 frequency (10.408 GHz here), not 10.525 or 10.3 GHz.
- [ ] **L20:** expect peak steps of about 5 ± 1 dB per halving rather than 6, grade on beamwidths, and revise the noise-floor explanation in "What the Three Traces Show".
- [ ] **L19:** write the procedure and packet (still a shell).

## Open Questions

- [ ] Is the single-element reading inflated? Compare E4's trace median with its maximum. A median about 1 dB lower would confirm it.
- [ ] Does the ADAR1000's per-channel phase shift with the element-gain setting? Measure each channel's phase at gains 100 and 50.
- [ ] Would recalibrating with the source exactly at boresight remove the +1–2° boresight offset seen in L18 and L20?
