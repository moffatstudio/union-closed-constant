# Certificate of formal verification — `UnionClosedCeiling`

**Date of this certificate:** 2026-09-10.
**Certified tree:** git commit `45949fa770f3588530bec0e8b2f201f366c61236`
(*Lean formalisation of the ceiling theorems (Theorems 3.1, 3.4, Lemma 3.3), CI gate, README/CITATION updated*),
repository <https://github.com/moffatstudio/union-closed-constant>, release **v1.1**.
The working tree was clean when the checks below were run; this file is added on top of that
commit and is not itself part of the hashed set.

**Paper certified against:** A. Moffat, *The ceiling of the single-letter entropy method for the
union-closed sets conjecture, and a protocol that reaches it*, 8 September 2026 (`../paper/paper.pdf`).
Appendix B of the paper describes the formalisation; Appendix C reproduces the source.

---

## 1. Toolchain

| Component | Version / pin |
|---|---|
| Lean | `leanprover/lean4:v4.23.0` (`lean-toolchain`) |
| Mathlib | tag `v4.23.0`, commit `37df177aaa770670452312393d4e84aaad56e7b6` (`lake-manifest.json`) |
| Lake | `Lake version 5.0.0-src+50aaf68 (Lean version 4.23.0)` |
| Package | `UnionClosedCeiling` 0.1.0, `autoImplicit = false`, `relaxedAutoImplicit = false` (`lakefile.toml`) |

Transitive dependencies are pinned in `lake-manifest.json` (plausible, LeanSearchClient,
importGraph, ProofWidgets4, aesop, Qq, batteries, Cli — all inherited from Mathlib).

## 2. Checked declarations and their axioms

`lake env lean AxiomCheck.lean`, run 2026-09-10, exit code 0, output verbatim:

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

Ten declarations, each depending on `propext`, `Classical.choice`, `Quot.sound` and nothing else —
Lean's three standard axioms. No `sorryAx`, no `Lean.ofReduceBool`, no user-declared axiom.

## 3. The gate

`bash check.sh`, run 2026-09-10, exit code 0, output verbatim:

```
== 1. lake build ==
⚠ [2076/2078] Replayed UnionClosedCeiling.Classes
warning: UnionClosedCeiling/Classes.lean:123:51: unused variable `hδ0`

Note: This linter can be disabled with `set_option linter.unusedVariables false`
ℹ [2077/2078] Replayed UnionClosedCeiling
info: UnionClosedCeiling.lean:20:0: 'UnionClosedCeiling.product_ceiling' depends on axioms: [propext, Classical.choice, Quot.sound]
info: UnionClosedCeiling.lean:21:0: 'UnionClosedCeiling.hiding_bound' depends on axioms: [propext, Classical.choice, Quot.sound]
info: UnionClosedCeiling.lean:22:0: 'UnionClosedCeiling.diagonal_bound' depends on axioms: [propext, Classical.choice, Quot.sound]
info: UnionClosedCeiling.lean:23:0: 'UnionClosedCeiling.fixed_point_form' depends on axioms: [propext, Classical.choice, Quot.sound]
info: UnionClosedCeiling.lean:24:0: 'UnionClosedCeiling.refined_ceiling_numeric' depends on axioms: [propext, Classical.choice, Quot.sound]
info: UnionClosedCeiling.lean:25:0: 'UnionClosedCeiling.containsProduct_iidClass' depends on axioms: [propext, Classical.choice, Quot.sound]
info: UnionClosedCeiling.lean:26:0: 'UnionClosedCeiling.containsProduct_allCouplings' depends on axioms: [propext, Classical.choice, Quot.sound]
info: UnionClosedCeiling.lean:27:0: 'UnionClosedCeiling.containsProduct_mixtureOfProducts' depends on axioms: [propext, Classical.choice, Quot.sound]
info: UnionClosedCeiling.lean:28:0: 'UnionClosedCeiling.admitsHiding_allCouplings' depends on axioms: [propext, Classical.choice, Quot.sound]
info: UnionClosedCeiling.lean:29:0: 'UnionClosedCeiling.admitsHiding_mixtureOfProducts' depends on axioms: [propext, Classical.choice, Quot.sound]
Build completed successfully (2078 jobs).
== 2. no 'sorry' ==
ok: no sorry in the build output or the sources
== 3. #print axioms ==
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
ok: only propext, Classical.choice, Quot.sound

ALL CHECKS PASSED
```

The one warning is an unused hypothesis binder in an auxiliary lemma (`hidingCoupling_diag`);
it is a linter note, not a proof obligation.

The build was a replay from the local `.lake` cache. The same gate was run from scratch, on a
fresh clone with no cache, in continuous integration — see §5.

## 4. Source hashes (SHA-256)

Of the files in `lean/` at the certified commit that constitute the formal development (sources, build configuration, gate; the documentation files `README.md` and `SPEC.md` are not hashed):

