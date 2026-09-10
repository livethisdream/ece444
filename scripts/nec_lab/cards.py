"""Reading NEC cards, so the deck in the GUI can be typed as well as read.

`model.py` writes cards. This reads them back, and it is the half that has to
be pedagogical: a student who mistypes a card should be told which field is
wrong and why, on the line it is on, rather than getting a plausible answer for
a different antenna.

What is supported is exactly what this tool writes -- CM, CE, GW, GE, EX, FR,
RP, XQ, EN. Anything else is refused by name with a pointer to 4nec2, and that
refusal is deliberate. A card like GN (a ground plane) or LD (a load) changes
the antenna in a way the rest of nec_lab does not model: the segmentation
rules, the free-space energy audit and the study code all assume a bare wire in
free space. Passing an unrecognized card through to the engine would give a
correct NEC answer described by a page that had quietly stopped applying to it,
which is a worse failure than being told no.
"""

from __future__ import annotations

from dataclasses import dataclass, field

from .model import Feed, Ground, Model, PatternRequest, Sweep, Wire

# Cards a NEC deck may carry that this tool cannot model, and what each one
# does -- the message is more use to a student than "unsupported card".
KNOWN_ELSEWHERE = {
    "GA": "an arc; nec_lab models straight wires only",
    "GH": "a helix; nec_lab models straight wires only",
    "GM": "a geometry copy/move; write the wires out as separate GW cards",
    "GR": "a rotational copy; write the wires out as separate GW cards",
    "GS": "a geometry scale factor; write the coordinates in meters instead",
    "GX": "a reflection in a symmetry plane; write the wires out",
    "LD": "a load on a segment; nec_lab models lossless wire",
    "TL": "a transmission line between segments",
    "NT": "a network between segments",
    "EK": "the extended thin-wire kernel",
    "KH": "an interaction-approximation distance",
    "NE": "a near-field request; nec_lab computes far fields",
    "NH": "a near-field request; nec_lab computes far fields",
    "PT": "print control for currents",
    "PQ": "print control for charge densities",
    "CP": "coupling between antennas",
}


@dataclass
class CardError:
    line_no: int
    text: str
    message: str
    hint: str = ""


@dataclass
class Token:
    """One field of a card, with the name the lesson gives it."""

    text: str
    label: str
    detail: str = ""


@dataclass
class CardGloss:
    """One line of the deck, annotated field by field."""

    line_no: int
    text: str
    card: str
    tokens: list[Token]
    summary: str
    ok: bool = True


@dataclass
class ParsedDeck:
    model: Model | None
    sweep: Sweep | None
    requests: tuple[PatternRequest, ...]
    gloss: list[CardGloss] = field(default_factory=list)
    errors: list[CardError] = field(default_factory=list)

    @property
    def ok(self) -> bool:
        return self.model is not None and not self.errors


def _num(tok: str) -> float:
    return float(tok.replace("D", "E").replace("d", "e"))


def _mm(x: float) -> str:
    return f"{x * 1000:.2f} mm"


def _xnda(field_text: str) -> tuple[int, int, int, int]:
    """Split the RP card's packed XNDA field into its four digits."""
    padded = field_text.rjust(4, "0")[-4:]
    return tuple(int(c) for c in padded)  # type: ignore[return-value]


# The RP card's fourth field is four digits glued together, which is the single
# most opaque thing in the format. Naming them is most of the fix.
XNDA_HELP = {
    "X": {0: "major/minor axis gains", 1: "vertical/horizontal gains"},
    "N": {0: "no normalization", 1: "normalized to the major-axis maximum",
          2: "normalized to the minor-axis maximum",
          3: "normalized to the vertical maximum",
          4: "normalized to the horizontal maximum",
          5: "normalized to the total-gain maximum"},
    "D": {0: "power gain", 1: "directive gain"},
    "A": {0: "no average", 1: "average power gain over the requested angles"},
}


