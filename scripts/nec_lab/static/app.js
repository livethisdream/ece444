'use strict';
/* nec_lab front end.
 *
 * Vanilla JS and canvas, in the house style: no framework, no build step, and
 * nothing loaded from a CDN, because the lab PCs may have no route to one.
 * Every number on screen came from NEC through the Python API in serve.py --
 * this file solves nothing, it only asks and draws.
 */

const $ = (id) => document.getElementById(id);
const css = (name) => getComputedStyle(document.body).getPropertyValue(name).trim();

const state = {
  solve: null,        // last /api/solve response
  sweep: null,        // last /api/sweep response
  measured: null,     // {cuts: Map, name}
  compare: null,
};

/* ---- talking to the service ------------------------------------------ */

async function api(path, body) {
  const r = await fetch('/api/' + path, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(body || {}),
  });
  const data = await r.json();
  if (!r.ok) throw new Error(data.error || r.statusText);
  return data;
}

function modelArgs() {
  const unit = $('unit').value;
  const len = parseFloat($('length').value);
  const args = {
    freq_mhz: parseFloat($('freq').value),
    radius_mm: parseFloat($('radius').value),
    segments: parseInt($('segments').value, 10),
  };
  if (unit === 'mm') args.length_mm = len; else args.length_lambda = len;
  return args;
}

function sweepArgs() {
  return Object.assign(modelArgs(), {
    start_mhz: parseFloat($('fstart').value),
    stop_mhz: parseFloat($('fstop').value),
    step_mhz: parseFloat($('fstep').value),
  });
}

function status(text, isError) {
  const el = $('status');
  el.textContent = text || ' ';
  el.className = 'status' + (isError ? ' err' : '');
}

async function busy(button, fn) {
  const buttons = [...document.querySelectorAll('button')];
  buttons.forEach((b) => { b.disabled = true; });
  try {
    await fn();
  } catch (err) {
    status(String(err.message || err), true);
  } finally {
    buttons.forEach((b) => { b.disabled = false; });
  }
}

/* ---- canvas plumbing -------------------------------------------------- */

function fit(canvas, aspect) {
  const dpr = window.devicePixelRatio || 1;
  const w = canvas.clientWidth || 360;
  const h = Math.round(w * aspect);
  canvas.width = Math.round(w * dpr);
  canvas.height = Math.round(h * dpr);
  canvas.style.height = h + 'px';
  const ctx = canvas.getContext('2d');
  ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
  ctx.clearRect(0, 0, w, h);
  return { ctx, w, h };
}

function text(ctx, s, x, y, size, color, align) {
  ctx.font = `${size}px ${css('--sans') || 'sans-serif'}`;
  ctx.fillStyle = color;
  ctx.textAlign = align || 'left';
  ctx.textBaseline = 'middle';
  ctx.fillText(s, x, y);
}

/* ---- the polar pattern plot ------------------------------------------- */

/* Every trace is normalized to its own peak. That is not a display
 * convenience: a simulated cut is absolute dBi and a measured cut is raw S21
 * in dB, and they only share an axis once each is referred to its own
 * maximum. The chamber app's compare() makes the same choice. */
function normalize(values) {
  const peak = Math.max(...values.filter(Number.isFinite));
  return values.map((v) => v - peak);
}

