#!/usr/bin/env python3
"""Render-verify an ECE 444 viz widget: height, aspect, and overflow.

Usage: check_widget.py book/extras/viz/<name>.html

Serves the widget's directory over HTTP (mjlabel.js is a relative import),
reroutes the MathJax CDN to the vendored copy, checks for console errors and
blank canvases, exercises each control once, and reports the measured height
to use as the lesson-page iframe fallback.

Two measurement rules, both learned the hard way in Module 2:

  Heights are measured at the widths a reader actually gets. The Sphinx book
  theme caps the article column, so a lesson-page iframe renders between 688px
  (at a 1280 viewport) and 790px (the cap). Height is not monotonic in width --
  canvases grow as it widens, but readout and control breakpoints add rows as
  it narrows -- so the whole range is swept and the worst case reported.
  Measuring at 900px, which no reader ever sees, under-reports it.

  Horizontal overflow is checked at phone widths. The course is reviewed on a
  phone, and zero overflow at 320px is a requirement.

Exit 0 = pass.
"""
import pathlib
import sys

from _common import launch, make_cdn_router, require_vendored, serve

# Widths the lesson-page iframe actually takes, for the height sweep.
HEIGHT_SWEEP = [688, 720, 755, 790]
# Widths where horizontal overflow and canvas aspect are verified.
NARROW_SWEEP = [430, 390, 320]

# Height is capped at EVERY width, not just the desktop ones. Measuring only
# 688-790 is how 29 widgets shipped over budget on a phone: the reader gets an
# inner scrollbar inside the widget, which is the one thing a frame may never
# do. The two caps come from the measured viz-frame budgets -- 720px at
# 1280x800 and 760px at 390x844 -- less the frame title, which takes 56px on
# one line and 96-98px wrapped.
CAP_WIDE, CAP_NARROW = 555, 660
# A widget written to fill its iframe (height:100vh; overflow:hidden, as
# solid-angle.html is) reports the measuring viewport at every width. It cannot
# be sized this way and is not over budget; check it by eye at its real height.
FILL_VIEWPORT_H = 1600
# A canvas whose drawn aspect differs from its CSS box by more than this is
# being stretched -- usually a Math.max() clamp fighting the layout.
MAX_ASPECT_SKEW = 0.02


