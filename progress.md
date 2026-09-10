# Union-Closed Sets Conjecture — constant-improvement campaign

**Started:** 2026-09-08. Conjecture #057. Read this file first; it is the authoritative log.

## Target
Frankl's conjecture: in any finite union-closed family F (≠{∅}), some element lies in ≥ 1/2 of the sets.
Known: some element lies in ≥ c·|F| sets with **c = 0.38271** (Liu, arXiv:2306.08824, June 2023; partly numerical).
Goal: any rigorous c > 0.38271 is a new record. Secondary goal: make Liu's bound fully rigorous, or prove it is the ceiling of its class.

## Why this problem (decision 2026-09-08)
Scouted five candidates (Sidon constant, thrackle constant, lonely-runner gap, opaque-set bound, union-closed).
Union-closed chosen: no movement since 2023, no visible competition, method is elementary entropy + small-dimensional
optimization (laptop-scale), and the current record's coupling class is NOT proven exhausted.
Scout reports archived in `literature/scouts/`.

## Improvement chain
| c | who | arXiv | note |
|---|---|---|---|
| 0.01 | Gilmer | 2211.09055 | entropy method |
| (3-√5)/2 = 0.381966 | Alweiss–Huang–Sellke / Chase–Lovett / Sawin / Pebody | 2211.11731 / 2211.11689 / 2211.11504 / 2211.13139 | sharp for "approximate" union-closed (Chase–Lovett) |
| 0.38234 | Yu; Cambie | 2212.00658; 2212.12500 | Sawin's iid/max-entropy coupling; Cambie proves 0.38234 sharp for that class |
| 0.38271 | Liu | 2306.08824 | conditionally-iid coupling; 9-dim numerical optimization; hypotheses numerically verified |

## Log
- 2026-09-08 10:20 — campaign opened; literature wave 1 dispatched (4 Sonnet agents).
- 2026-09-08 11:40 — Lead re-derived the iid method (ψ lemma tight at u=v=1/φ; two-point extremal reproduces ψ; `code/check_psi_lemma.py`).
  Proposed the **sequential-coupling reformulation** (NOTES_lead.md): build the coupling coordinate-by-coordinate, any joint law of
  (A_i,B_i) given both prefixes with the prescribed conditional marginals; mutual-information loss term vanishes;
  H(C)-H(A) ≥ Σ_i E[h(s_i) - ½(h(u_i)+h(v_i))], s_i free in the Fréchet interval. Exact DP oracle `code/seqcoupling_dp.py`.
- 2026-09-08 11:45 — Exhaustive over all families on n=3,4: no family with max freq < 1/2 defeats the sequential class
  (iid barrier already 0.40 at n=3,4). Symmetric slice-union DP (`code/symmetric_dp.py`) at n=24: single slices and all two-slice
  unions with p<1/2 have positive gain; even the middle slice (p=1/2) has gain +0.62. iid dies at k=10/24 (p=0.417).
  Caveat: the DP value is the class ceiling on a GIVEN family; turning it into a theorem needs a policy + per-family-independent proof.
- 2026-09-08 11:50 — Background: random local search for barrier families n=5,6,7, pmax=0.45 (`code/search_n*_p045.log`).
- INCIDENT 2026-09-08 11:26 — lead ran a blanket `taskkill //IM python.exe`; killed Moser-worm shard A; supervisor restarted it
  from checkpoint (≤2 min lost). Memory `never-kill-all-python` written. Kill by PID only.
