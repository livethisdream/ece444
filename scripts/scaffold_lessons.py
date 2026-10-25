#!/usr/bin/env python3
"""Scaffold lesson shells for every ECE 444 lesson.

For each lesson in the manifest that does not already exist, this writes:
  book/moduleNN/<slug>/index.md     material shell (title, LO list)

The reveal.js decks it used to write alongside were retired on 2026-10-23;
a frame lesson printed from present mode is the slide handout now.

It also rewrites book/_toc.yml from the manifest. Existing lesson index.md
files are left UNTOUCHED unless --force is passed, so hand-written
content (L1-L3, and any lesson you have since filled in) is safe to re-run
over. Every module landing page is now a hand-written frame page, so none of
them is generated -- the generator below still emits the pre-frame shape, and
running it over one would flatten the conversion.

The manifest is the single source of truth for the lesson -> LO mapping;
edit LESSONS below and re-run to change the scaffold.

Usage:
    python scripts/scaffold_lessons.py            # create missing shells + toc + module pages
    python scripts/scaffold_lessons.py --force     # also overwrite existing shells (careful!)
    python scripts/scaffold_lessons.py --dry-run    # print what would happen, write nothing
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
BOOK = REPO / "book"


# ---- Learning objectives, verbatim from the syllabus -----------------------
LO_TEXT = {
    "1.1": "I can define what an antenna is, articulate the reciprocity principle, and describe the role of an antenna in a wireless system.",
    "1.2": "I can define and calculate fundamental antenna properties: gain, directivity, effective aperture, beamwidth, and sidelobe level.",
    "1.3": "I can determine the polarization of an antenna and describe the bandwidth characteristics of common antenna types.",
    "1.4": "I can calculate input impedance, feed considerations, and the role of baluns in an antenna feed system.",
    "1.5": "I can identify and distinguish the reactive near-field, radiating near-field, and far-field regions and calculate the boundaries for a given antenna.",
    "1.6": "I can set up and interpret the radiation integrals to derive the far-field pattern of a current distribution.",
    "2.1": "I can describe the radiation behavior of simple resonant antennas (isotropic radiator, half-wave dipole, monopole, loop) and calculate their gain and impedance.",
    "2.2": "I can simulate a dipole antenna using an EM simulation tool and interpret the results against analytical predictions.",
    "2.3": "I can describe the radiation mechanism, pattern, and typical use cases for patch, slot, and horn antennas.",
    "2.4": "I can describe how reflectors, Yagi-Uda antennas, and arrays achieve high gain, explain how a log-periodic antenna trades gain for bandwidth, and select an appropriate high-gain antenna for a given application.",
    "2.5": "I can explain the theory behind antenna pattern measurement, including anechoic chambers, near-field to far-field transformations, and standard gain horns.",
    "2.6": "I can measure the impedance and S-parameters of an antenna using a vector network analyzer and interpret the results.",
    "2.7": "I can measure the radiation pattern of an antenna and extract gain, beamwidth, sidelobe level, and polarization from the data.",
    "3.1": "I can describe aperture distributions and calculate aperture efficiency for a given illumination.",
    "3.2": "I can derive the array factor for an arbitrary linear array and apply pattern multiplication.",
    "3.3": "I can identify the hardware architecture of the ADALM-PHASER and control it via SDR software.",
    "3.4": "I can calculate the phase weights required to steer a beam to a given angle and predict the resulting array pattern.",
    "3.5": "I can implement beam steering on the ADALM-PHASER and verify the steered pattern against theory.",
    "3.6": "I can distinguish between array factor and true antenna pattern and account for element pattern effects.",
    "3.7": "I can apply amplitude tapering (uniform, cosine, Chebyshev, Taylor) to control sidelobe level and predict the pattern trade-off.",
    "3.8": "I can identify grating lobes, beam squint, and quantization effects in a phased array and describe their impact on system performance.",
    "3.9": "I can calculate null-steering weights and implement pattern nulls on the ADALM-PHASER.",
    "4.1": "I can apply the radar equation to calculate received power for a given geometry, and account for path loss and radar cross section (RCS).",
    "4.2": "I can calculate range resolution, unambiguous range, and Doppler shift for a given radar waveform.",
    "4.3": "I can apply radar detection theory (PD, FAR, dwell time) to determine detection performance under noise.",
    "4.4": "I can describe FMCW radar operation and configure an FMCW waveform on the ADALM-PHASER.",
    "4.5": "I can process FMCW radar data to produce range, range-waterfall, and range-Doppler results.",
    "4.6": "I can implement moving target indication (MTI) processing to distinguish moving targets from clutter.",
    "4.7": "I can apply constant false-alarm rate (CFAR) processing to radar data and evaluate detection performance.",
    # 4.8 and 4.9 were 5.2 and 5.3 until Module 5 folded into Module 4
    # (Neil, 2026-10-15); 5.1 and 5.4 went with the capstone.
    "4.8": "I can integrate FMCW radar processing with a phased-array front-end to track a moving target.",
    "4.9": "I can classify a detected target from its micro-Doppler signature and report the classifier's accuracy.",
}

# ---- Module metadata -------------------------------------------------------
MODULES = {
    1: dict(
        caption="Module 1 — Foundations of Electromagnetics and Antennas",
        title="Module 1 — Antenna Fundamentals",
        los=["1.1", "1.2", "1.3", "1.4", "1.5", "1.6"],
        synopsis="Ground the physics. What an antenna is and why it matters, the chain from Maxwell's equations to the plane wave, the headline parameters (gain, directivity, effective area, beamwidth), impedance and feeding, field regions, and the radiation integrals.",
        generate_index=False,  # hand-written frame page; the generator predates frames
    ),
    2: dict(
        caption="Module 2 — Antenna Types, Simulation, and Measurement",
        title="Module 2 — Antenna Types, Simulation, and Measurement",
        los=["2.1", "2.2", "2.3", "2.4", "2.5", "2.6", "2.7"],
        synopsis="Move from theory to real antennas: the canonical families — dipoles, loops, monopoles, patches, slots, horns, reflectors, Yagis — and how we simulate and measure them. You'll simulate a dipole, then measure impedance and radiation patterns in the lab.",
        generate_index=False,  # hand-written frame page; the generator predates frames
    ),
    3: dict(
        caption="Module 3 — Arrays and ADALM-PHASER Beamforming",
        title="Module 3 — Arrays and ADALM-PHASER Beamforming",
        los=["3.1", "3.2", "3.3", "3.4", "3.5", "3.6", "3.7", "3.8", "3.9"],
        synopsis="Build beams from elements. Aperture distributions and the array factor, then hands-on beam steering, tapering, beam squint, and null steering on the ADALM-PHASER.",
        generate_index=False,  # hand-written frame page; the generator predates frames
    ),
    4: dict(
        caption="Module 4 — Radar Fundamentals and FMCW",
        title="Module 4 — Radar Fundamentals and FMCW",
        los=["4.1", "4.2", "4.3", "4.4", "4.5", "4.6", "4.7", "4.8", "4.9"],
        synopsis="From antennas to radar. The radar equation, range/Doppler/resolution, detection theory, and FMCW processing on the PHASER — range, range-Doppler, MTI, CFAR, and classifying and tracking what it finds. The L28-L31 Labs are the scaffolding for the final project report.",
        generate_index=False,  # hand-written frame page; the generator predates frames
    ),
}

# ---- Lab manifest: labs that hang off a lesson without taking a lesson number.
# Every lab in Modules 3-4 is one of these (2026-10-13): a lab is the bench
# half of its lesson, named "LNN Lab", and has no period number of its own.
# (module, anchor_lesson_slug, lab_slug, toc_title). The TOC lists each one
# directly after its anchor lesson. Lab pages are hand-written -- the scaffolder
# only places them in the TOC, it does not generate them.
LABS = [
    (1, "L04-impedance-feeding-baluns", "L04-lab-matching", "L4 Lab — Matching Procedures"),
    (3, "L17-phased-array-hardware", "L17-lab-bring-up", "L17 Lab — Phased Array Bring-Up"),
    (3, "L18-beam-steering", "L18-lab-beam-steering", "L18 Lab — Beam Steering"),
    (3, "L19-direction-finding", "L19-lab-fox-hunt", "L19 Lab — Fox Hunt"),
    (3, "L20-array-factor-beamwidth", "L20-lab-array-factor", "L20 Lab — Array Factor"),
    (3, "L21-antenna-pattern", "L21-lab-antenna-pattern", "L21 Lab — Antenna Pattern"),
    # One lab for L22 and L23 (Neil, 2026-10-13): it runs after Lesson 23, so it
    # hangs off L23. Part 1 is tapering (3.7), Part 2 the three departures (3.8).
    (3, "L23-beam-squint-quantization", "L22-L23-lab-tapering-squint", "L22–L23 Lab — Tapering, Squint, and Quantization"),
    (3, "L24-null-steering", "L24-lab-null-steering", "L24 Lab — Null Steering"),
    (4, "L28-fmcw", "L28-lab-fmcw-range", "L28 Lab — FMCW Range"),
    (4, "L29-range-doppler-mti", "L29-lab-range-doppler-mti", "L29 Lab — Range-Doppler and MTI"),
    (4, "L30-cfar", "L30-lab-cfar", "L30 Lab — CFAR Processing"),
    (4, "L31-classification-tracking", "L31-lab-spectrogram", "L31 Lab — Micro-Doppler Spectrogram"),
]

# Extra pages that sit after a lesson in the TOC but are NOT scaffolded --
# they are hand-authored and this list only places them in the nav.
#   (module, after-slug, slug, title)
EXTRA_PAGES = [
    # The final project is one report built on the L28-L31 Labs (Neil,
    # 2026-10-15); this page says so and sits after the last of them.
    (4, "L31-classification-tracking", "final-project", "Final Project — Radar Systems Report"),
]

# ---- Lesson manifest: (module, num, slug, title, [lo_ids], synopsis, has_practice)
LESSONS = [
    (1, 1, "L01-course-intro", "Course Introduction", ["1.1"], "What an antenna is, why antennas matter to the Air Force mission, and how ECE 444 is organized.", False),
    (1, 2, "L02-antenna-properties", "Basic Properties and Terminology", ["1.2"], "From Maxwell's equations to the plane wave; radiation intensity, directivity, gain, effective area, and pattern parameters.", True),
    (1, 3, "L03-polarization-bandwidth", "Polarization and Bandwidth", ["1.3"], "Linear, circular, and elliptical polarization; axial ratio and polarization loss; impedance / pattern / polarization bandwidth; Chu-Harrington.", True),
    (1, 4, "L04-impedance-feeding-baluns", "Impedance, Feeding, and Baluns", ["1.4"], "Input impedance, feed-point matching, and the role of baluns in an antenna feed system.", True),
    (1, 5, "L05-field-regions", "Field Regions", ["1.5"], "Reactive near-field, radiating near-field, and far-field — boundaries and why they matter.", False),
    (1, 6, "L06-radiation-integrals", "Radiation Integrals", ["1.6"], "Setting up the radiation integrals to get the far-field pattern from a current distribution.", False),

    (2, 7, "L07-simple-resonant-antennas", "Simple Resonant Antennas", ["2.1"], "Isotropic radiators and the half-wave dipole: pattern, gain, and impedance.", False),
    (2, 8, "L08-dipole-simulation-lab", "Dipole Simulation Lab", ["2.2"], "Simulate a dipole in an EM tool and compare against analytical predictions.", False),
    # The measurement block runs before the remaining antenna families so that
    # the midterm project is in cadets' hands as early as the calendar allows.
    (2, 9, "L09-pattern-measurement-theory", "Measurement Theory", ["2.5", "2.6"], "All the measurement theory in one place: ranges and chambers, what a VNA measures and how it is calibrated, gain by comparison, and dynamic range. Midterm project introduced.", False),
    (2, 10, "L10-measurement-lab-sparams", "Measurement Lab — Impedance and S-parameters", ["2.6"], "Measure impedance and S-parameters on a vector network analyzer.", False),
    (2, 11, "L11-measurement-lab-patterns", "Measurement Lab — Radiation Patterns", ["2.7"], "Measure a radiation pattern and extract gain, beamwidth, sidelobe level, and polarization.", False),
    (2, 12, "L12-loop-monopole-antennas", "Loop and Monopole Antennas", ["2.1"], "Small loops and monopoles: radiation behavior, gain, and impedance.", False),
    (2, 13, "L13-patch-slot-horn", "Patch, Slot, and Horn Antennas", ["2.3"], "Radiation mechanism, pattern, and use cases for patch, slot, and horn antennas.", False),
    (2, 14, "L14-high-gain-antennas", "High-Gain Antennas", ["2.4"], "Reflectors, Yagi-Uda, and arrays — how they get gain.", False),

    (3, 15, "L15-aperture-distributions", "Aperture Distributions and Efficiency", ["3.1"], "Aperture distributions and aperture efficiency for a given illumination.", False),
    (3, 16, "L16-array-factor", "The Array Factor and Pattern Multiplication", ["3.2"], "Array factor for a linear array and pattern multiplication.", False),
    (3, 17, "L17-phased-array-hardware", "Introduction to Phased Array Hardware", ["3.3"], "ADALM-PHASER architecture and SDR control.", False),
    (3, 18, "L18-beam-steering", "Beam Steering", ["3.4"], "Phase weights to steer a beam and the resulting array pattern.", False),
    # 2026-10-13 (Neil): lessons are topics, not class periods, and every lab
    # belongs to its lesson ("do the lesson in the time it takes, then do the
    # lab"). Labs are child pages in LABS below; project days and open-lab
    # slack are calendar, not lessons. Modules 1-2 keep their numbers.
    (3, 19, "L19-direction-finding", "Direction Finding", ["3.5"], "Bearings from the beam sweep, crossed from known positions: triangulation and how the crossing angle sets the error.", False),
    (3, 20, "L20-array-factor-beamwidth", "Array Factor and Beamwidth", ["3.2"], "Array factor and beamwidth in depth.", False),
    (3, 21, "L21-antenna-pattern", "Antenna Pattern", ["3.6"], "True antenna pattern vs. array factor; element-pattern effects.", False),
    (3, 22, "L22-sidelobes-tapering", "Sidelobes and Tapering", ["3.7"], "Amplitude tapering (uniform, cosine, Chebyshev, Taylor) and the sidelobe trade-off.", False),
    (3, 23, "L23-beam-squint-quantization", "Beam Squint and Quantization", ["3.8"], "Grating lobes, beam squint, and phase-quantization effects on array performance.", False),
    (3, 24, "L24-null-steering", "Null Steering", ["3.9"], "Null-steering weights and pattern nulls.", False),

    (4, 25, "L25-radar-equation", "The Radar Equation, Path Loss, and RCS", ["4.1"], "Radar equation, path loss, and radar cross section.", False),
    (4, 26, "L26-range-resolution-doppler", "Range, Resolution, and Doppler", ["4.2"], "Range resolution, unambiguous range, Doppler shift, and radar types.", False),
    (4, 27, "L27-radar-detection", "Radar Detection", ["4.3"], "Detection theory: probability of detection, false-alarm rate, and dwell time under noise.", False),
    (4, 28, "L28-fmcw", "FMCW on the Phaser", ["4.4"], "FMCW operation and configuring an FMCW waveform on the PHASER.", False),
    (4, 29, "L29-range-doppler-mti", "Range-Doppler and MTI", ["4.5", "4.6"], "Range-Doppler processing of a burst of chirps, and MTI to separate movers from clutter.", False),
    (4, 30, "L30-cfar", "CFAR Processing", ["4.7"], "Constant false-alarm-rate processing.", False),
    (4, 31, "L31-classification-tracking", "Classification and Tracking", ["4.8", "4.9"], "Micro-Doppler classification and range and angle tracking.", False),

]


def obj_label(lo_ids):
    if len(lo_ids) == 1:
        return f"objective {lo_ids[0]}"
    return "objectives " + ", ".join(lo_ids)


def lesson_index_md(num, title, lo_ids, slug):
    lo_items = "\n".join(f"  <li>{LO_TEXT[i]}</li>" for i in lo_ids)
    return f"""# L{num} - {title}

