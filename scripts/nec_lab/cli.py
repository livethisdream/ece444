"""Command line for the L8 lab: solve, sweep, trim, converge, export.

Everything the GUI does, without the GUI -- so the lab still runs from a
terminal, a batch file, or a marking script, and so a student can see the deck
that produced every number.

    python -m nec_lab solve --length-lambda 0.5 --freq 915
    python -m nec_lab sweep --start 800 --stop 1000 --step 5 --csv sweep.csv
    python -m nec_lab pattern --trim --csv pattern.csv
    python -m nec_lab report --trim
"""

from __future__ import annotations

import argparse
import os
import sys
from pathlib import Path

from . import cards, export, study
from .engine import EngineError, ExecutableEngine, PyNecEngine, pick_engine
from .model import E_PLANE, H_PLANE, SPHERE_AVG, Model, Sweep, wavelength


def _model_from_args(a) -> Model:
    """The model: a deck file when one is given, otherwise the dipole flags."""
    if getattr(a, "deck", None):
        text = Path(a.deck).read_text()
        parsed = cards.parse(text)
        if not parsed.ok:
            for err in parsed.errors:
                where = f"line {err.line_no}" if err.line_no else "the deck"
                print(f"error: {where}: {err.message}", file=sys.stderr)
                if err.hint:
                    print(f"       {err.hint}", file=sys.stderr)
            raise SystemExit(2)
        # A deck that asks for its own cuts gets them; one with no RP card
        # falls back to the standard pair so `solve` still has a pattern to
        # report. Stashed on the namespace so each command can pick it up.
        a._deck_requests = parsed.requests
        return parsed.model
    lam = wavelength(a.freq)
    length = a.length / 1000.0 if a.length else a.length_lambda * lam
    return Model.dipole(a.freq, length, radius_m=a.radius / 1000.0,
                        segments=a.segments)


def _requests(a, default=(E_PLANE, H_PLANE, SPHERE_AVG)):
    return getattr(a, "_deck_requests", ()) or default


def _provenance(engine, model: Model) -> str:
    return (f"ECE 444 nec_lab -- {engine.describe()}\n"
            f"{model.comment}\n"
            + model.deck().strip().replace("\n", " | "))


def _add_model_args(p):
    p.add_argument("--freq", type=float, default=915.0, help="MHz (default 915)")
    p.add_argument("--length", type=float, default=None,
                   help="wire length in mm; overrides --length-lambda")
    p.add_argument("--length-lambda", type=float, default=0.5,
                   help="wire length in wavelengths (default 0.5)")
    p.add_argument("--radius", type=float, default=0.5, help="mm (default 0.5)")
    p.add_argument("--segments", type=int, default=21, help="odd (default 21)")
    p.add_argument("--engine", choices=("auto", "pynec", "exe"), default="auto")
    p.add_argument("--deck", default=None,
                   help="run a NEC deck file instead of the dipole flags above")


def _rules(model: Model) -> str:
    lines = []
    for c in model.check():
        lines.append(f"  [{'ok ' if c['ok'] else 'BAD'}] {c['rule']:38s} {c['detail']}")
    return "\n".join(lines)


def cmd_solve(a, engine) -> int:
    model = _model_from_args(a)
    sol = engine.solve(model, _requests(a))
    cut = sol.cuts[0] if sol.cuts else None
    print(sol.deck)
    print(f"engine            {engine.describe()}")
    print(f"frequency         {sol.freq_hz / 1e6:.4f} MHz")
    print(f"Zin               {sol.z_real:.2f} {'+' if sol.z_imag >= 0 else '-'} "
          f"j{abs(sol.z_imag):.2f} ohm")
    if cut:
        print(f"peak gain         {cut.peak_dbi:.2f} dBi in cut '{cut.name}' "
              f"at {cut.peak_angle_deg:.0f} deg")
        hp = cut.hpbw_deg()
        print(f"HPBW              {hp:.1f} deg" if hp else "HPBW              -")
    if sol.average_power_gain is not None:
        flag = "" if 0.95 <= sol.average_power_gain <= 1.05 else "   <-- MODEL IS BROKEN"
        print(f"avg power gain    {sol.average_power_gain:.4f}{flag}")
    print("segmentation rules:")
    print(_rules(model))
    return 0


def cmd_sweep(a, engine) -> int:
    model = _model_from_args(a)
    n = int(round((a.stop - a.start) / a.step)) + 1
    sw = Sweep(a.start, n, a.step)
    res = study.resonant_frequency(engine, model, sw)
    print(f"{'freq (MHz)':>12}{'R (ohm)':>12}{'X (ohm)':>12}")
    for p in res["sweep"]:
        print(f"{p['freq_hz'] / 1e6:12.3f}{p['z_real']:12.2f}{p['z_imag']:12.2f}")
    if res["resonant_freq_hz"]:
        print(f"\nX crosses zero at {res['resonant_freq_hz'] / 1e6:.3f} MHz, "
              f"R = {res['r_at_resonance']:.2f} ohm")
    else:
        print("\nno reactance zero crossing inside the sweep")
    if a.csv:
        pts = engine.sweep(model, sw)
        Path(a.csv).write_text(export.sweep_csv(pts, provenance=_provenance(engine, model)))
        print(f"wrote {a.csv}")
    return 0


