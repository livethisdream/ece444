"""nec_lab -- NEC-2 for the ECE 444 dipole simulation lab.

A GUI and a CLI over the method-of-moments kernel, with two interchangeable
backends (PyNEC in-process, or a NEC executable such as the one inside a 4nec2
install) and a pattern export shaped for the chamber measurement tooling.

See README.md in this directory.
"""

__all__ = ["model", "engine", "study", "export", "cli", "serve", "selftest"]
