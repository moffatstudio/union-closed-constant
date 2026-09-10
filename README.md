# The ceiling of the single-letter entropy method for the union-closed sets conjecture, and a protocol that reaches it

Andrew Moffat, 8 September 2026. Paper: [`paper/paper.pdf`](paper/paper.pdf) (13 pp; source [`paper/paper.tex`](paper/paper.tex)). arXiv: *identifier to be added on announcement*; math.CO, cross-list cs.IT; MSC 05D05, 94A17, 60E15.

This repository holds everything needed to check the paper: the code, the raw logs of every run quoted in it, the reports of four referee rounds, an independent re-implementation of the certificate, and the campaign log. Nothing was removed to tidy the story; withdrawn intermediate claims are marked as such where they occur.

## What is claimed, and how firmly

| Claim | Where in the paper | Status |
|---|---|---|
| **Ceiling.** Every single-letter certificate whose classes contain product laws certifies at most $c_{\mathrm{ceil}} = 1 - h(1/\sqrt2)/\sqrt2 = 0.383099\ldots$ | Theorem 3.1 | **Proved** (short, elementary; `CEILING_THEOREM.md`) |
| **Refined ceiling.** Every certificate using the i.i.d. protocol whose other classes admit *component hiding* certifies at most $c^{**} = 0.382885260\ldots$ | Theorem 3.4 | **Proved** (`CEILING_THEOREM.md`, refined section) |
| All classes in Gilmer, AHS, Chase–Lovett, Sawin, Pebody, Yu, Cambie, Liu contain products and admit hiding | Lemma 3.3 | **Proved** |
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
4. Git history preserves every intermediate state, including the withdrawn $0.38293$–$0.38295$ figures (optimiser misses on the hiding law, explained in Remark 6.3 and `progress.md`).

The commits are timestamped; the whole campaign ran on 2026-09-08.

## How this was produced (AI disclosure)

The work was carried out by a team of Claude (Anthropic) language-model agents under the author's direction, in one day. The lead agent (Claude Fable 5.1) chose the problem from five scouted candidates (`literature/scouts/`), found the two ceiling theorems including the component-hiding adversary, and designed the protocol and the certification. Sonnet agents transcribed the cited literature (`literature/`). Opus agents refereed the manuscript over four rounds, proved the small-entropy lemma, and wrote the independent evaluator. The author set the goal and the standard, checked the claims, and decided what to publish. Every error the referee caught, including one in the lead agent's own lemma, is documented here.

## Layout

```
paper/                paper.tex, paper.pdf, arXiv package (union-closed-arxiv.tar.gz = paper.tex + anc/)
code/                 evaluator, certification scripts, every log; reports RECERT/REFEREE*/INERTIA/CONCAVITY/ROBUSTNESS/LEMMA
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
