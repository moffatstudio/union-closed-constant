# Gilmer's entropy breakthrough and the Chase–Lovett sharpness example

## Gilmer, arXiv:2211.09055

- **Title:** "A constant lower bound for the union-closed sets conjecture"
- **Submitted:** 16 Nov 2022 (Justin Gilmer, Google)
- **Main theorem:** In any union-closed family F ⊆ 2^[n], some element i ∈ [n]
  lies in at least a **0.01** fraction of the sets of F. First-ever constant
  (n-independent) lower bound, improving the previous Ω(1/log₂|F|)-type bounds
  (Knill, Wójcik — see 04_structural-facts.md).
- **Method (information-theoretic strengthening):** if A, B are i.i.d. samples
  from the uniform distribution on F, and Pr[i ∈ A] < 0.01 for every i, then
  H(A ∪ B) > H(A). Since H(A) = log₂|F| is the max-entropy value for a
  distribution supported on F, and A ∪ B is supported on F ∪ F ⊇ F, this forces
  |F ∪ F| > |F|; union-closedness (F ∪ F = F) then gives a contradiction unless
  some element has density ≥ 0.01.
- **Update note (28 Nov 2022, in the paper itself):** records that follow-up
  work rapidly pushed the constant to ψ = (3−√5)/2 ≈ 0.381966, and that a
  stronger conjecture Gilmer posed (that would have implied the *full* 1/2
  bound) was refuted — see arXiv:2211.12401 (Sawin/Ellis counterexample) and
  03_tao-and-scandone.md.

## The ψ = (3−√5)/2 improvement (four independent groups, ~20 Nov 2022)

Within days, four papers independently pushed Gilmer's constant to the root of
x² − 3x + 1 = 0, i.e. ψ = (3−√5)/2 ≈ 0.3819660:
- Alweiss, Huang, Sellke
- Chase, Lovett
- Sawin
- Pebody

All four proofs turn on the same sharp form of a binary-entropy inequality
("Lemma 5" in the later literature), later given a clean calculus proof by
Boppana (Jan 2023) via a classical 1989 result.

The current record is **Liu (2023), 0.38271...**, via a refined coupling
argument (per the campaign's problem statement) — a small improvement over ψ
itself but still governed by the same entropy machinery; the sharpness result
below explains why this family of techniques plateaus near ψ.

## Chase–Lovett, arXiv:2211.11689, "Approximate union closed conjecture"

- **Submitted:** 22 Nov 2022
- **Abstract (verbatim):** "A set system is called union closed if for any two
  sets in the set system their union is also in the set system. Gilmer
  recently proved that in any union closed set system some element belongs to
  at least a 0.01 fraction of sets, and conjectured that his technique can be
  pushed to the constant (3−√5)/2. We verify his conjecture; show that it
  extends to approximate union closed set systems, where for nearly all pairs
  of sets their union belong to the set system; and show that for such set
  systems this bound is optimal."

### The exact sharpness construction (Example 1.4 in the paper)

For n large, with ψ = (3−√5)/2:

```
F1 = { x ∈ {0,1}^n : |x| = ψn + n^(2/3) }      (a single Hamming-weight layer)
F2 = { x ∈ {0,1}^n : |x| ≥ (1−ψ)n }            (an upward-closed "cap")
F  = F1 ∪ F2
```

Properties verified in the paper (and reverified numerically here, see
`../code/chase_lovett_example.py`):

1. **F is (1−o(1))-approximately union-closed.** F2 is automatically closed
   under ∪ with anything (OR only increases Hamming weight, so any pair
   touching F2 has its union's weight ≥ the F2 threshold, landing back in F2).
   The only possible "escapes" are F1×F1 pairs. For x, y independent uniform
   weight-k1 vectors (k1 = ψn + n^(2/3)), the overlap |x∩y| is
   Hypergeometric(n, k1, k1) with mean k1²/n, so the union weight
   2k1 − |x∩y| concentrates around (1−ψ)n **plus a term of order 2(1−ψ)n^(2/3)**
   — i.e. the n^(2/3) correction added to k1 is exactly what pushes the union
   weight's mean safely above the F2 threshold by more than its
   O(√n) standard deviation, forcing P[union ∉ F] → 0.
2. **|F2| = o(|F1|)**, using the identity 1 − ψ = 2ψ − ψ² (equivalent to
   ψ² − 3ψ + 1 = 0): F1 sits essentially at the peak of the binomial
   distribution's relevant range while F2 is a vanishing tail.
3. **Every element i ∈ [n] lies in at most ψ + o(1) fraction of F.** Because
   F1, F2 are each unions of full symmetric Hamming layers, by symmetry every
   coordinate has the *same* frequency, exactly computable as a weighted
   average of k/n over the included layers — which our script confirms
   converges to ψ as n → ∞ (dominated by the F1 layer since |F2|/|F1| → 0).

### Numerical verification (this campaign)

`../code/chase_lovett_example.py` computes (a) the exact per-element frequency
via log-space binomial sums (no enumeration needed, exact for n up to 10^6+)
and (b) a vectorized Monte Carlo estimate of the F1×F1 "bad pair" probability
via direct hypergeometric sampling of the overlap. Results:

| n | freq(F) | freq − ψ | \|F2\|/\|F1\| | P(bad pair) |
|---|---|---|---|---|
| 50 | 0.6433 | 2.61e-01 | 6.80 | 0 (even at n=10) |
| 1,000 | 0.4820 | 1.00e-01 | 1.9e-12 | 0 |
| 100,000 | 0.4035 | 2.15e-02 | ~0 | 0 |
| 1,000,000 | 0.3920 | 1.00e-02 | ~0 | 0 |

freq(F) − ψ decays like n^(−1/3) (matching the n^(2/3)/n correction term
built into k1), confirming convergence to ψ from above; the bad-pair
probability is already numerically indistinguishable from 0 by n ≈ 20–30
because the concentration gap (n^(2/3) vs. O(√n) fluctuation) opens fast.

### Significance

This is the **sharp barrier for the entropy method as currently formulated**:
ψ is not an artifact of a weak proof technique, it is the true extremal
constant for the *approximate* version of the problem the entropy argument
actually controls. Any proof that pushes past ψ toward 1/2 for the *exact*
conjecture must use some fact that is true for exactly union-closed families
but **false** for this (1−o(1))-approximately union-closed F — see
SYNTHESIS_lane4.md for candidates.

## Sources

- Gilmer: https://arxiv.org/abs/2211.09055
- Chase–Lovett: https://arxiv.org/abs/2211.11689 (construction: arXiv:2211.11689 HTML, Example 1.4)
- Sawin/Ellis counterexample to Gilmer's stronger conjecture: https://arxiv.org/abs/2211.12401
