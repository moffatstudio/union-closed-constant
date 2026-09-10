import numpy as np
w=0.810222; c=0.38284; C=1.00005
r=(1-w)/w
def h(x):
    x=np.asarray(x,dtype=float)
    out=np.zeros_like(x)
    m=(x>0)&(x<1)
    xx=x[m]
    out[m]=-(xx*np.log2(xx)+(1-xx)*np.log2(1-xx))
    return out
t0=0.006306216520946655
# ratio on the square (0,t0]^2
def ratio(t,tp):
    tau=t+tp-t*tp
    return (h(t)+h(tp)-h(tau))/np.sqrt(h(t)*h(tp))
# log-spaced grid
u=np.concatenate([np.logspace(-14,np.log10(t0),4000)])
T,TP=np.meshgrid(u,u)
R=ratio(T,TP)
print("max ratio on square:",R.max(),"  r =",r)
i,j=np.unravel_index(np.argmax(R),R.shape)
print("argmax t,t' =",T[i,j],TP[i,j], " t0=",t0)
# check ratio along diagonal is increasing
d=ratio(u,u)
print("diag monotone increasing:",np.all(np.diff(d)>-1e-15))
print("diag values at few t:",[(f"{x:.2e}",float(ratio(np.array([x]),np.array([x])))) for x in [1e-12,1e-8,1e-4,1e-3,t0]])
# fix t'=t0, vary t
row=ratio(u,np.full_like(u,t0))
print("max over t with t'=t0:",row.max(),"at t=",u[np.argmax(row)])