function drawPolar() {
  const canvas = $('polar');
  const { ctx, w, h } = fit(canvas, 1.0);
  const floor = parseFloat($('floor').value);
  const cx = w / 2, cy = h / 2 + 4;
  const R = Math.min(w, h) / 2 - 26;

  const grid = css('--grid'), muted = css('--muted');
  ctx.lineWidth = 1;
  for (let db = 0; db >= floor; db -= 10) {
    const r = R * (db - floor) / (0 - floor);
    ctx.beginPath();
    ctx.arc(cx, cy, r, 0, 2 * Math.PI);
    ctx.strokeStyle = db === 0 ? css('--edge2') : grid;
    ctx.stroke();
    if (db < 0) text(ctx, `${db}`, cx + 3, cy - r, 10, muted, 'left');
  }
  ctx.beginPath();
  ctx.moveTo(cx - R, cy); ctx.lineTo(cx + R, cy);
  ctx.moveTo(cx, cy - R); ctx.lineTo(cx, cy + R);
  ctx.strokeStyle = grid; ctx.stroke();
  text(ctx, '0°', cx, cy - R - 12, 11, muted, 'center');
  text(ctx, '90°', cx + R + 14, cy, 11, muted, 'center');
  text(ctx, '180°', cx, cy + R + 12, 11, muted, 'center');
  text(ctx, '270°', cx - R - 14, cy, 11, muted, 'center');
  text(ctx, 'dB below peak', 4, 10, 11, muted, 'left');

  const trace = (angles, values, color, width) => {
    ctx.beginPath();
    let started = false;
    for (let i = 0; i < angles.length; i++) {
      const v = Math.max(values[i], floor);
      const r = R * (v - floor) / (0 - floor);
      const a = (angles[i] - 90) * Math.PI / 180;
      const x = cx + r * Math.cos(a), y = cy + r * Math.sin(a);
      if (!started) { ctx.moveTo(x, y); started = true; } else ctx.lineTo(x, y);
    }
    ctx.strokeStyle = color;
    ctx.lineWidth = width;
    ctx.lineJoin = 'round';
    ctx.stroke();
  };

  if (state.solve) {
    // Blue, green, red: three hues that stay apart in both themes. Amber
    // and the measured red were too close to tell apart in light mode.
    const colors = { 'E-plane': css('--blue'), 'H-plane': css('--trace3') };
    state.solve.cuts.forEach((cut) => {
      trace(cut.angle_deg, normalize(cut.gain_dbi),
            colors[cut.name] || css('--trace3'), 2);
    });
  }
  const meas = currentMeasuredCut();
  if (meas) {
    const rot = parseFloat($('rotate').value) || 0;
    trace(meas.angles.map((a) => a + rot), normalize(meas.values), css('--red'), 1.6);
  }
  if (!state.solve && !meas) {
    text(ctx, 'solve to draw a pattern', cx, cy, 12, muted, 'center');
  }
}

/* ---- the impedance sweep plot ----------------------------------------- */

function drawSweep() {
  const canvas = $('sweep-plot');
  const { ctx, w, h } = fit(canvas, 1.0);
  const muted = css('--muted'), grid = css('--grid');
  const L = 46, Rp = 12, T = 26, B = 34;
  const pts = state.sweep ? state.sweep.sweep : null;
  if (!pts || pts.length < 2) {
    text(ctx, 'sweep to plot R and X', w / 2, h / 2, 12, muted, 'center');
    return;
  }
  const f = pts.map((p) => p.freq_hz / 1e6);
  const vals = pts.flatMap((p) => [p.z_real, p.z_imag]);
  const f0 = Math.min(...f), f1 = Math.max(...f);
  let v0 = Math.min(...vals, 0), v1 = Math.max(...vals);
  const pad = 0.08 * (v1 - v0 || 1);
  v0 -= pad; v1 += pad;
  const X = (v) => L + (w - L - Rp) * (v - f0) / (f1 - f0 || 1);
  const Y = (v) => h - B - (h - T - B) * (v - v0) / (v1 - v0 || 1);

  ctx.lineWidth = 1;
  for (let i = 0; i <= 4; i++) {
    const v = v0 + (v1 - v0) * i / 4;
    ctx.beginPath(); ctx.moveTo(L, Y(v)); ctx.lineTo(w - Rp, Y(v));
    ctx.strokeStyle = grid; ctx.stroke();
    text(ctx, v.toFixed(0), L - 6, Y(v), 10, muted, 'right');
  }
  for (let i = 0; i <= 4; i++) {
    const v = f0 + (f1 - f0) * i / 4;
    ctx.beginPath(); ctx.moveTo(X(v), T); ctx.lineTo(X(v), h - B);
    ctx.strokeStyle = grid; ctx.stroke();
    text(ctx, v.toFixed(0), X(v), h - B + 12, 10, muted, 'center');
  }
  if (v0 < 0 && v1 > 0) {
    ctx.beginPath(); ctx.moveTo(L, Y(0)); ctx.lineTo(w - Rp, Y(0));
    ctx.strokeStyle = css('--edge2'); ctx.stroke();
  }
  text(ctx, 'ohms', 4, 9, 10, muted, 'left');
  text(ctx, 'MHz', w - Rp, h - B + 24, 10, muted, 'right');

  const line = (key, color) => {
    ctx.beginPath();
    pts.forEach((p, i) => {
      const x = X(p.freq_hz / 1e6), y = Y(p[key]);
      i ? ctx.lineTo(x, y) : ctx.moveTo(x, y);
    });
    ctx.strokeStyle = color; ctx.lineWidth = 2; ctx.stroke();
  };
  line('z_real', css('--blue'));
  line('z_imag', css('--red'));

  if (state.sweep.resonant_freq_hz) {
    const x = X(state.sweep.resonant_freq_hz / 1e6);
    ctx.save();
    ctx.setLineDash([4, 3]);
    ctx.beginPath(); ctx.moveTo(x, T); ctx.lineTo(x, h - B);
    ctx.strokeStyle = css('--green'); ctx.lineWidth = 1.5; ctx.stroke();
    ctx.restore();
    text(ctx, 'X = 0', x + 4, T + 8, 10, css('--green'), 'left');
  }
}

