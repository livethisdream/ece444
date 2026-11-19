# Module 4 Integrator handoff (2026-11-19)

For a fresh Integrator session. Read CLAUDE.md, project/ROADMAP.md and
project/ECE444_PROJECT.md first; this note is only what is not in them.

## Cost rule (Neil, 2026-11-19)
Any thread you create gets an explicit `model`: Sonnet for routine edits;
Opus or Fable only with Neil's word. Archive a thread as soon as its work
merges. Do not keep a long-running Integrator context: start fresh.

## State
- L25-L31 and Radar Overview 1 and 2 are merged and live. Labs run the weeks
  of 30 Nov and 7 Dec. L28-L31 follow the Module 3 lab rules on one page:
  lesson half reading only, lab half presents at most ten beats, lean packet.
- Depth rule for provided processing stages (ROADMAP): what to expect, not
  how to build it. Radar equation in dB uses L_p = 40 log R + 20 log f - 136.6
  dB (L25 and Overview 1).
- Notebook autograders (ECE444-faculty/autograder): 1 or 0 a check, no key
  values in feedback. Points L28 2, L29 3, L30 4, L31 1.

## Open
- L28 CW warm-up (Neil approved 2026-11-19): the L28 thread
  (session_01Qxg9EKX6TLZPLTAZkEjS5B, Opus) is paused at its pick question for
  Neil. One procedure block in CW mode (Spectrum, a waved hand), one
  Predicted/Measured row in the packet.
- Neil's call: split each M4 page into a lesson page and an "L28 Lab" child
  page (so the lab is not buried; reverses his 25 Oct decision), or a lighter
  "jump to the lab" link plus a presented divider.
- Neil's calls still open: Extra Effort as the extra credit and its 5% cap;
  setting up the four Gradescope assignments (build each zip with
  `bash autograder/build.sh LNN` in ECE444-faculty).
- Unverified from containers: the live site and the simulator at
  livethisdream.github.io/phaser/radar/ (github.io is not reachable here).
- Phaser app issues for Neil's Phaser thread: recordings play about 66 dB
  low; Peak Range locks onto the leakage near 0 m; a single-chirp Save Capture
  replays as a burst; "metre" and "Colour" in the UI.
