---
frame_view: true
---

# L17 - Introduction to Phased Array Hardware

::::{frame}
:class: title-frame

<div class="course-mark">ECE 444 · Fall 2026</div>

<h1 class="frame-title">Introduction to Phased Array Hardware</h1>

<div class="title-rule"></div>

The ADALM-PHASER sets the phase and gain of each of its eight elements.

Lesson 17 · Antennas, Phased Arrays, and Radar Systems · Dr. Neil Rogers
::::

::::{frame} Slides
:class: read-only

:::{admonition} Slides
:class: slides

<a href="../../slides/L17-phased-array-hardware.html" target="_blank" rel="noopener">html slides</a>
<a href="../../slides/L17-phased-array-hardware.html?print-pdf" target="_blank" rel="noopener">pdf slides</a>
<a href="../../slides/L17-phased-array-hardware.md" target="_blank" rel="noopener">raw markdown slides</a>
:::
::::

::::{frame} Learning Objectives

<ol class="lo-list" style="--module: '3'; counter-reset: lo 2">
  <li>I can identify the hardware architecture of the ADALM-PHASER and control it via SDR software.</li>
</ol>

:::{depth}
Lesson 16 built the array factor by assuming we can hand every element its
own amplitude and phase, then add the results. Every result in array theory
rests on that assumption, and satisfying it takes real hardware: eight phase
shifters, eight attenuators, a summing network, a frequency converter, and a
computer to command all of it. Today we bring up that hardware in the first
hands-on session with the **ADALM-PHASER**, the 8-element X-band array the
rest of Module 3 runs on. By the end of the period you will have brought your
kit up from a blank card, found each block on the board, seen the
$10.525\ \text{GHz}$ source on a spectrum display, and watched the kit's beam
sweep follow the source when you move it. The lab packet records both: that
the kit came up, and that it works.

The page assumes no receiver course. It needs one idea about frequency: the
SDR cannot digitize 10 GHz, so the board shifts the signal down to
$2.2\ \text{GHz}$ before anything is digitized, and the SDR only ever listens
there.
:::
::::

::::{frame} The ADALM-PHASER Receive Chain
:::{present}
<picture>
<source media="(max-width: 600px)" srcset="../../viz/img/L17-signal-chain-narrow.svg">
<img src="../../viz/img/L17-signal-chain.svg" alt="ADALM-PHASER receive chain. Eight patches, each with its own LNA, feed two ADAR1000 beamformers, four elements each. Each ADAR1000's sum goes to a frequency converter, which shifts it from 10.525 GHz down to 2.2 GHz. The two 2.2 GHz outputs enter the Pluto SDR's Rx1 and Rx2, the Pluto passes its samples to the Raspberry Pi, and the Pi commands the ADAR1000s over SPI." style="max-width: 700px; width: 100%; display: block; margin: 0 auto;">
</picture>

- The PHASER is a receive array: eight patches capture the wave from a source in front of it.
- Everything between the patches and the Raspberry Pi turns eight microwave signals into two streams of numbers.
:::

The frames that follow take the blocks in the figure in order, from the
patches to the Pi.
::::

::::{frame} The Patches and the LNAs
:::{present}
- Eight patches sit in a row $d = 14\ \text{mm}$ apart, and their phase differences alone record the arrival angle:

$$\Delta\phi_n = n\ kd\sin\theta$$

- An LNA behind each patch sets the noise figure, because its gain divides down the noise of every later stage.
:::

Eight microstrip patches sit in a horizontal row on the front
face of the board, spaced $d = 14\ \text{mm}$ center to center. Each one is an
antenna in its own right with its own element pattern, and the total pattern is
that element pattern times the Lesson 16 array factor (pattern multiplication).
A wave arriving off broadside reaches the patches in sequence, so element $n$
differs from element 0 by the geometric phase $\Delta\phi_n = n\ kd\sin\theta$
of Lesson 16. Preserving that phase difference is the job of everything downstream.

An ADL8107 low-noise amplifier sits directly behind every patch,
ahead of any phase shifting or combining. Gain placed first sets the receiver's
noise figure, because the noise each later stage adds is divided by that gain
when referred to the input. Phase shifters and power combiners are lossy, so
the order here is deliberate.

:::{depth}
The rule is the cascade noise figure. For a chain of stages with noise factors
$F_1, F_2, F_3, \ldots$ and available gains $G_1, G_2, \ldots$, all as linear
ratios rather than decibels, the noise factor of the whole chain is

$$F = F_1 + \frac{F_2 - 1}{G_1} + \frac{F_3 - 1}{G_1 G_2} + \cdots$$

Lesson 12 wrote a receiver's own noise as an equivalent input temperature,
$T_e = T_0(F - 1)$ with $T_0 = 290\ \text{K}$. Substituting it stage by stage
gives the same rule in temperatures,

$$T_e = T_{e1} + \frac{T_{e2}}{G_1} + \frac{T_{e3}}{G_1 G_2} + \cdots$$

so each stage's noise counts at the input divided by all the gain ahead of it.
A passive lossy stage, such as a phase shifter or a combiner, has a noise
factor equal to its loss when it sits at the reference temperature
$T_0 = 290\ \text{K}$ ($F = L$).

The numbers that follow are illustrative, not datasheet values: an LNA with a
$2\ \text{dB}$ noise figure ($F_1 = 1.585$) and $20\ \text{dB}$ of gain
($G_1 = 100$), followed by a beamformer stage with $10\ \text{dB}$ of loss and
so a $10\ \text{dB}$ noise figure ($F_2 = 10$). With the LNA first,

$$\begin{aligned}
F &= F_1 + \frac{F_2 - 1}{G_1} \\
  &= 1.585 + \frac{10 - 1}{100} \\
  &= 1.675 \quad (2.24\ \text{dB}),
\end{aligned}$$

or $T_e = 196\ \text{K}$. With the lossy stage first, $G_1 = 0.1$ and

$$\begin{aligned}
F &= 10 + \frac{1.585 - 1}{0.1} \\
  &= 15.85 \quad (12.0\ \text{dB}),
