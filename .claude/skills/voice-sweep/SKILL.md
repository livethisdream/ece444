---
name: voice-sweep
description: Audit one lesson (page, deck, practice set) against VOICE.md, list the violations by section, stop for Neil's go-ahead, then fix them. Manual only -- run as /voice-sweep <NN>.
argument-hint: <lesson number, e.g. 15>
disable-model-invocation: true
---

# Voice sweep for one lesson

Run on demand, one lesson at a time: `/voice-sweep 15`. The lesson is
`$ARGUMENTS`. `VOICE.md` is the rubric; the L12 and L13 voice-sweep commits
(`a5e7033`, `5dd2346`) show the finished shape. Run this one before
`/why-sweep` on the same lesson, so the new derivations land in prose that is
already in voice.

The sweep has two phases with a hard stop between them. **Do not edit anything
in phase 1.**

## Phase 0: start clean

```sh
git fetch origin main && git checkout -B <your branch> origin/main
```

Read `VOICE.md` in full, every time. It grows (§24 was added 2026-09), and
the rules that matter most are the ones added most recently.

## Phase 1: audit, then stop

Read the lesson page, deck, and practice source in full. Then run the
mechanical pass:

```sh
F="book/module*/L<NN>-*/index.md book/extras/slides/L<NN>-*.md latex/ECE444_Practice_L<NN>.tex"
grep -niE 'honest|genuinely|truly|rigorous|hand-wav|is the price|dear reader' $F
grep -nE '\b(is|are|was|were|be|been) +\w+(ed|en)\b' $F        # passive tells
grep -niE '\b(buy|buys|bought|pay|pays|price|cost|costs|spend|cheap|free lunch|for free)\b' $F
grep -niE 'colo[u]r|cent[r]e|gr[e]y|dough[n]ut|met[r]e|(organi|recogni|optimi|minimi|maximi|normali|characteri|reali|utili|summari|emphasi)s(e|ed|es|ing|ation)\b' $F
grep -nE '\byou\b' book/module*/L<NN>-*/index.md | wc -l
```

Read each money hit. A price in dollars is fine. Everything else is §20:
"buys 6 dB" becomes "adds 6 dB", "costs 1.0 dB" becomes "loses 1.0 dB", and a
title like *Bandwidth Is What You Pay* becomes a noun phrase that names the
quantity.

Then read for what no grep finds, by `VOICE.md` section:

- §4, §21: fragments and clipped sentences. Every sentence has a subject and a
  verb.
- §11: kicker sentences ("That is not a radar.").
- §12: "you" where the lesson's own reasoning should be "we".
- §13: frame and slide titles that are not Title Case noun phrases.
- §14: bold on a claim rather than a term.
- §18, §19: inline non-trivial equations; derivations that restate a
  left-hand side.
- §20: figurative framing and money metaphors.
- §23: a present block or slide that teases the point instead of stating it.
- §24: a quantity described as a cause.

Report one table: location, section, the offending text (short), and the
proposed rewrite. Group by section. **Then stop and wait for Neil.**

## Phase 2: fix what Neil approved

- Keep what `VOICE.md` says to keep ("What he does *not* want changed"). Short
  and direct is the house voice; only verbless or figurative is out.
- Change wording, not content. If a sentence is in voice but wrong, fix the
  fact and say so in the commit message; L12's sweep found two corrupted
  equations and a wrong number this way.
- Renaming a frame title changes its `#frame-<slug>` anchor. Grep the book for
  links to the old anchor and update them.
- Mirror each change in the deck; deck slide titles go to Title Case too.
  Follow the marked gotchas in `CLAUDE.md`.
- Present blocks stay at 40 words or fewer; a sentence rewrite usually adds
  words, so rerun `check_density` after.
- Run the `VOICE.md` self-check on your own new text before reporting.

The pitfalls and the verification list are the same as the why sweep's: read
`.claude/skills/why-sweep/SKILL.md`, "Pitfalls already paid for" and "Verify
before pushing", and do all of it. In particular, rebuild the practice PDFs
only with lualatex and the real `latex-tools` macros, and restore them with
`git checkout -- book/extras/practice/` if the `.tex` did not change.

## Finish

Commit with a message that names the `VOICE.md` sections applied and any fact
corrected. Add **one short Status line** to `project/ECE444_PROJECT.md`. Push,
open the PR, and watch it to green.
