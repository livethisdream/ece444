#!/usr/bin/env python3
"""Render a built jupyter-book lesson page with the CDN rerouted to vendored MathJax.

Usage: check_page.py module02/L07-simple-resonant-antennas/index.html
       (path relative to book/_build/html)

Reports typeset math count, visible raw $$/$ leaks, and iframe targets that
404. Math inside a raw-HTML block is not processed by MyST, and a '|' inside
$...$ splits a table cell -- neither errors at build time, so the page has to
be rendered to catch them.

Run `jupyter-book build book/ --all` first. An incremental build silently
skips changes under book/extras/**.
"""
import pathlib
import sys

from _common import REPO, launch, make_cdn_router, require_vendored, serve

ROOT = REPO / "book/_build/html"


def main():
    if len(sys.argv) < 2:
        raise SystemExit(f"usage: {sys.argv[0]} <path-relative-to-book/_build/html>")
    require_vendored()
    rel = sys.argv[1]
    if not (ROOT / rel).exists():
        raise SystemExit(f"FAIL: {ROOT / rel} does not exist (build the book first)")

    from playwright.sync_api import sync_playwright

    httpd, port = serve(ROOT)

    with sync_playwright() as p:
        browser = launch(p)
        page = browser.new_page(viewport={"width": 1280, "height": 900})
        page.route("**/*", make_cdn_router())
        page.goto(f"http://127.0.0.1:{port}/{rel}", wait_until="networkidle")
        page.wait_for_timeout(4000)
        info = page.evaluate("""() => {
            const art = document.querySelector('article') || document.body;
            const txt = art.innerText || '';
            return { math: document.querySelectorAll('mjx-container').length,
                     rawdd: (txt.match(/\\$\\$/g)||[]).length,
                     rawd: (txt.match(/\\$[a-zA-Z\\\\]/g)||[]).length,
                     iframes: [...document.querySelectorAll('iframe')]
                                .map(f => f.getAttribute('src')) };
        }""")
        browser.close()
    httpd.shutdown()

    print(
        f"{rel}: mjx={info['math']} raw$$={info['rawdd']} "
        f"raw$={info['rawd']} iframes={info['iframes']}"
    )
    bad = []
    for f in info["iframes"]:
        if not f or f.startswith(("http://", "https://")):
            continue
        if not ((ROOT / rel).parent / f).resolve().exists():
            bad.append(f"iframe target missing: {f}")
    if info["rawdd"]:
        bad.append(f"raw $$ visible in the article x{info['rawdd']}")
    if info["rawd"]:
        bad.append(f"raw $ visible in the article x{info['rawd']}")
    if info["math"] == 0:
        bad.append("no typeset math on the page (MathJax did not run?)")
    if bad:
        print("FAILURES:")
        for b in bad:
            print("  -", b)
        sys.exit(1)
    print("PASS")


if __name__ == "__main__":
    main()
