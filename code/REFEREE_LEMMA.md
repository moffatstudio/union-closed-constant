# Referee report: the sharp small-entropy lemma (`C:\tmp\lemma\LEMMA_SMALL_ENTROPY.md`)

**Verdict: the lemma is correct.** I checked every inequality analytically and re-verified every constant and every monotonicity claim independently, including a 50-digit recomputation and an adversarial search designed to break the main bound. I found no error. There is one substantive gap, and it concerns reach in `c`, not the mathematics.

---

## A. Step-by-step verification

**Lemma 1** `h(theta u) >= theta h(u)`. Concavity with `h(0) = 0`. Correct.

**Lemma 2** `h(a) <= 2 sqrt(a(1-a))`. Both branches check.
- (i) `h'' = -1/(p(1-p) ln2) <= -4/ln2` since `p(1-p) <= 1/4`, so Taylor at `1/2` with Lagrange remainder gives `h(1/2-u) <= 1 - 2u^2/ln2`. Squaring is legitimate (both sides positive on the range used), and `1-4u^2 >= 1 - 5.77078u^2 + 8.325475u^4` reduces to `u^2 <= 1.77078/8.325475 = 0.212695`, i.e. `u <= 0.4611888`, i.e. `a >= 0.038811`. The paper's `0.038813` is on the safe side of that.
- (ii) On `a < 0.038813`, `psi(a) <= a/ln2` from `(1-a)ln(1/(1-a)) <= a`. The derivative of `sqrt(a)(log2(1/a)+1/ln2)` is `(log2(1/a) - 1/ln2)/(2 sqrt a)`, positive for `a < 2^(-1/ln2) = 0.3679`, so the endpoint value `1.20767` is the max, against `2 sqrt(a(1-a)) >= 1.96079 sqrt(a)`. Correct.
- Grid check over 4,000,001 points: `max (h(a) - 2 sqrt(a(1-a))) = 0.0`, attained at `a = 1/2`.

**Lemma 3** `u Ltil(u) <= h(u)`. Reduces to `ln(1/(1-u)) >= u`. Correct. `Ltil' = -1/(u ln2) - 1/ln2 < 0`, so `Ltil` is decreasing. Correct.

**Lemma 4** `Lambda = tau h(gamma) + (A+B) h(alpha)`. The information-theoretic derivation is right: `Lambda = H(X,Y) - H(XY) = H(X,Y | XY)`, the conditional law given `XY = 0` is `(tt', A, B)/tau`, the chain rule gives `h(gamma) + (1-gamma)h(alpha)`, and `tau(1-gamma) = A+B`. I verified the identity numerically on a 1400x1400 log-grid on `(1e-16, t_0]^2`: max absolute discrepancy `5.5e-15`, which is the float noise of the naive form, not of the identity.

**Lemma 5** `Lambda <= 2 sqrt(tt') + tt'(Ltil(m) + 1 + m/ln2)`. Both halves check. `(A+B)h(alpha) <= 2 sqrt(AB) = 2 sqrt(tt'(1-t)(1-t')) <= 2 sqrt(tt')`. For the first half, `tau gamma = tt'`, `log2(1/gamma) = log2(tau/(tt')) <= log2(1/t + 1/t') <= 1 + log2(1/m)`, and `tau psi(gamma) <= tt'/ln2`; the regrouping `log2(1/m) + 1 + 1/ln2 = Ltil(m) + 1 + m/ln2` is an identity. Correct.

