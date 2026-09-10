import numpy as np, itertools
w=0.810222; c=0.38284; C=1.00005
def h(x):
    x=np.asarray(x,float); out=np.zeros_like(x); m=(x>0)&(x<1); xx=x[m]
    out[m]=-(xx*np.log2(xx)+(1-xx)*np.log2(1-xx)); return out
def fv(x):
    x=np.asarray(x,float); o=np.zeros_like(x)
    m1=x<=0.5; o[m1]=np.minimum(x[m1],1-x[m1])
    m2=(x>0.5)&(x<=2**-0.5); o[m2]=np.sqrt(np.maximum(0.5-x[m2]**2,0))
    return o
def Kup(xs,m,Wk):
    n=len(xs); best=float(m@Wk@m)
    for g in range(2,n+1):
        for lab in itertools.product(range(g),repeat=n):
            if len(set(lab))<g: continue
            tot=0.0
            for j in range(g):
                idx=[i for i in range(n) if lab[i]==j]
                a=m[idx]; p=a.sum()
                if p>0: tot+=float(a@Wk[np.ix_(idx,idx)]@a)/p
            best=min(best,tot)
    return best
def Rval(xs,m):
    E=float(m@h(xs))
    if E<=0: return np.inf,0.0
    Wh=h(xs[:,None]*xs[None,:]); Wk=h(np.clip(xs[:,None]*xs[None,:]+fv(xs)[:,None]*fv(xs)[None,:],0,1))
    return (w*float(m@Wh@m)+(1-w)*Kup(xs,m,Wk))/E, E
# family: sigma d_1 + z d_y + m0 d_0, mean exactly 1-c  => sigma = 1-c - z*y
rows=[]
ys=np.unique(np.concatenate([np.logspace(-12,-0.31,300), 1-np.logspace(-12,-0.31,300), np.linspace(0.02,0.98,200)]))
for y in ys:
    hy=float(h(np.array([y]))[0])
    for E in [1e-12,1e-9,1e-7,7.6e-7,1e-6,1e-5,1e-4,1e-3]:
        z=E/hy
        sig=1-c-z*y
        if z<=0 or sig<=0 or sig+z>1: continue
        xs=np.array([0.0,y,1.0]); m=np.array([1-sig-z,z,sig])
        r_,_=Rval(xs,m); rows.append((r_,y,E,z))
rows.sort()
print(" 2w(1-c)=",2*w*(1-c)," C=",C)
print("worst 12 (R, y, E, z):")
for t in rows[:12]: print(f"  R={t[0]:.10f}  y={t[1]:.8g}  E={t[2]:.1e}  z={t[3]:.3e}")
print("min R overall:",rows[0][0], " below C?",rows[0][0]<C)
# 4-atom: add a near-1 atom too
rows2=[]
for y in ys[::7]:
  hy=float(h(np.array([y]))[0])
  for t in [1e-9,1e-6,1e-4,0.006,0.05]:
    ht=float(h(np.array([t]))[0])
    for E in [1e-7,7.6e-7,1e-5,1e-4]:
      for frac in [0.0,0.3,0.7,1.0]:
        Eb=E*(1-frac); En=E*frac
        z=Eb/hy; s=En/ht
        sig=1-c-z*y-s*(1-t)
        if z<0 or s<0 or sig<=0 or sig+z+s>1: continue
        xs=np.array([0.0,y,1-t,1.0]); m=np.array([1-sig-z-s,z,s,sig])
        r_,_=Rval(xs,m); rows2.append((r_,y,t,E,frac))
rows2.sort()
print("4-atom worst 8 (R,y,t,E,frac):")
for t in rows2[:8]: print(f"  R={t[0]:.10f} y={t[1]:.6g} t={t[2]:.1e} E={t[3]:.1e} frac={t[4]}")
print("min:",rows2[0][0]," below C?",rows2[0][0]<C)
