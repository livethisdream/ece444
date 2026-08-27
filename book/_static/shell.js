/* ECE 444 -- the course mark and its module pills.
 *
 * Shared by the reading pages and the frame lessons, which otherwise run
 * page.js and frames.js respectively. This is the site's whole header: a mark
 * in the corner, and five module pills that spring out of it on demand.
 *
 * Loaded by both templates, so it must not assume either one's DOM beyond the
 * mark itself.
 */
(function () {
  var nav = document.querySelector('.mark-nav');
  if (!nav) return;
  var btn = document.getElementById('btnMark');
  var pills = document.getElementById('pills');
  if (!btn || !pills) return;

  function open(want) {
    var on = (want === undefined) ? !nav.classList.contains('open') : want;
    nav.classList.toggle('open', on);
    btn.setAttribute('aria-expanded', on);
    /* Out of the tab order while folded away, so keyboard users are not
       walked through five links they cannot see. */
    Array.prototype.forEach.call(pills.querySelectorAll('a'), function (a) {
      if (on) a.removeAttribute('tabindex');
      else a.setAttribute('tabindex', '-1');
    });
    if (on) {
      var first = pills.querySelector('a[aria-current="page"]') || pills.querySelector('a');
      first && first.focus();
    }
  }
  open(false);

  btn.addEventListener('click', function () { open(); });

  document.addEventListener('pointerdown', function (e) {
    if (!nav.classList.contains('open')) return;
    var t = e.target;
    if (!t || !t.closest || !t.closest('.mark-nav')) open(false);
  });

  document.addEventListener('keydown', function (e) {
    if (e.key !== 'Escape' || !nav.classList.contains('open')) return;
    open(false);
    btn.focus();
    /* Let the page's own Escape handling run too -- it may have an overlay or
       a pointer of its own to put away. */
  });

  /* Whatever the page uses to retract its chrome applies here as well. */
  var mo = new MutationObserver(function () {
    if (document.body.classList.contains('chrome-away')) open(false);
  });
  mo.observe(document.body, { attributes: true, attributeFilter: ['class'] });
})();
