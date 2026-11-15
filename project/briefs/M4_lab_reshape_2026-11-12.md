# Module 4 labs: reshape L28–L31 to the Module 3 lab rules (2026-11-12)

Neil, 2026-11-12: cadets have not started L28; the labs run the weeks of
30 Nov and 7 Dec. L28–L31 were finished on 4 Nov, before the lab rules of
8–12 Nov. Each page is rebuilt to those rules. One thread a page.

## What is different in Module 4: one page

The lesson and its lab are **one page** (`book/module04/LNN-*/index.md`),
lesson first, then the lab, one packet. Apply the Module 3 pair shape to it:

- **The lesson half is reading only** (Neil: "reading only, same as module
  3"). Every lesson frame is read before class and is not presented. It works
  every method Part 1 needs, prints **no value that equals a Part 1 answer**,
  and ends with a read-only **Pre-Lab** frame that maps each Part 1 prediction
  to the step lower on the same page that checks it.
- **Worked examples use a chirp the app does not.** Every kit runs the app's
  presets (COURSE_SPEC §M8.1), so the preset numbers (3.33 kHz/m, 0.30 m,
  0.118 m/s, ...) are the same Part 1 answers for every cadet. Work each
  method on another chirp (for example 400 MHz in 2 ms at 10.0 GHz) in the
  lesson half's examples, figures and widget defaults. Figures made from the
  recorded data may stay if they print no number Part 1 asks for.
- **The lab half is what is presented**, ten beats at most (`LAB_BEATS`):
  title, objectives, **The Big Picture** (what is measured by what is set, no
  outcomes), **Predict First** (a widget that hides its answer until the cadet
  commits), then **one beat per procedure block**. Fewer beats and a visual in
  place of bullets wherever one carries the beat. No step states a value Part
  1 predicts; it says to compare with the prediction. Then read-only: No
  Hardware? (the recorded-data and simulator path), Notebook Setup, Your Part
  2 Entries, Lab Packet, For Part 3, Looking Ahead.
- Add your page's line to `BEAT_EXCEPTIONS` in `scripts/verify/budgets.py`:
  `"L28": (LAB_BEATS, "one page, lesson half reading only (Neil, 2026-11-12)")`.

## The packet (ECE444-faculty), lean

Model: `ECE444_Lab_L21_Pattern.tex` on faculty `main`, with its macros
(`\predv`, `\predh`, `\kv`).

- **Predict, measure, analyze**, about four pages.
- **Predicted and measured share each table**: a shaded Predicted cell beside
  each white Measured cell. No separate prediction tables, no work box.
- Part 1 gives only what a cadet cannot know; it states no result and lists
  no steps. Part 2 is tables only, no prose questions.
- **Part 3 is two or three open-ended prompts** about what this lab measured.
  None leads to a set answer: none names the finding, its direction or its
  cause, and none would fit another lab unchanged. The key lists what a
  strong answer notices.
- No invented people, no invented readings. Timing is relative ("before
  Lesson 29"), never a date. The first page says what an analysis answer is
  graded on: claim, evidence, reasoning, uncertainty.
- The notebook's task results that the old packet recorded (Table E/F rows)
  go into the combined tables where they are a measurement; drop the rest.

## What stays

- The notebook, `radar_lab.py`, the recorded data, the bundles and the
  Gradescope autograder (`ECE444-faculty/autograder/LNN/checks.py`) stay as
  they are. Do not rename a notebook variable the autograder reads. If a
  notebook Check line now hands over a Part 1 answer, say so under "For the
  Integrator" rather than editing it.
- The app's presets and control names (§M8.1); the simulation-only track:
  every Measured cell must be fillable from recorded data or the simulator.
- Corner reflector: a 4 in trihedral (10 cm edge), settled.

## Rules to read first

`project/ROADMAP.md`; COURSE_SPEC "Lesson and lab, one shape" and "Lab packet
structure"; VOICE.md 27–43; the `write-lesson` skill (use it). Worked
examples: the L20 Lab page (#239) and the L21 Lab packet (#248, faculty).

## Edit rights

Your page, its figures and widgets, your line in `budgets.py`, your packet
`.tex`, key and blank PDF. Anything else goes under "For the Integrator".

## Done means

`jupyter-book build book/ --all` with 0 warnings; `mech_check.sh NN`;
`check_density` at or under 10; `check_frames`; `check_voice` 0 FAIL;
`check_widget` on any new widget, with a screenshot looked at; the packet
built with the real macros, 0 overfull boxes; the notebook still runs from
the bundle and the autograder still scores the solved notebook full. Stop
once for Neil's pick (the write-lesson review) before finalizing. Open ready
PRs in both repos; do not merge. Report to the Integrator with head SHAs.
