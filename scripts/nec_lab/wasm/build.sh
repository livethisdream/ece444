#!/usr/bin/env bash
# Build NEC-2 as WebAssembly.
#
# This is the spike that answered "can the simulator live on GitHub Pages?".
# It can: nec2c is plain C with file I/O, which is exactly what Emscripten
# handles, and the module it produces gives answers identical to the native
# binary -- verified on three decks, below.
#
#   bash scripts/nec_lab/wasm/build.sh /some/work/dir
#
# Leaves nec2.js + nec2.wasm (about 64 KB and 255 KB) in <work>/out.
#
# ONE TRAP, AND IT COST AN HOUR: do not use the Emscripten that apt installs.
# Ubuntu 24.04 ships 3.1.6 with a frozen cache; it compiles these sources
# without complaint and links a module of 8 KB -- the C code simply is not in
# it -- which then aborts with "FS error" in node and in the browser alike.
# The native build of the same sources is 296 KB. Use emsdk, as below.
set -euo pipefail

WORK="${1:-$PWD/wasm-build}"
mkdir -p "$WORK" && cd "$WORK"

[ -d emsdk ] || git clone --depth 1 https://github.com/emscripten-core/emsdk.git
(cd emsdk && ./emsdk install 3.1.61 && ./emsdk activate 3.1.61)
# shellcheck disable=SC1091
source emsdk/emsdk_env.sh

[ -d nec2c-src ] || git clone --depth 1 https://github.com/KJ7LNW/nec2c.git nec2c-src

cd nec2c-src
# The repo carries both the modern split sources and a legacy monolithic
# nec2c.c that no longer compiles beside them. Take the list the real build
# uses rather than *.c.
SRC="$(sed -n '/nec2c_SOURCES/,/^$/p' Makefile.am | grep -oE '[a-z0-9_]+\.c' | tr '\n' ' ')"

mkdir -p "$WORK/out"
emcc $SRC -O2 \
  -DPACKAGE_STRING='"nec2c (wasm)"' -DPACKAGE_VERSION='"1.3"' \
  -o "$WORK/out/nec2.js" \
  -sMODULARIZE -sEXPORT_NAME=createNec2 -sEXIT_RUNTIME=0 -sINVOKE_RUN=0 \
  -sALLOW_MEMORY_GROWTH -sFORCE_FILESYSTEM \
  -sEXPORTED_RUNTIME_METHODS=FS,callMain

echo
echo "built: $WORK/out/nec2.js + nec2.wasm"
echo "use it like this, from a page:"
cat <<'JS'
    const M = await createNec2();
    M.FS.writeFile('/in.nec', deckText);
    M.callMain(['-i/in.nec', '-o/out.txt']);
    const out = M.FS.readFile('/out.txt', { encoding: 'utf8' });
JS
