# Lean formalisation — specification

Target: machine-check the two *unconditional* results of the paper, Theorem 3.1 (product ceiling) and Theorem 3.4 (refined ceiling), together with the parts of Lemma 3.3 that are elementary, on a faithful finite model of the single-letter framework of Section 2.2. Nothing conditional (Theorem 6.2, the hypotheses) and nothing measure-theoretic (Proposition 2.2, Gilmer's argument over families) is in scope. Lean 4 + Mathlib, no `sorry`, no new axioms.

Conventions: `h` is the binary entropy **in bits**, `h p = Real.binEntropy p / Real.log 2` (Mathlib's `Real.binEntropy` is in nats). The facts needed about it are all in `Mathlib.Analysis.SpecialFunctions.BinaryEntropy`: `binEntropy_nonneg`, `binEntropy_le_log_two` (so `h p ≤ 1` for every real `p`), `binEntropy_eq_zero` (`h 0 = h 1 = 0`), `binEntropy_pos`.

## 1. The finite model (file `Framework.lean`)

A law `μ` on `[0,1]` is finitely supported, given by `n : ℕ`, atoms `a : Fin n → ℝ` with `a i ∈ Set.Icc 0 1`, weights `m : Fin n → ℝ` with `0 ≤ m i` and `∑ i, m i = 1`. Its mean is `∑ i, m i * a i`, its entropy `∑ i, m i * h (a i)`.

A coupling of `μ` with itself is `P : Fin n → Fin n → ℝ` with `0 ≤ P i j`, `∑ j, P i j = m i`, `∑ i, P i j = m j`. Expectation `∑ i, ∑ j, P i j * f (a i) (a j)`. The product coupling is `P i j = m i * m j`.

A protocol is `Π : ℝ → ℝ → ℝ` (the value `Π x y = Π_{x,y}(0,0)`) satisfying the Fréchet bounds for `x y ∈ [0,1]`: `max 0 (x + y - 1) ≤ Π x y` and `Π x y ≤ min x y`. (This is all the paper uses about protocols in Section 3. Consequences to prove once: `Π x 0 = 0`, `Π 0 y = 0`, `Π 1 1 = 1`, `Π 1 y = y`, `Π x 1 = x`, hence `h (Π x 0) = 0`, `h (Π 1 1) = 0`, `h (Π 1 y) = h y`.)

A class for protocol `k` is a predicate on couplings, depending on the law: `C k n a m P : Prop`.

**Certificate.** For protocols `Π : Fin K → ℝ → ℝ → ℝ`, weights `w : Fin K → ℝ` (`0 ≤ w k`, `∑ w = 1`), classes `C`, constants `Cc : ℝ` and `c : ℝ`:

```
Certifies Π w C Cc c :=
  ∀ n a m, IsLaw a m → (1 - c ≤ mean a m) →
  ∀ P : Fin K → (Fin n → Fin n → ℝ), (∀ k, IsCoupling m (P k) ∧ C k n a m (P k)) →
    Cc * entropy a m ≤ ∑ k, w k * expect a (P k) (fun x y => h (Π k x y))
```

This is *implied by* the paper's inequality (cert) (which has `inf` over the class on the left: `∑ w_k inf_P ≤ ∑ w_k E_{P_k}` for any choice `P_k ∈ C_k`), so every theorem proved from `Certifies` applies to the paper's certificate. Record this remark in the file's docstring.

`ContainsProduct C k := ∀ n a m, IsLaw a m → C k n a m (fun i j => m i * m j)`.

**Hiding law.** For `q y δ : ℝ`, the three-atom law `μ_{q,y,δ}`: atoms `![1, 0, y]`, weights `![q, (1-q)*(1-δ), (1-q)*δ]` (Definition 3.2).

`AdmitsHiding C k := ∀ q y, q ∈ Set.Ioo 0 1 → y ∈ Set.Ioo 0 1 → ∃ δ₀ > 0, ∀ δ, 0 < δ → δ < δ₀ → ∃ P, IsCoupling (hidingWeights q δ) P ∧ C k 3 (hidingAtoms y) (hidingWeights q δ) P ∧ P 2 0 = 0 ∧ P 0 2 = 0 ∧ P 2 2 ≤ δ^2`

(index 0 ↦ atom 1, index 1 ↦ atom 0, index 2 ↦ atom y).

## 2. Theorem 3.1 — product ceiling (file `Ceiling.lean`)

```
theorem product_ceiling
  (hΠ : ∀ k, IsProtocol (Π k)) (hw : ∀ k, 0 ≤ w k) (hw1 : ∑ k, w k = 1)
  (hC : ∀ k, ContainsProduct C k) (hCc : 1 ≤ Cc)
  (hcert : Certifies Π w C Cc c) :
  c ≤ 1 - h (1 / Real.sqrt 2) / Real.sqrt 2
```

Proof (paper, p. 6): let `x* = 1/√2`. If `c ≤ c_ceil` done. Otherwise `(1-c)·√2 < h x*` and `0 < h x*`, so pick `p` strictly between `max 0 ((1-c)√2)` and `h x*`. Apply `hcert` to the two-atom law `atoms ![x*, 0]`, `weights ![p, 1-p]` (mean `p x* ≥ 1-c`) with the product coupling for every `k`. Each term: the `(x*,x*)` cell has mass `p²` and `h(Π x* x*) ≤ 1`; every other cell has an atom `0`, so `Π = 0` and `h 0 = 0`. Hence `Cc · p · h x* ≤ ∑ w_k p² = p²`, so `h x* ≤ Cc · h x* ≤ p` (as `p > 0`), contradicting `p < h x*`. Note that only `h ≤ 1` is used, **not** `h(x*²) = 1`.

## 3. Theorem 3.4 — refined ceiling (file `Refined.lean`)

Hypotheses: `K ≥ 1`, protocol `0` is i.i.d. (`Π 0 x y = x * y`), `ContainsProduct C 0`; for `k ≠ 0`, `ContainsProduct C k` and `AdmitsHiding C k`; `w` as before, `1 ≤ Cc`, `0 < c`, `c < 1`, `Certifies Π w C Cc c`. Write `w₀ = w 0`.

(H) `theorem hiding_bound : 1 ≤ 2 * w₀ * (1 - c)`.
Proof: fix any `y ∈ (0,1)` (say `y = 1/2`), `q = 1 - c ∈ (0,1)`. For every small `δ` apply `hcert` to `μ_{q,y,δ}` (mean `q + (1-q)δy ≥ 1-c`; entropy `(1-q)δ h y`) with `P 0` = product and, for `k ≠ 0`, `P k` = the hiding coupling. Evaluate: cells containing atom `0` give `h 0 = 0`; cell `(1,1)` gives `h 1 = 0`; cells `(y,1)`, `(1,y)` give `h y` (Fréchet: `Π 1 y = y`); cell `(y,y)` gives `≤ 1`. So the i.i.d. term is exactly `2q(1-q)δ h y + (1-q)²δ² h(y²)` and each other term is `≤ P k 2 2 · 1 ≤ δ²`. Therefore `Cc (1-q) δ h y ≤ w₀[2q(1-q)δ h y + (1-q)²δ² h(y²)] + (1-w₀) δ²`. Divide by `(1-q) δ h y > 0`: `Cc ≤ 2 q w₀ + δ · B` with `B` a constant independent of `δ`. If `2 q w₀ < 1 ≤ Cc`, choosing `δ` small enough (below `δ₀` from every hiding class and below `(1 - 2qw₀)/(2 max(B,1))`) gives a contradiction. Do the limit by hand this way; no filters needed.

(D) `theorem diagonal_bound (x) (hx : x ∈ Set.Ioc 0 1) (hcond : h x ≤ w₀ * h (x^2) + 1 - w₀) : c ≤ 1 - x * h x / (w₀ * h (x^2) + 1 - w₀)`.
Proof: `D := w₀ h(x²) + 1 - w₀ > 0` (it is `≥ h x`, and if `h x = 0` then `x = 1` and `D ≥ 1 - w₀ + w₀ h 1`... handle: for `x = 1`, `h 1 = 0` and the claim is `c ≤ 1`, true). For `x ∈ (0,1)`: `h x > 0`, `D ≥ h x > 0`, `p* := h x / D ∈ (0,1]`. Suppose `c > 1 - x p*`, i.e. `p* x > 1 - c`. Pick `p` with `max 0 ((1-c)/x) < p < p*`... more simply: pick `p ∈ (0, p*)` with `p x ≥ 1 - c` (possible since `p* x > 1-c`). Apply `hcert` to `![x, 0]`, `![p, 1-p]` with products everywhere: i.i.d. term `= p² h(x²)`, other terms `≤ p²`, so `Cc p h x ≤ p² D`, i.e. `h x ≤ Cc h x ≤ p D`, i.e. `p* ≤ p`, contradiction.

**Fixed-point form** (corollary, exact): for `x ∈ (0,1)` with `h x ≤ h (x^2)`, and `c ≤ 1/2`:
`c ≤ 1 - x * h x / (1 - (1 - h (x^2)) / (2 * (1 - c)))`.
Proof: the condition `h x ≤ w₀ h(x²) + 1 - w₀` holds for every `w₀ ∈ [0,1]` because `h x ≤ h(x²) ≤ 1` (convex combination). `D(w₀) = 1 - w₀(1 - h(x²))` is decreasing in `w₀`, and (H) gives `w₀ ≥ 1/(2(1-c))`, so `D(w₀) ≤ 1 - (1-h(x²))/(2(1-c)) =: D₀`, and `D₀ > 0` because `1 - h(x²) ≤ 1 < 2(1-c)` for `c ≤ 1/2`... (`c < 1/2` strictly, or use `1 - h(x²) < 1`). Then `x h x / D(w₀) ≥ x h x / D₀`, and (D) gives the claim.

**Numerical corollary** `theorem refined_ceiling_numeric : c ≤ 0.3829` (i.e. `c ≤ 3829/10000`), under the hypotheses of the section plus `c ≤ 1/2`. Take `x = 6909/10000`. Need rigorous bounds: `h x ≥ 0.89211` and `h (x^2) ≤ 0.99853` (true values at x = 0.6909: `0.8921318…`, `0.9985183…`), plus the crude `h x ≤ h(x²)` (e.g. `h x ≤ 0.90`, `h(x²) ≥ 0.99`). With `F(c) := 1 - x h x / (1 - (1-h(x²))/(2(1-c)))`, the fixed-point form gives `c ≤ F(c)`; `F` is decreasing in `c` on `(0, 1/2]`; and `F(0.3829) < 0.3829` (at the true values `F(0.3829) = 0.382882`, margin `1.8·10⁻⁵`; the bounds above leave margin `≈ 8·10⁻⁶`, so they must be that tight). Hence if `c > 0.3829` then `c ≤ F(c) ≤ F(0.3829) < 0.3829 < c`, contradiction. Bounds on `log` at rational points: use `Real.abs_log_sub_add_sum_range_le` (Taylor series of `log(1 - t)` with explicit remainder) or `Real.log_le_sub_one_of_pos` / `Real.add_one_le_exp` chains, with `norm_num` on the rationals; for `log 2` use `Real.log_two_gt_d9` / `Real.log_two_lt_d9`. If `0.3829` proves too tight after a serious attempt, prove `c ≤ 0.383` instead (margin `1.2·10⁻⁴`) and say so in the README — even `0.383 < c_ceil = 0.383099` shows formally that the refined ceiling beats the product ceiling.

## 4. Lemma 3.3 — the classes (file `Classes.lean`)

Define the class of all couplings (`fun _ _ _ _ => True`) and the class of mixtures of products in the finite model (`∃ J (π : Fin J → ℝ) (ν : Fin J → Fin n → ℝ), 0 ≤ π, ∑ π = 1, each ν j is a probability vector, ∑ j, π j • ν j = m, and P i i' = ∑ j, π j * ν j i * ν j i'`). Prove: both contain the product law; both admit hiding, with the explicit witness of the paper: `P = q δ₁⊗δ₁ + (1-q) P₀⊗P₀`, `P₀ = (1-δ)δ₀ + δ δ_y` (so `P 2 2 = (1-q)δ² ≤ δ²`, `P 2 0 = P 0 2 = 0`). Also prove the singleton class `{product}` contains the product (trivial) — that is the i.i.d. class. The maximal-correlation classes are **not** formalised (singular-value continuity argument); say so.

## 5. Deliverables

- `lean/` is a Lake project `UnionClosedCeiling` requiring Mathlib **from git at a pinned tag** (so CI can fetch the cache): `lakefile.toml`, `lean-toolchain`, `lake-manifest.json`. Locally a Mathlib checkout of the same toolchain exists at `C:/ml/mathlib` (commit `37df177`, `leanprover/lean4:v4.23.0`); you may copy it into `.lake/packages/mathlib` to avoid a download, provided `lake build` then succeeds with the manifest pinned to that commit. Otherwise `lake exe cache get`.
- Files: `UnionClosedCeiling/Entropy.lean`, `Framework.lean`, `Ceiling.lean`, `Refined.lean`, `Classes.lean`, and `UnionClosedCeiling.lean` importing all.
- `lake build` exits 0 with **no `sorry`** and no warnings about `sorry`; run `#print axioms` on each main theorem and record the output (must be only `propext`, `Classical.choice`, `Quot.sound`).
- `lean/README.md`: table paper statement → Lean name → file → axioms; the modelling choices above (finite laws, `Certifies` implied by (cert)); what is and is not formalised; build instructions; the numeric bound proved.
- `lean/check.sh`: `lake build` + grep for `sorry` + `#print axioms` check, exit non-zero on failure.
- Keep every theorem statement readable: named hypotheses, no `autoImplicit`, docstrings quoting the paper's statement.
