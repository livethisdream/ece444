/* Boot the hosted build: no server, everything in the page.
 *
 * Three things have to be standing before app.js may run:
 *
 *   1. NEC-2 as WebAssembly. One module, loaded once. Its memory is
 *      snapshotted while pristine and rewound before every solve, because
 *      nec2c keeps its state in globals and a second run on a dirty module
 *      returns confident nonsense -- measured: 19 of 20 decks wrong.
 *   2. Pyodide, running nec_lab's own Python. Not a port of it: the same
 *      files the local tool and the selftest use.
 *   3. window.NEC_LAB_LOCAL, which app.js calls instead of fetch.
 *
 * Then app.js is injected and the page behaves exactly as it does over HTTP.
 */
(function () {
  'use strict';

  var PY_FILES = window.NEC_LAB_PY_FILES || [];
  var box = document.createElement('div');
  box.id = 'boot';
  box.innerHTML = '<div class="boot-card"><b>Starting the simulator</b>'
    + '<div class="boot-step" id="boot-step">loading…</div>'
    + '<div class="boot-note">First visit downloads about 6 MB — Python and '
    + 'NEC-2, both compiled for the browser. After that it is cached and opens '
    + 'at once, including offline.</div></div>';
  document.body.appendChild(box);
  var step = function (t) { document.getElementById('boot-step').textContent = t; };
  var fail = function (what, err) {
    step('could not start: ' + what + ' — ' + err);
    box.classList.add('failed');
  };

  function script(src) {
    return new Promise(function (res, rej) {
      var el = document.createElement('script');
      el.src = src; el.onload = res; el.onerror = function () { rej(new Error(src)); };
      document.head.appendChild(el);
    });
  }

  (async function () {
    try {
      step('loading the NEC-2 solver…');
      await script('nec2.js');
      var nec = await createNec2({ print: function () {}, printErr: function () {} });
      // The rewind point: every global and the whole heap, before any deck.
      var pristine = new Uint8Array(nec.HEAPU8.slice(0));
      window.necRunDeck = function (deck) {
        nec.HEAPU8.set(pristine);
        nec.FS.writeFile('/in.nec', deck);
        nec.callMain(['-i/in.nec', '-o/out.txt']);
        return nec.FS.readFile('/out.txt', { encoding: 'utf8' });
      };

      step('loading Python…');
      await script('pyodide/pyodide.js');
      var py = await loadPyodide({ indexURL: 'pyodide/' });

      step('loading nec_lab…');
      py.FS.mkdir('/nec_lab');
      await Promise.all(PY_FILES.map(function (f) {
        return fetch('nec_lab/' + f).then(function (r) {
          if (!r.ok) throw new Error(f + ': ' + r.status);
          return r.text();
        }).then(function (src) { py.FS.writeFile('/nec_lab/' + f, src); });
      }));

      step('starting the engine…');
      var handle = py.runPython([
        'import sys, json',
        "sys.path.insert(0, '/')",
        'import js',
        'from nec_lab.api import Api',
        'from nec_lab.engine import WasmEngine',
        '_api = Api(WasmEngine(js.necRunDeck, label="in this page"))',
        'def _handle(path, body):',
        '    return json.dumps(_api.dispatch(path, json.loads(body)))',
        '_handle',
      ].join('\n'));

      window.NEC_LAB_LOCAL = function (path, body) {
        try {
          return Promise.resolve(JSON.parse(handle(path, JSON.stringify(body || {}))));
        } catch (err) {
          return Promise.reject(new Error(String(err.message || err).split('\n').pop()));
        }
      };

      box.remove();
      await script('app.js');
    } catch (err) {
      fail(step === null ? 'startup' : 'startup', err.message || err);
    }
  })();
})();
