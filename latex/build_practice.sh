#!/usr/bin/env bash
# Build an ECE 444 lesson practice set as two PDFs: the SOLUTIONS copy (red
# worked solutions) and the blank student copy (work space reserved).
#
#   ./build_practice.sh [LESSON]        # LESSON defaults to 03
#
# Content lives in ECE444_Practice_L<LESSON>.tex; the harness is
# ECE444_Practice_main.tex. Runs pdflatex twice per version for \numpages.
set -euo pipefail
cd "$(dirname "$0")"
LES="${1:-03}"

build() {                       # build <iskey:0|1> <suffix>
	local iskey="$1" suffix="$2"
	local job="ECE444_L${LES}_Practice_${suffix}"
	for _ in 1 2; do
		pdflatex -interaction=nonstopmode -halt-on-error -jobname="$job" \
			"\\def\\lessonNumIn{${LES}}\\def\\iskey{${iskey}}\\input{ECE444_Practice_main}" >/dev/null
	done
	echo "wrote ${job}.pdf"
}

build 1 SOLUTIONS
build 0 blank

# Publish the PDFs to the site. book/extras/ is copied to the built site root
# (html_extra_path), and the CI only runs jupyter-book (never LaTeX), so the
# committed PDF under extras/practice/ IS what the site serves.
DEST="../book/extras/practice"
mkdir -p "$DEST"
cp -f "ECE444_L${LES}_Practice_SOLUTIONS.pdf" "ECE444_L${LES}_Practice_blank.pdf" "$DEST/"
echo "published -> $DEST/ECE444_L${LES}_Practice_{blank,SOLUTIONS}.pdf"
echo "done."
