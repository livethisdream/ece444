#!/usr/bin/env bash
# Build the ECE 444 equation sheet and publish it to the site.
#
#   ./build_equation_sheet.sh
#
# Two lualatex passes so \numpages and the multicols* balancing settle.
# Needs the private house macros on TEXINPUTS:
#   export TEXINPUTS=/path/to/latex-tools/tex/latex//:
set -euo pipefail
cd "$(dirname "$0")"
JOB="ECE444_Equation_Sheet"

for _ in 1 2; do
	lualatex -interaction=nonstopmode -halt-on-error -jobname="$JOB" \
		"\\input{${JOB}}" >/dev/null
done
echo "built ${JOB}.pdf"

DEST="../book/extras/handouts"
mkdir -p "$DEST"
cp -f "${JOB}.pdf" "$DEST/"
echo "published -> $DEST/${JOB}.pdf"
