import Mathlib.Analysis.SpecialFunctions.BinaryEntropy

/-! Binary entropy in bits. Placeholder created at environment setup; the formalisation fills this in. -/

namespace UnionClosedCeiling

noncomputable def h (p : ℝ) : ℝ := Real.binEntropy p / Real.log 2

lemma h_le_one (p : ℝ) : h p ≤ 1 := by
  unfold h
  rw [div_le_one (Real.log_pos (by norm_num : (1:ℝ) < 2))]
  exact Real.binEntropy_le_log_two

end UnionClosedCeiling
