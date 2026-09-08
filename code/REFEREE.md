# Referee report

**Paper:** "The ceiling of the single-letter entropy method for the union-closed sets conjecture, and a protocol that reaches it" (`paper/note.tex`), with `CEILING_THEOREM.md` and `RESULT.md`.

**Basis:** independent adversarial reading against `literature/2306.08824_liu.md` (Liu) and `literature/SYNTHESIS_lane2.md` (Yu/Cambie). Every numerical claim below was recomputed from scratch in this directory (`ref_check.py`, `cstar.py`, `liu_check.py`, `liu_repro.py`, `maxcorr.py`, `inertia.py`, `inertia2.py`, `adv.py`), not read off the repository's logs.

**Verdict.** The two ceiling theorems are essentially correct and the arithmetic is right throughout. But the definition of "component hiding" is too weak to support the proof of (H) as written, the degenerate region of Hypothesis 2 is not covered by any argument, and two stated identities are false. Nothing I found breaks `c** = 0.382885260`; all defects look repairable.

---

## A. Verified correct (recomputed independently)

**A1 [OK]** `h(1/sqrt2) = 0.8724293398564682`, `c_ceil = 1 - h(1/sqrt2)/sqrt2 = 0.3830992976813883`. Matches the note to all printed digits.

**A2 [OK]** `c** = 0.382885259967`, `w = 0.810222099`, `x* = 0.690907739`, from an independent bisection of the (H)-(D) system. Matches `0.382885260 / 0.810222 / 0.690908`.

**A3 [OK]** The two-point ratio of Hypothesis 2 at `w = 0.810222099` is `1.00007334` at `c = 0.38284`, `1.00000852` at `c = 0.38288`, and exactly `1.00000000` at `c = c**`, with minimiser `x = 0.690905` in all three cases. Those are the certification table's numbers to every printed digit.

**A4 [OK]** Liu's optimum reproduces: at `p* = 0.893604513905457`, `x* = 0.690787593924988`, `w = 1 - beta* = 0.899947`, the ratio is `1 - 9.3e-15`, and `1 - p* x* = 0.382709087918741`. The `0.382752` value of (D) at Liu's weight, and the "kernel-neutral point" `0.690787593924988` (root of `x^2 + x^2(1-x)^2 = 1 - x^2`), are both correct.

**A5 [OK]** Sawin's protocol formula `Pi(0,0) = 1 - max{1-x, 1-y, min(2-x-y, 1/2)}` is the correct zero-probability form of the max-entropy coupling (checked against the Frechet clamp of 1/2 at several points).

**A6 [OK]** "Every class contains the product law" genuinely holds for all four literature pairs: iid (the class is literally `{mu (x) mu}`), Sawin (all symmetric couplings), Yu (products have maximal correlation `0 <= rho`), Liu's `C3` (a one-component mixture of products). Checked against Liu's own listing of `C1`, `C2`, `C3`.

**A7 [OK]** Theorem 1's two load-bearing claims. If `x = 0` the marginal forces `Pi_{x,y}(0,0) = 0` for every protocol, so `h = 0`; likewise `(1,1)` gives `Pi = 1`. And on `(x*,x*)` with `x* = 1/sqrt2`, `h(Pi(0,0)) <= 1 = h(x*^2)` holds trivially because `h <= 1` and `x*^2 = 1/2`. Both correct.

**A8 [OK]** The maximal-correlation hiding claim. For the explicit coupling described (product on `{0,1}`, the `y`-atom paired only with the `0`-atom) I formed the normalised joint matrix and took singular values. The second singular value is `0.0824, 0.0252, 0.00789, 0.000786` at `delta = 1e-2, 1e-3, 1e-4, 1e-6`: `rho_m = Theta(sqrt delta) -> 0`, exactly as claimed, rate included. It does need `rho > 0` strictly, which is the case for Yu's classes.

**A9 [OK]** The iid term's concavity, i.e. `nu -> int int h(xy) dnu dnu <= 0` on `{int dnu = 0, int x dnu = 0}`. Projected spectrum at `n = 200..1600`: zero positive eigenvalues above `1e-12` at every resolution. This is the AHS fact, used exactly as Liu uses it.

**A10 [OK]** Hypothesis 1 (inertia = 2) is well supported and is *not* an artifact of the kernel's singularity. `code/CONCAVITY_ideal.md` correctly locates the second positive direction in a narrow window straddling `1/sqrt2`, where `f_ideal` has a vertical tangent, so I re-ran the count on uniform grids (`n = 200, 400, 800, 1600, 3200`) and on non-uniform grids with 2500-3000 extra points packed into windows of half-width `2e-2, 5e-3, 1e-3, 2e-4, 1e-5` around `1/sqrt2`. The number of positive eigenvalues is exactly 2 in all eleven runs; the two are stable at `9.25e-7` and `2.078e-2`; the third sits at `1.4e-13`, the noise floor. No continuum of positive directions accumulates at the kink, and the codim-4 form is numerically PSD at Liu-comparable precision.

