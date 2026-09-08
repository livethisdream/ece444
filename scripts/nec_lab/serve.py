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
import os
import socket
import threading
import webbrowser
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

from . import cards, export, study
from .engine import EngineError
from .model import E_PLANE, H_PLANE, Model, SPHERE_AVG, Sweep, wavelength
from .reference import HALF_WAVE

STATIC = Path(__file__).parent / "static"
_TYPES = {".html": "text/html; charset=utf-8", ".js": "text/javascript",
          ".css": "text/css", ".svg": "image/svg+xml", ".ico": "image/x-icon"}


class DeckError(ValueError):
    """The typed deck could not be read. Carries the per-line detail."""

    def __init__(self, parsed: "cards.ParsedDeck"):
        self.parsed = parsed
        super().__init__("; ".join(e.message for e in parsed.errors))


def _model(req: dict) -> Model:
    """Build the model from a request body: typed cards, or the form fields."""
    if req.get("deck"):
        parsed = cards.parse(req["deck"])
        if not parsed.ok:
            raise DeckError(parsed)
        return parsed.model
    freq = float(req.get("freq_mhz", 915.0))
    lam = wavelength(freq)
    if req.get("length_mm") is not None:
        length = float(req["length_mm"]) / 1000.0
    else:
        length = float(req.get("length_lambda", 0.5)) * lam
    return Model.dipole(freq, length,
                        radius_m=float(req.get("radius_mm", 0.5)) / 1000.0,
                        segments=int(req.get("segments", 21)))


def _geometry(model: Model) -> list[dict]:
    """The wires, for the page to draw. A picture catches the mistakes a
    column of coordinates hides -- a wire built along x when the pattern cut
    assumes z, or a feed that is not where the student thinks it is."""
    out = []
    for w in model.wires:
        fed = w.tag == model.feed.tag
        seg = model.feed.segment
        # Where the fed segment sits along the wire, as a fraction each end.
        t0 = (seg - 1) / w.segments if fed else 0.0
        t1 = seg / w.segments if fed else 0.0
        out.append({
            "tag": w.tag, "segments": w.segments, "radius": w.radius,
            "a": [w.x1, w.y1, w.z1], "b": [w.x2, w.y2, w.z2],
            "fed": fed,
            "feed_a": [w.x1 + (w.x2 - w.x1) * t0, w.y1 + (w.y2 - w.y1) * t0,
                       w.z1 + (w.z2 - w.z1) * t0] if fed else None,
            "feed_b": [w.x1 + (w.x2 - w.x1) * t1, w.y1 + (w.y2 - w.y1) * t1,
                       w.z1 + (w.z2 - w.z1) * t1] if fed else None,
        })
    return out


def _gloss_json(parsed: "cards.ParsedDeck") -> list[dict]:
    return [{"line_no": g.line_no, "text": g.text, "card": g.card, "ok": g.ok,
             "summary": g.summary,
             "tokens": [{"text": t.text, "label": t.label, "detail": t.detail}
                        for t in g.tokens]}
            for g in parsed.gloss]


def _form_for(model: Model) -> dict | None:
    """The form fields that would reproduce this model, when they can.

    A typed deck may be a Yagi, or a dipole off the origin, or fed off center.
    The four form fields cannot express any of those, so rather than showing
    numbers that no longer drive anything, the page is told to say the model
    came from the cards.
    """
    if len(model.wires) != 1:
        return None
    w = model.wires[0]
    if model.feed.tag != w.tag or model.feed.segment != w.center_segment:
        return None
    along_z = (abs(w.x1) < 1e-12 and abs(w.x2) < 1e-12
               and abs(w.y1) < 1e-12 and abs(w.y2) < 1e-12
               and abs(w.z1 + w.z2) < 1e-12)
    if not along_z:
        return None
    return {"freq_mhz": model.freq_mhz, "length_mm": w.length * 1000,
            "radius_mm": w.radius * 1000, "segments": w.segments}


def _cut_json(cut) -> dict:
    return {
        "name": cut.name, "axis": cut.axis, "freq_hz": cut.freq_hz,
        "angle_deg": cut.angle_deg, "gain_dbi": cut.gain_dbi,
        "peak_dbi": cut.peak_dbi, "peak_angle_deg": cut.peak_angle_deg,
        "hpbw_deg": cut.hpbw_deg(),
    }


