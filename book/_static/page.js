/* ECE 444 -- reading-page shell.
 *
 * The HUD, the contents overlay and the scroll rail for a normal (non-frame)
 * page. Deliberately a separate file from frames.js: a reading page has no
 * frames, no present mode and no laser, and frames.js is built around a
 * scroll-snap deck. The popover and overlay behaviour is the same shape in
 * both, which is a dedup worth doing once the shell has settled.
 */
(function () {
  var page    = document.getElementById('page');
  var indexEl = document.getElementById('index');
  var railfill = document.getElementById('railfill');
  var pct     = document.getElementById('pct');
  var showing = false;

  /* ---- scroll progress ------------------------------------------------ */
  function progress() {
    var h = document.documentElement;
    var max = h.scrollHeight - h.clientHeight;
    var p = max > 0 ? Math.min(1, Math.max(0, h.scrollTop / max)) : 1;
    railfill.style.height = (p * 100) + '%';
    pct.textContent = Math.round(p * 100) + '%';
  }
  window.addEventListener('scroll', progress, { passive: true });
  window.addEventListener('resize', progress, { passive: true });

  /* ---- chrome that gets out of the way -------------------------------- */
  /* Reading forward retracts the chip and the bar; scrolling back, or opening
     anything, brings them straight back. Kept off near the top and bottom,
     where there is nothing to collide with and their absence reads as a bug. */
  var lastY = window.scrollY, parked = false;
  function chrome(away) {
    if (away === parked) return;
    parked = away;
    document.body.classList.toggle('chrome-away', away);
  }
  window.addEventListener('scroll', function () {
    var y = window.scrollY;
    var h = document.documentElement;
    var atEdge = y < 180 || y + h.clientHeight > h.scrollHeight - 120;
    if (showing || anyPopOpen() || atEdge) chrome(false);
    else if (y > lastY + 6) chrome(true);
    else if (y < lastY - 6) chrome(false);
    lastY = y;
  }, { passive: true });
  /* Reaching for them with a mouse or the keyboard counts as asking for them. */
  window.addEventListener('pointermove', function (e) {
    if (parked && (e.clientY > innerHeight - 90 || e.clientY < 90)) chrome(false);
  }, { passive: true });
  document.addEventListener('focusin', function (e) {
    if (e.target.closest && e.target.closest('.hud, .mark-nav')) chrome(false);
  });

  /* Nothing pops out of the bar any more -- prev/next moved into the page
     footer and the presenter tools live on frame pages only. anyPopOpen and
     closePops are kept as no-ops so the scroll and Escape handlers below read
     the same in both shells. */
  function closePops() {}
  function anyPopOpen() { return false; }

  /* ---- contents overlay ----------------------------------------------- */
  var qEl = document.getElementById('q');
  /* Autofocusing the search field summons the on-screen keyboard, which eats
     half a phone screen the instant you open the contents -- exactly when you
     wanted to SEE the contents. Focus it only where a keyboard is already
     present; a touch user taps the field when they actually want to type. */
  function wantsKeyboard() {
    try { return window.matchMedia('(pointer: fine)').matches; }
    catch (e) { return false; }
  }
  /* Sphinx resolves the relative path for us; deriving it here would break at
     any nesting depth other than the one it was written for. */
  var SEARCH_URL = document.body.getAttribute('data-search');
  function toggleIndex(force) {
    showing = (force === undefined) ? !showing : force;
    if (showing) closePops();
    indexEl.classList.toggle('on', showing);
    if (showing) chrome(false);
    document.getElementById('btnIndex').setAttribute('aria-pressed', showing);
    if (showing) { markHere(); if (qEl && wantsKeyboard()) qEl.focus(); }
  }
  document.getElementById('btnIndex').addEventListener('click', function () { toggleIndex(); });
  document.getElementById('btnIndexClose').addEventListener('click', function () { toggleIndex(false); });
  indexEl.addEventListener('click', function (e) { if (e.target === indexEl) toggleIndex(false); });

  /* Mark the section you are currently reading in the page-local TOC. */
  function markHere() {
    var links = indexEl.querySelectorAll('.index-pagetoc a');
    var best = null, bestTop = -Infinity;
    for (var i = 0; i < links.length; i++) {
      var id = (links[i].getAttribute('href') || '').replace(/^#/, '');
      var el = id && document.getElementById(id);
      if (!el) continue;
      var top = el.getBoundingClientRect().top;
      if (top <= 120 && top > bestTop) { bestTop = top; best = links[i]; }
      links[i].classList.remove('here');
    }
    if (best) best.classList.add('here');
  }

  /* ---- instant filter over both columns -------------------------------- */
  /* Substring match on what is already in the DOM: no network, no index, fires
     on every keystroke. Enter escalates to Sphinx's full-text search. */
  function filter(term) {
    term = term.trim().toLowerCase();
    indexEl.querySelectorAll('.index-toc li, .index-pagetoc li').forEach(function (li) {
      if (!term) { li.removeAttribute('data-hit'); return; }
      var a = li.querySelector('a');
      var hit = !!(a && a.textContent.toLowerCase().indexOf(term) !== -1);
      /* keep a parent visible when a child matches */
      if (!hit) {
        hit = Array.prototype.some.call(li.querySelectorAll('li a'), function (c) {
          return c.textContent.toLowerCase().indexOf(term) !== -1;
        });
      }
      li.setAttribute('data-hit', hit ? '1' : '0');
    });
    /* A part caption is a sibling of its list, not an item in it, so it
       survives the pass above and leaves "MODULE 5" standing over nothing. */
    indexEl.querySelectorAll('.index-toc .caption, .index-toc p.caption').forEach(function (cap) {
      var list = cap.nextElementSibling;
      var live = list && list.querySelector('li:not([data-hit="0"])');
      cap.style.display = (!term || live) ? '' : 'none';
    });
    /* And say so when a column has nothing left, rather than showing a
       heading over blank space. */
    indexEl.querySelectorAll('.index-toc, .index-pagetoc').forEach(function (col) {
      var note = col.querySelector('.index-empty');
      var live = col.querySelector('li:not([data-hit="0"])');
      if (term && !live) {
        if (!note) {
          note = document.createElement('p');
          note.className = 'index-empty';
          note.textContent = 'No match here.';
          col.appendChild(note);
        }
        note.style.display = '';
      } else if (note) {
        note.style.display = 'none';
      }
    });
  }
  if (qEl) {
    qEl.addEventListener('input', function () { filter(qEl.value); });
    qEl.addEventListener('keydown', function (e) {
      if (e.key === 'Enter') {
        e.preventDefault();
        var q = qEl.value.trim();
        if (q) location.href = SEARCH_URL + '?q=' + encodeURIComponent(q);
      }
    });
  }
  /* ---- top ------------------------------------------------------------- */
  document.getElementById('btnTop').addEventListener('click', function () {
    window.scrollTo({ top: 0, behavior: 'smooth' });
  });

  /* ---- keys ------------------------------------------------------------ */
  document.addEventListener('keydown', function (e) {
    if (e.metaKey || e.ctrlKey || e.altKey) return;
    var t = e.target;
    if (t && (t.tagName === 'INPUT' || t.tagName === 'TEXTAREA' || t.isContentEditable)) {
      if (e.key === 'Escape') { toggleIndex(false); document.activeElement.blur(); }
      return;
    }
    switch (e.key) {
      case 'g': case 'G': e.preventDefault(); toggleIndex(); break;
      /* Typing "/" is itself a keyboard action, so land in the field
         regardless of what the pointer says. */
      case '/': e.preventDefault(); toggleIndex(true); qEl && qEl.focus(); break;
      case 'Escape':
        if (anyPopOpen()) closePops();
        else if (showing) toggleIndex(false);
        break;
    }
  });

  /* ---- let only the blocks that overflow scroll ------------------------ */
  /* A long run of inline math cannot wrap. Rather than make every block a
     scroll container -- which turns on overflow-y and clips tall radicals --
     measure first and tag only what actually needs it. Re-run on resize,
     because what overflows at 390px does not at 1280. */
  function tagOverflow() {
    Array.prototype.forEach.call(
      document.querySelectorAll('.page p, .page li, .page dd'), function (el) {
        el.classList.remove('scrolls-x');
        /* Never inside a table: the table already sits in its own scroll box,
           so a second one on the cell buys nothing and shaves the overbar off
           a tall radical that overflows the cell vertically. */
        if (el.closest('table')) return;
        if (el.scrollWidth > el.clientWidth + 1) el.classList.add('scrolls-x');
      });
  }
  var tagTimer;
  window.addEventListener('resize', function () {
    clearTimeout(tagTimer); tagTimer = setTimeout(tagOverflow, 150);
  }, { passive: true });
  if (document.fonts && document.fonts.ready) document.fonts.ready.then(tagOverflow);
  window.addEventListener('load', tagOverflow);
  tagOverflow();

  /* ---- give a bare table somewhere to scroll --------------------------- */
  /* Sphinx wraps the tables it generates in .pst-scrollable-table-container,
     but a table written as raw HTML in a lesson -- the syllabus grade scale --
     gets nothing, and overflows the page on a phone. Wrapping in the DOM keeps
     the table's own layout intact, which `display: block` on the table would
     not. */
  Array.prototype.forEach.call(document.querySelectorAll('.page table'), function (t) {
    if (t.closest('.pst-scrollable-table-container, .table-scroll')) return;
    var box = document.createElement('div');
    box.className = 'table-scroll';
    t.parentNode.insertBefore(box, t);
    box.appendChild(t);
  });

  /* Widget iframes are sized by _static/viz-autosize.js, which is kept on
     reading pages by _ext/frames.py. It uses a ResizeObserver and handles
     reflow; do not reimplement it here. */

  progress();
})();
