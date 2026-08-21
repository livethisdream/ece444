#!/usr/bin/env bash
# Build an ECE 444 lab packet as two PDFs: the KEY copy (red worked solutions)
# and the blank student copy (work space reserved).
#
#   ./build_lab.sh [SLUG]        # SLUG defaults to L04_Matching
#
# Content lives in ECE444_Lab_<SLUG>.tex. Unlike the practice sets there is no
# separate harness -- each lab is a standalone document. Runs pdflatex twice
# per version for \numpages.
#
# The VNA photographs live in the course figures folder, not in this repo.
# Pass NOFIGS=1 to substitute placeholder boxes (lets the packet compile on a
# machine without them -- useful for a syntax check in CI or a web session):
#
#   NOFIGS=1 TEXINPUTS=/workspace/latex-tools/tex/latex//: bash build_lab.sh
#
# Only the blank student copy is published to the site. The KEY is left in
# latex/ and is NOT committed (see .gitignore) -- the lab is a graded team
# deliverable, so its solutions do not belong on the public site.
set -euo pipefail
cd "$(dirname "$0")"
SLUG="${1:-L04_Matching}"
SRC="ECE444_Lab_${SLUG}"

NOFIGSDEF=""
if [[ "${NOFIGS:-0}" == "1" ]]; then
	NOFIGSDEF="\\def\\nofigsIn{}"
fi

build() {                       # build <iskey:0|1> <suffix>
	local iskey="$1" suffix="$2"
	local job="ECE444_Lab_${SLUG}_${suffix}"
	for _ in 1 2; do
		pdflatex -interaction=nonstopmode -halt-on-error -jobname="$job" \
			"${NOFIGSDEF}\\def\\iskey{${iskey}}\\input{${SRC}}" >/dev/null
	done
	echo "wrote ${job}.pdf"
}

build 1 KEY
build 0 blank

# Publish the student copy to the site. book/extras/ is copied to the built
# site root (html_extra_path), and the CI only runs jupyter-book (never
# LaTeX), so the committed PDF under extras/labs/ IS what the site serves.
DEST="../book/extras/labs"
mkdir -p "$DEST"
cp -f "ECE444_Lab_${SLUG}_blank.pdf" "$DEST/"
echo "published -> $DEST/ECE444_Lab_${SLUG}_blank.pdf"
echo "KEY left in latex/ (not published, not committed)."
echo "done."
