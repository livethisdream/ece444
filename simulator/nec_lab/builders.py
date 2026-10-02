"""The antenna types, as builders that write NEC cards.

Every builder returns a `Model`, and a Model prints its own deck -- so the GUI
never learns a second way to describe an antenna. Choosing "Yagi-Uda", filling
in three numbers and pressing Build puts *cards* in the deck editor, which is
the same editor a student can then type in. The builder is a way to get to a
deck quickly, not a way around the deck.

Each type carries a parameter spec so the page can render its form without
knowing anything about antennas, and names the lesson it belongs to.

What is here is what NEC-2 is: thin wires, and a ground plane. Patches, slots,
horns and dishes (L13, and the reflector half of L14) are not thin-wire
problems and are deliberately absent rather than approximated badly -- see
README.
"""

from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Callable

from .model import Feed, Ground, Model, Wire, wavelength


@dataclass(frozen=True)
class Param:
    """One field in the builder form."""

    key: str
    label: str
    default: float | str
    unit: str = ""            # 'lambda', 'mm', 'MHz', 'count', 'deg', 'choice'
    choices: tuple[str, ...] = ()
    step: float = 0.005
    help: str = ""


@dataclass(frozen=True)
class AntennaType:
    key: str
    name: str
    lesson: str
    summary: str
    params: tuple[Param, ...]
    build: Callable[[dict], Model]


def _f(p: dict, key: str, default: float) -> float:
    try:
        return float(p.get(key, default))
    except (TypeError, ValueError):
        return default


def _i(p: dict, key: str, default: int) -> int:
    try:
        return int(float(p.get(key, default)))
    except (TypeError, ValueError):
        return default


def _odd(n: int) -> int:
    """Segment counts want to be odd so a center feed lands on a segment."""
    return n if n % 2 else n + 1


def _ground(p: dict) -> Ground:
    kind = str(p.get("ground", "perfect"))
    return Ground(kind if kind in ("free", "perfect", "real") else "perfect")


# ---------------------------------------------------------------- dipole ---

def build_dipole(p: dict) -> Model:
    freq = _f(p, "freq_mhz", 915.0)
    lam = wavelength(freq)
    length = _f(p, "length_lambda", 0.5) * lam
    return Model.dipole(freq, length, radius_m=_f(p, "radius_mm", 0.5) / 1000,
                        segments=_odd(_i(p, "segments", 21)),
                        comment=f"dipole, {freq:g} MHz")


# -------------------------------------------------------------- monopole ---

def build_monopole(p: dict) -> Model:
    """A vertical monopole standing on a ground plane, fed at its base.

    The base sits on z = 0 exactly. That is not a detail: lift it a tenth of a
    millimeter and NEC sees an open circuit rather than a monopole, and reports
    a huge capacitive reactance instead of an error.
    """
    freq = _f(p, "freq_mhz", 915.0)
    lam = wavelength(freq)
    height = _f(p, "height_lambda", 0.236) * lam
    segs = max(3, _i(p, "segments", 21))
    wire = Wire(1, segs, 0, 0, 0.0, 0, 0, height, _f(p, "radius_mm", 0.5) / 1000)
    return Model(wires=(wire,), feeds=(Feed(1, 1),), freq_mhz=freq,
                 comment=f"monopole over ground, {freq:g} MHz",
                 ground=_ground(p))


# ------------------------------------------------------------------ loop ---

