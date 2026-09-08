# Structural facts about exact union-closed families

Facts that are true for **exact** union-closed families and that could in
principle be combined with the entropy method. Several of these are proved by
methods that do NOT relativize to approximately union-closed families — see
SYNTHESIS_lane4.md for which ones look most promising as "levers."

## (i) Minimal-counterexample size bounds

- **Roberts–Simpson:** if q = |U(F)| (universe size) is minimal among all
  union-closed counterexamples, then |F| ≥ 4q − 1. Combined with the universe
  bound below, this gives **|F| ≥ 51** for any minimal counterexample.
- **Vučković–Živković:** the conjecture holds by exhaustive computer
  verification for all union-closed families with universe size **n ≤ 12**;
  equivalently any counterexample needs universe size **≥ 13**.
  ⇒ **A minimal counterexample has |F| ≥ 51 sets over a ≥13-element universe.**
- Note: the general folklore verification-by-computer bound has moved over
  the decades from n ≤ 7 (Poonen-era) up to n ≤ 12 (Vučković–Živković); some
  secondary sources conflate this with a different parameter ("largest set
  size in F") — the search results here were inconsistent on that point and
  should be double-checked against the primary Vučković–Živković paper before
  being relied on for anything beyond the n ≤ 12 / |F| ≥ 51 headline figures.
- Source discussion: https://arxiv.org/html/1706.06167, journal version
  Discrete Mathematics (2023), doi:10.1016/j.disc.2023.113430

## (ii) Reimer's average set size theorem (2001/2003)

Every union-closed family F satisfies: the **average set size** of members of
F is at least **½ log₂|F|**. Proved via "Reimer's condition," a stronger
structural property that all union-closed families satisfy (related to
compression/shifting arguments and filters). Important caveat, explicitly
noted in the literature (e.g. arXiv:2405.10639, Raz): Reimer's condition alone
is **not sufficient** to imply the ≥|F|/2 frequency conclusion — it bounds
average size, not any individual element's frequency, so it is a genuinely
different structural axis from what the entropy method controls.

- Note added 2024: arXiv:2405.10639 ("Note on the union-closed sets
  conjecture and Reimer's average set size theorem") revisits exactly this
  gap — worth reading in full if pursuing this lever.

## (iii) Knill's and Wójcik's frequency bounds (pre-Gilmer state of the art)

- **Knill:** some element appears in at least **(|F| − 1)/log₂|F|** sets.
- **Wójcik (1992):** improved the constant to **2.4·|F|/log₂|F|** for large
  |F|.
- Both are logarithmic-type bounds, superseded in absolute strength by
  Gilmer's constant bound for large |F|, but they degrade differently (they
  give nontrivial guarantees that scale with |F|, unlike a flat 0.01 or ψ
  fraction) and were the state of the art the entropy method was explicitly
  built to beat.
- **2024 follow-up, Das–Wu, arXiv:2412.03862 ("Frequent elements in
  union-closed set families"):** proves **Nagel's conjecture** for k ≥ 2 — the
  k-th most popular element of F is contained in at least
  |F|/(2^(k−1) + 1) sets — and separately establishes an asymptotic bound of
  (ψ − o(1))·|F| = ((3−√5)/2 − o(1))·|F| for the k-th most frequent element in
  large families. (Direct comparison of this paper's bound to Wójcik's
  2.4|F|/log₂|F| could not be confirmed from the fetched abstract alone and
  should be checked against the full text.)

## (iv) Karpas' large-family results, arXiv:1708.01434, "Two Results on Union-Closed Families"

- **Author:** Ilan Karpas
- **Result 1:** there is an absolute constant c > 0 such that any union-closed
  F ⊆ 2^[n] with **|F| ≥ (½ − c)·2ⁿ** has some element in at least half of the
  sets of F. (I.e. the conjecture is confirmed for families that are a
  constant fraction close to the full power set — a genuinely different
  regime from "small" F.)
- **Result 2:** for any union-closed F ⊆ 2^[n], the number of sets **not** in F
  that "cover" some set of F (i.e., differ from a member of F by exactly one
  added element) is at most 2^(n−1), with tight examples. This bounds how much
  "room to grow" F has at its boundary — a purely combinatorial/covering fact
  with no obvious entropy-method analogue.

## (v) Large-family results: Balla–Bollobás–Eccles

- **Result:** any union-closed family with |F| ≥ (2/3)·2ⁿ sets satisfies the
  conjecture. Proved via the Kruskal–Katona theorem combined with
  up-compression, by determining the **minimum possible average total set
  size** of a union-closed family of given size |F| — the extremal minimizer
  is the "Hungarian family" H(n).
- **Known limitation (explicit in the literature):** the Kruskal–Katona/
  up-compression method used here provably **cannot** give a constant better
  than 2/3 — it hits a hard wall of its own, distinct from the entropy
  method's ψ wall. Tom Eccles' follow-up, "A stability result for the
  union-closed size problem" (arXiv:1311.2298), pushes on the same technique's
  stability but does not break the 2/3 barrier for the frequency conclusion
  itself.

## (vi) Special-structure results

- **Doubletons:** if F contains a 2-element set {x, y}, the conjecture holds
  for F. Proof sketch (folklore, appears in multiple surveys): partition F by
  membership of x, y into F₀, Fₓ, F_y, F_{xy}; union-closedness forces
  |F_{xy}| ≥ |F₀|, and then x or y (whichever of Fₓ, F_y is larger) is
  frequent. Singletons are the trivial base case.
- **Height-based results, arXiv:2112.06659:** introduces the "height number"
  H(F) of a union-closed family (a lattice-theoretic parameter, 1 ≤ H(F) ≤ n)
  and proves the conjecture holds whenever **H(F) ≤ 3 or H(F) ≥ n−1**. Framed
  explicitly by the authors as a partial-coverage strategy: if all height
  values could be handled this would resolve the conjecture in full — the
  paper handles only the two extremes so far.
- **Poonen's classical small-universe/small-largest-set results:**
  Poonen (1992, *J. Combin. Theory Ser. A* 59, 253–268) proved cases with
  small universe size, later extended computationally (Sarvate–Renaud,
  Lo Faro, Gao–Yu, Roberts) — these numbers are frequently conflated across
  secondary sources between "universe size ≤ k" and "largest set size ≤ k"
  framings; **the exact reported figures here (7, 18, 24, 27, 32, 40) could
  not be pinned to a single consistent parameter from search snippets alone**
  and should be verified against Poonen's original paper before being used —
  flagged as a to-verify item rather than a confirmed fact.

## Sources

- Roberts–Simpson / universe bound discussion: https://arxiv.org/html/1706.06167
- Reimer's theorem discussion: https://arxiv.org/abs/2405.10639
- Das–Wu (Nagel's conjecture): https://arxiv.org/abs/2412.03862
- Karpas: https://arxiv.org/abs/1708.01434
- Balla–Bollobás–Eccles / Eccles stability: https://arxiv.org/abs/1311.2298
- Height-number paper: https://arxiv.org/abs/2112.06659
