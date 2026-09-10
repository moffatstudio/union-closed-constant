import UnionClosedCeiling.Entropy

/-!
# The single-letter framework (finite model)

This file sets up a faithful **finite** model of the framework of Section 2.2 of the paper:
laws on `[0,1]` with finite support, couplings of such a law with itself, protocols
(represented by their value `Prot_{x,y}(0,0)`, which is all Section 3 uses about them),
classes of couplings, and the certificate inequality (cert).

## Modelling choices

* A law `μ` is given by atoms `a : Fin n → ℝ` in `[0,1]` and weights `m : Fin n → ℝ`
  summing to `1`.  All the adversarial laws used in Section 3 (two-point laws and the
  hiding law of Definition 3.2) are of this form, so restricting to finitely supported
  laws only *weakens* the certificate hypothesis, i.e. strengthens the theorems.
* A protocol is modelled by the function `Prot : ℝ → ℝ → ℝ`, `Prot x y = Prot_{x,y}(0,0)`,
  subject to the Fréchet bounds `max 0 (x+y-1) ≤ Prot x y ≤ min x y`.  Section 3 uses
  nothing else about protocols.
* **`Certifies` is implied by the paper's inequality (cert).**  (cert) reads
  `∑ₖ wₖ inf_{P ∈ Cₖ(μ)} 𝔼_P[ent(Prot⁽ᵏ⁾(X,Y))] ≥ C 𝔼_μ[ent X]`; since the infimum is at
  most the value at any particular admissible family `(P k)`, (cert) implies the
  statement `Certifies` below for every choice of admissible couplings.  Hence every
  theorem proved from `Certifies` applies verbatim to the paper's certificate.
-/

namespace UnionClosedCeiling

open Finset

variable {n : ℕ}

/-- `a` are atoms in `[0,1]` and `m` are probability weights: a finitely supported law on `[0,1]`. -/
def IsLaw (a m : Fin n → ℝ) : Prop :=
  (∀ i, a i ∈ Set.Icc (0:ℝ) 1) ∧ (∀ i, 0 ≤ m i) ∧ ∑ i, m i = 1

/-- The mean `𝔼_μ[X]` of the law. -/
noncomputable def mean (a m : Fin n → ℝ) : ℝ := ∑ i, m i * a i

/-- The entropy `𝔼_μ[ent X]` of the law, in bits. -/
noncomputable def entropy (a m : Fin n → ℝ) : ℝ := ∑ i, m i * h (a i)

/-- `P` is a coupling of the law with weights `m` with itself. -/
def IsCoupling (m : Fin n → ℝ) (P : Fin n → Fin n → ℝ) : Prop :=
  (∀ i j, 0 ≤ P i j) ∧ (∀ i, ∑ j, P i j = m i) ∧ (∀ j, ∑ i, P i j = m j)

/-- `𝔼_{(X,Y) ∼ P}[f X Y]`. -/
noncomputable def expect (a : Fin n → ℝ) (P : Fin n → Fin n → ℝ) (f : ℝ → ℝ → ℝ) : ℝ :=
  ∑ i, ∑ j, P i j * f (a i) (a j)

/-- The product coupling `μ ⊗ μ`. -/
def productCoupling (m : Fin n → ℝ) : Fin n → Fin n → ℝ := fun i j => m i * m j

lemma isCoupling_productCoupling {m : Fin n → ℝ} (hm : ∀ i, 0 ≤ m i) (hs : ∑ i, m i = 1) :
    IsCoupling m (productCoupling m) := by
  refine ⟨fun i j => mul_nonneg (hm i) (hm j), fun i => ?_, fun j => ?_⟩
  · simp [productCoupling, ← Finset.mul_sum, hs]
  · simp [productCoupling, ← Finset.sum_mul, hs]

/-- A protocol, represented by `Prot x y = Prot_{x,y}(0,0)`, constrained by the Fréchet bounds. -/
def IsProtocol (Prot : ℝ → ℝ → ℝ) : Prop :=
  ∀ x y, x ∈ Set.Icc (0:ℝ) 1 → y ∈ Set.Icc (0:ℝ) 1 →
    max 0 (x + y - 1) ≤ Prot x y ∧ Prot x y ≤ min x y

