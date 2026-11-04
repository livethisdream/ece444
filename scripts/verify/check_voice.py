#!/usr/bin/env python3
"""The mechanical half of VOICE.md and CLAUDE.md's prose rules, as a check.

The voice, why, and illustration sweeps used to find these by grep after a
lesson was written (Neil, 2026-11-04: "why not just build those rules into
the creation of lessons?"). The decidable ones live here instead, so a draft
meets them before anyone reads it and CI holds every PR to them.

FAIL (each one a rule Neil has stated):
  hedge        vouching words, VOICE 2 and 20: honest, genuinely, truly,
               rigorous, hand-waving, "is the price", "dear reader"
  third-person "instructor" in prose, VOICE 25 ("I NEVER speak or write in
               3rd person"); headings such as the syllabus's are labels
  british      colour, centre, grey, doughnut, -ise spellings (CLAUDE.md,
               "American spelling, everywhere"); file names are exempt
  thin-space   U+2009 anywhere (CLAUDE.md: "No thin spaces")
  math-space   \\, or \\; in a page's math; use "\\ " (CLAUDE.md, pages only)
  lo-math      $...$ inside the raw-HTML objectives list, which MathJax never
               sees (CLAUDE.md gotcha)
  table-pipe   | inside $...$ on a table row, which splits the cell; use \\vert

WARN (read each one; a regex cannot decide them):
  passive      VOICE 9's passive tells
  money        VOICE 20's money metaphors (buys, costs, pays, price, ...)

    check_voice.py L18                     every page and practice set of L18
    check_voice.py book/module03/L18-beam-steering/index.md
    check_voice.py --added-since origin/main
                                           only the lines a branch adds (CI)
    check_voice.py                         the whole book, a report
    check_voice.py -q ...                  FAIL lines only (CI)

A course can demote a rule to WARN in scripts/verify/voice_rules.json,
{"warn_only": ["third-person"], "why": "..."}: ECE 343 is co-taught, so
"your instructor" there names either of two people, not Neil in the third
person. The file is optional; with none, every FAIL rule fails.

Exit 1 if any FAIL. The whole book was brought to 0 FAIL when this landed
(2026-11-04), so CI runs it over every page; --added-since is there for a
branch that wants to see only its own lines.
"""

from __future__ import annotations

import glob
import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

FAIL = {
    "hedge": re.compile(r"\b(honest(ly)?|genuinely|truly|rigorous(ly)?|hand-?wav\w*|dear reader)\b"
                        r"|\bis the price\b", re.I),
    "third-person": re.compile(r"(?<![A-Za-z])instructor", re.I),
    "british": re.compile(r"[\w.]*(colour|centre|grey|doughnut)[\w.]*"
                          r"|\b(organi|recogni|optimi|minimi|maximi|normali|characteri|reali|utili|summari|emphasi)"
                          r"s(e|ed|es|ing|ation)\b", re.I),
    "thin-space": re.compile(" "),
}
MD_ONLY = {"math-space": re.compile(r"\\[,;](?![A-Za-z])")}
WARN = {
    "passive": re.compile(r"\b(is|are|was|were|be|been) +\w+(ed|en)\b"),
    "money": re.compile(r"\b(buy|buys|bought|pay|pays|price|costs?|spend|cheap|free lunch|for free)\b", re.I),
}
_CFG = Path(__file__).with_name("voice_rules.json")
WARN_ONLY = set(json.loads(_CFG.read_text())["warn_only"]) if _CFG.is_file() else set()
INLINE_MATH = re.compile(r"(?<![\\$])\$(?!\$)(.+?)(?<!\\)\$")


def is_filename(token: str) -> bool:
    return "_" in token or "." in token