/* ---- readouts, rules, deck, tables ------------------------------------ */

function setRo(id, value, cls) {
  const el = $(id);
  el.querySelector('.v').textContent = value;
  el.className = 'ro' + (cls ? ' ' + cls : '');
}

function renderSolve(data) {
  state.solve = data;
  const z = data.z;
  setRo('ro-z', `${z.real.toFixed(1)} ${z.imag >= 0 ? '+' : '-'} j${Math.abs(z.imag).toFixed(1)}`);
  setRo('ro-vswr', data.vswr ? data.vswr.toFixed(2) : '—',
        data.vswr && data.vswr <= 2 ? 'ok' : 'warn');
  const e = data.cuts.find((c) => c.name === 'E-plane') || data.cuts[0];
  setRo('ro-gain', e ? `${e.peak_dbi.toFixed(2)} dBi` : '—');
  setRo('ro-hpbw', e && e.hpbw_deg ? `${e.hpbw_deg.toFixed(1)}°` : '—');
  const g = data.average_power_gain;
  setRo('ro-avg', g === null || g === undefined ? '—' : g.toFixed(4),
        g === null || g === undefined ? '' : (g >= 0.95 && g <= 1.05 ? 'ok' : 'bad'));

  $('deck').textContent = data.deck;
  $('derived').textContent =
    `lambda ${(data.wavelength_m * 1000).toFixed(1)} mm | wire ${(data.length_m * 1000).toFixed(2)} mm `
    + `= ${data.length_lambda.toFixed(4)} lambda | segment ${(data.segment_length_m * 1000).toFixed(2)} mm`;

  $('rules').innerHTML = data.rules.map((r) =>
    `<li class="${r.ok ? 'ok' : 'bad'}"><span class="mark">${r.ok ? 'ok' : '!!'}</span>`
    + `<span>${r.rule}</span><span class="detail">${r.detail}</span></li>`).join('');

  drawPolar();
  runCompare();
}

function renderConvergence(rows) {
  $('conv-panel').hidden = false;
  const head = '<tr><th>N</th><th>R</th><th>X</th><th>gain</th><th>&Delta;/a</th><th>drift</th></tr>';
  const body = rows.map((r) =>
    `<tr class="${r.breaks_8a ? 'flag' : ''}"><td>${r.segments}</td>`
    + `<td>${r.z_real.toFixed(2)}</td><td>${r.z_imag.toFixed(2)}</td>`
    + `<td>${r.gain_dbi.toFixed(2)}</td><td>${r.delta_over_radius.toFixed(1)}</td>`
    + `<td>${r.drift_percent === null ? '—' : r.drift_percent.toFixed(2) + '%'}</td></tr>`).join('');
  $('conv').innerHTML = head + body;
}

/* ---- measured CSV: parse, pick a cut, compare -------------------------- */

/* The column names and the comparison rules mirror
 * usafa-chamber/frontend/src/reference.js, so the RMS this page reports and
 * the one the chamber dashboard reports are the same number. */
const ANGLE_KEYS = ['angle_actual_deg', 'angle_cmd_deg', 'angle_deg', 'angle',
                    'theta_deg', 'theta', 'phi_deg', 'phi', 'deg'];
const VALUE_KEYS = ['mag_db', 'gain_db', 'gain_dbi', 'db', 'amplitude_db',
                    'magnitude_db', 'directivity_db'];
const PARAM_KEYS = ['param', 'parameter', 's_param'];
const FREQ_KEYS = ['freq_hz', 'frequency_hz', 'freq', 'frequency', 'f_hz'];

function splitLine(line) {
  const d = line.includes('\t') ? '\t' : line.includes(';') ? ';' : ',';
  return line.split(d).map((c) => c.trim().replace(/^"|"$/g, ''));
}

