"""The Lesson 7 analytical numbers the lab grades the simulation against.

These are the sinusoidal-current half-wave dipole: the current is assumed, the
integral is done in closed form, and the answers below fall out. They are not
NEC's answers, and the interesting part of the lab is why. Kept here as data so
the CLI report and the GUI table quote the same values.
"""

HALF_WAVE = {
    "z_in": complex(73.1, 42.5),      # impedance of the assumed sinusoid
    "r_resonant": 70.0,               # near resonance, after trimming
    "resonant_length_lambda": (0.47, 0.48),
    "gain_dbi": 2.15,                 # D = 1.64, lossless
    "hpbw_deg": 78.0,                 # E-plane
    "average_power_gain": 1.0,        # lossless free space, energy audit
}

# What the lab expects NEC to say for a wire cut to exactly lambda/2 at the
# radius L8 uses -- quoted in the lesson so students can tell a converged
# answer from a broken model before they have any intuition for either.
NEC_EXPECTATION = {
    "z_in_at_half_wave": complex(86.0, 47.0),
    "resonant_length_lambda": 0.473,
}