## Learning outcomes

By the end of this lesson, you will be able to:

<ol class="lo-list" style="--module: '{num}'">
{lo_items}
</ol>

---

```{{note}}
Lesson material is under construction. This shell maps to {obj_label(lo_ids)}.
```
"""



def module_index_md(mnum):
    m = MODULES[mnum]
    lessons = [x for x in LESSONS if x[0] == mnum]
    lo_start, lo_end = lessons[0][1], lessons[-1][1]
    lo_items = "\n".join(f"  <li>{LO_TEXT[i]}</li>" for i in m["los"])
    cards = []
    for (_, num, slug, title, lo_ids, synopsis, _hp) in lessons:
        cards.append(
            f"""  <a class="mt-card mt-lesson" href="{slug}/index.html">
    <span class="mt-kind">Lesson {num}</span>
    <h4>{title}</h4>
    <p>{synopsis} {obj_label(lo_ids).capitalize()}.</p>
  </a>"""
        )
    cards_md = "\n".join(cards)
    return f"""# {m['title']}

<p class="module-meta"><span class="m-module">Module {mnum:02d}</span><span class="m-time">Lessons {lo_start}–{lo_end}</span></p>

<p class="module-synopsis">{m['synopsis']}</p>

## Learning Objectives

<ol class="lo-list" style="--module: '{mnum}'">
{lo_items}
</ol>