def _requests_for(req: dict):
    """The pattern requests: the deck's own RP cards, or the standard pair."""
    if req.get("deck"):
        parsed = cards.parse(req["deck"])
        if not parsed.ok:
            raise DeckError(parsed)
        return parsed.requests
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

    def deck(self, req: dict) -> dict:
        """Read a typed deck without running it: glosses and complaints."""
        parsed = cards.parse(req.get("deck", ""))
        return {
            "ok": parsed.ok,
            "gloss": _gloss_json(parsed),
            "errors": [{"line_no": e.line_no, "text": e.text,
                        "message": e.message, "hint": e.hint}
                       for e in parsed.errors],
            "geometry": _geometry(parsed.model) if parsed.model else [],
            "form": _form_for(parsed.model) if parsed.model else None,
            "cuts": [r.name for r in parsed.requests],
        }

    def solve(self, req: dict) -> dict:
        model = _model(req)
        sol = self.engine.solve(model, _requests_for(req))
        z = sol.z_in
        g = abs((z - 50) / (z + 50))
        deck_text = req.get("deck") or model.deck(requests=_requests_for(req))
        return {
            "ok": True,
            "engine": self.engine.describe(),
            "deck": deck_text,
            "gloss": _gloss_json(cards.parse(deck_text)),
            "geometry": _geometry(model),
            "form": _form_for(model),
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
        out = study.trim_to_resonance(self.engine, model)
        if out.get("resonant_length_m"):
            # Hand back the trimmed deck as well: when the student is working
            # in the cards, trimming should visibly rewrite the GW card rather
            # than move a form field they are not looking at.
            trimmed = model.with_length(out["resonant_length_m"])
            out["deck"] = trimmed.deck(requests=_requests_for(req))
            out["geometry"] = _geometry(trimmed)
            out["form"] = _form_for(trimmed)
        return out

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
                  "deck": api.deck,
                  "converge": api.converge, "export/pattern": api.export_pattern,
                  "export/sweep": api.export_sweep}.get(name)
            if fn is None:
                return self._send(404, b'{"error":"no such endpoint"}',
                                  "application/json")
            try:
                n = int(self.headers.get("Content-Length", 0))
                req = json.loads(self.rfile.read(n) or b"{}")
                body = json.dumps(fn(req)).encode()
            except DeckError as exc:
                # Not a server failure: the student typed a card wrong, and the
                # page wants the per-line detail to show against the deck.
                body = json.dumps({
                    "ok": False, "error": "the deck has errors",
                    "gloss": _gloss_json(exc.parsed),
                    "errors": [{"line_no": e.line_no, "text": e.text,
                                "message": e.message, "hint": e.hint}
                               for e in exc.parsed.errors]}).encode()
                return self._send(200, body, "application/json")
            except EngineError as exc:
                return self._send(500, json.dumps({"error": str(exc)}).encode(),
                                  "application/json")
            except Exception as exc:  # a bad number in a form field, usually
                return self._send(400, json.dumps({"error": f"{type(exc).__name__}: {exc}"}).encode(),
                                  "application/json")
            self._send(200, body, "application/json")

    return Handler


def _in_container() -> bool:
    """Are we inside a container? Then our own addresses are not the ones to
    hand out -- students reach the host, on whatever port it published."""
    if Path("/.dockerenv").exists():
        return True
    try:
        return "docker" in Path("/proc/1/cgroup").read_text()
    except OSError:
        return False


def _reachable_urls(host: str, port: int) -> list[str]:
    """The addresses a browser can actually be pointed at.

    Binding 0.0.0.0 means "every interface", which is not something anyone can
    type. When the service is shared with a room -- the container does exactly
    this -- the banner has to name the addresses students should use, or the
    first five minutes of the lab are spent finding them.
    """
    if host not in ("0.0.0.0", "::", ""):
        return [f"http://{host}:{port}/"]
    addrs: list[str] = []
    try:
        _, _, ips = socket.gethostbyname_ex(socket.gethostname())
        addrs += [ip for ip in ips if not ip.startswith("127.")]
    except OSError:
        pass
    if not addrs:
        # No name resolution (common in a container): ask the routing table
        # which address it would use to reach the outside world. Nothing is
        # sent -- a UDP socket connect just picks the interface.
        try:
            probe = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            probe.connect(("8.8.8.8", 9))    # nothing is sent; this only
                                             # asks which interface would be used
            addrs.append(probe.getsockname()[0])
            probe.close()
        except OSError:
            pass
    return [f"http://{a}:{port}/" for a in dict.fromkeys(addrs)] \
        + [f"http://127.0.0.1:{port}/"]


def serve(host: str = "127.0.0.1", port: int = 8444, engine=None,
          open_browser: bool = True, public_url: str | None = None) -> None:
    from .engine import pick_engine

    engine = engine or pick_engine()
    httpd = ThreadingHTTPServer((host, port), make_handler(Api(engine)))
    public_url = public_url or os.environ.get("NEC_LAB_PUBLIC_URL") or None
    urls = _reachable_urls(host, port)
    print(f"nec_lab -- {engine.describe()}")
    if public_url:
        # A container, or a box behind a name: the address students type is not
        # one this process can discover, so whoever deployed it says what it is.
        print(f"hand out {public_url}   (ctrl-c to stop)")
    elif len(urls) == 1:
        print(f"open {urls[0]}   (ctrl-c to stop)")
    else:
        print("open one of these   (ctrl-c to stop):")
        for u in urls:
            print(f"    {u}")
        print("shared mode: students on the same network use the address above "
              "that matches this machine")
    if _in_container() and not public_url:
        print("note: this is a container -- the addresses above are the "
              "container's own.\n      Students need the host's address and "
              "the port it published. Set\n      NEC_LAB_PUBLIC_URL to have "
              "that printed here instead.")
    if open_browser:
        threading.Timer(0.6, lambda: webbrowser.open(urls[0])).start()
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nstopped")
    finally:
        httpd.server_close()