**A11 [OK]** The realizability and pointwise-domination half of Lemma 3. `f <= min(x,1-x)`, the Cauchy-Schwarz bound `xy + f(x)f(y) <= 1/2` when `f(x)f(y) > 0`, and hence `h(Pi^id) >= h(xy)`. The algebra `1/2 - x^2 <= (1-x)^2 <=> (2x-1)^2 >= 0` is right.

**A12 [OK]** The remark's account of why Cambie's `0.3823455` sits below `c**`. Cambie's extremal law is, in zero-probability coordinates, `0.92112 delta_{0.67055} + 0.07888 delta_0`, and his sharpness identity `(1-a)^2 h(2b-b^2) = (1-2a) = (1-a)h(b)` is precisely "the diagonal mass is cut from `p^2` to `2p-1`" (`1 - 2a* = 0.842246 = 2p - 1`). Consistent.

**A13 [OK]** The reading of Liu's Proposition 3 and Definition 1 is faithful to the source, including the "class must contain every induced joint law" clause and the direction of the mean constraint (`E_mu[S] <= c` in Liu equals `E_mu[X] >= 1-c` here).

**A14 [OK]** The hiding law's ratio does converge to `2w(1-c)` from above within Liu's class, and this can be *proved* rather than tabulated. Among mixtures of products with zero `(y,1)` mass, Cauchy-Schwarz forces `(y,y)`-mass `>= (1-q) delta^2`, attained by the stated hiding coupling, and the ratio is then `2wq + delta [w(1-q)h(y^2) + beta h(y^2 + f(y)^2)] / h(y) > 2wq`. Worth putting in the paper in place of the table's numerical row.

**A15 [OK, weak corroboration]** I ran my own four- and five-atom-per-component adversary search (`adv2.py`, independent parametrisation, Powell, 120 random restarts per cell) at `w = 0.810222`. It found nothing below the claimed minimum: best `1.00654` at `c = 0.38284` and `1.00191` at `c = 0.38288`, the latter converging to `q = 0`, `P0 = 0.889 delta_{0.693} + 0.111 delta_{~0}` - the two-point law's structure, at low precision. So the *shape* of the minimiser is independently corroborated, but note the corollary: my search failed to locate the known minimum's value to better than three digits, which shows how optimiser-dependent this landscape is and reinforces B13.

---

## B. Errors and gaps

### B1 [GAP] The definition of component hiding does not imply what the proof of (H) uses

The proof of (H) states: *"The `(y,y)` mass is `O(delta^2)` for every coupling."* This is **false**. The `y`-atom has marginal mass `(1-q)delta`, so the comonotone coupling puts `(1-q)delta` on `(y,y)`, which is order `delta`, not `delta^2`.

Because the certificate's left side is an *infimum* over the class, the proof only needs *one* coupling that is simultaneously hiding and has `o(delta)` mass on `(y,y)`. But Definition 5 requires only `P(X=y,Y=1) = P(X=1,Y=y) = 0` and says nothing about the diagonal. A class could contain a hiding coupling that dumps all the `y`-mass on `(y,y)`; that term then contributes `Theta(delta) h(Pi_{y,y}(0,0))` and the limit `2wq >= 1` does not follow.

**Fix, cheap and available.** Add `P(X=y,Y=y) = O(delta^2)` to Definition 5. All three literature classes still satisfy it with the couplings the note already writes down: all-couplings can send the whole `y`-mass to the other coordinate's `0`-atom, giving `(y,y)`-mass exactly 0; the maximal-correlation coupling as described has `(y,y)`-mass 0 by construction; Liu's `q delta_1 (x) delta_1 + (1-q) P_0 (x) P_0` gives `(1-q) delta^2`. Then delete the false sentence and say instead that the hiding coupling puts `O(delta^2)` on `(y,y)` and the iid term's product law puts `((1-q)delta)^2` there.

### B2 [GAP] The degenerate region `E_mu h(X) < 1e-3` is not covered by Hypothesis 2

Hypothesis 2 floors `E_mu h(X) >= 1e-3` and defers the rest to "the hiding laws, whose ratio is handled in closed form by (H)". But (H) concerns a **three-atom, two-parameter family** `mu_delta`. The excluded region contains every four-atom law of small entropy, not just that family, and nothing shows `mu_delta` is the worst of them. As written, the certification has a hole exactly where the binding constraint lives.

