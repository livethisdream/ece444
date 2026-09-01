#!/bin/bash
# SessionStart hook — set up a Claude Code on the web container to build this repo.
#
# Two things get built here, and neither works out of the box:
#
#   1. the Jupyter Book        jupyter-book build book/ --all
#   2. the practice PDFs       TEXINPUTS=... bash latex/build_practice.sh <NN>
#
# CI only ever does (1), so requirements.txt alone is not enough for (2) — the
# house LaTeX preamble (myPackages_gr) pulls ~60 packages. This installs both
# toolchains. Local machines are left alone; see the CLAUDE_CODE_REMOTE guard.
set -euo pipefail

# Web sessions only. On a laptop the toolchain is already whatever the developer
# wants it to be, and apt-get here would be rude.
if [ "${CLAUDE_CODE_REMOTE:-}" != "true" ]; then
  exit 0
fi

# Async: the session starts immediately and this runs behind it. Chosen because
# a cold container spends a few minutes on the ~1.5 GB TeX install, and that cost
# lands on every parallel session in a multi-lesson fan-out. The race it opens is
# benign for how this repo is actually worked: lesson authoring happens first and
# LaTeX is not touched until the practice set at the end, by which time this is
# long finished. If a session ever does need pdflatex in its first minute, just
# wait for it — or drop this line to go back to synchronous.
echo '{"async": true, "asyncTimeout": 600000}'

SUDO=""
[ "$(id -u)" -ne 0 ] && SUDO="sudo"

log() { printf '[session-start] %s\n' "$*"; }

# --- Python: the book toolchain (same as .github/workflows/deploy.yml) -------
if python3 -c 'import jupyter_book' 2>/dev/null; then
  log "jupyter-book present, skipping pip install"
else
  log "installing Python deps from requirements.txt"
  pip install --quiet --disable-pip-version-check -r "$CLAUDE_PROJECT_DIR/requirements.txt"
fi

# --- LaTeX: the practice/assessment toolchain -------------------------------
# asymptote is the one package the preamble needs that no texlive-* metapackage
# carries. coloremoji and slashbox are also referenced but unavailable on Debian
# and unused by any ECE 444 source, so they are not installed and not missed.
TEX_PKGS=(
  texlive-latex-recommended
  texlive-latex-extra
  texlive-pictures
  texlive-fonts-recommended
  texlive-fonts-extra
  texlive-science
  texlive-plain-generic
  texlive-bibtex-extra
  texlive-lang-greek
  texlive-luatex
  asymptote
  poppler-utils
)

# texlive-luatex is load-bearing, not optional: the body font is Barlow, loaded
# as OpenType through fontspec, so the practice sets and labs build with
# lualatex. Without this package luaotfload is missing and lualatex dies with
# "module 'luaotfload-main' not found" -- which reads like a font problem and is
# actually a missing apt package. Hence the probe below tests for it directly:
# a container provisioned before this change has pdflatex and asymptote and
# would otherwise be waved through.
if command -v lualatex >/dev/null 2>&1 \
   && kpsewhich asymptote.sty >/dev/null 2>&1 \
   && kpsewhich -format=lua luaotfload-main.lua >/dev/null 2>&1; then
  log "TeX Live present, skipping apt install"
else
  log "installing TeX Live (~1.5 GB, a few minutes on a cold container)"
  export DEBIAN_FRONTEND=noninteractive
  $SUDO apt-get update -qq
  $SUDO apt-get install -y -qq --no-install-recommends "${TEX_PKGS[@]}"
fi

# --- where the house macros live --------------------------------------------
# myPackages_gr / myShortcuts / exam_config live in the PRIVATE livethisdream/
# latex-tools repo, which is not vendored here and cannot be cloned by a hook.
# Attach it in-session:
#
#     add_repo(owner="livethisdream", repo="latex-tools")
#
# It is NOT always /workspace. An attach lands the clone beside this repo, under
# whatever base directory the session was given -- /home/user/latex-tools on a
# web session, /workspace/latex-tools elsewhere. Hard-coding /workspace is how
# this silently failed for a whole run: the repo was attached and present, the
# macros were on disk, and every practice build still fell back to "file
# myPackages_gr.sty not found" because TEXINPUTS pointed at a path that did not
# exist. So list every candidate instead of guessing one. TEXINPUTS is a search
# path and kpathsea skips entries that are not there, which also means this
# stays correct when the clone lands after the hook has run.
if [ -n "${CLAUDE_ENV_FILE:-}" ]; then
  TT_ROOTS="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && dirname "$(pwd)")/latex-tools /home/user/latex-tools /workspace/latex-tools"
  TT_PATH=""
  for r in $TT_ROOTS; do
    case ":$TT_PATH" in *":$r/tex/latex//:"*) continue;; esac
    TT_PATH="$TT_PATH$r/tex/latex//:"
  done
  echo "export TEXINPUTS=$TT_PATH" >> "$CLAUDE_ENV_FILE"
  log "TEXINPUTS exported: $TT_PATH"
fi

log "ready: jupyter-book $(python3 -c 'import jupyter_book;print(jupyter_book.__version__)' 2>/dev/null || echo '?'), $(pdflatex --version 2>/dev/null | head -1 || echo 'no pdflatex')"
