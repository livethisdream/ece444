# ECE 444 COURSE SPEC — authoring contract (Module 2; Module 3 addendum at end)

This is the ONLY reference you get about the existing course. Do NOT read the
Module 1 lesson files, decks, or practice sources — everything you need to be
consistent with them is here. Follow it exactly.

Course: ECE 444, *Antennas, Phased Arrays, and Radar Systems*, USAFA, Fall
2026, Dr. Neil Rogers. **Undergraduate** level: derivations are shown but kept
short; intuition and design numbers outrank rigor; every equation earns its
place by being used.

## 1. Files each lesson owns

| Artifact | Path |
| :-- | :-- |
| Lesson page | `book/moduleNN/L<NN>-<slug>/index.md` (MyST markdown; dir already exists) |
| Deck source | `book/extras/slides/L<NN>-<slug>.md` (file already exists as HTML wrapper's target; overwrite the stub `.md` if present, else create) |
| Deck wrapper | generated: `python3 scripts/make_deck_html.py --slug L<NN>-<slug> --title "L<N> - <Title>" --course "ECE 444"` |
| Widget(s) | `book/extras/viz/<widget-name>.html` (name given in your brief) |
| Practice source | `latex/ECE444_Practice_L<NN>.tex` |
| Practice PDFs | `book/extras/practice/ECE444_L<NN>_Practice_{blank,SOLUTIONS}.pdf` (built, then auto-copied by the build script) |

Never touch: `book/_toc.yml`, `book/module02/index.md`, `scripts/`, anything
in `book/module01/`, other lessons' files, `project/`.

## 2. Lesson page (MyST) — section order

Exact skeleton (keep the existing Slides admonition from the stub verbatim):

```
# L<N> - <Title>

:::{admonition} Slides
:class: slides
<a href="../../slides/<slug>.html" target="_blank" rel="noopener">html slides</a>
<a href="../../slides/<slug>.html?print-pdf" target="_blank" rel="noopener">pdf slides</a>
<a href="../../slides/<slug>.md" target="_blank" rel="noopener">raw markdown slides</a>
:::

## Learning Objectives

<ol class="lo-list lo-sublist" style="--module: '2'; --lo: '<X>'">
  <li>I can ...</li>
  ...
</ol>

<one-paragraph hook connecting to the previous lesson and stating what this
lesson delivers>

## Part 1: <name>
...
## Part N: <name>

## Summary            (3-column table, 5-9 rows: Symbol / idea | What it is | Number to remember)

## Practice           (only after the PDFs are built)

- <a href="../../practice/ECE444_L<NN>_Practice_blank.pdf" target="_blank" rel="noopener">Problem set (PDF)</a>
- <a href="../../practice/ECE444_L<NN>_Practice_SOLUTIONS.pdf" target="_blank" rel="noopener">Solutions (PDF)</a>

## Where this is going    (2 short paragraphs: what's next, why it matters;
                           the "read before next lesson" note lives here —
                           no separate "Preparing for L<N>" section)
```

Rules:

- LO markup: 3-level numbers render automatically (`2.<X>.n`). `<X>` is the
  module objective number from your brief. If your brief says your lesson
  *continues* a shared objective (L09 continues 2.1 after L07), add a counter
  offset: `style="--module: '2'; --lo: '1'; counter-reset: lo 4"` starts at
  2.1.5. Sub-LO text comes from your brief. **No math inside LO `<li>` items**
  (raw HTML block — `$...$` is not processed there; if unavoidable use
  `\(...\)`).
- 3-6 numbered Parts. Interleave: concept -> short derivation -> worked
  example -> design numbers. Use admonitions:
  `:::{admonition} Key Point\n:class: key-concept` for the one takeaway;
  `:::{admonition} Worked example — ...\n:class: tip` for examples;
  triple-backtick `{note}` for asides.
- Widget embed: an explanatory paragraph FIRST (2-4 sentences saying what to
  do and what to notice — this is the caption), then:

```
<iframe src="../../viz/<widget-name>.html"
        width="100%" height="<measured px>"
        style="border: 1px solid #cddce9; border-radius: 6px;"
        loading="lazy"
        title="<what it shows>">
</iframe>
```

- Figure naming: every figure file is prefixed by its owning lesson,
  `L<NN>-<name>.svg`, in both `book/extras/slides/fig/` and
  `book/extras/viz/img/` — 41 lessons share these two flat directories.
- Static figures (if any) go in `book/extras/viz/img/<name>.svg`, embedded
  with `<img src="../../viz/img/<name>.svg" ... style="max-width: 700px;
  width: 100%; display: block; margin: 1em auto;">`.
- Cross-reference lessons as "Lesson 5" / "L5" prose (no links needed).
  Reference forward hooks (Module 3 arrays, L16 pattern multiplication,
  L29 radar equation) where they genuinely land.

## 3. Deck (reveal.js markdown)

Slides are separated by a line containing only `---` (blank line before and
after). Speaker notes: a `Note:` line at the end of a slide's markdown.
Stage is 1244x700 px, 16:9. Target 18-26 slides (labs 14-20) — but a lesson
that carries a full derivation may run longer when the brief says so, and a
deck is never trimmed by collapsing a derivation the brief asked for.
Structure:

1. Title slide (copy exactly, substituting lesson number/title):

```
<!-- .slide: class="title-slide" -->

<div class="title-left">

# ECE 444

Antennas, Phased Arrays, and Radar Systems

## Lesson <N> — <Title>

Fall 2026 · Dr. Neil Rogers

</div>

<div class="title-right">

![USAFA](./img/01-course-intro/USAFA-logo.png)

</div>
```

2. "Where we were" — 3-4 bullets recalling prior lessons, ending with a bold
   one-liner of today's point.
3. "Today's plan" — numbered list, 4-6 items.
4. Content slides. One idea per slide. Use:
   - `<div class="callout"> ... </div>` for the slide's takeaway (HTML
     `<strong>`/`<em>` inside, not markdown).
   - Markdown tables for comparisons (keep to <= 5 rows on a slide).
   - `<p class="viz-cue">↗ Interactive on the lesson page</p>` on slides
     backed by a widget, plus `<!-- .slide: class="viz-cue-slide" -->` as the
     slide's first line, plus a speaker note saying what to demo live.
   - Two-column: `<div class="two-col"><div class="col-text"> ... </div>
     <div class="col-fig"> ... </div></div>` (raw HTML block).
   - Figures: `<div class="fig" data-inline-svg="./fig/<name>.svg"
     style="max-width:790px; margin:0 auto;"></div>` — SVG lives in
     `book/extras/slides/fig/`. **Deck figures carry no equations** — put
     math in the slide text.
