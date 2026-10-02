<!-- .slide: class="title-slide" -->

<div class="title-left">

# ECE 444

Antennas, Phased Arrays, and Radar Systems

## Lesson 17 — Introduction to Phased Array Hardware

Fall 2026 · Dr. Neil Rogers

</div>

<div class="title-right">

![USAFA](./img/01-course-intro/USAFA-logo.png)

</div>

---

## Where we were

- The array factor sums $N$ elements with a progressive phase: $AF_N(\psi) = \frac{\sin(N\psi/2)}{N\sin(\psi/2)}$
- Pattern multiplication: element factor $\times$ array factor
- All of it assumed you can set **each element's amplitude and phase**
- Satisfying that assumption takes real hardware — eight phase shifters, eight attenuators, a combiner, a downconverter

**Today you meet the machine that provides it.**

Note:
Last lesson was entirely on paper. Every result depended on being able to hand
element number three its own phase. Today we open the box and find out what
that costs and what it constrains.

---

## Today's plan

1. Walk the receive chain: patches to Raspberry Pi
2. Why the PHASER is a hybrid beamformer, and what that decides
3. The frequency plan, traced with real numbers
4. Bring the station up and drive the browser interface
5. Read the Python that writes phases and tunes the SDR

Note:
Two background parts, then hands on the hardware for the rest of the period.
Every module three lab runs on this station, so today is the investment.

---

## The ADALM-PHASER receive chain

<div class="fig" data-inline-svg="./fig/L17-signal-chain.svg" style="max-width:790px; margin:0 auto;"></div>

Note:
Trace it left to right at the board with the students. Eight patches, eight
low-noise amplifiers, two four-channel beamformers, two mixers, one two-channel
software radio, one Raspberry Pi. Point at the physical parts on the board as
you name them.

---

## Front end: capture, amplify, weight

| Block | What it does |
| :-- | :-- |
| Patch $\times 8$ | 8 microstrip elements, $d = 14$ mm apart |
| ADL8107 LNA $\times 8$ | one per element, **ahead of everything lossy** |
| ADAR1000 $\times 2$ | phase + gain per element, then a 4:1 analog sum |

<div class="callout">
The ADAR1000 phase step is <strong>2.8125°</strong> — that is 360°/2<sup>7</sup>, a 7-bit phase shifter. Every element slider in the GUI writes a register in one of these two chips.
</div>

Note:
Gain first is deliberate. Noise figure is set by the first stage, and phase
shifters and combiners are lossy. Put the amplifier ahead of them and the loss
is divided by the gain when you refer it to the input.

---

## Back end: downconvert, digitize, command

| Block | What it does |
| :-- | :-- |
| LTC5548 mixer $\times 2$ | RF times LO, keep the difference |
| ADF4159 + HMC735 VCO | the tuned LO, 12.2–13.0 GHz |
| ADALM-Pluto (AD9361) | two Rx channels, tuned to 2.2 GHz, 3 MSPS |
| Raspberry Pi | SPI to the beamformers, `pyadi-iio`, browser UI |

Note:
Nothing in the lab digitizes X-band. The mixers hand the software radio a fixed
two point two gigahertz and the radio never learns what band the array is
looking at.

---

## Count the phase shifters, count the ADCs

**The board carries eight phase shifters and two ADC channels.** That ratio is the design decision.

| | Analog beamforming | Digital beamforming |
| :-- | :-- | :-- |
| Where on the PHASER | inside each ADAR1000, 4 elements | across the two subarray outputs |
| Weights available | 8, one per element | 2, one per channel |
| Receiver channels | 1 per subarray | 1 per channel |
| Beams at once | one | as many as software can compute |

Note:
A phase shifter and an attenuator at radio frequency are small, cheap and
low-power. A receive channel — mixer, filter, converter, and the plumbing to
carry samples away — is expensive in parts, area and power. Digitizing all
eight would give software complete freedom and cost four times the receiver
hardware.

---

## What the split decides

The PHASER is a **hybrid beamformer**: analog inside each 4-element subarray, digital across the two subarray outputs.

- Eight analog weights: steer, taper, and place a null wherever you want
- Once the ADAR1000 sums its four elements, those four signals are gone
- Software downstream sees **two** numbers per snapshot, not eight

