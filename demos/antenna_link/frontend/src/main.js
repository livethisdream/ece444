/* ECE 444 Antenna Link - frontend logic
 * Talks to antenna_link.py over a WebSocket, renders a live power strip chart
 * and a polar antenna pattern with a cos^2(theta) theory overlay.
 */

"use strict";

const WS_PORT = 8765;
const FPS = 20;                 // server streams ~20 Hz
const HISTORY = 300;            // strip-chart samples kept (~15 s)
const FLOOR_DB = -40;           // polar plot radial floor
const HOLD_MS = 1500;           // press-and-hold duration to clear the reference

const state = {
  ws: null,
  connected: false,             // link (radio) connected
  streaming: false,
  sim: false,
  refSet: false,
  powers: [],                   // rolling dBFS history
  pattern: [],                  // [{angle, rel_db, abs_dbfs}]
  refDbfs: null,
  pending: [],                  // FIFO command-response resolvers
};

const $ = (id) => document.getElementById(id);

/* ----------------------------------------------------------------- */
/* WebSocket                                                          */
/* ----------------------------------------------------------------- */
function connectWs() {
  const ws = new WebSocket(`ws://${location.hostname}:${WS_PORT}`);
  state.ws = ws;

  ws.onopen = async () => {
    setStatus("ready", "Server connected");
    const cfg = await send("get_config");
    if (cfg && cfg.config) applyConfig(cfg.config);
  };

  ws.onclose = () => {
    setStatus("", "Server disconnected");
    state.connected = false;
    // Try to reconnect after a moment (server may still be starting).
    setTimeout(connectWs, 1500);
  };

  ws.onmessage = (ev) => {
    let msg;
    try { msg = JSON.parse(ev.data); } catch { return; }
    if (msg.type === "power") {
      onPower(msg.data);
    } else {
      // Command response (has a `status` field). Resolve FIFO.
      const resolve = state.pending.shift();
      if (resolve) resolve(msg);
    }
  };
}

function send(cmd, data = {}) {
  return new Promise((resolve) => {
    if (!state.ws || state.ws.readyState !== WebSocket.OPEN) { resolve(null); return; }
    state.pending.push(resolve);
    state.ws.send(JSON.stringify({ cmd, data }));
  });
}

function applyConfig(cfg) {
  state.sim = !!cfg.sim;
  state.connected = !!cfg.connected;
  state.refDbfs = cfg.ref_dbfs;
  state.refSet = cfg.ref_dbfs !== null && cfg.ref_dbfs !== undefined;
  state.pattern = cfg.pattern || [];

  $("center-freq").value = (cfg.center_freq / 1e9).toFixed(3);
  setSlider("rx-gain", "val-rx-gain", cfg.rx_gain);
  setSlider("tx-gain", "val-tx-gain", cfg.tx_gain);

  // Simulation UI is shown only while the backend is in sim mode.
  $("sim-section").style.display = state.sim ? "" : "none";
  if (state.sim) setSlider("sim-angle", "val-sim-angle", cfg.sim_angle || 0);

  if (state.connected) setStatus("connected", state.sim ? "Simulation" : "Pluto connected");

  updateRefUI();
  updatePatternChart();
  updatePatternCount();

  // A --sim launch starts in sim mode but unconnected: kick it off once.
  if (state.sim && !state.connected && !state._simPending) startSim();
}

/* ----------------------------------------------------------------- */
/* Link (radio) connect                                              */
/* ----------------------------------------------------------------- */
async function connectLink() {
  const host = $("pluto-host").value.trim();
  const uri = host.startsWith("ip:") ? host : `ip:${host}`;
  showConn("Connecting...", "");
  const res = await send("connect", { uri });
  if (res && res.status === "ok") {
    state.sim = false;
    state.connected = true;
    setStatus("connected", "Pluto connected");
    showConn("Connected.", "success");
    if (res.config) applyConfig(res.config);
  } else {
    state.connected = false;
    setStatus("ready", "Connect failed");
    showConn(res ? (res.message || "Connection failed") : "No server", "error");
  }
  updateRefUI();
}

async function startSim() {
  state._simPending = true;
  showConn("Starting simulation...", "");
  const res = await send("start_sim");
  state._simPending = false;
  if (res && res.status === "ok") {
    state.sim = true;
    state.connected = true;
    setStatus("connected", "Simulation");
    showConn("Simulation ready.", "success");
    if (res.config) applyConfig(res.config);
  } else {
    showConn(res ? (res.message || "Sim start failed") : "No server", "error");
  }
  updateRefUI();
}

