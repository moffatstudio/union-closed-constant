import numpy as np
from math import sqrt
def h(p):
    p=np.asarray(p,float); o=np.zeros_like(p); m=(p>0)&(p<1)
    o[m]=-p[m]*np.log2(p[m])-(1-p[m])*np.log2(1-p[m]); return o
def fid(x):
    x=np.asarray(x,float)
    return np.where(x<=0.5,x,np.where(x<=1/sqrt(2),np.sqrt(np.maximum(0.5-x*x,0.0)),0.0))
r2=1/sqrt(2)
def grid(n_base,n_ref,halfwidth):
    a=np.linspace(1e-6,1-1e-6,n_base)
    b=np.linspace(max(1e-6,r2-halfwidth),min(1-1e-6,r2+halfwidth),n_ref)
    x=np.unique(np.concatenate([a,b]))
    # trapezoid-ish weights
    e=np.concatenate([[x[0]],(x[:-1]+x[1:])/2,[x[-1]]])
    w=np.diff(e)
    return x,w
def count(x,w):
    f=fid(x); K=h(np.outer(x,x)+np.outer(f,f))
    A=np.sqrt(w)[:,None]*K*np.sqrt(w)[None,:]
    C=np.array([np.sqrt(w), x*np.sqrt(w)]).T
    Q,_=np.linalg.qr(C); P=np.eye(len(x))-Q@Q.T
    ev=np.linalg.eigvalsh(P@A@P)
    return ev
for nb,nr,hw in [(1000,0,0),(1000,1500,0.02),(1000,2500,0.005),(1000,2500,0.001),(1000,3000,0.0002),(2000,3000,1e-5)]:
    x,w=grid(nb,nr,hw) if nr else grid(nb,2,1e-9)
    ev=count(x,w)
    pos=ev[ev>1e-11]
    print("base=%d refine=%d hw=%.0e  N=%d  #pos>1e-11=%d  top4=%s"%(nb,nr,hw,len(x),len(pos),["%.3e"%v for v in ev[-4:]]))
