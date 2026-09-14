#!/bin/sh
# nec_lab -- double-click launcher for macOS (and runnable on Linux).
# Uses the system Python; the NEC engine comes from PyNEC or from nec2c.
exec python3 "$(dirname "$0")/run.py" serve "$@"