function updateRefUI() {
  $("btn-ref").disabled = !state.connected;
}

/* ----------------------------------------------------------------- */
/* Streaming                                                         */
/* ----------------------------------------------------------------- */
async function toggleStream() {
  if (state.streaming) {
    await send("stop");
    state.streaming = false;
    $("btn-stream").textContent = "Start";
    $("btn-stream").classList.remove("running");
    return;
  }
  if (!state.connected) {
    await connectLink();
    if (!state.connected) return;
  }
  state.powers = [];
  await send("start");
  state.streaming = true;
  $("btn-stream").textContent = "Stop";
  $("btn-stream").classList.add("running");
}

function onPower(d) {
  // Readouts
  $("rd-power").textContent = d.power_dbfs.toFixed(1);
  $("rd-rel").textContent = (d.rel_db === null || d.rel_db === undefined)
    ? "--" : (d.rel_db >= 0 ? "+" : "") + d.rel_db.toFixed(1);

  const card = $("card-power");
  card.classList.toggle("alert", d.saturated);
  card.querySelector(".readout-label").textContent =
    d.saturated ? "Received power - CLIPPING" : "Received power";

  if (d.ref_dbfs !== null && d.ref_dbfs !== undefined) {
    state.refDbfs = d.ref_dbfs;
    state.refSet = true;
  }

  // Strip chart history
  state.powers.push(d.power_dbfs);
  if (state.powers.length > HISTORY) state.powers.shift();
  updatePowerChart();
}

/* ----------------------------------------------------------------- */
/* Plotly - colors follow the theme                                  */
/* ----------------------------------------------------------------- */
function themeColors() {
  const dark = document.documentElement.getAttribute("data-theme") !== "light";
  return {
    paper: "rgba(0,0,0,0)",
    plot: "rgba(0,0,0,0)",
    font: dark ? "#cbd5e1" : "#334155",
    grid: dark ? "rgba(255,255,255,0.08)" : "rgba(15,23,42,0.10)",
    line: "#0088d1",
    accent: "#10b981",
    theory: dark ? "rgba(148,163,184,0.9)" : "rgba(71,85,105,0.9)",
  };
}

function initCharts() {
  const c = themeColors();
  Plotly.newPlot("chart-power", [{
    y: [], mode: "lines", line: { color: c.line, width: 2 }, name: "Power",
  }], powerLayout(c), { displayModeBar: false, responsive: true });

  Plotly.newPlot("chart-pattern", patternTraces(c), patternLayout(c),
    { displayModeBar: false, responsive: true });
}

function powerLayout(c) {
  return {
    margin: { l: 52, r: 16, t: 10, b: 34 },
    paper_bgcolor: c.paper, plot_bgcolor: c.plot,
    font: { color: c.font, size: 12 },
    xaxis: { title: "seconds ago", gridcolor: c.grid, zeroline: false,
             color: c.font, autorange: "reversed" },
    yaxis: { title: "power (dBFS)", gridcolor: c.grid, zeroline: false,
             color: c.font, range: [-60, 0] },
    showlegend: false,
  };
}

function updatePowerChart() {
  const n = state.powers.length;
  const x = state.powers.map((_, i) => (n - 1 - i) / FPS); // seconds ago
  const c = themeColors();
  const shapes = [];
  if (state.refSet && state.refDbfs !== null) {
    shapes.push({
      type: "line", xref: "paper", x0: 0, x1: 1,
      yref: "y", y0: state.refDbfs, y1: state.refDbfs,
      line: { color: c.accent, width: 1.5, dash: "dash" },
    });
  }
  Plotly.react("chart-power",
    [{ x, y: state.powers, mode: "lines", line: { color: c.line, width: 2 } }],
    Object.assign(powerLayout(c), { shapes }),
    { displayModeBar: false, responsive: true });
}

function patternTraces(c) {
  // Theory: cos^2(theta) in dB.
  const th = [];
  const r = [];
  for (let a = -180; a <= 180; a += 2) {
    th.push(a);
    const db = 20 * Math.log10(Math.abs(Math.cos(a * Math.PI / 180)) + 1e-6);
    r.push(Math.max(db, FLOOR_DB));
  }
  const pts = state.pattern.slice().sort((p, q) => p.angle - q.angle);
  const pa = pts.map((p) => p.angle);
  const pr = pts.map((p) => Math.max(p.rel_db, FLOOR_DB));
  // close the measured loop if it spans a full turn
  return [
    { type: "scatterpolar", mode: "lines", theta: th, r,
      line: { color: c.theory, width: 1.5, dash: "dash" }, name: "cos&sup2; theory" },
    { type: "scatterpolar", mode: "lines+markers", theta: pa, r: pr,
      line: { color: c.accent, width: 2 }, marker: { color: c.accent, size: 7 },
      name: "measured" },
  ];
}

