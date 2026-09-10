# /// script
# requires-python = ">=3.10"
# dependencies = []
# ///
#
# The dependency list is empty on purpose, and that is the design rather than
# an omission: nec_lab needs nothing but the standard library, so `uv run` on
# this file spins up in a moment and never has to build anything. The NEC
# engine is the one thing that varies, and it is not always a Python package --
# on Windows it is the executable inside 4nec2, where PyNEC cannot be built at
# all. Listing PyNEC here would make `uv run` fail on exactly the machines the
# fallback exists for. To use the in-process engine on Linux, macOS or WSL:
#
#     uv run --with PyNEC scripts/nec_lab/run.py serve
#
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
