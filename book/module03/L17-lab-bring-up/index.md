---
frame_view: true
---

# L17 Lab — Phased Array Bring-Up

::::{frame}
:class: title-frame

<div class="course-mark">ECE 444 · Fall 2026</div>

<h1 class="frame-title">Phased Array Bring-Up</h1>

<div class="title-rule"></div>

Bring your own kit up from a blank card, then prove it works.

L17 Lab · Antennas, Phased Arrays, and Radar Systems · Dr. Neil Rogers
::::

::::{frame} Learning Objectives

<ol class="lo-list" style="--module: '3'; counter-reset: lo 2">
  <li>I can identify the hardware architecture of the ADALM-PHASER and control it via SDR software.</li>
</ol>

:::{depth}
This lab is the bench half of Lesson 17. The lesson walked the receive chain
block by block; here you bring up that hardware yourself, from a blank card to
a beam sweep that follows the source. The lab packet records both: that the kit
came up, and that it works.
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

::::{frame} Lab Packet
:class: read-only doc-links

The L17 Lab packet is one submission for the whole lab, turned in complete before Lesson 18. It has three parts:

1. **Part 1, Pre-Lab** (individual, before the lab period): the receive chain in order, the phase shifter's step, the element and channel counts, and how a kit number sets the kit's name and address.
2. **Part 2, Measurements** (your own kit's data, recorded in class): the bring-up record from Part A, and the kit check from Part B, the FFT peak and the sweep with the source at boresight, moved, and back.
3. **Part 3, Writeup** (individual, after the lab): a labeled block diagram, two bench diagnoses, and two written answers.

- <a class="doc-link" href="../../labs/ECE444_Lab_L17_Hardware_blank.pdf" target="_blank" rel="noopener">L17 Lab packet (PDF)</a>
::::
