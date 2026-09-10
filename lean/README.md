# `UnionClosedCeiling` — a Lean 4 / Mathlib formalisation of the ceiling theorems

Machine-checked versions of the two unconditional results of the paper *The ceiling of the
single-letter entropy method for the union-closed sets conjecture, and a protocol that reaches
it* (A. Moffat, 8 September 2026; `../paper/paper.pdf`): Theorem 3.1 (product ceiling) and
Theorem 3.4 (refined ceiling), together with the elementary parts of Lemma 3.3, on a
faithful **finite** model of the single-letter framework of Section 2.2. Written by a Claude
(Anthropic) agent from `SPEC.md` and the paper; every statement was checked against the paper
by the author before being committed.

No `sorry`; the only axioms used are `propext`, `Classical.choice`, `Quot.sound`.

## Paper statement → Lean name → file

| Paper | Lean | File |
|---|---|---|
| `ent` (binary entropy, in bits) | `UnionClosedCeiling.h` | `UnionClosedCeiling/Entropy.lean` |
| `ent ≥ 0`, `ent(0)=ent(1)=0`, `ent > 0` on `(0,1)`, `ent ≤ 1`, `ent(1/2)=1` | `h_nonneg`, `h_zero`, `h_one`, `h_pos`, `h_le_one`, `h_half` | `Entropy.lean` |
| law on `[0,1]`, mean, entropy | `IsLaw`, `mean`, `entropy` | `Framework.lean` |
| coupling of `μ` with itself, `μ ⊗ μ` | `IsCoupling`, `productCoupling` | `Framework.lean` |
| protocol (Definition 2.1) via `Π_{x,y}(0,0)` and the Fréchet interval | `IsProtocol` | `Framework.lean` |
| "pairs containing the atom `0` carry no entropy"; `Π_{1,1}(0,0)=1`; `Π_{1,y}(0,0)=y` | `protocol_right_zero`, `protocol_left_zero`, `protocol_one_one`, `protocol_one_left`, `protocol_one_right` | `Framework.lean` |
| the certificate (cert), Proposition 2.2 | `Certifies` | `Framework.lean` |
| class contains the product law | `ContainsProduct` | `Framework.lean` |
| hiding law `μ_{q,y,δ}` (Definition 3.2) | `hidingAtoms`, `hidingWeights` | `Framework.lean` |
| class admits hiding (Definition 3.2) | `AdmitsHiding` | `Framework.lean` |
| **Theorem 3.1 (product ceiling)** | `product_ceiling` | `Ceiling.lean` |
| `c_ceil = 1 - ent(1/√2)/√2` | `cCeil` | `Ceiling.lean` |
| **Theorem 3.4, inequality (H)** `2w(1-c) ≥ 1` | `hiding_bound` | `Refined.lean` |
| **Theorem 3.4, inequality (D)** | `diagonal_bound` | `Refined.lean` |
| Theorem 3.4, the fixed-point form (`G` of eq. (G)) | `fixed_point_form` | `Refined.lean` |
| Theorem 3.4, the numerical consequence `c ≤ c**` | `refined_ceiling_numeric` (proves `c ≤ 0.3829`) | `Refined.lean` |
| Lemma 3.3, products: i.i.d. singleton class | `containsProduct_iidClass` | `Classes.lean` |
| Lemma 3.3, products: all couplings (Sawin) | `containsProduct_allCouplings` | `Classes.lean` |
| Lemma 3.3, products: mixtures of products (conditionally-i.i.d.) | `containsProduct_mixtureOfProducts` | `Classes.lean` |
| Lemma 3.3, hiding: all couplings | `admitsHiding_allCouplings` | `Classes.lean` |
| Lemma 3.3, hiding: mixtures of products | `admitsHiding_mixtureOfProducts` | `Classes.lean` |

