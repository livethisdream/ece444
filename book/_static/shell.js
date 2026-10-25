/* ECE 444 -- the HUD's popovers, and the site nav that is one of them.
 *
 * Loaded by both the reading pages and the frame lessons, which otherwise run
 * page.js and frames.js respectively. Two jobs:
 *
 *   1. One popover implementation for the whole shell. It used to live in
 *      frames.js, which meant a reading page could not have a panel at all --
 *      page.js carried no-op `closePops`/`anyPopOpen` stubs purely so its
 *      handlers could read the same. Now both pages get the real thing.
 *   2. The site button, which is the only popover present on both.
 *
 * Deliberately does NOT bind Escape. Each shell already handles it in its own
 * order -- close a panel, else the index, else the laser -- and a second
 * handler here would close the panel first and let the page's chain fall
 * through to the wrong step.
 */
(function () {
  var pops = [];
  /* A page adds "and put your own surfaces away" here; opening a panel runs
     them. Keeps the index overlay and a popover from being open at once
     without shell.js knowing what an index is. */
  var onOpen = [];

  function popover(btnId, panelId) {
    var btn = document.getElementById(btnId), panel = document.getElementById(panelId);
    if (!btn || !panel) return null;
    var pop = {
      btn: btn, panel: panel,
      open: function (want) {
        var on = (want === undefined) ? panel.hidden : want;
        if (on) closePops(pop);            /* only one panel at a time */
        panel.hidden = !on;
        btn.setAttribute('aria-expanded', on);
        if (on) {
          place(btn, panel);
          onOpen.forEach(function (fn) { fn(); });
          (panel.querySelector('button, a') || btn).focus({ preventScroll: true });
        }
      },
      isOpen: function () { return !panel.hidden; }
    };
    btn.addEventListener('click', function () { pop.open(); });
    pops.push(pop);
    return pop;
  }

  /* Every panel opens under its own button, and a panel wider than the bar
     is normal -- the bar is a centerd pill only as wide as its contents.
     So clamp to the WINDOW, not to the bar: measure where the button is,
     then pull the panel back if either edge would leave the screen. Done on
     open rather than guessed, because the bar's width changes with its
     labels. */
  var EDGE = 8;
  function place(btn, panel) {
    var bar = panel.parentNode.getBoundingClientRect();
    var w = panel.getBoundingClientRect().width;
    var x = btn.getBoundingClientRect().left;                 /* window coords */
    x = Math.min(x, window.innerWidth - w - EDGE);
    x = Math.max(x, EDGE);
    panel.style.left = (x - bar.left) + 'px';                 /* back to the bar */
    /* A panel that drops down (data-drop) opens above its button instead
       when the window has no room for it below. */
    if (panel.hasAttribute('data-drop')) {
      panel.classList.remove('up');
      var r = panel.getBoundingClientRect(), top = btn.getBoundingClientRect().top;
      if (r.bottom > window.innerHeight - EDGE && top > r.height + EDGE) panel.classList.add('up');
    }
  }

  function closePops(except) {
    pops.forEach(function (p) { if (p !== except) p.open(false); });
  }
  function anyPopOpen() {
    return pops.some(function (p) { return p.isOpen(); });
  }

  window.ECE444 = {
    popover: popover, closePops: closePops, anyPopOpen: anyPopOpen, onOpen: onOpen
  };

  /* The site nav. Rendered only when _config.yml configures one, so this is a
     no-op on a build with no siblings. */
  popover('btnSite', 'sitepop');

  /* The landing page's Modules menu. */
  popover('btnModules', 'modpop');

  /* A tap anywhere off the bar dismisses whatever is open. */
  document.addEventListener('pointerdown', function (e) {
    if (!anyPopOpen()) return;
    var t = e.target;
    if (!t || !t.closest || !t.closest('.hud, .pop-anchor')) closePops();
  });

  /* Whatever the page uses to retract its chrome applies here as well. */
  var mo = new MutationObserver(function () {
    if (document.body.classList.contains('chrome-away')) closePops();
  });
  mo.observe(document.body, { attributes: true, attributeFilter: ['class'] });

  /* ---- help card and first-visit hint ---------------------------------- */
  /* The card is a modal over the page; the hint is one line above the bar,
     shown once per browser. Opening the card by any route counts as having
     seen the hint. Storage can be missing or throw (private windows), and
     then the hint simply shows again next visit. */
  var help = document.getElementById('help'), hint = document.getElementById('helpHint');
  var SEEN = 'ece-shell-help-seen', lastFocus = null;

  function seen() {
    if (hint) hint.hidden = true;
    try { localStorage.setItem(SEEN, '1'); } catch (e) {}
  }
  function helpOpen() { return help && !help.hidden; }
  function toggleHelp(want) {
    if (!help) return;
    var on = (want === undefined) ? help.hidden : want;
    if (on === helpOpen()) return;
    if (on) {
      closePops(); seen();
      lastFocus = document.activeElement;
      help.hidden = false;
      document.getElementById('btnHelpClose').focus({ preventScroll: true });
    } else {
      help.hidden = true;
      if (lastFocus && lastFocus.focus) lastFocus.focus({ preventScroll: true });
    }
  }

  document.addEventListener('click', function (e) {
    var t = e.target;
    if (t && t.closest && t.closest('[data-help]')) { e.preventDefault(); toggleHelp(true); }
  });
  if (help) {
    document.getElementById('btnHelpClose').addEventListener('click', function () { toggleHelp(false); });
    help.addEventListener('click', function (e) { if (e.target === help) toggleHelp(false); });
  }
  if (hint) document.getElementById('btnHintClose').addEventListener('click', seen);

  /* Capture phase, so with the card open the page's own keys (arrows that
     turn frames, G for the index) do not act on the page behind it. */
  document.addEventListener('keydown', function (e) {
    if (e.metaKey || e.ctrlKey || e.altKey) return;
    var t = e.target;
    if (t && (t.tagName === 'INPUT' || t.tagName === 'TEXTAREA' || t.isContentEditable)) return;
    if (e.key === '?') { e.preventDefault(); e.stopImmediatePropagation(); toggleHelp(); return; }
    if (!helpOpen()) return;
    if (e.key === 'Escape') { e.preventDefault(); toggleHelp(false); }
    if (e.key !== 'Tab') e.stopImmediatePropagation();
  }, true);

  /* The hint waits for the page to settle, and stays away from a lesson
     opened straight into present mode -- that is a class in progress. */
  if (hint) {
    var already = false;
    try { already = !!localStorage.getItem(SEEN); } catch (e) {}
    if (!already) setTimeout(function () {
      if (document.documentElement.getAttribute('data-mode') !== 'present' && !helpOpen()) hint.hidden = false;
    }, 800);
  }

  window.ECE444.toggleHelp = toggleHelp;
})();
