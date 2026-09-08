# Lane 4 synthesis: barriers, structure, and alternative approaches

Files in this lane: `01_ellis-ivan-leader.md`, `02_gilmer-and-chase-lovett.md`,
`03_tao-and-scandone.md`, `04_structural-facts.md`,
`05_recent-papers-2024-2026.md`, `06_ai-optimization-tracker.md`, and
`../code/chase_lovett_example.py` (numerically verified).

## The hard barrier: ψ = (3−√5)/2 ≈ 0.381966

Chase–Lovett (arXiv:2211.11689) prove — and this campaign's script
numerically confirms — that ψ is not a weakness of a particular proof but the
**true extremal constant for approximately union-closed families**. Their
Example 1.4 construction (F1 ∪ F2, a single Hamming-weight layer plus an
upward-closed cap) is (1−o(1))-approximately union-closed while every element's
frequency converges to exactly ψ from above. Liu's current record of 0.38271
is a small refinement of the same entropy machinery (coupling), not evidence
that the machinery itself can go much further: the whole family of proofs
unified around "Lemma 5" (a sharp binary-entropy inequality, cleanly reproved
by Boppana) is sharp at ψ for the relaxed (approximate) problem. Scandone's
February 2023 attempt to push past this with a convex-combination refinement
failed for a diagnosable reason (a conditional distribution silently replaced
by its mean — see `03_tao-and-scandone.md`), and the verdict attributed to Tao
is explicit: a single global scalar parameter is not enough; what's needed is
"a more involved construction."

## Levers the entropy method has not yet used

These are facts that hold for **exactly** union-closed families but are
**false, or not obviously true, for Chase–Lovett's (1−o(1))-approximate
family** — meaning they are structurally invisible to any proof (like the
current entropy method) that only ever uses the approximate-closure property
and treats near-misses as harmless.

1. **Exact closure forces exact recursive structure at every pair, not just
   almost every pair.** Chase–Lovett's construction tolerates a vanishing
   fraction of "bad" F1×F1 pairs (this campaign's Monte Carlo shows this
   fraction is already ≈0 by n≈20–30, i.e. structurally negligible almost
   immediately). Exact union-closedness means F1's own weight-k1 layer, if
   the family were genuinely exact, would need EVERY pairwise union to
   re-enter F — a combinatorially much more rigid condition than "almost
   every union does." Any argument that can extract a strict inequality from
   the *zero-tolerance* nature of exact closure (rather than a
   large-deviations tail bound, which is what the entropy method effectively
   uses) is invisible to Chase–Lovett's sharpness example by construction.

2. **Reimer's average-set-size theorem (½log₂|F|) is a genuinely different
   statistic from anything the entropy method tracks**, and — per the 2024
   note arXiv:2405.10639 — is explicitly *not* by itself known to relativize
   into a frequency bound. That gap is exactly the kind of thing worth
   attacking directly: if Reimer's condition (the stronger structural fact
   behind the average-size theorem, tied to compressions/shifting) could be
   combined with an entropy-style argument — rather than used as a separate,
   parallel bound — it is a genuinely unused structural axis. Untested
   against Chase–Lovett's example in the literature found here; worth
   checking directly (their F1 layer, being a single symmetric Hamming
   layer, has average set size ≈ ψn, which is far above ½log₂|F1| — so
   Reimer's bound alone is *not* violated by the sharp example, meaning it
   cannot on its own break ψ, but a refined/local version of Reimer's
   condition might still carry information the flat average bound discards).

3. **Karpas' covering-set bound** (# of sets outside F that cover a member of
   F is ≤ 2^(n−1), tight) is a purely combinatorial boundary-counting fact
   about exact union-closed families with no entropy analogue in the current
   literature. Because it counts *exact* covers (single-element extensions),
   it is sensitive to the same zero-tolerance structure as (1) above, and is
   a candidate for combination with an entropy-style counting argument on
   the "boundary" of F rather than on F itself.

4. **The Ellis–Ivan–Leader "small sets" result** is itself a barrier, not a
   lever, but it rules out an entire class of approaches (arguing via the
   unique smallest set) and thereby narrows the productive search space:
   any combination strategy should target facts about F's *frequent*
   structure or its *boundary*, not its minimal generators.

5. **Symmetric/near-symmetric structure.** Chase–Lovett's sharp example is
   fully S_n-symmetric (a union of Hamming layers). If a genuinely
   asymmetric structural fact — one that necessarily holds for exact
   union-closed families but has no reason to hold for a symmetrized
   approximate one — can be found (candidates: the doubleton/height-based
   results in `04_structural-facts.md`, items v–vi, all of which exploit
   *specific* small sets or lattice positions rather than symmetric layer
   counting), it automatically evades the sharpness example, since that
   example's whole force comes from coordinate symmetry making every
   element's frequency identical by construction. This is arguably the
   single cleanest structural distinction available: **any real union-closed
   family that is not coordinate-symmetric has more to exploit than
   Chase–Lovett's extremizer does, and the entropy method as currently
   formulated does not use asymmetry at all.**

6. **Boppana's inequality generalized (arXiv:2601.19327, 2026)** and
   **supersaturation for union-closed families (arXiv:2607.26425, 2026)** are
   the two most recent unread leads that could plausibly interact with (1)
   and (5) above — a generalized entropy inequality might have a strictly
   sharper form under an asymmetry hypothesis, and supersaturation techniques
   are historically exactly the tool used elsewhere to convert "extremal
   examples are sparse/rare" into "any non-extremal structure buys you a
   strictly better constant." Both are flagged as highest-priority reads,
   not yet digested in this pass.

## Bottom line for the campaign

Beating ψ (or even Liu's 0.38271) with anything resembling the current
entropy method is very unlikely to work, because Chase–Lovett proves the
method's natural domain (approximate closure) is already tight there. The
highest-leverage path is combining the entropy method with a fact that is
**exact-closure-specific and/or asymmetry-specific** — items (1), (3), and
(5) above are the cleanest candidates found in this pass, and
arXiv:2601.19327 / arXiv:2607.26425 are the most promising unread recent
papers for supplying the missing technical tool.
