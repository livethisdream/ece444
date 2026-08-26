#!/usr/bin/env python3
"""Assemble a scroll-frame lecture page -- currently L05 only.

EXPERIMENTAL, and parallel to everything else: this does not replace the
lesson page or the deck, both of which are untouched. It is the "one artifact
per lesson" idea made concrete, so it can be judged against the real thing.

The deck and the lesson page collapsed into a single scrolling document, one
full-viewport frame per beat, driven from the keyboard like a deck. Press P to
switch between presenting (frames snap, depth hidden) and reading (continuous
document, everything visible). The lesson-page depth is always in the DOM;
present mode only hides it, so presenting can never lose it.

Figures and widgets are read from the repo at build time -- nothing is copied
by hand -- so this file carries only the frame prose. That split is the point:
whatever must stay in sync with the course is sourced, and only the narration
is authored here.

    python3 scripts/build_frames.py               # -> book/extras/frames/
    python3 scripts/build_frames.py --standalone  # one self-contained file

CI never runs this (it only runs jupyter-book), so the generated HTML is
COMMITTED, exactly like the deck wrappers and the practice PDFs. Re-run and
re-commit after editing a figure, a widget, or the frame prose.
"""
import html
import pathlib
import re

import argparse
import sys

REPO = pathlib.Path(__file__).resolve().parent.parent
FIG = REPO / "book/extras/slides/fig"
VIZ = REPO / "book/extras/viz"
OUTDIR = REPO / "book/extras/frames"
SLUG = "L05-field-regions"
STANDALONE = False

# ---------------------------------------------------------------- figures ---
def svg(name):
    """Inline a committed figure verbatim.

    No rewriting: the house palette is retargeted by CSS attribute selectors
    (see FIGCSS), which beat SVG presentation attributes. So every generated
    course figure becomes theme-aware without touching its generator.
    """
    s = (FIG / name).read_text()
    s = re.sub(r'\s(width|height)="[\d.]+(pt|px)?"', "", s, count=2)
    return s.strip()

FIGCSS = """
[fill="#5a5a5a"]  { fill: var(--fig-line); }
[stroke="#5a5a5a"]{ stroke: var(--fig-line); }
[fill="#004a85"]  { fill: var(--blue-dark); }
[stroke="#004a85"]{ stroke: var(--blue-dark); }
[fill="#0067b9"]  { fill: var(--blue); }
[stroke="#0067b9"]{ stroke: var(--blue); }
[fill="#b01e24"]  { fill: var(--red); }
[stroke="#b01e24"]{ stroke: var(--red); }
[fill="#1d7a4d"]  { fill: var(--green); }
[fill="#cddce9"]  { fill: var(--fig-far); }
[stroke="#b9d2e5"]{ stroke: var(--fig-grid); }
[fill="#ffffff"]  { fill: var(--panel); }
"""

# ---------------------------------------------------------------- widgets ---
# mjlabel.js fetches MathJax from a CDN. Blocked here (and in the course
# containers), so MJ.draw silently returns 0 and the symbol labels never
# appear -- and because the widgets kick their first paint from MJ.onReady,
# the canvas can stay blank entirely. This shim replaces MJ with a canvas-text
# implementation that needs no network and fires onReady immediately.
MJ_SHIM = r"""
<script>
(function () {
  var MAP = {'\\Rightarrow':'\u21d2','\\rightarrow':'\u2192','\\leftarrow':'\u2190',
             '\\lambda':'\u03bb','\\Delta':'\u0394','\\delta':'\u03b4','\\theta':'\u03b8',
             '\\phi':'\u03c6','\\eta':'\u03b7','\\pi':'\u03c0','\\omega':'\u03c9',
             '\\Omega':'\u03a9','\\alpha':'\u03b1','\\beta':'\u03b2','\\Gamma':'\u0393',
             '\\propto':'\u221d','\\approx':'\u2248','\\times':'\u00d7','\\cdot':'\u00b7',
             '\\infty':'\u221e','\\ast':'*','\\sim':'~','\\pm':'\u00b1','\\ldots':'\u2026',
             '\\gg':'\u226b','\\ll':'\u226a','\\le':'\u2264','\\ge':'\u2265','\\to':'\u2192',
             '\\,':' ','\;':' ','\\!':'','\\ ':' '};
  /* longest key first, so \\Rightarrow is not eaten by \\rightarrow's prefix */
  var KEYS = Object.keys(MAP).sort(function (a, b) { return b.length - a.length; });
  function tex2txt(t) {
    var s = String(t);
    for (var i = 0; i < KEYS.length; i++) s = s.split(KEYS[i]).join(MAP[KEYS[i]]);
    s = s.replace(/\^\{([^}]*)\}|\^(\w)/g, function (m, a, b) {
      var v = a || b, sup = {'0':'\u2070','1':'\u00b9','2':'\u00b2','3':'\u00b3','-':'\u207b'};
      return v.split('').map(function (c) { return sup[c] || c; }).join('');
    });
    s = s.replace(/_\{([^}]*)\}|_(\w)/g, function (m, a, b) {
      var v = a || b, sub = {'0':'\u2080','1':'\u2081','2':'\u2082','3':'\u2083'};
      return v.split('').map(function (c) { return sub[c] || c; }).join('');
    });
    return s.replace(/[\\{}$]/g, '').trim();
  }
  var redraw = null;
  window.MJ = {
    get ready() { return true; },
    onReady: function (cb) { setTimeout(function () { cb && cb(); }, 0); },
    typeset: function () { return Promise.resolve(); },
    setRedraw: function (fn) { redraw = fn; },
    width: function (tex, color, h) {
      var c = document.createElement('canvas').getContext('2d');
      c.font = 'italic ' + h + 'px Georgia, serif';
      return c.measureText(tex2txt(tex)).width;
    },
    draw: function (ctx, tex, x, y, h, color, align) {
      var t = tex2txt(tex);
      ctx.save();
      ctx.font = 'italic ' + h + 'px Georgia, serif';
      ctx.fillStyle = color || '#000';
      ctx.textBaseline = 'middle';
      ctx.textAlign = align === 'center' ? 'center' : (align === 'right' ? 'right' : 'left');
      ctx.fillText(t, x, y);
      var w = ctx.measureText(t).width;
      ctx.restore();
      return w;
    }
  };
  /* the same substitution for \(..\) written into the HTML labels */
  document.addEventListener('DOMContentLoaded', function () {
    var w = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT);
    var n, hits = [];
    while ((n = w.nextNode())) if (n.nodeValue.indexOf('\\(') > -1) hits.push(n);
    hits.forEach(function (t) {
      t.nodeValue = t.nodeValue.replace(/\\\(([\s\S]*?)\\\)/g, function (m, inner) {
        return tex2txt(inner);
      });
      /* MathJax put an IMAGE here, which text-transform could not touch; now
         it is real text, so an uppercasing label would mangle Greek. */
      if (t.parentElement) t.parentElement.style.textTransform = 'none';
    });
  });
})();
</script>
"""