\end{aligned}$$

or $T_e \approx 4300\ \text{K}$. The same two parts in the other order lower
the signal-to-noise ratio by $9.8\ \text{dB}$.
:::
::::

::::{frame} The ADAR1000 Beamformers
:::{present}
- Each ADAR1000 applies a phase and a gain to four RF inputs and sums them into one output.
- Its 7-bit phase shifter sets the phase in $2.8125^\circ$ steps.
- The GUI's eight element sliders write registers in these chips.
:::
:::{present}
<img src="../../viz/img/L17-adar-align.svg" alt="Three panels. Four adjacent elements receive a wave from 20 degrees off broadside, each 60.5 degrees behind the last. After their phase shifters, with equal gains, the four line up. Their sum has amplitude 4, against 1.70 for the uncorrected sum." style="max-width: 100%; display: block; margin: 0 auto;">
:::

Two ADAR1000 chips do the beamforming. Each is a 4-channel
analog beamformer: it applies a programmable phase and a programmable gain to
each of its four inputs at RF, then sums the four into a single output. Each
chip sets the phase in steps of

$$\frac{360^\circ}{2^7} = 2.8125^\circ,$$

the step size of a 7-bit phase shifter. We will use the gain as a taper in
Lesson 25. When the GUI shows you eight element sliders, those sliders are
writing registers in these two chips.

In the figure, a wave from $20^\circ$ off broadside reaches each element
$60.5^\circ$ behind the last; after the phase shifters the four line up and
sum to 4, against 1.70 uncorrected.

:::{depth}
In degrees,

$$kd = 360^\circ \times \frac{d}{\lambda} = 176.9^\circ$$

at $10.525\ \text{GHz}$. The figure's step is

$$\begin{aligned}
kd\sin 20^\circ &= 176.9^\circ \times 0.342 \\
  &= 60.5^\circ,
\end{aligned}$$

and the uncorrected sum of four unit phasors stepped by $\psi = 60.5^\circ$ is
Lesson 16's array factor with $N = 4$,

$$\left\lvert \sum_{n=0}^{3} e^{-jn\psi} \right\rvert
  = \frac{\sin(2\psi)}{\sin(\psi/2)}
  = \frac{\sin 120.9^\circ}{\sin 30.2^\circ} = 1.70,$$

against 4 once the shifters align them.

A progressive phase of one LSB steers the beam from broadside to

$$\theta_0 = \arcsin\frac{2.8125^\circ}{176.9^\circ} = 0.91^\circ.$$

That does not confine the beam to a $0.91^\circ$ grid. Each element's phase is
rounded on its own, so the rounding error varies across the ramp; its main
effect is a phase error that raises the sidelobes, which Lesson 26 computes:
about $-42\ \text{dB}$ at 7 bits, far below the sweep's 23 dB floor.
:::
::::

::::{frame} The Back End
:::{present}
The Pluto cannot digitize 10 GHz, so the board shifts the signal down first.

| Block | Role |
| :-- | :-- |
| 2 LTC5548 converters | X-band down to 2.2 GHz |
| ADALM-Pluto | digitizes both channels |
| Raspberry Pi | SPI, `pyadi-iio`, browser |
:::

The SDR that digitizes the array's output, an ADALM-Pluto, tunes no higher
than $6\ \text{GHz}$, so it cannot take a $10\ \text{GHz}$ signal directly.
Each ADAR1000 output therefore goes through an LTC5548 frequency converter,
which shifts it down to $2.2\ \text{GHz}$. The board sets the size of the
shift from the source's frequency, so whatever the HB100's exact frequency,
the signal always arrives at $2.2\ \text{GHz}$, and the SDR only ever listens
there.

The ADALM-Pluto, an AD9361 transceiver, digitizes the two
$2.2\ \text{GHz}$ channels. It samples at 3 MSPS in the course GUI and
produces two streams of complex samples.

:::{depth}
Each sample is a complex number $I + jQ$, and a complex signal can tell a
tone above the center from a tone below it. The sampling theorem from your
signals course says a real signal sampled at $f_s$ covers $0$ to $f_s/2$; a
complex signal sampled at $f_s$ covers $-f_s/2$ to $+f_s/2$, a window $f_s$
wide. At $3\ \text{MSPS}$ that window runs from $-1.5$ to $+1.5\ \text{MHz}$
around $2.2\ \text{GHz}$, and it is the window the FFT tab displays.
:::

The Pi on the back of the board runs the Python backend.
It writes phases and gains to the ADAR1000s over SPI, tunes the Pluto and sets
the frequency shift through `pyadi-iio`, reads the IQ buffers, and serves the
browser interface. Everything you do in the lab arrives here as a command over
a WebSocket.
::::

::::{frame} The Hybrid Beamformer
:::{present}
- Analog inside each 4-element subarray, digital across the two subarray outputs.
- A receiver costs far more than a phase shifter, so 8 shifters feed 2 receivers.
- Software sees two numbers, so Lesson 28's MVDR can null about one interferer.
:::
:::{present}
<img src="../../viz/img/L17-hybrid-split.svg" alt="Three receive architectures for eight elements, side by side. All analog: 8 phase shifters summed into 1 receiver, no digital weights. The PHASER hybrid: 8 phase shifters summed four at a time into 2 receivers, then 2 digital weights. Fully digital: no phase shifters, 8 receivers, 8 digital weights. Shading marks the digital side of the ADC." style="max-width: 100%; display: block; margin: 0 auto;">
:::

The PHASER is a **hybrid beamformer**, between fully analog and fully digital:
the ADAR1000s form the beam in analog inside each 4-element subarray, and
software combines the two subarray outputs digitally.

:::{depth}
Count the phase shifters and count the analog-to-digital converters. The board
carries eight phase shifters but only two ADC channels, and the rest of the
architecture follows from the decision to digitize at that 4:1 ratio.

