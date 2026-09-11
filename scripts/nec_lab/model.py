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


def sphere_request(step_deg: float = 5.0, name: str = "sphere",
                   hemisphere: bool = False) -> PatternRequest:
    """A whole-sphere RP card: theta 0-180 and phi 0-360 on one grid.

    The same card the lab already uses for the energy audit, asked at a step
    fine enough to draw. NEC has always computed this -- the cuts are what we
    were choosing to look at.

    `hemisphere` stops at the horizon, and a grounded model needs it. There is
    no field below a ground plane and NEC does not pretend otherwise: ask for
    theta past 90 over ground and the numbers that come back are not small,
    they are garbage -- 1e120 dBi in the case that found this.
    """
    span = 90.0 if hemisphere else 180.0
    n_theta = int(round(span / step_deg)) + 1
    n_phi = int(round(360.0 / step_deg)) + 1
    return PatternRequest(name, theta_start=0.0, n_theta=n_theta, d_theta=step_deg,
                          phi_start=0.0, n_phi=n_phi, d_phi=step_deg)


def audit_request(model: "Model") -> PatternRequest:
    """The RP card for the energy audit, at a grid the antenna deserves.

    The average power gain is an integral, and NEC does it by summing the grid
    you asked for. L8's `RP 0 19 36 1001` -- ten degrees -- is plenty for a
    dipole, which is why the handout prints it. Point the same card at a
    4-element Yagi and it reads 0.88: the main lobe falls between samples and
    the sum misses power that is really there. The model is fine and the
    audit says it is broken, which is the worst way for a check to fail.

    So the grid follows the structure: ten degrees for a single wire, two for
    anything with more elements, where the pattern has structure to miss.
    """
    if len(model.wires) <= 1:
        return SPHERE_AVG
    return PatternRequest("sphere", theta_start=0.0, n_theta=91, d_theta=2.0,
                          phi_start=0.0, n_phi=180, d_phi=2.0, average=True)


def cuts_for(ground_present: bool) -> tuple[PatternRequest, ...]:
    """The principal cuts, as whole planes rather than half of one.

    A theta sweep at one phi is half a plane. The other half is the same theta
    sweep at phi + 180, and without it a dipole's E-plane is drawn as one lobe
    on the right of the dial. In free space NEC will sweep theta 0 to 360 in a
    single card and close the circle itself; over ground it will not (theta
    past 90 there returns garbage), so the plane is asked for as two cards and
    the page draws both on one dial.
    """
    if not ground_present:
        return (
            PatternRequest("elevation (x-z)", theta_start=0.0, n_theta=361,
                           d_theta=1.0, phi_start=0.0, n_phi=1, d_phi=0.0),
            PatternRequest("azimuth (x-y)", theta_start=90.0, n_theta=1,
                           d_theta=0.0, phi_start=0.0, n_phi=361, d_phi=1.0),
        )
    return (
        PatternRequest("elevation (+x side)", theta_start=0.0, n_theta=91,
                       d_theta=1.0, phi_start=0.0, n_phi=1, d_phi=0.0),
        PatternRequest("elevation (-x side)", theta_start=0.0, n_theta=91,
                       d_theta=1.0, phi_start=180.0, n_phi=1, d_phi=0.0),
        PatternRequest("azimuth (x-y)", theta_start=89.0, n_theta=1,
                       d_theta=0.0, phi_start=0.0, n_phi=361, d_phi=1.0),
    )


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
class Ground:
    """The GE flag and the GN card: what sits under the antenna.

    Free space is the L8 case. A monopole is the L9 case and is nothing
    without a ground plane -- half a dipole, fed against its image, and the
    image only exists because the ground is there.
    """

    kind: str = "free"          # 'free', 'perfect', or 'real'
    epsilon: float = 13.0       # relative permittivity, average soil
    sigma: float = 0.005        # conductivity, S/m

    @property
    def present(self) -> bool:
        return self.kind != "free"

    @property
    def ge_flag(self) -> int:
        return 1 if self.present else 0

    def card(self) -> str | None:
        if self.kind == "perfect":
            return "GN 1"
        if self.kind == "real":
            return f"GN 2 0 0 0 {_n(self.epsilon)} {_n(self.sigma)}"
        return None


FREE_SPACE = Ground("free")
PERFECT_GROUND = Ground("perfect")


