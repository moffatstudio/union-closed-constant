# code/

Every script and every log of the campaign, including exploratory and superseded runs. Nothing quoted in the paper depends on a file marked *exploratory* or *superseded* below. Entropy `h` is in natural log inside `kernel_game.py`; the ratio $R$ is base-invariant.

## Certification of $c = 0.38284$ (paper §5–6)

| File | Role |
|---|---|
| `kernel_game.py` | The evaluator. `ratio(z, K, beta, m)` computes $R$ of eq. (ratio) for a mixture of two products with $m$ atoms per law; `adversary_min` is the SLSQP multi-restart minimiser with `structured_inits` (two-point, Cambie, Liu, hiding laws); `c_max` bisects in $c$. `make_rank_kernel([f])` builds $K = f\otimes f$. Reproduces Liu's optimum to $10^{-9}$ (`liu_reproduce.py`). |
| `certify_v2.py` | Final certification at $w = 0.810222$ exactly. `part1`: hiding family in closed form and by direct evaluation (Table 2, row 4). `part2 <c> <m> [restarts]`: floor-constrained global search (Table 2, rows 1–3). `part3`: two-point/hiding combinations (Table 2, row 5). |
| `certify_v2_batch.py` | Runs `part2` over $(c, m) \in \{0.38284, 0.38288\}\times\{4,5,6\}$ in two halves `A`/`B`. Logs: `certify_v2_A.log`, `certify_v2_B.log`; machine output `certify_v2_results.jsonl`, `certify_v2_mixed.jsonl`; human log `certify_v2_log.txt`. |
| `floor_scan.py` | Same search with the entropy floor $\int h\,d\mu \ge \eta_0$ lowered to $10^{-4}, 10^{-5}, 10^{-6}$; also checks that the hiding coupling's maximal correlation $\to 0$. Log: `floor_scan.log`. |
| `big_restart.py` | The decisive cell: 5,000 restarts, floor $10^{-7}$, 4 atoms, $c=0.38284$ → min $1.00007334$ at the two-point law (Hypothesis 6.1). Log: `big_restart.log` (97 min). |
| `inertia_check.py` | Inertia of the projected quadratic form for Liu's kernel, $\Pi^{\mathrm{id}}$ and `K_new` at $dt = 10^{-3}, 5\cdot10^{-4}$ (Hypothesis 5.3). Log `INERTIA_run.log`, numbers `inertia_report.json`, report `INERTIA.md`. |
| `concavity_ideal.py` | Reproduces Liu's codim-3 PSD check for his kernel and shows $\Pi^{\mathrm{id}}$ fails it (§5). Log `CONCAVITY_ideal_run.log`, numbers `concavity_ideal_report.json`, report `CONCAVITY_ideal.md`. |
| `lemma_verify.py` | Numerical checks of every constant and inequality in Theorem 5.5 / Lemma 5.6 ($\rho$, $\varepsilon_0$, (F2), the corner ratio $0.9909$, $t_0$ up to $0.00631$). |
| `robustness_ideal.py` | Three-pass robustness sweep over $\beta$, $c$ and atom count (`ROBUSTNESS_ideal.md`; logs `robustness_beta15-20_partial_{A,B}.log`). The first pass is what exposed the hiding adversary. |
| `liu_reproduce.py` | Two reproductions of Liu's Theorem 13: closed-form equations (87)–(88), and the full 9-parameter optimisation. Requires nothing from Liu's MATLAB files (`liu/README.md`). |
| `recert_evaluator.py` | Copy of the independent evaluator (`verification/independent-recertification/evaluator.py`), written from the manuscript alone. Report: `RECERT.md`. |
| `small_entropy_lemma.py` | The *first* small-entropy lemma, whose numerical instance dropped a factor $w$ (caught in referee round 2). Kept for the record; superseded by `LEMMA_SMALL_ENTROPY.md` and `lemma_verify.py`. |

## Reports

`RECERT.md` (independent re-certification), `REFEREE.md`, `REFEREE2.md`, `REFEREE3.md`, `REFEREE4.md` (four referee rounds on the manuscript), `REFEREE_LEMMA.md` (referee report on the small-entropy lemma), `LEMMA_SMALL_ENTROPY.md` (the lemma's proof as first written, with all constants), `INERTIA.md`, `CONCAVITY_ideal.md`, `ROBUSTNESS_ideal.md`.

## Superseded certification runs

`certify_ideal.py`, `certify_batch.py`, logs `certify_A.log`, `certify_B.log`, `certify_log.txt`, `certify_results.jsonl`: the v1 run at the *rounded* weight $\beta = 0.1897$ and with the plain SLSQP that cannot resolve the hiding family. Replaced by `certify_v2.py` (exact $\beta^{**} = 0.189778$, closed-form hiding family). Numbers agree where they overlap.

## Kernel search and sweeps (§4, `KERNEL_OPT.md`)

`kernel_sweep.py <kernel> <betas> [m] [lam]` bisects $c_{\max}$ for a named kernel: logs `sweep_ideal_b*.log`, `sweep_liu_b0.1.log`, `sweep_new_b*.log`. **The values above $0.38289$ in `sweep_ideal_b0.3.log`, `sweep_ideal_b0.4_0.5.log` etc. are optimiser misses on the hiding law and are withdrawn** (paper Remark 6.3; `progress.md` 14:40 and 16:05 entries). `kernel_opt_search.py`, `smooth_kernel_opt.py`, `smooth_kernel_search.py`, `beta_scan_ideal.py`, `kernel_game3.py` (three-protocol mixtures with Sawin's term), `best_kernel.json`, `smooth_kernel_opt_best.json`, `smooth_kernel_search_coarse.json`, `kernel_opt_adversary_pool.json`, `KERNEL_OPT_run.log`, `smooth_kernel_opt_run.log`, `smoketest2.log`: the double-oracle search that found no kernel beating $c^{**}$. `degenerate_seed_check.py`, `dissect.py`, `policy_dump.py`, `check_psi_lemma.py`, `chase_lovett_example.py`, `liu_shared_ideal.py`: small diagnostic scripts.

## Machine-checked proofs: `../lean/`

The two ceiling theorems (paper Theorems 3.1 and 3.4) and the elementary parts of Lemma 3.3 are formalised in Lean 4 / Mathlib in [`../lean/`](../lean/) — no `sorry`, axioms `propext`, `Classical.choice`, `Quot.sound` only. Nothing in this directory is used by that proof and nothing there replaces the numerics here: the Lean development covers the *unconditional* ceilings (`c ≤ 0.3829`), while the scripts above certify the conditional constant $c = 0.38284$ and evaluate the exact fixed point $c^{**} = 0.382885260\ldots$, neither of which is formalised. Gate: `bash ../lean/check.sh`. See [`../lean/README.md`](../lean/README.md) and [`../lean/CERTIFICATE.md`](../lean/CERTIFICATE.md).

## Exploratory: sequential-coupling oracle on actual families (§7)

`seqcoupling_dp.py` (exact DP for any family), `symmetric_dp.py` (slice unions, $n \le 24$), `relaxed_game.py`, `barrier_hunt.py`, `barrier_search_random.py`, `greedy_hunt.py`, `symmetric_greedy.py`, `batch_driver.py`; logs `relaxed_n{3,4}.log`, `barrier_hunt_n4.log`, `search_n{5,6,7}_p045.log`, `greedy_search_n*.log`. These support only the qualitative remark in the Discussion and are not part of any theorem.
