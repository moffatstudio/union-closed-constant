import UnionClosedCeiling.Framework
import Mathlib.Analysis.SpecialFunctions.Log.Deriv
import Mathlib.Analysis.Complex.ExponentialBounds

/-!
# Theorem 3.4 — the refined ceiling

> **Theorem (refined ceiling).**  Suppose (cert) uses the i.i.d. protocol with its
> singleton class `{μ ⊗ μ}` and weight `w ∈ [0,1]`, and that every other class contains
> the product law and admits hiding.  Then
> `2w(1-c) ≥ 1` and `c ≤ 1 - x ent(x)/(w ent(x²) + 1 - w)` for every `x` with
> `ent(x) ≤ w ent(x²) + 1 - w`.  Consequently `c ≤ c** = 0.382885260…`.

Formalised here: the two inequalities (H) = `hiding_bound` and (D) = `diagonal_bound`,
the exact fixed-point form `fixed_point_form` they combine into, and the numerical
corollary `refined_ceiling_numeric` (`c ≤ 0.3829`, which already lies below the product
ceiling `c_ceil = 0.3830993…`).

Protocol `0` is the i.i.d. one.  The hypothesis on its class is only
`ContainsProduct (C 0)`, which is weaker than the paper's singleton class, so the
theorems are correspondingly stronger.
-/

namespace UnionClosedCeiling

open Finset

/-! ### Rigorous numerical bounds on the binary entropy at `x = 0.6909`

All bounds come from the Taylor series of `log (1-t)` with the explicit remainder
`Real.abs_log_sub_add_sum_range_le`, together with Mathlib's `log 2` bounds. -/

lemma binEntropy_eq' (p : ℝ) :
    Real.binEntropy p = -(p * Real.log p) - (1 - p) * Real.log (1 - p) := by
  simp [Real.binEntropy, Real.log_inv]; ring

