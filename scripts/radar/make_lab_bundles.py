#!/usr/bin/env python3
"""Zip each Module 4 lab's files into one download: the notebook, radar_lab.py,
every recorded capture of that lab, and the data README.

    python3 scripts/radar/make_lab_bundles.py [OUT_DIR]

OUT_DIR defaults to book/_build/html/bundles, so it runs after the book is
built (CI does this in deploy.yml) and the lab pages can link
../../bundles/L28_lab.zip. The zips are built, never committed: they would
duplicate the ~45 MB of recorded data already in book/extras/radar-data/.

A cadet unzips one bundle into their Module 4 folder and every notebook cell
finds its files (Neil, 2026-11-04: the Notebook Setup frames listed fewer
files than the notebooks load).
"""
import sys
import zipfile
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
EXTRAS = REPO / "book" / "extras"
NOTEBOOKS = {
    "L28": "L28_range.ipynb",
    "L29": "L29_range_doppler.ipynb",
    "L30": "L30_cfar.ipynb",
    "L31": "L31_classify_track.ipynb",
}


def bundle(lab, out_dir):
    nb = EXTRAS / "notebooks" / NOTEBOOKS[lab]
    files = [nb, EXTRAS / "notebooks" / "radar_lab.py",
             EXTRAS / "radar-data" / "README.txt"]
    files += sorted((EXTRAS / "radar-data").glob(f"{lab}_*.npz"))
    missing = [f for f in files if not f.exists()]
    if missing:
        raise SystemExit(f"{lab}: missing {', '.join(str(m) for m in missing)}")
    out = out_dir / f"{lab}_lab.zip"
    # Stored, not deflated: complex IQ barely compresses, and stored zips
    # open instantly on any laptop.
    with zipfile.ZipFile(out, "w", zipfile.ZIP_STORED) as z:
        for f in files:
            z.write(f, f.name)
    print(f"{out.relative_to(REPO) if out.is_relative_to(REPO) else out}: "
          f"{len(files)} files, {out.stat().st_size / 1e6:.1f} MB")


def main():
    out_dir = Path(sys.argv[1]) if len(sys.argv) > 1 else REPO / "book" / "_build" / "html" / "bundles"
    out_dir.mkdir(parents=True, exist_ok=True)
    for lab in NOTEBOOKS:
        bundle(lab, out_dir)


if __name__ == "__main__":
    main()
