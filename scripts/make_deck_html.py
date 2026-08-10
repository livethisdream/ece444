#!/usr/bin/env python3
"""Generate a standalone reveal.js HTML wrapper for a single deck.

The wrapper is a copy of the Jekyll `_layouts/slides.html` from the source
site with the five Liquid interpolations replaced by hardcoded values, so it
can be served as static HTML alongside the Jupyter Book output.

Usage:
    make_deck_html.py --slug L02-antenna-properties \
                      --title "L2 - Basic Properties and Terminology" \
                      --course "ECE 444"

Writes to book/extras/slides/<slug>.html and expects <slug>.md and
course-slides.css to already exist in the same directory (copied earlier
during the migration).
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
  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
  <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/reveal.js-plugins@latest/customcontrols/style.css">
  <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/reveal.js-plugins@latest/chalkboard/style.css">
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
  <script src="https://cdn.jsdelivr.net/npm/reveal.js-plugins@latest/customcontrols/plugin.js"></script>
  <script src="https://cdn.jsdelivr.net/npm/reveal.js-plugins@latest/chalkboard/plugin.js"></script>
  <script>
    // Runtime pen/chalk width tweak. The chalkboard plugin holds
    // boardmarkerWidth and chalkWidth in closure-local vars and exposes
    // RevealChalkboard.configure() to update them live; we track our own
    // current values and re-apply on each bump.
    window.courseSlides = {{
      _widths: {{ pen: 3, chalk: 6 }},
      bumpWidth: function (kind, delta) {{
        var next = Math.max(1, Math.min(40, this._widths[kind] + delta));
        this._widths[kind] = next;
        if (kind === 'pen') {{
          RevealChalkboard.configure({{ boardmarkerWidth: next }});
        }} else {{
          RevealChalkboard.configure({{ chalkWidth: next }});
        }}
        var el = document.getElementById('cs-width-toast');
        if (!el) {{
          el = document.createElement('div');
          el.id = 'cs-width-toast';
          el.style.cssText = 'position:fixed;bottom:12px;left:50%;transform:translateX(-50%);background:rgba(0,0,0,0.75);color:#fff;padding:0.35em 0.9em;border-radius:6px;font:600 14px/1 sans-serif;z-index:9999;pointer-events:none;transition:opacity .35s;';
          document.body.appendChild(el);
        }}
        el.textContent = (kind === 'chalk' ? 'Chalk' : 'Pen') + ' width: ' + next + 'px';
        el.style.opacity = '1';
        clearTimeout(el._t);
        el._t = setTimeout(function () {{ el.style.opacity = '0'; }}, 900);
      }},
      // Download chalkboard/notes annotations as JSON. The plugin's built-in
      // download() always names the file "chalkboard.json"; we name it after
      // the deck (derived from the page filename) plus today's date so
      // annotations from different lectures don't overwrite each other.
      downloadAnnotations: function () {{
        var data = RevealChalkboard.getData();
        var slug = (window.location.pathname.split('/').pop() || 'slides')
                     .replace(/\\.html?$/i, '') || 'slides';
        var d = new Date();
        var pad = function (n) {{ return (n < 10 ? '0' : '') + n; }};
        var stamp = d.getFullYear() + '-' + pad(d.getMonth() + 1) + '-' + pad(d.getDate());
        var a = document.createElement('a');
        a.download = slug + '-annotations-' + stamp + '.json';
        a.href = window.URL.createObjectURL(new Blob([data], {{ type: 'application/json' }}));
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
      }}
    }};

    Reveal.initialize({{
      hash: true,
      slideNumber: 'c/t',
      controls: true,
      progress: true,
      history: true,
      customcontrols: {{
        controls: [
          {{ icon: '<i class="fa fa-pen-square"></i>',
             title: 'Toggle chalkboard (B)',
             action: 'RevealChalkboard.toggleChalkboard();' }},
          {{ icon: '<i class="fa fa-pen"></i>',
             title: 'Toggle notes canvas (C)',
             action: 'RevealChalkboard.toggleNotesCanvas();' }},
          {{ icon: '<i class="fa fa-plus"></i>',
             title: 'Thicker pen',
             action: "window.courseSlides.bumpWidth('pen', 1);" }},
          {{ icon: '<i class="fa fa-minus"></i>',
             title: 'Thinner pen',
             action: "window.courseSlides.bumpWidth('pen', -1);" }},
          {{ icon: '<i class="fa fa-plus-square"></i>',
             title: 'Thicker chalk',
             action: "window.courseSlides.bumpWidth('chalk', 2);" }},
          {{ icon: '<i class="fa fa-minus-square"></i>',
             title: 'Thinner chalk',
             action: "window.courseSlides.bumpWidth('chalk', -2);" }},
          {{ icon: '<i class="fa fa-download"></i>',
             title: 'Download annotations',
             action: 'window.courseSlides.downloadAnnotations();' }}
        ]
      }},
      chalkboard: {{
        boardmarkerWidth: 3,
        chalkWidth: 6,
        chalkEffect: 0.5,
        toggleChalkboardButton: false,
        toggleNotesButton: false
      }},
      mathjax3: {{
        mathjax: 'https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js',
        tex: {{
          inlineMath: [['$', '$'], ['\\\\(', '\\\\)']],
          displayMath: [['$$', '$$'], ['\\\\[', '\\\\]']]
        }}
      }},
      plugins: [ RevealMarkdown, RevealHighlight, RevealNotes, RevealMath.MathJax3, RevealCustomControls, RevealChalkboard ]
    }});
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
