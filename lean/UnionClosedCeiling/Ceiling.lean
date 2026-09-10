import UnionClosedCeiling.Framework

/-!
# Theorem 3.1 — the product ceiling

> **Theorem (product ceiling).**  Suppose every class `C_k(μ)` in (cert) contains the
> product law `μ ⊗ μ` for every `μ`.  Then (cert) fails for every
> `c > c_ceil := 1 - ent(1/√2)/√2 = 0.3830993…`.

Formal contrapositive: if the certificate holds for `c` with `C > 1` (we only use
`C ≥ 1`), then `c ≤ 1 - ent(1/√2)/√2`.

The proof only uses `ent ≤ 1` on the diagonal cell — **not** `ent(x*²) = 1`.
-/

namespace UnionClosedCeiling

open Finset

/-- The ceiling constant `c_ceil = 1 - ent(1/√2)/√2 = 0.3830993…`. -/
noncomputable def cCeil : ℝ := 1 - h (1 / Real.sqrt 2) / Real.sqrt 2

lemma one_lt_sqrt_two : (1:ℝ) < Real.sqrt 2 := by
  nlinarith [Real.sq_sqrt (by norm_num : (0:ℝ) ≤ 2), Real.sqrt_nonneg 2]

lemma sqrt_two_pos : (0:ℝ) < Real.sqrt 2 := lt_trans one_pos one_lt_sqrt_two

/-- `x* = 1/√2` lies in `(0,1)`. -/
lemma xstar_mem : (1 / Real.sqrt 2) ∈ Set.Ioo (0:ℝ) 1 := by
  constructor
  · positivity
  · rw [div_lt_one sqrt_two_pos]; exact one_lt_sqrt_two

/-- **Theorem 3.1 (product ceiling).**  If every class contains the product law and the
certificate (cert) holds for `c` with constant `Cc ≥ 1`, then `c ≤ 1 - ent(1/√2)/√2`. -/
theorem product_ceiling {K : ℕ} {Prot : Fin K → ℝ → ℝ → ℝ} {w : Fin K → ℝ}
    {C : Fin K → ∀ n : ℕ, (Fin n → ℝ) → (Fin n → ℝ) → (Fin n → Fin n → ℝ) → Prop}
    {Cc c : ℝ}
    (hProt : ∀ k, IsProtocol (Prot k)) (hw : ∀ k, 0 ≤ w k) (hw1 : ∑ k, w k = 1)
    (hC : ∀ k, ContainsProduct (C k)) (hCc : 1 ≤ Cc)
    (hcert : Certifies Prot w C Cc c) :
    c ≤ 1 - h (1 / Real.sqrt 2) / Real.sqrt 2 := by
  by_contra hcon
  push_neg at hcon
  set x := 1 / Real.sqrt 2 with hxdef
  obtain ⟨hx0, hx1⟩ := xstar_mem
  have hxIcc : x ∈ Set.Icc (0:ℝ) 1 := ⟨le_of_lt hx0, le_of_lt hx1⟩
  have hhx : 0 < h x := h_pos hx0 hx1
  -- `(1-c)·√2 < ent(x*)`
  have hkey : (1 - c) * Real.sqrt 2 < h x := by
    have : 1 - h x / Real.sqrt 2 < c := hcon
    have h2 : 1 - c < h x / Real.sqrt 2 := by linarith
    calc (1 - c) * Real.sqrt 2 < (h x / Real.sqrt 2) * Real.sqrt 2 := by
          exact mul_lt_mul_of_pos_right h2 sqrt_two_pos
      _ = h x := by field_simp
  -- choose `p` strictly between `max 0 ((1-c)√2)` and `ent(x*)`
  set L : ℝ := max 0 ((1 - c) * Real.sqrt 2) with hLdef
  have hL : L < h x := max_lt hhx hkey
  have hL0 : 0 ≤ L := le_max_left _ _
  set p : ℝ := (L + h x) / 2 with hpdef
  have hpL : L < p := by simp only [hpdef]; linarith
  have hph : p < h x := by simp only [hpdef]; linarith
  have hp0 : 0 < p := lt_of_le_of_lt hL0 hpL
  have hp1 : p ≤ 1 := le_of_lt (lt_of_lt_of_le hph (h_le_one x))
  -- the two-point law `p δ_{x*} + (1-p) δ_0` has mean `p x* ≥ 1 - c`
  have hlaw : IsLaw (twoAtoms x) (twoWeights p) := isLaw_two hxIcc (le_of_lt hp0) hp1
  have hmean : 1 - c ≤ mean (twoAtoms x) (twoWeights p) := by
    rw [mean_two]
    have h1 : (1 - c) * Real.sqrt 2 < p := lt_of_le_of_lt (le_max_right _ _) hpL
    have h2 : 1 - c ≤ p / Real.sqrt 2 := by
      rw [le_div_iff₀ sqrt_two_pos]; linarith
    calc 1 - c ≤ p / Real.sqrt 2 := h2
      _ = p * x := by rw [hxdef]; ring
  -- present the product coupling to every class
  have hcoup : ∀ k, IsCoupling (twoWeights p) (productCoupling (twoWeights p)) ∧
      C k 2 (twoAtoms x) (twoWeights p) (productCoupling (twoWeights p)) := by
    intro k
    exact ⟨isCoupling_productCoupling hlaw.2.1 hlaw.2.2, hC k 2 _ _ hlaw⟩
  have hmain := hcert 2 (twoAtoms x) (twoWeights p) hlaw hmean
    (fun _ => productCoupling (twoWeights p)) hcoup
  rw [entropy_two] at hmain
  -- every term is at most `w k * p²`
  have hsum : ∑ k, w k * expect (twoAtoms x) (productCoupling (twoWeights p))
      (fun u v => h (Prot k u v)) ≤ p * p := by
    have hterm : ∀ k ∈ (univ : Finset (Fin K)),
        w k * expect (twoAtoms x) (productCoupling (twoWeights p))
          (fun u v => h (Prot k u v)) ≤ w k * (p * p) := by
      intro k _
      rw [expect_two_product (hProt k) hxIcc]
      refine mul_le_mul_of_nonneg_left ?_ (hw k)
      have := h_le_one (Prot k x x)
      nlinarith [mul_pos hp0 hp0]
    calc ∑ k, w k * expect (twoAtoms x) (productCoupling (twoWeights p))
            (fun u v => h (Prot k u v))
        ≤ ∑ k, w k * (p * p) := Finset.sum_le_sum hterm
      _ = p * p := by rw [← Finset.sum_mul, hw1, one_mul]
  -- hence `p ent(x*) ≤ Cc p ent(x*) ≤ p²`, so `ent(x*) ≤ p`, contradiction
  have h1 : p * h x ≤ Cc * (p * h x) := by nlinarith [mul_nonneg (le_of_lt hp0) (le_of_lt hhx)]
  have h2 : p * h x ≤ p * p := le_trans h1 (le_trans hmain hsum)
  have h3 : h x ≤ p := le_of_mul_le_mul_left (by linarith) hp0
  linarith
