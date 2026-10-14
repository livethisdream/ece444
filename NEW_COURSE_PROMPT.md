# Seed prompt — a new course site (ECE 448, ECE 343)

Use this once per course. Fill in the block below, then copy everything below
the line into a new Claude Code session that has **this repo attached
read-only** and the **course's repos attached with push access**. One session
per course; do not bootstrap both in one thread.

Decided 2026-10-14 (Neil): each course gets **its own repo and its own GitHub
Pages site**. The ece444 shell is copied once, pinned to the ece444 commit it
came from, and later shell fixes are synced across deliberately, never edited
in two places.

**Repo naming** (Neil, 2026-10-14): the public site repo is named by the
course number alone, so every site is at `livethisdream.github.io/eceNNN/`:
`ece444`, `ece448`, `ece343`. The private repo is that course's faculty repo.
Never rename a public site repo, because Pages does not redirect the old URL.

The two courses start from different places:

| | ECE 448 | ECE 343 |
| :-- | :-- | :-- |
| Title | Software Defined Radios | Intro to Electromagnetics |
| Public site | `ece448` **exists**: an August Jupyter Book on the old theme, with L01 written, `deploy.yml`, and `project/ECE448_PROJECT.md` | `ece343` **does not exist yet** |
| Faculty | `ECE448-faculty`: Beamer lessons, Pluto material | `ece343-faculty`: the 2023 sources, grades, and HW |
| Other sources | none | `ece343-site` (private): the Spring 2025 sources, which are newer than the faculty repo's |
| Mode | **upgrade** in place (step 4a) | **new** |

```text
COURSE        = ECE 448                 # or ECE 343
TITLE         = Software Defined Radios # or Intro to Electromagnetics
TERM          = Spring 2027
MODE          = upgrade                 # or new
REPO          = livethisdream/ece448    # or ece343: public, serves the site
FACULTY_REPO  = livethisdream/ECE448-faculty   # or ece343-faculty
SOURCES       = <the faculty repo, plus ece343-site for 343, plus any uploads
                 or OneDrive paths>
LABS          = <hardware or software the labs run on, or "none">
```

---

You are bootstrapping a new course website, **{COURSE}, {TITLE}**, for
{TERM}, by copying the course-site machinery built for ECE 444
(`livethisdream/ece444`) and following its conventions. Your job is the shell
and the scaffold, not the content: when you finish, the site builds, deploys,
and has one shell page per lesson, and every rule ECE 444 settled is either
carried over or explicitly marked as not applying.

## 1. Read first, in ece444

Read these before anything else. They encode decisions already made; follow
them rather than re-deriving them.

- `CLAUDE.md`: the layout, the build, and above all the **gotchas that ship
  wrong silently**. Most of it is course-independent and carries over.
- `project/ROADMAP.md`: roles (Integrator, lesson threads), who may touch
  which files, and the settled rules.
- `COURSE_SPEC.md`: the authoring contract. Its general sections (frame
  lessons, decks, widgets, practice-set format, objectives) carry over; its
  antenna and Phaser sections do not.
- `VOICE.md`: Neil's prose voice. It is about Neil, not about antennas, so it
  carries over whole.
- `REVIEW.md` and `.claude/skills/{voice,why,illustration}-sweep/`: the review
  rubric and the three quality sweeps.

Then read whatever `SOURCES` points at. If it points at nothing you can open,
stop and ask Neil for it.

## 2. Settle the course with Neil first (stop and ask)

Do not invent any of this. Draft each from `SOURCES`, put the draft to Neil,
and wait for his answer before scaffolding:

1. **Objectives**, two levels, worded the way ECE 444's are ("I can ...").
   They go in the syllabus table and every lesson quotes them word for word.
2. **Modules and lessons**: titles, order, and which objective each serves.
   Lessons are topics, not class periods (Neil, 2026-10-13).
3. **Labs**: which lessons own a lab, and whether the ECE 444 lab model
   applies (the lab is a child page of its lesson, named "LNN Lab"; one packet:
   Pre-Lab, Measurements, Writeup; one submission, one Gradescope assignment).
4. **Decks**: ECE 444 keeps a reveal.js deck beside every frame lesson only
   because the frame view was still being proven. Ask whether a new course
   needs decks at all. If not, `mech_check.sh` must stop requiring them.
5. **Assessments**: how many, and when. They live in `FACULTY_REPO` only.
6. **Schedule**: the term's calendar, if Neil has it.

