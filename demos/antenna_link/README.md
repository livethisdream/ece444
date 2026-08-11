# Antenna Tx/Rx Link Demo (single Pluto)

A browser-based teaching demo for **ECE 444 — Antennas, Phased Arrays, and Radar
Systems**. A single ADALM-PLUTO transmits a CW tone out one antenna and receives
it on a second antenna. As a student **rotates or cross-polarizes the Rx
antenna**, the received power changes — demonstrating **antenna pattern** and
**polarization loss**.

It is the single-Pluto, one-Rx-channel cousin of the `pluto_beamformer.py` app:
a Python backend (`antenna_link.py`) serves a static frontend over HTTP and
streams live power over a WebSocket at ~20 Hz.

<!-- Uses a stock Pluto: 1 Tx + 1 Rx. No AD9361 2-Rx hardware hack required. -->

## What it shows

| View | What the student sees |
|------|-----------------------|
| **Live Power** | A big received-power readout (dBFS) and its level relative to a marked co-pol reference, plus a rolling strip chart. Rotate the Rx antenna and watch it move. Use **Mark Ref** (top-right) to set the 0 dB co-pol reference. |
| **Pattern** | Type the current Rx angle, hit *Record*, and build up a polar pattern with a **cos²θ theory overlay** (the polarization loss factor). Feeds the midterm Antenna Pattern Measurement project. |

## Quick start

### Simulation (no hardware — for rehearsal / checking the UI)

```bash
# Windows
.venv-win\Scripts\python antenna_link.py --sim
# WSL / Linux
.venv-linux/bin/python antenna_link.py --sim
```

A browser opens at <http://localhost:8080>. Open the **Simulation** panel on the
left and drag the *Rx antenna angle* slider — synthetic power follows cos²θ.
Hit **Start**, **Mark Ref** at 0°, then go to the **Pattern** tab and record a
few angles to watch the measured curve land on the theory line.

You can also skip the `--sim` flag: launch normally and click **Start Sim** in
the Device panel to drop into simulation from the UI (and **Connect** to switch
back to a real Pluto).

### With a real Pluto

1. Install the hardware extras (requires `libiio` on the system):
   ```bash
   UV_PROJECT_ENVIRONMENT=.venv-win  uv sync --extra hardware     # Windows
   UV_PROJECT_ENVIRONMENT=.venv-linux uv sync --extra hardware    # WSL/Linux
   ```
2. Run against the Pluto:
   ```bash
   .venv-win\Scripts\python antenna_link.py --pluto-uri ip:192.168.2.1
   ```
3. In the browser, enter the Pluto IP, click **Connect**, then **Start**.

## Physical setup

At 2.4 GHz, λ ≈ 12.5 cm.

- **Tx SMA → fixed antenna** (e.g. vertical polarization).
- **Rx SMA → the antenna the student rotates.**
- Separate the two antennas **~30–50 cm** (a few wavelengths) so it is the real
  over-the-air path, not near-field coupling. The direct Tx→Rx path *is* the
  signal — rotating Rx changes the polarization/pattern match on that path.
- Tune **Tx gain** and **Rx gain** (sliders) so the co-pol level reads about
  **−15 dBFS**: strong enough that the null is visible, with headroom so it does
  not clip (the readout turns amber and says *CLIPPING* if it does).

> **Manual gain is deliberate.** The backend forces `gain_control_mode = manual`.
> With AGC/slow-attack the radio would silently compensate and the power would
> *not* drop as you rotate — defeating the whole demonstration.

## In-class flow (polarization)

1. Tx and Rx antennas co-polarized (both vertical). **Start**, then click
   **Mark Ref** → relative reads 0 dB. (To reset it, **press and hold Mark Ref
   for 3 s** — the button fills, then clears.)
2. Slowly rotate the Rx antenna toward horizontal. Watch the relative level fall;
   at 90° (cross-pol) it drops into the null (ideally −∞, in practice −20 dB or
   so from finite cross-pol isolation).
3. Switch to **Pattern**, record power every 15–30° through a full rotation, and
   compare the measured polar curve against the cos²θ overlay.

## UI notes

- **Mark Ref** (top-right): click to set the 0 dB co-pol reference; press-and-hold
  3 s to clear it.
- **Start Sim / Connect** (Device panel): switch between synthetic power and a real
  Pluto at runtime — no restart needed.
- The **ⓘ** icons carry inline hints (e.g. the gain-tuning tip on *Rx gain*).
- Theme follows your OS light/dark setting; the footer button overrides it.

## Files

```
antenna_link.py        backend: PlutoLink (Tx tone / Rx power) + LinkServer (HTTP + WS)
pyproject.toml         deps: numpy + websockets (base); pyadi-iio + pylibiio (hardware extra)
frontend/
  index.html           layout
  src/style.css         dark-glass theme (shared look with pluto_beamformer)
  src/main.js           WebSocket client, strip chart, polar pattern
  vendor/plotly.min.js  vendored so the demo works offline
  favicon.svg
```

## Options

```
--pluto-uri URI   Pluto address (default ip:192.168.2.1)
--sim             synthetic power, no hardware
--port N          HTTP port (default 8080)
--ws-port N       WebSocket port (default 8765)
```
