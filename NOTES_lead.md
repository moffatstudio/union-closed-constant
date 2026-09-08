# Lead's working notes (self-derived, before reading the transcripts) — 2026-09-08

Notation. F ⊆ 2^[n] union-closed, m=|F|. A,B random sets with marginals uniform on F, C = A∪B ∈ F, so H(C) ≤ log m = H(A).
h = binary entropy (bits). For a prefix a ∈ {0,1}^{i-1} write u_i(a) = P(A_i = 0 | A_{<i} = a). Frequency of i: P(A_i=1) = E[1-u_i] ≤ p.

## The iid method (Gilmer / AHS / Chase–Lovett / Sawin / Pebody), re-derived
H(C) = Σ_i H(C_i | C_{<i}) ≥ Σ_i H(C_i | A_{<i}, B_{<i}) = Σ_i E h(U_i V_i), U_i,V_i iid copies of u_i(prefix).
H(A) = Σ_i E h(U_i).  Need E h(UV) ≥ E h(U) whenever E U ≥ 1-p.
Lemma (verified numerically, code/check_psi_lemma.py): h(uv) ≥ (φ/2)(u h(v) + v h(u)), φ=(1+√5)/2, equality iff u=v=1/φ.
⇒ E h(UV) ≥ φ E[U] E[h(U)] ≥ φ(1-p) E h(U) ≥ E h(U) iff p ≤ 1-1/φ = ψ = (3-√5)/2.
Extremal: U ≡ 1/φ, i.e. every conditional 1-probability equals ψ; h(u²)=h(u) ⇔ u²=1-u ⇔ u=1/φ.
Two-point check: U ∈ {u0, 1}, P(U=u0)=q; violation iff q h(u0²) < (2q-1) h(u0); inf violating frequency = ψ (u0→1/φ, q→1).

## Reformulation: the sequential-coupling game (my proposed general framework)
For ANY coupling π of (A,B) with the right marginals:
  H(C) ≥ Σ_i E h(s_i(a,b)),   s_i(a,b) = P(A_i=0, B_i=0 | A_{<i}=a, B_{<i}=b),
  H(A) = Σ_i [ H(A_i | A_{<i},B_{<i}) + I(A_i ; B_{<i} | A_{<i}) ].
Class S ("sequential couplings"): build π coordinate by coordinate — given prefixes (a,b), choose ANY joint law of (A_i,B_i)
with marginals Bern(1-u_i(a)), Bern(1-v_i(b)). Then marginals of A,B are automatically uniform on F, the mutual-information
loss term vanishes (A_i ⊥ B_{<i} | A_{<i}), and
  H(C) - H(A) ≥ Σ_i E_{(a,b)} [ h(s_i(a,b)) - ½(h(u_i(a)) + h(v_i(b))) ],   s_i ∈ [max(0,u+v-1), min(u,v)]  (Fréchet interval).
Contains: iid (s=uv), A=B (s=u, gain 0), Sawin's mixture, Liu's conditionally-iid couplings (to check against transcript).
Pointwise gain g(u,v) = max_{s∈Fréchet} h(s) - ½(h(u)+h(v)) is ≥ 0 whenever u,v ≥ 1/2. Loss only at (prefix, coordinate)
pairs with conditional 1-probability > 1/2. The policy also shapes the joint law of future prefixes — a dynamic game.
Barrier for a class = a family F (any F, not nec. union-closed: the method only uses H(C) ≤ log|F|) on which no policy
in the class has positive total gain. Chase–Lovett's ψ-barrier is NOT a barrier for S, because "approximately union-closed"
is defined for iid pairs and a non-iid coupling can have P(A∪B ∉ F) ≫ ε.

## Questions to settle from the transcripts
1. Is S (sequential couplings) already Yu's "coupling framework"? What sub-class did Yu/Cambie/Liu actually optimise?
2. Where exactly is the mutual-information term handled in Liu's conditionally-iid class?
3. What is Cambie's extremal distribution for the mixture class (what feature of it defeats the mixture)?
4. Does the "uniform on F" constraint (all leaf probabilities equal) get used anywhere? (It is lost in the per-coordinate relaxation.)

## Findings from the DP experiments (2026-09-08, 12:00–12:30)
- Optimal policy structure on symmetric families (code/policy_dump.py): comonotone (A_i=B_i) whenever the common conditional
  0-probability u ≤ 1/2; when u > 1/2 pick s ≈ 1/2 (max entropy of the union bit); mismatched prefixes also get s ≈ 1/2.
  ⇒ candidate fixed rule **GREEDY**: s = clamp(1/2, Fréchet(u,v)).
