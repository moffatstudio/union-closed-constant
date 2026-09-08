# Tao's role: the Scandone flawed-proof episode (Feb 2023)

**Correction to the task brief:** there is no dedicated Terence Tao blog post
("What's new") on Gilmer's argument or on Scandone's paper — a direct search
of terrytao.wordpress.com for "union-closed" returns no results. Tao's
documented involvement is instead as the person who **privately/publicly
identified the fatal flaw** in Raffaele Scandone's February 2023 claimed full
proof, and this episode is recorded second-hand in Gil Kalai's survey
(arXiv:2306.12351, "Progress on the union-closed conjecture and offsprings in
winter 2022–2023") and Kalai's blog. No primary Tao blog post exists to cite;
what follows is sourced from Kalai's account, which explicitly attributes the
diagnosis and the quoted remark to Tao.

## Scandone's paper, arXiv:2302.03484, "A proof of the union-closed sets conjecture"

- **Submitted:** 6 Feb 2023; **withdrawn** 8 Feb 2023 (v2), two days later.
- **Withdrawal note (author's own words):** "There is a mistake in the proof
  of Proposition 1.2, at the end of page 4."
- **Abstract (verbatim):** "We provide a proof of the union-closed sets
  conjecture, by means of a suitable refinement of the breakthrough
  entropy-approach introduced by Gilmer. The novelty here is to consider a
  convex combination of A and A∪B, where A, B are independent samples from the
  uniform distribution over a union-closed family."

## The failure mode (per Kalai's account, diagnosis attributed to Tao)

The claimed refinement tried to strengthen Gilmer's entropy inequality by
working with a random variable that is a **convex combination** of A and A∪B
(effectively: with probability t sample A, with probability 1−t sample A∪B,
for some mixing parameter). The error was that **a conditional probability
distribution was erroneously replaced by its expected value** at a key step of
Proposition 1.2 — i.e., an argument that needed to hold for the actual
(possibly highly variable) conditional law of some auxiliary random variable
was instead carried out only for its mean, silently discarding the variance/
tail behavior that the entropy inequality actually depends on. This is exactly
the kind of step where Jensen's-inequality-style slack hides a fatal gap: the
entropy functional is concave, and replacing a distribution by its mean
inside a concave functional evaluation is not generally valid without an
explicit convexity/majorization argument, which the paper did not supply.

## Tao's assessed verdict (quoted, per Kalai's survey)

> "the idea of modifying the union operation by Gilmer is promising, but a
> single global bit is not sufficient to do the job, and a more involved
> construction is needed."

### What "a more involved construction" would need

Read literally, this says: Scandone's fix used **one scalar mixing parameter**
(a single global bit/weight t deciding how much to blend A vs. A∪B) applied
uniformly. Tao's remark implies that any successful entropy-based refinement
along these lines needs the mixing/modification to be **data-dependent** —
e.g., a construction where the "how much to deviate from plain A∪B" decision
depends on the local structure of F (which elements are already frequent,
which sets are being unioned, etc.), rather than a single fixed global
parameter applied identically everywhere. This is consistent with the broader
diagnosis in the field: the entropy method as unified around Lemma 5 (Chase–
Lovett/Alweiss–Huang–Sellke/Sawin/Pebody/Boppana) already extracts everything
obtainable from a *symmetric, structure-blind* two-sample entropy inequality —
pushing past ψ = (3−√5)/2 requires injecting genuine union-closed-specific
structure (not just entropy bookkeeping) into the construction, exactly the
kind of asymmetric/adaptive move a single global convex-combination parameter
cannot supply.

## Timeline context (from Kalai's survey, arXiv:2306.12351)

| Date | Event | Constant |
|---|---|---|
| 16 Nov 2022 | Gilmer's breakthrough | 0.01 |
| ~20 Nov 2022 | Alweiss–Huang–Sellke, Chase–Lovett, Sawin, Pebody (independently) | ψ = (3−√5)/2 ≈ 0.381966 |
| Dec 2022–Jan 2023 | Sawin's suggested refinement; Yu computes via Krein–Milman | ≈0.38234 |
|  | Cambie proves this value sharp | — |
| Jan 2023 | Boppana: elegant calculus proof of the key Lemma 5 (via a 1989 result) | — |
| 6–8 Feb 2023 | Scandone claims full 1/2 proof; Tao identifies flaw; withdrawn | (claim retracted) |
| June 2023 | Liu: improved constant via a different coupling method | 0.38271... (current record) |

Also from the same period: Sawin and Ellis independently found a
counterexample (arXiv:2211.12401) to a *stronger* conjecture Gilmer had
proposed (which would, if true, have implied the full 1/2 bound) — an
independent, earlier confirmation that the naive way of trying to strengthen
the entropy method does not work, consistent with what later sank Scandone's
attempt.

## Sources

- Scandone (withdrawn): https://arxiv.org/abs/2302.03484
- Kalai survey: https://arxiv.org/abs/2306.12351
- Gilmer→ψ counterexample: https://arxiv.org/abs/2211.12401
- (Searched, no result: terrytao.wordpress.com for "union-closed")
