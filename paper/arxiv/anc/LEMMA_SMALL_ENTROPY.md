# A sharp small-entropy lemma

**Verdict.** The statement is **TRUE**, with the explicit constant

> **epsilon_0 = 7.6e-7**

(the proof yields eps_0 = G*h(t_0)/(1-t_0) = 7.62787e-7 for t_0 = 0.006; we round down for
safety). No counterexample was found in any regime searched: numerically the infimum of R
over laws with E(mu) <= 1e-3 is exactly the hiding-law limit 2w(1-c) = 1.00007321904 > C.

---

## 0. Notation and constants

h(p) = -p log2 p - (1-p) log2(1-p), h(0)=h(1)=0, h(p)=h(1-p). Write

- psi(u) := (1-u) log2(1/(1-u)) >= 0,  so  h(u) = u log2(1/u) + psi(u);
- Ltil(u) := log2(1/u) + (1-u)/ln 2   (strictly decreasing).

| symbol | value |
|---|---|
| w | 0.810222 |
| c | 0.38284, 1-c = 0.61716 |
| C | 1.00005 |
| r := (1-w)/w | 0.234229630891286586 |
| 2w | 1.620444 |
| 2w(1-c) | 1.00007321904 |
| C/(2w) | 0.617145671186415575 |
| G := (1-c) - C/(2w) | 1.43288135844250e-5 |
| t_0 (region threshold) | 0.006 |
| Ltil_0 := Ltil(t_0) | 8.81486065458456 |
| h(t_0) | 0.052915080344847655 |
| rho := (1-t_0)/h(t_0) | 18.7848150947159 |
| eps_0 := G/rho | 7.62787044e-7 |

For a law mu on [0,1]: E(mu) = int h dmu, I(mu) = int int h(xy) dmu dmu, K_min(mu) as in the
statement, R(mu) = [w I(mu) + (1-w) K_min(mu)] / E(mu).

---

## 1. Theorem

> **Theorem.** Let mu be a Borel probability measure on [0,1] with int x dmu(x) >= 1-c and
> 0 < E(mu) <= eps_0 = 7.6e-7. Then
>
>     R(mu)  >=  2w [ (1-c) - rho * E(mu) ]  >=  C = 1.00005.

The middle expression is the real content: **R(mu) >= 2w[(1-c) - rho E(mu)] for every mu with
mean >= 1-c**, with rho = 18.78482. The threshold eps_0 is simply where this crosses C. The
loss relative to the extremal value 2w(1-c) is *linear* in E(mu) with an explicit slope; no
factor 1/log2(1/t) is lost anywhere, which is what lets the 2.3e-5 margin survive.

---

## 2. Elementary lemmas

**Lemma 1 (concavity).** For theta, u in [0,1]:  h(theta*u) >= theta*h(u).

*Proof.* h is concave with h(0)=0, so h(theta u) = h(theta u + (1-theta) 0) >= theta h(u) +
(1-theta) h(0). ∎

**Lemma 2.** h(a) <= 2 sqrt(a(1-a)) for all a in [0,1], equality iff a in {0, 1/2, 1}.

*Proof.* By symmetry take a = 1/2 - u, u in [0,1/2].
(i) Since h''(p) = -1/(p(1-p) ln2) <= -4/ln2, Taylor at 1/2 gives h(1/2-u) <= 1 - 2u^2/ln2 =
1 - 2.885390 u^2, while 2 sqrt(a(1-a)) = sqrt(1-4u^2). Squaring, sqrt(1-4u^2) >= 1 - 2.885390 u^2
is equivalent to 1.770780 u^2 >= 8.325475 u^4, i.e. u <= 0.461187, i.e. a >= 0.038813.
(ii) For a < 0.038813: psi(a) <= a/ln2 (since (1-a) ln(1/(1-a)) <= a), hence
h(a) <= sqrt(a) * [ sqrt(a) (log2(1/a) + 1/ln2) ]. The map a -> sqrt(a)(log2(1/a) + 1/ln2) has
derivative (log2(1/a) - 1/ln2)/(2 sqrt a) > 0 for a < 2^{-1/ln2} = 0.3679, so on (0, 0.038813]
it is at most its endpoint value 1.20767, while 2 sqrt(a(1-a)) >= 2 sqrt(0.961187) sqrt(a) =
1.96079 sqrt(a) > 1.20767 sqrt(a). ∎

