# Seed prompt — convert the lessons to frame view

Copy everything below the line into a new Claude Code session on this repo.

---

You are orchestrating the conversion of this antenna & radar course's lesson
pages to the **frame view** — the chrome-free, one-screen-at-a-time layout the
site already uses for its landing page, its five module overviews, and L05a.

Work on the branch **`claude/reviewer-md-definition-ciir1w`**, or a branch cut
from it. Do NOT start from `main`: the shell that makes frame pages render at
all lives only on that branch, and PR #7 is not merged. Check this first —
`git log --oneline -1` should show the frame-shell work, and
`book/_templates/frame.html` must exist.

## Read these first

- **`CLAUDE.md`** — the authoring contract. Its **Frame lessons** and **The
  shell** sections are the rules for this job specifically. Follow them rather
  than re-deriving them; every one of them is there because the defect it
  describes already shipped once.
- **`project/FRAMES_ARCHITECTURE.md`** — the design, and what is still open.
- **`VOICE.md`** — before writing or re-cutting any prose.
- **`project/ECE444_PROJECT.md`** — running status. Update its Status section
  when the batch is done. It is a conflict magnet across concurrent sessions,
  so **only you, the orchestrator, edit it** — never a subagent.

## Scope: 28 lessons, not 41

This is the single most important line in this prompt. The lessons are not
uniform, and treating them as one batch of 41 wastes most of the run:

| Group | Lessons | State | What to do |
| :-- | :-- | :-- | :-- |
| Authored | L01–L28, plus `L04-lab-matching` | 2,300–5,600 words, practice sets, decks | **Convert.** This is the work. |
| Stubs | L29–L41 | 64–137 words: a title, an LO list, an "under construction" note | **Leave alone.** |
| Duplicate | L05a | the frame-view copy of L05, built as the experiment | **Retire it** once L05 is converted — see below. |

A 68-word stub has no beats to break into frames. Wrapping one in frame
directives produces a single frame that says "under construction" and costs a
full agent to write. Convert them when they get content, not before.

Verify the split yourself before dispatching anything — do not trust this
table blind:

```sh
for f in book/module*/L*/index.md; do
  printf "%-40s %6s\n" "$(basename $(dirname $f))" "$(wc -w < $f)"
done | sort
```

## How to spend the budget

You are the expensive part of this system. Behave accordingly.

**Never read a lesson body yourself.** You dispatch, and you read gate output.
If you find yourself reading 4,000 words of a lesson to check an agent's work,
the gate is wrong — fix the gate instead.

**Two stages per lesson, and only one of them needs judgement.**

1. **Plan (judgement, expensive, once per lesson).** One agent reads the
   lesson page and its deck and produces a *frame plan*: an ordered list of
   frame titles, which existing section or deck beat feeds each one, and what
   drops into `:::{depth}`. It writes the plan and nothing else — no edits.
   The deck is the best input here: it is already the lesson cut into beats,
   and **the decks are the source of truth for nomenclature**.
2. **Apply (mechanical, cheap, once per lesson).** A second agent applies the
   plan: front matter, directives, moving blocks. It makes no content
   decisions. If it wants to make one, it stops and reports instead.

Route stage 2, and every verification agent, to the cheapest model that can do
it. Stage 1 is where the money should go.

**Batch by module, not all at once.** Module 1 (L01–L06) first, as the
calibration batch: run it end to end, look at the result yourself, and only
then dispatch Modules 2 and 3. A systematic mistake caught after 6 lessons
costs a sixth of what it costs after 28.

**Never let an agent run the site-wide sweeps.** `check_shell.py`,
`check_bar.py` and a full `check_parity.py` each drive a headless browser over
54 pages. They are yours to run once per batch, at the end. Per-lesson agents
run only `mech_check.sh`.

**One agent per lesson, no shared files.** Two agents editing `_toc.yml`,
`CLAUDE.md` or the project note will conflict. If a shared file needs
changing, you change it.

## Converting one lesson

The page keeps its path, its filename and its L-number. Nothing is renamed and
nothing moves directories.

1. Add `frame_view: true` to the front matter.
2. Keep the H1.
3. Every beat becomes a frame. The title is a **directive argument**:

```markdown
::::{frame} Why the boundary is where it is
Prose for this beat.

:::{callout}
The thing they must not miss.
:::

:::{depth}
The derivation, the caveat, the extra table. Shown in read mode, hidden in
present mode, always in the DOM and always searchable.
:::
::::
```

Fence lengths are load-bearing: `::::` for the frame, `:::` for anything
inside it. Same-length fences close the outer block early.

4. **Every frame must fit one screen.** `mech_check.sh` gates on this. When a
   frame overruns, **split it or move detail into `depth` — never cut the
   content**. A 3,000-word lesson lands around 25–35 frames; that is normal
   and not a reason to compress.
5. The `## Learning Objectives` list stays exactly as it is, including its
   `--module` / `counter-reset` markup. `mech_check.sh` checks it.

