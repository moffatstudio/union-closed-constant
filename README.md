# The ceiling of the single-letter entropy method for the union-closed sets conjecture, and a protocol that reaches it

[![verify](https://github.com/moffatstudio/union-closed-constant/actions/workflows/verify.yml/badge.svg)](https://github.com/moffatstudio/union-closed-constant/actions/workflows/verify.yml) [![lean](https://github.com/moffatstudio/union-closed-constant/actions/workflows/lean.yml/badge.svg)](https://github.com/moffatstudio/union-closed-constant/actions/workflows/lean.yml)

Andrew Moffat, 8 September 2026. Paper: [`paper/paper.pdf`](paper/paper.pdf) (13 pp + appendices; source [`paper/paper.tex`](paper/paper.tex); Appendix B describes the Lean formalisation and Appendix C reproduces its source). Preprint, not peer-reviewed. Intended for math.CO (cross-list cs.IT); MSC 05D05, 94A17, 60E15. Not yet on arXiv (endorsement pending); the release [`v1.2`](https://github.com/moffatstudio/union-closed-constant/releases/tag/v1.2) is the version of record (v1.0 = paper of 8 September; v1.1 = Lean formalisation; v1.2 = revised paper with Appendices B–C, certificate, ancillary Lean files), and a Zenodo DOI will be added here when minted.

This repository holds everything needed to check the paper: the code, the raw logs of every run quoted in it, the reports of four referee rounds, an independent re-implementation of the certificate, and the campaign log. Nothing was removed to tidy the story; withdrawn intermediate claims are marked as such where they occur.

## Check it in one minute

```
pip install -r requirements.txt
python verify.py --search
```

`verify.py` recomputes every constant printed in the paper (Appendix A, Table 2, Theorem 5.5) with **two independent evaluators** — the paper's `code/kernel_game.py` and `verification/independent-recertification/evaluator.py`, written from the manuscript alone — and compares each to the printed value: $c_{\mathrm{ceil}}$, $c^{**}$, $w^{**}$, $x^{**}$; calibration on Liu's published optimum to nine digits; the two-point minimum $1.0000733$ at $c = 0.38284$ and $1.0000085$ at $0.38288$; the hiding family's closed form and its limit $2w(1-c)$; $\rho$, $\varepsilon_0$, the Lemma 5.6 bound, the corner ratio $0.9909$ and (F2); agreement of the two evaluators to $10^{-10}$ on random laws; and, with `--search`, a short 4-atom optimiser run that lands on the same minimiser. It exits non-zero on any discrepancy. The same script runs in CI on every push (badge above). The long computations behind Hypothesis 6.1 (5,000 restarts; 5- and 6-atom laws; 97 minutes) are not repeated by `verify.py`; their logs and the scripts that produced them are listed below.

## Formal verification (Lean 4)

The two *unconditional* theorems of the paper are machine-checked. [`lean/`](lean/) is a Lake project (Lean 4.23.0, Mathlib v4.23.0) formalising Theorem 3.1, Theorem 3.4 and the elementary parts of Lemma 3.3 on a finite model of the single-letter framework of §2.2, written by a Claude (Anthropic) agent from [`lean/SPEC.md`](lean/SPEC.md), with every statement checked against the paper by the author. No `sorry`.

The five main statements, verbatim from the sources (hypothesis names as in the files; `h` is binary entropy in bits, `Prot k` a protocol, `w` its weight, `C k` its class, `Cc` the certificate constant, `Certifies` the paper's (cert) — which implies it):

```lean
-- Theorem 3.1, UnionClosedCeiling/Ceiling.lean
theorem product_ceiling {K : ℕ} {Prot : Fin K → ℝ → ℝ → ℝ} {w : Fin K → ℝ}
    {C : Fin K → ∀ n : ℕ, (Fin n → ℝ) → (Fin n → ℝ) → (Fin n → Fin n → ℝ) → Prop}
    {Cc c : ℝ}
    (hProt : ∀ k, IsProtocol (Prot k)) (hw : ∀ k, 0 ≤ w k) (hw1 : ∑ k, w k = 1)
    (hC : ∀ k, ContainsProduct (C k)) (hCc : 1 ≤ Cc)
    (hcert : Certifies Prot w C Cc c) :
    c ≤ 1 - h (1 / Real.sqrt 2) / Real.sqrt 2
```

```lean
-- Theorem 3.4, UnionClosedCeiling/Refined.lean
-- variable {K : ℕ} {Prot : Fin (K+1) → ℝ → ℝ → ℝ} {w : Fin (K+1) → ℝ}
--   {C : Fin (K+1) → ∀ n : ℕ, (Fin n → ℝ) → (Fin n → ℝ) → (Fin n → Fin n → ℝ) → Prop}
--   {Cc c : ℝ}

theorem hiding_bound                                                        -- (H)
    (hProt : ∀ k, IsProtocol (Prot k)) (hiid : ∀ x y, Prot 0 x y = x * y)
    (hw : ∀ k, 0 ≤ w k) (hw1 : ∑ k, w k = 1)
    (hC0 : ContainsProduct (C 0)) (hChide : ∀ k, k ≠ 0 → AdmitsHiding (C k))
    (hCc : 1 ≤ Cc) (hc0 : 0 < c) (hc1 : c < 1)
    (hcert : Certifies Prot w C Cc c) :
    1 ≤ 2 * w 0 * (1 - c)

theorem diagonal_bound                                                      -- (D)
    (hProt : ∀ k, IsProtocol (Prot k)) (hiid : ∀ x y, Prot 0 x y = x * y)
    (hw : ∀ k, 0 ≤ w k) (hw1 : ∑ k, w k = 1) (hC : ∀ k, ContainsProduct (C k))
    (hCc : 1 ≤ Cc) (hc1 : c < 1) (hcert : Certifies Prot w C Cc c)
    {x : ℝ} (hx : x ∈ Set.Ioc (0:ℝ) 1) (hcond : h x ≤ w 0 * h (x^2) + 1 - w 0) :
    c ≤ 1 - x * h x / (w 0 * h (x^2) + 1 - w 0)

theorem fixed_point_form                                                    -- (G)
    (hProt : ∀ k, IsProtocol (Prot k)) (hiid : ∀ x y, Prot 0 x y = x * y)
    (hw : ∀ k, 0 ≤ w k) (hw1 : ∑ k, w k = 1) (hC : ∀ k, ContainsProduct (C k))
    (hChide : ∀ k, k ≠ 0 → AdmitsHiding (C k))
    (hCc : 1 ≤ Cc) (hc0 : 0 < c) (hchalf : c ≤ 1/2) (hcert : Certifies Prot w C Cc c)
    {x : ℝ} (hx : x ∈ Set.Ioo (0:ℝ) 1) (hmono : h x ≤ h (x^2)) :
    c ≤ 1 - x * h x / (1 - (1 - h (x^2)) / (2 * (1 - c)))

theorem refined_ceiling_numeric
    (hProt : ∀ k, IsProtocol (Prot k)) (hiid : ∀ x y, Prot 0 x y = x * y)
    (hw : ∀ k, 0 ≤ w k) (hw1 : ∑ k, w k = 1) (hC : ∀ k, ContainsProduct (C k))
    (hChide : ∀ k, k ≠ 0 → AdmitsHiding (C k))
    (hCc : 1 ≤ Cc) (hc0 : 0 < c) (hchalf : c ≤ 1/2) (hcert : Certifies Prot w C Cc c) :
    c ≤ 3829/10000
```

Lemma 3.3 is `containsProduct_iidClass`, `containsProduct_allCouplings`, `containsProduct_mixtureOfProducts`, `admitsHiding_allCouplings`, `admitsHiding_mixtureOfProducts` in `lean/UnionClosedCeiling/Classes.lean` — the i.i.d., all-couplings and mixture-of-products classes; the maximal-correlation case is paper-only.

Axioms: all ten declarations above report

```
depends on axioms: [propext, Classical.choice, Quot.sound]
```

i.e. nothing beyond Lean's standard three.

**What is *not* formalised.** Proposition 2.2 (Gilmer's reduction from union-closed families to the certificate) is a *hypothesis* in the Lean development, not a theorem; the maximal-correlation classes of Lemma 3.3; Sections 4–6, including everything conditional (Theorem 6.2 and the constant $0.38284$); and the exact fixed point $c^{**} = 0.382885260\ldots$ — what Lean proves numerically is $c \le 0.3829$, which is already below $c_{\mathrm{ceil}} = 0.383099\ldots$, so the refined ceiling formally beats the product ceiling.

**Running the gate.** From a fresh clone (needs network for Mathlib and its `olean` cache):

```bash
cd lean
lake exe cache get
lake build
bash check.sh
```

`check.sh` exits `0` only if the build succeeds, no `sorry` occurs in the build output or the sources, and every one of the ten declarations depends on no axiom beyond `propext`, `Classical.choice`, `Quot.sound`. The same gate runs in GitHub Actions on every push to `master` touching `lean/` (badge above), from a fresh Ubuntu clone.

Details: [`lean/README.md`](lean/README.md) (statement-by-statement map and the modelling choices) and [`lean/CERTIFICATE.md`](lean/CERTIFICATE.md) (dated certificate: commit, toolchain, axiom output, file hashes, CI run). Appendix B of the paper describes the formalisation and Appendix C reproduces the source.

## What is claimed, and how firmly

| Claim | Where in the paper | Status |
|---|---|---|
| **Ceiling.** Every single-letter certificate whose classes contain product laws certifies at most $c_{\mathrm{ceil}} = 1 - h(1/\sqrt2)/\sqrt2 = 0.383099\ldots$ | Theorem 3.1 | **Proved**; **machine-checked in Lean 4 / Mathlib** — `lean/UnionClosedCeiling/Ceiling.lean`, `product_ceiling` |
| **Refined ceiling.** Every certificate using the i.i.d. protocol whose other classes admit *component hiding* certifies at most $c^{**} = 0.382885260\ldots$ | Theorem 3.4 | **Proved**; **machine-checked in Lean** — `hiding_bound` (H), `diagonal_bound` (D), `fixed_point_form`, and `refined_ceiling_numeric : c ≤ 0.3829` (`lean/UnionClosedCeiling/Refined.lean`) |
| All classes in Gilmer, AHS, Chase–Lovett, Sawin, Pebody, Yu, Cambie, Liu contain products and admit hiding | Lemma 3.3 | **Proved**; the i.i.d., all-couplings and mixtures-of-products cases machine-checked in Lean (`Classes.lean`); the maximal-correlation case is paper-only |
| **Small-entropy bound** $R \ge 2w[(1-c) - \rho E]$ | Theorem 5.5 | **Proved** (`code/LEMMA_SMALL_ENTROPY.md`, refereed in `code/REFEREE_LEMMA.md`) |
| **New constant:** every finite union-closed family $\ne\{\emptyset\}$ has an element in at least $0.38284\,\lvert\mathcal F\rvert$ members | Theorem 6.2 | **Computer-assisted, conditional** on Hypotheses 5.3 (inertia) and 6.1 (global minimum) — the same kind of hypotheses as Liu's record $0.382709$, with the small-entropy regime now covered unconditionally |
| Every $c < c^{**}$ is certified under the analogous hypothesis at each weight | Theorem 6.2, last sentence | Conditional, as above |

Frankl's conjecture ($c_0 = 1/2$) is **not** resolved by this work. The ceiling theorems show that the entropy method in every form used since 2022 cannot reach it.

## Reproducing the numbers in the paper

Environment: Python 3.12, `pip install -r requirements.txt` (numpy, scipy; mpmath for two referee scripts). All runs are single-process; times below are on a laptop.

| Number in paper | Script | Log / output | Time |
|---|---|---|---|
| $c_{\mathrm{ceil}}$, $c^{**}$, $w^{**}$, $x^{**}$ (Appendix A) | `verification/independent-recertification/closed.py` | prints `c** = 0.382885260 x*=0.6909077 w=0.810222` | seconds |
| Evaluator reproduces Liu's optimum to nine digits (§6) | `code/liu_reproduce.py` | stdout; also `verification/independent-recertification/calib.py` | minutes |
| Inertia $k=2$ for $\Pi^{\mathrm{id}}$, $k=1$ for Liu, stable across grids (Hyp. 5.3) | `code/inertia_check.py` | `code/INERTIA_run.log`, `code/inertia_report.json`, summary `code/INERTIA.md` | 5 min |
| Liu's PSD check reproduced; $\Pi^{\mathrm{id}}$ fails the codim-3 condition (§5) | `code/concavity_ideal.py` | `code/CONCAVITY_ideal_run.log`, `code/CONCAVITY_ideal.md` | minutes |
| **Table 2**, rows "all laws, 4/5/6 atoms" at $c=0.38284$ and $0.38288$: $1.0000733$, $1.0000085$ | `python code/certify_v2_batch.py A` and `... B` | `code/certify_v2_A.log`, `code/certify_v2_B.log`, `code/certify_v2_results.jsonl` | ~5–10 min per cell |
| Table 2, row "hiding laws, closed form" $\ge 1.000073$ | `python code/certify_v2.py 1` (part 1) | `code/certify_v2_log.txt` | seconds |
| Entropy floor lowered $10^{-4}\ldots10^{-6}$, same minimiser (§6) | `code/floor_scan.py` | `code/floor_scan.log` | 8 min |
| Decisive cell, **5,000 restarts**, floor $10^{-7}$, 4 atoms, $c=0.38284$: $1.00007334$ (Hyp. 6.1) | `code/big_restart.py` | `code/big_restart.log` | 97 min |
| Constants of Theorem 5.5 and Lemma 5.6 ($\rho$, $\varepsilon_0$, the $0.9909$ corner ratio, $t_0$ up to $0.00631$) | `code/lemma_verify.py` | stdout (prints $\varepsilon_0 = 7.6279\cdot10^{-7}$) | seconds |
| Robustness across $\beta$ and atom counts, three passes | `code/robustness_ideal.py <beta> <c> <m>` | `code/robustness_*.log`, summary `code/ROBUSTNESS_ideal.md` | hours total |
| Independent re-certification (second implementation, from the written statement only) | `verification/independent-recertification/search.py` | `verification/independent-recertification/ideal_n{4,5,6}_c38284.json`; report `code/RECERT.md` | 11 min / 53 min / 76 min |
| Sequential-coupling DP oracle on small families (§7, exploratory) | `code/seqcoupling_dp.py`, `code/symmetric_dp.py` | `code/relaxed_n{3,4}.log`, `code/search_n*.log` | minutes |

The paper's evaluator is `code/kernel_game.py` (function `ratio`; kernel `f_ideal` defined in `code/floor_scan.py` and `code/certify_v2.py`). The independent evaluator, written from the manuscript alone without sight of `kernel_game.py`, is `verification/independent-recertification/evaluator.py` (a copy is `code/recert_evaluator.py`); the two agree on every quoted number. See [`code/README.md`](code/README.md) for every script and log, including exploratory and superseded runs.

## Verification chain

1. **Referee rounds 1–4** on the manuscript, each by a fresh agent instructed to referee: `code/REFEREE.md`, `REFEREE2.md`, `REFEREE3.md`, `REFEREE4.md`. Round 1 found four errors and four gaps (all fixed: hiding definition, a $2x^2$ slip, stale $\beta=0.19$ claims, the singleton-class hypothesis, the (D) range condition); round 2 found that the first version of the small-entropy lemma dropped a factor $w$ (withdrawn, replaced by Theorem 5.5); round 3 four statement-precision gaps; round 4 no error, no gap. The referee's own check scripts are in `verification/referee-checks/`.
2. **Small-entropy lemma** proved separately (`code/LEMMA_SMALL_ENTROPY.md`, scripts `verification/small-entropy-lemma/`) and refereed (`code/REFEREE_LEMMA.md`: correct; one reach caveat, now stated in the paper as the $c > c^{**} - 1.9\cdot10^{-6}$ window).
3. **Independent re-certification** (`code/RECERT.md`): a second agent wrote its own evaluator from the manuscript, calibrated it on Liu's published optimum, and reproduced the two-point minimum $1.0000733414$ at 4, 5 and 6 atoms, the hiding-family limit $1.000073219$ from above, and the fixed point $c^{**}$.
4. **Lean formalisation** (`lean/`, see the section above): Theorems 3.1 and 3.4 and most of Lemma 3.3 are machine-checked in Lean 4 / Mathlib v4.23.0 on a finite model of the framework whose certificate hypothesis is *implied by* the paper's (so the Lean theorems apply to the paper). Zero `sorry`; axioms `propext`, `Classical.choice`, `Quot.sound` only; `bash lean/check.sh` is the gate and runs in CI (badge above). The numerical corollary proved is `c ≤ 0.3829` (< c_ceil = 0.383099, so the refined ceiling formally beats the product one); the exact `c** = 0.382885260…` is a real-number fixed point evaluated in `verify.py`, not in Lean. [`lean/CERTIFICATE.md`](lean/CERTIFICATE.md) is the dated certificate of the run — commit, toolchain, verbatim axiom output, SHA-256 of every source and build file, CI run reference, and what is and is not certified; [`lean/README.md`](lean/README.md) maps every paper statement to its Lean name.
5. Git history preserves every intermediate state, including the withdrawn $0.38293$–$0.38295$ figures (optimiser misses on the hiding law, explained in Remark 6.3 and `progress.md`).

The commits are timestamped; the whole campaign ran on 2026-09-08.

## How this was produced (AI disclosure)

The work was carried out by a team of Claude (Anthropic) language-model agents under the author's direction, in one day. The lead agent (Claude Fable 5.1) chose the problem from five scouted candidates (`literature/scouts/`), found the two ceiling theorems including the component-hiding adversary, and designed the protocol and the certification. Sonnet agents transcribed the cited literature (`literature/`). Opus agents refereed the manuscript over four rounds, proved the small-entropy lemma, and wrote the independent evaluator. The author set the goal and the standard, checked the claims, and decided what to publish. Every error the referee caught, including one in the lead agent's own lemma, is documented here.

## Layout

```
paper/                paper.tex, paper.pdf, arXiv package (union-closed-arxiv.tar.gz = paper.tex + anc/)
code/                 evaluator, certification scripts, every log; reports RECERT/REFEREE*/INERTIA/CONCAVITY/ROBUSTNESS/LEMMA
lean/                 Lean 4 / Mathlib formalisation of Theorems 3.1, 3.4 and Lemma 3.3
                      (README, SPEC, CERTIFICATE, check.sh)
verification/         scripts of the independent verifier, the lemma prover and the referee (archived verbatim)
literature/           transcripts and syntheses of the cited papers, written by the agents; candidate scouting
CEILING_THEOREM.md    the two ceiling theorems as first written, with proofs
RESULT.md             campaign result summary with per-claim status
KERNEL_OPT.md         kernel-shape search (no kernel beats c**)
NOTES_lead.md         lead agent's working notes (sequential-coupling reformulation)
progress.md           timestamped campaign log, including the incident and the withdrawn figures
```

## Licence and citation

Code, logs and JSON: MIT. Paper and reports: CC BY 4.0. See `LICENSE` and `CITATION.cff`. Liu's MATLAB scripts are not redistributed; `code/liu/README.md` gives their URLs and SHA-256 hashes.

Corrections are welcome: open an issue, or email the address on the paper.
