/* Shared MathJax canvas-label helper for the ECE 444 viz tools.
   Rule of the house: LaTeX (MathJax) is used ONLY for math symbols; all
   words, units, and numbers are drawn by each tool in the sans-serif UI
   font via ctx.fillText. This module just rasterizes a LaTeX string to a
   crisp image and draws it on a canvas.

   Usage in a tool:
     <script src="mjlabel.js"></script>
     ...
     MJ.setRedraw(drawAll);                 // so labels repaint when ready
     MJ.onReady(() => { MJ.typeset(panelEl); drawAll(); });
     // inside draw():  MJ.draw(ctx, '\\lambda', x, y, 13, color, 'center');
*/
(function () {
  if (window.MJ) return;
  if (!window.MathJax) {
    window.MathJax = { tex: { inlineMath: [['\\(', '\\)']] },
                       svg: { fontCache: 'none' },
                       startup: { typeset: false } };
    var s = document.createElement('script');
    s.src = 'https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-svg.js';
    s.async = true;
    document.head.appendChild(s);
  }
  var cache = new Map(), redraw = null, ready = false;
  var MJ = {
    get ready() { return ready; },
    onReady: function (cb) {
      var wait = function () {
        if (window.MathJax && MathJax.startup && MathJax.startup.promise) {
          MathJax.startup.promise.then(function () { ready = true; cb && cb(); });
        } else { setTimeout(wait, 30); }
      };
      wait();
    },
    typeset: function (el) {
      return (window.MathJax && MathJax.typesetPromise)
        ? MathJax.typesetPromise(el ? [el] : undefined) : Promise.resolve();
    },
    setRedraw: function (fn) { redraw = fn; },
    img: function (tex, color) {
      var key = color + '@@' + tex;
      if (cache.has(key)) return cache.get(key);
      var o = { ready: false, ratio: 1, img: new Image() };
      cache.set(key, o);
      try {
        var node = MathJax.tex2svg(tex, { display: false });
        var svg = node.querySelector('svg');
        var vb = svg.viewBox.baseVal; o.ratio = vb.width / vb.height;
        var str = new XMLSerializer().serializeToString(svg).replace(/currentColor/g, color);
        o.img.onload = function () { o.ready = true; if (redraw) redraw(); };
        o.img.src = 'data:image/svg+xml;charset=utf8,' + encodeURIComponent(str);
      } catch (e) {
        // tex2svg not usable yet — don't poison the cache; retry on a later call
        cache.delete(key);
      }
      return o;
    },
    // width (px) the label will occupy at the given pixel height
    width: function (tex, color, hpx) {
      if (!ready) return 0;
      var o = MJ.img(tex, color); return o.ready ? hpx * o.ratio : 0;
    },
    // draw a LaTeX string centered vertically at y; align 'left'|'center'|'right'
    draw: function (ctx, tex, x, y, hpx, color, align) {
      if (!ready) return 0;
      var o = MJ.img(tex, color); if (!o.ready) return 0;
      var w = hpx * o.ratio, dx = x;
      if (align === 'center') dx = x - w / 2; else if (align === 'right') dx = x - w;
      ctx.drawImage(o.img, dx, y - hpx / 2, w, hpx);
      return w;
    }
  };
  window.MJ = MJ;
})();
