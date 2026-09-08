"""Wire models for the L8 simulation lab, and the NEC deck they generate.

The deck is the point. NEC's two-letter cards are what the lesson teaches and
what every NEC front end -- 4nec2, xnec2c, this tool -- actually consumes, so
every model here can print the exact cards it is about to run. A student who
learns the form in this file can drive any of those programs.

Lengths are in meters throughout, because that is what the GW card wants.
Frequencies are in MHz, because that is what the FR card wants. Converting at
the edges keeps unit confusion out of the middle of the code.
"""

from __future__ import annotations

from dataclasses import dataclass, field, replace

C = 299_792_458.0  # m/s, exact by definition


def wavelength(freq_mhz: float) -> float:
    """Free-space wavelength in meters."""
    return C / (freq_mhz * 1e6)


def _n(x: float) -> str:
    """A number formatted the way NEC decks are conventionally written.

    Six significant figures is more than the solver resolves and less than the
    noise a full repr would add to a deck a student is meant to read.
    """
    return f"{x:.6g}"


@dataclass(frozen=True)
class Wire:
    """One GW card: a straight wire of constant radius, cut into segments."""

    tag: int
    segments: int
    x1: float
    y1: float
    z1: float
    x2: float
    y2: float
    z2: float
    radius: float

    @property
    def length(self) -> float:
        return ((self.x2 - self.x1) ** 2 + (self.y2 - self.y1) ** 2
                + (self.z2 - self.z1) ** 2) ** 0.5

    @property
    def segment_length(self) -> float:
        return self.length / self.segments

    @property
    def center_segment(self) -> int:
        """The segment a center feed belongs on, 1-indexed as NEC counts.

        Only exact for an odd segment count. An even count has a junction at
        the center rather than a segment, which is why the lab insists on odd
        and why `Model.check` complains when it is not.
        """
        return (self.segments + 1) // 2

    def card(self) -> str:
        return (f"GW {self.tag} {self.segments} "
                f"{_n(self.x1)} {_n(self.y1)} {_n(self.z1)} "
                f"{_n(self.x2)} {_n(self.y2)} {_n(self.z2)} {_n(self.radius)}")


@dataclass(frozen=True)
class Feed:
    """One EX card: an applied-field voltage source on a single segment.

    The lab drives 1 V so that Zin = 1/Ifeed, which makes the impedance
    readout and the current readout the same measurement seen twice.
    """

    tag: int
    segment: int
    volts_real: float = 1.0
    volts_imag: float = 0.0

    def card(self) -> str:
        return (f"EX 0 {self.tag} {self.segment} 0 "
                f"{_n(self.volts_real)} {_n(self.volts_imag)}")


@dataclass(frozen=True)
class PatternRequest:
    """One RP card: a pattern cut, or a coarse sphere for the energy audit.

    `average` sets the A digit of XNDA, which is what asks NEC for the average
    power gain. That number is the lab's conservation-of-energy check and is
    only meaningful over a complete sphere in free space.
    """

    name: str
    theta_start: float = 0.0
    n_theta: int = 181
    d_theta: float = 1.0
    phi_start: float = 0.0
    n_phi: int = 1
    d_phi: float = 0.0
    average: bool = False

    @property
    def xnda(self) -> str:
        # X=1 major/minor -> vertical/horizontal columns, N=D=0, A per request.
        return f"100{1 if self.average else 0}"

    @property
    def swept_axis(self) -> str:
        """Which angle a polar plot of this cut should run on."""
        return "theta" if self.n_theta >= self.n_phi else "phi"

    def card(self) -> str:
        return (f"RP 0 {self.n_theta} {self.n_phi} {self.xnda} "
                f"{_n(self.theta_start)} {_n(self.phi_start)} "
                f"{_n(self.d_theta)} {_n(self.d_phi)}")


# The three requests the lab actually uses. The wire lies along z by course
# convention, so the E-plane is a phi = 0 cut swept in theta and the H-plane is
# the theta = 90 cut swept in phi.
E_PLANE = PatternRequest("E-plane", theta_start=0.0, n_theta=181, d_theta=1.0,
                         phi_start=0.0, n_phi=1, d_phi=0.0)
H_PLANE = PatternRequest("H-plane", theta_start=90.0, n_theta=1, d_theta=0.0,
                         phi_start=0.0, n_phi=361, d_phi=1.0)
SPHERE_AVG = PatternRequest("sphere", theta_start=0.0, n_theta=19, d_theta=10.0,
                            phi_start=0.0, n_phi=36, d_phi=10.0, average=True)


@dataclass(frozen=True)
class Sweep:
    """One FR card: `n` frequencies from `start_mhz` in `step_mhz` steps."""

    start_mhz: float
    n: int = 1
    step_mhz: float = 0.0

    @property
    def frequencies_mhz(self) -> list[float]:
        return [self.start_mhz + i * self.step_mhz for i in range(self.n)]

    def card(self) -> str:
        return f"FR 0 {self.n} 0 0 {_n(self.start_mhz)} {_n(self.step_mhz)}"