5. A worked-example slide or two with a small table of (Quantity | Work |
   Result).
6. "Key point" slide — a single callout.
7. "Where this is going" closer.

### Deck LaTeX gotchas (the markdown parser mangles these — MyST does not)

- `\<punct>` escapes inside `$...$` are eaten: use `\lbrace`/`\rbrace`, drop
  `\,` and `\;` (use `\ ` or `\quad`). Word macros (`\quad`, `\text{ }`,
  `\frac`, `\sin`) are safe.
- A subscript after `}` or `)`: write `}\_{` in markdown regions (else marked
  eats the underscores and the slide shows raw `$$`). Inside a raw-HTML block
  (`two-col`, `callout`) do the OPPOSITE — plain `_`.
- Inside multi-line `$$...$$`, no continuation line may start with `+`, `-`,
  or `*`. Simplest: keep every `$$...$$` on ONE line.
- In markdown tables, `|` inside math splits the cell: use `\vert`.

## 4. Interactive widgets

One self-contained HTML file in `book/extras/viz/`. Vanilla JS + canvas (or
SVG). No build step, no network except the MathJax CDN that `mjlabel.js`
pulls (acceptable: the class network has it; the widget must still draw its
geometry without it). One idea per widget, 1-3 controls.

House boilerplate — start from this head:

```html
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title><what it shows></title>
<script src="mjlabel.js"></script>
<style>
  :root { --navy:#004a85; --mid:#0067b9; --edge:#cddce9; --edge2:#b9d2e5; --bg:#f5f9fc;
          --ink:#15202b; --ink3:#5b6573;
          --amber:#8a5a00; --red:#b01e24; --grn:#3f7d34; }
  html,body { margin:0; padding:0; font-family:'Inter',system-ui,-apple-system,sans-serif; color:var(--ink); background:#fff; }
  ...
</style>
</head>
```

Conventions (match them exactly):

- Layout: `<div class="app">` column, canvases on top, a `.controls` bar
  (label + range/select per control), then a `.pills` row of live readouts
  (e.g. `HPBW = 25.6°`). Copy the `.controls`/`.ctl`/`.pill` CSS pattern:
  controls bar has `background:var(--bg); border:1px solid var(--edge);
  border-radius:6px;`, pills are rounded chips with tabular numerals.
- `mjlabel.js` (already in `viz/`): LaTeX is for **math symbols only** —
  all words, units, and numbers are drawn with `ctx.fillText` in the sans
  font. Usage: `MJ.setRedraw(drawAll); MJ.onReady(()=>{MJ.typeset(panel);
  drawAll();});` then `MJ.draw(ctx,'\\lambda',x,y,13,color,'center')`.
  Control labels in HTML may use `\(...\)`.
- Canvas drawn at devicePixelRatio; redraw on `resize` and on every input.
- Physics computed honestly (real integrals/formulas, trapezoid sums fine),
  not sketched. Pin numeric readouts to the canonical numbers in §7 where
  they apply.
- Colors: navy = primary curve/geometry, amber = warning/sidelobe-ish
  quantities, green = beamwidth/good, red = danger/null/error. dB floors at
  −40 dB unless the brief says otherwise.
- Every widget needs a **static fallback for the deck**: either an existing
  deck figure or a `viz-cue` slide whose table/callout carries the numbers
  the widget demonstrates. If the brief asks for a static SVG, put a
  no-equations copy in `book/extras/slides/fig/`.

## 5. Practice set (LaTeX)

