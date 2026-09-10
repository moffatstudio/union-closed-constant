"""Quick verification of the numbers in the paper (runs in about a minute).

    python verify.py            # fast checks only
    python verify.py --search   # also a short 4-atom optimiser run (a few minutes)

Every check compares a value recomputed here against the value printed in the paper
(Appendix A, Table 2, Theorem 5.5) and exits non-zero on the first failure. Two
independent evaluators are used: code/kernel_game.py (the paper's) and
verification/independent-recertification/evaluator.py (written from the manuscript
alone). The heavy computations behind Table 2 and Hypothesis 6.1 (5,000 restarts,
5 and 6 atoms, 97 minutes) are not repeated here; their logs are in code/.
"""
import os, sys, time
import numpy as np
from scipy.optimize import minimize_scalar

ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(ROOT, "code"))
sys.path.insert(0, os.path.join(ROOT, "verification", "independent-recertification"))
import kernel_game as KG                      # paper's evaluator (natural-log h)
import evaluator as IE                        # independent evaluator (bits)

W = 0.810222          # w** as used in the paper
C = 0.38284           # certified constant
CERT = 1.00005        # C in Theorem 6.2
FAILS = []


def check(name, got, want, tol):
    ok = abs(got - want) <= tol
    print("%-62s %-18s paper %-14s %s" % (name, ("%.9f" % got), ("%.9f" % want), "ok" if ok else "FAIL"))
    if not ok:
        FAILS.append(name)


def hb(x):
    x = np.asarray(x, float)
    out = np.zeros_like(x)
    m = (x > 0) & (x < 1)
    out[m] = -(x[m] * np.log2(x[m]) + (1 - x[m]) * np.log2(1 - x[m]))
    return out


def f_ideal(x):
    x = np.asarray(x, float)
    return np.where(x <= 0.5, np.minimum(x, 1 - x), np.sqrt(np.maximum(0.0, 0.5 - x ** 2)))


K_IDEAL = KG.make_rank_kernel([f_ideal])
K_LIU = KG.make_rank_kernel([lambda x: x * (1 - x)])


def kg_ratio(q, P0, P1, K, w):
    """kernel_game.ratio on explicit laws P = [(atom, weight), ...]."""
    m = max(len(P0), len(P1))
    P0 = P0 + [(0.0, 0.0)] * (m - len(P0)); P1 = P1 + [(0.0, 0.0)] * (m - len(P1))
    z = np.concatenate([[q], [p[1] for p in P0], [p[0] for p in P0], [p[1] for p in P1], [p[0] for p in P1]])
    return KG.ratio(z, m, K, 1 - w)


def ie_ratio(q, P0, P1, f, w):
    return IE.ratio(np.array([p[0] for p in P0]), np.array([p[1] for p in P0]),
                    np.array([p[0] for p in P1]), np.array([p[1] for p in P1]), q, w, f)


print("== Appendix A: constants")
x0 = 1 / np.sqrt(2)
check("h(1/sqrt2)", float(hb(x0)), 0.872429340, 1e-9)
check("c_ceil = 1 - h(1/sqrt2)/sqrt2  (Theorem 3.1)", float(1 - hb(x0) / np.sqrt(2)), 0.383099298, 1e-9)


def G(c):
    r = minimize_scalar(lambda x: 1 - x * hb(x) / (1 - (1 - hb(x * x)) / (2 * (1 - c))),
                        bounds=(0.5, 1 / np.sqrt(2)), method="bounded", options={"xatol": 1e-13})
    return r.fun, r.x


c = 0.3828
for _ in range(200):
    c, xs = G(c)
check("c** fixed point  (Theorem 3.4)", float(c), 0.382885260, 1e-9)
check("w** = 1/(2(1-c**))", float(1 / (2 * (1 - c))), 0.810222, 1e-6)
check("x** minimiser", float(xs), 0.690908, 1e-6)

print("== Section 6: evaluator calibration on Liu's optimum (arXiv:2306.08824, Theorem 13)")
wL, cL = 0.899947, 0.382709087918741
liu_P0 = [(0.690787593924988, 0.893604513905457), (0.0, 1 - 0.893604513905457)]
check("kernel_game: R at Liu's minimiser", kg_ratio(0.0, liu_P0, [(0.5, 1.0)], K_LIU, wL), 1.0, 2e-9)
check("independent evaluator: same", ie_ratio(0.0, liu_P0, [(0.5, 1.0)], IE.f_liu, wL), 1.0, 2e-9)

print("== Proposition 4.3(a) / Table 2: two-point law at w = %.6f" % W)


def twopt(x, c, w, ev):
    p = (1 - c) / x
    if p > 1:
        return np.inf
    return ev(0.0, [(x, p), (0.0, 1 - p)], [(0.5, 1.0)])


for cc, want in ((0.38284, 1.0000733), (0.38288, 1.0000085)):
    r = minimize_scalar(lambda x: twopt(x, cc, W, lambda q, P0, P1: kg_ratio(q, P0, P1, K_IDEAL, W)),
                        bounds=(0.6, 0.75), method="bounded", options={"xatol": 1e-12})
    check("kernel_game: min two-point ratio, c=%.5f" % cc, float(r.fun), want, 6e-8)
    r2 = minimize_scalar(lambda x: twopt(x, cc, W, lambda q, P0, P1: ie_ratio(q, P0, P1, IE.f_ideal, W)),
                         bounds=(0.6, 0.75), method="bounded", options={"xatol": 1e-12})
    check("independent evaluator: same, c=%.5f" % cc, float(r2.fun), want, 6e-8)
    if cc == 0.38284:
        check("  minimiser x", float(r.x), 0.6909, 1e-3)
        check("  two evaluators agree", float(r.fun), float(r2.fun), 1e-11)