function patternLayout(c) {
  return {
    margin: { l: 30, r: 30, t: 20, b: 20 },
    paper_bgcolor: c.paper, plot_bgcolor: c.plot,
    font: { color: c.font, size: 11 },
    showlegend: true,
    legend: { orientation: "h", y: -0.05, font: { color: c.font } },
    polar: {
      bgcolor: c.plot,
      radialaxis: { range: [FLOOR_DB, 3], angle: 90, ticksuffix: " dB",
                    gridcolor: c.grid, color: c.font, tickfont: { size: 9 } },
      angularaxis: { direction: "counterclockwise", rotation: 0,
                     gridcolor: c.grid, color: c.font, dtick: 30 },
    },
  };
}

function updatePatternChart() {
  const c = themeColors();
  Plotly.react("chart-pattern", patternTraces(c), patternLayout(c),
    { displayModeBar: false, responsive: true });
}

function updatePatternCount() {
  $("pattern-count").textContent = `${state.pattern.length} point${state.pattern.length === 1 ? "" : "s"}`;
}

/* ----------------------------------------------------------------- */
/* UI helpers                                                        */
/* ----------------------------------------------------------------- */
function setStatus(cls, text) {
  const dot = $("conn-dot");
  dot.className = "dot" + (cls ? " " + cls : "");
  $("conn-text").textContent = text;
}
function showConn(msg, cls) {
  const box = $("conn-info");
  box.style.display = "";
  box.className = "feedback" + (cls ? " " + cls : "");
  $("conn-msg").textContent = msg;
}
function setSlider(rangeId, valId, value) {
  if (value === undefined || value === null) return;
  $(rangeId).value = value;
  $(valId).value = value;
}

/* Co-pol reference: quick click marks it, press-and-hold 3 s clears it. */
async function markRef() {
  const res = await send("mark_reference");
  if (res && res.status === "ok") {
    state.refSet = true; state.refDbfs = res.ref_dbfs;
    flashRefLabel("Ref set");
    updatePowerChart();
  }
}

async function clearRef() {
  await send("clear_reference");
  state.refSet = false; state.refDbfs = null;
  $("rd-rel").textContent = "--";
  flashRefLabel("Ref cleared");
  updatePowerChart();
}

function flashRefLabel(text) {
  const lbl = $("ref-label");
  lbl.textContent = text;
  clearTimeout(flashRefLabel._t);
  flashRefLabel._t = setTimeout(() => { lbl.textContent = "Mark Ref"; }, 1200);
}

/* Floating tooltips for .info-tip icons — positioned on <body>, clamped to
   the viewport so they never clip against the sidebar or run off-pane. */
function bindTooltips() {
  let tip = null;
  const hide = () => { if (tip) { tip.remove(); tip = null; } };
  const show = (icon) => {
    hide();
    tip = document.createElement("div");
    tip.className = "floating-tip";
    tip.textContent = icon.getAttribute("data-tip") || "";
    document.body.appendChild(tip);
    const r = icon.getBoundingClientRect();
    const t = tip.getBoundingClientRect();
    const pad = 8;
    let left = r.left + r.width / 2 - t.width / 2;
    left = Math.max(pad, Math.min(left, window.innerWidth - t.width - pad));
    let top = r.top - t.height - pad;
    if (top < pad) top = r.bottom + pad;         // flip below if no room above
    tip.style.left = `${left}px`;
    tip.style.top = `${top}px`;
    requestAnimationFrame(() => tip && tip.classList.add("visible"));
  };
  document.querySelectorAll(".info-tip").forEach((icon) => {
    icon.addEventListener("mouseenter", () => show(icon));
    icon.addEventListener("mouseleave", hide);
    icon.addEventListener("focus", () => show(icon));
    icon.addEventListener("blur", hide);
  });
}

