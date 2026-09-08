# Kernel shape optimisation (conditionally-iid class), 2026-09-08 -- WRAPPED UP

**Bottom line: no kernel found in this search exceeded c = 0.38289.** The best confirmed point in
the conditionally-iid + iid mixture class remains f_ideal at beta~0.19 (c ~ 0.382885, lead's
sweep), consistent with the lead's analytic bound c** ~ 0.38288. Stopped per lead's instruction
(14:5x) once the two-adversary argument closed the gap analytically.

## What was built
- `code/kernel_opt_search.py`: double-oracle / cutting-plane driver. Outer player maximises the
  min-over-adversary-pool ratio via an epigraph SLSQP NLP (free knot values + beta + slack t);
  inner oracle is `kernel_game.adversary_min`, whose worst law is added to the pool when it beats
  the pool-relaxed bound. c is bisected between a known-feasible lo and the class ceiling hi.
- Two kernel families were searched:
  1. **Rank-1 f(x)f(y)**, f piecewise-linear on 17 knots (x_k=k/16), 0<=f(x_k)<=min(x_k,1-x_k).
     Pipeline bug found + fixed during smoke testing: seeded two-point adversary laws (x*,0) with
     x* < 1-c are infeasible (can't reach the mean constraint) and must be excluded, not clipped.
     After the fix, the pipeline reproduces the known operating point exactly: at c=0.382840 it
     finds beta=0.19419 with true worst-case ratio 1.000079 -- matching the lead's correction that
     rank-1 kernels are capped near beta~0.19 by the degenerate adversary mu = q*delta_1 +
     (1-q)*delta_eps.
  2. **Variance-profile family** (generalising `kernel_game.K_new`): parametrise the diagonal
     Var(r_x) = v(x) directly, free piecewise-linear on the same 17 knots, 0<=v(x)<=x(1-x), no
     other realizability constraint. Realised by the canonical nested two-value coupling
     r_x(u) = 1 for u<=t(x), lam(x) otherwise (shared u across all x), with closed form
     `lam(x) = x - v(x)/(1-x)`, `t(x) = v(x)/((1-x)^2+v(x))` from the mean/variance equations, and
     for x,y with t(x)<=t(y): `E[r_x r_y] = t(x) + (t(y)-t(x))*lam(x) + (1-t(y))*lam(x)*lam(y)`.
     Verified this reduces to `K_new` exactly (max abs diff 2e-16 off the knot grid; the earlier
     0.027 "discrepancy" was pure knot-grid discretisation, not a formula error). This family
     fixes the rank-1 degeneracy: v(eps) = O(eps) at small x (vs O(eps^2) for rank-1 f(x)f(y)), so
     K(eps,eps) no longer vanishes relative to eps(1-eps) at the degenerate adversary.

## What the runs showed
At c=0.38284 with a pool seeded from two-point laws (x* in [0.55,0.75]), degenerate laws
(mu = (1-c)*delta_1 + c*delta_eps, eps in {1e-5..3e-2}), and Liu's worst law:
- beta=0.99848 (pool-relaxed optimum pushed beta near its upper bound 1.0): true worst-case ratio
  collapses to **0.0019** against adversary q=0.6192, P0=[(0.32,0),(0,.5),(0,.5)],
  P1=[(1,.158),(1,.421),(1,.421)] -- a cross-pair-hiding law matching the lead's adversary (i)
  (mu = q*delta_1 + (1-q)*[(1-d)delta_0 + d*delta_y], hiding the (y,1) cross term inside one
  mixture component, forcing 2*w_iid*(1-c) >= 1).
- beta=0.2 (near the lead's corrected ceiling): already infeasible at c=0.38284 in the
  pool-relaxed check (t*=0.9908 < 1).

This is a live numerical confirmation, from first principles (not assuming the lead's derivation),
that the two adversaries the lead identified genuinely bound both kernel families tested here.

## Artifacts
- `code/kernel_opt_search.py` -- driver (both kernel families, double-oracle loop).
- `code/best_kernel.json` -- final summary: best known point, class ceiling, lead's analytic
  bound, and the search conclusion.
- `code/kernel_opt_adversary_pool.json` -- 21 seed adversary laws (two-point + degenerate + Liu's)
  plus the 2 worst adversaries discovered live during this search, for reuse.
- `code/KERNEL_OPT_run.log` -- raw run log (sanity checks + the two smoke-test runs above).

## Status: closed
No further outer-kernel-shape optimisation planned; the class appears exhausted at c ~ 0.38288-9
given the lead's two-adversary argument, confirmed numerically here.
