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
echo "done."