function bindHoldRef() {
  const btn = $("btn-ref");
  btn.style.setProperty("--hold-ms", HOLD_MS + "ms");  // sync the fill to the timer
  let timer = null, held = false;
  const start = (e) => {
    if (btn.disabled) return;
    e.preventDefault();
    held = false;
    btn.classList.add("holding");           // fill grows over HOLD_MS
    timer = setTimeout(() => {
      held = true; timer = null;
      btn.classList.remove("holding");
      clearRef();                            // full hold -> clear
    }, HOLD_MS);
  };
  const finish = (doMark) => {
    if (timer) { clearTimeout(timer); timer = null; }
    btn.classList.remove("holding");
    if (doMark && !held) markRef();          // released early -> mark
    held = false;
  };
  btn.addEventListener("pointerdown", start);
  btn.addEventListener("pointerup", () => finish(true));
  btn.addEventListener("pointerleave", () => finish(false));
  btn.addEventListener("pointercancel", () => finish(false));
}

/* ----------------------------------------------------------------- */
/* Wire up events                                                    */
/* ----------------------------------------------------------------- */
function bindEvents() {
  // Accordions
  document.querySelectorAll(".accordion-header").forEach((h) => {
    h.addEventListener("click", () => h.parentElement.classList.toggle("active"));
  });

  // Tabs
  document.querySelectorAll(".tab-btn").forEach((b) => {
    b.addEventListener("click", () => {
      document.querySelectorAll(".tab-btn").forEach((x) => x.classList.remove("active"));
      document.querySelectorAll(".tab-panel").forEach((x) => x.classList.remove("active"));
      b.classList.add("active");
      $(b.dataset.target).classList.add("active");
      // Plotly needs a resize nudge when a hidden chart becomes visible.
      setTimeout(() => {
        Plotly.Plots.resize("chart-power");
        Plotly.Plots.resize("chart-pattern");
      }, 50);
    });
  });

  $("btn-connect").addEventListener("click", connectLink);
  $("btn-start-sim").addEventListener("click", startSim);
  $("btn-stream").addEventListener("click", toggleStream);
  bindHoldRef();   // Mark Ref: click = mark, hold 3 s = clear
  bindTooltips();

  // Config: center freq
  $("center-freq").addEventListener("change", (e) => {
    send("set_center_freq", { freq: parseFloat(e.target.value) * 1e9 });
  });

  // Sliders (range <-> number, and push to backend)
  bindSlider("rx-gain", "val-rx-gain", (v) => send("set_rx_gain", { gain: v }));
  bindSlider("tx-gain", "val-tx-gain", (v) => send("set_tx_gain", { gain: v }));
  bindSlider("sim-angle", "val-sim-angle", (v) => {
    send("set_sim_angle", { angle: v });
    $("capture-angle").value = v;   // convenience: capture at the simulated angle
  });

  // Pattern capture
  $("btn-capture").addEventListener("click", async () => {
    const angle = parseFloat($("capture-angle").value);
    const res = await send("capture_point", { angle });
    if (res && res.status === "ok") {
      state.pattern = res.pattern;
      updatePatternChart();
      updatePatternCount();
    }
  });
  $("btn-clear-pattern").addEventListener("click", async () => {
    const res = await send("clear_pattern");
    if (res && res.status === "ok") {
      state.pattern = res.pattern || [];
      updatePatternChart();
      updatePatternCount();
    }
  });

  // Theme
  $("btn-theme").addEventListener("click", toggleTheme);
}

function bindSlider(rangeId, valId, onChange) {
  const range = $(rangeId), val = $(valId);
  range.addEventListener("input", () => { val.value = range.value; onChange(parseFloat(range.value)); });
  val.addEventListener("change", () => { range.value = val.value; onChange(parseFloat(val.value)); });
}

function currentTheme() {
  return document.documentElement.getAttribute("data-theme") === "light" ? "light" : "dark";
}

function applyTheme(theme) {
  document.documentElement.setAttribute("data-theme", theme);
  const dark = theme !== "light";
  $("theme-icon").innerHTML = dark ? "&#9790;" : "&#9728;";
  $("theme-label").textContent = dark ? "Dark mode" : "Light mode";
  if (window.Plotly && document.getElementById("chart-power")) {
    updatePowerChart();
    updatePatternChart();
  }
}

function toggleTheme() {
  state.themeManual = true;                 // stop following the OS once toggled
  applyTheme(currentTheme() === "light" ? "dark" : "light");
}

function initTheme() {
  const mq = window.matchMedia && window.matchMedia("(prefers-color-scheme: light)");
  applyTheme(mq && mq.matches ? "light" : "dark");
  if (mq && mq.addEventListener) {
    mq.addEventListener("change", (e) => {
      if (!state.themeManual) applyTheme(e.matches ? "light" : "dark");
    });
  }
}

/* ----------------------------------------------------------------- */
window.addEventListener("DOMContentLoaded", () => {
  initCharts();
  initTheme();
  bindEvents();
  connectWs();
});
