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
  Repo: https://github.com/moffatstudio/union-closed-constant (private). Open: sharp small-entropy lemma (lemma-prover agent).
- 2026-09-08 20:15 — **WRAPPED.** Sharp small-entropy bound proved (lemma-prover agent, refereed: no error): R ≥ 2w[(1−c) − ρE], ρ=18.785,
  ε₀=7.6e-7 > numerical floor 1e-7 ⇒ no window at c=0.38284 (certificate now MORE complete than Liu's). Reach caveat: window reopens
  for c > c** − 1.9e-6. 5,000-restart run: min 1.00007334 (two-point law). Independent re-certification (own evaluator, no repo code):
  4 atoms 1.0000733414, 5 atoms 1.0000733414 — identical. Referee rounds 1–4 + lemma: no error, no gap. paper/paper.pdf = 13 pp final.
  NOT submitted; author line = user; repo private. Next (user's call): make repo public or attach code as arXiv ancillary; submit
  math.CO (cross-list cs.IT); then PR to teorth/optimizationproblems C6 with the arXiv id.
