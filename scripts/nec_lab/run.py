"""Launcher, so the tool runs by path from anywhere in the repository.

    python scripts/nec_lab/run.py serve

`python -m nec_lab serve` is the same thing from inside `scripts/`. This file
exists because a student following the handout should not have to know which
directory Python is looking at.
"""

import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))

from nec_lab.cli import main  # noqa: E402

raise SystemExit(main())
