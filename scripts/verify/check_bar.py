#!/usr/bin/env python3
"""The HUD is one pill, centred, holding three runs separated by a rule.

Symmetry is the whole point, so it is measured on both axes:

* the pill is centred in the WINDOW. Three separately pinned groups were not:
  `space-between` centres the middle group between the other two rather than
  in the window, which put it 16px off on a desktop and moved it whenever a
  label changed.
* the middle run is centred in the PILL. The outer runs hold different content
  -- "ECE 444" against "1/27" -- so the bar is a `1fr auto 1fr` grid whose
  outer columns are equal by definition. Nothing measures them, so nothing can
  drift when the counter reaches two digits.

Checked at four widths on both shells, with every panel landing under its own
button and actually receiving clicks.
"""
import pathlib, sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from _common import launch, make_cdn_router, serve, require_vendored, REPO  # noqa: E402
from playwright.sync_api import sync_playwright  # noqa: E402

BUILD = REPO / "book" / "_build" / "html"
PAGES = [("frame", "module01/L05a-field-regions-frames/index.html"),
         ("read",  "syllabus.html")]
# Desktop first, deliberately: it is the width with room to spare, so its bar
# height is the reference for "one row" that the narrow widths are measured
# against. A relative check does not work here -- when the pill hits its
# max-width the text wraps INSIDE a button, so the run and its tallest child
# grow together and any comparison between them still passes.
SIZES = [("desk", 1280, 800), ("tablet", 768, 1024), ("phone", 390, 844), ("320", 320, 640)]
PANELS = {"frame": [("btnSite", "sitepop"), ("btnMode", "modepop"), ("btnTools", "toolspop")],
          "read":  [("btnSite", "sitepop")]}

GEOM = """() => {
  const hud = document.querySelector('.hud');
  const r = hud.getBoundingClientRect();
  const gs = [...hud.querySelectorAll('.hud-group')].map(e => {
    const g = e.getBoundingClientRect();
    return {x: g.x, w: g.width, y: g.y, h: g.height};
  });
  /* Count the rules that are actually PAINTED, not the ones a selector says
     should be. The rule is a ::before on each group after the first, and it
     went missing once already because the popover panels sit between the
     groups in document order and broke an adjacent-sibling selector. */
  const mid = hud.querySelector('.hud-mid');
  const rules = ['::before', '::after'].filter(w => {
    const b = getComputedStyle(mid, w);
    return b.content !== 'none' && parseFloat(b.width) > 0;
  }).length;
  return {x: r.x, w: r.width, y: r.y, h: r.height, rules, gs,
          pad: parseFloat(getComputedStyle(hud).paddingLeft)};
}"""


def main():
    require_vendored()
    httpd, port = serve(BUILD)
    bad = []
    tall = {}          # per shell: the one-row bar height, measured at desktop
    with sync_playwright() as pw:
        browser = launch(pw)
        for kind, rel in PAGES:
            for label, w, h in SIZES:
                ctx = browser.new_context(viewport={"width": w, "height": h})
                ctx.route("**/*", make_cdn_router())
                ctx.route("**/*.pdf", lambda r: r.abort())
                page = ctx.new_page()
                errors = []
                page.on("pageerror", lambda e: errors.append(str(e)))
                page.goto(f"http://127.0.0.1:{port}/{rel}", wait_until="load")
                page.wait_for_timeout(450)
                tag = f"{kind} {label}"

                g = page.evaluate(GEOM)
                # centred in the WINDOW, which is what pinned groups could not do
                off = (g["x"] + g["w"] / 2) - w / 2
                if abs(off) > 1:
                    bad.append(f"{tag}: bar off centre by {off:.0f}px")
                if g["x"] < -0.5 or g["x"] + g["w"] > w + 0.5:
                    bad.append(f"{tag}: bar overhangs the window "
                               f"(x={g['x']:.0f} w={g['w']:.0f} vp={w})")
                if len(g["gs"]) != 3:
                    bad.append(f"{tag}: {len(g['gs'])} runs, expected 3")
                elif g["rules"] != 2:
                    bad.append(f"{tag}: {g['rules']} separating rules, expected 2")
                else:
                    # the outer runs are equal, so the middle one is centred
                    # in the pill and not merely between its neighbours
                    left, mid, right = g["gs"]
                    if abs(left["w"] - right["w"]) > 1:
                        bad.append(f"{tag}: outer runs differ: "
                                   f"{left['w']:.0f}px vs {right['w']:.0f}px")
                    midoff = (mid["x"] + mid["w"] / 2) - (g["x"] + g["w"] / 2)
                    if abs(midoff) > 1:
                        bad.append(f"{tag}: middle run off the pill's centre "
                                   f"by {midoff:.0f}px")
                    # one row: a wrapped bar is still centred but is not the
                    # design, so say so rather than passing it silently
                    mids = [x["y"] + x["h"] / 2 for x in g["gs"]]
                    if max(mids) - min(mids) > 1:
                        bad.append(f"{tag}: the bar wrapped onto more than one row")
                    ref = tall.setdefault(kind, g["h"])
                    if g["h"] > ref + 2:
                        bad.append(f"{tag}: the bar is {g['h']:.0f}px tall "
                                   f"against {ref:.0f}px at desktop -- something "
                                   f"inside it wrapped")

                for btn_id, pop_id in PANELS[kind]:
                    page.locator("#" + btn_id).click()
                    page.wait_for_timeout(220)
                    r = page.evaluate(f"""() => {{
                      const b = document.getElementById('{btn_id}').getBoundingClientRect();
                      const p = document.getElementById('{pop_id}');
                      const q = p.getBoundingClientRect();
                      const el = document.elementFromPoint(q.x + q.width / 2, q.y + q.height / 2);
                      return {{bx: b.x, bw: b.width, by: b.y,
                               px: q.x, pw: q.width, py: q.y, ph: q.height,
                               hit: !!(el && p.contains(el))}};
                    }}""")
                    if r["px"] < -0.5 or r["px"] + r["pw"] > w + 0.5:
                        bad.append(f"{tag} {pop_id}: off screen "
                                   f"(x={r['px']:.0f} w={r['pw']:.0f})")
                    overlap = (min(r["px"] + r["pw"], r["bx"] + r["bw"])
                               - max(r["px"], r["bx"]))
                    if overlap < min(r["bw"], r["pw"]) * 0.6:
                        bad.append(f"{tag} {pop_id}: not under its button "
                                   f"(panel {r['px']:.0f}+{r['pw']:.0f}, "
                                   f"button {r['bx']:.0f}+{r['bw']:.0f})")
                    if r["py"] + r["ph"] > r["by"] + 2:
                        bad.append(f"{tag} {pop_id}: overlaps the bar")
                    # a panel can render, measure and position perfectly while
                    # being entirely click-through; that has happened here
                    if not r["hit"]:
                        bad.append(f"{tag} {pop_id}: click-through, not clickable")
                    page.locator("#" + btn_id).click()
                    page.wait_for_timeout(150)

                if errors:
                    bad.append(f"{tag}: JS error {errors[0][:120]}")
                ctx.close()
        browser.close()
    httpd.shutdown()

    print(f"checked {len(PAGES)} bars at {len(SIZES)} widths")
    if bad:
        print(f"\n{len(bad)} PROBLEMS:")
        for x in bad:
            print("  " + x)
        return 1
    print("centred bar OK")
    return 0


if __name__ == "__main__":
    sys.exit(main())
