---
name: write-lesson
description: Write a new ECE 444 lesson or lab page (or rewrite most of one) to the course's voice, "why", and illustration rules from the first draft, then run one parallel three-lens review and stop once for Neil's pick. Use it whenever a lesson thread creates or substantially rewrites a page under book/module*/; it replaces running the three sweeps afterwards.
argument-hint: <lesson number, e.g. 25>
---

# Write a lesson to the rules, then review it once

Neil, 2026-11-04: "Why do I have to do 3 separate sweeps after a lesson is
run? Why not just build those rules into the creation of lessons?" This skill
is that answer. The rules the voice, why, and illustration sweeps enforce are
applied while you write. One review pass at the end, three lenses in
parallel, replaces the three sweeps in sequence, with one stop for Neil
instead of three. The sweep skills stay for pages written before this one
existed.

The lesson is `$ARGUMENTS`. Read `CLAUDE.md` and `project/ROADMAP.md` first,
as for any work: who may touch which files, the budgets, and the gotchas
that silently ship wrong.

## 1. Before you write a word

- Read `VOICE.md` in full, every time. It grows, and the newest rules (25,
  first person; 26, every sentence earns its place; 41-43, problems and
  packets) are the ones most often missed.
- Read the earlier lessons this one builds on and note their notation with
  `grep -n`: L02's directivity and A_e, L05's field regions, L06's radiation
  vector, L07's dipole impedance, L12's T_A, L13's aperture efficiency, L16's
  array factor, L18's progressive phase. A link to an earlier lesson uses
  that lesson's notation and names it.