Supporting numerical work (all in `Refined.lean`): `log_6909`, `log_6182`,
`log_104531438` (Taylor series of `log(1-t)` with the explicit remainder
`Real.abs_log_sub_add_sum_range_le`, 16 resp. 16 resp. 6 terms), and
`hx_lower`, `hx_upper`, `hx2_lower`, `hx2_upper`, the rigorous bounds

```
0.892131  ≤ ent(0.6909)   ≤ 0.8921319
0.9985182 ≤ ent(0.6909²)  ≤ 0.998519
```

(true values `0.89213183…`, `0.99851828…`), obtained from those log bounds together with
Mathlib's `Real.log_two_gt_d9` / `Real.log_two_lt_d9`.

## Modelling choices

* **Finite laws.** A law `μ` on `[0,1]` is finitely supported: atoms `a : Fin n → ℝ` in
  `[0,1]`, weights `m : Fin n → ℝ` with `m ≥ 0`, `∑ m = 1`. Every adversary used in
  Section 3 (the two-point laws of Theorem 3.1 and (D), and the three-point hiding law of
  Definition 3.2) is of this form. Restricting the certificate hypothesis to finitely
  supported laws *weakens* the hypothesis, hence *strengthens* the theorems proved from it.
* **`Certifies` is implied by (cert).** The paper's (cert) has an infimum over the class on
  the left-hand side. Since the infimum is at most the value at any particular admissible
  family of couplings, (cert) implies
  `Certifies Π w C C₀ c` as stated in `Framework.lean` (for every law of mean `≥ 1-c` and
  every admissible family `P k`, `C₀ · 𝔼_μ ent ≤ ∑ₖ wₖ 𝔼_{P k} ent(Π⁽ᵏ⁾)`). All theorems
  are proved from `Certifies`, so they apply verbatim to the paper's certificate.
  We use `C₀ ≥ 1` where the paper has `C > 1`.
* **Protocols by their `(0,0)`-value.** A protocol is modelled by `Π : ℝ → ℝ → ℝ`,
  `Π x y = Π_{x,y}(0,0)`, subject to the Fréchet bounds
  `max 0 (x+y-1) ≤ Π x y ≤ min x y`. Section 3 uses nothing else about protocols; all the
  facts it does use (`Π x 0 = 0`, `Π 1 1 = 1`, `Π 1 y = y`, `ent(Π) ≤ 1`) are derived from
  these bounds.
* **Index conventions.** In the hiding law, index `0 ↦ atom 1`, `1 ↦ atom 0`, `2 ↦ atom y`.
  In Theorem 3.4 the protocols are indexed by `Fin (K+1)` (so there is at least one) and
  index `0` is the i.i.d. protocol, characterised by the hypothesis
  `hiid : ∀ x y, Prot 0 x y = x * y`.
* **Weaker hypothesis on the i.i.d. class.** Theorem 3.4 in the paper gives the i.i.d.
  protocol its singleton class `{μ⊗μ}`. The Lean statements only assume
  `ContainsProduct (C 0)`, which is weaker (the singleton class satisfies it), so the Lean
  theorems are slightly stronger than the paper's.
* **Hiding witness for the class of all couplings.** The paper exhibits the
  maximal-correlation coupling there; since the class of all couplings imposes no
  constraint, we present the simpler mixture-of-two-products witness
  `P = q δ₁⊗δ₁ + (1-q) P₀⊗P₀`, `P₀ = (1-δ)δ₀ + δ δ_y`, for that class as well. It has
  `P(y,1) = P(1,y) = 0` and `P(y,y) = (1-q)δ² ≤ δ²`, which is what `AdmitsHiding` requires.
* **The limit `δ → 0` in (H)** is carried out by hand (no filters): `δ` is chosen below the
  hiding threshold of each of the finitely many classes (their minimum) and below
  `c(1 - 2 q w₀)`, which yields the contradiction directly.

## What is *not* formalised

* **Proposition 2.2** (the certificate itself: Gilmer's argument, the chain rule, the
  reduction to union-closed families). Nothing measure-theoretic or information-theoretic
  about families is in scope; the certificate is a hypothesis here.