## Module Lessons

<div class="module-toc">
{cards_md}
</div>
"""


def toc_yaml():
    lines = [
        "# Table of contents for ECE 444.",
        "# Generated by scripts/scaffold_lessons.py from the LESSONS manifest.",
        "# Re-run that script after editing the manifest; hand edits here will be overwritten.",
        "",
        "format: jb-book",
        "root: intro",
        "",
        "parts:",
        "  - caption: Course Information",
        "    chapters:",
        "      - file: syllabus",
        "      - file: materials",
        "      - file: interactives",
    ]
    for mnum, m in MODULES.items():
        lines.append("")
        lines.append(f"  - caption: {m['caption']}")
        lines.append("    chapters:")
        lines.append(f"      - file: module{mnum:02d}/index")
        lines.append(f"        title: Module {mnum} overview")
        for (_, num, slug, title, lo_ids, _syn, has_practice) in [x for x in LESSONS if x[0] == mnum]:
            lines.append(f"      - file: module{mnum:02d}/{slug}/index")
            lines.append(f'        title: "L{num} — {title}"')
            # Practice is served as linked PDFs from the lesson page itself --
            # there are no practice.md / practice-solutions.md pages to list.
            for (lmnum, anchor, lslug, ltitle) in LABS + EXTRA_PAGES:
                if lmnum == mnum and anchor == slug:
                    lines.append(f"      - file: module{mnum:02d}/{lslug}/index")
                    lines.append(f'        title: "{ltitle}"')
    return "\n".join(lines) + "\n"


def write(path: Path, content: str, force: bool, dry: bool, kind: str):
    exists = path.exists()
    if exists and not force:
        print(f"  skip (exists): {path.relative_to(REPO)}")
        return False
    action = "overwrite" if exists else "write"
    print(f"  {action} {kind}: {path.relative_to(REPO)}")
    if not dry:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")
    return True


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--force", action="store_true", help="overwrite existing lesson shells")
    ap.add_argument("--dry-run", action="store_true", help="print actions, write nothing")
    args = ap.parse_args()
    force, dry = args.force, args.dry_run

    print("== Lesson shells (index.md) ==")
    for (mnum, num, slug, title, lo_ids, _syn, _hp) in LESSONS:
        idx = BOOK / f"module{mnum:02d}" / slug / "index.md"
        write(idx, lesson_index_md(num, title, lo_ids, slug), force, dry, "index")

    print("== Module landing pages ==")
    for mnum, m in MODULES.items():
        if not m.get("generate_index"):
            print(f"  skip module {mnum} index (hand-written)")
            continue
        write(BOOK / f"module{mnum:02d}" / "index.md", module_index_md(mnum), True, dry, "module-index")

    print("== _toc.yml ==")
    write(BOOK / "_toc.yml", toc_yaml(), True, dry, "toc")

    print("done.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
