#!/usr/bin/env python3
"""Generate a standalone reveal.js HTML wrapper for a single deck.

The wrapper loads reveal.js (+ markdown/highlight/notes/math) from CDN and a
locally-vendored chalkboard plugin, then boots everything through
deck-tools.js — the shared chalkboard/annotation runtime ported from
USAFA-ECE/ece-495-ew. The per-deck HTML is intentionally thin: all config and
behavior lives in deck-tools.js, all styling in course-slides.css.

Usage:
    make_deck_html.py --slug L02-antenna-properties \
                      --title "L2 - Basic Properties and Terminology" \
                      --course "ECE 444"

Writes to book/extras/slides/<slug>.html and expects <slug>.md,
course-slides.css, deck-tools.js, and vendor/chalkboard.{js,css} to already
exist in the same directory.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

TEMPLATE = """<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{title} — {course}</title>

  <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/reveal.js@5.1.0/dist/reveal.css">
  <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/reveal.js@5.1.0/dist/theme/white.css" id="theme">
  <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/reveal.js@5.1.0/plugin/highlight/monokai.css">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Source+Sans+Pro:wght@400;600;700&family=Caveat:wght@600&display=swap">
  <link rel="stylesheet" href="./vendor/chalkboard.css">
  <link rel="stylesheet" href="./course-slides.css">
</head>
<body>
  <div class="reveal">
    <div class="slides">
      <section
        data-markdown="./{slug}.md"
        data-separator="^\\r?\\n---\\r?\\n$"
        data-separator-vertical="^\\r?\\n--\\r?\\n$"
        data-separator-notes="^Note:"
        data-charset="utf-8">
      </section>
    </div>
  </div>

  <script src="https://cdn.jsdelivr.net/npm/reveal.js@5.1.0/dist/reveal.js"></script>
  <script src="https://cdn.jsdelivr.net/npm/reveal.js@5.1.0/plugin/markdown/markdown.js"></script>
  <script src="https://cdn.jsdelivr.net/npm/reveal.js@5.1.0/plugin/highlight/highlight.js"></script>
  <script src="https://cdn.jsdelivr.net/npm/reveal.js@5.1.0/plugin/notes/notes.js"></script>
  <script src="https://cdn.jsdelivr.net/npm/reveal.js@5.1.0/plugin/math/math.js"></script>
  <script src="./vendor/chalkboard.js"></script>
  <script src="./deck-tools.js"></script>
  <script>
    // House Reveal config (incl. the touch:false zoom fix) and the
    // chalkboard/annotation toolbar all live in deck-tools.js; each deck
    // just boots it.
    DeckTools.init();
  </script>
</body>
</html>
"""


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--slug", required=True, help="Deck slug, e.g. L02-antenna-properties")
    ap.add_argument("--title", required=True, help="Human-readable lesson title")
    ap.add_argument("--course", default="ECE 444")
    ap.add_argument(
        "--out-dir",
        default="book/extras/slides",
        help="Where the HTML is written (relative to repo root)",
    )
    args = ap.parse_args()

    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / f"{args.slug}.html"

    html = TEMPLATE.format(slug=args.slug, title=args.title, course=args.course)
    # utf-8 explicitly: the template contains an em-dash and the page declares
    # <meta charset="utf-8">. Without this, write_text uses the platform default
    # (cp1252 on Windows) and the title mojibakes.
    out_path.write_text(html, encoding="utf-8")
    print(f"wrote {out_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
