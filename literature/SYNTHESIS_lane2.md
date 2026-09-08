# Synthesis (Lane 2): The Sawin coupling-entropy framework and why it caps at 0.382345533366703

Sources synthesized, in one consistent notation:
- Yu, "Dimension-Free Bounds for the Union-Closed Sets Conjecture," arXiv:2212.00658 → `2212.00658_yu.md`
- Cambie, "Better bounds for the union-closed sets conjecture using the entropy approach," arXiv:2212.12500 v2 → `2212.12500_cambie-bounds.md`
- Cambie, "Progress on the union-closed conjecture and offsprings in winter 2022–2023," arXiv:2306.12351 → `2306.12351_cambie-survey.md`

Notation note: Yu works with a general correlation parameter $\rho\in[0,1]$ and a function $\varphi(\rho,p,q)$; Cambie (following Sawin) works directly with the two extreme regimes $\rho=0$ (independent) and $\rho=1$ ("as negatively correlated as possible") and a mixture weight $\alpha$. Below, $\varphi(0,p,q)$ and $\varphi(1,p,q)$ are shown to coincide exactly with Cambie's two coupling laws, so the two papers' machinery is literally the same optimization problem, and I use Cambie's more concrete $(p,q,r,\alpha)$ notation as the spine, translating Yu's $(\rho,\varphi)$ notation into it where needed.

---

## 1. Setup: the entropy method (Gilmer's base case, $\alpha=0$)

$\mathcal F\subseteq 2^{[n]}$ nonempty, union-closed: $\mathcal F\cup\mathcal F=\mathcal F$ where $\mathcal F\cup\mathcal F:=\{A\cup B: A,B\in\mathcal F\}$. Since $\mathcal F\subseteq\mathcal F\cup\mathcal F$ always, non-union-closedness is witnessed by $|\mathcal F\cup\mathcal F|>|\mathcal F|$.

Let $A\sim\mathrm{Unif}(\mathcal F)$, coded as an indicator sequence $(A_1,\dots,A_n)\in\{0,1\}^n$. $H(A)=\log_2|\mathcal F|$ (uniform distribution maximizes entropy on its support). If a coupling of $A$ with a second $\mathcal F$-valued copy can be built so that $H(A\cup B)>\log_2|\mathcal F|$, then since $A\cup B$ is $\mathcal F\cup\mathcal F$-valued and entropy is capped by $\log_2|\mathcal F\cup\mathcal F|$, this forces $|\mathcal F\cup\mathcal F|>|\mathcal F|=|\mathcal F\cup\mathcal F|$... i.e. forces $\mathcal F$ to not be union-closed — contradiction if $\mathcal F$ *is* union-closed and every element's fraction is $<c$. Formally: **if $\mathcal F$ is union-closed and every $i\in[n]$ has $\mathbb P[i\in A]<c$, no such entropy-increasing coupling can exist.**

Per-coordinate, condition on the past $A_{<i}=(A_1,\dots,A_{i-1})$ and define the conditional inclusion probability
$$p_i \;=\; p_i(A_{<i}) \;:=\; \mathbb P[i\in A \mid A_{<i}] \in[0,1].$$
By the union-closed hypothesis (every element in $<c$ fraction of sets, in the appropriate conditional sense used throughout both papers) $p_i$ is a $[0,1]$-valued random variable with $\mathbb E[p_i]<c$, identically distributed across $i$ once one abstracts the coordinate index away (this abstraction — "the single-letter reduction" — is exactly the content of §3 below).

Gilmer/Sawin's base construction couples $A$ with an **independent** copy $B\sim\mathrm{Unif}(\mathcal F)$. Writing $q_i:=\mathbb P[i\in B\mid B_{<i}]$ (i.i.d. with $p_i$, independent of it), inclusion–exclusion gives the conditional law of the union bit:
$$\mathbb P[(A\cup B)_i=1 \mid A_{<i},B_{<i}] \;=\; p_i+q_i-p_iq_i \;=:\; \varphi(0,p_i,q_i). \tag{U0}$$

