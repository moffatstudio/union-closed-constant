import sys, math
from functools import lru_cache
from seqcoupling_dp import family_tree, h, max_freq, max_gain, greedy_gain, iid_gain
F = [int(x) for x in sys.argv[1].split(',')]; n = int(sys.argv[2])
print("F =", [bin(S)[2:].zfill(n)[::-1] for S in F], " (bit i = element i, leftmost = element 0)")
print("max freq", max_freq(F,n), "iid", iid_gain(F,n), "greedy", greedy_gain(F,n), "DP", max_gain(F,n))
cnt, u = family_tree(F, n)
# forward pass under greedy, print every state with its gain and occupation
occ = {((),()):1.0}
for i in range(n):
    nxt = {}
    for (a,b), pr in occ.items():
        ua, vb = u[a], u[b]; lo, hi = max(0.0, ua+vb-1), min(ua,vb); s = min(max(0.5,lo),hi)
        g = h(s)-0.5*(h(ua)+h(vb))
        print("i=%d a=%s b=%s occ=%.4f u=%.3f v=%.3f s=%.3f gain=%+.4f weighted=%+.4f" % (i,''.join(map(str,a)),''.join(map(str,b)),pr,ua,vb,s,g,pr*g))
        for (x,y,w) in ((0,0,s),(0,1,ua-s),(1,0,vb-s),(1,1,1-ua-vb+s)):
            if w > 1e-12 and (a+(x,)) in cnt and (b+(y,)) in cnt: nxt[(a+(x,),b+(y,))] = nxt.get((a+(x,),b+(y,)),0)+pr*w
    occ = nxt
