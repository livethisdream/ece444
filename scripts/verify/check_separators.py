#!/usr/bin/env python3
"""Find reveal.js slide separators that will not fire.

The deck wrapper configures data-separator="^\\r?\\n---\\r?\\n$". Read that
regex carefully: `^` `\\r?\\n` requires the line before `---` to be EMPTY, and
the trailing `\\r?\\n` `$` requires the line after it to be empty too. So a
separator only fires with a blank line on BOTH sides.

Missing either one is silent. Markdown renders the `---` as an <hr> (or, with
no blank line before it, as a setext underline that turns the previous line
into an <h2>), the build says nothing, and two slides merge into one. The
merge also drags the first slide's speaker notes into the visible body,
because reveal splits notes off a section only once.

    scripts/verify/check_separators.py [slug ...]     (default: every deck)
"""
import sys, pathlib, re

SLIDES = pathlib.Path(__file__).resolve().parents[2] / "book/extras/slides"


def check(path):
    lines = path.read_text().splitlines()
    bad = []
    for i, ln in enumerate(lines):
        if ln.strip() != "---" or ln != "---":
            continue                      # indented/decorated rules are not separators
        if i == 0:
            continue
        before_ok = lines[i - 1] == ""
        after_ok = i + 1 < len(lines) and lines[i + 1] == ""
        if before_ok and after_ok:
            continue
        why = []
        if not before_ok:
            why.append(f"no blank line before (prev: {lines[i - 1][:46]!r})")
        if not after_ok:
            nxt = lines[i + 1] if i + 1 < len(lines) else "<end of file>"
            why.append(f"no blank line after (next: {nxt[:46]!r})")
        bad.append((i + 1, "; ".join(why)))
    return bad


def main():
    slugs = sys.argv[1:]
    decks = ([SLIDES / f"{s}.md" for s in slugs] if slugs
             else sorted(SLIDES.glob("L*.md")))
    total = 0
    for d in decks:
        if not d.exists():
            print(f"FAIL: {d} not found"); return 2
        bad = check(d)
        if bad:
            total += len(bad)
            print(f"\n{d.name}: {len(bad)} separator(s) will not fire")
            for ln, why in bad:
                print(f"  line {ln}: {why}")
    if total:
        print(f"\nFAIL: {total} dead separator(s). Every '---' needs a blank line above AND below.")
        return 1
    print(f"PASS: every '---' in {len(decks)} deck(s) is a live separator")
    return 0


if __name__ == "__main__":
    sys.exit(main())
