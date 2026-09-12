# nec_lab — NEC-2 for the ECE 444 simulation lab

A browser front end and a command line over the NEC-2 method-of-moments
kernel, written so the L8 dipole lab runs on any machine in the department and
so its results drop straight onto a chamber measurement.

It replaces **4nec2's GUI**, not NEC. The cards the lesson teaches are the
cards this tool writes, and it will print them for you to paste into 4nec2 or
xnec2c if you would rather run them there.

```sh
python scripts/nec_lab/run.py serve     # the GUI, at http://127.0.0.1:8444/
```

## Getting it in front of a class

Ordered by what it costs the student, lowest first. On a managed Windows PC the
first path costs nothing at all.

### 1. One shared copy, and a URL (nothing installed at the student's end)

Run it on a machine you control and hand out the address. Students open a
browser; that is the whole procedure.

```sh
docker build -t nec_lab scripts/nec_lab
docker run --rm -p 8444:8444 nec_lab
# or: docker compose -f scripts/nec_lab/docker-compose.yml up -d
```

Without Docker, the same thing from a checkout:

```sh
python scripts/nec_lab/run.py serve --host 0.0.0.0 --no-browser
```

Either way the banner prints the addresses a browser can actually be pointed
at, rather than `0.0.0.0`. The service holds no per-student state -- every
request builds its model and solves independently -- so a room shares one copy
happily. Two practical notes: Windows Firewall will ask to allow the port the
first time, and this belongs on a classroom network, not a public one.

#### On a Raspberry Pi, or any small shared box

It fits, with one choice to make. Measured on four cores (Xeon 2.8 GHz), ten
students each firing solve + sweep + convergence + sphere at the same instant
-- the worst case, everyone clicking when you say "go":

| Engine | median | slowest | all 40 requests served in |
| :-- | --: | --: | --: |
| nec2c (subprocesses) | 383 ms | 1.2 s | 2.3 s |
| PyNEC (in-process) | 743 ms | 4.1 s | 5.3 s |

**Use `--engine exe` on a shared server.** PyNEC holds the GIL through the
solve, so requests queue behind each other; nec2c runs as subprocesses and uses
every core. The answers are identical -- the selftest asserts that -- so this
is purely about throughput. On a single-user laptop PyNEC is the faster one and
stays the default.

A Pi has the same four cores and a slower one: expect roughly 2-3x these
numbers on a Pi 5 and 4-5x on a Pi 4, so a worst-case wait of a few seconds
during a simultaneous burst, and sub-second once the class spreads out. The
service holds about 50 MB resident after serving 2-degree spheres on an
8-element array, so memory is not the constraint on any Pi.

Two practical notes:

- **PyNEC has no ARM wheel.** `apt install nec2c` is the whole install on
  Raspberry Pi OS, and the container image asks pip for a wheel only, so it
  builds on ARM and runs on nec2c there rather than failing on a source build
  with no compiler.
- **The energy audit is the expensive part of a solve** on a multi-element
  model -- a 2 degree sphere. Clear its checkbox if a Pi 4 feels slow during a
  lab; the cuts and the impedance do not need it.

#### On a headless box

A small always-on machine is the best home for the shared copy: it is up before
the class is, and nobody has to remember to start it.

```sh
sudo apt install docker.io docker-compose-v2 avahi-daemon
git clone https://github.com/livethisdream/ece444 /opt/ece444
cd /opt/ece444
NEC_LAB_PORT=80 NEC_LAB_PUBLIC_URL=http://nec-lab.local/ \
  docker compose -f scripts/nec_lab/docker-compose.yml up -d --build
sudo ufw allow 80/tcp        # if the firewall is on
```

Four details that make the difference between an address students type once and
one they fight with:

- **Publish port 80.** `http://nec-lab.local` beats `http://10.1.2.3:8444` by
  more than it looks like it should.
- **Give the box a name and a fixed address.** A DHCP reservation on the
  router, and `avahi-daemon` for the `.local` name -- Windows 10 and 11 resolve
  mDNS natively, so nothing is needed at the student's end. If the campus
  network blocks mDNS between clients, hand out the IP instead; the reservation
  is what keeps it from moving.
- **Set `NEC_LAB_PUBLIC_URL`.** A container cannot discover the host's name, so
  without it the log prints the container's own address and the note saying so.
- **`restart: unless-stopped` covers reboots**, and the image's healthcheck
  makes `docker ps` tell you the truth about whether it is serving.

Updating is `git pull` and the same `up -d --build`. The rebuild reruns the
selftest, so a broken engine or a broken number stops the deploy rather than
reaching a class.

