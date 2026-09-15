/* =====================================================================
   deck-tools.js — shared chalkboard/annotation runtime for ECE 444 decks
   ---------------------------------------------------------------------
   Adapted from USAFA-ECE/ece-495-ew's dfec-deck.js. Ported the CHALKBOARD
   INTERFACE only — the toolbar, laser pointer, iPad/Pencil guards, and
   print replay — not their slide-layout theme. ECE 444 decks are
   markdown-driven and keep their own course-slides.css look and reveal's
   default 960x700 coordinate system.

   Load AFTER reveal.js and its plugins (markdown, highlight, notes, math,
   chalkboard), then call once from the deck:

       DeckTools.init();

   It owns: the house Reveal config (incl. the touch:false zoom fix), the
   injected toolbar + nav buttons, the chalkboard wiring and button-state
   sync, the .overlay backdrop-filter fix, and print-view annotation replay.
   All toolbar styling lives in course-slides.css.
   ===================================================================== */

window.DeckTools = (function () {
  "use strict";

  /* 1x1 PNGs, inline, so the deck never reaches for the chalkboard plugin's
     img/ directory — that folder is not vendored and every reference to it
     404s. White = board background, transparent = eraser cursor. */
  var WHITE_PX = "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAAC0lEQVR4nGP4DwQACfsD/fteaysAAAAASUVORK5CYII=";
  var CLEAR_PX = "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAAC0lEQVR4nGNgAAIAAAUAAXpeqz8AAAAASUVORK5CYII=";

  /* One source of truth for the marker palette: the chalkboard config below,
     the toolbar swatches, and the print replay all read this. First three are
     USAFA brand (blue-dark, blue, red); last two add contrast. */
  var MARKER_COLORS = [
    'rgba(0,74,133,1)',    /* USAFA blue-dark  #004a85 */
    'rgba(0,103,185,1)',   /* USAFA blue       #0067b9 */
    'rgba(176,30,36,1)',   /* USAFA red        #b01e24 */
    'rgba(29,122,77,1)',   /* green */
    'rgba(230,126,34,1)'   /* orange */
  ];

  /* Per-deck sessionStorage key. Drawings survive reload and travel into the
     ?print-pdf tab; the print replay below reads the same key. */
  var STORAGE = 'ece444-' + location.pathname;

  function byId(id) { return document.getElementById(id); }

  /* ------------------------------------------------------------------
     Chrome markup — injected rather than repeated in every deck file.
     ------------------------------------------------------------------ */
  var TOOLS_HTML =
    '<div class="deck-tools" role="group" aria-label="Deck tools">' +
      '<button id="tool-draw" type="button" title="Draw on this slide (C)" aria-label="Draw on this slide">' +
        '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">' +
        '<path d="M16.5 3.5a2.1 2.1 0 0 1 3 3L8 18l-4 1 1-4z"></path></svg></button>' +
      '<button id="tool-board" type="button" title="Whiteboard (B)" aria-label="Toggle whiteboard">' +
        '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">' +
        '<rect x="3" y="4" width="18" height="13" rx="1.5"></rect><path d="M12 17v3M8.5 20h7"></path></svg></button>' +
      '<span class="swatches" id="swatches" aria-label="Marker colors">' +
      [0,1,2,3,4].map(function (i) {
        return '<button type="button" class="swatch" data-c="' + i + '" title="Marker color" aria-label="Marker color ' + (i+1) + '"></button>';
      }).join('') +
      '<button type="button" class="swatch swatch-eraser" data-c="-1" title="Eraser" aria-label="Eraser">' +
      '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M20 20H9L4 15a2 2 0 0 1 0-3l8-8a2 2 0 0 1 3 0l5 5a2 2 0 0 1 0 3l-8 8"></path></svg>' +
      '</button>' +
      '<button type="button" class="boardnav" id="board-prev" title="Previous board" aria-label="Previous board">' +
      '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M6 14.5 12 8.5l6 6"></path></svg>' +
      '</button>' +
      '<button type="button" class="boardnav" id="board-next" title="Next board" aria-label="Next board">' +
      '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M6 9.5l6 6 6-6"></path></svg>' +
      '</button>' +
      '</span>' +
      '<button id="tool-laser" type="button" title="Laser pointer — point with a fading trail" aria-label="Toggle laser pointer">' +
      '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><circle cx="12" cy="12" r="3.2"></circle><path d="M12 3v3M12 18v3M3 12h3M18 12h3M5.6 5.6l2.1 2.1M16.3 16.3l2.1 2.1M18.4 5.6l-2.1 2.1M7.7 16.3l-2.1 2.1"></path></svg>' +
      '</button>' +
      '<button id="tool-save" type="button" title="Save drawings to a JSON file" aria-label="Save drawings">' +
        '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">' +
        '<path d="M12 3v11"></path><path d="M8 10.5l4 4 4-4"></path><path d="M4 19h16"></path></svg></button>' +
      '<span class="sep"></span>' +
      '<button id="tool-clear" type="button" title="Clear drawings on this slide (double-click: clear ALL slides)" aria-label="Clear drawings">' +
      '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M4 19h16"></path><path d="M7 16 16.5 6.5a2.1 2.1 0 0 1 3 3L10 19H7z"></path><path d="M13 8l3 3"></path></svg>' +
      '</button>' +
      '<button id="tool-fs" type="button" title="Fullscreen" aria-label="Toggle fullscreen">' +
      '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M8 3H4a1 1 0 0 0-1 1v4"></path><path d="M16 3h4a1 1 0 0 1 1 1v4"></path><path d="M8 21H4a1 1 0 0 1-1-1v-4"></path><path d="M16 21h4a1 1 0 0 0 1-1v-4"></path></svg>' +
      '</button>' +
      '<button id="tool-pdf" type="button" title="Export PDF — opens your browser\'s print dialog; choose Save as PDF" aria-label="Export PDF">' +
        '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">' +
        '<path d="M7 8V3h10v5"></path><path d="M5 8h14a2 2 0 0 1 2 2v5h-4v4H7v-4H3v-5a2 2 0 0 1 2-2z"></path></svg></button>' +
    '</div>';

  var NAV_HTML =
    '<div class="deck-nav" role="group" aria-label="Slide navigation">' +
      '<button id="nav-prev" type="button" title="Previous slide" aria-label="Previous slide">' +
        '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">' +
        '<path d="M14.5 5.5 8 12l6.5 6.5"></path></svg></button>' +
      '<button id="nav-next" type="button" title="Next slide" aria-label="Next slide">' +
        '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">' +
        '<path d="M9.5 5.5 16 12l-6.5 6.5"></path></svg></button>' +
    '</div>';

  /* ------------------------------------------------------------------
     Chalkboard button state. Read the plugin's own DOM rather than
     mirroring our clicks, so C / B keyboard toggles stay in sync.
     ------------------------------------------------------------------ */
  function syncTools() {
    var notes = byId('notescanvas');
    var board = byId('chalkboard');
    var draw = byId('tool-draw'), brd = byId('tool-board');
    if (draw) draw.classList.toggle('on', !!notes && notes.style.pointerEvents === 'auto');
    if (brd)  brd.classList.toggle('on',  !!board && getComputedStyle(board).visibility !== 'hidden');
  }

  /* toolbar learns whether an ink mode is active, so the swatches can show;
     board mode additionally reveals the board prev/next buttons */
  function syncSwatches() {
    var notes = byId('notescanvas'), board = byId('chalkboard');
    var boardOn = board && board.style.visibility === 'visible';
    var on = (notes && notes.style.pointerEvents !== 'none') || boardOn;
    var tools = document.querySelector('.deck-tools');
    if (tools) {
      tools.classList.toggle('ink-on', !!on);
      tools.classList.toggle('board-on', !!boardOn);
    }
  }

  /* The plugin animates its toggle, so re-read after the transition. */
  function syncSoon() { setTimeout(function(){syncTools();syncSwatches();}, 60); setTimeout(function(){syncTools();syncSwatches();}, 550); }

  function wireChrome() {
    byId('tool-draw').addEventListener('click', function () {
      RevealChalkboard.toggleNotesCanvas(); syncSoon();
    });
    byId('tool-board').addEventListener('click', function () {
      RevealChalkboard.toggleChalkboard(); syncSoon();
    });
    byId('tool-save').addEventListener('click', downloadAnnotations);
    byId('tool-pdf').addEventListener('click', function () {
      /* Plain _blank (no 'noopener'): an auxiliary same-origin tab inherits
         sessionStorage, which is where chalkboard keeps the drawings. */
      window.open(location.pathname + '?print-pdf', '_blank');
    });
    var sw = byId('swatches');
    var currentColor = 0;                 /* last non-eraser marker index */
    function setInk(idx) {
      RevealChalkboard.colorIndex(idx);
      if (idx >= 0) currentColor = idx;
      sw.querySelectorAll('.swatch').forEach(function (x) {
        x.classList.toggle('on', parseInt(x.getAttribute('data-c'), 10) === idx);
      });
    }
    sw.querySelectorAll('.swatch').forEach(function (b, idx) {
      if (!b.classList.contains('swatch-eraser')) b.style.background = MARKER_COLORS[idx];
      b.addEventListener('click', function () {
        setInk(parseInt(b.getAttribute('data-c'), 10));
      });
    });
    setInk(0);
    var eraserActive = function () {
      var e = sw.querySelector('.swatch-eraser');
      return e && e.classList.contains('on');
    };

    /* Stylus barrel/eraser button (Surface, Wacom, etc.): hold to erase.
       Apple Pencil's double-tap and squeeze are NOT exposed to web pages by
       Safari, so on iPad use the two-finger tap below instead. */
    var barrelPrev = null;
    ['pointerdown', 'pointermove'].forEach(function (type) {
      document.addEventListener(type, function (e) {
        if (e.pointerType !== 'pen') return;
        var barrel = (e.buttons & 32) !== 0 || e.button === 5;
        if (barrel && barrelPrev === null && !eraserActive()) {
          barrelPrev = currentColor; setInk(-1);
        } else if (!barrel && barrelPrev !== null) {
          setInk(barrelPrev); barrelPrev = null;
        }
      }, true);
    });

    /* Two-finger tap on the drawing canvas toggles pen <-> eraser (fingers
       do not draw thanks to palm rejection, so the gesture is free). */
    var lastTwoFinger = 0;
    ['notescanvas', 'chalkboard'].forEach(function (id) {
      var el = byId(id);
      if (!el) return;
      el.addEventListener('touchstart', function (e) {
        if (e.touches.length !== 2) return;
        var now = Date.now();
        if (now - lastTwoFinger < 450) return;
        lastTwoFinger = now;
        setInk(eraserActive() ? currentColor : -1);
        e.preventDefault();
      }, { capture: true, passive: false });
    });

    /* ---- laser pointer: passive trail canvas over the deck ---- */
    var laserOn = false, laserPts = [], laserRAF = null, laserCv = null;
    function laserCanvas() {
      if (laserCv) return laserCv;
      laserCv = document.createElement('canvas');
      laserCv.id = 'laser-canvas';
      /* explicit box (not inset shorthand) for maximum Safari compatibility */
      laserCv.style.cssText = 'position:fixed;top:0;left:0;width:100vw;height:100vh;pointer-events:none;z-index:38;';
      document.body.appendChild(laserCv);
      return laserCv;
    }
    function laserFrame() {
      var cv = laserCanvas(), dpr = window.devicePixelRatio || 1;
      /* Points are stored as raw client coords. Draw them relative to where
         the canvas box ACTUALLY is each frame (rect and clientX/Y share one
         coordinate system), so fullscreen, collapsing browser chrome, pinch
         zoom, or any visual-viewport quirk cannot skew the trail. */
      var r = cv.getBoundingClientRect();
      if (!r.width || !r.height) { laserRAF = null; return; }
      var needW = Math.round(r.width * dpr), needH = Math.round(r.height * dpr);
      if (cv.width !== needW || cv.height !== needH) { cv.width = needW; cv.height = needH; }
      var ctx = cv.getContext('2d');
      ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
      ctx.clearRect(0, 0, r.width, r.height);
      var now = performance.now(), LIFE = 1400;
      laserPts = laserPts.filter(function (pt) { return now - pt.t < LIFE; });
      ctx.lineCap = 'round'; ctx.lineJoin = 'round';
      /* pure fading tail: no glow on segments (glow made sparse points read
         as dots); width tapers with age */
      for (var i = 1; i < laserPts.length; i++) {
        var a = laserPts[i - 1], b = laserPts[i];
        if (b.t - a.t > 280) continue;              /* pen truly lifted: break */
        var k = 1 - (now - b.t) / LIFE;
        var alpha = Math.pow(k, 1.6);
        ctx.strokeStyle = 'rgba(214,45,32,' + (0.7 * alpha).toFixed(3) + ')';
        ctx.lineWidth = 2 + 3.5 * k;
        ctx.beginPath();
        ctx.moveTo(a.x - r.left, a.y - r.top);
        ctx.lineTo(b.x - r.left, b.y - r.top);
        ctx.stroke();
      }
      /* the ONE dot: the live pointer position, gone ~immediately on stop */
      var head = laserPts[laserPts.length - 1];
      if (head && now - head.t < 200) {
        ctx.shadowBlur = 14; ctx.shadowColor = 'rgba(214,45,32,.9)';
        ctx.fillStyle = 'rgba(214,45,32,.95)';
        ctx.beginPath(); ctx.arc(head.x - r.left, head.y - r.top, 5.5, 0, 2 * Math.PI); ctx.fill();
        ctx.shadowBlur = 0;
      }
      if (laserOn || laserPts.length) laserRAF = requestAnimationFrame(laserFrame);
      else laserRAF = null;
    }
    window.addEventListener('pointermove', function (e) {
      if (!laserOn) return;
      var now = performance.now();
      var evs = (e.getCoalescedEvents && e.getCoalescedEvents().length) ? e.getCoalescedEvents() : [e];
      for (var i = 0; i < evs.length; i++) {
        laserPts.push({ x: evs[i].clientX, y: evs[i].clientY, t: now });
      }
      if (!laserRAF) laserRAF = requestAnimationFrame(laserFrame);
    }, true);
    byId('tool-laser').addEventListener('click', function () {
      laserOn = !laserOn;
      this.classList.toggle('on', laserOn);
      if (laserOn) {
        /* pointing and inking are different gestures — leave ink mode */
        if (byId('notescanvas') && byId('notescanvas').style.pointerEvents !== 'none') RevealChalkboard.toggleNotesCanvas();
        syncSoon();
      }
    });

    /* board prev/next proxy the plugin's own (hidden) handle anchors */
    ['board-prev', 'board-next'].forEach(function (id, i) {
      byId(id).addEventListener('click', function () {
        var a = document.getElementById(i === 0 ? 'previousboard' : 'nextboard');
        if (a) a.click();
      });
    });

    byId('tool-clear').addEventListener('click', function () {
      RevealChalkboard.clear();
    });
    byId('tool-clear').addEventListener('dblclick', function () {
      if (window.confirm('Clear drawings on ALL slides?')) RevealChalkboard.resetAll();
    });
    var fsBtn = byId('tool-fs');
    var fsRoot = document.documentElement;
    if (!fsRoot.requestFullscreen && !fsRoot.webkitRequestFullscreen) {
      fsBtn.style.display = 'none';   /* API unavailable (e.g. iPhone) */
    } else {
      fsBtn.addEventListener('click', function () {
        var d = document;
        if (d.fullscreenElement || d.webkitFullscreenElement) {
          (d.exitFullscreen || d.webkitExitFullscreen).call(d);
        } else {
          (fsRoot.requestFullscreen || fsRoot.webkitRequestFullscreen).call(fsRoot);
        }
      });
    }
    byId('nav-prev').addEventListener('click', function () { Reveal.prev(); });
    byId('nav-next').addEventListener('click', function () { Reveal.next(); });
    document.addEventListener('keyup', syncSoon);
  }

  /* Download chalkboard/notes annotations as JSON. The plugin's built-in
     download() always names the file "chalkboard.json"; we name it after the
     deck (derived from the page filename) plus today's date so annotations
     from different lectures don't overwrite each other. */
  function downloadAnnotations() {
    var data = RevealChalkboard.getData();
    var slug = (location.pathname.split('/').pop() || 'slides')
                 .replace(/\.html?$/i, '') || 'slides';
    var d = new Date();
    var pad = function (n) { return (n < 10 ? '0' : '') + n; };
    var stamp = d.getFullYear() + '-' + pad(d.getMonth() + 1) + '-' + pad(d.getDate());
    var a = document.createElement('a');
    a.download = slug + '-annotations-' + stamp + '.json';
    a.href = window.URL.createObjectURL(new Blob([data], { type: 'application/json' }));
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
  }

  /* BUG FIX — reveal 5 styles `.reveal > .overlay` as its frosted modal
     (dark wash + backdrop-filter: blur(6px)); the chalkboard plugin reuses
     that class name for its two full-screen canvas containers, so every slide
     sits under a permanent 6px blur. The stylesheet rule in course-slides.css
     is the primary fix; this re-asserts it inline in case the plugin rebuilds
     its containers after the sheet has parsed. */
  function killBackdropBlur() {
    ['notescanvas', 'chalkboard'].forEach(function (id) {
      var el = byId(id);
      if (el) {
        el.style.setProperty('backdrop-filter', 'none', 'important');
        el.style.setProperty('-webkit-backdrop-filter', 'none', 'important');
      }
    });
  }

  /* iPad + Apple Pencil guards, attached at the capture phase so the
     chalkboard plugin's raw touch/mouse handlers never see the bad input:
     - Palm rejection: Safari tags Pencil contacts touchType 'stylus' and skin
       contacts 'direct'. A palm touch on the canvas both drew and left the
       plugin's stroke state open. preventDefault on the touchstart also stops
       Safari synthesizing mouse events from it.
     - Hover guard: Pencil hover (M2 iPads) arrives as move events with no
       button down; with a stuck-open stroke the plugin drew a line chasing the
       hover point. Moves with buttons===0 never reach the plugin.
     On browsers without touchType nothing is blocked. */
  function guardPencilInput() {
    ['notescanvas', 'chalkboard'].forEach(function (id) {
      var el = byId(id);
      if (!el) return;
      ['touchstart', 'touchmove', 'touchend'].forEach(function (type) {
        el.addEventListener(type, function (e) {
          if (!e.target || e.target.tagName !== 'CANVAS') return;
          var touch = e.changedTouches && e.changedTouches[0];
          if (touch && touch.touchType === 'direct') {
            e.preventDefault();
            e.stopImmediatePropagation();
          }
        }, { capture: true, passive: false });
      });
      ['mousemove', 'pointermove'].forEach(function (type) {
        el.addEventListener(type, function (e) {
          if (e.buttons === 0 || e.pointerType === 'touch') {
            e.stopImmediatePropagation();
          }
        }, true);
      });
    });
  }

  /* The chalkboard plugin prints ONLY board-mode (B) drawings — its
     createPrintout explicitly hides the notes canvas. Draw-on-slide scribbles
     are replayed here from the plugin's own sessionStorage format onto each
     slide's pdf page. */
  function paintScribblesOnPrint() {
    var raw = sessionStorage.getItem(STORAGE);
    if (!raw) return;
    var data;
    try { data = JSON.parse(raw); } catch (e) { return; }
    var m0 = data && data[0];
    if (!m0 || !m0.data || !m0.data.length) return;
    var W = Reveal.getConfig().width, H = Reveal.getConfig().height;
    var scale = 1, xOff = 0, yOff = 0;
    if (m0.width && (m0.width !== W || m0.height !== H)) {
      scale = Math.min(W / m0.width, H / m0.height);
      xOff = (W - m0.width * scale) / 2;
      yOff = (H - m0.height * scale) / 2;
    }
    var slides = Reveal.getSlides();
    m0.data.forEach(function (entry) {
      if (!entry.events || !entry.events.length || !entry.slide) return;
      var section = slides[entry.slide.h];
      if (!section) return;
      var page = section.closest('.pdf-page');
      if (!page) return;
      var cv = document.createElement('canvas');
      cv.width = W; cv.height = H;
      cv.style.cssText = 'position:absolute;top:0;left:0;width:100%;height:100%;z-index:30;pointer-events:none;';
      var ctx = cv.getContext('2d');
      entry.events.forEach(function (ev) {
        if (ev.type === 'draw') {
          ctx.lineWidth = 3;
          ctx.lineCap = 'round';
          ctx.strokeStyle = MARKER_COLORS[ev.color || 0] || MARKER_COLORS[0];
          ctx.beginPath();
          ctx.moveTo(xOff + ev.x1 * scale, yOff + ev.y1 * scale);
          ctx.lineTo(xOff + ev.x2 * scale, yOff + ev.y2 * scale);
          ctx.stroke();
        } else if (ev.type === 'erase') {
          ctx.save();
          ctx.globalCompositeOperation = 'destination-out';
          ctx.beginPath();
          ctx.arc(xOff + ev.x * scale, yOff + ev.y * scale, 20, 0, 2 * Math.PI);
          ctx.fill();
          ctx.restore();
        } else if (ev.type === 'clear') {
          ctx.clearRect(0, 0, W, H);
        }
      });
      page.style.position = 'relative';
      page.appendChild(cv);
    });
  }

  /* Inline any <div data-inline-svg="./fig/x.svg"> by fetching the file and
     dropping its markup into the DOM. An <img>-referenced SVG renders in an
     isolated context and cannot reach the deck's web font, so every such
     diagram falls back to a system font; injected inline, its <text> inherits
     Source Sans Pro like the rest of the slide. Same-origin, tiny, cached. */
  function inlineSVGs() {
    var nodes = document.querySelectorAll('[data-inline-svg]:not([data-inlined])');
    if (!nodes.length) return;
    var jobs = [];
    nodes.forEach(function (el) {
      el.setAttribute('data-inlined', 'pending');   /* claim now, no double-fetch */
      jobs.push(
        fetch(el.getAttribute('data-inline-svg'))
          .then(function (r) { return r.text(); })
          .then(function (t) { el.innerHTML = t; el.setAttribute('data-inlined', '1'); })
          .catch(function () { el.removeAttribute('data-inlined'); })
      );
    });
    Promise.all(jobs).then(function () { Reveal.layout(); });
  }

  /* Placeholders arrive with the markdown, which reveal renders asynchronously
     — often AFTER initialize() resolves — so a one-shot call can run before
     they exist. Watch the slides subtree and inline them as they appear. */
  function watchInlineSVGs() {
    inlineSVGs();
    var slides = document.querySelector('.reveal .slides');
    if (slides && window.MutationObserver) {
      new MutationObserver(function () { inlineSVGs(); })
        .observe(slides, { childList: true, subtree: true });
    }
  }

  /* In the ?print-pdf view: once reveal has built the pdf pages (and the
     chalkboard has painted any stored drawings onto them), explain the flow
     and open the browser's print dialog. 'Save as PDF' as the destination is
     the export. &noprint=1 suppresses the auto-dialog (used by tests). */
  function printViewFlow() {
    if (!/print-pdf/.test(location.search)) return;
    var tries = 0;
    (function waitForPages() {
      if (document.querySelectorAll('.pdf-page').length === 0 && tries++ < 100) {
        return setTimeout(waitForPages, 100);
      }
      setTimeout(function () {
        paintScribblesOnPrint();
        var b = document.createElement('div');
        b.className = 'print-banner';
        b.innerHTML = 'Print layout ready — annotations included. In the print dialog, set the destination to <b>Save as PDF</b>. ' +
          '<button type="button" onclick="window.print()">Open print dialog</button>';
        document.body.appendChild(b);
        if (!/[?&]noprint/.test(location.search)) {
          try { window.print(); } catch (e) {}
        }
      }, 1200);
    })();
  }

  function init() {
    document.body.insertAdjacentHTML('beforeend', TOOLS_HTML + NAV_HTML);

    Reveal.initialize({
      /* 16:9 canvas at 1244x700. Height stays 700 (reveal's default), so
         course-slides.css — tuned to that vertical space — is unchanged; the
         width goes from 960 to 1244 (700 x 16/9) to fill widescreen instead of
         letterboxing 4:3. Reveal scales the whole thing to the viewport, so
         this is aspect ratio only, not resolution. */
      width: 1244,
      height: 700,
      hash: true,
      history: true,
      slideNumber: 'c/t',
      controls: false,            /* the injected .deck-nav replaces them */
      progress: true,

      /* ZOOM FIX — reveal's touch handler blanket-prevents one-finger
         touchmove ("block them all to avoid needless tossing around of the
         viewport in iOS") and reads a pinch's first-landing finger as a swipe,
         so it changed slides mid-pinch and blocked one-finger panning. Off, so
         the browser owns all touch gestures: two-finger pinch = native zoom,
         one finger = pan. Advance via the on-screen arrows / keyboard /
         clicker. */
      touch: false,

      /* one composite page per slide in the print view, not one per fragment */
      pdfSeparateFragments: false,

      mathjax3: {
        mathjax: 'https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js',
        tex: {
          inlineMath: [['$', '$'], ['\\(', '\\)']],
          displayMath: [['$$', '$$'], ['\\[', '\\]']]
        }
      },

      /* Whiteboard course — boardmarkers on both canvases, never chalk. */
      chalkboard: {
        theme: 'whiteboard',
        /* Persist drawings for this tab session so they survive the reload into
           the ?print-pdf view (the print tab inherits sessionStorage because
           tool-pdf opens a normal auxiliary tab — do NOT add 'noopener'). */
        storage: STORAGE,
        boardmarkerWidth: 3,
        background: ['rgba(127,127,127,.1)', WHITE_PX],
        grid: false,
        eraser: { src: CLEAR_PX, radius: 20 },
        boardmarkers: MARKER_COLORS.map(function (c) { return { color: c, cursor: 'crosshair' }; }),
        colorButtons: 5,
        boardHandle: true,
        transition: 400,
        toggleChalkboardButton: false,
        toggleNotesButton: false
      },

      plugins: [RevealMarkdown, RevealHighlight, RevealNotes, RevealMath.MathJax3, RevealChalkboard]
    }).then(function () {
      wireChrome();
      killBackdropBlur();
      guardPencilInput();
      watchInlineSVGs();
      printViewFlow();
      syncTools();
      Reveal.on('slidechanged', syncTools);
      Reveal.layout();
    });
  }

  return { init: init, syncTools: syncTools };
})();
