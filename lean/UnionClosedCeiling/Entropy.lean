import Mathlib.Analysis.SpecialFunctions.BinaryEntropy

/-!
# Binary entropy in bits

The paper writes `ent` for the binary entropy function measured in **bits**,
`ent(p) = -p log₂ p - (1-p) log₂ (1-p)`, normalised so that `ent(1/2) = 1`.
Mathlib's `Real.binEntropy` is the same function in *nats*, so we set
`h p = Real.binEntropy p / Real.log 2`.

Facts proved here (all of them are used later):
`h_zero`, `h_one`, `h_nonneg`, `h_pos`, `h_le_one`.
-/

namespace UnionClosedCeiling

open Real

/-- Binary entropy in bits: `h p = -p log₂ p - (1-p) log₂ (1-p)`.
This is the paper's `ent`. -/
noncomputable def h (p : ℝ) : ℝ := Real.binEntropy p / Real.log 2

lemma log_two_pos : (0:ℝ) < Real.log 2 := Real.log_pos (by norm_num)

@[simp] lemma h_zero : h 0 = 0 := by simp [h]

@[simp] lemma h_one : h 1 = 0 := by simp [h]

@[simp] lemma h_half : h (1/2) = 1 := by
  have : (1:ℝ)/2 = (2:ℝ)⁻¹ := by norm_num
  simp [h, this, Real.binEntropy_two_inv, div_self (ne_of_gt log_two_pos)]

/-- `h` is nonnegative on `[0,1]`. -/
lemma h_nonneg {p : ℝ} (hp₀ : 0 ≤ p) (hp₁ : p ≤ 1) : 0 ≤ h p :=
  div_nonneg (Real.binEntropy_nonneg hp₀ hp₁) (le_of_lt log_two_pos)

/-- `h` is strictly positive on `(0,1)`. -/
lemma h_pos {p : ℝ} (hp₀ : 0 < p) (hp₁ : p < 1) : 0 < h p :=
  div_pos (Real.binEntropy_pos hp₀ hp₁) log_two_pos

/-- `h p ≤ 1` for every real `p`: the paper's `ent(·) ≤ 1`. -/
lemma h_le_one (p : ℝ) : h p ≤ 1 := by
  unfold h
  rw [div_le_one log_two_pos]
  exact Real.binEntropy_le_log_two

end UnionClosedCeiling