**Lemma 3.** For u in (0,1):  u * Ltil(u) <= h(u).

*Proof.* psi(u) = (1-u) log2(1/(1-u)) >= (1-u) u / ln2 because ln(1/(1-u)) >= u. ∎
(Also Ltil'(u) = -1/(u ln2) - 1/ln2 < 0, so Ltil is decreasing.)

**Lemma 4 (exact product loss).** Let x = 1-t, y = 1-t' with t,t' in [0,1], and set

    tau := 1 - xy = t + t' - t t',  A := t(1-t'),  B := t'(1-t),
    gamma := t t' / tau,            alpha := A/(A+B).

Then, with Lambda(t,t') := h(t) + h(t') - h(xy),

    Lambda(t,t') = tau * h(gamma) + (A+B) * h(alpha)  >= 0.

*Proof.* Let X ~ Bern(x), Y ~ Bern(y) independent, so XY ~ Bern(xy) and
h(t)+h(t') = H(X)+H(Y) = H(X,Y) = H(XY) + H(X,Y | XY), i.e. Lambda = H(X,Y | XY). Given XY=1
the pair is determined; given XY=0 (probability tau) the pair (X,Y) takes values (0,0),(1,0),(0,1)
with probabilities proportional to t t', A, B (and t t' + A + B = tau). The chain rule for the
ternary law (gamma, (1-gamma)alpha, (1-gamma)(1-alpha)) gives entropy h(gamma) + (1-gamma) h(alpha),
and (1-gamma) tau = A+B. ∎

**Lemma 5 (loss bound).** For t,t' in (0,1/2], with m = min(t,t'),

    Lambda(t,t')  <=  2 sqrt(t t')  +  t t' ( Ltil(m) + 1 + m/ln2 ).

*Proof.* Second term of Lemma 4: by Lemma 2, (A+B) h(alpha) <= (A+B) * 2 sqrt(alpha(1-alpha))
= 2 sqrt(AB) = 2 sqrt(t t' (1-t)(1-t')) <= 2 sqrt(t t').
First term: tau h(gamma) = tau gamma log2(1/gamma) + tau psi(gamma), with tau gamma = t t'.
Since tau <= t+t',  log2(1/gamma) = log2(tau/(t t')) <= log2(1/t + 1/t') <= log2(2/m) = 1 + log2(1/m),
and psi(gamma) <= gamma/ln2 gives tau psi(gamma) <= t t'/ln2. Hence
tau h(gamma) <= t t' (log2(1/m) + 1 + 1/ln2) = t t' (Ltil(m) + 1 + m/ln2). ∎

**Lemma 6 (key pointwise inequality).** For all t,t' in [0, t_0] with t_0 = 0.006,

    (*)   w * Lambda(t,t')  <=  (1-w) * sqrt( h(t) h(t') ).

*Proof.* If t=0 or t'=0 then Lambda = 0 and the claim is trivial. Let m = min(t,t') <=
M = max(t,t') <= t_0. By Lemma 3, sqrt(h(t)h(t')) >= sqrt(mM) sqrt(Ltil(m) Ltil(M)), so by
Lemma 5 it suffices that

    2/sqrt(Ltil(m)Ltil(M))  +  sqrt(mM)(Ltil(m)+1+m/ln2)/sqrt(Ltil(m)Ltil(M))  <=  r = (1-w)/w.