```
4c41169f8f655132c4d1000040fb4d84b369328162d7e0f89b79ee83bd9afb84  UnionClosedCeiling.lean
b4a523813713dd8de3a023ce89136cce62eee03e495192f39ce499ff5fde06ed  AxiomCheck.lean
607e89ea0aa66ad5f31baf4fac2dec3816277f7af463fb5b4450d6ec5d57217e  UnionClosedCeiling/Entropy.lean
7e7a77a38f36625b8ca96ea16e7febb29209c1434d0c58279a126a8d3451303f  UnionClosedCeiling/Framework.lean
fd9eace8b7a2c0bc7109627b653a1289986ae36f909a00167d9dcb400e5a7b35  UnionClosedCeiling/Ceiling.lean
45ca6ee22d100b614a0761bfeb738f0801ee14f75ad944a20985b5b1cab8e2e2  UnionClosedCeiling/Refined.lean
a4a72e5a9f8386e18de33e606ae100ff3a1ccc0a151ee2068584b40c1ef05639  UnionClosedCeiling/Classes.lean
1a32562c2355f209905b7578fe00db8e54156779ca7d80d658b6bfc1bf56e458  lakefile.toml
ae8e6d481b3b03ce0011fa245776d5575237aae9d2819ecd35c582b02cc04b2b  lake-manifest.json
49e4916cabcb6ed4706f31d91b653d33ce83e12dc1e1c43bb560f11e4249f37d  lean-toolchain
2c7e527b7380ae77fc2d7d21a8e7e61e71d65424b428f80302e077529be81f8a  check.sh
```

Reproduce with `sha256sum` from `lean/` (the repository has `.gitattributes` set so line endings
are preserved; on Windows check out with `core.autocrlf=false`).

## 5. Continuous integration

Workflow `.github/workflows/lean.yml`, job `build`, **run 34522052221**: fresh `ubuntu-latest`
runner, `actions/checkout@v4`, elan installed from scratch, `lake exe cache get` (no local
state), `lake build`, a `grep` for `sorry` in the build log, then `bash check.sh`. Green in
**2 min 20 s**. The workflow runs on every push to `master` and every pull request touching `lean/` (or the workflow file itself).

## 6. What is certified

On the finite model described in §8, and under the hypotheses shown, the following are proved
in Lean with no `sorry` and no axiom beyond the three above.

**Theorem 3.1 of the paper (product ceiling)** — `UnionClosedCeiling.product_ceiling`
(`UnionClosedCeiling/Ceiling.lean`). If every class contains the product law, the certificate
constant satisfies

```lean
c ≤ 1 - h (1 / Real.sqrt 2) / Real.sqrt 2
```

i.e. `c ≤ c_ceil = 0.3830992976…` (`cCeil` in the same file).

**Theorem 3.4 of the paper (refined ceiling)** — four declarations in
`UnionClosedCeiling/Refined.lean`, with protocol `0` the i.i.d. one (`Prot 0 x y = x * y`),
every class containing products, and every other class admitting component hiding:

| Paper | Lean | Statement |
|---|---|---|
| (H) | `hiding_bound` | `1 ≤ 2 * w 0 * (1 - c)` |
| (D) | `diagonal_bound` | `c ≤ 1 - x * h x / (w 0 * h (x^2) + 1 - w 0)`, for `x ∈ Ioc 0 1` with `h x ≤ w 0 * h (x^2) + 1 - w 0` |
| (G) | `fixed_point_form` | `c ≤ 1 - x * h x / (1 - (1 - h (x^2)) / (2 * (1 - c)))`, for `x ∈ Ioo 0 1` with `h x ≤ h (x^2)` and `c ≤ 1/2` |
| numerical consequence | `refined_ceiling_numeric` | `c ≤ 3829/10000` |

