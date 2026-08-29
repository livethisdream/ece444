#!/usr/bin/env bash
# Build the ECE 444 equation sheet (Modules 1-3) as a single PDF.
#
#   ./build_equation_sheet.sh
#
# Content is ECE444_Equation_Sheet.tex -- a standalone extarticle document
# (no harness), modeled on Neil's ECE 343 equation sheet. Computer Modern
# math throughout (no Barlow), so lualatex is run first for house-toolchain
# consistency with the rest of latex/; if it chokes on the pdflatex-era
# refcards.sty preamble, pdflatex is the documented fallback.
set -euo pipefail
cd "$(dirname "$0")"

JOB="ECE444_Equation_Sheet"

run_engine() {
	local engine="$1"
	for _ in 1 2; do
		"$engine" -interaction=nonstopmode -halt-on-error "${JOB}.tex" >/dev/null
	done
}

if run_engine lualatex; then
	echo "built ${JOB}.pdf with lualatex"
else
	echo "lualatex failed on ${JOB}.tex -- falling back to pdflatex" >&2
	run_engine pdflatex
	echo "built ${JOB}.pdf with pdflatex"
fi

# Publish to the site. book/extras/ is copied to the built site root
# (html_extra_path); the committed PDF under extras/handouts/ IS what the
# site serves.
DEST="../book/extras/handouts"
mkdir -p "$DEST"
cp -f "${JOB}.pdf" "$DEST/"
echo "published -> $DEST/${JOB}.pdf"
echo "done."