---

## 2. The general coupling-entropy inequality (the object both papers optimize)

### 2.1 The three coupled copies and the two extreme coupling laws

Both papers' refinement of Gilmer's method is to add a **third**, *dependently* coupled copy $C\sim\mathrm{Unif}(\mathcal F)$, built element-by-element from the *same* per-coordinate marginal law as $A$ but coupled to be **as negatively correlated with $A$ as possible** subject to matching marginals. Concretely (Cambie §2.2, reproduced from Sawin): with $r_i:=\mathbb P[i\in C\mid C_{<i}]$ (identically distributed with $p_i$), the coupling of $(A_i,C_i)$ given the pasts is built by aligning the two Bernoulli draws at *opposite* ends of a shared uniform variable when $p_i,r_i\le 1/2$ — forcing $\mathbb P[A_i=C_i=1\mid\text{past}]=0$ whenever $p_i+r_i\le 1$ — and at the *same* end once $\max(p_i,r_i)>1/2$. This coupling yields the closed-form conditional union law
$$\mathbb P[(A\cup C)_i=1\mid A_{<i},C_{<i}] \;=\; \max\{p_i,\,r_i,\,\min(p_i+r_i,\,\tfrac12)\} \;=:\; \varphi(1,p_i,r_i). \tag{U1}$$

**These are exactly Yu's two boundary cases** of the single general function
$$\varphi(\rho,p,q):=\mathrm{median}\Big\{\max\{p,q,p+q-z_2\},\ \tfrac12,\ \min\{p+q,\,p+q-z_1\}\Big\},\qquad z_{1,2}=pq\mp\rho\sqrt{p(1-p)q(1-q)},$$
where $\rho=\rho_m(X;Y)$ is the *maximal correlation* of the two coupled Bernoulli($p$), Bernoulli($q$) coordinates: $\varphi(0,p,q)=p+q-pq$ recovers (U0), and $\varphi(1,p,q)=\mathrm{median}\{\max(p,q),\tfrac12,p+q\}=\max\{p,q,\min(p+q,\tfrac12)\}$ recovers (U1) (the two forms of the $\rho=1$ formula coincide because $\rho=1$ forces the coupling to the extremal/comonotone-or-anti-comonotone boundary of the Fréchet–Hoeffding class, and for $p,q\le1/2$ the median expression collapses to the max/min expression above). So Yu's $\rho$-parametrized coupling family literally interpolates between Cambie/Sawin's independent ($\rho=0$) and maximally-anti-correlated ($\rho=1$) couplings.

### 2.2 The mixture and the per-coordinate entropy inequality (Sawin's Question 2 / Yu's Theorem 1)

Fix a mixture weight $\alpha\in[0,1]$; the method uses coupling $B$ with weight $(1-\alpha)$ and coupling $C$ with weight $\alpha$ (equivalently, in Yu's language, a distribution $P_\rho=(1-\alpha)\delta_0+\alpha\delta_1$ over the correlation parameter $\rho$). The **single-letter entropy inequality** required, for *every* admissible law of the (identically distributed) triple $(p,q,r)$ with $p\perp q$ and $(p,r)$ coupled as in §2.1, with $\mathbb E[p]<c$, is:
$$\boxed{\ (1-\alpha)\,\mathbb E\big[h(p+q-pq)\big] \;+\; \alpha\,\mathbb E\big[h(\max(p,r,\min(p+r,\tfrac12)))\big] \;\ge\; \mathbb E[h(p)]\ } \tag{$\star$}$$
where $h(x)=-x\log_2x-(1-x)\log_2(1-x)$ is binary entropy. (In Yu's general notation, this is $\mathbb E_\rho\,\mathbb E_{p,q}\,h(\varphi(\rho,p,q))\ge\mathbb E h(p)$ with $\rho\sim P_\rho=(1-\alpha)\delta_0+\alpha\delta_1$.) Equality holds automatically whenever $p$ is $\{0,1\}$-valued (both sides reduce to Gilmer's original deterministic-OR identity), so $(\star)$ can never be strict at such degenerate laws — the whole game is to find the largest $c$ for which some $\alpha$ makes $(\star)$ hold for *every* non-degenerate admissible $(p,q,r)$ law with $\mathbb E[p]<c$. This is stated verbatim as **Sawin's Question 2** in Cambie's paper, and is the $\alpha$-mixture special case of Yu's general functional $\Gamma(t)$ (Yu's eq. (2)): $\Gamma(t)>1$ for some $t$ is *equivalent*, via the $P_\rho=(1-\alpha)\delta_0+\alpha\delta_1$ substitution, to $(\star)$ holding at $c=t$ for some $\alpha$.