A phase shifter and an attenuator at RF are small, cheap, and low-power, so
putting one behind each element adds little hardware. A receive channel — frequency converter,
filter, ADC, and the data path that carries the samples away — requires far
more parts, board area, and power. Digitizing all eight elements would give
software complete freedom to form any pattern after the fact, and it would
require four times the receiver hardware this board carries.
:::

| | PHASER, analog half | PHASER, digital half | Fully digital |
| :-- | :-- | :-- | :-- |
| Weights | 8, one per element | 2, one per subarray | 8, one per element |
| Receiver channels | none | 2, one per subarray | 8, one per element |
| Beams at once | one | several, from the same two subarray patterns | many, each independent |

:::{depth}
Two digital channels can form more than one beam from one set of samples, but
every such beam is a weighted sum of the same two subarray outputs, whose
patterns the analog weights already fixed. None of them can point
independently of the analog steer, which is what a fully digital array, with
one ADC per element, can do.
:::

:::{callout}
The hybrid split fixes how many weights each later lab can use. Eight elements
give us eight analog weights, so the array can steer, taper, and place a null
anywhere we choose. But once the ADAR1000 sums its four elements, the
individual element signals are gone, and software downstream sees two numbers,
not eight. When we reach adaptive nulling in Lesson 28, the MVDR algorithm has
exactly two digital degrees of freedom to work with, because the ADAR1000s sum
the elements in analog before anything is digitized. One of those degrees of
freedom holds the look direction, and $N$ channels can null about $N - 1$
interferers, so this board can null about one.
:::
::::

::::{frame} The HB100 Source
:::{present}
- The HB100's free-running dielectric resonator puts each unit anywhere from $10.1$ to $10.7\ \text{GHz}$, and it drifts with temperature.
- That spread is 200 times the Pluto's $3\ \text{MHz}$ window, so **Find HB100** measures each unit before anything uses it.
:::
:::{present}
<img src="../../viz/img/L17-hb100-spread.svg" alt="Two panels. Top: an axis from 10.0 to 10.8 GHz with the 10.1 to 10.7 GHz spread of HB100 units as a band, and the Pluto's 3 MHz window drawn to scale as a hairline at 10.525 GHz, one two-hundredth of the spread. Bottom: that window magnified, with one tone 1 MHz above Signal Freq standing 32 dB over a flat noise floor." style="max-width: 100%; display: block; margin: 0 auto;">
:::

The source is an **HB100** Doppler module, a self-contained X-band transmitter
about the size of a matchbox. Its nominal output is $10.525\ \text{GHz}$. The
oscillator inside it is a free-running dielectric resonator oscillator (DRO),
not a locked synthesizer. No reference corrects it, so the actual frequency of
any particular unit is set by the mechanical dimensions of that resonator and
drifts with temperature. Units land anywhere from about $10.1$ to
$10.7\ \text{GHz}$. This is why the GUI has a **Find HB100** button: the
software steps the board's frequency shift across the band, watches for the
tone in the SDR's window, and records the frequency where it appears. That
answer becomes **Signal Freq**, the source frequency the board sets its shift
from, so that the source lands at $2.2\ \text{GHz}$.

The lower panel of the figure magnifies the $3\ \text{MHz}$ window with a
source $1\ \text{MHz}$ above Signal Freq. With Signal Freq set by Find HB100,
the tone sits near $0\ \text{MHz}$. A source $200\ \text{MHz}$ from Signal
Freq lands far outside the window and does not appear at all, which is what a
skipped Find HB100 looks like on the screen.

:::{depth}
Find HB100 solves the 200-to-1 problem by widening the window and stepping it.
It captures at 30 MSPS, a $30\ \text{MHz}$ window, and steps
$10\ \text{MHz}$ at a time so that the window walks across $10.0$ to
$10.7\ \text{GHz}$ in 70 steps, overlapping as it goes, and keeps the
frequency where the tone stands highest.
:::

:::{depth}
The board can shift any source from $10.0$ to $10.8\ \text{GHz}$ down to
$2.2\ \text{GHz}$, so every HB100 the lab issues is reachable. The patches are
designed for $10.0$ to $10.5\ \text{GHz}$. Lesson 13's estimate for a thin
patch, one or two percent, is only $103$ to $205\ \text{MHz}$ at
$10.25\ \text{GHz}$, so the PHASER's patches are built broader than Lesson
13's thin patch, and their match still degrades outside the design band. A
unit near the top of the HB100 spread therefore gives a weaker peak, by the
mismatch loss, but the peak does not disappear.
:::
::::

::::{frame} Signal Chain Explorer
:class: viz-frame

:::{depth}
The widget below is the same chain as the figure, but you can click it. Select a
block to see what it does and what frequency the signal has at that point, then
drag the HB100 slider and watch the source frequency move while the frequency
the SDR receives stays at $2.2\ \text{GHz}$. The converter absorbs every
change in the source, so the SDR's tuning and sample rate never change.
:::

:::{present}
<iframe src="../../viz/phaser-signal-chain.html?plain=1"
        width="100%" height="418"
        style="border: 1px solid #cddce9; border-radius: 6px;"
        loading="lazy"
        title="Interactive block diagram of the PHASER receive chain with a tunable HB100 source">
</iframe>
:::
::::

::::{frame} Part A: Bring Up Your PHASER
:::{present}
- Each cadet brings their own kit up from a blank microSD card in six stages: flash, name, boot, connect, update, and calibrate.
- The Ethernet cable carries ssh and the browser; the Wi-Fi only connects the Pi to the internet.
:::
:::{present}
<img src="../../viz/img/L17-part-a-network.svg" alt="Part A network. The laptop, at 192.168.7.1, reaches the Pi, at 192.168.7.13, over the Ethernet cable, which carries ssh and the browser interface on port 8080. The Pi joins the AF_ACADEMY_GUEST Wi-Fi and reaches GitHub through it to run install.sh. A path from the laptop through the Wi-Fi access point to the Pi is crossed out, because the guest network can isolate its clients from each other." style="max-width: 100%; display: block; margin: 0 auto;">
:::

