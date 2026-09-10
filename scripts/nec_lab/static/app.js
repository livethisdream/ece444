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
  types: [],          // the antenna catalog, from /api/types
  // Which half of the page owns the model. The form and the cards are two
  // views of one thing, but only one of them can be the source at a time, so
  // whichever was touched last wins and the badge on the deck panel says so.
  mode: 'form',
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

/* The model always reaches the service as cards. The builder writes them, the
 * editor edits them, and there is exactly one path from here on -- so what the
 * page solves is always what the deck says. */
function modelArgs() {
  return { deck: $('deck').value, average: $('average').checked };
}

function buildArgs() {
  const t = state.types.find((x) => x.key === $('atype').value);
  const params = {};
  (t ? t.params : []).forEach((p) => {
    const el = $('p_' + p.key);
    if (el) params[p.key] = el.value;
  });
  return { type: $('atype').value, params };
}

function sweepArgs() {
  return Object.assign(modelArgs(), {
    start_mhz: parseFloat($('fstart').value),
    stop_mhz: parseFloat($('fstop').value),
    step_mhz: parseFloat($('fstep').value),
  });
}

function setMode(mode, label) {
  state.mode = mode;
  const badge = $('source');
  badge.textContent = label || (mode === 'deck' ? 'edited by hand' : 'from the form');
  badge.className = 'badge' + (mode === 'deck' ? ' cards' : '');
}

/* The form is rendered from the catalog the service serves, so adding an
 * antenna type is a Python change and nothing here has to know about it. */
function renderTypes() {
  $('atype').innerHTML = state.types.map((t) =>
    `<option value="${t.key}">${t.name} (${t.lesson})</option>`).join('');
  renderParams();
}

function renderParams() {
  const t = state.types.find((x) => x.key === $('atype').value);
  if (!t) return;
  $('typenote').innerHTML = `<b>${t.name}</b> &mdash; ${t.summary}`;
  const field = (p) => {
    const id = 'p_' + p.key;
    if (p.unit === 'choice') {
      return `<div><label for="${id}">${p.label}</label>`
           + `<select id="${id}">` + p.choices.map((c) =>
               `<option${c === p.default ? ' selected' : ''}>${c}</option>`).join('')
           + `</select></div>`;
    }
    const unit = p.unit && p.unit !== 'count'
      ? ` <span class="punit">(${p.unit === 'lambda' ? 'wavelengths' : p.unit})</span>` : '';
    return `<div><label for="${id}">${p.label}${unit}</label>`
         + `<input type="number" id="${id}" value="${p.default}" step="${p.step}"`
         + `${p.help ? ` title="${p.help}"` : ''}></div>`;
  };
  // Two to a row, so a nine-parameter Yagi does not become a nine-line column.
  const cells = t.params.map(field);
  let html = '';
  for (let i = 0; i < cells.length; i += 2) {
    html += `<div class="row">${cells[i]}${cells[i + 1] || '<div></div>'}</div>`;
  }
  $('params').innerHTML = html;
}