Without Docker, `deploy/nec_lab.service` is the same thing as a systemd unit:
port 80 through `CAP_NET_BIND_SERVICE` rather than root, `Restart=always`, and
the header of the file carries the four commands that install it.

### 2. Double-click, on the student's own machine

Download the repository (**Code -> Download ZIP** on GitHub; no git needed),
unzip, and double-click:

| Platform | File |
| :-- | :-- |
| Windows | `scripts\nec_lab\nec_lab.bat` |
| macOS | `scripts/nec_lab/nec_lab.command` |

The browser opens on the tool. No admin rights, no command line, no
installation step -- it uses the Python the machine already has, and says so
plainly if there is none.

### With uv

`uv run` works and needs no venv of its own, because `run.py` carries PEP 723
metadata with an empty dependency list -- the tool is standard library only:

```sh
uv run scripts/nec_lab/run.py serve                  # stdlib only
uv run --with PyNEC scripts/nec_lab/run.py serve     # + the in-process engine
```

PyNEC is deliberately **not** in that metadata. It is the one piece that is not
always a Python package -- on Windows the engine is the executable inside
4nec2, and PyNEC cannot be built there at all -- so listing it would make
`uv run` fail on exactly the machines the fallback exists for. `--with PyNEC`
asks for it where it works.

Tested on Python 3.10 (the floor `run.py` declares) as well as 3.11 and 3.12.

### Trying it on a Windows laptop first

Worth knowing before you start, because Windows is the one place the engine
question actually bites. `run.py engines` prints what a machine has, and the
error when it has nothing names these same three ways out.

1. **In WSL**, if the laptop has it: `sudo apt install nec2c`, then
   `python3 scripts/nec_lab/run.py serve`. Browse from Windows to
   `http://127.0.0.1:8444/` -- WSL2 forwards localhost, so nothing else is
   needed. This is the quickest honest test of the whole tool.
2. **Windows natively**, which is the student path: double-click
   `nec_lab.bat`. It needs an engine, and on Windows that means 4nec2 being
   installed -- `pip install PyNEC` will not work, because there is no Windows
   wheel and it would want a C++ toolchain.
3. **Docker** last, on whatever box will actually serve the room. Docker
   Desktop on a managed laptop usually wants admin rights; inside WSL,
   `sudo apt install docker.io` and starting `dockerd` avoids that entirely.

One WSL wrinkle if you want to test *shared* mode from a second device: a
service bound inside WSL2 is reachable from the Windows host but not from the
network, because WSL2 sits behind its own NAT. Either run that test from
Windows directly, or add a port proxy on the host:

```powershell
netsh interface portproxy add v4tov4 listenport=8444 connectport=8444 ^
      connectaddress=(wsl hostname -I).Trim()
```

That is a Windows-side workaround for a WSL networking detail, not something
nec_lab needs -- on the box that finally serves the class there is no NAT in
the way.

### 3. The command line

```sh
python scripts/nec_lab/run.py serve     # the GUI, at http://127.0.0.1:8444/
python scripts/nec_lab/run.py solve     # one frequency, in the terminal
cd scripts && python -m nec_lab.selftest  # prove the numbers against L7 and L8
```

`run.py` works from anywhere in the repository; from inside `scripts/` the same
commands are `python -m nec_lab <subcommand>`.

## The NEC engine

The Python side needs nothing but the standard library. The engine is the part
that varies, and `run.py engines` will tell you what a machine has.

| Machine | Engine | How |
| :-- | :-- | :-- |
| Windows lab PC with 4nec2 | the engine inside 4nec2 | nothing to install; the tool looks for `nec2dxs*.exe` under the usual install locations, including per-user ones, or set `NEC_LAB_ENGINE` to it |
| Linux, macOS, WSL | PyNEC, in-process | `pip install PyNEC` |
| Linux | `nec2c` | `apt install nec2c` |
| The container | both | already in the image |

PyNEC publishes Linux and macOS wheels but not Windows ones, so a Windows
machine without a C++ toolchain will not `pip install` it -- which is exactly
the case the executable backend exists for. Both backends are real NEC-2;
`python -m nec_lab.selftest` runs the same model through both when both are
present and asserts they agree. **The container build runs that selftest**, so
an image only exists if the two engines agreed and the L7 and L8 numbers still
came out right.

## Antenna types

The type picker drives everything. Choosing a type renders its parameters,
and **Build & solve writes NEC cards** into the deck editor and runs them --
so what the page solves is always what the deck says, and a student can pick
up where the builder left off by editing the cards.

| Type | Lesson | What it is for |
| :-- | :-- | :-- |
| Dipole | L7-L8 | the lab's antenna: one wire, center fed |
| Monopole over ground | L12 | half a dipole fed against its image; perfect or real ground |
| Loop | L12 | a closed loop as a polygon, because NEC-2 has no curve |
| Yagi-Uda | L14 | driven element, reflector, N directors; the parasitic array |
| Driven array | L16-L22 | dipoles with a source each and a phase per element |