Each cadet starts today with their own PHASER kit and a blank microSD card and brings the
kit up itself: you flash the course image onto the card, name the kit, boot it,
connect to it, update its software, and calibrate it. Part B then makes the
first measurements on the kit you brought up.

The laptop and the kit use two connections for two different jobs. A direct
Ethernet cable from the laptop to the Pi carries ssh and the browser interface.
The classroom Wi-Fi is only the Pi's route to the internet, which it needs for
the software update.

:::{depth}
The cable is there because of how guest networks are run. A guest network can
isolate its clients from one another, so a laptop and a Pi that have both
joined the classroom Wi-Fi may be unable to reach each other even though each
one reaches the internet. A cable between the two does not depend on the
network's settings, so every step that talks to the Pi from the laptop uses the
cable.
:::

Each cadet has their own kit:

- the ADALM-PHASER board, with the Raspberry Pi and the ADALM-Pluto attached on the back
- an HB100 microwave source on its own small stand or battery holder
- a USB-C supply for the board and a supply for the Pi
- a camera tripod, for the board and for aiming the source
- a blank microSD card and an Ethernet cable
- a laptop with Raspberry Pi Imager, a plain-text editor, and an ssh client

The course image, `phaser-golden.img`, is on the course share at
**[path to be added]**.

:::{depth}
The instructor builds the golden image once. The procedure, from the Phaser
repository's `docs/golden-image.md`, is to provision one kit, verify that it
calibrates and runs a lab, arm it for cloning with
`provision.sh --prepare-image`, and copy its card to a file. Every card flashed
from that file starts as a copy of the same working kit, with the operating
system configured and the course software already installed, so you never run
`provision.sh` or the card-preparation tools yourself.

On Windows the ssh client is the OpenSSH Client, under Settings > Apps >
Optional features; macOS and Linux include one.
:::
::::

::::{frame} Flash the Card
:class: read-only

:::{present}
1. Copy `phaser-golden.img` to the laptop.
2. Insert the card.
3. In Raspberry Pi Imager, choose **Use Custom** and the image.
4. Choose the microSD card as storage, not a laptop drive.
5. Decline customization, then write and verify.
:::

The image is on the course share, and the card goes in the laptop's card
reader. **Use Custom** is the last entry in Imager's
**Choose OS** list. Imager
offers its OS customization settings before it writes the card, and it
verifies the card after writing it.

Imager erases whatever storage it writes to, so check that the storage you chose
is the microSD card before you start the write.

:::{depth}
Imager's customization settings install their own first-boot script, through
the same `systemd.run=` entry in the card's `cmdline.txt` that the Phaser setup
tools use, and they can rename the kit and change its user and password. The
golden image carries its own first-boot setup, described two frames ahead, so
we leave Imager's turned off.
:::
::::

::::{frame} Name the Kit
:class: read-only

:::{present}
Kit NN is `phaser-NN` at `192.168.7.(10 + NN)`; examples use kit 03.

6. Reinsert the card to open its FAT partition.
7. In `phaser-hostname`, replace `phaser` with `phaser-03`.
8. In `phaser-ip`, replace `#192.168.7.2/24` with `192.168.7.13/24`, then save and eject.
:::

Your instructor assigns your kit a two-digit number, NN, so kit 03 is
`phaser-03` at `192.168.7.13`. Kit 03 appears in every example from here on;
use your own number.

The FAT partition is the small one that holds `config.txt` and `cmdline.txt`;
leave those two alone. Edit `phaser-hostname` and `phaser-ip` in a plain-text
editor. `phaser-hostname` holds one line, and
in `phaser-ip` you replace the last line and leave out the `#`.

:::{depth}
The two files sit on the FAT partition because it is the one part of the card
that Windows and macOS can write without extra tools. `phaser-hostname` is read
once, on the first boot. `phaser-ip` is read at every boot by
`phaser-netalias`, which adds the address as an alias alongside whatever DHCP
assigns, on the wired port only and once per boot. A line that starts with `#` is a comment, and the golden card ships
that line commented out, so a kit you do not edit has no fixed address. Each
kit gets its own name and address because kits that share either one collide
on the network.

Windows may offer to format the card's other partition, which it cannot read.
Cancel that offer, because formatting it erases the image. In Notepad's Open
dialog, choose All Files, because the two files have no extension.
:::
::::

::::{frame} First Boot
:class: read-only

:::{present}
9. Mount the PHASER on the tripod, patch face vertical and patch row horizontal.
10. Put the card in the Pi.
11. Run the Ethernet cable to the laptop.
12. Connect both supplies and wait through one automatic reboot.
:::

The two supplies in step 12 are the board's and the Pi's. The Pi reboots once
by itself during its first boot, and it does not answer until it has
restarted.

The array steers in the plane of its row of patches, so a board mounted on its
side steers in elevation, while every later lab sweeps the beam in azimuth.

Until its first boot, the card is a copy of the golden kit, including that kit's
SSH host keys and its `/etc/machine-id`. A service the instructor armed,
`phaser-firstboot`, runs before the ssh server starts. It:

- sets the hostname from `phaser-hostname`
- deletes the SSH host keys and generates new ones
- regenerates `/etc/machine-id` and deletes stale DHCP leases
- disables itself and reboots once

:::{depth}
Without the reset, every kit cloned from one image would be the same machine.
The **host key** is how ssh identifies the machine it reached. With identical
keys, the laptop's `known_hosts` file cannot tell the kits apart, and a key
copied off one kit would impersonate all of them. The **machine-id** is the
identifier the operating system's own services use to tell one installation
from another; the system journal and D-Bus both key on it. On an image whose
network is run by systemd-networkd, the DHCP client identity comes from it too,
so two kits with the same one would request the same lease and take turns
losing it. This kit's `dhcpcd` identifies itself by the adapter's hardware
address instead, so here the reset keeps each kit a distinct machine rather
than saving its lease.

The service runs before the ssh server, so the golden kit's keys are never
offered to anyone. It reboots because the init system reads the machine-id only
at boot. It records the time it ran in `/var/lib/phaser/firstboot-done`, and
because that file exists, it never runs again on this card.
:::
::::

