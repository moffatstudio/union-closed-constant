# Referee report, fourth pass (sign-off): `paper/paper.tex` at commit `41710dd`

## Round-three items: all four closed

**G1 (monotonicity of `G` with a `c`-dependent domain) — CLOSED, and the parenthetical is true.** The proof now argues that the constraint defining `X_c` is inactive at the minimiser for `c` in `[0.2, 0.45]`, so `G` equals the unrestricted minimum there and the earlier argument applies, with the two tails checked directly. I verified every part of that:

| `c` | smallest `x` in `X_c` | minimiser of `G` |
|---|---|---|
| 0.20 | 0.605592 | 0.69810 |
| 0.30 | 0.609149 | — |
| 0.382885 | 0.612495 | 0.69091 |
| 0.45 | 0.615534 | 0.67889 |

So `X_c` contains `[0.62, 1/sqrt2]` throughout the range (the threshold never exceeds `0.6156`, and even at `c = 0.49` it is only `0.6175`), while the minimiser stays in `[0.679, 0.698]`. The parenthetical claim is exactly right. The tails also check: `G(0.05) = 0.3830026`, `G(0.15) = 0.3829895`, `G(0.20) = 0.3829798`, all above `c`, and `G(0.45) = 0.3827288`, `G(0.46) = 0.3826762`, `G(0.49) = 0.3823162`, all below `c`. Hence `{c : c <= G(c)} = (0, c**]`.

**G2 (Hypothesis 6.1's value) — CLOSED.** The hypothesis now leads with `R >= C = 1.00005` on the set, then states the infimum as `2w(1-c) = 1.0000732` approached along the hiding family, with `1.0000733` attained at the two-point law on the subset with entropy at least `1e-7`. That is exact, and it is what Theorem 6.2 uses. The hiding family is legitimately inside the four-atom set (`P_1 = delta_1`, `P_0` two atoms), so the infimum statement is coherent.

**G3 (unbridged window) — CLOSED.** The text now gives the three-way division explicitly: proved below `eps_0` by Lemma 5.5 plus compactness, computed at or above `1e-7`, hypothesised between, with `eps_0 ~ 1e-30000` and the `kappa(eta) > 0.99998`, `eta < 2^-86000` figures. This matches my own computation and is the honest description.

**G4 (per-weight hypothesis) — CLOSED.** Hypothesis 6.1`(w,c)` is now parametrised, the `(0.810222, 0.38288)` instance is recorded, and the abstract, Theorem 1.2 and Theorem 6.2 all carry the qualifier. Theorem 6.2's final sentence now cites Hypothesis 6.1`(w,c)` rather than "the same computation".

Also noted: `code/big_restart.log` now records two batches of 500 restarts at floor `1e-7` returning `1.00007334` each. Table 6.1 still advertises "300-500 starts"; it could cite the 1000.

## Remaining, both cosmetic

**M1 [MINOR].** The abstract's last sentence still reads "the first theorem shows that it is the last one available to this family of arguments". It is the *second* ceiling theorem (Theorem 3.4) that gives `c**`; Theorem 3.1 gives only `0.383099`. Suggest "the ceiling theorems show".

**M2 [MINOR].** Lemma 5.5 still says "no admissible `eta` makes the right-hand side exceed `C`" without quantifying over `E_mu h(X)`. Strictly this is false as `E -> 0`, which is precisely the content of the `eps_0 ~ 1e-30000` discussion three pages later. Add "for `E_mu h(X)` above `10^-30000`", or "for any entropy the computation can reach".

No ERROR and no GAP remains.

## Overall assessment

Over four passes I checked every proof in the manuscript line by line and recomputed every numerical constant independently, and I now believe the mathematics is correct as stated. The unconditional content is Theorems 3.1 and 3.4 with Lemmas 3.3, 4.2, 5.1, 5.3, 5.5 and Propositions 2.3 and 4.3: two explicit adversarial families that cap the whole single-letter framework at `0.383099` in general and at `c** = 0.382885260` for certificates built the way the literature builds them. I reproduced `c**`, `w**`, `x**`, both ceiling constants, Liu's optimum to thirteen digits, Cambie's sharpness identity, the maximal-correlation rate of the hiding coupling, and both entries of the certification table; the inertia hypothesis survived eleven grid refinements including ones packed at the kernel's vertical tangent, and my own independent four- and five-atom adversary searches found nothing below the claimed minima. The positive result, `c_0 >= 0.38284`, is conditional on two numerical hypotheses, and the paper says so in the abstract, in the informal statement, in the theorem, in the history table and in the discussion. The honesty is now genuinely good: the paper states which of its own earlier numbers were wrong and why, quantifies the one window that neither its computation nor its analysis reaches rather than glossing it, is explicit that its cardinality reduction is a larger leap beyond the proved regime than Liu's was, and does not claim the ceiling for certificates outside the class it actually analyses. Its central claim, that the single-letter method as used since 2022 is exhausted at `0.382885`, is proved; its secondary claim, that the last `1.8e-4` is reachable, rests on numerics of the same character as the record it improves, and is presented as such.
