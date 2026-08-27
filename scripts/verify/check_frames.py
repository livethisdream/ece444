#!/usr/bin/env python3
"""Every frame must fit the screen in present mode.

A frame taller than the viewport is the same defect an overflowing slide was
in the deck: nothing errors, the build is happy, and the bottom of the frame is
simply not there when you present it. Checked at a phone and a laptop, because
a frame that fits one can overflow the other.
"""
import pathlib, sys

sys.path.insert(0, str(pathlib.Path(__file__).parent))
from _common import launch, make_cdn_router, serve, require_vendored  # noqa: E402
from playwright.sync_api import sync_playwright  # noqa: E402

ROOT = pathlib.Path(__file__).resolve().parents[2] / "book" / "_build" / "html"

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
      // A frame that scrolls is not clipping anything, so it is not over
      // budget -- the widget frames are deliberately scrollable because a
      // widget stacks its own controls and cannot be shrunk to fit.
      scrolls: cs.overflowY !== 'visible',
    };
  });
}"""


def main():
    require_vendored()
    pages = sorted(p for p in ROOT.rglob("*.html")
                   if p.relative_to(ROOT).parts[0] not in ("slides", "viz", "frames", "_static"))
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
                frames = page.evaluate(PROBE)
                if not frames:
                    continue
                checked += 1
                for f in frames:
                    if f["content"] > f["budget"] and f["scrolls"]:
                        scrollable += 1
                    elif f["content"] > f["budget"]:
                        over.append(f"{label} {rel} frame {f['n']} "
                                    f"\"{f['title']}\": {f['content']}px "
                                    f"in {f['budget']}px")
            page.close()
        browser.close()
    httpd.shutdown()

    print(f"checked {checked} frame-page renders at two widths"
          f" ({scrollable} frames scroll by design and are exempt)")
    if over:
        print(f"\n{len(over)} FRAMES OVER BUDGET:")
        for o in over:
            print("  " + o)
        return 1
    print("every frame fits")
    return 0


if __name__ == "__main__":
    sys.exit(main())