Adding a type is a Python change in `builders.py` and nothing in the page
needs to know: the form is rendered from the catalog the service serves.

Three things the types brought with them, worth knowing because they change
what the numbers mean:

- **Over ground, nothing is computed below the horizon.** Ask NEC for theta
  past 90 degrees over a ground plane and what comes back is not a small
  number, it is garbage -- 1e120 dBi in the case that found this. Cuts and the
  sphere both stop at 90 when a ground plane is present.
- **The energy audit's grid follows the structure.** L8's `RP 0 19 36 1001` is
  ten degrees and plenty for a dipole. Point it at a 4-element Yagi and it
  reads 0.88, because the main lobe falls between samples -- a correct model
  reported as broken. Multi-element models get a 2 degree grid instead, and
  the dipole keeps the handout's card exactly.
- **Every element of a driven array reports its own impedance**, and they
  differ. That difference is mutual coupling, and it is the gap between the
  array factor and the pattern NEC computes -- which is L22's subject.

### What NEC-2 cannot do

NEC-2 is a thin-wire code. Patches, slots, horns (L13) and parabolic
reflectors (half of L14) are not thin-wire problems, and they are absent here
rather than approximated badly. L13's patch designer widget and the aperture
theory in Module 3 cover that ground; this tool covers the wires.

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
- **Pattern cuts** — one dial per *plane*, not per swept angle. Theta is
  measured from +z and phi from +x, so a single dial with "0 at the top" puts
  the same beam in two different places: a Yagi beaming along +x lands at 90 on
  a theta dial and at 0 on a phi dial, and the two pictures look rotated
  against each other because they are. Each dial is a plane with a fixed
  orientation in space instead, labeled with its own axes (+x to the right, +z
  or +y up), and every sample is plotted by the direction it points in. Cuts
  sharing a plane share a dial, which is how the two halves of an elevation
  pattern over ground draw as one curve.
- **3D pattern** — gain over the whole sphere as a surface you can orbit, with
  the wire drawn to scale at the center so the nulls have something to be
  along. The radius scale is a choice and it matters: **linear power** is the
  donut from the lesson, **linear field** is the same shape with the lobes
  fattened, and **a dB radius** pushes everything far from the peak outward
  until a dipole looks nearly round -- right for reading sidelobes, misleading
  about a beam. The color is gain in dBi under all three. A 5 degree grid is
  2701 directions and solves in under a tenth of a second; 2 degrees is 16471
  and takes about a quarter. Exports as its own CSV (theta, phi, gain), not the
  cut file -- the chamber importer keys on a single angle column and a sphere
  has two.
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

Read: `CM CE GW GE GN EX FR RP XQ EN` -- exactly what this tool writes.
That covers any number of wires, any number of sources, and a perfect or real
ground plane.

Everything else is refused by name, with what it does and a pointer to 4nec2.
That is deliberate rather than lazy. A card like `LD` (a load) or `TL` (a
transmission line) changes the antenna in a way the rest of nec_lab does not
model: the segmentation rules, the energy audit, and the study code all assume
the structure is what the supported cards describe. Running it anyway would
give a correct NEC answer wrapped in a page that had quietly stopped applying
to it -- a worse failure than being told no.

`GN` used to be on that list and is not any more: L12 needs a monopole, a
monopole needs a ground plane, so the model layer learned about ground rather
than the parser learning to lie. What is still checked is that `GE` and `GN`
agree -- a `GN` card with `GE 0` is a ground NEC will never connect anything
to.

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
against a standard-gain horn — L9's material, not something a CSV can fix.

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
| `model.py` | geometry, feeds, ground, pattern requests, and the cards they write |
| `builders.py` | the antenna catalog: each type, its parameters, and its cards |
| `cards.py` | reading cards back: the parser, the field glosses, the complaints |
| `engine.py` | the two backends and the shared result types |
| `study.py` | sweep, resonance, trim, convergence, energy audit |
| `export.py` | chamber-shaped CSV, the sphere CSV, JSON, the comparison table |
| `cli.py` | the command line |
| `run.py` | launcher, so `run.py` works from any directory |
| `serve.py` | the JSON API and static server behind the GUI |
| `static/` | the page: `index.html`, `app.js`, `style.css` |
| `selftest.py` | the assertions against L7, L8, and the other engine |
| `nec_lab.bat`, `nec_lab.command` | double-click launchers, Windows and macOS |
| `Dockerfile`, `docker-compose.yml` | the shared copy that serves a room |
