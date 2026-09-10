# arXiv submission package

File: paper/union-closed-arxiv.tar.gz  (paper.tex + anc/ ancillary code, reports and Lean sources). Requires XeLaTeX (see Compilation below); packages amsmath/amssymb/amsthm/booktabs/microtype/hyperref/geometry plus fontspec/fancyvrb/newunicodechar for the Unicode Lean listings.

Revised: 2026-09-10. Changes from the 8 September text: one sentence added at the end of the abstract, one paragraph added in Section 1 after Theorem A, one sentence added to the Acknowledgements, the \date, and new Appendices B (description of the Lean formalisation) and C (its complete source). Sections 2-7 and Appendix A are untouched; theorem numbering (3.1, 3.2, 3.3, 3.4, 4.3, 5.3, 5.5, 5.6, 6.1, 6.2, 6.3, App. A) is unchanged. Package re-cut 2026-09-10 with the revised paper.tex and anc/lean/.

Ancillary files (anc/):

  kernel_game.py, kernel_sweep.py, floor_scan.py, big_restart.py, inertia_check.py,
  recert_evaluator.py                          -- evaluator, searches, the decisive runs
  INERTIA.md, LEMMA_SMALL_ENTROPY.md, RECERT.md, ROBUSTNESS_ideal.md
                                               -- reports quoted in the paper
  lean/README.md, lean/SPEC.md, lean/CERTIFICATE.md, lean/check.sh,
  lean/lakefile.toml, lean/lean-toolchain, lean/lake-manifest.json,
  lean/AxiomCheck.lean, lean/UnionClosedCeiling.lean,
  lean/UnionClosedCeiling/{Entropy,Framework,Ceiling,Refined,Classes}.lean
                                               -- the Lean 4 / Mathlib formalisation of
                                                  Theorems 3.1 and 3.4 and part of Lemma 3.3
                                                  (Lean 4.23.0, Mathlib v4.23.0; no sorry;
                                                  axioms propext, Classical.choice, Quot.sound)

Title: The ceiling of the single-letter entropy method for the union-closed sets conjecture, and a protocol that reaches it
Authors: Andrew Moffat
Primary: math.CO   Cross-list: cs.IT
MSC: 05D05 (primary); 94A17, 60E15
License: CC BY 4.0 (recommended)
Comments: 31 pages (13-page paper plus Appendices B-C reproducing the Lean formalisation), 2 tables. Code, logs, referee reports and independent re-certification at https://github.com/moffatstudio/union-closed-constant. A Lean 4 formalisation of Theorems 3.1 and 3.4 included as ancillary files (anc/lean/)
Abstract: (copy from the abstract environment in paper.tex)
Note for first-time math.CO submitters: arXiv may ask for an endorsement; the endorsement request page gives a code to send to any endorsed math.CO author.

Compilation: XeLaTeX only (Tectonic 0.17 used locally; pdfLaTeX cannot load fontspec). OPEN ITEM before submitting: confirm that arXiv's AutoTeX accepts a XeLaTeX source for this submission (its handling of XeLaTeX/LuaLaTeX has changed over time; the %!TEX magic comment is not honoured by AutoTeX). If it does not, produce a pdfLaTeX-compatible build of the appendices (inputenc + newunicodechar mappings for the 43 non-ASCII characters used, listings in a Type-1 monospace font) before uploading. The source loads fontspec, fancyvrb and newunicodechar for the Unicode Lean listings in Appendices B-C; the listing font is DejaVu Sans Mono when available (TeX Live), else Consolas with Cambria Math for the 14 glyphs Consolas lacks. Magic comment `%!TEX TS-program = xelatex` is at the top of paper.tex. Body text is fontspec's default Latin Modern.
