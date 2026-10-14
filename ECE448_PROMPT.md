# Seed prompt — ECE 448 course site

Copy everything below the line into a new Claude Code session with
`livethisdream/ece448` and `livethisdream/ECE448-faculty` attached for push,
and `livethisdream/ece444` and `livethisdream/latex-tools` attached to read.

---

You are building the course site for **ECE 448, Software Defined Radios**,
Spring 2027, in `livethisdream/ece448`, served at
`livethisdream.github.io/ece448/`.

**Follow ECE 444.** Its site (`livethisdream/ece444`) is the model for the
formatting, conventions, and rules of this one. Read these first and do what
they say, unless something applies only to ECE 444's own subject:
`CLAUDE.md`, `project/ROADMAP.md`, `COURSE_SPEC.md`, `VOICE.md`, `REVIEW.md`,
and `.claude/skills/`. Use ECE 444's shell, scaffolder, checks, and LaTeX
harness as they are, changing only what a cadet sees, such as the course name.

What is already here:

- `ece448` has an older Jupyter Book with L01 written, and its decisions are in
  `project/ECE448_PROJECT.md`. Keep L01 and those decisions; bring the site up
  to ECE 444's shell rather than starting over.
- `ECE448-faculty` (private) holds the existing lessons and source material.
  It stays private: assessments, keys, and sources never go in `ece448`.

Before you scaffold anything, put the objectives, the lesson list, and the labs
to Neil and wait for his answers. Work on one branch, open one PR, and do not
merge it.
