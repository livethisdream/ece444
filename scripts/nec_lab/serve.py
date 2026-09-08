"""A local web front end for the NEC engines.

The design constraint is the lab PC: no npm, no build step, no install beyond
Python. So this is `http.server` from the standard library serving a static
page, and a handful of JSON endpoints that wrap the same functions the CLI
calls. Start it and a browser opens on the tool.

It binds 127.0.0.1 by default and it will not execute a deck it did not
generate: the API takes model parameters, not NEC cards. The deck is shown in
the page so it can be copied into 4nec2, which keeps the cards the interface
the lesson says they are without turning this into a remote-execution service.
"""

from __future__ import annotations

import json
import math
import threading
import webbrowser
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

from . import export, study
from .engine import EngineError
from .model import E_PLANE, H_PLANE, Model, SPHERE_AVG, Sweep, wavelength
from .reference import HALF_WAVE

STATIC = Path(__file__).parent / "static"
_TYPES = {".html": "text/html; charset=utf-8", ".js": "text/javascript",
          ".css": "text/css", ".svg": "image/svg+xml", ".ico": "image/x-icon"}


def _model(req: dict) -> Model:
    """Build the model from a request body, in the units the page uses."""
    freq = float(req.get("freq_mhz", 915.0))
    lam = wavelength(freq)
    if req.get("length_mm") is not None:
        length = float(req["length_mm"]) / 1000.0
    else:
        length = float(req.get("length_lambda", 0.5)) * lam
    return Model.dipole(freq, length,
                        radius_m=float(req.get("radius_mm", 0.5)) / 1000.0,
                        segments=int(req.get("segments", 21)))


def _cut_json(cut) -> dict:
    return {
        "name": cut.name, "axis": cut.axis, "freq_hz": cut.freq_hz,
        "angle_deg": cut.angle_deg, "gain_dbi": cut.gain_dbi,
        "peak_dbi": cut.peak_dbi, "peak_angle_deg": cut.peak_angle_deg,
        "hpbw_deg": cut.hpbw_deg(),
    }


def _requests_for(req: dict):
    names = req.get("cuts") or ["E-plane", "H-plane"]
    out = []
    if "E-plane" in names:
        out.append(E_PLANE)
    if "H-plane" in names:
        out.append(H_PLANE)
    if req.get("average", True):
        out.append(SPHERE_AVG)
    return tuple(out)


class Api:
    """The endpoints, one method each, all returning plain dicts."""

    def __init__(self, engine):
        self.engine = engine

    def engine_info(self, req: dict) -> dict:
        return {"engine": self.engine.describe(),
                "reference": {"z_real": HALF_WAVE["z_in"].real,
                              "z_imag": HALF_WAVE["z_in"].imag,
                              "gain_dbi": HALF_WAVE["gain_dbi"],
                              "hpbw_deg": HALF_WAVE["hpbw_deg"]}}

    def solve(self, req: dict) -> dict:
        model = _model(req)
        sol = self.engine.solve(model, _requests_for(req))
        z = sol.z_in
        g = abs((z - 50) / (z + 50))
        return {
            "engine": self.engine.describe(),
            "deck": model.deck(requests=_requests_for(req)),
            "freq_hz": sol.freq_hz,
            "wavelength_m": model.wavelength,
            "length_m": model.wires[0].length,
            "length_lambda": model.wires[0].length / model.wavelength,
            "segment_length_m": model.wires[0].segment_length,
            "z": {"real": sol.z_real, "imag": sol.z_imag},
            "vswr": (1 + g) / (1 - g) if g < 1 else None,
            "s11_db": 20 * math.log10(g) if g > 0 else None,
            "cuts": [_cut_json(c) for c in sol.cuts],
            "average_power_gain": sol.average_power_gain,
            "rules": model.check(),
        }

    def sweep(self, req: dict) -> dict:
        model = _model(req)
        start = float(req.get("start_mhz", 800.0))
        stop = float(req.get("stop_mhz", 1000.0))
        step = float(req.get("step_mhz", 5.0))
        n = max(2, int(round((stop - start) / step)) + 1)
        res = study.resonant_frequency(self.engine, model, Sweep(start, n, step))
        res["deck"] = model.deck(sweep=Sweep(start, n, step))
        return res

    def trim(self, req: dict) -> dict:
        model = _model(req)
        return study.trim_to_resonance(self.engine, model)

    def converge(self, req: dict) -> dict:
        model = _model(req)
        counts = [int(c) for c in req.get("counts", [11, 21, 41, 81])]
        rows = study.convergence(self.engine, model, counts)
        return {"rows": [r.__dict__ for r in rows]}

    def export_pattern(self, req: dict) -> dict:
        model = _model(req)
        sol = self.engine.solve(model, _requests_for(req))
        prov = (f"ECE 444 nec_lab -- {self.engine.describe()}\n"
                + model.deck().strip().replace("\n", " | "))
        return {"filename": f"nec_lab_pattern_{model.freq_mhz:.0f}MHz.csv",
                "text": export.pattern_csv(sol.cuts, provenance=prov)}

    def export_sweep(self, req: dict) -> dict:
        model = _model(req)
        start = float(req.get("start_mhz", 800.0))
        stop = float(req.get("stop_mhz", 1000.0))
        step = float(req.get("step_mhz", 5.0))
        n = max(2, int(round((stop - start) / step)) + 1)
        pts = self.engine.sweep(model, Sweep(start, n, step))
        prov = f"ECE 444 nec_lab -- {self.engine.describe()}"
        return {"filename": f"nec_lab_sweep_{start:.0f}_{stop:.0f}MHz.csv",
                "text": export.sweep_csv(pts, provenance=prov)}


