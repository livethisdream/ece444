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

### 9. Active voice; name the agent

Neil, on his own edit to the L4 lab packet: *"I heavily prefer active voice,
and squash passive voice everywhere I can."*

> **Before:** A VNA is used to measure S-parameters.
>
> **After:** We will use a VNA to measure S-parameters.

> **Before:** The markers may be moved by tapping and dragging.
>
> **After:** You can move the markers by tapping and dragging.

> **Before:** This calibration needs to be performed every time a cable is
> connected or the frequency range is changed.
>
> **After:** You must recalibrate every time you connect a cable or change the
> frequency range.

In procedure text the agent is almost always **you** or **the instrument**.
Naming it is not just style — it is what makes a step followable, because the
reader learns whose job each step is.

## Neil's own hand: the Lesson 7 edit (2026-09-06)

Neil edited the first half of L07 himself, 45 lines. Every pair below is his
wording replacing the draft's. Together with the ECE 448 decks and his papers,
this is the largest sample of his course voice in the repo.

### 10. Plain verbs, not colorful ones

> **Before:** That kills one power of $\sin\theta$.
>
> **After:** That eliminates one power of $\sin\theta$.

> **Before:** for longer wires the peak walks off broadside entirely
>
> **After:** for longer wires the peak moves off broadside entirely

> **Before:** The wire radius drops straight out
>
> **After:** The wire radius factors out

> **Before:** the reactive near field of Lesson 5, sloshing energy back and
> forth, doing no useful work, and wrecking your match.
>
> **After:** the reactive near field of Lesson 5, which does no useful work,
> and wrecking your match.

> **Before:** Now it is a first-year integral.
>
> **After:** This is a relatively straightforward integral.

The verb does its job and nothing else. "Sloshing," "kills," "walks off," and
"drops straight out" are the draft performing; his versions describe.

### 11. No kicker sentences

> **Before:** **Doubling the wire bought 0.39 dB of directivity.** The
> half-wave dipole is not famous for its pattern.
>
> **After:** **Doubling the wire brought 0.39 dB of directivity.**

> **Before:** Lesson 8 is where you find out how much it costs.
>
> **After:** we will be exploring the tradeoffs.

> **Before:** One integral covers every length, which is what the radiation
> integral is for.
>
> **After:** One integral covers every length, which is the entire purpose of
> the radiation integral.

The one-line payoff at the end of a paragraph, the sentence that lands the
point with a snap, is deleted or flattened every time it appears. State the
fact; do not close on it.

### 12. "We," not "you," for the work of the lesson

> **Before:** You have a current. Lesson 6 gives you the rest, and this is the
> one antenna in the course where we run that machine end to end.
>
> **After:** We start with the current and the radiation integrals of Lesson 6
> provide the rest, and this is the one antenna in the course where we will
> run that computation end to end.

> **Before:** So compute $P_\text{rad}$ and you have $R_r$.
>
> **After:** If we can compute $P_\text{rad}$, we can find $R_r$.

> **Before:** For this antenna you may quote gain and directivity
> interchangeably — but say which one you mean
>
> **After:** For this antenna we can quote gain and directivity
> interchangeably — but it is still helpful to be in the habit of specifying
> which one you mean

"You" survives for what the reader will do at a bench or an analyzer (§9).
For the derivation and the reasoning, the lesson is something we do together.

### 13. Titles are Title Case noun phrases

> **Before:** What doubling the wire bought you
>
> **After:** Why Double the Wire?

> **Before:** The current is assumed, not solved for
>
> **After:** The current is the excitation, not the solution

> **Before:** That integral has no elementary antiderivative
>
> **After:** Tricky Integrals

> **Before:** What the bars and the proportionality sign mean
>
> **After:** Absolute Value and Proportionality

> **Before:** The antenna that cannot exist
>
> **After:** The Impossible Antenna

A title names the topic. It does not make the point; the frame does.

### 14. Bold a term, not a claim

> **Before:** Here the derivation stops being algebra. **That integral has no
> elementary antiderivative.**
>
> **After:** Here the derivation stops being algebra. That integral has no
> elementary antiderivative.

> **Before:** The proportionality matters because **normalizing means dividing
> by the peak of that expression**
>
> **After:** The proportionality matters because **normalizing** means dividing
> by the peak of that expression

### 15. Concrete names, ordinary words

> **Before:** exactly what a spectrum regulator writes into a license.
>
> **After:** exactly what the FCC specifies in their licensing regulations.

> **Before:** Half a wavelength is the celebrated length because it puts the
> current maximum right at the feed point, and it costs only 0.39 dB of
> directivity to get there.
>
> **After:** Half a wavelength is the optimal length because it puts the
> current maximum right at the feed point, and it costs only 0.39 dB of
> directivity to implement.

Also "donut," not "doughnut"; "thick," not "fat"; "out of phase," not "out of
step"; "narrower," not "slimmer."

### 16. A physical picture over a theorem

> **Before:** It cannot exist. The argument is short. In the far field the
> electric field is transverse: it lies tangent to the sphere of constant
> $r$. A truly isotropic radiator would need that tangential field to be
> nonzero everywhere on the sphere with no direction singled out, and
> topology forbids it — you cannot comb a hairy ball flat.
>
> **After:** An isotropic antenna is a physical impossibility. In order to
> create an antenna, we have to separate charge, which inherently produces
> curved electric field lines, which means at some physical location the
> field has to vanish

Trees, not species. The cadet needs to believe the null is required, not to
know which theorem requires it.

### 17. What he kept

