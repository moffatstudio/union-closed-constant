# Relaxed adversary: any tree of conditionals u(prefix) in [0,1] on {0,1}^n with every marginal P(A_i=1) <= p.
# Coupler: any sequential coupling (DP inner max). Payoff = sum_i E[h(s_i) - (h(u_i)+h(v_i))/2].
# We minimise the payoff over trees (outer), by differential evolution + local polish, for given (n,p),
# then bisect on p to find the relaxed barrier p*(n) = inf{p : min payoff <= 0}.
import math, sys, numpy as np
from functools import lru_cache
from scipy.optimize import differential_evolution, minimize
def h(x):
    if x <= 0 or x >= 1: return 0.0
    return -(x*math.log2(x)+(1-x)*math.log2(1-x))
def prefixes(n):
    P = [()]
    for i in range(n):
        P += [q+(b,) for q in P if len(q)==i for b in (0,1)]
    return [q for q in P if len(q) < n]
def dp_value(n, u):
    @lru_cache(maxsize=None)
    def V(a, b):
        i = len(a)
        if i == n: return 0.0
        ua, vb = u[a], u[b]; base = -0.5*(h(ua)+h(vb))
        def fut(s):
            tot = h(s)
            for (x,y,w) in ((0,0,s),(0,1,ua-s),(1,0,vb-s),(1,1,1-ua-vb+s)):
                if w > 1e-13: tot += w*V(a+(x,), b+(y,))
            return tot
        lo, hi = max(0.0, ua+vb-1.0), min(ua, vb)
        if hi-lo < 1e-13: return base+fut(lo)
        gr=(math.sqrt(5)-1)/2; x1=hi-gr*(hi-lo); x2=lo+gr*(hi-lo); f1,f2=fut(x1),fut(x2)
        for _ in range(40):
            if f1<f2: lo=x1; x1=x2; f1=f2; x2=lo+gr*(hi-lo); f2=fut(x2)
            else: hi=x2; x2=x1; f2=f1; x1=hi-gr*(hi-lo); f1=fut(x1)
        return base+max(f1,f2)
    return V((),())
def marginals(n, u):
    # P(prefix) forward, then P(A_i = 1)
    pr = {(): 1.0}; freq = []
    for i in range(n):
        f = 0.0; nxt = {}
        for a, w in pr.items():
            f += w*(1-u[a]); nxt[a+(0,)] = w*u[a]; nxt[a+(1,)] = w*(1-u[a])
        freq.append(f); pr = nxt
    return freq
def objective(x, n, P, p, pen=50.0):
    x = np.clip(x, 0.0, 1.0)
    u = dict(zip(P, x))
    fr = marginals(n, u)
    viol = sum(max(0.0, f-p) for f in fr)
    return dp_value(n, u) + pen*viol
def min_payoff(n, p, seed=0, maxiter=60):
    P = prefixes(n); d = len(P)
    res = differential_evolution(objective, [(0,1)]*d, args=(n,P,p), seed=seed, maxiter=maxiter, popsize=20, tol=1e-8, polish=False)
    res2 = minimize(objective, res.x, args=(n,P,p), method='Nelder-Mead', options={'xatol':1e-7,'fatol':1e-9,'maxiter':4000})
    best = res2 if res2.fun < res.fun else res
    return best.fun, dict(zip(P, np.clip(best.x,0,1)))
if __name__ == "__main__":
    n = int(sys.argv[1])
    for p in [float(t) for t in sys.argv[2:]]:
        val, u = min_payoff(n, p)
        print("n=%d p=%.4f  min over trees of coupler's best payoff = %+.5f" % (n, p, val), flush=True)
        if val <= 1e-6:
            print("   tree:", {''.join(map(str,k)): round(v,4) for k,v in u.items()}, " marginals:", [round(f,4) for f in marginals(n,u)], flush=True)