::::{frame} The Cable Connection
:class: read-only

:::{present}
13. Give the laptop's wired adapter `192.168.7.1`, mask `255.255.255.0`, and no gateway.
14. Run `ssh analog@192.168.7.13`.
15. Answer `yes`.
16. Enter the password `analog`.
17. Check that `hostname` prints `phaser-03` and `hostname -I` lists `192.168.7.13`.
:::

The address in step 13 goes on the laptop's wired Ethernet adapter, and step
14 runs in a terminal. The `yes` in step 15 answers ssh's question about
whether to trust the kit's host key.

:::{depth}
Nothing on a direct cable hands out addresses, so the laptop needs one of its
own on the same `/24` network as the kit's alias. The address `192.168.7.1`
sits below every kit's address, and each kit has its own cable, so every
laptop can use it.

The kit's fixed address exists only on its wired port, added once at boot,
which is why the cable goes in before the power (steps 11 and 12). If you
unplug the cable and plug it back in later, power-cycle the kit.

`analog` is the user and the password that ADI's Kuiper image ships with, and
the golden image keeps both unless your instructor says otherwise. The
host-key question appears because the first-boot reset gave this kit new keys
that the laptop has never seen. If ssh times out, the kit may still be in its
first boot; wait and try again. Where mDNS resolves, `ssh analog@phaser-03.local`
reaches the same kit, but the fixed address works without it.
:::
::::

::::{frame} Wi-Fi and the Software Update
:class: read-only

:::{present}
18. Check `wpa_supplicant.conf`, then run the Wi-Fi commands in order.
19. Run `ping -c 4 github.com` and expect four replies.
20. Run the `install.sh` line and wait for `Installed.`
:::

The classroom Wi-Fi is the open guest network `AF_ACADEMY_GUEST`. If the
instructor added the network to the golden image, it is already in the file:
run `cat /etc/wpa_supplicant/wpa_supplicant.conf` first, and skip the `tee`
command if `AF_ACADEMY_GUEST` appears.

The commands below set the Wi-Fi country, add the network to
`/etc/wpa_supplicant/wpa_supplicant.conf`, and tell the Wi-Fi client to reread
that file. `sudo` asks for the same password, `analog`.

```bash
sudo raspi-config nonint do_wifi_country US
sudo tee -a /etc/wpa_supplicant/wpa_supplicant.conf > /dev/null <<'EOF'

network={
    ssid="AF_ACADEMY_GUEST"
    key_mgmt=NONE
}
EOF
sudo wpa_cli -i wlan0 reconfigure
```

:::{depth}
The Kuiper image on this kit is based on Raspberry Pi OS bullseye, where
`wpa_supplicant` joins the Wi-Fi network and `dhcpcd` then requests an address
on it. The Wi-Fi country is a regulatory setting: the channels a radio may use
depend on where it is, so the operating system keeps the Wi-Fi radio blocked
(rfkill) until a country is set. The network block names the network, and
`key_mgmt=NONE` tells `wpa_supplicant` it has no password. `tee -a` appends the
block with root privileges, which a plain `>>` redirection would not have.
:::

Four replies mean the Pi reaches the internet over the Wi-Fi.

If the ping fails, tell the instructor rather than going on to the update.

:::{depth}
Two things must hold on an open guest network for this step and the next to
work, and the instructor checks both before class. The network must not put a
captive portal, a sign-in or terms page, in front of a new client, because the
Pi has no browser to click through one. It must also allow outbound HTTPS,
because the installer downloads the Phaser software from GitHub over HTTPS.

A failed ping does not stop the lab. The golden image already carries a working
backend, so the kit can run Part B without the update, and the instructor can
install the update from a local copy: `install.sh` installs from a directory on
the Pi, with no download, when `PHASER_SRC` names that directory.
:::

In the ssh session from step 14, run the installer. If `sudo` asks for a
password, it is `analog`.

```bash
curl -fsSL https://raw.githubusercontent.com/livethisdream/phaser/main/install.sh | bash
```

The installer prints its steps, `[1/6]` through `[6/6]`, and ends with
`Installed. Service is active and the UI answered HTTP 200.` and two addresses
for the interface.

:::{depth}
`install.sh` runs on the Pi. It downloads the current Phaser software from
GitHub, installs any missing Python packages, copies the backend into
`/home/analog/pyadi-iio/examples/phaser/`, replaces the browser interface,
updates the systemd unit if it has changed, restarts the `phaser-headless`
service, and checks that the interface answers. It never overwrites the kit's
`config.py`, and running it again is how you update a kit later.

The second address it prints is the first one `hostname -I` lists, which may be
the Pi's Wi-Fi address; use the fixed address instead. If the download fails
with a certificate error, the Pi's clock may be wrong, because a Raspberry Pi
has no battery-backed clock. The Phaser README's fix is
`sudo date -s "$(curl -sI http://deb.debian.org/ | sed -n 's/^[Dd]ate: *//p')"`,
after which you run the installer again.
:::

The lines the installer prints along the way are for the instructor; Part 2
of the lab packet records only its last line.
::::

::::{frame} The Phaser GUI
:class: read-only

:::{present}
21. Browse to `http://192.168.7.13:8080` and wait for the pill to read **Connected**.

Today you need four sidebar controls, **Find HB100**, **Calibrate**, **Signal Freq**, and **Rx Gain**, and the **FFT** tab.
:::

The pill sits at the bottom right and changes from **Checking...** to
**Connected**. **Start** stays disabled until the backend is ready.

The browser reaches the Pi over the cable, at the same fixed address as ssh.

:::{depth}
If the pill never reads **Connected**, turn on **Show Logs Tab** under **Plot
Options** and read the **Logs** tab: a message such as "Start blocked until
backend is ready" says the backend is still starting, and the page will
connect on its own once it is up. Where mDNS resolves,
`http://phaser-03.local:8080` reaches the same interface.
:::

The interface has a **sidebar** of control sections on the left and a **plot
area** with tabs on the right. You will use all of these over the next several
lessons; today only a few matter.

