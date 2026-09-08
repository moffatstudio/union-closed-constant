import time, numpy as np
from floor_scan import search, e_h, describe, m
t0=time.time(); best=(9,None)
for seed in range(10):
    val,z=search(1e-7, restarts=500, seed=100+seed)
    if val<best[0]: best=(val,z)
    print("batch %d (500 restarts): min ratio=%.8f  running best=%.8f  (%.0fs)"%(seed,val,best[0],time.time()-t0), flush=True)
print("FINAL 5000 restarts + seeds, floor 1e-7, m=4, c=0.38284, beta=0.189778: min ratio=%.8f  %s"%(best[0],describe(best[1],m)))