def make_handler(api: Api):
    class Handler(BaseHTTPRequestHandler):
        server_version = "nec_lab"

        def log_message(self, fmt, *args):   # quiet: the page is the interface
            pass

        def _send(self, code: int, body: bytes, ctype: str):
            self.send_response(code)
            self.send_header("Content-Type", ctype)
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)

        def do_GET(self):
            path = self.path.split("?")[0]
            if path == "/":
                path = "/index.html"
            if path == "/api/engine":
                return self._send(200, json.dumps(api.engine_info({})).encode(),
                                  "application/json")
            target = (STATIC / path.lstrip("/")).resolve()
            if not str(target).startswith(str(STATIC.resolve())) or not target.is_file():
                return self._send(404, b"not found", "text/plain")
            self._send(200, target.read_bytes(),
                       _TYPES.get(target.suffix, "application/octet-stream"))

        def do_POST(self):
            name = self.path.split("?")[0].removeprefix("/api/")
            fn = {"solve": api.solve, "sweep": api.sweep, "trim": api.trim,
                  "converge": api.converge, "export/pattern": api.export_pattern,
                  "export/sweep": api.export_sweep}.get(name)
            if fn is None:
                return self._send(404, b'{"error":"no such endpoint"}',
                                  "application/json")
            try:
                n = int(self.headers.get("Content-Length", 0))
                req = json.loads(self.rfile.read(n) or b"{}")
                body = json.dumps(fn(req)).encode()
            except EngineError as exc:
                return self._send(500, json.dumps({"error": str(exc)}).encode(),
                                  "application/json")
            except Exception as exc:  # a bad number in a form field, usually
                return self._send(400, json.dumps({"error": f"{type(exc).__name__}: {exc}"}).encode(),
                                  "application/json")
            self._send(200, body, "application/json")

    return Handler


def serve(host: str = "127.0.0.1", port: int = 8444, engine=None,
          open_browser: bool = True) -> None:
    from .engine import pick_engine

    engine = engine or pick_engine()
    httpd = ThreadingHTTPServer((host, port), make_handler(Api(engine)))
    url = f"http://{host}:{port}/"
    print(f"nec_lab -- {engine.describe()}")
    print(f"open {url}   (ctrl-c to stop)")
    if open_browser:
        threading.Timer(0.6, lambda: webbrowser.open(url)).start()
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nstopped")
    finally:
        httpd.server_close()
