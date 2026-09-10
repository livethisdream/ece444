"""The two NEC backends, behind one interface.

Every result in this tool comes from NEC-2 itself. There are two ways to reach
it and the lab needs both:

* **PyNEC** -- the nec2++ kernel in-process, one solve in about ten
  milliseconds. Wheels exist for Linux; on Windows it wants a compiler, so it
  is not the path for a lab PC.
* **A NEC executable** -- `nec2c`, or the `nec2dxs*.exe` that ships inside
  4nec2. The deck goes in as a file, the output file comes back, and we parse
  it. Slower, and the only option on a machine where 4nec2 is already the
  thing that is installed.

Both return the same dataclasses, so nothing above this file knows which one
ran. `pick_engine()` chooses, and both are worth having pointed at the same
model: two independent NEC implementations agreeing on an impedance is a
stronger statement than either one alone. `selftest.py` does exactly that.
"""

from __future__ import annotations

import os
import re
import shutil
import subprocess
import tempfile
from dataclasses import dataclass, field
from pathlib import Path

from .model import Model, PatternRequest, Sweep


@dataclass
class Cut:
    """One pattern cut: gain in dBi against the angle that was swept."""

    name: str
    freq_hz: float
    axis: str                      # 'theta' or 'phi'
    angle_deg: list[float]         # the swept angle
    gain_dbi: list[float]
    theta_deg: list[float] = field(default_factory=list)
    phi_deg: list[float] = field(default_factory=list)

    @property
    def peak_dbi(self) -> float:
        return max(self.gain_dbi)

    @property
    def peak_angle_deg(self) -> float:
        """The angle of the peak, taken as the middle of any tie.

        NEC's output *file* carries gains to two decimals, so an executable
        backend hands back a broad main lobe with several samples reading the
        same maximum -- taking the first of them puts the peak of a symmetric
        dipole pattern at 88 degrees instead of 90. The middle of the tied run
        is the honest reading at that resolution, and it costs nothing on the
        in-process backend, where the tie is a single sample.
        """
        peak = self.peak_dbi
        tied = [i for i, g in enumerate(self.gain_dbi) if g >= peak - 1e-9]
        return self.angle_deg[tied[len(tied) // 2]]

    def hpbw_deg(self) -> float | None:
        """Half-power beamwidth about the peak, by linear interpolation.

        Returns None when the cut never falls 3 dB on one side of the peak,
        which is the honest answer for an H-plane circle rather than a made-up
        360.
        """
        peak = self.peak_dbi
        i = self.gain_dbi.index(peak)

        def edge(step: int) -> float | None:
            j = i
            while 0 <= j + step < len(self.gain_dbi):
                if self.gain_dbi[j + step] <= peak - 3.0:
                    g0, g1 = self.gain_dbi[j], self.gain_dbi[j + step]
                    a0, a1 = self.angle_deg[j], self.angle_deg[j + step]
                    if g0 == g1:
                        return a1
                    t = (peak - 3.0 - g0) / (g1 - g0)
                    return a0 + t * (a1 - a0)
                j += step
            return None

        lo, hi = edge(-1), edge(+1)
        if lo is None or hi is None:
            return None
        return float(abs(hi - lo))


@dataclass
class Surface:
    """Gain over the whole sphere: a grid, not a cut.

    Stored as `gain_dbi[i_theta][i_phi]` with the two angle axes beside it, so
    the page can walk it as a mesh and the CSV can walk it as rows.
    """

    freq_hz: float
    theta_deg: list[float]
    phi_deg: list[float]
    gain_dbi: list[list[float]]

    @property
    def peak_dbi(self) -> float:
        return max(max(row) for row in self.gain_dbi)

    @property
    def peak_direction(self) -> tuple[float, float]:
        best, where = -1e9, (0.0, 0.0)
        for i, row in enumerate(self.gain_dbi):
            for j, g in enumerate(row):
                if g > best:
                    best, where = g, (self.theta_deg[i], self.phi_deg[j])
        return where


@dataclass
class Solution:
    """One frequency, one geometry: impedance, cuts, and the energy audit."""

    engine: str
    deck: str
    freq_hz: float
    z_real: float
    z_imag: float
    current_real: float
    current_imag: float
    cuts: list[Cut] = field(default_factory=list)
    average_power_gain: float | None = None

    @property
    def z_in(self) -> complex:
        return complex(self.z_real, self.z_imag)

    @property
    def vswr(self, z0: float = 50.0) -> float:
        g = abs((self.z_in - z0) / (self.z_in + z0))
        return (1 + g) / (1 - g) if g < 1 else float("inf")


@dataclass
class SweepPoint:
    freq_hz: float
    z_real: float
    z_imag: float


class EngineError(RuntimeError):
    """The solve did not produce a result we can read."""


# ---------------------------------------------------------------- PyNEC ----

class PyNecEngine:
    """nec2++ in-process, through the PyNEC bindings."""

    name = "PyNEC"

    @staticmethod
    def available() -> bool:
        try:
            import PyNEC  # noqa: F401
        except Exception:
            return False
        return True

    def describe(self) -> str:
        return "PyNEC (nec2++ in-process)"

    def _context(self, model: Model):
        import PyNEC

        ctx = PyNEC.nec_context()
        geo = ctx.get_geometry()
        for w in model.wires:
            # The trailing 1, 1 are the taper ratios: no tapering, which is
            # what a uniform GW card means.
            geo.wire(w.tag, w.segments, w.x1, w.y1, w.z1, w.x2, w.y2, w.z2,
                     w.radius, 1.0, 1.0)
        ctx.geometry_complete(0)
        f = model.feed
        ctx.ex_card(0, f.tag, f.segment, 0, f.volts_real, f.volts_imag,
                    0, 0, 0, 0)
        return ctx

    def solve(self, model: Model,
              requests: tuple[PatternRequest, ...] = ()) -> Solution:
        ctx = self._context(model)
        ctx.fr_card(0, 1, model.freq_mhz, 0.0)
        if requests:
            for r in requests:
                ctx.rp_card(0, r.n_theta, r.n_phi, 1, 0, 0,
                            1 if r.average else 0,
                            r.theta_start, r.phi_start, r.d_theta, r.d_phi,
                            0.0, 0.0)
        else:
            ctx.xq_card(0)

        ip = ctx.get_input_parameters(0)
        z = ip.get_impedance()[0]
        i = ip.get_current()[0]
        sol = Solution(
            engine=self.name,
            deck=model.deck(requests=requests),
            freq_hz=float(ip.get_frequency()),
            z_real=float(z.real), z_imag=float(z.imag),
            current_real=float(i.real), current_imag=float(i.imag),
        )
        for n, r in enumerate(requests):
            rp = ctx.get_radiation_pattern(n)
            gains = rp.get_gain()
            thetas = [float(t) for t in rp.get_theta_angles()]
            phis = [float(p) for p in rp.get_phi_angles()]
            if r.average:
                sol.average_power_gain = float(rp.get_average_power_gain())
                continue
            if r.swept_axis == "theta":
                angle, g = thetas, [float(gains[k][0]) for k in range(len(thetas))]
                th, ph = thetas, [phis[0]] * len(thetas)
            else:
                angle, g = phis, [float(gains[0][k]) for k in range(len(phis))]
                th, ph = [thetas[0]] * len(phis), phis
            sol.cuts.append(Cut(r.name, sol.freq_hz, r.swept_axis,
                                [float(a) for a in angle], g, th, ph))
        return sol

    def surface(self, model: Model, request: PatternRequest) -> Surface:
        ctx = self._context(model)
        ctx.fr_card(0, 1, model.freq_mhz, 0.0)
        ctx.rp_card(0, request.n_theta, request.n_phi, 1, 0, 0, 0,
                    request.theta_start, request.phi_start,
                    request.d_theta, request.d_phi, 0.0, 0.0)
        rp = ctx.get_radiation_pattern(0)
        gains = rp.get_gain()
        return Surface(
            freq_hz=float(rp.get_frequency()),
            theta_deg=[float(t) for t in rp.get_theta_angles()],
            phi_deg=[float(p) for p in rp.get_phi_angles()],
            gain_dbi=[[float(g) for g in row] for row in gains],
        )

    def sweep(self, model: Model, sweep: Sweep) -> list[SweepPoint]:
        ctx = self._context(model)
        ctx.fr_card(0, sweep.n, sweep.start_mhz, sweep.step_mhz)
        ctx.xq_card(0)
        out = []
        for k in range(sweep.n):
            ip = ctx.get_input_parameters(k)
            z = ip.get_impedance()[0]
            out.append(SweepPoint(float(ip.get_frequency()),
                                  float(z.real), float(z.imag)))
        return out


# ------------------------------------------------------------ executable ----

# 4nec2 ships its engine as nec2dxs<n>.exe next to the GUI; the free-standing
# translations are nec2c and nec2++. Any of them reads a deck and writes the
# same output file, so any of them can drive this tool.
_EXE_CANDIDATES = ("nec2c", "nec2++", "nec2dxs11", "nec2dxs11k", "nec2dxs",
                   "nec2dxs11.exe", "nec2dxs.exe", "nec2.exe")

_FREQ_RE = re.compile(r"FREQUENCY\s*[:=]\s*([-+0-9.EeDd]+)\s*MHZ", re.I)
_AVG_RE = re.compile(r"AVERAGE POWER GAIN\s*[:=]\s*([-+0-9.EeDd]+)", re.I)


def _f(tok: str) -> float:
    """NEC output is FORTRAN-formatted; a D exponent is still a float."""
    return float(tok.replace("D", "E").replace("d", "e"))


def _is_number(tok: str) -> bool:
    try:
        _f(tok)
    except ValueError:
        return False
    return True


class ExecutableEngine:
    """A NEC executable driven over files -- what a 4nec2 install already has.

    The engine is found in this order: the `NEC_LAB_ENGINE` environment
    variable, then PATH, then the usual 4nec2 install directories on Windows.
    """

    name = "NEC executable"

    def __init__(self, exe: str | None = None):
        self.exe = exe or self.find()

    @staticmethod
    def find() -> str | None:
        env = os.environ.get("NEC_LAB_ENGINE")
        if env and (Path(env).exists() or shutil.which(env)):
            return env
        for cand in _EXE_CANDIDATES:
            found = shutil.which(cand)
            if found:
                return found
        # Where 4nec2 actually lands. A managed machine often cannot write to
        # Program Files, so a per-user install under the profile or LocalAppData
        # is at least as likely as the documented location.
        import os as _os

        roots = [r"C:\4nec2", r"C:\Program Files\4nec2",
                 r"C:\Program Files (x86)\4nec2", r"D:\4nec2"]
        for var in ("USERPROFILE", "LOCALAPPDATA", "APPDATA", "PUBLIC"):
            base = _os.environ.get(var)
            if base:
                roots += [str(Path(base) / "4nec2"),
                          str(Path(base) / "Programs" / "4nec2")]
        for root in roots:
            d = Path(root)
            if not d.is_dir():
                continue
            for cand in (d / "exe", d):
                if cand.is_dir():
                    for exe in sorted(cand.glob("nec2dxs*.exe")):
                        return str(exe)
        return None

    def available(self) -> bool:
        return bool(self.exe)

    def describe(self) -> str:
        return f"NEC executable ({self.exe})"

    # ---- running -------------------------------------------------------

    def _run_deck(self, deck: str) -> str:
        if not self.exe:
            raise EngineError(
                "No NEC executable found. Install nec2c, or point NEC_LAB_ENGINE "
                "at the nec2dxs executable inside your 4nec2 install.")
        with tempfile.TemporaryDirectory(prefix="nec_lab_") as tmp:
            inp = Path(tmp) / "model.nec"
            out = Path(tmp) / "model.out"
            inp.write_text(deck)
            # nec2c takes -i/-o; the 4nec2 engines take the two paths
            # positionally. Try the flags first and fall back, because the
            # wrong form exits without writing an output file rather than
            # complaining.
            for argv in ([self.exe, f"-i{inp}", f"-o{out}"],
                         [self.exe, str(inp), str(out)]):
                try:
                    subprocess.run(argv, capture_output=True, timeout=300,
                                   check=False)
                except (OSError, subprocess.TimeoutExpired) as exc:
                    raise EngineError(f"{self.exe} would not run: {exc}") from exc
                if out.exists() and out.stat().st_size:
                    return out.read_text(errors="replace")
            raise EngineError(f"{self.exe} produced no output file")

    # ---- parsing -------------------------------------------------------

    @staticmethod
    def parse(text: str) -> list[dict]:
        """Split a NEC output file into one dict per frequency.

        Deliberately loose about spacing and column positions: NEC-2's output
        format has drifted between translations, and the parts we need -- the
        input-parameter row, the pattern rows, the average-gain line -- are
        identifiable by shape rather than by offset.
        """
        blocks: list[dict] = []
        cur: dict | None = None
        lines = text.splitlines()
        i = 0
        while i < len(lines):
            line = lines[i]
            m = _FREQ_RE.search(line)
            if m:
                cur = {"freq_hz": _f(m.group(1)) * 1e6, "input": None,
                       "patterns": [], "average_power_gain": None}
                blocks.append(cur)
                i += 1
                continue
            if cur is None:
                i += 1
                continue

            m = _AVG_RE.search(line)
            if m:
                cur["average_power_gain"] = _f(m.group(1))
                i += 1
                continue

            if "ANTENNA INPUT PARAMETERS" in line:
                i += 1
                while i < len(lines):
                    toks = lines[i].split()
                    if len(toks) >= 11 and all(_is_number(t) for t in toks[:11]):
                        cur["input"] = {
                            "tag": int(_f(toks[0])), "segment": int(_f(toks[1])),
                            "v_real": _f(toks[2]), "v_imag": _f(toks[3]),
                            "i_real": _f(toks[4]), "i_imag": _f(toks[5]),
                            "z_real": _f(toks[6]), "z_imag": _f(toks[7]),
                        }
                        break
                    if lines[i].strip() and "CURRENTS" in lines[i]:
                        break
                    i += 1
                i += 1
                continue

            if "RADIATION PATTERNS" in line:
                rows: list[tuple[float, float, float]] = []
                i += 1
                while i < len(lines):
                    s = lines[i]
                    # The average-gain line sits inside the pattern section,
                    # after the rows. Hand it back to the outer loop rather
                    # than swallowing it here.
                    if ("FREQUENCY" in s.upper() or "RADIATION PATTERNS" in s
                            or _AVG_RE.search(s)):
                        break
                    toks = s.split()
                    # theta, phi, vertical dB, horizontal dB, total dB
                    if len(toks) >= 5 and all(_is_number(t) for t in toks[:5]):
                        rows.append((_f(toks[0]), _f(toks[1]), _f(toks[4])))
                    i += 1
                if rows:
                    cur["patterns"].append(rows)
                continue
            i += 1
        return blocks

    # ---- the Engine interface -----------------------------------------

    def solve(self, model: Model,
              requests: tuple[PatternRequest, ...] = ()) -> Solution:
        deck = model.deck(requests=requests)
        blocks = self.parse(self._run_deck(deck))
        if not blocks or not blocks[0]["input"]:
            raise EngineError("NEC ran but the output had no input-parameter row")
        b = blocks[0]
        sol = Solution(
            engine=self.name, deck=deck, freq_hz=b["freq_hz"],
            z_real=b["input"]["z_real"], z_imag=b["input"]["z_imag"],
            current_real=b["input"]["i_real"], current_imag=b["input"]["i_imag"],
            average_power_gain=b["average_power_gain"],
        )
        pattern_requests = [r for r in requests if not r.average]
        for r, rows in zip(pattern_requests, b["patterns"]):
            th = [row[0] for row in rows]
            ph = [row[1] for row in rows]
            g = [row[2] for row in rows]
            angle = th if r.swept_axis == "theta" else ph
            sol.cuts.append(Cut(r.name, sol.freq_hz, r.swept_axis, angle, g, th, ph))
        return sol

    def surface(self, model: Model, request: PatternRequest) -> Surface:
        deck = model.deck(requests=(request,))
        blocks = self.parse(self._run_deck(deck))
        if not blocks or not blocks[0]["patterns"]:
            raise EngineError("NEC ran but wrote no pattern rows")
        rows = blocks[0]["patterns"][0]
        thetas = [request.theta_start + k * request.d_theta
                  for k in range(request.n_theta)]
        phis = [request.phi_start + k * request.d_phi
                for k in range(request.n_phi)]
        # Index by the angles NEC printed rather than by row order: the output
        # file is free to loop theta or phi on the inside, and a guess that is
        # wrong transposes the pattern silently.
        lookup = {(round(t, 3), round(p, 3)): g for t, p, g in rows}
        grid = [[lookup.get((round(t, 3), round(p, 3)), -999.99) for p in phis]
                for t in thetas]
        return Surface(blocks[0]["freq_hz"], thetas, phis, grid)

    def sweep(self, model: Model, sweep: Sweep) -> list[SweepPoint]:
        deck = model.deck(sweep=sweep)
        blocks = self.parse(self._run_deck(deck))
        out = []
        for b in blocks:
            if b["input"]:
                out.append(SweepPoint(b["freq_hz"], b["input"]["z_real"],
                                      b["input"]["z_imag"]))
        if len(out) != sweep.n:
            raise EngineError(
                f"asked for {sweep.n} frequencies, output carried {len(out)}")
        return out


def pick_engine(prefer: str | None = None):
    """The engine to use: PyNEC when it imported, an executable otherwise.

    `prefer` is 'pynec', 'exe', or None. An explicit choice that is not
    available raises rather than falling back silently -- a lab where half the
    room is unknowingly on a different engine is a bad afternoon.
    """
    if prefer == "pynec":
        if not PyNecEngine.available():
            raise EngineError("PyNEC is not installed in this environment")
        return PyNecEngine()
    if prefer == "exe":
        eng = ExecutableEngine()
        if not eng.available():
            raise EngineError("No NEC executable found (see NEC_LAB_ENGINE)")
        return eng
    if PyNecEngine.available():
        return PyNecEngine()
    eng = ExecutableEngine()
    if eng.available():
        return eng
    raise EngineError(
        "No NEC engine available. Either `pip install PyNEC` (Linux/macOS), or "
        "install nec2c, or set NEC_LAB_ENGINE to the nec2dxs executable in your "
        "4nec2 install.")