Harness: `latex/ECE444_Practice_main.tex` (`exam` class + private house
macros; do not edit it). Your file is `latex/ECE444_Practice_L<NN>.tex`,
compiled with the solutions/blank switch by:

```sh
TEXINPUTS=/workspace/latex-tools/tex/latex//: bash latex/build_practice.sh <NN>
```

File skeleton:

```latex
% !TEX root =./ECE444_Practice_main.tex
%
% L<N> practice set (<Title>) ... one comment line of context.

\fullwidth{\textbf{Learning Objective 2.<X>: } <objective text>
\\[4pt]\normalfont\small Show your work. A \textbf{Documentation} line at the end
is required (write \textbf{None} if you did not collaborate).}

\begin{questions}

\question \textbf{<Question theme>.} <stem>
\begin{parts}
	\part <concept part>
		\begin{solution}[1.2in]
		<worked solution — full sentences, boxed math via \eq{...}>
		\end{solution}
	...
\end{parts}

\newpage
\question ...

\vspace{1.5em}
\noindent\textbf{Documentation:} \rule[-2pt]{0.6\linewidth}{0.4pt}

\end{questions}
```

Rules:

- Every lesson ships a practice set, labs and intro lessons included (an
  intro-level set may be short — 2 questions of identification/concept parts).
- 4-6 `\question`s, each 3-4 `\part`s (hard max 4), `\newpage` between
  questions.
  Mix per set: ~40% concept/explain parts (1-2 sentence answers), ~45%
  numeric parts, ~15% design/interpretation parts that force a trade-off
  statement.
- Numeric parts use the minipage + answer-box pattern:

```latex
	\begin{minipage}[t]{0.58\linewidth}
		\part <numeric prompt>
		\begin{solution}[1.1in]
		\eq{ <work> }
		\end{solution}
	\end{minipage}\hfill%
	\begin{minipage}[t]{0.37\linewidth}
		\raggedleft \vspace{12pt}
		$<sym>$ = \ansbox[1.3in]{$<answer with units>$}
	\end{minipage}
```

- `\begin{solution}[h]` height `h` (0.8-1.6in) reserves blank workspace in
  the student copy; scale it to the work required.
- Every numeric part gets an `\ansbox` with units — 11-20 boxes per set.
- House macros (available; use these, not raw equivalents):
  `\eq{...}` display math (align-style, `&` and `\\` allowed);
  `\sinp{x} \cosp{x} \tanp{x}` = sin(x) etc. with parens; `\lp \rp` = big
  parens; `\mydeg` = degree; units `\m \km \ghz \mhz \khz \hz \db
  \dbi \dbm \dbsm \ohms \watts \mwatts \volts \amps` (NOTE: `\cm`/`\mm` do
  NOT exist — write `\text{cm}`/`\text{mm}`; `\db`/`\dbi`/`\ohms` carry a
  trailing space, so write `62\ \ohms` and avoid a period directly after);
  `\mylog{x}` = log10;
  `\zhat \xhat \yhat \rhat \thetahat \phihat`; `\vec{}` for vectors;
  `\clight` if needed. Subscripts/superscripts: plain LaTeX. Primes:
  `\vec{r}^{\prime}`, `z^{\prime}`.
- Difficulty calibration: a strong student finishes a set in 45-60 min. Every
  numeric answer is a *plausible engineering number* stated with units and a
  dB conversion where natural. At least one part per set explicitly connects
  to a rule of thumb or canonical number (§7), and at least one asks "why"
  in words.
- Solutions are complete worked derivations (they print in red in the
  SOLUTIONS copy) — full sentences for concept parts, `\eq{}` chains showing
  intermediate numbers for numeric parts.
- Both PDFs must build with **zero LaTeX errors** and no overfull-box
  warnings > 10pt. Check the `.log`.

## 6. Notation and symbols (course-wide; decks are the source of truth)

