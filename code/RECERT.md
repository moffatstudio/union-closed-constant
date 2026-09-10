# Independent re-certification of c = 0.38284

Verifier: independent agent, 2026-09-08. Evaluator written from `paper/note.tex`
Sections 2-4 and `RESULT.md` only. No repository code was read until every number
below had been produced.

## My code

- `verification/independent-recertification/evaluator.py` (also `code/recert_evaluator.py`) - certificate ratio, kernels `f_liu`, `f_ideal`,
  SLSQP local minimiser (softmax weights, atom locations in [0,1], q in [0,1]).
- `verification/independent-recertification/search.py` - seeds + multi-restart global search driver.
- `verification/independent-recertification/calib.py` - Liu calibration.
- `verification/independent-recertification/closed.py` - closed-form hiding family, two-point family, fixed point.
- Results: `verification/independent-recertification/ideal_n{4,5,6}_c38284.json`.

Objective implemented (base-2 h; ratio is log-base invariant):

    ratio = [ w E_{mu x mu} h(XY)
            + (1-w) ( (1-q) E_{P0 x P0} + q E_{P1 x P1} ) h(XY + f(X)f(Y)) ] / E_mu h(X)

with mu = (1-q)P0 + qP1, subject to E_mu[X] >= 1-c and the floor E_mu[h(X)] >= 1e-3.

## 1. Calibration against Liu (f(x) = x(1-x), w = 0.899947, c = 0.382709087918741)

| check | result |
|---|---|
| two-point family, closed form | min ratio 1.0000000000 at x = 0.690788, p = 0.893604 |
| full search, 4 atoms/component, 355 starts | min ratio 0.9999999988 |
| minimiser | q = 0, P0 = 0.8936 d_0.6908 + 0.1064 d_0 |

Reproduces Liu's optimum and his minimiser. **Calibration passes.**

## 2. Fixed point of (H) and (D), solved independently

| quantity | my value | note.tex |
|---|---|---|
| c** | 0.382885260 | 0.382885260 |
| x* | 0.6909077 | 0.690908 |
| w = 1/(2(1-c**)) | 0.810222 | 0.810222 |

## 3. Certification at w = 0.810222, c = 0.38284, f = f_ideal

355 starts per budget: 16 two-point seeds on x in [0.6,0.75], 15 hiding seeds
(d in {1e-2,1e-3,1e-4} x y in {0.05,0.2,0.5,0.7,0.9}), Liu / Cambie / x* seeds,
12 mixed (two-point + tiny atom) seeds, 320 random restarts. Floor E_mu h(X) >= 1e-3.

| atoms/component | min ratio | minimiser |
|---|---|---|
| 4 | 1.00007334 | q = 0, P0 = 0.89326 d_0.690908 + 0.10674 d_0 |
| 5 | 1.00007334 | q = 0, P0 = 0.89326 d_0.690908 + 0.10674 d_0 |
| 6 | 1.00007334 | q = 0, P0 = 0.89229 d_0.690908 + 0.10674 d_0 + 0.00097 d_0.690906 |

Every minimiser found is the two-point law. Nothing below 1 was found at any budget.

## 4. Hiding family, closed form (no optimiser)

mu_d = q d_1 + (1-q)[(1-d) d_0 + d d_y], q = 1-c, hiding coupling
P = q d_1 x d_1 + (1-q) P0 x P0. Exact ratio:

    ratio = 2wq + d * [ w(1-q) h(y^2) + (1-w) h(y^2 + f(y)^2) ] / h(y)

so it converges to 2w(1-c) from above, the bracket being non-negative. At c = 0.38284,
2w(1-c) = 1.000073219.

| y \ d | 1e-2 | 1e-3 | 1e-4 | 1e-6 |
|---|---|---|---|---|
| 0.05 | 1.00064721 | 1.00013062 | 1.00007896 | 1.00007328 |
| 0.20 | 1.00217149 | 1.00028305 | 1.00009420 | 1.00007343 |
| 0.50 | 1.00448747 | 1.00051464 | 1.00011736 | 1.00007366 |
| 0.70 | 1.00574528 | 1.00064043 | 1.00012994 | 1.00007379 |

## 5. Note's Theorem 2 / equation (H) numerical claims

| claim in note | my value | agrees |
|---|---|---|
| hiding limit 2w(1-c) = 1.000073 at c = 0.38284 | 1.000073219, approached from above | yes |
| two-point at x = 0.6909, c = 0.38284, ~1.00007 | 1.000073341 | yes |
| two-point at x = 0.6909, c = 0.38288 | 1.000008524 | yes |

## 6. Comparison with the repository (read only after the above)

`code/ROBUSTNESS_ideal.md` part 4.2 reports min ratio 1.00007334 at m = 4, 5, 6 for
c = 0.38284, minimiser the two-point law at x* = 0.6909, p* ~ 0.893-0.894. My 4-, 5- and
6-atom runs all give **1.00007334** with minimiser 0.89326 d_0.690908 + 0.10674 d_0.
Agreement to all 8 reported digits, from an evaluator that shares no code.

`ROBUSTNESS_ideal.md` part 4.1 degenerate table and my hiding table in Section 4 above
agree digit for digit at all 12 shared grid points.

`code/certify_A.log` / `certify_B.log` (v1, beta rounded to 0.1897) report 1.00007323;
my value at the exact beta** = 0.189778 is 1.00007334, matching v2 rather than v1, as
expected from the beta rounding.

Discrepancies found: **one, editorial.** Hypothesis 2 in `paper/note.tex` states the
minimum "equals the value 1.00005", while the table in the same paper, the repository
logs and my runs all give 1.0000733. The 1.00005 figure in the hypothesis statement is
wrong and should be corrected to 1.0000733.

Separately, at exactly c = c** = 0.382885260 with w quoted to six digits as 0.810222,
the hiding family evaluates to 0.999999935 at d = 1e-6, i.e. marginally below 1. This is
not an error: c** is a supremum and the note correctly claims only every c < c**.
The certified value c = 0.38284 has margin 7.3e-5.

## Caveat

The c = 0.38288 batch was not run (descoped by the lead). All three atom budgets at
c = 0.38284, the closed-form hiding family and the closed-form two-point family are
complete. The 6-atom minimiser splits its mass over two atoms at 0.690908 and 0.690906,
i.e. it is the same two-point law with a numerically duplicated atom.

## Verdict

**The claim c >= 0.38284 is reproduced independently.**
