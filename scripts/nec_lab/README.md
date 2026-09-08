# nec_lab — NEC-2 for the ECE 444 simulation lab

A browser front end and a command line over the NEC-2 method-of-moments
kernel, written so the L8 dipole lab runs on any machine in the department and
so its results drop straight onto a chamber measurement.

It replaces **4nec2's GUI**, not NEC. The cards the lesson teaches are the
cards this tool writes, and it will print them for you to paste into 4nec2 or
xnec2c if you would rather run them there.

```sh
python scripts/nec_lab/run.py serve     # the GUI, at http://127.0.0.1:8444/
python scripts/nec_lab/run.py solve     # one frequency, in the terminal
cd scripts && python -m nec_lab.selftest  # prove the numbers against L7 and L8
```

`run.py` works from anywhere in the repository; from inside `scripts/` the
same commands are `python -m nec_lab <subcommand>`.

## Installing

The Python side needs nothing but the standard library. The NEC engine is the
part that varies, and `run.py engines` will tell you what this
machine has.

| Machine | Engine | How |
| :-- | :-- | :-- |
| Linux, macOS, WSL | PyNEC, in-process | `pip install PyNEC` |
| Linux | `nec2c` | `apt install nec2c` |
| Windows lab PC with 4nec2 | the engine inside 4nec2 | nothing to install; the tool finds `nec2dxs*.exe` under `C:\4nec2\exe`, or set `NEC_LAB_ENGINE` to it |

PyNEC publishes Linux wheels only, so a Windows machine without a C++
toolchain will not `pip install` it — which is exactly the case the executable
backend exists for. Both backends are real NEC-2; `python -m nec_lab.selftest`
runs the same model through both when both are present and asserts they agree.

## The GUI

`run.py serve` starts a local service and opens a page with:

- **Model** — frequency, length in wavelengths or millimeters, wire radius,
  segment count, and every segmentation rule from Part 2 evaluated live with
  the arithmetic behind it. A drawing of the wire sits under the fields, with
  the fed segment marked: a wire built along the wrong axis is invisible in a
  column of coordinates and obvious in a picture.
- **Solve / Trim to resonance** — impedance, VSWR, peak gain, E-plane HPBW,
  and the average-power-gain energy audit, with the audit colored red when the
  model is broken.
- **Frequency sweep** — R and X against frequency with the reactance zero
  marked, refined by bisection rather than read off the grid.
- **Convergence** — impedance and gain against segment count, flagging the
  rows where refinement has pushed the segment length below `8a`.
- **Compare with a measurement** — load a chamber CSV and it is drawn over the
  simulated cut, with the RMS and worst-case difference reported.
- **NEC input file** — the deck, to read, to edit, to run, and to copy.

It binds `127.0.0.1`, and the cards it will run are only the ones it can read
(below).

## Typing cards

The deck panel is an editor, not a display. Edit the cards, press **Run these
cards**, and the results come from what you typed; touch a form field and the
form takes the model back. The badge next to the panel heading always says
which one is driving.

Beside the deck, every line is glossed: each field carries the name the lesson
gives it, hovering one explains it underneath, and the `XNDA` field -- the four
digits glued together on the `RP` card -- is spelled out digit by digit. Wrong
cards are reported by line, in the terms of the card rather than of Python:

```text
line 6: GN is not a card nec_lab can run
        a ground plane; nec_lab models free space only. Copy the deck into
        4nec2 to run it there.
the deck: the EX card feeds segment 11, but wire 1 has 9
        a center feed on this wire is segment 5
```

That second one is a cross-card check, and it is the mistake this is really
for: neither card is wrong on its own.

**Trim to resonance rewrites your `GW` card** when you are working in cards,
rather than moving a form field you are not looking at.

The CLI reads decks too:

```sh
python scripts/nec_lab/run.py solve --deck my_dipole.nec
```

### What is read, and what is refused

Read: `CM CE GW GE EX FR RP XQ EN` -- exactly what this tool writes.

Everything else is refused by name, with what it does and a pointer to 4nec2.
That is deliberate rather than lazy. A card like `GN` (a ground plane) or `LD`
(a load) changes the antenna in a way the rest of nec_lab does not model: the
segmentation rules, the free-space energy audit, and the study code all assume
a bare wire in free space. Running it anyway would give a correct NEC answer
wrapped in a page that had quietly stopped applying to it -- a worse failure
than being told no.

## The chamber handoff

`usafa-chamber`'s pattern importer matches CSV columns by name, so the pattern
export here writes the names it looks for — `param`, `angle_deg`, `freq_hz`,
`gain_dbi` — and a measured run and a simulated cut land on the same axes with
no editing in between.

The one thing the file cannot carry is the difference in what the two numbers
*are*. A simulated cut is absolute gain in dBi; a chamber cut is raw S21 in dB
through cables, connectors and fixture. Both tools normalize each trace to its
own peak before differencing, which compares pattern shape and says nothing
about absolute gain. Comparing absolute levels is a gain-transfer measurement
against a standard-gain horn — L12's material, not something a CSV can fix.

## The lab, step by step

| L8 step | Command |
| :-- | :-- |
| 3 — baseline run | `run.py solve` |
| 4 — average gain | printed by `solve`, or `--average` in the API |
| 5 — frequency sweep | `run.py sweep --start 800 --stop 1000 --step 5` |
| 6 — trim to resonance | `run.py pattern --trim` |
| 7 — pattern cuts | `run.py pattern --csv pattern.csv` |
| 8 — convergence study | `run.py converge` |
| Part 5 — deliverable | `run.py report` |

`report` prints the comparison table with the simulated column filled in and
the *why* column empty, which is the part that is the student's to write.

## What it does not do

- **Only straight wires and a single voltage feed.** That covers the dipole
  lab and a Yagi; it does not cover ground planes, loads, or transmission-line
  cards. The engines support all of that — the model layer here does not
  expose it yet.
- **It runs only the cards it can read.** See the list above; anything else
  belongs in 4nec2, and the page says so by name.
- **The executable backend reads NEC's output file**, which prints gains to two
  decimals. Impedance is full precision; pattern values are not.

## Layout

| File | What |
| :-- | :-- |
| `model.py` | geometry, feed, pattern requests, and the cards they write |
| `cards.py` | reading cards back: the parser, the field glosses, the complaints |
| `engine.py` | the two backends and the shared result types |
| `study.py` | sweep, resonance, trim, convergence, energy audit |
| `export.py` | chamber-shaped CSV, JSON, the comparison table |
| `cli.py` | the command line |
| `run.py` | launcher, so `run.py` works from any directory |
| `serve.py` | the JSON API and static server behind the GUI |
| `static/` | the page: `index.html`, `app.js`, `style.css` |
| `selftest.py` | the assertions against L7, L8, and the other engine |