section ProtocolFacts

variable {Prot : ℝ → ℝ → ℝ} (hProt : IsProtocol Prot)
include hProt

/-- "Pairs containing the atom `0` carry no entropy": `Prot x 0 = 0`. -/
lemma protocol_right_zero {x : ℝ} (hx : x ∈ Set.Icc (0:ℝ) 1) : Prot x 0 = 0 := by
  obtain ⟨hl, hu⟩ := hProt x 0 hx ⟨le_refl 0, by norm_num⟩
  have h1 : (0:ℝ) ≤ Prot x 0 := le_trans (le_max_left _ _) hl
  have h2 : Prot x 0 ≤ 0 := le_trans hu (min_le_right _ _)
  linarith

lemma protocol_left_zero {y : ℝ} (hy : y ∈ Set.Icc (0:ℝ) 1) : Prot 0 y = 0 := by
  obtain ⟨hl, hu⟩ := hProt 0 y ⟨le_refl 0, by norm_num⟩ hy
  have h1 : (0:ℝ) ≤ Prot 0 y := le_trans (le_max_left _ _) hl
  have h2 : Prot 0 y ≤ 0 := le_trans hu (min_le_left _ _)
  linarith

/-- On the pair `(1,1)` both bits are surely `0`: `Prot 1 1 = 1`. -/
lemma protocol_one_one : Prot 1 1 = 1 := by
  obtain ⟨hl, hu⟩ := hProt 1 1 ⟨by norm_num, le_refl 1⟩ ⟨by norm_num, le_refl 1⟩
  have h1 : (1:ℝ) ≤ Prot 1 1 := by
    have : (1:ℝ) ≤ max 0 (1 + 1 - 1) := by norm_num
    linarith [le_trans this hl]
  have h2 : Prot 1 1 ≤ 1 := le_trans hu (min_le_left _ _)
  linarith

/-- On the pair `(1,y)` one bit is surely `0`, so the union bit equals the other bit. -/
lemma protocol_one_left {y : ℝ} (hy : y ∈ Set.Icc (0:ℝ) 1) : Prot 1 y = y := by
  obtain ⟨hl, hu⟩ := hProt 1 y ⟨by norm_num, le_refl 1⟩ hy
  have h1 : y ≤ Prot 1 y := by
    have : y ≤ max 0 (1 + y - 1) := by
      have := le_max_right (0:ℝ) (1 + y - 1); linarith
    linarith [le_trans this hl]
  have h2 : Prot 1 y ≤ y := le_trans hu (min_le_right _ _)
  linarith

lemma protocol_one_right {x : ℝ} (hx : x ∈ Set.Icc (0:ℝ) 1) : Prot x 1 = x := by
  obtain ⟨hl, hu⟩ := hProt x 1 hx ⟨by norm_num, le_refl 1⟩
  have h1 : x ≤ Prot x 1 := by
    have : x ≤ max 0 (x + 1 - 1) := by
      have := le_max_right (0:ℝ) (x + 1 - 1); linarith
    linarith [le_trans this hl]
  have h2 : Prot x 1 ≤ x := le_trans hu (min_le_left _ _)
  linarith

end ProtocolFacts

variable {K : ℕ}

/-- The certificate inequality (cert) of Proposition 2.2, in the form we use:
for every finitely supported law of mean at least `1 - c` and every admissible family
of couplings `P k` (one in each class `C k`), the weighted average of the protocol
entropies dominates `Cc` times the entropy of the law.

This is **implied by** the paper's (cert), whose left-hand side is an infimum over the
class, hence at most the value at the chosen `P k`. -/
def Certifies (Prot : Fin K → ℝ → ℝ → ℝ) (w : Fin K → ℝ)
    (C : Fin K → ∀ n : ℕ, (Fin n → ℝ) → (Fin n → ℝ) → (Fin n → Fin n → ℝ) → Prop)
    (Cc c : ℝ) : Prop :=
  ∀ (n : ℕ) (a m : Fin n → ℝ), IsLaw a m → 1 - c ≤ mean a m →
    ∀ P : Fin K → (Fin n → Fin n → ℝ),
      (∀ k, IsCoupling m (P k) ∧ C k n a m (P k)) →
      Cc * entropy a m ≤ ∑ k, w k * expect a (P k) (fun x y => h (Prot k x y))

