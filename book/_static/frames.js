
(function () {
  var deck   = document.getElementById('deck');
  var frames = Array.prototype.slice.call(deck.querySelectorAll('.frame'));
  var laser  = document.getElementById('laser');
  var spot   = document.getElementById('spot');
  var railfill = document.getElementById('railfill');
  var curEl  = document.getElementById('cur');
  var idx = 0, pointing = false, spotting = false;
  var px = window.innerWidth / 2, py = window.innerHeight / 2;

  document.getElementById('tot').textContent = frames.length;

  /* ---- position ----------------------------------------------------- */
  function setIndex(i, push) {
    i = Math.max(0, Math.min(frames.length - 1, i));
    if (i === idx && !push) return;
    idx = i;
    curEl.textContent = i + 1;
    railfill.style.height = ((i + 1) / frames.length * 100) + '%';
    var id = '#' + frames[i].id;
    /* Deep-linking is a nicety; it must never take the page down. In any
       sandboxed or opaque-origin document -- an about:srcdoc iframe, a
       file:// page -- replaceState throws, and because setIndex runs during
       init the throw aborted the rest of this file: no present/read control,
       no "More detail" expanders, no widget sizing. All of it silently, with
       the page looking fine. */
    try {
      if (location.hash !== id) history.replaceState(null, '', id);
    } catch (err) { /* no addressable history here; carry on */ }
  }

  var io = new IntersectionObserver(function (entries) {
    entries.forEach(function (e) {
      if (e.isIntersecting && e.intersectionRatio > 0.5) {
        setIndex(frames.indexOf(e.target));
      }
    });
  }, { root: deck, threshold: [0.5] });
  frames.forEach(function (f) { io.observe(f); });

  function go(i) {
    i = Math.max(0, Math.min(frames.length - 1, i));
    frames[i].scrollIntoView({ block: 'start' });
    setIndex(i, true);
  }

  /* ---- pointer ------------------------------------------------------- */
  function paint() {
    laser.style.transform = 'translate(' + px + 'px,' + py + 'px)';
    if (spotting) {
      spot.style.background =
        'radial-gradient(circle at ' + px + 'px ' + py + 'px, ' +
        'rgba(0,0,0,0) 0 84px, rgba(0,0,0,.30) 132px, rgba(0,0,0,.66) 230px)';
    }
  }
  window.addEventListener('pointermove', function (e) {
    px = e.clientX; py = e.clientY;
    if (pointing || spotting) paint();
  }, { passive: true });

  function sync() {
    laser.classList.toggle('on', pointing);
    spot.classList.toggle('on', spotting);
    document.body.classList.toggle('pointing', pointing || spotting);
    document.getElementById('btnLaser').setAttribute('aria-pressed', pointing);
    document.getElementById('btnSpot').setAttribute('aria-pressed', spotting);
    /* The panel is usually shut, so the button that opens it has to show that
       something is running. */
    document.getElementById('btnTools').setAttribute('data-active', pointing || spotting);
    paint();
  }
  function toggleLaser() { pointing = !pointing; sync(); }
  function toggleSpot()  { spotting = !spotting; sync(); }

  /* ---- jump index --------------------------------------------------- */
  var indexEl = document.getElementById('index');
  var listEl  = document.getElementById('indexlist');
  var showing = false;
  frames.forEach(function (f, i) {
    /* Sphinx frames title themselves with a rubric, not a heading -- docutils
       will not allow a title node outside a section. The generated prototype
       used h2, so accept both. */
    var h = f.querySelector('h1, h2, p.rubric');
    var li = document.createElement('li');
    var b  = document.createElement('button');
    b.type = 'button';
    b.innerHTML = '<span class="n">' + (i + 1) + '</span><span>' +
                  (h ? h.textContent.trim() : 'Frame ' + (i + 1)) + '</span>';
    b.addEventListener('click', function () { toggleIndex(false); go(i); });
    li.appendChild(b); listEl.appendChild(li);
  });
  function toggleIndex(force) {
    showing = (force === undefined) ? !showing : force;
    if (showing) closePops();
    indexEl.classList.toggle('on', showing);
    document.getElementById('btnIndex').setAttribute('aria-pressed', showing);
    if (showing) {
      var btns = listEl.querySelectorAll('button');
      for (var i = 0; i < btns.length; i++)
        btns[i].setAttribute('aria-current', i === idx);
      btns[idx] && btns[idx].focus();
    }
  }
  document.getElementById('btnIndex').addEventListener('click', function () { toggleIndex(); });
  /* Escape closes it, but a phone has no Escape key. */
  document.getElementById('btnIndexClose')
    .addEventListener('click', function () { toggleIndex(false); });
  indexEl.addEventListener('click', function (e) {
    if (e.target === indexEl) toggleIndex(false);
  });

  /* ---- HUD popovers -------------------------------------------------- */
  /* The implementation, the one-at-a-time rule and the tap-off-the-bar
     dismissal all live in shell.js, so the site button in the same bar plays
     by the same rules as these two. All that is local is what a frame page
     wants when any panel opens: the index overlay out of the way. */
  var shell = window.ECE444;
  var closePops = shell.closePops, anyPopOpen = shell.anyPopOpen;
  shell.onOpen.push(function () { toggleIndex(false); });

  var modePop  = shell.popover('btnMode', 'modepop');
  var toolsPop = shell.popover('btnTools', 'toolspop');

  /* Picking a tool shuts the panel -- you turned the laser on to point at the
     slide, not at the menu. */
  document.getElementById('btnLaser').addEventListener('click', function () {
    toggleLaser(); toolsPop.open(false);
  });
  document.getElementById('btnSpot').addEventListener('click', function () {
    toggleSpot(); toolsPop.open(false);
  });
  document.getElementById('btnFull').addEventListener('click', function () {
    fullscreen(); toolsPop.open(false);
  });

  function fullscreen() {
    if (document.fullscreenElement) document.exitFullscreen();
    else if (document.documentElement.requestFullscreen) document.documentElement.requestFullscreen();
  }
  /* iPhone Safari has never implemented it; the call above would just no-op. */
  if (!document.documentElement.requestFullscreen) {
    document.getElementById('btnFull').hidden = true;
  }

  /* ---- keys ---------------------------------------------------------- */
  document.addEventListener('keydown', function (e) {
    if (e.metaKey || e.ctrlKey || e.altKey) return;
    var t = e.target;
    if (t && (t.tagName === 'INPUT' || t.tagName === 'TEXTAREA' || t.isContentEditable)) return;
    if (showing && e.key !== 'Escape' && e.key !== 'g' && e.key !== 'G') return;
    /* Space advances a frame, which would otherwise swallow the activation of
       whichever popover button has focus. Let the button have those two keys;
       every other shortcut still works with a panel open. */
    if ((e.key === ' ' || e.key === 'Enter') && t && t.closest && t.closest('.pop')) return;
    switch (e.key) {
      case 'ArrowRight': case 'ArrowDown': case 'PageDown': case ' ':
        e.preventDefault(); go(idx + 1); break;
      case 'ArrowLeft': case 'ArrowUp': case 'PageUp':
        e.preventDefault(); go(idx - 1); break;
      case 'Home': e.preventDefault(); go(0); break;
      case 'End':  e.preventDefault(); go(frames.length - 1); break;
      case 'l': case 'L': e.preventDefault(); toggleLaser(); break;
      case 's': case 'S': e.preventDefault(); toggleSpot(); break;
      case 'f': case 'F': e.preventDefault(); fullscreen(); break;
      case 'g': case 'G': e.preventDefault(); toggleIndex(); break;
      case 'p': case 'P':
        e.preventDefault();
        setMode(document.documentElement.getAttribute('data-mode') === 'read' ? 'present' : 'read');
        break;
      case 'd': case 'D':
        e.preventDefault();
        frames[idx] && frames[idx].classList.toggle('open');
        break;
      case 'Escape':
        if (anyPopOpen()) { closePops(); }
        else if (showing) { toggleIndex(false); }
        else if (pointing || spotting) { pointing = spotting = false; sync(); }
        break;
    }
  });

  /* ---- open on the hash the URL asked for ---------------------------- */
  var start = frames.findIndex(function (f) { return '#' + f.id === location.hash; });
  if (start > 0) { frames[start].scrollIntoView({ block: 'start' }); setIndex(start, true); }
  else setIndex(0, true);

  /* ---- size widget iframes from their own content -------------------- */
  function autosize(f) {
    try {
      var d = f.contentDocument;
      if (!d || !d.documentElement) return;
      var h = Math.max(d.documentElement.scrollHeight, d.body ? d.body.scrollHeight : 0);
      if (h > 40) f.style.height = h + 'px';
    } catch (err) { /* leave the fallback height in place */ }
  }
  Array.prototype.forEach.call(
    document.querySelectorAll('iframe.viz[data-autosize]'), function (f) {
      if (f.contentDocument && f.contentDocument.readyState === 'complete') autosize(f);
      f.addEventListener('load', function () { autosize(f); });
      setTimeout(function () { autosize(f); }, 400);
    });

  /* ---- present / read ------------------------------------------------ */
  var segPresent = document.getElementById('btnPresent');
  var segRead    = document.getElementById('btnRead');
  function setMode(m) {
    document.documentElement.setAttribute('data-mode', m);
    segPresent.setAttribute('aria-pressed', m === 'present');
    segRead.setAttribute('aria-pressed', m === 'read');
    /* The panel is usually shut, so the button IS the readout: labelled with
       the mode in force, the way a select shows its current value. */
    document.getElementById('btnMode').textContent = m;
    try { localStorage.setItem('ece444-frames-mode', m); } catch (err) {}
    /* Coming back to present, land on the frame you were reading rather than
       wherever the continuous scroll had got to. */
    if (m === 'present') frames[idx] && frames[idx].scrollIntoView({ block: 'start' });
  }
  var startMode = 'present';
  try { startMode = localStorage.getItem('ece444-frames-mode') || 'present'; } catch (err) {}
  setMode(startMode === 'read' ? 'read' : 'present');
  segPresent.addEventListener('click', function () { setMode('present'); modePop.open(false); });
  segRead.addEventListener('click', function () { setMode('read'); modePop.open(false); });

  /* an inline expander, so a question mid-lecture does not cost you the deck */
  Array.prototype.forEach.call(document.querySelectorAll('.depth'), function (d) {
    var f = d.closest('.frame');
    var b = document.createElement('button');
    b.type = 'button'; b.className = 'more';
    b.textContent = 'More detail  +';
    b.addEventListener('click', function () { f.classList.add('open'); d.focus && d.focus(); });
    d.parentNode.insertBefore(b, d);
  });

  deck.focus({ preventScroll: true });
})();
