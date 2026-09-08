# Referee report, second pass: `paper/paper.tex`

Scope: the full 11-page manuscript, read against Liu (arXiv:2306.08824) and the Yu/Cambie synthesis. Everything numerical below was recomputed independently (`lem55.py`, `chk2.py`, plus the first-pass scripts in this directory).

**Summary.** The round-one defects are fixed correctly, and the new structural material (Lemma 5.1, Lemma 5.3, Proposition 5.4, Theorem 6.2's case analysis) is sound. Lemma 5.5's *proof* is correct in every inequality. But its *numerical instance* is wrong by the factor `w`, and with the correct value the lemma cannot cover the small-entropy region for any choice of `eta`. That reopens the gap it was written to close, and Theorem 6.2's proof does not currently close.

---

## Verified fixed since the first pass

| first-pass finding | status |
|---|---|
| B1 hiding definition too weak | fixed: Definition 3.2 now requires `P(y,y) <= delta^2`, and Lemma 3.3 exhibits a coupling meeting it for each class. The maximal-correlation coupling is now given explicitly with `r_1 = p_1`, `r_0 = p_0 - p_y`; I checked its marginals and symmetry algebraically and its second singular value numerically (`0.081, 0.025, 0.0079, 0.00079` at `delta = 1e-2 .. 1e-6`), matching Appendix A. |
| B3 `x^2 + f(x)^2 = x` | fixed: Lemma 4.2 now has `2x^2 <= 1/2`. |
| B4 Liu's diagonal `< 1/2` | fixed: Remark 3.5(ii) now says the diagonal is not `1/2` at the binding point and gives `0.5228`. Both numbers check. |
| B6 singleton iid class | fixed: Theorem 3.4 names `{mu (x) mu}`. |
| B9 monotonicity of `G` | fixed: `G` decreasing, `c - G(c)` strictly increasing, unique root. Correct as now written. |
| B16 broken table | fixed: the table compiles. |
| B17 stale `beta = 0.19` | gone: the paper uses `w = 0.810222` throughout. |
| B10, B12, B13, B15 | addressed in the text (optimal diagonal now claimed only where it holds; Remark 6.4 states the two-functional price; Cambie's mixture is described correctly). |

Appendix A checks exactly: `h(x**) = 0.892123`, `h(x**^2) = 0.998520`, `c_2(0.899947) = 0.382752` at `x = 0.6807`, `c_2(0.85) = 0.382841`, `c_2(w**) = 0.382885`, and `(H)` at `c = 0.38284` reads `w >= 0.8101627`.

---

## E1 [ERROR] Lemma 5.5's numerical instance is wrong by the factor `w`

The lemma's bound is on the **weighted** ratio `R`, and reads `R >= 2 w kappa(eta) (1 - c - eta - E/h(eta))`. The stated instance is

> for `w = 0.810222` and `c = 0.38284`, taking `eta = 1e-4` gives a ratio of at least `1.048` whenever `E <= 1e-7`

and the proof's last line computes `2 * 0.810222 * kappa(1e-4) * (1 - 0.38284 - 1e-4 - 1e-7/h(1e-4)) = 1.0481`. That arithmetic is not what the expression evaluates to:

```
kappa(1e-4) = (1 - 1e-4)(1 - 2/log2(1e4)) = 0.8494001
h(1e-4)     = 0.00147303
2*w*kappa*(1 - c - eta - E/h(eta)) = 1.620444 * 0.8494001 * 0.6170421 = 0.8492312
```

The source of the slip is visible in the repository: `code/small_entropy_lemma.py` line 1 of its output computes `2 * kappa(1e-4) * (1 - c - 1e-4 - 1e-7/hb(1e-4))`, with **no `w`**, and that is `1.0483`. So `1.048` bounds the pure i.i.d. ratio `E h(XY) / E h(X)`, not `R`. Since `R >= w * (i.i.d. ratio)`, the correct figure is `0.8492`.

## E2 [ERROR/GAP, consequence] No choice of `eta` makes Lemma 5.5 exceed 1, so Theorem 6.2's second case fails

This is not a matter of picking a better `eta`. The bound is bounded above by `2w(1-c) kappa(eta) <= 1.000073 * kappa(eta)`, so beating `C = 1.00005` requires

```
kappa(eta) > 1.00005/1.000073 = 0.999977   =>   2/log2(1/eta) < 2.3e-5   =>   eta < 2^-87000,
```

at which point `E/h(eta)` with `E = 1e-7` is astronomically large. Maximising the bound over `eta` numerically at the paper's own threshold gives

| `E` | `max_eta` of the bound | at `eta` |
|---|---|---|
| `1e-7` | 0.89295 | 8.9e-7 |
| `1e-12` | 0.94175 | 1.8e-11 |
| `1e-30` | 0.97846 | 5.0e-29 |
| `1e-100` | 0.99389 | 1.8e-98 |

The bound reaches `2w(1-c) = 1.000073` only in the double limit `eta -> 0`, `E -> 0`; it is a liminf statement, not a uniform bound on a region of positive threshold. Consequently the step in the proof of Theorem 6.2 that reads "If `0 < int h dmu < 1e-7`, Lemma 5.5 gives `R >= 1.048 > C`" is false, and the region `0 < int h dmu < 1e-7` is not covered by anything. This is exactly the gap flagged as B2 in the first pass; it is not yet closed. It is worse for the final sentence of Theorem 6.2, where `c -> c**` drives the available margin `2w(1-c) - C` to zero.

**Where the loss is, and how it might be repaired.** The `kappa` factor comes from Claim 2, applied to all pairs in `T x T`. But on the pair that actually matters, `(y, 1)` with `y = 1 - t` also in `T`, the true inequality is an identity: `h(x * 1) = h(x) = h(x) + h(1)`, no loss at all. Claim 2 is lossy precisely when both `t` and `t'` are comparable, and its slack term is `2(t + t')` where the sharper truth is proportional to `min(t, t')` (the discarded term is `-(t+t') h(t/(t+t'))`, which is small when the ratio is near 0 or 1). Three routes, in order of my preference:

1. Sharpen Claim 2 so the `T x T` loss scales with `min(t, t')` rather than `t + t'`; then a law whose entropy sits on a single `T`-atom paired against `x = 1` pays nothing, and the surviving loss is second order in the entropy-carrying mass.
2. Do not discard the kernel term. For `x >= 1/sqrt2`, `f(x) = 0`, so on `T x T` pairs the `Pi^id` integrand *equals* the i.i.d. one; the weighted ratio there is the full `h(x^2)/h(x)`, not `w` times it. Concretely, for `mu = p delta_{1-t} + (1-p) delta_0` with `p = (1-c)/(1-t)` the true `R` is `p h(x^2)/h(x) = 1.192` while the lemma's bound gives `0.928`. Splitting the estimate by whether the entropy sits in `L` or in `T` should recover the missing factor.
3. Failing both, fold the region into Hypothesis 6.2 (state the hypothesis for all `int h dmu > 0`) and say plainly that the degenerate regime is numerical rather than proved. That is honest and arguably still at Liu's level, since Liu's own 9-dimensional minimisation had no entropy floor and his Lemma 7 is used only in the qualitative Theorem 6. But it must not be presented as covered "unconditionally".

## E3 [GAP] The proof of (D) is invalid on part of the stated range `x` in `[1/2, 1/sqrt2]`

The proof sets `p := h(x)/(w h(x^2) + 1 - w)` and treats `p delta_x + (1-p) delta_0` as a law. That needs `p <= 1`. At `w = 0.810222` this fails for `x < 0.6125`: `p(0.5) = 1.1805`, `p(0.55) = 1.0954`, `p(0.6) = 1.0182`. So (D) is unproved for `x` in `[1/2, 0.6125)`.

Non-binding, and the fix is one clause: the minimiser is `x** = 0.6909`, where `p = 0.8932`, and restricting the range to `{x : p <= 1}` (equivalently `x >= 1-c`, since `E_mu[X] = px >= 1-c` forces `x >= 1-c = 0.617`) leaves `G(c)` and `c** = 0.382885260` unchanged to 12 digits. I verified the minimum over `[1/2, 1/sqrt2]` and over `[1-c, 1/sqrt2]` agree. State (D) for `x` in `[1-c, 1/sqrt2]`.

---

## Verified correct in the new material

**Lemma 5.5's proof, inequality by inequality.** All of it checks.
- `m <= E/h(eta)`: `h >= h(eta)` on `M` by concavity and symmetry of `h`. Correct.
- `a >= 1 - c - eta - m` from `E_mu[X] <= eta mu(L) + m + a`. Correct.
- Claim 1, case `x <= 1/2`: `h(theta x) >= theta h(x)` for concave `h` with `h(0) = 0`, `xx' >= (1-eta)x`, `h` increasing on `[0,1/2]`. Correct.
- Claim 1, case `x > 1/2`, `xx' >= 1/2`: `h` decreasing on `[1/2,1]` and `xx' <= x`. Correct.
- Claim 1, case `x > 1/2`, `xx' < 1/2`: needs `h(1/2 - eta/2) >= 1 - eta` for `eta <= 1/4`; true, and I checked it (`0.9544 >= 0.75` at `eta = 1/4`, `0.99993 >= 0.99` at `eta = 0.01`).
- Claim 2: `s = t + t' - tt' >= (1-eta)(t+t')` since `tt'/(t+t') <= min(t,t') <= eta`; `s <= 2eta <= 1/2`. The identity `h(t+t') - h(t) - h(t') = -(t+t') h(t/(t+t')) + [phi(t) + phi(t') - phi(t+t')]` with `phi(u) = (1-u)log2(1-u)` is correct as written. `-(t+t')h(.) >= -(t+t')` since `h <= 1`. The bracket is `>= -tt'/((1-2eta) ln 2)` by the two-dimensional Taylor bound `phi(t+t') - phi(t) - phi(t') = int int phi''(u+v) <= tt' max phi''`, with `phi'' = 1/((1-u) ln 2)`. And `tt'/((1-2eta) ln 2) <= 2tt'/ln2 <= 2 eta (t+t')/ln 2 = 0.721(t+t') <= (t+t')` for `eta <= 1/4`. Then `h(t) >= t log2(1/t) >= t log2(1/eta)` gives `2(t+t') <= (2/log2(1/eta))(h(t)+h(t'))`. All correct.
- The assembly `>= 2 a kappa int_T h + 2 a (1-eta) int_{T^c} h >= 2 a kappa E`, using `kappa <= 1 - eta`. Correct.

One cosmetic point: at `eta = 1/4` exactly, `kappa = 0` and the lemma is vacuous; the range should be written `(0, 1/4)`.

**Proposition 5.4 and Lemma 5.3.** Sound. `Phi_C` is jointly concave on `M_0 x M_1` (concave functions of separate variables, plus a concave functional of the affine map `(P_0,P_1) -> mu` whose image lies in a fixed-mean slice, plus a linear term); all integrands are continuous on `[0,1]^2`, so `Phi_C` is weakly continuous and `M_0 x M_1` is weakly compact; Bauer's minimum principle applies; extreme points of a product are pairs of extreme points; Lemma 5.1 with `r = 3` gives at most four atoms each. Fixing `int x dP_j` for both `j` does fix `E_mu[X]`, so the mean constraint is respected, and every pair lies in some product of slices. The reduction direction in Theorem 6.2 is used correctly (`Phi_C(original) >= Phi_C(reduced) >= 0`). The AHS hypothesis needed for the i.i.d. term is exactly `iint h(xy) dnu dnu <= 0` on `{int dnu = int x dnu = 0}`, which I confirmed numerically has zero positive eigenvalues at `n = 200..1600`.

**Hypothesis 6.1.** Independently confirmed and strengthened: I recomputed the projected inertia on uniform grids (`n = 200 .. 3200`) and on grids with 2500-3000 extra points packed into windows of half-width down to `1e-5` around `1/sqrt2`, where `f` has a vertical tangent. Exactly two positive directions in all eleven runs, stable at `9.25e-7` and `2.078e-2`, with the third eigenvalue at `1.4e-13`. The "six orders of magnitude" separation is accurate (`9.25e-7` versus `1.4e-13` is nearly seven).

**Proposition 4.3.** (a) is right and is an improvement on the earlier draft: on `mu = p delta_x + (1-p) delta_0` the `Pi^id` term charges only the pair `(x,x)`, since `f(0) = 0`, and its mass is `>= p^2` by Cauchy-Schwarz with equality at the product law. (b) and (c) are correct; the monotonicity argument in (c) (take `w` strictly between `w_0(c)` and `w_0(c**)`) is valid.

**Theorem 3.4, Lemma 3.3, Theorem 3.1, Lemma 4.2, Proposition 2.3.** All correct as now stated, modulo E3.

---

## Minor

**M1.** Abstract: "the first theorem shows that it is the last one available to this family of arguments". It is the *second* ceiling theorem (Theorem 3.4) that gives `c**`; Theorem 3.1 gives only `0.383099`. And "this family" means, precisely, certificates that use the i.i.d. protocol with its singleton class and whose other classes admit hiding. A certificate mixing the i.i.d. protocol with a hypothetical class that admits neither hiding nor a classification is not excluded, since no such classification is proved. The Discussion's "in every form used since 2022" is the defensible wording; the abstract should match it.

**M2.** Section 6 says the optimiser was run with floors down to `1e-7` and "below `1e-7`, Lemma 5.5 gives `R >= 1.048` unconditionally". Both halves of that sentence need revising per E1/E2.

**M3.** Remark 6.4's disclosure of the withdrawn `0.38295` values is good practice and should be kept.

**M4.** The Acknowledgements say the manuscript was checked "by an agent instructed to referee" it. If that refers to this report, the reader should be told that the referee pass found errors that were then corrected, rather than being left to infer that the check was clean.
