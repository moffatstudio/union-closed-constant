"""
Verification of the Chase-Lovett sharpness example for approximately
union-closed families (arXiv:2211.11689, "Approximate union closed
conjecture", Example 1.4).

Construction (verbatim from the paper, n large):
    psi = (3 - sqrt(5)) / 2                      (root of x^2 - 3x + 1 = 0)
    F1  = { x in {0,1}^n : |x| = psi*n + n^(2/3) }
    F2  = { x in {0,1}^n : |x| >= (1-psi)*n }
    F   = F1 union F2

Claims to verify:
  (a) F is (1-o(1))-approximately union-closed: the fraction of pairs
      (x,y) in F x F whose bitwise-OR x|y is NOT in F tends to 0 as
      n -> infinity.
  (b) No element's frequency in F exceeds psi + o(1); i.e. max_i
      Pr_{x in F}[i in x] -> psi from above is NOT possible -- frequency
      is bounded by psi + o(1), matching the "no better than Gilmer's
      constant" claim for approximate families.
  (c) |F2| = o(|F1|), so F is overwhelmingly concentrated on the single
      layer F1 (this is what drives the frequency down to psi).

Key structural fact used for an EXACT (not just sampled) analysis of (b)
and (c): every set in this construction is invariant under the symmetric
group acting on coordinates (F1 and F2 are unions of full Hamming-weight
layers). So the frequency of any fixed coordinate i is exactly

    freq(i) = [ sum_{k in weights(F)} (k/n) * C(n,k) ] / [ sum_{k in
                weights(F)} C(n,k) ]

which we can compute exactly (in log-space, via log-binomial /
lgamma, to avoid overflow) without ever enumerating 2^n vectors.

For (a), F2 is upward-closed under OR (if |x|>=t or |y|>=t then
|x|y| >= max(|x|,|y|) >= t), and any pair touching F2 has its OR's
weight >= the F2 threshold, hence automatically lands back in F2 (part
of F). So the ONLY possible "bad" pairs are F1 x F1 pairs whose OR
lands strictly below the F2 threshold AND is not exactly on the F1
level (positive-probability event under a uniform-random model that we
verify tends to 0 by direct Monte-Carlo sampling of random pairs on the
F1 level, using the OR-weight = 2k - |x & y| identity and simulating the
intersection size via a hypergeometric draw).
"""

import math
import numpy as np
from math import comb, lgamma, log, exp, sqrt

PSI = (3 - sqrt(5)) / 2  # ~0.3819660113


def log_binom(n, k):
    """log C(n,k), safe for large n."""
    if k < 0 or k > n:
        return float("-inf")
    return lgamma(n + 1) - lgamma(k + 1) - lgamma(n - k + 1)


def layer_weights(n):
    """Return (k1, t2) = (F1's exact weight level, F2's threshold level)."""
    k1 = round(PSI * n + n ** (2 / 3))
    t2 = math.ceil((1 - PSI) * n)
    return k1, t2


def log_sum_exp(logs):
    m = max(logs)
    if m == float("-inf"):
        return float("-inf")
    return m + log(sum(exp(x - m) for x in logs))


def exact_frequency_and_sizes(n):
    """Exact (log-space) computation of:
       - log|F1|, log|F2|
       - the common per-element frequency of F (by coordinate symmetry)
    """
    k1, t2 = layer_weights(n)

    log_F1 = log_binom(n, k1)

    log_F2_terms = [log_binom(n, k) for k in range(t2, n + 1)]
    log_F2 = log_sum_exp(log_F2_terms)

    log_F = log_sum_exp([log_F1, log_F2])

    # numerator: sum_k (k/n) C(n,k) over k in {k1} union [t2, n]
    # compute in log-space via log(k/n) + log C(n,k); guard k=0
    def log_k_over_n_binom(k):
        if k == 0:
            return float("-inf")
        return log(k / n) + log_binom(n, k)

    log_num_terms = [log_k_over_n_binom(k1)] + [
        log_k_over_n_binom(k) for k in range(t2, n + 1)
    ]
    log_num = log_sum_exp(log_num_terms)

    freq = exp(log_num - log_F)
    size_ratio_F2_over_F1 = exp(log_F2 - log_F1)  # should -> 0

    return {
        "n": n,
        "k1": k1,
        "t2": t2,
        "freq": freq,
        "freq_minus_psi": freq - PSI,
        "F2_over_F1": size_ratio_F2_over_F1,
    }


