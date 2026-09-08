import sys, time, numpy as np
from kernel_game import *
name = sys.argv[1]; betas = [float(b) for b in sys.argv[2].split(',')]; m = int(sys.argv[3]) if len(sys.argv)>3 else 3
lam = float(sys.argv[4]) if len(sys.argv)>4 else 1.0
def f_ideal(x):
    x = np.asarray(x, float)
    return lam*np.where(x <= 0.5, np.minimum(x, 1-x), np.sqrt(np.maximum(0.0, 0.5 - x**2)))
def f_liu(x): return x*(1-x)
def f_minmax(x): return lam*np.minimum(x, 1-x)
kernels = {"liu": make_rank_kernel([f_liu]), "ideal": make_rank_kernel([f_ideal]), "minmax": make_rank_kernel([f_minmax]),
           "comono": make_interval_kernel(lambda x: 0*x), "new": K_new}
K = kernels[name]
x = 1/np.sqrt(2); hb = lambda t: -(t*np.log2(t)+(1-t)*np.log2(1-t))
print("class ceiling (two-point adversary at x=1/sqrt2): c <= %.6f" % (1 - x*hb(x)/hb(x*x)), flush=True)
for beta in betas:
    t0 = time.time()
    c, z = c_max(K, beta, m=m, restarts=30, lo=0.3815, hi=0.3835, tol=3e-6, seed=1, verbose=False)
    print("kernel=%s lam=%.3f beta=%.3f m=%d : c_max=%.6f  worst adversary: %s  (%.0fs)" % (name, lam, beta, m, c, describe(z, m) if z is not None else None, time.time()-t0), flush=True)
