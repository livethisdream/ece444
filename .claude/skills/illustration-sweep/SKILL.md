---
name: illustration-sweep
description: Audit one lesson (page, deck, practice set) for places a figure or an interactive widget would explain more than the text does, rank them, stop for Neil's pick, then build the approved ones. Manual only -- run as /illustration-sweep <NN>.
argument-hint: <lesson number, e.g. 15>
disable-model-invocation: true
---

# Illustration sweep for one lesson

Run on demand, one lesson at a time: `/illustration-sweep 15`. The lesson is
`$ARGUMENTS`. Neil's standing view (2026-09-29, on L13: "the more
illustrations, the better"; 2026-10-01: "anywhere you could/should build an
illustration or interactive widget to clarify understanding, we should
consider it strongly"). L14's sweep is the worked example: seven figures from
`scripts/graphics/l14_figures.py`, two widgets (`feed-dish.html`,
`yagi-two-element.html`), and one reuse of an L13 figure.

Run it after `/voice-sweep` and `/why-sweep` on the same lesson, so the
figures illustrate the final prose and the derivations they explain exist.

The sweep has two phases with a hard stop between them. **Do not build
anything in phase 1.**

## Phase 0: start clean

```sh
git fetch origin main && git checkout -B <your branch> origin/main
```

## Phase 1: audit, then stop

Inventory the lesson: for every frame, its title, its class (`read-only`,
`viz-frame`, callout), and the figures or widgets it already carries.

```sh
python3 - <<'EOF'
import re, glob
p = glob.glob('book/module*/L<NN>-*/index.md')[0]
for i, f in enumerate(re.split(r'^::::\{frame\}', open(p).read(), flags=re.M)[1:], 1):
    t = f.split('\n', 1)[0].strip()
    figs = re.findall(r'(?:img|viz)/([\w.-]+\.(?:svg|html))', f)
    print(f"{i:2} {t[:44]:44} {', '.join(figs)}")
EOF
ls book/extras/viz/*.html book/extras/viz/img/ | grep -i <topic words>   # what already exists
```

Then rank the candidates by how much a picture would teach. The strongest:

- **A mechanism the reader has to imagine.** Phases adding, a wave
  reflecting, a geometry described in words ("a slice cut off-axis from a
  larger paraboloid"). Draw it.
- **A trade with an optimum.** Two effects pulling opposite ways. Plot both
  and their product, or make it a widget with the knob that moves the
  optimum.
- **A number chain.** A link budget, an efficiency budget, a loss chain: a
  level diagram or a waterfall shows the chain at a glance.
- **A rule of thumb against its data.** A table of measured or typical values
  next to a scaling law: plot both.
- **A comparison stated in prose.** Two patterns, two designs: overlay them.
- **The lesson's central idea**, if it has no picture.

Prefer a **widget** when the understanding comes from moving a parameter and
watching two or more things respond; a **figure** when one well-chosen state
says it. Check `book/extras/viz/` and `viz/img/` for something to reuse, in
this lesson or a neighbor, before proposing new work.

Report a table: rank, frame, what is missing, the proposal, and the type
(widget, figure, computed figure, reuse). Name what is *not* worth
illustrating, in one line. Note the present-beat budget (each new widget
frame is a beat; the budget is in `scripts/verify/budgets.py`, 20 a lesson at present). Recommend a batching. **Then stop and wait for
Neil.**

## Phase 2: build what Neil approved

**Figures.** One generator per lesson, `scripts/graphics/l<NN>_figures.py`,
writing every figure to both `book/extras/slides/fig/` and
`book/extras/viz/img/` through `apply_font_stack()`. Labels only, no
equations, so one SVG serves both trees. Compute every plotted number in the
generator, and check it against the lesson text before you place it; a
figure that disagrees with the prose is worse than none. Place labels from
the data or in empty regions, never at offsets that happen to work today.

**Widgets.** `book/extras/viz/<name>.html`, built on
`book/extras/viz/reflector-gain.html` as the template (palette, `.cv2`,
`.controls`, `.readouts`, phone breakpoints, `mjlabel.js` for symbols only).
The model must match the lesson's equations and any generator that plots the
same quantity; give the builder the check values. Two widgets can be built in
parallel by subagents, one file each, while you do the figures.
`scripts/verify/check_widget.py` must pass: at most 555px at 688-790px and
660px at 320-430px, no overflow at 320, no console errors, no blank canvas.
Set the iframe `height` to what it reports.

**Screenshot everything** before it goes in: each figure at deck width, each
widget at 755 and 390 in at least two states including an extreme one. Fix
every collision, clipped label, overprint, and wrong sign ("−6 dB under the
noise" is a double negative). Fonts never below 10.5px.

**Placing them.**

- A figure that carries the frame's point goes in a present block. Two
  present blocks sit side by side, so the usual shape is bullets beside the
  figure. If a frame already has two blocks, merge the bullets into one
  rather than adding a third.
- A supporting figure goes in read mode only (prose outside the present
  blocks, or `:::{depth}`).
- A widget gets its own `:class: viz-frame` frame, with a title short enough
  to sit on one line at 390px, the iframe in a present block, and a depth
  paragraph that tells the reader what to try.
- Mirror each one in the deck: a figure as
  `<div class="fig" data-inline-svg="./fig/<name>.svg" ...>` on its slide or a
  new slide; a widget as a `<p class="viz-cue">↗ Interactive on the lesson
  page</p>` cue on the related slide, with a speaker note saying what to demo.
  Follow the marked gotchas in `CLAUDE.md`, and rerun `check_deck` for slide
  height after every figure you add.

## Verify before pushing

Everything in `.claude/skills/why-sweep/SKILL.md`, "Verify before pushing",
plus `check_widget.py` on each new widget, `check_frames.py L<NN>` (a figure
in a present block is what pushes a frame past the screen), and
`check_density.py L<NN>` for the beat count. Look at the present-mode
screenshot of every frame you touched, at both widths.

## Finish

Commit with a message that lists each figure and widget and the frame it
serves. Add **one short Status line** to `project/ECE444_PROJECT.md`. Push,
open the PR, and watch it to green.