**Lemma 6** (the key inequality) `w Lambda <= (1-w) sqrt(h(t)h(t'))` on `[0,t_0]^2`. The reduction to `Phi(t_0) <= r` is valid:
- `sqrt(h(t)h(t')) >= sqrt(mM Ltil(m)Ltil(M))` by Lemma 3.
- First term `2/sqrt(Ltil(m)Ltil(M)) <= 2/Ltil_0` since `Ltil` is decreasing and `m, M <= t_0`.
- `g(m,M)` increasing in `M`: `sqrt(M)/sqrt(Ltil(M))` is increasing. Correct.
- `g` increasing in `m`: the `m`-factor is `sqrt(m Ltil(m)) + sqrt(m)(1+m/ln2)/sqrt(Ltil(m))`. I confirmed `d/dm[m Ltil(m)] = log2(1/m) - 2m/ln2`, whose minimum on `(0, t_0]` is `7.3635 > 0`; the second summand is a product of positive increasing factors. Both monotonicity claims verified numerically on 200,000 log-spaced points.
- The constants, at 50 digits: `Ltil_0 = 8.81486065458456049`, `Phi(t_0) = 0.233576137120005`, `r = 0.234229630891286586`, so `Phi <= r` with slack `6.535e-4`. Correct.

**Lemma 7** `K_min >= (int_N sqrt h dmu)^2`. Correct. `h(xy + f(x)f(y)) >= h(xy)`, and in fact `f = 0` on `N` since `1 - t_0 > 1/sqrt2`, so that step is an equality here. `1 - xy = t_x + t_y - t_x t_y` lies in `[max(t_x,t_y), 2t_0] subset [0,1/2]`, where `h` is increasing, giving `h(xy) >= h(max) >= sqrt(h(t_x)h(t_y))`. Jensen on `s -> s^2` across components is applied correctly, and holds for every decomposition hence for the infimum. Using the infimum over *all* decompositions (rather than Liu's two-component form) is conservative in the right direction.

**Lemma 8** `int_B y dmu <= rho int_B h dmu`. `h(y)/y` is decreasing, so `y/h(y)` is increasing and maximised at `y = 1-t_0`, giving `rho = (1-t_0)/h(t_0)`. Numerically `max y/h(y) = 18.78481509471591` on a 3,000,000-point grid, against `rho = 18.78481509471592`. Correct and exactly attained.

**Main proof (a)-(e).** All correct.
- (a) `h(xy) >= x h(y)` by Lemma 1 with `theta = x`; the factor `2` for `N x B` and `B x N` is right.
- (b) is an identity, `2 sigma E_N - iint_{NxN} Lambda`.
- (c) The `B x B` part of `I` is dropped (non-negative) and the `N x N` integrand becomes `(1-w) sqrt(h h) - w Lambda >= 0` by Lemma 6, since `x, y in N` forces `t_x, t_y in [0, t_0)`. Then `sigma >= S` gives `2w(sigma E_N + S E_B) >= 2wSE`.
- (d) `S >= (1-c) - rho E` from the mean constraint.
- (e) `R >= 2wS >= 2w[(1-c) - rho E]`, and this exceeds `C` exactly when `E <= G/rho`.

**Constants**, all reproduced at 50 digits: `r`, `Ltil_0`, `h(t_0)`, `rho`, `Phi(t_0)`, `2w(1-c) = 1.00007321904`, `G = 1.4328813584425e-5`, `eps_0 = 7.62787044332e-7`.

**Does it hold for all `mu`, not just small-entropy ones?** Yes. No step uses `E` small; the bound `R >= 2w[(1-c) - rho E]` is simply vacuous once `E > (1-c)/rho = 0.0329`. The doc's "threshold-free" claim is justified.

**Adversarial test.** I searched 7,738 laws (structured hiding families with `y` spanning `1e-12` to `0.999` including the `1-t_0` boundary, four-atom families with an extra near-`1` atom at `t = 1e-9 .. 0.05` straddling `t_0`, and random multi-atom laws with masses down to `1e-9`), computing `K` as a minimum over up to three-group partitions, which is an *upper* bound on `K_min` and hence gives an upper bound on `R`. Minimum of `R - 2w[(1-c) - rho E]` over all of them: `-2.2e-16`, i.e. zero to machine precision, attained on the hiding family as `E -> 0` where both sides equal `2w(1-c) = 1.0000732190`. No violation anywhere, and the bound is exactly tight on the family that matters.

---

## B. GAP: the lemma closes the window at `c = 0.38284` and `c = 0.38288`, but not up to `c**`

`eps_0 = [2w(1-c) - C]/(2 w rho)`, and since the admissible weight satisfies `w < w_0(c**)`, the numerator is at most `(1-c)/(1-c**) - 1`. Requiring `eps_0` to reach the numerical floor `1e-7` therefore forces

```
c  <=  c** - (1-c**) * 2 w rho * 1e-7  =  0.3828834      (c** - 1.88e-6)
```

Computed sup of `eps_0` (taking `C -> 1`, the most generous choice):

| `c` | `sup 2w(1-c)` | `sup eps_0` | reaches `1e-7`? |
|---|---|---|---|
| 0.38284 | 1.00007334 | 2.41e-6 | yes (7.63e-7 at the paper's `C = 1.00005`) |
| 0.38288 | 1.00000852 | 2.80e-7 | yes |
| 0.382884 | 1.00000204 | 6.71e-8 | **no** |
| 0.382885 | 1.00000042 | 1.38e-8 | **no** |

So the paper's two computed instances are fully closed, and Hypothesis 6.1's small-entropy window genuinely disappears at `c = 0.38284` and `c = 0.38288`. But for `c` within about `1.9e-6` of `c**` a window `[eps_0(c), 1e-7]` reopens and shrinks to nothing as `c -> c**`. This is intrinsic to any bound of the form `R >= 2w(1-c) - kappa E` with `kappa > 0`, because the margin `2w(1-c) - C` vanishes as `c -> c**`; lowering the numerical floor cannot fix it either, since the required floor also goes to zero. Closing it would need a bound with no linear term, i.e. `R >= 2w(1-c)` outright for `E` below a fixed threshold, which the numerics (mine and the author's) suggest is the truth: the infimum of `R` appears to be exactly `2w(1-c)`, approached only in the hiding limit.

**Consequence for the paper.** Theorem 6.2's first claim (`c = 0.38284`, `C = 1.00005`) becomes unconditional in the small-entropy regime, so Hypothesis 6.1 reduces to the four-atom global-minimum statement on `int h dmu >= 1e-7` alone. That is a real strengthening, and it does make the certificate more rigorous than Liu's, whose degenerate regime rests on a liminf. The "every `c < c**`" statement should say that the small-entropy regime is proved for `c <= c** - 1.9e-6` and remains hypothesised on a shrinking window above that.

---

## C. Minor notes, no action required on the mathematics

**N1.** Anyone re-verifying `(*)` numerically must use the Lemma 4 identity, not the definition `h(t)+h(t')-h((1-t)(1-t'))`. My first pass used the subtraction and got a spurious maximum of `2.78` at `t = t' = 1.6e-16`, pure catastrophic cancellation. With the identity the maximum is `0.990894`, attained at the corner `(t_0, t_0)`, confirmed at 60 digits. The doc already flags this in its table; it is worth putting the warning next to the lemma itself.

**N2.** Lemma 6 constrains the weight: `Phi(t_0) <= (1-w)/w` requires `w <= 1/(1+Phi) = 0.8106512`. Every admissible weight in the paper is at most `w** = 0.8102221`, so the lemma holds across the whole range of `w` used by Hypothesis 6.1`(w,c)`. Worth stating, since it means the lemma need not be re-derived per weight.

**N3.** The doc's headline statement carries the hypothesis `0 < E <= eps_0`, but the content is the threshold-free inequality. State the inequality as the theorem and the threshold as a corollary.

**N4.** The suggested route to a larger `eps_0` (exploiting that middle mass also feeds the cross terms with the atom at `1`, which the proof banks once but not twice) looks right to me, and is the same mechanism that would remove the linear term entirely.
