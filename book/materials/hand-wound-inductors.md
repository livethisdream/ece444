---
orphan: true
---

# Hand-Wound Inductors for the Midterm L-Network

A field guide for Phase 4 of the midterm project. [Back to Materials](../materials.md)

## Why Wind Your Own

At 800-1050 MHz your L-network inductor is about 5-20 nH, and the easiest way
to get that is two or three turns of bare wire you wind yourself.

- The electronics-lab bins hold microhenry parts for audio and low-frequency
  work. Those are the wrong parts here: their leads alone add several nH, and
  many go self-resonant below 1 GHz.
- At these frequencies, about 1 mm of wire is about 1 nH. The coil and its
  leads are all part of the inductor.
- A hand-wound coil is tunable. Squeeze or spread the turns while the VNA is
  sweeping and watch the trace move. That is how RF technicians trim a match
  on real hardware.

Start from your own design value. This guide gets you within about 20% of it
on the first try, and the VNA does the rest. Everything here is leaded and
through-hole friendly: no surface-mount soldering.

## Materials and Tools

| Item | What to use | Why |
| :-- | :-- | :-- |
| Wire | 22 AWG (0.64 mm) solid copper; bare, tinned, or enameled | Stiff enough to hold its shape, thin enough to bend tight |
| Winding form | Drill bit shank: 2.0 mm, 2.5 mm, or 3.0 mm (1/8 in. works too) | Sets the coil diameter; the bit slides out cleanly |
| Cutters, needle-nose pliers, tweezers | Bench kit | Trimming leads and setting turn spacing |
| Fine sandpaper or a hobby knife | Only for enameled wire | Strip the enamel off the last 1-2 mm of each lead so it takes solder |
| Calipers or a ruler with mm | Bench kit | Measure coil length and lead length; you will report both |
| Soldering iron, fine tip | Bench | Short, clean joints; a solder blob adds capacitance |

Do not use stranded wire: the coil will not hold its spacing, and you cannot
tune it.

## Pick a Starting Coil

Two turns on a 2.5-3.0 mm form covers most of the 8-16 nH range; stretch the
coil to go lower, compress it to go higher. Wheeler's formula estimates it,
with $D$ the mean diameter (form diameter plus one wire diameter), $\ell$ the
coil length, and $N$ the number of turns, all lengths in inches:

$$
L\ [\mu\text{H}] = \frac{D^2 N^2}{18D + 40\ell}
$$

It is accurate to a few percent for coils longer than about $0.4D$. For the
short coils here, treat it as a starting point within about 20%.

| Form (mm) | Turns | Coil length (mm) | Coil only (nH) |
| :-- | :-- | :-- | :-- |
| 2.0 | 2 | 1.5 | 10 |
| 2.0 | 3 | 3.0 | 15 |
| 2.0 | 3 | 5.0 | 10 |
| 2.5 | 2 | 1.5 | 13 |
| 2.5 | 2 | 2.0 | 11 |
| 2.5 | 2 | 3.0 | 9 |
| 2.5 | 3 | 4.0 | 16 |
| 3.0 | 2 | 2.0 | 14 |
| 3.0 | 2 | 3.0 | 11 |
| 3.0 | 2 | 4.0 | 9 |
| 3.0 | 3 | 5.0 | 18 |

The table assumes 22 AWG wire. Coil length is measured from the center of the
first turn to the center of the last.

**Count the leads.** Each lead adds about 0.8-1 nH per mm from the coil to the
solder joint. Two 2 mm leads add about 3-4 nH, so aim the coil itself about
that much below your design value.

**Straight-wire option, for values under about 10 nH.** A straight piece of
22 AWG wire gives roughly 7 nH at 10 mm, 10 nH at 14 mm, and 12 nH at 16 mm.
Run close to a ground plane, it reads somewhat lower. It is easier to build,
but you can only tune it by cutting, so cut it long.

## Wind It and Mount It

1. Cut about 40 mm of wire. You need the extra length to hold onto while
   winding.
2. Hold one end against the drill-bit shank with pliers and wrap the wire
   tightly around the bit for the number of turns you picked. Keep the turns
   snug to the bit.