| Sidebar section | What lives there |
| :-- | :-- |
| Configuration | **Calibration** group: Calibrate, Find HB100, Reboot. Then Signal Freq (GHz), Signal BW (MHz), Rx Gain (dB), Tx Gain (dB), Tx Mode. **Connection** group: Simulator Mode, Backend URL (leave it empty) |
| Element Gains | E1–E8 gain sliders (0–100%); Window Presets Rect, Cheb, Hann, Black; Aperture Presets 2-Elem, Sparse λ; Enforce Symmetric Taper |
| Phase Control | E1–E8 phase offsets and Reset |
| Beam Steering | Steer Angle (deg), Taper (Uniform, Chebyshev, Hann, Blackman), Apply |
| Quantization | Steer Resolution (deg), Phase Shift Bits, Use Bits (ignore Steer Res) |
| Digital Beam Forming | Mode for the two digital channels: Manual (Reset, Beam 0/1 Gain and Phase) or MVDR (Snapshots (K), Diagonal Load) |
| Plot Options | Show Peak Gain Marker, Show Peak Angle Marker, Show Beam Squint Info, Show Logs Tab, Show Monopulse Delta Beam, Show Monopulse Error Function; X Min, X Max, Y Min, Y Max |
| Lab Presets | buttons 1 Steering Angle through 8 Tracking, one per workshop lab |

The plot tabs are **Rectangular**, **Polar**, **FFT**, and **Tracking**, plus
**Logs** when **Show Logs Tab** is on. **Start** runs the beam sweep, and
nothing plots until you press it. Today you work in the FFT tab, which plots
Amplitude (dBFS) against Frequency (MHz) for the two subarray outputs summed,
taken at the steering angle where the sweep saw the strongest signal.

:::{depth}
The FFT tab refreshes once per sweep. **Freeze** stores up to three reference
traces on the Rectangular and Polar tabs, and pressing and holding it clears
them; it is unavailable on the FFT tab.
:::
::::

::::{frame} Source Search and Array Calibration
:class: read-only

:::{present}
22. Place the powered HB100 $1\ \text{m}$ out at boresight.
23. Press **Find HB100** and record its frequency.
24. Then press **Calibrate**.
:::
:::{present}
:class: callout

Let each button finish. Holding the **Connected** pill for two seconds shuts the Pi down.
:::

Set the HB100 about $1\ \text{m}$ in front of the array, at the same height as
the patch row, with its own patch face toward the board.

:::{depth}
One meter is the shortest far-field distance for this array. Lesson 5's
far-field boundary, with the aperture $D = Nd = 8 \times 14\ \text{mm} = 112\ \text{mm}$
and $\lambda = 28.5\ \text{mm}$, is

$$\frac{2D^2}{\lambda} = \frac{2\ (0.112\ \text{m})^2}{0.0285\ \text{m}} = 0.88\ \text{m},$$

so moving the source closer than about $0.9\ \text{m}$ raises the signal but
curves the arriving wavefront enough to distort the patterns of later labs.
:::

Run Find HB100 first, because Calibrate reads the frequency that Find HB100
stores.

**Find HB100** searches the band until it locates the source and writes the measured
frequency to a calibration file on the Pi. Run it once per source, at the start
of the period, with the HB100 powered and pointed at the array. Every later
calculation the software does uses that number.

:::{depth}
The steering phase is where the frequency enters. Lesson 18 derives the
progressive phase

$$\Delta\phi = kd\sin\theta_0, \qquad k = \frac{2\pi f}{c},$$

so the same steering angle needs a different phase at a different frequency.
For a $30^\circ$ steer the ramp is $84.9^\circ$ per element at
$10.1\ \text{GHz}$ and $89.9^\circ$ at $10.7\ \text{GHz}$, and a ramp computed
for the wrong frequency points the beam at the wrong angle.
:::

**Calibrate** measures the per-element gain and phase offsets of the array
itself — the small differences between the eight channels caused by trace
lengths and part tolerances — and stores them so that zero commanded phase
across the array produces a broadside beam. The stored calibration survives a
reboot, so you normally run it once at the start of a lab period and leave it
alone.

:::{note}
Both buttons write files on the Pi and take some seconds to finish. Each opens a
**Calibration** window that reports progress, and the button reads
**Calibrating...** or **Scanning...** until it finishes. Wait for it, and do not
press either button again while it runs; use **Cancel** only if it stalls.
Leave **Reboot**, the third button beside them, alone.
:::

Expect **Find HB100** to report a frequency within a few hundred MHz of
$10.525\ \text{GHz}$. Leave the source at boresight while **Calibrate** runs, and
wait for it to finish.

:::{depth}
Both buttons write `calibration.json` on the Pi, which holds the HB100
frequency and the per-element phase and gain corrections. A freshly flashed card
carries the golden kit's copy of that file, which describes the golden kit's
source and board rather than yours, and these two runs replace it.
:::

:::{admonition} No hardware?
:class: tip

Part A has no simulated version, because every step acts on the card, the Pi,
or the network. If your kit will not come up, tell the instructor. The hosted
simulator covers Part B.
:::
::::

::::{frame} Part B: First Measurements
:::{present}
1. Press **1 Steering Angle** under **Lab Presets**.
2. Set **Rx Gain (dB)** to 10 and press **Start**.
3. Record the FFT peak's position, its level, and the floor, in dBFS.

Expect at least 20 dB between peak and floor.
:::

Part B runs on the kit you brought up in Part A and records the observations
any working kit produces, for Part 2 of the lab packet. Work through the steps
in order.

The preset loads the workshop's initial state, with a uniform taper, Phase
Control at zero, and the beam commanded to broadside, and opens the FFT tab;
**Start** begins the sweep. The presets do not set Rx Gain, whose start-up
value comes from the Pi's configuration file, so step 2 sets the 10 dB that
every later lab uses as its reference. dBFS is decibels relative to the ADC's
full-scale input.

