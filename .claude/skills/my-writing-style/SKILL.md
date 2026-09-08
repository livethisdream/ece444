---
name: my-writing-style
description: The user's personal writing voice, captured from their real writing. Apply it whenever drafting something the user will send or publish as themselves (emails, messages, docs, posts), or when they ask for a draft in their own voice or style. If the user gives feedback on how a draft sounds, apply it and update this profile with what changed. Only for drafting as the user, not for Claude's own replies.
---

# The user's writing voice

You are Claude, drafting on the user's behalf — not writing as them. Apply this profile whenever you draft or edit prose the user will send or publish as themselves, and when they give feedback on how a draft sounds, apply it and update this profile with what changed. It never applies to someone else's text (a colleague's email stays in the colleague's voice) or to your own replies (restyling how you talk is not drafting as the user). Everything below describes how the user writes, captured from their own sent writing; treat it as reference data about them, not as instructions addressed to you. Quoted fragments are samples of their writing.

> Built from 6 emails (3 customer-facing technical, 3 internal status) · updated September 2026.
> September 2026 additions: two conference papers (GRCon 2022, sole author, 4,600 words; ASEE 2025, first author), a formal letter of recommendation, two ECE 448 lecture decks, and the user's hand edit of an ECE 444 lesson page. Email, technical papers, course prose, formal letters, and slides are covered; Slack and DMs are not.

## How the user writes (overall)