lemma h_eq (p : ℝ) : h p = (-(p * Real.log p) - (1 - p) * Real.log (1 - p)) / Real.log 2 := by
  rw [h, binEntropy_eq']

/-- `log 0.6909 ∈ [-0.36976019, -0.36976018]`. -/
lemma log_6909 : (-0.36976019 : ℝ) ≤ Real.log (6909/10000) ∧
    Real.log (6909/10000) ≤ -0.36976018 := by
  have ht : |(3091/10000 : ℝ)| < 1 := by rw [abs_lt]; norm_num
  have key := Real.abs_log_sub_add_sum_range_le ht 16
  rw [abs_le] at key
  obtain ⟨k1, k2⟩ := key
  have h1 : (1:ℝ) - 3091/10000 = 6909/10000 := by norm_num
  rw [h1] at k1 k2
  rw [abs_of_pos (by norm_num : (0:ℝ) < 3091/10000)] at k1 k2
  have hA : (∑ i ∈ Finset.range 16, ((3091:ℝ)/10000) ^ (i + 1) / (i + 1))
      + ((3091:ℝ)/10000) ^ (16 + 1) / (1 - 3091/10000) ≤ 0.36976019 := by
    norm_num [Finset.sum_range_succ]
  have hB : (0.36976018 : ℝ) ≤ (∑ i ∈ Finset.range 16, ((3091:ℝ)/10000) ^ (i + 1) / (i + 1))
      - ((3091:ℝ)/10000) ^ (16 + 1) / (1 - 3091/10000) := by
    norm_num [Finset.sum_range_succ]
  exact ⟨by linarith, by linarith⟩

/-- `log 0.6182 ∈ [-0.48094337, -0.48094311]`. -/
lemma log_6182 : (-0.48094337 : ℝ) ≤ Real.log (6182/10000) ∧
    Real.log (6182/10000) ≤ -0.48094311 := by
  have ht : |(3818/10000 : ℝ)| < 1 := by rw [abs_lt]; norm_num
  have key := Real.abs_log_sub_add_sum_range_le ht 16
  rw [abs_le] at key
  obtain ⟨k1, k2⟩ := key
  have h1 : (1:ℝ) - 3818/10000 = 6182/10000 := by norm_num
  rw [h1] at k1 k2
  rw [abs_of_pos (by norm_num : (0:ℝ) < 3818/10000)] at k1 k2
  have hA : (∑ i ∈ Finset.range 16, ((3818:ℝ)/10000) ^ (i + 1) / (i + 1))
      + ((3818:ℝ)/10000) ^ (16 + 1) / (1 - 3818/10000) ≤ 0.48094337 := by
    norm_num [Finset.sum_range_succ]
  have hB : (0.48094311 : ℝ) ≤ (∑ i ∈ Finset.range 16, ((3818:ℝ)/10000) ^ (i + 1) / (i + 1))
      - ((3818:ℝ)/10000) ^ (16 + 1) / (1 - 3818/10000) := by
    norm_num [Finset.sum_range_succ]
  exact ⟨by linarith, by linarith⟩

/-- `log 1.04531438 ∈ [0.04431768, 0.04431769]`. -/
lemma log_104531438 : (0.04431768 : ℝ) ≤ Real.log (104531438/100000000) ∧
    Real.log (104531438/100000000) ≤ 0.04431769 := by
  have ht : |(-4531438/100000000 : ℝ)| < 1 := by rw [abs_lt]; norm_num
  have key := Real.abs_log_sub_add_sum_range_le ht 6
  rw [abs_le] at key
  obtain ⟨k1, k2⟩ := key
  have h1 : (1:ℝ) - (-4531438/100000000) = 104531438/100000000 := by norm_num
  rw [h1] at k1 k2
  rw [abs_of_neg (by norm_num : (-4531438/100000000 : ℝ) < 0)] at k1 k2
  have hA : (∑ i ∈ Finset.range 6, ((-4531438:ℝ)/100000000) ^ (i + 1) / (i + 1))
      + (-((-4531438:ℝ)/100000000)) ^ (6 + 1) / (1 - -((-4531438:ℝ)/100000000))
      ≤ -0.04431768 := by
    norm_num [Finset.sum_range_succ]
  have hB : (-0.04431769 : ℝ) ≤
      (∑ i ∈ Finset.range 6, ((-4531438:ℝ)/100000000) ^ (i + 1) / (i + 1))
      - (-((-4531438:ℝ)/100000000)) ^ (6 + 1) / (1 - -((-4531438:ℝ)/100000000)) := by
    norm_num [Finset.sum_range_succ]
  exact ⟨by linarith, by linarith⟩

lemma log_3091 : Real.log (3091/10000) = Real.log (6182/10000) - Real.log 2 := by
  rw [show (3091:ℝ)/10000 = (6182/10000)/2 by norm_num,
    Real.log_div (by norm_num) (by norm_num)]

lemma log_52265719 :
    Real.log (52265719/100000000) = Real.log (104531438/100000000) - Real.log 2 := by
  rw [show (52265719:ℝ)/100000000 = (104531438/100000000)/2 by norm_num,
    Real.log_div (by norm_num) (by norm_num)]

lemma log_47734281 : Real.log (47734281/100000000) = 2 * Real.log (6909/10000) := by
  rw [show (47734281:ℝ)/100000000 = (6909/10000)^2 by norm_num, Real.log_pow]
  norm_num

lemma xsq_eq : ((6909:ℝ)/10000)^2 = 47734281/100000000 := by norm_num

/-- `ent(0.6909) ≥ 0.892131`. -/
lemma hx_lower : (892131/1000000 : ℝ) ≤ h (6909/10000) := by
  rw [h_eq, le_div_iff₀ log_two_pos]
  norm_num [log_3091]
  linarith [log_6909.1, log_6909.2, log_6182.1, log_6182.2,
    Real.log_two_gt_d9, Real.log_two_lt_d9]

/-- `ent(0.6909) ≤ 0.8921319`. -/
lemma hx_upper : h (6909/10000) ≤ (8921319/10000000 : ℝ) := by
  rw [h_eq, div_le_iff₀ log_two_pos]
  norm_num [log_3091]
  linarith [log_6909.1, log_6909.2, log_6182.1, log_6182.2,
    Real.log_two_gt_d9, Real.log_two_lt_d9]

/-- `ent(0.6909²) ≥ 0.9985182`. -/
lemma hx2_lower : (9985182/10000000 : ℝ) ≤ h (47734281/100000000) := by
  rw [h_eq, le_div_iff₀ log_two_pos]
  norm_num [log_52265719, log_47734281]
  linarith [log_6909.1, log_6909.2, log_104531438.1, log_104531438.2,
    Real.log_two_gt_d9, Real.log_two_lt_d9]

/-- `ent(0.6909²) ≤ 0.998519`. -/
lemma hx2_upper : h (47734281/100000000) ≤ (998519/1000000 : ℝ) := by
  rw [h_eq, div_le_iff₀ log_two_pos]
  norm_num [log_52265719, log_47734281]
  linarith [log_6909.1, log_6909.2, log_104531438.1, log_104531438.2,
    Real.log_two_gt_d9, Real.log_two_lt_d9]

/-! ### The two inequalities of Theorem 3.4

Throughout, protocols are indexed by `Fin (K+1)` (so there is at least one), index `0`
is the i.i.d. protocol `Π⁰_{x,y}(0,0) = xy`. -/

variable {K : ℕ} {Prot : Fin (K+1) → ℝ → ℝ → ℝ} {w : Fin (K+1) → ℝ}
  {C : Fin (K+1) → ∀ n : ℕ, (Fin n → ℝ) → (Fin n → ℝ) → (Fin n → Fin n → ℝ) → Prop}
  {Cc c : ℝ}

lemma weight_zero_le_one (hw : ∀ k, 0 ≤ w k) (hw1 : ∑ k, w k = 1) : w 0 ≤ 1 := by
  calc w 0 ≤ ∑ k, w k := Finset.single_le_sum (fun i _ => hw i) (Finset.mem_univ 0)
    _ = 1 := hw1
/-- **Inequality (H) of Theorem 3.4 (component hiding).**

> Dividing by `𝔼[ent X] = (1-q) δ ent(y)` and letting `δ → 0`, (cert) forces `2 w q ≥ C > 1`.
> Hence `2w(1-c) ≥ 1` is necessary.

The limit `δ → 0` is done by hand: `δ` is chosen below the hiding threshold of every class
and below `c (1 - 2 q w₀)`. -/
theorem hiding_bound
    (hProt : ∀ k, IsProtocol (Prot k)) (hiid : ∀ x y, Prot 0 x y = x * y)
    (hw : ∀ k, 0 ≤ w k) (hw1 : ∑ k, w k = 1)
    (hC0 : ContainsProduct (C 0)) (hChide : ∀ k, k ≠ 0 → AdmitsHiding (C k))
    (hCc : 1 ≤ Cc) (hc0 : 0 < c) (hc1 : c < 1)
    (hcert : Certifies Prot w C Cc c) :
    1 ≤ 2 * w 0 * (1 - c) := by
  by_contra hcon
  push_neg at hcon
  obtain ⟨q, hqdef⟩ : ∃ q : ℝ, q = 1 - c := ⟨1 - c, rfl⟩
  have hq0 : 0 < q := by rw [hqdef]; linarith
  have hq1 : q < 1 := by rw [hqdef]; linarith
  have hw0 : 0 ≤ w 0 := hw 0
  have hcon' : 2 * w 0 * q < 1 := by rw [hqdef]; linarith
  have hgap : 0 < 1 - 2 * q * w 0 := by nlinarith
  -- every non-i.i.d. class supplies a hiding coupling below its own threshold `d k`
  have hex : ∀ k : Fin (K+1), ∃ e : ℝ, 0 < e ∧ ∀ δ : ℝ, 0 < δ → δ < e → k ≠ 0 →
      ∃ P : Fin 3 → Fin 3 → ℝ, IsCoupling (hidingWeights q δ) P ∧
        C k 3 (hidingAtoms (1/2)) (hidingWeights q δ) P ∧
        P 2 0 = 0 ∧ P 0 2 = 0 ∧ P 2 2 ≤ δ^2 := by
    intro k
    by_cases hk : k = 0
    · exact ⟨1, one_pos, fun δ _ _ hk0 => absurd hk hk0⟩
    · obtain ⟨e, he, hprop⟩ := hChide k hk q (1/2) ⟨hq0, hq1⟩ ⟨by norm_num, by norm_num⟩
      exact ⟨e, he, fun δ hδ hδd _ => hprop δ hδ hδd⟩
  choose d hd hdprop using hex
  -- one `δ` small enough for all of them, and small enough to force the contradiction
  obtain ⟨δ, hδpos, hδd, hδsmall, hδ1⟩ :
      ∃ δ : ℝ, 0 < δ ∧ (∀ k, δ < d k) ∧ δ < c * (1 - 2*q*w 0) ∧ δ ≤ 1 := by
    obtain ⟨δ₀, hδ₀, hδ₀le⟩ : ∃ e : ℝ, 0 < e ∧ ∀ k, e ≤ d k :=
      ⟨Finset.univ.inf' Finset.univ_nonempty d,
        (Finset.lt_inf'_iff Finset.univ_nonempty).2 (fun i _ => hd i),
        fun k => Finset.inf'_le d (Finset.mem_univ k)⟩
    refine ⟨min (δ₀/2) (min (c * (1 - 2*q*w 0) / 2) (1/4)), ?_, ?_, ?_, ?_⟩
    · exact lt_min (by linarith) (lt_min (div_pos (mul_pos hc0 hgap) two_pos) (by norm_num))
    · intro k
      calc min (δ₀/2) (min (c * (1 - 2*q*w 0) / 2) (1/4)) ≤ δ₀/2 := min_le_left _ _
        _ < δ₀ := by linarith
        _ ≤ d k := hδ₀le k
    · calc min (δ₀/2) (min (c * (1 - 2*q*w 0) / 2) (1/4)) ≤ c * (1 - 2*q*w 0) / 2 :=
          le_trans (min_le_right _ _) (min_le_left _ _)
        _ < c * (1 - 2*q*w 0) := by nlinarith
    · calc min (δ₀/2) (min (c * (1 - 2*q*w 0) / 2) (1/4)) ≤ 1/4 :=
          le_trans (min_le_right _ _) (min_le_right _ _)
        _ ≤ 1 := by norm_num
  -- the hiding law `μ_{q,1/2,δ}`
  have hyIcc : (1/2 : ℝ) ∈ Set.Icc (0:ℝ) 1 := ⟨by norm_num, by norm_num⟩
  have hlaw : IsLaw (hidingAtoms (1/2)) (hidingWeights q δ) :=
    isLaw_hiding (le_of_lt hq0) (le_of_lt hq1) (le_of_lt hδpos) hδ1 hyIcc
  have hmean : 1 - c ≤ mean (hidingAtoms (1/2)) (hidingWeights q δ) := by
    rw [mean_hiding]
    have hpos : 0 < (1-q)*δ := mul_pos (by linarith) hδpos
    rw [hqdef] at hpos ⊢
    nlinarith
  -- product coupling for the i.i.d. protocol, a hiding coupling for the others
  have hPex : ∀ k : Fin (K+1), ∃ Pk : Fin 3 → Fin 3 → ℝ,
      IsCoupling (hidingWeights q δ) Pk ∧ C k 3 (hidingAtoms (1/2)) (hidingWeights q δ) Pk ∧
      (k ≠ 0 → expect (hidingAtoms (1/2)) Pk (fun u v => h (Prot k u v)) ≤ δ^2) ∧
      (k = 0 → Pk = productCoupling (hidingWeights q δ)) := by
    intro k
    by_cases hk : k = 0
    · subst hk
      exact ⟨productCoupling (hidingWeights q δ),
        isCoupling_productCoupling hlaw.2.1 hlaw.2.2, hC0 3 _ _ hlaw,
        fun hne => absurd rfl hne, fun _ => rfl⟩
    · obtain ⟨P, hP1, hP2, h20, h02, h22⟩ := hdprop k δ hδpos (hδd k) hk
      exact ⟨P, hP1, hP2,
        fun _ => expect_hiding_le (hProt k) hyIcc hP1 h20 h02 h22, fun he => absurd he hk⟩
  choose P hP1 hP2 hP3 hP4 using hPex
  have hmain := hcert 3 (hidingAtoms (1/2)) (hidingWeights q δ) hlaw hmean P
    (fun k => ⟨hP1 k, hP2 k⟩)
  rw [entropy_hiding] at hmain
  -- the i.i.d. term is exactly `2q(1-q)δ ent(y) + (1-q)²δ² ent(y²)`
  have hzero : expect (hidingAtoms (1/2)) (P 0) (fun u v => h (Prot 0 u v))
      = 2*q*((1-q)*δ) * h (1/2) + ((1-q)*δ)^2 * h ((1/2:ℝ)^2) := by
    rw [hP4 0 rfl]
    simp only [hiid]
    exact expect_hiding_product_iid
  -- every other term is at most `δ²`
  have hrest : ∑ k ∈ Finset.univ.erase (0 : Fin (K+1)),
      w k * expect (hidingAtoms (1/2)) (P k) (fun u v => h (Prot k u v))
      ≤ (1 - w 0) * δ^2 := by
    have hb : ∀ k ∈ Finset.univ.erase (0 : Fin (K+1)),
        w k * expect (hidingAtoms (1/2)) (P k) (fun u v => h (Prot k u v)) ≤ w k * δ^2 :=
      fun k hk => mul_le_mul_of_nonneg_left (hP3 k (Finset.ne_of_mem_erase hk)) (hw k)
    have hs : ∑ k ∈ Finset.univ.erase (0 : Fin (K+1)), w k = 1 - w 0 := by
      have := Finset.add_sum_erase Finset.univ w (Finset.mem_univ (0 : Fin (K+1)))
      rw [hw1] at this; linarith
    calc ∑ k ∈ Finset.univ.erase (0 : Fin (K+1)),
          w k * expect (hidingAtoms (1/2)) (P k) (fun u v => h (Prot k u v))
        ≤ ∑ k ∈ Finset.univ.erase (0 : Fin (K+1)), w k * δ^2 := Finset.sum_le_sum hb
      _ = (1 - w 0) * δ^2 := by rw [← Finset.sum_mul, hs]
  have hsplit : ∑ k, w k * expect (hidingAtoms (1/2)) (P k) (fun u v => h (Prot k u v))
      = w 0 * expect (hidingAtoms (1/2)) (P 0) (fun u v => h (Prot 0 u v))
        + ∑ k ∈ Finset.univ.erase (0 : Fin (K+1)),
            w k * expect (hidingAtoms (1/2)) (P k) (fun u v => h (Prot k u v)) :=
    (Finset.add_sum_erase Finset.univ _ (Finset.mem_univ (0 : Fin (K+1)))).symm
  rw [hsplit, hzero] at hmain
  have hhalf : h (1/2 : ℝ) = 1 := h_half
  have hquarter : h ((1/2:ℝ)^2) ≤ 1 := h_le_one _
  have hcq : (1 : ℝ) - q = c := by rw [hqdef]; ring
  rw [hhalf, hcq] at hmain
  -- arithmetic: `Cc c δ ≤ 2 q w₀ c δ + δ²`, contradicting `δ < c (1 - 2 q w₀)`
  have hsum2 : Cc * (c * δ * 1) ≤
      w 0 * (2*q*(c*δ) * 1 + (c*δ)^2 * h ((1/2:ℝ)^2)) + (1 - w 0) * δ^2 := by
    linarith [hmain, hrest]
  have hA : (c*δ)^2 * h ((1/2:ℝ)^2) ≤ δ^2 := by
    have e1 : (c*δ)^2 * h ((1/2:ℝ)^2) ≤ (c*δ)^2 := by
      nlinarith [mul_nonneg (sq_nonneg (c*δ)) (sub_nonneg.2 hquarter)]
    have e2 : (c*δ)^2 ≤ δ^2 := by
      nlinarith [mul_nonneg (sq_nonneg δ) (by nlinarith : (0:ℝ) ≤ 1 - c^2)]
    linarith
  have hstep : Cc * (c * δ) ≤ 2*q*w 0*(c*δ) + δ^2 := by
    linarith [hsum2, mul_nonneg hw0 (sub_nonneg.2 hA)]
  have h1 : c * δ ≤ 2*q*w 0*(c*δ) + δ^2 := by
    linarith [hstep, mul_nonneg (sub_nonneg.2 hCc) (le_of_lt (mul_pos hc0 hδpos))]
  have hfin : c ≤ 2*q*w 0*c + δ := by
    by_contra hno
    push_neg at hno
    have hprod : 0 < (c - 2*q*w 0*c - δ) * δ :=
      mul_pos (by linarith) hδpos
    linarith [h1, hprod]
  linarith [hfin, hδsmall]

/-- **Inequality (D) of Theorem 3.4 (the diagonal adversary).**

> Present the product law to every class at `μ = p δ_x + (1-p) δ_0`.  The i.i.d. term
> equals `p² ent(x²)` and every other term is at most `p²`, so (cert) forces
> `c ≤ 1 - x ent(x)/(w ent(x²) + 1 - w)`. -/
theorem diagonal_bound
    (hProt : ∀ k, IsProtocol (Prot k)) (hiid : ∀ x y, Prot 0 x y = x * y)
    (hw : ∀ k, 0 ≤ w k) (hw1 : ∑ k, w k = 1) (hC : ∀ k, ContainsProduct (C k))
    (hCc : 1 ≤ Cc) (hc1 : c < 1) (hcert : Certifies Prot w C Cc c)
    {x : ℝ} (hx : x ∈ Set.Ioc (0:ℝ) 1) (hcond : h x ≤ w 0 * h (x^2) + 1 - w 0) :
    c ≤ 1 - x * h x / (w 0 * h (x^2) + 1 - w 0) := by
  obtain ⟨hx0, hx1⟩ := hx
  rcases eq_or_lt_of_le hx1 with hxe | hxlt
  · subst hxe
    simp only [h_one, mul_zero, zero_div, sub_zero]
    linarith
  · have hxIcc : x ∈ Set.Icc (0:ℝ) 1 := ⟨le_of_lt hx0, hx1⟩
    obtain ⟨D, hDdef⟩ : ∃ D : ℝ, D = w 0 * h (x^2) + 1 - w 0 := ⟨_, rfl⟩
    have hhx : 0 < h x := h_pos hx0 hxlt
    have hcond' : h x ≤ D := by rw [hDdef]; exact hcond
    have hDpos : 0 < D := lt_of_lt_of_le hhx hcond'
    rw [← hDdef]
    by_contra hcon
    push_neg at hcon
    -- `p*` and a slightly smaller `p`
    obtain ⟨ps, hpsdef⟩ : ∃ ps : ℝ, ps = h x / D := ⟨_, rfl⟩
    have hps0 : 0 < ps := by rw [hpsdef]; exact div_pos hhx hDpos
    have hps1 : ps ≤ 1 := by rw [hpsdef, div_le_one hDpos]; exact hcond'
    have hxps : 1 - c < x * ps := by
      have hxx : x * h x / D = x * ps := by rw [hpsdef]; ring
      rw [hxx] at hcon; linarith
    obtain ⟨p, hplt, hp0, hpx⟩ : ∃ p : ℝ, p < ps ∧ 0 < p ∧ 1 - c ≤ p * x := by
      refine ⟨max ((1-c)/x) (ps/2), max_lt ?_ (by linarith), ?_, ?_⟩
      · rw [div_lt_iff₀ hx0]; nlinarith
      · exact lt_of_lt_of_le (by linarith : (0:ℝ) < ps/2) (le_max_right _ _)
      · have hle : (1-c)/x ≤ max ((1-c)/x) (ps/2) := le_max_left _ _
        rw [div_le_iff₀ hx0] at hle; linarith
    have hp1 : p ≤ 1 := le_of_lt (lt_of_lt_of_le hplt hps1)
    have hlaw : IsLaw (twoAtoms x) (twoWeights p) := isLaw_two hxIcc (le_of_lt hp0) hp1
    have hmean : 1 - c ≤ mean (twoAtoms x) (twoWeights p) := by rw [mean_two]; exact hpx
    have hmain := hcert 2 (twoAtoms x) (twoWeights p) hlaw hmean
      (fun _ => productCoupling (twoWeights p))
      (fun k => ⟨isCoupling_productCoupling hlaw.2.1 hlaw.2.2, hC k 2 _ _ hlaw⟩)
    rw [entropy_two] at hmain
    have hzero : expect (twoAtoms x) (productCoupling (twoWeights p))
        (fun u v => h (Prot 0 u v)) = p * p * h (x^2) := by
      have hxx : x * x = x^2 := by ring
      rw [expect_two_product (hProt 0) hxIcc, hiid, hxx]
    have hrest : ∑ k ∈ Finset.univ.erase (0 : Fin (K+1)), w k *
        expect (twoAtoms x) (productCoupling (twoWeights p)) (fun u v => h (Prot k u v))
        ≤ (1 - w 0) * (p * p) := by
      have hb : ∀ k ∈ Finset.univ.erase (0 : Fin (K+1)), w k *
          expect (twoAtoms x) (productCoupling (twoWeights p)) (fun u v => h (Prot k u v))
          ≤ w k * (p * p) := by
        intro k _
        rw [expect_two_product (hProt k) hxIcc]
        refine mul_le_mul_of_nonneg_left ?_ (hw k)
        nlinarith [h_le_one (Prot k x x), mul_pos hp0 hp0]
      have hs : ∑ k ∈ Finset.univ.erase (0 : Fin (K+1)), w k = 1 - w 0 := by
        have := Finset.add_sum_erase Finset.univ w (Finset.mem_univ (0 : Fin (K+1)))
        rw [hw1] at this; linarith
      calc ∑ k ∈ Finset.univ.erase (0 : Fin (K+1)), w k *
            expect (twoAtoms x) (productCoupling (twoWeights p)) (fun u v => h (Prot k u v))
          ≤ ∑ k ∈ Finset.univ.erase (0 : Fin (K+1)), w k * (p * p) := Finset.sum_le_sum hb
        _ = (1 - w 0) * (p * p) := by rw [← Finset.sum_mul, hs]
    have hsplit : ∑ k, w k *
        expect (twoAtoms x) (productCoupling (twoWeights p)) (fun u v => h (Prot k u v))
        = w 0 * expect (twoAtoms x) (productCoupling (twoWeights p))
            (fun u v => h (Prot 0 u v))
          + ∑ k ∈ Finset.univ.erase (0 : Fin (K+1)), w k *
              expect (twoAtoms x) (productCoupling (twoWeights p))
                (fun u v => h (Prot k u v)) :=
      (Finset.add_sum_erase Finset.univ _ (Finset.mem_univ (0 : Fin (K+1)))).symm
    rw [hsplit, hzero] at hmain
    have hfin : p * h x ≤ p * p * D := by
      have e1 : Cc * (p * h x) ≤ w 0 * (p * p * h (x^2)) + (1 - w 0) * (p * p) := by
        linarith [hmain, hrest]
      have e2 : w 0 * (p * p * h (x^2)) + (1 - w 0) * (p * p) = p * p * D := by
        rw [hDdef]; ring
      linarith [e1, e2, mul_nonneg (sub_nonneg.2 hCc)
        (mul_nonneg (le_of_lt hp0) (le_of_lt hhx))]
    have h3 : h x ≤ p * D := by
      by_contra hno
      push_neg at hno
      have hlt : p * (p * D) < p * h x := mul_lt_mul_of_pos_left hno hp0
      linarith [hfin, hlt]
    have h4 : ps ≤ p := by rw [hpsdef, div_le_iff₀ hDpos]; exact h3
    linarith

/-- **The fixed-point form of Theorem 3.4.**  Substituting the bound (H) `w₀ ≥ 1/(2(1-c))`
into (D), whose right-hand side is decreasing in `w₀`. -/
theorem fixed_point_form
    (hProt : ∀ k, IsProtocol (Prot k)) (hiid : ∀ x y, Prot 0 x y = x * y)
    (hw : ∀ k, 0 ≤ w k) (hw1 : ∑ k, w k = 1) (hC : ∀ k, ContainsProduct (C k))
    (hChide : ∀ k, k ≠ 0 → AdmitsHiding (C k))
    (hCc : 1 ≤ Cc) (hc0 : 0 < c) (hchalf : c ≤ 1/2) (hcert : Certifies Prot w C Cc c)
    {x : ℝ} (hx : x ∈ Set.Ioo (0:ℝ) 1) (hmono : h x ≤ h (x^2)) :
    c ≤ 1 - x * h x / (1 - (1 - h (x^2)) / (2 * (1 - c))) := by
  obtain ⟨hx0, hx1⟩ := hx
  have hc1 : c < 1 := by linarith
  have hH := hiding_bound hProt hiid hw hw1 (hC 0) hChide hCc hc0 hc1 hcert
  have hw0 : 0 ≤ w 0 := hw 0
  have hw01 : w 0 ≤ 1 := weight_zero_le_one hw hw1
  have hx2p : (0:ℝ) < x^2 := by positivity
  have hx2l : x^2 < 1 := by nlinarith
  have hB0 : 0 < h (x^2) := h_pos hx2p hx2l
  have hB1 : h (x^2) ≤ 1 := h_le_one _
  have hcond : h x ≤ w 0 * h (x^2) + 1 - w 0 := by
    linarith [mul_nonneg (sub_nonneg.2 hw01) (sub_nonneg.2 hB1)]
  have hD := diagonal_bound hProt hiid hw hw1 hC hCc hc1 hcert ⟨hx0, le_of_lt hx1⟩ hcond
  have hden : 0 < 2*(1-c) := by linarith
  have hDpos : 0 < w 0 * h (x^2) + 1 - w 0 := lt_of_lt_of_le (h_pos hx0 hx1) hcond
  have hD0pos : 0 < 1 - (1 - h (x^2)) / (2*(1-c)) := by
    rw [sub_pos, div_lt_one hden]; linarith
  have hw0lb : 1/(2*(1-c)) ≤ w 0 := by rw [div_le_iff₀ hden]; linarith
  have hDD0 : w 0 * h (x^2) + 1 - w 0 ≤ 1 - (1 - h (x^2)) / (2*(1-c)) := by
    have hkey : (1 - h (x^2))/(2*(1-c)) ≤ w 0 * (1 - h (x^2)) := by
      rw [div_le_iff₀ hden]
      linarith [mul_nonneg (sub_nonneg.2 hB1)
        (by linarith [hH] : (0:ℝ) ≤ 2*w 0*(1-c) - 1)]
    linarith
  have hnum : 0 ≤ x * h x := mul_nonneg (le_of_lt hx0) (h_nonneg (le_of_lt hx0) (le_of_lt hx1))
  have hinv : 1/(1 - (1 - h (x^2)) / (2*(1-c))) ≤ 1/(w 0 * h (x^2) + 1 - w 0) :=
    one_div_le_one_div_of_le hDpos hDD0
  have hcmp : x * h x / (1 - (1 - h (x^2)) / (2*(1-c)))
      ≤ x * h x / (w 0 * h (x^2) + 1 - w 0) :=
    calc x * h x / (1 - (1 - h (x^2)) / (2*(1-c)))
        = x * h x * (1/(1 - (1 - h (x^2)) / (2*(1-c)))) := by ring
      _ ≤ x * h x * (1/(w 0 * h (x^2) + 1 - w 0)) := mul_le_mul_of_nonneg_left hinv hnum
      _ = x * h x / (w 0 * h (x^2) + 1 - w 0) := by ring
  linarith [hD, hcmp]

/-- **The numerical corollary of Theorem 3.4.**  Under the hypotheses of the section
(and `c ≤ 1/2`, as in Proposition 2.2), the certified constant satisfies `c ≤ 0.3829`.

This lies strictly below the product ceiling `c_ceil = 0.3830993…` of Theorem 3.1; the
exact value in the paper is `c** = 0.382885260…`.  The adversary is the two-point law at
`x = 0.6909`. -/
theorem refined_ceiling_numeric
    (hProt : ∀ k, IsProtocol (Prot k)) (hiid : ∀ x y, Prot 0 x y = x * y)
    (hw : ∀ k, 0 ≤ w k) (hw1 : ∑ k, w k = 1) (hC : ∀ k, ContainsProduct (C k))
    (hChide : ∀ k, k ≠ 0 → AdmitsHiding (C k))
    (hCc : 1 ≤ Cc) (hc0 : 0 < c) (hchalf : c ≤ 1/2) (hcert : Certifies Prot w C Cc c) :
    c ≤ 3829/10000 := by
  by_contra hcon
  push_neg at hcon
  have hxm : ((6909:ℝ)/10000) ∈ Set.Ioo (0:ℝ) 1 := ⟨by norm_num, by norm_num⟩
  have hBl : (9985182/10000000:ℝ) ≤ h (((6909:ℝ)/10000)^2) := by rw [xsq_eq]; exact hx2_lower
  have hBu : h (((6909:ℝ)/10000)^2) ≤ (998519/1000000:ℝ) := by rw [xsq_eq]; exact hx2_upper
  have hmono : h ((6909:ℝ)/10000) ≤ h (((6909:ℝ)/10000)^2) := by
    linarith [hx_upper, hBl]
  have hfp := fixed_point_form hProt hiid hw hw1 hC hChide hCc hc0 hchalf hcert hxm hmono
  have hc1 : c < 1 := by linarith
  have hden : 0 < 2*(1-c) := by linarith
  have hB1 : h (((6909:ℝ)/10000)^2) ≤ 1 := h_le_one _
  have hD0pos : 0 < 1 - (1 - h (((6909:ℝ)/10000)^2)) / (2*(1-c)) := by
    rw [sub_pos, div_lt_one hden]; linarith
  have hne : (1:ℝ) - c ≠ 0 := by linarith
  have key : ((6909:ℝ)/10000) * h ((6909:ℝ)/10000)
      ≤ (1 - c) - (1 - h (((6909:ℝ)/10000)^2))/2 := by
    have e1 : ((6909:ℝ)/10000) * h ((6909:ℝ)/10000)
        / (1 - (1 - h (((6909:ℝ)/10000)^2)) / (2*(1-c))) ≤ 1 - c := by linarith [hfp]
    rw [div_le_iff₀ hD0pos] at e1
    have e2 : (1 - c) * (1 - (1 - h (((6909:ℝ)/10000)^2)) / (2*(1-c)))
        = (1 - c) - (1 - h (((6909:ℝ)/10000)^2))/2 := by
      field_simp
    linarith [e1, e2.le, e2.ge]
  linarith [key, hx_lower, hBu, hcon]

end UnionClosedCeiling