| Symbol | Meaning | Notes |
| :-- | :-- | :-- |
| $k = 2\pi/\lambda$ | wavenumber | |
| $\eta_0 \approx 377\ \Omega$ | free-space impedance | |
| $D$, $G$ | directivity, gain | $G = \eta_{\text{rad}} D$; dBi when logarithmic |
| $U(\theta,\phi)$ | radiation intensity | W/sr |
| $\vert F(\theta,\phi)\vert$ | normalized field pattern | |
| $S(\theta)$ | space factor (distribution alone) | pattern = element factor × space factor |
| $\mathbf{N}(\theta,\phi)$ | radiation vector | $\int \mathbf{J} e^{+jk\hat{\mathbf r}\cdot\mathbf{r}'} dV'$ |
| $\theta_\text{HP}$ | half-power beamwidth (HPBW) | |
| $Z_{\text{in}} = R_{\text{in}} + jX_{\text{in}}$ | input impedance | resonance = $X_{\text{in}}=0$ |
| $R_{\text{rad}}$, $R_{\text{loss}}$ | radiation / loss resistance | $\eta_{\text{rad}} = R_{\text{rad}}/(R_{\text{rad}}+R_{\text{loss}})$ |
| $\psi$ | polarization tilt angle | never $\theta$, which is reserved for the polar angle |
| $\Gamma$, VSWR | reflection coefficient, standing-wave ratio | ref. $50\ \Omega$ unless said |
| $A_e$ | effective aperture | $A_e = G\lambda^2/4\pi$; "effective aperture", not "capture area" |
| $\eta_{\text{ap}}$ | aperture efficiency | |
| $r \ge 2D^2/\lambda$ | far-field distance | $D$ = largest dimension |
| $k_z = k\cos\theta$ | space frequency | line source on z |

Spherical coordinates: $\theta$ from the +z axis, $\phi$ from +x; wire
antennas lie along z; broadside = $\theta = 90^\circ$. Time convention
$e^{+j\omega t}$, phasors with $e^{-jkr}$ outgoing.

Subscript style: any non-math word or abbreviation in a sub- or superscript
is wrapped in `\text{}` — $Z_{\text{in}}$, $\eta_{\text{rad}}$,
$R_{\text{loss}}$, $\eta_{\text{ap}}$. Single-letter/digit math subscripts
stay bare ($\eta_0$, $A_e$, $G_t$, $G_r$).

## 7. Canonical numbers (must match everywhere they appear)

- Infinitesimal dipole: $\vert F\vert = \sin\theta$, HPBW $90^\circ$, $D = 1.5$ (1.76 dBi).
- Half-wave dipole: $\vert F\vert = \cos(\tfrac{\pi}{2}\cos\theta)/\sin\theta$, HPBW
  $78.1^\circ$ (call it $78^\circ$), $D = 1.64$ (2.15 dBi), $Z_{in} \approx 73 + j42.5\ \Omega$;
  resonant slightly short (~0.47-0.48 λ) at $\approx 70\ \Omega$ real.
- Quarter-wave monopole over perfect ground: half the impedance
  ($36.5 + j21.3\ \Omega$), double the directivity (5.15 dBi), radiates upper
  half-space only.
- Uniform line source / aperture: first sidelobe $-13.3$ dB, HPBW
  $\approx 0.886\ \lambda/L$ (line) — sidelobes set by shape, beamwidth by size.
- Tapers (same L): cosine $-23$ dB, triangular $-26.5$ dB, cosine² $-31.5$ dB;
  taper broadens the beam.
- Aperture antennas: $G = \eta_{ap} 4\pi A/\lambda^2$; typical
  $\eta_{ap} \approx 0.5\text{-}0.7$ (horns ~0.5, good reflectors ~0.55-0.7).
- Speed of light $3\times10^8$ m/s; "far-field criterion" $2D^2/\lambda$ with
  the $\pi/8$ (22.5°) phase-error tolerance behind it.
- Friis (L2): $P_r = P_t G_t G_r (\lambda/4\pi R)^2$. Radar range equation is
  deferred to L29 — preview only, never derived in Module 2.
- CP against a linear antenna at AR = 3 dB: received power swings over a 3 dB
  range with orientation, $-1.8$ to $-4.8$ dB (never "capped at 3 dB"); worst
  case against the wrong circular sense at AR = 3 dB: $-9.6$ dB.
- Pencil-beam directivity: $D \approx 41{,}253/(\theta_1^\circ\theta_2^\circ)$
  is the lossless geometric bound; the practical constant for real horns and
  dishes is 26,000-32,400 (sidelobes and spillover cost 1-2 dB).

## 8. Formatting rules (course-wide, non-negotiable)

- **No thin spaces (U+2009) anywhere.** Use `\ ` for spacing in math on MyST
  pages (never `\,` or `\;`).
- In markdown tables, absolute values/norms use `\vert`, never `|`.
- Units in math with an escaped space: `$0.05\ \text{m}$` style on pages;
  house unit macros in LaTeX practice sets.
- dB values get one decimal where meaningful ($-13.3$ dB, 2.15 dBi).
- Em dashes with spaces — like this — for asides in prose.

## 8b. Software and tooling

**Python or another FOSS language, never MATLAB.** Every lab procedure,
example, analysis script, and piece of code a student runs is Python unless
Neil says otherwise. Hardware control for the ADALM-PHASER goes through
`pyadi-iio`. Vendor material for this hardware is frequently MATLAB-first —
read it for the control sequence, then write the course version in Python.
Never assign, embed, or recommend MATLAB.

## 9. Voice

**Read `VOICE.md` before writing prose.** It carries the calibration set —
before-and-after pairs from Neil's own review corrections, which make the
target concrete. The rules below are the summary.

Second person, direct, confident, and **professional**. Bold the key term at
first use. Prefer "read the physics" framing over formalism: say what an
equation *does* before what it *is*. Every lesson opens by connecting to the
previous one and closes by pointing forward. Rules of thumb are named as such
and repeated deliberately. Tables summarize; prose explains. No filler ("In
this lesson we will...").

Four things to avoid. These were flagged in review as widespread, and they
read as unprofessional in a course text:

- **No sentence fragments used for rhythm or punch.** Write complete
  sentences. "0.95 to 1.05, fine. 0.6 or 1.4, your model is broken." becomes
  "An average gain between 0.95 and 1.05 is acceptable. A value near 0.6 or
  1.4 means the model is wrong, and no other number on the page can be
  trusted until it is fixed." Directness comes from short complete sentences,
  not from dropped verbs.
- **Never vouch for the material's own honesty or rigor.** Cut "honest",
  "genuinely", "really does", "actually solves", "no hand-waving". Say what
  the thing does; the reader assumes the text is truthful. (Neil: "if we're
  not being honest, why are we writing this book?")
- **No cheeky asides or winking humor** — arch understatement, jokes at the
  reader's expense, exclamations.
- **No scolding the reader.** State the fact ("a misplaced source moves the
  impedance"), not the accusation ("your model is broken").

Direct and plain is the target. Clever is not.

## 10. Self-checks before you report back (all mechanical, all required)

1. Practice: `TEXINPUTS=/workspace/latex-tools/tex/latex//: bash
   latex/build_practice.sh <NN>` — both PDFs, zero errors; grep the `.log`s
   for `Overfull`.
2. Deck: `python3 scripts/make_deck_html.py --slug <slug> --title
   "L<N> - <Title>" --course "ECE 444"`, then run the render check:
   `scripts/verify/check_deck.py <slug>` — every slide must fit 700px, zero
   raw `$$`, zero missing figures.
3. Widget: `scripts/verify/check_widget.py book/extras/viz/<name>.html` — no
   console errors, canvas paints, zero horizontal overflow down to 320px,
   undistorted aspect. It reports the worst-case height across the widths the
   article column actually takes; use that in the lesson-page iframe.
4. Tables: `scripts/verify/check_tables.py <your .md files>` — a `|` inside
   `$...$` splits a cell; use `\vert`.
5. Greps: no U+2009 (`grep -rP '\x{2009}'` on your files), no `\,`/`\;` in
   the deck `.md`, no unescaped `}_{` in deck markdown regions (outside
   raw-HTML divs).
6. Do NOT run `jupyter-book build` (the orchestrator builds once, centrally).
7. Do NOT commit or push. Leave files in the working tree.

`scripts/verify/mech_check.sh <NN> <slug>` runs all of the above at once, plus
the checks the orchestrator would otherwise run by hand. Prefer it. It needs
`cd scripts/verify && npm install` once per container — the CDNs are blocked
here, so reveal.js and MathJax have to be vendored.

Report back ≤20 lines: paths written, self-check results (pass/fail each),
assumptions made, ambiguities. Never lesson content.

---

# MODULE 3 ADDENDUM — Arrays and ADALM-PHASER Beamforming (L15–L28)

This addendum extends the contract above to Module 3. Where the two conflict
on module-specific details (module number, lesson list, platform), this
addendum wins; everything else above (deck rules, widget conventions,
practice format, voice, self-checks) applies unchanged. Use `--module: '3'`
in every LO block.

## M1. Lesson map and LO numbering

| NN | Slug | Title | Obj. | Sub-LO start | Kind |
| :-- | :-- | :-- | :-- | :-- | :-- |
| 15 | L15-aperture-distributions | Aperture Distributions and Efficiency | 3.1 | 3.1.1 | theory |
| 16 | L16-array-factor | The Array Factor and Pattern Multiplication | 3.2 | 3.2.1 | theory |
| 17 | L17-phased-array-hardware | Introduction to Phased Array Hardware | 3.3 | 3.3.1 | lab |
| 18 | L18-beam-steering-theory | Beam Steering Theory | 3.4 | 3.4.1 | theory |
| 19 | L19-beam-steering-lab | Beam Steering Lab | 3.5 | 3.5.1 | lab |
| 20 | L20-array-factor-beamwidth | Array Factor and Beamwidth Theory | 3.2 | 3.2.6 | theory |
| 21 | L21-array-factor-lab | Array Factor Lab | 3.2 | 3.2.10 | lab |
| 22 | L22-antenna-pattern-theory | Antenna Pattern Theory | 3.6 | 3.6.1 | theory |
| 23 | L23-antenna-pattern-lab | Antenna Pattern Lab | 3.6 | 3.6.5 | lab |
| 24 | L24-sidelobes-tapering | Sidelobes and Tapering Theory | 3.7 | 3.7.1 | theory |
| 25 | L25-tapering-lab | Tapering Lab | 3.7 | 3.7.6 | lab |
| 26 | L26-beam-squint-quantization | Beam Squint and Quantization | 3.8 | 3.8.1 | theory |
| 27 | L27-null-steering-theory | Null Steering Theory | 3.9 | 3.9.1 | theory |
| 28 | L28-null-steering-lab | Null Steering Lab | 3.9 | 3.9.5 | lab |

A lesson whose sub-LO start is not `.1` continues a shared objective: add
`counter-reset: lo <start-1>` to the `<ol>` style (e.g. L20:
`style="--module: '3'; --lo: '2'; counter-reset: lo 5"` renders 3.2.6
onward). Your brief carries the exact sub-LO texts — use them verbatim.

**L20 note:** the midterm project (Antenna Pattern Measurement, assigned at
L11) is **due at L20**. L20's page and deck open by acknowledging the
turn-in in one short paragraph/slide bullet before the lesson content; do
not restate the project requirements.

Objective 3.8 covers **grating lobes, beam squint, and phase quantization**
— the three ways a real steered array departs from the ideal pattern. All
three live in L26.

## M2. Array notation (Module 3 course-wide; decks are source of truth)

Module 3 works in the **scan angle** $\theta$, measured from broadside
(mechanical boresight) of the array, $-90^\circ \le \theta \le +90^\circ$.
This matches every PHASER plot, the GUI's angle axis, and the phased-array
literature. L16 makes the one-time connection to Module 1's polar angle
(line source on z: $\theta_{\text{polar}} = 90^\circ - \theta$, so the
space frequency $k\cos\theta_{\text{polar}}$ becomes $k\sin\theta$); no
other lesson revisits it.

| Symbol | Meaning |
| :-- | :-- |
| $N$, $d$ | element count, element spacing |
| $\theta$, $\theta_0$ | scan angle, steered (commanded) beam angle — both from broadside |
| $\Delta\phi = kd\sin\theta_0$ | progressive element-to-element phase (magnitude); the applied ramp compensates the arrival delay |
| $\psi = kd(\sin\theta - \sin\theta_0)$ | array-factor argument |
| $AF_N(\psi) = \dfrac{\sin(N\psi/2)}{N\sin(\psi/2)}$ | normalized uniform array factor (this normalization: peak = 1) |
| $a_n$, $w_n$ | element amplitude (taper), complex element weight |
| $EF(\theta)$ | element factor; pattern $= EF \times AF$ (pattern multiplication) |
| $\eta_t$ | taper efficiency $(\sum a_n)^2 / (N\sum a_n^2)$ |
| $B$ | phase-shifter bits; LSB $= 360^\circ/2^B$ |

Derivations are **shown, not asserted**: the array factor (phasor
superposition → closed form, L16), the steering phase (path-length
argument, L18), and the taper trade (L24) are each derived step by step,
one step per slide on the deck, with speaker notes that support deriving
it live at the board.

## M3. The platform: ADALM-PHASER (CN0566) + the course Phaser GUI

The hardware for every Module 3 lab. Facts below are canonical — do not
invent register names, frequencies, or call signatures beyond them.

**Hardware.** 8-element linear microstrip patch array (horizontal row,
element spacing $d = 14$ mm), fed through per-element LNAs (ADL8107) into
two **ADAR1000** 4-channel analog beamformer chips (phase + gain per
element). Each ADAR1000 sums its 4 elements into one RF channel; the two
channels are mixed down (LTC5548) and digitized by the two Rx channels of
an **ADALM-Pluto** SDR (AD9361). A Raspberry Pi on the back of the board
runs the control software and talks to the chips over SPI / `pyadi-iio`.
So the PHASER is a **hybrid beamformer**: analog beamforming inside each
4-element subarray, digital beamforming across the two subarray outputs.

**Frequency plan** (workshop appendix; canonical): the array receives
X-band, 10.0–10.5 GHz. The lab source is an **HB100** Doppler module,
10.525 GHz nominal (a free-running DRO — anywhere in 10.1–10.7 GHz, which
is why the software hunts for it). An ADF4159 PLL + HMC735 VCO generate a
12.2–13.0 GHz LO; the LTC5548 mixers convert the received signal to a
**2.2 GHz IF**, which the Pluto tunes directly (LO = RF + 2.2 GHz,
high-side injection). Pluto sample rate 3 MSPS in the GUI (30 MSPS in
ADI's standalone scripts); the sim places the received tone at a 1 MHz IF
offset in the baseband spectrum. ADAR1000 phase LSB = **2.8125°** (128
steps = 7 bits). At the workshop's 10.3 GHz, $\lambda = 29.1$ mm and
$d/\lambda = 0.481$; at the HB100's 10.525 GHz, $\lambda = 28.5$ mm and
$d/\lambda = 0.491$.

**Software: the course Phaser GUI (Neil's, replaces ADI's Thonny scripts).**
A headless Python backend (`phaser_headless.py`) runs on the Pi and drives
the ADAR1000s, Pluto, and ADF4159 through `pyadi-iio`; a browser UI
(vanilla JS + Plotly) connects over WebSocket from any machine on the
network at `http://phaser.local:8080`. Lab procedures are written against
**this GUI**, never against Thonny, `phaser_gui.py`, or MATLAB. Python
(`pyadi-iio`) is the only language shown for hardware control.

GUI inventory (use these exact names in procedures):

- **Sidebar sections:** Configuration (Signal Freq (GHz), Rx Gain (dB),
  Tx Gain (dB), Signal BW (MHz), Tx Mode, Calibrate), Element Gains
  (Rx1–Rx8 sliders, Taper presets Uniform / Chebyshev / Hann / Blackman,
  Aperture Presets 2-Elem / Sparse λ, Enforce Symmetric Taper), Phase
  Control (per-element phase offsets, Reset), Beam Steering (Steer Angle
  (deg), Apply), Quantization (Steer Resolution (deg), Phase Shift Bits,
  Use Bits (ignore Steer Res)), Digital Beam Forming (Mode: Manual / MVDR;
  Manual: Beam 0/1 Gain and Phase; MVDR: Snapshots (K), Diagonal Load),
  Plot Options (peak markers, squint info, monopulse delta/error), Lab
  Presets (buttons 1 Steering Angle, 2 Array Factor, 3 Tapering,
  4 Grating Lobes, 5 Beam Squint, 6 Quantization, 7 Antenna Pattern,
  8 Tracking).
- **Plot tabs:** Rectangular, Polar, FFT, Tracking. **Start** runs the
  beam sweep; **Freeze** holds up to 3 reference traces for comparison.
  Readouts: Peak Array Gain (dB), Est. Angle (°).
- **Lab presets** load the initial state for each workshop lab (aligned
  to ADI's *Phased Array Radar Workshop*); a lab procedure starts from its
  preset button, then names only the controls the student changes.
- **Simulation mode**: `python phaser_headless.py --sim` runs the whole
  UI against physics-based stubs (HB100 target at boresight). Labs are
  written for the real kit + HB100; where the sim behaves differently,
  add a short "no hardware?" note. Sim limits: the target is fixed at
  boresight (procedures that rotate the HB100 by hand have no sim
  equivalent — say so); CW radar is not simulated.
- **Instructor mode** (`?instructor=1`, sim only) adds a Simulator
  Interferer panel (angle, power rel. target) — a configurable jammer for
  nulling demos. Student-facing pages must NOT document instructor mode;
  it may appear in speaker notes as an instructor demo cue.

**Beam-sweep semantics** (get this right in prose): the Rectangular plot's
"gain vs steering angle" trace is produced by *electronically sweeping the
commanded steer angle* past a stationary source and recording received
power at each step. By reciprocity this traces the array pattern — but the
x-axis is the commanded steer angle, not a measured arrival angle. The
sweep step equals the phase LSB expressed as a steering resolution
(2.8125° default), so measured HPBW/FNBW read 1–3° off theory from grid
discretization alone; noise floor sits ≈ 23 dB below the uniform-taper
peak. The "Phase Shift Bits" slider couples the sweep grid to the LSB, so
at 2 bits the trace itself goes coarse — that IS the quantization
demonstration in sweep mode.

## M4. Canonical Module 3 numbers (verified in simulation 2026-08-23;
must match everywhere they appear)

Theory values are exact; "measured" values are what the sim/hardware
sweep actually reads and belong in lab expectation tables.

- **N=8 uniform, broadside** (10.3 GHz, d=14 mm): HPBW theory 13.2°
  (measured 13.1°), FNBW theory 30.1° (measured 28–30°), first sidelobe
  −12.8 dB for discrete N=8 (call it −13 dB; measured −11 to −13 dBc).
- **N=4** (center 4 on): HPBW 27° calc / 29° meas; FNBW 62°. **N=2**
  (center pair): HPBW 62° calc / 65° meas; FNBW 180° by convention
  ($\lambda/2d > 1$ — no visible-space null).
- HPBW $\approx 0.886\ \lambda/(Nd\cos\theta_0)$ — the L06/L15 line-source
  constant with $L = Nd$; beam broadens as $1/\cos\theta_0$ off broadside.
  FNBW (broadside) $= 2\arcsin(\lambda/Nd)$.
- Broadside directivity of a uniform ULA: $D \approx 2Nd/\lambda$ (= 7.7
  → 8.9 dB for the PHASER's 8 elements).
- **Grating lobes**: $\sin\theta_g = \sin\theta_0 \pm m\lambda/d$;
  avoidance criterion $d < \lambda/(1+\vert\sin\theta_0\vert)$. PHASER
  demos (broadside): every 3rd element on → $d_{\text{eff}}=42$ mm →
  lobes at 0°, ±44° (measured ±42°, equal height); every 4th element →
  56 mm → 0°, ±31°, ±90° (measured ±31°, ±85–90°).
- **Beam squint**: $\Delta\theta = \arcsin((f_0/f)\sin\theta_0) - \theta_0$ (phases set at $f_0$, observed at $f$). Canonical example:
  500 MHz below 10.525 GHz at $\theta_0 = 45°$ → +2.9° (measured +2.8°).
  Note the workshop's rounded version: 10.5 vs 10 GHz at 45° → ≈ 3°.
- **Quantization**: LSB $= 360°/2^B$; ADAR1000 gives B=7 → 2.8125°. RMS
  quantization sidelobe rule of thumb: QSLL $\approx -6B$ dB (2 bits →
  −12 dB). Null depth is quantization-limited: with 2.8° LSB and 1%-step
  gains, achievable pattern-notch depth ≈ 20–22 dB (measured 21.6 dB).
- **8-element taper presets** (the GUI's Element Gains percentages) and
  what the sweep measures relative to uniform:

| Preset | $a_n$ (%) | HPBW meas | Peak drop | $\eta_t$ |
| :-- | :-- | :-- | :-- | :-- |
| Uniform | 100 ×8 | 13.1° | 0 dB | 1.00 |
| Hann | 12, 43, 77, 100, 100, 77, 43, 12 | 19.5° | −4.7 dB | 0.83 (−0.8 dB) |
| Blackman | 6, 27, 66, 100, 100, 66, 27, 6 | 23.1° | −6.1 dB | 0.70 (−1.5 dB) |
| Chebyshev | 4, 23, 62, 100, 100, 62, 23, 4 | 24.3° | −6.5 dB | 0.68 (−1.7 dB) |

  Tapered first sidelobes drop below the sweep's noise floor (≥ 17 dB
  down) — lab tables should say "below the noise floor", not quote a
  number. **Peak drop on the plot** is the coherent receive-voltage loss
  $20\log_{10}(\sum a_n / N)$ — it is NOT the directivity loss, which is
  the taper efficiency $\eta_t$ (about −0.8 dB for Hann). L24/L25 must
  keep these two numbers distinct or students will misread the plot.
- **Scan loss (canonical rule)**: peak *power* gain of the steered array
  falls as $\cos\theta_0$ — the projected-aperture rule: $-0.6$ dB at
  30°, $-1.5$ dB at 45°, $-3.0$ dB at 60° ($-2.4$ dB at 55°). This is the
  ideal-element bound; real patch elements are steeper (power
  $\cos^{1.3\text{-}1.5}\theta$), which L22 states as the caveat. Do not
  use a $\cos\theta$ *field* pattern ($-6$ dB at 60°) as the canonical
  element model.
- **Continuous apertures (L15)** reuse the L06 table verbatim: uniform
  −13.3 dB / 0.886; cosine −23 dB / 1.19; triangular −26.5 dB / 1.27;
  cosine² −31.5 dB / 1.44 (HPBW constant × $\lambda/L$). Aperture
  efficiencies: uniform 1.00, cosine 0.81, triangular 0.75, cosine²
  0.667. $G = \eta_{ap}\,4\pi A/\lambda^2$ as in §7.
- **Null steering (weight subtraction)**: to keep a beam at $\theta_0$
  and null $\theta_1$: $w = w_d - r_n w_n$ with $r_n = \dfrac{w_n^H
  w_d}{w_n^H w_n}$, where $w_d$, $w_n$ are the steering-vector weights
  for $\theta_0$, $\theta_1$. On the PHASER, convert $w$ to per-element
  gain % ($100\vert w_n\vert/\max$) and phase offsets ($\angle w_n$),
  entered in Element Gains + Phase Control. Verified example: null at
  +22.5° from a broadside beam → gains 75, 65, 82, 100, 100, 82, 65, 75;
  phases −12.1°, +3.1°, +13.0°, +6.0°, −6.0°, −13.0°, −3.1°, +12.1°;
  measured notch −21.6 dBc (12 dB below the uniform sidelobe there),
  main-lobe cost 1.8 dB. Sign convention: $w_n$ built with
  $e^{-jnkd\sin\theta_1}$ puts the notch at $+\theta_1$ on the GUI axis.
- **Two-channel (digital) delta null**: Beam 1 Phase = 180° subtracts the
  two subarray outputs → boresight null ≈ −22 dBc with twin peaks near
  ±11° (the monopulse delta beam).
- **MVDR** (2 digital channels): $w_{\text{mvdr}} = \dfrac{R^{-1}s}{s^H
  R^{-1}s}$, $\hat R = \tfrac{1}{K}XX^H$ (K snapshots, diagonal loading
  ~0.001). Verified sim demo: interferer at +30°, 10 dB above target →
  manual beamformer is captured by it; MVDR keeps the look direction and
  suppresses the interferer response by ~17–19 dB. MVDR needs the
  *digital* channels — the analog sums destroy the per-element
  information, which is exactly the hybrid-architecture lesson.

## M5. Lab lesson pages (L17, L19, L21, L23, L25, L28)

Same skeleton as theory pages (Parts → Summary → Practice → Where this is
going), with the Parts covering, in order: background/theory recap (1–2
Parts), equipment and setup (one Part: kit, HB100, GUI bring-up, the lab
preset to load), procedure (one Part: numbered steps, each naming the
exact control and the expected observation with numbers from §M4), and
deliverables (one Part: what students record/submit — measurement tables
with "calculated" columns filled from theory, short written answers).
Target 14–20 deck slides for labs. Every lab teaches against the
expectation table: predict from theory first, measure second, reconcile
third. Lab practice sets emphasize reading real sweeps: give students
plausible measured numbers and ask what they indicate.

Deck title-slide image path and all other Module 2 rules apply unchanged.

## M6. Software rules (restated for Module 3)

Python or another FOSS language only — never MATLAB, never MATLAB
examples, even as "see also". Hardware control examples use `pyadi-iio`
and mirror the course GUI's backend (e.g. setting `adar1000` phases,
Pluto `rx_lo`, ADF4159 `frequency`); keep code excerpts short (≤ 15
lines) and runnable in spirit — no invented attribute names. The course
GUI is the deliverable interface; raw-Python excerpts exist to demystify
it, not to replace it.
