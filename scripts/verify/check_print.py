#!/usr/bin/env python3
"""A frame page and a reading page must both print as more than one sheet,
and a frame page printed from present mode must be a slide-only handout.

`.deck` is a fixed-height scroll container so present mode can pin one frame
per viewport -- exactly what `@media print` saw before frames.css carried a
print block: one clipped viewport, the whole lesson on a single sheet, the
bottom bar stamped on top of it. This renders each page to PDF the way a
browser's print dialog would (Playwright's `page.pdf()` always uses the
`print` media type) and counts pages with `pdfinfo`.

A frame page must print at least one sheet per `.frame` -- `break-after: page`
in frames.css is what does that, and a page count of 1 for a multi-frame
lesson means the deck is still clipped to a single viewport. A reading page
long enough to matter must print to more than one sheet -- a page count of 1
there means `.page`'s natural document flow got trapped in a fixed-height
box, or the bar/overlay chrome ate the only sheet whole.

    check_print.py                       # every printable page in the book
    check_print.py L05-field-regions    # only pages whose path contains this
"""
import pathlib
import subprocess
import sys
import tempfile

sys.path.insert(0, str(pathlib.Path(__file__).parent))
from _common import REPO, launch, make_cdn_router, require_vendored, serve  # noqa: E402
from playwright.sync_api import sync_playwright  # noqa: E402

ROOT = REPO / "book" / "_build" / "html"

# Same top-level exclusions as check_frames.py, plus the one page that never
# went through frame.html/page.html at all: the site-root index.html is a bare
# meta-refresh to intro.html, nothing to render. Every other index.html is a
# lesson's own page and stays. genindex.html is Sphinx's own theme, skipped
# automatically below by DOM (no #deck, no #page) rather than by name.
EXCLUDE_TOP = {"slides", "viz", "frames", "_static"}
SKIP_RELATIVE = {"index.html"}

# A reading page below this many characters of body text (search.html has 4;
# materials.html, mostly a table of links, has ~1500) is not "a long reading
# page" -- it may legitimately fit on one sheet, so it is rendered and counted
# but not held to the >1-page requirement.
LONG_TEXT_CHARS = 5000

# A frame page printed from present mode is the slide handout that replaced
# the reveal.js decks' ?print-pdf (2026-10-23): title and present blocks only,
# one frame a sheet. Nothing of the depth and no read-only frame may reach the
# paper, or the handout is the whole lesson again.
HANDOUT = """() => {
  document.documentElement.setAttribute('data-mode', 'present');
  const shown = el => getComputedStyle(el).display !== 'none' && el.getClientRects().length > 0;
  const frames = [...document.querySelectorAll('.frame')];
  return {
    slides: frames.filter(f => !f.classList.contains('read-only')).length,
    depth: [...document.querySelectorAll('.frame .depth')].filter(shown).length,
    readOnly: frames.filter(f => f.classList.contains('read-only') && shown(f)).length,
  };
}"""

CLASSIFY = """() => {
  const deck = document.getElementById('deck');
  const page = document.getElementById('page');
  return {
    frames: deck ? document.querySelectorAll('.frame').length : 0,
    reading: !!page && !deck,
    textLen: (document.body.innerText || '').length,
  };
}"""


def pdf_page_count(pdf_bytes):
    with tempfile.NamedTemporaryFile(suffix=".pdf") as f:
        f.write(pdf_bytes)
        f.flush()
        out = subprocess.run(["pdfinfo", f.name], capture_output=True, text=True, check=True).stdout
    for line in out.splitlines():
        if line.startswith("Pages:"):
            return int(line.split(":", 1)[1].strip())
    raise RuntimeError(f"pdfinfo gave no Pages: line:\n{out}")


def main():
    require_vendored()
    want = sys.argv[1] if len(sys.argv) > 1 else ""
    pages = sorted(
        p for p in ROOT.rglob("*.html")
        if p.relative_to(ROOT).parts[0] not in EXCLUDE_TOP
        and p.relative_to(ROOT).as_posix() not in SKIP_RELATIVE
        and want in p.relative_to(ROOT).as_posix()
    )

    httpd, port = serve(ROOT)
    bad, checked, skipped_short = [], 0, 0
    with sync_playwright() as pw:
        browser = launch(pw)
        page = browser.new_page(viewport={"width": 1280, "height": 900})
        # Same trap as check_shell.py/check_frames.py: a materials page iframes
        # a 9.8 MB PDF, and Chromium's viewer holds that connection open
        # against this single-threaded server, starving every request after it.
        cdn = make_cdn_router()

        def router(route):
            if route.request.url.lower().endswith(".pdf"):
                route.abort()
                return
            cdn(route)

        page.route("**/*", router)
        for path in pages:
            rel = path.relative_to(ROOT).as_posix()
            page.goto(f"http://127.0.0.1:{port}/{rel}", wait_until="networkidle")
            page.wait_for_timeout(400)
            info = page.evaluate(CLASSIFY)
            if not info["reading"] and info["frames"] == 0:
                continue  # not a frame page or a reading page (genindex, etc.)

            pdf_pages = pdf_page_count(page.pdf(print_background=True))

            if info["frames"] > 0:
                checked += 1
                n = info["frames"]
                if pdf_pages < n:
                    bad.append(f"{rel}: {n} frames but only {pdf_pages} printed "
                               f"page(s) -- the deck is still clipped to one viewport")
                elif n > 1 and pdf_pages == 1:
                    bad.append(f"{rel}: {n} frames printed as a single page")

                # the slide handout: same page, printed from present mode
                page.emulate_media(media="print")
                h = page.evaluate(HANDOUT)
                handout_pages = pdf_page_count(page.pdf(print_background=True))
                # back to no emulation, not "screen": page.pdf() honors an
                # emulated screen media and would print every later page as
                # one clipped viewport
                page.emulate_media(media=None)
                if h["depth"] or h["readOnly"]:
                    bad.append(f"{rel}: present-mode print shows {h['depth']} depth block(s) "
                               f"and {h['readOnly']} read-only frame(s) -- the handout "
                               f"is printing the reading page")
                elif handout_pages < h["slides"]:
                    bad.append(f"{rel}: {h['slides']} slides but the handout printed "
                               f"{handout_pages} page(s)")
            else:
                if info["textLen"] < LONG_TEXT_CHARS:
                    skipped_short += 1
                    continue
                checked += 1
                if pdf_pages <= 1:
                    bad.append(f"{rel}: a long reading page ({info['textLen']} chars) "
                               f"printed to {pdf_pages} page -- natural document flow "
                               f"is not reaching the printer")
        page.close()
        browser.close()
    httpd.shutdown()

    if want and not checked:
        print(f"no printable page matched {want!r} -- nothing was checked")
        return 1
    print(f"checked {checked} printable page(s) "
          f"({skipped_short} short reading page(s) exempt from the multi-page rule)")
    if bad:
        print(f"\n{len(bad)} PAGE(S) FAILED TO PRINT PROPERLY:")
        for b in bad:
            print("  " + b)
        return 1
    print("every frame page breaks one sheet per frame in read mode and prints a slide-only "
          "handout in present mode; every long reading page spans sheets")
    return 0


if __name__ == "__main__":
    sys.exit(main())
