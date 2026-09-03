#!/usr/bin/env python3
"""Every frame must fit the screen in present mode.

A frame taller than the viewport is the same defect an overflowing slide was
in the deck: nothing errors, the build is happy, and the bottom of the frame is
simply not there when you present it. Checked at a phone and a laptop, because
a frame that fits one can overflow the other.

    check_frames.py                 # every frame page in the book
    check_frames.py L07-dipoles     # only pages whose path contains this
"""
import pathlib, sys

sys.path.insert(0, str(pathlib.Path(__file__).parent))
from _common import launch, make_cdn_router, serve, require_vendored  # noqa: E402
from playwright.sync_api import sync_playwright  # noqa: E402

ROOT = pathlib.Path(__file__).resolve().parents[2] / "book" / "_build" / "html"

FORCE_IFRAMES = """() => {
  const fr = [...document.querySelectorAll('iframe')];
  fr.forEach(f => { f.loading = 'eager'; if (!f.src) f.src = f.getAttribute('src'); });
  return fr.length;
}"""

PROBE = """() => {
  const deck = document.querySelector('.deck');
  if (!deck) return null;
  // The frame's own padding is the budget: content taller than that is clipped
  // in present mode, where every frame is exactly one viewport tall.
  return [...document.querySelectorAll('.frame')].map((f, i) => {
    const cs = getComputedStyle(f);
    const pad = parseFloat(cs.paddingTop) + parseFloat(cs.paddingBottom);
    const wrap = f.querySelector('.wrap');
    return {
      n: i + 1,
      title: ((f.querySelector('.rubric') || {}).textContent || '(title frame)').trim().slice(0, 46),
      content: Math.round(wrap.getBoundingClientRect().height),
      budget: Math.round(window.innerHeight - pad),
      // Reported, but no longer an excuse: a frame that scrolls to fit its
      // widget is hiding controls below the fold.
      scrolls: cs.overflowY !== 'visible',
    };
  });
}"""


def main():
    require_vendored()
    # An optional path filter, so the per-lesson gate in mech_check.sh can hold
    # one converted lesson to the budget without sweeping all 41.
    want = sys.argv[1] if len(sys.argv) > 1 else ""
    pages = sorted(p for p in ROOT.rglob("*.html")
                   if p.relative_to(ROOT).parts[0] not in ("slides", "viz", "frames", "_static")
                   and want in p.relative_to(ROOT).as_posix())
    httpd, port = serve(ROOT)
    over, checked, scrollable = [], 0, 0
    with sync_playwright() as pw:
        browser = launch(pw)
        for width, height, label in ((390, 844, "phone"), (1280, 800, "laptop")):
            page = browser.new_page(viewport={"width": width, "height": height})
            # Same trap as check_shell.py: a materials page iframes a 9.8 MB
            # PDF, and Chromium's viewer holds that connection open against a
            # single-threaded server, starving every request after it.
            cdn = make_cdn_router()
            def router(route):
                if route.request.url.lower().endswith(".pdf"):
                    route.abort()
                    return
                cdn(route)
            page.route("**/*", router)
            for path in pages:
                rel = path.relative_to(ROOT)
                page.goto(f"http://127.0.0.1:{port}/{rel.as_posix()}",
                          wait_until="domcontentloaded")
                page.wait_for_timeout(900)
                # Widget iframes carry loading="lazy" and sit below the fold, so
                # on a plain load they never fetch: the .wrap this measures then
                # contains an iframe still at its hardcoded markup height, and a
                # widget far taller than that box passes. Force them eager, let
                # viz-autosize settle on the real content height, and measure
                # what a reader actually gets.
                if page.evaluate(FORCE_IFRAMES):
                    page.wait_for_timeout(2200)
                # Read mode is the default since 2026-09-03, and in read mode
                # a frame is content-height with its depth blocks showing --
                # not the thing this budget is about. Measure present mode.
                page.evaluate("() => document.documentElement.setAttribute('data-mode', 'present')")
                page.wait_for_timeout(300)
                frames = page.evaluate(PROBE)
                if not frames:
                    continue
                checked += 1
                for f in frames:
                    # No exemption for scrollable frames. A widget frame that
                    # scrolls is hiding its own controls below the fold, which
                    # is the defect, not a licence for it. Course rule: a
                    # graphic fits the span of one frame or it gets laid out
                    # until it does.
                    if f["scrolls"]:
                        scrollable += 1
                    if f["content"] > f["budget"]:
                        over.append(f"{label} {rel} frame {f['n']} "
                                    f"\"{f['title']}\": {f['content']}px "
                                    f"in {f['budget']}px")
            page.close()
        browser.close()
    httpd.shutdown()

    if want and not checked:
        # Silence here would read as a pass. If the filter matched nothing, or
        # matched a page that is not a frame page, say so and fail.
        print(f"no frame page matched {want!r} -- nothing was checked")
        return 1
    print(f"checked {checked} frame-page renders at two widths"
          f" ({scrollable} frames still declare a scroll container)")
    if over:
        print(f"\n{len(over)} FRAMES OVER BUDGET:")
        for o in over:
            print("  " + o)
        return 1
    print("every frame fits")
    return 0


if __name__ == "__main__":
    sys.exit(main())