function findColumn(header, candidates) {
  const lower = header.map((h) => h.toLowerCase());
  for (const want of candidates) { const i = lower.indexOf(want); if (i >= 0) return i; }
  for (const want of candidates) {
    const i = lower.findIndex((h) => h.includes(want)); if (i >= 0) return i;
  }
  return -1;
}

function parsePattern(csvText) {
  const lines = csvText.split(/\r?\n/)
    .filter((l) => l.trim() && !l.trim().startsWith('#') && !l.trim().startsWith('!'));
  if (lines.length < 2) throw new Error('file has no data rows');
  const header = splitLine(lines[0]);
  const iA = findColumn(header, ANGLE_KEYS), iV = findColumn(header, VALUE_KEYS);
  if (iA < 0 || iV < 0) throw new Error('no angle/dB columns in the header');
  const iP = findColumn(header, PARAM_KEYS), iF = findColumn(header, FREQ_KEYS);
  const cuts = new Map();
  for (let n = 1; n < lines.length; n++) {
    const c = splitLine(lines[n]);
    const angle = parseFloat(c[iA]), value = parseFloat(c[iV]);
    if (!Number.isFinite(angle) || !Number.isFinite(value)) continue;
    const param = iP >= 0 ? (c[iP] || '—') : '—';
    let freq = iF >= 0 ? parseFloat(c[iF]) : NaN;
    if (!Number.isFinite(freq)) freq = null;
    else if (freq > 0 && freq < 1e6) freq *= 1e9;
    const key = `${param}|${freq ?? ''}`;
    if (!cuts.has(key)) cuts.set(key, { param, freq, angles: [], values: [] });
    const cut = cuts.get(key);
    cut.angles.push(angle); cut.values.push(value);
  }
  if (!cuts.size) throw new Error('no numeric rows found');
  for (const cut of cuts.values()) {
    const order = cut.angles.map((_, i) => i).sort((x, y) => cut.angles[x] - cut.angles[y]);
    cut.angles = order.map((i) => cut.angles[i]);
    cut.values = order.map((i) => cut.values[i]);
  }
  return cuts;
}

const wrap180 = (x) => ((x + 180) % 360 + 360) % 360 - 180;

function sampleAt(angles, values, angleDeg, maxGapDeg = 10) {
  let below = null, above = null;
  for (let i = 0; i < angles.length; i++) {
    const d = wrap180(angles[i] - angleDeg);
    if (d <= 0 && (below === null || d > below.d)) below = { d, v: values[i] };
    if (d >= 0 && (above === null || d < above.d)) above = { d, v: values[i] };
  }
  if (!below || !above) {
    const one = below || above;
    return one && Math.abs(one.d) <= maxGapDeg ? one.v : null;
  }
  const gap = above.d - below.d;
  if (gap > 2 * maxGapDeg) return null;
  if (gap === 0) return below.v;
  return below.v + (-below.d / gap) * (above.v - below.v);
}

function currentMeasuredCut() {
  if (!state.measured) return null;
  return state.measured.get($('mcut').value) || null;
}

function runCompare() {
  const meas = currentMeasuredCut();
  const el = $('compare');
  if (!meas || !state.solve) { el.textContent = ' '; return; }
  const sim = state.solve.cuts.find((c) => c.name === 'E-plane') || state.solve.cuts[0];
  const floor = parseFloat($('floor').value);
  const rot = parseFloat($('rotate').value) || 0;
  const simN = normalize(sim.gain_dbi), measN = normalize(meas.values);
  const clamp = (v) => Math.max(v, floor);
  let sumSq = 0, n = 0, worst = 0, at = 0;
  for (let i = 0; i < meas.angles.length; i++) {
    const ref = sampleAt(sim.angle_deg, simN, wrap180(meas.angles[i] + rot));
    if (ref === null) continue;
    const d = clamp(measN[i]) - clamp(ref);
    sumSq += d * d; n++;
    if (Math.abs(d) > Math.abs(worst)) { worst = d; at = meas.angles[i]; }
  }
  el.textContent = n
    ? `measured vs ${sim.name}: RMS ${Math.sqrt(sumSq / n).toFixed(2)} dB, `
      + `worst ${worst.toFixed(2)} dB at ${at.toFixed(1)}°, over ${n} points `
      + `clamped at ${floor} dB`
    : 'no overlapping angles between the measurement and the simulated cut';
}

