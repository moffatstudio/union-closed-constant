import numpy as np
w=0.810222; c=0.38284; C=1.00005; r=(1-w)/w; ln2=np.log(2)
def h(x):
    x=np.asarray(x,float); out=np.zeros_like(x); m=(x>0)&(x<1); xx=x[m]
    out[m]=-(xx*np.log2(xx)+(1-xx)*np.log2(1-xx)); return out
t0=0.006
# (b) h(a) <= 2 sqrt(a(1-a))
a=np.linspace(1e-12,1-1e-12,2000001)
print("(b) max h(a)-2sqrt(a(1-a)) =", (h(a)-2*np.sqrt(a*(1-a))).max())
# (star) on the square, log grid
u=np.logspace(-16,np.log10(t0),3000)
T,TP=np.meshgrid(u,u)
tau=T+TP-T*TP
Lam=h(T)+h(TP)-h(tau)
lhs=w*Lam; rhs=(1-w)*np.sqrt(h(T)*h(TP))
print("(star) min slack rhs-lhs =", (rhs-lhs).min(), " min ratio lhs/rhs=",(lhs/rhs).max())
# also check sufficient chain: Lam <= 2sqrt(tt') + tt'(Ltil(min)+1+min/ln2)
def Lt(x): return np.log2(1/x)+(1-x)/ln2
mn=np.minimum(T,TP)
bound=2*np.sqrt(T*TP)+T*TP*(Lt(mn)+1+mn/ln2)
print("chain valid (Lam<=bound):", np.all(Lam<=bound+1e-18), " max Lam-bound=",(Lam-bound).max())
print("sufficient cond holds:", np.all(w*bound<=(1-w)*np.sqrt(h(T)*h(TP))))
# h(u)>=u*Ltilde(u)
print("h>=u Ltil:", np.all(h(u)>=u*Lt(u)-1e-18))
# y/h(y) increasing, rho
y=np.linspace(1e-9,1-t0,2000000)
ratio=y/h(y)
print("y/h(y) increasing:", np.all(np.diff(ratio)>=-1e-12), " rho=",(1-t0)/h(np.array([t0]))[0], " max=",ratio.max())
G=(1-c)-C/(2*w); eps0=G*h(np.array([t0]))[0]/(1-t0)
print("G=",G," eps0=",eps0)