<div class="callout">
In Lesson 28 the MVDR nulling algorithm gets exactly <strong>two</strong> digital degrees of freedom. That limit is set on this slide, not in the algorithm.
</div>

Note:
This is the slide to come back to in lesson twenty-eight. Students who
understand the hybrid split here will not be surprised when adaptive nulling
turns out to be sharply limited on this board.

---

## The frequency plan

<div class="fig" data-inline-svg="./fig/L17-frequency-plan.svg" style="max-width:790px; margin:0 auto;"></div>

<div class="callout">
The HB100 is a <strong>free-running dielectric resonator</strong>, not a synthesizer. Units land anywhere in 10.1–10.7 GHz, so the software has to <em>measure</em> the source before it can do anything else.
</div>

Note:
High-side injection: the local oscillator sits above the received signal, and
the mixer difference lands on the intermediate frequency. The intermediate
frequency is fixed by filtering, so retuning the array means retuning one block
and nothing else.

---

## Worked example — nominal HB100 to the IF

| Quantity | Work | Result |
| :-- | :-- | :-- |
| Source | measured by **Find HB100** | $10.525$ GHz |
| LO required | $f_{\text{LO}} = f_{\text{RF}} + f_{\text{IF}}$ | $12.725$ GHz |
| Inside 12.2–13.0 GHz? | yes, so it is reachable | ✓ |
| Mixer output | $12.725 - 10.525$ | $2.200$ GHz |
| Pluto tuning | fixed | $2.2$ GHz, 3 MHz window |

Run it backwards: LO limits of 12.2–13.0 GHz give **10.0–10.8 GHz** of RF coverage.

<div class="callout">
The window is only <strong>3 MHz wide</strong> at 3 MSPS. A tone 1 MHz off center is a clean peak; a tone 200 MHz off does not appear at all. An empty FFT is almost always a frequency error, not a dead array.
</div>

Note:
Have them do the reverse calculation at the board. Twelve point two minus two
point two is ten, thirteen minus two point two is ten point eight. Every HB100
they will be handed falls inside that. The callout is the most common failure
in this lab: before anyone debugs cables, check that the source frequency the
software believes matches the source on the bench.

---

## The station

- PHASER board on a tripod, **patch row horizontal**
- Raspberry Pi and ADALM-Pluto mounted on the back
- HB100 source on its own stand, about 1 m away at boresight
- USB-C supply for the board, supply for the Pi
- Laptop on the lab network — it only runs a browser

Bring-up: power, wait about a minute for the Pi, then browse to `http://phaser.local:8080`

Note:
The array steers in the plane of the patch row. A board mounted on its side
steers up and down and nothing in the lab works. Check the orientation before
anyone powers anything.

---

## The Phaser GUI

| Sidebar section | Today |
| :-- | :-- |
| Configuration | Signal Freq, **Rx Gain**, Calibrate |
| Element Gains | Rx1–Rx8 sliders, taper presets |
| Beam Steering | Steer Angle, Apply |
| Lab Presets | **1 Steering Angle** starts today's work |

Plot tabs: **Rectangular · Polar · FFT · Tracking**. **Start** runs a sweep, **Freeze** holds a reference trace.

<div class="callout">
<strong>Calibrate</strong> measures the eight per-element gain and phase offsets so that zero commanded phase gives a real broadside beam. <strong>Find HB100</strong> sweeps the LO until it locates the source. Both write files on the Pi; run each once, and let them finish.
</div>

Note:
Walk the sidebar on the projector before they touch anything. Today they only
need lab preset one, the frequency field, and the receive gain.

---

<!-- .slide: class="viz-cue-slide" -->

## The chain, one block at a time

- Click any block: what it does and what frequency lives at that node
- Drag the HB100 slider from 10.1 to 10.7 GHz
- The RF label moves. The LO label moves with it. **The IF label does not.**

<p class="viz-cue">↗ Interactive on the lesson page</p>

Note:
Demo live. Select the mixer, then drag the source slider and let them watch the
local oscillator track while the intermediate frequency stays pinned at two
point two. Ask why only one block has to change, then select the oscillator
block and read its description aloud.

---

## Procedure, part 1

1. Press **Lab Preset 1 (Steering Angle)** — loads the FFT tab in beam sweep mode
2. Place the HB100 about **1 m** away at boresight, patch face toward the array
3. Press **Find HB100** and record the frequency it reports
4. On the FFT tab, record the **peak frequency** and its height above the noise floor