def cmd_pattern(a, engine) -> int:
    model = _model_from_args(a)
    trim = None
    if a.trim:
        trim = study.trim_to_resonance(engine, model)
        if trim.get("resonant_length_lambda"):
            model = model.with_length(trim["resonant_length_m"])
            print(f"trimmed to {trim['resonant_length_lambda']:.4f} lambda "
                  f"({trim['resonant_length_m'] * 1000:.2f} mm), "
                  f"R = {trim['r_at_resonance']:.2f} ohm")
    sol = engine.solve(model, _requests(a))
    for cut in sol.cuts:
        hp = cut.hpbw_deg()
        print(f"{cut.name:10s} peak {cut.peak_dbi:6.2f} dBi   "
              f"HPBW {f'{hp:.1f} deg' if hp else '-- (no 3 dB point)'}   "
              f"{len(cut.angle_deg)} points")
    out = a.csv or "pattern.csv"
    Path(out).write_text(export.pattern_csv(sol.cuts,
                                            provenance=_provenance(engine, model)))
    print(f"wrote {out} -- drop this on a chamber run to overlay it")
    return 0


def cmd_converge(a, engine) -> int:
    model = _model_from_args(a)
    counts = [int(c) for c in a.counts.split(",")]
    print(f"{'N':>5}{'R (ohm)':>11}{'X (ohm)':>11}{'gain':>8}"
          f"{'d/lambda':>11}{'d/a':>8}{'drift':>9}")
    for r in study.convergence(engine, model, counts):
        drift = f"{r.drift_percent:.2f}%" if r.drift_percent is not None else "-"
        flag = "  <- breaks delta > 8a" if r.breaks_8a else ""
        print(f"{r.segments:5d}{r.z_real:11.2f}{r.z_imag:11.2f}{r.gain_dbi:8.2f}"
              f"{r.delta_over_lambda:11.4f}{r.delta_over_radius:8.1f}{drift:>9}{flag}")
    return 0


def cmd_report(a, engine) -> int:
    model = _model_from_args(a)
    trim = study.trim_to_resonance(engine, model) if a.trim else None
    sol = engine.solve(model, _requests(a))
    print(f"# L8 comparison -- {engine.describe()}\n")
    print("```text")
    print(model.deck(requests=(E_PLANE,)).strip())
    print("```\n")
    print(export.comparison_table(sol, trim))
    print("Convergence:\n")
    print(f"| N | R (ohm) | X (ohm) | gain (dBi) | delta/a | drift |")
    print("| :-- | :-- | :-- | :-- | :-- | :-- |")
    for r in study.convergence(engine, model):
        drift = f"{r.drift_percent:.2f}%" if r.drift_percent is not None else "-"
        print(f"| {r.segments} | {r.z_real:.2f} | {r.z_imag:.2f} | "
              f"{r.gain_dbi:.2f} | {r.delta_over_radius:.1f} | {drift} |")
    return 0


def cmd_serve(a, engine) -> int:
    from .serve import serve

    serve(host=a.host, port=a.port, engine=engine, open_browser=not a.no_browser)
    return 0


def cmd_engines(a, engine) -> int:
    print(f"PyNEC            {'available' if PyNecEngine.available() else 'not installed'}")
    exe = ExecutableEngine()
    print(f"NEC executable   {exe.exe or 'not found (set NEC_LAB_ENGINE)'}")
    print(f"in use           {engine.describe()}")
    return 0


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(prog="nec_lab",
                                 description="NEC-2 for the ECE 444 simulation lab")
    sub = ap.add_subparsers(dest="cmd", required=True)

    p = sub.add_parser("solve", help="one frequency: impedance, gain, HPBW, energy audit")
    _add_model_args(p)
    p.set_defaults(func=cmd_solve)

    p = sub.add_parser("sweep", help="impedance against frequency, and resonance")
    _add_model_args(p)
    p.add_argument("--start", type=float, default=800.0)
    p.add_argument("--stop", type=float, default=1000.0)
    p.add_argument("--step", type=float, default=5.0)
    p.add_argument("--csv", default=None)
    p.set_defaults(func=cmd_sweep)

    p = sub.add_parser("pattern", help="E- and H-plane cuts, exported for the chamber")
    _add_model_args(p)
    p.add_argument("--trim", action="store_true", help="trim to resonance first")
    p.add_argument("--csv", default=None)
    p.set_defaults(func=cmd_pattern)

    p = sub.add_parser("converge", help="impedance and gain against segment count")
    _add_model_args(p)
    p.add_argument("--counts", default="11,21,41,81")
    p.set_defaults(func=cmd_converge)

    p = sub.add_parser("report", help="the Part 5 comparison table, simulated column filled")
    _add_model_args(p)
    p.add_argument("--trim", action="store_true", default=True)
    p.set_defaults(func=cmd_report)

    p = sub.add_parser("serve", help="the browser GUI")
    _add_model_args(p)
    p.add_argument("--host", default="127.0.0.1")
    p.add_argument("--port", type=int, default=8444)
    p.add_argument("--no-browser", action="store_true")
    p.set_defaults(func=cmd_serve)

    p = sub.add_parser("engines", help="which NEC backends this machine has")
    _add_model_args(p)
    p.set_defaults(func=cmd_engines)

    a = ap.parse_args(argv)
    try:
        engine = pick_engine(None if a.engine == "auto" else a.engine)
    except EngineError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2
    try:
        return a.func(a, engine)
    except EngineError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1
    except BrokenPipeError:
        # `run.py solve | head` closes the pipe early. That is the shell doing
        # what it was asked, not a failure, and it should not print a
        # traceback at a student mid-lab.
        os.dup2(os.open(os.devnull, os.O_WRONLY), sys.stdout.fileno())
        return 0


if __name__ == "__main__":
    raise SystemExit(main())
