"""Checks that the tool still says what the lesson says.

Two kinds of assertion, and the second is the interesting one:

* **Against Lesson 7 and Lesson 8.** The trimmed resonant length, the
  resistance there, the gain, the HPBW, the energy audit, and the impedance of
  a wire cut to exactly lambda/2 -- every number the L8 handout tells students
  to expect.
* **Against the other engine.** When both PyNEC and a NEC executable are
  present, the same model goes through both. Two independent implementations
  of NEC-2 agreeing to a hundredth of an ohm is the strongest statement this
  repository can make about the numbers it puts in front of a class.

    python -m nec_lab.selftest
"""

from __future__ import annotations

import sys

from . import cards, export, study
from .engine import ExecutableEngine, PyNecEngine
from .model import E_PLANE, H_PLANE, Model, SPHERE_AVG, Sweep, wavelength

FAILURES: list[str] = []


def check(label: str, ok: bool, detail: str = "") -> None:
    print(f"  [{'PASS' if ok else 'FAIL'}] {label}" + (f"   {detail}" if detail else ""))
    if not ok:
        FAILURES.append(label)


def near(a: float, b: float, tol: float) -> bool:
    return abs(a - b) <= tol


# The deck printed in book/module02/L08-dipole-simulation-lab/index.md. If the
# card writer drifts from the handout, the lab and the tool stop agreeing and
# a student typing the handout's cards gets a different answer than the tool.
LESSON_DECK = """CM ECE 444 L8 -- half-wave dipole, 915 MHz
CE
GW 1 21 0 0 -0.08197 0 0 0.08197 0.0005
GE 0
EX 0 1 11 0 1 0
FR 0 1 0 0 915 0
RP 0 181 1 1000 0 0 1 0
EN
"""


