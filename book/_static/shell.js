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
          (panel.querySelector('button, a') || btn).focus();
        }
      },
      isOpen: function () { return !panel.hidden; }
    };
    btn.addEventListener('click', function () { pop.open(); });
    pops.push(pop);
    return pop;
  }

  /* Every panel opens under its own button, and a panel wider than the bar
     is normal -- the bar is a centred pill only as wide as its contents.
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

  /* A tap anywhere off the bar dismisses whatever is open. */
  document.addEventListener('pointerdown', function (e) {
    if (!anyPopOpen()) return;
    var t = e.target;
    if (!t || !t.closest || !t.closest('.hud')) closePops();
  });

  /* Whatever the page uses to retract its chrome applies here as well. */
  var mo = new MutationObserver(function () {
    if (document.body.classList.contains('chrome-away')) closePops();
  });
  mo.observe(document.body, { attributes: true, attributeFilter: ['class'] });
})();