The numerical corollary is obtained at `x = 0.6909` from rigorous entropy bounds proved in the
same file (`0.892131 ≤ ent(0.6909) ≤ 0.8921319`, `0.9985182 ≤ ent(0.6909²) ≤ 0.998519`, via
Taylor series of `log(1-t)` with the explicit remainder `Real.abs_log_sub_add_sum_range_le`
and Mathlib's `Real.log_two_gt_d9` / `Real.log_two_lt_d9`).

**Lemma 3.3 of the paper**, for three of its four classes
(`UnionClosedCeiling/Classes.lean`): the i.i.d. singleton class `{μ⊗μ}`, the class of all
couplings, and the class of mixtures of products each contain the product law
(`containsProduct_iidClass`, `containsProduct_allCouplings`,
`containsProduct_mixtureOfProducts`), and the latter two admit component hiding in the sense of
Definition 3.2 (`admitsHiding_allCouplings`, `admitsHiding_mixtureOfProducts`), with the
explicit witness `P = q δ₁⊗δ₁ + (1-q) P₀⊗P₀`, `P₀ = (1-δ)δ₀ + δ δ_y`.

## 7. What is **not** certified

* **Proposition 2.2 of the paper** — Gilmer's entropy argument and the reduction from finite
  union-closed families to the single-letter certificate. In the Lean development the
  certificate is a *hypothesis* (`Certifies`), not a theorem. Nothing about set families,
  and nothing measure-theoretic, appears in the formalisation.
* **The maximal-correlation class of Lemma 3.3** (Yu's protocols). Its hiding witness needs
  continuity of singular values in the matrix entries; it is proved in the paper only.
* **Sections 4–6 of the paper** in their entirety: the ideal-diagonal protocol and its kernel,
  Theorem 5.5 and Lemma 5.6, Hypotheses 5.3 and 6.1, Theorem 6.2 and its constant
  **0.38284**, Remark 6.3, and the numerical appendix. None of this is formalised, and the
  constant 0.38284 of Theorem 6.2 is *not* machine-checked.
* **The exact value `c** = 0.382885260…`.** It is the solution of a real fixed-point equation
  and is evaluated numerically by `../verify.py` and
  `../verification/independent-recertification/closed.py`. Lean proves the explicit rational
  bound `c ≤ 3829/10000 = 0.3829` — not `c ≤ c**`, and not `c ≤ 0.382885`. Since
  `0.3829 < c_ceil = 0.3830992976…`, the formal result already shows that the refined ceiling
  is strictly below the product ceiling.
* Frankl's conjecture itself, which this work does not resolve.

## 8. Modelling caveat

The theorems are proved on a **finite model** of the framework of §2.2 of the paper:

* laws on `[0,1]` are finitely supported (atoms `Fin n → ℝ` in `[0,1]`, non-negative weights
  summing to 1). Every adversarial law used in Section 3 — the two-point laws of Theorem 3.1
  and (D), and the three-point hiding law of Definition 3.2 — is of this form. Restricting the
  certificate *hypothesis* to finitely supported laws makes it weaker, hence makes the theorems
  proved from it stronger.
* a protocol is modelled by `Prot : ℝ → ℝ → ℝ`, `Prot x y = Π_{x,y}(0,0)`, subject to the
  Fréchet bounds `max 0 (x+y-1) ≤ Prot x y ≤ min x y`. Section 3 of the paper uses nothing else
  about protocols; the facts it does use (`Π x 0 = 0`, `Π 1 1 = 1`, `Π 1 y = y`) are derived from those
  bounds, while `ent(Π) ≤ 1` (`h_le_one`) holds for every real argument, from Mathlib's
  `Real.binEntropy_le_log_two`, independently of `IsProtocol`.
* **`Certifies` is implied by (cert).** The paper's (cert) has an infimum over the class on the
  left-hand side; since an infimum is at most the value at any particular admissible family of
  couplings, (cert) implies the Lean hypothesis `Certifies Prot w C Cc c`. Every theorem here is
  proved from `Certifies`, so all of them apply verbatim to the paper's certificate. The Lean
  development uses `1 ≤ Cc` where the paper has `C > 1`.
* the i.i.d. protocol is only assumed to have a class containing products, which is weaker than
  the paper's singleton class `{μ⊗μ}`, so the Lean statements are slightly stronger there.
* the limit `δ → 0` in (H) is carried out by hand: `δ` is chosen below the hiding threshold of
  each of the finitely many classes and below `c(1 - 2 q w₀)`.

These choices are recorded in the module docstring of `UnionClosedCeiling/Framework.lean` and
in `README.md`. What they mean in practice: the Lean theorems bound the constant certifiable by
any single-letter argument of the paper's shape, *given* the certificate; they do not
independently re-derive the certificate from union-closed families.

## 9. Provenance

The formalisation was written on 2026-09-10 by a Claude Fable 5.1 (Anthropic) agent from
`SPEC.md` — which fixes the finite model, the statements to prove and the modelling latitude —
and from the paper. Every resulting statement was read against the paper by the author before
being committed; the mapping is tabulated in `README.md` and in §6 above. The proofs themselves
are checked by Lean, not by a human or an agent.

## 10. Reproducing this certificate

From a fresh clone (network needed to fetch Mathlib and its `olean` cache; the CI run in §5
does exactly this in 2 min 20 s):

```bash
git clone https://github.com/moffatstudio/union-closed-constant
cd union-closed-constant/lean
lake exe cache get
lake build
bash check.sh
```

`check.sh` exits `0` only if the build succeeds, no `sorry` appears in the build output or the
sources, all ten `#print axioms` reports are present, and none of them names an axiom outside
`propext`, `Classical.choice`, `Quot.sound`. For the axiom list on its own:

```bash
lake env lean AxiomCheck.lean
```

To confirm you are checking the same sources, compare `sha256sum` against §4. Anyone reproducing
this on a different toolchain should say so: the pins in §1 are part of the claim.