Since Ltil is decreasing, the first term is <= 2/Ltil_0. Call the second term g(m,M). It is
increasing in M because sqrt(M)/sqrt(Ltil(M)) is; and in m it equals
sqrt(m Ltil(m)) + sqrt(m)(1 + m/ln2)/sqrt(Ltil(m)), whose first summand increases because
d/dm [m Ltil(m)] = log2(1/m) - 2m/ln2 > 0 on (0,t_0], and whose second summand is visibly
increasing. Hence g <= g(t_0,t_0) = t_0 (Ltil_0 + 1 + t_0/ln2)/Ltil_0, and

    Phi(t_0) := 2/Ltil_0 + t_0(Ltil_0 + 1 + t_0/ln2)/Ltil_0
              = 0.226889576 + 0.006686561 = 0.233576137  <=  r = 0.234229631.  ∎

*(Slack 6.5e-4. Direct numerical evaluation of (*) shows it in fact holds up to t_0 = 0.0063062,
so the elementary chain above costs only about 5% in t_0.)*

**Lemma 7 (K lower bound).** Let N = (1-t_0, 1] and, for x in N, t_x := 1-x. Then

    K_min(mu)  >=  ( int_N sqrt(h) dmu )^2.

*Proof.* Fix any decomposition mu = sum_j pi_j P_j. Using h(xy + f(x)f(y)) >= h(xy) >= 0 and
dropping all pairs outside N x N,
int int h(xy+ff) dP_j dP_j >= int int_{N x N} h(xy) dP_j dP_j.
For x,y in N we have 1 - xy = t_x + t_y - t_x t_y in [max(t_x,t_y), 2 t_0] which is contained in
[0, 1/2], where h is increasing; hence h(xy) >= h(max(t_x,t_y)) >= sqrt(h(t_x) h(t_y)). Therefore
int int h(xy+ff) dP_j dP_j >= ( int_N sqrt(h) dP_j )^2. Summing with weights pi_j and applying
Jensen to the convex map s -> s^2,
sum_j pi_j (int_N sqrt h dP_j)^2 >= ( sum_j pi_j int_N sqrt h dP_j )^2 = ( int_N sqrt h dmu )^2,
since sum_j pi_j P_j = mu. This holds for every decomposition, hence for the infimum. ∎

**Lemma 8 (mean deficiency).** With B = [0, 1-t_0]:  int_B y dmu(y) <= rho * int_B h(y) dmu(y),
where rho = (1-t_0)/h(t_0) = 18.78482.

*Proof.* y -> h(y)/y is decreasing on (0,1] (h concave, h(0)=0), so y/h(y) is increasing and on
(0, 1-t_0] attains its maximum at y = 1-t_0, where it equals (1-t_0)/h(1-t_0) = (1-t_0)/h(t_0) = rho.
Thus y <= rho h(y) pointwise on B (trivially at y=0). ∎

---

## 3. Proof of the Theorem

Split [0,1] = N u B with N = (1-t_0, 1], B = [0, 1-t_0], and set

    sigma = mu(N),   S = int_N x dmu,   E_N = int_N h dmu,   E_B = int_B h dmu,   E = E_N + E_B.

Note S <= sigma, and for x in N, h(x) = h(t_x) with t_x in [0, t_0).

**(a) Cross terms.** For x in N, y in B, Lemma 1 with theta = x gives h(xy) >= x h(y), so

    2 int_N int_B h(xy) dmu dmu  >=  2 ( int_N x dmu )( int_B h dmu )  =  2 S E_B.

**(b) N x N terms.** By the definition of Lambda,

    int int_{NxN} h(xy) dmu dmu  >=  int int_{NxN} [h(t_x) + h(t_y)] - int int_{NxN} Lambda(t_x,t_y)
                                 =  2 sigma E_N - int int_{NxN} Lambda.

**(c) Combination.** Dropping the nonnegative B x B part of I and using Lemma 7,

    w I + (1-w) K_min  >=  2 w S E_B + 2 w sigma E_N
                           + int int_{NxN} [ (1-w) sqrt(h(t_x)h(t_y)) - w Lambda(t_x,t_y) ].