def main():
    if len(sys.argv) < 2:
        raise SystemExit(f"usage: {sys.argv[0]} <widget.html>")
    require_vendored()
    target = pathlib.Path(sys.argv[1]).resolve()
    if not target.exists():
        raise SystemExit(f"FAIL: {target} does not exist")

    from playwright.sync_api import sync_playwright

    httpd, port = serve(target.parent)
    errs, failures = [], []

    with sync_playwright() as p:
        browser = launch(p)
        page = browser.new_page(viewport={"width": 790, "height": 1600})
        page.route("**/*", make_cdn_router())
        page.on("console", lambda m: errs.append(m.text) if m.type == "error" else None)
        page.on("pageerror", lambda e: errs.append(str(e)))
        page.goto(f"http://127.0.0.1:{port}/{target.name}", wait_until="networkidle")
        page.wait_for_timeout(2500)

        # Exercise every control once: nudge ranges, cycle selects, toggle boxes.
        page.evaluate("""() => {
            document.querySelectorAll('input[type=range]').forEach(r => {
                r.value = (Number(r.min) + Number(r.max)) / 2;
                r.dispatchEvent(new Event('input', {bubbles: true}));
            });
            document.querySelectorAll('select').forEach(s => {
                s.selectedIndex = (s.selectedIndex + 1) % s.options.length;
                s.dispatchEvent(new Event('change', {bubbles: true}));
                s.dispatchEvent(new Event('input', {bubbles: true}));
            });
            document.querySelectorAll('input[type=checkbox]').forEach(c => c.click());
        }""")
        page.wait_for_timeout(800)

        probe = """() => {
            // clientWidth/clientHeight, NOT getBoundingClientRect: the rect is the
            // OUTER box and includes the 1px border on each side, while the bitmap
            // covers the content box. Comparing the two adds a fixed +2px to the
            // box, which is under 1% on a 300px canvas but 3% on a 70px one -- so
            // the old check reported phantom "distortion" on every short canvas.
            const canvases = [...document.querySelectorAll('canvas')].map(cv => ({
                bw: cv.width, bh: cv.height, cw: cv.clientWidth, ch: cv.clientHeight
            }));
            return { height: Math.ceil(document.body.scrollHeight),
                     scrollW: document.documentElement.scrollWidth,
                     clientW: document.documentElement.clientWidth,
                     canvases };
        }"""

        heights, overflows = [], []
        for w in HEIGHT_SWEEP + NARROW_SWEEP:
            page.set_viewport_size({"width": w, "height": 1600})
            page.wait_for_timeout(700)
            info = page.evaluate(probe)
            heights.append((w, info["height"]))
            over = info["scrollW"] - info["clientW"]
            overflows.append((w, over))
            if over > 0:
                failures.append(f"horizontal overflow at {w}px: {over}px")
            for i, c in enumerate(info["canvases"]):
                if not (c["bw"] and c["cw"] and c["bh"] and c["ch"]):
                    continue
                skew = abs((c["bw"] / c["bh"]) / (c["cw"] / c["ch"]) - 1)
                if skew > MAX_ASPECT_SKEW:
                    failures.append(
                        f"canvas {i} aspect distorted at {w}px: "
                        f"bitmap {c['bw']}x{c['bh']} in box "
                        f"{c['cw']:.0f}x{c['ch']:.0f} (skew {skew:.2f})"
                    )

        if all(h == FILL_VIEWPORT_H for _, h in heights):
            fills = True
        else:
            fills = False
            for w, h in heights:
                cap = CAP_WIDE if w in HEIGHT_SWEEP else CAP_NARROW
                if h > cap:
                    failures.append(
                        f"height {h}px at {w}px wide exceeds the {cap}px cap "
                        f"-- the widget scrolls inside its own frame"
                    )
        wide = [kv for kv in heights if kv[0] in HEIGHT_SWEEP]
        worst_w, worst_h = max(wide, key=lambda kv: kv[1])
        page.set_viewport_size({"width": 790, "height": 1600})
        page.wait_for_timeout(500)

        # Ink check: a canvas that draws nothing renders as a blank white box,
        # which no other check catches.
        ink = page.evaluate("""() => {
            return [...document.querySelectorAll('canvas')].map(cv => {
                const ctx = cv.getContext('2d');
                if (!ctx || cv.width === 0) return 0;
                const d = ctx.getImageData(0, 0, cv.width, cv.height).data;
                let n = 0;
                for (let i = 0; i < d.length; i += 400) {
                    if (d[i+3] > 0 && (d[i] < 245 || d[i+1] < 245 || d[i+2] < 245)) n++;
                }
                return n;
            });
        }""")
        svgs = page.evaluate("()=>document.querySelectorAll('svg').length")
        browser.close()
    httpd.shutdown()

    if fills:
        print(f"{target.name}: fills its iframe (reports {FILL_VIEWPORT_H}px at every "
              "width) -- height not checkable here; render it at the iframe's real "
              "height and look")
    else:
        print(
            f"{target.name}: worst-case height = {worst_h}px (at {worst_w}px width) "
            f'-> use height="{worst_h + 10}" in the iframe'
        )
    print("  heights by width: " + ", ".join(f"{w}:{h}" for w, h in heights))
    print("  overflow by width: " + ", ".join(f"{w}:{o}" for w, o in overflows))
    for i, n in enumerate(ink):
        blank = n < 5
        print(f"  canvas {i}: ink samples={n}" + ("  BLANK?" if blank else ""))
        if blank and svgs == 0:
            failures.append(f"canvas {i} appears blank")
    real_errs = [e for e in errs if "favicon" not in e]
    failures.extend(f"console: {e}" for e in real_errs[:6])
    if failures:
        print("FAILURES:")
        for f in dict.fromkeys(failures):
            print("  -", f)
        sys.exit(1)
    print("PASS")


if __name__ == "__main__":
    main()
