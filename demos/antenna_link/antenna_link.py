#!/usr/bin/env python3
"""
Antenna Tx/Rx Link Demo - Browser-based GUI
============================================

A single ADALM-PLUTO transmits a CW tone out one antenna and receives it on a
second antenna. As a student rotates (or cross-polarizes) the Rx antenna, the
received power changes -- demonstrating antenna pattern and polarization loss.

This is the single-Pluto, single-Rx-channel cousin of pluto_beamformer.py.
It reuses that project's architecture: a hardware class (PlutoLink) plus a
server (LinkServer) that serves a static frontend over HTTP and streams live
power measurements over a WebSocket.

Two views in the browser:
  1. Live Power   - a big dBFS readout + rolling strip chart. Watch the number
                    drop as the Rx antenna is rotated away from co-pol.
  2. Pattern      - type the current Rx angle, hit Record, and build up a polar
                    pattern with a cos^2(theta) theory overlay (the polarization
                    loss factor). Feeds the midterm Antenna Pattern Measurement.

Run with real hardware:
    python antenna_link.py --pluto-uri ip:192.168.2.1

Run with no Pluto attached (synthetic power, for rehearsal / UI testing):
    python antenna_link.py --sim

Physical setup (2.4 GHz, lambda ~ 12.5 cm):
  * Tx SMA -> fixed antenna (say, vertical polarization).
  * Rx SMA -> the antenna the student rotates.
  * Separate the two antennas ~30-50 cm (a few wavelengths) so it is the real
    over-the-air path, not near-field coupling.
  * Tune Tx/Rx gain (sliders) so the co-pol level sits around -15 dBFS -- enough
    headroom that it does not clip, enough signal that the null is visible.

Based on Jon Kraft's Pluto examples: https://github.com/jonkraft/Pluto_Beamformer
"""

import argparse
import asyncio
import json
import math
import signal
import sys
import threading
import webbrowser
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

import numpy as np

try:
    import websockets
    HAS_WEBSOCKETS = True
except ImportError:
    HAS_WEBSOCKETS = False
    print("WebSocket support required. Install: pip install websockets")
    sys.exit(1)

try:
    import adi
    HAS_ADI = True
except ImportError:
    HAS_ADI = False
    print("[link] pyadi-iio not available - hardware disabled (use --sim)")