def line_hits(path: str, n: int, line: str, lo_lines: set[int]):
    md = path.endswith(".md")
    if md and line.lstrip().startswith("#"):          # a heading is a label
        rules = {k: v for k, v in FAIL.items() if k != "third-person"}
    else:
        rules = dict(FAIL)
    if md:
        rules.update(MD_ONLY)
    for name, rx in rules.items():
        for m in rx.finditer(line):
            if name == "british" and is_filename(m.group(0)):
                continue
            yield ("WARN" if name in WARN_ONLY else "FAIL"), name, m.group(0)
            break
    if md and n in lo_lines and "$" in line:
        yield "FAIL", "lo-math", line.strip()[:40]
    if md and line.lstrip().startswith("|"):
        for m in INLINE_MATH.finditer(line):
            if "|" in m.group(1):
                yield "FAIL", "table-pipe", m.group(0)[:40]
                break
    for name, rx in WARN.items():
        m = rx.search(line)
        if m:
            yield "WARN", name, m.group(0)


def lo_block_lines(text: str) -> set[int]:
    out = set()
    for m in re.finditer(r'<ol class="lo-list".*?</ol>', text, re.S):
        a = text.count("\n", 0, m.start()) + 1
        b = text.count("\n", 0, m.end()) + 1
        out.update(range(a, b + 1))
    return out


def targets(args: list[str]) -> list[str]:
    if not args:
        md = [p for p in glob.glob(str(ROOT / "book/**/*.md"), recursive=True) if "/_build/" not in p]
        return sorted(md) + sorted(glob.glob(str(ROOT / "latex/ECE*_Practice_L*.tex")))
    out = []
    for a in args:
        m = re.fullmatch(r"L(\d+)", a)
        if m:
            nn = int(m.group(1))
            out += glob.glob(str(ROOT / f"book/module*/L{nn:02d}-*/index.md"))
            out += glob.glob(str(ROOT / f"latex/ECE*_Practice_L{nn:02d}.tex"))
        else:
            out.append(str((ROOT / a) if not Path(a).is_absolute() else Path(a)))
    return sorted(set(out))


def added_lines(ref: str) -> dict[str, set[int]]:
    diff = subprocess.run(["git", "-C", str(ROOT), "diff", "-U0", "--no-color", f"{ref}...HEAD", "--",
                           "book/*.md", "book/**/*.md", "latex/ECE*_Practice_L*.tex"],
                          capture_output=True, text=True, check=True).stdout
    out: dict[str, set[int]] = {}
    cur = None
    for line in diff.splitlines():
        if line.startswith("+++ "):
            cur = None if line.endswith("/dev/null") else str(ROOT / line[6:])
        elif line.startswith("@@") and cur:
            m = re.search(r"\+(\d+)(?:,(\d+))?", line)
            start, count = int(m.group(1)), int(m.group(2) or 1)
            out.setdefault(cur, set()).update(range(start, start + count))
    return out


def main(argv: list[str]) -> int:
    quiet = "-q" in argv
    argv = [a for a in argv if a != "-q"]
    only: dict[str, set[int]] | None = None
    if argv[:1] == ["--added-since"]:
        if len(argv) < 2:
            print("usage: check_voice.py --added-since <ref>")
            return 2
        only = added_lines(argv[1])
        files = sorted(p for p in only if "/_build/" not in p)
    else:
        files = targets(argv)
    fails = warns = 0
    for path in files:
        p = Path(path)
        if not p.is_file():
            continue
        text = p.read_text(encoding="utf-8")
        lo = lo_block_lines(text) if path.endswith(".md") else set()
        rel = p.relative_to(ROOT)
        for n, line in enumerate(text.splitlines(), 1):
            if only is not None and n not in only.get(path, ()):
                continue
            for level, rule, hit in line_hits(path, n, line, lo):
                if level == "FAIL":
                    fails += 1
                else:
                    warns += 1
                    if quiet:
                        continue
                print(f"{level} {rel}:{n} [{rule}] {hit!r}")
    scope = f"lines added since {argv[1]}" if only is not None else f"{len(files)} file(s)"
    print(f"check_voice: {fails} FAIL, {warns} WARN in {scope}")
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