3. Slide the coil off the bit. Use tweezers to set the spacing so the coil
   length matches your table row, and measure it with calipers.
4. Bend both leads straight out from the coil and trim each to 2 mm. Strip the
   enamel off each lead end if needed.
5. Solder it in its spot on the SMA proto board, as close to the pads as you
   can. A series element goes in the signal path; a shunt element goes from the
   signal trace to ground, on whichever side of the series element your design
   puts it.
6. Keep the coil at least 3 mm from other parts and mount it with its axis at
   right angles to any other coil. Coupling between coils and to the ground
   plane shifts the value.
7. Write down the form diameter, turns, coil length, and lead lengths
   **before** you start tuning. That is your designed coil.

## Tune It on the VNA

Calibrate at the reference plane you will report, sweep across your $f_2$ with
the marker on $f_2$, and adjust one thing at a time.

| To do this | Do this to the coil | What happens |
| :-- | :-- | :-- |
| Raise $L$ | Squeeze the turns closer together | Coil length drops, $L$ rises |
| Lower $L$ | Spread the turns apart | Coil length grows, $L$ drops |
| Make a big change | Add or remove a turn, or change the form diameter | $L$ changes by about 1.5-2x |
| Make a fine change | Shorten a lead by 1 mm | $L$ drops by about 1 nH |

- **On the Smith chart:** a series inductor moves the point clockwise along a
  constant-resistance circle. A shunt inductor moves it counterclockwise along
  a constant-conductance circle. If the point moves the wrong way, you have the
  wrong element or the wrong position.
- **Read numbers from the marker readout**, not the Smith-chart grid, until the
  chamber software update is installed.
- Push turns with a plastic tool or a wooden toothpick, not metal tweezers:
  anything metal near the coil detunes it while you are touching it.
- Stop at VSWR $\le 2$ at $f_2$. Chasing a perfect 50 Ω by hand wastes chamber
  time; the bar is 2.
- Once you are done, put a small drop of hot glue or nail polish on the coil so
  the spacing does not move.

## What to Report

The project already asks for designed versus as-built values. For a
hand-wound coil, the as-built value is something you **measure**, not a number
printed on a part.

- **Designed:** the $L$ your network calculation called for, and the coil you
  picked from the table to hit it: form, turns, coil length, and leads.
- **As built:** the final coil's dimensions after tuning, and its measured
  inductance.
- **Measuring $L$ directly (recommended):** before the coil goes into the
  network, solder it from an SMA's center pin to its ground with the same lead
  lengths, calibrated at that SMA's reference plane. The marker reads
  $Z \approx jX$, so $L = X/(2\pi f)$.
- **Measuring $L$ in place:** for a series element, the change in reactance it
  causes is $X = 2\pi f L$. For a shunt element, the change in susceptance is
  $B = -1/(2\pi f L)$. Read both from the marker before and after the coil goes
  in.
- Re-sweep after gluing the coil. Glue changes the value slightly; report the
  final sweep.
- One sentence on the difference between the Wheeler estimate and your
  measurement, and what you think caused it: lead length, the board, the
  short-coil approximation.

## If You Also Need a 1-4 pF Capacitor

Make a twisted-wire "gimmick" capacitor. It covers 0.5-4 pF, needs no
surface-mount work, and tunes the same way the coil does.

1. Twist two pieces of insulated or enameled wire (24-26 AWG) tightly together
   for about 5-8 cm.
2. Solder one wire to each node of the capacitor's position. Leave the far end
   of the twist open, with the two wires not touching.
3. Expect very roughly 0.5 pF per cm of twist; it depends strongly on the wire
   and how tight the twist is. Measure it the same way as the coil: one wire to
   the SMA center pin and the other to ground, with $Z = -jX$ and
   $C = 1/(2\pi f X)$.
4. Tune by snipping the open end. A shorter twist means less capacitance, and
   you cannot add it back, so cut a few millimeters at a time.

A bin ceramic disc capacitor is the wrong part. Its leads add enough
inductance that a few-pF disc can be close to self-resonance at 1 GHz. Report
a gimmick capacitor's measured value as its as-built value, the same as the
coil.
