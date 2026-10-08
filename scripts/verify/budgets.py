"""Present-mode budgets: the one place to change them.

check_density.py reads these, and mech_check.sh gates on check_density, so a
change here moves every gate at once. The numbers are a measured pace, not a
law: change them when the classroom says so, and record why in the history
below and in COURSE_SPEC.md section M7.

History
-------
2026-09-03  WORDS 40, BEATS 30 (Neil: the frames were too dense to talk to).
2026-10-08  BEATS 30 -> 20 (Neil: "I can only get through 20 or so slides in a
            single period"). WORDS unchanged. Lab lessons count only the frames
            presented before bench time; their step-by-step procedure frames
            are `:class: read-only`, since teams follow them in read mode.
"""

# Words a present frame may show (the LO frame is exempt).
WORDS = 40

# Beats a lesson may have: shown frames in present mode, title and LO included,
# read-only frames excluded. One 53-minute period.
BEATS = 20

# Lessons allowed a different beat budget, with the reason. A lesson cut under
# an earlier budget is listed here until it is recut; delete its entry when it
# is. Keys match the lesson directory name by prefix (e.g. "L18").
BEAT_EXCEPTIONS = {
    "L05": (30, "cut under the 30-beat rule (2026-09); recut pending"),
    "L06": (30, "cut under the 30-beat rule (2026-09); recut pending"),
    "L07": (30, "cut under the 30-beat rule (2026-09); recut pending"),
    "L08": (30, "cut under the 30-beat rule (2026-09); recut pending"),
    "L09": (30, "cut under the 30-beat rule (2026-09); recut pending"),
    "L11": (30, "cut under the 30-beat rule (2026-09); recut pending"),
    "L12": (30, "cut under the 30-beat rule (2026-09); recut pending"),
    "L13": (30, "cut under the 30-beat rule (2026-09); recut pending"),
    "L14": (30, "cut under the 30-beat rule (2026-09); recut pending"),
    "L15": (30, "cut under the 30-beat rule (2026-10); recut pending"),
    "L16": (30, "cut under the 30-beat rule (2026-10); recut pending"),
}


def beat_budget(lesson):
    """The beat budget for a lesson directory name such as 'L18-beam-steering-theory'."""
    for prefix, (n, _why) in BEAT_EXCEPTIONS.items():
        if lesson.startswith(prefix + "-") or lesson == prefix:
            return n
    return BEATS