async function buildAndSolve() {
  const b = await api('build', buildArgs());
  if (b.ok === false) { status(b.error || 'could not build that', true); return false; }
  $('deck').value = b.deck;
  const t = state.types.find((x) => x.key === b.type);
  setMode('deck', `from the ${t ? t.name : b.type} builder`);
  return renderSolve(await api('solve', modelArgs()));
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

/* A typed RP card can be any cut, so traces are colored by position and the
 * legend is built from whatever came back rather than from two fixed names. */
function cutColor(i) {
  return [css('--blue'), css('--trace3'), css('--trace2')][i % 3];
}

function renderLegend() {
  const parts = (state.solve ? state.solve.cuts : []).map((c, i) =>
    `<span><i style="background:${cutColor(i)}"></i>${c.name}</span>`);
  if (currentMeasuredCut()) {
    parts.push(`<span><i style="background:${css('--red')}"></i>measured</span>`);
  }
  $('legend').innerHTML = parts.join('') || '<span>no cuts requested</span>';
}

/* ---- the geometry preview --------------------------------------------- */

/* The mistake this exists to catch: a wire built along x while the pattern cut
 * assumes z, or a source on a segment that is not the one the student means.
 * Neither is visible in a column of coordinates and both are obvious here. */
function drawGeometry() {
  const canvas = $('geom');
  const { ctx, w, h } = fit(canvas, 0.52);
  const muted = css('--muted');
  const geo = state.solve && state.solve.geometry;
  if (!geo || !geo.length) {
    text(ctx, 'solve to draw the geometry', w / 2, h / 2, 12, muted, 'center');
    return;
  }
  const pts = geo.flatMap((g) => [g.a, g.b]);
  const lo = [0, 1, 2].map((i) => Math.min(...pts.map((p) => p[i])));
  const hi = [0, 1, 2].map((i) => Math.max(...pts.map((p) => p[i])));
  const ext = [0, 1, 2].map((i) => hi[i] - lo[i]);
  const NAME = ['x', 'y', 'z'];
  // Vertical axis: whichever the structure is longest along -- z for the
  // course's dipole. Horizontal: the next longest, or a fixed second axis when
  // the model is a single straight wire and there is nothing else to show.
  const rank = [0, 1, 2].sort((a, b) => ext[b] - ext[a]);
  const V = rank[0];
  const H = ext[rank[1]] > 1e-12 ? rank[1] : (V === 0 ? 2 : 0);

  const pad = 26;
  // One scale for both axes -- a wire has to look like a wire, not an ellipse
  // -- but an axis the structure has no extent along must not shrink the
  // drawing, so it contributes no constraint rather than a huge one.
  const fit1 = (avail, e) => (e > 1e-9 ? avail / e : Infinity);
  const scale = Math.min(fit1(w - 2 * pad, ext[H]), fit1(h - 2 * pad, ext[V]));
  const midH = (lo[H] + hi[H]) / 2, midV = (lo[V] + hi[V]) / 2;
  const X = (p) => w / 2 + (p[H] - midH) * scale;
  const Y = (p) => h / 2 - (p[V] - midV) * scale;

  ctx.strokeStyle = css('--grid'); ctx.lineWidth = 1;
  ctx.beginPath(); ctx.moveTo(w / 2, 8); ctx.lineTo(w / 2, h - 8);
  ctx.moveTo(10, h / 2); ctx.lineTo(w - 10, h / 2); ctx.stroke();
  text(ctx, `+${NAME[V]}`, w / 2 + 5, 12, 10, muted, 'left');
  text(ctx, `+${NAME[H]}`, w - 12, h / 2 - 8, 10, muted, 'right');

  geo.forEach((g) => {
    ctx.strokeStyle = css('--blue-dark'); ctx.lineWidth = 3.5; ctx.lineCap = 'round';
    ctx.beginPath(); ctx.moveTo(X(g.a), Y(g.a)); ctx.lineTo(X(g.b), Y(g.b)); ctx.stroke();
    if (g.segments <= 41) {           // segment boundaries, while they are legible
      ctx.strokeStyle = css('--panel'); ctx.lineWidth = 1;
      for (let k = 1; k < g.segments; k++) {
        const t = k / g.segments;
        const p = [0, 1, 2].map((i) => g.a[i] + (g.b[i] - g.a[i]) * t);
        ctx.beginPath();
        ctx.arc(X(p), Y(p), 1.6, 0, 2 * Math.PI);
        ctx.stroke();
      }
    }
    if (g.fed) {
      ctx.strokeStyle = css('--red'); ctx.lineWidth = 5;
      ctx.beginPath();
      ctx.moveTo(X(g.feed_a), Y(g.feed_a));
      ctx.lineTo(X(g.feed_b), Y(g.feed_b));
      ctx.stroke();
      text(ctx, 'feed', X(g.feed_b) + 8, Y(g.feed_b), 10.5, css('--red'), 'left');
    }
    text(ctx, `wire ${g.tag}`, X(g.b) + 6, Y(g.b) - 6, 10.5, muted, 'left');
  });

  // Scale bar: a tenth of a wavelength, so the reader has a size reference in
  // the unit the lab actually thinks in.
  if (state.solve.wavelength_m) {
    const bar = state.solve.wavelength_m / 10;
    const x0 = 12, y0 = h - 12;
    ctx.strokeStyle = muted; ctx.lineWidth = 1.5;
    ctx.beginPath(); ctx.moveTo(x0, y0); ctx.lineTo(x0 + bar * scale, y0); ctx.stroke();
    text(ctx, `lambda/10 = ${(bar * 1000).toFixed(1)} mm`,
         x0 + bar * scale + 6, y0, 10, muted, 'left');
  }
}

/* ---- the deck gloss ---------------------------------------------------- */

function renderGloss(gloss, errors) {
  const g = $('gloss');
  g.innerHTML = (gloss || []).map((line) => {
    const toks = line.tokens.map((t, i) =>
      `<span class="tok${i === 0 ? ' card' : ''}" data-label="${escapeAttr(t.label)}"`
      + ` data-detail="${escapeAttr(t.detail)}" title="${escapeAttr(t.label)}`
      + `${t.detail ? ' -- ' + escapeAttr(t.detail) : ''}">${escapeHtml(t.text)}</span>`
    ).join(' ');
    return `<div class="line${line.ok ? '' : ' bad'}">`
         + `<span class="cardtext">${toks}</span>`
         + `<span class="say">${escapeHtml(line.summary)}</span></div>`;
  }).join('') || '<div class="line"><span class="say">no cards yet</span></div>';

  $('deckerrors').innerHTML = (errors || []).map((e) =>
    `<div class="e"><b>${e.line_no ? 'line ' + e.line_no : 'the deck'}</b>: `
    + `${escapeHtml(e.message)}`
    + (e.hint ? `<span class="hint">${escapeHtml(e.hint)}</span>` : '')
    + `</div>`).join('');
}

function escapeHtml(s) {
  return String(s ?? '').replace(/[&<>]/g, (c) =>
    ({ '&': '&amp;', '<': '&lt;', '>': '&gt;' })[c]);
}
function escapeAttr(s) { return escapeHtml(s).replace(/"/g, '&quot;'); }

/* Hovering a field explains it in one line under the deck. The title
 * attribute carries the same text for keyboard and touch users. */
$('gloss').addEventListener('mouseover', (ev) => {
  const t = ev.target.closest('.tok');
  if (!t) return;
  $('fieldhelp').innerHTML = `<b>${escapeHtml(t.textContent)}</b> &mdash; `
    + escapeHtml(t.dataset.label)
    + (t.dataset.detail ? `: ${escapeHtml(t.dataset.detail)}` : '');
});

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
  if (data.ok === false) {          // a typed card is wrong; keep the old results
    renderGloss(data.gloss, data.errors);
    status(data.errors && data.errors.length
      ? `${data.errors.length} problem(s) in the cards -- see the list beside the deck`
      : 'the deck could not be read', true);
    return false;
  }
  state.solve = data;
  const z = data.z;
  setRo('ro-z', `${z.real.toFixed(1)} ${z.imag >= 0 ? '+' : '-'} j${Math.abs(z.imag).toFixed(1)}`);
  setRo('ro-vswr', data.vswr ? data.vswr.toFixed(2) : '—',
        data.vswr && data.vswr <= 2 ? 'ok' : 'warn');
  const e = data.cuts.find((c) => c.name === 'E-plane') || data.cuts[0];
  setRo('ro-gain', e ? `${e.peak_dbi.toFixed(2)} dBi` : '—');
  setRo('ro-hpbw', e && e.hpbw_deg ? `${e.hpbw_deg.toFixed(1)}°` : '—');
  const g = data.average_power_gain;
  // A typed deck with no averaging RP card has no audit to show. Say which
  // card is missing rather than leaving a dash to be puzzled over.
  setRo('ro-avg', g === null || g === undefined ? 'no ...1001 card' : g.toFixed(4),
        g === null || g === undefined ? 'off' : (g >= 0.95 && g <= 1.05 ? 'ok' : 'bad'));

  renderGloss(data.gloss, []);
  drawGeometry();
  renderLegend();
  $('derived').textContent =
    `lambda ${(data.wavelength_m * 1000).toFixed(1)} mm | wire ${(data.length_m * 1000).toFixed(2)} mm `
    + `= ${data.length_lambda.toFixed(4)} lambda | segment ${(data.segment_length_m * 1000).toFixed(2)} mm`;

  renderRules(data.rules);

  drawPolar();
  runCompare();
  return true;
}

/* One line per rule, not per rule per wire. A 5-element Yagi produced 25 rows
 * of "ok" and a 16-element array would produce 80, which buries the one line
 * that matters. Passing rules collapse to a count; failures are listed by wire,
 * because when a rule fails you need to know which element broke it. */
function renderRules(rules) {
  const byRule = new Map();
  rules.forEach((r) => {
    if (!byRule.has(r.rule)) byRule.set(r.rule, []);
    byRule.get(r.rule).push(r);
  });
  const rows = [];
  for (const [rule, group] of byRule) {
    const bad = group.filter((r) => !r.ok);
    if (!bad.length) {
      const detail = group.length > 1
        ? `ok on all ${group.length} wires` : group[0].detail;
      rows.push(`<li class="ok"><span class="mark">ok</span><span>${rule}</span>`
              + `<span class="detail">${detail}</span></li>`);
    } else {
      bad.forEach((r) => rows.push(
        `<li class="bad"><span class="mark">!!</span>`
        + `<span>${rule}${group.length > 1 ? ` (wire ${r.wire})` : ''}</span>`
        + `<span class="detail">${r.detail}</span></li>`));
      const okCount = group.length - bad.length;
      if (okCount) rows.push(
        `<li class="ok"><span class="mark">ok</span><span>${rule}</span>`
        + `<span class="detail">on the other ${okCount} wire`
        + `${okCount > 1 ? 's' : ''}</span></li>`);
    }
  }
  $('rules').innerHTML = rows.join('');
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
  status('building the cards and solving…');
  if (await buildAndSolve()) status('solved');
});

$('trim').onclick = () => busy(null, async () => {
  status('trimming to resonance…');
  const t = await api('trim', modelArgs());
  if (!t.resonant_length_lambda) { status(t.note || 'no resonance found', true); return; }
  if (t.deck) {
    $('deck').value = t.deck;          // the trim rewrote the driven element
    setMode('deck', 'trimmed to resonance');
  }
  await renderSolve(await api('solve', modelArgs()));
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

$('rundeck').onclick = () => busy(null, async () => {
  setMode('deck');
  status('running your cards...');
  if (await renderSolve(await api('solve', modelArgs()))) status('solved from the cards');
});

$('resetdeck').onclick = () => busy(null, async () => {
  status('rebuilding from the form…');
  if (await buildAndSolve()) status('rebuilt from the form');
});

// Typing in the deck hands it the model, but nothing runs until the button is
// pressed: a half-typed card is not a request to solve.
$('deck').addEventListener('input', () => {
  setMode('deck', 'edited by hand');
  status('cards edited -- press Run these cards');
});

$('atype').addEventListener('change', () => {
  renderParams();
  status('press Build & solve');
});

$('params').addEventListener('input', () => status('press Build & solve'));

$('copy').onclick = () => {
  navigator.clipboard.writeText($('deck').value)
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
window.addEventListener('resize', () => { drawPolar(); drawSweep(); drawGeometry(); });

fetch('/api/engine').then((r) => r.json()).then((info) => {
  $('engine').textContent = info.engine;
}).catch(() => { $('engine').textContent = 'engine unknown'; });

drawPolar();
drawSweep();
drawGeometry();

// The catalog comes over the same POST channel as everything else; only
// /api/engine answers a GET.
api('types').then((info) => {
  state.types = info.types;
  renderTypes();
  return busy(null, async () => { await buildAndSolve(); status('solved'); });
}).catch((err) => status(`could not load the antenna catalog: ${err.message}`, true));

/* ---- the 3D pattern ---------------------------------------------------- */

/* A surface whose radius in each direction is the gain in that direction.
 * Canvas 2D and a painter's algorithm rather than WebGL and a library: the
 * page loads nothing from a CDN by design -- lab machines may have no route to
 * one -- and at a few thousand quads this is fast enough to orbit smoothly. */
const view3d = {
  yaw: -0.6, pitch: 0.35, zoom: 1,
  dragging: false, lastX: 0, lastY: 0,
  data: null,
};

function rotate3(p) {
  const cy = Math.cos(view3d.yaw), sy = Math.sin(view3d.yaw);
  const cp = Math.cos(view3d.pitch), sp = Math.sin(view3d.pitch);
  const x = p[0] * cy - p[1] * sy;
  const y = p[0] * sy + p[1] * cy;
  return [x, y * cp - p[2] * sp, y * sp + p[2] * cp];   // [right, depth, up]
}

/* Blue through green and amber to red, low gain to high. Same hues as the rest
 * of the page, ordered so the peak is the one that shouts. */
function gainColor(t) {
  const stops = [[0.00, [30, 64, 110]], [0.35, [0, 103, 185]],
                 [0.62, [63, 125, 52]], [0.82, [190, 140, 20]],
                 [1.00, [176, 30, 36]]];
  t = Math.min(1, Math.max(0, t));
  for (let i = 1; i < stops.length; i++) {
    if (t <= stops[i][0]) {
      const [a, ca] = stops[i - 1];
      const [b, cb] = stops[i];
      const u = (t - a) / (b - a || 1);
      return ca.map((v, k) => Math.round(v + u * (cb[k] - v)));
    }
  }
  return stops[stops.length - 1][1];
}

function drawSphere3D() {
  const canvas = $('sphere');
  const { ctx, w, h } = fit(canvas, 0.8);
  const muted = css('--muted');
  const d = view3d.data;
  if (!d) {
    text(ctx, 'press Draw sphere', w / 2, h / 2, 12, muted, 'center');
    return;
  }
  const range = parseFloat($('srange').value);
  const peak = d.peak_dbi, floor = peak - range;
  const mode = $('smode').value;
  const R = Math.min(w, h) * 0.36 * view3d.zoom;
  const px = (p) => w / 2 + p[0] * R;
  const py = (p) => h / 2 - p[2] * R;

  // While the mouse is down, draw every other row and column: orbiting stays
  // smooth on a 91 x 181 grid and the shape is unchanged.
  const stride = view3d.dragging && d.theta_deg.length > 40 ? 2 : 1;
  const nT = d.theta_deg.length, nP = d.phi_deg.length;
  const rad = Math.PI / 180;
  // What the radius means. The shape a dipole is remembered by is the linear
  // one; a dB radius is the same data with the small values pushed outward,
  // which is right for judging sidelobes and wrong for judging a beam.
  const radiusFor = (g) => {
    if (mode === "pow") return Math.pow(10, (g - peak) / 10);
    if (mode === "field") return Math.pow(10, (g - peak) / 20);
    return Math.max(0, (g - floor) / (peak - floor || 1));
  };
  const pt = (i, j) => {
    const g = d.gain_dbi[i][j];
    const r = radiusFor(g);
    const th = d.theta_deg[i] * rad, ph = d.phi_deg[j] * rad;
    return rotate3([r * Math.sin(th) * Math.cos(ph),
                    r * Math.sin(th) * Math.sin(ph),
                    r * Math.cos(th)]);
  };

  // Axes first, so the surface sits over them.
  const axis = (v, label) => {
    const a = rotate3([0, 0, 0]), b = rotate3(v);
    ctx.beginPath(); ctx.moveTo(px(a), py(a)); ctx.lineTo(px(b), py(b));
    ctx.strokeStyle = css('--grid'); ctx.lineWidth = 1; ctx.stroke();
    text(ctx, label, px(b) + 4, py(b), 10, muted, 'left');
  };
  axis([1.25, 0, 0], 'x'); axis([0, 1.25, 0], 'y'); axis([0, 0, 1.25], 'z');

  const faces = [];
  for (let i = 0; i + stride < nT; i += stride) {
    for (let j = 0; j + stride < nP; j += stride) {
      const a = pt(i, j), b = pt(i + stride, j);
      const c = pt(i + stride, j + stride), e = pt(i, j + stride);
      const g = (d.gain_dbi[i][j] + d.gain_dbi[i + stride][j]
                 + d.gain_dbi[i + stride][j + stride] + d.gain_dbi[i][j + stride]) / 4;
      if (!Number.isFinite(g)) continue;
      // Flat shade from the face normal so the surface reads as a solid.
      const u = [b[0] - a[0], b[1] - a[1], b[2] - a[2]];
      const v = [e[0] - a[0], e[1] - a[1], e[2] - a[2]];
      const n = [u[1] * v[2] - u[2] * v[1], u[2] * v[0] - u[0] * v[2],
                 u[0] * v[1] - u[1] * v[0]];
      const len = Math.hypot(n[0], n[1], n[2]) || 1;
      const shade = 0.72 + 0.28 * Math.abs(n[1] / len);
      const rgb = gainColor((g - floor) / (peak - floor || 1))
        .map((k) => Math.round(k * shade));
      faces.push({
        depth: (a[1] + b[1] + c[1] + e[1]) / 4,
        pts: [a, b, c, e],
        fill: `rgb(${rgb[0]},${rgb[1]},${rgb[2]})`,
      });
    }
  }
  // Painter's algorithm: farthest first. +y is into the screen after rotation.
  faces.sort((f1, f2) => f2.depth - f1.depth);
  for (const f of faces) {
    ctx.beginPath();
    ctx.moveTo(px(f.pts[0]), py(f.pts[0]));
    for (let k = 1; k < 4; k++) ctx.lineTo(px(f.pts[k]), py(f.pts[k]));
    ctx.closePath();
    ctx.fillStyle = f.fill;
    ctx.fill();
    // Hairline in the same color: closes the seams antialiasing leaves without
    // turning the surface into a wireframe.
    ctx.strokeStyle = f.fill; ctx.lineWidth = 0.6; ctx.stroke();
  }

  // The antenna itself, to scale, so the nulls have something to be along.
  if (d.geometry && d.geometry.length && d.wire_scale) {
    d.geometry.forEach((g) => {
      const a = rotate3(g.a.map((v) => v * d.wire_scale));
      const b = rotate3(g.b.map((v) => v * d.wire_scale));
      ctx.beginPath(); ctx.moveTo(px(a), py(a)); ctx.lineTo(px(b), py(b));
      ctx.strokeStyle = css('--ink'); ctx.lineWidth = 2.5; ctx.stroke();
    });
  }

  // Scale key: what the surface's own radius means.
  const keyW = 84, x0 = 10, y0 = h - 16;
  for (let k = 0; k < keyW; k++) {
    const rgb = gainColor(k / keyW);
    ctx.fillStyle = `rgb(${rgb[0]},${rgb[1]},${rgb[2]})`;
    ctx.fillRect(x0 + k, y0 - 7, 1, 7);
  }
  text(ctx, `${floor.toFixed(0)}`, x0, y0 + 6, 9.5, muted, 'left');
  text(ctx, `${peak.toFixed(1)} dBi`, x0 + keyW, y0 + 6, 9.5, muted, 'right');
}

async function loadSphere() {
  const args = Object.assign(modelArgs(), { step_deg: parseFloat($('sstep').value) });
  const t0 = performance.now();
  const d = await api('sphere', args);
  if (d.ok === false) { renderGloss(d.gloss, d.errors); return false; }
  // The wire is in meters and the pattern radius runs 0 to 1, so the antenna
  // needs a scale of its own to sit inside the surface at a readable size.
  const half = Math.max(...d.geometry.flatMap((g) =>
    [g.a, g.b].map((p) => Math.hypot(p[0], p[1], p[2])))) || 1;
  d.wire_scale = 0.42 / half;
  view3d.data = d;
  drawSphere3D();
  $('s3d').textContent =
    `${d.theta_deg.length} x ${d.phi_deg.length} directions, peak `
    + `${d.peak_dbi.toFixed(2)} dBi at theta ${d.peak_theta_deg.toFixed(0)}, `
    + `phi ${d.peak_phi_deg.toFixed(0)} -- solved in `
    + `${((performance.now() - t0) / 1000).toFixed(2)} s. Drag to rotate, scroll to zoom.`;
  return true;
}

$('draw3d').onclick = () => busy(null, async () => {
  status('solving the whole sphere...');
  if (await loadSphere()) status('sphere drawn');
});

$('exsph').onclick = () => busy(null, async () => {
  const r = await api('export/sphere',
                      Object.assign(modelArgs(), { step_deg: parseFloat($('sstep').value) }));
  download(r.filename, r.text);
  status(`exported ${r.filename}`);
});

$('srange').onchange = drawSphere3D;
$('smode').onchange = drawSphere3D;

(() => {
  const c = $('sphere');
  const down = (x, y) => { view3d.dragging = true; view3d.lastX = x; view3d.lastY = y; };
  const move = (x, y) => {
    if (!view3d.dragging) return;
    view3d.yaw += (x - view3d.lastX) * 0.01;
    view3d.pitch = Math.max(-1.5, Math.min(1.5, view3d.pitch + (y - view3d.lastY) * 0.01));
    view3d.lastX = x; view3d.lastY = y;
    drawSphere3D();
  };
  const up = () => { if (view3d.dragging) { view3d.dragging = false; drawSphere3D(); } };
  c.addEventListener('mousedown', (e) => down(e.clientX, e.clientY));
  window.addEventListener('mousemove', (e) => move(e.clientX, e.clientY));
  window.addEventListener('mouseup', up);
  c.addEventListener('touchstart', (e) => down(e.touches[0].clientX, e.touches[0].clientY),
                     { passive: true });
  c.addEventListener('touchmove', (e) => {
    move(e.touches[0].clientX, e.touches[0].clientY);
    if (view3d.dragging) e.preventDefault();
  }, { passive: false });
  c.addEventListener('touchend', up);
  c.addEventListener('wheel', (e) => {
    e.preventDefault();
    view3d.zoom = Math.max(0.4, Math.min(2.5, view3d.zoom * (e.deltaY < 0 ? 1.1 : 0.9)));
    drawSphere3D();
  }, { passive: false });
})();

window.addEventListener('resize', drawSphere3D);
drawSphere3D();
