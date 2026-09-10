# A ceiling for single-letter protocol arguments (lead, 2026-09-08)

> **Machine-checked (2026-09-10).** Both theorems below are formalised in Lean 4 / Mathlib in
> `lean/`, on a finite model of the framework whose certificate hypothesis is implied by the
> one used here (so the Lean theorems apply to these statements). Map:
>
> | Statement in this file | Lean name | File |
> |---|---|---|
> | **Theorem (ceiling)**, `c_ceil = 1 - h(1/√2)/√2` | `product_ceiling`, `cCeil` | `lean/UnionClosedCeiling/Ceiling.lean` |
> | **Theorem (refined ceiling)**, inequality (H) `2·w_iid·(1−c) ≥ 1` | `hiding_bound` | `lean/UnionClosedCeiling/Refined.lean` |
> | **Theorem (refined ceiling)**, inequality (D) | `diagonal_bound` | `lean/UnionClosedCeiling/Refined.lean` |
> | the joint (H)+(D) fixed-point form | `fixed_point_form` | `lean/UnionClosedCeiling/Refined.lean` |
> | the numerical consequence | `refined_ceiling_numeric : c ≤ 3829/10000` | `lean/UnionClosedCeiling/Refined.lean` |
> | the classes: all couplings, mixtures of products, i.i.d. singleton contain products / admit hiding | `containsProduct_*`, `admitsHiding_*` | `lean/UnionClosedCeiling/Classes.lean` |
>
> What Lean proves numerically is `c ≤ 0.3829`, not the exact fixed point `c** = 0.382885260…`
> (a real-number fixed point, evaluated in `verify.py`). The maximal-correlation classes are not
> formalised. See `lean/README.md` and `lean/CERTIFICATE.md`.

**Setting** (Liu 2306.08824, Prop. 3). A *protocol* Π assigns to each pair (s,t) of conditional inclusion probabilities a
joint law Π_{s,t} on {0,1}² with marginals Bern(s), Bern(t); it generates the two copies coordinate by coordinate.
Let C_Π(µ) be any class of couplings of µ with itself that contains every joint law of (S_i, T_i) := (P(X_i=1|X^{i-1}), P(Y_i=1|Y^{i-1}))
that Π can induce on some family. The certificate for a constant c with protocols Π^(1..K) and weights w_k is
   Σ_k w_k inf_{P ∈ C_k(µ)} E_P[ h(Π^(k)_{S,T}(0,0)) ] ≥ E_µ[h(S)]    for every µ on [0,1] with E_µ[S] ≤ c.      (16)

**Theorem (ceiling).** Suppose every class C_k(µ) contains the product law µ⊗µ. Then (16) can only hold for
   c ≤ c_ceil := 1 − (1/√2)·h(1/√2)/h(1/2) = 1 − h(1/√2)/√2 = 0.3830992976…   (h in bits, h(1/2)=1).
In particular this bounds the iid protocol (C={µ⊗µ}), Sawin's max-entropy protocol (C = all symmetric couplings),
Yu's maximal-correlation protocols (products have ρ=0), every conditionally-iid protocol (products are rank-one mixtures),
and every weighted mixture of these.

**Proof.** Work with zero-probabilities x = 1−s. Take µ = p·δ_{x*} + (1−p)·δ_0 with x* = 1/√2, i.e. S ∈ {1 − 1/√2, 1}:
the element is surely present (s=1) with probability 1−p, and present with probability 1−1/√2 otherwise.
E_µ[S] = 1 − p x*.  Present the product coupling P = µ⊗µ to every protocol (allowed by hypothesis).
- On pairs containing an s=1 coordinate, Π_{s,t}(0,0) = 0 for every protocol (the bit is surely 1), so h(·)=0.
- On the pair (x*,x*): Π(0,0) lies in the Fréchet interval [2x*−1, x*] and h(Π(0,0)) ≤ 1 = h(x*²), since x*² = 1/2.
Hence for every k,  E_{µ⊗µ}[h(Π^(k)(0,0))] ≤ p²·1, while E_µ[h(S)] = p·h(x*).  (16) forces p² ≥ p h(x*), i.e. p ≥ h(1/√2),
so E_µ[S] = 1 − p/√2 ≤ 1 − h(1/√2)/√2 = c_ceil. Thus for any c > c_ceil the law µ with p = h(1/√2) (mean exactly c_ceil < c)
violates (16) — actually gives equality, and perturbing p slightly below h(1/√2) gives a strict violation with mean < c. ∎

