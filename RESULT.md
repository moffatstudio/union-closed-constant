# Union-closed sets: the ceiling of the single-letter entropy method, and reaching it

**Final status 2026-09-08 18:30:** paper/paper.pdf is the publication version (13 pp). Four referee rounds → no error, no gap. Independent
re-certification agrees on every number. Record: c ≥ 0.38284 (Liu-level rigor); proved ceilings 0.383099 / 0.382885260.

Campaign 057, 2026-09-08. Lead: Claude (Fable 5.1); Sonnet agents for literature transcription and numerics.

Status of each claim is marked **[proved]**, **[numerical, Liu-level rigor]** or **[numerical only]**.

## 1. Setting

F ⊆ 2^[n] union-closed, A, B ~ Unif(F) coupled; H(A∪B) ≤ log|F| = H(A). Gilmer's chain-rule argument reduces, for a

*protocol* Π (a memoryless rule coupling the two conditional Bernoulli bits given the two prefixes) and a class C_Π(µ) of

joint laws of the two prefix-conditional zero-probabilities (X, Y) that Π can induce, to the single-letter certificate

   Σ_k w_k · inf_{P ∈ C_k(µ)} E_P[ h(Π^(k)_{X,Y}(0,0)) ] ≥ E_µ[h(X)]   for all µ on [0,1] with E_µ[X] ≥ 1 − c.        (16)

Known instances: iid (Gilmer/AHS/Chase–Lovett/Sawin/Pebody, ψ = 0.381966), Sawin's anti-correlated protocol with the

class of all couplings (Yu/Cambie, exactly 0.3823455), Liu's conditionally-iid protocol with the class of mixtures of

products (0.382709, conditional on two numerically verified hypotheses). Record before this campaign: **0.382709** (Liu 2023).

## 2. Results

**Theorem A (ceiling, [proved], CEILING_THEOREM.md).** For every protocol mixture in which each class contains the product

law µ⊗µ, (16) fails for c > 1 − h(1/√2)/√2 = 0.3830993. (Two-point law x* = 1/√2 with independent prefixes; on the diagonal

h(Π(0,0)) ≤ 1 = h(x*²) for every protocol, and all other pairs are forced.)

**Theorem B (refined ceiling, [proved], CEILING_THEOREM.md §2).** If the mixture contains the iid protocol with weight w_iid

and every other class admits *component hiding* (a coupling in which a tiny-mass entropy-carrying atom is never paired with

the "surely absent" atom — true for all couplings, for mixtures of products, and for every maximal-correlation class),

then (H) 2·w_iid·(1−c) ≥ 1, and with the diagonal adversary (D) the certified constant satisfies

   c ≤ c** = 0.382885260,   attained only with w_iid = 0.810222 (β = 0.189778) and diagonal value h(Π(0,0)) = 1 at x* = 0.690908.

Consequently the single-letter protocol method, in every form used since 2022, cannot certify more than 0.382885.

**Theorem C (attainment, [numerical, Liu-level rigor — CERTIFIED 2026-09-08 17:30]).** The conditionally-iid protocol with shared uniform U,

   P(bit = 0 | U=u) = x + f(x)·sgn(u − 1/2),   f(x) = min(x, 1−x) on [0, 1/2],  √(1/2 − x²) on [1/2, 1/√2],  0 on [1/2, 1]

(realizable: f ≤ min(x,1−x); kernel K = f⊗f; P(both 0) = xy + f(x)f(y) ≤ 1/2 wherever f(x)f(y) > 0, so it dominates iid

pointwise), mixed with the iid protocol at β = 0.19, certifies

   **c = 0.382885**  (bisection, code/sweep_ideal_b0.19.log; two-point adversary at x* ≈ 0.691 binding),

matching c** to the resolution of the search. Improvement over Liu: +0.000176; over Cambie's exact Sawin-class value: +0.00054.