@dataclass(frozen=True)
class Model:
    """A complete free-space wire model: geometry, feed, and a frequency."""

    wires: tuple[Wire, ...]
    feed: Feed
    freq_mhz: float
    comment: str = "ECE 444 -- nec_lab model"

    @staticmethod
    def dipole(freq_mhz: float, length_m: float, radius_m: float = 0.0005,
               segments: int = 21, comment: str | None = None) -> "Model":
        """A center-fed straight dipole along z -- the L8 antenna."""
        half = length_m / 2.0
        wire = Wire(1, segments, 0.0, 0.0, -half, 0.0, 0.0, half, radius_m)
        return Model(
            wires=(wire,),
            feed=Feed(1, wire.center_segment),
            freq_mhz=freq_mhz,
            comment=comment or f"ECE 444 -- dipole, {_n(freq_mhz)} MHz",
        )

    @property
    def wavelength(self) -> float:
        return wavelength(self.freq_mhz)

    def at_frequency(self, freq_mhz: float) -> "Model":
        return replace(self, freq_mhz=freq_mhz)

    def with_length(self, length_m: float) -> "Model":
        """The same model with wire 1 rescaled about its center.

        Used by the resonance trim, which shortens the wire and re-solves.
        """
        w = self.wires[0]
        scale = length_m / w.length
        moved = replace(w,
                        x1=w.x1 * scale, y1=w.y1 * scale, z1=w.z1 * scale,
                        x2=w.x2 * scale, y2=w.y2 * scale, z2=w.z2 * scale)
        return replace(self, wires=(moved,) + self.wires[1:])

    def with_segments(self, segments: int) -> "Model":
        """The same model at a different segmentation, feed kept centered."""
        w = replace(self.wires[0], segments=segments)
        feed = replace(self.feed, segment=w.center_segment)
        return replace(self, wires=(w,) + self.wires[1:], feed=feed)

    def deck(self, sweep: Sweep | None = None,
             requests: tuple[PatternRequest, ...] = ()) -> str:
        """The NEC input file for this model, as text.

        This is what the tool runs and what the student is expected to be able
        to read. Nothing else in the pipeline gets to know the geometry.
        """
        lines = [f"CM {self.comment}", "CE"]
        lines += [w.card() for w in self.wires]
        lines.append("GE 0")
        lines.append(self.feed.card())
        lines.append((sweep or Sweep(self.freq_mhz)).card())
        if requests:
            lines += [r.card() for r in requests]
        else:
            lines.append("XQ")  # execute with no pattern: impedance only
        lines.append("EN")
        return "\n".join(lines) + "\n"

    # ---- the segmentation rules the lab grades on ----------------------

    def check(self) -> list[dict]:
        """Every segmentation rule from Part 2, evaluated on this model.

        Returns one entry per rule with the numbers behind it, so the GUI can
        show the arithmetic rather than a bare pass/fail. Nothing here stops a
        run: NEC will happily solve a model that breaks all of them, and
        watching it do so badly is part of the lab.
        """
        lam = self.wavelength
        out = []
        for w in self.wires:
            d = w.segment_length
            out.append({
                "wire": w.tag, "rule": "delta < lambda/20",
                "ok": d < lam / 20, "value": d, "limit": lam / 20,
                "detail": f"segment {d * 1000:.2f} mm, limit {lam / 20 * 1000:.2f} mm",
            })
            out.append({
                "wire": w.tag, "rule": "delta > 8a",
                "ok": d > 8 * w.radius, "value": d, "limit": 8 * w.radius,
                "detail": f"segment {d * 1000:.2f} mm, floor {8 * w.radius * 1000:.2f} mm",
            })
            # The density rule has a hard floor and a soft ceiling. Below ten
            # per half wavelength the current is genuinely under-resolved;
            # above twenty the only cost is time, and the lesson's own 21
            # segments on a half-wave wire sit just past it. Flagging that as
            # a violation would teach the wrong thing, so the ceiling is
            # advisory and the delta > 8a rule is what actually bounds
            # refinement from above.
            per_half = w.segments / (w.length / (lam / 2))
            out.append({
                "wire": w.tag, "rule": "10+ segments per half wavelength",
                "ok": per_half >= 10, "value": per_half, "limit": 10.0,
                "detail": (f"{per_half:.1f} per half wavelength"
                           + (" (past 20: time, not accuracy)"
                              if per_half > 20 else "")),
            })
            out.append({
                "wire": w.tag, "rule": "2*pi*a << lambda",
                "ok": 2 * 3.141592653589793 * w.radius < lam / 100,
                "value": 2 * 3.141592653589793 * w.radius, "limit": lam / 100,
                "detail": f"circumference {2 * 3.141592653589793 * w.radius * 1000:.2f} mm",
            })
            out.append({
                "wire": w.tag, "rule": "odd segment count",
                "ok": w.segments % 2 == 1, "value": float(w.segments), "limit": 0.0,
                "detail": "feed lands off-center on an even count",
            })
        return out