print("== Proposition 4.3(b) / Table 2: hiding family, closed form at c = %.5f" % C)
lim = 2 * W * (1 - C)
check("limit 2w(1-c)", lim, 1.000073, 1e-6)
worst = np.inf
for d in (1e-2, 1e-3, 1e-4):
    for y in (0.05, 0.2, 0.5, 0.7):
        q = 1 - C
        v = ie_ratio(q, [(0.0, 1 - d), (y, d)], [(1.0, 1.0)], IE.f_ideal, W)
        v2 = kg_ratio(q, [(0.0, 1 - d), (y, d)], [(1.0, 1.0)], K_IDEAL, W)
        if abs(v - v2) > 1e-9:
            FAILS.append("hiding evaluators disagree d=%g y=%g" % (d, y))
        worst = min(worst, v)
print("%-62s %-18s paper %-14s %s" % ("hiding family, delta<=1e-2: min ratio", "%.9f" % worst, ">= 1.000073",
                                      "ok" if worst >= lim - 1e-9 else "FAIL"))
if worst < lim - 1e-9:
    FAILS.append("hiding family below limit")

print("== Theorem 5.5 / Lemma 5.6: small-entropy constants")
ln2 = np.log(2); t0 = 0.006
Lt = lambda u: np.log2(1 / u) + (1 - u) / ln2
rho = (1 - t0) / hb(t0)
check("rho = (1-t0)/h(t0)", float(rho), 18.784815, 1e-6)
check("h(t0)", float(hb(t0)), 0.0529151, 1e-7)
check("L~(t0)", float(Lt(t0)), 8.814861, 1e-6)
r = (1 - W) / W
check("r = (1-w)/w", float(r), 0.2342296, 1e-7)
check("(1-c) - C/(2w)", float((1 - C) - CERT / (2 * W)), 1.43288e-5, 1e-9)
check("eps0 = [(1-c) - C/(2w)]/rho", float(((1 - C) - CERT / (2 * W)) / rho), 7.62787e-7, 1e-11)
check("Lemma 5.6 bound 2/L~(t0) + t0(L~(t0)+1+t0/ln2)/L~(t0)",
      float(2 / Lt(t0) + t0 * (Lt(t0) + 1 + t0 / ln2) / Lt(t0)), 0.233577, 1e-6)
u = np.logspace(-16, np.log10(t0), 2000)
T, TP = np.meshgrid(u, u)
Lam = hb(T) + hb(TP) - hb(T + TP - T * TP)
corner = float(np.nanmax(W * Lam / ((1 - W) * np.sqrt(hb(T) * hb(TP)))))
check("max of w*Lambda/((1-w) sqrt(h h')) on [0,t0]^2 (must be < 1)", corner, 0.9909, 1e-3)
a = np.linspace(1e-12, 1 - 1e-12, 400001)
check("(F2): max h(a) - 2 sqrt(a(1-a))  (must be <= 0)", float((hb(a) - 2 * np.sqrt(a * (1 - a))).max()), 0.0, 1e-12)

print("== Cross-check: the two evaluators agree on random laws")
rng = np.random.default_rng(1)
md = 0.0
for _ in range(200):
    n = 4
    P0 = list(zip(rng.random(n), rng.dirichlet(np.ones(n))))
    P1 = list(zip(rng.random(n), rng.dirichlet(np.ones(n))))
    q = rng.random()
    md = max(md, abs(kg_ratio(q, P0, P1, K_IDEAL, W) - ie_ratio(q, P0, P1, IE.f_ideal, W)))
check("max |R_kernel_game - R_independent| over 200 random laws", md, 0.0, 1e-10)

if "--search" in sys.argv:
    print("== Short optimiser run (independent evaluator, 4 atoms, 40 restarts; full run: code/big_restart.py)")
    t = time.time(); best = np.inf; n = 4
    for s in range(40):
        z0 = np.concatenate([rng.random(n), rng.normal(size=n), rng.random(n), rng.normal(size=n), [rng.random()]])
        v, z = IE.local_min(z0, n, W, IE.f_ideal, C, hfloor=1e-3)
        best = min(best, v)
    # seeded at the known minimiser
    z0 = np.concatenate([[0.6909, 0, 0, 0], [3, 1, -9, -9], [0.5, 0.5, 0.5, 0.5], [0, 0, 0, 0], [0.0]])
    v, z = IE.local_min(z0, n, W, IE.f_ideal, C, hfloor=1e-3)
    best = min(best, v)
    print("   min ratio found = %.9f  (%.0fs)  minimiser %s" % (best, time.time() - t, IE.describe(z, n)))
    if best < CERT:
        FAILS.append("optimiser found ratio below C")
    check("short search minimum (>= 1.0000733 expected)", float(best), 1.0000733, 1e-6)

print()
if FAILS:
    print("FAILED:", FAILS); sys.exit(1)
print("ALL CHECKS PASSED")
