"""The tool's API, with no transport under it.

Every endpoint the page can call lives here as a plain method taking a dict and
returning a dict. `serve.py` wraps it in an HTTP server for the local tool; the
static build calls the same methods directly from the page through Pyodide.

One implementation, two hosts. The alternative -- a second copy of this logic
in JavaScript for the browser build -- would be a second set of physics-adjacent
decisions that the selftest cannot see.
"""

from __future__ import annotations

import math

from . import builders, cards, export, study
from .model import (E_PLANE, H_PLANE, Model, SPHERE_AVG, Sweep,
                    audit_request, cuts_for, sphere_request, wavelength)
from .reference import HALF_WAVE


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


def _front_to_back(surf) -> float | None:
    """Peak gain minus the gain in the opposite direction.

    The number a Yagi is judged by, and one a cut cannot give you unless the
    cut happens to contain both directions. On the sphere it is always there.
    """
    theta, phi = surf.peak_direction
    back_theta, back_phi = 180.0 - theta, (phi + 180.0) % 360.0
    try:
        i = min(range(len(surf.theta_deg)),
                key=lambda k: abs(surf.theta_deg[k] - back_theta))
        j = min(range(len(surf.phi_deg)),
                key=lambda k: abs(surf.phi_deg[k] - back_phi))
    except ValueError:
        return None
    back = surf.gain_dbi[i][j]
    if back < -100:            # a true null behind: report the floor, not -1000
        return None
    return surf.peak_dbi - back


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
        # Both angles per sample: the page plots a cut by the direction each
        # sample points in, not by the number on the swept axis, which is the
        # only way two cuts in different planes can agree about where the beam
        # is.
        "theta_deg": cut.theta_deg, "phi_deg": cut.phi_deg,
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
    grounded = _model(req).ground.present
    out = list(cuts_for(grounded))
    # The average power gain is a conservation check against a whole sphere in
    # free space. Over ground half the sphere is not there, and the number
    # stops meaning what the lab says it means, so it is not requested.
    if req.get("average", True) and not grounded:
        out.append(audit_request(_model(req)))
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

    # The routing table lives here, not in the HTTP layer, so the page behaves
    # identically whether the call crossed a socket or not -- including what a
    # bad deck looks like coming back.
    ROUTES = ("solve", "sweep", "trim", "converge", "deck", "sphere",
              "types", "build", "export/pattern", "export/sphere",
              "export/sweep")

    def dispatch(self, path: str, req: dict) -> dict:
        fn = {
            "solve": self.solve, "sweep": self.sweep, "trim": self.trim,
            "converge": self.converge, "deck": self.deck, "sphere": self.sphere,
            "types": self.types, "build": self.build,
            "export/pattern": self.export_pattern,
            "export/sphere": self.export_sphere,
            "export/sweep": self.export_sweep,
        }.get(path)
        if fn is None:
            return {"ok": False, "error": f"no such endpoint: {path}"}
        try:
            return fn(req or {})
        except DeckError as exc:
            # Not a failure of the tool: the student typed a card wrong, and
            # the page wants the per-line detail to show against the deck.
            return {
                "ok": False, "error": "the deck has errors",
                "gloss": _gloss_json(exc.parsed),
                "errors": [{"line_no": e.line_no, "text": e.text,
                            "message": e.message, "hint": e.hint}
                           for e in exc.parsed.errors],
            }

    def types(self, req: dict) -> dict:
        """The antenna catalog, for the page to render a form from."""
        return {"types": builders.spec()}

    def build(self, req: dict) -> dict:
        """Turn a type and its parameters into cards.

        The deck is the output. Everything downstream -- solving, the studies,
        the 3D view -- goes through the same path a typed deck does, so the
        builder cannot drift from what the cards say.
        """
        kind = req.get("type", "dipole")
        try:
            model = builders.build(kind, req.get("params", {}))
        except KeyError as exc:
            return {"ok": False, "error": str(exc)}
        requests = cuts_for(model.ground.present)
        if not model.ground.present:
            requests = requests + (audit_request(model),)
        return {"ok": True, "type": kind,
                "deck": model.deck(requests=requests),
                "geometry": _geometry(model),
                "ground": model.ground.kind}

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
            "feeds": sol.feeds,
            "ground": model.ground.kind,
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

    def sphere(self, req: dict) -> dict:
        """Gain over the whole sphere, for the 3D view."""
        model = _model(req)
        step = float(req.get("step_deg", 5.0))
        step = min(max(step, 1.0), 15.0)
        grounded = model.ground.present
        request = sphere_request(step, hemisphere=grounded)
        surf = self.engine.surface(model, request)
        theta, phi = surf.peak_direction
        return {
            "ok": True,
            "freq_hz": surf.freq_hz,
            "step_deg": step,
            "theta_deg": surf.theta_deg,
            "phi_deg": surf.phi_deg,
            "gain_dbi": surf.gain_dbi,
            "peak_dbi": surf.peak_dbi,
            "peak_theta_deg": theta,
            "peak_phi_deg": phi,
            "geometry": _geometry(model),
            "ground": model.ground.kind,
            "front_back_db": _front_to_back(surf),
            "deck": model.deck(requests=(request,)),
        }

    def export_sphere(self, req: dict) -> dict:
        model = _model(req)
        step = min(max(float(req.get("step_deg", 5.0)), 1.0), 15.0)
        surf = self.engine.surface(model, sphere_request(step))
        prov = (f"ECE 444 nec_lab -- {self.engine.describe()}\n"
                + model.deck().strip().replace("\n", " | "))
        return {"filename": f"nec_lab_sphere_{model.freq_mhz:.0f}MHz.csv",
                "text": export.sphere_csv(surf, provenance=prov)}

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
