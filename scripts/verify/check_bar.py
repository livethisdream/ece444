#!/usr/bin/env python3
"""Three groups, pinned left / centre / right. Measure, don't eyeball:
do they fit, do they stay in their thirds, and does each panel land under the
button that opened it?
"""
import pathlib, sys
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from _common import launch, make_cdn_router, serve, require_vendored, REPO
from playwright.sync_api import sync_playwright

BUILD = REPO / "book" / "_build" / "html"
PAGES = [("frame", "module01/L05a-field-regions-frames/index.html"),
         ("read",  "syllabus.html")]
SIZES = [("320", 320, 640), ("phone", 390, 844), ("tablet", 768, 1024), ("desk", 1280, 800)]
PANELS = {"frame": [("btnSite", "sitepop"), ("btnMode", "modepop"), ("btnTools", "toolspop")],
          "read":  [("btnSite", "sitepop")]}

require_vendored()
httpd, port = serve(BUILD)
bad = []
with sync_playwright() as pw:
    b = launch(pw)
    for kind, rel in PAGES:
        for label, w, h in SIZES:
            ctx = b.new_context(viewport={"width": w, "height": h})
            ctx.route("**/*", make_cdn_router()); ctx.route("**/*.pdf", lambda r: r.abort())
            pg = ctx.new_page()
            errs = []; pg.on("pageerror", lambda e: errs.append(str(e)))
            pg.goto(f"http://127.0.0.1:{port}/{rel}", wait_until="load")
            pg.wait_for_timeout(450)
            tag = f"{kind} {label}"

            g = pg.evaluate("""() => {
              const hud = document.querySelector('.hud').getBoundingClientRect();
              const gs = [...document.querySelectorAll('.hud-group')]
                  .filter(e => getComputedStyle(e).display !== 'none')
                  .map(e => { const r = e.getBoundingClientRect();
                              return {x: r.x, w: r.width, y: r.y, h: r.height}; });
              return {hud: {x: hud.x, w: hud.width, y: hud.y, h: hud.height}, gs};
            }""")
            if len(g["gs"]) != 3:
                bad.append(f"{tag}: {len(g['gs'])} groups visible, expected 3"); ctx.close(); continue

            # they must not overlap, and must stay inside the bar
            gs = g["gs"]
            for i in range(2):
                gap = gs[i + 1]["x"] - (gs[i]["x"] + gs[i]["w"])
                if gap < 2:
                    bad.append(f"{tag}: groups {i} and {i+1} collide (gap {gap:.0f}px)")
            if gs[0]["x"] < g["hud"]["x"] - 0.5:
                bad.append(f"{tag}: left group starts before the bar")
            right = gs[-1]["x"] + gs[-1]["w"]
            if right > g["hud"]["x"] + g["hud"]["w"] + 0.5:
                bad.append(f"{tag}: right group overhangs the bar by "
                           f"{right - g['hud']['x'] - g['hud']['w']:.0f}px")
            # one row: the bar must not have wrapped
            def mid(x): return x["y"] + x["h"] / 2
            if any(abs(mid(x) - mid(gs[0])) > 1 for x in gs):
                bad.append(f"{tag}: groups wrapped onto more than one row")
            # ...and the same height, which is what makes three pills read as
            # one bar rather than three unrelated blobs
            if max(x["h"] for x in gs) - min(x["h"] for x in gs) > 1:
                bad.append(f"{tag}: group heights differ: "
                           + ", ".join(f"{x['h']:.0f}" for x in gs))
            # actually pinned to the thirds
            if abs(gs[0]["x"] - g["hud"]["x"]) > 1:
                bad.append(f"{tag}: left group not flush left")
            if abs(right - (g["hud"]["x"] + g["hud"]["w"])) > 1:
                bad.append(f"{tag}: right group not flush right")

            for btn_id, pop_id in PANELS[kind]:
                pg.locator("#" + btn_id).click(); pg.wait_for_timeout(220)
                r = pg.evaluate(f"""() => {{
                  const b = document.getElementById('{btn_id}').getBoundingClientRect();
                  const p = document.getElementById('{pop_id}').getBoundingClientRect();
                  return {{bx: b.x, bw: b.width, px: p.x, pw: p.width, py: p.y, ph: p.height, by: b.y}};
                }}""")
                if r["px"] < -0.5 or r["px"] + r["pw"] > w + 0.5:
                    bad.append(f"{tag} {pop_id}: off screen (x={r['px']:.0f} w={r['pw']:.0f})")
                # the panel has to sit under the button that opened it
                overlap = min(r["px"] + r["pw"], r["bx"] + r["bw"]) - max(r["px"], r["bx"])
                if overlap < min(r["bw"], r["pw"]) * 0.6:
                    bad.append(f"{tag} {pop_id}: not under its button "
                               f"(panel {r['px']:.0f}+{r['pw']:.0f}, button {r['bx']:.0f}+{r['bw']:.0f})")
                if r["py"] + r["ph"] > r["by"] + 2:
                    bad.append(f"{tag} {pop_id}: overlaps the bar")
                pg.locator("#" + btn_id).click(); pg.wait_for_timeout(150)

            if errs: bad.append(f"{tag}: JS error {errs[0][:120]}")
            ctx.close()
    b.close()
httpd.shutdown()
print(f"checked {len(PAGES)} bars x {len(SIZES)} widths")
if bad:
    print(f"\n{len(bad)} PROBLEMS:")
    for x in bad: print("  " + x)
    sys.exit(1)
print("three-group bar OK")
