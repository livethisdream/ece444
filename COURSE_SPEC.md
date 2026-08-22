# ECE 444 COURSE SPEC — Module 2 authoring contract

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
