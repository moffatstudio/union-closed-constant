import numpy as np, sys, json, time
sys.path.insert(0, __import__('os').path.dirname(__import__('os').path.abspath(__file__)))
from evaluator import *

def seeds(n, c, rng, nrand):
    """structured seeds + random restarts, each as a z-vector"""
    S = []
    def mk(a0, p0, a1, p1, q):
        a0 = list(a0)+[0.0]*(n-len(a0)); p0 = list(p0)+[1e-9]*(n-len(p0))
        a1 = list(a1)+[0.0]*(n-len(a1)); p1 = list(p1)+[1e-9]*(n-len(p1))
        l0 = np.log(np.maximum(p0,1e-12)); l1 = np.log(np.maximum(p1,1e-12))
        return np.concatenate([a0, l0, a1, l1, [q]])
    # two-point laws
    for x in np.linspace(0.60, 0.75, 16):
        p = min(1.0,(1-c)/x)
        S.append(mk([x,0.0],[p,1-p],[x,0.0],[p,1-p],0.0))
        S.append(mk([x,0.0],[p,1-p],[1.0],[1.0],0.05))
    # hiding laws
    for d in [1e-2,1e-3,1e-4]:
        for y in [0.05,0.2,0.5,0.7,0.9]:
            qq = 1-c
            S.append(mk([0.0,y],[1-d,d],[1.0],[1.0],qq))
    # Liu / Cambie laws
    S.append(mk([0.6908,0.0],[0.8936,0.1064],[1.0],[1.0],0.0))
    S.append(mk([1/np.sqrt(2),0.0],[(1-c)*np.sqrt(2),1-(1-c)*np.sqrt(2)],[1.0],[1.0],0.0))
    S.append(mk([0.690908,0.0],[(1-c)/0.690908,1-(1-c)/0.690908],[1.0],[1.0],0.0))
    # mixtures: two-point + tiny atom
    for d in [1e-2,1e-3]:
        for y in [0.2,0.5,0.7]:
            x=0.6909; p=(1-c)/x
            S.append(mk([x,0.0,y],[p*(1-d),(1-p)*(1-d),d],[1.0],[1.0],0.0))
            S.append(mk([x,0.0,y],[p*(1-d),(1-p)*(1-d),d],[1.0],[1.0],0.3))
    # random restarts
    for _ in range(nrand):
        a0 = rng.random(n); a1 = rng.random(n)
        p0 = rng.dirichlet(np.ones(n)); p1 = rng.dirichlet(np.ones(n))
        S.append(mk(a0,p0,a1,p1,rng.random()))
    return S

def run(n, w, c, f, nrand=320, seed=0, hfloor=1e-3):
    rng = np.random.default_rng(seed)
    best = (np.inf, None)
    for z0 in seeds(n, c, rng, nrand):
        v, z = local_min(np.asarray(z0,float), n, w, f, c, hfloor)
        if v < best[0]: best = (v, z.copy())
    return best

if __name__ == '__main__':
    mode = sys.argv[1]
    if mode == 'liu':
        w=0.899947; c=0.382709087918741; f=f_liu
    else:
        w=0.810222; c=float(sys.argv[3]) if len(sys.argv)>3 else 0.38284; f=f_ideal
    n = int(sys.argv[2])
    t=time.time()
    v,z = run(n,w,c,f)
    print(json.dumps({'mode':mode,'n':n,'w':w,'c':c,'min_ratio':v,
                      'minimiser':describe(z,n),'secs':round(time.time()-t,1)}))
