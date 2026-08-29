#!/usr/bin/env bash
# Mechanical checks (REVIEW.md section A) for one lesson.
#
#   scripts/verify/mech_check.sh <NN> <slug>
#   e.g. scripts/verify/mech_check.sh 07 simple-resonant-antennas
#
# Everything here is scripted because it is decidable: files present, LaTeX
# compiles, every problem has a solution, decks and widgets render. Substance
# -- physics, derivations, difficulty -- is not checked here and never should
# be; that is the orchestrator's job (REVIEW.md section B).
#
# Requires the vendored render harness (cd scripts/verify && npm install) and,
# for the practice build, the private latex-tools macros:
#   TEXINPUTS=/workspace/latex-tools/tex/latex//:
#
# This gate is per-lesson. Two sweeps are site-wide and belong at the END of a
# batch, not here -- run them once when the batch is done:
#   scripts/verify/check_shell.py    every page, two widths
#   scripts/verify/check_bar.py      the HUD's geometry on both shells
set -u

if [ $# -lt 2 ]; then
  echo "usage: $0 <NN> <slug>   e.g. $0 07 simple-resonant-antennas" >&2
  exit 2
fi

NN="$1"; SLUG="$2"
HERE="$(cd "$(dirname "$0")" && pwd)"
REPO="$(cd "$HERE/../.." && pwd)"
LNN="L${NN}-${SLUG}"
: "${TEXINPUTS:=}"
export TEXINPUTS

fails=0
ok(){ echo "  PASS  $1"; }
bad(){ echo "  FAIL  $1"; fails=$((fails+1)); }

echo "== ${LNN} =="

# Locate the lesson page, and take the module number from where it actually
# lives rather than assuming a lesson-to-module mapping.
page="$(ls -d "$REPO"/book/module*/"$LNN"/index.md 2>/dev/null | head -1)"
if [ -z "$page" ]; then
  bad "lesson page not found under book/module*/$LNN/"
  echo "== ${LNN}: $fails failure(s) =="
  exit $fails
fi
MOD="$(basename "$(dirname "$(dirname "$page")")" | sed 's/^module0*//')"

# 1. files exist, page is not a stub
[ -s "$page" ] && ! grep -q "under construction" "$page" \
  && ok "lesson page non-stub (module $MOD)" || bad "lesson page missing/stub"
[ -s "$REPO/book/extras/slides/$LNN.md" ] && ok "deck md" || bad "deck md missing"
[ -s "$REPO/book/extras/slides/$LNN.html" ] && ok "deck html" || bad "deck html missing"
tex="$REPO/latex/ECE444_Practice_L$NN.tex"
[ -s "$tex" ] && ok "practice tex" || bad "practice tex missing"
b="$REPO/book/extras/practice/ECE444_L${NN}_Practice_blank.pdf"
s="$REPO/book/extras/practice/ECE444_L${NN}_Practice_SOLUTIONS.pdf"
[ -s "$b" ] && [ -s "$s" ] && ok "practice PDFs present" || bad "practice PDFs missing"

widgets="$(grep -oE 'viz/[a-z0-9-]+\.html' "$page" 2>/dev/null | sed 's|viz/||' | sort -u)"
for w in $widgets; do
  [ -s "$REPO/book/extras/viz/$w" ] && ok "widget $w exists" \
    || bad "widget $w referenced but missing"
done
[ -n "$widgets" ] && ok "page references $(echo "$widgets" | wc -w) widget(s)" \
  || bad "page references no interactive graphic"

# 2. practice compiles clean
if ( cd "$REPO" && bash latex/build_practice.sh "$NN" >"/tmp/mc_build_$NN.log" 2>&1 ); then
  ok "pdflatex builds"
else
  bad "pdflatex build failed (see /tmp/mc_build_$NN.log)"
fi
for L in "$REPO/latex/ECE444_L${NN}_Practice_SOLUTIONS.log" \
         "$REPO/latex/ECE444_L${NN}_Practice_blank.log"; do
  [ -f "$L" ] || continue
  over=$(grep -c "^Overfull" "$L")
  big=$(grep "^Overfull" "$L" | grep -oE '\(([0-9.]+)pt' | tr -d '(pt' | awk '$1>10' | wc -l)
  [ "$big" -eq 0 ] && ok "$(basename "$L"): no overfull >10pt (total: $over)" \
    || bad "$(basename "$L"): $big overfull boxes >10pt"
  grep -q "^!" "$L" && bad "$(basename "$L"): LaTeX errors" || true
done

# every \part has a solution
np=$(grep -c '\\part\b' "$tex" 2>/dev/null)
ns=$(grep -c '\\begin{solution}' "$tex" 2>/dev/null)
[ "$np" -gt 0 ] && [ "$np" -eq "$ns" ] && ok "parts=$np solutions=$ns" \
  || bad "parts=$np vs solutions=$ns"
pb=$(pdfinfo "$b" 2>/dev/null | awk '/^Pages/{print $2}')
ps=$(pdfinfo "$s" 2>/dev/null | awk '/^Pages/{print $2}')
[ -n "$ps" ] && [ "$ps" -ge "$pb" ] && ok "pages: blank=$pb solutions=$ps" \
  || bad "pagecount odd: blank=$pb sol=$ps"

# 3a. deck separators -- must run before the render check, because a dead
# separator merges two slides and then shows up as a bogus "slide too tall"
# rather than as what it is.
if sep=$(python3 "$HERE/check_separators.py" "$LNN" 2>&1); then
  ok "deck separators: all '---' live"
else
  bad "deck separators: $(echo "$sep" | grep -c 'line ') dead -- two slides are merged"
  echo "$sep" | grep '  line ' | sed 's/^/        /'
fi

# 3b. deck render
if python3 "$HERE/check_deck.py" "$LNN" >"/tmp/mc_deck_$NN.log" 2>&1; then
  ok "deck render: $(grep -m1 -E '^[A-Za-z0-9._-]+: [0-9]+ slides' "/tmp/mc_deck_$NN.log")"
else
  bad "deck render (see /tmp/mc_deck_$NN.log)"
fi

# 3c. frame budget -- only for a lesson that has opted into the frame view.
# A frame taller than the viewport is the deck's "slide too tall" defect in a
# new place: the build is happy and the bottom of the frame is simply gone when
# you present it. It has shipped that way before, so it is a gate, not a sweep.
if grep -qE '^frame_view:' "$page"; then
  if fr=$(python3 "$HERE/check_frames.py" "$LNN" 2>&1); then
    ok "frame budget: $(echo "$fr" | head -1)"
  else
    bad "frames over budget"
    echo "$fr" | sed 's/^/        /'
  fi
else
  ok "not a frame page (no frame_view in front matter)"
fi

# 4. widget render, height, overflow, aspect
for w in $widgets; do
  if python3 "$HERE/check_widget.py" "$REPO/book/extras/viz/$w" \
       >"/tmp/mc_w_${NN}_$w.log" 2>&1; then
    ok "widget $w: $(grep -m1 'worst-case height' "/tmp/mc_w_${NN}_$w.log")"
  else
    bad "widget $w (see /tmp/mc_w_${NN}_$w.log)"
  fi
done

# 5. greps for the gotchas that ship silently
files="$page $REPO/book/extras/slides/$LNN.md $tex"
grep -lP '\x{2009}' $files 2>/dev/null | grep -q . \
  && bad "U+2009 thin space found" || ok "no thin spaces"
grep -nE '\\[,;]' "$REPO/book/extras/slides/$LNN.md" 2>/dev/null \
  | grep -v '\\lbrace\|\\rbrace' | head -3 | grep -q . \
  && bad "deck has \\, or \; in math" || ok "deck free of \\, \;"
if python3 "$HERE/check_tables.py" "$page" "$REPO/book/extras/slides/$LNN.md"; then
  ok "no | inside table math"
else
  bad "raw | inside \$..\$ splits a table cell (use \\vert)"
fi
grep -q 'lo-list lo-sublist' "$page" && grep -q -- "--module: '$MOD'" "$page" \
  && ok "LO markup sublist + module $MOD" || bad "LO markup wrong for module $MOD"
grep -q "Learning Objective $MOD\." "$tex" && ok "practice LO banner" \
  || bad "practice LO banner missing (expected 'Learning Objective $MOD.x')"

# 6. voice self-check (VOICE.md) -- self-praise words, never in course prose
if grep -nEi '\b(honest|genuinely|rigorous|no hand-waving|is the price)\b' \
     "$page" "$REPO/book/extras/slides/$LNN.md" 2>/dev/null | head -5 | grep -q .; then
  bad "VOICE.md: self-vouching wording found"
  grep -nEi '\b(honest|genuinely|rigorous|no hand-waving|is the price)\b' \
    "$page" "$REPO/book/extras/slides/$LNN.md" 2>/dev/null | head -5 | sed 's/^/          /'
else
  ok "VOICE.md: no self-vouching wording"
fi

# 7. practice links only once the PDFs exist
if grep -q "Practice_blank.pdf" "$page"; then
  [ -s "$b" ] && ok "practice linked and built" || bad "practice linked but PDFs missing"
else
  bad "lesson page missing Practice links"
fi

echo "== ${LNN}: $fails failure(s) =="
exit $fails
