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
  asymptote
  poppler-utils
)

if command -v pdflatex >/dev/null 2>&1 && kpsewhich asymptote.sty >/dev/null 2>&1; then
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
# Attach it in-session, which clones it to /workspace/latex-tools:
#
#     add_repo(owner="livethisdream", repo="latex-tools")
#     git clone --depth 1 https://github.com/livethisdream/latex-tools /workspace/latex-tools
#
# Exporting TEXINPUTS now — pointing at a directory that does not exist yet is
# harmless, and it means build_practice.sh just works the moment the clone lands,
# with no second step to remember.
if [ -n "${CLAUDE_ENV_FILE:-}" ]; then
  echo 'export TEXINPUTS=/workspace/latex-tools/tex/latex//:' >> "$CLAUDE_ENV_FILE"
  log "TEXINPUTS exported for /workspace/latex-tools"
fi

log "ready: jupyter-book $(python3 -c 'import jupyter_book;print(jupyter_book.__version__)' 2>/dev/null || echo '?'), $(pdflatex --version 2>/dev/null | head -1 || echo 'no pdflatex')"