def widget(name, height):
    """Embed a course widget as an iframe.

    An iframe rather than inlining either way: the two widgets on this page use
    the same element ids (#d, #f, #r), so sharing one document would break both.

    On the site the widget is loaded by URL, same-origin, so it behaves exactly
    as it does on the lesson page -- same file, same MathJax, one copy. For a
    standalone build (sharing the file, or anywhere the CDN is blocked) it is
    inlined via srcdoc with a MathJax shim instead; see MJ_SHIM.
    """
    attrs = ('class="viz" data-autosize="1" style="height:{h}px" title="{t}"'
             .format(h=height, t=html.escape(name, quote=True)))
    if STANDALONE:
        src = (VIZ / name).read_text()
        src = src.replace('<script src="mjlabel.js"></script>', MJ_SHIM)
        return '<iframe {a} srcdoc="{s}"></iframe>'.format(
            a=attrs, s=html.escape(src, quote=True))
    # /frames/<slug>.html -> ../viz/<name> resolves to /viz/<name>
    return '<iframe {a} loading="lazy" src="../viz/{n}"></iframe>'.format(a=attrs, n=name)

# ----------------------------------------------------------------- frames ---
# (content, css-class, depth) -- `depth` is the lesson-page material that the
# deck does not carry. It is always in the DOM; present mode hides it.
EQ_E = """<i>E</i><sub>&theta;</sub> =
 <span class="frac"><span><i>jk&eta;</i><sub>0</sub><i>I&thinsp;dl</i>&thinsp;sin&thinsp;<i>&theta;</i></span><span>4<i>&pi;r</i></span></span>
 <span class="paren">(</span>1 + <span class="frac"><span>1</span><span><i>jkr</i></span></span>
 &minus; <span class="frac"><span>1</span><span>(<i>kr</i>)<sup>2</sup></span></span><span class="paren">)</span>
 <i>e</i><sup>&minus;<i>jkr</i></sup>"""

EQ_H = """<i>H</i><sub>&phi;</sub> =
 <span class="frac"><span><i>jkI&thinsp;dl</i>&thinsp;sin&thinsp;<i>&theta;</i></span><span>4<i>&pi;r</i></span></span>
 <span class="paren">(</span>1 + <span class="frac"><span>1</span><span><i>jkr</i></span></span><span class="paren">)</span>
 <i>e</i><sup>&minus;<i>jkr</i></sup>"""

R = '<span class="var">r</span>'
K = '<span class="var">k</span>'
KR = '<span class="var">kr</span>'
D = '<span class="var">D</span>'
LAM = '<span class="var">&lambda;</span>'
FF = '2' + D + '<sup>2</sup>/' + LAM