### What must survive, verbatim

**The practice links.** Every authored lesson ends with:

```markdown
## Practice

- <a href="../../practice/ECE444_L07_Practice_blank.pdf" target="_blank" rel="noopener">Problem set (PDF)</a>
- <a href="../../practice/ECE444_L07_Practice_SOLUTIONS.pdf" target="_blank" rel="noopener">Solutions (PDF)</a>
```

Those two links move into a frame of their own at the end of the lesson, with
the hrefs untouched. They are what students actually come to the page for.
`L04-lab-matching` has no practice set — do not invent one.

Also untouched: the Slides admonition and its three links (including
`?print-pdf`), every widget iframe and its measured `height`, every figure
`src`, and the deck itself. **Decks stay** — a frame lesson and its deck are a
parallel pair on purpose, and `mech_check.sh` still requires both.

## The print fix (one agent, once — not per lesson)

Students need to print a lesson for notetaking, and today they cannot: a frame
page prints as **one page**, in both present and read mode, with the bottom
bar stamped on it. Cause: `.deck { height: 100dvh; overflow-y: scroll }` in
`book/_static/frames.css` puts the whole lesson in a fixed-height scroll
container, so print sees exactly one viewport. The repo's only `@media print`
block, in `custom.css`, targets `.bd-sidebar-primary`, `.bd-header` and other
theme chrome that no longer exists on any page.

Dispatch this once, early, in parallel with the Module 1 batch — every later
lesson then inherits it:

- Add `@media print` to `frames.css`: unset the deck's `height` and
  `overflow`, drop `scroll-snap`, set `min-height: 0` on `.frame`, and give
  each frame `break-after: page` so one frame prints per sheet with room to
  write beside it.
- Print always renders as **read** mode: show `:::{depth}`, so the handout
  carries the material the slide deck does not.
- Hide the bar, the rail, the index overlay, the laser and the spotlight.
- Add the same `@media print` treatment to `page.css` for reading pages, and
  delete the dead theme-chrome print block in `custom.css`.
- **Verify by printing, not by reading the CSS**: render a frame lesson to PDF
  headless and assert the page count is one per frame, not 1. Add that as
  `scripts/verify/check_print.py` so it cannot regress.

## Definition of done

Per lesson, and the agent pastes the output:

```sh
scripts/verify/mech_check.sh <NN> <slug>     # must be 0 failures
```

Per batch, run by you:

```sh
jupyter-book build book/ --all               # must stay at ZERO warnings
scripts/verify/check_shell.py
scripts/verify/check_bar.py
scripts/verify/check_frames.py
scripts/verify/check_parity.py <baseline>    # see CLAUDE.md for the baseline
```

`check_parity.py` is the safety net for this whole job: it names every page
whose rendered text or component counts changed. The list should be exactly
the lessons you converted, and you should read the diff for each one — that is
how a dropped learning objective or a lost table gets caught. A run that
compares zero pages is a failure, not a pass.

## Do not

- Do not hand-edit `book/_toc.yml`. `scripts/scaffold_lessons.py` regenerates
  it from its `LESSONS` manifest.
- Do not delete a deck, a widget, a figure, or a practice PDF.
- Do not rewrite lesson prose while converting. Re-cutting content into frames
  is in scope; rewriting sentences is a separate pass and will bury the parity
  diff in noise.
- Do not touch `latex/` or rebuild practice PDFs. `mech_check.sh` rebuilds
  them as a side effect — `git checkout` any that show up in `git status`.
- Do not convert the stubs.

## Retiring L05a

`L05a-field-regions-frames` is the frame-view copy of L05, built as the
experiment that proved the format. Neil's call: **one L05.** Once L05 itself is
a frame page the two are near-duplicates — both in the TOC, both in the search
index — and the copy goes.

Order matters. L05a is the reference example the docs point at, so do not
delete it until its replacement exists and passes:

1. Convert `L05-field-regions` and let `mech_check.sh 05 field-regions` pass.
2. Read the two pages side by side and move anything L05a has that L05 does
   not. L05a was authored separately and is 2,867 words against L05's 2,627 —
   assume it has beats worth keeping until you have checked, and check by
   diffing the rendered text, not by skimming.
3. Delete the `L05a-field-regions-frames` entry from the `LESSONS` manifest in
   `scripts/scaffold_lessons.py` (it is the tuple on the line beginning
   `(1, "L05-field-regions", "L05a-field-regions-frames"`), re-run the script
   to regenerate `_toc.yml`, and delete the directory.
4. Repoint every reference to the worked example at L05: `CLAUDE.md`,
   `project/FRAMES_ARCHITECTURE.md`, `README.md`. Grep for `L05a` and leave
   none behind except in historical notes.
5. The L05 page links to L05a as "frame view". That link becomes a link to
   itself — remove it and the paragraph explaining it.

L05a has no practice set or deck of its own; L05's are the real ones and stay.
