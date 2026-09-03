# Seed prompt — cut the present layer into the frame lessons

Copy everything below the line into a new Claude Code session on this repo.

---

You are orchestrating the second pass over this antenna & radar course's frame
lessons: giving each frame a **present layer**, so that what the class sees on
screen is the frame's key points and its graphic, not the lesson prose.

Work on a branch cut from `main` after the present-layer mechanism has merged
(`book/_ext/frames.py` must define `PresentDirective`; check before you start).

## Read these first

- **`CLAUDE.md`**, the **Frame lessons** section: the `:::{present}` rules,
  the budgets, and the fence-nesting trap. Every line there is a defect that
  already shipped once.
- **`project/FRAMES_ARCHITECTURE.md`**, "The present layer": why, and the
  writing discipline that keeps read mode intact.
- **`book/module01/L05-field-regions/index.md`**: the worked example. Read it
  in full, once, and hold every other lesson to it.
- **`VOICE.md`** before writing or trimming any prose. Present blocks are
  prose too: complete sentences, no fragments, no self-praise.
- **`project/ECE444_PROJECT.md`**, running status. Only you, the
  orchestrator, edit it.

## The brief, in Neil's words

"Key points and graphics/animations on the side that I can talk to." The
present block is what he talks *to*, not what he reads *out*. If a present
block reads as a paragraph, it is wrong.

## Scope: 27 lessons

L01–L28 and `L04-lab-matching` are frame pages. L05 is done. The stubs
L29–L41 are not frame pages and are not in scope. Verify the list yourself:

```sh
python3 scripts/verify/check_density.py
```

Every line reading `uncut` is a lesson to do. The columns tell you how far
each one is from budget before you start.

## How to spend the budget

**Two stages per lesson.** Only the first needs judgement.

1. **Plan.** One agent reads the lesson page and its deck and writes a *cut
   plan*: for every frame, the present block's text (verbatim, ready to
   paste), whether the frame keeps its prose as depth or the prose needs a
   trim to avoid restating the present line, and which frames become
   `read-only` or merge. The deck is the best input: it is already the
   lesson cut into beats, and **the decks are the source of truth for
   nomenclature**. The plan must land the lesson under 30 present frames
   and every frame under 40 words; the planner checks its own counts with
   `check_density.py` against a scratch copy before it reports.
2. **Apply.** A second, cheaper agent applies the plan mechanically and
   makes no content decisions. If it wants to, it stops and reports.

**Gate every lesson with `scripts/verify/mech_check.sh <NN> <slug>`** after a
`jupyter-book build book/ --all`. The density check is inside it and bites
once the lesson has any present block; so is the frame-height check, which is
the one that catches a side-by-side stage that does not fit a phone.

**Batch by module.** Module 1 first (L01–L04, L06, the L04 lab), look at the
result yourself in present mode at 1280x800 and 390x844, then Modules 2 and 3.

## What a good cut looks like

- A claim frame: one or two complete sentences, the frame's topic sentence,
  the prose after it continuing that sentence. Not a summary of the prose.
- A figure or widget frame: the graphic in one present block and three or
  four key points in another, so they sit side by side.
- An equation frame: the lead-in clause and the equation, nothing else.
- A table frame: the table, trimmed to what a reader can take in at a glance.
- A derivation, a practice preview, a link list: `:class: read-only`.
- The title frame and the LO frame: leave them alone.

## What a bad cut looks like

- Bullets that restate the paragraph below them word for word. Trim the
  paragraph so it continues the bullets instead.
- A present block written in fragments to make the count. Forty words of
  complete sentences, or fewer words.
- A callout fenced *inside* a present block. It cannot nest; use
  `:::{present}` with `:class: callout`.
- Deleting prose to make a frame fit. Nothing on the page is lost to the
  present layer; that is the whole point of it.