Record his answers in the new repo's `project/ROADMAP.md`, dated and in his
words where he gave them.

## 3. The repos

Creating, renaming, or archiving repos, enabling Pages, and granting access are
Neil's to do, unless he tells you to do them yourself. For a **new** course, ask
him to create `REPO` (public) and to turn on GitHub Pages from Actions on it.
Attach `REPO`, `FACULTY_REPO`, any source repo, and `livethisdream/latex-tools`
(private, the house LaTeX macros) with `add_repo`, then clone them.

**Sources stay private.** The source repos hold Beamer decks, solutions,
grades, and MATLAB scripts. Copy nothing from them into `REPO` wholesale.
Content reaches the public site only as lessons are authored, one checked file
at a time. A figure is published only once you have confirmed it is not part of
a solution. MATLAB is read for reference and ported to Python, never shipped.

**ECE 343 only:** `ece343-site` and `ece343-faculty` overlap, and
`ece343-site` holds the newer (Spring 2025) versions. With Neil's go, merge
`ece343-site` into `ece343-faculty` on a branch, keeping both terms where they
differ (`diff -rq` the two first), and open a PR there. Neil archives
`ece343-site` once it merges. Until then, read the 2025 material from
`ece343-site`.

Work on a branch, `claude/bootstrap`, and open one PR. Do not merge it.

## 4. Copy the shell

Copy from ece444 `main` and write down the commit you copied from (step 7).

**Copy verbatim:**

