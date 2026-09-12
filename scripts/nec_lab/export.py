"""Serializers. The pattern CSV is the one that matters.

`usafa-chamber`'s importer (frontend/src/reference.js) reads any CSV with an
angle column and a dB column, matching header names exactly first and by
substring second. The columns written here -- param, angle_deg, freq_hz,
gain_dbi -- hit its exact-match pass, so a file from this tool drops onto a
measured cut with no editing: the param column becomes the trace label and the
frequency column groups the cuts.

One thing the file cannot carry: a simulated pattern is absolute gain in dBi
and a chamber cut is raw S21 in dB through cables and fixture. The chamber's
compare() normalizes both to their own peak before differencing, which is the
only honest way to put them on one axis. Anything that reads these files and
does not normalize is comparing two different quantities.
"""

from __future__ import annotations

import csv
import io
import json
import math
from dataclasses import asdict, is_dataclass

from .engine import Cut, Solution, Surface, SweepPoint
from .reference import HALF_WAVE


def pattern_csv(cuts: list[Cut], provenance: str = "") -> str:
    """Long-format pattern CSV, one row per angle per cut."""
    buf = io.StringIO()
    if provenance:
        for line in provenance.strip().splitlines():
            buf.write(f"# {line}\n")
    w = csv.writer(buf, lineterminator="\n")
    w.writerow(["param", "angle_deg", "freq_hz", "gain_dbi",
                "theta_deg", "phi_deg"])
    for cut in cuts:
        for i, ang in enumerate(cut.angle_deg):
            w.writerow([cut.name, f"{ang:.4f}", f"{cut.freq_hz:.0f}",
                        f"{cut.gain_dbi[i]:.4f}",
                        f"{cut.theta_deg[i]:.4f}" if cut.theta_deg else "",
                        f"{cut.phi_deg[i]:.4f}" if cut.phi_deg else ""])
    return buf.getvalue()


def sphere_csv(surface: Surface, provenance: str = "") -> str:
    """The whole sphere, one row per direction.

    Deliberately its own file rather than more rows in the cut export: the
    chamber importer keys on a single angle column, and a sphere has two. This
    is for a 3D plot, a solid-angle integration, or a student's own analysis.
    """
    buf = io.StringIO()
    if provenance:
        for line in provenance.strip().splitlines():
            buf.write(f"# {line}\n")
    w = csv.writer(buf, lineterminator="\n")
    w.writerow(["theta_deg", "phi_deg", "freq_hz", "gain_dbi"])
    for i, theta in enumerate(surface.theta_deg):
        for j, phi in enumerate(surface.phi_deg):
            w.writerow([f"{theta:.3f}", f"{phi:.3f}", f"{surface.freq_hz:.0f}",
                        f"{surface.gain_dbi[i][j]:.4f}"])
    return buf.getvalue()


def sweep_csv(points: list[SweepPoint], z0: float = 50.0,
              provenance: str = "") -> str:
    """Impedance sweep, with the two derived numbers a VNA would show."""
    buf = io.StringIO()
    if provenance:
        for line in provenance.strip().splitlines():
            buf.write(f"# {line}\n")
    w = csv.writer(buf, lineterminator="\n")
    w.writerow(["freq_hz", "r_ohm", "x_ohm", "s11_db", "vswr"])
    for p in points:
        z = complex(p.z_real, p.z_imag)
        g = abs((z - z0) / (z + z0))
        s11 = 20 * math.log10(g) if g > 0 else -999.0
        vswr = (1 + g) / (1 - g) if g < 1 else float("inf")
        w.writerow([f"{p.freq_hz:.0f}", f"{p.z_real:.4f}", f"{p.z_imag:.4f}",
                    f"{s11:.3f}", f"{vswr:.4f}"])
    return buf.getvalue()


def _plain(obj):
    if is_dataclass(obj):
        return {k: _plain(v) for k, v in asdict(obj).items()}
    if isinstance(obj, dict):
        return {k: _plain(v) for k, v in obj.items()}
    if isinstance(obj, (list, tuple)):
        return [_plain(v) for v in obj]
    if isinstance(obj, complex):
        return {"real": obj.real, "imag": obj.imag}
    return obj


def to_json(payload) -> str:
    return json.dumps(_plain(payload), indent=2)


def comparison_table(sol: Solution, trim: dict | None = None) -> str:
    """The Part 5 comparison table, with the simulated column filled in.

    The analytical column is Lesson 7's, and the 'why' column is left empty on
    purpose: accounting for each difference is the deliverable, and a tool that
    writes that paragraph has taken the lab away from the student.
    """
    cut = next((c for c in sol.cuts if c.axis == "theta"), None)
    # Gain, beamwidth and the energy audit belong to the trimmed antenna when
    # there is one: L8 takes its pattern cuts "at the resonant length", and a
    # table mixing the trimmed length with the untrimmed pattern would be
    # quoting two different antennas in the same column.
    hpbw = (trim or {}).get("hpbw_deg") or (cut.hpbw_deg() if cut else None)
    gain = (trim or {}).get("gain_dbi") or (cut.peak_dbi if cut else None)
    avg = (trim or {}).get("average_power_gain")
    if avg is None:
        avg = sol.average_power_gain
    rows = [
        ("$Z_{in}$ at the modeled length", f"{HALF_WAVE['z_in'].real:.1f} + j{HALF_WAVE['z_in'].imag:.1f} ohm",
         f"{sol.z_real:.1f} {'+' if sol.z_imag >= 0 else '-'} j{abs(sol.z_imag):.1f} ohm"),
        ("Resonant length", "0.47-0.48 lambda",
         f"{trim['resonant_length_lambda']:.4f} lambda" if trim and trim.get("resonant_length_lambda") else "-"),
        ("$R_{in}$ at resonance", "~70 ohm",
         f"{trim['r_at_resonance']:.1f} ohm" if trim and trim.get("r_at_resonance") else "-"),
        ("Gain", f"{HALF_WAVE['gain_dbi']:.2f} dBi",
         f"{gain:.2f} dBi" if gain is not None else "-"),
        ("E-plane HPBW", f"{HALF_WAVE['hpbw_deg']:.0f} deg",
         f"{hpbw:.1f} deg" if hpbw else "-"),
        ("Average power gain", "1.000",
         f"{avg:.4f}" if avg is not None else "-"),
    ]
    out = ["| Quantity | L7 analytical | Simulated | Difference | Why |",
           "| :-- | :-- | :-- | :-- | :-- |"]
    out += [f"| {q} | {a} | {s} | | |" for q, a, s in rows]
    return "\n".join(out) + "\n"
