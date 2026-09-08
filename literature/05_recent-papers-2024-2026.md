# 2024–2026 papers citing Gilmer (arXiv:2211.09055) or otherwise on the union-closed constant

Source: Semantic Scholar citations API for arXiv:2211.09055, filtered to
2024–2026, plus targeted arXiv search. One-line relevance note each.

## 2024

1. **arXiv:2412.18740** — "Chain Conditions and Optimal Elements in
   Generalized Union-Closed Families of Sets" (published *Order*,
   doi:10.1007/s11083-025-09717-w) — generalizes the conjecture's setting to
   families with chain-condition axioms; check for a weakened-hypothesis
   version of the entropy bound.
2. **arXiv:2412.18622** — "Entropy approach for a generalization of Frankl's
   conjecture" — directly extends the Gilmer-style entropy method to a
   generalized conjecture; high relevance, read in full.
3. **arXiv:2412.08075** — "When entropy meets Turán: New proofs and
   hypergraph Turán results" (doi:10.1112/jlms.70473) — uses union-closed-style
   entropy techniques for Turán-type problems; relevant for technique
   transfer, not the constant itself.
4. **arXiv:2412.03862** — "Frequent elements in union-closed set families"
   (Das–Wu) — proves Nagel's conjecture for k≥2 and an asymptotic
   ψ-fraction bound for k-th most frequent elements; see
   04_structural-facts.md. High relevance.
5. **DOI:10.1007/s00373-024-02834-0** — "Several Minimality Concepts Related
   to Frankl's Conjecture" — structural/minimality framework paper; check
   relevance to minimal-counterexample bounds.
6. **arXiv:2411.06588** — "Symmetric Union Closed Families" — restricts to
   symmetric families (relevant since the Chase–Lovett sharpness example is
   itself Sn-symmetric — worth checking if this paper's results say anything
   about symmetric families specifically beating or matching ψ).
7. **arXiv:2409.17050** — "A Cubical Perspective on Complements of
   Union-Closed Families of Sets" — topological/cubical-complex reframing;
   alternative-approach candidate, low immediate relevance to the constant.
8. **arXiv:2409.02221** — "A Study On The Graph Formulation Of Union Closed
   Sets Conjecture" — graph-theoretic reformulation (the "1-added-vertex"
   or "FC-family" graph translation); alternative approach.
9. **arXiv:2408.11213** — "On supratopologies, normalized families and Frankl
   conjecture" — topological generalization; low direct relevance.
10. **arXiv:2405.10639** — "Note on the union-closed sets conjecture and
    Reimer's average set size theorem" — see item (ii) in
    04_structural-facts.md; directly relevant, examines whether Reimer's
    condition can be strengthened toward the frequency conclusion.

## 2025

1. **arXiv:2511.19833** — "Average-Rare Order Ideals in Functional
   Preorders" — order-theoretic generalization; relevance unclear without
   full read.
2. **arXiv:2509.12537** — "An averaging result for union-closed families of
   sets" — proves: if a "separating" family A has height h=4 (≤ n) and
   |B| ≤ 2 (a companion/complement parameter), the average member-set size of
   A is at least n/2. A structural averaging result in the Reimer family;
   relevance to the entropy method unclear, worth a full read given the
   explicit n/2 threshold (matches the conjectured frequency constant in
   spirit, for a different statistic).
3. **arXiv:2508.17661** — "Spacer: Towards Engineered Scientific
   Inspiration" — appears to be an AI-for-discovery tool paper that cites
   Gilmer's problem as a use case/benchmark rather than proving new math on
   it; check for any concrete union-closed output before assuming pure
   AI-tooling relevance (see 06_ai-optimization-tracker.md).
4. **arXiv:2504.13454** — "On the Averaging Problem of Ideal Families Related
   to Frankl's Conjecture with Formal Proof by Lean 4" — a **formally
   verified (Lean 4)** partial result; high relevance for the campaign's
   formalization interests, and useful as a template if this campaign later
   wants machine-checked lemmas.
5. **arXiv:2504.13347** — "Partial results for union-closed conjectures on
   the weighted cube" — weighted/continuous generalization of the cube
   setting the entropy method operates in; check for weighted analogues of
   Lemma 5.
6. **arXiv:2501.02637** — "Isomorphism in Union-Closed Sets" — structural/
   classification angle, low direct relevance to the constant.

## 2026

1. **arXiv:2608.24388** — "A unified spectral bound for color-critical
   graphs via a weighted Turán theorem" — technique-transfer paper, not
   directly about the union-closed constant.
2. **arXiv:2607.26425** — "Supersaturation in union-closed families of sets"
   — supersaturation (how much *more* than the extremal count forces
   structure) is a classic lever for pushing constants past a barrier in
   other Turán-type problems; **high relevance, read in full**.
3. **arXiv:2607.24414** — "Entropy Methods in Combinatorics"
   (doi:10.1137/25m180874x) — broad recent survey of entropy methods; likely
   discusses Gilmer/Chase–Lovett/ψ explicitly as a flagship example (full text
   not accessible via fetch here beyond the abstract — recommend a follow-up
   fetch of the PDF/HTML for its union-closed section specifically).
4. **arXiv:2605.08676** — "Moonflowers and efficient code sparsification" —
   coding-theory technique paper citing the entropy method; low direct
   relevance.
5. **arXiv:2605.01508** — "Multiplicative Error Set System Sparsification: A
   Simpler Proof via Chain Length Contraction" (doi:10.4230/LIPIcs.ICALP.
   2026.44) — set-system sparsification, technique-adjacent, low direct
   relevance to the constant.
6. **arXiv:2601.19327** — "A generalization of Boppana's entropy
   inequality" — **directly relevant**: Boppana's inequality is the core
   "Lemma 5" underlying the ψ = (3−√5)/2 bound; a generalization of it is a
   strong candidate for pushing past ψ or explaining exactly why ψ is a hard
   wall for this inequality family. **Highest-priority follow-up read.**

## Overall read on 2024–2026 activity

No paper in this list claims to beat ψ (or Liu's 0.38271) for the *exact*
conjecture. The two highest-value follow-ups for this campaign are
**arXiv:2601.19327** (generalizing the exact inequality that caps the entropy
method at ψ) and **arXiv:2607.26425** (supersaturation, a technique class
historically used elsewhere to break through barriers of exactly this "the
current method is provably sharp for a relaxed version of the problem" type).

## Source

- Semantic Scholar citations query:
  https://api.semanticscholar.org/graph/v1/paper/arXiv:2211.09055/citations?fields=title,year,externalIds&limit=200