class PlutoLink:
    """Single-Pluto Tx tone / Rx power meter.

    One Tx channel radiates a CW tone at ``fc0`` above the LO; one Rx channel
    receives it. We report the power in the tone bin, in dBFS, plus its level
    relative to a marked co-pol reference.
    """

    def __init__(self, uri="ip:192.168.2.1", sim=False):
        self.uri = uri
        self.sim = sim
        self.sdr = None
        self.connected = False

        # --- RF parameters ---
        self.sample_rate = 2e6          # Hz
        self.num_samples = 2 ** 12      # Rx buffer / FFT length
        self.center_freq = 2.4e9        # Hz (Tx LO == Rx LO)
        self.rx_gain = 30               # dB, manual
        self.tx_gain = -20              # dB attenuation (0 = max power, -88 = min)
        self.fc0 = int(100e3)           # tone offset from LO, Hz

        # --- Measurement state ---
        self.ref_dbfs = None            # co-pol reference level (dBFS)
        self.pattern = []               # list of {angle, rel_db, abs_dbfs}

        # --- Simulation state ---
        self._sim_angle = 0.0           # deg; drives synthetic power in sim mode
        self._sim_copol_dbfs = -14.0    # synthetic co-pol level
        self._sim_floor_dbfs = -48.0    # synthetic cross-pol / noise floor

    # ------------------------------------------------------------------ #
    # Connection / configuration
    # ------------------------------------------------------------------ #
    def connect(self):
        """Connect to the Pluto (or fake it in sim mode) and start the tone."""
        if self.sim:
            self.connected = True
            print("[link] SIM mode - no hardware. Synthetic power enabled.")
            return True

        if not HAS_ADI:
            raise RuntimeError("pyadi-iio not installed (run with --sim instead)")

        try:
            print(f"[link] Connecting to Pluto at {self.uri} ...")
            self.sdr = adi.Pluto(uri=self.uri)

            # Rx
            self.sdr.sample_rate = int(self.sample_rate)
            self.sdr.rx_rf_bandwidth = int(self.sample_rate)
            self.sdr.rx_lo = int(self.center_freq)
            # Manual gain is CRITICAL: with AGC the radio silently compensates
            # and the power will NOT drop when the antenna is rotated.
            self.sdr.gain_control_mode_chan0 = "manual"
            self.sdr.rx_hardwaregain_chan0 = int(self.rx_gain)
            self.sdr.rx_buffer_size = int(self.num_samples)
            self.sdr._rxadc.set_kernel_buffers_count(1)  # avoid stale buffers

            # Tx
            self.sdr.tx_rf_bandwidth = int(self.sample_rate)
            self.sdr.tx_lo = int(self.center_freq)
            self.sdr.tx_cyclic_buffer = True
            self.sdr.tx_hardwaregain_chan0 = int(self.tx_gain)

            self.connected = True
            self._start_tone()

            # Warm up - let the Pluto run its calibrations before we trust data.
            for _ in range(20):
                self.sdr.rx()

            print(f"[link] Connected. Tx tone at {self.center_freq/1e9:.4f} GHz "
                  f"+ {self.fc0/1e3:.0f} kHz.")
            return True

        except Exception as e:
            print(f"[link] Connection failed: {e}")
            self.connected = False
            return False

    def disconnect(self):
        if self.sdr:
            try:
                self.sdr.tx_destroy_buffer()
            except Exception:
                pass
            self.sdr = None
        self.connected = False

    def _start_tone(self):
        """Load the cyclic Tx buffer with a complex CW tone at fc0."""
        if self.sim or not self.sdr:
            return
        fs = int(self.sdr.sample_rate)
        n = 2 ** 16
        ts = 1.0 / float(fs)
        t = np.arange(0, n * ts, ts)
        i = np.cos(2 * np.pi * t * self.fc0) * 2 ** 14
        q = np.sin(2 * np.pi * t * self.fc0) * 2 ** 14
        self.sdr.tx(i + 1j * q)

    def set_center_freq(self, freq_hz):
        self.center_freq = float(freq_hz)
        if self.connected and not self.sim:
            self.sdr.rx_lo = int(self.center_freq)
            self.sdr.tx_lo = int(self.center_freq)

    def set_rx_gain(self, gain_db):
        self.rx_gain = float(gain_db)
        if self.connected and not self.sim:
            self.sdr.rx_hardwaregain_chan0 = int(self.rx_gain)

    def set_tx_gain(self, gain_db):
        self.tx_gain = float(gain_db)
        if self.connected and not self.sim:
            self.sdr.tx_hardwaregain_chan0 = int(self.tx_gain)

    def set_sim_angle(self, angle_deg):
        self._sim_angle = float(angle_deg)

    # ------------------------------------------------------------------ #
    # Measurement
    # ------------------------------------------------------------------ #
    @staticmethod
    def dbfs(raw_data):
        """Convert IQ samples to an FFT magnitude spectrum in dBFS."""
        n = len(raw_data)
        win = np.hamming(n)
        y = raw_data * win
        s_fft = np.fft.fftshift(np.fft.fft(y) / np.sum(win))
        # Pluto is a signed 12-bit ADC -> full scale is 2**11.
        s_dbfs = 20 * np.log10(np.abs(s_fft) / (2 ** 11) + 1e-12)
        return s_dbfs

    def _signal_window(self):
        """Index range of FFT bins around the +fc0 tone."""
        lo = int(self.num_samples * (self.sample_rate / 2 + self.fc0 / 2) / self.sample_rate)
        hi = int(self.num_samples * (self.sample_rate / 2 + self.fc0 * 2) / self.sample_rate)
        return lo, hi

    def measure(self):
        """One power measurement. Returns dict or None if not connected."""
        if not self.connected:
            return None

        if self.sim:
            power = self._sim_power()
            saturated = power > -1.0
        else:
            data = self.sdr.rx()
            spectrum = self.dbfs(data)
            lo, hi = self._signal_window()
            power = float(np.max(spectrum[lo:hi]))
            # ADC clip check on the raw samples (full scale ~ 2047).
            peak_raw = float(max(np.max(np.abs(data.real)), np.max(np.abs(data.imag))))
            saturated = peak_raw > 2000

        rel = (power - self.ref_dbfs) if self.ref_dbfs is not None else None
        return {
            "power_dbfs": round(power, 2),
            "rel_db": round(rel, 2) if rel is not None else None,
            "ref_dbfs": round(self.ref_dbfs, 2) if self.ref_dbfs is not None else None,
            "saturated": bool(saturated),
        }

    def _sim_power(self):
        """Synthetic power: co-pol level attenuated by cos^2(angle), plus noise."""
        theta = math.radians(self._sim_angle)
        plf = math.cos(theta) ** 2                       # polarization loss factor
        sig_lin = 10 ** (self._sim_copol_dbfs / 10) * plf
        floor_lin = 10 ** (self._sim_floor_dbfs / 10)
        power = 10 * math.log10(sig_lin + floor_lin)
        power += float(np.random.randn()) * 0.3          # a little measurement jitter
        return power

    def average_power(self, n=12):
        """Average several measurements (for a stable captured pattern point)."""
        vals = []
        for _ in range(n):
            m = self.measure()
            if m:
                vals.append(m["power_dbfs"])
        if not vals:
            return None
        return float(np.mean(vals))

    # ------------------------------------------------------------------ #
    # Reference & pattern capture
    # ------------------------------------------------------------------ #
    def mark_reference(self):
        """Mark the current level as the 0 dB co-pol reference."""
        avg = self.average_power()
        if avg is None:
            return None
        self.ref_dbfs = avg
        print(f"[link] Co-pol reference set to {avg:.2f} dBFS")
        return avg

    def clear_reference(self):
        self.ref_dbfs = None

    def capture_point(self, angle_deg):
        """Record an averaged power point at the given angle for the pattern."""
        avg = self.average_power()
        if avg is None:
            return None
        rel = (avg - self.ref_dbfs) if self.ref_dbfs is not None else 0.0
        point = {
            "angle": float(angle_deg),
            "abs_dbfs": round(avg, 2),
            "rel_db": round(rel, 2),
        }
        # Replace an existing point at the same angle, else append.
        self.pattern = [p for p in self.pattern if abs(p["angle"] - angle_deg) > 1e-6]
        self.pattern.append(point)
        self.pattern.sort(key=lambda p: p["angle"])
        print(f"[link] Captured {angle_deg:.0f} deg -> {rel:+.2f} dB (rel co-pol)")
        return point

    def delete_point(self, angle_deg):
        """Remove a captured point at the given angle (used by Undo)."""
        self.pattern = [p for p in self.pattern if abs(p["angle"] - angle_deg) > 1e-6]

    def clear_pattern(self):
        self.pattern = []

    def get_config(self):
        return {
            "uri": self.uri,
            "sim": self.sim,
            "connected": self.connected,
            "sample_rate": self.sample_rate,
            "center_freq": self.center_freq,
            "rx_gain": self.rx_gain,
            "tx_gain": self.tx_gain,
            "fc0": self.fc0,
            "ref_dbfs": self.ref_dbfs,
            "sim_angle": self._sim_angle,
            "pattern": self.pattern,
        }


