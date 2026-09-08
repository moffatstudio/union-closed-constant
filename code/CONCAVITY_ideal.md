# Concavity / PSD check for K(x,y) = f_ideal(x) f_ideal(y)

Script: `concavity_ideal.py` (run log: `CONCAVITY_ideal_run.log`, raw numbers: `concavity_ideal_report.json`).
Grid: `dt=0.0004`, `n=2499` points on `(0,1)`, `h` in natural log (matches `kernel_game.py`).
`f_ideal(x) = min(x,1-x)` for `x<=1/2`, `sqrt(max(0, 1/2-x^2))` for `x>1/2` (zero at/after `x=1/sqrt2`),
identical to the `f_ideal` already used in `kernel_sweep.py` / `kernel_game3.py`.

## 1. Sanity: reproduce Liu's check for his own f(x)=x(1-x)

| kernel | projected-out | min eigenvalue |
|---|---|---|
| f_liu, codim-3 (⊥ 1,x,f) | Theorem-12 condition | **-1.67e-14** |
| f_liu, codim-2 (⊥ 1,x only) | stronger condition | **-5.74** (fails) |

The codim-3 number matches Liu's reported `-2.37e-14` (same order, both at the MATLAB/numpy noise
floor) — the reproduction is a clean pass, confirming the harness is faithful to `frankl3.m`. The codim-2
number failing hard is *expected*: Liu's Lemma 11 needs the extra `E[f(S̄)]=d` constraint; without it his
own kernel is not PSD either, so codim-2 alone was never the claim.

## 2. f_ideal: does the Theorem-12 condition hold?

| kernel | projected-out | min eigenvalue |
|---|---|---|
| f_ideal, codim-3 (Theorem-12 condition) | ⊥ 1,x,f | **-1.633e-3** |
| f_ideal, codim-2 (stronger) | ⊥ 1,x | **-35.9** (fails, as expected) |

The codim-3 eigenvalue (**-1.633e-3**) is **~5 orders of magnitude above the numerical noise floor**
(~1.8e-14 seen throughout, and matching Liu's own reported precision). This is not roundoff — it is a
genuine failure of positive-semidefiniteness on the exact subspace Lemma 11/Theorem 12 requires.
**Verdict: the concavity hypothesis behind Liu's 3-atom cardinality reduction (Theorem 12) does not hold
for f_ideal at grid resolution 0.0004.**

**Where it fails.** The top eigenvector components are overwhelmingly concentrated at
`x ∈ [0.6988, 0.7044]` — a narrow window straddling `1/√2 ≈ 0.70711`... actually centered just *below*
1/√2, i.e. exactly where f_ideal's sqrt-branch has a vertical tangent (`f'(x) → -∞`) just before dropping
to the flat zero-branch (`f'=0`) at `1/√2`. That non-smooth transition (a genuine kink plus a
divergent-slope point, not merely a corner) is the source of the violation.

**Confirmed with actual probability measures, not just the abstract quadratic form.** Since
`J(mu)=∫∫h(Z)dmu dmu` is bilinear in `mu`, `J((mu1+mu2)/2) - avg(J) = (1/4)·Q[mu1-mu2]` where `Q` is
exactly the tested quadratic form. Splitting the negative eigenvector `v` into positive/negative parts and
renormalizing each to a probability measure automatically gives two measures with *matched* mean and
matched `E[f]` (since `∫x dv=∫f dv=0` forces equal masses/moments on each side). Doing this explicitly:
mu1 concentrates on `x≈0.700-0.704`, mu2 on `x≈0.564-0.568`, both with mean 0.5585 and `E[f]=0.2818`
(matching to 7 digits), and

    J((mu1+mu2)/2) - [J(mu1)+J(mu2)]/2 = -1.78e-6   (< 0: genuine concavity violation)

The magnitude is diluted relative to the raw eigenvalue because the discrete eigenvector's mass, once
spread over ~2499/2 grid points and L1-renormalized, is far less concentrated than the ℓ2-optimal
direction — but the sign is unambiguous and this uses two literal probability measures, not a signed
functional-analytic object.

This also explains why the **random-sampling test (Task 4, below) found zero violations**: the bad
direction is a fine, localized effect requiring mass concentrated in a ~0.004-wide window right at the
`1/√2` singularity; scattered 3-5-atom random measures essentially never land there by chance.

## 3. Smoothed variants — none of them fix it

| variant | codim-3 min eigenvalue | verdict |
|---|---|---|
| `f_s = min(f_ideal, 0.9·min(x,1-x))` | -8.14e-4 | fails |
| `f_s = min(f_ideal, 0.8·min(x,1-x))` | -3.08e-4 | fails |
| C¹ quintic-Hermite smoothing at x=1/2 and x=1/√2 (width 0.03) | -1.39e-3 | fails, no better than raw |

Capping with `lam<1` (which mostly flattens the region near x=0.5, not the 1/√2 singularity) shrinks the
defect somewhat as `lam` drops (0.9→8e-4, 0.8→3e-4) but stays orders above noise. The explicit C¹ smoothing
(quintic Hermite blend removing both the corner at 1/2 and the vertical-tangent-to-flat transition at
1/√2, verified numerically to have continuous first derivative) does **not** help at all — its defect
(-1.39e-3) is essentially the same magnitude as the unsmoothed function. This says the problem is not
merely "f_ideal isn't C¹" but that its overall shape (values close to the `min(x,1-x)` realizability
ceiling, i.e. a "large-l" kernel far outside Liu's proven small-l perturbative regime) sits outside the PSD
region — smoothing the kinks alone doesn't move it back in.

## 4. Random-measure sampling (independent check)

300 random trials per kernel, 3-5 atom `mu1` + moment-matched (mean, `E[f]`) 3-5 atom `mu2` via LP
feasibility (matched to ~1e-9), checking `J(avg) ≥ avg(J)`:

| kernel | valid pairs | violations found | worst gap |
|---|---|---|---|
| f_liu | 298/300 | 0 | +4.1e-10 |
| f_ideal | 300/300 | 0 | +1.0e-8 |
| f_ideal, lam=0.9 | 300/300 | 0 | +2.5e-9 |
| f_ideal, lam=0.8 | 297/300 | 0 | +3.6e-8 |
| f_ideal, C¹-smoothed | 298/300 | 0 | +4.2e-7 |

Zero violations across the board — consistent with §2's explanation: the true bad direction is a
narrow, localized spike near `1/√2` that generic random atom placement essentially never hits. This
sampling test is not strong enough on its own to certify concavity; the grid/eigenvector check (§2) is the
decisive one, and it fails.

## Bottom line

**Liu's Theorem-12-style 3-atom reduction does not plausibly carry over to f_ideal as specified.** The
Theorem-12 PSD condition fails by ~1e-3 (five orders above noise) at grid resolution 0.0004, the failure
is explicitly localized at the `x=1/√2` kink/singularity where f_ideal transitions to its flat zero
branch, it is confirmed with an explicit pair of probability measures (not just an abstract eigenvalue),
and none of the tested smoothed variants (lam-capping at 0.9/0.8, or an explicit C¹ mollification of both
kinks) restore PSD-ness — the defect stays the same order of magnitude. Any argument using f_ideal in
Liu's cardinality-reduction machinery would need either a fundamentally different (much smaller/gentler)
perturbation of f_ideal, or a different route to bounding the mixture-component count that doesn't rely on
Lemma 11/Theorem 12's concavity.
