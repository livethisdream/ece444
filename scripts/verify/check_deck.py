#!/usr/bin/env python3
"""Render-verify an ECE 444 reveal.js deck without CDN access.

Usage: check_deck.py <slug>       e.g. check_deck.py L07-simple-resonant-antennas

Serves book/extras/slides over HTTP, reroutes CDN requests to the vendored
node_modules copies, steps through every slide, and reports:
  - slide count
  - slides whose content exceeds the 700px stage
  - slides containing raw '$$' or stray '\\_' after MathJax typesets
  - failed resource loads (missing figures) and console errors

A deck that builds is not a deck that renders: the markdown parser mangles
LaTeX in ways Sphinx never sees, so the same equation can be correct on the
lesson page and broken on the slide. Exit code 0 = all checks pass.
"""
import sys

from _common import REPO, launch, make_cdn_router, require_vendored, serve

SLIDES = REPO / "book/extras/slides"
STAGE_HEIGHT = 700


def main():
    if len(sys.argv) < 2:
        raise SystemExit(f"usage: {sys.argv[0]} <slug>")
    require_vendored()
    slug = sys.argv[1]
    html = SLIDES / f"{slug}.html"
    if not html.exists():
        print(f"FAIL: {html} does not exist (run scripts/make_deck_html.py first)")
        sys.exit(2)

    from playwright.sync_api import sync_playwright

    httpd, port = serve(SLIDES)
    failures, console_errs, missing = [], [], []

    with sync_playwright() as p:
        browser = launch(p)
        page = browser.new_page(viewport={"width": 1244, "height": STAGE_HEIGHT})
        page.route("**/*", make_cdn_router(missing))
        page.on(
            "console",
            lambda m: console_errs.append(m.text) if m.type == "error" else None,
        )
        page.on(
            "requestfailed",
            lambda r: missing.append(r.url) if r.url.startswith("http://127.0.0.1") else None,
        )

        page.goto(f"http://127.0.0.1:{port}/{slug}.html", wait_until="networkidle")
        page.wait_for_timeout(3000)  # let MathJax and inline-svg injection settle

        n = page.evaluate("Reveal.getTotalSlides()")
        report = []
        for i in range(n):
            page.evaluate(f"Reveal.slide({i}, 0)")
            page.wait_for_timeout(250)
            r = page.evaluate("""() => {
                const s = Reveal.getCurrentSlide();
                const txt = s.innerText || '';
                return { h: s.scrollHeight,
                         raw: (txt.match(/\\$\\$/g)||[]).length,
                         us: (txt.match(/\\\\_/g)||[]).length,
                         title: (s.querySelector('h1,h2,h3')||{}).innerText || '(untitled)' };
            }""")
            report.append((i + 1, r))
            if r["h"] > STAGE_HEIGHT:
                failures.append(
                    f"slide {i+1} '{r['title']}' overflows: {r['h']}px > {STAGE_HEIGHT}px"
                )
            if r["raw"]:
                failures.append(f"slide {i+1} '{r['title']}' shows raw $$ x{r['raw']}")
            if r["us"]:
                failures.append(f"slide {i+1} '{r['title']}' shows literal \\_ x{r['us']}")
        browser.close()
    httpd.shutdown()

    print(f"{slug}: {n} slides")
    for i, r in report:
        flag = " OVER" if r["h"] > STAGE_HEIGHT else ""
        print(f"  {i:2d}. {r['h']:4d}px{flag}  {r['title'][:60]}")
    failures.extend(f"missing resource: {u}" for u in sorted(set(missing)))
    mathjax_errs = [
        e for e in console_errs if "mathjax" in e.lower() or "typeset" in e.lower()
    ]
    failures.extend(f"console: {e}" for e in mathjax_errs[:5])
    if failures:
        print("FAILURES:")
        for f in failures:
            print("  -", f)
        sys.exit(1)
    print("PASS: all slides fit, no raw $$, no missing resources")


if __name__ == "__main__":
    main()
