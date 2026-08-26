
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
    if (location.hash !== id) history.replaceState(null, '', id);
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

  document.getElementById('btnLaser').addEventListener('click', toggleLaser);
  document.getElementById('btnSpot').addEventListener('click', toggleSpot);
  document.getElementById('btnFull').addEventListener('click', fullscreen);

  function fullscreen() {
    if (document.fullscreenElement) document.exitFullscreen();
    else if (document.documentElement.requestFullscreen) document.documentElement.requestFullscreen();
  }

  /* ---- keys ---------------------------------------------------------- */
  document.addEventListener('keydown', function (e) {
    if (e.metaKey || e.ctrlKey || e.altKey) return;
    var t = e.target;
    if (t && (t.tagName === 'INPUT' || t.tagName === 'TEXTAREA' || t.isContentEditable)) return;
    if (showing && e.key !== 'Escape' && e.key !== 'g' && e.key !== 'G') return;
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
        if (showing) { toggleIndex(false); }
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
  var modeBtn = document.getElementById('btnMode');
  function setMode(m) {
    document.documentElement.setAttribute('data-mode', m);
    modeBtn.textContent = m;
    modeBtn.setAttribute('aria-label', 'Mode: ' + m + '. Press P to switch.');
    try { localStorage.setItem('ece444-frames-mode', m); } catch (err) {}
    if (m === 'present') frames[idx] && frames[idx].scrollIntoView({ block: 'start' });
  }
  var startMode = 'present';
  try { startMode = localStorage.getItem('ece444-frames-mode') || 'present'; } catch (err) {}
  setMode(startMode === 'read' ? 'read' : 'present');
  modeBtn.addEventListener('click', function () {
    setMode(document.documentElement.getAttribute('data-mode') === 'read' ? 'present' : 'read');
  });

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
