#!/usr/bin/env bash
# Build an ECE 444 module assessment as two PDFs: the KEY (red solutions and
# filled answer boxes) and the blank student copy.
#
#   ./build_assessment.sh [MODULE]      # MODULE defaults to 01
#
# The shared macros (myPackages_gr, myShortcuts, exam_config) must be on the
# TeX input path. On this machine they resolve automatically from
#   ...\Tools\LaTeX\latex-tools\tex\latex\
#
# pdflatex runs twice per version so the exam class's "page N of M" count and
# \numpages resolve. Build artifacts (*.aux, *.log, ...) are left in place and
# are gitignored.
set -euo pipefail
cd "$(dirname "$0")"
MOD="${1:-01}"

build() {                       # build <iskey:0|1> <suffix>
	local iskey="$1" suffix="$2"
	local job="ECE444_M${MOD}_Assessment_${suffix}"
	for _ in 1 2; do
		pdflatex -interaction=nonstopmode -halt-on-error -jobname="$job" \
			"\\def\\moduleNumIn{${MOD}}\\def\\iskey{${iskey}}\\input{ECE444_Assessment_main}" >/dev/null
	done
	echo "wrote ${job}.pdf"
}

build 1 KEY
build 0 blank
echo "done."