/-- The class `C` contains the product law `μ ⊗ μ` for every law `μ`. -/
def ContainsProduct (C : ∀ n : ℕ, (Fin n → ℝ) → (Fin n → ℝ) → (Fin n → Fin n → ℝ) → Prop) :
    Prop :=
  ∀ (n : ℕ) (a m : Fin n → ℝ), IsLaw a m → C n a m (productCoupling m)

/-! ### The two-point adversary `p δ_x + (1-p) δ_0` -/

/-- Atoms of the two-point law: `x` and `0`. -/
def twoAtoms (x : ℝ) : Fin 2 → ℝ := ![x, 0]

/-- Weights of the two-point law: `p` and `1-p`. -/
def twoWeights (p : ℝ) : Fin 2 → ℝ := ![p, 1 - p]

lemma isLaw_two {x p : ℝ} (hx : x ∈ Set.Icc (0:ℝ) 1) (hp₀ : 0 ≤ p) (hp₁ : p ≤ 1) :
    IsLaw (twoAtoms x) (twoWeights p) := by
  refine ⟨?_, ?_, ?_⟩
  · intro i; fin_cases i
    · exact hx
    · simp [twoAtoms, Set.mem_Icc]
  · intro i; fin_cases i
    · exact hp₀
    · show (0:ℝ) ≤ 1 - p
      linarith
  · simp [twoWeights, Fin.sum_univ_two]

lemma mean_two {x p : ℝ} : mean (twoAtoms x) (twoWeights p) = p * x := by
  simp [mean, twoAtoms, twoWeights, Fin.sum_univ_two]

lemma entropy_two {x p : ℝ} : entropy (twoAtoms x) (twoWeights p) = p * h x := by
  simp [entropy, twoAtoms, twoWeights, Fin.sum_univ_two]

/-- Under the product coupling, the two-point law puts all the entropy on the diagonal
cell `(x,x)`: every other cell contains the atom `0`. -/
lemma expect_two_product {Prot : ℝ → ℝ → ℝ} (hProt : IsProtocol Prot) {x p : ℝ}
    (hx : x ∈ Set.Icc (0:ℝ) 1) :
    expect (twoAtoms x) (productCoupling (twoWeights p)) (fun u v => h (Prot u v))
      = p * p * h (Prot x x) := by
  have h0 : (0:ℝ) ∈ Set.Icc (0:ℝ) 1 := ⟨le_refl 0, by norm_num⟩
  simp [expect, productCoupling, twoAtoms, twoWeights, Fin.sum_univ_two,
    protocol_right_zero hProt hx, protocol_left_zero hProt hx, protocol_right_zero hProt h0]

/-! ### The hiding adversary `μ_{q,y,δ}` (Definition 3.2)

`μ_{q,y,δ} = q δ₁ + (1-q)[(1-δ) δ₀ + δ δ_y]`, with index `0 ↦ 1`, `1 ↦ 0`, `2 ↦ y`. -/

/-- Atoms of the hiding law: `1`, `0`, `y`. -/
def hidingAtoms (y : ℝ) : Fin 3 → ℝ := ![1, 0, y]

/-- Weights of the hiding law: `q`, `(1-q)(1-δ)`, `(1-q)δ`. -/
def hidingWeights (q δ : ℝ) : Fin 3 → ℝ := ![q, (1-q)*(1-δ), (1-q)*δ]

lemma isLaw_hiding {q y δ : ℝ} (hq₀ : 0 ≤ q) (hq₁ : q ≤ 1) (hδ₀ : 0 ≤ δ) (hδ₁ : δ ≤ 1)
    (hy : y ∈ Set.Icc (0:ℝ) 1) : IsLaw (hidingAtoms y) (hidingWeights q δ) := by
  refine ⟨?_, ?_, ?_⟩
  · intro i; fin_cases i
    · simp [hidingAtoms, Set.mem_Icc]
    · simp [hidingAtoms, Set.mem_Icc]
    · exact hy
  · intro i; fin_cases i
    · exact hq₀
    · exact mul_nonneg (by linarith) (by linarith)
    · exact mul_nonneg (by linarith) hδ₀
  · simp [hidingWeights, Fin.sum_univ_three]; ring