- Plan the figures and widgets with the outline, not after it. Candidates,
  strongest first (the illustration sweep's list): a mechanism the reader has
  to imagine; a trade with an optimum; a number chain; a rule of thumb against
  its data; a comparison stated in prose; the lesson's central idea, if it
  has no picture. Check `book/extras/viz/` and `viz/img/` for something to
  reuse first. A widget frame is a present beat; count it in the budget
  (`scripts/verify/budgets.py`).
- For a lab page, read current `livethisdream/phaser` `main` for anything the
  page will say about what the GUI or the backend shows or does.

## 2. While you write

Every sentence, as you write it:

- **Earns its place.** Ask what a cadet does or understands differently
  because of it. If nothing, leave it out; if something, say that thing.
  Build anecdotes, history, asides and repeated caveats are the usual
  offenders (VOICE 26).
- **Is in voice.** Complete sentences, active voice with the agent named,
  plain verbs, no kickers, no figurative or money framing, "we" for the
  lesson's own reasoning, first person for Neil and never "the instructor",
  bold on terms not claims, Title Case noun-phrase frame titles, American
  spelling (VOICE.md, all of it).
- **Says where a result comes from.** A mechanism, a derivation in read mode,
  or a named link to the lesson that derived it. Define every term the
  course has not; grep the earlier lessons before calling one undefined.
- **Has its numbers recomputed.** Compute every number in Python as you
  write it, not afterwards. Past sweeps found 0.01λ that should have been
  0.15λ, and 20 dB that should have been 23.
- **Agrees with the rest of the lesson.** One value per quantity, everywhere
  it appears; a change of unit or reference (dBFS to dBc) says what and why
  (VOICE.md 40).
- **Serves the story.** The opening frame states the lesson's one story as a
  plain outline, taken from what the cadet will see on the kit; no slogan,
  no teaser, no "cannot" without its reason, and no build-up for an effect
  smaller than the kit's own spread (VOICE.md 36-38). Antenna words for
  antenna things: an azimuth sweep, a null that drops to the noise floor
  (VOICE.md 39).

Every frame:

- A present block is two to four short bullets, a figure, a table, an
  equation chain, or a callout: 40 words at most, and it states the point,
  never a teaser for it. The connective prose goes outside the present
  blocks, where read mode shows it.
- A non-trivial equation gets its own display line, and a derivation runs
  general to specific as one chain aligned on the equals signs.
- The frame title is a directive argument, fences nest (`::::` frame, `:::`
  inside), and the frame fits one screen in present mode.
- No math in the raw-HTML objectives list, `\vert` not `|` in table math,
  `\ ` not `\,` or `\;`, no thin spaces (CLAUDE.md gotchas).

Every Module 3 lesson and lab pair has one shape (Neil, 2026-11-08: "The
lesson should be preparing them for the lab"; the L20 pair is the worked
example, lab page as approved in #239). Class time is the lab; cadets read
the lesson and do the pre-lab first.

- **The lesson** teaches everything the lab tests and how to read what the
  cadet will see. It is a reading page with no beat cap (`budgets.py`), and
  it ends with a read-only **Pre-Lab** frame that maps each Part 1 question
  to the step and table that checks it, linking the packet.
- **Every Part 1 method is worked on the lesson page, and no Part 1 answer
  is** (Neil, 2026-11-10). Go down Part 1 question by question: each needs a
  worked example of its method, or a one-line recap linking the lesson that
  worked it. Worked examples, figures and widget defaults use **10.0 GHz**;
  the kits run 10.1 to 10.7 GHz, so 10.3 and 10.525 GHz give answers away.
  No page prints a value that equals an answer-key value.
- **The lab page has cadets predict first** (Neil, 2026-11-10: the opening
  gave the answers away). Keep it as short as it can be, and prefer a figure
  or a widget to bullets ("Visuals are always better"); `LAB_BEATS` (10) is
  a ceiling. It presents: title;
  objectives; **The Big Picture**, listing what is measured by what is set
  or switched, with step ranges and no outcomes, expected traces or
  predicted numbers; **Predict First**, a widget that hides its answer until
  the cadet commits and asks, and hides it again on any change
  (`af-element-predict.html` is the model); then **one beat per procedure
  block**, each presenting three or four bullets of what the cadet does,
  with its steps and entry boxes in the frame's read-mode text. Equipment
  and Setup folds into Bring Up the Kit. No step states a value Part 1
  predicts; it says to compare with the prediction. Read-only after the
  procedure: No Hardware?, Your Part 2 Entries, Lab Packet, **For Part 3**
  (only what the writeup asks for), and a one-line Looking Ahead. No
  teaching on the lab page: a frame that explains goes in the lesson, or
  goes.
- **The packet's** Part 1 produces exactly the predictions Part 2 compares
  against, and Part 3 matches For Part 3. No practice set after L16.

Every lab page (VOICE.md 27-34, from Neil's L20 Lab notes):

- Steps run 1 to N straight through, a few frames of them, and the opening
  frame names the parts so the structure stays in sight. No A1, A2.
- A note about a step goes in that step's frame: the command, why, and
  what to do if it looks wrong. No later paragraph that says "Step 5 is".
- Say nothing the cadet already knows: no "per" headings, no second list of
  the kit, nothing an earlier lab already taught (the HB100's drift).
- Never "bench". Controls by the name a person would say ("the Array Factor
  preset"), not the GUI's numbered label.
- No dry-run anecdotes unless the cadet needs the number.
- Entry boxes at each step that takes a reading, and a summary frame, as
  the L17-L20 Labs do; packet boxes 1.5 in, right-justified in the 0.42
  answer column or in one row along the bottom of the part.
- Bold for control names, defined terms and step leads only; italics almost
  never (VOICE.md 35).

Every lab packet, practice set and assessment (VOICE.md 41-43, Neil,
2026-11-11):

- No invented people and no invented readings: never "a classmate", "a lab
  partner", "a colleague" or "a customer". A packet's data is the cadet's own.
- "What it doesn't explain", never "what X cannot show you" or "cannot tell
  you".
- A packet is predict, measure, analyze. Part 1 is a prediction table with
  Part 2's rows; it states no result and lists no steps. Part 3 is two or
  three open prompts about what this lab measured: none names the finding,
  its direction or its cause, and none would fit another lab unchanged.

Figures and widgets as you go: generators in `scripts/graphics/` through
`apply_font_stack()`, widgets from `book/extras/viz/reflector-gain.html` as
the template and inside `check_widget.py`'s budgets; the illustration
sweep's "Phase 2" section has the details and the screenshot list.

## 3. Check the draft yourself

```sh
python3 scripts/verify/check_voice.py L<NN>        # 0 FAIL; read every WARN
python3 scripts/verify/check_density.py L<NN>      # beats and words
jupyter-book build book/ --all                     # 0 warnings
python3 scripts/verify/check_frames.py L<NN>       # every frame fits
TEXINPUTS=/workspace/latex-tools/tex/latex//: scripts/verify/mech_check.sh <NN> <slug>
```

`check_voice.py` runs in CI on every page, so a FAIL there blocks the PR
anyway; a WARN (passive, money words) is a sentence to read and usually
rewrite.

## 4. One review, three lenses, in parallel

Start three `reviewer` subagents in one message, so they run at once. Give
each the page(s), the practice source if there is one, the earlier lessons the
page links to, and exactly one lens:

| Prefix | Lens | Give it |
| :-- | :-- | :-- |
| `VOI` | voice | `VOICE.md`, and the reading list in `.claude/skills/voice-sweep/SKILL.md` phase 1 |
| `WHY` | why | the "Look for" list in `.claude/skills/why-sweep/SKILL.md` phase 1, including recomputing every number |
| `ILL` | illustration | the ranking list in `.claude/skills/illustration-sweep/SKILL.md` phase 1, and the beat budget |

Merge their findings into one table: rank by student impact, drop
duplicates, and put each finding's proposed fix in one line. Then **stop
and wait for Neil's pick**, once, for all three lenses. Fix what he picks,
rerun section 3, and look at the present-mode screenshot of every frame you
changed at 390 and 1280.

## 5. Finish

The PR body lists the review findings fixed and the ones Neil left, every
number corrected, and anything outside the lesson's files under "For the
Integrator". A lesson thread does not edit `project/ECE444_PROJECT.md` or the
ROADMAP; report status in the PR body.

After the lesson is taught, what the cadets actually tripped over is the one
thing no draft review can catch: when Neil reports it, fix the page in a
short follow-up PR.
