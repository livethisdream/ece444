#!/usr/bin/env python3
"""Render every shell page and assert it holds together.

The theme used to guarantee a lot of this for free. Now that the pages own
their own layout, it has to be checked: no sideways scroll at phone width, no
JS error, a breadcrumb that says something, and no theme asset sneaking back
onto a page that no longer has the DOM to support it.
"""
import json, pathlib, sys

sys.path.insert(0, str(pathlib.Path(__file__).parent))
from _common import launch, make_cdn_router, serve, require_vendored  # noqa: E402
from playwright.sync_api import sync_playwright  # noqa: E402

ROOT = pathlib.Path(__file__).resolve().parents[2] / "book" / "_build" / "html"
SKIP_DIRS = {"slides", "viz", "frames", "_static", "practice"}

PROBE = """() => {
  const page = document.querySelector('.page');
  const crumb = document.getElementById('crumb');
  const hud = document.querySelector('.hud');
  const theme = [...document.querySelectorAll('link[rel=stylesheet], script[src]')]
      .map(e => e.getAttribute('href') || e.getAttribute('src') || '')
      .filter(u => /styles\\/(bootstrap|pydata|sphinx-book)|fontawesome|jquery/.test(u));
  const tracks = {};
  const p = page && page.querySelector('section > p');
  if (p) tracks.text = Math.round(p.getBoundingClientRect().width);
  const wide = page && page.querySelector('.two-col, .module-toc, .pst-scrollable-table-container, .hero');
  if (wide) tracks.wide = Math.round(wide.getBoundingClientRect().width);
  return {
    isShell: !!page,
    docOverflow: document.documentElement.scrollWidth - window.innerWidth,
    crumb: crumb ? crumb.innerText.replace(/\\s+/g, ' ').trim() : null,
    hud: !!hud,
    overlay: !!document.getElementById('index'),
    themeAssets: theme,
    tracks,
  };
}"""


def main():
    require_vendored()
    pages = sorted(
        p for p in ROOT.rglob("*.html")
        if not (SKIP_DIRS & set(p.relative_to(ROOT).parts))
        and p.name not in ("genindex.html", "search.html")
    )
    httpd, port = serve(ROOT)
    fails = []
    with sync_playwright() as pw:
        browser = launch(pw)
        for width, height, label in ((390, 844, "phone"), (1280, 900, "desk")):
            page = browser.new_page(viewport={"width": width, "height": height})
            errors = []
            page.on("pageerror", lambda e: errors.append(str(e)))
            # The materials pages iframe a 9.8 MB PDF. _common.serve() is a
            # single-threaded TCPServer, and Chromium's PDF viewer holds that
            # connection open -- which starves every later request and times
            # out the whole sweep. The layout check has no interest in the
            # PDF's contents, so refuse it.
            cdn = make_cdn_router()
            def router(route):
                if route.request.url.lower().endswith(".pdf"):
                    route.abort()
                    return
                cdn(route)
            page.route("**/*", router)
            for path in pages:
                rel = path.relative_to(ROOT)
                errors.clear()
                # Not networkidle: the materials pages embed PDFs that never
                # stop streaming, and the wait times out instead of failing.
                page.goto(f"http://127.0.0.1:{port}/{rel.as_posix()}",
                          wait_until="domcontentloaded")
                page.wait_for_timeout(700)
                r = page.evaluate(PROBE)
                if not r["isShell"]:
                    continue                       # still on the theme; not ours to check
                def bad(msg):
                    fails.append(f"{label} {rel}: {msg}")
                if r["docOverflow"] > 0:
                    bad(f"scrolls sideways by {r['docOverflow']}px")
                if not r["crumb"]:
                    bad("empty breadcrumb")
                if not r["hud"] or not r["overlay"]:
                    bad("missing HUD or overlay")
                if r["themeAssets"]:
                    bad(f"theme assets linked: {r['themeAssets'][:2]}")
                if errors:
                    bad(f"JS error: {errors[0][:120]}")
                # Not asserted: that a `wide` element is wider than the text
                # track. It gets the wider track, but nothing makes it fill it
                # -- a narrow two-col legitimately measures less. Overflow is
                # the failure that matters, and it is checked above.
            page.close()
        browser.close()
    httpd.shutdown()

    print(f"checked {len(pages)} pages at two widths")
    if fails:
        print(f"\n{len(fails)} FAILURES:")
        for f in fails[:25]:
            print("  " + f)
        return 1
    print("all shell pages OK")
    return 0


if __name__ == "__main__":
    sys.exit(main())
