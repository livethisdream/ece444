#!/usr/bin/env bash
# Build the ECE 444 midterm project description as a single PDF.
#
#   ./build_project.sh [SLUG]     # SLUG defaults to Midterm
#
# Content lives in ECE444_Project_<SLUG>.tex. Unlike the labs there is no
# KEY/blank split -- a project description has no worked answers in it, so one
# document is the whole deliverable. Runs lualatex twice for \numpages.
# lualatex, not pdflatex: the body font is Barlow, loaded as OpenType via
# fontspec (ece444_fonts.tex).
#
# Needs the house macros from the private latex-tools repo:
#
#   TEXINPUTS=/workspace/latex-tools/tex/latex//: bash build_project.sh
#
# The committed PDF under book/extras/projects/ IS what the site serves --
# book/extras/ is copied to the built site root (html_extra_path) and CI never
# runs LaTeX.
set -euo pipefail
cd "$(dirname "$0")"
SLUG="${1:-Midterm}"
SRC="ECE444_Project_${SLUG}"
JOB="ECE444_Project_${SLUG}"

for _ in 1 2; do
	lualatex -interaction=nonstopmode -halt-on-error -jobname="$JOB" \
		"\\input{${SRC}}" >/dev/null
done
echo "wrote ${JOB}.pdf"

DEST="../book/extras/projects"
mkdir -p "$DEST"
cp -f "${JOB}.pdf" "$DEST/"
echo "published -> $DEST/${JOB}.pdf"
echo "done."
