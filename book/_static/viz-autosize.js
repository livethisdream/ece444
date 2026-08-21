/* Auto-size the interactive-widget iframes on lesson pages.
 *
 * Why this exists: a widget's height is not a constant. The article column is
 * 688-790px on a desktop but ~358px on a phone, and as the frame narrows the
 * widget's control rows stack (taller) while its canvases shrink (shorter).
 * A single `height="..."` attribute therefore cannot fit every viewport --
 * measured worst case was a 225px overrun on mom-dipole at phone width, which
 * shows up for a reader as an inner scrollbar inside the widget.
 *
 * The height attribute stays in the markup as the no-JS fallback (correct at
 * desktop width); this script refines it to the true content height once the
 * widget has laid out, and again whenever it reflows.
 *
 * Widgets are served from the same origin, so contentDocument is readable.
 * Everything is wrapped defensively: if anything fails, the page keeps the
 * markup height and nothing breaks.
 */
(function () {
  'use strict';

  var PAD = 2;                 // guard against sub-pixel rounding
  var observed = new WeakSet();

  function isViz(frame) {
    var src = frame.getAttribute('src') || '';
    return src.indexOf('/viz/') !== -1 || src.indexOf('viz/') === 0;
  }

  function fit(frame) {
    try {
      var doc = frame.contentDocument;
      if (!doc || !doc.body) return;
      var h = Math.ceil(doc.body.scrollHeight) + PAD;
      if (h > 0 && Math.abs(h - frame.getBoundingClientRect().height) > 1) {
        frame.style.height = h + 'px';
      }
    } catch (e) { /* cross-origin or not ready: keep the markup height */ }
  }

  function watch(frame) {
    if (observed.has(frame)) { fit(frame); return; }
    observed.add(frame);
    fit(frame);
    // Re-fit when the widget's own content reflows (control stacking, MathJax
    // labels typesetting late, a canvas resizing itself).
    try {
      var doc = frame.contentDocument;
      if (doc && doc.body && typeof ResizeObserver === 'function') {
        new ResizeObserver(function () { fit(frame); }).observe(doc.body);
      }
    } catch (e) { /* no ResizeObserver, or not ready: resize handler covers it */ }
  }

  function fitAll() {
    var frames = document.querySelectorAll('iframe');
    for (var i = 0; i < frames.length; i++) {
      if (isViz(frames[i])) watch(frames[i]);
    }
  }

  function onReady() {
    fitAll();
    var frames = document.querySelectorAll('iframe');
    for (var i = 0; i < frames.length; i++) {
      if (isViz(frames[i])) {
        frames[i].addEventListener('load', (function (f) {
          return function () { watch(f); };
        })(frames[i]));
      }
    }
    // Lazy-loaded frames and late layout settle.
    setTimeout(fitAll, 300);
    setTimeout(fitAll, 1500);

    var t = null;
    window.addEventListener('resize', function () {
      if (t) clearTimeout(t);
      t = setTimeout(fitAll, 120);
    });
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', onReady);
  } else {
    onReady();
  }
})();