The last integrand is >= 0 pointwise by Lemma 6 (all t_x, t_y lie in [0, t_0)). Hence, using
sigma >= S,

    (3.1)   w I + (1-w) K_min  >=  2w ( sigma E_N + S E_B )  >=  2 w S (E_N + E_B)  =  2 w S E.

**(d) Mean constraint.** By Lemma 8,

    1 - c  <=  int_0^1 x dmu  =  S + int_B y dmu  <=  S + rho E_B  <=  S + rho E,

    (3.2)   S  >=  (1-c) - rho E.

**(e) Conclusion.** Combining (3.1) and (3.2) and dividing by E > 0,

    R(mu)  >=  2 w S  >=  2w(1-c) - 2 w rho E.

This is >= C exactly when E <= [2w(1-c) - C]/(2 w rho) = G/rho = 7.62787e-7. Since
E <= eps_0 = 7.6e-7 < G/rho, we conclude R(mu) >= C.  ∎

### Where sharpness comes from

1. Pairs {1} x {y} contribute h(y) exactly; a near-1 atom x = 1-t contributes x h(y) = (1-t)h(y),
   and *the same factor x* reappears in the mean constraint, because step (d) uses
   S = int_N x dmu and not sigma = mu(N). The two losses cancel identically. Had we bounded the
   cross terms by (1-t_0) sigma E_B and the mean by sigma, we would have paid t_0 ~ 6e-3, which
   dwarfs the available margin 2.3e-5 and destroys the proof.