---

## 3. Chain rule with conditioning on the past — how $(\star)$ propagates to the whole family

Both papers assemble the full-family entropy inequality from the single-letter inequality $(\star)$ by the **same telescoping mechanism**, differing only in bookkeeping style (Yu: explicit inf/sup chain over $i=1,\dots,n$; Cambie: direct martingale/chain-rule induction). In one notation:

For each $i=1,\dots,n$, the chain rule for entropy gives (exactly, no inequality yet)
$$H\big((A\cup B)_{\le i}\big) = H\big((A\cup B)_{<i}\big) + H\big((A\cup B)_i \mid (A\cup B)_{<i}\big).$$
Since $(A\cup B)_{<i}$ is a deterministic function of the finer pair $(A_{<i},B_{<i})$, the **data-processing inequality** for conditional entropy gives
$$H\big((A\cup B)_i \mid (A\cup B)_{<i}\big) \;\ge\; H\big((A\cup B)_i \mid A_{<i},B_{<i}\big),$$
and conditionally on the pasts, $(A\cup B)_i\mid A_{<i},B_{<i}\sim\mathrm{Bernoulli}(p_i+q_i-p_iq_i)=\mathrm{Bernoulli}(\varphi(0,p_i,q_i))$, and likewise $(A\cup C)_i\mid A_{<i},C_{<i}\sim\mathrm{Bernoulli}(\max(p_i,r_i,\min(p_i+r_i,\tfrac12)))$, with $p_i,q_i,r_i$ each identically distributed with $\mathbb E[\,\cdot\,]<c$ (by the union-closed/max-fraction hypothesis on $\mathcal F$). Taking the $\alpha$-mixture of the two chain-rule inequalities (one for the $B$-coupling, one for the $C$-coupling) and comparing to the trivial identity $H(A_{\le i})=H(A_{<i})+H(A_i\mid A_{<i})$ gives, **coordinate by coordinate**, exactly the inequality $(\star)$ applied to the conditional-on-the-past law of $(p_i,q_i,r_i)$. Summing (telescoping) over $i=1,\dots,n$ and using $H(A)=\sum_iH(A_i\mid A_{<i})=\log_2|\mathcal F|$:
$$(1-\alpha)H(A\cup B) + \alpha H(A\cup C) \;\ge\; H(A) \;=\;\log_2|\mathcal F|,$$
with the inequality **strict** at $i=1$ (base case, no conditioning, so $(\star)$'s equality case $\{0,1\}$-valued $p$ cannot occur when $H(A_1)>0$ genuinely). Hence $\max\{H(A\cup B),H(A\cup C)\}>\log_2|\mathcal F|$, forcing $|\mathcal F\cup\mathcal F|>|\mathcal F|$ — contradicting union-closedness. **This is exactly how "conditioning on earlier coordinates" is handled**: the data-processing step replaces conditioning on the coarser union-history by the finer pair-of-histories $(A_{<i},B_{<i})$ (resp. $(A_{<i},C_{<i})$), which is exactly what makes the per-coordinate law collapse to the single-letter functions $\varphi(0,\cdot,\cdot)$, $\varphi(1,\cdot,\cdot)$ of $(p_i,q_i,r_i)$ alone — decoupling the $n$-dimensional problem into $n$ copies of the *same* one-dimensional inequality $(\star)$. Yu's version makes this a genuine $\inf/\sup$ chain (his eq. (11)–(13)) because he does not assume a specific $\alpha$-mixture in advance and must greedily optimize the coupling coordinate-by-coordinate under a maximal-correlation budget $\rho$ that tensorizes (his Lemma 1, eq. (10): $\rho_m(X^n;Y^n)=\max_i\rho_m(X_i;Y_i\mid X^{i-1},Y^{i-1})$) — but the two derivations produce the identical single-letter target.

---

## 4. The resulting finite(izable)-dimensional variational problem

Putting §2–§3 together, **the entire question reduces to a pure two-(or-more)-variable probability-distribution optimization**, with no reference to $n$ or $\mathcal F$ left:

$$c^{*} \;:=\; \sup\Big\{\,c\in(0,\tfrac12)\ :\ \exists\,\alpha\in[0,1]\ \text{s.t. } (\star)\text{ holds for every admissible i.d. triple }(p,q,r),\ \mathbb E[p]<c\,\Big\}.$$

"Admissible" means: $p,q,r$ identically distributed on $[0,1]$; $p\perp q$; $(p,r)$ jointly coupled with $\mathbb P(p=r=1)=0$ whenever $p,r\le\tfrac12$ can be realized as marginals require (the "as negatively correlated as possible" law of §2.1). Yu's more general version replaces the fixed $\rho\in\{0,1\}$ mixture by an arbitrary finitely-supported distribution $P_\rho$ on $[0,1]$ and an arbitrary finitely-supported outer law $P_p$, giving his $\Gamma(t)=\sup_{P_\rho}\inf_{P_p}\mathbb E_\rho[\cdots]$ (eq. (2)); Cambie's $(\star)$-based Question 2 is the restriction of this to $P_\rho=(1-\alpha)\delta_0+\alpha\delta_1$, which both papers ultimately show is (numerically/essentially) where the optimum sits.

**This is not yet finite-dimensional** as stated (the outer $\inf$ ranges over *all* laws of $p$ on $[0,1]$). Both papers independently prove a **support-reduction theorem** that makes it so:

- **Yu (Krein–Milman, exact and general):** $g(P_{pq},\alpha):=(1-\alpha)\mathbb E_{P_p^{\otimes2}}h(p+q-pq)+\alpha\,\mathbb E_{P_{pq}}h(\varphi(1,p,q))$ is **concave** in the symmetric coupling $P_{pq}$ (linear pushforward $P_{pq}\mapsto P_p$ composed with the concave functional $P_p\mapsto\mathbb E_{P_p^{\otimes2}}h(p+q-pq)$, concave by Alweiss–Huang–Sellke's Lemma 5). The feasible set of symmetric couplings supported on a fixed finite grid $B^2$ with $\mathbb E[p]\le t$ is, by **Krein–Milman**, the closed convex hull of its extreme points, which Yu identifies *exactly*: mixtures $(1-\beta)Q_{a_1,a_2}+\beta Q_{b_1,b_2}$ of two symmetrized Dirac atoms $Q_{x,y}=\tfrac12\delta_{(x,y)}+\tfrac12\delta_{(y,x)}$, with $a=\tfrac{a_1+a_2}2\le t<b=\tfrac{b_1+b_2}2$ and $\beta\in\{0,\tfrac{t-a}{b-a}\}$ — **support size $\le 4$ points**. Because $g(\cdot,\alpha)/\mathbb E h(p)$ of a convex combination is $\ge$ the corresponding combination of ratios at the extreme points (concavity + the elementary bound $\frac{\sum a_i}{\sum c_i}\ge\min_i a_i/c_i$), the $\inf$ over *all* finitely supported $P_{pq}$ equals the $\inf$ over just these $\le4$-point extreme couplings — this is Yu's Proposition 1.

- **Cambie (analytic, in two stages):** (i) §3.1: any mass of $p$ on $(\tfrac12,1)$ can be redistributed onto $\{\tfrac12,1\}$ (preserving $\mathbb E[p]$) via a Jensen/concavity argument (Lemma 4 for the $B$-term, controlled by the explicit threshold constant $1.044>\frac1{1-\alpha}$; Lemma 5 for the $C$-term) **without decreasing** the LHS of $(\star)$ — so WLOG $\mathrm{supp}(p)\subseteq[0,\tfrac12]\cup\{1\}$. (ii) §3.2: on $[0,\tfrac12]\cup\{1\}$, a Karamata/majorization argument (Claim 7, using concavity of $g(x)=h(\min(x,\tfrac12))$) plus a convex-then-concave analysis of the reduced one-variable functional $F_\mu(q)$ (Lemma 8) forces the optimal law of $p$ to be supported on **at most 3 points**, at least one of which is $\le\tfrac14$ when exactly 3 are used, and (by a further comparison to Yu's framework in §3.4, added at referee request) this reduces exactly to Yu's own $\{(1-\beta)Q_{a,a}+\beta Q_{b,b},\ (1-\beta)Q_{a,a}+\beta Q_{1,b}\}$ extreme-point family — **i.e. the two papers' independent reductions land on the identical finite-dimensional family**, ultimately depending on just **two real parameters $(a,b)$** (with $\beta,\alpha$ pinned by $a,b,c$).

**The explicit finite-dimensional optimization actually solved** (unifying both papers' final form):
$$\hat\Gamma(t) \;=\; \sup_{\alpha\in[0,1]} \ \inf_{\substack{0\le a\le t<b\le1 \\ \beta\in\{0,\ (t-a)/(b-a)\}}} \ \frac{(1-\alpha)\,\mathbb E_{(p,q)\sim P_p^{\otimes2}}h(p+q-pq)\ +\ \alpha\,\mathbb E_{(p,q)\sim P_{pq}}h(\max(p,q,\min(p+q,\tfrac12)))}{\mathbb E_{P_p}h(p)},$$
$$P_{pq} = (1-\beta)\,Q_{a,a} + \beta\,Q_{b,1}\ \ (\text{or }Q_{b,b}),\qquad Q_{x,y}=\tfrac12\delta_{(x,y)}+\tfrac12\delta_{(y,x)},$$
and $c^*=\hat t_{\max}:=\sup\{t\in(0,\tfrac12):\hat\Gamma(t)>1\}$. Numerically:
$$c^{*} \;=\; \hat t_{\max} \;=\; 0.382345533366703\ldots,\qquad \alpha^{*}\approx0.0356069813\ldots$$
(Yu computes $\hat t_{\max}\ge0.38234$ directly and cites Cambie for the extra digits; Cambie computes the same constant to 15 digits and, crucially, proves it is an *exact* answer, not just a lower bound — see §5.)

---

## 5. Why Sawin's coupling class tops out exactly there: the sharpness mechanism

Cambie's paper does more than compute $c^*$ numerically — it proves $c^*=0.382345533366703$ is **exactly** the answer to Sawin's Question 2 (i.e. this is a *hard ceiling* for the entire $\alpha$-mixture coupling class, for **every** choice of $\alpha$ simultaneously, not an artifact of insufficient search). The mechanism:

**The extremal distribution.** Let $b_1<b_2$ be the two roots in $(0,1)$ of
$$h(x)(2-h(x)) \;-\; h(2x-x^2) \;=\; 0, \qquad b_1\approx0.139499451909862,\quad b_2\approx0.329454738503037.$$
Set $b:=b_2$ and $a:=\dfrac{1-h(b)}{2-h(b)}\approx0.0788772927059232$. Let $p$ (and identically-distributed $q,r$) have the **2-point law**
$$\mathbb P(p=1)=a,\qquad \mathbb P(p=b)=1-a,$$
with $p\perp q$ (independent copy) and $(p,r)$ coupled with $\mathbb P(p=r=1)=0$ (the anti-correlated coupling of §2.1 — since $b<\tfrac12$, this just means the "$1$"-events of $p,r$ are disjoint). Then:
$$\mathbb E[p] = a + (1-a)b = 0.382345533366703 = c^{*}.$$

**The simultaneous-tightness identity.** Direct computation gives
$$\mathbb E\big[h(p+q-pq)\big] = (1-a)^2\,h(2b-b^2), \qquad \mathbb E\big[h(\max(p,r,\min(p+r,\tfrac12)))\big] = (1-2a)\,h(\min(2b,\tfrac12)),\qquad \mathbb E[h(p)]=(1-a)h(b),$$
and at the specific $(a,b)$ above, **all three quantities coincide exactly**:
$$(1-a)^2h(2b-b^2) \;=\; (1-2a) \;=\; (1-a)h(b). \tag{sharpness identity}$$
(This is precisely the defining system of equations for $b$ and $a$: $b$ is chosen as the root of $h(x)(2-h(x))-h(2x-x^2)$ that makes the *independent*-coupling term's value equal the *anti-correlated*-coupling term's value once both are further set equal to $\mathbb E[h(p)]$ via the matching choice $a=\frac{1-h(b)}{2-h(b)}$.)

**Why this defeats the mixture, for *every* $\alpha$ at once.** Because $\mathbb E[h(p+q-pq)]=\mathbb E[h(\max(p,r,\min(p+r,\tfrac12)))]=\mathbb E[h(p)]$ **all three equal**, any convex combination
$$(1-\alpha)\,\mathbb E[h(p+q-pq)] + \alpha\,\mathbb E[h(\max(p,r,\min(p+r,\tfrac12)))]$$
is *also* exactly $\mathbb E[h(p)]$, for **every** $\alpha\in[0,1]$ — the convex combination of two numbers that both equal $\mathbb E[h(p)]$ is just $\mathbb E[h(p)]$ again, regardless of the weight. So $(\star)$ holds with **equality** at this distribution, uniformly in $\alpha$: there is no $\alpha$ that produces strict slack here, because neither individual term has any slack to offer — the mixture operation ($\alpha$) can only interpolate between two quantities, and here both quantities are already pinned to the same critical value. Cambie confirms (and the paper states explicitly) that perturbing $a$ **upward** (i.e. considering $\mathbb E[p]$ slightly larger than $c^*$, keeping $b$ fixed near $b_2$) breaks $(\star)$ for every $\alpha$ — the paper's own words: *"no linear combination satisfies Equation 1 with a strict inequality and local perturbations (increasing $a$) will result in counterexamples when $c$ is allowed to be slightly larger."* Hence:

> **The specific feature of the extremal distribution that blocks the mixture coupling is that it is a single 2-point law which simultaneously saturates *both* of the two "pure" coupling strategies (independent and maximally-anti-correlated) at the *same* point.** Because the whole $\alpha$-mixture machinery can never produce more slack than the *better* of its two ingredient terms at any fixed input law, and here neither ingredient term has any slack left at exactly this law, $\alpha$-mixing is structurally incapable of pushing past $c^*$ — the ceiling is not a failure of optimizing $\alpha$ correctly, it is a *feature of the extremal input distribution itself*, which was reverse-engineered (via the root-finding system for $b$ and $a$) to have exactly this simultaneous-equality property.

**Corroborating evidence that mixing is essential, not just insufficient.** Cambie also exhibits (§4.4 of the transcription; his paper's second example) that using the anti-correlated coupling *alone* ($\alpha=1$, no mixing) with $b=\tfrac14$ gives $\mathbb E[p]<0.37<\psi=\frac{3-\sqrt5}2\approx0.38197$ — i.e. the pure dependent coupling alone doesn't even recover Gilmer's original constant. So the mixture is doing real work (moving the achievable constant from below Gilmer's $\psi$, using either pure strategy alone, up to $c^*\approx0.38235$ using the optimal blend) — it is just that the specific 2-point distribution of $b=b_2$ is a simultaneous fixed point of both strategies, capping the blend's achievable gain.

**Connection to Yu's general $\rho$-framework.** In Yu's language, this says: the extreme points of the Krein–Milman reduction (§4 above) that are binding at optimality are exactly couplings sitting at $\rho\in\{0,1\}$ (i.e. genuinely at the boundary of the maximal-correlation simplex, not some intermediate $\rho\in(0,1)$) — consistent with Sawin's original $\alpha$-mixture-of-extremes ansatz being, empirically, exactly where the true optimum $\Gamma(t)=\hat\Gamma(t)$ is attained; Yu's more general $\Gamma(t)$ (allowing arbitrary $P_\rho$, not just two-point $\{0,1\}$ mixtures) is not proven equal to $\hat\Gamma(t)$ in either paper, but no example is given showing a strict improvement is possible from using intermediate $\rho$ values, and Cambie's exact matching upper bound for the $\{0,1\}$-mixture problem specifically (not the fully general $\Gamma(t)$) is the rigorously established ceiling.

---

## 6. What this means for pushing past $\approx0.38235$

Both papers converge on the same methodological verdict, stated explicitly by Cambie and echoed in his survey:

1. **Sawin's specific coupling-mixture idea is now exactly exhausted**: $c^*=0.382345533366703$ is proven (not just computed) to be the precise supremum of what inequality $(\star)$ can certify, over *all* $\alpha\in[0,1]$ and *all* admissible $(p,q,r)$-laws. Higher-precision computation past this point is explicitly deemed pointless by Cambie ("an even more rigorous analysis... is unnecessary, as it does not contribute to further understanding the underlying principles").
2. **Generalizing the coupling family further yields only marginal gains at much higher cost**: Liu's follow-up (arXiv:2306.08824, June 2023) extends to a 9-variable "conditionally i.i.d." coupling and gets only a "tiny improvement" (per Cambie's survey), consistent with the interpretation that the 2-real-parameter family $(a,b)$ found by both Yu and Cambie is close to capturing everything this style of extreme-point/support-reduction analysis can offer.
3. **The gap to the conjectured $1/2$ remains large and structural, not numerical**: since $c^*\ne\tfrac12$, "another core method will be needed for the full resolution" (Cambie); the survey's own conclusion is that "the focus should go towards essential new ideas," specifically floating Zachary Chase's proposed generalization ($|\mathcal F\cup\mathcal F|>|\mathcal F|^{c(\varepsilon)}$ for any max-fraction $<\tfrac12-\varepsilon$) as a candidate reframing that might escape this particular ceiling.
4. **Known hard technical obstructions to natural extensions** (from Yu's discussion): (i) Rényi entropies fail the chain rule, blocking the natural Rényi generalization of the whole method; (ii) the *exact* (zero-error) nature of the union-closed conjecture, as opposed to *approximate* versions, may be intrinsically harder for information-theoretic/entropy techniques, which "usually work very well" only for approximate/vanishing-error constraints.

---

## Files in this lane

- `2212.00658_yu.md` — full transcription of Yu's paper (general $\rho$-framework, Krein–Milman reduction, Theorem 1/Proposition 1/Corollary 1, numerics).
- `2212.12500_cambie-bounds.md` — full transcription of Cambie's bounds paper (Question 2, Theorem 3, Lemmas 4–8, the exact sharpness construction and identity).
- `2306.12351_cambie-survey.md` — full transcription of Cambie's survey (barrier discussion, open questions, historical record table).
- `SYNTHESIS_lane2.md` — this file.