class LinkServer:
    """WebSocket + HTTP server wrapping a PlutoLink."""

    def __init__(self, http_port=8080, ws_port=8765, pluto_uri="ip:192.168.2.1", sim=False):
        self.http_port = http_port
        self.ws_port = ws_port
        self.link = PlutoLink(uri=pluto_uri, sim=sim)

        self.running = False
        self.stream_running = False
        self.ws_clients = set()
        self._loop = None

    # ------------------------------------------------------------------ #
    # Lifecycle
    # ------------------------------------------------------------------ #
    def start(self):
        self.running = True
        http_thread = threading.Thread(target=self._run_http_server, daemon=True)
        http_thread.start()

        url = f"http://localhost:{self.http_port}"
        print(f"[server] HTTP on {self.http_port}, WebSocket on {self.ws_port}")
        print(f"[server] Open {url} in your browser")
        webbrowser.open(url)

        asyncio.run(self._run_ws_server())

    def _run_http_server(self):
        frontend_dir = Path(__file__).parent / "frontend"
        if not frontend_dir.exists():
            print(f"[server] WARNING: frontend not found at {frontend_dir}")
            frontend_dir = Path(__file__).parent
        class Handler(SimpleHTTPRequestHandler):
            # Always revalidate so edits show up on a normal reload (no stale cache).
            def end_headers(self):
                self.send_header("Cache-Control", "no-cache, no-store, must-revalidate")
                self.send_header("Pragma", "no-cache")
                self.send_header("Expires", "0")
                super().end_headers()

            def log_message(self, *args):
                pass  # keep the console focused on link/ws messages

        handler = partial(Handler, directory=str(frontend_dir))
        httpd = ThreadingHTTPServer(("", self.http_port), handler)
        print(f"[http] Serving {frontend_dir}")
        httpd.serve_forever()

    async def _run_ws_server(self):
        self._loop = asyncio.get_event_loop()
        async with websockets.serve(self._handle_ws, "0.0.0.0", self.ws_port):
            print(f"[ws] Ready on port {self.ws_port}")
            await asyncio.Future()  # run forever

    async def _handle_ws(self, websocket):
        self.ws_clients.add(websocket)
        print(f"[ws] Client connected ({len(self.ws_clients)} total)")
        try:
            async for message in websocket:
                response = await self._handle_command(message)
                await websocket.send(json.dumps(response))
        except websockets.exceptions.ConnectionClosed:
            pass
        finally:
            self.ws_clients.discard(websocket)
            print(f"[ws] Client disconnected ({len(self.ws_clients)} total)")

    # ------------------------------------------------------------------ #
    # Commands
    # ------------------------------------------------------------------ #
    async def _handle_command(self, message):
        try:
            payload = json.loads(message)
            cmd = payload.get("cmd", "")
            data = payload.get("data", {})
        except Exception:
            return {"status": "error", "message": "Invalid JSON"}

        if cmd == "ping":
            return {"status": "ok", "message": "pong"}

        if cmd == "get_config":
            return {"status": "ok", "config": self.link.get_config()}

        if cmd == "connect":
            # Hardware connect: leave sim mode and (re)open the radio cleanly.
            uri = data.get("uri")
            if uri:
                self.link.uri = uri
            self._stop_stream()
            self.link.disconnect()
            self.link.sim = False
            if self.link.connect():
                return {"status": "ok", "config": self.link.get_config()}
            return {"status": "error", "message": "Connection failed"}

        if cmd == "start_sim":
            # Enter simulation mode at runtime (no hardware needed).
            self._stop_stream()
            self.link.disconnect()
            self.link.sim = True
            if self.link.connect():
                return {"status": "ok", "config": self.link.get_config()}
            return {"status": "error", "message": "Sim start failed"}

        if cmd == "disconnect":
            self._stop_stream()
            self.link.disconnect()
            return {"status": "ok"}

        if cmd == "set_center_freq":
            self.link.set_center_freq(data.get("freq", 2.4e9))
            return {"status": "ok", "config": self.link.get_config()}

        if cmd == "set_rx_gain":
            self.link.set_rx_gain(data.get("gain", 30))
            return {"status": "ok"}

        if cmd == "set_tx_gain":
            self.link.set_tx_gain(data.get("gain", -20))
            return {"status": "ok"}

        if cmd == "set_sim_angle":
            self.link.set_sim_angle(data.get("angle", 0))
            return {"status": "ok"}

        if cmd == "start":
            self._start_stream()
            return {"status": "ok"}

        if cmd == "stop":
            self._stop_stream()
            return {"status": "ok"}

        if cmd == "mark_reference":
            ref = self.link.mark_reference()
            if ref is None:
                return {"status": "error", "message": "Not connected"}
            return {"status": "ok", "ref_dbfs": round(ref, 2)}

        if cmd == "clear_reference":
            self.link.clear_reference()
            return {"status": "ok"}

        if cmd == "capture_point":
            point = self.link.capture_point(data.get("angle", 0))
            if point is None:
                return {"status": "error", "message": "Not connected"}
            return {"status": "ok", "point": point, "pattern": self.link.pattern}

        if cmd == "delete_point":
            self.link.delete_point(data.get("angle", 0))
            return {"status": "ok", "pattern": self.link.pattern}

        if cmd == "clear_pattern":
            self.link.clear_pattern()
            return {"status": "ok", "pattern": self.link.pattern}

        return {"status": "error", "message": f"Unknown command: {cmd}"}

    # ------------------------------------------------------------------ #
    # Streaming loop
    # ------------------------------------------------------------------ #
    def _start_stream(self):
        if self.stream_running:
            return
        if not self.link.connected:
            self.link.connect()
        self.stream_running = True
        asyncio.create_task(self._stream_loop())
        print("[server] Streaming started")

    def _stop_stream(self):
        self.stream_running = False

    async def _stream_loop(self):
        while self.stream_running:
            try:
                m = self.link.measure()
                if m:
                    msg = json.dumps({"type": "power", "data": m})
                    for ws in list(self.ws_clients):
                        try:
                            await ws.send(msg)
                        except Exception:
                            pass
                await asyncio.sleep(0.05)  # ~20 Hz
            except Exception as e:
                print(f"[server] Stream error: {e}")
                await asyncio.sleep(0.5)


def main():
    parser = argparse.ArgumentParser(description="Antenna Tx/Rx Link Demo")
    parser.add_argument("--port", type=int, default=8080, help="HTTP port")
    parser.add_argument("--ws-port", type=int, default=8765, help="WebSocket port")
    parser.add_argument("--pluto-uri", type=str, default="ip:192.168.2.1",
                        help="Pluto URI (e.g. ip:192.168.2.1)")
    parser.add_argument("--sim", action="store_true",
                        help="Run with synthetic power, no hardware required")
    args = parser.parse_args()

    server = LinkServer(http_port=args.port, ws_port=args.ws_port,
                        pluto_uri=args.pluto_uri, sim=args.sim)

    def sig_handler(sig, frame):
        print("\nShutting down ...")
        server.running = False
        try:
            server.link.disconnect()
        except Exception:
            pass
        sys.exit(0)

    signal.signal(signal.SIGINT, sig_handler)
    server.start()


if __name__ == "__main__":
    main()