lemma mean_hiding {q y δ : ℝ} :
    mean (hidingAtoms y) (hidingWeights q δ) = q + (1-q)*δ*y := by
  simp [mean, hidingAtoms, hidingWeights, Fin.sum_univ_three]

lemma entropy_hiding {q y δ : ℝ} :
    entropy (hidingAtoms y) (hidingWeights q δ) = (1-q)*δ * h y := by
  simp [entropy, hidingAtoms, hidingWeights, Fin.sum_univ_three]

/-- The class `C` admits hiding (Definition 3.2): for all `q, y ∈ (0,1)` and all
sufficiently small `δ > 0` it contains a coupling of `μ_{q,y,δ}` with itself that puts
no mass on `(y,1)` and `(1,y)` and mass at most `δ²` on `(y,y)`. -/
def AdmitsHiding (C : ∀ n : ℕ, (Fin n → ℝ) → (Fin n → ℝ) → (Fin n → Fin n → ℝ) → Prop) :
    Prop :=
  ∀ q y : ℝ, q ∈ Set.Ioo (0:ℝ) 1 → y ∈ Set.Ioo (0:ℝ) 1 →
    ∃ δ₀ > (0:ℝ), ∀ δ : ℝ, 0 < δ → δ < δ₀ →
      ∃ P : Fin 3 → Fin 3 → ℝ, IsCoupling (hidingWeights q δ) P ∧
        C 3 (hidingAtoms y) (hidingWeights q δ) P ∧
        P 2 0 = 0 ∧ P 0 2 = 0 ∧ P 2 2 ≤ δ^2

/-- Value of the hiding law under a hiding coupling: at most `δ²`. -/
lemma expect_hiding_le {Prot : ℝ → ℝ → ℝ} (hProt : IsProtocol Prot) {q y δ : ℝ}
    (hy : y ∈ Set.Icc (0:ℝ) 1) {P : Fin 3 → Fin 3 → ℝ}
    (hP : IsCoupling (hidingWeights q δ) P)
    (h20 : P 2 0 = 0) (h02 : P 0 2 = 0) (h22 : P 2 2 ≤ δ^2) :
    expect (hidingAtoms y) P (fun u v => h (Prot u v)) ≤ δ^2 := by
  have h0 : (0:ℝ) ∈ Set.Icc (0:ℝ) 1 := ⟨le_refl 0, by norm_num⟩
  have h1 : (1:ℝ) ∈ Set.Icc (0:ℝ) 1 := ⟨by norm_num, le_refl 1⟩
  have hnn := hP.1
  have hkey : expect (hidingAtoms y) P (fun u v => h (Prot u v)) = P 2 2 * h (Prot y y) := by
    simp [expect, hidingAtoms, Fin.sum_univ_three, h20, h02,
      protocol_right_zero hProt h1, protocol_right_zero hProt hy, protocol_right_zero hProt h0,
      protocol_left_zero hProt h1, protocol_left_zero hProt hy,
      protocol_one_one hProt]
  rw [hkey]
  calc P 2 2 * h (Prot y y) ≤ P 2 2 * 1 :=
        mul_le_mul_of_nonneg_left (h_le_one _) (hnn 2 2)
    _ = P 2 2 := by ring
    _ ≤ δ^2 := h22

/-- Value of the hiding law under the **product** coupling, for the i.i.d. protocol
`Prot x y = x y`: exactly `2q(1-q)δ ent(y) + (1-q)²δ² ent(y²)`. -/
lemma expect_hiding_product_iid {q y δ : ℝ} :
    expect (hidingAtoms y) (productCoupling (hidingWeights q δ)) (fun u v => h (u * v))
      = 2*q*((1-q)*δ) * h y + ((1-q)*δ)^2 * h (y^2) := by
  have h1y : (1:ℝ) * y = y := one_mul y
  have hy1 : y * (1:ℝ) = y := mul_one y
  have hyy : y * y = y^2 := (sq y).symm
  simp [expect, productCoupling, hidingAtoms, hidingWeights, Fin.sum_univ_three,
    h1y, hyy]
  ring

end UnionClosedCeiling