- `book/_ext/`, `book/_templates/`, `book/_static/` (the shell, frames,
  page, `viz-autosize.js`, `custom.css`, the sidebar shim; **not**
  `_static/materials/`, which is ECE 444's reference PDFs)
- `book/extras/viz/mjlabel.js`; `book/extras/slides/course-slides.css`,
  `deck-tools.js`, and `vendor/` (only if Neil keeps decks)
- `scripts/scaffold_lessons.py` (then empty its `LESSONS` and `LABS`
  manifests), `scripts/make_deck_html.py`, `scripts/build_interactives.py`,
  `scripts/graphics/svg_font_stack.py`
- `scripts/verify/` (all of it except `node_modules/`), including
  `budgets.py` with its per-lesson exceptions cleared
- `latex/build_practice.sh`, `latex/build_lab.sh`, `latex/ece444_fonts.tex`,
  `latex/fonts/Barlow/`, and the harness `ECE444_Practice_main.tex`
- `.claude/hooks/session-start.sh`, `.claude/settings.json`,
  `.claude/agents/reviewer.md`, `.claude/skills/` (all four)
- `.github/workflows/deploy.yml`, `requirements.txt`, `.gitignore`
- `book/DFEC-logo.png`, `book/favicon.ico`
- `VOICE.md`, `REVIEW.md`

**Copy, then rewrite for the course:** `book/_config.yml`, `book/intro.md`,
`book/syllabus.md`, `book/materials.md`, `CLAUDE.md`, `COURSE_SPEC.md`,
`project/ROADMAP.md`, `README.md`.

**Do not copy:** any lesson, module, deck, widget, figure, practice set, lab,
or PDF; `project/` notes other than the roadmap's structure; anything about the
ADALM-PHASER, the kits, or `latex-tools` content. Do not copy anything from
`ECE444-faculty`.

### 4a. Upgrading an existing site (ECE 448)

`ece448` already has a Jupyter Book, but it predates the shell: theme chrome,
`custom.css`, and a `legacy-slides/` folder, with no `_ext/` and no frame
lessons. Upgrade it in place on the branch:

- Read its `project/ECE448_PROJECT.md` first. Its decisions stand unless they
  conflict with this prompt: the `figures/` folder at the repo root, the
  faculty repo nested at `faculty/<semester>/` behind `/faculty/` in
  `.gitignore`, and authoring lessons as they are taught. Raise any conflict
  with Neil. Its "Spring 2026" is stale; the course runs {TERM}.
- Bring in the shell from step 4 over the old theme files, and keep
  `figures/`, `requirements.txt`, and the existing `deploy.yml` unless the
  ece444 versions are needed (diff them).
- **Keep L01.** Convert it to a frame lesson. Its words, its bio photos, and
  its deck stay; the structure changes. `check_parity.py` against a build of
  the current `main` should list L01 and the pages you meant to rewrite, and
  nothing else.
- Move the project note's open items into the new `project/ROADMAP.md`, and
  keep the note itself as `project/ECE448_PROJECT.md`.

## 5. Make it {COURSE}, and only where a reader sees it

Change what a cadet sees: the site title and repository URL in `_config.yml`,
the course name in the bottom bar, the scaffolder's `COURSE` constant,
`make_deck_html.py`'s `--course` default, `\thisclass` in the practice
harness, and the `ECE444_` prefix on practice, lab, and harness file names.
Then `grep -rn "444"` outside `_build/` and `node_modules/`, and account for
every hit.

**Leave the internal identifiers alone**: `ece444_shell`, `ece444_site_nav`,
`window.ECE444`, `ece444_frame_ids`, `ece444_fonts.tex`, and the like. They
are the shell's names, not the course's, and renaming them turns every later
shell sync into a hand merge. List them in `project/SHELL_ORIGIN.md` (step 7)
so nobody "fixes" them.

## 6. Scaffold

Fill `LESSONS` (and `LABS`, if the course has labs) in `scaffold_lessons.py`
from Neil's answers in step 2, and run it. It writes `book/_toc.yml`. Never
hand-edit that file.

- Each lesson is a frame-view shell: title frame, objectives frame quoting the
  course objective(s) word for word, and a read-only "Under construction"
  note. ECE 444's `book/module03/L19-direction-finding/` is the model.
- Each module index and the landing page are frame pages, built like
  ece444's.
- The syllabus objectives table is the single source for objective wording.
- No Practice section on any page until its PDFs exist.

## 7. Record where the shell came from

Write `project/SHELL_ORIGIN.md`: the ece444 commit you copied from, the list
of shell files (step 4's verbatim list), and the internal identifiers left as
`ece444_*`.

Add `scripts/sync_shell.py`. Given a local ece444 checkout and a ref, it diffs
every shell file against that ref and reports what changed, so a shell fix can
be brought across deliberately. It reports and does nothing else. The rule it
enforces: **a shell fix lands in ece444 first**, then syncs out. A course repo
never carries its own edit to a shell file.

## 8. The course's own docs

- `CLAUDE.md`: keep ece444's general gotchas and conventions word for word,
  replace the course specifics, and drop anything that is ECE 444's alone.
- `project/ROADMAP.md`: the same roles and ownership table as ece444's, with
  this course's lessons, status, work queue, and open decisions.
- `project/{COURSE}_PROJECT.md`: the running status note, started.
- `.gitignore`: keep the guard that keeps assessments and keys out of the
  public repo.

**Rules that carry over unchanged:**

- 20 present frames a lesson and 40 words a frame, from `budgets.py`.
- The `present` and `depth` model.
- A slide states the point, never a teaser for it.
- Two-level course objectives, quoted verbatim.
- Assessments never hand students the formula, and live in the faculty repo
  only.
- Python only, never MATLAB.
- American spelling and no thin spaces.
- The SVG font stack on every figure.
- Widget height budgets.
- Practice PDFs built only with the real macros.
- Always `jupyter-book build --all`.

**Rules that are ECE 444's alone, so do not carry them:**

- the ADALM-PHASER, kit addressing, and the hardware-day checklist;
- the no-receiver-vocabulary rule;
- the frozen decks;
- the 2026 renumbering history.

If you are unsure which side a rule falls on, ask.

## 9. Verify, by rendering

All of these must pass before the PR:

- `jupyter-book build book/ --all`: 0 warnings.
- `scripts/verify/check_shell.py` and `check_bar.py`, at both widths.
- `check_frames.py` on the landing page, every module index, and one lesson.
- `check_density.py` across all lessons.
- `mech_check.sh` on one lesson (after step 2's deck answer is applied).
- One practice-set smoke test: write a one-question set for L01, then build it
  with `TEXINPUTS=<latex-tools>/tex/latex//: bash latex/build_practice.sh 01`.
  Confirm the header reads {COURSE} in Barlow, then delete the set; ship no
  placeholder PDFs.
- `grep -rn "444"`: every hit is on the step 5 list of internal identifiers.

The CDNs are blocked in these containers. Vendor reveal.js and MathJax from npm
into `book/_build/`, as ece444's `CLAUDE.md` describes, before rendering.

## 10. Hand back

One PR on `REPO`. In its body:

- what was copied, and from which ece444 commit;
- Neil's answers from step 2;
- the scaffold, as a table of modules, lessons, objectives, and labs;
- the check results;
- what Neil still has to do: Pages, Gradescope, and the faculty repo's first
  commit.

Do not merge it.