2. Inside N entropy is genuinely subadditive, h(xy) < h(t)+h(t'), with loss ~ 2 sqrt(t t').
   This is paid for exactly by the K term, which is >= (int_N sqrt h)^2 >= Ltil_0 (int_N sqrt t)^2.
   The trade-off (1-w) Ltil_0 >= 2w fixes the threshold t_0 ~ 6e-3. Note that no logarithmic
   factor is lost here: the log only determines a threshold. This is precisely the step where the
   crude bound h(t+t') >= h(t)+h(t') - 2(t+t') fails, since it loses a factor 1 - 1/log2(1/t).
3. The only genuine loss is Lemma 8: mass sitting just below 1-t_0 can be worth up to rho times
   its entropy in the mean. That single mechanism produces the linear term 2 w rho E, and hence
   eps_0.

### Optimising the free parameter

eps_0(t_0) = G h(t_0)/(1-t_0) is increasing in t_0, so t_0 is taken as large as Lemma 6 permits.
The elementary chain (Lemmas 3 and 5) allows t_0 <= 0.0060892 (the root of Phi(t_0) = r); we use
the round value t_0 = 0.006. Verifying (*) numerically instead permits t_0 = 0.0063062 and
eps_0 = 7.954e-7, a 4% gain not worth the loss of rigour. The ceiling of this method is about
8e-7; going beyond ~1e-6 requires a different treatment of Lemma 8 (i.e. of middle mass), not a
better t_0.

---

## 4. Numerical exploration

All scripts are in `verification/small-entropy-lemma/`.

### 4.1 Verification of every inequality used (`verify.py`, `verify2.py`)

Grids: 2,000,001 points for Lemma 2; a 3000 x 3000 log-grid on (1e-16, t_0]^2 for Lemma 5 and (*);
2,000,000 points for Lemma 8; spot checks repeated in 50-digit mpmath arithmetic.

| claim | result |
|---|---|
| Lemma 2: max over a of h(a) - 2 sqrt(a(1-a)) | 0.0 (attained at a = 1/2) |
| Lemma 3: min over u of h(u) - u Ltil(u) | >= 0 (7.2e-33 at u=1e-16, 2.6e-5 at u=0.006) |
| Lemma 5: max over square of Lambda - bound | <= 0 (max 1.6e-16, pure float noise where both sides vanish; slack 7.2e-5 at the corner (t_0,t_0) in 50-digit arithmetic) |
| (*) : max over square of w Lambda / ((1-w) sqrt(h h)) | 0.99089, attained at (t_0, t_0) |
| Lemma 8: y/h(y) increasing, max on (0, 1-t_0] | 18.784815, attained at y = 1-t_0 |

The maximum of the ratio in (*) sits exactly at the corner (t_0,t_0), confirming that the diagonal
endpoint is the binding case and that t_0 = 0.006 leaves a genuine 0.9% margin in (*).

Solving w*Lambda(t,t) = (1-w) h(t) exactly gives the true admissible threshold t_0 = 0.0063062,
whence the "numerically sharp" version eps_0 = 7.954e-7 quoted above.

### 4.2 Adversarial search for counterexamples (`adv2.py`, `adv3.py`)

K_min is computed as an *upper* bound (minimum over all partitions of the support into up to 3
groups, plus the trivial decomposition P = mu). Since K_min <= that value, any R computed this
way is an *upper* bound for the true R(mu): a dip below C would be a genuine counterexample.

- **Random search** (`adv2.py`): 4613 laws with 3-5 atoms, atoms drawn near 0, near 1 and in the
  middle on log scales, masses drawn from a Dirichlet then shrunk by random factors up to 1e-9,
  mean adjusted to exactly 1-c, retained only when 0 < E(mu) <= 1e-4.
  **Minimum found: R = 1.0000732190 = 2w(1-c)**, attained by the hiding laws
  mu = 0.61716 delta_1 + z delta_y + (0.38284 - z) delta_0 with y -> 0 and z -> 0. Never below.
- **Directed scan** (`adv3.py`): the family sigma delta_1 + z delta_y + m_0 delta_0 with mean
  exactly 1-c, over 800 values of y spanning [1e-12, 1-1e-12] on log and linear scales, and
  E in {1e-12, 1e-9, 1e-7, 7.6e-7, 1e-6, 1e-5, 1e-4, 1e-3}; plus a 4-atom family adding a near-1
  atom 1-t (t in {1e-9, 1e-6, 1e-4, 0.006, 0.05}) carrying a fraction frac in {0, 0.3, 0.7, 1} of
  the entropy.
  **Minimum: R = 1.0000732190 (3 atoms), R = 1.0000732257 (4 atoms). Never below 2w(1-c).**

So numerically the infimum of R over the whole small-entropy range appears to be exactly
2w(1-c) = 1.00007321904, approached only in the hiding limit, and the truth is very likely
R(mu) >= 2w(1-c) - o(1) for E(mu) up to at least 1e-3, i.e. eps_0 = 7.6e-7 is conservative by
some orders of magnitude. What we can *prove* with the linear bound R >= 2w[(1-c) - rho E] is
eps_0 = 7.6e-7.

---

## 5. Final verdict

- The statement is **true**; the largest constant we prove is **eps_0 = 7.6e-7** (rigorously
  7.62787e-7 with t_0 = 0.006, or 7.954e-7 if one accepts a numerically verified (*) with
  t_0 = 0.0063062). This meets the target eps_0 >= 1e-7.
- The proof is in fact quantitative and threshold-free: **R(mu) >= 2w[(1-c) - 18.78482 * E(mu)]**
  for every law mu on [0,1] with mean >= 1-c.
- No counterexample exists in the searched families; the infimum of R appears to be exactly the
  hiding-law value 2w(1-c) = 1.00007321904, which sits 2.3e-5 above C = 1.00005.
- The one lossy step is the mean-deficiency bound (Lemma 8), which charges middle mass at rate
  rho = (1-t_0)/h(t_0). Anyone wanting eps_0 >> 1e-6 should replace it by an argument that
  exploits the entropy that mass at y in (t_0, 1-t_0) also injects into the cross terms with the
  atom at 1 (which the present proof already banks once, but not twice).