In the FFT tab, a single narrow peak should stand well above a flat noise
floor, near $0\ \text{MHz}$, and its separation from the floor, in dB, should
be unambiguous: at least 20 dB with the source at $1\ \text{m}$, the smallest
separation seen on the bench at that distance. Less than that points to a
misaimed or distant source, or a weak battery in the HB100.

:::{depth}
Lesson 2's Friis equation sets the peak,

$$P_r = P_t G_t G_r \left(\frac{\lambda}{4\pi R}\right)^2;$$

doubling the distance lowers it by $20\log_{10}2 = 6.0\ \text{dB}$, and
misaiming the HB100 lowers its $G_t$. On the receive side, Lesson 21's
broadside directivity of the uniform array is

$$\begin{aligned}
D &\approx \frac{2Nd}{\lambda} \\
  &= \frac{2 \times 8 \times 14\ \text{mm}}{28.5\ \text{mm}} \\
  &= 7.86 \quad (8.96\ \text{dB})
\end{aligned}$$

at $10.525\ \text{GHz}$ (7.7 at the workshop's $10.3\ \text{GHz}$), the $G_r$
of the Friis equation.

The floor in the FFT is the noise in one frequency bin, so the peak-to-floor
separation also depends on the FFT length: a longer FFT narrows each bin,
lowers the floor, and raises the separation with no change at the antenna.
:::
::::

::::{frame} The Sweep Follows the Source
:class: read-only

:::{present}
4. Open the **Rectangular** tab and turn on **Show Peak Angle Marker** under **Plot Options**.
5. Record **Est. Angle** and **Peak Array Gain** with the source at boresight.
6. Carry the HB100 to about $30^\circ$ on one side, still $1\ \text{m}$ out and aimed at the array. Record both again, and which end of the array, E1 or E8, it moved toward.
7. Return the HB100 to boresight and record both once more.
:::

The Rectangular tab plots the beam sweep: the backend steers the beam across
the field of view one phase step at a time and records the received power at
each step, so the trace peaks where the beam points at the source. With the
source at boresight, Est. Angle should read within about $2^\circ$ of
$0^\circ$.

The source sits at $30^\circ$ when it is $0.5\ \text{m}$ to one side of the
array's centerline and still $1\ \text{m}$ from the array. The peak should
move with it, to about $30^\circ$, and drop by a dB or so, because each patch
receives less from the side. Returned to boresight, the trace comes back to
where it started. The sign of the moved reading records which side the GUI
calls positive, which Lesson 19 uses.

:::{depth}
On a working kit the sweep's floor sits about 23 dB below the uniform-taper
peak. A normal FFT peak with a sweep that stands well short of that, or that
peaks far from $0^\circ$ with the source at boresight, points to the
calibration rather than the signal: check that Phase Control reads zero, then
put the source back at boresight and run **Calibrate** again. Lesson 18
derives why the sweep peaks at the source, and Lesson 19 measures it on a
protractor arc.
:::

:::{admonition} No hardware?
:class: tip

Open [livethisdream.github.io/phaser](https://livethisdream.github.io/phaser/),
the same dashboard with no install. At a station whose hardware has failed, add
`?sim=1` to the station's URL or turn on **Simulator Mode** under
**Configuration**. An orange **SIMULATION** pill marks simulated data.

Steps 1 to 5 of Part B behave as described, except that the tone appears at
$-1\ \text{MHz}$ and the simulator does not model Rx Gain. Steps 6 and 7
cannot be done, because the simulated source is fixed at boresight. Find
HB100 and Calibrate run scripted scans.
:::

:::{depth}
With a checkout of the Phaser repository and Python,
`python phaser_headless.py --sim` serves the same page at
`http://localhost:8080`.
:::
::::

::::{frame} Reading the Code: Tuning the SDR
:::{present}
```python
sdr = adi.ad9361(uri=ip)
sdr.sample_rate = int(sample_rate)
sdr.rx_lo = int(rx_lo)
sdr.gain_control_mode_chan0 = "manual"
sdr.rx_hardwaregain_chan0 = int(rx_gain)
```

- `rx_lo`, the SDR's tuned frequency, is $2.2\ \text{GHz}$ every time, never X-band.
- Automatic gain control is off, because a gain that changes during a sweep distorts the measured pattern.
:::

Everything the GUI does reaches the hardware as a `pyadi-iio` call. Short
excerpts from the course backend cover the parts you have just used.

:::{depth}
The first excerpt is the full `SDR_init` setup, which tunes the SDR and sets
its gain:

```python
sdr = adi.ad9361(uri=ip)                 # the Pluto's AD9361 transceiver
sdr.rx_enabled_channels = [0, 1]         # both subarray channels (set via a fallback helper)
sdr.sample_rate = int(sample_rate)       # 3e6 in the GUI
sdr.rx_lo = int(rx_lo)                   # 2.2e9, where the SDR listens
sdr.rx_rf_bandwidth = int(sample_rate)
sdr.rx_buffer_size = int(buffer_size)    # 16384 samples
sdr.gain_control_mode_chan0 = "manual"
# Rx Gain (dB) at start-up; the slider later adds each channel's calibration trim
sdr.rx_hardwaregain_chan0 = int(rx_gain)
sdr.gain_control_mode_chan1 = "manual"
sdr.rx_hardwaregain_chan1 = int(rx_gain)
```
:::

Line by line: `adi.ad9361` opens a connection to the transceiver at a network
address, and the two enabled receive channels are the two subarray outputs. The
sample rate fixes the width of the window the SDR captures, and `rx_rf_bandwidth`
matches the analog filter to it. `rx_lo` is the tuned frequency. The backend switches off automatic gain control, because a receiver
that changes its own gain during a beam sweep scales each angle's sample by a
different amount and distorts the measured pattern. When you move the **Rx
Gain** slider, the backend writes its value plus each channel's calibration
trim to the two manual gains.
::::

::::{frame} Reading the Code: Writing the Phases
:::{present}
```python
for i in range(8):
    element_id = i + 1
    ramp = round(i * PhDelta / phase_step_size) * phase_step_size
    q_phase = (ramp + phaseList[i]) % 360
    array.elements[element_id].rx_phase = q_phase
array.latch_rx_settings()
```

- `phaseList` holds the **Calibrate** corrections plus your **Phase Control** offsets.
- The software rounds only the ramp `i * PhDelta`; the chip sets the nearest of its 128 states.
- `latch_rx_settings()` moves all eight phases into the live beam at once.
:::

:::{depth}
The next excerpt is the full function that writes the array's phases:

```python
def ADAR_set_Phase(array, PhDelta, phase_step_size, phaseList):
    """Set array phases for a given steering delta."""
    for i in range(8):
        element_id = i + 1
        # Quantize the steering ramp; leave the offsets at full resolution.
        ramp = round(i * PhDelta / phase_step_size) * phase_step_size
        q_phase = (ramp + phaseList[i]) % 360
        array.elements[element_id].rx_phase = q_phase
    # The rx_phase writes sit in SPI shadow registers until they are latched.
    array.latch_rx_settings()   # nothing takes effect until this runs
```
:::

Here `array` is the `pyadi-iio` object that represents both ADAR1000s as one
8-element array, so `array.elements[1]` through `array.elements[8]` reach the
individual channels regardless of which chip they live on. `PhDelta` is
the progressive phase from element to element, the $\beta$ of Lesson 16, which
Lesson 18 calls $\Delta\phi$, so `i * PhDelta` builds the linear phase ramp
across the aperture. The software rounds only that ramp, to `phase_step_size`,
which follows the GUI's **Phase Shift Bits** and is $2.8125^\circ$ at 7 bits;
it adds the offsets unrounded and wraps the sum into $0$ to $360^\circ$, and the
chip then sets the nearest of its 128 phase states. The writes wait in shadow registers until
`latch_rx_settings()` moves all eight into the live beam at once. Lesson 18
computes `PhDelta` from a steering angle, and Lesson 26 studies what that
rounding does to the pattern.

:::{depth}
The code adds `+i * PhDelta`, and Lesson 18 writes the ADAR1000 setting the
same way, $\phi_n = +n\ \Delta\phi$, so the code and Lesson 18 agree: a rising
ramp steers the beam to a positive angle, the side the sweep plot calls positive.
The GUI's Beam Steering **Apply** writes the opposite ramp into Phase Control as
offsets, for a reason Lesson 19 explains.
:::

The matching call for the taper writes gains instead of phases:

```python
array.elements[element_id].rx_gain = int(taper_list[i])   # 0-127
array.elements[element_id].rx_attenuator = not bool(taper_list[i])
array.latch_rx_settings()                                 # after the loop
```

The register runs from 0 to 127. The backend scales the GUI's 0–100% slider by
127/100 and by the gain calibration before it calls this, and a zero switches
the element's attenuator in, so a nulled element is off rather than only
turned down.
::::

::::{frame} Lab Packet
:class: read-only doc-links

The Lab 4 packet is one submission for the whole lab, turned in complete before Lesson 18. It has three parts:

1. **Part 1, Pre-Lab** (individual, before the lab period): the receive chain in order, the phase shifter's step, the element and channel counts, and how a kit number sets the kit's name and address.
2. **Part 2, Measurements** (your own kit's data, recorded in class): the bring-up record from Part A, and the kit check from Part B, the FFT peak and the sweep with the source at boresight, moved, and back.
3. **Part 3, Writeup** (individual, after the lab): a labeled block diagram, two bench diagnoses, and two written answers.

- <a class="doc-link" href="../../labs/ECE444_Lab_L17_Hardware_blank.pdf" target="_blank" rel="noopener">Lab 4 packet (PDF)</a>
::::

::::{frame} Summary
:class: read-only

| Symbol / idea | What it is | Number to remember |
| :-- | :-- | :-- |
| $d$ | patch pitch along the array | $14\ \text{mm}$, which is $0.491\lambda$ at 10.525 GHz |
| ADAR1000 | 4-channel analog beamformer, phase and gain per element | two chips, four elements each, phase step $2.8125^\circ$ |
| Hybrid split | analog sum inside a subarray, digital across subarrays | 8 elements in, 2 digital channels out |
| Frequency converter | shifts each subarray sum from X-band down to where the SDR listens | $2.2\ \text{GHz}$, for any source from 10.0 to 10.8 GHz |
| HB100 | free-running DRO source, not a synthesizer | $10.525\ \text{GHz}$ nominal, found anywhere in 10.1–10.7 GHz |
| Find HB100 | measures the source's frequency and sets Signal Freq | run once per source, before Calibrate |
| ADALM-Pluto | AD9361 SDR, two receive channels | 3 MSPS in the GUI, a 3 MHz window at 2.2 GHz |
| Beam sweep | received power against steered angle, source fixed | peaks at the source; floor about 23 dB down |
| Phaser GUI | browser front end served by the Pi | port 8080 at the kit's fixed address, such as `http://192.168.7.13:8080` |
::::

::::{frame} Where This Is Going
:::{present}
**Lesson 18** derives the steering phase from path length:

$$\Delta\phi = kd\sin\theta_0$$

- **Lesson 19** steers the real beam at this station and measures where it points.
- In **Lesson 28** the two digital channels limit MVDR to about one null.
:::

We now have a machine that can put an arbitrary phase on each of eight
elements, and we have not yet told it what phase to use. Lesson 18 supplies the
missing piece with a path-length argument: a wave arriving at angle $\theta_0$
reaches consecutive elements $d\sin\theta_0$ apart in distance, and the phase
ramp that compensates that delay is

$$ \Delta\phi = kd\sin\theta_0. $$

That expression turns a steering angle into the eight numbers `ADAR_set_Phase`
writes. Lesson 19 brings you back to this station to steer the real beam with
them and measure where it points.

:::{depth}
Before Lesson 18, review the array factor from Lesson 16 and be ready to state
what $\psi$ is and why the pattern peaks when it is zero. Keep the block
diagram from Part 3 of today's packet somewhere you can find it; the same figure comes back
in Lesson 28, where the two digital channels limit MVDR adaptive nulling to
about one null.
:::
::::