* **The maximal-correlation classes of Lemma 3.3** (Yu's protocols). Their hiding witness
  needs continuity of singular values in the matrix entries; only the i.i.d.,
  all-couplings and mixture-of-products classes are formalised.
* **Sections 4–6**: the ideal-diagonal protocol, anything conditional (Theorem 6.2 and its
  hypotheses), and the numerical appendix.
* The exact constant `c** = 0.382885260…` is not computed as a fixed point; what is proved
  is the explicit numerical bound below.

## The numeric bound actually proved

`refined_ceiling_numeric : c ≤ 3829/10000`, i.e. `c ≤ 0.3829`, under the hypotheses of
Theorem 3.4 plus `0 < c ≤ 1/2` (the range of Proposition 2.2). This is the target bound of
the specification (the paper's value is `c** = 0.382885260…`, and the margin at
`c = 0.3829` is `≈ 1.4·10⁻⁵` with the entropy bounds above). Since
`0.3829 < c_ceil = 0.3830992976…`, this already shows *formally* that the refined ceiling
is strictly below the product ceiling.

The proof is the paper's: `fixed_point_form` at `x = 0.6909` gives, after clearing the
denominator, `x·ent(x) ≤ (1-c) - (1-ent(x²))/2`; the rigorous entropy bounds and `c > 0.3829`
contradict it.

## Build

Fresh clone (needs network for Mathlib and its cache):

```bash
lake exe cache get
lake build
```

Full check (build, `sorry` scan, `#print axioms` scan):

```bash
bash check.sh
```

`check.sh` exits `0` only if `lake build` succeeds, no `sorry` appears in the build output
or in the sources, and every main theorem depends on no axioms beyond the three allowed.

Toolchain: `leanprover/lean4:v4.23.0`, Mathlib pinned at tag `v4.23.0`
(commit `37df177aaa770670452312393d4e84aaad56e7b6`).

## `#print axioms` output

```
'UnionClosedCeiling.product_ceiling' depends on axioms: [propext, Classical.choice, Quot.sound]
'UnionClosedCeiling.hiding_bound' depends on axioms: [propext, Classical.choice, Quot.sound]
'UnionClosedCeiling.diagonal_bound' depends on axioms: [propext, Classical.choice, Quot.sound]
'UnionClosedCeiling.fixed_point_form' depends on axioms: [propext, Classical.choice, Quot.sound]
'UnionClosedCeiling.refined_ceiling_numeric' depends on axioms: [propext, Classical.choice, Quot.sound]
'UnionClosedCeiling.containsProduct_iidClass' depends on axioms: [propext, Classical.choice, Quot.sound]
'UnionClosedCeiling.containsProduct_allCouplings' depends on axioms: [propext, Classical.choice, Quot.sound]
'UnionClosedCeiling.containsProduct_mixtureOfProducts' depends on axioms: [propext, Classical.choice, Quot.sound]
'UnionClosedCeiling.admitsHiding_allCouplings' depends on axioms: [propext, Classical.choice, Quot.sound]
'UnionClosedCeiling.admitsHiding_mixtureOfProducts' depends on axioms: [propext, Classical.choice, Quot.sound]
```

## Files

```
UnionClosedCeiling/Entropy.lean    binary entropy in bits and its basic bounds
UnionClosedCeiling/Framework.lean  laws, couplings, protocols, classes, the certificate,
                                   the two adversarial laws and their evaluations
UnionClosedCeiling/Ceiling.lean    Theorem 3.1
UnionClosedCeiling/Refined.lean    numerical entropy bounds; Theorem 3.4 (H), (D),
                                   fixed-point form, numerical corollary
UnionClosedCeiling/Classes.lean    Lemma 3.3 for the three formalised classes
UnionClosedCeiling.lean            imports everything, #print axioms for each main result
AxiomCheck.lean                    stand-alone axiom check used by check.sh
check.sh                           build + sorry scan + axiom scan
```