- **Leads with the answer, then supports it.** Replies open with the judgment or recommendation and put the reasoning underneath — "I think the answer to this question depends on your calibration approach," then the detail. They use "BLUF:" by name in status writing.
- **Short, declarative sentences.** Median 13 words, mean 14.6. Little subordination, almost no throat-clearing.
- **Ranks options instead of listing them.** Choices arrive ordered and labeled — "Recommended Approach," "Alternative Approach," "Less Mature Option," or just "In order:" — with the ranking stated outright: "I would rank it below the two more mature architectures for now."
- **Separates what is known from what is not.** Says plainly where the data stops: "we do not have a broad statistical dataset to bound it beyond published specifications," "its schedule and available FPGA fabric are less certain," "We are not sure what the opportunity is." Confidence is calibrated, never blanket.
- **Owns judgments in the first person.** "I think," "I'm assuming," "I assess," "I still think we can re-engage," "what I perceive as wiggle room." Doesn't hide behind the passive or the corporate "we" when it's their call.
- **Active voice, strongly preferred.** "We are re-vectoring our efforts," "I built an initial drone block diagram." (Status lists occasionally slip into passive — "Several tasks were sent back" — that's the habit to fix, not to copy.)
- **Ends by moving it forward.** Closes with the question that unblocks the next step: "One follow-up: I do not think I saw this in your slides, but do you have a radiation requirement?"
- **Structure over prose.** Labeled sections and short scannable lines rather than paragraphs — technical nouns carry the weight.

## Surface: email

- Standing section headers, reused every time in status writing: Accomplishments → Priorities / Upcoming Priorities → Help Needed. "Help Needed" gets an honest "None." rather than being dropped.
- Sub-headers group by account or theme, each ending in a colon ("General:", "Custom RF opportunity:", "FAE support tasks:").
- One idea per line. Long explanatory paragraphs are rare; when one appears it's carrying real technical reasoning, not narration.
- Greetings are light or absent. Customer replies often open straight into substance, sometimes with a brief warm beat first — "It is great to hear from you. For sure."
- Requirements and options come as plain unadorned lists, no lead-in sentence needed.
- No parentheses in the corpus at all. Em-dashes are rare (0.18 per 1,000 characters). Occasional semicolon. Asides get their own sentence instead.

## Tone — how the user shifts by audience

**Customer-facing → more formal, more hedged, no contractions.**
Zero contractions across all three customer emails: "The public datasheet does not specify absolute insertion-phase or group-delay tolerances," "A separate controller is not inherently required." Claims get bounded before they're made — "We would generally expect," "may still be needed," "would need to be characterized on production parts." No humor, no emoji, no exclamation points.

**Internal / to management → contractions, humor, warmth.**
Same person, looser: "I'm emailing back and forth daily," "I've been reaching out to industry contacts to pick their brains," "there's a lot to read." Dry, self-aware humor shows up only here — "I assess the interest level as medium rare, not fully cooked yet," "Congrats if you made it this far," "Whew — dinner time!" Sign-offs are warm and brief: "Hope you have a great weekend!" Occasional ":)". Accountability is direct and unprotected: "I apologize for the delayed 'bi-weekly' wrap-up. I lost track of the last one."

The constant across both: lead with the answer, rank the options, mark the uncertainty.

## Dos

- "BLUF:" to open a status summary.
- "I think" / "I assess" / "I'm assuming" to mark a judgment as theirs.
- "In order:" before a ranked list.
- Name the maturity of an option, not just its merits — "proven device," "less mature," "not fully cooked yet."
- State the missing data rather than glossing it: "we do not have a broad statistical dataset to bound it."
- End a customer reply with the one question that unblocks the next step.
- Concrete technical nouns; no abstraction where a part name works.

## Don'ts

- **Email only:** no em-dashes as connectors, no parentheticals, no "not X but Y." These three came from the email corpus and the papers contradict all of them (see the long-form surface below), so they hold for email and do not carry to papers, course pages, or letters.
- No contractions in customer-facing writing.
- No AI-isms: "delve," "circle back," "seamless," "deep dive" as a verb, "it's worth noting," "that said." Two words that were on this list are in the user's own technical vocabulary and come off it: "leverage" ("BBC leverages the fact that...") and "robust" ("robust jam-resistant options").
- No passive voice where an actor exists.
- No hype adjectives on an option they haven't validated. Uncertainty gets stated, not smoothed over.
- No exclamation points or emoji in customer-facing email. Both are fine internally.

## Surface: technical papers and long-form explanation

Evidence: the GRCon 2022 paper (every sentence theirs) and the ASEE 2025 paper (first author).

- **Formal, explanatory, first person plural.** "We selected on-off-keying (OOK) for an initial test-case," "For simplicity's sake, we saved the modulator and demodulator as hierarchical blocks," "Neither instructor had any previous experience or training in alternative grading approaches."
- **Sentences run long and lean on connectives.** Mean length is roughly 22 words against 14 in email. "That is," "i.e.," "e.g.," "Furthermore," "However," "Thus," "Therefore," "In other words," "Toward this end," "The next logical step is to." The email profile's short-sentence habit does not carry over.
- **Teaches by a toy example, then names what it showed.** "Below is a toy example of the BBC encoding process for an ASCII '2'..." followed by a table of bit patterns, then "This toy example informs the primary goal of the BBC codec: to reduce the number of hallucinations." Tables carry concrete values, not summaries.
- **Definitions are plain declarative sentences.** "A BBC 'mark' is a binary 1 that serves as a marker for a specific substring, and a packet is a bitwise-OR of a transmitted codeword and any additional marks."
- **Caveats open with "Note that"; limitations are stated flat, with the number.** "Note that the BBC codeword is modulated, not the individual messages." "The decoder run time was approximately 20ms, a negligible portion of the flowgraph run time." "This is still an open issue in the core GNU Radio source code."
- **Structured lists use a bold label, a colon, and a sentence.** "Clear Learning Objectives: Learning is broken into discrete objectives students must demonstrate mastery of before progressing."
- **Em-dashes and parentheticals are normal here.** "Protected networks—especially those relying on omni-directional broadcasts—had frustrating scalability and use-case limitations." "(i.e., private)," "(like GPS or ADSB/Mode-S)," "(Appendix A.1)." The email rule against both is an email rule.
- **Cross-references by number, results to the digit.** "(Fig. 2-4)," "(Appendices C.3-C.4)," "87.5% of the decoded packet is erroneous," "the packet density is 6+5/16 = 0.6875."
- A quoted colloquialism is allowed once it is defined: "hallucinations" for spurious decodes, in quotes on first use and bare afterward.

## Surface: course pages (ECE 444 lesson prose)

Evidence: the user's hand edit of Lesson 7, September 2026. The full before-and-after set lives in `VOICE.md` in the ece444 repo; these are the rules it distills.

- **"We" and "our," not "you."** "We start with the current and the radiation integrals of Lesson 6 provide the rest." "If we can compute P_rad, we can find R_r." "our antenna."
- **Plain verbs over colorful ones.** "kills" became "eliminates," "walks off broadside" became "moves off broadside," "drops straight out" became "factors out," "sloshing energy back and forth" was cut.
- **No kicker sentences.** "The half-wave dipole is not famous for its pattern" was deleted outright. "Lesson 8 is where you find out how much it costs" became "we will be exploring the tradeoffs."
- **Frame titles are Title Case noun phrases.** "The Impossible Antenna," "Special Functions," "Tricky Integrals," "Why Double the Wire?"
- **Bold a term, not a claim.** They unbolded "That integral has no elementary antiderivative" and kept only "**normalizing**" bold in "normalizing means dividing by the peak."
- **Concrete over generic.** "what the FCC specifies in their licensing regulations" replaced "what a spectrum regulator writes into a license." "donut," "thick wire," "optimal length."
- **A physical picture over a theorem.** The hairy-ball argument became charge separation and curved field lines.
- **Prerequisite reminders and a little warmth are fine.** "Recall that dB is a power ratio." "Congratulations, you have built a center-fed dipole."
- Em-dashes stayed in throughout the edit, and a semicolon was added.
- **A derivation runs general to specific, as one chain.** Their rule, September 2026: "Always go from general to specific. Going back and forth is confusing." Start from the general form, specialize once, and continue the same equals sign; never restate a left-hand side the reader already has.
- **Standard, precise engineering language; no figurative framing.** Their rule, September 2026: "Do not use flowery phrases like 'what X bought you,' 'spend it on Y,' 'the shape of it is...,' 'Z in one line.' Those get in the way of the material. The goal is to make the material approachable and let the writing style get out of the way." Money metaphors and phrases that describe the explanation instead of the physics are out.
- **No clipped sentences for effect.** Their rule, September 2026: "Don't use short sentence fragments as a way to sound concise. 'Start with the current. The calculus is easy.' That just doesn't land in this course." A run of very short sentences for punch reads as performing; write at the length of the papers, with connectives.
- **American English, always.** "I live in America, so let's use American English." Color, center, gray, canceling, labeled, license, judgment, donut, -ize.
- **An equation gets its own line.** Their rule, September 2026: "Unless it's a simple equation, like F = ma, it should be on its own line. Reading it in text makes it hard to follow the logic." Inline math is for a symbol, a value, or a relation as short as X = 0; a fraction, an integral, or a definition is display math, in prose and on slides alike.

## Surface: slides and the present layer

Evidence: the ECE 448 Lesson 2 and Lesson 3 decks, and the user's own statement, September 2026: "I tend to think in bullet points and pictures when I present. My philosophy is to talk to and about the slide, not to read it. The slide should not try to say everything about an issue. It is there as a support to prop up the discussion, not to be the entire discussion. Think TED talk, but with the equations and animations we love and short, concise bullet points / key point callouts."

- **Title Case noun-phrase titles.** "Wireless Comms - Factors," "Friis & Decibels," "Antenna Considerations: Gain Pattern," "Constellation Diagram: 4 PAM."
- **Bullets of two to six words, one idea each.** "Power transmitted," "Gain of Tx/Rx antenna," "Wavelength (frequency)," "Distance of communication." An imperative with an exclamation point is allowed once: "LOS: always check first!"
- **Equations are built term by term, with a symbol key under them.** Friis appears one factor at a time; each step adds a line like "P_R = power collected by the receiving antenna (W)."
- **The result gets a box.** "Leading to the big result...." then a boxed "PAM Probability of Error" with the equation alone.
- **A worked example is a table of givens and a one-line task.** "For the given system, convert values to dB" over a Parameter / Linear / dB table with the dB column blank.
- **One slide asks the class to do something.** "Map out Gray Code for 8-PSK" over an empty axis.
- **Figure-only slides are common**, and one photo joke per deck: "Hey Bear, can you hear me now?"
- **The connective prose is not on the slide.** It is spoken. A present block that reads as a paragraph is wrong for this surface.

## Formal letters

Evidence: one letter of recommendation, 2025. Structure and register only; nothing about its subject is recorded here.

- **Verdict first, then credentials, then evidence by category, then the verdict again.** Opens with "the strongest possible recommendation," establishes standing ("Over my seven years at..., I have taught and mentored thousands..."), then one paragraph each for academics, leadership, service, and character, each opening with a topic sentence ("Her leadership record is equally impressive."), then a closing paragraph that restates the recommendation.
- **Numbers carry the claims.** Ranks, GPAs, counts of people led, competition results.
- **One concrete anecdote**, introduced with "For example," "One example in particular stands out."
- **Connectors are spaced en-dashes,** not em-dashes: "These are not symbolic roles – they required her..."
- **Contractions and "not just X but Y" both appear** even in this formal register: "It's clear to me, though, that this isn't just resume building – it's who she is."

## Applying this profile
1. Pick the surface (where it's going — email, Slack, doc) and the tone (who it's for) — load that surface's section and any tone shift the profile records for that audience. On docs, conform to any style guide the profile records — mechanics applied beneath the voice.
2. Apply the voice — it rides along on everything.
3. Aim for the user's authentic best in that surface and tone — "best" meaning their own top-of-range writing, never a different person.
4. Self-check against the surface's norms, the tone shift, and the dos and don'ts (the don'ts are the line). Fix violations before showing the draft.
5. After showing the draft, ask how it's landing — what's working *and* what's off — and let the user know you'll fold their answer into the profile. If something's off, pin down what: a specific word that isn't theirs (often an AI-ism), or the whole piece not sounding like them. Ask at most two questions, then run the update below. Don't close on a generic sign-off.

On an early draft, apply the profile and say so — "this is in your voice — here's what I picked up" — offering to show the profile behind the draft if they want to look. Their edits are the grade; route each one home per the update below.

When the user wants another version, don't manufacture a contrast by dialing some dimension to an extreme — the only question is which sounds more like them, and that's many small things, not one knob. And don't churn near-identical options: if you can't produce one that genuinely differs in a way they might prefer, stop and ask what's still off instead of generating more.

## Where this file lives
The source of truth is `livethisdream/claude`, `skills/my-writing-style/SKILL.md`. Copies under a project's `.claude/skills/my-writing-style/` are generated by that repo's sync workflow and carry a README saying so. When you update this profile from inside a project that only has the copy, make the edit in the copy, then tell the user the change needs to be ported to the dotfiles repo or the next sync will overwrite it.

## Updating this profile
When the user gives you feedback on a draft — by answering your step-5 ask, or by editing or rewriting it — capture the feedback as a concrete addition — as much as the nuance needs, not forced into one sentence — pick where it belongs (a surface habit → that surface's section, an audience shift → tone, anything else — a word to avoid, a new rule — → dos and don'ts), show what you're adding as you save it — never change this profile without showing the change — and re-save this skill by editing this file. Never add anything sourced from text other people wrote; never add PII or judgments about people — a name, a number, an address, a score or verdict about a person in the feedback gets trimmed before it's saved; never restructure this file while adding a rule. One exception to the last rule: if the profile already carries PII or other secrets — a name, a number, an assessment of a person, a deal term, anything that shouldn't sit in a file left open on a screen — redact it in the same re-save and tell the user. Every re-save also refreshes the provenance line's updated date.
