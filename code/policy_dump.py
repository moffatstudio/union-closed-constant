# Dump the optimal sequential-coupling policy on a symmetric family: for each (i, wa, wb) reached, print
# u, v and the normalised choice lam = (s - uv)/(min(u,v) - uv)  (0 = iid, 1 = comonotone, <0 anti-correlated),
# plus the occupation probability of the state under the optimal policy.
import math, sys
from functools import lru_cache
from symmetric_dp import slice_family_tables, h
n = int(sys.argv[1]); K = [int(x) for x in sys.argv[2].split(',')]
N = slice_family_tables(n, K)
def u(i, w): return N[i+1][w]/N[i][w]
choice = {}
@lru_cache(maxsize=None)
def V(i, wa, wb):
    if i == n or N[i][wa] == 0 or N[i][wb] == 0: return 0.0
    ua, vb = u(i, wa), u(i, wb); base = -0.5*(h(ua)+h(vb))
    def fut(s):
        tot = h(s)
        for (x,y,w) in ((0,0,s),(0,1,ua-s),(1,0,vb-s),(1,1,1-ua-vb+s)):
            if w > 1e-13 and N[i+1][wa+x] > 0 and N[i+1][wb+y] > 0: tot += w*V(i+1, wa+x, wb+y)
        return tot
    lo, hi = max(0.0, ua+vb-1.0), min(ua, vb)
    if hi-lo < 1e-13: choice[(i,wa,wb)] = lo; return base + fut(lo)
    gr = (math.sqrt(5)-1)/2; x1 = hi-gr*(hi-lo); x2 = lo+gr*(hi-lo); f1, f2 = fut(x1), fut(x2)
    for _ in range(60):
        if f1 < f2: lo = x1; x1 = x2; f1 = f2; x2 = lo+gr*(hi-lo); f2 = fut(x2)
        else: hi = x2; x2 = x1; f2 = f1; x1 = hi-gr*(hi-lo); f1 = fut(x1)
    s = (x1+x2)/2; choice[(i,wa,wb)] = s; return base + fut(s)
print("G_max =", V(0,0,0))
# forward occupation
occ = {(0,0,0):1.0}
for i in range(n):
    nxt = {}
    for (ii,wa,wb), pr in occ.items():
        if ii != i or pr < 1e-9: continue
        ua, vb = u(i,wa), u(i,wb); s = choice[(i,wa,wb)]
        for (x,y,w) in ((0,0,s),(0,1,ua-s),(1,0,vb-s),(1,1,1-ua-vb+s)):
            if w > 1e-13 and N[i+1][wa+x]>0 and N[i+1][wb+y]>0:
                nxt[(i+1,wa+x,wb+y)] = nxt.get((i+1,wa+x,wb+y),0)+pr*w
    for (ii,wa,wb), pr in sorted(occ.items(), key=lambda t:-t[1])[:6]:
        ua, vb = u(i,wa), u(i,wb); s = choice[(i,wa,wb)]; iid = ua*vb; co = min(ua,vb)
        lam = (s-iid)/(co-iid) if co-iid > 1e-12 else float('nan')
        gain = h(s)-0.5*(h(ua)+h(vb))
        print("i=%2d wa=%2d wb=%2d occ=%.3f u=%.3f v=%.3f s=%.3f lam=%+.2f gain=%+.4f" % (i,wa,wb,pr,ua,vb,s,lam,gain))
    occ = nxt