def annotate(line: str, line_no: int) -> CardGloss:
    """Label every field of one card, for the deck view in the GUI."""
    toks = line.split()
    card = toks[0].upper() if toks else ""
    t = lambda i: toks[i] if i < len(toks) else ""   # noqa: E731

    def gl(pairs, summary, ok=True):
        return CardGloss(line_no, line, card,
                         [Token(x, lab, det) for x, lab, det in pairs],
                         summary, ok)

    if card == "CM":
        return gl([(toks[0], "comment card", "")]
                  + [(w, "comment text", "") for w in toks[1:]],
                  "a comment; NEC copies it into the output file")
    if card == "CE":
        return gl([(toks[0], "last comment card", "")],
                  "end of the comments; the model starts on the next line")
    if card == "GW":
        try:
            x1, y1, z1 = _num(t(3)), _num(t(4)), _num(t(5))
            x2, y2, z2 = _num(t(6)), _num(t(7)), _num(t(8))
            a = _num(t(9))
            length = ((x2 - x1) ** 2 + (y2 - y1) ** 2 + (z2 - z1) ** 2) ** 0.5
            n = int(_num(t(2)))
            summary = (f"wire {t(1)}: {_mm(length)} long, "
                       f"{n} segments of {_mm(length / n)}, radius {_mm(a)}")
        except (ValueError, IndexError, ZeroDivisionError):
            summary = "wire -- a field is missing or is not a number"
        return gl([(t(0), "card", "geometry: a straight wire"),
                   (t(1), "tag", "the wire's number, used by EX"),
                   (t(2), "segments", "how many pieces the wire is cut into"),
                   (t(3), "x1", "first end, meters"), (t(4), "y1", "meters"),
                   (t(5), "z1", "meters"),
                   (t(6), "x2", "second end, meters"), (t(7), "y2", "meters"),
                   (t(8), "z2", "meters"),
                   (t(9), "radius", "wire radius, meters")], summary)
    if card == "GE":
        flag = t(1) or "0"
        grounded = flag.strip().startswith("1")
        return gl([(t(0), "card", "geometry complete"),
                   (flag, "ground flag",
                    "1 = the structure meets a ground plane; 0 = free space")],
                  "the geometry is finished; "
                  + ("a ground plane follows on a GN card" if grounded
                     else "0 means no ground plane"))
    if card == "GN":
        kind = t(1) or "0"
        detail = {"1": "a perfect (infinite, lossless) ground plane",
                  "2": "real ground, from the permittivity and conductivity"}
        return gl([(t(0), "card", "ground"),
                   (kind, "type", detail.get(kind, "a ground model nec_lab "
                                                   "does not run")),
                   (t(2), "radials", "0"), (t(3), "unused", ""),
                   (t(4), "unused", ""), (t(5), "unused", ""),
                   (t(6), "permittivity", "relative, real ground only"),
                   (t(7), "conductivity", "S/m, real ground only")],
                  "perfect ground: the image of the antenna, for free"
                  if kind == "1" else
                  f"real ground, eps_r {t(6) or '?'} and {t(7) or '?'} S/m"
                  if kind == "2" else
                  f"GN type {kind}: not one nec_lab runs")
    if card == "EX":
        return gl([(t(0), "card", "excitation"),
                   (t(1), "type", "0 = applied-field voltage source"),
                   (t(2), "tag", "which wire carries the source"),
                   (t(3), "segment", "which segment of that wire"),
                   (t(4), "flags", "0 = no admittance printout"),
                   (t(5), "V real", "volts"), (t(6), "V imag", "volts")],
                  f"a voltage source on wire {t(2)}, segment {t(3)}; "
                  f"Zin comes from the current it drives")
    if card == "FR":
        try:
            n = int(_num(t(2)))
            start, step = _num(t(5)), _num(t(6) or 0)
            summary = (f"{n} frequency step(s) from {start:g} MHz"
                       + (f" in {step:g} MHz steps" if n > 1 else ""))
        except (ValueError, IndexError):
            summary = "frequency -- a field is missing or is not a number"
        return gl([(t(0), "card", "frequency"),
                   (t(1), "type", "0 = linear stepping"),
                   (t(2), "steps", "how many frequencies"),
                   (t(3), "unused", ""), (t(4), "unused", ""),
                   (t(5), "start", "MHz"), (t(6), "step", "MHz")], summary)
    if card == "RP":
        x, n, d, a = _xnda(t(4) or "0")
        try:
            summary = (f"pattern: {int(_num(t(2)))} theta x {int(_num(t(3)))} phi, "
                       f"from theta {_num(t(5)):g} phi {_num(t(6)):g} "
                       f"in steps of {_num(t(7)):g} and {_num(t(8) or 0):g} degrees"
                       + ("; and the average power gain" if a else ""))
        except (ValueError, IndexError):
            summary = "pattern -- a field is missing or is not a number"
        return gl([(t(0), "card", "radiation pattern"),
                   (t(1), "mode", "0 = normal far-field pattern"),
                   (t(2), "n theta", "number of theta angles"),
                   (t(3), "n phi", "number of phi angles"),
                   (t(4), "XNDA", "; ".join(
                       f"{k}={v}: {XNDA_HELP[k].get(v, 'unsupported')}"
                       for k, v in zip("XNDA", (x, n, d, a)))),
                   (t(5), "theta start", "degrees from +z"),
                   (t(6), "phi start", "degrees from +x"),
                   (t(7), "theta step", "degrees"),
                   (t(8), "phi step", "degrees")], summary)
    if card == "XQ":
        return gl([(t(0), "card", "execute")],
                  "run the model with no pattern requested: impedance only")
    if card == "EN":
        return gl([(t(0), "card", "end of the deck")], "end of input")
    hint = KNOWN_ELSEWHERE.get(card, "")
    return gl([(toks[0], "unsupported card", hint)] if toks else [],
              f"{card}: {hint}" if hint else f"{card}: not a card nec_lab knows",
              ok=False)