**Remarks.**
1. The iid protocol attains h(Π(0,0)) = 1 at (x*,x*) by itself; the ceiling is exactly the point where iid stops losing
   on the diagonal. Gilmer's ψ = 0.381966 is lower only because for x < 1/√2 the iid protocol under-uses the diagonal
   (h(x²) < 1); the whole gain of Sawin/Yu/Cambie/Liu and of our kernels is recovering that diagonal deficit while
   controlling what the adversary can do with mixtures.
2. Adding a non-product-containing protocol cannot help unless its own class excludes products. The comonotone
   (A=B) protocol has class {diagonal laws} and gives exactly E[h(S)] — no gain. Any protocol that ever decouples the
   two chains lets a family drive the prefix pair towards independence, so escaping the ceiling needs a *tensorising
   invariant that rules out near-independent prefixes* — none is known.
3. The β=0.3 sweep figure 0.382953 was an optimiser miss on the hiding law and is withdrawn; see the refined section below.

---
# Refined ceiling for protocol mixtures containing an iid term (lead, 2026-09-08, 16:00)

**Second adversary (component hiding).** For c ∈ (0,1/2), q := 1−c, small δ>0 and y ∈ (0,1), let
   µ_δ = q·δ_{x=1} + (1−q)·[(1−δ)·δ_{x=0} + δ·δ_{x=y}]      (x = zero-probability; x=1: element surely absent, x=0: surely present).
E_µ[X] = q + (1−q)δy ≥ 1−c, and E_µ[h(X)] = (1−q)δ·h(y). Only pairs (y, 1) and (y, y) can carry union-bit entropy:
(y, 0)-pairs are forced (bit surely 1) and (1,1),(0,0),(0,1) carry none. The (y,y) mass is O(δ²).
- iid protocol (class {µ⊗µ}): (y,1)-mass 2q(1−q)δ, giving E h(Π(0,0)) = 2q(1−q)δ h(y) + O(δ²).
- any protocol k whose class C_k(µ_δ) contains a coupling with P(S=y, T=1) = 0 — true for C2 (all couplings), for C3
  (put the y-atom in the same product component as the 0-atoms: P = q δ_1⊗δ_1 + (1−q) P0⊗P0, P0 = (1−δ)δ_0 + δδ_y), and for
  every maximal-correlation class ρ>0 (the hiding coupling has ρ_m = O(√δ)) — receives only the O(δ²) diagonal mass.
Hence as δ→0 the certificate (16) with iid weight w_iid forces   2·w_iid·(1−c) ≥ 1,   i.e.  w_iid ≥ 1/(2(1−c)).      (H)
(Liu's Lemma 7 is the iid-only version of this limit: liminf ≥ 2c̄.)

**First adversary (diagonal).** The two-point law p·δ_{x*} + (1−p)·δ_0 with independent prefixes gives, for any protocols,
   w_iid·p²·h(x*²) + (1−w_iid)·p²·1 ≥ p·h(x*)   ⇒   c ≤ 1 − x*·h(x*) / (w_iid·h(x*²) + 1 − w_iid)   for every x* ∈ [1/2, 1/√2],
using h(Π(0,0)) ≤ 1 on the diagonal; for x* ≥ 1/√2 the bound is 1 − x* h(x*)/h(x*²) (no protocol beats iid there).      (D)

**Theorem (refined ceiling).** For every mixture of the iid protocol with protocols whose classes admit component hiding
(all classes in the literature: Sawin/C2, Yu/max-correlation, Liu/conditionally-iid, and any realizable kernel K),
the certified constant satisfies c ≤ c** where c** is the joint solution of (H) with equality and (D) minimised over x*:
   **c** = 0.382885260…,   w_iid = 1/(2(1−c**)) = 0.810222,   β = 1 − w_iid = 0.189778,   binding x* = 0.690908.**
**Attainment.** The rank-one kernel f_ideal (ideal diagonal h=1 on [1/2,1/√2]) with β = β** = 0.189778 certifies every c < c** = 0.382885
(c = 0.38284 certified with margin 7e-5; at β = 0.19 exactly, (H) caps c at 0.382716 — the earlier 'β=0.19 certifies 0.382885' was a two-point-only figure and is withdrawn). Liu's kernel is at
0.382709 because its diagonal x²+x²(1−x)² is not ideal; Cambie's exact 0.3823455 for Sawin's class is below because
the anti-correlated class C2 also lets the adversary shrink the diagonal mass to 2p−1.
**Consequence.** The whole single-letter "protocol + coupling class" method, in every form used since 2022, is exhausted at
0.382885. Going further requires an argument in which the iid term is not needed to handle degenerate laws — e.g. a
tensorising constraint that forbids hiding a tiny-mass atom — or a genuinely non-single-letter use of union-closure.
