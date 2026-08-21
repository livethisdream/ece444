# ECE 444 — voice guide

The course's prose voice, captured from Neil's own review corrections. Read
this before writing any lesson page, deck, practice set, or assessment.
`COURSE_SPEC.md` §9 states the rules; this file is the calibration set — the
actual before-and-after pairs, so the target is concrete rather than abstract.

Every "after" below is either Neil's own wording or a rewrite he accepted.

## The target in one line

Plain, direct, professional. A competent colleague explaining something to
another engineer — not a performer, not a marketer, and not a friend being
clever.

## Paired examples

### 1. Say the consequence plainly; do not announce that you are about to

> **Before:** That is the whole of it, and it is worth being blunt about the
> consequence:
>
> **After (his wording):** It sounds simple, but there are consequences to
> this approach:

Do not narrate your own rhetorical moves ("it is worth being blunt", "here is
the honest caveat", "this is the most important paragraph in this lesson").
Just say the thing. If it is important, it will read as important.

### 2. Never vouch for the material's own honesty or rigor

> **Before:** The widget below runs an **honest** method-of-moments solve in
> your browser.
>
> **After:** The widget below runs a method-of-moments solve in your browser.

His objection, verbatim: *"no need to say 'honest'. if we're not being honest,
why are we writing this book?"*

Banned as self-praise: honest, genuinely, truly, really, actually, rigorous,
no hand-waving. The reader assumes the text is truthful and careful. Claiming
it implies the surrounding material is not.

### 3. Trade the epigram for a plain causal sentence

> **Before:** That simplicity is why NEC is fast, and the rules below are the
> price.
>
> **After (his wording):** That simplicity makes NEC fast, but we have to
> follow some rules to avoid divergent results.

Note what his version does: ordinary connective ("but"), first person plural
("we have to"), and it states the actual risk ("divergent results") instead of
gesturing at a "price". Cost-and-payment metaphors, and the "X is why Y, and Z
is the price" shape in particular, are out.

### 4. Complete sentences, always — no fragments for rhythm

> **Before:** Read the average gain as: 0.95 to 1.05, fine. 0.6 or 1.4, your
> model is broken and nothing else on the page means anything — go find the
> geometry error, the segment-length violation, or the misplaced source before
> you record a single number.
>
> **After:** An average gain between 0.95 and 1.05 is acceptable. A value near
> 0.6 or 1.4 means the model is wrong, and no other number on the page can be
> trusted until it is fixed. Check the geometry, the segment-length limits, and
> the source placement before recording any results.

His note: *"the first two sentences are fragments. this is widespread
throughout your writing. it's trying to be cheeky, but doesn't work in the
professional context."*

Verbless clauses used as sentences — "Same integral, three currents.",
"One integral, every length.", "Four times less area, two and a half times
less band." — are the single most common defect in this material. Directness
comes from short *complete* sentences, not dropped verbs.

### 5. State facts about the work, not verdicts about the reader

> **Before:** If a dipole calculation predicts 12 dBi or $8\ \Omega$, you have
> made an arithmetic error.
>
> **After:** A dipole calculation that returns 12 dBi or $8\ \Omega$ is outside
> the physically reasonable range and indicates an arithmetic error.

Also out: predicting that students who fail to learn something "will spend a
week finding out why". It reads as a taunt in a graded document.

### 6. Use the field's real vocabulary, and use it accurately

> **Before:** Card by card:
>
> **After:** Line by line:

"Cards" is correct NEC vocabulary where it names the input records, and it
stays there. But when walking a reader through a listing, "line by line" is
what a person says. Precision about *which* word is right matters more than
consistency for its own sake.

### 7. Quantities are symbols, not spelled-out words

> **Before:** Two ohms against a fifty ohm line is a hopeless match.
>
> **After:** $2\ \Omega$ against a $50\ \Omega$ line is a hopeless match.

Exception: speaker notes are spoken aloud, so "two ohms" is correct there.

### 8. Explanation belongs in the text, not inside the graphic

From his Smith-chart review: *"the Smith chart plot has too many words - those
should be in the text around it, not in the graphic."* A figure carries a
minimal key. The prose does the explaining.

## What he does *not* want changed

His voice is direct, and that is deliberate. Do not soften it into hedged
academic prose. These are all in the house voice and were kept on review:

- "Cut it long and trim. You can always remove wire."
- "Kill the reactance first; worry about the resistance second."
- "The edges are the antenna."
- "An unverified cal is an unmeasured antenna."

All four are complete sentences carrying real content. Short is good. Verbless
is not.

## Self-check before reporting

Grep your own draft for: `honest`, `genuinely`, `truly`, `rigorous`, `no
hand-waving`, `is the price`, `dear reader`. Then read every sentence and ask
whether it has a subject and a verb. Then ask whether any sentence is a joke,
a wink, or a judgement about the reader. Rewrite anything that is.