FRAMES = [

# 1 ---------------------------------------------------------------------
("""<div class="course-mark">ECE 444 &middot; Fall 2026</div>
<h1>Field Regions</h1>
<div class="title-rule"></div>
<p class="lede">Where you stand changes what you see.</p>
<p class="meta">Lesson 5 &middot; Antennas, Phased Arrays, and Radar Systems &middot; Dr. Neil Rogers</p>""",
 "title-frame", None),

# 2 ---------------------------------------------------------------------
("""<h2>Learning objectives</h2>
<ol class="plan">
  <li>I can distinguish the reactive near-field, radiating near-field, and far-field regions by what the fields are actually doing in each.</li>
  <li>I can calculate the boundaries between the three regions for a given antenna size and wavelength.</li>
  <li>I can explain the phase-error criterion behind the far-field distance, and why you must measure an antenna in its far field.</li>
</ol>""",
 "", """<p>Lesson 4 looked <em>into</em> the antenna terminals. Now we step back <em>out</em> into the space around the antenna and ask: as you walk away, at what point do the fields settle into the clean, predictable radiation pattern from Lesson 2 &mdash; and what are they doing before that?</p>
<p>The space around any antenna divides into <strong>three regions</strong>. They are not sharp walls; the fields transition gradually. But the boundaries are worth knowing, because <em>where you stand changes what you measure.</em></p>"""),

# 3 ---------------------------------------------------------------------
("""<h2>Where we were</h2>
<ul>
  <li><strong>L2</strong> &mdash; pattern, directivity, gain. Every one of those numbers was quoted <em class="term">far away</em>, without ever saying so.</li>
  <li><strong>L3</strong> &mdash; polarization and bandwidth of that same escaping wave.</li>
  <li><strong>L4</strong> &mdash; the <strong>terminals</strong>: <span class="var">Z</span><sub>in</sub>, reactance, stored energy the radio has to fight.</li>
</ul>
<p class="pull">Today we step outside the antenna. Where you stand changes what you measure.</p>""",
 "", None),

# 4 ---------------------------------------------------------------------
("""<h2>Today&rsquo;s plan</h2>
<ol class="plan">
  <li>What <strong>near</strong> and <strong>far</strong> actually mean</li>
  <li>The exact fields of one current element &mdash; <strong>three terms, three powers of """ + R + """</strong></li>
  <li>The crossover at """ + KR + """ = 1 &mdash; and what it does <em class="term">not</em> say</li>
  <li>The <strong>three regions</strong> and their boundaries</li>
  <li>Where """ + FF + """ comes from &mdash; a <strong>phase-error budget</strong></li>
  <li>Why an antenna range has to be so long</li>
</ol>""",
 "", None),

# 5 ---------------------------------------------------------------------
("""<h2>Near and far</h2>
<p>Walk away from a transmitting antenna and watch the field.</p>
<ul>
  <li><strong>Near</strong> &mdash; the field still remembers how the antenna is <em class="term">built</em>. Its shape depends on how far out you are, and some of it never leaves at all.</li>
  <li><strong>Far</strong> &mdash; the antenna has collapsed into a <strong>point source</strong>. The pattern shape stops changing with """ + R + """; the amplitude just scales as 1/""" + R + """.</li>
</ul>
<div class="callout"><p>&ldquo;The gain is 15 dBi&rdquo; means <strong>in the far field</strong>. Every spec you will ever read carries that silent qualifier.</p></div>""",
 "", None),

# 6 ---------------------------------------------------------------------
("""<h2>Where the regions come from</h2>
<p>The regions are not a convention someone imposed. Solve Maxwell exactly for the simplest antenna there is &mdash; an <strong>infinitesimal dipole</strong>, a current element <span class="var">I&thinsp;dl</span> along <span class="var">&zcaron;</span> with <span class="var">dl</span> &laquo; """ + LAM + """:</p>
<div class="eq">""" + EQ_E + """</div>
<div class="eq">""" + EQ_H + """</div>
<p><strong>Current elements like this make up every antenna.</strong> Whatever these fields do, real antennas do too &mdash; superposed.</p>""",
 "", """<p>The element is short enough (<span class="var">dl</span> &laquo; """ + LAM + """) that the current is uniform along it. These are spherical coordinates, phasor convention, with <i>e</i><sup>&minus;<i>jkr</i></sup> carried along as in Lesson 2, and """ + K + """ = 2<span class="var">&pi;</span>/""" + LAM + """.</p>
<p>There is a third component the slide leaves out &mdash; a purely radial field with no radiation term at all:</p>
<div class="eq"><i>E</i><sub>r</sub> =
 <span class="frac"><span><i>&eta;</i><sub>0</sub><i>I&thinsp;dl</i>&thinsp;cos&thinsp;<i>&theta;</i></span><span>2<i>&pi;r</i><sup>2</sup></span></span>
 <span class="paren">(</span>1 + <span class="frac"><span>1</span><span><i>jkr</i></span></span><span class="paren">)</span>
 <i>e</i><sup>&minus;<i>jkr</i></sup></div>
<p>with <i>E</i><sub>&phi;</sub> = <i>H</i><sub>r</sub> = <i>H</i><sub>&theta;</sub> = 0. It falls as 1/""" + R + """<sup>2</sup> at best, so it is a near-field quantity only &mdash; it contributes nothing to the pattern you measure far away.</p>"""),

# 7 ---------------------------------------------------------------------
("""<h2>Read the fields by their powers of """ + R + """</h2>
<p>Multiply the bracket through and the field is a sum of three pieces:</p>
<div class="eq"><i>E</i><sub>&theta;</sub> &prop;
 <span class="frac"><span>1</span><span><i>r</i></span></span> +
 <span class="frac"><span>1</span><span><i>kr</i><sup>2</sup></span></span> +
 <span class="frac"><span>1</span><span><i>k</i><sup>2</sup><i>r</i><sup>3</sup></span></span></div>
<div class="tablewrap"><table>
<thead><tr><th>Term</th><th>Falls off as</th><th>Physical origin</th><th>Wins where</th></tr></thead>
<tbody>
<tr><td class="res">radiation</td><td>1/<span class="m">r</span></td><td>the escaping wave &mdash; L2&rsquo;s far field</td><td><span class="m">kr</span> &raquo; 1</td></tr>
<tr><td class="res">induction</td><td>1/<span class="m">r</span><sup>2</sup></td><td>Biot&ndash;Savart / Amp&egrave;re field of the current</td><td><span class="m">kr</span> &sim; 1</td></tr>
<tr><td class="res">electrostatic</td><td>1/<span class="m">r</span><sup>3</sup></td><td>quasi-static field of the charge &plusmn;<span class="m">q</span> at the tips</td><td><span class="m">kr</span> &laquo; 1</td></tr>
</tbody></table></div>
<div class="callout"><p>Three regions, hiding inside one equation. The single number """ + KR + """ sets their relative sizes <strong>entirely</strong>.</p></div>""",
 "", None),

# 8 ---------------------------------------------------------------------
("""<h2>The three terms, on log&ndash;log axes</h2>
<figure>__SVG_CROSS__
<figcaption>Straight lines of slope &minus;1, &minus;2, &minus;3, all crossing at """ + KR + """ = 1.</figcaption></figure>""",
 "", """<p>To the left of the crossover the 1/""" + R + """<sup>3</sup> stored field runs away &mdash; the reactive near field. To the right the radiation term takes over, and its lead over the other two grows <strong>tenfold for every decade</strong> you move out. That is why &ldquo;negligible&rdquo; takes until """ + KR + """ &asymp; 10, not """ + KR + """ = 1.</p>"""),

# 9 ---------------------------------------------------------------------
("""<h2>Drive it yourself &mdash; the three terms</h2>
<p>Move the observation point in and out and watch which term is on top.</p>
__VIZ_TERMS__""",
 "viz-frame", None),

# 10 --------------------------------------------------------------------
("""<h2>The crossover is a single number</h2>
<p>Radiation (size 1 in the bracket) and induction (size 1/""" + KR + """) are equal when</p>
<div class="eq"><i>kr</i> = 1 &nbsp;&rArr;&nbsp; <i>r</i> =
 <span class="frac"><span>1</span><span><i>k</i></span></span> =
 <span class="frac"><span><i>&lambda;</i></span><span>2<i>&pi;</i></span></span> &asymp; 0.16<i>&lambda;</i></div>
<ul>
  <li>At """ + KR + """ = 1 all three terms are <strong>the same size</strong>. That is <em class="term">all</em> it says.</li>
  <li>Reactive terms are negligible only for """ + KR + """ &raquo; 1: at """ + KR + """ = 6 &mdash; about one wavelength out &mdash; induction is down to 17% and the electrostatic term to 3%.</li>
</ul>
<div class="callout"><p>""" + KR + """ = 1 is the <strong>crossover</strong>, not the start of the far field. For a small antenna the far field is usable from roughly a wavelength out, not from 0.16""" + LAM + """.</p></div>""",
 "", """<p>Read that carefully, because it is the single most misquoted number in the subject. Inside """ + LAM + """/2<span class="var">&pi;</span> the stored terms take over and blow up as you approach the antenna. Outside it the radiation term does not suddenly stand alone; it merely starts to <strong>dominate increasingly</strong>, because each reactive term keeps shedding another factor of 1/""" + KR + """.</p>
<p>Dividing the bracket through by the radiation term makes the bookkeeping obvious &mdash; the three sizes are 1 : 1/""" + KR + """ : 1/(""" + KR + """)<sup>2</sup>:</p>
<div class="tablewrap"><table>
<thead><tr><th><span class="m">kr</span></th><th><span class="m">r</span></th><th>radiation : induction : electrostatic</th></tr></thead>
<tbody>
<tr><td class="res">1</td><td>0.16<span class="m">&lambda;</span></td><td>1 : 1 : 1</td></tr>
<tr><td class="res">6</td><td>&asymp; 1<span class="m">&lambda;</span></td><td>1 : 0.17 : 0.03</td></tr>
<tr><td class="res">10</td><td>&asymp; 1.6<span class="m">&lambda;</span></td><td>1 : 0.1 : 0.01</td></tr>
</tbody></table></div>
<p>They fall below about 10% near """ + KR + """ &asymp; 10, i.e. """ + R + """ &asymp; 1.6""" + LAM + """. The 0.62&radic;(""" + D + """<sup>3</sup>/""" + LAM + """) boundary in the next section is this same idea, generalised to an antenna of finite size """ + D + """.</p>"""),

# 11 --------------------------------------------------------------------
("""<h2>Why &ldquo;reactive&rdquo; is the literal word</h2>
<p>Form the complex radial Poynting vector and the cross-terms collapse to just two:</p>
<div class="eq">&frac12;<i>E</i><sub>&theta;</sub><i>H</i><sub>&phi;</sub><sup>&lowast;</sup> &prop;
 <span class="frac"><span>1</span><span><i>r</i><sup>2</sup></span></span> &minus;
 <i>j</i><span class="frac"><span>1</span><span><i>k</i><sup>3</sup><i>r</i><sup>5</sup></span></span></div>
<ul>
  <li><strong>Real part</strong> &mdash; genuine outward power, falling as 1/""" + R + """<sup>2</sup>, the inverse-square law. It contains <strong>no near-field terms at all</strong>: radiation is radiation at every distance.</li>
  <li><strong>Imaginary part</strong> &mdash; reactive power, falling as 1/""" + R + """<sup>5</sup>. The <span class="var">j</span> says <strong>E</strong> and <strong>H</strong> sit 90&deg; apart: energy flows out for a quarter cycle, then all the way back. <strong>Nothing leaves.</strong></li>
</ul>
<div class="callout"><p>The same reactive power you met at the terminals in L4 &mdash; now seen from <em>outside</em> the antenna instead of inside it.</p></div>""",
 "", """<p>Multiplying <i>E</i><sub>&theta;</sub> by <i>H</i><sub>&phi;</sub><sup>&lowast;</sup> term by term, everything cancels except two pieces, with the constant written out:</p>
<div class="eq">&frac12;<i>E</i><sub>&theta;</sub><i>H</i><sub>&phi;</sub><sup>&lowast;</sup> =
 &frac12;<i>&eta;</i><sub>0</sub><span class="paren">(</span><span class="frac"><span><i>kI&thinsp;dl</i>&thinsp;sin&thinsp;<i>&theta;</i></span><span>4<i>&pi;</i></span></span><span class="paren">)</span><sup>2</sup>
 <span class="frac"><span>1</span><span><i>r</i><sup>2</sup></span></span> &minus; <i>j</i>&thinsp;&frac12;<i>&eta;</i><sub>0</sub><span class="paren">(</span><span class="frac"><span><i>kI&thinsp;dl</i>&thinsp;sin&thinsp;<i>&theta;</i></span><span>4<i>&pi;</i></span></span><span class="paren">)</span><sup>2</sup>
 <span class="frac"><span>1</span><span><i>k</i><sup>3</sup><i>r</i><sup>5</sup></span></span></div>
<p>No cross-term between a 1/""" + R + """ field and a 1/""" + R + """<sup>2</sup> field survives the algebra &mdash; which is <em>why</em> the real part carries no near-field content.</p>
<p>The minus sign on the <span class="var">j</span> even tells you the stored energy is predominantly <strong>electric</strong>, which fits: a short dipole is <em>capacitive</em> at its terminals. Its large negative reactance from Lesson 4 and this near-field electric energy are the same physics, seen from the outside versus the inside.</p>"""),

# 12 --------------------------------------------------------------------
("""<h2>The three regions</h2>
<figure>__SVG_REGION__
<figcaption>Not to scale, and the boundaries are gradual, not walls. Both radii depend on antenna size and wavelength.</figcaption></figure>""",
 "", None),

# 13 --------------------------------------------------------------------
("""<h2>Reactive near-field</h2>
<p>Right up against the antenna the field is <strong>stored energy</strong>, not radiation &mdash; the 1/""" + R + """<sup>2</sup> and 1/""" + R + """<sup>3</sup> terms, sloshing in and out each cycle.</p>
<ul>
  <li>Like the field around a charged capacitor or a current-carrying inductor.</li>
  <li>Put a receiver here and it <strong>loads the antenna</strong> and changes its behaviour.</li>
  <li>Which is also why you keep hands, heads, and hardware out of it.</li>
</ul>
<p class="pull">It falls off fast. Take one step out and it is gone.</p>""",
 "", None),

# 14 --------------------------------------------------------------------
("""<h2>Radiating near-field (Fresnel)</h2>
<p>Energy is now genuinely leaving &mdash; <strong>but the shape of the pattern still depends on how far away you are.</strong></p>
<ul>
  <li>Different parts of the antenna are at meaningfully different distances from your observation point.</li>
  <li>Their contributions add with <strong>distance-dependent phase</strong>, so the angular pattern keeps changing as you move out.</li>
  <li>The wavefront is noticeably <strong>curved</strong>.</li>
</ul>
<div class="callout"><p>Measure a pattern here and you have measured <em>this range</em>, not the antenna.</p></div>""",
 "", None),

# 15 --------------------------------------------------------------------
("""<h2>Far-field (Fraunhofer)</h2>
<p>Far enough out, the antenna looks like a <strong>point source</strong>:</p>
<ul>
  <li>fields fall as 1/""" + R + """, power as 1/""" + R + """<sup>2</sup></li>
  <li><strong>E</strong>, <strong>H</strong>, and the direction of propagation are mutually perpendicular</li>
  <li>locally the wave is a <strong>plane wave</strong> &mdash; flat wavefront</li>
</ul>
<p class="pull">Measure at 100 m or at 1 km and you get the same angular pattern, just weaker.</p>""",
 "", """<p>This is the region every antenna specification implicitly refers to. &ldquo;The gain is 15 dBi&rdquo; means <em>in the far field</em> &mdash; and nobody writes that down, because everyone in the field assumes it.</p>"""),

# 16 --------------------------------------------------------------------
("""<h2>The boundaries</h2>
<p>Let """ + D + """ be the antenna&rsquo;s <strong>largest dimension</strong> and """ + LAM + """ the wavelength.</p>
<div class="tablewrap"><table>
<thead><tr><th>Region</th><th>Extent</th><th>Fields</th></tr></thead>
<tbody>
<tr><td class="res">reactive near-field</td><td><span class="m">r</span> &lt; 0.62&radic;(<span class="m">D</span><sup>3</sup>/<span class="m">&lambda;</span>)</td><td>stored, non-radiating; 1/<span class="m">r</span><sup>2</sup>, 1/<span class="m">r</span><sup>3</sup></td></tr>
<tr><td class="res">radiating near-field</td><td>0.62&radic;(<span class="m">D</span><sup>3</sup>/<span class="m">&lambda;</span>) &le; <span class="m">r</span> &lt; 2<span class="m">D</span><sup>2</sup>/<span class="m">&lambda;</span></td><td>radiating, pattern varies with <span class="m">r</span>; curved wavefront</td></tr>
<tr><td class="res">far-field</td><td><span class="m">r</span> &ge; 2<span class="m">D</span><sup>2</sup>/<span class="m">&lambda;</span></td><td>pattern fixed; 1/<span class="m">r</span>; locally a plane wave</td></tr>
</tbody></table></div>
<p class="pull">Not walls &mdash; the fields transition gradually.</p>""",
 "", """<p>These formulas apply to <strong>electrically large</strong> antennas (""" + D + """ &gt; """ + LAM + """), where """ + FF + """ is the meaningful distance. For an electrically <strong>small</strong> antenna the reactive near-field simply extends out to about """ + LAM + """/2<span class="var">&pi;</span> &mdash; precisely the """ + KR + """ = 1 crossover derived from the dipole fields. Take the larger of the two:</p>
<div class="eq"><i>r</i><sub>ff</sub> &asymp; max
 <span class="paren">(</span><span class="frac"><span>2<i>D</i><sup>2</sup></span><span><i>&lambda;</i></span></span>,
 <span class="frac"><span><i>&lambda;</i></span><span>2<i>&pi;</i></span></span><span class="paren">)</span></div>
<p>But do not read """ + LAM + """/2<span class="var">&pi;</span> as &ldquo;the far field begins here&rdquo;. At that radius the stored terms are merely <em>equal</em> to the radiation term, not gone. In practice give a small antenna <strong>a few wavelengths</strong> &mdash; """ + KR + """ of order 10 &mdash; before you trust its pattern.</p>"""),

# 17 --------------------------------------------------------------------
("""<h2>Careful: these are for <em class="term">large</em> antennas</h2>
<p>Both formulas assume an <strong>electrically large</strong> antenna, """ + D + """ &gt; """ + LAM + """ &mdash; the regime where """ + FF + """ means anything.</p>
<p>For a <strong>small</strong> antenna it can come out smaller than a wavelength, which is nonsense: the reactive near field runs to about """ + LAM + """/2<span class="var">&pi;</span>, the """ + KR + """ = 1 crossover we derived.</p>
<div class="eq"><i>r</i><sub>ff</sub> &asymp; max
 <span class="paren">(</span><span class="frac"><span>2<i>D</i><sup>2</sup></span><span><i>&lambda;</i></span></span>,
 <span class="frac"><span><i>&lambda;</i></span><span>2<i>&pi;</i></span></span><span class="paren">)</span></div>
<div class="callout"><p>At """ + LAM + """/2<span class="var">&pi;</span> the stored terms are merely <em>equal</em>, so give a small antenna <strong>a few wavelengths</strong> before you trust the pattern.</p></div>""",
 "", None),

# 18 --------------------------------------------------------------------
("""<h2>Where """ + FF + """ comes from</h2>
<figure>__SVG_PHASE__
<figcaption>The source sits at a finite distance, so the wavefront reaching the aperture is a sphere, not a plane. The far-field distance is the range at which that sphere is flat enough across """ + D + """.</figcaption></figure>""",
 "", None),

# 19 --------------------------------------------------------------------
("""<h2>The phase-error budget</h2>
<p>Extra path from the source to the aperture <strong>edge</strong> over the path to its <strong>centre</strong>:</p>
<div class="eq">&Delta; &asymp; <span class="frac"><span>(<i>D</i>/2)<sup>2</sup></span><span>2<i>r</i></span></span>
 = <span class="frac"><span><i>D</i><sup>2</sup></span><span>8<i>r</i></span></span></div>
<p>Tolerance: &Delta; &le; """ + LAM + """/16, a peak phase error of 22.5&deg; (<span class="var">&pi;</span>/8). Set &Delta; = """ + LAM + """/16:</p>
<div class="eq"><span class="frac"><span><i>D</i><sup>2</sup></span><span>8<i>r</i></span></span>
 = <span class="frac"><span><i>&lambda;</i></span><span>16</span></span> &nbsp;&rArr;&nbsp;
 <i>r</i> = <span class="frac"><span>2<i>D</i><sup>2</sup></span><span><i>&lambda;</i></span></span></div>
<div class="callout"><p>""" + FF + """ is a <strong>budget</strong>, not a wall &mdash; inside it aperture phase distorts the pattern, beyond it the pattern stops changing.</p></div>""",
 "", """<p>Picture a point source a distance """ + R + """ away, radiating a <strong>spherical</strong> wavefront onto an aperture of size """ + D + """. Because the wavefront is a sphere, the path from the source to the <em>edge</em> of the aperture is slightly longer than the path to the <em>centre</em>. A plane wave, by definition, would have no such difference &mdash; and the plane-wave limit is exactly what you earn once this criterion is met.</p>
<p>Inside this distance the phase across the aperture curves enough to distort the pattern; beyond it the wavefront is &ldquo;flat enough&rdquo; and the pattern is stable. That is the whole content of the criterion: a statement about how flat a sphere looks over a finite width, not about where radiation starts.</p>"""),

# 20 --------------------------------------------------------------------
("""<h2>Drive it yourself &mdash; the boundaries</h2>
<p>Hold """ + '<span class="var">f</span>' + """ and double """ + D + """: the far-field distance goes up by <strong>four</strong>. Hold """ + D + """ and double """ + '<span class="var">f</span>' + """: it doubles.</p>
__VIZ_REGIONS__""",
 "viz-frame", None),

# 21 --------------------------------------------------------------------
("""<h2>Worked example &mdash; a 1.2 m dish at 10 GHz</h2>
<div class="tablewrap"><table>
<thead><tr><th>Quantity</th><th>Work</th><th>Result</th></tr></thead>
<tbody>
<tr><td>wavelength</td><td>3&times;10<sup>8</sup> &divide; 10&times;10<sup>9</sup></td><td class="res">0.03 m</td></tr>
<tr><td>electrical size</td><td><span class="m">D</span>/<span class="m">&lambda;</span> = 1.2 &divide; 0.03</td><td class="res">40 &mdash; electrically large</td></tr>
<tr><td>reactive boundary</td><td>0.62&radic;(1.728 &divide; 0.03) = 0.62&radic;57.6</td><td class="res">4.7 m</td></tr>
<tr><td>far-field distance</td><td>2(1.2)<sup>2</sup> &divide; 0.03</td><td class="res">96 m</td></tr>
<tr><td>radiating near-field</td><td>everything between</td><td class="res">4.7 to 96 m</td></tr>
</tbody></table></div>
<p class="pull">Almost a hundred metres of separation to measure a dish you can carry.</p>""",
 "", """<p>Written out, so the arithmetic is checkable:</p>
<div class="eq"><i>&lambda;</i> = <span class="frac"><span><i>c</i></span><span><i>f</i></span></span> =
 <span class="frac"><span>3&times;10<sup>8</sup></span><span>10&times;10<sup>9</sup></span></span> = 0.03 m</div>
<div class="eq"><i>r</i><sub>ff</sub> = <span class="frac"><span>2<i>D</i><sup>2</sup></span><span><i>&lambda;</i></span></span> =
 <span class="frac"><span>2(1.2)<sup>2</sup></span><span>0.03</span></span> = 96 m</div>
<div class="eq"><i>r</i><sub>reactive</sub> = 0.62&radic;<span class="paren">(</span><span class="frac"><span><i>D</i><sup>3</sup></span><span><i>&lambda;</i></span></span><span class="paren">)</span>
 = 0.62&radic;<span class="paren">(</span><span class="frac"><span>1.728</span><span>0.03</span></span><span class="paren">)</span> = 0.62&radic;57.6 &asymp; 4.7 m</div>
<p>Notice the """ + D + """<sup>2</sup>: go to 20 GHz and the far field starts at 192 m for the same dish.</p>"""),

# 22 --------------------------------------------------------------------
("""<h2>Which is why ranges are enormous</h2>
<p>To measure a true pattern, gain, or sidelobe level, the antenna under test must sit in the <strong>far field</strong> of the source &mdash; and the source in the far field of the antenna.</p>
<ul>
  <li>A large dish at high frequency wants <strong>hundreds of metres</strong> of clear, reflection-free range.</li>
  <li>Often impractical, sometimes impossible indoors.</li>
</ul>
<p class="pull">So instead: measure close in, on a surface in the radiating near-field, and propagate the result out mathematically &mdash; near-field scanning, in Module 2.</p>""",
 "", """<p>The far-field distance is not academic &mdash; it sets the size of your test range. That is exactly why <strong>near-field scanning</strong> exists: you measure the fields on a surface <em>close</em> to the antenna, in the radiating near-field, then mathematically propagate them out.</p>
<p>You will see this in Module 2&rsquo;s measurement lessons. But it only works because the near-field distribution <strong>completely determines</strong> the far-field pattern &mdash; which is the subject of the next lesson.</p>"""),

# 23 --------------------------------------------------------------------
("""<h2>Key point</h2>
<div class="callout">
<p>Where you stand changes what you see. Close in, the field is <strong>stored energy</strong> that never leaves. A bit farther out it <strong>radiates, but the pattern is still forming</strong>. Only beyond """ + FF + """ does the antenna show its <strong>true, distance-independent pattern</strong>.</p>
<p>Every gain number, every pattern plot, every sidelobe spec assumes you are out there in the far field.</p>
</div>""",
 "narrow", None),

# 24 --------------------------------------------------------------------
("""<h2>Summary</h2>
<div class="tablewrap"><table>
<thead><tr><th>Symbol / idea</th><th>What it is</th><th>Number to remember</th></tr></thead>
<tbody>
<tr><td class="res">Three field terms</td><td>One dipole equation holds all three regions</td><td>1 : 1/<span class="m">kr</span> : 1/(<span class="m">kr</span>)<sup>2</sup></td></tr>
<tr><td class="res"><span class="m">kr</span> = 1 crossover</td><td>Where all three terms are <em>equal</em> &mdash; not where the far field starts</td><td><span class="m">r</span> = <span class="m">&lambda;</span>/2<span class="m">&pi;</span> &asymp; 0.16<span class="m">&lambda;</span></td></tr>
<tr><td class="res">True far field</td><td>Reactive terms actually negligible</td><td><span class="m">kr</span> &raquo; 1; under 10% near <span class="m">kr</span> &asymp; 10 (<span class="m">r</span> &asymp; 1.6<span class="m">&lambda;</span>)</td></tr>
<tr><td class="res">Reactive near-field edge</td><td>Inner boundary for an electrically large antenna</td><td><span class="m">r</span> = 0.62&radic;(<span class="m">D</span><sup>3</sup>/<span class="m">&lambda;</span>)</td></tr>
<tr><td class="res">Far-field distance</td><td>Outer boundary; pattern stops changing with <span class="m">r</span></td><td><span class="m">r</span> &ge; 2<span class="m">D</span><sup>2</sup>/<span class="m">&lambda;</span></td></tr>
<tr><td class="res">Phase-error tolerance</td><td>What the criterion 2<span class="m">D</span><sup>2</sup>/<span class="m">&lambda;</span> comes from</td><td>&Delta; &le; <span class="m">&lambda;</span>/16, i.e. <span class="m">&pi;</span>/8 = 22.5&deg;</td></tr>
<tr><td class="res">Worked dish</td><td><span class="m">D</span> = 1.2 m at 10 GHz</td><td>reactive to 4.7 m; far field beyond 96 m</td></tr>
</tbody></table></div>""",
 "", None),

# 25 --------------------------------------------------------------------
("""<h2>Practice</h2>
<p>The set opens with a which-term-dominates part: evaluate the ratio 1 : 1/""" + KR + """ : 1/(""" + KR + """)<sup>2</sup> at """ + KR + """ = 0.1 and """ + KR + """ = 10, and name the winner in each. Do it by hand once and the crossover stops being a number to memorise.</p>
<ul>
  <li><a href="../../practice/ECE444_L05_Practice_blank.pdf" target="_blank" rel="noopener">Problem set (PDF)</a></li>
  <li><a href="../../practice/ECE444_L05_Practice_SOLUTIONS.pdf" target="_blank" rel="noopener">Solutions (PDF)</a></li>
</ul>""",
 "narrow", None),

# 26 --------------------------------------------------------------------
("""<h2>Where this is going</h2>
<ul>
  <li>You now know <strong>where</strong> the far-field pattern lives and how far away it starts.</li>
  <li><strong>L6 (Radiation Integrals)</strong> answers <strong>what</strong> that pattern is: given the current on the antenna, one integral produces the far field directly.</li>
  <li>And the criterion comes back immediately &mdash; the quadratic term L6 has to throw away is <strong>exactly</strong> &Delta; &le; """ + LAM + """/16. Same """ + FF + """, derived from the other direction.</li>
</ul>
<p class="pull">Same number, two stories. That is usually a sign you have the physics right.</p>""",
 "", """<p>Watch for one specific move in that derivation. Expanding the distance from a source point to the observer gives a linear term and a quadratic one, and <em>throwing the quadratic term away</em> is what defines the far field. That discarded term is the path difference """ + D + """<sup>2</sup>/8""" + R + """ from this lesson, and the licence to drop it is the <span class="var">&pi;</span>/8 tolerance.</p>
<p>So &ldquo;the far-field approximation&rdquo; in Lesson 6 and """ + R + """ &ge; """ + FF + """ here are the same statement &mdash; one written as an integral, one as a distance.</p>"""),
]


