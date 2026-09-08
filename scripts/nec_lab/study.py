"""The four studies the L8 procedure asks for, on top of either engine.

Nothing here knows which NEC is running. Each function takes an engine, a
model, and returns plain data -- which is what lets the CLI print it, the
service serialize it, and the selftest assert on it.
"""

from __future__ import annotations

from dataclasses import dataclass

from .model import E_PLANE, Model, SPHERE_AVG, Sweep, wavelength


@dataclass
class ConvergenceRow:
    segments: int
    z_real: float
    z_imag: float
    gain_dbi: float
    delta_over_lambda: float
    delta_over_radius: float
    drift_ohms: float | None      # |dZ| since the previous (halved) row
    drift_percent: float | None
    breaks_8a: bool


def convergence(engine, model: Model,
                counts=(11, 21, 41, 81)) -> list[ConvergenceRow]:
    """Step 8: re-solve at each segmentation and watch the answer settle.

    The drift column is the point. Convergence means the answer stopped moving
    under refinement, which is a different claim from the answer being right,
    and the lab asks students to say which one they have.
    """
    lam = model.wavelength
    rows: list[ConvergenceRow] = []
    prev: complex | None = None
    for n in counts:
        m = model.with_segments(n)
        sol = engine.solve(m, (E_PLANE,))
        w = m.wires[0]
        d = w.segment_length
        z = sol.z_in
        drift = abs(z - prev) if prev is not None else None
        rows.append(ConvergenceRow(
            segments=n, z_real=z.real, z_imag=z.imag,
            gain_dbi=sol.cuts[0].peak_dbi,
            delta_over_lambda=d / lam, delta_over_radius=d / w.radius,
            drift_ohms=drift,
            drift_percent=(100.0 * drift / abs(z)) if drift is not None else None,
            breaks_8a=d <= 8 * w.radius,
        ))
        prev = z
    return rows


def resonant_frequency(engine, model: Model, sweep: Sweep) -> dict:
    """Step 5: sweep, then find where the reactance crosses zero.

    The sweep is what the student plots; the crossing is refined by bisection
    on the two straddling points, because reading a zero crossing off a 5 MHz
    grid is worth about 2 MHz and the lab compares against a trim.
    """
    points = engine.sweep(model, sweep)
    series = [(p.freq_hz, p.z_real, p.z_imag) for p in points]
    crossing = None
    for (f0, r0, x0), (f1, r1, x1) in zip(series, series[1:]):
        if x0 == 0.0:
            crossing = (f0, r0)
            break
        if x0 * x1 < 0:
            lo, hi = f0 / 1e6, f1 / 1e6
            for _ in range(40):
                mid = 0.5 * (lo + hi)
                x = engine.solve(model.at_frequency(mid)).z_in.imag
                if x * x0 < 0:
                    hi = mid
                else:
                    lo, x0 = mid, x
            f = 0.5 * (lo + hi)
            crossing = (f * 1e6, engine.solve(model.at_frequency(f)).z_in.real)
            break
    return {
        "sweep": [{"freq_hz": f, "z_real": r, "z_imag": x} for f, r, x in series],
        "resonant_freq_hz": crossing[0] if crossing else None,
        "r_at_resonance": crossing[1] if crossing else None,
    }


def trim_to_resonance(engine, model: Model,
                      lo_lambda: float = 0.40, hi_lambda: float = 0.55,
                      tol_lambda: float = 1e-5) -> dict:
    """Step 6: hold the frequency and shorten the wire until X crosses zero.

    Bisection on length. The bracket is wide enough to hold any thin dipole
    and narrow enough to stay on the first resonance -- a wider one can land
    on the 3/2-wave resonance and report a confident wrong answer.
    """
    lam = model.wavelength

    def reactance(frac: float) -> float:
        return engine.solve(model.with_length(frac * lam)).z_in.imag

    x_lo, x_hi = reactance(lo_lambda), reactance(hi_lambda)
    if x_lo * x_hi > 0:
        return {"resonant_length_lambda": None, "r_at_resonance": None,
                "note": "no reactance sign change inside the search bracket"}
    while hi_lambda - lo_lambda > tol_lambda:
        mid = 0.5 * (lo_lambda + hi_lambda)
        x = reactance(mid)
        if x * x_lo <= 0:
            hi_lambda = mid
        else:
            lo_lambda, x_lo = mid, x
    frac = 0.5 * (lo_lambda + hi_lambda)
    sol = engine.solve(model.with_length(frac * lam), (E_PLANE, SPHERE_AVG))
    cut = sol.cuts[0]
    return {
        "resonant_length_lambda": frac,
        "resonant_length_m": frac * lam,
        "r_at_resonance": sol.z_real,
        "x_at_resonance": sol.z_imag,
        "gain_dbi": cut.peak_dbi,
        "hpbw_deg": cut.hpbw_deg(),
        "average_power_gain": sol.average_power_gain,
    }


def energy_audit(engine, model: Model) -> float | None:
    """Step 4: the average power gain over a coarse sphere.

    Anything far from 1.000 in a lossless free-space model means the model is
    broken, not that the antenna is unusual, and no other number in the run is
    worth reading until it is fixed.
    """
    return engine.solve(model, (SPHERE_AVG,)).average_power_gain