def build_loop(p: dict) -> Model:
    """A closed loop in the x-y plane, approximated by a regular polygon.

    NEC-2 has no curve: a loop is a ring of straight wires, and the number of
    sides is the model's honesty about that. Twelve is plenty for a
    one-wavelength loop; a small loop needs fewer.
    """
    freq = _f(p, "freq_mhz", 915.0)
    lam = wavelength(freq)
    circumference = _f(p, "circumference_lambda", 1.0) * lam
    sides = max(3, _i(p, "sides", 12))
    ring = circumference / (2 * math.pi)
    a = _f(p, "radius_mm", 0.5) / 1000
    per_side = max(1, _i(p, "segments_per_side", 3))

    wires = []
    for k in range(sides):
        t0 = 2 * math.pi * k / sides
        t1 = 2 * math.pi * (k + 1) / sides
        wires.append(Wire(k + 1, per_side,
                          ring * math.cos(t0), ring * math.sin(t0), 0.0,
                          ring * math.cos(t1), ring * math.sin(t1), 0.0, a))
    # Fed at the middle of side 1, which is the usual place to break a loop.
    return Model(wires=tuple(wires),
                 feeds=(Feed(1, (per_side + 1) // 2),),
                 freq_mhz=freq,
                 comment=(f"{_f(p, 'circumference_lambda', 1.0):g} lambda loop, "
                          f"{sides} sides, {freq:g} MHz"))


# ------------------------------------------------------------------ yagi ---

def build_yagi(p: dict) -> Model:
    """Reflector, driven element, and N directors along a boom on the x axis.

    Elements are parallel to z, so the beam runs along +x, toward the
    directors. Only the driven element is fed; the rest are parasitic, which
    is the whole idea and the reason the impedance is nothing like a dipole's.
    """
    freq = _f(p, "freq_mhz", 915.0)
    lam = wavelength(freq)
    a = _f(p, "radius_mm", 0.5) / 1000
    segs = _odd(_i(p, "segments", 21))
    n_dir = max(0, _i(p, "directors", 1))
    refl_len = _f(p, "reflector_lambda", 0.482) * lam
    driv_len = _f(p, "driven_lambda", 0.475) * lam
    dir_len = _f(p, "director_lambda", 0.442) * lam
    refl_sp = _f(p, "reflector_spacing_lambda", 0.20) * lam
    dir_sp = _f(p, "director_spacing_lambda", 0.20) * lam

    def element(tag: int, x: float, length: float) -> Wire:
        return Wire(tag, segs, x, 0, -length / 2, x, 0, length / 2, a)

    wires = [element(1, -refl_sp, refl_len), element(2, 0.0, driv_len)]
    for k in range(n_dir):
        wires.append(element(3 + k, (k + 1) * dir_sp, dir_len))
    driven = wires[1]
    return Model(wires=tuple(wires),
                 feeds=(Feed(2, driven.center_segment),),
                 freq_mhz=freq,
                 comment=f"Yagi-Uda, {2 + n_dir} elements, {freq:g} MHz")


# ----------------------------------------------------------------- array ---

def build_array(p: dict) -> Model:
    """A driven array of dipoles: every element has its own source.

    The phase shift per element is what steers it, and the impedances that come
    back differ element to element. That difference is mutual coupling, and it
    is the gap between the array factor and the pattern NEC computes -- L22's
    subject, in the one tool that can show both.
    """
    freq = _f(p, "freq_mhz", 915.0)
    lam = wavelength(freq)
    n = max(1, _i(p, "elements", 4))
    spacing = _f(p, "spacing_lambda", 0.5) * lam
    length = _f(p, "length_lambda", 0.475) * lam
    a = _f(p, "radius_mm", 0.5) / 1000
    segs = _odd(_i(p, "segments", 21))
    phase_step = _f(p, "phase_deg", 0.0)

    wires, feeds = [], []
    span = (n - 1) * spacing
    for k in range(n):
        y = -span / 2 + k * spacing
        tag = k + 1
        wires.append(Wire(tag, segs, 0, y, -length / 2, 0, y, length / 2, a))
        phase = math.radians(phase_step * k)
        feeds.append(Feed(tag, wires[-1].center_segment,
                          math.cos(phase), math.sin(phase)))
    return Model(wires=tuple(wires), feeds=tuple(feeds), freq_mhz=freq,
                 comment=(f"{n}-element driven array, "
                          f"{_f(p, 'spacing_lambda', 0.5):g} lambda spacing, "
                          f"{phase_step:g} deg per element, {freq:g} MHz"))


FREQ = Param("freq_mhz", "Frequency", 915.0, "MHz", step=1)
RADIUS = Param("radius_mm", "Wire radius", 0.5, "mm", step=0.05)
SEGMENTS = Param("segments", "Segments per element", 21, "count", step=2)

TYPES: tuple[AntennaType, ...] = (
    AntennaType(
        "dipole", "Dipole", "L7-L8",
        "One wire, fed at the center. The lab's antenna.",
        (FREQ, Param("length_lambda", "Length", 0.5, "lambda"), RADIUS, SEGMENTS),
        build_dipole),
    AntennaType(
        "monopole", "Monopole over ground", "L12",
        "Half a dipole, fed against its image in the ground plane.",
        (FREQ, Param("height_lambda", "Height", 0.236, "lambda"), RADIUS,
         SEGMENTS,
         Param("ground", "Ground", "perfect", "choice",
               choices=("perfect", "real", "free"),
               help="'free' removes the ground: useful only to watch the "
                    "monopole stop working")),
        build_monopole),
    AntennaType(
        "loop", "Loop", "L12",
        "A closed loop in the x-y plane, as a polygon of straight wires.",
        (FREQ, Param("circumference_lambda", "Circumference", 1.0, "lambda"),
         Param("sides", "Sides", 12, "count", step=1),
         Param("segments_per_side", "Segments per side", 3, "count", step=1),
         RADIUS),
        build_loop),
    AntennaType(
        "yagi", "Yagi-Uda", "L14",
        "Driven element with a reflector behind and directors in front.",
        (FREQ, Param("directors", "Directors", 1, "count", step=1),
         Param("reflector_lambda", "Reflector length", 0.482, "lambda"),
         Param("driven_lambda", "Driven length", 0.475, "lambda"),
         Param("director_lambda", "Director length", 0.442, "lambda"),
         Param("reflector_spacing_lambda", "Reflector spacing", 0.20, "lambda"),
         Param("director_spacing_lambda", "Director spacing", 0.20, "lambda"),
         RADIUS, SEGMENTS),
        build_yagi),
    AntennaType(
        "array", "Driven array", "L16-L22",
        "Dipoles along y, each with its own source and its own phase.",
        (FREQ, Param("elements", "Elements", 4, "count", step=1),
         Param("spacing_lambda", "Spacing", 0.5, "lambda"),
         Param("length_lambda", "Element length", 0.475, "lambda"),
         Param("phase_deg", "Phase per element", 0.0, "deg", step=5),
         RADIUS, SEGMENTS),
        build_array),
)

BY_KEY = {t.key: t for t in TYPES}


def build(kind: str, params: dict) -> Model:
    if kind not in BY_KEY:
        raise KeyError(f"unknown antenna type {kind!r}; "
                       f"known: {', '.join(BY_KEY)}")
    return BY_KEY[kind].build(params)


def spec() -> list[dict]:
    """The whole catalog, as the page needs it."""
    return [{
        "key": t.key, "name": t.name, "lesson": t.lesson, "summary": t.summary,
        "params": [{"key": p.key, "label": p.label, "default": p.default,
                    "unit": p.unit, "choices": list(p.choices), "step": p.step,
                    "help": p.help} for p in t.params],
    } for t in TYPES]
