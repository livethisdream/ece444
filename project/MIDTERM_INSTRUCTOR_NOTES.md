# Midterm Project: Instructor Notes

These notes go with `latex/ECE444_Project_Midterm_v3.tex`, the Fall 2027 packet. None of this goes to cadets.

## What changed from Fall 2026, and why

- **Coax-stub match replaces the discrete L-network.** The L-network worked for nobody, because at 850-1050 MHz it needs parts of a few nH and a few pF. Stub matching is taught in ECE 343 the semester before, and the stub is built the same way the dipole is: cut it, measure it, trim it.
- **Graded checkpoints at L11, L14, L16, L18,** 5 points each, at the class's request. Confirm those lessons still fall where the packet assumes before it goes out.
- **A reference dipole at the bench.** Several cadets could not tell a bad setup from a bad antenna. If a cadet can reproduce the reference dipole's numbers, the setup is not the problem.
- **ESD protection on the dipole.** The new chamber foam and equipment build up static faster. Every dipole gets heat-shrink on both arms and a shorted quarter-wave coax stub across the feed, which gives the arms a DC path to ground.

## ESD: the analyzer side

- **Put a port protector on every analyzer port,** both the handheld and the Copper Mountain: an inline DC block or a purpose-built RF ESD protector. Calibrate through it so it drops out of the measurement. Check Copper Mountain's guidance on port protection before buying.
- Wrist strap at the bench, and short the antenna's SMA to ground before connecting it.
- Chamber-side mitigation for the foam is in work separately.

## Before the term

- [ ] Build the reference dipole, measure its S11 and pattern, and post them at the bench.
- [ ] Buy the analyzer port protectors.
- [ ] Stock the parts: SMA tees, coax with SMA ends for stubs (semi-rigid or RG-316), heat-shrink sized for the dipole wire, and coax cutters.
- [ ] Put the first measurements in class time during L10-L11, so the first attempt happens with you in the room.

## Things cadets will hit

- **The grounding stub is an open only near 915 MHz.** At their second frequency it adds reactance, so the matching stub has to absorb it. This is intended: it is one of the decisions the packet leaves to them.
- **Velocity factor.** A stub cut to the free-space length will be too long. The packet asks how they accounted for it and does not tell them.
- **Heat-shrink lowers the resonance.** The packet tells them to trim with it on.
