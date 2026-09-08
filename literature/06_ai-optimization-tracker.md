# AI-related activity: Tao's optimizationproblems tracker and related

## Terence Tao's optimizationproblems site

URL: https://teorth.github.io/optimizationproblems/

**Confirmed entry for the union-closed sets conjecture constant:**

- **Entry ID:** C6, "Union-closed sets conjecture constant"
- **Best known lower bound:** 0.38271 (matches Liu 2023, the record this
  campaign is trying to beat)
- **Best known upper bound:** 0.5 (the conjectured true value)
- **Detail page:** https://teorth.github.io/optimizationproblems/constants/6a.html

This confirms Liu's 0.38271 as the tracker's current recorded state of the
art as of this research pass — consistent with the campaign's stated current
record.

**Detail page (constants/6a.html), fetched in full:**

- **Problem statement (verbatim framing):** C6 = "the largest constant such
  that any union-closed family of sets on an N-element ground set has an
  element contained in at least C6 fraction of the sets."
- **Lower-bound chronology recorded by the tracker:** 0 (trivial) → 0.1 →
  (3−√5)/2 ≈ 0.381966 → "strictly greater than (3−√5)/2" → 0.38234 → 0.38271.
- **Key references table:** Frankl (1979 orig., page lists 1995 for the
  upper-bound formalization) for the 1/2 upper bound; Bruhn–Schaudt (2015)
  survey of the pre-Gilmer literature; the 2022 entropy-method cluster
  (Gilmer, Alweiss–Huang–Sellke, Chase–Lovett, Pebody, Sawin, Cambie, Yu); Liu
  (2023) for the current 0.38271 record via "conditional coupling."
- **Notable remark:** the page points to Matthew Aldridge's blog for a
  post-2015 survey (https://mpaldridge.github.io/blog/union-closed.html,
  surfaced independently in this pass's searches) and flags 2022 as an
  unusually concentrated burst of independent progress.

No AI-discovery-specific sub-problem, note, or attempt is recorded on this
page — the tracker treats C6 purely as a numeric target with a citation
trail, not as a problem earmarked for automated/AlphaEvolve-style search.

## AlphaEvolve / Erdős-problems site

No direct evidence was found in this pass of AlphaEvolve or a dedicated
Erdős-problems-style tracker entry specifically targeting the union-closed
sets constant. One tangential hit from the citation search
(05_recent-papers-2024-2026.md): **arXiv:2508.17661, "Spacer: Towards
Engineered Scientific Inspiration"**, which cites Gilmer's paper — this reads
as an AI-for-scientific-discovery tool paper using the union-closed problem
as an example/benchmark rather than reporting a new bound; this should be
read in full before drawing conclusions, as it was not independently verified
beyond its citation appearing in the Semantic Scholar list.

## Recommendation

This is the weakest-covered item in this lane — the tracker confirms the
current numeric record is on Tao's radar as an active target (with the 0.5
upper bound explicitly recorded as unresolved), but no AI-discovery-specific
attempt on this exact constant was found. If the parent campaign wants
AlphaEvolve-style exploration on this problem, it would be a genuinely
unclaimed angle rather than duplicating known effort — worth flagging back to
the team lead as a possible gap/opportunity rather than a dead end.

## Sources

- https://teorth.github.io/optimizationproblems/
- https://teorth.github.io/optimizationproblems/constants/6a.html (linked, not independently fetched)
