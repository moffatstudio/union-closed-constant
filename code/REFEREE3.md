# Referee report, third pass: `paper/paper.tex`

Recomputed independently in this directory (`chk3.py`, plus the scripts from passes 1 and 2).

## Round-two items: all three closed

**E1 (Lemma 5.5's constant off by `w`) — CLOSED.** The `1.048` instance is gone. Lemma 5.5 now states only `liminf R >= 2w(1-c)` and says explicitly that, since `kappa(eta) < 1` and the margin `2w(1-c) - C` is only `2.3e-5`, no admissible `eta` makes the right-hand side exceed `C`. That is the correct diagnosis. The `liminf` is a valid consequence: each `eta` gives a lower bound whose limit is `2w kappa(eta)(1-c-eta)`, and the supremum over `eta` of those limits is `2w(1-c)`.

The new slack remark checks out. `(t+t') h(t/(t+t')) <= 2 sqrt(tt')` follows from `h(lambda) <= 2 sqrt(lambda(1-lambda))`, which I tested at 200,000 points with no violation, and which gives `(t+t') * 2 sqrt(lambda(1-lambda)) = 2 sqrt(tt')` exactly. So the diagnosis of where Claim 2 loses is right, and it is the right place to attack.

**E2 (small-entropy region uncovered) — CLOSED structurally.** Hypothesis 6.2 now carries no floor: it covers all four-atom laws with `int h dmu > 0` and states `R >= C = 1.00005` on that set. Theorem 6.3's proof no longer invokes any numerical instance of Lemma 5.5; its case analysis (`int h dmu' = 0` trivial, `> 0` by hypothesis) is complete, and the reduction direction is used correctly (`Phi_C(original) >= Phi_C(reduced) >= 0`). The proof is airtight given the two hypotheses.

**E3 ((D) invalid where `p > 1`) — CLOSED.** (D) now carries `h(x) <= w h(x^2) + 1 - w`, which is exactly `p in (0,1]`, and `G` minimises over `X_c`. I recomputed: the smallest admissible `x` is `0.6124947` (the paper's `0.6125`), and the root of `c = G(c)` over the restricted domain is `0.38288525997`, unchanged to 11 digits.

---

## Remaining GAPs

### G1 [GAP, small] The fixed-point argument's monotonicity no longer follows from the reason given

The proof still argues "since `w_0` is increasing in `c`, `G` is decreasing in `c`". With a fixed domain that was immediate. Now the domain `X_c` also depends on `c`, and it *shrinks* as `c` grows, which pushes the minimum *up*. The two effects oppose, so decreasingness does not follow from the displayed reason.

It is nonetheless true, and the repair is one sentence. I computed `G` over the restricted and the unrestricted domain at `c = 0.20, 0.30, 0.36, 0.38, 0.3828, 0.382885, 0.39, 0.42, 0.45`: the two agree exactly at every value, with minimiser drifting only from `0.6981` to `0.6789`. The constraint defining `X_c` is inactive at the minimiser throughout. Add: "for `c` in the range of interest, `X_c` contains a fixed neighbourhood of the minimiser, so the minimum is unchanged by the restriction and the previous argument applies".

### G2 [GAP] Hypothesis 6.2's value is misstated at the printed `w`, and this is now the load-bearing statement

The hypothesis says the infimum "is `1.0000733`, attained at the two-point law". At `w = 0.810222`, the value printed throughout the paper, the hiding family's limit is

```
2w(1-c) = 1.00007322   <   two-point minimum = 1.00007334
```

so the infimum over the stated set is `1.0000732`, it is **approached and not attained**, and the two-point law is not the minimiser. (At the exact `w** = 0.8102220991` the two coincide to ten digits, by construction; the discrepancy is an artefact of printing `w` to six places. The repository's own hiding table already shows `1.00007328` at `delta = 1e-6`, below the two-point `1.00007334`.)

Nothing downstream breaks, since both numbers exceed `C = 1.00005`. But with the floor removed, this hypothesis is what the whole positive result rests on, so it should be exact. Suggested wording: "the infimum is `2w(1-c) = 1.0000732`, approached along the hiding family and not attained; the minimum over laws with `int h dmu >= 1e-7` is `1.0000733`, attained at the two-point law of Table 6.1. In particular `R >= C = 1.00005` on the whole set."

### G3 [GAP] The unbridged window should be quantified, and Lemma 5.5 proves more than the paper claims

Lemma 5.5 plus a contradiction argument actually **proves the existence** of `eps_0 > 0` with `R >= C` on `{0 < int h dmu <= eps_0}`: if not, there is a sequence with `E_n -> 0` and `R_n < C`, contradicting `liminf R_n >= 2w(1-c) = 1.0000732 > C`. So Hypothesis 6.2 is needed only on `(eps_0, 1e-7)`, not on all of `(0, 1e-7)`. That is worth stating, and it strengthens the paper.

The catch is that `eps_0` is non-effective, and the lemma's own rate makes it astronomically small: beating `C` needs `kappa(eta) > C/(2w(1-c)) = 0.9999768`, i.e. `2/log2(1/eta) < 2.3e-5`, i.e. `eta < 2^-86000`, and then `E/h(eta) < 1.4e-5` forces `E` below roughly `10^-30000`. Numerically, `max_eta` of the bound is `0.893` at `E = 1e-7`, `0.942` at `1e-12`, `0.978` at `1e-30`, `0.994` at `1e-100`.

So the honest three-way description is: **proved** for entropy below about `10^-30000` (non-effectively, via the liminf), **computed** for entropy at or above `1e-7`, **hypothesised** in the window between. The current text ("the one part of the hypothesis that the computation cannot exhaust, because the infimum there is approached rather than attained") is accurate but leaves the reader thinking the window is a sliver. It is not.

### G4 [GAP, carried over] "Every `c < c**`" is not covered by the stated hypotheses

Hypothesis 6.2 is stated only at `(w, c) = (0.810222, 0.38284)`. The final sentence of Theorem 6.3, Theorem 1.2, and the abstract all claim every `c < c**`, which needs the analogous hypothesis at each `w` in the interval supplied by Proposition 4.3(c). Write "under the corresponding hypothesis for each such `w`", or restrict the headline claim to the two values actually computed.

### G5 [MINOR, carried over] Abstract attribution

"the first theorem shows that it is the last one available to this family of arguments": it is the *second* ceiling theorem (Theorem 3.4) that gives `c**`; Theorem 3.1 gives only `0.383099`. And "this family" means certificates that use the i.i.d. protocol with its singleton class and whose other classes admit hiding. The Discussion's phrasing is the defensible one; the abstract should match it.

### G6 [MINOR] One over-strong sentence in Lemma 5.5

"no admissible `eta` makes the right-hand side exceed `C`" is true for every entropy the computation can reach, but not for all `E`: as `E -> 0` the supremum over `eta` tends to `2w(1-c) > C`. Add the quantifier, e.g. "for any `E_mu h(X)` above `10^-30000`".

---

## Independent corroboration this pass

I re-ran my own adversary search (independent parametrisation, Powell, 120 restarts per cell, four and five atoms per component). Nothing below the claimed minima: best `1.00654` and `1.00517` at `c = 0.38284`, `1.00191` and `1.00014` at `c = 0.38288`. The five-atom run at `c = 0.38288` converged to a hiding-shaped law (`q = 0.366`, one component `0.974 delta_1 + 0.026 delta_0`, the other `delta_{0.0002}`) at `1.000143`, sitting above the claimed infimum as it should. The four-atom run at `c = 0.38288` converged to the two-point structure. Both binding families are reproduced independently.

---

## Assessment: does the paper state honestly what is proved and what is numerical?

Yes, with the three qualifications above. The division of labour is now correct and clearly signposted: Theorems 3.1 and 3.4 (the two ceilings), Lemmas 3.3, 4.2, 5.1, 5.3 and Proposition 4.3 are unconditional and I have checked every step of them; Proposition 5.4 is unconditional given Hypothesis 5.6; Theorem 6.3 is explicitly conditional on Hypotheses 5.6 and 6.2, and the text says so in the abstract, in the informal Theorem 1.2, in the statement, and in Table 1.1. The comparison to Liu is fair rather than flattering: the paper states that its cardinality reduction needs two functionals where Liu needed one, that Liu's kernel is smooth and within a perturbative regime his Lemma 11 covers while `f_ideal` is not, and that a first uncorrected computation of its own produced values now refuted by (H). The one place where the presentation is still more comfortable than the mathematics is the small-entropy window (G2, G3): Hypothesis 6.2 was widened to swallow a region that the numerics do not reach and that the analysis reaches only about `10^-30000` below it, and a reader should be told the size of that window rather than only that it exists. Fix G1 through G4 and I would consider the manuscript's claims accurately stated.