function download(filename, text) {
  const a = document.createElement('a');
  a.href = URL.createObjectURL(new Blob([text], { type: 'text/csv' }));
  a.download = filename;
  a.click();
  setTimeout(() => URL.revokeObjectURL(a.href), 1000);
}

/* ---- wiring ------------------------------------------------------------ */

$('solve').onclick = () => busy(null, async () => {
  status('solving…');
  renderSolve(await api('solve', modelArgs()));
  status('solved');
});

$('trim').onclick = () => busy(null, async () => {
  status('trimming to resonance…');
  const t = await api('trim', modelArgs());
  if (!t.resonant_length_lambda) { status(t.note || 'no resonance found', true); return; }
  $('unit').value = 'lambda';
  $('length').value = t.resonant_length_lambda.toFixed(4);
  renderSolve(await api('solve', modelArgs()));
  status(`resonant at ${t.resonant_length_lambda.toFixed(4)} lambda `
         + `(${(t.resonant_length_m * 1000).toFixed(2)} mm), R = ${t.r_at_resonance.toFixed(2)} ohm`);
});

$('sweep').onclick = () => busy(null, async () => {
  status('sweeping…');
  state.sweep = await api('sweep', sweepArgs());
  drawSweep();
  $('reslabel').textContent = state.sweep.resonant_freq_hz
    ? `X = 0 at ${(state.sweep.resonant_freq_hz / 1e6).toFixed(2)} MHz, `
      + `R = ${state.sweep.r_at_resonance.toFixed(1)} ohm`
    : 'no zero crossing in this span';
  status('swept');
});

$('converge').onclick = () => busy(null, async () => {
  status('running the convergence study…');
  const data = await api('converge', modelArgs());
  renderConvergence(data.rows);
  status('convergence done');
});

$('expat').onclick = () => busy(null, async () => {
  const r = await api('export/pattern', modelArgs());
  download(r.filename, r.text);
  status(`exported ${r.filename}`);
});

$('exswp').onclick = () => busy(null, async () => {
  const r = await api('export/sweep', sweepArgs());
  download(r.filename, r.text);
  status(`exported ${r.filename}`);
});

$('copy').onclick = () => {
  navigator.clipboard.writeText($('deck').textContent)
    .then(() => status('deck copied'))
    .catch(() => status('could not copy -- select the text instead', true));
};

$('measured').onchange = (ev) => {
  const file = ev.target.files[0];
  if (!file) return;
  const reader = new FileReader();
  reader.onload = () => {
    try {
      state.measured = parsePattern(String(reader.result));
      $('mcut').innerHTML = [...state.measured.entries()].map(([k, c]) =>
        `<option value="${k}">${c.param !== '—' ? c.param + ' @ ' : ''}`
        + `${c.freq ? (c.freq / 1e9).toFixed(4) + ' GHz' : 'no freq'} `
        + `(${c.angles.length} pts)</option>`).join('');
      drawPolar(); runCompare();
      status(`loaded ${file.name}: ${state.measured.size} cut(s)`);
    } catch (err) {
      status(`${file.name}: ${err.message}`, true);
    }
  };
  reader.readAsText(file);
};

$('clearmeas').onclick = () => {
  state.measured = null;
  $('mcut').innerHTML = '';
  $('measured').value = '';
  drawPolar(); runCompare();
  status('overlay cleared');
};

$('mcut').onchange = () => { drawPolar(); runCompare(); };
$('rotate').oninput = () => { drawPolar(); runCompare(); };
$('floor').onchange = () => { drawPolar(); runCompare(); };
$('unit').onchange = () => {
  // Keep the number meaningful when the unit changes rather than reinterpreting
  // 0.5 wavelengths as half a millimeter.
  const f = parseFloat($('freq').value), lam = 299792.458 / f;  // mm
  const v = parseFloat($('length').value);
  $('length').value = $('unit').value === 'mm'
    ? (v * lam).toFixed(2) : (v / lam).toFixed(4);
  $('length').step = $('unit').value === 'mm' ? 0.5 : 0.005;
};

window.addEventListener('resize', () => { drawPolar(); drawSweep(); });

fetch('/api/engine').then((r) => r.json()).then((info) => {
  $('engine').textContent = info.engine;
}).catch(() => { $('engine').textContent = 'engine unknown'; });

drawPolar();
drawSweep();
$('solve').click();