def parse(text: str) -> ParsedDeck:
    """Read a deck into a Model, a Sweep and a list of pattern requests."""
    wires: list[Wire] = []
    feeds: list[Feed] = []
    ground = Ground("free")
    ge_grounded = False
    sweep: Sweep | None = None
    requests: list[PatternRequest] = []
    comment = "ECE 444 -- from typed cards"
    errors: list[CardError] = []
    gloss: list[CardGloss] = []

    for i, raw in enumerate(text.splitlines(), start=1):
        line = raw.strip()
        if not line:
            continue
        gloss.append(annotate(line, i))
        toks = line.split()
        card = toks[0].upper()

        def bad(msg: str, hint: str = "") -> None:
            errors.append(CardError(i, line, msg, hint))

        try:
            if card == "CM":
                comment = line[2:].strip() or comment
            elif card in ("CE", "XQ", "EN"):
                pass
            elif card == "GE":
                flag = int(_num(toks[1])) if len(toks) > 1 else 0
                if flag not in (0, 1):
                    bad(f"GE flag {flag} is not one nec_lab runs",
                        "0 for free space, 1 when the structure meets ground")
                ge_grounded = flag == 1
            elif card == "GN":
                kind = int(_num(toks[1])) if len(toks) > 1 else -1
                if kind == 1:
                    ground = Ground("perfect")
                elif kind == 2:
                    eps = _num(toks[6]) if len(toks) > 6 else 13.0
                    sig = _num(toks[7]) if len(toks) > 7 else 0.005
                    ground = Ground("real", eps, sig)
                else:
                    bad(f"GN type {kind} is not a ground model nec_lab runs",
                        "GN 1 for perfect ground, or GN 2 0 0 0 eps sigma "
                        "for real ground")
            elif card == "GW":
                if len(toks) < 10:
                    bad(f"GW needs 9 numbers after the card, found {len(toks) - 1}",
                        "GW tag segments x1 y1 z1 x2 y2 z2 radius")
                    continue
                tag, segs = int(_num(toks[1])), int(_num(toks[2]))
                w = Wire(tag, segs, *(_num(t) for t in toks[3:10]))
                if segs < 1:
                    bad("a wire needs at least one segment")
                elif w.length <= 0:
                    bad("this wire has zero length",
                        "the two ends are the same point")
                elif w.radius <= 0:
                    bad("the wire radius must be greater than zero")
                elif any(x.tag == tag for x in wires):
                    bad(f"tag {tag} is already used by another wire",
                        "every GW card needs its own tag number")
                else:
                    wires.append(w)
            elif card == "EX":
                if len(toks) < 6:
                    bad(f"EX needs at least 5 fields, found {len(toks) - 1}",
                        "EX 0 tag segment 0 volts")
                    continue
                if int(_num(toks[1])) != 0:
                    bad("nec_lab supports excitation type 0 only",
                        "type 0 is the applied-field voltage source the lab uses")
                    continue
                feeds.append(Feed(int(_num(toks[2])), int(_num(toks[3])),
                                  _num(toks[5]),
                                  _num(toks[6]) if len(toks) > 6 else 0.0))
            elif card == "FR":
                if len(toks) < 6:
                    bad(f"FR needs 5 numbers after the card, found {len(toks) - 1}",
                        "FR 0 steps 0 0 start_MHz step_MHz")
                    continue
                if int(_num(toks[1])) != 0:
                    bad("nec_lab supports linear frequency stepping only",
                        "the first field must be 0")
                    continue
                n = int(_num(toks[2])) or 1
                start = _num(toks[5])
                step = _num(toks[6]) if len(toks) > 6 else 0.0
                if start <= 0:
                    bad("the frequency must be greater than zero")
                    continue
                sweep = Sweep(start, n, step)
            elif card == "RP":
                if len(toks) < 9:
                    bad(f"RP needs at least 8 numbers after the card, found {len(toks) - 1}",
                        "RP 0 n_theta n_phi XNDA theta0 phi0 dtheta dphi")
                    continue
                if int(_num(toks[1])) != 0:
                    bad("nec_lab supports RP mode 0 (normal far field) only")
                    continue
                x, nrm, d, avg = _xnda(toks[4])
                if x not in (0, 1) or d != 0 or nrm not in XNDA_HELP["N"]:
                    bad(f"XNDA field {toks[4]} asks for output nec_lab does not read",
                        "use 1000 for a pattern cut, 1001 to add the average power gain")
                    continue
                n_theta, n_phi = int(_num(toks[2])), int(_num(toks[3]))
                if n_theta < 1 or n_phi < 1:
                    bad("a pattern needs at least one angle on each axis")
                    continue
                # Name the cut after what it sweeps. The generated decks use
                # "E-plane" and "H-plane", but a typed RP card can be any cut,
                # and a legend reading "cut 2" tells a student nothing.
                if avg:
                    name = "sphere"
                elif n_phi <= 1:
                    name = f"theta cut, phi = {_num(toks[6]):g} deg"
                elif n_theta <= 1:
                    name = f"phi cut, theta = {_num(toks[5]):g} deg"
                else:
                    name = f"{n_theta} x {n_phi} sweep"
                requests.append(PatternRequest(
                    name=name,
                    theta_start=_num(toks[5]), n_theta=n_theta,
                    d_theta=_num(toks[7]),
                    phi_start=_num(toks[6]), n_phi=n_phi,
                    d_phi=_num(toks[8]) if len(toks) > 8 else 0.0,
                    average=bool(avg)))
            else:
                hint = KNOWN_ELSEWHERE.get(card, "")
                bad(f"{card} is not a card nec_lab can run",
                    (hint + ". Copy the deck into 4nec2 to run it there.")
                    if hint else "nec_lab reads CM CE GW GE EX FR RP XQ EN")
        except (ValueError, IndexError):
            bad("a field on this card is not a number")

    if not wires:
        errors.append(CardError(0, "", "the deck has no GW card",
                                "a model needs at least one wire"))
    if not feeds:
        errors.append(CardError(0, "", "the deck has no EX card",
                                "without a source there is no impedance to report"))
    # GE and GN have to agree. Either alone is a model the author did not mean:
    # a GN with GE 0 is a ground NEC will not connect anything to, and GE 1
    # with no GN leaves the ground unspecified.
    if ground.present and not ge_grounded:
        errors.append(CardError(0, "", "there is a GN card but GE does not say 1",
                                "GE 1 tells NEC the structure meets the ground"))
    if ge_grounded and not ground.present:
        errors.append(CardError(0, "", "GE says 1 but there is no GN card",
                                "add GN 1 for a perfect ground plane"))
    if sweep is None:
        errors.append(CardError(0, "", "the deck has no FR card",
                                "NEC needs to be told a frequency"))

    # Cross-card checks: the errors that only show up once the cards are read
    # together, which is exactly the class of mistake a beginner makes.
    for feed in feeds:
        host = next((w for w in wires if w.tag == feed.tag), None)
        if host is None:
            errors.append(CardError(
                0, "", f"an EX card feeds wire {feed.tag}, which no GW card defines",
                "the EX tag has to match a GW tag"))
        elif not 1 <= feed.segment <= host.segments:
            errors.append(CardError(
                0, "", f"an EX card feeds segment {feed.segment}, but wire "
                       f"{feed.tag} has {host.segments}",
                f"a center feed on this wire is segment {host.center_segment}"))

    model = None
    if wires and feeds and sweep is not None:
        model = Model(tuple(wires), tuple(feeds), sweep.start_mhz, comment, ground)

    return ParsedDeck(model, sweep, tuple(requests), gloss, errors)
