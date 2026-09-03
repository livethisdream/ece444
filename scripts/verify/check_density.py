#!/usr/bin/env python3
"""How much a frame page puts on screen in present mode, from its source.

Two budgets, both Neil's (2026-09-03): a present frame carries at most
WORDS words, and a lesson has at most FRAMES present frames -- one 53-minute
period. Measured on the lesson pages the day the rule was set, the median
frame carried 55-93 words and the lessons ran 28-76 frames, so the whole
site fails it. That is the point: this check is the gate for the re-cut, not
a description of the site as it stands.

What counts as "on screen" follows _ext/frames.py:

* a frame with `:::{present}` blocks shows only those (a CUT frame);
* a frame without any shows everything outside `:::{depth}` (LEGACY);
* a frame marked `:class: read-only` is not shown at all, and is not a beat.

Static, on the markdown: no build and no browser, so it runs in a second and
can sit in an editor loop. Display math counts as nothing (an equation is not
words) and inline math as one word. The LO frame is exempt from the word
budget by convention -- three "I can" sentences are the lesson's contract and
belong on screen whole.

Exit status: a lesson that has opted in (any present block) FAILS when a
frame is over WORDS or the lesson is over FRAMES. A lesson with no present
block is reported and passes: it has not been cut yet, and failing every
un-cut lesson would make the gate say nothing.

    check_density.py                 # every frame page, one line each
    check_density.py L05             # one lesson, frame by frame
    check_density.py --strict L05    # fail an un-cut lesson too
"""
import pathlib
import re
import sys

REPO = pathlib.Path(__file__).resolve().parents[2]
BOOK = REPO / "book"

WORDS = 40
FRAMES = 30

_FRAME_OPEN = re.compile(r"^::::\{frame\}(.*)$", re.M)
_OPT = re.compile(r"^:(\w[\w-]*):\s*(.*)$")


def _blocks(body, name):
    """Yield the bodies of the `:::{name}` blocks in a frame body."""
    out = []
    pat = re.compile(r"^:::\{%s\}[^\n]*\n(.*?)^:::\s*$" % name, re.M | re.S)
    for m in pat.finditer(body):
        inner = m.group(1)
        # drop option lines at the top of the block
        lines = inner.split("\n")
        while lines and _OPT.match(lines[0]):
            lines.pop(0)
        out.append("\n".join(lines))
    return out


def _strip_blocks(body, name):
    pat = re.compile(r"^:::\{%s\}[^\n]*\n.*?^:::\s*$" % name, re.M | re.S)
    return pat.sub(" ", body)


def words(text):
    """Count what a reader sees as words. Markup, math and HTML are not words."""
    text = re.sub(r"<[^>]+>", " ", text)                # HTML tags
    text = re.sub(r"\$\$.*?\$\$", " ", text, flags=re.S)  # display math: 0
    text = re.sub(r"\$[^$\n]+\$", " EQ ", text)          # inline math: 1
    text = re.sub(r"^\s*\|?\s*:?-+:?\s*(\|\s*:?-+:?\s*)*\|?\s*$", " ", text, flags=re.M)  # table rules
    text = re.sub(r"^:[\w-]+:.*$", " ", text, flags=re.M)  # directive options
    text = re.sub(r"[|*_`#>\[\]()]", " ", text)
    return len([w for w in text.split() if re.search(r"[A-Za-z0-9]", w)])


def frames_of(src):
    """Split a page into frames: (title, classes, body) in document order."""
    out = []
    for m in _FRAME_OPEN.finditer(src):
        start = m.end()
        end = src.find("\n::::\n", start)
        if end < 0:
            end = src.find("\n::::", start)
        body = src[start:end] if end >= 0 else src[start:]
        title = m.group(1).strip()
        classes = []
        lines = body.split("\n")
        # options sit on the lines right after the opener (after the title line)
        i = 0
        while i < len(lines) and (not lines[i].strip() or _OPT.match(lines[i])):
            om = _OPT.match(lines[i])
            if om and om.group(1) == "class":
                classes += om.group(2).split()
            i += 1
        out.append((title, classes, "\n".join(lines[i:])))
    return out


def measure(path):
    src = path.read_text(encoding="utf-8")
    rows = []
    for title, classes, body in frames_of(src):
        if "read-only" in classes:
            rows.append(dict(title=title, kind="read-only", words=0, shown=False))
            continue
        present = _blocks(body, "present")
        if present:
            n = sum(words(b) for b in present)
            kind = "cut"
        else:
            n = words(_strip_blocks(body, "depth"))
            kind = "legacy"
        exempt = "lo-list" in body
        rows.append(dict(title=title or "(title frame)", kind=kind, words=n,
                         shown=True, exempt=bool(exempt)))
    return rows


def report(path, rows, verbose, strict):
    shown = [r for r in rows if r["shown"]]
    cut = [r for r in shown if r["kind"] == "cut"]
    opted = bool(cut)
    over = [r for r in shown if r["words"] > WORDS and not r.get("exempt")]
    legacy = [r for r in shown if r["kind"] == "legacy"]
    name = path.relative_to(BOOK).parts[1] if len(path.relative_to(BOOK).parts) > 2 else path.parent.name
    fail = (opted or strict) and (over or len(shown) > FRAMES)
    flag = "FAIL" if fail else ("ok  " if opted else "uncut")
    line = (f"{flag} {name:<34} beats {len(shown):>3}/{FRAMES}  cut {len(cut):>3}  "
            f"legacy {len(legacy):>3}  over-{WORDS}w {len(over):>3}")
    print(line)
    if verbose:
        for i, r in enumerate(rows, 1):
            mark = "  " if r["shown"] and r["words"] <= WORDS else ("--" if not r["shown"] else "!!")
            if r.get("exempt") and r["words"] > WORDS:
                mark = "LO"
            print(f"   {mark} {i:>2} {r['kind']:<9} {r['words']:>3}w  {r['title'][:56]}")
        if len(shown) > FRAMES:
            print(f"   !! {len(shown)} present frames; the budget is {FRAMES}")
    return not fail


def main(argv):
    strict = "--strict" in argv
    args = [a for a in argv if not a.startswith("--")]
    want = args[0] if args else ""
    pages = sorted(p for p in BOOK.glob("module*/*/index.md")
                   if want in p.as_posix() and "frame_view: true" in p.read_text(encoding="utf-8"))
    if not pages:
        print(f"no frame page matched {want!r} -- nothing was checked")
        return 1
    ok = True
    for p in pages:
        ok = report(p, measure(p), verbose=bool(want), strict=strict) and ok
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