- Greedy vs full class: symmetric families n=24 — greedy ≈ full DP (middle slice +0.585 vs +0.625). But exhaustive n=4:
  greedy barrier p=3/7 (F={∅,{2},{2,3},{1,2,3},{4},{1,4},{1,3,4}}), full class none below 1/2. Random search: greedy fails at
  p=4/9 (n=5,6) and 3/7 (n=7,8); full class no failure found for p ≤ 0.45, n ≤ 7.
- Loss mechanism (code/dissect.py): after divergence, states with (u,v)=(0,1/2): the element is forced into A, so B's bit
  entropy is destroyed by the union: gain h(0) − ½(0+1) = −1/2. Full class avoids by decoupling less / realigning.
- Relaxed adversary (any tree of conditionals, marginals ≤ p; code/relaxed_game.py): n=2 the coupler wins for every p<1/2.
- **No frequency-only potential.** For an inductive proof V(a,b) ≥ Σ_i ψ(f_i(a), f_i(b)) one needs ψ convex along the
  comonotone mixtures (forced when u=v ≤ 1/2), and coordinates with u=v=1 or u=v=1/2 give zero gain ⇒ φ(f):=ψ(f,f) satisfies
  φ(0) ≤ 0, φ(1/2) ≤ 0, φ convex ⇒ φ ≤ 0 on [0,1/2]. So the potential must carry entropy terms (as Gilmer's does:
  Σ_i (φ(1−f_i) − 1)·H(A_i | A_{<i})). Natural state for an induction: per-coordinate (frequency, conditional entropy) pairs,
  both Jensen-exact under mixing.

## The conditionally-iid class, its ceiling, and the design space (2026-09-08, 13:30)
Liu's framework (transcript literature/2306.08824_liu.md): protocol Π_{s,t} = memoryless sequential coupling rule; provable
strength set by the class C(µ) of joint laws of the two prefix conditional means the protocol can induce.
iid: C1 = {µ⊗µ}. Sawin max-entropy: C2 = all symmetric couplings (adversary picks Cambie's anti-correlated law → 0.38234).
Conditionally iid given shared U: C3 = mixtures of products (Liu Thm 9: two components suffice, ANY such protocol).
General conditionally-iid protocol: r_x(u) = P(bit=0 | U=u) with mean x; Π(0,0) = xy + K(x,y), K = Cov(r_x, r_y), any
realizable PSD kernel. Liu used rank-1 K = f(x)f(y), f = x(1-x), well inside the realizability bound f ≤ min(x,1-x).
My evaluator code/kernel_game.py reproduces Liu: min ratio 1.000000000 at (c',β*) with his adversary q=0, P0 = .8936δ_{.6908} + .1064δ_0.

**Why Liu's optimum is where it is.** The adversary picks x* with x*² + f(x*)² = 1 − x*² (eq. 87): the kernel term is
h-neutral there (h symmetric about 1/2), and c' = 1 − x* h(x*)/h(x*²) from the iid balance p h(x²) = h(x). A larger kernel
pushes x* up, and c(x) = 1 − x h(x)/h(x²) is increasing for x > 1/φ.
**Ceiling of the whole conditionally-iid class (against C3, even against C1):** K(x,x) = Var(r_x) ≥ 0, so for x² ≥ 1/2
no conditionally-iid protocol gains on the diagonal; adversary P0 = pδ_{x*} + (1−p)δ_0, q = 0, x* = 1/√2 gives
  c ≤ 1 − (1/√2)·h(1/√2)/h(1/2) = 0.3830993.
So any conditionally-iid + iid mixture is capped at 0.38310; Liu's 0.382709 leaves ≈ 0.0004 of room.
**Candidate kernel** f_ideal(x) = min(x,1−x) for x ≤ 1/2, sqrt(1/2 − x²) for x ∈ [1/2, 1/√2], 0 beyond (rank 1, r_x = x ± f):
realizable; xy + f(x)f(y) ≤ 1/2 wherever f(x)f(y) > 0 ⇒ h(xy+K) ≥ h(xy) pointwise (dominates iid on every pair, and
achieves the ideal diagonal). Sweeps running: code/sweep_ideal_b*.log.
**Beyond the ceiling:** only a non-conditionally-iid term can gain at the ceiling adversary — Sawin's anti-correlated
protocol has Π(0,0) = 1/2 at (x*,x*) = (1/√2,1/√2) (s = 0.293, min(s+t,1/2) = 1/2). Liu's eq. (29) is the 3-protocol
mixture (iid, Sawin, cond-iid); Liu dropped the Sawin term numerically. Its adversary class C2 = all symmetric couplings
with margin µ: for fixed µ the worst coupling is a transportation LP. Implementing code/kernel_game3.py.