Em-dashes stayed in every sentence that had one, and he added a semicolon.
"Congratulations, you have built a center-fed dipole" went in. "Recall that
dB is a power ratio" went in. A little warmth and a reminder of a
prerequisite are both in the voice; a joke about the reader is not.

### 18. An equation gets its own line

> **Before:** **Lesson 6**: $\mathbf{N} = \int \mathbf{J}\ e^{+jk\hat{\mathbf r}\cdot\mathbf{r}'}\ dV'$, then $U \propto \vert N_\theta\vert^2 + \vert N_\phi\vert^2$, $\vert F\vert = \sqrt{U/U_\text{max}}$, and $D = 4\pi U_\text{max}/P_\text{rad}$.
>
> **After (his layout):** **Lesson 6: radiation integrals**, then each of
> $\mathbf{N}$, $U$, $\vert F\vert$, and $D$ as display math on its own line.

Neil, 2026-09-07: "Sometimes you include many equations in a line of text,
but we need to set them on their own line. This is a general rule. Unless it's
a simple equation, like $F = ma$, it should be on its own line. Reading it in
text makes it hard to follow the logic." Inline math is for a symbol, a value,
or a relation as short as $X_\text{in} = 0$. A fraction, an integral, a
product-to-sum identity, or a definition is display math, in prose and on
slides alike.

### 19. A derivation runs general to specific, as one chain

> **Before:** *Step 1: set up* $N_z(\theta) = \int I(z')\,e^{+jkz'\cos\theta}\,dz'$
> *Fold by symmetry* $N_z(\theta) = 2I_m\int_0^{L/2}\cdots$
>
> **After:** $\mathbf{N} = \int \mathbf{J}\,e^{+jk\hat{\mathbf r}\cdot\mathbf r'}\,dV'$,
> then $N_z(\theta) = \int I(z')\,e^{+jkz'\cos\theta}\,dz'$, then
> $= 2I_m\int_0^{L/2}\cdots$, aligned on the equals signs.

Neil, 2026-09-07: "You repeat $N_z(\theta)$. Step 1 starts with it, then we
do the symmetry argument, then you go back to $N_z(\theta)$. Always go from
general to specific. Going back and forth is confusing." Start from the
general form, specialize once, and continue the same equals sign. Never
restate a left-hand side the reader already has.

### 20. Standard, precise engineering language; no figurative framing

Neil, 2026-09-08: "Use standard, precise engineering language. Do not use
flowery phrases like 'what X bought you,' 'spend it on Y,' 'the shape of it
is...,' 'Z in one line.' Those get in the way of the material. The goal is to
make the material approachable and let the writing style get out of the way."

> **Before:** What doubling the wire bought you
>
> **After:** Why Double the Wire?

> **Before:** Today you spend that answer on hardware.
>
> **After:** Today we extend the math to real hardware.

> **Before:** The short dipole, in one slide
>
> **After:** The Short Dipole

> **Before:** Use the chart to understand the *shape* of the behavior
>
> **After:** Use the chart to see how the impedance moves with length

Money metaphors (bought, spend, cost, price, earn its keep, payoff), "the
shape of," "in one line," "in one slide," "the whole of it," and any phrase
that describes the explanation instead of the physics are out. Name the
quantity and say what it does.

### 21. No clipped sentences for effect

Neil, 2026-09-08: "Don't use short sentence fragments as a way to sound
concise. 'Start with the current. The calculus is easy.' That just doesn't
land in this course."

> **Before:** You have a current. Lesson 6 gives you the rest.
>
> **After:** We start with the current, and the radiation integrals of
> Lesson 6 provide the rest.

> **Before:** The calculus is elementary; the hard part was choosing the
> current.
>
> **After:** The integral is straightforward once the current is sinusoidal,
> which is why the sinusoidal assumption is worth making.

Section 4 bans verbless fragments. This goes further: a run of very short
complete sentences used for punch reads the same way. Prose in this course
runs at the length of his papers, with connectives, and a two-word sentence
is a signal that the writing is performing.

### 22. American English

Neil, 2026-09-08: "I live in America, so let's use American English. Do not
use 'centre,' 'colour,' etc." Also gray, canceling, labeled, license,
judgment, donut, and -ize. The rule and its sweep are in CLAUDE.md; it is
repeated here because it is a voice rule, not only a repo rule.

### 23. A slide states the point; it never withholds it

Neil, 2026-09-09, on L07's short-dipole frame: "It reads like clickbait ...
Why not just explain what's wrong with the impedance? In fact, the slide
doesn't say anything about the issue with the impedance. We don't have to
hook people into reading our material, that's my job. The job of the slides
is to provide context, a backdrop, and an outline."

> **Before:** The pattern is already almost as good as it gets. The
> impedance is the problem.
>
> **After:** On a 50 Ω line, 2 Ω gives |Γ| = 0.92 and VSWR 25: 85% of the
> power reflects.

A line that names a problem without stating it is a teaser, and a teaser is
a hook. The hook is his, spoken. If the point is worth a line on the slide,
the line carries the number or the mechanism; if it cannot, it goes to
depth or is cut.

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
hand-waving`, `is the price`, `dear reader`. Then grep for passive tells —
`is used`, `is shown`, `can be seen`, `will be connected`, `needs to be`,
`is referred to as`, and `\b(is|are|was|were|be|been)\b +\w+(ed|en)\b` — and
rewrite each one with its agent named. Then read every sentence and ask
whether it has a subject and a verb. Then ask whether any sentence is a joke,
a wink, or a judgment about the reader. Rewrite anything that is.