@dataclass(frozen=True)
class Model:
    """A wire model: geometry, one or more feeds, a frequency, and a ground."""

    wires: tuple[Wire, ...]
    feeds: tuple[Feed, ...]
    freq_mhz: float
    comment: str = "ECE 444 -- nec_lab model"
    ground: Ground = FREE_SPACE

    @property
    def feed(self) -> Feed:
        """The first feed. Most models have exactly one."""
        return self.feeds[0]

    @property
    def fed_wire(self) -> Wire:
        """The wire the first feed sits on -- the driven element.

        Studies that resize "the antenna" mean this one. On a dipole it is the
        only wire; on a Yagi it is the driven element, and resizing wire 1
        instead would quietly trim the reflector.
        """
        for w in self.wires:
            if w.tag == self.feed.tag:
                return w
        return self.wires[0]

    @staticmethod
    def dipole(freq_mhz: float, length_m: float, radius_m: float = 0.0005,
               segments: int = 21, comment: str | None = None) -> "Model":
        """A center-fed straight dipole along z -- the L8 antenna."""
        half = length_m / 2.0
        wire = Wire(1, segments, 0.0, 0.0, -half, 0.0, 0.0, half, radius_m)
        return Model(
            wires=(wire,),
            feeds=(Feed(1, wire.center_segment),),
            freq_mhz=freq_mhz,
            comment=comment or f"ECE 444 -- dipole, {_n(freq_mhz)} MHz",
        )

    @property
    def wavelength(self) -> float:
        return wavelength(self.freq_mhz)

    def at_frequency(self, freq_mhz: float) -> "Model":
        return replace(self, freq_mhz=freq_mhz)

    def with_length(self, length_m: float) -> "Model":
        """The same model with the DRIVEN wire rescaled about its center.

        Used by the resonance trim. It follows the feed rather than wire 1,
        because on a Yagi wire 1 is the reflector and trimming that would
        report someone else's resonance.
        """
        w = self.fed_wire
        scale = length_m / w.length
        # About the wire's own midpoint, not the origin: a dipole modeled away
        # from the origin -- which is what a typed deck often is -- has to stay
        # where the student put it while it is trimmed.
        cx, cy, cz = (w.x1 + w.x2) / 2, (w.y1 + w.y2) / 2, (w.z1 + w.z2) / 2
        moved = replace(w,
                        x1=cx + (w.x1 - cx) * scale, y1=cy + (w.y1 - cy) * scale,
                        z1=cz + (w.z1 - cz) * scale,
                        x2=cx + (w.x2 - cx) * scale, y2=cy + (w.y2 - cy) * scale,
                        z2=cz + (w.z2 - cz) * scale)
        return replace(self, wires=tuple(moved if x.tag == w.tag else x
                                        for x in self.wires))

    def with_segments(self, segments: int) -> "Model":
        """The same model at a different segmentation of the driven wire.

        The feed moves with it: a segment count that changes without the feed
        following puts the source somewhere else on the wire, and the
        convergence study then measures two things at once.
        """
        old = self.fed_wire
        new_wire = replace(old, segments=segments)
        # A feed at the old center goes to the new center; a feed elsewhere
        # keeps its fractional position along the wire (a monopole's base
        # stays its base).
        feeds = []
        for f in self.feeds:
            if f.tag != old.tag:
                feeds.append(f)
            elif f.segment == old.center_segment:
                feeds.append(replace(f, segment=new_wire.center_segment))
            else:
                frac = (f.segment - 0.5) / old.segments
                feeds.append(replace(f, segment=max(1, min(
                    segments, int(round(frac * segments + 0.5))))))
        return replace(self,
                       wires=tuple(new_wire if x.tag == old.tag else x
                                   for x in self.wires),
                       feeds=tuple(feeds))

    def deck(self, sweep: Sweep | None = None,
             requests: tuple[PatternRequest, ...] = ()) -> str:
        """The NEC input file for this model, as text.

        This is what the tool runs and what the student is expected to be able
        to read. Nothing else in the pipeline gets to know the geometry.
        """
        lines = [f"CM {self.comment}", "CE"]
        lines += [w.card() for w in self.wires]
        lines.append(f"GE {self.ground.ge_flag}")
        gn = self.ground.card()
        if gn:
            lines.append(gn)
        lines += [f.card() for f in self.feeds]
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
            if self.ground.present:
                # The two ways a grounded model goes wrong, both silent: a wire
                # that hangs below the ground plane, and a monopole whose base
                # does not quite touch it. The second one reads as a huge
                # capacitive reactance -- 53 - j1545 ohm for a quarter-wave
                # monopole left 0.1 mm short -- rather than as an error.
                lowest = min(w.z1, w.z2)
                out.append({
                    "wire": w.tag, "rule": "no wire below the ground plane",
                    "ok": lowest >= -1e-9, "value": lowest, "limit": 0.0,
                    "detail": f"lowest point {lowest * 1000:.2f} mm",
                })
                touches = abs(w.z1) < 1e-9 or abs(w.z2) < 1e-9
                fed_here = any(f.tag == w.tag for f in self.feeds)
                if fed_here:
                    out.append({
                        "wire": w.tag, "rule": "fed wire is bonded to the ground",
                        "ok": touches, "value": min(abs(w.z1), abs(w.z2)),
                        "limit": 0.0,
                        "detail": ("base sits on z = 0" if touches else
                                   "base is off the ground plane: NEC sees an "
                                   "open circuit, not a monopole"),
                    })
            center_fed = any(f.tag == w.tag and f.segment == w.center_segment
                             for f in self.feeds)
            if center_fed or not any(f.tag == w.tag for f in self.feeds):
                out.append({
                    "wire": w.tag, "rule": "odd segment count",
                    "ok": w.segments % 2 == 1, "value": float(w.segments),
                    "limit": 0.0,
                    "detail": "feed lands off-center on an even count",
                })
        return out