def run() -> int:
    print("nec_lab selftest\n")

    print("deck generation")
    model = Model.dipole(915.0, 0.16394, comment="ECE 444 L8 -- half-wave dipole, 915 MHz")
    check("the generated deck is the L8 handout's deck",
          model.deck(requests=(E_PLANE,)) == LESSON_DECK)

    engines = []
    if PyNecEngine.available():
        engines.append(PyNecEngine())
    exe = ExecutableEngine()
    if exe.available():
        engines.append(exe)
    if not engines:
        print("\nno NEC engine available -- nothing to check")
        return 2

    results = {}
    for eng in engines:
        print(f"\n{eng.describe()}")
        sol = eng.solve(model, (E_PLANE, H_PLANE, SPHERE_AVG))
        e_cut = sol.cuts[0]
        h_cut = sol.cuts[1]
        trim = study.trim_to_resonance(eng, model)
        results[eng.name] = (sol, trim)

        check("Zin at exactly lambda/2 is near 86 + j47 (L8, Part 5)",
              near(sol.z_real, 86.0, 4.0) and near(sol.z_imag, 47.0, 4.0),
              f"{sol.z_real:.2f} + j{sol.z_imag:.2f} ohm")
        check("peak gain is 2.15 dBi to a tenth (L7)",
              near(e_cut.peak_dbi, 2.15, 0.1), f"{e_cut.peak_dbi:.3f} dBi")
        check("peak sits broadside, theta = 90 deg",
              near(e_cut.peak_angle_deg, 90.0, 0.5),
              f"{e_cut.peak_angle_deg:.1f} deg")
        check("H-plane is a circle to under 0.01 dB",
              max(h_cut.gain_dbi) - min(h_cut.gain_dbi) < 0.01,
              f"ripple {max(h_cut.gain_dbi) - min(h_cut.gain_dbi):.4f} dB")
        check("average power gain is 1.000, accept 0.95-1.05 (L8, Step 4)",
              sol.average_power_gain is not None
              and 0.95 <= sol.average_power_gain <= 1.05,
              f"{sol.average_power_gain:.4f}")
        check("trimmed resonant length is 0.47-0.48 lambda (L7)",
              0.465 <= trim["resonant_length_lambda"] <= 0.485,
              f"{trim['resonant_length_lambda']:.4f} lambda")
        check("resistance at resonance is about 70 ohm (L7)",
              near(trim["r_at_resonance"], 70.0, 6.0),
              f"{trim['r_at_resonance']:.2f} ohm")
        check("E-plane HPBW is 78 deg to two degrees (L7)",
              near(trim["hpbw_deg"], 78.0, 2.0), f"{trim['hpbw_deg']:.1f} deg")

        rows = study.convergence(eng, model)
        drifts = [r.drift_percent for r in rows if r.drift_percent is not None]
        check("impedance drift shrinks under refinement",
              all(b <= a + 1e-9 for a, b in zip(drifts, drifts[1:])),
              " -> ".join(f"{d:.2f}%" for d in drifts))

        res = study.resonant_frequency(eng, model, Sweep(800.0, 41, 5.0))
        check("a wire cut to lambda/2 at 915 MHz resonates low",
              res["resonant_freq_hz"] is not None
              and 850e6 < res["resonant_freq_hz"] < 890e6,
              f"{res['resonant_freq_hz'] / 1e6:.2f} MHz")

    if len(engines) > 1:
        print("\ncross-engine agreement")
        (a_sol, a_trim), (b_sol, b_trim) = list(results.values())
        check("impedance agrees to 0.1 ohm",
              near(a_sol.z_real, b_sol.z_real, 0.1)
              and near(a_sol.z_imag, b_sol.z_imag, 0.1),
              f"{a_sol.z_real:.3f}{a_sol.z_imag:+.3f}j vs "
              f"{b_sol.z_real:.3f}{b_sol.z_imag:+.3f}j")
        check("peak gain agrees to 0.01 dB",
              near(a_sol.cuts[0].peak_dbi, b_sol.cuts[0].peak_dbi, 0.01))
        check("trimmed length agrees to 0.0005 lambda",
              near(a_trim["resonant_length_lambda"],
                   b_trim["resonant_length_lambda"], 5e-4))

    print("\nreading cards back")
    deck = model.deck(requests=(E_PLANE, H_PLANE, SPHERE_AVG))
    parsed = cards.parse(deck)
    check("the generated deck parses without complaint", parsed.ok,
          "; ".join(e.message for e in parsed.errors))
    if parsed.ok:
        check("parsing round-trips to the same cards",
              parsed.model.deck(sweep=parsed.sweep, requests=parsed.requests)
              .splitlines()[2:] == deck.splitlines()[2:])
        check("every line of the deck is glossed",
              len(parsed.gloss) == len([ln for ln in deck.splitlines() if ln.strip()]))
        xnda = [t for g in parsed.gloss for t in g.tokens if t.label == "XNDA"]
        check("the XNDA field is decoded for the reader",
              bool(xnda) and "average power gain" in xnda[-1].detail)
        # Both sides on one engine: `sol` above is whichever engine ran last,
        # and the claim here is about parsing, not about the engines agreeing.
        direct = engines[0].solve(model, (E_PLANE,))
        re_solved = engines[0].solve(parsed.model, parsed.requests)
        check("a parsed deck solves to the same impedance as the model",
              near(re_solved.z_real, direct.z_real, 1e-6)
              and near(re_solved.z_imag, direct.z_imag, 1e-6),
              f"{re_solved.z_real:.4f}{re_solved.z_imag:+.4f}j")

    # The mistakes a student actually makes. Each has to be caught, and caught
    # with a message that names the field rather than the exception.
    base = ["CM t", "CE", "GW 1 9 0 0 -0.08 0 0 0.08 0.0005", "GE 0",
            "EX 0 1 5 0 1 0", "FR 0 1 0 0 915 0", "RP 0 181 1 1000 0 0 1 0", "EN"]

    def broken(swap: dict[int, str] | None = None, drop: int | None = None,
               add: str | None = None) -> cards.ParsedDeck:
        lines = list(base)
        for i, text in (swap or {}).items():
            lines[i] = text
        if drop is not None:
            lines.pop(drop)
        if add:
            lines.insert(-1, add)
        return cards.parse("\n".join(lines))

    def complains(label: str, parsed: cards.ParsedDeck, wanted: str) -> None:
        msgs = " | ".join(e.message + " " + e.hint for e in parsed.errors)
        check(label, not parsed.ok and wanted in msgs,
              msgs or "no error was reported")

    complains("a feed past the end of the wire is caught",
              broken({4: "EX 0 1 11 0 1 0"}), "wire 1 has 9")
    complains("a feed on a wire that does not exist is caught",
              broken({4: "EX 0 2 5 0 1 0"}), "no GW card defines")
    complains("a ground plane is refused by name",
              broken(add="GN 1"), "free space")
    complains("a missing frequency card is caught", broken(drop=5), "no FR card")
    complains("a wire with no length is caught",
              broken({2: "GW 1 9 0 0 0 0 0 0 0.0005"}), "zero length")
    complains("a duplicate tag is caught",
              broken(add="GW 1 9 0 0.02 -0.08 0 0.02 0.08 0.0005"), "already used")
    complains("a short GW card is caught",
              broken({2: "GW 1 9 0 0 -0.08"}), "GW needs 9 numbers")
    complains("a non-numeric field is caught",
              broken({2: "GW 1 nine 0 0 -0.08 0 0 0.08 0.0005"}), "not a number")

    print("\nchamber interoperability")
    sol = engines[0].solve(model, (E_PLANE, H_PLANE))
    csv = export.pattern_csv(sol.cuts, provenance="selftest")
    header = [line for line in csv.splitlines() if not line.startswith("#")][0]
    cols = header.split(",")
    # These four names are what usafa-chamber's reference.js matches on its
    # exact pass. Rename one and the overlay silently stops finding the cut.
    for want in ("param", "angle_deg", "freq_hz", "gain_dbi"):
        check(f"pattern CSV carries the '{want}' column the chamber importer wants",
              want in cols)
    check("both cuts are in the file",
          {"E-plane", "H-plane"} <= {line.split(",")[0] for line in csv.splitlines()[1:]
                                     if not line.startswith("#")})

    print()
    if FAILURES:
        print(f"{len(FAILURES)} check(s) failed:")
        for f in FAILURES:
            print(f"  - {f}")
        return 1
    print("all checks passed")
    return 0


if __name__ == "__main__":
    sys.exit(run())
