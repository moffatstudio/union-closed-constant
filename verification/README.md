# verification/

Scripts written by the three checking agents, archived verbatim from their working directories (only the `sys.path` line and a machine path in one log were changed). Each agent worked in a separate clone of this repository at the commit named below. Their written reports live next to the main code: `code/RECERT.md`, `code/REFEREE.md`–`REFEREE4.md`, `code/REFEREE_LEMMA.md`, `code/LEMMA_SMALL_ENTROPY.md`.

## independent-recertification/ — second implementation of the certificate

Clone at commit `1dfde39`. The verifier was given the short note `paper/note.tex` (later retired; it is in the git history at that commit) and `RESULT.md`, and instructed to write an evaluator without reading `code/kernel_game.py`.

| File | Purpose | Result |
|---|---|---|
| `evaluator.py` | Ratio $R$, kernels `f_liu` and `f_ideal`, SLSQP local minimiser (softmax weights, atoms in $[0,1]$, $q \in [0,1]$) | — |
| `calib.py` | Calibration on Liu's published minimiser at $(c', w) = (0.382709, 0.899947)$ | $R = 1.000000000$ |
| `closed.py` | Two-point family, hiding family in closed form, fixed point $c^{**}$ | $c^{**} = 0.382885260$, $x^* = 0.6909077$, $w = 0.810222$; hiding limit $1.000073219$ from above at $c = 0.38284$ |
| `search.py` | Structured seeds + random restarts, $n = 4, 5, 6$ atoms | `ideal_n4_c38284.json` $1.0000733414$ (659 s), `ideal_n5_c38284.json` $1.0000733414$ (3185 s), `ideal_n6_c38284.json` $1.0000733413$ (4555 s) — all at the two-point law |

Run from this directory: `python calib.py`, `python closed.py`, `python search.py ideal <atoms> [c]` (e.g. `python search.py ideal 4 0.38284`; `python search.py liu 3` reproduces Liu's optimum).

## small-entropy-lemma/ — the lemma prover's scripts

Working files behind `code/LEMMA_SMALL_ENTROPY.md` (Theorem 5.5 of the paper). `constants.py` (all constants to full precision), `opt_t0.py` (choice of $t_0$), `verify.py`, `verify2.py` (grid checks of the pointwise inequality and of (F2)–(F5)), `explore1.py`, `explore2.py`, `adv.py`, `adv2.py`, `adv3.py` (adversarial searches for a law with $E \le 10^{-3}$ and $R$ below the claimed bound; none found, infimum equals the hiding limit $2w(1-c)$).

## referee-checks/ — the referee's recomputations

Clone at commit `41710dd` (round 3 state; round 4 signed off on the same text plus two cosmetic fixes). Every number the referee reports was recomputed with these: `cstar.py` ($c^{**}$, $w^{**}$, $x^*$), `ref_check.py` ($h(1/\sqrt2)$, $c_{\mathrm{ceil}}$), `liu_check.py`, `liu_repro.py` (Liu's constant to 13 digits), `inertia.py`, `inertia2.py` (inertia $k = 2$ on eleven grids with density and trapezoid weights), `maxcorr.py` (maximal correlation of the hiding coupling), `adv.py`, `adv2.py` (adversary searches; `adv2.log`), `chk2.py`, `chk3.py`, `chk4.py` (round 2–3 items: where $p > 1$ on $[1/2, 1/\sqrt2]$, monotonicity of $G$ on the restricted domain $X_c$, the $c$-range of the (D) condition), `lem55.py` (the factor-$w$ error in the first small-entropy lemma), `lemcheck.py`, `lemcheck2.py`, `lemcheck3.py`, `lemgap.py`, `lemadv.py`, `lemadv2.py` (round on the sharp lemma: 50-digit constants via mpmath, each inequality, the reach gap; logs `lemadv.log`, `lemadv2.log`).

## lean/ — machine-checked proofs

Not a script archive: the directory [`../lean/`](../lean/) is a Lake project holding a Lean 4 / Mathlib formalisation of the paper's two *unconditional* results, written on 2026-09-10 by a Claude (Anthropic) agent from `../lean/SPEC.md` and checked statement-by-statement against the paper by the author.

| Paper | Lean | File |
|---|---|---|
| Theorem 3.1 (product ceiling), $c_{\mathrm{ceil}} = 1 - h(1/\sqrt2)/\sqrt2$ | `product_ceiling`, `cCeil` | `UnionClosedCeiling/Ceiling.lean` |
| Theorem 3.4, inequality (H) | `hiding_bound` | `UnionClosedCeiling/Refined.lean` |
| Theorem 3.4, inequality (D) | `diagonal_bound` | `UnionClosedCeiling/Refined.lean` |
| Theorem 3.4, fixed-point form | `fixed_point_form` | `UnionClosedCeiling/Refined.lean` |
| Theorem 3.4, numerical consequence | `refined_ceiling_numeric : c ≤ 3829/10000` | `UnionClosedCeiling/Refined.lean` |
| Lemma 3.3 for the i.i.d., all-couplings and mixture-of-products classes | `containsProduct_*`, `admitsHiding_*` | `UnionClosedCeiling/Classes.lean` |

Zero `sorry`; the ten declarations above depend only on `propext`, `Classical.choice`, `Quot.sound`. Gate: `bash ../lean/check.sh` (build + `sorry` scan + `#print axioms` scan), which also runs in CI. Not formalised: Proposition 2.2, the maximal-correlation class of Lemma 3.3, Sections 4–6, and the exact value $c^{**} = 0.382885260\ldots$ (Lean proves $c \le 0.3829$). Details and the reproduction recipe: `../lean/README.md`, `../lean/CERTIFICATE.md`.