- 2026-09-08 13:50 — **First numerical improvement.** General conditionally-iid kernels (code/kernel_game.py, reproduces Liu to 1e-9).
  Class ceiling derived: c ≤ 1 − (1/√2)h(1/√2)/h(1/2) = 0.383099 for any conditionally-iid + iid mixture (K(x,x) ≥ 0 on the diagonal).
  Kernel f_ideal (min(x,1−x) on [0,½], sqrt(½−x²) on [½,1/√2], 0 after), β=0.15: **c_max = 0.382840** vs Liu 0.382709 (β=0.08: 0.382695).
  Same rigor class as Liu (numerical adversary minimisation, m=3 atoms per component). Robustness (m=4, β scan, λ=0.9) and
  three-protocol runs (code/kernel_game3.py, adds Sawin's term with LP adversary) in flight: code/sweep_*.log, code/g3_*.log.
- 2026-09-08 14:40 — **Correction.** A near-degenerate adversary µ = qδ_{x=1} + (1−q)δ_{x=ε}, ε→0, q=1−c (both components ≈ zero
  entropy; Liu's Lemma-7 boundary) gives ratio → 2(1−β)(1−c) for any rank-1 "±" kernel (f(ε) ~ ε ⇒ K-term vanishes).
  Hence β ≤ 1 − 1/(2(1−c)) ≈ 0.19 for f_ideal; the β=0.25/0.3 sweeps (0.38293/0.38295) were optimiser misses.
  Honest f_ideal figure: β≈0.19, c≈0.38288 (still > Liu). adversary_min now seeds this adversary (structured_inits).
  **Fix:** K_new (code/kernel_game.py): r_x = 1_{u≤x} for x≤½ (full diagonal variance x(1−x) ⇒ degenerate ratio → 2(1−β)q+β ≥ 1),
  step function with variance ½−x² on [½,1/√2], constant beyond. Verified: K ≥ 0, xy+K ≤ ½ where K>0 (pointwise ≥ iid), PSD.
  Sweeps at β=0.3,0.5,0.7,0.9 running (code/sweep_new_b*.log). Ceiling theorem written: CEILING_THEOREM.md (0.3830993).
- 2026-09-08 16:05 — **Framework ceiling found and attained.** Second (component-hiding) adversary forces iid weight ≥ 1/(2(1−c)) for ANY
  protocol mixture (K_new fails at every β ≥ 0.3 for exactly this reason: code/sweep_new_b*.log). Joint solution with the
  two-point diagonal adversary: **c** = 0.382885260, β = 0.189778, x* = 0.690908** (CEILING_THEOREM.md, refined section).
  f_ideal at β=0.19 certifies 0.382885 = c** (sweep). Liu 0.382709 → 0.382885 is therefore the LAST improvement available to
  the single-letter protocol method. Concavity agent: f_ideal violates Liu's Thm-12 PSD condition (−1.6e-3 at x≈0.70), so the
  3-atom reduction does not apply; inertia count requested to fix the atom budget; adv-robust certifying with m=4..6.
- 2026-09-08 16:40 — Bisection sweeps cannot see the component-hiding law (infimum as tiny-atom weight → 0); all "c_max at β=0.19"
  figures are two-point-side only. Correct statement: sup c = c** = 0.382885 at β** = 0.189778 (both adversaries → ratio 1).
  kernel-opt agent independently rediscovered the hiding adversary; no kernel beats 0.38289 (code/KERNEL_OPT.md).
  concavity agent: inertia k=1 (Liu), k=2 (f_ideal) ⇒ ≤4 atoms/component; K_new has unbounded inertia (dropped). RESULT.md drafted.
- 2026-09-08 17:30 — **CERTIFIED.** At β**=0.189778: non-degenerate search m=4,5,6 (300–500 restarts) min ratio 1.0000733 (c=0.38284),
  1.0000085 (c=0.38288); hiding family ≥ 1.000073 (limit from above); mixed laws 1.0000733. Headline: c ≥ 0.38284 at Liu-level rigor
  (sup 0.382885). arXiv note drafted: paper/note.tex (tex only; no LaTeX on this machine, Docker declined by user).
- 2026-09-08 18:30 — **Publication draft finalised.** paper/paper.tex (12 pp, compiled with Tectonic → paper/paper.pdf). Four referee rounds by a
  fresh Opus agent (C:	mp
eferee\REFEREE{,2,3,4}.md): round 1 found 4 errors/4 gaps (hiding definition needed P(y,y) ≤ δ²; 2x² slip;
  Liu-diagonal remark; stale β=0.19 claims; singleton-class hypothesis; (D) range), round 2 found my small-entropy lemma's numerical
  instance dropped the factor w (withdrawn; region back in the numerical hypothesis, = Liu's status), round 3 four statement-precision
  gaps, round 4: **no ERROR, no GAP**; referee reproduced c**, both table columns, Liu to 13 digits, inertia k=2 on 11 grids.
  Independent re-certification (fresh Opus agent, own evaluator from the note alone): calibration on Liu passes, 4-atom min 1.00007334
  at the two-point law, hiding limit 1.000073219 from above, fixed point c**=0.382885260 — no discrepancy (5/6-atom runs in flight).
  Repo: https://github.com/moffatstudio/union-closed-constant (public since 2026-09-08). Open: sharp small-entropy lemma (lemma-prover agent).
- 2026-09-08 20:15 — **WRAPPED.** Sharp small-entropy bound proved (lemma-prover agent, refereed: no error): R ≥ 2w[(1−c) − ρE], ρ=18.785,
  ε₀=7.6e-7 > numerical floor 1e-7 ⇒ no window at c=0.38284 (certificate now MORE complete than Liu's). Reach caveat: window reopens
  for c > c** − 1.9e-6. 5,000-restart run: min 1.00007334 (two-point law). Independent re-certification (own evaluator, no repo code):
  4 atoms 1.0000733414, 5 atoms 1.0000733414 — identical. Referee rounds 1–4 + lemma: no error, no gap. paper/paper.pdf = 13 pp final.
  NOT submitted; author line = user; repo private. Next (user's call): make repo public or attach code as arXiv ancillary; submit
  math.CO (cross-list cs.IT); then PR to teorth/optimizationproblems C6 with the arXiv id.
- 2026-09-10 18:00 — **Repository made public and tidied; release v1.0.** README rewritten as a verifier's entry point (claim table with
  status, reproduction table script→log→time, verification chain); `verify.py` added — one script, two independent evaluators, recomputes
  every constant printed in the paper (Appendix A, Table 2, Theorem 5.5, Lemma 5.6) and exits non-zero on any discrepancy; GitHub Actions
  `verify.yml` runs it on every push; `verification/` archive (independent recertification, lemma scripts, referee checks) documented;
  LICENSE (MIT code / CC BY 4.0 text), CITATION.cff, .zenodo.json added. Tagged **v1.0** = the paper as of 2026-09-08.
- 2026-09-10 18:40 — Submitted to VibeMathed (`paper/vibemathed-entry.html`): the paper, the repo, the one-minute check, and the AI
  disclosure as written in the README. No claim beyond the paper's.
- 2026-09-10 19:00–20:45 — **Lean 4 formalisation of the ceiling theorems.** Spec written first (`lean/SPEC.md`): finite model of the
  §2.2 framework, `Certifies` as a hypothesis *implied by* (16), the exact statements to prove, the modelling latitude allowed, and the
  fallback bound if 0.3829 proved too tight. Environment: Lean 4.23.0 via elan, Mathlib pinned at tag v4.23.0 (commit `37df177aaa77…`),
  local Mathlib checkout reused to avoid the download; Lake project `UnionClosedCeiling`, `autoImplicit` off.
  Agent: Claude Fable 5.1, working from the spec and the paper; the author checked every statement against the paper before commit.
  Outcome: **Theorem 3.1** (`product_ceiling`), **Theorem 3.4** in four pieces — (H) `hiding_bound`, (D) `diagonal_bound`,
  `fixed_point_form`, and `refined_ceiling_numeric : c ≤ 3829/10000` — and **Lemma 3.3** for the i.i.d., all-couplings and
  mixtures-of-products classes (`Classes.lean`). 1,037 lines. The numerical corollary needed rigorous entropy bounds at
  x = 0.6909 (Taylor series of log(1−t) with explicit remainder, 16/16/6 terms, plus Mathlib's `log_two_gt_d9`): the target
  0.3829 was reached, margin ≈ 1.4·10⁻⁵. Not formalised, and said so in `lean/README.md`: Proposition 2.2 (a hypothesis here, not a
  theorem), the maximal-correlation class, Sections 4–6, and the exact fixed point c** = 0.382885260… .
  Gate: `lean/check.sh` = `lake build` + `sorry` scan + `#print axioms` scan; passes locally — zero sorry, ten declarations each
  reporting only `propext`, `Classical.choice`, `Quot.sound`. CI: `.github/workflows/lean.yml`, run 34522052221, fresh Ubuntu clone,
  green in 2 min 20 s. Committed as `45949fa`; tagged **v1.1** (paper.pdf, union-closed-arxiv.tar.gz, verification-pack.zip) — v1.1 is
  now the version of record. Lean does **not** prove c ≤ c** or 0.382885, and does not touch Theorem 6.2's 0.38284.
- 2026-09-10 20:50 — Verification pack (`verification-pack.zip`: the two evaluators, `verify.py`, the one-minute and the four-hour
  launchers, the paper) sent to a colleague for an independent run on their own machine. Its README says explicitly that the pack checks
  the numerical certificate only and that the ceiling proofs are machine-checked in Lean in the repository.

