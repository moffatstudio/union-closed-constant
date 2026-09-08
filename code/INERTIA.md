# Inertia of the codim-2 (mean-only) quadratic form for K_liu, f_ideal, K_new

Script: `inertia_check.py` (log: `INERTIA_run.log`, raw numbers: `inertia_report.json`).
Form: `Q = [-h(x_i x_j + K(x_i,x_j))]` on a uniform grid, projected onto the Euclidean orthogonal
complement of `{1, x}` (mean-only, codim-2), symmetrised, **full** eigenspectrum computed (not a fixed
top-k window — see why below). Threshold for "negative": `< -1e-8`. Grid quadrature weights are uniform
(constant `dt`) so by Sylvester's law of inertia the plain-Euclidean projection gives the same inertia as
explicit `dt`-weighted projection would — no extra weighting needed.

## Counts k, at both requested resolutions

| kernel | dt=0.001 (n=999) | dt=0.0005 (n=1999) | stable? |
|---|---|---|---|
| **(a) K_liu** | k=1 | k=1 | yes — matches Liu's own f-direction |
| **(b) f_ideal** | k=2 | k=2 | yes |
| **(c) K_new** | k=500 (of rank 997) | k=999 (of rank 1997) | **no — scales as ~n/2, not a fixed number** |

## (a) K_liu — k=1

Single negative eigenvalue, magnitude growing with resolution (-2.28 at dt=0.001, -4.58 at dt=0.0005 —
consistent with an (integrable) log-curvature singularity of `h` at the grid's lower boundary `x→0`, not a
divergence in the *count*). Eigenvector concentrates entirely at the smallest grid points, `x≈0.001-0.01`.
Gap to the next eigenvalue is enormous: `-2.28` (or `-4.58`) down to `~-1.2e-14` (noise floor) — no
ambiguity about k=1.

## (b) f_ideal — k=2

Two negative eigenvalues:
1. Same boundary mode as K_liu (`x≈0.001-0.01`), magnitude -14.3 / -28.7 (again grows with resolution,
   same boundary-curvature origin, not a count issue).
2. **-6.41e-4** (dt=0.001) / **-1.28e-3** (dt=0.0005), concentrated at `x≈0.696-0.705` — this is the same
   `1/√2≈0.7071`-kink direction found in the earlier codim-3 (Theorem-12) check in `CONCAVITY_ideal.md`.
   Adding the f-moment constraint (going from codim-2 to codim-3) removes exactly this direction (that
   check's codim-3 spectrum starts at `-1.6e-3`ish only when the f-moment constraint is *not* also
   imposed — consistent).

Gap: k-th eigenvalue `-6.4e-4`/`-1.3e-3` down to `(k+1)`-th `-1.0e-10`/`-2.0e-10` — a clean 6-7 order-of-
magnitude gap, then true noise floor at `~1e-14` a couple of eigenvalues further. k=2 is unambiguous.

## (c) K_new — k is NOT small; it grows linearly with the grid

This is the headline result. At dt=0.001, **500 of 997** possible eigen-directions are negative; at
dt=0.0005, **999 of 1997** are — both almost exactly **half the rank**, and the fraction does not shrink as
the grid refines (0.5015 → 0.5005). This is qualitatively different from (a)/(b): there is no finite k
independent of resolution — in the continuum limit this reads as an effectively unbounded (half-dimensional)
negative subspace, not a small number of "extra moment constraints."

**Where the negative directions sit** (sampled across the sorted index, dt=0.001):

| index | eigenvalue | concentrates near x |
|---|---|---|
| 0 | -20.17 | 0.001-0.006 (boundary mode, as in a/b) |
| 20 | -0.070 | 0.001-0.025 |
| 100 | -3.14e-3 | 0.002-0.022 |
| 200 | -9.48e-4 | 0.023-0.032 |
| 300 | -4.75e-4 | 0.132-0.143 |
| 400 | -2.16e-4 | 0.299-0.309 |
| 499 (last negative) | -4.77e-8 | 0.708-0.713 (right at 1/√2) |

The negative directions **sweep continuously across the whole active support of K_new**, from the boundary
at x≈0 up through x≈0.71 (≈1/√2, where K_new's covariance drops to 0 and the kernel becomes plain i.i.d.)
as the eigenvalue index increases. This is not a localized defect at one or two special points (unlike
f_ideal's isolated 1/√2-kink) — it is a broadband failure of concavity across essentially the entire region
where K_new differs from independence.

## Verification (K_new): does removing exactly the k negative directions restore PSD-ness?

Yes, trivially and as expected: adding the k found negative eigenvectors (500 at dt=0.001, 999 at
dt=0.0005) as extra linear constraints and re-projecting drives the remaining spectrum to the noise floor
(`~1e-15` at dt=0.001; one residual `-4.9e-11` plus noise at dt=0.0005 — both far below the -1e-8
threshold, 0 remaining negative eigenvalues by that threshold). This confirms the math (removing all
negative directions of a symmetric form necessarily leaves a PSD remainder) but is close to tautological
here because k itself is ~n/2 — it does **not** yield a useful finite "k+2 atoms per component" reduction:
fixing ~500-1000 extra moment constraints is not a cardinality reduction in any practical sense, and (since
k scales with the grid) there is no evidence it converges to a finite number in the continuum.

## Verdict

- **(a) K_liu: k=1** — Liu's own result, reproduced exactly, stable across resolution.
- **(b) f_ideal: k=2** — small, stable, and localized (boundary mode + the 1/√2 kink mode already
  identified in `CONCAVITY_ideal.md`). A Liu-style "fix k=2 extra eigen-functionals → 4-atom-per-component
  reduction" argument is numerically plausible for f_ideal, *if* the boundary mode is a genuine artifact
  worth checking analytically (it grows with resolution — recommend an analytic look at behavior near
  x→0 before relying on it) — see caveat below.
- **(c) K_new: k grows as ~n/2, no stable finite count.** The generalized Liu argument (Theorem 12) as
  stated does **not** apply to K_new: there is no small k such that fixing k extra eigen-functionals
  restores concavity. The failure is broadband across nearly the whole support where K_new is
  non-degenerate, not a small number of isolated bad directions.

**Caveat on the boundary mode (present in all three kernels' top eigenvalue):** the single dominant
negative eigenvalue in all three cases sits at the grid's lower edge (`x≈0.001-0.01`) and its *magnitude*
roughly doubles as `dt` halves, consistent with an integrable but grid-resolution-sensitive `h`-curvature
singularity at `x→0`, not a change in the *count*. It doesn't affect the k-counts reported here (which are
stable), but if this mode is later used as one of the "k eigen-functionals" to fix, its exact form should
be derived analytically rather than read off a fixed-resolution grid vector, since its shape/magnitude is
resolution-dependent.