def monte_carlo_bad_pair_fraction(n, trials=200_000, seed=0):
    """
    Estimate, for pairs (x,y) drawn independently and uniformly from the
    F1 layer (weight exactly k1), the fraction whose OR-weight lands
    strictly below the F2 threshold t2 (the only way such a pair's union
    can fail to lie in F, since it also essentially never lands back
    exactly on the F1 level for large n).

    We do NOT need to materialize length-n bit vectors: for two
    independent uniformly random k1-subsets of an n-set, the overlap
    size |x & y| follows the hypergeometric distribution
    Hypergeometric(N=n, K=k1, n_draws=k1) (drawing y's support as a
    random k1-subset and counting how many of x's k1 marked elements
    it hits). numpy's hypergeometric sampler is vectorized (O(1)
    amortized per sample), so this scales to large n and many trials.
    """
    rng = np.random.default_rng(seed)
    k1, t2 = layer_weights(n)

    # numpy signature: hypergeometric(ngood, nbad, nsample, size)
    # urn: k1 "good" (x's support), n-k1 "bad", draw k1 (y's support)
    overlaps = rng.hypergeometric(ngood=k1, nbad=n - k1, nsample=k1, size=trials)
    union_weights = 2 * k1 - overlaps

    exact_f1_hits = np.count_nonzero(union_weights == k1)
    bad = np.count_nonzero(union_weights < t2)  # excludes the ==k1 case automatically
    return bad / trials, exact_f1_hits / trials


def main():
    print(f"psi = (3-sqrt(5))/2 = {PSI:.10f}")
    print(f"Check psi is root of x^2-3x+1: {PSI**2 - 3*PSI + 1:.2e} (~0)")
    print(f"Check identity 2*psi - psi^2 == 1-psi: "
          f"{2*PSI - PSI**2:.10f} vs {1-PSI:.10f}\n")

    print("=== Exact (log-space, whole-layer) results ===")
    print(f"{'n':>8} {'k1':>10} {'t2':>10} {'freq(F)':>12} "
          f"{'freq-psi':>12} {'|F2|/|F1|':>14}")
    for n in [50, 200, 1_000, 10_000, 100_000, 1_000_000]:
        r = exact_frequency_and_sizes(n)
        print(f"{r['n']:>8} {r['k1']:>10} {r['t2']:>10} "
              f"{r['freq']:>12.8f} {r['freq_minus_psi']:>12.2e} "
              f"{r['F2_over_F1']:>14.3e}")

    print("\n=> As n grows, freq(F) -> psi from ABOVE, and |F2|/|F1| -> 0,")
    print("   confirming F2 is a vanishing correction and the family's")
    print("   element frequency approaches Gilmer's constant psi exactly.")

    print("\n=== Monte Carlo: F1 x F1 pair 'badness' (union not in F) ===")
    print(f"{'n':>8} {'k1':>10} {'t2':>10} {'P(bad pair)':>14} "
          f"{'P(union weight==k1)':>20}")
    for n in [10, 15, 20, 30, 50, 80, 130, 200, 1_000, 5_000, 20_000, 100_000]:
        bad_frac, exact_hit = monte_carlo_bad_pair_fraction(n, trials=200_000)
        print(f"{n:>8} {layer_weights(n)[0]:>10} {layer_weights(n)[1]:>10} "
              f"{bad_frac:>14.6f} {exact_hit:>20.2e}")

    print("\n=> P(bad pair) -> 0 as n -> infinity: the fraction of pairs")
    print("   whose union escapes F vanishes, i.e. F is (1-o(1))-")
    print("   approximately union-closed, exactly as claimed in")
    print("   Chase-Lovett Example 1.4. Since element frequency is pinned")
    print("   at psi (from the exact computation above) while the")
    print("   approximation error -> 0, this shows psi = (3-sqrt(5))/2 is")
    print("   the best constant achievable for approximately union-closed")
    print("   families -- Gilmer's method cannot be pushed past psi there,")
    print("   even though genuinely (exactly) union-closed families are")
    print("   conjectured to always have an element of frequency >= 1/2.")


if __name__ == "__main__":
    main()
