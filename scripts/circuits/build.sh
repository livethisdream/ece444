#!/usr/bin/env bash
# Compile every circuitikz .tex in this folder to a self-contained SVG
# (text -> paths via --no-fonts) in book/extras/viz/img/.
# Requires: a LaTeX distro with circuitikz (pdflatex) and dvisvgm.
set -e
cd "$(dirname "$0")"
OUT="../../book/extras/viz/img"
mkdir -p "$OUT"
for tex in *.tex; do
  [ -e "$tex" ] || continue
  base="${tex%.tex}"
  echo "compiling $tex ..."
  pdflatex -interaction=nonstopmode "$tex" >/dev/null 2>&1
  dvisvgm --pdf --no-fonts --output="$OUT/$base.svg" "$base.pdf" >/dev/null 2>&1
  echo "  -> $OUT/$base.svg"
done
rm -f ./*.aux ./*.log ./*.pdf
echo "done."
