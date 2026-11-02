ECE 444 recorded radar data: the fallback for the L28-L31 Labs.

Simulated ADALM-PHASER FMCW captures in the course capture format, written by
scripts/radar/fmcw_sim.py (re-run it to regenerate). Each .npz holds:
  iq      complex64, n_chirps x n_samples, summed array, one chirp a row, 0 dBFS = |iq| 1
  iq_ch   complex64, 2 x n_chirps x n_samples, the two subarray halves (sum = iq)
  fs, fc, B, T_ramp, PRI, f0   (Hz, Hz, Hz, s, s, Hz)
  note    what the capture holds

L28 (500 MHz, 0.5 ms, 0.6 MSPS, PRI 50 ms, f0 101.4 kHz):
  L28_cal_0m.npz            plate against the array, for the 0 m calibration
  L28_corner_{1,2,3}m.npz   10 cm corner reflector at 1, 2, 3 m
  L28_corner_2m_B250.npz    the 2 m corner at B = 250 MHz
  L28_corner_2m_T1ms.npz    the 2 m corner at T_ramp = 1 ms
  L28_two_corners.npz       corners at 2.0 and 2.2 m, closer than one resolution cell
  L28_walker.npz            a person walking 1 m -> 4 m -> 1 m at 1 m/s, 10 s

L29 (256 chirps of 300 us, PRI 0.5 ms, 4 MSPS, 500 MHz, f0 101.4 kHz; iq only,
no iq_ch, 2.5 MB each; a wall at 2.5 m in every burst):
  L29_static.npz              the leakage and the wall, nothing moving
  L29_hand_closing.npz        a hand from 1.0 m toward the kit at 1.0 m/s
  L29_hand_opening.npz        a hand from 0.7 m away from the kit at 1.5 m/s
  L29_hand_closing_B200.npz   the closing hand at B = 200 MHz (0.75 m range cells)
  L29_spinner.npz             a fidget spinner edge-on at 0.5 m: three arms on a
                              3 cm radius at 15 rev/s (tip speed 2.83 m/s)
The simulated chirps are timed perfectly, so a pulse canceller removes the wall
completely; no kit does.