**Fix, and it upgrades the weakest step to Liu's own standard.** The `Pi^id` term is non-negative, so the ratio is at least `w` times the pure-iid ratio. Liu's Lemma 7 gives `liminf E_{mu (x) mu}[h(XY)] / E_mu[h(X)] >= 2(1-c)` for *every* sequence of laws converging weakly to the degenerate law `q delta_1 + (1-q) delta_0`. Since `E_mu h(X) -> 0` forces exactly that weak limit (compactness of the space of laws on `[0,1]`), one gets `liminf ratio >= 2w(1-c) = 1.000073 > 1` uniformly on a neighbourhood of the degenerate law, and the numerical search need only cover the complement. One paragraph.

### B3 [ERROR] Lemma 3's proof asserts `x^2 + f(x)^2 = x` on `[0,1/2]`; it is `2x^2`

On `[0,1/2]`, `f(x) = min(x,1-x) = x`, so `x^2 + f(x)^2 = 2x^2`. (Getting `x` would need `f = sqrt(x(1-x))`, which violates `f <= min(x,1-x)` for `x < 1/2` and is not realizable.) The conclusion is untouched: `2x^2 <= 1/2` on `[0,1/2]` is exactly what the Cauchy-Schwarz step needs. Replace "`= x` on `[0,1/2]`" with "`= 2x^2 <= 1/2` on `[0,1/2]`".

### B4 [ERROR] The claim that Liu's kernel has diagonal `x^2 + x^2(1-x)^2 < 1/2` is false

At the binding point `x = 0.6908` the diagonal is `0.52283 > 1/2`; it crosses `1/2` near `x = 0.6825` and reaches `0.6656` at `x = 0.8`. What is true, and what the argument needs, is that the diagonal *misses* `1/2`, i.e. `h(x^2 + x^2(1-x)^2) < 1` away from `x = 0.6825...`. Rewrite accordingly. The rest of that remark is correct: I checked the neutral point, the weight `w = 0.9`, and the value `0.382752`.

### B5 [GAP] "The single-letter method is exhausted at `c**`" is not proved; only `c_ceil` is

Theorem 2 assumes the certificate contains the iid protocol *and* that every other class admits hiding. Nothing rules out a protocol whose class admits neither hiding nor products, and no classification theorem is offered. `CEILING_THEOREM.md` Remark 2 gestures at one ("any protocol that ever decouples the two chains lets a family drive the prefix pair towards independence") but that is an assertion, not an argument.

So: what is proved unconditionally for the framework as such is `c <= c_ceil = 0.3830993`. The bound `c <= c** = 0.3828853` holds only under the stated hypothesis on the classes. `RESULT.md`'s "the whole single-letter protocol + coupling class method ... is exhausted at 0.382885" overstates this. The note's own Discussion is more careful ("in every form used since 2022"); that wording should be used everywhere, and the gap should be named as an open problem.

### B6 [GAP] Theorem 2 should require the iid protocol to be used *with its singleton class*

The proof uses "the iid term, whose class is a singleton, is guaranteed the cross pairs". A certificate is formally free to pair the iid protocol with a larger but still valid class, and then that term hides too and (H) yields nothing. Add "with the class `{mu (x) mu}`" to the hypothesis of Theorem 2.

### B7 [MINOR] `2w(1-c) >= 1` should be `> 1`

(16) demands `C > 1`, and the ratio on `mu_delta` tends to `2wq`, so the limit gives `2w(1-c) >= C > 1`. The note writes `>=` "with `C -> 1`". Harmless, since Theorem 4 only claims every `c < c**`, but as printed `c = c**` looks attainable.

### B8 [MINOR] The `x`-range in (D) should be `[1-c, 1/sqrt2]`, not `[1/2, 1/sqrt2]`

The two-point law needs `p = (1-c)/x <= 1`, i.e. `x >= 1-c = 0.617`; for `x` in `[1/2, 0.617)` the adversary is infeasible and the bound is spurious. It costs nothing here: I checked the minimiser is `0.690908` under either range and `c**` agrees to 12 digits. But the theorem should carry the correct constraint.

### B9 [MINOR] "`G` is increasing with slope less than one" is backwards; `G` is decreasing

`w = 1/(2(1-c))` increases with `c`, and the right side of (D) decreases in `w`, so `G` decreases: `G(0.36) = 0.3829088`, `G(0.38) = 0.3828887`, `G(0.39) = 0.3828763`. The conclusion is unaffected and in fact easier, since `c - G(c)` is strictly increasing, so the fixed point is unique and `c <= G(c)` iff `c <= c**`. The printed sentence is simply wrong.

