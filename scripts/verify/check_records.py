#!/usr/bin/env python3
"""Do a lab page's entry boxes match the fields in the packet they fill?

A lab page's Part 2 boxes (``<input data-field="b.ping">`` inside a
``.rec[data-lab]`` block) are written by records.js into the blank packet's
AcroForm fields of the same names, which the faculty LaTeX creates with
``\\kv[b.ping]{...}``. Nothing ties the two together but the names, and a
name that drifts on either side fails silently: the box saves, the download
succeeds, and the value is simply missing from the PDF. This reads every
built page that carries a ``.rec-summary``, opens the PDF its ``data-pdf``
points at, and fails if any field the page asks for is not in it. Field
names the PDF has and the page does not use are listed, not failed: Part 1
and Part 3 cells are fillable in the PDF without having a box on the page.

    python3 scripts/verify/check_records.py            # every lab page
    python3 scripts/verify/check_records.py L17        # pages matching L17

Run it after `jupyter-book build book/ --all`; it reads book/_build/html.
"""

from __future__ import annotations

import re
import sys
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
HTML = ROOT / "book" / "_build" / "html"


class Scan(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.depth = []            # stack of lab names for open .rec divs
        self.fields: dict[str, list[str]] = {}
        self.summaries: list[tuple[str, str]] = []

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        cls = (a.get("class") or "").split()
        if tag == "div":
            if "rec-summary" in cls and a.get("data-lab"):
                self.summaries.append((a["data-lab"], a.get("data-pdf", "")))
            self.depth.append(a.get("data-lab") if "rec" in cls else None)
        elif tag == "input" and a.get("data-field"):
            lab = next((x for x in reversed(self.depth) if x), None)
            if lab:
                self.fields.setdefault(lab, []).append(a["data-field"])

    def handle_endtag(self, tag):
        if tag == "div" and self.depth:
            self.depth.pop()


def pdf_fields(path: Path) -> set[str]:
    from pypdf import PdfReader
    return set((PdfReader(str(path)).get_fields() or {}).keys())


def main(argv: list[str]) -> int:
    if not HTML.is_dir():
        print(f"no build at {HTML}; run jupyter-book build book/ --all first")
        return 2
    pat = argv[1] if len(argv) > 1 else ""
    pages = [p for p in sorted(HTML.rglob("index.html")) if pat in str(p)]
    checked = failed = 0
    for page in pages:
        text = page.read_text(encoding="utf-8", errors="replace")
        if "rec-summary" not in text:
            continue
        s = Scan()
        s.feed(text)
        for lab, rel in s.summaries:
            rel_page = page.relative_to(HTML)
            pdf = (page.parent / rel).resolve()
            want = s.fields.get(lab, [])
            dupes = sorted({f for f in want if want.count(f) > 1})
            if not pdf.is_file():
                print(f"FAIL {rel_page} [{lab}]: data-pdf {rel} does not exist")
                failed += 1
                continue
            have = pdf_fields(pdf)
            missing = sorted(set(want) - have)
            unused = sorted(f for f in have - set(want) if not re.fullmatch(r"kv\d+", f))
            checked += 1
            status = "FAIL" if missing else "ok  "
            print(f"{status} {rel_page} [{lab}]: {len(set(want))} boxes, "
                  f"{len(have)} PDF fields ({pdf.name})")
            if missing:
                failed += 1
                print(f"       not in the PDF: {', '.join(missing)}")
            if dupes:
                print(f"       boxes repeated on the page (fine if intended): {', '.join(dupes)}")
            if unused:
                print(f"       named PDF fields with no box on the page: {', '.join(unused)}")
    if not checked and not failed:
        print("no page with a .rec-summary matched" + (f" '{pat}'" if pat else ""))
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
