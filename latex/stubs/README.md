# Stand-in macros — syntax checking only, **never** for shipping PDFs

`stub_macros.tex` re-implements just enough of the house macro library
(`myPackages_gr`, `myShortcuts`, `exam_config` — which live in
`.../Tools/LaTeX/latex-tools`, outside every project bind) to let a practice or
assessment source **compile** where that library is not mounted: CI, a container,
someone else's laptop.

Use it to catch macro-arity mistakes, math-mode errors, broken `minipage`/`parts`
nesting, overfull lines, and solutions that outgrow their reserved space:

```sh
cd latex && cp ECE444_Practice_main.tex /tmp/harness.tex
# repoint the three \input lines at stubs/stub_macros, then:
pdflatex -interaction=nonstopmode -jobname=CHECK \
  "\def\lessonNumIn{06}\def\iskey{1}\input{/tmp/harness}"
```

## What it is not

It is **not** a faithful reproduction of the real macros, and a PDF built with it
must not be committed to `book/extras/practice/`. Rebuilding the L04 set with
these stubs and overlaying it on the committed L04 PDF (built with the real
library) shows 2–4% of pixels differing on every page: page geometry, fonts,
margins, and the header all land exactly, but the unit macros' spacing and the
`\ansbox` metrics differ, and the error accumulates into visibly different
vertical placement further down each page. Two sets built different ways would
not sit comfortably next to each other in front of students.

Shipping PDFs still come from `./build_practice.sh <NN>` against the real
`latex-tools`.
