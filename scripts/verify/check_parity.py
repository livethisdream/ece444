#!/usr/bin/env python3
"""Did a layout change quietly drop content? Diff this build against a baseline.

The failure this exists for is silent: a template or CSS change that renders
53 pages beautifully and loses a learning objective, a table, or half a
callout on one of them. Nothing errors. Reading the pages does not scale.

    # make a baseline from whatever you are changing FROM
    git worktree add /tmp/base main
    (cd /tmp/base && jupyter-book build book/ --all)

    scripts/verify/check_parity.py /tmp/base/book/_build/html

Every page present in both builds is compared on the rendered text of its
content region and on a count of the components that carry the teaching:
callouts, two-column blocks, LO lists, module TOCs, math nodes, tables. Any
page that differs is named, with the first divergence quoted.

Pages you MEANT to rewrite will show up here. That is the point -- the list
should be exactly the pages you touched, and you should read the diff for each.

Prints the number of pages compared. A run that compares zero pages is a
failure, not a pass: this check was silently vacuous once, when the content
region of a new template did not match any of the patterns below.
"""
import pathlib
import re
import sys

#: The content region, per template. The theme wraps content in <article>; the
#: shell's reading pages in <main class="page">, its frame lessons in
#: <main class="deck">. A build being compared can use any of them.
REGIONS = (
    r'<article[^>]*>(.*?)</article>',
    r'<main[^>]*class="[^"]*\b(?:page|deck)\b[^"]*"[^>]*>(.*?)</main>',
)

#: Counted, not just present: losing one of eight callouts matters as much as
#: losing the only one.
COMPONENTS = ("callout", "two-col", "lo-list", "module-toc", "admonition",
              "math notranslate", "fig ", "headerlink")

#: Neither is a book page: one is a redirect stub, the other is generated.
SKIP_NAMES = {"genindex.html", "search.html"}


def region(html):
    for pat in REGIONS:
        m = re.search(pat, html, re.S)
        if m:
            return m.group(1)
    return None


def words(frag):
    t = re.sub(r'<(script|style)[^>]*>.*?</\1>', ' ', frag, flags=re.S)
    t = re.sub(r'<[^>]+>', ' ', t)
    t = t.replace('&#182;', ' ').replace('¶', ' ').replace('&amp;', '&')
    return re.sub(r'\s+', ' ', t).strip()


def profile(frag):
    return {c: frag.count(c) for c in COMPONENTS}


def main():
    if len(sys.argv) != 2:
        print(__doc__.strip().splitlines()[0])
        print(f"usage: {sys.argv[0]} <baseline html dir>", file=sys.stderr)
        return 2
    base = pathlib.Path(sys.argv[1]).resolve()
    new = pathlib.Path(__file__).resolve().parents[2] / "book" / "_build" / "html"
    if not base.is_dir():
        print(f"FAIL: baseline {base} is not a directory", file=sys.stderr)
        return 2

    bad, checked, skipped = [], 0, []
    for src in sorted(base.rglob("*.html")):
        rel = src.relative_to(base)
        if src.name in SKIP_NAMES:
            continue
        dst = new / rel
        if not dst.exists():
            bad.append((str(rel), "MISSING from this build"))
            continue
        fa, fb = region(src.read_text()), region(dst.read_text())
        if fa is None or fb is None:
            # Raw passthrough files -- decks, widgets, theme partials. They have
            # no content region in either build and are not pages.
            skipped.append(str(rel))
            continue
        checked += 1
        wa, wb = words(fa), words(fb)
        if wa != wb:
            i = next((k for k in range(min(len(wa), len(wb))) if wa[k] != wb[k]),
                     min(len(wa), len(wb)))
            bad.append((str(rel), f"TEXT differs at char {i}:\n"
                                  f"        base: …{wa[max(0, i - 60):i + 60]!r}\n"
                                  f"         new: …{wb[max(0, i - 60):i + 60]!r}"))
            continue
        pa, pb = profile(fa), profile(fb)
        diff = {k: (pa[k], pb[k]) for k in pa if pa[k] != pb[k]}
        if diff:
            bad.append((str(rel), f"COMPONENTS differ: {diff}"))

    print(f"compared {checked} pages ({len(skipped)} non-pages skipped)")
    if not checked:
        print("\nFAIL: zero pages compared. Neither build's content region "
              "matched, so this proved nothing -- check REGIONS above against "
              "the templates in play.")
        return 1
    if bad:
        print(f"\n{len(bad)} PAGES DIFFER:")
        for rel, why in bad:
            print(f"  {rel}\n      {why}")
        return 1
    print("every page identical in text and component counts")
    return 0


if __name__ == "__main__":
    sys.exit(main())
