import UnionClosedCeiling.Framework

/-!
# Lemma 3.3 — the classes

> **Lemma 3.3.**  The classes of the i.i.d. protocol, of Sawin's protocol, of Yu's
> protocols for every `ρ > 0`, and of every conditionally-i.i.d. protocol contain the
> product law.  All but the first admit hiding.

Formalised here, in the finite model:

* the singleton class `{μ ⊗ μ}` of the i.i.d. protocol (`iidClass`) contains the product;
* the class of **all couplings** (`allCouplings`, Sawin's class) contains the product and
  admits hiding;
* the class of **mixtures of products** (`mixtureOfProducts`, the class of every
  conditionally-i.i.d. protocol) contains the product and admits hiding.

The witness used for hiding is the paper's mixture-of-two-products coupling
`P = q δ₁⊗δ₁ + (1-q) P₀⊗P₀`, `P₀ = (1-δ)δ₀ + δ δ_y` (`hidingCoupling`).  For the class of
all couplings the paper offers the maximal-correlation witness instead; since that class
imposes no constraint, the same mixture witness serves, and we use it for both.

**Not formalised:** the maximal-correlation classes of Yu's protocols.  Their hiding
witness requires the continuity of singular values in the matrix entries, which is a
genuinely different argument; see the README.
-/

namespace UnionClosedCeiling

open Finset

/-- The class of *all* couplings (Sawin's class). -/
def allCouplings : ∀ n : ℕ, (Fin n → ℝ) → (Fin n → ℝ) → (Fin n → Fin n → ℝ) → Prop :=
  fun _ _ _ _ => True

/-- The singleton class `{μ ⊗ μ}` of the i.i.d. protocol. -/
def iidClass : ∀ n : ℕ, (Fin n → ℝ) → (Fin n → ℝ) → (Fin n → Fin n → ℝ) → Prop :=
  fun _ _ m P => P = productCoupling m

/-- The class of mixtures of product laws: `P = ∑ⱼ πⱼ νⱼ ⊗ νⱼ` with `∑ⱼ πⱼ νⱼ = μ`.
This is the class `C₃(μ)` of the conditionally-i.i.d. protocols. -/
def mixtureOfProducts : ∀ n : ℕ, (Fin n → ℝ) → (Fin n → ℝ) → (Fin n → Fin n → ℝ) → Prop :=
  fun n _ m P => ∃ (J : ℕ) (π : Fin J → ℝ) (ν : Fin J → Fin n → ℝ),
    (∀ j, 0 ≤ π j) ∧ (∑ j, π j = 1) ∧
    (∀ j i, 0 ≤ ν j i) ∧ (∀ j, ∑ i, ν j i = 1) ∧
    (∀ i, ∑ j, π j * ν j i = m i) ∧
    (∀ i i', P i i' = ∑ j, π j * (ν j i * ν j i'))

/-! ### Products -/

lemma containsProduct_allCouplings : ContainsProduct allCouplings :=
  fun _ _ _ _ => trivial

lemma containsProduct_iidClass : ContainsProduct iidClass :=
  fun _ _ _ _ => rfl

lemma containsProduct_mixtureOfProducts : ContainsProduct mixtureOfProducts := by
  intro n a m hlaw
  refine ⟨1, ![1], ![m], ?_, ?_, ?_, ?_, ?_, ?_⟩
  · intro j; fin_cases j; norm_num
  · simp
  · intro j i; fin_cases j; exact hlaw.2.1 i
  · intro j; fin_cases j; exact hlaw.2.2
  · intro i; simp
  · intro i i'; simp [productCoupling]

/-! ### Hiding -/

/-- The paper's hiding coupling of `μ_{q,y,δ}` with itself:
`q δ₁ ⊗ δ₁ + (1-q) P₀ ⊗ P₀` with `P₀ = (1-δ) δ₀ + δ δ_y`.
In our indexing (`0 ↦ 1`, `1 ↦ 0`, `2 ↦ y`), `δ₁ = ![1,0,0]` and `P₀ = ![0,1-δ,δ]`. -/
noncomputable def hidingComp1 : Fin 3 → ℝ := ![1, 0, 0]

/-- The second component `P₀ = (1-δ) δ₀ + δ δ_y` of the hiding coupling. -/
noncomputable def hidingComp2 (δ : ℝ) : Fin 3 → ℝ := ![0, 1 - δ, δ]

/-- The hiding coupling `P = q δ₁⊗δ₁ + (1-q) P₀⊗P₀`. -/
noncomputable def hidingCoupling (q δ : ℝ) : Fin 3 → Fin 3 → ℝ :=
  fun i j => q * (hidingComp1 i * hidingComp1 j) + (1-q) * (hidingComp2 δ i * hidingComp2 δ j)

lemma hidingCoupling_isCoupling {q δ : ℝ} (hq0 : 0 ≤ q) (hq1 : q ≤ 1)
    (hδ0 : 0 ≤ δ) (hδ1 : δ ≤ 1) : IsCoupling (hidingWeights q δ) (hidingCoupling q δ) := by
  have hc1 : ∀ i, 0 ≤ hidingComp1 i := by
    intro i; fin_cases i <;> simp [hidingComp1]
  have hc2 : ∀ i, 0 ≤ hidingComp2 δ i := by
    intro i; fin_cases i <;> simp [hidingComp2] <;> linarith
  refine ⟨?_, ?_, ?_⟩
  · intro i j
    have := mul_nonneg (hc1 i) (hc1 j)
    have := mul_nonneg (hc2 i) (hc2 j)
    unfold hidingCoupling
    have h1 : 0 ≤ q * (hidingComp1 i * hidingComp1 j) :=
      mul_nonneg hq0 (mul_nonneg (hc1 i) (hc1 j))
    have h2 : 0 ≤ (1-q) * (hidingComp2 δ i * hidingComp2 δ j) :=
      mul_nonneg (by linarith) (mul_nonneg (hc2 i) (hc2 j))
    linarith
  · intro i
    fin_cases i <;>
      simp [hidingCoupling, hidingComp1, hidingComp2, hidingWeights, Fin.sum_univ_three] <;> ring
  · intro j
    fin_cases j <;>
      simp [hidingCoupling, hidingComp1, hidingComp2, hidingWeights, Fin.sum_univ_three] <;> ring

lemma hidingCoupling_mixture {q δ : ℝ} (hq0 : 0 ≤ q) (hq1 : q ≤ 1)
    (hδ0 : 0 ≤ δ) (hδ1 : δ ≤ 1) (y : ℝ) :
    mixtureOfProducts 3 (hidingAtoms y) (hidingWeights q δ) (hidingCoupling q δ) := by
  refine ⟨2, ![q, 1-q], ![hidingComp1, hidingComp2 δ], ?_, ?_, ?_, ?_, ?_, ?_⟩
  · intro j; fin_cases j
    · exact hq0
    · show (0:ℝ) ≤ 1 - q
      linarith
  · simp [Fin.sum_univ_two]
  · intro j i; fin_cases j <;> fin_cases i <;>
      simp [hidingComp1, hidingComp2] <;> linarith
  · intro j; fin_cases j <;> simp [hidingComp1, hidingComp2, Fin.sum_univ_three]
  · intro i; fin_cases i <;>
      simp [hidingComp1, hidingComp2, hidingWeights, Fin.sum_univ_two]
  · intro i i'; simp [hidingCoupling, Fin.sum_univ_two]

lemma hidingCoupling_zeros {q δ : ℝ} : hidingCoupling q δ 2 0 = 0 ∧ hidingCoupling q δ 0 2 = 0 := by
  constructor <;> simp [hidingCoupling, hidingComp1, hidingComp2]

lemma hidingCoupling_diag {q δ : ℝ} (hq0 : 0 ≤ q) (hδ0 : 0 ≤ δ) :
    hidingCoupling q δ 2 2 ≤ δ^2 := by
  have : hidingCoupling q δ 2 2 = (1-q) * (δ * δ) := by
    simp [hidingCoupling, hidingComp1, hidingComp2]
  rw [this]
  nlinarith [mul_nonneg hδ0 hδ0]

/-- The class of all couplings admits hiding. -/
lemma admitsHiding_allCouplings : AdmitsHiding allCouplings := by
  intro q y hq hy
  refine ⟨1, one_pos, fun δ hδ0 hδ1 => ⟨hidingCoupling q δ, ?_, trivial, ?_, ?_, ?_⟩⟩
  · exact hidingCoupling_isCoupling (le_of_lt hq.1) (le_of_lt hq.2) (le_of_lt hδ0)
      (le_of_lt hδ1)
  · exact hidingCoupling_zeros.1
  · exact hidingCoupling_zeros.2
  · exact hidingCoupling_diag (le_of_lt hq.1) (le_of_lt hδ0)

/-- The class of mixtures of products admits hiding. -/
lemma admitsHiding_mixtureOfProducts : AdmitsHiding mixtureOfProducts := by
  intro q y hq hy
  refine ⟨1, one_pos, fun δ hδ0 hδ1 => ⟨hidingCoupling q δ, ?_, ?_, ?_, ?_, ?_⟩⟩
  · exact hidingCoupling_isCoupling (le_of_lt hq.1) (le_of_lt hq.2) (le_of_lt hδ0)
      (le_of_lt hδ1)
  · exact hidingCoupling_mixture (le_of_lt hq.1) (le_of_lt hq.2) (le_of_lt hδ0)
      (le_of_lt hδ1) y
  · exact hidingCoupling_zeros.1
  · exact hidingCoupling_zeros.2
  · exact hidingCoupling_diag (le_of_lt hq.1) (le_of_lt hδ0)

end UnionClosedCeiling
