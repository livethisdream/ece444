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

import math
import sys

from . import builders, cards, export, study
from .engine import ExecutableEngine, PyNecEngine
from .model import (E_PLANE, H_PLANE, Model, SPHERE_AVG, Sweep,
                    audit_request, cuts_for, sphere_request, wavelength)

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

    print("\nthe whole sphere")
    surfaces = {}
    for eng in engines:
        surf = eng.surface(model, sphere_request(10.0))
        surfaces[eng.name] = surf
        theta, phi = surf.peak_direction
        check(f"{eng.name}: the grid is the size the RP card asked for",
              len(surf.theta_deg) == 19 and len(surf.phi_deg) == 37,
              f"{len(surf.theta_deg)} x {len(surf.phi_deg)}")
        check(f"{eng.name}: the sphere's peak is the cut's peak",
              near(surf.peak_dbi, results[eng.name][0].cuts[0].peak_dbi, 0.01),
              f"{surf.peak_dbi:.3f} dBi at theta {theta:.0f}")
        check(f"{eng.name}: peak is broadside to the wire", near(theta, 90.0, 0.1))
        # A wire along z radiates the same in every phi. If it does not, the
        # grid has been transposed somewhere between NEC and here.
        ripple = max(max(row) - min(row) for row in surf.gain_dbi[1:-1])
        check(f"{eng.name}: gain does not vary with phi for a z-directed wire",
              ripple < 0.01, f"ripple {ripple:.4f} dB")
        # The null is on the wire axis, which is the whole point of the picture.
        pole = max(surf.gain_dbi[0])
        check(f"{eng.name}: the null is along the wire",
              pole < surf.peak_dbi - 30, f"{pole:.1f} dBi at theta 0")

    if len(engines) > 1:
        a, b = surfaces[engines[0].name], surfaces[engines[1].name]
        worst = max(abs(x - y) for ra, rb in zip(a.gain_dbi, b.gain_dbi)
                    for x, y in zip(ra, rb) if x > -100 and y > -100)
        check("the two engines agree over the whole sphere", worst < 0.02,
              f"worst {worst:.4f} dB")

    surf = surfaces[engines[0].name]
    sphere_text = export.sphere_csv(surf, provenance="selftest")
    body = [ln for ln in sphere_text.splitlines() if not ln.startswith("#")]
    check("the sphere CSV has a row per direction",
          len(body) - 1 == len(surf.theta_deg) * len(surf.phi_deg),
          f"{len(body) - 1} rows")
    check("the sphere CSV names both angles",
          body[0].split(",")[:2] == ["theta_deg", "phi_deg"], body[0])

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
    # GN is supported now (L9 needs it), so what has to be caught is the pair
    # coming apart: a ground card with a free-space GE, and the reverse.
    complains("a GN card with no GE 1 is caught",
              broken(add="GN 1"), "GE does not say 1")
    complains("GE 1 with no GN card is caught",
              broken(swap={3: "GE 1"}), "no GN card")
    complains("a ground model nec_lab does not run is refused",
              broken(swap={3: "GE 1"}, add="GN 0"), "not a ground model")
    complains("a load is still refused by name",
              broken(add="LD 0 1 5 5 10 0"), "load")
    complains("a missing frequency card is caught", broken(drop=5), "no FR card")
    complains("a wire with no length is caught",
              broken({2: "GW 1 9 0 0 0 0 0 0 0.0005"}), "zero length")
    complains("a duplicate tag is caught",
              broken(add="GW 1 9 0 0.02 -0.08 0 0.02 0.08 0.0005"), "already used")
    complains("a short GW card is caught",
              broken({2: "GW 1 9 0 0 -0.08"}), "GW needs 9 numbers")
    complains("a non-numeric field is caught",
              broken({2: "GW 1 nine 0 0 -0.08 0 0 0.08 0.0005"}), "not a number")

    print("\nthe antenna catalog")
    eng = engines[0]

    def built(kind, **params):
        m = builders.build(kind, params)
        grounded = m.ground.present
        sol = eng.solve(m, cuts_for(grounded)
                        + (() if grounded else (audit_request(m),)))
        surf = eng.surface(m, sphere_request(5.0, hemisphere=grounded))
        return m, sol, surf

    # Monopole: half a dipole over its image. Half the impedance, 3 dB more
    # gain, and the peak on the horizon.
    m, sol, surf = built("monopole")
    theta, _ = surf.peak_direction
    check("monopole: Zin is about 36 ohm (half the dipole's)",
          near(sol.z_real, 36.0, 3.0) and abs(sol.z_imag) < 5.0,
          f"{sol.z_real:.2f} {'+' if sol.z_imag >= 0 else '-'} j{abs(sol.z_imag):.2f}")
    check("monopole: gain is about 5.15 dBi (3 dB over the dipole)",
          near(surf.peak_dbi, 5.15, 0.2), f"{surf.peak_dbi:.2f} dBi")
    check("monopole: the peak is on the horizon", near(theta, 90.0, 1.0),
          f"theta {theta:.0f}")
    check("monopole: nothing is computed below the ground plane",
          max(surf.theta_deg) <= 90.0, f"theta runs to {max(surf.theta_deg):.0f}")
    # Take the ground away and it stops being a monopole: that is the point of
    # L9, and it is also proof the GN card is doing something.
    _, free_sol, _ = built("monopole", ground="free")
    check("monopole: removing the ground changes the antenna",
          abs(free_sol.z_real - sol.z_real) > 5.0,
          f"free space gives {free_sol.z_real:.1f}{free_sol.z_imag:+.1f}j")

    # A one-wavelength loop fires broadside to its own plane.
    m, sol, surf = built("loop")
    theta, _ = surf.peak_direction
    check("1 lambda loop: the peak is normal to the loop's plane",
          min(theta, 180 - theta) < 10.0, f"theta {theta:.0f}")
    check("1 lambda loop: gain is about 3 dBi",
          near(surf.peak_dbi, 3.2, 0.5), f"{surf.peak_dbi:.2f} dBi")

    # Yagi: a beam toward the directors, and a real front-to-back.
    m, sol, surf = built("yagi", directors=1)
    theta, phi = surf.peak_direction
    back = surf.gain_dbi[surf.theta_deg.index(90.0)][surf.phi_deg.index(180.0)]
    check("Yagi: the beam points at the directors (+x)",
          near(theta, 90.0, 1.0) and near(phi, 0.0, 1.0),
          f"theta {theta:.0f}, phi {phi:.0f}")
    check("Yagi: 3 elements give more than 7 dBi", surf.peak_dbi > 7.0,
          f"{surf.peak_dbi:.2f} dBi")
    check("Yagi: front-to-back is better than 10 dB",
          surf.peak_dbi - back > 10.0, f"{surf.peak_dbi - back:.1f} dB")
    check("Yagi: the driven element is not a dipole's 73 ohm",
          10.0 < sol.z_real < 40.0, f"{sol.z_real:.1f} ohm")
    # The studies must resize the driven element, not wire 1 (the reflector).
    trimmed = m.with_length(0.9 * m.fed_wire.length)
    check("Yagi: trimming resizes the driven element, not the reflector",
          trimmed.wires[0].length == m.wires[0].length
          and trimmed.wires[1].length < m.wires[1].length)

    # The defect this guards: theta is measured from +z and phi from +x, so
    # two cuts drawn on one dial by their swept angle disagree about where the
    # beam is. Every cut carries the direction of each sample, and the peak
    # directions have to be the same vector -- there is only one beam.
    def peak_direction_of(cut):
        i = cut.gain_dbi.index(cut.peak_dbi)
        th = math.radians(cut.theta_deg[i])
        ph = math.radians(cut.phi_deg[i])
        return (math.sin(th) * math.cos(ph), math.sin(th) * math.sin(ph),
                math.cos(th))

    m, sol, _ = built("yagi", directors=1)
    dirs = [peak_direction_of(c) for c in sol.cuts]
    worst = max(math.dist(dirs[0], d) for d in dirs) if len(dirs) > 1 else 0.0
    check("every cut agrees on which way the beam points",
          worst < 0.05 and len(dirs) > 1,
          f"{len(dirs)} cuts, peak directions differ by {worst:.4f} "
          f"(1.0 would be 60 degrees apart)")

    # A theta sweep at one phi is half a plane; in free space the cut closes
    # the circle so a dipole's elevation pattern has both of its lobes.
    _, dip_sol, _ = built("dipole")
    elev = next(c for c in dip_sol.cuts if c.axis == "theta")
    check("a free-space elevation cut is a whole plane, not half",
          max(elev.theta_deg) > 350, f"theta runs to {max(elev.theta_deg):.0f}")
    at90 = elev.gain_dbi[elev.theta_deg.index(90.0)]
    at270 = elev.gain_dbi[elev.theta_deg.index(270.0)]
    check("both lobes of the dipole are in that cut",
          near(at90, at270, 0.01) and near(at90, elev.peak_dbi, 0.01),
          f"{at90:.2f} dBi at theta 90, {at270:.2f} dBi at theta 270")

    # A driven array: one source per element, and coupling that makes them
    # differ. Then a phase slope that moves the beam.
    m, sol, surf = built("array", elements=4)
    theta, phi = surf.peak_direction
    check("array: one feed per element", len(sol.feeds) == 4,
          f"{len(sol.feeds)} feeds")
    zs = [complex(f["z_real"], f["z_imag"]) for f in sol.feeds]
    check("array: the element impedances differ (mutual coupling)",
          abs(zs[0] - zs[1]) > 1.0,
          " ".join(f"{z.real:.0f}{z.imag:+.0f}j" for z in zs))
    check("array: an unphased array fires broadside",
          near(theta, 90.0, 1.0) and min(abs(phi), abs(phi - 180)) < 2.0,
          f"theta {theta:.0f}, phi {phi:.0f}")
    _, _, steered = built("array", elements=4, phase_deg=-90)
    st_theta, st_phi = steered.peak_direction
    off = min(abs(st_phi - 150.0), abs(st_phi - 30.0))
    check("array: 90 deg per element at half-wave spacing steers 60 deg",
          off < 5.0, f"phi {st_phi:.0f}")

    # The audit has to pass on every type. A ten-degree grid reads 0.88 on a
    # 4-element Yagi -- a correct model called broken -- which is why the grid
    # now follows the structure.
    for kind, params in (("dipole", {}), ("loop", {}), ("yagi", {"directors": 3}),
                         ("array", {"elements": 4})):
        _, sol_k, _ = built(kind, **params)
        g = sol_k.average_power_gain
        check(f"{kind}: the energy audit passes at the grid we ask for",
              g is not None and 0.95 <= g <= 1.05, f"{g:.4f}")

    # Every builder writes cards, and those cards have to read back as the
    # same antenna -- otherwise the deck on screen is not what was solved.
    for kind in builders.BY_KEY:
        m_k = builders.build(kind, {})
        again = cards.parse(m_k.deck(requests=cuts_for(m_k.ground.present)))
        ok = (again.ok and len(again.model.wires) == len(m_k.wires)
              and len(again.model.feeds) == len(m_k.feeds)
              and again.model.ground.kind == m_k.ground.kind)
        check(f"{kind}: its deck reads back as the same antenna", ok,
              "; ".join(e.message for e in again.errors) if not ok else
              f"{len(m_k.wires)} wires, {len(m_k.feeds)} feeds, "
              f"{m_k.ground.kind} ground")

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