def main():
    global STANDALONE
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--standalone", action="store_true",
                    help="inline the widgets and drop CDN reliance; writes "
                         "<slug>-standalone.html next to this script")
    args = ap.parse_args()
    STANDALONE = args.standalone

    body = []
    for i, (content, cls, depth) in enumerate(FRAMES, 1):
        block = content
        if depth:
            block += '\n<div class="depth">\n' + depth + "\n</div>"
        block = (block
                 .replace("__SVG_CROSS__",  svg("L05-term-crossover.svg"))
                 .replace("__SVG_REGION__", svg("L05-region-diagram.svg"))
                 .replace("__SVG_PHASE__",  svg("L05-phase-error.svg"))
                 .replace("__VIZ_TERMS__",   widget("near-field-terms.html", 520))
                 .replace("__VIZ_REGIONS__", widget("field-regions.html", 600)))
        wrapcls = "wrap narrow" if cls == "narrow" else "wrap"
        framecls = "frame" + (" " + cls if cls and cls != "narrow" else "")
        body.append('<section class="%s" id="f%d">\n<div class="%s">\n%s\n</div>\n</section>'
                    % (framecls, i, wrapcls, block))

    shell = (pathlib.Path(__file__).parent / "frames-shell.html").read_text()
    out = (shell
           .replace("<!--FIGCSS-->", FIGCSS)
           .replace("<!--FRAMES-->", "\n\n".join(body))
           .replace("<!--TOTAL-->", str(len(FRAMES))))

    if STANDALONE:
        dest = pathlib.Path(__file__).parent / (SLUG + "-standalone.html")
    else:
        OUTDIR.mkdir(parents=True, exist_ok=True)
        dest = OUTDIR / (SLUG + ".html")
    dest.write_text(out)
    ndepth = sum(1 for _, _, d in FRAMES if d)
    print("wrote %s  (%d frames, %d with lesson depth, %.0f KB)%s"
          % (dest.relative_to(REPO) if REPO in dest.parents else dest,
             len(FRAMES), ndepth, dest.stat().st_size / 1024,
             "  [standalone]" if STANDALONE else ""))
    return 0


if __name__ == "__main__":
    sys.exit(main())