### B10 [MINOR] "Optimal diagonal" holds only on `[1/2, 1/sqrt2]`, and only among rank-one kernels

For a conditionally-iid protocol the diagonal is `int r_x^2`, whose maximum subject to `int r_x = x` and `0 <= r_x <= 1` is `x` (bang-bang `r_x = 1_{u<x}`), not `2x^2`. So on `[0,1/2)` the protocol is strictly below the achievable diagonal, and the "ideal" label holds only on `[1/2, 1/sqrt2]`, which is where Theorem 2 needs it. No theorem weakens, since (D) is only evaluated at `x* = 0.6909`, but the abstract's "a rank-one kernel whose diagonal is optimal" should be qualified. The possibility that a non-rank-one kernel with a better diagonal on `[0,1/2)` raises the Hypothesis-2 minimum elsewhere is not discussed.

### B11 [MINOR] The atom-count argument is missing a sentence

"Fixing the two functionals" is valid only if the two functionals are the two positive eigenfunctions `psi_1, psi_2` of the Mercer expansion `K = sum_j lambda_j psi_j (x) psi_j`, so that `Q(nu) = sum_j lambda_j (int psi_j dnu)^2` and killing the two positive terms leaves `Q <= 0`. Say so (Liu's single functional `E[f(S-bar)]` is exactly this for `k = 1`). Also name Bauer's minimum principle for the extreme-point step, and give the constraint count explicitly: normalisation + mean + 2 functionals = 4, hence at most 4 atoms per component. The `k+2` arithmetic is right and does reduce to Liu's 3 at `k = 1`.

### B12 [MINOR] The `1e-3` entropy floor is an extra constraint that could add an atom

The `<= 4` atoms per component is derived for the *difference* form `N - C D`, which is correct and is what makes the linear denominator harmless; the note does say "difference form". But the numerics minimise the *ratio* subject to `E_mu h(X) >= 1e-3`, and if that floor were active at an optimum it would be a fifth linear constraint admitting a fifth atom. The runs report the minimiser is always the two-point law with `E_mu h(X)` around `0.79`, far from the floor, so this is presentational, but it should be stated.

### B13 [MINOR] "The same level of rigor as Liu's 0.382709" is generous, in three concrete ways

1. Liu verified his hypothesis **twice, by independent methods**: a 2499-point grid eigenvalue at `-2.37e-14`, and an analytic power-series coefficient-matrix check exact to `L = 29` and numerical to `L = 90`. Only the grid check has an analogue here; there is no independent analytic check.
2. Liu ran about `1e5` random initialisations of a 9-dimensional problem. The note reports 300-500 restarts on a larger problem (17 to 25 free parameters at 4 to 6 atoms per component).
3. Liu's Theorem 12 is *proved* for `f = l x p(x)` with `p` polynomial and `l` small, and he evaluates at `l = 1`, `f = x(1-x)`, which is smooth: only the size of the perturbation is outside the proved range. `f_ideal` is not Lipschitz (`f'(x) -> -infinity` as `x -> 1/sqrt2` from below) and is not of the proved form at all, so Hypothesis 1 here is a strictly larger leap, even though (per A10) it survives every numerical test I could throw at it.

State plainly too that the certified margin is `8.5e-6` at `c = 0.38288`, so the positive result rests entirely on the global-minimum hypothesis.

**Precisely what is proved unconditionally:** Theorem 1 (`c <= 0.3830993` for any certificate whose classes contain product laws); Theorem 2's inequalities (H) and (D) and hence `c <= 0.382885260`, given the hypothesis on the classes and given the B1 repair; and Lemma 3. **Numerical only:** Hypotheses 1 and 2, and therefore the whole positive result `c = 0.38284` / `0.382885`.

### B14 [MINOR] Theorem 4's "certifies every `c < c**`" is asserted, not run

The table has two columns, `c = 0.38284` and `c = 0.38288`, both at the single weight `w = 0.810222`. Certifying `c` arbitrarily close to `c**` requires re-running the four-atom search at the corresponding `w(c)`. Either run a short sweep over `c` or weaken the claim to the two values actually certified.

### B15 [MINOR] Cambie's constant is a mixture result, and the phrasing hides that

The introduction says Cambie "proved that it gives exactly 0.3823455" for "Sawin's class". Cambie's certificate has `K = 2`, with iid weight `1 - alpha* = 0.964393` and only `alpha* = 0.035607` on the max-entropy protocol. This matters for the paper's own narrative: a certificate using *only* the max-entropy protocol with the class of all couplings certifies **nothing at all**, because the hiding law drives its ratio to 0. Saying so is direct evidence for the paper's thesis that the iid term is load-bearing, and prevents a reader from thinking Theorem 2 contradicts Cambie. Consistency check: `2 * 0.964393 * (1 - 0.3823455) = 1.1912 > 1`, so Cambie's certificate satisfies (H) comfortably, as it must.

### B16 [MINOR] The certification table does not compile

`\\midrule` parses as `\\` followed by the literal word "midrule"; the body rows end in a single `\` (an escaped space) rather than `\\`; `\\bottomrule` likewise. As typeset the table collapses into one row with the words "midrule" and "bottomrule" printed inside it.

### B17 [ERROR] `RESULT.md` and `CEILING_THEOREM.md` claim `beta = 0.19` certifies `0.382885`. Their own (H) refutes it.

`RESULT.md` Theorem C: "mixed with the iid protocol at `beta = 0.19`, certifies `c = 0.382885`". `CEILING_THEOREM.md`, Attainment: "the rank-one kernel `f_ideal` ... with `beta = 0.19` certifies `c = 0.382885` numerically".

`beta = 0.19` means `w = 0.81`, and (H) requires `2w(1-c) > 1`, i.e. `c < 1 - 1/1.62 = 0.3827160`. So `beta = 0.19` cannot certify anything at or above `0.3827160` - barely more than Liu's `0.382709`, and well short of `0.382885`. At `c = 0.382885`, `2 * 0.81 * 0.617115 = 0.99973 < 1`: the hiding adversary defeats it outright. The repository's own `code/ROBUSTNESS_ideal.md` says exactly this ("beta=0.20 (and beta=0.19) are refuted by the degenerate adversary; the usable beta window ... tops out at beta* ~ 0.1896-0.1898"), and `RESULT.md`'s own rigor ledger item 3 uses the correct `beta** = 0.189778`. So `RESULT.md` contradicts itself within one page, and both headline statements of Theorem C and of the Attainment paragraph are stale.

`paper/note.tex` is *not* affected: it uses `w = 0.810222`, i.e. `beta = 0.189778`, throughout. But the two summary documents must be corrected before anyone reads them as the record, and the `sweep_ideal_b0.19.log` cited as evidence should be re-checked or withdrawn.

Two smaller stale items in the same neighbourhood: `RESULT.md` writes the third branch of `f` as "0 on `[1/2, 1]`" (should be `[1/sqrt2, 1]`), and `code/ROBUSTNESS_ideal.md`'s verdict says `c** = 0.382885260` sits "between 0.38284 and 0.38288", which it does not - it is above both.

### B18 [MINOR] `CEILING_THEOREM.md`'s claim that "no protocol beats iid" for `x >= 1/sqrt2` is false

The (D) paragraph there asserts the bound is `1 - x h(x)/h(x^2)` for `x >= 1/sqrt2`. But the Frechet interval `[2x-1, x]` contains `1/2` for all `x <= 0.75`, so a protocol can reach `h(Pi(0,0)) = 1` there, strictly above `h(x^2)`: at `x = 0.72`, `h(x^2) = 0.999023 < 1`. The claimed bound is therefore not justified for `x` in `(1/sqrt2, 0.75]`. It is non-binding, so nothing downstream changes: the minimum of `1 - x h(x)/h(x^2)` over `[1/sqrt2, 1]` is `0.383099` at `x = 1/sqrt2`, above `c**`. The note itself avoids the error by restricting to `[1/2, 1/sqrt2]`; only the supporting document has it.

### B19 [MINOR] Theorem 1's endgame is more complicated than it needs to be

Since (16) requires `C > 1` strictly, the law with `p = h(1/sqrt2)` exactly already violates it (both sides equal `p h(x*)`), and its mean is exactly `1 - c_ceil >= 1 - c` for any `c > c_ceil`. No perturbation argument is needed. `CEILING_THEOREM.md` notices this ("actually gives equality"); the note's version does not.

---

## C. Not errors, but worth a line

**C1** The Discussion reports the sequential-coupling DP experiments as evidence that "the loss is entirely in the single-letter relaxation". "Entirely" is not supported by "no counterexample on families with `n <= 4` and on two-layer unions with `n <= 24`". Say "on every family we could test".

**C2** Liu's Remark 1 (the maximal-correlation class gives no small-perturbation improvement over `c*` for any `rho`) independently corroborates the paper's thesis and is not cited.

**C3** Given B13, the Reproducibility section should record the optimiser, its tolerances, the restart count per run, and the exact `w` used for each table column.