> **Correction (16:40, see progress.md).** The bisection sweep cannot see the component-hiding law, whose infimum is approached only as the tiny atom's weight tends to 0, so the figure 0.382885 above is the two-point-side value only. The correct statement is sup c = c** = 0.382885 at β** = 0.189778, where both adversaries give ratio exactly 1, and the constant actually certified (Table 2 of the paper, with a margin of 7.3·10⁻⁵ in the ratio) is **c = 0.38284**, as in the header. The +0.000176 becomes +0.000131 for the certified constant.

Rigor ledger for Theorem C (mirrors Liu's Theorem 13 exactly):

1. Reduction of the adversary to a mixture of two products — Liu's Theorem 9, valid for every conditionally-iid protocol **[proved by Liu]**.

2. Cardinality: the quadratic form −h(xy + K) on the mean-zero subspace has exactly k = 2 negative directions for f_ideal

   (k = 1 for Liu's kernel), stable under grid refinement (code/INERTIA.md) **[numerical]**; fixing those two functionals makes

   the objective concave on every slice, so minimisers have ≤ 4 atoms per component (Liu's Theorem-12 argument, generalised).

3. Global minimisation over adversaries with ≤ 4 (also 5, 6) atoms per component at β**=0.189778: min ratio 1.0000733 at

   c=0.38284 and 1.0000085 at c=0.38288 (300–500 restarts, structured + mixed seeds, floor E h ≥ 1e-3); hiding family ≥ 1.000073

   (closed form, converging from above); mixed laws 1.0000733. All minimisers = the two-point law.

   **[numerical, code/certify_*.log, code/ROBUSTNESS_ideal.md]**.

   code/ROBUSTNESS_ideal.md]**; structured seeds include both binding adversaries (the earlier β=0.25–0.3 claims were

   optimiser misses on the degenerate law and are withdrawn).

## 3. Why the earlier steps landed where they did

- Gilmer/ψ: iid protocol under-uses the diagonal for x < 1/√2 (h(x²) < 1). Extremal law U ≡ 1/φ.

- Sawin/Yu/Cambie 0.3823455: the anti-correlated protocol reaches h = 1 on the diagonal but its class lets the adversary

  cut the diagonal mass from p² to 2p−1 and, via Cambie's two-point law, saturate both terms simultaneously.

- Liu 0.382709: conditionally-iid protocols keep the product law but only mixtures of products; his rank-one kernel

  f = x(1−x) has diagonal x² + x²(1−x)², and the adversary sits exactly where that equals 1 − x² (kernel-neutral point).

- This campaign: the ideal diagonal 1/2 − x² is realizable; the component-hiding adversary is what caps β at 0.19 and

  makes the remaining gain +0.00018 rather than +0.0004.

## 4. Other findings (exploratory, not part of the theorem)

- Sequential-coupling DP oracle on actual families (code/seqcoupling_dp.py): no family on ≤ 4 elements with max frequency

  < 1/2 defeats the full sequential class; symmetric slice unions up to n = 24 all beaten. The single-letter relaxation is

  what loses this power (the adversary gets to choose the prefix joint law).

- Greedy "closest-to-1/2" rule alone fails at p = 0.40 by n = 6.

- No frequency-only potential can prove the conjecture (NOTES_lead.md).

## 5. What would be needed to go past 0.382885

A tensorising constraint on the prefix joint law that forbids component hiding (so the iid weight can drop below 0.81), or a

non-single-letter use of exact union-closure (e.g. H(A∪B) ≤ log|F| − D(law(A∪B) ‖ Unif(F))). Both are open.

## Files

CEILING_THEOREM.md · NOTES_lead.md · progress.md · literature/ (11 transcripts + 4 syntheses) · code/kernel_game.py,

kernel_sweep.py, seqcoupling_dp.py, symmetric_dp.py, relaxed_game.py, INERTIA.md, CONCAVITY_ideal.md, ROBUSTNESS_ideal.md.