Expect a clean single peak at least **20 dB** above a flat floor.

Note:
If the peak is missing, check the source is powered and pointed at the array
before touching anything in the software. If it is present but weak, check the
height and the aim rather than the gain.

---

## Procedure, part 2

5. Move **Rx Gain** down 10 dB, then up 10 dB. Record peak and floor at each setting.
6. Move **Signal Freq** by $-0.0005$ GHz. The peak walks 500 kHz down the window.
7. Rotate the HB100 away from the array by hand, then back. The peak drops and returns.

<div class="callout">
<strong>No hardware?</strong> Run <code>python phaser_headless.py --sim</code> and open <code>localhost:8080</code>. The synthetic source sits at boresight with its tone 1 MHz up in the baseband window. Step 3 is unnecessary and step 7 has no simulated equivalent — the simulated target cannot be moved.
</div>

Note:
Step five is the point about where noise is set. The receive gain lives inside
the software radio, long after the low-noise amplifiers have fixed how much
noise rides on the signal, so peak and floor move together. Step seven is their
first look at the element pattern, which they measure properly in lesson
twenty-three.

---

## Reading the code — tuning the SDR

```python
sdr = adi.ad9361(uri=ip)                 # the Pluto's AD9361
sdr.rx_enabled_channels = [0, 1]         # both subarray channels
sdr.sample_rate = int(sample_rate)       # 3e6 in the GUI
sdr.rx_lo = int(rx_lo)                   # 2.2e9 - the IF, never X-band
sdr.gain_control_mode_chan0 = "manual"
sdr.rx_hardwaregain_chan0 = int(rx_gain) # the Rx Gain slider, in dB
```

- `rx_lo` is **2.2 GHz every time** — the radio never learns the band
- AGC is switched off on purpose: a receiver that changes its own gain mid-sweep measures nothing

Note:
This is the whole of the tuning. Emphasize the manual gain control. If the
radio were allowed to ride its own gain during a beam sweep the pattern would
be flattened into meaninglessness.

---

## Reading the code — writing the phases

```python
def ADAR_set_Phase(array, PhDelta, phase_step_size, phaseList):
    for i in range(8):
        element_id = i + 1
        base_phase = phaseList[i] + i * PhDelta
        q_phase = round(base_phase / phase_step_size) * phase_step_size
        q_phase = q_phase % 360
        array.elements[element_id].rx_phase = q_phase
```

- `phaseList` — the per-element offsets **Calibrate** measured
- `i * PhDelta` — the linear ramp across the aperture, $\Delta\phi$ from Lesson 16
- `round(...) * phase_step_size` — quantized to $2.8125^\circ$, the hardware's limit

Note:
There are eight elements, one loop, and two lines of arithmetic. Lesson eighteen computes the
progressive phase from a steering angle. Lesson twenty-six studies what that
rounding does to the pattern.

---

## Deliverables

1. Measured HB100 frequency, required LO, resulting IF, and whether the LO is reachable
2. A block diagram you label yourself: every block, the frequency at each node, where the analog sum ends and the digital channels begin
3. FFT observations: peak frequency, peak and floor at three Rx Gain settings, the 500 kHz shift
4. Two written answers — why the software hunts for the HB100, and where the other six channels went

Note:
The two written answers are the ones that carry the lesson. Everything else is
a record of what they saw.

---

## Key point

<div class="callout">
<strong>Eight elements go in and two digital channels come out.</strong> The ADAR1000s form the beam in analog inside each four-element subarray, and only the two subarray sums are ever digitized. That single choice gives cheap per-element control and discards the per-element information, and it sets the limits of every lab from here to Lesson 28.
</div>

Note:
If they take one thing away, this is it. Write the ratio on the board: eight to
two.

---

## Where this is going

- **Lesson 18** — the path-length argument gives the steering phase: $\Delta\phi = kd\sin\theta_0$
- **Lesson 19** — back to this station to steer the real beam and measure where it points
- **Lesson 28** — the two digital channels stop being a detail and become the constraint

Before Lesson 18: review the array factor and be ready to say what $\psi$ is and why the pattern peaks when it is zero.

Note:
Today they have a machine that can put any phase on any element and no rule for
choosing it. Next lesson supplies the rule, and it is one line of geometry.
